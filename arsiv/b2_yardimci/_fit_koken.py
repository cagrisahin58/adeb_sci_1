#!/usr/bin/env python3
"""Iki-kol uydurmasi CIKTISINA A kolu dizinini yazar.

H2 muhafizi "yeni A kolundan uretildi mi" diye soruyor; bu ancak dosyanin
kendisi kaynagini soylerse dogrulanabilir. Aksi halde muhafiz bir varsayima
dayanir ve varsayimlar sessizce eskir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/q1_e3_iki_kol_fit.py")
t = p.read_text(encoding="utf-8")

if "A_kolu_kaynak_dizin" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = '''sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),'''
YENI = '''sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    # KOKEN: H2 muhafizi bunu okur. Dosya kendi kaynagini soylemezse
    # "yeni A kolundan uretildi" iddiasi dogrulanamaz.
    "A_kolu_kaynak_dizin": os.environ.get("E3A_DIR", "results/q1/e3_akolu"),'''

if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("koken alani eklendi")
