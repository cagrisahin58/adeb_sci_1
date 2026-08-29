#!/usr/bin/env python3
"""Sayfa kisaltma - dorduncu gecis: Tablo I'i tekrarlayan sekil kaldirilir.

fig1_robustness_comparison, Tablo I'in AYNI uc sutununu (temiz, PGD-10,
AutoAttack, eps=8/255) cubuk grafik olarak cizer. Metindeki tek anilma da
saf bir isaret cumlesidir ("visualizes this robustness gap"). Bir tabloyu
cizen sekil, hakemin ilk isaret ettigi fazlaliktir; sayilar tabloda kalir.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
p4 = ROOT / "04_experiments.tex"
t = p4.read_text(encoding="utf-8")

t2, n = re.subn(
    r"\\begin\{figure\}\[!t\]\s*\\centering\s*"
    r"\\includegraphics\[[^\]]*\]\{[^}]*fig1_robustness_comparison\.pdf\}\s*"
    r"\\caption\{.*?\}\s*\\label\{fig:robustness_comparison\}\s*\\end\{figure\}\s*",
    "", t, count=1, flags=re.DOTALL)
if n:
    p4.write_text(t2, encoding="utf-8")
    print("  [+] fig1_robustness_comparison sekil blogu kaldirildi")
elif "fig1_robustness_comparison" not in t:
    print("  [=] zaten yok")
else:
    sys.exit("BASARISIZ: sekil blogu desene uymadi")

YAMALAR = [
    ("04_experiments.tex",
     r"Figure~\ref{fig:robustness_comparison} visualizes this robustness gap "
     r"across architectures. To further understand the effect of perturbation "
     r"magnitude, Figure~\ref{fig:epsilon_sweep} shows PGD-10 robust accuracy "
     r"across perturbation budgets $\eps \in \{2/255, 4/255, 8/255, 16/255\}$ on "
     r"the full test set.",
     r"Figure~\ref{fig:epsilon_sweep} shows PGD-10 robust accuracy across "
     r"perturbation budgets $\eps \in \{2/255, 4/255, 8/255, 16/255\}$ on the full "
     r"test set.",
     "fig1 isaret cumlesi"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
