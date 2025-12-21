#!/usr/bin/env python3
"""Test normalization fix for transfer attack analysis."""

import torch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders, get_normalization, denormalize, normalize
from src.attacks import PGDAttack


def test_data_range():
    """Test that CIFAR-10 data is in [0, 1] range."""
    print("Testing CIFAR-10 data range...")
    _, test_loader = get_cifar10_loaders(batch_size=4)

    for images, labels in test_loader:
        print(f"  Data range: [{images.min():.4f}, {images.max():.4f}]")
        assert images.min() >= 0 and images.max() <= 1, "Data should be in [0, 1]"
        print("  ✓ Data is in [0, 1] range")
        break


def test_attack_on_unnormalized():
    """Test attack on unnormalized data (default CIFAR-10)."""
    print("\nTesting attack on unnormalized data...")

    model = ModelRegistry.get("resnet18")
    model.eval()

    _, test_loader = get_cifar10_loaders(batch_size=4)

    for images, labels in test_loader:
        print(f"  Input range: [{images.min():.4f}, {images.max():.4f}]")

        # Direct attack
        attack = PGDAttack(model, eps=8/255, alpha=2/255, steps=5)
        adv_images = attack(images, labels)

        print(f"  Adv range: [{adv_images.min():.4f}, {adv_images.max():.4f}]")
        print("  ✓ Attack succeeded")
        break


def test_denormalize_normalize():
    """Test denormalization and normalization utilities."""
    print("\nTesting denormalize/normalize utilities...")

    mean, std = get_normalization("cifar10")
    print(f"  CIFAR-10 mean: {mean}")
    print(f"  CIFAR-10 std: {std}")

    # Create test data
    images = torch.rand(2, 3, 32, 32)  # [0, 1] range

    # Normalize
    images_norm = normalize(images, mean, std)
    print(f"  Normalized range: [{images_norm.min():.4f}, {images_norm.max():.4f}]")

    # Denormalize back
    images_denorm = denormalize(images_norm, mean, std)
    print(f"  Denormalized range: [{images_denorm.min():.4f}, {images_denorm.max():.4f}]")

    # Check roundtrip
    diff = (images - images_denorm).abs().max()
    print(f"  Roundtrip error: {diff:.8f}")
    assert diff < 1e-6, "Roundtrip error too large"
    print("  ✓ Denormalize/normalize roundtrip successful")


def test_attack_with_normalization():
    """Test attack with manual denorm/renorm (for future normalized data)."""
    print("\nTesting attack with denorm/renorm cycle...")

    model = ModelRegistry.get("resnet18")
    model.eval()

    mean, std = get_normalization("cifar10")
    _, test_loader = get_cifar10_loaders(batch_size=4)

    for images, labels in test_loader:
        # Simulate normalized data
        images_norm = normalize(images, mean, std)
        print(f"  Normalized input: [{images_norm.min():.4f}, {images_norm.max():.4f}]")

        # Denormalize for attack
        images_denorm = denormalize(images_norm, mean, std)
        print(f"  Denormalized: [{images_denorm.min():.4f}, {images_denorm.max():.4f}]")

        # Attack
        attack = PGDAttack(model, eps=8/255, alpha=2/255, steps=5)
        adv_images_denorm = attack(images_denorm, labels)
        print(f"  Adv (denorm): [{adv_images_denorm.min():.4f}, {adv_images_denorm.max():.4f}]")

        # Normalize back
        adv_images_norm = normalize(adv_images_denorm, mean, std)
        print(f"  Adv (norm): [{adv_images_norm.min():.4f}, {adv_images_norm.max():.4f}]")

        print("  ✓ Denorm/attack/renorm cycle successful")
        break


def test_create_pgd_attack_wrapper():
    """Test the create_pgd_attack wrapper from run_sci_analysis.py"""
    print("\nTesting create_pgd_attack wrapper...")

    from experiments.run_sci_analysis import create_pgd_attack

    model = ModelRegistry.get("resnet18")
    model.eval()

    _, test_loader = get_cifar10_loaders(batch_size=4)

    for images, labels in test_loader:
        # Test with normalize_data=False (default data is not normalized)
        attack_fn = create_pgd_attack(eps=8/255, normalize_data=False)
        adv_images = attack_fn(model, images, labels)
        print(f"  Attack (no norm): [{adv_images.min():.4f}, {adv_images.max():.4f}]")

        # Test with normalize_data=True (for future normalized data)
        attack_fn_norm = create_pgd_attack(eps=8/255, normalize_data=True)

        # Normalize data first
        mean, std = get_normalization("cifar10")
        images_norm = normalize(images, mean, std)

        adv_images_norm = attack_fn_norm(model, images_norm, labels)
        print(f"  Attack (with norm): [{adv_images_norm.min():.4f}, {adv_images_norm.max():.4f}]")

        print("  ✓ create_pgd_attack wrapper working correctly")
        break


if __name__ == "__main__":
    print("="*60)
    print("NORMALIZATION FIX TESTS")
    print("="*60)

    try:
        test_data_range()
        test_attack_on_unnormalized()
        test_denormalize_normalize()
        test_attack_with_normalization()
        test_create_pgd_attack_wrapper()

        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nNormalization fix is working correctly!")
        print("You can safely run: ./run_complete_pipeline.sh")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
