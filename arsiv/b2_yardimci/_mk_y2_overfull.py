import re
log = open("/home/firat/projects/adeb_sci_1/paper/manuscript/main.log", encoding="latin-1").read()
# acik dosya yigini: '(' ile acilan ./sections/... dosyalari
cur = "main.tex"
for m in re.finditer(r"\(\./(sections/[^\s()]+\.tex)|Overfull \\hbox \(([\d.]+)pt too wide\) (in paragraph at lines \d+--\d+|in alignment at lines \d+--\d+|has occurred while \\output is active)", log):
    if m.group(1):
        cur = m.group(1)
    elif "output" not in m.group(3):
        print(cur, m.group(2), m.group(3))
print("output-aktif overfull sayisi:", len(re.findall(r"too wide\) has occurred while \\output is active", log)))
