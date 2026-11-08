#!/usr/bin/env python
"""z_source_gap_split (Fig. 7 v2, Üslup Z): the source gap split into symmetric and directional parts on three
receding floor slabs.

    python paper/figures_v2/z_source_gap_split.py [--check] [--bak]

Double column. Three slabs recede in depth (CIFAR-10 in front, CIFAR-100, descriptive ImageNetV2 at the back);
on each, three pairs lie as flat strips along the page-horizontal floor direction u: from zero to the symmetric
part (olive), from there to the total gap G (lavender grey; a negative directional part turns left, drawn with a
dashed edge), an ink diamond at G. The zero line and the registered 0.10 threshold run along the slab depth;
ticks sit on each slab's front edge. K7: the strips are lengths in the horizontal slab plane, true along u, and
every row prints G and q = symmetric / G (n/a for the ImageNetV2 pair at or under the threshold): the printed
numbers are the flat twin encoding. Data: the v1 rule paper/figures/charts/fig_source_gap_split.py veri()
(three frozen B2 outputs; sheet lines 1587-1932). Naming: step 4 (one title strip per slab).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
SG = Z.yukle("paper/figures/charts/fig_source_gap_split.py", "v1_source_gap_split")

STEM = "z_source_gap_split"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Source gap split into symmetric and directional parts, one slab per data set. Per seed pair on CIFAR"
           "-10 and CIFAR-100 and per same-recipe pair on ImageNetV2 (descriptive): olive symmetric part, lavend"
           "er-grey directional part, diamond total G. Strips lie in the slab plane; the printed G and share q c"
           "arry the values. A dashed part narrows the gap.")


def main():
    data, foy, okunan = SG.veri()
    vf.reset(STEM, W, 120.0, naming_step=4, naming_kind="serit")
    OX, OY = 4.0, 80.0
    S = Z.Sahne(OX, OY)
    LAB, SCW, VALW = 31.0, 88.0, 27.0
    RD, SM, GAPD = 5.6, 3.2, 5.0
    SD = 3 * RD + 2 * SM
    v0, v1 = -0.10, 0.50
    deg = []
    rows_txt = []
    for s_, (key, path, title, unit) in enumerate(SG.SETS):
        d = data[key]
        dep0 = s_ * (SD + GAPD)
        top = Z.plaka_un(S, f"slab{s_}", *Z.un(S, 0.0, dep0), LAB + SCW + VALW, SD, 1.8, tint="sahne")
        vf.THREE_D[f"slab{s_}"]["rol"] = "veri"

        def pt(v, depth):
            return S.P(*Z.un(S, LAB + (v - v0) / (v1 - v0) * SCW, dep0 + depth), 0.0)
        # zero line, ticks on the front edge, threshold on the ImageNetV2 slab
        vf.seg(f"z{s_}", pt(0.0, 0.6), pt(0.0, SD - 0.6), vf.C["frame"], vf.LW["ince"])
        for t_ in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
            a = pt(t_, 0.0)
            vf.seg(f"tk{s_}_{t_}", a, (a[0], a[1] + 0.9), vf.C["frame"], vf.LW["ince"])
        for t_ in (0.1, 0.2, 0.3, 0.4, 0.5):
            vf.seg(f"gl{s_}_{t_}", pt(t_, 0.6), pt(t_, SD - 0.6), vf.tint_of("izgara")[0], vf.LW["ince"])
        if key == "in":
            vf.seg("thr", pt(d["delta"], 0.6), pt(d["delta"], SD - 0.6), vf.C["muted"], vf.LW["ince"], dash=True)
        for i in range(3):
            depth = SM + i * RD + RD / 2
            sym, dr, G = d["sym"][i], d["dir"][i], d["D"][i]
            hw = 0.75

            def strip(pid, a, b, fill, dash=False):
                p = [pt(a, depth - hw), pt(b, depth - hw), pt(b, depth + hw), pt(a, depth + hw)]
                vf.poly(pid, p + [p[0]], fill=fill, line=Z.soft(fill, 0.35) if not dash else vf.C["ink"],
                        lw=vf.LW["ince"], role="obstacle", group=f"r{s_}_{i}")
            strip(f"sy{s_}_{i}", 0.0, sym, vf.C["vurgu2"])
            if dr >= 0:
                strip(f"dr{s_}_{i}", sym, G, vf.C["vurgu4"])
            else:
                strip(f"dr{s_}_{i}", G, sym, vf.tint_of("ton_4")[0])
                p = [pt(G, depth - hw), pt(sym, depth - hw)]
                vf.seg(f"drd{s_}_{i}", p[0], p[1], vf.C["ink"], vf.LW["ince"], dash=True)
            gp = pt(G, depth)
            Z.isaret(f"g{s_}_{i}", gp[0], gp[1], "D", fill="ink" if key != "in" else None, edge="ink", size=1.9,
                     group=f"r{s_}_{i}")
            lp = S.P(*Z.un(S, LAB - 2.0, dep0 + depth), 0.0)
            T(f"rl{s_}_{i}", lp[0], lp[1] - lh(Z.S8) / 2, [f"pair {i + 1}"], size=Z.S8, align="r",
              color="muted", cont=f"slab{s_}_top")
            qtxt = "q n/a" if i in d["payda_kucuk"] else f"q {d['q'][i]:.2f}"
            gtxt = f"{G:.4f}" if i in d["payda_kucuk"] else f"{G:.3f}"   # 0.0999 is under 0.10
            vp = S.P(*Z.un(S, LAB + SCW + 2.0, dep0 + depth), 0.0)
            T(f"vv{s_}_{i}", vp[0], vp[1] - lh(Z.S8) / 2, [f"G {gtxt}   {qtxt}"], size=Z.S8, cont=f"slab{s_}_top")
            fl = {"D": None, "sym": None, "dir": None, "q": None}
            for nm, fld, jk in (("G", "D", "D"), ("symmetric", "sym", "simetrik_pay"), ("directional", "dir", "yonlu_pay"),
                                ("q", "q", "q")):
                ln = (SG.FOY_LINES[key][0] if key in SG.FOY_LINES else SG.FOY_IN_PAIR[i])
                deg.append(Z.ev(f"{title} {unit} {i + 1} {nm}", d[fld][i], path, f"b2.F_B2.K-a.{jk}[{i}]",
                                f"read as stored; G == sym + dir, q == sym / G (1e-12); near foy line {ln}"))
        tp = S.P(*Z.un(S, 1.5, dep0 + SD / 2), 0.0)
        tt = title.split(", ")[0]
        subs = [unit + "s,", "descriptive"] if key == "in" else [unit + "s"]
        T(f"st{s_}", tp[0], tp[1] - lh(Z.S8) * (1 + len(subs)) / 2, [[(tt, "sb")]] + subs, size=Z.S8,
          cont=f"slab{s_}_top")
    # tick labels under the front slab, legend
    fy = S.P(*Z.un(S, 0.0, 0.0), 0.0)[1] + 1.8
    for t_ in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5):
        x = S.P(*Z.un(S, LAB + (t_ - v0) / (v1 - v0) * SCW, 0.0), 0.0)[0]
        T(f"tl{t_}", x, fy + 0.4, [f"{t_:.1f}"], size=Z.S8, align="c", color="muted")
    T("axl", OX + LAB + SCW / 2, fy + 0.6 + lh(Z.S8), ["log units; ticks on every slab's front edge"], size=Z.S8,
      color="muted", align="c")
    yl = fy + 1.8 + 2 * lh(Z.S8)
    x = 1.0
    for j, (kind_, col, lab) in enumerate((("s", vf.C["vurgu2"], "symmetric part"), ("s", vf.C["vurgu4"], "directional part"),
                                            ("D", vf.C["ink"], "total G"), ("D", None, "descriptive (open)"),
                                            ("-", None, "registered 0.10 threshold"))):
        if kind_ == "-":
            vf.seg(f"lg{j}", (x, yl + lh(Z.S8) / 2), (x + 3.0, yl + lh(Z.S8) / 2), vf.C["muted"], vf.LW["ince"], dash=True)
        else:
            Z.isaret(f"lg{j}", x + 1.2, yl + lh(Z.S8) / 2, kind_, fill=col, edge=col or "ink", size=2.0)
        T(f"lgt{j}", x + 3.6, yl, [lab], size=Z.S8)
        x += 3.6 + Z.tw([lab], Z.S8) + 3.0
    vf.seg("rule", (1.0, yl - 0.5), (W - 1.0, yl - 0.5), vf.C["frame"], vf.LW["vurgu"])
    # review round 2: where "q n/a" comes from (the registered denominator rule, D = G at or below delta)
    T("lgq", 1.0, yl + lh(Z.S8) + 0.4,
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
        manifest={"entities": ents, "sahne_kalibi": "zemin_levhalari",
                  "panel_adlari": [s[2] for s in SG.SETS],
                  "derinlik_ekseni": "data set and registration level: CIFAR-10 in front, the addendum sets behind",
                  "ikiz_kodlama": "every row prints G and q; the strip lengths lie in the horizontal slab plane",
                  "denge_muafiyet": {"3b_veri": "strip lengths lie in the horizontal slab plane, true along the one "
                                                "page-horizontal floor direction, and every row prints G and q (K7)"}},
        denge={"3b_veri": (True, "the strips are lengths in the horizontal slab plane; K7 twin coding: every row "
                                 "prints G and q"),
               "panel_basina_bir_iddia": (True, "each slab is one data set's source-gap split")},
        n_exempt_reason="three pairs per data set, each printed on its own row", okunan_ek=list(okunan))


if __name__ == "__main__":
    sys.exit(main())
