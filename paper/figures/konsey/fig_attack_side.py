#!/usr/bin/env python3
"""Attack side (B5): panel-mean log transfer L_k(m) of every source under each permitted attack
(brief 12, section 6.7).

Change log (degisiklik notu):
- 2026-10-31, hakem konseyi B14 (birlesik.md; mercek_sunum bulgu 3): x label gains the unit note
  "(T in %)" on a second line; L_k is the panel mean of log T_k with T in percent (03_methodology,
  "Rates enter the logarithm in percent"). Karar: "(T in %)" rather than the "(w in %)" of the
  report, because this axis carries transfer rates T, not the white-box rate w.
- 2026-10-31: width 3.358 in (= columnwidth of ieeeaccess.cls, see konsey_ortak.py).

One column (3.358 in). Rows are the twelve source models grouped by cell (R32, V-scr, R224-scr,
R224-IN, V-IN); x is the full-sample panel mean of log target-correct transfer S_tam under PGD-10
(circle), momentum PGD (square) and, for ViT sources only, TGR (triangle). Within a row the three
attacks are offset vertically so that near-equal values stay visible. A filled marker is the attack
chosen for that source by cross-fitted selection (both halves choose it); open markers were not
chosen. Colour is the source cell's architecture (same colours as every council figure).

Inputs (quarantine-safe): results/q1/konsey_ayrisim_b5.json (b5.birincil_C1-R32_V-scr.{kaynaklar.<m>.
{S_tam, S_pgd_yari, secilen_cift_tek, secilen_tam_orneklem}, G_PGD, R, V}, b5.betimsel.<pair>.kaynaklar,
b5.izinli), raporlar/konsey_2026-10-29/hucre_tablosu.json (modeller.<m>.hucre). Every drawn value is
compared with results/C1_REFERANS_FOYU.md lines 1620 and 1635-1648 before anything is written.

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_attack_side.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.transforms as mtransforms  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_attack_side.py"
J5P = "results/q1/konsey_ayrisim_b5.json"
HTP = "raporlar/konsey_2026-10-29/hucre_tablosu.json"
CELL_ORDER = [("C1-R32", "R32", "r32"), ("V-scr", "V-scr", "vit"), ("R224-scr", "R224-scr", "r224"),
              ("R224-IN", "R224-IN", "r224"), ("V-IN", "V-IN", "vit")]
FOY_ROW0 = 1635  # first per-source row (ResNet18_AT_s1001); rows run to 1646
ATK = [("pgd", "PGD-10", "o", -0.22), ("mi", "momentum PGD", "s", 0.0), ("tgr", "TGR", "^", 0.22)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_attack_side")
    ap.add_argument("--width-in", type=float, default=K.SINGLE_IN)
    ap.add_argument("--height-in", type=float, default=3.85)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

    J5, HT = K.load_json(J5P), K.load_json(HTP)
    foy = K.Foy()
    hucre = {m: v["hucre"] for m, v in K.dig(HT, "modeller").items()}
    B = K.dig(J5, "b5.birincil_C1-R32_V-scr")
    src = dict(K.dig(B, "kaynaklar"))
    for pair, v in K.dig(J5, "b5.betimsel").items():
        for m, s in v["kaynaklar"].items():
            if m in src:
                foy.esit(f"{m} S_tam.pgd: betimsel[{pair}] == birincil", s["S_tam"]["pgd"], src[m]["S_tam"]["pgd"], 0.0,
                         "same source record in primary and descriptive blocks")
            else:
                src[m] = s
    izinli = K.dig(J5, "b5.izinli")
    rows = []  # (model, cell label, colour key)
    for cell, lab, ck in CELL_ORDER:
        ms = sorted(m for m in src if hucre.get(m) == cell)
        if not ms:
            K.fail(f"no sources in cell {cell}")
        rows += [(m, lab, ck, cell) for m in ms]
    if len(rows) != len(src):
        K.fail(f"{len(src) - len(rows)} sources not placed in a cell group")
    # foy: each source row (order in the sheet is not assumed; the anchor carries model and cell)
    lines = {}
    for n in range(FOY_ROW0, FOY_ROW0 + len(rows)):
        t = foy.lines[n - 1]
        for m, _, _, cell in rows:
            if t.startswith(f"| {m} | {cell} |"):
                lines[m] = n
    if len(lines) != len(rows):
        K.fail(f"foy rows {FOY_ROW0}-{FOY_ROW0 + len(rows) - 1} do not cover all sources: {sorted(set(src) - set(lines))}")
    sel = {}
    for m, _, _, cell in rows:
        s = src[m]
        anc = f"| {m} | {cell} |"
        fam = "ViT" if cell.startswith("V-") else "CNN"
        if sorted(s["S_tam"]) != sorted(izinli[fam]):
            K.fail(f"{m}: attacks {sorted(s['S_tam'])} != permitted {izinli[fam]}")
        for a in s["S_tam"]:
            foy.kontrol(f"{m}.S_tam.{a}", s["S_tam"][a], lines[m], anc, 3)
        a1, a2 = s["secilen_cift_tek"]
        if a1 != a2:
            K.fail(f"{m}: the two halves select different attacks ({a1}, {a2}); filled-marker rule undefined")
        sel[m] = a1
        foy.metin(f"{m} selection", f"{anc} {a1} / {a2} | {s['secilen_tam_orneklem']} |", lines[m], anc)
    n_tgr = sum(1 for m, _, _, cell in rows if cell.startswith("V-") and sel[m] == "tgr")
    n_vit = sum(1 for m, _, _, cell in rows if cell.startswith("V-"))
    foy.metin("TGR selected count", f"secildigi kaynak sayisi: {n_tgr} / {n_vit} ViT kaynagi", 1648, "TGR'nin en iyi")
    R, V = K.dig(B, "R"), K.dig(B, "V")
    gp = sum(src[m]["S_pgd_yari"] for m in R) / len(R) - sum(src[m]["S_pgd_yari"] for m in V) / len(V)
    foy.esit("G_PGD == mean_R S_pgd_yari - mean_V S_pgd_yari", gp, K.dig(B, "G_PGD"), 1e-9, "gap definition")
    foy.kontrol("G_PGD", K.dig(B, "G_PGD"), 1620, "| G_PGD (log birimi", 4)
    foy_sonuc = foy.bitir()

    # ---- figure ----
    K.style(args.seed)
    W, H = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0.36, 0.315, 0.60, 0.663])  # 2026-10-31: room for the two-line x label (B14)
    ypos, y, prev = {}, 0.0, None
    centres = []
    for m, lab, ck, cell in rows:
        if prev is not None and cell != prev:
            y += 0.6
        ypos[m] = y
        prev = cell
        y += 1.0
    cizilen = {}
    for m, lab, ck, cell in rows:
        for a, alab, mk, dy in ATK:
            if a not in src[m]["S_tam"]:
                continue
            v = src[m]["S_tam"][a]
            filled = sel[m] == a
            ax.plot([v], [ypos[m] + dy], ls="none", marker=mk, ms=4.6, mec=K.COL[ck], mew=1.0,
                    mfc=K.COL[ck] if filled else "white", zorder=4 if filled else 3)
            cizilen.setdefault(m, {"hucre": cell, "secilen": sel[m]})[a] = round(v, 6)
    for cell, lab, ck in CELL_ORDER:
        ys = [ypos[m] for m, _, _, c in rows if c == cell]
        centres.append(((min(ys) + max(ys)) / 2, lab, min(ys), max(ys)))
    ax.set_yticks([ypos[m] for m, *_ in rows])
    ax.set_yticklabels([m.rsplit("_s", 1)[-1] for m, *_ in rows])
    ax.set_ylim(y - 0.4, -0.6)
    tr = mtransforms.blended_transform_factory(fig.transFigure, ax.transData)
    for yc, lab, y0, y1 in centres:
        fig.text(0.015, yc, lab, transform=tr, ha="left", va="center", fontsize=8)
        ax.plot([-0.175, -0.175], [y0 - 0.3, y1 + 0.3], transform=mtransforms.blended_transform_factory(ax.transAxes, ax.transData),
                color=K.EDGE, lw=0.6, clip_on=False)
    ax.set_xlabel(r"panel-mean log transfer $L_k(m)$" + "\n" + r"($T$ in %)", labelpad=2, linespacing=1.15)  # B14
    ax.tick_params(axis="y", length=0, pad=2)
    ax.grid(axis="x", color="#e6e6e6", lw=0.5, zorder=0)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.xaxis.set_major_locator(plt.MultipleLocator(0.2))
    hs = [Line2D([], [], ls="none", marker=mk, ms=4.6, mfc="white", mec=K.INK, mew=0.9, label=alab)
          for _, alab, mk, _ in ATK]
    hs.append(Line2D([], [], ls="none", marker="o", ms=4.6, mfc=K.INK, mec=K.INK, mew=0.9, label="selected (filled)"))
    hs += [Line2D([], [], ls="none", marker="s", ms=5.5, mfc=K.COL[k], mec=K.COL[k], label=l)
           for k, l in (("r32", "ResNet-18 (32 px)"), ("r224", "ResNet-18 (224 px)"), ("vit", "ViT-Tiny"))]
    fig.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False, handletextpad=0.3,
               columnspacing=1.0, labelspacing=0.3)

    min_pt = K.layout_checks(fig)
    Rr = fig.canvas.get_renderer()
    if fig.legends[0].get_window_extent(Rr).overlaps(ax.get_tightbbox(Rr)):
        K.fail("legend overlaps the axes")
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    okunan = {J5P: ["b5.birincil_C1-R32_V-scr.kaynaklar.<m>.{S_tam, S_pgd_yari, secilen_cift_tek, secilen_tam_orneklem}",
                    "b5.birincil_C1-R32_V-scr.{R, V, G_PGD}", "b5.betimsel.<pair>.kaynaklar.<m>", "b5.izinli"],
              HTP: ["modeller.<m>.hucre"]}
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], [J5P, HTP], (W, H), args.dpi, min_pt, okunan, cizilen,
                       foy_sonuc,
                       ["every S_tam (12 sources x permitted attacks) vs foy 1635-1646 (3 dp), row found by model and cell",
                        "attack sets == b5.izinli per family; cross-fitted halves agree; selection text vs foy rows",
                        "TGR selected 0 of 5 ViT sources vs foy 1648",
                        "G_PGD recomputed from S_pgd_yari == JSON (1e-9) and vs foy 1620 (4 dp); not drawn",
                        "V-scr sources identical in primary and descriptive blocks",
                        "no text overlap, all text inside, >= 8 pt, legend clear of axes, no Type 3 font"],
                       ["Tick labels are seeds; group labels at left are cells.",
                        "Vertical offsets inside a row separate the attacks (PGD-10 above, momentum PGD centre, TGR below); "
                        "they carry no value."],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
