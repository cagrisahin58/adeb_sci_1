#!/usr/bin/env python3
"""Sayfa kisaltma - son gecis: 21. sayfada kalan biyografi kuyrugu icin ~60 kelime."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

YAMALAR = [
    # entropi null'i zaten iki kez soylendi; sekil isaret cumlesi fazla
    ("04_experiments.tex",
     "\nIn Figure~\\ref{fig:feature_degradation} the clean and adversarial entropy "
     "curves lie on top of each other, which is the visual form of the null "
     "result reported above.\n",
     "\n",
     "entropi sekil cumlesi"),

    ("04_experiments.tex",
     r"Complementing the quantitative measurements, "
     r"Figure~\ref{fig:attention_layers} visualizes CLS-token attention maps at "
     r"layers 1, 6, and 12 for a representative sample. The visualization is "
     r"consistent with the displacement measurement above, since later layers move "
     r"more than early ones, but we caution that single-sample attention panels of "
     r"this kind are easy to over-read: the aggregate entropy change over "
     r"1{,}000 samples is null, so the visible differences reflect redirection, "
     r"not diffusion. Attention-shift effects under patch "
     r"perturbations~\cite{gu2022vision} and attacks that explicitly target the "
     r"attention mechanism~\cite{fu2022patchfool} operate in a different regime "
     r"from the $L_\infty$-bounded perturbations studied here.",

     r"Figure~\ref{fig:attention_layers} visualizes CLS-token attention maps at "
     r"layers 1, 6, and 12 for a representative sample. It agrees with the "
     r"displacement measurement, since later layers move more, but single-sample "
     r"panels of this kind are easy to over-read: the aggregate entropy change "
     r"over 1{,}000 samples is null, so the visible differences reflect "
     r"redirection and not diffusion. Attention-shift effects under patch "
     r"perturbations~\cite{gu2022vision} and attacks that target the attention "
     r"mechanism directly~\cite{fu2022patchfool} operate in a different regime "
     r"from the $L_\infty$-bounded perturbations studied here.",
     "dikkat haritasi paragrafi"),

    ("04_experiments.tex",
     r"shows how far capacity, additional training data, and a stronger recipe "
     r"jointly push robustness beyond the architectural choice; we keep it "
     r"visually and analytically separate from the matched pair throughout.",
     r"shows how far capacity, extra training data and a stronger recipe jointly "
     r"push robustness beyond the architectural choice; we keep it separate from "
     r"the matched pair throughout.",
     "WRN cumlesi"),

    ("04_experiments.tex",
     r"Penultimate-space geometry is measured in the original feature space, not "
     r"from a low-dimensional embedding, because embeddings of this kind invite "
     r"qualitative over-reading ($n$=500 per run, each model attacked white-box, "
     r"mean$\pm$std over three runs).",
     r"Penultimate-space geometry is measured in the original feature space, not "
     r"from a low-dimensional embedding, which would invite qualitative "
     r"over-reading ($n$=500 per run, white-box, mean$\pm$std over three runs).",
     "geometri paragrafi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
