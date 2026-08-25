#!/usr/bin/env python3
"""B2 oncesi degerler metinde kalmis mi? (kapinin izlemedigi yerler dahil)"""
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
DOSYALAR = (sorted((ROOT / "paper/manuscript").rglob("*.tex"))
            + sorted((ROOT / "paper/manuscript_tr").rglob("*.tex"))
            + [ROOT / "paper/bildiri/bildiri.tex"])

# (desen, ne oldugu)
BAYAT = [
    ("14.60", "CIFAR-10 basarili-kaynak (eski)"),
    ("14{,}60", "CIFAR-10 basarili-kaynak (eski, TR)"),
    ("14.6 ", "CIFAR-10 ust sinir (eski)"),
    ("3.3-fold", "kat iddiasi (eski)"),
    ("factor of 3.3", "kat iddiasi (eski)"),
    ("3,3 kat", "kat iddiasi (eski, TR)"),
    ("10.45", "CIFAR-10 yayilim (eski)"),
    ("10{,}45", "CIFAR-10 yayilim (eski, TR)"),
    ("10.24", "protokol ort. acikligi (eski)"),
    ("10{,}24", "protokol ort. acikligi (eski, TR)"),
    ("11.44", "CIFAR-100 basarili-kaynak (eski)"),
    ("11{,}44", "CIFAR-100 basarili-kaynak (eski, TR)"),
    ("9.51", "L2 basarili-kaynak (eski)"),
    ("9{,}51", "L2 basarili-kaynak (eski, TR)"),
    ("2.64", "SVHN basarili-kaynak (eski)"),
    ("2{,}64", "SVHN basarili-kaynak (eski, TR)"),
    ("13.58", "CIFAR-100 yayilim (eski)"),
    ("13{,}58", "CIFAR-100 yayilim (eski, TR)"),
    ("3.65", "SVHN yayilim (eski)"),
    ("3{,}65", "SVHN yayilim (eski, TR)"),
    ("19.68", "en genis protokol cifti (eski)"),
    ("19{,}68", "en genis protokol cifti (eski, TR)"),
    ("0.567", "B kolu egimi (eski)"),
    ("0{,}567", "B kolu egimi (eski, TR)"),
    ("10.91", "L2 yayilim (eski)"),
    ("10{,}91", "L2 yayilim (eski, TR)"),
    ("22.7", "oran ust (eski)"),
    ("22{,}7", "oran ust (eski, TR)"),
    ("20.9 ", "benzeri-benzeriyle oran (eski)"),
    ("3{,}122", "basarili-kaynak paydasi (eski, TR)"),
    ("3{,}122/5", "basarili-kaynak paydasi (eski)"),
    ("38.50", "basarili-kaynak orani (eski)"),
    ("38,50", "basarili-kaynak orani (eski, TR)"),
    ("62.50", "SVHN basarili-kaynak orani (eski)"),
    ("62,50", "SVHN basarili-kaynak orani (eski, TR)"),
]

bulundu = 0
for d, ne in BAYAT:
    for f in DOSYALAR:
        t = f.read_text(encoding="utf-8")
        if d in t:
            for i, satir in enumerate(t.splitlines(), 1):
                if d in satir:
                    yer = satir.index(d)
                    print(f"  {f.relative_to(ROOT)}:{i}  [{ne}]  "
                          f"...{satir[max(0, yer-60):yer+40]}...")
                    bulundu += 1
print(f"\nBAYAT DEGER: {bulundu}")
