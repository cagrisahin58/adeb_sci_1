"""A1: Ana sonucun koşullu ayrıştırması (rev2 BLOK A).

Per-sample loglardan: conditioned fooling/survival (PGD-10, AutoAttack),
both-correct ortak kümede robust accuracy + McNemar, ayrıştırma denklemi
robust_acc = clean_acc x conditioned_survival dogrulamasi.

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/a1_conditioned_main.py
Çıktı: results/rev2_blockA/a1_conditioned_main.json
"""
import json
import math
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
OUT_DIR = os.path.join(ROOT, "results/rev2_blockA")
os.makedirs(OUT_DIR, exist_ok=True)

RNG = np.random.default_rng(42)
N_BOOT = 10000


def boot_ci_prop(mask_num, mask_den):
    """Percentile bootstrap CI for P(num | den) resampling the den-restricted set."""
    idx = np.flatnonzero(mask_den)
    vals = mask_num[idx].astype(float)
    n = len(vals)
    stats = np.empty(N_BOOT)
    for b in range(N_BOOT):
        stats[b] = vals[RNG.integers(0, n, n)].mean()
    return [float(np.percentile(stats, 2.5)) * 100, float(np.percentile(stats, 97.5)) * 100]


def mcnemar(only_a, only_b):
    """Continuity-corrected McNemar chi2 + p (normal approx via chi2 1 dof)."""
    n01, n10 = int(only_a), int(only_b)
    if n01 + n10 == 0:
        return 0.0, 1.0
    chi2 = (abs(n01 - n10) - 1) ** 2 / (n01 + n10)
    p = math.erfc(math.sqrt(chi2 / 2.0))
    return chi2, p


# --- Yukle -------------------------------------------------------------------
aa = {}
for model, fname in [("ResNet18_AT", "per_sample_ResNet18_AT.npz"), ("ViT_Tiny_AT", "per_sample_ViT_Tiny_AT.npz")]:
    with np.load(os.path.join(ROOT, "results/autoattack_run3_full", fname)) as z:
        aa[model] = {"clean": z["clean_correct"].copy(), "robust": z["robust_correct"].copy()}

pgd = {}
for model, fname in [
    ("ResNet18_AT", "per_sample_ResNet18_AT_to_ResNet18_AT.npz"),
    ("ViT_Tiny_AT", "per_sample_ViT_Tiny_AT_to_ViT_Tiny_AT.npz"),
]:
    with np.load(os.path.join(ROOT, "results/transfer_analysis_run3", fname)) as z:
        pgd[model] = {"clean": z["target_clean_correct"].copy(), "robust": ~z["target_adv_wrong"].copy()}

report = {"seed": 42, "n_bootstrap": N_BOOT, "models": {}, "both_correct": {}, "notes": []}

# --- Model bazli kosullu metrikler -------------------------------------------
for model in ["ResNet18_AT", "ViT_Tiny_AT"]:
    entry = {}
    for attack, d in [("AA", aa[model]), ("PGD10", pgd[model])]:
        clean, robust = d["clean"], d["robust"]
        clean_acc = clean.mean() * 100
        robust_acc = robust.mean() * 100
        cond_survival = robust[clean].mean() * 100
        cond_fooling = 100 - cond_survival
        # robust-but-clean-wrong orani (ayristirma denkleminin tamligi icin)
        robust_clean_wrong = (robust & ~clean).mean() * 100
        entry[attack] = {
            "clean_acc": round(float(clean_acc), 2),
            "robust_acc": round(float(robust_acc), 2),
            "cond_survival": round(float(cond_survival), 2),
            "cond_fooling": round(float(cond_fooling), 2),
            "cond_fooling_ci95": [round(100 - x, 2) for x in reversed(boot_ci_prop(d["robust"], d["clean"]))],
            "decomposition_clean_x_survival": round(float(clean_acc * cond_survival / 100), 2),
            "robust_but_clean_wrong_pct": round(float(robust_clean_wrong), 3),
        }
    report["models"][model] = entry

# --- Both-correct ortak kume -------------------------------------------------
for attack, data in [("AA", aa), ("PGD10", pgd)]:
    B = data["ResNet18_AT"]["clean"] & data["ViT_Tiny_AT"]["clean"]
    nB = int(B.sum())
    r_R = data["ResNet18_AT"]["robust"][B]
    r_V = data["ViT_Tiny_AT"]["robust"][B]
    only_R = int((r_R & ~r_V).sum())
    only_V = int((~r_R & r_V).sum())
    chi2, p = mcnemar(only_R, only_V)
    report["both_correct"][attack] = {
        "n_common": nB,
        "robust_acc_ResNet": round(float(r_R.mean() * 100), 2),
        "robust_acc_ViT": round(float(r_V.mean() * 100), 2),
        "diff_R_minus_V": round(float((r_R.mean() - r_V.mean()) * 100), 2),
        "only_ResNet_robust": only_R,
        "only_ViT_robust": only_V,
        "mcnemar_chi2": round(chi2, 2),
        "mcnemar_p": float(f"{p:.3g}"),
    }

report["notes"].append(
    "PGD-10 per-sample maskeleri transfer_analysis_run3 kosusunun white-box kosegeninden gelir "
    "(full-test PGD 40.87/36.06); Tablo I'deki seedli 40.97/36.09 ayri bir degerlendirme kosusudur "
    "(restart stokastisitesi ~0.1pp)."
)
report["notes"].append("AA icin robust_correct her zaman clean_correct alt kumesidir; ayristirma denklemi tamdir.")

out = os.path.join(OUT_DIR, "a1_conditioned_main.json")
with open(out, "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps(report, indent=1))
print(f"\nkaydedildi: {out}")
