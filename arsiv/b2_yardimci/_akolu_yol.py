#!/usr/bin/env python3
"""Iki-kol uydurmasi ve sekli A kolu dizinine PARAMETRELI baglar.

E3A_DIR verilirse o dizin okunur; verilmezse eski varsayilan. Ayrica uretilen
JSON'a hangi dizinden geldigi YAZILIR -- kapinin H2 muhafizi bunu okur, yani
"yeni A kolundan uretildi" iddiasi dosyanin kendisinden dogrulanabilir olur.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata = []


def yama(rel, ciftler, imza):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza in t:
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


yama("scripts/q1_e3_iki_kol_fit.py", [
    ('    ad = ROOT / "results/q1/e3_akolu"',
     '    # E3A_DIR: B2 sonrasi yeniden kosum ayri dizine yazildi.\n'
     '    ad = ROOT / os.environ.get("E3A_DIR", "results/q1/e3_akolu")',
     "A kolu yolu"),
], "E3A_DIR")

yama("scripts/q1_e3_figur.py", [
    ('        d = ROOT / "results/q1/e3_akolu"',
     '        d = ROOT / os.environ.get("E3A_DIR", "results/q1/e3_akolu")',
     "sekil A kolu yolu"),
], "E3A_DIR")

# os import'u ikisinde de var mi
for rel in ("scripts/q1_e3_iki_kol_fit.py", "scripts/q1_e3_figur.py"):
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    if "\nimport os\n" not in t and not t.startswith("import os\n"):
        satirlar = t.split("\n")
        for i, s in enumerate(satirlar):
            if s.startswith("import ") or s.startswith("from "):
                satirlar.insert(i, "import os")
                break
        p.write_text("\n".join(satirlar), encoding="utf-8")
        print(f"  os import eklendi: {rel}")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("tamam")
