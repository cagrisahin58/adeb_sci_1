"""Adversarial trainer for robust model training."""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Optional, Dict, Any, Union
from pathlib import Path
from tqdm import tqdm
import time

from ..utils.checkpoint import save_checkpoint, load_checkpoint
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
        val_loader: Optional[DataLoader] = None,
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
        save_every: int = 0,
        grad_clip: float = 10.0,
        vit_lr_cap: Optional[float] = 1e-3,
        eps_warmup_epochs: int = 0,
        lr_warmup_epochs: int = 0,
    ):
        """
        Initialize the adversarial trainer.

        Args:
            model: Model to train
            train_loader: Training data loader
            test_loader: Test data loader
            val_loader: Validation loader for model selection / early stopping.
                Saglanirsa best.pth secimi ve early stopping bu set uzerinden
                yapilir ve test seti egitim boyunca HIC kullanilmaz (M7:
                test-set selection leakage onlenir). None ise eski davranis
                (test seti ile secim) korunur.
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
            save_every: Her N epokta periyodik checkpoint kaydet
                (checkpoint_dir/epochs/epoch_XXX.pth, yalniz model agirliklari;
                E3 kalibrasyon egrisi yorunge noktalari icin). 0 = kapali.
            grad_clip: Gradyan kirpma L2 max-norm (ViT-S icin 1.0 onerilir;
                10.0 fiilen devre disi demektir).
            vit_lr_cap: ViT'lerde LR ust siniri (None = sinirsiz). Kalibrasyon
                deneylerinde kasitli dusuk/yuksek LR icin parametrik.
            eps_warmup_epochs: Ilk N epokta egitim eps'i 0'dan hedefe lineer
                artar (SVHN 8/255 ve ViT-S kararsizligi sigortasi).
                DEGERLENDIRME her zaman tam eps'te yapilir.
            lr_warmup_epochs: Ilk N epokta lineer LR isinmasi (sonra cosine).
        """
        self.model = model
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.val_loader = val_loader
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
                effective_lr = min(lr, vit_lr_cap) if vit_lr_cap else lr
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

        # Scheduler (istege bagli lineer LR isinmasi + cosine)
        if scheduler is not None:
            self.scheduler = scheduler
        elif lr_warmup_epochs > 0:
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
        else:
            self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=epochs,
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

        # E0 altyapisi: periyodik checkpoint + egitim sigortalari
        self.save_every = save_every
        self.grad_clip = grad_clip
        self.eps_warmup_epochs = eps_warmup_epochs
        # Egitim eps'i warmup'ta degisir; degerlendirme HER ZAMAN bu tabanda
        self.base_eps = eps

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

            # NaN/Inf kontrolu backward/step'ten ONCE yapilmali; sonrasinda
            # yapilirsa bozuk gradyan agirliklara islenmis olur (M25)
            if torch.isnan(loss) or torch.isinf(loss):
                print("Warning: NaN/Inf loss detected, skipping batch")
                continue

            loss.backward()

            # Gradient clipping to prevent explosion (ViT-S icin 1.0 onerilir)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=self.grad_clip)
            self.optimizer.step()

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
    def evaluate_clean(self, loader: Optional[DataLoader] = None) -> float:
        """
        Evaluate clean accuracy on the given loader (default: test set).

        Returns:
            Clean accuracy percentage
        """
        loader = loader if loader is not None else self.test_loader
        self.model.eval()
        correct = 0
        total = 0

        for inputs, labels in loader:
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            outputs = self.model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        return 100.0 * correct / total

    def evaluate_adversarial(
        self,
        eps: Optional[float] = None,
        loader: Optional[DataLoader] = None,
    ) -> float:
        """
        Evaluate adversarial accuracy on the given loader (default: test set).

        Args:
            eps: Perturbation size for evaluation
            loader: Data loader to evaluate on (None = test set)

        Returns:
            Adversarial accuracy percentage
        """
        loader = loader if loader is not None else self.test_loader
        # eps verilmezse trainer'in TAM egitim eps'i kullanilir (base_eps);
        # eps-warmup degerlendirmeyi asla etkilemez
        eps = eps if eps is not None else getattr(self, "base_eps", 8 / 255)
        self.model.eval()
        correct = 0
        total = 0

        # Normal yolda defense'in eps'ini gecici olarak istenen degere sabitle
        old_def_eps = getattr(self.defense, "eps", None)
        if old_def_eps is not None:
            self.defense.eps = eps
        try:
            for inputs, labels in loader:
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
        finally:
            if old_def_eps is not None:
                self.defense.eps = old_def_eps

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
            delta = delta.detach().requires_grad_(True)

            outputs = self.model(original_images + delta)
            loss = nn.CrossEntropyLoss()(outputs, labels)

            # torch.autograd.grad: model parametrelerine gradyan biriktirmeden
            # yalnizca delta gradyanini hesapla (M10/M25)
            grad = torch.autograd.grad(loss, delta)[0].sign()
            delta = delta.detach() + alpha * grad
            delta = torch.clamp(delta, -eps, eps)
            delta = torch.clamp(original_images + delta, 0, 1) - original_images

        return original_images + delta

    def train(self, resume: bool = False) -> Dict[str, list]:
        """
        Run full adversarial training loop.

        Args:
            resume: True ise checkpoint_dir/last.pth'tan devam eder
                (elektrik kesintisi vb. sonrasi kaldigi epoch'tan surer).
                last.pth yoksa sifirdan baslar.

        Returns:
            Training history dictionary
        """
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()

        # Kesinti sonrasi devam (resume)
        start_epoch = 0
        last_path = self.checkpoint_dir / "last.pth"
        if resume and last_path.exists():
            ckpt = load_checkpoint(
                str(last_path), self.model, self.optimizer, self.scheduler, self.device
            )
            start_epoch = ckpt.get("epoch", -1) + 1
            self.best_adv_acc = ckpt.get("best_adv_acc", ckpt.get("accuracy", 0.0) or 0.0)
            self.patience_counter = ckpt.get("patience_counter", 0)
            saved_history = ckpt.get("history")
            if saved_history:
                self.history = saved_history
            if ckpt.get("early_stopped", False):
                self.early_stopped = True
                if self.verbose:
                    print(f"Training already early-stopped at epoch {start_epoch}; nothing to resume.")
                # Kokme TRAINING_COMPLETE yazilmadan once olduysa marker'i
                # burada tamamla; aksi halde pipeline guard'i sonsuza dek kilitli
                (self.checkpoint_dir / "TRAINING_COMPLETE").write_text(
                    f"epochs_run={start_epoch}\n"
                    f"early_stopped=True\n"
                    f"best_adv_acc={self.best_adv_acc:.4f}\n"
                )
                return self.history
            if self.verbose:
                print(f"Resuming from epoch {start_epoch} "
                      f"(best adv acc so far: {self.best_adv_acc:.2f}%, "
                      f"patience: {self.patience_counter}/{self.patience})")
            # metrics.jsonl budamasi: yeniden kosulacak epoch'larin eski
            # satirlarini at (cokme epoch-ckpt ile last.pth arasina duserse
            # ayni epoch icin cift satir olusmasin)
            if self.save_every > 0:
                mfile = self.checkpoint_dir / "epochs" / "metrics.jsonl"
                if mfile.exists():
                    import json as _json
                    kept = [ln for ln in mfile.read_text().splitlines()
                            if ln.strip() and _json.loads(ln)["epoch"] <= start_epoch]
                    tmp = mfile.with_suffix(".jsonl.tmp")
                    tmp.write_text("\n".join(kept) + ("\n" if kept else ""))
                    tmp.replace(mfile)

        if self.verbose:
            print(f"Adversarial training on {self.device}")
            print(f"Defense method: {self.defense.name}")
            print(f"Model parameters: {sum(p.numel() for p in self.model.parameters()):,}")

        # Resume'da dongu hic donmese bile (tum epochlar zaten bitmis)
        # TRAINING_COMPLETE dogru epochs_run yazsin
        if start_epoch > 0:
            self.current_epoch = start_epoch - 1

        for epoch in range(start_epoch, self.epochs):
            self.current_epoch = epoch

            # eps-warmup: EGITIM saldirisi ilk N epokta lineer buyuyen eps
            # kullanir; asagidaki degerlendirmeden once tabana geri alinir
            if self.eps_warmup_epochs > 0 and hasattr(self.defense, "eps"):
                frac = min(1.0, (epoch + 1) / self.eps_warmup_epochs)
                self.defense.eps = self.base_eps * frac

            # Train
            train_metrics = self.train_epoch()

            # Degerlendirme ve best-secimi HER ZAMAN tam eps'te yapilir
            if hasattr(self.defense, "eps"):
                self.defense.eps = self.base_eps

            # Evaluate: val_loader saglanmissa secim/izleme validasyon
            # setinde yapilir, test seti egitim boyunca kullanilmaz (M7)
            eval_loader = self.val_loader if self.val_loader is not None else self.test_loader
            clean_acc = self.evaluate_clean(eval_loader)
            adv_acc = self.evaluate_adversarial(loader=eval_loader)

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

            # E3 kalibrasyon yorungeleri icin periyodik checkpoint: yalniz
            # model agirliklari (optimizersiz) + metrics.jsonl satiri, boylece
            # checkpoint'ler sonradan TEMIZ-DOGRULUK KANTILLERINE gore secilebilir
            if self.save_every > 0 and (epoch + 1) % self.save_every == 0:
                ep_dir = self.checkpoint_dir / "epochs"
                ep_dir.mkdir(parents=True, exist_ok=True)
                ep_tmp = ep_dir / f"epoch_{epoch + 1:03d}.pth.tmp"
                torch.save({
                    "model_state_dict": self.model.state_dict(),
                    "epoch": epoch,
                    "clean_acc": clean_acc,
                    "adv_acc": adv_acc,
                }, ep_tmp)
                ep_tmp.replace(ep_dir / f"epoch_{epoch + 1:03d}.pth")
                with open(ep_dir / "metrics.jsonl", "a") as f:
                    f.write('{"epoch": %d, "clean_acc": %.4f, "adv_acc": %.4f, "lr": %.6g}\n'
                            % (epoch + 1, clean_acc, adv_acc,
                               self.optimizer.param_groups[0]["lr"]))

            # Her epoch sonunda kesintiye dayanikli last.pth (atomik yaz:
            # once .tmp'ye kaydet sonra yerine tasi - yazim sirasinda elektrik
            # giderse eski last.pth bozulmaz)
            if self.save_last:
                tmp_path = self.checkpoint_dir / "last.pth.tmp"
                save_checkpoint(
                    self.model,
                    tmp_path,
                    self.optimizer,
                    self.scheduler,
                    epoch,
                    adv_acc,
                    extra_info={
                        "clean_acc": clean_acc,
                        "best_adv_acc": self.best_adv_acc,
                        "patience_counter": self.patience_counter,
                        "early_stopped": self.early_stopped,
                        "history": self.history,
                    },
                )
                tmp_path.replace(self.checkpoint_dir / "last.pth")

            if self.early_stopped:
                break

        # Tamamlanma isareti: orkestrasyon scripti bu dosyaya bakarak
        # egitimin bittigini (kesintiye ugramadigini) anlar
        (self.checkpoint_dir / "TRAINING_COMPLETE").write_text(
            f"epochs_run={self.current_epoch + 1}\n"
            f"early_stopped={self.early_stopped}\n"
            f"best_adv_acc={self.best_adv_acc:.4f}\n"
        )

        elapsed_time = time.time() - start_time
        if self.verbose:
            print(f"\nTraining completed in {elapsed_time / 60:.2f} minutes")
            print(f"Best adversarial accuracy: {self.best_adv_acc:.2f}%")

        return self.history
