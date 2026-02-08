#!/usr/bin/env python3
"""Simple transfer attack analysis - memory efficient."""

import torch
import torch.nn.functional as F
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


def evaluate_accuracy(model, data_loader, device, max_batches=10):
    """Evaluate model accuracy."""
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for i, (images, labels) in enumerate(data_loader):
            if i >= max_batches:
                break
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return 100. * correct / total


def generate_adversarial(model, images, labels, attack, device):
    """Generate adversarial examples."""
    model.eval()
    adv_images = attack(images, labels)
    return adv_images


def transfer_attack(source_model, target_model, data_loader, attack, device, max_batches=10):
    """Measure transfer attack success rate."""
    source_model.eval()
    target_model.eval()

    total = 0
    source_success = 0
    transfer_success = 0

    for i, (images, labels) in enumerate(data_loader):
        if i >= max_batches:
            break

        images, labels = images.to(device), labels.to(device)

        # Generate adversarial examples using source model
        adv_images = generate_adversarial(source_model, images, labels, attack, device)

        # Evaluate on source model
        with torch.no_grad():
            source_outputs = source_model(adv_images)
            _, source_pred = source_outputs.max(1)
            source_success += (source_pred != labels).sum().item()

        # Evaluate on target model
        with torch.no_grad():
            target_outputs = target_model(adv_images)
            _, target_pred = target_outputs.max(1)
            transfer_success += (target_pred != labels).sum().item()

        total += labels.size(0)

    source_rate = 100. * source_success / total
    transfer_rate = 100. * transfer_success / total

    return source_rate, transfer_rate


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    output_dir = Path("results/transfer_analysis_20260110")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    print("\nLoading CIFAR-10...")
    _, test_loader = get_cifar10_loaders(data_dir='./data', test_batch_size=50)

    # Model configs - only AT models
    models_config = [
        ("ResNet18_AT", "resnet18", "models/resnet18/adv/adversarial_training/best.pth"),
        ("ViT_Tiny_AT", "vit_tiny", "models/vit_tiny/adv/adversarial_training/best.pth"),
    ]

    # Attack config
    eps = 8/255
    alpha = 2/255
    steps = 10

    results = []

    # Pairwise transfer attacks
    for i, (source_name, source_type, source_path) in enumerate(models_config):
        print(f"\n{'='*60}")
        print(f"Source Model: {source_name}")
        print(f"{'='*60}")

        # Load source model
        clear_gpu()
        source_model = ModelRegistry.get(source_type)
        load_model_weights(source_model, source_path, device)
        source_model = source_model.to(device)
        source_model.eval()

        # Create attack
        attack = PGDAttack(source_model, eps=eps, alpha=alpha, steps=steps)

        for j, (target_name, target_type, target_path) in enumerate(models_config):
            print(f"\n  Target: {target_name}")

            if i == j:
                # Same model - just measure attack success
                clear_gpu()
                target_model = source_model
                source_rate, _ = transfer_attack(source_model, target_model, test_loader, attack, device, max_batches=20)
                print(f"    Attack Success Rate: {source_rate:.2f}%")
                results.append({
                    'source': source_name,
                    'target': target_name,
                    'attack_success': source_rate,
                    'transfer_rate': source_rate,
                    'is_self': True
                })
            else:
                # Load target model
                clear_gpu()
                target_model = ModelRegistry.get(target_type)
                load_model_weights(target_model, target_path, device)
                target_model = target_model.to(device)
                target_model.eval()

                source_rate, transfer_rate = transfer_attack(
                    source_model, target_model, test_loader, attack, device, max_batches=20
                )

                print(f"    Source Attack Success: {source_rate:.2f}%")
                print(f"    Transfer Success: {transfer_rate:.2f}%")
                print(f"    Transfer Rate: {100*transfer_rate/source_rate:.1f}% of source")

                results.append({
                    'source': source_name,
                    'target': target_name,
                    'attack_success': source_rate,
                    'transfer_rate': transfer_rate,
                    'is_self': False
                })

                del target_model
                clear_gpu()

        del source_model
        del attack
        clear_gpu()

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_dir / "transfer_results.csv", index=False)

    # Create transfer matrix
    print("\n" + "="*60)
    print("TRANSFER ATTACK MATRIX")
    print("="*60)

    models = [m[0] for m in models_config]
    matrix = np.zeros((len(models), len(models)))

    for r in results:
        i = models.index(r['source'])
        j = models.index(r['target'])
        matrix[i, j] = r['transfer_rate']

    print("\nTransfer Success Rate (%):")
    print(f"{'Source/Target':<15}", end="")
    for m in models:
        print(f"{m:<15}", end="")
    print()

    for i, source in enumerate(models):
        print(f"{source:<15}", end="")
        for j in range(len(models)):
            print(f"{matrix[i,j]:.1f}%{'':<10}", end="")
        print()

    # Save matrix
    np.save(output_dir / "transfer_matrix.npy", matrix)

    with open(output_dir / "transfer_summary.json", 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'models': models,
            'matrix': matrix.tolist(),
            'eps': eps,
            'steps': steps
        }, f, indent=2)

    print(f"\nResults saved to {output_dir}")
    print("\nKey Findings:")

    # Analyze asymmetry
    if len(models) >= 2:
        cnn_to_vit = matrix[0, 1]  # ResNet -> ViT
        vit_to_cnn = matrix[1, 0]  # ViT -> ResNet
        print(f"  CNN → ViT transfer: {cnn_to_vit:.1f}%")
        print(f"  ViT → CNN transfer: {vit_to_cnn:.1f}%")
        print(f"  Asymmetry: {abs(cnn_to_vit - vit_to_cnn):.1f}%")


if __name__ == "__main__":
    main()
