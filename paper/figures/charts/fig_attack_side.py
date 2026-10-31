#!/usr/bin/env python
"""Attack side (B5): panel-mean log transfer L_k(m) of every source under each permitted attack;
card figure, visio-cizici style 7 (plan 04_cizim_plani.md section 9.10).

    python paper/figures/charts/fig_attack_side.py --uslup 7

Single column, one card (naming step 1, no panel name). Rows are the twelve source models grouped
by cell (R32, V-scr, R224-scr, R224-IN, V-IN; group label and bracket at the left, seed as the
row label); x is the full-sample panel mean of log target-correct transfer (T in %) under PGD-10
(circle), momentum PGD (square) and, for ViT sources only, TGR (triangle), offset vertically
inside a row. A filled mark is the attack chosen by cross-fitted selection (both halves agree);
open marks were not chosen. Colour is the source cell's architecture (paper palette).

Data rule: copied verbatim from paper/figures/konsey/fig_attack_side.py main() (left untouched;
constants imported): every S_tam against the sheet rows 1635-1646 (found by model and cell),
permitted attack sets, agreeing halves, TGR count line 1648, G_PGD line 1620 (not drawn).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
import fig_attack_side as AS  # noqa: E402  (constants only)

ARGS = O.argumanlar(__doc__)
STEM = "attack_side"
SCRIPT = "paper/figures/charts/fig_attack_side.py"
J5P, HTP, CELL_ORDER, FOY_ROW0, ATK = AS.J5P, AS.HTP, AS.CELL_ORDER, AS.FOY_ROW0, AS.ATK


YOL = {}   # model -> concrete key path of its source record in J5P
D_ROWS = []  # (model, label, colour key, cell) as placed, for the concrete key paths


def veri():
    J5, HT = K.load_json(J5P), K.load_json(HTP)
    foy = K.Foy()
    hucre = {m: v["hucre"] for m, v in K.dig(HT, "modeller").items()}
    B = K.dig(J5, "b5.birincil_C1-R32_V-scr")
    src = dict(K.dig(B, "kaynaklar"))
    # duzeltme turu 2: the concrete record path of every source (no placeholder in the kanit file)
    for m in src:
        YOL[m] = f"b5.birincil_C1-R32_V-scr.kaynaklar.{m}"
    for pair, v in K.dig(J5, "b5.betimsel").items():
        for m, s in v["kaynaklar"].items():
            if m in src:
                foy.esit(f"{m} S_tam.pgd: betimsel[{pair}] == birincil", s["S_tam"]["pgd"], src[m]["S_tam"]["pgd"], 0.0,
                         "same source record in primary and descriptive blocks")
            else:
                src[m] = s
                YOL[m] = f"b5.betimsel.{pair}.kaynaklar.{m}"
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
    D_ROWS[:] = rows
    n_vit = sum(1 for m, _, _, cell in rows if cell.startswith("V-"))
    foy.metin("TGR selected count", f"secildigi kaynak sayisi: {n_tgr} / {n_vit} ViT kaynagi", 1648, "TGR'nin en iyi")
    R, V = K.dig(B, "R"), K.dig(B, "V")
    gp = sum(src[m]["S_pgd_yari"] for m in R) / len(R) - sum(src[m]["S_pgd_yari"] for m in V) / len(V)
    foy.esit("G_PGD == mean_R S_pgd_yari - mean_V S_pgd_yari", gp, K.dig(B, "G_PGD"), 1e-9, "gap definition")
    foy.kontrol("G_PGD", K.dig(B, "G_PGD"), 1620, "| G_PGD (log birimi", 4)
    foy_sonuc = foy.bitir()

    okunan = {J5P: ["b5.birincil_C1-R32_V-scr.kaynaklar.<m>.{S_tam, S_pgd_yari, secilen_cift_tek, secilen_tam_orneklem}",
                    "b5.birincil_C1-R32_V-scr.{R, V, G_PGD}", "b5.betimsel.<pair>.kaynaklar.<m>", "b5.izinli"],
              HTP: ["modeller.<m>.hucre"]}
    return dict(src=src, rows=rows, sel=sel, lines=lines, n_tgr=n_tgr, n_vit=n_vit), foy_sonuc, okunan


def main():
    D, foy, okunan = veri()
    src, rows, sel, lines = D["src"], D["rows"], D["sel"], D["lines"]
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    import matplotlib.transforms as mtransforms
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    W = O.W("single")
    H = 95.0
    M = 0.5
    L, R, T, B = 24.5, 3.0, cards.BAND + 1.0, 30.0
    ms = vg["ortalama_markersize_pt"]
    cv = cards.Canvas("single", H, naming_step=1, naming_kind="yok")
    c = cv.card(None, "Transfer by attack, per source", M, M, W - 2 * M, H - 2 * M, tint="kap",
                note=f"n = {len(rows)} sources")
    ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
    O.eksen(ax, base="x", grid="x")
    ypos, y, prev = {}, 0.0, None
    for m, lab, ck, cell in rows:
        if prev is not None and cell != prev:
            y += 0.6
        ypos[m] = y
        prev = cell
        y += 1.0
    cizilen, deg = {}, []
    for m, lab, ck, cell in rows:
        e = O.ent(ck)
        for a, alab, mk, dy in ATK:
            if a not in src[m]["S_tam"]:
                continue
            v = src[m]["S_tam"][a]
            filled = sel[m] == a
            ax.plot([v], [ypos[m] + dy], ls="none", marker=mk, ms=ms, mec=e.hex, mew=ST.weights.emph,
                    mfc=e.hex if filled else "white", zorder=4 if filled else 3)
            cizilen.setdefault(m, {"hucre": cell, "secilen": sel[m]})[a] = v
            deg.append(O.deger(f"{m} S_tam {a}", v, J5P, f"{YOL[m]}.S_tam.{a}",
                               "read as stored; == foy (3 dp), row found by model and cell", lines[m]))
    ylim = (y - 0.4, -0.6)
    ax.set_ylim(*ylim)
    ax.set_yticks([ypos[m] for m, *_ in rows])
    ax.set_yticklabels([m.rsplit("_s", 1)[-1] for m, *_ in rows])
    from matplotlib.ticker import MultipleLocator
    ax.xaxis.set_major_locator(MultipleLocator(0.2))
    O.tick_fmt(ax, "x", fmt="{:.1f}")
    ax.set_xlabel("panel-mean log transfer L(m)\n(T in %)", labelpad=1, linespacing=1.4)
    # group labels and brackets in the row-label column (mm geometry of the axes)
    axh = H - 2 * M - T - B
    bx = -9.6 / (W - 2 * M - L - R)
    trb = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    for cell, lab, ck in CELL_ORDER:
        ys = [ypos[m] for m, _, _, cc in rows if cc == cell]
        y0, y1 = min(ys) - 0.3, max(ys) + 0.3
        ax.plot([bx, bx], [y0, y1], transform=trb, color=U.ink, lw=ST.weights.axis, clip_on=False)
        ymm = T + ((y0 + y1) / 2 - ylim[1]) / (ylim[0] - ylim[1]) * axh
        c.text(L - 10.4, ymm, lab, ha="right", va="center", fontsize=ST.type_scale.annot, color=U.ink)
    # key under the axes, inside the card
    kax = O.bos_eksen(cv, c.x + 1.5, c.y + c.h - 15.5, c.w - 3.0, 14.0)
    hs = [Line2D([], [], ls="none", marker=mk, ms=ms, mfc="white", mec=U.ink, mew=ST.weights.emph, label=alab)
          for _, alab, mk, _ in ATK]
    hs.append(Line2D([], [], ls="none", marker="o", ms=ms, mfc=U.ink, mec=U.ink, mew=ST.weights.emph,
                     label="filled: selected"))
    hs += [Line2D([], [], ls="none", marker="s", ms=ms, mfc=O.ent(k).hex, mec=O.ent(k).hex, label=lab)
           for k, lab in (("r32", "ResNet-18 (32 px)"), ("r224", "ResNet-18 (224 px)"), ("vit", "ViT-Tiny"))]
    kax.legend(handles=hs, loc="center", ncol=2, frameon=False, handletextpad=0.3, columnspacing=1.2,
               labelspacing=0.3, borderaxespad=0.0)
    deg.append(O.deger("TGR selected count (not drawn as a number)", D["n_tgr"], J5P,
                       "; ".join(f"{YOL[m]}.secilen_cift_tek" for m, _, _, cell in D_ROWS if cell.startswith("V-")),
                       "count of ViT sources whose secilen_cift_tek is tgr; == foy 1648 text", 1648))
    O.kaydet(cv, STEM, message=("Cross-fitted selection picks PGD-10 or momentum PGD for every source; TGR is selected "
                                "for none of the ViT sources."),
             inputs=[J5P, HTP], degerler=deg, foy=foy, okunan=okunan, cizilen=cizilen,
             notlar=["Row labels are seeds; group labels at the left are cells.",
                     "Vertical offsets inside a row separate the attacks (PGD-10 above, momentum PGD centre, TGR "
                     "below); they carry no value."],
             kararlar=["Karar: the x label writes L(m) instead of L_k(m), because a mathtext subscript prints "
                       "below the 8 pt floor (trap 6); the caption keeps L_k(m).",
                       "Karar: the key stands under the axes inside the single card, because naming step 1 allows "
                       "one card only (a separate key strip would be a second card)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tek_kart_veri")
    O.ajan(STEM, iddia="one card, one claim: the attack selected per source",
           dogrudan_etiket="cells and seeds are named at the rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
