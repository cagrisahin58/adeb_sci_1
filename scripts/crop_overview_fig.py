"""mimari.png'nin beyaz kenar boslugunu kirpar -> fig_b0_overview.png

Dikey bosluk figurun sayfada kapladigi yeri buyutuyor; icerigi kaybetmeden
kirpmak sayfa maliyetini dusurur. Kucuk bir guvenlik payi birakilir.
"""
import numpy as np
from PIL import Image

SRC = "paper/bildiri/figures/mimari_v2.png"
DST = "paper/bildiri/figures/fig_b0_overview.png"
PAD = 8          # piksel guvenlik payi
THRESH = 247     # bundan acik pikseller "bos" sayilir

im = Image.open(SRC).convert("RGB")
a = np.asarray(im)
mask = (a < THRESH).any(axis=2)          # icerik pikselleri
rows = np.flatnonzero(mask.any(axis=1))
cols = np.flatnonzero(mask.any(axis=0))
top, bottom = max(0, rows[0] - PAD), min(a.shape[0], rows[-1] + 1 + PAD)
left, right = max(0, cols[0] - PAD), min(a.shape[1], cols[-1] + 1 + PAD)

out = im.crop((left, top, right, bottom))
out.save(DST)
print(f"kaynak {im.size} -> kirpilmis {out.size}")
print(f"dikey kazanc: %{100 * (1 - out.size[1] / im.size[1]):.1f}, "
      f"yatay kazanc: %{100 * (1 - out.size[0] / im.size[0]):.1f}")
print(f"cift sutunda (18cm) dpi: {out.size[0] / (18.0 / 2.54):.0f}")
