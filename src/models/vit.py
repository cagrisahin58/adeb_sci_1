"""Vision Transformer (ViT) models for CIFAR-10."""

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


@register_model("vit_tiny")
class CIFAR10ViTTiny(BaseModel):
    """
    ViT-Tiny adapted for CIFAR-10.

    Uses timm library's vit_tiny_patch16_224 model.
    Input images are resized to 224x224 for patch-based processing.
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        """
        Initialize ViT-Tiny for CIFAR-10.

        Args:
            num_classes: Number of output classes (default: 10)
            pretrained: Whether to use pretrained weights (default: False)
        """
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_tiny_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        # Resize layer for CIFAR-10 (32x32 -> 224x224)
        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Resize input from 32x32 to 224x224
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Get features before the final classification head."""
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        """Freeze all layers except the classification head."""
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)  # Native input, resized internally


@register_model("vit_small")
class CIFAR10ViTSmall(BaseModel):
    """ViT-Small adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_small_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False


@register_model("vit_base")
class CIFAR10ViTBase(BaseModel):
    """ViT-Base adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        if not TIMM_AVAILABLE:
            raise ImportError(
                "timm library is required for ViT models. "
                "Install it with: pip install timm"
            )

        self.model = timm.create_model(
            "vit_base_patch16_224",
            pretrained=pretrained,
            num_classes=num_classes,
        )

        self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.resize(x)
        return self.model.forward_features(x)

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "head" not in name:
                param.requires_grad = False
