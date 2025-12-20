"""Tests for model architectures."""

import pytest
import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestModelRegistry:
    """Tests for ModelRegistry."""

    def test_list_models(self):
        from src.models import ModelRegistry

        models = ModelRegistry.list_models()
        assert "resnet18" in models
        assert "vit_tiny" in models
        assert "densenet121" in models

    def test_get_model(self):
        from src.models import ModelRegistry

        model = ModelRegistry.get("resnet18")
        assert model is not None

    def test_get_unknown_model(self):
        from src.models import ModelRegistry

        with pytest.raises(ValueError):
            ModelRegistry.get("unknown_model")


class TestResNet:
    """Tests for ResNet models."""

    def test_resnet18_forward_shape(self, sample_batch):
        from src.models import CIFAR10ResNet18

        model = CIFAR10ResNet18()
        images, _ = sample_batch
        output = model(images)

        assert output.shape == (4, 10)

    def test_resnet18_cifar_adaptation(self):
        from src.models import CIFAR10ResNet18

        model = CIFAR10ResNet18()

        # Check CIFAR-10 adaptations
        assert model.model.conv1.kernel_size == (3, 3)
        assert isinstance(model.model.maxpool, torch.nn.Identity)

    def test_count_parameters(self):
        from src.models import CIFAR10ResNet18

        model = CIFAR10ResNet18()
        params = model.count_parameters()

        assert params > 0
        assert params < 20_000_000  # ResNet18 should be under 20M params


class TestViT:
    """Tests for ViT models."""

    def test_vit_tiny_forward_shape(self, sample_batch):
        pytest.importorskip("timm")
        from src.models import CIFAR10ViTTiny

        model = CIFAR10ViTTiny()
        images, _ = sample_batch
        output = model(images)

        assert output.shape == (4, 10)


class TestDenseNet:
    """Tests for DenseNet models."""

    def test_densenet121_forward_shape(self, sample_batch):
        from src.models import CIFAR10DenseNet121

        model = CIFAR10DenseNet121()
        images, _ = sample_batch
        output = model(images)

        assert output.shape == (4, 10)
