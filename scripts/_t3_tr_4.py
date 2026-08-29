#!/usr/bin/env python3
"""TR aynasi - 4: kaldirilan sekillere sarkan gondermeler + oran/TGR paragraflari."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
D = "04_deneyler.tex"

YAMALAR = [
    (D,
     r"Şekil~\ref{fig:robustness_comparison} bu gürbüzlük farkını mimariler "
     r"boyunca görselleştirir. Pertürbasyon büyüklüğünün etkisini anlamak için "
     r"Şekil~\ref{fig:epsilon_sweep}, $\eps \in \{2/255, 4/255, 8/255, 16/255\}$ "
     r"bütçelerinde tam test kümesindeki PGD-10 gürbüz doğruluğunu gösterir.",
     r"Şekil~\ref{fig:epsilon_sweep}, $\eps \in \{2/255, 4/255, 8/255, 16/255\}$ "
     r"bütçelerinde tam test kümesindeki PGD-10 gürbüz doğruluğunu gösterir.",
     "TR fig1 isaret cumlesi"),

    (D,
     "\nŞekil~\\ref{fig:adversarial_examples}, çekişmeli pertürbasyonların ve "
     "model tahminleri üzerindeki etkilerinin görsel örneklerini vermektedir.\n",
     "\n",
     "TR ornek sekli isaret cumlesi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
