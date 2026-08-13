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
import os
from datetime import datetime
import gc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders, get_loaders
from src.utils.load_model_auto import load_model_auto
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
    """Full seeding (M15): python-random + cudnn determinism dahil."""
    import random
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_model(model_type, model_path, device):
    # Q1: num_classes checkpoint'ten otomatik cikarilir (CIFAR-100 destegi)
    return load_model_auto(model_type, model_path, device)


# =============================================================================
# 1. TRANSFER ANALYSIS
# =============================================================================
def _bootstrap_ci(values: np.ndarray, n_boot: int = 1000, seed: int = 42):
    """Percentile bootstrap 95% CI for the mean of a boolean/float array."""
    rng = np.random.default_rng(seed)
    n = len(values)
    if n == 0:
        return (float('nan'), float('nan'))
    boot_means = np.array([
        values[rng.integers(0, n, n)].mean() for _ in range(n_boot)
    ])
    return (float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5)))


def run_transfer_analysis(device, n_samples=10000, output_dir="results/transfer_analysis_run3", seed=42,
                          dataset="cifar10", models_config=None):
    """Transfer analysis with the conditioned fooling-rate metric (M3).

    Onceki surum ham hedef-yanlis-siniflandirma oranini rapor ediyordu; bu,
    hedefin temiz hata oranini icerdiginden (ViT %26 vs CNN %20 temiz hata)
    mimariler arasi karsilastirmayi bozuyordu. Yeni birincil metrik:
    hedefin temiz-dogru siniflandirdigi ornekler icinde adversarial ornekle
    yanlisa donen oran (conditioned fooling rate). Ham oran da seffaflik
    icin raporlanir. Ornek-bazli bool dizileri .npz olarak kaydedilir
    (McNemar / bootstrap esli testleri icin) ve bootstrap %95 CI hesaplanir.
    """
    print("\n" + "=" * 70)
    print(f"TRANSFER ANALYSIS (conditioned metric, n={n_samples})")
    print("=" * 70)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    _, test_loader = get_loaders(dataset=dataset, data_dir='./data', test_batch_size=50)

    models_config = list((models_config or RUN2_MODELS).items())
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

            src_clean_ok, tgt_clean_ok = [], []
            src_adv_wrong, tgt_adv_wrong = [], []
            total = 0

            for images, labels in test_loader:
                if total >= n_samples:
                    break
                # Son partiyi tam n_samples'a kirp (M20)
                if total + labels.size(0) > n_samples:
                    keep = n_samples - total
                    images, labels = images[:keep], labels[:keep]

                images, labels = images.to(device), labels.to(device)

                adv_images = attack(images, labels)

                with torch.no_grad():
                    src_clean_pred = source_model(images).argmax(1)
                    tgt_clean_pred = target_model(images).argmax(1)
                    src_adv_pred = source_model(adv_images).argmax(1)
                    tgt_adv_pred = target_model(adv_images).argmax(1)

                src_clean_ok.append((src_clean_pred == labels).cpu().numpy())
                tgt_clean_ok.append((tgt_clean_pred == labels).cpu().numpy())
                src_adv_wrong.append((src_adv_pred != labels).cpu().numpy())
                tgt_adv_wrong.append((tgt_adv_pred != labels).cpu().numpy())

                total += labels.size(0)

            src_clean_ok = np.concatenate(src_clean_ok)
            tgt_clean_ok = np.concatenate(tgt_clean_ok)
            src_adv_wrong = np.concatenate(src_adv_wrong)
            tgt_adv_wrong = np.concatenate(tgt_adv_wrong)

            # Ham oranlar (eski metrik - seffaflik icin)
            source_rate_raw = 100. * src_adv_wrong.mean()
            transfer_rate_raw = 100. * tgt_adv_wrong.mean()

            # Kosullu fooling rate (birincil metrik, M3):
            # hedefin temiz-dogru orneklerinde adv ile yanlisa donme orani
            cond_mask = tgt_clean_ok
            cond_fool = tgt_adv_wrong[cond_mask]
            cond_rate = 100. * cond_fool.mean() if cond_mask.sum() > 0 else float('nan')
            ci_lo, ci_hi = _bootstrap_ci(cond_fool.astype(float), n_boot=1000, seed=seed)

            print(f"    Raw: src={source_rate_raw:.2f}%, tgt={transfer_rate_raw:.2f}% | "
                  f"Conditioned fooling: {cond_rate:.2f}% "
                  f"[95% CI {100*ci_lo:.2f}-{100*ci_hi:.2f}] (n_cond={int(cond_mask.sum())})")

            # Ornek-bazli loglar: esli testler icin (M3/M8)
            np.savez(
                output_dir / f"per_sample_{source_name}_to_{target_name}.npz",
                source_clean_correct=src_clean_ok,
                target_clean_correct=tgt_clean_ok,
                source_adv_wrong=src_adv_wrong,
                target_adv_wrong=tgt_adv_wrong,
            )

            results.append({
                'source': source_name,
                'target': target_name,
                'attack_success_raw': float(source_rate_raw),
                'transfer_rate_raw': float(transfer_rate_raw),
                'conditioned_fooling_rate': float(cond_rate),
                'conditioned_ci95': [100 * ci_lo, 100 * ci_hi],
                'n_conditioned': int(cond_mask.sum()),
                'target_clean_acc': float(100. * tgt_clean_ok.mean()),
                'is_self': i == j,
                'total_samples': int(total),
            })

            if i != j:
                del target_model
                clear_gpu()

        del source_model, attack
        clear_gpu()

    # Save
    models = [m[0] for m in models_config]
    matrix = np.zeros((len(models), len(models)))          # conditioned (primary)
    matrix_raw = np.zeros((len(models), len(models)))      # raw (legacy)
    for r in results:
        ii = models.index(r['source'])
        jj = models.index(r['target'])
        matrix[ii, jj] = r['conditioned_fooling_rate']
        matrix_raw[ii, jj] = r['transfer_rate_raw']

    summary = {
        'timestamp': datetime.now().isoformat(),
        'models': models,
        'metric': 'conditioned_fooling_rate',
        'matrix': matrix.tolist(),
        'matrix_raw': matrix_raw.tolist(),
        'eps': EPS,
        'steps': STEPS,
        'n_samples': n_samples,
        'seed': seed,
        'dataset': dataset,
        'model_variant': 'run3-metric',
        # Provenans: gercekten degerlendirilen modeller (models_config),
        # modul-duzeyi RUN2_MODELS degil (Q1 review bulgusu)
        'model_paths': {name: cfg[1] for name, cfg in models_config},
        'results': results,
    }

    with open(output_dir / "transfer_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    pd.DataFrame(results).to_csv(output_dir / "transfer_results.csv", index=False)
    np.save(output_dir / "transfer_matrix.npy", matrix)
    np.save(output_dir / "transfer_matrix_raw.npy", matrix_raw)

    print(f"\nTransfer matrix (conditioned fooling rate):")
    print(f"  CNN → ViT: {matrix[0, 1]:.1f}%  (raw: {matrix_raw[0, 1]:.1f}%)")
    print(f"  ViT → CNN: {matrix[1, 0]:.1f}%  (raw: {matrix_raw[1, 0]:.1f}%)")
    print(f"  Asymmetry: {matrix[0, 1] - matrix[1, 0]:+.1f}pp (conditioned)")
    print(f"Saved to {output_dir}")

    return summary


# =============================================================================
# 2. GRADIENT ANALYSIS (500 samples)
# =============================================================================
def run_gradient_analysis(device, seed=42, output_dir="results/gradient_analysis_run3"):
    print("\n" + "=" * 70)
    print("GRADIENT ANALYSIS (500 samples, scale-invariant metrics)")
    print("=" * 70)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    n_samples = 500
    batch_size = 50  # 10 tam parti = tam 500 ornek (M20)
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=batch_size)

    # Native-cozunurluk kontrolu (M11): 32->224 upsample confound'unu test
    # etmek icin CIFAR-native ViT checkpoint'i varsa analize dahil et
    models_to_analyze = dict(RUN2_MODELS)
    native_ckpt = "models/vit_cifar_tiny/adv/vit_cifar_tiny/adv/adversarial_training/best.pth"
    if Path(native_ckpt).exists():
        models_to_analyze["ViT_CIFAR_Native_AT"] = ("vit_cifar_tiny", native_ckpt)
        print("Native-resolution ViT control included (vit_cifar_tiny)")

    all_stats = {}
    gradient_data = {}

    for name, (model_type, model_path) in models_to_analyze.items():
        print(f"\nAnalyzing: {name}")
        clear_gpu()

        model = load_model(model_type, model_path, device)
        analyzer = GradientAnalyzer(model, device)

        # Accumulate gradient statistics over multiple batches
        all_l2_norms = []
        all_linf_norms = []
        all_sparsities = []
        all_hoyer = []
        all_gini = []
        all_rel_sparsity = []
        all_spatial_vars = []
        all_alignments = []
        total_collected = 0

        for batch_idx, (images, labels) in enumerate(test_loader):
            if total_collected >= n_samples:
                break
            # Son partiyi tam n_samples'a kirp (M20)
            if total_collected + images.size(0) > n_samples:
                keep = n_samples - total_collected
                images, labels = images[:keep], labels[:keep]

            images, labels = images.to(device), labels.to(device)

            # Compute per-batch gradient statistics
            stats = analyzer.compute_gradient_statistics(images, labels)
            all_l2_norms.append(stats['l2_norm_mean'])
            all_linf_norms.append(stats['linf_norm_mean'])
            all_sparsities.append(stats['sparsity'])
            all_hoyer.append(stats['sparsity_hoyer'])
            all_gini.append(stats['sparsity_gini'])
            all_rel_sparsity.append(stats['sparsity_rel_threshold'])
            all_spatial_vars.append(stats['spatial_variance'])

            # Compute alignment (tum-ciftler, M21)
            alignment = analyzer.compute_gradient_alignment(images, labels)
            all_alignments.append(alignment)

            total_collected += images.size(0)

            if batch_idx % 5 == 0:
                print(f"  Batch {batch_idx}, collected {total_collected}/{n_samples} samples")

        # Aggregate (± degerleri parti-ortalamalari uzerinden std'dir; makalede
        # bu sekilde beyan edilmeli, M20)
        aggregated_stats = {
            'l2_norm_mean': float(np.mean(all_l2_norms)),
            'l2_norm_std': float(np.std(all_l2_norms)),
            'linf_norm_mean': float(np.mean(all_linf_norms)),
            'sparsity': float(np.mean(all_sparsities)),
            'sparsity_std': float(np.std(all_sparsities)),
            'sparsity_hoyer': float(np.mean(all_hoyer)),
            'sparsity_hoyer_std': float(np.std(all_hoyer)),
            'sparsity_gini': float(np.mean(all_gini)),
            'sparsity_gini_std': float(np.std(all_gini)),
            'sparsity_rel_threshold': float(np.mean(all_rel_sparsity)),
            'sparsity_rel_threshold_std': float(np.std(all_rel_sparsity)),
            'spatial_variance': float(np.mean(all_spatial_vars)),
            'gradient_alignment': float(np.mean(all_alignments)),
            'gradient_alignment_std': float(np.std(all_alignments)),
            'std_semantics': 'std across batch means (10 batches of 50)',
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
        'seed': seed,
        'model_variant': 'run3-metric',
        'model_paths': {k: v[1] for k, v in RUN2_MODELS.items()},
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
            'sparsity_hoyer': stats['sparsity_hoyer'],
            'sparsity_hoyer_std': stats['sparsity_hoyer_std'],
            'sparsity_gini': stats['sparsity_gini'],
            'sparsity_gini_std': stats['sparsity_gini_std'],
            'sparsity_rel_threshold': stats['sparsity_rel_threshold'],
            'sparsity_rel_threshold_std': stats['sparsity_rel_threshold_std'],
            'spatial_variance': stats['spatial_variance'],
            'gradient_alignment': stats['gradient_alignment'],
            'gradient_alignment_std': stats['gradient_alignment_std'],
            'n_samples': stats['n_samples'],
        })
    pd.DataFrame(comparison).to_csv(output_dir / "gradient_statistics.csv", index=False)

    # Visualization
    colors = ['#2ecc71', '#e74c3c', '#3498db']  # 3. renk: native-res ViT kontrolu
    model_names = list(all_stats.keys())

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for i, (name, data) in enumerate(gradient_data.items()):
        ax1.hist(data['l2_norms'], bins=20, alpha=0.6, label=name, color=colors[i])
    ax1.set_xlabel('Gradient L2 Norm', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Gradient Norm Distribution: CNN vs ViT', fontsize=14)
    ax1.legend()
    fig1.savefig(output_dir / "gradient_norm_distribution.pdf", dpi=300, bbox_inches='tight')
    plt.close(fig1)

    print(f"\nSaved to {output_dir}")

    # Key findings
    resnet = all_stats[model_names[0]]
    vit = all_stats[model_names[1]]
    print(f"\nKey Findings ({n_samples} samples):")
    print(f"  Sparsity ratio, absolute threshold (ResNet/ViT): {resnet['sparsity']/vit['sparsity']:.2f}x  [OLCEK BAGIMLI - dikkat]")
    print(f"  Hoyer sparsity: ResNet={resnet['sparsity_hoyer']:.4f}, ViT={vit['sparsity_hoyer']:.4f}")
    print(f"  Gini sparsity: ResNet={resnet['sparsity_gini']:.4f}, ViT={vit['sparsity_gini']:.4f}")
    print(f"  Relative-threshold sparsity: ResNet={resnet['sparsity_rel_threshold']:.4f}, ViT={vit['sparsity_rel_threshold']:.4f}")
    print(f"  Alignment ratio (ViT/ResNet): {vit['gradient_alignment']/resnet['gradient_alignment']:.2f}x")
    if "ViT_CIFAR_Native_AT" in all_stats:
        nat = all_stats["ViT_CIFAR_Native_AT"]
        print(f"  Native-res ViT control: Hoyer={nat['sparsity_hoyer']:.4f}, "
              f"Gini={nat['sparsity_gini']:.4f} (upsample confound testi, M11)")

    return summary


# =============================================================================
# 3. FEATURE DEGRADATION / ATTENTION ANALYSIS
# =============================================================================
def run_feature_degradation_analysis(device, seed=42, output_dir="results/attention_analysis_run3"):
    print("\n" + "=" * 70)
    print("FEATURE DEGRADATION ANALYSIS")
    print("=" * 70)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    n_samples = 100
    batch_size = 20  # 5 tam parti = tam 100 ornek (M20)
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
        # Son partiyi tam n_samples'a kirp (M20)
        if total_collected + images.size(0) > n_samples:
            keep = n_samples - total_collected
            images, labels = images[:keep], labels[:keep]

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
        'model': 'ViT-Tiny AT',
        'attack': f'PGD-{STEPS} (eps={EPS:.4f})',
        'n_samples': total_collected,
        'seed': seed,
        'clean_accuracy': 100 * total_clean_correct / total_collected,
        'adv_accuracy': 100 * total_adv_correct / total_collected,
        'model_variant': 'run3-metric',
        'model_paths': {k: v[1] for k, v in RUN2_MODELS.items()},
        'hook_target': 'transformer block MLP sub-block outputs (blocks.*.mlp)',
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
    """NOT: Bu analiz yalnizca SALDIRI BASLATMA rastgeleligini olcer -
    test loader shuffle=False oldugundan ayni ilk 1000 ornek kullanilir ve
    clean accuracy seed'ler arasi degismez (M18). Makalede bu sekilde
    beyan edilmelidir; egitim-seviyesi varyans icin bagimsiz egitim
    kosulari gerekir."""
    print("\n" + "=" * 70)
    print("STATISTICAL VALIDATION (attack-init randomness only)")
    print("=" * 70)

    output_dir = Path(os.environ.get("STATVAL_OUT_DIR", "results/statistical_validation_run3"))
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
            'model_variant': 'run3-metric',
            'model_paths': {k: v[1] for k, v in RUN2_MODELS.items()},
            'results': all_results
        }, f, indent=2)

    pd.DataFrame(all_results).to_csv(output_dir / "statistical_summary.csv", index=False)
    print(f"\nSaved to {output_dir}")

    return all_results


# =============================================================================
# MAIN
# =============================================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run2/run3 analyses (seeded, conditioned transfer metric)")
    parser.add_argument("--only", type=str, default="all",
                        choices=["all", "transfer", "gradient", "attention", "statistical"],
                        help="Run only the selected analysis")
    parser.add_argument("--dataset", type=str, default="cifar10",
                        help="Transfer analizi veri kumesi (Q1); diger analizler "
                             "simdilik cifar10-sabittir ve farkli kumeyle reddedilir")
    parser.add_argument("--n-samples", type=int, default=10000,
                        help="Transfer analysis sample count (default: full test set)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--resnet-path", type=str, default=None,
                        help="Override ResNet18 AT checkpoint path (run3 icin)")
    parser.add_argument("--vit-path", type=str, default=None,
                        help="Override ViT-Tiny AT checkpoint path (run3 icin)")
    parser.add_argument("--transfer-output-dir", type=str,
                        default="results/transfer_analysis_run3",
                        help="Transfer analizi cikti dizini (C19 clean-model kosusu icin)")
    args = parser.parse_args()

    if args.resnet_path:
        RUN2_MODELS["ResNet18_AT"] = ("resnet18", args.resnet_path)
    if args.vit_path:
        RUN2_MODELS["ViT_Tiny_AT"] = ("vit_tiny", args.vit_path)

    # Tum analizler icin tam seed (M15): PGD random-start dahil
    set_seed(args.seed)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seed: {args.seed}, only: {args.only}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"\nModel Paths:")
    for name, (mtype, mpath) in RUN2_MODELS.items():
        print(f"  {name}: {mpath}")

    # Check models exist
    for name, (mtype, mpath) in RUN2_MODELS.items():
        if not Path(mpath).exists():
            print(f"ERROR: Model not found: {mpath}")
            sys.exit(1)
    print("\nAll models found. Starting analyses...\n")

    results = {}

    if args.dataset != "cifar10" and args.only != "transfer":
        sys.exit("FATAL: --dataset != cifar10 yalniz --only transfer ile kullanilabilir "
                 "(gradyan/attention/statistical analizleri cifar10-sabit)")

    if args.only in ("all", "transfer"):
        results['transfer'] = run_transfer_analysis(
            device, n_samples=args.n_samples, seed=args.seed,
            output_dir=args.transfer_output_dir, dataset=args.dataset)

    if args.only in ("all", "gradient"):
        results['gradient'] = run_gradient_analysis(device, seed=args.seed)

    if args.only in ("all", "attention"):
        results['feature_degradation'] = run_feature_degradation_analysis(
            device, seed=args.seed)

    if args.only in ("all", "statistical"):
        results['statistical'] = run_statistical_validation(device)

    print("\n" + "=" * 70)
    print("ANALYSES COMPLETE")
    print("=" * 70)
    print(f"\nResults saved to results/*_run3/ directories")
    print(f"Timestamp: {datetime.now().isoformat()}")
