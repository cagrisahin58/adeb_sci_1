"""C1 3-seed toplu analizi.

Girdi : results/c1_seeds/pair{1,2,3}/  (per-sample PGD ve AutoAttack npz'leri)
Cikti : results/c1_seeds/c1_seed_summary.json  ve  results/c1_seeds/C1_SEED_RAPORU.md

Uretilenler:
  * cift basina temiz / PGD-10 / AutoAttack dogrulugu (tam test, n=10000)
  * mimari basina ortalama +- std (ddof=1)
  * kosullu ayrisma: robust = temiz x kosullu_hayatta_kalma (birebir ozdeslik)
  * her ikisi dogru (both-correct) eslesmis alt kumede robust dogruluk
  * kosu-basina McNemar (tam binom, iki yonlu) hem PGD hem AA icin
  * seed duzeyinde eslesmis fark ozetleri
"""
import glob
import json
import os
import re

import numpy as np

try:
    from scipy.stats import binomtest as _binomtest

    def mcnemar_exact(b, c):
        n = b + c
        if n == 0:
            return 1.0
        return float(_binomtest(min(b, c), n, 0.5, alternative="two-sided").pvalue)
except Exception:  # scipy yoksa normal yaklasim
    from math import erfc, sqrt

    def mcnemar_exact(b, c):
        n = b + c
        if n == 0:
            return 1.0
        z = abs(b - c) / sqrt(n)
        return float(erfc(z / sqrt(2)))


ROOT = "results/c1_seeds"
PAIRS = [1, 2, 3]
RESNET_SEEDS = {1: 1001, 2: 1002, 3: 1003}
VIT_SEEDS = {1: 2001, 2: 2002, 3: 2003}


def load(path):
    d = np.load(path)
    return d["clean_correct"].astype(bool), d["robust_correct"].astype(bool)


def acc(mask):
    return 100.0 * float(mask.mean())


def cond_survival(clean, robust):
    """Temiz-dogru ornekler uzerinde hayatta kalma orani (%)."""
    if clean.sum() == 0:
        return float("nan")
    return 100.0 * float(robust[clean].mean())


def ms(values):
    a = np.asarray(values, dtype=float)
    return {
        "mean": float(a.mean()),
        "std": float(a.std(ddof=1)) if a.size > 1 else 0.0,
        "values": [float(v) for v in a],
    }


rows = []
for p in PAIRS:
    d = os.path.join(ROOT, f"pair{p}")
    rc, rr = load(os.path.join(d, f"pgd_per_sample_resnet18_s{RESNET_SEEDS[p]}.npz"))
    vc, vr = load(os.path.join(d, f"pgd_per_sample_vit_tiny_s{VIT_SEEDS[p]}.npz"))
    rac, rar = load(os.path.join(d, "per_sample_ResNet18_AT.npz"))
    vac, var = load(os.path.join(d, "per_sample_ViT_Tiny_AT.npz"))

    # temiz maskeler PGD ve AA dosyalarinda ayni olmali (ayni checkpoint, ayni test seti)
    assert rc.sum() == rac.sum(), f"pair{p}: ResNet temiz sayilari uyusmuyor"
    assert vc.sum() == vac.sum(), f"pair{p}: ViT temiz sayilari uyusmuyor"

    both_pgd = rc & vc
    both_aa = rac & vac

    b_pgd = int((rr & ~vr).sum())
    c_pgd = int((vr & ~rr).sum())
    b_aa = int((rar & ~var).sum())
    c_aa = int((var & ~rar).sum())

    rows.append(
        {
            "pair": p,
            "resnet_seed": RESNET_SEEDS[p],
            "vit_seed": VIT_SEEDS[p],
            "resnet": {
                "clean": acc(rc),
                "pgd": acc(rr),
                "aa": acc(rar),
                "cond_survival_pgd": cond_survival(rc, rr),
                "cond_survival_aa": cond_survival(rac, rar),
                "cond_fooling_pgd": 100.0 - cond_survival(rc, rr),
                "cond_fooling_aa": 100.0 - cond_survival(rac, rar),
            },
            "vit": {
                "clean": acc(vc),
                "pgd": acc(vr),
                "aa": acc(var),
                "cond_survival_pgd": cond_survival(vc, vr),
                "cond_survival_aa": cond_survival(vac, var),
                "cond_fooling_pgd": 100.0 - cond_survival(vc, vr),
                "cond_fooling_aa": 100.0 - cond_survival(vac, var),
            },
            "both_correct": {
                "n_pgd": int(both_pgd.sum()),
                "n_aa": int(both_aa.sum()),
                "resnet_robust_pgd": 100.0 * float(rr[both_pgd].mean()),
                "vit_robust_pgd": 100.0 * float(vr[both_pgd].mean()),
                "resnet_robust_aa": 100.0 * float(rar[both_aa].mean()),
                "vit_robust_aa": 100.0 * float(var[both_aa].mean()),
            },
            "mcnemar_pgd": {
                "resnet_only": b_pgd,
                "vit_only": c_pgd,
                "p_exact": mcnemar_exact(b_pgd, c_pgd),
            },
            "mcnemar_aa": {
                "resnet_only": b_aa,
                "vit_only": c_aa,
                "p_exact": mcnemar_exact(b_aa, c_aa),
            },
        }
    )

agg = {}
for arch in ("resnet", "vit"):
    agg[arch] = {
        k: ms([r[arch][k] for r in rows])
        for k in (
            "clean",
            "pgd",
            "aa",
            "cond_survival_pgd",
            "cond_survival_aa",
            "cond_fooling_pgd",
            "cond_fooling_aa",
        )
    }
agg["both_correct"] = {
    k: ms([r["both_correct"][k] for r in rows])
    for k in (
        "n_pgd",
        "n_aa",
        "resnet_robust_pgd",
        "vit_robust_pgd",
        "resnet_robust_aa",
        "vit_robust_aa",
    )
}
agg["gaps"] = {
    "clean": ms([r["resnet"]["clean"] - r["vit"]["clean"] for r in rows]),
    "pgd": ms([r["resnet"]["pgd"] - r["vit"]["pgd"] for r in rows]),
    "aa": ms([r["resnet"]["aa"] - r["vit"]["aa"] for r in rows]),
    "cond_fooling_pgd": ms(
        [r["resnet"]["cond_fooling_pgd"] - r["vit"]["cond_fooling_pgd"] for r in rows]
    ),
    "cond_fooling_aa": ms(
        [r["resnet"]["cond_fooling_aa"] - r["vit"]["cond_fooling_aa"] for r in rows]
    ),
    "both_correct_pgd": ms(
        [r["both_correct"]["resnet_robust_pgd"] - r["both_correct"]["vit_robust_pgd"] for r in rows]
    ),
    "both_correct_aa": ms(
        [r["both_correct"]["resnet_robust_aa"] - r["both_correct"]["vit_robust_aa"] for r in rows]
    ),
}

# egitim sureleri (TIMING.md'den, varsa)
timing = {}
if os.path.exists("TIMING.md"):
    with open("TIMING.md", encoding="utf-8") as fh:
        timing["raw_lines"] = sum(1 for _ in fh)
log_path = "logs/c1_pipeline.log"
if os.path.exists(log_path):
    durations = {}
    with open(log_path, encoding="utf-8") as fh:
        for line in fh:
            m = re.search(r"DONE\s+(\S+)\s+\((\d+)s\)", line)
            if m:
                durations[m.group(1)] = int(m.group(2))
    timing["stage_seconds"] = durations
    timing["total_hours"] = round(sum(durations.values()) / 3600.0, 2)

out = {"pairs": rows, "aggregate": agg, "timing": timing}
os.makedirs(ROOT, exist_ok=True)
with open(os.path.join(ROOT, "c1_seed_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)


def f(x, n=2):
    return f"{x:.{n}f}"


lines = []
lines.append("# C1: 3 Tohumlu (seed) Sonuclar - Sizinti Duzeltmeli Protokol\n")
lines.append(
    "Sabit ortak 2000 orneklik dogrulama bolmesi (seed 777) clean on-egitimden ONCE ayrildi; "
    "model secimi val PGD-10 uzerinden. Tum degerlendirmeler tam test kumesinde (n=10000).\n"
)
lines.append("## Cift bazinda\n")
lines.append(
    "| Cift | Model | Temiz | PGD-10 | AA | Kos. yanilt. (PGD) | Kos. yanilt. (AA) |"
)
lines.append("|---|---|---|---|---|---|---|")
for r in rows:
    lines.append(
        f"| {r['pair']} (s{r['resnet_seed']}) | ResNet-18 AT | {f(r['resnet']['clean'])} | "
        f"{f(r['resnet']['pgd'])} | {f(r['resnet']['aa'])} | {f(r['resnet']['cond_fooling_pgd'])} | "
        f"{f(r['resnet']['cond_fooling_aa'])} |"
    )
    lines.append(
        f"| {r['pair']} (s{r['vit_seed']}) | ViT-Tiny AT | {f(r['vit']['clean'])} | "
        f"{f(r['vit']['pgd'])} | {f(r['vit']['aa'])} | {f(r['vit']['cond_fooling_pgd'])} | "
        f"{f(r['vit']['cond_fooling_aa'])} |"
    )

lines.append("\n## Ortalama +- std (3 tohum)\n")
lines.append("| Metrik | ResNet-18 AT | ViT-Tiny AT | Fark (R-V) |")
lines.append("|---|---|---|---|")
for key, label in [
    ("clean", "Temiz"),
    ("pgd", "PGD-10"),
    ("aa", "AutoAttack"),
    ("cond_fooling_pgd", "Kosullu yaniltma (PGD)"),
    ("cond_fooling_aa", "Kosullu yaniltma (AA)"),
]:
    gap = agg["gaps"][key]
    lines.append(
        f"| {label} | {f(agg['resnet'][key]['mean'])} +- {f(agg['resnet'][key]['std'])} | "
        f"{f(agg['vit'][key]['mean'])} +- {f(agg['vit'][key]['std'])} | "
        f"{f(gap['mean'])} +- {f(gap['std'])} |"
    )

lines.append("\n## Kosullu ayrisma (robust = temiz x kosullu hayatta kalma)\n")
for r in rows:
    for arch, name in (("resnet", "ResNet-18"), ("vit", "ViT-Tiny")):
        a = r[arch]
        lines.append(
            f"- Cift {r['pair']} {name} (AA): {f(a['clean'])} x {f(a['cond_survival_aa'])}% = "
            f"{f(a['clean'] * a['cond_survival_aa'] / 100.0)} (olculen {f(a['aa'])})"
        )

lines.append("\n## Her ikisi dogru (both-correct) eslesmis alt kume\n")
lines.append("| Cift | n (PGD) | ResNet PGD | ViT PGD | n (AA) | ResNet AA | ViT AA |")
lines.append("|---|---|---|---|---|---|---|")
for r in rows:
    b = r["both_correct"]
    lines.append(
        f"| {r['pair']} | {b['n_pgd']} | {f(b['resnet_robust_pgd'])} | {f(b['vit_robust_pgd'])} | "
        f"{b['n_aa']} | {f(b['resnet_robust_aa'])} | {f(b['vit_robust_aa'])} |"
    )

lines.append("\n## Kosu bazinda McNemar (tam binom, iki yonlu)\n")
lines.append("| Cift | Saldiri | Yalniz ResNet dogru | Yalniz ViT dogru | p |")
lines.append("|---|---|---|---|---|")
for r in rows:
    for key, label in (("mcnemar_pgd", "PGD-10"), ("mcnemar_aa", "AutoAttack")):
        m = r[key]
        lines.append(
            f"| {r['pair']} | {label} | {m['resnet_only']} | {m['vit_only']} | {m['p_exact']:.3e} |"
        )

if "total_hours" in timing:
    lines.append(f"\n## Sure\n\nToplam C1 GPU zamani: {timing['total_hours']} saat (RTX 5090).\n")

with open(os.path.join(ROOT, "C1_SEED_RAPORU.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")

print("\n".join(lines))
