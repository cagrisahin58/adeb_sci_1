#!/usr/bin/env python3
"""Source gap of the transformer relative to its CNN counterpart, split into symmetric and
directional parts (brief 12, section 6.4).

Double column (7.16 in), three panels side by side with a shared y axis (log units):
(a) CIFAR-10 seed pairs, (b) CIFAR-100 seed pairs, (c) ImageNetV2 same-recipe pairs (descriptive,
hatched). Each pair is a diverging stacked bar: the symmetric part sigma(CNN) - sigma(T) and the
directional part -(rho(CNN) - rho(T))/2 start at zero (a negative part goes below zero); the black
tick is the total gap D, and q = symmetric / D is printed above. In (c) the dashed line is the
registered denominator threshold (meta.delta); a pair with D at or below it has no interpretable q
and is printed as "q n/a".

Inputs: results/q1/konsey_ayrisim_b2.json, results/q1/konsey_b9_c100/b9_dondurulmus_b2.json,
results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json (b2.F_B2.K-a.{ciftler, D, simetrik_pay,
yonlu_pay, q, payda_kucuk_tohumlar}, meta.delta). Every drawn value is compared with
results/C1_REFERANS_FOYU.md (lines 1587, 1593, 1838, 1848, 1930-1932) before anything is written.

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_source_gap_split.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_source_gap_split.py"
J2P = "results/q1/konsey_ayrisim_b2.json"
J9P = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
J8P = "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json"
SETS = [  # key, file, title, foy rows (q line / anchor, detail line / anchor or per-pair lines), descriptive
    ("c10", J2P, "CIFAR-10", "seed pair"),
    ("c100", J9P, "CIFAR-100", "seed pair"),
    ("in", J8P, "ImageNetV2 (descriptive)", "model pair"),
]
FOY_IN_PAIR = {0: 1930, 1: 1931, 2: 1932}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_source_gap_split")
    ap.add_argument("--width-in", type=float, default=K.DOUBLE_IN)
    ap.add_argument("--height-in", type=float, default=2.6)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

    foy = K.Foy()
    data = {}
    for key, path, title, xl in SETS:
        J = K.load_json(path)
        Ka = K.dig(J, "b2.F_B2.K-a")
        n = len(Ka["ciftler"])
        for f in ("D", "simetrik_pay", "yonlu_pay", "q"):
            if len(Ka[f]) != n:
                K.fail(f"{path}: K-a.{f} length {len(Ka[f])} != {n} pairs")
        for i in range(n):
            foy.esit(f"{key}[{i}] D == sym + dir", Ka["D"][i], Ka["simetrik_pay"][i] + Ka["yonlu_pay"][i], 1e-12,
                     "identity of the source-gap split")
            foy.esit(f"{key}[{i}] q == sym / D", Ka["q"][i], Ka["simetrik_pay"][i] / Ka["D"][i], 1e-12,
                     "symmetric ratio definition")
        data[key] = {"ciftler": Ka["ciftler"], "D": Ka["D"], "sym": Ka["simetrik_pay"], "dir": Ka["yonlu_pay"],
                     "q": Ka["q"], "payda_kucuk": list(Ka["payda_kucuk_tohumlar"]), "delta": K.dig(J, "meta.delta")}
    # foy: CIFAR-10 (1587 q_s, 1593 D/sym/dir), CIFAR-100 (1838 q_s, 1848), ImageNetV2 (1930-1932)
    for key, ql, qa, dl, da in (("c10", 1587, "| K-a, simetrik oran", 1593, "K-a ayrintisi"),
                                ("c100", 1838, "| K-a, simetrik oran", 1848, "K-a ayrintisi")):
        d = data[key]
        for i in range(3):
            foy.kontrol(f"{key}.q[{i}]", d["q"][i], ql, qa, 3)
            foy.kontrol(f"{key}.D[{i}]", d["D"][i], dl, da, 3)
            foy.kontrol(f"{key}.sym[{i}]", d["sym"][i], dl, da, 3)
            foy.kontrol(f"{key}.dir[{i}]", d["dir"][i], dl, da, 3)
        foy.metin(f"{key}.payda kurali", "payda kurali tetiklenen tohum", dl, da)
        if d["payda_kucuk"]:
            K.fail(f"{key}: unexpected small-denominator seeds {d['payda_kucuk']}")
    d = data["in"]
    for i, n in FOY_IN_PAIR.items():
        cnn, tr = d["ciftler"][i]
        anc = f"| {i + 1} | {cnn} | {tr} |"
        foy.kontrol(f"in.D[{i}]", d["D"][i], n, anc, 4)
        foy.kontrol(f"in.sym[{i}]", d["sym"][i], n, anc, 3)
        foy.kontrol(f"in.dir[{i}]", d["dir"][i], n, anc, 3)
        foy.kontrol(f"in.q[{i}]", d["q"][i], n, anc, 3)
    foy.metin("in.payda kurali cift 3", "payda kurali tetiklenen cift: cift 3", 1945, "Dondurulmus betigin B8 ciktisi")
    foy.metin("in.payda esigi", "payda kurali D_k <= 0.1", 1926, "Cift duzeyi")
    for i in range(3):
        small = d["D"][i] <= d["delta"]
        if small != (i in d["payda_kucuk"]):
            K.fail(f"in pair {i}: D <= delta is {small} but payda_kucuk_tohumlar = {d['payda_kucuk']}")
    foy_sonuc = foy.bitir()

    # ---- figure ----
    K.style(args.seed)
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    left, right, bottom, top = 0.075, 0.995, 0.36, 0.865
    gap = 0.035
    pw = (right - left - 2 * gap) / 3
    axs = []
    for k in range(3):
        ax = fig.add_axes([left + k * (pw + gap), bottom, pw, top - bottom], sharey=axs[0] if axs else None)
        axs.append(ax)
    allv = [v for key in data for v in data[key]["sym"] + data[key]["dir"] + data[key]["D"]]
    ymin, ymax = min(0.0, min(allv)), max(allv)
    cizilen = {}
    for ax, (key, path, title, xl) in zip(axs, SETS):
        d = data[key]
        desc = key == "in"
        xs = list(range(len(d["D"])))
        for x, s_, r_, D_, q_ in zip(xs, d["sym"], d["dir"], d["D"], d["q"]):
            pos = [("sym", s_), ("dir", r_)]
            up, dn = 0.0, 0.0
            for comp, v in pos:
                base = up if v >= 0 else dn
                ax.bar(x, v, bottom=base, width=0.62, color=K.COL[comp], edgecolor=K.INK, linewidth=0.5,
                       hatch=("////" if desc else None), zorder=3)
                if v >= 0:
                    up += v
                else:
                    dn += v
            ax.plot([x - 0.38, x + 0.38], [D_, D_], color="black", lw=1.6, solid_capstyle="butt", zorder=4)
            lab = "q n/a" if (desc and xs.index(x) in d["payda_kucuk"]) else f"q = {q_:.3f}"
            ax.text(x, max(up, D_) + 0.012, lab, ha="center", va="bottom", fontsize=8)
        if desc:
            ax.axhline(d["delta"], color=K.MUTE, lw=0.8, ls=(0, (3, 2)), zorder=2)
        ax.axhline(0.0, color=K.EDGE, lw=0.6, zorder=2)
        ax.set_xticks(xs)
        if desc:
            ax.set_xticklabels([f"{i + 1}" for i in xs])
        else:
            ax.set_xticklabels([f"{i + 1}" for i in xs])
        ax.set_xlabel(xl, labelpad=2)
        ax.set_xlim(-0.6, len(xs) - 0.4)
        ax.set_title(title, fontsize=9, pad=3)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        cizilen[key] = [{"cift": list(c), "D": round(D_, 6), "simetrik_pay": round(s_, 6), "yonlu_pay": round(r_, 6),
                         "q": round(q_, 6), "q_yazildi": not (desc and i in d["payda_kucuk"])}
                        for i, (c, D_, s_, r_, q_) in enumerate(zip(d["ciftler"], d["D"], d["sym"], d["dir"], d["q"]))]
    axs[0].set_ylim(ymin - 0.03, ymax + 0.085)
    axs[0].yaxis.set_major_locator(mticker.MultipleLocator(0.1))
    axs[0].set_ylabel("Source gap (log units)", labelpad=3)
    for ax in axs[1:]:
        ax.tick_params(labelleft=False)
    for ax, lab in zip(axs, ("(a)", "(b)", "(c)")):
        bb = ax.get_position()
        K.panel_label(fig, bb.x0 - (0.07 if ax is axs[0] else 0.028), top + 0.075, lab)
    handles = [Patch(facecolor=K.COL["sym"], edgecolor=K.INK, lw=0.5, label=r"symmetric part $\sigma_{\mathrm{CNN}}-\sigma_{\mathrm{T}}$"),
               Patch(facecolor=K.COL["dir"], edgecolor=K.INK, lw=0.5, label=r"directional part $-\frac{1}{2}(\rho_{\mathrm{CNN}}-\rho_{\mathrm{T}})$"),
               Line2D([], [], color="black", lw=1.6, label="total gap $D$"),
               Patch(facecolor="white", edgecolor=K.INK, lw=0.5, hatch="////", label="descriptive (no decision)"),
               Line2D([], [], color=K.MUTE, lw=0.8, ls=(0, (3, 2)), label="registered $D$ threshold")]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False,
               handletextpad=0.4, columnspacing=1.2, labelspacing=0.3, handlelength=1.6)

    min_pt = K.layout_checks(fig)
    R = fig.canvas.get_renderer()
    leg = fig.legends[0].get_window_extent(R)
    for ax in axs:
        if leg.overlaps(ax.get_tightbbox(R)):
            K.fail("legend overlaps an axes")
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    okunan = {p: ["b2.F_B2.K-a.{ciftler, D, simetrik_pay, yonlu_pay, q, payda_kucuk_tohumlar}", "meta.delta"]
              for p in (J2P, J9P, J8P)}
    cizilen["esik_D (c)"] = data["in"]["delta"]
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], [J2P, J9P, J8P], (W, H), args.dpi, min_pt,
                       okunan, cizilen, foy_sonuc,
                       ["D == symmetric + directional (1e-12) and q == symmetric / D (1e-12) for every pair",
                        "CIFAR-10 q_s vs foy 1587, D/sym/dir vs 1593; CIFAR-100 vs 1838 and 1848 (3 dp)",
                        "ImageNetV2 D (4 dp), sym, dir, q (3 dp) vs foy 1930-1932; small-denominator pair 3 vs 1945",
                        "D <= meta.delta agrees with payda_kucuk_tohumlar for every ImageNetV2 pair",
                        "no text overlap, all text inside, >= 8 pt, legend clear of axes, no Type 3 font"],
                       ["Pair 3 of ImageNetV2 (Liu ConvNeXt-B / Swin-B) has D at or below the registered 0.10 "
                        "denominator threshold; its q (0.547 in the sheet) is not printed on the figure.",
                        "Negative components are stacked downward from zero (ImageNetV2 pair 1 directional part).",
                        "x tick labels are pair indices: CIFAR seed pairs 1-3 are C1 pairs (ResNet s1001-s1003 / "
                        "ViT s2001-s2003); ImageNetV2 pairs 1-3 are Singh ConvNeXt-T/ViT-S, Singh ConvNeXt-B/ViT-B, "
                        "Liu ConvNeXt-B/Swin-B."],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
