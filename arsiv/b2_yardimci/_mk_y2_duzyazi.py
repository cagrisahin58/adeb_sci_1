import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n"))
toplam = len(t.split())
# ortamlar
env = re.compile(r"\\begin\{(equation\*?|align\*?|table\*?|tabular)\}.*?\\end\{\1\}", re.S)
ortam = sum(len(m.group(0).split()) for m in env.finditer(t))
t2 = env.sub(" ", t)
# satir ici matematik
im = re.findall(r"\$[^$]*\$", t2)
imn = sum(len(x.split()) for x in im)
t3 = re.sub(r"\$[^$]*\$", "M", t2)
print("toplam", toplam, "| denklem+tablo ortamlari", ortam, "| satir ici matematik", imn, "| duzyazi (matematik tek kelime)", len(t3.split()))
