#!/usr/bin/env python3
"""Hakem turu 3 - CERCEVE duzeltmeleri (Ingilizce).

Defter: results/q1_research/HAKEM_TURU3_DEFTER.md bolum A ve B.
Yinelenebilir; tum eslesmeler dogrulanmadan hicbir dosya yazilmaz.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # ================= A1: MANSET AYRISTIRMASI =================
    ("04_experiments.tex",
     r"the mean per-seed spread between the largest and the smallest protocol "
     r"estimate is $15.01\pm0.84$ points, a factor of 4.4, whereas the seed-level "
     r"standard deviation within any single protocol stays below 1.5 points.",

     r"the mean per-seed spread between the largest and the smallest protocol "
     r"estimate is $15.01\pm0.84$ points, a factor of 4.4, whereas the seed-level "
     r"standard deviation within any single protocol stays below 1.5 points. "
     r"That spread is not a single quantity, and separating it is part of the "
     r"result. Ordering the four estimates gives three adjacent gaps: $3.91$ "
     r"points between target-correct and both-correct, the two protocols we "
     r"endorse for directional claims and which differ only in whether the source "
     r"must also be correct; $5.30$ points between both-correct and the "
     r"unconditioned rate, a gap that Equation~\eqref{eq:raw_identity} below "
     r"predicts in closed form and that a reader can therefore undo given the "
     r"target's clean error; and $5.80$ points between the unconditioned and the "
     r"successful-source rate, which conditions on the source's own white-box "
     r"failure and so estimates a different quantity. Only the first is "
     r"irreducible discretion between two defensible readings of the same "
     r"question, and at $3.91$ points it is still more than twice what retraining "
     r"both architectures moves. The corresponding endorsed-protocol gap is "
     r"$5.96$ points on CIFAR-100 and $0.65$ on SVHN.",
     "A1 manset ayristirmasi"),

    # ================= B3: TOST yonu =================
    ("04_experiments.tex",
     r"and TOST equivalence rejected at all three margins ($\pm1$, $\pm2$ and "
     r"$\pm3$ points, $p=1.0$ in each); under the target-correct protocol",
     r"and TOST unable to establish equivalence at any of the three margins "
     r"($\pm1$, $\pm2$ and $\pm3$ points, $p=1.0$ in each), the interval lying "
     r"entirely outside $\pm3$; under the target-correct protocol",
     "B3 TOST yonu"),

    # ================= B2: bootstrap GA durustlugu =================
    ("04_experiments.tex",
     r"the difference is $8.27\pm0.24$ points, differing in the third decimal from "
     r"the $\pm0.23$ of the table only because the two estimators differ, with a "
     r"paired bootstrap CI of $[7.33, 9.22]$, a sign-flip permutation "
     r"$p<5\times10^{-5}$ in every seed,",
     r"the difference is $8.27\pm0.24$ points, differing in the third decimal from "
     r"the $\pm0.23$ of the table only because the two estimators differ. Each run "
     r"has its own paired bootstrap CI ($[7.61, 9.44]$, $[7.10, 9.01]$ and "
     r"$[7.28, 9.20]$); we summarize them by the average of their endpoints, "
     r"$[7.33, 9.22]$, which is a description of three intervals and not itself an "
     r"interval with a coverage guarantee, and we give the across-run $t$ interval, "
     r"$[7.68, 8.86]$, for the inference that is actually at the run level. The "
     r"sign-flip permutation $p$ is below $5\times10^{-5}$ in every seed,",
     "B2 bootstrap GA"),

    # ================= A4: SVHN provenansi =================
    ("04_experiments.tex",
     r"The pool for this fit is the one fixed in the pre-registration, which "
     r"assigns the SVHN pair to an independent consistency check rather than to "
     r"the fitted points. Adding its two directions,",
     r"The pool for this fit excludes the SVHN pair, and we record how that "
     r"exclusion arose because it is not what the pre-registration says. The "
     r"registration placed SVHN in the fitted arm and named it as the pair that "
     r"would occupy the empty band below twelve points on the $x$ axis; its "
     r"reassignment to an independent consistency check was written after the "
     r"SVHN result was in hand. We therefore treat the SVHN-inclusive fit as the "
     r"pre-registered one. Adding its two directions,",
     "A4 SVHN provenansi"),

    # ---- A4 devami: duyarliligin okunusu tersine cevrilir ----
    ("04_experiments.tex",
     r"while the three-protocol slope keeps both its sign and its interval. We "
     r"report the sensitivity rather than absorb it, because it shows how thinly "
     r"the four-protocol slope is supported.",
     r"while the three-protocol slope keeps both its sign and its interval "
     r"($+0.470$, CI $[+0.361, +0.665]$). The four-protocol slope is therefore not "
     r"supported in the pre-registered pool, and we withdraw it; the mechanism "
     r"claim rests on the three-protocol slope, which survives the pool question "
     r"and is the quantity Section~\ref{subsec:statistics_results} carries forward.",
     "A4 duyarlilik okunusu"),

    # ================= B5: A kolu "survives" =================
    ("04_experiments.tex",
     r"and the controlled arm's slope survives dropping early checkpoints "
     r"($+0.201$ to $+0.492$ across thresholds), with the three-protocol slope the "
     r"most stable quantity of all ($0.661$ to $0.673$).",
     r"and the controlled arm's four-protocol slope keeps its sign but not its "
     r"magnitude when early checkpoints are dropped, moving over $+0.201$ to "
     r"$+0.492$ across thresholds, a range its own interval of $[+0.219, +0.371]$ "
     r"does not cover; the three-protocol slope is the most stable quantity of all "
     r"($0.661$ to $0.673$).",
     "B5 A kolu kaldirac"),

    # ================= B6: L2 ucuncu ongoru =================
    ("04_experiments.tex",
     r"All three registered predictions hold: the protocol spread is $10.92$ "
     r"points under $L_2$ against $15.01$ under $\Linf$, so it is smaller under "
     r"the changed norm but stays far above the two-point floor the "
     r"pre-registration set and an order of magnitude above the run-to-run "
     r"standard deviation. The sign is positive in all twelve measurements, and "
     r"the deviation of unconditioned from conditioned rates still rises with the "
     r"target's clean error (slope $+0.914$; we report the slope rather than a "
     r"correlation because the eighteen directions take only seven distinct "
     r"target-error values, six of them the same fixed WideResNet, so a "
     r"correlation over them would overstate the precision in the way "
     r"Section~\ref{subsec:transfer} describes).",

     r"Two of the three registered predictions hold and the third turns out not to "
     r"be testable. The protocol spread is $10.92$ points under $L_2$ against "
     r"$15.01$ under $\Linf$, so it is smaller under the changed norm but stays far "
     r"above the two-point floor the pre-registration set and an order of magnitude "
     r"above the run-to-run standard deviation. The sign is positive in all twelve "
     r"measurements. The third prediction, that the deviation of unconditioned from "
     r"conditioned rates would rise with the target's clean error, cannot fail once "
     r"Equation~\eqref{eq:raw_identity} holds: the deviation \emph{is} "
     r"$e\,(1 - r_{\text{cond}})$, so it rises with $e$ by construction, and the "
     r"fitted slope of $+0.914$ estimates $1 - r_{\text{cond}}$ rather than testing "
     r"anything. We registered it before writing the identity down; we now report it "
     r"as an out-of-sample check on the identity, which is the status we also give "
     r"it in Section~\ref{subsec:cifar100}.",
     "B6 L2 ucuncu ongoru"),

    # ---- B6 devami: :274'teki tekrar kisaltilir ----
    ("04_experiments.tex",
     r"The slope also confirms the identity out of sample. "
     r"Equation~\eqref{eq:raw_identity} predicts a slope of $1-r_{\text{cond}}$ "
     r"averaged over targets. Conditioned rates are far lower under this $L_2$ "
     r"budget than under $\Linf$ (roughly $2$ to $9\%$ against $9$ to $22\%$), so "
     r"the identity predicts a \emph{steeper} slope, and the measured $0.914$ sits "
     r"where it should, against $0.762$ on the same models under $\Linf$.",
     r"That check passes. Conditioned rates are far lower under this $L_2$ budget "
     r"than under $\Linf$ (roughly $2$ to $9\%$ against $9$ to $22\%$), so the "
     r"identity predicts a \emph{steeper} slope, and the measured $0.914$ sits "
     r"where it should, against $0.762$ on the same models under $\Linf$.",
     "B6 L2 tekrar"),

    # ================= A3: Yu ve ark. =================
    ("02_related_work.tex",
     r"Yu et al.~\cite{yu2025reliable} report that transferability is "
     r"systematically overestimated when it is measured across a single "
     r"architecture family and propose three evaluation protocols in response. "
     r"Both hold the scoring rule fixed and vary the attack and the model pool. "
     r"We do the opposite: the models, the data and the attack budget are fixed, "
     r"and only the scoring rule changes, which isolates the contribution of the "
     r"protocol itself and makes it possible to state the arithmetic relation "
     r"between the resulting estimates.",

     r"Yu et al.~\cite{yu2025reliable} report that transferability is "
     r"systematically overestimated when it is measured across a single "
     r"architecture family, and propose three evaluation protocols that differ in "
     r"how a multi-target outcome is scored: treating an ensemble as a single "
     r"target, counting how many targets are fooled, and requiring that all of "
     r"them are. TA-Bench holds the scoring rule fixed and varies the attack and "
     r"the model pool; Yu et al.\ vary the scoring rule along the "
     r"target-aggregation axis. We vary it along the conditioning axis instead, "
     r"with the models, the data and the attack budget fixed, which isolates the "
     r"contribution of the conditioning set and makes it possible to state the "
     r"arithmetic relation between the resulting estimates.",
     "A3 Yu ve ark."),

    # ================= A2: TRADES ozdesligi =================
    ("04_experiments.tex",
     r"We previously stated this result as a Pearson correlation ($r = 0.997$ over "
     r"six directions drawn from three targets) and that phrasing understated it:",

     r"The algebra itself is not new. Written over one model rather than a "
     r"source-target pair, $r_{\text{raw}} = e + r_{\text{cond}}(1 - e)$ is the "
     r"natural-plus-boundary decomposition of TRADES~\cite{zhang2019theoretically}, "
     r"where the premise corresponding to our $p$ holds by definition because the "
     r"boundary term is defined by an existential quantifier over the perturbation "
     r"neighborhood. What is new here is that in the transfer setting the premise "
     r"is not definitional: a fixed source-crafted perturbation either preserves "
     r"the target's clean error or does not, so $p$ becomes an empirical quantity, "
     r"and we measure it rather than assume it. We previously stated this result "
     r"as a Pearson correlation ($r = 0.997$ over six directions drawn from three "
     r"targets) and that phrasing understated it:",
     "A2 TRADES ozdesligi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
