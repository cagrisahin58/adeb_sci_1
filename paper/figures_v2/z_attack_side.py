#!/usr/bin/env python
"""z_attack_side (Fig. 10 v2, Üslup Z): transfer by attack per source on one flat card.

    python paper/figures_v2/z_attack_side.py [--check] [--bak]

Single column, flat-card composition (third round, 09.11.2026: the abacus frame, posts, beams and base are
gone). One flat card holds twelve thin rows, one per source model, grouped by cell (R32, V-scr, R224-scr,
R224-IN, V-IN; alternate cells on a light tone band). Each permitted attack is a mark on the row at the source's
full-sample panel-mean log transfer L(m) (T in %): circle PGD-10, square momentum PGD, triangle TGR; the attack
chosen by cross-fitted selection is filled. The value is the mark's x position, read on the base line under
the rows. Data: the v1 rule
paper/figures/charts/fig_attack_side.py veri() (results/q1/konsey_ayrisim_b5.json and the frozen cell table,
every S_tam checked against results/C1_REFERANS_FOYU.md lines 1635-1646, TGR count line 1648).
Naming: step 1 (one panel; the cell names are axis labels).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
AS = Z.yukle("paper/figures/charts/fig_attack_side.py", "v1_attack_side")

STEM = "z_attack_side"
KIND = "single"
W = vf.page_width(KIND)
ENT = {"r32": ("vurgu5", "R32"), "r224": ("vurgu1", "R224"), "vit": ("vurgu3", "ViT")}
CAPTION = ("Transfer by attack, per source. Each row is one source model, grouped by cell; marks sit at its "
           "panel-mean log transfer L(m) under PGD-10 (circle), momentum PGD (square) and, for ViT sources, TGR "
           "(triangle). Filled marks are the attacks chosen by cross-fitted selection; TGR is never chosen.")


def main():
    d, foy, okunan = AS.veri()
    rows, src, sel = d["rows"], d["src"], d["sel"]
    vf.reset(STEM, W, 110.0, naming_step=1, naming_kind="yok")
    # third round (09.11.2026): one flat card, no abacus frame, posts, beams or base. Every source is a thin row
    # line; the cells alternate a light tone band (grouping inside the card); the scale is a base line (kot)
    # under the rows.
    PITCH, GG = 4.7, 1.6
    LH = lh(Z.S8)
    groups = []
    for m, lab, ck, cell in rows:
        if not groups or groups[-1][0] != lab:
            groups.append((lab, ck, []))
        groups[-1][2].append(m)
    inner = len(rows) * PITCH + (len(groups) - 1) * GG
    CX, CY = 1.0, 1.0
    CW = W - 2.0
    XSEED = CX + 23.2                              # right edge of the seed labels
    x0, x1 = CX + 24.8, CX + CW - 1.4
    sc = Z.Olcek(2.2, 2.9, x0 + 3.4, x1 - 1.6)
    ytop = CY + 1.4
    yax = ytop + inner + 1.6
    CH = (yax + 1.4 + LH + 0.4 + LH + 1.0) - CY
    Z.duz_kart("card", CX, CY, CW, CH, "kutu")
    face = "card_face"
    y = ytop
    placed = []
    for g, (lab, ck, ms) in enumerate(groups):
        yg0 = y
        hgt = len(ms) * PITCH
        if g % 2 == 0:                             # alternate light band per cell
            bb = [(x0 - 0.6, yg0 - 0.4), (x1 + 0.6, yg0 - 0.4), (x1 + 0.6, yg0 + hgt + 0.4), (x0 - 0.6, yg0 + hgt + 0.4)]
            vf.poly(f"band{g}", bb + [bb[0]], fill=vf.tint_of("ton_6")[0], line=None, role="deco", container=face)
        for m in ms:
            yc = y + PITCH / 2
            vf.seg(f"w_{m}", (x0, yc), (x1, yc), vf.tint_of("izgara")[0], vf.LW["ince"])
            seed = m.rsplit("_s", 1)[-1]
            T(f"sd_{m}", XSEED, yc - LH / 2, [seed], size=Z.S8, align="r", color="muted", cont=face)
            col = vf.C[ENT[ck][0]]
            for a, alab, mk, off in AS.ATK:
                if a not in src[m]["S_tam"]:
                    continue
                v = src[m]["S_tam"][a]
                filled = sel[m] == a
                Z.isaret(f"b_{m}_{a}", sc(v), yc + (-1.2 if a == "pgd" else 1.2), mk, fill=col if filled else None, edge=col, size=1.9,
                         group=f"row_{m}")
                placed.append((m, a, v, filled))
            y += PITCH
        T(f"cl{g}", XSEED - 8.6, (yg0 + y) / 2 - LH / 2, [[(lab, "sb")]], size=Z.S8, align="r", cont=face)
        y += GG
    # the scale: a base line with ticks under the rows, labels and the axis name inside the card
    Z.kot("tkb", sc(2.2), sc(2.9), yax, sc, [2.2, 2.4, 2.6, 2.8], labels=[f"{v:.1f}" for v in (2.2, 2.4, 2.6, 2.8)],
          cont=face, lw=vf.LW["vurgu"], color="ink")
    T("ax", (sc(2.2) + sc(2.9)) / 2, yax + 1.4 + LH + 0.4, [[("panel-mean log transfer L(m), T in %", "r")]], size=Z.S8,
      align="c", color="muted", cont=face)
    # legend under the card
    yl = CY + CH + 1.6
    x = 1.0
    for a, alab, mk, off in AS.ATK:
        Z.isaret(f"lg_{a}", x + 1.0, yl + LH / 2, mk, fill=None, edge="ink", size=1.9)
        T(f"lgt_{a}", x + 2.4, yl, [alab], size=Z.S8)
        x += 2.4 + Z.tw([alab], Z.S8) + 2.2
    Z.isaret("lg_f", x + 1.0, yl + LH / 2, "o", fill="ink", edge="ink", size=1.9)
    T("lgt_f", x + 2.4, yl, ["selected"], size=Z.S8)
    yl += LH + 0.6
    x = 1.0
    for ck, labx in (("r32", "ResNet-18, 32 px"), ("r224", "ResNet-18, 224 px"), ("vit", "ViT-Tiny")):
        Z.isaret(f"sw_{ck}", x + 1.0, yl + LH / 2, "s", fill=vf.C[ENT[ck][0]], edge=vf.C[ENT[ck][0]], size=2.2)
        T(f"swt_{ck}", x + 2.6, yl, [labx], size=Z.S8)
        x += 2.6 + Z.tw([labx], Z.S8) + 2.2
    yl += LH + 0.6
    T("tgr", 1.0, yl, [f"TGR chosen for {d['n_tgr']} of {d['n_vit']} ViT sources"], size=Z.S8,
      color="muted")
    Z.sayfa_sigdir()
    deg = []
    for m, a, v, filled in placed:
        deg.append(Z.ev(f"{m} L({a})", v, AS.J5P, f"{AS.YOL[m]}.S_tam.{a}",
                        f"read as stored; == foy line {d['lines'][m]}; mark x position on the base-line scale"
                        + ("; filled (selected)" if filled else "")))
    deg.append(Z.ev("TGR selected count", d["n_tgr"], "results/C1_REFERANS_FOYU.md:1648", "secildigi kaynak sayisi",
                    "count of ViT sources whose agreeing halves select tgr"))
    deg.append(Z.ev("ViT source count", d["n_vit"], AS.HTP, "modeller.<m>.hucre", "count of V-* sources"))
    ents = {k: "#" + vf.C[v[0]] for k, v in ENT.items()}
    return Z.bitir(
        STEM, message="Per source, the chosen attack is PGD-10 or momentum PGD, never TGR; ViT-scr sources transfer "
                      "least.", kind=KIND, panels=1, caption=CAPTION, sablon="tek_kart_veri", tur="veri",
        degerler=deg, kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan},
        manifest={"entities": ents, "sahne_kalibi": "yok (tek duz kart, ucuncu tur)",
                  "derinlik_ekseni": "none: one flat card"},
        denge={"panel_basina_bir_iddia": (True, "one panel: the chosen attack per source"),
               "dogrudan_etiket": (True, "cells and seeds are labelled beside the rows; markers in one legend line")},
        n_exempt_reason="every source is one row; the twelve sources are listed by seed",
        okunan_ek=[AS.J5P, AS.HTP, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
