"""Test-Time Augmentation (TTA) defense."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Tuple
import torchvision.transforms as T

from .base import InferenceDefense
from .registry import register_defense


@register_defense("tta")
class TTADefense(InferenceDefense):
    """
    Test-Time Augmentation (TTA) defense.

    Applies multiple augmentations to the input image during inference
    and averages the predictions to improve robustness.
    """

    def __init__(
        self,
        model: nn.Module,
        n_augmentations: int = 10,
        crop_size: int = 32,
        use_flips: bool = True,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize TTA defense.

        Args:
            model: The model to defend
            n_augmentations: Number of random augmentations
            crop_size: Size for random crops
            use_flips: Whether to include horizontal flips
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.n_augmentations = n_augmentations
        self.crop_size = crop_size
        self.use_flips = use_flips

    def _generate_augmentations(
        self,
        images: torch.Tensor,
    ) -> List[torch.Tensor]:
        """Generate augmented versions of the input images."""
        augmented = [images]  # Include original

        batch_size, channels, height, width = images.shape
        padding = 4

        for _ in range(self.n_augmentations - 1):
            # Random crop with padding
            padded = F.pad(images, [padding] * 4, mode="reflect")

            # Random crop positions
            top = torch.randint(0, 2 * padding + 1, (batch_size,))
            left = torch.randint(0, 2 * padding + 1, (batch_size,))

            cropped = torch.zeros_like(images)
            for i in range(batch_size):
                cropped[i] = padded[i, :, top[i]:top[i] + height, left[i]:left[i] + width]

            # Random horizontal flip
            if self.use_flips and torch.rand(1) > 0.5:
                cropped = torch.flip(cropped, dims=[3])

            augmented.append(cropped)

        return augmented

    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply TTA defense (returns defended images).

        Note: For TTA, we don't modify the images, just ensemble predictions.
        This method returns the original images.
        """
        return images

    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Apply TTA and return averaged predictions.

        Args:
            images: Input images
            labels: Not used

        Returns:
            Averaged logits from all augmentations
        """
        images = images.to(self.device)
        self.model.eval()

        # Generate augmentations
        augmented_images = self._generate_augmentations(images)

        # Get predictions for each augmentation
        all_logits = []
        with torch.no_grad():
            for aug_images in augmented_images:
                logits = self.model(aug_images)
                all_logits.append(logits)

        # Average predictions
        avg_logits = torch.stack(all_logits).mean(dim=0)

        return avg_logits


@register_defense("tta_tencrop")
class TenCropTTADefense(InferenceDefense):
    """
    TTA defense using TenCrop augmentation.

    Uses 5 crops (4 corners + center) and their horizontal flips.
    """

    def __init__(
        self,
        model: nn.Module,
        crop_size: int = 32,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize TenCrop TTA defense.

        Args:
            model: The model to defend
            crop_size: Size for crops
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.crop_size = crop_size
        self.ten_crop = T.TenCrop(crop_size)

    def _apply_ten_crop(self, images: torch.Tensor) -> torch.Tensor:
        """Apply TenCrop to a batch of images."""
        batch_size = images.shape[0]
        all_crops = []

        for i in range(batch_size):
            # TenCrop returns tuple of 10 crops
            crops = self.ten_crop(images[i])
            crops_tensor = torch.stack(crops)  # Shape: (10, C, H, W)
            all_crops.append(crops_tensor)

        # Shape: (batch_size, 10, C, H, W)
        return torch.stack(all_crops)

    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """Returns original images."""
        return images

    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Apply TenCrop TTA and return averaged predictions.

        Args:
            images: Input images
            labels: Not used

        Returns:
            Averaged logits from all crops
        """
        images = images.to(self.device)
        self.model.eval()

        batch_size = images.shape[0]

        # Apply TenCrop: (batch_size, 10, C, H, W)
        crops = self._apply_ten_crop(images)

        # Reshape for batch processing: (batch_size * 10, C, H, W)
        crops_flat = crops.view(-1, *crops.shape[2:])

        # Get predictions
        with torch.no_grad():
            logits = self.model(crops_flat)

        # Reshape back: (batch_size, 10, num_classes)
        logits = logits.view(batch_size, 10, -1)

        # Average predictions
        avg_logits = logits.mean(dim=1)

        return avg_logits
