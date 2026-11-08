#!/usr/bin/env python
"""z_decomposition_schematic (Fig. 3 v2, Üslup Z): the decomposition as a three-tier frosted section.

    python paper/figures_v2/z_decomposition_schematic.py [--check] [--bak]

Single column. At the top the 2 x 2 transfer matrix stands on a small plinth (rows and columns R and V; the
diagonal cells are the white-box rate w, the off-diagonal cells the transfer rate T) beside the definitions of
similarity and direction. Below, three frosted glass tiers, each set 3 mm further back (the depth axis is the
aggregation level): the pair-level split of log T into vulnerability, similarity and half the directional
residual; the panel means sigma and rho; the source gap G split into a symmetric and a directional part. Labelled
flow arrows join the tiers (per pair (i, j), panel mean, R minus V). Term families are carried by coloured
under-brackets and names (vulnerability stone, similarity olive, direction lavender grey); formula text is ink.
No measured number is drawn; the identity check of paper/figures/konsey/fig_decomposition_schematic.py goes to
the evidence file. Naming: step 2 (labelled flow arrows).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
import fig_decomposition_schematic as DS  # noqa: E402  (konsey; identity_check only)

STEM = "z_decomposition_schematic"
KIND = "single"
W = vf.page_width(KIND)
DV = {"⟨", "⟩", "∈"}
LHS = None
CAPTION = ("Decomposition used throughout, in three tiers. Top to bottom, the arrows per pair (i, j), panel "
           "mean and R minus V mark three steps: the log transfer rate splits exactly into vulnerability, similarity "
           "and half a directional residual; panel averages give σ and ρ; the source gap G splits into symmetric and "
           "directional parts. Tiers recede with the aggregation level.")


def F(s, key="r"):
    """Runs of one line: glyphs Open Sans lacks (angle brackets, element-of, tau-bar) go to DejaVu Sans."""
    runs, cur = [], ""
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "τ" and i + 1 < len(s) and s[i + 1] == "̄":
            if cur:
                runs.append((cur, key))
                cur = ""
            runs.append(("τ̄", key + "@DejaVuSans" if "@" not in key else key))
            i += 2
            continue
        if ch in DV:
            if cur:
                runs.append((cur, key))
                cur = ""
            runs.append((ch, key + "@DejaVuSans"))
        else:
            cur += ch
        i += 1
    if cur:
        runs.append((cur, key))
    return runs


def bracket(pid, x0, x1, y, col, lab, cont, xc=None):
    y = y + 0.5
    vf.seg(pid, (x0, y + 0.9), (x1, y + 0.9), col, vf.LW["vurgu"])
    vf.seg(pid + "a", (x0, y), (x0, y + 0.9), col, vf.LW["ince"])
    vf.seg(pid + "b", (x1, y), (x1, y + 0.9), col, vf.LW["ince"])
    T(pid + "t", xc if xc is not None else (x0 + x1) / 2, y + 1.6, [[(lab, "sb")]], size=Z.S8, align="c", cont=cont)


TONE = {"vul": "ton_1", "sim": "ton_2", "dir": "ton_4"}


def term_row(pid, x, y, items, cont, gap=2.2, labels=None):
    """Place the terms of one formula line; a bracketed term sits in its own light family-tone box together with
    its bracket and name (nesting: tier card > term box > text). Returns [(x0, x1, key)]."""
    out, pos = [], []
    xx = x
    for k, (txt, br) in enumerate(items):
        w = Z.tw([F(txt)], Z.S8)
        lw_ = Z.tw([[(labels[len(pos)], "sb")]], Z.S8) if (br and labels) else 0.0
        if br:
            pos.append((k, xx, w, lw_))
        xx += max(w, lw_ if br else 0.0) + gap
    xx = x
    j = 0
    for k, (txt, br) in enumerate(items):
        w = Z.tw([F(txt)], Z.S8)
        c = cont
        if br:
            lw_ = pos[j][3]
            span = max(w, lw_)
            bx0, bx1 = xx - 1.0, xx + span + 1.0
            box = [(bx0, y - 1.0), (bx1, y - 1.0), (bx1, y + 2 * LHS + 3.8), (bx0, y + 2 * LHS + 3.8)]
            vf.poly(f"{pid}bx{k}", box + [box[0]], fill=vf.tint_of(TONE[br])[0], line=None, role="container",
                    container=cont)
            c = f"{pid}bx{k}"
            tx0 = xx + (span - w) / 2
            T(f"{pid}{k}", tx0, y, [F(txt)], size=Z.S8, cont=c)
            out.append((tx0, tx0 + w, br, c, xx + span / 2))
            j += 1
            xx += span + gap
        else:
            T(f"{pid}{k}", xx, y, [F(txt)], size=Z.S8, cont=c)
            xx += w + gap
    return out


def main():
    r1, r2 = DS.identity_check(20261031, trials=200)[:2]
    vf.reset(STEM, W, 150.0, naming_step=2, naming_kind="akis")
    OX, OY = 2.0, 140.0
    S = Z.Sahne(OX, OY)
    global LHS
    LH = lh(Z.S8)
    LHS = LH
    col = {"vul": vf.C["vurgu1"], "sim": vf.C["vurgu2"], "dir": vf.C["vurgu4"]}
    # ---- top: the 2 x 2 matrix on a plinth, and the definitions
    S0 = Z.Sahne(8.0, 27.5)
    CS = 9.0
    mx, my, mw, mh = Z.kart(S0, "mat", 0.0, 0.0, 0.0, 2 * CS, 2 * CS, "kutu", t=3.0, k=(0.06, 0.04), group="mat")
    for i in range(2):
        for j in range(2):
            x, y_ = mx + j * CS, my + i * CS
            pts = [(x, y_), (x + CS, y_), (x + CS, y_ + CS), (x, y_ + CS)]
            vf.poly(f"mc{i}{j}", pts + [pts[0]], fill=vf.tint_of("notr")[1] if i == j else vf.tint_of("kutu")[0],
                    line=Z.soft(vf.tint_of("kutu")[1], 0.2), lw=vf.LW["ince"], role="deco", container="mat_face")
            T(f"mt{i}{j}", x + CS / 2, y_ + (CS - LH) / 2, [[("w" if i == j else "T", "i")]], size=Z.S8, align="c",
              cont=f"mc{i}{j}", color="white" if i == j else "ink")
    for i, lab in enumerate(("R", "V")):
        T(f"rl{i}", mx - 1.0, my + i * CS + (CS - LH) / 2, [lab], size=Z.S8, align="r")
        T(f"cl{i}", mx + i * CS + CS / 2, my - LH - 2.8, [lab], size=Z.S8, align="c")
    tx = 33.0
    T("d0", tx, 4.0, [[("i", "i"), (" source (row), ", "r"), ("j", "i"), (" target (column)", "r")]], size=Z.S8,
      color="muted")
    T("dT", tx, 4.0 + LH + 1.0, [[("T", "i"), (": transfer rate, off the diagonal", "r")]], size=Z.S8)
    T("dw", tx, 4.0 + 2 * LH + 2.0, [[("w", "i"), (": white-box rate, on the diagonal", "r")]], size=Z.S8)
    yd = 31.0
    T("sim_l", 2.0, yd, [[("similarity", "sb")]], size=Z.S8)
    T("sim_f", 21.0, yd, [F("log τ̄(i, j) = ½ log[T(i, j) T(j, i) / w(i) w(j)]")], size=Z.S8)
    T("dir_l", 2.0, yd + LH + 0.4, [[("direction", "sb")]], size=Z.S8)
    T("dir_f", 21.0, yd + LH + 0.4, [F("r(i, j) = log[T(i, j) w(i) / T(j, i) w(j)]")], size=Z.S8)
    for k, (key, y) in enumerate((("sim", yd), ("dir", yd + LH + 0.4))):
        Z.isaret(f"dsq{k}", 19.0, y + LH / 2, "s", fill=col[key], edge=col[key], size=1.8)
    # ---- three frosted tiers, each 3 mm further back
    tiers = [
        ("per pair (i, j)", 3 * LH + 9.0),
        ("panel mean", 3 * LH + 8.6),
        ("R minus V", 2 * LH + 7.0),
    ]
    y = yd + 2 * LH + 1.6
    zt = 0
    boxes = []
    for k, (arrow_lab, h) in enumerate(tiers):
        # flow arrow with its label
        ay0, ay1 = y + 0.3, y + 6.0
        vf.spline(f"ar{k}", [(W / 2 - 6.0, ay0), (W / 2 - 9.0, (ay0 + ay1) / 2), (W / 2 - 7.0, ay1)], vf.C["arrow"], vf.LW["ince"], arrow=True)
        vf.note_naming(f"ar{k}", "flow")
        T(f"arl{k}", W / 2 - 3.4, ay0 + 0.6, [arrow_lab], size=Z.S8, color="muted")
        y = ay1 + 0.8
        dep = 6.0 * k
        sh = Z.Sahne(OX, y + h + 0.664 * dep + 1.4)
        X, Y = Z.un(sh, 0.0, dep)
        fx, fy, fw, fh = Z.kart(sh, f"t{k}", X, Y, 0.0, W - OX - 6.0, h, "cam", t=1.6, shadow=False, group=f"t{k}")
        boxes.append((fx, fy, fw, fh))
        y = fy + fh + 0.6
    face = "t0_face"
    fx, fy, fw, fh = boxes[0]
    T("p0", fx + 1.4, fy + 0.8, [F("log T(i, j) =")], size=Z.S8, cont=face)
    yt1 = fy + 0.8 + LH + 2.0
    br = term_row("p1_", fx + 4.0, yt1, [("log w(j)", "vul"), ("+", None), ("log τ̄(i, j)", "sim"), ("+", None),
                                                  ("½ r(i, j)", "dir")], face, gap=2.4,
                  labels=["vulnerability", "similarity", "direction"])
    names = {"vul": "vulnerability", "sim": "similarity", "dir": "direction"}
    for k, (x0, x1, key, c, xc) in enumerate(br):
        bracket(f"b0{k}", x0, x1, yt1 + LH - 0.2, col[key], names[key], c, xc)
    face = "t1_face"
    fx, fy, fw, fh = boxes[1]
    yt2 = fy + 1.8
    br = term_row("p2_", fx + 3.0, yt2, [("σ(m) = ⟨log τ̄(m, c)⟩", "sim"), ("ρ(m) = ⟨r(c, m)⟩", "dir")], face,
                  gap=3.0, labels=["panel similarity", "direction"])
    for k, (x0, x1, key, c, xc) in enumerate(br):
        bracket(f"b1{k}", x0, x1, yt2 + LH - 0.2, col[key], ("panel similarity", "direction")[k], c, xc)
    T("p2n", fx + 1.4, yt2 + 2 * LH + 4.6, [F("⟨·⟩: mean over panel members c ∈ P")], size=Z.S8, color="muted",
      cont=face)
    face = "t2_face"
    fx, fy, fw, fh = boxes[2]
    yt3 = fy + 1.8
    br = term_row("p3_", fx + 2.0, yt3, [("G", "vul"), ("=", None), ("[σ(R) − σ(V)]", "sim"),
                                             ("− ½[ρ(R) − ρ(V)]", "dir")], face, gap=2.0,
                  labels=["source gap", "symmetric", "directional"])
    for k, (x0, x1, key, c, xc) in enumerate(br):
        bracket(f"b2{k}", x0, x1, yt3 + LH - 0.2, col[key], ("source gap", "symmetric", "directional")[k], c, xc)
    Z.sayfa_sigdir()
    deg = [Z.ev("identity log T = log w + log tau-bar + r/2, max abs residual", r1,
                "paper/figures/konsey/fig_decomposition_schematic.py", "identity_check(seed=20261031, trials=200)[0]",
                "200 seeded random positive 7-model matrices; not drawn"),
           Z.ev("gap G = (sigma_R - sigma_V) - (rho_R - rho_V)/2, max abs residual", r2,
                "paper/figures/konsey/fig_decomposition_schematic.py", "identity_check(seed=20261031, trials=200)[1]",
                "not drawn"),
           Z.ev("the constant 1/2 of the definitions", 0.5, "paper/manuscript/sections/03_methodology.tex",
                "eq. definitions of log tau-bar and r", "definition, printed as ½")]
    ents = {"sigma": "#" + col["sim"], "rho": "#" + col["dir"]}
    return Z.bitir(
        STEM, message="The log transfer rate splits exactly into vulnerability, similarity and direction, and the "
                      "source gap into a symmetric and a directional part.", kind=KIND, panels=4, caption=CAPTION,
        sablon="model_acilimi_3b", tur="sematik", degerler=deg, kanit_ek={},
        manifest={"entities": ents, "sahne_kalibi": "uc_katli_kesit",
                  "derinlik_ekseni": "aggregation level: each tier 3 mm further back (pair, panel, gap)",
                  "ic_ice_derinlik": {"deger": 3, "gerekce": "frosted tier card holds a family-tone term box that holds "
                                                             "the formula term, its bracket and its name; the PDF "
                                                             "measure reads the polygon tier face as one level"}},
        denge={"panel_basina_bir_iddia": (True, "each tier is one step of the decomposition"),
               "her_sayinin_kaynagi": (True, "no measured number is drawn; the identity check is in the evidence file")},
        n_exempt_reason="a definitional schematic; no sample is drawn",
        okunan_ek=["paper/figures/konsey/fig_decomposition_schematic.py"])


if __name__ == "__main__":
    sys.exit(main())
