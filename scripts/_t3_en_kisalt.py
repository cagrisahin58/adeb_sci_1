#!/usr/bin/env python3
"""Sayfa kisaltma (olculen tekrarlar) + kalan AI kalintilari.

Kesilenler, _t3_tekrar_bul.py'nin yakin-tekrar olarak isaretledigi ve
BASKA BIR BOLUMDE zaten tam haliyle soylenen cumlelerdir. Yeni bilgi
kaybi yoktur; gonderme birakilir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # ---- benim ekledigim tekrar (04:336) ----
    ("04_experiments.tex",
     r"which is the difference that matters even though neither family clears "
     r"run-level correction at three runs. Per-sample tests within a single run "
     r"reach much smaller $p$-values on these measures, but they answer a "
     r"different question, whether two fixed checkpoints differ on these 500 "
     r"images, and the sign is not stable across runs on two of the four measures.",
     r"which is the difference that matters even though neither family clears "
     r"run-level correction at three runs. Per-sample tests within a single run "
     r"reach much smaller $p$-values here too, but they answer the narrower "
     r"question of whether two fixed checkpoints differ on these 500 images.",
     "tekrar 04:336"),

    # ---- 06: 05 ile ayni cumle ----
    ("06_conclusion.tex",
     r"A conditional decomposition separates absolute robustness into a "
     r"clean-accuracy factor and a conditional-susceptibility factor. Both favor "
     r"the CNN in our corrected runs, but the attribution between them differed",
     r"In the conditional decomposition of absolute robustness both factors favor "
     r"the CNN in our corrected runs, but the attribution between them differed",
     "tekrar 06 kosullu"),

    # ---- 04 TGR girisi: butce ve kontrol cumlesi 03'te zaten var ----
    ("04_experiments.tex",
     r"whereas we apply the same mechanism to our CIFAR-10 ViT-Tiny wrapper and "
     r"match the attack budget to the rest of the paper ($\eps=8/255$, "
     r"$\alpha=2/255$, 10 steps, momentum 1.0) instead of ImageNet defaults. As a "
     r"control we generate plain MI-FGSM examples in the same run, so the "
     r"comparison is paired on identical samples and identical budget.",
     r"whereas we apply the same mechanism to our CIFAR-10 ViT-Tiny wrapper at the "
     r"budget used throughout this paper (Section~\ref{subsec:attacks}), with plain "
     r"MI-FGSM generated in the same run as a paired control.",
     "tekrar 04 TGR girisi"),

    # ---- 04: token toplulastirma 03'te zaten var ----
    ("04_experiments.tex",
     r"and the token aggregation used to summarize a transformer block. For the "
     r"ViT we report the CLS token alone, the mean over the 196 patch tokens, and "
     r"the flattened concatenation of all tokens; for the CNN each residual block "
     r"output is flattened over its spatial dimensions.",
     r"and the token aggregation used to summarize a transformer block "
     r"(Section~\ref{subsec:feature_metrics}).",
     "tekrar 04 token"),

    # ---- 05: CIFAR-100 sayilari girişte zaten var ----
    ("05_discussion.tex",
     r"On CIFAR-100 the spread is close to the CIFAR-10 value ($13.83\pm1.30$ "
     r"against $15.01\pm0.84$ points) and the sign is preserved in all twelve "
     r"measurements (Section~\ref{subsec:cifar100}).",
     r"On CIFAR-100 the spread stays close to the CIFAR-10 value and the sign is "
     r"preserved throughout (Section~\ref{subsec:cifar100}).",
     "tekrar 05 c100"),

    # ---- 02: uc iddia, girişle ortusen kisim ----
    ("02_related_work.tex",
     r"We measure each directly, and none holds in our setting, and we report "
     r"these results because an untested assumption of this kind is exactly what "
     r"a protocol-sensitive comparison cannot afford.",
     r"We measure each directly and none holds in our setting; an untested "
     r"assumption of this kind is exactly what a protocol-sensitive comparison "
     r"cannot afford.",
     "tekrar 02 uc iddia"),

    # ================= kalan AI kalintilari =================
    ("04_experiments.tex",
     r"Two results follow, the first being that the two architectures differ less "
     r"in \emph{whether} damage accumulates than in \emph{where}.",
     r"Two results follow. The architectures differ less in \emph{whether} damage "
     r"accumulates than in \emph{where}.",
     "AI: the first being"),

    ("02_related_work.tex",
     r"Despite these advances, comprehensive behavioral comparisons between CNN "
     r"and ViT robustness under unified evaluation frameworks remain limited.",
     r"Despite these advances, behavioral comparisons between CNN and ViT "
     r"robustness under a single evaluation protocol remain limited.",
     "AI: comprehensive"),

    ("02_related_work.tex",
     r"with CNNs preferring high-frequency information while ViTs favor "
     r"low-frequency patterns, significantly impact transfer success",
     r"with CNNs preferring high-frequency information while ViTs favor "
     r"low-frequency patterns, shape transfer success",
     "AI: significantly impact"),

    ("02_related_work.tex",
     r"Understanding these transfer patterns is crucial for developing robust "
     r"ensemble systems and evaluating real-world attack scenarios.",
     r"These transfer patterns bear directly on ensemble design and on "
     r"black-box threat assessment.",
     "AI: crucial"),

    ("03_methodology.tex",
     r"follows established practice~\cite{liu2017delving, dong2018boosting, "
     r"mahmood2021robustness, ravikumar2023trend, zhao2025revisiting} and is "
     r"essential in cross-architecture comparisons:",
     r"follows established practice~\cite{liu2017delving, dong2018boosting, "
     r"mahmood2021robustness, ravikumar2023trend, zhao2025revisiting} and matters "
     r"most in cross-architecture comparisons:",
     "AI: essential"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
