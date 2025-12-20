"""MART (Improving Adversarial Robustness Requires Revisiting Misclassified Examples) defense."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

from .base import TrainingDefense
from .registry import register_defense


@register_defense("mart")
class MARTDefense(TrainingDefense):
    """
    MART: Improving Adversarial Robustness Requires Revisiting Misclassified Examples.

    Reference: Wang et al., "Improving Adversarial Robustness Requires Revisiting Misclassified Examples", ICLR 2020

    MART explicitly differentiates the misclassified and correctly classified examples
    during adversarial training by reweighting the loss.

    Loss = BCE(f(x'), y) + beta * (1 - p_y(x)) * KL(f(x) || f(x'))

    where p_y(x) is the probability of the true class on natural examples.
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
        Initialize MART defense.

        Args:
            model: The model to defend
            beta: Regularization parameter
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

    def _mart_loss(
        self,
        logits_adv: torch.Tensor,
        logits_natural: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute MART loss.

        Uses Boosted Cross-Entropy (BCE) for adversarial examples
        and weighted KL divergence.
        """
        batch_size = labels.size(0)

        # Probabilities
        prob_natural = F.softmax(logits_natural, dim=1)
        prob_adv = F.softmax(logits_adv, dim=1)

        # Get probability of true class on natural examples
        # Shape: (batch_size,)
        true_class_prob = prob_natural[torch.arange(batch_size), labels]

        # Boosted Cross-Entropy loss
        # BCE = -log(p_y(x')) - log(1 - max_{k != y} p_k(x'))
        log_prob_adv = F.log_softmax(logits_adv, dim=1)

        # First term: -log(p_y(x'))
        ce_loss = F.cross_entropy(logits_adv, labels, reduction="none")

        # Second term: -log(1 - max_{k != y} p_k(x'))
        # Create mask for non-true classes
        mask = torch.ones_like(prob_adv)
        mask[torch.arange(batch_size), labels] = 0

        # Get max probability for non-true classes
        max_other_prob = (prob_adv * mask).max(dim=1)[0]

        # Boosted term (with numerical stability)
        boosted_term = -torch.log(1 - max_other_prob + 1e-8)

        # BCE loss
        bce_loss = ce_loss + boosted_term

        # KL divergence weighted by misclassification probability
        kl_div = F.kl_div(
            log_prob_adv,
            prob_natural.detach(),
            reduction="none",
        ).sum(dim=1)

        # Weight: (1 - p_y(x)) emphasizes misclassified examples
        weight = 1 - true_class_prob.detach()

        # Combined loss
        loss = bce_loss.mean() + self.beta * (weight * kl_div).mean()

        return loss

    def _pgd_attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Generate adversarial examples using PGD."""
        images = images.detach()
        original_images = images.clone()

        # Random initialization
        delta = torch.empty_like(images).uniform_(-self.eps, self.eps)
        delta = torch.clamp(original_images + delta, 0, 1) - original_images

        for _ in range(self.steps):
            delta.requires_grad = True

            adv_images = original_images + delta
            outputs = self.model(adv_images)
            loss = F.cross_entropy(outputs, labels)

            loss.backward()

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
        Compute MART loss.

        Args:
            model: The model being trained
            images: Training images
            labels: Training labels

        Returns:
            MART loss
        """
        # Natural predictions
        logits_natural = model(images)

        # Generate adversarial examples
        model.eval()
        adv_images = self._pgd_attack(images, labels)
        model.train()

        # Adversarial predictions
        logits_adv = model(adv_images)

        # Compute MART loss
        loss = self._mart_loss(logits_adv, logits_natural, labels)

        return loss

    def generate_adversarial(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Generate adversarial examples."""
        self.model.eval()
        return self._pgd_attack(images, labels)
