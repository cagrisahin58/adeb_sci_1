"""Tests for defense mechanisms."""

import pytest
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDefenseRegistry:
    """Tests for DefenseRegistry."""

    def test_list_defenses(self):
        from src.defenses import DefenseRegistry

        defenses = DefenseRegistry.list_defenses()
        assert "adversarial_training" in defenses
        assert "trades" in defenses
        assert "tta" in defenses

    def test_get_defense(self, resnet_model):
        from src.defenses import DefenseRegistry

        defense = DefenseRegistry.get("tta", model=resnet_model)
        assert defense is not None


class TestAdversarialTraining:
    """Tests for AdversarialTraining defense."""

    def test_get_loss(self, resnet_model, sample_batch):
        from src.defenses import AdversarialTraining

        model = resnet_model
        defense = AdversarialTraining(model, eps=8/255, steps=3)

        images, labels = sample_batch
        loss = defense.get_loss(model, images, labels)

        assert loss.item() > 0
        assert torch.isfinite(loss)

    def test_generate_adversarial(self, resnet_model, sample_batch):
        from src.defenses import AdversarialTraining

        model = resnet_model.eval()
        defense = AdversarialTraining(model, eps=8/255, steps=3)

        images, labels = sample_batch
        adv_images = defense.generate_adversarial(images, labels)

        assert adv_images.shape == images.shape


class TestTRADES:
    """Tests for TRADES defense."""

    def test_trades_loss(self, resnet_model, sample_batch):
        from src.defenses import TRADESDefense

        model = resnet_model
        defense = TRADESDefense(model, beta=6.0, eps=8/255, steps=3)

        images, labels = sample_batch
        loss = defense.get_loss(model, images, labels)

        assert loss.item() > 0
        assert torch.isfinite(loss)


class TestTTA:
    """Tests for Test-Time Augmentation defense."""

    def test_tta_output_shape(self, resnet_model, sample_batch):
        from src.defenses import TTADefense

        model = resnet_model.eval()
        defense = TTADefense(model, n_augmentations=5)

        images, labels = sample_batch
        output = defense(images, labels)

        assert output.shape == (4, 10)

    def test_tencrop_tta(self, resnet_model, sample_batch):
        from src.defenses import TenCropTTADefense

        model = resnet_model.eval()
        defense = TenCropTTADefense(model, crop_size=32)

        images, labels = sample_batch
        output = defense(images, labels)

        assert output.shape == (4, 10)


class TestPurification:
    """Tests for purification defenses."""

    def test_denoise_defense(self, resnet_model, sample_batch):
        from src.defenses import DenoisingDefense

        model = resnet_model.eval()
        defense = DenoisingDefense(model, denoise_method="gaussian")

        images, labels = sample_batch
        defended = defense.defend(images)

        assert defended.shape == images.shape
        assert defended.min() >= 0
        assert defended.max() <= 1

    def test_jpeg_defense(self, resnet_model, sample_batch):
        from src.defenses import JPEGDefense

        model = resnet_model.eval()
        defense = JPEGDefense(model, quality=75)

        images, labels = sample_batch
        defended = defense.defend(images)

        assert defended.shape == images.shape
