#!/usr/bin/env python
"""z_gradient_alignment (Fig. 11 v2, Üslup Z): input-gradient alignment against similarity on a two-step stand.

    python paper/figures_v2/z_gradient_alignment.py [--check] [--bak]

Double column. A two-step stand: three upright cards on the ground in front, three on a raised step behind.
The back row is the raw relation (cosine c between input gradients against log tau-bar), the front row the
residual after the additive model main effects are removed from both matrices; columns are CIFAR-10, CIFAR-100
and ImageNetV2. Depth carries the processing step (raw behind, residual in front); the step height only lifts the
back row into view. Each card is a flat scatter plot: pair type by marker shape, colour and size (CNN-CNN stone
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
GAV = Z.yukle("paper/figures/charts/fig_gradient_alignment.py", "v1_gradient_alignment")

STEM = "z_gradient_alignment"
KIND = "double"
W = vf.page_width(KIND)
LOOK = {"mixed": ("s", "notr", 1.0, "mixed"), "CNN-CNN": ("o", "vurgu1", 1.15, "CNN–CNN"),
        "T-T": ("^", "vurgu3", 1.35, "transformer–transformer")}
CAPTION = ("Input-gradient alignment against similarity on a two-step stand. Cosine c between input gradients "
           "against log τ̄ for every model pair on CIFAR-10, CIFAR-100 and ImageNetV2; back row, raw; front row, "
           "residual, with additive model main effects removed. Each card prints the Spearman r and pair count "
           "n; values are positions on the flat cards.")


def main():
    d, *_rest = GAV.veri()
    keys = ["cifar10", "cifar100", "imagenetv2"]
    vf.reset(STEM, W, 140.0, naming_step=4, naming_kind="serit")
    RS, CW, CG, CH = 15.5, 49.0, 2.6, 40.0
    DEP, H1 = 10.0, 36.5
    OX, OY = 1.0, 104.0
    S = Z.Sahne(OX, OY)
    rise = -(S.n[0] * DEP * S.ax["w"][1] + S.n[1] * DEP * S.ax["d"][1])
    # the raised step: a tall block behind the front row
    trib = Z.plaka_un(S, "trib", *Z.un(S, RS - 1.5, 2.0), 3 * CW + 2 * CG + 3.0, DEP + 4.0, H1, tint="sahne",
                      z=H1)
    vf.IDS["trib_front"]["container"] = "trib_top"     # the front row stands before the step
    deg = []
    for row, (rk, rlab, dep, z0, cont) in enumerate((("raw", "raw", DEP / 2 + 3.5, H1, "trib_top"),
                                                    ("res", "residual", 0.0, 0.0, "trib_front"))):
        for c, key in enumerate(keys):
            dd = d[key]
            X, Y = Z.un(S, RS + c * (CW + CG), dep)
            fx, fy, fw, fh = Z.kart(S, f"k{row}{c}", X, Y, z0, CW, CH, "kutu", t=1.4, shadow=(row == 1),
                                    k=(0.03, 0.02), group=f"k{row}{c}", cont=cont)
            face = f"k{row}{c}_face"
            rs = dd["rs_h"] if rk == "raw" else dd["rs_r"]
            xs = dd["t"] if rk == "raw" else dd["tr"]
            ys = dd["c"] if rk == "raw" else dd["cr"]
            T(f"ti{row}{c}", fx + 1.2, fy + 0.6, [[(dd["title"], "sb")]], size=Z.S8, cont=face)
            T(f"tn{row}{c}", fx + fw - 1.2, fy + 0.6, [f"r = {rs:.2f}, n = {dd['pairs']}"], size=Z.S8, align="r",
              cont=face)
            x0, x1 = fx + 9.6, fx + fw - 4.2
            y0, y1 = fy + fh - 7.0, fy + 1.0 + lh(Z.S8) + 1.6
            lo_x, hi_x = float(xs.min()), float(xs.max())
            lo_y, hi_y = float(ys.min()), float(ys.max())
            px, py = (hi_x - lo_x) * 0.05, (hi_y - lo_y) * 0.06
            sx = Z.Olcek(lo_x - px, hi_x + px, x0, x1)
            sy = Z.Olcek(lo_y - py, hi_y + py, y0, y1)
            import math as _m

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
            Z.kot(f"ax{row}{c}", x0, x1, y0 + 0.5, sx, xt, [Z.fmt(v, dx_) for v in xt], cont=face)
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
        # row strip at the left
        rp = S.P(*Z.un(S, RS - 1.5, dep), z0 + CH / 2)
        T(f"rs{row}", 0.8, rp[1] - lh(Z.S8) / 2, [[(rlab, "sb")]], size=Z.S8,
          cont=None)
    T("axx", OX + RS + 1.5 * CW + CG, OY + 1.4, [[("x: log ", "r"), ("τ̄", "r@DejaVuSans"),
                                                  (" (raw) or its residual;  y: input-gradient cosine c (raw) or its "
                                                   "residual", "r")]], size=Z.S8, color="muted", align="c")
    yl = OY + 1.8 + lh(Z.S8)
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
        manifest={"entities": ents, "sahne_kalibi": "iki_basamakli_tribun",
                  "panel_adlari": ["raw", "residual", "CIFAR-10", "CIFAR-100", "ImageNetV2"],
                  "derinlik_ekseni": "processing step: raw on the raised back step, residual in front",
                  "ikiz_kodlama": "values are positions on six flat upright cards"},
        denge={"panel_basina_bir_iddia": (True, "each card is one data set and one step (raw or residual)")},
        n_exempt_reason="each card prints its pair count n", okunan_ek=[d[k]["kaynak"] for k in keys])


if __name__ == "__main__":
    sys.exit(main())
