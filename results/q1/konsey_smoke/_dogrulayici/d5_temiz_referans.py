"""Celisik dogrulayici, D5: temiz asama denetiminin referanslari.

V_IN referansi (C1 ViT-Tiny temiz best.pth 'accuracy' alani) ve, R224 icin
fikir vermek uzere, C1 ResNet-18 (32x32) temiz best.pth dogruluklari.
Cikti: results/q1/konsey_smoke/_dogrulayici/d5_temiz_referans.json
"""
import json
from pathlib import Path

import torch

out = {}
for kal, ad in (("models/c1/vit_tiny_s200{}/vit_tiny/clean/best.pth", "c1_vit_tiny_temiz"),
                ("models/c1/resnet18_s100{}/resnet18/clean/best.pth", "c1_resnet18_temiz")):
    d = {}
    for s in (1, 2, 3):
        p = Path(kal.format(s))
        if p.exists():
            ck = torch.load(p, map_location="cpu", weights_only=False)
            d[str(p)] = {"accuracy": float(ck.get("accuracy")), "epoch": ck.get("epoch")}
    vals = [v["accuracy"] for v in d.values()]
    out[ad] = {"dosyalar": d, "ortalama": round(sum(vals) / len(vals), 4) if vals else None}
# Smoke temiz kontrol noktalarinin dogrulugu (200 iterasyon)
for p in sorted(Path("models/q1/konsey_smoke").glob("*/*/clean/best.pth")):
    ck = torch.load(p, map_location="cpu", weights_only=False)
    out.setdefault("smoke", {})[str(p)] = float(ck.get("accuracy"))
Path("results/q1/konsey_smoke/_dogrulayici/d5_temiz_referans.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
