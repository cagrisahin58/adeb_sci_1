#!/usr/bin/env python3
"""HER-IKISI-DOGRU alt kumesinde McNemar (eksik istatistik).

Iddia-kanit hakemi (2026-08-28) gosterdi ki Bolum 4.1'de her-ikisi-dogru
altkumesine atfedilen McNemar p degerleri aslinda TAM TEST KUMESI
karsilastirmasindan aliniyor: uyusmaz sayilar (1677/483) tam kumedeki
dogruluk farkina (44,67-32,73 = 11,94 puan x 10.000 = 1194) birebir esit.
Iddia muhtemelen dogru ama KANITSIZ.

Bu betik eksik istatistigi ORNEK BAZINDA verilerden hesaplar.
"""
import glob
import json
from math import comb
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path("/workspace/results/c1_seeds")
TOHUM = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def aa_yukle(pair, ad):
    """AutoAttack parcalarini sirayla birlestir."""
    parcalar = sorted(glob.glob(str(ROOT / f"pair{pair}/aa_chunk_{ad}_*.npz")))
    cc, rc = [], []
    for p in parcalar:
        z = np.load(p)
        anahtar = set(z.files)
        c = "clean_correct" if "clean_correct" in anahtar else None
        r = "robust_correct" if "robust_correct" in anahtar else None
        if c is None or r is None:
            return None, None, sorted(anahtar)
        cc.append(z[c]); rc.append(z[r])
    if not cc:
        return None, None, []
    return np.concatenate(cc), np.concatenate(rc), None


def mcnemar_tam(b, c):
    """Tam binom iki yonlu McNemar."""
    n = b + c
    if n == 0:
        return 1.0
    # comb() tabanli dogrudan toplam n buyudukce float'a tasiyor;
    # scipy tam binom testi ayni degeri tasmasiz verir.
    return float(stats.binomtest(min(b, c), n, 0.5,
                                 alternative="two-sided").pvalue)


print(f"{'cift':6s}{'saldiri':8s}{'n_ortak':>9s}{'R dogru':>9s}{'V dogru':>9s}"
      f"{'b':>7s}{'c':>7s}{'fark(puan)':>12s}  p")
print("-" * 78)
ozet = {}
for pair, (rs, vs) in TOHUM.items():
    # --- PGD ---
    zr = np.load(ROOT / f"pair{pair}/pgd_per_sample_resnet18_s{rs}.npz")
    zv = np.load(ROOT / f"pair{pair}/pgd_per_sample_vit_tiny_s{vs}.npz")
    ortak = zr["clean_correct"] & zv["clean_correct"]
    R, V = zr["robust_correct"][ortak], zv["robust_correct"][ortak]
    b = int((R & ~V).sum()); c = int((~R & V).sum())
    p = mcnemar_tam(b, c)
    fark = 100 * (R.mean() - V.mean())
    print(f"{pair:<6d}{'PGD-10':8s}{int(ortak.sum()):>9d}{100*R.mean():>9.2f}"
          f"{100*V.mean():>9.2f}{b:>7d}{c:>7d}{fark:>12.2f}  {p:.3g}")
    ozet.setdefault("pgd", []).append((int(ortak.sum()), fark, p, b, c))

    # --- AutoAttack ---
    cr, rr, eksik = aa_yukle(pair, "ResNet18_AT")
    cv, rv, eksik2 = aa_yukle(pair, "ViT_Tiny_AT")
    if cr is None or cv is None:
        print(f"{pair:<6d}{'AA':8s}  AA parcalarinda beklenen alan yok: {eksik or eksik2}")
        continue
    ortak = cr & cv
    R, V = rr[ortak], rv[ortak]
    b = int((R & ~V).sum()); c = int((~R & V).sum())
    p = mcnemar_tam(b, c)
    fark = 100 * (R.mean() - V.mean())
    print(f"{pair:<6d}{'AA':8s}{int(ortak.sum()):>9d}{100*R.mean():>9.2f}"
          f"{100*V.mean():>9.2f}{b:>7d}{c:>7d}{fark:>12.2f}  {p:.3g}")
    ozet.setdefault("aa", []).append((int(ortak.sum()), fark, p, b, c))

print()
for ad, v in ozet.items():
    farklar = [x[1] for x in v]
    pler = [x[2] for x in v]
    print(f"{ad.upper():8s} fark ort {np.mean(farklar):.2f} +/- {np.std(farklar, ddof=1):.2f} puan"
          f"   en buyuk p = {max(pler):.3g}")
