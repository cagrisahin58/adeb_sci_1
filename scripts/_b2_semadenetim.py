#!/usr/bin/env python3
"""B2 on-denetim: per-sample transfer npz'lerinin ALAN ADLARINI raporlar.

Hicbir sey degistirmez. Amac: 'successful_source' maskesinin siki
varyantini (kaynak temizde DOGRU ve adv'de YANLIS) hesaplamak icin
gereken alanlarin her veri kumesinde bulunup bulunmadigini olcmek.
"""
from pathlib import Path
import numpy as np

ROOT = Path("/workspace")

KUMELER = {
    "cifar10_linf": sorted(ROOT.glob("results/c1_transfer/pair*/per_sample_*.npz")),
    "cifar100": sorted(ROOT.glob("results/q1/cifar100/transfer/pair*/per_sample_*.npz")),
    "svhn": sorted(ROOT.glob("results/q1/svhn/transfer/pair*/per_sample_*.npz")),
    "cifar10_l2": sorted(ROOT.glob("results/q1/cifar10_l2/transfer/pair*/per_sample_*.npz")),
}

for ad, dosyalar in KUMELER.items():
    print(f"\n=== {ad}: {len(dosyalar)} dosya ===")
    if not dosyalar:
        print("  DOSYA YOK")
        continue
    d = np.load(dosyalar[0])
    print(f"  ornek: {dosyalar[0].relative_to(ROOT)}")
    for k in d.files:
        a = d[k]
        print(f"    {k:28s} shape={a.shape} dtype={a.dtype}")
    # tum dosyalarda ayni alanlar var mi?
    ilk = set(d.files)
    farkli = [p.name for p in dosyalar if set(np.load(p).files) != ilk]
    print(f"  alan seti farkli olan dosya sayisi: {len(farkli)}")
    if farkli:
        print("   ", farkli[:5])
