#!/usr/bin/env python3
"""E3: protokol yayilimini KIM suruyor -- temiz hata farki mi, basarili-kaynak mi?

BULGU (q1_e3_asimetri.py): asimetri yayilimi ile ciftin temiz hata farki
arasindaki egim NEGATIF cikti (-0,381). En buyuk yayilim, hata farki ~0 olan
ResNet<->WRN ciftindeydi (25,98 puan). Oradaki uc protokoller:
    hedef-dogru      -14,71
    basarili-kaynak  -35,02
Yani yayilimi suren sey fark degil, BASARILI-KAYNAK protokolunun tek basina
actigi mesafeydi.

Bu betik surucuyu AYRISTIRIR:
  A) 4 protokol yayilimi           (mevcut)
  B) basarili-kaynak HARIC 3 protokol yayilimi
  C) her protokol ciftinin acikligi
ve her birini ciftin temiz hata farkina karsi uydurur.

Eger B, fark ile POZITIF ve A negatifse: mekanizma anlatisi "temiz dogruluk
farki" ile SINIRLI olarak dogrudur; basarili-kaynak AYRI bir surucudur ve
makale bunu ayirmalidir.

Cikti: results/q1/e3_surucu_ayristirma.json
"""
import json
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
P = ["raw", "target_correct", "both_correct", "successful_source"]

d = json.loads((ROOT / "results/q1/e3_asimetri_fit.json").read_text(encoding="utf-8"))
ciftler = d["ciftler"]

x = np.array([c["x_temiz_hata_farki"] for c in ciftler])
kume = np.array([c["kume"] for c in ciftler])
uniq = sorted(set(kume))


def kb(y, B=10000, seed=42):
    rng = np.random.default_rng(seed)
    e = []
    for _ in range(B):
        take = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([np.flatnonzero(kume == t) for t in take])
        if len(set(x[idx])) < 2:
            continue
        b1, _ = np.polyfit(x[idx], y[idx], 1)
        e.append(b1)
    return np.percentile(e, [2.5, 97.5]).tolist() if e else [float("nan")] * 2


def fit(y, ad):
    b1, b0 = np.polyfit(x, y, 1)
    ci = kb(y)
    return {"ad": ad, "egim": float(b1), "kesisim": float(b0),
            "pearson_r": float(np.corrcoef(x, y)[0, 1]),
            "egim_GA95": ci, "GA_sifiri_iceriyor_mu": bool(ci[0] <= 0 <= ci[1]),
            "y_ort": float(y.mean()), "y_araligi": [float(y.min()), float(y.max())]}


y4 = np.array([c["y_asimetri_yayilimi"] for c in ciftler])
y3 = np.array([max(c["asimetri"][k] for k in P if k != "successful_source")
               - min(c["asimetri"][k] for k in P if k != "successful_source")
               for c in ciftler])

# hangi protokol kac kez UC (max veya min) oluyor
uc_sayaci = {k: {"max": 0, "min": 0} for k in P}
for c in ciftler:
    a = c["asimetri"]
    uc_sayaci[max(a, key=a.get)]["max"] += 1
    uc_sayaci[min(a, key=a.get)]["min"] += 1

# protokol cifti bazinda ortalama aciklik
ikili = {}
for k1, k2 in combinations(P, 2):
    farklar = np.array([abs(c["asimetri"][k1] - c["asimetri"][k2]) for c in ciftler])
    ikili[f"{k1} vs {k2}"] = {"ort_aciklik": float(farklar.mean()),
                              "max_aciklik": float(farklar.max())}

sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "n_cift": len(ciftler), "n_kume": len(uniq),
    "A_dort_protokol": fit(y4, "4 protokol yayilimi"),
    "B_basarili_kaynak_HARIC": fit(y3, "3 protokol yayilimi (basarili-kaynak haric)"),
    "protokol_uc_olma_sayilari": uc_sayaci,
    "protokol_cifti_ortalama_aciklik": dict(
        sorted(ikili.items(), key=lambda kv: -kv[1]["ort_aciklik"])),
}

A, B = sonuc["A_dort_protokol"], sonuc["B_basarili_kaynak_HARIC"]
if A["egim"] < 0 < B["egim"]:
    hukum = ("SURUCU AYRISTI. Basarili-kaynak protokolu CIKARILDIGINDA yayilim "
             f"temiz hata farkiyla POZITIF olcekleniyor (egim {B['egim']:.3f}, "
             f"GA {[round(v,3) for v in B['egim_GA95']]}); dahil edildiginde "
             f"iliski TERSINE donuyor (egim {A['egim']:.3f}). Yani makalenin "
             "'yayilim hedefler arasi temiz dogruluk farkindan gelir' mekanizma "
             "anlatisi UC PROTOKOL icin gecerli, DORDUNCU icin DEGILDIR. "
             "Basarili-kaynak, KAYNAGIN kendi gurbuzlugune bagli AYRI bir "
             "surucudur ve makale bunu ayirmak zorundadir.")
elif A["egim"] < 0 and B["egim"] < 0:
    hukum = ("IKISI DE NEGATIF. Mekanizma anlatisi bu model havuzunda "
             "DESTEKLENMIYOR; makale bunu raporlamalidir (K8).")
else:
    hukum = (f"A egim {A['egim']:.3f}, B egim {B['egim']:.3f}. "
             "Ayristirma net bir yon vermiyor; GA'lara bakiniz.")
sonuc["HUKUM"] = hukum

out = ROOT / "results/q1/e3_surucu_ayristirma.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"n = {len(ciftler)} cift / {len(uniq)} kume\n")
for k in ("A_dort_protokol", "B_basarili_kaynak_HARIC"):
    v = sonuc[k]
    print(f"{v['ad']:48s} egim {v['egim']:+.4f}  r {v['pearson_r']:+.3f}  "
          f"GA [{v['egim_GA95'][0]:+.3f}, {v['egim_GA95'][1]:+.3f}]"
          f"{'  (sifiri iceriyor)' if v['GA_sifiri_iceriyor_mu'] else ''}")
print("\nprotokol UC olma sayilari (max/min):")
for k, v in uc_sayaci.items():
    print(f"  {k:20s} max {v['max']:2d}  min {v['min']:2d}")
print("\nen genis protokol ciftleri (ortalama aciklik):")
for k, v in list(sonuc["protokol_cifti_ortalama_aciklik"].items())[:3]:
    print(f"  {k:45s} {v['ort_aciklik']:6.2f}")
print("\nHUKUM:", hukum)
print(f"-> {out}")
