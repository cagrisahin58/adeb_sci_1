#!/usr/bin/env python3
"""FAZ 2.1 DOGRULAMA: kol karsilastirmasi hangi havuzda kuruluyor?

Panel iddiasi: 04:111 SVHN'li havuzu ON KAYITLI ilan edip dort protokollu
egimi geri cekiyor; 04:115 ise kol karsilastirmasini SVHN'SIZ (post-hoc)
havuzdan kuruyor. On kayitli havuzda B kolunun araligi A kolununkini
KAPSIYOR, dolayisiyla "dort protokolde uyusmuyorlar" hukmu orada yanlis.

Ayrica: A kolunun havuzlanmis OLS egimi (+0,273) kume-ici (sabit etki)
kestirimden ayrik mi? Havuzlanmis egim kumeler-ARASI karsitliktan
etkilenir; kume-ici kestirim o karsitligi disarida birakir.
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
        e.append(np.polyfit(x[idx], y[idx], 1)[0])
    return np.percentile(e, [2.5, 97.5])


def yukle(yol):
    d = json.loads((ROOT / yol).read_text(encoding="utf-8"))
    c = d["ciftler"]
    x = np.array([q["x_temiz_hata_farki"] for q in c])
    kume = np.array([q["kume"] for q in c])
    return x, kume, c


def yayilim(c, P):
    return np.array([max(q["asimetri"][k] for k in P)
                     - min(q["asimetri"][k] for k in P) for q in c])


def kume_ici_egim(x, y, kume):
    """Sabit-etki (within) egim: her kumenin ortalamasi cikarilir."""
    xw, yw = x.astype(float).copy(), y.astype(float).copy()
    for t in set(kume):
        m = kume == t
        if m.sum() >= 2:
            xw[m] -= xw[m].mean()
            yw[m] -= yw[m].mean()
        else:
            xw[m] = np.nan
    ok = ~np.isnan(xw)
    if ok.sum() < 2 or len(set(xw[ok])) < 2:
        return float("nan"), 0
    return float(np.polyfit(xw[ok], yw[ok], 1)[0]), int(ok.sum())


def ortusuyor(a, b):
    return not (a[1] < b[0] or b[1] < a[0])


print("=" * 74)
print("B KOLU: iki havuz, iki protokol seti")
print("=" * 74)
B = {}
for ad, yol in (("SVHN'siz (post-hoc)", "results/q1/e3_asimetri_fit.json"),
                ("SVHN'li (ON KAYITLI)", "results/q1/e3_asimetri_fit_svhnli.json")):
    x, kume, c = yukle(yol)
    for etiket, P in (("dort", P4), ("uc", P3)):
        y = yayilim(c, P)
        egim = float(np.polyfit(x, y, 1)[0])
        ga = kume_bootstrap(x, y, kume)
        B[(ad, etiket)] = (egim, ga)
        print(f"  {ad:22s} {etiket:5s} protokol  egim {egim:+.4f}  "
              f"GA [{ga[0]:+.4f}, {ga[1]:+.4f}]  (n={len(c)}, {len(set(kume))} kume)")

print()
print("=" * 74)
print("A KOLU: havuzlanmis OLS vs KUME-ICI (sabit etki)")
print("=" * 74)
ak = ROOT / "results/q1/e3_akolu_noktalar.json"
if not ak.exists():
    adaylar = sorted(ROOT.glob("results/q1/*akolu*")) + sorted(ROOT.glob("results/q1/e3_akolu*"))
    print("  A kolu nokta dosyasi bulunamadi. Adaylar:",
          [p.name for p in adaylar] or "(yok)")
else:
    x, kume, c = yukle("results/q1/e3_akolu_noktalar.json")
    for etiket, P in (("dort", P4), ("uc", P3)):
        y = yayilim(c, P)
        havuz = float(np.polyfit(x, y, 1)[0])
        ici, n = kume_ici_egim(x, y, kume)
        print(f"  {etiket:5s} protokol  havuzlanmis {havuz:+.4f}  "
              f"kume-ici {ici:+.4f}  (n_within={n})")

print()
print("=" * 74)
print("HUKUM: makaledeki 'dort protokolde uyusmuyorlar' cumlesi")
print("=" * 74)
A4 = (0.2189, 0.3712)   # makaleden: kontrollu kol, dort protokol
A3 = (0.602, 0.727)     # makaleden: kontrollu kol, uc protokol
for ad in ("SVHN'siz (post-hoc)", "SVHN'li (ON KAYITLI)"):
    for etiket, Ax in (("dort", A4), ("uc", A3)):
        ga = B[(ad, etiket)][1]
        o = ortusuyor(Ax, ga)
        print(f"  {ad:22s} {etiket:5s}: A {list(np.round(Ax,3))} vs "
              f"B [{ga[0]:+.3f}, {ga[1]:+.3f}] -> "
              f"{'ORTUSUYOR' if o else 'ortusmuyor'}")
