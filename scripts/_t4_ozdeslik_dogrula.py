#!/usr/bin/env python3
"""A5-1 BAGIMSIZ DOGRULAMA: Denklem 1'in genel bicimi hangisi?

Makale (04:133) su bicimi yaziyor:
    r_ham = e*(1-p) + r_kos*(1-e)          <-- IDDIA EDILEN
Hakem paneli sunu soyluyor:
    r_ham = e*p     + r_kos*(1-e)          <-- ONERILEN

p'nin TANIMI: temizde YANLIS siniflandirilan bir orneğin saldiri altinda
YANLIS KALMA olasiligi, yani P(adv yanlis | temiz yanlis).

Toplam olasilik yasasi:
    P(adv yanlis) = P(adv yanlis | temiz yanlis) P(temiz yanlis)
                  + P(adv yanlis | temiz dogru)  P(temiz dogru)
                  = p*e + r_kos*(1-e)

Bu betik iddiayi ORNEK BAZINDA veriden, iki bicimi de hesaplayarak sinar.
Transfer yonleri icin kaynakta uretilmis ornekler hedefte degerlendirilir.
"""
import glob
from pathlib import Path

import numpy as np

KOK = Path("/workspace/results/c1_seeds")
TOHUM = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def satir(ad, tc, ta):
    """tc = hedef temizde dogru mu, ta = hedef saldiri altinda dogru mu."""
    e = 1.0 - tc.mean()                       # temiz hata
    r_ham = 1.0 - ta.mean()                   # kosullamasiz yanlis oran
    r_kos = 1.0 - ta[tc].mean()               # temiz-dogru altkumesinde
    p = 1.0 - ta[~tc].mean() if (~tc).sum() else float("nan")

    onerilen = e * p + r_kos * (1 - e)
    basili = e * (1 - p) + r_kos * (1 - e)
    return dict(ad=ad, e=100 * e, p=p, r_ham=100 * r_ham, r_kos=100 * r_kos,
                onerilen=100 * onerilen, basili=100 * basili,
                h_onerilen=100 * abs(onerilen - r_ham),
                h_basili=100 * abs(basili - r_ham))


kayit = []
for cift, (rs, vs) in TOHUM.items():
    zr = np.load(KOK / f"pair{cift}/pgd_per_sample_resnet18_s{rs}.npz")
    zv = np.load(KOK / f"pair{cift}/pgd_per_sample_vit_tiny_s{vs}.npz")
    for ad, z in ((f"cift{cift} ResNet(beyaz kutu)", zr),
                  (f"cift{cift} ViT(beyaz kutu)", zv)):
        kayit.append(satir(ad, z["clean_correct"].astype(bool),
                           z["robust_correct"].astype(bool)))

# transfer yonleri (varsa)
for f in sorted(glob.glob(str(KOK / "pair*/transfer_per_sample_*.npz"))):
    z = np.load(f)
    if {"target_clean_correct", "target_adv_correct"} <= set(z.files):
        kayit.append(satir(Path(f).name[:44],
                           z["target_clean_correct"].astype(bool),
                           z["target_adv_correct"].astype(bool)))

print(f"{'yon':34s}{'e%':>7s}{'p':>7s}{'r_ham%':>8s}"
      f"{'ONERILEN hata':>15s}{'BASILI hata':>13s}")
print("-" * 84)
for k in kayit:
    print(f"{k['ad']:34s}{k['e']:7.2f}{k['p']:7.4f}{k['r_ham']:8.2f}"
          f"{k['h_onerilen']:15.4f}{k['h_basili']:13.2f}")

on = np.array([k["h_onerilen"] for k in kayit])
ba = np.array([k["h_basili"] for k in kayit])
print("-" * 84)
print(f"ONERILEN  e*p + r_kos*(1-e)   : ort {on.mean():.6f} puan, "
      f"en buyuk {on.max():.6f} puan   ({len(kayit)} yon)")
print(f"BASILI    e*(1-p) + r_kos*(1-e): ort {ba.mean():.4f} puan, "
      f"en buyuk {ba.max():.4f} puan")

print("\np=1 SINIRI (makalenin 'Denklem 1'e indirgenir' iddiasi):")
print("  onerilen bicim, p=1  ->  e*1 + r_kos*(1-e) = e + r_kos*(1-e)   = DENKLEM 1")
print("  basili   bicim, p=1  ->  e*0 + r_kos*(1-e) =     r_kos*(1-e)   = DENKLEM 1 DEGIL")
print(f"\nHUKUM: {'ONERILEN dogru, BASILI YANLIS' if on.max() < ba.max() else 'BASILI dogru'}")
