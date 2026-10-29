# -*- coding: utf-8 -*-
"""Betigin istatistik yardimcilarini bagimsiz formullerle sinar ve karar kurallarinin
ON_KAYIT metniyle uyumunu ornek veriyle yoklar. SINAMA_SONUC_DEGIL: sayilar sentetiktir."""
import io
import json
import sys

import numpy as np
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "/workspace")
sys.path.insert(0, "/workspace/experiments")
import q1_konsey_ayrisim as A  # noqa: E402

out = {"SINAMA_SONUC_DEGIL": True}
rng = np.random.default_rng(7)

# 1) Holm: bagimsiz uygulama
def holm_ref(p):
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); adj = np.empty(m); run = 0
    for k, i in enumerate(o):
        run = max(run, (m - k) * p[i]); adj[i] = min(1, run)
    return adj
mx = 0
for _ in range(2000):
    p = rng.uniform(0, 0.2, rng.integers(1, 5))
    mx = max(mx, float(np.max(np.abs(np.array(A.holm(p)) - holm_ref(p)))))
out["holm_en_buyuk_fark"] = mx

# 2) Birlesik varyans karsitligi (3,2,2,2), elle formul
mxk = 0
for _ in range(500):
    d = {"V-scr": rng.normal(0, 1, 3).tolist(), "V-IN": rng.normal(0, 1, 2).tolist(),
         "R224-scr": rng.normal(0, 1, 2).tolist(), "R224-IN": rng.normal(0, 1, 2).tolist()}
    for K in (A.K_H1, A.K_H2, A.K_H3):
        k = A.karsitlik(d, K, A.HUC4)
        ss = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in d.values())
        sp = np.sqrt(ss / 5)
        est = sum(c * np.mean(d[h]) for h, c in K.items())
        se = sp * np.sqrt(sum(c * c / len(d[h]) for h, c in K.items()))
        q = stats.t.ppf(0.95, 5)
        mxk = max(mxk, abs(k["kestirim"] - est), abs(k["se"] - se), abs(k["ci90"][0] - (est - q * se)),
                  abs(k["p_tek_kucuk"] - stats.t.cdf(est / se, 5)))
out["karsitlik_en_buyuk_fark"] = float(mxk)
out["etkilesim_carpani"] = A.karsitlik({"V-scr": [0, 1, 2], "V-IN": [0, 1], "R224-scr": [0, 1], "R224-IN": [0, 1]}, A.K_H2, A.HUC4)["carpan"]

# 3) TOST: p<0,05 <=> %90 aralik (-0,1;0,1) icinde
uyum = 0; N = 0
for _ in range(5000):
    est, se, df = rng.normal(0, 0.08), abs(rng.normal(0.03, 0.02)) + 1e-4, int(rng.integers(1, 8))
    p, _, _ = A.tost_p(est, se, df)
    q = stats.t.ppf(0.95, df)
    ici = (est - q * se > -0.1) and (est + q * se < 0.1)
    uyum += int((p < 0.05) == ici); N += 1
out["tost_aralik_denkligi"] = f"{uyum}/{N}"

# 4) H1 destek ve curutme olcutlerinin ortusmesi (ON_KAYIT satir 60): sentetik sigma degerleri
sig = {"V-scr": [-0.80, -0.81, -0.79], "R224-scr": [-0.74, -0.745], "V-IN": [-0.70, -0.705], "R224-IN": [-0.60, -0.605]}
rho = {h: [0.0 + 0.001 * i for i in range(len(v))] for h, v in sig.items()}
k = A.b4_karsitliklar(sig, rho)
kL = A.b4_karsitliklar(sig, rho)
pler = [k["H1"]["p_tek_kucuk"], k["H2"]["p_iki"], k["H3"]["tost_p"]]
adj = A.holm(pler)
kr = A.b4_karar(k, kL, adj)
out["H1_ortusme_ornegi"] = {"A_sigma_scr": k["H1"]["kestirim"], "ci90": k["H1"]["ci90"], "p_holm": adj[0],
                           "karar": kr["H1"], "H1_esdeger": kr["H1_esdeger"], "sonuc_bolgesi": kr["sonuc_bolgesi"],
                           "yorum": "Holm p<0,05 (ON_KAYIT destek) ve %90 aralik (-0,10;0,10) icinde (ON_KAYIT curutme) ayni anda"}
# 5) H2 icin ayni ortusme
sig2 = {"V-scr": [-0.80, -0.805, -0.795], "R224-scr": [-0.60, -0.601], "V-IN": [-0.65, -0.651], "R224-IN": [-0.50, -0.501]}
k2 = A.b4_karsitliklar(sig2, rho)
adj2 = A.holm([k2["H1"]["p_tek_kucuk"], k2["H2"]["p_iki"], k2["H3"]["tost_p"]])
kr2 = A.b4_karar(k2, k2, adj2)
out["H2_ortusme_ornegi"] = {"I_sigma": k2["H2"]["kestirim"], "ci90": k2["H2"]["ci90"], "p_holm": adj2[1],
                           "karar": kr2["H2"], "H2_esdeger": kr2["H2_esdeger"], "sonuc_bolgesi": kr2["sonuc_bolgesi"]}
for a, b in out.items():
    print(a, b)
with io.open("/workspace/results/q1/konsey_masa/_dogrulayici/istatistik_sinama.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump(A.jsonla(out), fh, ensure_ascii=False, indent=1)
