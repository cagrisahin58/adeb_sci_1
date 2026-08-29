#!/usr/bin/env python3
"""Sayfa kisaltma - yedinci gecis: son ~60 kelime (yalniz ifade, olcum degil)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    ("04_experiments.tex",
     r"which supported the reading that the CNN advantage was entirely a "
     r"clean-accuracy effect (lower block of Table~\ref{tab:conditional}). None of "
     r"the three corrected runs reproduces that reading, and the three agree with "
     r"one another far more closely than any of them agrees with the earlier run. "
     r"We cannot isolate a single cause, since the corrected protocol changed the "
     r"validation handling and the training run at the same time; notably, a "
     r"simple data-quantity explanation does not hold, because the corrected clean "
     r"models are \emph{better} than the earlier ones despite seeing 2{,}000 fewer "
     r"images",
     r"supporting the reading that the CNN advantage was entirely a clean-accuracy "
     r"effect (lower block of Table~\ref{tab:conditional}). None of the three "
     r"corrected runs reproduces it, and they agree with one another far more "
     r"closely than with the earlier run. We cannot isolate a cause, since the "
     r"corrected protocol changed validation handling and the training run "
     r"together; a data-quantity explanation does not hold, because the corrected "
     r"clean models are \emph{better} despite seeing 2{,}000 fewer images",
     "ayrisma sikistirma"),

    ("04_experiments.tex",
     r"Holding a training trajectory completely fixed and varying only how its "
     r"final checkpoint is chosen, that is which validation split, what "
     r"early-stopping patience, and whether the validation curve is smoothed "
     r"before the argmax (eighteen combinations), moves the reported PGD-10 "
     r"accuracy",
     r"Holding a training trajectory fixed and varying only how its final "
     r"checkpoint is chosen (validation split, early-stopping patience, and "
     r"whether the validation curve is smoothed before the argmax; eighteen "
     r"combinations) moves the reported PGD-10 accuracy",
     "secim paragrafi 1"),

    ("04_experiments.tex",
     r"We report both figures because the larger one measures what an undocumented "
     r"preprocessing step can add, and the smaller one measures what a documented "
     r"protocol still leaves open. We report this dispersion in absolute units and "
     r"deliberately not as a ratio to seed-level dispersion, because that ratio "
     r"depends on which of the eighteen cells is taken as the reference: swept "
     r"across all eighteen it runs from $0.67$ to $3.38$ for the ResNet and $0.63$ "
     r"to $7.38$ for the ViT, falling below unity for some references and "
     r"inverting the comparison.",
     r"We report both: the larger measures what an undocumented preprocessing step "
     r"can add, the smaller what a documented protocol still leaves open. The "
     r"dispersion is quoted in absolute units and deliberately not as a ratio to "
     r"seed-level dispersion, because that ratio depends on which of the eighteen "
     r"cells is the reference: across all eighteen it runs from $0.67$ to $3.38$ "
     r"for the ResNet and $0.63$ to $7.38$ for the ViT, inverting the comparison "
     r"for some of them.",
     "secim paragrafi 2"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
