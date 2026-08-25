#!/usr/bin/env python3
"""Iki iddianin DOGRU sayisini olcer (denetim bulgulari 10 ve 13)."""
import json
from pathlib import Path

ROOT = Path("/workspace")


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


print("=== (A) 'tohum duzeyi degisim en cok 0,55 puan' -- Tablo II kapsami ===")
s = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
enb, nerede = 0.0, ""
for model in ("resnet", "vit"):
    for k, v in s[model].items():
        if isinstance(v, dict) and "std" in v:
            print(f"  {model:8s} {k:22s} sd {v['std']:.4f}")
            if v["std"] > enb:
                enb, nerede = v["std"], f"{model}.{k}"
if "both_correct" in s:
    for k, v in s["both_correct"].items():
        if isinstance(v, dict) and "std" in v:
            print(f"  {'ortak':8s} {k:22s} sd {v['std']:.4f}")
            if v["std"] > enb:
                enb, nerede = v["std"], f"both_correct.{k}"
print(f"  -> EN BUYUK sd {enb:.4f} ({nerede})")

print("\n=== (B) Tablo V nicelikleri eski tek kosumla sd icinde tutuyor mu? ===")
beh = jl("results/c1_behavior_summary.json")["gradient"]
a3 = jl("results/rev2_blockA/a3_gradient_paired.json")
sp = a3["paired_sparsity_ResNet_vs_ViT"]
esle = [
    ("Hoyer", "sparsity_hoyer", "hoyer"),
    ("Gini", "sparsity_gini", "gini"),
    ("Frac<1%", "sparsity_rel_threshold", "rel"),
]
tutan, toplam = 0, 0
for ad, bk, ak in esle:
    for model, a3k in (("ResNet18_AT", "mean_ResNet"), ("ViT_Tiny_AT", "mean_ViT")):
        yeni = beh[model][bk]["mean"]
        sd = beh[model][bk].get("std")
        eski = sp[ak][a3k]
        if sd is None:
            continue
        toplam += 1
        ok = abs(yeni - eski) <= sd
        tutan += ok
        print(f"  {ad:9s} {model:12s} yeni {yeni:.4f}+/-{sd:.4f}  eski {eski:.4f}  "
              f"fark {abs(yeni-eski):.4f}  {'EVET' if ok else 'HAYIR'}")
for model, a3k in (("ResNet18_AT", "ResNet18_AT"), ("ViT_Tiny_AT", "ViT_Tiny_AT")):
    yeni = beh[model]["gradient_alignment"]["mean"]
    sd = beh[model]["gradient_alignment"].get("std")
    eski = a3["alignment"][a3k]["all_pairs_abs_mean"]
    if sd is None:
        continue
    toplam += 1
    ok = abs(yeni - eski) <= sd
    tutan += ok
    print(f"  {'Hizalanma':9s} {model:12s} yeni {yeni:.4f}+/-{sd:.4f}  eski {eski:.4f}  "
          f"fark {abs(yeni-eski):.4f}  {'EVET' if ok else 'HAYIR'}")
print(f"  -> {tutan}/{toplam} nicelik sd icinde tutuyor")

print("\n=== (C) CIFAR-100 bilesim etkisinin ASIMETRIYE orani ===")
for pr in ("target_correct", "successful_source"):
    oran = []
    for p in (1, 2, 3):
        d = jl(f"results/q1/cifar100/transfer/pair{p}/a2b_class_balance_cifar100.json")
        a = d["protokoller"][pr]["AYRISTIRMA"]
        oran.append(100 * abs(a["bilesim_etkisi"]) / abs(a["toplam_kontrol"]))
    print(f"  {pr:20s} {[round(x,1) for x in oran]}  -> {min(oran):.1f} ile {max(oran):.1f}")
