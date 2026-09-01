#!/usr/bin/env python3
"""ieeeaccess.cls ile \\textbf{$...$} calismiyor ("Extra }, or forgotten $").

Sablonun kalin-matematik kurulumu bu bicimi kurtarmiyor. Tablo basliklarinda
matematik kipine gerek de yok: \\textbf{$p$} yerine \\textbf{\\textit{p}}
gorsel olarak ayni (kalin italik p) ve sinifla uyumlu.
"""
import re
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper")
DESEN = re.compile(r"\\textbf\{\$([A-Za-z0-9\\{}^_]+)\$\}")

toplam = 0
for alt in ("manuscript", "manuscript_tr"):
    for p in sorted((KOK / alt / "sections").glob("*.tex")):
        t = p.read_text(encoding="utf-8")
        bulunan = DESEN.findall(t)
        if not bulunan:
            continue
        yeni = DESEN.sub(lambda m: r"\textbf{\textit{" + m.group(1) + "}}", t)
        p.write_text(yeni, encoding="utf-8")
        toplam += len(bulunan)
        print(f"  {alt}/{p.name}: {len(bulunan)} yer -> {sorted(set(bulunan))}")

print(f"\ntoplam {toplam} degisiklik")
