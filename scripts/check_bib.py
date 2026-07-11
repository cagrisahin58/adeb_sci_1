"""Bib girdileri ile \\cite kullanimlarinin iki yonlu kapanis kontrolu."""
import glob
import re

ROOT = "/home/firat/projects/adeb_sci_1/paper/manuscript"
bib = open(f"{ROOT}/references.bib", encoding="utf-8", errors="replace").read()
keys = set(re.findall(r"@\w+\{([^,]+),", bib))

tex = ""
for f in glob.glob(f"{ROOT}/main.tex") + glob.glob(f"{ROOT}/sections/*.tex"):
    tex += open(f, encoding="utf-8", errors="replace").read()

cited = set()
for m in re.findall(r"\\cite\{([^}]+)\}", tex):
    for k in m.split(","):
        cited.add(k.strip())

print("bib girdisi:", len(keys), "| benzersiz atif:", len(cited))
print("KULLANILMAYAN BIB:", sorted(keys - cited) or "YOK")
print("BIBDE OLMAYAN CITE:", sorted(cited - keys) or "YOK")
