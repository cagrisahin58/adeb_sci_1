import re, sys
f = sys.argv[1]
t = open(f, encoding="utf-8").read().split("\n")
cur = "giris"; counts = {}; order = []
blk = None
for l in t:
    m = re.match(r"\\(sub)*section\{([^}]*)\}", l)
    if m:
        cur = m.group(2)
    s = re.sub(r"(?<!\\)%.*$", "", l)
    key = cur
    if "\\begin{table" in s: blk = "TABLO"
    if blk: key = cur + " [tablo]"
    if key not in counts:
        counts[key] = 0; order.append(key)
    counts[key] += len(s.split())
    if "\\end{table" in s: blk = None
for k in order:
    print(counts[k], k)
