import re, glob, collections
kok = "/home/firat/projects/adeb_sci_1/paper/manuscript/"
dosyalar = [kok + "main.tex"] + sorted(glob.glob(kok + "sections/*.tex"))
tanim = collections.defaultdict(list); gonder = collections.defaultdict(list)
for f in dosyalar:
    t = open(f, encoding="utf-8").read()
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n"))
    ad = f.split("/")[-1]
    for m in re.findall(r"\\label\{([^}]*)\}", t): tanim[m].append(ad)
    for m in re.findall(r"\\(?:eq|c|C)?ref\{([^}]*)\}", t):
        for x in m.split(","): gonder[x.strip()].append(ad)
benim = ("02_related_work.tex", "03_methodology.tex")
print("cift tanim:", {k: v for k, v in tanim.items() if len(v) > 1})
for k, v in sorted(tanim.items()):
    if any(x in benim for x in v) and k not in gonder:
        print("GONDERILMEYEN (benim):", k)
for k, v in sorted(gonder.items()):
    if any(x in benim for x in v) and k not in tanim:
        print("TANIMSIZ GONDERME (benim):", k, v)
for k, v in sorted(gonder.items()):
    if k not in tanim:
        print("tanimsiz gonderme (genel):", k, sorted(set(v)))
