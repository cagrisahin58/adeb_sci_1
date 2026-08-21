#!/usr/bin/env python3
"""E6 ON-KESTIRIM SINAMASI (L2 tehdit modeli).

On-kayit: results/q1_research/E6_ON_KAYIT.md §2. Uc SINANABILIR kestirim,
L2 sonuclari GORULMEDEN yazildi:

  O1 (yon)     L2 altinda da ham-kosullu sapma hedefin temiz hatasiyla
               POZITIF iliskili olacak (egim > 0).
  O2 (yayilim) Dort protokol arasindaki asimetri yayilimi EN AZ 2 PUAN olacak.
               (Alt sinir bilincli DUSUK: is, yayilimin L-infinity'dekiyle ayni
               BUYUKLUKTE oldugunu degil YOK OLMADIGINI gostermektir.)
  O3 (isaret)  CNN->ViT asimetrisinin isareti dort protokolde de POZITIF kalacak.

TUTMAZSA: hukum geri cekilmez, RAPORLANIR (K8). Tutmayan bir on-kestirim,
tezin tehdit modeline duyarli oldugunu gosterir ve bu da bir sonuctur.

BAGLAYICI CERCEVE (E6_ON_KAYIT §0): modeller L-infinity ile EGITILMISTIR.
Cikan mutlak sayilar L2-EGITILMIS RobustBench girdileriyle KARSILASTIRILAMAZ.

Cikti: results/q1/cifar10_l2/e6_onkestirim.json
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
L2 = ROOT / "results/q1/cifar10_l2"
PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]


def jl(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def olc_o1():
    """Kosegen-disi yonlerde (ham - kosullu) ~ hedefin temiz HATASI egimi."""
    x, y, ayrinti = [], [], []
    for i in (1, 2, 3):
        f = L2 / f"transfer/pair{i}/transfer_matrix.json"
        if not f.exists():
            continue
        for yon, v in jl(f)["results"].items():
            src, tgt = yon.split("->")
            if src == tgt:
                continue
            e = 100.0 - v["target_clean_acc"]
            sapma = v["raw_fooling"] - v["cond_fooling"]
            x.append(e)
            y.append(sapma)
            ayrinti.append({"cift": i, "yon": yon, "e": round(e, 2),
                            "sapma": round(sapma, 3)})
    if len(x) < 3:
        return {"DURUM": f"yetersiz nokta ({len(x)})", "n": len(x)}
    x, y = np.array(x), np.array(y)
    b1, b0 = np.polyfit(x, y, 1)
    return {"n_yon": len(x), "egim": float(b1), "kesisim": float(b0),
            "pearson_r": float(np.corrcoef(x, y)[0, 1]),
            "hedef_hatasi_araligi": [float(x.min()), float(x.max())],
            "GECTI_mi": bool(b1 > 0), "noktalar": ayrinti}


def olc_o2_o3():
    f = L2 / "transfer/e6_l2_transfer_summary.json"
    if not f.exists():
        return ({"DURUM": f"ozet yok: {f}"}, {"DURUM": "ozet yok"})
    d = jl(f)
    sp = d.get("protocol_spread_pp", {})
    o2 = {"yayilim_ort": sp.get("mean"), "yayilim_sd": sp.get("std"),
          "tohum_degerleri": sp.get("values"), "esik": 2.0,
          "GECTI_mi": bool(sp.get("mean") is not None and sp["mean"] >= 2.0)}
    farklar, hepsi_poz = {}, True
    for p in PROTOKOLLER:
        v = d["protocols"][p]["diff"]
        farklar[p] = {"ort": v["mean"], "sd": v["std"], "degerler": v["values"]}
        if not all(t > 0 for t in v["values"]):
            hepsi_poz = False
    n_poz = sum(1 for p in PROTOKOLLER for t in d["protocols"][p]["diff"]["values"] if t > 0)
    n_tot = sum(len(d["protocols"][p]["diff"]["values"]) for p in PROTOKOLLER)
    o3 = {"farklar": farklar, "pozitif_olcum": f"{n_poz}/{n_tot}",
          "GECTI_mi": bool(hepsi_poz)}
    return o2, o3


o1 = olc_o1()
o2, o3 = olc_o2_o3()

sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "ON_KAYIT": "results/q1_research/E6_ON_KAYIT.md §2 (L2 sonuclari GORULMEDEN yazildi)",
    "BAGLAYICI_CERCEVE": "Modeller L-infinity ile EGITILMISTIR; E6 onlari L2 altinda "
                         "OLCER. Mutlak sayilar L2-EGITILMIS referanslarla "
                         "KARSILASTIRILAMAZ (E6_ON_KAYIT §0).",
    "O1_yon": o1, "O2_yayilim": o2, "O3_isaret": o3,
}

gecen = [k for k, v in (("O1", o1), ("O2", o2), ("O3", o3)) if v.get("GECTI_mi")]
kalan = [k for k, v in (("O1", o1), ("O2", o2), ("O3", o3))
         if "GECTI_mi" in v and not v["GECTI_mi"]]
eksik = [k for k, v in (("O1", o1), ("O2", o2), ("O3", o3)) if "GECTI_mi" not in v]
sonuc["HUKUM"] = {
    "gecen": gecen, "kalan": kalan, "olculemeyen": eksik,
    # DIKKAT: "olculemedi" ile "tutmadi" AYNI SEY DEGILDIR. Ilk surum veri
    # henuz uretilmemisken "0/3 tuttu" diyordu; bu, sonradan "on-kestirim
    # basarisiz" diye okunabilirdi. Uc durum ayri raporlanir.
    "yorum": (
        "HENUZ OLCULEMEDI: E6 ciktilari uretilmedi. Bu bir BASARISIZLIK DEGILDIR; "
        f"eksik olan olcumler: {eksik}."
        if len(eksik) == 3 else
        "Uc on-kestirimin ucu de TUTTU: protokol duyarliligi tehdit modeli "
        "degisince YOK OLMUYOR."
        if len(gecen) == 3 else
        f"{len(gecen)}/3 TUTTU, {len(kalan)} TUTMADI"
        + (f", {len(eksik)} HENUZ OLCULEMEDI" if eksik else "")
        + ". TUTMAYANLAR RAPORLANIR (K8): tutmayan bir on-kestirim, tezin tehdit "
        "modeline duyarli oldugunu gosterir ve bu da bir sonuctur."),
}

L2.mkdir(parents=True, exist_ok=True)
out = L2 / "e6_onkestirim.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print("=== E6 ON-KESTIRIM SINAMASI (L2) ===")
if "egim" in o1:
    print(f"O1 yon     : egim {o1['egim']:+.4f}  r {o1['pearson_r']:+.3f}  "
          f"({o1['n_yon']} yon)  -> {'GECTI' if o1['GECTI_mi'] else 'KALDI'}")
else:
    print(f"O1 yon     : {o1.get('DURUM')}")
if o2.get("yayilim_ort") is not None:
    print(f"O2 yayilim : {o2['yayilim_ort']:.2f} puan (esik 2,0)  -> "
          f"{'GECTI' if o2['GECTI_mi'] else 'KALDI'}")
else:
    print(f"O2 yayilim : {o2.get('DURUM')}")
if "pozitif_olcum" in o3:
    print(f"O3 isaret  : {o3['pozitif_olcum']} pozitif  -> "
          f"{'GECTI' if o3['GECTI_mi'] else 'KALDI'}")
    for p, v in o3["farklar"].items():
        print(f"             {p:20s} {v['ort']:+7.2f} +/- {v['sd']:.2f}")
else:
    print(f"O3 isaret  : {o3.get('DURUM')}")
print()
print("HUKUM:", sonuc["HUKUM"]["yorum"])
print(f"-> {out}")
sys.exit(0 if not kalan and not eksik else 1)
