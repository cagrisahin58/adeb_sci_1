#!/usr/bin/env python3
"""Bagimsiz denetimin (2026-08-25) teyit ettigi metin kalemlerini duzeltir."""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# ============================== INGILIZCE 04 ==============================
EN = []

# (1) tohum degisimi: 0,55 -> 0,80 (Tablo II'nin kendisi 0,80 basiyor)
EN.append(("at most 0.55 points on any reported quantity",
           "at most 0.80 points on any reported accuracy", "EN 0.55"))

# (2) Sekil 1 basligi: figurde FGSM cubugu YOK
EN.append(("\\caption{Clean, FGSM, PGD-10, and AutoAttack accuracy at "
           "$\\eps=8/255$ on the full CIFAR-10 test set.",
           "\\caption{Clean, PGD-10, and AutoAttack accuracy at "
           "$\\eps=8/255$ on the full CIFAR-10 test set.", "EN sekil 1"))

# (3) benim 2026-08-25 duzenlememde bozulan cumle siniri
EN.append(("so it is the extreme in $16$, The protocol pair with the largest "
           "average gap is",
           "so it is the extreme in $16$ of them. The protocol pair with the "
           "largest average gap is", "EN cumle siniri"))

# (4) temiz dogruluk farki: ~11 -> 12,3 (uc tohum ortalamasi 12,26)
EN.append(("both place the two architectures far apart in clean accuracy "
           "(about $11$ and $21$ points)",
           "both place the two architectures far apart in clean accuracy "
           "(about $12$ and $21$ points)", "EN 11 puan a"))
EN.append(("the clean-accuracy gaps are $1.85$, $\\approx11$ and $\\approx21$ points",
           "the clean-accuracy gaps are $1.85$, $\\approx12$ and $\\approx21$ points",
           "EN 11 puan b"))

# (5) 'bir buyukluk mertebesi' -> olculen oran ~4 kat
EN.append(("an order of magnitude apart from the two CIFAR values while the "
           "clean-accuracy gaps are",
           "roughly four times smaller than the two CIFAR values while the "
           "clean-accuracy gaps are", "EN mertebe"))

# (6) 4.4 paragraf basi: nokta kestirimi DARALMISTIR
EN.append(("so the harder dataset places the protocol effect in the same range "
           "rather than shrinking it.",
           "so the harder dataset leaves the protocol effect in the same range, "
           "slightly below the CIFAR-10 value rather than above it.",
           "EN 4.4 acici"))

# (7) kosum sd araligi 1,48 -> 1,27
EN.append(("moves that same asymmetry by a standard deviation of only $0.23$ to "
           "$1.48$ points",
           "moves that same asymmetry by a standard deviation of only $0.23$ to "
           "$1.27$ points", "EN 1.48"))

# (8) Tablo V: 8 nicelikten 2'si sd icinde; SIRALAMA korunuyor
EN.append(("every quantity in Table~\\ref{tab:gradient} reproduces the value "
           "measured on our earlier single-run checkpoints to within the reported "
           "standard deviations, in contrast to the conditional decomposition of "
           "Section~\\ref{subsec:robustness}.",
           "every quantity in Table~\\ref{tab:gradient} reproduces the "
           "\\emph{ordering} measured on our earlier single-run checkpoints, "
           "although in six of the eight cases the value itself moves by more "
           "than the seed-level standard deviation reported here. The contrast "
           "with the conditional decomposition of "
           "Section~\\ref{subsec:robustness} is therefore about direction rather "
           "than magnitude: there the attribution between clean accuracy and "
           "conditional sensitivity changed between checkpoint sets, whereas here "
           "no gradient-structure difference changes sign.",
           "EN Tablo V"))

# (9) CIFAR-100 bilesim yuzdesi: asimetriye oran 17,4-29,7
EN.append(("that is $12.9$ to $18.6\\%$ of the asymmetry and \\emph{negative}",
           "that is $17.4$ to $29.7\\%$ of the asymmetry and \\emph{negative}",
           "EN bilesim yuzdesi"))

yama("paper/manuscript/sections/04_experiments.tex", EN)

# ================================ TURKCE 04 ================================
TR = []
TR.append(("raporlanan hiçbir büyüklükte 0,55 puanı aşmaz",
           "raporlanan hiçbir doğrulukta 0,80 puanı aşmaz", "TR 0.55"))
TR.append(("yani $16$ çiftte uçtur Ortalama açıklığı en büyük olan protokol çifti",
           "yani $16$ çiftte uçtur. Ortalama açıklığı en büyük olan protokol çifti",
           "TR cumle siniri"))
TR.append(("temiz doğrulukta birbirinden hayli uzağa yerleştirmektedir "
           "(yaklaşık $11$ ve $21$ puan)",
           "temiz doğrulukta birbirinden hayli uzağa yerleştirmektedir "
           "(yaklaşık $12$ ve $21$ puan)", "TR 11 puan a"))
TR.append(("temiz doğruluk farkları ise sırasıyla $1{,}85$, $\\approx11$ ve "
           "$\\approx21$ puandır",
           "temiz doğruluk farkları ise sırasıyla $1{,}85$, $\\approx12$ ve "
           "$\\approx21$ puandır", "TR 11 puan b"))
# (TR mertebe: Turkce surumde boyle bir ifade zaten YOK)
TR.append(("göre daha zor veri kümesi protokol etkisini daraltmamakta, aynı "
           "aralıkta bırakmaktadır.",
           "göre daha zor veri kümesi protokol etkisini aynı aralıkta "
           "bırakmakta, CIFAR-10 değerinin bir miktar altında tutmaktadır.",
           "TR 4.4 acici"))
TR.append(("$0{,}23$ ile $1{,}48$ puanlık standart sapmayla oynatmaktadır",
           "$0{,}23$ ile $1{,}27$ puanlık standart sapmayla oynatmaktadır",
           "TR 1.48"))
TR.append(("Tablo~\\ref{tab:gradient}'teki her büyüklük, önceki tek koşuluk "
           "kontrol noktalarında ölçülen değeri raporlanan standart sapmalar "
           "içinde yeniden üretmektedir",
           "Tablo~\\ref{tab:gradient}'teki her büyüklük, önceki tek koşuluk "
           "kontrol noktalarında ölçülen \\emph{sıralamayı} yeniden "
           "üretmektedir; sekiz niceliğin altısında değerin kendisi buradaki "
           "tohum düzeyi standart sapmadan fazla oynasa da hiçbir gradyan yapısı "
           "farkı işaret değiştirmemektedir", "TR Tablo V"))
TR.append(("yani asimetrinin $\\%12{,}9$ ile $18{,}6$'sı kadar ve \\emph{negatiftir}",
           "yani asimetrinin $\\%17{,}4$ ile $29{,}7$'si kadar ve \\emph{negatiftir}",
           "TR bilesim yuzdesi"))

yama("paper/manuscript_tr/sections/04_deneyler.tex", TR)

# ============================= Tartisma: 1,48 =============================
yama("paper/manuscript/sections/05_discussion.tex",
     [("moves it by a standard deviation of $0.23$ to $1.48$ points",
       "moves it by a standard deviation of $0.23$ to $1.27$ points",
       "EN disc 1.48")])
yama("paper/manuscript_tr/sections/05_tartisma.tex",
     [("onu $0{,}23$ ile $1{,}48$ puanlık standart sapmayla oynatırken",
       "onu $0{,}23$ ile $1{,}27$ puanlık standart sapmayla oynatırken",
       "TR disc 1.48")])

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
