"""Defense mechanisms for adversarial robustness."""

from .registry import DefenseRegistry, register_defense
from .base import BaseDefense, TrainingDefense, InferenceDefense

# Import all defenses to register them
from .adversarial_training import AdversarialTraining
from .tta import TTADefense, TenCropTTADefense
from .trades import TRADESDefense
from .mart import MARTDefense
from .purification import DenoisingDefense, JPEGDefense, RandomizationDefense

__all__ = [
    "DefenseRegistry",
    "register_defense",
    "BaseDefense",
    "TrainingDefense",
    "InferenceDefense",
    # Training defenses
    "AdversarialTraining",
    "TRADESDefense",
    "MARTDefense",
    # Inference defenses
    "TTADefense",
    "TenCropTTADefense",
    "DenoisingDefense",
    "JPEGDefense",
    "RandomizationDefense",
]
