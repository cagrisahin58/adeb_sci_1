#!/usr/bin/env python3
"""TR aynasi - 7: yontem bolumu (cikarim birimi politikasi, TOST marji, atif)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
Y = "03_yontem.tex"

YAMALAR = [
    # ---------- C9: basarili kaynak atifsiz "yerlesik" ----------
    (Y,
     r"ve mimariler arası karşılaştırmalarda zorunludur:",
     r"ve en çok mimariler arası karşılaştırmalarda önem taşır:",
     "TR C9 zorunlu -> onemli"),

    (Y,
     r"iki yerleşik alternatifi de raporluyoruz: kaynak ve hedefin ikisinin de "
     r"doğru sınıflandırdığı örneklerle koşullayan \emph{her ikisi doğru} "
     r"protokolü~\cite{mahmood2021robustness, ravikumar2023trend} ve saldırının "
     r"kaynakta beyaz kutu anlamında başarılı olduğu hedef-doğru örneklerle "
     r"koşullayan \emph{başarılı kaynak} protokolü.",
     r"iki alternatifi de raporluyoruz: kaynak ve hedefin ikisinin de doğru "
     r"sınıflandırdığı örneklerle koşullayan \emph{her ikisi doğru} "
     r"protokolü~\cite{mahmood2021robustness, ravikumar2023trend} ve saldırının "
     r"kaynakta beyaz kutu anlamında başarılı olduğu hedef-doğru örneklerle "
     r"koşullayan \emph{başarılı kaynak} protokolü. Birincisi anılan anlamda "
     r"yerleşiktir; ikincisi için tek bir kanonik kaynak bilmiyoruz ve onu, bir "
     r"transfer oranı ``başarılı'' çekişmeli örnekler üzerinden raporlandığında "
     r"örtük olarak kullanılan protokol olduğu için dâhil ediyoruz.",
     "TR C9 basarili kaynak atfi"),

    # ---------- A5 + B4: cikarim birimi politikasi ve TOST marji ----------
    (Y,
     r"Eşdeğerlik iddiaları iki tek yönlü test (TOST) ile yapılır. Birincil marj "
     r"$\pm2$ puandır ve karşılaştırmalardan önce, PGD doğruluğundaki koşumlar "
     r"arası değişimden küçük farkların pratikte eşdeğer sayılması ilkesiyle "
     r"sabitlenmiştir; her eşdeğerlik iddiası ayrıca $\pm1$ ve $\pm3$ puanda da "
     r"raporlanır, böylece hüküm marja karşı okunabilir.",

     r"Bu çalışmada iki çıkarım birimi mevcuttur ve farklı soruları yanıtlarlar. "
     r"Örnek bazlı bir test, iki sabit kontrol noktasının değerlendirilen "
     r"görüntülerde farklı olup olmadığını sorar; üç eğitim tekrarı üzerinden "
     r"yapılan koşum düzeyi bir test ise mimarilerin farklı olup olmadığını. "
     r"Mimari bir iddiayı yalnızca ikincisi destekler ve üç koşumla ikisinden çok "
     r"daha zayıftır. İzlediğimiz kural şudur: her testin yanında birimi anmak, "
     r"iddia mimari olduğu her yerde koşum düzeyini kullanmak ve ikisinin "
     r"uyuşmadığı yerde iddiayı kayıranı değil ikisini birden raporlamak; "
     r"uyuşmadıkları yer Bölüm~\ref{subsec:gradient}'tir. Eşdeğerlik iddiaları "
     r"iki tek yönlü test (TOST) ile ve $\pm2$ puanlık birincil marjla yapılır; bu "
     r"marj karşılaştırmalardan önce PGD doğruluğundaki koşumlar arası değişimden "
     r"sabitlenmiştir. Bu, mutlak bir doğruluk için doğru ölçek, transfer "
     r"asimetrisi için yanlış ölçektir: asimetrinin kendi koşumlar arası standart "
     r"sapması $0{,}23$ puandır, dolayısıyla orada marj yaklaşık sekiz kat "
     r"cömerttir ve TOST'u eşdeğerliği kabul etmeye doğru yanlılaştırır. Ön "
     r"kayıtlı marjı veriyi gördükten sonra yeniden ayarlamak yerine koruyor ve "
     r"her eşdeğerlik iddiasını $\pm1$ ve $\pm3$ puanda da raporluyoruz; kabul "
     r"ettiğimiz tek eşdeğerlik olan SVHN, $\pm1$ puanda da geçerlidir.",
     "TR A5+B4 birim ve marj"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
