#!/usr/bin/env python3
"""AutoAttack evaluation - gold standard robustness evaluation."""

import torch
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import gc

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders
from src.utils.checkpoint import load_model_weights

try:
    from autoattack import AutoAttack
    AUTOATTACK_AVAILABLE = True
except ImportError:
    AUTOATTACK_AVAILABLE = False
    print("WARNING: AutoAttack not available")


def clear_gpu():
    """Clear GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()


def evaluate_with_autoattack(model, test_loader, device, eps=8/255, n_samples=500, batch_size=100):
    """Evaluate model with AutoAttack."""

    model.eval()

    # Collect samples
    all_images = []
    all_labels = []
    total = 0

    for images, labels in test_loader:
        all_images.append(images)
        all_labels.append(labels)
        total += images.size(0)
        if total >= n_samples:
            break

    images = torch.cat(all_images, dim=0)[:n_samples]
    labels = torch.cat(all_labels, dim=0)[:n_samples]

    images = images.to(device)
    labels = labels.to(device)

    # Clean accuracy
    with torch.no_grad():
        outputs = model(images)
        clean_correct = (outputs.argmax(1) == labels).sum().item()

    clean_acc = 100 * clean_correct / len(labels)
    print(f"  Clean accuracy: {clean_acc:.2f}%")

    # AutoAttack
    adversary = AutoAttack(model, norm='Linf', eps=eps, version='standard', verbose=True)

    # Run evaluation
    adv_images = adversary.run_standard_evaluation(images, labels, bs=batch_size)

    # Robust accuracy
    with torch.no_grad():
        adv_outputs = model(adv_images)
        robust_correct = (adv_outputs.argmax(1) == labels).sum().item()

    robust_acc = 100 * robust_correct / len(labels)

    return {
        'n_samples': len(labels),
        'clean_accuracy': clean_acc,
        'robust_accuracy': robust_acc,
        'clean_correct': clean_correct,
        'robust_correct': robust_correct,
    }


def main():
    if not AUTOATTACK_AVAILABLE:
        print("AutoAttack not available. Skipping evaluation.")
        return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    output_dir = Path("results/autoattack_evaluation_20260110")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading CIFAR-10...")
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=100)

    # Model configs - AT models
    models_config = [
        ("ResNet18_AT", "resnet18", "models/resnet18/adv/adversarial_training/best.pth"),
        ("ViT_Tiny_AT", "vit_tiny", "models/vit_tiny/adv/adversarial_training/best.pth"),
    ]

    eps = 8/255
    n_samples = 500  # AutoAttack is slow, use fewer samples
    batch_size = 100

    results = []

    for name, model_type, model_path in models_config:
        print(f"\n{'='*60}")
        print(f"Evaluating: {name}")
        print(f"{'='*60}")

        clear_gpu()

        # Load model
        model = ModelRegistry.get(model_type)
        load_model_weights(model, model_path, device)
        model = model.to(device)
        model.eval()

        # Evaluate
        result = evaluate_with_autoattack(
            model, test_loader, device,
            eps=eps, n_samples=n_samples, batch_size=batch_size
        )
        result['model'] = name
        result['model_type'] = model_type
        result['eps'] = eps
        results.append(result)

        print(f"\n  Results for {name}:")
        print(f"    Clean Accuracy: {result['clean_accuracy']:.2f}%")
        print(f"    AutoAttack Accuracy: {result['robust_accuracy']:.2f}%")

        del model
        clear_gpu()

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_dir / "autoattack_results.csv", index=False)

    summary = {
        'timestamp': datetime.now().isoformat(),
        'eps': eps,
        'n_samples': n_samples,
        'results': results,
    }

    with open(output_dir / "autoattack_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "="*60)
    print("AUTOATTACK EVALUATION SUMMARY")
    print("="*60)
    print(f"\nEpsilon: {eps:.4f} ({eps*255:.0f}/255)")
    print(f"Samples: {n_samples}")
    print("\n" + "-"*50)
    print(f"{'Model':<20} {'Clean':<12} {'AutoAttack':<12}")
    print("-"*50)

    for r in results:
        print(f"{r['model']:<20} {r['clean_accuracy']:.2f}%{'':<6} {r['robust_accuracy']:.2f}%")

    print("-"*50)
    print(f"\nResults saved to {output_dir}")


if __name__ == "__main__":
    main()
