#!/usr/bin/env python3
"""Sayfa kisaltma - ikinci gecis.

1) t-SNE SEKLI kaldirilir. Gerekce makalenin kendi basliginda: "t-SNE is
   shown for orientation only; the quantitative comparison is given in the
   text." Okunmamasi gerektigi soylenen bir sekil, sayfa maliyeti olan bir
   sekildir. SAYILAR metinde KALIR.
2) Oran paragraflari sikistirilir (iddia degismez).
3) Ozdeslik paragrafindaki revizyon-tarihi notu kisaltilir.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")

# --- 1) t-SNE sekil blogunu tamamen kaldir ---
p4 = ROOT / "04_experiments.tex"
t = p4.read_text(encoding="utf-8")
onceki = len(t)
t, n = re.subn(
    r"\\begin\{figure\}\[!t\]\s*\\centering\s*"
    r"\\includegraphics\[[^\]]*\]\{[^}]*fig_tsne_features\.pdf\}\s*"
    r"\\caption\{.*?\}\s*\\label\{fig:tsne_features\}\s*\\end\{figure\}\s*",
    "", t, count=1, flags=re.DOTALL)
if n:
    p4.write_text(t, encoding="utf-8")
    print(f"  [+] t-SNE sekil blogu kaldirildi ({onceki - len(t)} karakter)")
elif "fig_tsne_features" not in t:
    print("  [=] t-SNE sekli zaten yok")
else:
    sys.exit("BASARISIZ: t-SNE sekil blogu desene uymadi")

YAMALAR = [
    # --- t-SNE paragrafi: sekle gonderme kalkar, sayilar kalir ---
    ("04_experiments.tex",
     r"Figure~\ref{fig:tsne_features} shows an illustrative t-SNE embedding of "
     r"the penultimate feature spaces. Because t-SNE embeddings are sensitive to "
     r"hyperparameters and invite qualitative over-reading, we base all claims on "
     r"metrics computed in the original feature space ($n$=500 per run, each "
     r"model attacked white-box, mean$\pm$std over three runs). The attack "
     r"collapses class structure most strongly in the \emph{CNN}: clean-fit 5-NN "
     r"label consistency drops from $87.3\pm2.6\%$ to $51.3\pm1.8\%$, the "
     r"silhouette score falls from $0.196\pm0.010$ to $-0.032\pm0.004$, the "
     r"intra/inter-class distance ratio rises from $0.511\pm0.013$ to "
     r"$0.847\pm0.003$, and the relative class-centroid shift is $0.238\pm0.012$. "
     r"The ViT's penultimate space is only weakly class-separated even on clean "
     r"inputs (silhouette $-0.021\pm0.005$; 5-NN consistency $61.1\pm1.4\%$, "
     r"dropping to $48.5\pm1.4\%$), and its centroids shift far less "
     r"($0.083\pm0.004$).",

     r"Penultimate-space geometry is measured in the original feature space, not "
     r"from a low-dimensional embedding, because embeddings of this kind invite "
     r"qualitative over-reading ($n$=500 per run, each model attacked white-box, "
     r"mean$\pm$std over three runs). The attack collapses class structure most "
     r"strongly in the \emph{CNN}: clean-fit 5-NN label consistency drops from "
     r"$87.3\pm2.6\%$ to $51.3\pm1.8\%$, the silhouette score from $0.196\pm0.010$ "
     r"to $-0.032\pm0.004$, and the relative class-centroid shift is "
     r"$0.238\pm0.012$ against $0.083\pm0.004$ for the ViT, whose space is weakly "
     r"class-separated even on clean inputs (silhouette $-0.021\pm0.005$; 5-NN "
     r"consistency $61.1\pm1.4\%$, dropping to $48.5\pm1.4\%$).",
     "t-SNE paragrafi"),

    # --- oran paragrafi 1 ---
    ("04_experiments.tex",
     r"This figure is the mean of the per-seed ranges, and here it coincides with "
     r"the range of the protocol means because the extremal protocols are the "
     r"same in all three seeds, successful-source above and target-correct below; "
     r"on CIFAR-100 the two figures differ ($13.83$ against $13.58$) because there "
     r"the extremal protocol does change between seeds.",
     r"This figure is the mean of the per-seed ranges; it coincides with the range "
     r"of the protocol means here because the extremal protocols are the same in "
     r"all three seeds, and differs on CIFAR-100 ($13.83$ against $13.58$) because "
     r"there they are not.",
     "oran paragrafi 1"),

    # --- oran paragrafi 2 ---
    ("04_experiments.tex",
     r"With three runs the denominator carries two degrees of freedom, so a "
     r"$\chi^2$ interval on any single ratio is very wide: for the "
     r"successful-source protocol, whose run-to-run standard deviation is the "
     r"largest of the four, the $95\%$ interval on the ratio runs from $0.8$ to "
     r"$9.9$ and therefore includes unity. Reported as a sensitivity rather than "
     r"an estimate, the ratio spans $5.2$ to $32.6$ across dispersion measures and "
     r"reference protocols, and equals $28.3$ under the like-for-like "
     r"standard-deviation comparison on the both-correct protocol that we treat as "
     r"primary. Two cautions bound it further. The protocol with the largest "
     r"asymmetry also carries the largest run-to-run standard deviation, so "
     r"numerator and denominator are not independent. And because all three runs "
     r"share the single validation split drawn before any training, this standard "
     r"deviation excludes split-to-split variance, which makes the ratio an upper "
     r"bound. The absolute comparison survives the width of that interval and both "
     r"cautions, which is why it, and not the fold-change, carries the claim.",

     r"With three runs the denominator carries two degrees of freedom, so a "
     r"$\chi^2$ interval on any single ratio is very wide: for the "
     r"successful-source protocol it runs from $0.8$ to $9.9$ and includes unity. "
     r"Reported as a sensitivity, the ratio spans $5.2$ to $32.6$ across dispersion "
     r"measures and reference protocols, and equals $28.3$ under the like-for-like "
     r"comparison on the both-correct protocol we treat as primary. Two cautions "
     r"bound it further: the protocol with the largest asymmetry also carries the "
     r"largest run-to-run standard deviation, so numerator and denominator are not "
     r"independent, and because all three runs share one validation split the "
     r"denominator excludes split-to-split variance, which makes the ratio an "
     r"upper bound. The absolute comparison survives both, which is why it and not "
     r"the fold-change carries the claim.",
     "oran paragrafi 2"),

    # --- ozdeslik: revizyon-tarihi notu ---
    ("04_experiments.tex",
     r"We previously stated this result as a Pearson correlation ($r = 0.997$ over "
     r"six directions drawn from three targets) and that phrasing understated it: "
     r"a near-unit correlation between a quantity and its own dominant component "
     r"is arithmetic, and the small-sample caveat it required is unnecessary once "
     r"the identity is written down.",
     r"We previously reported this as a Pearson correlation ($r = 0.997$), which "
     r"understated it: a near-unit correlation between a quantity and its own "
     r"dominant component is arithmetic, and the small-sample caveat it required "
     r"is unnecessary once the identity is written down.",
     "ozdeslik revizyon notu"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
