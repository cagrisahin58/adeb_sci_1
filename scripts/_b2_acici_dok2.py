#!/usr/bin/env python3
"""Kalan acicilarin paragraf baslarini doker (es dilin karsiliklari)."""
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
HEDEF = {
    "paper/manuscript/sections/01_introduction.tex": [9, 11, 23],
    "paper/manuscript/sections/04_experiments.tex": [213, 468],
    "paper/manuscript/sections/05_discussion.tex": [13],
    "paper/manuscript_tr/sections/01_giris.tex": [9],
    "paper/manuscript_tr/sections/04_deneyler.tex": [215],
    "paper/manuscript_tr/sections/06_sonuc.tex": [9],
}
for rel, satirlar in HEDEF.items():
    t = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    for n in satirlar:
        print(f"--- {rel}:{n}")
        print("   ", t[n - 1].strip()[:300])
        print()
