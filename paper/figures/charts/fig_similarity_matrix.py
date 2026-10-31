#!/usr/bin/env python
"""Pairwise symmetric similarity log tau_ij on CIFAR-10, CIFAR-100 and ImageNetV2; card figure,
visio-cizici style 7 (plan 04_cizim_plani.md section 9.8).

    python paper/figures/charts/fig_similarity_matrix.py --uslup 7

Three heat maps on one shared five-step scale, rows and columns in the frozen group order
(CIFAR-10: V-scr, V-IN, R224-scr, R224-IN, R32, panel, secondary; CIFAR-100: ViT, ResNet, panel,
secondary; ImageNetV2: transformers, CNN pair counterparts, panel, secondary); each diagonal group
block is framed; the diagonal is undefined and left blank. Columns follow the row order (the
matrices are symmetric, checked), so only the rows are labelled. A key strip at the bottom gives
the five bins.

Data rule: copied verbatim from paper/figures/konsey/fig_similarity_matrix.py main() (left
untouched; its constants SETS, GROUPS, FOY_KC and J4P are imported): symmetric matrices with zero
diagonal, the split-half identities against the frozen B2/B9/B4 outputs, and the reference sheet
lines 1595, 1741, 1850, 1943, 1945, 1970, 1972, 1974. A mismatch writes nothing.
Naming: step 4, letterless title strip.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
np = O.np
import fig_similarity_matrix as SM  # noqa: E402  (constants only; its main() is not run)

ARGS = O.argumanlar(__doc__)
STEM = "similarity_matrix"
SCRIPT = "paper/figures/charts/fig_similarity_matrix.py"
J4P, SETS, GROUPS, FOY_KC = SM.J4P, SM.SETS, SM.GROUPS, SM.FOY_KC


def veri():
    foy = K.Foy()
    J4 = K.load_json(J4P)
    MT4 = K.dig(J4, "b4.model_tablosu")
    data, okunan, inputs = {}, {}, [J4P]
    okunan[J4P] = ["b4.model_tablosu.<m>.yari_log.sigma (identity check only)"]
    for key, mp, hp, bp, title, kline, kanc in SETS:
        Mj, Hj, Bj = K.load_json(mp), K.load_json(hp), K.load_json(bp)
        inputs += [mp, hp, bp]
        okunan[mp] = ["log_tau_matrisi", "modeller_ortak", "dislanan", "sinamalar.ham.K"]
        okunan[hp] = ["modeller.<m>.{hucre, aile, birincil_panel, ikincil_panel}"]
        okunan[bp] = ["b2.F_B2.K-c.{log_tau_tur_ici, sigma_V}", "b2.tur_ici_resnet_log_tau"]
        mods = list(K.dig(Mj, "modeller_ortak"))
        T = np.array(K.dig(Mj, "log_tau_matrisi"), dtype=float)
        if K.dig(Mj, "dislanan"):
            K.fail(f"{key}: excluded models {Mj['dislanan']}")
        HT = K.dig(Hj, "modeller")
        if set(mods) != set(HT):
            K.fail(f"{key}: modeller_ortak != cell-table models")
        n = len(mods)
        if T.shape != (n, n):
            K.fail(f"{key}: matrix shape {T.shape} for {n} models")
        foy.esit(f"{key}: max |T - T^T|", float(np.abs(T - T.T).max()), 0.0, 0.0, "log tau matrix is symmetric")
        foy.esit(f"{key}: max |diag|", float(np.abs(np.diag(T)).max()), 0.0, 0.0, "diagonal stored as 0 (undefined)")
        foy.esit(f"{key}: K == sinamalar.ham.K", n, K.dig(Mj, "sinamalar.ham.K"), 0, "model count")
        foy.kontrol(f"{key}: K", n, kline, kanc, 0)
        idx = {m: i for i, m in enumerate(mods)}

        def lt(a, b):
            return float(T[idx[a], idx[b]])
        # identity checks: the plotted matrix is the frozen split-half log tau
        Kc = K.dig(Bj, "b2.F_B2.K-c")
        for pk, v in K.dig(Kc, "log_tau_tur_ici").items():
            a, b = pk.split("|")
            foy.esit(f"{key}: log tau {pk} == K-c.log_tau_tur_ici", lt(a, b), v, 1e-12,
                     "matrix cell equals the frozen script's within-family value")
        for pk, v in K.dig(Bj, "b2.tur_ici_resnet_log_tau").items():
            a, b = pk.split("|")
            foy.esit(f"{key}: log tau {pk} == tur_ici_resnet_log_tau", lt(a, b), v, 1e-12,
                     "matrix cell equals the frozen script's within-ResNet value")
        panel = [m for m in mods if HT[m]["birincil_panel"]]
        for m, sv in K.dig(Kc, "sigma_V").items():
            foy.esit(f"{key}: sigma({m}) from matrix == K-c.sigma_V", float(np.mean([lt(m, c) for c in panel])), sv,
                     1e-9, "panel mean of the row equals the frozen sigma")
        if key in FOY_KC:
            ln = FOY_KC[key]
            vit = list(K.dig(Kc, "log_tau_tur_ici").values())
            res = list(K.dig(Bj, "b2.tur_ici_resnet_log_tau").values())
            for i, v in enumerate(vit):
                foy.kontrol(f"{key}: ViT within log tau [{i}]", v, ln, "K-c ayrintisi", 3)
            for i, v in enumerate(res):
                foy.kontrol(f"{key}: ResNet within log tau [{i}]", v, ln, "K-c ayrintisi", 3)
            foy.kontrol(f"{key}: ViT within mean", float(np.mean(vit)), ln, "K-c ayrintisi", 3)
            foy.kontrol(f"{key}: ResNet within mean", float(np.mean(res)), ln, "K-c ayrintisi", 3)
            for m, sv in K.dig(Kc, "sigma_V").items():
                foy.kontrol(f"{key}: sigma_V {m}", sv, ln, "K-c ayrintisi", 3)
        if key == "cifar10":  # every model's split-half sigma in B4 (panel members: panel without itself)
            for m in mods:
                if m not in MT4:
                    continue
                pp = [c for c in panel if c != m]
                foy.esit(f"cifar10: sigma({m}) from matrix == b4 yari_log.sigma", float(np.mean([lt(m, c) for c in pp])),
                         MT4[m]["yari_log"]["sigma"], 1e-9, "matrix reproduces B4 sigma (split-half, log)")
        if key == "imagenetv2":
            trs = [m for m in mods if HT[m]["hucre"] == "V-scr"]
            for m in trs:
                pp = [c for c in panel if c != m]
                foy.kontrol(f"imagenetv2: sigma({m})", float(np.mean([lt(m, c) for c in pp])), 1943,
                            "Donusturucu rho ve sigma", 3)
            within = [lt(a, b) for i, a in enumerate(trs) for b in trs[i + 1:]]
            foy.kontrol("imagenetv2: transformer within log tau min", min(within), 1945, "Dondurulmus betigin B8 ciktisi", 3)
            foy.kontrol("imagenetv2: transformer within log tau max", max(within), 1945, "Dondurulmus betigin B8 ciktisi", 3)
            foy.metin("imagenetv2: 6 transformer pairs", "6 cift", 1945, "Dondurulmus betigin B8 ciktisi")
            if len(within) != 6:
                K.fail("imagenetv2: expected six transformer pairs")
        # order
        order, bounds = [], []
        for cell, lab in GROUPS[key]:
            g = [m for m in mods if HT[m]["hucre"] == cell]
            if not g:
                K.fail(f"{key}: empty group {cell}")
            bounds.append((len(order), len(order) + len(g), lab))
            order += g
        if sorted(order) != sorted(mods):
            K.fail(f"{key}: grouping does not cover all models")
        P = np.array([[T[idx[a], idx[b]] for b in order] for a in order])
        if np.isnan(P).any():
            K.fail(f"{key}: off-diagonal NaN in log tau; the grey 'undefined' fill would hide it")
        np.fill_diagonal(P, np.nan)
        data[key] = {"title": title, "order": order, "bounds": bounds, "P": P}
    foy.metin("panel P has 7 members (cifar10)", "panel 7 uyeli", 1741, "Havuz modellerinde sigma ve rho")
    foy_sonuc = foy.bitir()

    return data, foy_sonuc, okunan, inputs


def kutular(allv):
    """Five bins at the pooled quintiles of the drawn cells (20, 40, 60, 80 %), inner edges rounded to
    the nearest 0.05, outer edges the data range rounded outward to 0.1 (duzeltme turu 2: five equal
    bins put 104 of CIFAR-10's 190 cells into one step)."""
    lo, hi = math.floor(allv.min() * 10) / 10, math.ceil(allv.max() * 10) / 10
    inner = [round(round(float(np.quantile(allv, q)) * 20) / 20, 6) for q in (0.2, 0.4, 0.6, 0.8)]
    edges = [round(lo, 6)] + inner + [round(hi, 6)]
    if any(b <= a for a, b in zip(edges, edges[1:])):
        K.fail(f"quintile bin edges are not increasing after rounding: {edges}")
    if edges[-1] < allv.max() or edges[0] > allv.min():
        K.fail("bin edges do not cover the data")
    return edges


def fmt(v):
    return O.minus(f"{v:.2f}".rstrip("0").rstrip(".") if abs(v * 10 - round(v * 10)) < 1e-9 else f"{v:.2f}")


def main():
    data, foy, okunan, inputs = veri()
    allv = np.concatenate([d["P"][~np.isnan(d["P"])] for d in data.values()])
    if allv.max() >= 0:
        K.fail("non-negative log tau present; the one-hue sequential scale no longer fits")
    edges = kutular(allv)
    O.basla(ARGS.uslup)
    from matplotlib.colors import BoundaryNorm, ListedColormap
    from matplotlib.patches import Patch, Rectangle
    from motor.figspec import cards

    ST, U = O.ST, O.U
    tones = [U.tones()[f"isi_{i}"][0] for i in range(1, 6)]
    cmap = ListedColormap(tones)
    cmap.set_bad(U.muted)       # the undefined diagonal: dark grey, apart from every ramp step
    norm = BoundaryNorm(edges, cmap.N)
    W = O.W("double")
    M, GX, KEY_H = 0.5, 1.6, 10.5
    cw = (W - 2 * M - 2 * GX) / 3
    L, R, T = 22.5, 1.5, cards.BAND + 1.0
    side = cw - L - R
    ch = T + side + 1.5
    H = round(M + ch + 1.6 + KEY_H + M, 2)
    cv = cards.Canvas("double", H, naming_step=4, naming_kind="serit")
    row, cizilen, deg = [], {}, []
    paths = {s[0]: s[1] for s in SETS}
    for k, (key, d) in enumerate(data.items()):
        n = len(d["order"])
        c = cv.card(None, d["title"], M + k * (cw + GX), M, cw, ch, tint="white", note=f"n = {n}")
        ax = c.axes(left=L, right=R, top=T, bottom=ch - T - side, grid=None)
        # vector cells (pcolormesh), not a raster image: the PDF carries no embedded picture
        ax.pcolormesh(np.arange(n + 1) - 0.5, np.arange(n + 1) - 0.5, np.ma.masked_invalid(d["P"]), cmap=cmap,
                      norm=norm, edgecolors="face", linewidth=0, rasterized=False)
        ax.add_patch(Rectangle((-0.5, -0.5), n, n, fill=False, ec=U.ink, lw=ST.weights.axis, zorder=5))
        for a, b, _ in d["bounds"]:
            ax.add_patch(Rectangle((a - 0.5, a - 0.5), b - a, b - a, fill=False, ec=U.ink, lw=ST.weights.emph,
                                   zorder=4))
        for sp in ax.spines.values():
            sp.set_visible(False)
        cen = [(a + b - 1) / 2 for a, b, _ in d["bounds"]]
        ax.set_yticks(cen)
        ax.set_yticklabels([lab.replace("\n", " ") for _, _, lab in d["bounds"]])
        ax.set_xticks([])
        ax.tick_params(length=0, pad=1.5)
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(n - 0.5, -0.5)
        ax.grid(False)
        iu = np.triu_indices(n, 1)
        cnt = np.histogram(d["P"][iu], bins=edges)[0]
        cizilen[key] = {"sira": d["order"], "gruplar": [{"etiket": lab, "bas": a, "son": b}
                                                       for a, b, lab in d["bounds"]],
                        "kutu_sayilari": [int(x) for x in cnt], "hucre_sayisi": int(len(iu[0]))}
        for i, j in zip(*iu):
            a, b = d["order"][i], d["order"][j]
            deg.append(O.deger(f"{key} log tau {a} | {b}", float(d["P"][i, j]), paths[key],
                               f"log_tau_matrisi[modeller_ortak.index({a!r})][modeller_ortak.index({b!r})]",
                               "read as stored; drawn as one of five quintile bins (edges in cizilen.kutular)"))
        row.append(c)
    cv.title_strip(row)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white",
                    n_exempt="a key to the colour bins")
    kax = O.anahtar_ekseni(cv, key_c)
    h = [Patch(facecolor=tones[i], edgecolor=U.ink, lw=ST.weights.grid,
                label=("log τ̄ " if i == 0 else "") + f"{fmt(edges[i])} to {fmt(edges[i + 1])}")
          for i in range(5)]
    h += [Patch(facecolor=U.muted, edgecolor=U.ink, lw=ST.weights.grid, label="diagonal (undefined)")]
    h = [h[0], h[3], h[1], h[4], h[2], h[5]]      # rows read low to high: steps 1-3, then 4, 5, diagonal
    kax.legend(handles=h, loc="center", ncol=3, labelspacing=0.3, frameon=False, handlelength=1.2, handletextpad=0.3,
               columnspacing=0.9, borderaxespad=0.0)
    cizilen["kutular"] = {"kenarlar": edges, "tonlar": tones, "veri_en_kucuk": float(allv.min()),
                          "veri_en_buyuk": float(allv.max()),
                          "kural": "pooled quintiles of the drawn cells (20/40/60/80 %), inner edges rounded to 0.05, "
                                  "outer edges the data range rounded outward to 0.1"}
    O.kaydet(cv, STEM, message=("Symmetric similarity is block-structured by cell and family on all three data "
                                "sets, on one shared scale."),
             inputs=inputs, degerler=deg, foy=foy, okunan=okunan, cizilen=cizilen,
             notlar=["Group labels name groups, not models; the model order inside each group follows "
                     "modeller_ortak (cizilen.<set>.sira).",
                     "ImageNetV2 cell table labels transformers 'V-scr' and CNN counterparts 'C1-R32' (frozen "
                     "script reuse); shown as 'transformer' and 'CNN (pair)'. CIFAR-100 'V-scr'/'C1-R32' are shown "
                     "as 'ViT (C100)' and 'ResNet (C100)' (konsey m15)."],
             kararlar=["Karar (duzeltme turu 2): the bin edges are the pooled quintiles of the drawn cells "
                       "(rounded to 0.05) instead of five equal steps, because equal steps put 104 of CIFAR-10's "
                       "190 cells into one step and hid the within-block gradation; the step count stays five, "
                       "because the style supplies five ramp tones (isi_1..isi_5) and a sixth or seventh tone would "
                       "be a colour the palette does not hold.",
                       "Karar (duzeltme turu 2): the undefined diagonal is filled dark grey (the style's muted "
                       "ink), because white sat next to the lightest step (#EAEAF2) and could not be told apart.",
                       "Karar (duzeltme turu 2): the ramp stays the style's blue isi ramp, because a non-blue "
                       "ramp would need new tones outside style 7; the caption must say the blue ramp is not the "
                       "ResNet (R224) colour (Faz C).",
                       "Karar: the continuous cividis map of the council draft became the style's five-step "
                       "one-hue ramp (isi_1..isi_5), because the skill's heat-map rule asks for five steps of one "
                       "hue and the style supplies them; the bin edges come from the data range (kutular).",
                       "Karar: white cards for the heat maps, because the lightest ramp step equals the style's "
                       "grey plot-area tone and would merge with a grey card.",
                       "Karar: only rows are labelled, because every matrix is symmetric (checked, max |T - T^T| = 0) "
                       "and column labels would cost the height ceiling (70 mm).",
                       "Veri alani payi does not apply: a heat map has no value axis (plan 9.8)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="ortak_satirli_katlar")
    O.ajan(STEM, iddia="each card: one data set's similarity matrix, block structure",
           dogrudan_etiket="group names stand at the rows; titles name the data set",
           renk_haritasi="a five-step one-hue ramp, not a rainbow map")
    return 0


if __name__ == "__main__":
    sys.exit(main())
