import re, sys
# Bir .tex dosyasini bos satirla ayrilmis bloklara boler, her blogun yorumsuz kelime sayisini yazar.
t = open(sys.argv[1], encoding="utf-8").read()
lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
blok, no, bas = [], 0, 1
for i, l in enumerate(lines + [""], 1):
    if l.strip() == "":
        if blok:
            n = len(" ".join(blok).split())
            print(f"{n:5d}  satir {bas}: {' '.join(blok)[:70]}")
        blok, bas = [], i + 1
    else:
        blok.append(l)
