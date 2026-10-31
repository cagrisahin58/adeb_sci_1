#!/usr/bin/env python
"""Nested conditioning sets and the measured asymmetry under each; card figure, visio-cizici
style 7 (plan 04_cizim_plani.md section 9.14, with Y3: masks in the sets).

    python paper/figures/charts/fig_protocol_sets.py --uslup 7

Single column, two stacked cards under one title strip each (naming step 4, rule branch 5; no
letters). Top card: the four evaluation sets as nested boxes (schematic, not area-proportional;
the CNN->ViT nesting, the ViT->CNN sets nest in the same order), each with the protocol name, the
condition it adds (Table 2 of the manuscript, its mask column in words) and N for the two
directions where they differ. Fills are the paper palette's protocol family (four purples, light
to dark along the nesting); the name is printed in every box, so the tone is never the only cue.
Bottom card: per protocol the three seed-pair asymmetries (open circles), their mean (the
protocol's mark in its tone) and SD (line), joined by a stepped path whose three steps are the
pairwise distances between adjacent rows (identity term, marginal subsets removed, source
robustness).

Data rule: as paper/figures/konsey/fig_protocol_sets.py (left untouched): load_and_check is
imported from it (nesting, mean and SD of the seed values, the decomposition terms and their
signs), and every printed number is compared with results/C1_REFERANS_FOYU.md lines 53-56, 60,
212, 214, 215 and 805-808. The masks are definitions, not numbers; their wording is taken from
paper/manuscript/sections/03_methodology.tex (tab:protocol_masks), which the script reads and
checks. A mismatch writes nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
import fig_protocol_sets as PS  # noqa: E402  (data rules only; its main() is not run)

ARGS = O.argumanlar(__doc__)
STEM = "protocol_sets"
SCRIPT = "paper/figures/charts/fig_protocol_sets.py"
DATA = "results/q1/fig_protokol_kumeleri_veri.json"
SRC = "results/c1_transfer/c1_transfer_summary.json"
TEX = "paper/manuscript/sections/03_methodology.tex"
PROTOCOLS = PS.PROTOCOLS
ENT = {"raw": "prot_raw", "target_correct": "prot_target", "both_correct": "prot_both",
       "successful_source": "prot_success"}
NAME = {"raw": "Unconditioned", "target_correct": "Target-correct", "both_correct": "Both-correct",
        "successful_source": "Successful-source"}
# the condition each set adds, in words; (manuscript row label, LaTeX mask cell that must be present)
MASK = {"raw": ("every test image", "Unconditioned (raw) & always &"),
        "target_correct": ("target correct on the clean image", "Target-correct & $f_T(x) = y$ &"),
        "both_correct": ("and source correct on the clean image",
                         "Both-correct & $f_T(x) = y$ and $f_S(x) = y$ &"),
        "successful_source": ("and the source's own attack succeeds",
                              "Successful-source & $f_T(x) = y$, $f_S(x) = y$, $f_S(x^S_{adv}) \\neq y$ &")}
FOY_ROW = {"raw": (53, "| Kosulsuz (ham) |"), "target_correct": (54, "| Hedef dogru |"),
           "both_correct": (55, "| Her ikisi dogru |"), "successful_source": (56, "| Basarili kaynak |")}
STEPS = [("raw", "target_correct", "ozdeslik_terimi_ham_eksi_hedef_dogru", 212, "| raw - tc", "identity term"),
         ("target_correct", "both_correct", "artik_takdir_her_ikisi_eksi_hedef", 214, "| bc - tc",
          "marginal subsets removed"),
         ("both_correct", "successful_source", "bas_kaynak_eksi_her_ikisi_dogru", 215, "| ss - bc", "source robustness")]


def veri():
    d, k_seeds, per_seed = PS.load_and_check(Path(DATA))
    P, A = d["protokoller"], d["ayrisim"]
    if d["kaynak"] != SRC:
        K.fail(f"{DATA}: kaynak {d['kaynak']} != {SRC}")
    if K.sha(SRC) != d["kaynak_sha256"]:
        K.fail(f"{SRC} changed since {DATA} was written (sha256)")
    foy = K.Foy()
    for p_ in PROTOCOLS:
        ln, anc = FOY_ROW[p_]
        foy.kontrol(f"{p_}: asimetri_ort", P[p_]["asimetri_ort"], ln, anc, 2)
        foy.kontrol(f"{p_}: asimetri_sd", P[p_]["asimetri_sd"], ln, anc, 2)
        foy.kontrol(f"{p_}: n_CNN_to_ViT", P[p_]["n_CNN_to_ViT"], ln, anc, 0)
        foy.kontrol(f"{p_}: n_ViT_to_CNN", P[p_]["n_ViT_to_CNN"], ln, anc, 0)
        for i_, v_ in enumerate(P[p_]["asimetri_tohum_degerleri"]):
            foy.kontrol(f"{p_}: seed pair {i_ + 1}", v_, 805 + i_, f"| cift {i_ + 1} |", 2)
    foy.metin("per-pair table columns", "ort.$\\pm$SD", 808, "| ort.$\\pm$SD |")
    foy.kontrol("yayilim", A["yayilim"], 60, "Protokol yayilimi", 2)
    for a, b, key, ln, anc, _ in STEPS:
        foy.kontrol(key, A[key], ln, anc, 2)
        sgn = 1 if key.startswith("ozdeslik") else -1     # raw - tc is A - B; the other two are lower - upper
        foy.esit(f"{key} == means", A[key], sgn * (P[a]["asimetri_ort"] - P[b]["asimetri_ort"]), 0.0101,
                 "connector distance from the protocol means (one rounding unit per operand)")
    tex = Path(TEX).read_text(encoding="utf-8")
    if "\\label{tab:protocol_masks}" not in tex:
        K.fail(f"{TEX}: tab:protocol_masks not found")
    for p_, (_, cell) in MASK.items():
        if cell not in tex:
            K.fail(f"{TEX}: mask row {cell!r} not found; the words in the boxes would no longer follow Table 2")
    return d, k_seeds, foy.bitir()


def main():
    d, k_seeds, foy = veri()
    P, A = d["protokoller"], d["ayrisim"]
    O.basla(ARGS.uslup)
    import matplotlib.transforms as mtransforms
    from matplotlib.patches import Rectangle
    from motor.figspec import cards
    from motor.figspec.cvd import hex_to_rgb, relative_luminance

    ST, U = O.ST, O.U
    vg = O.vg()
    E = {p: O.ent(ENT[p]) for p in PROTOCOLS}
    W = O.W("single")
    H = 118.0
    M, GY = 0.5, 1.6
    TOP_H = 60.0
    cv = cards.Canvas("single", H, naming_step=4, naming_kind="serit")
    # ---------------- top card: nested sets
    a = cv.card(None, "Conditioning sets", M, M, W - 2 * M, TOP_H, tint="kap",
                n_exempt="set definitions with image counts")
    BAND_L, INS, BOT = 9.4, 2.6, 1.5
    x0, y0 = a.x + 2.0, a.y + cards.BAND + 0.6
    x1, y1 = a.x + a.w - 2.0, a.y + a.h - 9.0
    for i, p in enumerate(PROTOCOLS):
        bx, by = x0 + i * INS, y0 + i * BAND_L
        bw, bh = (x1 - i * INS) - bx, (y1 - i * BOT) - by
        fill = E[p].hex
        cv.fig.add_artist(Rectangle(cv.inches(bx, by + bh), bw / 25.4, bh / 25.4, transform=cv.fig.dpi_scale_trans,
                                    facecolor=fill, edgecolor=U.ink, linewidth=ST.weights.axis, zorder=-5 + i))
        tc = U.ink if relative_luminance(hex_to_rgb(fill)) > 0.12 else "#FFFFFF"
        n1, n2 = P[p]["n_CNN_to_ViT"], P[p]["n_ViT_to_CNN"]
        nlab = f"N = {n1:,}" if n1 == n2 else f"N = {n1:,} / {n2:,}"
        cv.text(bx + 1.6, by + 2.9, NAME[p], fontsize=ST.type_scale.annot, fontweight="semibold", color=tc,
                va="center", ha="left")
        cv.text(bx + bw - 1.6, by + 2.9, nlab, fontsize=ST.type_scale.annot, color=tc, va="center", ha="right")
        cv.text(bx + 1.6, by + 6.6, MASK[p][0], fontsize=ST.type_scale.annot, color=tc, va="center", ha="left",
                style="italic")
    # duzeltme turu 2: N is the mean over the three seed pairs (c1_transfer_summary n_cond_*.mean,
    # rounded; foy line 31 'Ortak kume n = 7061+-68'), said in the footnote
    cv.text(a.x + a.w / 2, a.y + a.h - 4.6, "N: mean over the three seed pairs;\nCNN→ViT / ViT→CNN where the two differ",
            fontsize=ST.type_scale.annot, color=U.muted, ha="center", va="center", linespacing=1.4)
    # ---------------- bottom card: asymmetry per protocol
    by0 = M + TOP_H + GY
    b = cv.card(None, "Measured asymmetry", M, by0, W - 2 * M, H - M - by0, tint="kap",
                note=f"n = {k_seeds} seed pairs")
    L, R, T, B = 23.5, 20.5, cards.BAND + 1.0, 9.5
    ax = b.axes(left=L, right=R, top=T, bottom=B, grid=None)
    O.eksen(ax, base="x", grid="x")
    ys = {p: i for i, p in enumerate(PROTOCOLS)}
    ms, ms_s, mew = vg["ortalama_markersize_pt"], vg["tohum_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    cizilen = {}
    for p in PROTOCOLS:
        y = ys[p]
        m_, sd = P[p]["asimetri_ort"], P[p]["asimetri_sd"]
        sv = P[p]["asimetri_tohum_degerleri"]
        O.hata(ax, E[p].key, [m_], [y], kind="sd", xerr=[sd], ecolor=U.ink, zorder=3, capsize=0,
               tanim="+-1 SD (ddof = 1) of the asymmetry over the three seed pairs (asimetri_sd)")
        ax.plot(sv, [y - 0.22] * len(sv), ls="none", marker="o", ms=ms_s, mfc="white", mec=U.ink,
                mew=ST.weights.emph, zorder=4)
        ax.plot([m_], [y], ls="none", marker=E[p].marker, ms=ms, mfc=E[p].hex, mec=U.ink, mew=mew, zorder=5)
        ax.text(1.0 + 1.5 / (b.w - L - R), y, f"{m_:.2f}±{sd:.2f}", transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=ST.type_scale.annot, color=U.ink, clip_on=False)
        cizilen[p] = {"ort": m_, "sd": sd, "tohumlar": sv, "n_CNN_to_ViT": P[p]["n_CNN_to_ViT"],
                      "n_ViT_to_CNN": P[p]["n_ViT_to_CNN"]}
    for a_, b_, key, ln, anc, lab in STEPS:
        ya, yb = ys[a_], ys[b_]
        xa, xb = P[a_]["asimetri_ort"], P[b_]["asimetri_ort"]
        ym = (ya + yb) / 2
        ax.plot([xa, xa, xb, xb], [ya + 0.28, ym, ym, yb - 0.28], color=U.muted, lw=ST.weights.grid,
                zorder=2, solid_joinstyle="miter")
        cizilen[key] = A[key]
    ax.set_xlim(0, 25)
    ax.set_ylim(len(PROTOCOLS) - 0.45, -0.55)
    ax.set_yticks(range(len(PROTOCOLS)))
    ax.set_yticklabels([NAME[p].replace("Successful-", "Successful-\n") for p in PROTOCOLS], linespacing=1.4)
    ax.set_xlabel("CNN→ViT − ViT→CNN (pts)", labelpad=1)
    O.tick_fmt(ax, "x")
    # connector distances in the free right-hand part of the plot, between the rows they join
    trb = mtransforms.blended_transform_factory(ax.transData, ax.transData)
    for a_, b_, key, ln, anc, lab in STEPS:
        ym = (ys[a_] + ys[b_]) / 2
        xm = (P[a_]["asimetri_ort"] + P[b_]["asimetri_ort"]) / 2
        if key == "artik_takdir_her_ikisi_eksi_hedef":
            # the short step (about 6 mm): its number stands right of the step's corner, on its level
            # (duzeltme turu 2: left of the step it ran over the x = 0 axis into the row names)
            xr = max(P[a_]["asimetri_ort"], P[b_]["asimetri_ort"])
            pos = dict(x=xr + 0.5, y=ym, ha="left", va="center")
        else:
            pos = dict(x=xm, y=ym + 0.07, ha="center", va="top")
        ax.text(pos["x"], pos["y"], f"{A[key]:.2f}", transform=trb, ha=pos["ha"], va=pos["va"],
                fontsize=ST.type_scale.annot, color=U.muted, style="italic", zorder=6)
    cv.title_strip([a])
    cv.title_strip([b])
    deg = []
    for p in PROTOCOLS:
        ln = FOY_ROW[p][0]
        for f in ("asimetri_ort", "asimetri_sd", "n_CNN_to_ViT", "n_ViT_to_CNN"):
            deg.append(O.deger(f"{p} {f}", P[p][f], DATA, f"protokoller.{p}.{f}", "read as stored; == foy", ln))
        for i_, v_ in enumerate(P[p]["asimetri_tohum_degerleri"]):
            deg.append(O.deger(f"{p} seed pair {i_ + 1}", v_, DATA, f"protokoller.{p}.asimetri_tohum_degerleri[{i_}]",
                               "read as stored; == foy (2 dp)", 805 + i_))
    S = K.load_json(SRC)
    for p in PROTOCOLS:
        for f, sk in (("n_CNN_to_ViT", "n_cond_CNN_to_ViT"), ("n_ViT_to_CNN", "n_cond_ViT_to_CNN")):
            mv = K.dig(S, f"protocols.{p}.{sk}.mean")
            if round(mv) != P[p][f]:
                K.fail(f"{p} {f}: {P[p][f]} != round(mean {mv}) in {SRC}")
            deg.append(O.deger(f"{p} {f} (mean over the three seed pairs)", mv, SRC, f"protocols.{p}.{sk}.mean",
                               "printed as N, rounded; == fig_protokol_kumeleri_veri.json", FOY_ROW[p][0]))
    for a_, b_, key, ln, anc, lab in STEPS:
        deg.append(O.deger(f"connector {lab}", A[key], DATA, f"ayrisim.{key}", "read as stored; == foy (2 dp)", ln))
    O.kaydet(cv, STEM, message=("The measured asymmetry depends on the conditioning set: it is smallest on the "
                                "target-correct set and largest on the successful-source set."),
             inputs=[DATA, SRC, TEX], degerler=deg, foy=foy,
             okunan={DATA: ["protokoller.<p>.{asimetri_ort, asimetri_sd, asimetri_tohum_degerleri, n_CNN_to_ViT, "
                            "n_ViT_to_CNN}", "ayrisim.*", "ic_icelik_tutuyor", "kaynak", "kaynak_sha256"],
                     SRC: ["sha256 only (the source of DATA)"],
                     TEX: ["tab:protocol_masks rows (definitions printed in words, not numbers)"]},
             cizilen=cizilen,
             notlar=["The nested boxes are schematic, not area-proportional; the CNN->ViT nesting is drawn.",
                     f"The spread ({A['yayilim']:.2f} pts, successful-source minus target-correct, foy line 60) is "
                     "checked but not printed; the caption carries it.",
                     "Mask wording: Table 2 (tab:protocol_masks) in words; the loose reading of successful-source is "
                     "a sensitivity analysis and is not drawn."],
             kararlar=["Karar (duzeltme turu 2): the footnote says N is the mean over the three seed pairs "
                       "(checked against c1_transfer_summary.json n_cond_*.mean), the SD line is drawn through "
                       "annotate.errorbar (kind sd, recorded in the manifest), and '3.91' stands right of its "
                       "step; the top card grows by 3 mm (height 118 mm, ceiling 120).",
                       "Karar: the three connector distances are printed as numbers on their steps and the "
                       "terms (identity term, marginal subsets removed, source robustness) go to the caption, because "
                       "at single-column width the term names collide with the row values at any height under the "
                       "120 mm ceiling; mean and SD stand in a value column right of the axis (data axis share "
                       "stays above 0.45).",
                       "Karar: letters A-D and (a)/(b) are removed and the two cards are named by a title strip "
                       "(plan section 8, rule branch 5), protocol names stand in the boxes and at the rows.",
                       "Karar: the sets are filled with the protocol family's four purples, because the blue scale "
                       "of the council figure collides with R224's #0072B2 (plan 9.14).",
                       "Karar: the masks are written in words, because mathtext subscripts would print under the "
                       "8 pt floor (trap 6)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tasarim_izgarasi")
    O.ajan(STEM, iddia="top card defines the sets, bottom card measures the asymmetry in each",
           dogrudan_etiket="protocol names stand in the boxes and at the rows; distances are printed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
