"""Standard adversarial training defense."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Callable

from .base import TrainingDefense
from .registry import register_defense


@register_defense("adversarial_training")
class AdversarialTraining(TrainingDefense):
    """
    Standard Adversarial Training defense.

    Reference: Madry et al., "Towards Deep Learning Models Resistant to Adversarial Attacks", ICLR 2018

    Trains the model on both clean and adversarial examples.
    Loss = (L_clean + L_adversarial) / 2
    """

    def __init__(
        self,
        model: nn.Module,
        attack: Optional[Callable] = None,
        eps: float = 8 / 255,
        alpha: float = 2 / 255,
        steps: int = 10,
        random_start: bool = True,
        mix_ratio: float = 0.5,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize Adversarial Training.

        Args:
            model: The model to defend
            attack: Attack function (if None, uses internal PGD)
            eps: Maximum perturbation
            alpha: Step size for PGD
            steps: Number of PGD steps
            random_start: Whether to use random initialization
            mix_ratio: Ratio of adversarial loss (0.5 means equal weight)
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.attack = attack
        self.eps = eps
        self.alpha = alpha
        self.steps = steps
        self.random_start = random_start
        self.mix_ratio = mix_ratio
        self.loss_fn = nn.CrossEntropyLoss()

    def _pgd_attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Internal PGD attack for adversarial training."""
        images = images.detach()
        original_images = images.clone()

        if self.random_start:
            images = images + torch.empty_like(images).uniform_(-self.eps, self.eps)
            images = torch.clamp(images, 0, 1)

        for _ in range(self.steps):
            images.requires_grad = True

            outputs = self.model(images)
            loss = self.loss_fn(outputs, labels)

            loss.backward()

            adv_images = images + self.alpha * images.grad.sign()
            delta = torch.clamp(adv_images - original_images, -self.eps, self.eps)
            images = torch.clamp(original_images + delta, 0, 1).detach()

        return images

    def get_loss(
        self,
        model: nn.Module,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute adversarial training loss.

        Args:
            model: The model being trained
            images: Training images
            labels: Training labels

        Returns:
            Combined loss
        """
        # Save current training mode and set to eval for attack generation
        was_training = model.training

        # Generate adversarial examples
        model.eval()
        if self.attack is not None:
            adv_images = self.attack(images, labels)
        else:
            adv_images = self._pgd_attack(images, labels)

        # Restore training mode
        model.train(was_training)

        # Compute losses
        outputs_clean = model(images)
        loss_clean = self.loss_fn(outputs_clean, labels)

        outputs_adv = model(adv_images)
        loss_adv = self.loss_fn(outputs_adv, labels)

        # Combined loss
        loss = (1 - self.mix_ratio) * loss_clean + self.mix_ratio * loss_adv

        return loss

    def generate_adversarial(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Generate adversarial examples for a batch."""
        self.model.eval()
        if self.attack is not None:
            return self.attack(images, labels)
        else:
            return self._pgd_attack(images, labels)
