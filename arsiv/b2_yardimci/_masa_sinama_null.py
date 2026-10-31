# -*- coding: utf-8 -*-
"""Kod sinamasi (31.10.2026; yapay veri, sonuc degil): experiments/q1_ek_masa.py Mantel yardimcilari
(1) gradyan betiginin mantel()/ana_etki_artik() islevleriyle ayni sayilari veriyor mu,
(2) bagimsiz yapay matrislerde p dagilimi kabaca tekduze mi, (3) kisitli permutasyon gruplari koruyor mu."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]


def mod(ad, yol):
    s = importlib.util.spec_from_file_location(ad, KOK / yol)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


E = mod("q1_ek_masa", "experiments/q1_ek_masa.py")
G = mod("q1_ek_gradyan_kosinus", "experiments/q1_ek_gradyan_kosinus.py")
rng = np.random.default_rng(7)
K = 11
gr = ["CNN"] * 7 + ["donusturucu"] * 4
fark = []
for t in range(5):
    A = rng.normal(size=(K, K)); A = (A + A.T) / 2
    Bm = 0.5 * A + rng.normal(size=(K, K)); Bm = (Bm + Bm.T) / 2
    yB = E.ust(Bm)
    g_ham = G.mantel(A, Bm, None, 199)
    e_ham = E.permutasyon(lambda p: E.spearman(E.ust(A[np.ix_(p, p)]), yB), K, 199, G.TOHUM)
    RA, RB = G.ana_etki_artik(A), G.ana_etki_artik(Bm)
    g_aea = G.mantel(RA, RB, None, 199)
    EA = E.ana_etki_artik_matrisi(A)
    eB = E.artik_yapici(E.tasarim_ana_etki(K)) @ yB
    e_aea = E.permutasyon(lambda p: E.spearman(E.ust(EA[np.ix_(p, p)]), eB), K, 199, G.TOHUM)
    cc, tt, _ = E.aile_gostergeleri(gr)
    CCm, TTm = E.ciftten_matris(cc, K), E.ciftten_matris(tt, K)
    g_sira = G.mantel(RA, RB, [CCm, TTm], 199)
    Zs = np.column_stack([np.ones(len(cc)), __import__("scipy").stats.rankdata(cc), __import__("scipy").stats.rankdata(tt)])
    Rz = E.artik_yapici(Zs)
    ry = Rz @ __import__("scipy").stats.rankdata(E.ust(RB))
    e_sira = E.permutasyon(lambda p: E.pearson(Rz @ __import__("scipy").stats.rankdata(E.ust(EA[np.ix_(p, p)])), ry), K, 199, G.TOHUM)
    for g_, e_ in ((g_ham, e_ham), (g_aea, e_aea), (g_sira, e_sira)):
        fark.append(max(abs(g_[k] - e_[k]) for k in ("istatistik", "p_tek", "p_iki", "perm_ort", "perm_sd")))
print("gradyan betigi ile en buyuk fark (15 karsilastirma):", max(fark))
# bos hipotez altinda p dagilimi (bagimsiz matrisler), S10-3 istatistigi
ps = []
X1 = np.column_stack([E.tasarim_ana_etki(K), cc, tt]); R1 = E.artik_yapici(X1)
for t in range(200):
    A = rng.normal(size=(K, K)); A = (A + A.T) / 2
    Bm = rng.normal(size=(K, K)); Bm = (Bm + Bm.T) / 2
    EA1 = E.ciftten_matris(R1 @ E.ust(A), K); eB1 = R1 @ E.ust(Bm)
    ps.append(E.permutasyon(lambda p: E.spearman(E.ust(EA1[np.ix_(p, p)]), eB1), K, 99, t)["p_tek"])
ps = np.array(ps)
print("bos hipotez S10-3 p: ort %.3f, P(p<=0.05) %.3f, P(p<=0.20) %.3f" % (ps.mean(), (ps <= 0.05).mean(), (ps <= 0.2).mean()))
# kisitli permutasyon grup koruma
idx = [np.arange(7), np.arange(7, 11)]
ok = True
r = np.random.default_rng(1)
for _ in range(1000):
    p = np.arange(K)
    for gi in idx:
        p[gi] = gi[r.permutation(len(gi))]
    ok &= all(gr[p[k]] == gr[k] for k in range(K))
print("kisitli permutasyon gruplari koruyor:", ok)
