"""Bildiri figurleri (rev2 BLOK B). Yalniz gercek artefaktlardan; eksikte raise.

Cikti: paper/bildiri/figures/fig_b1_robustness.pdf, fig_b2_eps_sweep.pdf,
       fig_b3_feature_drift.pdf
WRN-28-10 ana ciftten GORSEL olarak ayrilir (B5): gri/taramali + 'reference'
etiketi (daha guclu recete + ek veri ile egitilmis harici checkpoint).
"""
import csv
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Repo koku: bu dosya paper/bildiri/ altinda oldugundan iki ust dizin.
# Docker icinde /workspace'e bagliyken de, host'ta da dogru cozulur.
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "paper/bildiri/figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 10, "axes.labelsize": 11, "axes.titlesize": 11,
    "legend.fontsize": 9, "xtick.labelsize": 10, "ytick.labelsize": 10,
    "figure.dpi": 150, "savefig.bbox": "tight",
})
C_CNN, C_VIT, C_WRN = "#0f62fe", "#da1e28", "#8d8d8d"


def die(path):
    raise FileNotFoundError(f"Gerekli artefakt yok: {path}")


def read_eval_csv(path):
    if not os.path.exists(path):
        die(path)
    vals = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            vals[(row["Attack"], round(float(row["Epsilon"]), 5))] = float(row["Accuracy"])
    return vals


# --- Veri -------------------------------------------------------------------
EPS8 = round(8 / 255, 5)
rn = read_eval_csv(os.path.join(ROOT, "results/final_eval_seeded/resnet18_at/resnet18_robustness_results.csv"))
vt = read_eval_csv(os.path.join(ROOT, "results/final_eval_seeded/vit_tiny_at/vit_tiny_robustness_results.csv"))
aa_path = os.path.join(ROOT, "results/autoattack_run3_full/autoattack_summary.json")
if not os.path.exists(aa_path):
    die(aa_path)
with open(aa_path) as f:
    aa = json.load(f)
aa_rn = aa_vt = None
for entry in aa["results"]:
    s = json.dumps(entry)
    if "ResNet18" in s:
        aa_rn = entry["robust_accuracy"]
    elif "ViT" in s:
        aa_vt = entry["robust_accuracy"]
if aa_rn is None or aa_vt is None:
    raise ValueError("autoattack_summary.json icinde model girdileri bulunamadi")
wrn_path = os.path.join(ROOT, "results/wrn_eval/wrn_eval_summary.json")
if not os.path.exists(wrn_path):
    die(wrn_path)
with open(wrn_path) as f:
    wrn = json.load(f)["results"]
WRN_AA_RB = 62.76  # RobustBench-raporlu AA (yerel AA kosulmadi)

# --- Fig B1: robustluk cubuklari (WRN ayri blok) ----------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.2))
metrics = ["Clean", "PGD-10", "AutoAttack"]
rn_vals = [rn[("clean", 0.0)], rn[("pgd", EPS8)], aa_rn]
vt_vals = [vt[("clean", 0.0)], vt[("pgd", EPS8)], aa_vt]
wrn_vals = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.03137"]["accuracy"], WRN_AA_RB]
x = np.arange(len(metrics), dtype=float)
w = 0.26
ax.bar(x - w / 2, rn_vals, w, color=C_CNN, label="ResNet-18 (AT)")
ax.bar(x + w / 2, vt_vals, w, color=C_VIT, label="ViT-Tiny (AT)")
# WRN: sagda ayri blok, gri + tarama + ayirici cizgi
xw = x + 3.4
ax.bar(xw, wrn_vals, w * 1.3, color=C_WRN, hatch="//", alpha=0.85,
       label="WRN-28-10 (reference$^{\\dagger}$)")
sep = (x[-1] + xw[0]) / 2
ax.axvline(sep, color="black", linewidth=0.8, linestyle=":")
for xi, v in zip(np.concatenate([x - w / 2, x + w / 2, xw]), rn_vals + vt_vals + wrn_vals):
    ax.text(xi, v + 1.2, f"{v:.1f}", ha="center", fontsize=7.5)
ax.set_xticks(np.concatenate([x, xw]))
ax.set_xticklabels(metrics + metrics, fontsize=9)
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(0, 100)
ax.text(float(np.mean(x)), 96, "Matched AT pair", ha="center", fontsize=9, fontweight="bold")
ax.text(float(np.mean(xw)), 96, "Reference$^{\\dagger}$", ha="center", fontsize=9, color="#444444")
ax.legend(loc="center", bbox_to_anchor=(0.5, -0.28), ncol=3, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(os.path.join(OUT, "fig_b1_robustness.pdf"))
plt.close(fig)
print("fig_b1_robustness.pdf")

# --- Fig B2: epsilon taramasi (WRN gri kesikli referans) --------------------
fig, ax = plt.subplots(figsize=(5.0, 3.1))
eps_grid = [0.0, 2 / 255, 4 / 255, 8 / 255, 16 / 255]
eps_lbl = ["0", "2/255", "4/255", "8/255", "16/255"]
rs = read_eval_csv(os.path.join(ROOT, "results/epsilon_sweep_seeded/resnet18/resnet18_robustness_results.csv"))
vs = read_eval_csv(os.path.join(ROOT, "results/epsilon_sweep_seeded/vit_tiny/vit_tiny_robustness_results.csv"))


def sweep_vals(d, clean):
    out = [clean]
    for e in eps_grid[1:]:
        out.append(d[("pgd", round(e, 5))])
    return out


wrn_sweep = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.00784"]["accuracy"], wrn["pgd10_eps0.01569"]["accuracy"],
             wrn["pgd10_eps0.03137"]["accuracy"], wrn["pgd10_eps0.06275"]["accuracy"]]
xi = np.arange(len(eps_grid))
ax.plot(xi, sweep_vals(rs, rs[("clean", 0.0)]), "o-", color=C_CNN, label="ResNet-18 (AT)")
ax.plot(xi, sweep_vals(vs, vs[("clean", 0.0)]), "s-", color=C_VIT, label="ViT-Tiny (AT)")
ax.plot(xi, wrn_sweep, "^--", color=C_WRN, alpha=0.9, label="WRN-28-10 (reference$^{\\dagger}$)")
ax.axvline(3, color="black", linewidth=0.7, linestyle=":", alpha=0.6)
ax.text(3.05, 5, "$\\epsilon$=8/255", fontsize=8)
ax.set_xticks(xi)
ax.set_xticklabels(eps_lbl)
ax.set_xlabel("Perturbation budget $\\epsilon$ ($L_\\infty$, PGD-10)")
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(0, 95)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(os.path.join(OUT, "fig_b2_eps_sweep.pdf"))
plt.close(fig)
print("fig_b2_eps_sweep.pdf")

# --- Fig B3: katman-bazli feature drift (ViT 12 blok vs ResNet 8 blok) ------
att_path = os.path.join(ROOT, "results/attention_analysis_run3/attention_summary.json")
res_path = os.path.join(ROOT, "results/c_addenda/resnet_feature_degradation.json")
for p in (att_path, res_path):
    if not os.path.exists(p):
        die(p)
with open(att_path) as f:
    att = json.load(f)
vit_layers = att["feature_analysis"] if "feature_analysis" in att else att["layers"]
vit_cos = [d["cosine_similarity"] for d in vit_layers]
vit_std = [d.get("cosine_similarity_std", 0.0) for d in vit_layers]
if not any(vit_std):  # summary json'da std yoksa CSV'den al
    csv_path = os.path.join(ROOT, "results/attention_analysis_run3/attention_feature_analysis.csv")
    with open(csv_path) as f:
        rows = list(csv.DictReader(f))
    vit_std = [float(r["cosine_similarity_std"]) for r in rows]
    assert len(vit_std) == len(vit_cos), "CSV blok sayisi summary ile uyusmuyor"
with open(res_path) as f:
    resdeg = json.load(f)["feature_analysis"]
res_cos = [d["cosine_similarity"] for d in resdeg]
res_std = [d.get("cosine_similarity_std", 0.0) for d in resdeg]

fig, ax = plt.subplots(figsize=(5.0, 3.0))
xv = np.linspace(0, 1, len(vit_cos))
xr = np.linspace(0, 1, len(res_cos))
# +-1 std bantlari (5 parti ortalamasi uzerinden std; ChatGPT hakemligi 4. madde)
ax.fill_between(xv, np.array(vit_cos) - np.array(vit_std), np.array(vit_cos) + np.array(vit_std),
                color=C_VIT, alpha=0.15, linewidth=0)
ax.fill_between(xr, np.array(res_cos) - np.array(res_std), np.array(res_cos) + np.array(res_std),
                color=C_CNN, alpha=0.15, linewidth=0)
ax.plot(xv, vit_cos, "o-", color=C_VIT, label="ViT-Tiny (12 blocks)")
ax.plot(xr, res_cos, "s--", color=C_CNN, label="ResNet-18 (8 residual blocks)")
imin = int(np.argmin(vit_cos))
ax.annotate("min 0.955 (block 8)\nthen slight recovery", xy=(xv[imin], vit_cos[imin]),
            xytext=(0.45, 0.975), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.annotate("monotonic drop\nto 0.913", xy=(xr[-1], res_cos[-1]), xytext=(0.62, 0.935),
            fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("Relative depth (block / total blocks)")
ax.set_ylabel("Clean-adversarial cosine similarity")
ax.legend(frameon=False, loc="lower left")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(os.path.join(OUT, "fig_b3_feature_drift.pdf"))
plt.close(fig)
print("fig_b3_feature_drift.pdf")
print("TAMAM")
