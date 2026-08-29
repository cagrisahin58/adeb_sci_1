#!/usr/bin/env python3
"""TR metninden belirli satirlari doker (yama yazmak icin)."""
import sys
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
dosya = sys.argv[1]
satirlar = [int(x) for x in sys.argv[2].split(",")]
t = (KOK / dosya).read_text(encoding="utf-8").splitlines()
for n in satirlar:
    print(f"\n<<<{dosya}:{n}>>>")
    print(t[n - 1])
