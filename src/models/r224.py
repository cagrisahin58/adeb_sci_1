"""Konsey 2x2 (mimari x baslatma) sarmalayicilari (B1, 29.10.2026).

Girdi hatti (K3 karari): V-scr (C1 `vit_tiny`, src/models/vit.py) su hatti
kullanir ve bu dosyadaki *scr* hucresi onunla BIREBIR ayni hatti kullanir:

  veri yukleyici: RandomCrop(32, padding=4) + RandomHorizontalFlip + ToTensor
      (src/data/datasets.py::_default_transforms), deger araligi [0, 1],
      normalizasyon YOK
  model ici: nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

ImageNet normalizasyonu (timm pretrained_cfg mean/std) YALNIZ ImageNet
baslatmali hucrelerde (V-IN = `vit_tiny_in1k`, R224-IN = `resnet18_224_in1k`)
model icinde, buyutmeden SONRA uygulanir; baslatma demetinin parcasidir
(agirlik + temiz asama uzunlugu + normalizasyon). Normalizasyon degerleri
kalici tampon (buffer) olarak checkpoint'e girer; boylece normalizasyonlu bir
checkpoint normalizasyonsuz sarmalayiciya (ya da tersi) strict yuklemede
hata verir.

Kayitli tipler:
  resnet18_224       R224-scr: timm `resnet18`, 32->224, normalizasyon yok
  resnet18_224_in1k  R224-IN : ayni mimari + model ici IN normalizasyonu
                     (agirliklar `--init-weights resnet18_a1_in1k` ile)
  vit_tiny_in1k      V-IN    : `vit_tiny` ile ayni mimari ve buyutme + model
                     ici IN normalizasyonu (agirliklar
                     `--init-weights deit_tiny_in1k` ile). Sinif adinda "vit"
                     korunur (Trainer'in otomatik iyileyici secimi ve TGR
                     kancalari self.model.blocks'a bakar).
"""
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn

try:
    import timm
    TIMM_AVAILABLE = True
except ImportError:  # pragma: no cover
    TIMM_AVAILABLE = False

from .base import BaseModel
from .registry import register_model
from .vit import CIFAR10ViTTiny

# --init-weights anahtari -> (timm pretrained adi, uyumlu sarmalayici tipleri)
INIT_WEIGHTS = {
    "deit_tiny_in1k": ("deit_tiny_patch16_224.fb_in1k", ("vit_tiny_in1k",)),
    "resnet18_a1_in1k": ("resnet18.a1_in1k", ("resnet18_224_in1k",)),
}
# Normalizasyon degerlerinin okundugu pretrained_cfg (sarmalayici tipi -> timm adi)
NORM_SOURCE = {
    "vit_tiny_in1k": "deit_tiny_patch16_224.fb_in1k",
    "resnet18_224_in1k": "resnet18.a1_in1k",
}
# Yerel agirlik kopyasi (varsa ag erisimi gerekmez): models/timm_agirliklar/<ad>/model.safetensors
LOCAL_WEIGHT_DIR = Path("models/timm_agirliklar")


def imagenet_norm_from_cfg(timm_name: str) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
    """timm pretrained_cfg'den (mean, std) okur; ag erisimi gerektirmez."""
    cfg = timm.models.get_pretrained_cfg(timm_name)
    if cfg is None:
        raise ValueError(f"timm pretrained_cfg bulunamadi: {timm_name}")
    return tuple(float(v) for v in cfg.mean), tuple(float(v) for v in cfg.std)


class ResizeNormalize(nn.Module):
    """32->224 bilinear buyutme (V-scr ile ayni), ardindan istege bagli
    kanal normalizasyonu. mean/std None ise yalniz buyutme yapar ve tampon
    tasimaz (scr hucresi; state_dict'i nn.Upsample ile ayni kalir)."""

    def __init__(self, size: int = 224, mean=None, std=None):
        super().__init__()
        self.up = nn.Upsample(size=(size, size), mode="bilinear", align_corners=False)
        self.normalize = mean is not None
        if self.normalize:
            self.register_buffer("mean", torch.tensor(mean, dtype=torch.float32).view(1, 3, 1, 1))
            self.register_buffer("std", torch.tensor(std, dtype=torch.float32).view(1, 3, 1, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.up(x)
        if self.normalize:
            x = (x - self.mean) / self.std
        return x


@register_model("vit_tiny_in1k")
class CIFAR10ViTTinyIN1k(CIFAR10ViTTiny):
    """V-IN: `vit_tiny` ile ayni timm mimarisi (vit_tiny_patch16_224) ve ayni
    buyutme; buyutmeden sonra DeiT pretrained_cfg normalizasyonu. Agirliklar
    yapicida YUKLENMEZ (checkpoint yuklemesi ag gerektirmesin); temiz asamada
    `--init-weights deit_tiny_in1k` ile yuklenir."""

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes, pretrained=False)
        mean, std = imagenet_norm_from_cfg(NORM_SOURCE["vit_tiny_in1k"])
        # self.resize, CIFAR10ViTTiny.forward/get_features ve
        # TimmViTAttentionMixin.get_attention_maps tarafindan kullanilir;
        # normalizasyon boylece her yolda uygulanir.
        self.resize = ResizeNormalize(224, mean, std)


class _ResNet18R224Base(BaseModel):
    """timm `resnet18` (standart ImageNet ResNet-18: 7x7 stem + maxpool),
    girdi model icinde 32->224 buyutulur."""

    _norm_key: Optional[str] = None

    def __init__(self, num_classes: int = 10, pretrained: bool = False):
        super().__init__(num_classes=num_classes)
        if not TIMM_AVAILABLE:
            raise ImportError("timm gerekli")
        self.model = timm.create_model("resnet18", pretrained=False, num_classes=num_classes)
        if self._norm_key is not None:
            mean, std = imagenet_norm_from_cfg(NORM_SOURCE[self._norm_key])
            self.resize = ResizeNormalize(224, mean, std)
        else:
            # V-scr ile birebir ayni: yalniz bilinear buyutme, normalizasyon yok
            self.resize = nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(self.resize(x))

    def get_features(self, x: torch.Tensor) -> torch.Tensor:
        return self.model.forward_head(self.model.forward_features(self.resize(x)),
                                       pre_logits=True)

    def freeze_backbone(self) -> None:
        for name, p in self.model.named_parameters():
            if not name.startswith("fc."):
                p.requires_grad = False

    @property
    def input_size(self) -> Tuple[int, int]:
        return (32, 32)


@register_model("resnet18_224")
class CIFAR10ResNet18R224(_ResNet18R224Base):
    """R224-scr: rastgele baslatma, normalizasyon yok (V-scr girdi hatti)."""
    _norm_key = None


@register_model("resnet18_224_in1k")
class CIFAR10ResNet18R224IN1k(_ResNet18R224Base):
    """R224-IN: ayni mimari + model ici `resnet18.a1_in1k` normalizasyonu."""
    _norm_key = "resnet18_224_in1k"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_imagenet_init(model: nn.Module, init_key: str, model_type: str,
                       strict_report: bool = True) -> Dict:
    """ImageNet on egitimli govde agirliklarini sarmalayicinin `model.model`
    alt modulune yukler; siniflandirici basi atlanir (10 sinif, yeniden
    baslatilmis kalir). Yerel kopya (models/timm_agirliklar/<ad>/
    model.safetensors) varsa o kullanilir, yoksa timm/HF hub'dan indirilir.

    Rapor: yuklenen anahtar sayisi, bas disindaki eksik/fazla/sekil uyusmazligi
    listeleri, kaynak dosyanin sha256'si, pretrained_cfg mean/std.
    strict_report=True iken bas disinda tek bir uyumsuzluk bile RuntimeError.
    """
    if init_key not in INIT_WEIGHTS:
        raise ValueError(f"Bilinmeyen --init-weights: {init_key}")
    timm_name, ok_types = INIT_WEIGHTS[init_key]
    if model_type not in ok_types:
        raise ValueError(f"--init-weights {init_key} yalniz {ok_types} ile kullanilir "
                         f"(K3: IN normalizasyonu IN baslatmali tipte); verilen: {model_type}")

    local = LOCAL_WEIGHT_DIR / timm_name / "model.safetensors"
    kwargs = {}
    if local.exists():
        kwargs["pretrained_cfg_overlay"] = dict(file=str(local))
    src = timm.create_model(timm_name, pretrained=True, **kwargs)
    head_prefix = src.pretrained_cfg.get("classifier", "head")
    src_sd = src.state_dict()
    tgt = model.model
    tgt_sd = tgt.state_dict()

    def is_head(k):
        return k == head_prefix or k.startswith(head_prefix + ".")

    load_sd, mismatch = {}, []
    for k, v in src_sd.items():
        if is_head(k):
            continue
        if k in tgt_sd:
            if tgt_sd[k].shape == v.shape:
                load_sd[k] = v
            else:
                mismatch.append(f"{k}: {tuple(v.shape)} -> {tuple(tgt_sd[k].shape)}")
    missing_nonhead = sorted(k for k in tgt_sd if not is_head(k) and k not in load_sd)
    unexpected_nonhead = sorted(k for k in src_sd if not is_head(k) and k not in tgt_sd)
    head_skipped = sorted(k for k in src_sd if is_head(k))
    res = tgt.load_state_dict(load_sd, strict=False)
    mean, std = imagenet_norm_from_cfg(timm_name)

    report = {
        "init_key": init_key,
        "timm_name": timm_name,
        "source_file": str(local) if local.exists() else "timm/HF hub onbellegi",
        "source_sha256": _sha256(local) if local.exists() else None,
        "n_loaded": len(load_sd),
        "n_target_keys": len(tgt_sd),
        "missing_nonhead": missing_nonhead,
        "unexpected_nonhead": unexpected_nonhead,
        "shape_mismatch": mismatch,
        "head_keys_skipped": head_skipped,
        "torch_missing_after_load": sorted(res.missing_keys),
        "pretrained_cfg_mean": list(mean),
        "pretrained_cfg_std": list(std),
    }
    # Sarmalayicidaki normalizasyon tamponu pretrained_cfg ile ayni mi?
    rz = getattr(model, "resize", None)
    if isinstance(rz, ResizeNormalize) and rz.normalize:
        report["wrapper_mean"] = [float(v) for v in rz.mean.flatten()]
        report["wrapper_std"] = [float(v) for v in rz.std.flatten()]
        # float32 tampon ile Python float'i: 1e-6 toleransla karsilastirilir
        report["norm_matches_cfg"] = all(
            abs(a - b) < 1e-6 for a, b in
            zip(report["wrapper_mean"] + report["wrapper_std"],
                report["pretrained_cfg_mean"] + report["pretrained_cfg_std"]))
    else:
        report["norm_matches_cfg"] = False
    if strict_report and (missing_nonhead or unexpected_nonhead or mismatch
                          or not report["norm_matches_cfg"]):
        raise RuntimeError(f"ImageNet baslatma yuklemesi temiz degil: {report}")
    del src
    return report
