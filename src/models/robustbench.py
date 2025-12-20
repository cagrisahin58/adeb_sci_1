"""RobustBench pre-trained robust models."""

import torch
import torch.nn as nn
from typing import Optional, Tuple, List

from .base import BaseModel
from .registry import register_model

try:
    from robustbench import load_model as rb_load_model
    from robustbench.utils import load_model
    ROBUSTBENCH_AVAILABLE = True
except ImportError:
    ROBUSTBENCH_AVAILABLE = False


# Popular RobustBench models for CIFAR-10
ROBUSTBENCH_MODELS = {
    "Carmon2019Unlabeled": "Carmon2019Unlabeled",
    "Wang2023Better_WRN-28-10": "Wang2023Better_WRN-28-10",
    "Rebuffi2021Fixing_70_16_cutmix_extra": "Rebuffi2021Fixing_70_16_cutmix_extra",
    "Gowal2021Improving_28_10_ddpm_100m": "Gowal2021Improving_28_10_ddpm_100m",
    "Sehwag2021Proxy_ResNest152": "Sehwag2021Proxy_ResNest152",
}


class RobustBenchModel(BaseModel):
    """
    Wrapper for RobustBench pre-trained robust models.

    These models are pre-trained with various adversarial training techniques
    and provide state-of-the-art adversarial robustness on CIFAR-10.
    """

    def __init__(
        self,
        model_name: str = "Carmon2019Unlabeled",
        dataset: str = "cifar10",
        threat_model: str = "Linf",
        num_classes: int = 10,
    ):
        """
        Initialize a RobustBench model.

        Args:
            model_name: Name of the RobustBench model
            dataset: Dataset the model was trained on ('cifar10', 'cifar100', 'imagenet')
            threat_model: Threat model ('Linf', 'L2', 'corruptions')
            num_classes: Number of output classes
        """
        super().__init__(num_classes=num_classes)

        if not ROBUSTBENCH_AVAILABLE:
            raise ImportError(
                "robustbench library is required for RobustBench models. "
                "Install it with: pip install robustbench"
            )

        self.model_name = model_name
        self.dataset = dataset
        self.threat_model = threat_model

        # Load the pre-trained model
        self.model = rb_load_model(
            model_name=model_name,
            dataset=dataset,
            threat_model=threat_model,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        """
        Get features before the final classification layer.

        Note: This may not be available for all RobustBench models.
        """
        if hasattr(self.model, "forward_features"):
            return self.model.forward_features(x)
        else:
            raise NotImplementedError(
                f"get_features is not implemented for {self.model_name}"
            )

    def freeze_backbone(self) -> None:
        """Freeze all parameters (RobustBench models are typically used frozen)."""
        for param in self.model.parameters():
            param.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        if self.dataset == "imagenet":
            return (224, 224)
        return (32, 32)

    @staticmethod
    def list_available_models(
        dataset: str = "cifar10",
        threat_model: str = "Linf"
    ) -> List[str]:
        """
        List available RobustBench models for a dataset and threat model.

        Args:
            dataset: Dataset name
            threat_model: Threat model

        Returns:
            List of available model names
        """
        if not ROBUSTBENCH_AVAILABLE:
            raise ImportError("robustbench library is required")

        from robustbench.utils import list_available_models as rb_list
        return rb_list(dataset=dataset, threat_model=threat_model)


# Register specific popular models
@register_model("robustbench_carmon")
class RobustBenchCarmon(RobustBenchModel):
    """Carmon2019Unlabeled model from RobustBench."""

    def __init__(self, num_classes: int = 10):
        super().__init__(
            model_name="Carmon2019Unlabeled",
            dataset="cifar10",
            threat_model="Linf",
            num_classes=num_classes,
        )


@register_model("robustbench_wang")
class RobustBenchWang(RobustBenchModel):
    """Wang2023Better model from RobustBench (state-of-the-art)."""

    def __init__(self, num_classes: int = 10):
        super().__init__(
            model_name="Wang2023Better_WRN-28-10",
            dataset="cifar10",
            threat_model="Linf",
            num_classes=num_classes,
        )


def load_robustbench_model(
    model_name: str,
    dataset: str = "cifar10",
    threat_model: str = "Linf",
) -> RobustBenchModel:
    """
    Convenience function to load a RobustBench model.

    Args:
        model_name: Name of the model
        dataset: Dataset name
        threat_model: Threat model

    Returns:
        RobustBenchModel instance
    """
    return RobustBenchModel(
        model_name=model_name,
        dataset=dataset,
        threat_model=threat_model,
    )
