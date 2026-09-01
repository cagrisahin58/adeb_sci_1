#!/usr/bin/env python3
"""Makalede KULLANILMAYAN sekilleri paper/figures/arsiv/ altina tasir.

Tur 3'te uc sekil kaldirildi ama dosyalari figures/final'da kaldi; teslim
paketi 'final' klasorunu oldugu gibi kopyaladigi icin pakette makalede
BULUNMAYAN sekiller gidiyordu (geri cekilen egimin kalibrasyon sekli dahil).
Dosyalar SILINMEZ, arsive tasinir.
"""
import re
import shutil
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper")
FINAL = KOK / "figures/final"
ARSIV = KOK / "figures/arsiv"

kullanilan = set()
for alt in ("manuscript", "manuscript_tr", "bildiri"):
    d = KOK / alt
    if not d.is_dir():
        continue
    for p in list(d.rglob("*.tex")):
        for m in re.finditer(r"includegraphics\[[^\]]*\]\{([^}]*)\}",
                             p.read_text(encoding="utf-8")):
            kullanilan.add(Path(m.group(1)).name)

print(f"metinlerde cagrilan sekil: {len(kullanilan)}")
for k in sorted(kullanilan):
    print(f"  = {k}")

varolan = sorted(p for p in FINAL.glob("*") if p.is_file())
kullanilmayan = [p for p in varolan if p.name not in kullanilan]
print(f"\nfigures/final icinde {len(varolan)} dosya, "
      f"{len(kullanilmayan)} tanesi kullanilmiyor")

if kullanilmayan:
    ARSIV.mkdir(parents=True, exist_ok=True)
    for p in kullanilmayan:
        shutil.move(str(p), str(ARSIV / p.name))
        print(f"  -> arsiv/{p.name}")
    (ARSIV / "README.md").write_text(
        "# Arsiv: makalede kullanilmayan sekiller\n\n"
        "Bu klasordeki dosyalar hicbir surumde (EN makale, TR makale,\n"
        "bildiri) `\\includegraphics` ile cagrilmiyor. Tarihsel kayit\n"
        "olarak saklanmaktadir; teslim paketine GIRMEZ.\n\n"
        "Tasima: tur 4, 2026-09-01.\n", encoding="utf-8")
else:
    print("  (tasinacak dosya yok)")
