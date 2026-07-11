#!/usr/bin/env python3
"""2026-07-10 hakem paneli B-maddeleri: mevcut artefaktlardan ek istatistikler.

GPU gerektirmez; yalnizca results/ altindaki per-sample .npz ve ozet
JSON/CSV'lerden hesaplar. Ciktilar: results/stat_addendum/stat_addendum.json

Hesaplananlar:
  B14  TOST (iki tek-tarafli z-testi) — kosullu transfer oranlarinin
       esdegerligi (marj: ±2 puan) + iki-oran z-testi
  B15  Tablo 3 metrikleri icin Welch t-testleri (10 parti-ortalamasindan)
  B16  Tablo 4 Blok8-vs-Blok11 cosine farki icin Welch t (5 parti)
  B18a Kosullu oranlar icin 10.000-resample percentile bootstrap CI
  B18b Native-ViT kontrol modelinin parametre sayisi ve checkpoint
       metriklerinden dogruluklari (dipnot icin)
"""

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "results" / "stat_addendum"
OUT_DIR.mkdir(parents=True, exist_ok=True)

out = {}

# ---------------------------------------------------------------------------
# B14 + B18a: kosullu transfer — iki-oran z, TOST, 10k bootstrap
# ---------------------------------------------------------------------------
tdir = ROOT / "results" / "transfer_analysis_run3"
cnn2vit = np.load(tdir / "per_sample_ResNet18_AT_to_ViT_Tiny_AT.npz")
vit2cnn = np.load(tdir / "per_sample_ViT_Tiny_AT_to_ResNet18_AT.npz")

# Kosullu kumeler: hedefin temiz-dogru siniflandirdigi ornekler
mask_a = cnn2vit["target_clean_correct"]            # hedef ViT
fool_a = cnn2vit["target_adv_wrong"][mask_a]        # CNN->ViT kosullu fooling
mask_b = vit2cnn["target_clean_correct"]            # hedef ResNet
fool_b = vit2cnn["target_adv_wrong"][mask_b]        # ViT->CNN kosullu fooling

p1, n1 = fool_a.mean(), len(fool_a)
p2, n2 = fool_b.mean(), len(fool_b)
diff = p1 - p2
se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)


def z_sf(z):
    """Standart normal sag-kuyruk olasiligi."""
    return 0.5 * math.erfc(z / math.sqrt(2))


# Iki-oran z-testi (fark = 0 hipotezi)
z_diff = diff / se
p_twosided = 2 * z_sf(abs(z_diff))

# TOST: |fark| < delta esdegerlik marji (2 puan)
DELTA = 0.02
z_lower = (diff + DELTA) / se   # H0: fark <= -delta
z_upper = (diff - DELTA) / se   # H0: fark >= +delta
p_tost = max(z_sf(z_lower), z_sf(-z_upper))

# 10.000-resample percentile bootstrap (B18: 1.000'den yukseltildi)
rng = np.random.default_rng(42)


def boot_ci(v, n_boot=10000):
    means = np.array([v[rng.integers(0, len(v), len(v))].mean() for _ in range(n_boot)])
    return [float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))]


ci_a = boot_ci(fool_a.astype(float))
ci_b = boot_ci(fool_b.astype(float))

out["transfer_equivalence"] = {
    "cnn_to_vit": {"rate": 100 * p1, "n": int(n1), "ci95_boot10k": [100 * c for c in ci_a]},
    "vit_to_cnn": {"rate": 100 * p2, "n": int(n2), "ci95_boot10k": [100 * c for c in ci_b]},
    "difference_pp": 100 * diff,
    "two_proportion_z": z_diff,
    "p_two_sided": p_twosided,
    "tost_margin_pp": 100 * DELTA,
    "tost_p": p_tost,
    "tost_conclusion": "equivalent within ±2pp" if p_tost < 0.05 else "equivalence not established",
}

# ---------------------------------------------------------------------------
# B15: Tablo 3 metrikleri icin Welch t (10 parti-ortalamasi/model)
# ---------------------------------------------------------------------------
gsum = json.load(open(ROOT / "results" / "gradient_analysis_run3" / "gradient_summary.json"))
stats = gsum["statistics"]


def welch(m1, s1, n1_, m2, s2, n2_):
    """Welch t-testi: mean/std/n ozetlerinden (std = orneklem std'si varsayimi)."""
    from scipy import stats as sps
    v1, v2 = s1 ** 2 / n1_, s2 ** 2 / n2_
    t = (m1 - m2) / math.sqrt(v1 + v2)
    df = (v1 + v2) ** 2 / (v1 ** 2 / (n1_ - 1) + v2 ** 2 / (n2_ - 1))
    p = 2 * float(sps.t.sf(abs(t), df))
    return t, df, p


NB = 10  # parti sayisi
r, v = stats["ResNet18_AT"], stats["ViT_Tiny_AT"]
table3_tests = {}
for metric, key_m, key_s in [
    ("hoyer", "sparsity_hoyer", "sparsity_hoyer_std"),
    ("gini", "sparsity_gini", "sparsity_gini_std"),
    ("rel_threshold", "sparsity_rel_threshold", "sparsity_rel_threshold_std"),
    ("alignment", "gradient_alignment", "gradient_alignment_std"),
]:
    t, df, p = welch(r[key_m], r[key_s], NB, v[key_m], v[key_s], NB)
    table3_tests[metric] = {
        "resnet_mean": r[key_m], "resnet_std": r[key_s],
        "vit_mean": v[key_m], "vit_std": v[key_s],
        "welch_t": t, "df": df, "p_two_sided": p,
    }
out["table3_welch"] = table3_tests

# ---------------------------------------------------------------------------
# B16: Tablo 4 — Blok8 vs Blok11 cosine (Welch, 5 parti)
# ---------------------------------------------------------------------------
asum = json.load(open(ROOT / "results" / "attention_analysis_run3" / "attention_summary.json"))
by_layer = {r_["layer"]: r_ for r_ in asum["feature_analysis"]}
b8, b11 = by_layer["blocks.8.mlp"], by_layer["blocks.11.mlp"]
t, df, p = welch(b8["cosine_similarity"], b8["cosine_similarity_std"], 5,
                 b11["cosine_similarity"], b11["cosine_similarity_std"], 5)
out["table4_block8_vs_block11"] = {
    "block8_cos": b8["cosine_similarity"], "block8_std": b8["cosine_similarity_std"],
    "block11_cos": b11["cosine_similarity"], "block11_std": b11["cosine_similarity_std"],
    "welch_t": t, "df": df, "p_two_sided": p,
}

# ---------------------------------------------------------------------------
# B18b: Native-ViT kontrol dipnot verileri (parametre sayisi + ckpt metrikleri)
# ---------------------------------------------------------------------------
native_info = {}
try:
    import sys
    sys.path.insert(0, str(ROOT))
    import torch
    from src.models import ModelRegistry
    m = ModelRegistry.get("vit_cifar_tiny")
    native_info["params"] = sum(p_.numel() for p_ in m.parameters())
    ckpt = torch.load(
        ROOT / "models/vit_cifar_tiny/adv/vit_cifar_tiny/adv/adversarial_training/best.pth",
        map_location="cpu", weights_only=False)
    native_info["ckpt_adv_acc"] = float(ckpt.get("accuracy", float("nan")))
    native_info["ckpt_clean_acc"] = float(ckpt.get("clean_acc", ckpt.get("extra_info", {}).get("clean_acc", float("nan"))) if not isinstance(ckpt.get("clean_acc"), type(None)) else ckpt.get("extra_info", {}).get("clean_acc", float("nan")))
except Exception as e:  # torch yoksa da diger sonuclar yazilsin
    native_info["error"] = str(e)
out["native_vit_control"] = native_info

with open(OUT_DIR / "stat_addendum.json", "w") as f:
    json.dump(out, f, indent=2)

print(json.dumps(out, indent=2))
print("\nSaved to", OUT_DIR / "stat_addendum.json")
