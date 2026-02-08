#!/usr/bin/env python3
"""
Publication-Quality Figure Generation for SCI Q1 Paper
CNN vs ViT Adversarial Robustness Comparison

Style Guidelines:
- Clean, minimal design following Nature/IEEE standards
- Colorblind-friendly palette
- Consistent typography (serif for labels)
- 300 DPI minimum, vector PDF output
- Single column: 3.5 inches, Double column: 7 inches
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# =============================================================================
# PUBLICATION STYLE CONFIGURATION
# =============================================================================

def setup_publication_style():
    """Configure matplotlib for publication-quality figures."""

    # Use a clean style base
    plt.style.use('seaborn-v0_8-whitegrid')

    # Custom settings for IEEE/Nature style
    mpl.rcParams.update({
        # Figure
        'figure.facecolor': 'white',
        'figure.edgecolor': 'white',
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.format': 'pdf',
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.05,

        # Font - use serif for professional look
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
        'font.size': 9,
        'axes.titlesize': 10,
        'axes.labelsize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,

        # Axes
        'axes.linewidth': 0.8,
        'axes.edgecolor': '#333333',
        'axes.labelcolor': '#333333',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linewidth': 0.5,

        # Ticks
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'xtick.color': '#333333',
        'ytick.color': '#333333',

        # Legend
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'legend.edgecolor': '#cccccc',

        # Lines
        'lines.linewidth': 1.5,
        'lines.markersize': 6,
    })

# Colorblind-friendly palette (IBM Design)
COLORS = {
    'blue': '#648FFF',
    'purple': '#785EF0',
    'magenta': '#DC267F',
    'orange': '#FE6100',
    'yellow': '#FFB000',
    'gray': '#666666',
}

# Model-specific colors
MODEL_COLORS = {
    'ResNet-18': COLORS['blue'],
    'WRN-28-10': COLORS['purple'],
    'ViT-Tiny': COLORS['orange'],
    'ViT-Small': COLORS['magenta'],
}

# Figure dimensions (inches) - IEEE single column = 3.5", double = 7"
FIG_SINGLE = (3.5, 2.8)
FIG_DOUBLE = (7.0, 3.0)
FIG_SQUARE = (3.5, 3.5)


# =============================================================================
# FIGURE 1: MAIN ROBUSTNESS COMPARISON (Bar Chart)
# =============================================================================

def figure1_robustness_comparison(results: dict, output_path: str):
    """
    Main robustness comparison bar chart.

    Args:
        results: Dict with structure {model_name: {'clean': X, 'fgsm': X, 'pgd': X, 'aa': X}}
        output_path: Path to save the figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=FIG_DOUBLE)

    models = list(results.keys())
    metrics = ['Clean', 'FGSM', 'PGD-20', 'AutoAttack']
    x = np.arange(len(models))
    width = 0.2

    # Color scheme for metrics
    metric_colors = [COLORS['blue'], COLORS['yellow'], COLORS['orange'], COLORS['magenta']]

    for i, (metric, color) in enumerate(zip(metrics, metric_colors)):
        metric_key = metric.lower().replace('-', '').replace('autoattack', 'aa')
        values = [results[m].get(metric_key, 0) for m in models]
        bars = ax.bar(x + i * width, values, width, label=metric, color=color, edgecolor='white', linewidth=0.5)

        # Add value labels on bars
        for bar, val in zip(bars, values):
            if val > 0:
                ax.annotate(f'{val:.1f}',
                           xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                           xytext=(0, 2), textcoords='offset points',
                           ha='center', va='bottom', fontsize=6, color='#333333')

    ax.set_ylabel('Accuracy (%)')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=15, ha='right')
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', ncol=2)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# FIGURE 2: EPSILON SWEEP (Line Plot)
# =============================================================================

def figure2_epsilon_sweep(results: dict, output_path: str):
    """
    Epsilon sensitivity analysis line plot.

    Args:
        results: Dict {model_name: {epsilon: accuracy}}
        output_path: Path to save the figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    # Standard epsilon values
    epsilons = [0, 2/255, 4/255, 8/255, 16/255]
    eps_labels = ['0', '2/255', '4/255', '8/255', '16/255']

    markers = ['o', 's', '^', 'D']
    linestyles = ['-', '-', '--', '--']  # Solid for CNN, dashed for ViT

    for i, (model, data) in enumerate(results.items()):
        color = list(MODEL_COLORS.values())[i % len(MODEL_COLORS)]
        marker = markers[i % len(markers)]
        ls = linestyles[i % len(linestyles)]

        accuracies = [data.get(eps, 0) for eps in epsilons]
        ax.plot(range(len(epsilons)), accuracies,
                marker=marker, linestyle=ls, color=color,
                label=model, markerfacecolor='white', markeredgewidth=1.5)

    ax.set_xlabel(r'Perturbation Budget ($\epsilon$)')
    ax.set_ylabel('Accuracy (%)')
    ax.set_xticks(range(len(epsilons)))
    ax.set_xticklabels(eps_labels)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', framealpha=0.95)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# FIGURE 3: TRANSFER ATTACK HEATMAP
# =============================================================================

def figure3_transfer_heatmap(transfer_matrix: np.ndarray, model_names: list, output_path: str):
    """
    Transfer attack success rate heatmap.

    Args:
        transfer_matrix: NxN matrix of transfer success rates
        model_names: List of model names
        output_path: Path to save the figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=FIG_SQUARE)

    # Custom colormap: white (low) to dark red (high)
    cmap = plt.cm.Reds

    im = ax.imshow(transfer_matrix, cmap=cmap, vmin=0, vmax=100, aspect='equal')

    # Add colorbar
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Transfer Success Rate (%)', rotation=270, labelpad=15)

    # Set ticks
    ax.set_xticks(np.arange(len(model_names)))
    ax.set_yticks(np.arange(len(model_names)))
    ax.set_xticklabels(model_names, rotation=45, ha='right')
    ax.set_yticklabels(model_names)

    ax.set_xlabel('Target Model')
    ax.set_ylabel('Source Model')

    # Add text annotations
    for i in range(len(model_names)):
        for j in range(len(model_names)):
            value = transfer_matrix[i, j]
            text_color = 'white' if value > 50 else 'black'
            ax.text(j, i, f'{value:.1f}', ha='center', va='center',
                   color=text_color, fontsize=8, fontweight='bold')

    # Add grid lines
    ax.set_xticks(np.arange(-.5, len(model_names), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(model_names), 1), minor=True)
    ax.grid(which='minor', color='white', linestyle='-', linewidth=2)
    ax.tick_params(which='minor', size=0)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# FIGURE 4: GRADIENT VISUALIZATION
# =============================================================================

def figure4_gradient_analysis(
    images: np.ndarray,
    cnn_grads: np.ndarray,
    vit_grads: np.ndarray,
    perturbations: np.ndarray,
    output_path: str
):
    """
    Gradient visualization comparing CNN and ViT.

    Args:
        images: Original images (N, H, W, C)
        cnn_grads: CNN gradient magnitudes (N, H, W)
        vit_grads: ViT gradient magnitudes (N, H, W)
        perturbations: Adversarial perturbations (N, H, W, C)
        output_path: Path to save the figure
    """
    setup_publication_style()

    n_samples = min(3, len(images))
    fig, axes = plt.subplots(n_samples, 4, figsize=(7, n_samples * 1.8))

    if n_samples == 1:
        axes = axes.reshape(1, -1)

    col_titles = ['Original', 'Perturbation (×10)', 'CNN Gradient', 'ViT Gradient']

    for i in range(n_samples):
        # Original image
        axes[i, 0].imshow(images[i])
        axes[i, 0].axis('off')

        # Perturbation (magnified for visibility)
        pert = perturbations[i] * 10 + 0.5  # Scale and shift for visibility
        pert = np.clip(pert, 0, 1)
        axes[i, 1].imshow(pert)
        axes[i, 1].axis('off')

        # CNN gradient
        im_cnn = axes[i, 2].imshow(cnn_grads[i], cmap='hot', vmin=0)
        axes[i, 2].axis('off')

        # ViT gradient
        im_vit = axes[i, 3].imshow(vit_grads[i], cmap='hot', vmin=0)
        axes[i, 3].axis('off')

    # Column titles
    for j, title in enumerate(col_titles):
        axes[0, j].set_title(title, fontsize=9, pad=5)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def figure4b_gradient_distribution(cnn_norms: np.ndarray, vit_norms: np.ndarray, output_path: str):
    """
    Gradient norm distribution comparison.

    Args:
        cnn_norms: Array of CNN gradient norms
        vit_norms: Array of ViT gradient norms
        output_path: Path to save the figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    # KDE plots
    from scipy import stats

    x_range = np.linspace(0, max(cnn_norms.max(), vit_norms.max()) * 1.1, 200)

    cnn_kde = stats.gaussian_kde(cnn_norms)
    vit_kde = stats.gaussian_kde(vit_norms)

    ax.fill_between(x_range, cnn_kde(x_range), alpha=0.3, color=COLORS['blue'], label='CNN')
    ax.plot(x_range, cnn_kde(x_range), color=COLORS['blue'], linewidth=2)

    ax.fill_between(x_range, vit_kde(x_range), alpha=0.3, color=COLORS['orange'], label='ViT')
    ax.plot(x_range, vit_kde(x_range), color=COLORS['orange'], linewidth=2)

    # Add mean lines
    ax.axvline(cnn_norms.mean(), color=COLORS['blue'], linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(vit_norms.mean(), color=COLORS['orange'], linestyle='--', linewidth=1, alpha=0.7)

    ax.set_xlabel('Gradient Norm')
    ax.set_ylabel('Density')
    ax.legend(loc='upper right')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# FIGURE 5: ATTENTION ANALYSIS
# =============================================================================

def figure5_attention_degradation(
    clean_attention: dict,
    adv_attention: dict,
    sample_image: np.ndarray,
    output_path: str
):
    """
    Attention pattern comparison between clean and adversarial inputs.

    Args:
        clean_attention: Dict {layer_idx: attention_map}
        adv_attention: Dict {layer_idx: attention_map}
        sample_image: Sample image for overlay
        output_path: Path to save the figure
    """
    setup_publication_style()

    layers_to_show = [0, 5, 11]  # Early, middle, late
    layer_names = ['Layer 1', 'Layer 6', 'Layer 12']

    fig, axes = plt.subplots(2, 3, figsize=(7, 4.5))

    for j, (layer_idx, layer_name) in enumerate(zip(layers_to_show, layer_names)):
        # Clean attention
        clean_attn = clean_attention.get(layer_idx, np.zeros((8, 8)))
        axes[0, j].imshow(sample_image)
        im = axes[0, j].imshow(clean_attn, cmap='jet', alpha=0.5,
                               extent=[0, sample_image.shape[1], sample_image.shape[0], 0])
        axes[0, j].axis('off')
        axes[0, j].set_title(layer_name, fontsize=9)

        # Adversarial attention
        adv_attn = adv_attention.get(layer_idx, np.zeros((8, 8)))
        axes[1, j].imshow(sample_image)
        axes[1, j].imshow(adv_attn, cmap='jet', alpha=0.5,
                         extent=[0, sample_image.shape[1], sample_image.shape[0], 0])
        axes[1, j].axis('off')

    # Row labels
    axes[0, 0].set_ylabel('Clean', fontsize=9, rotation=0, ha='right', va='center')
    axes[1, 0].set_ylabel('Adversarial', fontsize=9, rotation=0, ha='right', va='center')

    # Colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Attention Weight', rotation=270, labelpad=15)

    plt.tight_layout(rect=[0, 0, 0.9, 1])
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


def figure5b_attention_entropy(entropy_data: dict, output_path: str):
    """
    Layer-wise attention entropy comparison.

    Args:
        entropy_data: Dict {'clean': [layer_entropies], 'adversarial': [layer_entropies]}
        output_path: Path to save the figure
    """
    setup_publication_style()

    fig, ax = plt.subplots(figsize=FIG_SINGLE)

    layers = range(1, len(entropy_data['clean']) + 1)

    ax.plot(layers, entropy_data['clean'], 'o-', color=COLORS['blue'],
            label='Clean', markerfacecolor='white', markeredgewidth=1.5)
    ax.plot(layers, entropy_data['adversarial'], 's--', color=COLORS['magenta'],
            label='Adversarial', markerfacecolor='white', markeredgewidth=1.5)

    ax.set_xlabel('Layer')
    ax.set_ylabel('Attention Entropy')
    ax.set_xticks(layers)
    ax.legend(loc='upper right')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# =============================================================================
# DEMO DATA GENERATION (for testing without real results)
# =============================================================================

def generate_demo_data():
    """Generate demo data for testing figure generation."""

    # Figure 1: Robustness comparison
    robustness_results = {
        'ResNet-18\n(Clean)': {'clean': 94.4, 'fgsm': 12.3, 'pgd20': 0.0, 'aa': 0.0},
        'ResNet-18\n(AT)': {'clean': 80.3, 'fgsm': 55.2, 'pgd20': 40.3, 'aa': 38.1},
        'WRN-28-10': {'clean': 89.5, 'fgsm': 71.2, 'pgd20': 66.1, 'aa': 62.8},
        'ViT-Tiny\n(AT)': {'clean': 65.0, 'fgsm': 42.1, 'pgd20': 32.5, 'aa': 30.2},
    }

    # Figure 2: Epsilon sweep
    epsilon_results = {
        'ResNet-18 (AT)': {0: 80.3, 2/255: 62.1, 4/255: 51.2, 8/255: 40.3, 16/255: 25.1},
        'WRN-28-10': {0: 89.5, 2/255: 78.3, 4/255: 72.1, 8/255: 66.1, 16/255: 52.3},
        'ViT-Tiny (AT)': {0: 65.0, 2/255: 48.2, 4/255: 40.1, 8/255: 32.5, 16/255: 20.8},
    }

    # Figure 3: Transfer matrix
    model_names = ['ResNet-18', 'WRN-28-10', 'ViT-Tiny', 'ViT-Small']
    transfer_matrix = np.array([
        [100.0, 45.2, 28.3, 25.1],
        [52.1, 100.0, 32.5, 30.2],
        [18.5, 15.2, 100.0, 78.3],
        [20.1, 17.8, 82.1, 100.0],
    ])

    # Figure 4: Gradient data (random for demo)
    np.random.seed(42)
    n_samples = 3
    images = np.random.rand(n_samples, 32, 32, 3)
    cnn_grads = np.random.rand(n_samples, 32, 32) * 0.5
    vit_grads = np.random.rand(n_samples, 32, 32) * 0.3
    perturbations = (np.random.rand(n_samples, 32, 32, 3) - 0.5) * 0.1

    cnn_norms = np.random.exponential(0.5, 1000)
    vit_norms = np.random.exponential(0.3, 1000)

    # Figure 5: Attention data
    clean_attention = {0: np.random.rand(8, 8), 5: np.random.rand(8, 8), 11: np.random.rand(8, 8)}
    adv_attention = {0: np.random.rand(8, 8), 5: np.random.rand(8, 8), 11: np.random.rand(8, 8)}
    sample_image = np.random.rand(32, 32, 3)

    entropy_data = {
        'clean': np.linspace(2.5, 1.8, 12) + np.random.rand(12) * 0.1,
        'adversarial': np.linspace(3.2, 2.5, 12) + np.random.rand(12) * 0.15,
    }

    return {
        'robustness': robustness_results,
        'epsilon': epsilon_results,
        'transfer': (transfer_matrix, model_names),
        'gradient': (images, cnn_grads, vit_grads, perturbations, cnn_norms, vit_norms),
        'attention': (clean_attention, adv_attention, sample_image, entropy_data),
    }


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate all figures with demo data."""

    output_dir = Path(__file__).parent / 'raw'
    output_dir.mkdir(exist_ok=True)

    print("Generating publication figures...")
    print("=" * 50)

    # Generate demo data
    demo = generate_demo_data()

    # Figure 1
    print("\n[1/5] Robustness Comparison")
    figure1_robustness_comparison(
        demo['robustness'],
        str(output_dir / 'fig1_robustness_comparison.pdf')
    )

    # Figure 2
    print("\n[2/5] Epsilon Sweep")
    figure2_epsilon_sweep(
        demo['epsilon'],
        str(output_dir / 'fig2_epsilon_sweep.pdf')
    )

    # Figure 3
    print("\n[3/5] Transfer Attack Heatmap")
    transfer_matrix, model_names = demo['transfer']
    figure3_transfer_heatmap(
        transfer_matrix,
        model_names,
        str(output_dir / 'fig3_transfer_heatmap.pdf')
    )

    # Figure 4
    print("\n[4/5] Gradient Analysis")
    images, cnn_grads, vit_grads, perts, cnn_norms, vit_norms = demo['gradient']
    figure4_gradient_analysis(
        images, cnn_grads, vit_grads, perts,
        str(output_dir / 'fig4a_gradient_visualization.pdf')
    )
    figure4b_gradient_distribution(
        cnn_norms, vit_norms,
        str(output_dir / 'fig4b_gradient_distribution.pdf')
    )

    # Figure 5
    print("\n[5/5] Attention Analysis")
    clean_attn, adv_attn, sample_img, entropy = demo['attention']
    figure5_attention_degradation(
        clean_attn, adv_attn, sample_img,
        str(output_dir / 'fig5a_attention_comparison.pdf')
    )
    figure5b_attention_entropy(
        entropy,
        str(output_dir / 'fig5b_attention_entropy.pdf')
    )

    print("\n" + "=" * 50)
    print(f"All figures saved to: {output_dir}")
    print("\nNote: These are demo figures. Run with real data for publication.")


if __name__ == '__main__':
    main()
