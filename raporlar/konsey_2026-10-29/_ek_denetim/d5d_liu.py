import re, html, sys
p = "/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis/"
r = open(p + "ares_rt_readme.md", encoding="utf-8").read().splitlines()
for i, l in enumerate(r[50:70], 51):
    print(i, l[:160])
t = open(p + "liu_html.html", encoding="utf-8").read()
txt = html.unescape(re.sub(r"<[^>]+>", " ", t))
txt = re.sub(r"\s+", " ", txt)
for m in re.finditer(r"Table\s*7", txt):
    print("---", txt[max(0, m.start()-100): m.start()+900])
    break
i = txt.find("57.3")
while i != -1 and i < len(txt):
    print("57.3 ctx:", txt[max(0, i-300): i+80])
    i = txt.find("57.3", i + 1)
    if i > 0 and txt[max(0,i-300):i].count("Table") == 0:
        pass
