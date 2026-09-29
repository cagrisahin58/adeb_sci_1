#!/usr/bin/env python3
"""Nested conditioning sets figure (IEEE Access, Section 4.2).

Left: the four evaluation sets of the CNN->ViT direction drawn as nested
rectangles (schematic, NOT area-proportional). Right: the measured
asymmetry (CNN->ViT minus ViT->CNN, mean +- SD over seeds) of each
protocol on the same row. Bottom: spread and its decomposition.

QUARANTINE RULE: every number drawn comes from ONE file,
results/q1/fig_protokol_kumeleri_veri.json (produced by
scripts/fig_protokol_kumeleri_veri.py from results/c1_transfer/). No number
is typed into this script. The script refuses to draw if the file is
internally inconsistent.

Run from the repo root inside the container:
    docker exec -w /workspace adeb_eval python paper/figures/fig_protocol_sets.py
"""
import argparse
import datetime as dt
import hashlib
import io
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]
SET_NAMES = {
    "raw": "All test samples",
    "target_correct": "Target correct",
    "both_correct": "Both correct",
    "successful_source": "Successful source",
}
# IBM blue scale around the CNN colour #0F62FE of the journal figures
# (scripts/generate_journal_figs_c1.py: C_CNN = "#0f62fe"): blue 10/20/40/60.
FILLS = ["#EDF5FF", "#D0E2FF", "#78A9FF", "#0F62FE"]
TEXT_ON_FILL = ["#161616", "#161616", "#161616", "#FFFFFF"]
EDGE = "#393939"
INK = "#262626"
GREY = "#6F6F6F"
GUIDE = "#C6C6C6"
CM = 1 / 2.54


def fail(msg):
    sys.stderr.write(f"HATA / ERROR: {msg}\n")
    sys.exit(1)


def load_and_check(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    P = d.get("protokoller", {})
    for p in PROTOCOLS:
        if p not in P:
            fail(f"protocol '{p}' missing in {path}")
        for k in ("asimetri_ort", "asimetri_sd", "n_CNN_to_ViT", "n_ViT_to_CNN"):
            if k not in P[p]:
                fail(f"field protokoller.{p}.{k} missing")
    if d.get("ic_icelik_tutuyor") is not True:
        fail("ic_icelik_tutuyor is not true: the sets are not nested, figure would be false")
    for direc in ("n_CNN_to_ViT", "n_ViT_to_CNN"):
        ns = [P[p][direc] for p in PROTOCOLS]
        if any(a < b for a, b in zip(ns, ns[1:])):
            fail(f"{direc} not non-increasing along the nesting: {ns}")
    if P["both_correct"]["n_CNN_to_ViT"] != P["both_correct"]["n_ViT_to_CNN"]:
        fail("both_correct must be a shared set (same N in both directions)")
    # Decomposition terms must agree with the (rounded) protocol means.
    # The file computes them from UNROUNDED means, so allow one rounding unit
    # per operand (0.005 + 0.005) plus float slack.
    a = {p: P[p]["asimetri_ort"] for p in PROTOCOLS}
    A = d.get("ayrisim", {})
    expect = {
        "yayilim": max(a.values()) - min(a.values()),
        "ozdeslik_terimi_ham_eksi_hedef_dogru": a["raw"] - a["target_correct"],
        "farkli_estimand_bas_kaynak_eksi_ham": a["successful_source"] - a["raw"],
        "artik_takdir_her_ikisi_eksi_hedef": a["both_correct"] - a["target_correct"],
    }
    for k, v in expect.items():
        if k not in A:
            fail(f"field ayrisim.{k} missing")
        if abs(A[k] - v) > 0.0101:
            fail(f"ayrisim.{k} = {A[k]} disagrees with protocol means ({v:.4f})")
    # The pivot decomposition is only valid if raw lies between the extremes
    # that define the spread (target_correct = min, successful_source = max).
    if not (min(a, key=a.get) == "target_correct" and max(a, key=a.get) == "successful_source"):
        fail("spread is not target_correct -> successful_source; bottom-line wording would be wrong")
    return d


def git_info(root):
    def run(*args):
        try:
            return subprocess.run(["git", "-c", f"safe.directory={root}", "-C", str(root), *args],
                                  capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {
        "commit": run("rev-parse", "HEAD") or "unknown",
        "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
        "dirty_paths": [ln for ln in run("status", "--porcelain", "--",
                                         "results/q1/fig_protokol_kumeleri_veri.json",
                                         "scripts/fig_protokol_kumeleri_veri.py",
                                         "paper/figures/fig_protocol_sets.py",
                                         "results/c1_transfer/c1_transfer_summary.json").splitlines()],
    }


def keep_old(outdir, name):
    """Never overwrite a figure silently: move an existing version to _vN."""
    exts = [".pdf", ".png", ".kanit.json"]
    if not any((outdir / f"{name}{e}").exists() for e in exts):
        return None
    k = 1
    while any((outdir / f"{name}_v{k}{e}").exists() for e in exts):
        k += 1
    for e in exts:
        src = outdir / f"{name}{e}"
        if src.exists():
            shutil.move(str(src), str(outdir / f"{name}_v{k}{e}"))
    return f"{name}_v{k}"


def fmt_n(n):
    return f"{n:,}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default="results/q1/fig_protokol_kumeleri_veri.json")
    ap.add_argument("--outdir", default="paper/figures/final")
    ap.add_argument("--name", default="fig_protocol_sets")
    ap.add_argument("--width-cm", type=float, default=8.8, help="IEEE single column")
    ap.add_argument("--height-cm", type=float, default=7.2)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="unused (no randomness); kept for the log")
    args = ap.parse_args()

    root = Path.cwd()
    data_path = Path(args.data)
    if not data_path.is_file():
        fail(f"{data_path} not found (run from repo root; generate it with scripts/fig_protokol_kumeleri_veri.py)")
    d = load_and_check(data_path)
    P, A = d["protokoller"], d["ayrisim"]

    plt.rcParams.update({
        # Same family/sizes as scripts/generate_journal_figs_c1.py (current final figures).
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 8,
        "axes.labelsize": 8,
        "xtick.labelsize": 7.5,
        "axes.linewidth": 0.6,
        "axes.edgecolor": EDGE,
        "xtick.color": EDGE,
        "xtick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.hashsalt": str(args.seed),
    })

    W, H = args.width_cm * CM, args.height_cm * CM
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")

    # Manual layout (no bbox='tight') so the printed width is exactly the column.
    top, bottom_ax = 0.90, 0.30
    axL = fig.add_axes([0.020, bottom_ax, 0.500, top - bottom_ax])
    axR = fig.add_axes([0.575, bottom_ax, 0.400, top - bottom_ax], sharey=axL)

    # ---- geometry (layout units only; carries no data) ----
    band = 0.8                     # label band height per ring
    ymax = band * len(PROTOCOLS) + band  # outer box top; last band is the innermost box
    rows = {}
    x_in, y_in = 0.055, 0.13        # horizontal / bottom inset per nesting level
    nlev = len(PROTOCOLS)
    y_inner0 = ymax - nlev * band   # bottom of the innermost box (one band tall)
    y_outer0 = y_inner0 - (nlev - 1) * y_in
    for k, p in enumerate(PROTOCOLS):
        x0, x1 = k * x_in, 1 - k * x_in
        y1 = ymax - k * band
        y0 = y_outer0 + k * y_in if k < nlev - 1 else y_inner0
        axL.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=FILLS[k],
                                edgecolor=EDGE, linewidth=0.6, joinstyle="miter"))
        yc = y1 - band / 2 if k < len(PROTOCOLS) - 1 else (y0 + y1) / 2
        rows[p] = yc
        n = P[p]["n_CNN_to_ViT"]
        axL.text(0.5, yc + 0.13, SET_NAMES[p], ha="center", va="center",
                 fontsize=7.5, fontweight="bold", color=TEXT_ON_FILL[k])
        axL.text(0.5, yc - 0.17, f"N = {fmt_n(n)}", ha="center", va="center",
                 fontsize=7.5, color=TEXT_ON_FILL[k])
    axL.set_xlim(-0.005, 1.005)
    axL.set_ylim(y_outer0 - 0.02, ymax + 0.02)
    axL.axis("off")

    # ---- right: measured asymmetry per set, same rows ----
    means = [P[p]["asimetri_ort"] for p in PROTOCOLS]
    sds = [P[p]["asimetri_sd"] for p in PROTOCOLS]
    xmax = 5 * math.ceil(max(m + s for m, s in zip(means, sds)) / 5 + 0.2)
    xmin = min(0.0, 5 * math.floor(min(m - s for m, s in zip(means, sds)) / 5))
    for p in PROTOCOLS:
        y, m, s = rows[p], P[p]["asimetri_ort"], P[p]["asimetri_sd"]
        axR.plot([xmin, xmax], [y, y], color=GUIDE, lw=0.5, ls=(0, (1, 2)), zorder=1)
        axR.errorbar(m, y, xerr=s, fmt="o", ms=3.6, mfc=INK, mec=INK, ecolor=INK,
                     elinewidth=0.9, capsize=2.2, capthick=0.9, zorder=3)
        axR.annotate(f"{m:+.2f} pts", (m, y), xytext=(0, 4.5), textcoords="offset points",
                     ha="center", va="bottom", fontsize=7.5, color=INK)
        axR.annotate(f"±{s:.2f}", (m, y), xytext=(0, -4.5), textcoords="offset points",
                     ha="center", va="top", fontsize=6.5, color=GREY)
    axR.set_xlim(xmin, xmax)
    axR.set_xticks(range(int(xmin), int(xmax) + 1, 5))
    axR.tick_params(axis="y", left=False, labelleft=False)
    for sp in ("top", "right", "left"):
        axR.spines[sp].set_visible(False)
    axR.set_xlabel("CNN→ViT − ViT→CNN (pts)", labelpad=2)

    # column headers
    fig.text(0.020 + 0.250, top + 0.012, "Evaluation set, CNN→ViT", ha="center",
             va="bottom", fontsize=7.5, color=INK)
    fig.text(0.575 + 0.200, top + 0.012, "Measured asymmetry", ha="center",
             va="bottom", fontsize=7.5, color=INK)

    # ---- bottom lines: spread and its decomposition (all from 'ayrisim') ----
    lines = [
        f"Spread {A['yayilim']:.2f} pts ≈ {A['ozdeslik_terimi_ham_eksi_hedef_dogru']:.2f} "
        f"identity term (raw − target-correct)",
        f"+ {A['farkli_estimand_bas_kaynak_eksi_ham']:.2f} different estimand "
        f"(successful-source − raw);",
        f"{A['artik_takdir_her_ikisi_eksi_hedef']:.2f} pts remain between target-correct "
        f"and both-correct.",
    ]
    for i, ln in enumerate(lines):
        fig.text(0.020, 0.100 - i * 0.045, ln, ha="left", va="bottom", fontsize=7,
                 style="italic", color=INK)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    moved = keep_old(outdir, args.name)
    pdf, png = outdir / f"{args.name}.pdf", outdir / f"{args.name}.png"
    fig.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=args.dpi)
    plt.close(fig)

    raw = pdf.read_bytes()
    if b"/Type3" in raw:
        fail("Type 3 font in PDF")

    printed = {}
    for key, p in (("all", "raw"), ("target_correct", "target_correct"),
                   ("both_correct", "both_correct"), ("successful_source", "successful_source")):
        printed[f"N_{key}"] = {"deger": P[p]["n_CNN_to_ViT"], "gosterim": f"N = {fmt_n(P[p]['n_CNN_to_ViT'])}",
                               "kaynak": f"protokoller.{p}.n_CNN_to_ViT"}
        printed[f"asimetri_{key}"] = {"deger": P[p]["asimetri_ort"], "gosterim": f"{P[p]['asimetri_ort']:+.2f} pts",
                                      "kaynak": f"protokoller.{p}.asimetri_ort"}
        printed[f"sd_{key}"] = {"deger": P[p]["asimetri_sd"], "gosterim": f"±{P[p]['asimetri_sd']:.2f}",
                                "kaynak": f"protokoller.{p}.asimetri_sd"}
    for k in ("yayilim", "ozdeslik_terimi_ham_eksi_hedef_dogru",
              "farkli_estimand_bas_kaynak_eksi_ham", "artik_takdir_her_ikisi_eksi_hedef"):
        printed[k] = {"deger": A[k], "gosterim": f"{A[k]:.2f}", "kaynak": f"ayrisim.{k}"}

    kanit = {
        "sekil": args.name,
        "betik": "paper/figures/fig_protocol_sets.py",
        "komut": "docker exec -w /workspace adeb_eval python paper/figures/fig_protocol_sets.py",
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "veri": str(data_path),
        "veri_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "veri_ust_kaynagi": d.get("kaynak"),
        "git": git_info(root),
        "yerlesim": {
            "secim": "tek sutun",
            "genislik_cm": args.width_cm, "yukseklik_cm": args.height_cm, "dpi": args.dpi,
            "gerekce": ("IEEE Access column width 8.8 cm like every other transfer figure "
                        "(\\columnwidth). Asymmetry is read on a horizontal axis with one row per "
                        "set, because the values are not monotone in the nesting order and a "
                        "vertical value axis would need crossing leader lines."),
            "dikdortgenler": "schematic, NOT area-proportional to N",
            "font": "DejaVu Sans (as in scripts/generate_journal_figs_c1.py), pdf.fonttype 42",
            "dolgular": dict(zip(PROTOCOLS, FILLS)),
        },
        "basilan_sayilar": printed,
        "denetimler": [
            "ic_icelik_tutuyor == true",
            "N non-increasing along nesting, both directions",
            "both_correct N equal in both directions",
            "ayrisim terms == differences of protocol means within rounding (<=0.0101)",
            "spread endpoints are target_correct (min) and successful_source (max)",
            "no Type 3 font in PDF",
        ],
        "not_yuvarlama": (f"{A['ozdeslik_terimi_ham_eksi_hedef_dogru']:.2f} + "
                          f"{A['farkli_estimand_bas_kaynak_eksi_ham']:.2f} = "
                          f"{A['ozdeslik_terimi_ham_eksi_hedef_dogru'] + A['farkli_estimand_bas_kaynak_eksi_ham']:.2f} "
                          f"vs spread {A['yayilim']:.2f}: terms rounded from unrounded means, hence '≈'."),
        "eski_surum_tasindi": moved,
    }
    with io.open(outdir / f"{args.name}.kanit.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(kanit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"written: {pdf}\nwritten: {png}\nwritten: {outdir / (args.name + '.kanit.json')}")
    if moved:
        print(f"old version kept as {moved}.*")


if __name__ == "__main__":
    main()
