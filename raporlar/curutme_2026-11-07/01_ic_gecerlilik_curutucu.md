# B1 iç geçerlilik kolu, çürütücü raporu (opus-curutucu, 07.11.2026)

Teslimat: `raporlar/curutme_2026-11-07/01_ic_gecerlilik.md` ve `01_bulgular.json` (17 bulgu, birinci tur).

Karar: duzeltilmeli.

Yürütücünün sayılarının büyük çoğunluğu kaynağıyla birebir tutuyor. Hesap mantığı da dondurulmuş `experiments/q1_konsey_ayrisim.py` ile uyumlu: r_ij, tau_ij, bölünmüş yarı ve ρ_m = −ort r_mc işareti aynı. Buna karşın üç major bulguda sonucu değiştiren hata var. B1-03'teki "%12 ile 88" yanlış hesaplanmış. B1-04'ün yorumu yürütücünün kendi JSON çıktısıyla çelişiyor. B1-02'nin önerdiği kapatan işin çoğu makalede zaten yapılmış ve rapor bunu söylemiyor.

## Sorunlar (önce sonucu değiştirenler)

1. B1-03, major, `01_ic_gecerlilik.md:33` ve `:191`. "Karıştırıcının payı yüzde 12 ile 88 arasında" yanlış. %12, kendi CNN'lerimizden kurulan doğruda açıklanmadan kalan pay (0,043/0,364); karıştırıcının payı değil. `ayrisim.json` `f_sigma_temiz_dogruluk` verisinden yeniden hesaplandı: tüm-CNN doğrusunda V-scr artığı −0,203, yani doğruluğun payı kabaca %44; R224-scr'nin kendi artığı (−0,082) da düşülürse %67; kendi CNN doğrusunda %88. Doğrusu "yaklaşık %44 (ya da %67) ile %88 arası". Bu bulguyu güçlendiriyor; aynı satırdaki "yaklaşık yarısı açıklanmaz" cümlesi de düzeltilmeli. Ayrıca kendi CNN doğrusunun x aralığı 83,34-89,69 değil, 85,11-86,35; 1,24 puanlık aralıktan 12 puan dışa değerleme yapılıyor ve yedi noktanın ikisi ImageNet başlatmalı R224-IN. Hakem cümlesindeki "predicts ... to within 0.04" aşırı güçlü; cümle ya iki doğruyu birlikte vermeli ya da dışa değerlemeyi açıkça yazmalı.

2. B1-04, major, `:43`, `:45` ve `:190`. "Sıfırdan ViT-Tiny kendi tohumları dışında herkese uzaktır" cümlesini aynı JSON çürütüyor. `b_capraz_benzerlik`: V-scr ile V-IN arası −0,798; V-scr ile CNN'ler arası −1,085 (R224-IN), −1,084 (R32), −1,135 (R224-scr), −1,009 (panel). Yani V-scr öbür ViT'ye, eşleşmiş ResNet'ine göre 0,29 ile 0,34 log birimi daha yakın; bu mimari ailesi okumasını destekleyen bir kanıt. Rapor tabloya yalnız V-IN'in tarafından bakıyor. XCiT karşılaştırması da tek başına aile itirazını taşımıyor: XCiT ImageNet ön eğitimli ve panele en yakın model (−0,561); XCiT'e karşı yönlü terim (+0,20) makalede zaten var (`05_discussion.tex:69`, `01_introduction.tex:42`). Bulgu "karışık kanıt" diye yeniden yazılmalı. Kapatan işte tutarsızlık: metin 6 koşu diyor, süre 4 koşuyla hesaplanmış (41 sa); altı koşuyla yaklaşık 61 sa.

3. B1-02, major, `:23` ve `:27`. Önerilen "yönlülük iddiasını her geçtiği yerde 'log ölçekte' diye sınırla" işi büyük ölçüde zaten yapılmış: `main.tex:133` ("A small directional term holds only on CIFAR-10, the log scale and a CNN panel; on the logit scale it is strongly negative"), `01_introduction.tex:42`, `05_discussion.tex:19`; "düşecek cümle" `04_experiments.tex:144` de "on the log scale" kaydını taşıyor. Yeni ve geçerli pay: κ penceresinin darlığı ve Önerme 2'nin h ölçeğiyle birincil ölçek arasındaki gerilim. Dışarıda kalan iki sonuç: H3'ün ±0,10 bandı κ ∈ [−0,7; 0,9] gibi geniş pencerede tutuyor (`olcek.json` `H3_ci90_band_icinde_kappa_min/max`), dolayısıyla "the equivalence claim is a choice of scale" yalnız K-b için doğru; h ölçeğinde H1 −0,134'e iniyor (öngörülen −0,20 büyüklüğünün altında).

4. B1-01, major, `:13`, `:15` ve `:229`. Sayılar doğru (q 0,577; ρ +0,188 [0,166; 0,211]; K-b TOST p 0,996; H3 +0,100, TOST p 0,501; CIFAR-100 q 0,495, ρ +0,287). Eksik bağlam: payda değişiyor. Kaynak açığı G hedef-doğru protokolde 0,391/0,387/0,390 (föy 1580), tutarlı her-ikisi-doğru protokolde 0,711/0,729/0,767 (`her_ikisi_tutarli.json` `cifar10.G`). Simetrik bileşen küçülmüyor, 0,368'den yaklaşık 0,42'ye büyüyor; q'nun düşmesinin tamamı yönlü payın 0,02'den yaklaşık 0,31'e çıkmasından. Okuma "simetrik pay çöktü" değil, "bu protokolde ViT ayrıca yönlü olarak da zayıf kaynak". Ön kayıtla ilişki açık yazılmamış: ön kayıtlı S9-4, `src/analysis/protokoller.py` içindeki `both_correct = tc & sc` tanımına dayanıyor; köşegende sc = tc olduğundan w hedef-doğru kalıyor, yani ön kaydın uygulaması yürütücünün "yarı tutarlı" dediği sürüme (ρ +0,492) denk. Ortak maskeli sürüm savunulabilir ama sapma olarak yazılmalı; "yapay olarak şişirir" gösterilmemiş; w çifte bağlı hale geliyor, bu da yazılmamış. Kısmen metinde: `04_experiments.tex:540` her-ikisi-doğru protokolünde çift düzeyinde yönlü farkın 3,91 puan arttığını raporluyor; `05_discussion.tex:69` ve `04_experiments.tex:154` CIFAR-100 için bu duyarlılığın üretilmediğini yazıyor. Küçük sayı hatası: "T_Vc'nin yaklaşık dörtte biri V'nin temiz hatası" yanlış; föy 1211-1215'e göre 1517/(1517+7061), yaklaşık %18.

5. B1-10, major, `:103` ve `:107`. Süre aritmetiği tutarsız: normalizasyon hücresi önce 16 sa, sonra 8 sa; 16 + 10 = 26 ederken toplam 18 yazılmış; 26 alınırsa genel toplam 273,5. "H2'nin büyük kısmı bu doğruluk kazancıyla gelir" dayanaksız (`d_H1_bolusu` doğrulukla bağ kurmuyor). Geçerli yeni pay: `03_methodology.tex:96` "The bundle is the same for both architectures" ifadesi, DeiT ile RSB-A1 tariflerinin farklılığı karşısında sorgulanabilir.

6. B1-05, major, `:53`. Gerekçe hatalı: V-scr'nin AT LR çizelgesi kosinüs ve T_max = 100 (föy 2450), B3 tavanı 80; kosinüs çizelgesinde tavan her epoktaki LR'yi değiştirir, durma epoğu tavanın altında kalsa da fark sürer. Bu bulguyu güçlendirir. Bulgu önceki konseyin R1 M3 bulgusunun tekrarı (`03_hakem_R1_istatistik.md:39`), metin 03:96'da açıklıyor; yeni pay (çizelge ve donanım) ayrı yazılmalı.

7. B1-06, major, `:63` ve `:65`. Şiddet abartılı: raporun kendi "denenen ama düşmeyen" bölümü Welch-Holm altında üç kararın sürdüğünü söylüyor; 49 katlık varyans oranı 1-2 serbestlik dereceli kestirimlerin uçlarından seçilmiş; "zar zor ayrışmaktadır" sayılarla çelişiyor (gözlenen −0,134, MDE 0,080'in 1,7 katı; föy M12.1 satır 2238 %90 aralığı [−0,180; −0,088], Holm p 0,012). Minor ya da "major, kararları değiştirmiyor".

8. B1-12, minor, `:125`. "two and a half times the run-to-run variance" yanlış: 0,0164/0,0065 = 2,5 standart hatalar oranı; varyans oranı yaklaşık 6,3. `main.tex:133` aralıkların "conditional on test images and panel" olduğunu zaten yazıyor.

9. B1-03 süre, `:37`. "Koşu başına yaklaşık 2 sa" defter sürelerine uymuyor; R224-scr'nin AT aşaması ortalama 3,03 sa; üç koşu 9 sa; asgari paket 64'ten yaklaşık 67'ye çıkar.

10. B1-07, `:77`. ResNet-50/R224 FLOP oranı 8,178/3,627 = 2,25, "2,4 ile 2,55" değil. "ViT'ler için düşük kapasitenin AT başarısını düşürdüğü bilinmektedir" atıfsız. R3 (`03_hakem_R3_uygulanabilirlik.md:109`) ve makale (01:42, 05:23, 05:83) bunu zaten not etmiş.

11. B1-15, `:153`. "PGD-10 ile AA arasında 7 puanlık fark olağan değildir" kaynaksız; kaynak ya da kaldır.

12. B1-16 ve B1-17. Welch köprüsü (`04_experiments.tex:241`) ve ImageNetV2'nin betimsel niteliği (`04_experiments.tex:387`, `05_discussion.tex:23`) metinde zaten var; "düşecek cümle"lerin zaten kayıtlı olduğu belirtilmeli.

13. B1-11, `:113`. Off-diagonal T'yi PGD-10'la bırakıp yalnız w'yi AutoAttack'le değiştirmek farklı bir bölüştürme, duyarlılık değil; sınır yazılmalı.

14. Diğer: `:83` "Kullanıcının sorusunun özü buradadır" yönerge izi. Biçim: 41 paragraf "Kapatan iş:", "Kapatılmazsa düşecek cümle:", "Karar:" etiketiyle açılıyor; yedi "Karar:" paragrafı düzyazıya çevrilmeli.

## Doğrulananlar

κ = 0 satırı föyü yeniden üretiyor. h ölçeğinde ρ −0,316 [−0,327; −0,306]; ρ'nun sıfırı kestiği κ 0,038, bant penceresi [−0,20; 0,25]. B1-04 log τ̄ değerleri tutuyor. 15 sınamalık Holm, Welch p'leri 0,027/0,042/0,026, MDE ve δ taraması tutuyor. GPU-saat toplamı 265,5 ve asgari paket 63,5 aritmetiği doğru; düzeltmelerle (B1-04 altı koşu, B1-10 toplam 26) yaklaşık 294. On yedi "düşecek cümle" alıntısı tex'te birebir bulundu.

## Eksik mercek

1. Hiyerarşik belirsizlik: K-a ve K-b aralıkları üç tohum, df = 2; görüntü örneklemi girmiyor; önceki panel görüntü gürültüsünün tohum yayılımının üç katı olduğunu not etmişti (`birlesik.md:502`). Tohum, görüntü ve panel bileşenlerini birlikte taşıyan aralık istenecektir.
2. Kontrol noktası seçimi ve yakınsama: hücreler 16 ile 38 arası epoklarda doğrulama PGD'siyle seçilmiş; erken durma kuralının σ'yı hücreye göre farklı etkileyip etkilemediği B1-03 ile birlikte sorulacaktır.
3. CNN içi mimari varyansıyla kıyas: panel σ'ları −0,38 ile −0,58; ViT'nin −1,01 sapması CNN'ler arası doğal yayılımla ölçeklenmiş etki büyüklüğü olarak verilirse B1-04'ün aile sorusu ucuzca yanıtlanır.

## Genel değerlendirme

Yürütücü veriye sadık ve istatistik iskeletini doğru sınamış. Manşete karşı kullanılan iki ana bulguda (B1-01 ve B1-04) yorum, aynı çıktılarda duran bağlamı dışarıda bırakıyor: payda iki katına çıkıyor ve V-scr V-IN'e CNN'lerden belirgin biçimde yakın. B1-03'teki aralık yanlış hesaplanmış. B1-02 ile B1-05 makalede zaten kısmen kapatılmış. Bu düzeltmelerle rapor hakem diline uygun ve savunulabilir olur.


# İkinci tur okuması (yalnız değişen kısımlar, 08.11.2026)

Karar: gecer.

B1-01 doğru: q×G tohum başına 0,423/0,415/0,435, yönlü bileşen 0,288/0,314/0,332, ikisi de `her_ikisi_tutarli.json`'dan birebir; %18 = 1517/(1517+7061) (föy 1211-1215); S9-4'ün `protokoller.py:60` tanımıyla yarı tutarlı sürüme denk düştüğü doğru yazılmış. B1-03 doğru: %44, %67 (fark −0,120) ve %88 yeniden hesaplandı; x aralığı 85,11-86,35 ve 12 puanlık dış değerleme yazılmış. B1-04 JSON'la uyumlu (`b_capraz_benzerlik`, `olcekli_etki.json`); hakem cümlesi iki yönü birlikte veriyor. B1-05'te yürütücü haklı, birinci tur bulgusu yanlıştı: föy 2415-2417'ye göre B3 hücreleri de kosinüs T_max 100 çizelgesiyle eğitildi, 80 epokluk tavan yalnız `--stop-epoch` ile uygulandı ve bütün koşular tavanın altında durdu (V-scr 45/38/39, föy 1383-1390; B3 36-58, föy M9.1); minöre inmesi yerinde. B1-07 doğru: 2,4 × 2,97 × 12 = 85,5, iki matrisle yaklaşık 88. `olcekli_etki.json` sayıları doğru: SD 0,102; z V-scr −4,8, V-IN −2,2, XCiT −0,45; H1/SD −3,6. B1-18'de seçilen epoklar ve log τ̄ −1,170/−1,083 föy 1383-1390 ve 1707-1713 ile tutuyor. Toplam 297 GPU-saat doğru (8 eğitim, 5 veri). Uzun tire ve koyu etiket yok.

Geçmeyi engellemeyen iki küçük kalan: (1) `01_ic_gecerlilik.md:187` (B1-18) −0,087 çift düzeyinde log τ̄ farkı, H1 ise model düzeyinde σ karşıtlığı; "H1'in dörtte biri" yalnız büyüklük sırası olarak okunmalı. (2) `olcekli_etki.json` 10 birimlik SD, panel üyelerinin altı üyeyle (kendini dışarıda bırakarak) hesaplanan σ'sını kendi hücrelerin yedi üyeyle hesaplanan σ'sıyla karıştırıyor; notta yazılı, metinde yarım cümleyle anılabilir.

Yardımcı Fable'nin nokta denetimi: B1-01'in sayıları (ρ(V-scr) ortalama 0,1884, %90 aralığı [0,166; 0,211], H3 TOST p 0,5013, q ortalama 0,577, G 0,711/0,729/0,767) `results/q1/curutme_2026-11-07/her_ikisi_tutarli.json` içinde doğrudan açılarak doğrulandı; B1-05 için föy 1383-1385 ve 2414-2434 okundu, yürütücünün gerekçesi doğru bulundu.
