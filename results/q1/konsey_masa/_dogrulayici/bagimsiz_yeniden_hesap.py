# -*- coding: utf-8 -*-
"""Celisik dogrulayici (29.10.2026): ham npz'den bagimsiz yeniden hesap.

experiments/q1_konsey_ayrisim.py ve _sentez_r_tau_masa.py ICE AKTARILMAZ. Tanimlar ON_KAYIT_TASLAGI.md §2'den
dogrudan yazildi. Oranlar tamsayi sayimlardan kurulur:
  T_ij = 100 * #(hedef temiz dogru & hedef cekismeli yanlis) / #(hedef temiz dogru)
  bolunmus yari: yari A = 0-tabanli cift indeks, yari B = tek indeks; (w<-A, T<-B) ve (w<-B, T<-A) ortalamasi.
Cikti: results/q1/konsey_masa/_dogrulayici/bagimsiz_yeniden_hesap.json
"""
import io
import json
import math
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = "/workspace"
CIK = os.path.join(KOK, "results/q1/konsey_masa/_dogrulayici/bagimsiz_yeniden_hesap.json")
N = 10000
IDX = np.arange(N)
HALF = {"tam": np.ones(N, bool), "A": IDX % 2 == 0, "B": IDX % 2 == 1}


def oku(d, s, t):
    z = np.load(os.path.join(KOK, d, f"per_sample_{s}_to_{t}.npz"))
    return np.asarray(z["target_clean_correct"], bool), np.asarray(z["target_adv_wrong"], bool)


class Kume:
    def __init__(self, d):
        self.d = d
        self.c = {}

    def T(self, s, t, h="tam"):
        k = (s, t, h)
        if k not in self.c:
            tc, aw = oku(self.d, s, t)
            m = HALF[h]
            pay = int(np.count_nonzero(tc & aw & m))
            payda = int(np.count_nonzero(tc & m))
            self.c[k] = 100.0 * pay / payda
        return self.c[k]


def L(x):
    return math.log(x)


def logit(x):
    p = x / 100.0
    return math.log(p / (1.0 - p))


# Tek yapi icin (w yarisi hw, T yarisi hT) nicelikler, olcek fonksiyonu F
def r(K, i, j, hw, hT, F=L):
    # r_ij = F(T_ij) - F(T_ji) - [F(w_j) - F(w_i)]
    return (F(K.T(i, j, hT)) - F(K.T(j, i, hT))) - (F(K.T(j, j, hw)) - F(K.T(i, i, hw)))


def lt(K, i, j, hw, hT, F=L):
    # log tau_ij = 1/2 [F(T_ij) + F(T_ji) - F(w_i) - F(w_j)]
    return 0.5 * ((F(K.T(i, j, hT)) + F(K.T(j, i, hT))) - (F(K.T(i, i, hw)) + F(K.T(j, j, hw))))


YAP = {"tam": [("tam", "tam")], "yari": [("A", "B"), ("B", "A")]}


def yapi_ort(fn, kest):
    v = [fn(hw, hT) for hw, hT in YAP[kest]]
    return sum(v) / len(v)


def model(K, m, P, kest="tam", F=L):
    P = [c for c in P if c != m]
    sig = yapi_ort(lambda hw, hT: np.mean([lt(K, m, c, hw, hT, F) for c in P]), kest)
    rho = yapi_ort(lambda hw, hT: np.mean([r(K, c, m, hw, hT, F) for c in P]), kest)
    S = yapi_ort(lambda hw, hT: np.mean([F(K.T(m, c, hT)) for c in P]), kest)
    return {"sigma": float(sig), "rho": float(rho), "S": float(S), "omega_tam": F(K.T(m, m, "tam"))}


def ayrisim(K, R, V, P, kest="tam", F=L):
    a, b = model(K, R, P, kest, F), model(K, V, P, kest, F)
    D = a["S"] - b["S"]
    sim = a["sigma"] - b["sigma"]
    yon = -0.5 * (a["rho"] - b["rho"])
    return {"D": D, "simetrik_pay": sim, "yonlu_pay": yon, "ozdeslik_artik": D - sim - yon, "q": sim / D,
            "R": a, "V": b}


sonuc = {"betik": "results/q1/konsey_masa/_dogrulayici/bagimsiz_yeniden_hesap.py", "n": N}

# ---------------- Havuz ----------------
H = "results/q1/havuz_cifar10"
KH = Kume(H)
tm = json.load(open(os.path.join(KOK, H, "transfer_matrix.json"), encoding="utf-8"))
modeller = tm["models"]
# 1) transfer_matrix.json cond_fooling (deney betiginin kendi ozeti) ile npz'den kurulan T
fark = []
for s in modeller:
    for t in modeller:
        v = tm["results"][f"{s}->{t}"]["cond_fooling"]
        fark.append(abs(round(KH.T(s, t), 2) - v))
sonuc["havuz_T_transfer_matrix_json_ile_en_buyuk_fark"] = max(fark)
sonuc["havuz_hucre_sayisi"] = len(fark)

PANEL = ["Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Gowal2020_WRN28_10"]
R, V, X = "ResNet18_AT", "ViT_Tiny_AT", "Debenedetti2022_XCiT_S12"
hv = {"w": {m: KH.T(m, m) for m in modeller}}
for kest in ("tam", "yari"):
    for olc, F in (("log", L), ("logit", logit)):
        key = f"{kest}_{olc}"
        hv[key] = {m: model(KH, m, PANEL, kest, F) for m in (R, V, X)}
        hv[key]["ayrisim_R_eksi_V"] = ayrisim(KH, R, V, PANEL, kest, F)
# panel ici log tau (tam)
ic = [lt(KH, PANEL[a], PANEL[b], "tam", "tam") for a in range(4) for b in range(a + 1, 4)]
hv["panel_ici_log_tau_ort_tam"] = float(np.mean(ic))
# jackknife (yari, log): panel uyesi birakmali
jk = {}
for c in PANEL:
    Pj = [x for x in PANEL if x != c]
    a = ayrisim(KH, R, V, Pj, "yari")
    jk[c] = {"q": a["q"], "sigma_V": a["V"]["sigma"], "rho_V": a["V"]["rho"]}
hv["jackknife_yari_log"] = jk
# 04 tablo (1): her model m icin P \ {m, R} uzerinden D = S(R) - S(m)
AT7 = [R, V, "Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", X, "Gowal2020_WRN28_10"]
t1 = {}
for m in AT7:
    Pm = [c for c in PANEL if c not in (m, R)]
    d = {"sigma": model(KH, m, PANEL, "yari")["sigma"], "rho": model(KH, m, PANEL, "yari")["rho"],
         "w": KH.T(m, m)}
    if m != R:
        a = ayrisim(KH, R, m, Pm, "yari")
        d.update({"D": a["D"], "simetrik_pay": a["simetrik_pay"], "yonlu_pay": a["yonlu_pay"], "q": a["q"]})
    t1[m] = d
hv["tablo1_yari_log"] = t1
# ResNet-ViT cifti dogrudan
hv["RV_cifti_tam"] = {"r": r(KH, R, V, "tam", "tam"), "log_tau": lt(KH, R, V, "tam", "tam"),
                     "T_RV": KH.T(R, V), "T_VR": KH.T(V, R)}
sonuc["havuz"] = hv

# ---------------- C1 cift kumeleri ----------------
KUMELER = {"c10_c1_secilen": "results/c1_c3/pair{}", "c10_son_kontrol_noktasi": "results/q1/son_kontrol_noktasi/pair{}",
           "c100_c1_secilen": "results/q1/cifar100/transfer/pair{}"}
kk = {}
for ad, sab in KUMELER.items():
    rows = []
    for p in (1, 2, 3):
        K = Kume(sab.format(p))
        Lo = L(K.T(R, V)) - L(K.T(V, R))
        Po = L(K.T(V, V)) - L(K.T(R, R))
        yari_r = yapi_ort(lambda hw, hT: r(K, R, V, hw, hT), "yari")
        yari_t = yapi_ort(lambda hw, hT: lt(K, R, V, hw, hT), "yari")
        rows.append({"r_tam": r(K, R, V, "tam", "tam"), "log_tau_tam": lt(K, R, V, "tam", "tam"),
                     "pot_payi_tam": Po / Lo, "log_oran_tam": Lo, "r_yari": yari_r, "log_tau_yari": yari_t,
                     "w_R": K.T(R, R), "w_V": K.T(V, V)})
    o = {}
    for k in rows[0]:
        a = np.array([x[k] for x in rows])
        o[k] = {"degerler": a.tolist(), "ort": float(a.mean()), "sd": float(a.std(ddof=1))}
    kk[ad] = o
sonuc["kumeler"] = kk

with io.open(CIK, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(sonuc, fh, ensure_ascii=False, indent=1)
print("yazildi", CIK)
