#!/usr/bin/env python
"""Protocol spread versus clean-accuracy gap over all model pairs; card figure, visio-cizici
style 7 (plan 04_cizim_plani.md section 9.15).

    python paper/figures/charts/fig_spread_clean_gap.py --uslup 7

Single column, two stacked cards on a shared x (|clean-accuracy gap|, pts): top, the
three-protocol spread (raw, target-correct, both-correct) per model pair with the identity
prediction |raw - target-correct| at p = 1 as a small open ring at the same x; bottom, the
successful-source minus both-correct asymmetry (signed) with a dashed zero line. Eight groups by
the paper palette's ayar family (hex and marker shape per group; the group of each palette entry
is its veri_grubu field, read from the palette file). A key strip at the bottom.

Data rule: paper/figures/fig_yayilim_temiz_fark.py (left untouched) supplies load_and_check
(definition checks of every plotted field, quarantine-safe sources, identity parity). Added here:
per group the point count and the ranges of |clean gap| and three-protocol spread against the
reference sheet table (lines 1022-1030), the identity parity line 1073 and the source line 1014.
A mismatch writes nothing.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
sys.path.insert(0, str(Path(O.ROOT_S) / "paper" / "figures"))
import fig_yayilim_temiz_fark as YT  # noqa: E402  (data rules only; its main() is not run)

ARGS = O.argumanlar(__doc__)
STEM = "spread_clean_gap"
SCRIPT = "paper/figures/charts/fig_spread_clean_gap.py"
DATA = "results/q1/fig_yayilim_temiz_fark_veri.json"


def veri():
    d, parity_dev = YT.load_and_check(Path(DATA))
    N = d["noktalar"]
    foy = K.Foy()
    by = defaultdict(list)
    for n in N:
        by[n["grup"]].append(n)
    foy.metin("source line", "results/q1/fig_yayilim_temiz_fark_veri.json", 1014, "_Kaynak:")
    rows = {}
    for ln in range(1022, 1031):
        t = foy.lines[ln - 1]
        g = t.split("|")[1].strip()
        rows[g] = ln
    if set(rows) - {"Tum noktalar"} != set(by):
        K.fail(f"sheet group rows {sorted(rows)} != data groups {sorted(by)}")
    for g, pts in list(by.items()) + [("Tum noktalar", N)]:
        ln, anc = rows[g], f"| {g} |"
        xs = [p["temiz_fark_mutlak"] for p in pts]
        ys = [p["yayilim_uc"] for p in pts]
        foy.kontrol(f"{g}: n", len(pts), ln, anc, 0)
        foy.kontrol(f"{g}: |clean gap| min", min(xs), ln, anc, 2)
        foy.kontrol(f"{g}: |clean gap| max", max(xs), ln, anc, 2)
        foy.kontrol(f"{g}: spread (three) min", min(ys), ln, anc, 2)
        foy.kontrol(f"{g}: spread (three) max", max(ys), ln, anc, 2)
    par = d["egim"]["ozdeslik_paritesi"]
    foy.kontrol("identity parity max |dev|", par["mutlak_sapma_max"], 1073, "mutlak sapma en buyuk", 2)
    foy.kontrol("identity parity n", par["n"], 1073, "mutlak sapma en buyuk", 0)
    return d, by, parity_dev, foy.bitir()


def main():
    d, by, parity_dev, foy = veri()
    N = d["noktalar"]
    O.basla(ARGS.uslup)
    import math
    import yaml
    from matplotlib.lines import Line2D
    from matplotlib.ticker import MultipleLocator
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    raw = yaml.safe_load(Path(ST.palette_path).read_text(encoding="utf-8"))["entities"]
    G2E = {v["veri_grubu"]: k for k, v in raw.items() if v.get("aile") == "ayar" and v.get("veri_grubu")}
    if set(by) - set(G2E):
        K.fail(f"groups without a palette ayar entry: {sorted(set(by) - set(G2E))}")
    # denge.py forbids more than six accent hues; the palette's ayar family has seven chromatic hexes
    # plus the grey pool, so one group is drawn neutral: open mark, ink edge, its palette shape
    NEUTRAL = {k for k, v in raw.items() if k == "ayar_std"}

    def look(g):
        e = O.ent(G2E[g])
        if G2E[g] in NEUTRAL:
            return dict(marker=e.marker, mfc="white", mec=U.ink, mew=ST.weights.emph)
        ec, ew = O.kenar(G2E[g])
        return dict(marker=e.marker, mfc=e.hex, mec=ec, mew=ew)
    order = [g for g in G2E if g in by]
    pool = [g for g in order if "havuz" in g]
    order = pool + [g for g in order if g not in pool]          # the large pool first, under the others
    W = O.W("single")
    H = 119.0
    M, GY, KEY_H = 0.5, 1.6, 19.0
    ch = (H - 2 * M - KEY_H - 2 * GY) / 2
    L, R, T, B = 14.0, 3.0, cards.BAND + 1.0, 9.0
    ms, mew = vg["ortalama_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    cv = cards.Canvas("single", H, naming_step=4, naming_kind="serit")
    specs = [("Three-protocol spread", "spread (pts)", "yayilim_uc"),
             ("Successful-source minus both-correct", "difference (pts)", "bas_kaynak_eksi_bc_asimetri")]
    xs_all = [n["temiz_fark_mutlak"] for n in N]
    xmax = 5 * math.ceil((max(xs_all) * 1.02) / 5)
    kart, cizilen = [], {}
    for r, (title, yl, fld) in enumerate(specs):
        c = cv.card(None, title, M, M + r * (ch + GY), W - 2 * M, ch, tint="kap", note=f"n = {len(N)} pairs")
        ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
        O.eksen(ax, base="x", grid="both")
        for z, g in enumerate(order):
            pts = by[g]
            ax.plot([p["temiz_fark_mutlak"] for p in pts], [p[fld] for p in pts], ls="none", ms=ms, zorder=3 + z,
                    **look(g))
        if fld == "yayilim_uc":
            ax.plot(xs_all, [abs(n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"]) for n in N], ls="none", marker="o",
                    ms=vg["tohum_markersize_pt"], mfc="none", mec=U.ink, mew=ST.weights.emph, zorder=20)
            ax.yaxis.set_major_locator(MultipleLocator(5))
        else:
            ax.axhline(0.0, color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
            ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.set_xlim(-0.02 * xmax, xmax)
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.set_ylabel(yl, labelpad=1)
        ax.set_xlabel("|clean-accuracy gap| (pts)", labelpad=1)
        O.tick_fmt(ax)
        kart.append(c)
    cv.title_strip(kart)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white", n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c, inset=0.9)
    hs = []
    for g in [g for g in G2E if g in by]:
        # display form of the palette label (the palette file keeps its ASCII 'Linf' / 'L2')
        lab = O.ent(G2E[g]).label.replace("Linf", "L∞").replace(" L2 ", " L₂ ")
        hs.append(Line2D([], [], ls="none", ms=ms, label=lab, **look(g)))
    hs.append(Line2D([], [], ls="none", marker="o", ms=vg["tohum_markersize_pt"], mfc="none", mec=U.ink,
                     mew=ST.weights.emph, label="identity prediction"))
    kax.legend(handles=hs, loc="center", ncol=2, frameon=False, handletextpad=0.3, columnspacing=1.0,
               labelspacing=0.25, borderaxespad=0.0)
    deg = []
    for i, n in enumerate(N):
        for f in ("temiz_fark_mutlak", "yayilim_uc", "bas_kaynak_eksi_bc_asimetri",
                  "raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"):
            deg.append(O.deger(f"pair {i} ({n['grup']}) {f}", n[f], DATA, f"noktalar[{i}].{f}",
                               "read as stored; recomputed from its definition fields (load_and_check)"))
    cizilen = {"gruplar": {g: {"varlik": G2E[g], "nokta": len(by[g])} for g in by},
               "ozdeslik_paritesi_max_sapma": parity_dev, "x_ust": xmax}
    O.kaydet(cv, STEM, message=("Three-protocol spread and the successful-source term against the clean-accuracy gap, "
                                "all 60 model pairs."),
             inputs=[DATA] + list(d["kaynaklar"]), degerler=deg, foy=foy,
             okunan={DATA: ["noktalar[*].{grup, temiz_a, temiz_b, temiz_fark_mutlak, asimetri, yayilim_uc, "
                            "raw_eksi_tc_asimetri_olculen, raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1, "
                            "bas_kaynak_eksi_bc_asimetri}", "egim.ozdeslik_paritesi", "kaynaklar", "n_nokta"]},
             cizilen=cizilen,
             notlar=["Pairs listed twice in the data file (same checkpoints measured in two runs) are drawn twice, "
                     "as in the council figure.",
                     "The sheet lists per-group ranges, not every point; per-point values are checked against their "
                     "definition fields in the data file the sheet cites (line 1014)."],
             kararlar=["Karar (duzeltme turu 2): the key writes 'L∞' and 'L₂' (display form of the palette "
                       "labels, as in protocol_settings and the final figure), and the bottom y label reads "
                       "'difference (pts)', because the card title already spells 'Successful-source minus "
                       "both-correct' and the two-line label 'successful-source - both-correct' would need about "
                       "30 mm on a 31 mm axis; the abbreviation 'ss - bc' is gone.",
                       "Karar: the eight groups take the paper palette's ayar family (hex and shape), because the "
                       "council figure's orange, green, blue and vermilion collide with the semantic colours of "
                       "sigma, rho, R224 and ViT (plan 9.15).",
                       "Karar: the standard-training group is drawn as an open mark with an ink edge (its palette "
                       "shape kept), because the ayar family has seven chromatic hexes besides the grey pool and "
                       "denge.py forbids more than six accent hues in one figure; the palette entry ayar_std is left "
                       "unused here (open issue for the palette generator).",
                       "Karar: (a) and (b) become two title-strip cards, referred to by position."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tasarim_izgarasi")
    O.ajan(STEM, iddia="top card spread versus gap, bottom card the successful-source term",
           dogrudan_etiket="titles name the quantity; groups are keyed by shape and hue")
    return 0


if __name__ == "__main__":
    sys.exit(main())
