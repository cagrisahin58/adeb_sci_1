"""TRADES (TRadeoff-inspired Adversarial DEfense via Surrogate-loss minimization) defense."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

from .base import TrainingDefense
from .registry import register_defense


@register_defense("trades")
class TRADESDefense(TrainingDefense):
    """
    TRADES: TRadeoff-inspired Adversarial DEfense via Surrogate-loss minimization.

    Reference: Zhang et al., "Theoretically Principled Trade-off between Robustness and Accuracy", ICML 2019

    Loss = CE(f(x), y) + beta * KL(f(x) || f(x'))

    TRADES explicitly balances natural accuracy and robustness through the beta parameter.
    """

    def __init__(
        self,
        model: nn.Module,
        beta: float = 6.0,
        eps: float = 8 / 255,
        alpha: float = 2 / 255,
        steps: int = 10,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize TRADES defense.

        Args:
            model: The model to defend
            beta: Trade-off parameter (higher = more robust, less accurate)
            eps: Maximum perturbation
            alpha: Step size for PGD
            steps: Number of PGD steps
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.beta = beta
        self.eps = eps
        self.alpha = alpha
        self.steps = steps
        self.ce_loss = nn.CrossEntropyLoss()
        self.kl_loss = nn.KLDivLoss(reduction="batchmean")

    def _trades_pgd(
        self,
        images: torch.Tensor,
        logits_natural: torch.Tensor,
    ) -> torch.Tensor:
        """
        Generate adversarial examples for TRADES.

        Instead of maximizing CE loss, TRADES maximizes KL divergence
        between natural and adversarial predictions.
        """
        images = images.detach()
        original_images = images.clone()

        # Random initialization
        delta = torch.empty_like(images).uniform_(-self.eps, self.eps)
        delta = torch.clamp(original_images + delta, 0, 1) - original_images

        for _ in range(self.steps):
            delta.requires_grad = True

            adv_images = original_images + delta
            logits_adv = self.model(adv_images)

            # KL divergence loss (maximize divergence from natural)
            loss = self.kl_loss(
                F.log_softmax(logits_adv, dim=1),
                F.softmax(logits_natural.detach(), dim=1),
            )

            loss.backward()

            # Update delta
            grad = delta.grad.sign()
            delta = delta.detach() + self.alpha * grad
            delta = torch.clamp(delta, -self.eps, self.eps)
            delta = torch.clamp(original_images + delta, 0, 1) - original_images

        return original_images + delta

    def get_loss(
        self,
        model: nn.Module,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute TRADES loss.

        Args:
            model: The model being trained
            images: Training images
            labels: Training labels

        Returns:
            TRADES loss
        """
        # Natural predictions
        logits_natural = model(images)
        loss_natural = self.ce_loss(logits_natural, labels)

        # Generate adversarial examples
        model.eval()
        adv_images = self._trades_pgd(images, logits_natural.detach())
        model.train()

        # Adversarial predictions
        logits_adv = model(adv_images)

        # KL divergence loss
        loss_robust = self.kl_loss(
            F.log_softmax(logits_adv, dim=1),
            F.softmax(logits_natural.detach(), dim=1),
        )

        # Combined loss
        loss = loss_natural + self.beta * loss_robust

        return loss

    def generate_adversarial(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """Generate TRADES adversarial examples."""
        self.model.eval()
        with torch.no_grad():
            logits_natural = self.model(images)
        return self._trades_pgd(images, logits_natural)
