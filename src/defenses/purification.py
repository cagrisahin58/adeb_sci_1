"""Adversarial purification defenses."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional

from .base import InferenceDefense
from .registry import register_defense


@register_defense("denoise")
class DenoisingDefense(InferenceDefense):
    """
    Denoising-based adversarial purification.

    Uses a simple denoising operation to remove adversarial perturbations.
    Can use mean filtering, Gaussian blur, or a learned denoiser.
    """

    def __init__(
        self,
        model: nn.Module,
        denoise_method: str = "gaussian",
        kernel_size: int = 3,
        sigma: float = 1.0,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize denoising defense.

        Args:
            model: The model to defend
            denoise_method: Denoising method ('gaussian', 'mean', 'median')
            kernel_size: Kernel size for filtering
            sigma: Standard deviation for Gaussian blur
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.denoise_method = denoise_method
        self.kernel_size = kernel_size
        self.sigma = sigma

        # Create Gaussian kernel
        if denoise_method == "gaussian":
            self.kernel = self._create_gaussian_kernel(kernel_size, sigma)

    def _create_gaussian_kernel(self, kernel_size: int, sigma: float) -> torch.Tensor:
        """Create a Gaussian kernel for blurring."""
        # Create 1D Gaussian kernel
        x = torch.arange(kernel_size) - kernel_size // 2
        gauss_1d = torch.exp(-x.float() ** 2 / (2 * sigma ** 2))
        gauss_1d = gauss_1d / gauss_1d.sum()

        # Create 2D kernel via outer product
        gauss_2d = gauss_1d.unsqueeze(1) @ gauss_1d.unsqueeze(0)

        # Shape for conv2d: (out_channels, in_channels/groups, kH, kW)
        # We'll apply to each channel separately
        kernel = gauss_2d.unsqueeze(0).unsqueeze(0)

        return kernel

    def _gaussian_blur(self, images: torch.Tensor) -> torch.Tensor:
        """Apply Gaussian blur."""
        batch_size, channels, height, width = images.shape
        padding = self.kernel_size // 2

        kernel = self.kernel.to(images.device)
        kernel = kernel.repeat(channels, 1, 1, 1)

        blurred = F.conv2d(
            images,
            kernel,
            padding=padding,
            groups=channels,
        )

        return blurred

    def _mean_filter(self, images: torch.Tensor) -> torch.Tensor:
        """Apply mean filter."""
        batch_size, channels, height, width = images.shape
        padding = self.kernel_size // 2

        # Mean kernel
        kernel = torch.ones(channels, 1, self.kernel_size, self.kernel_size, device=images.device)
        kernel = kernel / (self.kernel_size ** 2)

        filtered = F.conv2d(
            images,
            kernel,
            padding=padding,
            groups=channels,
        )

        return filtered

    def _median_filter(self, images: torch.Tensor) -> torch.Tensor:
        """Apply median filter (per-pixel approximation)."""
        padding = self.kernel_size // 2
        batch_size, channels, height, width = images.shape

        # Pad images
        padded = F.pad(images, [padding] * 4, mode="reflect")

        # Unfold to get local patches
        patches = padded.unfold(2, self.kernel_size, 1).unfold(3, self.kernel_size, 1)
        # Shape: (batch, channels, height, width, k, k)

        # Compute median
        patches_flat = patches.reshape(*patches.shape[:4], -1)
        median = patches_flat.median(dim=-1)[0]

        return median

    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply denoising defense.

        Args:
            images: Input images (potentially adversarial)

        Returns:
            Denoised images
        """
        images = images.to(self.device)

        if self.denoise_method == "gaussian":
            return self._gaussian_blur(images)
        elif self.denoise_method == "mean":
            return self._mean_filter(images)
        elif self.denoise_method == "median":
            return self._median_filter(images)
        else:
            raise ValueError(f"Unknown denoise method: {self.denoise_method}")


@register_defense("jpeg")
class JPEGDefense(InferenceDefense):
    """
    JPEG compression-based defense.

    Applies JPEG-like compression to remove high-frequency adversarial perturbations.
    """

    def __init__(
        self,
        model: nn.Module,
        quality: int = 75,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize JPEG defense.

        Args:
            model: The model to defend
            quality: JPEG quality (1-100, lower = more compression)
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.quality = quality

    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """
        Apply JPEG-like compression.

        This is a differentiable approximation of JPEG compression.
        """
        images = images.to(self.device)

        # Simple approximation: quantize then dequantize
        # Lower quality = more aggressive quantization
        levels = max(2, int(255 * self.quality / 100))

        # Quantize
        quantized = torch.round(images * levels) / levels

        # Ensure valid range
        quantized = torch.clamp(quantized, 0, 1)

        return quantized


@register_defense("randomization")
class RandomizationDefense(InferenceDefense):
    """
    Input randomization defense.

    Applies random transformations to break adversarial perturbations.
    """

    def __init__(
        self,
        model: nn.Module,
        resize_range: tuple = (0.9, 1.1),
        padding_range: tuple = (0, 4),
        n_samples: int = 10,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize randomization defense.

        Args:
            model: The model to defend
            resize_range: Range of resize scales (min, max)
            padding_range: Range of padding sizes (min, max)
            n_samples: Number of random samples to average
            device: Device to run on
        """
        super().__init__(model=model, device=device)
        self.resize_range = resize_range
        self.padding_range = padding_range
        self.n_samples = n_samples

    def _random_transform(self, images: torch.Tensor) -> torch.Tensor:
        """Apply random transformation."""
        batch_size, channels, height, width = images.shape

        # Random resize
        scale = torch.empty(1).uniform_(*self.resize_range).item()
        new_size = (int(height * scale), int(width * scale))

        resized = F.interpolate(images, size=new_size, mode="bilinear", align_corners=False)

        # Random padding to restore original size
        h_diff = height - new_size[0]
        w_diff = width - new_size[1]

        if h_diff > 0:
            pad_top = torch.randint(0, h_diff + 1, (1,)).item()
            pad_bottom = h_diff - pad_top
        else:
            pad_top = pad_bottom = 0
            resized = resized[:, :, :height, :]

        if w_diff > 0:
            pad_left = torch.randint(0, w_diff + 1, (1,)).item()
            pad_right = w_diff - pad_left
        else:
            pad_left = pad_right = 0
            resized = resized[:, :, :, :width]

        # Apply padding
        padded = F.pad(resized, [pad_left, pad_right, pad_top, pad_bottom])

        # Crop to original size if needed
        if padded.shape[2] > height or padded.shape[3] > width:
            padded = padded[:, :, :height, :width]

        return padded

    def defend(
        self,
        images: torch.Tensor,
    ) -> torch.Tensor:
        """Returns original images (transformation applied in apply())."""
        return images

    def apply(
        self,
        images: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Apply randomization defense with ensemble.

        Args:
            images: Input images
            labels: Not used

        Returns:
            Averaged logits from random transformations
        """
        images = images.to(self.device)
        self.model.eval()

        all_logits = []
        with torch.no_grad():
            for _ in range(self.n_samples):
                transformed = self._random_transform(images)
                logits = self.model(transformed)
                all_logits.append(logits)

        avg_logits = torch.stack(all_logits).mean(dim=0)
        return avg_logits
