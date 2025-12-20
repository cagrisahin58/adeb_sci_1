"""Base model class for all model architectures."""

from abc import ABC, abstractmethod
from typing import Optional, Tuple
import torch
import torch.nn as nn


class BaseModel(nn.Module, ABC):
    """
    Abstract base class for all model architectures.

    All models should inherit from this class and implement the required methods.
    """

    def __init__(self, num_classes: int = 10):
        """
        Initialize the base model.

        Args:
            num_classes: Number of output classes
        """
        super().__init__()
        self.num_classes = num_classes

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the model.

        Args:
            x: Input tensor of shape (batch_size, channels, height, width)

        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        pass

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get feature representations before the final classification layer.

        Args:
            x: Input tensor

        Returns:
            Feature tensor
        """
        raise NotImplementedError("get_features not implemented for this model")

    @property
    def input_size(self) -> Tuple[int, int]:
        """Expected input image size (height, width)."""
        return (32, 32)  # Default for CIFAR-10

    @property
    def input_channels(self) -> int:
        """Expected number of input channels."""
        return 3

    def count_parameters(self) -> int:
        """Count the number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def freeze(self) -> None:
        """Freeze all model parameters."""
        for param in self.parameters():
            param.requires_grad = False

    def unfreeze(self) -> None:
        """Unfreeze all model parameters."""
        for param in self.parameters():
            param.requires_grad = True

    def freeze_backbone(self) -> None:
        """Freeze backbone parameters, keeping classifier trainable."""
        raise NotImplementedError("freeze_backbone not implemented for this model")

    @classmethod
    def load_pretrained(cls, path: str, device: Optional[torch.device] = None, **kwargs) -> "BaseModel":
        """
        Load a pretrained model from a checkpoint.

        Args:
            path: Path to the checkpoint file
            device: Device to load the model to
            **kwargs: Additional arguments for model initialization

        Returns:
            Loaded model instance
        """
        model = cls(**kwargs)

        map_location = device if device is not None else "cpu"
        state_dict = torch.load(path, map_location=map_location)

        # Handle both full checkpoints and plain state dicts
        if isinstance(state_dict, dict) and "model_state_dict" in state_dict:
            state_dict = state_dict["model_state_dict"]

        model.load_state_dict(state_dict)

        if device is not None:
            model = model.to(device)

        return model
