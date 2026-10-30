import re, html, subprocess
p = "/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis/zhang_html.html"
subprocess.run(["curl", "-sL", "https://arxiv.org/html/2307.07873", "-o", p])
t = open(p, encoding="utf-8", errors="replace").read()
txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
print(len(txt))
for m in re.finditer(r"Definition\s*2", txt):
    print("---", txt[m.start(): m.start() + 700])
    break
