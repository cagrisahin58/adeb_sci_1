#!/usr/bin/env python3
"""Son sayfalarda ne var ve son sayfa ne kadar dolu?

Sayfa kisaltmasinin ne kadar metin gerektirdigini TAHMIN degil OLCUM ile
belirlemek icin: son sayfadaki metin yuksekligi / kullanilabilir yukseklik.
"""
import sys

import fitz

yol = sys.argv[1] if len(sys.argv) > 1 else "/workspace/paper/manuscript/main.pdf"
d = fitz.open(yol)
print(f"{yol}: {len(d)} sayfa\n")

for i in range(max(0, len(d) - 3), len(d)):
    s = d[i]
    metin = s.get_text().strip()
    kelime = len(metin.split())
    bloklar = [b for b in s.get_text("blocks") if b[4].strip()]
    alt = max((b[3] for b in bloklar), default=0.0)
    ust = min((b[1] for b in bloklar), default=0.0)
    h = s.rect.height
    print(f"--- sayfa {i+1}: {kelime} kelime, {len(bloklar)} blok, "
          f"metin {ust:.0f}-{alt:.0f} / sayfa {h:.0f}  "
          f"(doluluk ~%{100*(alt-ust)/h:.0f})")
    print("   ", " ".join(metin.split())[:220])
    print()

# son sayfayi eritmek icin gereken metin: son sayfadaki satir sayisi
son = d[-1]
bloklar = [b for b in son.get_text("blocks") if b[4].strip()]
if bloklar:
    kelime = len(son.get_text().split())
    print(f"SON SAYFAYI ERITMEK ICIN kabaca {kelime} kelime cikmali "
          f"(son sayfadaki metnin tamami).")
