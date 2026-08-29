#!/usr/bin/env python3
"""TR aynasi - 2: L2 ucuncu ongoru, seyreklik cikarim birimi, mekansal karsilastirma."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
D = "04_deneyler.tex"

YAMALAR = [
    # ---------- B6: L2 ucuncu ongoru yanlislanabilir degil ----------
    (D,
     r"Kayıtlı üç ön kestirimin üçü de tutmaktadır: protokol yayılımı $L_2$ "
     r"altında $10{,}92$ puandır; $\Linf$ altında $15{,}01$ idi. Yani norm "
     r"değişince küçülmekte, ama ön kayıtın koyduğu iki puanlık tabanın çok "
     r"üstünde ve koşumlar arası standart sapmadan bir mertebe büyük kalmaktadır. "
     r"İşaret on iki ölçümün tamamında pozitiftir ve koşulsuz oranın koşullu "
     r"orandan sapması hâlâ hedefin temiz hatasıyla artmaktadır (eğim $+0{,}914$; "
     r"korelasyon yerine eğimi raporluyoruz, çünkü on sekiz yön yalnızca yedi "
     r"ayrık hedef hatası değeri almakta ve bunların altısı aynı sabit "
     r"WideResNet'ten gelmektedir, dolayısıyla bunlar üzerinde bir korelasyon "
     r"Bölüm~\ref{subsec:transfer}'in anlattığı biçimde kesinliği abartırdı).",

     r"Kayıtlı üç ön kestirimin ikisi tutmakta, üçüncüsü ise sınanabilir "
     r"çıkmamaktadır. Protokol yayılımı $L_2$ altında $10{,}92$ puandır; $\Linf$ "
     r"altında $15{,}01$ idi. Yani norm değişince küçülmekte, ama hem ön kayıtın "
     r"koyduğu iki puanlık tabanın hem de koşumlar arası standart sapmanın çok "
     r"üstünde kalmakta ve işaret on iki ölçümün tamamında pozitif olmaktadır. "
     r"Üçüncü kestirim, koşulsuz oranın koşullu orandan sapmasının hedefin temiz "
     r"hatasıyla artacağı, Denklem~\eqref{eq:raw_identity} sağlandığı sürece "
     r"yanlışlanamaz: sapma zaten $e\,(1 - r_{\text{koş}})$'dir, dolayısıyla $e$ "
     r"ile yapısı gereği artar ve uydurulan $+0{,}914$ eğimi bir şeyi sınamak "
     r"yerine $1 - r_{\text{koş}}$'u kestirmektedir. Bunu özdeşliği yazmadan önce "
     r"kaydetmiştik; şimdi özdeşliğin örneklem dışı bir sınaması olarak "
     r"raporluyoruz; Bölüm~\ref{subsec:cifar100}'de de aynı konumu veriyoruz.",
     "TR B6 L2 ucuncu ongoru"),

    # ---------- B1: seyreklik iki cikarim birimi ----------
    (D,
     r"Aynı 500 örnek iki modelde de ölçüldüğünden farklar örnek başına "
     r"eşleştirilmiş istatistiklerle test edilir: üçü de üç koşuda da anlamlıdır "
     r"(Wilcoxon işaretli sıra, baştan sona Holm düzeltmeli $p<10^{-11}$; "
     r"eşleştirilmiş Cohen $d$ 0,32 ile 1,23 arasında).",

     r"İki çıkarım birimimizin uyuşmadığı tek yer burasıdır, bu yüzden ikisini de "
     r"raporluyoruz. Koşum içinde, aynı 500 örnek iki modelde de ölçüldüğünde, "
     r"örnek başına eşleştirilmiş testler üç ölçüde de üç koşuda da kesindir "
     r"(Wilcoxon işaretli sıra, baştan sona Holm düzeltmeli $p<10^{-11}$; "
     r"eşleştirilmiş Cohen $d$ 0,32 ile 1,23 arasında); bu, bu kontrol "
     r"noktalarının bu görüntülerde farklı olduğunu kurar. Mimari bir iddianın "
     r"gerektirdiği ve Tablo~\ref{tab:spatial}'in kullandığı koşum düzeyinde ise "
     r"üç eşleştirilmiş koşum Gini, \%1 altı kesir ve Hoyer için sırasıyla "
     r"$0{,}036$, $0{,}042$ ve $0{,}067$ ham $p$ değeri vermekte, üç ölçü "
     r"üzerinden Holm düzeltmesi bunları $0{,}108$'e çıkarmaktadır. Sıralama üç "
     r"koşumun üçünde ve her ölçüde tutarlıdır ve açıklık koşumlar arası standart "
     r"sapmanın birkaç katıdır; ancak üç koşumla, üç ölçünün neredeyse eşdoğrusal "
     r"olması nedeniyle burada tutucu kalan bir düzeltmeden sonra $\alpha=0{,}05$ "
     r"eşiğini geçmemektedir. Bu nedenle seyreklik sonucunu anlamlı değil "
     r"yeniden üretilebilir olarak raporluyoruz. Aşağıdaki hizalanma farkı koşum "
     r"düzeyinde anlamlılığa ulaşmaktadır ($p=0{,}0009$) ve tartışmaya bu temelde "
     r"taşıdığımız gradyan sonucu odur.",
     "TR B1 seyreklik iki birim"),

    # ---------- B1: esit birimde karsilastirma ----------
    (D,
     r"ve düzeltmeden sonra ayakta kalmaz; bu da $p<10^{-11}$'de anlamlı olan "
     r"Hoyer farkının yanında marjinal bir etkidir. Tek bir koşum içindeki örnek "
     r"bazlı testler bu ölçülerde çok daha küçük $p$ değerlerine ulaşır, ama "
     r"farklı bir soruyu yanıtlarlar, yani iki sabit kontrol noktasının bu 500 "
     r"görüntüde farklı olup olmadığını; üstelik dört ölçünün ikisinde işaret "
     r"koşumlar boyunca kararlı değildir.",

     r"ve düzeltmeden sonra ayakta kalmaz. Aynı birimde karşılaştırıldığında "
     r"mekânsal ölçüler seyreklik ölçülerinden yalnızca zayıf değildir: seyreklik "
     r"sıralaması her koşuda ve her ölçüde tutarlıyken mekânsal sıralama dört "
     r"ölçünün ikisinde koşumlar boyunca kararlı değildir; üç koşumla iki aile de "
     r"koşum düzeyi düzeltmesini geçemese bile önemli olan fark budur. Tek bir "
     r"koşum içindeki örnek bazlı testler burada da çok daha küçük $p$ "
     r"değerlerine ulaşır, ama iki sabit kontrol noktasının bu 500 görüntüde "
     r"farklı olup olmadığı gibi daha dar bir soruyu yanıtlarlar.",
     "TR B1 esit birim"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
