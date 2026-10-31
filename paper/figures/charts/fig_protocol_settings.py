#!/usr/bin/env python
"""Transfer asymmetry under the four conditioning protocols in every setting (Y7, replaces Table 13
of the manuscript, tab:protocol_settings); card figure, visio-cizici style 7 (plan
04_cizim_plani.md section 9.13).

    python paper/figures/charts/fig_protocol_settings.py --uslup 7

Single column, one card (naming step 1). Rows are the settings (CIFAR-10 L-inf, CIFAR-100 L-inf,
SVHN L-inf, CIFAR-10 L2); inside a row each protocol has its own lane (Unconditioned,
Target-correct, Both-correct, Successful-source from top), marked with the protocol family's tone
and shape (paper palette, as in the protocol_sets figure). Settings with three seed pairs: mean
(filled mark) +- SD (line) and the pair values (open circles). SVHN has two pairs: both values are
drawn as filled marks joined by a thin line, with no mean and no SD, as in the table. The value
column at the right prints the spread (per-pair range over the four protocols, averaged over
pairs; SVHN both values).

Data: the four transfer summaries the reference sheet cites at line 153
(protocols.<p>.diff.values, protocol_spread_pp.values); every mean, SD and SVHN value against the
sheet table lines 159-163, the pair counts against line 165. A mismatch writes nothing.
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
ARGS = O.argumanlar(__doc__)
STEM = "protocol_settings"
SCRIPT = "paper/figures/charts/fig_protocol_settings.py"
SETTINGS = [("C10_Linf", "CIFAR-10, L∞", "results/c1_transfer/c1_transfer_summary.json", 1),
            ("C100_Linf", "CIFAR-100, L∞", "results/q1/cifar100/transfer/e1_transfer_summary.json", 2),
            ("SVHN_Linf", "SVHN, L∞", "results/q1/svhn/transfer/e7_transfer_summary.json", 3),
            ("C10_L2", "CIFAR-10, L₂", "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json", 4)]
PROTOCOLS = [("raw", "Unconditioned (raw)", "prot_raw", "Unconditioned"),
             ("target_correct", "Target-correct", "prot_target", "Target-correct"),
             ("both_correct", "Both-correct", "prot_both", "Both-correct"),
             ("successful_source", "Successful-source", "prot_success", "Successful-source")]
FOY_ROW = {"raw": 159, "target_correct": 160, "both_correct": 161, "successful_source": 162}


def cell(line, col):
    """The col-th data cell (1-based after the row label) of a sheet table line."""
    return line.split("|")[1 + col].strip()


def veri():
    foy = K.Foy()
    foy.metin("source line", "results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json", 153, "_Kaynak:")
    data = {}
    for key, lab, path, col in SETTINGS:
        J = K.load_json(path)
        P = K.dig(J, "protocols")
        rows = {}
        nrun = None
        for p, plab, _, _ in PROTOCOLS:
            v = list(K.dig(P, f"{p}.diff.values"))
            nrun = nrun or len(v)
            if len(v) != nrun:
                K.fail(f"{path}: {p} has {len(v)} pairs, others {nrun}")
            ln = FOY_ROW[p]
            anc = f"| {plab} |"
            txt = cell(foy.satir(ln, anc), col)
            if nrun >= 3:
                m, sd = statistics.mean(v), statistics.stdev(v)
                foy.esit(f"{key} {p} mean == JSON", m, K.dig(P, f"{p}.diff.mean"), 1e-9, "mean of pair values")
                foy.esit(f"{key} {p} SD == JSON", sd, K.dig(P, f"{p}.diff.std"), 1e-9, "SD ddof=1 of pair values")
                foy.kontrol(f"{key} {p} mean", m, ln, anc, 2)
                foy.kontrol(f"{key} {p} SD", sd, ln, anc, 2)
                if f"{abs(m):.2f}$\\pm${sd:.2f}" not in txt:
                    K.fail(f"{key} {p}: sheet cell {txt!r} does not print {m:.2f} +- {sd:.2f}")
            else:
                m = sd = None
                for i, x in enumerate(v):
                    foy.kontrol(f"{key} {p} pair {i + 1}", x, ln, anc, 2)
                if " / ".join(f"{x:+.2f}" for x in v) != txt:
                    K.fail(f"{key} {p}: sheet cell {txt!r} != the pair values {v}")
            rows[p] = {"values": v, "mean": m, "sd": sd}
        sp = list(K.dig(J, "protocol_spread_pp.values"))
        per = [max(rows[p]["values"][i] for p, *_ in PROTOCOLS) - min(rows[p]["values"][i] for p, *_ in PROTOCOLS)
               for i in range(nrun)]
        for a, b in zip(sp, per):
            foy.esit(f"{key} spread pair == max - min", a, b, 1e-9, "per-pair spread over the four protocols")
        sptxt = cell(foy.satir(163, "| Spread |"), col)
        if nrun >= 3:
            sm, ssd = statistics.mean(sp), statistics.stdev(sp)
            foy.kontrol(f"{key} spread mean", sm, 163, "| Spread |", 2)
            if f"{sm:.2f}$\\pm${ssd:.2f}" != sptxt:
                K.fail(f"{key}: sheet spread {sptxt!r} != {sm:.2f}+-{ssd:.2f}")
            spread_lab = f"{sm:.2f}"
        else:
            if " / ".join(f"{x:.2f}" for x in sp) != sptxt:
                K.fail(f"{key}: sheet spread {sptxt!r} != {sp}")
            spread_lab = " / ".join(f"{x:.2f}" for x in sp)
        if cell(foy.satir(165, "| Cift (kosum) sayisi |"), col) != str(nrun):
            K.fail(f"{key}: sheet pair count != {nrun}")
        foy.metin(f"{key} pair count", f"| {nrun}", 165, "| Cift (kosum) sayisi |")
        data[key] = {"label": lab, "path": path, "rows": rows, "spread": sp, "spread_lab": spread_lab, "n": nrun}
    return data, foy.bitir()


def main():
    data, foy = veri()
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    E = {p: O.ent(e) for p, _, e, _ in PROTOCOLS}
    W = O.W("single")
    H = 84.0
    M = 0.5
    L, R, T, B = 24.0, 12.5, cards.BAND + 4.0, 27.0
    DY_SEED = -0.09   # seed pairs sit just above their lane (y grows downward), as in protocol_sets
    ms, ms_s, mew = vg["ortalama_markersize_pt"], vg["tohum_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    cv = cards.Canvas("single", H, naming_step=1, naming_kind="yok")
    c = cv.card(None, "Protocol by setting", M, M, W - 2 * M, H - 2 * M, tint="kap",
                note="n = 3 seed pairs (SVHN 2)")
    ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
    O.eksen(ax, base="x", grid="x")
    lane = {p: d for (p, *_), d in zip(PROTOCOLS, (-0.3, -0.1, 0.1, 0.3))}
    # duzeltme turu 2: the lightest protocol tone (#E7D4E8) is close to the grey plot area (#EAEAF2);
    # its mark takes the style's emphasis stroke as edge, the others the marker-edge token
    ew = {p: (ST.weights.emph if p == "raw" else mew) for p, *_ in PROTOCOLS}
    deg, cizilen = [], {}
    for r, (key, lab, path, col) in enumerate(SETTINGS):
        d = data[key]
        for p, plab, ek, short in PROTOCOLS:
            y = r + lane[p]
            row = d["rows"][p]
            e = E[p]
            if row["mean"] is not None:
                O.hata(ax, e.key, [row["mean"]], [y], kind="sd", xerr=[row["sd"]], ecolor=U.ink, zorder=3, capsize=0,
                       tanim="+-1 SD (ddof = 1) of the per-pair asymmetry over the three seed pairs; SVHN (two "
                             "pairs) has none")
                ax.plot(row["values"], [y + DY_SEED] * len(row["values"]), ls="none", marker="o", ms=ms_s,
                        mfc="white", mec=U.ink, mew=ST.weights.emph, zorder=4)
                ax.plot([row["mean"]], [y], ls="none", marker=e.marker, ms=ms, mfc=e.hex, mec=U.ink,
                        mew=ew[p], zorder=5)
            else:
                ax.plot(row["values"], [y] * len(row["values"]), color=U.ink, lw=ST.weights.grid, zorder=3)
                ax.plot(row["values"], [y] * len(row["values"]), ls="none", marker=e.marker, ms=ms, mfc=e.hex,
                        mec=U.ink, mew=ew[p], zorder=5)
            for i, v in enumerate(row["values"]):
                deg.append(O.deger(f"{lab} {short} pair {i + 1}", v, path, f"protocols.{p}.diff.values[{i}]",
                                   "read as stored; == foy (2 dp)", FOY_ROW[p]))
            if row["mean"] is not None:
                deg.append(O.deger(f"{lab} {short} mean", row["mean"], path, f"protocols.{p}.diff.values",
                                   "mean; == diff.mean (1e-9); == foy (2 dp)", FOY_ROW[p]))
                deg.append(O.deger(f"{lab} {short} SD", row["sd"], path, f"protocols.{p}.diff.values",
                                   "SD ddof=1; == diff.std (1e-9); == foy (2 dp)", FOY_ROW[p]))
        ax.text(1.0 + 1.5 / (c.w - L - R), r, d["spread_lab"].replace(" / ", " /\n"), transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=ST.type_scale.annot, color=U.ink, clip_on=False, linespacing=1.4)
        for i, v in enumerate(d["spread"]):
            deg.append(O.deger(f"{lab} spread pair {i + 1}", v, path, f"protocol_spread_pp.values[{i}]",
                               "max - min over the four protocols (1e-9)", 163))
        cizilen[key] = {"satirlar": d["rows"], "yayilim": d["spread"], "yayilim_etiketi": d["spread_lab"]}
    ax.text(1.0 + 1.5 / (c.w - L - R), -0.62, "spread", transform=ax.get_yaxis_transform(), ha="left", va="bottom",
            fontsize=ST.type_scale.annot, color=U.muted, style="italic", clip_on=False)
    ax.axvline(0.0, color=U.muted, lw=vg["referans_pt"], ls=(0, (3, 2)), zorder=1)
    ax.set_ylim(len(SETTINGS) - 0.5, -0.55)
    ax.set_yticks(range(len(SETTINGS)))
    ax.set_yticklabels([s[1] for s in SETTINGS])
    ax.set_xlabel("CNN→ViT − ViT→CNN (pts)", labelpad=1)
    ax.locator_params(axis="x", nbins=6)
    O.tick_fmt(ax, "x")
    kax = O.bos_eksen(cv, c.x + 1.5, c.y + c.h - 16.5, c.w - 3.0, 15.5)
    hs = [Line2D([], [], ls="none", marker=E[p].marker, ms=ms, mfc=E[p].hex, mec=U.ink, mew=ew[p], label=short)
          for p, _, _, short in PROTOCOLS]
    hs.insert(2, Line2D([], [], ls="none", marker="o", ms=ms_s, mfc="white", mec=U.ink, mew=ST.weights.emph,
                        label="seed pair"))
    hs.append(Line2D([], [], color=U.ink, lw=ST.weights.err, label="± SD"))
    # SVHN: two pairs, both drawn with the protocol mark on a thin line, no mean and no SD
    hs.insert(3, Line2D([], [], color=U.ink, lw=ST.weights.grid, ls="-", marker="o", ms=ms, mfc=U.muted, mec=U.ink,
                        mew=mew, markevery=[0, -1], label="SVHN: two pairs, no mean"))
    kax.legend(handles=hs, loc="center", ncol=2, frameon=False, handletextpad=0.3, columnspacing=1.0,
               labelspacing=0.25, borderaxespad=0.0)
    O.kaydet(cv, STEM, message=("The sign and size of the asymmetry depend on the protocol in every setting; in SVHN, "
                                "matched in clean accuracy, the sign itself changes with the protocol."),
             inputs=[s[2] for s in SETTINGS], degerler=deg, foy=foy,
             okunan={s[2]: ["protocols.<p>.diff.{values, mean, std}", "protocol_spread_pp.values"] for s in SETTINGS},
             cizilen=cizilen,
             notlar=["Lanes inside a row are fixed offsets per protocol; they carry no value.",
                     "SVHN has two seed pairs: both values are drawn, no mean, no SD (as in the table and the sheet).",
                     "Per-direction rates and the both-correct paired analysis of the sheet (lines 167-195) are not "
                     "drawn."],
             kararlar=["Karar (duzeltme turu 2): seed pairs are lifted 0.09 row units above their lane "
                       "(as in protocol_sets), so the SD whisker ends and the seed marks no longer coincide; the "
                       "SD is drawn through annotate.errorbar (kind sd); the Unconditioned mark takes the emphasis "
                       "stroke (0.55 pt) as edge instead of a darker palette tone (the palette is regenerated only "
                       "by _palet_uret.py); the key names the SVHN encoding ('SVHN: two pairs', protocol marks on "
                       "a thin line, no mean); 'L2' reads 'L₂'. Height 84 mm (ceiling 88).",
                       "Karar: protocol marks take the protocol family of the paper palette (tone and shape, as in "
                       "protocol_sets), and seed pairs are small open ink circles, because the two light purples "
                       "would vanish as open marks on the grey plot area.",
                       "Karar: the key stands under the axes inside the single card (naming step 1 allows one card)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tek_kart_veri")
    O.ajan(STEM, iddia="one card: the protocol effect in every setting",
           dogrudan_etiket="settings name the rows; the spread is printed at the right")
    return 0


if __name__ == "__main__":
    sys.exit(main())
