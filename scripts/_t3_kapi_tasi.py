#!/usr/bin/env python3
"""T3 blogunu CHECKS dongusunun ONUNE tasir (yanlis yere dusmustu)."""
import re
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/scripts/verify_manuscript_numbers.py")
t = P.read_text(encoding="utf-8")

BAS = "# --- T3: hakem turu 3'te metne giren sayilar ---"
i = t.find(BAS)
if i < 0:
    sys.exit("BASARISIZ: T3 blogu yok")

# blogun sonu: bir sonraki "except ImportError:\n    pass\n" bitisi
son_imza = "except ImportError:\n    pass\n"
j = t.find(son_imza, i)
if j < 0:
    sys.exit("BASARISIZ: T3 blogunun sonu bulunamadi")
j += len(son_imza)
blok = t[i:j]
t = t[:i] + t[j:]

# hedef: "rows = []" satirinin hemen onu
m = re.search(r"^rows = \[\]$", t, re.M)
if not m:
    sys.exit("BASARISIZ: 'rows = []' bulunamadi")
t = t[:m.start()] + blok + "\n\n" + t[m.start():]
P.write_text(t, encoding="utf-8")
print("T3 blogu CHECKS dongusunun onune tasindi")
