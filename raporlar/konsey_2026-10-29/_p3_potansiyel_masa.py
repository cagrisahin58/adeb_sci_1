# -*- coding: utf-8 -*-
"""Konsey P3 (kuram ve olcum) masa testi, 29.10.2026.

Yeni olcum YOK, GPU YOK. Mevcut ornek bazli kayitlardan:
  1) Transfer asimetri matrisinin Hodge ayrismasi (potansiyel farki + dolasim),
     uc olcekte (oran, logit, h = -log(1 - oran)) ve uc protokolde (raw, tc, bc).
  2) "Ayar (gauge) onermesi": h olceginde raw ile tc arasindaki fark saf hedef
     ana etkisi -log(temiz dogruluk_j) arti kucuk bir bozucu terim g_ij'dir;
     kaynak etkileri ve dolasim protokolden bagimsiz kalmalidir.
  3) Tek-donusturuculu tasarimda ayni-aile benzerlik terimi gamma'nin kaynak
     ve hedef paylarina tam karismasi; havuzda olculebilen benzerlik terimleri
     (ayni mimari ciftleri) ve bootstrap araliklari.
Calistirma (depo kokunden): python raporlar/konsey_2026-10-29/_p3_potansiyel_masa.py
Cikti: raporlar/konsey_2026-10-29/_p3_potansiyel_masa.json
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
CIKTI = os.path.join(KOK, "raporlar", "konsey_2026-10-29", "_p3_potansiyel_masa.json")
B = 400
RNG = np.random.default_rng(20261029)
EPS = 1e-6


def yukle(klasor, modeller):
    """Hucre basina dort gosterge vektoru."""
    h = {}
    for s in modeller:
        for t in modeller:
            if s == t:
                continue
            yol = os.path.join(KOK, klasor, f"per_sample_{s}_to_{t}.npz")
            z = np.load(yol)
            h[(s, t)] = {k: z[k].astype(bool) for k in z.files}
    return h


def oran_matrisleri(h, modeller, agirlik=None):
    """agirlik: (n,) ya da (n, B) sayim; None ise esit. Donus: protokol -> (K, K[, B])."""
    K = len(modeller)
    n = next(iter(h.values()))["target_adv_wrong"].shape[0]
    W = np.ones((n, 1)) if agirlik is None else agirlik
    Bn = W.shape[1]
    out = {p: np.full((K, K, Bn), np.nan) for p in ("raw", "tc", "bc")}
    for i, s in enumerate(modeller):
        for j, t in enumerate(modeller):
            if s == t:
                continue
            d = h[(s, t)]
            aw = d["target_adv_wrong"].astype(float)
            tc = d["target_clean_correct"].astype(float)
            bc = (d["target_clean_correct"] & d["source_clean_correct"]).astype(float)
            out["raw"][i, j] = (aw @ W) / W.sum(0)
            out["tc"][i, j] = ((aw * tc) @ W) / (tc @ W)
            out["bc"][i, j] = ((aw * bc) @ W) / (bc @ W)
    return out


def olcek(R, ad):
    R = np.clip(R, EPS, 1 - EPS)
    if ad == "oran":
        return 100.0 * R
    if ad == "logit":
        return np.log(R / (1 - R))
    if ad == "h":
        return -np.log(1 - R)
    raise ValueError(ad)


def hodge(T):
    """T: (K, K) kosegeni anlamsiz. A = T - T^T. Tam grafikte en kucuk kareler
    potansiyeli delta_i = (1/K) sum_j A_ij. Donus: delta, grad, curl, G."""
    K = T.shape[0]
    A = T - T.T
    np.fill_diagonal(A, 0.0)
    delta = A.sum(1) / K
    grad = delta[:, None] - delta[None, :]
    curl = A - grad
    iu = np.triu_indices(K, 1)
    nA = float((A[iu] ** 2).sum())
    nG = float((grad[iu] ** 2).sum())
    G = nG / nA if nA > 0 else float("nan")
    return delta, grad, curl, G, A


def toplamsal(T):
    """Kosegen disi hucrelerde T_ij = mu + a_i + b_j (toplam-sifir).
    Tam tasarimda simetrik ve ters-simetrik kisimlar ortogonal ayrisir."""
    K = T.shape[0]
    satir, y = [], []
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            x = np.zeros(1 + 2 * (K - 1))
            x[0] = 1.0
            # etki kodlamasi: son model = -(digerleri toplami)
            if i < K - 1:
                x[1 + i] = 1.0
            else:
                x[1:K] = -1.0
            if j < K - 1:
                x[K + j] = 1.0
            else:
                x[K:2 * K - 1] = -1.0
            satir.append(x)
            y.append(T[i, j])
    X = np.array(satir)
    y = np.array(y)
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    mu = coef[0]
    a = np.append(coef[1:K], -coef[1:K].sum())
    b = np.append(coef[K:2 * K - 1], -coef[K:2 * K - 1].sum())
    yhat = X @ coef
    res = y - yhat
    R2 = 1 - (res ** 2).sum() / ((y - y.mean()) ** 2).sum()
    return mu, a, b, float(R2), float(np.sqrt((res ** 2).mean()))


def benzerlik_uydur(T, modeller, gruplar):
    """Toplamsal model + her grup icin simetrik benzerlik gostergesi
    (gruptaki modeller arasindaki kosegen disi hucreler). Donus: gamma sozlugu
    ve tanimlanabilirlik (rank) bilgisi."""
    K = len(modeller)
    ad2i = {m: i for i, m in enumerate(modeller)}
    satir, y = [], []
    for i in range(K):
        for j in range(K):
            if i == j:
                continue
            x = np.zeros(2 * K + len(gruplar))
            x[i] = 1.0
            x[K + j] = 1.0
            for g, (gad, uyeler) in enumerate(gruplar.items()):
                if modeller[i] in uyeler and modeller[j] in uyeler:
                    x[2 * K + g] = 1.0
            satir.append(x)
            y.append(T[i, j])
    X = np.array(satir)
    y = np.array(y)
    # a ve b icin ortak sabit serbestligi: rank kontrolu
    rank = int(np.linalg.matrix_rank(X))
    rank0 = int(np.linalg.matrix_rank(X[:, :2 * K]))
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    gam = {gad: float(coef[2 * K + g]) for g, gad in enumerate(gruplar)}
    tanimli = {}
    for g, gad in enumerate(gruplar):
        Xg = np.delete(X, 2 * K + g, axis=1)
        tanimli[gad] = int(np.linalg.matrix_rank(Xg)) < rank
    return gam, tanimli, rank, rank0


def ozet_hodge(Rb, modeller, olcekler=("oran", "logit", "h")):
    """Rb: protokol -> (K, K, 1+B); ilk dilim nokta tahmini."""
    K = len(modeller)
    iu = np.triu_indices(K, 1)
    out = {}
    for p, R in Rb.items():
        out[p] = {}
        for o in olcekler:
            T = olcek(R, o)
            d0, g0, c0, G0, A0 = hodge(T[:, :, 0])
            Gs, cs, ds = [], [], []
            for b in range(1, T.shape[2]):
                d, g, c, G, A = hodge(T[:, :, b])
                Gs.append(G)
                cs.append(c[iu])
                ds.append(d)
            cs = np.array(cs)
            ds = np.array(ds)
            curl_gurultu_sd = cs.std(0, ddof=1)
            curl_rms = float(np.sqrt((c0[iu] ** 2).mean()))
            gurultu_rms = float(np.sqrt((curl_gurultu_sd ** 2).mean()))
            mu, a, bb, R2, rmse = toplamsal(T[:, :, 0])
            out[p][o] = {
                "G_potansiyel_payi": G0,
                "G_bootstrap_95": [float(np.percentile(Gs, 2.5)), float(np.percentile(Gs, 97.5))],
                "G_rastgele_beklenti_2_bolu_K": 2.0 / K,
                "dolasim_serbestlik": (K - 1) * (K - 2) // 2,
                "potansiyel_serbestlik": K - 1,
                "dolasim_rms": curl_rms,
                "dolasim_ornekleme_gurultusu_rms": gurultu_rms,
                "dolasim_rms_bolu_gurultu": curl_rms / gurultu_rms if gurultu_rms > 0 else None,
                "asimetri_rms": float(np.sqrt((A0[iu] ** 2).mean())),
                "potansiyel_delta": {m: float(d0[i]) for i, m in enumerate(modeller)},
                "potansiyel_delta_bootstrap_sd": {m: float(ds[:, i].std(ddof=1)) for i, m in enumerate(modeller)},
                "toplamsal": {
                    "mu": float(mu), "R2": R2, "rmse": rmse,
                    "kaynak_alfa": {m: float(a[i]) for i, m in enumerate(modeller)},
                    "hedef_beta": {m: float(bb[i]) for i, m in enumerate(modeller)},
                    "simetrik_katilim_s_eksi_ortalama": {m: float(a[i] + bb[i]) for i, m in enumerate(modeller)},
                },
            }
    return out


def ayar_testi(Rb0, h, modeller):
    """h olceginde raw - tc = tau_j + g_ij; tau_j = -log(acc_j)."""
    K = len(modeller)
    acc = np.zeros(K)
    p = np.full((K, K), np.nan)
    for j, t in enumerate(modeller):
        s0 = modeller[0] if modeller[0] != t else modeller[1]
        acc[j] = h[(s0, t)]["target_clean_correct"].mean()
    for i, s in enumerate(modeller):
        for j, t in enumerate(modeller):
            if s == t:
                continue
            d = h[(s, t)]
            yanlis = ~d["target_clean_correct"]
            p[i, j] = d["target_adv_wrong"][yanlis].mean() if yanlis.sum() else np.nan
    rraw = Rb0["raw"][:, :, 0]
    rtc = Rb0["tc"][:, :, 0]
    rbc = Rb0["bc"][:, :, 0]
    e = 1 - acc
    g = -np.log(1 + e[None, :] * (1 - p) / ((1 - e[None, :]) * (1 - rtc)))
    np.fill_diagonal(g, 0.0)
    out = {"temiz_dogruluk": {m: float(acc[i]) for i, m in enumerate(modeller)},
           "p_en_kucuk": float(np.nanmin(p)),
           "g_mutlak_en_buyuk": float(np.nanmax(np.abs(g))),
           "g_mutlak_ortalama": float(np.nanmean(np.abs(g[~np.eye(K, dtype=bool)])))}
    for o in ("oran", "logit", "h"):
        Tr = olcek(rraw, o)
        Tt = olcek(rtc, o)
        Tb = olcek(rbc, o)
        _, ar, br, _, _ = toplamsal(Tr)
        _, at, bt, _, _ = toplamsal(Tt)
        _, ab, bb, _, _ = toplamsal(Tb)
        _, _, cr, _, _ = hodge(Tr)
        _, _, ct, _, _ = hodge(Tt)
        _, _, cb, _, _ = hodge(Tb)
        iu = np.triu_indices(K, 1)
        # olcek birimini karsilastirilabilir kilmak icin kaynak etkisi farkini
        # tc kaynak etkilerinin yayilimina (SD) boleriz
        sd_at = float(np.std(at, ddof=1))
        out[o] = {
            "kaynak_alfa_raw_eksi_tc_en_buyuk_mutlak": float(np.max(np.abs(ar - at))),
            "kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD": float(np.max(np.abs(ar - at)) / sd_at),
            "hedef_beta_raw_eksi_tc_ile_tau_korelasyonu": float(np.corrcoef(br - bt, -np.log(acc) - np.mean(-np.log(acc)))[0, 1]),
            "dolasim_raw_eksi_tc_rms_bolu_dolasim_tc_rms": float(np.sqrt(((cr - ct)[iu] ** 2).mean()) / np.sqrt((ct[iu] ** 2).mean())),
            "kaynak_alfa_bc_eksi_tc_bolu_tc_alfa_SD": float(np.max(np.abs(ab - at)) / sd_at),
            "dolasim_bc_eksi_tc_rms_bolu_dolasim_tc_rms": float(np.sqrt(((cb - ct)[iu] ** 2).mean()) / np.sqrt((ct[iu] ** 2).mean())),
            "kaynak_alfa_raw": {m: float(ar[i]) for i, m in enumerate(modeller)},
            "kaynak_alfa_tc": {m: float(at[i]) for i, m in enumerate(modeller)},
            "kaynak_alfa_bc": {m: float(ab[i]) for i, m in enumerate(modeller)},
        }
    return out


def bootstrap_agirlik(n, B):
    idx = RNG.integers(0, n, size=(B, n))
    W = np.zeros((n, B))
    for b in range(B):
        W[:, b] = np.bincount(idx[b], minlength=n)
    return np.concatenate([np.ones((n, 1)), W], axis=1)


def kume_analizi(klasor, modeller, gruplar=None, alt_kumeler=None):
    h = yukle(klasor, modeller)
    n = next(iter(h.values()))["target_adv_wrong"].shape[0]
    W = bootstrap_agirlik(n, B)
    Rb = oran_matrisleri(h, modeller, W)
    sonuc = {"klasor": klasor, "modeller": modeller, "n": int(n), "B": B,
             "hodge": ozet_hodge(Rb, modeller),
             "ayar_testi": ayar_testi(Rb, h, modeller)}
    if alt_kumeler:
        sonuc["alt_kumeler"] = {}
        for ad, alt in alt_kumeler.items():
            ix = [modeller.index(m) for m in alt]
            Rs = {p: R[np.ix_(ix, ix)] for p, R in Rb.items()}
            sonuc["alt_kumeler"][ad] = {"modeller": alt, "hodge": ozet_hodge(Rs, alt)}
    if gruplar:
        sonuc["benzerlik"] = {}
        for p in ("tc", "bc", "raw"):
            sonuc["benzerlik"][p] = {}
            for o in ("oran", "h"):
                T = olcek(Rb[p], o)
                g0, tanimli, rk, rk0 = benzerlik_uydur(T[:, :, 0], modeller, gruplar)
                gb = {k: [] for k in gruplar}
                for b in range(1, T.shape[2]):
                    gg, _, _, _ = benzerlik_uydur(T[:, :, b], modeller, gruplar)
                    for k in gruplar:
                        gb[k].append(gg[k])
                sonuc["benzerlik"][p][o] = {
                    k: {"gamma": g0[k], "tanimli": tanimli[k],
                        "bootstrap_95": [float(np.percentile(gb[k], 2.5)), float(np.percentile(gb[k], 97.5))]}
                    for k in gruplar}
                sonuc["benzerlik"][p][o]["_rank"] = [rk, rk0]
    return sonuc


def mahmood():
    d = json.load(io.open(os.path.join(KOK, "results", "q1", "dis_veri", "mahmood2021_tablolar.json"), encoding="utf-8"))
    out = {}
    for ds in ("CIFAR-10", "CIFAR-100"):
        M = d["transfer_matrisleri_yuzde"][ds]
        mods = d["model_adlari"]
        K = len(mods)
        R = np.array([[M[s][t] / 100.0 for t in mods] for s in mods])
        out[ds] = {}
        for o in ("oran", "logit", "h"):
            T = olcek(R, o)
            dlt, g, c, G, A = hodge(T)
            # binom gurultusu (m = 1000, hucre bagimsiz varsayimi), parametrik
            cs = []
            for b in range(B):
                Rb_ = RNG.binomial(1000, np.clip(R, EPS, 1 - EPS)) / 1000.0
                _, _, cb_, _, _ = hodge(olcek(Rb_, o))
                cs.append(cb_[np.triu_indices(K, 1)])
            cs = np.array(cs)
            iu = np.triu_indices(K, 1)
            gur = float(np.sqrt((cs.std(0, ddof=1) ** 2).mean()))
            out[ds][o] = {"G_potansiyel_payi": G, "G_rastgele_beklenti": 2.0 / K,
                          "dolasim_rms": float(np.sqrt((c[iu] ** 2).mean())),
                          "dolasim_binom_gurultu_rms": gur,
                          "potansiyel_delta": {m: float(dlt[i]) for i, m in enumerate(mods)}}
    out["not"] = "Dis veri (arXiv:2104.02610), bc protokolu, standart egitim, m = 1000; gurultu hucre bagimsiz binom varsayimiyla, yaklasik."
    return out


def main():
    havuz_mod = ["ResNet18_AT", "ViT_Tiny_AT", "Standard_WRN28_10", "Wong2020_PRN18",
                 "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Debenedetti2022_XCiT_S12",
                 "Gowal2020_WRN28_10"]
    gruplar = {
        "ayni_mimari_WRN28_10_gurbuz": ["Carmon2019_WRN28_10", "Gowal2020_WRN28_10"],
        "ayni_mimari_ResNet18_PRN18": ["ResNet18_AT", "Wong2020_PRN18"],
        "dikkat_tabanli_ViT_XCiT": ["ViT_Tiny_AT", "Debenedetti2022_XCiT_S12"],
    }
    alt = {"yalniz_AT_7": [m for m in havuz_mod if m != "Standard_WRN28_10"],
           "yalniz_AT_ViTsiz_6": [m for m in havuz_mod if m not in ("Standard_WRN28_10", "ViT_Tiny_AT")]}
    sonuc = {"uretildi_utc": datetime.now(timezone.utc).isoformat(),
             "betik": "raporlar/konsey_2026-10-29/_p3_potansiyel_masa.py",
             "yontem": ("Hodge: A = T - T^T, delta_i = (1/K) sum_j A_ij, grad = delta_i - delta_j, dolasim = A - grad; "
                        "G = ||grad||^2/||A||^2 (i<j); rastgele ters-simetrik matriste E[G] = 2/K. "
                        "Bootstrap: goruntu duzeyi, tum hucrelerde ortak yeniden ornekleme, B = %d. "
                        "Olcekler: oran (puan), logit, h = -log(1 - oran). Ayar testi: h olceginde raw - tc = -log(acc_j) + g_ij." % B),
             "havuz_cifar10": kume_analizi("results/q1/havuz_cifar10", havuz_mod, gruplar, alt)}
    uc = ["ResNet18_AT", "ViT_Tiny_AT", "WRN_28_10"]
    sonuc["c1_3x3"] = {f"pair{k}": kume_analizi(f"results/c1_c3/pair{k}", uc) for k in (1, 2, 3)}
    sonuc["c100_3x3"] = {f"pair{k}": kume_analizi(f"results/q1/cifar100/transfer/pair{k}", uc) for k in (1, 2, 3)}
    tz = ["ResNet18_clean", "ViT_Tiny_clean", "Standard_WRN28_10"]
    sonuc["temiz_3x3"] = {f"pair{k}": kume_analizi(f"results/q1/temiz_ciftler/pair{k}", tz) for k in (1, 2, 3)}
    sonuc["mahmood2021"] = mahmood()
    with io.open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)

    # kisa ozet
    H = sonuc["havuz_cifar10"]
    for p in ("raw", "tc", "bc"):
        for o in ("oran", "logit", "h"):
            x = H["hodge"][p][o]
            print(f"havuz {p:3s} {o:5s} G={x['G_potansiyel_payi']:.3f} [{x['G_bootstrap_95'][0]:.3f},{x['G_bootstrap_95'][1]:.3f}] "
                  f"dolasim/gurultu={x['dolasim_rms_bolu_gurultu']:.1f} R2_top={x['toplamsal']['R2']:.3f}")
    for ad, a in H["alt_kumeler"].items():
        for p in ("tc", "bc"):
            for o in ("oran", "h"):
                x = a["hodge"][p][o]
                print(f"  {ad} {p} {o} G={x['G_potansiyel_payi']:.3f} dolasim/gurultu={x['dolasim_rms_bolu_gurultu']:.1f}")
    print("ayar testi havuz:", json.dumps({k: v for k, v in H["ayar_testi"].items() if not isinstance(v, dict) or k in ()}, ensure_ascii=False))
    for o in ("oran", "logit", "h"):
        x = H["ayar_testi"][o]
        print(f"  {o}: alfa(raw-tc)/SD={x['kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD']:.3f} "
              f"dolasim(raw-tc)/dolasim_tc={x['dolasim_raw_eksi_tc_rms_bolu_dolasim_tc_rms']:.3f} "
              f"alfa(bc-tc)/SD={x['kaynak_alfa_bc_eksi_tc_bolu_tc_alfa_SD']:.3f} "
              f"dolasim(bc-tc)/dolasim_tc={x['dolasim_bc_eksi_tc_rms_bolu_dolasim_tc_rms']:.3f} "
              f"r(beta_raw-beta_tc, tau)={x['hedef_beta_raw_eksi_tc_ile_tau_korelasyonu']:.3f}")
    print("benzerlik:", json.dumps(H["benzerlik"], ensure_ascii=False))
    for ds in ("c1_3x3", "c100_3x3", "temiz_3x3"):
        for pk, x in sonuc[ds].items():
            for p in ("tc", "bc", "raw"):
                y = x["hodge"][p]["oran"]
                yh = x["hodge"][p]["h"]
                print(f"{ds} {pk} {p}: G_oran={y['G_potansiyel_payi']:.3f} dolasim_oran={y['dolasim_rms']:.2f} "
                      f"gurultu={y['dolasim_ornekleme_gurultusu_rms']:.2f} | G_h={yh['G_potansiyel_payi']:.3f} "
                      f"dolasim_h/gurultu={yh['dolasim_rms_bolu_gurultu']:.1f}")
    for ds in ("CIFAR-10", "CIFAR-100"):
        for o in ("oran", "logit", "h"):
            x = sonuc["mahmood2021"][ds][o]
            print(f"mahmood {ds} {o}: G={x['G_potansiyel_payi']:.3f} dolasim={x['dolasim_rms']:.3f} gurultu={x['dolasim_binom_gurultu_rms']:.3f}")


if __name__ == "__main__":
    main()
