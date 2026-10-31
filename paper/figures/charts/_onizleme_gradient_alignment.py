#!/usr/bin/env python
"""Style preview of the gradient-alignment figure (fig:gradient_alignment) in one catalogue style, card engine.

    python paper/figures/charts/_onizleme_gradient_alignment.py --uslup 7

N is 7, H or 1 (the chosen data style and its two preview candidates,
raporlar/visio_2026-10-31/02_uslup_secimi.md). The data and every check are those of
paper/figures/konsey/fig_gradient_alignment.py (left untouched): c_ij and log tau_ij from
the three B10 Mantel files, pair types from the frozen cell tables, the additive
main-effect residual, the raw and residual Spearman statistics recomputed and required
to equal the JSON (1e-9) and the reference sheet (1e-3, lines 1970-1975), pair counts
and mean c per type against the sheet (lines 2009-2011). A mismatch stops the figure.

The composition follows the style's own ``ic_ice_izgara`` template
(styles/uslup_<N>/sablonlar.yaml):

* 7 (Salman 2020 Figure 2): a tall summary card on the left and a grid of small cards,
  grey plot area, white grid, no spines, in-axes rounded legend.
* H (HP Figure 18): a tall summary card, two cards each holding two sub-axes, one wide
  card at the bottom; tone cards, plot area in the card tone, direct key.
* 1 (Jiao 2021 Figure 2): a 2 x 3 grid under one column-head strip, white plot areas,
  L axes, an aligned count table under each top-row panel (the template's risk table).

Naming: step 4 (letterless title strip), decided before drawing
(raporlar/visio_2026-10-31/01_envanter.md section 7.2). Colours and markers of the pair
types are the paper's (paper/figures/visio/palettes/adeb_konsey_uslup_<N>.yaml: r224 CNN,
vit transformer, mixed).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "visio"))
import _vz_ortam  # noqa: E402

_vz_ortam.kur()
import numpy as np  # noqa: E402
from motor import figspec  # noqa: E402
from motor.figspec import cards  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402

sys.path.insert(0, "paper/figures/konsey")
import konsey_ortak as K  # noqa: E402
import fig_gradient_alignment as GA  # noqa: E402  (data rules only; its main() is not run)

AP = argparse.ArgumentParser(description=__doc__.splitlines()[0])
AP.add_argument("--uslup", required=True, choices=["7", "H", "1"])
ARGS, _ = AP.parse_known_args()
NO = ARGS.uslup
STEM = f"_onizleme_gradient_alignment_uslup_{NO}"
OUT = Path("paper/figures/charts")
VENUE = "ieee_access"
TYPES = [("CNN-CNN", "r224", "CNN–CNN"), ("T-T", "vit", "transformer–transformer"), ("mixed", "mixed", "mixed")]


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
        data[key] = {"title": title, "c": c, "t": t, "cr": cr, "tr": tr, "typ": typ, "n": n, "pairs": len(c),
                     "rs_h": S["ham"]["istatistik"], "rs_r": S["ana_etki_artik"]["istatistik"], "tur": tsum,
                     "kaynak": mp}
    foy.metin("p at floor in 6/6", "Tek yonlu p'si p tabanina esit olan sinama: 6/6", 1977, "p tabanina esit")
    return data, foy.bitir(), okunan, inputs


DATA, FOY, OKUNAN, INPUTS = veri()
ST = figspec.use(venue=VENUE, palette=f"paper/figures/visio/palettes/adeb_konsey_uslup_{NO}.yaml", uslup=NO)
U = ST.uslup
VG = (U.raw.get("bilesen_kurallari") or {}).get("veri_grafigi") or {}
PAL = ST.palette
INK, MUTED = U.ink, U.muted
W = ST.venue.width_in("double") * 25.4


def num(v):
    return f"{v:+.3f}".replace("-", "−")


def tick_fmt(ax):
    import matplotlib.pyplot as plt
    f = plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−"))
    ax.xaxis.set_major_formatter(f)
    ax.yaxis.set_major_formatter(f)


def style_axes(ax):
    """Axis, grid and plot area by the style's veri_grafigi tokens."""
    eksen = str(VG.get("eksen", "L"))
    alan = str(VG.get("cizim_alani", "beyaz"))
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    if eksen == "yok":
        for sp in ("left", "bottom"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(length=0)
    if alan.startswith("#"):
        ax.set_facecolor(alan)
    elif alan == "beyaz":
        ax.set_facecolor("#FFFFFF")
    iz = str(VG.get("izgara", "yok"))
    if iz in ("beyaz_gri_ustu", "beyaz_ton_ustu"):
        ax.grid(True, axis="both", color=str(VG.get("izgara_rengi", "#FFFFFF")), linewidth=ST.weights.grid, zorder=0)
    else:
        ax.grid(False)
    ax.set_axisbelow(True)
    ax.locator_params(axis="both", nbins=4)
    tick_fmt(ax)


def scatter(ax, d, raw=True, small=False, above=False):
    xs, ys = (d["c"], d["t"]) if raw else (d["cr"], d["tr"])
    sz = 6 if small else 9
    for tk, ent, _ in TYPES:
        e = PAL[ent]
        sel = d["typ"] == tk
        ax.scatter(xs[sel], ys[sel], s=sz, marker=e.marker, facecolor=e.hex, edgecolor=INK,
                   linewidth=figspec.layout.marker_edge_pt(U), zorder=3 if tk != "mixed" else 2)
    if not raw:
        ax.axhline(0, color=MUTED, lw=ST.weights.grid, ls=(0, (3, 2)), zorder=1)
    style_axes(ax)
    rs = d["rs_h"] if raw else d["rs_r"]
    if above:   # over the plot area, under the card title: never on a data point
        ax.text(0.0, 1.0, f"r = {num(rs)}", transform=ax.transAxes, ha="left", va="bottom",
                fontsize=ST.type_scale.annot, color=INK)
    else:
        ax.text(0.04, 0.96, f"r = {num(rs)}", transform=ax.transAxes, ha="left", va="top",
                fontsize=ST.type_scale.annot, color=INK)
    return {"r_S": rs, "nokta": int(len(xs)), "x_aralik": [float(xs.min()), float(xs.max())],
            "y_aralik": [float(ys.min()), float(ys.max())]}


def summary(ax):
    """Raw and residual Spearman statistic per data set: a dumbbell (two states of one measure)."""
    keys = list(DATA)
    for k_, key in enumerate(keys):
        d = DATA[key]
        y = len(keys) - 1 - k_
        ax.plot([d["rs_r"], d["rs_h"]], [y, y], color=INK, lw=0.5, zorder=2)
        ax.plot(d["rs_h"], y, ls="none", marker="o", ms=4.2, mfc=INK, mec=INK, zorder=3)
        ax.plot(d["rs_r"], y, ls="none", marker="D", ms=3.8, mfc="white", mec=INK, mew=0.8, zorder=3)
    style_axes(ax)
    from matplotlib.ticker import FixedFormatter, FixedLocator
    ax.yaxis.set_major_locator(FixedLocator(list(range(len(keys)))))
    ax.yaxis.set_major_formatter(FixedFormatter([DATA[k]["title"] for k in reversed(keys)]))
    ax.set_ylim(-0.6, len(keys) - 0.4)
    ax.locator_params(axis="x", nbins=3)
    ax.set_xlabel("Spearman r")
    ax.margins(x=0.18)          # room for the direct labels inside the spines
    # direct labels for the two states on the row where they stand furthest apart
    kk = max(keys, key=lambda k: abs(DATA[k]["rs_h"] - DATA[k]["rs_r"]))
    row = len(keys) - 1 - keys.index(kk)
    for v, lab in ((DATA[kk]["rs_h"], "raw"), (DATA[kk]["rs_r"], "residual")):
        ax.annotate(lab, (v, row), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                    fontsize=ST.type_scale.annot, color=INK)
    return {k: {"raw": DATA[k]["rs_h"], "residual": DATA[k]["rs_r"]} for k in keys}


def key_handles(small=False):
    from matplotlib.lines import Line2D
    return [Line2D([], [], ls="none", marker=PAL[e].marker, ms=4.0, mfc=PAL[e].hex, mec=INK, mew=0.3, label=lab)
            for _, e, lab in TYPES]


def tpl():
    from motor.figspec.uslup import load_sablonlar
    return load_sablonlar(NO, argv=[]).template("ic_ice_izgara")


# ------------------------------------------------------------------ layouts
M = 0.5          # canvas margin kept by every card (the controller asks 0.3)


def legend_below(ax, ax_left_mm, frame):
    """The pair-type key under an axes, inside its card (x anchored at the card inset)."""
    bb = ax.get_position()
    axw_mm = bb.width * W
    axh_mm = bb.height * ax.figure.get_size_inches()[1] * 25.4
    return ax.legend(handles=key_handles(), loc="upper left",
                     bbox_to_anchor=(-(ax_left_mm - 2.5) / axw_mm, -9.0 / axh_mm), frameon=frame, fancybox=frame,
                     handletextpad=0.3, borderpad=0.4 if frame else 0.0, labelspacing=0.3, edgecolor=MUTED,
                     borderaxespad=0.0)


def lay_7():
    t = tpl()
    sx = W / float(t["izgara_mm"]["genislik"])
    H = 96.0
    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    a = [p for p in t["paneller"] if p["ad"] == "a"][0]["konum"]
    aw = round(float(a["w"]) * sx, 2) - M
    x0 = M + aw + round(4.0 * sx, 2)
    gx = gy = 3.0
    cw = (W - M - x0 - 2 * gx) / 3
    ch = (H - 2 * M - gy) / 2
    A = cv.card(None, "Rank correlation", M, M, aw, H - 2 * M, tint="kap",
                n_exempt="one statistic per data set")
    axA = A.axes(left=21.0, right=3.0, top=cards.BAND + 2.0, bottom=30.0)
    drawn = {"ozet": summary(axA)}
    legend_below(axA, 21.0, frame=True)
    rows = []
    for r, raw in enumerate((True, False)):
        row = []
        for k, (key, d) in enumerate(DATA.items()):
            c = cv.card(None, d["title"] if raw else "residual", x0 + k * (cw + gx), M + r * (ch + gy), cw, ch,
                        tint="kap", note=f"n = {d['pairs']}")
            ax = c.axes(left=14.5 if k == 0 else 11.0, right=2.5, top=cards.BAND + 5.0, bottom=9.5)
            drawn[f"{key}_{'ham' if raw else 'artik'}"] = scatter(ax, d, raw, small=True, above=True)
            ax.set_xlabel("cosine c" if raw else "c residual", labelpad=1)
            if k == 0:
                ax.set_ylabel("log τ" if raw else "residual", labelpad=1)
            row.append(c)
        rows.append(row)
    cv.title_strip([A] + rows[0])
    cv.title_strip(rows[1])
    return cv, drawn


def lay_H():
    t = tpl()
    gap = 1.6        # the style's card gap (grup.kartlar_arasi_mm 1.5) kept above the controller's 1.5
    sx = W / float(t["izgara_mm"]["genislik"])
    P = {p["ad"]: {k: float(v) * sx for k, v in p["konum"].items()} for p in t["paneller"]}
    H = round(float(t["izgara_mm"]["yukseklik"]), 2)
    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    aw = P["A"]["w"] - M
    bx = M + aw + gap
    bw = (W - M - bx - gap) / 2
    th = P["B"]["h"]
    A = cv.card(None, "Rank correlation", M, M, aw, H - 2 * M, tint="neutral",
                n_exempt="one statistic per data set")
    axA = A.axes(left=21.0, right=3.0, top=cards.BAND + 2.0, bottom=30.0)
    drawn = {"ozet": summary(axA)}
    legend_below(axA, 21.0, frame=False)
    keys = list(DATA)
    cardsB = []
    for i, key in enumerate(keys[:2]):
        d = DATA[key]
        c = cv.card(None, d["title"], bx + i * (bw + gap), M, bw, th, tint="neutral", note=f"n = {d['pairs']}")
        avail = th - cards.BAND - 1.0 - 9.5
        sub = (avail - 6.5) / 2
        ax1 = c.axes(left=14.0, right=2.5, top=cards.BAND + 1.0, bottom=9.5 + sub + 6.5)
        ax2 = c.axes(left=14.0, right=2.5, top=cards.BAND + 1.0 + sub + 6.5, bottom=9.5)
        drawn[f"{key}_ham"] = scatter(ax1, d, True, small=True)
        drawn[f"{key}_artik"] = scatter(ax2, d, False, small=True)
        ax1.set_ylabel("log τ", labelpad=1)
        ax2.set_ylabel("residual", labelpad=1)
        ax2.set_xlabel("c residual (upper: raw c)", labelpad=1)
        cardsB.append(c)
    d = DATA[keys[2]]
    dy = M + th + gap
    dw = W - M - bx
    D = cv.card(None, d["title"], bx, dy, dw, H - M - dy, tint="neutral", note=f"n = {d['pairs']}")
    hw = dw / 2
    ax1 = D.axes(left=14.0, right=hw + 1.0, top=cards.BAND + 1.0, bottom=9.5)
    ax2 = D.axes(left=hw + 13.5, right=2.5, top=cards.BAND + 1.0, bottom=9.5)
    drawn[f"{keys[2]}_ham"] = scatter(ax1, d, True)
    drawn[f"{keys[2]}_artik"] = scatter(ax2, d, False)
    ax1.set_xlabel("cosine c", labelpad=1)
    ax1.set_ylabel("log τ", labelpad=1)
    ax2.set_xlabel("c residual", labelpad=1)
    ax2.set_ylabel("residual", labelpad=1)
    cv.title_strip([A] + cardsB)
    cv.title_strip([D])
    return cv, drawn


def lay_1():
    from matplotlib.patches import Rectangle
    H = 100.0
    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    keys = list(DATA)
    gx = gy = 3.0
    cw = (W - 2 * M - 2 * gx) / 3
    top_h = 60.0
    bot_h = H - 2 * M - top_h - gy
    stripe = U.tones().get("zemin_gri", U.tones()["kap"])[0]
    drawn = {}
    rows = [[], []]
    for k, key in enumerate(keys):
        d = DATA[key]
        x = M + k * (cw + gx)
        c = cv.card(None, d["title"], x, M, cw, top_h, tint="zemin", note=f"n = {d['pairs']}")
        ax = c.axes(left=14.0, right=2.5, top=cards.BAND + 5.0, bottom=31.0)
        drawn[f"{key}_ham"] = scatter(ax, d, True, above=True)
        ax.set_xlabel("gradient cosine c", labelpad=1)
        if k == 0:
            ax.set_ylabel("log τ", labelpad=1)
        # the template's aligned table under the panel (Jiao's risk table): pairs and mean c per type
        ty = top_h - 20.5
        tb = cv.axes(x + 2.5, M + ty, cw - 5.0, 19.0)
        tb.set_xticks([])
        tb.set_yticks([])
        for sp in tb.spines.values():
            sp.set_visible(False)
        tb.set_facecolor("none")
        tb.add_patch(Rectangle((0, 0), 1, 1, transform=tb.transAxes, facecolor="white", edgecolor=MUTED,
                               linewidth=ST.weights.grid, gid="bg_table"))
        for i in range(3):
            if i % 2 == 0:
                tb.add_patch(Rectangle((0.03, 0.72 - (i + 1) * 0.2 - 0.02), 0.94, 0.2, transform=tb.transAxes,
                                       facecolor=stripe, edgecolor="none", gid="bg_stripe"))
        c.text(4.5, ty + 4.5, "pair type", fontsize=ST.type_scale.annot, color=MUTED, va="baseline")
        c.text(cw * 0.62, ty + 4.5, "pairs", fontsize=ST.type_scale.annot, color=MUTED, va="baseline", ha="right")
        c.text(cw - 4.5, ty + 4.5, "mean c", fontsize=ST.type_scale.annot, color=MUTED, va="baseline", ha="right")
        for i, (tk, e, lab) in enumerate(TYPES):
            yy = ty + 8.6 + i * 3.8
            ent = PAL[e]      # the row's marker doubles as the key (the style's direct-label rule)
            tb.plot([2.6 / (cw - 5.0)], [1 - (yy - 1.15 - ty) / 19.0], transform=tb.transAxes, ls="none",
                    marker=ent.marker, ms=4.0, mfc=ent.hex, mec=INK, mew=0.3, clip_on=False)
            c.text(6.5, yy, "T–T" if tk == "T-T" else lab, fontsize=ST.type_scale.annot, color=INK, va="baseline")
            c.text(cw * 0.62, yy, str(d["tur"][tk]["n"]), fontsize=ST.type_scale.annot, color=INK, va="baseline",
                   ha="right")
            c.text(cw - 4.5, yy, f"{d['tur'][tk]['mean_c']:.3f}", fontsize=ST.type_scale.annot, color=INK,
                   va="baseline", ha="right")
        drawn[f"{key}_tablo"] = d["tur"]
        rows[0].append(c)
        c2 = cv.card(None, "residual", x, M + top_h + gy, cw, bot_h, tint="zemin", note=f"n = {d['pairs']}")
        ax2 = c2.axes(left=14.0, right=2.5, top=cards.BAND + 5.0, bottom=9.5)
        drawn[f"{key}_artik"] = scatter(ax2, d, False, above=True)
        ax2.set_xlabel("c residual", labelpad=1)
        if k == 0:
            ax2.set_ylabel("log τ residual", labelpad=1)
        rows[1].append(c2)
    cv.title_strip(rows[0])
    cv.title_strip(rows[1])
    return cv, drawn


LAYOUT = {"7": lay_7, "H": lay_H, "1": lay_1}


def main():
    cv, drawn = LAYOUT[NO]()
    msg = ("Input-gradient cosine tracks pairwise symmetric similarity on all three data sets, raw and with "
           "additive model main effects removed.")
    cv.save(STEM, OUT, message=msg, sources=INPUTS)
    deg = []
    for key, d in DATA.items():
        deg.append({"etiket": f"{key} raw Spearman", "deger": d["rs_h"], "kaynak": d["kaynak"],
                    "anahtar_yolu": "sinamalar.ham.istatistik", "hesap": "recomputed == JSON (1e-9) == foy (1e-3)"})
        deg.append({"etiket": f"{key} residual Spearman", "deger": d["rs_r"], "kaynak": d["kaynak"],
                    "anahtar_yolu": "sinamalar.ana_etki_artik.istatistik",
                    "hesap": "recomputed == JSON (1e-9) == foy (1e-3)"})
        deg.append({"etiket": f"{key} pairs", "deger": d["pairs"], "kaynak": d["kaynak"],
                    "anahtar_yolu": "sinamalar.ham.cift_sayisi", "hesap": "upper triangle of c_matrisi; == foy"})
        for tk, v in d["tur"].items():
            deg.append({"etiket": f"{key} {tk} n", "deger": v["n"], "kaynak": d["kaynak"],
                        "anahtar_yolu": "c_matrisi + hucre_tablosu modeller.<m>.aile",
                        "hesap": "count of pairs of this type; == foy 2009-2011"})
            deg.append({"etiket": f"{key} {tk} mean c", "deger": v["mean_c"], "kaynak": d["kaynak"],
                        "anahtar_yolu": "c_matrisi + hucre_tablosu modeller.<m>.aile",
                        "hesap": "mean of c over pairs of this type; == foy 2009-2011 (3 decimals)"})
    p = write_kanit(STEM, OUT, uslup_no=U.no, degerler=deg, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    k.update({"foy_karsilastirmasi": FOY, "okunan_anahtarlar": OKUNAN, "cizilen": drawn,
              "git": K.git_info(INPUTS), "betik": "paper/figures/charts/_onizleme_gradient_alignment.py --uslup " + NO})
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False, default=float) + "\n")
    print(f"written: {OUT / STEM}.pdf  foy comparisons {FOY['karsilastirma_sayisi']}, all matched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
