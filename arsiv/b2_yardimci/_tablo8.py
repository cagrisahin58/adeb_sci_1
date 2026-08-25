#!/usr/bin/env python3
"""Tablo VIII'in ilk IKI satiri artefaktla tutmuyordu (2026-08-06'dan beri).

Artefakt (results/c1_c45_summary.json ve C1_C45_RAPORU.md, ikisi birebir ayni):
  Blok 1: CLS 0.9993 · yama ort. 0.9989 · tum jetonlar 0.9942
  Blok 2: CLS 0.9910 · yama ort. 0.9957 · tum jetonlar 0.9868
Metinde ise Blok 1 = 0.9964 / 0.9990 / 0.9975 ve Blok 2 = 0.9893 / 0.9954 /
0.9911 yaziyordu. Satir 3-12'nin OTUZ ALTI hucresi ve ResNet sutununun
tamami tutuyor; yalniz ilk iki satir sapiyordu, yani dizgi degil aktarim
hatasi. Ayni hatali satirlar IKI DILDE de vardi.

Sapma yuvarlamayi asiyor (0.9964 vs 0.9993 -> 0.0029). Ustelik bir NITEL
ayrinti ters donuyordu: artefaktta blok 1'de CLS (0.9993) yama
ortalamasindan (0.9989) DAHA AZ kayarken tablo tersini gosteriyordu.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata = []

CIFTLER = [
    ("paper/manuscript/sections/04_experiments.tex",
     [("1 & 0.9964 & 0.9990 & 0.9975 & layer1.0 & 0.9951 \\\\",
       "1 & 0.9993 & 0.9989 & 0.9942 & layer1.0 & 0.9951 \\\\", "EN blok 1"),
      ("2 & 0.9893 & 0.9954 & 0.9911 & layer1.1 & 0.9918 \\\\",
       "2 & 0.9910 & 0.9957 & 0.9868 & layer1.1 & 0.9918 \\\\", "EN blok 2")]),
    ("paper/manuscript_tr/sections/04_deneyler.tex",
     [("1 & 0,9964 & 0,9990 & 0,9975 & layer1.0 & 0,9951 \\\\",
       "1 & 0,9993 & 0,9989 & 0,9942 & layer1.0 & 0,9951 \\\\", "TR blok 1"),
      ("2 & 0,9893 & 0,9954 & 0,9911 & layer1.1 & 0,9918 \\\\",
       "2 & 0,9910 & 0,9957 & 0,9868 & layer1.1 & 0,9918 \\\\", "TR blok 2")]),
]

for rel, ciftler in CIFTLER:
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            continue
        t = t.replace(eski, yeni, 1)
    if not hata and t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"  yamalandi: {rel}")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("tamam")
