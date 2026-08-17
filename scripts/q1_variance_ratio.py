#!/usr/bin/env python3
"""Olcek-uyumlu varyans siralamasi artefakti.

Makalede "protokol yayilimi ~ egitim-kosusu sd'sinin yirmi kati" seklinde
raporlanan oran OLCEK-UYUMSUZDU: payi transfer ASIMETRISININ araligi,
paydasi ise MUTLAK DOGRULUGUN sd'si idi. Bu betik ayni nicelik (asimetri =
CNN->ViT eksi ViT->CNN kandirma orani) uzerinde her iki yayilimi da hesaplar
ve oranin tanima ne kadar duyarli oldugunu gosterir.

Girdi : results/c1_transfer/c1_transfer_summary.json (3 tohum cifti x 4 protokol)
Cikti : results/q1/variance_ratio.json
"""

import json
import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "results" / "c1_transfer" / "c1_transfer_summary.json"
OUT = ROOT / "results" / "q1" / "variance_ratio.json"

PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]


def sd(x):
    """Ornek standart sapmasi (ddof=1) — makale boyunca kullanilan tanim."""
    return float(np.std(np.asarray(x, dtype=float), ddof=1))


def main():
    data = json.load(open(SRC))["protocols"]

    # asimetri (diff) degerleri: protokol -> tohum listesi
    diff = {p: [float(v) for v in data[p]["diff"]["values"]] for p in PROTOCOLS}
    n_seeds = {p: len(v) for p, v in diff.items()}
    assert len(set(n_seeds.values())) == 1, f"tohum sayilari esit degil: {n_seeds}"
    n = next(iter(n_seeds.values()))

    # ---- PAY: protokol degistirmenin ayni tohum ciftinde asimetriyi oynatmasi
    per_seed = [[diff[p][i] for p in PROTOCOLS] for i in range(n)]
    proto_range = [max(v) - min(v) for v in per_seed]          # makaledeki 10.45
    proto_sd = [sd(v) for v in per_seed]                        # olcek-uyumlu sd

    # ---- PAYDA: yeniden egitmenin AYNI nicelikte yaptigi oynama
    seed_sd = {p: sd(diff[p]) for p in PROTOCOLS}
    seed_range = {p: max(diff[p]) - min(diff[p]) for p in PROTOCOLS}

    # ---- oran: hangi tanimla? hepsini yaz, tek sayi manseti KURMA
    ratios = {
        "sd_vs_sd": {
            "tanim": "protokol sd'si (tohum icinde, 4 protokol) / kosum sd'si (protokol icinde, 3 tohum)",
            "pay_ortalama": round(float(np.mean(proto_sd)), 4),
            "degerler": {p: round(float(np.mean(proto_sd)) / seed_sd[p], 2) for p in PROTOCOLS},
        },
        "aralik_vs_aralik": {
            "tanim": "protokol araligi (10.45) / kosum araligi (protokol icinde)",
            "pay_ortalama": round(float(np.mean(proto_range)), 4),
            "degerler": {p: round(float(np.mean(proto_range)) / seed_range[p], 2) for p in PROTOCOLS},
        },
        "aralik_vs_sd_OLCEK_UYUMSUZ": {
            "tanim": "MAKALEDE KULLANILAN HATALI BICIM: aralik / sd. Sadece kayit icin.",
            "degerler": {p: round(float(np.mean(proto_range)) / seed_sd[p], 2) for p in PROTOCOLS},
        },
    }

    tum_oranlar = [
        v for k, d in ratios.items() if not k.endswith("OLCEK_UYUMSUZ")
        for v in d["degerler"].values()
    ]

    result = {
        "kaynak": str(SRC.relative_to(ROOT)),
        "n_tohum_cifti": n,
        "protokoller": PROTOCOLS,
        "asimetri_degerleri_tohum_bazli": diff,
        "PAY_protokol_etkisi": {
            "aralik_tohum_bazli": [round(v, 4) for v in proto_range],
            "aralik_ortalama": round(float(np.mean(proto_range)), 4),
            "aralik_sd": round(sd(proto_range), 4),
            "sd_tohum_bazli": [round(v, 4) for v in proto_sd],
            "sd_ortalama": round(float(np.mean(proto_sd)), 4),
        },
        "PAYDA_kosum_etkisi_AYNI_NICELIK": {
            "sd_protokol_bazli": {p: round(seed_sd[p], 4) for p in PROTOCOLS},
            "sd_min": round(min(seed_sd.values()), 4),
            "sd_max": round(max(seed_sd.values()), 4),
            "aralik_protokol_bazli": {p: round(seed_range[p], 4) for p in PROTOCOLS},
        },
        "ORAN_TANIMA_DUYARLI": ratios,
        "ORAN_ACIKLIGI": {
            "min": round(min(tum_oranlar), 2),
            "max": round(max(tum_oranlar), 2),
            "yorum": (
                "Tek bir kat-degeri manseti KURULAMAZ: olcek-uyumlu iki tanim "
                "arasinda oran {:.1f}x-{:.1f}x araliginda oynuyor. Ayrica en buyuk "
                "asimetri yayilimini veren protokol (successful_source) ayni zamanda "
                "en buyuk kosum sd'sine sahip; yani pay ve payda bagimsiz degil."
            ).format(min(tum_oranlar), max(tum_oranlar)),
        },
        "EN_BUYUK_KOSUM_SD_PROTOKOLU": max(seed_sd, key=seed_sd.get),
        "EN_BUYUK_ASIMETRI_PROTOKOLU": max(PROTOCOLS, key=lambda p: float(np.mean(diff[p]))),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
