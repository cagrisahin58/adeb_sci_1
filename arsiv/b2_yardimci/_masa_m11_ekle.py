# -*- coding: utf-8 -*-
"""scripts/build_reference_sheet.py icine M11 blogunu '# <<< M10 SONU' isaretinden sonra, '# --- 8. Sabit dizgeler'den
once ekler (31.10.2026). Baska satira dokunmaz; isaretlerin tekil oldugunu ve M11'in daha once eklenmedigini denetler."""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
p = KOK / "scripts/build_reference_sheet.py"
s = io.open(p, encoding="utf-8").read()
blok = io.open(KOK / "arsiv/b2_yardimci/_masa_m11_blok.py.txt", encoding="utf-8").read()
a = "# <<< M10 SONU (ek bloklar B8-B10)\n\n"
b = "# --- 8. Sabit dizgeler"
if s.count(a) != 1 or s.count(b) != 1 or "M11" in s:
    raise SystemExit("isaretler tekil degil ya da M11 zaten var")
i = s.index(a) + len(a)
if not s[i:].startswith(b):
    raise SystemExit("M10 SONU ile Sabit dizgeler arasinda beklenmeyen metin")
for yasak in ("52.15 vs 52.33", "old_run3_diff", "89.48 / FGSM 70.91"):
    if yasak in blok:
        raise SystemExit(f"blok _satir ipucu iceriyor: {yasak}")
yeni = s[:i] + blok + "\n" + s[i:]
io.open(p, "w", encoding="utf-8", newline="\n").write(yeni)
print("eklendi; satir sayisi", s.count("\n"), "->", yeni.count("\n"))
