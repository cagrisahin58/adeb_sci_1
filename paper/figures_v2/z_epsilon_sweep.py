#!/usr/bin/env python
"""z_epsilon_sweep (Fig. 16 v2, Üslup Z): robust accuracy under PGD-10 as three eroded terraces.

    python paper/figures_v2/z_epsilon_sweep.py [--check] [--bak]

Single column (85.29 mm). Each model is one terrace of five sand blocks standing on the floor in the one
dimetric 36 degree view: the width axis runs over the budget (clean, 2/255, 4/255, 8/255, 16/255), the depth
axis orders the models from the least to the most robust (ViT-Tiny AT in front, ResNet-18 AT, WRN-28-10 at the
back), so no terrace hides a taller one. Block height is the accuracy on the vertical axis, a true length in
this view (0.4 mm per point); K7: the same value is printed in the number rows under the scene (the flat twin
encoding that carries every value). Data: the v1 rule paper/figures/charts/fig_epsilon_sweep.py veri() is
imported read-only (C1 sweep CSVs, three seed pairs, mean and SD; the WRN file is the sheet's own cited
source, lines 354-364), every mean is checked against results/C1_REFERANS_FOYU.md lines 360-364.
Naming: step 1 (one panel, no name).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
sys.argv += ["--uslup", "Z"]
ES = Z.yukle("paper/figures/charts/fig_epsilon_sweep.py", "v1_epsilon_sweep")
sys.argv = sys.argv[:-2]

STEM = "z_epsilon_sweep"
KIND = "single"
W = vf.page_width(KIND)
HS = 0.40          # mm per accuracy point on the vertical axis (true length)
BW, BD, GAP = 8.6, 6.0, 3.2
ROWS = [("vit_tiny", "govde_vit", "^", "ViT-Tiny AT"), ("resnet18", "govde_r32", "s", "ResNet-18 AT"),
        ("wrn", "govde_panel", "v", "WRN-28-10")]
CAPTION = ("Robust accuracy under PGD-10 as cut-out profiles. Each card's top edge traces CIFAR-10 test accuracy "
           "over the budget ε, clean to 16/255, as height above its own base (back bases dashed; scale bar 25 points); "
           "the number rows print the same values, which carry the result (mean of three seed pairs; WRN-28-10 is one "
           "RobustBench model).")


def main():
    data, inputs, foy = ES.veri()
    vf.reset(STEM, W, 96.0, naming_step=1, naming_kind="yok")
    OX, OY = 6.0, 60.0
    S = Z.Sahne(OX, OY)
    labs = ["clean", "2/255", "4/255", "8/255", "16/255"]
    STEP = 11.0
    dx = [2.0 + i * STEP for i in range(5)]
    DEPTH = 9.0                                    # world mm between the cut-outs along the floor normal
    sdmax = 0.0
    feet = {}
    for r in (2, 1, 0):                            # back to front
        key, tint, mk, lab = ROWS[r]
        d = data[key]
        # bulgu 11 (08.11): the back cut-outs are moved left along u by the page shift of their depth, so every
        # marker stands straight above its budget label (depth lifts a profile, it no longer shifts it right)
        shift = S.P(S.n[0] * DEPTH * r, S.n[1] * DEPTH * r)[0] - S.ox
        X, Y = Z.un(S, -shift, DEPTH * r)
        hts = [v * HS for v in d["mean"]]
        fx = [0.0] + dx + [dx[-1] + 2.0]
        fh = [hts[0]] + hts + [hts[-1]]
        p0, top = Z.profil_kart(S, f"c{r}", X, Y, 0.0, fx, fh, tint, t=4.0, edge_hex=vf.tint_of(tint)[1], k=(0.05, 0.03),
                                group=f"c{r}")
        feet[r] = (p0, p0[0] + fx[-1])
        ec = vf.tint_of(tint)[1]
        for i, (px, py) in enumerate(top[1:-1]):
            Z.isaret(f"m{r}_{i}", px, py, mk, fill=vf.tint_of(tint)[0], edge=ec, size=2.0, group=f"c{r}")
        if "sd" in d:
            sdmax = max(sdmax, max(d["sd"]))
    # review round 2 (08.11.2026): the back cut-outs stand straight behind the front one, so their own bases are
    # hidden and a reader measured them from the front base (WRN clean read ~119 instead of 89.5). The hidden base
    # edges are drawn dashed (the hidden-line convention of technical drawing), each across its own cut-out, so
    # every height is read from its own base; the scale bar holds within any one cut-out.
    for r in (1, 2):
        (bx0, by0), bx1 = feet[r]
        vf.seg(f"hb{r}", (bx0, by0), (bx1, by0), vf.tint_of(ROWS[r][1])[1], vf.LW["ince"], dash=True)
    # true-length ruler on the front cut-out and the budget labels on its foot
    p0 = feet[0][0]
    # a scale bar instead of an axis: the cut-outs stand at different depths, so one ruler would misread the
    # back profiles; 25 points of accuracy are 10 mm of true vertical length on every cut-out
    xb, yb0 = W - 3.0, p0[1]
    vf.seg("sbar", (xb, yb0), (xb, yb0 - 25 * HS), vf.C["ink"], vf.LW["vurgu"])
    for j, yy_ in enumerate((yb0, yb0 - 25 * HS)):
        vf.seg(f"sbar_t{j}", (xb - 0.9, yy_), (xb + 0.9, yy_), vf.C["ink"], vf.LW["ince"])
    Z.T("sbar_l", xb - 1.6, yb0 - 25 * HS / 2 - lh(Z.S8), ["25", "points"], size=Z.S8, align="r", color="muted")
    for i in range(5):
        Z.T(f"eh{i}", p0[0] + dx[i], p0[1] + 1.2, [labs[i]], size=Z.S8, align="c", color="muted")
    Z.T("eps_h", p0[0] + dx[2], p0[1] + 1.4 + lh(Z.S8), [[("PGD-10 budget ", "r"), ("ε", "r")]], size=Z.S8,
        color="muted", align="c")
    yl = p0[1] + 3.0 + 3 * lh(Z.S8)
    for i in range(5):
        Z.T(f"th{i}", 29.0 + i * 12.0, yl - lh(Z.S8) - 0.5, [labs[i]], size=Z.S8, align="c", color="muted")
    vf.seg("rule0", (1.0, yl - 0.3), (W - 1.0, yl - 0.3), vf.C["frame"], vf.LW["ince"])
    for j, r in enumerate((2, 1, 0)):
        key, tint, mk, lab = ROWS[r]
        y = yl + j * (lh(Z.S8) + 0.4)
        Z.isaret(f"lg{r}", 2.2, y + lh(Z.S8) / 2, mk, fill=vf.tint_of(tint)[0], edge=vf.tint_of(tint)[1], size=2.0)
        Z.T(f"lgt{r}", 3.8, y, [lab], size=Z.S8)
        for i in range(5):
            Z.T(f"n{r}_{i}", 29.0 + i * 12.0, y, [f"{data[key]['mean'][i]:.1f}"], size=Z.S8, align="c")
    yb = yl + 3 * (lh(Z.S8) + 0.4)
    vf.seg("rule1", (1.0, yb), (W - 1.0, yb), vf.C["frame"], vf.LW["vurgu"])
    Z.T("note", 1.0, yb + 0.8, ["accuracy %, back to front; AT models: mean of 3", f"seed pairs, largest SD {sdmax:.2f}; WRN-28-10: one model"],
        size=Z.S8, color="muted")
    Z.sayfa_sigdir()
    deg = []
    for key, tint, mk, lab in ROWS:
        d = data[key]
        for i in range(5):
            if key == "wrn":
                deg.append(Z.ev(f"{lab} {labs[i]}", d["mean"][i], ES.WRN, f"results.{d['keys'][i]}.accuracy",
                                f"read as stored; == foy line {ES.FOY_ROWS[i][0]}"))
            else:
                deg.append(Z.ev(f"{lab} {labs[i]} mean", d["mean"][i], ES.csv_path(1, key),
                                "Accuracy where Attack/Epsilon match", f"mean over pair1-3 files (same path with pair2, pair3); == foy line "
                                f"{ES.FOY_ROWS[i][0]}; printed with one decimal; height {HS} mm per point"))
                deg.append(Z.ev(f"{lab} {labs[i]} sd", d["sd"][i], ES.csv_path(1, key),
                                "Accuracy", f"SD over the pair1-3 files; == foy line {ES.FOY_ROWS[i][0]}"))
    deg.append(Z.ev("largest SD printed", round(sdmax, 2), "results/C1_REFERANS_FOYU.md:360", "max of the SD cells",
                    "max over models and budgets, two decimals"))
    ents = {"vit": "#" + vf.C["vurgu3"], "r32": "#" + vf.C["vurgu5"], "panel": "#" + vf.C["vurgu6"]}
    return Z.bitir(
        STEM, message="Robust accuracy under PGD-10: three cut-out profiles whose heights are the accuracies; the "
                      "number rows print the same values.", kind=KIND, panels=1, caption=CAPTION,
        sablon="tek_kart_veri", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "girdiler": inputs, "olcek_mm_per_puan": HS,
                  "karantina_istisnasi": {"yol": ES.WRN, "foy_satirlari": [19, 354, 360, 361, 362, 363, 364],
                                          "gerekce": "the reference sheet cites this file (line 354) and prints its values"}},
        manifest={"entities": ents, "sahne_kalibi": "kesik_profil_levhalari",
                  "ikiz_kodlama": "every accuracy is printed as a number in the rows under the scene",
                  "denge_muafiyet": {"3b_veri": "block height is the accuracy as a true length on the one vertical "
                                                "dimetric axis, and the number rows print every value (K7)"},
                  "derinlik_ekseni": "orders the models by robustness (front least robust), carries no value"},
        denge={"3b_veri": (True, "block heights carry the measured accuracy on the vertical axis; K7 twin coding: the "
                                 "number rows print every value"),
               "panel_basina_bir_iddia": (True, "one panel: accuracy falls with the budget for all three models")},
        n_exempt_reason="three seed pairs per AT model are stated in the note line, WRN is one model",
        okunan_ek=inputs + ["results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
