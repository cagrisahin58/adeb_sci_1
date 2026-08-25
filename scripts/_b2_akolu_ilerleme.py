#!/usr/bin/env python3
"""A kolu v1 (eski) ve v2 (B2 sonrasi) nokta sayilarini yorunge bazinda kiyaslar."""
import re
from collections import Counter
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")


def say(d):
    if not d.is_dir():
        return Counter()
    return Counter(re.sub(r"_ep\d+\.json$", "", f.name) for f in d.glob("*.json"))


v1 = say(ROOT / "results/q1/e3_akolu")
v2 = say(ROOT / "results/q1/e3_akolu_v2")
eksik = 0
for k in sorted(set(v1) | set(v2)):
    a, b = v1.get(k, 0), v2.get(k, 0)
    if a != b:
        eksik += a - b
    print(f"{k:26s} v1={a:3d}  v2={b:3d}   {'' if a == b else '<<< EKSIK ' + str(a - b)}")
print(f"\ntoplam v1={sum(v1.values())}  v2={sum(v2.values())}  eksik={eksik}")
