#!/usr/bin/env python
"""z_similarity_matrix (Fig. 8 v2, Üslup Z): pairwise symmetric similarity as three flat heat maps.

    python paper/figures_v2/z_similarity_matrix.py [--check] [--bak]

Double column, flat-card composition (third round, 09.11.2026: plate, plinths and the oblique tile view are
gone). Three flat cards side by side each hold the split-half log tau-bar matrix of one data set (CIFAR-10,
CIFAR-100, ImageNetV2) as a flat heat map, rows top to bottom and columns left to right in frozen group order,
one cell size for all three. The measured value is only the colour of each cell, one of five pooled quintile
bins (the rule of paper/figures/charts/fig_similarity_matrix.py kutular()); the undefined diagonal is the
darkest neutral. The frozen groups are dark frames on the diagonal (design, not data). Data: the v1 rule paper/figures/charts/fig_similarity_matrix.py veri() (Mantel
files, cell tables, frozen B2 values; K against sheet line 1970). Naming: step 3 (rings 1-3, one per card).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _z2 as Z  # noqa: E402
from _z2 import vf, gr, lh, T  # noqa: E402

Z.baslat()
Z.duz()
SMV = Z.yukle("paper/figures/charts/fig_similarity_matrix.py", "v1_similarity_matrix")
import numpy as np  # noqa: E402

STEM = "z_similarity_matrix"
KIND = "double"
W = vf.page_width(KIND)
CAPTION = ("Pairwise symmetric similarity. log τ̄ (split-half) for all models on CIFAR-10 (1), CIFAR-100 (2) "
           "and ImageNetV2 (3), rows and columns in frozen group order; cell colour is one of five pooled quintile bins with rounded "
           "bins, the dark diagonal undefined, dark frames mark the groups. Scratch-trained ViT-Tiny seeds form a "
           "block dissimilar to the CNN panel.")


def fmt(v):
    return SMV.fmt(v)


def main():
    data, foy, okunan, inputs = SMV.veri()
    keys = ["cifar10", "cifar100", "imagenetv2"]
    allv = np.concatenate([data[k]["P"][~np.isnan(data[k]["P"])] for k in keys])
    edges = SMV.kutular(allv)
    vf.reset(STEM, W, 110.0, naming_step=3, naming_kind="rakam")
    # third round (09.11.2026): three flat cards side by side, each holding a flat heat map (rows top to bottom
    # and columns left to right in frozen group order); no plinth, no plate, no oblique tiles (closes review 10)
    CS = 2.0
    ns = [len(data[k]["order"]) for k in keys]
    GAPC = 2.0
    CWc = (W - 2.0 - 2 * GAPC) / 3
    LHs = lh(Z.S8)
    tones = [vf.tint_of(f"isi_{i}")[0] for i in range(1, 6)]
    diag = vf.tint_of("isi_0")[0]
    deg = []
    counts_all = {}

    def wrap(words, width):
        lines, cur = [], ""
        for w_ in words:
            cand = (cur + " " + w_).strip()
            if Z.tw([cand], Z.S8) <= width or not cur:
                cur = cand
            else:
                lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
        return lines
    # card height: station (ring row + sub-line), the largest matrix, the group-order lines
    texts = []
    for key in keys:
        names = [b[2].replace("\n", " ") for b in data[key]["bounds"]]
        words = [nm + ("," if i < len(names) - 1 else "") for i, nm in enumerate(names)]
        texts.append(["groups, top to bottom:"] + wrap(words, CWc - 2.6))
    ST_H = 4.6 + LHs
    MAXL = max(ns) * CS
    CH = 1.0 + ST_H + 1.6 + MAXL + 1.6 + max(len(t) for t in texts) * LHs + 1.2
    for g_, key in enumerate(keys):
        d = data[key]
        P, bounds = d["P"], d["bounds"]
        n = ns[g_]
        L = n * CS
        fx, fy, fw, fh = Z.duz_kart(f"card{g_}", 1.0 + g_ * (CWc + GAPC), 1.0, CWc, CH, "kutu")
        face = f"card{g_}_face"
        npairs = int(np.sum(~np.isnan(P))) // 2
        Z.istasyon(g_ + 1, fx + 1.2, fy + 1.0, d["title"], [f"{n} models, {npairs} pairs"], cont=face)
        X0 = fx + (fw - L) / 2
        Y0 = fy + 1.0 + ST_H + 1.6 + (MAXL - L) / 2
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
            x, y = X0 + j * CS, Y0 + i * CS
            pts = [(x, y), (x + CS, y), (x + CS, y + CS), (x, y + CS)]
            vf.poly(f"c{g_}_{i}_{j}", pts + [pts[0]], fill=fill, line=vf.tint_of("kutu")[0], lw=vf.LW["ince"],
                    role="obstacle", group=f"m{g_}")
        for g, (a, b, lab) in enumerate(bounds):
            x, y, w = X0 + a * CS, Y0 + a * CS, (b - a) * CS
            fr = [(x, y), (x + w, y), (x + w, y + w), (x, y + w)]
            vf.poly(f"fr{g_}_{g}", fr + [fr[0]], fill=None, line=vf.C["ink"], lw=vf.LW["vurgu"], role="deco",
                    group=f"m{g_}")
        counts_all[key] = counts
        deg.append(Z.ev(f"{d['title']} model count", n, SMV.SETS[g_][1], "len(modeller_ortak)", "count; == foy line 1970 (K)"))
        deg.append(Z.ev(f"{d['title']} pairs", npairs, SMV.SETS[g_][1], "log_tau_matrisi off-diagonal / 2", "count"))
        for k in range(5):
            deg.append(Z.ev(f"{d['title']} cells in bin {k + 1}", counts[k], SMV.SETS[g_][1], "log_tau_matrisi",
                            "count over both triangles; drawn as cell colour"))
        for g, (a, b, lab) in enumerate(bounds):
            deg.append(Z.ev(f"{d['title']} group {lab.replace(chr(10), ' ')} size", b - a, SMV.SETS[g_][2],
                            "modeller.<m>.hucre", "count"))
        yt = fy + 1.0 + ST_H + 1.6 + MAXL + 1.6
        T(f"go{g_}", fx + 1.2, yt, texts[g_], size=Z.S8, color="muted", cont=face)
    ybot = 1.0 + CH
    # key: five bins and the diagonal, one row under the cards
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
    T("hnote", 1.0, ky + lh(Z.S8) + 0.6, ["dark frames mark the frozen groups; rows and columns share one order"],
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
        manifest={"entities": ents, "sahne_kalibi": "yok (duz isi haritalari, ucuncu tur)",
                  "istasyonlar": ["1 CIFAR-10", "2 CIFAR-100", "3 ImageNetV2"],
                  "derinlik_ekseni": "none: flat cards side by side",
                  "denge_muafiyet": {"veri_alani_payi": "binned matrices have equal cells and no data axis; the "
                                                         "value is read from the colour key"}},
        denge={"3b_veri": (False, "flat heat map; the measured log tau is only the binned colour; group frames are "
                                  "design labels"),
               "gokkusagi_renk_haritasi": (False, "one low-chroma sequential ramp of five steps"),
               "panel_basina_bir_iddia": (True, "each card is one data set's similarity matrix")},
        n_exempt_reason="model and pair counts are printed under each station", okunan_ek=list(inputs))


if __name__ == "__main__":
    sys.exit(main())
