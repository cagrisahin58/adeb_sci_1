"""Carlini & Wagner (C&W) attack implementation."""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Optional

from .base import BaseAttack
from .registry import register_attack


@register_attack("cw")
class CWAttack(BaseAttack):
    """
    Carlini & Wagner L2 Attack.

    Reference: Carlini & Wagner, "Towards Evaluating the Robustness of Neural Networks", IEEE S&P 2017

    This is an optimization-based attack that minimizes the L2 perturbation
    while ensuring misclassification.
    """

    def __init__(
        self,
        model: nn.Module,
        c: float = 1.0,
        kappa: float = 0.0,
        steps: int = 1000,
        lr: float = 0.01,
        binary_search_steps: int = 9,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        """
        Initialize C&W attack.

        Args:
            model: The model to attack
            c: Initial constant for balancing loss terms
            kappa: Confidence parameter (higher = stronger attack)
            steps: Number of optimization steps
            lr: Learning rate for optimizer
            binary_search_steps: Number of binary search steps for c
            targeted: Whether the attack is targeted
            device: Device to run the attack on
        """
        super().__init__(model=model, eps=float("inf"), targeted=targeted, device=device)
        self.c = c
        self.kappa = kappa
        self.steps = steps
        self.lr = lr
        self.binary_search_steps = binary_search_steps

    def _arctanh(self, x: torch.Tensor) -> torch.Tensor:
        """Inverse hyperbolic tangent."""
        return 0.5 * torch.log((1 + x) / (1 - x + 1e-8) + 1e-8)

    def _f(self, outputs: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        """
        Compute the f function from the C&W paper.

        f(x') = max(max{Z(x')_i : i != t} - Z(x')_t, -kappa)
        """
        one_hot = torch.zeros_like(outputs)
        one_hot.scatter_(1, labels.unsqueeze(1), 1)

        # Get the logit of the true class
        real = (one_hot * outputs).sum(dim=1)

        # Get the maximum logit of other classes
        other = ((1 - one_hot) * outputs - one_hot * 1e4).max(dim=1)[0]

        if self.targeted:
            # For targeted: we want the target class to be higher
            return torch.clamp(other - real, min=-self.kappa)
        else:
            # For untargeted: we want the true class to be lower
            return torch.clamp(real - other, min=-self.kappa)

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Generate adversarial examples using C&W attack.

        Args:
            images: Clean images of shape (batch_size, channels, height, width)
            labels: True labels (or target labels for targeted attack)
            target_labels: Target labels for targeted attacks

        Returns:
            Adversarial images
        """
        images, labels = self._check_inputs(images, labels)
        batch_size = images.shape[0]

        if self.targeted and target_labels is not None:
            labels = target_labels.to(self.device)

        # Initialize in tanh space
        # x = 0.5 * (tanh(w) + 1), so w = arctanh(2x - 1)
        images_tanh = self._arctanh(images * 2 - 1)

        # Binary search for optimal c
        c_lower = torch.zeros(batch_size, device=self.device)
        c_upper = torch.ones(batch_size, device=self.device) * 1e10
        c = torch.ones(batch_size, device=self.device) * self.c

        best_adv = images.clone()
        best_l2 = torch.full((batch_size,), float("inf"), device=self.device)

        for _ in range(self.binary_search_steps):
            # Initialize perturbation
            w = images_tanh.clone().detach().requires_grad_(True)
            optimizer = optim.Adam([w], lr=self.lr)

            for _ in range(self.steps):
                optimizer.zero_grad()

                # Convert from tanh space to image space
                adv_images = 0.5 * (torch.tanh(w) + 1)

                # Compute L2 distance
                l2_dist = ((adv_images - images) ** 2).view(batch_size, -1).sum(dim=1)

                # Compute classification loss
                outputs = self.model(adv_images)
                f_loss = self._f(outputs, labels)

                # Total loss
                loss = l2_dist.sum() + (c * f_loss).sum()

                loss.backward()
                optimizer.step()

            # Evaluate final adversarial examples
            with torch.no_grad():
                adv_images = 0.5 * (torch.tanh(w) + 1)
                outputs = self.model(adv_images)
                preds = outputs.argmax(dim=1)

                # Check success
                if self.targeted:
                    success = preds == labels
                else:
                    success = preds != labels

                l2_dist = ((adv_images - images) ** 2).view(batch_size, -1).sum(dim=1).sqrt()

                # Update best adversarial examples
                improved = success & (l2_dist < best_l2)
                best_adv[improved] = adv_images[improved]
                best_l2[improved] = l2_dist[improved]

                # Update c for binary search
                c_upper[success] = torch.min(c_upper[success], c[success])
                c_lower[~success] = torch.max(c_lower[~success], c[~success])

                # Update c
                is_upper_finite = c_upper < 1e9
                c[is_upper_finite] = (c_lower[is_upper_finite] + c_upper[is_upper_finite]) / 2
                c[~is_upper_finite] = c[~is_upper_finite] * 10

        return best_adv


@register_attack("cw_linf")
class CWLinfAttack(BaseAttack):
    """
    C&W-style attack with Linf constraint.

    Uses the same optimization objective but projects to Linf ball.
    """

    def __init__(
        self,
        model: nn.Module,
        eps: float = 8 / 255,
        c: float = 1.0,
        kappa: float = 0.0,
        steps: int = 100,
        lr: float = 0.01,
        targeted: bool = False,
        device: Optional[torch.device] = None,
    ):
        super().__init__(model=model, eps=eps, targeted=targeted, device=device)
        self.c = c
        self.kappa = kappa
        self.steps = steps
        self.lr = lr

    def _f(self, outputs: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        one_hot = torch.zeros_like(outputs)
        one_hot.scatter_(1, labels.unsqueeze(1), 1)
        real = (one_hot * outputs).sum(dim=1)
        other = ((1 - one_hot) * outputs - one_hot * 1e4).max(dim=1)[0]

        if self.targeted:
            return torch.clamp(other - real, min=-self.kappa)
        else:
            return torch.clamp(real - other, min=-self.kappa)

    def attack(
        self,
        images: torch.Tensor,
        labels: torch.Tensor,
        target_labels: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        images, labels = self._check_inputs(images, labels)
        batch_size = images.shape[0]

        if self.targeted and target_labels is not None:
            labels = target_labels.to(self.device)

        # Initialize perturbation
        delta = torch.zeros_like(images, requires_grad=True)
        optimizer = optim.Adam([delta], lr=self.lr)

        for _ in range(self.steps):
            optimizer.zero_grad()

            adv_images = self._clamp(images + delta)

            outputs = self.model(adv_images)
            f_loss = self._f(outputs, labels)

            # Minimize f_loss (misclassification objective)
            loss = (self.c * f_loss).sum()

            loss.backward()
            optimizer.step()

            # Project to Linf ball
            with torch.no_grad():
                delta.data = torch.clamp(delta.data, -self.eps, self.eps)
                delta.data = torch.clamp(images + delta.data, 0, 1) - images

        return self._clamp(images + delta.detach())
