#!/usr/bin/env python
"""z_protocol_settings (Fig. 13 v2, Üslup Z): protocol by setting on four flat protocol cards.

    python paper/figures_v2/z_protocol_settings.py [--check] [--bak]

Single column, flat-card composition (third round, 09.11.2026: the exploded boards and the spine block are gone).
Four flat cards, one per conditioning protocol (1 Unconditioned, 2 Target-correct, 3 Both-correct,
4 Successful-source), are stacked on one left edge, layer 1 at the top; a flat narrow card at the right prints
the spread per setting. Each card carries the four settings as 2D dot-interval rows: mean
(filled) +- SD (line) and the seed pairs (small open circles); SVHN shows its two pairs joined by a thin line,
no mean. Every card has its own gridlines on one shared scale; tick numbers sit under the bottom card.
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
Z.duz()
PS = Z.yukle("paper/figures/charts/fig_protocol_settings.py", "v1_protocol_settings")

STEM = "z_protocol_settings"
KIND = "single"
W = vf.page_width(KIND)
MK = {"raw": ("o", "isi_2"), "target_correct": ("^", "isi_3"), "both_correct": ("s", "isi_4"),
      "successful_source": ("D", "isi_5")}
SHORT = {"C10_Linf": "C10 L∞", "C100_Linf": "C100 L∞", "SVHN_Linf": "SVHN L∞", "C10_L2": "C10 L2"}
CAPTION = ("Protocol by setting. Transfer asymmetry (CNN to ViT minus ViT to CNN) on one shared scale: panels 1-4 "
           "are the conditioning protocols; rows are settings, mean±SD over three seed pairs, pairs as small "
           "circles (SVHN two, no mean). The narrow panel at the right prints the spread over the four protocols.")


def main():
    D, foy = PS.veri()
    vf.reset(STEM, W, 140.0, naming_step=3, naming_kind="rakam")
    # third round (09.11.2026): four flat protocol cards stacked on one left edge (layer 1 at the top), the
    # spread as one flat narrow card at the right spanning the stack; no exploded boards, no spine block
    OX = 1.0
    SPW = 15.6
    BW, RH, GAP = W - 2 * OX - SPW - 2.0, Z.lh(Z.S8) + 0.1, 2.0
    FH = 1.0 + lh(Z.S8) + 4 * RH + 1.2
    v0, v1 = -2.0, 21.5
    deg = []
    sets = [s[0] for s in PS.SETTINGS]
    nb = len(PS.PROTOCOLS)
    # the spread card: flat, at the right, as tall as the stack
    sx0 = OX + BW + 2.0
    Hs = nb * FH + (nb - 1) * GAP
    fxs, fys, fws, fhs = Z.duz_kart("spine", sx0, 1.0, SPW, Hs, "govde_panel")
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
    for k in range(nb):                      # layer 1 at the top
        p, plong, ent, pshort = PS.PROTOCOLS[k]
        fx, fy, fw, fh = Z.duz_kart(f"bd{k}", OX, 1.0 + k * (FH + GAP), BW, FH, "kutu")
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
        manifest={"entities": ents, "sahne_kalibi": "yok (dort duz protokol karti, ucuncu tur)",
                  "istasyonlar": [f"{i + 1} {PS.PROTOCOLS[i][3]}" for i in range(nb)],
                  "derinlik_ekseni": "none: flat cards, layer 1 at the top"},
        denge={"panel_basina_bir_iddia": (True, "each card is one protocol across the four settings")},
        n_exempt_reason="three seed pairs per setting (SVHN two) are drawn as single marks",
        okunan_ek=[s[2] for s in PS.SETTINGS] + ["results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
