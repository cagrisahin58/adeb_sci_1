"""General trainer class for model training."""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Optional, Dict, Any, Callable
from pathlib import Path
from tqdm import tqdm
import time

from ..utils.checkpoint import save_checkpoint, load_checkpoint


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
        save_every: int = 0,
        optimizer_name: str = "auto",
        lr_schedule: str = "cosine",
        max_train_batches: int = 0,
        lr_warmup_epochs: int = 0,
        stop_epoch: int = 0,
        mixup_fn: Optional[Callable] = None,
        train_criterion: Optional[nn.Module] = None,
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
        self.save_every = save_every
        # Konsey B1: smoke/pilot icin epok basina en fazla N egitim batch'i (0 = sinirsiz)
        self.max_train_batches = max_train_batches
        # Curutme B (08.11.2026): istege bagli temiz asama ekleri. Hepsi varsayilanda
        # kapalidir ve kapaliyken egitim yolu eski koddakiyle ayni islemleri ayni sirayla
        # yapar (regresyon: results/q1/curutme_2026-11-08/_duman/regresyon_*.txt).
        #   stop_epoch: >0 ise egitim bu epokta durur, LR cizelgesi `epochs` uzerinden kalir
        #   mixup_fn: timm.data.Mixup (yumusak hedef uretir); train_criterion yumusak hedefi alir
        #   train_criterion: yalniz egitim kaybi (or. etiket yumusatmali CE); degerlendirme
        #       kaybi her zaman self.criterion'dur
        self.stop_epoch = stop_epoch
        self.mixup_fn = mixup_fn

        # Device
        self.device = device or (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.model = self.model.to(self.device)

        # Loss function
        self.criterion = criterion or nn.CrossEntropyLoss()
        self.train_criterion = train_criterion  # None -> self.criterion (eski davranis)

        # Optimizer - use AdamW for ViT models, SGD for CNNs
        if optimizer is not None:
            self.optimizer = optimizer
        elif optimizer_name == "adamw":
            # Konsey B1: iyileyici bayrakla zorlanir (sinif adina bakilmaz);
            # ViT temiz tarifiyle ayni AdamW agirlik azaltmasi (0.05), LR tavani yok
            self.optimizer = optim.AdamW(self.model.parameters(), lr=lr, weight_decay=0.05)
            if self.verbose:
                print(f"Using AdamW optimizer (forced, lr={lr}, wd=0.05)")
        elif optimizer_name == "sgd":
            self.optimizer = optim.SGD(self.model.parameters(), lr=lr,
                                       momentum=momentum, weight_decay=weight_decay)
            if self.verbose:
                print(f"Using SGD optimizer (forced, lr={lr})")
        elif optimizer_name != "auto":
            raise ValueError(f"Bilinmeyen optimizer_name: {optimizer_name}")
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

        # Scheduler (varsayilan: cosine, T_max=epochs -- eski davranis)
        if scheduler is not None:
            self.scheduler = scheduler
        elif lr_schedule == "cosine" and lr_warmup_epochs > 0:
            # Curutme B: AdversarialTrainer'daki lr_warmup ile ayni kurulum
            # (LinearLR 0.1 -> 1.0, ardindan cosine T_max = epochs - isinma)
            warm = optim.lr_scheduler.LinearLR(
                self.optimizer, start_factor=0.1, end_factor=1.0,
                total_iters=lr_warmup_epochs,
            )
            cos = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=max(1, epochs - lr_warmup_epochs),
            )
            self.scheduler = optim.lr_scheduler.SequentialLR(
                self.optimizer, [warm, cos], milestones=[lr_warmup_epochs],
            )
        elif lr_schedule == "cosine":
            self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer,
                T_max=epochs,
            )
        elif lr_schedule == "constant":
            self.scheduler = optim.lr_scheduler.LambdaLR(self.optimizer, lambda _e: 1.0)
        else:
            raise ValueError(f"Bilinmeyen lr_schedule: {lr_schedule}")

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

        for b_idx, (inputs, labels) in enumerate(iterator):
            if self.max_train_batches and b_idx >= self.max_train_batches:
                break
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            self.optimizer.zero_grad()

            if self.mixup_fn is not None and inputs.size(0) % 2 == 0:
                # Curutme B: karisik girdi ve yumusak hedef; dogruluk ozgun etikete gore
                # (egitim dogrulugu bu kipte yalniz izleme amaclidir)
                inputs, targets = self.mixup_fn(inputs, labels)
                outputs = self.model(inputs)
                loss = self.train_criterion(outputs, targets)
            elif self.train_criterion is not None and self.mixup_fn is None:
                # (mixup acikken tek sayili batch yumusak hedef alamaz; o batch asagidaki
                # sert etiketli self.criterion'a duser. 48000/128 bolmesinde tek batch olusmaz.)
                outputs = self.model(inputs)
                loss = self.train_criterion(outputs, labels)
            else:
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

        n_batches = (min(self.max_train_batches, len(self.train_loader))
                     if self.max_train_batches else len(self.train_loader))
        return {
            "train_loss": running_loss / n_batches,
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

    def train(self, resume: bool = False) -> Dict[str, list]:
        """
        Run full training loop.

        Args:
            resume: True ise checkpoint_dir/last.pth'tan devam eder
                (kesinti sonrasi). last.pth yoksa sifirdan baslar.

        Returns:
            Training history dictionary
        """
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()

        # Kesinti sonrasi devam (resume) - AdversarialTrainer ile ayni desen
        start_epoch = 0
        last_path = self.checkpoint_dir / "last.pth"
        if resume and last_path.exists():
            ckpt = load_checkpoint(
                str(last_path), self.model, self.optimizer, self.scheduler, self.device
            )
            start_epoch = ckpt.get("epoch", -1) + 1
            self.best_acc = ckpt.get("best_acc", ckpt.get("accuracy", 0.0) or 0.0)
            saved_history = ckpt.get("history")
            if saved_history:
                self.history = saved_history
            if self.verbose:
                print(f"Resuming clean training from epoch {start_epoch} "
                      f"(best acc so far: {self.best_acc:.2f}%)")

        if self.verbose:
            print(f"Training on {self.device}")
            print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")

        # Resume'da dongu hic donmese bile TRAINING_COMPLETE dogru epochs_run yazsin
        if start_epoch > 0:
            self.current_epoch = start_epoch - 1

        test_metrics = {"test_acc": 0.0}
        end_epoch = (min(self.epochs, self.stop_epoch) if self.stop_epoch > 0
                     else self.epochs)
        for epoch in range(start_epoch, end_epoch):
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

            # Periyodik checkpoint (E3 yorunge noktalari; yalniz agirlik)
            if self.save_every > 0 and (epoch + 1) % self.save_every == 0:
                ep_dir = self.checkpoint_dir / "epochs"
                ep_dir.mkdir(parents=True, exist_ok=True)
                ep_tmp = ep_dir / f"epoch_{epoch + 1:03d}.pth.tmp"
                torch.save({
                    "model_state_dict": self.model.state_dict(),
                    "epoch": epoch,
                    "test_acc": test_metrics["test_acc"],
                }, ep_tmp)
                ep_tmp.replace(ep_dir / f"epoch_{epoch + 1:03d}.pth")

            # Kesintiye dayanikli last.pth (atomik: .tmp'ye yaz, tasi)
            if self.save_last:
                tmp_path = self.checkpoint_dir / "last.pth.tmp"
                save_checkpoint(
                    self.model,
                    tmp_path,
                    self.optimizer,
                    self.scheduler,
                    epoch,
                    test_metrics["test_acc"],
                    extra_info={
                        "best_acc": self.best_acc,
                        "history": self.history,
                    },
                )
                tmp_path.replace(self.checkpoint_dir / "last.pth")

        # Tamamlanma isareti: orkestrasyon scripti yarim egitimi tam sanmasin
        marker = (f"epochs_run={self.current_epoch + 1}\n"
                  f"best_acc={self.best_acc:.4f}\n")
        if self.stop_epoch > 0:
            # Curutme B: eski marker bicimi korunur, yalniz stop_epoch verildiginde eklenir
            marker += f"stop_epoch={self.stop_epoch}\n"
        (self.checkpoint_dir / "TRAINING_COMPLETE").write_text(marker)

        elapsed_time = time.time() - start_time
        if self.verbose:
            print(f"\nTraining completed in {elapsed_time / 60:.2f} minutes")
            print(f"Best test accuracy: {self.best_acc:.2f}%")

        return self.history
