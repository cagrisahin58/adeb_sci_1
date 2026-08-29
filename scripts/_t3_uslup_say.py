#!/usr/bin/env python3
"""Insanlastirma hedefleri: asiri kullanilan kaliplar ve tekrar bloklari."""
import re
from collections import Counter
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
DOSYALAR = sorted(KOK.glob("0*.tex"))

KALIPLAR = ["rather than", "belong with", "belongs with", "crucial",
            "comprehensive", "essential", "significantly impact",
            "it is worth noting", "it should be noted", "furthermore",
            "moreover", "in order to", "delve", "leverage", "robustly",
            "notably", "importantly", "the first being", "that is to say",
            "we would like to", "a wide range of", "plays a role"]

metin = {p.name: p.read_text(encoding="utf-8") for p in DOSYALAR}
tum = "\n".join(metin.values())
alt = tum.lower()
kelime = len(re.findall(r"[A-Za-z][A-Za-z'-]+", tum))

print(f"toplam kelime ~{kelime}\n")
print("=== ASIRI KULLANILAN KALIPLAR ===")
for k in KALIPLAR:
    n = alt.count(k)
    if n:
        aralik = kelime // n
        bayrak = "  <-- SIK" if aralik < 500 else ""
        print(f"  {k:22s} {n:3d} kez  (her ~{aralik} kelimede bir){bayrak}")
        if n >= 4:
            for ad, t in metin.items():
                c = t.lower().count(k)
                if c:
                    print(f"        {ad}: {c}")

print("\n=== TEKRAR EDEN 8-GRAMLAR (>=2 kez, icerikli) ===")
kelimeler = re.findall(r"[a-z][a-z'-]+", alt)
g = Counter(" ".join(kelimeler[i:i + 8]) for i in range(len(kelimeler) - 8))
DOLGU = {"the", "of", "a", "and", "is", "to", "in", "that", "it", "we"}
n = 0
for gram, c in g.most_common(60):
    if c < 2:
        break
    if sum(1 for w in gram.split() if w in DOLGU) > 4:
        continue
    print(f"  {c}x  {gram}")
    n += 1
    if n >= 20:
        break
