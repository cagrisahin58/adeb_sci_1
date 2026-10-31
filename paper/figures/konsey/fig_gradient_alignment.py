#!/usr/bin/env python3
"""Input-gradient cosine c_ij against pairwise symmetric similarity log tau_ij (brief 12, section 6.6).

Change log (degisiklik notu):
- 2026-10-31: width 6.989 in (= textwidth of ieeeaccess.cls, see konsey_ortak.py), so the figure
  prints at scale 1.00 and 8 pt text stays 8 pt. Drawn values, layout fractions and labels
  unchanged; panel letters (a)-(c) raw and (d)-(f) residual already match the caption as revised
  by the author (hakem konseyi m15, caption side).
- 2026-10-31: height 4.9 -> 4.78 in, the printed height of the 7.16 x 4.9 in draft at textwidth;
  at 4.9 in the float page with Table 11 overflowed by 1.3 pt (Overfull vbox in main.log).

Double column (6.989 in), 2 x 3 panels. Columns: CIFAR-10, CIFAR-100, ImageNetV2. Top row: raw c_ij
against raw log tau_ij for every unordered model pair. Bottom row: the same pairs after additive
model main effects (X_ij = mu + a_i + a_j + e_ij, least squares over unordered pairs, ek on kayit
section 6.2) are removed from both matrices. Colour and marker encode the pair type from the
frozen cell tables' 'aile' field (CNN-CNN, transformer-transformer, mixed; transformer = any family
other than CNN). The Spearman correlation printed in each panel is the frozen value (sinamalar.ham /
sinamalar.ana_etki_artik.istatistik); the script recomputes both and requires agreement within
1e-3 with the reference sheet (lines 1970-1975) and within 1e-9 with the JSON before drawing.

Inputs (quarantine-safe): results/q1/konsey_b10_gradyan/mantel_{cifar10,cifar100,imagenetv2}.json
(c_matrisi, log_tau_matrisi, modeller_ortak, sinamalar.{ham, ana_etki_artik}.{K, istatistik}),
raporlar/konsey_2026-10-29/hucre_tablosu{,_b9,_b8}.json (modeller.<m>.aile).

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_gradient_alignment.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from scipy import stats  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_gradient_alignment.py"
SETS = [  # key, mantel json, cell table, title, foy lines (ham, ana_etki_artik), c summary line
    ("cifar10", "results/q1/konsey_b10_gradyan/mantel_cifar10.json", "raporlar/konsey_2026-10-29/hucre_tablosu.json",
     "CIFAR-10", (1970, 1971), 2009),
    ("cifar100", "results/q1/konsey_b10_gradyan/mantel_cifar100.json", "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
     "CIFAR-100", (1972, 1973), 2010),
    ("imagenetv2", "results/q1/konsey_b10_gradyan/mantel_imagenetv2.json", "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json",
     "ImageNetV2", (1974, 1975), 2011),
]
TYPES = [("CNN-CNN", "CNN–CNN", K.COL["r224"], "o"), ("T-T", "transformer–transformer", K.COL["vit"], "^"),
         ("mixed", "mixed", K.MUTE, "s")]


def ana_etki_artik(A):
    """Same additive main-effect residual as experiments/q1_ek_gradyan_kosinus.py (ek on kayit 6.2)."""
    n = A.shape[0]
    i, j = np.triu_indices(n, 1)
    X = np.zeros((len(i), n + 1))
    X[:, 0] = 1.0
    X[np.arange(len(i)), 1 + i] = 1.0
    X[np.arange(len(i)), 1 + j] = 1.0
    y = A[i, j]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta


def spearman(a, b):
    return float(stats.spearmanr(a, b).statistic)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_gradient_alignment")
    ap.add_argument("--width-in", type=float, default=K.DOUBLE_IN)
    ap.add_argument("--height-in", type=float, default=4.78)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

    foy = K.Foy()
    data, okunan, inputs = {}, {}, []
    for key, mp, hp, title, (lh, lr), lc in SETS:
        Mj, Hj = K.load_json(mp), K.load_json(hp)
        inputs += [mp, hp]
        okunan[mp] = ["c_matrisi", "log_tau_matrisi", "modeller_ortak", "dislanan",
                      "sinamalar.{ham, ana_etki_artik}.{K, cift_sayisi, istatistik}"]
        okunan[hp] = ["modeller.<m>.aile"]
        mods = list(K.dig(Mj, "modeller_ortak"))
        if K.dig(Mj, "dislanan"):
            K.fail(f"{key}: excluded models present")
        C = np.array(K.dig(Mj, "c_matrisi"), float)
        T = np.array(K.dig(Mj, "log_tau_matrisi"), float)
        HT = K.dig(Hj, "modeller")
        n = len(mods)
        if C.shape != (n, n) or T.shape != (n, n) or set(mods) != set(HT):
            K.fail(f"{key}: matrix shape or model set mismatch")
        foy.esit(f"{key}: max |C - C^T|", float(np.abs(C - C.T).max()), 0.0, 0.0, "c matrix symmetric")
        i, j = np.triu_indices(n, 1)
        c, t = C[i, j], T[i, j]
        if not (np.all(np.isfinite(c)) and np.all(np.isfinite(t))):
            K.fail(f"{key}: non-finite entries")
        cr, tr = ana_etki_artik(C), ana_etki_artik(T)
        rs_h, rs_r = spearman(c, t), spearman(cr, tr)
        S = K.dig(Mj, "sinamalar")
        foy.esit(f"{key}: recomputed raw Spearman == JSON", rs_h, S["ham"]["istatistik"], 1e-9, "raw Mantel statistic")
        foy.esit(f"{key}: recomputed residual Spearman == JSON", rs_r, S["ana_etki_artik"]["istatistik"], 1e-9,
                 "main-effect residual Mantel statistic")
        foy.kontrol(f"{key}: raw r_S (recomputed, 1e-3)", rs_h, lh, f"| {key} | ham |", 3, tol=1e-3)
        foy.kontrol(f"{key}: residual r_S (recomputed, 1e-3)", rs_r, lr, f"| {key} | ana_etki_artik |", 3, tol=1e-3)
        foy.kontrol(f"{key}: K", n, lh, f"| {key} | ham |", 0)
        foy.kontrol(f"{key}: pairs", len(c), lh, f"| {key} | ham |", 0)
        foy.esit(f"{key}: pairs == JSON cift_sayisi", len(c), S["ham"]["cift_sayisi"], 0, "pair count")
        # pair types from the cell tables' family field; check means and counts against foy
        fam = [("CNN" if HT[m]["aile"] == "CNN" else "T") for m in mods]
        typ = np.array(["CNN-CNN" if fam[a] == fam[b] == "CNN" else ("T-T" if fam[a] == fam[b] == "T" else "mixed")
                        for a, b in zip(i, j)])
        for tk, _, _, _ in TYPES:
            sel = typ == tk
            foy.kontrol(f"{key}: mean c {tk}", float(c[sel].mean()), lc, f"| {key} |", 3)
            foy.kontrol(f"{key}: n {tk}", int(sel.sum()), lc, f"| {key} |", 0)
        foy.kontrol(f"{key}: mean c all", float(c.mean()), lc, f"| {key} |", 3)
        data[key] = {"title": title, "c": c, "t": t, "cr": cr, "tr": tr, "typ": typ, "rs_h": S["ham"]["istatistik"],
                     "rs_r": S["ana_etki_artik"]["istatistik"], "n": n}
    foy.metin("p at floor in 6/6", "Tek yonlu p'si p tabanina esit olan sinama: 6/6", 1977, "p tabanina esit")
    foy_sonuc = foy.bitir()

    # ---- figure ----
    K.style(args.seed)
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    left, right, gapx = 0.095, 0.99, 0.06
    pw = (right - left - 2 * gapx) / 3
    rows = [(0.615, 0.315), (0.15, 0.315)]  # (bottom, height)
    axs = [[fig.add_axes([left + k * (pw + gapx), b, pw, h]) for k in range(3)] for b, h in rows]
    cizilen = {}

    def f3(v):
        return f"{v:+.3f}".replace("-", "−")
    for k, (key, d) in enumerate(data.items()):
        for r, (xs, ys, rs, tag) in enumerate(((d["c"], d["t"], d["rs_h"], "raw"), (d["cr"], d["tr"], d["rs_r"], "residual"))):
            ax = axs[r][k]
            for tk, lab, col, mk in TYPES:
                sel = d["typ"] == tk
                ax.scatter(xs[sel], ys[sel], s=9, marker=mk, facecolor=col, edgecolor=K.INK, linewidth=0.25,
                           alpha=0.9, zorder=3 if tk != "mixed" else 2)
            if r == 1:
                ax.axhline(0, color=K.ZERO, lw=0.5, ls=(0, (3, 2)), zorder=1)
                ax.axvline(0, color=K.ZERO, lw=0.5, ls=(0, (3, 2)), zorder=1)
            ax.text(0.04 if r == 0 else 0.04, 0.95, r"$r_{\mathrm{S}}$ = " + f3(rs), transform=ax.transAxes,
                    ha="left", va="top", fontsize=8)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.locator_params(axis="both", nbins=4)
            cizilen.setdefault(key, {})[tag] = {"r_S_gosterilen": rs, "nokta_sayisi": int(len(xs)),
                                                "x_aralik": [float(xs.min()), float(xs.max())],
                                                "y_aralik": [float(ys.min()), float(ys.max())]}
        axs[0][k].set_title(d["title"], fontsize=9, pad=3)
        axs[0][k].set_xlabel(r"gradient cosine $c_{ij}$", labelpad=2)
        axs[1][k].set_xlabel(r"$c_{ij}$ residual", labelpad=2)
        cizilen[key]["cift_turu_sayilari"] = {tk: int((d["typ"] == tk).sum()) for tk, _, _, _ in TYPES}
    axs[0][0].set_ylabel(r"$\log\bar\tau_{ij}$", labelpad=3)
    axs[1][0].set_ylabel(r"$\log\bar\tau_{ij}$ residual", labelpad=3)
    fig.align_ylabels([axs[0][0], axs[1][0]])
    for ax in [a for row in axs for a in row]:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−")))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−")))
    labs = iter("abcdef")
    for row in axs:
        for ax in row:
            bb = ax.get_position()
            K.panel_label(fig, bb.x0 - (0.075 if ax in (axs[0][0], axs[1][0]) else 0.045), bb.y1 + 0.022,
                          f"({next(labs)})", va="bottom")
    handles = [Line2D([], [], ls="none", marker=mk, ms=4.5, mfc=col, mec=K.INK, mew=0.3, label=lab)
               for _, lab, col, mk in TYPES]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False,
               handletextpad=0.3, columnspacing=1.6)

    min_pt = K.layout_checks(fig)
    R = fig.canvas.get_renderer()
    leg = fig.legends[0].get_window_extent(R)
    for ax in [a for row in axs for a in row]:
        if leg.overlaps(ax.get_tightbbox(R)):
            K.fail("legend overlaps an axes")
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], inputs, (W, H), args.dpi, min_pt, okunan, cizilen,
                       foy_sonuc,
                       ["raw and main-effect-residual Spearman recomputed == JSON (1e-9) and == foy 1970-1975 (1e-3)",
                        "K and pair counts vs foy and JSON",
                        "pair-type c means and counts (CNN-CNN, transformer-transformer, mixed) vs foy 2009-2011: "
                        "confirms the family assignment used for colours",
                        "permutation p at floor in 6/6 vs foy 1977 (not drawn, caption refers to the table)",
                        "no text overlap, all text inside, >= 8 pt, legend clear of axes, no Type 3 font"],
                       ["Bottom-row residuals use the same least-squares additive model as the frozen gradient script; "
                        "they are drawn only because the recomputed statistic matches.",
                        "Pairs are drawn once (upper triangle). No jitter, no randomness."],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
