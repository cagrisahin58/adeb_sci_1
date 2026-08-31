#!/usr/bin/env python3
"""TUR 4 FAZ 0 (Turkce aynasi) - Ingilizce tarafla AYNI duzeltmeler."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr")
S = KOK / "sections"

YAMALAR = [
    # ================= 0.1: genel bicim e*p =================
    ("04_deneyler.tex",
     r"genel biçim $r_{\text{ham}} = e\,(1-p) + r_{\text{koş}}\,(1 - e)$ olur "
     r"ve $p=1$ olduğunda Denklem~\eqref{eq:raw_identity}'e indirgenir.",
     r"genel biçim $r_{\text{ham}} = e\,p + r_{\text{koş}}\,(1 - e)$ olur ve "
     r"$p=1$ olduğunda Denklem~\eqref{eq:raw_identity}'e indirgenir. $p<1$ "
     r"olduğunda Denklem~\eqref{eq:raw_identity} sapmayı tam olarak $e\,(1-p)$ "
     r"kadar abartır; yani öncül sağlanmadığında bir eşitlik değil bir üst "
     r"sınırdır.",
     "TR 0.1 genel bicim"),

    # ================= 1.4: p=0,88 nitelemesi =================
    ("04_deneyler.tex",
     r"Transfer çalışmalarının çoğunun saldırdığı standart eğitilmiş "
     r"hedeflerde ise kendi önceki koşumlarımızda $p$ değerini $0{,}88$'e kadar "
     r"inerken gözlemledik; orada özdeşlik bir eşitlik değil bir üst sınırdır.",
     r"Transfer çalışmalarının çoğunun saldırdığı standart eğitilmiş "
     r"hedeflerde ise düzeltme öncesi koşumlarımızda $p$ değerini $0{,}88$'e "
     r"kadar inerken gözlemledik; bunu mevcut boru hattının ölçülmüş bir değeri "
     r"olarak değil bir mertebe göstergesi olarak anıyoruz ve orada özdeşlik "
     r"bir üst sınırdır.",
     "TR 1.4 p=0,88"),

    # ================= 0.2: manset ayrisimi =================
    ("04_deneyler.tex",
     r"Dört tahmin sıralandığında üç bitişik açıklık çıkar: hedef doğru ile her "
     r"ikisi doğru arasında $3{,}91$ puan (yönlü iddialar için onayladığımız ve "
     r"birbirinden yalnızca kaynağın da doğru olmasının gerekip gerekmediğiyle "
     r"ayrılan iki protokol); her ikisi doğru ile koşulsuz oran arasında "
     r"$5{,}31$ puan (aşağıdaki Denklem~\eqref{eq:raw_identity}'in kapalı "
     r"formda öngördüğü ve okurun hedefin temiz hatasını bilerek geri "
     r"alabileceği açıklık); koşulsuz oranla başarılı kaynak oranı arasında "
     r"$5{,}79$ puan (kaynağın kendi beyaz kutu başarısızlığına koşullandığı "
     r"için farklı bir niceliği kestiren protokol). Yalnızca ilki aynı sorunun "
     r"iki savunulabilir okuması arasındaki indirgenemez takdirdir ve $3{,}91$ "
     r"puanla bile iki mimariyi yeniden eğitmenin hareket ettirdiğinin iki "
     r"katından fazladır. Aynı açıklık CIFAR-100'de $5{,}96$, SVHN'de $0{,}65$ "
     r"puandır.",

     r"Koşulsuz oranı eksen noktası alalım: başarılı kaynak oranı onun "
     r"$5{,}79$ puan üstündedir ve kaynağın kendi beyaz kutu başarısızlığına "
     r"koşullandığı için farklı bir niceliği kestirir; hedef doğru oranı ise "
     r"$9{,}21$ puan altındadır ve bu açıklığın tamamı "
     r"Denklem~\eqref{eq:raw_identity}'in kapalı formda öngördüğü paydır, yani "
     r"hedefin temiz hatasını bilen bir okur onu birebir geri alabilir. İkisi "
     r"$15{,}01$ puanın tamamını verir. Düzeltmeden sonra ayakta kalan şey, "
     r"yönlü iddialar için onayladığımız ve birbirinden yalnızca kaynağın da "
     r"doğru olmasının gerekip gerekmediğiyle ayrılan iki protokol arasındaki "
     r"farktır: $3{,}91$ puan, yani iki mimariyi yeniden eğitmenin hareket "
     r"ettirdiğinin hâlâ iki katından fazlası. Bu artık CIFAR-100'de $5{,}97$, "
     r"SVHN'de $0{,}65$ puandır. Eksen yapısı veri kümesine bağlıdır: "
     r"CIFAR-100'de koşulsuz oran dördün en büyüğüdür, dolayısıyla oradaki "
     r"$13{,}58$ puanlık yayılımın tamamı özdeşlik payıdır ve başarılı kaynak "
     r"oranı bu aralığın içine düşer.",
     "TR 0.2 manset ayrisimi"),

    # ================= 0.3: tek birincil =================
    ("03_yontem.tex",
     r"Birincil transfer metriğimiz \emph{koşullu yanıltma oranıdır}: hedef "
     r"modelin temizde doğru sınıflandırdığı örnekler içinde, kaynak modelde "
     r"üretilen çekişmeli örneklerle yanlışa dönenlerin oranı.",
     r"Transfer metriklerimiz, yalnızca koşullama kümesiyle ayrışan bir "
     r"\emph{koşullu yanıltma oranları} ailesidir. Ailenin taban üyesi "
     r"\emph{hedef doğru} oranıdır: hedef modelin temizde doğru sınıflandırdığı "
     r"örnekler içinde, kaynak modelde üretilen çekişmeli örneklerle yanlışa "
     r"dönenlerin oranı.",
     "TR 0.3 metrik ailesi"),

    ("03_yontem.tex",
     r"onu, bir transfer oranı ``başarılı'' çekişmeli örnekler üzerinden "
     r"raporlandığında örtük olarak kullanılan protokol olduğu için dâhil "
     r"ediyoruz.",
     r"onu, bir transfer oranı ``başarılı'' çekişmeli örnekler üzerinden "
     r"raporlandığında örtük olarak kullanılan protokol olduğu için dâhil "
     r"ediyoruz. Yönlü iddialar için birincil tahmin olarak her ikisi doğru "
     r"oranını alıyoruz, çünkü iki yönü de aynı örnekler üzerinde puanlar ve bu "
     r"yüzden eşleştirilmiş çıkarımı destekler; diğer üçü baştan sona onun "
     r"yanında raporlanır.",
     "TR 0.3 birincil tahmin"),

    # ================= 0.4: oksuz sekil =================
    ("04_deneyler.tex",
     r"Saldırı dikkatı hafifçe yeniden yönlendirmekte, ama ne genişletmekte ne "
     r"keskinleştirmektedir.",
     r"Saldırı dikkatı hafifçe yeniden yönlendirmekte, ama ne genişletmekte ne "
     r"keskinleştirmektedir; Şekil~\ref{fig:feature_degradation} üst üste binen "
     r"katman başına eğrileri vermektedir.",
     "TR 0.4 oksuz sekil"),
]

if not uygula(YAMALAR, S):
    sys.exit(1)

# ---------------------------------------------------------------- main.tex
MAIN = [
    ("main.tex",
     "Bu $15{,}01$ puanlık yayılım tek bir şey değildir: $5{,}79$ puanı farklı "
     "bir niceliği kestiren bir protokolden, $5{,}31$ puanı koşullamayı "
     "büsbütün bırakmaktan ve $3{,}91$ puanı ikisi de savunulabilir iki "
     "protokol arasındaki indirgenemez takdirden gelmektedir. Ortadaki pay tam "
     "olarak düzeltilebilir: koşulsuz oranın koşullu orandan sapması, hedefin "
     "temiz hatasının bir eksi koşullu oranla ölçeklenmiş hâline eşittir ve bu "
     "özdeşliğin öncülünü varsaymak yerine ölçüyoruz.",

     "Bu $15{,}01$ puanlık yayılım tek bir şey değildir: $9{,}21$ puanı "
     "koşulsuz oranı hedef doğru orandan ayırır ve türettiğimiz bir özdeşlik "
     "onu kapalı formda kaldırır; $5{,}79$ puanı ise farklı bir niceliği "
     "kestiren bir protokolden gelir. Düzeltmeden sonra ayakta kalan, "
     "onayladığımız iki protokol arasındaki $3{,}91$ puanlık takdirdir. "
     "Özdeşlik, koşulsuz oranın koşullu orandan sapmasının hedefin temiz "
     "hatasının bir eksi koşullu oranla ölçeklenmiş hâline eşit olduğunu söyler "
     "ve onun öncülünü varsaymak yerine ölçüyoruz.",
     "TR 0.2 ozet"),

    ("main.tex",
     r"Yazarlar, hesaplama kaynakları için Fırat Üniversitesi Yazılım "
     r"Mühendisliği Bölümü'ne teşekkür eder.",
     r"Yazarlar, hesaplama kaynakları için Fırat Üniversitesi Yazılım "
     r"Mühendisliği Bölümü'ne teşekkür eder." "\n\n"
     r"Yazarlar bu çalışmanın hazırlanması sırasında Claude (Anthropic) "
     r"kullanmıştır. Araç, makale metninin tüm bölümlerinin yazımına ve "
     r"gözden geçirilmesine ve makaleyle birlikte yayımlanan analiz ve denetim "
     r"betiklerinin gerçeklenmesine yardımcı olmuştur. Çalışmanın tasarımı, "
     r"deney protokolü ve tüm sonuçlar yazarlara aittir; yazarlar raporlanan "
     r"her sayıyı yayımlanan artefaktlarla doğrulamıştır.",
     "TR 1.5 YZ beyani"),
]

# Tesekkur yamasinda eski metin yeninin ONEKIDIR; imzayla korunur.
if "Claude (Anthropic)" in (KOK / "main.tex").read_text(encoding="utf-8"):
    MAIN = [y for y in MAIN if "YZ beyani" not in y[3]]
    print("  [=] TR 1.5 YZ beyani zaten var")

if not uygula(MAIN, KOK):
    sys.exit(1)

# ---------------------------------------------------------- giris ve sonuc
SON = [
    ("01_giris.tex",
     r"Ardından bu yayılımı tek bir sayı olarak bırakmak yerine ayrıştırıyoruz: "
     r"$5{,}79$ puanı farklı bir niceliği kestiren bir protokolden, $5{,}31$ "
     r"puanı koşullamayı büsbütün bırakmaktan (türettiğimiz bir özdeşlik bunu "
     r"kapalı formda düzeltmektedir) ve $3{,}91$ puanı ikisi de savunulabilir "
     r"iki protokol arasındaki takdirden gelmektedir; sonuncusu bile yeniden "
     r"eğitmenin etkisinin iki katından fazladır.",
     r"Ardından bu yayılımı tek bir sayı olarak bırakmak yerine ayrıştırıyoruz: "
     r"$9{,}21$ puanı koşulsuz oranı hedef doğru orandan ayırır ve türettiğimiz "
     r"bir özdeşlik onu kapalı formda kaldırır; $5{,}79$ puanı farklı bir "
     r"niceliği kestiren bir protokolden gelir. Düzeltmeden sonra ayakta kalan, "
     r"ikisi de savunulabilir iki protokol arasındaki $3{,}91$ puanlık "
     r"takdirdir; bu bile yeniden eğitmenin etkisinin iki katından fazladır.",
     "TR 0.2 giris"),

    ("06_sonuc.tex",
     r"Bu $15{,}01$ puanlık yayılım üç parçaya ayrılmaktadır: $5{,}79$ puan "
     r"farklı bir estimand, $5{,}31$ puan bir özdeşliğin kapalı formda "
     r"düzelttiği pay ve $3{,}91$ puan ikisi de savunulabilir iki protokol "
     r"arasındaki gerçek takdir; bir raporlama ölçütünün ele alması gereken de "
     r"sonuncusudur.",
     r"Bu $15{,}01$ puanlık yayılım, türettiğimiz bir özdeşliğin kapalı formda "
     r"kaldırdığı $9{,}21$ puan ile farklı bir niceliği kestiren bir "
     r"protokolden gelen $5{,}79$ puana ayrılmaktadır; düzeltmeden sonra ayakta "
     r"kalan $3{,}91$ puanlık gerçek takdirdir ve bir raporlama ölçütünün ele "
     r"alması gereken de odur.",
     "TR 0.2 sonuc"),
]

if not uygula(SON, S):
    sys.exit(1)
