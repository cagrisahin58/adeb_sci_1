# P2 önerisi: dış geçerlilik ve ölçek merceği (konsey, 29.10.2026)

Hazırlayan: öneri sahibi araştırmacı (opus alt ajan). Kısaltmalar: FÖY = `results/C1_REFERANS_FOYU.md`, DURUM = `raporlar/konsey_2026-10-29/00_durum_dosyasi.md`, MASA = `raporlar/konsey_2026-10-29/01_masa_testi.md`. PANEL1, PANEL2 ve PANEL3 bu öneri için üretilen `_P2_panel_masa.json`, `_P2_panel_logit.json` ve `_P2_panel_logit_ayri.json` dosyalarıdır (aynı klasör, betikler `_P2_panel_*.py`, tek girdi `results/q1/havuz_cifar10/havuz_protokoller.json`, GPU'suz). Karantinadaki klasörler kullanılmamıştır.

## 1. Manşet iddia

> Under adversarial training, the CNN-to-ViT transfer asymmetry is set by the transformer's training-data regime, not by its architecture family: the same ViT-Tiny trained with the same recipe stops being a weak transfer source when initialised from ImageNet-21k, a ResNet-18 becomes one when starved of data, and accuracy-matched, same-recipe CNN and transformer pairs on ImageNet show no family-level source deficit.

Türkçesi: Çekişmeli eğitimde CNN'den ViT'ye transfer asimetrisini mimari ailesi değil dönüştürücünün eğitim verisi rejimi belirler; aynı tarifle eğitilen aynı ViT-Tiny ImageNet-21k ile başlatıldığında zayıf kaynak olmaktan çıkar, verisi kısılan ResNet-18 zayıf kaynağa dönüşür ve ImageNet'te doğruluğu eşleşmiş, aynı tarifli CNN ve dönüştürücü çiftlerinde aile düzeyinde kaynak açığı görülmez.

Başlık adayı: "Weak Sources, Not Weak Architectures: The CNN-ViT Transfer Asymmetry under Adversarial Training Follows the Data Regime".

Kaynak gücü S(m), m modelinde üretilen PGD örneklerinin sabit ve dış bir hedef paneline giden hedef-doğru transfer oranlarının logit ortalamasıdır; hedef duyarlılığı T(m) panelden m'ye gelen oranların aynı ortalamasıdır. İddia S'nin hangi müdahaleyle değiştiğini söyler, tanım gereği doğru değildir ve üç ayrı müdahale tersini gösterebilir. Makalenin "asimetri bu ViT-Tiny'nin kaynak etkisidir" cümlesi korunup nedensel düzeye taşınır; dört protokol ve özdeşlik ölçüm yöntemi olarak kalır.

## 2. Neden önemsiz ya da bilinen bir sonuç değil

Naseer ve ark. (arXiv 2106.04169) standart eğitimli ViT'lerde geleneksel saldırıların çok düşük kara kutu aktarılabilirliği verdiğini, Mahmood ve ark. (arXiv 2104.02610) ise ImageNet-21K ön eğitimli ViT'lerin CNN'lere güçlü kaynak olduğunu bildirir (FÖY:700, kaynak farkı −25.01). Springer ve ark. (arXiv 2106.02105) hafif gürbüz kaynakların, Demontis ve ark. (arXiv 1809.02861) düşük karmaşıklıklı vekillerin daha iyi aktardığını gösterir. Bu çalışmalar arasında ön eğitim, eğitim amacı, ölçek ve protokol birlikte değişmektedir. Yalnız başlatmayı, yalnız gövdeyi ya da yalnız veri miktarını değiştirip kaynak gücünü sabit dış panelle ölçen bir tasarım iki hızlı aramada bulunamamıştır; bu bir yenilik iddiası değildir, belgelenmiş tarama (DURUM A11) yenilik merceğinin işidir.

| En sert itiraz | Tasarımın yanıtı |
|---|---|
| Ön eğitimli model daha iyi modeldir, elbette daha güçlü kaynaktır | Gürbüz CNN'lerde temiz doğruluk 83.34 ile 90.06, beyaz kutu koşullu yanıltma 25.25 ile 47.56 arasında değişirken S dar bir bantta kalır (logit −1.661 ile −1.365, PANEL3 `target_correct.S_logit`); en doğru model Standard WRN (94.78) en zayıf kaynaktır (−4.286). R_20 kolu ve Andriushchenko2020 (temiz 79.84) doğruluğu ters yönden sınar |
| Tek dönüştürücü var, aile ile model karışıyor | Yönlü aile terimi dönüşüm matrislerinden tanımlanamaz (MASA Bölüm 1). İddia bu yüzden aile karşıtlığına değil aile içi müdahalelere dayanır; aynı ailedeki iki modelin S farkında aile terimi sadeleşir. Aile düzeyi okuma yalnız ImageNet'teki aynı tarifli çiftlerden yapılır |
| Tarif karışık (ViT'de AdamW, ResNet'te SGD, 224 büyütme) | Her müdahale kendi ailesinin tarifini aynen tutar; ImageNet çiftlerinde iki aile tek tarifle eğitilmiştir |
| XCiT zaten CNN gibi davranıyor | XCiT-S12 hem konvolüsyonlu yama gövdesi taşır hem ImageNet-1k ön eğitimli XCiT'ten CIFAR'a ince ayarlanmıştır (Debenedetti ve ark., arXiv 2209.07399, ar5iv metni); iki aday neden bu modelde birlikte değişir, tasarım bunları ayırır |
| Logit ölçeği sonradan seçildi | Seçim mevcut havuzda yapılmıştır (Bölüm 3) ve yeni bloklar için bu belgeyle önceden yazılır; oran ölçeği her tabloda yanında verilir |
| İki tohum azdır | Karar her iki tohumun eşiği ayrı ayrı geçmesini ister; gürültü tabanı üç tohumlu C1 modellerinden gelir |
| Panel yalnız CNN'dir, CNN'e özgü aktarım ölçülüyor | İkincil panel XCiT S/M/L'dir; bugün ViT-Tiny XCiT'e karşı da zayıftır (tc 9.81'e karşı 13.81, logit farkı 0.39; PANEL1 `karsitlik.target_correct`, fark türetilmiş) |

## 3. Mevcut kanıt ne diyor

Havuzun dört dış gürbüz CNN'i (Wong2020, Engstrom2019, Carmon2019, Gowal2020) panel alındığında, logit hedef-doğru ölçekte ResNet-18 ile ViT-Tiny arasındaki kaynak karşıtlığı 0.493'tür ve dört panel üyesinin dördünde de pozitiftir (0.411 ile 0.560); hedef karşıtlığı −0.257'dir ve dördünde de negatiftir (PANEL3). ViT-Tiny'nin S değeri (−2.106) bandın alt ucunun (Wong, −1.661) 0.445 altında, T değeri (−1.433) ise bandın içindedir (−1.683 ile −1.176). Kaynak okuması bu nedenle dış referansla ve model düzeyinde savunulabilir; ViT-Tiny sıradan bir hedef, aykırı bir kaynaktır.

Çift hücreleri uydurmaya hiç girmeden panelden yapılan dış örneklem öngörüsü logit ölçeğinde çift asimetrisinin büyük kısmını verir: hedef-doğruda 0.236'ya karşı gözlenen 0.337, her-ikisi-doğruda 0.588'e karşı 0.731; panel üyelerinin tek tek öngörüleri tutarlıdır (tc'de 0.218 ile 0.257) (PANEL2). Oran ölçeğinde ise aynı öngörü 1.60 puana karşı gözlenen 4.81'dir ve üyeden üyeye 0.75 ile 3.13 arasında oynar. Buradan iki sonuç çıkar. Birincisi, makalenin oran ölçeğindeki 3x3 ayrıştırması (+5.13 kaynak, −2.03 hedef; FÖY:390) seçilen referansa bağlıdır ve sert bir hakem bunu havuz verisiyle gösterebilir; ayrıştırma logit ölçeğine ve dış panele taşınmalıdır. İkincisi, logitte kalan çifte özgü artık (tc 0.10, bc 0.14) on CNN-CNN çiftinin en büyük artığının (0.048 ve 0.038) iki ila dört katıdır; küçük ama gerçek bir çift terimi vardır ve raporlanmalıdır.

Ham oranla hedef-doğru arasında kaynak karşıtlığının işareti korunur (5.18'e karşı 5.95; oran 0.871, panel hedeflerinin doğruluğundan türetilen ortalama 1−e değeri 0.874, FÖY:940-944), hedef karşıtlığı ise işaret değiştirir (+5.33'e karşı −4.35; PANEL1). Özdeşlik böylece somut bir işe yarar: sabit hedefe karşı kaynak karşılaştırmaları koşullama protokolüne işaret bakımından duyarsızdır, hedef karşılaştırmaları duyarlıdır. Bu, DURUM A1 itirazına verilebilecek en iyi yanıttır.

Standart rejimde de ViT_Tiny_clean hem en zayıf kaynak hem en az duyarlı hedeftir (FÖY:1412; Standard WRN'den hedef-doğru 84.05'e karşı 7.62, FÖY:1420). Havuz yalnız C1 çift 1 kontrol noktalarını içerdiği için (FÖY:937-938) yukarıdaki sayılar tek tohumludur. Mevcut kanıt böylece iddianın önkoşulunu destekler, kendisini sınamaz: XCiT'te gövde ile ön eğitim, ViT-Tiny'de mimari, veri rejimi ve doğruluk birlikte değişmektedir.

## 4. Deney blokları

Bütün bloklarda saldırı mevcut `experiments/c1_c3_transfer_matrix.py` ile PGD-10, L∞'dur; birincil ölçek logit hedef-doğru, ikincil ölçekler oran ölçeğinde dört protokoldür ve örnek bazlı kayıt tutulur. Çıktılar `results/q1/` altına yazılır (tez karantina kuralı).

### B1. CIFAR-10 sabit panel (eğitim yok)

Amaç önkoşulu üç tohumda doğrulamak, gürültü tabanını kurmak ve doğruluk ile kapasiteyi gözlemsel olarak denetlemektir. Modeller C1 ResNet-18 AT ile ViT-Tiny AT (üç tohum, `best.pth`; `last.pth` duyarlılık), birincil panel Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled ve Gowal2020Uncovering_28_10_extra (diskte), ikincil dönüştürücü paneli XCiT-S12 (konteyner önbelleğinden `models/robustbench_zoo`'ya alınır), XCiT-M12 (temiz 91.30) ve XCiT-L12 (91.73), düşük doğruluklu CNN Andriushchenko2020Understanding (PreActResNet-18, temiz 79.84, AA 43.93) ve ön eğitimli CNN Hendrycks2019Using'dir (WRN-28-10, temiz 87.11); değerler 29.10'da RobustBench `model_info` dosyalarından okunmuştur. Veri CIFAR-10 test kümesi, n = 10000, ε = 8/255, α = 2/255. Ölçülen nicelikler S(m), T(m) ve tohum başına Δ0 = S(R0) − S(V0)'dır; keşifsel olarak E2'de saklı epok kontrol noktalarından (tohum 1, iki mimari, 10'ar epok) S'nin temiz doğrulukla model içi eğimi çıkarılır.

Öngörü: Δ0 her tohumda en az 0.30 logittir (çift 1'de 0.493); XCiT-M12, XCiT-L12 ve Andriushchenko bant içinde (bant ± 0.10) kalır. Çürütme: Δ0 herhangi bir tohumda 0.15'in altındaysa zayıf kaynaklık tohuma özgüdür ve B2 başlatılmaz; Andriushchenko bandın 0.30 altına düşerse doğruluk tek başına zayıf kaynak üretiyor demektir ve manşet doğruluk yönüne kayar. GPU: yaklaşık 2 saat (8x8 matris 13.5 dk ve kaynak başına 1.3 ile 1.6 dk, DURUM §5; 15 kaynak ve büyük XCiT için üç kat pay, yörüngeler için 0.5 sa). İndirme yaklaşık 1.3 GB tahmin edilir (boyutlar doğrulanmadı); kullanıcı başlatır.

### B2. Sabit tarifte nedensel müdahaleler (altı çekişmeli eğitim)

Üç kol, ikişer tohumla. V_IN, `timm` `vit_tiny_patch16_224.augreg_in21k` ağırlığıyla başlatılan ViT-Tiny'dir (Apache-2.0; 21k kafasıyla 9.74M parametre, HF kartı); tarif C1 ViT ile aynıdır: 200 epok temiz eğitim (AdamW, lr 1e-3, bs 128), ardından karışık kayıplı AT (lr 1e-3, bs 64, patience 20) (`logs/C1_clean_vit_2002.log:1-5`, `logs/C1_at_vit_2002.log:1-6`). V_CS, Xiao ve ark.'nın (arXiv 2106.14881, NeurIPS 2021) konvolüsyonlu gövdesini taşıyan ViT-Tiny'dir: dört 3x3 adım-2 konvolüsyon (24, 48, 96, 192 kanal, BN ve ReLU) ve 1x1 izdüşüm; 12 blok korunur ve bu, Xiao'dan sapma olarak yazılır (yaklaşık +0.1M parametre, türetilmiş hesap); sıfırdan, aynı tarifle. R_20, eğitim kümesinin sınıf dengeli %20'siyle (48000 içinden 9600, sabit indeks dosyası, doğrulama bölmesi aynı) C1 ResNet tarifiyle eğitilen ResNet-18'dir. Tohumlar 2001-2002 ve 1001-1002'dir. Her model B1 paneline eklenir ve tohum eşli R0 ya da V0 ile dört protokolde çift asimetrisi verir.

Ölçülen nicelikler kapanma oranı φ(V_x) = [S(V_x) − S̄(V0)] / Δ̄0, açılma oranı ψ(R_20) = [S̄(R0) − S(R_20)] / Δ̄0 ve R0 ile V_IN arasındaki çift asimetrisidir. Önceden yazılan manipülasyon denetimi: V_IN temiz doğruluğu V0'ın (73.53, FÖY:17) en az 5 puan üstünde olmalıdır, yoksa kol "müdahale tutmadı" diye raporlanır; R_20 için 70 ile 80 arası beklenir, tutmazsa yorum doğruluk eş değişkeniyle yapılır.

Öngörü (veri rejimi hipotezi H_D): φ(V_IN) her iki tohumda en az 0.6, ψ(R_20) her iki tohumda en az 0.5; R0 ile V_IN arasındaki asimetri hedef-doğruda en çok +1, her-ikisi-doğruda en çok +2 puandır (bugün +4.36 ve +8.27, FÖY:54-55) ve işaretin dönmesi Mahmood yönünün kendi hattımızda üretilmesi anlamına gelir. V_CS ayrıştırıcı koldur: H_D altında φ 0.25 ile 1 arasında, yama gövdesi hipotezi H_T altında en az 0.6, dikkat mimarisi hipotezi H_A altında en çok 0.25 beklenir. Çürütme: φ(V_IN) ve ψ(R_20) iki tohumda da 0.25 ya da altındaysa H_D düşer.

GPU: V_IN tohum başına 3.35 sa tipik, 7.5 sa en kötü (temiz 200 epok 1.31-1.38 sa; AT erken durdurmalı 1.82-1.89 sa, tam 100 epok 6.01-6.15 sa; DURUM §5, `TIMING.md` C1_at_vit_2002/2003 6806 ve 7094 sn); V_CS 3.7 ve 8.3 sa (gövde yükü için 1.1 çarpanı, ölçülmedi); R_20 0.56 ve 0.70 sa (ResNet temiz 0.63-0.68 sa, tam AT 2.66-2.78 sa, beşte bir veri). Altı eğitimin toplamı 15.2 sa tipik, 33.0 sa en kötüdür; değerlendirme 0.5 sa ekler. Kullanıcı tmux'ta başlatır. GPU'suz kod önkoşulları: `--train-subset` bayrağı, `vit_tiny_convstem` kaydı, `timm` etiket seçimi ve ViT girdi normalizasyonunun ön eğitimli ağırlıkla uyumu.

### B3. ImageNet aynı tarifli panel (eğitim yok, indirmeyi kullanıcı yapar)

Amaç aile düzeyi iddiayı tek tarif ve eşleşmiş doğrulukla, büyük veri rejiminde sınamak ve gövde etkisini ölçekte görmektir. Singh ve ark. (arXiv 2303.01870, NeurIPS 2023; `github.com/nmndeep/revisiting-at`) aynı tarifle 300 epokluk bir 2x2 yayımlamıştır: ViT-S 69.2/44.0, ViT-S-CvSt 72.5/48.1, ConvNeXt-T 72.4/48.6, ConvNeXt-T-CvSt 72.7/49.5; ayrıca ViT-B ile ConvNeXt-B (50 epok, 73.3/50.0 ve 75.6/54.3) ve CvSt sürümleri (250 epok, 76.3/54.7 ve 75.9/56.1) vardır (temiz/AA, README). Bai ve ark. (arXiv 2111.05464; `github.com/ytongbai/ViTs-vs-CNNs`) DeiT-S 66.50/35.50 ile ResNet-50-GELU 67.38/35.51'i aynı PGD-1, ε = 4/255 tarifiyle verir. Liu ve ark. (arXiv 2302.14301) Swin-B 76.16/56.16 ile ConvNeXt-B 76.02/55.82'yi RobustBench'te yayımlar; tarif ortaklığı bu oturumda doğrulanmadı. Referans olarak Salman2020Do_R50 ve ImageNet XCiT-S12 eklenir. Veri ImageNet doğrulama kümesinden sınıf başına beş görüntü (n = 5000), PGD-10, ε = 4/255, α = 1/255; 224 kırpma bir kez üretilir, her model normalizasyonunu kendi içinde uygular.

Ölçülen nicelik aynı tarifli her çift için ΔS = S(dönüştürücü) − S(CNN)'dir (panel, çiftin dışındaki modeller) ve Singh içinde S(ViT-CvSt) − S(ViT)'dir. Öngörü (H_D): altı aynı tarifli çiftin (Singh S yama, S CvSt, B yama, B CvSt, Bai, Liu) hiçbirinde ΔS −0.25 logitin altına inmez, en az dördünde ±0.25 sınırıyla TOST eşdeğerliği sağlanır ve işaretler karışıktır. Çürütme: altı çiftin altısında ΔS negatif ve en az dördünde −0.25'in altındaysa dönüştürücülerin zayıf kaynaklığı ölçekte de sürer. GPU yaklaşık 3 sa'tir; depoda ImageNet süre kaydı olmadığı için değer tahmindir ve 200 görüntülük bir pilotla (5 dk altı) ayarlanır. ImageNet doğrulama kümesi Hugging Face'te kapılıdır, yalnız ticari olmayan araştırmaya açıktır (`ILSVRC/imagenet-1k` kartı); boyutu (yaklaşık 6.4 GB) ve kontrol noktalarının toplamı (4 ile 6 GB) tahmindir. Singh ve Bai depolarında lisans yazmaz ve Singh README'si yama gövdeli dört model için aynı bağlantıyı verir; indirmeden önce denetlenmelidir.

### B4. CIFAR-100 panel tekrarı (eğitim yok, isteğe bağlı)

Q1 CIFAR-100 ResNet-18 ve ViT-Tiny (üçer tohum), Pang2022 WRN-28-10 (diskte), XCiT S/M/L, Hendrycks2019Using ve Addepalli2022Efficient_RN18 (CIFAR-100). Öngörü: Δ0 her tohumda en az 0.30 ve XCiT bant içinde; çürütme: herhangi bir tohumda 0.15 altı. GPU yaklaşık 1 sa, indirme yaklaşık 1.5 GB (tahmin), kullanıcı başlatır. Bütçe aşılırsa ilk düşen bloktur.

## 5. Sonuç örüntüleri ve hangi makaleyi verdikleri

| Örüntü | Okuma | Manşet |
|---|---|---|
| φ(V_IN) ≥ 0.6, ψ(R_20) ≥ 0.5, ImageNet'te eşdeğerlik | Veri rejimi | Bölüm 1'deki iddia |
| φ(V_CS) ≥ 0.6, V_IN ve R_20 ≤ 0.25, Singh'te ViT-CvSt ViT'den güçlü | Yama gövdesi | "The patchify stem, not attention, makes adversarially trained ViTs weak transfer sources" |
| Bütün kollar ≤ 0.25, ImageNet'te altıda altı negatif | Mimari sabiti | "Adversarially trained ViTs are weak transfer sources across initialisation, stem and scale" |
| V_IN tutar, R_20 tutmaz | Dönüştürücüye özgü veri açlığı | "ImageNet initialisation removes the ViT's source deficit; data scarcity does not create one in a CNN" |

Karıştırıcılar el ile değiştirildiği için her satır yayımlanabilir; Δ0 B1'de çökerse B2 başlatılmaz (Bölüm 8).

## 6. İstatistik planı

Tahmin edilen nicelikler S, T, iki model arasındaki S farkı, φ, ψ ve dört protokolde çift asimetrisidir. Birincil ölçek logit hedef-doğrudur; oran ölçeği, ham ve her-ikisi-doğru betimsel olarak verilir, karara girmez. Belirsizlik üç düzeyde raporlanır: görüntü düzeyinde, her yinelemede bütün hücreler için aynı indekslerle yeniden örneklenen eşli bootstrap (B = 2000, yüzdelik aralık); eğitim düzeyinde, her tohum ayrı ayrı (n = 3 olan V0 ve R0 için koşum düzeyi t aralığı, n = 2 olan kollarda iki değer yan yana, SD yazılmadan); panel düzeyinde, karşıtlığın panel üyelerinde işaret tutarlılığı (dörtte dört). Birincil aile üç CIFAR müdahale karşıtlığıdır (V_IN, V_CS, R_20); tek yönlü bootstrap p değerleri tohumların büyüğü alınarak Holm ile düzeltilir. İkincil aile altı ImageNet çiftidir; Holm ve ±0.25 sınırlı TOST, ayrıca altı çift üzerinde işaret testi (tek yönlü en küçük p = 1/64). ImageNet kontrol noktaları tek eğitimdir, bu yüzden oradaki çıkarım bu kontrol noktalarına koşulludur ve böyle yazılır. Eşikler (0.25, 0.5, 0.6, ±0.25) bu belgeyle önceden kaydedilir; B1'de V0'ın tohumlar arası S sapması 0.1·Δ̄0'ı aşarsa eşikler o sapmanın üç katına yükseltilir. Post-hoc güç hesabı yapılmaz.

## 7. Başlık, özet ve katkılarda ne değişir

Başlık Bölüm 5'te gerçekleşen satırdan alınır. Özet şu sırayı izler: soru (asimetri ailenin mi özelliği), ölçüm (koşullama protokolü ve özdeşlik; kaynak karşılaştırmaları protokole işaret bakımından duyarsız, hedef karşılaştırmaları duyarlı), tanımlama (iki modelli asimetri ayrıştırılamaz, sabit dış panele karşı kaynak gücü ayrıştırılır; tezin 5.1.1'deki "ayrıştırılamıyor" hükmü iki model için doğru kalır, makale model düzeyinde konuşur), müdahaleler ve ImageNet. Katkılar dörde iner: çift hücrelerini kullanmayan dış panelle logit ölçekte kaynak ve hedef etkilerinin tanımlanması, aynı tarifte üç müdahale, üç bağımsız grubun aynı tarifli ImageNet modelleriyle ölçek tekrarı ve kısaltılmış protokol-özdeşlik katmanı. DURUM'daki A2, A3, A4, A5, A6, A7 ve A9 itirazları bu tasarımda doğrudan yanıt bulur.

## 8. Geri çekilme iddiası

İddia tutmazsa iki geri çekilme sırayla kullanılır. B2 ve B3 H_A örüntüsünü verirse manşet tersine döner ve daha güçlü hâle gelir: ViT'nin zayıf kaynaklığı başlatma, gövde, veri kıtlığı ve ImageNet ölçeği karşısında sürer. B1'de Δ0 tohumlar arasında 0.15'in altına düşerse kaynak okuması makaleden çıkarılır; geriye "sabit dış panele karşı kaynak karşılaştırmaları koşullama protokolüne işaret bakımından duyarsız, hedef karşılaştırmaları duyarlıdır; çift asimetrisi iki modelle ayrıştırılamaz" bulgusu ile mevcut protokol ve özdeşlik katkısı kalır. Bu en dar sürüm de bugünkü metinden daha savunulabilirdir.

## 9. Bütçe ve kaynak durumu

| Blok | Eğitim | GPU-saat (tipik / en kötü) | Başlatan |
|---|---|---|---|
| B1 | 0 | 2.0 / 2.0 | kullanıcı (indirme 1.3 GB) |
| B2 | 6 AT (+6 temiz aşama) | 15.7 / 33.5 | kullanıcı |
| B3 | 0 | 3.0 / 3.0 | kullanıcı (ImageNet ve 4-6 GB) |
| B4 | 0 | 1.0 / 1.0 | kullanıcı, isteğe bağlı |
| Toplam | 6 | 21.7 / 39.5 | |

En kötü durum 40 sınırının hemen altındadır; B2 tipik süreyi %50 aşarsa önce B4, sonra B1 yörüngeleri düşer. Şimdi masa başında yapılabilecek olan, kod önkoşulları ile PANEL betiklerinin `experiments/` altında bootstrap'lı bir betiğe dönüştürülmesidir.

arXiv sayfaları 29.10.2026'da açılıp başlık ve yazarla doğrulanan kaynaklar: 2104.02610, 2106.04169, 2106.02105, 1809.02861, 2303.01870, 2111.05464, 2209.07399, 2302.14301, 2106.14881. Doğrulanmayanlar: Bai ve ark.'nın yayın yeri, Liu ve ark.'nda tarif ortaklığı, Singh ve Bai kontrol noktalarının lisansı ve boyutu.
