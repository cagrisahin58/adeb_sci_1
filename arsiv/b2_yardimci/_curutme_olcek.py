# -*- coding: utf-8 -*-
"""Curutme: yonlu terimin olcege duyarliligi. f_k(x) = log x - k log(1 - x) ailesi (k = 0 log, k = 1 logit)
ve h = -log(1 - x) olcegi (Onerme 2'nin protokol-degismez olcegi). K-b (CIFAR-10 ve CIFAR-100), K-a, H1-H3."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _curutme_ortak as O  # noqa: E402

K = O.K


def coz(M, t, P, b4_var):
    g = K.Alici(M)
    ciftler = [tuple(c) for c in t["b2_tohum_ciftleri"]]
    V = O.hucre(t, M, "V-scr")
    hucreler = {h: O.hucre(t, M, h) for h in K.HUC4} if b4_var else None
    satirlar = []
    kappalar = [round(x, 3) for x in np.arange(-1.0, 2.0001, 0.05)]
    for kap in kappalar:
        f = O.f_kappa(kap)
        a = O.kb_ka(g, f, ciftler, V, P)
        s = {"kappa": kap, "q_ort": a["q_ort"], "rho_V": a["K-b"]["ort"], "rho_V_ci90": a["K-b"].get("ci90"),
             "rho_V_tost_p": a["K-b"].get("tost_p"),
             "rho_V_ci90_band_icinde": bool(K.icinde(a["K-b"].get("ci90")))}
        if b4_var:
            h, _, _ = O.b4(g, f, hucreler, P)
            s.update({"H1": h["H1"]["kestirim"], "H2": h["H2"]["kestirim"], "H3": h["H3"]["kestirim"],
                      "H3_ci90": h["H3"]["ci90"], "H3_tost_p": h["H3"].get("tost_p"),
                      "H3_ci90_band_icinde": bool(K.icinde(h["H3"]["ci90"]))})
        satirlar.append(s)
    # h olcegi
    a = O.kb_ka(g, O.f_h, ciftler, V, P)
    hsat = {"q_ort": a["q_ort"], "q": a["q"], "K-b": a["K-b"]}
    if b4_var:
        hb, _, _ = O.b4(g, O.f_h, hucreler, P)
        hsat["B4"] = hb
    # sifir gecisi ve bant araligi
    k = np.array([s["kappa"] for s in satirlar])
    r = np.array([s["rho_V"] for s in satirlar])
    sifir = None
    for i in range(len(k) - 1):
        if r[i] == 0 or r[i] * r[i + 1] < 0:
            sifir = float(k[i] - r[i] * (k[i + 1] - k[i]) / (r[i + 1] - r[i]))
            break
    band = [s["kappa"] for s in satirlar if s["rho_V_ci90_band_icinde"]]
    out = {"satirlar": satirlar, "h_olcegi": hsat, "rho_V_sifir_gecisi_kappa": sifir,
           "rho_V_ci90_band_icinde_kappa_min": min(band) if band else None,
           "rho_V_ci90_band_icinde_kappa_max": max(band) if band else None}
    if b4_var:
        b3 = [s["kappa"] for s in satirlar if s["H3_ci90_band_icinde"]]
        out["H3_ci90_band_icinde_kappa_min"] = min(b3) if b3 else None
        out["H3_ci90_band_icinde_kappa_max"] = max(b3) if b3 else None
    return out


def main():
    M, t, P, _ = O.yukle(*O.C10)
    c10 = coz(M, t, P, True)
    M2, t2, P2, _ = O.yukle(*O.C100)
    c100 = coz(M2, t2, P2, False)
    O.yaz("olcek", {"tanim": "f_k(x) = log x - k log(1-x), x = T/100; k=0 log (birincil), k=1 logit; h = -log(1-x). "
                    "Bolunmus yari, yedi uyeli birincil panel; K-b TOST +-0,10, ham p (Holm'suz).",
                    "cifar10": c10, "cifar100": c100}, __file__)


if __name__ == "__main__":
    main()
