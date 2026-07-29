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
def clean(model, epochs, lr, batch_size, data_dir, output_dir, seed, device, val_indices):
    """Train a model with clean data."""
    from src.utils.seed import set_seed
    from src.utils.device import get_device
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders, get_cifar10_loaders_with_val
    from src.training import Trainer

    # Setup
    set_seed(seed)
    device = get_device(device)

    click.echo(f"Training {model} on {device}")
    click.echo(f"Epochs: {epochs}, LR: {lr}, Batch size: {batch_size}")

    # Create model
    model_instance = ModelRegistry.get(model)
    click.echo(f"Model parameters: {model_instance.count_parameters():,}")

    # Load data
    if val_indices:
        # rev2 C1: sabit val split egitimden cikarilir; epoch-degerlendirme ve
        # best-checkpoint secimi VAL uzerinden yapilir (test dokunulmaz).
        train_loader, val_loader, _ = get_cifar10_loaders_with_val(
            data_dir=data_dir,
            batch_size=batch_size,
            val_indices_path=val_indices,
        )
        test_loader = val_loader
        click.echo(f"Fixed val split ({val_indices}): egitim {len(train_loader.dataset)} ornek; "
                   f"secim {len(val_loader.dataset)} val ornegi uzerinden (test kullanilmiyor)")
    else:
        train_loader, test_loader = get_cifar10_loaders(
            data_dir=data_dir,
            batch_size=batch_size,
        )

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
    )

    # Train
    history = trainer.train()

    click.echo(f"\nTraining complete!")
    click.echo(f"Best accuracy: {trainer.best_acc:.2f}%")
    click.echo(f"Checkpoint saved to: {checkpoint_dir}")


@train.command()
@click.option("--model", "-m", type=str, required=True, help="Model name")
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
def adversarial(model, defense, pretrained, epochs, lr, batch_size, eps, alpha, steps,
                beta, data_dir, output_dir, seed, device, patience, val_split, resume,
                val_indices):
    """Train a model with adversarial defense."""
    from src.utils.seed import set_seed
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders, get_cifar10_loaders_with_val
    from src.training import AdversarialTrainer

    # Setup
    set_seed(seed)
    device = get_device(device)

    click.echo(f"Adversarial training {model} with {defense}")
    click.echo(f"Epochs: {epochs}, LR: {lr}, eps: {eps:.4f}")

    # Create model
    model_instance = ModelRegistry.get(model)

    # Load pretrained weights if provided
    if pretrained:
        click.echo(f"Loading pretrained weights from {pretrained}")
        load_model_weights(model_instance, pretrained, device)

    model_instance = model_instance.to(device)

    # Load data
    if val_indices:
        train_loader, val_loader, test_loader = get_cifar10_loaders_with_val(
            data_dir=data_dir,
            batch_size=batch_size,
            val_indices_path=val_indices,
        )
        click.echo(f"Fixed validation split from {val_indices} "
                   f"({len(val_loader.dataset)} samples; shared across training seeds)")
    elif val_split > 0:
        train_loader, val_loader, test_loader = get_cifar10_loaders_with_val(
            data_dir=data_dir,
            batch_size=batch_size,
            val_size=val_split,
            split_seed=seed,
        )
        click.echo(f"Validation split: {val_split} samples (model selection on val, not test)")
    else:
        train_loader, test_loader = get_cifar10_loaders(
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
    )

    if patience > 0:
        click.echo(f"Early stopping enabled (patience={patience})")
    if resume:
        click.echo("Resume mode: last.pth varsa kaldigi epoch'tan devam edilecek")

    # Train
    history = trainer.train(resume=resume)

    click.echo(f"\nAdversarial training complete!")
    click.echo(f"Best adversarial accuracy: {trainer.best_adv_acc:.2f}%")
    click.echo(f"Checkpoint saved to: {checkpoint_dir}")
