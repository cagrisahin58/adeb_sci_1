"""C1 degerlendirme CSV'lerini (FGSM/PGD/temiz) 3 tohum uzerinden toplulastirir."""
import csv
import glob
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
PAIRS = [1, 2, 3]
EPS8 = round(8 / 255, 5)


def read_csv(path):
    vals = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            vals[(row["Attack"], round(float(row["Epsilon"]), 5))] = float(row["Accuracy"])
    return vals


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return {"mean": round(float(a.mean()), 2), "std": round(float(a.std(ddof=1)), 2) if a.size > 1 else 0.0,
            "values": [float(v) for v in a]}


out = {}
for tag, base in (("at", "results/c1_eval"), ("clean", "results/c1_eval_clean")):
    for model in ("resnet18", "vit_tiny"):
        paths = [os.path.join(ROOT, f"{base}/pair{p}/{model}/{model}_robustness_results.csv") for p in PAIRS]
        have = [p for p in paths if os.path.exists(p)]
        if len(have) != len(PAIRS):
            print(f"eksik ({len(have)}/3): {base} {model}")
            continue
        d = [read_csv(p) for p in have]
        out[f"{model}_{tag}"] = {
            "clean": ms([x[("clean", 0.0)] for x in d]),
            "fgsm": ms([x[("fgsm", EPS8)] for x in d]),
            "pgd": ms([x[("pgd", EPS8)] for x in d]),
        }

# Epsilon taramasi
for model in ("resnet18", "vit_tiny"):
    paths = [os.path.join(ROOT, f"results/c1_sweep/pair{p}/{model}/{model}_robustness_results.csv") for p in PAIRS]
    if not all(os.path.exists(p) for p in paths):
        continue
    d = [read_csv(p) for p in paths]
    sweep = {}
    for e in (0.0, 2 / 255, 4 / 255, 8 / 255, 16 / 255):
        key = ("clean", 0.0) if e == 0.0 else ("pgd", round(e, 5))
        if all(key in x for x in d):
            sweep[f"{e:.5f}"] = ms([x[key] for x in d])
    out[f"{model}_sweep"] = sweep

path = os.path.join(ROOT, "results/c1_eval_summary.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
print("kaydedildi:", path)
