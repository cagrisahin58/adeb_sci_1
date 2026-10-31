#!/usr/bin/env python
"""Two-by-two design on CIFAR-10: cell means and runs of sigma, rho and omega; card figure,
visio-cizici style 7 (plan 04_cizim_plani.md section 9.9).

    python paper/figures/charts/fig_cells_interaction.py --uslup 7

Single column, three stacked cards on a shared categorical x (R32 bridge, scratch, ImageNet):
panel similarity sigma, direction rho with the registered +-delta equivalence band (log scale,
as registered), vulnerability omega = log w (w in %). Lines join the cell means of ViT-Tiny and of
ResNet-18 (224 px); open marks are single runs; the three 32-pixel ResNet-18 runs (R32 bridge)
stand left of scratch in sigma and rho; R32 is absent from omega because its per-run omega is not
in the reference sheet. The card title's colour carries the term family (sigma green, rho orange,
omega neutral), always together with the term's name (naming step 4, colour code).

Data rule: copied verbatim from paper/figures/konsey/fig_cells_interaction.py main() (left
untouched; constants imported): runs per cell, cell means, H1/H2 contrasts, the R32 identities,
reference sheet lines 1496-1499, 1505-1513, 1526-1527, 1532, 1561-1562, 1588, 1593, 1595, 1745.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
import fig_cells_interaction as CI  # noqa: E402  (constants only)

ARGS = O.argumanlar(__doc__)
STEM = "cells_interaction"
SCRIPT = "paper/figures/charts/fig_cells_interaction.py"
J4P, J2P, HTP, CELLS, FOY_CELL, FOY_RUN, mean = CI.J4P, CI.J2P, CI.HTP, CI.CELLS, CI.FOY_CELL, CI.FOY_RUN, CI.mean


def veri():
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

    okunan = {J4P: ["b4.model_tablosu.<m>.yari_log.{sigma, rho, omega}", "b4.hucreler.<cell>",
                    "b4.F_B4.karsitliklar.H1.kestirim", "b4.F_B4.karsitliklar.H2.{kestirim, hucre_ort}",
                    "b4.F_B4.karsitliklar.H3.hucre_ort", "meta.delta"],
              J2P: ["b2.F_B2.K-a.{ciftler, simetrik_pay, yonlu_pay}", "b2.F_B2.K-b.degerler",
                    "b2.F_B2.K-c.sigma_V (R32 identity checks only)"],
              HTP: ["modeller.<m>.hucre"]}
    return dict(runs=runs, r32=r32, val=val, cm=cm, A=A, I=I, delta=delta, q=q), foy_sonuc, okunan


def main():
    D, foy, okunan = veri()
    runs, r32, val, cm, A, I, delta, q = (D[k] for k in ("runs", "r32", "val", "cm", "A", "I", "delta", "q"))
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    E = {a: O.ent(a) for a in ("vit", "r224", "r32", "sym", "dir")}
    band = U.tones()["vurgu_kutusu"][0]
    W = O.W("single")
    H = 121.0
    M, GY, KEY_H = 0.5, 1.6, 13.0
    ch = (H - 2 * M - KEY_H - 3 * GY) / 3
    L, R, T, B = 14.5, 2.0, cards.BAND + 1.0, 7.0
    X = {"scr": 0.0, "IN": 1.0}
    XR32 = -0.42
    OFF = {"vit": -0.07, "r224": 0.07}
    ms, ms_run, mew = vg["ortalama_markersize_pt"], vg["tohum_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    cv = cards.Canvas("single", H, naming_step=4, naming_kind="renk")
    titles = {"sigma": ("Panel similarity σ", E["sym"].hex, "σ"),
              "rho": ("Direction ρ", E["dir"].hex, "ρ"),
              "omega": ("Vulnerability ω = log w, w in %", U.ink, "ω")}
    cizilen = {"hucre_ortalamalari": {}, "kosular": {}, "r32_kopru": {}}
    kartlar = []
    for r, k in enumerate(q):
        nrun = sum(len(runs[c]) for c in CELLS) + (len(r32) if k != "omega" else 0)
        c = cv.card(None, titles[k][0], M, M + r * (ch + GY), W - 2 * M, ch, tint="kap", note=f"n = {nrun} runs")
        c.artists["title"].set_color(titles[k][1])
        ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
        O.eksen(ax, base="x", grid="y")
        if k == "rho":
            ax.axhspan(-delta, delta, color=band, lw=0, zorder=0.5)
            ax.axhline(0.0, color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
        for arch in ("vit", "r224"):
            e = E[arch]
            cells = [cc for cc in CELLS if CELLS[cc][0] == arch]
            xs = [X[CELLS[cc][1]] + OFF[arch] for cc in cells]
            ys = [cm[cc][k] for cc in cells]
            ax.plot(xs, ys, color=e.hex, ls=e.ls, lw=ST.weights.line, marker=e.marker, ms=ms, mfc=e.hex,
                    mec=U.ink, mew=mew, zorder=4)
            for cc in cells:
                rs = runs[cc]
                for i, m in enumerate(rs):
                    xx = X[CELLS[cc][1]] + OFF[arch] * 2.6 + (i - (len(rs) - 1) / 2) * 0.045
                    ax.plot([xx], [val[m][k]], ls="none", marker=e.marker, ms=ms_run, mfc="white", mec=e.hex,
                            mew=ST.weights.emph, zorder=5)
                    cizilen["kosular"].setdefault(m, {})[k] = val[m][k]
                cizilen["hucre_ortalamalari"].setdefault(cc, {})[k] = cm[cc][k]
        ticks, labs = [X["scr"], X["IN"]], ["scratch", "ImageNet"]
        if k != "omega":
            for i, m in enumerate(r32):
                ax.plot([XR32 + (i - 1) * 0.045], [val[m][k]], ls="none", marker=E["r32"].marker, ms=ms_run,
                        mfc="white", mec=E["r32"].hex, mew=ST.weights.emph, zorder=5)
                cizilen["r32_kopru"].setdefault(m, {})[k] = val[m][k]
            ticks, labs = [XR32] + ticks, ["R32"] + labs
        ax.set_xlim(-0.62, 1.38)
        ax.set_xticks(ticks)
        ax.set_xticklabels(labs)
        ax.set_ylabel(titles[k][2], labelpad=1)
        ax.locator_params(axis="y", nbins=6)
        O.tick_fmt(ax, "y", fmt={"sigma": "{:.1f}", "rho": "{:.2f}", "omega": "{:.2f}"}[k])
        if k == "sigma":
            ax.text(0.98, 0.05, f"A(σ, scr) = {O.minus(f'{A:+.3f}')}\nI(σ) = {O.minus(f'{I:+.3f}')}",
                    transform=ax.transAxes, ha="right", va="bottom", fontsize=ST.type_scale.annot, color=U.ink,
                    linespacing=1.4)
        kartlar.append(c)
    cv.title_strip(kartlar)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white", n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c)
    h = [Line2D([], [], color=E["vit"].hex, ls=E["vit"].ls, lw=ST.weights.line, marker=E["vit"].marker, ms=ms,
                mfc=E["vit"].hex, mec=U.ink, mew=mew, label="ViT-Tiny, cell mean"),
         Line2D([], [], ls="none", marker="o", ms=ms_run, mfc="white", mec=U.muted, mew=ST.weights.emph,
                label="open: single run"),
         Line2D([], [], color=E["r224"].hex, ls=E["r224"].ls, lw=ST.weights.line, marker=E["r224"].marker, ms=ms,
                mfc=E["r224"].hex, mec=U.ink, mew=mew, label="ResNet-18 (224), cell mean"),
         Patch(facecolor=band, edgecolor="none", label=f"±{delta:.2f} band (ρ)"),
         Line2D([], [], ls="none", marker=E["r32"].marker, ms=ms_run, mfc="white", mec=E["r32"].hex,
                mew=ST.weights.emph, label="R32 bridge run")]
    h = [h[0], h[2], h[4], h[1], h[3]]          # column-major: models left, conventions right
    kax.legend(handles=h, loc="center", ncol=2, frameon=False, handlelength=1.8, handletextpad=0.4,
               columnspacing=1.0, labelspacing=0.3, borderaxespad=0.0)
    cizilen["ek_aciklama"] = {"A_sigma_scr (H1)": A, "I_sigma (H2)": I, "delta_bandi": delta}

    deg = []
    for m, n in FOY_RUN.items():
        for k in q:
            deg.append(O.deger(f"run {m} {k}", val[m][k], J4P, f"b4.model_tablosu.{m}.yari_log.{k}",
                               "read as stored; == foy (3 dp)", n))
    for cc, n in FOY_CELL.items():
        for k in q:
            deg.append(O.deger(f"cell {cc} mean {k}", cm[cc][k], J4P, "; ".join(f"b4.model_tablosu.{m}.yari_log.{k}" for m in runs[cc]),
                               "mean of the cell's runs; == foy (3 dp), == H2/H3 hucre_ort (1e-12)", n))
    for m in r32:
        for k in ("sigma", "rho"):
            deg.append(O.deger(f"R32 run {m} {k}", val[m][k], J4P, f"b4.model_tablosu.{m}.yari_log.{k}",
                               "read as stored; B2 identities with foy 1588/1593/1595 parts (1e-9); "
                               "s1001 == foy 1745", 1745 if m == "ResNet18_AT_s1001" else None))
    deg.append(O.deger("A sigma scr (H1)", A, J4P, "b4.F_B4.karsitliklar.H1.kestirim", "read as stored; == foy", 1526))
    deg.append(O.deger("I sigma (H2)", I, J4P, "b4.F_B4.karsitliklar.H2.kestirim", "read as stored; == foy", 1527))
    deg.append(O.deger("delta band", delta, J4P, "meta.delta", "read as stored; == foy 1532 text", 1532))
    O.kaydet(cv, STEM, message=("ViT-Tiny's panel similarity rises with ImageNet initialization while ResNet-18's "
                                "stays flat; rho and omega move far less."),
             inputs=[J4P, J2P, HTP], degerler=deg, foy=foy, okunan=okunan, cizilen=cizilen,
             notlar=["R32 is omitted from the omega card: its per-run omega is not in the reference sheet.",
                     "x positions are categorical with fixed offsets; no jitter, no randomness."],
             kararlar=["Karar (duzeltme turu 2): A^sigma_scr and I^sigma are written 'A(sigma, scr)' and "
                       "'I(sigma)' (function notation, Greek sigma), because mathtext super- and subscripts print "
                       "at 70 % and fall under the 8 pt floor (trap 6), and a bare 'A' would read as the A^rho of "
                       "estimates_forest; the caption maps A(sigma, scr) = A^sigma_scr, I(sigma) = I^sigma.",
                       "Karar: the +-delta band uses the style's vurgu_kutusu tone (deep orange, 15 % light), because "
                       "the style's grey band tone equals the grey plot area, and the band belongs to rho (orange).",
                       "Karar: R32 gets a tick label of its own, so the bridge runs are named on the axis."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tasarim_izgarasi")
    O.ajan(STEM, iddia="each card: one term over the two-by-two cells",
           dogrudan_etiket="titles name the term; x labels name the cells")
    return 0


if __name__ == "__main__":
    sys.exit(main())
