import re, html
p = "/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis/zhang_html.html"
t = open(p, encoding="utf-8", errors="replace").read()
txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
i = txt.find("infimum of loss gradient simila")
print(txt[i: i + 500])
for kw in ["expected gradient similarity", "average gradient similarity", "expectation of", "average similarity", "mean gradient similarity", "𝔼"]:
    j = txt.find(kw)
    if j >= 0:
        print("==", kw, "::", txt[max(0, j - 250): j + 250])
