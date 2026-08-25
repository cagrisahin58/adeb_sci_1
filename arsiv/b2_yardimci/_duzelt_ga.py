#!/usr/bin/env python3
"""Sertlestirilmis kapinin actigi IKI kalemi kapatir.

(1) SVHN esli bootstrap GA'si metinde [-0.77, +0.06] yaziyordu; artefakt
    ortalamalari [-0.755, 0.065] -> iki basamakta [-0.76, +0.07]. IKI SINIR
    DA yanlisti. Kapi bunu goremiyordu cunku '0.07' yalniz gradyan
    tablosundaki '0.079' icinde eslesiyordu (ilgisiz nicelik).

(2) 'E6 O1 r' kontrolu, makalenin BILEREK raporlamadigi bir korelasyonu
    ariyordu: Bolum 4.6 acikca "we report the slope rather than a
    correlation because the eighteen directions take only seven distinct
    target-error values" diyor. Kontrol yalniz oznitelik tablosundaki
    '0.9990' icinde eslesip geciyordu. Sayi kontrolu KALDIRILDI; yerine
    iddia kapisina KARARIN AYAKTA oldugunu sinayan bir muhafiz kondu.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata = []


def yama(rel, ciftler, imza=None):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza and imza in t:
        print(f"  atlandi: {rel}")
        return
    for eski, yeni, ad in ciftler:
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"  yamalandi: {rel}")


# --- (1) SVHN GA, iki dil ---
yama("paper/manuscript/sections/04_experiments.tex",
     [("a paired bootstrap CI of $[-0.77, +0.06]$",
       "a paired bootstrap CI of $[-0.76, +0.07]$", "EN SVHN GA")])
yama("paper/manuscript_tr/sections/04_deneyler.tex",
     [("eşleştirilmiş bootstrap güven aralığı $[-0{,}77;\\ +0{,}06]$",
       "eşleştirilmiş bootstrap güven aralığı $[-0{,}76;\\ +0{,}07]$", "TR SVHN GA")])

# --- (2) kaldirilan sayi kontrolu ---
yama("scripts/verify_manuscript_numbers.py",
     [('chk("E6 O1 r", e6o["O1_yon"]["pearson_r"], 3)',
       '# KALDIRILDI (2026-08-25): Bolum 4.6 korelasyon YERINE egimi raporlamaya\n'
       '# karar verdi ("we report the slope rather than a correlation ..."), yani\n'
       '# bu sayi metinde YOK. Kontrol yalniz oznitelik tablosundaki 0.9990 icinde\n'
       '# eslesip geciyordu. Kararin AYAKTA oldugunu iddia kapisi denetliyor (I1).\n'
       '# chk("E6 O1 r", e6o["O1_yon"]["pearson_r"], 3)',
       "E6 O1 r kaldirildi")])

# --- kararin muhafizi ---
yama("scripts/check_manuscript_claims.py",
     [('# --- H: B2 MUHAFIZI',
       '# --- I: E6\'da korelasyon YERINE egim raporlaniyor mu ---\n'
       '# Sayi kapisindan bir kontrol KALDIRILDI (E6 O1 r) cunku makale o sayiyi\n'
       '# bilerek raporlamiyor. Karar sessizce geri alinabilsin diye degil,\n'
       '# muhafizla korunsun diye buraya kondu.\n'
       'kontrol("I1. EN E6 korelasyon yerine egim gerekcesi duruyor",\n'
       '        "we report the slope rather than a correlation" in en)\n'
       'kontrol("I1. TR E6 korelasyon yerine egim gerekcesi duruyor",\n'
       '        "korelasyon yerine eğimi raporluyoruz" in tr)\n'
       '\n'
       '# --- H: B2 MUHAFIZI',
       "I1 muhafizi")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("tamam")
