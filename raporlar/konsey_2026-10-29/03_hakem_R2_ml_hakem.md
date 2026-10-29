# Hakem raporu: konsey önerileri P1, P2, P3 (29.10.2026), çekişmeli öğrenme merceği

**Özet (TR):** Üç önerinin üçü de düzeltilebilir. Hiçbiri bugünkü haliyle çürütülemez değil. Hepsinin ortak ve en ağır sorunu şu: P1 ile P2'nin ölçtüğü "kaynak gücü" büyük ölçüde simetrik bir aileler arası benzemezlikten oluşuyor. P3'ün önerdiği yasa ise bugünkü veride tam da iki dikkat tabanlı modelde, kendi eşdeğerlik sınırında bozuluyor. Mevcut havuz verisi yeniden hesaplandı. ViT-Tiny'nin kaynak tarafındaki açığının yaklaşık dörtte üçü hedef tarafında da görülüyor, yani ViT-Tiny her iki rolde de CNN'lere benzemiyor. Yönlü kalıntı ViT-Tiny'de +0,084, XCiT-S12'de ise −0,121 log birimidir ve işaretleri terstir. Bu desen, P1'in başlatma müdahalesi ile P3'ün ölçüm katmanının birleştirilmesini gerektiriyor. En sağlam paket P1'in 2x2 tasarımı, P3'ün ayrıştırması ve P2'nin eğitimsiz B1 bloğundan oluşur.

**Genel:** üçü de büyük revizyon. Güven O-Y.

## Bu raporda yeniden hesaplanan sayılar (betik scratchpad'de, `hakem_kontrol.py`; girdi `results/q1/havuz_cifar10/per_sample_*.npz`, hedef-doğru)

| Nicelik | Değer |
|---|---|
| P3 yasası, 7 AT modeli | λ 1,0145, R²(λ=1) 0,953, 21/21; ayrıca `_p3_carpimsal_yasa_masa.json` `havuz_AT7` ile birebir aynı |
| ViT çıkarılınca | λ 0,915, R² 0,938 (15 çift) |
| Tek model bırakmalı λ | 0,915 (ViT çıkar) ile 1,149 (Gowal çıkar) arası |
| 7 potansiyel ile −log w arası korelasyon | 0,978 (6 sd; "21 çift" sözde yinelemedir) |
| ResNet18_AT→ViT ile ViT→ResNet18_AT | 19,73 / 14,92; log oran 0,279, yasa 0,160, artık **0,119** |
| Yasanın açıkladığı asimetri | 4,81 puanın 2,60'ı (%54) |
| Yönlü artık r_V (6 eş) | 0,119; 0,070; 0,082; 0,057; 0,213; −0,037; ortalama **+0,084** |
| Yönlü artık r_XCiT (6 eş) | altısı da negatif, ortalama **−0,121** |
| log τ, kaynak/hedef tarafı | ViT −1,132/−1,049; öteki altı model ort. −0,697/−0,711; açık −0,435/−0,338 → ViT açığının yaklaşık %78'i simetrik |
| R→XCiT ile V→XCiT | 13,81 / 9,80 (P2'nin 13,81/9,81 değeri tutuyor) |

Doğrulanan öneri sayıları şunlar. P1'in yörünge sayıları tutuyor: geri tc 13,80/15,23/15,75'ten 9,85/10,43/10,70'e, ResNet tarafı 13,44/13,30/14,01'den 18,76/18,35/18,23'e (`results/q1/e3_akolu_v2/*`). FÖY M8.14'teki seçilmiş epoklar 25/18/19 ve 51/56/57; TIMING.md'de 6806 s ve 7094 s. P2'nin `_P2_panel_logit_ayri.json` dosyasında Δ0 0,4927±0,0685, S bandı −1,661 ile −1,365, ViT −2,106. P3'ün M4 değerleri de tutuyor. Tutmayan bir sayı bulunmadı. Sorun yorumda.

## Ortak ölümcül nokta [F0]: "kaynak gücü" bir kaynak niteliği değil

P3'ün Önerme 1(c)'si cebirsel olarak doğru. Tek ViT'li tasarımda CNN'ler arası benzerlik γ, α_V ve β_V'ye birlikte −γ olarak yüklenir. Makalenin +5,13/−2,03 bölüşümü (FÖY:390) tam bu deseni üretir. Havuzda da ViT-Tiny'nin w ile normalize edilmiş açığı iki rolde neredeyse eşit (yukarıdaki tablo). Yani P1 ile P2'nin S(m) niceliği, yani CNN paneline giden hedef-doğru ortalama, panel kırılganlığı ile modelin CNN'lere simetrik benzerliğinin çarpımını ölçer. Mahmood ve ark. 2021 (arXiv:2104.02610) cinsler arası düşük transferi zaten bildirmiştir. Düzeltme her öneri için zorunlu: S ile T birlikte raporlanmalı, birincil kestirilen nicelik w ile normalize edilmiş yönlü artık r = ort[log(T_CV/T_VC) − log(w_V/w_C)] olmalı, simetrik τ ise ayrı ikinci nicelik olarak verilmeli.

## P1, müdahale (duzeltilebilir, 6,5/10)

Güçlü yanı şu: önerilerin içinde karıştırıcıyı müdahaleyle ayıran tek tasarım bu. Girdi hattı (32→224) ile iyileyici eşitleniyor, başlatma iki mimariye de veriliyor ve geri çekilme bölgeleri önceden yazılmış.

**Saldırı 1 (yapı geçerliliği, F0).** "ImageNet başlatmalı ViT güçlü kaynak olur" sonucu büyük olasılıkla "ImageNet başlatmalı ViT CNN'lere daha çok benzer" demektir. Bu sonucun bir kısmı Bhojanapalli ve ark. 2021'in (arXiv:2103.14586, ICCV 2021; yeterli ön eğitimle ViT en az ResNet kadar gürbüz) ve Mahmood'un bulgularına indirgenir. Panelde ImageNet'te çekişmeli ön eğitilmiş XCiT'lerin bulunması da IN hücrelerine ortak ön eğitimden gelen bir benzerlik yanlılığı ekler.

**Saldırı 2 (müdahale eşit değil).** DeiT-Tiny ağır büyütme ve 300 epokla eğitilmiştir. torchvision ResNet-18 ise 90 epoklu basit bir tarifle eğitilmiştir. "IN başlatma" iki kolda farklı bir müdahaledir. Üstelik başlatma temiz doğruluğu ve gürbüzlüğü de değiştirir. P3'ün yasasına göre bu, hedef kırılganlığı (w) üzerinden de etki eder. Etkileşim, ViT'nin veriye aç olduğu bilgisine (Dosovitskiy ve ark., arXiv:2010.11929, bu oturumda doğrulanmadı) indirgenebilir.

**Saldırı 3 (çıkarım ve atıf).** Hücre başına n=2 var. Bütçe bekçisi tetiklenirse R224-IN hücresi n=1'e düşer ve θ_arch|IN için TOST anlamsızlaşır. AT tavanı 60 epok, ResNet ise C1'de 51-57. epokta seçiliyor (FÖY:1386-1388), yani 3 epokluk pay var ve AdamW altında seçim epoku bilinmiyor. "Dikkat değil" cümlesi yama gövdesini ayırmıyor (P2'nin V_CS kolu bunu yapar). ViT'ye özgü transfer saldırıları da yok. Naseer ve ark. 2022 (arXiv:2106.04169), geleneksel saldırıların ViT'nin kaynak gücünü düşük gösterdiğini bildirir. Blok 3'teki MI-PGD ve PGD-50 bu itirazı karşılamaz. Gradyan maskeleme işareti yok: ViT'de PGD ile AA arası fark 32,69'dan 29,14'e, ResNet'te 44,11'den 37,93'e (FÖY:17). Bu yüzden bu bir eksik değil.

**Zorunlu düzeltmeler**
- Birincil nicelik r ve τ, ayrı ayrı Holm ile sınanmalı.
- ResNet-18 için RSB tarifli timm ağırlığı (`resnet18.a1_in1k`, arXiv:2110.00476, doğrulanmadı) kullanılmalı ve iki IN hücresinin ImageNet top-1 değeri raporlanmalı.
- Panel IN ön eğitimsiz CNN'lerle sınırlanmalı. XCiT'ler ikincil tabaka olarak kalmalı.
- Bekçi tetiklenirse R224-IN değil Blok 2 kesilmeli; her hücrede n≥2 zorunlu.
- AT tavanı 80 epok olmalı.
- Blok 3'e TGR ya da PNA eklenmeli (zaten `c1_c2_tgr.py`'de var).
- Başlıkta "attention" yerine "patch-ViT" yazılmalı.
- R224-scr ile C1 ResNet arasında bir köprü karşıtlığı kurulmalı. Yoksa 2x2'nin sonucu makaledeki çifte bağlanmaz.

## P2, dış geçerlilik (duzeltilebilir, 5/10)

**Saldırı 1 (iddia ile ölçüt uyumsuz).** Manşet üç parçalı bir birleşik önerme. Çürütme ise yalnız φ ve ψ'nin ikisi birden 0,25'in altına düşerse işliyor. 0,25 ile 0,6 arası gri bölgede ve tek kolun tuttuğu durumda manşet ayakta kalıyor. Bu ölçüt çürütmeyi neredeyse imkânsız kılıyor.

**Saldırı 2 (müdahaleler simetrik değil).** ViT'ye ImageNet-21k veriliyor, ResNet'ten veri alınıyor ve ResNet-IN kolu yok. "Veri rejimi" ile "ViT'nin veri açlığı" ayrılamaz. Verisi %20'ye kısılmış ResNet'in zayıf model olması beklenen bir sonuçtur: Schmidt ve ark. 2018 (arXiv:1804.11285, doğrulanmadı) çekişmeli eğitimin daha çok veri istediğini gösterir. ψ böylece doğruluk karıştırıcısını ölçer. V_IN'e C1 ViT tarifi (lr 1e-3, 200 epok temiz) uygulanırsa 21k özellikleri silinebilir. Manipülasyon denetimi bunu yakalar ama önlemez.

**Saldırı 3 (B3 çıkarım taşımıyor).** ImageNet çiftleri tek kontrol noktasından oluşuyor. Singh S ve S-CvSt aynı tarifi paylaştığı için bağımsız değil. ConvNeXt dönüştürücü tarifine göre "modernleştirilmiş" bir CNN'dir. Bai çiftinde ε=4/255 ve PGD-1 var. Lisans ve kontrol noktası bağlantıları doğrulanmamış, süre de ölçülmemiş. "Aile düzeyinde açık yok" önermesi n=1 noktalarda TOST'la kurulamaz.

**Değerli kısım.** Oran ölçeğindeki panel öngörüsü 1,60'a karşı gözlenen 4,81; logitte 0,236'ya karşı 0,337 (`_P2_panel_logit.json`). Makalenin 3x3 oran ayrıştırmasının referansa bağlı olduğunu gösteren bu bulgu korunmalı. B1 ucuz ve gerekli.

**Zorunlu düzeltmeler**
- F0 uygulanmalı.
- Çürütme her kol için ayrı yazılmalı. Tutmayan kolun manşet parçası düşmeli.
- ResNet-IN kolu eklenmeli ya da "veri rejimi" sözü kaldırılmalı.
- R_20 doğruluk eşleşmeli yorumlanmalı ya da çıkarılmalı.
- B3 ya manşetten çıkarılmalı ya da yalnız betimsel tutulmalı.
- V_IN için kısa ince ayar tarifi (P1'deki gibi) kullanılmalı.

## P3, kuram ve ölçüm (duzeltilebilir, manşet olarak ölüme yakın; 5,5/10)

**Saldırı 1 (yasa kendi sınırında bozuluyor).** Önerilen P3 sınaması ±0,10 log birimlik bir eşdeğerlik sınırı istiyor. r_XCiT −0,121 ve altı eşin altısında aynı işarette. r_V +0,084; ViT ile XCiT arasındaki çiftte 0,213. Makalenin çifti için artık 0,119 ve yasa asimetrinin yalnız %54'ünü açıklıyor. "Yönü gürbüzlük, miktarı mimari belirler" cümlesi, makalenin konusu olan çiftte ve iki dikkat modelinde ters işaretli bir yönlü terimle çelişiyor. Bu terim ön eğitim farkıyla uyumlu: XCiT'in IN ön eğitimi P1 önerisinde arXiv:2209.07399'dan doğrulandı, bu raporda bağımsız doğrulanmadı.

**Saldırı 2 (sözde yineleme ve kapsamın sonradan seçilmesi).** 21 çift yalnız 7 potansiyel taşıyor (6 sd, korelasyon 0,978). Havuz R²'si merkezsiz hesaplanıyor, yörüngelerinki merkezli (`_p3_carpimsal_yasa_masa.py:58-59` ile `:119`). Yasa yörüngelerde (λ 1,46/2,07) ve standart eğitimde (−4,49, FÖY:1403) tutmuyor. "Yakınsamış AT" kapsamı veriye bakıldıktan sonra çizilmiş.

**Saldırı 3 (bilinen sonuca indirgenme, gevşek çürütme).** Sonuç Demontis ve ark. 2019'un (arXiv:1809.02861) hedef kırılganlığı ve simetrik gradyan hizası çerçevesine "kaynak terimi sıfır" varsayımı eklenmiş halidir. T4 işaret dönüşü sınaması ayırt edici değil: az gürbüz hedefin daha çok transfer alacağını her açıklama öngörür. "%95 aralık [0,77; 1,30]'un tümüyle dışında" ölçütü, az sayıda yeni çiftle neredeyse hiç tetiklenmez ve kararsız sonucu destek sayar.

**Değerli kısım.** Önerme 1(c) bugünkü makalenin en ağır itirazıdır. Önerme 3 (h ölçeğinde ham ile tc arasında yalnız hedef potansiyeli kayar) özdeşliğe ders kitabı aritmetiğinin ötesinde bir iş verir.

**Zorunlu düzeltmeler**
- Manşet "yasa" olmaktan çıkıp ayrıştırmaya dönmeli: T = w·τ·yönlü terim.
- Yönlü terim birincil nicelik olmalı. Çürütme eşdeğerlik biçiminde yazılmalı (aralık bölgenin içinde değilse destek yok).
- Potansiyel düzeyinde model bırakmalı çıkarım yapılmalı; R² tanımı her yerde aynı olmalı.
- T4 ayırt edici sınama olarak sunulmamalı.

## Hüküm ve önerilen birleşim

| Öneri | Hüküm | Puan |
|---|---|---|
| P1 | duzeltilebilir | 6,5 |
| P2 | duzeltilebilir | 5 |
| P3 | duzeltilebilir | 5,5 |

En sağlam birleşim şu: **P1 Blok 4 (2x2, RSB ResNet ile) + P1 Blok 3 ve 5 + P2 B1 + P3 Önerme 1 ve 3 ölçüm katmanı**. Buna eğitimsiz iki ekleme yapılmalı. Birincisi, C1'deki üç ViT tohumunun ve üç ResNet tohumunun kendi aralarında transfer matrisi; bu, tür içi τ'yu ölçer ve "ViT doğası gereği zayıf kaynak mı" sorusunu eğitimsiz yanıtlar. İkincisi, B1 bloğunun panelinde r ile τ'nun ayrı ayrı hesaplanması.

Önceden kaydedilecek manşet adayı şudur: *CNN ile ViT arasındaki çekişmeli transfer, hedef kırılganlığı, simetrik aile benzemezliği ve küçük bir yönlü kaynak terimine ayrışır; yönlü terimin işaretini mimari değil başlatma belirler.* Öngörüler: V-scr için r>0, V-IN için r≤0 (XCiT'te bugün −0,121), τ(V-IN, CNN) > τ(V-scr, CNN). Çürütme ölçütleri: r(V-IN) ≥ r(V-scr) çıkması ya da R224-IN'de r'nin V-IN kadar kayması (bu durumda ön eğitim mimariden bağımsız etki eder).

Bütçe kabaca 29,1 + 1,5 + 3,5 + 2 ≈ 36 GPU-saat ve 6 eğitim. P1 Blok 2, P2 B2/B3 ve P3 Blok 3 dışarıda kalır.

**Kabul için tek koşul:** F0 düzeltmesi. "Kaynak gücü" yerine w ile normalize edilmiş yönlü terim ve simetrik τ ayrı ayrı ölçülmezse hangi müdahale yapılırsa yapılsın, hakem sonucu "benzerlik" diye okuyup çürütür.

## Hakemin soracağı sorular
1. "ViT zayıf kaynak mı, yoksa CNN'lere mi benzemiyor?" Yanıtı log τ tablosu ve r verir.
2. "ImageNet başlatması yalnız daha iyi bir model mi üretiyor?" Yanıtı R224-IN hücresi ile w ortak değişkeni verir.
3. "Transfer saldırısı ViT için zayıf mı?" Yanıtı TGR, MI ve topluluk saldırısı ile PGD ve AA farkının raporlanmasıdır.

Kaynaklar: [arXiv 2103.14586](https://arxiv.org/abs/2103.14586v1), [arXiv 2103.15670](https://arxiv.org/abs/2103.15670v3), [Mahmood ICCV 2021](https://openaccess.thecvf.com/content/ICCV2021/html/Mahmood_On_the_Robustness_of_Vision_Transformers_to_Adversarial_Examples_ICCV_2021_paper.html). Öteki kimlikler öneri dosyalarından alındı ya da "doğrulanmadı" diye işaretlendi.

HÜKÜMLER: [{"proposal":"P1_mudahale","verdict":"duzeltilebilir","score":6.5,"key_attacks":["Yapı geçerliliği: CNN paneline karşı ölçülen kaynak gücü çoğunlukla simetrik benzemezliktir. Havuzda ViT'nin log τ açığı kaynak tarafında −0,435, hedef tarafında −0,338, yani yaklaşık %78'i simetrik. 'IN başlatmalı ViT güçlü kaynak' sonucu 'CNN'lere daha çok benzer' sonucuna, dolayısıyla Mahmood 2021 ve Bhojanapalli 2021'e indirgenebilir. Paneldeki IN ön eğitimli XCiT'ler ortak ön eğitim yanlılığı ekler.","Başlatma müdahalesi iki mimaride eşit değil: DeiT-Tiny 300 epok ve ağır büyütme, torchvision ResNet-18 90 epok ve basit tarif. Başlatma, temiz aşama uzunluğu ve doğruluk/gürbüzlük birlikte değişiyor; w üzerinden hedef kırılganlığını da kaydırır.","Çıkarım zayıf: hücre başına n=2 var ve bekçi tetiklenirse R224-IN n=1'e düşer, TOST anlamsızlaşır. 60 epok tavanı ResNet'in 51-57. epok seçimine çok yakın. 'Dikkat' yama gövdesinden ayrılmıyor. ViT'ye özgü transfer saldırıları (Naseer 2022) yok."],"required_fixes":["Birincil nicelik w ile normalize edilmiş yönlü artık r ve simetrik τ olmalı, ayrı ayrı Holm ile sınanmalı; S ile T birlikte raporlanmalı","ResNet-18 için RSB tarifli timm resnet18.a1_in1k kullanılmalı, iki IN hücresinin ImageNet top-1 değeri raporlanmalı","Panel IN ön eğitimsiz CNN'lerle sınırlanmalı, XCiT'ler ikincil tabaka olarak kalmalı","Bekçi tetiklenirse R224-IN değil Blok 2 kesilmeli; her hücrede n≥2 zorunlu; AT tavanı 80 epok olmalı","Blok 3'e TGR ya da PNA eklenmeli; başlıkta 'attention' yerine 'patch-ViT' yazılmalı; R224-scr ile C1 ResNet arasında köprü karşıtlığı kurulmalı"]},{"proposal":"P2_dis_gecerlilik","verdict":"duzeltilebilir","score":5,"key_attacks":["Birleşik üç parçalı manşet, yalnız φ ve ψ'nin ikisi birden ≤0,25 olunca çürüyor. 0,25-0,6 gri bölgesi ve tek kolun tuttuğu durum manşeti ayakta bırakıyor; çürütme pratikte imkânsız.","Müdahaleler simetrik değil: ViT'ye IN-21k veriliyor, ResNet'ten veri alınıyor, ResNet-IN kolu yok. 'Veri rejimi' ile ViT'nin veri açlığı ayrılamaz. R_20 doğruluk karıştırıcısını ölçer. C1 ViT tarifi (lr 1e-3, 200 epok) 21k özelliklerini silebilir.","B3 çıkarım taşımıyor: tek kontrol noktaları, bağımsız olmayan Singh çiftleri, ConvNeXt'in temsil sorunu, Bai'de ε=4/255 ve PGD-1, lisans ve süre doğrulanmamış. n=1 noktalarda TOST ile 'aile düzeyinde açık yok' kurulamaz. F0 sorunu burada da geçerli."],"required_fixes":["S ile T birlikte ölçülmeli; birincil nicelik r ve τ olmalı","Çürütme her kol için ayrı yazılmalı, tutmayan kolun manşet parçası düşmeli","ResNet-IN kolu eklenmeli ya da 'veri rejimi' sözü kaldırılmalı; R_20 çıkarılmalı ya da doğruluk eşleşmeli yorumlanmalı","B3 manşetten çıkarılmalı, yalnız betimsel kalmalı","V_IN için kısa ince ayar tarifi kullanılmalı; B1 ve oran/logit ölçek bulgusu korunmalı"]},{"proposal":"P3_kuram_olcum","verdict":"duzeltilebilir","score":5.5,"key_attacks":["Yasa bugünkü veride kendi ±0,10 sınırında bozuluyor: r_XCiT −0,121 (6/6 aynı işaret), r_V +0,084, makalenin çiftinde artık 0,119. Yasa 4,81 puanlık asimetrinin yalnız 2,60'ını açıklıyor. Ters işaretli yönlü terim ön eğitimle uyumlu.","Sözde yineleme: 21 çift 7 potansiyele dayanıyor (6 sd, r=0,978). Havuzda merkezsiz, yörüngelerde merkezli R² kullanılıyor. Yörüngelerde λ 1,46/2,07, standart eğitimde −4,49; 'yakınsamış AT' kapsamı sonradan seçilmiş.","Demontis 2019'a 'kaynak terimi sıfır' varsayımı eklenmiş hale indirgeniyor. T4 işaret dönüşü sınaması ayırt edici değil. '%95 aralık [0,77; 1,30] dışında' ölçütü gevşek, kararsız sonucu destek sayıyor."],"required_fixes":["Manşet yasadan ayrıştırmaya dönmeli (T = w·τ·yönlü terim); yönlü terim birincil nicelik olmalı","Çürütme eşdeğerlik biçiminde yazılmalı: aralık bölgenin içinde değilse destek yok","Potansiyel düzeyinde model bırakmalı çıkarım yapılmalı, R² tanımı birleştirilmeli","T4 ayırt edici sınama olarak sunulmamalı; Önerme 1(c) ve Önerme 3 ölçüm katmanı olarak korunmalı"]}]
