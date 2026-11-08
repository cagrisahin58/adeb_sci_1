#!/usr/bin/env python
"""z_spread_clean_gap (Fig. 15 v2, Üslup Z): protocol spread against the clean-accuracy gap on a deep stage.

    python paper/figures_v2/z_spread_clean_gap.py [--check] [--bak]

Single column. A deep stage plate, aligned with the cards (front edge page-horizontal), carries two upright
cards: at the back the three-protocol spread (raw, target-correct, both-correct) of every model pair with the
identity prediction at p = 1 as a small open ring; at the front the successful-source minus both-correct term
with a dashed zero line. Depth tells the reading order (the measure at the back, the term it leaves out in
front); the back card stands higher and to the right, so the two never overlap. Values are positions on flat
cards; no line is fitted. Data: the v1 rule paper/figures/charts/fig_spread_clean_gap.py veri()
(results/q1/fig_yayilim_temiz_fark_veri.json, checked against sheet lines 1014-1073). Naming: step 4.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
SC = Z.yukle("paper/figures/charts/fig_spread_clean_gap.py", "v1_spread_clean_gap")

STEM = "z_spread_clean_gap"
KIND = "single"
W = vf.page_width(KIND)
GROUPS = [  # data group -> (marker, fill, edge, printed label)
    ("CIFAR-10 Linf, AT cifti", "o", "vurgu1", "vurgu1", "CIFAR-10 L∞ AT"),
    ("CIFAR-10 L2, AT cifti", "^", "vurgu2", "vurgu2", "CIFAR-10 L2 AT"),
    ("CIFAR-100 Linf, AT cifti", "s", "vurgu3", "vurgu3", "CIFAR-100 AT"),
    ("SVHN Linf, AT cifti", "D", "vurgu4", "vurgu4", "SVHN AT"),
    ("CIFAR-10 Linf, WRN-28-10 referansiyla", "v", "vurgu5", "vurgu5", "with WRN-28-10 ref."),
    ("CIFAR-10 Linf, standart egitimli modeller", "s", "FFFFFF", "ink", "standard training"),
    ("CIFAR-10 Linf, son kontrol noktasi", "D", "vurgu6", "muted", "last checkpoint"),
    ("CIFAR-10 Linf, RobustBench havuzu", "o", "ECE9E5", "frame", "RobustBench pool"),
]
CAPTION = ("Protocol spread against the clean-accuracy gap on a deep stage. All 60 model pairs. Back card, "
           "Three-protocol spread: unconditioned, target-correct and both-correct, rings the identity prediction "
           "at p = 1; front card, Successful-source minus both-correct, the term left out. Values are positions "
           "on the flat cards; no line is fitted.")


def main():
    d, by, parity, foy = SC.veri()
    N = d["noktalar"]
    vf.reset(STEM, W, 130.0, naming_step=4, naming_kind="serit")
    OX, OY = 2.5, 118.0
    S = Z.Sahne(OX, OY)
    CW = 59.5
    HF, HB = 40.0, 36.0
    DB = 62.0
    Z.plaka_un(S, "stage", *Z.un(S, 0.0, 0.0), CW + 3.0, DB + 6.0, 2.0)
    look = {g[0]: g[1:] for g in GROUPS}
    xmax = 24.0
    cards = [("back", "Three-protocol spread", HB, DB + 2.0, (0.0, 22.0), (0, 5, 10, 15, 20), "pts"),
             ("front", "Successful-source minus both-correct", HF, 2.0, (-38.0, 22.0), (-30, -15, 0, 15),
              "pts")]
    deg = []
    for ci, (key, title, ch, dep, (v0, v1), ticks, ylab) in enumerate(cards):
        X, Y = Z.un(S, 1.0, dep)
        fx, fy, fw, fh = Z.kart(S, key, X, Y, 0.0, CW, ch, "kutu", t=1.6, k=(0.05, 0.035), group=key,
                                cont="stage_top")
        face = f"{key}_face"
        T(f"ti_{key}", fx + 1.2, fy + 0.8, [[(title, "sb")]], size=Z.S8, cont=face)
        px0, px1 = fx + 10.5, fx + fw - 2.0
        py0, py1 = fy + fh - 2.2 - lh(Z.S8) - 1.6, fy + 1.0 + 2 * lh(Z.S8) + 1.6
        sx = Z.Olcek(0.0, xmax, px0, px1)
        sy = Z.Olcek(v0, v1, py0, py1)
        T(f"tn_{key}", px0 - 2.0, fy + 0.8 + lh(Z.S8) + 0.2, [ylab], size=Z.S8, color="muted", align="r", cont=face)
        Z.kot_dikey(f"ay_{key}", px0 - 0.8, py0, py1, sy, list(ticks), [Z.fmt(t_, 0) for t_ in ticks], cont=face)
        Z.kot(f"ax_{key}", px0, px1, py0 + 0.8, sx, [0, 5, 10, 15, 20], ["0", "5", "10", "15", "20"], cont=face)
        if key == "front":
            vf.seg("zero", (px0, sy(0.0)), (px1, sy(0.0)), vf.C["frame"], vf.LW["ince"], dash=True)
        if key == "back":                          # identity rings first: nothing grey lies under a white mark
            for i, n in enumerate(N):
                Z.isaret(f"id_{i}", sx(n["temiz_fark_mutlak"]), sy(abs(n["raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"])),
                         "o", fill=None, edge="ink", size=1.35, group=f"pt_{key}")
        order = sorted(range(len(N)), key=lambda i: 0 if "havuzu" in N[i]["grup"] else 1)   # pool first, behind
        for i in order:
            n = N[i]
            mk, fill, edge, lab = look[n["grup"]]
            x = sx(n["temiz_fark_mutlak"])
            if key == "back":
                y = sy(n["yayilim_uc"])
            else:
                y = sy(n["bas_kaynak_eksi_bc_asimetri"])
            sz = 1.35 if "havuzu" in n["grup"] else 2.0 if "standart" in n["grup"] else 1.7
            Z.isaret(f"p{ci}_{i}", x, y, mk, fill=vf.C.get(fill, fill), edge=vf.C.get(edge, edge), size=sz,
                     group=f"pt_{key}")
    T("xl", OX + 1.0 + CW / 2, OY + 2.8, [f"|clean-accuracy gap| (pts); n = {len(N)} pairs"], size=Z.S8, color="muted",
      align="c")
    yl = OY + 2.8 + lh(Z.S8) + 1.0
    for j, (g, mk, fill, edge, lab) in enumerate(GROUPS):
        cx = 1.0 + (j % 2) * 42.0
        cy = yl + (j // 2) * (lh(Z.S8) + 0.2)
        Z.isaret(f"lg{j}", cx + 1.0, cy + lh(Z.S8) / 2, mk, fill=vf.C.get(fill, fill), edge=vf.C.get(edge, edge),
                 size=1.8)
        T(f"lgt{j}", cx + 2.6, cy, [lab], size=Z.S8)
    cy = yl + 4 * (lh(Z.S8) + 0.2)
    Z.isaret("lgid", 2.0, cy + lh(Z.S8) / 2, "o", fill=None, edge="ink", size=1.35)
    T("lgidt", 3.6, cy, ["identity prediction (back card)"], size=Z.S8)
    for _pid in ["ti_back", "ti_front"]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    for i, n in enumerate(N):
        for k in ("temiz_fark_mutlak", "yayilim_uc", "bas_kaynak_eksi_bc_asimetri",
                  "raw_eksi_tc_asimetri_ozdeslik_ongorusu_p1"):
            deg.append(Z.ev(f"point {i} ({n['grup']}, pair {n['cift']}) {k}", n[k], SC.DATA, f"noktalar[{i}].{k}",
                            "read as stored; definition checks of fig_yayilim_temiz_fark.load_and_check; position"))
    for g, pts in by.items():
        deg.append(Z.ev(f"{g} n", len(pts), SC.DATA, "noktalar[].grup", "count; == foy lines 1022-1030"))
    deg.append(Z.ev("identity parity max |dev|", parity, SC.DATA, "egim.ozdeslik_paritesi.mutlak_sapma_max",
                    "read; == foy line 1073"))
    ents = {}
    return Z.bitir(
        STEM, message="The three-protocol spread grows with the clean-accuracy gap as the identity predicts; the "
                      "successful-source term it leaves out is large and of either sign.", kind=KIND, panels=2,
        caption=CAPTION, sablon="ortak_satirli_katlar", tur="veri", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy},
        manifest={"entities": ents, "sahne_kalibi": "derin_sahne",
                  "panel_adlari": [c[1] for c in cards],
                  "derinlik_ekseni": "reading order: the measure at the back, the term it leaves out in front",
                  "ikiz_kodlama": "values are positions on two flat upright cards"},
        denge={"panel_basina_bir_iddia": (True, "back card the spread, front card the term it leaves out"),
               "sus_arka_plan": (False, "the stage plate is the grouping tool of style Z and carries both cards")},
        n_exempt_reason="each card prints n = 60 pairs", okunan_ek=[SC.DATA, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
