#!/usr/bin/env python3
"""Paragraf uzunluk raporu: kesilecek yeri TAHMIN degil OLCUMLE sec."""
import re
import sys
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
hedef = sys.argv[1] if len(sys.argv) > 1 else "04_experiments.tex"
t = (KOK / hedef).read_text(encoding="utf-8")

# yuzen nesneleri cikar
t = re.sub(r"\\begin\{(figure|table)\*?\}.*?\\end\{\1\*?\}", "", t, flags=re.DOTALL)

satir_no = 1
paragraflar = []
for blok in t.split("\n\n"):
    n = blok.count("\n") + 1
    duz = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", blok)
    k = len(duz.split())
    if k >= 60:
        bas = " ".join(blok.split())[:105]
        paragraflar.append((k, satir_no, bas))
    satir_no += n + 1

paragraflar.sort(reverse=True)
print(f"{hedef}: {len(paragraflar)} paragraf >=60 kelime, "
      f"toplam {sum(p[0] for p in paragraflar)} kelime\n")
for k, ln, bas in paragraflar[:18]:
    print(f"{k:4d} kelime  satir {ln:4d}  {bas}")
