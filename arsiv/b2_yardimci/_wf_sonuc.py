#!/usr/bin/env python3
"""Denetim akisinin nihai ciktisini ozetler."""
import json
import re
from pathlib import Path

P = Path("/mnt/c/Users/cagri/AppData/Local/Temp/claude/"
         "--wsl-localhost-Ubuntu-22-04-home-firat-projects-adeb-sci-1/"
         "0d0fab82-c6b8-472d-a420-d8ffb5857ab2/tasks/w1ixmsxsx.output")

t = P.read_text(encoding="utf-8", errors="replace")
m = re.search(r'\{"teyitli"', t)
if not m:
    print("teyitli blogu bulunamadi; ham uzunluk", len(t))
    raise SystemExit(1)

# dengeli parantez ile kes
i = m.start()
derinlik, j, dize = 0, i, False
while j < len(t):
    c = t[j]
    if dize:
        if c == "\\":
            j += 2
            continue
        if c == '"':
            dize = False
    else:
        if c == '"':
            dize = True
        elif c == "{":
            derinlik += 1
        elif c == "}":
            derinlik -= 1
            if derinlik == 0:
                break
    j += 1

d = json.loads(t[i:j + 1])
print(f"TEYIT EDILEN BULGU: {len(d.get('teyitli', []))}\n")
for x in d.get("teyitli", []):
    a = x.get("teyit", {}).get("duzeltilmis_agirlik", "?")
    print(f"[{a:6s}] ({x.get('boyut')}) {x.get('baslik')[:120]}")
    print(f"         {x.get('dosya')}:{x.get('satir', '')}")
    print(f"         iddia  : {str(x.get('iddia'))[:180]}")
    print()

c = d.get("curuyen", [])
print(f"CURUYEN / SUPHELI: {len(c)}")
for x in c:
    print("  -", str(x)[:120])
