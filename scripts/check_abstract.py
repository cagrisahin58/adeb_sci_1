"""Ozet kelime sayisi ve minor denetimler."""
import re
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
t = (ROOT / "paper/manuscript/main.tex").read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", t, re.S)
words = re.findall(r"[A-Za-z0-9-]+", m.group(1))
print("ozet kelime sayisi:", len(words))
print("PLACE PHOTO:", t.count("PLACE PHOTO"))
