"""C4 (n=1000 oznitelik/attention) ve C5 (mekansal lokalite) sonuclarini
3 tohum uzerinden toplulastirir.

Cikti: results/c1_c45_summary.json + results/C1_C45_RAPORU.md
"""
import json
import os

import numpy as np

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
PAIRS = [1, 2, 3]


def load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def ms(vals):
    a = np.asarray(vals, dtype=float)
    return float(a.mean()), (float(a.std(ddof=1)) if a.size > 1 else 0.0)


c4 = [load(os.path.join(ROOT, f"results/c1_c4/pair{p}/c4_summary.json")) for p in PAIRS]
c5 = [load(os.path.join(ROOT, f"results/c1_c5/pair{p}/c5_spatial.json")) for p in PAIRS]

out = {}
L = ["# C4 + C5: n=1000 oznitelik/attention ve mekansal lokalite (3 tohum)\n"]

# ---- C4: ViT agregasyon varyantlari ----------------------------------------
blocks = [f"block{i}.mlp" for i in range(12)]
variants = {
    "cos_cls": "CLS jetonu",
    "cos_token_mean": "Yama jetonlari ortalamasi",
    "cos_flat_all_tokens": "Tum jetonlar (duzlestirilmis)",
}
L.append("## ViT: oznitelik kaymasi, agregasyon varyantina gore\n")
L.append("| Blok | " + " | ".join(variants.values()) + " | Blok cikisi |")
L.append("|---" * (len(variants) + 2) + "|")
out["vit_drift"] = {}
for i, b in enumerate(blocks):
    row = [f"| {i + 1}"]
    for v in variants:
        m, s = ms([d["vit"][v][b]["mean"] for d in c4])
        out["vit_drift"].setdefault(v, {})[b] = [m, s]
        row.append(f"{m:.4f}$\\pm${s:.4f}")
    bm, bs = ms([d["vit"]["cos_block_output"][f"block{i}"]["mean"] for d in c4])
    out["vit_drift"].setdefault("cos_block_output", {})[f"block{i}"] = [bm, bs]
    row.append(f"{bm:.4f}$\\pm${bs:.4f}")
    L.append(" | ".join(row) + " |")

mins = {}
for v in list(variants) + ["cos_block_output"]:
    keys = blocks if v in variants else [f"block{i}" for i in range(12)]
    means = [out["vit_drift"][v][k][0] for k in keys]
    mins[v] = (int(np.argmin(means)) + 1, float(np.min(means)))
out["vit_drift_minima"] = mins
L.append("\nEn dusuk kosinusun gorildigu blok (1-tabanli): " +
         ", ".join(f"{variants.get(v, 'Blok cikisi')} = {b} ({m:.4f})" for v, (b, m) in mins.items()) + "\n")

# ---- C4: ResNet katman profili ---------------------------------------------
res_keys = list(c4[0]["resnet"]["cos"].keys())
L.append("## ResNet: katman profili (n=1000)\n")
L.append("| Katman | Kosinus | Norm degisimi (%) |")
L.append("|---|---|---|")
out["resnet_drift"] = {}
for k in res_keys:
    cm, cs = ms([d["resnet"]["cos"][k]["mean"] for d in c4])
    nm, ns = ms([d["resnet"]["norm_change_pct"][k]["mean"] for d in c4])
    out["resnet_drift"][k] = {"cos": [cm, cs], "norm": [nm, ns]}
    L.append(f"| {k} | {cm:.4f}$\\pm${cs:.4f} | {nm:+.2f}$\\pm${ns:.2f} |")

# ---- C4: attention ----------------------------------------------------------
ent_d = np.array([d["vit"]["attention"]["entropy_delta_mean"] for d in c4])
disp = np.array([d["vit"]["attention"]["displacement_mean"] for d in c4])
out["attention"] = {
    "entropy_delta_mean": ent_d.mean(0).tolist(),
    "entropy_delta_std": ent_d.std(0, ddof=1).tolist(),
    "displacement_mean": disp.mean(0).tolist(),
    "displacement_std": disp.std(0, ddof=1).tolist(),
}
L.append("\n## ViT attention: entropi degisimi ve CLS yer degistirmesi\n")
L.append("| Katman | Entropi degisimi (adv - temiz) | CLS yer degistirmesi (toplam varyasyon) |")
L.append("|---|---|---|")
for i in range(ent_d.shape[1]):
    L.append(f"| {i + 1} | {ent_d.mean(0)[i]:+.4f}$\\pm${ent_d.std(0, ddof=1)[i]:.4f} | "
             f"{disp.mean(0)[i]:.4f}$\\pm${disp.std(0, ddof=1)[i]:.4f} |")

# ---- C4: saldiri sonucuna gore ayrim ----------------------------------------
L.append("\n## Saldirida devrilen ve devrilmeyen ornekler (son blok, tum jetonlar)\n")
last = "block11.mlp"
fl, nfl = [], []
for d in c4:
    s = d["vit"]["cos_by_attack_outcome"].get(last)
    if s and s.get("flipped"):
        fl.append(s["flipped"]["mean"])
        nfl.append(s["not_flipped"]["mean"])
if fl:
    fm, fs = ms(fl)
    nm2, ns2 = ms(nfl)
    out["flip_split_last_block"] = {"flipped": [fm, fs], "not_flipped": [nm2, ns2]}
    L.append(f"- ViT son blok kosinusu: devrilen {fm:.4f}$\\pm${fs:.4f}, "
             f"devrilmeyen {nm2:.4f}$\\pm${ns2:.4f}\n")

res_last = res_keys[-1]
fl_r = [d["resnet"]["cos_by_attack_outcome"][res_last]["flipped"]["mean"] for d in c4
        if d["resnet"]["cos_by_attack_outcome"][res_last].get("flipped")]
nfl_r = [d["resnet"]["cos_by_attack_outcome"][res_last]["not_flipped"]["mean"] for d in c4]
if fl_r:
    fm, fs = ms(fl_r)
    nm2, ns2 = ms(nfl_r)
    out["flip_split_resnet_last"] = {"flipped": [fm, fs], "not_flipped": [nm2, ns2]}
    L.append(f"- ResNet {res_last} kosinusu: devrilen {fm:.4f}$\\pm${fs:.4f}, "
             f"devrilmeyen {nm2:.4f}$\\pm${ns2:.4f}\n")

# ---- C5 ---------------------------------------------------------------------
L.append("## C5: gradyanlarin mekansal lokalitesi (n=500)\n")
L.append("| Olcut | ResNet-18 AT | ViT-Tiny AT | Eslesmis fark (R-V) | Wilcoxon p |")
L.append("|---|---|---|---|---|")
metrics = [("energy_area_50pct", "area50", "Enerjinin %50'sini tasiyan alan orani"),
           ("energy_area_90pct", "area90", "Enerjinin %90'ini tasiyan alan orani"),
           ("spatial_entropy", "entropy", "Mekansal entropi (nat)"),
           ("morans_i", "morans_i", "Moran's I (4-komsuluk)")]
out["spatial"] = {}
for key, diffkey, label in metrics:
    rm, rs = ms([d["models"]["ResNet18_AT"][key]["mean"] for d in c5])
    vm, vs = ms([d["models"]["ViT_Tiny_AT"][key]["mean"] for d in c5])
    dm, ds = ms([d["paired_diff_ResNet_minus_ViT"][diffkey]["mean"] for d in c5])
    ps = [d["paired_wilcoxon_p"][diffkey] for d in c5 if isinstance(d.get("paired_wilcoxon_p"), dict)]
    pmax = max(ps) if ps else float("nan")
    out["spatial"][key] = {"resnet": [rm, rs], "vit": [vm, vs], "diff": [dm, ds], "p_max": pmax}
    L.append(f"| {label} | {rm:.4f}$\\pm${rs:.4f} | {vm:.4f}$\\pm${vs:.4f} | "
             f"{dm:+.4f}$\\pm${ds:.4f} | {pmax:.2e} |")

L.append("\nDusuk alan orani ve dusuk entropi = daha lokalize; yuksek Moran's I = "
         "enerji bitisik piksellerde daha kumeli.\n")

with open(os.path.join(ROOT, "results/c1_c45_summary.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
with open(os.path.join(ROOT, "results/C1_C45_RAPORU.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print("\n".join(L))
