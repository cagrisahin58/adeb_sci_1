#!/usr/bin/env python3
"""Tartisma bolumunun paragraflarini yan yana listeler (ayna denetimi)."""
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")


def paragraflar(p):
    t = p.read_text(encoding="utf-8")
    return [s.strip() for s in t.split("\n")
            if len(s.strip()) > 200 and not s.strip().startswith("\\")
            and not s.strip().startswith("%")]


en = paragraflar(ROOT / "paper/manuscript/sections/05_discussion.tex")
tr = paragraflar(ROOT / "paper/manuscript_tr/sections/05_tartisma.tex")
print(f"EN {len(en)} paragraf, TR {len(tr)} paragraf\n")
for i in range(max(len(en), len(tr))):
    e = en[i][:72] if i < len(en) else "--- YOK ---"
    t = tr[i][:72] if i < len(tr) else "--- YOK ---"
    print(f"{i + 1:2d} EN {e}")
    print(f"   TR {t}")
    print()
