#!/usr/bin/env python3
"""S3 DOGRULAMASI: gradyan seyreklik iddiasi KOSUM duzeyinde ayakta mi?

Istatistik hakemi (2026-08-28) sunu iddia etti: Tablo VIII'in kendi basligi
"Inference is at the run level ... so that the unit of inference matches the
unit of the claim" diyor, ama seyreklik iddiasi ORNEK duzeyi Wilcoxon ile
kuruluyor (p < 1e-11). Kosum duzeyinde (n=3) Holm duzeltmesiyle ucu de
0,108'e cikiyor ve alpha=0,05'te DUSUYOR.

Bu betik onu bagimsiz olarak yeniden hesaplar.
"""
import glob
import json
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path("/workspace")

OLCUTLER = [("Hoyer", "sparsity_hoyer"), ("Gini", "sparsity_gini"),
            ("Frac<1%", "sparsity_rel_threshold"),
            ("Hizalanma", "gradient_alignment")]


def cift_degerleri(olcut):
    """Her kosum icin (ResNet, ViT) degeri."""
    R, V = [], []
    for p in sorted(glob.glob(str(ROOT / "results/c1_gradient/pair*"))):
        f = Path(p) / "gradient_summary.json"
        if not f.exists():
            adaylar = list(Path(p).glob("*.json"))
            if not adaylar:
                continue
            f = adaylar[0]
        d = json.loads(f.read_text(encoding="utf-8"))

        def bul(o, model):
            if isinstance(o, dict):
                if model in o and isinstance(o[model], dict):
                    v = o[model].get(olcut)
                    if isinstance(v, dict):
                        return v.get("mean")
                    if v is not None:
                        return v
                for x in o.values():
                    r = bul(x, model)
                    if r is not None:
                        return r
            return None

        r, v = bul(d, "ResNet18_AT"), bul(d, "ViT_Tiny_AT")
        if r is not None and v is not None:
            R.append(r); V.append(v)
    return np.array(R), np.array(V)


print(f"{'olcut':12s}{'ResNet':>22s}{'ViT':>22s}{'ham p':>10s}")
print("-" * 68)
ham = {}
for ad, anahtar in OLCUTLER:
    R, V = cift_degerleri(anahtar)
    if len(R) < 2:
        print(f"{ad:12s}  artefakt bulunamadi (n={len(R)})")
        continue
    t, p = stats.ttest_rel(R, V)
    ham[ad] = p
    print(f"{ad:12s}{str([round(x,4) for x in R]):>22s}"
          f"{str([round(x,4) for x in V]):>22s}{p:>10.4f}")

# Holm duzeltmesi (yalniz uc seyreklik olcutu; hizalanma ayri aile)
seyreklik = {k: v for k, v in ham.items() if k != "Hizalanma"}
if seyreklik:
    sirali = sorted(seyreklik.items(), key=lambda kv: kv[1])
    m = len(sirali)
    print("\nHOLM (uc seyreklik olcutu):")
    onceki = 0.0
    for i, (ad, p) in enumerate(sirali):
        duz = max(onceki, min(1.0, (m - i) * p))
        onceki = duz
        print(f"  {ad:12s} ham {p:.4f}  ->  Holm {duz:.4f}   "
              f"{'anlamli' if duz < 0.05 else 'ANLAMLI DEGIL'}")
    print(f"\n  IUT (max-p) = {max(seyreklik.values()):.4f}")
if "Hizalanma" in ham:
    print(f"\nHizalanma (ayri aile): p = {ham['Hizalanma']:.4f}  "
          f"{'anlamli' if ham['Hizalanma'] < 0.05 else 'ANLAMLI DEGIL'}")
