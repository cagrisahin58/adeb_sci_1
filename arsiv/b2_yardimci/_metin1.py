#!/usr/bin/env python3
"""B2 metin guncellemesi -- 1/n: Tablo III, 4.2 paydalar/aralik/kat + yeni
protokol-ici duyarlilik paragrafi. Iki dil."""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata, yazilan = [], []


def yama(rel, ciftler, imza):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza in t:
        print(f"  atlandi (zaten yapilmis): {rel}")
        return
    for eski, yeni, ad in ciftler:
        n = t.count(eski)
        if n != 1:
            hata.append(f"{rel} :: {ad}: {n} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        yazilan.append(rel)


# =============================== INGILIZCE ===============================
EN_TABLO_E = ("Successful-source & 38.50$\\pm$0.75 & 23.91$\\pm$0.80 & "
              "$+$14.60$\\pm$1.48 & $+$5.28 \\\\")
EN_TABLO_Y = ("Successful-source & 36.39$\\pm$0.76 & 17.02$\\pm$0.52 & "
              "$+$19.37$\\pm$1.27 & $+$11.17 \\\\")

EN_PAYDA_E = ("and 3{,}122/5{,}331 under successful-source.")
EN_PAYDA_Y = ("and 2{,}831/3{,}814 under successful-source.")

EN_ARALIK_E = ("the asymmetry ranges from $+4.36\\pm0.44$ to $+14.60\\pm1.48$ points; "
               "the mean per-seed spread between the largest and the smallest protocol "
               "estimate is $10.45\\pm0.76$ points, a factor of 3.3, whereas the "
               "seed-level standard deviation within any single protocol stays below "
               "1.5 points.")
EN_ARALIK_Y = ("the asymmetry ranges from $+4.36\\pm0.44$ to $+19.37\\pm1.27$ points; "
               "the mean per-seed spread between the largest and the smallest protocol "
               "estimate is $15.01\\pm0.84$ points, a factor of 4.4, whereas the "
               "seed-level standard deviation within any single protocol stays below "
               "1.5 points.")

EN_GA_E = "with a paired bootstrap CI of $[7.33, 9.21]$"
EN_GA_Y = "with a paired bootstrap CI of $[7.33, 9.22]$"

# yeni paragraf, protokol tablosu paragrafinin hemen ardina
EN_ANKOR = ("A reader given only one of these numbers would draw a different "
            "conclusion about whether the architectures differ at all.")
EN_YENI_PARA = EN_ANKOR + """

A protocol name is not by itself a specification. The successful-source protocol conditions on samples whose attack succeeded on the source, and whether that phrase requires the source to classify the clean input correctly is a sub-choice that transfer studies rarely state. We report the stricter reading, in which white-box success means that the source is correct on the clean input and wrong on its adversarial counterpart. Under the looser reading, which also admits samples the source already misclassified, the measured asymmetry falls from $+19.37$ to $+14.60$ points and the protocol spread from $15.01$ to $10.45$ points. That shift of $4.77$ points is larger than the run-to-run standard deviation of any protocol in Table~\\ref{tab:transfer_protocols} by more than a factor of three, and the other three protocols are unchanged by construction. Because a sub-choice of this size is invisible in a protocol's name, all four conditioning masks are defined in a single place in the released code."""

yama("paper/manuscript/sections/04_experiments.tex",
     [(EN_TABLO_E, EN_TABLO_Y, "EN tablo"),
      (EN_PAYDA_E, EN_PAYDA_Y, "EN payda"),
      (EN_ARALIK_E, EN_ARALIK_Y, "EN aralik"),
      (EN_GA_E, EN_GA_Y, "EN GA"),
      (EN_ANKOR, EN_YENI_PARA, "EN yeni paragraf")],
     "A protocol name is not by itself a specification")

# ================================ TURKCE =================================
TR_TABLO_E = ("Başarılı kaynak & 38,50$\\pm$0,75 & 23,91$\\pm$0,80 & "
              "$+$14,60$\\pm$1,48 & $+$5,28 \\\\")
TR_TABLO_Y = ("Başarılı kaynak & 36,39$\\pm$0,76 & 17,02$\\pm$0,52 & "
              "$+$19,37$\\pm$1,27 & $+$11,17 \\\\")

TR_PAYDA_E = "ve başarılı kaynakta 3.122/5.331'dir."
TR_PAYDA_Y = "ve başarılı kaynakta 2.831/3.814'tür."

TR_ARALIK_E = ("asimetri $+4{,}36\\pm0{,}44$ ile $+14{,}60\\pm1{,}48$ puan arasında "
               "değişmektedir; en büyük ve en küçük protokol tahmini arasındaki "
               "tohum-başına ortalama yayılım $10{,}45\\pm0{,}76$ puandır (3,3 kat), "
               "oysa herhangi bir protokolün içindeki tohum düzeyi standart sapma "
               "1,5 puanın altında kalır.")
TR_ARALIK_Y = ("asimetri $+4{,}36\\pm0{,}44$ ile $+19{,}37\\pm1{,}27$ puan arasında "
               "değişmektedir; en büyük ve en küçük protokol tahmini arasındaki "
               "tohum-başına ortalama yayılım $15{,}01\\pm0{,}84$ puandır (4,4 kat), "
               "oysa herhangi bir protokolün içindeki tohum düzeyi standart sapma "
               "1,5 puanın altında kalır.")

TR_GA_E = "eşleştirilmiş bootstrap GA $[7{,}33; 9{,}21]$"
TR_GA_Y = "eşleştirilmiş bootstrap GA $[7{,}33; 9{,}22]$"

TR_ANKOR = ("Bu sayıların yalnızca birini gören bir okur, mimarilerin farklı olup "
            "olmadığı hakkında farklı bir sonuca varırdı.")
TR_YENI_PARA = TR_ANKOR + """

Bir protokolün adı tek başına bir tanım değildir. Başarılı kaynak protokolü, saldırının kaynakta başarılı olduğu örneklerle koşullamaktadır; bu ifadenin kaynağın temiz girdiyi doğru sınıflandırmasını gerektirip gerektirmediği ise transfer çalışmalarının nadiren yazdığı bir alt seçimdir. Bu makale daha sıkı okumayı raporlamaktadır: beyaz kutu başarısı, kaynağın temiz girdide doğru ve çekişmeli karşılığında yanlış olması demektir. Kaynağın zaten yanlış sınıflandırdığı örnekleri de içeri alan gevşek okumada ölçülen asimetri $+19{,}37$ puandan $+14{,}60$ puana, protokol yayılımı ise $15{,}01$ puandan $10{,}45$ puana inmektedir. Bu $4{,}77$ puanlık kayma, Tablo~\\ref{tab:transfer_protocols}'teki hiçbir protokolün koşumlar arası standart sapmasının üç katından azı değildir; diğer üç protokol ise tanım gereği değişmemektedir. Bu büyüklükte bir alt seçim protokolün adında görünmediği için, dört koşullama maskesinin tamamı yayımlanan kodda tek bir yerde tanımlanmaktadır."""

yama("paper/manuscript_tr/sections/04_deneyler.tex",
     [(TR_TABLO_E, TR_TABLO_Y, "TR tablo"),
      (TR_PAYDA_E, TR_PAYDA_Y, "TR payda"),
      (TR_ARALIK_E, TR_ARALIK_Y, "TR aralik"),
      (TR_GA_E, TR_GA_Y, "TR GA"),
      (TR_ANKOR, TR_YENI_PARA, "TR yeni paragraf")],
     "Bir protokolün adı tek başına bir tanım değildir")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("yazilan:", *yazilan, sep="\n  ")
