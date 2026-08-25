#!/usr/bin/env python3
"""Bildiriyi B2 duzeltmesine gore gunceller.

Yalniz 'basarili kaynak' protokolunun tasidigi sayilar degisir; digerleri
tanim geregi ayni kalir. Her degisiklik tekil-eslesme kontrolunden gecer.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/paper/bildiri/bildiri.tex")
t = p.read_text(encoding="utf-8")

if "19.4 points" in t:
    print("zaten guncel")
    sys.exit(0)

CIFTLER = [
    # --- ozet ---
    (r"ranges from $+$4.4 to $+$14.6 points across the unconditioned, "
     r"target-correct, both-correct, and successful-source protocols, "
     r"a 3.3-fold spread",
     r"ranges from $+$4.4 to $+$19.4 points across the unconditioned, "
     r"target-correct, both-correct, and successful-source protocols, "
     r"a 4.4-fold spread",
     "ozet aralik+kat"),

    # --- 4. bolum govde ---
    (r"the measured asymmetry ranges from $+$4.4 to $+$14.6 points depending "
     r"only on which protocol is used: the spread between the largest and the "
     r"smallest protocol estimate is 10.5$\pm$0.8 points, a factor of 3.3.",
     r"the measured asymmetry ranges from $+$4.4 to $+$19.4 points depending "
     r"only on which protocol is used: the spread between the largest and the "
     r"smallest protocol estimate is 15.0$\pm$0.8 points, a factor of 4.4.",
     "govde aralik+yayilim+kat"),

    # --- eslesmis GA (Monte Carlo akis ayrimi sonrasi ucuncu basamak) ---
    (r"paired bootstrap CI [7.33; 9.21]",
     r"paired bootstrap CI [7.33; 9.22]",
     "esli GA"),

    # --- tablo satiri ---
    (r"Successful-source & 38.50$\pm$0.75 & 23.91$\pm$0.80 & $+$14.60 & $+$5.28 \\",
     r"Successful-source & 36.39$\pm$0.76 & 17.02$\pm$0.52 & $+$19.37 & $+$11.17 \\",
     "tablo satiri"),

    # --- paydalar ---
    (r"successful-source $N=3{,}122/5{,}331$.",
     r"successful-source $N=2{,}831/3{,}814$.",
     "paydalar"),
]

for eski, yeni, ad in CIFTLER:
    n = t.count(eski)
    if n != 1:
        print(f"BASARISIZ ({ad}): {n} eslesme -- HICBIR SEY YAZILMADI")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("bildiri guncellendi: 5 degisiklik")
