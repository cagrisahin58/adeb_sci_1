# -*- coding: utf-8 -*-
"""B10 ImageNetV2 kayitli ciktisini okur (salt okur): R18-R50 cifti ve denetim ciftleri."""
import json
import sys

import numpy as np

D = "results/q1/konsey_b10_gradyan/imagenetv2/"
o = json.load(open(D + "kosinus_ozet.json"))
print({k: v for k, v in o.items() if k not in ("c_tum", "c_iki_model_dogru", "n_iki_model_dogru", "log_gradyan_normu_ort", "temiz_dogruluk_yuzde")})
names = o["modeller"]
np.set_printoptions(precision=3, linewidth=250, suppress=True)
C = np.array(o["c_tum"])
for i, n in enumerate(names):
    print(f"{i:2d} {n:32s} acc={o['temiz_dogruluk_yuzde'][n]:6.2f} loggn={o['log_gradyan_normu_ort'][n]:8.3f} ", C[i])
z = np.load(D + "kosinus.npz")
print({k: z[k].shape for k in z.files})
print("modeller npz:", list(z["modeller"]))
ciftler = [tuple(int(v) for v in c) for c in z["ciftler"]]
cos = z["cos"].astype(np.float64)
norm = z["norm"]
ok = z["temiz_dogru"]
def p(a, b):
    i, j = names.index(a), names.index(b)
    return ciftler.index((min(i, j), max(i, j)))
for a, b in [("IN_Salman2020Do_R18", "IN_Salman2020Do_R50"), ("IN_Salman2020Do_R18", "IN_Salman2020Do_50_2"),
             ("IN_Salman2020Do_R50", "IN_Engstrom2019Robustness"), ("IN_Singh_ConvNeXt-T-CvSt", "IN_Singh_ConvNeXt-B-CvSt")]:
    k = p(a, b)
    v = cos[:, k]
    print(a, b, "pair idx", k, "mean2000=%.5f sd=%.5f mean100=%.5f sd100=%.5f maxabs=%.4f" % (np.nanmean(v), np.nanstd(v), np.nanmean(v[:100]), np.nanstd(v[:100]), np.nanmax(np.abs(v))))
    print("  ilk 10:", np.round(v[:10], 4))
for n in ["IN_Salman2020Do_R18", "IN_Salman2020Do_R50"]:
    k = names.index(n)
    print(n, "norm ilk100 ort=%.4g medyan=%.4g; acc100=%.2f acc2000=%.2f" % (norm[k, :100].mean(), np.median(norm[k, :100]), 100 * ok[k, :100].mean(), 100 * ok[k].mean()))
json.dump({"names": names, "ciftler": ciftler}, open(sys.argv[1], "w"))
np.save(sys.argv[1].replace(".json", "_cos100.npy"), cos[:100])
np.save(sys.argv[1].replace(".json", "_norm100.npy"), norm[:, :100])
np.save(sys.argv[1].replace(".json", "_ok100.npy"), ok[:, :100])
