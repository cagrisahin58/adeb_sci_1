#!/usr/bin/env python3
"""HER-IKISI-DOGRU altkumesinde AutoAttack McNemar'i.

AA parcalari yalniz `robust_correct` tasiyor. Temiz dogruluk saldiridan
bagimsiz oldugu icin ayni model/tohum ciftinin PGD ornek-bazli dosyasindaki
`clean_correct` alani AA icin de gecerlidir; iki dosya da tam test kumesini
ayni sirada tasir (once uzunluk esitligi dogrulanir).

Amac: makalenin 04_experiments.tex:64'te her-ikisi-dogru altkumesine
atfettigi "AA icin 10,7 puan, McNemar p<1e-84" iddiasini KANITLAMAK ya da
CURUTMEK. Referans foyundeki 1e-84 TAM KUME degeridir.
"""
import glob
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path("/workspace/results/c1_seeds")
TOHUM = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def aa_robust(pair, ad):
    parcalar = sorted(glob.glob(str(ROOT / f"pair{pair}/aa_chunk_{ad}_*.npz")))
    return np.concatenate([np.load(p)["robust_correct"] for p in parcalar])


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return float(stats.binomtest(min(b, c), n, 0.5,
                                 alternative="two-sided").pvalue)


print(f"{'cift':6s}{'n_ortak':>9s}{'R dogru':>9s}{'V dogru':>9s}"
      f"{'b':>7s}{'c':>7s}{'fark':>8s}  p")
print("-" * 62)
farklar, pler, nler = [], [], []
for pair, (rs, vs) in TOHUM.items():
    zr = np.load(ROOT / f"pair{pair}/pgd_per_sample_resnet18_s{rs}.npz")
    zv = np.load(ROOT / f"pair{pair}/pgd_per_sample_vit_tiny_s{vs}.npz")
    rr, rv = aa_robust(pair, "ResNet18_AT"), aa_robust(pair, "ViT_Tiny_AT")
    assert len(rr) == len(zr["clean_correct"]) == len(rv) == len(zv["clean_correct"]), \
        "AA ve PGD dosyalari ayni uzunlukta degil; hizalama varsayimi gecersiz"

    ortak = zr["clean_correct"] & zv["clean_correct"]
    R, V = rr[ortak], rv[ortak]
    b = int((R & ~V).sum())
    c = int((~R & V).sum())
    p = mcnemar(b, c)
    fark = 100 * (R.mean() - V.mean())
    print(f"{pair:<6d}{int(ortak.sum()):>9d}{100*R.mean():>9.2f}"
          f"{100*V.mean():>9.2f}{b:>7d}{c:>7d}{fark:>8.2f}  {p:.3g}")
    farklar.append(fark); pler.append(p); nler.append(int(ortak.sum()))

print(f"\nAA her-ikisi-dogru: n ort {np.mean(nler):.0f}  "
      f"fark {np.mean(farklar):.2f} +/- {np.std(farklar, ddof=1):.2f} puan  "
      f"en buyuk p = {max(pler):.3g}")
print("\nMakale iddiasi (04_experiments.tex:64): 10,7 puan, p<1e-84")
print(f"OLCULEN: {np.mean(farklar):.2f} puan, en buyuk p {max(pler):.3g}  "
      f"-> {'p siniri TUTUYOR' if max(pler) < 1e-84 else 'p SINIRI TUTMUYOR'}")
