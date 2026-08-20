#!/usr/bin/env python3
"""r=0,997 CEBIRSEL bir OZDESLIK mi, ampirik bir bulgu mu?

SORU. Makale, ham transfer orani ile kosullu oran arasindaki sapmanin hedefin
temiz hatasiyla aciklandigini r = 0,997 diye raporluyor. Ama:

  ham   = |{tum ornekler: hedef adv'de yanlis}| / N
  kos.  = |{hedef temiz-DOGRU: hedef adv'de yanlis}| / |temiz-dogru|

Temiz-YANLIS bir ornek saldiri altinda da yanlis kaliyorsa (ki beklenir),

  ham  = e + kos*(1-e)          e = hedefin temiz HATASI
  ham - kos = e*(1 - kos)       <-- OZDESLIK, olculen bir iliski DEGIL

Bu dogruysa r'nin 1'e yakin olmasi bir KESIF degil ARITMETIKTIR ve makale
bunu boyle sunmalidir. Yanlissa, artik (residual) gercek ampirik icerigi
tasir ve buyuklugu raporlanmalidir.

OLCUM. Ornek-bazli maskelerden dogrudan:
  1) P(adv yanlis | temiz yanlis)  -- ozdesligin dayandigi varsayim
  2) ham_tahmin = e + kos*(1-e)  vs  ham_gercek  -- artik
  3) artigin buyuklugu, sapmanin (ham-kos) yuzde kaci

Cikti: results/q1/ozdeslik_kontrol.json
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"

KAYNAKLAR = {
    "cifar10_C1": [ROOT / f"results/c1_c3/pair{i}" for i in (1, 2, 3)],
    "cifar100_E1": [ROOT / f"results/q1/cifar100/transfer/pair{i}" for i in (1, 2, 3)],
}

satirlar = []
for kume, dizinler in KAYNAKLAR.items():
    for d in dizinler:
        if not d.is_dir():
            continue
        for npz in sorted(d.glob("per_sample_*_to_*.npz")):
            ad = npz.stem[len("per_sample_"):]
            src, tgt = ad.split("_to_")
            if src == tgt:
                continue                      # kosegen = beyaz kutu, transfer degil
            z = np.load(npz)
            gerekli = {"target_clean_correct", "target_adv_wrong"}
            if not gerekli.issubset(set(z.files)):
                continue
            tc = z["target_clean_correct"].astype(bool)   # hedef temiz-DOGRU mu
            aw = z["target_adv_wrong"].astype(bool)       # hedef adv'de YANLIS mi
            n = tc.size

            e = 1.0 - tc.mean()                           # hedefin temiz HATASI
            ham = aw.mean()
            kos = aw[tc].mean() if tc.any() else np.nan

            # ozdesligin dayandigi varsayim
            temiz_yanlis = ~tc
            p_adv_yanlis_verili_temiz_yanlis = (
                aw[temiz_yanlis].mean() if temiz_yanlis.any() else np.nan)

            ham_tahmin = e + kos * (1.0 - e)
            artik = ham - ham_tahmin
            sapma = ham - kos
            satirlar.append({
                "kume": kume, "cift": d.name, "yon": f"{src}->{tgt}",
                "n": int(n),
                "hedef_temiz_hata_yuzde": round(100 * e, 4),
                "ham_yuzde": round(100 * ham, 4),
                "kosullu_yuzde": round(100 * kos, 4),
                "P_advyanlis_verili_temizyanlis": round(float(p_adv_yanlis_verili_temiz_yanlis), 6),
                "ham_TAHMIN_ozdeslikle_yuzde": round(100 * ham_tahmin, 4),
                "ARTIK_puan": round(100 * artik, 4),
                "sapma_ham_eksi_kosullu_puan": round(100 * sapma, 4),
                "artigin_sapmaya_orani_yuzde": round(100 * abs(artik) / abs(sapma), 3) if sapma else None,
            })

if not satirlar:
    raise SystemExit("HATA: hicbir per_sample npz okunamadi")

artiklar = np.array([s["ARTIK_puan"] for s in satirlar])
oranlar = np.array([s["artigin_sapmaya_orani_yuzde"] for s in satirlar
                    if s["artigin_sapmaya_orani_yuzde"] is not None])
pcond = np.array([s["P_advyanlis_verili_temizyanlis"] for s in satirlar])

ozet = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "n_yon": len(satirlar),
    "P_advyanlis_verili_temizyanlis": {
        "min": float(pcond.min()), "max": float(pcond.max()), "ort": float(pcond.mean())},
    "ARTIK_puan": {
        "min": float(artiklar.min()), "max": float(artiklar.max()),
        "mutlak_ort": float(np.abs(artiklar).mean()), "mutlak_max": float(np.abs(artiklar).max())},
    "artigin_sapmaya_orani_yuzde": {
        "min": float(oranlar.min()), "max": float(oranlar.max()), "ort": float(oranlar.mean())},
}
ozet["HUKUM"] = (
    "OZDESLIK PRATIKTE TAM: ham = e + kos*(1-e) iliskisi tum yonlerde "
    f"{ozet['ARTIK_puan']['mutlak_max']:.3f} puandan kucuk bir artikla tutuyor. "
    "Yani ham-kosullu sapmasinin hedefin temiz hatasiyla artmasi bir OLCUM "
    "BULGUSU DEGIL, ARITMETIK bir sonuctur; r'nin 1'e yakinligi da oyle. "
    "Makale bunu ampirik korelasyon olarak sunmamali, OZDESLIGI TUREtip "
    "artigi raporlamalidir. Iyi haber: boyle sunuldugunda iddia UC HEDEFE "
    "dayanmaktan cikar ve KUCUK-n sorunu ORTADAN KALKAR; ayrica iddia bu "
    "veri kumesine degil TUM calismalara genellenir."
    if ozet["ARTIK_puan"]["mutlak_max"] < 1.0 else
    "OZDESLIK TAM DEGIL: artik buyuk; iliskinin ampirik icerigi var ve "
    "artigin buyuklugu raporlanmalidir."
)

out = ROOT / "results/q1/ozdeslik_kontrol.json"
out.write_text(json.dumps({"ozet": ozet, "yonler": satirlar}, indent=2, ensure_ascii=False),
               encoding="utf-8")

print(f"{'kume':13s} {'yon':28s} {'e%':>7s} {'ham%':>7s} {'kos%':>7s} "
      f"{'tahmin%':>8s} {'artik':>7s} {'P(aw|cw)':>9s}")
print("-" * 92)
for s in satirlar:
    print(f"{s['kume']:13s} {s['yon']:28s} {s['hedef_temiz_hata_yuzde']:7.2f} "
          f"{s['ham_yuzde']:7.2f} {s['kosullu_yuzde']:7.2f} "
          f"{s['ham_TAHMIN_ozdeslikle_yuzde']:8.2f} {s['ARTIK_puan']:7.3f} "
          f"{s['P_advyanlis_verili_temizyanlis']:9.4f}")
print("-" * 92)
print(f"P(adv yanlis | temiz yanlis): {ozet['P_advyanlis_verili_temizyanlis']['min']:.4f} - "
      f"{ozet['P_advyanlis_verili_temizyanlis']['max']:.4f}")
print(f"ARTIK (puan): mutlak ort {ozet['ARTIK_puan']['mutlak_ort']:.4f}, "
      f"mutlak max {ozet['ARTIK_puan']['mutlak_max']:.4f}")
print(f"artik / sapma: %{ozet['artigin_sapmaya_orani_yuzde']['min']:.2f} - "
      f"%{ozet['artigin_sapmaya_orani_yuzde']['max']:.2f}")
print()
print("HUKUM:", ozet["HUKUM"])
print(f"-> {out}")
