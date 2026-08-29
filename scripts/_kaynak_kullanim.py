#!/usr/bin/env python3
"""Kaynakcada olup metinde ANILMAYAN kunye var mi? SALT OKUR."""
import re
from pathlib import Path

R = Path("/home/firat/projects/adeb_sci_1/paper/manuscript")
bib = (R / "references.bib").read_text(encoding="utf-8")
metin = (R / "main.tex").read_text(encoding="utf-8") + "\n" + "\n".join(
    p.read_text(encoding="utf-8") for p in sorted((R / "sections").glob("*.tex")))

kunyeler = re.findall(r"@\w+\{([^,]+),", bib)
anilan = set()
for m in re.finditer(r"\\cite[a-zA-Z]*\{([^}]*)\}", metin):
    for k in m.group(1).split(","):
        anilan.add(k.strip())

kullanilmayan = [k for k in kunyeler if k.strip() not in anilan]
eksik = [k for k in anilan if k not in [x.strip() for x in kunyeler]]

print(f"kunye : {len(kunyeler)}")
print(f"anilan: {len(anilan)}")
print(f"\nKAYNAKCADA OLUP ANILMAYAN: {len(kullanilmayan)}")
for k in kullanilmayan:
    print("  -", k)
print(f"\nANILIP KAYNAKCADA OLMAYAN: {len(eksik)}")
for k in eksik:
    print("  -", k)
