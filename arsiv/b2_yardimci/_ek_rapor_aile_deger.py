"""Salt okur (konteynerde, numpy): aile eslesmesi ayiklamasinin iki yontemle karsilastirilmasi (31.10.2026 dogrulama turu).
(a) sira olceginde: ana etki artiklarinin siralari cift turu gostergesine gore ayiklanir (rapordaki yontem);
(b) deger olceginde: ana etki artiklari cift turu gostergesine gore ayiklanir, sonra Spearman alinir;
(c) deger olceginde: cift turu ana etki modeline eklenir, artiklardan Spearman alinir.
Depo kokunden: docker exec -w /workspace adeb_eval python arsiv/b2_yardimci/_ek_rapor_aile_deger.py
"""
import json
import sys

import numpy as np

R = "results/q1/konsey_b10_gradyan/"
HT = {"cifar10": "raporlar/konsey_2026-10-29/hucre_tablosu.json",
      "cifar100": "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
      "imagenetv2": "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"}


# yardimci islevler _ek_rapor_b10_yeniden.py dosyasindan birebir kopyadir
def sira(x):
    o = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[o] = np.arange(len(x))
    # bag ortalamasi
    xs = x[o]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        if j > i:
            r[o[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = sira(a), sira(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def ust(M):
    K = M.shape[0]
    iu = np.triu_indices(K, 1)
    return M[iu], iu


def artik(M):
    K = M.shape[0]
    y, (ii, jj) = ust(M)
    X = np.zeros((len(y), K + 1))
    X[:, 0] = 1.0
    X[np.arange(len(y)), 1 + ii] = 1.0
    X[np.arange(len(y)), 1 + jj] = 1.0
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta



for d in ["cifar10", "cifar100", "imagenetv2"]:
    m = json.load(open(f"{R}mantel_{d}.json"))
    mod = m["modeller_ortak"]
    C = np.array(m["c_matrisi"], dtype=float)
    L = np.array(m["log_tau_matrisi"], dtype=float)
    ht = json.load(open(HT[d]))["modeller"]
    don = np.array([ht[x]["aile"] != "CNN" for x in mod])
    _, (ii, jj) = ust(C)
    K = C.shape[0]
    tur = np.where(don[ii] == don[jj], np.where(don[ii], 2, 0), 1)
    Z = np.column_stack([np.ones(len(tur)), tur == 1, tur == 2]).astype(float)
    ec, el = artik(C), artik(L)
    rc, rl = sira(ec), sira(el)
    a = float(np.corrcoef(rc - Z @ np.linalg.lstsq(Z, rc, rcond=None)[0], rl - Z @ np.linalg.lstsq(Z, rl, rcond=None)[0])[0, 1])
    b = spearman(ec - Z @ np.linalg.lstsq(Z, ec, rcond=None)[0], el - Z @ np.linalg.lstsq(Z, el, rcond=None)[0])
    X = np.zeros((len(tur), K + 3))
    X[:, 0] = 1.0
    X[np.arange(len(tur)), 1 + ii] = 1.0
    X[np.arange(len(tur)), 1 + jj] = 1.0
    X[:, K + 1] = tur == 1
    X[:, K + 2] = tur == 2
    yc, yl = ust(C)[0], ust(L)[0]
    c = spearman(yc - X @ np.linalg.lstsq(X, yc, rcond=None)[0], yl - X @ np.linalg.lstsq(X, yl, rcond=None)[0])
    print(f"{d}: (a) sira={a:.4f} (b) deger artik={b:.4f} (c) modele ekli={c:.4f}  fark a-b={a-b:+.4f} a-c={a-c:+.4f}")
