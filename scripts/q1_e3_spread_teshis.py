#!/usr/bin/env python3
"""E3 TESHIS: nokta duzeyindeki 'spread' ne kadar OZDESLIK terimidir?

SORUN. E3 noktalarinda `spread`, TEK BIR YON icin dort protokol oraninin
acikligidir (max-min). Ama makalenin manset niceligi bu DEGIL: makale
"protokol yayilimi" derken IKI YON ARASINDAKI ASIMETRININ protokoller
boyunca ne kadar oynadigini kastediyor (CIFAR-10'da 10,45 · CIFAR-100'de
13,58 puan). Tek-yon acikligi ise CIFAR-100'de 37 puan mertebesinde.

Dahasi: tek-yon acikliginin buyuk kismi
    raw - target_correct = e * (1 - kos)
yani OZDESLIK terimi olabilir (bkz. ozdeslik_kontrol.json). Oyleyse E3'un
"yayilim ~ hedefin temiz hatasi" egimi buyuk olcude ARITMETIGI yeniden
olcuyor demektir ve EK B'nin amacladigi ampirik soruyu yanitlamiyordur.

BU BETIK TAHMIN ETMEZ, OLCER:
  1) spread'in kac puani identity terimidir (raw - target_correct)
  2) identity terimi CIKARILDIGINDA geriye kalan ARTIK yayilim ne olur
  3) her ikisinin hedefin temiz hatasina karsi egimi nedir
Egimler yakinsa, E3'un mevcut hali aritmetigi olcuyor demektir.

Cikti: results/q1/e3_spread_teshis.json
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
PTS = ROOT / "results/q1/e3_points"

pts = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PTS.glob("*.json"))]
if not pts:
    raise SystemExit(f"HATA: {PTS} bos")

satirlar = []
for p in pts:
    dort = [p["raw"], p["target_correct"], p["both_correct"], p["successful_source"]]
    spread = max(dort) - min(dort)
    ozdeslik_terimi = p["raw"] - p["target_correct"]     # = e*(1-kos), turetilebilir
    # identity terimi cikarildiginda: ham'i kosullu seviyesine indir, sonra ac
    dort_duzeltilmis = [p["raw"] - ozdeslik_terimi, p["target_correct"],
                        p["both_correct"], p["successful_source"]]
    artik_spread = max(dort_duzeltilmis) - min(dort_duzeltilmis)
    satirlar.append({
        "id": p["trajectory_id"], "yon": p.get("yon"), "dataset": p.get("dataset"),
        "arm": p.get("arm"),
        "e": p["target_clean_err"],
        "spread": spread,
        "ozdeslik_terimi": ozdeslik_terimi,
        "ozdeslik_payi_yuzde": round(100 * ozdeslik_terimi / spread, 2) if spread else None,
        "artik_spread": artik_spread,
        "raw_en_buyuk_mu": max(dort) == p["raw"],
    })

x = np.array([s["e"] for s in satirlar])
sp = np.array([s["spread"] for s in satirlar])
oz = np.array([s["ozdeslik_terimi"] for s in satirlar])
ar = np.array([s["artik_spread"] for s in satirlar])
pay = np.array([s["ozdeslik_payi_yuzde"] for s in satirlar if s["ozdeslik_payi_yuzde"] is not None])


def fit(y):
    b1, b0 = np.polyfit(x, y, 1)
    return {"egim": float(b1), "kesisim": float(b0),
            "pearson_r": float(np.corrcoef(x, y)[0, 1])}


sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "n_nokta": len(satirlar),
    "UYARI_NICELIK": "Buradaki 'spread' TEK YON icin dort protokol oraninin "
                     "acikligidir. Makalenin manset 'protokol yayilimi' "
                     "(CIFAR-10 10,45 · CIFAR-100 13,58) IKI YON ARASINDAKI "
                     "ASIMETRININ yayilimidir. IKISI AYNI NICELIK DEGILDIR.",
    "ozdeslik_payi_yuzde": {
        "min": float(pay.min()), "max": float(pay.max()), "ort": float(pay.mean())},
    "raw_her_zaman_en_buyuk_mu": bool(all(s["raw_en_buyuk_mu"] for s in satirlar)),
    "uydurmalar_x_hedefin_temiz_hatasi": {
        "spread": fit(sp),
        "ozdeslik_terimi": fit(oz),
        "ARTIK_spread": fit(ar),
    },
    "noktalar": satirlar,
}

e_sp = sonuc["uydurmalar_x_hedefin_temiz_hatasi"]["spread"]["egim"]
e_oz = sonuc["uydurmalar_x_hedefin_temiz_hatasi"]["ozdeslik_terimi"]["egim"]
e_ar = sonuc["uydurmalar_x_hedefin_temiz_hatasi"]["ARTIK_spread"]["egim"]
sonuc["HUKUM"] = (
    f"spread egimi {e_sp:.3f}, bunun {e_oz:.3f}'i OZDESLIK teriminden geliyor; "
    f"ozdeslik cikarilinca artik egim {e_ar:.3f}. "
    + ("OZDESLIK BASKIN: E3'un mevcut hali buyuk olcude ARITMETIGI olcuyor ve "
       "EK B'nin amacladigi ampirik soruyu yanitlamiyor. x ekseni ve y niceligi "
       "yeniden tanimlanmalidir."
       if abs(e_oz) > 0.5 * abs(e_sp) else
       "Ozdeslik terimi baskin DEGIL; artik yayilimin bagimsiz ampirik icerigi var.")
)

out = ROOT / "results/q1/e3_spread_teshis.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"n = {len(satirlar)} nokta")
print(f"ozdeslik payi (spread'in yuzde kaci): "
      f"%{pay.min():.1f} - %{pay.max():.1f}  (ort %{pay.mean():.1f})")
print(f"raw her zaman en buyuk protokol mu: {sonuc['raw_her_zaman_en_buyuk_mu']}")
print()
print(f"{'nicelik':20s} {'egim':>9s} {'r':>8s}")
for k, v in sonuc["uydurmalar_x_hedefin_temiz_hatasi"].items():
    print(f"{k:20s} {v['egim']:9.4f} {v['pearson_r']:8.4f}")
print()
print("HUKUM:", sonuc["HUKUM"])
print(f"-> {out}")
