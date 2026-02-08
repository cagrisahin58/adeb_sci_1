#!/usr/bin/env python3
"""Statistical validation - run evaluations with different seeds."""

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
from src.attacks import PGDAttack
from src.utils.checkpoint import load_model_weights


def clear_gpu():
    """Clear GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()


def set_seed(seed):
    """Set random seed for reproducibility."""
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)


def evaluate_model(model, test_loader, attack, device, n_samples=1000):
    """Evaluate model under attack."""
    model.eval()

    clean_correct = 0
    robust_correct = 0
    total = 0

    for images, labels in test_loader:
        if total >= n_samples:
            break

        images, labels = images.to(device), labels.to(device)
        batch_size = images.size(0)

        # Clean accuracy
        with torch.no_grad():
            clean_outputs = model(images)
            clean_correct += (clean_outputs.argmax(1) == labels).sum().item()

        # Generate adversarial examples
        adv_images = attack(images, labels)

        # Robust accuracy
        with torch.no_grad():
            adv_outputs = model(adv_images)
            robust_correct += (adv_outputs.argmax(1) == labels).sum().item()

        total += batch_size

    return {
        'clean_acc': 100 * clean_correct / total,
        'robust_acc': 100 * robust_correct / total,
        'n_samples': total
    }


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    output_dir = Path("results/statistical_validation_20260110")
    output_dir.mkdir(parents=True, exist_ok=True)

    seeds = [42, 123, 456]
    n_samples = 1000
    eps = 8/255
    alpha = 2/255
    steps = 10

    # Models to evaluate
    models_config = [
        ("ResNet18_AT", "resnet18", "models/resnet18/adv/adversarial_training/best.pth"),
        ("ViT_Tiny_AT", "vit_tiny", "models/vit_tiny/adv/adversarial_training/best.pth"),
    ]

    all_results = []

    for name, model_type, model_path in models_config:
        print(f"\n{'='*60}")
        print(f"Model: {name}")
        print(f"{'='*60}")

        model_results = []

        for seed in seeds:
            print(f"\n  Seed: {seed}")
            set_seed(seed)
            clear_gpu()

            # Load data with this seed
            _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=100)

            # Load model
            model = ModelRegistry.get(model_type)
            load_model_weights(model, model_path, device)
            model = model.to(device)
            model.eval()

            # Create attack
            attack = PGDAttack(model, eps=eps, alpha=alpha, steps=steps)

            # Evaluate
            result = evaluate_model(model, test_loader, attack, device, n_samples)
            result['seed'] = seed
            result['model'] = name
            model_results.append(result)

            print(f"    Clean: {result['clean_acc']:.2f}%")
            print(f"    Robust: {result['robust_acc']:.2f}%")

            del model
            del attack
            clear_gpu()

        # Compute statistics
        clean_accs = [r['clean_acc'] for r in model_results]
        robust_accs = [r['robust_acc'] for r in model_results]

        summary = {
            'model': name,
            'clean_mean': np.mean(clean_accs),
            'clean_std': np.std(clean_accs),
            'robust_mean': np.mean(robust_accs),
            'robust_std': np.std(robust_accs),
            'n_runs': len(seeds),
            'n_samples': n_samples,
        }
        all_results.append(summary)

        print(f"\n  Summary:")
        print(f"    Clean: {summary['clean_mean']:.2f} ± {summary['clean_std']:.2f}%")
        print(f"    Robust: {summary['robust_mean']:.2f} ± {summary['robust_std']:.2f}%")

    # Save results
    df = pd.DataFrame(all_results)
    df.to_csv(output_dir / "statistical_summary.csv", index=False)

    with open(output_dir / "statistical_validation.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'seeds': seeds,
            'n_samples': n_samples,
            'eps': eps,
            'results': all_results
        }, f, indent=2)

    print("\n" + "="*60)
    print("STATISTICAL VALIDATION SUMMARY")
    print("="*60)
    print(f"\nSeeds: {seeds}")
    print(f"Samples per run: {n_samples}")
    print(f"Attack: PGD-{steps} (eps={eps:.4f})")
    print("\n" + "-"*50)
    print(f"{'Model':<20} {'Clean':<15} {'Robust (PGD)':<15}")
    print("-"*50)

    for r in all_results:
        clean_str = f"{r['clean_mean']:.2f} ± {r['clean_std']:.2f}"
        robust_str = f"{r['robust_mean']:.2f} ± {r['robust_std']:.2f}"
        print(f"{r['model']:<20} {clean_str:<15} {robust_str:<15}")

    print("-"*50)
    print(f"\nResults saved to {output_dir}")


if __name__ == "__main__":
    main()
