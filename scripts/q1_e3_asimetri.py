#!/usr/bin/env python3
"""E3 -- DOGRU NICELIK: ASIMETRININ protokoller arasi yayilimi.

NEDEN YENIDEN. Mevcut E3 noktalari TEK YON icin dort protokol oraninin
acikligini olcuyordu. Teshis (q1_e3_spread_teshis.py) o acikligin ortalama
%82'sinin OZDESLIK terimi (ham - hedef_dogru = e*(1-kos)) oldugunu, ozdeslik
cikarilinca egimin 0,608'den 0,070'e dustugunu gosterdi. Yani o nicelik
ampirik degil ARITMETIKTI.

Makalenin manset niceligi ise farklidir ve EK B'de ilan edilen budur:
  y = ASIMETRININ (A->B eksi B->A) dort protokol arasindaki YAYILIMI
  x = CIFTIN temiz dogruluk FARKI
CIFAR-10'da y = 10,45 · CIFAR-100'de 13,58 puandir.

Asimetride ozdeslik terimleri KISMEN SADELESIR:
  ham asimetri     = (e_B - e_A) + [kos_AB(1-e_B) - kos_BA(1-e_A)]
  hedef-dogru asim = kos_AB - kos_BA
Fark, once (e_B - e_A) yani CIFTIN HATA FARKI tarafindan surulur -- x ekseninin
cift farki olmasinin sebebi tam olarak budur.

Bu betik mevcut nokta json'larini YONE GORE ESLESTIRIR, asimetri yayilimini
kurar ve kume bootstrap ile uydurur. YENI GPU KOSUMU GEREKTIRMEZ.

Cikti: results/q1/e3_asimetri_fit.json
"""
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
PTS = ROOT / "results/q1/e3_points"
PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]

# --- ON-KAYITLI BILESIM (EK E.1/E.5) ---
# B kolu 18 nokta / 6 kumedir; SVHN uydurmaya girmez, BAGIMSIZ tutarlilik
# kontrolu olarak kullanilir. E3B_SVHN=1 duyarlilik kolunu acar.
SVHN_DAHIL = os.environ.get("E3B_SVHN", "0") == "1"

pts = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(PTS.glob("*.json"))]
if not pts:
    raise SystemExit(f"HATA: {PTS} bos")

_svhn = [q for q in pts if q.get("dataset") == "svhn"]
if not SVHN_DAHIL:
    pts = [q for q in pts if q.get("dataset") != "svhn"]
    print(f"ON-KAYITLI BILESIM: SVHN'in {len(_svhn)} noktasi uydurmanin DISINDA "
          f"(EK E.5: bagimsiz tutarlilik kontrolu). Duyarlilik icin E3B_SVHN=1.")
else:
    print(f"DUYARLILIK KOLU: SVHN'in {len(_svhn)} noktasi uydurmaya DAHIL "
          f"(kayitli bilesim DEGIL).")

# --- yonleri (kume, cift) anahtarina gore topla ---
gruplar = defaultdict(dict)
atlanan = []
for p in pts:
    yon = p.get("yon")
    if not yon or "->" not in yon:
        atlanan.append({"neden": "yon alani yok", "id": p.get("trajectory_id"), "epoch": p.get("epoch")})
        continue
    src, tgt = yon.split("->")
    kd = p.get("kaynak_dizin", "")
    m = re.search(r"pair(\d+)", kd)
    cift = m.group(1) if m else "?"
    anahtar = (p.get("arm"), p.get("dataset"), cift, tuple(sorted([src, tgt])))
    gruplar[anahtar][(src, tgt)] = p

satirlar, eksik_es = [], []
for anahtar, yonler in sorted(gruplar.items(), key=lambda kv: str(kv[0])):
    kol, ds, cift, ikili = anahtar
    if len(yonler) != 2:
        eksik_es.append({"anahtar": str(anahtar), "bulunan_yon": len(yonler)})
        continue
    (s1, t1), (s2, t2) = sorted(yonler.keys())
    ileri, geri = yonler[(s1, t1)], yonler[(s2, t2)]

    # asimetri = ileri - geri, HER PROTOKOLDE
    asim = {k: ileri[k] - geri[k] for k in PROTOKOLLER}
    yayilim = max(asim.values()) - min(asim.values())

    # x: ciftin temiz hata FARKI (mutlak)
    e_ileri_hedef = ileri["target_clean_err"]     # t1'in hatasi
    e_geri_hedef = geri["target_clean_err"]       # t2'nin hatasi
    fark = abs(e_ileri_hedef - e_geri_hedef)

    # OZDESLIKTEN TURETILEN ongoru: ham asimetri - hedef-dogru asimetri
    #   = (e_t1 - e_t2) - [kos_ileri*e_t1 - kos_geri*e_t2]
    kos_i, kos_g = ileri["target_correct"] / 100.0, geri["target_correct"] / 100.0
    ongoru_ham_eksi_tc = ((e_ileri_hedef - e_geri_hedef)
                          - (kos_i * e_ileri_hedef - kos_g * e_geri_hedef))
    gercek_ham_eksi_tc = asim["raw"] - asim["target_correct"]

    satirlar.append({
        "kol": kol, "dataset": ds, "cift": cift,
        "yon_ileri": f"{s1}->{t1}", "yon_geri": f"{s2}->{t2}",
        "e_hedef_ileri": e_ileri_hedef, "e_hedef_geri": e_geri_hedef,
        "x_temiz_hata_farki": fark,
        "asimetri": {k: round(v, 4) for k, v in asim.items()},
        "y_asimetri_yayilimi": yayilim,
        "ozdeslik_ongorusu_ham_eksi_tc": ongoru_ham_eksi_tc,
        "gercek_ham_eksi_tc": gercek_ham_eksi_tc,
        "ongoru_artigi": gercek_ham_eksi_tc - ongoru_ham_eksi_tc,
        "kume": f"{ds}_pair{cift}",
    })

if len(satirlar) < 3:
    raise SystemExit(f"HATA: yalniz {len(satirlar)} eslesmis cift; uydurma yapilamaz")

x = np.array([s["x_temiz_hata_farki"] for s in satirlar])
y = np.array([s["y_asimetri_yayilimi"] for s in satirlar])
kume = np.array([s["kume"] for s in satirlar])
uniq = sorted(set(kume))
artik = np.array([s["ongoru_artigi"] for s in satirlar])


def kume_bootstrap(y, x, kume, uniq, B=10000, seed=42):
    rng = np.random.default_rng(seed)
    egimler = []
    for _ in range(B):
        take = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([np.flatnonzero(kume == t) for t in take])
        if len(set(x[idx])) < 2:
            continue
        b1, _ = np.polyfit(x[idx], y[idx], 1)
        egimler.append(b1)
    if not egimler:
        return [float("nan")] * 2
    return np.percentile(egimler, [2.5, 97.5]).tolist()


b1, b0 = np.polyfit(x, y, 1)
ci = kume_bootstrap(y, x, kume, uniq)

sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "NICELIK": "y = ASIMETRININ dort protokol arasindaki yayilimi (puan); "
               "x = ciftin temiz HATA farki (puan). Makalenin manset niceligiyle "
               "AYNI turdendir (CIFAR-10 10,45 · CIFAR-100 13,58).",
    "n_eslesmis_cift": len(satirlar),
    "n_kume": len(uniq),
    "SERBESTLIK_DERECESI_NOTU": f"Cikarim {len(uniq)} KUME uzerinden kume bootstrap "
                                f"iledir; n={len(satirlar)} serbestlik derecesi DEGILDIR.",
    "x_araligi": [float(x.min()), float(x.max())],
    "y_araligi": [float(y.min()), float(y.max())],
    "uydurma": {"egim": float(b1), "kesisim": float(b0),
                "pearson_r": float(np.corrcoef(x, y)[0, 1]) if len(set(x)) > 1 else None,
                "egim_GA95_kume_bootstrap": ci},
    "OZDESLIK_ONGORUSU": {
        "aciklama": "ham asimetri eksi hedef-dogru asimetri, ozdeslikten TURETILIR: "
                    "(e_1 - e_2) - (kos_1*e_1 - kos_2*e_2). Artik kucukse bu bilesen "
                    "olculmeden hesaplanabilir demektir.",
        "artik_mutlak_ort": float(np.abs(artik).mean()),
        "artik_mutlak_max": float(np.abs(artik).max()),
    },
    "eslesmeyen_gruplar": eksik_es,
    "yon_alani_olmayan_noktalar": len(atlanan),
    "ciftler": satirlar,
}

out = ROOT / ("results/q1/e3_asimetri_fit_svhnli.json" if SVHN_DAHIL
              else "results/q1/e3_asimetri_fit.json")
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"eslesmis cift : {len(satirlar)}  (kume: {len(uniq)})")
if eksik_es:
    print(f"eslesmeyen    : {len(eksik_es)} grup -> {eksik_es[:3]}")
if atlanan:
    print(f"yon alani yok : {len(atlanan)} nokta (A kolu noktalari henuz yok olabilir)")
print()
print(f"{'kume':16s} {'x (hata farki)':>15s} {'y (asim. yayilim)':>18s}")
for s in satirlar:
    print(f"{s['kume']:16s} {s['x_temiz_hata_farki']:15.2f} {s['y_asimetri_yayilimi']:18.2f}")
print()
print(f"egim {b1:.4f}  kesisim {b0:.4f}  GA95 [{ci[0]:.4f}, {ci[1]:.4f}]")
print(f"ozdeslik ongorusu artigi: mutlak ort {np.abs(artik).mean():.4f}, "
      f"max {np.abs(artik).max():.4f} puan")
print(f"-> {out}")
