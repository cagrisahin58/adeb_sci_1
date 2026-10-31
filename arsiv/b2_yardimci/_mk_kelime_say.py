import re, glob, sys
kok = sys.argv[1] if len(sys.argv) > 1 else "."
tot = 0
for f in [kok + "/main.tex"] + sorted(glob.glob(kok + "/sections/*.tex")):
    t = open(f, encoding="utf-8").read()
    lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
    n = len(" ".join(lines).split())
    tot += n
    print(n, f)
print(tot, "toplam (yorum satirlari haric)")
