"""Tests for attack implementations."""

import pytest
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAttackRegistry:
    """Tests for AttackRegistry."""

    def test_list_attacks(self):
        from src.attacks import AttackRegistry

        attacks = AttackRegistry.list_attacks()
        assert "fgsm" in attacks
        assert "pgd" in attacks
        assert "deepfool" in attacks

    def test_get_attack(self, resnet_model):
        from src.attacks import AttackRegistry

        attack = AttackRegistry.get("fgsm", model=resnet_model)
        assert attack is not None


class TestFGSM:
    """Tests for FGSM attack."""

    def test_fgsm_output_shape(self, resnet_model, sample_batch):
        from src.attacks import FGSMAttack

        model = resnet_model.eval()
        attack = FGSMAttack(model, eps=8/255)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        assert adv_images.shape == images.shape

    def test_fgsm_perturbation_bounded(self, resnet_model, sample_batch):
        from src.attacks import FGSMAttack

        model = resnet_model.eval()
        eps = 8/255
        attack = FGSMAttack(model, eps=eps)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        perturbation = (adv_images - images).abs()
        assert perturbation.max() <= eps + 1e-6

    def test_fgsm_valid_range(self, resnet_model, sample_batch):
        from src.attacks import FGSMAttack

        model = resnet_model.eval()
        attack = FGSMAttack(model, eps=8/255)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        assert adv_images.min() >= 0
        assert adv_images.max() <= 1


class TestPGD:
    """Tests for PGD attack."""

    def test_pgd_output_shape(self, resnet_model, sample_batch):
        from src.attacks import PGDAttack

        model = resnet_model.eval()
        attack = PGDAttack(model, eps=8/255, alpha=2/255, steps=5)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        assert adv_images.shape == images.shape

    def test_pgd_perturbation_bounded(self, resnet_model, sample_batch):
        from src.attacks import PGDAttack

        model = resnet_model.eval()
        eps = 8/255
        attack = PGDAttack(model, eps=eps, alpha=2/255, steps=5)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        perturbation = (adv_images - images).abs()
        assert perturbation.max() <= eps + 1e-6

    def test_pgd_stronger_than_fgsm(self, resnet_model, sample_batch):
        """PGD should generally reduce accuracy more than FGSM."""
        from src.attacks import FGSMAttack, PGDAttack

        model = resnet_model.eval()
        eps = 8/255

        fgsm = FGSMAttack(model, eps=eps)
        pgd = PGDAttack(model, eps=eps, alpha=2/255, steps=10)

        images, labels = sample_batch

        # Get predictions
        with torch.no_grad():
            clean_pred = model(images).argmax(1)
            fgsm_pred = model(fgsm(images, labels)).argmax(1)
            pgd_pred = model(pgd(images, labels)).argmax(1)

        # Calculate success rates
        fgsm_success = (fgsm_pred != labels).float().mean()
        pgd_success = (pgd_pred != labels).float().mean()

        # PGD should be at least as effective
        assert pgd_success >= fgsm_success - 0.1  # Allow small tolerance


class TestDeepFool:
    """Tests for DeepFool attack."""

    def test_deepfool_output_shape(self, resnet_model, sample_batch):
        from src.attacks import DeepFoolAttack

        model = resnet_model.eval()
        attack = DeepFoolAttack(model, num_classes=10, max_iter=10)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        assert adv_images.shape == images.shape

    def test_deepfool_valid_range(self, resnet_model, sample_batch):
        from src.attacks import DeepFoolAttack

        model = resnet_model.eval()
        attack = DeepFoolAttack(model, num_classes=10, max_iter=10)

        images, labels = sample_batch
        adv_images = attack(images, labels)

        assert adv_images.min() >= 0
        assert adv_images.max() <= 1
