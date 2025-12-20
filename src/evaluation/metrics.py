"""Evaluation metrics for adversarial robustness."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Optional, Dict, List
from tqdm import tqdm


def compute_accuracy(
    model: nn.Module,
    data_loader: DataLoader,
    device: Optional[torch.device] = None,
    verbose: bool = False,
) -> float:
    """
    Compute accuracy on a dataset.

    Args:
        model: Model to evaluate
        data_loader: Data loader
        device: Device to run on
        verbose: Whether to show progress bar

    Returns:
        Accuracy percentage
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    correct = 0
    total = 0

    iterator = data_loader
    if verbose:
        iterator = tqdm(iterator, desc="Evaluating")

    with torch.no_grad():
        for inputs, labels in iterator:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return 100.0 * correct / total


def compute_robustness(
    model: nn.Module,
    attack,
    data_loader: DataLoader,
    device: Optional[torch.device] = None,
    verbose: bool = False,
) -> float:
    """
    Compute robustness against an attack.

    Args:
        model: Model to evaluate
        attack: Attack function (takes images, labels -> adv_images)
        data_loader: Data loader
        device: Device to run on
        verbose: Whether to show progress bar

    Returns:
        Robust accuracy percentage
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    correct = 0
    total = 0

    iterator = data_loader
    if verbose:
        iterator = tqdm(iterator, desc="Evaluating robustness")

    for inputs, labels in iterator:
        inputs, labels = inputs.to(device), labels.to(device)

        # Generate adversarial examples
        adv_inputs = attack(inputs, labels)

        with torch.no_grad():
            outputs = model(adv_inputs)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    return 100.0 * correct / total


def compute_per_class_accuracy(
    model: nn.Module,
    data_loader: DataLoader,
    num_classes: int = 10,
    device: Optional[torch.device] = None,
) -> Dict[int, float]:
    """
    Compute per-class accuracy.

    Args:
        model: Model to evaluate
        data_loader: Data loader
        num_classes: Number of classes
        device: Device to run on

    Returns:
        Dictionary mapping class index to accuracy
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    class_correct = [0] * num_classes
    class_total = [0] * num_classes

    with torch.no_grad():
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            _, predicted = outputs.max(1)

            for i in range(len(labels)):
                label = labels[i].item()
                class_total[label] += 1
                if predicted[i] == label:
                    class_correct[label] += 1

    return {
        i: 100.0 * class_correct[i] / max(class_total[i], 1)
        for i in range(num_classes)
    }


def compute_attack_success_rate(
    model: nn.Module,
    attack,
    data_loader: DataLoader,
    device: Optional[torch.device] = None,
) -> float:
    """
    Compute attack success rate (percentage of correctly classified
    samples that become misclassified after attack).

    Args:
        model: Model to evaluate
        attack: Attack function
        data_loader: Data loader
        device: Device to run on

    Returns:
        Attack success rate percentage
    """
    if device is None:
        device = next(model.parameters()).device

    model.eval()
    originally_correct = 0
    attack_success = 0

    for inputs, labels in data_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        # Get original predictions
        with torch.no_grad():
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            correct_mask = predicted.eq(labels)
            originally_correct += correct_mask.sum().item()

        # Generate adversarial examples
        adv_inputs = attack(inputs, labels)

        # Get adversarial predictions
        with torch.no_grad():
            adv_outputs = model(adv_inputs)
            _, adv_predicted = adv_outputs.max(1)

            # Count successful attacks (correct -> incorrect)
            attack_success += (correct_mask & ~adv_predicted.eq(labels)).sum().item()

    if originally_correct == 0:
        return 0.0

    return 100.0 * attack_success / originally_correct


def compute_perturbation_statistics(
    clean_images: torch.Tensor,
    adv_images: torch.Tensor,
) -> Dict[str, float]:
    """
    Compute statistics about adversarial perturbations.

    Args:
        clean_images: Clean images
        adv_images: Adversarial images

    Returns:
        Dictionary with perturbation statistics
    """
    delta = adv_images - clean_images

    # Flatten for norm computation
    delta_flat = delta.view(delta.shape[0], -1)

    return {
        "l_inf": delta.abs().max().item(),
        "l_inf_mean": delta.abs().max(dim=1)[0].max(dim=1)[0].max(dim=1)[0].mean().item(),
        "l_2_mean": torch.norm(delta_flat, p=2, dim=1).mean().item(),
        "l_1_mean": torch.norm(delta_flat, p=1, dim=1).mean().item(),
        "l_0_mean": (delta_flat.abs() > 1e-6).float().sum(dim=1).mean().item(),
    }
