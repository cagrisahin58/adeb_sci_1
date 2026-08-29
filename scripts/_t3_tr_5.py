#!/usr/bin/env python3
"""TR aynasi - 5: TGR girisi ve oran paragraflari (EN ile ayni kesimler)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
D = "04_deneyler.tex"

YAMALAR = [
    # ---- TGR girisi: butce ve kontrol cumlesi 03'te zaten var ----
    (D,
     r"biz aynı mekanizmayı CIFAR-10 ViT-Tiny sarmalayıcımıza uyguluyor ve "
     r"saldırı bütçesini ImageNet varsayılanları yerine makalenin geri kalanıyla "
     r"eşliyoruz ($\eps=8/255$, $\alpha=2/255$, 10 adım, momentum 1,0). Kontrol "
     r"olarak aynı koşuda düz MI-FGSM örnekleri üretilir; böylece karşılaştırma "
     r"özdeş örnekler ve özdeş bütçe üzerinde eşleştirilmiştir.",
     r"biz aynı mekanizmayı CIFAR-10 ViT-Tiny sarmalayıcımıza, makale boyunca "
     r"kullanılan bütçeyle uyguluyoruz (Bölüm~\ref{subsec:attack_methods}); "
     r"eşleştirilmiş kontrol olarak aynı koşuda düz MI-FGSM üretilmektedir.",
     "TR TGR girisi"),

    # ---- oran paragrafi 1 ----
    (D,
     r"Bu değer tohum-başına açıklıkların ortalamasıdır ve burada protokol "
     r"ortalamalarının açıklığıyla çakışmaktadır, çünkü uç protokoller üç tohumun "
     r"üçünde de aynıdır: üstte başarılı kaynak, altta hedef doğru. CIFAR-100'de "
     r"ise iki değer ayrışmaktadır ($13{,}83$'e karşı $13{,}58$), çünkü orada uç "
     r"protokol tohumlar arasında değişmektedir.",
     r"Bu değer tohum-başına açıklıkların ortalamasıdır; burada protokol "
     r"ortalamalarının açıklığıyla çakışmakta, çünkü uç protokoller üç tohumun "
     r"üçünde de aynıdır, CIFAR-100'de ise ayrışmaktadır ($13{,}83$'e karşı "
     r"$13{,}58$), çünkü orada aynı değildir.",
     "TR oran paragrafi 1"),

    # ---- oran paragrafi 2 ----
    (D,
     r"Üç koşumla payda iki serbestlik derecesi taşır; dolayısıyla herhangi bir "
     r"tek oran için $\chi^2$ aralığı çok geniştir: dördü içinde en büyük koşumlar "
     r"arası standart sapmaya sahip başarılı-kaynak protokolünde oranın $\%95$ "
     r"aralığı $0{,}8$ ile $9{,}9$ arasında uzanır ve \emph{birimi içerir}. Tahmin "
     r"olarak değil duyarlılık olarak raporlandığında oran, yayılım ölçüleri ve "
     r"referans protokoller boyunca $5{,}2$ ile $32{,}6$ arasında değişmekte ve "
     r"birincil saydığımız her-ikisi-doğru protokolünde benzeri-benzeriyle standart "
     r"sapma karşılaştırmasında $28{,}3$ olmaktadır. İki uyarı oranı daha da "
     r"sınırlar. En büyük asimetriyi veren protokol aynı zamanda en büyük koşumlar "
     r"arası standart sapmayı taşımaktadır; yani pay ile payda bağımsız değildir. "
     r"Ayrıca üç koşumun tamamı, eğitimden önce çekilen tek doğrulama bölmesini "
     r"paylaştığından bu standart sapma bölmeler arası varyansı dışarıda bırakır; "
     r"bu da oranı bir üst sınır yapar. Bu aralığın genişliğini ve iki uyarıyı da "
     r"atlatan şey mutlak karşılaştırmadır; iddiayı taşıyan da kat değeri değil "
     r"odur.",

     r"Üç koşumla payda iki serbestlik derecesi taşır; dolayısıyla herhangi bir "
     r"tek oran için $\chi^2$ aralığı çok geniştir: başarılı-kaynak protokolünde "
     r"oran $0{,}8$ ile $9{,}9$ arasında uzanır ve \emph{birimi içerir}. "
     r"Duyarlılık olarak raporlandığında oran, yayılım ölçüleri ve referans "
     r"protokoller boyunca $5{,}2$ ile $32{,}6$ arasında değişmekte, birincil "
     r"saydığımız her-ikisi-doğru protokolünde benzeri-benzeriyle karşılaştırmada "
     r"$28{,}3$ olmaktadır. İki uyarı oranı daha da sınırlar: en büyük asimetriyi "
     r"veren protokol aynı zamanda en büyük koşumlar arası standart sapmayı "
     r"taşımakta, yani pay ile payda bağımsız olmamakta; ve üç koşum tek doğrulama "
     r"bölmesini paylaştığından payda bölmeler arası varyansı dışarıda bırakmakta, "
     r"bu da oranı bir üst sınır yapmaktadır. İkisini de atlatan şey mutlak "
     r"karşılaştırmadır; iddiayı taşıyan da kat değeri değil odur.",
     "TR oran paragrafi 2"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
