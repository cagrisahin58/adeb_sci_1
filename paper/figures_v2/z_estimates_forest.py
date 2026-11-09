#!/usr/bin/env python
"""z_estimates_forest (Fig. 12 v2, Üslup Z): registered estimates on two flat cards.

    python paper/figures_v2/z_estimates_forest.py [--check] [--bak]

Single column, flat-card composition (third round, 09.11.2026: the tablet, its plinth and the recessed panels of
the second round are gone; this also closes review finding 3, the stone-slab repeat of Figures 11 and 12). Two
flat cards stacked on one left edge each hold one forest plot. Upper card: contrasts on panel similarity sigma;
lower panel: directional terms. Point estimate (circle log, diamond logit, open = descriptive), thick bar 90 %,
thin line 95 % confidence interval; the +-0.10 lines and the H1 size line over the log rows of the upper panel,
the +-0.10 band over the log rows of the lower panel. Data: the v1
rule paper/figures/charts/fig_estimates_forest.py veri() (results/q1 B2, B4, B8, B9; sheet lines 1526-1939).
Naming: step 4 (title strips, family colour as a small square beside the name).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
EF = Z.yukle("paper/figures/charts/fig_estimates_forest.py", "v1_estimates_forest")

STEM = "z_estimates_forest"
KIND = "single"
W = vf.page_width(KIND)
CARDS = [("a", "Contrasts on panel similarity σ", "vurgu2", (-0.62, 0.52), (-0.6, -0.4, -0.2, 0.0, 0.2, 0.4),
          "contrast on σ"),
         ("b", "Directional terms", "vurgu4", (-0.62, 0.24), (-0.6, -0.4, -0.2, 0.0, 0.2),
          "directional term ρ or A(ρ)")]
LABEL = {"ImageNetV2 mean $\\bar{A}^{\\sigma}_{\\mathrm{IN}}$": "IN-V2 Ā(σ, IN)"}
CAPTION = ("Registered estimates. Upper panel, Contrasts on panel similarity σ: H1, H2 and descriptive "
           "ImageNetV2 rows; lower panel, Directional terms: K-b and H3. Circles log, diamonds logit, open marks "
           "descriptive; thick and thin bars are 90% and 95% intervals; the ±0.10 lines apply to log rows only.")


def main():
    D, foy, okunan = EF.veri()
    delta, thr = D["delta"], D["thr"]
    vf.reset(STEM, W, 130.0, naming_step=4, naming_kind="serit")
    XL, XR = 1.0, W - 1.0
    RP, LABW = 4.5, 25.0
    heights = [5.6 + len(D[k]) * RP + 2.0 + lh(Z.S8) + 2.6 + lh(Z.S8) + 1.0 for k, *_ in CARDS]
    # third round (09.11.2026): two flat cards stacked on one left edge; no plinth, no tablet, no recess walls
    # (closes review finding 3, the stone-slab repeat of Figures 11 and 12)
    GAPC = 2.4
    deg = []
    col = {}
    ry = 1.0
    for ci, (key, title, ckey, (v0, v1), ticks, axlab) in enumerate(CARDS):
        ch = heights[ci]
        face = f"rec{ci}_face"
        fx, fy, fw, fh = Z.duz_kart(f"rec{ci}", XL, ry, XR - XL, ch, "kutu")
        y1 = ry + ch
        ry = y1 + GAPC
        c = vf.C[ckey]
        col[key] = c
        Z.isaret(f"tsq{ci}", fx + 3.0, fy + 2.4 + lh(Z.S8) / 2, "s", fill=c, edge=c, size=2.0, group=f"card{ci}")
        T(f"ti{ci}", fx + 4.8, fy + 2.4, [[(title, "sb")]], size=Z.S8, cont=face)
        # third round: Visio printed the right-aligned "6 estimates" 0.31 mm past its box; the label is now
        # left-aligned in a box with 1.2 mm slack, its right edge where the right-aligned box ended
        tnw = Z.tw([f"{len(D[key])} estimates"], Z.S8) + 1.2
        T(f"tn{ci}", fx + fw - 1.2 - tnw + 1.2, fy + 2.4, [f"{len(D[key])} estimates"], size=Z.S8, color="muted",
          cont=face, w=tnw)
        px0, px1 = fx + LABW + 1.0, fx + fw - 2.0
        sc = Z.Olcek(v0, v1, px0, px1)
        ytop = fy + 2.4 + lh(Z.S8) + 1.8
        rows = D[key]
        ybot = ytop + len(rows) * RP
        logrows = [i for i, r in enumerate(rows) if r[1] == "log" and r[2] == "reg"]
        if key == "b":
            ylo = ytop + (max(logrows) + 1) * RP
            band = [(sc(-delta), ytop), (sc(delta), ytop), (sc(delta), ylo), (sc(-delta), ylo)]
            vf.poly("bandb", band + [band[0]], fill=vf.tint_of("ton_4")[0], line=None, role="deco", container=face)
        else:
            nlog = [i for i, r in enumerate(rows) if r[1] == "log"]
            ylo = ytop + (max(nlog) + 1) * RP
            for v, dash, nm in ((-delta, True, "dm"), (delta, True, "dp"), (thr, True, "h1")):
                vf.seg(f"ref_{nm}", (sc(v), ytop), (sc(v), ylo), vf.C["frame"] if nm != "h1" else vf.C["muted"],
                       vf.LW["ince"], dash=dash)
        vf.seg(f"zero{ci}", (sc(0.0), ytop), (sc(0.0), ybot), vf.C["ink"], vf.LW["ince"])
        prev = None
        for i, (lab, scl, st, d, n, anc) in enumerate(rows):
            yc = ytop + i * RP + RP / 2
            grp = (scl, st)
            if prev is not None and grp != prev:
                vf.seg(f"sep{ci}_{i}", (fx + 1.0, ytop + i * RP), (fx + fw - 1.0, ytop + i * RP), vf.C["frame"],
                       vf.LW["ince"])
            prev = grp
            plab = EF.SATIR[lab][0]
            plab = LABEL.get(lab, plab)
            T(f"rl{ci}_{i}", fx + LABW, yc - lh(Z.S8) / 2, [plab], size=Z.S8, align="r", cont=face)
            vf.seg(f"c95_{ci}_{i}", (sc(d["c95"][0]), yc), (sc(d["c95"][1]), yc), c, vf.LW["ince"])
            bar = [(sc(d["c90"][0]), yc - 0.55), (sc(d["c90"][1]), yc - 0.55), (sc(d["c90"][1]), yc + 0.55),
                   (sc(d["c90"][0]), yc + 0.55)]
            vf.poly(f"c90_{ci}_{i}", bar + [bar[0]], fill=c, line=None, role="obstacle", group=f"est{ci}_{i}")
            mk = "o" if scl == "log" else "D"
            Z.isaret(f"pt{ci}_{i}", sc(d["e"]), yc, mk, fill=None if st == "desc" else c, edge="ink", size=2.0,
                     group=f"est{ci}_{i}")
            psrc, src, kp, ek, k90, k95 = EF.SATIR[lab]
            for nm, v, yol in (("estimate", d["e"], f"{kp}.{ek}"), ("ci90 low", d["c90"][0], f"{kp}.{k90}[0]"),
                               ("ci90 high", d["c90"][1], f"{kp}.{k90}[1]"), ("ci95 low", d["c95"][0], f"{kp}.{k95}[0]"),
                               ("ci95 high", d["c95"][1], f"{kp}.{k95}[1]")):
                deg.append(Z.ev(f"{plab} {nm}", v, src, yol, f"read as stored; == foy line {n} (3 dp); position"))
        if key == "a":
            ins = [i for i, r in enumerate(rows) if r[2] == "desc"]
            T("boot", fx + fw - 1.6,   # third round: 0.4 mm further in (Visio printed it 0.32 mm past its box)
              ytop + (ins[0] + 1.0) * RP - 0.2, ["image", "bootstrap"], size=Z.S8,
              color="muted", align="r", cont=face)
        Z.kot(f"ax{ci}", px0, px1, ybot + 0.6, sc, list(ticks), [Z.fmt(t_, 1) if t_ else "0" for t_ in ticks],
              cont=face)
        T(f"axl{ci}", (px0 + px1) / 2, ybot + 0.6 + 1.4 + lh(Z.S8), [axlab], size=Z.S8, color="muted", align="c",
          cont=face)
    # legend under the cards; bulgu 5 (08.11): the key rule is the 1.5 pt (vurgu) line (as Figures 7, 13, 16)
    yl = ry - GAPC + 2.4
    vf.seg("rule", (1.0, yl - 0.8), (W - 1.0, yl - 0.8), vf.C["frame"], vf.LW["vurgu"])
    items = [("o", True, "log"), ("D", True, "logit"), ("o", False, "descriptive")]
    x = 1.0
    for j, (mk, filled, labx) in enumerate(items):
        Z.isaret(f"lg{j}", x + 1.0, yl + lh(Z.S8) / 2, mk, fill="muted" if filled else None, edge="ink", size=2.0)
        T(f"lgt{j}", x + 2.4, yl, [labx], size=Z.S8)
        x += 2.4 + Z.tw([labx], Z.S8) + 2.0
    bar = [(x, yl + lh(Z.S8) / 2 - 0.55), (x + 4.0, yl + lh(Z.S8) / 2 - 0.55), (x + 4.0, yl + lh(Z.S8) / 2 + 0.55),
           (x, yl + lh(Z.S8) / 2 + 0.55)]
    vf.poly("lgbar", bar + [bar[0]], fill=vf.C["muted"], line=None, role="obstacle")
    T("lgbart", x + 4.8, yl, ["90%, line 95%"], size=Z.S8)
    yl += lh(Z.S8) + 0.4
    vf.seg("lgdash", (1.0, yl + lh(Z.S8) / 2), (5.0, yl + lh(Z.S8) / 2), vf.C["frame"], vf.LW["ince"], dash=True)
    T("lgdasht", 5.8, yl, [f"±{delta:.2f} (log rows); H1 size {Z.fmt(thr, 2)}, darker"], size=Z.S8)
    for _pid in ["ti0", "ti1"]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    deg.append(Z.ev("delta", delta, EF.J4P, "meta.delta", "read as stored; == foy line 1532 text"))
    deg.append(Z.ev("H1 size threshold", thr, EF.J8P, "A_sigma_scr_Liu.beklenti_esigi", "read; == foy line 1939"))
    ents = {"sigma": "#" + col["a"], "rho": "#" + col["b"]}
    return Z.bitir(
        STEM, message="H1 and H2 clear the registered margin on both scales; the directional terms stay small on "
                      "the log scale.", kind=KIND, panels=2, caption=CAPTION, sablon="ortak_satirli_katlar",
        tur="veri", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan},
        manifest={"entities": ents, "sahne_kalibi": "yok (iki duz kart, ucuncu tur)",
                  "panel_adlari": [c[1] for c in CARDS],
                  "derinlik_ekseni": "none: flat cards"},
        denge={"panel_basina_bir_iddia": (True, "upper panel the sigma contrasts, lower panel the directional terms")},
        n_exempt_reason="each panel prints its estimate count in the title strip",
        okunan_ek=list(okunan) if isinstance(okunan, dict) else [])


if __name__ == "__main__":
    sys.exit(main())
