"""Tek bir PDF'i PNG'ye cevirir (konteynerde, PyMuPDF).
docker exec -w /workspace adeb_eval python scripts/pdf2png.py girdi.pdf cikti.png [dpi=200]
"""
import sys

import fitz  # type: ignore

src, dst = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200
doc = fitz.open(src)
page = doc[0]
pix = page.get_pixmap(dpi=dpi)
pix.save(dst)
w_cm = page.rect.width / 72 * 2.54
h_cm = page.rect.height / 72 * 2.54
print(f"{dst}: {pix.width}x{pix.height}px, sayfa {w_cm:.2f}x{h_cm:.2f} cm")
