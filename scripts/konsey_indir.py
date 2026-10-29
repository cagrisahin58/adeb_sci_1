"""Konsey B1: indirmeler (29.10.2026). Konteynerde, depo kokunden:

    docker exec -w /workspace adeb_eval python scripts/konsey_indir.py

1. timm ImageNet agirliklari -> models/timm_agirliklar/<timm adi>/model.safetensors
   (src/models/r224.py::load_imagenet_init once bu yerel kopyaya bakar).
2. RobustBench CIFAR-10 Linf: Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18,
   Rade2021Helper_R18_ddpm -> models/robustbench_zoo/cifar10/Linf/<ad>.pt
   (robustbench.load_model, gdown).
3. Debenedetti2022Light_XCiT-S12: konteyner torch hub onbelleginden
   models/robustbench_zoo/cifar10/Linf/Debenedetti2022Light_XCiT-S12.pth.tar
   kopyasi (robustbench bu modeli timm yolundan yukler; kopya, onbellek
   silinirse experiments/c1_c3_transfer_matrix.py tarafindan geri konur).

Indirme oncesi olculen boyutlar (HTTP basliklari, 29.10.2026): Sehwag 44 763 573,
Addepalli 44 778 553, Rade 50 261 042, deit_tiny 22 883 348, resnet18.a1
46 807 446 bayt; toplam 209 493 962 bayt (< 1 GB).
Rapor: results/q1/konsey_smoke/indirmeler.json
"""
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

TIMM = ["deit_tiny_patch16_224.fb_in1k", "resnet18.a1_in1k"]
RB = ["Sehwag2021Proxy_R18", "Addepalli2022Efficient_RN18", "Rade2021Helper_R18_ddpm"]
XCIT = ("Debenedetti2022Light_XCiT-S12", "debenedetti2022light-xcit-s-cifar10-linf.pth.tar")
OUT = Path("results/q1/konsey_smoke/indirmeler.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    rap = {"tarih": time.strftime("%Y-%m-%d %H:%M:%S"), "timm": {}, "robustbench": {}, "xcit": {}}
    from huggingface_hub import hf_hub_download

    for name in TIMM:
        d = Path("models/timm_agirliklar") / name
        d.mkdir(parents=True, exist_ok=True)
        f = d / "model.safetensors"
        if not f.exists():
            p = hf_hub_download(repo_id=f"timm/{name}", filename="model.safetensors",
                                local_dir=str(d))
            print(f"indirildi {p}")
        rap["timm"][name] = {"yol": str(f), "bayt": f.stat().st_size, "sha256": sha(f)}

    from robustbench.utils import load_model

    for name in RB:
        t = time.time()
        p = Path("models/robustbench_zoo/cifar10/Linf") / f"{name}.pt"
        onceden = p.exists()
        try:
            m = load_model(model_name=name, dataset="cifar10", threat_model="Linf",
                           model_dir="models/robustbench_zoo")
            n = sum(x.numel() for x in m.parameters())
            rap["robustbench"][name] = {"yol": str(p), "onceden_vardi": onceden,
                                        "bayt": p.stat().st_size, "sha256": sha(p),
                                        "parametre": n, "sure_s": round(time.time() - t, 1),
                                        "durum": "OK"}
            del m
        except Exception as e:  # noqa: BLE001
            rap["robustbench"][name] = {"durum": f"HATA {type(e).__name__}: {str(e)[:300]}"}
        print(name, rap["robustbench"][name].get("durum"))

    name, fname = XCIT
    hub = Path(torch.hub.get_dir()) / "checkpoints" / fname
    dst = Path("models/robustbench_zoo/cifar10/Linf") / f"{name}.pth.tar"
    if hub.exists() and not dst.exists():
        shutil.copy2(hub, dst)
    rap["xcit"] = {"hub": str(hub), "hub_var": hub.exists(), "kopya": str(dst),
                   "kopya_var": dst.exists(),
                   "sha256_hub": sha(hub) if hub.exists() else None,
                   "sha256_kopya": sha(dst) if dst.exists() else None,
                   "bayt": dst.stat().st_size if dst.exists() else None}
    rap["xcit"]["ozdes"] = (rap["xcit"]["sha256_hub"] is not None
                            and rap["xcit"]["sha256_hub"] == rap["xcit"]["sha256_kopya"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rap, indent=2, ensure_ascii=False))
    print(json.dumps(rap, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
