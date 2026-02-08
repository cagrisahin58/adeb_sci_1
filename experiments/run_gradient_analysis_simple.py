#!/usr/bin/env python3
"""Simple gradient analysis - memory efficient."""

import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import gc
import matplotlib.pyplot as plt

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders
from src.utils.checkpoint import load_model_weights
from src.analysis.gradient_analysis import GradientAnalyzer


def clear_gpu():
    """Clear GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    output_dir = Path("results/gradient_analysis_20260110")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading CIFAR-10...")
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=32)

    # Get a batch of data for analysis
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)

    # Model configs - AT models only
    models_config = [
        ("ResNet18_AT", "resnet18", "models/resnet18/adv/adversarial_training/best.pth"),
        ("ViT_Tiny_AT", "vit_tiny", "models/vit_tiny/adv/adversarial_training/best.pth"),
    ]

    all_stats = {}
    gradient_data = {}

    for name, model_type, model_path in models_config:
        print(f"\n{'='*60}")
        print(f"Analyzing: {name}")
        print(f"{'='*60}")

        clear_gpu()

        # Load model
        model = ModelRegistry.get(model_type)
        load_model_weights(model, model_path, device)
        model = model.to(device)
        model.eval()

        # Create analyzer
        analyzer = GradientAnalyzer(model, device)

        # Compute gradient statistics
        print("Computing gradient statistics...")
        stats = analyzer.compute_gradient_statistics(images, labels)
        all_stats[name] = stats

        print(f"  L2 Norm (mean): {stats['l2_norm_mean']:.6f}")
        print(f"  L2 Norm (std): {stats['l2_norm_std']:.6f}")
        print(f"  L∞ Norm (mean): {stats['linf_norm_mean']:.6f}")
        print(f"  Sparsity: {stats['sparsity']:.4f}")
        print(f"  Spatial Variance: {stats['spatial_variance']:.6f}")

        # Compute gradient alignment
        print("Computing gradient alignment...")
        alignment = analyzer.compute_gradient_alignment(images, labels)
        all_stats[name]['gradient_alignment'] = alignment
        print(f"  Gradient Alignment: {alignment:.4f}")

        # Store raw gradients for visualization
        grads = analyzer.compute_input_gradients(images, labels)
        gradient_data[name] = {
            'grads': grads.cpu(),
            'l2_norms': torch.norm(grads.view(grads.shape[0], -1), p=2, dim=1).cpu().numpy()
        }

        # Compare gradient landscapes
        print("Computing gradient landscape...")
        landscape = analyzer.compare_gradient_landscapes(
            images, labels,
            epsilon_range=[0.002, 0.004, 0.008, 0.016, 0.031]  # 0.5/255 to 8/255
        )
        all_stats[name]['landscape'] = landscape

        del model
        del analyzer
        clear_gpu()

    # Save statistics
    print("\n" + "="*60)
    print("GRADIENT ANALYSIS SUMMARY")
    print("="*60)

    # Create comparison table
    comparison = []
    for name, stats in all_stats.items():
        row = {
            'model': name,
            'l2_norm_mean': stats['l2_norm_mean'],
            'l2_norm_std': stats['l2_norm_std'],
            'linf_norm_mean': stats['linf_norm_mean'],
            'sparsity': stats['sparsity'],
            'spatial_variance': stats['spatial_variance'],
            'gradient_alignment': stats['gradient_alignment'],
        }
        comparison.append(row)
        print(f"\n{name}:")
        print(f"  L2 Norm: {stats['l2_norm_mean']:.6f} ± {stats['l2_norm_std']:.6f}")
        print(f"  Sparsity: {stats['sparsity']:.4f}")
        print(f"  Gradient Alignment: {stats['gradient_alignment']:.4f}")

    df = pd.DataFrame(comparison)
    df.to_csv(output_dir / "gradient_statistics.csv", index=False)

    # Create visualizations
    print("\nCreating visualizations...")

    # Figure 1: L2 Norm Distribution
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    colors = ['#2ecc71', '#e74c3c']
    for i, (name, data) in enumerate(gradient_data.items()):
        ax1.hist(data['l2_norms'], bins=20, alpha=0.6, label=name, color=colors[i])
    ax1.set_xlabel('Gradient L2 Norm', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Gradient Norm Distribution: CNN vs ViT', fontsize=14)
    ax1.legend()
    fig1.savefig(output_dir / "gradient_norm_distribution.pdf", dpi=300, bbox_inches='tight')
    fig1.savefig(output_dir / "gradient_norm_distribution.png", dpi=150, bbox_inches='tight')
    plt.close(fig1)

    # Figure 2: Gradient Statistics Comparison
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    metrics = ['l2_norm_mean', 'linf_norm_mean', 'sparsity', 'spatial_variance', 'gradient_alignment']
    x = np.arange(len(metrics))
    width = 0.35

    model_names = list(all_stats.keys())
    values1 = [all_stats[model_names[0]][m] for m in metrics]
    values2 = [all_stats[model_names[1]][m] for m in metrics]

    # Normalize for visualization
    max_vals = [max(v1, v2) for v1, v2 in zip(values1, values2)]
    values1_norm = [v/m if m > 0 else 0 for v, m in zip(values1, max_vals)]
    values2_norm = [v/m if m > 0 else 0 for v, m in zip(values2, max_vals)]

    bars1 = ax2.bar(x - width/2, values1_norm, width, label=model_names[0], color='#2ecc71')
    bars2 = ax2.bar(x + width/2, values2_norm, width, label=model_names[1], color='#e74c3c')

    ax2.set_ylabel('Normalized Value', fontsize=12)
    ax2.set_title('Gradient Characteristics Comparison', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels(['L2 Norm', 'L∞ Norm', 'Sparsity', 'Spatial Var', 'Alignment'], fontsize=10)
    ax2.legend()

    # Add value labels
    for bars, values in [(bars1, values1), (bars2, values2)]:
        for bar, val in zip(bars, values):
            height = bar.get_height()
            ax2.annotate(f'{val:.4f}',
                        xy=(bar.get_x() + bar.get_width()/2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=45)

    fig2.savefig(output_dir / "gradient_comparison.pdf", dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / "gradient_comparison.png", dpi=150, bbox_inches='tight')
    plt.close(fig2)

    # Figure 3: Gradient Landscape
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for i, (name, stats) in enumerate(all_stats.items()):
        landscape = stats['landscape']
        ax3.plot(landscape['epsilons'], landscape['loss_gradient'],
                marker='o', label=f'{name} (gradient)', color=colors[i])
        ax3.plot(landscape['epsilons'], landscape['loss_random'],
                marker='x', linestyle='--', label=f'{name} (random)', color=colors[i], alpha=0.5)

    ax3.set_xlabel('Epsilon', fontsize=12)
    ax3.set_ylabel('Loss', fontsize=12)
    ax3.set_title('Loss Landscape: Gradient vs Random Perturbation', fontsize=14)
    ax3.legend()
    fig3.savefig(output_dir / "gradient_landscape.pdf", dpi=300, bbox_inches='tight')
    fig3.savefig(output_dir / "gradient_landscape.png", dpi=150, bbox_inches='tight')
    plt.close(fig3)

    # Figure 4: Sample Gradient Visualization
    fig4, axes = plt.subplots(2, 4, figsize=(16, 8))
    sample_indices = [0, 1, 2, 3]

    for idx, sample_idx in enumerate(sample_indices):
        # Original image
        img = images[sample_idx].cpu().permute(1, 2, 0).numpy()
        axes[0, idx].imshow(img.clip(0, 1))
        axes[0, idx].set_title(f'Sample {sample_idx}', fontsize=10)
        axes[0, idx].axis('off')

        # Gradient visualization (ResNet)
        grad_resnet = gradient_data[model_names[0]]['grads'][sample_idx].abs().mean(0).numpy()
        axes[1, idx].imshow(grad_resnet, cmap='hot')
        if idx == 0:
            axes[1, idx].set_ylabel('Gradient (ResNet)', fontsize=10)
        axes[1, idx].axis('off')

    fig4.suptitle('Input Gradients: ResNet18 AT', fontsize=14)
    fig4.savefig(output_dir / "gradient_samples_resnet.pdf", dpi=300, bbox_inches='tight')
    fig4.savefig(output_dir / "gradient_samples_resnet.png", dpi=150, bbox_inches='tight')
    plt.close(fig4)

    # Save summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'models': list(all_stats.keys()),
        'batch_size': 32,
        'statistics': {k: {kk: vv for kk, vv in v.items() if kk != 'landscape'}
                      for k, v in all_stats.items()},
    }

    with open(output_dir / "gradient_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to {output_dir}")

    # Key findings
    print("\n" + "="*60)
    print("KEY FINDINGS")
    print("="*60)

    resnet_stats = all_stats[model_names[0]]
    vit_stats = all_stats[model_names[1]]

    l2_ratio = resnet_stats['l2_norm_mean'] / vit_stats['l2_norm_mean']
    spatial_ratio = resnet_stats['spatial_variance'] / vit_stats['spatial_variance']

    print(f"  L2 Norm Ratio (ResNet/ViT): {l2_ratio:.2f}x")
    print(f"  Spatial Variance Ratio: {spatial_ratio:.2f}x")
    print(f"  ResNet Gradient Alignment: {resnet_stats['gradient_alignment']:.4f}")
    print(f"  ViT Gradient Alignment: {vit_stats['gradient_alignment']:.4f}")


if __name__ == "__main__":
    main()
