"""General trainer class for model training."""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Optional, Dict, Any, Callable
from pathlib import Path
from tqdm import tqdm
import time

from ..utils.checkpoint import save_checkpoint


class Trainer:
    """
    General trainer for clean model training.

    Handles the training loop, validation, checkpointing, and logging.
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        test_loader: DataLoader,
        optimizer: Optional[optim.Optimizer] = None,
        scheduler: Optional[Any] = None,
        criterion: Optional[nn.Module] = None,
        device: Optional[torch.device] = None,
        epochs: int = 50,
        lr: float = 0.1,
        momentum: float = 0.9,
        weight_decay: float = 5e-4,
        checkpoint_dir: str = "./models",
        save_best: bool = True,
        save_last: bool = True,
        verbose: bool = True,
    ):
        """
        Initialize the trainer.

        Args:
            model: Model to train
            train_loader: Training data loader
            test_loader: Test data loader
            optimizer: Optimizer (None to create default SGD)
            scheduler: Learning rate scheduler (None to create CosineAnnealingLR)
            criterion: Loss function (None for CrossEntropyLoss)
            device: Device to train on
            epochs: Number of training epochs
            lr: Learning rate (used if optimizer is None)
            momentum: SGD momentum (used if optimizer is None)
            weight_decay: Weight decay (used if optimizer is None)
            checkpoint_dir: Directory to save checkpoints
            save_best: Whether to save best model
            save_last: Whether to save last model
            verbose: Whether to print progress
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

        # Loss function
        self.criterion = criterion or nn.CrossEntropyLoss()

        # Optimizer - use AdamW for ViT models, SGD for CNNs
        if optimizer is not None:
            self.optimizer = optimizer
        else:
            # Check if model is a ViT (by checking class name or module name)
            model_name = model.__class__.__name__.lower()
            is_vit = 'vit' in model_name or 'vision' in model_name or 'transformer' in model_name
            
            if is_vit:
                # ViT models work better with AdamW and lower LR
                effective_lr = min(lr, 1e-3)  # Cap LR at 1e-3 for ViT
                self.optimizer = optim.AdamW(
                    self.model.parameters(),
                    lr=effective_lr,
                    weight_decay=0.05,
                )
                if self.verbose:
                    print(f"Using AdamW optimizer for ViT (lr={effective_lr})")
            else:
                # CNN models work well with SGD
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
        self.best_acc = 0.0
        self.current_epoch = 0
        self.history: Dict[str, list] = {
            "train_loss": [],
            "train_acc": [],
            "test_loss": [],
            "test_acc": [],
            "lr": [],
        }

    def train_epoch(self) -> Dict[str, float]:
        """
        Train for one epoch.

        Returns:
            Dictionary with training loss and accuracy
        """
        self.model.train()
        running_loss = 0.0
        correct = 0
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

            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)

            loss.backward()
            self.optimizer.step()

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            if self.verbose and hasattr(iterator, "set_postfix"):
                iterator.set_postfix({
                    "loss": running_loss / (total / inputs.size(0)),
                    "acc": 100.0 * correct / total,
                })

        return {
            "train_loss": running_loss / len(self.train_loader),
            "train_acc": 100.0 * correct / total,
        }

    @torch.no_grad()
    def evaluate(self) -> Dict[str, float]:
        """
        Evaluate on test set.

        Returns:
            Dictionary with test loss and accuracy
        """
        self.model.eval()
        test_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in self.test_loader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)

            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        return {
            "test_loss": test_loss / len(self.test_loader),
            "test_acc": 100.0 * correct / total,
        }

    def train(self) -> Dict[str, list]:
        """
        Run full training loop.

        Returns:
            Training history dictionary
        """
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()

        if self.verbose:
            print(f"Training on {self.device}")
            print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")

        for epoch in range(self.epochs):
            self.current_epoch = epoch

            # Train
            train_metrics = self.train_epoch()

            # Evaluate
            test_metrics = self.evaluate()

            # Update scheduler
            self.scheduler.step()

            # Record history
            self.history["train_loss"].append(train_metrics["train_loss"])
            self.history["train_acc"].append(train_metrics["train_acc"])
            self.history["test_loss"].append(test_metrics["test_loss"])
            self.history["test_acc"].append(test_metrics["test_acc"])
            self.history["lr"].append(self.optimizer.param_groups[0]["lr"])

            # Print progress
            if self.verbose:
                print(
                    f"Epoch {epoch + 1}/{self.epochs} - "
                    f"Train Loss: {train_metrics['train_loss']:.4f}, "
                    f"Train Acc: {train_metrics['train_acc']:.2f}%, "
                    f"Test Acc: {test_metrics['test_acc']:.2f}%"
                )

            # Save best model
            if self.save_best and test_metrics["test_acc"] > self.best_acc:
                self.best_acc = test_metrics["test_acc"]
                save_checkpoint(
                    self.model,
                    self.checkpoint_dir / "best.pth",
                    self.optimizer,
                    self.scheduler,
                    epoch,
                    test_metrics["test_acc"],
                )
                if self.verbose:
                    print(f"  Best model saved! Accuracy: {self.best_acc:.2f}%")

        # Save last model
        if self.save_last:
            save_checkpoint(
                self.model,
                self.checkpoint_dir / "last.pth",
                self.optimizer,
                self.scheduler,
                self.epochs - 1,
                test_metrics["test_acc"],
            )

        elapsed_time = time.time() - start_time
        if self.verbose:
            print(f"\nTraining completed in {elapsed_time / 60:.2f} minutes")
            print(f"Best test accuracy: {self.best_acc:.2f}%")

        return self.history
