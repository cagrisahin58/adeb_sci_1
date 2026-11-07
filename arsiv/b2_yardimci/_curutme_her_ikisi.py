# -*- coding: utf-8 -*-
"""Curutme: tutarli her-ikisi-dogru ayrisimi. Her (i, j) cifti icin maske = i ve j temiz ornegi dogru siniflar;
T_ij, T_ji, w_i ve w_j AYNI maskede (bolunmus yari: w cift, T tek indeksli ve tersi). Boylece _curutme_ayrisim.py
(e) satirindaki kosegen/kosegen-disi maske uyusmazligi ortadan kalkar. K-a, K-b, H1-H3 (CIFAR-10), K-a, K-b
(CIFAR-100). Ayrica hedef-dogru protokolde w'nin cift maskesinde hesaplanmasinin tek basina etkisi."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _curutme_ortak as O  # noqa: E402

K = O.K


class Cift:
    def __init__(self, M):
        self.M = M
        idx = np.arange(M.n)
        self.alt = {"cift": idx % 2 == 0, "tek": idx % 2 == 1}
        self.tc = {m: M.h[(m, m)]["tc"] for m in M.modeller()}
        self.aw = {m: M.h[(m, m)]["aw"] for m in M.modeller()}

    def oran(self, s, t, maske):
        d = self.M.h[(s, t)]
        return 100.0 * d["aw"][maske].mean()

    def nicelik(self, i, j):
        """(log tau_ij, r_ij) bolunmus yari, ortak maske."""
        ortak = self.tc[i] & self.tc[j]
        lt, rr = [], []
        for wa, Ta in (("cift", "tek"), ("tek", "cift")):
            mw, mT = ortak & self.alt[wa], ortak & self.alt[Ta]
            Tij, Tji = self.oran(i, j, mT), self.oran(j, i, mT)
            wi, wj = 100 * self.aw[i][mw].mean(), 100 * self.aw[j][mw].mean()
            lt.append(0.5 * (np.log(Tij) + np.log(Tji) - np.log(wi) - np.log(wj)))
            rr.append(np.log(Tij / Tji) - np.log(wj / wi))
            # S icin kaynak i'nin log T'si
        return float(np.mean(lt)), float(np.mean(rr))

    def logT(self, i, j):
        ortak = self.tc[i] & self.tc[j]
        return float(np.mean([np.log(self.oran(i, j, ortak & self.alt[a])) for a in ("tek", "cift")]))


def md(C, m, P):
    Pm = [c for c in P if c != m]
    lt = [C.nicelik(m, c) for c in Pm]
    sig = float(np.mean([x[0] for x in lt]))
    rho = float(np.mean([-x[1] for x in lt]))  # rho_m = ort r_cm = -ort r_mc
    S = float(np.mean([C.logT(m, c) for c in Pm]))
    return {"sigma": sig, "rho": rho, "S": S}


def coz(M, t, P, b4_var):
    C = Cift(M)
    ciftler = [tuple(c) for c in t["b2_tohum_ciftleri"]]
    V = O.hucre(t, M, "V-scr")
    q, G = [], []
    for R, Vv in ciftler:
        a, b = md(C, R, P), md(C, Vv, P)
        D = a["S"] - b["S"]
        G.append(D)
        q.append((a["sigma"] - b["sigma"]) / D)
    rho = [md(C, v, P)["rho"] for v in V]
    kb = K.tek_orneklem(rho)
    kb["tost_p"] = K.tost_p(kb["ort"], kb["se"], kb["df"])[0]
    out = {"q": q, "q_ort": float(np.mean(q)), "G": G, "K-b": kb}
    if b4_var:
        sig, rh = {}, {}
        for h in K.HUC4:
            d = [md(C, m, P) for m in O.hucre(t, M, h)]
            sig[h] = [x["sigma"] for x in d]
            rh[h] = [x["rho"] for x in d]
        k = K.b4_karsitliklar(sig, rh)
        out["B4"] = {a: {"kestirim": k[a]["kestirim"], "ci90": k[a]["ci90"], "ci95": k[a]["ci95"]} for a in k}
        out["B4"]["H3"]["tost_p"] = K.tost_p(k["H3"]["kestirim"], k["H3"]["se"], k["H3"]["df"])[0]
        out["hucre_sigma"], out["hucre_rho"] = sig, rh
    return out


def main():
    M, t, P, _ = O.yukle(*O.C10)
    M2, t2, P2, _ = O.yukle(*O.C100)
    O.yaz("her_ikisi_tutarli", {"tanim": "Cift basina ortak maske (iki model de temiz dogru); T ve w ayni maskede, "
                                        "bolunmus yari. Kesifsel, on kayit disi (B9 icin on kayitli ama uretilmemis "
                                        "her-ikisi-dogru duyarliliginin bir yorumu).",
                                "cifar10": coz(M, t, P, True), "cifar100": coz(M2, t2, P2, False)}, __file__)


if __name__ == "__main__":
    main()
