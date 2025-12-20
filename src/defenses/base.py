"""Base defense class for all defense mechanisms."""

from abc import ABC, abstractmethod
from typing import Optional, Callable
import torch
import torch.nn as nn


class BaseDefense(ABC):
    """
    Abstract base class for all defense mechanisms.

    All defenses should inherit from this class and implement the required methods.
    """

    def __init__(self, model: nn.Module, device: Optional[torch.device] = None):
        """
        Initialize the base defense.

        Args:
            model: The model to defend
            device: Device to run the defense on
        """
        self.model = model
        self.device = device or next(model.parameters()).device

    @abstractmethod
    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Apply the defense mechanism.

        Args:
            images: Input images
            labels: Optional labels

        Returns:
            Defended/processed images or predictions
        """
        pass

    def __call__(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Convenience method to call apply."""
        return self.apply(images, labels)

    @property
    def name(self) -> str:
        """Return the name of the defense."""
        return self.__class__.__name__


class TrainingDefense(BaseDefense):
    """
    Base class for training-time defenses.

    These defenses modify the training procedure to improve robustness.
    """

    @abstractmethod
    def get_loss(
        self,
        model: nn.Module,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """
        Compute the defense-specific loss.

        Args:
            model: The model being trained
            images: Training images
            labels: Training labels

        Returns:
            Loss tensor
        """
        pass

    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Training defenses don't apply at inference time."""
        return self.model(images)


class InferenceDefense(BaseDefense):
    """
    Base class for inference-time defenses.

    These defenses are applied during inference to improve robustness.
    """

    @abstractmethod
    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply defense to input images before classification.

        Args:
            images: Input images (potentially adversarial)

        Returns:
            Defended images
        """
        pass

    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Apply defense and then classify."""
        defended_images = self.defend(images)
        return self.model(defended_images)
