#!/usr/bin/env python3
"""TR aynasi - 1: 4. bolum cerceve ve olgu duzeltmeleri (41, 64, 120, 126, 130, 148).

Ingilizce tarafla AYNI defter maddelerini uygular:
HAKEM_TURU3_DEFTER.md bolum A (cerceve), B (istatistik), C (olgu).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

ROOT = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")
D = "04_deneyler.tex"

YAMALAR = [
    # ---------- C7: 0,80 bir oran, dogruluk degil ----------
    (D,
     r"Tohum düzeyindeki değişim, çekişmeli eğitilmiş çift için baştan sona "
     r"küçüktür (raporlanan hiçbir doğrulukta 0,80 puanı aşmaz); dolayısıyla "
     r"sıralama koşudan koşuya gürültünün ürünü değildir.",
     r"Çekişmeli eğitilmiş çiftte tohum düzeyindeki değişim raporlanan hiçbir "
     r"doğrulukta 0,55 puanı aşmaz; dolayısıyla sıralama koşudan koşuya gürültü "
     r"değildir.",
     "TR C7 0,80 -> 0,55"),

    # ---------- ifade sikilastirmasi (EN ile ayni) ----------
    (D,
     r"her koşu içinde McNemar'ın eşleştirilmiş testi uygulanabilir; test üç "
     r"çiftte de CNN lehine kesindir",
     r"her koşu içinde McNemar'ın eşleştirilmiş testi uygulanabilir ve üç çiftte "
     r"de CNN lehine kesindir",
     "TR McNemar cumlesi"),

    (D,
     r"AutoAttack gürbüzlüğü iki mimaride de PGD-10'un tutarlı biçimde altındadır "
     r"(ResNet-18 için 6,2, ViT-Tiny için 3,6 puan); bu, daha güçlü topluluğun "
     r"değerini doğrular. \%62{,}76'daki WideResNet-28-10 "
     r"referansı~\cite{gowal2020uncovering}, kapasitenin, ek eğitim verisinin ve "
     r"daha güçlü tarifin birlikte gürbüzlüğü mimari seçiminin ötesine ne kadar "
     r"taşıdığını göstermektedir; bu modeli eşleşmiş çiftten görsel ve analitik "
     r"olarak ayrı tutuyoruz.",
     r"AutoAttack gürbüzlüğü iki mimaride de PGD-10'un altına düşmektedir "
     r"(ResNet-18 için 6,2, ViT-Tiny için 3,6 puan); bu, daha güçlü topluluğun "
     r"değerini doğrular. \%62{,}76'daki WideResNet-28-10 "
     r"referansı~\cite{gowal2020uncovering}, kapasitenin, ek eğitim verisinin ve "
     r"daha güçlü tarifin gürbüzlüğü mimari seçiminin ötesine ne kadar taşıdığını "
     r"göstermektedir; bu modeli eşleşmiş çiftten ayrı tutuyoruz.",
     "TR AutoAttack ve WRN"),

    # ---------- C2: her-ikisi-dogru McNemar siniri ----------
    (D,
     r"Çiftin iki modelinin de temizde doğru sınıflandırdığı $n=7.061\pm68$ "
     r"örnekten oluşan ve bu nedenle ortak girdiler üzerinde birebir eşleştirilmiş "
     r"bir karşılaştırma sağlayan ortak çözülen altkümede CNN 13,8 ve 10,7 puan "
     r"öndedir (her koşuda McNemar $p<10^{-84}$).",
     r"Çiftin iki modelinin de temizde doğru sınıflandırdığı $n=7.061\pm68$ "
     r"örnekte, yani birebir eşleştirilmiş bir karşılaştırmada, CNN 13,8 ve 10,7 "
     r"puan öndedir (her koşuda McNemar $p<10^{-67}$; bu sınır bu altkümede "
     r"hesaplanmıştır ve yukarıda anılan tam küme sınırından zayıftır, aradaki "
     r"fark büyük paydanın satın aldığı şeydir).",
     "TR C2 McNemar siniri"),

    # ---------- A1: manset ayristirmasi ----------
    (D,
     r"en büyük ve en küçük protokol tahmini arasındaki tohum-başına ortalama "
     r"yayılım $15{,}01\pm0{,}84$ puandır (4,4 kat), oysa herhangi bir protokolün "
     r"içindeki tohum düzeyi standart sapma 1,5 puanın altında kalır.",

     r"en büyük ve en küçük protokol tahmini arasındaki tohum-başına ortalama "
     r"yayılım $15{,}01\pm0{,}84$ puandır (4,4 kat), oysa herhangi bir protokolün "
     r"içindeki tohum düzeyi standart sapma 1,5 puanın altında kalır. Bu yayılım "
     r"tek bir nicelik değildir ve onu ayrıştırmak sonucun bir parçasıdır. Dört "
     r"tahmin sıralandığında üç bitişik açıklık çıkar: hedef doğru ile her ikisi "
     r"doğru arasında $3{,}91$ puan (yönlü iddialar için onayladığımız ve "
     r"birbirinden yalnızca kaynağın da doğru olmasının gerekip gerekmediğiyle "
     r"ayrılan iki protokol); her ikisi doğru ile koşulsuz oran arasında $5{,}30$ "
     r"puan (aşağıdaki Denklem~\eqref{eq:raw_identity}'in kapalı formda "
     r"öngördüğü ve okurun hedefin temiz hatasını bilerek geri alabileceği "
     r"açıklık); koşulsuz oranla başarılı kaynak oranı arasında $5{,}80$ puan "
     r"(kaynağın kendi beyaz kutu başarısızlığına koşullandığı için farklı bir "
     r"niceliği kestiren protokol). Yalnızca ilki aynı sorunun iki savunulabilir "
     r"okuması arasındaki indirgenemez takdirdir ve $3{,}91$ puanla bile iki "
     r"mimariyi yeniden eğitmenin hareket ettirdiğinin iki katından fazladır. Aynı "
     r"açıklık CIFAR-100'de $5{,}96$, SVHN'de $0{,}65$ puandır.",
     "TR A1 manset ayristirmasi"),

    # ---------- B2 + B3: bootstrap GA ve TOST yonu ----------
    (D,
     r"Eşleştirilmiş bootstrap GA $[7{,}33; 9{,}22]$, her tohumda işaret çevirme "
     r"permütasyonu $p<5\times10^{-5}$ ve TOST eşdeğerliği üç marjın üçünde de "
     r"($\pm1$, $\pm2$ ve $\pm3$ puan; her birinde $p=1{,}0$) reddedilir.",

     r"Her koşunun kendi eşleştirilmiş bootstrap GA'sı vardır ($[7{,}61;\ 9{,}44]$, "
     r"$[7{,}10;\ 9{,}01]$ ve $[7{,}28;\ 9{,}20]$); bunları uç noktalarının "
     r"ortalamasıyla, $[7{,}33;\ 9{,}22]$ ile özetliyoruz. Bu, üç aralığın bir "
     r"betimlemesidir, kapsama garantisi olan bir aralık değildir; koşum düzeyinde "
     r"yapılan çıkarım için koşumlar arası $t$ aralığı $[7{,}68;\ 8{,}86]$'dır. "
     r"İşaret çevirme permütasyonu $p$ değeri her tohumda $5\times10^{-5}$'in "
     r"altındadır ve TOST üç marjın hiçbirinde ($\pm1$, $\pm2$, $\pm3$ puan; her "
     r"birinde $p=1{,}0$) eşdeğerliği kuramamaktadır; aralık $\pm3$'ün tamamen "
     r"dışında kalmaktadır.",
     "TR B2+B3 GA ve TOST"),

    # ---------- A4: SVHN provenansi ----------
    (D,
     r"Bu uydurmanın havuzu ön kayıtta sabitlenen havuzdur; ön kayıt SVHN çiftini "
     r"uydurulan noktalara değil bağımsız bir tutarlılık kontrolüne atamaktadır. "
     r"Temiz hata farkı iki puanın altında kalan ve $x$ ekseninin başka türlü boş "
     r"olan bir bandına düşen iki SVHN yönü eklendiğinde dört protokollü eğim "
     r"$-0{,}133$'e gitmekte ve küme bootstrap güven aralığı "
     r"$[-0{,}570;\ +0{,}469]$ sıfırı içermektedir; üç protokollü eğim ise hem "
     r"işaretini hem aralığını korumaktadır. Bu duyarlılığı içeri almak yerine "
     r"raporluyoruz, çünkü dört protokollü eğimin ne kadar ince bir dayanağı "
     r"olduğunu göstermektedir.",

     r"Bu uydurmanın havuzu SVHN çiftini dışarıda bırakmaktadır ve bu dışlamanın "
     r"nasıl doğduğunu kayda geçiriyoruz, çünkü ön kayıtta yazan bu değildir: ön "
     r"kayıt SVHN'i uydurulan kola koymuş ve $x$ ekseninde on iki puanın altındaki "
     r"boş bandı dolduracak çift olarak adlandırmıştır; bağımsız bir tutarlılık "
     r"kontrolüne atanması ise SVHN sonucu elde edildikten sonra yazılmıştır. "
     r"Dolayısıyla SVHN'i içeren uydurmayı ön kayıtlı olan sayıyoruz. İki SVHN "
     r"yönü eklendiğinde dört protokollü eğim $-0{,}133$'e gitmekte ve küme "
     r"bootstrap güven aralığı $[-0{,}570;\ +0{,}469]$ sıfırı içermektedir; üç "
     r"protokollü eğim ise işaretini de aralığını da korumaktadır ($+0{,}470$, GA "
     r"$[+0{,}361;\ +0{,}665]$). Bu nedenle dört protokollü eğimi geri çekiyoruz; "
     r"mekanizma iddiası, havuz sorusunu aşan ve "
     r"Bölüm~\ref{subsec:statistics_results}'e taşınan üç protokollü eğime "
     r"dayanmaktadır.",
     "TR A4 SVHN provenansi"),

    # ---------- mekanizma ayrinti sikistirmasi ----------
    (D,
     r"Başarılı kaynak oranı $18$ çiftin $12$'sinde dördün en küçüğü, $4$ çiftte "
     r"daha en büyüğüdür; yani $16$ çiftte uçtur. Ortalama açıklığı en büyük olan "
     r"protokol çifti hedef doğru ile başarılı kaynak arasındadır ($23{,}77$ puan) "
     r"ve bu çift $18$ yönün $13$'ünde en geniştir; kalan beşinde, ki hepsi "
     r"CIFAR-100'dedir, uçtaki protokol koşulsuz orandır. Kaynak başarısıyla "
     r"koşullama \emph{kaynağın} kendi gürbüzlüğüne göre seçim yapar; bu, çiftin "
     r"temiz doğruluk farkının bir fonksiyonu değildir ve dolayısıyla ikinci, "
     r"kısmen ters yönlü bir terim katmaktadır.",
     r"Başarılı kaynak oranı $18$ çiftin $16$'sında dördün ucudur ve en geniş "
     r"protokol çifti hedef doğru ile başarılı kaynak arasındadır ($23{,}77$ puan "
     r"ortalama açıklık, $18$ yönün $13$'ünde en geniş). Kaynak başarısıyla "
     r"koşullama \emph{kaynağın} kendi gürbüzlüğüne göre seçim yapar; bu, çiftin "
     r"temiz doğruluk farkının bir fonksiyonu değildir ve ikinci, kısmen ters "
     r"yönlü bir terim katmaktadır.",
     "TR mekanizma ayrinti"),

    # ---------- B5: A kolu kaldirac ----------
    (D,
     r"kontrollü kolun eğimi ise erken kontrol noktaları çıkarıldığında ayakta "
     r"kalmaktadır (eşiklere göre $+0{,}201$ ile $+0{,}492$ arasında) ve en "
     r"kararlı nicelik üç protokollü eğimdir ($0{,}661$ ile $0{,}673$).",
     r"kontrollü kolun dört protokollü eğimi ise erken kontrol noktaları "
     r"çıkarıldığında işaretini korumakta ama büyüklüğünü korumamakta, eşiklere "
     r"göre $+0{,}201$ ile $+0{,}492$ arasında gezinmektedir; kendi aralığı "
     r"$[+0{,}219;\ +0{,}371]$ bu aralığı kapsamamaktadır. En kararlı nicelik üç "
     r"protokollü eğimdir ($0{,}661$ ile $0{,}673$).",
     "TR B5 A kolu kaldirac"),

    # ---------- A2: TRADES ozdesligi ----------
    (D,
     r"Bu sonucu daha önce bir Pearson korelasyonu olarak ifade etmiştik (üç "
     r"hedeften gelen altı yön üzerinde $r = 0{,}997$)",
     r"Cebirin kendisi yeni değildir. Bir kaynak-hedef çifti yerine tek bir model "
     r"üzerine yazıldığında $r_{\text{ham}} = e + r_{\text{koş}}(1 - e)$, "
     r"TRADES'in~\cite{zhang2019theoretically} doğal-artı-sınır ayrıştırmasıdır; "
     r"orada bizim $p$'mize karşılık gelen öncül tanım gereği sağlanır, çünkü "
     r"sınır terimi tedirginlik komşuluğu üzerinde bir varlık niceleyicisiyle "
     r"tanımlanmıştır. Burada yeni olan, transfer ortamında öncülün tanımsal "
     r"olmamasıdır: kaynakta üretilmiş sabit bir tedirginlik hedefin temiz "
     r"hatasını ya korur ya korumaz, dolayısıyla $p$ görgül bir nicelik hâline "
     r"gelir ve biz onu varsaymak yerine ölçüyoruz. Bu sonucu daha önce bir "
     r"Pearson korelasyonu olarak ifade etmiştik ($r = 0{,}997$)",
     "TR A2 TRADES"),

    (D,
     r"ve bu ifade sonucu olduğundan zayıf göstermekteydi:",
     r"; bu ifade sonucu olduğundan zayıf göstermekteydi:",
     "TR A2 baglac"),
]

if not uygula(YAMALAR, ROOT):
    sys.exit(1)
