#!/usr/bin/env python
"""Study overview (fig:study_overview), style 8, Visio, full width (double), naming step 7.

    python paper/figures/visio/fig_study_overview.py --uslup 8 [--check]

Binding plan: raporlar/visio_2026-10-31/04_cizim_plani.md section 9.1. Template yontem_semasi
(styles/uslup_8/sablonlar.yaml): (a) Trained models, (b) Reference panels, (c) Matrices on a light
band; (d) Registered before measurement and (e) Exact split and contrasts below; a 7 mm key strip.
Panel names stand under each panel ('(a)' regular 9 pt, style 8 panel_alti). Flows between the rows
are labelled thin arrows ('PGD-10', 'split-half, log scale'). Target height 142 mm, ceiling 150 mm.

3D objects (one oblique 25-degree view, depth x0.5, from the style): the four 2 x 2 cells and the two
seed-pair models as blocks, the three panel decks, the transfer-matrix block. Their faces follow the
paper's rule (front = entity hex, right 0.25 and top 0.50 toward white; _yuz_tonlari.py); the key
shows the front-face hue. The figure prints counts only; they are counted from the frozen cell
tables and Mantel files and checked against results/C1_REFERANS_FOYU.md (_icerik_study_overview.py).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _sema_ortak as O  # noqa: E402
from _sema_ortak import vf, bl, gr, gc, gf, lh, tw, T, TW, kutu, yuz_tonlari  # noqa: E402
from _yuz_tonlari import notr_kenar  # noqa: E402

O.baslat()
import _icerik_study_overview as IC  # noqa: E402

STEM = "study_overview"
KIND = "double"
STEP = 7
HEDEF, TAVAN = 142.0, 150.0
C, FOY, OKUNAN = IC.sayilar()
IMG = IC.goruntuler()
S = vf.SMALL
LHS = lh(S)
W = vf.page_width(KIND)
XR = gf(W - 0.5)
FACES = O.yuz_tablosu()
OTHER_IN = C["NmodIN"] - C["PanelIN"]          # ImageNetV2 models outside the robust CNN panel
DIST = {}                                     # label-to-block clearances (plan 9.1: at least 1.0 mm)

CELLS = [("V-scr", "SeedVscr", "vit"), ("V-IN", "SeedVin", "vit"),
         ("R224-scr", "SeedRscr", "r224"), ("R224-IN", "SeedRin", "r224")]
PANELS = [("CIFAR-10", "cifar10", f"{C['PanelCten']} robust CNNs + XCiT-S12", C["PanelCten"]),
          ("CIFAR-100", "cifar100", f"{C['PanelChun']} robust CNNs + {C['SecChun']} secondary", C["PanelChun"]),
          ("ImageNetV2", None, f"{C['PanelIN']} robust CNNs + {OTHER_IN} other models, descriptive",
           C["PanelIN"])]
MODELS = [("CIFAR-10", C["NmodCten"]), ("CIFAR-100", C["NmodChun"]), ("ImageNetV2", C["NmodIN"])]
FAMILIES = [("panel family", "K-a, K-b, K-c", "CIFAR-10"), ("two-by-two family", "H1, H2, H3", "CIFAR-10"),
            ("attack side", "best attack per source", ""), ("masking check", "AutoAttack", ""),
            ("replication", "K-a, K-b, K-c", "CIFAR-100"), ("gradient family", "Mantel tests", "all three"),
            ("ImageNetV2 panel", "descriptive, no decision", "")]
EQ = ["log T = log w", "+ log τ + ½ r"]
EQW = "w vulnerability, τ symmetric similarity, r direction"
PROTOCOL = "Protocol layer: nested conditioning sets (raw, target-correct, both-correct, successful-source); h = −log(1 − T) scale"
KEY = [("vit", "ViT-Tiny"), ("r224", "ResNet-18, 224 pipeline"), ("r32", "ResNet-18, CIFAR stem (R32)"),
       ("panel", "robust CNN panel")]


def block(pid, x, y, w, d, h, ent, cont):
    with yuz_tonlari(ent) as tint:
        return notr_kenar(bl.iso_box(pid, gr(x), gr(y), w, d, h, tint, container=cont))


def gap_to(name, label_x, box_right):
    DIST[name] = round(label_x - box_right, 3)


def lay():
    vf.reset(STEM, W, 150.0, naming_step=STEP, naming_kind="karma")
    f, _ = vf.tint_of("zemin_bandi")
    vf.rect("band", 0.5, 0.5, gf(XR - 0.5), 10.0, fill=f, line=None, role="container", ctype="band")
    flow_gap = gc(tw(["PGD-10"], S) + 3.0)
    top = 2.0
    ax, aw = 2.0, 78.0
    bx, bw = ax + aw + 3.0, 45.0
    cx = bx + bw + flow_gap
    cw = gf(XR - 2.0 - cx)
    # ---------------- (a) models: two dashed inner containers with 3D blocks
    ya = O.panel_alti("pa", "a", "Trained models", ax, top, aw, 10, cont="band")
    kx, kw = ax + 2.0, aw - 4.0
    k1 = kutu("k1", kx, ya, kw, 10, "kutu", cont="pa", dash=True)
    T("k1_t", kx + O.IN, ya + 1.0, ["Architecture × initialization, CIFAR-10"], size=S, color="muted", cont="k1")
    rowh_w = tw([[("ResNet-18", "sb")]], S)
    bw_ = 7.0
    labw = max(tw([[(n, "sb")]], S) for n, _, _ in CELLS)
    cube_w = 7.0 + 5.0 * 0.5 * 0.9063           # w + d * depth_scale * cos 25
    colw = gc(cube_w + 1.0 + labw + 1.25)
    x_c0 = kx + O.IN + rowh_w + 1.0
    cy0 = ya + 1.0 + LHS
    for c, lab in enumerate(("scratch", "ImageNet init.")):
        T(f"k1_c{c}", x_c0 + c * colw, cy0, [lab], size=S, color="muted", cont="k1")
    yy = cy0 + LHS + 0.25
    rows_h = 9.0
    for i, (name, ck, ent) in enumerate(CELLS):
        r, c = divmod(i, 2)
        if c == 0:
            T(f"k1_r{r}", kx + O.IN, yy + r * rows_h + 2.0, [[("ViT-Tiny" if r == 0 else "ResNet-18", "sb")]],
              size=S, cont="k1")
        rec = block(f"c{i}", x_c0 + c * colw, yy + r * rows_h, bw_, 5.0, 7.0, ent, "k1")
        x0, y0, w0, h0 = rec["bbox_mm"]
        lx = gc(x0 + w0 + 1.0)
        T(f"c{i}_t", lx, y0 + 0.25, [[(name, "sb")], [f"{C[ck]} runs"]], size=S, cont="k1")
        gap_to(f"{name} label to its block", lx, x0 + w0)
        if c == 0:
            nxt = x_c0 + colw
            gap_to(f"{name} label to the next block", nxt, lx + labw)
            if nxt - (lx + labw) < 1.0 - 1e-9:
                raise SystemExit(f"{name}: label {nxt - (lx + labw):.2f} mm from the next block (< 1.0)")
    k1["h"] = gc(yy + 2 * rows_h + 0.25 - k1["y"])
    k2y = k1["y"] + k1["h"] + 1.5
    k2 = kutu("k2", kx, k2y, kw, 10, "kutu", cont="pa", dash=True)
    T("k2_t", kx + O.IN, k2y + 1.0, ["Seed pair, CIFAR-10"], size=S, color="muted", cont="k2")
    sy = k2y + 1.0 + LHS + 0.25
    sx = kx + O.IN
    for j, (name, ent, k_, arch) in enumerate((("R32", "r32", "SeedRtt", "ResNet-18"),
                                               ("V-scr", "vit", "SeedVscr", "ViT-Tiny"))):
        rec = block(f"s{j}", sx, sy, 7.0, 5.0, 7.0, ent, "k2")
        x0, y0, w0, h0 = rec["bbox_mm"]
        lx = gc(x0 + w0 + 1.0)
        lab = [[(name, "sb"), (", " + arch, "r")], [f"{C[k_]} runs"]]
        T(f"s{j}_t", lx, y0 + 0.25, lab, size=S, cont="k2")
        gap_to(f"seed pair {name} label to its block", lx, x0 + w0)
        if j == 0:
            sx = gc(max(kx + O.IN + gf((kw - 2 * O.IN) / 2), lx + tw(lab, S) + 2.0))
            gap_to("seed pair R32 label to the next block", sx, lx + tw(lab, S))
    ny = sy + h0 + 0.75
    T("k2_n", kx + O.IN, ny, [f"replicated on CIFAR-100: {C['SeedChunR']} + {C['SeedChunV']} runs"], size=S,
      color="muted", cont="k2")
    k2["h"] = gc(ny + LHS + 1.0 - k2y)
    pa_h = gc(k2y + k2["h"] + 2.0 - top)
    # ---------------- (b) reference panels: one deck per data set, one card per member
    yb = O.panel_alti("pb", "b", "Reference panels", bx, top, bw, pa_h, cont="band")
    dy = yb + 0.25
    for i, (name, img, text, n) in enumerate(PANELS):
        kw_ = dict(front_image=IMG[img]["png"]) if img else {}
        with yuz_tonlari("panel") as tint:
            rec = notr_kenar(bl.iso_stack(f"d{i}", gr(bx + 2.0), gr(dy), n, 9.0, 1.0, 9.0, 0.4, tint,
                                          axis="d", container="pb", **kw_))
        x0, y0, w0, h0 = rec["bbox_mm"]
        tx = gc(x0 + w0 + 1.0)
        gap_to(f"deck {name} label", tx, x0 + w0)
        T(f"d{i}_n", tx, y0, [[(name, "sb")]], size=S, cont="pb")
        th = TW(f"d{i}_t", tx, y0 + LHS, text, bx + bw - O.IN - 0.5 - tx, size=S, cont="pb")
        dy = max(y0 + h0, y0 + LHS + th) + 1.25
    pa_h = gc(max(pa_h, dy + 0.75 - top))
    # ---------------- (c) transfer matrices: one 3D block, its front face ruled n x n
    yc = O.panel_alti("pc", "c", "Matrices", cx, top, cw, pa_h, cont="band")
    with yuz_tonlari("panel") as tint:
        rec = notr_kenar(bl.iso_box("mx", gr(cx + 2.5), gr(yc + 0.5), 16.0, 6.0, 16.0, tint, container="pc"))
    pts = vf.IDS[rec["faces"]["front"]]["pts"][:4]
    (x0_, y0_), (x1_, _), _, (_, y3_) = pts[0], pts[1], pts[2], pts[3]
    n = C["NmodCten"]
    col = rec["outline"].lstrip("#")
    for i in range(1, n):
        fr = i / n
        vf.seg(f"mx_gv{i}", (x0_ + (x1_ - x0_) * fr, y0_), (x0_ + (x1_ - x0_) * fr, y3_), col, vf.USLUP.line_min_pt)
        vf.seg(f"mx_gh{i}", (x0_, y0_ + (y3_ - y0_) * fr), (x1_, y0_ + (y3_ - y0_) * fr), col, vf.USLUP.line_min_pt)
    x0, y0, w0, h0 = rec["bbox_mm"]
    ty = y0 + h0 + 1.0
    ty += TW("mx_t", cx + 2.5, ty, "models per matrix:", cw - 5.0, size=S, color="muted",
             cont="pc")
    for i, (name, nn) in enumerate(MODELS):
        T(f"mx_n{i}", cx + 2.5, ty + i * LHS, [[(name, "sb"), (f" {nn}", "r")]], size=S, cont="pc")
    pa_h = gc(max(pa_h, ty + 3 * LHS + 0.75 - top))
    for p in ("pa", "pb", "pc"):
        vf.IDS[p]["h"] = pa_h
    capb = max(O.panel_alti_yaz(p, cont="band") for p in ("pa", "pb", "pc"))
    band_h = gc(capb + 1.0 - 0.5)
    vf.IDS["band"]["h"] = band_h
    bl.flow("f_bc", "pb", "pc", label="PGD-10", kind="arrow")
    # ---------------- row 2: (d) registered families, (e) the exact split
    y2 = 0.5 + band_h + 6.0
    dx, dw = 0.5, 84.0
    ex = dx + dw + 4.0
    ew = gf(XR - ex)
    yd = O.panel_alti("pd", "d", "Registered before measurement", dx, y2, dw, 10)
    namew = max(tw([[(nm, "sb")]], S) for nm, _, _ in FAMILIES)
    dsw = max(tw([ds], S) for _, _, ds in FAMILIES if ds)
    fy = yd
    for i, (nm, det, ds) in enumerate(FAMILIES):
        T(f"fa{i}_n", dx + 2.5, fy, [[(nm, "sb")]], size=S, cont="pd", w=namew)
        T(f"fa{i}_d", dx + 2.5 + namew + 0.75, fy, [det], size=S, cont="pd")
        if ds:
            T(f"fa{i}_s", dx + dw - 2.5 - dsw, fy, [ds], size=S, color="muted", cont="pd", w=dsw)
        fy += LHS
    py = fy + 0.75
    pk = kutu("prot", dx + 2.5, py, dw - 5.0, 10, "kap", cont="pd")
    # nested-set glyph: four nested frames, largest = raw, smallest = successful-source
    gs = 9.0
    for i in range(4):
        o = i * 1.25
        vf.rect(f"prot_g{i}", gr(dx + 2.5 + O.IN + o), gr(py + 1.0 + o), gs - 2 * o, gs - 2 * o, fill=None,
                line=vf.C["muted"], lw=vf.USLUP.line_min_pt, role="container", ctype="box",
                container="prot" if i == 0 else f"prot_g{i - 1}")
    ph = TW("prot_t", dx + 2.5 + O.IN + gs + 1.5, py + 1.0, PROTOCOL, dw - 5.0 - 2 * O.IN - gs - 2.0, size=S,
            cont="prot")
    pk["h"] = gc(max(ph, gs) + 2.0)
    pd_h = gc(py + pk["h"] + 2.0 - y2)
    ye = O.panel_alti("pe", "e", "Exact split and contrasts", ex, y2, ew, pd_h)
    cg = 13.0                                   # column gap: room for the 'Mantel' label
    qw = gf((ew - 5.0 - cg) / 2)
    lx, rx = ex + 2.5, ex + 2.5 + qw + cg
    # q0 exact split (2 x 2 matrix glyph, w on the diagonal)
    q0 = kutu("q0", lx, ye, qw, 10, "kutu", cont="pe")
    T("q0_h", lx + O.IN, ye + 1.0, [[("exact split per pair", "sb")]], size=S, cont="q0")
    T("q0_e", lx + O.IN, ye + 1.0 + LHS, EQ, size=S, cont="q0")
    side = 7.0
    O.matrix_glyph("q0_m", lx + qw - O.IN - side, ye + 1.0 + LHS + 0.5, side, 2, "q0",
                   diag=vf.mix("FFFFFF", vf.C["panel"], 0.45))
    eh = TW("q0_w", lx + O.IN, ye + 1.0 + 3 * LHS + 0.25, EQW, qw - 2 * O.IN - 0.5, size=S, color="muted",
            cont="q0")
    q0["h"] = gc(1.0 + 3 * LHS + 0.25 + eh + 1.0)
    # gradient box (cosine glyph)
    g_ = kutu("grad", rx, ye, qw, q0["h"], "kutu", cont="pe")
    T("grad_h", rx + O.IN, ye + 1.0, [[("input gradients", "sb")]], size=S, cont="grad")
    gh = TW("grad_t", rx + O.IN, ye + 1.0 + LHS, "cosine c on clean images", qw - 2 * O.IN - 0.5 - 9.0, size=S,
            cont="grad")
    O.cos_glyph("grad_g", rx + qw - O.IN - 7.5, ye + 1.0 + LHS + 0.25, 6.5, "grad")
    g_["h"] = q0["h"] = gc(max(q0["h"], 1.0 + LHS + max(gh, 7.5) + 1.0))
    my = gr(ye + q0["h"] / 2)
    vf.connector("ga", [(rx - 0.5, my), (lx + qw + 0.5, my)], dash=True)
    T("ga_t", lx + qw + 1.0, my - LHS - 0.25, ["Mantel"], size=S, color="muted", cont="pe")
    r2 = ye + q0["h"] + 4.0
    # q1 panel means (a row of member marks and their mean line), q2 contrasts (stacked bar)
    m_ = kutu("q1", lx, r2, qw, 10, "kutu", cont="pe")
    T("q1_h", lx + O.IN, r2 + 1.0, [[("panel means", "sb")]], size=S, cont="q1")
    mh = TW("q1_b", lx + O.IN, r2 + 1.0 + LHS, "per model: σ, ρ, ω = log w", qw - 2 * O.IN - 0.5 - 9.0,
            size=S, cont="q1")
    gx0, gy0 = gr(lx + qw - O.IN - 7.5), gr(r2 + 1.0 + LHS)
    for i, dyv in enumerate((2.5, 0.75, 3.75, 1.5, 3.0)):
        vf.oval(f"q1_p{i}", gx0 + i * 1.5, gy0 + dyv, 1.0, 1.0, fill=vf.C["panel"], line=None, role="mark",
                container="q1", grid=False)
    vf.seg("q1_mean", (gx0 - 0.25, gy0 + 2.8), (gx0 + 7.5, gy0 + 2.8), vf.C["ink"], vf.LW["normal"])
    c_ = kutu("q2", rx, r2, qw, 10, "kutu", cont="pe")
    T("q2_h", rx + O.IN, r2 + 1.0, [[("contrasts", "sb")]], size=S, cont="q2")
    ch = TW("q2_b", rx + O.IN, r2 + 1.0 + LHS, "source gap = symmetric + directional part; cell contrasts",
            qw - 2 * O.IN - 0.5 - 6.0, size=S, cont="q2")
    bx0, by0 = gr(rx + qw - O.IN - 4.0), gr(r2 + 1.0 + LHS)
    vf.rect("q2_b1", bx0, by0, 3.0, 4.5, fill=vf.mix("FFFFFF", vf.C["panel"], 0.30), line=vf.C["muted"],
            lw=vf.USLUP.line_min_pt, role="mark", container="q2")
    vf.rect("q2_b2", bx0, by0 + 4.5, 3.0, 3.0, fill=vf.C["panel"], line=vf.C["muted"], lw=vf.USLUP.line_min_pt,
            role="mark", container="q2")
    m_["h"] = c_["h"] = gc(1.0 + LHS + max(mh, ch, 7.5) + 1.0)
    vf.connector("qa0", [(gr(lx + 8.0), ye + q0["h"] + 0.5), (gr(lx + 8.0), r2 - 0.5)])
    vf.connector("qa1", [(lx + qw + 0.5, gr(r2 + m_["h"] / 2)), (rx - 0.5, gr(r2 + m_["h"] / 2))])
    pe_h = gc(r2 + m_["h"] + 2.0 - y2)
    h2 = max(pd_h, pe_h)
    vf.IDS["pd"]["h"] = vf.IDS["pe"]["h"] = h2
    capd = max(O.panel_alti_yaz("pd"), O.panel_alti_yaz("pe"))
    # the band feeds (e): one labelled arrow from below the band to (e)
    axx = gr(cx + cw - 6.0)
    vf.connector("f_ce", [(axx, 0.5 + band_h + 0.5), (axx, y2 - 0.5)])
    lab = "split-half, log scale"
    T("f_ce_t", axx - 1.0 - tw([lab], S), 0.5 + band_h + 1.0, [lab], size=S, color="muted")
    # key strip (the template's 7 mm lejant): front-face hues, plain conventions
    ky = capd + 1.5
    _, e = vf.tint_of("notr")
    kb = vf.rect("keyb", 0.5, gr(ky), gf(XR - 0.5), 10.0, fill=None, line=e, lw=vf.LW["ince"],
                 role="container", ctype="box")
    keys = [(FACES[k]["on"], lab_) for k, lab_ in KEY]
    kh = O.legend_keys("key", 2.5, ky + 1.0, XR - 5.0, keys, "keyb", size=S)
    kb["h"] = gc(kh + 2.0)
    return gc(ky + kb["h"] + 0.5)


def main():
    h = lay()
    v = O.bitir(h, "Study design: trained models and fixed reference panels give transfer matrices, split "
                   "exactly into vulnerability, symmetric similarity and direction and read by registered "
                   "families.", KIND, 5, n_exempt="model and run counts are printed in the panels",
                sablon="yontem_semasi", hedef=HEDEF, tavan=TAVAN,
                extra={"panel_adlari": ["(a) Trained models", "(b) Reference panels", "(c) Matrices",
                                        "(d) Registered before measurement", "(e) Exact split and contrasts"],
                       "lejant": [lab for _, lab in KEY]})
    if v != "PASS":
        print("layout:", v, "| label clearances:", DIST)
        return 0
    deg = IC.kanit_degerleri(C)
    deg.append(O.ev("ImageNetV2 models outside the robust CNN panel", OTHER_IN, IC.M8,
                    "len(modeller_ortak) - count(birincil_panel)",
                    "NmodIN - PanelIN; PanelIN from raporlar/konsey_2026-10-29/hucre_tablosu_b8.json"))
    for name, d in IMG.items():
        deg.append(O.ev(f"{name} test images", d["indeksler"], d["kaynak"], "b'data'[0:4] (pickle)", d["islem"]))
    O.kanit_yaz(STEM, deg, foy=FOY, okunan=OKUNAN,
                ek={"goruntuler": IMG, "etiket_blok_araligi_mm": DIST,
                    "uc_boyut_yuzleri": {k: FACES[k] for k in ("vit", "r224", "r32", "panel")}},
                girdiler=[IC.HT10, IC.HT100, IC.HT8, IC.M10, IC.M100, IC.M8, IC.J8])
    O.denge_ajan(STEM, 2, {"gercek_goruntu": (True, "the CIFAR-10 and CIFAR-100 decks carry the first four test "
                                                     "images of each set on their front card")})
    print("label clearances (mm):", DIST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
