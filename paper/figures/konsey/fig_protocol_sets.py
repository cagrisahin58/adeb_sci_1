#!/usr/bin/env python3
"""Nested conditioning sets figure (IEEE Access, Section 4.2), version 5 (2026-10-31, council copy).

Change log (degisiklik notu):
- 2026-10-31, hakem konseyi m16 (birlesik.md section 3; mercek_sunum bulgu 14): this file is a copy of
  paper/figures/fig_protocol_sets.py (v4, 2026-10-04) placed in paper/figures/konsey/, because the
  council-round figure agent may write only there. Changes against v4:
  * connector labels use the manuscript's terms: "endorsed pair" -> "marginal subsets removed"
    (04_experiments, "these marginal subsets differ five-fold in size"), "different estimand" ->
    "source robustness" (05_discussion, "a second driver tied to the source's own
    robustness"); "identity term" unchanged (eq:raw_identity). Karar: the report's
    "source-robustness term" does not fit the C-D gap at 8 pt at any height up to 12 cm (checked
    by the placement search), so the shorter "source robustness" is used, same meaning;
  * panel (a) key "N: CNN->ViT / ViT->CNN" -> "N (CNN->ViT / ViT->CNN)", which reads as one N with
    two directions instead of two N's for the CNN->ViT boxes;
  * every printed number (four protocol means and SDs, N in both directions, three seed values per
    protocol, three connector distances, spread) is compared with results/C1_REFERANS_FOYU.md
    (lines 53-56, 60, 212, 214, 215, 805-807) through konsey_ortak.Foy before drawing;
  * two more line-break variants for connector labels (at the last space; one word per line), needed
    by the longer terms; the failure message names the connector that could not be placed;
  * height 10.5 cm (v4: 10.0 cm), the smallest at which the new labels are placed without overlap;
  * output to paper/figures/konsey (EN only; --lang tr is refused here, the TR mirror stays with
    paper/figures/fig_protocol_sets.py and paper/figures/final_tr);
  * width kept at 8.89 cm (3.5 in): at 8.53 cm (columnwidth) the right header does not fit beside
    "(b)" at 8 pt; printed at x0.959, so the smallest text is 7.7 pt on the page.
  The manuscript still includes ../figures/final/fig_protocol_sets.pdf (04_experiments.tex); the
  author switches the path to ../figures/konsey/fig_protocol_sets.pdf to use this version.

Version 4 notes follow.

Left: the four evaluation sets drawn as nested boxes (schematic, NOT
area-proportional; the nesting is the CNN->ViT one, the ViT->CNN sets nest in
the same order). Each box carries N for both directions where they differ.
Right: per protocol, the three seed-pair asymmetries (open circles), their
mean (short vertical bar) and SD. Version 4 (reviewer B2): the bracket stack
above the axis (9.21 + 5.79, which read as a partition of the spread although
the 3.91 interval lies inside 9.21) is removed. Instead THREE PAIRWISE
DISTANCES between adjacent rows are drawn as mean-bar-to-mean-bar connectors:
A-B target-correct -> raw (identity term), B-C target-correct -> both-correct
(endorsed pair), C-D both-correct -> successful-source (different estimand).
Rows are lettered A-D on both panels.
--lang tr writes the Turkish variant to paper/figures/final_tr.

QUARANTINE RULE: every result number drawn comes from ONE file,
results/q1/fig_protokol_kumeleri_veri.json (scripts/fig_protokol_kumeleri_veri.py).
The only other file read is the LaTeX .aux, for the equation NUMBER of
eq:raw_identity (a cross-reference, not a result), so the bracket label follows
the manuscript's numbering instead of a hand-typed one.

Run from the repo root inside the container:
    docker exec -w /workspace adeb_eval python paper/figures/fig_protocol_sets.py
"""
import argparse
import datetime as dt
import hashlib
import io
import itertools
import json
import math
import re
import shutil
import statistics
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from matplotlib.transforms import Bbox  # noqa: E402
import matplotlib.text  # noqa: E402,F401

PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]
# 2026-10-04 (hakem paneli, mercek D kucuk 2 / yeniden uretim 12): satir
# harfleri A-D iki panelde de; sol-sag eslesmesi dikey konuma birakilmaz.
ROW_LETTERS = ["A", "B", "C", "D"]
TXT = {
    "en": {
        "sets": {"raw": ["All test samples (raw)"], "target_correct": ["Target (ViT) correct"],
                 "both_correct": ["Both correct"], "successful_source": ["Successful source", "(CNN white-box)"]},
        "n_key": "N (CNN→ViT / ViT→CNN)",
        "hdr_left": "Evaluation set\n(CNN→ViT boxes)",
        "hdr_right": "Measured asymmetry\n(mean ± SD, {k} seed pairs)",
        "xlabel": "CNN→ViT − ViT→CNN (pts)", "unit": "pts",
        "identity": "identity term", "estimand": "source robustness", "endorsed": "marginal subsets removed",
        "spread": "Spread {v} pts (successful-source minus target-correct)",
        "dec": ".", "thou": ",", "aux": "paper/manuscript/main.aux", "outdir": "paper/figures/konsey",
    },
    "tr": {
        "sets": {"raw": ["Tüm örnekler (koşulsuz)"], "target_correct": ["Hedef (ViT) doğru"],
                 "both_correct": ["Her ikisi doğru"], "successful_source": ["Başarılı kaynak", "(CNN beyaz kutu)"]},
        "n_key": "N: CNN→ViT / ViT→CNN",
        "hdr_left": "Değerlendirme kümesi\n(CNN→ViT kutuları)",
        "hdr_right": "Ölçülen asimetri\n(ort. ± SS, {k} tohum çifti)",
        "xlabel": "CNN→ViT − ViT→CNN (puan)", "unit": "puan",
        "identity": "özdeşlik terimi", "estimand": "farklı nicelik", "endorsed": "onaylanan ikili",
        "spread": "Yayılım {v} puan (başarılı kaynak eksi hedef doğru)",
        "dec": ",", "thou": ".", "aux": "paper/manuscript_tr/main.aux", "outdir": "paper/figures/final_tr",
    },
}
LANG = "en"


def loc_num(s):
    """Dile gore ondalik/binlik ayiraci: TR '13,57' ve '10.000'."""
    t = TXT[LANG]
    if t["dec"] == ".":
        return s
    return s.replace(",", "\0").replace(".", t["dec"]).replace("\0", t["thou"])
# IBM blue scale around the CNN colour #0F62FE of the journal figures
# (scripts/generate_journal_figs_c1.py: C_CNN = "#0f62fe"): blue 10/20/40/60.
FILLS = ["#EDF5FF", "#D0E2FF", "#78A9FF", "#0F62FE"]
TEXT_ON_FILL = ["#161616", "#161616", "#161616", "#FFFFFF"]
EDGE = "#393939"
INK = "#262626"
GUIDE = "#C6C6C6"
CM = 1 / 2.54
MIN_FONT = 8.0   # 2026-10-04: dergi sekillerinin tumunde en kucuk yazi 8 pt (onceden 7)


def fail(msg):
    sys.stderr.write(f"HATA / ERROR: {msg}\n")
    sys.exit(1)


def load_and_check(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    P = d.get("protokoller", {})
    for k in ("kaynak", "kaynak_sha256", "ayrisim", "ic_icelik_tutuyor"):
        if k not in d:
            fail(f"top-level field '{k}' missing in {path}")
    for p in PROTOCOLS:
        if p not in P:
            fail(f"protocol '{p}' missing in {path}")
        for k in ("asimetri_ort", "asimetri_sd", "asimetri_tohum_degerleri",
                  "n_CNN_to_ViT", "n_ViT_to_CNN"):
            if k not in P[p]:
                fail(f"field protokoller.{p}.{k} missing")
    if d["ic_icelik_tutuyor"] is not True:
        fail("ic_icelik_tutuyor is not true: the sets are not nested, figure would be false")
    for direc in ("n_CNN_to_ViT", "n_ViT_to_CNN"):
        ns = [P[p][direc] for p in PROTOCOLS]
        if any(a < b for a, b in zip(ns, ns[1:])):
            fail(f"{direc} not non-increasing along the nesting: {ns}")
    for p in ("raw", "both_correct"):
        if P[p]["n_CNN_to_ViT"] != P[p]["n_ViT_to_CNN"]:
            fail(f"{p} must be the same set in both directions (single N is printed)")
    # Seed values must reproduce the stored mean and SD (n-1).
    nseed = {len(P[p]["asimetri_tohum_degerleri"]) for p in PROTOCOLS}
    if len(nseed) != 1 or min(nseed) < 2:
        fail(f"seed value lists differ in length or are too short: {nseed}")
    for p in PROTOCOLS:
        v = P[p]["asimetri_tohum_degerleri"]
        if abs(statistics.mean(v) - P[p]["asimetri_ort"]) > 0.0051:
            fail(f"{p}: mean of seed values {statistics.mean(v):.4f} != asimetri_ort {P[p]['asimetri_ort']}")
        if abs(statistics.stdev(v) - P[p]["asimetri_sd"]) > 0.0051:
            fail(f"{p}: SD(n-1) of seed values {statistics.stdev(v):.4f} != asimetri_sd {P[p]['asimetri_sd']}")
    # Decomposition terms vs (rounded) protocol means: one rounding unit per operand.
    a = {p: P[p]["asimetri_ort"] for p in PROTOCOLS}
    A = d["ayrisim"]
    expect = {
        "yayilim": max(a.values()) - min(a.values()),
        "ozdeslik_terimi_ham_eksi_hedef_dogru": a["raw"] - a["target_correct"],
        "farkli_estimand_bas_kaynak_eksi_ham": a["successful_source"] - a["raw"],
        "artik_takdir_her_ikisi_eksi_hedef": a["both_correct"] - a["target_correct"],
        "bas_kaynak_eksi_her_ikisi_dogru": a["successful_source"] - a["both_correct"],
    }
    for k, v in expect.items():
        if k not in A:
            fail(f"field ayrisim.{k} missing")
        if abs(A[k] - v) > 0.0101:
            fail(f"ayrisim.{k} = {A[k]} disagrees with protocol means ({v:.4f})")
    if "tohum_basina_ortalama_yayilim" not in A:
        fail("field ayrisim.tohum_basina_ortalama_yayilim missing")
    # Per-seed spread recomputed from the seed values (seed order is shared).
    k_seeds = min(nseed)
    per_seed = [max(P[p]["asimetri_tohum_degerleri"][i] for p in PROTOCOLS)
                - min(P[p]["asimetri_tohum_degerleri"][i] for p in PROTOCOLS) for i in range(k_seeds)]
    if abs(statistics.mean(per_seed) - A["tohum_basina_ortalama_yayilim"]) > 0.0051:
        fail(f"per-seed spread from seed values {statistics.mean(per_seed):.4f} != "
             f"tohum_basina_ortalama_yayilim {A['tohum_basina_ortalama_yayilim']}")
    if A["tohum_basina_ortalama_yayilim"] != A["yayilim"]:
        fail("tohum_basina_ortalama_yayilim != yayilim: 'Spread' would be ambiguous")
    # v4: the bottom line names the spread's endpoints ("successful-source minus
    # target-correct"); fail if the data no longer has them as max and min.
    if max(a, key=a.get) != "successful_source" or min(a, key=a.get) != "target_correct":
        fail(f"spread endpoints changed ({a}); the bottom line would name the wrong protocols")
    # The three connectors print UNSIGNED distances between adjacent rows; each
    # printed difference must be positive or the label would drop a sign.
    for k in ("ozdeslik_terimi_ham_eksi_hedef_dogru", "artik_takdir_her_ikisi_eksi_hedef",
              "bas_kaynak_eksi_her_ikisi_dogru"):
        if not A[k] > 0:
            fail(f"ayrisim.{k} = {A[k]} is not positive; connector label would misstate it")
    return d, k_seeds, per_seed


def eq_number(aux, key):
    if not aux.is_file():
        fail(f"{aux} not found: compile the manuscript first (needed for the equation number)")
    m = re.search(r"\\newlabel\{" + re.escape(key) + r"\}\{\{([^}]*)\}", aux.read_text(encoding="utf-8", errors="replace"))
    if not m:
        fail(f"label {key} not in {aux}")
    return m.group(1)


def git_info(root, paths):
    def run(*args):
        try:
            return subprocess.run(["git", "-c", f"safe.directory={root}", "-C", str(root), *args],
                                  capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {
        "commit": run("rev-parse", "HEAD") or "unknown",
        "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
        "dirty_paths": run("status", "--porcelain", "--", *paths).splitlines(),
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
    return loc_num(f"{n:,}")


def n_label(P, p):
    a, b = P[p]["n_CNN_to_ViT"], P[p]["n_ViT_to_CNN"]
    return f"N = {fmt_n(a)}" if a == b else f"N = {fmt_n(a)} / {fmt_n(b)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default="results/q1/fig_protokol_kumeleri_veri.json")
    ap.add_argument("--lang", choices=sorted(TXT), default="en",
                    help="en -> paper/figures/final, tr -> paper/figures/final_tr (decimal comma)")
    ap.add_argument("--aux", default=None, help="default: the language's main.aux")
    ap.add_argument("--eq-key", default="eq:raw_identity")
    ap.add_argument("--outdir", default=None, help="default: by --lang")
    ap.add_argument("--name", default="fig_protocol_sets")
    ap.add_argument("--width-cm", type=float, default=8.89, help="3.5 in; printed at x0.959 in columnwidth (header needs the width)")
    ap.add_argument("--height-cm", type=float, default=10.5)  # 2026-10-31: v4 10.0; longer connector labels
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="unused (no randomness); kept for the log")
    args = ap.parse_args()
    global LANG
    LANG = args.lang
    if LANG != "en":
        fail("council copy writes the EN figure only; the TR mirror is paper/figures/fig_protocol_sets.py --lang tr")
    T = TXT[LANG]
    args.aux = args.aux or T["aux"]
    args.outdir = args.outdir or T["outdir"]

    root = Path.cwd()
    data_path = Path(args.data)
    if not data_path.is_file():
        fail(f"{data_path} not found (run from repo root; generate it with scripts/fig_protokol_kumeleri_veri.py)")
    d, k_seeds, per_seed = load_and_check(data_path)
    P, A = d["protokoller"], d["ayrisim"]
    # 2026-10-31: every printed number vs the reference sheet (konsey_ortak.Foy), before drawing
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import konsey_ortak as KO
    foy = KO.Foy()
    FOY_ROW = {"raw": (53, "| Kosulsuz (ham) |"), "target_correct": (54, "| Hedef dogru |"),
               "both_correct": (55, "| Her ikisi dogru |"), "successful_source": (56, "| Basarili kaynak |")}
    for p_ in PROTOCOLS:
        ln, anc = FOY_ROW[p_]
        foy.kontrol(f"{p_}: asimetri_ort", P[p_]["asimetri_ort"], ln, anc, 2)
        foy.kontrol(f"{p_}: asimetri_sd", P[p_]["asimetri_sd"], ln, anc, 2)
        foy.kontrol(f"{p_}: n_CNN_to_ViT", P[p_]["n_CNN_to_ViT"], ln, anc, 0)
        foy.kontrol(f"{p_}: n_ViT_to_CNN", P[p_]["n_ViT_to_CNN"], ln, anc, 0)
        for i_, v_ in enumerate(P[p_]["asimetri_tohum_degerleri"]):
            foy.kontrol(f"{p_}: seed pair {i_ + 1}", v_, 805 + i_, f"| cift {i_ + 1} |", 2)
    foy.metin("per-pair table columns", "ort.$\\pm$SD", 808, "| ort.$\\pm$SD |")
    foy.kontrol("yayilim", A["yayilim"], 60, "Protokol yayilimi", 2)
    foy.kontrol("ozdeslik_terimi_ham_eksi_hedef_dogru", A["ozdeslik_terimi_ham_eksi_hedef_dogru"], 212, "| raw - tc", 2)
    foy.kontrol("artik_takdir_her_ikisi_eksi_hedef", A["artik_takdir_her_ikisi_eksi_hedef"], 214, "| bc - tc", 2)
    foy.kontrol("bas_kaynak_eksi_her_ikisi_dogru", A["bas_kaynak_eksi_her_ikisi_dogru"], 215, "| ss - bc", 2)
    foy_sonuc = foy.bitir()
    aux = Path(args.aux)
    eqn = eq_number(aux, args.eq_key)

    plt.rcParams.update({
        # Same family as scripts/generate_journal_figs_c1.py (current final figures).
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 8.0,
        "axes.labelsize": 9.0,
        "xtick.labelsize": 8.0,
        "ytick.labelsize": 8.0,
        "axes.linewidth": 0.6,
        "axes.edgecolor": EDGE,
        "xtick.color": EDGE,
        "xtick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.hashsalt": str(args.seed),
    })
    # 2026-10-04: every text >= 8 pt at the final column width (was 7-7.5 pt).
    FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR, FS_ROW, FS_PANEL = 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 9.0
    assert min(FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR, FS_ROW, FS_PANEL) >= MIN_FONT

    W, H = args.width_cm * CM, args.height_cm * CM
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")

    # ---- geometry in layout units (carries no data) ----
    band = 1.0                              # label band of rings 0..2 (row letter + two lines)
    inner_h = 1.2                           # innermost box: row letter + three lines
    nlev = len(PROTOCOLS)
    ymax = band * (nlev - 1) + inner_h + 0.0
    x_in, y_in = 0.04, 0.12
    y_inner0 = ymax - (nlev - 1) * band - inner_h
    y_outer0 = y_inner0 - (nlev - 1) * y_in
    # v4: no bracket stack above the axis any more; only the direction key sits there.
    y_top = ymax + 0.45

    ax_bottom, ax_top = 0.165, 0.905   # v4: 0.885 -> 0.905 (header ends at ~0.91)
    axL = fig.add_axes([0.015, ax_bottom, 0.475, ax_top - ax_bottom])
    axR = fig.add_axes([0.535, ax_bottom, 0.440, ax_top - ax_bottom], sharey=axL)

    rows = {}
    for k, p in enumerate(PROTOCOLS):
        x0, x1 = k * x_in, 1 - k * x_in
        y1 = ymax - k * band
        y0 = y_outer0 + k * y_in if k < nlev - 1 else y_inner0
        axL.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=FILLS[k],
                                edgecolor=EDGE, linewidth=0.6, joinstyle="miter"))
        yc = y1 - band / 2 - 0.07 if k < nlev - 1 else y0 + (y1 - y0 - 0.2) / 2
        rows[p] = yc
        lines = T["sets"][p] + [n_label(P, p)]
        step = 0.235
        y_first = yc + step * (len(lines) - 1) / 2
        for i, ln in enumerate(lines):
            is_n = ln.startswith("N = ")
            axL.text(0.5, y_first - i * step, ln, ha="center", va="center",
                     fontsize=FS_N if is_n else FS_NAME,
                     fontweight="normal" if (is_n or ln.startswith("(")) else "bold",
                     color=TEXT_ON_FILL[k])
        # row letter in the top-left corner of the set's own band
        axL.text(x0 + 0.012, y1 - 0.035, ROW_LETTERS[k], ha="left", va="top",
                 fontsize=FS_ROW, fontweight="bold", color=TEXT_ON_FILL[k])
    axL.set_xlim(-0.005, 1.005)
    axL.set_ylim(y_outer0 - 0.02, y_top)
    axL.axis("off")
    axL.text(0.5, ymax + 0.10, T["n_key"], ha="center", va="bottom", fontsize=FS_N, color=INK)
    # column headers at figure level, above both panels; panel letters at the left of each
    fig.text(0.015 + 0.475 / 2 + 0.025, 0.985, T["hdr_left"], ha="center", va="top",
             fontsize=FS_NAME, color=INK, linespacing=1.1)
    fig.text(0.004, 0.985, "(a)", ha="left", va="top", fontsize=FS_PANEL, fontweight="bold", color=INK)
    fig.text(0.500, 0.985, "(b)", ha="left", va="top", fontsize=FS_PANEL, fontweight="bold", color=INK)

    # ---- right: seed values, mean, SD ----
    allv = [v for p in PROTOCOLS for v in P[p]["asimetri_tohum_degerleri"]]
    xmax = 5 * math.ceil(max(allv) / 5 + 0.2)
    xmin = min(0.0, 5 * math.floor(min(allv) / 5))
    offs = [(i - (k_seeds - 1) / 2) * 0.11 for i in range(k_seeds)]  # visibility only
    half_bar = 0.2
    a = {p: P[p]["asimetri_ort"] for p in PROTOCOLS}
    for p in PROTOCOLS:
        y, m = rows[p], a[p]
        axR.plot([xmin, xmax], [y, y], color=GUIDE, lw=0.5, ls=(0, (1, 2)), zorder=1)
        for dy, v in zip(offs, P[p]["asimetri_tohum_degerleri"]):
            axR.plot(v, y + dy, "o", ms=3.2, mfc="white", mec=INK, mew=0.7, zorder=3)
        axR.plot([m, m], [y - half_bar, y + half_bar], color=INK, lw=1.1, solid_capstyle="butt", zorder=4)
    axR.set_xlim(xmin, xmax)
    axR.set_xticks(range(int(xmin), int(xmax) + 1, 5))
    # row letters A-D on the right panel too (shared y with the boxes)
    axR.set_yticks([rows[p] for p in PROTOCOLS])
    axR.set_yticklabels(ROW_LETTERS, fontsize=FS_ROW, fontweight="bold", color=INK)
    axR.tick_params(axis="y", left=False, labelleft=True, pad=1)
    for sp in ("top", "right", "left"):
        axR.spines[sp].set_visible(False)
    axR.set_xlabel(T["xlabel"], labelpad=2, loc="right")  # TR label is wider than the axis
    hdr_r = fig.text(0.535 + 0.440 / 2, 0.985, T["hdr_right"].format(k=k_seeds),
                     ha="center", va="top", fontsize=FS_NAME, color=INK, linespacing=1.1)
    # v4: the centred header touched the "(b)" panel letter (found by the global
    # overlap check); shift it right just enough, never past the figure edge.
    fig.canvas.draw()
    _r = fig.canvas.get_renderer()
    _b = [t for t in fig.texts if t.get_text() == "(b)"][0].get_window_extent(_r)
    _h = hdr_r.get_window_extent(_r)
    _gap = 2.0 * fig.dpi / 72
    if _h.x0 < _b.x1 + _gap:
        dx = (_b.x1 + _gap - _h.x0) / fig.bbox.width
        if _h.x1 + dx * fig.bbox.width > fig.bbox.x1:
            fail("right header does not fit between '(b)' and the figure edge")
        hdr_r.set_x(hdr_r.get_position()[0] + dx)
    fig.text(0.5, 0.015, T["spread"].format(v=loc_num(f"{A['yayilim']:.2f}")),
             ha="center", va="bottom", fontsize=FS_BR, style="italic", color=INK)

    # ---- v4: three pairwise distances, adjacent rows, mean bar to mean bar ----
    # Reviewer B2: the old 9.21 / 5.79 brackets read as a partition of the spread
    # while the 3.91 interval lies inside 9.21. Each distance is now a separate
    # connector in the gap between the two rows it joins; no connector nests in
    # another. Plain lines, no arrowheads: a distance, not a direction of effect.
    # 2026-09-29 rule kept: the equation NUMBER is not printed (caption \eqref).
    CONNECTORS = [  # (upper row, lower row, data field, label key)
        ("raw", "target_correct", "ozdeslik_terimi_ham_eksi_hedef_dogru", "identity"),
        ("target_correct", "both_correct", "artik_takdir_her_ikisi_eksi_hedef", "endorsed"),
        ("both_correct", "successful_source", "bas_kaynak_eksi_her_ikisi_dogru", "estimand"),
    ]
    conn_info = {}
    for pu, pl, key, lab in CONNECTORS:
        if PROTOCOLS.index(pl) != PROTOCOLS.index(pu) + 1:
            fail(f"connector {pu}-{pl} does not join adjacent rows")
        yu, yl = rows[pu], rows[pl]
        ymid = (yu + yl) / 2
        axR.plot([a[pu], a[pu], a[pl], a[pl]], [yu - half_bar, ymid, ymid, yl + half_bar],
                 color=INK, lw=0.7, solid_joinstyle="miter", zorder=4)
        conn_info[key] = (pu, pl, lab, ymid)

    # ---- label placement: deterministic search, rejected on any overlap ----
    # Per-row mean/SD labels (unit dropped in v4: the x-axis label carries "pts")
    # and the three connector labels are placed jointly: row-label sides are
    # tried in order of preference (side with more free axis length first);
    # for each, every connector label takes the first candidate position that
    # overlaps no text and no data mark (seed circles, mean bars, connector
    # segments; the dotted row guides are background). Positions are fixed
    # candidates, so the result is reproducible.
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    ax_bb, fig_bb = axR.get_window_extent(R), fig.bbox
    px = fig.dpi / 72.0
    PAD = 0.75 * px

    def mark_boxes():
        out = []
        for ln in axR.get_lines():
            if ln.get_color() == GUIDE:
                continue
            xy = ln.get_transform().transform(ln.get_xydata())
            if len(xy) == 1:
                rad = ln.get_markersize() / 2 * px + PAD
                out += [Bbox.from_extents(x - rad, y - rad, x + rad, y + rad) for x, y in xy]
            else:
                w = ln.get_linewidth() / 2 * px + PAD
                for (x0, y0), (x1, y1) in zip(xy[:-1], xy[1:]):
                    out.append(Bbox.from_extents(min(x0, x1) - w, min(y0, y1) - w,
                                                 max(x0, x1) + w, max(y0, y1) + w))
        return out

    MARKS = mark_boxes()

    def free(t, left_limit):
        bb = t.get_window_extent(R)
        # >= 2 pt clear of the figure edge (no glyph flush with the crop line)
        if bb.x0 < left_limit or bb.x1 > fig_bb.x1 - 2 * px or bb.y0 < fig_bb.y0 or bb.y1 > fig_bb.y1:
            return False
        if any(bb.overlaps(m) for m in MARKS):
            return False
        for o in fig.findobj(matplotlib.text.Text):
            if o is t or not o.get_visible() or not o.get_text().strip():
                continue
            if bb.overlaps(o.get_window_extent(R)):
                return False
        return True

    def ann(txt, xy, off, ha, va, italic=False):
        # italic = a difference BETWEEN protocols (connectors, bottom spread line);
        # upright = a per-row measurement (mean, SD)
        return axR.annotate(txt, xy, xytext=off, textcoords="offset points", ha=ha, va=va,
                            fontsize=FS_VAL, color=INK, annotation_clip=False, linespacing=1.05,
                            multialignment="center", style="italic" if italic else "normal")

    def row_label(p, side):
        seeds = P[p]["asimetri_tohum_degerleri"]
        right = side == "right"
        xa = max(seeds + [a[p]]) if right else min(seeds + [a[p]])
        return ann(f"{loc_num(f'{a[p]:+.2f}')}\n±{loc_num(format(P[p]['asimetri_sd'], '.2f'))}",
                   (xa, rows[p]), (5 if right else -5, 0), "left" if right else "right", "center")

    def conn_candidates(key):
        pu, pl, lab, ymid = conn_info[key]
        val, name = loc_num(f"{A[key]:.2f}"), T[lab]
        x_lo, x_hi, xm = min(a[pu], a[pl]), max(a[pu], a[pl]), (a[pu] + a[pl]) / 2
        variants = [f"{val} ({name})", f"{val}\n{name}"]
        if " " in name:
            variants.append(f"{val}\n" + name.replace(" ", "\n", 1))
            if name.count(" ") > 1:  # 2026-10-31: longer terms also break at the last space
                head, tail = name.rsplit(" ", 1)
                variants.append(f"{val}\n{head}\n{tail}")
            # 2026-10-31: narrowest variant, one word per line, hyphenated words broken after the hyphen
            variants.append(f"{val}\n" + name.replace("-", "-\n").replace(" ", "\n"))
        pos = [((x_hi, ymid), (3, 0), "left", "center", "right of the horizontal segment"),
               ((x_lo, ymid), (-3, 0), "right", "center", "left of the horizontal segment"),
               ((xm, ymid), (0, 2), "center", "bottom", "centred above the horizontal segment"),
               ((xm, ymid), (0, -2), "center", "top", "centred below the horizontal segment"),
               ((a[pu], ymid), (3, 2), "left", "bottom", "right of the upper riser"),
               ((a[pu], ymid), (-3, 2), "right", "bottom", "left of the upper riser"),
               ((a[pl], ymid), (3, -2), "left", "top", "right of the lower riser"),
               ((a[pl], ymid), (-3, -2), "right", "top", "left of the lower riser")]
        # beside the segment end at mid-gap first (any number of lines), so the
        # label sits between the two rows it joins; riser/centred positions after.
        return ([(v,) + q for q in pos[:2] for v in variants]
                + [(v,) + q for q in pos[4:] + pos[2:4] for v in variants])

    def pref(p):
        seeds = P[p]["asimetri_tohum_degerleri"] + [a[p]]
        return "right" if (xmax - max(seeds)) >= (min(seeds) - xmin) else "left"

    other = {"right": "left", "left": "right"}
    combos = sorted(itertools.product(*[(pref(p), other[pref(p)]) for p in PROTOCOLS]),
                    key=lambda c: (sum(s != pref(p) for s, p in zip(c, PROTOCOLS)), c))
    label_side, placed, done = {}, {}, False
    unplaced = []
    for combo in combos:
        made = []
        ok = True
        for p, side in zip(PROTOCOLS, combo):
            t = row_label(p, side)
            made.append(t)
            if not free(t, ax_bb.x0):
                ok = False
                break
        if ok:
            placed = {}
            for key in conn_info:
                hit = None
                for txt, xy, off, ha, va, where in conn_candidates(key):
                    t = ann(txt, xy, off, ha, va, italic=True)
                    if free(t, ax_bb.x0):
                        hit = (t, txt, where, ha, va, off)
                        break
                    t.remove()
                if hit is None:
                    ok = False
                    unplaced.append((combo, key))  # 2026-10-31: reported if no layout is found
                    break
                made.append(hit[0])
                placed[key] = {"metin": hit[1], "yer": hit[2], "ha": hit[3], "va": hit[4], "ofset_pt": list(hit[5])}
        if ok:
            label_side = dict(zip(PROTOCOLS, combo))
            done = True
            break
        for t in made:
            t.remove()
    if not done:
        fail(f"no overlap-free label layout found (raise --height-cm); unplaced connector per row-side combo: {unplaced}")

    # final global check: no two texts overlap anywhere in the figure
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()]
    for i in range(len(texts)):
        bb = texts[i].get_window_extent(R)
        for j in range(i + 1, len(texts)):
            if bb.overlaps(texts[j].get_window_extent(R)):
                fail(f"text overlap: {texts[i].get_text()!r} / {texts[j].get_text()!r}")
        if bb.x0 < fig_bb.x0 or bb.x1 > fig_bb.x1 or bb.y0 < fig_bb.y0 or bb.y1 > fig_bb.y1:
            fail(f"text outside the figure: {texts[i].get_text()!r}")
    min_pt = min(t.get_fontsize() for t in texts)
    if min_pt < MIN_FONT - 1e-6:
        fail(f"text below {MIN_FONT} pt: {min_pt}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    moved = keep_old(outdir, args.name)
    pdf, png = outdir / f"{args.name}.pdf", outdir / f"{args.name}.png"
    fig.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=args.dpi)
    plt.close(fig)
    if b"/Type3" in pdf.read_bytes():
        fail("Type 3 font in PDF")

    printed = {}
    for key, p in (("all", "raw"), ("target_correct", "target_correct"),
                   ("both_correct", "both_correct"), ("successful_source", "successful_source")):
        q = P[p]
        printed[f"N_CNN_to_ViT_{key}"] = {"deger": q["n_CNN_to_ViT"], "kaynak": f"protokoller.{p}.n_CNN_to_ViT"}
        printed[f"N_ViT_to_CNN_{key}"] = {"deger": q["n_ViT_to_CNN"], "kaynak": f"protokoller.{p}.n_ViT_to_CNN",
                                          "basildi": q["n_ViT_to_CNN"] != q["n_CNN_to_ViT"],
                                          "not": None if q["n_ViT_to_CNN"] != q["n_CNN_to_ViT"]
                                          else "equal to CNN->ViT, single N printed"}
        printed[f"N_gosterim_{key}"] = {"gosterim": n_label(P, p)}
        printed[f"asimetri_{key}"] = {"deger": q["asimetri_ort"], "gosterim": f"{loc_num(format(q['asimetri_ort'], '+.2f'))}", "satir": ROW_LETTERS[PROTOCOLS.index(p)],
                                      "kaynak": f"protokoller.{p}.asimetri_ort"}
        printed[f"sd_{key}"] = {"deger": q["asimetri_sd"], "gosterim": "\u00b1" + loc_num(f"{q['asimetri_sd']:.2f}"),
                                "kaynak": f"protokoller.{p}.asimetri_sd"}
        printed[f"tohum_{key}"] = {"deger": q["asimetri_tohum_degerleri"], "gosterim": "open circles (not labelled)",
                                   "kaynak": f"protokoller.{p}.asimetri_tohum_degerleri"}
    printed["tohum_cifti_sayisi"] = {"deger": k_seeds, "gosterim": f"{k_seeds} seed pairs",
                                     "kaynak": "len(protokoller.*.asimetri_tohum_degerleri)"}
    printed["yayilim"] = {"deger": A["yayilim"], "gosterim": loc_num(f"{A['yayilim']:.2f}"),
                          "yer": "bottom line (successful_source minus target_correct, checked as max/min)",
                          "kaynak": "ayrisim.yayilim"}
    for k, (pu, pl, lab, _) in conn_info.items():
        printed[k] = {"deger": A[k], "gosterim": loc_num(f"{A[k]:.2f}"), "etiket": T[lab],
                      "yer": (f"connector between rows {ROW_LETTERS[PROTOCOLS.index(pu)]} ({pu}) and "
                              f"{ROW_LETTERS[PROTOCOLS.index(pl)]} ({pl}), mean bar to mean bar"),
                      "etiket_yerlesimi": placed[k], "kaynak": f"ayrisim.{k}"}
    printed["farkli_estimand_bas_kaynak_eksi_ham"] = {
        "deger": A["farkli_estimand_bas_kaynak_eksi_ham"], "basildi": False,
        "not": "v4: no longer drawn (successful_source vs raw bracket removed, reviewer B2)"}
    printed["denklem_numarasi"] = {"deger": eqn,
                                   "gosterim": "sekle BASILMIYOR (baslik \\eqref tasir); .aux'taki numara yalniz kayit icin",
                                   "kaynak": f"{aux} \\newlabel{{{args.eq_key}}}",
                                   "aux_sha256": hashlib.sha256(aux.read_bytes()).hexdigest(),
                                   "aux_mtime_utc": dt.datetime.fromtimestamp(aux.stat().st_mtime, dt.timezone.utc).isoformat(timespec="seconds"),
                                   "not": "cross-reference, not a result; regenerate the figure if equations are renumbered"}

    kanit = {
        "sekil": args.name,
        "surum": 5,
        "dil": LANG,
        "degisiklik_2026_10_31_v5": [
            "hakem konseyi m16: connector labels 'endorsed pair' -> 'marginal subsets removed', "
            "'different estimand' -> 'source robustness' (manuscript terms, 04_experiments and 05_discussion; "
            "the report's 'source-robustness term' does not fit the C-D gap at 8 pt up to 12 cm height)",
            "height 10.5 cm (v4 10.0 cm)",
            "panel (a) key 'N: CNN->ViT / ViT->CNN' -> 'N (CNN->ViT / ViT->CNN)'",
            "every printed number compared with results/C1_REFERANS_FOYU.md (foy_karsilastirmasi)",
            "copy in paper/figures/konsey (council figure agent's write area); width 8.89 cm kept (header fit)",
            "manuscript path still ../figures/final/fig_protocol_sets.pdf until the author switches it",
        ],
        "foy_karsilastirmasi": foy_sonuc,
        "degisiklik_2026_10_04_v4": [
            "reviewer B2: bracket stack above the axis (9.21, 5.79) removed; it implied a partition of the spread",
            "three pairwise distances drawn as connectors between adjacent rows: A-B raw vs target_correct "
            "(identity term), B-C target_correct vs both_correct (endorsed pair), C-D both_correct vs "
            "successful_source (different estimand, new data field ayrisim.bas_kaynak_eksi_her_ikisi_dogru)",
            "connector label position chosen automatically from fixed candidates; rejected if it overlaps any "
            "text or data mark; final all-pairs text overlap and in-figure check",
            "bottom line: 'terms rounded separately' replaced by the named endpoints; endpoints checked as max/min",
            "left panel, row letters A-D and panel letters unchanged; equation number still not printed",
        ],
        "degisiklik_2026_10_04": [
            "row letters A-D on both panels (left: box corner, right: y tick labels)",
            "panel letters (a)/(b)",
            "3.91 term moved from the bracket stack to a connector between rows B and C (mean bar to mean bar); 9.21 and 5.79 brackets unchanged (author decision pending)",
            "per-row mean and SD labels moved beside the row (side with more free axis length) to free the B-C gap",
            "all text >= 8 pt; width 8.89 cm (3.5 in), height 10.0 cm",
            "--lang tr: Turkish labels, decimal comma, thousands dot, output to paper/figures/final_tr",
        ],
        "betik": "paper/figures/konsey/fig_protocol_sets.py",
        "kopyalandigi_betik": "paper/figures/fig_protocol_sets.py (v4, 2026-10-04)",
        "onceki_betik": "paper/figures/fig_protocol_sets_v1.py",
        "komut": "docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_protocol_sets.py",
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "veri": str(data_path),
        "veri_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "ust_kaynak": d["kaynak"],
        "ust_kaynak_sha256": d["kaynak_sha256"],
        "ust_kaynak_sha256_kaynagi": "fig_protokol_kumeleri_veri.json: kaynak_sha256 (as recorded by the data script)",
        "git": git_info(root, [str(data_path), "scripts/fig_protokol_kumeleri_veri.py",
                               "paper/figures/konsey/fig_protocol_sets.py", d["kaynak"]]),
        "yerlesim": {
            "secim": "tek sutun",
            "genislik_cm": args.width_cm, "yukseklik_cm": args.height_cm, "dpi": args.dpi,
            "en_kucuk_yazi_pt": min(FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR, FS_ROW, FS_PANEL),
            "satir_etiketi_yonu": label_side,
            "gerekce": ("IEEE Access column width 3.5 in as the other journal figures (v5 keeps it: header fit). One row per set; "
                        "values on a horizontal axis because they are not monotone in the nesting order. "
                        "Height: rows spaced so the three connector labels sit between rows with >= 8 pt text and no overlap (checked)."),
            "dikdortgenler": "schematic, NOT area-proportional to N; nesting drawn for CNN->ViT",
            "tohum_noktalari": "vertical offsets of seed points are for visibility only, same order in every row",
            "yon_anahtari": ("'N (CNN->ViT / ViT->CNN)' (v5; v4 'N: CNN->ViT / ViT->CNN') placed once under the left header instead of inside each box: "
                             "the full string does not fit the inner boxes at >=8 pt"),
            "font": "DejaVu Sans (as in scripts/generate_journal_figs_c1.py), pdf.fonttype 42",
            "dolgular": dict(zip(PROTOCOLS, FILLS)),
        },
        "basilan_sayilar": printed,
        "esitlik_kaydi": {
            "tohum_basina_ortalama_yayilim": A["tohum_basina_ortalama_yayilim"],
            "yayilim": A["yayilim"],
            "esit": A["tohum_basina_ortalama_yayilim"] == A["yayilim"],
            "tohum_basina_yayilim_tohum_degerlerinden": [round(v, 2) for v in per_seed],
            "ortalamasi": round(statistics.mean(per_seed), 4),
        },
        "denetimler": [
            "ic_icelik_tutuyor == true",
            "N non-increasing along nesting, both directions",
            "raw and both_correct: same N in both directions",
            "mean and SD(n-1) of asimetri_tohum_degerleri == asimetri_ort / asimetri_sd within 0.0051",
            "ayrisim terms (incl. bas_kaynak_eksi_her_ikisi_dogru) == differences of protocol means within rounding (<=0.0101)",
            "mean per-seed spread recomputed from seed values == tohum_basina_ortalama_yayilim (<=0.0051)",
            "tohum_basina_ortalama_yayilim == yayilim",
            "spread endpoints: max = successful_source, min = target_correct (bottom line names them)",
            "three connector values > 0 (labels are unsigned distances); connectors join adjacent rows",
            "no text overlaps another text or a data mark; all text inside the figure; all text >= 8 pt",
            "equation number read from compiled .aux (record only, not printed)",
            "no Type 3 font in PDF",
        ],
        "not_toplam": (f"B-C {A['artik_takdir_her_ikisi_eksi_hedef']:.2f} + C-D "
                       f"{A['bas_kaynak_eksi_her_ikisi_dogru']:.2f} = "
                       f"{A['artik_takdir_her_ikisi_eksi_hedef'] + A['bas_kaynak_eksi_her_ikisi_dogru']:.2f} "
                       f"vs spread {A['yayilim']:.2f} (telescoping identity, not a decomposition claim; "
                       "each term rounded from unrounded means)"),
        "eski_surum_tasindi": moved,
        "dizindeki_eski_surumler": sorted({f.name.split(".")[0] for f in outdir.glob(f"{args.name}_v*.pdf")}),
    }
    with io.open(outdir / f"{args.name}.kanit.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(kanit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"written: {pdf}\nwritten: {png}\nwritten: {outdir / (args.name + '.kanit.json')}")
    print(f"equation number from {aux}: {eqn}")
    if moved:
        print(f"old version kept as {moved}.*")


if __name__ == "__main__":
    main()
