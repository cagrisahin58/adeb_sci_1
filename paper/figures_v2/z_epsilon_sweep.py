#!/usr/bin/env python
"""z_epsilon_sweep (Fig. 16 v2, Üslup Z): robust accuracy under PGD-10 as a flat line chart.

    python paper/figures_v2/z_epsilon_sweep.py [--check] [--bak]

Single column (85.29 mm), flat-card composition (third round, 09.11.2026: the extruded cut-out profiles and the
K7 exemption are gone). One flat card holds a 2D line chart: accuracy (y, 0-100 %, 0.4 mm per point) against
the budget (clean, 2/255, 4/255, 8/255, 16/255), one line with markers per model, each labelled at its line end;
the number rows under the card print the same values. Data: the v1 rule paper/figures/charts/fig_epsilon_sweep.py veri() is
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
Z.duz()
sys.argv += ["--uslup", "Z"]
ES = Z.yukle("paper/figures/charts/fig_epsilon_sweep.py", "v1_epsilon_sweep")
sys.argv = sys.argv[:-2]

STEM = "z_epsilon_sweep"
KIND = "single"
W = vf.page_width(KIND)
HS = 0.60          # mm per accuracy point on the y axis
YLO, YHI = 5.0, 95.0   # y range of the chart (accuracy %); every plotted mean lies inside it
ROWS = [("vit_tiny", "govde_vit", "^", "ViT-Tiny AT"), ("resnet18", "govde_r32", "s", "ResNet-18 AT"),
        ("wrn", "govde_panel", "v", "WRN-28-10")]
CAPTION = ("Robust accuracy under PGD-10. CIFAR-10 test accuracy over the budget ε, clean to 16/255, for "
           "ViT-Tiny AT, ResNet-18 AT and WRN-28-10; the number rows under the chart print the plotted values "
           "(mean of three seed pairs; WRN-28-10 is one RobustBench model).")


def main():
    data, inputs, foy = ES.veri()
    vf.reset(STEM, W, 96.0, naming_step=1, naming_kind="yok")
    labs = ["clean", "2/255", "4/255", "8/255", "16/255"]
    LH = lh(Z.S8)
    # third round (09.11.2026): one flat card holding a 2D line chart (accuracy against the budget), the three
    # models labelled directly at the line ends; the number rows under the card print the same values. No
    # cut-out profiles, no depth, no K7 exemption.
    CX, CY = 1.0, 1.0
    CW = W - 2.0
    px0, px1 = CX + 11.0, CX + CW - 21.0
    py1 = CY + 1.0 + LH + 1.4                      # 100 %
    py0 = py1 + (YHI - YLO) * HS
    CH = (py0 + 1.4 + 0.9 + LH + 0.4 + LH + 1.2) - CY
    Z.duz_kart("card", CX, CY, CW, CH, "kutu")
    face = "card_face"
    sy = Z.Olcek(YLO, YHI, py0, py1)
    allv = [v for k_ in data for v in data[k_]["mean"]]
    assert YLO < min(allv) and max(allv) < YHI, (min(allv), max(allv))
    xs = [px0 + 3.0 + i * (px1 - px0 - 5.0) / 4 for i in range(5)]
    for t_ in (25, 50, 75):
        vf.seg(f"gy{t_}", (px0, sy(t_)), (px1, sy(t_)), vf.tint_of("izgara")[0], vf.LW["ince"])
    Z.kot_dikey("ay", px0 - 0.6, py0, py1, sy, [25, 50, 75], ["25", "50", "75"], cont=face)
    sxc = Z.Olcek(0, 4, xs[0], xs[4])
    Z.kot("ax", px0, px1, py0 + 0.6, sxc, [0, 1, 2, 3, 4], labs, cont=face)
    Z.T("eps_h", (xs[0] + xs[4]) / 2, py0 + 0.6 + 1.4 + LH + 0.2, [[("PGD-10 budget ", "r"), ("ε", "r")]], size=Z.S8,
        color="muted", align="c", cont=face)
    Z.T("ylab", CX + 1.2, CY + 0.8, ["accuracy %"], size=Z.S8, color="muted", cont=face)
    sdmax = 0.0
    # direct labels at the line ends, pushed apart where two ends are closer than one line box
    ends = sorted(((sy(data[ROWS[r][0]]["mean"][4]) - LH / 2, r) for r in range(3)))
    lab_y = {}
    last = -1e9
    for y_, r in ends:
        y_ = max(y_, last + LH + 0.2)
        lab_y[r] = y_
        last = y_
    for r in (2, 1, 0):
        key, tint, mk, lab = ROWS[r]
        d = data[key]
        ec = vf.tint_of(tint)[1]
        pts = [(xs[i], sy(v)) for i, v in enumerate(d["mean"])]
        for i in range(4):
            vf.seg(f"l{r}_{i}", pts[i], pts[i + 1], ec, vf.LW["vurgu"])
        for i, (px, py) in enumerate(pts):
            Z.isaret(f"m{r}_{i}", px, py, mk, fill=vf.tint_of(tint)[0], edge=ec, size=1.8, group=f"c{r}")
        Z.T(f"dl{r}", xs[4] + 2.2, lab_y[r], [lab], size=Z.S8, cont=face)
        if "sd" in d:
            sdmax = max(sdmax, max(d["sd"]))
    yl = CY + CH + 1.6 + LH + 0.5
    for i in range(5):
        Z.T(f"th{i}", 29.0 + i * 12.0, yl - LH - 0.5, [labs[i]], size=Z.S8, align="c", color="muted")
    vf.seg("rule0", (1.0, yl - 0.3), (W - 1.0, yl - 0.3), vf.C["frame"], vf.LW["ince"])
    for j, r in enumerate((2, 1, 0)):
        key, tint, mk, lab = ROWS[r]
        y = yl + j * (LH + 0.4)
        Z.isaret(f"lg{r}", 2.2, y + LH / 2, mk, fill=vf.tint_of(tint)[0], edge=vf.tint_of(tint)[1], size=2.0)
        Z.T(f"lgt{r}", 3.8, y, [lab], size=Z.S8)
        for i in range(5):
            Z.T(f"n{r}_{i}", 29.0 + i * 12.0, y, [f"{data[key]['mean'][i]:.1f}"], size=Z.S8, align="c")
    yb = yl + 3 * (LH + 0.4)
    vf.seg("rule1", (1.0, yb), (W - 1.0, yb), vf.C["frame"], vf.LW["vurgu"])
    Z.T("note", 1.0, yb + 0.8, ["accuracy %; AT models: mean of 3 seed pairs,", f"largest SD {sdmax:.2f}; WRN-28-10: one model"],
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
                                f"{ES.FOY_ROWS[i][0]}; printed with one decimal; y position, {HS} mm per point"))
                deg.append(Z.ev(f"{lab} {labs[i]} sd", d["sd"][i], ES.csv_path(1, key),
                                "Accuracy", f"SD over the pair1-3 files; == foy line {ES.FOY_ROWS[i][0]}"))
    deg.append(Z.ev("largest SD printed", round(sdmax, 2), "results/C1_REFERANS_FOYU.md:360", "max of the SD cells",
                    "max over models and budgets, two decimals"))
    ents = {"vit": "#" + vf.C["vurgu3"], "r32": "#" + vf.C["vurgu5"], "panel": "#" + vf.C["vurgu6"]}
    return Z.bitir(
        STEM, message="Robust accuracy under PGD-10 falls with the budget for all three models; the CNN margin over "
                      "the ViT narrows at 16/255.", kind=KIND, panels=1, caption=CAPTION,
        sablon="tek_kart_veri", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "girdiler": inputs, "olcek_mm_per_puan": HS,
                  "karantina_istisnasi": {"yol": ES.WRN, "foy_satirlari": [19, 354, 360, 361, 362, 363, 364],
                                          "gerekce": "the reference sheet cites this file (line 354) and prints its values"}},
        manifest={"entities": ents, "sahne_kalibi": "yok (tek duz kart, cizgi grafigi, ucuncu tur)",
                  "derinlik_ekseni": "none: flat card"},
        denge={"panel_basina_bir_iddia": (True, "one panel: accuracy falls with the budget for all three models")},
        n_exempt_reason="three seed pairs per AT model are stated in the note line, WRN is one model",
        okunan_ek=inputs + ["results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
