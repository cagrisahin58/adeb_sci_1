"""Tur 2: smoke AA ciktisi ile smoke matrislerindeki V_IN_smoke kosegeni."""
import glob
import json

import numpy as np

d = np.load("results/q1/konsey_smoke/aa/per_sample_V_IN_smoke.npz")
print("AA npz anahtarlar:", {k: d[k].shape for k in d.files})
print(json.dumps(json.load(open("results/q1/konsey_smoke/aa/autoattack_summary.json")), indent=1)[:1500])
for f in sorted(glob.glob("results/q1/konsey_smoke/matris_*/transfer_matrix.json")):
    j = json.load(open(f))
    print(f, j.get("n_samples"), j.get("attack"), {k: v for k, v in (j.get("model_specs") or {}).items() if "smoke" in k})
