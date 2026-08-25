#!/usr/bin/env python3
"""A kolu surucusune cikti dizini parametresi ekler (dosya uzerinden -- bash
genisletmesi Python'a ulasmadan degiskeni yiyor)."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_akolu_run.sh")
t = p.read_text(encoding="utf-8")

HEDEF = 'PTS="results/q1/e3_akolu"   # B2 yeniden kosumu icin ayri dizin verilebilir'
YENI = ('PTS="${E3A_OUT:-results/q1/e3_akolu}"   '
        '# B2 yeniden kosumu icin ayri dizin verilebilir')

if "E3A_OUT" in t:
    print("zaten dogru")
    sys.exit(0)
if t.count(HEDEF) != 1:
    print(f"YAMA BASARISIZ: {t.count(HEDEF)} eslesme")
    sys.exit(1)
p.write_text(t.replace(HEDEF, YENI, 1), encoding="utf-8")
print("surucu parametrelendi (dogru)")
