#!/usr/bin/env python
"""ViT-Tiny AT under its own PGD-10 attack, per layer: CLS attention entropy change, CLS attention
displacement and the clean-to-adversarial cosine of the residual block outputs; card figure,
visio-cizici style 7 (plan 04_cizim_plani.md section 9.17, with Y8: the block-output cosine
card that replaces Table 16).

    python paper/figures/charts/fig_feature_degradation.py --uslup 7

Single column, three stacked cards on a shared layer axis (1-12), naming step 4 (title strip):
top, the change of the head-averaged CLS attention entropy (adversarial minus clean, nat), the
three run values (open) and their mean with the run-level 90% interval of the TOST file, inside
the pre-registered +-0.05 nat equivalence margin (band); middle, the total-variation displacement
of the CLS attention map, runs and mean +- SD; bottom, the block-output cosine for the CLS token,
the patch-token mean and all tokens, mean +- SD over runs. A key strip at the bottom.

Data: results/c1_c4/pair{1,2,3}/c4_summary.json (vit.attention.{entropy_delta_mean,
displacement_mean}, vit.cos_block_{cls, token_mean, output}.block<k>.mean) and
results/c1_c4/c4_entropy_tost.json (entropi_TOST.{marj_nat, katmanlar[k].{degerler, GA90}}).
Every mean and SD is compared with results/C1_REFERANS_FOYU.md lines 292-303 and 334-345 (4 dp),
the TOST run values with the summaries (1e-12), the margin with line 1113. A mismatch writes nothing.
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
ARGS = O.argumanlar(__doc__)
STEM = "feature_degradation"
SCRIPT = "paper/figures/charts/fig_feature_degradation.py"
PAIRS = (1, 2, 3)
TOST = "results/c1_c4/c4_entropy_tost.json"
COS = [("cos_block_cls", "CLS token", "vit"), ("cos_block_token_mean", "patch-token mean", None),
       ("cos_block_output", "all tokens", None)]
NL = 12


def p_(p):
    return f"results/c1_c4/pair{p}/c4_summary.json"


def ms_(v):
    return statistics.mean(v), statistics.stdev(v)


def veri():
    foy = K.Foy()
    S = [K.load_json(p_(p)) for p in PAIRS]
    Tj = K.load_json(TOST)
    marj = K.dig(Tj, "entropi_TOST.marj_nat")
    foy.metin("TOST margin text", f"Marj +-{marj} nat", 1113, "esdeger katman sayisi")
    if abs(marj - 0.05) > 1e-12:
        K.fail(f"margin {marj} != the registered 0.05 nat (foy 1111, 1113)")
    TL = K.dig(Tj, "entropi_TOST.katmanlar")
    dlt = [[K.dig(s, "vit.attention.entropy_delta_mean")[k] for s in S] for k in range(NL)]
    tv = [[K.dig(s, "vit.attention.displacement_mean")[k] for s in S] for k in range(NL)]
    cos = {key: [[K.dig(s, f"vit.{key}.block{k}.mean") for s in S] for k in range(NL)] for key, _, _ in COS}
    out = {"dlt": [], "tv": [], "cos": {key: [] for key, _, _ in COS}, "ga90": [], "marj": marj}
    for k in range(NL):
        ln, anc = 334 + k, f"| {k + 1} | "
        m, sd = ms_(dlt[k])
        foy.kontrol(f"layer {k + 1} entropy change mean", m, ln, anc, 4)
        foy.kontrol(f"layer {k + 1} entropy change SD", sd, ln, anc, 4)
        t = TL[k]
        if t["katman"] != k:
            K.fail(f"TOST layer index {t['katman']} != {k}")
        for a, b in zip(t["degerler"], dlt[k]):
            foy.esit(f"layer {k + 1} TOST run value == summary", a, b, 1e-12, "same run values in both files")
        foy.esit(f"layer {k + 1} TOST mean == mean of runs", t["ortalama"], m, 1e-12, "mean of the three runs")
        if not (t["GA90"][0] <= m <= t["GA90"][1]):
            K.fail(f"layer {k + 1}: mean outside its 90% interval")
        out["dlt"].append({"runs": dlt[k], "mean": m, "sd": sd})
        out["ga90"].append(list(t["GA90"]))
        m, sd = ms_(tv[k])
        foy.kontrol(f"layer {k + 1} TV mean", m, ln, anc, 4)
        foy.kontrol(f"layer {k + 1} TV SD", sd, ln, anc, 4)
        out["tv"].append({"runs": tv[k], "mean": m, "sd": sd})
        lc, ac = 292 + k, f"| {k + 1} | "
        for key, lab, _ in COS:
            m, sd = ms_(cos[key][k])
            foy.kontrol(f"block {k + 1} {key} mean", m, lc, ac, 4)
            foy.kontrol(f"block {k + 1} {key} SD", sd, lc, ac, 4)
            out["cos"][key].append({"runs": cos[key][k], "mean": m, "sd": sd})
    return out, [p_(p) for p in PAIRS] + [TOST], foy.bitir()


def main():
    D, inputs, foy = veri()
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from matplotlib.ticker import MultipleLocator
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    V = O.ent("vit")
    band = U.tones()["vurgu_kutusu"][0]
    W = O.W("single")
    H = 121.0
    M, GY, KEY_H = 0.5, 1.6, 14.0
    ch = (H - 2 * M - KEY_H - 3 * GY) / 3
    L, R, T, B = 15.0, 3.0, cards.BAND + 1.0, 8.5
    ms, ms_r, mew = vg["ortalama_markersize_pt"], vg["tohum_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    xs = list(range(1, NL + 1))
    cv = cards.Canvas("single", H, naming_step=4, naming_kind="serit")
    specs = [("CLS attention entropy change (nat)", "Δ (nat)"),
             ("CLS attention displacement (TV)", "TV"),
             ("Block-output cosine under attack", "cosine")]
    kart = []
    cos_style = {"cos_block_cls": dict(color=V.hex, marker=V.marker, ls=V.ls, mfc=V.hex),
                 "cos_block_token_mean": dict(color=U.ink, marker="o", ls="--", mfc=U.ink),
                 "cos_block_output": dict(color=U.muted, marker="s", ls=":", mfc="white")}
    for r, (title, yl) in enumerate(specs):
        c = cv.card(None, title, M, M + r * (ch + GY), W - 2 * M, ch, tint="kap", note="n = 3 runs")
        ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
        O.eksen(ax, base="x", grid="y")
        if r in (0, 1):
            rows = D["dlt"] if r == 0 else D["tv"]
            for k, x in enumerate(xs):
                ax.plot([x + o for o in (-0.18, 0.0, 0.18)], rows[k]["runs"], ls="none", marker="o", ms=ms_r,
                        mfc="white", mec=V.hex, mew=ST.weights.emph, zorder=3)
            means = [row["mean"] for row in rows]
            if r == 0:
                ax.axhspan(-D["marj"], D["marj"], color=band, lw=0, zorder=0.5)
                ax.axhline(0.0, color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
                lo = [m - g[0] for m, g in zip(means, D["ga90"])]
                hi = [g[1] - m for m, g in zip(means, D["ga90"])]
                ax.set_ylim(-1.3 * D["marj"], 1.3 * D["marj"])
            else:
                lo = hi = [row["sd"] for row in rows]
                ax.set_ylim(0, None)
            if r == 0:
                O.hata(ax, V.key, xs, means, kind="ci90", yerr=[lo, hi], ecolor=V.hex, zorder=4,
                       tanim="top card: run-level 90% interval of the TOST file (entropi_TOST.katmanlar[k].GA90), "
                             "the interval the equivalence decision reads against the +-0.05 nat margin; ci90 is "
                             "outside annotate.ERRORBAR_KINDS, recorded so the caption check runs")
            else:
                O.hata(ax, V.key, xs, means, kind="sd", yerr=[lo, hi], ecolor=V.hex, zorder=4,
                       tanim="middle and bottom cards: +-1 SD (ddof = 1) over the three runs")
            ax.plot(xs, means, color=V.hex, ls=V.ls, lw=ST.weights.line, marker=V.marker, ms=ms, mfc=V.hex,
                    mec=U.ink, mew=mew, zorder=5)
        else:
            for key, lab, _ in COS:
                st = cos_style[key]
                rows = D["cos"][key]
                O.hata(ax, V.key, xs, [q["mean"] for q in rows], kind="sd", yerr=[q["sd"] for q in rows],
                       ecolor=st["color"], zorder=3,
                       tanim="middle and bottom cards: +-1 SD (ddof = 1) over the three runs")
                ax.plot(xs, [q["mean"] for q in rows], color=st["color"], ls=st["ls"], lw=ST.weights.line,
                        marker=st["marker"], ms=ms, mfc=st["mfc"], mec=U.ink if st["mfc"] != "white" else st["color"],
                        mew=mew if st["mfc"] != "white" else ST.weights.emph, zorder=4)
        ax.set_xlim(0.4, NL + 0.6)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.set_xlabel("layer" if r < 2 else "block", labelpad=1)
        ax.set_ylabel(yl, labelpad=1)
        ax.locator_params(axis="y", nbins=4)
        O.tick_fmt(ax, "y")
        kart.append(c)
    cv.title_strip(kart)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white", n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c, inset=0.9)
    hs = [Line2D([], [], ls="none", marker="o", ms=ms_r, mfc="white", mec=V.hex, mew=ST.weights.emph,
                 label="single run"),
          Patch(facecolor=band, edgecolor="none", label=f"±{D['marj']:.2f} nat margin"),
          Line2D([], [], color=V.hex, ls=V.ls, lw=ST.weights.line, marker=V.marker, ms=ms, mfc=V.hex, mec=U.ink,
                 mew=mew, label="CLS token")]
    for key, lab, _ in COS[1:]:
        st = cos_style[key]
        hs.append(Line2D([], [], color=st["color"], ls=st["ls"], lw=ST.weights.line, marker=st["marker"], ms=ms,
                         mfc=st["mfc"], mec=U.ink if st["mfc"] != "white" else st["color"],
                         mew=mew if st["mfc"] != "white" else ST.weights.emph, label=lab))
    kax.legend(handles=hs, loc="upper center", ncol=3, frameon=False, handletextpad=0.3, columnspacing=0.6,
               labelspacing=0.25, handlelength=1.3, borderaxespad=0.0)
    # what the bars are (duzeltme turu 2): the top card's interval differs from the two others
    kax.text(0.5, 0.0, "bars: 90% interval (top), \u00b1SD (middle, bottom)", transform=kax.transAxes,
             ha="center", va="bottom", fontsize=ST.type_scale.annot, color=U.ink)
    deg = []
    for k in range(NL):
        for lab, rows, path_key in (("entropy change", D["dlt"], "vit.attention.entropy_delta_mean"),
                                    ("TV displacement", D["tv"], "vit.attention.displacement_mean")):
            for i, p in enumerate(PAIRS):
                deg.append(O.deger(f"layer {k + 1} {lab} run {p}", rows[k]["runs"][i], p_(p), f"{path_key}[{k}]",
                                   "read as stored"))
            deg.append(O.deger(f"layer {k + 1} {lab} mean", rows[k]["mean"], p_(1), f"{path_key}[{k}] (pairs 1-3)",
                               "mean of the three runs; == foy (4 dp)", 334 + k))
            deg.append(O.deger(f"layer {k + 1} {lab} SD", rows[k]["sd"], p_(1), f"{path_key}[{k}] (pairs 1-3)",
                               "SD ddof=1 of the three runs; == foy (4 dp)", 334 + k))
        deg.append(O.deger(f"layer {k + 1} entropy change 90% interval", D["ga90"][k], TOST,
                           f"entropi_TOST.katmanlar[{k}].GA90", "read as stored; contains the mean"))
        for key, lab, _ in COS:
            q = D["cos"][key][k]
            deg.append(O.deger(f"block {k + 1} {lab} cosine mean", q["mean"], p_(1), f"vit.{key}.block{k}.mean (pairs 1-3)",
                               "mean of the three runs; == foy (4 dp)", 292 + k))
            deg.append(O.deger(f"block {k + 1} {lab} cosine SD", q["sd"], p_(1), f"vit.{key}.block{k}.mean (pairs 1-3)",
                               "SD ddof=1; == foy (4 dp)", 292 + k))
    deg.append(O.deger("equivalence margin", D["marj"], TOST, "entropi_TOST.marj_nat", "read as stored; == foy 1113",
                       1113))
    O.kaydet(cv, STEM, message=("Under attack the ViT's CLS attention moves (displacement grows with depth) without "
                                "broadening, and block outputs drift gradually."),
             inputs=inputs, degerler=deg, foy=foy,
             okunan={p_(1) + " (and pair2, pair3)": ["vit.attention.{entropy_delta_mean, displacement_mean}",
                                                     "vit.cos_block_{cls, token_mean, output}.block<k>.mean"],
                     TOST: ["entropi_TOST.{marj_nat, katmanlar[k].{katman, degerler, ortalama, GA90}}"]},
             cizilen={"entropi_degisimi": D["dlt"], "ga90": D["ga90"], "tv": D["tv"], "kosinus": D["cos"],
                      "marj": D["marj"]},
             notlar=["Layer and block numbers are 1-based (the sheet's numbering); the files store 0-based keys.",
                     "The ResNet-18 layer cosines of Table 16 are not drawn (a different layer axis); they stay in "
                     "the reference sheet and the appendix text.",
                     "TOST p values are not drawn."],
             kararlar=["Karar (duzeltme turu 2): the key carries 'bars: 90% interval (top), +-SD (middle, "
                       "bottom)' and the bars are drawn through annotate.errorbar (sd) or with the kind recorded "
                       "(ci90), so the manifest's errorbar_kinds is [ci90, sd] and fig_qc D3 checks the caption; "
                       "the key strip grows by 3 mm (height 121 mm, ceiling 122).",
                       "Karar: the entropy-change interval is the run-level 90% interval of the TOST file, because "
                       "the equivalence decision reads that interval against the +-0.05 nat margin; the council "
                       "figure drew 95% t intervals, so the caption must say 90%.",
                       "Karar: the run values are drawn beside every mean, so no card is a single-series panel.",
                       "Karar: the block-output cosine card (Y8) draws the ViT's three token aggregations only; the "
                       "CLS series keeps the ViT hue, the two others are ink and grey with their own shapes."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tasarim_izgarasi")
    O.ajan(STEM, iddia="entropy unchanged, attention displaced, features drift: one claim per card",
           dogrudan_etiket="titles name each measure; the key names the series")
    return 0


if __name__ == "__main__":
    sys.exit(main())
