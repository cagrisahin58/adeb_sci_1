#!/usr/bin/env python
"""Style preview of the study overview (fig:study_overview) in one catalogue style, drawn in Visio.

    python paper/figures/visio/_onizleme_study_overview.py --uslup 8 [--check]

N is 8, H, 5 or 3 (the chosen schematic style and its preview candidates; 5 was skipped by the
montage as TOKEN-ONLY against 8 and 3 is the next style in the liked-distance order,
raporlar/visio_2026-10-31/02_uslup_secimi.md). The content is the same in every style
(_icerik_study_overview.py: counts from the frozen cell tables and Mantel files, checked
against results/C1_REFERANS_FOYU.md; CIFAR test images). The composition follows the
style's own ``yontem_semasi`` template (styles/uslup_<N>/sablonlar.yaml):

* 8 (Madry 2018 / Ma 2021): three panels on a light band, dashed inner containers with
  3D layer blocks (oblique 25, the style's view), detail panel and end-point panel below,
  a 7 mm key strip; labelled thin arrows.
* H (HP Figure 1): a flow band of toned boxes joined by chevrons with embedded pills and
  images, a detail panel and an end-point column below, a letterless conventions strip.
* 5 (Seyyed-Kalantari 2021 / Bulten 2022): the whole figure on a grey canvas, three steps
  left to right joined by labelled connectors, a big-number row and a yellow note strip.

Colours, type sizes, strokes and corners come from the style; the entity hues (ViT,
ResNet-18, panel, sigma, rho) are the paper's (paper/figures/konsey/konsey_ortak.py COL)
and are recorded in the paper palette paper/figures/visio/palettes/adeb_konsey_uslup_<N>.yaml.
Naming: step 7 (mixed), decided before drawing (raporlar/visio_2026-10-31/01_envanter.md
section 7.2; paper/figures/panel_yapisi.yaml).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _vz_ortam  # noqa: E402

_vz_ortam.kur()
import visiofig as vf  # noqa: E402
import bilesenler as bl  # noqa: E402
from motor.figspec.kanit import write_kanit  # noqa: E402

import _icerik_study_overview as IC  # noqa: E402

sys.path.insert(0, "paper/figures/konsey")
import konsey_ortak as K  # noqa: E402

AP = argparse.ArgumentParser(description=__doc__.splitlines()[0])
AP.add_argument("--uslup", required=True, choices=["8", "H", "5", "3"])
ARGS, _ = AP.parse_known_args()
NO = ARGS.uslup
STEM = f"_onizleme_study_overview_uslup_{NO}"
VENUE = "ieee_access"
KIND = "double"
STEP = 7

G = vf.GRID
U = vf.use(uslup=NO, venue=VENUE, palette=f"paper/figures/visio/palettes/adeb_konsey_uslup_{NO}.yaml")
C, FOY, OKUNAN = IC.sayilar()
IMG = IC.goruntuler()
NOTES = []

# the paper's entity hues (konsey_ortak.COL), bound for this scene: flat tints for boxes
# (light fill, entity edge) and a mid tint for 3D faces (the face ladder darkens it)
ENT = {k: K.COL[k].lstrip("#").upper() for k in ("vit", "r224", "r32", "panel", "xcit", "sym", "dir")}
for k, h in ENT.items():
    vf.C[k] = h
    vf.TINT[k] = (vf.mix("FFFFFF", h, 0.12), h)
    vf.TINT[k + "_3b"] = (vf.mix("FFFFFF", h, 0.45), vf.mix(h, "000000", 0.25))


# ------------------------------------------------------------------ helpers
def gr(v):
    return round(v / G) * G


def gc(v):
    return math.ceil(v / G - 1e-9) * G


def gf(v):
    return math.floor(v / G + 1e-9) * G


def lh(size=None):
    return vf.line_h(size)


def tw(spec, size=None, key="r"):
    return gc(max(bl.text_box_w(ln, size) for ln in vf.norm_lines(spec, key)))


def wrap(text, width, size=None, key="r"):
    """Greedy word wrap with the controller's own text measure; returns run lines."""
    out, cur = [], ""
    for word in text.split(" "):
        cand = (cur + " " + word).strip()
        if cur and bl.text_box_w([(cand, key)], size) > width:
            out.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        out.append(cur)
    return [[(t, key)] for t in out]


def T(pid, x, y, spec, *, size=None, color="ink", cont=None, align="l", w=None, key="r"):
    """A text box sized to its lines; returns (w, h)."""
    ln = vf.norm_lines(spec, key)
    ww = gc(w) if w is not None else tw(ln, size)
    h = len(ln) * lh(size)
    vf.text(pid, gr(x), gr(y), ww, h, ln, color=color, size=size, align=align, container=cont)
    return ww, h


def TW(pid, x, y, text, width, *, size=None, color="ink", cont=None, key="r"):
    """Wrapped text in a column ``width`` wide; returns its height."""
    ln = wrap(text, width, size, key)
    T(pid, x, y, ln, size=size, color=color, cont=cont, w=width, key=key)
    return len(ln) * lh(size)


def kutu(pid, x, y, w, h, tint, cont=None, dash=False, rnd=None):
    """A box by the style's kutu rule (frame language, stroke, corner) in a tint."""
    k = vf.USLUP.component("kutu")
    frame = k.get("cerceve") or {"cercevesiz": "dolgu", "ince cerceve": "ince+dolgu",
                                 "dolgu bandi": "dolgu"}[vf.USLUP.cerceve_dili]
    f, e = vf.tint_of(tint)
    vf.rect(pid, gr(x), gr(y), gc(w), gc(h), fill=f if "dolgu" in frame else None,
            line=e if "ince" in frame else None, lw=float(k.get("cizgi_pt", vf.LW["ince"])),
            rnd=rnd if rnd is not None else float(k.get("kose_mm", vf.USLUP.corner_mm)),
            role="container", ctype="box", container=cont, dash=dash)
    return vf.IDS[pid]


def panel(pid, letter, title, x, y, w, h, cont=None):
    vf.panel(pid, letter, title, gr(x), gr(y), gc(w), gc(h), naming="letter" if letter else "none")
    vf.IDS[pid]["container"] = cont
    t = vf.IDS[pid + "_title"]
    a = t["size"]
    t["w"] = gc(vf.line_width_mm(t["lines"][0], max(a, vf.visio_printed_max(a)), t["ls"]) + vf.TEXT_SLACK + 0.05)
    return gc(t["y"] + t["h"] + 1.5)          # content top


def pill(pid, x, y, label, tint, cont, size=None, w=None, key="r"):
    """A small filled tag with its label (a model cell or a count); returns (w, h)."""
    ww = gc(w) if w else gc(tw([[(label, key)]], size) + 3.0)
    hh = gc(lh(size) + 2.0)
    kutu(pid, x, y, ww, hh, tint, cont=cont, rnd=min(1.0, float(vf.USLUP.corner_mm) or 0.0))
    vf.text(pid + "_t", gr(x) + 1.25, gr(y) + 1.0, ww - 2.5, lh(size), [[(label, key)]], size=size,
            container=pid, align="c")
    return ww, hh


def front_grid(pid, rec, n, colour=None):
    """n x n rules on the front face of a 3D box: a transfer matrix of n models."""
    pts = vf.IDS[rec["faces"]["front"]]["pts"][:4]
    (x0, y0), (x1, _), _, (_, y3) = pts[0], pts[1], pts[2], pts[3]
    col = colour or rec["outline"].lstrip("#")
    for i in range(1, n):
        f = i / n
        vf.seg(f"{pid}_gv{i}", (x0 + (x1 - x0) * f, y0), (x0 + (x1 - x0) * f, y3), col, vf.USLUP.line_min_pt)
        vf.seg(f"{pid}_gh{i}", (x0, y0 + (y3 - y0) * f), (x1, y0 + (y3 - y0) * f), col, vf.USLUP.line_min_pt)


def matrix_glyph(pid, x, y, side, n, cont, tint="panel"):
    """A flat n x n matrix glyph (style H keeps its source's 2D boxes)."""
    f, e = vf.tint_of(tint)
    vf.rect(pid, gr(x), gr(y), side, side, fill=f, line=e, lw=vf.USLUP.line_min_pt, role="obstacle",
            container=cont)
    step = side / n
    for i in range(1, n):
        vf.seg(f"{pid}_v{i}", (gr(x) + i * step, gr(y)), (gr(x) + i * step, gr(y) + side), e, vf.USLUP.line_min_pt)
        vf.seg(f"{pid}_h{i}", (gr(x), gr(y) + i * step), (gr(x) + side, gr(y) + i * step), e, vf.USLUP.line_min_pt)


def kanit_yaz():
    deg = IC.kanit_degerleri(C)
    for name, d in IMG.items():
        deg.append({"etiket": f"{name} test images", "deger": d["indeksler"], "kaynak": d["kaynak"],
                    "anahtar_yolu": "b'data'[0:4] (pickle)", "hesap": d["islem"]})
    p = write_kanit(STEM, vf.OUT_DIR, uslup_no=U.no, degerler=deg, records=None)
    k = json.loads(Path(p).read_text(encoding="utf-8"))
    k["foy_karsilastirmasi"] = FOY
    k["okunan_anahtarlar"] = OKUNAN
    k["goruntuler"] = IMG
    k["git"] = K.git_info([IC.HT10, IC.HT100, IC.HT8, IC.M10, IC.M100, IC.M8, IC.J8])
    k["betik"] = "paper/figures/visio/_onizleme_study_overview.py --uslup " + NO
    k["notlar"] = NOTES
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(k, indent=2, ensure_ascii=False) + "\n")


W = vf.page_width(KIND)
XR = gf(W - 0.5)
LHB, LHS = lh(), lh(vf.SMALL)
S = vf.SMALL
IN = 1.5            # text inset from a box edge (the controller asks 1.0, plus the print shift)

CELLS = [("V-scr", "SeedVscr", "vit"), ("V-IN", "SeedVin", "vit"),
         ("R224-scr", "SeedRscr", "r224"), ("R224-IN", "SeedRin", "r224")]
PANELS = [("CIFAR-10", "C10", "cifar10", f"{C['PanelCten']} robust CNNs + XCiT-S12", C["PanelCten"]),
          ("CIFAR-100", "C100", "cifar100", f"{C['PanelChun']} robust CNNs + {C['SecChun']} secondary", C["PanelChun"]),
          ("ImageNetV2", "IN-V2", None, f"{C['PanelIN']} robust CNNs + XCiT-S12; {C['PairsIN']} same-recipe "
                                        f"CNN-transformer pairs + {C['UnpairedIN']} unpaired (descriptive)",
           C["PanelIN"])]
MODELS = [("CIFAR-10", C["NmodCten"]), ("CIFAR-100", C["NmodChun"]), ("ImageNetV2", C["NmodIN"])]
FAMILIES = [("panel family", "K-a, K-b, K-c", "CIFAR-10"), ("two-by-two family", "H1, H2, H3", "CIFAR-10"),
            ("attack side", "best attack per source", ""), ("masking check", "AutoAttack", ""),
            ("replication", "K-a, K-b, K-c", "CIFAR-100"), ("gradient family", "Mantel tests", "all three"),
            ("ImageNetV2 panel", "descriptive, no decision", "")]
EQ1, EQ2 = "log T = log w", "+ log τ + ½ r"
EQW = "w vulnerability, τ symmetric similarity, r direction, per ordered pair"
PROTOCOL = "Protocol layer: conditioning sets nested, raw, target-correct, both-correct, successful-source; h = −log(1 − T) scale"
KEY = [("vit", "ViT-Tiny / transformer"), ("r224", "ResNet-18, ViT pipeline"), ("r32", "ResNet-18, CIFAR stem"),
       ("panel", "robust CNN panel"), ("sym", "symmetric, σ"), ("dir", "directional, ρ")]


def key_rows(pid, x, y, w, cont, cols, size=None):
    """Swatch + label conventions; returns height."""
    cw = gf(w / cols)
    rows = math.ceil(len(KEY) / cols)
    for i, (k, lab) in enumerate(KEY):
        c, r = divmod(i, rows)
        bx, by = x + c * cw, y + r * lh(size)
        vf.rect(f"{pid}_s{i}", gr(bx), gr(by + (lh(size) - 2.0) / 2), 2.0, 2.0, fill=ENT[k], line=None,
                role="mark", container=cont)
        T(f"{pid}_l{i}", bx + 3.0, by, [lab], size=size, cont=cont)
    return rows * lh(size)


# ================================================================== style 8
def lay_8():
    vf.reset(STEM, W, 150.0, naming_step=STEP)
    f, _ = vf.tint_of("zemin_bandi")
    vf.rect("band", 0.5, 0.5, gf(XR - 0.5), 10.0, fill=f, line=None, role="container", ctype="band")
    flow_gap = gc(tw(["PGD-10"], S) + 3.0)
    top = 2.5
    ax, aw = 2.5, 77.0
    bx, bw = ax + aw + 3.0, 45.0
    cx = bx + bw + flow_gap
    cw = gf(XR - 2.0 - cx)
    # (a) models: two dashed inner containers with oblique 3D layer blocks
    ya = panel("pa", "a", "Trained models", ax, top, aw, 10, cont="band")
    kx, kw = ax + 2.0, aw - 4.0
    k1 = kutu("k1", kx, ya, kw, 10, "kutu", cont="pa", dash=True)
    T("k1_t", kx + IN, ya + 1.0, ["Architecture × initialization, CIFAR-10"], size=S, color="muted", cont="k1")
    rowh_w = tw([[("ResNet-18", "sb")]], S)
    colw = gf((kw - 2 * IN - rowh_w - 1.0) / 2)
    cy0 = ya + 1.0 + LHS + 0.25
    for c, lab in enumerate(("scratch", "ImageNet init.")):
        T(f"k1_c{c}", kx + IN + rowh_w + 1.0 + c * colw, cy0, [lab], size=S, color="muted", cont="k1")
    yy = cy0 + LHS + 0.5
    rec = None
    for i, (name, ck, ent) in enumerate(CELLS):
        r, c = divmod(i, 2)
        if c == 0:
            T(f"k1_r{r}", kx + IN, yy + r * 10.0 + 2.0, [[("ViT-Tiny" if r == 0 else "ResNet-18", "sb")]], size=S,
              cont="k1")
        rec = bl.iso_box(f"c{i}", gr(kx + IN + rowh_w + 1.0 + c * colw), gr(yy + r * 10.0), 7.0, 5.0, 7.0,
                         ent + "_3b", container="k1")
        x0, y0, w0, h0 = rec["bbox_mm"]
        T(f"c{i}_t", x0 + w0 + 1.0, y0 + 0.5, [[(name, "sb")], [f"{C[ck]} runs"]], size=S, cont="k1")
    k1["h"] = gc(yy + 20.0 + 0.5 - k1["y"])
    k2y = k1["y"] + k1["h"] + 1.5
    k2 = kutu("k2", kx, k2y, kw, 10, "kutu", cont="pa", dash=True)
    T("k2_t", kx + IN, k2y + 1.0, ["Seed pair, CIFAR-10 and CIFAR-100"], size=S, color="muted", cont="k2")
    sy = k2y + 1.0 + LHS + 0.5
    for j, (name, ent, k_, arch) in enumerate((("R32", "r32", "SeedRtt", "ResNet-18"),
                                               ("V-scr", "vit", "SeedVscr", "ViT-Tiny"))):
        rec = bl.iso_box(f"s{j}", gr(kx + IN + j * gf((kw - 2 * IN) / 2)), gr(sy), 9.0, 5.0, 7.0, ent + "_3b",
                         container="k2")
        x0, y0, w0, h0 = rec["bbox_mm"]
        T(f"s{j}_t", x0 + w0 + 1.0, y0, [[(name, "sb")], [arch], [f"{C[k_]} runs"]], size=S, cont="k2")
    ny = sy + max(h0, 3 * LHS) + 0.75
    T("k2_n", kx + IN, ny, [f"replicated on CIFAR-100: {C['SeedChunR']} + {C['SeedChunV']} runs"], size=S,
      color="muted", cont="k2")
    k2["h"] = gc(ny + LHS + 1.0 - k2y)
    pa_h = gc(k2y + k2["h"] + 2.0 - top)
    # (b) reference panels: one deck per data set, one card per panel member
    yb = panel("pb", "b", "Reference panels", bx, top, bw, pa_h, cont="band")
    dy = yb + 0.25
    for i, (name, short, img, text, n) in enumerate(PANELS):
        kw_ = dict(front_image=IMG[img]["png"]) if img else {}
        rec = bl.iso_stack(f"d{i}", gr(bx + 2.5), gr(dy), n, 9.0, 1.0, 9.0, 0.4, "panel_3b", axis="d",
                           container="pb", **kw_)
        x0, y0, w0, h0 = rec["bbox_mm"]
        tx = gc(x0 + w0 + 1.0)
        T(f"d{i}_n", tx, y0, [[(name, "sb")]], size=S, cont="pb")
        th = TW(f"d{i}_t", tx, y0 + LHS, text, bx + bw - IN - 0.5 - tx, size=S, cont="pb")
        dy = max(y0 + h0, y0 + LHS + th) + 1.5
    pa_h = gc(max(pa_h, dy + 0.5 - top))
    # (c) transfer matrices: one 3D block, its front face ruled n x n
    yc = panel("pc", "c", "Matrices", cx, top, cw, pa_h, cont="band")
    rec = bl.iso_box("mx", gr(cx + 2.5), gr(yc + 0.5), 16.0, 6.0, 16.0, "panel_3b", container="pc")
    front_grid("mx", rec, C["NmodCten"])
    x0, y0, w0, h0 = rec["bbox_mm"]
    ty = y0 + h0 + 1.0
    ty += TW("mx_t", cx + 2.5, ty, "target-correct, PGD-10", cw - 5.0, size=S, color="muted", cont="pc")
    for i, (name, n) in enumerate(MODELS):
        T(f"mx_n{i}", cx + 2.5, ty + i * LHS, [[(name, "sb"), (f" {n}", "r")]], size=S, cont="pc")
    pa_h = gc(max(pa_h, ty + 3 * LHS + 1.5 - top))
    for p in ("pa", "pb", "pc"):
        vf.IDS[p]["h"] = pa_h
    band_h = gc(top + pa_h + 2.0 - 0.5)
    vf.IDS["band"]["h"] = band_h
    bl.flow("f_bc", "pb", "pc", label="PGD-10", kind="arrow")
    # row 2: (d) registered families, (e) the exact split, fed from the band
    y2 = 0.5 + band_h + 7.0
    dx, dw = 0.5, 84.0
    ex = dx + dw + 4.0
    ew = gf(XR - ex)
    yd = panel("pd", "d", "Registered before measurement", dx, y2, dw, 10)
    namew = max(tw([[(n, "sb")]], S) for n, _, _ in FAMILIES)
    dsw = max(tw([ds], S) for _, _, ds in FAMILIES if ds)
    fy = yd
    for i, (n, det, ds) in enumerate(FAMILIES):
        T(f"fa{i}_n", dx + 2.5, fy, [[(n, "sb")]], size=S, cont="pd", w=namew)
        T(f"fa{i}_d", dx + 2.5 + namew + 0.5, fy, [det], size=S, cont="pd")
        if ds:
            T(f"fa{i}_s", dx + dw - 2.5 - dsw, fy, [ds], size=S, color="muted", cont="pd", w=dsw)
        fy += LHS
    py = fy + 1.0
    pk = kutu("prot", dx + 2.5, py, dw - 5.0, 10, "kap", cont="pd")
    ph = TW("prot_t", dx + 2.5 + IN, py + 1.0, PROTOCOL, dw - 5.0 - 2 * IN - 0.5, size=S, cont="prot")
    pk["h"] = gc(ph + 2.0)
    pd_h = gc(py + pk["h"] + 2.0 - y2)
    ye = panel("pe", "e", "Exact split and contrasts", ex, y2, ew, pd_h)
    # e: split box (left) <- dashed Mantel arrow <- gradient box (right); split -> means -> contrasts
    gw = gc(tw(["input-gradient"], S, "sb") + 2 * IN + 0.5)
    sw = gf(ew - 5.0 - gw - 16.0)
    s_ = kutu("q0", ex + 2.5, ye, sw, 10, "kutu", cont="pe")
    T("q0_h", ex + 2.5 + IN, ye + 1.0, [[("exact split per pair", "sb")]], size=S, cont="q0")
    T("q0_e", ex + 2.5 + IN, ye + 1.0 + LHS, [EQ1, EQ2], size=S, cont="q0")
    eh = TW("q0_w", ex + 2.5 + IN, ye + 1.0 + 3 * LHS, EQW, sw - 2 * IN - 0.5, size=S, color="muted", cont="q0")
    s_["h"] = gc(3 * LHS + eh + 2.0)
    gx = ex + ew - 2.5 - gw
    g_ = kutu("grad", gx, ye, gw, s_["h"], "kutu", cont="pe")
    T("grad_h", gx + IN, ye + 1.0, [[("input-gradient", "sb")]], size=S, cont="grad")
    TW("grad_t", gx + IN, ye + 1.0 + LHS, "cosine c on clean images", gw - 2 * IN - 0.5, size=S, cont="grad")
    my = gr(ye + s_["h"] / 2)
    vf.connector("ga", [(gx - 0.5, my), (ex + 2.5 + sw + 0.5, my)], dash=True)
    T("ga_t", ex + 2.5 + sw + 1.0, my - LHS - 0.25, ["Mantel"], size=S, color="muted", cont="pe")
    r2 = ye + s_["h"] + 5.0
    halfw = gf((ew - 5.0 - 6.0) / 2)
    m_ = kutu("q1", ex + 2.5, r2, halfw, 10, "kutu", cont="pe")
    T("q1_h", ex + 2.5 + IN, r2 + 1.0, [[("panel means", "sb")]], size=S, cont="q1")
    mh = TW("q1_b", ex + 2.5 + IN, r2 + 1.0 + LHS, "per model: σ, ρ, ω = log w", halfw - 2 * IN - 0.5, size=S,
            cont="q1")
    c2x = ex + 2.5 + halfw + 6.0
    c_ = kutu("q2", c2x, r2, halfw, 10, "kutu", cont="pe")
    T("q2_h", c2x + IN, r2 + 1.0, [[("contrasts", "sb")]], size=S, cont="q2")
    ch = TW("q2_b", c2x + IN, r2 + 1.0 + LHS, "source gap = symmetric + directional; cell contrasts",
            halfw - 2 * IN - 0.5, size=S, cont="q2")
    m_["h"] = c_["h"] = gc(LHS + max(mh, ch) + 2.0)
    vf.connector("qa0", [(gr(ex + 2.5 + 8.0), ye + s_["h"] + 0.5), (gr(ex + 2.5 + 8.0), r2 - 0.5)])
    vf.connector("qa1", [(ex + 2.5 + halfw + 0.5, gr(r2 + m_["h"] / 2)), (c2x - 0.5, gr(r2 + m_["h"] / 2))])
    pe_h = gc(r2 + m_["h"] + 2.0 - y2)
    h2 = max(pd_h, pe_h)
    vf.IDS["pd"]["h"] = vf.IDS["pe"]["h"] = h2
    # the band feeds (e): one labelled arrow
    axx = gr(cx + cw / 2)
    vf.connector("f_ce", [(axx, 0.5 + band_h + 0.5), (axx, y2 - 0.5)])
    T("f_ce_t", axx - 1.0 - tw(["split-half, log scale"], S), 0.5 + band_h + 1.0, ["split-half, log scale"], size=S,
      color="muted")
    # key strip (the template's 7 mm lejant): plain conventions, not a naming component
    ky = y2 + h2 + 2.0
    _, e = vf.tint_of("notr")
    kb = vf.rect("keyb", 0.5, gr(ky), gf(XR - 0.5), 10.0, fill=None, line=e, lw=vf.LW["ince"],
                 role="container", ctype="box")
    kh = key_rows("key", 2.5, ky + 1.0, XR - 5.0, "keyb", cols=3, size=S)
    kb["h"] = gc(kh + 2.0)
    return gc(ky + kb["h"] + 1.0), 6


# ================================================================== style H
def lay_H():
    vf.reset(STEM, W, 150.0, naming_step=STEP)
    top = 0.5
    ya = panel("pa", "A", "Models, panels and the transfer matrix", 0.5, top, gf(XR - 0.5), 10)
    gap = 4.0
    widths = [27.0, 39.0, 31.0, 27.0, 32.0]
    x = 0.5 + 2.5 + gf((XR - 0.5 - 5.0 - sum(widths) - gap * 4) / 2)
    xs = []
    for w_ in widths:
        xs.append(x)
        x += w_ + gap
    by = ya + 0.25
    heads = ["Seed pair", "Architecture × init.", "Reference panels", "Transfer matrix", "Exact split"]
    tints = ["r32", "vit", "panel", "panel", "sym"]
    boxes = [kutu(f"b{i}", xs[i], by, widths[i], 10, tints[i], cont="pa") for i in range(5)]
    for i in range(5):
        T(f"b{i}_h", xs[i] + IN, by + 1.0, [[(heads[i], "sb")]], cont=f"b{i}")
    cy = by + 1.0 + LHB + 0.5
    bottoms = []
    _, ph = pill("b0_p0", xs[0] + IN, cy, f"R32 · {C['SeedRtt']} runs", "r32", "b0", size=S)
    pill("b0_p1", xs[0] + IN, cy + ph + 1.0, f"V-scr · {C['SeedVscr']} runs", "vit", "b0", size=S)
    nh = TW("b0_n", xs[0] + IN, cy + 2 * ph + 1.75, f"CIFAR-100: {C['SeedChunR']} + {C['SeedChunV']} runs",
            widths[0] - 2 * IN - 0.5, size=S, color="muted", cont="b0")
    bottoms.append(cy + 2 * ph + 1.75 + nh)
    pw = gf((widths[1] - 2 * IN - 1.0) / 2)
    for c, lab in enumerate(("scratch", "IN init.")):
        T(f"b1_c{c}", xs[1] + IN + c * (pw + 1.0), cy, [lab], size=S, color="muted", w=pw, cont="b1")
    for i, (name, ck, ent) in enumerate(CELLS):
        r, c = divmod(i, 2)
        pill(f"b1_p{i}", xs[1] + IN + c * (pw + 1.0), cy + LHS + 0.5 + r * (ph + 1.0), f"{name} {C[ck]}", ent,
             "b1", size=S, w=pw)
    nh = TW("b1_n", xs[1] + IN, cy + LHS + 0.5 + 2 * (ph + 1.0), "runs per cell, CIFAR-10",
            widths[1] - 2 * IN - 0.5, size=S, color="muted", cont="b1")
    bottoms.append(cy + LHS + 0.5 + 2 * (ph + 1.0) + nh)
    iw = 9.0
    vf.image("b2_i0", gr(xs[2] + IN), gr(cy), iw, iw, IMG["cifar10"]["png"], container="b2")
    vf.image("b2_i1", gr(xs[2] + IN + iw + 1.5), gr(cy), iw, iw, IMG["cifar100"]["png"], container="b2")
    ty = cy + iw + 1.0
    lines = [f"C10 {C['PanelCten']} + {C['SecCten']}", f"C100 {C['PanelChun']} + {C['SecChun']}",
             f"IN-V2 {C['PanelIN']} + {C['SecIN']}"]
    T("b2_t", xs[2] + IN, ty, lines, size=S, cont="b2")
    nh = TW("b2_n", xs[2] + IN, ty + 3 * LHS, "robust CNNs + secondary", widths[2] - 2 * IN - 0.5, size=S,
            color="muted", cont="b2")
    bottoms.append(ty + 3 * LHS + nh)
    side = 12.0
    matrix_glyph("b3_m", xs[3] + IN, cy, side, C["NmodCten"], "b3")
    ty = cy + side + 1.0
    nh = TW("b3_t", xs[3] + IN, ty, f"{C['NmodCten']} / {C['NmodChun']} / {C['NmodIN']} models; "
                                     "target-correct, PGD-10", widths[3] - 2 * IN - 0.5, size=S, cont="b3")
    bottoms.append(ty + nh)
    T("b4_e", xs[4] + IN, cy, [EQ1, EQ2], size=S, cont="b4")
    nh = TW("b4_w", xs[4] + IN, cy + 2 * LHS + 0.5, EQW, widths[4] - 2 * IN - 0.5, size=S, color="muted",
            cont="b4")
    bottoms.append(cy + 2 * LHS + 0.5 + nh)
    bh = gc(max(bottoms) + 1.25 - by)
    for b in boxes:
        b["h"] = bh
    for i in range(4):
        bl.chevron(f"ch{i}", gr(xs[i] + widths[i] + gap / 2), gr(by + bh / 2), "h", container="pa")
    pa_h = gc(by + bh + 2.0 - top)
    vf.IDS["pa"]["h"] = pa_h
    y2 = top + pa_h + 1.5
    bw2 = 100.0
    yb = panel("pb", "B", "From pair split to contrasts", 0.5, y2, bw2, 10)
    cx = 0.5 + bw2 + 1.5
    cw = gf(XR - cx)
    yc = panel("pc", "C", "Registered before measurement", cx, y2, cw, 10)
    items = [("panel means", "σ symmetric, ρ directional, ω = log w", "sym"),
             ("contrasts", "source gap = σ part + ρ part; 2 × 2 cell contrasts", "dir"),
             ("input gradients", "cosine c on clean images, Mantel with log τ", "panel")]
    iw_ = gf((bw2 - 5.0 - 2 * gap) / 3)
    ibs = []
    hs = []
    for i, (h_, body, tint) in enumerate(items):
        x0 = 0.5 + 2.5 + i * (iw_ + gap)
        ibs.append(kutu(f"bb{i}", x0, yb, iw_, 10, tint, cont="pb"))
        T(f"bb{i}_h", x0 + IN, yb + 1.0, [[(h_, "sb")]], size=S, cont=f"bb{i}")
        hs.append(TW(f"bb{i}_b", x0 + IN, yb + 1.0 + LHS, body, iw_ - 2 * IN - 0.5, size=S, cont=f"bb{i}"))
    ih = gc(LHS + max(hs) + 2.0)
    for b in ibs:
        b["h"] = ih
    for i in range(2):
        bl.chevron(f"bch{i}", gr(0.5 + 2.5 + (i + 1) * iw_ + i * gap + gap / 2), gr(yb + ih / 2), "h",
                   container="pb")
    py = yb + ih + 1.5
    x0 = 0.5 + 2.5
    for i, (lab, tint) in enumerate((("σ similarity", "sym"), ("ρ direction", "dir"), ("ω vulnerability", "panel"))):
        w_, ph2 = pill(f"bp{i}", x0, py, lab, tint, "pb", size=S)
        x0 += w_ + 1.5
    pb_h = gc(py + ph2 + 2.0 - y2)
    ry = yc
    rh = gc(LHS + 2.0)
    dsw = max(tw([ds], S) for _, _, ds in FAMILIES if ds)
    for i, (n_, det, ds) in enumerate(FAMILIES):
        kutu(f"fr{i}", cx + 2.0, ry, cw - 4.0, rh, "kutu", cont="pc")
        vf.rect(f"fr{i}_bar", gr(cx + 2.75), gr(ry + 0.5), 0.75, gc(rh - 1.0), fill=ENT["panel"], line=None,
                role="mark", container=f"fr{i}")
        T(f"fr{i}_t", cx + 4.25, ry + 1.0, [[(n_, "sb"), ("  " + det, "r")]], size=S, cont=f"fr{i}")
        if ds:
            T(f"fr{i}_s", cx + cw - 2.0 - IN - 0.5 - dsw, ry + 1.0, [ds], size=S, color="muted", cont=f"fr{i}",
              w=dsw)
        ry += rh + 0.75
    pc_h = gc(ry + 1.25 - y2)
    h2 = max(pb_h, pc_h)
    vf.IDS["pb"]["h"] = vf.IDS["pc"]["h"] = h2
    ly = y2 + h2 + 1.5
    items = [[(PROTOCOL.split(";")[0], "r")],
             [(PROTOCOL.split("; ")[1] + "; RobustBench checkpoints frozen before measurement", "r")]]
    bl.legend_strip("lg", "Conventions", 0.5, gr(ly), gf(XR - 0.5), items, cols=1)
    return gc(ly + vf.IDS["lg"]["h"] + 1.0), 4


# ================================================================== style 5
def lay_5():
    vf.reset(STEM, W, 150.0, naming_step=STEP)
    f, _ = vf.tint_of("tuval")
    vf.rect("tuval", 0.5, 0.5, gf(XR - 0.5), 10.0, fill=f, line=None, role="container", ctype="band")
    pad = 3.0
    gap = gc(tw(["PGD-10"], S) + 3.0)
    sw = gf((XR - 0.5 - 2 * pad - 2 * gap) / 3)
    xs = [0.5 + pad + i * (sw + gap) for i in range(3)]
    top = 0.5 + pad
    titles = ["Train and collect", "Measure transfer", "Decide by rules"]
    ys = [panel(f"p{i}", "abc"[i], titles[i], xs[i], top, sw, 10, cont="tuval") for i in range(3)]
    inner = sw - 4.0
    # (a) white boxes: isometric cubes for the cells, decks for the panels
    bx, y = xs[0] + 2.0, ys[0]
    a1 = kutu("a1", bx, y, inner, 10, "kutu", cont="p0")
    hh = TW("a1_h", bx + IN, y + 1.0, "Architecture × initialization", inner - 2 * IN - 0.5, size=S, cont="a1",
            key="sb")
    yy = y + 1.0 + hh + 0.5
    colw = gf((inner - 2 * IN) / 2)
    cell_h = 0.0
    for i, (name, ck, ent) in enumerate(CELLS):
        r, c = divmod(i, 2)
        rec = bl.iso_box(f"c{i}", gr(bx + IN + c * colw), gr(yy + r * cell_h), 5.0, 5.0, 4.0, ent + "_3b",
                         container="a1")
        x0, y0, w0, h0 = rec["bbox_mm"]
        T(f"c{i}_t", x0, y0 + h0 + 0.25, [[(name, "sb"), (f" {C[ck]}", "r")]], size=S, cont="a1")
        cell_h = gc(h0 + 0.25 + LHS + 1.0)
    a1["h"] = gc(yy + 2 * cell_h + 0.25 - y)
    y = y + a1["h"] + 1.5
    a2 = kutu("a2", bx, y, inner, 10, "kutu", cont="p0")
    hh = TW("a2_h", bx + IN, y + 1.0, "Seed pair and reference panels", inner - 2 * IN - 0.5, size=S, cont="a2",
            key="sb")
    hh += TW("a2_s", bx + IN, y + 1.0 + hh, f"R32 {C['SeedRtt']} + V-scr {C['SeedVscr']} runs; CIFAR-100 "
                                             f"{C['SeedChunR']} + {C['SeedChunV']}", inner - 2 * IN - 0.5,
             size=S, color="muted", cont="a2")
    yy = y + 1.0 + hh + 1.0
    dx = bx + IN
    last = yy
    for i, (name, short, img, text, n) in enumerate(PANELS):
        kw_ = dict(front_image=IMG[img]["png"]) if img else {}
        rec = bl.iso_stack(f"d{i}", gr(dx), gr(yy), n, 6.0, 0.6, 6.0, 0.3, "panel_3b", axis="d",
                           container="a2", **kw_)
        x0, y0, w0, h0 = rec["bbox_mm"]
        lab = [[(short, "sb")], [f"{n} CNNs"]]
        T(f"d{i}_t", x0, y0 + h0 + 0.5, lab, size=S, cont="a2")
        dx = gc(x0 + max(w0, tw(lab, S)) + 2.0)
        last = y0 + h0 + 0.5 + 2 * LHS
    a2["h"] = gc(last + 1.25 - y)
    h_a = y + a2["h"] + 2.0 - top
    # (b) the matrix slab and the equation
    bx, y = xs[1] + 2.0, ys[1]
    b1 = kutu("b1", bx, y, inner, 10, "kutu", cont="p1")
    T("b1_h", bx + IN, y + 1.0, [[("Transfer matrix T", "sb")]], size=S, cont="b1")
    T("b1_s", bx + IN, y + 1.0 + LHS, ["target-correct, PGD-10"], size=S, color="muted", cont="b1")
    rec = bl.iso_slab("m0", gr(bx + IN), gr(y + 1.0 + 2 * LHS + 0.5), 11.0, 11.0, 1.0, "panel_3b",
                      top_grid=(C["NmodCten"], C["NmodCten"]), container="b1")
    x0, y0, w0, h0 = rec["bbox_mm"]
    T("b1_n", bx + IN, y0 + h0 + 0.5, [[(name, "sb"), (f" {n} models", "r")] for name, n in MODELS], size=S,
      cont="b1")
    b1["h"] = gc(y0 + h0 + 0.5 + 3 * LHS + 1.25 - y)
    y3 = y + b1["h"] + 1.5
    b2 = kutu("b2", bx, y3, inner, 10, "kutu", cont="p1")
    T("b2_h", bx + IN, y3 + 1.0, [[("Exact split per pair", "sb")]], size=S, cont="b2")
    T("b2_e", bx + IN, y3 + 1.0 + LHS, [EQ1, EQ2], size=S, cont="b2")
    eh = TW("b2_w", bx + IN, y3 + 1.0 + 3 * LHS, EQW, inner - 2 * IN - 0.5, size=S, color="muted", cont="b2")
    mh = TW("b2_m", bx + IN, y3 + 1.0 + 3 * LHS + eh + 0.5,
            "σ, ρ panel means; gradient cosine c, Mantel with log τ", inner - 2 * IN - 0.5, size=S, cont="b2")
    b2["h"] = gc(3 * LHS + eh + 0.5 + mh + 2.0)
    h_b = y3 + b2["h"] + 2.0 - top
    # (c) registered families
    bx, y = xs[2] + 2.0, ys[2]
    c1 = kutu("c1", bx, y, inner, 10, "kutu", cont="p2")
    fy = y + 1.0
    for i, (n_, det, ds) in enumerate(FAMILIES):
        fy += TW(f"fm{i}", bx + IN, fy, f"{n_}: {det}" + (f" ({ds})" if ds else ""), inner - 2 * IN - 0.5,
                 size=S, cont="c1")
    c1["h"] = gc(fy + 1.0 - y)
    h_c = y + c1["h"] + 2.0 - top
    hh = gc(max(h_a, h_b, h_c))
    for i in range(3):
        vf.IDS[f"p{i}"]["h"] = hh
    bl.flow("f01", "p0", "p1", label="PGD-10", kind="arrow")
    bl.flow("f12", "p1", "p2", label="tests", kind="arrow")
    # (d) big-number row
    y2 = top + hh + 3.0
    dw = gf(XR - 0.5 - 2 * pad)
    yd = panel("pd", "d", "Models in each transfer matrix", 0.5 + pad, y2, dw, 10, cont="tuval")
    cw = gf((dw - 5.0) / 3)
    for i, (name, n_) in enumerate(MODELS):
        x0 = 0.5 + pad + 2.5 + i * cw
        nw = tw([[(str(n_), "b")]], vf.TITLE)
        T(f"n{i}_v", x0, yd, [[(str(n_), "b")]], size=vf.TITLE, cont="pd")
        T(f"n{i}_l", x0 + nw + 1.0, yd + gr((lh(vf.TITLE) - LHS) / 2), [f"models, {name}"], size=S, cont="pd")
    vf.IDS["pd"]["h"] = gc(yd + lh(vf.TITLE) + 1.5 - y2)
    # yellow note strip (the template's 'not'): the protocol layer
    ny = y2 + vf.IDS["pd"]["h"] + 2.0
    f, _ = vf.tint_of("not_kutusu")
    nb = vf.rect("note", gr(0.5 + pad), gr(ny), dw, 10.0, fill=f, line=None, role="container", ctype="box",
                 container="tuval")
    nh = TW("note_t", 0.5 + pad + IN, ny + 1.0, PROTOCOL, dw - 2 * IN - 0.5, size=S, cont="note")
    nb["h"] = gc(nh + 2.0)
    vf.IDS["tuval"]["h"] = gc(ny + nb["h"] + pad - 0.5)
    return gc(0.5 + vf.IDS["tuval"]["h"] + 1.0), 5


# ================================================================== style 3
def lay_3():
    """GIRAFFE 2021 Figure 3 / UniAD 2023 Figure 2: grey outer cap > light inner caps > pastel
    module boxes on the flow row, two equal panels below, a bracketed stage strip; right-angled
    grey connectors with labels. The template allows no image (goruntu pay_araligi 0.0-0.1)."""
    vf.reset(STEM, W, 150.0, naming_step=STEP)
    top = 0.5
    ya = panel("pa", "a", "From trained models to the exact split", 0.5, top, gf(XR - 0.5), 10)
    ox, ow = 0.5 + 1.5, gf(XR - 0.5 - 3.0)
    ao = kutu("ao", ox, ya, ow, 10, "gri", cont="pa")
    lg1 = gc(tw(["PGD-10"], S) + 3.0)
    lg2 = gc(tw(["per pair"], S) + 3.0)
    k1w, k2w, mw = 48.0, 33.0, 26.0
    ix = ox + 2.0
    iy = ya + 2.0
    # inner cap holding the two input groups (models, panels)
    ki = kutu("ki", ix, iy, k1w + k2w + 3 * 2.0, 10, "kap", cont="ao")
    k1x, k2x = ix + 2.0, ix + 2.0 + k1w + 2.0
    # models group
    k1 = kutu("k1", k1x, iy + 2.0, k1w, 10, "kutu", cont="ki")
    T("k1_t", k1x + IN, iy + 3.0, [[("Models, CIFAR-10", "sb")]], size=S, cont="k1")
    bw = gf((k1w - 2 * IN - 1.0) / 2)
    by = iy + 3.0 + LHS + 0.5
    bh = gc(2 * LHS + 2.0)
    for i, (name, ck, ent) in enumerate(CELLS):
        r, c = divmod(i, 2)
        x0, y0 = k1x + IN + c * (bw + 1.0), by + r * (bh + 1.0)
        kutu(f"c{i}", x0, y0, bw, bh, ent, cont="k1")
        T(f"c{i}_t", x0 + IN, y0 + 1.0, [[(name, "sb")], [f"{C[ck]} runs"]], size=S, cont=f"c{i}")
    ry = by + 2 * (bh + 1.0)
    kutu("c_r32", k1x + IN, ry, k1w - 2 * IN, gc(LHS + 2.0), "r32", cont="k1")
    T("c_r32_t", k1x + 2 * IN, ry + 1.0, [[("R32", "sb"), (f" ResNet-18, {C['SeedRtt']} runs", "r")]], size=S,
      cont="c_r32")
    ny = ry + gc(LHS + 2.0) + 0.5
    nh = TW("k1_n", k1x + IN, ny, f"seed pair with V-scr; CIFAR-100: {C['SeedChunR']} + {C['SeedChunV']} runs",
            k1w - 2 * IN - 0.5, size=S, color="muted", cont="k1")
    k1["h"] = gc(ny + nh + 1.0 - k1["y"])
    # panels group
    k2 = kutu("k2", k2x, iy + 2.0, k2w, 10, "kutu", cont="ki")
    T("k2_t", k2x + IN, iy + 3.0, [[("Fixed panels", "sb")]], size=S, cont="k2")
    py = iy + 3.0 + LHS + 0.5
    for i, (name, short, img, text, n) in enumerate(PANELS):
        sec = {0: C["SecCten"], 1: C["SecChun"], 2: C["SecIN"]}[i]
        kutu(f"p{i}", k2x + IN, py, k2w - 2 * IN, gc(LHS + 2.0), "panel", cont="k2")
        T(f"p{i}_t", k2x + 2 * IN, py + 1.0, [[(short, "sb"), (f" {n} + {sec}", "r")]], size=S, cont=f"p{i}")
        py += gc(LHS + 2.0) + 1.0
    nh = TW("k2_n", k2x + IN, py, f"robust CNNs + secondary; IN-V2: {C['PairsIN']} pairs", k2w - 2 * IN - 0.5,
            size=S, color="muted", cont="k2")
    k2["h"] = gc(py + nh + 1.0 - k2["y"])
    kh = max(k1["h"], k2["h"])
    k1["h"] = k2["h"] = kh
    ki["h"] = gc(kh + 4.0)
    # module boxes: transfer matrix, exact split
    mx = ix + ki["w"] + lg1
    m = kutu("m", mx, iy, mw, ki["h"], "altin", cont="ao")
    mh = TW("m_t", mx + IN, iy + 1.0, "Transfer matrix T", mw - 2 * IN - 0.5, size=S, cont="m", key="sb")
    matrix_glyph("m_g", mx + IN, iy + 1.0 + mh + 0.5, 12.0, C["NmodCten"], "m")
    TW("m_n", mx + IN, iy + 1.0 + mh + 13.0, f"{C['NmodCten']} / {C['NmodChun']} / {C['NmodIN']} models, "
                                             "target-correct", mw - 2 * IN - 0.5, size=S, cont="m")
    sx = mx + mw + lg2
    sw = gf(ox + ow - 2.0 - sx)
    s_ = kutu("sp", sx, iy, sw, ki["h"], "mor", cont="ao")
    T("sp_t", sx + IN, iy + 1.0, [[("Exact split", "sb")]], size=S, cont="sp")
    T("sp_e", sx + IN, iy + 1.0 + LHS, [EQ1, EQ2], size=S, cont="sp")
    TW("sp_w", sx + IN, iy + 1.0 + 3 * LHS + 0.5, EQW, sw - 2 * IN - 0.5, size=S, color="muted", cont="sp")
    yc = gr(iy + ki["h"] / 2)
    vf.connector("e1", [(ix + ki["w"] + 0.5, yc), (mx - 0.5, yc)])
    T("e1_t", ix + ki["w"] + 1.0, yc - LHS - 0.25, ["PGD-10"], size=S, color="muted", cont="ao")
    vf.connector("e2", [(mx + mw + 0.5, yc), (sx - 0.5, yc)])
    T("e2_t", mx + mw + 1.0, yc - LHS - 0.25, ["per pair"], size=S, color="muted", cont="ao")
    ao["h"] = gc(ki["h"] + 4.0)
    pa_h = gc(ya + ao["h"] + 1.5 - top)
    vf.IDS["pa"]["h"] = pa_h
    # (b) and (c): two equal panels
    y2 = top + pa_h + 4.0
    hw = gf((XR - 0.5 - 6.0) / 2)
    yb = panel("pb", "b", "Panel means and contrasts", 0.5, y2, hw, 10)
    cx = 0.5 + hw + 6.0
    yc2 = panel("pc", "c", "Registered before measurement", cx, y2, gf(XR - cx), 10)
    tw3 = gf((hw - 5.0 - 2 * 2.0) / 3)
    items = [("σ", "symmetric similarity", "sym"), ("ρ", "directional part", "dir"), ("ω", "= log w, vulnerability", "panel")]
    hs = []
    for i, (g, t_, tint) in enumerate(items):
        x0 = 0.5 + 2.5 + i * (tw3 + 2.0)
        kutu(f"g{i}", x0, yb, tw3, 10, tint, cont="pb")
        T(f"g{i}_s", x0 + IN, yb + 1.0, [[(g, "sb")]], size=S, cont=f"g{i}")
        hs.append(TW(f"g{i}_t", x0 + IN, yb + 1.0 + LHS, t_, tw3 - 2 * IN - 0.5, size=S, cont=f"g{i}"))
    gh = gc(LHS + max(hs) + 2.0)
    for i in range(3):
        vf.IDS[f"g{i}"]["h"] = gh
    cy_ = yb + gh + 5.0
    cbx = kutu("con", 0.5 + 2.5, cy_, hw - 5.0, 10, "kutu", cont="pb")
    T("con_t", 0.5 + 2.5 + IN, cy_ + 1.0, [[("contrasts", "sb")]], size=S, cont="con")
    ch = TW("con_b", 0.5 + 2.5 + IN, cy_ + 1.0 + LHS, "source gap = σ part + ρ part; 2 × 2 cell contrasts; "
                                                      "gradient cosine c tested against log τ (Mantel)",
            hw - 5.0 - 2 * IN - 0.5, size=S, cont="con")
    cbx["h"] = gc(LHS + ch + 2.0)
    for i in range(2):
        xm = gr(0.5 + 2.5 + i * (tw3 + 2.0) + tw3 / 2)
        vf.connector(f"gc{i}", [(xm, yb + gh + 0.5), (xm, cy_ - 0.5)])
    pb_h = gc(cy_ + cbx["h"] + 2.0 - y2)
    namew = max(tw([[(n, "sb")]], S) for n, _, _ in FAMILIES)
    fy = yc2
    for i, (n, det, ds) in enumerate(FAMILIES):
        T(f"fa{i}_n", cx + 2.5, fy, [[(n, "sb")]], size=S, cont="pc", w=namew)
        txt = det + (f", {ds}" if ds else "")
        fy += TW(f"fa{i}_d", cx + 2.5 + namew + 0.5, fy, txt, gf(XR - cx) - 5.0 - namew - 1.0, size=S, cont="pc")
    pc_h = gc(fy + 1.5 - y2)
    h2 = max(pb_h, pc_h)
    vf.IDS["pb"]["h"] = vf.IDS["pc"]["h"] = h2
    # stage strip (template 'asama'): bracketed italic stage names, a letterless legend strip
    ly = y2 + h2 + 3.0
    bl.legend_strip("st", "Stages", 0.5, gr(ly), gf(XR - 0.5),
                    [[("[ training: a, inputs ]", "i")], [("[ measurement: a, b ]", "i")],
                     [("[ decision: c, registered ]", "i")]], cols=3)
    return gc(ly + vf.IDS["st"]["h"] + 1.0), 4


LAYOUT = {"8": lay_8, "H": lay_H, "5": lay_5, "3": lay_3}


def main():
    page_h, panels = LAYOUT[NO]()
    # the scene was opened 150 mm high before the content height was known
    vf.PAGE_H = vf.snap_page(page_h)
    rep = vf.run()
    if rep["verdict"] == "PREFLIGHT-ONLY":
        return 0
    if rep["verdict"] != "PASS":
        return 1
    vf.write_fig_manifest("Study design: models and fixed panels give transfer matrices, split exactly into "
                          "vulnerability, symmetric similarity and direction, read by registered families.",
                          kind=KIND, panels=panels,
                          n_exempt_reason="model and run counts are printed in the panels")
    kanit_yaz()
    return 0


if __name__ == "__main__":
    sys.exit(main())
