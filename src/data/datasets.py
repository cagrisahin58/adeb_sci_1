"""Dataset loaders for adversarial robustness evaluation."""

import torch
import torchvision
from torchvision import transforms as T
from torch.utils.data import DataLoader, Subset
from typing import Tuple, Optional


def get_cifar10_loaders(
    data_dir: str = "./data",
    batch_size: int = 128,
    test_batch_size: int = 100,
    num_workers: int = 2,
    train_transform: Optional[T.Compose] = None,
    test_transform: Optional[T.Compose] = None,
    download: bool = True,
    subset_size: Optional[int] = None,
) -> Tuple[DataLoader, DataLoader]:
    """
    Get CIFAR-10 train and test data loaders.

    Args:
        data_dir: Directory to store/load data
        batch_size: Training batch size
        test_batch_size: Test batch size
        num_workers: Number of data loading workers
        train_transform: Custom training transforms (None for default)
        test_transform: Custom test transforms (None for default)
        download: Whether to download the dataset
        subset_size: If specified, use only this many samples for testing

    Returns:
        Tuple of (train_loader, test_loader)
    """
    # Default transforms
    if train_transform is None:
        train_transform = T.Compose([
            T.RandomCrop(32, padding=4),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
        ])

    if test_transform is None:
        test_transform = T.Compose([
            T.ToTensor(),
        ])

    # Load datasets
    trainset = torchvision.datasets.CIFAR10(
        root=data_dir,
        train=True,
        download=download,
        transform=train_transform,
    )

    testset = torchvision.datasets.CIFAR10(
        root=data_dir,
        train=False,
        download=download,
        transform=test_transform,
    )

    # Create subset if specified
    if subset_size is not None and subset_size < len(testset):
        indices = torch.randperm(len(testset))[:subset_size].tolist()
        testset = Subset(testset, indices)

    # Create data loaders
    trainloader = DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    testloader = DataLoader(
        testset,
        batch_size=test_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return trainloader, testloader


def get_cifar10_loaders_with_val(
    data_dir: str = "./data",
    batch_size: int = 128,
    test_batch_size: int = 100,
    val_size: int = 2000,
    split_seed: int = 42,
    num_workers: int = 2,
    download: bool = True,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Get CIFAR-10 loaders with a held-out validation split for model selection.

    Egitim setinden sabit tohumlu bir permutasyonla `val_size` ornek ayrilir;
    validasyon augmentasyonsuz (ToTensor) degerlendirilir. Model secimi ve
    early stopping bu set uzerinden yapilarak test-set selection leakage
    onlenir (M7). Test seti yalnizca son degerlendirmede kullanilmalidir.

    Args:
        data_dir: Directory to store/load data
        batch_size: Training batch size
        test_batch_size: Validation/test batch size
        val_size: Number of training samples held out for validation
        split_seed: Seed for the fixed train/val permutation
        num_workers: Number of data loading workers
        download: Whether to download the dataset

    Returns:
        Tuple of (train_loader, val_loader, test_loader)
    """
    train_transform = T.Compose([
        T.RandomCrop(32, padding=4),
        T.RandomHorizontalFlip(),
        T.ToTensor(),
    ])
    eval_transform = T.Compose([
        T.ToTensor(),
    ])

    # Ayni goruntuler, farkli transformlar: iki dataset ornegi gerekir
    train_aug_set = torchvision.datasets.CIFAR10(
        root=data_dir, train=True, download=download, transform=train_transform,
    )
    train_eval_set = torchvision.datasets.CIFAR10(
        root=data_dir, train=True, download=False, transform=eval_transform,
    )
    testset = torchvision.datasets.CIFAR10(
        root=data_dir, train=False, download=download, transform=eval_transform,
    )

    generator = torch.Generator().manual_seed(split_seed)
    perm = torch.randperm(len(train_aug_set), generator=generator).tolist()
    val_indices = perm[:val_size]
    train_indices = perm[val_size:]

    trainloader = DataLoader(
        Subset(train_aug_set, train_indices),
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    valloader = DataLoader(
        Subset(train_eval_set, val_indices),
        batch_size=test_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )
    testloader = DataLoader(
        testset,
        batch_size=test_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return trainloader, valloader, testloader


def get_cifar100_loaders(
    data_dir: str = "./data",
    batch_size: int = 128,
    test_batch_size: int = 100,
    num_workers: int = 2,
    train_transform: Optional[T.Compose] = None,
    test_transform: Optional[T.Compose] = None,
    download: bool = True,
) -> Tuple[DataLoader, DataLoader]:
    """
    Get CIFAR-100 train and test data loaders.

    Args:
        data_dir: Directory to store/load data
        batch_size: Training batch size
        test_batch_size: Test batch size
        num_workers: Number of data loading workers
        train_transform: Custom training transforms
        test_transform: Custom test transforms
        download: Whether to download the dataset

    Returns:
        Tuple of (train_loader, test_loader)
    """
    if train_transform is None:
        train_transform = T.Compose([
            T.RandomCrop(32, padding=4),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
        ])

    if test_transform is None:
        test_transform = T.Compose([
            T.ToTensor(),
        ])

    trainset = torchvision.datasets.CIFAR100(
        root=data_dir,
        train=True,
        download=download,
        transform=train_transform,
    )

    testset = torchvision.datasets.CIFAR100(
        root=data_dir,
        train=False,
        download=download,
        transform=test_transform,
    )

    trainloader = DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    testloader = DataLoader(
        testset,
        batch_size=test_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    return trainloader, testloader


# CIFAR-10 class names
CIFAR10_CLASSES = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# CIFAR-100 class names (superclasses)
CIFAR100_SUPERCLASSES = [
    'aquatic_mammals', 'fish', 'flowers', 'food_containers',
    'fruit_and_vegetables', 'household_electrical_devices',
    'household_furniture', 'insects', 'large_carnivores',
    'large_man-made_outdoor_things', 'large_natural_outdoor_scenes',
    'large_omnivores_and_herbivores', 'medium_mammals',
    'non-insect_invertebrates', 'people', 'reptiles',
    'small_mammals', 'trees', 'vehicles_1', 'vehicles_2'
]
