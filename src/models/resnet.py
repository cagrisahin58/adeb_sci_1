"""ResNet models adapted for CIFAR-10."""

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Optional, Tuple

from .base import BaseModel
from .registry import register_model


@register_model("resnet18")
class CIFAR10ResNet18(BaseModel):
    """
    ResNet18 adapted for CIFAR-10.

    Modifications from standard ResNet18:
    - First conv layer uses 3x3 kernel instead of 7x7 (for 32x32 images)
    - MaxPool layer is removed
    - Final FC layer outputs 10 classes
    """

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        """
        Initialize CIFAR-10 adapted ResNet18.

        Args:
            num_classes: Number of output classes (default: 10 for CIFAR-10)
            pretrained: Whether to use ImageNet pretrained weights (default: False)
        """
        super().__init__(num_classes=num_classes)

        # Load base ResNet18
        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.resnet18(weights=weights)

        # Adapt for CIFAR-10 (32x32 images)
        self.model.conv1 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.maxpool = nn.Identity()
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """Get features before the final FC layer."""
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        x = self.model.avgpool(x)
        x = torch.flatten(x, 1)
        return x

    def freeze_backbone(self) -> None:
        """Freeze all layers except the final FC layer."""
        for name, param in self.model.named_parameters():
            if "fc" not in name:
                param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


@register_model("resnet34")
class CIFAR10ResNet34(BaseModel):
    """ResNet34 adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.resnet34(weights=weights)

        self.model.conv1 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.maxpool = nn.Identity()
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        x = self.model.avgpool(x)
        x = torch.flatten(x, 1)
        return x

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "fc" not in name:
                param.requires_grad = False


@register_model("resnet50")
class CIFAR10ResNet50(BaseModel):
    """ResNet50 adapted for CIFAR-10."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)

        weights = "IMAGENET1K_V1" if pretrained else None
        self.model = models.resnet50(weights=weights)

        self.model.conv1 = nn.Conv2d(
            3, 64, kernel_size=3, stride=1, padding=1, bias=False
        )
        self.model.maxpool = nn.Identity()
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        x = self.model.avgpool(x)
        x = torch.flatten(x, 1)
        return x

    def freeze_backbone(self) -> None:
        for name, param in self.model.named_parameters():
            if "fc" not in name:
                param.requires_grad = False
