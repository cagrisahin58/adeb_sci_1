#!/usr/bin/env python3
"""Decomposition schematic (brief 12, section 6.2). No data: symbols only.

One column (3.5 in), read top to bottom. (1) The two-model target-correct transfer matrix T with the
white-box vulnerabilities w on the diagonal, next to the definitions of the symmetric similarity
log tau_ij and the directional residual r_ij. (2) The exact split
log T_ij = log w_j + log tau_ij + r_ij / 2. (3) Averages over a fixed CNN panel P give the model-level
similarity sigma_m and direction rho_m. (4) The panel source gap of V relative to R is a symmetric
part plus a directional part. Colours follow the council palette (similarity green, direction
orange); every coloured term also carries a word label, so the figure reads in grey scale.

Self-check (not drawn): on seeded random positive matrices the script confirms that the identity
in (2) holds exactly and that the panel source gap equals the expression in (4); the figure is not
written otherwise.

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_decomposition_schematic.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_decomposition_schematic.py"
GREY = "#e4e4e4"


def identity_check(seed, trials=200):
    """Random positive rates for 2 models + a panel of 5: identity (2) and gap formula (4)."""
    rng = np.random.default_rng(seed)
    worst_id, worst_gap = 0.0, 0.0
    for _ in range(trials):
        n = 7  # models 0 = R, 1 = V, 2..6 = panel
        T = rng.uniform(0.05, 0.95, size=(n, n))
        w = np.diag(T).copy()
        L = np.log(T)
        lw = np.log(w)
        ltau = 0.5 * (L + L.T - lw[:, None] - lw[None, :])
        r = (L - L.T) - (lw[None, :] - lw[:, None])          # r_ij = log(T_ij/T_ji) - log(w_j/w_i)
        rec = lw[None, :] + ltau + 0.5 * r
        off = ~np.eye(n, dtype=bool)
        worst_id = max(worst_id, float(np.abs(rec - L)[off].max()))
        P = list(range(2, n))
        sig = {m: ltau[m, P].mean() for m in (0, 1)}
        rho = {m: r[P, m].mean() for m in (0, 1)}               # rho_m = mean_c r_cm
        G = L[0, P].mean() - L[1, P].mean()                     # panel source gap of V relative to R
        worst_gap = max(worst_gap, abs(G - ((sig[0] - sig[1]) - 0.5 * (rho[0] - rho[1]))))
    return float(worst_id), float(worst_gap)


def place_row(fig, R, y, items, gap_in, W):
    """Place [(text, colour, label or None, fontsize)] centred on the figure at height y (fig coords).
    Each slot is as wide as the larger of its term and its label; returns created text objects."""
    tmp = []
    for txt, col, lab, fs in items:
        t = fig.text(0, y, txt, color=col, fontsize=fs, ha="left", va="baseline")
        lt = fig.text(0, y, lab, fontsize=8, ha="center", va="top", color=col) if lab else None
        tmp.append((t, lt))
    fig.canvas.draw()
    widths = []
    for t, lt in tmp:
        wt = t.get_window_extent(R).width
        wl = lt.get_window_extent(R).width if lt else 0.0
        widths.append((wt, max(wt, wl)))
    gap = gap_in * fig.dpi
    total = sum(s for _, s in widths) + gap * (len(widths) - 1)
    x = (W * fig.dpi - total) / 2
    for (t, lt), (wt, slot) in zip(tmp, widths):
        cx = x + slot / 2
        t.set_x((cx - wt / 2) / (W * fig.dpi))
        if lt:
            lt.set_x(cx / (W * fig.dpi))
            lt.set_y(y - 0.035)
        x += slot + gap
    return tmp


def arrow(fig, x, y0, y1):
    fig.add_artist(FancyArrowPatch((x, y0), (x, y1), transform=fig.transFigure, arrowstyle="-|>",
                                   mutation_scale=8, lw=0.8, color=K.EDGE))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_decomposition_schematic")
    ap.add_argument("--width-in", type=float, default=K.SINGLE_IN)
    ap.add_argument("--height-in", type=float, default=3.55)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261031, help="seed of the random self-check")
    args = ap.parse_args()

    wid, wgap = identity_check(args.seed)
    if wid > 1e-12 or wgap > 1e-12:
        K.fail(f"identity self-check failed: {wid}, {wgap}")
    foy = K.Foy()
    foy.esit("identity log T = log w_j + log tau + r/2 (max abs residual, random matrices)", wid, 0.0, 1e-12,
             "algebraic self-check, not a result")
    foy.esit("gap G = (sigma_R - sigma_V) - (rho_R - rho_V)/2 (max abs residual)", wgap, 0.0, 1e-12,
             "algebraic self-check, not a result")
    foy_sonuc = foy.bitir()

    K.style(0)
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    R = fig.canvas.get_renderer()
    sym, dr = K.COL["sym"], K.COL["dir"]

    # (1) matrix
    ax = fig.add_axes([0.20, 0.625, 0.24, 0.24 * W / H])
    cells = {(0, 0): (r"$w_R$", GREY), (0, 1): (r"$T_{RV}$", "white"), (1, 0): (r"$T_{VR}$", "white"),
             (1, 1): (r"$w_V$", GREY)}
    for (i, j), (s, fc) in cells.items():
        ax.add_patch(Rectangle((j, i), 1, 1, fc=fc, ec=K.INK, lw=0.7, clip_on=False))
        ax.text(j + 0.5, i + 0.5, s, ha="center", va="center", fontsize=9)
    ax.set_xlim(0, 2)
    ax.set_ylim(2, 0)
    ax.set_xticks([0.5, 1.5])
    ax.set_xticklabels(["R", "V"])
    ax.set_yticks([0.5, 1.5])
    ax.set_yticklabels(["R", "V"])
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=2)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xlabel("target $j$", labelpad=6)
    ax.xaxis.set_label_position("top")
    ax.set_ylabel("source $i$", labelpad=3)
    fig.text(0.53, 0.83, r"$\log\bar\tau_{ij}=\frac{1}{2}\log\frac{T_{ij}\,T_{ji}}{w_i\,w_j}$", color=sym, fontsize=9,
             ha="left", va="center")
    fig.text(0.53, 0.735, r"$r_{ij}=\log\frac{T_{ij}\,w_i}{T_{ji}\,w_j}$", color=dr, fontsize=9, ha="left", va="center")
    fig.text(0.53, 0.665, "diagonal: white-box rate", fontsize=8, ha="left", va="center", color=K.MUTE)
    arrow(fig, 0.5, 0.64, 0.605)

    # (2) exact split
    place_row(fig, R, 0.55, [(r"$\log T_{ij}$", K.INK, None, 9), ("=", K.INK, None, 9),
                              (r"$\log w_j$", K.INK, "vulnerability", 9), ("+", K.INK, None, 9),
                              (r"$\log\bar\tau_{ij}$", sym, "similarity", 9), ("+", K.INK, None, 9),
                              (r"$\frac{1}{2}\,r_{ij}$", dr, "direction", 9)], 0.06, W)
    fig.text(0.5, 0.445, r"mean over a fixed CNN panel $c\in P$", fontsize=8, ha="center", va="center", color=K.MUTE)
    arrow(fig, 0.5, 0.42, 0.385)

    # (3) panel averages
    place_row(fig, R, 0.33, [(r"$\sigma_m=\overline{\log\bar\tau_{mc}}$", sym, "panel similarity", 9),
                             (r"$\rho_m=\overline{r_{cm}}$", dr, "direction ($m$ as target)", 9)], 0.28, W)
    arrow(fig, 0.5, 0.235, 0.19)

    # (4) source gap
    place_row(fig, R, 0.125, [(r"$G$", K.INK, "source gap", 9), ("=", K.INK, None, 9),
                              (r"$(\sigma_R-\sigma_V)$", sym, "symmetric part", 9),
                              (r"$-\,\frac{1}{2}(\rho_R-\rho_V)$", dr, "directional part", 9)], 0.11, W)
    for lab, y in (("(1)", 0.955), ("(2)", 0.565), ("(3)", 0.345), ("(4)", 0.14)):
        K.panel_label(fig, 0.01, y, lab, va="center")

    min_pt = K.layout_checks(fig)
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], [], (W, H), args.dpi, min_pt, {},
                       {"veri": "yok; yalniz semboller ve tanimlar (brif 6.2)"}, foy_sonuc,
                       [f"identity (2) on {200} seeded random 7-model matrices: max abs residual {wid:.1e}",
                        f"gap formula (4) on the same matrices: max abs residual {wgap:.1e}",
                        "no text overlap, all text inside, >= 8 pt, no Type 3 font"],
                       ["No number from any result file is drawn; the only numerals are the 1/2 of the definitions.",
                        "Overline denotes the mean over panel members c in P (for a panel member, P without itself), "
                        "as in brief 12 section 3.1; the caption should say so.",
                        "rho_m = mean_c r_cm: positive rho_m means m is directionally the weaker source."],
                       moved, extra={"rastgele_denetim_tohumu": args.seed})
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"self-check residuals {wid:.1e}, {wgap:.1e}; min font {min_pt}")


if __name__ == "__main__":
    main()
