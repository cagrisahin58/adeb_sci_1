"""Spatial transformation attacks."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
import math

from .base import BaseAttack
from .registry import register_attack


@register_attack("spatial")
class SpatialAttack(BaseAttack):
    """
    Spatial transformation attack.

    Reference: Engstrom et al., "Exploring the Landscape of Spatial Robustness", ICML 2019

    This attack finds adversarial examples through spatial transformations
    (rotation, translation) rather than pixel-wise perturbations.
    """

    def __init__(
        self,
        model: nn.Module,
        rotation_range: Tuple[float, float] = (-30.0, 30.0),
        translation_range: Tuple[float, float] = (-0.1, 0.1),
        grid_size: int = 5,
        use_grid_search: bool = True,
        steps: int = 20,
        lr: float = 0.1,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize Spatial attack.

        Args:
            model: The model to attack
            rotation_range: Range of rotation angles in degrees (min, max)
            translation_range: Range of translation as fraction of image size (min, max)
            grid_size: Number of grid points for each dimension (for grid search)
            use_grid_search: Use grid search (True) or gradient-based optimization (False)
            steps: Number of optimization steps (for gradient-based)
            lr: Learning rate for optimization (for gradient-based)
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=0.0, targeted=False, device=device)
        self.rotation_range = rotation_range
        self.translation_range = translation_range
        self.grid_size = grid_size
        self.use_grid_search = use_grid_search
        self.steps = steps
        self.lr = lr
        self.loss_fn = nn.CrossEntropyLoss(reduction="none")

    def _get_affine_matrix(
        self,
        theta: torch.Tensor,
        tx: torch.Tensor,
        ty: torch.Tensor,
    ) -> torch.Tensor:
        """
        Create affine transformation matrix.

        Args:
            theta: Rotation angle in radians
            tx: X translation
            ty: Y translation

        Returns:
            Affine matrix of shape (batch_size, 2, 3)
        """
        cos_theta = torch.cos(theta)
        sin_theta = torch.sin(theta)

        # Rotation + Translation matrix
        matrix = torch.zeros(theta.shape[0], 2, 3, device=self.device)
        matrix[:, 0, 0] = cos_theta
        matrix[:, 0, 1] = -sin_theta
        matrix[:, 0, 2] = tx
        matrix[:, 1, 0] = sin_theta
        matrix[:, 1, 1] = cos_theta
        matrix[:, 1, 2] = ty

        return matrix

    def _apply_transform(
        self,
        images: torch.Tensor,
        theta: torch.Tensor,
        tx: torch.Tensor,
        ty: torch.Tensor,
    ) -> torch.Tensor:
        """Apply affine transformation to images."""
        batch_size = images.shape[0]

        # Get affine matrix
        affine_matrix = self._get_affine_matrix(theta, tx, ty)

        # Create sampling grid
        grid = F.affine_grid(affine_matrix, images.shape, align_corners=False)

        # Apply transformation
        transformed = F.grid_sample(images, grid, align_corners=False, padding_mode="border")

        return transformed

    def _grid_search(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Grid search for adversarial transformations."""
        batch_size = images.shape[0]

        # Generate grid of parameters
        rotations = torch.linspace(
            self.rotation_range[0], self.rotation_range[1], self.grid_size, device=self.device
        )
        translations = torch.linspace(
            self.translation_range[0], self.translation_range[1], self.grid_size, device=self.device
        )

        # Convert degrees to radians
        rotations_rad = rotations * math.pi / 180

        best_adv = images.clone()
        best_loss = torch.full((batch_size,), float("-inf"), device=self.device)

        # Search over all combinations
        for theta in rotations_rad:
            for tx in translations:
                for ty in translations:
                    # Apply transformation
                    theta_batch = torch.full((batch_size,), theta.item(), device=self.device)
                    tx_batch = torch.full((batch_size,), tx.item(), device=self.device)
                    ty_batch = torch.full((batch_size,), ty.item(), device=self.device)

                    transformed = self._apply_transform(images, theta_batch, tx_batch, ty_batch)

                    # Compute loss
                    with torch.no_grad():
                        outputs = self.model(transformed)
                        loss = self.loss_fn(outputs, labels)

                    # Update best adversarial examples
                    improved = loss > best_loss
                    best_adv[improved] = transformed[improved]
                    best_loss[improved] = loss[improved]

        return best_adv

    def _gradient_search(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
    ) -> torch.Tensor:
        """Gradient-based optimization for adversarial transformations."""
        batch_size = images.shape[0]

        # Initialize parameters
        theta = torch.zeros(batch_size, device=self.device, requires_grad=True)
        tx = torch.zeros(batch_size, device=self.device, requires_grad=True)
        ty = torch.zeros(batch_size, device=self.device, requires_grad=True)

        optimizer = torch.optim.Adam([theta, tx, ty], lr=self.lr)

        best_adv = images.clone()
        best_loss = torch.full((batch_size,), float("-inf"), device=self.device)

        for _ in range(self.steps):
            optimizer.zero_grad()

            # Clamp parameters to valid range
            theta_clamped = torch.clamp(
                theta,
                self.rotation_range[0] * math.pi / 180,
                self.rotation_range[1] * math.pi / 180,
            )
            tx_clamped = torch.clamp(tx, self.translation_range[0], self.translation_range[1])
            ty_clamped = torch.clamp(ty, self.translation_range[0], self.translation_range[1])

            # Apply transformation
            transformed = self._apply_transform(images, theta_clamped, tx_clamped, ty_clamped)

            # Compute loss (maximize for adversarial)
            outputs = self.model(transformed)
            loss = self.loss_fn(outputs, labels)

            # Backward pass (negate for maximization)
            (-loss.mean()).backward()
            optimizer.step()

            # Update best adversarial examples
            with torch.no_grad():
                improved = loss > best_loss
                best_adv[improved] = transformed[improved].detach()
                best_loss[improved] = loss[improved]

        return best_adv

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using spatial transformations.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Not used for this attack

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)

        if self.use_grid_search:
            return self._grid_search(images, labels)
        else:
            return self._gradient_search(images, labels)


@register_attack("spatial_rotation")
class RotationAttack(SpatialAttack):
    """Spatial attack with rotation only (no translation)."""

    def __init__(
        self,
        model: nn.Module,
        rotation_range: Tuple[float, float] = (-30.0, 30.0),
        grid_size: int = 11,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            rotation_range=rotation_range,
            translation_range=(0.0, 0.0),
            grid_size=grid_size,
            use_grid_search=True,
            device=device,
        )


@register_attack("spatial_translation")
class TranslationAttack(SpatialAttack):
    """Spatial attack with translation only (no rotation)."""

    def __init__(
        self,
        model: nn.Module,
        translation_range: Tuple[float, float] = (-0.1, 0.1),
        grid_size: int = 11,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            rotation_range=(0.0, 0.0),
            translation_range=translation_range,
            grid_size=grid_size,
            use_grid_search=True,
            device=device,
        )
