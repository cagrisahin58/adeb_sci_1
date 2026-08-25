#!/usr/bin/env python3
"""Oz-sinama 3. kolunu SAYI-NOTR hale getirir.

Onceki tasarim ozete dolgu CUMLESI ekliyordu; kapi uzunluk yerine bir SAYI
uyusmazligi bildirdi, yani kol istedigi seyi sinamiyordu. Yeni tasarim ozet
GOVDESINI IKI KEZ yaziyor: kelime sayisi ikiye katlanir, ama gecen sayilar
kumesi DEGISMEZ, dolayisiyla yalnizca uzunluk muhafizi tetiklenebilir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/test_abstract_body_check.sh")
t = p.read_text(encoding="utf-8")

ESKI = '''python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib
import re
import sys

p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
m = re.search(r"\\\\begin\\{abstract\\}(.*?)\\\\end\\{abstract\\}", t, re.S)
dolgu = " The measurement protocol is part of the reported result." * 40
t = t[:m.end(1)] + dolgu + t[m.end(1):]
p.write_text(t, encoding="utf-8")
PY
python3 "$TMP/chk.py" | tail -3'''

YENI = '''python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib
import re
import sys

# SAYI-NOTR uzatma: ozet govdesi IKI KEZ yazilir. Kelime sayisi ikiye
# katlanir, gecen sayilar kumesi DEGISMEZ; boylece yalnizca uzunluk
# muhafizi tetiklenebilir ve kol gercekten uzunlugu sinar.
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
m = re.search(r"\\\\begin\\{abstract\\}(.*?)\\\\end\\{abstract\\}", t, re.S)
if not m:
    sys.exit("SINAMA HATASI: ozet ortami bulunamadi -- kol KOSULMADI")
govde = m.group(1)
t = t[:m.start(1)] + govde + " " + govde.strip() + t[m.end(1):]
p.write_text(t, encoding="utf-8")
print(f"  (ozet {len(govde.split())} -> {2 * len(govde.split())} kelimeye cikarildi)")
PY
python3 "$TMP/chk.py" | grep -E "ozet uzunlugu|SONUC"'''

if "SAYI-NOTR uzatma" in t:
    print("zaten yamali")
    sys.exit(0)
if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
p.write_text(t.replace(ESKI, YENI, 1), encoding="utf-8")
print("3. kol sayi-notr hale getirildi")
