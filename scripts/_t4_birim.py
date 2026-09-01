#!/usr/bin/env python3
"""FAZ 2.2: birim politikasi CIFAR-100 ve SVHN'e tasinabilir mi?

CIFAR-10'da (04:105) su serh var: raporlanan "eslestirilmis bootstrap GA"
uc TOHUMUN kendi GA uclarinin ORTALAMASIDIR, kapsama garantisi olan bir
aralik degildir; kosum duzeyi cikarim icin tohumlar-arasi t araligi verilir.
Ayni serh CIFAR-100 ve SVHN bolumlerinde YOK.

Bu betik her iki veri kumesi icin:
  - GA'nin gercekten uc-ortalamasi olup olmadigini,
  - kac tohum uzerinden kuruldugunu,
  - ve (anlamliysa) tohumlar-arasi t araligini hesaplar.
"""
import json
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path("/workspace")


def bak(ad, yol):
    p = ROOT / yol
    if not p.exists():
        print(f"\n{ad}: dosya yok -> {yol}")
        return
    d = json.loads(p.read_text(encoding="utf-8"))

    def ara(o, hedef):
        if isinstance(o, dict):
            if hedef in o:
                return o[hedef]
            for v in o.values():
                r = ara(v, hedef)
                if r is not None:
                    return r
        return None

    bc = ara(d, "both_correct_paired")
    print(f"\n{'='*70}\n{ad}\n{'='*70}")
    if bc is None:
        print("  both_correct_paired yok; ust anahtarlar:", list(d.keys())[:10])
        return

    for k in ("ci_low", "ci_high", "diff_pp"):
        v = bc.get(k)
        if isinstance(v, dict):
            print(f"  {k:10s} degerler {v.get('values')}  ort {v.get('mean')}")
    for k in ("perm_p_max", "perm_p", "tost_equivalent_any", "n_common"):
        if k in bc:
            v = bc[k]
            print(f"  {k:22s} {v.get('values') if isinstance(v, dict) else v}")

    dv = bc.get("diff_pp", {}).get("values")
    if dv and len(dv) >= 2:
        a = np.array(dv, dtype=float)
        n = len(a)
        if n >= 3:
            t = stats.t.ppf(0.975, n - 1)
            yari = t * a.std(ddof=1) / np.sqrt(n)
            print(f"  -> {n} tohum · tohumlar-arasi t araligi "
                  f"[{a.mean()-yari:.2f}, {a.mean()+yari:.2f}]")
        else:
            print(f"  -> {n} tohum: t araligi df={n-1}, BILGI TASIMAZ "
                  f"(sd tek gozlemden kestirilir). Yalniz ETIKETLEME yapilmali.")
    lo = bc.get("ci_low", {}).get("values")
    hi = bc.get("ci_high", {}).get("values")
    if lo and hi:
        print(f"  -> raporlanan GA = uc-ortalamasi "
              f"[{np.mean(lo):.2f}, {np.mean(hi):.2f}]  "
              f"({len(lo)} tohumun kendi araligindan)")


bak("CIFAR-10 (referans, serh ZATEN var)",
    "results/c1_transfer/c1_transfer_summary.json")
bak("CIFAR-100", "results/q1/cifar100/transfer/e1_transfer_summary.json")
bak("SVHN", "results/q1/svhn/transfer/e7_transfer_summary.json")
