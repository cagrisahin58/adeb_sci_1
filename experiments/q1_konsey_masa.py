# -*- coding: utf-8 -*-
"""Konsey plani §5 masa cozumlemeleri (1)-(5) (29.10.2026). GPU yok, yeni olcum yok.

Tanimlar ve kestiriciler experiments/q1_konsey_ayrisim.py'den alinir (ayni kod yolu).
(1) Havuzun yedi AT modelinde sigma, rho, omega, S ve ResNet18_AT_s1001'e gore kaynak acigi ayrisimi;
    panel uyesi birakmali jackknife.
(2) Havuz r matrisinin Hodge ayrisimi (model duzeyi potansiyel ve dolasim payi), goruntu bootstrap gurultusu.
(3) Mahmood ve ark. 2021 8x8 matrisleri (dis karsilastirma, her-ikisi-dogru protokolu, standart egitim).
(4) CIFAR-10 (secilen, son kontrol noktasi, L2), CIFAR-100 ve SVHN cift matrislerinde potansiyel payi.
(5) Onerme 3 h olcegi ayar sinamasi C1 3x3'lerde (_p3_potansiyel_masa.py fonksiyonlariyla).
Girdiler yalniz results/c1_c3/* ve results/q1/* altindadir. Cikti: results/q1/konsey_masa/konsey_masa_cozumlemeleri.json
"""
import importlib.util
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "experiments"))
sys.path.insert(0, str(KOK))
import q1_konsey_ayrisim as A  # noqa: E402

CIKTI = KOK / "results" / "q1" / "konsey_masa" / "konsey_masa_cozumlemeleri.json"
TABLO = KOK / "raporlar" / "konsey_2026-10-29" / "hucre_tablosu.json"
R, V, X = "ResNet18_AT_s1001", "ViT_Tiny_AT_s2001", "Debenedetti2022Light_XCiT-S12"
PANEL = ["Wong2020Fast", "Engstrom2019Robustness", "Carmon2019Unlabeled", "Gowal2020Uncovering_28_10_extra"]
AT7 = [R, V, "Wong2020Fast", "Engstrom2019Robustness", "Carmon2019Unlabeled", X, "Gowal2020Uncovering_28_10_extra"]
B_HODGE = 400


def havuz():
    M = A.Matris()
    M.ekle(KOK / "results/q1/havuz_cifar10", A.HAVUZ_ESLEME)
    return M


def kaynak_acigi(g, m, P, kestirim, olcek="log", ref=R):
    """ref ile m arasinda ortak panel P \\ {m, ref} uzerinde D = S_ref - S_m = (sig_ref - sig_m) - 1/2 (rho_ref - rho_m)."""
    Pm = [c for c in P if c not in (m, ref)]
    a = A.model_duzeyi(g, ref, Pm, olcek, kestirim)
    b = A.model_duzeyi(g, m, Pm, olcek, kestirim)
    D = a["S"] - b["S"]
    sim = a["sigma"] - b["sigma"]
    yon = -0.5 * (a["rho"] - b["rho"])
    return {"panel": Pm, "D": D, "simetrik_pay": sim, "yonlu_pay": yon, "artik": D - sim - yon,
            "simetrik_oran": sim / D if abs(D) > 1e-12 else None}


def analiz1(M):
    g = A.Alici(M)
    out = {"panel": PANEL, "modeller": {}, "jackknife": {}}
    for m in AT7:
        kay = {}
        for k, o in A.TAHMINCILER:
            kay[f"{k}_{o}"] = A.model_duzeyi(g, m, PANEL, o, k)
        if m != R:
            kay["kaynak_acigi_R_eksi_m_yari_log"] = kaynak_acigi(g, m, PANEL, "yari")
            kay["kaynak_acigi_R_eksi_m_tam_log"] = kaynak_acigi(g, m, PANEL, "tam")
            kay["kaynak_acigi_R_eksi_m_yari_logit"] = kaynak_acigi(g, m, PANEL, "yari", "logit")
        out["modeller"][m] = kay
    for c in PANEL:
        Pj = [x for x in PANEL if x != c]
        jk = {}
        for m in AT7:
            if m == c:
                continue
            d = A.model_duzeyi(g, m, Pj, "log", "yari")
            jk[m] = {"sigma": d["sigma"], "rho": d["rho"]}
            if m != R:
                ka = kaynak_acigi(g, m, Pj, "yari")
                jk[m].update({"D": ka["D"], "simetrik_oran": ka["simetrik_oran"]})
        out["jackknife"][f"{c}_birakildi"] = jk
    # ozet: ViT ve XCiT icin jackknife araligi
    oz = {}
    for m in (V, X):
        vs = [out["jackknife"][k][m] for k in out["jackknife"] if m in out["jackknife"][k]]
        oz[m] = {key: [float(min(v[key] for v in vs)), float(max(v[key] for v in vs))]
                 for key in ("sigma", "rho", "simetrik_oran")}
    out["jackknife_aralik"] = oz
    return out


def hodge(Mx):
    K = Mx.shape[0]
    delta = Mx.sum(1) / K
    grad = delta[:, None] - delta[None, :]
    curl = Mx - grad
    iu = np.triu_indices(K, 1)
    nA = float((Mx[iu] ** 2).sum())
    return delta, grad, curl, (float((grad[iu] ** 2).sum() / nA) if nA > 0 else float("nan"))


def r_matrisi(g, mods, olcek, kestirim, b=None):
    f = A.olcek_f(olcek)
    K = len(mods)
    r = np.zeros((K, K))
    for i in range(K):
        for j in range(K):
            if i != j:
                v = A.ort_yapi(lambda wa, Ta: A.r_ij(g, f, mods[i], mods[j], wa, Ta), kestirim)
                r[i, j] = v if b is None else v[b]
    return r


def analiz2(M):
    g = A.Alici(M)
    rng = np.random.default_rng(A.BOOT_TOHUM)
    W = A.bootstrap_agirlik(M.n, B_HODGE, rng)
    gb = A.Alici(M, W)
    out = {"modeller": AT7, "B": B_HODGE}
    K = len(AT7)
    iu = np.triu_indices(K, 1)
    for kest, ol in (("yari", "log"), ("tam", "log"), ("yari", "logit")):
        r = r_matrisi(g, AT7, ol, kest)
        d, gr, cu, G = hodge(r)
        # bootstrap: dolasim gurultusu ve G araligi
        f = A.olcek_f(ol)
        rb = np.zeros((K, K, B_HODGE))
        for i in range(K):
            for j in range(K):
                if i != j:
                    rb[i, j] = A.ort_yapi(lambda wa, Ta: A.r_ij(gb, f, AT7[i], AT7[j], wa, Ta), kest)
        Gs, cs, ds = [], [], []
        for b in range(B_HODGE):
            d_, _, c_, G_ = hodge(rb[:, :, b])
            Gs.append(G_)
            cs.append(c_[iu])
            ds.append(d_)
        cs, ds = np.array(cs), np.array(ds)
        gur = float(np.sqrt((cs.std(0, ddof=1) ** 2).mean()))
        iR, iV = AT7.index(R), AT7.index(V)
        out[f"{kest}_{ol}"] = {
            "delta_potansiyel": {m: float(d[i]) for i, m in enumerate(AT7)},
            "delta_bootstrap_sd": {m: float(ds[:, i].std(ddof=1)) for i, m in enumerate(AT7)},
            "G_potansiyel_payi": G, "G_bootstrap_95": [float(np.percentile(Gs, 2.5)), float(np.percentile(Gs, 97.5))],
            "G_rastgele_beklenti_2_bolu_K": 2.0 / K, "dolasim_serbestlik": (K - 1) * (K - 2) // 2,
            "dolasim_rms": float(np.sqrt((cu[iu] ** 2).mean())), "dolasim_gurultu_rms": gur,
            "dolasim_rms_bolu_gurultu": float(np.sqrt((cu[iu] ** 2).mean())) / gur if gur > 0 else None,
            "r_rms": float(np.sqrt((r[iu] ** 2).mean())),
            "RV_cifti": {"r_RV": float(r[iR, iV]), "potansiyel_farki_delta_R_eksi_delta_V": float(d[iR] - d[iV]),
                         "dolasim_RV": float(cu[iR, iV])},
            "r_matrisi": r.tolist()}
    return out


def analiz3():
    yol = KOK / "results/q1/dis_veri/mahmood2021_tablolar.json"
    d = json.loads(yol.read_text(encoding="utf-8"))
    mods = d["model_adlari"]
    aile = d["aile"]
    out = {"kaynak": str(yol.relative_to(KOK)), "kaynak_sha256": A.sha256(yol), "etiket": (
        "DIS KARSILASTIRMA: Mahmood ve ark. 2021 (arXiv 2104.02610), her-ikisi-dogru protokolu, m = 1000, "
        "standart egitim (AT degil). Kosegen beyaz kutu DEGILDIR (bagimsiz egitilmis ikinci kopyaya transfer); "
        "w tanimsizdir. Bu yuzden on kayitli w-tau-r ayrisimi bu veride kurulamaz; asagida (a) yalniz T'den "
        "kurulabilen log asimetri ve simetrik geometrik ortalama, (b) kosegeni VEKIL w sayan ayrisim verilir; "
        "(b) beyaz kutu anlaminda okunamaz."),
        "yon_notu": d["yon_dogrulamasi"].get("tablo2_basligi")}
    cnn = [m for m in mods if aile[m] == "CNN"]
    for ds in ("CIFAR-10", "CIFAR-100"):
        Mx = d["transfer_matrisleri_yuzde"][ds]
        T = np.array([[Mx[s][t] for t in mods] for s in mods], float)
        K = len(mods)
        L = np.zeros((K, K))
        for i in range(K):
            for j in range(K):
                if i != j:
                    L[i, j] = np.log(T[i, j] / T[j, i])
        dl, _, cu, G = hodge(L)
        iu = np.triu_indices(K, 1)
        sim = {}
        for i in range(K):
            for j in range(i + 1, K):
                gk = "-".join(sorted([aile[mods[i]], aile[mods[j]]]))
                sim.setdefault(gk, []).append(0.5 * np.log(T[i, j] * T[j, i]))
        kay = {"log_asimetri_hodge": {"delta": {m: float(dl[i]) for i, m in enumerate(mods)}, "G_potansiyel_payi": G,
                                      "G_rastgele_beklenti": 2.0 / K,
                                      "dolasim_rms": float(np.sqrt((cu[iu] ** 2).mean()))},
               "log_geometrik_ortalama_aile": {k: {"n": len(v), "ort": float(np.mean(v)), "min": float(np.min(v)),
                                                   "max": float(np.max(v))} for k, v in sim.items()}}
        # (b) vekil w = kosegen
        w = np.diag(T)
        vek = {}
        for m in mods:
            P = [c for c in cnn if c != m]
            i = mods.index(m)
            sig = np.mean([0.5 * (np.log(T[i, mods.index(c)] * T[mods.index(c), i]) - np.log(w[i] * w[mods.index(c)])) for c in P])
            rho = np.mean([np.log(T[mods.index(c), i] / T[i, mods.index(c)]) - np.log(w[i] / w[mods.index(c)]) for c in P])
            S = np.mean([np.log(T[i, mods.index(c)]) for c in P])
            vek[m] = {"aile": aile[m], "sigma_vekil": float(sig), "rho_vekil": float(rho), "omega_vekil": float(np.log(w[i])),
                      "S": float(S), "panel": P}
        kay["vekil_w_ayrisimi_CNN_paneli"] = vek
        # ViT ailesinin CNN paneline karsi kaynak acigi (BiT-M-R50x1 referansina gore degil; aile ortalamasi)
        vit = [m for m in mods if aile[m] == "ViT"]
        kay["aile_ortalamasi_vekil"] = {
            "ViT_sigma": float(np.mean([vek[m]["sigma_vekil"] for m in vit])),
            "ViT_rho": float(np.mean([vek[m]["rho_vekil"] for m in vit])),
            "CNN_sigma_panel_ici": float(np.mean([vek[m]["sigma_vekil"] for m in cnn])),
            "CNN_rho_panel_ici": float(np.mean([vek[m]["rho_vekil"] for m in cnn]))}
        out[ds] = kay
    return out


def baglamlar4():
    b = []
    for k in (1, 2, 3):
        b.append(("cifar10_linf_secilen", f"results/c1_c3/pair{k}", k))
        b.append(("cifar10_linf_son_kontrol", f"results/q1/son_kontrol_noktasi/pair{k}", k))
        b.append(("cifar100_linf_secilen", f"results/q1/cifar100/transfer/pair{k}", k))
        b.append(("cifar10_l2_secilen", f"results/q1/cifar10_l2/transfer/pair{k}", k))
    for k in (1, 2):
        b.append(("svhn_linf_secilen", f"results/q1/svhn/transfer/pair{k}", k))
    return b


def analiz4():
    out = {"tanim": "potansiyel payi = log(w_j/w_i) / log(T_ij/T_ji); i kaynak (CNN ya da ResNet), j hedef",
           "ciftler": {}, "ozet": {}}
    for ad, dz, k in baglamlar4():
        p = KOK / dz
        if not p.exists():
            continue
        M = A.Matris()
        M.ekle(p, {"ResNet18_AT": "R", "ViT_Tiny_AT": "V", "WRN_28_10": "W"})
        g = A.Alici(M)
        mods = [m for m in ("R", "V", "W") if (m, m) in M.h]
        kay = {"n": M.n}
        for i, j in (("R", "V"), ("R", "W"), ("V", "W")):
            if i in mods and j in mods:
                t = A.cift_nicelik(g, i, j)
                y = A.cift_yari(g, i, j)
                kay[f"{i}->{j}"] = {"tam": {kk: t[kk] for kk in ("asimetri_puan", "log_oran", "log_w_potansiyel", "r",
                                                               "log_tau", "potansiyel_payi", "w_i", "w_j")},
                                    "bolunmus_yari": dict(y, potansiyel_payi=(y["log_w_potansiyel"] / y["log_oran"]
                                                                             if abs(y["log_oran"]) > 1e-9 else None))}
        out["ciftler"][f"{ad}/pair{k}"] = kay
    for ad in sorted({a for a, _, _ in baglamlar4()}):
        ks = [v for kk, v in out["ciftler"].items() if kk.startswith(ad + "/") and "R->V" in v]
        if not ks:
            continue
        oz = {}
        for kk in ("log_oran", "log_w_potansiyel", "r", "potansiyel_payi", "log_tau", "asimetri_puan"):
            a = np.array([v["R->V"]["tam"][kk] for v in ks], float)
            oz[kk] = {"degerler": a.tolist(), "ort": float(a.mean()), "sd": float(a.std(ddof=1)) if len(a) > 1 else None}
        a = np.array([v["R->V"]["bolunmus_yari"]["potansiyel_payi"] for v in ks], float)
        oz["potansiyel_payi_bolunmus_yari"] = {"degerler": a.tolist(), "ort": float(a.mean()),
                                               "sd": float(a.std(ddof=1)) if len(a) > 1 else None}
        out["ozet"][ad] = oz
    return out


def analiz5():
    yol = KOK / "raporlar/konsey_2026-10-29/_p3_potansiyel_masa.py"
    spec = importlib.util.spec_from_file_location("p3pot", yol)
    p3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p3)
    out = {"fonksiyon_kaynagi": str(yol.relative_to(KOK)), "fonksiyon_kaynagi_sha256": A.sha256(yol),
           "not": ("K = 3: toplamsal uydurmada 6 hucre, 5 parametre (1 artik serbestlik); Hodge dolasimi 1 serbestlik. "
                   "Oranlar oran olceginde yuzde degil kesirdir (fonksiyonun kendi birimi)."),
           "kumeler": {}}
    uc = ["ResNet18_AT", "ViT_Tiny_AT", "WRN_28_10"]
    for ad, sab in (("c10_secilen", "results/c1_c3/pair{}"), ("c10_son_kontrol", "results/q1/son_kontrol_noktasi/pair{}"),
                    ("c100_secilen", "results/q1/cifar100/transfer/pair{}"), ("c10_l2", "results/q1/cifar10_l2/transfer/pair{}")):
        for k in (1, 2, 3):
            kl = sab.format(k)
            h = p3.yukle(kl, uc)
            Rb = p3.oran_matrisleri(h, uc)
            at = p3.ayar_testi(Rb, h, uc)
            out["kumeler"][f"{ad}/pair{k}"] = {
                "g_mutlak_en_buyuk": at["g_mutlak_en_buyuk"], "g_mutlak_ortalama": at["g_mutlak_ortalama"],
                "p_en_kucuk": at["p_en_kucuk"], "temiz_dogruluk": at["temiz_dogruluk"],
                **{f"{o}": {kk: at[o][kk] for kk in ("kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD",
                                                    "dolasim_raw_eksi_tc_rms_bolu_dolasim_tc_rms",
                                                    "kaynak_alfa_bc_eksi_tc_bolu_tc_alfa_SD",
                                                    "dolasim_bc_eksi_tc_rms_bolu_dolasim_tc_rms",
                                                    "hedef_beta_raw_eksi_tc_ile_tau_korelasyonu")}
                   for o in ("oran", "logit", "h")}}
    return out


def main():
    t0 = datetime.now(timezone.utc)
    M = havuz()
    sonuc = {"betik": "experiments/q1_konsey_masa.py", "betik_sha256": A.sha256(__file__),
             "ayrisim_betigi_sha256": A.sha256(KOK / "experiments/q1_konsey_ayrisim.py"),
             "uretildi_utc": t0.isoformat(), "havuz_tutarlilik": M.tutarlilik(),
             "not": "Tek tohumlu havuz ve dort uyeli panel: on kayit oncesi gorulmus veri, sinama degil.",
             "1_havuz_model_tablosu": analiz1(M), "2_hodge_r": analiz2(M), "3_mahmood": analiz3(),
             "4_potansiyel_payi": analiz4(), "5_onerme3_h_olcegi": analiz5()}
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with io.open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        json.dump(A.jsonla(sonuc), f, ensure_ascii=False, indent=1)
    print("yazildi:", CIKTI, "sure", (datetime.now(timezone.utc) - t0).total_seconds(), "s")


if __name__ == "__main__":
    main()
