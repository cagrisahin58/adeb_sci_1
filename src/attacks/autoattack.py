"""AutoAttack wrapper for reliable robustness evaluation."""

import torch
import torch.nn as nn
from typing import Optional, List

from .base import BaseAttack
from .registry import register_attack

try:
    from autoattack import AutoAttack as AA
    AUTOATTACK_AVAILABLE = True
except ImportError:
    AUTOATTACK_AVAILABLE = False


@register_attack("autoattack")
class AutoAttackWrapper(BaseAttack):
    """
    AutoAttack: A reliable evaluation of adversarial robustness.

    Reference: Croce & Hein, "Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks", ICML 2020

    AutoAttack is an ensemble of four attacks:
    - APGD-CE: Auto-PGD with cross-entropy loss
    - APGD-T: Auto-PGD with targeted DLR loss
    - FAB-T: Fast Adaptive Boundary attack (targeted)
    - Square: Query-efficient black-box attack

    This wrapper provides a consistent interface with other attacks.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        norm: str = "Linf",
        version: str = "standard",
        attacks_to_run: Optional[List[str]] = None,
        verbose: bool = False,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize AutoAttack.

        Args:
            model: The model to attack
            eps: Maximum perturbation (epsilon)
            norm: Norm for perturbation constraint ('Linf' or 'L2')
            version: AutoAttack version ('standard', 'plus', 'rand')
            attacks_to_run: List of attacks to run (None for all)
            verbose: Whether to print progress
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=eps, targeted=False, device=device)

        if not AUTOATTACK_AVAILABLE:
            raise ImportError(
                "autoattack library is required for AutoAttack. "
                "Install it with: pip install autoattack"
            )

        self.norm = norm
        self.version = version
        self.attacks_to_run = attacks_to_run
        self.verbose = verbose

        # Create AutoAttack instance
        self.autoattack = AA(
            model=model,
            norm=norm,
            eps=eps,
            version=version,
            verbose=verbose,
        )

        if attacks_to_run is not None:
            self.autoattack.attacks_to_run = attacks_to_run

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using AutoAttack.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Not used (AutoAttack handles targeting internally)

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)

        # Run AutoAttack
        adv_images = self.autoattack.run_standard_evaluation(
            images, labels, bs=images.shape[0]
        )

        return adv_images

    def run_individual_attacks(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> dict:
        """
        Run individual attacks and return results for each.

        Args:
            images: Clean images
            labels: True labels

        Returns:
            Dictionary with attack name -> adversarial images
        """
        images, labels = self._check_inputs(images, labels)
        results = {}

        for attack_name in self.autoattack.attacks_to_run:
            # Save current settings
            original_attacks = self.autoattack.attacks_to_run

            # Run single attack
            self.autoattack.attacks_to_run = [attack_name]
            adv_images = self.autoattack.run_standard_evaluation(
                images.clone(), labels, bs=images.shape[0]
            )
            results[attack_name] = adv_images

            # Restore settings
            self.autoattack.attacks_to_run = original_attacks

        return results


@register_attack("autoattack_linf")
class AutoAttackLinf(AutoAttackWrapper):
    """AutoAttack with Linf norm."""

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        version: str = "standard",
        verbose: bool = False,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            eps=eps,
            norm="Linf",
            version=version,
            verbose=verbose,
            device=device,
        )


@register_attack("autoattack_l2")
class AutoAttackL2(AutoAttackWrapper):
    """AutoAttack with L2 norm."""

    def __init__(
        self,
        model: nn.Module,
        eps: float = 0.5,
        version: str = "standard",
        verbose: bool = False,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            eps=eps,
            norm="L2",
            version=version,
            verbose=verbose,
            device=device,
        )
