"""Verilen dosya:satir ciftlerinin tam icerigini yazar (salt okur).
Kullanim: python3 arsiv/b2_yardimci/_satir_yaz.py paper/manuscript_tr/sections/01_giris.tex:9 ...
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

for spec in sys.argv[1:]:
    f, n = spec.rsplit(":", 1)
    lines = io.open(ROOT / f, encoding="utf-8").read().splitlines()
    print(f"##### {f}:{n}")
    print(lines[int(n) - 1])
    print()
