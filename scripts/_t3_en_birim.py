#!/usr/bin/env python3
"""Hakem turu 3 - CIKARIM BIRIMI politikasi + seyreklik iddiasi (Ingilizce).

Defter bolum A5, B1, B4 ve ozet/sonuc duzeltmeleri.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # ============ A5 + B4: cikarim birimi politikasi ve TOST marji ============
    ("03_methodology.tex",
     r"Equivalence claims use two one-sided tests (TOST). The primary margin is "
     r"$\pm2$ points, fixed before the comparisons on the principle that "
     r"differences smaller than the run-to-run variation in PGD accuracy should "
     r"count as practically equivalent, and every equivalence claim is also "
     r"reported at $\pm1$ and $\pm3$ points so that the verdict can be read "
     r"against the margin.",

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
     "A5+B4 birim politikasi ve marj"),

    # ============ B1: seyreklik iddiasi iki birimde ============
    ("04_experiments.tex",
     r"Because the same 500 samples are measured under both models, the "
     r"differences are tested with per-sample paired statistics: all three are "
     r"significant in all three runs (Wilcoxon signed-rank, Holm-corrected "
     r"$p<10^{-11}$ throughout) with paired Cohen's $d$ between 0.32 and 1.23.",

     r"This is the one place where our two units of inference disagree, so we "
     r"report both. Within a run, where the same 500 samples are measured under "
     r"both models, per-sample paired tests are decisive on all three measures in "
     r"all three runs (Wilcoxon signed-rank, Holm-corrected $p<10^{-11}$ "
     r"throughout, paired Cohen's $d$ between 0.32 and 1.23); that establishes "
     r"that these checkpoints differ on these images. At the run level, which is "
     r"the unit an architectural claim needs and the unit Table~\ref{tab:spatial} "
     r"uses, three paired runs give raw $p$ of $0.036$, $0.042$ and $0.067$ for "
     r"Gini, the sub-1\% fraction and Hoyer, which Holm correction across the "
     r"three measures raises to $0.108$. The ordering is perfectly consistent, "
     r"three runs out of three on every measure, and the gap is several times the "
     r"run-to-run standard deviation; but with three runs it does not clear "
     r"$\alpha=0.05$ after correction, and the three measures are near-collinear, "
     r"which makes Holm conservative here. We therefore state the sparsity result "
     r"as reproducible rather than as significant, and we do not let the "
     r"per-sample $p$-values carry the architectural claim. The alignment "
     r"difference below does reach run-level significance ($p=0.0009$), and it is "
     r"the gradient result we carry into the discussion on that basis.",
     "B1 seyreklik iki birim"),

    # ---- 04:336 ayni birimde karsilastirma ----
    ("04_experiments.tex",
     r"points toward a \emph{smaller} area for the CNN by two percentage points "
     r"of image area and does not survive correction, which is a marginal effect "
     r"next to a Hoyer gap that is significant at $p<10^{-11}$.",
     r"points toward a \emph{smaller} area for the CNN by two percentage points "
     r"of image area and does not survive correction. Compared at the same unit, "
     r"the spatial measures are not merely weaker than the sparsity ones: the "
     r"sparsity ordering is consistent in every run and every measure while the "
     r"spatial ordering is not stable across runs on two of the four measures, "
     r"which is the difference that matters even though neither family clears "
     r"run-level correction at three runs.",
     "B1 esit birimde karsilastirma"),

    # ---- 05:25 birim adi ----
    ("05_discussion.tex",
     r"adversarially trained CNN gradients concentrate more mass on fewer "
     r"components (Hoyer $0.4928$ versus $0.4561$, paired $p<10^{-11}$), but four "
     r"spatial descriptors",
     r"adversarially trained CNN gradients concentrate more mass on fewer "
     r"components (Hoyer $0.4928$ versus $0.4561$, consistent in every run; "
     r"per-sample $p<10^{-11}$, run-level $p=0.108$ after correction), but four "
     r"spatial descriptors",
     "B1 tartisma birimi"),

    # ============ imla ============
    ("04_experiments.tex", r"Moran's $I$ with 4-neighbourhood weights",
     r"Moran's $I$ with 4-neighborhood weights", "imla neighbourhood"),

    # ============ "uc iddia literaturde yaygin" fazla iddiasi ============
    ("06_conclusion.tex",
     r"Three claims common in this literature did not survive direct measurement: "
     r"adversarially trained CNN gradients are sparser but not spatially more "
     r"localized, CLS attention entropy does not change under $L_\infty$ attack at "
     r"$n=1000$, and a transformer-specific transfer attack yields no transfer "
     r"gain in this regime.",
     r"Three readings did not survive direct measurement: adversarially trained "
     r"CNN gradients are sparser but not spatially more localized, CLS attention "
     r"entropy does not change under $L_\infty$ attack at $n=1000$, and a "
     r"transformer-specific transfer attack yields no transfer gain in this "
     r"regime. Only the third is a published claim; the first two are natural "
     r"readings that our own earlier figures encouraged, and we test them as such.",
     "sonuc iddia provenansi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
