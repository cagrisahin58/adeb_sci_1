import io
yol = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/03_methodology.tex"
t = io.open(yol, encoding="utf-8").read()
a = "so its results bound this adaptation and not the published scheme."
b = "so its results speak for this adaptation only."
assert t.count(a) == 1
t = t.replace(a, b)
io.open(yol, "w", encoding="utf-8", newline="\n").write(t)
print("tamam")
