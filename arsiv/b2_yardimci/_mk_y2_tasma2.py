import io
yol = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/03_methodology.tex"
t = io.open(yol, encoding="utf-8").read()
a = "\\label{tab:design}\n\\footnotesize\n\\setlength{\\tabcolsep}{3pt}"
assert t.count(a) == 1
t = t.replace(a, "\\label{tab:design}\n\\footnotesize\n\\setlength{\\tabcolsep}{2.4pt}")
sat = t.split("\n")
bas = [i for i, l in enumerate(sat) if l.startswith("Panel members come")][0]
son = [i for i, l in enumerate(sat) if l.startswith("On ImageNet the panel")][0]
assert "sloppypar" not in sat[bas - 1]
sat.insert(son + 1, "\\end{sloppypar}")
sat.insert(bas, "% Uzun RobustBench adlari (\\texttt) satir sonunda bolunemedigi icin.\n\\begin{sloppypar}")
io.open(yol, "w", encoding="utf-8", newline="\n").write("\n".join(sat))
print("tamam")
