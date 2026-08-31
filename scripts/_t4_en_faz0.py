#!/usr/bin/env python3
"""TUR 4 FAZ 0 (Ingilizce) - dogrulanmis kritik duzeltmeler.

0.1 Denklem (1)'in genel bicimi CEBIRSEL YANLIS: e(1-p) -> e*p
    (bagimsiz olcum: scripts/_t4_ozdeslik_dogrula.py; dogru bicim 6/6 yonde
     0,0000 puan, basili bicim 26,99 puana kadar hata)
0.2 Manset ayrisimi yanlis acikligi ozdeslige atfediyordu. Denklem (1)
    HEDEF-DOGRU orani baglar; kapattigi aciklik ham<->hedef-dogru = 9,21.
    Yeni cerceve (kullanici onayli): koşulsuz oran EKSEN NOKTASI.
0.3 Iki farkli protokol "birincil" ilan edilmisti.
0.4 fig:feature_degradation oksuz kalmisti (tur 3 sayfa kisaltmasi regresyonu).
1.4 p=0,88 karantina disindaydi; nitelenir.
1.5 IEEE zorunlulugu: YZ kullanim beyani.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript")
S = KOK / "sections"

YAMALAR = [
    # ================= 0.1 + 1.4: ozdesligin genel bicimi =================
    ("04_experiments.tex",
     r"Writing $p$ for the probability that a clean-misclassified sample stays "
     r"misclassified under attack, the general form is $r_{\text{raw}} = "
     r"e\,(1-p) + r_{\text{cond}}\,(1 - e)$, which reduces to "
     r"Equation~\eqref{eq:raw_identity} when $p=1$.",

     r"Writing $p$ for the probability that a clean-misclassified sample stays "
     r"misclassified under attack, the general form is $r_{\text{raw}} = "
     r"e\,p + r_{\text{cond}}\,(1 - e)$, which reduces to "
     r"Equation~\eqref{eq:raw_identity} when $p=1$. Where $p<1$, "
     r"Equation~\eqref{eq:raw_identity} overstates the deviation by exactly "
     r"$e\,(1-p)$, so it is an upper bound and not an equality once the "
     r"antecedent fails.",
     "0.1 genel bicim e*p"),

    ("04_experiments.tex",
     r"On standard-trained targets, which is the regime most transfer studies "
     r"attack, we observe $p$ as low as $0.88$ in our own earlier runs, and "
     r"there the identity becomes a bound rather than an equality.",
     r"On standard-trained targets, which is the regime most transfer studies "
     r"attack, we observed $p$ as low as $0.88$ in our own pre-correction runs; "
     r"we quote that as an order-of-magnitude indication and not as a measured "
     r"value of the present pipeline, and there the identity is a bound.",
     "1.4 p=0,88 nitelemesi"),

    # ================= 0.2: manset ayrisimi =================
    ("04_experiments.tex",
     r"That spread is not a single quantity, and separating it is part of the "
     r"result. Ordering the four estimates gives three adjacent gaps: $3.91$ "
     r"points between target-correct and both-correct, the two protocols we "
     r"endorse for directional claims and which differ only in whether the "
     r"source must also be correct; $5.31$ points between both-correct and the "
     r"unconditioned rate, a gap that Equation~\eqref{eq:raw_identity} below "
     r"predicts in closed form and that a reader can therefore undo given the "
     r"target's clean error; and $5.79$ points between the unconditioned and "
     r"the successful-source rate, which conditions on the source's own "
     r"white-box failure and so estimates a different quantity. Only the first "
     r"is irreducible discretion between two defensible readings, and at $3.91$ "
     r"points it is still more than twice what retraining moves. The same gap "
     r"is $5.96$ points on CIFAR-100 and $0.65$ on SVHN.",

     r"That spread is not a single quantity, and separating it is part of the "
     r"result. Take the unconditioned rate as the pivot: the successful-source "
     r"rate sits $5.79$ points above it and conditions on the source's own "
     r"white-box failure, so it estimates a different quantity, while the "
     r"target-correct rate sits $9.21$ points below it and that entire gap is "
     r"what Equation~\eqref{eq:raw_identity} predicts in closed form, so a "
     r"reader given the target's clean error can remove it exactly. The two "
     r"account for the full $15.01$ points. What survives the correction is the "
     r"difference between the two protocols we endorse for directional claims, "
     r"target-correct and both-correct, which differ only in whether the source "
     r"must also be correct: $3.91$ points, still more than twice what "
     r"retraining both architectures moves. That residual is $5.97$ points on "
     r"CIFAR-100 and $0.65$ on SVHN. The pivot structure is dataset-dependent: "
     r"on CIFAR-100 the unconditioned rate is the largest of the four, so the "
     r"whole $13.58$-point spread there is the identity term and the "
     r"successful-source rate falls inside it.",
     "0.2 manset ayrisimi"),

    # ================= 0.3: tek birincil =================
    ("03_methodology.tex",
     r"Our primary transfer metric is the \emph{conditioned fooling rate}: "
     r"among the samples that the target model classifies correctly on clean "
     r"inputs, the fraction that becomes misclassified under adversarial "
     r"examples crafted on the source model.",
     r"Our transfer metrics are a family of \emph{conditioned fooling rates} "
     r"that differ only in the conditioning set. The base member is the "
     r"\emph{target-correct} rate: among the samples that the target model "
     r"classifies correctly on clean inputs, the fraction that becomes "
     r"misclassified under adversarial examples crafted on the source model.",
     "0.3 metrik ailesi"),

    ("03_methodology.tex",
     r"The first is established in the cited sense; for the second we know of "
     r"no canonical reference, and include it because it is the protocol "
     r"implied whenever a transfer rate is reported over ``successful'' "
     r"examples.",
     r"The first is established in the cited sense; for the second we know of "
     r"no canonical reference, and include it because it is the protocol "
     r"implied whenever a transfer rate is reported over ``successful'' "
     r"examples. For directional claims we take the both-correct rate as the "
     r"primary estimate, because it scores both directions on identical samples "
     r"and therefore supports paired inference; the other three are reported "
     r"beside it throughout.",
     "0.3 birincil tahmin beyani"),

    # ================= 0.4: oksuz sekil =================
    ("04_experiments.tex",
     r"The attack therefore redirects attention slightly without broadening or "
     r"sharpening it.",
     r"The attack therefore redirects attention slightly without broadening or "
     r"sharpening it; Figure~\ref{fig:feature_degradation} plots the per-layer "
     r"curves, which lie on top of each other.",
     "0.4 oksuz sekil"),
]

if not uygula(YAMALAR, S):
    sys.exit(1)

# ---------------------------------------------------------------- main.tex
MAIN = [
    # ozet
    ("main.tex",
     "That 15.01-point spread is not one thing: 5.79 points come from a "
     "protocol estimating a different quantity, 5.31 from dropping "
     "conditioning altogether, and 3.91 remain as irreducible discretion "
     "between two defensible protocols. The middle part is exactly correctable: "
     "the deviation of unconditioned from conditioned rates equals the target's "
     "clean error scaled by one minus the conditioned rate, an identity whose "
     "premise we measure rather than assume.",

     "That 15.01-point spread is not one thing: 9.21 points separate the "
     "unconditioned rate from the target-correct rate and an identity we derive "
     "removes them in closed form, while 5.79 points come from a protocol that "
     "estimates a different quantity. What survives the correction is 3.91 "
     "points of discretion between the two protocols we endorse. The identity "
     "states that the deviation of unconditioned from conditioned rates equals "
     "the target's clean error scaled by one minus the conditioned rate, and we "
     "measure its premise rather than assume it.",
     "0.2 ozet"),

    # YZ beyani (1.5)
    ("main.tex",
     r"\section*{Acknowledgment}" "\n"
     r"The authors acknowledge the computational resources provided by the "
     r"Department of Software Engineering, F{\i}rat University.",
     r"\section*{Acknowledgment}" "\n"
     r"The authors acknowledge the computational resources provided by the "
     r"Department of Software Engineering, F{\i}rat University." "\n\n"
     r"The authors used Claude (Anthropic) during the preparation of this work. "
     r"The tool assisted with drafting and revising the manuscript text in all "
     r"sections, and with implementing the analysis and verification scripts "
     r"released with the paper. The study design, the experimental protocol, "
     r"and all conclusions are the authors', who verified every reported number "
     r"against the released artifacts.",
     "1.5 YZ beyani"),
]

if not uygula(MAIN, KOK):
    sys.exit(1)

# ---------------------------------------------------------- giris ve sonuc
SON = [
    ("01_introduction.tex",
     r"We then separate that spread rather than leave it as one number: $5.79$ "
     r"points of it come from a protocol that estimates a different quantity, "
     r"$5.31$ from dropping conditioning altogether, which an identity we "
     r"derive corrects in closed form, and $3.91$ remain as discretion between "
     r"two protocols that are both defensible, which is still more than twice "
     r"the retraining effect.",
     r"We then separate that spread instead of leaving it as one number: $9.21$ "
     r"points of it separate the unconditioned rate from the target-correct "
     r"rate and an identity we derive removes them in closed form, while $5.79$ "
     r"points come from a protocol that estimates a different quantity. What "
     r"survives the correction is $3.91$ points of discretion between two "
     r"protocols that are both defensible, still more than twice the retraining "
     r"effect.",
     "0.2 giris"),

    ("06_conclusion.tex",
     r"That $15.01$-point spread decomposes into $5.79$ points of a different "
     r"estimand, $5.31$ points that an identity corrects in closed form, and "
     r"$3.91$ points of genuine discretion between two defensible protocols; "
     r"the last of these is the part a reporting standard has to address.",
     r"That $15.01$-point spread decomposes into $9.21$ points that an identity "
     r"we derive removes in closed form and $5.79$ points contributed by a "
     r"protocol that estimates a different quantity; what survives the "
     r"correction is $3.91$ points of genuine discretion between two defensible "
     r"protocols, and that is the part a reporting standard has to address.",
     "0.2 sonuc"),
]

if not uygula(SON, S):
    sys.exit(1)
