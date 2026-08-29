#!/usr/bin/env python3
"""Sayfa kisaltma - besinci gecis: iddia tasimayan ornek sekli kaldirilir.

fig_adversarial_examples niteldir ve makalenin hicbir iddiasini tasimaz;
metindeki tek anilmasi saf bir isaret cumlesidir ("provides visual
examples"). Sekil dosyasi figures/final altinda DURUYOR; poster ve sunum
malzemesi icin kullanilabilir. Kaldirilan yalnizca makale sayfasidir.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
p4 = ROOT / "04_experiments.tex"
t = p4.read_text(encoding="utf-8")

t2, n = re.subn(
    r"\\begin\{figure\}\[!t\]\s*\\centering\s*"
    r"\\includegraphics\[[^\]]*\]\{[^}]*fig_adversarial_examples\.pdf\}\s*"
    r"\\caption\{.*?\}\s*\\label\{fig:adversarial_examples\}\s*\\end\{figure\}\s*",
    "", t, count=1, flags=re.DOTALL)
if n:
    p4.write_text(t2, encoding="utf-8")
    print("  [+] fig_adversarial_examples sekil blogu kaldirildi")
elif "fig_adversarial_examples" not in t:
    print("  [=] zaten yok")
else:
    sys.exit("BASARISIZ: sekil blogu desene uymadi")

YAMALAR = [
    ("04_experiments.tex",
     "Figure~\\ref{fig:adversarial_examples} provides visual examples of "
     "adversarial perturbations and their effects on model predictions.\n",
     "",
     "ornek sekli isaret cumlesi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
