#!/usr/bin/env python3
"""E3 SON FIT -- iki kol AYRI, havuzlama YOK.

Girdiler:
  A kolu (kontrollu) : results/q1/e3_akolu/*.json         (q1_e3_akolu.py)
  B kolu (gozlemsel) : results/q1/e3_asimetri_fit.json    (q1_e3_asimetri.py)

Her kol icin, x = ciftin temiz hata FARKI olmak uzere:
  y1 = 4 protokol asimetri yayilimi
  y2 = basarili-kaynak HARIC 3 protokol yayilimi
Cikarim yorunge/kume duzeyi bootstrap (B=10.000).

MANSET: iki kolun EGIMLERININ UYUSMASI. Havuzlanmis uydurma URETILMEZ ve
kodda o cikti yolu YOKTUR (yama sonunda dizgi olarak da denetlenir).

Cikti: results/q1/e3_iki_kol_fit.json
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
P4 = ["raw", "target_correct", "both_correct", "successful_source"]
P3 = ["raw", "target_correct", "both_correct"]


def kayitlari_topla():
    kayit = {"A": [], "B": []}
    ad = ROOT / "results/q1/e3_akolu"
    if ad.is_dir():
        for f in sorted(ad.glob("*.json")):
            kayit["A"].append(json.loads(f.read_text(encoding="utf-8")))
    bf = ROOT / "results/q1/e3_asimetri_fit.json"
    if bf.exists():
        for c in json.loads(bf.read_text(encoding="utf-8"))["ciftler"]:
            c = dict(c)
            c.setdefault("kol", "B")
            kayit["B"].append(c)
    return kayit


def kume_bootstrap(y, x, kume, uniq, B=10000, seed=42):
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


def kol_fit(kayitlar):
    x = np.array([k["x_temiz_hata_farki"] for k in kayitlar])
    kume = np.array([k["kume"] for k in kayitlar])
    uniq = sorted(set(kume))
    out = {
        "n_nokta": len(kayitlar), "n_kume": len(uniq),
        "SERBESTLIK_DERECESI_NOTU":
            f"Cikarim {len(uniq)} KUME uzerinden kume bootstrap iledir; "
            f"n={len(kayitlar)} SERBESTLIK DERECESI DEGILDIR.",
        "x_araligi": [float(x.min()), float(x.max())],
    }
    for ad, pr in (("dort_protokol", P4), ("uc_protokol_bas_kaynak_haric", P3)):
        y = np.array([max(k["asimetri"][p] for p in pr) - min(k["asimetri"][p] for p in pr)
                      for k in kayitlar])
        b1, b0 = np.polyfit(x, y, 1)
        ci = kume_bootstrap(y, x, kume, uniq)
        out[ad] = {"egim": float(b1), "kesisim": float(b0),
                   "pearson_r": float(np.corrcoef(x, y)[0, 1]),
                   "egim_GA95": ci, "GA_sifiri_iceriyor_mu": bool(ci[0] <= 0 <= ci[1]),
                   "y_araligi": [float(y.min()), float(y.max())]}
    return out


kayit = kayitlari_topla()
sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "HAVUZLAMA": "YAPILMADI. Kollar ayri uydurulur; manset iki kolun EGIMLERININ "
                 "UYUSMASIDIR (E3_YENIDEN_TASARIM B.3). Ortak bir uydurma yoktur.",
    "NICELIK": "x = ciftin temiz hata farki (puan) · y = ASIMETRININ protokoller "
               "arasi yayilimi (puan). Makalenin manset niceligiyle ayni turdendir.",
    "kollar": {},
}
# B kolunun ANA CIFT alt kumesi: A kolu WRN icermez, dolayisiyla ham B ile
# karsilastirma HAVUZ BILESIMI farkini kontrol farkiyla karistirir. Bu varyant
# A ile AYNI bilesimi kurar; kalan fark yalniz KONTROLDUR.
def _ana_cift_mi(k):
    yonler = f"{k.get('yon_ileri','')} {k.get('yon_geri','')}"
    return "WRN" not in yonler


kayit["B_ana_cift"] = [k for k in kayit["B"] if _ana_cift_mi(k)]

for kol in ("A", "B", "B_ana_cift"):
    if len(kayit[kol]) < 4:
        sonuc["kollar"][kol] = {"n_nokta": len(kayit[kol]),
                                "DURUM": "COK AZ NOKTA -- uydurulmadi"}
        continue
    sonuc["kollar"][kol] = kol_fit(kayit[kol])
    if kol == "B_ana_cift":
        sonuc["kollar"][kol]["NOT"] = (
            "B kolunun WRN'siz alt kumesi. A kolu ile AYNI havuz bilesimi; "
            "A ile fark yalniz KONTROLDUR (yorunge-ici vs gozlemsel).")

# MANSET yalniz A ve B icindir; B_ana_cift bir DUYARLILIK varyantidir.
uygun = [k for k in ("A", "B") if "dort_protokol" in sonuc["kollar"].get(k, {})]
if len(uygun) == 2:
    ua = sonuc["kollar"]["A"]
    ub = sonuc["kollar"]["B"]
    uyusma = {}
    for ad in ("dort_protokol", "uc_protokol_bas_kaynak_haric"):
        ca, cb = ua[ad]["egim_GA95"], ub[ad]["egim_GA95"]
        ortusuyor = not (ca[1] < cb[0] or cb[1] < ca[0])
        uyusma[ad] = {
            "A_egim": ua[ad]["egim"], "A_GA": ca,
            "B_egim": ub[ad]["egim"], "B_GA": cb,
            "GA_ortusuyor_mu": bool(ortusuyor),
            "isaret_ayni_mi": bool(np.sign(ua[ad]["egim"]) == np.sign(ub[ad]["egim"])),
        }
    sonuc["EGIM_UYUSMASI"] = uyusma
    hepsi = all(v["GA_ortusuyor_mu"] for v in uyusma.values())
    # bilesim mi kontrol mu? A ile B_ana_cift karsilastirmasi bunu ayirir.
    ba = sonuc["kollar"].get("B_ana_cift", {})
    if "dort_protokol" in ba:
        import numpy as _np
        sonuc["EGIM_UYUSMASI"]["BILESIM_mi_KONTROL_mu"] = {
            "aciklama": "A (kontrollu, WRN yok) ile B_ana_cift (gozlemsel, WRN yok) "
                        "AYNI havuz bilesimine sahiptir; aralarindaki fark KONTROLDEN "
                        "gelir. Ham B ile fark ise bilesimi de icerir.",
            "A_egim": ua["dort_protokol"]["egim"],
            "B_ana_cift_egim": ba["dort_protokol"]["egim"],
            "B_tum_egim": ub["dort_protokol"]["egim"],
            "isaret_A_ile_B_ana_cift_ayni_mi":
                bool(_np.sign(ua["dort_protokol"]["egim"]) == _np.sign(ba["dort_protokol"]["egim"])),
            "isaret_A_ile_B_tum_ayni_mi":
                bool(_np.sign(ua["dort_protokol"]["egim"]) == _np.sign(ub["dort_protokol"]["egim"])),
        }
    sonuc["EGIM_UYUSMASI"]["yorum"] = (
        "Iki kolun egimleri her iki nicelikte de ortusuyor: kontrollu ve gozlemsel "
        "kanit ayni yonu veriyor."
        if hepsi else
        "Kollar ORTUSMUYOR. Bu, gozlemsel koldaki karistiricilarin etkisine isarettir "
        "ve RAPORLANMALIDIR (K8); havuzlama yine YAPILMAZ.")
else:
    sonuc["EGIM_UYUSMASI"] = {"DURUM": f"iki kol da uydurulamadi (uygun: {uygun})"}

out = ROOT / "results/q1/e3_iki_kol_fit.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

for kol, v in sonuc["kollar"].items():
    if "dort_protokol" not in v:
        print(f"kol {kol}: {v['DURUM']} (n={v['n_nokta']})")
        continue
    print(f"kol {kol}: n={v['n_nokta']} nokta / {v['n_kume']} kume  "
          f"x araligi {v['x_araligi'][0]:.2f}-{v['x_araligi'][1]:.2f}")
    for ad in ("dort_protokol", "uc_protokol_bas_kaynak_haric"):
        w = v[ad]
        print(f"   {ad:32s} egim {w['egim']:+.4f}  r {w['pearson_r']:+.3f}  "
              f"GA [{w['egim_GA95'][0]:+.3f}, {w['egim_GA95'][1]:+.3f}]")
print()
print("EGIM UYUSMASI:", json.dumps(sonuc["EGIM_UYUSMASI"], ensure_ascii=False)[:400])
print(f"-> {out}")
