"""Render denetimi (2026-10-04) sonrasi bicim duzeltmeleri, EN + TR.
1) Tablo 2: 'Earlier single run ...' coklu-sutun satiri tablo genisligini asiyordu (render'da kesik);
   iki satira bolunur (EN + TR).
2) Tablo 10: dikey cizgi (|) booktabs stiline aykiri ve diger tablolarla tutarsiz; kaldirilir,
   bloklar arasina bosluk + cmidrule (EN + TR).
3) Genel bakis sekli: yapay zeka cizimi PNG -> vektor TikZ PDF (paper/figures/overview), tam genislik.
4) Dikkat haritalari basligi: satir olcekleme notu (sekil betigi degisikligiyle uyumlu).
5) Baslik sayfasi: tek yazarin iki kurumu '12' yerine '1,2'.
6) Biyografi: 'Turkey' -> 'T\\"urkiye' (adres satirlariyla tutarli).
7) references.bib: rw2019timm 'Formerly hosted at ...' notu kaldirilir.
Her eski dize TAM BIR kez gecmeli. Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_render_duzeltmeleri.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

PATCHES = [
    (ROOT / "paper/manuscript/sections/04_experiments.tex", [
        (
            "\\multicolumn{5}{l}{\\textit{Earlier single run, validation split seen during clean pre-training ($n$=7{,}260)}} \\\\\n",
            "\\multicolumn{5}{l}{\\textit{Earlier single run ($n$=7{,}260); validation split}} \\\\\n"
            "\\multicolumn{5}{l}{\\textit{seen during clean pre-training}} \\\\\n",
        ),
        (
            "\\begin{tabular}{lccc|lc}\n",
            "\\begin{tabular}{lccc@{\\hspace{9pt}}lc}\n",
        ),
        (
            "\\multicolumn{4}{c|}{\\textbf{ViT-Tiny AT}} & \\multicolumn{2}{c}{\\textbf{ResNet-18 AT}} \\\\\n",
            "\\multicolumn{4}{c}{\\textbf{ViT-Tiny AT}} & \\multicolumn{2}{c}{\\textbf{ResNet-18 AT}} \\\\\n"
            "\\cmidrule(lr){1-4} \\cmidrule(lr){5-6}\n",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/04_deneyler.tex", [
        (
            "\\multicolumn{5}{l}{\\textit{Önceki tek koşu, doğrulama bölmesi temiz ön eğitimde görülmüş ($n$=7.260)}} \\\\\n",
            "\\multicolumn{5}{l}{\\textit{Önceki tek koşu ($n$=7.260); doğrulama bölmesi}} \\\\\n"
            "\\multicolumn{5}{l}{\\textit{temiz ön eğitimde görülmüş}} \\\\\n",
        ),
        (
            "\\begin{tabular}{lccc|lc}\n",
            "\\begin{tabular}{lccc@{\\hspace{9pt}}lc}\n",
        ),
        (
            "\\multicolumn{4}{c|}{\\textbf{ViT-Tiny AT}} & \\multicolumn{2}{c}{\\textbf{ResNet-18 AT}} \\\\\n",
            "\\multicolumn{4}{c}{\\textbf{ViT-Tiny AT}} & \\multicolumn{2}{c}{\\textbf{ResNet-18 AT}} \\\\\n"
            "\\cmidrule(lr){1-4} \\cmidrule(lr){5-6}\n",
        ),
    ]),
    (ROOT / "paper/manuscript/sections/03_methodology.tex", [
        (
            "% Genel bakis sekli (2026-09-29): bildirideki fig_b0_overview.png'nin aynisi.\n"
            "% Sayi tasimaz; okur protokol tartismasina girmeden once mimariyi ve olcum\n"
            "% hattini gorur. Kaynak PNG 1647 px genis: 14 cm'de ~295 dpi (IEEE 300\n"
            "% onerisinin sinirinda; vektor/daha yuksek cozunurluklu yeniden uretim\n"
            "% kullanici tarafinda, bkz. paper/bildiri/mimari_figur_promptu.md).\n"
            "\\begin{figure*}[!t]\n"
            "\\centering\n"
            "\\includegraphics[width=0.8\\textwidth]{../figures/final/fig_study_overview.png}\n",
            "% Genel bakis sekli (2026-10-04): vektor TikZ, kaynak paper/figures/overview/\n"
            "% fig_study_overview.tex (derleme: bash paper/figures/overview/derle.sh). Yapay\n"
            "% zeka cizimi PNG (2026-09-29) paper/figures/arsiv/ altinda. Sayi tasimaz; her\n"
            "% etiket Bolum III kurulum olgusu ya da Bolum IV olcum ailesi adidir.\n"
            "\\begin{figure*}[!t]\n"
            "\\centering\n"
            "\\includegraphics[width=\\textwidth]{../figures/final/fig_study_overview.pdf}\n",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/03_yontem.tex", [
        (
            "\\includegraphics[width=0.8\\textwidth]{../figures/final/fig_study_overview.png}\n",
            "\\includegraphics[width=\\textwidth]{../figures/final/fig_study_overview.pdf}\n",
        ),
    ]),
    (ROOT / "paper/manuscript/main.tex", [
        (
            "\\author{\\c{C}A\\u{G}RI \\c{S}AH\\.IN\\authorrefmark{1}\\authorrefmark{2},",
            "\\author{\\c{C}A\\u{G}RI \\c{S}AH\\.IN\\authorrefmark{1,2},",
        ),
        (
            "received the B.Sc.\\ degree in software engineering from F{\\i}rat University, Elaz{\\i}\\u{g}, Turkey.",
            "received the B.Sc.\\ degree in software engineering from F{\\i}rat University, Elaz{\\i}\\u{g}, T\\\"urkiye.",
        ),
        (
            "is with the Department of Software Engineering, F{\\i}rat University, Elaz{\\i}\\u{g}, Turkey.",
            "is with the Department of Software Engineering, F{\\i}rat University, Elaz{\\i}\\u{g}, T\\\"urkiye.",
        ),
    ]),
    (ROOT / "paper/manuscript/references.bib", [
        (
            "  doi          = {10.5281/zenodo.4414861},\n"
            "  note         = {Formerly hosted at github.com/rwightman/pytorch-image-models}\n",
            "  doi          = {10.5281/zenodo.4414861}\n",
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
    print("\nRender duzeltmeleri tamam.")


if __name__ == "__main__":
    main()
