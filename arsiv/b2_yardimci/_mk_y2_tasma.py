import io, re
yol = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/03_methodology.tex"
t = io.open(yol, encoding="utf-8").read()

# 1) Panel paragraflarinda \texttt{...} adlarina bolme noktasi
def kir(m):
    ic = m.group(1)
    if "allowbreak" in ic:
        return m.group(0)
    ic = ic.replace("\\_", "\\_\\allowbreak{}")
    ic = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", r"\\allowbreak{}", ic)
    ic = re.sub(r"(?<=[a-zA-Z])(?=[0-9]{4})", r"\\allowbreak{}", ic)
    return "\\texttt{" + ic + "}"

sat = t.split("\n")
n = 0
for i, l in enumerate(sat):
    if l.startswith(("Panel members come", "The CIFAR-100 panel is", "On ImageNet the panel")):
        sat[i] = re.sub(r"\\texttt\{([^{}]*)\}", kir, l)
        n += 1
t = "\n".join(sat)
assert n == 3, n

# 2) tab:design: tek sutuna sigacak bicim
eski_bas = t.index("\\caption{Cells of the design on CIFAR-10.")
eski_son = t.index("\\end{tabular}", eski_bas) + len("\\end{tabular}")
yeni = r"""\caption{Cells of the design on CIFAR-10. Inputs of 224 pixels are upsampled bilinearly from 32, and $^\ast$ marks in-model ImageNet normalization; the ImageNet-row clean phase uses AdamW with learning rate $10^{-4}$. All cells except the bridge R32 share one adversarial recipe (mixed loss, PGD-10, AdamW with weight decay 0.05, learning rate $10^{-3}$, batch 64, cosine schedule over 100 epochs, patience 20), and the three new cells stop at an 80-epoch cap.}
\label{tab:design}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}llllll@{}}
\toprule
\textbf{Cell} & \textbf{Model} & \textbf{Init.} & \textbf{Input} & \textbf{Clean phase} & \textbf{Seeds} \\
\midrule
R32 & ResNet-18, $3{\times}3$ & random & 32 & SGD, 200 ep & 1001--1003 \\
\cellname{V-scr} & ViT-Tiny & random & 224 & AdamW, 200 ep & 2001--2003 \\
\cellname{V-IN} & ViT-Tiny & DeiT-Ti & 224$^\ast$ & AdamW, 30 ep & 2101, 2102 \\
\cellname{R224-scr} & ResNet-18, $7{\times}7$ & random & 224 & as \cellname{V-scr} & 1201, 1202 \\
\cellname{R224-IN} & ResNet-18, $7{\times}7$ & RSB A1 & 224$^\ast$ & AdamW, 30 ep & 1301, 1302 \\
\bottomrule
\end{tabular}"""
t = t[:eski_bas] + yeni + t[eski_son:]
io.open(yol, "w", encoding="utf-8", newline="\n").write(t)
print("tamam")
