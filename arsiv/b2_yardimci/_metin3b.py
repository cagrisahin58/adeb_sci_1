#!/usr/bin/env python3
"""B2 metin -- 3b: SVHN yayilim paragrafinin TEKDUZE-ARTIS iddiasi.

Duzeltilmis tanimda uc veri kumesi arasindaki iliski TEKDUZE DEGIL:
  SVHN     fark ~1,85  -> yayilim  3,70
  CIFAR-10 fark ~11    -> yayilim 15,01
  CIFAR-100 fark ~21   -> yayilim 13,83
Yani en buyuk fark en buyuk yayilimi vermiyor. "Tam olarak temiz dogruluk
farklarinin sirasiyla" ve "daha kucuk bir fark daha kucuk bir yayilim uretir"
ifadeleri artik savunulamaz; yerine OLCULEN sey yazilir. Bu, B kolunun dort
protokollu eiminin zaten ince olan dayanagiyla da tutarlidir.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue
        n = t.count(eski)
        if n != 1:
            hata.append(f"{rel} :: {ad}: {n} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


yama("paper/manuscript/sections/04_experiments.tex", [(
    "A smaller gap produces a smaller spread; and once the spread is small enough, "
    "it no longer clears the asymmetry itself, so the sign becomes a property of the "
    "protocol rather than of the architectures.",
    "The relation is not monotone across the three: the largest gap does not produce "
    "the largest spread, and CIFAR-100 sits slightly below CIFAR-10. What separates "
    "the datasets here is the near-matched pair, not the ordering among the "
    "mismatched ones. Once the spread is small enough it no longer clears the "
    "asymmetry itself, so the sign becomes a property of the protocol rather than of "
    "the architectures.",
    "EN SVHN tekduze")])

yama("paper/manuscript_tr/sections/04_deneyler.tex", [(
    "SVHN'de protokol yayılımı $3{,}65\\pm0{,}19$ puandır; CIFAR-10'da "
    "$10{,}45\\pm0{,}76$, CIFAR-100'de $13{,}58\\pm1{,}71$ idi; yani tam olarak temiz "
    "doğruluk farklarının sırasıyla ($1{,}85$, $\\approx11$, $\\approx21$ puan). "
    "Daha küçük bir fark daha küçük bir yayılım üretmekte; yayılım yeterince "
    "küçüldüğünde ise",
    "SVHN'de protokol yayılımı $3{,}70\\pm0{,}62$ puandır; CIFAR-10'da "
    "$15{,}01\\pm0{,}84$, CIFAR-100'de $13{,}83\\pm1{,}30$ puandır; temiz doğruluk "
    "farkları ise sırasıyla $1{,}85$, $\\approx11$ ve $\\approx21$ puandır. İlişki üçü "
    "arasında tekdüze değildir: en büyük fark en büyük yayılımı vermemekte, "
    "CIFAR-100 CIFAR-10'un bir miktar altında kalmaktadır. Veri kümelerini burada "
    "ayıran şey, eşitlenmeye yakın çift ile diğerleri arasındaki uzaklıktır; "
    "eşitlenmemiş ikisi arasındaki sıralama değil. Yayılım yeterince küçüldüğünde ise",
    "TR SVHN tekduze")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
