#!/usr/bin/env python3
"""Her sekil/tablo metinde aniliyor mu? Anilmayan yuzen nesne IEEE kusurudur
ve sayfa kisaltmasinin en ucuz kaynagidir."""
import re
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
metin = "\n".join(p.read_text(encoding="utf-8") for p in sorted(KOK.glob("0*.tex")))
gonderme = re.findall(r"\\(?:ref|autoref|eqref)\{([^}]*)\}", metin)

for tur in ("fig", "tab"):
    print(f"=== {tur} ===")
    for et in re.findall(r"\\label\{(" + tur + r":[^}]*)\}", metin):
        n = gonderme.count(et)
        bayrak = "   <-- ANILMIYOR" if n == 0 else ""
        print(f"  {et:34s} {n} gonderme{bayrak}")
