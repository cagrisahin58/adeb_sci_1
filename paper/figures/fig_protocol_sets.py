#!/usr/bin/env python3
"""Nested conditioning sets figure (IEEE Access, Section 4.2), version 2.

Left: the four evaluation sets drawn as nested boxes (schematic, NOT
area-proportional; the nesting is the CNN->ViT one, the ViT->CNN sets nest in
the same order). Each box carries N for both directions where they differ.
Right: per protocol, the three seed-pair asymmetries (open circles), their
mean (short vertical bar) and SD; above the axis, brackets for the spread
decomposition.

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

PROTOCOLS = ["raw", "target_correct", "both_correct", "successful_source"]
SET_NAMES = {
    "raw": ["All test samples (raw)"],
    "target_correct": ["Target (ViT) correct"],
    "both_correct": ["Both correct"],
    "successful_source": ["Successful source", "(CNN white-box)"],
}
# IBM blue scale around the CNN colour #0F62FE of the journal figures
# (scripts/generate_journal_figs_c1.py: C_CNN = "#0f62fe"): blue 10/20/40/60.
FILLS = ["#EDF5FF", "#D0E2FF", "#78A9FF", "#0F62FE"]
TEXT_ON_FILL = ["#161616", "#161616", "#161616", "#FFFFFF"]
EDGE = "#393939"
INK = "#262626"
GUIDE = "#C6C6C6"
CM = 1 / 2.54
MIN_FONT = 7.0


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
    # Brackets assume: min = target_correct, max = successful_source, raw between,
    # both_correct between target_correct and raw (the 3.91 bracket nests in 9.21).
    if not (a["target_correct"] <= a["both_correct"] <= a["raw"] <= a["successful_source"]):
        fail(f"protocol order changed ({a}); bracket layout would misstate the decomposition")
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
    return f"{n:,}"


def n_label(P, p):
    a, b = P[p]["n_CNN_to_ViT"], P[p]["n_ViT_to_CNN"]
    return f"N = {fmt_n(a)}" if a == b else f"N = {fmt_n(a)} / {fmt_n(b)}"


def bracket(ax, x0, x1, y, label, tick, fs, label_side="above", lw=0.7):
    ax.plot([x0, x0, x1, x1], [y - tick, y, y, y - tick], color=INK, lw=lw,
            solid_joinstyle="miter", clip_on=False, zorder=4)
    if label_side == "above":
        ax.annotate(label, ((x0 + x1) / 2, y), xytext=(0, 1.5), textcoords="offset points",
                    ha="center", va="bottom", fontsize=fs, color=INK, annotation_clip=False,
                    linespacing=1.0)
    else:  # right of the bracket, same height
        ax.annotate(label, (x1, y), xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=fs, color=INK, annotation_clip=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default="results/q1/fig_protokol_kumeleri_veri.json")
    ap.add_argument("--aux", default="paper/manuscript/main.aux")
    ap.add_argument("--eq-key", default="eq:raw_identity")
    ap.add_argument("--outdir", default="paper/figures/final")
    ap.add_argument("--name", default="fig_protocol_sets")
    ap.add_argument("--width-cm", type=float, default=8.8, help="IEEE single column")
    ap.add_argument("--height-cm", type=float, default=9.4)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="unused (no randomness); kept for the log")
    args = ap.parse_args()

    root = Path.cwd()
    data_path = Path(args.data)
    if not data_path.is_file():
        fail(f"{data_path} not found (run from repo root; generate it with scripts/fig_protokol_kumeleri_veri.py)")
    d, k_seeds, per_seed = load_and_check(data_path)
    P, A = d["protokoller"], d["ayrisim"]
    aux = Path(args.aux)
    eqn = eq_number(aux, args.eq_key)

    plt.rcParams.update({
        # Same family as scripts/generate_journal_figs_c1.py (current final figures).
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 7.5,
        "axes.labelsize": 7.5,
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
    FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR = 7.5, 7.0, 7.5, 7.0, 7.0
    assert min(FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR) >= MIN_FONT

    W, H = args.width_cm * CM, args.height_cm * CM
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")

    # ---- geometry in layout units (carries no data) ----
    band = 0.9                              # label band of rings 0..2
    inner_h = 1.0                           # innermost box holds three lines
    nlev = len(PROTOCOLS)
    ymax = band * (nlev - 1) + inner_h + 0.0
    x_in, y_in = 0.05, 0.12
    y_inner0 = ymax - (nlev - 1) * band - inner_h
    y_outer0 = y_inner0 - (nlev - 1) * y_in
    y_brackets = [ymax + 0.20, ymax + 0.55, ymax + 1.02]   # 3.91 / 9.21 / 5.79
    y_top = ymax + 1.40

    ax_bottom, ax_top = 0.165, 0.885
    axL = fig.add_axes([0.015, ax_bottom, 0.475, ax_top - ax_bottom])
    axR = fig.add_axes([0.535, ax_bottom, 0.440, ax_top - ax_bottom], sharey=axL)

    rows = {}
    for k, p in enumerate(PROTOCOLS):
        x0, x1 = k * x_in, 1 - k * x_in
        y1 = ymax - k * band
        y0 = y_outer0 + k * y_in if k < nlev - 1 else y_inner0
        axL.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor=FILLS[k],
                                edgecolor=EDGE, linewidth=0.6, joinstyle="miter"))
        yc = y1 - band / 2 if k < nlev - 1 else (y0 + y1) / 2
        rows[p] = yc
        lines = SET_NAMES[p] + [n_label(P, p)]
        step = 0.235
        y_first = yc + step * (len(lines) - 1) / 2
        for i, ln in enumerate(lines):
            is_n = ln.startswith("N = ")
            axL.text(0.5, y_first - i * step, ln, ha="center", va="center",
                     fontsize=FS_N if is_n else FS_NAME,
                     fontweight="normal" if (is_n or ln.startswith("(")) else "bold",
                     color=TEXT_ON_FILL[k])
    axL.set_xlim(-0.005, 1.005)
    axL.set_ylim(y_outer0 - 0.02, y_top)
    axL.axis("off")
    axL.text(0.5, ymax + 0.10, "N: CNN\u2192ViT / ViT\u2192CNN", ha="center", va="bottom",
             fontsize=FS_N, color=INK)
    # column headers at figure level, above both panels
    fig.text(0.015 + 0.475 / 2, 0.985, "Evaluation set\n(CNN\u2192ViT boxes)", ha="center", va="top",
             fontsize=FS_NAME, color=INK, linespacing=1.1)

    # ---- right: seed values, mean, SD ----
    allv = [v for p in PROTOCOLS for v in P[p]["asimetri_tohum_degerleri"]]
    xmax = 5 * math.ceil(max(allv) / 5 + 0.2)
    xmin = min(0.0, 5 * math.floor(min(allv) / 5))
    offs = [(i - (k_seeds - 1) / 2) * 0.11 for i in range(k_seeds)]  # visibility only
    for p in PROTOCOLS:
        y, m, s = rows[p], P[p]["asimetri_ort"], P[p]["asimetri_sd"]
        axR.plot([xmin, xmax], [y, y], color=GUIDE, lw=0.5, ls=(0, (1, 2)), zorder=1)
        for dy, v in zip(offs, P[p]["asimetri_tohum_degerleri"]):
            axR.plot(v, y + dy, "o", ms=3.2, mfc="white", mec=INK, mew=0.7, zorder=3)
        axR.plot([m, m], [y - 0.2, y + 0.2], color=INK, lw=1.1, solid_capstyle="butt", zorder=4)
        axR.annotate(f"{m:+.2f} pts", (m, y + 0.2), xytext=(0, 1), textcoords="offset points",
                     ha="center", va="bottom", fontsize=FS_VAL, color=INK)
        axR.annotate(f"\u00b1{s:.2f}", (m, y - 0.2), xytext=(0, -1), textcoords="offset points",
                     ha="center", va="top", fontsize=FS_SD, color=INK)
    axR.set_xlim(xmin, xmax)
    axR.set_xticks(range(int(xmin), int(xmax) + 1, 5))
    axR.tick_params(axis="y", left=False, labelleft=False)
    for sp in ("top", "right", "left"):
        axR.spines[sp].set_visible(False)
    axR.set_xlabel("CNN\u2192ViT \u2212 ViT\u2192CNN (pts)", labelpad=2)
    fig.text(0.535 + 0.440 / 2, 0.985, f"Measured asymmetry\n(mean \u00b1 SD, {k_seeds} seed pairs)",
             ha="center", va="top", fontsize=FS_NAME, color=INK, linespacing=1.1)

    # ---- brackets: decomposition, endpoints = protocol means ----
    a = {p: P[p]["asimetri_ort"] for p in PROTOCOLS}
    tick = 0.07
    bracket(axR, a["target_correct"], a["both_correct"], y_brackets[0],
            f"{A['artik_takdir_her_ikisi_eksi_hedef']:.2f}", tick, FS_BR, label_side="right")
    bracket(axR, a["target_correct"], a["raw"], y_brackets[1],
            # 2026-09-29: denklem NUMARASI sekle basilmaz. Numara .aux'a
            # baglidir; her yeniden numaralandirma sekli sessizce yanlislar.
            # Gonderme baslikta \eqref ile durur, sekil yalniz terimi adlandirir.
            f"{A['ozdeslik_terimi_ham_eksi_hedef_dogru']:.2f}, identity term", tick, FS_BR)
    bracket(axR, a["raw"], a["successful_source"], y_brackets[2],
            f"{A['farkli_estimand_bas_kaynak_eksi_ham']:.2f},\ndifferent estimand", tick, FS_BR)

    fig.text(0.5, 0.015, f"Spread {A['yayilim']:.2f} pts (terms rounded separately)",
             ha="center", va="bottom", fontsize=FS_BR, style="italic", color=INK)

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
        printed[f"asimetri_{key}"] = {"deger": q["asimetri_ort"], "gosterim": f"{q['asimetri_ort']:+.2f} pts",
                                      "kaynak": f"protokoller.{p}.asimetri_ort"}
        printed[f"sd_{key}"] = {"deger": q["asimetri_sd"], "gosterim": f"\u00b1{q['asimetri_sd']:.2f}",
                                "kaynak": f"protokoller.{p}.asimetri_sd"}
        printed[f"tohum_{key}"] = {"deger": q["asimetri_tohum_degerleri"], "gosterim": "open circles (not labelled)",
                                   "kaynak": f"protokoller.{p}.asimetri_tohum_degerleri"}
    printed["tohum_cifti_sayisi"] = {"deger": k_seeds, "gosterim": f"{k_seeds} seed pairs",
                                     "kaynak": "len(protokoller.*.asimetri_tohum_degerleri)"}
    for k, where in (("yayilim", "bottom line"),
                     ("ozdeslik_terimi_ham_eksi_hedef_dogru", "bracket target_correct..raw"),
                     ("farkli_estimand_bas_kaynak_eksi_ham", "bracket raw..successful_source"),
                     ("artik_takdir_her_ikisi_eksi_hedef", "bracket target_correct..both_correct")):
        printed[k] = {"deger": A[k], "gosterim": f"{A[k]:.2f}", "yer": where, "kaynak": f"ayrisim.{k}"}
    printed["denklem_numarasi"] = {"deger": eqn,
                                   "gosterim": "sekle BASILMIYOR (baslik \\eqref tasir); .aux'taki numara yalniz kayit icin",
                                   "kaynak": f"{aux} \\newlabel{{{args.eq_key}}}",
                                   "aux_sha256": hashlib.sha256(aux.read_bytes()).hexdigest(),
                                   "aux_mtime_utc": dt.datetime.fromtimestamp(aux.stat().st_mtime, dt.timezone.utc).isoformat(timespec="seconds"),
                                   "not": "cross-reference, not a result; regenerate the figure if equations are renumbered"}

    kanit = {
        "sekil": args.name,
        "surum": 2,
        "betik": "paper/figures/fig_protocol_sets.py",
        "onceki_betik": "paper/figures/fig_protocol_sets_v1.py",
        "komut": "docker exec -w /workspace adeb_eval python paper/figures/fig_protocol_sets.py",
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "veri": str(data_path),
        "veri_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "ust_kaynak": d["kaynak"],
        "ust_kaynak_sha256": d["kaynak_sha256"],
        "ust_kaynak_sha256_kaynagi": "fig_protokol_kumeleri_veri.json: kaynak_sha256 (as recorded by the data script)",
        "git": git_info(root, [str(data_path), "scripts/fig_protokol_kumeleri_veri.py",
                               "paper/figures/fig_protocol_sets.py", d["kaynak"]]),
        "yerlesim": {
            "secim": "tek sutun",
            "genislik_cm": args.width_cm, "yukseklik_cm": args.height_cm, "dpi": args.dpi,
            "en_kucuk_yazi_pt": min(FS_NAME, FS_N, FS_VAL, FS_SD, FS_BR),
            "gerekce": ("IEEE Access column width 8.8 cm as the other transfer figures. One row per set; "
                        "values on a horizontal axis because they are not monotone in the nesting order. "
                        "Height raised from 7.2 to 9.4 cm to stack the three brackets above the axis "
                        "without overlap at >=7 pt."),
            "dikdortgenler": "schematic, NOT area-proportional to N; nesting drawn for CNN->ViT",
            "tohum_noktalari": "vertical offsets of seed points are for visibility only, same order in every row",
            "yon_anahtari": ("'N: CNN->ViT / ViT->CNN' placed once under the left header instead of inside each box: "
                             "the full string does not fit the inner boxes at >=7 pt"),
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
            "ayrisim terms == differences of protocol means within rounding (<=0.0101)",
            "mean per-seed spread recomputed from seed values == tohum_basina_ortalama_yayilim (<=0.0051)",
            "tohum_basina_ortalama_yayilim == yayilim",
            "order target_correct <= both_correct <= raw <= successful_source (bracket layout)",
            "equation number read from compiled .aux",
            "no Type 3 font in PDF",
        ],
        "not_yuvarlama": (f"{A['ozdeslik_terimi_ham_eksi_hedef_dogru']:.2f} + "
                          f"{A['farkli_estimand_bas_kaynak_eksi_ham']:.2f} = "
                          f"{A['ozdeslik_terimi_ham_eksi_hedef_dogru'] + A['farkli_estimand_bas_kaynak_eksi_ham']:.2f} "
                          f"vs spread {A['yayilim']:.2f}: each term rounded from unrounded means "
                          "(printed as 'terms rounded separately')."),
        "eski_surum_tasindi": moved,
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
