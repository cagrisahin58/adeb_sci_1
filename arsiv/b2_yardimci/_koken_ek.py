#!/usr/bin/env python3
"""Koken defterine B2 ile ortaya cikan iki artefakti ekler.

  results/q1/e3_asimetri_fit_svhnli.json  -- makalede RAPORLANAN SVHN duyarliligi
                                             (egim -0,133, GA sifiri iceriyor)
  results/rev2_blockA/a2_transfer_protocols.json -- Tablo III'un kacak-etkili
                                             karsilastirma sutununun kaynagi

Ikisi de metne dogrudan sayi tasiyor; defterde olmamalari, defterin amacina
(disari cikan her sayinin kokeni belli olsun) aykiridir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_koken.py")
t = p.read_text(encoding="utf-8")

if "e3_asimetri_fit_svhnli" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = '    "results/q1/e3_asimetri_fit.json",'
YENI = ('    "results/q1/e3_asimetri_fit.json",\n'
        '    # B2 (2026-08-25): makalede RAPORLANAN duyarliliklarin kaynaklari\n'
        '    "results/q1/e3_asimetri_fit_svhnli.json",\n'
        '    "results/rev2_blockA/a2_transfer_protocols.json",')

if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("koken defterine iki artefakt eklendi")
