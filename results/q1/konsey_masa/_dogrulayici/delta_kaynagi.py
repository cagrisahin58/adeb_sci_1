# -*- coding: utf-8 -*-
"""delta = 0,10 gerekcesi: havuz AT7'de r_ij RMS'sinin hangi ciftlerden geldigi (bagimsiz hesap)."""
import io
import json
import math
import os
import sys
from itertools import combinations

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
H = "results/q1/havuz_cifar10"


def T(s, t):
    z = np.load(os.path.join(H, f"per_sample_{s}_to_{t}.npz"))
    tc, aw = z["target_clean_correct"].astype(bool), z["target_adv_wrong"].astype(bool)
    return 100.0 * np.count_nonzero(tc & aw) / np.count_nonzero(tc)


AT7 = ["ResNet18_AT", "ViT_Tiny_AT", "Wong2020_PRN18", "Engstrom2019_RN50", "Carmon2019_WRN28_10",
       "Debenedetti2022_XCiT_S12", "Gowal2020_WRN28_10"]
r = {}
for a, b in combinations(AT7, 2):
    r[(a, b)] = math.log(T(a, b) / T(b, a)) - math.log(T(b, b) / T(a, a))


def rms(sec):
    v = np.array([r[k] for k in sec])
    return float(np.sqrt(np.mean(v ** 2))), len(v)


hepsi = list(r)
vit = [k for k in r if "ViT_Tiny_AT" in k]
vit_disi = [k for k in r if "ViT_Tiny_AT" not in k]
cnn = [k for k in r if "ViT_Tiny_AT" not in k and "Debenedetti2022_XCiT_S12" not in k]
out = {"hepsi_21": rms(hepsi), "vit_li_6": rms(vit), "vit_disi_15": rms(vit_disi), "yalniz_cnn_10": rms(cnn),
       "r_vit_ciftleri": {f"{a}|{b}": r[(a, b)] for (a, b) in vit},
       "kaynak": "results/q1/havuz_cifar10 per_sample npz; karsilastirma: results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json havuz_AT7.log_tau_simetri_ihlali_rms"}
ref = json.load(open("results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json", encoding="utf-8"))["havuz_AT7"]["log_tau_simetri_ihlali_rms"]
out["referans_0_0897"] = ref
for k, v in out.items():
    print(k, v)
with io.open("results/q1/konsey_masa/_dogrulayici/delta_kaynagi.json", "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)
