#!/usr/bin/env python3
"""Sayfa kisaltma - son 30 kelime. Yalniz ifade sikilastirmasi."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    ("04_experiments.tex",
     r"McNemar's paired test applies within each run; it favors the CNN "
     r"decisively in all three pairs",
     r"McNemar's paired test applies within each run and favors the CNN "
     r"decisively in all three pairs",
     "McNemar cumlesi"),

    ("04_experiments.tex",
     r"Seed-level variation is small throughout for the adversarially trained "
     r"pair, at most 0.55 points on any reported accuracy, so the ordering is not "
     r"a product of run-to-run noise;",
     r"Seed-level variation for the adversarially trained pair is at most 0.55 "
     r"points on any reported accuracy, so the ordering is not run-to-run noise;",
     "tohum oynakligi"),

    ("04_experiments.tex",
     r"AutoAttack robustness is consistently below PGD-10 robustness for both "
     r"architectures (6.2 points for ResNet-18, 3.6 for ViT-Tiny), confirming the "
     r"value of the stronger ensemble.",
     r"AutoAttack falls below PGD-10 for both architectures (6.2 points for "
     r"ResNet-18, 3.6 for ViT-Tiny), confirming the value of the stronger "
     r"ensemble.",
     "AutoAttack cumlesi"),

    ("04_experiments.tex",
     r"Only the first is irreducible discretion between two defensible readings of "
     r"the same question, and at $3.91$ points it is still more than twice what "
     r"retraining both architectures moves. The corresponding endorsed-protocol "
     r"gap is $5.96$ points on CIFAR-100 and $0.65$ on SVHN.",
     r"Only the first is irreducible discretion between two defensible readings, "
     r"and at $3.91$ points it is still more than twice what retraining moves. The "
     r"same gap is $5.96$ points on CIFAR-100 and $0.65$ on SVHN.",
     "ayristirma kapanisi"),

    ("05_discussion.tex",
     r"On SVHN, where adversarial training under the same recipe leaves the two "
     r"architectures $1.85$ points apart in clean accuracy, not $12.3$ or $20.7$, "
     r"that is no longer true: two protocols report a CNN advantage and two report "
     r"a ViT advantage,",
     r"On SVHN, where the same recipe leaves the two architectures $1.85$ points "
     r"apart in clean accuracy, not $12.3$ or $20.7$, that is no longer true: two "
     r"protocols report a CNN advantage and two a ViT advantage,",
     "05 SVHN cumlesi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
