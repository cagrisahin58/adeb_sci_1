#!/usr/bin/env python
"""z_registry_map (Fig. 5 v2, Üslup Z): registered tests and decision rules as a two-flight staircase.

    python paper/figures_v2/z_registry_map.py [--check] [--bak]

Double column. Every test family is a step; the step's riser (an upright face of the one dimetric view) carries
the family's tests row by row, its tread the depth up to the next family. The left flight holds the four
families of the main registration, the right flight the three of the addendum; each family stands behind and
above the previous one, so the depth axis is the registration order (rings 1-7). Each row: test id and quantity,
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
RM = Z.yukle_sema("paper/figures/visio/fig_registry_map.py", "v1_registry_map")

STEM = "z_registry_map"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Registered tests and decision rules as a staircase. Each step is one family, numbered in registration "
           "order and set behind the previous one; rows give test and quantity, place the predicted size (diamond) "
           "and falsification threshold (circle) on a number line with the ±0.1 band, and state the falsifying "
           "rule. Holm correction is per family; ImageNetV2 rows are descriptive.")


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
    D = 4.0
    nF = len(fams)
    FW = W - 3.0 - nF * D * 0.273 - D * 0.273 - 1.0
    COLF, COLQ, COLL, COLP = 30.5, 47.0, 23.0, 11.0
    COLR = FW - COLF - COLQ - COLL - COLP - 3.0

    def rlines(rule):
        return 1 if Z.tw([Z.runs(rule)], Z.S8) <= COLR - 0.6 else 2

    def fam_h(f):
        return max(sum(rlines(r[8]) for r in f["rows"]) * LH, 2 * LH) + 1.8
    tot = sum(fam_h(f) for f in fams)
    OY = 3.0 + LH + 2.5 + tot + nF * D * 0.664 + 1.0
    S = Z.Sahne(2.0, OY)
    Z.plaka_un(S, "stage", *Z.un(S, -0.6, -1.5), FW + 1.6, nF * D + 2.5, 1.6, tint="sahne")
    z, dep = 0.0, 0.0
    for k, fam in enumerate(fams):
        hgt = fam_h(fam)
        X, Y = Z.un(S, 0.0, dep)
        fx, fy, fw, fh = Z.kart(S, f"st{k}", X, Y, z, FW, hgt, "govde_panel" if k % 2 == 0 else "ton_6", t=D,
                                shadow=False, group=f"stp{k}", cont="stage_top")
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
        z += hgt
        dep += D
    yh = 1.0
    T("hf", 1.0, yh, [[("Family", "sb")]], size=Z.S8, color="muted")
    T("hq", 1.0 + COLF, yh, [[("Test and quantity", "sb")]], size=Z.S8, color="muted")
    T("hl", 1.0 + COLF + COLQ + 1.0, yh, [[("Pre-registered values", "sb")]], size=Z.S8, color="muted")
    T("hr", 1.0 + COLF + COLQ + COLL + COLP + 2.6, yh, [[("Falsified if", "sb")]], size=Z.S8, color="muted")
    # legend
    yl = OY + 3.4
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
    return Z.bitir(
        STEM, message="The registry: every pre-registered test with its quantity, predicted size, falsification "
                      "threshold and rule, ordered by registration.", kind=KIND, panels=7, caption=CAPTION,
        sablon="tablodan_sekle", tur="sematik", degerler=deg, kanit_ek={"foy_karsilastirmasi": foy},
        manifest={"sahne_kalibi": "yedi_basamakli_merdiven",
                  "istasyonlar": [f"{i + 1} {f['name']}" for i, f in enumerate(fams)],
                  "derinlik_ekseni": "registration order: each family behind and above the previous one",
                  "denge_muafiyet": {"karakter_cm2": "the figure replaces Table 3; test names, quantities and rules are "
                                                     "its content",
                                     "yazi_kutusu_alani": "two lines per test (quantity and rule) at the 8 pt floor"},
                  "sonuc_cizilmedi": "measured outcomes are not drawn"},
        denge={"panel_basina_bir_iddia": (True, "each step is one test family with its decision rules"),
               "her_sayinin_kaynagi": (True, "every threshold is read from the registry rules file")},
        n_exempt_reason="a registry of thresholds draws no sample", okunan_ek=[RM.SRC, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
