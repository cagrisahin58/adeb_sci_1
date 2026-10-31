"""11_sonuc_b8_b10 raporu icin salt okur yardimci (konteynerde, numpy ile). Hicbir dosya yazmaz.
1) Mantel ciktilarindaki c_matrisi ve log_tau_matrisi'nden ham Spearman ve ana etki artikli Spearman'i
   bagimsiz olarak yeniden hesaplar (ek on kayit §6.2 tanimi) ve dosyadaki istatistikle karsilastirir.
2) KESIFSEL: iki modelin de temiz dogru oldugu goruntulerle sinirli c (kosinus_ozet.c_iki_model_dogru) ile ayni
   iki istatistik ve 9999 permutasyonlu tek yonlu p (tohum 20261030; ek §6.2'deki duyarlilik, Mantel ciktisinda yok).
3) KESIFSEL S10-2: C1 ciftlerinde gamma(ViT) - gamma(ResNet), gamma_m = ort_{c in P} c_mc (P birincil panel).
Depo kokunden: docker exec -w /workspace adeb_eval python arsiv/b2_yardimci/_ek_rapor_b10_yeniden.py
"""
import json
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
R = "results/q1/konsey_b10_gradyan/"
HT = {"cifar10": "raporlar/konsey_2026-10-29/hucre_tablosu.json",
      "cifar100": "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
      "imagenetv2": "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"}


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


def mantel_p(C, L, fn, perm=9999, tohum=20261030):
    rng = np.random.default_rng(tohum)
    gozlenen = fn(C, L)
    K = C.shape[0]
    say = 0
    for _ in range(perm):
        p = rng.permutation(K)
        if fn(C[np.ix_(p, p)], L) >= gozlenen:
            say += 1
    return gozlenen, (1 + say) / (perm + 1)


def ham(C, L):
    return spearman(ust(C)[0], ust(L)[0])


def kismi(C, L):
    return spearman(artik(C), artik(L))


for d in ["cifar10", "cifar100", "imagenetv2"]:
    m = json.load(open(f"{R}mantel_{d}.json"))
    k = json.load(open(f"{R}{d}/kosinus_ozet.json"))
    mod = m["modeller_ortak"]
    C = np.array(m["c_matrisi"], dtype=float)
    L = np.array(m["log_tau_matrisi"], dtype=float)
    print(f"\n== {d}: K={len(mod)}")
    print(f"  ham yeniden={ham(C, L):.6f} dosya={m['sinamalar']['ham']['istatistik']:.6f}")
    print(f"  ana_etki_artik yeniden={kismi(C, L):.6f} dosya={m['sinamalar']['ana_etki_artik']['istatistik']:.6f}")
    # c_tum ile mantel c_matrisi ayni mi (sira eslemesiyle)
    km = k["modeller"]
    idx = [km.index(x) for x in mod]
    Ct = np.array(k["c_tum"], dtype=float)[np.ix_(idx, idx)]
    print(f"  c_matrisi == kosinus_ozet.c_tum (sira eslemeli): max fark {np.abs(Ct - C).max():.2e}")
    Ci = np.array(k["c_iki_model_dogru"], dtype=float)[np.ix_(idx, idx)]
    g1, p1 = mantel_p(Ci, L, ham)
    g2, p2 = mantel_p(Ci, L, kismi)
    print(f"  KESIFSEL c_iki_model_dogru: ham={g1:.4f} p={p1:.4f}; ana_etki_artik={g2:.4f} p={p2:.4f}")
    # S10-2
    ht = json.load(open(HT[d]))["modeller"]
    P = [x for x in mod if ht.get(x, {}).get("birincil_panel")]
    print(f"  birincil panel ({len(P)}): {P}")
    gam = {x: float(np.mean([C[mod.index(x), mod.index(p)] for p in P if p != x])) for x in mod}
    if d in ("cifar10", "cifar100"):
        on = "" if d == "cifar10" else "C100_"
        for s in range(1, 4):
            rr, vv = f"{on}ResNet18_AT_s100{s}", f"{on}ViT_Tiny_AT_s200{s}"
            print(f"  S10-2 cift {s}: gamma(ViT)={gam[vv]:.4f} gamma(ResNet)={gam[rr]:.4f} fark={gam[vv] - gam[rr]:+.4f}")
    else:
        for c, v in [("IN_Singh_ConvNeXt-T-CvSt", "IN_Singh_ViT-S-CvSt"), ("IN_Singh_ConvNeXt-B-CvSt", "IN_Singh_ViT-B-CvSt"),
                     ("IN_Liu_ConvNeXt-B", "IN_Liu_Swin-B")]:
            print(f"  S10-2 benzeri {v} - {c}: {gam[v]:.4f} - {gam[c]:.4f} = {gam[v] - gam[c]:+.4f}")

# 4) KESIFSEL: ImageNetV2'de IN_Salman2020Do_R18 ya da IN_Salman2020Do_R50 cikarilinca ham ve artik Spearman
#    (c(R18, R50) = 0,0034 aykiri cifti icin duyarlilik; permutasyonsuz, yalniz nokta kestirimi).
m = json.load(open(f"{R}mantel_imagenetv2.json"))
mod = m["modeller_ortak"]
C = np.array(m["c_matrisi"], dtype=float)
L = np.array(m["log_tau_matrisi"], dtype=float)
for cik in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50"]:
    kal = [i for i, x in enumerate(mod) if x != cik]
    Cs, Ls = C[np.ix_(kal, kal)], L[np.ix_(kal, kal)]
    print(f"\nKESIFSEL imagenetv2 {cik} cikarilinca (K={len(kal)}): ham={ham(Cs, Ls):.4f} ana_etki_artik={kismi(Cs, Ls):.4f}")

# 5) KESIFSEL (S10-3'e yakin, on kayitta kodu yazilmamis): ana etki artiklarinda aile eslesmesi
#    (CNN-CNN, donusturucu-donusturucu, karma) etkisi ayiklaninca kalan Spearman ve yalniz CNN-CNN ciftlerinde
#    artik Spearman. Permutasyonsuz, nokta kestirimi; aile hucre tablosunun "aile" alanindan (CNN / digerleri).
print("\n==== KESIFSEL aile eslesmesi")
for d in ["cifar10", "cifar100", "imagenetv2"]:
    m = json.load(open(f"{R}mantel_{d}.json"))
    mod = m["modeller_ortak"]
    C = np.array(m["c_matrisi"], dtype=float)
    L = np.array(m["log_tau_matrisi"], dtype=float)
    ht = json.load(open(HT[d]))["modeller"]
    don = np.array([ht[x]["aile"] != "CNN" for x in mod])
    _, (ii, jj) = ust(C)
    tur = np.where(don[ii] == don[jj], np.where(don[ii], 2, 0), 1)  # 0 CNN-CNN, 1 karma, 2 DON-DON
    ec, el = artik(C), artik(L)
    rc, rl = sira(ec), sira(el)
    Z = np.column_stack([np.ones(len(tur)), tur == 1, tur == 2]).astype(float)
    kc = rc - Z @ np.linalg.lstsq(Z, rc, rcond=None)[0]
    kl = rl - Z @ np.linalg.lstsq(Z, rl, rcond=None)[0]
    kis = float(np.corrcoef(kc, kl)[0, 1])
    cc = tur == 0
    print(f"  {d}: artik Spearman aile ayiklanmis={kis:.4f}; yalniz CNN-CNN ({cc.sum()} cift) artik Spearman={spearman(ec[cc], el[cc]):.4f}; "
          f"ham Spearman yalniz CNN-CNN={spearman(ust(C)[0][cc], ust(L)[0][cc]):.4f}")
