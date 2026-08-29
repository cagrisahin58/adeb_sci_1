#!/usr/bin/env python3
"""Hakem turu 3'te metne GIREN yeni tasiyici sayilari artefaktla dogrular.

Bu betik, sayilari verify_manuscript_numbers.py'ye eklemeden ONCE
artefaktlardan hesaplar; degerler tutmuyorsa metin degil BETIK yanlistir.
"""
import glob
import json
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path("/workspace")


def js(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


print("=" * 66)
print("1) AYRISTIRMA ACIKLIKLARI (CIFAR-10 / CIFAR-100 / SVHN)")
print("=" * 66)
tr = js("results/c1_transfer/c1_transfer_summary.json")
P = {k: v["diff"]["mean"] for k, v in tr["protocols"].items()}
print(f"  CIFAR-10  TC->BC {P['both_correct'] - P['target_correct']:.4f}"
      f"  BC->ham {P['raw'] - P['both_correct']:.4f}"
      f"  ham->SS {P['successful_source'] - P['raw']:.4f}")

for ad, yol in (("CIFAR-100", "results/q1/e1_cifar100_summary.json"),
                ("SVHN", "results/q1/e7_svhn_summary.json")):
    d = js(yol)

    def ara(o, hedef):
        if isinstance(o, dict):
            if hedef in o:
                return o[hedef]
            for v in o.values():
                r = ara(v, hedef)
                if r is not None:
                    return r
        return None

    pr = ara(d, "protocols")
    if pr is None:
        print(f"  {ad}: 'protocols' anahtari yok -> {list(d.keys())[:8]}")
        continue

    def dg(k):
        v = pr[k]
        if isinstance(v, dict):
            for a in ("diff", "asimetri", "asymmetry"):
                if a in v:
                    w = v[a]
                    return w["mean"] if isinstance(w, dict) else w
        return v

    tc, bc = dg("target_correct"), dg("both_correct")
    print(f"  {ad:10s} TC {tc}  BC {bc}  ->  TC->BC {bc - tc:.4f}")

print()
print("=" * 66)
print("2) KOSUM DUZEYI SEYREKLIK p DEGERLERI")
print("=" * 66)
OLC = [("Hoyer", "sparsity_hoyer"), ("Gini", "sparsity_gini"),
       ("Frac", "sparsity_rel_threshold"), ("Hizalanma", "gradient_alignment")]
ham = {}
for ad, key in OLC:
    R, V = [], []
    for p in sorted(glob.glob(str(ROOT / "results/c1_gradient/pair*"))):
        f = Path(p) / "gradient_summary.json"
        if not f.exists():
            continue
        o = json.loads(f.read_text(encoding="utf-8"))

        def bul(x, m):
            if isinstance(x, dict):
                if m in x and isinstance(x[m], dict):
                    v = x[m].get(key)
                    if isinstance(v, dict):
                        return v.get("mean")
                    if v is not None:
                        return v
                for y in x.values():
                    r = bul(y, m)
                    if r is not None:
                        return r
            return None
        a, b = bul(o, "ResNet18_AT"), bul(o, "ViT_Tiny_AT")
        if a is not None and b is not None:
            R.append(a); V.append(b)
    if len(R) >= 2:
        ham[ad] = float(stats.ttest_rel(R, V).pvalue)
        print(f"  {ad:10s} ham p = {ham[ad]:.4f}")

seyrek = {k: v for k, v in ham.items() if k != "Hizalanma"}
sirali = sorted(seyrek.items(), key=lambda kv: kv[1])
onceki, holm = 0.0, {}
for i, (ad, p) in enumerate(sirali):
    holm[ad] = onceki = max(onceki, min(1.0, (len(sirali) - i) * p))
print(f"  Holm (uc olcu de) = {max(holm.values()):.4f}")
print(f"  Hizalanma p       = {ham['Hizalanma']:.4f}")

print()
print("=" * 66)
print("3) HER-IKISI-DOGRU GA UCLARI VE t ARALIGI")
print("=" * 66)
bcp = tr["both_correct_paired"]
print(f"  GA alt uclari : {bcp['ci_low']['values']}")
print(f"  GA ust uclari : {bcp['ci_high']['values']}")
d3 = np.array(bcp["diff_pp"]["values"])
m, s = d3.mean(), d3.std(ddof=1)
t = stats.t.ppf(0.975, len(d3) - 1)
print(f"  koşumlar arasi t araligi: [{m - t*s/np.sqrt(len(d3)):.2f}, "
      f"{m + t*s/np.sqrt(len(d3)):.2f}]")

print()
print("=" * 66)
print("4) EN BUYUK DOGRULUK SS'si (AT cifti)")
print("=" * 66)
s = js("results/c1_eval_summary.json") if (ROOT / "results/c1_eval_summary.json").exists() else None
sd = js("results/c1_seeds/c1_seed_summary.json")
en_buyuk, nerede = 0.0, ""
for model in ("resnet", "vit"):
    for k, v in sd.get(model, {}).items():
        if isinstance(v, dict) and "std" in v and any(
                x in k for x in ("clean", "fgsm", "pgd", "aa")):
            if v["std"] > en_buyuk:
                en_buyuk, nerede = v["std"], f"{model}.{k}"
print(f"  en buyuk SS = {en_buyuk:.4f}  ({nerede})")
