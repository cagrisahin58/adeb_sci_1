"""DenseNet models adapted for CIFAR-10."""

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Tuple

from .base import BaseModel
from .registry import register_model


@register_model("densenet121")
class CIFAR10DenseNet121(BaseModel):
    """
    DenseNet121 adapted for CIFAR-10.

    Modifications from standard DenseNet121:
    - First conv layer uses 3x3 kernel instead of 7x7
    - Initial pooling is removed
    - Final classifier outputs 10 classes
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        """
        Initialize DenseNet121 for CIFAR-10.

        Args:
            num_classes: Number of output classes (default: 10)
            pretrained: Whether to use ImageNet pretrained weights (default: False)
        """
        super().__init__(num_classes=num_classes)

        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.densenet121(weights=weights)

        # Adapt for CIFAR-10 (32x32 images)
        self.model.features.conv0 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.features.pool0 = nn.Identity()

        # Update classifier for num_classes
        num_features = self.model.classifier.in_features
        self.model.classifier = nn.Linear(num_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Get features before the final classifier."""
        features = self.model.features(x)
        out = nn.functional.relu(features, inplace=True)
        out = nn.functional.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        return out

    def freeze_backbone(self) -> None:
        """Freeze all layers except the classifier."""
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


@register_model("densenet169")
class CIFAR10DenseNet169(BaseModel):
    """DenseNet169 adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.densenet169(weights=weights)

        self.model.features.conv0 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.features.pool0 = nn.Identity()

        num_features = self.model.classifier.in_features
        self.model.classifier = nn.Linear(num_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        features = self.model.features(x)
        out = nn.functional.relu(features, inplace=True)
        out = nn.functional.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        return out

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False


@register_model("densenet201")
class CIFAR10DenseNet201(BaseModel):
    """DenseNet201 adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.densenet201(weights=weights)

        self.model.features.conv0 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.features.pool0 = nn.Identity()

        num_features = self.model.classifier.in_features
        self.model.classifier = nn.Linear(num_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        features = self.model.features(x)
        out = nn.functional.relu(features, inplace=True)
        out = nn.functional.adaptive_avg_pool2d(out, (1, 1))
        out = torch.flatten(out, 1)
        return out

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "classifier" not in name:
                param.requires_grad = False
