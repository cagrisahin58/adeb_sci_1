"""EfficientNet models for CIFAR-10."""

import torch
import torch.nn as nn
from typing import Tuple

try:
    import timm
    TIMM_AVAILABLE = True
except ImportError:
    TIMM_AVAILABLE = False

from .base import BaseModel
from .registry import register_model


@register_model("efficientnet_b0")
class CIFAR10EfficientNetB0(BaseModel):
    """
    EfficientNet-B0 for CIFAR-10.

    Uses timm library's efficientnet_b0 model.
    Automatically handles input resizing.
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        """
        Initialize EfficientNet-B0 for CIFAR-10.

        Args:
            num_classes: Number of output classes (default: 10)
            pretrained: Whether to use pretrained weights (default: False)
        """
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for EfficientNet models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "efficientnet_b0",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        # Resize layer for CIFAR-10 (32x32 -> 224x224)
        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Get features before the final classifier."""
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        """Freeze all layers except the classifier."""
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


@register_model("efficientnet_b1")
class CIFAR10EfficientNetB1(BaseModel):
    """EfficientNet-B1 for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for EfficientNet models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "efficientnet_b1",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(240, 240), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False


@register_model("efficientnet_b2")
class CIFAR10EfficientNetB2(BaseModel):
    """EfficientNet-B2 for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for EfficientNet models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "efficientnet_b2",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(260, 260), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False
