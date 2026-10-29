# -*- coding: utf-8 -*-
"""Konsey P3 masa testi 2 (29.10.2026): A kolu yorunge kayitlarinda asimetri
ile iki modelin beyaz kutu gurbuzluk farki arasindaki iliski.

Yeni olcum YOK. Girdiler:
  results/q1/e3_akolu_v2/A_*.json        (epok kontrol noktasi ile es model arasi dort protokol)
  results/q1/e2/testcurve_*.npz          (CIFAR-10 E2 yorungeleri, epok basina 10k test temiz ve PGD-10)
  results/q1/cifar100/testcurve/*.npz    (CIFAR-100 E1 yorungeleri)
  results/c1_seeds/c1_seed_summary.json  (CIFAR-10 es modeller, C1 best.pth)
  results/q1/e1_cifar100_summary.json    (CIFAR-100 es modeller)
Konvansiyon: A = CNN->ViT eksi ViT->CNN (makale). ResNet yorungelerinde kayittaki
'asimetri' (ViT->ResNet@ep eksi ResNet@ep->ViT) isaret degistirir.
w = beyaz kutu kosullu yaniltma = 100 (1 - PGD dogrulugu / temiz dogruluk).
Delta_w = w_ViT - w_CNN (pozitif: CNN daha gurbuz).
Cikti: raporlar/konsey_2026-10-29/_p3_yorunge_gurbuzluk_masa.json
"""
import glob
import io
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CIKTI = os.path.join(KOK, "raporlar", "konsey_2026-10-29", "_p3_yorunge_gurbuzluk_masa.json")


def oku(yol):
    return json.load(io.open(os.path.join(KOK, yol), encoding="utf-8"))


def es_modeller():
    es = {}
    c1 = oku("results/c1_seeds/c1_seed_summary.json")
    for p in c1["pairs"]:
        k = f"c10_pair{p['pair']}"
        es[k] = {"resnet18": (p["resnet"]["clean"], p["resnet"]["pgd"]),
                 "vit_tiny": (p["vit"]["clean"], p["vit"]["pgd"])}
    c100 = oku("results/q1/e1_cifar100_summary.json")["mimariler"]
    rs = ["1001", "1002", "1003"]
    vs = ["2001", "2002", "2003"]
    for i in range(3):
        k = f"c100_pair{i + 1}"
        r = c100["resnet18"]["tohumlar"][rs[i]]
        v = c100["vit_tiny"]["tohumlar"][vs[i]]
        es[k] = {"resnet18": (r["test_clean"], r["test_pgd10"]),
                 "vit_tiny": (v["test_clean"], v["test_pgd10"])}
    return es


def egri(ds, arch, tohum):
    if ds == "cifar10":
        yol = os.path.join(KOK, "results", "q1", "e2", f"testcurve_{arch}_s{tohum}.npz")
    else:
        yol = os.path.join(KOK, "results", "q1", "cifar100", "testcurve", f"testcurve_{arch}_s{tohum}.npz")
    z = np.load(yol)
    return {int(e): (float(c), float(a)) for e, c, a in zip(z["epochs"], z["clean_acc"], z["adv_acc"])}


def w(temiz, pgd):
    return 100.0 * (1.0 - pgd / temiz)


def main():
    es = es_modeller()
    kayit = []
    for f in sorted(glob.glob(os.path.join(KOK, "results", "q1", "e3_akolu_v2", "A_*.json"))):
        d = json.load(io.open(f, encoding="utf-8"))
        ds = d["dataset"]
        tid = d["trajectory_id"]
        if ds not in ("cifar10", "cifar100"):
            continue  # SVHN icin epok egrisi dosyasi yok; hareketli modelin w'si bilinmiyor
        arch = "resnet18" if "_rn18_" in tid else "vit_tiny"
        tohum = tid.split("_s")[-1]
        ep = int(d["epoch"])
        cr = egri(ds, arch, tohum)
        if ep not in cr:
            continue
        hareketli = cr[ep]
        es_arch = "vit_tiny" if arch == "resnet18" else "resnet18"
        es_m = es[d["kume"]][es_arch]
        if arch == "resnet18":
            cnn, vit = hareketli, es_m
            isaret = -1.0
        else:
            cnn, vit = es_m, hareketli
            isaret = 1.0
        A = {k: isaret * float(v) for k, v in d["asimetri"].items()}
        kayit.append({
            "dosya": os.path.relpath(f, KOK).replace("\\", "/"), "veri": ds, "yorunge": tid,
            "hareketli": arch, "epok": ep,
            "cnn_temiz": cnn[0], "cnn_pgd": cnn[1], "vit_temiz": vit[0], "vit_pgd": vit[1],
            "w_cnn": w(*cnn), "w_vit": w(*vit), "delta_w": w(*vit) - w(*cnn),
            "delta_pgd_dogruluk": cnn[1] - vit[1], "delta_temiz": cnn[0] - vit[0],
            "A": A,
        })

    def ozet(alt, ad):
        out = {"n": len(alt)}
        if not alt:
            return out
        x = np.array([k["delta_w"] for k in alt])
        xp = np.array([k["delta_pgd_dogruluk"] for k in alt])
        xc = np.array([k["delta_temiz"] for k in alt])
        for p in ("raw", "target_correct", "both_correct", "successful_source"):
            y = np.array([k["A"][p] for k in alt])
            b1, b0 = np.polyfit(x, y, 1)
            r = float(np.corrcoef(x, y)[0, 1])
            rc = float(np.corrcoef(xc, y)[0, 1])
            isaret = int(np.sum(np.sign(y) == np.sign(x)))
            # iki degiskenli: delta_w ve temiz fark birlikte
            X = np.column_stack([np.ones_like(x), x, xc])
            coef, *_ = np.linalg.lstsq(X, y, rcond=None)
            out[p] = {"egim_delta_w": float(b1), "kesisim": float(b0),
                      "sifir_gecis_delta_w": float(-b0 / b1) if b1 != 0 else None,
                      "pearson_r_delta_w": r, "pearson_r_temiz_fark": rc,
                      "isaret_uyumu_delta_w": f"{isaret}/{len(y)}",
                      "iki_degiskenli_katsayilar_[sabit,delta_w,temiz_fark]": [float(c) for c in coef],
                      "pearson_r_delta_pgd_dogruluk": float(np.corrcoef(xp, y)[0, 1]),
                      "egim_delta_pgd": float(np.polyfit(xp, y, 1)[0]),
                      "kesisim_delta_pgd": float(np.polyfit(xp, y, 1)[1]),
                      "isaret_uyumu_delta_pgd": f"{int(np.sum(np.sign(y) == np.sign(xp)))}/{len(y)}"}
        return out

    sonuc = {"uretildi_utc": datetime.now(timezone.utc).isoformat(),
             "betik": "raporlar/konsey_2026-10-29/_p3_yorunge_gurbuzluk_masa.py",
             "not": ("Kayit ve egri farkli PGD tohumlariyla olculmus olabilir; w hareketli kontrol noktasi icin "
                     "egri dosyasindan, es model icin ozet dosyalarindan. Noktalar bagimsiz degildir "
                     "(ayni yorunge ve ayni es model); egimler betimseldir."),
             "kayitlar": kayit,
             "ozet": {
                 "tum": ozet(kayit, "tum"),
                 "cifar10": ozet([k for k in kayit if k["veri"] == "cifar10"], "c10"),
                 "cifar100": ozet([k for k in kayit if k["veri"] == "cifar100"], "c100"),
                 "cifar10_resnet_hareketli": ozet([k for k in kayit if k["veri"] == "cifar10" and k["hareketli"] == "resnet18"], ""),
                 "cifar10_vit_hareketli": ozet([k for k in kayit if k["veri"] == "cifar10" and k["hareketli"] == "vit_tiny"], ""),
                 "cifar100_resnet_hareketli": ozet([k for k in kayit if k["veri"] == "cifar100" and k["hareketli"] == "resnet18"], ""),
                 "cifar100_vit_hareketli": ozet([k for k in kayit if k["veri"] == "cifar100" and k["hareketli"] == "vit_tiny"], ""),
             }}
    with io.open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    for k in kayit:
        if k["epok"] <= 11 or k["delta_w"] < 0:
            print(f"{k['yorunge']:18s} ep{k['epok']:3d} cnn {k['cnn_temiz']:.2f}/{k['cnn_pgd']:.2f} vit {k['vit_temiz']:.2f}/{k['vit_pgd']:.2f} "
                  f"dw={k['delta_w']:+.2f} A_tc={k['A']['target_correct']:+.2f} A_bc={k['A']['both_correct']:+.2f} A_raw={k['A']['raw']:+.2f}")
    for ad, o in sonuc["ozet"].items():
        if o["n"] == 0:
            continue
        print(ad, o["n"], {p: (round(o[p]["egim_delta_w"], 3), round(o[p]["kesisim"], 2), o[p]["isaret_uyumu_delta_w"],
                               round(o[p]["pearson_r_delta_w"], 3), round(o[p]["pearson_r_temiz_fark"], 3))
                           for p in ("target_correct", "both_correct")})


if __name__ == "__main__":
    main()
