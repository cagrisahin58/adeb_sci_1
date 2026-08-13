"""Checkpoint'ten num_classes'i otomatik cikaran model yukleyici (Q1 Adim 4).

CIFAR-100 degerlendirmelerinde "num_classes bayragini unutma" hatasini yapisal
olarak engeller: siniflandirici basinin agirlik seklinden sinif sayisi okunur,
model o sayiyla insa edilir, agirliklar yuklenir.

Kullanim:
    from src.utils.load_model_auto import load_model_auto
    model = load_model_auto("resnet18", "models/q1/cifar100/.../best.pth", device)
"""
from typing import Optional

import torch

# Siniflandirici basi agirliklarinin state_dict anahtari adaylari (satir sayisi
# = sinif sayisi). Sarmalayicilar "model." onekiyle kaydeder.
_HEAD_KEYS = (
    "model.fc.weight",        # torchvision ResNet sarmalayicilari
    "model.head.weight",      # timm ViT sarmalayicilari
    "model.classifier.weight",  # DenseNet/EfficientNet sarmalayicilari
    "fc.weight",
    "head.weight",
    "classifier.weight",
)


def infer_num_classes(state_dict: dict) -> Optional[int]:
    """State dict'ten sinif sayisini cikar (bulunamazsa None)."""
    for key in _HEAD_KEYS:
        if key in state_dict:
            return int(state_dict[key].shape[0])
    # Son care: '.weight' ile biten 2 boyutlu son katman adaylarini tara
    for key in reversed(list(state_dict.keys())):
        if key.endswith(("fc.weight", "head.weight", "classifier.weight")):
            w = state_dict[key]
            if getattr(w, "ndim", 0) == 2:
                return int(w.shape[0])
    return None


def load_model_auto(model_type: str, ckpt_path: str, device, strict: bool = True):
    """Model tipini kur, sinif sayisini checkpoint'ten okuyarak agirliklari yukle.

    Returns:
        Yuklenmis model (device uzerinde, eval kipinde).
    """
    from src.models import ModelRegistry

    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    state = ckpt.get("model_state_dict", ckpt.get("state_dict", ckpt))

    nc = infer_num_classes(state)
    if nc is None:
        raise ValueError(
            f"{ckpt_path}: siniflandirici basi bulunamadi; num_classes cikarilamiyor. "
            f"Mevcut anahtarlardan ornek: {list(state.keys())[:5]}"
        )

    model = ModelRegistry.get(model_type, num_classes=nc)
    missing, unexpected = model.load_state_dict(state, strict=strict)
    if strict is False and (missing or unexpected):
        print(f"UYARI load_model_auto: missing={list(missing)[:3]} "
              f"unexpected={list(unexpected)[:3]}")
    model = model.to(device)
    model.eval()
    return model
