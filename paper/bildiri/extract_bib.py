"""bildiri.bib: references.bib'den secili girdileri birebir kopyalar."""
import os
import re

ROOT = os.path.expanduser("~/projects/adeb_sci_1") if os.path.isdir(os.path.expanduser("~/projects/adeb_sci_1")) else "/workspace"
SRC = os.path.join(ROOT, "paper/manuscript/references.bib")
DST = os.path.join(ROOT, "paper/bildiri/bildiri.bib")

KEYS = [
    "szegedy2014intriguing", "goodfellow2015explaining", "madry2018towards",
    "zhang2019theoretically", "he2016deep", "dosovitskiy2021image",
    "krizhevsky2009learning", "rw2019timm", "loshchilov2017decoupled",
    "rice2020overfitting", "debenedetti2023light", "mo2022adversarial",
    "bai2021transformers", "benz2021adversarial", "ali2024adversarial",
    "croce2020reliable", "croce2021robustbench", "gowal2020uncovering",
    "liu2017delving", "dong2018boosting", "mahmood2021robustness",
    "ravikumar2023trend", "hurley2009comparing", "chalasani2020concise",
    "raghu2021vision", "wu2025vision",
]

with open(SRC, encoding="utf-8") as f:
    content = f.read()

# Girdileri @tip{anahtar, ... } bloklari olarak ayikla (dengeli parantez sayimi)
entries = {}
for m in re.finditer(r"@\w+\{([^,\s]+)\s*,", content):
    key = m.group(1)
    start = m.start()
    depth = 0
    for i in range(start, len(content)):
        if content[i] == "{":
            depth += 1
        elif content[i] == "}":
            depth -= 1
            if depth == 0:
                entries[key] = content[start : i + 1]
                break

missing = [k for k in KEYS if k not in entries]
if missing:
    raise SystemExit(f"EKSIK ANAHTARLAR: {missing}")

with open(DST, "w", encoding="utf-8") as f:
    f.write("% bildiri.bib — paper/manuscript/references.bib'den secili kopya (rev2 BLOK B)\n\n")
    for k in KEYS:
        f.write(entries[k] + "\n\n")
print(f"yazildi: {DST} ({len(KEYS)} girdi)")
