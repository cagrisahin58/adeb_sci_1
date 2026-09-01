#!/usr/bin/env python3
"""FAZ 2.5: zincir celiskileri (giris <-> govde <-> sonuc).

(a) GIRIS "asimetrinin yonu kararlidir" diyor, NITELIKSIZ. SONUC ise
    "CIFAR'larda kararli, veri kumeleri arasinda DEGIL; SVHN'de dort
    protokolun ikisi isareti tersine ceviriyor" diyor. Giris rejim
    kaydini tasimali.
(b) OZET SVHN'i saf protokol kaosu gibi sunuyor ("iki CNN, iki ViT"),
    govde (04:228) ise bolunmenin RASGELE OLMADIGINI, onayladigimiz iki
    protokolun BIRBIRIYLE UYUSTUGUNU soyluyor. Ozet govdeyi asiyor.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper")

if not uygula([
    # ---------------- (a) giris rejim kaydi ----------------
    ("sections/01_introduction.tex",
     r"The protocol decides whether an equivalence test is accepted or "
     r"rejected, while the direction of the asymmetry, unlike its magnitude, "
     r"is stable.",
     r"The protocol decides whether an equivalence test is accepted or "
     r"rejected, while the direction of the asymmetry, unlike its magnitude, "
     r"is stable \emph{as long as the two models differ in clean accuracy}; "
     r"once they are matched, two of the four protocols reverse it.",
     "2.5 EN giris rejim kaydi"),

    # ---------------- (b) ozet: govdeyi asma ----------------
    ("main.tex",
     "the protocol decides the sign and not just the size: two report a CNN "
     "advantage and two a ViT advantage.",
     "the protocol decides the sign as well as the size: two report a CNN "
     "advantage and two a ViT advantage, though the two we endorse agree.",
     "2.5 EN ozet SVHN"),

    ("main.tex",
     "Three further readings fail to replicate under direct measurement, and we "
     "close with reporting requirements",
     "Three further readings fail to replicate, and we close with reporting "
     "requirements",
     "2.5 EN ozet kirpma"),
], KOK / "manuscript"):
    sys.exit(1)

if not uygula([
    ("sections/01_giris.tex",
     r"Protokol, bir eşdeğerlik testinin kabul mü ret mi edileceğine karar "
     r"vermekte; asimetrinin yönü ise büyüklüğünün aksine kararlı kalmaktadır.",
     r"Protokol, bir eşdeğerlik testinin kabul mü ret mi edileceğine karar "
     r"vermekte; asimetrinin yönü ise büyüklüğünün aksine, \emph{iki model "
     r"temiz doğrulukta ayrıştığı sürece} kararlı kalmaktadır; eşitlendiklerinde "
     r"dört protokolün ikisi yönü tersine çevirmektedir.",
     "2.5 TR giris rejim kaydi"),

    ("main.tex",
     "SVHN'de ise protokol yalnızca büyüklüğe değil işarete de karar "
     "vermektedir: iki protokol CNN, ikisi ViT üstünlüğü bildirmektedir.",
     "SVHN'de ise protokol büyüklük kadar işarete de karar vermektedir: iki "
     "protokol CNN, ikisi ViT üstünlüğü bildirmekte, onayladığımız iki protokol "
     "ise birbiriyle uyuşmaktadır.",
     "2.5 TR ozet SVHN"),
], KOK / "manuscript_tr"):
    sys.exit(1)

for ad in ("manuscript", "manuscript_tr"):
    t = (KOK / ad / "main.tex").read_text(encoding="utf-8")
    oz = re.search(r"\\begin\{abstract\}(.+?)\\end\{abstract\}", t, re.DOTALL)
    print(f"  {ad} ozet: {len(oz.group(1).split())} kelime")
