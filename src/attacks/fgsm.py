"""FGSM (Fast Gradient Sign Method) attack implementation."""

import torch
import torch.nn as nn
from typing import Optional

from .base import BaseAttack
from .registry import register_attack


@register_attack("fgsm")
class FGSMAttack(BaseAttack):
    """
    Fast Gradient Sign Method (FGSM) attack.

    Reference: Goodfellow et al., "Explaining and Harnessing Adversarial Examples", ICLR 2015

    This is a single-step attack that perturbs the input in the direction
    of the gradient sign scaled by epsilon.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize FGSM attack.

        Args:
            model: The model to attack
            eps: Maximum perturbation (epsilon)
            targeted: Whether the attack is targeted
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=eps, targeted=targeted, device=device)
        self.loss_fn = nn.CrossEntropyLoss()

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using FGSM.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Target labels for targeted attacks

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)
        images = images.clone().detach()

        # Enable gradient computation for images
        images.requires_grad = True

        # Forward pass
        outputs = self.model(images)

        # Compute loss
        if self.targeted and target_labels is not None:
            target_labels = target_labels.to(self.device)
            loss = self.loss_fn(outputs, target_labels)
        else:
            loss = self.loss_fn(outputs, labels)

        # Backward pass
        loss.backward()

        # Get gradient sign
        grad_sign = images.grad.sign()

        # Create adversarial examples
        if self.targeted:
            # For targeted attacks, move toward target
            adv_images = images - self.eps * grad_sign
        else:
            # For untargeted attacks, move away from true label
            adv_images = images + self.eps * grad_sign

        # Clamp to valid range
        adv_images = self._clamp(adv_images.detach())

        return adv_images


@register_attack("fgsm_targeted")
class TargetedFGSMAttack(FGSMAttack):
    """Targeted FGSM attack."""

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        device: Optional[torch.device] = None,
    ):
        super().__init__(model=model, eps=eps, targeted=True, device=device)
