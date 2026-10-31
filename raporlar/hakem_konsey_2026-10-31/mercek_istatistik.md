# Mercek 1: istatistik ve on kayit sadakati (31.10.2026)

Bu rapor salt okur hakem ajaninin yapisal ciktisindan ana oturumca dosyaya aktarilmistir; metin ajanin kendi ifadeleridir.

Genel karar: BUYUK_REVIZYON

## Bulgular (siddet sirasiyla)

### 1. [sari] K-a ve K-b aralıklarında görüntü örneklemesi yok; ön kayıtlı hiyerarşik bootstrap üretilmemiş

Dosya: paper/manuscript/main.tex:117; paper/manuscript/sections/04_experiments.tex:70, 145-148, 165, 175-176

Ifade: Özet: "testing pre-registered predictions with three seeds (brackets: 90% intervals). On CIFAR-10, 0.936 [0.925, 0.948] ..."; 04:70: "an image bootstrap gives a standard deviation of 0.030 for r_RV, three times its run-to-run spread, so the three runs agree to within image noise."

Kanit: Ön kayıt §5 (satır 86) hiyerarşik bootstrap'ı (koşular hücre içinde, görüntüler ortak, B = 2000) bağlayıcı duyarlılık olarak yazar; föy 1607 K-a ve K-b için bunu 'bulunamadi' diye kaydeder. K-a ve K-b aralıkları df 2'lik t aralığıdır ve yalnız tohum yayılımını taşır; föy 1722'ye göre çift düzeyinde r_RV'nin görüntü bootstrap SD'si 0.030, koşum SD'si 0.010'dur (föy 1706). Görüntüler bütün koşularda ortak olduğundan görüntü gürültüsü koşum yayılımına hiç girmez; 04:70'deki 'agree to within image noise' cümlesi bu yüzden kanıt değil, aralığın neyi dışarıda bıraktığının itirafıdır. Tablo V altyazısı (04:165) koşulluluğu doğru yazıyor, ama özet ve giriş (01:28) aynı aralıkları niteleme olmadan veriyor. Kaba bir hesapla ρ'nun görüntü bileşeni eklense bile K-b(CIFAR-10) kararı büyük olasılıkla değişmez (yarı genişlik 0.02'den 0.04 düzeyine çıkar), ama bunu metin değil ölçüm göstermelidir.

Duzeltme: Mevcut örnek bazında npz kayıtlarından, yeniden eğitim olmadan, K-a ve K-b için ön kayıttaki hiyerarşik bootstrap'ı CIFAR-10 ve CIFAR-100'de üretin, föye build_reference_sheet.py ile ekleyin ve Tablo V'in duyarlılık bloğuna bir satır olarak koyun. Özetteki parantezi "(brackets: 90% intervals over training runs, conditional on the test images and panel)" biçiminde daraltın. 04:70'teki son yan cümleyi "so the run-level intervals below, which hold the images fixed, do not include this component" gibi bir cümleyle değiştirin.

### 2. [sari] "Necessary condition" iddiası mantıksal olarak yanlış ve kendi verisiyle çelişiyor

Dosya: paper/manuscript/main.tex:117; sections/01_introduction.tex:42; sections/03_methodology.tex:260; sections/04_experiments.tex:445, 480; sections/05_discussion.tex:21; sections/06_conclusion.tex:14

Ifade: Özet: "input-gradient cosine, a necessary condition for similar transfer, tracks similarity on three datasets"; 03:260: "Alignment at one clean point is a necessary condition for similar transfer and not evidence of a mechanism"

Kanit: Ek ön kayıt §9 (satır 200) şöyle der: "τ̄ ile ilişkisi bir mekanizmanın gerekli koşuludur, yeterli kanıtı değildir"; yani gerekli koşul olan şey ilişkinin varlığıdır (bir hizalanma açıklaması bu korelasyonu gerektirir). Metin bunu "hizalanma benzer transferin gerekli koşuludur" diye, veriyle sınanmamış bir mantıksal iddiaya çevirmiş. Bir sıra korelasyonu gereklilik göstermez; üstelik veri karşı örnek veriyor: ImageNetV2'de Salman R18 ile R50 arasındaki c_ij = 0.0034 matrisin en küçük değeridir (föy 2011, en küçük 0.003), aynı çiftin log τ̄'su −0.936'dır ve R18'in en yüksek benzerliklerinden biridir (11_sonuc_b8_b10.md §6, mantel_imagenetv2.json log_tau_matrisi[0][1]; 13_b10_r18_r50_denetimi.md bu değeri gerçek bulmuştur). Şekil 9(c)'nin sol üst köşesindeki CNN-CNN noktası bu çifttir. Yani ölçülen nicelik sıfıra yakınken benzerlik yüksektir; c_ij gerekli koşul değildir. Brif 12 §2 ve §8.1 m.7 aynı yanlış okumayı taşıyor.

Duzeltme: Altı yerde ifadeyi "an association that a gradient-alignment account requires, but not evidence of a mechanism" çizgisine çekin; özette "a necessary condition for similar transfer" yan cümlesini "measured without any attack" ile değiştirin. 04:445'teki R18-R50 cümlesine, enerji ağırlıklı kosinüsün sıfıra yakın olduğu bir çiftte benzerliğin yüksek kaldığını ve bu yüzden c_ij'nin benzer transfer için gerekli olmadığını ekleyin. Sayı verilecekse 0.0034 ve −0.936 önce föye (M10 eki) alınmalıdır; o zamana kadar cümle sayısız kurulur.

### 3. [sari] Mantel sınamasında aile blok yapısı ve değiştirilebilirlik; ön kayıtlı S10-3 üretilmemiş

Dosya: paper/manuscript/sections/04_experiments.tex:437, 445, 459-464; sections/03_methodology.tex:260, 330; main.tex:117

Ifade: 04:437: "Every one-sided Mantel p sits at the permutation floor of 10^-4 ... The symmetric term is thus predicted by input-gradient alignment ... also after model-level main effects are removed."

Kanit: Toplamsal artıklama X_ij = μ + a_i + a_j + e_ij aile bloklarını ayırmaz (metin 04:445'te bunu yazıyor). CIFAR-10 matrisinde 20 modelin 10'u aynı tarifin tohumlarıdır; Şekil 9(a) ve (d)'de karma çiftler sol altta kümelenir, ViT tohum çiftleri sağ üstte uç noktalardır. Etiket permütasyonu bu blokları karıştıran bir sıfır dağılımı kurar; p'nin tabanda olması 'ilişki aile ayrımının ötesine geçer' anlamına gelmez. Ek ön kayıt §6.4 aile göstergeli kısmi Mantel'i (S10-3) kaydetmiş, kod yazılmamıştır (EK Dondurma doğrulayıcısı m.4; 11_sonuc §6 m.4). Aile ayıklamalı Spearman (0.905, 0.892, 0.888) ve yalnız CNN-CNN artık Spearman (0.963, 0.929, 0.843) 11_sonuc §7'de hesaplanmış ama föyde yoktur (brif §9), bu yüzden metne giremiyor. Özet ise "residual Spearman 0.893-0.944" değerini model etkilerinden arınmış hizalanma gibi sunuyor.

Duzeltme: S10-3'ü ve aile içinde kısıtlı permütasyonla (etiketler yalnız aynı aile içinde karıştırılarak) Mantel'i keşifsel etiketle üretin; R11 §7 değerlerini build_reference_sheet.py ile föye (M10.7 gibi) alın ve Tablo XII'ye 'within-family' satırı ekleyin. Bu yapılana kadar özette "also after additive model effects, though not family blocks, are removed" niteleme ekleyin ve 04:437'nin son cümlesini "after additive model main effects are removed; the family block structure remains (below)" diye daraltın.

### 4. [sari] Çürütülen K-b(B9) özette ve başlıkta yumuşamış

Dosya: paper/manuscript/main.tex:65-67, 117; sections/04_experiments.tex:497

Ifade: Özet: "On CIFAR-100 the symmetric share (0.840) and seed similarity replicate but the ViT's small directional term does not (+0.143)"; başlık: "Not a Weak Source but a Different One"

Kanit: Föy 1839: K-b(B9) 'curutuldu (pozitif yon)', TOST p 0.953, %95 [+0.082, +0.203]. Metodolojiye göre (03:211) pozitif ρ, modelin yönlü olarak zayıf kaynak olduğu anlamına gelir; yani CIFAR-100'de ViT log ölçekte yönlü olarak da zayıf kaynaktır. XCiT ikincil panelinde CIFAR-10'da da ρ(V-scr) +0.198 ile +0.204'tür (föy 1606). "does not [replicate]" ifadesi ek ön kayıdın ayırdığı 'kararsız' ile 'çürütüldü' arasındaki farkı siliyor; brif 12 §2 B9 satırı K-b(B9)'u yumuşatmayı açıkça yasaklar. Giriş (01:28) ve IV-C (04:155) kararı doğru yazıyor, sorun özet ve başlık düzeyinde. Ayrıca föy 1842'ye göre bu çürütme, dondurmadan önce iki yöne genişletilen kuraldan bağımsızdır (K-b_eski_yalniz_pozitif_okuma_curutme: evet); bu, metnin dürüstlüğünü güçlendirecek ama kullanılmamış bir bilgi.

Duzeltme: Özette "but the registered equivalence of the ViT's directional term is refuted (+0.143): on CIFAR-100 the ViT is also a directionally weaker source" yazın. Başlığa bir niceleyici ekleyin ("Less a Weak Source than a Different One" ya da "Mostly a Different One"). 03:328'deki kural değişikliği cümlesine, CIFAR-100 çürütmesinin özgün tek yönlü kuralla da çıktığını bir yan cümleyle ekleyin.

### 5. [sari] n = 2 hücreler: "three seeds" ifadesi ve Welch altında tutmayan S1 köprü eşdeğerliği

Dosya: paper/manuscript/main.tex:117; sections/04_experiments.tex:227, 235; sections/03_methodology.tex:272

Ifade: Özet: "testing pre-registered predictions with three seeds"; 04:235: "so the change of stem and input pipeline does not move the bridge (S1) ... this bridge is what H1 adds"

Kanit: Yeni üç hücrede ikişer koşu vardır (Tablo II; föy 1497-1499); özet bütün sınamalar için üç tohum diyor. Birleşik varyanslı df 5 t aralığı eşit varyans varsayar; Welch df 1.10-1.95'tir (föy 1553). S1 köprüsünün σ farkı −0.0003, birleşik %90 [−0.035, +0.034] (df 3) iken Welch %90 [−0.120, +0.119]'dur (föy 1561) ve ±0.10'u aşar; yani köprü eşdeğerliği eşit olmayan varyans altında gösterilememiştir. Metin ise H1'in ön kayıt öncesinde görülmüş σ farkının ötesindeki bilgi içeriğini (03:328) tam bu keşifsel köprüye bağlıyor.

Duzeltme: Özette "three seeds in the original pair and two in each new cell" yazın. 04:235'e S1'in Welch %90 aralığını ekleyin ve "does not move the bridge" yerine "is consistent with an unchanged bridge under pooled variances, though not under Welch intervals" kurun. Sınırlılık paragrafında (05:60) H1 için verilen Welch cümlesinin yanına S1'in de Welch altında eşdeğerlik vermediğini ekleyin.

### 6. [yesil] H3'ün logit sonucu iki yerde çelişik niteleniyor

Dosya: paper/manuscript/sections/04_experiments.tex:494 (ve 230)

Ifade: 04:494: "H3 reverses in the same way (Section IV-D)."

Kanit: Logit H3 −0.087, %90 [−0.110, −0.064], %95 [−0.116, −0.058] (föy 1551): işaret değişiyor ama kestirim ±0.10 içinde. 04:230 bunu doğru biçimde 'kural bu ölçekte ne destek ne çürütme verirdi' diye yazıyor; 04:494 ise K-b'nin −0.304 ile bandın çok dışına çıkmasıyla 'aynı biçimde' döndüğünü söylüyor.

Duzeltme: "H3 changes sign as well but stays inside the band, with a 95% interval that excludes zero, so the registered rule would leave it undecided on that scale (Section IV-D)."

### 7. [yesil] Log birimi için tanımlı δ logit ölçeğe kayıtsız aktarılıyor

Dosya: paper/manuscript/sections/04_experiments.tex:230, 494; paper/figures/konsey/fig_estimates_forest.pdf (b)

Ifade: 04:230: "the estimate stays inside ±0.10, so the registered rule would return neither support nor refutation on that scale"; 04:494: "far outside the ±0.10 band"

Kanit: Ön kayıt §5 (satır 50): "Eşdeğerlik sınırı bütün log ölçekli niceliklerde δ = 0,10". Logit farkları, T 0.2-0.5 aralığında log farklarının yaklaşık 1.3-2 katıdır; aynı ±0.10 bandı logit ölçekte daha dar bir göreli değişime karşılık gelir. H3'ün logit 'kararsız' etiketi bu kayıtsız aktarıma bağlıdır; orman şeklinde logit satırlarının üstüne de aynı gri bant çizilmiş.

Duzeltme: Logit karşılaştırmalarının ±0.10 ile yapılmasının kayıtlı olmadığını bir yan cümleyle yazın; ya bandı logit satırlarından kaldırın ya da altyazıda bandın yalnız log ölçek için kayıtlı olduğunu belirtin.

### 8. [yesil] Betimsel ImageNetV2 sonucuna çıkarım dili sızıyor; n = 1 referans niteleme gerektiriyor

Dosya: paper/manuscript/sections/04_experiments.tex:389, 497, 499

Ifade: 04:499: "A symmetric dissimilarity carries the ViT's weak-source appearance ... and the descriptive ImageNetV2 panel points the same way"; 04:497: "Against a transformer reference the ViT is a directionally weak source."

Kanit: ImageNetV2'de kaynak açığının simetrik payını ölçen tek istatistik bilgi taşımıyor: üç çiftin ortalama q'su 0.864, %90 [0.126, 1.603], payda kuralı Liu çiftinde tetiklenmiş (föy 1945); çift q'ları 1.364, 0.682 ve tanımsızdır (föy 1930-1932). Singh çiftlerindeki A^σ benzerlik karşıtlığıdır, açığın bölünmesi değil. Ek ön kayıt §5.6 üç çift ortalamasının yalnız dipnotta verilmesini ister; 04:389'da gövdededir. 04:497'deki cümle tek üyeli XCiT paneline dayanır ve aralık taşımaz.

Duzeltme: 04:499'u "and on ImageNetV2 the transformers of the two Singh pairs are, descriptively, less similar to the CNN panel" diye kurun; 04:389'daki 0.864 cümlesini dipnota taşıyın. 04:497'yi "Against a single transformer reference, without an interval, the ViT is a directionally weak source" biçiminde niteleyin.

### 9. [yesil] Maskeleme sonucu kuralın ötesinde genelleniyor

Dosya: paper/manuscript/sections/06_conclusion.tex:12

Ifade: "none of the new models shows signs of gradient masking"

Kanit: Kural ilk 1000 görüntüde 10 puanlık eşiktir; en büyük fark R224_IN_s1301'de 7.40, eşiğe uzaklık 2.60 puandır (föy 1673). V-scr ve R32 kuralın kapsamında değildir (ÖK Dondurma eki (i) m.7). Giriş ve özet doğru biçimde "flags no new model" diyor.

Duzeltme: "and the registered AutoAttack rule flags none of the six new models" yazın.

### 10. [yesil] Karar ilkesi ve δ dayanağı eksik ya da belirsiz anlatılıyor

Dosya: paper/manuscript/sections/03_methodology.tex:272, 275

Ifade: 03:275: "Support is read from Holm-adjusted p < 0.05, refutation and equivalence from raw intervals"; 03:272: "The margin came from the root-mean-square directional residual ..."

Kanit: K-b ve H3'te eşdeğerlik desteği Holm sonrası TOST p ile verilir (ÖK §5 satır 62, 74; föy 1528, 1588); 'equivalence from raw intervals' yalnız H1 ve H2'nin eşdeğerlik kolu için doğrudur. ÖK §5 (satır 50) σ ölçekli karşıtlıklarda (H1, H2, K-c) δ'nın ampirik dayanağı olmadığını, uzlaşım olduğunu yazar; metin yalnız yönlü terimin dayanağını veriyor.

Duzeltme: "refutation, and the equivalence arms of H1 and H2, from raw intervals; equivalence support for K-b and H3 from Holm-adjusted TOST p" yazın; δ cümlesine "for the σ contrasts the same margin is a convention without a separate empirical basis" ekleyin.

### 11. [yesil] Ön işleme farkı için verilen 1.20 puan matristeki bir modele ait değil

Dosya: paper/manuscript/sections/04_experiments.tex:377; sections/05_discussion.tex:72

Ifade: 04:377: "Every candidate passed the registered preprocessing check, with a largest difference of 1.20 points"; 05:72: "departs from some models' own pipeline by at most 1.20 points"

Kanit: Föy 1816-1818: 1.20 puan, matrise girmeyen yedek IN_Wong2020Fast'e aittir. Matrisdeki on dört model arasında en büyük mutlak fark Mo ViT-B'nin 0.95 puanıdır (föy 1814).

Duzeltme: "with a largest difference of 0.95 points among the fourteen models in the matrix (1.20 for the unused reserve)"; 05:72'de 0.95 kullanın.

### 12. [yesil] V-IN ile R224-IN karşılaştırması aralıksız argüman olarak kullanılıyor

Dosya: paper/manuscript/sections/04_experiments.tex:238; sections/05_discussion.tex:60

Ifade: "yet its panel similarity stays below that of R224-IN (−0.739 against −0.635). This single comparison, which was not registered as a test, argues against reducing the dissimilarity to accuracy alone."

Kanit: Karşılaştırma ikiye iki koşuya dayanır ve aralık verilmemiştir; fark (−0.104) brif §9 gereği föyde yoktur. Birleşik SD 0.0273 ile (föy 1532) kaba bir %90 aralık sıfırı dışlar görünüyor, ama bu hesap föyde değil.

Duzeltme: Farkı birleşik varyanslı aralığıyla föye (önerilen M9.10 türetilmiş karşıtlıklar) ekleyin ve keşifsel etiketle verin; o zamana kadar "argues against" yerine "is consistent with not reducing" yazın.

### 13. [yesil] Orman şeklinde farklı türden aralıklar yan yana

Dosya: paper/figures/konsey/fig_estimates_forest.pdf (a); sections/04_experiments.tex:506

Ifade: Altyazı: "Registered estimates with 90% (thick) and 95% (thin) intervals ... with the descriptive ImageNetV2 pair estimates (open markers) for comparison"

Kanit: H1 ve H2 aralıkları koşu düzeyinde df 5 t aralığıdır; ImageNetV2 aralıkları yalnız görüntü bootstrap'ıdır ve kontrol noktası değişkenliğini taşımaz (ek ön kayıt §5.6). Aynı kalınlık kodu görsel olarak karşılaştırılabilirlik izlenimi veriyor.

Duzeltme: Altyazıya "ImageNetV2 intervals cover image sampling only and are not comparable with the run-level intervals above" ekleyin.

## Guclu yanlar

- Ön kayda sadakat yüksek: F_B2, F_B4, F_B9 ve F_B10'un bütün kararları, Holm aileleri, TOST δ = 0.10 ve 0.06 duyarlılığı, payda kuralı, H2'nin logit işaret koşulu, B5 eşiği ve B6 maskeleme kuralı metinde ve Tablo III'te ön kayıt §5-§6 ve ek §4-§6 ile birebir örtüşüyor; O1 bölgesi doğru sırayla ve maskeleme sonrası olarak veriliyor.
- Föyle örneklem denetimi temiz: H1, H2, H3 kestirimleri ve %90/%95 aralıkları, t, ham ve Holm p'leri (föy 1526-1528); logit, oran, Welch, jackknife ve hiyerarşik bootstrap satırları (1549-1555); K-a, K-b, K-c ve δ = 0.06 (1587-1606); CIFAR-100 K-a, K-b, K-c, logit ve oran (1838-1860); B5 oranı ve aralıkları (1620-1629); B6 farkları (1666-1673); ImageNetV2 A^σ değerleri ve etiketleri (1930-1939); Mantel istatistikleri ve Holm p (1970-1988); McNemar sınırları ve Tablo III. Yirmiden fazla sayının hepsi föyle aynı.
- Olumsuz sonuçlar saklanmamış: K-b(B9) çürütmesi gövdede açıkça, logit ölçekte işaret dönmesi, V-IN'nin bant dışı ρ'su, Liu çiftinin 'belirsiz' etiketi, XCiT panelinde ρ ≈ +0.20, CIFAR-100 bant öngörüsünün tutmaması ve çarpımsal yasanın yörüngelerde başarısızlığı yazılmış.
- Görülmüş veri beyanı ayrıntılı ve yönlü: H1 öngörüsünün σ farkı bilinerek yazıldığı, K-b kuralının çürütmeyi kolaylaştıran yönde genişletildiği, B5 öngörü sırasının doğrulanamadığı, B9 sırasında ekrana düşen günlük satırları ve üretilmeyen duyarlılıklar tek tek beyan edilmiş.
- Bütünlük zinciri güçlü: dondurulmuş çözümleme betiği, hücre tabloları ve iki ön kayıt gövdesinin SHA-256 özetleri çıktılarla eşleşiyor (föy 1684-1686, 2022-2032).
- ImageNetV2 bölümünde önceden yazılmış cümle büyük ölçüde korunmuş, 'destek' ve 'çürütüldü' sözcükleri kullanılmamış, aralıkların yalnız görüntü örneklemini taşıdığı yazılmış.
- Tanımlanabilirlik önermesi iki modelli toplamsal bölüşümün neden kaynak etkisi okunamayacağını açık biçimde gösteriyor; logit ve oran ölçekleri sonuçları zayıflattığı yerde de raporlanmış.
- Kabul için tek en önemli koşul: K-a ve K-b için ön kayıtlı hiyerarşik (tohum ve görüntü) bootstrap'ın her iki CIFAR veri kümesinde üretilip kararların değişmediğinin gösterilmesi ve 'necessary condition' iddiasının ek ön kayıt §9'daki anlamına geri çekilmesi.
