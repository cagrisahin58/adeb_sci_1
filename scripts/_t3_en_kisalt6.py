#!/usr/bin/env python3
"""Sayfa kisaltma - altinci gecis.

Dort-protokollu egim CEKILDIGI icin onu betimleyen ayrinti da kisalir;
olcumlerin hicbiri kaybolmaz (13/18 durustluk kaydi dahil korunur).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    ("04_experiments.tex",
     r"The successful-source rate is the smallest of the four in $12$ of $18$ "
     r"pairs and the largest in $4$ more, so it is the extreme in $16$ of them. "
     r"The protocol pair with the largest average gap is target-correct against "
     r"successful-source ($23.77$ points), and it is the widest pair in $13$ of "
     r"the $18$ directions; in the remaining five, all on CIFAR-100, the "
     r"unconditioned rate is the far end instead. Conditioning on source success "
     r"selects by the \emph{source's} own robustness, which is not a function of "
     r"the clean-accuracy gap between the pair, so it contributes a second and "
     r"partly opposing term.",
     r"The successful-source rate is the extreme of the four in $16$ of the $18$ "
     r"pairs, and the widest pair is target-correct against successful-source "
     r"($23.77$ points average gap, widest in $13$ of the $18$ directions). "
     r"Conditioning on source success selects by the \emph{source's} own "
     r"robustness, which is not a function of the pair's clean-accuracy gap, so it "
     r"contributes a second and partly opposing term.",
     "mekanizma ayrinti"),

    ("04_experiments.tex",
     r"We therefore treat the SVHN-inclusive fit as the pre-registered one. Adding "
     r"its two directions, whose clean-error gap of under two points falls in an "
     r"otherwise unoccupied band of the $x$ axis, moves the four-protocol slope to "
     r"$-0.133$ with a cluster-bootstrap CI of $[-0.570, +0.469]$ that includes "
     r"zero, while the three-protocol slope keeps both its sign and its interval "
     r"($+0.470$, CI $[+0.361, +0.665]$). The four-protocol slope is therefore not "
     r"supported in the pre-registered pool, and we withdraw it; the mechanism "
     r"claim rests on the three-protocol slope, which survives the pool question "
     r"and is the quantity Section~\ref{subsec:statistics_results} carries forward.",
     r"We therefore treat the SVHN-inclusive fit as the pre-registered one. Adding "
     r"its two directions moves the four-protocol slope to $-0.133$, with a "
     r"cluster-bootstrap CI of $[-0.570, +0.469]$ that includes zero, while the "
     r"three-protocol slope keeps its sign and its interval ($+0.470$, CI "
     r"$[+0.361, +0.665]$). We therefore withdraw the four-protocol slope; the "
     r"mechanism claim rests on the three-protocol one, which survives the pool "
     r"question and is what Section~\ref{subsec:statistics_results} carries forward.",
     "SVHN sikistirma"),

    ("05_discussion.tex",
     r"It is a bound on what the omission costs, not a dispersion of a single "
     r"estimator, and it is the reason the protocol belongs in the result. This is "
     r"not an argument against conditioning, since conditioning on correctly "
     r"classified samples is established practice~\cite{liu2017delving, "
     r"dong2018boosting, ravikumar2023trend} and remains necessary, but an "
     r"argument that the choice belongs in the result, not in a footnote.",
     r"It is a bound on what the omission costs, not a dispersion of a single "
     r"estimator. This is not an argument against conditioning, which remains "
     r"established practice~\cite{liu2017delving, dong2018boosting, "
     r"ravikumar2023trend} and necessary, but an argument that the choice belongs "
     r"in the result and not in a footnote.",
     "05 itiraz sikistirma"),

    ("05_discussion.tex",
     r"Two of the extensions we previously listed as future work have since been "
     r"run, and we record both what they settled and what they did not. The "
     r"leakage ablation was carried out on six full-budget trajectories, and it "
     r"did not detect an effect of leakage on checkpoint selection; it answers a "
     r"weaker question than the one originally posed, because the treatment was "
     r"applied to a single validation split, so split identity and leakage cannot "
     r"be separated within that design. Its informative by-product is the "
     r"selection-protocol dispersion reported in "
     r"Section~\ref{subsec:statistics_results}. The second dataset has also been "
     r"run (Section~\ref{subsec:cifar100}). What remains open is the "
     r"capacity-matched pair (for example ViT-Small against ResNet-50), which "
     r"would test whether the surviving behavioral differences, the sparsity "
     r"ordering and the depth profiles, are properties of the families or of these "
     r"particular small models.",
     r"Two extensions we previously listed as future work have since been run. The "
     r"leakage ablation, on six full-budget trajectories, did not detect an effect "
     r"of leakage on checkpoint selection, but it answers a weaker question than "
     r"the one posed: the treatment was applied to a single validation split, so "
     r"split identity and leakage are not separable within that design, and its "
     r"informative by-product is the selection-protocol dispersion of "
     r"Section~\ref{subsec:statistics_results}. The second dataset has also been "
     r"run (Section~\ref{subsec:cifar100}). What remains open is the "
     r"capacity-matched pair (ViT-Small against ResNet-50, say), which would test "
     r"whether the sparsity ordering and the depth profiles are properties of the "
     r"families or of these particular small models.",
     "05 gelecek is sikistirma"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
