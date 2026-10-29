# Hakem raporu: konsey 29.10.2026, üç öneri (P1, P2, P3), mercek: uygulanabilirlik ve maliyet

Üç önerinin bütçe tabloları kâğıt üzerinde 40 GPU-saat ve 6 eğitim sınırına sığıyor. Ancak üçü de depoda olmayan kodu "hazır" sayıyor. Üçünde de ön eğitimli ağırlıkların girdi normalizasyonu ya eksik ya yanlış kurulmuş. P1'in kendi bütçe bekçisi, gerçekçi bir hız tahmininde manşetin dayandığı hücreyi tek tohuma düşürüyor. P3'ün yasası da kendi elindeki havuz dışı veride, kendi koyduğu çürütme ölçütüyle zaten düşüyor. Uygulanabilirlik açısından en sağlam yol, P1'in 2x2 çekirdeğini P2'nin B1 panel ölçümüyle birleştirmek ve ImageNet bloklarını çıkarmaktır.

Genel hüküm: üçü de düzeltilebilir. Güven düzeyi orta-yüksek. Sayıların hepsi aşağıda dosyasıyla doğrulandı.

## Doğrulanan dayanaklar

Önerilerin sayıları kaynağında açıldı ve tuttu. P1'in yörünge oranları `results/q1/e3_akolu_v2/A_c10_vit_s200{1,2,3}_ep0031.json` dosyalarında `oranlar_geri.target_correct` alanında 13.80, 15.23 ve 15.75; `_ep0100` dosyalarında 9.85, 10.43 ve 10.70. ResNet tohum 1001'de epok 1 için 13.44, epok 100 için 18.76. FÖY:1390-1392'de seçilen epoklar 25/18/19 (ViT) ve 51/56/57 (ResNet). FÖY:1039'da eğim +0.796. P2'nin Δ0 değeri `_P2_panel_logit_ayri.json` dosyasında `target_correct.kaynak_R_eksi_V[0]` = 0.4927; S bandı ve ViT-Tiny için −2.106 da aynı dosyada. P3 için `_p3_carpimsal_yasa_masa.json` dosyasının `havuz_AT7` kısmında λ = 1.0145, R²(λ=1) = 0.9530, işaret 21/21. Epok kontrol noktaları diskte: E2 ResNet ve ViT için koşu başına 101 dosya, CIFAR-100'de de var. Konteynerde ağ erişimi var ve küçük ağırlıkları (DeiT-Tiny, torchvision ResNet-18) indirmek 1 GB sınırının altında kalıyor.

## Ortak bulgular (üç öneriyi birden ilgilendiriyor)

[O1] Ön eğitimli ağırlıkların girdi normalizasyonu sorunu. Veri hattı yalnız `ToTensor` uyguluyor (`src/data/transforms.py:31,44`). `vit_tiny` sarmalayıcısı da yalnız 32'den 224'e büyütme yapıyor (`src/models/vit.py:383-395`). DeiT ve torchvision ağırlıkları ImageNet ortalama ve sapmasını, augreg ağırlıkları 0.5/0.5 değerlerini bekliyor. Normalizasyon eklenmezse ImageNet başlatması zayıflamış bir başlatma olur ve başlatma etkisi sıfıra doğru yanlı ölçülür. P2 bu sorunu ön koşul olarak yazmış. P1 ve P3 hiç anmıyor.

[O2] İyileyici, sınıf adına bakılarak seçiliyor. Sınıf adında 'vit', 'vision' ya da 'transformer' geçmiyorsa sessizce SGD kullanılıyor (`src/training/adversarial_trainer.py:149-170`, `trainer.py:80-105`). Yeni R224 sarmalayıcısı (P1) ya da evrişimli gövdeli ViT (P2'deki V_CS) yanlış adlandırılırsa tarif bozulur. ViT'de AdamW için ağırlık azaltma 0.05 ve öğrenme oranı tavanı 1e-3; bu ikisi beyan edilmeli.

[O3] Transfer betiği kare n×n matris üretiyor. Bütün modeller GPU'ya birlikte yükleniyor ve çekişmeli örnekler saklanmıyor (`experiments/c1_c3_transfer_matrix.py:120-190`). ε sabit kodlu: EPS = 8/255 (satır 25). ImageNet yolu yok (`--dataset` yalnız CIFAR ve SVHN kabul ediyor).

[O4] Disk %95 dolu, 57 GB boş (`df -h`). Bu, her epokta kayıt ve ImageNet indirmesi planlayan öneriler için gerçek bir kısıt.

[O5] GPU başka bir projeyle paylaşılıyor. E2'deki ViT epoğu (213-219 s) C1'dekinden (179-182 s; `TIMING.md` 6806/38, 7094/39) yavaş. GPU-saat bütçeleri ayrıcalıklı kullanım varsayıyor. Takvim sıralı bir kuyrukla kurulmalı ve günlüklere duvar saati yazılmalı.

## P1, müdahale (2x2: mimari × başlatma)

Hüküm: düzeltilebilir, 6/10.

[P1-a] Bekçi, manşetin dayandığı hücreyi kesiyor. P1, R224 epok süresini ViT'nin 1.2 katı kabul etmiş: AT için 263 s. Bu oran ölçülmemiş. CNN verim katsayısını korursak gerçekçi değer daha yüksek çıkıyor. CIFAR ResNet-18 yaklaşık 0.56 GMAC ile epokta 93-99 s, ViT-Tiny yaklaşık 1.08 GMAC ile 213-219 s sürüyor (`00_durum_dosyasi.md` §5). 224 girdili torchvision ResNet-18 yaklaşık 1.82 GMAC olduğundan epok tahmini 310 s civarında, yani ViT'nin yaklaşık 1.43 katı. GMAC değerleri model kartlarından alındı, depoda doğrulanmadı. Bu hızla tavan şöyle çıkıyor:

- R224-scr: 2.1 + 5.2 = 7.3 sa
- R224-IN: 0.3 + 5.2 = 5.5 sa
- V-IN: 3.86 sa

Altı eğitim yaklaşık 33.3 sa; öteki bloklar eklenince 41.9 sa ediyor ve 40 sınırını aşıyor. P1'in kendi kuralına göre pilot ölçüm 263 s'yi geçerse R224-IN'in ikinci tohumu iptal ediliyor. Böylece θ_arch|IN eşdeğerlik sınaması (TOST, manşetin üçüncü koşulu) 2'ye karşı 1 koşuyla, havuzlanmış 5 serbestlik derecesi ve Holm düzeltmesi altında yapılmak zorunda kalıyor. Bu bir güç hesabı değil, tasarımın kendi kurgusundan çıkan bir durum.

[P1-b] Blok 2'nin maliyeti yaklaşık üç kat düşük hesaplanmış. 78 kontrol noktası, 6 C1 modeli ve 10 panel modeli toplam 94 modeldir. Mevcut kare betikte bu iş yaklaşık 94 × (1.15 + 94 × 0.07) dk ≈ 12 sa sürer; katsayılar P3'ün 8x8 kalibrasyonundan alındı. P1 bu blok için 3.5 sa tavan yazmış. Bu tavanı tutmak için iki yeni kod gerekiyor: kaynaktan panele dikdörtgen bir mod ve panel çekişmeli örneklerinin önbelleğe alınması. İkisi de Blok 1'in kod listesinde yok. PGD-50 için `--steps` bayrağı da eksik; betikte adım sayısı sabit.

[P1-c] Bazı kırmızı çizgiler ve yan riskler doğru ayrılmamış. "5 dakikalık pilot" tam bir R224 AT epoğunu ölçemez, çünkü epok en az 263 s artı yükleme süresi tutuyor. Pilot yaklaşık 50 iterasyonla yapılıp sonuç dışa kestirilmeli. 60 epokluk tavan, C1 ResNet'in seçtiği 51-57. epoklara 3 ila 9 epokluk pay bırakıyor. Üstelik bu C1 epokları 32x32 girdi ve SGD ile elde edilmişti; AdamW ve 224 girdiyle en iyi epoğun nerede olacağı bilinmiyor. V-scr ise 100 epok tavanla eğitildi. Bu, hücreler arasında asimetrik bir kırpma riski doğuruyor. Her epokta kayıt yaklaşık 13 GB yer kaplar ([O4]). Normalizasyon eksiği için bkz. [O1].

Hükmü 'ayakta'ya çevirecek düzeltmeler:

1. Bekçinin keseceği kalem değişmeli. R224-IN iki tohumda kalmalı; bütçe Blok 2'deki yörünge yoğunluğu (78 kontrol noktasından 24'e) ve Blok 3'teki PGD-50 kesilerek açılmalı.
2. Pilot, 50 iterasyonluk bir zaman ölçümü olmalı.
3. Normalizasyon katmanı eklenmeli ve V-scr ile farkı beyan edilmeli.
4. Dikdörtgen ölçüm modu ile önbellek kodlanmalı; `--steps` bayrağı eklenmeli.
5. AdamW'yi zorlayan bir bayrak eklenmeli (sınıf adına güvenilmemeli).
6. AT tavanı 80 epoğa çıkarılmalı ya da kırpılan koşu ön kayıtta tanımlanmalı.

## P2, dış geçerlilik (veri rejimi)

Hüküm: düzeltilebilir, 5/10.

[P2-a] B3'teki "altı aynı tarifli ImageNet çifti" sayısı şişirilmiş. `_rb_imagenet_P2.json` dosyasına göre RobustBench'te yalnız Singh'in evrişimli gövdeli modelleri (ViT-S/B-ConvStem ve ConvNeXt-T/B-ConvStem) ile Liu'nun Swin-B ve ConvNeXt-B modelleri var. Singh'in yama gövdeli ViT-S/B ve ConvNeXt modelleri ile Bai'nin DeiT-S ve R50-GELU modelleri katalog dışında; erişim ve lisansları doğrulanmadı ve P2 bunu kendisi de not ediyor. Gerçekte elde kalan en fazla üç çift. Bunların ikisindeki ViT'ler saf yama gövdeli değil, Liu çiftinde de tarif ortaklığı doğrulanmadı. Bu durumda "6/6 negatif" çürütme ölçütüne ulaşılamaz. İşaret testinde ulaşılabilir en küçük p 1/8 olur. Aile düzeyindeki cümle sınanamaz hale gelir.

[P2-b] B3, P2'nin yazdığı gibi "mevcut betikle" yapılamaz. Yeni kod gerekiyor: ImageNet yükleyicisi, ε'un parametreye bağlanması, RobustBench ImageNet yüklemesi ve modellere göre değişen ön işleme (Crop288, Res256Crop224, BicubicRes256Crop224) ([O3]). İndirme yaklaşık 10-12 GB tutuyor ve disk %95 dolu. B3 için 3 GPU-saat ölçüme dayanmıyor, tahmin.

[P2-c] V_IN müdahalesinin tutmama riski yüksek. Tarif şöyle: in21k ağırlığı üzerine 200 epok temiz eğitim, AdamW ile lr 1e-3 (`trainer.py:89-95` tavanı tam bu değer) ve ağırlık azaltma 0.05. Bu, sıfırdan eğitimle aynı uzunlukta ve yüksek oranlı bir ince ayar; ön eğitimin izini büyük ölçüde silebilir. Manipülasyon denetimi ("en az 5 puan") bu yüzden başarısız olabilir ve manşet sınanamadan kalır. En kötü durum bütçesi 39.5 sa, yani yalnız 0.5 sa pay bırakıyor. Üstelik iki kalem hiç ölçülmemiş: evrişimli gövde için 1.1 çarpanı ve ImageNet süresi. Ek olarak çürütme kuralı asimetrik: veri rejimi hipotezi H_D, ancak φ ve ψ iki tohumda da ≤ 0.25 çıkarsa düşüyor. 0.25 ile 0.6 arasındaki bölgenin ne anlama geldiği tanımlanmamış.

Düzeltmeler:

1. B3 bütünüyle çıkarılmalı ya da yalnız RobustBench'teki iki ConvStem çiftiyle keşifsel bir ek olarak kalmalı.
2. V_IN, kısa ve düşük oranlı bir ince ayarla eğitilmeli (P1'deki 30 epok, lr 1e-4 tarifi gibi) ve normalizasyon eklenmeli.
3. 0.25 ile 0.6 arası bölge için önceden bir geri çekilme cümlesi yazılmalı.
4. V_CS sınıf adı 'vit' içermeli ya da AdamW bayrakla zorlanmalı.
5. B1 korunmalı. Ucuz (yaklaşık 2 sa), mevcut kare betikle yapılabiliyor ve en değerli ölçüm aracı.

## P3, kuram (kırılganlık-benzerlik yasası)

Hüküm: düzeltilebilir, 4/10.

[P3-a] Yasa, havuz dışındaki mevcut veride kendi çürütme ölçütüyle düşüyor. `_p3_carpimsal_yasa_masa.json` dosyasının `A_kolu` kısmında n = 100 yörünge noktası var. Bu noktalarda R²(λ=1) = 0.201 ve kesişimsiz λ = 1.878. P3'ün ön kayıt eşiklerine göre R² < 0.70 ve λ, [0.77; 1.30] aralığının dışında. Öneri metninin tablosunda yalnız r = 0.958 ile eğimler (1.46 ve 2.07) görünüyor; R² = 0.20 yazılmamış. Manşet "herhangi iki model" diyor, epok kontrol noktaları da modeldir. "Yakınsamış modeller" kısıtı sonradan konmuş. Daha da önemlisi Blok 2, ResNet'in 2-8 ve 10. epok kontrol noktalarını yeni çift olarak matrise ekliyor. Bu noktalar test kümesine girerse P3 yasası tasarım gereği çürür; girmezse sınama alanı sonradan daraltılmış olur. Ayrıca `log_oran_artik_rms_lambda1` ile `log_tau_simetri_ihlali_rms` değerleri birebir aynı (0.08967). Bu, yasanın τ simetrisinin yeniden yazılmış hali olduğunu gösteriyor; "sıfır parametreli" bir sınama değil.

[P3-b] T1 tanımlandığından farklı bir model üretir. `--timm-pretrained` bayrağı konteynerdeki timm 1.0.27'de `vit_tiny_patch16_224.augreg_in21k_ft_in1k` ağırlığını yüklüyor (bu doğrulandı). Yani başlatma ImageNet-21k, normalizasyon yok ve öğrenme oranı tavanı 1e-3. T3'ün süre dayanağı C1 öncesi, eski GPU'da tutulmuş bir günlük (`logs/vit_cifar_tiny_at.log`); o koşu 59. epokta bitiyor ve doğrulama Adv değeri %22-23'te kalıyor. T3 çok zayıf bir model olacağı için w oranı çok büyük çıkar ve işaret uyumunu kolayca şişirir.

[P3-c] Blok 5 (ImageNet) "bütçeye sayılmadı" diye yazılmış. Bu, 40 GPU-saatlik toplam sınırı kuralını çiğniyor. Ayrıca ImageNet yolu kodda yok ([O3]). Eğitimsiz bloklar (Blok 2 için yaklaşık 1.3 sa, Blok 4 için yaklaşık 3.5 sa) kare betiğe tam uyuyor ve tahminleri tutarlı. Uygulanabilirlik bakımından P3 en ucuz ve en hazır öneri, ama yasa zaten zedelenmiş durumda.

Düzeltmeler:

1. A_kolu sonucu (R² = 0.20) metne yazılmalı.
2. "Yakınsamış model" Blok 2'den önce operasyonel olarak tanımlanmalı (örneğin seçilen ya da son epok, doğrulama PGD platosu) ve epok kontrol noktaları birincil sınamadan çıkarılmalı.
3. Manşet "yakınsamış AT modelleri" diye daraltılmalı.
4. T1 için etiket ve normalizasyon açıkça seçilmeli.
5. ImageNet bütçeye sayılmalı ya da öneriden çıkarılmalı.
6. T3 işaret sınamasında ayrı raporlanmalı.

## İddia ve kanıt tablosu (uygulanabilirlik)

| # | İddia | Kanıt | Güç | Hüküm |
|---|---|---|---|---|
| 1 | P1 için 37.7 sa tavan | R224 hızı 1.2× varsayımı, ölçüm yok | zayıf | gerçekçi tahminde 41.9 sa |
| 2 | P1 Blok 2 için 3.5 sa | kaynak başına 1.3-1.6 dk | zayıf | kare betikte yaklaşık 12 sa |
| 3 | P2'de altı ImageNet çifti | `_rb_imagenet_P2.json` | zayıf | en fazla üç |
| 4 | P2 Δ0 = 0.493 | `_P2_panel_logit_ayri.json` | güçlü (tek tohum) | tutar |
| 5 | P3 λ = 1.015, 21/21 | `havuz_AT7` | güçlü (havuz içi) | tutar |
| 6 | P3 yasası yeni çiftlerde tutar | `A_kolu` R² = 0.201 | olumsuz | şimdiden çürük |
| 7 | T1 "ImageNet ön eğitimli" | timm varsayılan etiketi | doğrulandı | in21k_ft_in1k |

## En sağlam birleşim

Önerilen birleşim P1'in 2x2 çekirdeği (Blok 1, 4 ve 5, yukarıdaki düzeltmelerle) ile P2'nin B1 paneli. P2-B1, kaynak gücünü sabit bir dış panel üzerinde logit ölçeğinde ölçen araç olarak kullanılır, mevcut kare betikle yaklaşık 2 sa tutar. P3'ün eğitimsiz Blok 2'si yalnız keşifsel bir yön analizi olarak kalır. P2-B3 ve P3-Blok 5 (ImageNet) çıkarılır.

Eğitim sayısı 6. GPU tahmini yaklaşık 33 sa eğitim, 2 sa panel ve 3 sa değerlendirme, toplam yaklaşık 38 sa. Bütçeyi bu sınırda tutmak için P1'in Blok 2 ve Blok 3'ü budanır.

Kabul için tek koşul şudur: R224-IN dahil dört hücre iki tohumla tamamlanmalı ve ImageNet başlatması doğru normalizasyonla yapılmalı. Bu ikisi olmadan manşetteki eşdeğerlik koşulu sınanamaz.

## Hakemin soracağı sorular

ImageNet başlatmasının etkisi normalizasyon eksikliğinden mi kaynaklanıyor? Ancak [O1] düzeltilirse "hayır" denebilir.

R224, ViT ile aynı FLOP düzeyinde mi? Değil, ResNet yaklaşık 1.7 kat fazla MAC kullanıyor. Kapasite ve hesap eşleşmesi değil, yalnız girdi hattı eşleşmesi iddia edilmeli.

Panel neden ağırlıkla CNN'lerden oluşuyor? P1'in panelinde üç XCiT var, P2'nin ikincil panelinde de XCiT bulunuyor. Homojenlik sınaması sonuca bakılmadan önceden kaydedilmeli.

HÜKÜMLER: [{"proposal":"P1_mudahale","verdict":"duzeltilebilir","score":6,"key_attacks":["Bütçe bekçisi manşetin dayandığı hücreyi kesiyor. R224 epoğu ölçülmemiş ve 1.2× varsayılmış (263 s). CNN verimiyle ölçeklenince yaklaşık 310 s çıkıyor (CIFAR ResNet 93-99 s/0.56 GMAC, ViT 213-219 s; GMAC model kartlarından). Bu hızla tavan 41.9 sa olur ve kural R224-IN'in ikinci tohumunu iptal eder, θ_arch|IN eşdeğerlik sınaması 2'ye karşı 1 koşuyla kalır.","Blok 2 yaklaşık üç kat düşük hesaplanmış. c1_c3_transfer_matrix.py kare n×n matris üretiyor ve önbellek tutmuyor; 94 model yaklaşık 12 sa sürer, 3.5 sa değil. Dikdörtgen mod, önbellek ve --steps bayrağı kod listesinde yok.","Normalizasyon eksik: veri yalnız ToTensor (transforms.py:31,44), sarmalayıcıda normalizasyon yok, bu yüzden DeiT ve torchvision başlatması zayıflar ve θ_init|V sıfıra yanlı çıkar. Ayrıca 5 dakikalık pilot tam bir R224 epoğunu ölçemez, 60 epok tavanı C1 ResNet'in 51-57 seçim penceresine dar pay bırakıyor ve disk %95 dolu."],"required_fixes":["Bekçi R224-IN tohumunu değil, Blok 2 yörünge yoğunluğunu (78'den 24'e) ve PGD-50'yi kessin","Pilot 50 iterasyonluk zaman ölçümü olsun","Yeni hücrelere ImageNet normalizasyon katmanı eklensin, V-scr ile farkı beyan edilsin","Kaynaktan panele dikdörtgen ölçüm modu, panel çekişmeli örnek önbelleği ve --steps bayrağı kodlansın","AdamW bayrakla zorlansın (sınıf adına güvenilmesin)","AT tavanı 80 epoğa çıksın ya da kırpılan koşu ön kayıtta tanımlansın"]},{"proposal":"P2_dis_gecerlilik","verdict":"duzeltilebilir","score":5,"key_attacks":["B3'teki altı ImageNet çifti şişirilmiş. RobustBench'te yalnız Singh ConvStem modelleri ve Liu Swin-B/ConvNeXt-B var (_rb_imagenet_P2.json); yama gövdeli Singh ve Bai kontrol noktaları doğrulanmadı. Gerçekte en fazla üç çift kalıyor, ViT'leri saf değil, 6/6 çürütme ölçütüne ulaşılamaz.","B3 mevcut betikle yapılamaz: ImageNet yolu yok, EPS=8/255 sabit kodlu (c1_c3_transfer_matrix.py:25,72). İndirme yaklaşık 10-12 GB ve disk %95 dolu.","V_IN müdahalesi tutmayabilir: in21k ağırlığı üzerine 200 epok, AdamW lr 1e-3 ve ağırlık azaltma 0.05 ön eğitimi silebilir. En kötü durum 39.5 sa ve yalnız 0.5 sa pay var; evrişimli gövde ve ImageNet süreleri ölçülmemiş. Çürütme kuralı asimetrik, 0.25 ile 0.6 arası bölge tanımsız."],"required_fixes":["B3 çıkarılsın ya da yalnız iki ConvStem çiftiyle keşifsel bir ek olarak kalsın","V_IN için kısa ve düşük oranlı ince ayar (30 epok, lr 1e-4) ile normalizasyon kullanılsın","0.25 ile 0.6 arası bölge için önceden bir geri çekilme cümlesi yazılsın","V_CS sınıf adı 'vit' içersin ya da AdamW bayrakla zorlansın","B1 korunsun (yaklaşık 2 sa, mevcut kare betikle çalışıyor)"]},{"proposal":"P3_kuram_olcum","verdict":"duzeltilebilir","score":4,"key_attacks":["Yasa havuz dışı mevcut veride kendi ölçütüyle çürüyor: _p3_carpimsal_yasa_masa.json A_kolu kısmında n=100 nokta için R²(λ=1)=0.201 ve kesişimsiz λ=1.878. Bu değer metinde verilmemiş. Blok 2 epok kontrol noktalarını yeni çift olarak ekliyor, 'yakınsamış model' kısıtı sonradan konmuş.","T1'deki --timm-pretrained bayrağı timm 1.0.27'de augreg_in21k_ft_in1k yüklüyor (doğrulandı); normalizasyon yok ve lr tavanı 1e-3. T3'ün süre dayanağı C1 öncesi eski bir günlük, model zayıf (doğrulama Adv %22-23) ve işaret uyumunu şişirir.","Blok 5 (ImageNet) bütçeye sayılmamış, bu 40 GPU-saat toplam sınırını çiğniyor; ImageNet kod yolu da yok. log oran artığı RMS'i τ simetri ihlali RMS'ine özdeş (0.08967), yani yasa τ simetrisinin yeniden yazılmış hali."],"required_fixes":["A_kolu sonucu (R²=0.20) metne yazılsın","'Yakınsamış model' Blok 2'den önce operasyonel olarak tanımlansın, epok kontrol noktaları birincil sınamadan çıkarılsın","Manşet 'yakınsamış AT modelleri' diye daraltılsın","T1 için etiket ve normalizasyon açıkça seçilsin","ImageNet bütçeye sayılsın ya da çıkarılsın","T3 işaret sınamasında ayrı raporlansın"]}]
