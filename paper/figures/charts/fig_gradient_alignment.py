#!/usr/bin/env python
"""Input-gradient cosine against symmetric similarity on three data sets, raw and with the additive
model main effects removed; card figure, visio-cizici style 7 (plan 04_cizim_plani.md sections 6
and 9.11).

    python paper/figures/charts/fig_gradient_alignment.py --uslup 7

Two by three cards (template ortak_satirli_katlar, 2 x 3 adaptation): a narrow row strip at the
left names the rows (raw; residual), the top row's card titles name the data sets (CIFAR-10,
CIFAR-100, ImageNetV2) with the pair count, each column about 53.6 mm wide; every card prints its
own Spearman r. The earlier "Rank correlation" summary card is removed (plan section 6, M5): its
six values stand in the panels. A key strip at the bottom names the three pair types:
CNN-CNN (black circle), transformer-transformer (yellow triangle, black edge), mixed (grey
square); paper palette family cift_turu.

Data rule: the same as paper/figures/konsey/fig_gradient_alignment.py (left untouched; its SETS,
ana_etki_artik and spearman are imported): c_ij and log tau_ij from the three B10 Mantel files,
pair types from the frozen cell tables, the additive main-effect residual, raw and residual
Spearman recomputed and required to equal the JSON (1e-9) and the reference sheet (1e-3, lines
1970-1975), K and pair counts, pair counts and mean c per type against lines 2009-2011, and the
p-floor text line 1977. A mismatch writes nothing.
Naming: step 4 (letterless title strip), naming_kind serit.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
np = O.np
import fig_gradient_alignment as GA  # noqa: E402  (data rules only; its main() is not run)

ARGS = O.argumanlar(__doc__)
STEM = "gradient_alignment"
SCRIPT = "paper/figures/charts/fig_gradient_alignment.py"
TYPES = [("CNN-CNN", "cift_cnn", "CNN–CNN"), ("T-T", "cift_vit", "transformer–transformer"),
         ("mixed", "mixed", "mixed")]


def veri():
    """The data and checks of fig_gradient_alignment.main(), without drawing or writing."""
    foy = K.Foy()
    data, okunan, inputs = {}, {}, []
    for key, mp, hp, title, (lh, lr), lc in GA.SETS:
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
        foy.esit(f"{key}: max |T - T^T|", float(np.abs(T - T.T).max()), 0.0, 0.0,
                 "log tau matrix symmetric, so the axis is the symmetric log tau-bar")
        i, j = np.triu_indices(n, 1)
        c, t = C[i, j], T[i, j]
        cr, tr = GA.ana_etki_artik(C), GA.ana_etki_artik(T)
        rs_h, rs_r = GA.spearman(c, t), GA.spearman(cr, tr)
        S = K.dig(Mj, "sinamalar")
        foy.esit(f"{key}: recomputed raw Spearman == JSON", rs_h, S["ham"]["istatistik"], 1e-9, "raw Mantel statistic")
        foy.esit(f"{key}: recomputed residual Spearman == JSON", rs_r, S["ana_etki_artik"]["istatistik"], 1e-9,
                 "main-effect residual Mantel statistic")
        foy.kontrol(f"{key}: raw r_S (1e-3)", rs_h, lh, f"| {key} | ham |", 3, tol=1e-3)
        foy.kontrol(f"{key}: residual r_S (1e-3)", rs_r, lr, f"| {key} | ana_etki_artik |", 3, tol=1e-3)
        foy.kontrol(f"{key}: K", n, lh, f"| {key} | ham |", 0)
        foy.kontrol(f"{key}: pairs", len(c), lh, f"| {key} | ham |", 0)
        foy.esit(f"{key}: pairs == JSON cift_sayisi", len(c), S["ham"]["cift_sayisi"], 0, "pair count")
        fam = [("CNN" if HT[m]["aile"] == "CNN" else "T") for m in mods]
        typ = np.array(["CNN-CNN" if fam[a] == fam[b] == "CNN" else ("T-T" if fam[a] == fam[b] == "T" else "mixed")
                        for a, b in zip(i, j)])
        tsum = {}
        for tk, _, _ in TYPES:
            sel = typ == tk
            foy.kontrol(f"{key}: mean c {tk}", float(c[sel].mean()), lc, f"| {key} |", 3)
            foy.kontrol(f"{key}: n {tk}", int(sel.sum()), lc, f"| {key} |", 0)
            tsum[tk] = {"n": int(sel.sum()), "mean_c": float(c[sel].mean())}
        foy.kontrol(f"{key}: mean c all", float(c.mean()), lc, f"| {key} |", 3)
        data[key] = {"title": title, "c": c, "t": t, "cr": cr, "tr": tr, "typ": typ, "n": n, "pairs": len(c),
                     "rs_h": S["ham"]["istatistik"], "rs_r": S["ana_etki_artik"]["istatistik"], "tur": tsum,
                     "kaynak": mp, "foy": (lh, lr, lc)}
    foy.metin("p at floor in 6/6", "Tek yonlu p'si p tabanina esit olan sinama: 6/6", 1977, "p tabanina esit")
    return data, foy.bitir(), okunan, inputs


def main():
    DATA, foy, okunan, inputs = veri()
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    PE = {e: O.ent(e) for _, e, _ in TYPES}
    W = O.W("double")
    H = 110.0
    M, GX, GY, STRIP, KEY_H = 0.5, 3.0, 1.6, 8.0, 6.0
    x0 = M + STRIP + 1.6
    cw = (W - M - x0 - 2 * GX) / 3
    ch = (H - 2 * M - KEY_H - 2 * GY) / 2
    L, R, T, B = 14.0, 2.5, cards.BAND + 4.5, 9.0
    s_pt2 = vg["tohum_markersize_pt"] ** 2

    def edge(e):
        return O.kenar(e.key)

    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    strip = cv.card(None, "", M, M, STRIP, 2 * ch + GY, tint="white", n_exempt="row names of the grid")
    rows, drawn = [], {}
    for r, raw in enumerate((True, False)):
        row = []
        for k, (key, d) in enumerate(DATA.items()):
            title = d["title"] if raw else f"{d['title']}, residual"
            c = cv.card(None, title, x0 + k * (cw + GX), M + r * (ch + GY), cw, ch, tint="kap",
                        note=f"n = {d['pairs']}")
            ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
            O.eksen(ax, base="x", grid="both")
            xs, ys = (d["c"], d["t"]) if raw else (d["cr"], d["tr"])
            for tk, ek, _ in TYPES:
                e = PE[ek]
                ec, ew = edge(e)
                sel = d["typ"] == tk
                op = tk == "mixed"      # open grey square (see kararlar: shadow detector and overlap)
                ax.scatter(xs[sel], ys[sel], s=s_pt2, marker=e.marker, facecolor="white" if op else e.hex,
                           edgecolor=e.hex if op else ec, linewidth=ST.weights.emph if op else ew,
                           zorder={"T-T": 2, "mixed": 3, "CNN-CNN": 4}[tk])
            if not raw:
                ax.axhline(0, color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
            ax.locator_params(axis="both", nbins=4)
            O.tick_fmt(ax)
            rs = d["rs_h"] if raw else d["rs_r"]
            ax.text(0.0, 1.0 + 1.0 / (ch - T - B), f"r = {O.minus(f'{rs:+.3f}')}", transform=ax.transAxes, ha="left",
                    va="bottom", fontsize=ST.type_scale.annot, color=U.ink)
            ax.set_xlabel("cosine c" if raw else "c residual", labelpad=1)
            if k == 0:
                # tau with a combining macron (U+0304), the symmetric similarity of the text and of
                # similarity_matrix's key (plan section 2, O5; DejaVu Sans carries the mark)
                ax.set_ylabel("log τ̄" if raw else "log τ̄ residual", labelpad=1)
            drawn[f"{key}_{'ham' if raw else 'artik'}"] = {
                "r_S": rs, "nokta": int(len(xs)), "x_aralik": [float(xs.min()), float(xs.max())],
                "y_aralik": [float(ys.min()), float(ys.max())]}
            row.append(c)
        rows.append(row)
    cv.title_strip(rows[0])
    cv.title_strip(rows[1])
    for r, lab in enumerate(("raw", "residual")):
        strip.text(STRIP / 2, M + r * (ch + GY) + ch / 2 - M, lab, rotation=90, ha="center", va="center",
                   fontsize=ST.type_scale.label, color=U.ink)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white", n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c, inset=0.9)
    hs = []
    for tk, ek, lab in TYPES:
        e = PE[ek]
        ec, ew = edge(e)
        op = tk == "mixed"
        hs.append(Line2D([], [], ls="none", marker=e.marker, ms=vg["ortalama_markersize_pt"],
                         mfc="white" if op else e.hex, mec=e.hex if op else ec,
                         mew=ST.weights.emph if op else ew, label=f"{lab} pair"))
    kax.legend(handles=hs, loc="center", ncol=3, frameon=False, handletextpad=0.3, columnspacing=2.0,
               borderaxespad=0.0)

    deg = []
    for key, d in DATA.items():
        lh, lr, lc = d["foy"]
        deg.append(O.deger(f"{key} raw Spearman", d["rs_h"], d["kaynak"], "sinamalar.ham.istatistik",
                           "recomputed == JSON (1e-9) == foy (1e-3)", lh))
        deg.append(O.deger(f"{key} residual Spearman", d["rs_r"], d["kaynak"], "sinamalar.ana_etki_artik.istatistik",
                           "recomputed == JSON (1e-9) == foy (1e-3)", lr))
        deg.append(O.deger(f"{key} pairs", d["pairs"], d["kaynak"], "sinamalar.ham.cift_sayisi",
                           "upper triangle of c_matrisi; == foy", lh))
        deg.append(O.deger(f"{key} scatter points c", [float(v) for v in d["c"]], d["kaynak"],
                           "c_matrisi upper triangle (row-major)", "read as stored"))
        deg.append(O.deger(f"{key} scatter points log tau", [float(v) for v in d["t"]], d["kaynak"],
                           "log_tau_matrisi upper triangle (row-major)", "read as stored"))
        for tk, v in d["tur"].items():
            deg.append(O.deger(f"{key} {tk} n", v["n"], d["kaynak"],
                               "c_matrisi upper triangle; pair type from hucre_tablosu.json modeller.{model}.aile "
                               "for every model of modeller_ortak",
                               "count of pairs of this type; == foy", lc))
            deg.append(O.deger(f"{key} {tk} mean c (not drawn as a number)", v["mean_c"], d["kaynak"],
                               "c_matrisi upper triangle; pair type from hucre_tablosu.json modeller.{model}.aile "
                               "for every model of modeller_ortak", "mean of c over the type; == foy", lc))
    O.kaydet(cv, STEM, message=("Input-gradient cosine tracks pairwise symmetric similarity on all three data sets, raw "
                                "and with additive model main effects removed."),
             inputs=inputs, degerler=deg, foy=foy, okunan=okunan, cizilen=drawn,
             notlar=["Residual axes are the additive main-effect residuals of experiments/q1_ek_gradyan_kosinus.py "
                     "(ek on kayit 6.2), recomputed here with GA.ana_etki_artik.",
                     "Spearman r and the pair count n are printed in every card; the p floor (6/6 at the floor, foy "
                     "1977) is not printed."],
             kararlar=["Karar: the Rank correlation summary card is removed (plan section 6, M5), because its six "
                       "values are printed in the panels; the scatter columns grow to about 53.6 mm.",
                       "Karar: pair types use the paper palette family cift_turu (black, yellow with black edge, grey), "
                       "because #0072B2 and #D55E00 encode R224 and ViT-Tiny elsewhere (plan 4.3, m9).",
                       "Karar: mixed pairs are drawn as open grey squares and layered yellow, grey, black from the "
                       "back, because denge.py's shadow test read a filled grey square under an overlapping black or "
                       "yellow mark as a drop shadow (a data overlap, not a shadow); an open mark is a white copy, which "
                       "the test does not count, and the hue still binds the palette's mixed entry.",
                       "Karar (duzeltme turu 2): the y labels read 'log τ̄' and 'log τ̄ residual', because the "
                       "plotted matrix is the symmetric log_tau_matrisi (max |T - T^T| = 0), which the text and "
                       "the council figure write as log τ̄_ij.",
                       "Karar: the row strip is a narrow white card with rotated row names, because every text must "
                       "stand inside a card (millimetre controller)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="ortak_satirli_katlar")
    O.ajan(STEM, iddia="each card: one data set and one row (raw or residual), one claim",
           dogrudan_etiket="r is printed in each card; rows and columns are named")
    return 0


if __name__ == "__main__":
    sys.exit(main())
