"""Model architectures for adversarial robustness evaluation."""

from .registry import ModelRegistry, register_model
from .base import BaseModel

# Import all models to register them
from .resnet import CIFAR10ResNet18, CIFAR10ResNet34, CIFAR10ResNet50
from .vit import CIFAR10ViTTiny, CIFAR10ViTSmall, CIFAR10ViTBase
from .densenet import CIFAR10DenseNet121, CIFAR10DenseNet169, CIFAR10DenseNet201
from .efficientnet import CIFAR10EfficientNetB0, CIFAR10EfficientNetB1, CIFAR10EfficientNetB2
# Konsey 2x2 (29.10.2026): resnet18_224, resnet18_224_in1k, vit_tiny_in1k
from .r224 import CIFAR10ResNet18R224, CIFAR10ResNet18R224IN1k, CIFAR10ViTTinyIN1k

# RobustBench models (optional dependency)
try:
    from .robustbench import RobustBenchModel, RobustBenchCarmon, RobustBenchWang, load_robustbench_model
    ROBUSTBENCH_AVAILABLE = True
except ImportError:
    ROBUSTBENCH_AVAILABLE = False

__all__ = [
    "ModelRegistry",
    "register_model",
    "BaseModel",
    # ResNet
    "CIFAR10ResNet18",
    "CIFAR10ResNet34",
    "CIFAR10ResNet50",
    # ViT
    "CIFAR10ViTTiny",
    "CIFAR10ViTSmall",
    "CIFAR10ViTBase",
    # DenseNet
    "CIFAR10DenseNet121",
    "CIFAR10DenseNet169",
    "CIFAR10DenseNet201",
    # EfficientNet
    "CIFAR10EfficientNetB0",
    "CIFAR10EfficientNetB1",
    "CIFAR10EfficientNetB2",
]

if ROBUSTBENCH_AVAILABLE:
    __all__.extend([
        "RobustBenchModel",
        "RobustBenchCarmon",
        "RobustBenchWang",
        "load_robustbench_model",
    ])
