#!/usr/bin/env python3
"""Ayristirma acikliklarini HAM artefakt degerlerinden yeniden yuvarlar.

Aciklıkları once tablodaki YUVARLANMIS degerlerden turetmistim
(13,57-8,27=5,30 ve 19,37-13,57=5,80). Ham degerlerden dogru sonuc
5,31 ve 5,79'dur. Bu betik once artefaktla dogrular, sonra iki dilde
duzeltir.
"""
import json
import re
import sys
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1")
d = json.loads((KOK / "results/c1_transfer/c1_transfer_summary.json")
               .read_text(encoding="utf-8"))
P = {k: v["diff"]["mean"] for k, v in d["protocols"].items()}

tc_bc = P["both_correct"] - P["target_correct"]
bc_ham = P["raw"] - P["both_correct"]
ham_ss = P["successful_source"] - P["raw"]
yayilim = P["successful_source"] - P["target_correct"]

print(f"  hedef-dogru -> her-ikisi-dogru : {tc_bc:.4f}  -> {tc_bc:.2f}")
print(f"  her-ikisi-dogru -> ham         : {bc_ham:.4f}  -> {bc_ham:.2f}")
print(f"  ham -> basarili-kaynak         : {ham_ss:.4f}  -> {ham_ss:.2f}")
print(f"  TOPLAM yayilim                 : {yayilim:.4f}  -> {yayilim:.2f}")
assert abs((tc_bc + bc_ham + ham_ss) - yayilim) < 1e-9, "acikliklar toplami tutmuyor"

DOGRU_BC = f"{bc_ham:.2f}"   # 5.31
DOGRU_SS = f"{ham_ss:.2f}"   # 5.79

DOSYALAR = [
    ("manuscript", ["sections/01_introduction.tex", "sections/04_experiments.tex",
                    "sections/06_conclusion.tex", "main.tex"], "5.30", "5.80"),
    ("manuscript_tr", ["sections/01_giris.tex", "sections/04_deneyler.tex",
                       "sections/06_sonuc.tex", "main.tex"],
     "5{,}30", "5{,}80"),
]

toplam = 0
for taban, dosyalar, eski_bc, eski_ss in DOSYALAR:
    yeni_bc = DOGRU_BC if "{,}" not in eski_bc else DOGRU_BC.replace(".", "{,}")
    yeni_ss = DOGRU_SS if "{,}" not in eski_ss else DOGRU_SS.replace(".", "{,}")
    for f in dosyalar:
        p = KOK / "paper" / taban / f
        t = p.read_text(encoding="utf-8")
        n = t.count(eski_bc) + t.count(eski_ss)
        if n:
            t = t.replace(eski_bc, yeni_bc).replace(eski_ss, yeni_ss)
            p.write_text(t, encoding="utf-8")
            toplam += n
            print(f"  [+] {taban}/{f}: {n} degisiklik")

if toplam == 0:
    # zaten duzeltilmis mi?
    kontrol = (KOK / "paper/manuscript/main.tex").read_text(encoding="utf-8")
    if DOGRU_BC in kontrol and DOGRU_SS in kontrol:
        print("  [=] zaten duzeltilmis")
    else:
        sys.exit("BASARISIZ: ne eski ne yeni deger bulundu")
print(f"\ntoplam {toplam} degisiklik")
