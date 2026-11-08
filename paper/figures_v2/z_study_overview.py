#!/usr/bin/env python
"""pv_a_study_scene: the study design (fig:study_overview's content) as one dimetric maquette scene (Üslup Z).

    python paper/figures_v2/z_study_overview.py [--check] [--bak]   (Fig. 1 v2, from the Faz 1 preview pv_a; letters (a)-(e) as cited in the body text)

Double column (177.53 mm, IEEE Access). One stage plate carries three stations: (1) the trained models
as a 2 x 2 table (rows ViT-Tiny and ResNet-18, columns scratch and ImageNet init.), every cell a stack of
thin slices, one slice per training run, and the R32 bridge plinth beside it; (2) the three reference
panels as card decks, one card per panel member, the CIFAR decks carrying their first four test images
on the front card; (3) the three transfer matrices as flat tiles whose side follows the model count and
whose top is ruled n x n. Floor traces join (1) and (2) to (3). Below the stage, (4) the exact split of
each log transfer rate is three frosted glass layers drawn apart (the lower layers are seen through the
upper ones by pre-composited tones, style Z 'saydamlik'), and (5) the registered families stand on a
note card. Every count is the one fig1_study_overview printed, recounted from the frozen cell tables and
Mantel files and checked against results/C1_REFERANS_FOYU.md by the shared content module
paper/figures/visio/_icerik_study_overview.py (imported read-only; its goruntuler() writer is not used).
Naming: step 3, ring-numbered stations.
"""
from __future__ import annotations

import hashlib
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, bl, gr, gc, lh, tw, T  # noqa: E402

Z.baslat()
sys.path.insert(0, str(Z.ROOT / "paper" / "figures" / "visio"))
import _icerik_study_overview as IC  # noqa: E402  (read-only: sayilar(), kanit_degerleri())

STEM = "z_study_overview"
KIND = "double"
W = vf.page_width(KIND)
S8 = vf.SMALL
TITLE = vf.TITLE
PAGE_H = 106.0
OX, OY = 27.5, 54.0
TAU_BAR = [("log ", "r"), ("τ̄", "r@DejaVuSans")]     # macros_konsey.tex line 3: \simt = \bar{\tau}
IMG_DIR = Z.OUT / "_img"


def mosaics(n=4, up=8):
    """The first four test images of CIFAR-10 and CIFAR-100, 2 x 2, nearest x8 (the rule of
    _icerik_study_overview.goruntuler, written here instead of into paper/figures/visio)."""
    import numpy as np
    from PIL import Image
    IMG_DIR.mkdir(exist_ok=True)
    out = {}
    for name, (src, key) in IC.GORUNTU.items():
        raw = Path(src).read_bytes()
        d = pickle.loads(raw, encoding="bytes")
        x = np.asarray(d[key][:n]).reshape(n, 3, 32, 32).transpose(0, 2, 3, 1)
        rows = [np.concatenate(list(x[r * 2:(r + 1) * 2]), axis=1) for r in range(2)]
        mos = np.concatenate(rows, axis=0)
        im = Image.fromarray(mos.astype("uint8"), "RGB").resize((mos.shape[1] * up, mos.shape[0] * up), Image.NEAREST)
        p = IMG_DIR / f"{name}_test_0-{n - 1}.png"
        im.save(p)
        out[name] = {"png_abs": str(p.resolve()), "png": Z._rel(str(p.resolve())), "kaynak": Z._rel(src), "kaynak_sha256": hashlib.sha256(raw).hexdigest(),
                     "indeksler": list(range(n)), "islem": f"2x2 mosaic, nearest x{up}"}
    return out          # png_abs: Visio's Import needs a full path; only the relative "png" goes to the evidence


LETTER = {1: "a", 2: "b", 3: "e", 4: "d", 5: "c"}


def station(k, x, y, title, subs, cont=None, sub_runs=None):
    """Second round (08.11.2026, bulgu 11): every station name is a small note card (style Z 'kutu', the flat
    information card) whose panel letter stands inside the card at the bottom left (uslup_Z.yaml panel_harfi
    konum kart_ici_sol_alt); title and sub-lines are indented past the letter. (x, y) is the card's top left
    corner; returns the card's bottom y."""
    titles = title if isinstance(title, list) else [title]
    let = [[(f"({LETTER[k]})", "sb")]]
    d = tw(let, TITLE) + 0.6
    tx = x + 1.0 + d
    wmax = max([tw([[(t_, "sb")]], TITLE) for t_ in titles] +
               [tw([s_] if isinstance(s_, str) else [s_], S8) for s_ in subs] + [0.0])
    hh = len(titles) * lh(TITLE) + len(subs) * lh(S8)
    h0 = gc(1.0 + max(hh, lh(TITLE)) + 1.0)
    w0 = gc(1.0 + d + wmax + 1.0)
    f, _e = vf.tint_of("kutu")
    vf.rect(f"lc{k}", gr(x), gr(y), w0, h0, fill=f, line=None, rnd=float(vf.USLUP.corner_mm), role="container",
            ctype="card")
    cid = f"lc{k}"
    T(f"st{k}_t", tx, y + 1.0, [[(t_, "sb")] for t_ in titles], size=TITLE, cont=cid)
    yy = y + 1.0 + len(titles) * lh(TITLE)
    for i, s_ in enumerate(subs):
        T(f"st{k}_s{i}", tx, yy + i * lh(S8), [s_] if isinstance(s_, str) else [s_], size=S8,
          color="muted", cont=cid)
    T(f"st{k}", x + 1.0, gr(y) + h0 - 1.0 - lh(TITLE), let, size=TITLE, cont=cid)
    vf.note_naming(f"st{k}", "letter")
    return gr(y) + h0


def lay(C, IMG):
    vf.reset(STEM, W, PAGE_H, naming_step=5, naming_kind="harf")
    S = Z.Sahne(OX, OY)
    lead = vf.C["frame"]
    lw0 = vf.USLUP.line_min_pt
    Z.plaka(S, "pl", -14.0, -16.0, 104.0, 50.0, 1.8)
    # ---------------- (1) the 2 x 2 table and the R32 plinth
    Z.plaka(S, "tb", 0.0, 1.0, 54.0, 28.0, 1.2, tint="kap", z=1.2)
    for f_ in ("top", "front", "right"):
        vf.IDS[f"tb_{f_}"]["container"] = "pl_top"        # the table stands on the stage
    cells = [("R224-scr", "SeedRscr", "govde_res", 0, 0), ("R224-IN", "SeedRin", "govde_res", 1, 0),
             ("V-scr", "SeedVscr", "govde_vit", 0, 1), ("V-IN", "SeedVin", "govde_vit", 1, 1)]
    stacks = {}
    th, gp, fw = 1.0, 0.8, 5.5
    order = sorted(cells, key=lambda c: (-c[4], c[3]))          # back row first, then left to right
    for name, key, tint, c, r in order:
        X0, Y0 = 2.5 + c * 24.0, 4.0 + r * 13.5
        n = C[key]
        Z.golge(S, f"g_{key}", X0, Y0, 1.2, fw, fw, n * (th + gp), group="tbl", k=(0.35, 0.25))
        for i in range(n):
            Z.prizma(S, f"s_{key}_{i}", X0, Y0, 1.2 + i * (th + gp), fw, fw, th, tint, group="tbl")
        stacks[name] = (X0, Y0, n)
    # R32 bridge plinth on the stage floor, right of the table
    n32 = C["SeedRtt"]
    Z.golge(S, "g_r32", -11.0, 24.0, 0, fw, fw, n32 * (th + gp), group="r32", k=(0.35, 0.25))
    for i in range(n32):
        Z.prizma(S, f"s_r32_{i}", -11.0, 24.0, i * (th + gp), fw, fw, th, "govde_r32", group="r32")
    # cell labels on the table top, right of each stack
    for name, key, tint, c, r in cells:
        X0, Y0, n = stacks[name]
        p = S.P(X0 + fw + 4.6, Y0 + 0.5, 1.2)
        T(f"cl_{key}", p[0], p[1] - 2 * lh(S8) + 0.6, [[(name, "sb")], [f"{n} runs"]], size=S8, cont="tb_top")
    p = S.P(-11.0 + fw / 2, 24.0 + fw / 2, n32 * (th + gp))
    bx, by, bw, bh = T("cl_r32", 1.0, 20.5, [[("R32 bridge", "sb"), (f", {n32} runs", "r")]], size=S8)
    vf.seg("cl_r32_ld", (bx + bw * 0.6, by + bh + 0.3), (p[0], p[1] - 0.3), vf.C["frame"], vf.USLUP.line_min_pt)
    # row heads left of the table (columns: station 1 subtitle and the cell names)
    for r, lab in enumerate(("ResNet-18", "ViT-Tiny")):
        a = S.P(0.0, 4.0 + r * 13.5 + fw / 2, 1.2)
        bx, by, bw, bh = T(f"rh{r}", a[0] - 3.5, a[1] - lh(S8) / 2, [[(lab, "sb")]], size=S8, align="r", cont="pl_top")
        vf.seg(f"rh{r}_ld", (bx + bw + 0.3, a[1]), (a[0] - 0.3, a[1]), lead, lw0)
    # ---------------- (2) each reference panel is a deck that stands on its own transfer-matrix tile: the
    # cards are sliced into the matrix plate (one card per panel member; tile side 0.55 mm per model, ruled
    # n x n, the undefined diagonal dark). The physical bond replaces the old deck -> matrix arrow.
    sets = [("CIFAR-10", "cifar10", C["PanelCten"], C["NmodCten"]), ("CIFAR-100", "cifar100", C["PanelChun"], C["NmodChun"]),
            ("ImageNetV2", None, C["PanelIN"], C["NmodIN"])]
    ct, cg = 0.35, 0.55
    TY = 12.0                                         # front edge of the tiles (depth)
    X0 = 59.0
    deckrec, tilerec = {}, {}
    geo = []
    for name, img, npanel, nmod in sets:
        sd = 0.55 * nmod
        geo.append((name, img, npanel, nmod, X0, sd))
        X0 += sd + 3.0
    for name, img, npanel, nmod, X0, sd in geo:
        Z.golge(S, f"g_t{nmod}", X0, TY, 0, sd, sd, 0.8, group="data", k=(0.6, 0.45))
    for name, img, npanel, nmod, X0, sd in geo:
        rec = Z.prizma(S, f"t{nmod}", X0, TY, 0.0, sd, sd, 0.8, "notr", group="data")
        a, b, c, d = rec["corners"]["top"]
        for k in range(1, nmod):
            f = k / nmod
            vf.seg(f"t{nmod}_u{k}", (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f),
                   (d[0] + (c[0] - d[0]) * f, d[1] + (c[1] - d[1]) * f), vf.tint_of("izgara")[0], lw0)
            vf.seg(f"t{nmod}_v{k}", (a[0] + (d[0] - a[0]) * f, a[1] + (d[1] - a[1]) * f),
                   (b[0] + (c[0] - b[0]) * f, b[1] + (c[1] - b[1]) * f), vf.tint_of("izgara")[0], lw0)
        p0 = lambda u, v: (a[0] + (b[0] - a[0]) * u + (d[0] - a[0]) * v, a[1] + (b[1] - a[1]) * u + (d[1] - a[1]) * v)
        for k in range(nmod):
            cell = [p0(k / nmod, k / nmod), p0((k + 1) / nmod, k / nmod), p0((k + 1) / nmod, (k + 1) / nmod),
                    p0(k / nmod, (k + 1) / nmod)]
            vf.poly(f"t{nmod}_d{k}", cell + [cell[0]], fill=vf.tint_of("isi_0")[0], line=None, role="obstacle",
                    group="data", ctype="iso")
        tilerec[name] = (X0, nmod, rec)
        # the deck on the back half of the tile; cards as wide as the tile allows
        cw = min(9.0, sd - 1.0)
        dy0 = TY + sd - 0.3 - npanel * (ct + cg)
        recs = []
        for k in reversed(range(npanel)):
            recs.append(Z.prizma(S, f"d{nmod}_{k}", X0 + (sd - cw) / 2, dy0 + k * (ct + cg), 0.8, cw, ct, cw,
                                 "ton_6", group="data"))
        front = recs[-1]
        if img:
            fx, fy, fw_, fh_ = bl.fit_on_front_face(front["corners"]["front"], IMG[img]["png_abs"], margin=0.4)
            vf.image(f"im_{img}", fx, fy, fw_, fh_, IMG[img]["png_abs"], border=False, group="data", grid=False)
        deckrec[name] = (X0 + (sd - cw) / 2, dy0, npanel, front, cw)
    # ---------------- floor trace: the trained models are attacked against the panels (PGD-10)
    ink, lwn = vf.C["arrow"], vf.LW["normal"]
    k = S.P(57.5, 4.0, 0)
    vf.seg("f13_a", S.P(54.3, 2.0, 0.0), k, ink, lwn)
    vf.seg("f13_b", k, S.P(61.0, 11.6, 0), ink, lwn, arrow=True)
    return S, stacks, deckrec, tilerec


def labels(S, C, deckrec, tilerec):
    lead, lw0 = vf.C["frame"], vf.USLUP.line_min_pt
    # the PGD-10 attack is named in station 2's title (no free floor beside the trace head)
    # one label per data set above the stage: panel members and the matrix size
    texts = {"CIFAR-10": [f"{C['PanelCten']} robust CNNs", f"+ {C['SecCten']} secondary (XCiT-S12)"],
             "CIFAR-100": [f"{C['PanelChun']} robust CNNs", f"+ {C['SecChun']} secondary"],
             "ImageNetV2": [f"{C['PanelIN']} robust CNNs", f"+ {C['NmodIN'] - C['PanelIN']} other, descriptive"]}
    xs = {"CIFAR-10": 66.0, "CIFAR-100": 103.0, "ImageNetV2": 134.0}
    for name, (X0, Y0, n, front, cw) in deckrec.items():
        nmod = tilerec[name][1]
        top = front["corners"]["top"][3]
        lines = [[(name, "sb")]] + [[(t, "r")] for t in texts[name]] + [[(f"matrix of {nmod} models", "r")]]
        bx, by, bw, bh = T(f"dl_{name}", xs[name], 8.0, lines, size=S8)
        vf.seg(f"dl_{name}_ld", (min(max(top[0], bx + 0.5), bx + bw - 0.5), by + bh + 0.3), (top[0], top[1] - 0.4),
               lead, lw0)


def split(C, S):
    """(4) the exact split: three frosted layers drawn apart, lower layers seen through the upper ones."""
    L = S                                          # on the stage now, in front of the matrices
    lw0 = vf.USLUP.line_min_pt
    layers = [("w", "govde_panel", 0.0), ("tau", "ton_2", 3.9), ("r", "ton_4", 7.8)]
    Wl, Dl, Tl = 16.0, 8.0, 0.9
    SX, SY = 70.0, -9.0
    drawn = []
    for key, tint, z in layers:
        rec = Z.prizma(L, f"sp_{key}", SX, SY, z, Wl, Dl, Tl, tint, group="data")
        # see-through: every part of a lower layer under this layer is redrawn, pre-composited with it
        for lk, lrec in drawn:
            for lf in ("top", "front", "right"):
                for uf in ("front", "top", "right"):
                    piece = Z.kirp(lrec["corners"][lf], rec["corners"][uf])
                    if len(piece) >= 3:
                        lo = lrec["tones"][lf].lstrip("#")
                        up = rec["tones"][uf].lstrip("#")
                        vf.poly(f"sp_see_{key}_{lk}_{lf}_{uf}", piece + [piece[0]], fill=vf.mix(up, lo, 0.45),
                                line=None, role="obstacle", group="data", ctype="iso")
        drawn.append((key, rec))
    # the upper layers' edges again on top, so the glass keeps its outline
    for key, rec in drawn[1:]:
        for f in ("front", "right", "top"):
            pts = rec["corners"][f]
            vf.poly(f"sp_edge_{key}_{f}", pts + [pts[0]], fill=None, line=rec["outline"].lstrip("#"), lw=lw0,
                    role="deco", group="data", ctype="iso")
    labs = {"w": [("log w", "r")], "tau": TAU_BAR, "r": [("½ r", "r")]}
    lead = vf.C["frame"]
    for key, rec in drawn:
        f = rec["corners"]["front"]
        a = ((f[0][0] + f[3][0]) / 2, (f[0][1] + f[3][1]) / 2)
        wl = tw([labs[key]], S8) + 1.0
        bx, by, bw, bh = T(f"spl_{key}", a[0] - 3.5 - wl, a[1] - lh(S8) / 2, [labs[key]], size=S8, w=wl,
                           cont="pl_top")
        vf.seg(f"spl_{key}_ld", (bx + bw + 0.6, a[1]), (a[0] - 0.3, a[1]), lead, lw0)
    return L, drawn


FAMILIES = [("panel family", "K-a, K-b, K-c", "CIFAR-10"), ("two-by-two family", "H1, H2, H3", "CIFAR-10"),
            ("attack side", "best attack per source", ""), ("masking check", "AutoAttack", ""),
            ("replication", "K-a, K-b, K-c", "CIFAR-100"), ("gradient family", "Mantel tests", "all three"),
            ("ImageNetV2 panel", "descriptive, no decision", "")]


def registry():
    """(5) registered families on a narrow note card in the right column."""
    x0, y0, w0 = 140.75, 24.5, 36.0
    f, e = vf.tint_of("kutu")
    rows = len(FAMILIES)
    h0 = gc(1.25 + 2 * lh(TITLE) + 0.9 + (rows + 1) * 2 * lh(S8) + 0.3 + lh(TITLE) + 1.0)
    vf.rect("reg", gr(x0), gr(y0), gc(w0), h0, fill=f, line=None, rnd=float(vf.USLUP.corner_mm), role="container",
            ctype="card")
    yb = y0 + 1.25
    T("st4_t", x0 + 1.25, yb, [[("Registered before", "sb")], [("measurement", "sb")]], size=TITLE, cont="reg")
    yb += 2 * lh(TITLE) + 0.3
    # bulgu 5 (08.11): booktabs head rule, the 1.5 pt (vurgu) line of the figure (as Figures 7, 13 and 16)
    vf.seg("reg_rule", (x0 + 1.25, yb), (x0 + w0 - 1.25, yb), vf.C["frame"], vf.LW["vurgu"])
    yb += 0.6
    for i, (nm, det, ds) in enumerate(FAMILIES):
        y = yb + i * 2 * lh(S8)
        T(f"fam{i}", x0 + 1.25, y, [[(nm, "sb")], [det if not ds else f"{det} · {ds}"]], size=S8, cont="reg",
          w=w0 - 2.0)
    y = yb + rows * 2 * lh(S8)
    T("fam_prot", x0 + 1.25, y, [[("protocol layer", "sb")], ["four nested sets"]], size=S8, cont="reg", w=w0 - 2.0)
    T("st4", x0 + 1.25, y0 + h0 - 1.0 - lh(TITLE), [[("(d)", "sb")]], size=TITLE, cont="reg")   # bottom left
    vf.note_naming("st4", "letter")
    return y0 + h0


CAPTION = ("Study overview as one scene. (a) Trained models: the two-by-two design, one slice per run, beside the "
           "R32 bridge; (b) Reference panels, decks of robust CNNs, sliced into (c) their PGD-10 matrices; (d) "
           "Registered before measurement gives the test families; (e) Exact split and contrasts factors each log "
           "rate. Depth runs from inputs (back) to the derived split (front).")


def main():
    C, FOY, OKUNAN = IC.sayilar()
    IMG = mosaics()
    S, stacks, deckrec, tilerec = lay(C, IMG)
    labels(S, C, deckrec, tilerec)
    split(C, S)
    registry()
    station(1, 0.5, 0.75, "Trained models", ["2×2 on CIFAR-10: scratch | ImageNet init.",
                                            "seed pair R32 and V-scr replicated",
                                            f"on CIFAR-100: {C['SeedChunR']} + {C['SeedChunV']} runs"])
    station(2, 67.5, 0.75, "Reference panels", [])
    # (c) has its own card below the matrix tiles and one hairline leader to each tile (bulgu 11)
    yc = station(5, 111.5, 89.0, ["PGD-10", "matrices"], [])
    for name, (X0, nmod, rec) in tilerec.items():
        if name == "CIFAR-10":
            # the CIFAR-10 tile stands right behind the glass layers of (e): any leader to it would cross them;
            # its own data-set label already names it "matrix of 20 models"
            continue
        # review round 2: the leader ends with a dot on the ruled tile top in front of the deck (the deck stands
        # on the back of the tile), so (c) points at the matrix plate while the (b) labels point at the decks
        a, b, c_, d = rec["corners"]["top"]
        u, w_ = 0.5, 0.07
        tip = (a[0] + (b[0] - a[0]) * u + (d[0] - a[0]) * w_, a[1] + (b[1] - a[1]) * u + (d[1] - a[1]) * w_)
        cx_ = min(max(tip[0], 112.5), 111.5 + vf.IDS["lc5"]["w"] - 1.0)
        vf.seg(f"lc5_ld_{nmod}", (cx_, 88.7), tip, vf.C["frame"], vf.USLUP.line_min_pt)
        Z.isaret(f"lc5_dot_{nmod}", tip[0], tip[1], "o", fill="ink", edge="ink", size=0.8, role="deco")
    y3 = station(3, 0.5, 87.0, "Exact split and contrasts",
            [[("log T = log w + ", "r")] + TAU_BAR + [(" + ½ r", "r")],
             "vulnerability, symmetric similarity, direction;", "then panel means per model"])
    # the split goes to the analysis: a trace from the lowest glass layer down to station 3's title (flow label)
    wl = vf.THREE_D["sp_w"]["corners"]["front"][0]
    tt = vf.IDS["st3_t"]
    tip = (tt["x"] + tt["w"] + 0.8, tt["y"] + tt["h"] / 2)
    vf.seg("f_split_a", (wl[0] - 0.3, wl[1] + 0.3), (wl[0] - 4.0, tip[1]), vf.C["arrow"], vf.LW["normal"])
    vf.seg("f_split_b", (wl[0] - 4.0, tip[1]), tip, vf.C["arrow"], vf.LW["normal"], arrow=True)
    if "--bak" in sys.argv:
        Z.onizle(str(Path(vf.STEM).with_name(STEM + "_bak.png")))
        print("quick look written")
        return 0
    rep = vf.run()
    print("verdict", rep["verdict"])
    if rep["verdict"] == "PREFLIGHT-ONLY":
        return 0
    if rep["verdict"] != "PASS":
        return 1
    vf.write_fig_manifest("Study design as one scene: trained models and fixed reference panels give transfer "
                          "matrices, each log rate split exactly into vulnerability, similarity and direction; "
                          "families registered before measurement.", kind=KIND, panels=5,
                          n_exempt_reason="model and run counts are printed at each station")
    Z.manifest_ek(sablon="yontem_semasi", tur="sematik", surec_zinciri=True, uslup_yolu="<skill>/styles/uslup_Z.yaml",
                  sahne_kalibi="maket_masasi", altyazi_taslagi=CAPTION,
                  panel_adlari=["(a) Trained models", "(b) Reference panels", "(c) PGD-10 matrices",
                                "(d) Registered before measurement", "(e) Exact split and contrasts"],
                  derinlik_ekseni="pipeline order: inputs (trained models, panels) at the back, the derived split in "
                                  "front; the registry card stands aside as the fixed rule",
                  uslup_surumu=3)
    deg = IC.kanit_degerleri(C)
    deg.append(Z.ev("ImageNetV2 models outside the robust CNN panel", C["NmodIN"] - C["PanelIN"], IC.M8,
                    "len(modeller_ortak) - count(birincil_panel)", "NmodIN - PanelIN"))
    for name, d in IMG.items():
        deg.append(Z.ev(f"{name} test images", d["indeksler"], d["kaynak"], "b'data'[0:4] (pickle)", d["islem"]))
    Z.kanit_yaz(STEM, deg, ek={"foy_karsilastirmasi": FOY, "okunan_anahtarlar": OKUNAN, "goruntuler": {k_: {a_: b_ for a_, b_ in v_.items() if a_ != "png_abs"} for k_, v_ in IMG.items()},
                              "icerik_modulu": "paper/figures/visio/_icerik_study_overview.py (salt okunur ice aktarim)",
                              "gosterim": {"tau_bar": "τ̄", "kaynak": "paper/manuscript/macros_konsey.tex line 3"},
                              "aileler_kaynagi": "paper/figures/visio/fig_study_overview.py FAMILIES (metin, sayi degil)",
                              "altyazi_taslagi": CAPTION})
    Z.denge_ajan(STEM, 2, {"gercek_goruntu": (True, "the CIFAR-10 and CIFAR-100 decks carry the first four test "
                                                    "images of each set on their front card")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
