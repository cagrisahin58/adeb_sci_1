#!/usr/bin/env python
"""Source gap of the transformer relative to its CNN counterpart, split into a symmetric and a
directional part; card figure, visio-cizici style 7 (plan 04_cizim_plani.md section 9.7).

    python paper/figures/charts/fig_source_gap_split.py --uslup 7

Three cards on shared rows (CIFAR-10 and CIFAR-100 seed pairs, ImageNetV2 same-recipe model
pairs, descriptive), one shared x scale in log units. Each row is a point-range: a thin rule
from zero to the symmetric part sigma(CNN) - sigma(T) (green mark), the directional part
-(rho(CNN) - rho(T))/2 as the orange segment from there to the total gap G (ink diamond); a
negative directional part runs leftwards. q = symmetric / G stands in a value column at the right
edge of each card; for the ImageNetV2 pair whose G is at or below the registered denominator
threshold (meta.delta, dashed line) q is not printed ("n/a"). Open marks: descriptive pairs.

Data rule: the same as paper/figures/konsey/fig_source_gap_split.py (left untouched): three
frozen B2 outputs, the identities G == sym + dir and q == sym / G (1e-12), and the reference
sheet lines 1587, 1593, 1838, 1848, 1930-1932, 1926 and 1945. A mismatch writes nothing.
Naming: step 4, letterless title strip (plan section 8); a key strip at the bottom.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
ARGS = O.argumanlar(__doc__)
STEM = "source_gap_split"
SCRIPT = "paper/figures/charts/fig_source_gap_split.py"
J2P = "results/q1/konsey_ayrisim_b2.json"
J9P = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
J8P = "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json"
SETS = [("c10", J2P, "CIFAR-10", "seed pair"), ("c100", J9P, "CIFAR-100", "seed pair"),
        ("in", J8P, "ImageNetV2, descriptive", "model pair")]
FOY_IN_PAIR = {0: 1930, 1: 1931, 2: 1932}
FOY_LINES = {"c10": (1587, "| K-a, simetrik oran", 1593, "K-a ayrintisi"),
             "c100": (1838, "| K-a, simetrik oran", 1848, "K-a ayrintisi")}


def veri():
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
                     "q": Ka["q"], "payda_kucuk": list(Ka["payda_kucuk_tohumlar"]), "delta": K.dig(J, "meta.delta"),
                     "path": path}
    lines = {}
    for key, (ql, qa, dl, da) in FOY_LINES.items():
        d = data[key]
        for i in range(3):
            foy.kontrol(f"{key}.q[{i}]", d["q"][i], ql, qa, 3)
            foy.kontrol(f"{key}.D[{i}]", d["D"][i], dl, da, 3)
            foy.kontrol(f"{key}.sym[{i}]", d["sym"][i], dl, da, 3)
            foy.kontrol(f"{key}.dir[{i}]", d["dir"][i], dl, da, 3)
            lines[(key, i)] = {"q": ql, "D": dl, "sym": dl, "dir": dl}
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
        lines[("in", i)] = {"q": n, "D": n, "sym": n, "dir": n}
    foy.metin("in.payda kurali cift 3", "payda kurali tetiklenen cift: cift 3", 1945, "Dondurulmus betigin B8 ciktisi")
    foy.metin("in.payda esigi", "payda kurali D_k <= 0.1", 1926, "Cift duzeyi")
    for i in range(3):
        small = d["D"][i] <= d["delta"]
        if small != (i in d["payda_kucuk"]):
            K.fail(f"in pair {i}: D <= delta is {small} but payda_kucuk_tohumlar = {d['payda_kucuk']}")
    for key in data:
        for s_, D_ in zip(data[key]["sym"], data[key]["D"]):
            if s_ < 0 or D_ < 0:
                K.fail(f"{key}: negative symmetric part or gap; the point-range assumes both >= 0")
    return data, foy.bitir(), lines


def main():
    data, foy, lines = veri()
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from motor.figspec import cards, veri_dili

    ST, U = O.ST, O.U
    vg = O.vg()
    SYM, DIR = O.ent("sym"), O.ent("dir")
    W = O.W("double")
    H = 69.0
    M, GX, KEY_H = 0.5, 3.0, 10.0
    # negative directional part: open (white) with a dashed rho-hue edge; a matplotlib hatch is written
    # as 72 pt pattern tiles that the printed-PDF checker reads as closed boxes (box_spill FAIL)
    NEG = dict(facecolor="white", edgecolor=DIR.hex, linestyle=(0, (2, 1)), linewidth=ST.weights.emph)
    cw = (W - 2 * M - 2 * GX) / 3
    ch = H - 2 * M - KEY_H - 1.6
    L, R, T, B = 13.0, 11.0, cards.BAND + 2.0, 10.0
    xmax = max(v for k in data for v in data[k]["D"] + data[k]["sym"])
    xlim = (0.0, round(xmax + 0.06, 1))
    ms = vg["ortalama_markersize_pt"]
    mew = O.figspec.layout.marker_edge_pt(U)
    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    row, cizilen = [], {}
    for k, (key, path, title, ylab) in enumerate(SETS):
        d = data[key]
        desc = key == "in"
        c = cv.card(None, title, M + k * (cw + GX), M, cw, ch, tint="kap", note=f"n = {len(d['D'])}")
        ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
        O.eksen(ax, base="x", grid="x")
        n = len(d["D"])
        rows = []
        for i in range(n):
            y = n - 1 - i
            s_, r_, D_, q_ = d["sym"][i], d["dir"][i], d["D"][i], d["q"][i]
            if abs((s_ + r_) - D_) > 1e-12:
                K.fail(f"{key} pair {i + 1}: sym + dir != G")
            ax.plot([0.0, s_], [y, y], color=U.muted, lw=ST.weights.grid, zorder=2, solid_capstyle="butt")
            if r_ < 0:
                # duzeltme turu 2: a negative directional part narrows the gap (G left of the symmetric
                # mark); it is drawn open and hatched in the rho hue, with its own key entry
                ax.barh(y, r_, left=s_, height=0.3, zorder=3, **NEG)
            else:
                ax.barh(y, r_, left=s_, height=0.3, color=DIR.hex, edgecolor="none", zorder=3)
            ax.plot([s_], [y], ls="none", marker=SYM.marker, ms=ms, mfc="white" if desc else SYM.hex,
                    mec=SYM.hex if desc else U.ink, mew=ST.weights.emph if desc else mew,
                    zorder=4)
            ax.plot([D_], [y], ls="none", marker="D", ms=ms, mfc="white" if desc else U.ink, mec=U.ink,
                    mew=ST.weights.emph if desc else mew, zorder=5)
            na = desc and i in d["payda_kucuk"]
            ax.text(1.0 + 2.0 / (cw - L - R), y, "n/a" if na else f"{q_:.3f}", transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=ST.type_scale.annot, color=U.ink, clip_on=False)
            rows.append({"cift": list(d["ciftler"][i]), "G": D_, "simetrik_pay": s_, "yonlu_pay": r_, "q": q_,
                         "q_yazildi": not na, "satir_y": y})
        ax.text(1.0 + 2.0 / (cw - L - R), n - 0.45, "q", transform=ax.get_yaxis_transform(), ha="left",
                va="bottom", fontsize=ST.type_scale.annot, color=U.muted, clip_on=False, style="italic")
        if desc:
            ax.axvline(d["delta"], color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.6, n - 0.35)
        ax.set_yticks(range(n))
        ax.set_yticklabels([str(n - j) for j in range(n)])
        ax.set_ylabel(ylab, labelpad=1)
        ax.set_xlabel("source gap (log units)", labelpad=1)
        ax.locator_params(axis="x", nbins=5)
        O.tick_fmt(ax, "x")
        cizilen[key] = rows
        row.append(c)
    cv.title_strip(row)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white",
                    n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c)
    from matplotlib.patches import Patch
    h = [Line2D([], [], ls="none", marker=SYM.marker, ms=ms, mfc=SYM.hex, mec=U.ink, mew=mew, label="symmetric part"),
         Patch(facecolor=DIR.hex, edgecolor="none", label="directional part"),
         Patch(label="negative directional part (narrows the gap)", **NEG),
         Line2D([], [], ls="none", marker="D", ms=ms, mfc=U.ink, mec=U.ink, label="total gap G"),
         Line2D([], [], ls="none", marker=SYM.marker, ms=ms, mfc="white", mec=SYM.hex, mew=ST.weights.emph,
                label="open: descriptive"),
         Line2D([], [], color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), label="registered G threshold")]
    h = [h[0], h[3], h[1], h[4], h[2], h[5]]      # column-major in three columns: marks, parts, conventions
    kax.legend(handles=h, loc="center", ncol=3, frameon=False, handlelength=1.6, handletextpad=0.4,
               columnspacing=1.6, labelspacing=0.3, borderaxespad=0.0)
    cizilen["esik_G_imagenetv2"] = data["in"]["delta"]

    deg = []
    for key, path, _, _ in SETS:
        d = data[key]
        for i in range(len(d["D"])):
            fl = lines[(key, i)]
            for fld, nm in (("D", "G"), ("sym", "simetrik_pay"), ("dir", "yonlu_pay"), ("q", "q")):
                jk = {"D": "D", "sym": "simetrik_pay", "dir": "yonlu_pay", "q": "q"}[fld]
                deg.append(O.deger(f"{key} pair {i + 1} {nm}", d[fld][i], path, f"b2.F_B2.K-a.{jk}[{i}]",
                                   "read as stored; G == sym + dir, q == sym / G (1e-12)", fl[fld]))
    deg.append(O.deger("ImageNetV2 registered G threshold", data["in"]["delta"], J8P, "meta.delta",
                       "read as stored; == foy 1926 'payda kurali D_k <= 0.1'", 1926))
    okunan = {p: ["b2.F_B2.K-a.{ciftler, D, simetrik_pay, yonlu_pay, q, payda_kucuk_tohumlar}", "meta.delta"]
              for p in (J2P, J9P, J8P)}
    O.kaydet(cv, STEM, message=("The transformer's source gap is mostly symmetric on CIFAR-10 and CIFAR-100; "
                                "the ImageNetV2 pairs are descriptive."),
             inputs=[J2P, J9P, J8P], degerler=deg, foy=foy, okunan=okunan, cizilen=cizilen,
             notlar=["The JSON field D is the total gap G of the text (brief 12 section 3.1).",
                     "Pair 3 of ImageNetV2 has G at or below the registered 0.10 threshold; its q is not printed.",
                     "Row labels are pair indices: CIFAR seed pairs 1-3 are C1 pairs; ImageNetV2 pairs 1-3 are "
                     "Singh ConvNeXt-T/ViT-S, Singh ConvNeXt-B/ViT-B, Liu ConvNeXt-B/Swin-B (konsey kanit notes)."],
             kararlar=["Karar (duzeltme turu 2): a negative directional part (ImageNetV2 pair 1, yonlu_pay "
                       "-0.0445) is drawn as an open segment with a dashed rho-hue edge (a hatch prints as 72 pt pattern tiles that fig_mm_pdf reads as closed boxes) with the key entry 'negative "
                       "directional part (narrows the gap)', as in the council figure; the key takes two rows "
                       "(height 69 mm, ceiling 72). No '(>1)' mark is added to q = 1.364: the open segment "
                       "already says why q exceeds 1, and the q column (11 mm) has no room for it.",
                       "Karar: stacked bars became a point-range (plan 9.7), because the style-7 template "
                       "ortak_satirli_katlar draws point and interval marks; the orange segment's length is the "
                       "directional part, so a negative part (ImageNetV2 pair 1) reads as G left of the green mark.",
                       "Karar: one shared x scale over the three cards, because the cards share rows and the "
                       "original shared its y axis."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="ortak_satirli_katlar")
    O.ajan(STEM, iddia="each card: one data set's source gap split, one claim per card",
           dogrudan_etiket="q is printed beside each row; titles name the data set")
    return 0


if __name__ == "__main__":
    sys.exit(main())
