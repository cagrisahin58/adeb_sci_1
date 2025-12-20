"""PGD (Projected Gradient Descent) attack implementation."""

import torch
import torch.nn as nn
from typing import Optional

from .base import BaseAttack
from .registry import register_attack


@register_attack("pgd")
class PGDAttack(BaseAttack):
    """
    Projected Gradient Descent (PGD) attack.

    Reference: Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks", ICLR 2018

    This is an iterative attack that takes multiple small steps in the direction
    of the gradient sign, projecting back to the epsilon ball after each step.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        alpha: float = 2 / 255,
        steps: int = 10,
        random_start: bool = True,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize PGD attack.

        Args:
            model: The model to attack
            eps: Maximum perturbation (epsilon)
            alpha: Step size for each iteration
            steps: Number of attack iterations
            random_start: Whether to start with random perturbation
            targeted: Whether the attack is targeted
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=eps, targeted=targeted, device=device)
        self.alpha = alpha
        self.steps = steps
        self.random_start = random_start
        self.loss_fn = nn.CrossEntropyLoss()

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using PGD.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Target labels for targeted attacks

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)
        original_images = images.clone().detach()

        # Initialize adversarial images
        if self.random_start:
            # Start from random point within epsilon ball
            adv_images = images + torch.empty_like(images).uniform_(-self.eps, self.eps)
            adv_images = self._clamp(adv_images)
        else:
            adv_images = images.clone()

        # Iterative attack
        for _ in range(self.steps):
            adv_images = adv_images.clone().detach().requires_grad_(True)

            # Forward pass
            outputs = self.model(adv_images)

            # Compute loss
            if self.targeted and target_labels is not None:
                target_labels = target_labels.to(self.device)
                loss = self.loss_fn(outputs, target_labels)
            else:
                loss = self.loss_fn(outputs, labels)

            # Backward pass
            loss.backward()

            # Get gradient sign
            grad_sign = adv_images.grad.sign()

            # Update adversarial images
            if self.targeted:
                adv_images = adv_images - self.alpha * grad_sign
            else:
                adv_images = adv_images + self.alpha * grad_sign

            # Project back to epsilon ball
            adv_images = self._project(adv_images.detach(), original_images)

        return adv_images


@register_attack("pgd_targeted")
class TargetedPGDAttack(PGDAttack):
    """Targeted PGD attack."""

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        alpha: float = 2 / 255,
        steps: int = 10,
        random_start: bool = True,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            eps=eps,
            alpha=alpha,
            steps=steps,
            random_start=random_start,
            targeted=True,
            device=device,
        )


@register_attack("pgd_l2")
class PGDL2Attack(BaseAttack):
    """
    PGD attack with L2 norm constraint.

    Instead of Linf ball, projects to L2 ball.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 0.5,
        alpha: float = 0.1,
        steps: int = 10,
        random_start: bool = True,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        super().__init__(model=model, eps=eps, targeted=targeted, device=device)
        self.alpha = alpha
        self.steps = steps
        self.random_start = random_start
        self.loss_fn = nn.CrossEntropyLoss()

    def _project_l2(
        self,
        adv_images: torch.Tensor,
        original_images: torch.Tensor,
    ) -> torch.Tensor:
        """Project to L2 ball."""
        delta = adv_images - original_images
        batch_size = delta.shape[0]

        # Compute L2 norm per sample
        delta_flat = delta.view(batch_size, -1)
        norm = torch.norm(delta_flat, p=2, dim=1, keepdim=True)

        # Scale down if exceeds epsilon
        factor = torch.clamp(self.eps / (norm + 1e-12), max=1.0)
        delta_flat = delta_flat * factor
        delta = delta_flat.view_as(delta)

        adv_images = original_images + delta
        return self._clamp(adv_images)

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        images, labels = self._check_inputs(images, labels)
        original_images = images.clone().detach()

        if self.random_start:
            delta = torch.randn_like(images)
            delta_flat = delta.view(images.shape[0], -1)
            norm = torch.norm(delta_flat, p=2, dim=1, keepdim=True)
            delta_flat = delta_flat / (norm + 1e-12) * self.eps * torch.rand(images.shape[0], 1, device=self.device)
            delta = delta_flat.view_as(images)
            adv_images = self._clamp(images + delta)
        else:
            adv_images = images.clone()

        for _ in range(self.steps):
            adv_images = adv_images.clone().detach().requires_grad_(True)

            outputs = self.model(adv_images)

            if self.targeted and target_labels is not None:
                target_labels = target_labels.to(self.device)
                loss = self.loss_fn(outputs, target_labels)
            else:
                loss = self.loss_fn(outputs, labels)

            loss.backward()

            # Normalize gradient for L2 attack
            grad = adv_images.grad
            grad_flat = grad.view(grad.shape[0], -1)
            grad_norm = torch.norm(grad_flat, p=2, dim=1, keepdim=True)
            grad_normalized = grad_flat / (grad_norm + 1e-12)
            grad_normalized = grad_normalized.view_as(grad)

            if self.targeted:
                adv_images = adv_images - self.alpha * grad_normalized
            else:
                adv_images = adv_images + self.alpha * grad_normalized

            adv_images = self._project_l2(adv_images.detach(), original_images)

        return adv_images
