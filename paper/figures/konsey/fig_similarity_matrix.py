#!/usr/bin/env python3
"""Pairwise symmetric similarity log tau_ij on CIFAR-10, CIFAR-100 and ImageNetV2 (brief 12, section 6.5).

Double column (7.16 in), three heat maps side by side with one shared colour scale. Rows and
columns are ordered by cell or family group (CIFAR-10: V-scr, V-IN, R224-scr, R224-IN, R32,
primary panel, secondary panel; CIFAR-100: V-scr, R32, primary panel, secondary panel;
ImageNetV2: transformers, CNN pair counterparts, primary panel, secondary panel), diagonal
blocks of each group are framed, diagonal cells are undefined and left blank.

Colour map: every off-diagonal log tau in the three matrices is negative, so a diverging scale
centred at zero would use only one arm; a luminance-monotone sequential map (cividis, colour-blind
safe, survives grey-scale printing) is used instead, with a shared range rounded outward to 0.1.

Inputs (quarantine-safe): results/q1/konsey_b10_gradyan/mantel_{cifar10,cifar100,imagenetv2}.json
(log_tau_matrisi, modeller_ortak, sinamalar.ham.K), raporlar/konsey_2026-10-29/hucre_tablosu{,_b9,_b8}.json
(modeller.<m>.{hucre, aile, birincil_panel, ikincil_panel}), results/q1/konsey_ayrisim_b2.json and
results/q1/konsey_b9_c100/b9_dondurulmus_b2.json (b2.F_B2.K-c, b2.tur_ici_resnet_log_tau) and
results/q1/konsey_ayrisim_b4.json (b4.model_tablosu.<m>.yari_log.sigma) for the identity checks that
the matrices are split-half log tau (ek on kayit section 6.1). Every check against
results/C1_REFERANS_FOYU.md must pass before anything is written.

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_similarity_matrix.py
"""
import argparse
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_similarity_matrix.py"
J4P = "results/q1/konsey_ayrisim_b4.json"
SETS = [
    # key, mantel json, cell table, B2-type json (or None), title, foy line of Mantel 'ham' row, anchor
    ("cifar10", "results/q1/konsey_b10_gradyan/mantel_cifar10.json", "raporlar/konsey_2026-10-29/hucre_tablosu.json",
     "results/q1/konsey_ayrisim_b2.json", "CIFAR-10", 1970, "| cifar10 | ham |"),
    ("cifar100", "results/q1/konsey_b10_gradyan/mantel_cifar100.json", "raporlar/konsey_2026-10-29/hucre_tablosu_b9.json",
     "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json", "CIFAR-100", 1972, "| cifar100 | ham |"),
    ("imagenetv2", "results/q1/konsey_b10_gradyan/mantel_imagenetv2.json", "raporlar/konsey_2026-10-29/hucre_tablosu_b8.json",
     "results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json", "ImageNetV2", 1974, "| imagenetv2 | ham |"),
]
# group order and display label per data set: (cell value in the frozen cell table, label)
GROUPS = {
    "cifar10": [("V-scr", "V-scr"), ("V-IN", "V-IN"), ("R224-scr", "R224-scr"), ("R224-IN", "R224-IN"),
                ("C1-R32", "R32"), ("panel", "panel"), ("ikincil_panel", "secondary")],
    "cifar100": [("V-scr", "V-scr"), ("C1-R32", "R32"), ("panel", "panel"), ("ikincil_panel", "secondary")],
    # B8 cell table reuses the frozen labels: transformers carry 'V-scr', their CNN counterparts 'C1-R32'
    "imagenetv2": [("V-scr", "transformer"), ("C1-R32", "CNN (pair)"), ("panel", "panel"),
                   ("ikincil_panel", "secondary")],
}
# K-c lines: within-ViT and within-ResNet log tau and sigma_V (CIFAR-10 1595, CIFAR-100 1850)
FOY_KC = {"cifar10": 1595, "cifar100": 1850}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_similarity_matrix")
    ap.add_argument("--width-in", type=float, default=K.DOUBLE_IN)
    ap.add_argument("--height-in", type=float, default=2.52)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

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
        np.fill_diagonal(P, np.nan)
        data[key] = {"title": title, "order": order, "bounds": bounds, "P": P}
    foy.metin("panel P has 7 members (cifar10)", "panel 7 uyeli", 1741, "Havuz modellerinde sigma ve rho")
    foy_sonuc = foy.bitir()

    allv = np.concatenate([d["P"][~np.isnan(d["P"])] for d in data.values()])
    if allv.max() >= 0:
        K.fail("non-negative log tau present; the sequential-scale rationale no longer holds, revisit the colour map")
    vmin, vmax = math.floor(allv.min() * 10) / 10, math.ceil(allv.max() * 10) / 10

    # ---- figure ----
    K.style(args.seed)
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    cmap = plt.get_cmap("cividis").copy()
    cmap.set_bad("white")
    s_in, lab_in, x0_in = 1.43, 0.63, 0.02
    bot_in = 0.74
    axs = []
    for k in range(3):
        x = x0_in + lab_in + k * (s_in + lab_in + 0.08)
        axs.append(fig.add_axes([x / W, bot_in / H, s_in / W, s_in / H]))
    cizilen = {}
    for ax, (key, d) in zip(axs, data.items()):
        n = len(d["order"])
        im = ax.imshow(d["P"], cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest", aspect="equal")
        for a, b, _ in d["bounds"]:
            ax.add_patch(Rectangle((a - 0.5, a - 0.5), b - a, b - a, fill=False, ec=K.INK, lw=0.8, zorder=3))
        cen = [(a + b - 1) / 2 for a, b, _ in d["bounds"]]
        labs = [lab for _, _, lab in d["bounds"]]
        ax.set_yticks(cen)
        ax.set_yticklabels(labs)
        ax.set_xticks(cen)
        ax.set_xticklabels(labs, rotation=90)
        ax.tick_params(length=0, pad=2)
        bnd = [a - 0.5 for a, _, _ in d["bounds"][1:]]
        ax.set_xticks(bnd, minor=True)
        ax.set_yticks(bnd, minor=True)
        ax.tick_params(which="minor", length=2.5, width=0.6)
        ax.set_xlim(-0.5, n - 0.5)
        ax.set_ylim(n - 0.5, -0.5)
        for sp in ax.spines.values():
            sp.set_linewidth(0.6)
        ax.set_title(d["title"], fontsize=9, pad=3)
        cizilen[key] = {"sira": d["order"], "gruplar": [{"etiket": lab, "bas": a, "son": b} for a, b, lab in d["bounds"]],
                        "matris_ust_ucgen_ozet": {"en_kucuk": float(np.nanmin(d["P"])), "en_buyuk": float(np.nanmax(d["P"])),
                                                  "hucre_sayisi": int(n * (n - 1) / 2)}}
    cb_x = (x0_in + 3 * (s_in + lab_in) + 0.08 * 2 + 0.07) / W
    cax = fig.add_axes([cb_x, bot_in / H, 0.08 / W, s_in / H])
    cb = fig.colorbar(im, cax=cax)
    cb.outline.set_linewidth(0.6)
    cb.ax.tick_params(length=2.5, width=0.6, pad=1.5)
    cb.set_label(r"$\log\bar\tau_{ij}$", labelpad=2)
    cb.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}".replace("-", "−")))
    for ax, lab in zip(axs, ("(a)", "(b)", "(c)")):
        bb = ax.get_position()
        K.panel_label(fig, bb.x0 - lab_in / W + 0.004, bb.y1 + 0.012, lab, va="bottom")

    min_pt = K.layout_checks(fig)
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    cizilen["renk_olcegi"] = {"harita": "cividis (sequential, luminance-monotone)", "vmin": vmin, "vmax": vmax,
                              "veri_en_kucuk": float(allv.min()), "veri_en_buyuk": float(allv.max())}
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], inputs, (W, H), args.dpi, min_pt, okunan, cizilen,
                       foy_sonuc,
                       ["matrices symmetric with zero diagonal; model set == cell table; K vs foy 1970/1972/1974",
                        "split-half identity: within-family cells == frozen K-c / tur_ici_resnet values (1e-12)",
                        "split-half identity: panel-mean rows == frozen sigma_V (1e-9); CIFAR-10 every B4 model sigma (1e-9)",
                        "K-c within-ViT and within-ResNet log tau, means and sigma_V vs foy 1595 (CIFAR-10), 1850 (CIFAR-100)",
                        "ImageNetV2 transformer sigma vs foy 1943; within-transformer min/max vs foy 1945",
                        "no text overlap, all text inside, >= 8 pt, no Type 3 font"],
                       ["Brief 6.5 asks for a diverging scale; every off-diagonal log tau is negative "
                        f"(range {allv.min():.3f} to {allv.max():.3f}), so a sequential luminance-monotone map is used.",
                        "Axis labels name groups, not individual models; the model order inside each group follows "
                        "modeller_ortak and is recorded under cizilen_degerler.",
                        "ImageNetV2 cell table labels transformers 'V-scr' and their CNN counterparts 'C1-R32' (frozen "
                        "script reuse); they are displayed as 'transformer' and 'CNN (pair)'. Mo ViT-B is in the "
                        "transformer group."],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
