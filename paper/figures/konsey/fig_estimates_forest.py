#!/usr/bin/env python3
"""Registered estimates with 90% and 95% intervals on the log and logit scales (brief 12, section 6.8).

One column (3.5 in), two panels stacked.
(a) Contrasts on panel similarity sigma: H1 (A^sigma_scr) and H2 (I^sigma) on the log and logit
    scales, and the descriptive ImageNetV2 pair estimates (pair 1, pair 2, their mean A^sigma_IN,
    and the Liu scratch-row pair), drawn with open markers. Reference lines at 0, +-delta and at
    the registered H1 size threshold (-0.20).
(b) Directional terms: K-b (rho of the scratch ViT-Tiny) on CIFAR-10 and CIFAR-100 and H3 (A^rho),
    each on the log and logit scales, with the +-delta equivalence band.
Thick bars are 90% intervals, thin bars 95% intervals. Colour follows the council palette
(similarity green, direction orange); the marker carries the scale (circle log, diamond logit),
fill carries the status (filled registered, open descriptive). The ratio scale (points) is left out
because its unit differs (brief 12, 6.8 decision).

Inputs (quarantine-safe): results/q1/konsey_ayrisim_b4.json (b4.F_B4.karsitliklar.H{1,2,3}.{kestirim,
ci90, ci95}, b4.duyarlilik.yari_logit.H{1,2,3}.{kestirim, ci90, ci95}, meta.delta),
results/q1/konsey_ayrisim_b2.json and results/q1/konsey_b9_c100/b9_dondurulmus_b2.json (b2.F_B2.K-b.
{ort, ci90, ci95}, b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}),
results/q1/konsey_b8_imagenetv2/b8_betimsel.json (ciftler[k].{A_sigma, goruntu_bootstrap_ci90,
goruntu_bootstrap_ci95}, A_sigma_IN, A_sigma_scr_Liu). Every value is compared with
results/C1_REFERANS_FOYU.md (1526-1528, 1532, 1551, 1588, 1603, 1839, 1857, 1930-1931, 1938-1939).

    docker exec -w /workspace adeb_eval python -B paper/figures/konsey/fig_estimates_forest.py
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import konsey_ortak as K  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

SCRIPT_REL = "paper/figures/konsey/fig_estimates_forest.py"
J4P = "results/q1/konsey_ayrisim_b4.json"
J2P = "results/q1/konsey_ayrisim_b2.json"
J9P = "results/q1/konsey_b9_c100/b9_dondurulmus_b2.json"
J8P = "results/q1/konsey_b8_imagenetv2/b8_betimsel.json"


def est(d, k="kestirim"):
    return {"e": d[k], "c90": list(d["ci90"]), "c95": list(d["ci95"])}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", default="fig_estimates_forest")
    ap.add_argument("--width-in", type=float, default=K.SINGLE_IN)
    ap.add_argument("--height-in", type=float, default=4.9)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0, help="no randomness; kept for the log")
    args = ap.parse_args()

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

    # ---- figure ----
    K.style(args.seed)
    W, Hh = args.width_in, args.height_in
    fig = plt.figure(figsize=(W, Hh))
    fig.patch.set_facecolor("white")
    left, right = 0.425, 0.975
    na, nb = len(a_rows), len(b_rows)
    unit = 0.045
    top_a = 0.945
    ha_, hb_ = na * unit, nb * unit
    ax_a = fig.add_axes([left, top_a - ha_, right - left, ha_])
    top_b = top_a - ha_ - 0.10
    ax_b = fig.add_axes([left, top_b - hb_, right - left, hb_])
    cizilen = {}
    MK = {"log": "o", "logit": "D"}
    for ax, rws, ck, key in ((ax_a, a_rows, "sym", "a"), (ax_b, b_rows, "dir", "b")):
        col = K.COL[ck]
        for y, (lab, sc, st, d, n, _) in enumerate(rws):
            ax.plot(d["c95"], [y, y], color=col, lw=0.8, solid_capstyle="butt", zorder=3)
            ax.plot(d["c90"], [y, y], color=col, lw=2.6, solid_capstyle="butt", zorder=3)
            ax.plot([d["e"]], [y], ls="none", marker=MK[sc], ms=4.4 if sc == "log" else 3.8,
                    mfc=("white" if st == "desc" else col), mec=K.INK, mew=0.7, zorder=4)
            cizilen.setdefault(key, []).append({"satir": lab, "olcek": sc, "durum": st, "kestirim": d["e"],
                                                "ci90": d["c90"], "ci95": d["c95"], "foy_satiri": n})
        ax.set_yticks(range(len(rws)))
        ax.set_yticklabels([r[0] for r in rws])
        ax.set_ylim(len(rws) - 0.5, -0.6)
        ax.axvline(0, color=K.ZERO, lw=0.7, zorder=1)
        ax.tick_params(axis="y", length=0, pad=3)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:g}".replace("-", "−")))
    for v in (-delta, delta):
        ax_a.axvline(v, color=K.MUTE, lw=0.6, ls=(0, (4, 2)), zorder=1)
    ax_a.axvline(thr, color=K.MUTE, lw=0.6, ls=(0, (1, 1.5)), zorder=1)
    ax_a.axhline(3.5, color="#d0d0d0", lw=0.5, zorder=0)
    ax_b.axvspan(-delta, delta, color="#e4e4e4", lw=0, zorder=0)
    for y in (1.5, 3.5):
        ax_b.axhline(y, color="#d0d0d0", lw=0.5, zorder=0)
    ax_a.set_xlabel(r"contrast on panel similarity $\sigma$", labelpad=2)
    ax_b.set_xlabel(r"directional term $\rho$ or $A^{\rho}$", labelpad=2)
    for ax, lab in ((ax_a, "(a)"), (ax_b, "(b)")):
        K.panel_label(fig, 0.01, ax.get_position().y1 + 0.012, lab, va="bottom")
    hs = [Line2D([], [], ls="none", marker="o", ms=4.4, mfc=K.MUTE, mec=K.INK, mew=0.7, label="log scale"),
          Line2D([], [], ls="none", marker="D", ms=3.8, mfc=K.MUTE, mec=K.INK, mew=0.7, label="logit scale"),
          Line2D([], [], ls="none", marker="o", ms=4.4, mfc="white", mec=K.INK, mew=0.7, label="descriptive"),
          Line2D([], [], color=K.MUTE, lw=2.6, label="90% interval"),
          Line2D([], [], color=K.MUTE, lw=0.8, label="95% interval"),
          Line2D([], [], color=K.MUTE, lw=0.6, ls=(0, (4, 2)), label=r"$\pm\delta$ (a)"),
          Line2D([], [], color=K.MUTE, lw=0.6, ls=(0, (1, 1.5)), label="H1 size (a)"),
          Patch(facecolor="#e4e4e4", edgecolor="none", label=r"$\pm\delta$ band (b)")]
    fig.legend(handles=hs, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3, frameon=False, handletextpad=0.35,
               columnspacing=0.8, labelspacing=0.3, handlelength=1.6)

    min_pt = K.layout_checks(fig)
    R = fig.canvas.get_renderer()
    for ax in (ax_a, ax_b):
        if fig.legends[0].get_window_extent(R).overlaps(ax.get_tightbbox(R)):
            K.fail("legend overlaps an axes")
    out = K.OUTDIR
    pdf, png, moved = K.save(fig, out, args.name, args.dpi)
    okunan = {J4P: ["b4.F_B4.karsitliklar.H{1,2,3}.{kestirim, ci90, ci95}",
                    "b4.duyarlilik.yari_logit.H{1,2,3}.{kestirim, ci90, ci95}", "meta.delta"],
              J2P: ["b2.F_B2.K-b.{ort, ci90, ci95}", "b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}"],
              J9P: ["b2.F_B2.K-b.{ort, ci90, ci95}", "b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}"],
              J8P: ["ciftler[0..1].{cift, cnn, donusturucu, satir, A_sigma, goruntu_bootstrap_ci90, goruntu_bootstrap_ci95}",
                    "A_sigma_IN.{kestirim, goruntu_bootstrap.ci90, goruntu_bootstrap.ci95}",
                    "A_sigma_scr_Liu.{kestirim, goruntu_bootstrap.ci90, goruntu_bootstrap.ci95, beklenti_esigi}"]}
    cizilen["referans_cizgileri"] = {"sifir": 0.0, "delta": delta, "H1_buyukluk_esigi": thr}
    kp = K.write_kanit(out, args.name, SCRIPT_REL, sys.argv[1:], [J4P, J2P, J9P, J8P], (W, Hh), args.dpi, min_pt, okunan,
                       cizilen, foy_sonuc,
                       ["14 estimates x (point, 90% low/high, 95% low/high) vs foy (3 dp): 1526-1528, 1551, 1588, 1603, "
                        "1839, 1857, 1930-1931, 1938-1939",
                        "intervals nested around each estimate",
                        "delta vs foy 1532; H1 size threshold -0.20 vs foy 1526 and 1939",
                        "descriptive labels of A_sigma_IN and Liu present in foy (not drawn as words)",
                        "no text overlap, all text inside, >= 8 pt, legend clear of axes, no Type 3 font"],
                       ["ImageNetV2 intervals are image-bootstrap intervals (image uncertainty only, B = 2000), "
                        "not between-pair intervals; they are drawn with open markers as descriptive.",
                        "Ratio-scale (points) sensitivities are not drawn (different unit), per brief 12 section 6.8."],
                       moved)
    print(f"written: {pdf}\nwritten: {png}\nwritten: {kp}")
    print(f"foy comparisons {foy_sonuc['karsilastirma_sayisi']}, all matched; min font {min_pt}")


if __name__ == "__main__":
    main()
