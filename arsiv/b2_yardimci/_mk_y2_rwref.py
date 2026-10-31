import io
yol = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/03_methodology.tex"
t = io.open(yol, encoding="utf-8").read()
degis = [
    ("known to depend on pre-training~\\cite{mo2022adversarial}.",
     "known to depend on pre-training~\\cite{mo2022adversarial} (Section~\\ref{subsec:rw_robustness})."),
    ("TGR~\\cite{zhang2023tgr} with momentum",
     "TGR~\\cite{zhang2023tgr} (Section~\\ref{subsec:rw_transfer}) with momentum"),
    ("Conditioning on correctly classified images is established practice~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, zhao2025revisiting},",
     "Conditioning on correctly classified images is established practice (Section~\\ref{subsec:rw_protocols}),"),
    ("is the quasi-symmetry model of Caussinus~\\cite{caussinus1965contribution} with",
     "is the quasi-symmetry model of Caussinus~\\cite{caussinus1965contribution} (Section~\\ref{subsec:rw_decomposition}) with"),
]
for a, b in degis:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
io.open(yol, "w", encoding="utf-8", newline="\n").write(t)
print("tamam")
