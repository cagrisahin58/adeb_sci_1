"""C1 t-SNE nicellestirmesi ve istatistiksel dogrulama sayilarini toplulastirir."""
import json

import numpy as np


def ms(v):
    a = np.asarray(v, dtype=float)
    return a.mean(), (a.std(ddof=1) if a.size > 1 else 0.0)


a5 = [json.load(open(f"results/c1_a5/pair{p}/a5_tsne_quant.json", encoding="utf-8")) for p in (1, 2, 3)]
print("=== t-SNE nicellestirmesi (whitebox), 3 tohum ort+-std ===")
keys = ["silhouette_clean", "silhouette_adv", "knn_clean_fit_clean_consistency",
        "knn_clean_fit_adv_consistency", "centroid_shift_rel",
        "intra_inter_ratio_clean", "intra_inter_ratio_adv"]
for model in ("ResNet18_AT", "ViT_Tiny_AT"):
    print(f"-- {model}")
    for k in keys:
        m, s = ms([d["designs"]["whitebox"][model][k] for d in a5])
        print(f"   {k:36s} {m:7.4f} +- {s:.4f}")

print("\n=== istatistiksel dogrulama (saldiri-baslatma) ===")
sv = json.load(open("results/c1_statval/statistical_validation.json", encoding="utf-8"))
for k, v in sv.items():
    if k in ("timestamp",):
        continue
    print(k, json.dumps(v)[:400])
