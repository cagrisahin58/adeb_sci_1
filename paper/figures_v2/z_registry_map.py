#!/usr/bin/env python
"""z_registry_map (Fig. 5 v2, Üslup Z): registered tests and decision rules as a flat table-chart.

    python paper/figures_v2/z_registry_map.py [--check] [--bak]

Double column, flat-card composition (third round, 09.11.2026: the staircase is gone). Every test family is a
flat row band (alternating tones), numbered by a ring in registration order (1-7) from top to bottom; the four
families of the main registration sit in one group card, the three of the addendum in a second (the split is
the text's sentence, 03_methodology.tex line 295). Each row: test id and quantity,
the falsification rule underneath (muted), and at the right the registered values on a number line (predicted
size filled diamond, falsification threshold open circle, the +-0.1 equivalence band a grey bar) with the
predicted value printed. Measured outcomes are not drawn. Content: the v1 rule paper/figures/visio/fig_registry_map.py
(rows, foy_checks; results/q1/konsey_kayit_kurallari.json against sheet section M13.2). Naming: step 3.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
RM =Z.yukle_sema("paper/figures/visio/fig_registry_map.py", "v1_registry_map")

STEM = "z_registry_map"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Registered tests and decision rules. Each band is one family, numbered in registration order and "
           "grouped into the main registration and the addendum; rows give test and quantity, place the predicted "
           "size (diamond) and falsification threshold (circle) on a number line with the ±0.1 band, and state the "
           "falsifying rule. Holm correction is per family; ImageNetV2 rows are descriptive.")


def main():
    R = RM.rows()
    foy, _ab = RM.foy_checks()
    fams = []
    for r in R:
        if r[0]:
            fams.append({"name": r[0], "holm": r[1], "rows": []})
        fams[-1]["rows"].append(r)
    vf.reset(STEM, W, 150.0, naming_step=3, naming_kind="rakam")
    LH = lh(Z.S8)
    nF = len(fams)
    # the registration split is the text's own sentence (03_methodology.tex line 295): main = panel tests,
    # two-by-two design, attack side, masking; addendum = CIFAR-100, ImageNetV2, gradient alignment
    NMAIN = 4
    assert [f["name"] for f in fams[NMAIN:]] and "CIFAR-100" in fams[NMAIN]["name"], [f["name"] for f in fams]
    GX = 1.0                       # outer group cards
    FX = GX + 1.2                  # family rows inside them
    FW = W - 2 * FX
    COLF, COLQ, COLL, COLP = 30.5, 47.0, 23.0, 11.0
    COLR = FW - COLF - COLQ - COLL - COLP - 3.0

    def rlines(rule):
        return 1 if Z.tw([Z.runs(rule)], Z.S8) <= COLR - 0.6 else 2

    def fam_h(f):
        return max(sum(rlines(r[8]) for r in f["rows"]) * LH, 2 * LH) + 1.8
    # third round (09.11.2026): flat table-chart. Families run top to bottom in registration order as flat
    # row bands (alternating tones) inside two group cards, main registration and addendum; no staircase.
    GH = LH + 1.6                                  # group card head
    groups = [("Main registration", "frozen before any run", fams[:NMAIN], 0),
              ("Addendum", "frozen before its matrices or gradients", fams[NMAIN:], NMAIN)]
    y0 = 1.0 + LH + 2.2
    gcards = []
    for gi, (gname, gsub, gf_, k0) in enumerate(groups):
        gh = GH + sum(fam_h(f) for f in gf_) + (len(gf_) - 1) * 0.8 + 1.0
        Z.duz_kart(f"grp{gi}", GX, y0, W - 2 * GX, gh, "kutu")
        T(f"gn{gi}", FX, y0 + 0.6, [[(gname, "sb")]], size=Z.S8, cont=f"grp{gi}_face")
        T(f"gs{gi}", FX + Z.tw([[(gname, "sb")]], Z.S8) + 1.6, y0 + 0.6, [gsub], size=Z.S8, color="muted",
          cont=f"grp{gi}_face")
        gcards.append((y0, gh, k0, len(gf_)))
        y0 += gh + 2.0
    OY = y0 - 2.0
    for k, fam in enumerate(fams):
        hgt = fam_h(fam)
        gi = 0 if k < NMAIN else 1
        gy0, _gh, k0, _n = gcards[gi]
        fy_ = gy0 + GH + sum(fam_h(f) + 0.8 for f in fams[k0:k])
        fx, fy, fw, fh = Z.duz_kart(f"st{k}", FX, fy_, FW, hgt, "govde_panel" if k % 2 == 0 else "ton_6",
                                    cont=f"grp{gi}_face")
        face = f"st{k}_face"
        Z.bl.ring(f"rg{k}", gr(fx + 1.0), gr(fy + 0.9), k + 1, container=face)
        dr = vf.IDS[f"rg{k}"]["w"]
        T(f"fn{k}", fx + 1.6 + dr, fy + 0.9 + (dr - LH) / 2, [[(fam["name"], "sb")]], size=Z.S8, cont=face)
        T(f"fh{k}", fx + 1.6 + dr, fy + 0.9 + (dr - LH) / 2 + LH, [fam["holm"]], size=Z.S8, color="muted", cont=face)
        y = fy + 0.9
        for j, r in enumerate(fam["rows"]):
            _f, _h, tid, qty, pred, band, thr, ptxt, rule = r
            xq = fx + COLF
            T(f"ti{k}{j}", xq, y, [[(tid + "  ", "sb")] + Z.runs(qty)], size=Z.S8, cont=face)
            lx0 = xq + COLQ + 1.0
            lx1 = lx0 + COLL
            yl = y + LH / 2
            sc = Z.Olcek(RM.LO, RM.HI, lx0, lx1)
            if pred is not None or band or thr is not None:
                vf.seg(f"nl{k}{j}", (lx0, yl), (lx1, yl), vf.C["frame"], vf.LW["ince"])
                for tk in (0.0, 0.4, 0.8):
                    vf.seg(f"nt{k}{j}{tk}", (sc(tk), yl - 0.5), (sc(tk), yl + 0.5), vf.C["frame"], vf.LW["ince"])
                if band:
                    bb = [(sc(-RM.DELTA), yl - 0.45), (sc(RM.DELTA), yl - 0.45), (sc(RM.DELTA), yl + 0.45),
                          (sc(-RM.DELTA), yl + 0.45)]
                    vf.poly(f"nb{k}{j}", bb + [bb[0]], fill=vf.tint_of("notr")[1], line=None, role="obstacle",
                            group=f"nl{k}{j}")
                if thr is not None:
                    Z.isaret(f"nc{k}{j}", sc(thr), yl, "o", fill=None, edge="ink", size=1.6, group=f"nl{k}{j}")
                if pred is not None:
                    Z.isaret(f"nd{k}{j}", sc(pred[1]), yl, "D", fill="ink", edge="ink", size=1.7, group=f"nl{k}{j}")
            if ptxt:
                T(f"pv{k}{j}", lx1 + 1.2, y, [Z.runs(ptxt)], size=Z.S8, cont=face)
            xr = lx1 + COLP + 1.6
            nl = rlines(rule)
            if nl == 1:
                T(f"tr{k}{j}", xr, y, [Z.runs(rule)], size=Z.S8, color="muted", cont=face)
            else:
                wds = rule.split(" ")
                cut = len(wds) // 2 + 1
                T(f"tr{k}{j}", xr, y, [Z.runs(" ".join(wds[:cut])), Z.runs(" ".join(wds[cut:]))], size=Z.S8,
                  color="muted", cont=face)
            y += nl * LH
    yh = 1.0
    T("hf", FX, yh, [[("Family", "sb")]], size=Z.S8, color="muted")
    T("hq", FX + COLF, yh, [[("Test and quantity", "sb")]], size=Z.S8, color="muted")
    T("hl", FX + COLF + COLQ + 1.0, yh, [[("Pre-registered values", "sb")]], size=Z.S8, color="muted")
    T("hr", FX + COLF + COLQ + COLL + COLP + 1.6, yh, [[("Falsified if", "sb")]], size=Z.S8, color="muted")
    # bulgu 5 (08.11): booktabs head rule, the one 1.5 pt (vurgu) line of the figure; table rules are the
    # emphasis edges of style Z (as Figures 7, 13 and 16)
    vf.seg("h_rule", (1.0, yh + LH + 0.4), (W - 1.0, yh + LH + 0.4), vf.C["frame"], vf.LW["vurgu"])
    # legend
    yl = OY + 2.0
    x = 1.0
    Z.isaret("lgd", x + 1.0, yl + LH / 2, "D", fill="ink", edge="ink", size=1.7)
    T("lgdt", x + 2.6, yl, ["predicted size"], size=Z.S8)
    x += 2.6 + Z.tw(["predicted size"], Z.S8) + 3.0
    Z.isaret("lgc", x + 1.0, yl + LH / 2, "o", fill=None, edge="ink", size=1.6)
    T("lgct", x + 2.6, yl, ["falsification threshold"], size=Z.S8)
    x += 2.6 + Z.tw(["falsification threshold"], Z.S8) + 3.0
    b = [(x, yl + LH / 2 - 0.45), (x + 3.0, yl + LH / 2 - 0.45), (x + 3.0, yl + LH / 2 + 0.45), (x, yl + LH / 2 + 0.45)]
    vf.poly("lgb", b + [b[0]], fill=vf.tint_of("notr")[1], line=None, role="obstacle")
    T("lgbt", x + 3.8, yl, [f"±{RM.DELTA:g} equivalence band"], size=Z.S8)
    x += 3.8 + Z.tw([f"±{RM.DELTA:g} equivalence band"], Z.S8) + 3.0
    T("lgax", x, yl, ["ticks 0, 0.4, 0.8; measured outcomes are not drawn"], size=Z.S8,
      color="muted")
    Z.sayfa_sigdir()
    deg = [Z.ev(p, v_, RM.SRC, p, "read as is; printed with :g") for p, v_ in RM.OKUNAN.items()
           if not isinstance(v_, (dict, list))]
    deg.append(Z.ev("number line axis", [RM.LO, RM.HI], RM.SRC, "(axis, not data)",
                    "axis range -0.3 to 0.9, ticks 0, 0.4, 0.8, chosen to hold every threshold"))
    deg.append(Z.ev("registration groups", {"main": [f["name"] for f in fams[:NMAIN]],
                                            "addendum": [f["name"] for f in fams[NMAIN:]]},
                    "paper/manuscript/sections/03_methodology.tex:295", "main registration (panel tests, two-by-two "
                    "design, attack side, masking) ... addendum (CIFAR-100, ImageNetV2, gradient alignment)",
                    "group membership read from the text sentence; no number drawn"))
    return Z.bitir(
        STEM, message="The registry: every pre-registered test with its quantity, predicted size, falsification "
                      "threshold and rule, ordered by registration.", kind=KIND, panels=7, caption=CAPTION,
        sablon="tablodan_sekle", tur="sematik", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy},
        manifest={"sahne_kalibi": "yok (duz satirli tablo-grafik, ucuncu tur)",
                  "istasyonlar": [f"{i + 1} {f['name']}" for i, f in enumerate(fams)],
                  "derinlik_ekseni": "none: registration order runs top to bottom",
                  "ic_ice_derinlik": {"deger": 3, "gerekce": "group card holds family band which holds number lines"},
                  "denge_muafiyet": {"karakter_cm2": "the figure replaces Table 3; test names, quantities and rules are "
                                                     "its content",
                                     "yazi_kutusu_alani": "two lines per test (quantity and rule) at the 8 pt floor"},
                  "sonuc_cizilmedi": "measured outcomes are not drawn"},
        denge={"panel_basina_bir_iddia": (True, "each band is one test family with its decision rules"),
               "her_sayinin_kaynagi": (True, "every threshold is read from the registry rules file")},
        n_exempt_reason="a registry of thresholds draws no sample", okunan_ek=[RM.SRC, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
