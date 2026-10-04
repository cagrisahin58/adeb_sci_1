#!/usr/bin/env python3
"""Gorev 1.4(a): SVHN-dahil B kolu uzerinde UC protokol (raw, tc, bc; successful_source HARIC)
asimetri yayiliminin temiz hata farkina egimi ve kume bootstrap GA'si.

Girdi : results/q1/e3_asimetri_fit_svhnli.json  ('ciftler', 20 yon cifti, 8 kume)
        results/q1/e3_iki_kol_fit.json          (SVHN-haric B kolu uc protokol egimi: gerileme kontrolu)
Cikti : results/q1/e3_uc_protokol_svhnli_fit.json

Kume bootstrap, scripts/q1_e3_asimetri.py'deki kume_bootstrap ile AYNI yordamdir
(np.random.default_rng(42), kume duzeyinde yerine koymali cekim, B = 10.000, x'te tek deger
kalan cekim atlanir, %2.5 / %97.5 yuzdelikleri).

Calistirma (depo kokunden):
  docker exec -w /workspace adeb_eval python experiments/q1_e3_uc_protokol_svhnli_fit.py
"""
import datetime
import hashlib
import io
import json
import os
import sys

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
os.chdir(ROOT)
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

GIRDI = "results/q1/e3_asimetri_fit_svhnli.json"
IKI_KOL = "results/q1/e3_iki_kol_fit.json"
OUT = "results/q1/e3_uc_protokol_svhnli_fit.json"
UC = ["raw", "target_correct", "both_correct"]
DORT = UC + ["successful_source"]
KAYNAK = {}


def sha256(yol):
    h = hashlib.sha256()
    with open(yol, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def oku_json(yol):
    KAYNAK[yol] = sha256(yol)
    with io.open(yol, encoding="utf-8") as fh:
        return json.load(fh)


def kume_bootstrap(y, x, kume, uniq, B=10000, seed=42):
    rng = np.random.default_rng(seed)
    egimler = []
    atlanan = 0
    for _ in range(B):
        take = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([np.flatnonzero(kume == t) for t in take])
        if len(set(x[idx])) < 2:
            atlanan += 1
            continue
        b1, _ = np.polyfit(x[idx], y[idx], 1)
        egimler.append(b1)
    return np.percentile(egimler, [2.5, 97.5]).tolist(), atlanan


def uydur(satirlar, y_f):
    x = np.array([s["x_temiz_hata_farki"] for s in satirlar], dtype=float)
    y = np.array([y_f(s) for s in satirlar], dtype=float)
    kume = np.array([s["kume"] for s in satirlar])
    uniq = sorted(set(kume))
    b1, b0 = np.polyfit(x, y, 1)
    ga, atl = kume_bootstrap(y, x, kume, uniq)
    return {"egim": float(b1), "kesisim": float(b0), "pearson_r": float(np.corrcoef(x, y)[0, 1]),
            "egim_GA95_kume_bootstrap": ga, "GA_sifiri_iceriyor_mu": bool(ga[0] <= 0 <= ga[1]),
            "atlanan_bootstrap": atl, "n_nokta": int(len(y)), "n_kume": len(uniq),
            "y_araligi": [float(y.min()), float(y.max())]}


def main():
    d = oku_json(GIRDI)
    ik = oku_json(IKI_KOL)
    C = d["ciftler"]

    def y3(s):
        v = [s["asimetri"][p] for p in UC]
        return max(v) - min(v)

    def y4(s):
        v = [s["asimetri"][p] for p in DORT]
        return max(v) - min(v)

    def ozdes(s):
        return abs(s["ozdeslik_ongorusu_ham_eksi_tc"])

    svhn_haric = [s for s in C if s["dataset"] != "svhn"]
    sonuc = {
        "uc_protokol_svhn_dahil": uydur(C, y3),
        "dort_protokol_svhn_dahil": uydur(C, y4),
        "uc_protokol_svhn_haric_gerileme_kontrolu": uydur(svhn_haric, y3),
        "ozdeslik_terimi_abs_ham_eksi_tc_ongoru_svhn_dahil": uydur(C, ozdes),
    }
    # gerileme kontrolleri: mevcut artefaktlarla
    sonuc["kontrol_dort_protokol_vs_e3_asimetri_fit_svhnli"] = {
        "saklanan_egim": d["uydurma"]["egim"],
        "saklanan_GA": d["uydurma"]["egim_GA95_kume_bootstrap"],
        "yeniden_egim": sonuc["dort_protokol_svhn_dahil"]["egim"],
        "yeniden_GA": sonuc["dort_protokol_svhn_dahil"]["egim_GA95_kume_bootstrap"],
        "egim_farki": sonuc["dort_protokol_svhn_dahil"]["egim"] - d["uydurma"]["egim"],
    }
    bk = ik["kollar"]["B"]["uc_protokol_bas_kaynak_haric"]
    sonuc["kontrol_uc_protokol_svhn_haric_vs_e3_iki_kol_fit_B"] = {
        "saklanan_egim": bk["egim"], "saklanan_GA": bk["egim_GA95"],
        "yeniden_egim": sonuc["uc_protokol_svhn_haric_gerileme_kontrolu"]["egim"],
        "yeniden_GA": sonuc["uc_protokol_svhn_haric_gerileme_kontrolu"]["egim_GA95_kume_bootstrap"],
        "egim_farki": sonuc["uc_protokol_svhn_haric_gerileme_kontrolu"]["egim"] - bk["egim"],
    }
    # uc protokol yayilimi ozdeslik teriminin kendisi mi?
    esit = []
    for s in C:
        a = s["asimetri"]
        ht = abs(a["raw"] - a["target_correct"])
        esit.append({
            "kume": s["kume"], "yon_ileri": s["yon_ileri"], "x": s["x_temiz_hata_farki"],
            "yayilim_uc": y3(s), "abs_ham_eksi_tc": ht,
            "yayilim_uc_esittir_abs_ham_eksi_tc": bool(abs(y3(s) - ht) < 1e-9),
            "abs_ozdeslik_ongorusu": ozdes(s),
            "abs_ham_eksi_tc_eksi_ongoru": ht - ozdes(s),
            "aradaki_protokol": ("both_correct tc ile raw arasinda" if min(a["raw"], a["target_correct"]) <= a["both_correct"] <= max(a["raw"], a["target_correct"])
                                 else "both_correct disarida"),
        })
    n_es = sum(e["yayilim_uc_esittir_abs_ham_eksi_tc"] for e in esit)
    sonuc["totoloji_kontrolu"] = {
        "yayilim_uc_esit_abs_ham_eksi_tc_sayisi": n_es,
        "toplam": len(esit),
        "max_abs_ham_eksi_tc_eksi_ozdeslik_ongorusu": max(abs(e["abs_ham_eksi_tc_eksi_ongoru"]) for e in esit),
        "esitlik_bozulan_ciftler": [e for e in esit if not e["yayilim_uc_esittir_abs_ham_eksi_tc"]],
        "cift_tablosu": esit,
    }
    out = {
        "uretildi_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kaynaklar": dict(KAYNAK),
        "yontem": ("x = x_temiz_hata_farki (puan), y = asimetrinin raw/tc/bc uzerinden max-min yayilimi "
                   "(successful_source haric); EKK egimi; GA kume bootstrap (8 kume, B=10.000, tohum 42, "
                   "q1_e3_asimetri.py ile ayni yordam). Dort protokol ve SVHN-haric uydurmalar saklanan "
                   "artefaktlara karsi gerileme kontroludur."),
        "makaledeki_ifade_kaynagi": "makale +0.470 [+0.361, +0.665] diyor; bu dosya o sayinin yeniden uretilip uretilmedigini gosterir",
        "sonuc": sonuc,
    }
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("yazildi:", OUT)
    for k, v in sonuc.items():
        if isinstance(v, dict) and "egim" in v:
            print(f"{k:55s} egim {v['egim']:+.4f} GA [{v['egim_GA95_kume_bootstrap'][0]:+.4f}, {v['egim_GA95_kume_bootstrap'][1]:+.4f}] r {v['pearson_r']:+.3f} n {v['n_nokta']}/{v['n_kume']} atl {v['atlanan_bootstrap']}")
    print(json.dumps(sonuc["kontrol_dort_protokol_vs_e3_asimetri_fit_svhnli"]))
    print(json.dumps(sonuc["kontrol_uc_protokol_svhn_haric_vs_e3_iki_kol_fit_B"]))
    t = sonuc["totoloji_kontrolu"]
    print("totoloji:", t["yayilim_uc_esit_abs_ham_eksi_tc_sayisi"], "/", t["toplam"], "max |ht - ongoru|", t["max_abs_ham_eksi_tc_eksi_ozdeslik_ongorusu"])
    for e in t["esitlik_bozulan_ciftler"]:
        print("  bozulan:", e["kume"], e["yon_ileri"], round(e["yayilim_uc"], 3), round(e["abs_ham_eksi_tc"], 3), e["aradaki_protokol"])


if __name__ == "__main__":
    main()
