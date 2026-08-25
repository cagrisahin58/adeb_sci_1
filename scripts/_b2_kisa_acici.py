#!/usr/bin/env python3
"""Paragraf basi KISA ACICI cumleleri bulur.

Kullanicinin sikayeti (2026-08-18): "Kisa basliklar atmissin ornegin
'The protocol spread grows rather than shrinks.' tarzi ifadeler. bu paragraf
basi kisa ifadeleri kaldir. AI yapimi ifadeler bunlar."

Olcut: paragrafin ILK cumlesi kisa (<= ESIK karakter) ve bir mini-baslik gibi
duruyor. Tablo/sekil/komut satirlari elenir.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
ESIK = int(sys.argv[1]) if len(sys.argv) > 1 else 75

DOSYALAR = (sorted((ROOT / "paper/manuscript/sections").glob("*.tex"))
            + sorted((ROOT / "paper/manuscript_tr/sections").glob("*.tex")))

toplam = 0
for f in DOSYALAR:
    satirlar = f.read_text(encoding="utf-8").splitlines()
    for i, s in enumerate(satirlar, 1):
        s = s.strip()
        if not s or s.startswith("%") or s.startswith("\\"):
            continue
        if len(s) < 120:            # cok kisa satir = tablo hucresi vb.
            continue
        # ilk cumle
        m = re.match(r"^(.{10,}?[.!?])\s+[A-ZÇĞİÖŞÜ]", s)
        if not m:
            continue
        ilk = m.group(1)
        if len(ilk) > ESIK:
            continue
        if "~\\cite" in ilk or "\\ref" in ilk or "$" in ilk:
            continue
        toplam += 1
        print(f"  {f.relative_to(ROOT)}:{i}\n      >>> {ilk}")

print(f"\nKISA ACICI (<= {ESIK} karakter): {toplam}")
