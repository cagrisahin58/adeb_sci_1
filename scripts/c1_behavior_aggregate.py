"""C1 davranissal analizlerin (gradyan yapisi, blok bazli kayma, MI-FGSM,
temiz gradyan) 3 tohum uzerinden toplulastirilmasi.

Girdi : results/c1_gradient/pairN, results/c1_drift/pairN, results/c1_addenda/pairN
Cikti : results/c1_behavior_summary.json + results/C1_DAVRANIS_RAPORU.md
"""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
PAIRS = [1, 2, 3]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return {"mean": float(a.mean()), "std": float(a.std(ddof=1)) if a.size > 1 else 0.0,
            "values": [float(v) for v in a]}


def dig(obj, *keys, default=None):
    """Ic ice sozlukte ilk eslesen anahtar yolunu dener."""
    for key in keys:
        cur = obj
        ok = True
        for part in key.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            return cur
    return default


out = {}

# --- Gradyan yapisi ---------------------------------------------------------
grads = [load(os.path.join(ROOT, f"results/c1_gradient/pair{p}/gradient_summary.json")) for p in PAIRS]
GRAD_METRICS = [
    "sparsity_hoyer",
    "sparsity_gini",
    "sparsity_rel_threshold",
    "gradient_alignment",
    "l2_norm_mean",
]
out["gradient"] = {}
for model in ("ResNet18_AT", "ViT_Tiny_AT"):
    out["gradient"][model] = {
        m: ms([g["statistics"][model][m] for g in grads]) for m in GRAD_METRICS
    }
out["gradient"]["diff_R_minus_V"] = {
    m: ms([g["statistics"]["ResNet18_AT"][m] - g["statistics"]["ViT_Tiny_AT"][m] for g in grads])
    for m in GRAD_METRICS
}

# Eslesmis istatistikler (a3): varsa Wilcoxon/Holm ve tum-cift alignment
a3_files = [os.path.join(ROOT, f"results/c1_a3/pair{p}/a3_gradient_paired.json") for p in PAIRS]
if all(os.path.exists(f) for f in a3_files):
    out["gradient_paired"] = {"per_pair": [load(f) for f in a3_files]}

# --- Blok bazli kayma -------------------------------------------------------
drifts = [load(os.path.join(ROOT, f"results/c1_drift/pair{p}/attention_summary.json")) for p in PAIRS]
vit_layers = [d.get("feature_analysis", d.get("layers")) for d in drifts]
cos = np.array([[x["cosine_similarity"] for x in layers] for layers in vit_layers], dtype=float)
out["drift_vit"] = {
    "n_blocks": cos.shape[1],
    "cosine_mean": cos.mean(axis=0).tolist(),
    "cosine_std": (cos.std(axis=0, ddof=1) if cos.shape[0] > 1 else np.zeros(cos.shape[1])).tolist(),
    "min_block_1indexed": [int(np.argmin(c)) + 1 for c in cos],
    "min_value": ms([float(c.min()) for c in cos]),
}

res_files = [os.path.join(ROOT, f"results/c1_addenda/pair{p}/resnet_feature_degradation.json") for p in PAIRS]
if all(os.path.exists(f) for f in res_files):
    rcos = np.array([[x["cosine_similarity"] for x in load(f)["feature_analysis"]] for f in res_files], dtype=float)
    out["drift_resnet"] = {
        "n_blocks": rcos.shape[1],
        "cosine_mean": rcos.mean(axis=0).tolist(),
        "cosine_std": (rcos.std(axis=0, ddof=1) if rcos.shape[0] > 1 else np.zeros(rcos.shape[1])).tolist(),
        "final_value": ms([float(c[-1]) for c in rcos]),
        "monotonic": [bool(np.all(np.diff(c) <= 1e-9)) for c in rcos],
    }

# --- MI-FGSM transfer -------------------------------------------------------
mi_files = [os.path.join(ROOT, f"results/c1_addenda/pair{p}/mifgsm_transfer.json") for p in PAIRS]
if all(os.path.exists(f) for f in mi_files):
    mi = [load(f)["results"] for f in mi_files]
    pairs_keys = [(r["source"], r["target"]) for r in mi[0]] if "source" in mi[0][0] else None
    out["mifgsm"] = {}
    for i, entry in enumerate(mi[0]):
        src = entry.get("source", entry.get("src", f"idx{i}"))
        tgt = entry.get("target", entry.get("tgt", ""))
        if src == tgt:
            continue
        out["mifgsm"][f"{src}->{tgt}"] = ms([m[i]["conditioned_fooling_rate"] for m in mi])
    out["mifgsm_pairs"] = pairs_keys

# --- Temiz modellerde gradyan (AT'nin siralamayi tersine cevirmesi) ---------
clean_files = [os.path.join(ROOT, f"results/c1_addenda/pair{p}/clean_gradient_stats.json") for p in PAIRS]
if all(os.path.exists(f) for f in clean_files):
    out["clean_gradient"] = {"per_pair": [load(f) for f in clean_files]}

out_path = os.path.join(ROOT, "results/c1_behavior_summary.json")
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
print(f"kaydedildi: {out_path}")
print(json.dumps({k: v for k, v in out.items() if k not in ("gradient",)}, indent=1, ensure_ascii=False)[:3000])
