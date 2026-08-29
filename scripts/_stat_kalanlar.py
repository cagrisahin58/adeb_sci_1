#!/usr/bin/env python3
"""Istatistik hakeminin kalan bulgulari (S1, S2, S5, S6, S8) - dogrulama.

S1: her-ikisi-dogru "paired bootstrap GA" gercekte tohum basina GA uclarinin
    ORTALAMASI mi? Oyleyse bu tanimli bir aralik yordami degildir.
S2: "TOST equivalence rejected ... p=1.0" -- TOST'ta buyuk p EsDEGERLIK
    KURULAMADI demektir, "reddedildi" degil.
S5: TOST marji +/-2 hangi nicelikten tureti? (mutlak dogruluk oynakligi mi,
    transfer asimetrisi mi?)
S6: A kolu egim GA'si kendi kaldirac duyarliligini kapsiyor mu?
S8: L2 kolunun ucuncu ongorusu Denklem (1)'den TURUYOR mu (yani
    yanlislanabilir mi)?
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/workspace")


def yaz(baslik):
    print("\n" + "=" * 70)
    print(baslik)
    print("=" * 70)


# ---------------------------------------------------------------- S1
yaz("S1: her-ikisi-dogru bootstrap GA'si tanimli bir yordam mi?")
d = json.loads((ROOT / "results/c1_transfer/c1_transfer_summary.json")
               .read_text(encoding="utf-8"))


def gez(o, yol=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from gez(v, f"{yol}.{k}" if yol else k)
    elif isinstance(o, list):
        yield yol, o
    else:
        yield yol, o


alanlar = dict(gez(d))
ilgili = {k: v for k, v in alanlar.items()
          if "ci_low" in k or "ci_high" in k or "both_correct" in k.lower()}
for k in sorted(ilgili):
    print(f"  {k} = {ilgili[k]}")

# ---------------------------------------------------------------- S6
yaz("S6: A kolu egim GA'si kaldirac duyarliligini kapsiyor mu?")
for ad, yol in (("A kolu", "results/q1/e3_a_kolu_fit.json"),
                ("A kolu (alt)", "results/q1/e3_akolu_fit.json")):
    p = ROOT / yol
    if p.exists():
        j = json.loads(p.read_text(encoding="utf-8"))
        print(f"  {ad} ({yol}):")
        for k, v in j.items():
            if not isinstance(v, (list, dict)) or (isinstance(v, list) and len(v) < 6):
                print(f"    {k} = {v}")
    else:
        print(f"  {yol} YOK")

print("\n  --- q1 klasorundeki fit dosyalari ---")
for p in sorted((ROOT / "results/q1").glob("*fit*.json")):
    print(f"    {p.name}")
