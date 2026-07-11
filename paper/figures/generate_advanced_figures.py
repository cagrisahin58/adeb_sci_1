#!/usr/bin/env python3
"""
Advanced Figure Generation for SCI Paper

Generates:
1. Adversarial Example Showcase (3x3 grid)
2. Improved Gradient Visualization (2x2)
3. Attention Map Comparison (3x2 with difference)
4. t-SNE Feature Space Visualization

Usage:
    python paper/figures/generate_advanced_figures.py --all
    python paper/figures/generate_advanced_figures.py --figure 1
"""

import os
import sys
import json
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from pathlib import Path

# Add project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1 import make_axes_locatable

# CIFAR-10 class names
CIFAR10_CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                   'dog', 'frog', 'horse', 'ship', 'truck']

# Style settings
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1,
})


def load_models_and_data():
    """Load models and sample data."""
    from src.models import ModelRegistry
    from src.data import get_cifar10_loaders

    def create_model(name, **kwargs):
        return ModelRegistry.get(name, **kwargs)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load models
    models = {}

    # Tablolarin tanimladigi FINAL checkpoint'ler (M9: onceki surum run1
    # checkpoint'lerinden figur uretiyordu, tablolar ise run2 raporluyordu).
    # run3 varsa run3, yoksa run2 (ikisi de gercek egitim ciktisi).
    def _pick_ckpt(key):
        for c in [PROJECT_ROOT / f'models/{key}/adv/at_run3/{key}/adv/adversarial_training/best.pth',
                  PROJECT_ROOT / f'models/{key}/adv/at_run2/{key}/adv/adversarial_training/best.pth']:
            if c.exists():
                return c
        raise FileNotFoundError(f"{key} icin at_run3/at_run2 checkpoint'i yok")

    resnet_path = _pick_ckpt('resnet18')
    models['resnet18'] = create_model('resnet18', num_classes=10).to(device)
    ckpt = torch.load(resnet_path, map_location=device, weights_only=False)
    models['resnet18'].load_state_dict(ckpt['model_state_dict'])
    models['resnet18'].eval()
    print(f"Loaded ResNet18 AT from {resnet_path}")

    # ViT-Tiny AT (uses 224x224 upsampling model)
    vit_path = _pick_ckpt('vit_tiny')
    # Use vit_tiny (224x224 upsampling, 16x16 patches)
    models['vit'] = create_model('vit_tiny', num_classes=10).to(device)
    ckpt = torch.load(vit_path, map_location=device, weights_only=False)
    models['vit'].load_state_dict(ckpt['model_state_dict'])
    models['vit'].eval()
    print(f"Loaded ViT-Tiny AT from {vit_path}")

    # Load test data
    _, test_loader = get_cifar10_loaders(batch_size=128, num_workers=0)

    return models, test_loader, device


def pgd_attack(model, images, labels, eps=8/255, alpha=2/255, steps=10):
    """PGD attack."""
    images = images.clone().detach()
    adv_images = images.clone().detach()
    adv_images = adv_images + torch.empty_like(adv_images).uniform_(-eps, eps)
    adv_images = torch.clamp(adv_images, 0, 1)

    for _ in range(steps):
        adv_images.requires_grad = True
        outputs = model(adv_images)
        loss = F.cross_entropy(outputs, labels)

        grad = torch.autograd.grad(loss, adv_images)[0]
        adv_images = adv_images.detach() + alpha * grad.sign()
        delta = torch.clamp(adv_images - images, -eps, eps)
        adv_images = torch.clamp(images + delta, 0, 1).detach()

    return adv_images


def figure1_adversarial_showcase(models, test_loader, device, output_path):
    """
    GÖREV 1: Adversarial Example Showcase
    3x3 grid: [Clean | Perturbation ×10 | Adversarial]
    Row 1: Attack on ResNet
    Row 2: Attack on ViT
    Row 3: Transfer example
    """
    print("\n[GÖREV 1] Generating Adversarial Example Showcase...")

    if 'resnet18' not in models or 'vit' not in models:
        # Sentetik placeholder KALDIRILDI (M1): eksik model = yuksek sesli hata
        raise RuntimeError("Model checkpoint'leri yuklenemedi; figur uretilemez.")

    # Ornek secimi (2026-07-10 paneli MIN-9): her satir icin saldirinin
    # GERCEKTEN sinif degistirdigi ornekler secilir; onceki surum rastgele ilk
    # 3 dogru-ornegi aliyordu ve ViT satirinda saldiri basarisiz kalabiliyordu
    # (baslik 'new prediction' vaat ederken).
    images, labels = next(iter(test_loader))
    images, labels = images[:64].to(device), labels[:64].to(device)

    with torch.no_grad():
        resnet_clean_ok = models['resnet18'](images).argmax(1) == labels
        vit_clean_ok = models['vit'](images).argmax(1) == labels

    pool_adv_resnet = pgd_attack(models['resnet18'], images, labels)
    pool_adv_vit = pgd_attack(models['vit'], images, labels)

    with torch.no_grad():
        resnet_adv_flip = models['resnet18'](pool_adv_resnet).argmax(1) != labels
        vit_adv_flip = models['vit'](pool_adv_vit).argmax(1) != labels
        transfer_flip = models['vit'](pool_adv_resnet).argmax(1) != labels

    def pick(mask, exclude):
        idxs = torch.where(mask)[0]
        for k in idxs.tolist():
            if k not in exclude:
                return k
        raise RuntimeError("Uygun (saldirisi basarili) ornek bulunamadi; havuzu buyutun.")

    used = set()
    i1 = pick(resnet_clean_ok & resnet_adv_flip, used); used.add(i1)
    i2 = pick(vit_clean_ok & vit_adv_flip, used); used.add(i2)
    i3 = pick(resnet_clean_ok & vit_clean_ok & transfer_flip, used); used.add(i3)

    sample_images = torch.stack([images[i1], images[i2], images[i3]])
    sample_labels = torch.stack([labels[i1], labels[i2], labels[i3]])

    # Havuzdan, basarisi dogrulanmis adv ornekleri kullan
    adv_resnet = pool_adv_resnet[i1:i1 + 1]
    adv_vit = pool_adv_vit[i2:i2 + 1]
    adv_transfer = pool_adv_resnet[i3:i3 + 1]

    # Get predictions
    with torch.no_grad():
        # Row 1
        clean1_logits = models['resnet18'](sample_images[0:1])
        adv1_logits = models['resnet18'](adv_resnet)
        clean1_conf = F.softmax(clean1_logits, dim=1).max().item()
        adv1_conf = F.softmax(adv1_logits, dim=1).max().item()
        clean1_pred = clean1_logits.argmax(1).item()
        adv1_pred = adv1_logits.argmax(1).item()

        # Row 2
        clean2_logits = models['vit'](sample_images[1:2])
        adv2_logits = models['vit'](adv_vit)
        clean2_conf = F.softmax(clean2_logits, dim=1).max().item()
        adv2_conf = F.softmax(adv2_logits, dim=1).max().item()
        clean2_pred = clean2_logits.argmax(1).item()
        adv2_pred = adv2_logits.argmax(1).item()

        # Row 3 (transfer)
        clean3_logits = models['vit'](sample_images[2:3])
        adv3_logits = models['vit'](adv_transfer)
        clean3_conf = F.softmax(clean3_logits, dim=1).max().item()
        adv3_conf = F.softmax(adv3_logits, dim=1).max().item()
        clean3_pred = clean3_logits.argmax(1).item()
        adv3_pred = adv3_logits.argmax(1).item()

    # Create figure
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))

    def to_numpy(tensor):
        return tensor.squeeze().permute(1, 2, 0).cpu().numpy()

    def show_image(ax, img, title):
        img = np.clip(img, 0, 1)
        ax.imshow(img, interpolation='bilinear')
        ax.set_title(title, fontsize=10)
        ax.axis('off')

    # Row 1: ResNet attack
    show_image(axes[0, 0], to_numpy(sample_images[0]),
               f'Clean\n{CIFAR10_CLASSES[clean1_pred]} ({clean1_conf:.1%})')

    perturbation1 = (adv_resnet - sample_images[0:1]) * 10 + 0.5
    show_image(axes[0, 1], to_numpy(perturbation1), 'Perturbation (×10)')

    show_image(axes[0, 2], to_numpy(adv_resnet),
               f'Adversarial\n{CIFAR10_CLASSES[adv1_pred]} ({adv1_conf:.1%})')

    # Row 2: ViT attack
    show_image(axes[1, 0], to_numpy(sample_images[1]),
               f'Clean\n{CIFAR10_CLASSES[clean2_pred]} ({clean2_conf:.1%})')

    perturbation2 = (adv_vit - sample_images[1:2]) * 10 + 0.5
    show_image(axes[1, 1], to_numpy(perturbation2), 'Perturbation (×10)')

    show_image(axes[1, 2], to_numpy(adv_vit),
               f'Adversarial\n{CIFAR10_CLASSES[adv2_pred]} ({adv2_conf:.1%})')

    # Row 3: Transfer attack
    show_image(axes[2, 0], to_numpy(sample_images[2]),
               f'Clean\n{CIFAR10_CLASSES[clean3_pred]} ({clean3_conf:.1%})')

    perturbation3 = (adv_transfer - sample_images[2:3]) * 10 + 0.5
    show_image(axes[2, 1], to_numpy(perturbation3), 'Perturbation (×10)\n(from ResNet)')

    show_image(axes[2, 2], to_numpy(adv_transfer),
               f'Transfer to ViT\n{CIFAR10_CLASSES[adv3_pred]} ({adv3_conf:.1%})')

    # Row labels
    fig.text(0.02, 0.78, 'ResNet-18\nAttack', fontsize=11, fontweight='bold',
             rotation=90, va='center')
    fig.text(0.02, 0.5, 'ViT-Tiny\nAttack', fontsize=11, fontweight='bold',
             rotation=90, va='center')
    fig.text(0.02, 0.22, 'Transfer\n(CNN→ViT)', fontsize=11, fontweight='bold',
             rotation=90, va='center')

    plt.tight_layout(rect=[0.05, 0, 1, 0.96])
    fig.suptitle('Adversarial Examples: PGD Attack ($\\epsilon=8/255$)', fontsize=14)

    plt.savefig(output_path)
    plt.close()
    print(f"  Saved: {output_path}")


def figure2_gradient_comparison(models, test_loader, device, output_path):
    """
    GÖREV 2: Improved Gradient Visualization
    2x2 grid with colorbars
    """
    print("\n[GÖREV 2] Generating Gradient Comparison...")

    if 'resnet18' not in models or 'vit' not in models:
        # Sentetik fallback KALDIRILDI (M1)
        raise RuntimeError("Model checkpoint'leri yuklenemedi; gradient figuru uretilemez.")

    # Get sample
    images, labels = next(iter(test_loader))
    images, labels = images[:4].to(device), labels[:4].to(device)

    # Compute gradients for both models
    def get_gradients(model, images, labels):
        images = images.clone().detach().requires_grad_(True)
        model.zero_grad()
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)
        grads = torch.autograd.grad(loss, images, create_graph=False)[0]
        return grads.abs()

    resnet_grads = get_gradients(models['resnet18'], images.clone(), labels)
    vit_grads = get_gradients(models['vit'], images.clone(), labels)

    # Iki mimari AYNI goruntuler uzerinde karsilastirilir (2026-07-10 paneli
    # MAJ-7: onceki surum CNN'i 'cat', ViT'i 'ship' uzerinde gosteriyordu ve
    # 'direct comparison' basligiyla celisiyordu). Satirlar: goruntu A ve B;
    # sutunlar: orijinal | ResNet-18 gradyani | ViT-Tiny gradyani.
    fig = plt.figure(figsize=(15, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.25, wspace=0.3)

    for row, idx in enumerate([0, 1]):
        img = images[idx].permute(1, 2, 0).detach().cpu().numpy()
        ax_img = fig.add_subplot(gs[row, 0])
        ax_img.imshow(np.clip(img, 0, 1), interpolation='bilinear')
        ax_img.set_title(f'Original Image\n(Class: {CIFAR10_CLASSES[labels[idx].item()]})', fontsize=12)
        ax_img.axis('off')

        cnn_grad = resnet_grads[idx].max(0)[0].detach().cpu().numpy()
        ax_cnn = fig.add_subplot(gs[row, 1])
        im_c = ax_cnn.imshow(cnn_grad, cmap='hot', vmin=0, vmax=cnn_grad.max(), interpolation='bilinear')
        ax_cnn.set_title('ResNet-18 Gradient\n(more concentrated)', fontsize=12)
        ax_cnn.axis('off')
        divider = make_axes_locatable(ax_cnn)
        plt.colorbar(im_c, cax=divider.append_axes("right", size="5%", pad=0.05))

        vit_grad = vit_grads[idx].max(0)[0].detach().cpu().numpy()
        ax_vit = fig.add_subplot(gs[row, 2])
        im_v = ax_vit.imshow(vit_grad, cmap='hot', vmin=0, vmax=vit_grad.max(), interpolation='bilinear')
        ax_vit.set_title('ViT-Tiny Gradient\n(more distributed)', fontsize=12)
        ax_vit.axis('off')
        divider = make_axes_locatable(ax_vit)
        plt.colorbar(im_v, cax=divider.append_axes("right", size="5%", pad=0.05))

    # Anotasyon: OLCEK-BAGIMSIZ Hoyer sparsity (2026-07-10 paneli MAJ-7:
    # onceki esik-tabanli metrik makalenin kendisinin reddettigi metrikti)
    grad_summary_candidates = [
        PROJECT_ROOT / 'results/gradient_analysis_run3/gradient_summary.json',
        PROJECT_ROOT / 'results/gradient_analysis_run2/gradient_summary.json',
    ]
    grad_summary_path = next((p for p in grad_summary_candidates if p.exists()), None)
    if grad_summary_path is None:
        raise FileNotFoundError(
            "gradient_summary.json bulunamadi; once gradient analizini calistirin")
    with open(grad_summary_path) as f:
        grad_stats = json.load(f)['statistics']
    cnn_hoyer = grad_stats['ResNet18_AT']['sparsity_hoyer']
    vit_hoyer = grad_stats['ViT_Tiny_AT']['sparsity_hoyer']
    print(f"  Hoyer annotations from {grad_summary_path.name}: "
          f"CNN={cnn_hoyer:.3f}, ViT={vit_hoyer:.3f}")

    fig.text(0.5, 0.02,
             f'Hoyer sparsity (scale-invariant): ResNet-18 {cnn_hoyer:.3f} | ViT-Tiny {vit_hoyer:.3f}',
             ha='center', fontsize=11, style='italic')

    plt.savefig(output_path)
    plt.close()
    print(f"  Saved: {output_path}")


def figure3_attention_comparison(models, test_loader, device, output_path):
    """
    GÖREV 3: Attention Map Comparison
    3 rows (Layer 1, 6, 12) x 3 cols (Clean, Adversarial, Difference)
    """
    print("\n[GÖREV 3] Generating Attention Comparison...")

    if 'vit' not in models:
        # Sentetik fallback KALDIRILDI (M9c)
        raise RuntimeError("ViT model yuklenemedi; attention figuru uretilemez.")

    vit = models['vit']

    # Get sample
    images, labels = next(iter(test_loader))
    images, labels = images[:1].to(device), labels[:1].to(device)

    # Generate adversarial
    adv_images = pgd_attack(vit, images, labels)

    # Gercek post-softmax attention (M1: torch.rand fallback kaldirildi;
    # src/models/vit.py get_attention_maps dict dondurur)
    if not hasattr(vit, 'get_attention_maps'):
        raise AttributeError(
            "vit_tiny modelinde get_attention_maps yok; src/models/vit.py "
            "guncel degil (M1 attention-extraction edit'i gerekli).")
    clean_attn = vit.get_attention_maps(images)['attention']
    adv_attn = vit.get_attention_maps(adv_images)['attention']

    # Select layers 0, 5, 11 (1, 6, 12 in 1-indexed)
    layer_indices = [0, 5, 11]
    layer_names = ['Layer 1', 'Layer 6', 'Layer 12']

    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    for row, (layer_idx, layer_name) in enumerate(zip(layer_indices, layer_names)):
        # Get attention for CLS token, average over heads
        if layer_idx >= len(clean_attn):
            raise IndexError(f"Layer {layer_idx} yok (toplam {len(clean_attn)} katman)")
        clean_att = clean_attn[layer_idx][0, :, 0, 1:].mean(0).detach().cpu().numpy()
        adv_att = adv_attn[layer_idx][0, :, 0, 1:].mean(0).detach().cpu().numpy()

        # Reshape to grid
        grid_size = int(np.sqrt(len(clean_att)))
        clean_att = clean_att[:grid_size**2].reshape(grid_size, grid_size)
        adv_att = adv_att[:grid_size**2].reshape(grid_size, grid_size)
        diff_att = adv_att - clean_att

        # Clean attention
        im1 = axes[row, 0].imshow(clean_att, cmap='viridis', vmin=0, vmax=clean_att.max(), interpolation='bilinear')
        axes[row, 0].set_title(f'{layer_name}\nClean', fontsize=11)
        axes[row, 0].axis('off')

        # Adversarial attention
        im2 = axes[row, 1].imshow(adv_att, cmap='viridis', vmin=0, vmax=adv_att.max(), interpolation='bilinear')
        axes[row, 1].set_title(f'{layer_name}\nAdversarial', fontsize=11)
        axes[row, 1].axis('off')

        # Difference
        max_diff = max(abs(diff_att.min()), abs(diff_att.max()))
        im3 = axes[row, 2].imshow(diff_att, cmap='RdBu_r', vmin=-max_diff, vmax=max_diff, interpolation='bilinear')
        axes[row, 2].set_title(f'{layer_name}\nDifference', fontsize=11)
        axes[row, 2].axis('off')

        # Add colorbar to difference
        divider = make_axes_locatable(axes[row, 2])
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im3, cax=cax)

    fig.suptitle('Attention Map Degradation Under Adversarial Attack', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    plt.savefig(output_path)
    plt.close()
    print(f"  Saved: {output_path}")


def figure4_tsne_features(models, test_loader, device, output_path):
    """
    GÖREV 4: t-SNE Feature Space Visualization
    2 panels: CNN and ViT
    Clean (circles) vs Adversarial (triangles)
    """
    print("\n[GÖREV 4] Generating t-SNE Feature Space...")

    # Sentetik fallback'ler KALDIRILDI (M1): eksik bagimlilik/model = hata
    from sklearn.manifold import TSNE

    if 'resnet18' not in models or 'vit' not in models:
        raise RuntimeError("Model checkpoint'leri yuklenemedi; t-SNE figuru uretilemez.")

    # Collect features
    n_samples = 500  # Reduced for speed
    all_images = []
    all_labels = []

    for images, labels in test_loader:
        all_images.append(images)
        all_labels.append(labels)
        if sum(x.shape[0] for x in all_images) >= n_samples:
            break

    images = torch.cat(all_images)[:n_samples].to(device)
    labels = torch.cat(all_labels)[:n_samples].to(device)

    print(f"  Collecting features from {n_samples} samples...")

    # Generate adversarial examples
    adv_images = pgd_attack(models['resnet18'], images, labels)

    # Get features
    def get_features(model, images):
        with torch.no_grad():
            if hasattr(model, 'get_features'):
                return model.get_features(images)
            elif hasattr(model, 'model'):
                # Try to get penultimate layer
                if hasattr(model.model, 'forward_features'):
                    return model.model.forward_features(images)
            # Fallback: use output logits
            return model(images)

    # ResNet features (flatten if needed)
    resnet_clean_feat = get_features(models['resnet18'], images).cpu().numpy()
    resnet_adv_feat = get_features(models['resnet18'], adv_images).cpu().numpy()
    if resnet_clean_feat.ndim > 2:
        resnet_clean_feat = resnet_clean_feat.reshape(resnet_clean_feat.shape[0], -1)
        resnet_adv_feat = resnet_adv_feat.reshape(resnet_adv_feat.shape[0], -1)

    # ViT features (flatten if needed)
    vit_clean_feat = get_features(models['vit'], images).cpu().numpy()
    vit_adv_feat = get_features(models['vit'], adv_images).cpu().numpy()
    if vit_clean_feat.ndim > 2:
        vit_clean_feat = vit_clean_feat.reshape(vit_clean_feat.shape[0], -1)
        vit_adv_feat = vit_adv_feat.reshape(vit_adv_feat.shape[0], -1)

    labels_np = labels.cpu().numpy()

    print("  Running t-SNE (this may take a moment)...")

    # Ensure 2D for t-SNE (flatten any remaining dimensions)
    def ensure_2d(arr):
        if arr.ndim > 2:
            return arr.reshape(arr.shape[0], -1)
        elif arr.ndim == 1:
            return arr.reshape(-1, 1)
        return arr

    resnet_clean_feat = ensure_2d(resnet_clean_feat)
    resnet_adv_feat = ensure_2d(resnet_adv_feat)
    vit_clean_feat = ensure_2d(vit_clean_feat)
    vit_adv_feat = ensure_2d(vit_adv_feat)

    # t-SNE for ResNet
    resnet_all_feat = np.vstack([resnet_clean_feat, resnet_adv_feat])
    tsne_resnet = TSNE(n_components=2, perplexity=30, random_state=42)
    resnet_embedded = tsne_resnet.fit_transform(resnet_all_feat)
    resnet_clean_emb = resnet_embedded[:n_samples]
    resnet_adv_emb = resnet_embedded[n_samples:]

    # t-SNE for ViT
    vit_all_feat = np.vstack([vit_clean_feat, vit_adv_feat])
    tsne_vit = TSNE(n_components=2, perplexity=30, random_state=42)
    vit_embedded = tsne_vit.fit_transform(vit_all_feat)
    vit_clean_emb = vit_embedded[:n_samples]
    vit_adv_emb = vit_embedded[n_samples:]

    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    # ResNet plot
    for c in range(10):
        mask = labels_np == c
        axes[0].scatter(resnet_clean_emb[mask, 0], resnet_clean_emb[mask, 1],
                       c=[colors[c]], marker='o', s=20, alpha=0.6, label=f'{CIFAR10_CLASSES[c]}' if c < 5 else '')
        axes[0].scatter(resnet_adv_emb[mask, 0], resnet_adv_emb[mask, 1],
                       c=[colors[c]], marker='^', s=20, alpha=0.4)

    axes[0].set_title('ResNet-18 Feature Space', fontsize=12)
    axes[0].set_xlabel('t-SNE 1')
    axes[0].set_ylabel('t-SNE 2')

    # ViT plot
    for c in range(10):
        mask = labels_np == c
        axes[1].scatter(vit_clean_emb[mask, 0], vit_clean_emb[mask, 1],
                       c=[colors[c]], marker='o', s=20, alpha=0.6)
        axes[1].scatter(vit_adv_emb[mask, 0], vit_adv_emb[mask, 1],
                       c=[colors[c]], marker='^', s=20, alpha=0.4)

    axes[1].set_title('ViT-Tiny Feature Space', fontsize=12)
    axes[1].set_xlabel('t-SNE 1')
    axes[1].set_ylabel('t-SNE 2')

    # Legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=8, label='Clean'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', markersize=8, label='Adversarial'),
    ]
    fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.99, 0.99))

    fig.suptitle('Feature Space Perturbation: Clean vs Adversarial Samples', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.savefig(output_path)
    plt.close()
    print(f"  Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate advanced figures')
    parser.add_argument('--all', action='store_true', help='Generate all figures')
    parser.add_argument('--figure', type=int, choices=[1, 2, 3, 4], help='Generate specific figure')
    parser.add_argument('--output-dir', type=str, default='paper/figures/raw')
    args = parser.parse_args()

    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Generating Advanced Figures for SCI Paper")
    print("=" * 60)

    # Load models and data
    models, test_loader, device = load_models_and_data()

    if args.all or args.figure is None:
        figure1_adversarial_showcase(models, test_loader, device,
                                     output_dir / 'fig_adversarial_examples.pdf')
        figure2_gradient_comparison(models, test_loader, device,
                                   output_dir / 'fig4_gradient_comparison.pdf')
        figure3_attention_comparison(models, test_loader, device,
                                    output_dir / 'fig5_attention_comparison.pdf')
        figure4_tsne_features(models, test_loader, device,
                             output_dir / 'fig_tsne_features.pdf')
    else:
        generators = {
            1: lambda: figure1_adversarial_showcase(models, test_loader, device,
                                                    output_dir / 'fig_adversarial_examples.pdf'),
            2: lambda: figure2_gradient_comparison(models, test_loader, device,
                                                  output_dir / 'fig4_gradient_comparison.pdf'),
            3: lambda: figure3_attention_comparison(models, test_loader, device,
                                                   output_dir / 'fig5_attention_comparison.pdf'),
            4: lambda: figure4_tsne_features(models, test_loader, device,
                                            output_dir / 'fig_tsne_features.pdf'),
        }
        generators[args.figure]()

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == '__main__':
    main()
