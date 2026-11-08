#!/usr/bin/env python
"""z_similarity_matrix (Fig. 8 v2, Üslup Z): pairwise symmetric similarity as three matrices on plinths.

    python paper/figures_v2/z_similarity_matrix.py [--check] [--bak]

Double column. One long sand plate carries three low plinths; on each the split-half log tau-bar matrix of
one data set lies flat (CIFAR-10, CIFAR-100, ImageNetV2), rows back to front and columns left to right in
frozen group order. No cell is raised or hidden: the measured value is only the colour of each cell, one of
five pooled quintile bins (the rule of paper/figures/charts/fig_similarity_matrix.py kutular()); the undefined
diagonal is the darkest neutral. The frozen groups are dark frames on
the matrix (design, not data). Depth carries the registration order: CIFAR-10 (main registration) in front,
the addendum sets behind it. Data: the v1 rule paper/figures/charts/fig_similarity_matrix.py veri() (Mantel
files, cell tables, frozen B2 values; K against sheet line 1970). Naming: step 3 (rings 1-3, one per plinth).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
SMV = Z.yukle("paper/figures/charts/fig_similarity_matrix.py", "v1_similarity_matrix")
import numpy as np  # noqa: E402

STEM = "z_similarity_matrix"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Pairwise symmetric similarity on three plinths. log τ̄ (split-half) for all models on CIFAR-10 (1), "
           "CIFAR-100 (2) and ImageNetV2 (3), in frozen group order; cell colour is one of five joint quintile b"
           "ins, the dark diagonal undefined. Dark frames mark the groups; no height carries a value. Scratch-tr"
           "ained ViT-Tiny seeds form a block dissimilar to the CNN panel.")


def fmt(v):
    return SMV.fmt(v)


def main():
    data, foy, okunan, inputs = SMV.veri()
    keys = ["cifar10", "cifar100", "imagenetv2"]
    allv = np.concatenate([data[k]["P"][~np.isnan(data[k]["P"])] for k in keys])
    edges = SMV.kutular(allv)
    vf.reset(STEM, W, 110.0, naming_step=3, naming_kind="rakam")
    CS, GAPX, DY, M, TW_, TH = 1.58, 4.5, 6.0, 2.6, 1.5, 1.3
    ns = [len(data[k]["order"]) for k in keys]
    Ls = [n * CS for n in ns]
    OX, OY = 10.0, 70.0
    S = Z.Sahne(OX, OY)
    pos, xo = [], 0.0
    for i, L in enumerate(Ls):
        pos.append(Z.un(S, xo, i * DY))
        xo += 1.76 * L + GAPX
    nmin = -0.4654 * Ls[0] - 4.0
    nmax = max(i * DY + 0.8851 * L for i, L in enumerate(Ls)) + 4.5
    plate_top = Z.plaka_un(S, "stage", *Z.un(S, -3.2, nmin), xo - GAPX + 8.0, nmax - nmin, 1.6)
    plate_front_y = max(pt[1] for pt in plate_top) + 1.6
    tones = [vf.tint_of(f"isi_{i}")[0] for i in range(1, 6)]
    diag = vf.tint_of("isi_0")[0]
    deg = []
    counts_all = {}
    ybot = 0.0
    for g_, key in enumerate(keys):
        d = data[key]
        P, bounds = d["P"], d["bounds"]
        n = ns[g_]
        L = Ls[g_]
        X0, Y0 = pos[g_]
        Z.golge(S, f"g_base{g_}", X0, Y0, 0.0, L, L, 0.5, group=f"m{g_}", k=(0.9, 0.7))
        Z.prizma(S, f"base{g_}", X0, Y0, 0.0, L, L, 0.5, "kutu", group=f"m{g_}", faces=("front", "right"))
        tabs = []
        for g, (a, b, lab) in enumerate(bounds):
            tint = "govde_panel" if g % 2 == 0 else "notr"
            y0, y1 = Y0 + (n - b) * CS + 0.12, Y0 + (n - a) * CS - 0.12
            tabs.append(("L", g, X0 - 0.5 - TW_, y0, TW_, y1 - y0, tint))
            tabs.append(("B", g, X0 + a * CS + 0.12, Y0 + L + 0.5, (b - a) * CS - 0.24, TW_, tint))
        counts = [0] * 5
        cells = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    cells.append((9, i, j, diag))
                else:
                    v = P[i, j]
                    k = next((k for k in range(5) if v <= edges[k + 1] + 1e-12), 4)
                    counts[k] += 1
                    cells.append((k, i, j, tones[k]))
        # light cells first, darker later, the undefined diagonal last: no earlier cell is a darker copy of a
        # later neighbour (the balance gate's offset-shadow test; cells never overlap, the order is not seen)
        for k, i, j, fill in sorted(cells):
            X, Y = X0 + j * CS, Y0 + (n - 1 - i) * CS
            pts = [S.P(X, Y, 0.5), S.P(X + CS, Y, 0.5), S.P(X + CS, Y + CS, 0.5), S.P(X, Y + CS, 0.5)]
            vf.poly(f"c{g_}_{i}_{j}", pts + [pts[0]], fill=fill, line=vf.tint_of("kutu")[0], lw=vf.LW["ince"],
                    role="obstacle", group=f"m{g_}", ctype="iso")
        for g, (a, b, lab) in enumerate(bounds):
            XA, YA = X0 + a * CS, Y0 + (n - b) * CS
            w = (b - a) * CS
            fr = [S.P(XA, YA, 0.5), S.P(XA + w, YA, 0.5), S.P(XA + w, YA + w, 0.5), S.P(XA, YA + w, 0.5)]
            vf.poly(f"fr{g_}_{g}", fr + [fr[0]], fill=None, line=vf.C["ink"], lw=vf.LW["vurgu"], role="deco",
                    group=f"m{g_}", ctype="iso")
        counts_all[key] = counts
        # station title above the back-left corner, group order under the front edge
        npairs = int(np.sum(~np.isnan(P))) // 2
        deg.append(Z.ev(f"{d['title']} model count", n, SMV.SETS[g_][1], "len(modeller_ortak)", "count; == foy line 1970 (K)"))
        deg.append(Z.ev(f"{d['title']} pairs", npairs, SMV.SETS[g_][1], "log_tau_matrisi off-diagonal / 2", "count"))
        for k in range(5):
            deg.append(Z.ev(f"{d['title']} cells in bin {k + 1}", counts[k], SMV.SETS[g_][1], "log_tau_matrisi",
                            "count over both triangles; drawn as top-face colour"))
        for g, (a, b, lab) in enumerate(bounds):
            deg.append(Z.ev(f"{d['title']} group {lab.replace(chr(10), ' ')} size", b - a, SMV.SETS[g_][2],
                            "modeller.<m>.hucre", "count"))
        fp = S.P(X0, Y0, 0.0)
        names = [b[2].replace("\n", " ") for b in bounds]
        half = (len(names) + 1) // 2
        yb_ = Z.istasyon(g_ + 1, fp[0] - 4.0, plate_front_y + 1.2, d["title"], [f"{n} models, {n * (n - 1) // 2} pairs"])
        T(f"go{g_}", fp[0] - 4.0, yb_ + 0.4, ["groups, back to front:", ", ".join(names[:half]) + ",",
                                            ", ".join(names[half:])], size=Z.S8, color="muted")
        ybot = max(ybot, yb_ + 0.4 + 3 * lh(Z.S8))
    # key: five bins and the diagonal, one row under the plate
    ky = ybot + 1.6
    T("kt", 1.0, ky, [[("log ", "r"), ("τ̄", "r@DejaVuSans"), (" bins:", "r")]], size=Z.S8)
    x = 1.0 + Z.tw([[("log ", "r"), ("τ̄", "r@DejaVuSans"), (" bins:", "r")]], Z.S8) + 2.0
    for k in range(5):
        Z.isaret(f"key{k}", x + 1.6, ky + lh(Z.S8) / 2, "s", fill=tones[k], edge=vf.tint_of("kutu")[1], size=3.2)
        lab = f"{fmt(edges[k])} to {fmt(edges[k + 1])}"
        T(f"keyt{k}", x + 3.8, ky, [lab], size=Z.S8)
        x += 3.8 + Z.tw([lab], Z.S8) + 3.0
    Z.isaret("keyd", x + 1.6, ky + lh(Z.S8) / 2, "s", fill=diag, edge=diag, size=3.2)
    T("keydt", x + 3.8, ky, ["diagonal"], size=Z.S8, color="muted")
    T("hnote", 1.0, ky + lh(Z.S8) + 0.6, ["dark frames mark the frozen groups; the plinth height carries no value"],
      size=Z.S8, color="muted")
    Z.sayfa_sigdir()
    for k in range(6):
        deg.append(Z.ev(f"bin edge {k}", edges[k], SMV.SETS[0][1], "log_tau_matrisi of the three Mantel files",
                        "kutular(): pooled quintiles 0.2/0.4/0.6/0.8 rounded to 0.05, range rounded outward to 0.1"))
    ents = {}
    return Z.bitir(
        STEM, message="Scratch-trained ViT-Tiny seeds form a block of high mutual similarity that is dissimilar to "
                      "the CNN panel on all three data sets.", kind=KIND, panels=3, caption=CAPTION,
        sablon="ic_ice_izgara", tur="veri", degerler=deg,
        kanit_ek={"foy_karsilastirmasi": foy, "okunan_anahtarlar": okunan, "kutu_kenarlari": edges,
                  "hucre_sayilari": counts_all},
        manifest={"entities": ents, "sahne_kalibi": "uc_kaide",
                  "istasyonlar": ["1 CIFAR-10", "2 CIFAR-100", "3 ImageNetV2"],
                  "derinlik_ekseni": "registration order: CIFAR-10 (main) in front, the addendum sets behind",
                  "ikiz_kodlama": "the measured value is only the flat cell colour, read on the key strip",
                  "denge_muafiyet": {"veri_alani_payi": "binned matrices have equal cells and no data axis; the "
                                                         "value is read from the colour key"}},
        denge={"3b_veri": (False, "every cell lies flat and visible; the measured log tau is only the binned colour; "
                                  "group frames are design labels"),
               "gokkusagi_renk_haritasi": (False, "one low-chroma sequential ramp of five steps"),
               "panel_basina_bir_iddia": (True, "each plinth is one data set's similarity matrix")},
        n_exempt_reason="model and pair counts are printed under each station", okunan_ek=list(inputs))


if __name__ == "__main__":
    sys.exit(main())
