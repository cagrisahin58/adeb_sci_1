#!/usr/bin/env python3
"""FAZ 2.6: gonderim malzemelerinin yanlis beyanlari.

(a) ATEEC bildirisinin kapsami IKI belgede yanlis: "mimari basina TEK
    kosum" deniyor. Bildiri "three independent training runs" kullaniyor
    (paper/bildiri/bildiri.tex, 23 adet +/- gosterimi). Fark yalnizca
    VERI KUMESI kapsami: bildiri CIFAR-10 ile sinirli, dergi surumu
    CIFAR-100 ve SVHN'i de kapsiyor. Bu beyan, portalin "previously
    presented" alani ve benzerlik degerlendirmesi icin onemlidir.
(b) paper/cover_letter.txt (2026-02-16) guncel LaTeX surumunun bayat bir
    kopyasi; kendi basliginda da oyle diyor. Silinir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper")

if not uygula([
    ("cover_letter.tex",
     r"A preliminary subset of these results, limited to CIFAR-10 and a single "
     r"training run per architecture, is under review as a conference paper; "
     r"the present manuscript is the extended version and cites it.",
     r"A preliminary subset of these results, limited to CIFAR-10, is under "
     r"review as a conference paper; the present manuscript is the extended "
     r"version and cites it. The conference paper reports the same three "
     r"training runs per architecture; what the journal version adds is the "
     r"CIFAR-100 and SVHN replications, the $L_2$ threat model, the "
     r"three-architecture matrix and the behavioral analyses.",
     "2.6 kapak mektubu ATEEC kapsami"),

    ("pre_submission_checklist.md",
     "This IS a conference extension: a preliminary subset (CIFAR-10 only, one "
     "run per architecture) is under review at ATEEC 2026.",
     "This IS a conference extension: a preliminary subset (CIFAR-10 only; the "
     "same three runs per architecture) is under review at ATEEC 2026.",
     "2.6 kontrol listesi ATEEC kapsami"),
], KOK / "submission"):
    sys.exit(1)

bayat = KOK / "cover_letter.txt"
if bayat.exists():
    bayat.unlink()
    print("  [+] bayat paper/cover_letter.txt silindi (2026-02-16)")
else:
    print("  [=] bayat kapak mektubu zaten yok")
