#!/usr/bin/env python3
"""Re-run all analyses with run2 models for consistency.

This script runs:
1. Transfer analysis (run2 models)
2. Gradient analysis (run2 models, 500 samples instead of 32)
3. Feature degradation / attention analysis (run2 models, larger sample)
4. Statistical validation (run2 models)

Output: results/*_run2/ directories
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import gc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders
from src.attacks import PGDAttack
from src.utils.checkpoint import load_model_weights
from src.analysis.gradient_analysis import GradientAnalyzer


# Run2 model paths
RUN2_MODELS = {
    "ResNet18_AT": ("resnet18", "models/resnet18/adv/at_run2/resnet18/adv/adversarial_training/best.pth"),
    "ViT_Tiny_AT": ("vit_tiny", "models/vit_tiny/adv/at_run2/vit_tiny/adv/adversarial_training/best.pth"),
}

EPS = 8/255
ALPHA = 2/255
STEPS = 10


def clear_gpu():
    gc.collect()
    torch.cuda.empty_cache()


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def load_model(model_type, model_path, device):
    model = ModelRegistry.get(model_type)
    load_model_weights(model, model_path, device)
    model = model.to(device)
    model.eval()
    return model


# =============================================================================
# 1. TRANSFER ANALYSIS
# =============================================================================
def run_transfer_analysis(device):
    print("\n" + "=" * 70)
    print("TRANSFER ANALYSIS (RUN2)")
    print("=" * 70)

    output_dir = Path("results/transfer_analysis_run2")
    output_dir.mkdir(parents=True, exist_ok=True)

    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=50)

    models_config = list(RUN2_MODELS.items())
    results = []

    for i, (source_name, (source_type, source_path)) in enumerate(models_config):
        print(f"\nSource Model: {source_name}")
        clear_gpu()
        source_model = load_model(source_type, source_path, device)
        attack = PGDAttack(source_model, eps=EPS, alpha=ALPHA, steps=STEPS)

        for j, (target_name, (target_type, target_path)) in enumerate(models_config):
            print(f"  Target: {target_name}")

            if i == j:
                target_model = source_model
            else:
                clear_gpu()
                target_model = load_model(target_type, target_path, device)

            total = 0
            source_success = 0
            transfer_success = 0

            for batch_idx, (images, labels) in enumerate(test_loader):
                if batch_idx >= 20:
                    break
                images, labels = images.to(device), labels.to(device)

                adv_images = attack(images, labels)

                with torch.no_grad():
                    source_pred = source_model(adv_images).argmax(1)
                    source_success += (source_pred != labels).sum().item()

                    target_pred = target_model(adv_images).argmax(1)
                    transfer_success += (target_pred != labels).sum().item()

                total += labels.size(0)

            source_rate = 100. * source_success / total
            transfer_rate = 100. * transfer_success / total

            print(f"    Source Attack: {source_rate:.2f}%, Transfer: {transfer_rate:.2f}%")

            results.append({
                'source': source_name,
                'target': target_name,
                'attack_success': source_rate,
                'transfer_rate': transfer_rate,
                'is_self': i == j,
                'total_samples': total,
            })

            if i != j:
                del target_model
                clear_gpu()

        del source_model, attack
        clear_gpu()

    # Save
    models = [m[0] for m in models_config]
    matrix = np.zeros((len(models), len(models)))
    for r in results:
        ii = models.index(r['source'])
        jj = models.index(r['target'])
        matrix[ii, jj] = r['transfer_rate']

    summary = {
        'timestamp': datetime.now().isoformat(),
        'models': models,
        'matrix': matrix.tolist(),
        'eps': EPS,
        'steps': STEPS,
        'model_variant': 'run2',
        'results': results,
    }

    with open(output_dir / "transfer_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    pd.DataFrame(results).to_csv(output_dir / "transfer_results.csv", index=False)
    np.save(output_dir / "transfer_matrix.npy", matrix)

    print(f"\nTransfer matrix (run2):")
    print(f"  CNN → ViT: {matrix[0, 1]:.1f}%")
    print(f"  ViT → CNN: {matrix[1, 0]:.1f}%")
    print(f"  Asymmetry: {abs(matrix[0, 1] - matrix[1, 0]):.1f}%")
    print(f"Saved to {output_dir}")

    return summary


# =============================================================================
# 2. GRADIENT ANALYSIS (500 samples)
# =============================================================================
def run_gradient_analysis(device):
    print("\n" + "=" * 70)
    print("GRADIENT ANALYSIS (RUN2, 500 samples)")
    print("=" * 70)

    output_dir = Path("results/gradient_analysis_run2")
    output_dir.mkdir(parents=True, exist_ok=True)

    n_samples = 500
    batch_size = 32
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=batch_size)

    all_stats = {}
    gradient_data = {}

    for name, (model_type, model_path) in RUN2_MODELS.items():
        print(f"\nAnalyzing: {name}")
        clear_gpu()

        model = load_model(model_type, model_path, device)
        analyzer = GradientAnalyzer(model, device)

        # Accumulate gradient statistics over multiple batches
        all_l2_norms = []
        all_linf_norms = []
        all_sparsities = []
        all_spatial_vars = []
        all_alignments = []
        total_collected = 0

        for batch_idx, (images, labels) in enumerate(test_loader):
            if total_collected >= n_samples:
                break

            images, labels = images.to(device), labels.to(device)

            # Compute per-batch gradient statistics
            stats = analyzer.compute_gradient_statistics(images, labels)
            all_l2_norms.append(stats['l2_norm_mean'])
            all_linf_norms.append(stats['linf_norm_mean'])
            all_sparsities.append(stats['sparsity'])
            all_spatial_vars.append(stats['spatial_variance'])

            # Compute alignment
            alignment = analyzer.compute_gradient_alignment(images, labels)
            all_alignments.append(alignment)

            total_collected += images.size(0)

            if batch_idx % 5 == 0:
                print(f"  Batch {batch_idx}, collected {total_collected}/{n_samples} samples")

        # Aggregate
        aggregated_stats = {
            'l2_norm_mean': float(np.mean(all_l2_norms)),
            'l2_norm_std': float(np.std(all_l2_norms)),
            'linf_norm_mean': float(np.mean(all_linf_norms)),
            'sparsity': float(np.mean(all_sparsities)),
            'sparsity_std': float(np.std(all_sparsities)),
            'spatial_variance': float(np.mean(all_spatial_vars)),
            'gradient_alignment': float(np.mean(all_alignments)),
            'gradient_alignment_std': float(np.std(all_alignments)),
            'n_samples': total_collected,
            'n_batches': len(all_l2_norms),
        }

        all_stats[name] = aggregated_stats

        print(f"  L2 Norm: {aggregated_stats['l2_norm_mean']:.6f} (±{aggregated_stats['l2_norm_std']:.6f})")
        print(f"  Sparsity: {aggregated_stats['sparsity']:.4f} (±{aggregated_stats['sparsity_std']:.4f})")
        print(f"  Alignment: {aggregated_stats['gradient_alignment']:.4f} (±{aggregated_stats['gradient_alignment_std']:.4f})")

        # Store last batch gradient data for visualization
        grads = analyzer.compute_input_gradients(images, labels)
        gradient_data[name] = {
            'grads': grads.cpu(),
            'l2_norms': torch.norm(grads.view(grads.shape[0], -1), p=2, dim=1).cpu().numpy()
        }

        # Gradient landscape (on last batch)
        landscape = analyzer.compare_gradient_landscapes(
            images, labels,
            epsilon_range=[0.002, 0.004, 0.008, 0.016, 0.031]
        )
        all_stats[name]['landscape'] = landscape

        del model, analyzer
        clear_gpu()

    # Save
    summary = {
        'timestamp': datetime.now().isoformat(),
        'models': list(all_stats.keys()),
        'n_samples': n_samples,
        'model_variant': 'run2',
        'statistics': {k: {kk: vv for kk, vv in v.items() if kk != 'landscape'}
                       for k, v in all_stats.items()},
    }

    with open(output_dir / "gradient_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # Create comparison table
    comparison = []
    for name, stats in all_stats.items():
        comparison.append({
            'model': name,
            'l2_norm_mean': stats['l2_norm_mean'],
            'l2_norm_std': stats['l2_norm_std'],
            'linf_norm_mean': stats['linf_norm_mean'],
            'sparsity': stats['sparsity'],
            'sparsity_std': stats['sparsity_std'],
            'spatial_variance': stats['spatial_variance'],
            'gradient_alignment': stats['gradient_alignment'],
            'gradient_alignment_std': stats['gradient_alignment_std'],
            'n_samples': stats['n_samples'],
        })
    pd.DataFrame(comparison).to_csv(output_dir / "gradient_statistics.csv", index=False)

    # Visualization
    colors = ['#2ecc71', '#e74c3c']
    model_names = list(all_stats.keys())

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for i, (name, data) in enumerate(gradient_data.items()):
        ax1.hist(data['l2_norms'], bins=20, alpha=0.6, label=name, color=colors[i])
    ax1.set_xlabel('Gradient L2 Norm', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Gradient Norm Distribution: CNN vs ViT (Run2)', fontsize=14)
    ax1.legend()
    fig1.savefig(output_dir / "gradient_norm_distribution.pdf", dpi=300, bbox_inches='tight')
    plt.close(fig1)

    print(f"\nSaved to {output_dir}")

    # Key findings
    resnet = all_stats[model_names[0]]
    vit = all_stats[model_names[1]]
    print(f"\nKey Findings (run2, {n_samples} samples):")
    print(f"  Sparsity ratio (ResNet/ViT): {resnet['sparsity']/vit['sparsity']:.1f}x")
    print(f"  Alignment ratio (ViT/ResNet): {vit['gradient_alignment']/resnet['gradient_alignment']:.1f}x")

    return summary


# =============================================================================
# 3. FEATURE DEGRADATION / ATTENTION ANALYSIS
# =============================================================================
def run_feature_degradation_analysis(device):
    print("\n" + "=" * 70)
    print("FEATURE DEGRADATION ANALYSIS (RUN2)")
    print("=" * 70)

    output_dir = Path("results/attention_analysis_run2")
    output_dir.mkdir(parents=True, exist_ok=True)

    n_samples = 100  # More than 16, reasonable for feature analysis
    batch_size = 16
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=batch_size)

    # Load ViT model (run2)
    vit_type, vit_path = RUN2_MODELS["ViT_Tiny_AT"]
    print(f"\nLoading ViT-Tiny AT (run2)...")
    model = load_model(vit_type, vit_path, device)

    attack = PGDAttack(model, eps=EPS, alpha=ALPHA, steps=STEPS)

    # Collect multiple batches
    all_feature_results = []  # List of per-batch results
    total_collected = 0
    total_clean_correct = 0
    total_adv_correct = 0

    for batch_idx, (images, labels) in enumerate(test_loader):
        if total_collected >= n_samples:
            break

        images, labels = images.to(device), labels.to(device)

        # Generate adversarial examples
        adv_images = attack(images, labels)

        # Check predictions
        with torch.no_grad():
            clean_pred = model(images).argmax(1)
            adv_pred = model(adv_images).argmax(1)
            total_clean_correct += (clean_pred == labels).sum().item()
            total_adv_correct += (adv_pred == labels).sum().item()

        # Hook intermediate layers
        clean_features = {}
        adv_features = {}
        hooks = []

        def get_hook(storage, name):
            def hook(module, input, output):
                if isinstance(output, torch.Tensor):
                    storage[name] = output.detach()
            return hook

        inner_model = model.model if hasattr(model, 'model') else model
        target_layers = []
        for name, module in inner_model.named_modules():
            if 'blocks' in name and name.endswith('.mlp'):
                target_layers.append((name, module))

        # All layers (not just first 3 + last 3)
        for name, module in target_layers:
            hooks.append(module.register_forward_hook(get_hook(clean_features, name)))
        with torch.no_grad():
            _ = model(images)
        for hook in hooks:
            hook.remove()

        hooks = []
        for name, module in target_layers:
            hooks.append(module.register_forward_hook(get_hook(adv_features, name)))
        with torch.no_grad():
            _ = model(adv_images)
        for hook in hooks:
            hook.remove()

        # Compute per-batch feature metrics
        batch_results = {}
        for layer_name in clean_features.keys():
            if layer_name not in adv_features:
                continue
            clean_feat = clean_features[layer_name]
            adv_feat = adv_features[layer_name]

            l2_dist = torch.norm(clean_feat - adv_feat, p=2, dim=-1).mean().item()
            clean_flat = clean_feat.view(clean_feat.size(0), -1)
            adv_flat = adv_feat.view(adv_feat.size(0), -1)
            cos_sim = F.cosine_similarity(clean_flat, adv_flat, dim=-1).mean().item()
            clean_norm = torch.norm(clean_feat, p=2, dim=-1).mean().item()
            adv_norm = torch.norm(adv_feat, p=2, dim=-1).mean().item()
            norm_change = (adv_norm - clean_norm) / clean_norm * 100

            batch_results[layer_name] = {
                'l2_distance': l2_dist,
                'cosine_similarity': cos_sim,
                'clean_norm': clean_norm,
                'adv_norm': adv_norm,
                'norm_change_pct': norm_change,
            }

        all_feature_results.append(batch_results)
        total_collected += images.size(0)

        if batch_idx % 2 == 0:
            print(f"  Batch {batch_idx}, collected {total_collected}/{n_samples}")

    # Aggregate across batches
    layer_names = list(all_feature_results[0].keys())
    aggregated = []

    for layer_name in layer_names:
        l2_dists = [b[layer_name]['l2_distance'] for b in all_feature_results if layer_name in b]
        cos_sims = [b[layer_name]['cosine_similarity'] for b in all_feature_results if layer_name in b]
        norm_changes = [b[layer_name]['norm_change_pct'] for b in all_feature_results if layer_name in b]
        clean_norms = [b[layer_name]['clean_norm'] for b in all_feature_results if layer_name in b]
        adv_norms = [b[layer_name]['adv_norm'] for b in all_feature_results if layer_name in b]

        agg = {
            'layer': layer_name,
            'l2_distance': float(np.mean(l2_dists)),
            'l2_distance_std': float(np.std(l2_dists)),
            'cosine_similarity': float(np.mean(cos_sims)),
            'cosine_similarity_std': float(np.std(cos_sims)),
            'clean_norm': float(np.mean(clean_norms)),
            'adv_norm': float(np.mean(adv_norms)),
            'norm_change_pct': float(np.mean(norm_changes)),
            'norm_change_pct_std': float(np.std(norm_changes)),
        }
        aggregated.append(agg)

        print(f"  {layer_name}: cosine={agg['cosine_similarity']:.4f}±{agg['cosine_similarity_std']:.4f}, "
              f"L2={agg['l2_distance']:.4f}, norm_change={agg['norm_change_pct']:+.2f}%")

    # Save
    df = pd.DataFrame(aggregated)
    df.to_csv(output_dir / "attention_feature_analysis.csv", index=False)

    summary = {
        'timestamp': datetime.now().isoformat(),
        'model': 'ViT-Tiny AT (run2)',
        'attack': f'PGD-{STEPS} (eps={EPS:.4f})',
        'n_samples': total_collected,
        'clean_accuracy': 100 * total_clean_correct / total_collected,
        'adv_accuracy': 100 * total_adv_correct / total_collected,
        'model_variant': 'run2',
        'feature_analysis': aggregated,
    }

    with open(output_dir / "attention_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # Visualization
    layers_short = [r['layer'].split('.')[-2] for r in aggregated]
    l2_dists_agg = [r['l2_distance'] for r in aggregated]
    cos_sims_agg = [r['cosine_similarity'] for r in aggregated]
    norm_changes_agg = [r['norm_change_pct'] for r in aggregated]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].bar(range(len(layers_short)), l2_dists_agg, color='#e74c3c')
    axes[0].set_xticks(range(len(layers_short)))
    axes[0].set_xticklabels(layers_short, rotation=45, ha='right')
    axes[0].set_ylabel('L2 Distance')
    axes[0].set_title('Feature L2 Distance (Clean vs Adversarial) - Run2')

    axes[1].bar(range(len(layers_short)), cos_sims_agg, color='#2ecc71')
    axes[1].set_xticks(range(len(layers_short)))
    axes[1].set_xticklabels(layers_short, rotation=45, ha='right')
    axes[1].set_ylabel('Cosine Similarity')
    axes[1].set_title('Feature Cosine Similarity - Run2')
    axes[1].set_ylim(0, 1)

    bar_colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in norm_changes_agg]
    axes[2].bar(range(len(layers_short)), norm_changes_agg, color=bar_colors)
    axes[2].set_xticks(range(len(layers_short)))
    axes[2].set_xticklabels(layers_short, rotation=45, ha='right')
    axes[2].set_ylabel('Norm Change (%)')
    axes[2].set_title('Feature Norm Change - Run2')
    axes[2].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    fig.savefig(output_dir / "feature_degradation.pdf", dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"\nSaved to {output_dir}")
    return summary


# =============================================================================
# 4. STATISTICAL VALIDATION
# =============================================================================
def run_statistical_validation(device):
    print("\n" + "=" * 70)
    print("STATISTICAL VALIDATION (RUN2)")
    print("=" * 70)

    output_dir = Path("results/statistical_validation_run2")
    output_dir.mkdir(parents=True, exist_ok=True)

    seeds = [42, 123, 456]
    n_samples = 1000

    all_results = []

    for name, (model_type, model_path) in RUN2_MODELS.items():
        print(f"\nModel: {name}")
        model_results = []

        for seed in seeds:
            print(f"  Seed: {seed}")
            set_seed(seed)
            clear_gpu()

            _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=100)
            model = load_model(model_type, model_path, device)
            attack = PGDAttack(model, eps=EPS, alpha=ALPHA, steps=STEPS)

            clean_correct = 0
            robust_correct = 0
            total = 0

            for images, labels in test_loader:
                if total >= n_samples:
                    break
                images, labels = images.to(device), labels.to(device)

                with torch.no_grad():
                    clean_correct += (model(images).argmax(1) == labels).sum().item()

                adv_images = attack(images, labels)
                with torch.no_grad():
                    robust_correct += (model(adv_images).argmax(1) == labels).sum().item()

                total += images.size(0)

            result = {
                'seed': seed,
                'model': name,
                'clean_acc': 100 * clean_correct / total,
                'robust_acc': 100 * robust_correct / total,
                'n_samples': total,
            }
            model_results.append(result)
            print(f"    Clean: {result['clean_acc']:.2f}%, Robust: {result['robust_acc']:.2f}%")

            del model, attack
            clear_gpu()

        clean_accs = [r['clean_acc'] for r in model_results]
        robust_accs = [r['robust_acc'] for r in model_results]

        summary = {
            'model': name,
            'clean_mean': float(np.mean(clean_accs)),
            'clean_std': float(np.std(clean_accs)),
            'robust_mean': float(np.mean(robust_accs)),
            'robust_std': float(np.std(robust_accs)),
            'n_runs': len(seeds),
            'n_samples': n_samples,
        }
        all_results.append(summary)
        print(f"  Summary: Clean={summary['clean_mean']:.2f}±{summary['clean_std']:.2f}, "
              f"Robust={summary['robust_mean']:.2f}±{summary['robust_std']:.2f}")

    # Save
    with open(output_dir / "statistical_validation.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'seeds': seeds,
            'n_samples': n_samples,
            'eps': EPS,
            'model_variant': 'run2',
            'results': all_results
        }, f, indent=2)

    pd.DataFrame(all_results).to_csv(output_dir / "statistical_summary.csv", index=False)
    print(f"\nSaved to {output_dir}")

    return all_results


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"\nRun2 Model Paths:")
    for name, (mtype, mpath) in RUN2_MODELS.items():
        print(f"  {name}: {mpath}")

    # Check models exist
    for name, (mtype, mpath) in RUN2_MODELS.items():
        if not Path(mpath).exists():
            print(f"ERROR: Model not found: {mpath}")
            sys.exit(1)
    print("\nAll models found. Starting analyses...\n")

    results = {}

    # 1. Transfer analysis
    results['transfer'] = run_transfer_analysis(device)

    # 2. Gradient analysis (500 samples)
    results['gradient'] = run_gradient_analysis(device)

    # 3. Feature degradation analysis
    results['feature_degradation'] = run_feature_degradation_analysis(device)

    # 4. Statistical validation
    results['statistical'] = run_statistical_validation(device)

    print("\n" + "=" * 70)
    print("ALL ANALYSES COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to:")
    print(f"  results/transfer_analysis_run2/")
    print(f"  results/gradient_analysis_run2/")
    print(f"  results/attention_analysis_run2/")
    print(f"  results/statistical_validation_run2/")
    print(f"\nTimestamp: {datetime.now().isoformat()}")
