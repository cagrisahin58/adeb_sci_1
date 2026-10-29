# -*- coding: utf-8 -*-
"""B1 smoke matrislerinde hangi modeller ve kac goruntu var (gorulmus veri envanteri)."""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
K = "/home/firat/projects/adeb_sci_1/results/q1/konsey_smoke"
for d in sorted(glob.glob(os.path.join(K, "matris_*"))):
    if not os.path.isdir(d):
        continue
    tm = os.path.join(d, "transfer_matrix.json")
    n_npz = len(glob.glob(os.path.join(d, "per_sample_*.npz")))
    if os.path.exists(tm):
        j = json.load(open(tm, encoding="utf-8"))
        print(os.path.basename(d), "n", j.get("n_samples"), "npz", n_npz, "modeller", j.get("models"))
    else:
        print(os.path.basename(d), "transfer_matrix.json yok; npz", n_npz,
              sorted({os.path.basename(f) for f in glob.glob(os.path.join(d, "*"))})[:6])
