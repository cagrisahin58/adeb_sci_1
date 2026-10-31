import re, glob, sys
# Brif 12 Sec. 11 sayim betigi (Y1 kopyasi) + ozet govdesi sayimi.
kok = sys.argv[1] if len(sys.argv) > 1 else "."
tot = 0
for f in [kok + "/main.tex"] + sorted(glob.glob(kok + "/sections/*.tex")):
    t = open(f, encoding="utf-8").read()
    lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
    n = len(" ".join(lines).split())
    tot += n
    print(n, f)
print(tot, "toplam (yorum satirlari haric)")
t = open(kok + "/main.tex", encoding="utf-8").read()
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", t, re.S)
ab = " ".join(re.sub(r"(?<!\\)%.*$", "", l) for l in m.group(1).split("\n"))
print(len(ab.split()), "ozet kelime (bosluk ayrimli)")
