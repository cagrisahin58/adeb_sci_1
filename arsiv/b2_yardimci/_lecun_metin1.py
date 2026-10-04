"""LeCun paneli (2026-10-04) sonrasi metin duzeltmeleri, 1. parti (sekil/tablo kapsamindakiler), EN + TR.
- Sekil 4 (transfer isi haritasi) kaldirilir: Tablo 4'un Kos. sutununu ayni sayfada yineliyordu (mercek D Y6, hukum 7).
- 03:7 "hicbir saldiri yeniden kosulmadan" -> "her analizin icinde" (Tablo 4 ve Sekil 2 ayri kosulardan; mercek D Y2).
- 04:41 McNemar sinirlari: fo'ydeki maksimumlar 1,2e-84 ve 1,9e-120 -> "p < 2x10^-84", "p < 2x10^-120" (hukum M9).
- Tablo 3: iki "Diff." basligi ayristirilir, birim (pp) eklenir (mercek D 🟢6).
- Tablo 4 basligi: ayri saldiri kosusu beyani, Tablo 2/3 ile en cok 0,06 puan fark (mercek D Y2).
- Tablo 11 basligi: kisaltmalar acilir, eslesmis butce yazilir (mercek D 🟢10).
- Basliklarda matematik kipindeki binlik ayirici ({,}) Formata+CMMI7 karisimi veriyor -> metin kipi (mercek D 🟢13).
- main.tex: url paketi (p.22 URL tasmasi), \\vol{14} (2026 cildi), biyografi; references.bib: ilk ad baslangici kume icinde ("c. Sahin" -> "C. Sahin").
Her eski dize TAM BIR kez gecmeli. Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_lecun_metin1.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

PATCHES = [
    (ROOT / "paper/manuscript/sections/04_experiments.tex", [
        # Sekil 4 kaldir: cumle + ortam
        (
            "Figure~\\ref{fig:transfer_heatmap} shows the conditioned matrix. The third architecture also reframes",
            "The third architecture also reframes",
        ),
        (
            "\\begin{figure}[!t]\n\\centering\n\\includegraphics[width=\\columnwidth]{../figures/final/fig3_transfer_heatmap.pdf}\n",
            "% Sekil (isi haritasi) 2026-10-04'te kaldirildi: Tablo 4'un Kos. sutununu ayni sayfada\n"
            "% yineliyordu (hakem paneli, mercek D Y6). Betik ve PDF paper/figures altinda duruyor.\n"
            "\\iffalse\n\\begin{figure}[!t]\n\\centering\n\\includegraphics[width=\\columnwidth]{../figures/final/fig3_transfer_heatmap.pdf}\n",
        ),
        (
            "\\label{fig:transfer_heatmap}\n\\end{figure}\n",
            "\\label{fig:transfer_heatmap}\n\\end{figure}\n\\fi\n",
        ),
        # McNemar sinirlari
        (
            "($p < 10^{-84}$ under AutoAttack, $p < 10^{-120}$ under PGD-10)",
            "($p < 2\\times10^{-84}$ under AutoAttack, $p < 2\\times10^{-120}$ under PGD-10)",
        ),
        # (Tablo 3 basliklari _lecun_metin2.py'ye tasindi: besinci sutun kaldirildi)
        # Tablo 4 basligi: ayri kosu beyani
        (
            "Raw = unconditioned fooling rate, Cond. = target-correct conditioned rate. Diagonal entries are white-box attacks.}",
            "Raw = unconditioned fooling rate, Cond. = target-correct conditioned rate. Diagonal entries are white-box attacks. "
            "The attacks for this matrix were generated in a separate run (attack seed 42); the cells it shares with "
            "Tables~\\ref{tab:conditional} and~\\ref{tab:transfer_protocols} differ from them by at most $0.06$ points, "
            "within the attack-initialization variance of Section~\\ref{subsec:statistics_results}.}",
        ),
        # Tablo 11 basligi
        (
            "\\caption{ViT$\\rightarrow$CNN transfer under TGR~\\cite{zhang2023tgr} and plain MI-FGSM at a matched budget ($n$=10{,}000 per run; mean$\\pm$std over three runs).}",
            "\\caption{ViT$\\rightarrow$CNN transfer under Token Gradient Regularization (TGR)~\\cite{zhang2023tgr} and plain momentum iterative FGSM (MI-FGSM) at a matched budget ($L_\\infty$, $\\eps$=8/255, 10 steps, $\\alpha$=2/255; $n$=10,000 per run; mean$\\pm$std over three runs).}",
        ),
        # Basliklarda binlik ayirici
        (
            "The ViT$\\rightarrow$CNN sets nest in the same order ($N = 10{,}000$, $8{,}579$, $7{,}061$ and $3{,}814$);",
            "The ViT$\\rightarrow$CNN sets nest in the same order ($N$ = 10,000, 8,579, 7,061 and 3,814);",
        ),
        (
            "full test set $n$=26{,}032; mean$\\pm$std over two seed pairs;",
            "full test set $n$=26,032; mean$\\pm$std over two seed pairs;",
        ),
        (
            "AutoAttack-L2 uses a pre-registered $5{,}000$-sample subset,",
            "AutoAttack-L2 uses a pre-registered 5,000-sample subset,",
        ),
        (
            "the depth trend in attention displacement is reported quantitatively in the text over $n=1{,}000$ samples per run.}",
            "the depth trend in attention displacement is reported quantitatively in the text over $n$=1,000 samples per run.}",
        ),
        (
            "for clean and adversarial inputs, $n=1{,}000$ samples per run,",
            "for clean and adversarial inputs, $n$=1,000 samples per run,",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/04_deneyler.tex", [
        (
            "Koşullanmış matris Şekil~\\ref{fig:transfer_heatmap}'te verilmektedir. Üçüncü mimari, asimetrinin kendisini de yeniden çerçevelemektedir.",
            "Üçüncü mimari, asimetrinin kendisini de yeniden çerçevelemektedir.",
        ),
        (
            "\\begin{figure}[!t]\n\\centering\n\\includegraphics[width=\\columnwidth]{../figures/final_tr/fig3_transfer_heatmap.pdf}\n",
            "% Isi haritasi sekli 2026-10-04'te kaldirildi (EN ile ayni gerekce; hakem paneli mercek D Y6).\n"
            "\\iffalse\n\\begin{figure}[!t]\n\\centering\n\\includegraphics[width=\\columnwidth]{../figures/final_tr/fig3_transfer_heatmap.pdf}\n",
        ),
        (
            "\\label{fig:transfer_heatmap}\n\\end{figure}\n",
            "\\label{fig:transfer_heatmap}\n\\end{figure}\n\\fi\n",
        ),
        (
            "(AutoAttack altında $p < 10^{-84}$, PGD-10 altında $p < 10^{-120}$)",
            "(AutoAttack altında $p < 2\\times10^{-84}$, PGD-10 altında $p < 2\\times10^{-120}$)",
        ),
        (
            "Ham = koşulsuz yanıltma oranı, Koş. = hedef doğru koşullu oran. Köşegen girdileri beyaz kutu saldırılardır.}",
            "Ham = koşulsuz yanıltma oranı, Koş. = hedef doğru koşullu oran. Köşegen girdileri beyaz kutu saldırılardır. "
            "Bu matrisin saldırıları ayrı bir koşuda üretilmiştir (saldırı tohumu 42); Tablo~\\ref{tab:conditional} ve "
            "Tablo~\\ref{tab:transfer_protocols} ile paylaştığı hücreler onlardan en çok $0{,}06$ puan ayrılır; bu fark "
            "Bölüm~\\ref{subsec:statistics_results}'deki saldırı başlangıcı varyansının içindedir.}",
        ),
    ]),
    (ROOT / "paper/manuscript/sections/03_methodology.tex", [
        (
            "so that the four conditioning protocols of Section~\\ref{subsec:metrics} can be applied to the same records without re-running any attack.",
            "so that, within each analysis, the four conditioning protocols of Section~\\ref{subsec:metrics} can be applied to the same records without re-running the attack.",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/03_yontem.tex", [
        (
            "böylece Bölüm~\\ref{subsec:metrics}'teki dört koşullama protokolü hiçbir saldırı yeniden koşulmadan aynı kayıtlara uygulanabilmektedir.",
            "böylece her analizin içinde Bölüm~\\ref{subsec:metrics}'teki dört koşullama protokolü, saldırı yeniden koşulmadan aynı kayıtlara uygulanabilmektedir.",
        ),
    ]),
    (ROOT / "paper/manuscript/main.tex", [
        (
            "\\usepackage{booktabs}\n",
            "\\usepackage{booktabs}\n"
            "% 2026-10-04: kaynakcadaki URL (timm) sutun disina tasiyordu; url paketi kirilabilir URL verir.\n"
            "\\usepackage{url}\n",
        ),
        (
            "\\year{2026}\n",
            "\\year{2026}\n"
            "% Altbilgi cildi: sinif varsayilani 11 (2023). IEEE Access 2026 = cilt 14; uretim yine de doldurur.\n"
            "\\vol{14}\n",
        ),
    ]),
    (ROOT / "paper/manuscript/references.bib", [
        (
            "  author       = {\\c{S}ahin, \\c{C}a\\u{g}r{\\i} and Y{\\i}ld{\\i}r{\\i}m, \\\"{O}zal},",
            "  author       = {{\\c{S}}ahin, {\\c{C}}a{\\u{g}}r{\\i} and Y{\\i}ld{\\i}r{\\i}m, {\\\"{O}}zal},",
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
        print(f"\n{hata} yama uygulanamadi; hatali dosya(lar) yazilmadi.")
        sys.exit(1)
    print("\nMetin duzeltmeleri (1. parti) tamam.")


if __name__ == "__main__":
    main()
