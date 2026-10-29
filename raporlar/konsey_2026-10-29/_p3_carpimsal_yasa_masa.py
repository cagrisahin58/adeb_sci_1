# -*- coding: utf-8 -*-
"""Konsey P3 masa testi 4 (29.10.2026): carpimsal "kirilganlik x benzerlik" yasasi.
Model: T_ij (hedef-dogru transfer orani, i kaynak, j hedef) = w_j * tau_ij, tau_ij = tau_ji.
w_j = hedefin kendi beyaz kutu kosullu yaniltma orani (PGD-10, hedef-dogru).
Sonuc 1 (serbest parametresiz): log(T_ij / T_ji) = log(w_j / w_i)  (egim lambda = 1).
Sonuc 2: tau_ij = T_ij / w_j simetrik olmali; aile bilgisi tau'da toplanir.
Veri: havuz (8x8), C1 3x3 (uc cift), CIFAR-100 3x3 (uc cift), A kolu yorungeleri.
Yeni olcum yok. Cikti: raporlar/konsey_2026-10-29/_p3_carpimsal_yasa_masa.json
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


def oku(y):
    return json.load(io.open(os.path.join(KOK, y), encoding="utf-8"))


def npz_oran(klasor, s, t):
    z = np.load(os.path.join(KOK, klasor, f"per_sample_{s}_to_{t}.npz"))
    tc = z["target_clean_correct"].astype(bool)
    aw = z["target_adv_wrong"].astype(bool)
    return 100.0 * aw[tc].mean()


def matris(klasor, mods):
    K = len(mods)
    T = np.zeros((K, K))
    for a, s in enumerate(mods):
        for b, t in enumerate(mods):
            T[a, b] = npz_oran(klasor, s, t)
    return T  # kosegen = beyaz kutu kosullu yaniltma w


def yasa(T, mods, aile=None):
    K = len(mods)
    w = np.diag(T).copy()
    L, X = [], []
    for a in range(K):
        for b in range(a + 1, K):
            L.append(np.log(T[a, b] / T[b, a]))
            X.append(np.log(w[b] / w[a]))
    L = np.array(L)
    X = np.array(X)
    lam = float((L @ X) / (X @ X))
    R2_lam = float(1 - ((L - lam * X) ** 2).sum() / (L ** 2).sum())
    R2_bir = float(1 - ((L - X) ** 2).sum() / (L ** 2).sum())  # lambda = 1 sabit, serbest parametre yok
    out = {"modeller": mods, "w_beyaz_kutu": {m: float(x) for m, x in zip(mods, w)},
           "lambda": lam, "R2_lambda_uydurma": R2_lam, "R2_lambda_1_sabit": R2_bir,
           "isaret": f"{int(np.sum(np.sign(L) == np.sign(X)))}/{len(L)}",
           "log_oran_artik_rms_lambda1": float(np.sqrt(((L - X) ** 2).mean()))}
    tau = T / w[None, :]
    asim_tau = []
    for a in range(K):
        for b in range(a + 1, K):
            asim_tau.append(np.log(tau[a, b] / tau[b, a]))
    out["log_tau_simetri_ihlali_rms"] = float(np.sqrt(np.mean(np.square(asim_tau))))
    if aile:
        ts = {}
        for a in range(K):
            for b in range(a + 1, K):
                g = "-".join(sorted([aile[mods[a]], aile[mods[b]]]))
                ts.setdefault(g, []).append(float(np.sqrt(tau[a, b] * tau[b, a])))
        out["tau_geometrik_simetrik_aile_gruplari"] = {g: {"n": len(v), "ort": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v))} for g, v in ts.items()}
        out["tau_ciftler"] = {f"{mods[a]}|{mods[b]}": float(np.sqrt(tau[a, b] * tau[b, a])) for a in range(K) for b in range(a + 1, K)}
    return out


def main():
    sonuc = {"uretildi_utc": datetime.now(timezone.utc).isoformat(),
             "betik": "raporlar/konsey_2026-10-29/_p3_carpimsal_yasa_masa.py"}
    hm = ["ResNet18_AT", "ViT_Tiny_AT", "Wong2020_PRN18", "Engstrom2019_RN50",
          "Carmon2019_WRN28_10", "Debenedetti2022_XCiT_S12", "Gowal2020_WRN28_10"]
    aile = {m: "CNN" for m in hm}
    aile["ViT_Tiny_AT"] = "ViT"
    aile["Debenedetti2022_XCiT_S12"] = "XCiT"
    T = matris("results/q1/havuz_cifar10", hm)
    sonuc["havuz_AT7"] = yasa(T, hm, aile)
    uc = ["ResNet18_AT", "ViT_Tiny_AT", "WRN_28_10"]
    for ad, kl in (("c10", "results/c1_c3/pair{}"), ("c100", "results/q1/cifar100/transfer/pair{}")):
        sonuc[f"{ad}_3x3"] = {}
        for k in (1, 2, 3):
            sonuc[f"{ad}_3x3"][f"pair{k}"] = yasa(matris(kl.format(k), uc), uc)
    # A kolu: hareketli kontrol noktasi w'si egriden, es model w'si ozetten; tc oranlari kayittan
    yk = oku("raporlar/konsey_2026-10-29/_p3_yorunge_gurbuzluk_masa.json")["kayitlar"]
    L, X = [], []
    satir = []
    for k in yk:
        d = oku(k["dosya"])
        # makale yonu: CNN->ViT ve ViT->CNN hedef-dogru oranlari
        if k["hareketli"] == "resnet18":
            t_cv = d["oranlar_geri"]["target_correct"]   # resnet@ep -> vit
            t_vc = d["oranlar_ileri"]["target_correct"]  # vit -> resnet@ep
        else:
            t_cv = d["oranlar_ileri"]["target_correct"]  # resnet -> vit@ep
            t_vc = d["oranlar_geri"]["target_correct"]   # vit@ep -> resnet
        l = np.log(t_cv / t_vc)
        x = np.log(k["w_vit"] / k["w_cnn"])
        L.append(l)
        X.append(x)
        satir.append({"yorunge": k["yorunge"], "epok": k["epok"], "log_oran": float(l), "log_w_orani": float(x)})
    L = np.array(L)
    X = np.array(X)
    lam = float((L @ X) / (X @ X))
    b1, b0 = np.polyfit(X, L, 1)
    sonuc["A_kolu"] = {"n": len(L), "lambda_kesisimsiz": lam,
                       "R2_lambda_1": float(1 - ((L - X) ** 2).sum() / ((L - L.mean()) ** 2).sum()),
                       "egim_kesisimli": float(b1), "kesisim": float(b0),
                       "pearson_r": float(np.corrcoef(X, L)[0, 1]),
                       "isaret": f"{int(np.sum(np.sign(L) == np.sign(X)))}/{len(L)}",
                       "veri_ayrimi": {}}
    for ds in ("cifar10", "cifar100"):
        ix = [i for i, k in enumerate(yk) if k["veri"] == ds]
        l, x = L[ix], X[ix]
        bb1, bb0 = np.polyfit(x, l, 1)
        sonuc["A_kolu"]["veri_ayrimi"][ds] = {"n": len(ix), "egim": float(bb1), "kesisim": float(bb0),
                                              "pearson_r": float(np.corrcoef(x, l)[0, 1]),
                                              "isaret": f"{int(np.sum(np.sign(l) == np.sign(x)))}/{len(ix)}"}
    sonuc["A_kolu"]["noktalar"] = satir
    with io.open(os.path.join(KOK, "raporlar", "konsey_2026-10-29", "_p3_carpimsal_yasa_masa.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(sonuc, f, ensure_ascii=False, indent=1)
    h = sonuc["havuz_AT7"]
    print("havuz AT7: lambda=%.3f R2(lam)=%.3f R2(lam=1)=%.3f isaret=%s tau simetri ihlali rms=%.3f" % (
        h["lambda"], h["R2_lambda_uydurma"], h["R2_lambda_1_sabit"], h["isaret"], h["log_tau_simetri_ihlali_rms"]))
    print(" tau aile:", json.dumps(h["tau_geometrik_simetrik_aile_gruplari"]))
    print(" tau ciftler:", {k: round(v, 3) for k, v in h["tau_ciftler"].items()})
    for ad in ("c10_3x3", "c100_3x3"):
        for p, v in sonuc[ad].items():
            print(ad, p, "lambda=%.3f R2(lam=1)=%.3f isaret=%s" % (v["lambda"], v["R2_lambda_1_sabit"], v["isaret"]), {m[:6]: round(x, 2) for m, x in v["w_beyaz_kutu"].items()})
    a = sonuc["A_kolu"]
    print("A kolu: n=%d lambda=%.3f egim=%.3f kesisim=%.3f r=%.3f isaret=%s R2(lam=1)=%.3f" % (
        a["n"], a["lambda_kesisimsiz"], a["egim_kesisimli"], a["kesisim"], a["pearson_r"], a["isaret"], a["R2_lambda_1"]))
    print(" ", json.dumps(a["veri_ayrimi"]))


if __name__ == "__main__":
    main()
