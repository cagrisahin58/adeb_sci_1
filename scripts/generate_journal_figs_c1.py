"""Dergi figurlerini C1 (3 tohum, sizinti duzeltmeli) artefaktlarindan uretir.

Cikti dosya adlari makaledeki \\includegraphics yollariyla ayni tutulur, boylece
metinde degisiklik gerekmez: paper/figures/final/<ad>.pdf

Uretilenler:
  fig1_robustness_comparison   temiz/PGD/AA cubuklari, 3 tohum hata cubuklu
  fig2_epsilon_sweep           epsilon taramasi, +-1 std bantli
  fig3_transfer_heatmap        3x3 kosullu (hedef-dogru) transfer isi haritasi
  fig4b_gradient_distribution  ornek basina gradyan L2 dagilimi
  fig4_gradient_comparison     ayni girdilerde gradyan enerji haritalari
  fig5b_attention_entropy      katman basina CLS attention entropisi (temiz/adv)
  fig_tsne_features            penultimate t-SNE (her model KENDI beyaz kutusu)
  fig_adversarial_examples     ornek gorseller (en yakin komsu buyutme)

Kullanim: python scripts/generate_journal_figs_c1.py [--only ad1 ad2]
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

# CUBLAS_WORKSPACE_CONFIG, torch CUDA'yi baslatmadan ONCE kurulmalidir;
# use_deterministic_algorithms(True) bu degisken olmadan matmul'de hata verir.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
import torch.nn as nn  # noqa: E402

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
OUT = ROOT / "paper/figures/final"
OUT.mkdir(parents=True, exist_ok=True)

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

# Tohum sabitlemesi: figtsne/figadv/fig5maps PGD kosuyor ve PGD rastgele
# baslangicli. Bu olmadan her uretim farkli PDF veriyordu (bkz. yeniden uretim
# gurultusu commit'leri) ve Yontem 3.7'deki "seed 42 ile yeniden uretilebilir"
# cumlesi kod tarafindan desteklenmiyordu.
FIG_SEED = 42


def _tohumla(seed: int = FIG_SEED) -> None:
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    # Tohum TEK BASINA yetmiyor: cekirdek secimi de belirlenimsiz. Olculdu --
    # bu satir olmadan ayni tohumla iki uretim farkli PDF veriyor.
    torch.use_deterministic_algorithms(True)


PAIRS = [1, 2, 3]
C_CNN, C_VIT, C_WRN = "#0f62fe", "#da1e28", "#8d8d8d"
EPS8 = round(8 / 255, 5)

# --lang tr: Turkce etiketli varyantlar paper/figures/final_tr/ altina uretilir.
LANGS = {
    "en": {
        "classes": ["airplane", "automobile", "bird", "cat", "deer", "dog",
                    "frog", "horse", "ship", "truck"],
        "metrics": ["Clean", "PGD-10", "AutoAttack"],
        "acc": "Accuracy (%)", "matched": "Matched AT pair", "ref": "Reference",
        "wrn": "WRN-28-10 (reference)",
        "eps_x": r"Perturbation budget $\epsilon$ ($L_\infty$, PGD-10)",
        "target": "Target", "source": "Source",
        "cond_cbar": "Conditioned fooling rate (%)",
        "blk_x": "Transformer block", "ent_y": "CLS attention entropy (nats)",
        "clean": "Clean", "adv": "Adversarial",
        "gnorm_x": r"Per-sample input-gradient $L_2$ norm", "count": "Count",
        "input": "Input", "mean": "mean",
        "cap_clean": "clean", "cap_pert": r"perturbation ($\times$10)",
        "cap_adv": "adversarial",
        "att_clean": "clean", "att_adv": "adversarial", "att_diff": "difference",
        "block": "block",
    },
    "tr": {
        "classes": ["uçak", "otomobil", "kuş", "kedi", "geyik", "köpek",
                    "kurbağa", "at", "gemi", "kamyon"],
        "metrics": ["Temiz", "PGD-10", "AutoAttack"],
        "acc": "Doğruluk (%)", "matched": "Eşleşmiş AT çifti", "ref": "Referans",
        "wrn": "WRN-28-10 (referans)",
        "eps_x": r"Pertürbasyon bütçesi $\epsilon$ ($L_\infty$, PGD-10)",
        "target": "Hedef", "source": "Kaynak",
        "cond_cbar": "Koşullu yanıltma oranı (%)",
        "blk_x": "Dönüştürücü bloğu", "ent_y": "CLS dikkat entropisi (nat)",
        "clean": "Temiz", "adv": "Çekişmeli",
        "gnorm_x": r"Örnek başına girdi gradyanı $L_2$ normu", "count": "Adet",
        "input": "Girdi", "mean": "ort.",
        "cap_clean": "temiz", "cap_pert": r"pertürbasyon ($\times$10)",
        "cap_adv": "çekişmeli",
        "att_clean": "temiz", "att_adv": "çekişmeli", "att_diff": "fark",
        "block": "blok",
    },
}
L = LANGS["en"]
CLASSES = L["classes"]

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 10, "axes.titlesize": 10,
    "legend.fontsize": 8, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "figure.dpi": 150, "savefig.bbox": "tight",
})


def jload(rel):
    with open(ROOT / rel, encoding="utf-8") as fh:
        return json.load(fh)


def read_eval_csv(rel):
    vals = {}
    with open(ROOT / rel) as fh:
        for row in csv.DictReader(fh):
            vals[(row["Attack"], round(float(row["Epsilon"]), 5))] = float(row["Accuracy"])
    return vals


def ms(v):
    a = np.asarray(v, dtype=float)
    return float(a.mean()), (float(a.std(ddof=1)) if a.size > 1 else 0.0)


def c1_model(kind, pair, stage="adv"):
    rs, vs = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}[pair]
    if kind == "resnet18":
        base = f"models/c1/resnet18_s{rs}/resnet18"
    else:
        base = f"models/c1/vit_tiny_s{vs}/vit_tiny"
    p = f"{base}/adv/adversarial_training/best.pth" if stage == "adv" else f"{base}/clean/best.pth"
    m = ModelRegistry.get(kind)
    load_model_weights(m, p, DEVICE)
    return m.to(DEVICE).eval()


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# ---------------------------------------------------------------- fig 1 ------
def fig1():
    ev = {p: {m: read_eval_csv(f"results/c1_eval/pair{p}/{m}/{m}_robustness_results.csv")
              for m in ("resnet18", "vit_tiny")} for p in PAIRS}
    aa = {}
    for p in PAIRS:
        d = jload(f"results/c1_seeds/pair{p}/autoattack_summary.json")
        for e in d["results"]:
            key = "resnet18" if "ResNet18" in json.dumps(e) else "vit_tiny"
            aa.setdefault(key, []).append(e["robust_accuracy"])
    wrn = jload("results/wrn_eval/wrn_eval_summary.json")["results"]

    metrics = L["metrics"]
    rn = [ms([ev[p]["resnet18"][("clean", 0.0)] for p in PAIRS]),
          ms([ev[p]["resnet18"][("pgd", EPS8)] for p in PAIRS]), ms(aa["resnet18"])]
    vt = [ms([ev[p]["vit_tiny"][("clean", 0.0)] for p in PAIRS]),
          ms([ev[p]["vit_tiny"][("pgd", EPS8)] for p in PAIRS]), ms(aa["vit_tiny"])]
    wv = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.03137"]["accuracy"], 62.76]

    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    x = np.arange(3, dtype=float)
    w = 0.26
    ax.bar(x - w / 2, [m for m, _ in rn], w, yerr=[s for _, s in rn], capsize=2.5,
           error_kw={"lw": 0.8}, color=C_CNN, label="ResNet-18 (AT)")
    ax.bar(x + w / 2, [m for m, _ in vt], w, yerr=[s for _, s in vt], capsize=2.5,
           error_kw={"lw": 0.8}, color=C_VIT, label="ViT-Tiny (AT)")
    xw = x + 3.4
    ax.bar(xw, wv, w * 1.3, color=C_WRN, hatch="//", alpha=0.85, label=L["wrn"])
    ax.axvline((x[-1] + xw[0]) / 2, color="black", lw=0.8, ls=":")
    for xi, v in zip(np.concatenate([x - w / 2, x + w / 2, xw]),
                     [m for m, _ in rn] + [m for m, _ in vt] + wv):
        ax.text(xi, v + 1.8, f"{v:.1f}", ha="center", fontsize=7)
    ax.set_xticks(np.concatenate([x, xw]))
    ax.set_xticklabels(metrics + metrics, fontsize=8)
    ax.set_ylabel(L["acc"])
    ax.set_ylim(0, 100)
    ax.text(float(np.mean(x)), 95, L["matched"], ha="center", fontsize=8, fontweight="bold")
    ax.text(float(np.mean(xw)), 95, L["ref"], ha="center", fontsize=8, color="#444")
    ax.legend(loc="center", bbox_to_anchor=(0.5, -0.24), ncol=3, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "fig1_robustness_comparison.pdf")
    plt.close(fig)
    print("fig1_robustness_comparison.pdf")


# ---------------------------------------------------------------- fig 2 ------
def fig2():
    grid = [0.0, 2 / 255, 4 / 255, 8 / 255, 16 / 255]
    lbl = ["0", "2/255", "4/255", "8/255", "16/255"]
    sw = {p: {m: read_eval_csv(f"results/c1_sweep/pair{p}/{m}/{m}_robustness_results.csv")
              for m in ("resnet18", "vit_tiny")} for p in PAIRS}

    def series(model):
        out = [ms([sw[p][model][("clean", 0.0)] for p in PAIRS])]
        for e in grid[1:]:
            out.append(ms([sw[p][model][("pgd", round(e, 5))] for p in PAIRS]))
        return np.array([m for m, _ in out]), np.array([s for _, s in out])

    wrn = jload("results/wrn_eval/wrn_eval_summary.json")["results"]
    wv = [wrn["clean"]["accuracy"], wrn["pgd10_eps0.00784"]["accuracy"], wrn["pgd10_eps0.01569"]["accuracy"],
          wrn["pgd10_eps0.03137"]["accuracy"], wrn["pgd10_eps0.06275"]["accuracy"]]

    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    xi = np.arange(len(grid))
    for model, color, marker, lab in (("resnet18", C_CNN, "o-", "ResNet-18 (AT)"),
                                      ("vit_tiny", C_VIT, "s-", "ViT-Tiny (AT)")):
        m, s = series(model)
        ax.fill_between(xi, m - s, m + s, color=color, alpha=0.18, lw=0)
        ax.plot(xi, m, marker, color=color, label=lab)
    ax.plot(xi, wv, "^--", color=C_WRN, alpha=0.9, label=L["wrn"])
    ax.axvline(3, color="black", lw=0.7, ls=":", alpha=0.6)
    ax.text(3.05, 5, r"$\epsilon$=8/255", fontsize=8)
    ax.set_xticks(xi)
    ax.set_xticklabels(lbl)
    ax.set_xlabel(L["eps_x"])
    ax.set_ylabel(L["acc"])
    ax.set_ylim(0, 95)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "fig2_epsilon_sweep.pdf")
    plt.close(fig)
    print("fig2_epsilon_sweep.pdf")


# ---------------------------------------------------------------- fig 3 ------
def fig3():
    names = ["ResNet18_AT", "ViT_Tiny_AT", "WRN_28_10"]
    short = ["ResNet-18", "ViT-Tiny", "WRN-28-10"]
    M = np.zeros((3, 3))
    for i, s in enumerate(names):
        for j, t in enumerate(names):
            vals = [jload(f"results/c1_c3/pair{p}/transfer_matrix.json")["results"][f"{s}->{t}"]["cond_fooling"]
                    for p in PAIRS]
            M[i, j] = float(np.mean(vals))
    fig, ax = plt.subplots(figsize=(4.4, 3.6))
    im = ax.imshow(M, cmap="YlOrRd", vmin=0, vmax=60)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{M[i, j]:.1f}", ha="center", va="center",
                    color="white" if M[i, j] > 35 else "black", fontsize=10,
                    fontweight="bold" if i == j else "normal")
    ax.set_xticks(range(3), short, fontsize=8)
    ax.set_yticks(range(3), short, fontsize=8)
    ax.set_xlabel(L["target"])
    ax.set_ylabel(L["source"])
    fig.colorbar(im, ax=ax, shrink=0.85, label=L["cond_cbar"])
    fig.savefig(OUT / "fig3_transfer_heatmap.pdf")
    plt.close(fig)
    print("fig3_transfer_heatmap.pdf")


# ------------------------------------------------------------- fig 5b --------
def fig5b():
    ec = np.array([jload(f"results/c1_c4/pair{p}/c4_summary.json")["vit"]["attention"]["entropy_clean_mean"]
                   for p in PAIRS])
    ea = np.array([jload(f"results/c1_c4/pair{p}/c4_summary.json")["vit"]["attention"]["entropy_adv_mean"]
                   for p in PAIRS])
    x = np.arange(1, ec.shape[1] + 1)
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    for arr, color, lab, marker in ((ec, "#1a7f37", L["clean"], "o-"), (ea, C_VIT, L["adv"], "s--")):
        m, s = arr.mean(0), arr.std(0, ddof=1)
        ax.fill_between(x, m - s, m + s, color=color, alpha=0.18, lw=0)
        ax.plot(x, m, marker, color=color, label=lab, ms=4)
    ax.set_xlabel(L["blk_x"])
    ax.set_ylabel(L["ent_y"])
    ax.set_xticks(x)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "fig5b_attention_entropy.pdf")
    plt.close(fig)
    print("fig5b_attention_entropy.pdf")


# ------------------------------------------------------- gradyan figurleri ---
def _grads(model, images, labels):
    images = images.clone().requires_grad_(True)
    loss = nn.CrossEntropyLoss()(model(images), labels)
    return torch.autograd.grad(loss, images)[0].detach()


def fig4():
    rn, vt = c1_model("resnet18", 1), c1_model("vit_tiny", 1)
    _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=50)
    norms = {"ResNet-18 (AT)": [], "ViT-Tiny (AT)": []}
    seen = 0
    first = None
    for images, labels in loader:
        if seen >= 500:
            break
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        gr, gv = _grads(rn, images, labels), _grads(vt, images, labels)
        norms["ResNet-18 (AT)"].append(gr.flatten(1).norm(dim=1).cpu().numpy())
        norms["ViT-Tiny (AT)"].append(gv.flatten(1).norm(dim=1).cpu().numpy())
        if first is None:
            first = (images[:4].cpu(), gr[:4].cpu(), gv[:4].cpu())
        seen += labels.size(0)

    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    for lab, color in (("ResNet-18 (AT)", C_CNN), ("ViT-Tiny (AT)", C_VIT)):
        v = np.concatenate(norms[lab])
        ax.hist(v, bins=40, alpha=0.55, color=color, label=f"{lab} ({L[chr(39)+chr(39) if False else chr(109)+chr(101)+chr(97)+chr(110)]} {v.mean():.3f})")
    ax.set_xlabel(L["gnorm_x"])
    ax.set_ylabel(L["count"])
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(OUT / "fig4b_gradient_distribution.pdf")
    plt.close(fig)
    print("fig4b_gradient_distribution.pdf")

    imgs, gr, gv = first
    fig, axes = plt.subplots(3, 4, figsize=(5.4, 4.2))
    for k in range(4):
        axes[0, k].imshow(imgs[k].permute(1, 2, 0).numpy(), interpolation="nearest")
        for r, g, color in ((1, gr, "CNN"), (2, gv, "ViT")):
            e = (g[k] ** 2).sum(0).numpy()
            e = e / (e.max() + 1e-12)
            axes[r, k].imshow(e, cmap="inferno", interpolation="nearest")
        for r in range(3):
            axes[r, k].set_xticks([])
            axes[r, k].set_yticks([])
    for r, lab in enumerate([L["input"], "ResNet-18 (AT)", "ViT-Tiny (AT)"]):
        axes[r, 0].set_ylabel(lab, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig4_gradient_comparison.pdf")
    fig.savefig(OUT / "fig4a_gradient_visualization.pdf")
    plt.close(fig)
    print("fig4_gradient_comparison.pdf + fig4a_gradient_visualization.pdf")


# --------------------------------------------------------------- t-SNE -------
def figtsne():
    from sklearn.manifold import TSNE

    rn, vt = c1_model("resnet18", 1), c1_model("vit_tiny", 1)
    _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=100)
    xs, ys = [], []
    for images, labels in loader:
        xs.append(images)
        ys.append(labels)
        if sum(t.shape[0] for t in xs) >= 500:
            break
    images = torch.cat(xs)[:500].to(DEVICE)
    labels = torch.cat(ys)[:500].to(DEVICE)

    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.1))
    for ax, model, name in ((axes[0], rn, "ResNet-18 (AT)"), (axes[1], vt, "ViT-Tiny (AT)")):
        adv = PGDAttack(model, eps=8 / 255, alpha=2 / 255, steps=10)(images, labels)
        feats = []
        for batch in (images, adv):
            out = []
            with torch.no_grad():
                for i in range(0, batch.shape[0], 100):
                    f = model.forward_features(batch[i:i + 100]) if hasattr(model, "forward_features") \
                        else model(batch[i:i + 100])
                    out.append(f.flatten(1).cpu())
            feats.append(torch.cat(out).numpy())
        emb = TSNE(n_components=2, random_state=42, init="pca", perplexity=30).fit_transform(
            np.concatenate(feats))
        n = feats[0].shape[0]
        lab = labels.cpu().numpy()
        ax.scatter(emb[n:, 0], emb[n:, 1], c=lab, cmap="tab10", s=6, marker="^", alpha=0.45)
        ax.scatter(emb[:n, 0], emb[:n, 1], c=lab, cmap="tab10", s=6, marker="o", alpha=0.9)
        ax.set_title(name, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(OUT / "fig_tsne_features.pdf")
    plt.close(fig)
    print("fig_tsne_features.pdf")


# ------------------------------------------------------ adversarial ornek ----
def figadv():
    _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=200)
    images, labels = next(iter(loader))
    images, labels = images.to(DEVICE), labels.to(DEVICE)
    rows = []
    for kind, name in (("resnet18", "ResNet-18 (AT)"), ("vit_tiny", "ViT-Tiny (AT)")):
        model = c1_model(kind, 1)
        adv = PGDAttack(model, eps=8 / 255, alpha=2 / 255, steps=10)(images, labels)
        with torch.no_grad():
            pc, pa = model(images).argmax(1), model(adv).argmax(1)
        idx = int(torch.nonzero((pc == labels) & (pa != labels))[0])
        rows.append((name, images[idx].cpu(), adv[idx].cpu(), int(pc[idx]), int(pa[idx])))

    fig, axes = plt.subplots(len(rows), 3, figsize=(4.6, 3.2))
    for r, (name, clean, adv, pc, pa) in enumerate(rows):
        pert = (adv - clean)
        pert = (pert - pert.min()) / (pert.max() - pert.min() + 1e-12)
        for c, (img, title) in enumerate([
            (clean, f"{L[chr(99)+chr(97)+chr(112)+chr(95)+chr(99)+chr(108)+chr(101)+chr(97)+chr(110)]}: {L[chr(99)+chr(108)+chr(97)+chr(115)+chr(115)+chr(101)+chr(115)][pc]}"),
            (pert, L["cap_pert"]),
            (adv, f"{L['cap_adv']}: {L['classes'][pa]}"),
        ]):
            axes[r, c].imshow(img.permute(1, 2, 0).numpy(), interpolation="nearest")
            axes[r, c].set_title(title, fontsize=7)
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
        axes[r, 0].set_ylabel(name, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig_adversarial_examples.pdf")
    plt.close(fig)
    print("fig_adversarial_examples.pdf")


# ------------------------------------------------------ attention haritalari -
def fig5maps():
    vit = c1_model("vit_tiny", 1)
    if not hasattr(vit, "get_attention_maps"):
        raise AttributeError("vit_tiny modelinde get_attention_maps yok")
    _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=16)
    images, labels = next(iter(loader))
    images, labels = images.to(DEVICE), labels.to(DEVICE)
    adv = PGDAttack(vit, eps=8 / 255, alpha=2 / 255, steps=10)(images, labels)
    with torch.no_grad():
        ca, aa = vit.get_attention_maps(images), vit.get_attention_maps(adv)
    cm, am = ca["cls_maps"][0].cpu().numpy(), aa["cls_maps"][0].cpu().numpy()

    layers = [0, 5, 11]
    fig, axes = plt.subplots(len(layers), 3, figsize=(4.6, 4.4))
    for r, l in enumerate(layers):
        d = am[l] - cm[l]
        vmax = max(cm[l].max(), am[l].max())
        for c, (arr, title, kw) in enumerate([
            (cm[l], L["att_clean"], {"cmap": "viridis", "vmin": 0, "vmax": vmax}),
            (am[l], L["att_adv"], {"cmap": "viridis", "vmin": 0, "vmax": vmax}),
            (d, L["att_diff"], {"cmap": "coolwarm", "vmin": -np.abs(d).max(), "vmax": np.abs(d).max()}),
        ]):
            axes[r, c].imshow(arr, interpolation="nearest", **kw)
            if r == 0:
                axes[r, c].set_title(title, fontsize=8)
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
        axes[r, 0].set_ylabel(f"{L['block']} {l + 1}", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "fig5_attention_comparison.pdf")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.9))
    vmax = max(cm[11].max(), am[11].max())
    for ax, arr, title in ((axes[0], cm[11], "clean"), (axes[1], am[11], "adversarial")):
        ax.imshow(arr, cmap="viridis", vmin=0, vmax=vmax, interpolation="nearest")
        ax.set_title(title, fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(OUT / "fig5a_attention_comparison.pdf")
    plt.close(fig)
    print("fig5_attention_comparison.pdf + fig5a_attention_comparison.pdf")


ALL = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig5b": fig5b,
       "fig4": fig4, "tsne": figtsne, "adv": figadv, "fig5maps": fig5maps}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="+", default=list(ALL))
    ap.add_argument("--lang", choices=["en", "tr"], default="en")
    args = ap.parse_args()
    L = LANGS[args.lang]
    CLASSES = L["classes"]
    if args.lang != "en":
        OUT = ROOT / f"paper/figures/final_{args.lang}"
        OUT.mkdir(parents=True, exist_ok=True)
    for name in args.only:
        _tohumla()          # her figur ayni durumdan basasin
        ALL[name]()
    print(f"TAMAM (lang={args.lang}, out={OUT})")
