import re, collections, subprocess, sys
kok = "/home/firat/projects/adeb_sci_1/paper/manuscript/"
bib = open(kok + "references.bib", encoding="utf-8").read()
keys = re.findall(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,", bib, re.M)
c = collections.Counter(k for _, k in keys)
print("girdi sayisi", len(keys))
print("cift anahtar:", [k for k, n in c.items() if n > 1])
# kume dengesi: her girdi icin parantez dengesi
parts = re.split(r"(?=^@)", bib, flags=re.M)
for p in parts:
    if not p.startswith("@"):
        continue
    if p.count("{") != p.count("}"):
        print("DENGESIZ:", p.split("\n")[0])
brif = """demontis2019adversarial adam2019reducing caussinus1965contribution jiang2011statistical
balduzzi2018reevaluating mahmood2021robustness shao2022adversarial mo2022adversarial naseer2022improving
awad2025defense bai2021transformers zhang2024why liu2023comprehensive sitawarin2024pubdef smouse1986multiple
touvron2021training wightman2021resnet bhojanapalli2021understanding recht2019imagenet singh2023revisiting
croce2021robustbench zhang2023tgr dong2018boosting wong2020fast engstrom2019robustness carmon2019unlabeled
gowal2020uncovering debenedetti2023light rice2020overfitting wang2023better sehwag2022robust addepalli2022efficient
rade2022reducing pang2022robustness jia2022lasat hendrycks2019using salman2020adversarially chen2024data
peng2023robust mantel1967detection springer2021little""".split()
print("brif anahtari eksik:", [k for k in brif if k not in c])
# yeni eklenen girdiler (HEAD'de olmayan)
head = subprocess.run(["git", "-C", kok, "show", "HEAD:paper/manuscript/references.bib"], capture_output=True, text=True).stdout
hk = set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,", head, re.M))
yeni = [k for _, k in keys if k not in hk]
print("yeni girdiler:", yeni)
print("HEAD'den silinen:", sorted(hk - set(c)))
# atiflar
for f in ["sections/02_related_work.tex", "sections/03_methodology.tex"]:
    t = open(kok + f, encoding="utf-8").read()
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n"))
    cites = set()
    for m in re.findall(r"\\cite[pt]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", t):
        cites.update(x.strip() for x in m.split(","))
    print(f, "tanimsiz atif:", sorted(x for x in cites if x not in c))
