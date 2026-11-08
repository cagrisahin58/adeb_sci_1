"""Training CLI commands."""

import click
import torch
from pathlib import Path


@click.group()
def train():
    """Training commands for models."""
    pass


@train.command()
@click.option("--model", "-m", type=str, required=True, help="Model name (e.g., resnet18, vit_tiny)")
@click.option("--dataset", type=click.Choice(["cifar10", "cifar100", "svhn"]),
              default="cifar10", help="Egitim veri kumesi (num_classes kumeden turer)")
@click.option("--epochs", "-e", type=int, default=50, help="Number of training epochs")
@click.option("--lr", type=float, default=0.1, help="Learning rate")
@click.option("--batch-size", "-b", type=int, default=128, help="Training batch size")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--output-dir", "-o", type=str, default="./models", help="Output directory for checkpoints")
@click.option("--seed", type=int, default=42, help="Random seed")
@click.option("--device", type=str, default="auto", help="Device (auto, cuda, cpu)")
@click.option("--val-indices", type=str, default=None,
              help="Sabit validasyon indeksleri JSON'u (rev2 C1 leak fix): bu ornekler "
                   "egitimden CIKARILIR ve model secimi val seti uzerinden yapilir "
                   "(test seti egitim/secime hic girmez)")
@click.option("--save-every", type=int, default=0,
              help="Her N epokta periyodik checkpoint (E3 kalibrasyon yorungeleri); 0=kapali")
@click.option("--resume", is_flag=True, default=False,
              help="Checkpoint dizinindeki last.pth'tan devam et (kesinti sonrasi)")
@click.option("--timm-pretrained", is_flag=True, default=False,
              help="Modeli ImageNet on-egitimli agirliklarla baslat "
                   "(ViT-Small tarifi: pretrained + kisa temiz finetune)")
@click.option("--optimizer", "optimizer_name", type=click.Choice(["auto", "adamw", "sgd"]),
              default="auto",
              help="auto = eski davranis (sinif adinda vit -> AdamW, degilse SGD); "
                   "adamw/sgd = sinif adina bakmadan zorla (konsey B3)")
@click.option("--init-weights", type=click.Choice(["none", "deit_tiny_in1k", "resnet18_a1_in1k",
                                                  "augreg_in21k_ft_in1k", "fb_swsl_ig1b_ft_in1k"]),
              default="none",
              help="Govdeyi on egitimli agirliklarla baslat (bas haric); yalniz uyumlu "
                   "tiplerle: deit_tiny_in1k -> vit_tiny_in1k, "
                   "resnet18_a1_in1k -> resnet18_224_in1k, "
                   "augreg_in21k_ft_in1k -> vit_tiny_in21k, "
                   "fb_swsl_ig1b_ft_in1k -> resnet18_224_swsl (curutme C1/C2)")
@click.option("--lr-schedule", type=click.Choice(["cosine", "constant"]), default="cosine",
              help="Temiz asama LR cizelgesi (varsayilan cosine, T_max=epochs: eski davranis)")
@click.option("--max-train-batches", type=int, default=0,
              help="Epok basina en fazla N egitim batch'i (yalniz smoke); 0 = sinirsiz")
# --- Curutme B (08.11.2026): temiz asamaya ozgu artirma ve kayip bayraklari. Hicbiri
# verilmezse egitim eski kodla ayni islemleri ayni sirayla yapar (regresyon kaniti:
# results/q1/curutme_2026-11-08/_duman/regresyon_*.txt). ---
@click.option("--trivial-augment", is_flag=True, default=False,
              help="Egitim artirmasina torchvision TrivialAugmentWide ekle (crop + flip'ten sonra)")
@click.option("--random-erasing", type=float, default=0.0,
              help="ToTensor'dan sonra RandomErasing olasiligi (deger 0, [0,1] piksel uzayi); 0 = kapali")
@click.option("--mixup", type=float, default=0.0,
              help="timm Mixup alfa (0 = kapali); --cutmix ile birlikte batch kipinde, switch_prob 0.5")
@click.option("--cutmix", type=float, default=0.0, help="timm CutMix alfa (0 = kapali)")
@click.option("--label-smoothing", type=float, default=0.0,
              help="Egitim kaybinda etiket yumusatma (mixup aciksa Mixup'a verilir); 0 = kapali")
@click.option("--lr-warmup", type=int, default=0,
              help="Ilk N epokta lineer LR isinmasi (0.1 -> 1.0), sonra cosine T_max = epochs - N; "
                   "yalniz --lr-schedule cosine ile; 0 = kapali")
@click.option("--stop-epoch", type=int, default=0,
              help="Temiz egitimi bu epokta durdur, LR cizelgesi -e uzerinden kalsin "
                   "(pilot ve duman); 0 = kapali")
def clean(model, dataset, epochs, lr, batch_size, data_dir, output_dir, seed, device,
          val_indices, save_every, resume, timm_pretrained, optimizer_name, init_weights,
          lr_schedule, max_train_batches, trivial_augment, random_erasing, mixup, cutmix,
          label_smoothing, lr_warmup, stop_epoch):
    """Train a model with clean data."""
    from src.utils.seed import set_seed
    from src.utils.device import get_device
    from src.models import ModelRegistry
    from src.data import get_loaders, get_loaders_with_val, DATASETS
    from src.training import Trainer

    # Setup
    set_seed(seed)
    device = get_device(device)

    num_classes = DATASETS[dataset]["num_classes"]
    click.echo(f"Training {model} on {device} (dataset={dataset}, num_classes={num_classes})")
    click.echo(f"Epochs: {epochs}, LR: {lr}, Batch size: {batch_size}")

    # Create model
    model_instance = ModelRegistry.get(model, num_classes=num_classes,
                                       pretrained=timm_pretrained)
    if timm_pretrained:
        click.echo("ImageNet on-egitimli agirliklarla baslatildi")
    if init_weights != "none":
        import json as _json
        from src.models.r224 import load_imagenet_init
        rep = load_imagenet_init(model_instance, init_weights, model)
        click.echo("INIT_WEIGHTS_RAPORU " + _json.dumps(
            {k: rep[k] for k in ("init_key", "timm_name", "source_file", "source_sha256",
                                 "n_loaded", "n_target_keys", "missing_nonhead",
                                 "unexpected_nonhead", "shape_mismatch", "head_keys_skipped",
                                 "pretrained_cfg_mean", "pretrained_cfg_std",
                                 "norm_matches_cfg")}))
    elif model in ("vit_tiny_in1k", "resnet18_224_in1k", "vit_tiny_in21k", "resnet18_224_swsl"):
        click.echo(f"UYARI: {model} IN normalizasyonlu tiptir ama --init-weights none "
                   f"(rastgele baslatma); K3 demeti bozulur, bilerek mi?")
    click.echo(f"Optimizer: {optimizer_name}, LR schedule: {lr_schedule}")
    click.echo(f"Model parameters: {model_instance.count_parameters():,}")

    # Load data
    if val_indices:
        # rev2 C1: sabit val split egitimden cikarilir; epoch-degerlendirme ve
        # best-checkpoint secimi VAL uzerinden yapilir (test dokunulmaz).
        train_loader, val_loader, _ = get_loaders_with_val(
            dataset=dataset,
            data_dir=data_dir,
            batch_size=batch_size,
            val_indices_path=val_indices,
        )
        test_loader = val_loader
        click.echo(f"Fixed val split ({val_indices}): egitim {len(train_loader.dataset)} ornek; "
                   f"secim {len(val_loader.dataset)} val ornegi uzerinden (test kullanilmiyor)")
    else:
        train_loader, test_loader = get_loaders(
            dataset=dataset,
            data_dir=data_dir,
            batch_size=batch_size,
        )

    # Curutme B: istege bagli temiz asama artirmasi ve kaybi (bayrak yoksa hicbir sey yapilmaz)
    extra_trainer_kwargs = {}
    if trivial_augment or random_erasing > 0:
        from torchvision import transforms as _T
        _aug = [_T.RandomCrop(DATASETS[dataset]["img_size"], padding=4)]
        if DATASETS[dataset]["flip"]:
            _aug.append(_T.RandomHorizontalFlip())
        if trivial_augment:
            _aug.append(_T.TrivialAugmentWide())
        _aug.append(_T.ToTensor())
        if random_erasing > 0:
            _aug.append(_T.RandomErasing(p=random_erasing, value=0))
        _ds = train_loader.dataset
        _base = _ds.dataset if hasattr(_ds, "dataset") else _ds  # Subset -> taban veri kumesi
        _base.transform = _T.Compose(_aug)
        click.echo(f"TEMIZ_ARTIRMA egitim donusumu: {_base.transform}")
    if mixup > 0 or cutmix > 0:
        from timm.data import Mixup
        from timm.loss import SoftTargetCrossEntropy
        extra_trainer_kwargs["mixup_fn"] = Mixup(
            mixup_alpha=mixup, cutmix_alpha=cutmix, prob=1.0, switch_prob=0.5, mode="batch",
            label_smoothing=label_smoothing, num_classes=num_classes)
        extra_trainer_kwargs["train_criterion"] = SoftTargetCrossEntropy()
        click.echo(f"TEMIZ_KARISIM mixup={mixup} cutmix={cutmix} prob=1.0 switch_prob=0.5 "
                   f"mode=batch label_smoothing={label_smoothing} kayip=SoftTargetCrossEntropy")
    elif label_smoothing > 0:
        import torch.nn as _nn
        extra_trainer_kwargs["train_criterion"] = _nn.CrossEntropyLoss(label_smoothing=label_smoothing)
        click.echo(f"TEMIZ_KAYIP CrossEntropyLoss(label_smoothing={label_smoothing}) (yalniz egitim)")
    if lr_warmup > 0:
        if lr_schedule != "cosine":
            raise click.UsageError("--lr-warmup yalniz --lr-schedule cosine ile kullanilir")
        extra_trainer_kwargs["lr_warmup_epochs"] = lr_warmup
        click.echo(f"TEMIZ_ISINMA ilk {lr_warmup} epok LinearLR 0.1->1.0, sonra cosine T_max={epochs - lr_warmup}")
    if stop_epoch > 0:
        extra_trainer_kwargs["stop_epoch"] = stop_epoch
        click.echo(f"TEMIZ_DURMA stop_epoch={stop_epoch} (LR cizelgesi {epochs} epok uzerinden)")

    # Create trainer
    checkpoint_dir = Path(output_dir) / model / "clean"
    trainer = Trainer(
        model=model_instance,
        train_loader=train_loader,
        test_loader=test_loader,
        device=device,
        epochs=epochs,
        lr=lr,
        checkpoint_dir=str(checkpoint_dir),
        save_every=save_every,
        optimizer_name=optimizer_name,
        lr_schedule=lr_schedule,
        max_train_batches=max_train_batches,
        **extra_trainer_kwargs,
    )
    if resume:
        click.echo("Resume mode: last.pth varsa kaldigi epoch'tan devam edilecek")

    # Train
    history = trainer.train(resume=resume)

    click.echo(f"\nTraining complete!")
    click.echo(f"Best accuracy: {trainer.best_acc:.2f}%")
    click.echo(f"Checkpoint saved to: {checkpoint_dir}")


@train.command()
@click.option("--model", "-m", type=str, required=True, help="Model name")
@click.option("--dataset", type=click.Choice(["cifar10", "cifar100", "svhn"]),
              default="cifar10", help="Egitim veri kumesi (num_classes kumeden turer)")
@click.option("--defense", "-d", type=click.Choice(["adversarial_training", "trades", "mart"]),
              default="adversarial_training", help="Defense method")
@click.option("--pretrained", "-p", type=str, default=None, help="Path to pretrained model")
@click.option("--epochs", "-e", type=int, default=25, help="Number of training epochs")
@click.option("--lr", type=float, default=0.01, help="Learning rate")
@click.option("--batch-size", "-b", type=int, default=128, help="Training batch size")
@click.option("--eps", type=float, default=8/255, help="Perturbation epsilon")
@click.option("--alpha", type=float, default=2/255, help="PGD step size")
@click.option("--steps", type=int, default=10, help="PGD steps")
@click.option("--beta", type=float, default=6.0, help="TRADES/MART beta parameter")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--output-dir", "-o", type=str, default="./models", help="Output directory")
@click.option("--seed", type=int, default=42, help="Random seed")
@click.option("--device", type=str, default="auto", help="Device")
@click.option("--patience", type=int, default=0, help="Early stopping patience (0=disabled)")
@click.option("--val-split", type=int, default=2000,
              help="Egitim setinden ayrilacak validasyon ornegi sayisi; model secimi "
                   "bu set uzerinden yapilir (0 = eski davranis: test setiyle secim, "
                   "selection leakage icerir)")
@click.option("--resume", is_flag=True, default=False,
              help="Checkpoint dizinindeki last.pth'tan devam et (kesinti sonrasi). "
                   "last.pth yoksa sifirdan baslar.")
@click.option("--val-indices", type=str, default=None,
              help="Sabit validasyon indeksleri JSON'u (rev2 C1 leak fix): split "
                   "seed'den turetilmez, tum seed'ler ayni val setini paylasir")
@click.option("--save-every", type=int, default=0,
              help="Her N epokta periyodik checkpoint (E3 kalibrasyon yorungeleri; "
                   "checkpoint_dir/epochs/ altina yalniz agirlik); 0=kapali")
@click.option("--grad-clip", type=float, default=10.0,
              help="Gradyan kirpma L2 max-norm (ViT-Small icin 1.0 onerilir)")
@click.option("--eps-warmup", type=int, default=0,
              help="Ilk N epokta egitim eps'i 0->hedef lineer isinir "
                   "(SVHN 8/255 ve ViT-S kararsizlik sigortasi); 0=kapali")
@click.option("--lr-warmup", type=int, default=0,
              help="Ilk N epokta lineer LR isinmasi, sonra cosine; 0=kapali")
@click.option("--vit-lr-cap", type=float, default=1e-3,
              help="ViT'lerde LR ust siniri (0 = sinirsiz; kalibrasyon deneyleri icin)")
@click.option("--optimizer", "optimizer_name", type=click.Choice(["auto", "adamw", "sgd"]),
              default="auto",
              help="auto = eski davranis (sinif adinda vit -> AdamW wd 0.05, degilse SGD); "
                   "adamw/sgd = zorla (konsey B3: dort hucrede adamw)")
@click.option("--stop-epoch", type=int, default=0,
              help="Egitimi bu epokta durdur, LR cizelgesi -e uzerinden kalsin "
                   "(konsey bekcisi AT tavani); 0 = kapali")
@click.option("--max-train-batches", type=int, default=0,
              help="Epok basina en fazla N egitim batch'i (yalniz smoke); 0 = sinirsiz")
def adversarial(model, dataset, defense, pretrained, epochs, lr, batch_size, eps, alpha,
                steps, beta, data_dir, output_dir, seed, device, patience, val_split,
                resume, val_indices, save_every, grad_clip, eps_warmup, lr_warmup,
                vit_lr_cap, optimizer_name, stop_epoch, max_train_batches):
    """Train a model with adversarial defense."""
    from src.utils.seed import set_seed
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_loaders, get_loaders_with_val, DATASETS
    from src.training import AdversarialTrainer

    # Setup
    set_seed(seed)
    device = get_device(device)

    num_classes = DATASETS[dataset]["num_classes"]
    click.echo(f"Adversarial training {model} with {defense} "
               f"(dataset={dataset}, num_classes={num_classes})")
    click.echo(f"Epochs: {epochs}, LR: {lr}, eps: {eps:.4f}")

    # Create model
    model_instance = ModelRegistry.get(model, num_classes=num_classes)

    # Load pretrained weights if provided
    if pretrained:
        click.echo(f"Loading pretrained weights from {pretrained}")
        load_model_weights(model_instance, pretrained, device)

    model_instance = model_instance.to(device)

    # Load data
    if val_indices:
        train_loader, val_loader, test_loader = get_loaders_with_val(
            dataset=dataset,
            data_dir=data_dir,
            batch_size=batch_size,
            val_indices_path=val_indices,
        )
        click.echo(f"Fixed validation split from {val_indices} "
                   f"({len(val_loader.dataset)} samples; shared across training seeds)")
    elif val_split > 0:
        train_loader, val_loader, test_loader = get_loaders_with_val(
            dataset=dataset,
            data_dir=data_dir,
            batch_size=batch_size,
            val_size=val_split,
            split_seed=seed,
        )
        click.echo(f"Validation split: {val_split} samples (model selection on val, not test)")
    else:
        train_loader, test_loader = get_loaders(
            dataset=dataset,
            data_dir=data_dir,
            batch_size=batch_size,
        )
        val_loader = None
        click.echo("WARNING: no validation split - model selection uses the TEST set (leakage)")

    # Create trainer
    checkpoint_dir = Path(output_dir) / model / "adv" / defense
    trainer = AdversarialTrainer(
        model=model_instance,
        train_loader=train_loader,
        test_loader=test_loader,
        val_loader=val_loader,
        defense=defense,
        device=device,
        epochs=epochs,
        lr=lr,
        eps=eps,
        alpha=alpha,
        steps=steps,
        beta=beta,
        checkpoint_dir=str(checkpoint_dir),
        patience=patience,
        save_every=save_every,
        grad_clip=grad_clip,
        vit_lr_cap=(vit_lr_cap if vit_lr_cap > 0 else None),
        eps_warmup_epochs=eps_warmup,
        lr_warmup_epochs=lr_warmup,
        optimizer_name=optimizer_name,
        stop_epoch=stop_epoch,
        max_train_batches=max_train_batches,
    )
    click.echo(f"Optimizer: {optimizer_name}; stop_epoch: {stop_epoch or 'kapali'} "
               f"(LR cizelgesi {epochs} epok uzerinden)")
    if save_every > 0:
        click.echo(f"Periyodik checkpoint: her {save_every} epokta epochs/ altina")
    if eps_warmup > 0:
        click.echo(f"Eps warmup: ilk {eps_warmup} epok (degerlendirme tam eps'te)")

    if patience > 0:
        click.echo(f"Early stopping enabled (patience={patience})")
    if resume:
        click.echo("Resume mode: last.pth varsa kaldigi epoch'tan devam edilecek")

    # Train
    history = trainer.train(resume=resume)

    click.echo(f"\nAdversarial training complete!")
    click.echo(f"Best adversarial accuracy: {trainer.best_adv_acc:.2f}%")
    click.echo(f"Checkpoint saved to: {checkpoint_dir}")
