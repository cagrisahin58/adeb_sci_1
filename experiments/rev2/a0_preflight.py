"""A0 preflight: rev2 BLOK A analizlerinin ihtiyaç duyduğu per-sample artefaktları introspekte eder.

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/a0_preflight.py
"""
import csv
import glob
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")


def show_npz(path):
    print(f"\n=== {os.path.relpath(path, ROOT)} ===")
    with np.load(path, allow_pickle=True) as z:
        for k in z.files:
            a = z[k]
            desc = f"  {k}: shape={a.shape} dtype={a.dtype}"
            if a.dtype == bool or (a.dtype.kind in "iu" and a.size and set(np.unique(a[: min(a.size, 10000)])) <= {0, 1}):
                desc += f" mean={a.astype(float).mean():.4f}"
            elif a.dtype.kind == "f" and a.size:
                desc += f" min={a.min():.4f} max={a.max():.4f} mean={a.mean():.4f}"
            elif a.dtype.kind in "iu" and a.size:
                u = np.unique(a)
                desc += f" uniq={u[:8]}{'...' if len(u) > 8 else ''}"
            print(desc)


for pattern in [
    "results/autoattack_run3_full/per_sample_*.npz",
    "results/transfer_analysis_run3/per_sample_*.npz",
    "results/wrn_eval/per_sample_*.npz",
    "results/c_addenda/*.npz",
]:
    for p in sorted(glob.glob(os.path.join(ROOT, pattern))):
        show_npz(p)

csv_path = os.path.join(ROOT, "results/gradient_analysis_run3/gradient_statistics.csv")
print(f"\n=== {os.path.relpath(csv_path, ROOT)} ===")
with open(csv_path) as f:
    rows = list(csv.reader(f))
print(f"  satır sayısı: {len(rows)} (başlık dahil)")
print(f"  başlık: {rows[0]}")
for r in rows[1:4]:
    print(f"  örnek: {r}")
