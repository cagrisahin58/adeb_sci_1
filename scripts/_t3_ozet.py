#!/usr/bin/env python3
"""Ingilizce ozeti butun olarak degistirir (<=250 kelime, dogru sira).

Parca parca yamalar sirayi bozdu ("The second of those parts" ozdeslik
cumlesi SVHN'den sonraya dustu). Ozet tek blok olarak yazilir.
"""
import re
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/main.tex")

YENI = """\\begin{abstract}
Comparisons of adversarial robustness across architecture families reach conflicting conclusions, usually attributed to models, training recipes, or datasets. We show that much of the disagreement comes from the measurement protocol itself. On adversarially trained ResNet-18 and ViT-Tiny pairs, three runs each, with full-test-set per-sample logging and a validation split held out before any training, we fix models, data, threat model and attack budget and vary only how transfer is scored. Across four conditioning protocols the measured CNN-to-ViT transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10, whereas retraining both architectures moves it by under 1.5 points. That 15.01-point spread is not one thing: 5.80 points come from a protocol estimating a different quantity, 5.30 from dropping conditioning altogether, and 3.91 remain as irreducible discretion between two defensible protocols. The middle part is exactly correctable: the deviation of unconditioned from conditioned rates equals the target's clean error scaled by one minus the conditioned rate, an identity whose premise we measure rather than assume. Replicating the design on CIFAR-100 preserves the sign in all twelve measurements. On SVHN, where the same recipe leaves the architectures 1.85 points apart in clean accuracy, the protocol decides the sign and not just the size: two report a CNN advantage and two a ViT advantage. Varying only the checkpoint-selection rule adds a fourth, almost never reported, source of variance. Three further readings fail to replicate under direct measurement, and we close with reporting requirements for cross-architecture robustness studies.
\\end{abstract}"""

t = P.read_text(encoding="utf-8")
yeni_t, n = re.subn(r"\\begin\{abstract\}.*?\\end\{abstract\}", lambda _: YENI,
                    t, count=1, flags=re.DOTALL)
if n != 1:
    sys.exit("BASARISIZ: ozet blogu bulunamadi")
P.write_text(yeni_t, encoding="utf-8")

govde = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", YENI, re.DOTALL).group(1)
print(f"ozet yazildi: {len(govde.split())} kelime")
