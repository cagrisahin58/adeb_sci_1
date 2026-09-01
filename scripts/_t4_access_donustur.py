#!/usr/bin/env python3
"""main.tex'i IEEEtran[journal]'dan IEEE Access sablonuna (ieeeaccess.cls) tasir.

IEEE Access kendi sablonunu ZORUNLU tutuyor (preparing-your-article sayfasi:
"The article must be submitted (i) using one of the following IEEE Access
templates..."). Onceki preamble'da da bu tasimanin ertelendigi yaziliydi.

Govde (\\begin{document} sonrasi) DEGISMEZ; yalnizca preamble ve yazar
blogu sablonun bekledigi bicime cevrilir:
  IEEEtran                         ieeeaccess
  \\author{...\\thanks{...}}   ->   \\author{\\uppercase{..}\\authorrefmark{n}..}
                                    + \\address[n]{..} + \\corresp{..}
  (yok)                        ->   \\history{} ve \\doi{}
  \\maketitle                   ->   \\titlepgskip=-21pt  \\maketitle
"""
import re
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/main.tex")
t = P.read_text(encoding="utf-8")

if "documentclass{ieeeaccess}" in t:
    print("zaten ieeeaccess sinifinda")
    sys.exit(0)

YENI_PREAMBLE = r"""\documentclass{ieeeaccess}

% ============================================================================
% PACKAGES
% ============================================================================
% NOT: ieeeaccess.cls cite/graphicx/amsmath'i kendisi yukler; yalnizca
% ek olarak ihtiyac duyduklarimiz burada.
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{textcomp}
\usepackage{booktabs}
\usepackage{subcaption}
\usepackage{hyperref}

% Custom commands
\newcommand{\eps}{\epsilon}
\newcommand{\Linf}{L_\infty}

% ============================================================================
% DOCUMENT INFO  (IEEE Access sablonu: history + doi + author/address/corresp)
% ============================================================================
\history{Submitted for review.}
\doi{10.1109/ACCESS.2026.0000000}

\title{The Measurement Protocol Decides the Conclusion: A Methodological Study
of CNN and Vision Transformer Adversarial Robustness Comparisons}

\author{\uppercase{\c{C}a\u{g}r{\i} \c{S}ahin}\authorrefmark{1}\authorrefmark{2},
\uppercase{and \"Ozal Y{\i}ld{\i}r{\i}m}\authorrefmark{2}}

\address[1]{Department of Software Engineering, Mu\c{s} Alparslan University,
49250 Mu\c{s}, T\"urkiye (e-mail: c.sahin@alparslan.edu.tr)}
\address[2]{Department of Software Engineering, F{\i}rat University,
23119 Elaz{\i}\u{g}, T\"urkiye (e-mail: ozalyildirim@firat.edu.tr)}

\corresp{Corresponding author: \c{C}a\u{g}r{\i} \c{S}ahin
(e-mail: c.sahin@alparslan.edu.tr).}

% ============================================================================
% DOCUMENT
% ============================================================================
\begin{document}

\titlepgskip=-21pt

\maketitle
"""

i = t.index(r"\maketitle")
govde = t[i + len(r"\maketitle"):]
yeni = YENI_PREAMBLE + govde

# \balance ieeeaccess ile gerekmiyor (sinif kendi dengelemesini yapar)
yeni = yeni.replace("\\balance\n", "")

P.write_text(yeni, encoding="utf-8")
print("main.tex ieeeaccess sinifina tasindi")
print("  \\balance kaldirildi (sinif kendi dengeliyor)")
n = len(re.findall(r"\\address\[", yeni))
c = "var" if "\\corresp{" in yeni else "YOK"
print(f"  {n} adres blogu · corresp: {c}")
