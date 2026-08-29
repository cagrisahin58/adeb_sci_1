#!/usr/bin/env python3
"""ON KAYITLI havuzda (SVHN DAHIL) uc ve dort protokollu egimler.

Kirmizi takim hakemi (2026-08-25) gosterdi ki on kayit SVHN'i B koluna VE
x-ekseninin %12 alti bosugunu kapatmaya atamis; SVHN'i disarida birakan
"bagimsiz tutarlilik kontrolu" cercevesi ise sonuc gorildukten 28 DAKIKA
SONRA yazilmis. Dolayisiyla ON KAYITLI havuz SVHN'i ICERIR.

Bu betik, mekanizma iddiasinin dayandigi UC PROTOKOLLU egimin o havuzda
ayakta kalip kalmadigini olcer.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")
P4 = ["raw", "target_correct", "both_correct", "successful_source"]
P3 = [p for p in P4 if p != "successful_source"]


def kume_bootstrap(x, y, kume, B=10000, tohum=42):
    rng = np.random.default_rng(tohum)
    uniq = sorted(set(kume))
    e = []
    for _ in range(B):
        sec = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([np.flatnonzero(kume == t) for t in sec])
        if len(set(x[idx])) < 2:
            continue
        b1, _ = np.polyfit(x[idx], y[idx], 1)
        e.append(b1)
    return np.percentile(e, [2.5, 97.5])


def olc(yol, ad):
    d = json.loads((ROOT / yol).read_text(encoding="utf-8"))
    c = d["ciftler"]
    x = np.array([q["x_temiz_hata_farki"] for q in c])
    kume = np.array([q["kume"] for q in c])
    print(f"\n=== {ad}: n={len(c)} cift / {len(set(kume))} kume ===")
    for etiket, P in (("dort protokol", P4), ("uc protokol (SS haric)", P3)):
        y = np.array([max(q["asimetri"][k] for k in P)
                      - min(q["asimetri"][k] for k in P) for q in c])
        b1, b0 = np.polyfit(x, y, 1)
        r = np.corrcoef(x, y)[0, 1]
        ga = kume_bootstrap(x, y, kume)
        sifir = "SIFIRI ICERIYOR" if ga[0] <= 0 <= ga[1] else ""
        print(f"  {etiket:24s} egim {b1:+.4f}  r {r:+.3f}  "
              f"GA [{ga[0]:+.4f}, {ga[1]:+.4f}]  {sifir}")


olc("results/q1/e3_asimetri_fit.json", "SVHN DISARIDA (post-hoc havuz)")
olc("results/q1/e3_asimetri_fit_svhnli.json", "SVHN DAHIL (ON KAYITLI havuz)")
