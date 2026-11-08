#!/usr/bin/env python
"""z_design_recipe (Fig. 2 v2, Üslup Z): the architecture-by-initialization design as a four-drawer card cabinet.

    python paper/figures_v2/z_design_recipe.py [--check] [--bak]

Single column. The cabinet's front is the 2 x 2 design (rows ViT-Tiny and ResNet-18 224 px, columns scratch and
ImageNet init.); each drawer is one cell, pulled out a little: its front carries the cell name, the clean stage
(epochs, learning rate) and the seeds, and inside the open drawer every run is an index card (V-scr three, the
others two). A low wide drawer under the cabinet is the R32 bridge with its own recipe and three cards; a sign on
top of the cabinet carries the AT recipe the four cells share. Depth carries the runs (index cards in seed order).
Every value comes from results/q1/konsey_b3_tarif.json through the v1 rule paper/figures/visio/fig_design_recipe.py
(get, stage, foy_checks against sheet sections M13.1 and M9.1); the 7x7 stem from src/models/r224.py.
Naming: step 6 (letterless strips and a convention sign).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
DR = Z.yukle_sema("paper/figures/visio/fig_design_recipe.py", "v1_design_recipe")

STEM = "z_design_recipe"
KIND = "single"
W = vf.page_width(KIND)
CAPTION = ("Architecture-by-initialization design as a card cabinet. On CIFAR-10 the drawer rows ViT-Tiny and "
           "ResNet-18 cross the columns scratch (random init.) and ImageNet init.; each drawer gives its clean stage "
           "(epochs, learning rate) and seeds, one index card per run. The R32 bridge drawer keeps its own recipe; "
           "the sign on top is the AT recipe of the four cells.")


def main():
    foy, _ab = DR.foy_checks()
    vf.reset(STEM, W, 150.0, naming_step=6)
    OX, OY = 2.0, 120.0
    S = Z.Sahne(OX, OY)
    S8 = Z.S8
    LH = lh(S8)
    CW = W - OX - 6.0                       # cabinet face width
    DW, DG, P = (CW - 3.0 * 2 - 2.0) / 2, 3.6, 4.0
    DH = 3 * LH + 2.2                       # drawer front height
    RH = 2 * LH + 3.2                       # row header, two lines, clear of the index cards below
    rows = [("ViT-Tiny", "govde_vit", ("V-scr", "V-IN")), ("ResNet-18", "govde_res", ("R224-scr", "R224-IN"))]
    stem7, stem7_line = DR.stem_r224()
    # --- R32 bridge drawer (low, wide) at the bottom
    s32 = DR.stem_r32()
    c = "C1-R32"
    L32 = DR.cell_lines(c)
    inp = DR.get("hucreler.C1-R32.girdi_hatti.girdi").split(" ")[0].replace("x", "×")
    clean = (f"clean: {DR.stage(c, 'temiz', 'epok_bayragi')} ep, {DR.stage(c, 'temiz', 'eniyileyici_eniyileyici')} "
             f"lr {DR.num(DR.stage(c, 'temiz', 'eniyileyici_lr_etkin'))}, momentum "
             f"{DR.num(DR.stage(c, 'temiz', 'eniyileyici_momentum'))}")
    atl = (f"AT: {DR.stage(c, 'AT', 'eniyileyici_eniyileyici')} lr {DR.num(DR.stage(c, 'AT', 'eniyileyici_lr_etkin'))}, "
           f"batch {DR.stage(c, 'AT', 'batch')}, cap {DR.stage(c, 'AT', 'epok_bayragi')} ep")
    lines32 = [[(f"R32 bridge, {L32['seeds']}", "sb")], f"ResNet-18, {s32} stem, no max-pool, {inp}", clean, atl]
    BH = 4 * LH + 2.2
    X, Y = Z.un(S, 0.0, 0.0)
    Z.kart(S, "brbox", X, Y, 0.0, CW, BH + 2.0, "notr", t=8.0, shadow=False, group="br")
    X, Y = Z.un(S, 1.5, -P)
    bx, by, bw, bh = Z.kart(S, "brd", X, Y, 1.0, CW - 3.0, BH, "govde_r32", t=P, shadow=False, group="brd",
                            cont="brbox_face")
    for j in range(3):                       # index cards in the bridge drawer
        X, Y = Z.un(S, 10.0, -P + (j + 1) * P / 4.0)
        Z.kart(S, f"brc{j}", X, Y, 1.0 + BH, CW - 23.0, 1.8, "kutu", t=0.25, shadow=False, group=f"brc{j}",
               cont="brbox_face")
    X, Y = Z.un(S, CW - 12.0, -P - 0.8)
    Z.kart(S, "mb32", X, Y, 2.4, 5.0, 6.0, "kutu", t=1.6, shadow=False, group="mb32", cont="brd_face")
    for i, ln in enumerate(lines32):
        T(f"br_t{i}", bx + 1.4, by + 1.0 + i * LH, [ln] if isinstance(ln, str) else [ln], size=S8, cont="brd_face")
    # --- the cabinet with four drawers
    z0 = BH + 2.0
    CH = LH + 1.0 + 2 * (RH + DH + DG) + 3.4
    X, Y = Z.un(S, 0.0, 0.0)
    cx, cy, cw_, ch_ = Z.kart(S, "cab", X, Y, z0, CW, CH, "govde_panel", t=8.0, shadow=False, group="cab")
    for r, (arch, tint, cells) in enumerate(rows):
        zr = z0 + CH - 1.0 - LH - (r + 1) * (RH + DH + DG) + DG
        model = DR.get(f"hucreler.{cells[0]}.girdi_hatti.model")
        inp_r = DR.get(f"hucreler.{cells[0]}.girdi_hatti.girdi").replace("->", " to ").replace(" bilinear buyutme", "")
        extra = f", {stem7} stem" if tint == "govde_res" else ""
        hy = OY - (zr + DH + RH)
        T(f"rowh{r}", cx + 1.4, hy + 0.2, [[(arch + ": ", "sb"), (f"{model}{extra},", "r")], [(f"input {inp_r}", "r")]],
          size=S8, cont="cab_face")
        for cc, cell in enumerate(cells):
            Lc = DR.cell_lines(cell)
            xo = 3.0 + cc * (DW + 2.0)
            # the dark slot behind the pulled-out drawer
            sx, sy = cx + xo, OY - zr - DH
            slot = [(sx, sy - 0.2), (sx + DW, sy - 0.2), (sx + DW, sy + DH), (sx, sy + DH)]
            vf.poly(f"slot{r}{cc}", slot + [slot[0]], fill=vf.tint_of("golge")[0], line=None, role="deco",
                    container="cab_face")
            runs = list(DR.H[cell]["kosular"])
            X, Y = Z.un(S, xo, -P)
            dx, dy, dw, dh = Z.kart(S, f"d{r}{cc}", X, Y, zr, DW, DH, tint, t=P, shadow=False, group=f"d{r}{cc}",
                                    cont=f"slot{r}{cc}")
            for j in range(len(runs)):
                X, Y = Z.un(S, xo + 3.0 + 1.6 * j, -P + (j + 1) * P / (len(runs) + 1))
                Z.kart(S, f"dc{r}{cc}{j}", X, Y, zr + DH, DW - 12.0, 1.8 + 0.7 * j, "kutu", t=0.25, shadow=False,
                       group=f"dc{r}{cc}{j}", cont="cab_face")
            face = f"d{r}{cc}_face"
            # a small model body on the drawer front: the cell's network (3D object, not an icon)
            X, Y = Z.un(S, xo + DW - 8.0, -P - 0.8)
            Z.kart(S, f"mb{r}{cc}", X, Y, zr + 1.6, 5.0, 5.6, "kutu", t=1.6, shadow=False, group=f"mb{r}{cc}",
                   cont=face)
            T(f"dt{r}{cc}", dx + 1.4, dy + 0.9, [[(Lc["title"], "sb")]], size=S8, cont=face)
            T(f"dl{r}{cc}", dx + 1.4, dy + 0.9 + LH, [Lc["clean"], Lc["seeds"]], size=S8, cont=face)
            if Lc["init"]:
                DR.CAPTION_MOVED[cell] = Lc["init"]
    # column heads above the cabinet
    yh = OY - z0 - CH + 0.6
    for cc, lab in enumerate(("scratch (random init.)", "ImageNet init.")):
        T(f"colh{cc}", cx + 3.0 + cc * (DW + 2.0) + 1.4, yh, [[(lab, "sb")]], size=S8, color="muted",
          cont="cab_face")
    # --- the AT sign standing on top of the cabinet
    cst = "V-IN"
    mix = DR.get("ortak.at_kaybi.mix_ratio")
    items = [f"PGD-{DR.stage(cst, 'AT', 'pgd_adim')}, ε {DR.stage(cst, 'AT', 'eps_ifade')}, "
             f"α {DR.stage(cst, 'AT', 'alpha_ifade')}, mix {DR.num(mix)}",
             f"{DR.stage(cst, 'AT', 'eniyileyici_eniyileyici')} lr {DR.num(DR.stage(cst, 'AT', 'eniyileyici_lr_etkin'))}, "
             f"wd {DR.num(DR.stage(cst, 'AT', 'eniyileyici_agirlik_azaltma'))}, batch {DR.stage(cst, 'AT', 'batch')}",
             f"patience {DR.stage(cst, 'AT', 'sabir')}, cap {DR.stage(cst, 'AT', 'epok_tavani')} ep "
             f"(V-scr {DR.stage('V-scr', 'AT', 'epok_bayragi')})"]
    SH = (len(items) + 1) * LH + 1.8
    zs = z0 + CH + LH + 1.6
    X, Y = Z.un(S, 4.0, 5.0)
    gx, gy, gw, gh = Z.kart(S, "sign", X, Y, zs, CW - 8.0, SH, "kutu", t=1.2, shadow=False, group="sign")
    for j in (0, 1):                        # two posts under the sign, from the cabinet top
        X, Y = Z.un(S, 12.0 + j * (CW - 26.0), 5.6)
        Z.kart(S, f"post{j}", X, Y, z0 + CH, 1.2, zs - z0 - CH, "govde_res", t=0.8, shadow=False, group=f"post{j}")
    T("sg_t", gx + 1.4, gy + 0.9, [[("AT", "sb"), (", shared by the 2×2 cells (R32 in its drawer)", "r")]], size=S8,
      cont="sign_face")
    for i, txt in enumerate(items):
        T(f"sg{i}", gx + 1.4, gy + 0.9 + (i + 1) * LH, [txt], size=S8, color="ink",
          cont="sign_face")
    Z.sayfa_sigdir()
    deg = []
    for path, val in DR.OKUNAN.items():
        if not isinstance(val, str) or val != "(structure)":
            deg.append(Z.ev(path, val, DR.SRC, path, "read as is; formatted with :g"))
    deg.append(Z.ev("timm ResNet-18 stem", "7x7", f"{DR.R224_PY}:{stem7_line}", "docstring 'NxN stem'", "read"))
    ents = {"vit": "#" + vf.C["vurgu3"], "r224": "#" + vf.C["vurgu1"], "r32": "#" + vf.C["vurgu5"]}   # entity hues;
    # the drawer fills are their body tints (style Z govde_*), as in every v2 figure
    return Z.bitir(
        STEM, message="Two architectures cross two initializations in four cells with their own clean stage and "
                      "seeds; the R32 bridge keeps its recipe and all cells share one AT recipe.", kind=KIND,
        panels=6, caption=CAPTION, sablon="tasarim_izgarasi", tur="sematik", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "altyaziya_tasinan": DR.CAPTION_MOVED},
        manifest={"entities": ents, "sahne_kalibi": "kartotek_dolabi",
                  "derinlik_ekseni": "runs: one index card per run inside each drawer, in seed order",
                  "altyaziya_tasinan": DR.CAPTION_MOVED,
                  "denge_muafiyet": {"karakter_cm2": "the figure replaces Table 1 of the paper; each cell's training "
                                                     "settings are its content and every value is read from the recipe file",
                                     "yazi_kutusu_alani": "the settings of five cells and the shared adversarial recipe "
                                                          "are text by nature; the 8 pt floor fixes their line boxes"}},
        denge={"panel_basina_bir_iddia": (True, "each drawer is one design cell"),
               "dogrudan_etiket": (True, "every drawer carries its own name and recipe")},
        n_exempt_reason="runs per cell are drawn as index cards and listed by seed",
        okunan_ek=[DR.SRC, DR.R224_PY, "results/C1_REFERANS_FOYU.md"])


if __name__ == "__main__":
    sys.exit(main())
