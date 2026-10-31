import io, re
# Y3: tablo dipnotlarini \multicolumn{N}{l}{...} -> sarilabilir p{} sutununa cevirir (yalniz 04_experiments.tex).
yol = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/04_experiments.tex"
t = io.open(yol, encoding="utf-8").read()
degis = {
    r"\multicolumn{9}{l}{\scriptsize $^\dagger$Robust": r"\multicolumn{9}{p{0.96\textwidth}}{\scriptsize $^\dagger$Robust",
    r"\multicolumn{7}{l}{\scriptsize Image-bootstrap": r"\multicolumn{7}{p{0.96\textwidth}}{\scriptsize Image-bootstrap",
    r"\multicolumn{7}{l}{\scriptsize Over all $56$": r"\multicolumn{7}{p{0.95\columnwidth}}{\scriptsize Over all $56$",
    r"\multicolumn{11}{l}{\scriptsize Hierarchical-bootstrap": r"\multicolumn{11}{p{0.96\textwidth}}{\scriptsize Hierarchical-bootstrap",
}
for a, b in degis.items():
    n = t.count(a)
    assert n == 1, (a, n)
    t = t.replace(a, b)
io.open(yol, "w", encoding="utf-8", newline="\n").write(t)
print("tamam", len(degis))
