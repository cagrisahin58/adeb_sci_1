"""A3: Gradyan istatistiklerinin paired duzeltmesi (rev2 BLOK A).

Ayni ilk-500 test ornegi uc modelde de olculur (deterministik loader, seed 42):
- Per-sample Hoyer/Gini/rel-threshold -> paired Wilcoxon + paired bootstrap CI
  + paired Cohen's d + Holm duzeltmesi (3 sparsity metrigi).
- Alignment: TUM-ciftler (500x499/2) signed VE absolute cosine; ayrica 10
  rastgele 50'lik bolunme ortalamasi (eski batch semantigiyle karsilastirma).

Çalıştırma: docker exec adeb_eval python /workspace/experiments/rev2/a3_gradient_paired.py
Çıktı: results/rev2_blockA/a3_gradient_paired.json + a3_per_sample.npz
"""
import json
import math
import os
import sys

import numpy as np
import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

OUT_DIR = os.path.join(ROOT, "results/rev2_blockA")
os.makedirs(OUT_DIR, exist_ok=True)

SEED = 42
N_SAMPLES = 500
N_BOOT = 10000

MODELS = {
    "ResNet18_AT": ("resnet18", "models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth"),
    "ViT_Tiny_AT": ("vit_tiny", "models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth"),
    "ViT_CIFAR_Native_AT": ("vit_cifar_tiny", "models/vit_cifar_tiny/adv/vit_cifar_tiny/adv/adversarial_training/best.pth"),
}

torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)
np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def per_sample_metrics(grads_flat: torch.Tensor):
    """Olcek-bagimsiz sparsity metriklerinin PER-SAMPLE degerleri.

    Formuller src/analysis/gradient_analysis.py ile birebir ayni (yalnizca
    .mean() kaldirildi).
    """
    n = grads_flat.shape[1]
    l1 = grads_flat.abs().sum(dim=1)
    l2 = torch.norm(grads_flat, p=2, dim=1)
    sqrt_n = math.sqrt(float(n))
    hoyer = (sqrt_n - l1 / (l2 + 1e-12)) / (sqrt_n - 1)

    abs_sorted, _ = grads_flat.abs().sort(dim=1)
    idx = torch.arange(1, n + 1, device=grads_flat.device, dtype=abs_sorted.dtype)
    gini = 2 * (idx * abs_sorted).sum(dim=1) / (n * abs_sorted.sum(dim=1) + 1e-12) - (n + 1) / n

    max_abs = grads_flat.abs().max(dim=1, keepdim=True)[0]
    rel = (grads_flat.abs() < 0.01 * max_abs).float().mean(dim=1)
    return hoyer.cpu().numpy(), gini.cpu().numpy(), rel.cpu().numpy()


_, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=50)
loss_fn = torch.nn.CrossEntropyLoss(reduction="sum")

per_sample = {}
grad_store = {}
for name, (mtype, mpath) in MODELS.items():
    model = ModelRegistry.get(mtype)
    load_model_weights(model, mpath, device)
    model = model.to(device).eval()
    hoyers, ginis, rels, gvecs = [], [], [], []
    total = 0
    for images, labels in test_loader:
        if total >= N_SAMPLES:
            break
        if total + labels.size(0) > N_SAMPLES:
            keep = N_SAMPLES - total
            images, labels = images[:keep], labels[:keep]
        images = images.to(device).clone().requires_grad_(True)
        labels = labels.to(device)
        loss = loss_fn(model(images), labels)
        loss.backward()
        g = images.grad.detach()
        gf = g.view(g.shape[0], -1)
        h, gi, r = per_sample_metrics(gf)
        hoyers.append(h)
        ginis.append(gi)
        rels.append(r)
        gvecs.append((gf / (gf.norm(dim=1, keepdim=True) + 1e-12)).cpu())
        total += labels.size(0)
    per_sample[name] = {
        "hoyer": np.concatenate(hoyers),
        "gini": np.concatenate(ginis),
        "rel": np.concatenate(rels),
    }
    grad_store[name] = torch.cat(gvecs)
    del model
    torch.cuda.empty_cache()
    print(f"{name}: {total} ornek islendi")

# --- Alignment: tum-ciftler + partisyon kararliligi ---------------------------
rng = np.random.default_rng(SEED)
alignment = {}
for name, G in grad_store.items():
    C = (G @ G.T).numpy()
    off = C[np.triu_indices(C.shape[0], k=1)]
    part_means = []
    for _ in range(10):
        perm = rng.permutation(C.shape[0])
        vals = []
        for b in range(0, C.shape[0], 50):
            sub = C[np.ix_(perm[b : b + 50], perm[b : b + 50])]
            vals.append(np.abs(sub[np.triu_indices(sub.shape[0], k=1)]).mean())
        part_means.append(float(np.mean(vals)))
    alignment[name] = {
        "all_pairs_abs_mean": round(float(np.abs(off).mean()), 4),
        "all_pairs_signed_mean": round(float(off.mean()), 4),
        "n_pairs": int(off.size),
        "partition50_abs_mean": round(float(np.mean(part_means)), 4),
        "partition50_abs_std": round(float(np.std(part_means)), 4),
    }

# --- Paired istatistik (ana cift) --------------------------------------------
def wilcoxon_signed_rank(d):
    """Normal yaklasimli Wilcoxon signed-rank (sifir farklar atilir)."""
    d = d[d != 0]
    n = len(d)
    ranks = np.argsort(np.argsort(np.abs(d))) + 1.0
    w_pos = ranks[d > 0].sum()
    mu = n * (n + 1) / 4.0
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    z = (w_pos - mu) / sigma
    p = math.erfc(abs(z) / math.sqrt(2))
    return float(z), float(p), int(n)


paired = {}
pvals = {}
for metric in ["hoyer", "gini", "rel"]:
    d = per_sample["ResNet18_AT"][metric] - per_sample["ViT_Tiny_AT"][metric]
    z, p, n_eff = wilcoxon_signed_rank(d)
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        boots[b] = d[rng.integers(0, len(d), len(d))].mean()
    paired[metric] = {
        "mean_ResNet": round(float(per_sample["ResNet18_AT"][metric].mean()), 4),
        "mean_ViT": round(float(per_sample["ViT_Tiny_AT"][metric].mean()), 4),
        "paired_mean_diff": round(float(d.mean()), 4),
        "paired_bootstrap_ci95": [round(float(np.percentile(boots, 2.5)), 4), round(float(np.percentile(boots, 97.5)), 4)],
        "wilcoxon_z": round(z, 2),
        "wilcoxon_p_raw": float(f"{p:.3g}"),
        "cohens_d_paired": round(float(d.mean() / (d.std(ddof=1) + 1e-12)), 3),
        "n_effective": n_eff,
    }
    pvals[metric] = p

# Holm duzeltmesi (3 sparsity metrigi)
order = sorted(pvals, key=lambda k: pvals[k])
m = len(order)
prev = 0.0
for i, k in enumerate(order):
    adj = min(1.0, (m - i) * pvals[k])
    adj = max(adj, prev)
    prev = adj
    paired[k]["wilcoxon_p_holm"] = float(f"{adj:.3g}")

report = {
    "seed": SEED,
    "n_samples": N_SAMPLES,
    "n_bootstrap": N_BOOT,
    "model_paths": {k: v[1] for k, v in MODELS.items()},
    "paired_sparsity_ResNet_vs_ViT": paired,
    "alignment": alignment,
    "notes": [
        "Sparsity metrik formulleri src/analysis/gradient_analysis.py ile birebir ayni; yalnizca per-sample toplandi.",
        "Alignment all-pairs 500x499/2 cift uzerinden; partition50 eski batch-of-50 semantiginin 10 rastgele bolunme ortalamasi.",
        "Absolute cosine paylasilan duyarlilik YONLERINI (isaretten bagimsiz) olcer; signed ortalama, yon tutarliligini gosterir (UAP argumani icin ikisi de rapor edilir).",
    ],
}

np.savez_compressed(
    os.path.join(OUT_DIR, "a3_per_sample.npz"),
    **{f"{name}_{metric}": per_sample[name][metric] for name in per_sample for metric in per_sample[name]},
)
out = os.path.join(OUT_DIR, "a3_gradient_paired.json")
with open(out, "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps(report, indent=1))
print(f"\nkaydedildi: {out}")
