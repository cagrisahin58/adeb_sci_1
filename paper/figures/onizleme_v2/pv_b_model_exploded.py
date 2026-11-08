#!/usr/bin/env python
"""pv_b_model_exploded: ViT-Tiny and ResNet-18 as two exploded bodies on one dimetric stage (Üslup Z).

    python paper/figures/onizleme_v2/pv_b_yapi.py                 # once: the structure dump
    python paper/figures/onizleme_v2/pv_b_model_exploded.py [--check] [--bak]

Double column (177.53 mm, IEEE Access). Two tracks run along the width axis of the one dimetric
36 degree view: ViT-Tiny behind, ResNet-18 in front, both fed by the same 32 x 32 CIFAR input and
both ending in the same 10 class scores (skill principle 9, model opening: before, the 3D bodies,
after). Every layer is a slab standing across the track; the encoder's twelve blocks are drawn
apart (exploded) and the first block is opened on a frosted lens in the free top-left corner
(LayerNorm, three attention heads of 64 dims, MLP 192-768-192). Slab sizes are log-scaled
(side = 2.5 + 1.9 log2(S/7) mm for a spatial side S, thickness = 0.6 + 0.55 log2(C/3) mm for C
channels); every printed number is read from pv_b_model_yapisi.txt (the dump of the project's own
model classes), and the evidence file cites its line. Naming: step 3, ring-numbered stations.
--bak writes a matplotlib quick look (layout only), --check runs the preflight without Visio.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z_ortak as Z  # noqa: E402
from _z_ortak import vf, bl, gr, gc, lh, tw, T  # noqa: E402

Z.baslat()
STEM = "pv_b_model_exploded"
KIND = "double"
YAPI = "paper/figures/onizleme_v2/pv_b_model_yapisi.txt"
W = vf.page_width(KIND)
S8 = vf.SMALL
TITLE = vf.TITLE
SQ = "²"

# ------------------------------------------------------------------ numbers, each with its file line
LINES = Path(YAPI).read_text(encoding="utf-8").splitlines()
D, LN = {}, {}
for _i, _t in enumerate(LINES, 1):
    _m = re.match(r"^([\w.]+) = (.*?)(\s{3}\(.*\))?$", _t)
    if _m:
        D[_m.group(1)] = json.loads(_m.group(2))
        LN[_m.group(1)] = _i
EV = []


def v(key, label=None):
    """Value of a dump key; logs it with file:line for the evidence file."""
    val = D[key]
    EV.append(Z.ev(label or key, val, f"{YAPI}:{LN[key]}", key))
    return val


def fmt_m(n, key):
    s = f"{n / 1e6:.2f} M"
    EV.append(Z.ev(f"{key} printed as {s}", n, f"{YAPI}:{LN[key]}", key, "round(n / 1e6, 2)"))
    return s


def side(s):
    return 2.5 + 1.9 * math.log2(s / 7.0)


def thick(c):
    return 0.6 + 0.55 * math.log2(c / 3.0)


OX, OY, PAGE_H = 46.0, 60.0, 106.0
YV = 28.0
IN_X = -21.0
LENS_O = (17.0, 22.0)
LENS2_O = (3.0, 97.0)
COL_W, COL_GAP, COL_X0 = 18.0, 0.55, 46.0


def lay():
    vf.reset(STEM, W, PAGE_H, naming_step=3, naming_kind="rakam")
    S = Z.Sahne(OX, OY)
    n = {}
    n["vin"] = v("vit.input_hw")[0]
    n["patch"] = v("vit.patch")[0]
    n["grid"] = v("vit.grid")[0]
    n["npatch"] = v("vit.num_patches")
    n["dim"] = v("vit.embed_dim")
    n["ntok"] = v("vit.tokens")
    n["cls"] = v("vit.cls_token")
    n["depth"] = v("vit.depth")
    n["heads"] = v("vit.heads")
    n["hdim"] = v("vit.head_dim")
    n["mlp"] = v("vit.mlp_hidden")
    n["vout"] = v("vit.head_out")
    n["vpar"] = fmt_m(v("vit.params"), "vit.params")
    n["sk"] = v("res.stem_kernel")[0]
    n["ss"] = v("res.stem_stride")[0]
    n["sc"] = v("res.stem_out")
    n["mk"], n["ms"] = v("res.maxpool_kernel"), v("res.maxpool_stride")
    n["st"] = v("res.shape.stem")[2]
    n["mp"] = v("res.shape.maxpool")[2]
    n["layers"] = [(v(f"res.layer{i}.blocks"), v(f"res.layer{i}.channels"), v(f"res.layer{i}.shape")[2])
                   for i in range(1, 5)]
    n["pool"] = v("res.shape.pool")[1]
    n["rout"] = v("res.fc_out")
    n["rpar"] = fmt_m(v("res.params"), "res.params")
    n["nconv"] = v("res.conv_layers_main_path")
    n["nw"] = v("res.weighted_layers_main_path")
    n["l1_children"] = v("res.layer1.block_last_children")
    n["qkv"] = v("vit.qkv_out")
    n["in_init"] = v("vit.in_init_timm_name")
    if n["qkv"] != 3 * n["dim"]:
        raise SystemExit("qkv width is not 3 x embed_dim")
    if n["vout"] != n["rout"]:
        raise SystemExit("the two heads disagree on the class count")
    if n["heads"] * n["hdim"] != n["dim"]:
        raise SystemExit("heads x head_dim != embed_dim")
    # ---------------- track geometry (world mm)
    res, vit = [], []
    x = 3.0
    rs = [("in224", n["vin"], 3, 3.6, "govde_panel"), ("stem", n["st"], n["sc"], 3.0, "govde_res"),
          ("pool", n["mp"], n["sc"], 3.4, "govde_res")]
    for li, (nb, ch, sp) in enumerate(n["layers"], 1):
        for b in range(nb):
            rs.append((f"l{li}b{b}", sp, ch, 0.9 if b < nb - 1 else 3.4, "govde_res"))
    for name, sp, ch, gap, tint in rs:
        sd, th = side(sp), thick(ch)
        res.append(dict(name=name, X=x, Y=(12.0 - sd) / 2, w=th, d=sd, h=sd, tint=tint))
        x += th + gap
    res.append(dict(name="gpool", X=x, Y=6.0 - 0.6, w=thick(n["pool"]), d=1.2, h=1.2, tint="govde_res"))
    x += thick(n["pool"]) + 2.0
    res_end = x
    xv = 3.0
    tok = side(n["grid"])
    for name, sp, ch, gap, tint in (("in224", n["vin"], 3, 3.6, "govde_panel"),
                                    ("patch", n["grid"], n["dim"], 3.2, "govde_vit")):
        sd, th = side(sp), thick(ch)
        vit.append(dict(name=name, X=xv, Y=YV + (12.0 - sd) / 2, w=th, d=sd, h=sd, tint=tint))
        xv += th + gap
    for b in range(n["depth"]):
        vit.append(dict(name=f"blk{b}", X=xv, Y=YV + (12.0 - tok) / 2, w=1.6, d=tok, h=tok, tint="govde_vit"))
        xv += 1.6 + 1.9
    vit.append(dict(name="cls", X=xv + 0.6, Y=YV + 6.0 - 0.6, w=thick(n["dim"]), d=1.2, h=1.2, tint="govde_vit"))
    xv += thick(n["dim"]) + 2.6
    out_X = max(res_end, xv) + 1.5
    oY, oD = YV / 2 + 1.0, 10.0
    in_side = side(32)
    inp = dict(name="in32", X=IN_X, Y=YV / 2 + 6.0 - in_side / 2, w=0.8, d=in_side, h=in_side, tint="govde_panel")
    # ---------------- stage
    PX0, PY0 = IN_X - 3.0, -6.0
    Z.plaka(S, "pl", PX0, PY0, out_X + 3.0 - PX0, YV + 12.0 + 6.0 - PY0, 1.6)
    # ---------------- shadows, then bodies (back track first, each track left to right)
    for key, trk in (("vit", vit), ("res", res)):
        for i, o in enumerate(trk):
            Z.golge(S, f"g_{key}{i}", o["X"], o["Y"], 0, o["w"], o["d"], o["h"], group=f"trk_{key}")
    Z.golge(S, "g_in", inp["X"], inp["Y"], 0, inp["w"], inp["d"], inp["h"], group="in")
    Z.golge(S, "g_out", out_X, oY, 0, 1.2, oD, 1.2, group="out")
    recs = {}
    for key, trk in (("vit", vit), ("res", res)):
        for o in trk:
            recs[(key, o["name"])] = Z.prizma(S, f"{key}_{o['name']}", o["X"], o["Y"], 0.0, o["w"], o["d"], o["h"],
                                              o["tint"], group=f"trk_{key}")
    recs["in"] = Z.prizma(S, "in32", inp["X"], inp["Y"], 0.0, inp["w"], inp["d"], inp["h"], inp["tint"], group="in",
                          )
    recs["out"] = Z.prizma(S, "out", out_X, oY, 0.0, 1.2, oD, 1.2, "govde_r32", group="out")
    o_top = recs["out"]["corners"]["top"]
    for i in range(1, n["rout"]):
        f = i / n["rout"]
        vf.seg(f"out_c{i}", (o_top[0][0] + (o_top[3][0] - o_top[0][0]) * f, o_top[0][1] + (o_top[3][1] - o_top[0][1]) * f),
               (o_top[1][0] + (o_top[2][0] - o_top[1][0]) * f, o_top[1][1] + (o_top[2][1] - o_top[1][1]) * f),
               vf.tint_of("govde_r32")[1], vf.USLUP.line_min_pt)
    # the 14 x 14 patch field: one inset panel on the right face of the patch-embedding slab (third nesting
    # level), its grid drawn inside it
    a_, b_, c_, d_ = recs[("vit", "patch")]["corners"]["right"]
    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    m = 0.08
    ins = [lerp(lerp(a_, b_, m), lerp(d_, c_, m), m), lerp(lerp(a_, b_, 1 - m), lerp(d_, c_, 1 - m), m),
           lerp(lerp(a_, b_, 1 - m), lerp(d_, c_, 1 - m), 1 - m), lerp(lerp(a_, b_, m), lerp(d_, c_, m), 1 - m)]
    vf.poly("pg_field", ins + [ins[0]], fill=vf.tint_of("ton_3")[0], line=None, role="obstacle", group="trk_vit",
            ctype="iso")
    face_grid("pg", ins, n["grid"], vf.tint_of("govde_vit")[1])
    # two conv strips on the right face of every BasicBlock slab: the block's two 3x3 convs (texture that
    # separates ResNet from ViT without a hue contrast, and the block's structure)
    for o in res:
        if not o["name"].startswith("l"):
            continue
        a_, b_, c_, d_ = recs[("res", o["name"])]["corners"]["right"]
        for k, (t0, t1) in enumerate(((0.14, 0.44), (0.56, 0.86))):
            q = [lerp(lerp(a_, b_, 0.12), lerp(d_, c_, 0.12), t0), lerp(lerp(a_, b_, 0.88), lerp(d_, c_, 0.88), t0),
                 lerp(lerp(a_, b_, 0.88), lerp(d_, c_, 0.88), t1), lerp(lerp(a_, b_, 0.12), lerp(d_, c_, 0.12), t1)]
            vf.poly(f"res_{o['name']}_cv{k}", q + [q[0]], fill=vf.tint_of("govde_res")[1], line=None, role="obstacle",
                    group="trk_res", ctype="iso")
    # the resized image as an inset field on the right face of both 224 x 224 slabs (third nesting level)
    for key in ("res", "vit"):
        a_, b_, c_, d_ = recs[(key, "in224")]["corners"]["right"]
        ins = [lerp(lerp(a_, b_, m), lerp(d_, c_, m), m), lerp(lerp(a_, b_, 1 - m), lerp(d_, c_, 1 - m), m),
               lerp(lerp(a_, b_, 1 - m), lerp(d_, c_, 1 - m), 1 - m), lerp(lerp(a_, b_, m), lerp(d_, c_, m), 1 - m)]
        vf.poly(f"{key}_img", ins + [ins[0]], fill=vf.tint_of("ton_6")[0], line=vf.tint_of("govde_panel")[1],
                lw=vf.USLUP.line_min_pt, role="obstacle", group=f"trk_{key}", ctype="iso")
    # ---------------- floor connectors (zemin izi): input -> both tracks, both tracks -> output
    ink = vf.C["arrow"]
    lw = vf.LW["normal"]
    yin = inp["Y"] + inp["d"] / 2
    vf.spline("c_in_res", [S.P(IN_X + 1.2, yin - 2.5, 0), S.P(-2.0, 6.0, 0), S.P(res[0]["X"] - 0.6, 6.0, 0)], ink, lw,
              arrow=True)
    vf.spline("c_in_vit", [S.P(IN_X + 1.2, yin + 2.5, 0), S.P(-2.0, YV + 6.0, 0), S.P(vit[0]["X"] - 0.6, YV + 6.0, 0)],
              ink, lw, arrow=True)
    # flow label (what the floor trace carries): the same image goes to both models
    re_, ve_ = res[-1], vit[-1]
    gp = v("vit.global_pool")
    lp = S.P(ve_["X"] + ve_["w"] + 1.0, YV + 6.0 + 1.6, 0)
    T("c_vit_lab", lp[0], lp[1] - lh(S8) - 0.25, ["CLS token" if gp == "token" else gp], size=S8, color="muted",
      cont="pl_top")
    vf.spline("c_res_out", [S.P(re_["X"] + re_["w"] + 0.5, 6.0, 0), S.P(out_X - 2.5, 6.0, 0),
                            S.P(out_X - 0.4, oY + 2.0, 0)], ink, lw, arrow=True)
    vf.spline("c_vit_out", [S.P(ve_["X"] + ve_["w"] + 0.5, YV + 6.0, 0), S.P(out_X - 2.5, YV + 6.0, 0),
                            S.P(out_X - 0.4, oY + oD - 2.0, 0)], ink, lw, arrow=True)
    return S, res, vit, recs, inp, n, out_X, oY, oD


def face_grid(pid, corners, k, col):
    a, b, c, d = corners
    for i in range(1, k):
        f = i / k
        vf.seg(f"{pid}_u{i}", (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f),
               (d[0] + (c[0] - d[0]) * f, d[1] + (c[1] - d[1]) * f), col, vf.USLUP.line_min_pt)
        vf.seg(f"{pid}_v{i}", (a[0] + (d[0] - a[0]) * f, a[1] + (d[1] - a[1]) * f),
               (b[0] + (c[0] - b[0]) * f, b[1] + (c[1] - b[1]) * f), col, vf.USLUP.line_min_pt)


def station(k, x, y, title, subs, cont=None):
    bl.ring(f"st{k}", gr(x), gr(y), k, container=cont)
    d = vf.IDS[f"st{k}"]["w"]
    T(f"st{k}_t", x + d + 1.0, y + (d - lh(TITLE)) / 2, [[(title, "sb")]], size=TITLE, cont=cont)
    yy = y + (d - lh(TITLE)) / 2 + lh(TITLE)
    for i, s_ in enumerate(subs):
        T(f"st{k}_s{i}", x + d + 1.0, yy + i * lh(S8), [s_], size=S8, color="muted", cont=cont)
    return yy + len(subs) * lh(S8)


def labels(S, res, vit, recs, inp, n, out_X, oY, oD):
    # ---- ResNet: one label per stage, below the front track, two staggered rows
    groups = [("stem", ["stem"], [[("stem", "sb")], [f"{n['sk']}×{n['sk']}, stride {n['ss']}"],
                                  [f"{n['sc']} ch · {n['st']}{SQ}"]]),
              ("pool", ["pool"], [[("max-pool", "sb")], [f"{n['mk']}, stride {n['ms']}"], [f"{n['sc']} ch · {n['mp']}{SQ}"]])]
    for li, (nb, ch, sp) in enumerate(n["layers"], 1):
        groups.append((f"l{li}", [f"l{li}b{b}" for b in range(nb)],
                       [[(f"layer{li}", "sb")], [f"{nb} blocks"], [f"{ch} ch · {sp}{SQ}"]]))
    groups.append(("gpool", ["gpool"], [[("pool, fc", "sb")], [f"{n['pool']}, then {n['rout']}"]]))
    # parts list under the stage: one column per stage, hairline leaders fanning down to it
    ytab = PAGE_H - 0.75 - 3 * lh(S8)
    for k, (gid, names, lines) in enumerate(groups):
        a = recs[("res", names[0])]["corners"]["front"][0]
        ax_, ay_ = a[0] + 0.3, a[1] + 0.6
        cx = COL_X0 + k * (COL_W + COL_GAP)
        Z.T(f"rl_{gid}", cx, ytab, lines, size=S8, w=COL_W)
        vf.seg(f"rl_{gid}_ld", (cx + 0.6, ytab - 0.4), (ax_, ay_), vf.C["frame"], vf.USLUP.line_min_pt)
    # ---- ViT labels above the back track
    a = recs[("vit", "patch")]["corners"]["top"][3]
    Z.etiket("vl_patch", 56.0, 5.0,
             [[("patch embedding", "sb")], [f"{n['patch']}×{n['patch']} patches, {n['grid']}×{n['grid']} = {n['npatch']}"],
              [f"{n['dim']} dims per token"]], None, size=S8)
    vf.seg("vl_patch_ld", (a[0] - 0.2, 5.0 + 3 * lh(S8) + 0.4), (a[0] - 0.2, a[1] - 0.5), vf.C["muted"],
           vf.USLUP.line_min_pt)
    b0 = recs[("vit", "blk0")]["corners"]["top"][3]
    b1 = recs[("vit", f"blk{n['depth'] - 1}")]["corners"]["top"][2]
    mx = ((b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2)
    Z.etiket("vl_enc", mx[0] + 1.0, mx[1] - 12.5,
             [[(f"encoder: {n['depth']} blocks, drawn apart", "sb")],
              [f"{n['ntok']} tokens ({n['npatch']} + {n['cls']} CLS) · {n['dim']} dims"]], (mx[0], mx[1] - 0.6),
             size=S8, lead_from=(mx[0], mx[1] - 4.5))
    c = recs[("vit", "blk0")]["corners"]["front"][0]
    T("vl_b0", c[0] - 1.25, c[1] + 0.75, ["1"], size=S8, color="muted", cont="pl_top")
    c = recs[("vit", f"blk{n['depth'] - 1}")]["corners"]["front"][1]
    T("vl_b11", c[0] + 0.25, c[1] + 0.75, [str(n["depth"])], size=S8, color="muted", cont="pl_top")
    # ---- stations (ring digits)
    station(1, 1.0, 57.0, "Input", ["CIFAR 32×32×3,", f"resized to {n['vin']}×{n['vin']}", "in both drawn models"])
    station(3, 1.0, 73.0, "ResNet-18 (R224)", ["timm resnet18, 224 px",
                                                  f"{n['nconv']} conv + 1 fc, {n['rpar']}", "below: conv, BN, skip"])
    b1 = recs[("vit", f"blk{n['depth'] - 1}")]["corners"]["top"][2]
    station(2, b1[0] - 22.0, 2.0, "ViT-Tiny", [f"timm vit_tiny_patch16_224, {n['vpar']} parameters",
                                               f"V-IN starts from {n['in_init'].split('.')[0]}"])
    ot = recs["out"]["corners"]["top"][2]
    yb = station(5, 148.0, 40.0, "Output", [f"{n['rout']} class scores"])
    # the scores leave the stage: an arrow from the output bar up to the station label (flow label within 3 mm)
    k1 = (ot[0] + 9.0, ot[1] - 2.0)
    vf.seg("st5_ok_a", (ot[0] + 0.3, ot[1] - 0.3), k1, vf.C["arrow"], vf.LW["normal"])
    vf.seg("st5_ok_b", k1, (155.0, yb + 1.2), vf.C["arrow"], vf.LW["normal"], arrow=True)


def lens(S, recs, n):
    """Station 4: block 1 opened on a frosted lens in the free top-left corner."""
    L = Z.Sahne(*LENS_O)
    Z.plaka(L, "ln", 0.0, 0.0, 33.0, 11.0, 0.9, tint="cam")
    objs = []
    x = 2.0
    objs.append(("ln1", x, 2.0, 0.7, 7.0, 6.0, "notr"))
    x += 0.7 + 2.6
    hd = 2.6
    for h in range(n["heads"]):                      # each head: its Q, K and V plates (qkv = 3 x 192 -> 3 heads x 64)
        for q, tint in enumerate(("govde_vit", "ton_3", "govde_panel")):
            objs.append((f"h{h}{'qkv'[q]}", x + q * 1.6, 1.2 + h * (hd + 0.6), 0.5, hd, 6.0, tint))
    x += 3.7 + 2.6
    objs.append(("ln2", x, 2.0, 0.7, 7.0, 6.0, "notr"))
    x += 0.7 + 2.6
    hi = 6.0 * n["mlp"] / n["dim"] / 2.0          # fc1 is 768 / 192 = 4 times as wide; drawn at half that
    objs.append(("fc1", x, 2.0, 1.8, 7.0, hi, "govde_vit"))
    x += 1.8 + 2.6
    objs.append(("fc2", x, 2.0, 1.8, 7.0, 6.0, "govde_vit"))
    for oid, X, Y, w, d, h, t in objs:
        Z.golge(L, f"lg_{oid}", X, Y, 0, w, d, h, group="lens", k=(0.30, 0.22))
    rl = {}
    for oid, X, Y, w, d, h, t in objs:
        rl[oid] = Z.prizma(L, f"lens_{oid}", X, Y, 0, w, d, h, t, group="lens")
    # labels under the lens (white wedge between the lens and the stage), leaders up to the parts
    def front_c(oid):
        t = rl[oid]["corners"]["front"]
        return ((t[0][0] + t[1][0]) / 2, (t[0][1] + t[1][1]) / 2)
    lab = [("lb_ln", 31.0, [[("LayerNorm ×2", "r")]], ["ln1", "ln2"]),
           ("lb_h", 35.5, [[(f"{n['heads']} heads: Q K V × {n['hdim']}", "r")]], ["h0q"]),
           ("lb_mlp", 40.0, [[(f"MLP {n['dim']} · {n['mlp']} · {n['dim']}", "r")]], ["fc1", "fc2"])]
    for pid, y, lines, oids in lab:
        bx, by, bw, bh = Z.T(pid, 1.0, y, lines, size=S8)
        for j, oid in enumerate(oids):
            tx, ty = front_c(oid)
            vf.seg(f"{pid}_ld{j}", (bx + bw + 0.3 if tx > bx + bw else tx, by + bh / 2 if tx > bx + bw else by - 0.3),
                   (tx, ty + 0.3), vf.C["frame"], vf.USLUP.line_min_pt)
    station(4, 1.0, 1.0, "Block 1, opened", ["on a frosted lens"])
    # ---- station 6: one ResNet BasicBlock opened on a second lens (bottom right)
    L2 = Z.Sahne(*LENS2_O)
    Z.plaka(L2, "ln2", 0.0, 0.0, 23.0, 7.5, 0.9, tint="cam")
    ch1 = n["layers"][0][1]
    seq = [("c1", 1.8, 2.0, "govde_res"), ("bn1", 0.6, 1.0, "notr"), ("c2", 1.8, 2.0, "govde_res"),
           ("bn2", 0.6, 1.0, "notr"), ("add", 1.0, 1.4, "govde_panel")]
    x = 2.0
    o2 = []
    for oid, w, gap, tint in seq:
        hh = 3.0 if oid.startswith("c") else (1.8 if oid == "add" else 2.6)
        o2.append((oid, x, 1.5, w, 4.5, hh, tint))
        x += w + gap
    for oid, X, Y, w, d_, h, t in o2:
        Z.golge(L2, f"lg2_{oid}", X, Y, 0, w, d_, h, group="lens2", k=(0.30, 0.22))
    r2 = {}
    for oid, X, Y, w, d_, h, t in o2:
        r2[oid] = Z.prizma(L2, f"lens2_{oid}", X, Y, 0, w, d_, h, t, group="lens2")
    # identity skip: an arc over the block from the input side to the add node
    a0 = L2.P(0.6, 3.75, 0.2)
    a1 = L2.P(o2[-1][1] + 0.5, 3.75, o2[-1][5] + 0.1)
    vf.spline("skip", [a0, L2.P(6.0, 3.75, 3.9), L2.P(13.0, 3.75, 4.0), a1], vf.C["arrow"], vf.LW["normal"], arrow=True)
    kids = [c.split(":")[1] for c in n["l1_children"]]
    nconv = sum(1 for c in kids if c == "Conv2d")
    nbn = sum(1 for c in kids if c == "BatchNorm2d")
    if any(c.startswith("downsample") for c in n["l1_children"]):
        raise SystemExit("the opened block has a downsample path; the drawn skip is the identity")
    n["l1_open"] = (nconv, ch1, nbn)
    # the block's parts named under the lens, one line, from the dump (conv, BN, conv, BN, add)
    # parts of the opened block, named in station 3's last line (conv 3x3 twice, BN twice, identity skip)
    # callout from the last BasicBlock of layer4 to the second lens
    l1 = recs[("res", "l1b1")]["corners"]["front"]
    lr2 = vf.IDS["ln2_right"]["pts"]
    vf.seg("cal2_a", (l1[0][0] - 0.3, l1[0][1] + 0.3), (lr2[2][0] + 0.4, lr2[2][1]), vf.C["frame"], vf.USLUP.line_min_pt,
           dash=True)
    # callout: two dashed hairlines from block 1 to the lens's right edge
    b0 = recs[("vit", "blk0")]["corners"]["top"]
    lr = vf.IDS["ln_right"]["pts"]
    col = vf.mix(vf.C["muted"], vf.tint_of("cam")[0], 0.0)
    vf.seg("cal_a", (b0[3][0] - 0.3, b0[3][1] - 0.3), (lr[2][0] + 0.4, lr[2][1]), col, vf.USLUP.line_min_pt, dash=True)
    vf.seg("cal_b", (b0[0][0] - 0.3, b0[0][1] + 0.2), (lr[0][0] + 0.4, lr[0][1]), col, vf.USLUP.line_min_pt, dash=True)
    return L, rl, lab


CAPTION = ("ViT-Tiny and the 224-pipeline ResNet-18 as exploded bodies. Both take one 32×32 CIFAR image, resize it "
           "to 224×224 inside the model and end in ten class scores (1, 5); the ViT blocks are drawn apart and block 1 "
           "opens with its three Q, K, V heads (2, 4); a ResNet BasicBlock opens with its skip (3). Sizes are log-scaled.")


def main():
    S, res, vit, recs, inp, n, out_X, oY, oD = lay()
    labels(S, res, vit, recs, inp, n, out_X, oY, oD)
    L, rl, lab = lens(S, recs, n)
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
    vf.write_fig_manifest("ViT-Tiny and ResNet-18 drawn as exploded 3D bodies from the project's own model classes, "
                          "fed by one input and ending in ten class scores.", kind=KIND, panels=5,
                          n_exempt_reason="a model schematic shows layer sizes, not samples")
    Z.manifest_ek(sablon="model_acilimi_3b", tur="sematik", surec_zinciri=True, uslup_yolu="<skill>/styles/uslup_Z.yaml",
                  sunum_kalibi="sahne", altyazi_taslagi=CAPTION,
                  istasyonlar=["1 Input", "2 ViT-Tiny", "3 ResNet-18 (R224), its layer1 block opened below",
                               "4 Block 1, opened", "5 Output"],
                  olcek_kurali="side = 2.5 + 1.9 log2(S/7) mm, thickness = 0.6 + 0.55 log2(C/3) mm (log scale)")
    ev = list(EV)
    ev.append(Z.ev("model-internal resize 32 -> 224 (ViT)", "nn.Upsample(size=(224, 224), bilinear)", "src/models/vit.py:392",
                   "self.resize"))
    ev.append(Z.ev("model-internal resize 32 -> 224 (ResNet)", "nn.Upsample(size=(224, 224), bilinear)", "src/models/r224.py:120",
                   "self.resize"))
    ev.append(Z.ev("CIFAR input 32 x 32 x 3", "32x32x3", "src/models/r224.py:136 input_size returns (32, 32); pv_b_yapi.py feeds zeros 1x3x32x32",
                   "input_size"))
    Z.kanit_yaz(STEM, ev, ek={"yapi_dokumu": YAPI, "yapi_dokumu_sha256": Z.sha_file(YAPI),
                             "yapi_betigi": "paper/figures/onizleme_v2/pv_b_yapi.py",
                             "kaynak_siniflar": ["src/models/vit.py:361 CIFAR10ViTTiny", "src/models/r224.py:139 CIFAR10ResNet18R224"],
                             "fig2_kaniti_ile": "paper/figures/fig2_design_recipe.kanit.json taslak icin okundu; bu sekil egitim tarifini cizmez",
                             "altyazi_taslagi": CAPTION})
    Z.denge_ajan(STEM, 0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
