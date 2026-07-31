"""Bildiri PDF sayfalarini PNG'ye cevirir (Read araci pdflatex PDF'lerini acamiyor)."""
import sys

import fitz

pdf = "/workspace/paper/bildiri/bildiri.pdf"
out = "/tmp/bildiri_page"
doc = fitz.open(pdf)
pages = [int(x) for x in sys.argv[1:]] or list(range(1, doc.page_count + 1))
for p in pages:
    page = doc[p - 1]
    pix = page.get_pixmap(dpi=140)
    path = f"{out}{p}.png"
    pix.save(path)
    print(path)
