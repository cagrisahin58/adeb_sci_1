"""Attention pattern analysis for Vision Transformers under adversarial attacks."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Dict, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class AttentionAnalyzer:
    """
    Analyze attention patterns in Vision Transformers under adversarial perturbations.

    This helps understand WHY ViTs are more vulnerable to adversarial attacks
    by examining how attention patterns degrade under perturbation.
    """

    def __init__(
        self,
        model: nn.Module,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize attention analyzer.

        Args:
            model: ViT model to analyze
            device: Device to run analysis on
        """
        self.model = model
        self.device = device or next(model.parameters()).device
        self.attention_maps: Dict[str, torch.Tensor] = {}
        self._hooks = []

    def _register_hooks(self):
        """Register forward hooks to capture attention maps."""
        self._hooks = []

        def get_attention_hook(name):
            def hook(module, input, output):
                # For timm ViT models, attention is in the output
                if hasattr(module, 'attn_drop'):
                    # Get attention weights before dropout
                    self.attention_maps[name] = output.detach()
            return hook

        # Find attention modules
        for name, module in self.model.named_modules():
            if 'attn' in name.lower() and hasattr(module, 'forward'):
                hook = module.register_forward_hook(get_attention_hook(name))
                self._hooks.append(hook)

    def _remove_hooks(self):
        """Remove all registered hooks."""
        for hook in self._hooks:
            hook.remove()
        self._hooks = []
        self.attention_maps = {}

    def get_attention_maps(
        self,
        images: torch.Tensor,
    ) -> Dict[str, torch.Tensor]:
        """
        Extract attention maps for given images.

        Args:
            images: Input images (batch_size, C, H, W)

        Returns:
            Dictionary of attention maps per layer
        """
        self.model.eval()
        self._register_hooks()

        try:
            with torch.no_grad():
                images = images.to(self.device)
                _ = self.model(images)

            return {k: v.cpu() for k, v in self.attention_maps.items()}
        finally:
            self._remove_hooks()

    def compute_attention_entropy(
        self,
        attention_map: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute entropy of attention distribution.

        Higher entropy = more diffuse attention
        Lower entropy = more focused attention

        Args:
            attention_map: Attention weights (batch, heads, seq, seq)

        Returns:
            Entropy per head (batch, heads)
        """
        # Normalize attention if not already
        attn = attention_map / (attention_map.sum(dim=-1, keepdim=True) + 1e-9)

        # Compute entropy
        entropy = -torch.sum(attn * torch.log(attn + 1e-9), dim=-1)

        # Average over sequence positions
        return entropy.mean(dim=-1)

    def compute_attention_distance(
        self,
        clean_attention: torch.Tensor,
        adv_attention: torch.Tensor,
        metric: str = "kl",
    ) -> torch.Tensor:
        """
        Compute distance between clean and adversarial attention patterns.

        Args:
            clean_attention: Clean attention maps
            adv_attention: Adversarial attention maps
            metric: Distance metric ('kl', 'js', 'l2', 'cosine')

        Returns:
            Distance per sample
        """
        clean = clean_attention.flatten(start_dim=1)
        adv = adv_attention.flatten(start_dim=1)

        if metric == "kl":
            # KL divergence
            clean_norm = F.softmax(clean, dim=-1)
            adv_norm = F.softmax(adv, dim=-1)
            return F.kl_div(
                torch.log(adv_norm + 1e-9),
                clean_norm,
                reduction='none'
            ).sum(dim=-1)

        elif metric == "js":
            # Jensen-Shannon divergence
            clean_norm = F.softmax(clean, dim=-1)
            adv_norm = F.softmax(adv, dim=-1)
            m = 0.5 * (clean_norm + adv_norm)
            kl_clean = F.kl_div(torch.log(m + 1e-9), clean_norm, reduction='none').sum(-1)
            kl_adv = F.kl_div(torch.log(m + 1e-9), adv_norm, reduction='none').sum(-1)
            return 0.5 * (kl_clean + kl_adv)

        elif metric == "l2":
            return torch.norm(clean - adv, p=2, dim=-1)

        elif metric == "cosine":
            return 1 - F.cosine_similarity(clean, adv, dim=-1)

        else:
            raise ValueError(f"Unknown metric: {metric}")

    def analyze_attention_degradation(
        self,
        clean_images: torch.Tensor,
        adv_images: torch.Tensor,
    ) -> Dict[str, any]:
        """
        Comprehensive analysis of attention degradation under attack.

        Args:
            clean_images: Clean input images
            adv_images: Adversarial input images

        Returns:
            Dictionary with analysis results
        """
        # Get attention maps
        clean_attn = self.get_attention_maps(clean_images)
        adv_attn = self.get_attention_maps(adv_images)

        results = {
            "layers": {},
            "summary": {},
        }

        for layer_name in clean_attn.keys():
            if layer_name not in adv_attn:
                continue

            clean_map = clean_attn[layer_name]
            adv_map = adv_attn[layer_name]

            # Entropy analysis
            clean_entropy = self.compute_attention_entropy(clean_map)
            adv_entropy = self.compute_attention_entropy(adv_map)
            entropy_change = (adv_entropy - clean_entropy).mean().item()

            # Distance analysis
            distances = {
                "kl": self.compute_attention_distance(clean_map, adv_map, "kl").mean().item(),
                "l2": self.compute_attention_distance(clean_map, adv_map, "l2").mean().item(),
                "cosine": self.compute_attention_distance(clean_map, adv_map, "cosine").mean().item(),
            }

            results["layers"][layer_name] = {
                "clean_entropy": clean_entropy.mean().item(),
                "adv_entropy": adv_entropy.mean().item(),
                "entropy_change": entropy_change,
                "distances": distances,
            }

        # Summary statistics
        if results["layers"]:
            all_entropy_changes = [v["entropy_change"] for v in results["layers"].values()]
            all_kl_distances = [v["distances"]["kl"] for v in results["layers"].values()]

            results["summary"] = {
                "mean_entropy_change": np.mean(all_entropy_changes),
                "max_entropy_change": np.max(all_entropy_changes),
                "mean_kl_distance": np.mean(all_kl_distances),
                "most_affected_layer": max(results["layers"].keys(),
                                          key=lambda k: results["layers"][k]["distances"]["kl"]),
            }

        return results

    def visualize_attention_comparison(
        self,
        clean_images: torch.Tensor,
        adv_images: torch.Tensor,
        sample_idx: int = 0,
        layer_name: Optional[str] = None,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Visualize attention map comparison between clean and adversarial.

        Args:
            clean_images: Clean input images
            adv_images: Adversarial input images
            sample_idx: Which sample to visualize
            layer_name: Which layer to visualize (None for first)
            save_path: Path to save figure

        Returns:
            matplotlib Figure
        """
        clean_attn = self.get_attention_maps(clean_images)
        adv_attn = self.get_attention_maps(adv_images)

        if layer_name is None:
            layer_name = list(clean_attn.keys())[0]

        clean_map = clean_attn[layer_name][sample_idx].mean(0)  # Average over heads
        adv_map = adv_attn[layer_name][sample_idx].mean(0)

        fig, axes = plt.subplots(1, 4, figsize=(16, 4))

        # Clean image
        img = clean_images[sample_idx].cpu().permute(1, 2, 0).numpy()
        img = (img - img.min()) / (img.max() - img.min())
        axes[0].imshow(img)
        axes[0].set_title("Clean Image")
        axes[0].axis("off")

        # Clean attention
        axes[1].imshow(clean_map.numpy(), cmap="viridis")
        axes[1].set_title("Clean Attention")
        axes[1].axis("off")

        # Adversarial attention
        axes[2].imshow(adv_map.numpy(), cmap="viridis")
        axes[2].set_title("Adversarial Attention")
        axes[2].axis("off")

        # Difference
        diff = (adv_map - clean_map).abs().numpy()
        axes[3].imshow(diff, cmap="hot")
        axes[3].set_title("Attention Difference")
        axes[3].axis("off")

        plt.suptitle(f"Attention Analysis: {layer_name}")
        plt.tight_layout()

        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=150, bbox_inches="tight")

        return fig
