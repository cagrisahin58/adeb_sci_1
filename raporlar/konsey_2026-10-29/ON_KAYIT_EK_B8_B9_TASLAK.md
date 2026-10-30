# Ön kayıt eki taslağı: B8 (ImageNet paneli), B9 (CIFAR-100 paneli), B10 (gradyan hizalanması)

Bu dosya 30.10.2026 tarihli bir TASLAKTIR. Dosya `ON_KAYIT_2026-10-29.md` (dondurulmuş, commit e32f2ce) dosyasına eklenen ayrı bir ön kayıttır ve onu değiştirmez. Dondurulmuş ön kaydın tanımları, eşdeğerlik sınırı δ, karar ilkesi ve çözümleme betiği burada aynen geçerlidir; burada yalnız yeni bloklara özgü olanlar yazılır. Tasarım gerekçesi `raporlar/konsey_2026-10-29/06_ek_deney_tasarim.md` içindedir. Bu ek, B2, B3, B4, B5, B6, B8, B9 ve B10'un hiçbirinin sonucu görülmeden dondurulmalıdır; dondurma satırı ve özetler dosya sonundaki Dondurma ekine yazılır.

## 1. Kayıt öncesinde görülmüş veriler

Dondurulmuş ön kaydın §1'inde listelenen bütün veriler burada da görülmüş sayılır. B9 için önemli olanlar C1 CIFAR-100 çiftlerinin Pang2022Robustness_WRN28_10 ile kurulmuş 3x3 matrisleri ve bunlardan türetilen değerlerdir: çift düzeyinde r_RV ortalaması 0,154 (koşum SD 0,041), potansiyel payı 0,283, log τ̄ koşum SD'si 0,023 (`results/q1/konsey_masa/konsey_masa_cozumlemeleri.json`, `4_potansiyel_payi.ozet`; `results/q1/konsey_sentez_r_tau_masa.json`, `kumeler.c100_c1_secilen`). C1 CIFAR-100 modellerinin AutoAttack parçaları da görülmüştür (`results/q1/cifar100/pair*/aa_chunk_*`). B9 panelinin diğer altı üyesinin ve iki ikincil üyesinin CIFAR-100 transfer verisi görülmemiştir. Mahmood ve ark. 2021'in standart eğitimli dış matrisi (MASA `3_mahmood`) görülmüştür; orada CIFAR-10'da ViT-ViT log geometrik ortalaması 4,278, CNN-ViT 2,691'dir ve bu B8'deki K-c yönü için önceki bağlamdır.

B8 için hiçbir ImageNet modeli koşulmamış, hiçbir ImageNet görüntüsü indirilmemiştir. Görülen yalnız düzenek bilgisidir: RobustBench model sözlüğü ve ön işleme tanımları, mimarilerin rastgele ağırlıklı FLOP ve parametre sayıları (`raporlar/konsey_2026-10-29/_ek_flop_olcumu.json`), arşivlerin HEAD boyutları (`_ek_indirme_boyutlari.txt`) ve süre kestirimi (`_ek_sure_kestirimi.json`). Literatürden aktarılmış ImageNet temiz ve AutoAttack doğrulukları (Singh README üzerinden `01_oneri_P2_dis_gecerlilik.md` satır 61) görülmüştür; bunlar transfer verisi değildir.

B10 için modeller arası aynı görüntü gradyan kosinüsü hiçbir veri kümesinde hesaplanmamıştır. Görülen tek gradyan hizalanması tek modelin farklı görüntüleri arasındaki mutlak kosinüstür (`results/C1_REFERANS_FOYU.md` M8.10: ResNet-18 AT 0,0377/0,0370/0,0388, ViT-Tiny AT 0,0557/0,0564/0,0565). B10'un τ̄ tarafı B2, B4, B8 ve B9 matrislerinden gelecektir ve bunların hiçbiri bu ek yazılırken görülmemiştir; B2 koşmaktadır ve çıktı klasörünün yalnız dosya adları listelenmiştir.

Dondurma anında bu liste yeniden denetlenir. B2 ya da başka bir bloğun sonucu dondurmadan önce açılmışsa buraya tarihiyle yazılır ve hangi öngörüyü etkileyebileceği belirtilir.

## 2. Ortak tanımlar

T_ij, w_j, r_ij, log τ̄_ij, σ_m, ρ_m, ω_m, S_m, logit ve oran ölçekleri, bölünmüş yarı birincil kestiricisi, panel üyesinin kendi değerinde kendisinin panelden çıkarılması ve "yüklenemeyen üye" tanımı dondurulmuş §2 ile aynıdır. δ = 0,10, duyarlılık δ = 0,06, α = 0,05 ve karar ilkesi (destek Holm sonrası p ile, çürütme ve eşdeğerlik ham aralıkla; çürütme ve eşdeğerlik koşulu önce denetlenir; hesaplanamayan sınama p = 1 ile ailede kalır; öngörülen büyüklük karar ölçütü değildir, ayrı satırda raporlanır) dondurulmuş §5 ile aynıdır.

Çözümleme dondurulmuş `experiments/q1_konsey_ayrisim.py` (SHA-256 `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`) ile `--mod b2` kipinde, bu ek için yazılan ayrı hücre tablolarıyla yapılır. Betiğin hücre etiketleri ("C1-R32", "V-scr") ek tablolarda aşağıda tanımlanan rolleri taşır. Ek çözümlemeler `experiments/q1_ek_ayrisim.py` ile yapılır; bu betik dondurulmuş betiği değiştirmeden içe aktarır ve onun özetini çalışma anında denetler.

## 3. B8: ImageNet ölçeğinde panel

### 3.1 Veri ve saldırı

Görüntüler Imagenette2-320 ve Imagewoof2-320 arşivlerinde adı `ILSVRC2012_val_` ile başlayan bütün dosyalardır (ImageNet-1k doğrulama kümesinin parçası); etiket klasör wnid'inin ImageNet indeksidir, wnid eğitim dosyası önekleriyle denetlenir ve uyuşmazlıkta önek esas alınır. Görüntü listesi, sırası ve dosya özetleri `data/imagenet_heldout/manifest.json` ile sabitlenir; manifestin SHA-256'sı B8 koşusundan önce sapma kaydına yazılır. Ön işleme bütün modellerde `Resize(256, bicubic, antialias)`, `CenterCrop(224)`, [0, 1] değer aralığıdır; normalizasyon her modelin içindedir. Değerlendirme modellerin 1000 sınıflı çıktısıyla yapılır, logit kısıtı yoktur. Saldırı PGD-10 L∞, ε = 4/255, α = 1/255, rastgele başlangıç, tohum 42, kaynak başına tohumlu önbellekle (`--cache-adv`).

### 3.2 Modeller ve roller

Birincil panel P8 (ImageNet L∞ klasik CNN'ler, altı üye): Salman2020Do_R18, Salman2020Do_R50, Salman2020Do_50_2, Engstrom2019Robustness, Chen2024Data_WRN_50_2, Peng2023Robust. Yedek: Wong2020Fast (yalnız bir P8 üyesi elenirse, aynı denetimle). En az beş üye gerekir (`--panel-en-az` varsayılanı).

"C1-R32" etiketi aynı tarifli modern CNN'ler: Singh2023Revisiting_ConvNeXt-T-ConvStem (çift 1), Singh2023Revisiting_ConvNeXt-B-ConvStem (çift 2), Liu2023Comprehensive_ConvNeXt-B (çift 3). "V-scr" etiketi dönüştürücüler: Singh2023Revisiting_ViT-S-ConvStem (çift 1), Singh2023Revisiting_ViT-B-ConvStem (çift 2), Liu2023Comprehensive_Swin-B (çift 3), Mo2022When_ViT-B (çiftsiz). `b2_tohum_ciftleri` bu üç çifttir. İkincil panel: Debenedetti2022Light_XCiT-S12 (ImageNet). Takma adlar `IN_` önekiyle `ek_hucre_tablosu_b8.json` içinde sabitlenir. Çıkarım birimi aynı grup ve aynı tarifle eğitilmiş CNN-dönüştürücü çiftidir; kontrol noktaları tek eğitimdir ve çıkarım bu kontrol noktalarına koşulludur. Liu çiftinin tarif ortaklığı dondurmadan önce makaleden denetlenir ve sonucu Dondurma ekine yazılır; ortak değilse çift "aynı grup" etiketiyle kalır.

### 3.3 Manipülasyon denetimi ve dışlama

Transfer matrisinden önce, yalnız temiz tahminlerle: her model için manifest görüntülerinde 1000 sınıflı temiz doğruluk ortak hatla ve RobustBench'teki kendi ön işlemesiyle ölçülür. Model, kendi hatla doğruluğu en az %40 ve iki hat arasındaki fark en çok 3 puansa matrise girer; değilse çıkar ve bu kayda geçer. Eşik dondurmadan önce RobustBench'te yayımlanan temiz doğruluklarla karşılaştırılır ve iyi yüklenmiş bir adayı eleyecekse T görülmeden ve gerekçesiyle düşürülür. ImageNet-21k ya da 22k ön eğitimi kullandığı makalesinden anlaşılan modeller tabloda işaretlenir; birincil çözümlemede kalırlar, dışlandıkları çözümleme duyarlılıktır. Bunun dışında hiçbir model sonuca göre dışlanmaz.

### 3.4 Öngörüler, sınamalar ve çürütme ölçütleri (aile F_B8, dört sınama, Holm α = 0,05)

Birincil çözümleme önce `python experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini results/q1/konsey_b8_imagenet/matris --hucre-tablosu raporlar/konsey_2026-10-29/ek_hucre_tablosu_b8.json --cikti results/q1/konsey_b8_imagenet/b8_dondurulmus_b2.json` çağrısıyla, ardından `python experiments/q1_ek_ayrisim.py --mod b8 ...` çağrısıyla yapılır. F_B8'in Holm'u K-a, K-b, K-c'nin dondurulmuş çıktıdaki ham p'leri (`F_B2.p_ham`) ile H8-σ'nın ham p'si üzerinden dört sınamalı yapılır; dondurulmuş çıktıdaki üç sınamalı Holm kararları B8'de yalnız betimseldir.

H8-σ, aynı tarifte dönüştürücünün klasik CNN paneline benzerliği. Δσ_k = σ(dönüştürücü_k) − σ(CNN_k), k = 1, 2, 3, σ bölünmüş yarı log ölçekte P8 üzerinden. Öngörü: ortalama Δσ ≤ −0,20 ve üç çiftte de negatif. Sınama: tek yönlü t, H0: ort Δσ ≥ 0 (df 2). Kurallar sırayla: (i) ham %90 aralık (−0,10; 0,10) içindeyse çürütüldü (eşdeğer; ölçekte benzemezlik yok); (ii) değilse Holm sonrası p < 0,05 ise destek; (iii) kestirim pozitif ve ham %95 aralık sıfırı dışlıyorsa çürütüldü (ters yön); (iv) kalan sonuç kararsızdır. Üç çiftte işaret tutarlılığı ve öngörülen büyüklüğün tutup tutmadığı ayrı satırda raporlanır.

K-a(B8), kaynak açığının simetrik oranı. Dondurulmuş K-a tanımı çift k için uygulanır: D_k = S(CNN_k) − S(dönüştürücü_k), q_k = [σ(CNN_k) − σ(dönüştürücü_k)]/D_k. Öngörü: her çiftte q_k ≥ 0,75. Sınama, destek, çürütme ve payda kuralı (bir çiftte D_k ≤ 0,10 ise K-a kararsız, p = 1) dondurulmuş K-a ile aynıdır (df 2). Payda kuralı tetiklenirse D_k'lar aralıklarıyla raporlanır ve bu durum "aynı tarifli dönüştürücüler ImageNet'te belirgin biçimde zayıf kaynak değildir" bulgusu olarak okunabilir; bu okuma için D_k'ların görüntü bootstrap %90 aralıklarının üst sınırının 0,10'un altında kalması gerekir.

K-b(B8), dönüştürücülerin yönlü terimi. ρ'nun dört dönüştürücü üzerinden ortalaması. Öngörü: eşdeğer, |ρ| < 0,10. Sınama ve kurallar dondurulmuş K-b ile aynıdır (TOST ±0,10, df 3; destek Holm sonrası TOST p < 0,05; çürütme %95 aralık sıfırı dışlar ve |kestirim| > 0,10, iki yönde).

K-c(B8), dönüştürücü ailesi içi benzerlik. Δ_w = ort log τ̄(dönüştürücü, dönüştürücü') − ort σ(dönüştürücü), altı dönüştürücü çifti üzerinden; dondurulmuş K-c'deki hiyerarşik bootstrap modeller tohum yerine geçerek uygulanır. Öngörü: Δ_w ≥ +0,30. Sınama ve kurallar dondurulmuş K-c ile aynıdır. Bu sınama B8'de tohum içi değil, farklı grupların dönüştürücüleri arası aile benzerliğini ölçer; metinde böyle adlandırılır.

### 3.5 Keşifsel çözümlemeler (çoklu düzeltme yok, aralıklarla)

S8-1 çift başına D_k ve Δσ_k için görüntü bootstrap aralıkları (B = 2000, görüntüler bütün hücrelerde ortak ağırlıkla). S8-2 r matrisinin Hodge ayrışımı (potansiyel payı G, 2/K beklentisi; dondurulmuş `hodge_r`). S8-3 logit ve oran ölçekleri, tam örneklem, δ = 0,06, panel üyesi ve grup bırakmalı jackknife (Salman üyeleri bir grup). S8-4 Imagenette ve Imagewoof alt kümeleri ayrı ayrı. S8-5 logitlerin 20 sınıfa kısıtlandığı ikinci matris (Tier 2; koşulursa raporlanır). S8-6 conv gövdeli ViT-B ile yama gövdeli Mo ViT-B arasında σ ve ρ farkı. S8-7 Salman2020Do_R18 ile Singh ViT-S-CvSt çiftinde r ve potansiyel payı (C1 çiftinin karşılığı). S8-8 dört koşullama protokolü. S8-9 21k/22k ön eğitimli modeller çıkarılarak H8-σ ve K-b.

## 4. B9: CIFAR-100 paneli

### 4.1 Veri, saldırı, modeller

CIFAR-100 test kümesi, n = 10000, tohum 42, PGD-10 L∞, ε = 8/255, α = 2/255, kaynak başına tohumlu önbellek; dondurulmuş §2 ile aynı. "C1-R32" etiketi C1 CIFAR-100 ResNet-18 AT tohumları 1001, 1002, 1003; "V-scr" etiketi C1 CIFAR-100 ViT-Tiny AT tohumları 2001, 2002, 2003 (`models/q1/cifar100/...`, seçim kuralı E1 protokolü). `b2_tohum_ciftleri` (1001, 2001), (1002, 2002), (1003, 2003). Birincil panel P9 (yedi üye, RobustBench CIFAR-100 L∞, ImageNet ön eğitimsiz): Rice2020Overfitting, Rade2021Helper_R18_ddpm, Addepalli2022Efficient_RN18, Sehwag2021Proxy, Pang2022Robustness_WRN28_10, Wang2023Better_WRN-28-10, Jia2022LAS-AT_34_10. Yedekler sırasıyla Chen2021LTD_WRN34_10 ve Cui2023Decoupled_WRN-28-10. İkincil panel: Debenedetti2022Light_XCiT-S12 ve Hendrycks2019Using (ikisi de ImageNet ön eğitimli). Takma adlar `C100_` önekiyle `ek_hucre_tablosu_b9.json` içinde sabitlenir. Hiçbir model sonuca göre dışlanmaz.

### 4.2 Öngörüler, sınamalar ve çürütme ölçütleri (aile F_B9, üç sınama, Holm α = 0,05)

Çözümleme `python experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini results/q1/konsey_b9_c100/matris --hucre-tablosu raporlar/konsey_2026-10-29/ek_hucre_tablosu_b9.json --cikti results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` çağrısıyla yapılır. Betiğin üç sınamalı Holm'u ve karar etiketleri B9'da bağlayıcıdır.

K-a(B9), K-b(B9) ve K-c(B9) dondurulmuş K-a, K-b ve K-c'nin birebir aynısıdır: öngörüler her tohumda q_s ≥ 0,75, |ρ(V)| < 0,10 (TOST) ve Δ_w ≥ +0,30; sınamalar, destek, çürütme ve payda kuralı değişmez. B9 bir yinelemedir; öngörüler bu yüzden CIFAR-10 öngörülerinden kopyalanmıştır. Görülmüş CIFAR-100 verisinde çift düzeyi r'nin 0,154 olması ve koşum SD'sinin 0,041 olması (§1), K-b'nin TOST desteğinin CIFAR-10'dakinden çok daha zor olduğunu gösterir: üç tohumda %90 aralığın beklenen yarı genişliği yaklaşık 2,920 × 0,041/√3 ≈ 0,069'dur. Bu bir öngörü değişikliği değil, önceden yazılmış bir kesinlik notudur.

### 4.3 Keşifsel çözümlemeler

S9-1 ikincil panelle (ImageNet ön eğitimli iki üye) K-a ve K-b değerleri. S9-2 r matrisinin Hodge ayrışımı ve potansiyel payı tablosu, CIFAR-10 ile yan yana. S9-3 logit ve oran ölçekleri, δ = 0,06, panel jackknife (dondurulmuş betiğin duyarlılık alanları).

## 5. B10: saldırıdan bağımsız simetrik benzerlik

### 5.1 Ölçü

c_ij = ort_x cos(∇_x L_i(x, y), ∇_x L_j(x, y)), L çapraz entropi, x temiz görüntü [0, 1] uzayında, y doğru etiket, gradyan model içi normalizasyonu da içerir, modeller eval kipinde ve fp32'dir. Görüntüler her veri kümesinde matrisin görüntüleridir. Birincil c_ij bütün görüntülerin ortalamasıdır; iki modelin de temiz doğru olduğu görüntülerle sınırlı c_ij duyarlılıktır. log τ̄_ij dondurulmuş tanımla bölünmüş yarı, log ölçekte hesaplanır. Veri kümeleri ve modeller: CIFAR-10'da B4'ün son matrisindeki modeller (B4 oluşmazsa B2'nin modelleri), CIFAR-100'de B9'un modelleri, ImageNet'te B8'in denetimden geçen modelleri. Kod `experiments/q1_ek_gradyan_kosinus.py` (hesap) ve `experiments/q1_ek_ayrisim.py --mod b10` (çözümleme).

### 5.2 Öngörü, sınama ve çürütme (aile F_B10, üç sınama, Holm α = 0,05)

H10-d, d ∈ {CIFAR-10, CIFAR-100, ImageNet}: matristeki bütün sırasız model çiftleri üzerinde c_ij ile log τ̄_ij arasındaki Spearman korelasyonu pozitiftir. Öngörü: her veri kümesinde Spearman ≥ 0,50. Sınama: Mantel permütasyon sınaması, model etiketleri c matrisinin satır ve sütunlarında ortak permüte edilir, 9999 permütasyon, tohum 20261030, p = (1 + #{istatistik_perm ≥ istatistik_gözlenen})/10000, tek yönlü. Kurallar sırayla: (i) Spearman nokta kestirimi ≤ 0,20 ve ham Mantel p ≥ 0,20 ise çürütüldü; (ii) değilse Holm sonrası p < 0,05 ise destek; (iii) kalan sonuç kararsızdır. Öngörülen büyüklüğün (≥ 0,50) tutup tutmadığı ayrı satırda verilir.

### 5.3 Keşifsel çözümlemeler

S10-1 model düzeyi γ_m = ort_{c∈P} c_mc ile σ_m arasındaki ilişki. S10-2 C1 çiftlerinde γ(ViT) − γ(ResNet), CIFAR-10 ve CIFAR-100'de tohum başına; beklenen yön negatiftir. S10-3 aynı aileden olma göstergesini denetleyen kısmi Mantel. S10-4 log(‖∇L_j‖/‖∇L_i‖) ile log(w_j/w_i) arasındaki Spearman (Adam ve ark., arXiv 1904.07980'in gradyan normu açıklaması). S10-5 c_ij ile |r_ij| arasındaki ilişki (beklenti: zayıf). S10-6 her-ikisi-doğru görüntü alt kümesi.

## 6. Sonuç haritası ve metne girişi

Ek bloklar dondurulmuş §6'daki O1-O5a bölgesini değiştirmez; bölge yalnız B2-B6'dan belirlenir. Ek bloklar ancak aşağıdaki önceden yazılmış cümleleri ekler ya da manşete önceden yazılmış nitelemeyi getirir.

| Koşul | Metne giren cümle |
|---|---|
| H8-σ destek ve K-b(B8) destek | ImageNet ölçeğinde, bağımsız gruplarca aynı tarifle eğitilmiş CNN-dönüştürücü çiftlerinde de dönüştürücüler klasik CNN paneline simetrik olarak daha az benzer ve yönlü kaynak terimleri küçüktür; manşet "CIFAR ve ImageNet ölçeğinde" diye genişletilebilir |
| H8-σ destek, K-a(B8) payda kuralıyla kararsız ve D_k aralıkları 0,10'un altında | ImageNet'te dönüştürücüler benzemez ama belirgin biçimde zayıf kaynak değildir; CIFAR'daki kaynak açığı ölçek ya da tarif koşuluna bağlanır |
| H8-σ çürütüldü (eşdeğer ya da ters yön) | Simetrik benzemezlik ImageNet ölçeğinde aynı tarifli çiftlerde görülmez; manşet CIFAR ölçeğiyle sınırlanır |
| K-b(B8) çürütüldü | ImageNet ölçeğinde dönüştürücülere ait bir yönlü kaynak terimi vardır; büyüklüğü aralığıyla verilir |
| F_B9'da K-a ve K-b destek | Ayrışım CIFAR-100'de üç tohumla yinelenir |
| K-b(B9) çürütüldü | Yönlü terim veri kümesine bağlıdır (CIFAR-100'de büyük, SVHN'de ters işaretli); "küçük yönlü terim" cümlesi CIFAR-10 ile sınırlanır |
| F_B10'da en az iki veri kümesinde destek ve hiçbirinde çürütme yok | Simetrik terim, transferden ve saldırıdan bağımsız ölçülen girdi gradyanı hizalanmasıyla öngörülür |
| F_B10'da en az bir çürütme | τ̄ "simetrik transfer verimi" diye adlandırılır, gradyan hizalanması mekanizma olarak öne sürülmez |
| Diğer bütün durumlar | Kestirimler aralıklarıyla ek tabloda verilir, manşet değişmez |

Olumsuz sonuçlar metinden çıkarılmaz. "İlk kez" ve "bildiğimiz kadarıyla" ifadeleri kullanılmaz.

## 7. Bütçe ve sıra

B9 tavanı 1,0, B8 0,75, B10 0,25 GPU-saattir (Tier 1 toplamı 2,0); B8'in 20 sınıf kısıtlı matrisi 0,5 GPU-saattir (Tier 2). Bu bütçe dondurulmuş Dondurma eki (e)'deki 42,2 GPU-saatin dışındadır, B6 bittikten sonra ve GPU'da başka eğitim yokken harcanır. İndirmeler ve B8'in ön işleme denetimi B3 sürerken CPU'da yapılabilir. Süre dayanağı `raporlar/konsey_2026-10-29/_ek_sure_kestirimi.json`'dur.

## 8. Sapmalar

Dondurmadan sonraki her değişiklik, çözümleme yapılmadan önce tarihiyle `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasının "Ek B8-B10" başlığı altına yazılır. Manifestin özeti, ön işleme denetiminin sonucu ve dışlanan ya da yedekle değiştirilen modeller T görülmeden bu dosyaya yazılır ve sapma sayılmaz, çünkü kuralları burada tanımlıdır. Dondurma ekindeki dosya özetlerinden biri değişirse yapılan çözümleme ön kayıtlı sayılmaz. Manifestte 400'den az görüntü çıkarsa yedek veri yolu (v1 arşivleri, sonra fable onayıyla ImageNetV2 matched-frequency) sapma olarak yazılır ve B8'in bütün kuralları yeni veride aynen uygulanır.

## Dondurma eki (dondurmada doldurulacak)

(a) Bağlı dosyaların SHA-256 özetleri: `experiments/q1_konsey_ayrisim.py` (beklenen `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`, değişmemiş olmalı), `raporlar/konsey_2026-10-29/ek_hucre_tablosu_b8.json`, `raporlar/konsey_2026-10-29/ek_hucre_tablosu_b9.json`, `experiments/q1_ek_ayrisim.py`, `experiments/q1_ek_gradyan_kosinus.py`, `experiments/c1_c3_transfer_matrix.py` (B8 eklerinden sonraki hâli).

(b) Bu ekin gövdesinin SHA-256 özeti (ilk satırdan `## Dondurma eki` başlığına kadar).

(c) Liu çiftinin tarif ortaklığı denetiminin sonucu ve kaynağı; B8 modellerinin ön eğitim verisi tablosu (ImageNet-1k, 21k ya da 22k); ön işleme denetimi eşiğinin RobustBench temiz doğruluklarıyla karşılaştırılması.

(d) Dondurma anındaki git HEAD ve bu dosyayı içeren commit; o ana kadar açılmış B2-B6 çıktısı varsa listesi (yoksa "yok").
