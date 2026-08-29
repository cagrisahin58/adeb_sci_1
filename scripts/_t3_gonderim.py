#!/usr/bin/env python3
"""Gonderim malzemelerini hakem turu 3 revizyonuyla hizalar.

Kapi (gonderim_tutarlilik.py) SAYILARI denetliyor ama ANLATIYI denetlemiyor;
manset ayristirmasi, null sayisi ve iddia provenansi elle hizalanmali.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/submission")

YAMALAR = [
    # ---------- cover letter: manset ayristirmasi ----------
    ("cover_letter.tex",
     r"Across four established conditioning protocols, the measured CNN-to-ViT "
     r"transfer asymmetry on CIFAR-10 ranges from $+4.4$ to $+19.4$ points, a "
     r"mean per-seed spread of $15.01 \pm 0.84$ points. Retraining both "
     r"architectures from scratch moves the same quantity by a standard deviation "
     r"of only $0.23$ to $1.27$ points. The protocol also decides whether an "
     r"equivalence test is accepted or rejected.",
     r"Across four conditioning protocols, the measured CNN-to-ViT transfer "
     r"asymmetry on CIFAR-10 ranges from $+4.4$ to $+19.4$ points, a mean "
     r"per-seed spread of $15.01 \pm 0.84$ points, while retraining both "
     r"architectures from scratch moves the same quantity by a standard deviation "
     r"of only $0.23$ to $1.27$ points. We do not leave that spread as one "
     r"number. It separates into $3.91$ points between the two protocols we "
     r"endorse, $5.31$ points that the identity below corrects in closed form, "
     r"and $5.79$ points contributed by a protocol that estimates a different "
     r"quantity. Only the first is irreducible discretion, and at $3.91$ points "
     r"it is still more than twice the training effect.",
     "gonderim manset ayristirmasi"),

    # ---------- cover letter: null sayisi ve provenans ----------
    ("cover_letter.tex",
     r"\item \textbf{Three claims common in this area fail to replicate.} "
     r"Scale-invariant gradient sparsity differences do not correspond to spatial "
     r"localization differences (three of four spatial measures are null);",
     r"\item \textbf{Three readings fail to replicate under direct measurement.} "
     r"Scale-invariant gradient sparsity differences do not correspond to spatial "
     r"localization differences (all four spatial measures are null);",
     "gonderim null sayisi"),

    ("cover_letter.tex",
     r"and a ViT-specific transfer attack gives no gain over plain MI-FGSM under "
     r"a matched budget.",
     r"and a ViT-specific transfer attack gives no gain over plain MI-FGSM under "
     r"a matched budget. Only the last is a published claim; we test the first "
     r"two because our own earlier figures encouraged them.",
     "gonderim iddia provenansi"),

    # ---------- ABD imlasi (makale boyunca 'favor') ----------
    ("cover_letter.tex", r"Both factors favour the CNN", r"Both factors favor the CNN",
     "gonderim imla 1"),
    ("cover_letter.tex", r"two of the four protocols report a CNN advantage",
     r"two of the four protocols report a CNN advantage", "gonderim imla 2 (yok)"),

    # ---------- highlights ----------
    ("highlights.txt",
     "   measured CNN-to-ViT transfer asymmetry ranges from +4.4 to +19.4 points\n"
     "   across four established conditioning protocols: a mean per-seed spread of\n"
     "   15.01 +/- 0.84 points.",
     "   measured CNN-to-ViT transfer asymmetry ranges from +4.4 to +19.4 points\n"
     "   across four conditioning protocols: a mean per-seed spread of\n"
     "   15.01 +/- 0.84 points. That spread separates into 3.91 points of\n"
     "   irreducible discretion between the two protocols we endorse, 5.31 points\n"
     "   that an identity corrects in closed form, and 5.79 points from a protocol\n"
     "   that estimates a different quantity.",
     "highlights ayristirma"),

    ("highlights.txt", "Both factors favour the CNN",
     "Both factors favor the CNN", "highlights imla"),
]

# "yok" isaretli yamalari at
YAMALAR = [y for y in YAMALAR if not y[3].endswith("(yok)")]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
