"""LeCun paneli (2026-10-04), 3. parti: tablolar. EN + TR.
1. Sekil 4 (isi haritasi) icin birakilan \\iffalse ... \\fi bloklari tamamen silinir.
2. Tablo 6 (SVHN) yerine protokol x ayar table* (tab:protocol_settings): CIFAR-10 Linf, CIFAR-100, SVHN (iki
   cift ayri ayri), CIFAR-10 L2. Kaynak: results/C1_REFERANS_FOYU.md 'Transfer asimetrisi, dort protokol, ayarlar'.
   tab:svhn_protocols ve 04:280'deki yanlis tab:l2_results gondermeleri yeni tabloya cevrilir; Tablo 7'ye
   mutlak L2 cumlesinden gonderme eklenir.
3. Tablo 8: tekduze dort ondalik, kesir satiri yuzde yerine oran, native sutun dort ondalik, isaretli hizalanma
   uc kosum ortalamasi±SD (foy 'Tablo 8 ek sutunlari'); basliga kalin kurali.
4. Tablo 9: Fark sutununa kosumlar arasi SD, 'p (Holm)' basligi (foy 'Tablo 9 ek sutunlari'); scriptsize.
5. Tablo 10: ResNet satir adlari kod adi yerine 'asama.blok'; basliga kosumlar arasi SD cumlesi (foy 'Tablo 10').
6. 04:314 isaretli kosinus siniri 'her kosumda' nitelemesi.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_lecun_metin3.py
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
EN = ROOT / "paper/manuscript/sections/04_experiments.tex"
TR = ROOT / "paper/manuscript_tr/sections/04_deneyler.tex"

HATA = []


def once(text, old, new, tag):
    n = text.count(old)
    if n == 1:
        print(f"OK    {tag}")
        return text.replace(old, new)
    if n == 0 and new in text:
        print(f"ZATEN {tag}")
        return text
    HATA.append(f"{tag}: eski dize {n} kez")
    return text


def regex_once(text, pattern, repl, tag, flags=re.S):
    m = list(re.finditer(pattern, text, flags))
    if len(m) == 1:
        print(f"OK    {tag}")
        return text[: m[0].start()] + repl + text[m[0].end():]
    if len(m) == 0 and (repl.strip()[:40] in text if repl.strip() else True):
        print(f"ZATEN {tag}")
        return text
    HATA.append(f"{tag}: desen {len(m)} kez")
    return text


def caption_append(text, label, sentence, tag):
    """\\label{label} oncesindeki \\caption{...} icine, kapanis parantezinden once cumle ekler."""
    li = text.find("\\label{" + label + "}")
    if li < 0:
        HATA.append(f"{tag}: etiket yok")
        return text
    ci = text.rfind("\\caption{", 0, li)
    if ci < 0:
        HATA.append(f"{tag}: caption yok")
        return text
    depth, i = 0, ci + len("\\caption")
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    if sentence in text[ci:i]:
        print(f"ZATEN {tag}")
        return text
    print(f"OK    {tag}")
    return text[:i] + " " + sentence + text[i:]


TABLE_EN = r"""\begin{table*}[!t]
\centering
\caption{Transfer asymmetry (CNN$\rightarrow$ViT minus ViT$\rightarrow$CNN, percentage points) under the four conditioning protocols in every setting of this paper (PGD-10; $\eps$=8/255 under $L_\infty$, $\eps$=0.5 under $L_2$; full test sets). Settings with three seed pairs give the mean$\pm$std across pairs; SVHN has two pairs, so both values are printed instead of a standard deviation. Spread is the per-pair range over the four protocols, averaged over pairs. The two endorsed protocols, target-correct and both-correct, agree in sign within every setting; the sign changes across protocols only on SVHN, where all four estimates lie within three points of zero.}
\label{tab:protocol_settings}
\footnotesize
\begin{tabular}{lcccc}
\toprule
\textbf{Protocol} & \textbf{CIFAR-10, $L_\infty$} & \textbf{CIFAR-100, $L_\infty$} & \textbf{SVHN, $L_\infty$} & \textbf{CIFAR-10, $L_2$} \\
 & 3 pairs, $n$=10,000 & 3 pairs, $n$=10,000 & 2 pairs, $n$=26,032 & 3 pairs, $n$=10,000 \\
\midrule
Unconditioned (raw) & $+$13.57$\pm$0.33 & $+$18.53$\pm$0.71 & $+$0.33 / $+$0.45 & $+$13.03$\pm$0.81 \\
Target-correct & $+$4.36$\pm$0.44 & $+$4.96$\pm$1.01 & $-$1.16 / $-$0.85 & $+$2.12$\pm$0.18 \\
Both-correct & $+$8.27$\pm$0.23 & $+$10.92$\pm$0.34 & $-$0.34 / $-$0.36 & $+$4.07$\pm$0.36 \\
Successful-source & $+$19.37$\pm$1.27 & $+$17.50$\pm$0.92 & $+$2.98 / $+$2.41 & $+$12.06$\pm$0.23 \\
\midrule
Spread (max $-$ min) & 15.01$\pm$0.84 & 13.83$\pm$1.30 & 4.14 / 3.26 & 10.92$\pm$0.82 \\
\bottomrule
\end{tabular}
\end{table*}
"""

TABLE_TR = r"""\begin{table*}[!t]
\centering
\caption{Bu makaledeki her ayarda dört koşullama protokolü altında transfer asimetrisi (CNN$\rightarrow$ViT eksi ViT$\rightarrow$CNN, yüzde puan; PGD-10; $L_\infty$ altında $\eps$=8/255, $L_2$ altında $\eps$=0{,}5; tam test kümeleri). Üç tohum çiftli ayarlarda çiftler üzerinden ortalama$\pm$std verilir; SVHN'de iki çift olduğundan standart sapma yerine iki değer ayrı ayrı basılır. Yayılım, çift başına dört protokol üzerindeki açıklığın çiftler üzerinden ortalamasıdır. Onaylanan iki protokol, hedef doğru ve her ikisi doğru, her ayarın içinde aynı işareti verir; protokoller arasında işaret yalnız SVHN'de değişir ve orada dört kestirimin tamamı sıfırın üç puan yakınındadır.}
\label{tab:protocol_settings}
\footnotesize
\begin{tabular}{lcccc}
\toprule
\textbf{Protokol} & \textbf{CIFAR-10, $L_\infty$} & \textbf{CIFAR-100, $L_\infty$} & \textbf{SVHN, $L_\infty$} & \textbf{CIFAR-10, $L_2$} \\
 & 3 çift, $n$=10.000 & 3 çift, $n$=10.000 & 2 çift, $n$=26.032 & 3 çift, $n$=10.000 \\
\midrule
Koşulsuz (ham) & $+$13,57$\pm$0,33 & $+$18,53$\pm$0,71 & $+$0,33 / $+$0,45 & $+$13,03$\pm$0,81 \\
Hedef doğru & $+$4,36$\pm$0,44 & $+$4,96$\pm$1,01 & $-$1,16 / $-$0,85 & $+$2,12$\pm$0,18 \\
Her ikisi doğru & $+$8,27$\pm$0,23 & $+$10,92$\pm$0,34 & $-$0,34 / $-$0,36 & $+$4,07$\pm$0,36 \\
Başarılı kaynak & $+$19,37$\pm$1,27 & $+$17,50$\pm$0,92 & $+$2,98 / $+$2,41 & $+$12,06$\pm$0,23 \\
\midrule
Yayılım (en büyük $-$ en küçük) & 15,01$\pm$0,84 & 13,83$\pm$1,30 & 4,14 / 3,26 & 10,92$\pm$0,82 \\
\bottomrule
\end{tabular}
\end{table*}
"""


def main():
    en = io.open(EN, encoding="utf-8").read()
    tr = io.open(TR, encoding="utf-8").read()

    # 1. iffalse bloklari
    en = regex_once(en, r"% Sekil \(isi haritasi\) 2026-10-04'te kaldirildi.*?\\iffalse\n.*?\\fi\n",
                    "% Isi haritasi sekli (fig3_transfer_heatmap) 2026-10-04'te kaldirildi: Tablo 4'un Kos.\n"
                    "% sutununu ayni sayfada yineliyordu (hakem paneli, mercek D Y6). Betik ve PDF duruyor.\n",
                    "EN iffalse sil")
    tr = regex_once(tr, r"% Isi haritasi sekli 2026-10-04'te kaldirildi.*?\\iffalse\n.*?\\fi\n",
                    "% Isi haritasi sekli 2026-10-04'te kaldirildi (EN ile ayni gerekce; hakem paneli mercek D Y6).\n",
                    "TR iffalse sil")

    # 2. Tablo 6 -> protokol x ayar table*
    en = regex_once(en, r"\\begin\{table\}\[!t\]\n\\centering\n\\caption\{SVHN transfer asymmetry.*?\\end\{table\}\n",
                    TABLE_EN, "EN Tablo 6 -> table*")
    tr = regex_once(tr, r"\\begin\{table\}\[!t\]\n\\centering\n\\caption\{SVHN'de dört protokol.*?\\end\{table\}\n",
                    TABLE_TR, "TR Tablo 6 -> table*")
    en = once(en, "(Table~\\ref{tab:svhn_protocols})", "(Table~\\ref{tab:protocol_settings})", "EN ref svhn")
    tr = once(tr, "(Tablo~\\ref{tab:svhn_protocols})", "(Tablo~\\ref{tab:protocol_settings})", "TR ref svhn")
    en = once(en, "The four protocols (Table~\\ref{tab:l2_results}) report asymmetries of",
              "The four protocols (Table~\\ref{tab:protocol_settings}) report asymmetries of", "EN ref l2 -> settings")
    tr = once(tr, "Dört protokolün (Tablo~\\ref{tab:l2_results}) bildirdiği asimetriler",
              "Dört protokolün (Tablo~\\ref{tab:protocol_settings}) bildirdiği asimetriler", "TR ref l2 -> settings")
    en = once(en, "Absolute robustness keeps the CNN-over-ViT ordering under both attacks,",
              "Absolute robustness (Table~\\ref{tab:l2_results}) keeps the CNN-over-ViT ordering under both attacks,",
              "EN Tablo 7 gondermesi")
    # TR: 10^{-57} iceren cumlenin sonuna Tablo 7 gondermesi
    k = tr.find("10^{-57}")
    if k < 0:
        HATA.append("TR 10^-57 cumlesi yok")
    else:
        dot = tr.find(".", k)
        ins = " (Tablo~\\ref{tab:l2_results})"
        if "tab:l2_results" in tr[k - 400:dot]:
            print("ZATEN TR Tablo 7 gondermesi")
        else:
            tr = tr[:dot] + ins + tr[dot:]
            print("OK    TR Tablo 7 gondermesi")

    # 3. Tablo 8
    en = once(en,
              "Hoyer sparsity & \\textbf{0.4928}$\\pm$0.0120 & 0.4561$\\pm$0.0055 & 0.405 \\\\\n"
              "Gini coefficient & \\textbf{0.6498}$\\pm$0.0089 & 0.6099$\\pm$0.0051 & 0.571 \\\\\n"
              "Frac.\\ $<$1\\% of max & \\textbf{34.8\\%}$\\pm$2.1 & 26.8\\%$\\pm$0.9 & 17.9\\% \\\\\n"
              "Alignment (absolute) & 0.0378$\\pm$0.0009 & \\textbf{0.0562}$\\pm$0.0004 & 0.079 \\\\\n"
              "Alignment (signed) & 0.0014 & 0.0005 & -- \\\\\n",
              "Hoyer sparsity & \\textbf{0.4928}$\\pm$0.0120 & 0.4561$\\pm$0.0055 & 0.4046 \\\\\n"
              "Gini coefficient & \\textbf{0.6498}$\\pm$0.0089 & 0.6099$\\pm$0.0051 & 0.5712 \\\\\n"
              "Fraction $<$1\\% of max & \\textbf{0.3477}$\\pm$0.0210 & 0.2682$\\pm$0.0090 & 0.1785 \\\\\n"
              "Alignment (absolute) & 0.0378$\\pm$0.0009 & \\textbf{0.0562}$\\pm$0.0004 & 0.0794 \\\\\n"
              "Alignment (signed) & 0.0010$\\pm$0.0003 & 0.0004$\\pm$0.0001 & -- \\\\\n",
              "EN Tablo 8 satirlari")
    tr = once(tr,
              "Hoyer seyrekliği & \\textbf{0,4928}$\\pm$0,0120 & 0,4561$\\pm$0,0055 & 0,405 \\\\\n"
              "Gini katsayısı & \\textbf{0,6498}$\\pm$0,0089 & 0,6099$\\pm$0,0051 & 0,571 \\\\\n"
              "Maks.\\ \\%1 altı kesir & \\textbf{\\%34,8}$\\pm$2,1 & \\%26,8$\\pm$0,9 & \\%17,9 \\\\\n"
              "Hizalanma (mutlak) & 0,0378$\\pm$0,0009 & \\textbf{0,0562}$\\pm$0,0004 & 0,079 \\\\\n"
              "Hizalanma (işaretli) & 0,0014 & 0,0005 & -- \\\\\n",
              "Hoyer seyrekliği & \\textbf{0,4928}$\\pm$0,0120 & 0,4561$\\pm$0,0055 & 0,4046 \\\\\n"
              "Gini katsayısı & \\textbf{0,6498}$\\pm$0,0089 & 0,6099$\\pm$0,0051 & 0,5712 \\\\\n"
              "Maks.\\ \\%1 altı kesir & \\textbf{0,3477}$\\pm$0,0210 & 0,2682$\\pm$0,0090 & 0,1785 \\\\\n"
              "Hizalanma (mutlak) & 0,0378$\\pm$0,0009 & \\textbf{0,0562}$\\pm$0,0004 & 0,0794 \\\\\n"
              "Hizalanma (işaretli) & 0,0010$\\pm$0,0003 & 0,0004$\\pm$0,0001 & -- \\\\\n",
              "TR Tablo 8 satirlari")
    en = caption_append(en, "tab:gradient",
                        "Bold marks the larger of the two adversarially trained models; the native control is a single checkpoint, so no standard deviation applies.",
                        "EN Tablo 8 baslik")
    tr = caption_append(tr, "tab:gradient",
                        "Kalın, çekişmeli eğitilmiş iki modelden büyük olanı gösterir; yerel kontrol tek kontrol noktasıdır, standart sapma uygulanmaz.",
                        "TR Tablo 8 baslik")

    # 4. Tablo 9
    en = once(en,
              "\\textbf{Measure} & \\textbf{ResNet-18} & \\textbf{ViT-Tiny} & \\textbf{Diff.} & \\textbf{$p$} \\\\\n\\midrule\n"
              "Area for 50\\% energy & 0.0378$\\pm$0.0017 & 0.0397$\\pm$0.0010 & $-$0.0019 & 0.54 \\\\\n"
              "Area for 90\\% energy & 0.2345$\\pm$0.0078 & 0.2570$\\pm$0.0067 & $-$0.0224 & 0.40 \\\\\n"
              "Spatial entropy (nat) & 5.2014$\\pm$0.0387 & 5.2524$\\pm$0.0197 & $-$0.0509 & 0.54 \\\\\n"
              "Moran's $I$ & 0.4141$\\pm$0.0132 & 0.3941$\\pm$0.0024 & $+$0.0200 & 0.47 \\\\\n",
              "\\textbf{Measure} & \\textbf{ResNet-18} & \\textbf{ViT-Tiny} & \\textbf{Diff.\\ (R$-$V)} & \\textbf{$p$ (Holm)} \\\\\n\\midrule\n"
              "Area for 50\\% energy & 0.0378$\\pm$0.0017 & 0.0397$\\pm$0.0010 & $-$0.0019$\\pm$0.0027 & 0.54 \\\\\n"
              "Area for 90\\% energy & 0.2345$\\pm$0.0078 & 0.2570$\\pm$0.0067 & $-$0.0224$\\pm$0.0133 & 0.40 \\\\\n"
              "Spatial entropy (nat) & 5.2014$\\pm$0.0387 & 5.2524$\\pm$0.0197 & $-$0.0509$\\pm$0.0580 & 0.54 \\\\\n"
              "Moran's $I$ & 0.4141$\\pm$0.0132 & 0.3941$\\pm$0.0024 & $+$0.0200$\\pm$0.0156 & 0.47 \\\\\n",
              "EN Tablo 9 satirlari")
    tr = once(tr,
              "\\textbf{Ölçüt} & \\textbf{ResNet-18} & \\textbf{ViT-Tiny} & \\textbf{Fark} & \\textbf{$p$} \\\\\n\\midrule\n"
              "\\%50 enerji alanı & 0,0378$\\pm$0,0017 & 0,0397$\\pm$0,0010 & $-$0,0019 & 0,54 \\\\\n"
              "\\%90 enerji alanı & 0,2345$\\pm$0,0078 & 0,2570$\\pm$0,0067 & $-$0,0224 & 0,40 \\\\\n"
              "Mekansal entropi (nat) & 5,2014$\\pm$0,0387 & 5,2524$\\pm$0,0197 & $-$0,0509 & 0,54 \\\\\n"
              "Moran's $I$ & 0,4141$\\pm$0,0132 & 0,3941$\\pm$0,0024 & $+$0,0200 & 0,47 \\\\\n",
              "\\textbf{Ölçüt} & \\textbf{ResNet-18} & \\textbf{ViT-Tiny} & \\textbf{Fark (R$-$V)} & \\textbf{$p$ (Holm)} \\\\\n\\midrule\n"
              "\\%50 enerji alanı & 0,0378$\\pm$0,0017 & 0,0397$\\pm$0,0010 & $-$0,0019$\\pm$0,0027 & 0,54 \\\\\n"
              "\\%90 enerji alanı & 0,2345$\\pm$0,0078 & 0,2570$\\pm$0,0067 & $-$0,0224$\\pm$0,0133 & 0,40 \\\\\n"
              "Mekansal entropi (nat) & 5,2014$\\pm$0,0387 & 5,2524$\\pm$0,0197 & $-$0,0509$\\pm$0,0580 & 0,54 \\\\\n"
              "Moran's $I$ & 0,4141$\\pm$0,0132 & 0,3941$\\pm$0,0024 & $+$0,0200$\\pm$0,0156 & 0,47 \\\\\n",
              "TR Tablo 9 satirlari")
    for nm, txt in (("EN", en), ("TR", tr)):
        li = txt.find("\\label{tab:spatial}")
        seg_end = txt.find("\\begin{tabular}", li)
        seg = txt[li:seg_end]
        if "\\footnotesize" in seg:
            txt = txt[:li] + seg.replace("\\footnotesize", "\\scriptsize") + txt[seg_end:]
            print(f"OK    {nm} Tablo 9 scriptsize")
        else:
            print(f"ZATEN {nm} Tablo 9 scriptsize")
        if nm == "EN":
            en = txt
        else:
            tr = txt

    # 5. Tablo 10
    for old_lab, new_lab in (("layer1.0", "1.1"), ("layer1.1", "1.2"), ("layer2.0", "2.1"), ("layer2.1", "2.2"),
                             ("layer3.0", "3.1"), ("layer3.1", "3.2"), ("layer4.0", "4.1"), ("layer4.1", "4.2")):
        en = once(en, f"& {old_lab} & ", f"& {new_lab} & ", f"EN Tablo 10 {old_lab}")
        tr = once(tr, f"& {old_lab} & ", f"& {new_lab} & ", f"TR Tablo 10 {old_lab}")
    en = once(en, "\\textbf{Blk} & \\textbf{CLS} & \\textbf{Patch mean} & \\textbf{All tokens} & \\textbf{Block} & \\textbf{Cosine} \\\\",
              "\\textbf{Block} & \\textbf{CLS} & \\textbf{Patch mean} & \\textbf{All tokens} & \\textbf{Stage.block} & \\textbf{Cosine} \\\\",
              "EN Tablo 10 baslik satiri")
    tr = once(tr, "\\textbf{Blok} & \\textbf{CLS} & \\textbf{Yama ort.} & \\textbf{Tüm jetonlar} & \\textbf{Blok} & \\textbf{Kosinüs} \\\\",
              "\\textbf{Blok} & \\textbf{CLS} & \\textbf{Yama ort.} & \\textbf{Tüm jetonlar} & \\textbf{Aşama.blok} & \\textbf{Kosinüs} \\\\",
              "TR Tablo 10 baslik satiri")
    en = caption_append(en, "tab:feature_degradation",
                        "Run-to-run standard deviations are at most 0.0061 in the ViT columns and 0.0181 in the ResNet column (stage 4, block 1); bold marks the minimum of each column.",
                        "EN Tablo 10 baslik")
    tr = caption_append(tr, "tab:feature_degradation",
                        "Koşumlar arası standart sapma ViT sütunlarında en çok 0,0061, ResNet sütununda en çok 0,0181'dir (aşama 4, blok 1); kalın her sütunun en küçük değerini gösterir.",
                        "TR Tablo 10 baslik")

    # 6. isaretli kosinus siniri
    en = once(en, "mean cosine is near zero for both models ($\\leq0.0014$):",
              "mean cosine is near zero for both models ($\\leq0.0014$ in every run):", "EN 0.0014")
    tr = once(tr, "ortalama kosinüs ise iki modelde de sıfıra yakındır ($\\leq0{,}0014$):",
              "ortalama kosinüs ise iki modelde de sıfıra yakındır (her koşumda $\\leq0{,}0014$):", "TR 0.0014")

    if HATA:
        print("\nHATA:", "; ".join(HATA))
        print("Hicbir dosya yazilmadi.")
        sys.exit(1)
    io.open(EN, "w", encoding="utf-8", newline="\n").write(en)
    io.open(TR, "w", encoding="utf-8", newline="\n").write(tr)
    print("\n3. parti tamam.")


if __name__ == "__main__":
    main()
