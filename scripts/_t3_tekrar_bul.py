#!/usr/bin/env python3
"""Bolumler arasi (ve ici) YAKIN-TEKRAR cumleleri bulur.

Sayfa kisaltmasi icin: hangi cumleler baska bir yerde neredeyse aynen
soylenmis? Jaccard benzerligi >= esik olan cift raporlanir.
"""
import re
import sys
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
ESIK = float(sys.argv[1]) if len(sys.argv) > 1 else 0.45
DOLGU = set("the of a and is to in that it we as for on with are this by an be "
            "not or from at its than which we our".split())


def cumleler(p):
    t = p.read_text(encoding="utf-8")
    t = re.sub(r"(?m)^%.*$", "", t)
    t = re.sub(r"\\begin\{(figure|table|tabular)\}.*?\\end\{\1\}", " ", t, flags=re.DOTALL)
    t = re.sub(r"\\(label|ref|eqref|cite|citep)\{[^}]*\}", " ", t)
    t = re.sub(r"\\[a-zA-Z]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    out = []
    for c in re.split(r"(?<=[.!?]) +", t):
        c = c.strip()
        if len(c.split()) >= 12:
            out.append(c)
    return out


hepsi = []
for p in sorted(KOK.glob("0*.tex")):
    for c in cumleler(p):
        hepsi.append((p.name[:2], c))


def cek(c):
    return {w for w in re.findall(r"[a-z][a-z-]+", c.lower()) if w not in DOLGU}


kume = [cek(c) for _, c in hepsi]
ciftler = []
for i in range(len(hepsi)):
    for j in range(i + 1, len(hepsi)):
        a, b = kume[i], kume[j]
        if not a or not b:
            continue
        j_ = len(a & b) / len(a | b)
        if j_ >= ESIK:
            ciftler.append((j_, i, j))

ciftler.sort(reverse=True)
print(f"esik {ESIK}, {len(ciftler)} yakin-tekrar cifti\n")
toplam = 0
for s, i, j in ciftler[:25]:
    n = min(len(hepsi[i][1].split()), len(hepsi[j][1].split()))
    toplam += n
    print(f"--- benzerlik {s:.2f}  (~{n} kelime kazanilabilir)")
    print(f"  [{hepsi[i][0]}] {hepsi[i][1][:210]}")
    print(f"  [{hepsi[j][0]}] {hepsi[j][1][:210]}\n")
print(f"ilk 25 ciftte kabaca {toplam} kelimelik ortusme")
