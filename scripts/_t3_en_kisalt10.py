#!/usr/bin/env python3
"""Sayfa kisaltma - onuncu gecis: 3. bolum ifade sikilastirmasi (~45 kelime)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    ("03_methodology.tex",
     r"Two units of inference are available throughout this study and they answer "
     r"different questions. A per-sample test asks whether two fixed checkpoints "
     r"differ on the images evaluated; a run-level test, over the three training "
     r"repetitions, asks whether the architectures differ. Only the second "
     r"supports an architectural claim, and with three runs it is the weaker of "
     r"the two by a wide margin. Our policy is to name the unit next to every "
     r"test, to use the run level wherever the claim is architectural, and to "
     r"report both units wherever they disagree rather than the one that favors "
     r"the claim; Section~\ref{subsec:gradient} is where they disagree. "
     r"Equivalence claims use two one-sided tests (TOST). The primary margin is "
     r"$\pm2$ points, fixed before the comparisons from the run-to-run variation "
     r"in PGD accuracy. That is the right scale for an absolute accuracy and the "
     r"wrong one for the transfer asymmetry, whose own run-to-run standard "
     r"deviation is $0.23$ points, so on transfer the margin is about eight times "
     r"too generous and biases TOST toward accepting equivalence. We keep the "
     r"pre-registered margin rather than retune it after seeing the data, and "
     r"report every equivalence claim at $\pm1$ and $\pm3$ points as well so the "
     r"verdict can be read against the margin. The one equivalence we accept, on "
     r"SVHN, is accepted at $\pm1$ point as well.",

     r"Two units of inference are available throughout and they answer different "
     r"questions. A per-sample test asks whether two fixed checkpoints differ on "
     r"the images evaluated; a run-level test, over the three repetitions, asks "
     r"whether the architectures differ. Only the second supports an architectural "
     r"claim, and with three runs it is much the weaker. We name the unit next to "
     r"every test, use the run level wherever the claim is architectural, and "
     r"report both units wherever they disagree instead of the one that favors the "
     r"claim; Section~\ref{subsec:gradient} is where they disagree. Equivalence "
     r"claims use two one-sided tests (TOST) at a primary margin of $\pm2$ points, "
     r"fixed before the comparisons from the run-to-run variation in PGD accuracy. "
     r"That is the right scale for an absolute accuracy and the wrong one for the "
     r"transfer asymmetry, whose run-to-run standard deviation is $0.23$ points, "
     r"so there the margin is some eight times too generous and biases TOST toward "
     r"accepting equivalence. We keep the pre-registered margin instead of "
     r"retuning it after seeing the data, and report every equivalence claim at "
     r"$\pm1$ and $\pm3$ points as well; the one equivalence we accept, on SVHN, "
     r"holds at $\pm1$ too.",
     "03 birim politikasi sikistirma"),

    ("03_methodology.tex",
     r"The first is established in the cited sense; for the second we know of no "
     r"single canonical reference, and we include it because it is the protocol "
     r"implied whenever a transfer rate is reported over ``successful'' "
     r"adversarial examples.",
     r"The first is established in the cited sense; for the second we know of no "
     r"canonical reference, and include it because it is the protocol implied "
     r"whenever a transfer rate is reported over ``successful'' examples.",
     "03 basarili kaynak notu"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
