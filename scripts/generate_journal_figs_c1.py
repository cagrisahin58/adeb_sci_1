"""Dergi figurlerini C1 (3 tohum, sizinti duzeltmeli) artefaktlarindan uretir.

Cikti dosya adlari makaledeki \\includegraphics yollariyla ayni tutulur, boylece
metinde degisiklik gerekmez: paper/figures/final/<ad>.pdf

Uretilenler:
  fig1_robustness_comparison   temiz/PGD/AA cubuklari, 3 tohum hata cubuklu
  fig2_epsilon_sweep           epsilon taramasi, 3 kosum ort. +-1 SD hata cubugu
  fig3_transfer_heatmap        3x3 kosullu (hedef-dogru) transfer isi haritasi
  fig4b_gradient_distribution  ornek basina gradyan L2 normu ECDF'si (3 cift, log-x)
  fig4_gradient_comparison     ayni girdilerde gradyan enerji haritalari (cift 1)
  fig5_attention_comparison    CLS dikkat haritalari, tum satirlarda ortak olcek
  fig5b_attention_entropy      (a) entropi farki %95 GA + TOST marji, (b) CLS TV
  fig_tsne_features            penultimate t-SNE (her model KENDI beyaz kutusu)
  fig_adversarial_examples     ornek gorseller (en yakin komsu buyutme)

2026-10-04 (hakem paneli, mercek D Y3/Y4/Y5, kucuk 1/14/15): fig2, fig4,
fig5maps ve fig5b son sutun genisliginde (3.5 in) cizilir, olceklenmez;
yazi 8 pt, eksen etiketi 9 pt; CNN/ViT renkleri esit parlaklikta oldugu icin
her yerde isaretci + cizgi stili cifti (STY). Bu dort sekil PDF + PNG +
<ad>.kanit.json yazar (veri yolu, sha256, git, okunan degerler).

Kullanim: python scripts/generate_journal_figs_c1.py [--only ad1 ad2] [--lang tr]
"""
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys
from pathlib import Path

# CUBLAS_WORKSPACE_CONFIG, torch CUDA'yi baslatmadan ONCE kurulmalidir;
# use_deterministic_algorithms(True) bu degisken olmadan matmul'de hata verir.
os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.text  # noqa: E402,F401
import matplotlib.ticker  # noqa: E402,F401
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
        # 2026-10-04 eklenen etiketler
        "eps0": "0\n(clean)", "train_eps": "AT budget",
        "cnn2": "ResNet-18\n(AT)", "vit2": "ViT-Tiny\n(AT)",
        "ecdf_y": "Cumulative fraction", "layer": "Layer", "layer_x": "ViT layer",
        "gmap_cbar": "Gradient energy\n(per-map max = 1)",
        "attn_cbar": "Attention weight", "diff_cbar": r"Adv. $-$ clean",
        "dent_y": r"$\Delta$ entropy (nats)", "tost": "TOST margin",
        "tv_y": "Displacement (TV)", "ci95": "mean, 95% CI", "msd": r"mean $\pm$ SD",
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
        "eps0": "0\n(temiz)", "train_eps": "AT bütçesi",
        "cnn2": "ResNet-18\n(AT)", "vit2": "ViT-Tiny\n(AT)",
        "ecdf_y": "Birikimli oran", "layer": "Katman", "layer_x": "ViT katmanı",
        "gmap_cbar": "Gradyan enerjisi\n(harita maks. = 1)",
        "attn_cbar": "Dikkat ağırlığı", "diff_cbar": r"Çekişmeli $-$ temiz",
        "dent_y": r"$\Delta$ entropi (nat)", "tost": "TOST marjı",
        "tv_y": "Yer değiştirme (TV)", "ci95": "ortalama, %95 GA", "msd": r"ortalama $\pm$ SS",
    },
}
L = LANGS["en"]
LANG = "en"
CLASSES = L["classes"]
SCRIPT_REL = "scripts/generate_journal_figs_c1.py"

# Son sutun genisligi (IEEE Access): tek sutun 3.5 in, cift sutun 7.16 in.
# Yeni sekiller bu genislikte cizilir ve bbox kirpmasi yapilmaz, boylece
# \includegraphics[width=\columnwidth] olceklemez ve 8 pt yazi 8 pt basilir.
FIG_W1, FIG_W2 = 3.5, 7.16
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 9, "axes.titlesize": 9,
    "legend.fontsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "lines.linewidth": 1.2, "lines.markersize": 4,
    "figure.dpi": 150,
    # "standard": tam figsize. Eski sekiller (fig1, fig3, tsne, adv) kendi
    # savefig cagrilarinda bbox_inches="tight" ile eski davranisi korur.
    "savefig.bbox": "standard",
    # 2026-09-29: Type 3 font gomulmesin. Uretilen alti PDF'in hepsinde
    # /Type3 izi vardi; IEEE PDF eXpress bunu isaretler. 42 = TrueType.
    "pdf.fonttype": 42, "ps.fonttype": 42,
})
# CNN mavisi ile ViT kirmizisi esit goreli parlaklikta (0.160/0.160): gri
# tonlamada ayni gri. Her cizimde renk + isaretci + cizgi stili birlikte.
STY = {
    "cnn": {"color": C_CNN, "marker": "o", "ls": "-"},
    "vit": {"color": C_VIT, "marker": "s", "ls": "--"},
    "wrn": {"color": C_WRN, "marker": "^", "ls": ":"},
}
MIN_FONT_PT = 8.0


def _git_info():
    def run(*args):
        try:
            return subprocess.run(["git", "-c", f"safe.directory={ROOT}", "-C", str(ROOT), *args],
                                  capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {"commit": run("rev-parse", "HEAD") or "unknown",
            "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
            "betik_kirli": bool(run("status", "--porcelain", "--", SCRIPT_REL))}


def _sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def _min_font(fig):
    sizes = [t.get_fontsize() for t in fig.findobj(matplotlib.text.Text)
             if t.get_text().strip() and t.get_visible()]
    return min(sizes) if sizes else None


class _VirgulFormatter(matplotlib.ticker.ScalarFormatter):
    """TR metin ondalik virgul kullanir ("13,57", "4,9 nat"); eksen sayilari da."""

    def __call__(self, x, pos=None):
        return super().__call__(x, pos).replace(".", ",")


def _tr_virgul(fig):
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            if type(axis.get_major_formatter()) is matplotlib.ticker.ScalarFormatter:
                axis.set_major_formatter(_VirgulFormatter())


def _save(fig, name, sources, values, notes=None, extra_names=()):
    """PDF + PNG (300 dpi) + <ad>.kanit.json; Type 3 ve 8 pt alti yazi denetimi."""
    if LANG == "tr":
        _tr_virgul(fig)
    w, h = (float(v) for v in fig.get_size_inches())
    fmin = _min_font(fig)
    if fmin is not None and fmin < MIN_FONT_PT - 1e-6:
        raise SystemExit(f"{name}: {fmin} pt yazi var (< {MIN_FONT_PT})")
    pdf, png = OUT / f"{name}.pdf", OUT / f"{name}.png"
    fig.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=300)
    for extra in extra_names:
        fig.savefig(OUT / f"{extra}.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    if b"/Type3" in pdf.read_bytes():
        raise SystemExit(f"Type 3 font in {pdf}")
    kanit = {
        "sekil": name, "dil": LANG, "betik": SCRIPT_REL,
        "komut": "docker exec -w /workspace adeb_eval python " + " ".join([SCRIPT_REL] + sys.argv[1:]),
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "git": _git_info(), "cihaz": str(DEVICE), "tohum": FIG_SEED,
        "boyut_in": [w, h], "en_kucuk_yazi_pt": fmin,
        "kaynaklar": {rel: _sha(rel) for rel in sources},
        "degerler": values, "notlar": notes or [],
        "ek_ciktilar": [f"{e}.pdf" for e in extra_names],
    }
    with io.open(OUT / f"{name}.kanit.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(kanit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"{name}.pdf/.png/.kanit.json ({w:.2f}x{h:.2f} in, min {fmin} pt)")


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
    fig.savefig(OUT / "fig1_robustness_comparison.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig1_robustness_comparison.pdf")


# ---------------------------------------------------------------- fig 2 ------
def fig2():
    # Kategorik x ekseni (esit aralikli 0, 2, 4, 8, 16 /255) korunur; eps=0
    # noktasi PGD degil TEMIZ dogruluktur ve eksende "0 (clean)" diye yazar.
    grid = [0.0, 2 / 255, 4 / 255, 8 / 255, 16 / 255]
    lbl = [L["eps0"], "2/255", "4/255", "8/255", "16/255"]
    srcs = [f"results/c1_sweep/pair{p}/{m}/{m}_robustness_results.csv"
            for p in PAIRS for m in ("resnet18", "vit_tiny")] + ["results/wrn_eval/wrn_eval_summary.json"]
    sw = {p: {m: read_eval_csv(f"results/c1_sweep/pair{p}/{m}/{m}_robustness_results.csv")
              for m in ("resnet18", "vit_tiny")} for p in PAIRS}

    def per_pair(model):
        rows = [[sw[p][model][("clean", 0.0)] for p in PAIRS]]
        for e in grid[1:]:
            rows.append([sw[p][model][("pgd", round(e, 5))] for p in PAIRS])
        return np.array(rows)                       # (eps, pair)

    wrn = jload("results/wrn_eval/wrn_eval_summary.json")["results"]
    wkeys = ["clean", "pgd10_eps0.00784", "pgd10_eps0.01569", "pgd10_eps0.03137", "pgd10_eps0.06275"]
    wv = [wrn[k]["accuracy"] for k in wkeys]

    fig, ax = plt.subplots(figsize=(FIG_W1, 2.55), layout="constrained")
    xi = np.arange(len(grid))
    # eps=0 (temiz) ile PGD noktalarini ayiran ince cizgi; 8/255 egitim butcesi
    ax.axvline(0.5, color="#c6c6c6", lw=0.6, zorder=0)
    ax.axvline(3, color="black", lw=0.6, ls=(0, (1, 2)), zorder=0)
    vals = {}
    for model, key, lab in (("resnet18", "cnn", "ResNet-18 (AT)"), ("vit_tiny", "vit", "ViT-Tiny (AT)")):
        a = per_pair(model)
        m, s = a.mean(1), a.std(1, ddof=1)
        st = STY[key]
        ax.errorbar(xi, m, yerr=s, color=st["color"], marker=st["marker"], ls=st["ls"], ms=4,
                    capsize=2, elinewidth=0.8, capthick=0.8, label=lab, zorder=3)
        vals[model] = {"eps_etiket": ["0 (clean)", "2/255", "4/255", "8/255", "16/255"],
                       "tohum_degerleri": a.tolist(), "ortalama": m.tolist(), "sd_n-1": s.tolist(),
                       "en_buyuk_sd": float(s.max())}
    st = STY["wrn"]
    ax.plot(xi, wv, color=st["color"], marker=st["marker"], ls=st["ls"], ms=4, label=L["wrn"], zorder=2)
    vals["wrn_28_10"] = {"anahtarlar": wkeys, "deger": wv, "not": "tek checkpoint, SD yok"}
    vals["fark_cnn_eksi_vit"] = (np.array(vals["resnet18"]["ortalama"])
                                 - np.array(vals["vit_tiny"]["ortalama"])).round(4).tolist()
    ax.text(3.08, 2, L["train_eps"], fontsize=8, ha="left", va="bottom")
    ax.set_xticks(xi)
    ax.set_xticklabels(lbl)
    ax.set_xlim(-0.3, len(grid) - 0.7)
    ax.set_xlabel(L["eps_x"])
    ax.set_ylabel(L["acc"])
    ax.set_ylim(0, 95)
    h, lab_ = ax.get_legend_handles_labels()
    order = [lab_.index(n) for n in ("ResNet-18 (AT)", "ViT-Tiny (AT)", L["wrn"])]
    ax.legend([h[i] for i in order], [lab_[i] for i in order], loc="lower left", handlelength=2.6, borderaxespad=0.2,
              frameon=True, framealpha=1.0, facecolor="white", edgecolor="none")
    ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "fig2_epsilon_sweep", srcs, vals, notes=[
        "x ekseni kategorik (esit aralik), lineer epsilon degil",
        "eps=0 noktasi temiz dogruluk (CSV satiri Attack=clean, Epsilon=0)",
        "hata cubugu: 3 tohum cifti uzerinden +-1 SD (ddof=1); cogu nokta isaretciden dar",
        "tarama kosusu (results/c1_sweep) Tablo 1'in kosusundan ayridir; 8/255 noktasi Tablo 1 ile birebir ayni degildir",
    ])


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
    fig.savefig(OUT / "fig3_transfer_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig3_transfer_heatmap.pdf")


# ------------------------------------------------------------- fig 5b --------
C_DENT, C_TV = "#0f62fe", "#e66100"   # CVD-guvenli, farkli parlaklik (mavi/turuncu)


def fig5b():
    """(a) Delta entropi (cekismeli - temiz), 3 kosum ort. ve %95 GA (t, df=2),
    +-TOST marji; (b) CLS dikkat yer degistirmesi (TV), ort. +- SD.

    TOST marji (ARGS.tost_margin, varsayilan 0.05 nat) bir analiz parametresidir,
    sonuc dosyasinda kayitli degildir; degeri 04_experiments.tex'teki on-tanimli
    marjdan gelir ve kanit dosyasina parametre olarak yazilir."""
    from scipy import stats

    srcs = [f"results/c1_c4/pair{p}/c4_summary.json" for p in PAIRS]
    att = [jload(s)["vit"]["attention"] for s in srcs]
    ec = np.array([a["entropy_clean_mean"] for a in att])          # (run, layer)
    ea = np.array([a["entropy_adv_mean"] for a in att])
    ed = np.array([a["entropy_delta_mean"] for a in att])
    tv = np.array([a["displacement_mean"] for a in att])
    nrun, nl = ed.shape
    # Kendi icinde tutarlilik: delta = adv - clean (ayni orneklerin ortalamasi)
    gap = float(np.abs(ed - (ea - ec)).max())
    if gap > 1e-5:
        raise SystemExit(f"fig5b: entropy_delta_mean != adv - clean (en buyuk fark {gap:.2e})")
    x = np.arange(1, nl + 1)
    dm = ed.mean(0)
    dsd = ed.std(0, ddof=1)
    tcrit = float(stats.t.ppf(0.975, df=nrun - 1))
    half = tcrit * dsd / np.sqrt(nrun)
    tm, tsd = tv.mean(0), tv.std(0, ddof=1)
    marg = float(ARGS.tost_margin)

    fig, (axa, axb) = plt.subplots(2, 1, figsize=(FIG_W1, 3.6), sharex=True, layout="constrained")
    axa.axhline(0, color="#8d8d8d", lw=0.6, zorder=0)
    for yv in (-marg, marg):
        axa.axhline(yv, color="black", lw=0.8, ls=(0, (4, 2)), zorder=1)
    axa.errorbar(x, dm, yerr=half, color=C_DENT, marker="o", ls="-", ms=3.5, capsize=2,
                 elinewidth=0.8, capthick=0.8, label=L["ci95"], zorder=3)
    axa.plot([], [], color="black", lw=0.8, ls=(0, (4, 2)), label=L["tost"])
    lim = 1.6 * marg
    axa.set_ylim(-lim, lim)
    axa.set_ylabel(L["dent_y"])
    axa.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.0),
               handlelength=2.4, columnspacing=1.2)
    axa.spines[["top", "right"]].set_visible(False)
    axa.set_title("(a)", loc="left", fontsize=9, fontweight="bold", pad=2)

    axb.errorbar(x, tm, yerr=tsd, color=C_TV, marker="s", ls="--", ms=3.5, capsize=2,
                 elinewidth=0.8, capthick=0.8, label=L["msd"], zorder=3)
    axb.set_ylim(0, None)
    axb.set_ylabel(L["tv_y"])
    axb.set_xlabel(L["layer_x"])
    axb.set_xticks(x)
    axb.legend(frameon=False, loc="upper left", handlelength=2.4)
    axb.spines[["top", "right"]].set_visible(False)
    axb.set_title("(b)", loc="left", fontsize=9, fontweight="bold", pad=2)

    lay_clean, lay_adv = ec.mean(0), ea.mean(0)
    vals = {
        "anahtarlar": {"entropi_temiz": "vit.attention.entropy_clean_mean",
                       "entropi_cekismeli": "vit.attention.entropy_adv_mean",
                       "delta": "vit.attention.entropy_delta_mean",
                       "tv": "vit.attention.displacement_mean"},
        "kosum_sayisi": nrun, "n_ornek_kosum_basina": [jload(s)["n_samples"] for s in srcs],
        "delta_kosum": ed.tolist(), "delta_ort": dm.tolist(), "delta_sd": dsd.tolist(),
        "delta_ga95_t_df2": [[float(a), float(b)] for a, b in zip(dm - half, dm + half)],
        "t_kritik": tcrit, "en_buyuk_mutlak_delta_ort": float(np.abs(dm).max()),
        "en_buyuk_mutlak_ga_ucu": float(np.abs(np.concatenate([dm - half, dm + half])).max()),
        "tum_ga_marj_icinde": bool(np.all(np.abs(np.concatenate([dm - half, dm + half])) < marg)),
        "tost_marji_parametre": marg,
        "tv_kosum": tv.tolist(), "tv_ort": tm.tolist(), "tv_sd": tsd.tolist(),
        "katman_ortalamasi_entropi_temiz": lay_clean.tolist(),
        "katman_ortalamasi_entropi_cekismeli": lay_adv.tolist(),
        "genel_ortalama_temiz": float(lay_clean.mean()),
        "genel_ortalama_cekismeli": float(lay_adv.mean()),
        "katman_ortalamasi_temiz_aralik": [float(lay_clean.min()), float(lay_clean.max())],
    }
    _save(fig, "fig5b_attention_entropy", srcs, vals, notes=[
        "(a) %95 GA kosum duzeyinde t araligi (df=2); TOST %5 duzeyinde %90 GA'ya karsilik gelir, bu yuzden %95 GA daha tutucudur",
        "TOST p degerleri bu sekilden ya da herhangi bir sonuc dosyasindan okunmaz; metindeki p=0.006 icin artefakt bulunamadi",
        "(b) TV = 0.5 * sum |a_adv - a_clean| CLS satiri uzerinde (experiments/c1_c4_attention_features.py:191), ornek ortalamasi; hata cubugu kosumlar arasi SD",
    ])


# ------------------------------------------------------- gradyan figurleri ---
def _grads(model, images, labels):
    """ORNEK BASINA kaybin girdi gradyani.

    2026-10-04 duzeltmesi (mercek D, Y3): eskiden nn.CrossEntropyLoss() (parti
    ORTALAMASI) kullaniliyordu; 50'lik partide her gradyan 1/50 olcekleniyor ve
    eksendeki "per-sample" ifadesi yanlis oluyordu. reduction="sum" ile her
    ornegin gradyani yalniz kendi kaybinin gradyanidir (eval kipinde ornekler
    arasi etkilesim yok), src/analysis/gradient_analysis.py:37 ile ayni tanim."""
    images = images.clone().requires_grad_(True)
    loss = nn.CrossEntropyLoss(reduction="sum")(model(images), labels)
    return torch.autograd.grad(loss, images)[0].detach()


GRAD_N, GRAD_BS = 500, 50   # results/c1_gradient ile ayni: ilk 500 test ornegi, 50'lik parti
N_MAPS = 4


def _plot_gradmaps(imgs, gr, gv):
    """3 x N_MAPS izgara (girdi / ResNet / ViT) + gradyan satirlarini kaplayan
    ortak 0-1 renk cubugu. Elle yerlesim (inc): satirlar esit aralikli kalir."""
    # gap_r 0.10: 9 pt dikey satir etiketleri ("ResNet-18", "ViT-Tiny") birbirine degmesin
    W, msz, gap, gap_r, left, bot, top = FIG_W1, 0.54, 0.05, 0.10, 0.42, 0.05, 0.05
    H = bot + 3 * msz + 2 * gap_r + top
    fig = plt.figure(figsize=(W, H))
    axes = np.empty((3, N_MAPS), dtype=object)
    for r in range(3):
        y = bot + (2 - r) * (msz + gap_r)
        for k in range(N_MAPS):
            axes[r, k] = fig.add_axes([(left + k * (msz + gap)) / W, y / H, msz / W, msz / H])
    x_cb = left + N_MAPS * msz + (N_MAPS - 1) * gap + 0.06
    cax = fig.add_axes([x_cb / W, bot / H, 0.07 / W, (2 * msz + gap_r) / H])
    maxima = {"resnet18": [], "vit_tiny": []}
    im = None
    for k in range(N_MAPS):
        axes[0, k].imshow(imgs[k].permute(1, 2, 0).numpy(), interpolation="nearest")
        for r, g, m in ((1, gr, "resnet18"), (2, gv, "vit_tiny")):
            e = (g[k] ** 2).sum(0).numpy()          # piksel basina kanallar toplami g^2
            maxima[m].append(float(e.max()))
            e = e / (e.max() + 1e-12)               # harita basina maks. = 1
            im = axes[r, k].imshow(e, cmap="inferno", vmin=0, vmax=1, interpolation="nearest")
        for r in range(3):
            axes[r, k].set_xticks([])
            axes[r, k].set_yticks([])
    for r, lab in enumerate([L["input"], L["cnn2"], L["vit2"]]):
        axes[r, 0].set_ylabel(lab, fontsize=9)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label(L["gmap_cbar"], fontsize=8)
    cb.set_ticks([0, 0.5, 1])
    cb.ax.tick_params(labelsize=8, width=0.6)
    return fig, maxima


def fig4():
    _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=GRAD_BS)
    norms = {"resnet18": {}, "vit_tiny": {}}
    first = None
    for p in PAIRS:
        rn, vt = c1_model("resnet18", p), c1_model("vit_tiny", p)
        acc = {"resnet18": [], "vit_tiny": []}
        seen = 0
        for images, labels in loader:
            if seen >= GRAD_N:
                break
            keep = min(labels.size(0), GRAD_N - seen)
            images, labels = images[:keep].to(DEVICE), labels[:keep].to(DEVICE)
            gr, gv = _grads(rn, images, labels), _grads(vt, images, labels)
            acc["resnet18"].append(gr.flatten(1).norm(dim=1).cpu().numpy())
            acc["vit_tiny"].append(gv.flatten(1).norm(dim=1).cpu().numpy())
            if p == 1 and first is None:
                first = (images[:N_MAPS].cpu(), labels[:N_MAPS].cpu(), gr[:N_MAPS].cpu(), gv[:N_MAPS].cpu())
            seen += keep
        for m in acc:
            norms[m][p] = np.concatenate(acc[m])
        del rn, vt
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # --- kaynakla karsilastirma: results/c1_gradient/pair*/gradient_summary.json
    gsrc = [f"results/c1_gradient/pair{p}/gradient_summary.json" for p in PAIRS]
    keymap = {"resnet18": "ResNet18_AT", "vit_tiny": "ViT_Tiny_AT"}
    karsi = {}
    uyusmazlik = []
    for p, src in zip(PAIRS, gsrc):
        g = jload(src)
        for m, k in keymap.items():
            ref = float(g["statistics"][k]["l2_norm_mean"])
            got = float(norms[m][p].mean())
            rel = abs(got - ref) / ref
            karsi[f"pair{p}/{m}"] = {"hesaplanan_ort": got, "kaynak_l2_norm_mean": ref,
                                     "goreli_fark": rel, "n": int(norms[m][p].size),
                                     "kaynak_n": g["statistics"][k].get("n_samples"),
                                     "medyan": float(np.median(norms[m][p])),
                                     "min": float(norms[m][p].min()), "max": float(norms[m][p].max())}
            if rel > 1e-3:
                uyusmazlik.append(f"pair{p}/{m}: {got:.5f} vs {ref:.5f} (goreli {rel:.2e})")
    if uyusmazlik:
        print("UYARI fig4b: hesaplanan ortalamalar gradient_summary.json ile uyusmuyor:\n  "
              + "\n  ".join(uyusmazlik))

    fig, ax = plt.subplots(figsize=(FIG_W1, 2.45), layout="constrained")
    for m, key, lab in (("resnet18", "cnn", "ResNet-18 (AT)"), ("vit_tiny", "vit", "ViT-Tiny (AT)")):
        st = STY[key]
        for i, p in enumerate(PAIRS):
            v = np.sort(norms[m][p])
            y = np.arange(1, v.size + 1) / v.size
            ax.step(v, y, where="post", color=st["color"], ls=st["ls"], lw=1.0,
                    label=lab if i == 0 else None)
    ax.set_xscale("log")
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(L["gnorm_x"])
    ax.set_ylabel(L["ecdf_y"])
    ax.legend(frameon=False, loc="upper left", handlelength=2.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, which="major", axis="x", color="#e0e0e0", lw=0.5)
    _save(fig, "fig4b_gradient_distribution",
          gsrc + [f"models/c1/{d}/{'resnet18' if d.startswith('resnet') else 'vit_tiny'}/adv/adversarial_training/best.pth"
                  for d in ("resnet18_s1001", "resnet18_s1002", "resnet18_s1003",
                            "vit_tiny_s2001", "vit_tiny_s2002", "vit_tiny_s2003")],
          {"kayip": "CrossEntropyLoss(reduction='sum'), ornek basina gradyan",
           "orneklem": f"ilk {GRAD_N} CIFAR-10 test ornegi (shuffle=False), parti {GRAD_BS}, her cift icin ayni",
           "ciftler": PAIRS, "karsilastirma": karsi, "uyusmazliklar": uyusmazlik,
           "esik_goreli": 1e-3},
          notes=["her cizgi bir tohum cifti (3 cift x 2 mimari); lejantta sayi yok",
                 "ECDF basamak fonksiyonu, log-x"])

    # --- gradyan enerji haritalari (cift 1, ilk dort test goruntusu) ---------
    imgs, labs, gr, gv = first
    fig, maxima = _plot_gradmaps(imgs, gr, gv)
    _save(fig, "fig4_gradient_comparison",
          ["models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth",
           "models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"],
          {"cift": 1, "goruntu_indeksleri": list(range(N_MAPS)),
           "etiketler": [int(v) for v in labs], "siniflar": [LANGS["en"]["classes"][int(v)] for v in labs],
           "enerji": "sum_c g_c(x,y)^2, g = ornek basina CE kaybinin girdi gradyani",
           "olcek": "her harita kendi maksimumuna bolunur (0-1); renk cubugu ortak 0-1",
           "harita_maksimumlari_ham": maxima},
          notes=["haritalar arasi mutlak buyukluk KARSILASTIRILAMAZ (harita basina normalize)"],
          extra_names=("fig4a_gradient_visualization",))


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
    fig.savefig(OUT / "fig_tsne_features.pdf", bbox_inches="tight")
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
    fig.savefig(OUT / "fig_adversarial_examples.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig_adversarial_examples.pdf")


def _plot_attnmaps(cm, am, layers, vmax, dmax):
    """Satir = katman; sutunlar temiz / cekismeli / fark. Ortak vmax ve ortak
    simetrik +-dmax; iki renk cubugu ucer satirin tam boyunda, hizmet ettikleri
    sutunlarin sagina. Elle yerlesim (inc): constrained layout tek sutunluk fark
    renk cubugunu kisa birakiyordu."""
    W, msz, gap_c, gap_r, top_t, bot, left = FIG_W1, 0.53, 0.05, 0.06, 0.22, 0.05, 0.36
    H = top_t + 3 * msz + 2 * gap_r + bot
    x_map = [left, left + msz + gap_c, None]
    x_cb1 = x_map[1] + msz + gap_c
    x_map[2] = x_cb1 + 0.07 + 0.60          # cb1 tik etiketleri + etiketi icin bosluk
    x_cb2 = x_map[2] + msz + gap_c
    fig = plt.figure(figsize=(W, H))
    axes = np.empty((len(layers), 3), dtype=object)
    for r in range(len(layers)):
        y = bot + (len(layers) - 1 - r) * (msz + gap_r)
        for c in range(3):
            axes[r, c] = fig.add_axes([x_map[c] / W, y / H, msz / W, msz / H])
    y_lo, y_hi = bot / H, (bot + 3 * msz + 2 * gap_r) / H
    cax1 = fig.add_axes([x_cb1 / W, y_lo, 0.07 / W, y_hi - y_lo])
    cax2 = fig.add_axes([x_cb2 / W, y_lo, 0.07 / W, y_hi - y_lo])
    ims = {}
    for r, l in enumerate(layers):
        d = am[l] - cm[l]
        for c, (arr, title, kw) in enumerate([
            (cm[l], L["att_clean"], {"cmap": "viridis", "vmin": 0, "vmax": vmax}),
            (am[l], L["att_adv"], {"cmap": "viridis", "vmin": 0, "vmax": vmax}),
            (d, L["att_diff"], {"cmap": "coolwarm", "vmin": -dmax, "vmax": dmax}),
        ]):
            ims[c] = axes[r, c].imshow(arr, interpolation="nearest", **kw)
            if r == 0:
                axes[r, c].set_title(title, fontsize=9)
            axes[r, c].set_xticks([])
            axes[r, c].set_yticks([])
        # iki satirli etiket: "Katman 12" 9 pt'de harita yuksekligine sigmiyor
        axes[r, 0].set_ylabel(f"{L['layer']}\n{l + 1}", fontsize=9, linespacing=1.3)
    cb1 = fig.colorbar(ims[1], cax=cax1)
    cb2 = fig.colorbar(ims[2], cax=cax2)
    for cb, lab in ((cb1, L["attn_cbar"]), (cb2, L["diff_cbar"])):
        cb.set_label(lab, fontsize=8, labelpad=2)
        cb.ax.tick_params(labelsize=8, width=0.6, length=2)
        cb.ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(3))
    return fig


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
    with torch.no_grad():
        pred_c, pred_a = int(vit(images[:1]).argmax(1)), int(vit(adv[:1]).argmax(1))

    # 2026-10-04 (mercek D, Y4): satir basina ayri olcek yerine TUM satirlar
    # icin ortak vmax (temiz/cekismeli) ve ortak simetrik +-dmax (fark).
    # Boylece satirlar arasi doygunluk karsilastirilabilir.
    layers = [0, 5, 11]
    vmax = float(max(cm[layers].max(), am[layers].max()))
    dmax = float(np.abs(am[layers] - cm[layers]).max())
    fig = _plot_attnmaps(cm, am, layers, vmax, dmax)
    tv_img = [float(0.5 * np.abs(am[l] - cm[l]).sum()) for l in range(cm.shape[0])]
    _save(fig, "fig5_attention_comparison",
          ["models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"],
          {"cift": 1, "goruntu_indeksi": 0, "etiket": int(labels[0]),
           "sinif": LANGS["en"]["classes"][int(labels[0])],
           "tahmin_temiz": LANGS["en"]["classes"][pred_c], "tahmin_cekismeli": LANGS["en"]["classes"][pred_a],
           "saldiri": "PGD-10, eps=8/255, alpha=2/255, 16'lik ilk test partisi uzerinde, tohum 42",
           "katmanlar_1tabanli": [l + 1 for l in layers],
           "ortak_vmax_dikkat": vmax, "ortak_dmax_fark": dmax,
           "satir_maks_dikkat": [float(max(cm[l].max(), am[l].max())) for l in layers],
           "satir_maks_mutlak_fark": [float(np.abs(am[l] - cm[l]).max()) for l in layers],
           "bu_goruntu_tv_tum_katmanlar": tv_img},
          notes=["tek goruntu (ilk test ornegi), ornek degil illustrasyon",
                 "cls_maps: CLS satiri, basliklar uzerinden ortalama, 14x14 yama izgarasi (vit.get_attention_maps)"])

    fig, axes = plt.subplots(1, 2, figsize=(3.4, 1.9))
    vmax = max(cm[11].max(), am[11].max())
    for ax, arr, title in ((axes[0], cm[11], "clean"), (axes[1], am[11], "adversarial")):
        ax.imshow(arr, cmap="viridis", vmin=0, vmax=vmax, interpolation="nearest")
        ax.set_title(title, fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(OUT / "fig5a_attention_comparison.pdf", bbox_inches="tight")
    plt.close(fig)
    print("fig5a_attention_comparison.pdf (makalede kullanilmiyor)")


ALL = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig5b": fig5b,
       "fig4": fig4, "tsne": figtsne, "adv": figadv, "fig5maps": fig5maps}
ARGS = argparse.Namespace(tost_margin=0.05)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="+", default=list(ALL))
    ap.add_argument("--lang", choices=["en", "tr"], default="en")
    ap.add_argument("--tost-margin", type=float, default=0.05,
                    help="fig5b esdegerlik marji (nat); metindeki on-tanimli +-0.05, sonuc dosyasinda yok")
    args = ap.parse_args()
    ARGS = args
    L = LANGS[args.lang]
    LANG = args.lang
    CLASSES = L["classes"]
    if args.lang != "en":
        OUT = ROOT / f"paper/figures/final_{args.lang}"
        OUT.mkdir(parents=True, exist_ok=True)
    for name in args.only:
        _tohumla()          # her figur ayni durumdan basasin
        ALL[name]()
    print(f"TAMAM (lang={args.lang}, out={OUT})")
