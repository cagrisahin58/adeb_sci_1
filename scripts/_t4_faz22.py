#!/usr/bin/env python3
"""FAZ 2.2: cikarim birimi serhi CIFAR-100 ve SVHN'e tasinir.

04:105'te CIFAR-10 icin su serh var: raporlanan "eslestirilmis bootstrap
GA" tohumlarin kendi GA uclarinin ORTALAMASIDIR, kapsama garantisi olan
bir aralik degildir; kosum duzeyi cikarim icin tohumlar-arasi t araligi
verilir. Serh CIFAR-100 ve SVHN'e tasinmamisti.

Olculen (scripts/_t4_birim.py):
  CIFAR-100  GA uclari [9,65 9,08 9,69] / [12,63 11,95 12,48] -> ort
             [9,47; 12,35];  3 tohum, t araligi [10,07; 11,77]
  SVHN       GA uclari [-0,75 -0,76] / [0,07 0,06] -> ort [-0,76; +0,07]
             YALNIZ 2 tohum; df=1, t araligi bilgi tasimaz -> ETIKETLEME

Ayrica CIFAR-100'de TOST yonu terstir ("reddedilmistir"); artefakt
tost_equivalent_any = False, yani ESDEGERLIK KURULAMADI.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

EN = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
TR = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

if not uygula([
    # ---------------- CIFAR-100 ----------------
    ("04_experiments.tex",
     r"Under the both-correct protocol the paired difference is $10.92$ points "
     r"with a bootstrap CI of $[9.47, 12.35]$, a sign-flip permutation $p$ "
     r"below the resolution of $20{,}000$ permutations in every seed, and "
     r"equivalence rejected at every margin tested.",

     r"Under the both-correct protocol the paired difference is $10.92$ points. "
     r"As on CIFAR-10, the quoted interval $[9.47, 12.35]$ is the average of the "
     r"three per-seed bootstrap endpoints rather than an interval with a "
     r"coverage guarantee; the across-run $t$ interval, which is the one that "
     r"matches a claim about architectures, is $[10.07, 11.77]$. The sign-flip "
     r"permutation $p$ is below the resolution of $20{,}000$ permutations in "
     r"every seed, and TOST does not establish equivalence at any margin tested.",
     "2.2 EN CIFAR-100"),

    # ---------------- SVHN ----------------
    ("04_experiments.tex",
     r"the difference is $-0.35$ points with a paired bootstrap CI of "
     r"$[-0.76, +0.07]$, a sign-flip permutation $p$ of $0.105$, and TOST "
     r"equivalence \emph{accepted} at all three margins, including the tightest "
     r"one we test ($\pm1$ point, $p=0.0007$).",

     r"the difference is $-0.35$ points, with a sign-flip permutation $p$ of "
     r"$0.105$ and TOST equivalence \emph{accepted} at all three margins, "
     r"including the tightest one we test ($\pm1$ point, $p=0.0007$). One "
     r"qualification belongs with that acceptance. SVHN was run with two seed "
     r"pairs, so the quoted interval $[-0.76, +0.07]$ averages the endpoints of "
     r"two per-seed bootstraps and no across-run interval is available: with two "
     r"runs the run-to-run standard deviation is estimated from a single "
     r"contrast and carries no information. The equivalence therefore rests on "
     r"the within-run comparison, and we report it because the two runs agree "
     r"closely ($-0.34$ and $-0.36$), not because two runs bound the run-to-run "
     r"variation.",
     "2.2 EN SVHN"),
], EN):
    sys.exit(1)

if not uygula([
    ("04_deneyler.tex",
     r"Her ikisi doğru protokolünde eşleştirilmiş fark $10{,}92$ puan, "
     r"bootstrap güven aralığı $[9{,}47;\ 12{,}35]$, işaret çevirme permütasyon "
     r"$p$ değeri her tohumda $20{,}000$ permütasyonun çözünürlüğünün altında "
     r"ve eşdeğerlik sınanan her marjda reddedilmiştir.",

     r"Her ikisi doğru protokolünde eşleştirilmiş fark $10{,}92$ puandır. "
     r"CIFAR-10'da olduğu gibi, verilen $[9{,}47;\ 12{,}35]$ aralığı üç tohumun "
     r"kendi bootstrap uçlarının ortalamasıdır, kapsama garantisi olan bir "
     r"aralık değildir; mimarilere dair bir iddiayla eşleşen koşumlar-arası $t$ "
     r"aralığı $[10{,}07;\ 11{,}77]$'dir. İşaret çevirme permütasyon $p$ değeri "
     r"her tohumda $20{,}000$ permütasyonun çözünürlüğünün altındadır ve TOST "
     r"sınanan hiçbir marjda eşdeğerliği kuramamaktadır.",
     "2.2 TR CIFAR-100"),

    ("04_deneyler.tex",
     r"fark $-0{,}35$ puan, eşleştirilmiş bootstrap güven aralığı "
     r"$[-0{,}76;\ +0{,}07]$, işaret çevirme permütasyon $p$ değeri $0{,}105$ "
     r"ve TOST eşdeğerliği, denediğimiz en dar marj dâhil ($\pm1$ puan, "
     r"$p=0{,}0007$) üç marjın üçünde de \emph{kabul edilmektedir}.",

     r"fark $-0{,}35$ puandır; işaret çevirme permütasyon $p$ değeri $0{,}105$ "
     r"ve TOST eşdeğerliği, denediğimiz en dar marj dâhil ($\pm1$ puan, "
     r"$p=0{,}0007$) üç marjın üçünde de \emph{kabul edilmektedir}. Bu kabulle "
     r"birlikte bir kayıt düşülmelidir. SVHN iki tohum çiftiyle koşulmuştur, "
     r"dolayısıyla verilen $[-0{,}76;\ +0{,}07]$ aralığı iki tohumun bootstrap "
     r"uçlarının ortalamasıdır ve koşumlar-arası bir aralık mevcut değildir: "
     r"iki koşumla koşumlar-arası standart sapma tek bir karşıtlıktan kestirilir "
     r"ve bilgi taşımaz. Eşdeğerlik bu yüzden koşum-içi karşılaştırmaya "
     r"dayanmaktadır; onu, iki koşum birbirine çok yakın olduğu için "
     r"($-0{,}34$ ve $-0{,}36$) raporluyoruz, iki koşum koşumlar-arası değişimi "
     r"sınırladığı için değil.",
     "2.2 TR SVHN"),
], TR):
    sys.exit(1)
