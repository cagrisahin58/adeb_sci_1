#!/usr/bin/env python3
"""Protocol spread versus clean-accuracy gap, all model pairs (IEEE Access, Section 4.D).

One column (3.5 in), two panels stacked, shared x = |clean-accuracy gap| (pts).
(a) y = three-protocol spread (raw / target-correct / both-correct; field
    yayilim_uc), filled marker per group; a small open black ring at the same
    x marks the identity prediction |raw - target-correct| at p = 1 (field
    raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1). No OLS line (slope is in the
    reference sheet, not on the figure).
(b) y = successful-source minus both-correct asymmetry (signed; field
    bas_kaynak_eksi_bc_asimetri), same markers, dashed y = 0 line.
Colour + marker shape per group (Okabe-Ito, grey for the RobustBench pool);
filled = measured, open ring = identity prediction (print-safe second channel).

QUARANTINE RULE: every number drawn comes from ONE file,
results/q1/fig_yayilim_temiz_fark_veri.json (scripts/fig_yayilim_temiz_fark_veri.py),
whose own sources are results/c1_* and results/q1/* only (checked below).

Run from the repo root inside the container:
    docker exec -w /workspace adeb_eval python paper/figures/fig_yayilim_temiz_fark.py [--lang tr]
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
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.text  # noqa: E402,F401
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

SCRIPT_REL = "paper/figures/fig_yayilim_temiz_fark.py"
INK, EDGE, ZERO = "#262626", "#393939", "#8d8d8d"
MIN_FONT = 8.0

# Group key in the data file -> (legend key, colour, marker, size, zorder).
# Okabe-Ito colours; the large RobustBench pool is neutral grey and drawn first.
# The same group keeps the same colour and marker in both panels.
GROUPS = {
    "CIFAR-10 Linf, AT cifti":                   ("c10",   "#E69F00", "o", 4.6, 4),
    "CIFAR-10 L2, AT cifti":                     ("c10l2", "#009E73", "^", 4.8, 4),
    "CIFAR-100 Linf, AT cifti":                  ("c100",  "#56B4E9", "s", 4.2, 4),
    "SVHN Linf, AT cifti":                       ("svhn",  "#F0E442", "D", 4.0, 4),
    "CIFAR-10 Linf, WRN-28-10 referansiyla":     ("wrn",   "#0072B2", "v", 4.8, 4),
    "CIFAR-10 Linf, standart egitimli modeller": ("std",   "#D55E00", "P", 5.0, 4),
    "CIFAR-10 Linf, son kontrol noktasi":        ("last",  "#CC79A7", "X", 5.0, 4),
    "CIFAR-10 Linf, RobustBench havuzu":         ("pool",  "#A8A8A8", "h", 4.8, 3),
}
TXT = {
    "en": {
        "x": "|Clean-accuracy gap| (pts)",
        "ya": "Three-protocol spread (pts)",
        "yb": "Successful-source −\nboth-correct (pts)",
        "leg": {"c10": r"CIFAR-10 $L_\infty$ AT", "c10l2": r"CIFAR-10 $L_2$ AT", "c100": "CIFAR-100 AT",
                "svhn": "SVHN AT", "wrn": "with WRN-28-10 ref.", "std": "standard training",
                "last": "last checkpoint", "pool": "RobustBench pool"},
        "pred": "identity prediction",
        "outdir": "paper/figures/final",
    },
    "tr": {
        "x": "|Temiz doğruluk farkı| (puan)",
        "ya": "Üç protokol yayılımı (puan)",
        "yb": "Başarılı kaynak −\nher ikisi doğru (puan)",
        "leg": {"c10": r"CIFAR-10 $L_\infty$ AT", "c10l2": r"CIFAR-10 $L_2$ AT", "c100": "CIFAR-100 AT",
                "svhn": "SVHN AT", "wrn": "WRN-28-10 referanslı", "std": "standart eğitim",
                "last": "son kontrol noktası", "pool": "RobustBench havuzu"},
        "pred": "özdeşlik öngörüsü",
        "outdir": "paper/figures/final_tr",
    },
}
PROT = ("raw", "target_correct", "both_correct", "successful_source")


def fail(msg):
    sys.stderr.write(f"HATA / ERROR: {msg}\n")
    sys.exit(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_info(paths):
    def run(*args):
        try:
            return subprocess.run(["git", "-c", f"safe.directory={Path.cwd()}", *args],
                                  capture_output=True, text=True, timeout=20).stdout.strip()
        except Exception:
            return ""
    return {"commit": run("rev-parse", "HEAD") or "unknown",
            "branch": run("rev-parse", "--abbrev-ref", "HEAD") or "unknown",
            "dirty_or_untracked": run("status", "--porcelain", "--", *paths).splitlines()}


def keep_old(outdir, name):
    """Never overwrite a figure silently: move an existing version to _vN."""
    exts = [".pdf", ".png", ".kanit.json"]
    if not any((outdir / f"{name}{e}").exists() for e in exts):
        return None
    k = 1
    while any((outdir / f"{name}_v{k}{e}").exists() for e in exts):
        k += 1
    for e in exts:
        if (outdir / f"{name}{e}").exists():
            shutil.move(str(outdir / f"{name}{e}"), str(outdir / f"{name}_v{k}{e}"))
    return f"{name}_v{k}"


def load_and_check(path):
    d = json.loads(path.read_text(encoding="utf-8"))
    for k in ("noktalar", "n_nokta", "kaynaklar", "egim", "gruplar"):
        if k not in d:
            fail(f"top-level field '{k}' missing in {path}")
    N = d["noktalar"]
    if d["n_nokta"] != len(N):
        fail(f"n_nokta {d['n_nokta']} != len(noktalar) {len(N)}")
    for rel in d["kaynaklar"]:
        if not (rel.startswith("results/c1_") or rel.startswith("results/q1/")):
            fail(f"source outside the quarantine-safe paths: {rel}")
    unknown = sorted({n["grup"] for n in N} - set(GROUPS))
    if unknown:
        fail(f"group(s) without a legend entry: {unknown}")
    need = ("grup", "modeller", "temiz_a", "temiz_b", "temiz_fark_mutlak", "yayilim_uc", "asimetri",
            "raw_eksi_tc_asimetri_olculen", "raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1",
            "bas_kaynak_eksi_bc_asimetri")
    for i, n in enumerate(N):
        for k in need:
            if k not in n:
                fail(f"noktalar[{i}].{k} missing")
        s = n["asimetri"]
        # every plotted field recomputed from its own definition fields
        if abs(n["temiz_fark_mutlak"] - abs(n["temiz_a"] - n["temiz_b"])) > 1e-6:
            fail(f"noktalar[{i}]: temiz_fark_mutlak != |temiz_a - temiz_b|")
        y3 = max(s[p] for p in PROT[:3]) - min(s[p] for p in PROT[:3])
        if abs(n["yayilim_uc"] - y3) > 1e-9:
            fail(f"noktalar[{i}]: yayilim_uc {n['yayilim_uc']} != max-min of raw/tc/bc {y3}")
        if abs(n["bas_kaynak_eksi_bc_asimetri"] - (s["successful_source"] - s["both_correct"])) > 1e-9:
            fail(f"noktalar[{i}]: bas_kaynak_eksi_bc_asimetri != ss - bc")
        if abs(n["raw_eksi_tc_asimetri_olculen"] - (s["raw"] - s["target_correct"])) > 1e-9:
            fail(f"noktalar[{i}]: raw_eksi_tc_asimetri_olculen != raw - tc")
    dev = max(abs(n["raw_eksi_tc_asimetri_olculen"] - n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"]) for n in N)
    stored = d["egim"]["ozdeslik_paritesi"]["mutlak_sapma_max"]
    if abs(dev - stored) > 1e-9:
        fail(f"identity parity max deviation {dev} != egim.ozdeslik_paritesi.mutlak_sapma_max {stored}")
    return d, dev


def repeated_pairs(N):
    """Same model pair measured in two groups (same attack family, same clean accuracies)."""
    fam = lambda g: g.split(",")[0]  # "CIFAR-10 Linf", "CIFAR-10 L2", ...
    seen = defaultdict(list)
    for i, n in enumerate(N):
        key = (fam(n["grup"]), tuple(sorted((round(n["temiz_a"], 2), round(n["temiz_b"], 2)))))
        seen[key].append(i)
    out = []
    for key, idx in seen.items():
        if len({N[i]["grup"] for i in idx}) > 1:
            out.append([{"grup": N[i]["grup"], "modeller": N[i]["modeller"], "cift": N[i].get("cift"),
                         "temiz_fark_mutlak": round(N[i]["temiz_fark_mutlak"], 4),
                         "yayilim_uc": round(N[i]["yayilim_uc"], 4),
                         "bas_kaynak_eksi_bc_asimetri": round(N[i]["bas_kaynak_eksi_bc_asimetri"], 4)} for i in idx])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default="results/q1/fig_yayilim_temiz_fark_veri.json")
    ap.add_argument("--lang", choices=sorted(TXT), default="en")
    ap.add_argument("--outdir", default=None, help="default: by --lang")
    ap.add_argument("--name", default="fig_spread_clean_gap")
    ap.add_argument("--width-in", type=float, default=3.5, help="IEEE single column")
    ap.add_argument("--height-in", type=float, default=4.9)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="unused (no randomness); kept for the log")
    args = ap.parse_args()
    T = TXT[args.lang]
    outdir = Path(args.outdir or T["outdir"])
    data_path = Path(args.data)
    if not data_path.is_file():
        fail(f"{data_path} not found (run from repo root; scripts/fig_yayilim_temiz_fark_veri.py makes it)")
    d, parity_dev = load_and_check(data_path)
    N = d["noktalar"]

    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"], "mathtext.fontset": "dejavusans",
        "font.size": 8, "axes.labelsize": 9, "legend.fontsize": 8,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.linewidth": 0.6, "axes.edgecolor": EDGE, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5,
        "pdf.fonttype": 42, "ps.fonttype": 42, "savefig.bbox": "standard",
        "svg.hashsalt": str(args.seed),
    })
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    # layout in figure fractions (carries no data); legend band at the bottom
    left, right = 0.205, 0.975
    axA = fig.add_axes([left, 0.565, right - left, 0.415])
    axB = fig.add_axes([left, 0.255, right - left, 0.275], sharex=axA)

    order = sorted(GROUPS, key=lambda g: GROUPS[g][4])  # pool first (lowest zorder)
    by_group = defaultdict(list)
    for n in N:
        by_group[n["grup"]].append(n)
    hmap = {}
    for g in order:
        key, col, mk, ms, z = GROUPS[g]
        pts = by_group.get(g, [])
        if not pts:
            continue
        xs = [n["temiz_fark_mutlak"] for n in pts]
        kw = dict(ls="none", marker=mk, ms=ms, mfc=col, mec=INK, mew=0.35, zorder=z)
        axA.plot(xs, [n["yayilim_uc"] for n in pts], **kw)
        axB.plot(xs, [n["bas_kaynak_eksi_bc_asimetri"] for n in pts], **kw)
        hmap[g] = Line2D([], [], label=T["leg"][key], **kw)
    handles = [hmap[g] for g in GROUPS if g in hmap]  # legend in definition order, pool last
    # identity prediction: small open ring, same x, drawn above every group
    ring = dict(ls="none", marker="o", ms=2.3, mfc="none", mec=INK, mew=0.6, zorder=6)
    axA.plot([n["temiz_fark_mutlak"] for n in N],
             [abs(n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"]) for n in N], **ring)
    handles.append(Line2D([], [], label=T["pred"], **ring))
    axB.axhline(0.0, color=ZERO, lw=0.6, ls=(0, (4, 2)), zorder=1)

    xs_all = [n["temiz_fark_mutlak"] for n in N]
    ya_all = [n["yayilim_uc"] for n in N] + [abs(n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"]) for n in N]
    yb_all = [n["bas_kaynak_eksi_bc_asimetri"] for n in N]
    # limits from the data plus a margin so no marker is cut by the frame
    xpad = 0.02 * max(xs_all)
    axA.set_xlim(-xpad, 5 * math.ceil((max(xs_all) + xpad) / 5))
    axA.set_ylim(-0.03 * max(ya_all), 5 * math.ceil(max(ya_all) * 1.03 / 5))
    ypad_b = 0.04 * (max(yb_all) - min(yb_all))
    axB.set_ylim(min(yb_all) - ypad_b, max(yb_all) + ypad_b)
    for ax in (axA, axB):
        ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axA.yaxis.set_major_locator(mticker.MultipleLocator(5))
    axB.yaxis.set_major_locator(mticker.MultipleLocator(10))
    axA.tick_params(labelbottom=False)
    axB.set_xlabel(T["x"], labelpad=2)
    axA.set_ylabel(T["ya"], labelpad=3)
    axB.set_ylabel(T["yb"], labelpad=3, linespacing=1.0)
    fig.align_ylabels([axA, axB])
    fig.text(0.008, 0.993, "(a)", ha="left", va="top", fontsize=9, fontweight="bold", color=INK)
    fig.text(0.008, 0.533, "(b)", ha="left", va="bottom", fontsize=9, fontweight="bold", color=INK)
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False,
               handletextpad=0.3, columnspacing=1.0, borderaxespad=0.2, labelspacing=0.35,
               handlelength=1.0)

    if args.lang == "tr":
        class Virgul(mticker.ScalarFormatter):
            def __call__(self, x, pos=None):
                return super().__call__(x, pos).replace(".", ",")
        for ax in (axA, axB):
            ax.xaxis.set_major_formatter(Virgul())
            ax.yaxis.set_major_formatter(Virgul())

    # ---- checks: text overlap, inside figure, >= 8 pt ----
    fig.canvas.draw()
    R = fig.canvas.get_renderer()
    # tick labels outside the view interval are kept as Text objects but never
    # drawn; only the drawn ones (Axis._update_ticks) take part in the checks
    tick_objs, drawn = set(), set()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            for tk in axis.get_major_ticks() + axis.get_minor_ticks():
                tick_objs.update({id(tk.label1), id(tk.label2)})
            for tk in axis._update_ticks():
                if tk.label1.get_visible():
                    drawn.add(id(tk.label1))
                if tk.label2.get_visible():
                    drawn.add(id(tk.label2))
    texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()
             and (id(t) not in tick_objs or id(t) in drawn)]
    for i in range(len(texts)):
        bb = texts[i].get_window_extent(R)
        if bb.x0 < 0 or bb.y0 < 0 or bb.x1 > fig.bbox.x1 or bb.y1 > fig.bbox.y1:
            fail(f"text outside the figure: {texts[i].get_text()!r}")
        for j in range(i + 1, len(texts)):
            if bb.overlaps(texts[j].get_window_extent(R)):
                fail(f"text overlap: {texts[i].get_text()!r} {bb.bounds} / {texts[j].get_text()!r} "
                     f"{texts[j].get_window_extent(R).bounds} (px at {fig.dpi} dpi)")
    leg_bb = fig.legends[0].get_window_extent(R)
    for ax in (axA, axB):
        tb = ax.get_tightbbox(R)
        if leg_bb.overlaps(tb):
            fail("legend overlaps an axes")
    if axA.get_tightbbox(R).overlaps(axB.get_window_extent(R)):
        fail("panel (a) decorations overlap panel (b)")
    min_pt = min(t.get_fontsize() for t in texts)
    if min_pt < MIN_FONT - 1e-6:
        fail(f"text below {MIN_FONT} pt: {min_pt}")

    outdir.mkdir(parents=True, exist_ok=True)
    moved = keep_old(outdir, args.name)
    pdf, png = outdir / f"{args.name}.pdf", outdir / f"{args.name}.png"
    fig.savefig(pdf, metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(png, dpi=args.dpi)
    plt.close(fig)
    if b"/Type3" in pdf.read_bytes():
        fail("Type 3 font in PDF")

    def mm(v):
        return {"min": round(min(v), 4), "max": round(max(v), 4)}

    cnt = Counter(n["grup"] for n in N)
    eg = d["egim"]
    kanit = {
        "sekil": args.name, "dil": args.lang, "surum": 1,
        "betik": SCRIPT_REL,
        "komut": "docker exec -w /workspace adeb_eval python " + " ".join([SCRIPT_REL] + sys.argv[1:]),
        "uretim_zamani_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "veri": str(data_path), "veri_sha256": sha(data_path),
        "veri_uretildi_utc": d.get("uretildi_utc"),
        "veri_betigi": "scripts/fig_yayilim_temiz_fark_veri.py",
        "ust_kaynaklar_sha256": d["kaynaklar"],
        "ust_kaynaklar_sha256_kaynagi": "fig_yayilim_temiz_fark_veri.json: kaynaklar (as recorded by the data script)",
        "git": git_info([str(data_path), "scripts/fig_yayilim_temiz_fark_veri.py", SCRIPT_REL]),
        "yerlesim": {"boyut_in": [W, H], "dpi": args.dpi, "en_kucuk_yazi_pt": min_pt,
                     "font": "DejaVu Sans, pdf.fonttype 42",
                     "gruplar": {g: {"lejant": T["leg"][GROUPS[g][0]], "renk": GROUPS[g][1],
                                     "isaretci": GROUPS[g][2]} for g in GROUPS},
                     "ozdeslik_isaretcisi": "open black ring, ms 2.3, same x as the measured point (panel a only)",
                     "egim_cizgisi": "none (slope reported in the reference sheet, not drawn)"},
        "okunan_degerler": {
            "nokta_sayisi": len(N),
            "grup_sayilari": {g: cnt.get(g, 0) for g in GROUPS},
            "x_temiz_fark_mutlak": mm(xs_all),
            "a_y_yayilim_uc": mm([n["yayilim_uc"] for n in N]),
            "a_y_ozdeslik_ongorusu_mutlak": mm([abs(n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"]) for n in N]),
            "b_y_bas_kaynak_eksi_bc": mm(yb_all),
            "ozdeslik_paritesi_sapma_max": parity_dev,
            "ozdeslik_paritesi_sapma_max_kaynak": "recomputed from points == egim.ozdeslik_paritesi.mutlak_sapma_max",
            "uc_protokol_yayilimi_esit_raw_tc_farki": eg.get("uc_protokol_yayilimi_vs_raw_tc_farki"),
            "cizilmeyen_egim_ozetleri": {k: {kk: eg[k][kk] for kk in ("egim", "pearson_r", "spearman_rho", "n_cift")}
                                         for k in ("dort_protokol", "uc_protokol_bas_kaynak_haric") if k in eg},
        },
        "havuz_var": cnt.get("CIFAR-10 Linf, RobustBench havuzu", 0) > 0,
        "tekrar_olculen_ciftler": repeated_pairs(N),
        "tekrar_notu": ("pairs listed together are the same two checkpoints measured in two runs; the data "
                        "file keeps both, the figure draws both; group counts and slopes count them twice"),
        "denetimler": [
            "n_nokta == len(noktalar)", "every source path under results/c1_* or results/q1/*",
            "every group has a legend entry (unknown group -> error)",
            "temiz_fark_mutlak == |temiz_a - temiz_b| (1e-6)",
            "yayilim_uc == max-min of raw/tc/bc asymmetries (1e-9)",
            "bas_kaynak_eksi_bc_asimetri == ss - bc; raw_eksi_tc_asimetri_olculen == raw - tc (1e-9)",
            "identity parity max deviation recomputed == stored (1e-9)",
            "no text overlap, all text inside the figure, legend clear of both axes, all text >= 8 pt",
            "no Type 3 font in PDF",
        ],
        "eski_surum_tasindi": moved,
    }
    with io.open(outdir / f"{args.name}.kanit.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(kanit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"written: {pdf}\nwritten: {png}\nwritten: {outdir / (args.name + '.kanit.json')}")
    print(f"points {len(N)}, groups {dict(cnt)}, parity max dev {parity_dev:.4f}, min font {min_pt}")
    if moved:
        print(f"old version kept as {moved}.*")


if __name__ == "__main__":
    main()
