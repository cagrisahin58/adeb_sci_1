#!/usr/bin/env python
"""z_attack_side (Fig. 10 v2, Üslup Z): transfer by attack per source as beads on an abacus.

    python paper/figures_v2/z_attack_side.py [--check] [--bak]

Single column. An upright abacus frame (two posts, top and bottom beams, a base block casting a floor
shadow; every part an upright card of the one dimetric view) carries twelve wires, one per source model,
grouped by cell (R32, V-scr, R224-scr, R224-IN, V-IN). Each permitted attack is a bead on the wire at the
source's full-sample panel-mean log transfer L(m) (T in %): circle PGD-10, square momentum PGD, triangle TGR;
the attack chosen by cross-fitted selection is filled. The value is the bead's position along the wire, read
on the scale of the bottom beam (a length on a flat face; no value in depth). Data: the v1 rule
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
AS = Z.yukle("paper/figures/charts/fig_attack_side.py", "v1_attack_side")

STEM = "z_attack_side"
KIND = "single"
W = vf.page_width(KIND)
ENT = {"r32": ("vurgu5", "R32"), "r224": ("vurgu1", "R224"), "vit": ("vurgu3", "ViT")}
CAPTION = ("Transfer by attack, per source, on an abacus. Each wire is one source; beads sit at its panel-mean log "
           "transfer L(m) under PGD-10 (circle), momentum PGD (square) and, for ViT sources, TGR (triangle). Filled "
           "beads are the attacks chosen by cross-fitted selection; TGR is never chosen. The value is the bead's "
           "position on the beam scale.")


def main():
    d, foy, okunan = AS.veri()
    rows, src, sel = d["rows"], d["src"], d["sel"]
    vf.reset(STEM, W, 110.0, naming_step=1, naming_kind="yok")
    OX = 25.0
    FW = W - OX - 4.0
    PITCH, GG, TB, BB, BASE = 4.7, 1.6, 2.4, 6.0, 2.6
    groups = []
    for m, lab, ck, cell in rows:
        if not groups or groups[-1][0] != lab:
            groups.append((lab, ck, []))
        groups[-1][2].append(m)
    inner = len(rows) * PITCH + (len(groups) - 1) * GG + 5.0
    H = TB + inner + BB
    OY = 8.0 + H + BASE
    S = Z.Sahne(OX, OY)

    def at(off):
        a = off / S.u_page
        return S.u[0] * a, S.u[1] * a
    fr = "govde_panel"
    bx, by = at(-1.2)
    Z.kart(S, "base", bx, by, 0.0, FW + 2.4, BASE, "notr", t=4.0, group="frame")
    DX, DY = S.n[0] * 4.0, S.n[1] * 4.0            # the frame stands on the back edge of the base top
    Z.kart(S, "postL", DX, DY, BASE, 2.2, H, fr, t=3.0, shadow=False, group="frame")
    rx, ry = at(FW - 2.2)
    Z.kart(S, "postR", rx + DX, ry + DY, BASE, 2.2, H, fr, t=3.0, shadow=False, group="frame")
    lx, ly = at(2.2)
    Z.kart(S, "beamT", lx + DX, ly + DY, BASE + H - TB, FW - 4.4, TB, fr, t=2.4, shadow=False, group="frame")
    bxx, byy, bww, bhh = Z.kart(S, "beamB", lx + DX, ly + DY, BASE, FW - 4.4, BB, fr, t=2.4, shadow=False, group="frame")
    pf = S.P(DX, DY, 0.0)
    sx_, sy_ = pf[0] - OX, pf[1] - OY
    x0, x1 = OX + sx_ + 2.2, OX + sx_ + FW - 2.2
    sc = Z.Olcek(2.2, 2.9, x0 + 3.4, x1 - 1.6)
    ytop = OY + sy_ - BASE - H + TB + 1.2
    y = ytop
    placed = []
    for g, (lab, ck, ms) in enumerate(groups):
        yg0 = y
        for m in ms:
            yc = y + PITCH / 2
            vf.seg(f"w_{m}", (x0, yc), (x1, yc), vf.C["frame"], vf.LW["ince"])
            seed = m.rsplit("_s", 1)[-1]
            T(f"sd_{m}", OX - 1.2, yc - lh(Z.S8) / 2, [seed], size=Z.S8, align="r", color="muted")
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
        T(f"cl{g}", OX - 9.6, (yg0 + y) / 2 - lh(Z.S8) / 2, [[(lab, "sb")]], size=Z.S8, align="r")
        y += GG
    # scale on the bottom beam (its face is the container of the labels)
    ys = OY + sy_ - BASE - BB
    for i, v in enumerate((2.2, 2.4, 2.6, 2.8)):
        vf.seg(f"tk{i}", (sc(v), ys), (sc(v), ys + 1.0), vf.C["ink"], vf.LW["ince"])
        T(f"tl{i}", sc(v), ys + 1.5, [f"{v:.1f}"], size=Z.S8, align="c", cont="beamB_face")
    vf.seg("tkb", (sc(2.2), ys + 0.05), (sc(2.9), ys + 0.05), vf.C["ink"], vf.LW["vurgu"])
    # legend and axis name under the base
    yl = OY + 3.4
    T("ax", OX + FW / 2, yl, [[("panel-mean log transfer L(m), T in %", "r")]], size=Z.S8, align="c", color="muted")
    yl += lh(Z.S8) + 0.8
    x = 1.0
    for a, alab, mk, off in AS.ATK:
        Z.isaret(f"lg_{a}", x + 1.0, yl + lh(Z.S8) / 2, mk, fill=None, edge="ink", size=1.9)
        T(f"lgt_{a}", x + 2.4, yl, [alab], size=Z.S8)
        x += 2.4 + Z.tw([alab], Z.S8) + 2.2
    Z.isaret("lg_f", x + 1.0, yl + lh(Z.S8) / 2, "o", fill="ink", edge="ink", size=1.9)
    T("lgt_f", x + 2.4, yl, ["selected"], size=Z.S8)
    yl += lh(Z.S8) + 0.6
    x = 1.0
    for ck, labx in (("r32", "ResNet-18, 32 px"), ("r224", "ResNet-18, 224 px"), ("vit", "ViT-Tiny")):
        Z.isaret(f"sw_{ck}", x + 1.0, yl + lh(Z.S8) / 2, "s", fill=vf.C[ENT[ck][0]], edge=vf.C[ENT[ck][0]], size=2.2)
        T(f"swt_{ck}", x + 2.6, yl, [labx], size=Z.S8)
        x += 2.6 + Z.tw([labx], Z.S8) + 2.2
    yl += lh(Z.S8) + 0.6
    T("tgr", 1.0, yl, [f"TGR chosen for {d['n_tgr']} of {d['n_vit']} ViT sources"], size=Z.S8,
      color="muted")
    Z.sayfa_sigdir()
    deg = []
    for m, a, v, filled in placed:
        deg.append(Z.ev(f"{m} L({a})", v, AS.J5P, f"{AS.YOL[m]}.S_tam.{a}",
                        f"read as stored; == foy line {d['lines'][m]}; bead position on the beam scale"
                        + ("; filled (selected)" if filled else "")))
    deg.append(Z.ev("TGR selected count", d["n_tgr"], "results/C1_REFERANS_FOYU.md:1648", "secildigi kaynak sayisi",
                    "count of ViT sources whose agreeing halves select tgr"))
    deg.append(Z.ev("ViT source count", d["n_vit"], AS.HTP, "modeller.<m>.hucre", "count of V-* sources"))
    ents = {k: "#" + vf.C[v[0]] for k, v in ENT.items()}
    return Z.bitir(
        STEM, message="Per source, the chosen attack is PGD-10 or momentum PGD, never TGR; ViT-scr sources transfer "
                      "least.", kind=KIND, panels=1, caption=CAPTION, sablon="tek_kart_veri", tur="veri",
        degerler=deg, kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan},
        manifest={"entities": ents, "sahne_kalibi": "abakus",
                  "derinlik_ekseni": "none: one frame, the wires lie in one vertical plane; depth is the thickness "
                                     "of posts and base",
                  "ikiz_kodlama": "the value is the bead position along a wire on a flat face, read on the beam scale"},
        denge={"panel_basina_bir_iddia": (True, "one panel: the chosen attack per source"),
               "dogrudan_etiket": (True, "cells and seeds are labelled beside the wires; markers in one legend line")},
        n_exempt_reason="every source is one wire; the twelve sources are listed by seed",
        okunan_ek=[AS.J5P, AS.HTP, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
