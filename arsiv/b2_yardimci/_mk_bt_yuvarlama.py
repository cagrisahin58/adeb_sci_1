import re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")
kok = "/home/firat/projects/adeb_sci_1/paper/manuscript/"
fs = [kok + "main.tex"] + sorted(glob.glob(kok + "sections/*.tex"))
ana = ["0.936", "0.925", "0.948", "0.012", "0.566", "0.364", "0.415", "0.314", "0.260",
       "0.186", "0.335", "0.003", "0.960", "0.941", "0.976", "3.20", "7.40", "0.840",
       "0.143", "0.142", "0.197", "0.090", "0.893", "0.944", "4.36", "19.37", "0.0044",
       "0.541", "0.115", "0.251", "0.136", "1.083", "0.989", "1.000", "62.76", "37.93", "29.14",
       "55.53", "48.58", "0.919", "0.890", "0.201", "0.304", "0.413", "0.087"]
metin = {}
for f in fs:
    t = open(f, encoding="utf-8").read()
    metin[f] = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
for x in ana:
    tam = []
    for f, ls in metin.items():
        for i, l in enumerate(ls, 1):
            if re.search(r"(?<![\d.])" + re.escape(x) + r"(?!\d)", l):
                tam.append(f.split("/")[-1] + ":" + str(i))
    # yuvarlanmis bicim
    d = len(x.split(".")[1])
    yv = []
    if d >= 3:
        r = ("%." + str(d - 1) + "f") % float(x)
        if r != x:
            for f, ls in metin.items():
                for i, l in enumerate(ls, 1):
                    if re.search(r"(?<![\d.])" + re.escape(r) + r"(?![\d])", l):
                        yv.append(f.split("/")[-1] + ":" + str(i))
    print(x, "tam:", len(tam), sorted(set(t.split(":")[0] for t in tam)), "| yuvarlak", r if d >= 3 else "-", yv[:6])
