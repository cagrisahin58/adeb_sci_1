"""Pytest configuration and fixtures."""

import pytest
import torch
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def device():
    """Get device for tests."""
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@pytest.fixture
def sample_batch():
    """Sample CIFAR-10 batch for testing."""
    images = torch.rand(4, 3, 32, 32)
    labels = torch.randint(0, 10, (4,))
    return images, labels


@pytest.fixture
def sample_batch_gpu(sample_batch, device):
    """Sample batch on device."""
    images, labels = sample_batch
    return images.to(device), labels.to(device)


@pytest.fixture
def resnet_model():
    """Create a ResNet18 model for testing."""
    from src.models import ModelRegistry
    return ModelRegistry.get("resnet18")


@pytest.fixture
def resnet_model_gpu(resnet_model, device):
    """ResNet18 model on device."""
    return resnet_model.to(device)
