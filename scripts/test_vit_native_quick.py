#!/usr/bin/env python3
"""
Quick GPU Test for Native CIFAR-10 ViT

Verifies:
1. Model creation with native 32x32 resolution
2. Forward pass works correctly
3. Backward pass and gradient computation
4. Mini training loop (1 epoch, small batch)

Usage:
    python scripts/test_vit_native_quick.py
"""

import sys
import time
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def test_model_creation():
    """Test native ViT model creation."""
    print("=" * 60)
    print("Test 1: Model Creation")
    print("=" * 60)

    try:
        from src.models.vit import CIFARViT

        # Native CIFAR-10 configuration (32x32 with 4x4 patches)
        model = CIFARViT(
            img_size=32,
            patch_size=4,  # 8x8 = 64 patches
            in_chans=3,
            num_classes=10,
            embed_dim=192,
            depth=12,
            num_heads=3,
            mlp_ratio=4.0,
            drop_rate=0.1,
            attn_drop_rate=0.0,
        )

        num_params = sum(p.numel() for p in model.parameters())
        print(f"  Model created successfully")
        print(f"  Parameters: {num_params:,} ({num_params/1e6:.2f}M)")
        print(f"  Patch grid: 8x8 = 64 patches")
        print("  [PASS]")
        return model

    except Exception as e:
        print(f"  [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return None


def test_forward_pass(model):
    """Test forward pass with native resolution."""
    print("\n" + "=" * 60)
    print("Test 2: Forward Pass")
    print("=" * 60)

    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"  Device: {device}")

        model = model.to(device)
        model.eval()

        # Native 32x32 input
        x = torch.randn(4, 3, 32, 32).to(device)
        print(f"  Input shape: {x.shape}")

        with torch.no_grad():
            start = time.time()
            output = model(x)
            elapsed = time.time() - start

        print(f"  Output shape: {output.shape}")
        print(f"  Inference time: {elapsed*1000:.2f}ms")
        print("  [PASS]")
        return True

    except Exception as e:
        print(f"  [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backward_pass(model):
    """Test backward pass and gradient computation."""
    print("\n" + "=" * 60)
    print("Test 3: Backward Pass")
    print("=" * 60)

    try:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        model.train()

        x = torch.randn(4, 3, 32, 32).to(device)
        y = torch.randint(0, 10, (4,)).to(device)

        criterion = nn.CrossEntropyLoss()

        start = time.time()
        output = model(x)
        loss = criterion(output, y)
        loss.backward()
        elapsed = time.time() - start

        # Check gradients exist
        grad_norm = 0.0
        for p in model.parameters():
            if p.grad is not None:
                grad_norm += p.grad.norm().item() ** 2
        grad_norm = grad_norm ** 0.5

        print(f"  Loss: {loss.item():.4f}")
        print(f"  Gradient norm: {grad_norm:.4f}")
        print(f"  Backward time: {elapsed*1000:.2f}ms")
        print("  [PASS]")
        return True

    except Exception as e:
        print(f"  [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mini_training():
    """Test a mini training loop."""
    print("\n" + "=" * 60)
    print("Test 4: Mini Training Loop")
    print("=" * 60)

    try:
        from src.models.vit import CIFARViT

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Create fresh model
        model = CIFARViT(
            img_size=32,
            patch_size=4,
            in_chans=3,
            num_classes=10,
            embed_dim=192,
            depth=12,
            num_heads=3,
            mlp_ratio=4.0,
        ).to(device)
        model.train()

        optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.05)
        criterion = nn.CrossEntropyLoss()

        # Generate fake data
        num_batches = 10
        batch_size = 32

        total_loss = 0.0
        correct = 0
        total = 0

        start = time.time()
        for i in range(num_batches):
            x = torch.randn(batch_size, 3, 32, 32).to(device)
            y = torch.randint(0, 10, (batch_size,)).to(device)

            optimizer.zero_grad()
            output = model(x)
            loss = criterion(output, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()
            _, predicted = output.max(1)
            total += y.size(0)
            correct += predicted.eq(y).sum().item()

        elapsed = time.time() - start
        avg_loss = total_loss / num_batches
        accuracy = 100.0 * correct / total

        print(f"  Batches: {num_batches}")
        print(f"  Batch size: {batch_size}")
        print(f"  Avg loss: {avg_loss:.4f}")
        print(f"  Accuracy: {accuracy:.2f}%")
        print(f"  Total time: {elapsed:.2f}s")
        print(f"  Throughput: {num_batches * batch_size / elapsed:.1f} samples/s")
        print("  [PASS]")
        return True

    except Exception as e:
        print(f"  [FAIL] {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gpu_memory():
    """Report GPU memory usage."""
    print("\n" + "=" * 60)
    print("GPU Memory Status")
    print("=" * 60)

    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA version: {torch.version.cuda}")

        allocated = torch.cuda.memory_allocated() / 1024**2
        reserved = torch.cuda.memory_reserved() / 1024**2
        max_allocated = torch.cuda.max_memory_allocated() / 1024**2

        print(f"  Allocated: {allocated:.1f} MB")
        print(f"  Reserved: {reserved:.1f} MB")
        print(f"  Max allocated: {max_allocated:.1f} MB")

        # Clear cache
        torch.cuda.empty_cache()
        print("  Cache cleared")
    else:
        print("  No GPU available")


def main():
    print("\n" + "=" * 60)
    print("Native CIFAR-10 ViT Quick Test")
    print("=" * 60)
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # Run tests
    results = []

    model = test_model_creation()
    results.append(("Model Creation", model is not None))

    if model:
        results.append(("Forward Pass", test_forward_pass(model)))
        results.append(("Backward Pass", test_backward_pass(model)))

    results.append(("Mini Training", test_mini_training()))

    test_gpu_memory()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: [{status}]")
        if not passed:
            all_passed = False

    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
