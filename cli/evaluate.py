"""Evaluation CLI commands."""

import click
from pathlib import Path


@click.group()
def evaluate():
    """Evaluation commands for model robustness."""
    pass


@evaluate.command()
@click.option("--model-path", "-m", type=str, required=True, help="Path to model checkpoint")
@click.option("--model-type", "-t", type=str, required=True, help="Model type (e.g., resnet18)")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--batch-size", "-b", type=int, default=100, help="Batch size")
@click.option("--device", type=str, default="auto", help="Device")
def clean(model_path, model_type, data_dir, batch_size, device):
    """Evaluate model on clean test set."""
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders
    from src.evaluation import compute_accuracy

    device = get_device(device)

    # Load model
    model = ModelRegistry.get(model_type)
    load_model_weights(model, model_path, device)
    model = model.to(device)
    model.eval()

    # Load data
    _, test_loader = get_cifar10_loaders(
        data_dir=data_dir,
        test_batch_size=batch_size,
    )

    # Evaluate
    acc = compute_accuracy(model, test_loader, device, verbose=True)

    click.echo(f"\nClean accuracy: {acc:.2f}%")


@evaluate.command()
@click.option("--model-path", "-m", type=str, required=True, help="Path to model checkpoint")
@click.option("--model-type", "-t", type=str, required=True, help="Model type")
@click.option("--attacks", "-a", multiple=True, default=["fgsm", "pgd"], help="Attacks to evaluate")
@click.option("--epsilons", "-e", multiple=True, type=float, default=[2/255, 4/255, 8/255],
              help="Epsilon values")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--output-dir", "-o", type=str, default="./results", help="Output directory")
@click.option("--batch-size", "-b", type=int, default=100, help="Batch size")
@click.option("--device", type=str, default="auto", help="Device")
@click.option("--seed", type=int, default=None,
              help="Random seed (PGD random-start dahil tam determinizm; None = seed'siz)")
def robustness(model_path, model_type, attacks, epsilons, data_dir, output_dir, batch_size, device, seed):
    """Evaluate model robustness against attacks."""
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders
    from src.evaluation import Evaluator, CSVReporter

    if seed is not None:
        import random
        import numpy as np
        import torch as _torch
        random.seed(seed)
        np.random.seed(seed)
        _torch.manual_seed(seed)
        _torch.cuda.manual_seed_all(seed)
        _torch.backends.cudnn.deterministic = True
        _torch.backends.cudnn.benchmark = False
        click.echo(f"Seed: {seed} (cudnn deterministic)")

    device = get_device(device)

    click.echo(f"Evaluating {model_type} robustness")
    click.echo(f"Attacks: {', '.join(attacks)}")
    click.echo(f"Epsilons: {', '.join([f'{e:.4f}' for e in epsilons])}")

    # Load model
    model = ModelRegistry.get(model_type)
    load_model_weights(model, model_path, device)
    model = model.to(device)

    # Load data
    _, test_loader = get_cifar10_loaders(
        data_dir=data_dir,
        test_batch_size=batch_size,
    )

    # Create evaluator
    evaluator = Evaluator(model, test_loader, device)

    # Evaluate
    results = evaluator.evaluate_multiple_attacks(
        attacks=list(attacks),
        epsilons=list(epsilons),
    )

    # Save results
    reporter = CSVReporter(output_dir)
    filename = f"{model_type}_robustness_results.csv"
    path = reporter.save(results, filename, model_name=model_type)

    click.echo(f"\nResults saved to: {path}")
    click.echo("\nSummary:")
    click.echo(results.to_string(index=False))


@evaluate.command()
@click.option("--model-path", "-m", type=str, required=True, help="Path to model checkpoint")
@click.option("--model-type", "-t", type=str, required=True, help="Model type")
@click.option("--defense", "-d", type=click.Choice(["tta", "tta_tencrop", "denoise", "jpeg"]),
              default="tta", help="Defense to evaluate")
@click.option("--attack", "-a", type=str, default="pgd", help="Attack to test against")
@click.option("--eps", type=float, default=8/255, help="Attack epsilon")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--output-dir", "-o", type=str, default="./results", help="Output directory")
@click.option("--device", type=str, default="auto", help="Device")
def defense(model_path, model_type, defense, attack, eps, data_dir, output_dir, device):
    """Evaluate a defense mechanism."""
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders
    from src.defenses import DefenseRegistry
    from src.evaluation import Evaluator, CSVReporter

    device = get_device(device)

    click.echo(f"Evaluating {defense} defense on {model_type}")
    click.echo(f"Attack: {attack}, eps: {eps:.4f}")

    # Load model
    model = ModelRegistry.get(model_type)
    load_model_weights(model, model_path, device)
    model = model.to(device)

    # Load data
    _, test_loader = get_cifar10_loaders(data_dir=data_dir)

    # Create defense
    defense_instance = DefenseRegistry.get(defense, model=model, device=device)

    # Create evaluator
    evaluator = Evaluator(model, test_loader, device)

    # Evaluate without defense
    click.echo("\nWithout defense:")
    evaluator.evaluate_clean()
    evaluator.evaluate_attack(attack, eps)

    # Evaluate with defense
    click.echo(f"\nWith {defense} defense:")
    evaluator.evaluate_defense(defense_instance, attack, eps)

    # Save results
    reporter = CSVReporter(output_dir)
    filename = f"{model_type}_{defense}_defense_results.csv"
    results = evaluator.get_results_dataframe()
    path = reporter.save(results, filename)

    click.echo(f"\nResults saved to: {path}")


@evaluate.command()
@click.option("--model-path", "-m", type=str, required=True, help="Path to model checkpoint")
@click.option("--model-type", "-t", type=str, required=True, help="Model type")
@click.option("--data-dir", type=str, default="./data", help="Data directory")
@click.option("--output-dir", "-o", type=str, default="./results", help="Output directory")
@click.option("--device", type=str, default="auto", help="Device")
def full(model_path, model_type, data_dir, output_dir, device):
    """Run full evaluation suite."""
    from src.utils.device import get_device
    from src.utils.checkpoint import load_model_weights
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders
    from src.evaluation import Evaluator, CSVReporter, PlotReporter

    device = get_device(device)

    click.echo(f"Running full evaluation on {model_type}")
    click.echo("=" * 50)

    # Load model
    model = ModelRegistry.get(model_type)
    load_model_weights(model, model_path, device)
    model = model.to(device)

    # Load data
    _, test_loader = get_cifar10_loaders(data_dir=data_dir)

    # Create evaluator
    evaluator = Evaluator(model, test_loader, device)

    # Full evaluation
    results = evaluator.evaluate_multiple_attacks(
        attacks=["fgsm", "pgd"],
        epsilons=[2/255, 4/255, 8/255],
    )

    # Save results
    csv_reporter = CSVReporter(output_dir)
    plot_reporter = PlotReporter(output_dir)

    csv_path = csv_reporter.save(results, f"{model_type}_full_evaluation.csv", model_name=model_type)
    plot_path = plot_reporter.plot_accuracy_vs_epsilon(
        results,
        f"{model_type}_robustness_plot.png",
        title=f"{model_type} Robustness",
    )

    click.echo(f"\nResults saved to: {csv_path}")
    click.echo(f"Plot saved to: {plot_path}")
    click.echo("\nSummary:")
    click.echo(results.to_string(index=False))
