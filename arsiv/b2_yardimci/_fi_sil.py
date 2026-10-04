"""EN 04'te isi haritasi yorumundan sonra artakalan tek '\\fi' satirini siler (tam bir kez)."""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
p = Path(__file__).resolve().parents[2] / "paper/manuscript/sections/04_experiments.tex"
t = io.open(p, encoding="utf-8").read()
old = "Betik ve PDF duruyor.\n\\fi\n"
new = "Betik ve PDF duruyor.\n"
n = t.count(old)
if n == 1:
    io.open(p, "w", encoding="utf-8", newline="\n").write(t.replace(old, new))
    print("OK: artik \\fi silindi")
elif n == 0 and new in t and "\n\\fi\n" not in t:
    print("ZATEN")
else:
    print(f"HATA: {n} eslesme; dosyadaki \\fi sayisi: {t.count(chr(92) + 'fi' + chr(10))}")
    sys.exit(1)
