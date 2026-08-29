#!/usr/bin/env python3
"""Yapay zeka uslup kalintilarini ve uzunluk dagilimini olcer. SALT OKUR."""
import re
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript")
BOLUMLER = ["sections/01_introduction.tex", "sections/02_related_work.tex",
            "sections/03_methodology.tex", "sections/04_experiments.tex",
            "sections/05_discussion.tex", "sections/06_conclusion.tex"]

# --- yaygin yapay zeka doldurucular ---
KALIP = [
    (r"\bnot only\b.{0,60}\bbut also\b", "not only ... but also"),
    (r"[Ii]t is important to note that", "it is important to note that"),
    (r"[Ii]t is worth noting that", "it is worth noting that"),
    (r"plays? a (crucial|key|vital|significant) role", "plays a crucial role"),
    (r"\bdelve into\b", "delve into"),
    (r"\bleverag(e|es|ing)\b", "leverage (fiil)"),
    (r"robust framework", "robust framework"),
    (r"comprehensive (analysis|study|framework)", "comprehensive X"),
    (r"shed(s)? light on", "shed light on"),
    (r"pave(s)? the way", "pave the way"),
    (r"\bIn conclusion\b", "In conclusion"),
    (r"\bFurthermore\b", "Furthermore"),
    (r"\bMoreover\b", "Moreover"),
    (r"\bAdditionally\b", "Additionally"),
    (r"\bNotably\b", "Notably"),
    (r"\bIndeed\b", "Indeed"),
    (r"may potentially", "may potentially"),
    (r"could potentially", "could potentially"),
    (r"\ba wide (range|variety) of\b", "a wide range of"),
    (r"\bcutting[- ]edge\b", "cutting-edge"),
    (r"\bstate[- ]of[- ]the[- ]art\b", "state-of-the-art"),
    (r"---", "em-dash (metin ici tire YASAK)"),
    (r"(?<![\-$0-9])--(?![\->0-9])", "en-dash"),
    (r"\bFirst,.{0,400}?\bSecond,.{0,400}?\b(Finally|Third),", "First/Second/Finally zinciri"),
]

print("=== YAPAY ZEKA USLUP KALINTILARI ===")
toplam = 0
for b in BOLUMLER:
    t = (ROOT / b).read_text(encoding="utf-8")
    for satir_no, satir in enumerate(t.splitlines(), 1):
        if satir.strip().startswith("%"):
            continue
        for desen, ad in KALIP:
            for m in re.finditer(desen, satir, re.S):
                yer = m.start()
                print(f"  {b.split('/')[-1]}:{satir_no}  [{ad}]")
                print(f"      ...{satir[max(0, yer-45):yer+len(m.group(0))+35]}...")
                toplam += 1
print(f"\nTOPLAM KALINTI: {toplam}")

# --- uzunluk dagilimi ---
print("\n=== UZUNLUK DAGILIMI ===")
print(f"{'bolum':28s}{'kelime':>9s}{'paragraf':>10s}{'tablo':>7s}{'sekil':>7s}")
tk = 0
for b in BOLUMLER:
    t = (ROOT / b).read_text(encoding="utf-8")
    govde = [s for s in t.splitlines()
             if len(s.strip()) > 120 and not s.strip().startswith(("\\", "%"))]
    kelime = sum(len(s.split()) for s in govde)
    tk += kelime
    print(f"{b.split('/')[-1]:28s}{kelime:>9d}{len(govde):>10d}"
          f"{len(re.findall(r'begin.table', t)):>7d}"
          f"{len(re.findall(r'begin.figure', t)):>7d}")
print(f"{'TOPLAM':28s}{tk:>9d}")

# --- ayni sayi kac kez? ---
print("\n=== EN COK TEKRARLANAN SAYILAR (>= 4 kez) ===")
hepsi = "\n".join((ROOT / b).read_text(encoding="utf-8") for b in BOLUMLER)
hepsi = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", hepsi, flags=re.S)
say = {}
for m in re.finditer(r"(?<![\d.])\d+\.\d+(?![\d])", hepsi):
    say[m.group(0)] = say.get(m.group(0), 0) + 1
for v, n in sorted(say.items(), key=lambda kv: -kv[1])[:14]:
    if n >= 4:
        print(f"  {v:>9s}  {n} kez")
