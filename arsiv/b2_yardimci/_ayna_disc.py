#!/usr/bin/env python3
"""EN/TR AYNA KUSURU: Ingilizce Tartisma'da MAHMOOD KARSITLIGI YOK.

Turkce Tartisma (05_tartisma.tex:17) Mahmood ve ark.'nin TERS yonlu bulgusuyla
yuzlesen tam bir paragraf tasiyor; Ingilizce surumde bu paragraf HIC YOK ve
mahmood2021robustness Tartisma boyunca bir kez bile anilmiyor. Gonderilecek
surum Ingilizce oldugu icin bu, gonderilen metnin eksigidir: bir hakemin ilk
soracagi sey, karsit yayimlanmis bir bulgunun nasil ele alindigidir.

EN/TR ayna kontrolu (scripts/_b2_ayna_kontrol.py) buldu: EN 18 paragraf,
TR 19.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections/05_discussion.tex")
t = p.read_text(encoding="utf-8")

if "report the opposite direction" in t:
    print("zaten var")
    sys.exit(0)

ANKOR = ("This is not an argument against conditioning, since conditioning on "
         "correctly classified samples is established practice~\\cite{liu2017delving, "
         "dong2018boosting, ravikumar2023trend} and remains necessary, but an "
         "argument that the choice belongs in the result, not in a footnote.")

EK = ANKOR + """

Nor is it an argument that our direction is the correct one. Under a both-correct protocol comparable to ours, Mahmood et al.~\\cite{mahmood2021robustness} report the opposite direction on a different architecture pair, finding transfer into the transformer weaker than transfer out of it. Our mechanism is compatible with that result: we attribute the asymmetry to the target's own vulnerability rather than to any special strength of CNN-crafted perturbations, and the weaker target in their pair is not the weaker target in ours. Testing this properly would require their per-direction clean accuracies under a shared protocol, which is exactly the reporting we ask for and the sharpest external test the mechanism admits."""

if t.count(ANKOR) != 1:
    print(f"BASARISIZ: ankor {t.count(ANKOR)} kez")
    sys.exit(1)
p.write_text(t.replace(ANKOR, EK, 1), encoding="utf-8")
print("EN Tartisma'ya Mahmood karsitligi paragrafi eklendi")
