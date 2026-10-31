#!/usr/bin/env python
"""Registered estimates with 90% and 95% intervals on the log and logit scales; card figure,
visio-cizici style 7 (plan 04_cizim_plani.md section 9.12).

    python paper/figures/charts/fig_estimates_forest.py --uslup 7

Single column, two stacked cards: contrasts on panel similarity sigma (green title: H1, H2 on the
log scale, the descriptive ImageNetV2 rows with image-bootstrap intervals, H1 and H2 on the logit
scale) and directional terms (orange title: K-b on CIFAR-10 and CIFAR-100 and H3, log then
logit). Thick bar 90% interval, thin line 95% interval; circle log scale, diamond logit scale,
open mark descriptive. The +-delta lines and the H1 size line (top card) and the +-delta band
(bottom card) are drawn over the log-scale rows only, for which the margin is registered.
Naming: step 4 with a colour code (the title colour carries the family, always with its name).

Data rule: copied verbatim from paper/figures/konsey/fig_estimates_forest.py main() (left
untouched; constants imported): 14 estimates x (point, 90% and 95% bounds) against the sheet
lines 1526-1528, 1551, 1588, 1603, 1839, 1857, 1930-1931, 1938-1939; delta line 1532; nested
intervals. A mismatch writes nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
import fig_estimates_forest as EF  # noqa: E402  (constants only)

ARGS = O.argumanlar(__doc__)
STEM = "estimates_forest"
SCRIPT = "paper/figures/charts/fig_estimates_forest.py"
J4P, J2P, J9P, J8P, est = EF.J4P, EF.J2P, EF.J9P, EF.J8P, EF.est
# council row label -> (printed row label, source file, key path of the estimate record)
SATIR = {
    # council row label -> (printed row label, source file, record path, estimate key, ci90 key, ci95 key)
    "H1, log": ("H1 log", J4P, "b4.F_B4.karsitliklar.H1", "kestirim", "ci90", "ci95"),
    "H2, log": ("H2 log", J4P, "b4.F_B4.karsitliklar.H2", "kestirim", "ci90", "ci95"),
    "H1, logit": ("H1 logit", J4P, "b4.duyarlilik.yari_logit.H1", "kestirim", "ci90", "ci95"),
    "H2, logit": ("H2 logit", J4P, "b4.duyarlilik.yari_logit.H2", "kestirim", "ci90", "ci95"),
    "ImageNetV2 pair 1": ("IN-V2 pair 1", J8P, "ciftler[0]", "A_sigma", "goruntu_bootstrap_ci90",
                          "goruntu_bootstrap_ci95"),
    "ImageNetV2 pair 2": ("IN-V2 pair 2", J8P, "ciftler[1]", "A_sigma", "goruntu_bootstrap_ci90",
                          "goruntu_bootstrap_ci95"),
    # A-bar (U+0100) with sigma and IN in function notation, as A(sigma, scr) in cells_interaction
    r"ImageNetV2 mean $\bar{A}^{\sigma}_{\mathrm{IN}}$": ("IN-V2 Ā(σ, IN)", J8P, "A_sigma_IN", "kestirim",
                                                         "goruntu_bootstrap.ci90", "goruntu_bootstrap.ci95"),
    "ImageNetV2 Liu (scratch)": ("IN-V2 Liu scr.", J8P, "A_sigma_scr_Liu", "kestirim", "goruntu_bootstrap.ci90",
                                 "goruntu_bootstrap.ci95"),
    "K-b CIFAR-10, log": ("K-b C10 log", J2P, "b2.F_B2.K-b", "ort", "ci90", "ci95"),
    "K-b CIFAR-10, logit": ("K-b C10 logit", J2P, "b2.duyarlilik.yari_logit.rho_V", "ort", "ci90", "ci95"),
    "K-b CIFAR-100, log": ("K-b C100 log", J9P, "b2.F_B2.K-b", "ort", "ci90", "ci95"),
    "K-b CIFAR-100, logit": ("K-b C100 logit", J9P, "b2.duyarlilik.yari_logit.rho_V", "ort", "ci90", "ci95"),
    "H3, log": ("H3 log", J4P, "b4.F_B4.karsitliklar.H3", "kestirim", "ci90", "ci95"),
    "H3, logit": ("H3 logit", J4P, "b4.duyarlilik.yari_logit.H3", "kestirim", "ci90", "ci95"),
}


def veri():
    J4, J2, J9, J8 = (K.load_json(p) for p in (J4P, J2P, J9P, J8P))
    foy = K.Foy()
    H = K.dig(J4, "b4.F_B4.karsitliklar")
    HL = K.dig(J4, "b4.duyarlilik.yari_logit")
    a_rows, b_rows = [], []  # (label, scale, status, estimate dict, foy line, anchor)
    for h, lab in (("H1", "H1"), ("H2", "H2")):
        a_rows.append((f"{lab}, log", "log", "reg", est(H[h]), {"H1": 1526, "H2": 1527}[h],
                       {"H1": "| H1, A^sigma_scr", "H2": "| H2, I^sigma"}[h]))
        a_rows.append((f"{lab}, logit", "logit", "reg", est(HL[h]), 1551, "| Logit olcek"))
    cif = K.dig(J8, "ciftler")
    for k, n in ((0, 1930), (1, 1931)):
        c = cif[k]
        if c["satir"] != "IN":
            K.fail(f"ImageNetV2 pair {k + 1} is not an IN-row pair")
        a_rows.append((f"ImageNetV2 pair {c['cift']}", "log", "desc",
                       {"e": c["A_sigma"], "c90": list(c["goruntu_bootstrap_ci90"]), "c95": list(c["goruntu_bootstrap_ci95"])},
                       n, f"| {c['cift']} | {c['cnn']} | {c['donusturucu']} |"))
    AIN, ALiu = K.dig(J8, "A_sigma_IN"), K.dig(J8, "A_sigma_scr_Liu")
    a_rows.append((r"ImageNetV2 mean $\bar{A}^{\sigma}_{\mathrm{IN}}$", "log", "desc",
                   {"e": AIN["kestirim"], "c90": list(AIN["goruntu_bootstrap"]["ci90"]), "c95": list(AIN["goruntu_bootstrap"]["ci95"])},
                   1938, "| A_sigma_IN"))
    a_rows.append(("ImageNetV2 Liu (scratch)", "log", "desc",
                   {"e": ALiu["kestirim"], "c90": list(ALiu["goruntu_bootstrap"]["ci90"]), "c95": list(ALiu["goruntu_bootstrap"]["ci95"])},
                   1939, "| A_sigma_scr_Liu"))
    for J, ds, lr, ll in ((J2, "CIFAR-10", 1588, 1603), (J9, "CIFAR-100", 1839, 1857)):
        b_rows.append((f"K-b {ds}, log", "log", "reg", est(K.dig(J, "b2.F_B2.K-b"), "ort"), lr, "| K-b, ViT yonlu terimi"))
        b_rows.append((f"K-b {ds}, logit", "logit", "reg", est(K.dig(J, "b2.duyarlilik.yari_logit.rho_V"), "ort"), ll,
                       "| Yari logit"))
    b_rows.append(("H3, log", "log", "reg", est(H["H3"]), 1528, "| H3, A^rho"))
    b_rows.append(("H3, logit", "logit", "reg", est(HL["H3"]), 1551, "| Logit olcek"))
    # m1 regrouping: log rows first (one contiguous block for the registered margin), logit rows last
    a_rows = ([r for r in a_rows if r[1] == "log" and r[2] == "reg"] + [r for r in a_rows if r[2] == "desc"]
              + [r for r in a_rows if r[1] == "logit"])
    b_rows = [r for r in b_rows if r[1] == "log"] + [r for r in b_rows if r[1] == "logit"]
    if any(r[1] != "log" for r in a_rows if r[2] == "desc"):
        K.fail("descriptive ImageNetV2 rows are expected on the log scale")
    for lab, _, _, d, n, anc in a_rows + b_rows:
        foy.kontrol(f"{lab}: estimate", d["e"], n, anc, 3)
        for nm in ("c90", "c95"):
            for i in range(2):
                foy.kontrol(f"{lab}: {nm}[{i}]", d[nm][i], n, anc, 3)
        if not (d["c95"][0] <= d["c90"][0] <= d["e"] <= d["c90"][1] <= d["c95"][1]):
            K.fail(f"{lab}: intervals not nested around the estimate")
    delta = K.dig(J4, "meta.delta")
    foy.metin("delta", f"delta = {delta}", 1532, "TOST esdegerlik siniri")
    thr = ALiu["beklenti_esigi"]
    foy.metin("H1 size threshold (Liu expectation)", f"esik {thr}", 1939, "| A_sigma_scr_Liu")
    foy.metin("H1 registered size", "(A <= -0,20)", 1526, "| H1, A^sigma_scr")
    foy.esit("H1 size threshold == -0.20 as registered", thr, -0.2, 1e-12, "Liu expectation is H1's predicted size")
    foy.metin("A_sigma_IN label", "beklentiyle uyumlu", 1938, "| A_sigma_IN")
    foy.metin("Liu label", "belirsiz", 1939, "| A_sigma_scr_Liu")
    foy_sonuc = foy.bitir()

    okunan = {J4P: ["b4.F_B4.karsitliklar.H{1,2,3}.{kestirim, ci90, ci95}",
                    "b4.duyarlilik.yari_logit.H{1,2,3}.{kestirim, ci90, ci95}", "meta.delta"],
              J2P: ["b2.F_B2.K-b.{ort, ci90, ci95}", "b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}"],
              J9P: ["b2.F_B2.K-b.{ort, ci90, ci95}", "b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}"],
              J8P: ["ciftler[0..1].{cift, cnn, donusturucu, satir, A_sigma, goruntu_bootstrap_ci90, goruntu_bootstrap_ci95}",
                    "A_sigma_IN.{kestirim, goruntu_bootstrap.ci90, goruntu_bootstrap.ci95}",
                    "A_sigma_scr_Liu.{kestirim, goruntu_bootstrap.ci90, goruntu_bootstrap.ci95, beklenti_esigi}"]}
    return dict(a=a_rows, b=b_rows, delta=delta, thr=thr), foy_sonuc, okunan


def main():
    D, foy, okunan = veri()
    a_rows, b_rows, delta, thr = D["a"], D["b"], D["delta"], D["thr"]
    for r in a_rows + b_rows:
        if r[0] not in SATIR:
            K.fail(f"row {r[0]!r} has no printed label / key path entry")
    O.basla(ARGS.uslup)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    E = {k: O.ent(k) for k in ("sym", "dir")}
    band = U.tones()["vurgu_kutusu"][0]
    W = O.W("single")
    H = 127.0
    M, GY, KEY_H, PITCH = 0.5, 1.6, 16.0, 5.0
    L, R, T, B = 24.0, 3.0, cards.BAND + 1.0, 9.5
    ms = vg["ortalama_markersize_pt"]
    MK = {"log": "o", "logit": "D"}
    cv = cards.Canvas("single", H, naming_step=4, naming_kind="renk")
    specs = [("a", a_rows, "sym", "Contrasts on panel similarity σ", "contrast on σ"),
             ("b", b_rows, "dir", "Directional terms", "directional term ρ or A(ρ)")]
    y0, kartlar, cizilen, deg = M, [], {}, []
    for key, rws, ck, title, xl in specs:
        ch = T + len(rws) * PITCH + B
        col = E[ck].hex
        c = cv.card(None, title, M, y0, W - 2 * M, ch, tint="kap", note=f"n = {len(rws)} estimates")
        c.artists["title"].set_color(col)
        ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
        O.eksen(ax, base="x", grid="x")
        O.aralik(ax, "ci90", "thick bar: 90% interval of the estimate (registered rows: the file's ci90; "
                 "ImageNetV2 rows: image-bootstrap ci90); kind outside annotate.ERRORBAR_KINDS, recorded so the "
                 "caption check (fig_qc D3) runs")
        O.aralik(ax, "ci95", "thin line: 95% interval of the estimate (registered rows: ci95; ImageNetV2 rows: "
                 "image-bootstrap ci95)")
        for y, (lab, sc, st, d, n, _) in enumerate(rws):
            ax.plot(d["c95"], [y, y], color=col, lw=ST.weights.err, solid_capstyle="butt", zorder=3)
            ax.barh(y, d["c90"][1] - d["c90"][0], left=d["c90"][0], height=0.22, color=col, edgecolor="none",
                    zorder=3)
            ax.plot([d["e"]], [y], ls="none", marker=MK[sc], ms=ms, mfc=("white" if st == "desc" else col),
                    mec=U.ink, mew=ST.weights.emph if st == "desc" else O.figspec.layout.marker_edge_pt(U), zorder=4)
            plab, src, kp, ek, k90, k95 = SATIR[lab]
            cizilen.setdefault(key, []).append({"satir": plab, "konsey_etiketi": lab, "olcek": sc, "durum": st,
                                                "kestirim": d["e"], "ci90": d["c90"], "ci95": d["c95"],
                                                "foy_satiri": n})
            for nm, v, yol in (("estimate", d["e"], f"{kp}.{ek}"), ("ci90 low", d["c90"][0], f"{kp}.{k90}[0]"),
                               ("ci90 high", d["c90"][1], f"{kp}.{k90}[1]"),
                               ("ci95 low", d["c95"][0], f"{kp}.{k95}[0]"),
                               ("ci95 high", d["c95"][1], f"{kp}.{k95}[1]")):
                deg.append(O.deger(f"{plab} {nm}", v, src, yol, "read as stored; == foy (3 dp); nested", n))
        ax.set_yticks(range(len(rws)))
        ax.set_yticklabels([SATIR[r[0]][0] for r in rws])
        ax.set_ylim(len(rws) - 0.5, -0.6)
        ax.axvline(0, color=U.muted, lw=vg["referans_pt"], zorder=1)
        idx = [i for i, r in enumerate(rws) if r[1] == "log"]
        if idx != list(range(len(idx))):
            K.fail("log rows are not a leading contiguous block")
        ylo, yhi = -0.6, idx[-1] + 0.5
        if key == "a":
            for v in (-delta, delta):
                ax.vlines(v, ylo, yhi, color=U.muted, lw=vg["referans_pt"], ls=(0, (4, 2)), zorder=1)
            ax.vlines(thr, ylo, yhi, color=U.muted, lw=vg["referans_pt"], ls=(0, (1, 1.5)), zorder=1)
            n_reg = sum(1 for r in rws if r[1] == "log" and r[2] == "reg")
            for yy in (n_reg - 0.5, len(idx) - 0.5):
                ax.axhline(yy, color=U.muted, lw=ST.weights.grid, zorder=1)
            ax.text(0.985, (n_reg - 0.5 + len(idx) - 0.5) / 2, "image\nbootstrap", transform=ax.get_yaxis_transform(),
                    ha="right", va="center", fontsize=ST.type_scale.annot, color=U.muted, style="italic",
                    linespacing=1.4)
        else:
            ax.fill_betweenx([ylo, yhi], -delta, delta, color=band, lw=0, zorder=0.5)
            ax.axhline(len(idx) - 0.5, color=U.muted, lw=ST.weights.grid, zorder=1)
        ax.set_xlabel(xl, labelpad=1)
        ax.locator_params(axis="x", nbins=6)
        O.tick_fmt(ax, "x")
        kartlar.append(c)
        y0 += ch + GY
    cv.title_strip(kartlar)
    key_c = cv.card(None, "", M, H - M - KEY_H, W - 2 * M, KEY_H, tint="white", n_exempt="a key to the marks")
    kax = O.anahtar_ekseni(cv, key_c)
    mew = O.figspec.layout.marker_edge_pt(U)
    hs = [Line2D([], [], ls="none", marker="o", ms=ms, mfc=U.muted, mec=U.ink, mew=mew, label="log scale"),
          Line2D([], [], ls="none", marker="D", ms=ms, mfc=U.muted, mec=U.ink, mew=mew, label="logit scale"),
          Line2D([], [], ls="none", marker="o", ms=ms, mfc="white", mec=U.ink, mew=ST.weights.emph, label="descriptive"),
          Patch(facecolor=U.muted, edgecolor="none", label="90% interval"),
          Line2D([], [], color=U.muted, lw=ST.weights.err, label="95% interval"),
          Line2D([], [], color=U.muted, lw=vg["referans_pt"], ls=(0, (4, 2)), label=f"±{delta:.2f}, log rows"),
          Line2D([], [], color=U.muted, lw=vg["referans_pt"], ls=(0, (1, 1.5)), label="H1 size, log rows"),
          Patch(facecolor=band, edgecolor="none", label=f"±{delta:.2f} band, log rows")]
    kax.legend(handles=hs, loc="center", ncol=2, frameon=False, handletextpad=0.35, columnspacing=1.0,
               labelspacing=0.3, handlelength=1.6, borderaxespad=0.0)
    cizilen["referans_cizgileri"] = {"sifir": 0.0, "delta": delta, "H1_buyukluk_esigi": thr,
                                     "yalniz_log_satirlarinda": True}
    deg.append(O.deger("delta", delta, J4P, "meta.delta", "read as stored; == foy 1532 text", 1532))
    deg.append(O.deger("H1 size threshold", thr, J8P, "A_sigma_scr_Liu.beklenti_esigi",
                       "read as stored; == -0.20 (foy 1526, 1939 text)", 1939))
    O.kaydet(cv, STEM, message=("Registered sigma contrasts and directional terms with 90% and 95% intervals on the "
                                "log and logit scales; the margin applies to log rows only."),
             inputs=[J4P, J2P, J9P, J8P], degerler=deg, foy=foy, okunan=okunan, cizilen=cizilen,
             notlar=["ImageNetV2 intervals are image-bootstrap intervals, not between-pair intervals; drawn open "
                     "as descriptive.",
                     "Ratio-scale sensitivities are not drawn (different unit), as in the council figure.",
                     "Row labels: C10 = CIFAR-10, C100 = CIFAR-100, IN-V2 = ImageNetV2, Liu scr. = the Liu "
                     "scratch-row pair."],
             kararlar=["Karar (duzeltme turu 2): the A-bar row reads 'IN-V2 Ā(σ, IN)' and the bottom "
                       "x label 'A(ρ)', in the function notation of cells_interaction, because super- and "
                       "subscripts print under the 8 pt floor and a bare 'A' named two different contrasts in two "
                       "figures; the caption maps them to A-bar^sigma_IN and A^rho.",
                       "Karar (duzeltme turu 2): the reference lines (+-delta, H1 size) already stop at the last "
                       "log-scale row (vlines from -0.6 to idx[-1] + 0.5); the verifier's finding holds for the "
                       "council figure, not for this one, so nothing changes there.",
                       "Karar: row labels are shortened (C10, C100, IN-V2) so the row-label column stays at "
                       "24 mm (plan section 6: at most 25 mm) and the value axis keeps over 0.45 of the width.",
                       "Karar: the 90% interval is a thin bar (an area) and the 95% interval the style's error "
                       "line, so no line weight is written in the script.",
                       "Karar: the +-delta band uses the style's vurgu_kutusu tone (orange family, as in "
                       "cells_interaction), because the grey band tone equals the plot area."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tasarim_izgarasi")
    O.ajan(STEM, iddia="top card sigma contrasts, bottom card directional terms",
           dogrudan_etiket="every row is named at its axis; titles name the family")
    return 0


if __name__ == "__main__":
    sys.exit(main())
