#!/usr/bin/env python3
"""Tum "rather than" gecislerini kisa baglamla doker (numarali)."""
import re
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
n = 0
for p in sorted(KOK.glob("0*.tex")):
    t = p.read_text(encoding="utf-8")
    for m in re.finditer(r"rather than", t):
        n += 1
        a, b = max(0, m.start() - 95), min(len(t), m.end() + 75)
        parca = re.sub(r"\s+", " ", t[a:b])
        print(f"{n:3d} [{p.name[:2]}] ...{parca}...")
print(f"\ntoplam {n}")
