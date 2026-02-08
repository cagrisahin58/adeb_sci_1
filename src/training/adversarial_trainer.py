"""Adversarial trainer for robust model training."""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Optional, Dict, Any, Union
from pathlib import Path
from tqdm import tqdm
import time

from ..utils.checkpoint import save_checkpoint
from ..defenses.base import TrainingDefense
from ..defenses.adversarial_training import AdversarialTraining
from ..defenses.trades import TRADESDefense
from ..defenses.mart import MARTDefense


class AdversarialTrainer:
    """
    Trainer for adversarial training methods.

    Supports various adversarial training methods including:
    - Standard adversarial training (Madry et al.)
    - TRADES (Zhang et al.)
    - MART (Wang et al.)
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        test_loader: DataLoader,
        defense: Optional[Union[TrainingDefense, str]] = None,
        optimizer: Optional[optim.Optimizer] = None,
        scheduler: Optional[Any] = None,
        device: Optional[torch.device] = None,
        epochs: int = 25,
        lr: float = 0.01,
        momentum: float = 0.9,
        weight_decay: float = 5e-4,
        eps: float = 8 / 255,
        alpha: float = 2 / 255,
        steps: int = 10,
        beta: float = 6.0,
        checkpoint_dir: str = "./models",
        save_best: bool = True,
        save_last: bool = True,
        verbose: bool = True,
        patience: int = 0,
        min_delta: float = 0.1,
    ):
        """
        Initialize the adversarial trainer.

        Args:
            model: Model to train
            train_loader: Training data loader
            test_loader: Test data loader
            defense: Defense method (TrainingDefense instance or name string)
            optimizer: Optimizer (None to create default SGD)
            scheduler: Learning rate scheduler
            device: Device to train on
            epochs: Number of training epochs
            lr: Learning rate
            momentum: SGD momentum
            weight_decay: Weight decay
            eps: Maximum perturbation for attacks
            alpha: Step size for PGD
            steps: Number of PGD steps
            beta: TRADES/MART beta parameter
            checkpoint_dir: Directory to save checkpoints
            save_best: Whether to save best model
            save_last: Whether to save last model
            verbose: Whether to print progress
            patience: Early stopping patience (0 = disabled)
            min_delta: Minimum improvement to reset patience counter
        """
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.epochs = epochs
        self.checkpoint_dir = Path(checkpoint_dir)
        self.save_best = save_best
        self.save_last = save_last
        self.verbose = verbose

        # Device
        self.device = device or (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.model = self.model.to(self.device)

        # Create or use provided defense
        if defense is None or defense == "adversarial_training":
            self.defense = AdversarialTraining(
                model=self.model,
                eps=eps,
                alpha=alpha,
                steps=steps,
                device=self.device,
            )
        elif defense == "trades":
            self.defense = TRADESDefense(
                model=self.model,
                beta=beta,
                eps=eps,
                alpha=alpha,
                steps=steps,
                device=self.device,
            )
        elif defense == "mart":
            self.defense = MARTDefense(
                model=self.model,
                beta=beta,
                eps=eps,
                alpha=alpha,
                steps=steps,
                device=self.device,
            )
        elif isinstance(defense, TrainingDefense):
            self.defense = defense
        else:
            raise ValueError(f"Unknown defense: {defense}")

        # Optimizer - use AdamW for ViT models, SGD for CNNs
        if optimizer is not None:
            self.optimizer = optimizer
        else:
            model_name = model.__class__.__name__.lower()
            is_vit = 'vit' in model_name or 'vision' in model_name or 'transformer' in model_name
            
            if is_vit:
                effective_lr = min(lr, 1e-3)
                self.optimizer = optim.AdamW(
                    self.model.parameters(),
                    lr=effective_lr,
                    weight_decay=0.05,
                )
                if self.verbose:
                    print(f"Using AdamW optimizer for ViT (lr={effective_lr})")
            else:
                self.optimizer = optim.SGD(
                    self.model.parameters(),
                    lr=lr,
                    momentum=momentum,
                    weight_decay=weight_decay,
                )

        # Scheduler
        self.scheduler = scheduler or optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=epochs,
        )

        # Training state
        self.best_adv_acc = 0.0
        self.current_epoch = 0
        self.history: Dict[str, list] = {
            "train_loss": [],
            "clean_acc": [],
            "adv_acc": [],
            "lr": [],
        }

        # Early stopping
        self.patience = patience
        self.min_delta = min_delta
        self.patience_counter = 0
        self.early_stopped = False

    def train_epoch(self) -> Dict[str, float]:
        """
        Train for one epoch with adversarial training.

        Returns:
            Dictionary with training loss
        """
        self.model.train()
        running_loss = 0.0
        total = 0

        iterator = self.train_loader
        if self.verbose:
            iterator = tqdm(
                iterator,
                desc=f"Epoch {self.current_epoch + 1}/{self.epochs}",
                leave=True,
            )

        for inputs, labels in iterator:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            self.optimizer.zero_grad()

            # Compute defense loss
            loss = self.defense.get_loss(self.model, inputs, labels)

            loss.backward()

            # Gradient clipping to prevent explosion
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=10.0)
            self.optimizer.step()

            # Skip NaN losses
            if torch.isnan(loss) or torch.isinf(loss):
                continue
            # Skip if loss is NaN or Inf
            if torch.isnan(loss) or torch.isinf(loss):
                print(f"Warning: NaN/Inf loss detected, skipping batch")
                continue
            running_loss += loss.item()
            total += labels.size(0)

            if self.verbose and hasattr(iterator, "set_postfix"):
                iterator.set_postfix({
                    "loss": running_loss / (len(iterator) if hasattr(iterator, '__len__') else 1),
                })

        return {
            "train_loss": running_loss / len(self.train_loader),
        }

    @torch.no_grad()
    def evaluate_clean(self) -> float:
        """
        Evaluate on clean test set.

        Returns:
            Clean accuracy percentage
        """
        self.model.eval()
        correct = 0
        total = 0

        for inputs, labels in self.test_loader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            outputs = self.model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        return 100.0 * correct / total

    def evaluate_adversarial(self, eps: float = 8 / 255) -> float:
        """
        Evaluate on adversarial test set.

        Args:
            eps: Perturbation size for evaluation

        Returns:
            Adversarial accuracy percentage
        """
        self.model.eval()
        correct = 0
        total = 0

        for inputs, labels in self.test_loader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            # Generate adversarial examples
            if hasattr(self.defense, "generate_adversarial"):
                if "labels" in self.defense.generate_adversarial.__code__.co_varnames:
                    adv_inputs = self.defense.generate_adversarial(inputs, labels)
                else:
                    adv_inputs = self.defense.generate_adversarial(inputs)
            else:
                # Fallback to simple PGD
                adv_inputs = self._simple_pgd(inputs, labels, eps)

            with torch.no_grad():
                outputs = self.model(adv_inputs)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

        return 100.0 * correct / total

    def _simple_pgd(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        eps: float,
        steps: int = 10,
        alpha: float = 2 / 255,
    ) -> torch.Tensor:
        """Simple PGD attack for evaluation."""
        images = images.detach()
        original_images = images.clone()

        delta = torch.empty_like(images).uniform_(-eps, eps)
        delta = torch.clamp(original_images + delta, 0, 1) - original_images

        for _ in range(steps):
            delta.requires_grad = True

            outputs = self.model(original_images + delta)
            loss = nn.CrossEntropyLoss()(outputs, labels)

            loss.backward()

            # Gradient clipping to prevent explosion
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=10.0)

            grad = delta.grad.sign()
            delta = delta.detach() + alpha * grad
            delta = torch.clamp(delta, -eps, eps)
            delta = torch.clamp(original_images + delta, 0, 1) - original_images

        return original_images + delta

    def train(self) -> Dict[str, list]:
        """
        Run full adversarial training loop.

        Returns:
            Training history dictionary
        """
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()

        if self.verbose:
            print(f"Adversarial training on {self.device}")
            print(f"Defense method: {self.defense.name}")
            print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")

        for epoch in range(self.epochs):
            self.current_epoch = epoch

            # Train
            train_metrics = self.train_epoch()

            # Evaluate
            clean_acc = self.evaluate_clean()
            adv_acc = self.evaluate_adversarial()

            # Update scheduler
            self.scheduler.step()

            # Record history
            self.history["train_loss"].append(train_metrics["train_loss"])
            self.history["clean_acc"].append(clean_acc)
            self.history["adv_acc"].append(adv_acc)
            self.history["lr"].append(self.optimizer.param_groups[0]["lr"])

            # Print progress
            if self.verbose:
                print(
                    f"Epoch {epoch + 1}/{self.epochs} - "
                    f"Loss: {train_metrics['train_loss']:.4f}, "
                    f"Clean: {clean_acc:.2f}%, "
                    f"Adv: {adv_acc:.2f}%"
                )

            # Save best model (based on adversarial accuracy)
            if self.save_best and adv_acc > self.best_adv_acc + self.min_delta:
                self.best_adv_acc = adv_acc
                self.patience_counter = 0
                save_checkpoint(
                    self.model,
                    self.checkpoint_dir / "best.pth",
                    self.optimizer,
                    self.scheduler,
                    epoch,
                    adv_acc,
                    extra_info={"clean_acc": clean_acc},
                )
                if self.verbose:
                    print(f"  Best model saved! Adv accuracy: {self.best_adv_acc:.2f}%")
            elif self.patience > 0:
                self.patience_counter += 1
                if self.verbose:
                    print(f"  No improvement ({self.patience_counter}/{self.patience})")
                if self.patience_counter >= self.patience:
                    self.early_stopped = True
                    if self.verbose:
                        print(f"\nEarly stopping triggered at epoch {epoch + 1}")
                    break

        # Save last model
        if self.save_last:
            save_checkpoint(
                self.model,
                self.checkpoint_dir / "last.pth",
                self.optimizer,
                self.scheduler,
                self.epochs - 1,
                adv_acc,
                extra_info={"clean_acc": clean_acc},
            )

        elapsed_time = time.time() - start_time
        if self.verbose:
            print(f"\nTraining completed in {elapsed_time / 60:.2f} minutes")
            print(f"Best adversarial accuracy: {self.best_adv_acc:.2f}%")

        return self.history
