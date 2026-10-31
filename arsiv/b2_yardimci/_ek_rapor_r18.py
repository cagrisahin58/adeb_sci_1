"""Salt okur (konteyner, numpy): ImageNetV2 kosinus.npz icinde IN_Salman2020Do_R18 ile diger modellerin
goruntu basina kosinus dagilimi. Hicbir dosya yazmaz."""
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
z = np.load("results/q1/konsey_b10_gradyan/imagenetv2/kosinus.npz")
mod = [str(x) for x in z["modeller"]]
cos = z["cos"].astype(np.float64)
cf = z["ciftler"]
norm = z["norm"].astype(np.float64)
for a, b in [("IN_Salman2020Do_R18", "IN_Salman2020Do_R50"), ("IN_Salman2020Do_R18", "IN_Engstrom2019Robustness"),
             ("IN_Salman2020Do_R50", "IN_Engstrom2019Robustness"), ("IN_Salman2020Do_R18", "IN_Salman2020Do_50_2"),
             ("IN_Salman2020Do_R50", "IN_Salman2020Do_50_2")]:
    i, j = mod.index(a), mod.index(b)
    k = [t for t in range(len(cf)) if set(cf[t]) == {i, j}][0]
    v = cos[:, k]
    print(f"{a}|{b}: ort={v.mean():.4f} medyan={np.median(v):.4f} sd={v.std():.4f} negatif_oran={(v < 0).mean():.3f} "
          f"|v|<0.02 oran={(np.abs(v) < 0.02).mean():.3f}")
for m in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50", "IN_Engstrom2019Robustness"]:
    i = mod.index(m)
    print(f"{m}: gradyan normu medyan={np.median(norm[i]):.4g} sifir_norm={(norm[i] == 0).sum()}")
