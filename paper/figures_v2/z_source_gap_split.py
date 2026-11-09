#!/usr/bin/env python
"""z_source_gap_split (Fig. 7 v2, Üslup Z): the source gap split into symmetric and directional parts on three
flat cards.

    python paper/figures_v2/z_source_gap_split.py [--check] [--bak]

Double column, flat-card composition (third round, 09.11.2026: the receding floor slabs are gone, and with them
the K7 exemption). Three flat cards stacked top to bottom (CIFAR-10, CIFAR-100, descriptive ImageNetV2) share
one x scale; on each, three pairs are horizontal bars: from zero to the symmetric part (olive), from there to
the total gap G (lavender grey; a negative directional part turns left, drawn with a dashed edge), an ink diamond
at G. Zero line, faint gridlines and, on ImageNetV2, the registered 0.10 threshold are vertical; every row also
prints G and q = symmetric / G (n/a for the ImageNetV2 pair at or under the threshold). Data: the v1 rule paper/figures/charts/fig_source_gap_split.py veri()
(three frozen B2 outputs; sheet lines 1587-1932). Naming: step 4 (one title strip per card).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
SG = Z.yukle("paper/figures/charts/fig_source_gap_split.py", "v1_source_gap_split")

STEM = "z_source_gap_split"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Source gap split into symmetric and directional parts. One card per data set, one log-unit scale; "
           "per seed pair on CIFAR-10 and CIFAR-100 and per same-recipe pair on ImageNetV2 (descriptive): olive "
           "symmetric part, lavender-grey directional part, diamond total G; each row prints G and the share q. "
           "A dashed part narrows the gap.")


def main():
    data, foy, okunan = SG.veri()
    vf.reset(STEM, W, 120.0, naming_step=4, naming_kind="serit")
    # third round (09.11.2026): three flat cards stacked top to bottom (CIFAR-10, CIFAR-100, descriptive
    # ImageNetV2); each holds a flat horizontal bar chart on one shared x scale. No slab, no depth, no K7 exemption.
    LAB, SCW = 31.0, 92.0
    RD, BH = 4.6, 2.0
    PADT, PADB = 1.4, 2.2
    CH = PADT + 3 * RD + PADB
    CX, CW = 1.0, W - 2.0
    v0, v1 = -0.10, 0.50
    LH = lh(Z.S8)
    deg = []
    cy = 1.0
    x_of = None
    for s_, (key, path, title, unit) in enumerate(SG.SETS):
        d = data[key]
        fx, fy, fw, fh = Z.duz_kart(f"slab{s_}", CX, cy, CW, CH, "kutu")
        face = f"slab{s_}_face"
        sc = Z.Olcek(v0, v1, fx + LAB, fx + LAB + SCW)
        x_of = sc
        ya0, ya1 = fy + PADT - 0.4, fy + PADT + 3 * RD + 0.2
        yax = fy + PADT + 3 * RD + 0.6
        # faint gridlines at the ticks, the zero line, the threshold on the ImageNetV2 card, the base line (kot)
        for t_ in (0.1, 0.2, 0.3, 0.4, 0.5):
            vf.seg(f"gl{s_}_{t_}", (sc(t_), ya0), (sc(t_), ya1), vf.tint_of("izgara")[0], vf.LW["ince"])
        vf.seg(f"z{s_}", (sc(0.0), ya0), (sc(0.0), ya1), vf.C["frame"], vf.LW["ince"])
        if key == "in":
            vf.seg("thr", (sc(d["delta"]), ya0), (sc(d["delta"]), ya1), vf.C["muted"], vf.LW["ince"], dash=True)
        Z.kot(f"ax{s_}", sc(v0), sc(v1), yax, sc, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
              labels=[None] * 6, cont=face)
        for i in range(3):
            yc = fy + PADT + i * RD + RD / 2
            sym, dr, G = d["sym"][i], d["dir"][i], d["D"][i]

            def strip(pid, a, b, fill, dash=False):
                p = [(sc(a), yc - BH / 2), (sc(b), yc - BH / 2), (sc(b), yc + BH / 2), (sc(a), yc + BH / 2)]
                vf.poly(pid, p + [p[0]], fill=fill, line=Z.soft(fill, 0.35) if not dash else vf.C["ink"],
                        lw=vf.LW["ince"], role="obstacle", group=f"r{s_}_{i}")
            strip(f"sy{s_}_{i}", 0.0, sym, vf.C["vurgu2"])
            if dr >= 0:
                strip(f"dr{s_}_{i}", sym, G, vf.C["vurgu4"])
            else:
                strip(f"dr{s_}_{i}", G, sym, vf.tint_of("ton_4")[0])
                vf.seg(f"drd{s_}_{i}", (sc(G), yc - BH / 2), (sc(sym), yc - BH / 2), vf.C["ink"], vf.LW["ince"],
                       dash=True)
            Z.isaret(f"g{s_}_{i}", sc(G), yc, "D", fill="ink" if key != "in" else None, edge="ink", size=1.9,
                     group=f"r{s_}_{i}")
            T(f"rl{s_}_{i}", fx + LAB - 2.0, yc - LH / 2, [f"pair {i + 1}"], size=Z.S8, align="r",
              color="muted", cont=face)
            qtxt = "q n/a" if i in d["payda_kucuk"] else f"q {d['q'][i]:.2f}"
            gtxt = f"{G:.4f}" if i in d["payda_kucuk"] else f"{G:.3f}"   # 0.0999 is under 0.10
            T(f"vv{s_}_{i}", fx + LAB + SCW + 4.0, yc - LH / 2, [f"G {gtxt}   {qtxt}"], size=Z.S8, cont=face)
            for nm, fld, jk in (("G", "D", "D"), ("symmetric", "sym", "simetrik_pay"), ("directional", "dir", "yonlu_pay"),
                                ("q", "q", "q")):
                ln = (SG.FOY_LINES[key][0] if key in SG.FOY_LINES else SG.FOY_IN_PAIR[i])
                deg.append(Z.ev(f"{title} {unit} {i + 1} {nm}", d[fld][i], path, f"b2.F_B2.K-a.{jk}[{i}]",
                                f"read as stored; G == sym + dir, q == sym / G (1e-12); near foy line {ln}"))
        tt = title.split(", ")[0]
        subs = [unit + "s,", "descriptive"] if key == "in" else [unit + "s"]
        T(f"st{s_}", fx + 1.2, fy + PADT, [[(tt, "sb")]] + subs, size=Z.S8, cont=face)
        cy += CH + 1.6
    # tick labels once, under the last card, then the legend
    fy = cy - 1.6 + 0.4
    for t_ in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        T(f"tl{t_}", x_of(t_), fy, [f"{t_:.1f}"], size=Z.S8, align="c", color="muted")
    T("axl", x_of(0.2), fy + LH + 0.2, ["log units; one scale for the three cards"], size=Z.S8,
      color="muted", align="c")
    yl = fy + 1.6 + 2 * LH
    x = 1.0
    for j, (kind_, col, lab) in enumerate((("s", vf.C["vurgu2"], "symmetric part"), ("s", vf.C["vurgu4"], "directional part"),
                                            ("D", vf.C["ink"], "total G"), ("D", None, "descriptive (open)"),
                                            ("-", None, "registered 0.10 threshold"))):
        if kind_ == "-":
            vf.seg(f"lg{j}", (x, yl + LH / 2), (x + 3.0, yl + LH / 2), vf.C["muted"], vf.LW["ince"], dash=True)
        else:
            Z.isaret(f"lg{j}", x + 1.2, yl + LH / 2, kind_, fill=col, edge=col or "ink", size=2.0)
        T(f"lgt{j}", x + 3.6, yl, [lab], size=Z.S8)
        x += 3.6 + Z.tw([lab], Z.S8) + 3.0
    vf.seg("rule", (1.0, yl - 0.5), (W - 1.0, yl - 0.5), vf.C["frame"], vf.LW["vurgu"])
    # review round 2: where "q n/a" comes from (the registered denominator rule, D = G at or below delta)
    T("lgq", 1.0, yl + LH + 0.4,
      [f"q n/a: G at or below the registered {Z.fmt(data['in']['delta'], 2)} threshold, so the share is not computed"],
      size=Z.S8, color="muted")
    for _pid in [f"st{i}" for i in range(3)]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    deg.append(Z.ev("ImageNetV2 registered G threshold", data["in"]["delta"], SG.J8P, "meta.delta",
                    "read as stored; == foy line 1926"))
    ents = {"sigma": "#" + vf.C["vurgu2"], "rho": "#" + vf.C["vurgu4"]}
    return Z.bitir(
        STEM, message="On CIFAR-10 and CIFAR-100 the symmetric part carries 81 to 94 percent of the source gap; on "
                      "ImageNetV2 the descriptive shares spread and one pair falls under the threshold.",
        kind=KIND, panels=3, caption=CAPTION, sablon="ortak_satirli_katlar", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan},
        manifest={"entities": ents, "sahne_kalibi": "yok (duz kartlar, ucuncu tur)",
                  "panel_adlari": [s[2] for s in SG.SETS],
                  "derinlik_ekseni": "none: flat cards on one shared x scale"},
        denge={"panel_basina_bir_iddia": (True, "each card is one data set's source-gap split")},
        n_exempt_reason="three pairs per data set, each printed on its own row", okunan_ek=list(okunan))


if __name__ == "__main__":
    sys.exit(main())
