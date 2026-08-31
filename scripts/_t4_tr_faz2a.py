#!/usr/bin/env python3
"""TUR 4 FAZ 2 - A bolumu (Turkce aynasi)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

S = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

YAMALAR = [
    # ================= 2.1: kol karsilastirmasi =================
    ("04_deneyler.tex",
     r"Başarılı kaynak protokolü dışarıda bırakıldığında iki kol $+0{,}673$ "
     r"(GA $[+0{,}602;\ +0{,}727]$) ve $+0{,}431$ (GA $[+0{,}333;\ +0{,}633]$) "
     r"eğimleri vermektedir: işaret aynı, aralıklar örtüşüyor. Dahil "
     r"edildiğinde kontrollü kol $+0{,}273$ (GA $[+0{,}219;\ +0{,}371]$), "
     r"gözlemsel kol $-0{,}528$ (GA $[-0{,}664;\ -0{,}418]$) vermektedir. "
     r"Bileşim, bu uyuşmazlığın büyük kısmını açıklamakta ama onu "
     r"kapatmamaktadır. Kontrollü kol WideResNet içermez; gözlemsel kol aynı "
     r"mimari çiftine kısıtlandığında dört protokollü eğimi $-0{,}528$'den "
     r"$-0{,}100$'e gelmekte (GA $[-0{,}464;\ +0{,}092]$), yani aralık sıfırı "
     r"içermekte ama kontrollü kolun aralığıyla hâlâ örtüşmemektedir. "
     r"Dolayısıyla iki kol üç protokollü eğimde uyuşmakta, dört protokollüde "
     r"uyuşmamaktadır; mekanizma iddiasının dayandığı sıralama da budur.",

     r"Başarılı kaynak protokolü dışarıda bırakıldığında iki kol uyuşmaktadır: "
     r"ön kayıtlı havuzda kontrollü kol $+0{,}673$ (GA "
     r"$[+0{,}602;\ +0{,}727]$), gözlemsel kol $+0{,}470$ (GA "
     r"$[+0{,}361;\ +0{,}665]$) vermekte; işaret aynı, aralıklar örtüşüyor. "
     r"Yukarıda geri çektiğimiz dört protokollü eğim ise hiçbir yönde "
     r"karşılaştırma taşımaz: ön kayıtlı havuzda gözlemsel aralık "
     r"$[-0{,}570;\ +0{,}469]$, kontrollü kolun $[+0{,}219;\ +0{,}371]$ "
     r"aralığını bütünüyle kapsar; yani kollar orada bilgi taşıyan bir anlamda "
     r"ne uyuşur ne uyuşmaz. Post-hoc karşıtlığı yalnızca havuz seçiminin ne "
     r"yaptığını göstermek için kaydediyoruz. SVHN dışarıda bırakıldığında "
     r"gözlemsel dört protokollü eğim $-0{,}528$'e (GA "
     r"$[-0{,}664;\ -0{,}418]$) gitmekte ve kontrollü kolla örtüşmemekte; o "
     r"havuz eşleşmiş mimari çiftine kısıtlandığında ise $-0{,}100$'e (GA "
     r"$[-0{,}464;\ +0{,}092]$) gelmektedir. Hangi çiftlerin uydurmaya girdiğine "
     r"bu kadar duyarlı bir nicelik, bir mekanizma iddiasının dayanağı olamaz. "
     r"İddiayı taşıyan uyuşma üç protokollü olandır ve uydurduğumuz her havuzda "
     r"geçerlidir.",
     "TR 2.1 kol karsilastirmasi"),

    # ================= 1.2: derinlik anlatisi =================
    ("04_deneyler.tex",
     r"ViT'te kayma kademeli ve sığdır: benzerlik 8 ile 10. bloklar "
     r"civarındaki bir minimuma doğru düzenli biçimde azalır ve çıkışa doğru "
     r"toparlanır; öznitelik normları baştan sona temiz değerlerinin "
     r"\%0,7'si içinde kalır,",
     r"ViT'te kayma kademeli ve sığdır: benzerlik 11. bloktaki minimuma kadar "
     r"tekdüze azalır ve çıkışta hafifçe toparlanır; öznitelik normları baştan "
     r"sona temiz değerlerinin \%0,45'i içinde kalır,",
     "TR 1.2 derinlik anlatisi"),

    # ================= 1.2: toplulastirma paragrafi =================
    ("04_deneyler.tex",
     r"Kendi minimumlarında CLS yolu, yama jetonu ortalamasının yaklaşık dört "
     r"katı kadar kaymakta ($0{,}9343$'e karşı $0{,}9840$; $1-\cos$ cinsinden "
     r"oran $4{,}1$) ve iki özet, minimumu farklı derinliklere bile "
     r"yerleştirmektedir (blok 10'a karşı blok 8). Sınıflandırıcının okuduğu "
     r"şey CLS jetonu olduğundan bu bir ayrıntı değil bir sonuçtur: "
     r"pertürbasyon sınıflandırma yoluna yoğunlaşırken ortalama yama temsili "
     r"görece korunmaktadır. Bu ayrıca, farklı makalelerden katman bazlı kayma "
     r"eğrilerinin, agregasyon belirtilmedikçe doğrudan karşılaştırılamayacağı "
     r"anlamına gelir.",

     r"Kendi minimumlarında CLS yolu, yama jetonu ortalamasının yaklaşık üç "
     r"katı kadar kaymakta ($0{,}9604$'e karşı $0{,}9870$; $1-\cos$ cinsinden "
     r"oran $3{,}05$) ve iki özet minimumu farklı derinliklere yerleştirmektedir "
     r"(blok 11'e karşı blok 9). Sınıflandırıcının okuduğu şey blok çıkışındaki "
     r"CLS jetonu olduğundan bu bir ayrıntı değil bir sonuçtur: pertürbasyon "
     r"sınıflandırma yoluna yoğunlaşırken ortalama yama temsili görece "
     r"korunmaktadır. Özetin alındığı tensör, en az agregasyon kadar önemlidir. "
     r"Artık blok çıkışı yerine MLP alt-blok çıkışında okunduğunda aynı üç özet "
     r"blok 10'da $0{,}9343$ CLS minimumu, blok 8'de $0{,}9840$ yama jetonu "
     r"minimumu ve $4{,}12$ oranı vermektedir: kayma daha büyük görünmekte, "
     r"derinlikler yer değiştirmekte ve alt blok, sınıflandırıcının okuduğu "
     r"tensör olmamaktadır. Dolayısıyla farklı makalelerden katman bazlı kayma "
     r"eğrileri, hem agregasyon hem de alındıkları tensör belirtilmedikçe "
     r"karşılaştırılamaz.",
     "TR 1.2 toplulastirma"),

    # ================= 1.2: tablo =================
    ("04_deneyler.tex",
     "1 & 0,9993 & 0,9989 & 0,9942 & layer1.0 & 0,9951 \\\\\n"
     "2 & 0,9910 & 0,9957 & 0,9868 & layer1.1 & 0,9918 \\\\\n"
     "3 & 0,9785 & 0,9928 & 0,9821 & layer2.0 & 0,9879 \\\\\n"
     "4 & 0,9709 & 0,9877 & 0,9734 & layer2.1 & 0,9853 \\\\\n"
     "5 & 0,9652 & 0,9870 & 0,9719 & layer3.0 & 0,9753 \\\\\n"
     "6 & 0,9596 & 0,9873 & 0,9712 & layer3.1 & 0,9607 \\\\\n"
     "7 & 0,9497 & 0,9870 & 0,9698 & layer4.0 & \\textbf{0,8777} \\\\\n"
     "8 & 0,9414 & \\textbf{0,9840} & \\textbf{0,9663} & layer4.1 & 0,9108 \\\\\n"
     "9 & 0,9353 & 0,9850 & 0,9675 & & \\\\\n"
     "10 & \\textbf{0,9343} & 0,9877 & 0,9696 & & \\\\\n"
     "11 & 0,9352 & 0,9912 & 0,9753 & & \\\\\n"
     "12 & 0,9779 & 0,9955 & 0,9884 & & \\\\",

     "1 & 0,9993 & 0,9980 & 0,9927 & layer1.0 & 0,9951 \\\\\n"
     "2 & 0,9950 & 0,9959 & 0,9901 & layer1.1 & 0,9918 \\\\\n"
     "3 & 0,9902 & 0,9940 & 0,9881 & layer2.0 & 0,9879 \\\\\n"
     "4 & 0,9873 & 0,9919 & 0,9861 & layer2.1 & 0,9853 \\\\\n"
     "5 & 0,9845 & 0,9904 & 0,9847 & layer3.0 & 0,9753 \\\\\n"
     "6 & 0,9814 & 0,9894 & 0,9835 & layer3.1 & 0,9607 \\\\\n"
     "7 & 0,9782 & 0,9885 & 0,9826 & layer4.0 & \\textbf{0,8777} \\\\\n"
     "8 & 0,9743 & 0,9875 & 0,9816 & layer4.1 & 0,9108 \\\\\n"
     "9 & 0,9703 & \\textbf{0,9870} & 0,9809 & & \\\\\n"
     "10 & 0,9661 & 0,9872 & 0,9805 & & \\\\\n"
     "11 & \\textbf{0,9604} & 0,9874 & \\textbf{0,9803} & & \\\\\n"
     "12 & 0,9663 & 0,9915 & 0,9837 & & \\\\",
     "TR 1.2 tablo satirlari"),

    # ================= tartisma =================
    ("05_tartisma.tex",
     r"yani CLS yolunun yama ortalamasının yaklaşık dört katı kayması",
     r"yani CLS yolunun yama ortalamasının yaklaşık üç katı kayması",
     "TR 1.2 tartisma orani"),
]

if not uygula(YAMALAR, S):
    sys.exit(1)
