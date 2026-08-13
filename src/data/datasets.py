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
    val_indices_path: str = None,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Get CIFAR-10 loaders with a held-out validation split for model selection.

    Egitim setinden sabit tohumlu bir permutasyonla `val_size` ornek ayrilir;
    validasyon augmentasyonsuz (ToTensor) degerlendirilir. Model secimi ve
    early stopping bu set uzerinden yapilarak test-set selection leakage
    onlenir (M7). Test seti yalnizca son degerlendirmede kullanilmalidir.

    rev2 C1 (leak fix): `val_indices_path` verilirse split, seed'den TUREMEZ;
    JSON dosyasindaki sabit indeks listesi kullanilir. Boylece (1) tum egitim
    seed'leri AYNI validasyon setini paylasir, (2) ayni indeks dosyasi clean
    pretraining'de de kullanilarak validasyon orneklerinin pretraining'de
    gorulmesi engellenir.

    Args:
        data_dir: Directory to store/load data
        batch_size: Training batch size
        test_batch_size: Validation/test batch size
        val_size: Number of training samples held out for validation
        split_seed: Seed for the fixed train/val permutation
        num_workers: Number of data loading workers
        download: Whether to download the dataset
        val_indices_path: Sabit validasyon indeksleri JSON dosyasi (opsiyonel;
            {"val_indices": [...]} formati). Verilirse val_size/split_seed
            yoksayilir.

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

    if val_indices_path is not None:
        import json as _json
        with open(val_indices_path) as _f:
            _payload = _json.load(_f)
        val_indices = list(_payload["val_indices"])
        _val_set = set(val_indices)
        if len(_val_set) != len(val_indices):
            raise ValueError(f"{val_indices_path}: tekrarli indeks var")
        if any(i < 0 or i >= len(train_aug_set) for i in _val_set):
            raise ValueError(f"{val_indices_path}: indeks araligi disi deger var")
        train_indices = [i for i in range(len(train_aug_set)) if i not in _val_set]
    else:
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


# ============================================================================
# Q1 genisletmesi: dataset-parametrik generic loaders
# ============================================================================
# Mevcut get_cifar10_* fonksiyonlarina DOKUNULMAZ (27 dosya import ediyor);
# yeni kod generic yolu kullanir. Normalizasyon YOKTUR: tum modeller [0,1]
# ham piksel girdisi tuketir (saldiri tabani src/attacks bunu varsayar).

DATASETS = {
    "cifar10": {
        "cls": "CIFAR10", "num_classes": 10, "n_train": 50000, "n_test": 10000,
        "img_size": 32, "flip": True,
    },
    "cifar100": {
        "cls": "CIFAR100", "num_classes": 100, "n_train": 50000, "n_test": 10000,
        "img_size": 32, "flip": True,
    },
    # SVHN: rakam siniflari - yatay cevirme ANLAMSIZ (flip kapali);
    # extra-604k split'i BILEREK kullanilmaz (literatur karsilastirilabilirligi)
    "svhn": {
        "cls": "SVHN", "num_classes": 10, "n_train": 73257, "n_test": 26032,
        "img_size": 32, "flip": False,
    },
}


def _make_dataset(name: str, data_dir: str, train: bool, transform, download: bool):
    """torchvision dataset fabrikasi (SVHN'in train/split imza farkini gizler)."""
    spec = DATASETS[name]
    cls = getattr(torchvision.datasets, spec["cls"])
    if name == "svhn":
        return cls(root=data_dir, split="train" if train else "test",
                   download=download, transform=transform)
    return cls(root=data_dir, train=train, download=download, transform=transform)


def _default_transforms(name: str):
    spec = DATASETS[name]
    aug = [T.RandomCrop(spec["img_size"], padding=4)]
    if spec["flip"]:
        aug.append(T.RandomHorizontalFlip())
    aug.append(T.ToTensor())
    return T.Compose(aug), T.Compose([T.ToTensor()])


def get_loaders(
    dataset: str = "cifar10",
    data_dir: str = "./data",
    batch_size: int = 128,
    test_batch_size: int = 100,
    num_workers: int = 2,
    download: bool = True,
) -> Tuple[DataLoader, DataLoader]:
    """Generic train/test loader cifti (cifar10 | cifar100 | svhn)."""
    if dataset not in DATASETS:
        raise ValueError(f"Bilinmeyen dataset '{dataset}'. Secenekler: {list(DATASETS)}")
    train_tf, test_tf = _default_transforms(dataset)
    trainset = _make_dataset(dataset, data_dir, True, train_tf, download)
    testset = _make_dataset(dataset, data_dir, False, test_tf, download)
    trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True,
                             num_workers=num_workers, pin_memory=True)
    testloader = DataLoader(testset, batch_size=test_batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)
    return trainloader, testloader


def get_loaders_with_val(
    dataset: str = "cifar10",
    data_dir: str = "./data",
    batch_size: int = 128,
    test_batch_size: int = 100,
    val_size: int = 2000,
    split_seed: int = 42,
    num_workers: int = 2,
    download: bool = True,
    val_indices_path: str = None,
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Generic train/val/test loaders; sabit val bolmesi C1 protokoluyle ayni.

    val_indices_path verilirse split seed'den TUREMEZ: JSON'daki sabit indeks
    listesi kullanilir (tum egitim tohumlari ayni val setini paylasir ve ayni
    dosya clean pretraining'de de kullanilarak secim sizintisi engellenir).
    Dataset basina AYRI indeks dosyasi gerekir (SVHN n_train=73257!).
    """
    if dataset not in DATASETS:
        raise ValueError(f"Bilinmeyen dataset '{dataset}'. Secenekler: {list(DATASETS)}")
    train_tf, eval_tf = _default_transforms(dataset)

    train_aug_set = _make_dataset(dataset, data_dir, True, train_tf, download)
    train_eval_set = _make_dataset(dataset, data_dir, True, eval_tf, False)
    testset = _make_dataset(dataset, data_dir, False, eval_tf, download)

    if val_indices_path is not None:
        import json as _json
        with open(val_indices_path) as _f:
            _payload = _json.load(_f)
        if _payload.get("dataset", dataset) != dataset:
            raise ValueError(
                f"{val_indices_path} '{_payload['dataset']}' icin uretilmis; "
                f"'{dataset}' ile kullanilamaz")
        val_indices = list(_payload["val_indices"])
        _val_set = set(val_indices)
        if len(_val_set) != len(val_indices):
            raise ValueError(f"{val_indices_path}: tekrarli indeks var")
        if any(i < 0 or i >= len(train_aug_set) for i in _val_set):
            raise ValueError(f"{val_indices_path}: indeks araligi disi deger var")
        train_indices = [i for i in range(len(train_aug_set)) if i not in _val_set]
    else:
        generator = torch.Generator().manual_seed(split_seed)
        perm = torch.randperm(len(train_aug_set), generator=generator).tolist()
        val_indices = perm[:val_size]
        train_indices = perm[val_size:]

    trainloader = DataLoader(Subset(train_aug_set, train_indices),
                             batch_size=batch_size, shuffle=True,
                             num_workers=num_workers, pin_memory=True)
    valloader = DataLoader(Subset(train_eval_set, val_indices),
                           batch_size=test_batch_size, shuffle=False,
                           num_workers=num_workers, pin_memory=True)
    testloader = DataLoader(testset, batch_size=test_batch_size, shuffle=False,
                            num_workers=num_workers, pin_memory=True)
    return trainloader, valloader, testloader


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
