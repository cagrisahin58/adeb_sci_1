#!/usr/bin/env python3
"""EN PDF'in secili sayfalarini PNG'ye cevirir (taze gozle bakmak icin).
Access sablonuna gecisten sonra kimse baslik blogunu, yazar bandini ve
biyografi/EOD sayfasini GORMEDI; kapilar metni denetler, gorunumu degil."""
import sys
from pathlib import Path

import fitz

pdf = Path("/workspace/paper/manuscript/main.pdf")
out = Path("/workspace/results/q1_research/_sayfa_goruntu")
out.mkdir(parents=True, exist_ok=True)
d = fitz.open(pdf)
n = len(d)
sayfalar = [1, 2, n] if n > 2 else list(range(1, n + 1))
for s in sayfalar:
    pix = d[s - 1].get_pixmap(dpi=110)
    yol = out / f"EN_s{s:02d}.png"
    pix.save(yol)
    print(f"{yol}  ({pix.width}x{pix.height})")
print(f"toplam {n} sayfa")
