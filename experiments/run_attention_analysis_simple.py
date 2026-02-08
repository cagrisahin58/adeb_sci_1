#!/usr/bin/env python3
"""Simple attention degradation analysis for ViT under adversarial attacks."""

import torch
import torch.nn as nn
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
from src.attacks import PGDAttack
from src.utils.checkpoint import load_model_weights


def clear_gpu():
    """Clear GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()


class AttentionExtractor:
    """Extract attention maps from ViT model."""

    def __init__(self, model, device):
        self.model = model
        self.device = device
        self.attention_maps = {}
        self._hooks = []

    def _hook_fn(self, name):
        def hook(module, input, output):
            # For timm ViT, attention is computed as: attn = (q @ k.transpose(-2, -1)) * scale
            # We need to capture the attention weights
            if hasattr(module, 'scale'):
                # This is the Attention module
                self.attention_maps[name] = output.detach()
        return hook

    def register_hooks(self):
        """Register hooks on attention modules."""
        self._hooks = []
        self.attention_maps = {}

        # Access the inner model if wrapped
        inner_model = self.model.model if hasattr(self.model, 'model') else self.model

        for name, module in inner_model.named_modules():
            if 'attn' in name.lower():
                hook = module.register_forward_hook(self._hook_fn(name))
                self._hooks.append(hook)

    def remove_hooks(self):
        """Remove all hooks."""
        for hook in self._hooks:
            hook.remove()
        self._hooks = []

    def get_attention_maps(self, images):
        """Get attention maps for images."""
        self.model.eval()
        self.register_hooks()

        try:
            with torch.no_grad():
                _ = self.model(images.to(self.device))
            return {k: v.cpu() for k, v in self.attention_maps.items()}
        finally:
            self.remove_hooks()


def compute_attention_entropy(attention_map):
    """Compute entropy of attention distribution."""
    # Normalize to probability distribution
    attn = attention_map / (attention_map.sum(dim=-1, keepdim=True) + 1e-9)
    # Compute entropy
    entropy = -torch.sum(attn * torch.log(attn + 1e-9), dim=-1)
    return entropy.mean()


def compute_cls_attention_concentration(attention_map):
    """Compute how concentrated attention is on CLS token."""
    # attention_map shape: (batch, heads, seq, seq) or (batch, seq, seq)
    if attention_map.dim() == 4:
        # Average over heads
        attn = attention_map.mean(dim=1)
    else:
        attn = attention_map

    # CLS token is usually at position 0
    cls_attn = attn[:, :, 0]  # Attention TO CLS token from all positions
    # Or attention FROM CLS token
    from_cls = attn[:, 0, :]  # Attention from CLS to all patches

    return from_cls.mean().item(), cls_attn.mean().item()


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    output_dir = Path("results/attention_analysis_20260110")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading CIFAR-10...")
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=16)

    # Get a batch for analysis
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)

    # Load ViT model
    print("\nLoading ViT-Tiny AT model...")
    model = ModelRegistry.get("vit_tiny")
    load_model_weights(model, "models/vit_tiny/adv/adversarial_training/best.pth", device)
    model = model.to(device)
    model.eval()

    # Create PGD attack
    eps = 8/255
    alpha = 2/255
    steps = 10
    attack = PGDAttack(model, eps=eps, alpha=alpha, steps=steps)

    # Generate adversarial examples
    print("Generating adversarial examples...")
    adv_images = attack(images, labels)

    # Analyze predictions
    with torch.no_grad():
        clean_outputs = model(images)
        adv_outputs = model(adv_images)

        clean_pred = clean_outputs.argmax(dim=1)
        adv_pred = adv_outputs.argmax(dim=1)

        clean_correct = (clean_pred == labels).sum().item()
        adv_correct = (adv_pred == labels).sum().item()

    print(f"\nPrediction Analysis:")
    print(f"  Clean accuracy: {100*clean_correct/len(labels):.1f}%")
    print(f"  Adversarial accuracy: {100*adv_correct/len(labels):.1f}%")
    print(f"  Attack success: {100*(clean_correct-adv_correct)/clean_correct:.1f}%")

    # Extract features at different stages
    print("\nAnalyzing feature representations...")

    # Get intermediate features by hooking
    clean_features = {}
    adv_features = {}
    hooks = []

    def get_hook(storage, name):
        def hook(module, input, output):
            if isinstance(output, torch.Tensor):
                storage[name] = output.detach()
        return hook

    # Hook intermediate layers
    inner_model = model.model if hasattr(model, 'model') else model

    target_layers = []
    for name, module in inner_model.named_modules():
        if 'blocks' in name and name.endswith('.mlp'):
            target_layers.append((name, module))

    # Limit to a few layers
    target_layers = target_layers[:3] + target_layers[-3:]

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

    # Analyze feature changes
    print("\nFeature Change Analysis:")
    feature_results = []

    for layer_name in clean_features.keys():
        if layer_name not in adv_features:
            continue

        clean_feat = clean_features[layer_name]
        adv_feat = adv_features[layer_name]

        # Compute L2 distance
        l2_dist = torch.norm(clean_feat - adv_feat, p=2, dim=-1).mean().item()

        # Compute cosine similarity
        clean_flat = clean_feat.view(clean_feat.size(0), -1)
        adv_flat = adv_feat.view(adv_feat.size(0), -1)
        cos_sim = F.cosine_similarity(clean_flat, adv_flat, dim=-1).mean().item()

        # Compute feature norm change
        clean_norm = torch.norm(clean_feat, p=2, dim=-1).mean().item()
        adv_norm = torch.norm(adv_feat, p=2, dim=-1).mean().item()
        norm_change = (adv_norm - clean_norm) / clean_norm * 100

        result = {
            'layer': layer_name,
            'l2_distance': l2_dist,
            'cosine_similarity': cos_sim,
            'clean_norm': clean_norm,
            'adv_norm': adv_norm,
            'norm_change_pct': norm_change,
        }
        feature_results.append(result)

        print(f"  {layer_name}:")
        print(f"    L2 Distance: {l2_dist:.4f}")
        print(f"    Cosine Similarity: {cos_sim:.4f}")
        print(f"    Norm Change: {norm_change:+.2f}%")

    # Save results
    df = pd.DataFrame(feature_results)
    df.to_csv(output_dir / "attention_feature_analysis.csv", index=False)

    # Create visualizations
    print("\nCreating visualizations...")

    # Figure 1: Feature change across layers
    fig1, axes = plt.subplots(1, 3, figsize=(15, 5))

    layers = [r['layer'].split('.')[-2] for r in feature_results]
    l2_dists = [r['l2_distance'] for r in feature_results]
    cos_sims = [r['cosine_similarity'] for r in feature_results]
    norm_changes = [r['norm_change_pct'] for r in feature_results]

    axes[0].bar(range(len(layers)), l2_dists, color='#e74c3c')
    axes[0].set_xticks(range(len(layers)))
    axes[0].set_xticklabels(layers, rotation=45, ha='right')
    axes[0].set_ylabel('L2 Distance')
    axes[0].set_title('Feature L2 Distance (Clean vs Adversarial)')

    axes[1].bar(range(len(layers)), cos_sims, color='#2ecc71')
    axes[1].set_xticks(range(len(layers)))
    axes[1].set_xticklabels(layers, rotation=45, ha='right')
    axes[1].set_ylabel('Cosine Similarity')
    axes[1].set_title('Feature Cosine Similarity')
    axes[1].set_ylim(0, 1)

    colors = ['#e74c3c' if x < 0 else '#2ecc71' for x in norm_changes]
    axes[2].bar(range(len(layers)), norm_changes, color=colors)
    axes[2].set_xticks(range(len(layers)))
    axes[2].set_xticklabels(layers, rotation=45, ha='right')
    axes[2].set_ylabel('Norm Change (%)')
    axes[2].set_title('Feature Norm Change')
    axes[2].axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    plt.tight_layout()
    fig1.savefig(output_dir / "feature_degradation.pdf", dpi=300, bbox_inches='tight')
    fig1.savefig(output_dir / "feature_degradation.png", dpi=150, bbox_inches='tight')
    plt.close(fig1)

    # Figure 2: Sample visualizations
    fig2, axes = plt.subplots(3, 4, figsize=(16, 12))

    for i in range(4):
        # Original image
        img = images[i].cpu().permute(1, 2, 0).numpy()
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)
        axes[0, i].imshow(img)
        pred_label = clean_pred[i].item()
        axes[0, i].set_title(f'Clean (pred: {pred_label})')
        axes[0, i].axis('off')

        # Adversarial image
        adv_img = adv_images[i].cpu().permute(1, 2, 0).numpy()
        adv_img = (adv_img - adv_img.min()) / (adv_img.max() - adv_img.min() + 1e-8)
        axes[1, i].imshow(adv_img)
        adv_label = adv_pred[i].item()
        axes[1, i].set_title(f'Adversarial (pred: {adv_label})')
        axes[1, i].axis('off')

        # Perturbation (amplified for visibility)
        pert = (adv_images[i] - images[i]).cpu().permute(1, 2, 0).numpy()
        pert = np.abs(pert)
        pert = (pert - pert.min()) / (pert.max() - pert.min() + 1e-8)
        axes[2, i].imshow(pert)
        axes[2, i].set_title('Perturbation (amplified)')
        axes[2, i].axis('off')

    plt.tight_layout()
    fig2.savefig(output_dir / "adversarial_samples.pdf", dpi=300, bbox_inches='tight')
    fig2.savefig(output_dir / "adversarial_samples.png", dpi=150, bbox_inches='tight')
    plt.close(fig2)

    # Summary
    summary = {
        'timestamp': datetime.now().isoformat(),
        'model': 'ViT-Tiny AT',
        'attack': f'PGD-{steps} (eps={eps:.4f})',
        'clean_accuracy': 100*clean_correct/len(labels),
        'adv_accuracy': 100*adv_correct/len(labels),
        'attack_success': 100*(clean_correct-adv_correct)/max(clean_correct, 1),
        'feature_analysis': feature_results,
    }

    with open(output_dir / "attention_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to {output_dir}")

    # Key findings
    print("\n" + "="*60)
    print("KEY FINDINGS")
    print("="*60)

    early_layers = feature_results[:3]
    late_layers = feature_results[-3:]

    avg_early_dist = np.mean([r['l2_distance'] for r in early_layers])
    avg_late_dist = np.mean([r['l2_distance'] for r in late_layers])

    avg_early_sim = np.mean([r['cosine_similarity'] for r in early_layers])
    avg_late_sim = np.mean([r['cosine_similarity'] for r in late_layers])

    print(f"  Early Layers:")
    print(f"    Avg L2 Distance: {avg_early_dist:.4f}")
    print(f"    Avg Cosine Similarity: {avg_early_sim:.4f}")
    print(f"  Late Layers:")
    print(f"    Avg L2 Distance: {avg_late_dist:.4f}")
    print(f"    Avg Cosine Similarity: {avg_late_sim:.4f}")
    print(f"  Degradation Ratio (Late/Early): {avg_late_dist/avg_early_dist:.2f}x")


if __name__ == "__main__":
    main()
