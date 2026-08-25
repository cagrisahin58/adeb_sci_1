#!/usr/bin/env python3
"""Denetimin buldugu iki AYNA boslugunu kapatir.

(1) Ingilizcede tabloda yazan +-0,23 ile metindeki +-0,24 farkini aciklayan
    yan cumle var, Turkcede YOK. Turk okuru celiskiyi aciklamasiz goruyordu.
(2) Ingilizcede Sekil 4'e gonderme yapan tam bir cumle var, Turkcede YOK.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
p = ROOT / "paper/manuscript_tr/sections/04_deneyler.tex"
t = p.read_text(encoding="utf-8")
hata = []

CIFTLER = [
    ("her ikisi doğru protokolünde fark $8{,}27\\pm0{,}24$ puandır; "
     "eşleştirilmiş bootstrap GA",
     "her ikisi doğru protokolünde fark $8{,}27\\pm0{,}24$ puandır; bu değer "
     "tablodaki $\\pm0{,}23$'ten yalnızca üçüncü ondalıkta ayrılmaktadır, "
     "çünkü iki kestirici farklıdır. Eşleştirilmiş bootstrap GA",
     "TR ucuncu ondalik"),

    ("\\label{fig:gradient_heatmap}\n\\end{figure}\n",
     "\\label{fig:gradient_heatmap}\n\\end{figure}\n\n"
     "Şekil~\\ref{fig:gradient_heatmap}, gradyan enerji haritalarını doğrudan "
     "karşılaştırmakta ve iki mimarinin girdi gradyanlarını hesaplama "
     "biçimindeki yapısal farkları görünür kılmaktadır.\n",
     "TR sekil 4 cumlesi"),
]

if "gradyan enerji haritalarını doğrudan" in t:
    print("zaten yapilmis")
    sys.exit(0)

for eski, yeni, ad in CIFTLER:
    if t.count(eski) != 1:
        hata.append(f"{ad}: {t.count(eski)} eslesme")
        continue
    t = t.replace(eski, yeni, 1)

if hata:
    print("BASARISIZ -- yazilmadi:", *hata, sep="\n  ")
    sys.exit(1)
p.write_text(t, encoding="utf-8")
print("TR ayna bosluklari kapatildi")
