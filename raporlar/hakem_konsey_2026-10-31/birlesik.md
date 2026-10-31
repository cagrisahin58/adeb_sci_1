<!-- Panel sekreteri (salt okur ajan) bu raporu yapisal ciktisinda dondurdu; ana oturum 31.10.2026'da dosyaya aktardi. -->

# Birleşik hakem raporu ve karar kartı (31.10.2026)

**Hedef:** paper/manuscript (main.tex, macros_konsey.tex, sections/01-07, derlenmiş main.pdf)
**Dergi:** IEEE Access
**Mercekler:** istatistik (BUYUK_REVIZYON), iddia (BUYUK_REVIZYON), sunum (KUCUK_REVIZYON)

**Okuduğum dayanak belgeler:**
- 12_makale_revizyon_brifi.md: §1, §2, §8, §9, §12.4, §13
- 14_makale_revizyon_notu.md: tamamı
- ON_KAYIT_EK_B8_B10_2026-10-30.md: satır 126 ve 195-201
- 13_b10_r18_r50_denetimi.md: §1 ve §6
- Föy satırları: 1532, 1549-1563, 1600-1607, 1812-1818, 1838-1844, 1928-1946, 2005-2011
- _ek_flop_olcumu.json
- Makale satırları: main.tex:62-67 ve 117; 01:16-48; 03:52, 205-242, 260-275, 328; 04:66-70, 143-155, 224-238, 375-389, 435-445, 492-506; 05:17-72; 06 tamamı

Merceklerin aktardığı sayılardan şunları föyle karşılaştırdım ve hepsini doğru buldum:
- K-b(B9) çürütmesi ve "K-b_eski_yalniz_pozitif_okuma_curutme: evet" kaydı (föy 1839, 1842)
- S1'in Welch %90 aralığı [−0.120, +0.119] (föy 1561)
- Logit H3 −0.087 [−0.110, −0.064] (föy 1551)
- XCiT panelinde ρ(V-scr) +0.198 ile +0.204 (föy 1606)
- K-a ve K-b için hiyerarşik bootstrap "bulunamadi" (föy 1607)
- ImageNetV2'de en küçük c_ij 0.003 (föy 2011)
- Mo ViT-B 0.95 puan ve yedek Wong2020Fast 1.20 puan (föy 1814, 1818)
- Birleşik SD 0.0273 ve 0.0169 (föy 1532)
- ViT-Tiny parametre sayısı 5.53M (_ek_flop_olcumu.json)

## 1. Karar ve gerekçe

Kararım BUYUK_REVIZYON. Makalenin ölçüm katmanı sağlam. Bulgunun özü, yani panel kaynak açığının büyük kısmının simetrik olması, bütün ölçeklerde, jackknife'ta, δ = 0.06'da ve iki CIFAR veri kümesinde tutuyor. Ön kayda sadakat ve olumsuz sonuçların açıkça yazılması da bu türde bir makale için ortalamanın üstünde.

Sorun, başlık ve özetin gövdenin kendi kabul ettiği sınırların ötesine geçmesinde. Dört nokta öne çıkıyor:
- Başlıktaki "Not a Weak Source", CIFAR-100'deki K-b çürütmesiyle, XCiT panelindeki ρ +0.20 ile ve çift içindeki r_RV = +0.115 ile sözcüğü sözcüğüne çelişiyor.
- Sıfırdan eğitilmiş ViT'nin büyük benzemezliği, temiz doğruluğu düşük olan tek hücrede ortaya çıkıyor. Bu karıştırıcı gövdede dört yerde kabul ediliyor, ama özette ve başlıkta yok.
- "Necessary condition" ifadesi ek ön kayıt §9'un anlamından kaymış. Makalenin kendi ImageNetV2 verisinde bir karşı örneği var.
- Ön kayıtlı hiyerarşik bootstrap ve aile ayıklamalı Mantel çözümlemesi üretilmemiş. Bu yüzden K-a, K-b ve B10 aralıkları görüntü örneklemini ve aile blok yapısını taşımıyor.

İlk üç nokta yeni sayı gerektirmeden metinle kapanabiliyor. Dördüncüsü yeniden eğitim gerektirmeyen masa hesaplarıyla kapanabiliyor; föyün güncellenmesi gerekiyor. Bu nedenle küçük revizyon yetmez, ama ret gerektiren bir kusur da yok.

Kabul için tek en önemli koşul şu: başlık ve özet, brif §2'nin iddia sınırına çekilmeli. Bu, sıfırdan satırındaki doğruluk karıştırıcısının ve K-b(B9) çürütmesinin özete girmesi demek. Ayrıca K-a ve K-b için ön kayıtlı hiyerarşik bootstrap üretilip kararların değişmediği gösterilmeli.

İddia merceğinin kırmızı bulgusunu (B1) birleşik değerlendirmede sarıya indirdim. Bunun iki gerekçesi var:
- Karıştırıcı gövdede dört yerde açıkça kabul ediliyor (04:238, 05:60, 06:12, 01:42).
- Doğruluğu eşleşmiş iki karşılaştırma işaret değiştirmiyor: V-IN ile R224-IN'in σ ortalamaları −0.739 ve −0.635 (föy 1497, 1499), Singh çiftlerinde −0.142 [−0.197, −0.090] (föy 1938).

Kusur gövdede değil, özet ve başlık düzeyinde. Yine de bir hakemin ilk soracağı kalem budur.

Brifle çelişen dört nokta var ve hepsinde bu panel brifin ilgili yerini aşıyor:
- Brif §1.1 başlığı sabitliyor. Ama brif §2 iddianın üst sınırıdır; "yönlü terim her veri kümesinde ve her panelde küçüktür" iddiasını söylenemez sayıyor. Başlık bu sınırı aştığı için §2, §1.1'den önce gelir.
- Brif §2'nin B10 satırı ve §8.1 m.7 "gerekli koşul" ifadesini taşıyor. Bu, ek ön kayıt §9'un yanlış okunmasıdır. Ek ön kayıt §9'da "τ̄ ile ilişkisi bir mekanizmanın gerekli koşuludur" yazar; yani gerekli olan ilişkidir, hizalanmanın kendisi değildir. Ön kayıt metni briften önce gelir.
- Brif §13'teki kapı önerisi "necessary condition" dizgesini korumalı ifade listesine alıyor. Bu dizge listeden çıkarılmalı.
- Brif §8.1 m.6'daki 1.20 puan matristeki bir modele ait değil; föy 1814'e göre bu değer 0.95 olmalı.

## 2. Bulgular: tekilleştirilmiş, şiddete ve etkiye göre sıralı

Her bulgunun sonunda kaynak merceği ve sınıfı yazılı. "Açık iş" etiketi yeni deney, föy dışı sayı ya da bu turun dışındaki bir aşama gerektiren kısımları gösterir; bunlar §2 sonunda A1-A15 olarak numaralı.

### Sarı (büyük revizyon)

B1. Sıfırdan eğitilmiş ViT'nin büyük benzemezliği temiz doğruluk ve yakınsamayla birlikte değişiyor.
- Sayılar: V-scr 73.53, R224-scr 85.73 temiz doğruluk ve A^σ_scr −0.364 (föy 1496, 1498, 1526). Doğruluk eşleşince fark kabaca üçte bire iniyor: Singh çiftleri −0.142, üst uç −0.090 (föy 1938); V-IN ile R224-IN için −0.739 ile −0.635.
- H2 de aynı karıştırıcıyla hizalı. Başlatma, ViT'nin temiz doğruluğunu ResNet'inkinden çok daha fazla artırıyor (föy 1496-1499).
- Gövde bunu kabul ediyor, özet ve başlık etmiyor. 04:238'deki "argues against reducing the dissimilarity to accuracy alone" cümlesi, aralığı olmayan ve kayıtlı olmayan tek bir karşılaştırmaya dayanıyor.
- Kaynak: iddia (kırmızı), istatistik (yeşil, V-IN ile R224-IN).
- Sınıf: uygulanır (metin). Özete karıştırıcı yan cümlesi girer, başlık B2 ile daraltılır, 03:275'e niteleme eklenir, 04:238 yumuşatılır, 05:21 daraltılır.
- Açık iş kısmı: A1 (doğruluğu eşleşmiş sıfırdan ViT hücresi), A2 (föy eki M9.10), A3 (σ'nın temiz doğruluğa masa regresyonu). Fark sayısı −0.104 brif §9 gereği föye girmeden yazılmaz.

B2. Başlık ve özetteki "zayıf kaynak" iki niceliği karıştırıyor ve K-b(B9) çürütmesini yumuşatıyor.
- "Not a Weak Source", birincil log ölçekte üç durumda çürüyor: çift içinde r_RV +0.115 (föy 1708), CIFAR-100'de ρ +0.143 ile çürütüldü (föy 1839), XCiT panelinde +0.198 ile +0.204 (föy 1606).
- Özetteki "does not [replicate]" ifadesi, "kararsız" ile "çürütüldü" arasındaki farkı siliyor. Brif §2'nin B9 satırı bunu açıkça yasaklar.
- Föy 1842, çürütmenin özgün tek yönlü kuralla da çıktığını gösteriyor. Bu bilgi metinde kullanılmamış.
- Kaynak: istatistik (sarı), iddia (sarı).
- Sınıf: uygulanır. Başlık "Less a Weak Source than a Different One" olur. "Weak source" yöntemde bir kez tanımlanır. Özet çürütmeyi açıkça yazar. 05:33'e r_RV'nin δ'yı aştığı eklenir. 03:328'e föy 1842 yan cümlesi girer.
- Kapı notu: check_pdf_render yeni başlık dizgesiyle güncellenmeli (A15).

B3. "Necessary condition" iddiası mantıksal olarak yanlış ve makalenin kendi verisiyle çelişiyor.
- Yüksek bir sıra korelasyonu gerekliliği sınamaz.
- Salman R18 ile R50 çiftinde c_ij matrisin en küçük değeri (0.003; föy 2011), ama bu çiftin transfer benzerliği yüksek. 13_b10_r18_r50_denetimi.md §6 değeri gerçek buluyor; ilgili log τ̄ 11_sonuc §6'da.
- İfade yedi yerde geçiyor: main 117, 01:42, 03:260, 04:445, 04:480 altyazısı, 05:21, 06:14.
- Kaynak: istatistik (sarı), iddia (sarı), sunum (tekrar).
- Sınıf: uygulanır. İfade "an association that a gradient-alignment account requires, but not evidence of a mechanism" çizgisine çekilir. Karşı örnek sayısız ya da föydeki 0.003 ile kurulur.
- Açık iş kısmı: A4 (0.0034 ve −0.936 föye alınacaksa), A15 (kapı listesinden çıkarma ve brif düzeltmesi).

B4. K-a ve K-b aralıkları görüntü örneklemini taşımıyor; ön kayıtlı hiyerarşik bootstrap üretilmemiş.
- Föy 1607 bu satırı "bulunamadi" diye kaydediyor. Görüntü bootstrap SD'si 0.030, koşum SD'si 0.010 (föy 1706, 1722).
- 04:70'teki "agree to within image noise" yan cümlesi kanıt değil.
- 14_makale_revizyon_notu.md'deki bulgu 21 bunu zaten açık iş olarak bırakmıştı.
- Kaynak: istatistik.
- Sınıf: uygulanır (özette aralık türünün niteliği ve 04:70) ve açık iş A5.

B5. Mantel sınamasında aile blok yapısı ayrılmıyor; S10-3 üretilmemiş.
- Toplamsal artıklama blokları ayırmıyor. Etiket permütasyonu blokları karıştırıyor.
- Aile ayıklamalı Spearman 11_sonuc §7'de var, ama föyde yok (brif §9).
- 14_makale_revizyon_notu.md'deki bulgu 22'de birinci yol açık kalmıştı.
- Kaynak: istatistik.
- Sınıf: uygulanır (özette ve 04:437'de niteleme) ve açık iş A6.

B6. Saldırı yetersizliği açıklaması yalnız PGD'ye çok yakın saldırılarla sınanmış.
- MI ile PGD arasındaki fark +0.015 ile +0.018 (föy 1638-1640).
- Uyarlanmış TGR, PGD'den 0.147 ile 0.218 log birimi daha kötü transfer ediyor (föy 1648). Bu, TGR'nin yayımlanmış amacının tersi; uyarlamanın doğrulaması da yok.
- Naseer ve ark.'nın yöntemi hiç koşulmamış.
- Kaynak: iddia.
- Sınıf: uygulanır (özet, 01:32, 05:21, 05:68 ve 06:12 daraltılır) ve açık iş A7, A8.

B7. Özetteki "architecture leaves direction unchanged" cümlesi işaret değiştiren bir etkileşimi ana etki ortalamasıyla örtüyor.
- 04:230 bunu kabul ediyor; özet, 01:32 ve 06:12 etmiyor.
- Basit etkiler (+0.070, −0.064) ve etkileşim (−0.134) brif §9 gereği föye girmeden yazılamaz.
- Kaynak: iddia.
- Sınıf: uygulanır (sayısız "averaged over initialization" nitelemesi). Sayılar açık iş A2.

B8. "Sign reverses" dili sıfıra eşdeğer bir kestirim için kullanılıyor ve H3'ün logit sonucu iki yerde çelişik niteleniyor.
- Log ρ(V-scr) +0.012 [−0.007, +0.031], yani sıfıra eşdeğer. Logit H3 −0.087 ve bandın içinde (föy 1551).
- 04:494'teki "H3 reverses in the same way", 04:230 ile çelişiyor.
- 14_makale_revizyon_notu.md'deki bulgu 20, altyazının ve 04:494'ün "large and negative" kalıbına geçtiğini kaydediyordu. Bu iki yer o kayda uymuyor.
- Kaynak: istatistik (yeşil), iddia (yeşil), sunum (sarı). Üç mercek ayrı ayrı gördüğü için sarı.
- Sınıf: uygulanır.

B9. Simetrik pay q'nun okunuşu eksik.
- Bir kaynak ana etkisi r'ye tam olarak, log τ̄'ya yarı ağırlıkla girer. Saf bir kaynak etkisi bu yüzden q = 0.5 verir; bu da K-a'nın sıfır hipotezidir. Cebri denetledim, doğru.
- K-c'deki tür içi benzerlik (ViT −0.443, ResNet −0.489; föy 1595), genel bir kaynak zayıflığına karşı en güçlü argüman, ama metinde kullanılmamış.
- Kaynak: iddia.
- Sınıf: uygulanır (Önerme 1(d), σ tanımına not, 04:151'e bir cümle). Türetilmiş 2q − 1 sayısı açık iş A9.

B10. Özetteki "three seeds" ve "pre-registered" ifadeleri ile S1 köprüsünün Welch aralığı.
- Yeni hücrelerde ikişer koşu var.
- S1'in Welch %90 aralığı [−0.120, +0.119], ±0.10'u aşıyor (föy 1561).
- CIFAR-10 panel öngörüleri görülmüş ilk tohumun genişletilmesi (03:328).
- Kaynak: istatistik (sarı), iddia (yeşil).
- Sınıf: uygulanır.

B11. CNN paneli büyük ölçüde ResNet-18 türevlerinden oluşuyor.
- Yedi üyenin dördü ResNet-18 türevi. Aile düzeyinde bir dışlama duyarlılığı yok.
- Kaynak: iddia.
- Sınıf: uygulanır (panelin tanımı ve 04:499 genellemesi) ve açık iş A10.

B12. Demontis çerçevesi iki terimli özetlenmiş; Awad atfı ters bağlamda.
- Demontis ve ark.'nın vekil karmaşıklığı terimi düşmüş. Bu terim, makalenin çürüttüğünü söylediği kaynak etkisinin ta kendisi.
- "Robust surrogates transfer better" bir kaynak niteliği bulgusu ve 05:21'deki benzerlik cümlesini desteklemiyor.
- Kaynak: iddia.
- Sınıf: uygulanır. Awad, Springer ve Zhang anahtarları atif-kontrol turunda doğrulanmalı.

B13. Gösterim çakışmaları.
- A^σ_scr ve A^ρ ImageNetV2'de başka nicelikler için kullanılıyor. Ek ön kayıt satır 126 zaten A^σ_scr,Liu yazıyor.
- A^ω tanımsız.
- Pearson korelasyonu çıplak r ile yazılıyor.
- Kaynak: sunum.
- Sınıf: uygulanır.

B14. ω ve L_k yüzde biriminin logaritması, ama bu hiçbir yerde yazılmıyor.
- ln(55.91) = 4.024; denetledim.
- Kaynak: sunum.
- Sınıf: uygulanır (bir cümle ve eksen notu). Oran ölçeğine çevirme önerisi reddedildi (R3).

B15. Şekil kusurları.
- Renk çubuğunun .1f biçimi −0.25'i −0.2, −1.25'i −1.2 diye basıyor.
- fig_source_gap_split göstergesinde hâlâ D yazıyor. Negatif yönlü pay sıfırın altına çizilmiş; çubuğun tepesi 0.167, gerçek toplam 0.122 (föy 1930).
- 14_makale_revizyon_notu.md'deki bulgu 24 bu kısmı şekil ajanına bırakmıştı.
- Kaynak: sunum.
- Sınıf: uygulanır (şekil ajanı).

B16. Önerme numaralandırması brif §3.1'in tersine basılıyor.
- Tanımlanabilirlik Proposition 2, h ölçeği Proposition 1 olarak çıkıyor.
- G ve P tanımlanmadan III-B'de kullanılıyor.
- Kaynak: sunum.
- Sınıf: uygulanır.

B17. Özet sembol yüklü ve kendi başına okunmuyor.
- Δ_seed, w, τ̄ ve r sembolleri özette açıklanmadan geçiyor.
- "PGD-10 gaps" ifadesi tanımsız; karşılaştırma nesnesi belirsiz.
- Kaynak: sunum.
- Sınıf: uygulanır (§3'teki özet taslağı).

B18. Kelime bütçesi ve tekrar.
- 03 dosyası 3900 kelimeyle 3400 tavanının üstünde.
- Sınır cümlesi altı kez, "necessary condition" sekiz kez geçiyor.
- Kaynak: sunum.
- Sınıf: kısmen uygulanır. Tekrarlar ayıklanır; B3 düzeltmesi tekrarın çoğunu zaten kaldırıyor. Ön kayıt beyan paragrafının eke taşınması reddedildi (R1). Giriş katkılarındaki sayıların teke indirilmesi de reddedildi (R2).

### Yeşil (küçük revizyon)

m1. Logit ölçekte de ±0.10 bandının kullanılması kayıtlı değil (ön kayıt §5 satır 50). Orman şeklinde de logit satırlarının üstüne aynı bant çizilmiş. Kaynak: istatistik. Sınıf: uygulanır.

m2. ImageNetV2 betimsel sonucuna çıkarım dili sızıyor.
- 0.864 değeri ek ön kayıt §5.6 gereği dipnotta olmalı.
- 04:497'deki XCiT cümlesi tek üyeli bir referansa dayanıyor ve aralık taşımıyor.
- Kaynak: istatistik. Sınıf: uygulanır.

m3. 06:12'deki "none of the new models shows signs of gradient masking" ifadesi kuralın ötesine genelleniyor. Kaynak: istatistik. Sınıf: uygulanır.

m4. 03:272 ve 03:275'teki karar ilkesi eksik anlatılıyor; δ'nın σ karşıtlıkları için bir uzlaşım olduğu yazılmamış. Kaynak: istatistik. Sınıf: uygulanır.

m5. 1.20 puan, matriste olmayan yedek modele ait.
- 04:377 "every candidate" dediği için teknik olarak doğru. Yalnız açıklama eklenir; "bu ifade hatalı" okuması reddedildi (R6).
- 05:72'de 0.95 yazılır.
- Kaynak: istatistik. Sınıf: uygulanır.

m6. Orman şeklinde koşu düzeyindeki aralıklar ile yalnız görüntü bootstrap'ından gelen aralıklar aynı kalınlık koduyla çizilmiş. Kaynak: istatistik. Sınıf: uygulanır (altyazı).

m7. 04:155'teki SVHN yan cümlesi yönlü terime kanıt gibi okunuyor. Brif §2'nin istediği bu cümle korunur, ama bağlam olarak kurulur. Kaynak: iddia. Sınıf: uygulanır.

m8. 05:19 ve 05:21'in ilk cümleleri, ölçek ve veri kümesi kaydı gelmeden genelleniyor. Kaynak: iddia. Sınıf: uygulanır.

m9. 05:33 ve 01:48'deki tez uzlaşmasında Önerme 1(b)'nin ölçek kaydı ve gönderme eksik. Kaynak: iddia. Sınıf: uygulanır (makale tarafı). Tezdeki AS1 yanıtının hizalanması açık iş A11.

m10. ViT-Tiny 5.7M değil 5.5M parametre taşıyor (03:52, Tablo I). Kaynak: iddia. Sınıf: uygulanır.

m11. 04z:15'teki "involved no training" ifadesi belirsiz. Kaynak: iddia. Sınıf: uygulanır.

m12. 05:38'deki Mahmood aday açıklaması ölçeğe bağlı. Kaynak: iddia. Sınıf: uygulanır.

m13. tab:registry'de H10 ve H10k etiketleri, kullanılmayan aile sembolleri ve q̄. Kaynak: sunum. Sınıf: uygulanır. Etiketler ek ön kayıttan geldiği için korunur ve tab:mantel'e aynı etiketler konur; yeniden adlandırma reddedildi (R5).

m14. Standart sapma ve p değeri yazımı tablolar arasında tutarsız. Kaynak: sunum. Sınıf: uygulanır.

m15. Altyazı ile panel harfleri uyumsuz; şematikte panel ortalaması ile τ̄ aynı üst çizgiyle gösterilmiş; CIFAR-100 etiketleri yanlış. Kaynak: sunum. Sınıf: uygulanır (altyazı yazarda, şekil ajanda).

m16. fig_protocol_sets'te metinde olmayan terimler var ("endorsed pair", "different estimand"). Kaynak: sunum. Sınıf: uygulanır (şekil ajanı).

m17. tab:external_pool iki tabloyu tek gövdede birleştiriyor; ileri göndermeler uzak; 04:56 cümlesi 03:79'u yineliyor. Kaynak: sunum. Sınıf: uygulanır.

m18. Katkı paragrafları üç ayrı kalıpla açılıyor. Kaynak: sunum. Sınıf: uygulanır.

Kalan üç sunum bulgusu bu turun dışında olduğu için açık işe gitti:
- Yazı boyutları ve genel bakış şeklindeki ok: A12, visio-cizici turu.
- IEEE Access biyografisi ve düz şekil yolları: A13, gönderim paketi.
- 07:137 ve 07:144'teki TODO(foy) yorumları: A14.

### Reddedilen alt öneriler

- R1. Ön kayıt beyan paragrafı (03:326-330) eke taşınmaz. Görülmüş veri ve kural değişikliği beyanları makalenin en güçlü dürüstlük unsurudur ve gövdede kalmalıdır; 14_makale_revizyon_notu.md'deki bulgu 27'nin gerekçesi de bu yöndedir. Bütçe başka yerden kısılır.
- R2. Giriş katkılarındaki sayılar teke indirilmez. Katkı paragraflarının sayıları brif §4.2'de bilinçli olarak belirlenmiş. Yalnız 01:32'deki saldırı ve maskeleme ayrıntıları kısaltılır.
- R3. ω ve L_k oran ölçeğine çevrilmez. Bu, föyle eşleşen bütün tablo değerlerini değiştirirdi; birim notu yeterli.
- R4. "Necessary condition" ifadesi Taylor argümanıyla korunmaz. Makalenin kendi karşı örneği varken türetme yükü üstlenmeye değmez.
- R5. H10 ve H10k "G-raw" ve "G-res" diye yeniden adlandırılmaz. Bunlar ek ön kaydın etiketleri; bağlantı kopar.
- R6. 04:377'deki 1.20 puan hatalı sayılmaz. "Every candidate" ifadesi doğru; yalnız açıklama eklenir.

### Açık işler

Ana oturum için önerilen sıra:

| No | İş | Gerek | Kimin işi |
|---|---|---|---|
| A2 | Föy eki M9.10. Birleşik varyanslı aralıklarıyla hücre karşıtlıkları: σ(V-IN) − σ(R224-IN), σ satır farkları, ρ basit etkileri ve ρ etkileşimi. | GPU yok | kod-mimar, build_reference_sheet.py |
| A5 | CIFAR-10 ve CIFAR-100'de K-a ve K-b için ön kayıtlı hiyerarşik bootstrap (B = 2000). Mevcut örnek bazlı npz kayıtlarından föye; tab:panel_tests'e duyarlılık satırı olarak. | GPU yok | kod-mimar |
| A6 | S10-3, yani aile göstergeli kısmi Mantel, ve aile içinde kısıtlı permütasyonlu Mantel. 11_sonuc §7'deki aile ayıklamalı ve yalnız CNN-CNN Spearman değerleri M10.7 olarak föye; tab:mantel'e bir satır. Keşifsel etiketle. | GPU yok | kod-mimar |
| A9 | Türetilmiş satır: 2q − 1 ("dissimilarity share"). | GPU yok | kod-mimar |
| A3 | Yirmi modelli CIFAR-10 matrisinde σ'nın temiz doğruluğa regresyonu ve V-scr'nin CNN eğilim çizgisinden sapması. Keşifsel. | GPU yok | kod-mimar |
| A10 | ResNet-18 türevleri çıkarılmış üç üyeli panelle (Engstrom RN-50, Carmon ve Gowal WRN-28-10) q, ρ(V-scr) ve H1. Keşifsel. | GPU yok | kod-mimar |
| A4 | Salman R18 ile R50 çifti için c 0.0034 ve log τ̄ −0.936 föye. İsteğe bağlı: metin sayısız ya da föydeki 0.003 ile kurulabiliyor. | GPU yok | kod-mimar |
| A15 | Kapı ve brif güncellemesi. check_manuscript_claims için önerilen korumalı ifade listesinden "necessary condition" çıkarılır, "refuted" kalır. check_pdf_render yeni başlığı arar. Brif §2'nin B10 satırı, §8.1 m.6 (1.20 yerine 0.95) ve m.7 düzeltilir. | GPU yok | kod-mimar, ana oturum |
| A7 | TGR uygulamasının, temiz eğitilmiş ViT-Tiny'den CNN'e transferde yayımlanmış yönü verdiğinin doğrulanması. | kısa GPU | deney |
| A1 | Doğruluğu eşleşmiş, sıfırdan eğitilmiş ViT hücresi (CIFAR'a özgü 4×4 yamalı ViT-Tiny ya da uzatılmış temiz aşama, temiz doğruluk en az %83). İki tohum, ön kayıt eki, aynı panel. | GPU, en pahalısı | deney, ek ön kayıt |
| A8 | Genişletilmiş saldırı kümesi: Naseer self-ensemble ve token refinement ya da PNA, artı DI/TI 50 adım. Ek ön kayıtla, keşifsel. | GPU | deney |
| A11 | Tezdeki AS1 yanıtının "yönün yaklaşık yarısı hedef kırılganlığı; temiz doğruluk eşleşince yön kararsızlaşır" biçiminde hizalanması. | yok | tez oturumu |
| A12 | Yazı boyutu en az 6.5 pt; genel bakış şeklinde (c)'den (d)'ye giden okun düzeltilmesi. | yok | visio-cizici |
| A13 | Gönderim paketi: düz şekil yolları ve ikinci yazarın biyografisi. | yok | gönderim |
| A14 | 07:137 ve 07:144'teki iki değer ya föye eklenir ya da yorum satırları silinir; 07:138'deki "essentially unchanged" sayısız kalır. | yok | ana oturum |

A2, A3, A4, A5, A6, A9 ve A10'un hepsi yeniden eğitim gerektirmiyor. En az emekle en çok işi görecek yol, bunların tek bir kod-mimar işinde föye girmesi. A1 ve A8 yapılmazsa §3'teki metin daraltmaları yeterli kabul edilebilir; A7 ucuzdur ve B6'nın en zayıf noktasını kapatır.

## 3. Uygulanacak düzeltmeler: dosya dosya (yazar talimatı)

Rol dağılımı brif §13'teki gibidir:
- Y1: main.tex, 01, 06
- Y2: 02, 03
- Y3: 04, 07
- Y4: 05, 04z
- Şekil ajanı: paper/figures/konsey

Bu turda föy değişmez. A2-A10 föye girene kadar aşağıdaki cümleler sayısız kalır. Satır numaraları 31.10.2026 dosyalarınındır.

### main.tex (Y1)

**Satır 65-67, başlık.** \title{Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design}. Brif §1.1'den bu tek sapma, §2 gerekçesiyle yapılır; 62-64'teki yorum satırına tarihli bir not eklenir.

**Satır 117, özet.** Aşağıdaki taslakla değiştirilir. Elle sayımla yaklaşık 249 kelime. check_abstract_body yeniden koşulur. Taslaktaki her sayı gövdede var; 4.36 ile 19.37 cümlesi brif §1.2 kuralı gereği ilk kesilen cümle olarak çıktı ve protokol katmanı katkı 4'te kalır.

> Adversarially trained ViTs look like weak transfer sources against CNNs, but two models cannot split this asymmetry between source and target. We factor each log target-correct transfer rate into target vulnerability, symmetric similarity and a directional residual, averaged over a fixed panel of seven robust ResNet-family CNNs, and test registered predictions with two or three runs per cell (brackets: 90\% run-level intervals). On CIFAR-10, 0.936 [0.925, 0.948] of ViT-Tiny's panel source gap to ResNet-18 is symmetric, the ViT's directional term ($+0.012$) is equivalent to zero within $\pm0.10$, and ViT seeds are closer to each other than to the panel ($+0.566$). In an architecture-by-initialization design on a matched pipeline, the scratch-trained ViT is less similar to the panel than the ResNet ($-0.364$ [$-0.415$, $-0.314$]), a contrast confounded with its lower clean accuracy; ImageNet initialization narrows it more for the ViT ($+0.260$ [0.186, 0.335]); averaged over initialization, architecture leaves the log directional term within $\pm0.10$ ($+0.003$). The gap is retained under PGD-10, momentum PGD and an adapted token gradient regularization (0.960), and AutoAttack flags no new model for masking. On CIFAR-100 the symmetric share (0.840) and seed similarity replicate, but equivalence of the ViT's directional term is refuted ($+0.143$), and it is strongly negative on the logit scale, so a small directional term holds only on CIFAR-10, the log scale and a CNN panel. On ImageNetV2, transformers in two same-recipe pairs are descriptively less similar to the panel ($-0.142$), and input-gradient cosine tracks similarity on three datasets (Spearman 0.893--0.944 after additive model effects are removed).

### sections/01_introduction.tex (Y1)

**Satır 16.** "and the difference between directions comes from how vulnerable each target is" yerine şu yazılır: "and the asymmetry within the pair is then left to target vulnerability and a pair-specific residual. We call a model a weak source when its examples transfer poorly to third models, a quantity distinct from the asymmetry within the pair."

**Satır 19.** Paragraf sonuna şu eklenir: "Of these predictions, the new two-by-two cells, the CIFAR-100 replication, the ImageNetV2 panel and the gradient tests are out of sample; the CIFAR-10 panel tests extend a first seed that had been seen (Section~\ref{subsec:prereg})."

**Satır 28.** "is symmetric" ifadesinden sonra şu eklenir: ", against one half for a pure source effect (Proposition~\ref{prop:identifiability})".

**Satır 32, üç değişiklik.**
- Açılış: "The third contribution is an intervention on the pair itself."
- H3 cümlesi: "averaged over the two initializations, the effect of architecture on the directional term is equivalent to zero ($\Arho = +0.003$), which does not imply a small directional term in every cell".
- Saldırı cümlesi: "Under momentum PGD and our adaptation of token gradient regularization, which transferred worse than PGD-10 from every ViT source, a fraction of $0.960$ of the gap is retained (Section~\ref{subsec:attack_side}), and the registered AutoAttack rule flags none of the new models".

**Satır 42.** Son cümle şöyle olur: "Input-gradient alignment, measured at a single clean point, is associated with similarity as a gradient-alignment account requires, but it is not evidence of a mechanism, and one ImageNet pair shows that a near-zero cosine can coexist with high similarity (Sections~\ref{subsec:gradcos} and~\ref{subsec:limitations})."

**Satır 48.** Son cümleye "(Section~\ref{subsec:transfer}, Table~\ref{tab:pair_decomposition})" eklenir.

### sections/06_conclusion.tex (Y1)

**Satır 12.**
- "on the log scale architecture leaves the directional term unchanged" yerine: "averaged over initialization, architecture leaves the log-scale directional term within the margin".
- Son cümle: "Momentum PGD and our adapted token gradient regularization do not close the gap, and the registered AutoAttack rule flags none of the six new models."

**Satır 14.**
- "on the logit scale it is large and of opposite sign" yerine: "on the logit scale it is large and negative".
- "we read it as a necessary condition for similar transfer, which leaves the mechanism open" yerine: "we read it as an association a gradient-alignment account requires, not as a mechanism".

### sections/02_related_work.tex (Y2)

**Satır 35.** Demontis cümlesi şöyle olur: "Demontis et al.~\cite{demontis2019adversarial} trace transferability to the intrinsic vulnerability of the target, the complexity of the surrogate and the alignment between the input gradients of surrogate and target."

**Satır 37.** Yenilik cümlesinin sonuna şu eklenir: "; the decomposition here is a parameter-free identity on measured rates whose target term is fixed at a measured value, and a surrogate-complexity term has no separate slot in it: a source main effect enters $r$ as a potential and $\log\simt$ with half weight."

### sections/03_methodology.tex (Y2)

**Satır 52.** "5.7M parameters" yerine "5.5M parameters" yazılır. Üstüne şu yorum konur: % KAYNAK: raporlar/konsey_2026-10-29/_ek_flop_olcumu.json (param_M 5.53, on sinifli baslik).

**Satır 193.** "close to the split of Demontis et al. into target vulnerability and symmetric alignment" yerine: "close to the target-vulnerability and alignment terms of Demontis et al.; their surrogate-complexity term is absorbed as described in Proposition~\ref{prop:identifiability}(d)".

**Satır 207-211.** 211'in sonuna iki cümle eklenir:
- "Rates enter the logarithm in percent, so $\omega$ and $L_k$ carry an additive constant $\log 100$ that cancels from every contrast."
- "$\sigma_m$ also takes up half of any model main effect not captured by $w$."

**Satır 215.** q tanımından sonra şu eklenir: "A pure source effect gives $q = 1/2$, the null value of K-a, so $q$ above one half measures symmetric dissimilarity beyond what a source effect would produce."

**Satır 219, Önerme 1'e (d) maddesi.** "(d) A source main effect $\alpha_i$ in $\ell_{ij}$ enters $r_{ij}$ as the potential difference $\alpha_i - \alpha_j$ and $\log\simt_{ij}$ as $\tfrac12(\alpha_i+\alpha_j)$; with no symmetric difference it gives $q = 1/2$." Satır 222'ye "(d) follows by the same substitution" eklenir.

**Satır 238.**
- "seven $\Linf$-robust CNNs" yerine: "seven $\Linf$-robust CNNs of the ResNet family, four of them (PreAct) ResNet-18 variants".

**Satır 242.** Ā^σ_IN tanımının ardından şu eklenir: "For pair $k$ we write $A^{\sigma}_k$, $A^{\rho}_k$ and $A^{\omega}_k$ for transformer minus CNN differences in $\sigma$, $\rho$ and $\omega$, and $A^{\sigma}_{\mathrm{scr,Liu}}$ for the Liu pair." Ā^σ_IN, 03:242, 03:303, 04:380 ve 04:424'te elle yazılmış; macros_konsey.tex'e \AbarIN makrosu ve \Ak{}{} biçimi eklenir.

**Satır 260.** Son cümle şöyle olur: "The association between alignment at one clean point and similarity is one that a gradient-alignment account requires, but it is not evidence of a mechanism, and the additive fit leaves in place multiplicative or interacting model effects as well as the block structure of the CNN and transformer families."

**Satır 272.**
- "roughly a ten percent relative change in a rate" ifadesinden sonra şu eklenir: "; it is registered for log quantities, so logit and ratio comparisons against the same band are descriptive".
- Paragraf sonuna: "For the $\sigma$ contrasts (H1, H2, K-c) the same margin is a convention without a separate empirical basis."

**Satır 275.**
- "refutation and equivalence from raw intervals" yerine: "refutation, and the equivalence arms of H1 and H2, from raw intervals; equivalence support for K-b and H3 from Holm-adjusted TOST $p$".
- O1 cümlesindeki "which the results below narrow" ifadesinden sonra: ", here also because the design does not separate architecture from convergence in the scratch row".

**Satır 290 ve 303-307, tab:registry.**
- q̄ yerine q yazılır.
- Aile sembolleri metinde bir kez anılır ya da "panel family (CIFAR-10)" biçimine çevrilir.
- H10 ve H10k korunur; tab:mantel'e aynı etiketler konur.

**Satır 328.** "which makes refutation easier" ifadesinden sonra şu eklenir: "; the CIFAR-100 refutation also follows from the original one-sided rule".
- Föy dayanağı: üstüne % FOY:M10.2:1842 yorumu konur.

**Alt bölüm sırası.** subsec:decomposition_def ve subsec:panels, subsec:metrics'ten önceye alınır; böylece tanımlanabilirlik Proposition 1, h ölçeği Proposition 2 olur. 03:64'teki L_k tanımı G tanımının ardına bir cümle olarak iner.

### sections/04_experiments.tex ve 07_appendix.tex (Y3)

**Satır 43-44, Tablo I.** ViT-Tiny 5.5M olur.

**Satır 70.** Son yan cümle şöyle olur: "For one seed pair an image bootstrap gives a standard deviation of $0.030$ for $r_{RV}$, three times its run-to-run spread, so the run-level intervals below, which hold the images fixed, do not include this component."

**Satır 129-132, tab:external_pool.** Pearson korelasyonu $r_{\mathrm{P}}$ ile yazılır; 04:534 ve 07:145'te de aynı yapılır. Eğim bloğu tab:protocol_settings dipnotuna ya da IV-I metnine taşınır. 04:56'daki yineleyen cümle silinir.

**Satır 151.** Paragraf sonuna şu eklenir: "A general weakness of the ViT as a source would also lower the similarity between ViT seeds, which instead matches that between ResNet seeds."

**Satır 155.** SVHN yan cümlesi şöyle olur: "and on SVHN, where no panel was run, the pair's target-correct asymmetry itself changes sign at closely matched clean accuracy (Section~\ref{subsec:transfer})".

**Satır 230.** "so the registered rule would return neither support nor refutation on that scale" ifadesinden sonra şu eklenir: ", and the $\pm0.10$ band itself is registered only for log quantities".

**Satır 235.**
- "so the change of stem and input pipeline does not move the bridge (S1)" yerine: "which is consistent with an unchanged bridge under pooled variances, though not under a Welch interval ($[-0.120, +0.119]$; S1)".
- Yorum satırına FOY:M9.4:1561 zaten var.

**Satır 238.** Son cümle şöyle olur: "This single comparison, which was not registered as a test and carries no interval here, is consistent with a dissimilarity that does not reduce to accuracy alone."

**Satır 246, tab:cells başlığı.** "($w$ in \%, $\omega = \log w$)" yazılır.

**Satır 377.** "with a largest difference of $1.20$ points" yerine: "with a largest difference of $0.95$ points among the fourteen models in the matrix ($1.20$ for an unused reserve)". Yorum satırına FOY:M10.1:1814 eklenir.

**Satır 386, 389 ve tab:imagenet (425).**
- Sembol değişiklikleri: \Asig{scr} yerine $A^{\sigma}_{\mathrm{scr,Liu}}$; "within-pair contrast $A^{\rho}$" yerine $A^{\rho}_k$.
- A^ω başlıkta tanımlanır.
- 389'daki 0.864 cümlesi dipnota taşınır (ek ön kayıt §5.6, satır 126).

**Satır 437.** Son cümle şöyle olur: "The symmetric term is thus tracked by input-gradient alignment, a quantity measured independently of transfer and attack, also after additive model main effects are removed; the family block structure remains (below)."

**Satır 445.**
- İlk cümle şöyle olur: "Alignment measured at one clean point is associated with similar transfer but is not evidence of a mechanism: it is not measured along the attack path, and the residual statistic removes additive model effects only."
- Son cümlenin sonuna şu eklenir: "; this pair has the smallest cosine of the ImageNetV2 matrix, yet its transfer similarity is among the highest of its source, so the energy-weighted cosine is not necessary for similar transfer."
- Yorum satırına FOY:M10.5:2011 ve % KAYNAK: 13_b10_r18_r50_denetimi.md §6 eklenir.

**Satır 480, fig:gradient_alignment altyazısı.**
- "(top)" ve "(bottom)" yerine "(a)-(c) raw, (d)-(f) residual" yazılır.
- "Necessary condition" geçen son cümle atılır.

**Satır 494, ortadaki iki cümle.** "The sign reverses: ... H3 reverses in the same way (Section~\ref{subsec:twobytwo})." yerine şu iki cümle gelir: "On the logit scale the ViT's $\rho$ is large and negative on both datasets, which makes it the directionally stronger source there; on CIFAR-100 this reverses a positive log estimate. H3 also changes sign on the logit scale ($-0.087$) but stays inside the band, where the registered rule would be undecided (Section~\ref{subsec:twobytwo})."

**Satır 497.** "Against a transformer reference the ViT is a directionally weak source." yerine: "Against a single transformer reference, without an interval, the ViT is a directionally weak source."

**Satır 499.**
- "against robust CNNs" yerine: "against this panel of robust ResNet-family CNNs".
- "and the descriptive ImageNetV2 panel points the same way" yerine: "and on ImageNetV2 the transformers of the two Singh pairs are, descriptively, less similar to the CNN panel".
- Cümlenin başına "For this ViT-Tiny," eklenir.

**Satır 506, fig:estimates_forest altyazısı.**
- "(b)" cümlesi şöyle olur: "on the logit scale the ViT's directional term is large and negative on both datasets; the $\pm0.10$ band is registered for the log scale only".
- Sona: "ImageNetV2 intervals cover image sampling only and are not comparable with the run-level intervals above."

**Satır 566 ve tab:fb4, tab:panel_tests, tab:mantel, tab:main_results, tab:protocol_settings.**
- Altyazılarda "mean$\pm$SD" kullanılır.
- p değerleri $1.26\times10^{-4}$ biçimine çevrilir ya da tabloya "aE-b denotes a×10^{-b}" dipnotu konur.

**07:137 ve 07:144.** A14 sonuçlanana kadar dokunulmaz.

### sections/05_discussion.tex ve 04z_computational.tex (Y4)

**05:19.** İlk cümleye "on CIFAR-10 and the log scale" eklenir: "...and the unlikeness runs both ways: on CIFAR-10 and the log scale, once each target's white-box vulnerability is divided out, ...".

**05:21, dört değişiklik.**
- "token gradient regularization transfers worse" yerine: "our adaptation of token gradient regularization, not validated against its published gain, transfers worse".
- Awad cümlesi: "Similarity to the target family then accounts for most of a source's transfer deficit into it, in contrast to source-quality effects such as the better transfer of robust surrogates~\cite{awad2025defense}, which the directional term bounds on this panel."
- Siyah kutu cümlesi: "For a scratch-trained ViT-Tiny like ours, a black-box score measured with CNN surrogates therefore reflects dissimilarity along with vulnerability".
- Demontis cümlesi: "The decomposition separates the target-vulnerability and alignment terms of Demontis et al., while their surrogate-complexity term is split between $r$ and $\log\simt$ (Proposition~\ref{prop:identifiability}(d))".
- "a necessary condition that leaves the mechanism open" yerine: "an association that leaves the mechanism open".

**05:33.**
- Proposition 1(b) cümlesinden sonra şu eklenir: "Part (b) holds on any additive scale, including the points scale of that fit."
- "the rest is a seed-stable directional residual" yerine: "the rest is a seed-stable directional residual of $+0.115$, above the margin".

**05:38.**
- "gives it a negative directional term" yerine: "gives it a negative directional term on the log scale, in an exploratory secondary analysis".

**05:60.** Welch cümlesinden sonra şu eklenir: "the bridge between the two ResNet-18 pipelines (S1) is equivalent under pooled variances but not under a Welch interval."

**05:68.**
- TGR cümlesi şöyle olur: "TGR ran with its original settings in adapted form, without a check that the adaptation reproduces its published gain on a standard ViT, and attacks with input diversity, more steps or the self-ensemble of Naseer et al. were not run."
- Demontis anıldığı yere "and its surrogate-complexity term" eklenir.

**05:72.**
- "by at most $1.20$ points" yerine "by at most $0.95$ points for the models in the matrix" yazılır; yorum satırı FOY:M10.1:1814 olur.
- R18 ile R50 cümlesinin sonuna: ", so for this measure the cosine is not a necessary condition for similar transfer".

**04z:15.** "The registered CIFAR-100, ImageNetV2 and gradient blocks reused existing checkpoints and trained no new model."

### paper/figures/konsey/ (şekil ajanı; kalıcı çizim visio-cizici turunda)

**fig_similarity_matrix.py**
- Satır 207'deki biçim .2f olur ya da çentikler [−1.5, −1.0, −0.5] gibi tek ondalıklı değerlere sabitlenir.
- (b) panelindeki etiketler "ViT (C100)" ve "ResNet (C100)" olur.

**fig_source_gap_split.py**
- Gösterge "total gap $G$" ve "registered $G$ threshold" olur.
- Negatif yönlü pay simetrik çubuğun tepesinden aşağı doğru (0.122 ile 0.167 arası, açık renk) çizilir.

**fig_estimates_forest.py.** Gri bant yalnız log satırlarına çizilir.

**fig_cells_interaction (c) ve fig_attack_side.** Eksen etiketlerine "(w in %)" eklenir.

**fig_decomposition_schematic**
- Paneller (a)-(d) olur.
- Panel ortalaması ⟨·⟩_P ile gösterilir.
- (c)'deki dönüştürücü bloğu çerçevelenir.

**final/fig_protocol_sets**
- "endorsed pair" yerine "marginal subsets removed", "different estimand" yerine "source-robustness term" yazılır.
- (a) başlığı "N (CNN→ViT / ViT→CNN)" olur.

## 4. En zayıf üç halka ve hakem yanıtı için hazırlık

### Birinci halka: sıfırdan satırındaki benzemezlik bir yakınsama yapıtı olabilir

**Beklenen hakem cümlesi:** "Kötü yakınsamış bir ViT-Tiny'nin CNN'lere benzemediğini göstermişsiniz; bu, ViT ailesi hakkında bir sonuç değil."

**Hazır yanıtın omurgası:**
- Manşetin taşıyıcısı A^σ'nın büyüklüğü değil, simetrik payın büyüklüğüdür. q, doğruluğu düşük CIFAR-100 ViT'sinde de 0.840'tır.
- Saf bir kaynak etkisi q = 0.5 verirdi (B9 düzeltmesinden sonra bu metinde yazılı olacak).
- Doğruluğu eşleşmiş iki karşılaştırma işareti korur: V-IN, R224-IN'e göre daha düşük σ taşır (föy 1497, 1499); Singh çiftleri −0.142 [−0.197, −0.090] verir (föy 1938).
- K-c'de ViT tohumları birbirine ResNet tohumları kadar benzer. Genel bir kaynak zayıflığı bunu düşürürdü.

**Yanıtın dürüst kabulü:** doğruluk eşleşince etki kabaca üçte bire iniyor ve ImageNet ölçeğinde sıfırdan satırı belirsiz. Bu kabul özete girmeli; taslakta "a contrast confounded with its lower clean accuracy" ile girmiş durumda.

**Bu turda hazırlanacaklar:**
- Yanıtı sayıyla kurmak için A2 (−0.104'ün aralığı) föyde olmalı.
- A3 (CNN eğilim çizgisinden sapma) masada üretilmeli.
- GPU varsa en güçlü yanıt A1'dir. Ancak o zaman ön kayıt eki önce dondurulmalı; sonucu görülmüş bir hücre "registered" sayılamaz.

### İkinci halka: zayıf kaynak görünümü saldırı yetersizliğinden kaynaklanıyor olabilir

**Beklenen hakem cümlesi:** "Naseer'in ViT'ye özgü saldırısını koşmadınız; TGR'niz PGD'den kötü çıktı, uygulamanız bozuk olabilir."

**Hazır yanıtın omurgası:**
- Ön kayıtlı küme önceden sabitlendi.
- TGR hiçbir ViT kaynağında seçilmedi (föy 1648).
- Korunma oranı 0.960 [0.941, 0.976] (föy 1624-1625).

**Yanıtın dürüst kabulü:** MI ile PGD neredeyse aynıdır; seçim, açığın yalnız küçük bir kısmını kapattı (föy 1623). Saldırı tarafı açıklaması bu kümeyle kapanmış sayılamaz.

**Hazırlanacaklar:**
- A7: temiz ViT-Tiny ile TGR doğrulaması. Kısa bir koşu; sonuç ne çıkarsa çıksın yanıtı güçlendirir.
- A7 yapılmazsa 05:68'deki sınırlılık cümlesi bu soruyu önceden yanıtlar.

### Üçüncü halka: yönlü terim ve gradyan iddialarının çıkarım yapısı

**Beklenen hakem cümleleri:**
- "K-b'nin aralığı yalnız üç tohumun yayılımı; görüntü gürültüsü üç kat büyük."
- "Mantel p'si aile bloklarından geliyor."
- "Gereklilik iddiasını hiçbir şey sınamıyor."

**Hazır yanıtın omurgası:** görüntüler bütün koşularda ortaktır ve aralıklar bu görüntülere koşulludur; bu metinde yazılı (03:272). A5 ile hiyerarşik bootstrap üretildiğinde K-b(CIFAR-10) kararının büyük olasılıkla değişmeyeceği istatistik merceğinin kaba hesabıdır; bu bir ölçüm değildir. Ölçüm gelmeden yanıt verilmemeli.

Mantel için yanıt A6 ile hazırlanır:
- Aile içi kısıtlı permütasyon.
- 11_sonuc §7'deki aile ayıklamalı Spearman 0.905, 0.892, 0.888; yalnız CNN-CNN Spearman 0.963, 0.929, 0.843. Bu değerler föye girdikten sonra kullanılabilir.

Gereklilik iddiası bu turda geri çekiliyor (B3). Hakemin karşı örneği bulmasındansa makalenin onu kendisinin vermesi daha iyidir.

H3 için yanıt: H3 bir ana etki eşdeğerliğidir. Hücre başına yönlü terimin değişkenliği 04:230 ve 05:68'de zaten yazılı. Basit etkiler A2 ile föye girerse bir tabloda gösterilir.

## 5. Güçlü yanlar

- **Ön kayıt disiplini.** IEEE Access'te bu türde bir makale için ortalamanın çok üstünde.
  - Dondurma tarihleri ve SHA-256 özetleri föyle eşleşiyor (föy 1684-1686, 2022-2032).
  - Kayıttan önce görülmüş veri satır satır beyan edilmiş (03:328).
  - Sonradan gevşetilen iki kural adıyla anılmış; üretilmeyen duyarlılıklar listelenmiş.
  - Holm aileleri, TOST sınırları, payda kuralı, H2'nin logit işaret koşulu ve B6 maskeleme kuralı metinde ve Tablo III'te ön kayıtla birebir örtüşüyor.
- **Sayı-kaynak zinciri.** Üç mercek yirmiden fazla sayıyı föyle karşılaştırdı ve hepsini aynı buldu. Tohum başına q, A^σ, I^σ ve A^ρ hücre ortalamalarından bağımsız olarak yeniden hesaplandı ve tuttu.
- **Olumsuz sonuçlar saklanmamış.** Gövdede ya da tablolarda açıkça duranlar:
  - K-b(B9) çürütmesi.
  - Logit ölçekte yönlü terimin büyük ve negatif olması.
  - V-IN'in bant dışı ρ'su.
  - Liu çiftinin "uncertain" etiketi.
  - XCiT panelinde ρ yaklaşık +0.20.
  - Yörüngelerde çarpımsal yasanın tutmaması (R² 0.201).
  - Önceki sürümün yön iddiasının düzeltilmesi.
- **Simetrik pay bulgusu sağlam.** Log, logit ve oran ölçeklerinde, panel jackknife'ında (0.931 ile 0.941), δ = 0.06'da, XCiT ikincil panelinde ve iki CIFAR veri kümesinde tutuyor.
- **Önerme 1 alana uygulanabilir bir katkı.** İki modelli ve tek ViT'li tasarımlarda toplamsal kaynak-hedef bölüşümünün neden tanımlanamadığını kısa ve doğru gösteriyor. (d) maddesi eklenince q'nun okunuşu da kendi içinde kapanır.
- **R224-scr köprü hücresi.** Giriş çözünürlüğü ve girdi hattı itirazını birleşik varyans altında ikna edici biçimde kapatıyor (−0.0003 [−0.035, +0.034]; föy 1561).
- **Protokol katmanı uygulanabilir.** Toplam olasılık özdeşliğine ve ölçülmüş p öncülüne dayanıyor (en küçük p 0.989, h ölçeğinde en büyük ayar terimi 0.0044). Raporlama gereklilikleri kanıta bağlı.
- **Biçim ve sunum temiz.**
  - Göndermeler eksiksiz: 78 etiketin hepsi gönderiliyor, tanımsız gönderme yok.
  - Şablon dışında taşma yok.
  - Makine yazımı sayacı temiz.
  - Şekiller tutarlı bir renk ve işaret dili kullanıyor, renk dışında ikinci bir kanal taşıyor.
  - Tablo başlıkları ölçeği, aralık türünü ve karar kuralını açıkça veriyor.