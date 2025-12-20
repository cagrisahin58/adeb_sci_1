"""Visualization utilities for adversarial analysis."""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from typing import Optional, Dict, List, Tuple, Union
from pathlib import Path
import seaborn as sns


class AdversarialVisualizer:
    """
    Comprehensive visualization tools for adversarial robustness analysis.

    Generates publication-quality figures for:
    - Perturbation analysis
    - Transfer attack matrices
    - Attention pattern comparison
    - Gradient landscapes
    """

    def __init__(
        self,
        figsize: Tuple[int, int] = (12, 8),
        dpi: int = 150,
        style: str = "seaborn-v0_8-whitegrid",
    ):
        """
        Initialize visualizer.

        Args:
            figsize: Default figure size
            dpi: Figure resolution
            style: Matplotlib style
        """
        self.figsize = figsize
        self.dpi = dpi
        try:
            plt.style.use(style)
        except OSError:
            plt.style.use("seaborn-whitegrid")

        # Color palette for consistent styling
        self.colors = {
            "cnn": "#2ecc71",      # Green for CNNs
            "vit": "#3498db",      # Blue for ViTs
            "clean": "#27ae60",    # Green for clean
            "adv": "#e74c3c",      # Red for adversarial
            "resnet": "#2ecc71",
            "densenet": "#27ae60",
            "vit_tiny": "#3498db",
            "vit_small": "#2980b9",
        }

    def plot_perturbation_samples(
        self,
        clean_images: torch.Tensor,
        adv_images: torch.Tensor,
        labels: torch.Tensor,
        predictions_clean: torch.Tensor,
        predictions_adv: torch.Tensor,
        class_names: Optional[List[str]] = None,
        num_samples: int = 5,
        amplify_perturbation: float = 10.0,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Visualize clean images, perturbations, and adversarial images.

        Args:
            clean_images: Original images (B, C, H, W)
            adv_images: Adversarial images
            labels: True labels
            predictions_clean: Model predictions on clean
            predictions_adv: Model predictions on adversarial
            class_names: Optional class name mapping
            num_samples: Number of samples to show
            amplify_perturbation: Factor to amplify perturbation visibility
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        # Select samples where attack succeeded
        misclassified = predictions_adv != labels
        if misclassified.sum() > 0:
            indices = torch.where(misclassified)[0][:num_samples]
        else:
            indices = torch.arange(min(num_samples, len(clean_images)))

        n = len(indices)
        fig, axes = plt.subplots(n, 4, figsize=(16, 4 * n))

        if n == 1:
            axes = axes.reshape(1, -1)

        for i, idx in enumerate(indices):
            # Clean image
            clean_img = clean_images[idx].cpu().permute(1, 2, 0).numpy()
            clean_img = np.clip(clean_img, 0, 1)

            # Adversarial image
            adv_img = adv_images[idx].cpu().permute(1, 2, 0).numpy()
            adv_img = np.clip(adv_img, 0, 1)

            # Perturbation
            perturbation = adv_img - clean_img
            pert_display = np.clip(perturbation * amplify_perturbation + 0.5, 0, 1)

            # Perturbation magnitude
            pert_magnitude = np.abs(perturbation).mean(axis=2)

            # Labels
            true_label = labels[idx].item()
            pred_clean = predictions_clean[idx].item()
            pred_adv = predictions_adv[idx].item()

            if class_names:
                true_name = class_names[true_label]
                pred_clean_name = class_names[pred_clean]
                pred_adv_name = class_names[pred_adv]
            else:
                true_name = str(true_label)
                pred_clean_name = str(pred_clean)
                pred_adv_name = str(pred_adv)

            # Plot
            axes[i, 0].imshow(clean_img)
            axes[i, 0].set_title(f"Clean\nTrue: {true_name}\nPred: {pred_clean_name}")
            axes[i, 0].axis("off")

            axes[i, 1].imshow(pert_display)
            axes[i, 1].set_title(f"Perturbation (×{amplify_perturbation})")
            axes[i, 1].axis("off")

            im = axes[i, 2].imshow(pert_magnitude, cmap="hot")
            axes[i, 2].set_title("Perturbation Magnitude")
            axes[i, 2].axis("off")
            plt.colorbar(im, ax=axes[i, 2], fraction=0.046)

            axes[i, 3].imshow(adv_img)
            color = "red" if pred_adv != true_label else "green"
            axes[i, 3].set_title(f"Adversarial\nPred: {pred_adv_name}", color=color)
            axes[i, 3].axis("off")

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_transfer_matrix(
        self,
        transfer_matrix: np.ndarray,
        model_names: List[str],
        title: str = "Adversarial Transfer Matrix",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Plot transferability matrix as heatmap.

        Args:
            transfer_matrix: N×N transfer success rates
            model_names: Names of models
            title: Figure title
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        # Create heatmap
        im = ax.imshow(transfer_matrix, cmap="YlOrRd", vmin=0, vmax=1)

        # Add colorbar
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("Transfer Success Rate", rotation=-90, va="bottom")

        # Set ticks
        ax.set_xticks(np.arange(len(model_names)))
        ax.set_yticks(np.arange(len(model_names)))
        ax.set_xticklabels(model_names, rotation=45, ha="right")
        ax.set_yticklabels(model_names)

        # Add text annotations
        for i in range(len(model_names)):
            for j in range(len(model_names)):
                value = transfer_matrix[i, j]
                text_color = "white" if value > 0.5 else "black"
                ax.text(j, i, f"{value:.2f}",
                       ha="center", va="center", color=text_color, fontsize=10)

        ax.set_xlabel("Target Model")
        ax.set_ylabel("Source Model")
        ax.set_title(title)

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_robustness_comparison(
        self,
        results: Dict[str, Dict[str, float]],
        metric: str = "adversarial_accuracy",
        title: str = "Model Robustness Comparison",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Plot bar chart comparing model robustness.

        Args:
            results: Results dictionary {model_name: {metric: value}}
            metric: Metric to plot
            title: Figure title
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        model_names = list(results.keys())
        values = [results[name].get(metric, 0) for name in model_names]
        colors = [self.colors.get(name.lower(), "#95a5a6") for name in model_names]

        bars = ax.bar(model_names, values, color=colors, edgecolor="black", linewidth=1.2)

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2%}',
                   ha='center', va='bottom', fontsize=10)

        ax.set_xlabel("Model")
        ax.set_ylabel(metric.replace("_", " ").title())
        ax.set_title(title)
        ax.set_ylim(0, 1.1)

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_epsilon_sweep(
        self,
        epsilon_results: Dict[str, Dict[float, float]],
        title: str = "Robustness vs Perturbation Budget",
        ylabel: str = "Accuracy",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Plot accuracy vs epsilon for multiple models.

        Args:
            epsilon_results: {model_name: {epsilon: accuracy}}
            title: Figure title
            ylabel: Y-axis label
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        for model_name, eps_acc in epsilon_results.items():
            epsilons = sorted(eps_acc.keys())
            accuracies = [eps_acc[e] for e in epsilons]
            color = self.colors.get(model_name.lower(), None)
            ax.plot(epsilons, accuracies, marker="o", linewidth=2,
                   label=model_name, color=color)

        ax.set_xlabel("Epsilon (ε)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend(loc="best")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_attention_comparison(
        self,
        clean_attention: torch.Tensor,
        adv_attention: torch.Tensor,
        clean_image: torch.Tensor,
        adv_image: torch.Tensor,
        layer_idx: int = -1,
        head_idx: int = 0,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Visualize attention pattern changes under adversarial attack.

        Args:
            clean_attention: Attention maps for clean image
            adv_attention: Attention maps for adversarial image
            clean_image: Clean input image
            adv_image: Adversarial input image
            layer_idx: Layer to visualize
            head_idx: Attention head to visualize
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(16, 8))
        gs = gridspec.GridSpec(2, 4, figure=fig)

        # Clean image
        ax1 = fig.add_subplot(gs[0, 0])
        clean_img = clean_image.cpu().permute(1, 2, 0).numpy()
        clean_img = np.clip(clean_img, 0, 1)
        ax1.imshow(clean_img)
        ax1.set_title("Clean Image")
        ax1.axis("off")

        # Adversarial image
        ax2 = fig.add_subplot(gs[1, 0])
        adv_img = adv_image.cpu().permute(1, 2, 0).numpy()
        adv_img = np.clip(adv_img, 0, 1)
        ax2.imshow(adv_img)
        ax2.set_title("Adversarial Image")
        ax2.axis("off")

        # Clean attention
        ax3 = fig.add_subplot(gs[0, 1])
        clean_attn = clean_attention[layer_idx, head_idx].cpu().numpy()
        im3 = ax3.imshow(clean_attn, cmap="viridis")
        ax3.set_title(f"Clean Attention (Layer {layer_idx}, Head {head_idx})")
        ax3.axis("off")
        plt.colorbar(im3, ax=ax3, fraction=0.046)

        # Adversarial attention
        ax4 = fig.add_subplot(gs[1, 1])
        adv_attn = adv_attention[layer_idx, head_idx].cpu().numpy()
        im4 = ax4.imshow(adv_attn, cmap="viridis")
        ax4.set_title(f"Adversarial Attention (Layer {layer_idx}, Head {head_idx})")
        ax4.axis("off")
        plt.colorbar(im4, ax=ax4, fraction=0.046)

        # Attention difference
        ax5 = fig.add_subplot(gs[0, 2])
        attn_diff = adv_attn - clean_attn
        im5 = ax5.imshow(attn_diff, cmap="RdBu_r", vmin=-0.1, vmax=0.1)
        ax5.set_title("Attention Difference")
        ax5.axis("off")
        plt.colorbar(im5, ax=ax5, fraction=0.046)

        # Attention entropy comparison
        ax6 = fig.add_subplot(gs[1, 2])
        clean_entropy = -np.sum(clean_attn * np.log(clean_attn + 1e-9), axis=-1)
        adv_entropy = -np.sum(adv_attn * np.log(adv_attn + 1e-9), axis=-1)
        ax6.bar([0, 1], [clean_entropy.mean(), adv_entropy.mean()],
               color=[self.colors["clean"], self.colors["adv"]])
        ax6.set_xticks([0, 1])
        ax6.set_xticklabels(["Clean", "Adversarial"])
        ax6.set_ylabel("Average Attention Entropy")
        ax6.set_title("Entropy Comparison")

        # Overlay attention on images
        ax7 = fig.add_subplot(gs[0, 3])
        # Resize attention to image size
        h, w = clean_img.shape[:2]
        attn_size = int(np.sqrt(clean_attn.shape[0]))
        cls_attn_clean = clean_attn[0, 1:].reshape(attn_size, attn_size)
        cls_attn_clean_resized = np.array(
            plt.cm.hot(cls_attn_clean / cls_attn_clean.max())[:, :, :3]
        )
        # Simple upsampling
        cls_attn_clean_resized = np.repeat(
            np.repeat(cls_attn_clean, h // attn_size, axis=0),
            w // attn_size, axis=1
        )[:h, :w]
        ax7.imshow(clean_img)
        ax7.imshow(cls_attn_clean_resized, alpha=0.5, cmap="hot")
        ax7.set_title("Clean: CLS Attention Overlay")
        ax7.axis("off")

        ax8 = fig.add_subplot(gs[1, 3])
        cls_attn_adv = adv_attn[0, 1:].reshape(attn_size, attn_size)
        cls_attn_adv_resized = np.repeat(
            np.repeat(cls_attn_adv, h // attn_size, axis=0),
            w // attn_size, axis=1
        )[:h, :w]
        ax8.imshow(adv_img)
        ax8.imshow(cls_attn_adv_resized, alpha=0.5, cmap="hot")
        ax8.set_title("Adversarial: CLS Attention Overlay")
        ax8.axis("off")

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_gradient_comparison(
        self,
        grads_cnn: torch.Tensor,
        grads_vit: torch.Tensor,
        image: torch.Tensor,
        cnn_name: str = "ResNet",
        vit_name: str = "ViT",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Compare gradient characteristics between CNN and ViT.

        Args:
            grads_cnn: Gradients from CNN
            grads_vit: Gradients from ViT
            image: Input image
            cnn_name: Name for CNN model
            vit_name: Name for ViT model
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))

        # Input image
        img = image.cpu().permute(1, 2, 0).numpy()
        img = np.clip(img, 0, 1)
        axes[0, 0].imshow(img)
        axes[0, 0].set_title("Input Image")
        axes[0, 0].axis("off")
        axes[1, 0].axis("off")

        # Gradient magnitudes
        grad_mag_cnn = grads_cnn.abs().mean(dim=0).cpu().numpy()
        grad_mag_vit = grads_vit.abs().mean(dim=0).cpu().numpy()

        im1 = axes[0, 1].imshow(grad_mag_cnn, cmap="hot")
        axes[0, 1].set_title(f"{cnn_name} Gradient Magnitude")
        axes[0, 1].axis("off")
        plt.colorbar(im1, ax=axes[0, 1], fraction=0.046)

        im2 = axes[1, 1].imshow(grad_mag_vit, cmap="hot")
        axes[1, 1].set_title(f"{vit_name} Gradient Magnitude")
        axes[1, 1].axis("off")
        plt.colorbar(im2, ax=axes[1, 1], fraction=0.046)

        # Gradient distributions
        axes[0, 2].hist(grads_cnn.cpu().flatten().numpy(), bins=100,
                       alpha=0.7, color=self.colors["cnn"], density=True)
        axes[0, 2].set_xlabel("Gradient Value")
        axes[0, 2].set_ylabel("Density")
        axes[0, 2].set_title(f"{cnn_name} Gradient Distribution")

        axes[1, 2].hist(grads_vit.cpu().flatten().numpy(), bins=100,
                       alpha=0.7, color=self.colors["vit"], density=True)
        axes[1, 2].set_xlabel("Gradient Value")
        axes[1, 2].set_ylabel("Density")
        axes[1, 2].set_title(f"{vit_name} Gradient Distribution")

        # Spatial gradient variance
        def spatial_variance(grad):
            return grad.abs().mean(dim=0).cpu().numpy().var()

        cnn_var = spatial_variance(grads_cnn)
        vit_var = spatial_variance(grads_vit)

        axes[0, 3].bar([cnn_name, vit_name], [cnn_var, vit_var],
                      color=[self.colors["cnn"], self.colors["vit"]])
        axes[0, 3].set_ylabel("Spatial Variance")
        axes[0, 3].set_title("Gradient Spatial Variance")

        # L2 norms
        cnn_l2 = torch.norm(grads_cnn.flatten()).item()
        vit_l2 = torch.norm(grads_vit.flatten()).item()

        axes[1, 3].bar([cnn_name, vit_name], [cnn_l2, vit_l2],
                      color=[self.colors["cnn"], self.colors["vit"]])
        axes[1, 3].set_ylabel("L2 Norm")
        axes[1, 3].set_title("Gradient L2 Norm")

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def plot_comprehensive_results(
        self,
        results: Dict[str, any],
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Create comprehensive results figure for paper.

        Args:
            results: Dictionary with all experiment results
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        fig = plt.figure(figsize=(20, 12))
        gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3)

        # 1. Clean vs Adversarial Accuracy
        if "accuracy" in results:
            ax1 = fig.add_subplot(gs[0, 0])
            acc_data = results["accuracy"]
            models = list(acc_data.keys())
            clean_acc = [acc_data[m].get("clean", 0) for m in models]
            adv_acc = [acc_data[m].get("adversarial", 0) for m in models]

            x = np.arange(len(models))
            width = 0.35
            ax1.bar(x - width/2, clean_acc, width, label="Clean", color=self.colors["clean"])
            ax1.bar(x + width/2, adv_acc, width, label="Adversarial", color=self.colors["adv"])
            ax1.set_xticks(x)
            ax1.set_xticklabels(models, rotation=45, ha="right")
            ax1.set_ylabel("Accuracy")
            ax1.set_title("Clean vs Adversarial Accuracy")
            ax1.legend()

        # 2. Transfer Matrix
        if "transfer_matrix" in results:
            ax2 = fig.add_subplot(gs[0, 1:3])
            tm = results["transfer_matrix"]
            names = results.get("model_names", [f"M{i}" for i in range(len(tm))])
            im = ax2.imshow(tm, cmap="YlOrRd", vmin=0, vmax=1)
            ax2.set_xticks(np.arange(len(names)))
            ax2.set_yticks(np.arange(len(names)))
            ax2.set_xticklabels(names, rotation=45, ha="right")
            ax2.set_yticklabels(names)
            ax2.set_xlabel("Target")
            ax2.set_ylabel("Source")
            ax2.set_title("Transfer Attack Success Rate")
            plt.colorbar(im, ax=ax2)

        # 3. Epsilon sweep
        if "epsilon_sweep" in results:
            ax3 = fig.add_subplot(gs[0, 3])
            for model_name, eps_acc in results["epsilon_sweep"].items():
                epsilons = sorted(eps_acc.keys())
                accuracies = [eps_acc[e] for e in epsilons]
                ax3.plot(epsilons, accuracies, marker="o", label=model_name)
            ax3.set_xlabel("ε")
            ax3.set_ylabel("Accuracy")
            ax3.set_title("Robustness vs ε")
            ax3.legend()

        # 4-6. Attack comparison
        if "attacks" in results:
            ax4 = fig.add_subplot(gs[1, :2])
            attack_data = results["attacks"]
            models = list(attack_data.keys())
            attacks = list(attack_data[models[0]].keys())

            x = np.arange(len(attacks))
            width = 0.8 / len(models)

            for i, model in enumerate(models):
                acc = [attack_data[model][atk] for atk in attacks]
                ax4.bar(x + i * width, acc, width, label=model)

            ax4.set_xticks(x + width * (len(models) - 1) / 2)
            ax4.set_xticklabels(attacks)
            ax4.set_ylabel("Accuracy")
            ax4.set_title("Robustness Against Different Attacks")
            ax4.legend()

        # 7. Gradient statistics
        if "gradient_stats" in results:
            ax5 = fig.add_subplot(gs[1, 2:])
            grad_stats = results["gradient_stats"]
            metrics = ["l2_norm_mean", "spatial_variance", "sparsity"]
            models = list(grad_stats.keys())

            x = np.arange(len(metrics))
            width = 0.8 / len(models)

            for i, model in enumerate(models):
                values = [grad_stats[model].get(m, 0) for m in metrics]
                ax5.bar(x + i * width, values, width, label=model)

            ax5.set_xticks(x + width * (len(models) - 1) / 2)
            ax5.set_xticklabels([m.replace("_", "\n") for m in metrics])
            ax5.set_title("Gradient Statistics Comparison")
            ax5.legend()

        # 8. Summary statistics table
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis("off")

        if "summary" in results:
            summary = results["summary"]
            table_data = [[k, f"{v:.4f}" if isinstance(v, float) else str(v)]
                         for k, v in summary.items()]
            table = ax6.table(
                cellText=table_data,
                colLabels=["Metric", "Value"],
                cellLoc="center",
                loc="center",
                colWidths=[0.4, 0.2]
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            ax6.set_title("Summary Statistics", pad=20)

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches="tight")

        return fig

    def save_all_figures(
        self,
        figures: Dict[str, plt.Figure],
        output_dir: str,
        formats: List[str] = ["png", "pdf"],
    ) -> None:
        """
        Save multiple figures in multiple formats.

        Args:
            figures: Dictionary of {name: figure}
            output_dir: Output directory
            formats: List of file formats to save
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        for name, fig in figures.items():
            for fmt in formats:
                filepath = output_path / f"{name}.{fmt}"
                fig.savefig(filepath, dpi=self.dpi, bbox_inches="tight", format=fmt)
                print(f"Saved: {filepath}")
