#!/usr/bin/env python
"""z_protocol_settings (Fig. 13 v2, Üslup Z): protocol by setting as four exploded protocol boards.

    python paper/figures_v2/z_protocol_settings.py [--check] [--bak]

Single column. Four boards, one per conditioning protocol (1 Unconditioned, 2 Target-correct, 3 Both-correct,
4 Successful-source), are stacked with gaps; each board sits 4.5 mm further back than the one under it, so the
stack reads like half-open drawers and the depth axis is the protocol layer (layer 1 at the back and top). The
boards plug into an upright spine at the right whose face prints the spread per setting. Each board's front
face (an upright card face of the one dimetric view) carries the four settings as 2D dot-interval rows: mean
(filled) +- SD (line) and the seed pairs (small open circles); SVHN shows its two pairs joined by a thin line,
no mean. Values are positions on flat faces; every board has its own ticks, numbers sit on the bottom board.
Data: the v1 rule paper/figures/charts/fig_protocol_settings.py veri() (four transfer summaries cited at sheet
line 153, table lines 159-165). Naming: step 3 (rings 1-4 give the layer order).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
PS = Z.yukle("paper/figures/charts/fig_protocol_settings.py", "v1_protocol_settings")

STEM = "z_protocol_settings"
KIND = "single"
W = vf.page_width(KIND)
MK = {"raw": ("o", "isi_2"), "target_correct": ("^", "isi_3"), "both_correct": ("s", "isi_4"),
      "successful_source": ("D", "isi_5")}
SHORT = {"C10_Linf": "C10 L∞", "C100_Linf": "C100 L∞", "SVHN_Linf": "SVHN L∞", "C10_L2": "C10 L2"}
CAPTION = ("Protocol by setting as four exploded boards. Transfer asymmetry (CNN to ViT minus ViT to CNN): "
           "boards 1-4 are the conditioning protocols, set back layer by layer; rows are settings, mean±SD over "
           "three seed pairs, pairs as small circles (SVHN two, no mean). Values are positions on each board's "
           "flat face; the spine prints the spread.")


def main():
    D, foy = PS.veri()
    vf.reset(STEM, W, 140.0, naming_step=3, naming_kind="rakam")
    OX, OY = 1.5, 100.0
    S = Z.Sahne(OX, OY)
    BW, RH, GAP, DSTEP, TB = 57.0, Z.lh(Z.S8) + 0.1, 3.4, 4.5, 4.0
    FH = 1.0 + lh(Z.S8) + 4 * RH + 1.2
    SPW = 15.6
    v0, v1 = -2.0, 21.5
    deg = []
    sets = [s[0] for s in PS.SETTINGS]
    nb = len(PS.PROTOCOLS)
    # the spine: an upright card at the right, as deep as the whole stack
    sx0 = OX + BW + 5.4
    Hs = nb * FH + (nb - 1) * GAP + 2.0
    X, Y = Z.un(S, sx0 - OX, 0.0)
    fxs, fys, fws, fhs = Z.kart(S, "spine", X, Y, 0.0, SPW, Hs, "govde_panel", t=11.0, k=(0.03, 0.02),
                                group="spine")
    T("sp_t", fxs + fws / 2, fys + 1.4, [[("spread", "sb")]], size=Z.S8, align="c", cont="spine_face")
    T("sp_u", fxs + fws / 2, fys + 1.4 + lh(Z.S8), ["(pts)"], size=Z.S8, align="c", color="muted", cont="spine_face")
    for j, s in enumerate(sets):
        y = fys + 4.0 + 2 * lh(Z.S8) + j * 2 * (lh(Z.S8) + 0.4)
        T(f"sp_n{j}", fxs + fws / 2, y, [SHORT[s]], size=Z.S8, align="c", color="muted", cont="spine_face")
        lab = D[s]["spread_lab"].replace(" / ", "/")
        T(f"sp_v{j}", fxs + fws / 2, y + lh(Z.S8), [lab], size=Z.S8, align="c", cont="spine_face")
        for i, v in enumerate(D[s]["spread"]):
            deg.append(Z.ev(f"{SHORT[s]} spread pair {i + 1}", v, D[s]["path"], f"protocol_spread_pp.values[{i}]",
                            "max - min over the four protocols; == foy line 163"))
    for k in range(nb - 1, -1, -1):          # back (k = 0, top) drawn first
        p, plong, ent, pshort = PS.PROTOCOLS[k]
        dep = (nb - 1 - k) * DSTEP + 1.0
        zb = (nb - 1 - k) * (FH + GAP) + 2.0
        X, Y = Z.un(S, 0.0, dep)
        fx, fy, fw, fh = Z.kart(S, f"bd{k}", X, Y, zb, BW, FH, "kutu", t=TB, shadow=False, group=f"bd{k}")
        face = f"bd{k}_face"
        bl_ring = Z.bl.ring(f"st{k + 1}", gr(fx + 1.0), gr(fy + 0.7), k + 1, container=face)
        d_ = vf.IDS[f"st{k + 1}"]["w"]
        T(f"pn{k}", fx + 1.6 + d_, fy + 0.7 + (d_ - lh(Z.S8)) / 2, [[(pshort, "sb")]], size=Z.S8, cont=face)
        mk, tint = MK[p]
        col = vf.tint_of(tint)[0]
        px0, px1 = fx + 15.0, fx + fw - 1.5
        sc = Z.Olcek(v0, v1, px0, px1)
        ytop = fy + 1.0 + lh(Z.S8)
        for t_ in (0, 5, 10, 15, 20):
            vf.seg(f"g{k}_{t_}", (sc(t_), ytop + 0.6), (sc(t_), fy + fh - 0.6), vf.C["izgara"] if "izgara" in vf.C
                   else vf.tint_of("izgara")[0], vf.LW["ince"], dash=(t_ == 0))
        for j, s in enumerate(sets):
            yc = ytop + j * RH + RH / 2 + 0.3
            T(f"rl{k}_{j}", px0 - 1.4, yc - lh(Z.S8) / 2, [SHORT[s]], size=Z.S8, align="r", color="muted", cont=face)
            row = D[s]["rows"][p]
            path = D[s]["path"]
            if row["mean"] is not None:
                vf.seg(f"sd{k}_{j}", (sc(row["mean"] - row["sd"]), yc), (sc(row["mean"] + row["sd"]), yc), vf.C["ink"],
                       vf.LW["ince"])
                for i, v in enumerate(row["values"]):
                    Z.isaret(f"pr{k}_{j}_{i}", sc(v), yc - 1.25, "o", fill=None, edge="ink", size=0.95,
                             group=f"row{k}_{j}")
                Z.isaret(f"mn{k}_{j}", sc(row["mean"]), yc, mk, fill=col, edge=Z.soft(col, 0.4), size=2.0,
                         group=f"row{k}_{j}")
                deg.append(Z.ev(f"{SHORT[s]} {pshort} mean", row["mean"], path, f"protocols.{p}.diff.values",
                                f"mean; == foy line {PS.FOY_ROW[p]} (2 dp)"))
                deg.append(Z.ev(f"{SHORT[s]} {pshort} SD", row["sd"], path, f"protocols.{p}.diff.values",
                                f"SD ddof=1; == foy line {PS.FOY_ROW[p]} (2 dp)"))
            else:
                xs_ = [sc(v) for v in row["values"]]
                vf.seg(f"sv{k}_{j}", (min(xs_), yc), (max(xs_), yc), vf.C["ink"], vf.LW["ince"])
                for i, x in enumerate(xs_):
                    Z.isaret(f"pv{k}_{j}_{i}", x, yc, mk, fill=col, edge=Z.soft(col, 0.4), size=1.8, group=f"row{k}_{j}")
            for i, v in enumerate(row["values"]):
                deg.append(Z.ev(f"{SHORT[s]} {pshort} pair {i + 1}", v, path, f"protocols.{p}.diff.values[{i}]",
                                f"read as stored; == foy line {PS.FOY_ROW[p]} (2 dp); position"))
        if k == nb - 1:
            Z.kot("ax", px0, px1, fy + fh + 0.3, sc, [0, 5, 10, 15, 20], ["0", "5", "10", "15", "20"])
            T("axl", (px0 + px1) / 2, fy + fh + 1.8 + lh(Z.S8), ["CNN to ViT minus ViT to CNN (pts)"], size=Z.S8,
              color="muted", align="c")
            ylg = fy + fh + 2.4 + 2 * lh(Z.S8)
    x = 1.0
    for j, (mk_, lab) in enumerate((("o", "seed pair"), ("-", "± SD"), ("p", "SVHN: two pairs, no mean"))):
        if mk_ == "o":
            Z.isaret(f"lg{j}", x + 1.0, ylg + lh(Z.S8) / 2, "o", fill=None, edge="ink", size=0.95)
        elif mk_ == "-":
            vf.seg(f"lg{j}", (x, ylg + lh(Z.S8) / 2), (x + 2.4, ylg + lh(Z.S8) / 2), vf.C["ink"], vf.LW["ince"])
        else:
            vf.seg(f"lg{j}", (x, ylg + lh(Z.S8) / 2), (x + 2.4, ylg + lh(Z.S8) / 2), vf.C["ink"], vf.LW["ince"])
        T(f"lgt{j}", x + 3.0, ylg, [lab], size=Z.S8)
        x += 3.0 + Z.tw([lab], Z.S8) + 2.4
    vf.seg("rule", (OX, ylg - 0.4), (OX + BW, ylg - 0.4), vf.C["frame"], vf.LW["vurgu"])
    Z.sayfa_sigdir()
    ents = {PS.PROTOCOLS[i][3]: "#" + vf.tint_of(MK[PS.PROTOCOLS[i][0]][1])[0] for i in range(nb)}
    return Z.bitir(
        STEM, message="The transfer asymmetry of one pair depends on the conditioning protocol in every setting; the "
                      "spread over the four protocols is printed per setting.", kind=KIND, panels=4, caption=CAPTION,
        sablon="ortak_satirli_katlar", tur="veri", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy},
        manifest={"entities": ents, "sahne_kalibi": "patlatilmis_levha",
                  "istasyonlar": [f"{i + 1} {PS.PROTOCOLS[i][3]}" for i in range(nb)],
                  "derinlik_ekseni": "protocol layer: layer 1 at the back and top, layer 4 in front",
                  "ikiz_kodlama": "values are positions on the flat front faces of the boards"},
        denge={"panel_basina_bir_iddia": (True, "each board is one protocol across the four settings")},
        n_exempt_reason="three seed pairs per setting (SVHN two) are drawn as single marks",
        okunan_ek=[s[2] for s in PS.SETTINGS] + ["results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
