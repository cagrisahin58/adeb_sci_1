#!/usr/bin/env python3
"""C3 karistirici korelasyonunun KESINLIGI — n=6 mi n=3 mu?

c1_c3_aggregate.py, (ham - kosullu) sapmasini hedefin temiz hatasina karsi
KOSEGEN-DISI 6 nokta uzerinde regresyona sokuyor ve Pearson r veriyor
(CIFAR-10'da 0,997). Ama o 6 nokta 3 HEDEF x 2 KAYNAK'tan gelir: x degiskeni
yalnizca UC AYRI DEGER alir. Yani noktalar bagimsiz degildir ve n=6 varsayimi
kesinligi ABARTIR.

Bu betik uc sayiyi birlikte verir:
  1. n=6 (mevcut rapor) r ve Fisher-z %95 GA'si
  2. n=3 (hedef duzeyinde toplanmis) r ve GA'si  -- gercek serbestlik derecesi
  3. iki veri kumesi arasinda karsilastirma

Kullanim:
  docker exec -w /workspace adeb_eval python scripts/q1_c3_precision.py
"""

import json
import math
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
OUT = os.path.join(ROOT, "results", "q1", "c3_precision.json")

SETS = {
    "cifar10": "results/c1_c3",
    "cifar100": "results/q1/cifar100/transfer",
}


def fisher_ci(r, n, alpha=0.05):
    """Fisher-z %95 GA. n < 4 ise tanimsiz (SE = 1/sqrt(n-3))."""
    if n < 4 or abs(r) >= 1.0:
        return None
    z = math.atanh(r)
    se = 1.0 / math.sqrt(n - 3)
    k = 1.959963984540054
    return [round(math.tanh(z - k * se), 4), round(math.tanh(z + k * se), 4)]


def collect(d):
    """pair*/transfer_matrix.json -> kosegen-disi (hedef_hata, sapma) noktalari."""
    acc = {}
    for p in (1, 2, 3):
        f = os.path.join(ROOT, d, f"pair{p}", "transfer_matrix.json")
        if not os.path.exists(f):
            return None
        with open(f, encoding="utf-8") as fh:
            js = json.load(fh)
        for k, v in js["results"].items():
            e = acc.setdefault(k, {"raw": [], "cond": [], "tgt_clean": []})
            e["raw"].append(v["raw_fooling"])
            e["cond"].append(v["cond_fooling"])
            e["tgt_clean"].append(v["target_clean_acc"])

    pts = []
    for k, v in acc.items():
        src, tgt = k.split("->")
        if src == tgt:
            continue
        gap = float(np.mean(v["raw"]) - np.mean(v["cond"]))
        err = float(100.0 - np.mean(v["tgt_clean"]))
        pts.append({"src": src, "tgt": tgt, "gap": gap, "tgt_err": err})
    return pts


def main():
    out = {
        "aciklama": (
            "Kosegen-disi 6 nokta 3 HEDEF x 2 KAYNAK'tir; x degiskeni yalniz 3 "
            "ayri deger alir. n=6 varsayan Pearson GA'si kesinligi ABARTIR. "
            "Hedef duzeyinde toplanmis n=3 hesabi gercek serbestlik derecesini "
            "yansitir ama Fisher-z GA'si n<4'te TANIMSIZDIR -- yani bu "
            "korelasyona GA verilemiyor, bu da baslibasina raporlanmasi gereken "
            "bir sinirlamadir."
        ),
        "veri_kumeleri": {},
    }

    for name, d in SETS.items():
        pts = collect(d)
        if pts is None:
            out["veri_kumeleri"][name] = {"durum": "EKSIK", "dizin": d}
            continue

        gaps = np.array([p["gap"] for p in pts])
        errs = np.array([p["tgt_err"] for p in pts])
        r6 = float(np.corrcoef(errs, gaps)[0, 1])
        s6, i6 = np.polyfit(errs, gaps, 1)

        # hedef duzeyinde topla (her hedef icin 2 kaynak ortalamasi)
        by_t = {}
        for p in pts:
            by_t.setdefault(p["tgt"], []).append(p)
        t_err, t_gap, tnames = [], [], []
        for t, lst in sorted(by_t.items()):
            t_err.append(float(np.mean([q["tgt_err"] for q in lst])))
            t_gap.append(float(np.mean([q["gap"] for q in lst])))
            tnames.append(t)
        t_err_a, t_gap_a = np.array(t_err), np.array(t_gap)
        r3 = float(np.corrcoef(t_err_a, t_gap_a)[0, 1])
        s3, i3 = np.polyfit(t_err_a, t_gap_a, 1)

        # x-ekseni AYRIKLIGI: iki hedefin temiz hatasi cakisiyorsa korelasyon
        # uc nokta uzerinden degil IKI KUME uzerinden hesaplaniyor demektir.
        srt = sorted(t_err)
        rng = srt[-1] - srt[0]
        min_gap = min(srt[i + 1] - srt[i] for i in range(len(srt) - 1))
        cakisik = min_gap < 0.1 * rng if rng > 0 else True

        out["veri_kumeleri"][name] = {
            "n_kosegen_disi": len(pts),
            "n_ayri_hedef": len(by_t),
            "X_AYRIKLIGI": {
                "hedef_hatalari_sirali": [round(v, 2) for v in srt],
                "aralik": round(rng, 2),
                "en_kucuk_ara": round(min_gap, 2),
                "en_kucuk_ara_aralik_orani": round(min_gap / rng, 4) if rng > 0 else None,
                "IKI_HEDEF_CAKISIYOR": bool(cakisik),
                "etkin_ayri_x_degeri": (len(by_t) - 1) if cakisik else len(by_t),
                "uyari": (
                    "Iki hedefin temiz hatasi cakisik -> korelasyon fiilen IKI KUME "
                    "uzerinden hesaplaniyor. Dogrusal iliski icin GUCLU KANIT DEGILDIR."
                ) if cakisik else "Uc hedef de ayrik; korelasyon uc nokta uzerinden.",
            },
            "hedefler": tnames,
            "hedef_temiz_hatasi": [round(v, 2) for v in t_err],
            "hedef_sapmasi": [round(v, 2) for v in t_gap],
            "RAPOR_EDILEN_n6": {
                "pearson_r": round(r6, 4),
                "egim": round(float(s6), 4),
                "kesisim": round(float(i6), 4),
                "fisher_95_GA": fisher_ci(r6, len(pts)),
                "uyari": "noktalar bagimsiz DEGIL; bu GA kesinligi abartir",
            },
            "HEDEF_DUZEYI_n3": {
                "pearson_r": round(r3, 4),
                "egim": round(float(s3), 4),
                "kesisim": round(float(i3), 4),
                "fisher_95_GA": fisher_ci(r3, len(by_t)),
                "not": "n=3 -> Fisher-z GA'si TANIMSIZ (SE = 1/sqrt(n-3))",
            },
        }

    ok = [k for k, v in out["veri_kumeleri"].items() if "RAPOR_EDILEN_n6" in v]
    if len(ok) == 2:
        a, b = out["veri_kumeleri"]["cifar10"], out["veri_kumeleri"]["cifar100"]
        out["HUKUM"] = {
            "yon_korunuyor_mu": bool(a["RAPOR_EDILEN_n6"]["egim"] > 0
                                     and b["RAPOR_EDILEN_n6"]["egim"] > 0),
            "cifar10_r_n6": a["RAPOR_EDILEN_n6"]["pearson_r"],
            "cifar100_r_n6": b["RAPOR_EDILEN_n6"]["pearson_r"],
            "cifar10_r_n3": a["HEDEF_DUZEYI_n3"]["pearson_r"],
            "cifar100_r_n3": b["HEDEF_DUZEYI_n3"]["pearson_r"],
            "yorum": (
                "B.4 madde 3 YONSELDIR ('sapma hedefin temiz hatasiyla ARTMALI'), "
                "bir r degerine baglanmis degildir. Iki veri kumesinde de egim "
                "POZITIF ise on-kestirim dogrulanir. Ancak makale r=0,997'yi "
                "NOKTA KESTIRIMI olarak veriyor; bu deger 3 hedefe dayandigi icin "
                "kesinligi abartilmis olabilir ve boyle nitelenmelidir."
            ),
        }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
