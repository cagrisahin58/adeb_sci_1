"""Kapi ciktisindaki EKSIK satirlarin metin baglamini basar (yalniz okuma)."""
import re, subprocess, sys
from pathlib import Path
B = Path("/workspace/paper/manuscript")
out = subprocess.run([sys.executable, "-B", "/workspace/scripts/verify_manuscript_numbers.py"] + sys.argv[1:],
                     capture_output=True, text=True).stdout
seen = set()
for s in out.splitlines():
    m = re.match(r"\s+EKSIK  (\S+?):(\d+)  (?:p < )?(.+?)  -- (\S+)", s)
    if not m:
        continue
    f, ln, x, tur = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    satir = (B / f).read_text(encoding="utf-8").split("\n")[ln - 1]
    x0 = x.split()[0].lstrip("-[").rstrip(",]")
    x0 = x0.split("e")[0] if "e-" in x0 else x0
    i = satir.find(x0)
    print(f"{f}:{ln} [{tur}] {x}  ::  {satir[max(0, i - 110):i + 70] if i >= 0 else satir[:160]}")
