#!/usr/bin/env python3
"""
SCI Publication Analysis Script

Runs comprehensive experiments for mechanism analysis and transfer attack study
comparing CNN (ResNet) and Vision Transformer (ViT) architectures.

Research Questions:
1. Why do CNNs show better adversarial robustness than ViTs?
2. How do adversarial examples transfer between architectures?
3. What gradient/attention characteristics explain the vulnerability gap?

Usage:
    python experiments/run_sci_analysis.py --experiment all
    python experiments/run_sci_analysis.py --experiment gradient
    python experiments/run_sci_analysis.py --experiment transfer
    python experiments/run_sci_analysis.py --experiment attention
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

import torch
import torch.nn as nn
import numpy as np
import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.attacks import AttackRegistry
from src.data import get_cifar10_loaders
from src.analysis import (
    GradientAnalyzer,
    TransferAttackAnalyzer,
    AttentionAnalyzer,
    AdversarialVisualizer,
)
from src.utils import set_seed, get_device


def load_models(device: torch.device, model_paths: dict = None) -> dict:
    """Load all models for analysis."""
    models = {}

    # ResNet models
    print("Loading ResNet18...")
    resnet = ModelRegistry.get("resnet18")
    if model_paths and "resnet_clean" in model_paths:
        resnet.load_state_dict(torch.load(model_paths["resnet_clean"], map_location=device))
    models["resnet_clean"] = resnet.to(device).eval()

    if model_paths and "resnet_adv" in model_paths:
        resnet_adv = ModelRegistry.get("resnet18")
        resnet_adv.load_state_dict(torch.load(model_paths["resnet_adv"], map_location=device))
        models["resnet_adv"] = resnet_adv.to(device).eval()

    # ViT models
    print("Loading ViT-Tiny...")
    try:
        vit = ModelRegistry.get("vit_tiny")
        if model_paths and "vit_clean" in model_paths:
            vit.load_state_dict(torch.load(model_paths["vit_clean"], map_location=device))
        models["vit_clean"] = vit.to(device).eval()

        if model_paths and "vit_adv" in model_paths:
            vit_adv = ModelRegistry.get("vit_tiny")
            vit_adv.load_state_dict(torch.load(model_paths["vit_adv"], map_location=device))
            models["vit_adv"] = vit_adv.to(device).eval()
    except Exception as e:
        print(f"Warning: Could not load ViT models: {e}")

    # Additional architectures for diversity
    try:
        print("Loading DenseNet121...")
        densenet = ModelRegistry.get("densenet121")
        models["densenet_clean"] = densenet.to(device).eval()
    except Exception as e:
        print(f"Warning: Could not load DenseNet: {e}")

    return models


def create_pgd_attack(eps: float, normalize_data: bool = True):
    """
    Create PGD attack function for given epsilon.

    Args:
        eps: Perturbation budget
        normalize_data: If True, expects normalized inputs and handles denorm/renorm
    """
    def attack_fn(model, images, labels):
        from src.attacks import PGDAttack
        from src.data import get_normalization, denormalize, normalize

        if normalize_data:
            # Get CIFAR-10 normalization parameters
            mean, std = get_normalization("cifar10")

            # Denormalize to [0, 1] range for attack
            images_denorm = denormalize(images, mean, std)

            # Run attack on denormalized images
            attack = PGDAttack(model, eps=eps, alpha=eps/4, steps=20)
            adv_images_denorm = attack(images_denorm, labels)

            # Normalize back for model input
            adv_images = normalize(adv_images_denorm, mean, std)
            return adv_images
        else:
            # Direct attack (for non-normalized data)
            attack = PGDAttack(model, eps=eps, alpha=eps/4, steps=20)
            return attack(images, labels)

    return attack_fn


def run_gradient_analysis(
    models: dict,
    dataloader: torch.utils.data.DataLoader,
    device: torch.device,
    output_dir: Path,
    num_batches: int = 10,
) -> dict:
    """
    Run gradient analysis comparing CNN vs ViT.

    Analyzes:
    - Gradient magnitude distributions
    - Spatial variance of gradients
    - Gradient alignment across samples
    - Loss landscape characteristics
    """
    print("\n" + "="*60)
    print("GRADIENT ANALYSIS")
    print("="*60)

    results = {"gradient_stats": {}, "landscape": {}, "alignment": {}}

    for model_name, model in models.items():
        print(f"\nAnalyzing {model_name}...")
        analyzer = GradientAnalyzer(model, device)

        all_stats = []
        all_landscapes = []
        alignments = []

        for batch_idx, (images, labels) in enumerate(dataloader):
            if batch_idx >= num_batches:
                break

            images, labels = images.to(device), labels.to(device)

            # Gradient statistics
            stats = analyzer.compute_gradient_statistics(images, labels)
            all_stats.append(stats)

            # Loss landscape
            landscape = analyzer.compare_gradient_landscapes(
                images, labels,
                epsilon_range=[0.001, 0.005, 0.01, 0.02, 0.03]
            )
            all_landscapes.append(landscape)

            # Gradient alignment
            alignment = analyzer.compute_gradient_alignment(images, labels)
            alignments.append(alignment)

        # Aggregate results
        avg_stats = {}
        for key in all_stats[0].keys():
            avg_stats[key] = np.mean([s[key] for s in all_stats])

        results["gradient_stats"][model_name] = avg_stats
        results["alignment"][model_name] = np.mean(alignments)

        # Aggregate landscape
        eps_list = all_landscapes[0]["epsilons"]
        avg_landscape = {
            "epsilons": eps_list,
            "loss_gradient": [
                np.mean([l["loss_gradient"][i] for l in all_landscapes])
                for i in range(len(eps_list))
            ],
            "loss_random": [
                np.mean([l["loss_random"][i] for l in all_landscapes])
                for i in range(len(eps_list))
            ],
        }
        results["landscape"][model_name] = avg_landscape

        print(f"  L2 norm mean: {avg_stats['l2_norm_mean']:.6f}")
        print(f"  Spatial variance: {avg_stats['spatial_variance']:.6f}")
        print(f"  Sparsity: {avg_stats['sparsity']:.4f}")
        print(f"  Gradient alignment: {np.mean(alignments):.4f}")

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "gradient_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    # Create comparison DataFrame
    df = pd.DataFrame(results["gradient_stats"]).T
    df.to_csv(output_dir / "gradient_stats.csv")
    print(f"\nResults saved to {output_dir}")

    return results


def run_transfer_analysis(
    models: dict,
    dataloader: torch.utils.data.DataLoader,
    device: torch.device,
    output_dir: Path,
    num_batches: int = 10,
    epsilon: float = 8/255,
) -> dict:
    """
    Run transfer attack analysis between architectures.

    Analyzes:
    - Full transfer matrix
    - CNN→ViT vs ViT→CNN transfer rates
    - Perturbation similarity
    - Gradient alignment correlation with transfer
    """
    print("\n" + "="*60)
    print("TRANSFER ATTACK ANALYSIS")
    print("="*60)

    results = {
        "transfer_matrices": {},
        "perturbation_similarity": {},
        "gradient_alignment": {},
        "summary": {},
    }

    # Collect batches
    all_images, all_labels = [], []
    for batch_idx, (images, labels) in enumerate(dataloader):
        if batch_idx >= num_batches:
            break
        all_images.append(images)
        all_labels.append(labels)

    images = torch.cat(all_images, dim=0).to(device)
    labels = torch.cat(all_labels, dim=0).to(device)

    print(f"Using {len(images)} samples for transfer analysis")

    # Use first model as source for analyzer initialization
    first_model = list(models.values())[0]
    analyzer = TransferAttackAnalyzer(
        source_model=first_model,
        target_models=models,
        device=device,
    )

    # Attack function
    attack_fn = create_pgd_attack(epsilon)

    # Full analysis
    print("\nComputing transfer matrix...")
    full_results = analyzer.full_transfer_analysis(
        images, labels, attack_fn, models
    )

    results["transfer_matrix"] = full_results["transfer_matrix"].tolist()
    results["model_names"] = full_results["model_names"]
    results["perturbation_similarity"] = full_results["perturbation_similarity"]
    results["gradient_alignment"] = full_results["gradient_alignment"]
    results["summary"] = full_results["summary"]

    # Print transfer matrix
    print("\nTransfer Matrix (rows=source, cols=target):")
    df = analyzer.export_results_to_dataframe(
        full_results["transfer_matrix"],
        full_results["model_names"]
    )
    print(df.to_string())

    # Analyze epsilon sensitivity
    print("\nAnalyzing epsilon sensitivity...")
    eps_range = [0.005, 0.01, 0.02, 0.03]

    def attack_factory(eps):
        return create_pgd_attack(eps)

    eps_results = analyzer.analyze_perturbation_transferability(
        images, labels, eps_range, attack_factory
    )
    results["epsilon_sensitivity"] = {
        name: {str(eps): rate for eps, rate in rates.items()}
        for name, rates in eps_results.items()
    }

    # Summary statistics
    print("\n" + "-"*40)
    print("SUMMARY:")
    print(f"  CNN→ViT average transfer: {results['summary']['cnn_to_vit_avg_transfer']:.4f}")
    print(f"  ViT→CNN average transfer: {results['summary']['vit_to_cnn_avg_transfer']:.4f}")

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "transfer_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    df.to_csv(output_dir / "transfer_matrix.csv")
    print(f"\nResults saved to {output_dir}")

    return results


def run_attention_analysis(
    models: dict,
    dataloader: torch.utils.data.DataLoader,
    device: torch.device,
    output_dir: Path,
    num_batches: int = 5,
    epsilon: float = 8/255,
) -> dict:
    """
    Run attention pattern analysis for ViT models.

    Analyzes:
    - Attention entropy changes under attack
    - Attention pattern degradation
    - Layer-wise attention differences
    """
    print("\n" + "="*60)
    print("ATTENTION ANALYSIS")
    print("="*60)

    results = {"attention_degradation": {}}

    # Filter ViT models
    vit_models = {k: v for k, v in models.items() if "vit" in k.lower()}

    if not vit_models:
        print("No ViT models found for attention analysis")
        return results

    attack_fn = create_pgd_attack(epsilon)

    for model_name, model in vit_models.items():
        print(f"\nAnalyzing attention for {model_name}...")

        try:
            analyzer = AttentionAnalyzer(model, device)
        except Exception as e:
            print(f"  Could not create analyzer: {e}")
            continue

        all_degradation = []

        for batch_idx, (images, labels) in enumerate(dataloader):
            if batch_idx >= num_batches:
                break

            images, labels = images.to(device), labels.to(device)

            # Generate adversarial examples
            adv_images = attack_fn(model, images, labels)

            # Analyze attention degradation
            try:
                degradation = analyzer.analyze_attention_degradation(
                    images, adv_images
                )
                all_degradation.append(degradation)
            except Exception as e:
                print(f"  Batch {batch_idx} error: {e}")
                continue

        if all_degradation:
            # Aggregate
            avg_degradation = {}
            for key in all_degradation[0].keys():
                if isinstance(all_degradation[0][key], (int, float)):
                    avg_degradation[key] = np.mean([d[key] for d in all_degradation])

            results["attention_degradation"][model_name] = avg_degradation

            print(f"  Avg entropy change: {avg_degradation.get('avg_entropy_change', 0):.4f}")
            print(f"  Avg attention distance: {avg_degradation.get('avg_attention_distance', 0):.4f}")

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "attention_analysis.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_dir}")
    return results


def create_visualizations(
    gradient_results: dict,
    transfer_results: dict,
    attention_results: dict,
    output_dir: Path,
) -> None:
    """Create publication-quality visualizations."""
    print("\n" + "="*60)
    print("CREATING VISUALIZATIONS")
    print("="*60)

    viz = AdversarialVisualizer(figsize=(12, 8), dpi=300)
    figures = {}

    # 1. Gradient statistics comparison
    if "gradient_stats" in gradient_results:
        print("Creating gradient statistics figure...")
        fig = viz.plot_robustness_comparison(
            gradient_results["gradient_stats"],
            metric="l2_norm_mean",
            title="Gradient L2 Norm Comparison",
        )
        figures["gradient_l2_comparison"] = fig

    # 2. Transfer matrix heatmap
    if "transfer_matrix" in transfer_results:
        print("Creating transfer matrix figure...")
        fig = viz.plot_transfer_matrix(
            np.array(transfer_results["transfer_matrix"]),
            transfer_results["model_names"],
            title="Adversarial Example Transferability",
        )
        figures["transfer_matrix"] = fig

    # 3. Epsilon sensitivity
    if "epsilon_sensitivity" in transfer_results:
        print("Creating epsilon sensitivity figure...")
        # Convert string keys back to float
        eps_results = {
            name: {float(eps): rate for eps, rate in rates.items()}
            for name, rates in transfer_results["epsilon_sensitivity"].items()
        }
        fig = viz.plot_epsilon_sweep(
            eps_results,
            title="Transfer Rate vs Perturbation Budget",
            ylabel="Transfer Success Rate",
        )
        figures["epsilon_sensitivity"] = fig

    # Save all figures
    figures_dir = output_dir / "figures"
    viz.save_all_figures(figures, str(figures_dir), formats=["png", "pdf"])

    print(f"\nFigures saved to {figures_dir}")


def run_all_experiments(args):
    """Run all experiments."""
    # Setup
    set_seed(args.seed)
    device = get_device(args.device)
    print(f"Using device: {device}")

    # Output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir) / f"sci_analysis_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")

    # Load data
    print("\nLoading CIFAR-10...")
    _, test_loader = get_cifar10_loaders(
        batch_size=args.batch_size,
        num_workers=args.num_workers,
    )

    # Load models
    model_paths = {}
    if args.model_dir:
        model_dir = Path(args.model_dir)
        if (model_dir / "resnet/clean/best.pth").exists():
            model_paths["resnet_clean"] = str(model_dir / "resnet/clean/best.pth")
        if (model_dir / "resnet/adv/best.pth").exists():
            model_paths["resnet_adv"] = str(model_dir / "resnet/adv/best.pth")
        if (model_dir / "vit/clean/best.pth").exists():
            model_paths["vit_clean"] = str(model_dir / "vit/clean/best.pth")
        if (model_dir / "vit/adv/best.pth").exists():
            model_paths["vit_adv"] = str(model_dir / "vit/adv/best.pth")

    models = load_models(device, model_paths)
    print(f"Loaded {len(models)} models: {list(models.keys())}")

    # Run experiments
    gradient_results = {}
    transfer_results = {}
    attention_results = {}

    if args.experiment in ["all", "gradient"]:
        gradient_results = run_gradient_analysis(
            models, test_loader, device, output_dir,
            num_batches=args.num_batches,
        )

    if args.experiment in ["all", "transfer"]:
        transfer_results = run_transfer_analysis(
            models, test_loader, device, output_dir,
            num_batches=args.num_batches,
            epsilon=args.epsilon,
        )

    if args.experiment in ["all", "attention"]:
        attention_results = run_attention_analysis(
            models, test_loader, device, output_dir,
            num_batches=args.num_batches,
            epsilon=args.epsilon,
        )

    # Create visualizations
    if args.visualize:
        create_visualizations(
            gradient_results,
            transfer_results,
            attention_results,
            output_dir,
        )

    # Final summary
    print("\n" + "="*60)
    print("EXPERIMENT COMPLETE")
    print("="*60)
    print(f"All results saved to: {output_dir}")

    # Save combined results
    all_results = {
        "config": vars(args),
        "gradient": gradient_results,
        "transfer": transfer_results,
        "attention": attention_results,
    }
    with open(output_dir / "all_results.json", "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    return all_results


def main():
    parser = argparse.ArgumentParser(
        description="Run SCI publication analysis experiments"
    )
    parser.add_argument(
        "--experiment",
        type=str,
        choices=["all", "gradient", "transfer", "attention"],
        default="all",
        help="Which experiment to run",
    )
    parser.add_argument(
        "--model-dir",
        type=str,
        default="./models",
        help="Directory containing trained models",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./results/sci_paper",
        help="Output directory for results",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch size for evaluation",
    )
    parser.add_argument(
        "--num-batches",
        type=int,
        default=10,
        help="Number of batches to analyze",
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=8/255,
        help="Perturbation budget for attacks",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Device to use (cuda/cpu)",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of data loading workers",
    )
    parser.add_argument(
        "--visualize",
        action="store_true",
        default=True,
        help="Create visualizations",
    )
    parser.add_argument(
        "--no-visualize",
        action="store_false",
        dest="visualize",
        help="Skip visualizations",
    )

    args = parser.parse_args()
    run_all_experiments(args)


if __name__ == "__main__":
    main()
