#!/usr/bin/env python3
"""TR makalesinde MATEMATIK KIPINDE ciplak ondalik virgul taramasi.

Turkce metinde `0,1` METIN kipinde DOGRUDUR. Sorun yalnizca matematik
kipindedir: `$0,1$` LaTeX'te virgulu NOKTALAMA sayar ve arkasina bosluk
koyar ("0, 1" gibi gorunur). Dogru kullanim `$0{,}1$`.

Bu betik $...$ araliklarini ayikleyip yalniz onlarin icindeki rakam-virgul-
rakam desenlerini raporlar; metin kipindeki dogru virgullere DOKUNMAZ.

Kullanim: docker exec -w /workspace adeb_eval python scripts/q1_tr_decimal_check.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path("/workspace") if pathlib.Path("/workspace/results").is_dir() \
    else pathlib.Path.home() / "projects/adeb_sci_1"
BASE = ROOT / "paper" / "manuscript_tr"

# $...$ (tek dolar) araliklari; \$ kacislari haric tutulur
MATH = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$", re.DOTALL)
BAD = re.compile(r"\d,\d")


def main():
    files = sorted(BASE.rglob("*.tex"))
    total_bad = 0
    rows = []
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8")
        except Exception:
            continue
        lines = txt.splitlines()
        for i, line in enumerate(lines, 1):
            for m in MATH.finditer(line):
                seg = m.group(1)
                if BAD.search(seg):
                    total_bad += 1
                    rows.append((str(f.relative_to(ROOT)), i, seg.strip()[:70]))

    if not rows:
        print("TEMIZ: matematik kipinde ciplak ondalik virgul YOK.")
        print("(Metin kipindeki virguller Turkce icin dogrudur, taranmadi.)")
        return 0

    print("MATEMATIK KIPINDE CIPLAK VIRGUL BULUNDU (%d yer):" % total_bad)
    print("Dogru kullanim: $0{,}1$  --  yanlis: $0,1$ (virgul noktalama sayilir,")
    print("arkasina bosluk konur).\n")
    for path, ln, seg in rows[:40]:
        print("  %s:%d  ->  $%s$" % (path, ln, seg))
    if len(rows) > 40:
        print("  ... ve %d yer daha" % (len(rows) - 40))
    return 1


if __name__ == "__main__":
    sys.exit(main())
