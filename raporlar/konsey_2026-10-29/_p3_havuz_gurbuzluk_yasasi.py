# -*- coding: utf-8 -*-
"""Konsey P3 masa testi 3 (29.10.2026): havuzda tek parametreli gurbuzluk yasasi.
A_ij (i->j eksi j->i) ~ kappa (rho_i - rho_j); rho = beyaz kutu PGD-10 dogrulugu
(kosegen hucrenin ham oranindan: rho_i = 100 - raw_ii). Yeni olcum yok.
Girdi: results/q1/havuz_cifar10/havuz_protokoller.json (yonlu oranlar).
Cikti: raporlar/konsey_2026-10-29/_p3_havuz_gurbuzluk_yasasi.json
"""
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
H = json.load(io.open(os.path.join(KOK, "results", "q1", "havuz_cifar10", "havuz_protokoller.json"), encoding="utf-8"))
mods = H["modeller"]
Y = H["yonlu"]


def rho(m):
    return 100.0 - Y[f"{m}->{m}"]["oranlar"]["raw"]


def analiz(alt, protokol):
    K = len(alt)
    r = np.array([rho(m) for m in alt])
    rows = []
    for a in range(K):
        for b in range(a + 1, K):
            i, j = alt[a], alt[b]
            Aij = Y[f"{i}->{j}"]["oranlar"][protokol] - Y[f"{j}->{i}"]["oranlar"][protokol]
            rows.append((i, j, Aij, r[a] - r[b]))
    A = np.array([x[2] for x in rows])
    d = np.array([x[3] for x in rows])
    kappa = float((A @ d) / (d @ d))  # kesisimsiz (ters-simetrik) tek parametre
    pred = kappa * d
    R2 = 1 - ((A - pred) ** 2).sum() / (A ** 2).sum()
    isaret = int(np.sum(np.sign(A) == np.sign(d)))
    # model basina ortalama artik (potansiyel artigi): e_i = (1/K) sum_j (A_ij - kappa d_ij)
    E = np.zeros((K, K))
    for (i, j, a_, d_) in rows:
        ii, jj = alt.index(i), alt.index(j)
        E[ii, jj] = a_ - kappa * d_
        E[jj, ii] = -(a_ - kappa * d_)
    pot_artik = {m: float(E[k].sum() / K) for k, m in enumerate(alt)}
    # birini-birak: ViT_Tiny_AT'yi disarida birakarak kappa, sonra onun ciftlerini ongor
    out = {"modeller": alt, "rho_pgd10_dogruluk": {m: float(x) for m, x in zip(alt, r)},
           "kappa": kappa, "R2_kesisimsiz": float(R2), "isaret_uyumu": f"{isaret}/{len(A)}",
           "model_potansiyel_artigi": pot_artik,
           "ciftler": [{"i": i, "j": j, "A": float(a_), "rho_farki": float(d_), "ongoru": float(kappa * d_)} for (i, j, a_, d_) in rows]}
    if "ViT_Tiny_AT" in alt:
        tut = [x for x in rows if "ViT_Tiny_AT" not in (x[0], x[1])]
        At = np.array([x[2] for x in tut])
        dt = np.array([x[3] for x in tut])
        k2 = float((At @ dt) / (dt @ dt))
        vit = [x for x in rows if "ViT_Tiny_AT" in (x[0], x[1])]
        hata = []
        for (i, j, a_, d_) in vit:
            s = 1.0 if i == "ViT_Tiny_AT" else -1.0  # ViT perspektifi: ViT->X eksi X->ViT
            hata.append({"es": j if i == "ViT_Tiny_AT" else i, "gozlenen_ViT_eksi_es": s * a_,
                         "ongorulen_ViTsiz_kappa": s * k2 * d_, "artik": s * (a_ - k2 * d_)})
        out["ViT_disarida_kappa"] = k2
        out["ViT_ciftleri_dis_ornek_ongoru"] = hata
        out["ViT_ciftleri_artik_ortalama"] = float(np.mean([h["artik"] for h in hata]))
        out["ViT_ciftleri_artik_mutlak_en_buyuk"] = float(np.max([abs(h["artik"]) for h in hata]))
    return out


sonuc = {"uretildi_utc": datetime.now(timezone.utc).isoformat(),
         "betik": "raporlar/konsey_2026-10-29/_p3_havuz_gurbuzluk_yasasi.py",
         "tanim": "A_ij = (i->j) - (j->i) oran (puan); rho = 100 - kosegen ham oran (beyaz kutu PGD-10 dogrulugu, havuz kosusu).",
         "sonuc": {}}
at7 = [m for m in mods if m != "Standard_WRN28_10"]
for p in ("target_correct", "both_correct", "raw"):
    sonuc["sonuc"][p] = {"AT7": analiz(at7, p), "hepsi8": analiz(mods, p)}
with io.open(os.path.join(KOK, "raporlar", "konsey_2026-10-29", "_p3_havuz_gurbuzluk_yasasi.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(sonuc, f, ensure_ascii=False, indent=1)
for p, v in sonuc["sonuc"].items():
    for k, o in v.items():
        print(p, k, "kappa=%.3f R2=%.3f isaret=%s" % (o["kappa"], o["R2_kesisimsiz"], o["isaret_uyumu"]),
              "potansiyel artigi:", {m[:10]: round(x, 2) for m, x in o["model_potansiyel_artigi"].items()})
        if "ViT_disarida_kappa" in o:
            print("   ViT disarida kappa=%.3f, ViT ciftleri artik ort=%.2f, en buyuk |artik|=%.2f" % (
                o["ViT_disarida_kappa"], o["ViT_ciftleri_artik_ortalama"], o["ViT_ciftleri_artik_mutlak_en_buyuk"]))
            for h in o["ViT_ciftleri_dis_ornek_ongoru"]:
                print("     ", h["es"][:18], "gozlenen %.2f ongoru %.2f" % (h["gozlenen_ViT_eksi_es"], h["ongorulen_ViTsiz_kappa"]))
print({m: round(rho(m), 2) for m in mods})
