"""DeepFool attack implementation."""

import torch
import torch.nn as nn
from typing import Optional

from .base import BaseAttack
from .registry import register_attack


@register_attack("deepfool")
class DeepFoolAttack(BaseAttack):
    """
    DeepFool: A simple and accurate method to fool deep neural networks.

    Reference: Moosavi-Dezfooli et al., "DeepFool: a simple and accurate method to fool deep neural networks", CVPR 2016

    DeepFool finds the minimal perturbation that crosses the decision boundary
    by iteratively linearizing the classifier and computing the orthogonal
    projection to the nearest hyperplane.
    """

    def __init__(
        self,
        model: nn.Module,
        num_classes: int = 10,
        overshoot: float = 0.02,
        max_iter: int = 50,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize DeepFool attack.

        Args:
            model: The model to attack
            num_classes: Number of classes
            overshoot: Overshoot parameter to ensure crossing the boundary
            max_iter: Maximum number of iterations
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=float("inf"), targeted=False, device=device)
        self.num_classes = num_classes
        self.overshoot = overshoot
        self.max_iter = max_iter

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using DeepFool.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels
            target_labels: Not used for DeepFool

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)
        batch_size = images.shape[0]

        # Process each image individually
        adv_images = images.clone()

        for idx in range(batch_size):
            image = images[idx:idx + 1].clone()
            label = labels[idx].item()

            adv_image = self._deepfool_single(image, label)
            adv_images[idx] = adv_image[0]

        return adv_images

    def _deepfool_single(self, image: torch.Tensor, label: int) -> torch.Tensor:
        """
        DeepFool attack on a single image.

        Args:
            image: Single image tensor of shape (1, C, H, W)
            label: True label

        Returns:
            Adversarial image
        """
        image = image.clone().detach()
        original_image = image.clone()

        # Get initial prediction
        image.requires_grad = True
        output = self.model(image)
        pred = output.argmax(dim=1).item()

        # If already misclassified, return original
        if pred != label:
            return original_image

        # Total perturbation
        r_total = torch.zeros_like(image)

        for _ in range(self.max_iter):
            image = (original_image + r_total).detach().requires_grad_(True)
            output = self.model(image)

            # Check if misclassified
            pred = output.argmax(dim=1).item()
            if pred != label:
                break

            # Compute gradients for all classes
            grads = []
            for k in range(self.num_classes):
                if k == label:
                    continue

                self.model.zero_grad()
                if image.grad is not None:
                    image.grad.zero_()

                # Compute gradient of (f_k - f_label)
                output = self.model(image)
                diff = output[0, k] - output[0, label]
                diff.backward(retain_graph=True)

                grad_k = image.grad.clone()
                grads.append((k, grad_k, diff.item()))

            # Find the closest hyperplane
            min_pert = float("inf")
            best_pert = None

            for k, grad_k, f_diff in grads:
                # Compute perturbation for class k
                grad_norm = torch.norm(grad_k.flatten())

                if grad_norm > 1e-8:
                    pert = abs(f_diff) / (grad_norm ** 2 + 1e-8) * grad_k

                    pert_norm = torch.norm(pert.flatten())
                    if pert_norm < min_pert:
                        min_pert = pert_norm
                        best_pert = pert

            if best_pert is None:
                break

            # Update total perturbation
            r_total = r_total + best_pert

        # Apply overshoot and clamp
        adv_image = original_image + (1 + self.overshoot) * r_total
        adv_image = self._clamp(adv_image)

        return adv_image


@register_attack("deepfool_linf")
class DeepFoolLinfAttack(DeepFoolAttack):
    """
    DeepFool with Linf constraint.

    Clips the perturbation to the epsilon ball after each iteration.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        num_classes: int = 10,
        overshoot: float = 0.02,
        max_iter: int = 50,
        device: Optional[torch.device] = None,
    ):
        super().__init__(
            model=model,
            num_classes=num_classes,
            overshoot=overshoot,
            max_iter=max_iter,
            device=device,
        )
        self.eps = eps

    def _deepfool_single(self, image: torch.Tensor, label: int) -> torch.Tensor:
        """DeepFool with Linf constraint on a single image."""
        image = image.clone().detach()
        original_image = image.clone()
        r_total = torch.zeros_like(image)

        for _ in range(self.max_iter):
            image = (original_image + r_total).detach().requires_grad_(True)
            output = self.model(image)

            pred = output.argmax(dim=1).item()
            if pred != label:
                break

            grads = []
            for k in range(self.num_classes):
                if k == label:
                    continue

                self.model.zero_grad()
                if image.grad is not None:
                    image.grad.zero_()

                output = self.model(image)
                diff = output[0, k] - output[0, label]
                diff.backward(retain_graph=True)

                grad_k = image.grad.clone()
                grads.append((k, grad_k, diff.item()))

            min_pert = float("inf")
            best_pert = None

            for k, grad_k, f_diff in grads:
                grad_norm = torch.norm(grad_k.flatten())

                if grad_norm > 1e-8:
                    pert = abs(f_diff) / (grad_norm ** 2 + 1e-8) * grad_k
                    pert_norm = torch.norm(pert.flatten())

                    if pert_norm < min_pert:
                        min_pert = pert_norm
                        best_pert = pert

            if best_pert is None:
                break

            r_total = r_total + best_pert

            # Clip to Linf ball
            r_total = torch.clamp(r_total, -self.eps, self.eps)

        adv_image = original_image + (1 + self.overshoot) * r_total
        adv_image = self._project(adv_image, original_image, self.eps)

        return adv_image
