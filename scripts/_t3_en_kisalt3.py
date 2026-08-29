#!/usr/bin/env python3
"""Sayfa kisaltma - ucuncu gecis: Overfull duzeltmesi + siskinlik.

Kesilen hicbir sey OLCUM ya da IDDIA degildir; yalnizca ayni seyi iki kez
soyleyen ya da gereginden uzun anlatan ifadeler.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # ---- Overfull \hbox: tablo dipnotu satirlari cok genis ----
    ("04_experiments.tex",
     r"\multicolumn{4}{l}{\scriptsize $^\ddagger$CIFAR-native ViT control "
     r"(4$\times$4 patches, no upsampling; 5.4M params),}\\"
     "\n"
     r"\multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}a single checkpoint "
     r"predating the fixed-split protocol, selected on the test set,}\\"
     "\n"
     r"\multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}and included only for "
     r"the sign of the upsampling effect, not as a quantitative comparison.}",

     r"\multicolumn{4}{l}{\scriptsize $^\ddagger$CIFAR-native ViT control "
     r"(4$\times$4 patches, 5.4M params); a single}\\"
     "\n"
     r"\multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}checkpoint predating "
     r"the fixed-split protocol, selected on the}\\"
     "\n"
     r"\multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}test set, included "
     r"only for the sign of the upsampling effect.}",
     "Overfull tablo dipnotu"),

    # ---- seyreklik paragrafi sikistirma ----
    ("04_experiments.tex",
     r"The ordering is perfectly consistent, three runs out of three on every "
     r"measure, and the gap is several times the run-to-run standard deviation; "
     r"but with three runs it does not clear $\alpha=0.05$ after correction, and "
     r"the three measures are near-collinear, which makes Holm conservative here. "
     r"We therefore state the sparsity result as reproducible rather than as "
     r"significant, and we do not let the per-sample $p$-values carry the "
     r"architectural claim.",
     r"The ordering is consistent three runs out of three on every measure and the "
     r"gap is several times the run-to-run standard deviation, but with three runs "
     r"it does not clear $\alpha=0.05$ after a correction that is conservative "
     r"here because the three measures are near-collinear. We therefore report the "
     r"sparsity result as reproducible and not as significant.",
     "seyreklik sikistirma"),

    # ---- 05: yon paragrafi ----
    ("05_discussion.tex",
     r"The direction is a property of the unmatched regime, not of the "
     r"architectures. Within the unmatched regime what changes across protocols is "
     r"only how large the effect looks and whether an equivalence test accepts it; "
     r"once the models are matched, the sign changes too. Our three-target "
     r"analysis suggests a reading of this direction that does not require the "
     r"CNN's perturbations to be special: incoming transfer tracks each target's "
     r"own white-box vulnerability ($r = 0.986$ over three targets), and the most "
     r"robust target absorbs attacks from both families almost equally.",
     r"The direction is a property of the unmatched regime, not of the "
     r"architectures: while the models are unmatched the protocol changes only how "
     r"large the effect looks and whether equivalence is accepted, and once they "
     r"are matched it changes the sign as well. Our three-target analysis reads "
     r"this direction without requiring the CNN's perturbations to be special: "
     r"incoming transfer tracks each target's own white-box vulnerability "
     r"($r = 0.986$), and the most robust target absorbs both families almost "
     r"equally.",
     "05 yon paragrafi"),

    # ---- 04: kosullu ayrisma paragrafi ----
    ("04_experiments.tex",
     r"It starts from a 12.3-point higher clean accuracy \emph{and} loses a "
     r"smaller fraction of what it solves, with conditional fooling of $48.58$ "
     r"versus $55.53\%$ under PGD-10 and $55.78$ versus $60.37\%$ under "
     r"AutoAttack. On the jointly solved subset, the $n=7{,}061\pm68$ samples that "
     r"both models of a pair classify correctly on clean inputs and therefore an "
     r"exactly paired comparison on shared inputs, the CNN leads by 13.8 and 10.7 "
     r"points",
     r"It starts from a 12.3-point higher clean accuracy \emph{and} loses a "
     r"smaller fraction of what it solves, with conditional fooling of $48.58$ "
     r"versus $55.53\%$ under PGD-10 and $55.78$ versus $60.37\%$ under "
     r"AutoAttack. On the $n=7{,}061\pm68$ samples both models classify correctly "
     r"on clean inputs, an exactly paired comparison, the CNN leads by 13.8 and "
     r"10.7 points",
     "04 kosullu sikistirma"),

    # ---- 04: denominators paragrafi, Diff. sutunu aciklamasi ----
    ("04_experiments.tex",
     r"The spread quoted in the Diff.\ column is the standard deviation of the "
     r"paired within-seed difference, which cannot be recovered from the two "
     r"per-direction spreads because the directions covary across seeds, and it is "
     r"the training-run reference used in "
     r"Section~\ref{subsec:statistics_results}. The result is that the protocol, "
     r"not the model, dominates the measured quantity.",
     r"The spread in the Diff.\ column is the standard deviation of the paired "
     r"within-seed difference, which the two per-direction spreads cannot recover "
     r"because the directions covary across seeds; it is the training-run "
     r"reference of Section~\ref{subsec:statistics_results}. The protocol, not the "
     r"model, dominates the measured quantity.",
     "04 Diff sutunu"),

    # ---- 04: L2 paragrafi ----
    ("04_experiments.tex",
     r"so it is smaller under the changed norm but stays far above the two-point "
     r"floor the pre-registration set and an order of magnitude above the "
     r"run-to-run standard deviation. The sign is positive in all twelve "
     r"measurements.",
     r"so it is smaller under the changed norm but far above both the two-point "
     r"floor the pre-registration set and the run-to-run standard deviation, and "
     r"the sign is positive in all twelve measurements.",
     "04 L2 sikistirma"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
