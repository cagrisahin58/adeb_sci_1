#!/usr/bin/env python3
"""C3 muhafizini cekime duyarsiz yapar.

"sinanamadi" ve "sinanamamistir" ikisi de gecerli Turkcedir; muhafizin amaci
NITELEMENIN AYAKTA olmasidir, belirli bir cekimin degil. Govde
("bu tasarimda sinanama") yine ayirt edicidir, baska hicbir yerde gecmez.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/check_manuscript_claims.py")
t = p.read_text(encoding="utf-8")

ESKI = 'kontrol("C3. TR \'bu tasarımda sınanamadı\'", "bu tasarımda sınanamadı" in tr)'
YENI = ('kontrol("C3. TR \'bu tasarımda sınanama...\'", '
        '"bu tasarımda sınanama" in tr)   # cekime duyarsiz govde')

if "sınanama\" in tr" in t:
    print("zaten yamali")
    sys.exit(0)
if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("C3 muhafizi guncellendi")
