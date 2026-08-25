#!/usr/bin/env python3
"""Rapor denetleyicisinin normallestirme SIRASINI duzeltir.

Kusur: once ondalik virgulu noktaya cevirip sonra binlik ayracini
silmek "0,056" -> "0.056" -> "0056" yapiyordu; kendi kontrolum dort
sayiyi 'bulunamadi' diye raporladi, oysa rapor dogruydu. Sira ters
cevrildi ve Unicode eksi isareti ASCII'ye normallestirildi.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/_rapor_denetle.py")
t = p.read_text(encoding="utf-8")

if "SIRA ONEMLI" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = '''# TR ondalik -> nokta
metin = re.sub(r"(?<=\\d),(?=\\d)", ".", RAPOR)
metin = re.sub(r"(?<=\\d)\\.(?=\\d{3}(?!\\d))", "", metin)   # binlik'''

YENI = '''# SIRA ONEMLI: once binlik ayracini (TR'de NOKTA) sil, sonra ondalik
# virgulu noktaya cevir. Ters sira "0,056" -> "0.056" -> "0056" yapar ve
# dogru bir sayiyi "bulunamadi" diye raporlar.
metin = re.sub(r"(?<=\\d)\\.(?=\\d{3}(?!\\d))", "", RAPOR)
metin = re.sub(r"(?<=\\d),(?=\\d)", ".", metin)
metin = metin.replace("\\u2212", "-")          # Unicode eksi -> ASCII'''

if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("denetleyici duzeltildi")
