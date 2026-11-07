# -*- coding: utf-8 -*-
"""Curutme: cikarim yapisi. (1) Holm ailesi yeniden tanimlaninca (bütün dogrulayici sinamalar tek aile)
duzeltilmis p'ler; (2) Welch aralik ve serbestlik dereceleriyle F_B4 kararlari; (3) TOST delta taramasi ve
destegi veren en kucuk delta (t ve hiyerarsik bootstrap); (4) birlesik SD'den MDE ve guc (n = 2 ve n = 5);
(5) hucre varyanslari heterojenligi. Yalniz mevcut JSON ciktilarini okur."""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _curutme_ortak as O  # noqa: E402

K = O.K
Q = O.KOK / "results/q1"


def oku(p):
    return json.loads((Q / p).read_text(encoding="utf-8"))


def main():
    b2 = oku("konsey_ayrisim_b2.json")["b2"]["F_B2"]
    b4j = oku("konsey_ayrisim_b4.json")["b4"]
    b4 = b4j["F_B4"]
    b9 = oku("konsey_b9_c100/b9_dondurulmus_b2.json")["b2"]["F_B2"]
    b10 = oku("konsey_b10_gradyan/b10_aile.json")["F_B10"]["sinamalar"]
    adlar = ["K-a(C10)", "K-b(C10)", "K-c(C10)", "H1", "H2", "H3", "K-a(C100)", "K-b(C100)", "K-c(C100)"] + \
        [s["sinama"] for s in b10]
    pler = list(b2["p_ham"]) + list(b4["p_ham"]) + list(b9["p_ham"]) + [s["p_tek_ham"] for s in b10]
    aile_holm = list(b2["p_holm"]) + list(b4["p_holm"]) + list(b9["p_holm"]) + [s["p_holm"] for s in b10]
    tek = K.holm(pler)
    c10 = K.holm(pler[:6])
    bonf = [min(1.0, p * len(pler)) for p in pler]
    holm_tablo = [{"sinama": a, "p_ham": p, "p_holm_kayitli_aile": h, "p_holm_tek_aile_15": t15,
                   "p_bonferroni_15": b, "p_holm_C10_6": (c10[i] if i < 6 else None),
                   "kayitli_destek": h < 0.05, "tek_aile_destek": t15 < 0.05}
                  for i, (a, p, h, t15, b) in enumerate(zip(adlar, pler, aile_holm, tek, bonf))]
    degisen = [r["sinama"] for r in holm_tablo if r["kayitli_destek"] != r["tek_aile_destek"]]

    # (2) Welch ile F_B4
    k = b4["karsitliklar"]
    w = b4j["duyarlilik"]["welch"]
    pw = []
    welch = {}
    for ad in ("H1", "H2", "H3"):
        est, se, df = k[ad]["kestirim"], w[ad]["se"], w[ad]["df"]
        tt = est / se
        if ad == "H1":
            p = float(stats.t.cdf(tt, df))
        elif ad == "H2":
            p = float(2 * min(stats.t.cdf(tt, df), 1 - stats.t.cdf(tt, df)))
        else:
            p = K.tost_p(est, se, df)[0]
        pw.append(p)
        welch[ad] = {"kestirim": est, "se_welch": se, "df_welch": df, "p_ham_welch": p}
    adjw = K.holm(pw)
    for i, ad in enumerate(("H1", "H2", "H3")):
        welch[ad]["p_holm_welch"] = adjw[i]
        welch[ad]["destek_welch_holm"] = adjw[i] < 0.05
        # Holm duzeltmesine denk aralik: ilgili sira icin alfa/(m-k)
    welch["not"] = "Welch se ve df dondurulmus ciktinin duyarlilik.welch alanindan; H1 tek yonlu, H2 iki yonlu, H3 TOST +-0,10."

    # (3) delta taramasi
    deltalar = [round(x, 3) for x in np.arange(0.01, 0.2001, 0.005)]
    kbC10 = b2["K-b"]
    kbC100 = b9["K-b"]
    h3 = k["H3"]

    def tarama(est, se, df, digerleri, sira):
        out = []
        for d in deltalar:
            p = K.tost_p(est, se, df, d)[0]
            pp = list(digerleri)
            pp.insert(sira, p)
            out.append({"delta": d, "tost_p": p, "holm_p": K.holm(pp)[sira]})
        dmin = next((r["delta"] for r in out if r["holm_p"] < 0.05), None)
        return out, dmin

    t_kb10, d_kb10 = tarama(kbC10["ort"], kbC10["se"], kbC10["df"], [b2["p_ham"][0], b2["p_ham"][2]], 1)
    t_kb100, d_kb100 = tarama(kbC100["ort"], kbC100["se"], kbC100["df"], [b9["p_ham"][0], b9["p_ham"][2]], 1)
    t_h3, d_h3 = tarama(h3["kestirim"], h3["se"], h3["df"], [b4["p_ham"][0], b4["p_ham"][1]], 2)
    t_h3w, d_h3w = tarama(h3["kestirim"], w["H3"]["se"], w["H3"]["df"], [pw[0], pw[1]], 2)
    bs10 = oku("konsey_ek_masa/bootstrap_cifar10.json")["K-b"]["bootstrap"]
    bs100 = oku("konsey_ek_masa/bootstrap_cifar100.json")["K-b"]["bootstrap"]
    hb = b4j["duyarlilik"]["hiyerarsik_bootstrap"]["H3"]
    delta_ozet = {
        "K-b(C10)_t_en_kucuk_delta_holm": d_kb10, "K-b(C100)_t_en_kucuk_delta_holm": d_kb100,
        "H3_t_en_kucuk_delta_holm": d_h3, "H3_welch_en_kucuk_delta_holm": d_h3w,
        "K-b(C10)_hiyerarsik_bootstrap_ci90_esdeger_delta": max(abs(bs10["ci90"][0]), abs(bs10["ci90"][1])),
        "K-b(C100)_hiyerarsik_bootstrap_ci90_esdeger_delta": max(abs(bs100["ci90"][0]), abs(bs100["ci90"][1])),
        "H3_hiyerarsik_bootstrap_ci90_esdeger_delta": max(abs(hb["ci90"][0]), abs(hb["ci90"][1])),
        "H3_welch_ci90_esdeger_delta": max(abs(w["H3"]["ci90"][0]), abs(w["H3"]["ci90"][1])),
        "kayitli_delta": K.DELTA, "dayanak_rms_vit_li_havuz": 0.0897, "dayanak_rms_yalniz_cnn": 0.0605,
        "dayanak_not": "0,0897 ve 0,0605 ON_KAYIT_2026-10-29.md satir 50'den (havuz_AT7 ve yalniz_cnn_10)."}

    # (4) MDE ve guc
    def mde(se, df, alfa, tek_yon, guc=0.80):
        ta = stats.t.ppf(1 - alfa, df) if tek_yon else stats.t.ppf(1 - alfa / 2, df)
        # merkezi olmayan t ile guc = guc saglayan en kucuk etki
        lo, hi = 0.0, 20 * se
        for _ in range(80):
            mid = (lo + hi) / 2
            nc = mid / se
            g = 1 - stats.nct.cdf(ta, df, nc)
            if g < guc:
                lo = mid
            else:
                hi = mid
        return hi

    sp_sig = k["H1"]["sp_birlesik"]
    sp_rho = k["H3"]["sp_birlesik"]
    guc = {}
    for n_yeni, n_vscr in ((2, 3), (5, 5)):
        n = {"V-scr": n_vscr, "V-IN": n_yeni, "R224-scr": n_yeni, "R224-IN": n_yeni}
        df = sum(v - 1 for v in n.values())
        c1 = np.sqrt(1 / n["V-scr"] + 1 / n["R224-scr"])
        c2 = np.sqrt(sum(1 / v for v in n.values()))
        c3 = 0.5 * np.sqrt(sum(1 / v for v in n.values()))
        cint_rho = np.sqrt(sum(1 / v for v in n.values()))
        g = {"df": df,
             "MDE_H1_tek_yon_alfa_0.0167": mde(sp_sig * c1, df, 0.05 / 3, True),
             "MDE_H2_iki_yon_alfa_0.0167": mde(sp_sig * c2, df, 0.05 / 3, False),
             "MDE_rho_etkilesim_iki_yon_alfa_0.05": mde(sp_rho * cint_rho, df, 0.05, False),
             "se_H3": sp_rho * c3, "se_H2": sp_sig * c2, "se_rho_etkilesim": sp_rho * cint_rho}
        # TOST gucu: gercek etki 0 iken esdegerlik ilan etme olasiligi (H3, delta 0.10 ve 0.06)
        for d in (0.10, 0.06):
            se = sp_rho * c3
            ta = stats.t.ppf(0.95, df)
            # yaklasik: P(|est| + ta*se < d) gercek 0 iken
            sinir = d - ta * se
            g[f"TOST_guc_H3_delta_{d}"] = float(max(0.0, 2 * stats.t.cdf(sinir / se, df) - 1)) if sinir > 0 else 0.0
        guc[f"n_yeni_{n_yeni}_n_vscr_{n_vscr}"] = g
    # Welch'e gore sigma karsitliklarinda tek hucre SD'si ile MDE (heterojenlik)
    deg = b4["degerler"]
    sd = {o: {h: (float(np.std(v, ddof=1)) if len(v) > 1 else None) for h, v in deg[o].items()} for o in ("sigma", "rho")}
    het = {o: {"hucre_sd": sd[o], "en_buyuk_en_kucuk_varyans_orani":
               float(max(x for x in sd[o].values()) ** 2 / min(x for x in sd[o].values()) ** 2)} for o in sd}
    # Hartley Fmax icin kritik deger yok (df 1); yalniz betimsel
    # Rho etkilesimi gozlenen (A2 foyu -0,134) ile karsilastirma icin nokta
    rho_int = (np.mean(deg["rho"]["V-IN"]) - np.mean(deg["rho"]["V-scr"])) - \
        (np.mean(deg["rho"]["R224-IN"]) - np.mean(deg["rho"]["R224-scr"]))
    O.yaz("cikarim", {"holm_aileleri": {"tablo": holm_tablo, "tek_ailede_karari_degisen": degisen,
                                         "aile_buyuklugu": len(pler)},
                       "welch_F_B4": welch, "delta_taramasi": {"ozet": delta_ozet, "K-b(C10)": t_kb10,
                                                              "K-b(C100)": t_kb100, "H3": t_h3, "H3_welch": t_h3w},
                       "guc_ve_MDE": guc, "varyans_heterojenligi": het,
                       "rho_etkilesimi_nokta": float(rho_int)}, __file__)


if __name__ == "__main__":
    main()
