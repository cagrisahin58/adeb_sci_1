"""Base attack class for all attack methods."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import torch
import torch.nn as nn


class BaseAttack(ABC):
    """
    Abstract base class for all attack methods.

    All attacks should inherit from this class and implement the required methods.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize the base attack.

        Args:
            model: The model to attack
            eps: Maximum perturbation (epsilon)
            targeted: Whether the attack is targeted
            device: Device to run the attack on
        """
        self.model = model
        self.eps = eps
        self.targeted = targeted
        self.device = device or next(model.parameters()).device

        # Set model to eval mode for attacks
        self.model.eval()

    @abstractmethod
    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Target labels for targeted attacks

        Returns:
            Adversarial images
        """
        pass

    def __call__(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Convenience method to call attack."""
        return self.attack(images, labels, target_labels)

    def _check_inputs(
        self, images: torch.Tensor, labels: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Validate and prepare inputs.

        Args:
            images: Input images
            labels: Input labels

        Returns:
            Tuple of (images, labels) on the correct device
        """
        images = images.to(self.device)
        labels = labels.to(self.device)

        # Ensure images are in valid range [0, 1] (with small tolerance for floating point errors)
        if images.min() < -1e-6 or images.max() > 1 + 1e-6:
            raise ValueError(
                f"Images should be in range [0, 1], got [{images.min():.4f}, {images.max():.4f}]. "
                f"If using normalized data, denormalize before attacks."
            )

        # Clamp to [0, 1] to handle small floating point errors
        images = torch.clamp(images, 0.0, 1.0)

        return images, labels

    def _clamp(self, images: torch.Tensor, min_val: float = 0.0, max_val: float = 1.0) -> torch.Tensor:
        """Clamp images to valid range."""
        return torch.clamp(images, min=min_val, max=max_val)

    def _project(
        self,
        adv_images: torch.Tensor,
        original_images: torch.Tensor,
        eps: Optional[float] = None,
    ) -> torch.Tensor:
        """
        Project adversarial images to epsilon ball around original images.

        Args:
            adv_images: Current adversarial images
            original_images: Original clean images
            eps: Maximum perturbation (uses self.eps if None)

        Returns:
            Projected adversarial images
        """
        if eps is None:
            eps = self.eps

        # Project to Linf ball
        delta = adv_images - original_images
        delta = torch.clamp(delta, -eps, eps)
        adv_images = original_images + delta

        # Clamp to valid image range
        return self._clamp(adv_images)

    @property
    def name(self) -> str:
        """Return the name of the attack."""
        return self.__class__.__name__
