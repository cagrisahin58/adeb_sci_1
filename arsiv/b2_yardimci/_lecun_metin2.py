"""LeCun paneli (2026-10-04), 2. parti: Tablo 3 sutun tasmasi.
Besinci sutun (onceki tek kosu farklari) tabloyu 3,5 in sutunun disina tasiriyordu (render: +5..+16 pt).
Sutun kaldirilir, dort degeri dipnot satirina tasinir; sayilar degismez. EN + TR.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_lecun_metin2.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

PATCHES = [
    (ROOT / "paper/manuscript/sections/04_experiments.tex", [
        (
            "\\begin{tabular}{lcccc}\n\\toprule\n\\textbf{Protocol} & \\textbf{CNN$\\rightarrow$ViT} & \\textbf{ViT$\\rightarrow$CNN} & \\textbf{Diff.\\ (pp)} & \\textbf{Earlier run}$^{\\ddagger}$ \\\\\n\\midrule\n"
            "Unconditioned (raw) & 41.02$\\pm$0.55 & 27.45$\\pm$0.27 & $+$13.57$\\pm$0.33 & $+$8.27 \\\\\n"
            "Target-correct & 19.87$\\pm$0.18 & 15.51$\\pm$0.59 & $+$4.36$\\pm$0.44 & $+$0.63 \\\\\n"
            "Both-correct & 18.25$\\pm$0.17 & 9.98$\\pm$0.31 & $+$8.27$\\pm$0.23 & $+$5.33 \\\\\n"
            "Successful-source & 36.39$\\pm$0.76 & 17.02$\\pm$0.52 & $+$19.37$\\pm$1.27 & $+$11.17 \\\\\n"
            "\\bottomrule\n"
            "\\multicolumn{5}{l}{\\scriptsize $^{\\ddagger}$Diff.\\ (pp) on a single earlier run whose validation split was seen during clean pre-training.}\n",
            "\\begin{tabular}{lccc}\n\\toprule\n\\textbf{Protocol} & \\textbf{CNN$\\rightarrow$ViT} & \\textbf{ViT$\\rightarrow$CNN} & \\textbf{Diff.\\ (pp)}$^{\\ddagger}$ \\\\\n\\midrule\n"
            "Unconditioned (raw) & 41.02$\\pm$0.55 & 27.45$\\pm$0.27 & $+$13.57$\\pm$0.33 \\\\\n"
            "Target-correct & 19.87$\\pm$0.18 & 15.51$\\pm$0.59 & $+$4.36$\\pm$0.44 \\\\\n"
            "Both-correct & 18.25$\\pm$0.17 & 9.98$\\pm$0.31 & $+$8.27$\\pm$0.23 \\\\\n"
            "Successful-source & 36.39$\\pm$0.76 & 17.02$\\pm$0.52 & $+$19.37$\\pm$1.27 \\\\\n"
            "\\bottomrule\n"
            "\\multicolumn{4}{l}{\\scriptsize $^{\\ddagger}$On a single earlier run whose validation split was seen during}\\\\\n"
            "\\multicolumn{4}{l}{\\scriptsize \\phantom{$^{\\ddagger}$}clean pre-training the same differences were $+$8.27, $+$0.63,}\\\\\n"
            "\\multicolumn{4}{l}{\\scriptsize \\phantom{$^{\\ddagger}$}$+$5.33 and $+$11.17 (top to bottom).}\n",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/04_deneyler.tex", [
        (
            "\\begin{tabular}{lcccc}\n\\toprule\n\\textbf{Protokol} & \\textbf{CNN$\\rightarrow$ViT} & \\textbf{ViT$\\rightarrow$CNN} & \\textbf{Fark} & \\textbf{Fark}$^{\\ddagger}$ \\\\\n\\midrule\n"
            "Koşulsuz (ham) & 41,02$\\pm$0,55 & 27,45$\\pm$0,27 & $+$13,57$\\pm$0,33 & $+$8,27 \\\\\n"
            "Hedef doğru & 19,87$\\pm$0,18 & 15,51$\\pm$0,59 & $+$4,36$\\pm$0,44 & $+$0,63 \\\\\n"
            "Her ikisi doğru & 18,25$\\pm$0,17 & 9,98$\\pm$0,31 & $+$8,27$\\pm$0,23 & $+$5,33 \\\\\n"
            "Başarılı kaynak & 36,39$\\pm$0,76 & 17,02$\\pm$0,52 & $+$19,37$\\pm$1,27 & $+$11,17 \\\\\n"
            "\\bottomrule\n",
            "\\begin{tabular}{lccc}\n\\toprule\n\\textbf{Protokol} & \\textbf{CNN$\\rightarrow$ViT} & \\textbf{ViT$\\rightarrow$CNN} & \\textbf{Fark (puan)}$^{\\ddagger}$ \\\\\n\\midrule\n"
            "Koşulsuz (ham) & 41,02$\\pm$0,55 & 27,45$\\pm$0,27 & $+$13,57$\\pm$0,33 \\\\\n"
            "Hedef doğru & 19,87$\\pm$0,18 & 15,51$\\pm$0,59 & $+$4,36$\\pm$0,44 \\\\\n"
            "Her ikisi doğru & 18,25$\\pm$0,17 & 9,98$\\pm$0,31 & $+$8,27$\\pm$0,23 \\\\\n"
            "Başarılı kaynak & 36,39$\\pm$0,76 & 17,02$\\pm$0,52 & $+$19,37$\\pm$1,27 \\\\\n"
            "\\bottomrule\n",
        ),
        (
            "\\multicolumn{5}{l}{\\scriptsize $^{\\ddagger}$Tek koşu; doğrulama bölmesi temiz ön eğitimde görülmüş.}\n",
            "\\multicolumn{4}{l}{\\scriptsize $^{\\ddagger}$Doğrulama bölmesi temiz ön eğitimde görülmüş önceki tek koşuda}\\\\\n"
            "\\multicolumn{4}{l}{\\scriptsize \\phantom{$^{\\ddagger}$}aynı farklar yukarıdan aşağıya $+$8,27, $+$0,63, $+$5,33 ve}\\\\\n"
            "\\multicolumn{4}{l}{\\scriptsize \\phantom{$^{\\ddagger}$}$+$11,17 idi.}\n",
        ),
    ]),
]


def main():
    hata = 0
    for path, pairs in PATCHES:
        text = io.open(path, encoding="utf-8").read()
        new_text = text
        for i, (old, new) in enumerate(pairs, 1):
            n_old = new_text.count(old)
            if n_old == 1:
                new_text = new_text.replace(old, new)
                print(f"OK    {path.name} #{i}")
            elif n_old == 0 and new_text.count(new) == 1:
                print(f"ZATEN {path.name} #{i}")
            else:
                print(f"HATA  {path.name} #{i}: eski dize {n_old} kez gecti")
                hata += 1
        if new_text != text and not hata:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    if hata:
        print(f"\n{hata} yama uygulanamadi.")
        sys.exit(1)
    print("\nTablo 3 yamasi tamam.")


if __name__ == "__main__":
    main()
