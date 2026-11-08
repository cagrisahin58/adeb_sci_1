#!/usr/bin/env python
"""z_cells_interaction (Fig. 9 v2, Üslup Z): the two-by-two cells on CIFAR-10 as a three-floor tower.

    python paper/figures_v2/z_cells_interaction.py [--check] [--bak]

Single column. Three floor cards (panel similarity sigma, direction rho, vulnerability omega), each an upright
card of the one dimetric view, are stacked; two posts behind them stand at the scratch and ImageNet positions,
so the categorical axis all floors share is a structural member. Each floor carries a flat 2D interaction plot:
cell means joined by a line (ViT-Tiny triangles, ResNet-18 224 px circles), single runs as small open marks,
the three R32 bridge runs as diamonds on their own position (sigma and rho only; R32 omega is not in the
reference sheet), the registered +-0.10 band on rho, the H1 and H2 estimates printed on sigma. Values are
positions on a flat face (each floor's own scale). Data: the v1 rule paper/figures/charts/fig_cells_interaction.py
veri() (results/q1 B4 model table, sheet lines 1496-1595, 1745). Naming: step 4 (title strips, no letters).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
CI = Z.yukle("paper/figures/charts/fig_cells_interaction.py", "v1_cells_interaction")

STEM = "z_cells_interaction"
KIND = "single"
W = vf.page_width(KIND)
FLOORS = [("sigma", "Panel similarity σ", "vurgu2", (-1.0, -0.9, -0.8, -0.7)),
          ("rho", "Direction ρ", "vurgu4", (-0.1, 0.0, 0.1)),
          ("omega", "Vulnerability ω = log w", "muted", (3.9, 4.0))]
CAPTION = ("Two-by-two cells on CIFAR-10 as a three-floor tower. Floors Panel similarity σ, Direction ρ and "
           "Vulnerability ω share the posts at scratch and ImageNet; lines join cell means (split-half, log scale), "
           "open marks are runs, diamonds the R32 bridge. σ prints A(σ, scr) (H1) and I(σ) (H2); ρ carries the "
           "±0.10 band. Values are positions on each floor.")


def main():
    D, foy, okunan = CI.veri()
    runs, r32, val, cm, A, I, delta = D["runs"], D["r32"], D["val"], D["cm"], D["A"], D["I"], D["delta"]
    vf.reset(STEM, W, 120.0, naming_step=4, naming_kind="serit")
    XL, XR = 13.5, W - 3.0
    CH, GAP, TCK = 27.0, 5.0, 2.2
    OY = 4.0 + 3 * CH + 2 * GAP + 2.0
    S = Z.Sahne(XL, OY)
    xs = {"r32": XL + 16.0, "scr": XL + 34.0, "in": XL + 58.0}

    def wx(xpage, depth=0.0):
        a = (xpage - XL) / S.u_page
        return S.u[0] * a + S.n[0] * depth, S.u[1] * a + S.n[1] * depth
    H = 3 * CH + 2 * GAP
    DEP = 3.4                                      # the posts stand DEP mm behind the floor faces
    dy_dep = -(S.n[0] * DEP * S.ax["w"][1] + S.n[1] * DEP * S.ax["d"][1])   # page rise of that depth
    rise_sl = -(S.n[0] * TCK * S.ax["w"][1] + S.n[1] * TCK * S.ax["d"][1])  # page rise of a floor's top sliver
    for k in ("scr", "in"):                        # only the post pieces visible in the gaps are drawn
        X, Y = wx(xs[k] - 1.1, DEP)
        for g in range(3):
            zlo = g * (CH + GAP) + CH + rise_sl - dy_dep
            hh = (GAP - rise_sl) if g < 2 else 1.6
            Z.kart(S, f"post_{k}{g}", X, Y, zlo, 2.2, hh, "govde_panel", t=2.0, shadow=False, group="tower")
    col = {"vit": vf.C["vurgu3"], "res": vf.C["vurgu1"], "r32": vf.C["vurgu5"]}
    deg = []
    for f, (q, title, tcol, ticks) in enumerate(FLOORS):
        Zb = (2 - f) * (CH + GAP)
        fx, fy, fw, fh = Z.kart(S, f"fl{f}", 0.0, 0.0, Zb, XR - XL, CH, "kutu", t=TCK, group=f"fl{f}",
                                    shadow=(f == 2), k=(0.12, 0.08))
        face = f"fl{f}_face"
        tc = vf.C[tcol] if tcol in vf.C else tcol
        Z.isaret(f"tsq{f}", fx + 2.2, fy + 0.8 + lh(Z.S8) / 2, "s", fill=tc, edge=tc, size=2.0, group=f"fl{f}")
        T(f"ti{f}", fx + 3.9, fy + 0.8, [[(title, "sb")]], size=Z.S8, cont=face)
        nrun = sum(len(runs[c]) for c in ("V-scr", "V-IN", "R224-scr", "R224-IN")) + (len(r32) if q != "omega" else 0)
        T(f"tn{f}", fx + fw - 1.2, fy + 0.8, [f"n = {nrun} runs"], size=Z.S8, color="muted", align="r", cont=face)
        vals = [val[m][q] for c in runs for m in runs[c] if (q != "omega" or c != "C1-R32")]
        vals += [cm[c][q] for c in ("V-scr", "V-IN", "R224-scr", "R224-IN")]
        if q == "rho":
            vals += [-delta, delta]
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.08
        y0, y1 = fy + fh - 2.2, fy + 1.0 + lh(Z.S8) + 1.6
        sc = Z.Olcek(lo - pad, hi + pad, y0, y1)
        if q == "rho":
            band = [(fx + 10.7, sc(delta)), (fx + fw - 0.8, sc(delta)), (fx + fw - 0.8, sc(-delta)), (fx + 10.7, sc(-delta))]
            vf.poly("band", band + [band[0]], fill=vf.tint_of("ton_4")[0],
                    line=None, role="deco", container=face)
            vf.seg("zero", (fx + 10.7, sc(0.0)), (fx + fw - 0.8, sc(0.0)), vf.C["frame"], vf.LW["ince"], dash=True)
            T("bandl", fx + fw - 2.2, sc(delta) + 0.8, ["±0.10 band"], size=Z.S8, color="muted", align="r", cont="band")
        Z.kot_dikey(f"ax{f}", fx + 10.2, y0 + 0.6, y1 - 0.6, sc, list(ticks),
                    [Z.fmt(t_, 2 if q == "rho" else 1) for t_ in ticks], cont=face)
        for arch, cs, mk, dx_m, dx_r in (("vit", ("V-scr", "V-IN"), "^", -3.2, -7.0), ("res", ("R224-scr", "R224-IN"), "o", 3.2, 6.4)):
            pts = []
            for c, key in zip(cs, ("scr", "in")):
                x = xs[key] + dx_m
                pts.append((x, sc(cm[c][q])))
                for j, m in enumerate(runs[c]):
                    xr_ = xs[key] + dx_r + (j * 1.6 if arch == "res" else -j * 1.6)
                    Z.isaret(f"r{f}_{m}", xr_, sc(val[m][q]), mk, fill=None, edge=col[arch], size=1.4,
                             group=f"fl{f}")
            vf.seg(f"l{f}_{arch}", pts[0], pts[1], col[arch], vf.LW["vurgu"])
            for j, (x, y) in enumerate(pts):
                Z.isaret(f"m{f}_{arch}{j}", x, y, mk, fill=col[arch], edge=Z.soft(col[arch], 0.3), size=2.2,
                         group=f"fl{f}")
        if q != "omega":
            for j, m in enumerate(r32):
                Z.isaret(f"d{f}_{m}", xs["r32"] - 2.0 + j * 2.0, sc(val[m][q]), "D", fill=None, edge=col["r32"],
                         size=1.6, group=f"fl{f}")
        if q == "sigma":
            T("est", fx + fw - 1.2, sc(-0.88), [f"A(σ, scr) = {Z.fmt(A, 3)}", f"I(σ) = {Z.fmt(I, 3, plus=True)}"],
              size=Z.S8, align="r", cont=face)
    yb = OY + 1.2
    for key, lab in (("r32", "R32"), ("scr", "scratch"), ("in", "ImageNet")):
        T(f"x_{key}", xs[key], yb, [lab], size=Z.S8, align="c", color="muted")
    yl = yb + lh(Z.S8) + 1.2
    x = 1.0
    for key, mk, lab, fill in (("vit", "^", "ViT-Tiny mean", True), ("res", "o", "ResNet-18 (224) mean", True),
                               ("r32", "D", "R32 run", False)):
        Z.isaret(f"lg_{key}", x + 1.1, yl + lh(Z.S8) / 2, mk, fill=col[key] if fill else None, edge=col[key], size=2.0)
        T(f"lgt_{key}", x + 2.6, yl, [lab], size=Z.S8)
        x += 2.6 + Z.tw([lab], Z.S8) + 2.0
    yl += lh(Z.S8) + 0.4
    Z.isaret("lg_open", 2.1, yl + lh(Z.S8) / 2, "o", fill=None, edge="ink", size=1.4)
    T("lgt_open", 3.6, yl, ["open: single run; w in %; R32 ω not in the sheet"], size=Z.S8)
    for _pid in [f"ti{i}" for i in range(3)]:          # the panel titles are the strips of naming step 4
        vf.note_naming(_pid, "strip")
    Z.sayfa_sigdir()
    for m, n in CI.FOY_RUN.items():
        for k in D["q"]:
            deg.append(Z.ev(f"run {m} {k}", val[m][k], CI.J4P, f"b4.model_tablosu.{m}.yari_log.{k}",
                            f"read as stored; == foy line {n} (3 dp); position on the floor"))
    for cc, n in CI.FOY_CELL.items():
        for k in D["q"]:
            deg.append(Z.ev(f"cell {cc} mean {k}", cm[cc][k], CI.J4P, f"b4.model_tablosu.<runs of {cc}>.yari_log.{k}",
                            f"mean of the cell's runs; == foy line {n} (3 dp)"))
    for m in r32:
        for k in ("sigma", "rho"):
            deg.append(Z.ev(f"R32 run {m} {k}", val[m][k], CI.J4P, f"b4.model_tablosu.{m}.yari_log.{k}",
                            "read as stored; B2 identities with foy 1588/1593/1595 (1e-9)"))
    deg.append(Z.ev("A sigma scr (H1)", A, CI.J4P, "b4.F_B4.karsitliklar.H1.kestirim", "read; == foy line 1526; printed 3 dp"))
    deg.append(Z.ev("I sigma (H2)", I, CI.J4P, "b4.F_B4.karsitliklar.H2.kestirim", "read; == foy line 1527; printed 3 dp"))
    deg.append(Z.ev("delta band", delta, CI.J4P, "meta.delta", "read; == foy line 1532 text"))
    deg.append(Z.ev("runs sigma/rho", sum(len(v) for v in runs.values()), CI.HTP, "modeller.<m>.hucre", "count"))
    ents = {"vit": "#" + col["vit"], "r224": "#" + col["res"], "r32": "#" + col["r32"]}
    return Z.bitir(
        STEM, message="ViT-Tiny's panel similarity rises with ImageNet initialization while ResNet-18's stays flat; "
                      "rho and omega move far less.", kind=KIND, panels=3, caption=CAPTION,
        sablon="ortak_satirli_katlar", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan},
        manifest={"entities": ents, "sahne_kalibi": "kule",
                  "panel_adlari": ["Panel similarity σ", "Direction ρ", "Vulnerability ω = log w"],
                  "derinlik_ekseni": "none: floor thickness; the posts stand behind the floors",
                  "ikiz_kodlama": "values are positions on each flat floor card, read on its own scale"},
        denge={"panel_basina_bir_iddia": (True, "each floor shows one term across the two-by-two cells")},
        n_exempt_reason="each floor prints its run count in the title strip", okunan_ek=[CI.J4P, CI.J2P, CI.HTP])


if __name__ == "__main__":
    sys.exit(main())
