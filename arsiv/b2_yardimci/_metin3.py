#!/usr/bin/env python3
"""B2 metin guncellemesi -- 3/n: CIFAR-100, SVHN, L2, sinif bilesimi ve
istatistik bolumu. Iki dil."""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    for eski, yeni, ad in ciftler:
        if eski not in t and yeni in t:
            continue                      # idempotent
        n = t.count(eski)
        if n != 1:
            hata.append(f"{rel} :: {ad}: {n} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# ============================ INGILIZCE: 04 ============================
EN = []

# --- 4.4 CIFAR-100: kisa acici kaldirildi, sayilar ve ANLATI duzeltildi ---
EN.append((
    "The protocol spread grows rather than shrinks. Across the same four protocols "
    "the measured CNN$\\rightarrow$ViT asymmetry runs from $+4.96\\pm1.01$ points "
    "(target-correct) to $+18.53\\pm0.71$ points (unconditioned), with "
    "$+10.92\\pm0.34$ under both-correct and $+11.44\\pm1.82$ under "
    "successful-source. The mean per-seed spread is $13.58\\pm1.71$ points, against "
    "$10.45\\pm0.76$ on CIFAR-10.",
    "Across the same four protocols the measured CNN$\\rightarrow$ViT asymmetry runs "
    "from $+4.96\\pm1.01$ points (target-correct) to $+18.53\\pm0.71$ points "
    "(unconditioned), with $+10.92\\pm0.34$ under both-correct and $+17.50\\pm0.92$ "
    "under successful-source. The mean per-seed spread is $13.83\\pm1.30$ points, "
    "against $15.01\\pm0.84$ on CIFAR-10, so the harder dataset places the protocol "
    "effect in the same range rather than shrinking it.",
    "EN C100 aralik"))
EN.append(("with a bootstrap CI of $[9.48, 12.36]$",
           "with a bootstrap CI of $[9.47, 12.35]$", "EN C100 GA"))

# --- sinif bilesimi: isaret artik KARARLI ve pozitif ---
EN.append((
    "Under successful-source it is negligible and its sign is not stable "
    "($+0.039$, $+0.013$, $-0.174$).",
    "Under successful-source it is small and positive in every seed ($+0.527$, "
    "$+0.435$ and $+0.382$ points, that is $2.1$ to $3.1\\%$ of the asymmetry).",
    "EN bilesim"))

# --- 4.5 SVHN ---
EN.append(("Successful-source & 62.50 & 59.86 & $+$2.64$\\pm$0.03 \\\\",
           "Successful-source & 61.38 & 58.69 & $+$2.70$\\pm$0.40 \\\\", "EN SVHN tablo"))
EN.append(("would announce a $2.64$-point CNN advantage on SVHN",
           "would announce a $2.70$-point CNN advantage on SVHN", "EN SVHN cumle"))
EN.append((
    "The protocol spread on SVHN is $3.65\\pm0.19$ points, against $10.45\\pm0.76$ on "
    "CIFAR-10 and $13.58\\pm1.71$ on CIFAR-100, ordered exactly as the clean-accuracy "
    "gaps are ($1.85$, $\\approx11$, $\\approx21$ points).",
    "The protocol spread on SVHN is $3.70\\pm0.62$ points, against $15.01\\pm0.84$ on "
    "CIFAR-10 and $13.83\\pm1.30$ on CIFAR-100, an order of magnitude apart from the "
    "two CIFAR values while the clean-accuracy gaps are $1.85$, $\\approx11$ and "
    "$\\approx21$ points.",
    "EN SVHN yayilim"))

# --- 4.6 L2: kisa acici kaldirildi, "ayni buyuklukte" suslemesi dustu ---
EN.append((
    "All three registered predictions hold. The protocol spread is $10.91$ points "
    "under $L_2$ against $10.45$ under $\\Linf$, which is not merely non-zero but the "
    "same size.",
    "All three registered predictions hold. The protocol spread is $10.92$ points "
    "under $L_2$ against $15.01$ under $\\Linf$, so it is smaller under the changed "
    "norm but stays far above the two-point floor the pre-registration set and an "
    "order of magnitude above the run-to-run standard deviation.",
    "EN L2 yayilim"))
EN.append(("and $+9.51\\pm0.89$ (successful-source)",
           "and $+12.06\\pm0.23$ (successful-source)", "EN L2 SS"))

# --- 4.7 istatistik: iki yayilim tanimi artik ESIT, uc protokol her tohumda AYNI ---
EN.append((
    "Within a fixed seed pair, changing only the conditioning protocol moves the "
    "asymmetry by $10.45\\pm0.76$ points. This figure is the mean of the per-seed "
    "ranges and slightly exceeds the $10.24$-point range of the protocol means, "
    "because the extremal protocol is not the same in every seed: in the third seed "
    "pair the largest asymmetry comes from the unconditioned rate rather than from "
    "successful-source.",
    "Within a fixed seed pair, changing only the conditioning protocol moves the "
    "asymmetry by $15.01\\pm0.84$ points. This figure is the mean of the per-seed "
    "ranges, and here it coincides with the range of the protocol means because the "
    "extremal protocols are the same in all three seeds, successful-source above and "
    "target-correct below; on CIFAR-100 the two figures differ ($13.83$ against "
    "$13.58$) because there the extremal protocol does change between seeds.",
    "EN yayilim tanimi"))
EN.append(("A ten-point measurement effect against a sub-$1.5$-point training effect "
           "is the ordering the paper rests on.",
           "A fifteen-point measurement effect against a sub-$1.5$-point training "
           "effect is the ordering the paper rests on.", "EN sira"))
EN.append((
    "the $95\\%$ interval on the ratio runs from $0.5$ to $6.3$ and therefore includes "
    "unity. Reported as a sensitivity rather than an estimate, the ratio spans $3.3$ "
    "to $22.7$ across dispersion measures and reference protocols, and equals $20.9$ "
    "under the like-for-like standard-deviation comparison on the both-correct "
    "protocol that we treat as primary.",
    "the $95\\%$ interval on the ratio runs from $0.8$ to $9.9$ and therefore includes "
    "unity. Reported as a sensitivity rather than an estimate, the ratio spans $5.2$ "
    "to $32.6$ across dispersion measures and reference protocols, and equals $28.3$ "
    "under the like-for-like standard-deviation comparison on the both-correct "
    "protocol that we treat as primary.",
    "EN oran duyarliligi"))

yama("paper/manuscript/sections/04_experiments.tex", EN)

# ============================== TURKCE: 04 ==============================
TR = []
TR.append((
    "Protokol yayılımı daralmamakta, genişlemektedir. Aynı dört protokol boyunca "
    "ölçülen CNN$\\rightarrow$ViT asimetrisi $+4{,}96\\pm1{,}01$ puandan (hedef doğru) "
    "$+18{,}53\\pm0{,}71$ puana (koşulsuz) uzanmakta; her ikisi doğru protokolünde "
    "$+10{,}92\\pm0{,}34$, başarılı kaynak protokolünde $+11{,}44\\pm1{,}82$ puandır. "
    "Tohum başına ortalama yayılım $13{,}58\\pm1{,}71$ puandır; CIFAR-10'da bu değer "
    "$10{,}45\\pm0{,}76$ idi.",
    "Aynı dört protokol boyunca ölçülen CNN$\\rightarrow$ViT asimetrisi "
    "$+4{,}96\\pm1{,}01$ puandan (hedef doğru) $+18{,}53\\pm0{,}71$ puana (koşulsuz) "
    "uzanmakta; her ikisi doğru protokolünde $+10{,}92\\pm0{,}34$, başarılı kaynak "
    "protokolünde $+17{,}50\\pm0{,}92$ puandır. Tohum başına ortalama yayılım "
    "$13{,}83\\pm1{,}30$ puandır; CIFAR-10'da bu değer $15{,}01\\pm0{,}84$ olduğuna "
    "göre daha zor veri kümesi protokol etkisini daraltmamakta, aynı aralıkta "
    "bırakmaktadır.",
    "TR C100 aralik"))
TR.append(("bootstrap güven aralığı $[9{,}48;\\ 12{,}36]$",
           "bootstrap güven aralığı $[9{,}47;\\ 12{,}35]$", "TR C100 GA"))
TR.append((
    "Başarılı kaynak protokolünde etki ihmal edilebilirdir ve işareti kararlı "
    "değildir ($+0{,}039$, $+0{,}013$, $-0{,}174$).",
    "Başarılı kaynak protokolünde etki küçüktür ve üç tohumun üçünde de pozitiftir "
    "($+0{,}527$, $+0{,}435$ ve $+0{,}382$ puan; asimetrinin \\%$2{,}1$ ile "
    "$3{,}1$'i kadar).",
    "TR bilesim"))
TR.append(("Başarılı kaynak & 62,50 & 59,86 & $+$2,64$\\pm$0,03 \\\\",
           "Başarılı kaynak & 61,38 & 58,69 & $+$2,70$\\pm$0,40 \\\\", "TR SVHN tablo"))
TR.append(("SVHN'de $2{,}64$ puanlık bir CNN üstünlüğü duyururdu",
           "SVHN'de $2{,}70$ puanlık bir CNN üstünlüğü duyururdu", "TR SVHN cumle"))
TR.append(("$+9{,}51\\pm0{,}89$ (başarılı kaynak)",
           "$+12{,}06\\pm0{,}23$ (başarılı kaynak)", "TR L2 SS"))
TR.append((
    "Protokol yayılımı $L_2$ altında $10{,}91$ puandır; $\\Linf$ altında $10{,}45$ "
    "idi; yani yalnızca sıfırdan farklı değil, aynı büyüklüktedir.",
    "Protokol yayılımı $L_2$ altında $10{,}92$ puandır; $\\Linf$ altında $15{,}01$ "
    "idi. Yani norm değişince küçülmekte, ama ön kayıtın koyduğu iki puanlık tabanın "
    "çok üstünde ve koşumlar arası standart sapmadan bir mertebe büyük kalmaktadır.",
    "TR L2 yayilim"))
TR.append((
    "Sabit bir tohum çiftinde yalnızca koşullama protokolünü değiştirmek asimetriyi "
    "$10{,}45\\pm0{,}76$ puan oynatmaktadır. Bu değer tohum-başına açıklıkların "
    "ortalamasıdır ve protokol ortalamalarının $10{,}24$ puanlık açıklığını bir "
    "miktar aşar; çünkü uç protokol her tohumda aynı değildir: üçüncü tohum çiftinde "
    "en büyük asimetri başarılı-kaynak değil koşulsuz orandan gelmektedir.",
    "Sabit bir tohum çiftinde yalnızca koşullama protokolünü değiştirmek asimetriyi "
    "$15{,}01\\pm0{,}84$ puan oynatmaktadır. Bu değer tohum-başına açıklıkların "
    "ortalamasıdır ve burada protokol ortalamalarının açıklığıyla çakışmaktadır, "
    "çünkü uç protokoller üç tohumun üçünde de aynıdır: üstte başarılı kaynak, altta "
    "hedef doğru. CIFAR-100'de ise iki değer ayrışmaktadır ($13{,}83$'e karşı "
    "$13{,}58$), çünkü orada uç protokol tohumlar arasında değişmektedir.",
    "TR yayilim tanimi"))
TR.append(("on puanlık bir ölçüm etkisine karşı $1{,}5$ puanın altında bir eğitim etkisi.",
           "on beş puanlık bir ölçüm etkisine karşı $1{,}5$ puanın altında bir eğitim "
           "etkisi.", "TR sira"))
TR.append((
    "oranın $\\%95$ aralığı $0{,}5$ ile $6{,}3$ arasında uzanır ve \\emph{birimi "
    "içerir}. Tahmin olarak değil duyarlılık olarak raporlandığında oran, yayılım "
    "ölçüleri ve referans protokoller boyunca $3{,}3$ ile $22{,}7$ arasında "
    "değişmekte ve birincil saydığımız her-ikisi-doğru protokolünde benzeri-benzeriyle "
    "standart sapma karşılaştırmasında $20{,}9$ olmaktadır.",
    "oranın $\\%95$ aralığı $0{,}8$ ile $9{,}9$ arasında uzanır ve \\emph{birimi "
    "içerir}. Tahmin olarak değil duyarlılık olarak raporlandığında oran, yayılım "
    "ölçüleri ve referans protokoller boyunca $5{,}2$ ile $32{,}6$ arasında "
    "değişmekte ve birincil saydığımız her-ikisi-doğru protokolünde benzeri-benzeriyle "
    "standart sapma karşılaştırmasında $28{,}3$ olmaktadır.",
    "TR oran duyarliligi"))
# (TR SVHN yayilim: _metin3b.py tarafindan yapildi)
# kendi yazdigim hantal Turkce ifadenin duzeltilmesi
TR.append((
    "Bu $4{,}77$ puanlık kayma, Tablo~\\ref{tab:transfer_protocols}'teki hiçbir "
    "protokolün koşumlar arası standart sapmasının üç katından azı değildir; diğer "
    "üç protokol ise tanım gereği değişmemektedir.",
    "Bu $4{,}77$ puanlık kayma, Tablo~\\ref{tab:transfer_protocols}'teki her "
    "protokolün koşumlar arası standart sapmasının üç katından büyüktür; diğer üç "
    "protokol ise tanım gereği değişmemektedir.",
    "TR uslup duzeltmesi"))

yama("paper/manuscript_tr/sections/04_deneyler.tex", TR)

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
