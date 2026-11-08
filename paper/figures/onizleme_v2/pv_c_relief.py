#!/usr/bin/env python
"""pv_c_relief: the CIFAR-10 pairwise similarity matrix (fig:similarity_matrix, CIFAR-10 card) as a relief (Üslup Z).

    python paper/figures/onizleme_v2/pv_c_relief.py [--check] [--bak]

Double column (177.53 mm, IEEE Access). The 20 x 20 matrix of split-half log tau-bar lies on a plinth in
the one dimetric 36 degree view: rows run back to front, columns left to right, both in the frozen group
order (V-scr, V-IN, R224-scr, R224-IN, R32, panel, secondary). The relief is the DESIGN, not the data: every
cell whose two models belong to the same frozen group is raised as one plateau (seven diagonal blocks), so
the registered block structure is a landform. The MEASURED value is only the colour of each cell's top
face, one of the five quintile bins of Fig. 8 (pooled over CIFAR-10, CIFAR-100 and ImageNetV2, inner edges
rounded to 0.05, the rule of paper/figures/charts/fig_similarity_matrix.py kutular()); no height, depth or
angle carries a value (skill data rule; style Z sapma 'kabartma'). The undefined diagonal is the darkest
neutral. Data rule: the matrices are read from the frozen Mantel files and checked as fig8 checks them
(symmetric, zero diagonal, K equal to the test's K and to results/C1_REFERANS_FOYU.md line 1970, the
within-ViT and within-ResNet cells equal to the frozen B2 values, sigma_V equal to the panel mean of its
row); a mismatch writes nothing. Karantina: only results/q1/* and the reference sheet are read.
Naming: step 3, ring-numbered stations.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z_ortak as Z  # noqa: E402
from _z_ortak import vf, bl, gr, gc, lh, tw, T  # noqa: E402

Z.baslat()
sys.path.insert(0, str(Z.ROOT / "paper" / "figures" / "konsey"))
import numpy as np  # noqa: E402
import konsey_ortak as K  # noqa: E402
import fig_similarity_matrix as SM  # noqa: E402  (constants only: SETS, GROUPS, FOY_KC; main() is not run)

STEM = "pv_c_relief"
KIND = "double"
W = vf.page_width(KIND)
S8 = vf.SMALL
TITLE = vf.TITLE
PAGE_H = 96.0
OX, OY = 26.0, 66.0
CS = 3.1                  # cell side, mm
H_FLAT = 0.5              # top of every cell: the matrix is flat, no cell is raised or hidden (second round)
EV = []


def veri():
    foy = K.Foy()
    out, okunan = {}, {}
    for key, mp, hp, bp, title, kline, kanc in SM.SETS:
        Mj, Hj, Bj = K.load_json(mp), K.load_json(hp), K.load_json(bp)
        mods = list(K.dig(Mj, "modeller_ortak"))
        T_ = np.array(K.dig(Mj, "log_tau_matrisi"), dtype=float)
        if K.dig(Mj, "dislanan"):
            K.fail(f"{key}: excluded models")
        HT = K.dig(Hj, "modeller")
        n = len(mods)
        if set(mods) != set(HT) or T_.shape != (n, n):
            K.fail(f"{key}: model set or shape")
        foy.esit(f"{key}: max |T - T^T|", float(np.abs(T_ - T_.T).max()), 0.0, 0.0, "symmetric")
        foy.esit(f"{key}: max |diag|", float(np.abs(np.diag(T_)).max()), 0.0, 0.0, "diagonal stored as 0")
        foy.esit(f"{key}: K == sinamalar.ham.K", n, K.dig(Mj, "sinamalar.ham.K"), 0, "model count")
        foy.kontrol(f"{key}: K", n, kline, kanc, 0)
        idx = {m: i for i, m in enumerate(mods)}
        Kc = K.dig(Bj, "b2.F_B2.K-c")
        for pk, v in K.dig(Kc, "log_tau_tur_ici").items():
            a, b = pk.split("|")
            foy.esit(f"{key}: log tau {pk} == K-c", float(T_[idx[a], idx[b]]), v, 1e-12, "frozen within-family value")
        for pk, v in K.dig(Bj, "b2.tur_ici_resnet_log_tau").items():
            a, b = pk.split("|")
            foy.esit(f"{key}: log tau {pk} == within-ResNet", float(T_[idx[a], idx[b]]), v, 1e-12, "frozen value")
        panel = [m for m in mods if HT[m]["birincil_panel"]]
        for m, sv in K.dig(Kc, "sigma_V").items():
            foy.esit(f"{key}: sigma({m}) == K-c.sigma_V", float(np.mean([T_[idx[m], idx[c]] for c in panel])), sv,
                     1e-9, "panel mean of the row")
        order, bounds = [], []
        for cell, lab in SM.GROUPS[key]:
            g = [m for m in mods if HT[m]["hucre"] == cell]
            if not g:
                K.fail(f"{key}: empty group {cell}")
            bounds.append((len(order), len(order) + len(g), lab.replace("\n", " ")))
            order += g
        if sorted(order) != sorted(mods):
            K.fail(f"{key}: grouping does not cover all models")
        P = np.array([[T_[idx[a], idx[b]] for b in order] for a in order])
        np.fill_diagonal(P, np.nan)
        out[key] = {"title": title, "order": order, "bounds": bounds, "P": P, "mantel": mp, "cells": hp,
                    "kline": kline}
        okunan[mp] = ["log_tau_matrisi", "modeller_ortak", "dislanan", "sinamalar.ham.K"]
        okunan[hp] = ["modeller.<m>.{hucre, birincil_panel}"]
        okunan[bp] = ["b2.F_B2.K-c.{log_tau_tur_ici, sigma_V}", "b2.tur_ici_resnet_log_tau"]
    foy.metin("panel P has 7 members (cifar10)", "panel 7 uyeli", 1741, "Havuz modellerinde sigma ve rho")
    sonuc = foy.bitir()
    return out, sonuc, okunan


def kutular(allv):
    """Five bins at the pooled quintiles (20/40/60/80 %), inner edges rounded to 0.05, outer edges the data range
    rounded outward to 0.1: the rule of paper/figures/charts/fig_similarity_matrix.py kutular()."""
    lo, hi = math.floor(allv.min() * 10) / 10, math.ceil(allv.max() * 10) / 10
    inner = [round(round(float(np.quantile(allv, q)) * 20) / 20, 6) for q in (0.2, 0.4, 0.6, 0.8)]
    edges = [round(lo, 6)] + inner + [round(hi, 6)]
    if any(b <= a for a, b in zip(edges, edges[1:])):
        K.fail("bin edges not increasing")
    return edges


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".") if abs(v * 10 - round(v * 10)) < 1e-9 else f"{v:.2f}"
    return s.replace("-", "−")


def station(k, x, y, title, subs, cont=None):
    bl.ring(f"st{k}", gr(x), gr(y), k, container=cont)
    d = vf.IDS[f"st{k}"]["w"]
    T(f"st{k}_t", x + d + 1.0, y + (d - lh(TITLE)) / 2, [[(title, "sb")]], size=TITLE, cont=cont)
    yy = y + (d - lh(TITLE)) / 2 + lh(TITLE)
    for i, s_ in enumerate(subs):
        T(f"st{k}_s{i}", x + d + 1.0, yy + i * lh(S8), [s_] if isinstance(s_, str) else [s_], size=S8,
          color="muted", cont=cont)
    return yy + len(subs) * lh(S8)


def lay(d, edges):
    """Flat matrix on a plinth (no cell is raised or hidden); the frozen groups stand as raised tabs on the
    left (rows) and back (columns) margins, the only margins whose tabs cannot cover a cell in this view,
    and as frames on the matrix."""
    vf.reset(STEM, W, PAGE_H, naming_step=3, naming_kind="rakam")
    S = Z.Sahne(OX, OY)
    P, bounds = d["P"], d["bounds"]
    n = len(d["order"])
    tones = [vf.tint_of(f"isi_{i}")[0] for i in range(1, 6)]
    diag = vf.tint_of("isi_0")[0]
    L = n * CS
    M = 3.4                                   # margin of the plinth that carries the tabs
    Z.plaka(S, "pl", -M, -1.5, L + M + 1.5, L + M + 1.5, 1.6)
    Z.golge(S, "g_base", 0.0, 0.0, 0.0, L, L, H_FLAT, group="relief", k=(0.9, 0.7))
    Z.prizma(S, "base", 0.0, 0.0, 0.0, L, L, H_FLAT, "kutu", group="relief", faces=("front", "right"))

    def XY(i, j):            # row i runs back (i = 0) to front, column j left to right
        return j * CS, (n - 1 - i) * CS

    def binof(v):
        for k in range(5):
            if v <= edges[k + 1] + 1e-12:
                return k
        return 4
    TH, TW_ = 1.8, 2.2
    tabs = []
    for g, (a, b, lab) in enumerate(bounds):
        tint = "govde_panel" if g % 2 == 0 else "notr"
        y0, y1 = (n - b) * CS + 0.15, (n - a) * CS - 0.15
        tabs.append(("L", g, -0.6 - TW_, y0, TW_, y1 - y0, tint))
        tabs.append(("B", g, a * CS + 0.15, L + 0.6, (b - a) * CS - 0.3, TW_, tint))
    for side, g, X, Y, w, dd, tint in tabs:
        Z.golge(S, f"g_tab{side}{g}", X, Y, 0.0, w, dd, TH, group="relief", k=(0.35, 0.25))
    counts = [0] * 5
    for i in range(n):
        for j in range(n):
            X, Y = XY(i, j)
            if i == j:
                fill = diag
            else:
                k = binof(P[i, j])
                counts[k] += 1
                fill = tones[k]
            pts = [S.P(X, Y, H_FLAT), S.P(X + CS, Y, H_FLAT), S.P(X + CS, Y + CS, H_FLAT), S.P(X, Y + CS, H_FLAT)]
            vf.poly(f"c{i}_{j}", pts + [pts[0]], fill=fill, line=vf.tint_of("kutu")[0], lw=vf.USLUP.line_min_pt,
                    role="obstacle", group="relief", ctype="iso")
    blocks = []
    for g, (a, b, lab) in enumerate(bounds):
        X0, Y0 = a * CS, (n - b) * CS
        w = (b - a) * CS
        fr = [S.P(X0, Y0, H_FLAT), S.P(X0 + w, Y0, H_FLAT), S.P(X0 + w, Y0 + w, H_FLAT), S.P(X0, Y0 + w, H_FLAT)]
        vf.poly(f"frame{g}", fr + [fr[0]], fill=None, line=vf.C["ink"], lw=vf.LW["vurgu"], role="deco",
                group="relief", ctype="iso")
        blocks.append((g, a, b, lab, X0, Y0, w))
    rec = {}
    for side, g, X, Y, w, dd, tint in sorted(tabs, key=lambda t: (t[0] != "B", -t[3])):
        rec[(side, g)] = Z.prizma(S, f"tab{side}{g}", X, Y, 0.0, w, dd, TH, tint, group="relief")
    Fp, Bp = S.P(-M, -1.5, 0.0), S.P(-M, L + M, 0.0)        # the plinth's left edge, front and back

    def edge_x(y):
        return Fp[0] + (y - Fp[1]) * (Bp[0] - Fp[0]) / (Bp[1] - Fp[1])
    for g, (a, b, lab) in enumerate(bounds):
        ym = (n - (a + b) / 2) * CS
        anc = S.P(-0.6 - TW_, ym, TH)                       # middle of the tab's outer top edge
        ytxt = anc[1] - lh(S8) / 2
        xr = edge_x(ytxt + lh(S8)) - 2.0 - (21.0 if g in (1, 3) else 0.0)
        xr = min(xr, rec[("L", g)]["bbox_mm"][0] - 1.5)        # outside the tab's box (PDF box-spill check)
        bx, by, bw, bh = T(f"rl{g}", xr, ytxt, [lab], size=S8, align="r")
        vf.seg(f"rl{g}_ld", (bx + bw + 0.3, anc[1]), (anc[0] - 0.4, anc[1]), vf.C["frame"], vf.USLUP.line_min_pt)
    return S, counts, blocks


def key_panel(edges, counts, d):
    """(2) the five bins as flat swatches with their ranges; (3) how to read the relief."""
    x0, y0 = 136.0, 4.0
    station(2, x0, y0, "Measured: colour", [[("log ", "r"), ("τ̄", "r@DejaVuSans"), (", five bins", "r")]])
    yy = y0 + 13.0
    for k in range(5):
        lo, hi = edges[k], edges[k + 1]
        vf.rect(f"key{k}", gr(x0 + 1.0), gr(yy + k * 4.25), 6.0, 3.5, fill=vf.tint_of(f"isi_{k + 1}")[0],
                line=vf.tint_of("kutu")[1], lw=vf.USLUP.line_min_pt, role="obstacle")
        T(f"keyt{k}", x0 + 8.5, yy + k * 4.25 - 0.1, [f"{fmt(lo)} to {fmt(hi)}"], size=S8)
    vf.rect("key_d", gr(x0 + 1.0), gr(yy + 5 * 4.25), 6.0, 3.5, fill=vf.tint_of("isi_0")[0], line=None, role="obstacle")
    T("key_dt", x0 + 8.5, yy + 5 * 4.25 - 0.1, ["diagonal, undefined"], size=S8, color="muted")
    y3 = yy + 6 * 4.25 + 12.0
    yb = station(3, x0, y3, "Design: groups", ["raised tabs and frames:", "the seven frozen groups;",
                                               "height carries no value"])
    return yb


CAPTION = ("CIFAR-10 pairwise similarity on a plinth. The 20×20 split-half log τ̄ matrix lies flat in frozen group "
           "order (1); cell colour is one of five pooled quintile bins (2); raised edge tabs and frames mark the seven "
           "frozen groups (3). No height carries a measured value; the dark diagonal is undefined.")


def main():
    data, foy, okunan = veri()
    allv = np.concatenate([d_["P"][~np.isnan(d_["P"])] for d_ in data.values()])
    if allv.max() >= 0:
        K.fail("non-negative log tau present")
    edges = kutular(allv)
    d = data["cifar10"]
    n = len(d["order"])
    S, counts, blocks = lay(d, edges)
    yb = key_panel(edges, counts, d)
    npairs = int(np.sum(~np.isnan(d["P"]))) // 2
    station(1, 1.0, 2.0, "CIFAR-10 split-half similarity", [f"n = {n} models, {npairs} pairs; rows back to front,",
                                                           "columns left to right, same order"])
    ys = [p["y"] + p["h"] for p in vf.SCENE]
    vf.PAGE_H = vf.snap_page(max(ys) + 0.75)        # no dead band under the content (QC A5)
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
    vf.write_fig_manifest("CIFAR-10 split-half log tau-bar as a relief: colour gives the measured bin, the plateaus "
                          "give the registered same-group blocks.", kind=KIND, panels=3,
                          n_exempt_reason="the model and pair count is printed under station 1")
    Z.manifest_ek(sablon="ic_ice_izgara", tur="veri", uslup_yolu="<skill>/styles/uslup_Z.yaml",
                  entities={f"bin{k + 1}": "#" + vf.tint_of(f"isi_{k + 1}")[0] for k in range(5)},
                  denge_muafiyet={"veri_alani_payi": "a binned matrix has equal cells and no data axis; the "
                                                     "measured value is read from the colour key, not from a length"},
                  sunum_kalibi="kabartma", altyazi_taslagi=CAPTION,
                  istasyonlar=["1 CIFAR-10 split-half similarity", "2 Measured: colour", "3 Design: relief"],
                  kabartma_kurali="flat matrix; raised tabs and frames = frozen group membership (design); colour = measured bin",
                  tur_gerekcesi="data figure (second round): the data-axis share is exempted with a reason because a binned "
                                "matrix has no axis; D1 and D2 do not apply to a Visio build")
    deg = [Z.ev("CIFAR-10 model count n", n, d["mantel"], "len(modeller_ortak)"),
           Z.ev("CIFAR-10 pairs", npairs, d["mantel"], "log_tau_matrisi off-diagonal / 2", "count of off-diagonal cells / 2")]
    for k in range(6):
        deg.append(Z.ev(f"bin edge {k}", edges[k], SM.SETS[0][1],
                        "log_tau_matrisi of the three Mantel files (pooled off-diagonal cells)",
                        "kutular(): quintiles 0.2/0.4/0.6/0.8 rounded to 0.05, range rounded outward to 0.1"))
    for k in range(5):
        deg.append(Z.ev(f"CIFAR-10 cells in bin {k + 1} (both triangles)", counts[k], d["mantel"], "log_tau_matrisi",
                        "count, drawn as top-face colour"))
    for g, (a, b, lab) in enumerate(d["bounds"]):
        deg.append(Z.ev(f"group {lab} size", b - a, d["cells"], "modeller.<m>.hucre", "count"))
    Z.kanit_yaz(STEM, deg, ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan,
                              "kutu_kenarlari": edges, "sira": d["order"], "gruplar": d["bounds"],
                              "kural_kaynagi": "paper/figures/charts/fig_similarity_matrix.py kutular() ve veri()",
                              "altyazi_taslagi": CAPTION})
    Z.denge_ajan(STEM, 0, {"3b_veri": (False, "the matrix is flat and every cell is visible; the measured log tau is "
                                              "only the binned colour of equal cells; the raised tabs mark frozen group "
                                              "membership, a design label"),
                           "panel_basina_bir_iddia": (True, "station 1 the matrix, 2 the colour key, 3 the group marks"),
                           "gokkusagi_renk_haritasi": (False, "one low-chroma sequential ramp of five steps")})
    return 0


if __name__ == "__main__":
    sys.exit(main())
