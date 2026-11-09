#!/usr/bin/env python
"""z_gradient_alignment (Fig. 11 v2, Üslup Z): input-gradient alignment against similarity in three flat columns.

    python paper/figures_v2/z_gradient_alignment.py [--check] [--bak]

Double column, flat-card composition (third round, 09.11.2026: the steles on the stage plate are gone, which also
closes review finding 3, the repeated stone-slab idea of Figures 11 and 12). Each data set is one flat column card
(CIFAR-10, CIFAR-100, ImageNetV2, left to right, top-aligned). In every column the raw relation (cosine c between
input gradients against log tau-bar) is the upper panel and the residual after the additive model main effects
are removed from both matrices is the lower panel; between them a flat inset strip names the operation ("main
effects removed"), so a column reads as raw, operation, residual rather than as a 2 x 3 grid of equal cards.
Each panel is a flat scatter plot: pair type by marker shape, colour and size (CNN-CNN stone
circle, transformer-transformer terracotta triangle, mixed light square), Spearman r and the pair count printed.
Data: the v1 rule paper/figures/charts/fig_gradient_alignment.py veri() (B10 Mantel files, frozen cell tables;
sheet lines 1970-1977, 2009-2011). Naming: step 4 (row strips and column titles).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
GAV = Z.yukle("paper/figures/charts/fig_gradient_alignment.py", "v1_gradient_alignment")

STEM = "z_gradient_alignment"
KIND = "double"
W = vf.page_width(KIND)
LOOK = {"mixed": ("s", "notr", 1.0, "mixed"), "CNN-CNN": ("o", "vurgu1", 1.15, "CNN–CNN"),
        "T-T": ("^", "vurgu3", 1.35, "transformer–transformer")}
CAPTION = ("Input-gradient alignment against similarity. Cosine c between input gradients against log τ̄ for "
           "every model pair on CIFAR-10, CIFAR-100 and ImageNetV2; upper panels raw, lower panels residual, after "
           "the additive model main effects are removed from both matrices. Each panel prints the Spearman r and "
           "pair count n.")


def panel(deg, d, key, row, rk, c, fx, fy, fw, fh, face):
    """One flat scatter plot in the rectangle (fx, fy, fw, fh) of a column card."""
    import math as _m
    dd = d[key]
    rs = dd["rs_h"] if rk == "raw" else dd["rs_r"]
    xs = dd["t"] if rk == "raw" else dd["tr"]
    ys = dd["c"] if rk == "raw" else dd["cr"]
    title = dd["title"] if rk == "raw" else "residual"
    T(f"ti{row}{c}", fx + 1.2, fy + 0.6, [[(title, "sb")]], size=Z.S8, cont=face,
      color="ink" if rk == "raw" else "muted")
    T(f"tn{row}{c}", fx + fw - 1.2, fy + 0.6, [f"r = {rs:.2f}, n = {dd['pairs']}"], size=Z.S8, align="r", cont=face)
    x0, x1 = fx + 9.6, fx + fw - 4.2
    y0, y1 = fy + fh - 7.0, fy + 1.0 + lh(Z.S8) + 1.6
    lo_x, hi_x = float(xs.min()), float(xs.max())
    lo_y, hi_y = float(ys.min()), float(ys.max())
    px, py = (hi_x - lo_x) * 0.05, (hi_y - lo_y) * 0.06
    sx = Z.Olcek(lo_x - px, hi_x + px, x0, x1)
    sy = Z.Olcek(lo_y - py, hi_y + py, y0, y1)

    def nice(lo, hi, n=3):
        step = (hi - lo) / n
        mag = 10 ** _m.floor(_m.log10(step))
        step = min((1, 2, 5, 10), key=lambda s_: abs(s_ * mag - step)) * mag
        a = _m.ceil(lo / step) * step
        out = []
        while a <= hi + 1e-9:
            out.append(round(a, 6))
            a += step
        return out
    xt = nice(lo_x - px, hi_x + px)
    yt = nice(lo_y - py, hi_y + py)
    dx_ = max(0, -_m.floor(_m.log10(xt[1] - xt[0]) + 1e-9)) if len(xt) > 1 else 1
    dy_ = max(0, -_m.floor(_m.log10(yt[1] - yt[0]) + 1e-9)) if len(yt) > 1 else 1
    xl = [Z.fmt(v, dx_) for v in xt]
    if len(xt) > 1 and sx(xt[1]) - sx(xt[0]) < max(Z.tw([t_], Z.S8) for t_ in xl) + 1.2:
        # second round: labels touched at this tick spacing; every tick stays, every other one is labelled
        k0 = min(range(2), key=lambda k_: abs(xt[k_]) if True else 0)
        xl = [t_ if (i - k0) % 2 == 0 else None for i, t_ in enumerate(xl)]
    Z.kot(f"ax{row}{c}", x0, x1, y0 + 0.5, sx, xt, xl, cont=face)
    Z.kot_dikey(f"ay{row}{c}", x0 - 0.6, y0, y1, sy, yt, [Z.fmt(v, dy_) for v in yt], cont=face)
    order = sorted(range(len(xs)), key=lambda i: LOOK[str(dd["typ"][i])][2])
    for i in order:
        mk, ck, sz, _ = LOOK[str(dd["typ"][i])]
        fill = vf.tint_of(ck)[0] if ck == "notr" else vf.C[ck]
        edge = vf.tint_of(ck)[1] if ck == "notr" else Z.soft(vf.C[ck], 0.35)
        Z.isaret(f"p{row}{c}_{i}", sx(float(xs[i])), sy(float(ys[i])), mk, fill=fill, edge=edge, size=sz,
                 group=f"pts{row}{c}")
    if row == 0:
        lh_, lr_, l2 = dd["foy"]
        deg.append(Z.ev(f"{key} raw Spearman", dd["rs_h"], dd["kaynak"], "sinamalar.ham.istatistik",
                        f"recomputed == JSON (1e-9) == foy line {lh_} (1e-3); printed 2 dp"))
        deg.append(Z.ev(f"{key} residual Spearman", dd["rs_r"], dd["kaynak"],
                        "sinamalar.ana_etki_artik.istatistik", f"recomputed == JSON == foy line {lr_}; printed 2 dp"))
        deg.append(Z.ev(f"{key} pairs", dd["pairs"], dd["kaynak"], "sinamalar.ham.cift_sayisi", f"== foy line {lh_}"))
        for nm, arr, kp in (("c", dd["c"], "c_matrisi upper triangle"), ("log tau", dd["t"], "log_tau_matrisi upper triangle"),
                            ("c residual", dd["cr"], "ana_etki_artik(c_matrisi)"),
                            ("log tau residual", dd["tr"], "ana_etki_artik(log_tau_matrisi)")):
            deg.append(Z.ev(f"{key} scatter {nm}", [round(float(v), 6) for v in arr], dd["kaynak"], kp,
                            "read as stored or recomputed by the frozen konsey rule; positions"))
        for tk, v in dd["tur"].items():
            deg.append(Z.ev(f"{key} {tk} n", v["n"], dd["kaynak"], "pair type from the cell table",
                            f"count; == foy line {l2}"))


def main():
    d, *_rest = GAV.veri()
    keys = ["cifar10", "cifar100", "imagenetv2"]
    vf.reset(STEM, W, 150.0, naming_step=4, naming_kind="serit")
    # third round (09.11.2026): three flat column cards side by side, top-aligned (no stage plate, no steles in
    # depth). In each column the raw panel sits above, a flat inset strip names the operation ("main effects
    # removed") and the residual panel sits below it; the row strips raw and residual are at the left.
    RS, G, CH = 13.0, 2.0, 36.0
    SW = (W - RS - 1.0 - 2 * G)
    SW = SW / 3
    LG = lh(Z.S8) + 1.4                            # strip height
    OY0 = 1.0
    SH = CH + LG + 1.4 + CH
    deg = []
    faces = {}
    for c in (0, 1, 2):
        fx, fy, fw, fh = Z.duz_kart(f"st{c}", RS + c * (SW + G), OY0, SW, SH, "kutu")
        face = f"st{c}_face"
        lx, ly, lw_, lh2 = Z.duz_kart(f"le{c}", fx + 1.0, fy + CH + 0.4, fw - 2.0, LG, "kap", cont=face)
        T(f"let{c}", lx + lw_ / 2, ly + 0.7, ["main effects removed"], size=Z.S8, color="muted", align="c",
          cont=f"le{c}_face")
        panel(deg, d, keys[c], 0, "raw", c, fx, fy, fw, CH, face)
        top2 = ly + lh2 + 0.4
        panel(deg, d, keys[c], 1, "res", c, fx, top2, fw, fy + fh - top2 - 1.6, face)
        faces[c] = (fx, fy, fw, fh, top2)
    # row strips at the left, level with the panels
    fx, fy, fw, fh, top2 = faces[0]
    T("rs0", 0.8, fy + CH / 2 - lh(Z.S8) / 2, [[("raw", "sb")]], size=Z.S8)
    T("rs1", 0.8, (top2 + fy + fh) / 2 - lh(Z.S8) / 2, [[("residual", "sb")]], size=Z.S8)
    OY = OY0 + SH
    T("axx", RS + 1.5 * SW + G, OY + 1.4, [[("x: log ", "r"), ("τ̄", "r@DejaVuSans"),
                                            (" (raw) or its residual;  y: input-gradient cosine c (raw) or its "
                                             "residual", "r")]], size=Z.S8, color="muted", align="c")
    yl = OY + 2.4 + lh(Z.S8)
    # bulgu 5 (08.11): the key rule, the 1.5 pt (vurgu) line between scene and key (as Figures 7, 13, 16)
    vf.seg("rule", (1.0, yl - 0.5), (W - 1.0, yl - 0.5), vf.C["frame"], vf.LW["vurgu"])
    x = 1.0
    for tk in ("CNN-CNN", "T-T", "mixed"):
        mk, ck, sz, lab = LOOK[tk]
        fill = vf.tint_of(ck)[0] if ck == "notr" else vf.C[ck]
        edge = vf.tint_of(ck)[1] if ck == "notr" else Z.soft(vf.C[ck], 0.35)
        Z.isaret(f"lg_{tk}", x + 1.2, yl + lh(Z.S8) / 2, mk, fill=fill, edge=edge, size=2.0)
        T(f"lgt_{tk}", x + 3.0, yl, [lab], size=Z.S8)
        x += 3.0 + Z.tw([lab], Z.S8) + 3.0
    T("lgp", x + 2.0, yl, ["every permutation p is at its floor"], size=Z.S8, color="muted")
    for _pid in ["rs0", "rs1"] + [f"ti0{c}" for c in range(3)]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    ents = {}
    return Z.bitir(
        STEM, message="Input-gradient cosine rises with symmetric similarity on all three data sets, raw and after "
                      "removing model main effects.", kind=KIND, panels=6, caption=CAPTION,
        sablon="ortak_satirli_katlar", tur="veri", degerler=deg, kanit_ek={},
        manifest={"entities": ents, "sahne_kalibi": "yok (uc duz sutun karti, ucuncu tur)",
                  "panel_adlari": ["raw", "residual", "CIFAR-10", "CIFAR-100", "ImageNetV2"],
                  "derinlik_ekseni": "none: flat column cards; the processing step is the inset strip between the raw and the residual panel"},
        denge={"panel_basina_bir_iddia": (True, "each panel is one data set and one step (raw or residual)")},
        n_exempt_reason="each panel prints its pair count n", okunan_ek=[d[k]["kaynak"] for k in keys])


if __name__ == "__main__":
    sys.exit(main())
