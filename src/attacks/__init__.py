"""Attack methods for adversarial robustness evaluation."""

from .registry import AttackRegistry, register_attack
from .base import BaseAttack

# Import all attacks to register them
from .fgsm import FGSMAttack, TargetedFGSMAttack
from .pgd import PGDAttack, TargetedPGDAttack, PGDL2Attack
from .cw import CWAttack, CWLinfAttack
from .deepfool import DeepFoolAttack, DeepFoolLinfAttack
from .spatial import SpatialAttack, RotationAttack, TranslationAttack

# AutoAttack (optional dependency)
try:
    from .autoattack import AutoAttackWrapper, AutoAttackLinf, AutoAttackL2
    AUTOATTACK_AVAILABLE = True
except ImportError:
    AUTOATTACK_AVAILABLE = False

__all__ = [
    "AttackRegistry",
    "register_attack",
    "BaseAttack",
    # FGSM
    "FGSMAttack",
    "TargetedFGSMAttack",
    # PGD
    "PGDAttack",
    "TargetedPGDAttack",
    "PGDL2Attack",
    # C&W
    "CWAttack",
    "CWLinfAttack",
    # DeepFool
    "DeepFoolAttack",
    "DeepFoolLinfAttack",
    # Spatial
    "SpatialAttack",
    "RotationAttack",
    "TranslationAttack",
]

if AUTOATTACK_AVAILABLE:
    __all__.extend([
        "AutoAttackWrapper",
        "AutoAttackLinf",
        "AutoAttackL2",
    ])
