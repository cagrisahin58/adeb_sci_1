"""Data transforms for training and evaluation."""

import torch
import torchvision.transforms as T
from typing import Tuple


def get_train_transforms(
    crop_size: int = 32,
    padding: int = 4,
    horizontal_flip: bool = True,
) -> T.Compose:
    """
    Get training transforms for CIFAR-10/100.

    Args:
        crop_size: Size of random crop
        padding: Padding for random crop
        horizontal_flip: Whether to apply random horizontal flip

    Returns:
        Composed transforms
    """
    transforms_list = [
        T.RandomCrop(crop_size, padding=padding),
    ]

    if horizontal_flip:
        transforms_list.append(T.RandomHorizontalFlip())

    transforms_list.append(T.ToTensor())

    return T.Compose(transforms_list)


def get_test_transforms() -> T.Compose:
    """
    Get test transforms for CIFAR-10/100.

    Returns:
        Composed transforms
    """
    return T.Compose([
        T.ToTensor(),
    ])


def get_vit_train_transforms(
    input_size: int = 224,
    crop_size: int = 32,
) -> T.Compose:
    """
    Get training transforms for ViT models.

    ViT models typically require larger input sizes (224x224).

    Args:
        input_size: Target input size for ViT
        crop_size: Original crop size

    Returns:
        Composed transforms
    """
    return T.Compose([
        T.RandomCrop(crop_size, padding=4),
        T.RandomHorizontalFlip(),
        T.Resize(input_size),
        T.ToTensor(),
    ])


def get_vit_test_transforms(
    input_size: int = 224,
) -> T.Compose:
    """
    Get test transforms for ViT models.

    Args:
        input_size: Target input size for ViT

    Returns:
        Composed transforms
    """
    return T.Compose([
        T.Resize(input_size),
        T.ToTensor(),
    ])


def get_tta_transforms(
    crop_size: int = 32,
    n_crops: int = 10,
) -> T.Compose:
    """
    Get Test-Time Augmentation transforms.

    Args:
        crop_size: Size for crops
        n_crops: Number of crops (TenCrop gives 10)

    Returns:
        Composed transforms with TenCrop
    """
    return T.Compose([
        T.TenCrop(crop_size),
        T.Lambda(lambda crops: [T.ToTensor()(crop) for crop in crops]),
    ])


def get_normalization(
    dataset: str = "cifar10",
) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
    """
    Get normalization parameters for a dataset.

    Args:
        dataset: Dataset name ('cifar10', 'cifar100', 'imagenet')

    Returns:
        Tuple of (mean, std)
    """
    normalizations = {
        "cifar10": (
            (0.4914, 0.4822, 0.4465),
            (0.2023, 0.1994, 0.2010),
        ),
        "cifar100": (
            (0.5071, 0.4867, 0.4408),
            (0.2675, 0.2565, 0.2761),
        ),
        "imagenet": (
            (0.485, 0.456, 0.406),
            (0.229, 0.224, 0.225),
        ),
    }

    if dataset not in normalizations:
        raise ValueError(f"Unknown dataset: {dataset}")

    return normalizations[dataset]


def denormalize(tensor, mean, std):
    """
    Denormalize a tensor image.

    Args:
        tensor: Normalized image tensor (C, H, W) or (B, C, H, W)
        mean: Mean values per channel
        std: Std values per channel

    Returns:
        Denormalized tensor in [0, 1] range
    """
    if isinstance(mean, (list, tuple)):
        mean = torch.tensor(mean, dtype=tensor.dtype, device=tensor.device)
    if isinstance(std, (list, tuple)):
        std = torch.tensor(std, dtype=tensor.dtype, device=tensor.device)

    # Handle both (C, H, W) and (B, C, H, W)
    if tensor.ndim == 4:
        mean = mean.view(1, -1, 1, 1)
        std = std.view(1, -1, 1, 1)
    else:
        mean = mean.view(-1, 1, 1)
        std = std.view(-1, 1, 1)

    return tensor * std + mean


def normalize(tensor, mean, std):
    """
    Normalize a tensor image.

    Args:
        tensor: Image tensor in [0, 1] range (C, H, W) or (B, C, H, W)
        mean: Mean values per channel
        std: Std values per channel

    Returns:
        Normalized tensor
    """
    if isinstance(mean, (list, tuple)):
        mean = torch.tensor(mean, dtype=tensor.dtype, device=tensor.device)
    if isinstance(std, (list, tuple)):
        std = torch.tensor(std, dtype=tensor.dtype, device=tensor.device)

    # Handle both (C, H, W) and (B, C, H, W)
    if tensor.ndim == 4:
        mean = mean.view(1, -1, 1, 1)
        std = std.view(1, -1, 1, 1)
    else:
        mean = mean.view(-1, 1, 1)
        std = std.view(-1, 1, 1)

    return (tensor - mean) / std
