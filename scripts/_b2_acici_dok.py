#!/usr/bin/env python3
"""Kisa acicilarin bulundugu paragraflarin ILK 300 karakterini doker."""
import re
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
HEDEF = {
    "paper/manuscript/sections/01_introduction.tex": [27],
    "paper/manuscript/sections/04_experiments.tex": [124, 128, 211, 215, 272, 391, 452],
    "paper/manuscript/sections/05_discussion.tex": [25],
    "paper/manuscript/sections/06_conclusion.tex": [9],
    "paper/manuscript_tr/sections/01_giris.tex": [11, 23, 27],
    "paper/manuscript_tr/sections/04_deneyler.tex": [124, 128, 211, 213, 272, 391, 452, 468],
    "paper/manuscript_tr/sections/05_tartisma.tex": [13, 25],
    "paper/manuscript_tr/sections/06_sonuc.tex": [9],
}

for rel, satirlar in HEDEF.items():
    t = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    for n in satirlar:
        s = t[n - 1].strip()
        print(f"--- {rel}:{n}")
        print("   ", s[:330])
        print()
