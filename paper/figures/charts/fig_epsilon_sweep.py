#!/usr/bin/env python
"""Robust accuracy under PGD-10 (L-inf) across the attack budget; card figure, visio-cizici
style 7 (plan 04_cizim_plani.md section 9.16).

    python paper/figures/charts/fig_epsilon_sweep.py --uslup 7

Single column, one card (naming step 1). Categorical x (clean, 2/255, 4/255, 8/255, 16/255;
equally spaced, not a linear epsilon axis), y robust accuracy (%). ResNet-18 AT and ViT-Tiny AT:
mean of the three C1 seed pairs with +-1 SD (ddof = 1); WRN-28-10 (RobustBench Gowal2020, one
checkpoint, no SD) as the external reference. Lines are labelled directly at their right end.

Data: results/c1_sweep/pair{1,2,3}/{resnet18,vit_tiny}/*_robustness_results.csv and
results/wrn_eval/wrn_eval_summary.json, the files the reference sheet cites at line 354; every
mean, SD and WRN value is compared with the sheet table (lines 360-364) and the WRN line 19.
Karar: the WRN-28-10 path is added to konsey_ortak.ALLOWED in this process only, because it lies
outside the quarantine-safe prefixes (results/c1_*, results/q1/*) but the sheet itself cites it
(line 354) and prints its values (lines 19, 360-364); konsey_ortak.py is not edited.
"""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _kart_ortak as O  # noqa: E402

K = O.K
WRN = "results/wrn_eval/wrn_eval_summary.json"
K.ALLOWED = tuple(K.ALLOWED) + (WRN,)   # see the module docstring (Karar); this process only
ARGS = O.argumanlar(__doc__)
STEM = "epsilon_sweep"
SCRIPT = "paper/figures/charts/fig_epsilon_sweep.py"
PAIRS = (1, 2, 3)
MODELS = [("resnet18", "ResNet-18 AT", "r32"), ("vit_tiny", "ViT-Tiny AT", "vit")]
EPS_LAB = ["clean", "2/255", "4/255", "8/255", "16/255"]
FOY_ROWS = {0: (360, "| 0 (temiz) |"), 1: (361, "| 2/255 |"), 2: (362, "| 4/255 |"), 3: (363, "| 8/255 |"),
            4: (364, "| 16/255 |")}


def csv_path(p, m):
    return f"results/c1_sweep/pair{p}/{m}/{m}_robustness_results.csv"


def veri():
    foy = K.Foy()
    foy.metin("source line cites the WRN file", WRN, 354, "_Kaynak:")
    J = K.load_json(WRN)
    eps = list(K.dig(J, "eps_sweep"))
    if len(eps) != 4:
        K.fail("expected four sweep budgets in the WRN file")
    data, inputs = {}, []
    for m, lab, ent in MODELS:
        vals = [[None] * 3 for _ in range(5)]
        for k, p in enumerate(PAIRS):
            path = csv_path(p, m)
            K.check_source(path)
            inputs.append(path)
            rows = list(csv.DictReader(Path(path).read_text(encoding="utf-8").splitlines()))
            for r in rows:
                if r["Model"] != m:
                    K.fail(f"{path}: model {r['Model']} != {m}")
                e = float(r["Epsilon"])
                if r["Attack"] == "clean" and e == 0.0:
                    i = 0
                elif r["Attack"] == "pgd":
                    hits = [j for j, v in enumerate(eps) if abs(v - e) < 1e-12]
                    if not hits:
                        continue
                    i = hits[0] + 1
                else:
                    continue
                if vals[i][k] is not None:
                    K.fail(f"{path}: duplicate row for eps index {i}")
                vals[i][k] = float(r["Accuracy"])
        if any(v is None for row in vals for v in row):
            K.fail(f"{m}: missing sweep values {vals}")
        mean = [statistics.mean(v) for v in vals]
        sd = [statistics.stdev(v) for v in vals]
        for i in range(5):
            ln, anc = FOY_ROWS[i]
            foy.kontrol(f"{m} {EPS_LAB[i]} mean", mean[i], ln, anc, 2)
            foy.kontrol(f"{m} {EPS_LAB[i]} sd", sd[i], ln, anc, 2)
        data[m] = {"label": lab, "ent": ent, "seeds": vals, "mean": mean, "sd": sd}
    R = K.dig(J, "results")
    keys = ["clean"] + [f"pgd10_eps{e:.5f}" for e in eps]
    wv = []
    for i, kk in enumerate(keys):
        if kk not in R:
            K.fail(f"{WRN}: results.{kk} missing")
        v = R[kk]["accuracy"]
        if R[kk]["n"] != 10000 or abs(v - 100.0 * R[kk]["correct"] / R[kk]["n"]) > 1e-9:
            K.fail(f"{WRN}: results.{kk} accuracy != 100 * correct / n")
        ln, anc = FOY_ROWS[i]
        foy.kontrol(f"WRN {EPS_LAB[i]}", v, ln, anc, 2)
        wv.append(v)
    foy.kontrol("WRN clean (line 19)", wv[0], 19, "WRN-28-10 (harici referans)", 2)
    foy.kontrol("WRN PGD 8/255 (line 19)", wv[3], 19, "WRN-28-10 (harici referans)", 2)
    data["wrn"] = {"label": "WRN-28-10", "ent": "panel", "mean": wv, "keys": keys}
    return data, inputs + [WRN], foy.bitir()


def main():
    data, inputs, foy = veri()
    O.basla(ARGS.uslup)
    from motor.figspec import cards

    ST, U = O.ST, O.U
    vg = O.vg()
    W = O.W("single")
    H = 62.0
    M = 0.5
    L, R, T, B = 12.0, 22.0, cards.BAND + 1.0, 9.0
    ms, mew = vg["ortalama_markersize_pt"], O.figspec.layout.marker_edge_pt(U)
    cv = cards.Canvas("single", H, naming_step=1, naming_kind="yok")
    c = cv.card(None, "Robust accuracy under PGD-10", M, M, W - 2 * M, H - 2 * M, tint="kap",
                note="n = 3 seed pairs")
    ax = c.axes(left=L, right=R, top=T, bottom=B, grid=None)
    O.eksen(ax, base="x", grid="y")
    xs = list(range(5))
    deg, cizilen = [], {}
    for key in ("wrn", "resnet18", "vit_tiny"):
        d = data[key]
        e = O.ent(d["ent"])
        if key != "wrn":
            O.hata(ax, e.key, xs, d["mean"], kind="sd", yerr=d["sd"], ecolor=e.hex, zorder=3,
                   tanim="+-1 SD (ddof = 1) over the three C1 seed pairs; WRN-28-10 has none (one model)")
        ax.plot(xs, d["mean"], color=e.hex, ls=e.ls, lw=ST.weights.line, marker=e.marker, ms=ms, mfc=e.hex, mec=U.ink,
                mew=mew, zorder=4)
        # duzeltme turu 2: the WRN label says it is one model (n = 3 seed pairs holds for the other two)
        lab_ = d["label"] + (chr(10) + "(one model)" if key == "wrn" else "")
        ax.text(1.0 + 1.5 / (W - 2 * M - L - R), d["mean"][-1], lab_, transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=ST.type_scale.annot, color=U.ink, clip_on=False, linespacing=1.4)
        cizilen[key] = {k: d[k] for k in d if k in ("mean", "sd", "seeds")}
        for i in range(5):
            ln = FOY_ROWS[i][0]
            if key == "wrn":
                deg.append(O.deger(f"WRN-28-10 {EPS_LAB[i]}", d["mean"][i], WRN, f"results.{d['keys'][i]}.accuracy",
                                   "read as stored; == 100 correct / n; == foy", ln))
            else:
                for k, p in enumerate(PAIRS):
                    deg.append(O.deger(f"{d['label']} {EPS_LAB[i]} pair {p}", d["seeds"][i][k], csv_path(p, key),
                                       f"row Attack={'clean' if i == 0 else 'pgd'}, Epsilon={'0.0' if i == 0 else 'eps_sweep[' + str(i - 1) + ']'}"
                                       ".Accuracy", "read as stored"))
                deg.append(O.deger(f"{d['label']} {EPS_LAB[i]} mean", d["mean"][i], csv_path(1, key) + " (+ pair2, pair3)",
                                   "Accuracy over the three pairs", "mean; == foy (2 dp)", ln))
                deg.append(O.deger(f"{d['label']} {EPS_LAB[i]} SD", d["sd"][i], csv_path(1, key) + " (+ pair2, pair3)",
                                   "Accuracy over the three pairs", "SD ddof=1; == foy (2 dp)", ln))
    ax.set_xticks(xs)
    ax.set_xticklabels(EPS_LAB)
    ax.set_xlim(-0.3, 4.3)
    ax.set_ylim(0, 100)
    ax.set_ylabel("accuracy (%)", labelpad=1)
    ax.set_xlabel("PGD-10 budget ε (L∞)", labelpad=1)
    ax.locator_params(axis="y", nbins=5)
    O.tick_fmt(ax, "y")
    for dd in deg:
        if " (+ pair2, pair3)" in dd["kaynak"]:
            dd["kaynak"] = dd["kaynak"].replace(" (+ pair2, pair3)", "")
            dd["hesap"] += " (pairs 1-3: " + ", ".join(csv_path(p, "<model>") for p in PAIRS) + ")"
    O.kaydet(cv, STEM, message="ResNet-18 AT stays above ViT-Tiny AT at every budget; WRN-28-10 is the external reference.",
             inputs=inputs, degerler=deg, foy=foy,
             okunan={"results/c1_sweep/pair*/*/*_robustness_results.csv": ["Model, Attack, Epsilon, Accuracy"],
                     WRN: ["eps_sweep", "results.{clean, pgd10_eps*}.{accuracy, correct, n}"]},
             cizilen=cizilen,
             notlar=["x is categorical (equal spacing), not a linear epsilon axis.",
                     "Error bars: +-1 SD over three seed pairs (ddof = 1); most are narrower than the mark.",
                     "The sweep runs (results/c1_sweep) are separate from Table I's runs; the 8/255 point is not identical "
                     "to Table I (the sheet's consistency table below line 364).",
                     "WRN-28-10: one RobustBench checkpoint (Gowal2020), no SD."],
             kararlar=["Karar (duzeltme turu 2): the WRN-28-10 line label reads 'WRN-28-10 (one model)' "
                       "in two lines (the card title and a longer note do not fit one 85 mm line), because WRN-28-10 is a single RobustBench checkpoint (foy line 356) and n = 3 did not hold "
                       "for it.",
                       "Karar: ResNet-18 AT takes the r32 colour, because the C1 ResNet-18 is the 32-pixel CIFAR "
                       "stem (palette label 'ResNet-18, CIFAR stem (R32)'); WRN-28-10 takes the robust CNN panel "
                       "colour.",
                       "Karar: direct labels at the line ends replace the legend (style 7 direct labelling)."],
             betik=SCRIPT + " --uslup " + ARGS.uslup, sablon="tek_kart_veri",
             ekstra={"karantina_istisnasi": {"yol": WRN, "foy_satirlari": [19, 354, 360, 361, 362, 363, 364],
                                             "gerekce": "the sheet cites this file (line 354) and prints its values"}})
    O.ajan(STEM, iddia="one card: accuracy against budget for three models",
           dogrudan_etiket="each line is named at its right end")
    return 0


if __name__ == "__main__":
    sys.exit(main())
