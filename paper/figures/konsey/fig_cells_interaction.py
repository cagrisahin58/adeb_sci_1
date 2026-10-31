#!/usr/bin/env python3
"""Two-by-two design on CIFAR-10: cell means and runs of sigma, rho and omega (brief 12, section 6.3).

One column (3.5 in), three panels stacked, shared x = initialization (scratch, ImageNet).
(a) panel similarity sigma, (b) directional term rho with the +-delta equivalence band,
(c) vulnerability omega = log w. Lines join the cell means of ViT-Tiny and of ResNet-18 (224 px);
small markers are the individual runs; open squares in (a) and (b) are the three 32-pixel
ResNet-18 runs (bridge cell R32). R32 is absent from (c) because its per-run omega is not in the
reference sheet (brief 12, section 9 rule: nothing outside the sheet is drawn).

Inputs (quarantine-safe): results/q1/konsey_ayrisim_b4.json (b4.model_tablosu.<m>.yari_log,
b4.F_B4.karsitliklar, meta.delta), results/q1/konsey_ayrisim_b2.json (b2.F_B2.K-a, K-b, K-c; only
for the R32 identity checks), raporlar/konsey_2026-10-29/hucre_tablosu.json (modeller.<m>.hucre).
Every drawn value is compared with results/C1_REFERANS_FOYU.md before anything is written.

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_cells_interaction.py
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

SCRIPT_REL = "paper/figures/konsey/fig_cells_interaction.py"
J4P = "results/q1/konsey_ayrisim_b4.json"
J2P = "results/q1/konsey_ayrisim_b2.json"
HTP = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
CELLS = {"V-scr": ("vit", "scr"), "V-IN": ("vit", "IN"), "R224-scr": ("r224", "scr"), "R224-IN": ("r224", "IN")}
# foy M9.2 lines (31.10.2026 sheet): cell summary rows and per-run rows
FOY_CELL = {"V-scr": 1496, "V-IN": 1497, "R224-scr": 1498, "R224-IN": 1499}
FOY_RUN = {"ViT_Tiny_AT_s2001": 1505, "ViT_Tiny_AT_s2002": 1506, "ViT_Tiny_AT_s2003": 1507,
           "V_IN_s2101": 1508, "V_IN_s2102": 1509, "R224_scr_s1201": 1510, "R224_scr_s1202": 1511,
           "R224_IN_s1301": 1512, "R224_IN_s1302": 1513}


def mean(v):
    return sum(v) / len(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_cells_interaction")
    ap.add_argument("--width-in", type=float, default=K.SINGLE_IN)
    ap.add_argument("--height-in", type=float, default=4.75)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

    J4, J2, HT = K.load_json(J4P), K.load_json(J2P), K.load_json(HTP)
    foy = K.Foy()
    MT = K.dig(J4, "b4.model_tablosu")
    hucre = {m: v["hucre"] for m, v in K.dig(HT, "modeller").items()}
    runs = {c: sorted(m for m in MT if hucre.get(m) == c) for c in list(CELLS) + ["C1-R32"]}
    for c in CELLS:
        if runs[c] != sorted(K.dig(J4, f"b4.hucreler.{c}")):
            K.fail(f"cell {c}: hucre_tablosu runs {runs[c]} != b4.hucreler")
    r32 = runs["C1-R32"]
    if len(r32) != 3:
        K.fail(f"expected three R32 runs, got {r32}")
    q = ("sigma", "rho", "omega")
    val = {m: {k: K.dig(MT, f"{m}.yari_log.{k}") for k in q} for m in MT}

    # ---- foy comparisons: runs, cell means, contrasts, delta ----
    for m, n in FOY_RUN.items():
        for k in q:
            foy.kontrol(f"{m}.{k}", val[m][k], n, f"| {m} |", 3)
    cm = {c: {k: mean([val[m][k] for m in runs[c]]) for k in q} for c in CELLS}
    for c, n in FOY_CELL.items():
        foy.metin(f"{c}.n", f"| {c} | {len(runs[c])} |", n, f"| {c} |")
        for k in q:
            foy.kontrol(f"{c}.{k}_ort", cm[c][k], n, f"| {c} |", 3)
    H = K.dig(J4, "b4.F_B4.karsitliklar")
    for c in CELLS:
        foy.esit(f"{c}.sigma_ort == H2.hucre_ort", cm[c]["sigma"], H["H2"]["hucre_ort"][c], 1e-12,
                 "cell mean recomputed from runs equals the frozen script's cell mean")
        foy.esit(f"{c}.rho_ort == H3.hucre_ort", cm[c]["rho"], H["H3"]["hucre_ort"][c], 1e-12,
                 "cell mean recomputed from runs equals the frozen script's cell mean")
    A = H["H1"]["kestirim"]
    I = H["H2"]["kestirim"]
    foy.kontrol("H1.kestirim", A, 1526, "| H1, A^sigma_scr", 3)
    foy.kontrol("H2.kestirim", I, 1527, "| H2, I^sigma", 3)
    foy.esit("H1 == sigma(V-scr) - sigma(R224-scr)", A, cm["V-scr"]["sigma"] - cm["R224-scr"]["sigma"], 1e-12,
             "contrast recomputed from cell means")
    foy.esit("H2 == interaction of cell means", I,
             (cm["V-IN"]["sigma"] - cm["V-scr"]["sigma"]) - (cm["R224-IN"]["sigma"] - cm["R224-scr"]["sigma"]),
             1e-12, "contrast recomputed from cell means")
    delta = K.dig(J4, "meta.delta")
    foy.metin("meta.delta", f"delta = {delta}", 1532, "TOST esdegerlik siniri")
    # R32 bridge runs: sigma and rho through the B2 identities, s1001 directly, cell mean through S1
    Ka, Kb, Kc = K.dig(J2, "b2.F_B2.K-a"), K.dig(J2, "b2.F_B2.K-b"), K.dig(J2, "b2.F_B2.K-c")
    for s, (rm, vm) in enumerate(Ka["ciftler"]):
        foy.kontrol(f"K-a.simetrik_pay[{s}]", Ka["simetrik_pay"][s], 1593, "K-a ayrintisi", 3)
        foy.kontrol(f"K-a.yonlu_pay[{s}]", Ka["yonlu_pay"][s], 1593, "K-a ayrintisi", 3)
        foy.kontrol(f"K-c.sigma_V[{vm}]", Kc["sigma_V"][vm], 1595, "K-c ayrintisi", 3)
        foy.kontrol(f"K-b.degerler[{s}]", Kb["degerler"][s], 1588, "| K-b, ViT yonlu terimi", 3)
        foy.esit(f"sigma({rm}) == sigma_V + simetrik_pay", val[rm]["sigma"],
                 Kc["sigma_V"][vm] + Ka["simetrik_pay"][s], 1e-9, "B2 identity: symmetric part = sigma(R) - sigma(V)")
        foy.esit(f"rho({rm}) == rho_V - 2 yonlu_pay", val[rm]["rho"],
                 Kb["degerler"][s] - 2 * Ka["yonlu_pay"][s], 1e-9, "B2 identity: directional part = -(rho(R) - rho(V))/2")
    foy.kontrol("ResNet18_AT_s1001.sigma (B4 column)", val["ResNet18_AT_s1001"]["sigma"], 1745, "| ResNet18_AT_s1001 |", 3)
    foy.kontrol("ResNet18_AT_s1001.rho (B4 column)", val["ResNet18_AT_s1001"]["rho"], 1745, "| ResNet18_AT_s1001 |", 3)
    s1s = mean([val[m]["sigma"] for m in runs["R224-scr"]]) - mean([val[m]["sigma"] for m in r32])
    s1r = mean([val[m]["rho"] for m in runs["R224-scr"]]) - mean([val[m]["rho"] for m in r32])
    foy.kontrol("S1 sigma = sigma(R224-scr) - sigma(R32)", s1s, 1561, "| S1, kopru sigma", 4)
    foy.kontrol("S1 rho = rho(R224-scr) - rho(R32)", s1r, 1562, "| S1, kopru rho", 3)
    foy_sonuc = foy.bitir()

    # ---- figure ----
    K.style(args.seed)
    W, Hh = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, Hh))
    fig.patch.set_facecolor("white")
    left, right = 0.215, 0.975
    hs = [0.26, 0.205, 0.18]
    tops = [0.950, 0.655, 0.400]
    axs = [fig.add_axes([left, t - h, right - left, h]) for t, h in zip(tops, hs)]
    X = {"scr": 0.0, "IN": 1.0}
    OFF = {"vit": -0.07, "r224": 0.07}
    STY = {"vit": dict(marker="^", ls="-", ms_mean=6.4), "r224": dict(marker="o", ls=(0, (4, 2)), ms_mean=6.0)}
    cizilen = {"hucre_ortalamalari": {}, "kosular": {}, "r32_kopru": {}}
    for ax, k in zip(axs, q):
        for arch in ("vit", "r224"):
            cells = [c for c in CELLS if CELLS[c][0] == arch]
            xs = [X[CELLS[c][1]] + OFF[arch] for c in cells]
            ys = [cm[c][k] for c in cells]
            ax.plot(xs, ys, color=K.COL[arch], ls=STY[arch]["ls"], lw=1.1, marker=STY[arch]["marker"],
                    ms=STY[arch]["ms_mean"], mfc=K.COL[arch], mec=K.INK, mew=0.5, zorder=4)
            for c in cells:
                rs = runs[c]
                for i, m in enumerate(rs):
                    dx = (i - (len(rs) - 1) / 2) * 0.045
                    xx = X[CELLS[c][1]] + OFF[arch] * 2.6 + dx
                    ax.plot([xx], [val[m][k]], ls="none", marker=STY[arch]["marker"], ms=3.2,
                            mfc="white", mec=K.COL[arch], mew=0.9, zorder=5)
                    cizilen["kosular"].setdefault(m, {})[k] = round(val[m][k], 6)
                cizilen["hucre_ortalamalari"].setdefault(c, {})[k] = round(cm[c][k], 6)
        if k in ("sigma", "rho"):
            for i, m in enumerate(r32):
                xx = -0.42 + (i - 1) * 0.045
                ax.plot([xx], [val[m][k]], ls="none", marker="s", ms=3.4, mfc="white", mec=K.COL["r32"],
                        mew=1.0, zorder=5)
                cizilen["r32_kopru"].setdefault(m, {})[k] = round(val[m][k], 6)
        ax.set_xlim(-0.62, 1.38)
        ax.set_xticks([X["scr"], X["IN"]])
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    axs[1].axhspan(-delta, delta, color="#e4e4e4", lw=0, zorder=0)
    axs[1].axhline(0.0, color=K.ZERO, lw=0.6, ls=(0, (4, 2)), zorder=1)
    for ax in axs[:2]:
        ax.tick_params(labelbottom=False)
    axs[2].set_xticklabels(["scratch", "ImageNet"])
    axs[2].set_xlabel("Initialization", labelpad=2)
    axs[0].set_ylabel(r"Panel similarity $\sigma$", labelpad=3)
    axs[1].set_ylabel(r"Direction $\rho$", labelpad=3)
    axs[2].set_ylabel(r"$\omega=\log w$", labelpad=3)
    for ax, step in zip(axs, (0.1, 0.05, 0.05)):
        ax.yaxis.set_major_locator(mticker.MultipleLocator(step))
    fig.align_ylabels(axs)

    def f3(v):
        return f"{v:+.3f}".replace("-", "−")
    axs[0].text(0.98, 0.05, r"$A^{\sigma}_{\mathrm{scr}}$ = " + f3(A) + "\n" + r"$I^{\sigma}$ = " + f3(I),
                transform=axs[0].transAxes, ha="right", va="bottom", fontsize=8, linespacing=1.4)
    for ax, lab in zip(axs, ("(a)", "(b)", "(c)")):
        bb = ax.get_position()
        K.panel_label(fig, 0.008, bb.y1 + 0.008, lab, va="bottom")

    hv = Line2D([], [], color=K.COL["vit"], ls="-", lw=1.1, marker="^", ms=5.5, mfc=K.COL["vit"], mec=K.INK,
                mew=0.5, label="ViT-Tiny, cell mean")
    hr = Line2D([], [], color=K.COL["r224"], ls=(0, (4, 2)), lw=1.1, marker="o", ms=5.0, mfc=K.COL["r224"],
                mec=K.INK, mew=0.5, label="ResNet-18 (224), cell mean")
    hrun = Line2D([], [], ls="none", marker="o", ms=3.4, mfc="white", mec=K.MUTE, mew=0.9, label="single run")
    h32 = Line2D([], [], ls="none", marker="s", ms=3.4, mfc="white", mec=K.COL["r32"], mew=1.0,
                 label="R32 bridge run")
    hb = Patch(facecolor="#e4e4e4", edgecolor="none", label=r"$\pm\delta$ band (b)")
    fig.legend(handles=[hv, hr, hrun, h32, hb], loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2,
               frameon=False, handletextpad=0.4, columnspacing=1.0, labelspacing=0.35, handlelength=1.9)

    min_pt = K.layout_checks(fig)
    leg = fig.legends[0].get_window_extent(fig.canvas.get_renderer())
    for ax in axs:
        if leg.overlaps(ax.get_tightbbox(fig.canvas.get_renderer())):
            K.fail("legend overlaps an axes")
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    okunan = {J4P: ["b4.model_tablosu.<m>.yari_log.{sigma, rho, omega}", "b4.hucreler.<cell>",
                    "b4.F_B4.karsitliklar.H1.kestirim", "b4.F_B4.karsitliklar.H2.{kestirim, hucre_ort}",
                    "b4.F_B4.karsitliklar.H3.hucre_ort", "meta.delta"],
              J2P: ["b2.F_B2.K-a.{ciftler, simetrik_pay, yonlu_pay}", "b2.F_B2.K-b.degerler",
                    "b2.F_B2.K-c.sigma_V (R32 identity checks only)"],
              HTP: ["modeller.<m>.hucre"]}
    cizilen["ek_aciklama"] = {"A_sigma_scr (H1)": round(A, 6), "I_sigma (H2)": round(I, 6), "delta_bandi": delta}
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], [J4P, J2P, HTP], (W, Hh), args.dpi, min_pt,
                       okunan, cizilen, foy_sonuc,
                       ["cell runs from hucre_tablosu == b4.hucreler", "every run value vs foy 1505-1513 (3 dp)",
                        "cell means vs foy 1496-1499 and == frozen H2/H3 hucre_ort (1e-12)",
                        "H1, H2 vs foy 1526-1527 and recomputed from cell means (1e-12)",
                        "R32 sigma, rho through B2 identities (1e-9) with K-a/K-b/K-c parts vs foy 1588, 1593, 1595",
                        "R32 s1001 vs foy 1745; R32 mean through S1 vs foy 1561-1562",
                        "no text overlap, all text inside, >= 8 pt, legend clear of axes, no Type 3 font"],
                       ["R32 omitted from panel (c): per-run omega of the 32-pixel ResNet-18 is not in the reference sheet",
                        "x positions are categorical (scratch, ImageNet) with fixed horizontal offsets; no jitter, no randomness"],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
