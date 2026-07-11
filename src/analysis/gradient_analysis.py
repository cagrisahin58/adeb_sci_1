"""Gradient analysis for understanding adversarial vulnerability."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Dict, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class GradientAnalyzer:
    """
    Analyze gradient characteristics of models under adversarial attacks.

    Compares gradient properties between CNNs and ViTs to understand
    why they exhibit different adversarial robustness.
    """

    def __init__(
        self,
        model: nn.Module,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize gradient analyzer.

        Args:
            model: Model to analyze
            device: Device to run analysis on
        """
        self.model = model
        self.device = device or next(model.parameters()).device
        # reduction='sum': ornek-basina gradyan olcegi batch boyutundan
        # BAGIMSIZ olur (mean-reduction'da grad 1/N olceklenir ve farkli
        # batch boyutlariyla hesaplanan normlar karsilastirilamaz)
        self.loss_fn = nn.CrossEntropyLoss(reduction="sum")

    def compute_input_gradients(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute gradients of loss with respect to input images.

        Args:
            images: Input images
            labels: True labels

        Returns:
            Input gradients (same shape as images)
        """
        self.model.eval()
        images = images.to(self.device).clone().requires_grad_(True)
        labels = labels.to(self.device)

        outputs = self.model(images)
        loss = self.loss_fn(outputs, labels)
        loss.backward()

        return images.grad.detach()

    def compute_gradient_statistics(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> Dict[str, float]:
        """
        Compute various gradient statistics.

        Args:
            images: Input images
            labels: True labels

        Returns:
            Dictionary of gradient statistics
        """
        grads = self.compute_input_gradients(images, labels)

        # Flatten gradients for statistics
        grads_flat = grads.view(grads.shape[0], -1)

        stats = {
            # Magnitude statistics
            "l2_norm_mean": torch.norm(grads_flat, p=2, dim=1).mean().item(),
            "l2_norm_std": torch.norm(grads_flat, p=2, dim=1).std().item(),
            "linf_norm_mean": grads_flat.abs().max(dim=1)[0].mean().item(),
            "l1_norm_mean": torch.norm(grads_flat, p=1, dim=1).mean().item(),

            # Distribution statistics
            "mean": grads_flat.mean().item(),
            "std": grads_flat.std().item(),
            "skewness": self._compute_skewness(grads_flat).item(),
            "kurtosis": self._compute_kurtosis(grads_flat).item(),

            # Sparsity (percentage of near-zero gradients)
            # UYARI: mutlak esik olcek bagimlidir (M11) - gradyan normu buyuk
            # modelde "sparsity" yapay olarak dusuk cikar; karsilastirma icin
            # asagidaki olcek-bagimsiz metrikleri kullanin
            "sparsity": (grads_flat.abs() < 1e-6).float().mean().item(),

            # Scale-invariant sparsity metrics (M11)
            "sparsity_hoyer": self._compute_hoyer_sparsity(grads_flat).item(),
            "sparsity_gini": self._compute_gini_sparsity(grads_flat).item(),
            "sparsity_rel_threshold": self._compute_relative_sparsity(grads_flat).item(),

            # Spatial statistics (for 2D gradients)
            "spatial_variance": self._compute_spatial_variance(grads).item(),
        }

        return stats

    @staticmethod
    def _compute_hoyer_sparsity(grads_flat: torch.Tensor) -> torch.Tensor:
        """
        Hoyer sparsity: (sqrt(n) - L1/L2) / (sqrt(n) - 1), per-sample mean.

        Scale-invariant; 0 = uniform, 1 = single nonzero component.
        Reference: Hoyer, "Non-negative Matrix Factorization with Sparseness
        Constraints", JMLR 2004.
        """
        n = grads_flat.shape[1]
        l1 = grads_flat.abs().sum(dim=1)
        l2 = torch.norm(grads_flat, p=2, dim=1)
        sqrt_n = torch.sqrt(torch.tensor(float(n), device=grads_flat.device))
        hoyer = (sqrt_n - l1 / (l2 + 1e-12)) / (sqrt_n - 1)
        return hoyer.mean()

    @staticmethod
    def _compute_gini_sparsity(grads_flat: torch.Tensor) -> torch.Tensor:
        """
        Gini coefficient of |g| per sample, averaged over the batch.

        Scale-invariant; 0 = perfectly uniform magnitudes, ->1 = concentrated.
        """
        abs_sorted, _ = grads_flat.abs().sort(dim=1)
        n = abs_sorted.shape[1]
        idx = torch.arange(1, n + 1, device=grads_flat.device, dtype=abs_sorted.dtype)
        # Gini = (2*sum(i*x_i) / (n*sum(x_i))) - (n+1)/n  (x sorted ascending)
        gini = (2 * (idx * abs_sorted).sum(dim=1) / (n * abs_sorted.sum(dim=1) + 1e-12)
                - (n + 1) / n)
        return gini.mean()

    @staticmethod
    def _compute_relative_sparsity(grads_flat: torch.Tensor, rel: float = 0.01) -> torch.Tensor:
        """
        Fraction of components below `rel` * per-sample max |g|.

        Scale-invariant alternative to the absolute 1e-6 threshold.
        """
        max_abs = grads_flat.abs().max(dim=1, keepdim=True)[0]
        frac = (grads_flat.abs() < rel * max_abs).float().mean(dim=1)
        return frac.mean()

    def _compute_skewness(self, x: torch.Tensor) -> torch.Tensor:
        """Compute skewness of distribution."""
        mean = x.mean()
        std = x.std()
        return ((x - mean) ** 3).mean() / (std ** 3 + 1e-9)

    def _compute_kurtosis(self, x: torch.Tensor) -> torch.Tensor:
        """Compute kurtosis of distribution."""
        mean = x.mean()
        std = x.std()
        return ((x - mean) ** 4).mean() / (std ** 4 + 1e-9) - 3

    def _compute_spatial_variance(self, grads: torch.Tensor) -> torch.Tensor:
        """Compute variance of gradient magnitudes across spatial locations."""
        # grads: (batch, C, H, W)
        grad_magnitude = grads.abs().mean(dim=1)  # Average over channels
        # Compute variance across spatial dimensions
        spatial_var = grad_magnitude.view(grad_magnitude.shape[0], -1).var(dim=1)
        return spatial_var.mean()

    def compare_gradient_landscapes(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        epsilon_range: List[float] = [0.001, 0.005, 0.01, 0.02, 0.03],
    ) -> Dict[str, List[float]]:
        """
        Analyze how loss landscape changes with perturbation magnitude.

        This reveals how "smooth" or "rugged" the loss surface is.

        Args:
            images: Input images
            labels: True labels
            epsilon_range: Range of perturbation magnitudes to test

        Returns:
            Dictionary with loss values at different epsilons
        """
        self.model.eval()
        images = images.to(self.device)
        labels = labels.to(self.device)

        results = {
            "epsilons": epsilon_range,
            "loss_random": [],
            "loss_gradient": [],
            "loss_change_rate": [],
        }

        # Get gradient direction
        grads = self.compute_input_gradients(images, labels)
        grad_sign = grads.sign()

        # Base loss
        with torch.no_grad():
            base_outputs = self.model(images)
            base_loss = self.loss_fn(base_outputs, labels).item()

        for eps in epsilon_range:
            # Random perturbation
            random_pert = torch.randn_like(images) * eps
            random_pert = random_pert.clamp(-eps, eps)

            with torch.no_grad():
                random_images = (images + random_pert).clamp(0, 1)
                random_outputs = self.model(random_images)
                random_loss = self.loss_fn(random_outputs, labels).item()

            # Gradient-aligned perturbation
            with torch.no_grad():
                grad_images = (images + eps * grad_sign).clamp(0, 1)
                grad_outputs = self.model(grad_images)
                grad_loss = self.loss_fn(grad_outputs, labels).item()

            results["loss_random"].append(random_loss)
            results["loss_gradient"].append(grad_loss)
            results["loss_change_rate"].append((grad_loss - base_loss) / eps)

        return results

    def compute_gradient_alignment(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        use_abs: bool = True,
    ) -> float:
        """
        Measure how consistent gradient directions are across samples.

        High alignment suggests the model is vulnerable to universal perturbations.

        Computes ALL within-batch pairs (M21: onceki surum yalnizca ilk 10
        ornegi kullaniyordu; makaledeki tum-ciftler formuluyle uyum icin
        vektorize edildi).

        Args:
            images: Input images
            labels: True labels
            use_abs: If True, average |cos|; if False, signed cosine.
                Reported run2 values used |cos| - keep True for comparability,
                and disclose the estimator in the paper.

        Returns:
            Average pairwise cosine similarity between gradient pairs
        """
        grads = self.compute_input_gradients(images, labels)
        grads_flat = grads.view(grads.shape[0], -1)

        # Normalize gradients
        grads_norm = F.normalize(grads_flat, p=2, dim=1)

        batch_size = grads_norm.shape[0]
        if batch_size < 2:
            return 0.0

        # All-pairs cosine similarity via Gram matrix, upper triangle
        sim_matrix = grads_norm @ grads_norm.t()
        iu = torch.triu_indices(batch_size, batch_size, offset=1)
        pair_sims = sim_matrix[iu[0], iu[1]]
        if use_abs:
            pair_sims = pair_sims.abs()

        return pair_sims.mean().item()

    def compute_layer_gradient_norms(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> Dict[str, float]:
        """
        Compute gradient norms for each layer.

        Helps identify which layers are most sensitive to perturbations.

        Args:
            images: Input images
            labels: True labels

        Returns:
            Dictionary mapping layer names to gradient norms
        """
        self.model.eval()
        images = images.to(self.device)
        labels = labels.to(self.device)

        # Forward pass
        outputs = self.model(images)
        loss = self.loss_fn(outputs, labels)

        # Backward pass
        self.model.zero_grad()
        loss.backward()

        layer_norms = {}
        for name, param in self.model.named_parameters():
            if param.grad is not None:
                layer_norms[name] = param.grad.norm().item()

        return layer_norms

    def visualize_gradient_comparison(
        self,
        model1: nn.Module,
        model2: nn.Module,
        images: torch.Tensor,
        labels: torch.Tensor,
        model1_name: str = "ResNet",
        model2_name: str = "ViT",
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Visualize gradient comparison between two models.

        Args:
            model1: First model
            model2: Second model
            images: Input images
            labels: True labels
            model1_name: Name for first model
            model2_name: Name for second model
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        # Compute gradients for both models
        self.model = model1.to(self.device)
        grads1 = self.compute_input_gradients(images, labels)
        stats1 = self.compute_gradient_statistics(images, labels)

        self.model = model2.to(self.device)
        grads2 = self.compute_input_gradients(images, labels)
        stats2 = self.compute_gradient_statistics(images, labels)

        fig, axes = plt.subplots(2, 3, figsize=(15, 10))

        # Gradient magnitude histograms
        axes[0, 0].hist(grads1.cpu().flatten().numpy(), bins=100, alpha=0.5, label=model1_name, density=True)
        axes[0, 0].hist(grads2.cpu().flatten().numpy(), bins=100, alpha=0.5, label=model2_name, density=True)
        axes[0, 0].set_xlabel("Gradient Value")
        axes[0, 0].set_ylabel("Density")
        axes[0, 0].set_title("Gradient Distribution")
        axes[0, 0].legend()

        # L2 norms comparison
        l2_1 = torch.norm(grads1.view(grads1.shape[0], -1), p=2, dim=1).cpu().numpy()
        l2_2 = torch.norm(grads2.view(grads2.shape[0], -1), p=2, dim=1).cpu().numpy()
        axes[0, 1].bar([0, 1], [l2_1.mean(), l2_2.mean()], yerr=[l2_1.std(), l2_2.std()])
        axes[0, 1].set_xticks([0, 1])
        axes[0, 1].set_xticklabels([model1_name, model2_name])
        axes[0, 1].set_ylabel("L2 Norm")
        axes[0, 1].set_title("Gradient L2 Norm")

        # Sample gradient visualizations
        sample_idx = 0
        grad_vis1 = grads1[sample_idx].abs().mean(0).cpu().numpy()
        grad_vis2 = grads2[sample_idx].abs().mean(0).cpu().numpy()

        axes[0, 2].imshow(images[sample_idx].cpu().permute(1, 2, 0).numpy().clip(0, 1))
        axes[0, 2].set_title("Input Image")
        axes[0, 2].axis("off")

        axes[1, 0].imshow(grad_vis1, cmap="hot")
        axes[1, 0].set_title(f"{model1_name} Gradient")
        axes[1, 0].axis("off")

        axes[1, 1].imshow(grad_vis2, cmap="hot")
        axes[1, 1].set_title(f"{model2_name} Gradient")
        axes[1, 1].axis("off")

        # Statistics comparison
        stats_names = ["l2_norm_mean", "linf_norm_mean", "sparsity", "spatial_variance"]
        stats_values1 = [stats1[k] for k in stats_names]
        stats_values2 = [stats2[k] for k in stats_names]

        x = np.arange(len(stats_names))
        width = 0.35
        axes[1, 2].bar(x - width/2, stats_values1, width, label=model1_name)
        axes[1, 2].bar(x + width/2, stats_values2, width, label=model2_name)
        axes[1, 2].set_xticks(x)
        axes[1, 2].set_xticklabels(stats_names, rotation=45, ha="right")
        axes[1, 2].set_title("Gradient Statistics")
        axes[1, 2].legend()

        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=150, bbox_inches="tight")

        return fig
