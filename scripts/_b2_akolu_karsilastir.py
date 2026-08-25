#!/usr/bin/env python3
"""A kolu v1 (eski) ve v2 (B2 sonrasi) noktalarini kiyaslar.

IKI ETKI ayrilir:
  (1) TOHUMLAMA etkisi -- v2'nin GEVSEK degeri ile v1'in ayni degeri arasindaki
      fark. Tanim degismedi; degisen tek sey PGD random_start'inin artik
      kontrol noktasina bagli olmasi. Bu, eski sayilarin ne kadar tarama
      sirasina bagli oldugunun OLCUSUDUR.
  (2) TANIM etkisi -- v2 icinde SIKI ile GEVSEK arasindaki fark.
"""
import json
import re
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")
V1 = ROOT / "results/q1/e3_akolu"
V2 = ROOT / "results/q1/e3_akolu_v2"
P4 = ["raw", "target_correct", "both_correct", "successful_source"]

tohum_etkisi = {k: [] for k in P4}
tanim_etkisi = []
yayilim_v1, yayilim_v2 = [], []

for f2 in sorted(V2.glob("*.json")):
    f1 = V1 / f2.name
    if not f1.exists():
        continue
    a = json.loads(f1.read_text(encoding="utf-8"))
    b = json.loads(f2.read_text(encoding="utf-8"))
    # (1) tohumlama: TANIMDAN BAGIMSIZ uc protokol + gevsek varyant
    for k in ("raw", "target_correct", "both_correct"):
        tohum_etkisi[k].append(b["asimetri"][k] - a["asimetri"][k])
    tohum_etkisi["successful_source"].append(
        b["asimetri_gevsek_successful_source"] - a["asimetri"]["successful_source"])
    # (2) tanim
    tanim_etkisi.append(b["asimetri"]["successful_source"]
                        - b["asimetri_gevsek_successful_source"])
    yayilim_v1.append(a["y_asimetri_yayilimi"])
    yayilim_v2.append(b["y_asimetri_yayilimi"])

print(f"karsilastirilan nokta: {len(tanim_etkisi)}\n")
print("(1) TOHUMLAMA ETKISI -- ayni tanim, kontrol noktasi basina tohum")
print(f"{'protokol':22s}{'ort':>9s}{'|ort|':>9s}{'maks |.|':>10s}")
for k in P4:
    v = np.array(tohum_etkisi[k])
    print(f"{k:22s}{v.mean():>+9.3f}{np.abs(v).mean():>9.3f}{np.abs(v).max():>10.3f}")

print("\n(2) TANIM ETKISI -- siki eksi gevsek (yalniz basarili-kaynak)")
v = np.array(tanim_etkisi)
print(f"{'successful_source':22s}{v.mean():>+9.3f}{np.abs(v).mean():>9.3f}"
      f"{np.abs(v).max():>10.3f}")

print("\n(3) DORT PROTOKOL YAYILIMI")
a, b = np.array(yayilim_v1), np.array(yayilim_v2)
print(f"  v1 ort {a.mean():6.2f}   v2 ort {b.mean():6.2f}   fark {b.mean() - a.mean():+6.2f}")
