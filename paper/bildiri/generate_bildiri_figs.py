"""Bildiri figurleri (rev2 BLOK B). Yalniz gercek artefaktlardan; eksikte raise.

Cikti: paper/bildiri/figures/fig_b1_robustness.pdf, fig_b2_eps_sweep.pdf,
       fig_b3_feature_drift.pdf

Iki kaynak modu:
  --source run3 : tek kosu, eski (sizintili val bolmesi) kontrol noktalari
  --source c1   : 3 tohum, sizinti duzeltmeli C1 kontrol noktalari (varsayilan);
                  cubuk/egrilerde ortalama, hata cubuklari ve bantlar +-1 std
                  (tohumlar arasi).

WRN-28-10 ana ciftten GORSEL olarak ayrilir (B5): gri/taramali + 'reference'
etiketi (daha guclu recete + ek veri ile egitilmis harici checkpoint).
"""
import argparse
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

ap = argparse.ArgumentParser()
ap.add_argument("--source", choices=["run3", "c1"], default="c1")
args = ap.parse_args()
PAIRS = [1, 2, 3]

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


def load_json(path):
    if not os.path.exists(path):
        die(path)
    with open(path) as f:
        return json.load(f)


def ms(vals):
    """Ortalama ve std (tek deger listesinde std=0)."""
    a = np.asarray(vals, dtype=float)
    return float(a.mean()), (float(a.std(ddof=1)) if a.size > 1 else 0.0)


def aa_from_summary(path):
    aa = load_json(path)
    rn = vt = None
    for entry in aa["results"]:
        s = json.dumps(entry)
        if "ResNet18" in s:
            rn = entry["robust_accuracy"]
        elif "ViT" in s:
            vt = entry["robust_accuracy"]
    if rn is None or vt is None:
        raise ValueError(f"model girdileri bulunamadi: {path}")
    return rn, vt


EPS8 = round(8 / 255, 5)
EPS_GRID = [0.0, 2 / 255, 4 / 255, 8 / 255, 16 / 255]
EPS_LBL = ["0", "2/255", "4/255", "8/255", "16/255"]

# --- Veri: kaynak moduna gore ----------------------------------------------
if args.source == "run3":
    rn = read_eval_csv(os.path.join(ROOT, "results/final_eval_seeded/resnet18_at/resnet18_robustness_results.csv"))
    vt = read_eval_csv(os.path.join(ROOT, "results/final_eval_seeded/vit_tiny_at/vit_tiny_robustness_results.csv"))
    aa_rn, aa_vt = aa_from_summary(os.path.join(ROOT, "results/autoattack_run3_full/autoattack_summary.json"))
    rn_bar = [(rn[("clean", 0.0)], 0.0), (rn[("pgd", EPS8)], 0.0), (aa_rn, 0.0)]
    vt_bar = [(vt[("clean", 0.0)], 0.0), (vt[("pgd", EPS8)], 0.0), (aa_vt, 0.0)]
    rs = read_eval_csv(os.path.join(ROOT, "results/epsilon_sweep_seeded/resnet18/resnet18_robustness_results.csv"))
    vs = read_eval_csv(os.path.join(ROOT, "results/epsilon_sweep_seeded/vit_tiny/vit_tiny_robustness_results.csv"))
    rn_sweep = [(rs[("clean", 0.0)], 0.0)] + [(rs[("pgd", round(e, 5))], 0.0) for e in EPS_GRID[1:]]
    vt_sweep = [(vs[("clean", 0.0)], 0.0)] + [(vs[("pgd", round(e, 5))], 0.0) for e in EPS_GRID[1:]]
    drift_vit_dirs = [os.path.join(ROOT, "results/attention_analysis_run3")]
    drift_res_files = [os.path.join(ROOT, "results/c_addenda/resnet_feature_degradation.json")]
else:
    ev = {p: {m: read_eval_csv(os.path.join(ROOT, f"results/c1_eval/pair{p}/{m}/{m}_robustness_results.csv"))
              for m in ("resnet18", "vit_tiny")} for p in PAIRS}
    sw = {p: {m: read_eval_csv(os.path.join(ROOT, f"results/c1_sweep/pair{p}/{m}/{m}_robustness_results.csv"))
              for m in ("resnet18", "vit_tiny")} for p in PAIRS}
    aa = {p: aa_from_summary(os.path.join(ROOT, f"results/c1_seeds/pair{p}/autoattack_summary.json")) for p in PAIRS}
    rn_bar = [
        ms([ev[p]["resnet18"][("clean", 0.0)] for p in PAIRS]),
        ms([ev[p]["resnet18"][("pgd", EPS8)] for p in PAIRS]),
        ms([aa[p][0] for p in PAIRS]),
    ]
    vt_bar = [
        ms([ev[p]["vit_tiny"][("clean", 0.0)] for p in PAIRS]),
        ms([ev[p]["vit_tiny"][("pgd", EPS8)] for p in PAIRS]),
        ms([aa[p][1] for p in PAIRS]),
    ]
    rn_sweep = [ms([sw[p]["resnet18"][("clean", 0.0)] for p in PAIRS])] + [
        ms([sw[p]["resnet18"][("pgd", round(e, 5))] for p in PAIRS]) for e in EPS_GRID[1:]
    ]
    vt_sweep = [ms([sw[p]["vit_tiny"][("clean", 0.0)] for p in PAIRS])] + [
        ms([sw[p]["vit_tiny"][("pgd", round(e, 5))] for p in PAIRS]) for e in EPS_GRID[1:]
    ]
    drift_vit_dirs = [os.path.join(ROOT, f"results/c1_drift/pair{p}") for p in PAIRS]
    drift_res_files = [os.path.join(ROOT, f"results/c1_addenda/pair{p}/resnet_feature_degradation.json") for p in PAIRS]

wrn = load_json(os.path.join(ROOT, "results/wrn_eval/wrn_eval_summary.json"))["results"]
WRN_AA_RB = 62.76  # RobustBench-raporlu AA (yerel AA kosulmadi)

# --- Fig B1: robustluk cubuklari (WRN ayri blok) ----------------------------
fig, ax = plt.subplots(figsize=(5.0, 3.2))
metrics = ["Clean", "PGD-10", "AutoAttack"]
rn_vals = [m for m, _ in rn_bar]
rn_err = [s for _, s in rn_bar]
vt_vals = [m for m, _ in vt_bar]
vt_err = [s for _, s in vt_bar]
wrn_vals = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.03137"]["accuracy"], WRN_AA_RB]
x = np.arange(len(metrics), dtype=float)
w = 0.26
ax.bar(x - w / 2, rn_vals, w, yerr=rn_err, capsize=2.5, error_kw={"lw": 0.8},
       color=C_CNN, label="ResNet-18 (AT)")
ax.bar(x + w / 2, vt_vals, w, yerr=vt_err, capsize=2.5, error_kw={"lw": 0.8},
       color=C_VIT, label="ViT-Tiny (AT)")
# WRN: sagda ayri blok, gri + tarama + ayirici cizgi
xw = x + 3.4
ax.bar(xw, wrn_vals, w * 1.3, color=C_WRN, hatch="//", alpha=0.85,
       label="WRN-28-10 (reference$^{\\dagger}$)")
sep = (x[-1] + xw[0]) / 2
ax.axvline(sep, color="black", linewidth=0.8, linestyle=":")
for xi, v in zip(np.concatenate([x - w / 2, x + w / 2, xw]), rn_vals + vt_vals + wrn_vals):
    ax.text(xi, v + 1.8, f"{v:.1f}", ha="center", fontsize=7.5)
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
wrn_sweep = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.00784"]["accuracy"], wrn["pgd10_eps0.01569"]["accuracy"],
             wrn["pgd10_eps0.03137"]["accuracy"], wrn["pgd10_eps0.06275"]["accuracy"]]
xi = np.arange(len(EPS_GRID))
rn_m = np.array([m for m, _ in rn_sweep])
rn_s = np.array([s for _, s in rn_sweep])
vt_m = np.array([m for m, _ in vt_sweep])
vt_s = np.array([s for _, s in vt_sweep])
ax.fill_between(xi, rn_m - rn_s, rn_m + rn_s, color=C_CNN, alpha=0.18, linewidth=0)
ax.fill_between(xi, vt_m - vt_s, vt_m + vt_s, color=C_VIT, alpha=0.18, linewidth=0)
ax.plot(xi, rn_m, "o-", color=C_CNN, label="ResNet-18 (AT)")
ax.plot(xi, vt_m, "s-", color=C_VIT, label="ViT-Tiny (AT)")
ax.plot(xi, wrn_sweep, "^--", color=C_WRN, alpha=0.9, label="WRN-28-10 (reference$^{\\dagger}$)")
ax.axvline(3, color="black", linewidth=0.7, linestyle=":", alpha=0.6)
ax.text(3.05, 5, "$\\epsilon$=8/255", fontsize=8)
ax.set_xticks(xi)
ax.set_xticklabels(EPS_LBL)
ax.set_xlabel("Perturbation budget $\\epsilon$ ($L_\\infty$, PGD-10)")
ax.set_ylabel("Accuracy (%)")
ax.set_ylim(0, 95)
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(os.path.join(OUT, "fig_b2_eps_sweep.pdf"))
plt.close(fig)
print("fig_b2_eps_sweep.pdf")


# --- Fig B3: katman-bazli feature drift (ViT 12 blok vs ResNet 8 blok) ------
def vit_profile(d):
    att = load_json(os.path.join(d, "attention_summary.json"))
    layers = att["feature_analysis"] if "feature_analysis" in att else att["layers"]
    return [x["cosine_similarity"] for x in layers]


def res_profile(path):
    return [x["cosine_similarity"] for x in load_json(path)["feature_analysis"]]


vit_runs = np.array([vit_profile(d) for d in drift_vit_dirs], dtype=float)
res_runs = np.array([res_profile(p) for p in drift_res_files], dtype=float)
vit_cos, vit_std = vit_runs.mean(axis=0), (vit_runs.std(axis=0, ddof=1) if len(vit_runs) > 1 else np.zeros(vit_runs.shape[1]))
res_cos, res_std = res_runs.mean(axis=0), (res_runs.std(axis=0, ddof=1) if len(res_runs) > 1 else np.zeros(res_runs.shape[1]))
if args.source == "run3":  # tek kosu: bant CSV'deki parti-ici std'den
    csv_path = os.path.join(ROOT, "results/attention_analysis_run3/attention_feature_analysis.csv")
    with open(csv_path) as f:
        vit_std = np.array([float(r["cosine_similarity_std"]) for r in csv.DictReader(f)])
    res_std = np.array([x.get("cosine_similarity_std", 0.0)
                        for x in load_json(drift_res_files[0])["feature_analysis"]], dtype=float)

fig, ax = plt.subplots(figsize=(5.0, 3.0))
xv = np.linspace(0, 1, len(vit_cos))
xr = np.linspace(0, 1, len(res_cos))
ax.fill_between(xv, vit_cos - vit_std, vit_cos + vit_std, color=C_VIT, alpha=0.15, linewidth=0)
ax.fill_between(xr, res_cos - res_std, res_cos + res_std, color=C_CNN, alpha=0.15, linewidth=0)
ax.plot(xv, vit_cos, "o-", color=C_VIT, label="ViT-Tiny (12 blocks)")
ax.plot(xr, res_cos, "s--", color=C_CNN, label="ResNet-18 (8 residual blocks)")
imin = int(np.argmin(vit_cos))
ax.annotate(f"min {vit_cos[imin]:.3f} (block {imin + 1})\nthen slight recovery",
            xy=(xv[imin], vit_cos[imin]), xytext=(0.42, min(0.995, vit_cos.max())), fontsize=8,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.annotate(f"monotonic drop\nto {res_cos[-1]:.3f}", xy=(xr[-1], res_cos[-1]),
            xytext=(0.62, res_cos[-1] + 0.03), fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("Relative depth (block / total blocks)")
ax.set_ylabel("Clean-adversarial cosine similarity")
ax.legend(frameon=False, loc="lower left")
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(os.path.join(OUT, "fig_b3_feature_drift.pdf"))
plt.close(fig)
print("fig_b3_feature_drift.pdf")
print(f"TAMAM (kaynak: {args.source})")
