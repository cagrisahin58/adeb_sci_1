#!/usr/bin/env python3
"""Konsey sentezi masa cozumlemesi (29.10.2026). Yeni olcum yok, GPU yok.

Girdi: mevcut ornek bazli npz dosyalari (results/c1_c3/pair{1,2,3}, results/q1/son_kontrol_noktasi/pair{1,2,3},
results/q1/cifar100/transfer/pair{1,2,3}, results/q1/havuz_cifar10).
Cikti: results/q1/konsey_sentez_r_tau_masa.json

Nicelikler (hedef-dogru protokol, T_ij = kaynak i -> hedef j kosullu yaniltma orani, w_i = T_ii beyaz kutu):
  yonlu artik r_ij = log(T_ij/T_ji) - log(w_j/w_i)      (i CNN, j ViT ise r>0: ViT yonlu olarak zayif kaynak)
  simetrik verim log tau_ij = 0.5*[log(T_ij*T_ji) - log(w_i*w_j)]
  potansiyel payi = log(w_j/w_i) / log(T_ij/T_ji)
Bolunmus yari: w cift indeksli goruntulerden, T tek indeksli goruntulerden (ve tersi), iki yarinin ortalamasi.
"""
import io
import json
import os
import sys

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CIKTI = os.path.join(KOK, "results", "q1", "konsey_sentez_r_tau_masa.json")
R, V = "ResNet18_AT", "ViT_Tiny_AT"


def yukle(klasor, s, t):
    z = np.load(os.path.join(KOK, klasor, f"per_sample_{s}_to_{t}.npz"))
    return z["target_clean_correct"].astype(bool), z["target_adv_wrong"].astype(bool)


def oran(tc, aw, maske=None):
    m = tc if maske is None else (tc & maske)
    return 100.0 * aw[m].mean()


def nicelikler(klasor, i, j, maske_w=None, maske_T=None):
    w_i = oran(*yukle(klasor, i, i), maske_w)
    w_j = oran(*yukle(klasor, j, j), maske_w)
    T_ij = oran(*yukle(klasor, i, j), maske_T)
    T_ji = oran(*yukle(klasor, j, i), maske_T)
    L = np.log(T_ij / T_ji)
    P = np.log(w_j / w_i)
    return {"T_ij": T_ij, "T_ji": T_ji, "w_i": w_i, "w_j": w_j, "asimetri_puan": T_ij - T_ji,
            "log_oran": L, "log_w_potansiyel": P, "r": L - P,
            "log_tau": 0.5 * (np.log(T_ij * T_ji) - np.log(w_i * w_j)),
            "potansiyel_payi": P / L if abs(L) > 1e-9 else None}


def bolunmus(klasor, i, j, n=10000):
    idx = np.arange(n)
    A, B = (idx % 2 == 0), (idx % 2 == 1)
    q1 = nicelikler(klasor, i, j, A, B)
    q2 = nicelikler(klasor, i, j, B, A)
    return {k: 0.5 * (q1[k] + q2[k]) for k in ("r", "log_tau", "log_w_potansiyel", "log_oran")}


def bootstrap_r(klasor, i, j, B=300, tohum=0):
    rng = np.random.default_rng(tohum)
    d = {(a, b): yukle(klasor, a, b) for a in (i, j) for b in (i, j)}
    n = len(d[(i, i)][0])
    rs, ts = [], []
    for _ in range(B):
        ix = rng.integers(0, n, n)
        def o(a, b):
            tc, aw = d[(a, b)]
            tc, aw = tc[ix], aw[ix]
            return 100.0 * aw[tc].mean()
        wi, wj, Tij, Tji = o(i, i), o(j, j), o(i, j), o(j, i)
        rs.append(np.log(Tij / Tji) - np.log(wj / wi))
        ts.append(0.5 * (np.log(Tij * Tji) - np.log(wi * wj)))
    return {"r_sd": float(np.std(rs, ddof=1)), "log_tau_sd": float(np.std(ts, ddof=1)), "B": B}


def f(x):
    if isinstance(x, dict):
        return {k: f(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [f(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return float(x)
    return x


def ozet(liste, anahtar):
    a = np.array([q[anahtar] for q in liste], dtype=float)
    return {"degerler": a.tolist(), "ort": float(a.mean()), "sd_kosum": float(a.std(ddof=1)) if len(a) > 1 else None}


sonuc = {"betik": "raporlar/konsey_2026-10-29/_sentez_r_tau_masa.py",
         "tanim": __doc__.strip().splitlines()[0], "kumeler": {}}

kumeler = {
    "c10_c1_secilen": "results/c1_c3/pair{}",
    "c10_son_kontrol_noktasi": "results/q1/son_kontrol_noktasi/pair{}",
    "c100_c1_secilen": "results/q1/cifar100/transfer/pair{}",
}
for ad, sablon in kumeler.items():
    tam, yari = [], []
    for p in (1, 2, 3):
        kl = sablon.format(p)
        tam.append(nicelikler(kl, R, V))
        yari.append(bolunmus(kl, R, V))
    kayit = {"tam_orneklem": {k: ozet(tam, k) for k in ("asimetri_puan", "log_oran", "log_w_potansiyel", "r", "log_tau", "potansiyel_payi")},
             "bolunmus_yari": {k: ozet(yari, k) for k in ("r", "log_tau", "log_w_potansiyel", "log_oran")},
             "goruntu_bootstrap_pair1": bootstrap_r(sablon.format(1), R, V)}
    sonuc["kumeler"][ad] = kayit

# Havuz: ViT ve ResNet icin sabit CNN paneline karsi model duzeyi r ve log tau
H = "results/q1/havuz_cifar10"
panel = ["Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10", "Gowal2020_WRN28_10"]
hv = {}
for m in (V, R, "Debenedetti2022_XCiT_S12"):
    satir = {c: nicelikler(H, c, m) for c in panel}
    hv[m] = {"panel": panel,
             "r_uyeler (CNN->m yonunde)": {c: satir[c]["r"] for c in panel},
             "r_ort": float(np.mean([satir[c]["r"] for c in panel])),
             "log_tau_uyeler": {c: satir[c]["log_tau"] for c in panel},
             "log_tau_ort": float(np.mean([satir[c]["log_tau"] for c in panel]))}
# panel ici log tau (CNN-CNN), karsilastirma tabani
ic = []
for a in range(len(panel)):
    for b in range(a + 1, len(panel)):
        ic.append(nicelikler(H, panel[a], panel[b])["log_tau"])
hv["panel_ici_log_tau"] = {"degerler": ic, "ort": float(np.mean(ic))}
hv["ResNet18_ViT_cifti"] = nicelikler(H, R, V)
# Kaynak acigi ayristirmasi: panel ortalamasinda log T(R->c) - log T(V->c)
# log T_mc = log w_c + log tau_mc(simetrik) - 0.5 * r_cm   (r_cm = log(T_cm/T_mc) - log(w_m/w_c))
def kaynak_logT(m):
    return float(np.mean([np.log(nicelikler(H, m, c)["T_ij"]) for c in panel]))
def hedef_logT(m):
    return float(np.mean([np.log(nicelikler(H, c, m)["T_ij"]) for c in panel]))
dk = kaynak_logT(R) - kaynak_logT(V)
sim = hv[R]["log_tau_ort"] - hv[V]["log_tau_ort"]
yon = -0.5 * (hv[R]["r_ort"] - hv[V]["r_ort"])
dh = hedef_logT(V) - hedef_logT(R)
pot = float(np.log(nicelikler(H, V, V)["w_i"]) - np.log(nicelikler(H, R, R)["w_i"]))
hv["kaynak_acigi_ayristirma_log"] = {
    "tanim": "panel ortalamasi log T(R->c) - log T(V->c) = simetrik (log tau_R - log tau_V) + yonlu (-0.5*(r_R - r_V))",
    "toplam": dk, "simetrik_pay": sim, "yonlu_pay": yon, "kontrol_artik": dk - sim - yon,
    "simetrik_oran": sim / dk}
hv["hedef_farki_ayristirma_log"] = {
    "tanim": "panel ortalamasi log T(c->V) - log T(c->R) = potansiyel (log w_V - log w_R) + simetrik (log tau_V - log tau_R) + yonlu (0.5*(r_V - r_R))",
    "toplam": dh, "potansiyel_pay": pot, "simetrik_pay": -sim, "yonlu_pay": 0.5 * (hv[V]["r_ort"] - hv[R]["r_ort"]),
    "kontrol_artik": dh - pot + sim - 0.5 * (hv[V]["r_ort"] - hv[R]["r_ort"])}
sonuc["havuz_tohum1"] = hv

# Onceden kesinlik plani girdisi: kosum duzeyi SD (C1 secilen, CIFAR-10) ile n=2'ye n=2 ve n=2'ye n=3 karsitliklarinda
# %90 aralik yari genisligi (t_0.95, df=5). Bu post-hoc guc hesabi degildir; deney oncesi kesinlik planidir.
t95_df5 = 2.015
s_r = sonuc["kumeler"]["c10_c1_secilen"]["tam_orneklem"]["r"]["sd_kosum"]
s_t = sonuc["kumeler"]["c10_c1_secilen"]["tam_orneklem"]["log_tau"]["sd_kosum"]
sonuc["kesinlik_plani"] = {
    "kaynak": "c10_c1_secilen kosum SD (3 tohum, cift duzeyi)",
    "t_0.95_df5": t95_df5,
    "r_sd": s_r, "log_tau_sd": s_t,
    "yari_genislik_r_2e2": t95_df5 * s_r * np.sqrt(1 / 2 + 1 / 2),
    "yari_genislik_r_2e3": t95_df5 * s_r * np.sqrt(1 / 2 + 1 / 3),
    "yari_genislik_logtau_2e2": t95_df5 * s_t * np.sqrt(1 / 2 + 1 / 2),
    "yari_genislik_logtau_2e3": t95_df5 * s_t * np.sqrt(1 / 2 + 1 / 3),
}

sonuc = f(sonuc)
with io.open(CIKTI, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(sonuc, fh, ensure_ascii=False, indent=1)
print(json.dumps(sonuc, ensure_ascii=False, indent=1)[:6000])
