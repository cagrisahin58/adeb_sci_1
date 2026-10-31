"""Probe icin main.tex kopyasi: ieeeaccess.cls belge sonunda \\EOD ister.

Makalenin kendisi degismez; kopya karalama klasorune yazilir.
"""
import io
import re
import sys

src = "//wsl.localhost/Ubuntu-22.04/home/firat/projects/adeb_sci_1/paper/manuscript/main.tex"
dst = sys.argv[1]
t = io.open(src, encoding="utf-8").read()
pat = re.compile(r"^\\titlepgskip=-21pt[ \t]*\r?$", re.M)
hits = pat.findall(t)
assert len(hits) == 1, hits
ek = "\n% PROBE KOPYASI: ieeeaccess.cls belge sonunda EOD ister (cls satir 1080)\n\\EOD"
t = pat.sub(lambda m: m.group(0) + ek, t)
io.open(dst, "w", encoding="utf-8", newline="\n").write(t)
print("ok", dst)
