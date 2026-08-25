#!/usr/bin/env python3
"""Ozet kapisinin SAYAC/MESAJ karisikligini duzeltir.

Bulgu (2026-08-25): iki ayri kusur tek sayaca (`kalan`) yaziliyordu ve nihai
mesaj hepsini "ozde gecip govdede bulunmayan N sayi" diye adlandiriyordu.
Uzunluk muhafizi tetiklendiginde kapi, eksik sayi SIFIR oldugu halde
"1 sayi var" diyordu. Kapi dogru KALIYOR ama YANLIS SEBEP soyluyordu; boyle
bir mesaj okuru yanlis dosyaya gonderir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/check_abstract_body.py")
t = p.read_text(encoding="utf-8")

if "kalan_uzunluk" in t:
    print("zaten yamali")
    sys.exit(0)

CIFTLER = [
    ("    kalan += len(eksik)", "    kalan_sayi += len(eksik)", "sayi sayaci"),
    ("""    if k > UZUNLUK_ESIGI:
        kalan += 1""",
     """    if k > UZUNLUK_ESIGI:
        kalan_uzunluk += 1""", "uzunluk sayaci"),
    ("""print("-" * 66)
if kalan:
    print(f"SONUC: KALDI -- ozde gecip govdede bulunmayan {kalan} sayi var.")
    print("Oz ile govde AYRI YASIYOR demektir; bu kusur bu projede iki kez cikti.")
    sys.exit(1)
print("SONUC: GECTI -- ozdeki her sayinin govdede karsiligi var.")
sys.exit(0)""",
     """print("-" * 66)
# Iki kusur AYRI adlandirilir: yanlis sebep soyleyen bir kapi, okuru yanlis
# dosyaya gonderir (2026-08-25'te tam bu oldu).
if kalan_sayi or kalan_uzunluk:
    print("SONUC: KALDI")
    if kalan_sayi:
        print(f"  - ozde gecip govdede bulunmayan {kalan_sayi} sayi var; "
              "oz ile govde AYRI YASIYOR demektir "
              "(bu kusur bu projede iki kez cikti).")
    if kalan_uzunluk:
        print(f"  - {kalan_uzunluk} dilde ozet {UZUNLUK_ESIGI} kelime sinirini "
              "asiyor.")
    sys.exit(1)
print("SONUC: GECTI -- ozdeki her sayinin govdede karsiligi var ve iki ozet de "
      "uzunluk sinirinin altinda.")
sys.exit(0)""", "nihai mesaj"),
]

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        print(f"BASARISIZ ({ad}): {t.count(eski)} eslesme")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

# sayac tanimi
import re as _re
m = _re.search(r"^kalan = 0\s*$", t, _re.M)
if not m:
    print("BASARISIZ: 'kalan = 0' tanimi bulunamadi")
    sys.exit(1)
t = t[:m.start()] + "kalan_sayi = 0\nkalan_uzunluk = 0" + t[m.end():]

p.write_text(t, encoding="utf-8")
print("ozet kapisi sayaclari ayrildi")
