# Ek deney tasarımı: B8 (ImageNet ölçeği), B9 (CIFAR-100 paneli) ve B10 (saldırıdan bağımsız benzerlik) (30.10.2026)

Bu belge deney planlayıcı (opus alt ajan, deney-takibi rolü) tarafından hazırlanmıştır ve yalnız plandır. GPU işi başlatılmamış, veri ya da model indirilmemiştir. Yapılan ölçümler şunlardır: konteynerde CPU üzerinde rastgele ağırlıklı mimarilerin FLOP ve parametre sayımı (`raporlar/konsey_2026-10-29/_ek_flop_olcumu.py` → `_ek_flop_olcumu.json`), fastai arşivlerinin yalnız HTTP HEAD ile boyut sorgusu (`_ek_indirme_boyutlari.sh` → `_ek_indirme_boyutlari.txt`), RobustBench kurulu paketinin model sözlüğü ve ön işleme tablosunun okunması, arXiv API ile sekiz kimliğin doğrulanması ve süre kestiriminin betikle hesaplanması (`_ek_sure_kestirimi.py` → `_ek_sure_kestirimi.json`). B2'nin koşmakta olan çıktı klasörünün (`results/q1/konsey_b2_panel/`) içeriği açılmamıştır; yalnız dosya adları listelenmiştir. Ön kayıt eki taslağı ayrı dosyadadır: `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B9_TASLAK.md`.

En önemli üç nokta şunlardır. Birincisi, F1'in dayandığı "Imagenette doğrulama görüntüleri ImageNet doğrulama kümesinden gelir" varsayımı yanlıştır: fastai deposu 6 Aralık 2019'da Imagenette ve Imagewoof'un "70/30 train/valid split" ile yeniden bölündüğünü yazar (github.com/fastai/imagenette, 30.10.2026'da okundu). ImageNet doğrulama kümesinde sınıf başına 50 görüntü bulunduğundan on sınıfta en çok 500 görüntü ImageNet doğrulamasından gelebilir; geri kalanı ImageNet eğitim kümesindendir ve RobustBench modelleri bunları eğitimde görmüştür. B8 bu yüzden yalnız `ILSVRC2012_val_*` adını taşıyan dosyalarla, Imagenette ve Imagewoof birlikte en çok yaklaşık 1000 görüntüyle kurulmalıdır; logitler de 10 sınıfa kısıtlanmamalı, modellerin kendi 1000 sınıflı çıktısı kullanılmalıdır (kısıt yalnız duyarlılık). İkincisi, B8 ve B9'un birincil sınamaları dondurulmuş `experiments/q1_konsey_ayrisim.py --mod b2` ile, betiğe tek bayt dokunmadan, yalnız yeni hücre tablolarıyla yapılabilir; betik hücre ve panel üyeliğini tamamen tablodan okur. B8'de tohum olmadığı için çıkarım birimi aynı grup ve aynı tarifle eğitilmiş CNN-dönüştürücü çiftidir (Singh ConvNeXt-T/ViT-S, Singh ConvNeXt-B/ViT-B, Liu ConvNeXt-B/Swin-B). Üçüncüsü, önerilen tek ek fikir B10'dur: modellerin temiz görüntüdeki girdi gradyanlarının kosinüsü saldırıdan ve transferden bağımsız, tanım gereği simetrik bir benzerlik ölçüsüdür; bu ölçünün log τ̄'yu üç veri kümesinde öngörüp öngörmediği sınanırsa "τ̄ yalnız T'nin yeniden yazılmış hâlidir" dairesellik itirazı kapanır ve ayrışıma bir mekanizma bağlanır. B10 indirme istemez, toplam yaklaşık 5 GPU-dakikasıdır.

Toplam bütçe tavan olarak B8 için 0,75, B9 için 1,0, B10 için 0,25 GPU-saattir (Tier 1 toplamı 2,0); B8'in 20 sınıf kısıtı duyarlılığı 0,5 GPU-saat (Tier 2). Hesaba dayalı beklenen süre yaklaşık 1 GPU-saattir. İndirme yaklaşık 4,85 GB'tır (veri 670 MB, B8 modelleri 3,28 GB, B9 modelleri 0,90 GB; `_ek_sure_kestirimi.json`, `toplam_indirme_MB`); disk 56 GB boştur. Koşu sırası B6'dan sonradır; indirmeler B3 sürerken CPU ile yapılabilir.

## 1. Doğrulanan olgular

| Olgu | Değer | Kaynak |
|---|---|---|
| Imagenette ve Imagewoof v2 bölmesi | "They now have a 70/30 train/valid split" (6 Aralık 2019) | github.com/fastai/imagenette README, WebFetch 30.10.2026 |
| Eski sürümler | "The old versions (which have a much smaller validation set) are still available with the same URLs" | aynı README |
| Lisans (depo) | Apache-2.0; görüntülerin kendisi ImageNet kullanım koşullarına tabidir | aynı README; görüntü koşulu genel bilgidir, ayrıca denetlenmelidir |
| Arşiv boyutları (bayt) | imagenette2-320: 341 663 724; imagewoof2-320: 328 387 740; imagenette-320 (v1): 341 289 752; imagewoof-320 (v1): 328 003 750 | `_ek_indirme_boyutlari.txt` (HEAD, 30.10.2026) |
| Paraşüt sınıfının WordNet kimliği | n03888257 (fastai `lbl_dict`); n03888605 "parallel bars"dır | docs.fast.ai/tutorial.imagenette.html; timm `ImageNetInfo` (konteyner) |
| Imagenette sınıflarının ImageNet indeksleri | tench 0, English springer 217, cassette player 482, chain saw 491, church 497, French horn 566, garbage truck 569, gas pump 571, golf ball 574, parachute 701 | timm 1.0.27 `ImageNetInfo`, konteyner çıktısı |
| Dosya adları | eğitim dosyaları wnid önekini taşır (örnek `n03425413_7416.JPEG`) | docs.fast.ai tutorial; `ILSVRC2012_val_*` adlarının v2 arşivinde korunduğu indirmeden sonra sayılarak doğrulanacak (doğrulanmadı) |
| RobustBench ImageNet ön işleme tanımları | Res256Crop224 (bilinear 256, merkez 224), BicubicRes256Crop224, Crop288 (yalnız merkez 288), Res224 (224x224'e ezme) | `robustbench.data.PREPROCESSINGS`, konteyner |
| Normalizasyonun yeri | ResNet'lerde `normalize_model(..., mu, sigma)` model içinde; Singh `vit_s_cvst` sarmalayıcıda normalizasyon var, `convnext_t_cvst`, `convnext_b_cvst`, `vit_b_cvst` için `get_convstem_models` içinde normalizasyon yok; `Chen2024Data_WRN_50_2` girdisi `normalize_model` sarmalamıyor | `robustbench.model_zoo.architectures.convstem_models.get_convstem_models` kaynak metni; `raporlar/konsey_2026-10-29/_rb_imagenet_P2.json` |
| İndirme yolu | XCiT (ImageNet ve CIFAR-100) GitHub sürüm bağlantısından timm ile; diğer bütün adaylar Google Drive (gdown) kimliğiyle | konteynerde `model_dicts[...]['gdrive_id']`; `robustbench/model_zoo/architectures/xcit.py` |
| arXiv kimlikleri | 2007.08489 (Salman), 2302.14301 (Liu), 2308.16258 (Peng), 2001.03994 (Wong), 2010.09670 (RobustBench), 2209.07399 (Debenedetti), 2303.01870 (Singh), 2210.07540 (Mo) başlıklarıyla eşleşti | export.arxiv.org API, 30.10.2026 |
| ImageNetV2 boyutu | matched-frequency 1,26 GB (1 GB sınırının üstünde) | huggingface.co/datasets/vaishaal/ImageNetV2, 30.10.2026 |

Bu tablodan çıkan sonuç açıktır. fable metnindeki 3925 doğrulama görüntüsü sayısı doğruysa bunun en az 3425'i ImageNet eğitim kümesindendir. Bu görüntülerde ölçülen beyaz kutu ve transfer oranları eğitim görüntüsü üzerindedir ve gürbüz modellerde eğitim ile test arasındaki gürbüzlük açığı büyük olduğundan w'yi ve T'yi doğrudan değiştirir. Bu bir sızıntı riskidir, B8 tasarımının ilk düzeltmesidir.

## 2. B8: ImageNet ölçeğinde gürbüz model paneli (eğitim yok)

### 2.1 Soru ve ölçüt

B8, bağımsız gruplarca ImageNet'te L∞ ε = 4/255 ile eğitilmiş, mimarisi gerçekten çeşitli gürbüz modellerde iki şeyi sınar: dönüştürücülerin klasik CNN paneline göre daha düşük simetrik benzerlik (σ) taşıyıp taşımadığı ve kaynak gücü farklarının simetrik terimle mi yönlü terimle mi taşındığı. Hakemin "CIFAR-10 oyuncak kurulum" itirazına doğrudan yanıt budur. Çıkarımın birimi aynı grup ve aynı tarifle eğitilmiş CNN-dönüştürücü çiftidir; böylece tarif farkı çift içinde sabitlenir ve fark mimariye yüklenebilir. ImageNet kontrol noktaları tek eğitimdir, çıkarım bu kontrol noktalarına koşulludur ve böyle yazılır.

### 2.2 Veri hattı

Veri Imagenette2-320 ve Imagewoof2-320 arşivlerindeki, adı `ILSVRC2012_val_` ile başlayan bütün JPEG dosyalarıdır (eğitim ve doğrulama klasörlerinin ikisinden de; klasör yalnız etiket için kullanılır). Beklenen sayı her küme için en çok 500, toplam en çok yaklaşık 1000'dir; gerçek sayı indirmeden sonra manifest betiğiyle sayılır. Bu görüntüler ImageNet-1k doğrulama kümesinin parçasıdır ve ImageNet-1k ile eğitilmiş modellerin eğitiminde yer almaz. ImageNet-21k ya da 22k ön eğitimi kullanan bir model varsa bu güvence o model için zayıflar; böyle modeller manifestte işaretlenir ve dışlanarak duyarlılık yapılır (Bölüm 9).

Etiket, klasörün wnid'inden timm `ImageNetInfo` ile ImageNet indeksine çevrilir. Manifest betiği her klasörde wnid önekli eğitim dosyalarının önekinin klasör adıyla aynı olduğunu da denetler; paraşüt sınıfındaki n03888257 ile n03888605 karışıklığı (Bölüm 1) bu denetimle yakalanır. Uyuşmazlıkta dosya önekindeki wnid esas alınır ve durum manifestte yazılır.

Ortak ön işleme bütün modeller için tektir, çünkü transfer matrisinde bir kaynağın çekişmeli tensörü bütün hedeflere aynı biçimde verilmelidir: `Resize(256, bicubic, antialias=True)`, `CenterCrop(224)`, `ToTensor()`; değer aralığı [0, 1]'dir ve ImageNet normalizasyonu her modelin kendi içindedir (Bölüm 1, normalizasyon satırı). Bicubic seçimi, panelin çoğunun (Singh, Liu, Mo dışındaki dönüştürücüler, ConvNeXt'ler) BicubicRes256Crop224 beklemesindendir; Res256Crop224 bekleyen ResNet'ler için fark yalnız aradeğerleme türüdür. Görüntüler 320 piksel kısa kenara önceden küçültülmüş olduğundan özgün ImageNet hattıyla birebir aynı değildir; bu fark ön işleme denetimiyle ölçülür. Saldırı 224x224 [0, 1] uzayında yapılır.

Logitler birincil çözümlemede kısıtlanmaz: modellerin kendi 1000 sınıflı çıktısı ve doğru ImageNet etiketi kullanılır, "yanıltma" argmax'ın doğru indeksten ayrılmasıdır. Bunun üç gerekçesi vardır. Birincisi, 10 ya da 20 sınıfa kısıtlamak hem sınıflandırıcıyı hem saldırı amacını değiştirir; yanıltmak için örneğin dokuz uzak sınıftan birine geçmek gerektiğinden w ve T değişir ve bu değişimin modeller arasında eşit olacağına dair bir dayanak yoktur. Kısıt, w'yi şişirebilir de bastırabilir de; yönü Imagenette'in kolay ayrılan sınıflarında ve Imagewoof'un birbirine benzeyen köpek ırklarında farklı olabilir. İkincisi, 1000 sınıflı değerlendirme RobustBench'in yayımladığı temiz ve gürbüz doğruluklarla aynı tanımdadır ve hattın kaba bir sağlamasını verir. Üçüncüsü, böylece ImageNet'in sınıf uzayı değil yalnız görüntü örneklemi daraltılmış olur; tanımlar dondurulmuş ön kaydın §2'siyle aynı kalır. 20 sınıf kısıtı (Imagenette ve Imagewoof sınıflarının birleşimi) yalnız Tier 2 duyarlılık olarak koşulur.

### 2.3 Modeller

Takma adlar CIFAR-10 hücre tablosundaki aynı adlı modellerle çakışmasın diye `IN_` önekiyle başlar. GFLOP ve boyut `_ek_flop_olcumu.json` içindeki rastgele ağırlıklı mimarilerin ölçümüdür; boyut 4 bayt × parametre kestirimidir, gerçek dosya boyutu indirme kaydına yazılır (CIFAR-10 zoo dosyalarında gerçek boyut bu kestirimle yakın çıkmıştır, örneğin Engstrom2019Robustness 94 350 601 bayt, CIFAR ResNet-50 kestirimi 94,1 MB; `models/robustbench_zoo/cifar10/Linf/`).

| Takma ad | RobustBench adı | Mimari | B8 rolü (tablo hücresi) | Grup, kaynak | Model ön işlemesi | GFLOP | Boyut (MB, kestirim) |
|---|---|---|---|---|---|---|---|
| IN_Salman2020Do_R18 | Salman2020Do_R18 | ResNet-18 | birincil panel P8 | Salman ve ark., arXiv 2007.08489 | Res256Crop224 | 3,63 | 47 |
| IN_Salman2020Do_R50 | Salman2020Do_R50 | ResNet-50 | P8 | aynı | Res256Crop224 | 8,18 | 102 |
| IN_Salman2020Do_50_2 | Salman2020Do_50_2 | WRN-50-2 | P8 | aynı | Res256Crop224 | 22,80 | 276 |
| IN_Engstrom2019Robustness | Engstrom2019Robustness | ResNet-50 | P8 | MadryLab `robustness` kütüphanesi (yazılım atfı) | Res256Crop224 | 8,18 | 102 |
| IN_Chen2024Data_WRN_50_2 | Chen2024Data_WRN_50_2 | WRN-50-2 | P8 | Chen ve ark. 2024 (kimlik doğrulanmadı) | Res256Crop224 | 22,80 | 276 |
| IN_Peng2023Robust | Peng2023Robust | RaWRN-101-2 | P8 | Peng ve ark., arXiv 2308.16258 | Res256Crop224 | 51,01 | 416 |
| IN_Singh_ConvNeXt-T-CvSt | Singh2023Revisiting_ConvNeXt-T-ConvStem | ConvNeXt-T, conv gövde | "C1-R32" etiketi, çift 1 | Singh, Croce, Hein, arXiv 2303.01870 | BicubicRes256Crop224 | 9,18 | 115 |
| IN_Singh_ViT-S-CvSt | Singh2023Revisiting_ViT-S-ConvStem | ViT-S, conv gövde | "V-scr" etiketi, çift 1 | aynı | BicubicRes256Crop224 | 9,24 | 91 |
| IN_Singh_ConvNeXt-B-CvSt | Singh2023Revisiting_ConvNeXt-B-ConvStem | ConvNeXt-B, conv gövde | "C1-R32", çift 2 | aynı | BicubicRes256Crop224 | 31,76 | 355 |
| IN_Singh_ViT-B-CvSt | Singh2023Revisiting_ViT-B-ConvStem | ViT-B, conv gövde | "V-scr", çift 2 | aynı | BicubicRes256Crop224 | 34,39 | 349 |
| IN_Liu_ConvNeXt-B | Liu2023Comprehensive_ConvNeXt-B | ConvNeXt-B | "C1-R32", çift 3 | Liu ve ark., arXiv 2302.14301 | BicubicRes256Crop224 | 30,71 | 354 |
| IN_Liu_Swin-B | Liu2023Comprehensive_Swin-B | Swin-B | "V-scr", çift 3 | aynı | BicubicRes256Crop224 | 30,86 | 351 |
| IN_Mo_ViT-B | Mo2022When_ViT-B | ViT-B/16, yama gövdesi | "V-scr", çiftsiz | Mo ve ark., arXiv 2210.07540 | Res224 | 33,70 | 346 |
| IN_Debenedetti_XCiT-S12 | Debenedetti2022Light_XCiT-S12 | XCiT-S12 (karma) | ikincil panel | Debenedetti ve ark., arXiv 2209.07399 | timm yapılandırması | 9,59 | 105 |
| IN_Wong2020Fast (yedek) | Wong2020Fast | ResNet-50 | yalnız bir P8 üyesi elenirse | Wong ve ark., arXiv 2001.03994 | Crop288 | 8,18 | 102 |

Hücre etiketleri dondurulmuş betiğin kod yolunu kullanmak içindir: betik K-a çiftlerini `b2_tohum_ciftleri` alanından, R ve V hücrelerini "C1-R32" ve "V-scr" etiketlerinden okur. B8 tablosunda bu etiketler sırasıyla "aynı tarifli modern CNN" ve "dönüştürücü" anlamına gelir; bu eşleme tablonun `hucreler` açıklamasına ve ek ön kayda yazılır. Singh çiftlerinin aynı tarifle eğitildiği P2 önerisinde Singh README'sinden aktarılmıştır (`01_oneri_P2_dis_gecerlilik.md` satır 61: ViT-S-CvSt 72,5/48,1, ConvNeXt-T-CvSt 72,7/49,5; B-CvSt sürümleri 250 epok, 76,3/54,7 ve 75,9/56,1, temiz/AA); bu oturumda README'den yeniden okunmamıştır. Liu çiftinde tarif ortaklığı P2'de de doğrulanmamıştır; dondurmadan önce Liu ve ark.'nın eğitim ayrıntıları okunmalı, ortak değilse çift "aynı grup, tarif farklı olabilir" diye etiketlenir ve ön kayıtta öyle kalır. Mo ViT-B yama gövdeli saf ViT olduğu için K-b ve K-c'ye girer, eşi olmadığından K-a'ya girmez; "conv gövde ViT'yi CNN'e benzetiyor" itirazına karşı tek saf ViT tanığıdır. Panelin üç üyesinin aynı gruptan (Salman) gelmesi bilinçlidir, çünkü ResNet-18, ResNet-50 ve WRN-50-2 ölçek eksenini verir; grup bağımlılığı için grup bırakmalı jackknife duyarlılığı planlanmıştır.

### 2.4 Saldırı, örneklem, tohum

PGD-10 L∞, ε = 4/255, α = 1/255, rastgele başlangıç, tohum 42, kaynak başına tohum (`--cache-adv` ile). α/ε oranı CIFAR'daki 2/255 ile 8/255 oranıyla aynıdır (1/4) ve toplam adım yolu 2,5ε'dur. ε = 4/255, RobustBench ImageNet L∞ değerlendirmesinin standart yarıçapıdır. n manifestteki bütün görüntülerdir (beklenen yaklaşık 1000); sıra manifest sırasıdır ve bütün modellerde ortaktır. Birincil kestirici dondurulmuş ön kaydın §2'sindeki bölünmüş yarıdır.

### 2.5 Ön işleme denetimi (manipülasyon denetimi)

Transfer matrisinden önce ve yalnız temiz tahminlerle yapılır, sonucu T görülmeden kesinleşir. Her model için manifest görüntülerinde iki temiz doğruluk ölçülür: ortak hatla ve modelin RobustBench'teki kendi ön işlemesiyle (`robustbench.data.get_preprocessing`). Kural: kendi hatla 1000 sınıflı temiz doğruluk en az %40 ve iki hat arasındaki fark en çok 3 puan. Normalizasyonu eksik ya da yanlış yüklenmiş bir ImageNet modelinin temiz doğruluğunun bu eşiğin çok altına düşmesi beklenir; eşik bu yüzden yükleme hatasını yakalamaya yöneliktir. Adayların RobustBench'te yayımlanan temiz doğrulukları depoda kayıtlı değildir (`_rb_imagenet_P2.json` yalnız ad ve ön işleme taşır); eşiğin iyi yüklenmiş en zayıf adayı elemeyeceği dondurmadan önce RobustBench tablosundan okunarak denetlenmeli, gerekirse eşik T görülmeden düşürülmelidir. Kuralı geçmeyen model matristen çıkar; P8 üyesiyse yedek IN_Wong2020Fast aynı denetimden geçerek girer. Bu denetim CPU'da yapılabilir (14 model × 1000 görüntü, tahminen 20-30 dk), böylece B3 sürerken GPU'ya dokunmadan tamamlanır.

### 2.6 Çözümleme

Birincil sınamalar dondurulmuş betikle yapılır: `python experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini results/q1/konsey_b8_imagenet/matris --hucre-tablosu raporlar/konsey_2026-10-29/ek_hucre_tablosu_b8.json --cikti results/q1/konsey_b8_imagenet/b8_dondurulmus_b2.json`. Bu çağrı K-a (çift başına kaynak açığının simetrik oranı, payda kuralıyla), K-b (dönüştürücülerin ρ ortalaması için ±0,10 TOST, dört model, df 3) ve K-c (dönüştürücüler arası log τ̄ ile dönüştürücülerin panel σ'sı farkı, Δ_w) değerlerini ve logit, oran, tam örneklem, panel jackknife ve ikincil panel duyarlılıklarını üretir. B8'in kendi dördüncü sınaması H8-σ, aynı çıktının `model_tablosu` alanındaki σ değerlerinden yeni betikte hesaplanır: Δσ_k = σ(dönüştürücü_k) − σ(CNN_k), üç çift, tek yönlü t (df 2). B8 ailesinin kararı dört ham p üzerinden Holm ile verilir; dondurulmuş betiğin kendi üçlü Holm'u B8'de yalnız betimseldir. Ayrıntı ve karar kuralları ek ön kayıttadır.

Keşifsel B8 çözümlemeleri şunlardır: çift başına D_k ve Δσ_k için görüntü bootstrap aralıkları (B = 2000, görüntüler bütün hücrelerde ortak ağırlıkla), r matrisinin Hodge ayrışımı (potansiyel payı G ve 2/K beklentisi; dondurulmuş `hodge_r` işlevi içe aktarılarak), dört koşullama protokolü (`src/analysis/protokoller.py`), Imagenette ve Imagewoof alt kümeleri ayrı ayrı, 20 sınıf kısıtı (Tier 2), conv gövdeli ViT ile Mo'nun yama gövdeli ViT-B'si arasındaki σ farkı ve C1 ResNet-ViT çiftinin karşılığı olarak IN_Salman2020Do_R18 ile IN_Singh_ViT-S-CvSt çiftinde r ile potansiyel payı.

### 2.7 Önceden kesinlik planı (post-hoc güç değildir)

Görüntü kaynaklı belirsizlik yaklaşık şöyledir. n ≈ 1000 ve temiz doğruluk %75 varsayılırsa hedef-doğru payda yaklaşık 750, her yarıda 375'tir; T = 0,30 için tek hücrede log T'nin standart hatası √(0,7/(0,3 × 375)) ≈ 0,079'dur. σ altı panel üyesi üzerinden ortalandığından model başına görüntü kaynaklı standart hata kabaca 0,03-0,05 log birimi beklenir. Asıl sınır çift sayısıdır: üç çiftte df 2 ve t_0,95 = 2,920 olduğundan, çiftler arası Δσ SD'si 0,10 ise %90 aralığın yarı genişliği 2,920 × 0,10/√3 ≈ 0,17 olur. CIFAR'daki ViT açığının simetrik payı log ölçekte 0,392'dir (`results/q1/konsey_masa/konsey_ayrisim_masa.json`, `havuz_on_kayit_tanimlari.b2_nokta_tohum1.yari_log.simetrik_pay`); ImageNet'te etki bu düzeydeyse ve çiftler tutarlıysa saptanır, 0,1 düzeyindeyse B8 büyük olasılıkla kararsız kalır. Bu sınırlılık önceden yazılmıştır; B8 bir kestirim ve yön sınamasıdır, eşdeğerlik kanıtı üretmesi beklenmez.

### 2.8 Süre ve disk

Etkin hız iki kalibrasyondan türetilmiştir: 8x8 havuz matrisi 13,5 dk (`00_durum_dosyasi.md` satır 94, zaman damgalarından türetilmiş; havuzun sekiz modelinin ileri geçiş toplamı 41,56 GFLOP) yaklaşık 20,0 TFLOP/s, 224 girdili ResNet-18'in kaynak başına 1,15 dk'sı (`01_oneri_P3_kuram_olcum.md` satır 57) yaklaşık 15,8 TFLOP/s verir (`_ek_sure_kestirimi.json`, `kalibrasyon`). İş modeli n × ΣF × (30 + K + 1)'dir: on adımlı PGD'de ileri ve geri geçiş yaklaşık üç ileri geçiş sayılır, her kaynağın örnekleri K hedefte bir kez ileri geçer, bir de temiz geçiş vardır.

Görüntü başına ileri geçişte ImageNet ResNet-50, 224 girdili ResNet-18'in 2,25 katı, Singh ViT-S-CvSt 2,55 katı, WRN-50-2 6,29 katı, Swin-B 8,51 katı, ViT-B 9,29 katı, RaWRN-101-2 14,06 katıdır (`_ek_sure_kestirimi.json`, `oran_224_resnet18_e_gore`). Buna göre n = 1000'de kaynak başına saldırı süresi ResNet-50 için yaklaşık 1,15 × 0,1 × 2,25 ≈ 0,26 dk, ViT-B için yaklaşık 1,07 dk, RaWRN için yaklaşık 1,6 dk'dır. On dört modelin toplamı 306,0 GFLOP'tur ve B8 matrisi n = 1000 için 11,5-14,6 dk sürer (`B8_n1000`). Dönüştürücülerde ve büyük modellerde kalibrasyondaki CIFAR modellerinden farklı GPU verimi, veri yükleme ve model yükleme için iki kat pay konmuş, tavan 0,75 GPU-saat alınmıştır. Bellek: on dört modelin ağırlıkları yaklaşık 3,3 GB'tır; ViT-B ve Swin-B'nin 50'lik grupta geri geçişi için `--batch-size 25` önerilir. 20 sınıf kısıtı ikinci bir tam matristir (aynı süre, Tier 2, tavan 0,5 sa).

Disk gereksinimi şöyledir: veri arşivleri 670 MB, açılmış hâli yaklaşık aynı, B8 modelleri yaklaşık 3,28 GB (`B8_indirme_fp32_MB`), çekişmeli örnek önbelleği 14 kaynak × 1000 × 3 × 224 × 224 × 4 bayt ≈ 8,4 GB'tır. Önbellek bu blokta en büyük disk kalemidir; float16 saklama ya da önbelleği matris bittikten sonra silme seçeneği runbook'a yazılmalıdır (önbellek yalnız devam ve B10 dışı yeniden kullanım içindir). Toplam en kötü durum yaklaşık 13 GB'tır ve 56 GB boş alanın içinde kalır; B3 kontrol noktaları da aynı diske yazıldığından indirme öncesi `df -h` bakılmalıdır.

## 3. B9: CIFAR-100 paneli (eğitim yok)

### 3.1 Soru

B9, dondurulmuş B2'nin birebir CIFAR-100 yinelemesidir: aynı üç tohumlu C1 ResNet-18 ve ViT-Tiny çiftleri (CIFAR-100 eğitimli), CIFAR-10 panelinin bileşimine olabildiğince yakın yedi üyeli bir RobustBench CIFAR-100 L∞ paneli, aynı K-a, K-b, K-c öngörüleri ve karar kuralları. Masa bulgusu CIFAR-100'de çift düzeyi tablonun farklı olduğunu göstermiştir (potansiyel payı 0,283'e karşı CIFAR-10'da 0,541; r_RV 0,154'e karşı 0,115; `04_masa_cozumlemeleri.md` Bölüm 4(4), MASA `4_potansiyel_payi.ozet`); ancak bu çift düzeyi değerler tek üyeli (Pang) panelle kurulmuştur ve model düzeyinde σ, ρ ayrışımını vermez. B9, CIFAR-10'daki manşetin veri kümesine taşınıp taşınmadığını üç tohumla, yani B2 ile aynı çıkarım gücüyle sınar.

### 3.2 Modeller

| Takma ad | Kaynak | Mimari | Rol | Boyut (MB, kestirim) |
|---|---|---|---|---|
| C100_ResNet18_AT_s1001, s1002, s1003 | `models/q1/cifar100/resnet18_s100{1,2,3}/resnet18/adv/adversarial_training/best.pth` (diskte) | ResNet-18 | "C1-R32" | 0 |
| C100_ViT_Tiny_AT_s2001, s2002, s2003 | `models/q1/cifar100/vit_tiny_s200{1,2,3}/vit_tiny/adv/adversarial_training/best.pth` (diskte) | ViT-Tiny 32→224 | "V-scr" | 0 |
| C100_Rice2020Overfitting | RobustBench | PreActResNet-18 | birincil panel P9 (CIFAR-10'daki Wong PRN-18'in karşılığı) | 45 |
| C100_Rade2021Helper_R18_ddpm | RobustBench | PreActResNet-18 (DM) | P9 (CIFAR-10 panelinde de var) | 50 |
| C100_Addepalli2022Efficient_RN18 | RobustBench | ResNet-18 | P9 (CIFAR-10 panelinde de var) | 45 |
| C100_Sehwag2021Proxy | RobustBench | WRN-34-10 | P9 (CIFAR-10'daki Sehwag'ın karşılığı) | 185 |
| C100_Pang2022Robustness_WRN28_10 | diskte, `models/robustbench_zoo/cifar100/Linf/` | WRN-28-10 | P9 (Gowal'ın karşılığı, C1 CIFAR-100 referansı) | 0 |
| C100_Wang2023Better_WRN-28-10 | RobustBench | WRN-28-10 | P9 (Carmon'un karşılığı, ek veri) | 146 |
| C100_Jia2022LAS-AT_34_10 | RobustBench | WRN-34-10 | P9 | 185 |
| C100_Debenedetti2022Light_XCiT-S12 | RobustBench (GitHub sürümü, timm) | XCiT-S12 | ikincil panel | 104 |
| C100_Hendrycks2019Using | RobustBench | WRN-28-10, ImageNet ön eğitimli | ikincil panel | 146 |

Yedek üyeler sırasıyla Chen2021LTD_WRN34_10 ve Cui2023Decoupled_WRN-28-10'dur. Engstrom ve Gowal 28-10'un CIFAR-100 L∞ karşılığı RobustBench'te yoktur (Gowal2020Uncovering CIFAR-100 girdisi WRN-70-16'dır, 1 GB sınırını aşar). İkincil panelde iki ImageNet ön eğitimli üye (biri CNN, biri karma dönüştürücü) bilinçli olarak durur; birincil panel CIFAR-10'daki gibi ImageNet ön eğitimsizdir. Saldırı ve örneklem dondurulmuş §2 ile aynıdır: PGD-10, ε = 8/255, α = 2/255, CIFAR-100 test kümesi n = 10000, tohum 42, kaynak başına tohumlu önbellek. C1 CIFAR-100 kontrol noktalarının seçim kuralı E1 protokolüdür (tek bölme; `results/q1/b8_secim_bandi.json` alanı `veri_kumeleri.cifar100.bolme`); bu, CIFAR-10'daki C1 seçim kuralından farklıdır ve beyan edilir. Ad çakışması uyarısı: `results/q1/b8_secim_bandi.json` Ağustos 2026'daki eski bir "seçim bandı" çözümlemesidir ve bu B8 ile ilgisi yoktur; yeni çıktılar `results/q1/konsey_b8_imagenet/`, `results/q1/konsey_b9_c100/` ve `results/q1/konsey_b10_gradyan/` altına yazılmalıdır.

### 3.3 Çözümleme, süre, kesinlik

Çözümleme dondurulmuş betikle, yalnız tablo değişerek yapılır: `--mod b2 --matris-dizini results/q1/konsey_b9_c100/matris --hucre-tablosu raporlar/konsey_2026-10-29/ek_hucre_tablosu_b9.json`. Aile F_B9 üç sınamalıdır (K-a, K-b, K-c), Holm α = 0,05; betiğin kendi Holm'u bağlayıcıdır. On beş modelin toplamı 74,3 GFLOP'tur, matris 28,5-36,1 dk sürer (`B9_n10000`); dondurulmuş planın doğrusal formülü 15 × (1,15 + 15 × 0,07) ≈ 33 dk verir. Tavan 1,0 GPU-saattir. İndirme yaklaşık 0,90 GB'tır (`B9_indirme_fp32_MB_pang_haric`); önbellek 15 × 10000 × 3 × 32 × 32 × 4 bayt ≈ 1,8 GB'tır.

Kesinlik açısından CIFAR-100 C1 çiftlerinde r'nin koşum SD'si 0,041, log τ̄'nınki 0,023'tür (ON_KAYIT §5, `results/q1/konsey_sentez_r_tau_masa.json`, `kumeler.c100_c1_secilen`). Bu SD model düzeyi ρ'ya vekil alınırsa, üç tohumda df 2 ile K-b'nin %90 aralığının yarı genişliği 2,920 × 0,041/√3 ≈ 0,069'dur; TOST desteği için ρ ortalamasının mutlak değeri yaklaşık 0,03'ün altında kalmalıdır. CIFAR-10'da aynı yarı genişlik 0,017'dir (SD 0,010). B9'da K-b'nin destek alması bu yüzden CIFAR-10'dakinden çok daha zordur; bu önceden yazılır.

## 4. B10: saldırıdan bağımsız simetrik benzerlik (üçüncü fikir)

### 4.1 Neden bu ve neden tek bu

Manşetin taşıyıcı terimi τ̄'dur, ama τ̄ tanım gereği T ve w'den hesaplanır. Sert bir hakem "w-τ̄-r yalnız bir yeniden parametrelemedir, τ̄'ya benzerlik demek için transferden bağımsız bir ölçü göstermediniz" diyecektir. Demontis ve ark. (arXiv 1809.02861, `02_literatur.md` satır 57'de doğrulanmış) aktarılabilirliği hedef kırılganlığı ile vekil ve hedef girdi gradyanlarının kosinüs hizalanmasının çarpımına ayırır ve kosinüs iki modelde simetriktir; T_ij = w_j τ̄_ij biçimi bu çarpımın vekil karmaşıklığı terimi atılmış hâlidir (`02_literatur.md` aynı satır). B10, bu kuramın öngördüğü ölçüyü doğrudan ölçer: c_ij, i ve j modellerinin aynı temiz görüntüde doğru etiketli çapraz entropi kaybının girdiye göre gradyanları arasındaki kosinüsün görüntüler üzerinden ortalamasıdır. c_ij transfer, w ve saldırı adımı içermez. log τ̄_ij'yi öngörürse simetrik terim mekanizması olan bir nicelik olur; öngörmezse τ̄ betimsel bir özet olarak kalır ve makale "benzerlik" sözcüğünü daraltır. Mevcut gradyan ölçümleri bunun yerine geçmez: FÖY M8.10'daki hizalanma tek modelin farklı görüntüleri arasındaki mutlak kosinüstür, modeller arası aynı görüntü kosinüsü hiçbir artefaktta yoktur (`results/C1_REFERANS_FOYU.md` satır 247-269; `src/analysis/gradient_analysis.py::compute_gradient_alignment`).

Diğer adaylar daha zayıf kalmıştır. ImageNetV2 en temiz dış veri olurdu (10 000 hiç görülmemiş görüntü), ama arşivi 1,26 GB'tır ve fable kararı K4'ün ruhuna yakındır; B8 için yedek yol olarak bırakılmıştır. Daha çok CIFAR modeli eklemek dış geçerliliği değil yalnız panel büyüklüğünü artırır. B10 ise üç veri kümesine birden uygulanır, indirme gerektirmez ve B8 ile B9'un matrislerini yeniden kullanır.

### 4.2 Tasarım

Görüntüler her veri kümesinde matrisin görüntüleridir (CIFAR-10 ve CIFAR-100 test kümesinin ilk 10000'i, ImageNet'te B8 manifesti); gradyanlar [0, 1] piksel uzayında, model içi normalizasyon dahil, eval kipinde ve fp32 ile alınır. Birincil c_ij bütün görüntülerin ortalamasıdır; iki modelin de temiz doğru olduğu görüntülerle sınırlı c_ij duyarlılıktır. Modeller: CIFAR-10'da B4'ün son 20x20 matrisindeki 20 model (B3 tamamlanmazsa B2'nin 14 modeli; bu yedek kural önceden yazılır), CIFAR-100'de B9'un 15 modeli, ImageNet'te B8'in ön işleme denetimini geçen modelleri. Gradyanlar saklanmaz; her grupta bütün modellerin gradyanı hesaplanır, çiftlerin görüntü başına kosinüsü biriktirilir (ImageNet'te 25'lik grupta 14 model × 25 × 150 528 × 4 bayt ≈ 211 MB GPU belleği). Çıktı görüntü başına çift kosinüsleri (float16) ve model başına gradyan normlarıdır.

Sınama her veri kümesinde ayrıdır: sırasız model çiftleri üzerinde c_ij ile bölünmüş yarı log τ̄_ij arasındaki Spearman korelasyonu, model etiketlerinin ortak permütasyonuyla Mantel sınaması (9999 permütasyon, tek yönlü). Mantel, aynı modeli paylaşan çiftlerin bağımlılığını hesaba katan standart yoldur. Üç veri kümesi bir ailedir (F_B10, Holm). Ayrıntılı öngörü ve çürütme ölçütleri ek ön kayıttadır.

### 4.3 Süre

Model başına görüntü başına bir ileri ve bir geri geçiş (yaklaşık 3 ileri geçiş) yeterlidir: ImageNet n = 1000'de 0,97 dk, CIFAR-100 n = 10000'de 2,36 dk, CIFAR-10 B4 kümesinde 1,89 dk (`_ek_sure_kestirimi.json`, `B10_gradyan_dk_hiz_b`). Tavan 0,25 GPU-saattir.

## 5. Kod değişiklikleri (yazılmadı, plan)

Dondurulmuş iki dosyaya (`experiments/q1_konsey_ayrisim.py`, `raporlar/konsey_2026-10-29/hucre_tablosu.json`) dokunulmaz. B9 için matris betiğinde değişiklik gerekmez; B8 için gereken ekler varsayılan davranışı değiştirmeyecek biçimde tasarlanmıştır ve mevcut regresyon matrisiyle (`results/q1/konsey_smoke/regresyon/`) yeniden sınanmalıdır.

1. `experiments/c1_c3_transfer_matrix.py`. `main()` argümanlarına `--eps` ve `--alpha` (255 cinsinden, örneğin 4 ve 1; verilmezse eski sabitler), `--batch-size` (varsayılan 50; şu an `get_loaders(..., test_batch_size=50)` sabit), `--manifest` ve `--logit-alt-kume` eklenir; `--dataset` seçeneklerine `imagenet_heldout` katılır. Yeni `HeldoutImageNet(Dataset)` sınıfı ve `imagenet_heldout_loader(manifest, batch_size)` işlevi manifestteki dosyaları sırasıyla açar, `Resize(256, BICUBIC, antialias=True)`, `CenterCrop(224)`, `ToTensor()` uygular, etiket olarak ImageNet indeksini verir, karıştırma yapmaz. `load_wrn()` içinde `imagenet_heldout` RobustBench veri kümesi adına (`imagenet`) çevrilir ve ImageNet için varsayılan referans eklenmez (`has_rb` mantığı). `RB_TIMM_CACHE` sözlüğü (model, veri kümesi) anahtarlı olur ve `_restore_rb_timm_cache()` ile ilk indirmeden sonra hub önbelleğini `models/robustbench_zoo/<ds>/Linf/` altına kopyalayan yeni `_persist_rb_timm_cache()` işlevi ImageNet ve CIFAR-100 XCiT'i kapsar. Önbellek dosya kökü (`stem`) yalnız `--eps` verildiğinde `_e{eps*255:g}` eki alır; böylece eski önbellekler geçerli kalır, farklı ε'lu örnekler karışmaz (hücre metası zaten `eps` taşır). `RestrictLogits(nn.Module)` sarmalayıcısı `--logit-alt-kume` verilince logitleri seçili indekslere indirger ve etiketleri yeniden numaralar (yalnız Tier 2). `transfer_matrix.json` ImageNet koşusunda `manifest_sha256`, `on_isleme` ve `eps_255` alanlarını taşır.
2. `scripts/q1_b8_manifest.py` (yeni). Açılmış iki arşivi tarar, `ILSVRC2012_val_*` dosyalarını seçer, klasör wnid'ini eğitim dosyası önekleriyle denetler, timm `ImageNetInfo` ile indekse çevirir, dosya başına SHA-256 hesaplar ve `data/imagenet_heldout/manifest.json` ile sınıf başına sayım özetini yazar. Görüntü sayısı 400'ün altındaysa durur (Bölüm 8).
3. `scripts/q1_ek_indir.py` (yeni, CPU). B8 ve B9 modellerini `CUDA_VISIBLE_DEVICES=` ile `robustbench.utils.load_model` üzerinden indirir; bayt, SHA-256, parametre, süre ve durum alanlarını `results/q1/konsey_b8_imagenet/indirmeler.json` ve `results/q1/konsey_b9_c100/indirmeler.json` dosyasına yazar (`results/q1/konsey_smoke/indirmeler.json` biçimi). gdown hatasında üç yeniden deneme yapar, sonra elle indirme bağlantısını (`https://drive.google.com/uc?id=<gdrive_id>`) ve hedef yolu yazar.
4. `experiments/q1_b8_on_isleme_denetimi.py` (yeni, CPU ya da GPU). Bölüm 2.5'teki iki temiz doğruluğu ve kuralın sonucunu `results/q1/konsey_b8_imagenet/on_isleme_denetimi.json` dosyasına yazar.
5. `raporlar/konsey_2026-10-29/ek_hucre_tablosu_b8.json` ve `ek_hucre_tablosu_b9.json` (yeni). `hucre_tablosu.json` şemasıyla aynıdır (`modeller`, `hucreler`, `b2_tohum_ciftleri`, `panel_dondurma`); B8'de `tohum` alanı çift numarasıdır (1, 2, 3; Mo için 4).
6. `experiments/q1_ek_gradyan_kosinus.py` (yeni). Matris betiğinin yükleyicilerini (`load_local`, `load_wrn`, `_iter_batches`, `imagenet_heldout_loader`) içe aktarır; `--dataset`, `--model`, `--rb-model`, `--manifest`, `--n-samples`, `--batch-size`, `--cikti` alır; `kosinus.npz` ve özet JSON yazar.
7. `experiments/q1_ek_ayrisim.py` (yeni). Dondurulmuş betiği `importlib` ile yükler ve çalışma anında SHA-256'sının `4bce2c98...b667389` olduğunu denetler (değilse durur). `--mod b8` dondurulmuş çıktıyı okuyup H8-σ'yı, dört sınamalı F_B8 Holm'unu ve keşifsel çözümlemeleri; `--mod b10` Mantel sınamalarını ve F_B10 Holm'unu yapar. Kendi SHA-256'sı ek ön kaydın dondurma ekine yazılır.
8. `scripts/konsey_ek_zincir.sh` (yeni). B6 bittikten sonra kullanıcının başlatacağı sıra: `nvidia-smi` ile başka eğitim yokken B9, B8, B10. `scripts/konsey_tam_zincir.sh`, `logs/` ve `models/` altındaki B3 dosyalarına dokunmaz.

Kodun sınanması üç adımda yapılmalıdır: (a) varsayılan bayraklarla regresyon matrisi bit düzeyinde eski çıktıyı verir; (b) `--dataset imagenet_heldout` 16 görüntülük sahte manifestle (CPU) uçtan uca çalışır ve iki modelli 2x2 matris üretir; (c) dondurulmuş `--mod b2`, B8 ve B9 tablolarıyla sahte matrislerde koşar (sahte sınamanın `SINAMA_SONUC_DEGIL` deseniyle). Kod işi `kod-mimar` ajanına tam yollarla verilebilir.

## 6. Takvim ve bütçe

| Blok | İş | Beklenen | Tavan | Ne zaman | Tier |
|---|---|---|---|---|---|
| B8-0 | Veri ve model indirme, manifest, ön işleme denetimi | CPU, yaklaşık 1 sa (ağa bağlı) | 0 GPU | B3 sürerken | 1 |
| B9-0 | B9 indirmeleri | CPU | 0 GPU | B3 sürerken | 1 |
| B9 | 15x15 CIFAR-100 matrisi | 28,5-36,1 dk | 1,0 sa | B6'dan sonra | 1 |
| B8 | 14x14 ImageNet matrisi (n ≈ 1000) | 11,5-14,6 dk | 0,75 sa | B9'dan sonra | 1 |
| B10 | Üç kümede gradyan kosinüsü | yaklaşık 5 dk | 0,25 sa | B4 ve B8 sonrası | 1 |
| B8-S4 | 20 sınıf kısıtlı ikinci ImageNet matrisi | 11,5-14,6 dk | 0,5 sa | Tier 1'den sonra | 2 |

Toplam tavan Tier 1 için 2,0, Tier 2 ile 2,5 GPU-saattir; bu bütçe dondurulmuş Dondurma eki (e)'deki 42,2 GPU-saatin dışındadır ve B3'ün bekçi kuralına dokunmaz. B8 ve B9'un B3 ile aynı anda koşulması önerilmez: B3 pilotu boş GPU'da ölçülmüştür ve paylaşım B3'ün duvar saatini iki katına çıkarabilir (`results/q1/konsey_pilot_zaman.json`, `paylasimda_iki_kat_yavaslama_W_sa`).

## 7. Kayıt defteri (durum: planlandı)

Projede `experiments/registry.yaml` yoktur; eşdeğeri `KONSEY_PLANI.md` §4 tablosudur ve başka bir ajan bu dosyalarla çalıştığı için dokunulmamıştır. Aşağıdaki satırlar ek ön kayıt dondurulunca plan tablosuna işlenmelidir.

| Kimlik | Amaç | Yapılandırma | Tohum | Ölçü | GPU-saat (tavan) | Durum |
|---|---|---|---|---|---|---|
| B8 | ImageNet ölçeğinde σ, ρ ayrışımı | 14 RobustBench ImageNet L∞ modeli, ILSVRC2012_val alt kümesi, PGD-10 ε = 4/255, α = 1/255, 1000 sınıf | 42 (kaynak başına) | K-a, K-b, K-c, H8-σ | 0,75 | planlandı |
| B8-S4 | 20 sınıf kısıtı duyarlılığı | B8 ile aynı, logitler 20 sınıfa | 42 | aynı nicelikler, keşifsel | 0,5 | planlandı |
| B9 | CIFAR-100 yinelemesi | 6 C1 + 7 panel + 2 ikincil, PGD-10 ε = 8/255, n = 10000 | 42; C1 tohumları 1001-1003, 2001-2003 | K-a, K-b, K-c | 1,0 | planlandı |
| B10 | Saldırıdan bağımsız benzerlik | girdi gradyanı kosinüsü, üç küme | yok (belirlenimci) | Mantel Spearman, c ile log τ̄ | 0,25 | planlandı |

## 8. Sonuçlar hayal kırıklığı verirse

Manifestte 400'den az görüntü çıkarsa (dosya adları ImageNet kimliğini taşımıyorsa) önce v1 arşivleri (imagenette-320 ve imagewoof-320, aynı bağlantılarda, toplam 669 MB) denenir; README'ye göre v1'in doğrulama kümesi "much smaller"dır ve büyük olasılıkla ImageNet doğrulama görüntüleridir, bu da dosya adlarıyla doğrulanmalıdır. O da olmazsa tek temiz yol ImageNetV2 matched-frequency'dir (1,26 GB); 1 GB sınırını aştığı için fable onayı gerekir ve onaysız indirilmez. Her iki yol da tutmazsa B8 iptal edilir ve dış geçerlilik yalnız B9 ve Mahmood dış verisiyle (yalnız bağlam olarak) savunulur.

gdown kotası ya da kaldırılmış dosya yüzünden bir model 48 saat içinde indirilemezse ön kaydın "yüklenemeyen üye" tanımı uygulanır: P8'de yedek Wong2020Fast girer, P9'da yedekler sırayla girer. Bir aynı tarifli çiftin bir üyesi kaybedilirse o çift K-a'dan ve H8-σ'dan çıkar; iki çiftin altına düşülürse bu iki sınama hesaplanamaz sayılır, p = 1 ile ailede kalır ve değerler betimsel verilir.

B8'de dönüştürücüler zayıf kaynak çıkmazsa (çiftlerde D ≤ 0,10), K-a payda kuralıyla kararsız olur. Bu bir başarısızlık değil, "ImageNet ölçeğinde aynı tarifli dönüştürücüler zayıf kaynak değildir" diye raporlanacak bir sonuçtur ve CIFAR'daki manşetin ölçek ya da tarif koşuluna bağlanması gerektiğini söyler. H8-σ çürütülürse benzemezlik iddiası CIFAR ölçeğiyle ve ViT-Tiny ile sınırlanır. B9'da K-b çürütülürse (yönlü terim CIFAR-100'de büyükse) "küçük yönlü terim" cümlesi CIFAR-10'a daraltılır; masa verisindeki SVHN ters işareti (MASA `4_potansiyel_payi`) bununla birlikte "yönlü terim veri kümesine bağlıdır" olarak yazılır. B10 çürütülürse τ̄ "simetrik benzerlik" yerine "simetrik transfer verimi" diye adlandırılır ve Demontis bağlantısı mekanizma iddiası olarak kullanılmaz. Hiçbir durumda olumsuz sonuç metinden çıkarılmaz.

## 9. Riskler

1. Imagenette doğrulama görüntülerinin çoğunun ImageNet eğitim kümesinden gelmesi. Bölüm 1'de doğrulandı; dosya adı filtresiyle giderilir. Filtre sonrası örneklem küçüktür (en çok yaklaşık 1000) ve Bölüm 2.7'deki kesinlik sınırını getirir.
2. 10 sınıf kısıtının w'yi ve T'yi modeller arasında eşit olmayan biçimde değiştirmesi. Birincil çözümleme kısıtsızdır; kısıt yalnız Tier 2 duyarlılıktır.
3. ImageNet-21k ya da 22k ön eğitimi kullanan modellerin ImageNet-1k doğrulama görüntülerine benzerlerini görmüş olması. Her modelin ön eğitim verisi dondurmadan önce makalesinden okunup tabloya yazılmalıdır; böyle modeller dışlanarak duyarlılık yapılır. Bazı grupların ImageNet doğrulama kümesini model seçiminde kullanmış olması ayrıca hafif bir seçim yanlılığıdır ve beyan edilir.
4. Farklı ön işleme beklentisi. Ortak bicubic 256/224 hattı Res256Crop224 (bilinear), Res224 (Mo, ezme) ve Crop288 (Wong) bekleyen modellerden sapar; Singh ConvNeXt ve ViT-B-CvSt ile Chen WRN-50-2 sarmalayıcısında görünür normalizasyon yoktur. Hepsi Bölüm 2.5'teki temiz doğruluk denetimiyle T görülmeden yakalanır.
5. timm sürüm kayması. Singh ve Liu modelleri timm yapıcılarıyla kurulur; konteynerde timm 1.0.27 vardır ve RobustBench Swin için uyarlama kodu taşır. Yükleme hatası ya da düşük temiz doğruluk aynı denetimle yakalanır.
6. gdown indirme sorunları. XCiT dışındaki bütün adaylar Google Drive'dadır; kota ve onay sayfası hataları olasıdır. İndirme betiği yeniden dener ve elle indirme yolunu yazar; B1'de CIFAR-10 panelinin üç üyesi gdown ile sorunsuz indirilmiştir (`results/q1/konsey_smoke/indirmeler.json`, durum "OK").
7. Disk. Toplam en kötü durum yaklaşık 13 GB'tır (modeller 4,2 GB, veri 0,67 GB ve açılmış hâli, ImageNet önbelleği 8,4 GB, CIFAR-100 önbelleği 1,8 GB). Disk 56 GB boştur ama kök bölüm %95 doludur ve B3 kontrol noktaları da yazılmaktadır; ImageNet önbelleği float16 tutulmalı ya da matristen sonra silinmelidir.
8. B8'in az çiftle çıkarımı. Üç aynı tarifli çift df 2 verir; B8 büyük olasılıkla yön ve kestirim sonucu üretir, eşdeğerlik değil. Bu önceden yazılmıştır.
9. Liu çiftinde tarif ortaklığının doğrulanmamış olması. Dondurmadan önce makaleden okunmalıdır.
10. Ek ön kaydın B2 çıktısı açılmadan dondurulamaması. B2 şu an koşmaktadır; B9'un öngörüleri B2'ninkilerle aynı olduğu için B2 sonucu görülmeden dondurulmaları yinelemenin bağımsızlığı açısından önemlidir. B2 çıktısı dondurmadan önce açılırsa ek ön kaydın §1'ine yazılmalıdır.
11. B10'da karıştırıcılar. Büyük ve çok gürbüz modeller hem yüksek gradyan kosinüsü hem yüksek τ̄ gösterebilir; aile göstergesini denetleyen kısmi Mantel ve model düzeyi γ ile σ ilişkisi keşifsel olarak raporlanır.
12. Lisans. fastai deposu Apache-2.0'dır, görüntülerin kendisi ImageNet koşullarına tabidir; RobustBench model lisansları modele göre değişir ve bazı depolarda lisans yazmaz (P2 önerisi satır 63). Yayında yalnız türetilmiş sayılar paylaşılır, görüntü ve ağırlık dağıtılmaz.

## 10. Dondurulmuş ön kayda etkisi

Ek bloklar dondurulmuş ön kaydı değiştirmez. Dondurulmuş dosya, `experiments/q1_konsey_ayrisim.py` ve `hucre_tablosu.json` olduğu gibi kalır; SHA-256 özetleri sırasıyla `4bce2c98...b667389` ve `2a891331...bfe5500`'dür ve bu oturumda yeniden hesaplanıp aynı bulunmuştur. B8 ve B9 dondurulmuş betiği yeni girdi tablolarıyla çağırır; bu, dondurulmuş §7'deki "betik ya da hücre tablosu özeti farklıysa" kuralına girmez, çünkü değişen dosya dondurulmuş hücre tablosu değil, ayrı adlı yeni tablolardır ve onların özetleri ek ön kayıtta dondurulur. Yeni aileler (F_B8, F_B9, F_B10) F_B2 ve F_B4'ün Holm hesaplarına girmez; dondurulmuş §6'nın O1-O5a sonuç haritası yalnız B2-B6'dan belirlenir ve ek bloklar bölge değiştirmez, yalnız ek cümle ekler ya da manşete önceden yazılmış bir niteleme getirir (ek ön kayıt §8). GPU bütçesi dondurulmuş Dondurma eki (e)'nin dışındadır ve B6'dan sonra harcanır. Ek ön kayıt taslağı B2-B6 sonuçları görülmeden yazılmıştır ve aynı koşulla dondurulmalıdır.

Ana oturumun karar vermesi gereken dört nokta şunlardır: Imagewoof'un B8'e katılması (öneri: evet, n'yi iki katına çıkarır, Imagenette ve Imagewoof ayrı alt küme duyarlılığıyla), ImageNetV2'nin yalnız yedek yol olarak 1,26 GB'la onaylanıp onaylanmayacağı, Liu çiftinin tarif ortaklığı denetiminin dondurmadan önce yapılması ve ek ön kaydın B2 çıktısı açılmadan dondurulması.
