#!/usr/bin/env python3
"""I1 muhafizi: "korelasyon yerine egim" gerekcesi L2 yeniden yaziminda
dusmustu. Karar (korelasyon degil egim raporlamak) hala gecerli ve ayri bir
yontem noktasidir; kisa haliyle geri konur. Bkz. check_manuscript_claims I1.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

EN = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
TR = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

if not uygula([
    ("04_experiments.tex",
     r"the fitted slope of $+0.914$ estimates $1 - r_{\text{cond}}$ rather than "
     r"testing anything.",
     r"the fitted slope of $+0.914$ estimates $1 - r_{\text{cond}}$ rather than "
     r"testing anything. In any case we report the slope rather than a "
     r"correlation, because the eighteen directions take only seven distinct "
     r"target-error values, six of them the same fixed WideResNet.",
     "I1 EN"),
], EN):
    sys.exit(1)

if not uygula([
    ("04_deneyler.tex",
     r"uydurulan $+0{,}914$ eğimi bir şeyi sınamak yerine $1 - r_{\text{koş}}$'u "
     r"kestirmektedir.",
     r"uydurulan $+0{,}914$ eğimi bir şeyi sınamak yerine $1 - r_{\text{koş}}$'u "
     r"kestirmektedir. Her durumda korelasyon yerine eğimi raporluyoruz, çünkü on "
     r"sekiz yön yalnızca yedi ayrık hedef hatası değeri almakta, bunların altısı "
     r"aynı sabit WideResNet'ten gelmektedir.",
     "I1 TR"),
], TR):
    sys.exit(1)
