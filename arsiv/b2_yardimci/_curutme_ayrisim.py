# -*- coding: utf-8 -*-
"""Curutme: ayrisimin kendisi ve nedensel kimlik. Mevcut ornek bazli kayitlardan (GPU yok):
 (a) w'nin beyaz kutu saldirisina bagliligi: PGD-10 yerine AutoAttack ile kosullu w kullanilsaydi H1-H3, q ve
     K-b ne kadar kayardi (yeni alti model ilk 1000 goruntu B6, C1 cifti tam test c1_seed_summary);
 (b) mimari ici, baslatmalar arasi benzerlik: log tau(V-scr, V-IN) ile log tau(V-scr, CNN) karsilastirmasi;
 (c) r'nin Hodge dolasim payinin bolunmus yari guvenilirligi ve serbest potansiyelin omega'ya egimi;
 (d) H1'in ham simetrik transfer ve -1/2 Delta omega bilesenlerine bolunmesi;
 (e) her-ikisi-dogru protokolunde K-a, K-b, H1-H3 (CIFAR-10) ve K-a, K-b (CIFAR-100);
 (f) sigma ~ temiz dogruluk (yalniz CNN modelleri) ve V-scr, V-IN artiklari (A3);
 (g) panel orneklemini rastgele etki sayan jackknife SE ile kosu SE'sinin birlesimi."""
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _curutme_ortak as O  # noqa: E402

K = O.K
f = O.f_log


def w_kos(M, m, n=None):
    d = M.h[(m, m)]
    tc, aw = d["tc"], d["aw"]
    if n:
        tc, aw = tc[:n], aw[:n]
    return float((aw & tc).sum() / tc.sum()), int(tc.sum())


def a_aa(M, t):
    out = {}
    aa_dir = O.KOK / "results/q1/konsey_b6_aa"
    for m in ["V_IN_s2101", "V_IN_s2102", "R224_scr_s1201", "R224_scr_s1202", "R224_IN_s1301", "R224_IN_s1302"]:
        z = np.load(aa_dir / f"per_sample_{m}.npz")
        rc = z["robust_correct"].astype(bool)[:1000]
        w_pgd, ntc = w_kos(M, m, 1000)
        tc = M.h[(m, m)]["tc"][:1000]
        w_aa = float(1 - (rc & tc).sum() / tc.sum())
        out[m] = {"w_pgd_1k": w_pgd, "w_aa_1k": w_aa, "d_omega": float(np.log(w_aa) - np.log(w_pgd)),
                  "kaynak": "konsey_b6_aa/per_sample + konsey_b4_matris kosegen, ilk 1000"}
    s = json.loads((O.KOK / "results/c1_seeds/c1_seed_summary.json").read_text(encoding="utf-8"))
    for p in s["pairs"]:
        for anah, ad in (("resnet", f"ResNet18_AT_s{p['resnet_seed']}"), ("vit", f"ViT_Tiny_AT_s{p['vit_seed']}")):
            x = p[anah]
            w_pgd = 1 - x["pgd"] / x["clean"]
            w_aa = 1 - x["aa"] / x["clean"]
            out[ad] = {"w_pgd_tam": w_pgd, "w_aa_tam": w_aa, "d_omega": float(np.log(w_aa) - np.log(w_pgd)),
                       "kaynak": "results/c1_seeds/c1_seed_summary.json pairs[].{resnet,vit}.{clean,pgd,aa}"}
    hucre_d = {}
    for h, uy in (("V-scr", ["ViT_Tiny_AT_s2001", "ViT_Tiny_AT_s2002", "ViT_Tiny_AT_s2003"]),
                  ("V-IN", ["V_IN_s2101", "V_IN_s2102"]), ("R224-scr", ["R224_scr_s1201", "R224_scr_s1202"]),
                  ("R224-IN", ["R224_IN_s1301", "R224_IN_s1302"]),
                  ("C1-R32", ["ResNet18_AT_s1001", "ResNet18_AT_s1002", "ResNet18_AT_s1003"])):
        hucre_d[h] = float(np.mean([out[m]["d_omega"] for m in uy]))
    # Kaymalar: sigma_m -1/2 d_omega_m - 1/2 ort_P d_omega_c ; rho_m: -d_omega_m + ort_P d_omega_c
    # Panel terimi karsitliklarda (H1, H2, H3) ve q'nun payinda (sigma_R - sigma_V) sadelesir.
    dH1 = -0.5 * (hucre_d["V-scr"] - hucre_d["R224-scr"])
    dH2 = -0.5 * ((hucre_d["V-IN"] - hucre_d["V-scr"]) - (hucre_d["R224-IN"] - hucre_d["R224-scr"]))
    dH3 = -0.5 * ((hucre_d["V-scr"] - hucre_d["R224-scr"]) + (hucre_d["V-IN"] - hucre_d["R224-IN"]))
    b2 = json.loads((O.KOK / "results/q1/konsey_ayrisim_b2.json").read_text(encoding="utf-8"))["b2"]["F_B2"]
    ka = b2["K-a"]
    q_yeni = []
    for (R, V), D, ds in zip(ka["ciftler"], ka["D"], ka["simetrik_pay"]):
        q_yeni.append((ds - 0.5 * (out[R]["d_omega"] - out[V]["d_omega"])) / D)
    kb = b2["K-b"]
    yari = (kb["ci90"][1] - kb["ci90"][0]) / 2
    rho_V_kayma_panelsiz = -hucre_d["V-scr"]
    esik = K.DELTA - yari - kb["ort"] - rho_V_kayma_panelsiz  # panel ort d_omega bu esigi asarsa CI90 ust > 0.10
    cnn_aralik = [hucre_d["C1-R32"], hucre_d["R224-scr"], hucre_d["R224-IN"]]
    return {"model": out, "hucre_ort_d_omega": hucre_d,
            "kayma": {"H1": dH1, "H2": dH2, "H3": dH3, "H3_yeni_nokta": 0.0033636 + dH3,
                      "q_tohum_yeni": q_yeni, "q_yeni_ort": float(np.mean(q_yeni)),
                      "K-b_kayma_panel_haric": rho_V_kayma_panelsiz,
                      "K-b_ci90_ust_0.10_asilir_eger_panel_ort_d_omega_buyukse": esik,
                      "olculen_CNN_d_omega_araligi": [min(cnn_aralik), max(cnn_aralik)],
                      "K-b_yeni_nokta_CNN_araligiyla": [kb["ort"] + rho_V_kayma_panelsiz + min(cnn_aralik),
                                                         kb["ort"] + rho_V_kayma_panelsiz + max(cnn_aralik)]},
            "uyari": "Yeni alti modelde AA yalniz ilk 1000 goruntude; C1 ciftinde tam test. Panel uyelerinin AA "
                     "kosullu w'si olculmedi; K-b icin yalniz esik verilir. H3 icin H3 nokta degeri 0,0034 (M9.3)."}


def b_capraz(M, t, P, P2):
    g = K.Alici(M)
    gr = {h: O.hucre(t, M, h) for h in ["V-scr", "V-IN", "R224-scr", "R224-IN", "C1-R32"]}
    gr["XCiT"] = list(P2)
    gr["panel"] = list(P)
    lt = {}

    def tau(a, b):
        key = tuple(sorted((a, b)))
        if key not in lt:
            lt[key] = float(K.ort_yapi(lambda wa, Ta: K.tau_ij(g, f, a, b, wa, Ta), "yari"))
        return lt[key]

    out = {}
    adlar = list(gr)
    for i, A in enumerate(adlar):
        for B in adlar[i:]:
            v = [tau(a, b) for a in gr[A] for b in gr[B] if a != b]
            if v:
                out[f"{A}|{B}"] = {"ort_log_tau": float(np.mean(v)), "n_cift": len(v),
                                   "min": float(np.min(v)), "max": float(np.max(v))}
    return out


def c_hodge(M, t, P, P2):
    g = K.Alici(M)
    mod = sorted(M.modeller())
    Kn = len(mod)
    iu = np.triu_indices(Kn, 1)
    r = {}
    for yapi in ("cift_tek", "tek_cift"):
        wa, Ta = ("cift", "tek") if yapi == "cift_tek" else ("tek", "cift")
        R = np.zeros((Kn, Kn))
        for a in range(Kn):
            for b in range(Kn):
                if a != b:
                    R[a, b] = K.r_ij(g, f, mod[a], mod[b], wa, Ta)
        r[yapi] = R

    def ayir(R):
        d = R.sum(1) / Kn
        gr = d[:, None] - d[None, :]
        return gr, R - gr

    g1, c1 = ayir(r["cift_tek"])
    g2, c2 = ayir(r["tek_cift"])
    Rm = 0.5 * (r["cift_tek"] + r["tek_cift"])
    gm, cm = ayir(Rm)
    gurultu = 0.5 * (r["cift_tek"] - r["tek_cift"])
    out = {"K": Kn, "modeller": mod,
           "potansiyel_payi_ortalama_r": float((gm[iu] ** 2).sum() / (Rm[iu] ** 2).sum()),
           "dolasim_rms": float(np.sqrt((cm[iu] ** 2).mean())),
           "yari_fark_gurultu_rms": float(np.sqrt((gurultu[iu] ** 2).mean())),
           "dolasim_yarilar_arasi_korelasyon": float(np.corrcoef(c1[iu], c2[iu])[0, 1]),
           "potansiyel_yarilar_arasi_korelasyon": float(np.corrcoef(g1[iu], g2[iu])[0, 1]),
           "not": "dolasim_rms ile yari_fark_gurultu_rms karsilastirilir; gurultu RMS'i iki bolunmus yari kestiriminin "
                  "farkinin yarisidir (ortalamanin ornekleme gurultusu icin kaba olcu)."}
    # serbest potansiyel ve omega
    om = np.array([np.log(M.h[(m, m)]["aw"][M.h[(m, m)]["tc"]].mean() * 100) for m in mod])
    L = np.zeros((Kn, Kn))
    for a in range(Kn):
        for b in range(Kn):
            if a != b:
                L[a, b] = K.ort_yapi(lambda wa, Ta: f(g(mod[a], mod[b], Ta)) - f(g(mod[b], mod[a], Ta)), "yari")
    dL = L.sum(1) / Kn  # delta_i = ort_j (log T_ij - log T_ji); saf w modelinde = ort omega - omega_i
    x = -(om - om.mean())
    y = dL - dL.mean()
    b = float((x * y).sum() / (x * x).sum())
    r2 = float(1 - ((y - b * x) ** 2).sum() / (y ** 2).sum())
    out["serbest_potansiyel_omega_egimi"] = {"egim_b": b, "R2": r2, "egim_1_beklenen": 1.0,
                                             "yorum": "b = 1 ise w potansiyeli tam tasir; b != 1 ise (1-b) omega yapisi r'ye "
                                                      "kalir ve rho_m'ye (1-b)(omega_m - ort_P omega) eklenir."}
    # b ile duzeltilmis rho(V-scr) ve H3
    idx = {m: i for i, m in enumerate(mod)}
    Pm = list(P)
    omP = float(np.mean([om[idx[c]] for c in Pm]))
    V = O.hucre(t, M, "V-scr")
    duz = {}
    for m in mod:
        duz[m] = (1 - b) * (om[idx[m]] - omP)
    out["b_ile_rho_kaymasi"] = {"V-scr_ort": float(np.mean([duz[v] for v in V])),
                               "H3_kayma": float(0.5 * (np.mean([duz[m] for m in O.hucre(t, M, "V-scr")]) -
                                                        np.mean([duz[m] for m in O.hucre(t, M, "R224-scr")]) +
                                                        np.mean([duz[m] for m in O.hucre(t, M, "V-IN")]) -
                                                        np.mean([duz[m] for m in O.hucre(t, M, "R224-IN")])))}
    return out


def d_h1_bolus(M, t, P):
    g = K.Alici(M)
    out = {}
    for h in ["V-scr", "R224-scr", "V-IN", "R224-IN"]:
        A, B = [], []
        for m in O.hucre(t, M, h):
            Pm = [c for c in P if c != m]
            A.append(K.ort_yapi(lambda wa, Ta: sum(0.5 * (f(g(m, c, Ta)) + f(g(c, m, Ta))) for c in Pm) / len(Pm), "yari"))
            B.append(K.ort_yapi(lambda wa, Ta: 0.5 * f(g(m, m, wa)), "yari"))
        out[h] = {"ham_simetrik_log_T": float(np.mean(A)), "yarim_omega": float(np.mean(B))}
    H1 = (out["V-scr"]["ham_simetrik_log_T"] - out["R224-scr"]["ham_simetrik_log_T"]) - \
        (out["V-scr"]["yarim_omega"] - out["R224-scr"]["yarim_omega"])
    H2_ham = (out["V-IN"]["ham_simetrik_log_T"] - out["V-scr"]["ham_simetrik_log_T"]) - \
        (out["R224-IN"]["ham_simetrik_log_T"] - out["R224-scr"]["ham_simetrik_log_T"])
    H2_om = -((out["V-IN"]["yarim_omega"] - out["V-scr"]["yarim_omega"]) -
              (out["R224-IN"]["yarim_omega"] - out["R224-scr"]["yarim_omega"]))
    return {"hucre": out, "H1_yeniden": float(H1),
            "H1_ham_simetrik_bilesen": out["V-scr"]["ham_simetrik_log_T"] - out["R224-scr"]["ham_simetrik_log_T"],
            "H1_eksi_yarim_delta_omega": -(out["V-scr"]["yarim_omega"] - out["R224-scr"]["yarim_omega"]),
            "H2_ham_simetrik_bilesen": float(H2_ham), "H2_omega_bileseni": float(H2_om)}


def e_her_ikisi(M, t, P, b4_var):
    gb = O.AliciBC(M)
    ciftler = [tuple(c) for c in t["b2_tohum_ciftleri"]]
    V = O.hucre(t, M, "V-scr")
    a = O.kb_ka(gb, f, ciftler, V, P)
    out = {"K-a_q": a["q"], "K-a_q_ort": a["q_ort"], "G": a["G"], "K-b": a["K-b"]}
    if b4_var:
        hucreler = {h: O.hucre(t, M, h) for h in K.HUC4}
        h, sig, rho = O.b4(gb, f, hucreler, P)
        out["B4"] = h
        out["hucre_sigma"] = sig
        out["hucre_rho"] = rho
    return out


def f_dogruluk(M, t, P, P2):
    g = K.Alici(M)
    mod = sorted(M.modeller())
    temiz = {m: float(M.h[(m, m)]["tc"].mean() * 100) for m in mod}
    sig = {m: O.md(g, f, m, P)["sigma"] for m in mod}
    aile = {m: t["modeller"][m]["aile"] if m in t["modeller"] else "?" for m in mod}
    cnn = [m for m in mod if aile[m] == "CNN"]
    x = np.array([temiz[m] for m in cnn])
    y = np.array([sig[m] for m in cnn])
    sl, ic, rr, pp, se = stats.linregress(x, y)
    res = {}
    for m in mod:
        if aile[m] != "CNN":
            res[m] = {"temiz": temiz[m], "sigma": sig[m], "cnn_cizgisi_ongorusu": float(ic + sl * temiz[m]),
                      "artik": float(sig[m] - (ic + sl * temiz[m]))}
    # yalniz sizin kendi CNN'leriniz (R32 ve R224) ile
    kendi = [m for m in cnn if t["modeller"][m]["hucre"] in ("C1-R32", "R224-scr", "R224-IN")]
    sl2, ic2, rr2, _, _ = stats.linregress([temiz[m] for m in kendi], [sig[m] for m in kendi])
    return {"cnn_modelleri": cnn, "egim_sigma_temiz_puan_basina": float(sl), "kesisim": float(ic), "r": float(rr),
            "p": float(pp), "x_araligi": [float(x.min()), float(x.max())],
            "cnn_disi_artiklar": res, "temiz": temiz, "sigma": sig,
            "yalniz_kendi_CNN": {"modeller": kendi, "egim": float(sl2), "r": float(rr2),
                                 "V-scr_ort_artik": float(np.mean([sig[m] - (ic2 + sl2 * temiz[m]) for m in O.hucre(t, M, 'V-scr')]))},
            "uyari": "V-scr temiz dogrulugu (yaklasik 73) CNN araliginin disinda; ongoru disdegerlemedir."}


def g_panel_jk(M, t, P):
    g = K.Alici(M)
    ciftler = [tuple(c) for c in t["b2_tohum_ciftleri"]]
    V = O.hucre(t, M, "V-scr")
    hucreler = {h: O.hucre(t, M, h) for h in K.HUC4}

    def hepsi(Pp):
        a = O.kb_ka(g, f, ciftler, V, Pp)
        h, _, _ = O.b4(g, f, hucreler, Pp)
        return {"q": a["q_ort"], "rho_V": a["K-b"]["ort"], "H1": h["H1"]["kestirim"], "H2": h["H2"]["kestirim"],
                "H3": h["H3"]["kestirim"], "_se": {"rho_V": a["K-b"]["se"], "H1": h["H1"]["se"], "H2": h["H2"]["se"],
                                                   "H3": h["H3"]["se"]}}

    tam = hepsi(P)
    jk = [hepsi([x for x in P if x != c]) for c in P]
    n = len(P)
    out = {}
    for k_ in ("q", "rho_V", "H1", "H2", "H3"):
        v = np.array([j[k_] for j in jk])
        se_jk = float(np.sqrt((n - 1) / n * ((v - v.mean()) ** 2).sum()))
        o = {"tam": tam[k_], "jk_degerler": v.tolist(), "se_panel_jackknife": se_jk}
        if k_ in tam["_se"]:
            se_k = tam["_se"][k_]
            se_t = float(np.sqrt(se_k ** 2 + se_jk ** 2))
            o.update({"se_kosu": se_k, "se_birlesik": se_t,
                      "ci90_birlesik_normal": [tam[k_] - 1.645 * se_t, tam[k_] + 1.645 * se_t]})
        out[k_] = o
    out["not"] = ("Panel uyesi bir populasyondan cekilmis sayilirsa (rastgele etki) jackknife SE panel ornekleme "
                  "belirsizligini verir; kosu SE'si ile karelerin toplami olarak birlestirildi (normal yaklasim, kaba).")
    return out


def main():
    M, t, P, P2 = O.yukle(*O.C10)
    M2, t2, Pc, P2c = O.yukle(*O.C100)
    sonuc = {
        "a_w_saldiri_bagimliligi": a_aa(M, t),
        "b_capraz_benzerlik": b_capraz(M, t, P, P2),
        "c_hodge_ve_serbest_potansiyel": c_hodge(M, t, P, P2),
        "d_H1_bolusu": d_h1_bolus(M, t, P),
        "e_her_ikisi_dogru": {"cifar10": e_her_ikisi(M, t, P, True), "cifar100": e_her_ikisi(M2, t2, Pc, False)},
        "f_sigma_temiz_dogruluk": f_dogruluk(M, t, P, P2),
        "g_panel_rastgele_etki": g_panel_jk(M, t, P),
    }
    O.yaz("ayrisim", sonuc, __file__)


if __name__ == "__main__":
    main()
