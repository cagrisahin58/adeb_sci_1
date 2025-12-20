"""Main CLI entry point for Adversarial Defense Study."""

import click
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cli.train import train
from cli.evaluate import evaluate


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """
    Adversarial Defense Study CLI

    A comprehensive framework for evaluating adversarial robustness
    of deep learning models.

    Examples:

        # Train a clean ResNet18 model
        advdefense train clean --model resnet18 --epochs 50

        # Train with TRADES defense
        advdefense train adversarial --model resnet18 --defense trades

        # Evaluate robustness
        advdefense evaluate robustness --model-path ./models/best.pth

        # Run full evaluation suite
        advdefense evaluate full --model-path ./models/best.pth
    """
    pass


# Add command groups
cli.add_command(train)
cli.add_command(evaluate)


@cli.command()
def list_models():
    """List all available models."""
    from src.models import ModelRegistry

    click.echo("Available models:")
    for name in ModelRegistry.list_models():
        click.echo(f"  - {name}")


@cli.command()
def list_attacks():
    """List all available attacks."""
    from src.attacks import AttackRegistry

    click.echo("Available attacks:")
    for name in AttackRegistry.list_attacks():
        click.echo(f"  - {name}")


@cli.command()
def list_defenses():
    """List all available defenses."""
    from src.defenses import DefenseRegistry

    click.echo("Available defenses:")
    for name in DefenseRegistry.list_defenses():
        click.echo(f"  - {name}")


if __name__ == "__main__":
    cli()
