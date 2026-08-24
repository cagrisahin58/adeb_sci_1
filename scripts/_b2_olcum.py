#!/usr/bin/env python3
"""B2 OLCUM: 'basarili kaynak' protokolunun GEVSEK ve SIKI varyantlari.

Makale (3.5) protokolu soyle tanimliyor: "hedef-dogru ornekler ICINDE
saldirinin kaynakta BEYAZ KUTU ANLAMINDA BASARILI oldugu ornekler".
Beyaz kutu basarisi standart tanimda kaynagin temizde DOGRU olup adv'de
YANLIS olmasidir. Kod ise yalnizca kaynagin adv'de yanlis olmasini ariyor:

    GEVSEK (kodda):  target_clean_correct & source_adv_wrong
    SIKI  (metinde): target_clean_correct & source_clean_correct & source_adv_wrong

Bu betik hicbir sey YAZMAZ; iki varyanti yan yana olcer.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")

# (etiket, dizinler, kaynak-model-adi, hedef-model-adi)
KUMELER = [
    ("CIFAR-10 Linf", [ROOT / f"results/c1_transfer/pair{i}" for i in (1, 2, 3)]),
    ("CIFAR-100", [ROOT / f"results/q1/cifar100/transfer/pair{i}" for i in (1, 2, 3)]),
    ("SVHN", [ROOT / f"results/q1/svhn/transfer/pair{i}" for i in (1, 2)]),
    ("CIFAR-10 L2", [ROOT / f"results/q1/cifar10_l2/transfer/pair{i}" for i in (1, 2, 3)]),
]

CNN, VIT = "ResNet18_AT", "ViT_Tiny_AT"


def oranlar(d, siki):
    """a2_transfer_protocols.rate_ci ile ayni yuvarlama (2 basamak)."""
    fool = d["target_adv_wrong"]
    tc = d["target_clean_correct"]
    sc = d["source_clean_correct"]
    sa = d["source_adv_wrong"]
    ss_mask = (tc & sc & sa) if siki else (tc & sa)
    m = {"raw": np.ones_like(fool, dtype=bool), "target_correct": tc,
         "both_correct": tc & sc, "successful_source": ss_mask}
    return ({k: round(float(100 * fool[v].mean()), 2) if v.sum() else float("nan")
             for k, v in m.items()},
            {k: int(v.sum()) for k, v in m.items()})


P4 = ["raw", "target_correct", "both_correct", "successful_source"]
sonuc = {}

for etiket, dizinler in KUMELER:
    print(f"\n{'=' * 78}\n{etiket}\n{'=' * 78}")
    kayit = {"gevsek": {p: [] for p in P4}, "siki": {p: [] for p in P4},
             "yayilim_gevsek": [], "yayilim_siki": [],
             "n_gevsek": [], "n_siki": []}
    for d in dizinler:
        f_cv = d / f"per_sample_{CNN}_to_{VIT}.npz"
        f_vc = d / f"per_sample_{VIT}_to_{CNN}.npz"
        if not (f_cv.exists() and f_vc.exists()):
            print(f"  ATLANDI {d.name}: dosya yok")
            continue
        cv, vc = dict(np.load(f_cv)), dict(np.load(f_vc))
        for siki, ad in ((False, "gevsek"), (True, "siki")):
            r_cv, n_cv = oranlar(cv, siki)
            r_vc, n_vc = oranlar(vc, siki)
            asim = {p: round(r_cv[p] - r_vc[p], 2) for p in P4}
            for p in P4:
                kayit[ad][p].append(asim[p])
            kayit["yayilim_" + ad].append(max(asim.values()) - min(asim.values()))
            kayit["n_" + ad].append((n_cv["successful_source"], n_vc["successful_source"]))
        print(f"  {d.name}: "
              f"SS gevsek {kayit['gevsek']['successful_source'][-1]:+7.2f}  "
              f"siki {kayit['siki']['successful_source'][-1]:+7.2f}   |  "
              f"yayilim {kayit['yayilim_gevsek'][-1]:6.2f} -> {kayit['yayilim_siki'][-1]:6.2f}   |  "
              f"n(SS) {kayit['n_gevsek'][-1]} -> {kayit['n_siki'][-1]}")

    def ms(v):
        a = np.asarray(v, float)
        return a.mean(), (a.std(ddof=1) if len(a) > 1 else 0.0)

    print(f"\n  {'protokol':<20}{'GEVSEK (kod)':>22}{'SIKI (metin)':>22}{'fark':>10}")
    for p in P4:
        g, gs = ms(kayit["gevsek"][p])
        s, ss_ = ms(kayit["siki"][p])
        yildiz = "  <<<" if p == "successful_source" else ""
        print(f"  {p:<20}{g:>+13.2f}+/-{gs:<6.2f}{s:>+13.2f}+/-{ss_:<6.2f}{s - g:>+10.2f}{yildiz}")
    yg, ygs = ms(kayit["yayilim_gevsek"])
    ys, yss = ms(kayit["yayilim_siki"])
    print(f"  {'YAYILIM (tohum ort)':<20}{yg:>13.2f}+/-{ygs:<6.2f}{ys:>13.2f}+/-{yss:<6.2f}{ys - yg:>+10.2f}")

    # protokol ORTALAMALARININ acikligi (makaledeki 10,24 buradan)
    for ad in ("gevsek", "siki"):
        ort = [np.mean(kayit[ad][p]) for p in P4]
        kayit[ad + "_ort_aciklik"] = max(ort) - min(ort)
        pos = [abs(v) for v in ort]
        kayit[ad + "_oran"] = max(pos) / min(pos) if min(pos) > 0 else float("nan")
    print(f"  {'ORT ACIKLIK':<20}{kayit['gevsek_ort_aciklik']:>13.2f}       "
          f"{kayit['siki_ort_aciklik']:>13.2f}")
    print(f"  {'ORAN (max/min)':<20}{kayit['gevsek_oran']:>13.2f} kat   "
          f"{kayit['siki_oran']:>13.2f} kat")
    sonuc[etiket] = kayit

# --- isaret kontrolu: SVHN'de isaret cevrilmesi degisiyor mu? ---
print(f"\n{'=' * 78}\nISARET KONTROLU (her olcumde isaret)\n{'=' * 78}")
for etiket, kayit in sonuc.items():
    for ad in ("gevsek", "siki"):
        isaretler = [np.sign(v) for p in P4 for v in kayit[ad][p]]
        arti = sum(1 for s in isaretler if s > 0)
        print(f"  {etiket:<16} {ad:<7}: {arti}/{len(isaretler)} pozitif")

(ROOT / "results/q1/_b2_olcum.json").write_text(
    json.dumps({k: {kk: (vv if not isinstance(vv, list) or not vv or not isinstance(vv[0], tuple)
                         else [list(t) for t in vv])
                    for kk, vv in v.items()} for k, v in sonuc.items()},
               indent=1, ensure_ascii=False), encoding="utf-8")
print("\nyazildi: results/q1/_b2_olcum.json")
