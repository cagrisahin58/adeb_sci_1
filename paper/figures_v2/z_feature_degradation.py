#!/usr/bin/env python
"""z_feature_degradation (Fig. 17 v2, Üslup Z): ViT-Tiny's twelve blocks as a spine with per-block readouts.

    python paper/figures_v2/z_feature_degradation.py [--check] [--bak]

Single column. At the left the twelve blocks of ViT-Tiny are thin discs stacked upward (block 1 at the bottom),
each numbered on its face; a labelled arrow brings the clean and PGD-10 image in at the base, a second one
leads from the spine to three upright readout cards whose rows sit level with the discs: change of the CLS
attention entropy (runs open, mean filled, run-level 90 % TOST interval, the registered +-0.05 nat margin as a
band), CLS attention displacement (TV; runs, mean +- SD) and block-output cosine (CLS token, patch-token mean,
all tokens; mean +- SD). The layer axis is the spine's height; values are positions on flat card faces.
Data: the v1 rule paper/figures/charts/fig_feature_degradation.py veri() (results/c1_c4 summaries and TOST
file, sheet lines 292-303, 334-345, 1113). Naming: step 2 (labelled flow arrows).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
FD = Z.yukle("paper/figures/charts/fig_feature_degradation.py", "v1_feature_degradation")

STEM = "z_feature_degradation"
KIND = "single"
W = vf.page_width(KIND)
COSLOOK = {"cos_block_cls": ("o", "vurgu3", "CLS token"), "cos_block_token_mean": ("s", "vurgu1", "patch mean"),
           "cos_block_output": ("^", "vurgu2", "all tokens")}
CAPTION = ("Feature degradation of ViT-Tiny under attack, block by block. The clean and PGD-10 image enter the "
           "spine, block 1 at the bottom; per block over three runs: CLS attention entropy change with 90% TOST "
           "intervals inside the ±0.05-nat band, attention displacement (TV), block-output cosine, mean±SD. "
           "Values are positions on the flat cards.")


def main():
    o, inputs, foy = FD.veri()
    NL = FD.NL
    vf.reset(STEM, W, 140.0, naming_step=2, naming_kind="akis")
    RH, DH = 4.6, 3.4
    OY = 9.0 + 2 * lh(Z.S8) + NL * RH + 2.0
    S = Z.Sahne(1.8, OY)
    zb0 = 6.0
    deg = []
    # the spine
    X, Y = Z.un(S, -0.5, 0.0)
    Z.kart(S, "base", X, Y, 0.0, 9.6, zb0 - 1.0, "govde_res", t=6.0, k=(0.04, 0.03), group="spine")
    rowy = {}
    for k in range(NL):
        z = zb0 + k * RH
        X, Y = Z.un(S, 1.0, 1.5)
        fx, fy, fw, fh = Z.kart(S, f"b{k}", X, Y, z, 8.0, DH, "govde_vit", t=4.0, shadow=False, group=f"b{k}")
        rowy[k] = fy + fh / 2
    yb = OY - 2.0
    T("inlab", 16.0, OY + 0.6, [[("clean x and PGD-10 x′", "r")]], size=Z.S8, color="muted")
    vf.seg("inarr", (15.4, OY + 0.6 + lh(Z.S8) / 2), (9.0, OY - zb0 + 2.0), vf.C["arrow"], vf.LW["ince"], arrow=True)
    # three readout cards
    cx0 = 20.6
    cw = (W - cx0 - 1.6 - 2 * 1.4) / 3
    cards = [("Entropy Δ", "nat", (-0.06, 0.06), (-0.05, 0.05), ("−0.05", "0.05")),
             ("TV", "shift", (0.0, 0.1), (0.0, 0.05, 0.1), ("0", "0.05", "0.1")),
             ("Cosine", "block output", (0.955, 1.0), (0.96, 1.0), ("0.96", "1"))]
    ctop = rowy[NL - 1] - RH / 2 - 2 * lh(Z.S8) - 1.4
    cbot = rowy[0] + RH / 2 + 6.2
    for c, (title, sub, (v0, v1), ticks, tlabs) in enumerate(cards):
        X, Y = Z.un(S, cx0 - 2.0 + c * (cw + 1.4), 0.0)
        fx, fy, fw, fh = Z.kart(S, f"c{c}", X, Y, OY - cbot, cw, cbot - ctop, "kutu", t=1.4, shadow=False,
                                group=f"c{c}")
        face = f"c{c}_face"
        T(f"ct{c}", fx + fw / 2, fy + 0.6, [[(title, "sb")]], size=Z.S8, align="c", cont=face)
        T(f"cs{c}", fx + fw / 2, fy + 0.6 + lh(Z.S8), [sub], size=Z.S8, align="c", color="muted", cont=face)
        x0, x1 = fx + (5.2 if c == 0 else 3.9), fx + fw - 3.3
        sc = Z.Olcek(v0, v1, x0, x1)
        if c == 0:
            band = [(sc(-0.05), rowy[NL - 1] - RH / 2), (sc(0.05), rowy[NL - 1] - RH / 2), (sc(0.05), rowy[0] + RH / 2),
                    (sc(-0.05), rowy[0] + RH / 2)]
            vf.poly("band", band + [band[0]], fill=vf.tint_of("ton_4")[0], line=None, role="deco", container=face)
            vf.seg("zero", (sc(0.0), rowy[NL - 1] - RH / 2), (sc(0.0), rowy[0] + RH / 2), vf.C["frame"], vf.LW["ince"],
                   dash=True)
        for k in range(NL):
            y = rowy[k]
            if c == 0:
                d = o["dlt"][k]
                g = o["ga90"][k]
                vf.seg(f"ga{k}", (sc(g[0]), y), (sc(g[1]), y), vf.C["ink"], vf.LW["vurgu"])
                for j, v in enumerate(d["runs"]):
                    Z.isaret(f"er{k}_{j}", sc(v), y - 1.3, "o", fill=None, edge="ink", size=0.85, group=f"e{k}")
                Z.isaret(f"em{k}", sc(d["mean"]), y, "o", fill=vf.C["vurgu3"], edge=Z.soft(vf.C["vurgu3"], 0.4),
                         size=1.6, group=f"e{k}")
                deg.append(Z.ev(f"layer {k + 1} entropy change mean", d["mean"], FD.p_(1), "vit.attention.entropy_delta_mean",
                                f"mean over pair1-3 files; == foy line {334 + k} (4 dp)"))
                for j, v in enumerate(d["runs"]):
                    deg.append(Z.ev(f"layer {k + 1} entropy change run {j + 1}", v, FD.p_(j + 1),
                                    f"vit.attention.entropy_delta_mean[{k}]", "read as stored"))
                deg.append(Z.ev(f"layer {k + 1} GA90 low", g[0], FD.TOST, f"entropi_TOST.katmanlar[{k}].GA90[0]", "read"))
                deg.append(Z.ev(f"layer {k + 1} GA90 high", g[1], FD.TOST, f"entropi_TOST.katmanlar[{k}].GA90[1]", "read"))
            elif c == 1:
                d = o["tv"][k]
                vf.seg(f"tvs{k}", (sc(d["mean"] - d["sd"]), y), (sc(d["mean"] + d["sd"]), y), vf.C["ink"], vf.LW["ince"])
                for j, v in enumerate(d["runs"]):
                    Z.isaret(f"tr{k}_{j}", sc(v), y - 1.3, "o", fill=None, edge="ink", size=0.85, group=f"t{k}")
                Z.isaret(f"tm{k}", sc(d["mean"]), y, "s", fill=vf.C["vurgu3"], edge=Z.soft(vf.C["vurgu3"], 0.4), size=1.6,
                         group=f"t{k}")
                deg.append(Z.ev(f"layer {k + 1} TV mean", d["mean"], FD.p_(1), "vit.attention.displacement_mean",
                                f"mean over pair1-3; == foy line {334 + k} (4 dp)"))
                deg.append(Z.ev(f"layer {k + 1} TV SD", d["sd"], FD.p_(1), "vit.attention.displacement_mean",
                                f"SD over pair1-3; == foy line {334 + k} (4 dp)"))
            else:
                offs = {"cos_block_cls": -1.1, "cos_block_token_mean": 0.0, "cos_block_output": 1.1}
                for key, (mk, ck, lab) in COSLOOK.items():
                    d = o["cos"][key][k]
                    yy = y + offs[key]
                    vf.seg(f"cs_{key}{k}", (sc(d["mean"] - d["sd"]), yy), (sc(d["mean"] + d["sd"]), yy), vf.C[ck],
                           vf.LW["ince"])
                    Z.isaret(f"cm_{key}{k}", sc(d["mean"]), yy, mk, fill=vf.C[ck], edge=Z.soft(vf.C[ck], 0.4), size=1.3,
                             group=f"cos{k}")
                    deg.append(Z.ev(f"block {k + 1} {key} mean", d["mean"], FD.p_(1), f"vit.{key}.block{k}.mean",
                                    f"mean over pair1-3; == foy line {292 + k} (4 dp)"))
                    deg.append(Z.ev(f"block {k + 1} {key} SD", d["sd"], FD.p_(1), f"vit.{key}.block{k}.mean",
                                    f"SD over pair1-3; == foy line {292 + k} (4 dp)"))
        Z.kot(f"ax{c}", x0, x1, rowy[0] + RH / 2 + 0.4, sc, list(ticks), list(tlabs), cont=face)
    # second flow arrow: spine -> readouts, and row guides
    ya = ctop - 2.6
    top_sp = rowy[NL - 1] - DH / 2 - 3.6
    T("rolab", cx0 + 3.0, ya - lh(Z.S8) - 0.4, [[("per-block readouts, 3 runs", "r")]], size=Z.S8, color="muted")

    vf.note_naming("inarr", "flow")
    for k in range(NL):
        c0x = S.P(*Z.un(S, cx0 - 2.0, 0.0), 0.0)[0]
        T(f"bn{k}", c0x + 0.8, rowy[k] - lh(Z.S8) / 2, [f"{k + 1}"], size=Z.S8, color="muted", cont="c0_face")
        vf.seg(f"ro{k}", (12.6, rowy[k]), (c0x - 0.5, rowy[k]), vf.C["arrow"], vf.LW["ince"], arrow=True)
        vf.note_naming(f"ro{k}", "flow")
    # legend
    yl = OY + 1.2 + lh(Z.S8)
    x = 1.0
    items = [("o", None, "ink", "run"), ("o", "vurgu3", None, "mean"), ("-", None, None, "90% TOST or SD")]
    for j, (mk, f_, e_, lab) in enumerate(items):
        if mk == "-":
            vf.seg(f"lg{j}", (x, yl + lh(Z.S8) / 2), (x + 2.4, yl + lh(Z.S8) / 2), vf.C["ink"], vf.LW["vurgu"])
        else:
            Z.isaret(f"lg{j}", x + 1.0, yl + lh(Z.S8) / 2, mk, fill=vf.C[f_] if f_ else None, edge=e_ or vf.C["vurgu3"],
                     size=1.4 if f_ else 0.9)
        T(f"lgt{j}", x + 3.0, yl, [lab], size=Z.S8)
        x += 3.0 + Z.tw([lab], Z.S8) + 2.0
    yl += lh(Z.S8) + 0.3
    x = 1.0
    for key, (mk, ck, lab) in COSLOOK.items():
        Z.isaret(f"lc_{key}", x + 1.0, yl + lh(Z.S8) / 2, mk, fill=vf.C[ck], edge=Z.soft(vf.C[ck], 0.4), size=1.5)
        T(f"lct_{key}", x + 2.6, yl, [lab], size=Z.S8)
        x += 2.6 + Z.tw([lab], Z.S8) + 2.0
    T("lcband", x, yl, ["band ±0.05 nat"], size=Z.S8, color="muted")
    Z.sayfa_sigdir()
    deg.append(Z.ev("TOST margin", o["marj"], FD.TOST, "entropi_TOST.marj_nat", "read; == foy line 1113"))
    ents = {"vit": "#" + vf.C["vurgu3"]}
    return Z.bitir(
        STEM, message="Under its own attack ViT-Tiny's CLS attention entropy stays inside the registered margin in "
                      "every block while attention displacement grows and block-output cosine falls with depth.",
        kind=KIND, panels=3, caption=CAPTION, sablon="ortak_satirli_katlar", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "girdiler": inputs},
        manifest={"entities": ents, "sahne_kalibi": "omurga",
                  "panel_adlari": [c[0] for c in cards],
                  "derinlik_ekseni": "none in depth: the layer axis is the spine's height; depth is disc thickness",
                  "ikiz_kodlama": "values are positions on the flat faces of the three readout cards"},
        denge={"panel_basina_bir_iddia": (True, "each readout card is one measure across the twelve blocks"),
               "dogrudan_etiket": (True, "blocks are numbered on their faces; measures name the cards")},
        n_exempt_reason="three runs per block; the legend says so", okunan_ek=inputs + ["results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
