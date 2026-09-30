"""Atif-baglam denetimi (2026-09-30) icin TR aynasindaki isaretli cumleleri bul.
Salt okur. Kullanim: python3 arsiv/b2_yardimci/_atif_tr_bul.py  (depo kokunden)
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "paper" / "manuscript_tr" / "sections"
BILDIRI = ROOT / "paper" / "bildiri" / "bildiri.tex"

KEYS = [
    "ravikumar2023trend", "bhojanapalli2021understanding", "shao2022adversarial",
    "jain2024towards", "chen2023understanding", "demontis2019adversarial",
    "chalasani2020concise", "lyu2024adaptive", "zhao2025revisiting",
    "rice2020overfitting", "croce2021robustbench", "wang2023better",
    "mahmood2021robustness",
]


def sentences_with(line, key, width=380):
    """Anahtar kelimeyi iceren cumleyi (kabaca) dondur."""
    out = []
    for m in re.finditer(re.escape(key), line):
        start = max(0, m.start() - width)
        end = min(len(line), m.end() + 120)
        out.append(line[start:end].replace("\n", " "))
    return out


for path in sorted(TR.glob("*.tex")):
    text = io.open(path, encoding="utf-8").read().splitlines()
    for key in KEYS:
        for i, line in enumerate(text, 1):
            if key in line and not line.lstrip().startswith("%"):
                for s in sentences_with(line, key):
                    print(f"[{path.name}:{i}] <{key}> ...{s}...")
                    print()

print("=== bildiri.tex satir 57 ===")
lines = io.open(BILDIRI, encoding="utf-8").read().splitlines()
print(lines[56][:900])
