"""Tur 2: temiz checkpoint'lerde epok gecmisi (history.test_acc) var mi?"""
import glob
import torch

yollar = sorted(glob.glob("models/c1/vit_tiny_s200[123]/vit_tiny/clean/*.pth")
                + glob.glob("models/c1/resnet18_s100[123]/resnet18/clean/best.pth")
                + glob.glob("models/q1/konsey_smoke/*/*/clean/*.pth"))
for p in yollar:
    ck = torch.load(p, map_location="cpu", weights_only=False)
    h = ck.get("history") or {}
    ta = h.get("test_acc") or []
    print(p, "epoch=", ck.get("epoch"), "acc=", ck.get("accuracy"),
          "n_hist=", len(ta), "ilk5=", [round(float(x), 2) for x in ta[:5]],
          "anahtarlar=", sorted(h.keys()))
