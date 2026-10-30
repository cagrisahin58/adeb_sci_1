# Ek deney literatür ve uygulanabilirlik taraması: F1 (ImageNet ölçeği), F2 (CIFAR-100 paneli) ve üçüncü öneri (30.10.2026)

Hazırlayan: literatür ve uygulanabilirlik tarayıcısı (opus alt ajan). GPU kullanılmamış, hiçbir model ya da veri kümesi indirilmemiştir. Model listeleri `adeb_eval` konteynerindeki robustbench kurulumunun kendi kodundan (`robustbench.model_zoo.model_dicts`, `robustbench.utils.load_model`) okunmuş, kontrol noktası boyutları indirme yapılmadan HTTP HEAD isteğinin `Content-Length` başlığından alınmış, temiz ve AutoAttack doğrulukları RobustBench deposunun `model_info/<veri>/Linf/<ad>.json` dosyalarından (raw.githubusercontent.com, master dalı) çekilmiştir. Önceki konsey taraması (`02_literatur.md`, 29.10.2026) yinelenmemiş, yalnız genişletilmiştir.

## Yönetici özeti

F1'in en önemli sorunu veri tarafındadır: Imagenette'in doğrulama kümesi ImageNet doğrulama kümesinden gelmez. imagenette2 sürümünde Aralık 2019'da 70/30 eğitim-doğrulama bölmesine geçilmiş (fastai/imagenette README) ve doğrulama klasöründeki 3925 dosyanın yalnız 134'ü `ILSVRC2012_val_` adlı, 3791'i (%96,6) ImageNet eğitim kümesi adlandırmasıyla (`n01440764_XXXX.JPEG`) gelmektedir; yani RobustBench modellerinin neredeyse tamamı bu görüntüleri eğitimde görmüştür. Bu yüzden F1 Imagenette doğrulama kümesiyle yapılmamalı; en az emekle temiz çözüm ImageNetV2 MatchedFrequency'dir (1,26 GB, 10.000 yeni Flickr görüntüsü, 1000 sınıfın tam logitiyle, kısıtlama gerektirmez). Literatürde ImageNet ölçeğinde gürbüz modeller arası transfer ısı haritası zaten vardır (Liu ve ark. 2023, arXiv 2302.14301, Şekil 8; Awad ve ark. 2025, arXiv 2512.02830), ama hiçbiri hedef-doğru koşullama, beyaz kutu kırılganlığına göre ayrışım ya da CNN-ViT yönlü asimetri sorusu sormaz; F1'in yeniliği ölçümde değil ayrışımın bağımsız gruplarca eğitilmiş, mimarisi çeşitli bir panelde yinelenmesindedir. Önerilen F1 paneli sekiz modeldir (Salman R50 ve R18, Liu ConvNeXt-B ve Swin-B, Mo ViT-B, Singh ViT-S-ConvStem ve ConvNeXt-T-ConvStem, Debenedetti XCiT-S12), indirme 1514 MB'tır ve iki aynı tarifli CNN-dönüştürücü çifti içerir. F2 için RobustBench CIFAR-100 L∞ listesinde dönüştürücü olarak yalnız ImageNet ön eğitimli XCiT vardır; beş modellik ek (525 MB) mevcut 3x3 ile birleşince sekiz-dokuz üyeli bir panel kurar ve ImageNet ön eğitimli bir CNN (Hendrycks2019Using) sayesinde "dönüştürücü mü, ön eğitim mi" sorusuna panel düzeyinde kaba bir karşıt sağlar. Üçüncü öneri olarak indirme gerektirmeyen tek bir deney öneriyorum: mevcut CIFAR-10 havuzunda ε süpürmesi (2, 4, 6, 12/255), çünkü masa çözümlemesinin bulduğu ölçek bağımlılığını (ViT'nin ρ'su log ölçekte +0,043, logit ölçekte −0,265) doğrudan sınayan tek ucuz düzenektir. Üç işin toplamı yaklaşık 2 GPU-saat ve 3,3 GB indirmedir; hepsi B3 eğitim zinciri bittikten sonra koşmalıdır, çünkü B3'ün 80 epokluk tavanı boş GPU'da ölçülmüş pilot süresine dayanır.

## Karar kartı

| | |
|---|---|
| Soru | F1 (ImageNet ölçeği) ve F2 (CIFAR-100 paneli) eğitimsiz ek deneyleri yapılmalı mı, hangi veri ve modellerle; üçüncü bir ekleme var mı? |
| Kanıt | Imagenette2 doğrulamasının %96,6'sı ImageNet eğitim görüntüsü (Bölüm 4.2); ImageNetV2 MatchedFrequency 1.264.079.360 bayt, MIT kod lisansı, görüntüler Flickr lisanslı (Bölüm 4.3); RobustBench ImageNet L∞'da 29 gürbüz model, seçilen sekizinin toplamı 1514 MB, hepsi tek tek 1 GB altı (Bölüm 3); CIFAR-100 L∞'da 37 gürbüz model, yalnız XCiT dönüştürücü (Bölüm 6); en yakın öncüller ayrışım yapmıyor (Bölüm 2); matris betiğinde ε sabit ve önbellek adında ε yok (Bölüm 8). |
| Seçenekler | (a) F1'i ImageNetV2 ile, F2'yi beş ek modelle ve ε süpürmesini birlikte yap; (b) yalnız F2 ve ε süpürmesi (indirme 525 MB, ImageNet benzeri veri yok, K4 kararına hiç dokunmaz); (c) F1'i Imagenette içindeki ImageNet doğrulama görüntüleriyle (en çok yaklaşık 500, sınıf başına 50) ve 10 sınıflı logitle yap; (d) hiçbiri. |
| Öneri | (a). F1 ImageNetV2 ile, F2 beş ek modelle, ε süpürmesi havuzla; üçü de ön kayıttan ayrı, koşudan önce yazılmış kısa bir ek ön kayıt dosyasıyla ve keşifsel etiketiyle. K4 kararı "ImageNet indirilmeyecek" derken 6,4 GB'lık kapılı ImageNet'i kastediyorsa ImageNetV2 ona aykırı değildir; aykırı sayılırsa (b) seçilir ve F1 makaleden çıkar, (c) seçilmez. |
| Karar satırı (fable doldurur) | ____ |

## 1. Kapsam ve tarama yöntemi

Tarama 30.10.2026'da 2021-2026 aralığında, ImageNet ölçeğinde CNN, ViT ve hibrit mimariler arasında transfer saldırısı, özellikle gürbüz (çekişmeli eğitilmiş) modeller arası transfer ve kaynak-hedef ayrıştırması için yapılmıştır. Dört web araması (ikisi genişletilmiş), on bir sayfa okuması ve on yedi arXiv kimliğinin arXiv özet sayfasındaki `citation_title` ve `citation_author` meta etiketlerinden doğrulanması yapılmıştır; arXiv API hız sınırına takıldığından (yanıt "Rate exceeded") doğrulama özet sayfaları üzerinden yürütülmüştür. "Doğrulandı" etiketi başlık, ilk yazar ve kimliğin birincil sayfadan okunduğunu; içeriğin özetten mi tam metinden mi geldiği ayrıca yazılmıştır. Son on iki ay için "asymmetric transferability", "robust surrogate", "transfer attack matrix RobustBench ImageNet" sorgularıyla rekabet taraması yapılmış, Awad ve ark. (Aralık 2025) ile TESSER (Mayıs 2025) dışında yeni bir yakın çalışma çıkmamıştır.

## 2. Literatür: ImageNet ölçeğinde CNN-ViT transferi ve F1'in yeniliği

| Çalışma ve kimlik | Ne gösteriyor | F1 ile örtüşme |
|---|---|---|
| Liu ve ark., "A Comprehensive Study on Robustness of Image Classification Models: Benchmarking and Rethinking", arXiv 2302.14301 (doğrulandı, html; yorum alanı IJCV hakemde) | ARES-Bench: 55 ImageNet modeli. §4.3.2 ve Şekil 8'de çekişmeli eğitilmiş modeller arasında VMI-FGSM ile kaynak-hedef transfer ısı haritası verir; "beyaz kutu gürbüzlüğü yüksek modeller kara kutuya da dayanıklı", "CNN'ler içinde ConvNeXt, dönüştürücüler içinde Swin transfer saldırısına en dayanıklı" der. Standart modellerde CNN ile dönüştürücü arasında transferin aile içine göre düşük olduğunu yazar. AT modelleri için kaynak-hedef asimetrisi raporlanmaz. AT tarifinin başlatması (sıfırdan ya da ön eğitimli) metnin okunabilen kısmında açık değildir (doğrulanmadı, Ek A okunamadı). | Yüksek. F1'in ham matrisinin en yakın öncülüdür ve F1 panelinin iki modeli (ConvNeXt-B, Swin-B) bu çalışmanındır. Metinde açıkça anılmalı; F1 "ImageNet'te gürbüz modeller arası transfer matrisi" iddiası taşıyamaz. |
| Awad, Mohamed, Gomaa, "Defense That Attacks: How Robust Models Become Better Attackers", arXiv 2512.02830 (önceki taramada doğrulandı) | Aynı Free-AT protokolüyle eğitilmiş 36 CNN ve ViT'de çekişmeli eğitilmiş vekillerin dört yönde daha iyi aktardığını bildirir; asimetri ve koşullama yoktur. | Yüksek, aile düzeyi kaynak karşılaştırması için. |
| Sitawarin ve ark., "PubDef: Defending Against Transfer Attacks From Public Models", arXiv 2310.17645, ICLR 2024 (doğrulandı, özet ve arama özeti) | CIFAR-10, CIFAR-100 ve ImageNet'te 24 halka açık kaynak model ve 11 saldırıyla 264 transfer saldırısı; kaynak model bazlı doğruluk dökümü verir. Odak savunmadır, kaynak-hedef ayrışımı yoktur. | Orta. Halka açık gürbüz ve standart modellerden transferin büyük ölçekli kaydı. |
| Jiang ve Chen, arXiv 2606.22516 (önceki taramada doğrulandı) | Gürbüz ImageNet vekilleri (Engstrom ve Salman R50, Mo ViT-B, ARES ConvNeXt-B, Singh ConvStem ViT-B) ile Swin-B ve ConvNeXt-B hedeflerine transfer. | Orta-yüksek. F1 panelinin dört modeli bu çalışmada da vekildir. |
| Shao ve ark., "On the Adversarial Robustness of Vision Transformers", arXiv 2103.15670, TMLR (önceki taramada doğrulandı) | Standart rejimde ImageNet-21k ön eğitimli ViT'lerin güçlü kaynak, CNN'den ViT'ye transferin zayıf olduğunu bildirir. | Orta. Standart rejim, ayrışım yok. |
| Mahmood, Mahmood, van Dijk, arXiv 2104.02610, ICCV 2021 (önceki taramada doğrulandı) | Aile arası düşük transfer; her-ikisi-doğru m = 1000; köşegen bağımsız ikinci kopya olduğundan w tanımsız (`04_masa_cozumlemeleri.md` §4(3)). | Orta-yüksek. F1, Mahmood'da kurulamayan ayrışımı gerçek beyaz kutu köşegeniyle kurar. |
| Naseer ve ark., "On Improving Adversarial Transferability of Vision Transformers", arXiv 2106.04169, ICLR 2022 (doğrulandı, meta) | ViT kaynaklı düşük aktarımın eniyi olmayan saldırıdan kaynaklandığını savunur. | Orta. B5'teki MI ve TGR ile karşılanıyor; F1'de yalnız PGD olursa aynı itiraz gelir. |
| Wei ve ark., "Towards Transferable Adversarial Attacks on Vision Transformers", arXiv 2109.04176, AAAI 2022 (doğrulandı, meta; yayın yeri arama özetinden) | ViT'ye özgü PNA ve PatchOut ile ViT'den CNN'ye aktarımı artırır. | Düşük-orta, aynı itirazın kaynağı. |
| Bhojanapalli ve ark., "Understanding Robustness of Transformers for Image Classification", arXiv 2103.14586 (doğrulandı, meta) | Standart ViT ve ResNet arasında ImageNet ölçeğinde düşük transfer bildirir (içerik özetten değil önceki bilgiden; doğrulanmadı). | Düşük. |
| Benz ve ark., "Adversarial Robustness Comparison of Vision Transformer and MLP-Mixer to CNNs", arXiv 2110.02797 (doğrulandı, meta; içerik doğrulanmadı) | ViT, MLP-Mixer ve CNN'ler arasında standart rejimde transfer karşılaştırması. | Düşük. |
| Bai ve ark., "Are Transformers More Robust Than CNNs?", arXiv 2111.05464, NeurIPS 2021 (doğrulandı, meta) | Aynı tarifle eğitilen CNN'in dönüştürücü kadar gürbüz olabildiğini gösterir. | Düşük-orta; aynı tarif fikrinin öncülü. |
| Singh, Croce, Hein, "Revisiting Adversarial Training for ImageNet", arXiv 2303.01870, NeurIPS 2023 (doğrulandı, meta ve depo README) | Aynı tarifle ViT-S, ViT-S-ConvStem, ConvNeXt-T, ConvNeXt-T-ConvStem (300 epok) yayımlar; README'ye göre AT temiz eğitilmiş bir modelden başlatılmıştır ("weights for the clean model (the one used as initialization for Adversarial Training)"). | Orta. F1'deki aynı tarifli çiftin kaynağı; gövde etkisi gürbüzlük için gösterilmiş, transfer kaynağı rolü için değil. |
| Mo ve ark., "When Adversarial Training Meets Vision Transformers", arXiv 2210.07540, NeurIPS 2022 (doğrulandı, html) | ImageNet-1k'da ViT'ler ε = 4/255 ile yalnız 10 epok çekişmeli eğitilir; §3'te "By default, all models are pretrained on ImageNet-1K" yazar, ImageNet ekinin başlatmayı ayrıca yazıp yazmadığı açık değildir. Bu çalışma deneylerinde Imagenette'i de kullanır. | Orta. Mo ViT-B F1'deki tek düz yamalı ViT'dir ve kısa AT ile ön eğitimli başlatma taşır; "zayıf kaynak" okuması bu modelde başlatma ile karışır. |
| Debenedetti, Sehwag, Mittal, "A Light Recipe to Train Robust Vision Transformers", arXiv 2209.07399, SaTML 2023 (doğrulandı, özet) | XCiT için hafif AT tarifi; ImageNet-1k'da büyük modellere genellendiğini söyler. ImageNet XCiT'in sıfırdan eğitilip eğitilmediği özetten okunamadı (doğrulanmadı). CIFAR XCiT'lerinin ImageNet XCiT'ten ince ayarlandığı önceki taramada ar5iv metninden doğrulanmıştır (`01_oneri_P2_dis_gecerlilik.md` satır 24). | Orta. XCiT CIFAR-10 havuzunda da vardır; F1'e girerse iki veri kümesi arasında aynı ailenin köprüsü olur. |
| Salman ve ark., "Do Adversarially Robust ImageNet Models Transfer Better?", arXiv 2007.08489, NeurIPS 2020 (doğrulandı, meta) | Gürbüz ImageNet ResNet'leri; F1'in klasik CNN kolu. Konu temsil aktarımıdır, saldırı transferi değil; terim karışıklığı önlenmelidir. | Düşük. |
| Guesmi, Ouni, Shafique, TESSER, arXiv 2505.19613 (arama özeti; doğrulanmadı) | ViT kaynaklı transferi artıran saldırı; gürbüz CNN'lere karşı ASR bildirir. | Düşük, rekabet değil. |

F1'in yeniliği bu tabloya göre dar ama gerçektir. ImageNet ölçeğinde gürbüz modeller arası ham transfer matrisi Liu ve ark.'nda, kaynak bazlı transfer kaydı PubDef'te, aynı tarifli CNN-ViT vekil karşılaştırması Awad ve ark.'nda vardır. Taranan çalışmaların hiçbiri hedef-doğru koşullu yanıltma oranını beyaz kutu köşegeniyle bölüp simetrik benzerlik ve yönlü terim olarak ayırmamış, CNN-ViT asimetrisinin işaretini ve kaynağını sormamıştır. F1 bu yüzden "ImageNet ölçeğinde ilk transfer matrisi" olarak değil, "CIFAR'da önceden kaydedilmiş w-τ̄-r ayrışımının bağımsız gruplarca eğitilmiş, mimarisi çeşitli bir ImageNet panelinde yinelenmesi" olarak yazılabilir. "İlk kez" ifadesi bu taramayla desteklenmez, yalnız "bulunamadı (30.10.2026 taraması)" biçiminde yazılabilir.

F1 paneli başlatma bakımından da türdeş değildir: Salman modelleri Madry kütüphanesiyle sıfırdan, Singh modelleri temiz modelden, Mo ViT-B büyük olasılıkla ImageNet-1k temiz ağırlıklarından 10 epok AT ile, Liu ve Debenedetti modellerinin başlatması doğrulanmamıştır. Ön kayıttaki 2x2'nin başlatma etmeni bu panelde kontrol edilmez; F1'in sonucu mimari etkisi olarak değil "bağımsız, gerçek dünya panelinde ayrışımın davranışı" olarak okunmalıdır.

## 3. RobustBench ImageNet L∞ (ε = 4/255) listesi

Konteynerdeki robustbench kurulumunda (`/usr/local/lib/python3.12/dist-packages/robustbench`, sürüm etiketi yok; timm 1.0.27) ImageNet L∞ altında 30 girdi vardır; biri `Standard_R50` (AA 0,0) olduğundan gürbüz model sayısı 29'dur. İndirme yolu kodun kendisinden okunmuştur: `load_model` önce timm adına bakar (XCiT'ler `timm.create_model(..., pretrained=True)` ile GitHub release HTTP adresinden iner), değilse `download_gdrive_new` ile gdown üzerinden Google Drive'dan iner; liste girdisi olan modeller birden çok Drive dosyası indirir. Boyutlar HEAD isteğiyle alınmıştır (Drive için `drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`). Temiz ve AA doğrulukları `model_info/imagenet/Linf/<ad>.json` dosyalarındandır ve RobustBench'in 5000 ImageNet doğrulama görüntüsündeki değerleridir.

| Model | Mimari | Tür | Temiz / AA (%) | Dosya (bayt) | Kaynak | Önişleme |
|---|---|---|---|---|---|---|
| Wong2020Fast | ResNet-50 | CNN | 55,62 / 26,24 | 102.546.991 | Drive | Crop288 |
| Engstrom2019Robustness | ResNet-50 | CNN | 62,56 / 29,22 | 102.529.618 | Drive | Res256Crop224 |
| Salman2020Do_R50 | ResNet-50 | CNN | 64,02 / 34,96 | 102.546.991 (HEAD, Salman R50) | Drive | Res256Crop224 |
| Salman2020Do_R18 | ResNet-18 | CNN | 52,92 / 25,32 | 46.836.793 | Drive | Res256Crop224 |
| Salman2020Do_50_2 | WRN-50-2 | CNN | 68,46 / 38,14 | 275.912.303 | Drive | Res256Crop224 |
| Chen2024Data_WRN_50_2 | WRN-50-2 | CNN | 68,76 / 40,60 | 275.913.601 | Drive | Res256Crop224 |
| Peng2023Robust | RaWRN-101-2 | CNN | 73,44 / 48,94 | 417.089.026 | Drive | Res256Crop224 |
| Liu2023Comprehensive_ConvNeXt-B | ConvNeXt-B | modern CNN | 76,02 / 55,82 | 354.496.687 | Drive | BicubicRes256Crop224 |
| Liu2023Comprehensive_ConvNeXt-L | ConvNeXt-L | modern CNN | 78,02 / 58,48 | 791.200.175 | Drive | BicubicRes256Crop224 |
| Singh2023Revisiting_ConvNeXt-T-ConvStem | ConvNeXt-T + ConvStem | modern CNN | 72,72 / 49,46 | 114.572.173 | Drive | BicubicRes256Crop224 |
| Singh2023Revisiting_ConvNeXt-S-ConvStem | ConvNeXt-S + ConvStem | modern CNN | 74,10 / 52,42 | 201.165.449 | Drive | BicubicRes256Crop224 |
| Singh2023Revisiting_ConvNeXt-B-ConvStem | ConvNeXt-B + ConvStem | modern CNN | 75,90 / 56,14 | 355.132.063 | Drive | BicubicRes256Crop224 |
| Singh2023Revisiting_ConvNeXt-L-ConvStem | ConvNeXt-L + ConvStem | modern CNN | 77,00 / 57,70 | 792.657.601 | Drive | BicubicRes256Crop224 |
| Amini2024MeanSparse_ConvNeXt-L | MeanSparse ConvNeXt-L | modern CNN, son işlem | 77,92 / 59,64 | ölçülmedi | Drive | BicubicRes256Crop224 |
| Mo2022When_ViT-B | ViT-B/16 | düz ViT | 68,38 / 34,40 | 346.330.174 | Drive | Res224 |
| Singh2023Revisiting_ViT-S-ConvStem | ViT-S + ConvStem | hibrit | 72,56 / 48,08 | 91.166.417 | Drive | BicubicRes256Crop224 |
| Singh2023Revisiting_ViT-B-ConvStem | ViT-B + ConvStem | hibrit | 76,30 / 54,66 | 348.642.911 | Drive | BicubicRes256Crop224 |
| Debenedetti2022Light_XCiT-S12 | XCiT-S12 | hibrit (konvolüsyonlu yama) | 72,34 / 41,78 | 105.172.083 | GitHub release | timm varsayılanı |
| Debenedetti2022Light_XCiT-M12 | XCiT-M12 | hibrit | 74,04 / 45,24 | 185.777.715 | GitHub release | timm varsayılanı |
| Debenedetti2022Light_XCiT-L12 | XCiT-L12 | hibrit | 73,76 / 47,60 | 415.372.403 | GitHub release | timm varsayılanı |
| Mo2022When_Swin-B | Swin-B | hiyerarşik dönüştürücü | 74,66 / 38,30 | 352.793.274 | Drive | Res224 |
| Liu2023Comprehensive_Swin-B | Swin-B | hiyerarşik dönüştürücü | 76,16 / 56,16 | 352.787.535 | Drive | BicubicRes256Crop224 |
| Liu2023Comprehensive_Swin-L | Swin-L | hiyerarşik dönüştürücü | 78,92 / 59,56 | 787.843.919 | Drive | BicubicRes256Crop224 |
| RodriguezMunoz2024Characterizing_Swin-B | Swin-B | hiyerarşik dönüştürücü | 77,76 / 51,56 | 352.793.946 | Drive | BicubicRes256Crop224 |
| RodriguezMunoz2024Characterizing_Swin-L | Swin-L | hiyerarşik dönüştürücü | ölçülmedi | ölçülmedi | Drive | BicubicRes256Crop224 |
| Xu2024MIMIR_Swin-B | Swin-B | hiyerarşik dönüştürücü | 76,62 / 55,90 | 352.773.354 | Drive | BicubicRes256Crop224 |
| Xu2024MIMIR_Swin-L | Swin-L | hiyerarşik dönüştürücü | ölçülmedi | ölçülmedi | Drive | BicubicRes256Crop224 |
| Amini2024MeanSparse_Swin-L | MeanSparse Swin-L | dönüştürücü, son işlem | ölçülmedi | ölçülmedi | Drive | BicubicRes256Crop224 |
| Bai2024MixedNUTS | ConvNeXtV2-L + Swin-L karışımı | topluluk, ek veri | 81,48 / 58,62 | iki dosya, ölçülmedi | Drive | BicubicRes256Crop224 |

Salman2020Do_R50 satırındaki boyut ilk HEAD denemesinde dosya adı `Salman2020Do_R50.pt` ile döndü; değer Wong2020Fast ile aynı bayt sayısını vermiştir (102.546.991), ResNet-50 için beklenen büyüklüktür ama iki dosyanın aynı boyutta olması tesadüf ya da aynı biçimli kayıt olabilir, indirmeden önce yeniden bakılmalıdır.

Seçim ölçütleri şunlardır: CNN, düz ViT, hiyerarşik dönüştürücü ve hibrit sınıflarının her biri temsil edilsin; en az iki aynı grup ve aynı tarifli CNN-dönüştürücü çifti olsun; bağımsız grup sayısı en az beş olsun; her dosya 1 GB altında, toplam 2 GB altında kalsın; büyük L modelleri (yaklaşık 790 MB, ileri geçişi B modelinin iki katından fazla) ve son işlemli ya da topluluk girdileri (MeanSparse, MixedNUTS) dışarıda kalsın, çünkü ikincileri gradyanı değiştirir ve beyaz kutu köşegenini anlamsızlaştırabilir. Bu ölçütlerle önerilen sekizli şudur.

| Takma ad önerisi | Model | Sınıf | Grup | Boyut (MB) | Neden |
|---|---|---|---|---|---|
| IN_R50 | Salman2020Do_R50 | CNN | MIT Madry | 102,5 | Klasik gürbüz CNN, Jiang ve Chen ile Awad'da da vekil |
| IN_R18 | Salman2020Do_R18 | CNN | MIT Madry | 46,8 | Makaledeki ResNet-18'in ImageNet karşılığı |
| IN_CNXB | Liu2023Comprehensive_ConvNeXt-B | modern CNN | Tsinghua ARES | 354,5 | Swin-B ile aynı grup, aynı AT çerçevesi |
| IN_SWINB | Liu2023Comprehensive_Swin-B | hiyerarşik dönüştürücü | Tsinghua ARES | 352,8 | ConvNeXt-B ile eşleşik, temiz ve AA doğrulukları neredeyse aynı (76,16/56,16 ile 76,02/55,82) |
| IN_VITB | Mo2022When_ViT-B | düz ViT | Mo ve ark. | 346,3 | Paneldeki tek düz yamalı ViT, makaledeki ViT-Tiny'nin akrabası |
| IN_VITS_CS | Singh2023Revisiting_ViT-S-ConvStem | hibrit | Tübingen | 91,2 | ConvNeXt-T-ConvStem ile aynı tarif, 300 epok |
| IN_CNXT_CS | Singh2023Revisiting_ConvNeXt-T-ConvStem | modern CNN | Tübingen | 114,6 | ViT-S-ConvStem ile eşleşik (72,56/48,08 ile 72,72/49,46) |
| IN_XCIT | Debenedetti2022Light_XCiT-S12 | hibrit | EPFL | 105,2 | CIFAR-10 havuzundaki XCiT'in ImageNet kardeşi |

Toplam 1513,9 MB'tır. İsteğe bağlı olarak Singh'in yama gövdeli ViT-S (69,2/44,0) ve ConvNeXt-T (72,4/48,6) modelleri eklenirse ImageNet ölçeğinde aynı tarifli bir mimari × gövde 2x2'si oluşur; bu iki model RobustBench'te yoktur, Singh deposunun kendi bağlantısından iner ve önceki rapora göre README dört yama gövdeli model için aynı bağlantıyı vermektedir (`01_oneri_P2_dis_gecerlilik.md` satır 63); bu yüzden bu rapor onları çekirdeğe almaz. Mo ViT-B'nin AA doğruluğu (34,40) panelin geri kalanından belirgin düşüktür; ViT'nin "zayıf kaynak" görünmesi bu modelde gürbüzlük düzeyiyle karışabilir (Springer ve ark., Zhang ve ark. çerçevesi; `02_literatur.md`). Bunu karşılamak için çözümlemede w ile birlikte AA doğruluğu da betimsel olarak verilmelidir.

## 4. Imagenette

### 4.1 Sürümler, boyutlar, lisans

fastai/imagenette README'si üç sürüm verir ve "The '320 px' and '160 px' versions have their shortest side resized to that size, with their aspect ratio maintained" der. İndirme adresleri ve HEAD ile ölçülen boyutlar şöyledir: `imagenette2.tgz` 1.557.161.267 bayt, `imagenette2-320.tgz` 341.663.724 bayt, `imagenette2-160.tgz` 99.003.388 bayt (s3.amazonaws.com/fast-ai-imageclas). Depo lisansı Apache-2.0'dır; README görüntü verisi için ayrı bir lisans yazmaz, görüntüler ImageNet'ten alındığı için ImageNet kullanım koşulları geçerli sayılmalıdır (bu çıkarım doğrulanmadı). README'de görüntü sayısı ve atıf biçimi yoktur. torchvision 0.17 sonrası `torchvision.datasets.Imagenette` sınıfı `split` için "train" ve "val", `size` için "full", "320px" ve "160px" seçeneklerini taşır (docs.pytorch.org).

### 4.2 Doğrulama kümesinin kökeni: olumsuz bulgu

Görev metnindeki "Imagenette val görüntüleri ImageNet val'den geldiği için modeller bunları görmüş olmaz" varsayımı yanlıştır. README "The Imagenette and Imagewoof datasets changed on Dec 6th 2019. They now have a 70/30 train/valid split" der. Bunu dosya düzeyinde doğrulamak için Hugging Face'teki `zeno-ml/imagenette` alanının `imagenette/val/<wnid>` ağacı Hugging Face API'siyle (yalnız dosya adları, görüntü indirilmeden) sayılmıştır. On sınıfta toplam 3925 dosya vardır; bunların 134'ü `ILSVRC2012_val_` önekiyle ImageNet doğrulama kümesinden, 3791'i (%96,6) `n01440764_XXXX.JPEG` biçimindeki ImageNet eğitim kümesi adlandırmasıyla gelmektedir. Sınıf başına ImageNet doğrulama kökenli dosya sayısı tench 10, English springer 15, cassette player 11, chain saw 14, church 19, French horn 12, garbage truck 12, gas pump 14, golf ball 13, parachute 14'tür. Ayna imagenette2'nin kendisi değil üçüncü taraf bir kopyadır; toplamın 3925 olması görev metnindeki sayıyla örtüşür ama resmi kaynaktan doğrulanmamıştır, indirme sonrası aynı sayım `find val -name 'ILSVRC2012_val_*' | wc -l` ile yinelenmelidir. Noisy Imagenette yazısı (tmabraham.github.io, 02.03.2021) `train/` altında `ILSVRC2012_val_` adlı bir dosya gösterdiğinden ImageNet doğrulama görüntülerinin bir kısmı Imagenette'in eğitim klasöründedir; on sınıfın ImageNet doğrulama görüntüsü en çok 500'dür (sınıf başına 50).

Sonuç şudur: Imagenette2 doğrulama kümesinin neredeyse tamamı RobustBench ImageNet modellerinin eğitim görüntüsüdür. Gürbüz modellerde eğitim ve sınama arasında gürbüz doğruluk farkı bulunduğundan w (beyaz kutu kırılganlığı) eğitim görüntüsünde sistematik olarak düşük ölçülür ve bu sapma modelin ne kadar ezberlediğine göre değişir; bu da modeller arası w karşılaştırmasını ve dolayısıyla ayrışımı bozar. Imagenette yalnız içindeki ImageNet doğrulama görüntüleriyle (en çok yaklaşık 500) kullanılabilir.

### 4.3 Önerilen alternatif: ImageNetV2 MatchedFrequency

Recht ve ark. ("Do ImageNet Classifiers Generalize to ImageNet?", arXiv 1902.10811, doğrulandı) ImageNet protokolüyle Flickr'dan yeniden toplanmış üç sınama kümesi yayımlamıştır; depo README'si "ImageNetV2 contains three test sets with 10,000 new images each" der ve yeni küme ile özgün ImageNet arasında yakın kopya denetimi yapıldığını yazar (github.com/modestyachts/ImageNetV2). Kod MIT lisanslıdır, README lisansın "does _not_ apply to the actual image data" olduğunu, görüntülerin Flickr lisans bilgisi taşıdığını ve "can be used the same way as the original ImageNet dataset" olduğunu söyler. Hugging Face `vaishaal/ImageNetV2` kopyası kapısızdır (kartta kapı uyarısı yok, lisans alanı "mit"); `imagenetv2-matched-frequency.tar.gz` HEAD ile 1.264.079.360 bayttır. Klasör adları 0-999 sınıf indeksidir (HF önizlemesinde `.../imagenetv2-matched-frequency-format-val/986/...`; indeks eşlemesi indirme sonrası denetlenmeli).

Bu küme F1 için Imagenette'ten üç bakımdan üstündür: görüntüler modellerin eğitim kümesinde değildir, 1000 sınıfın tam logiti kullanılır ve w RobustBench'in AA sayılarıyla doğrudan karşılaştırılabilir kalır (logit kısıtlama yok), sınıf başına 10 görüntü sınıf dengesi verir. Bedeli, ImageNetV2'de doğruluğun özgün doğrulama kümesine göre düşük olmasıdır (Recht ve ark.'nın ana bulgusu); hedef-doğru koşullama bunu payda düzeyinde zaten yönetir. Önerilen örneklem sınıf başına 5 görüntüdür (n = 5000, RobustBench ImageNet değerlendirmesiyle aynı büyüklük); temiz doğruluk %65-75 aralığında kalırsa hedef başına yaklaşık 3300-3700 hedef-doğru görüntü kalır.

### 4.4 On sınıfın ImageNet indeksleri

timm `ImageNetInfo` (konteyner, timm 1.0.27; eşanlam kümesi listesi alfabetik sıralı, denetlendi) ile: n01440764 tench 0; n02102040 English springer 217; n02979186 cassette player 482; n03000684 chain saw 491; n03028079 church 497; n03394916 French horn 566; n03417042 garbage truck 569; n03425413 gas pump 571; n03445777 golf ball 574; n03888257 parachute 701.

## 5. Logitleri sınıf alt kümesine kısıtlamanın emsali

ImageNet-R değerlendirmesi 1000 sınıflı modelin çıktısını 200 sınıfa maskeleyerek tahmin üretir; `hendrycks/imagenet-r` deposundaki `eval.py` dosyasında `imagenet_r_mask = [wnid in imagenet_r_wnids for wnid in all_wnids]` ve `output = net(data)[:,imagenet_r_mask]` satırları vardır (Hendrycks ve ark., arXiv 2006.16241, doğrulandı). ImageNet-A (arXiv 1907.07174, doğrulandı) aynı 200 sınıflı düzeni kullanır; ancak depo README'sinde bu kısıtlama cümlesi bulunamamıştır (doğrulanmadı). Xiao ve ark.'nın ImageNet-9 arka plan çalışması (arXiv 2006.09994, doğrulandı) 1000 sınıflı modelleri dokuz üst sınıfa eşleyerek değerlendirir (eşleme ayrıntısı doğrulanmadı). Tsipras ve ark.'nın Restricted ImageNet'i (arXiv 1805.12152, doğrulandı) ise modeli alt kümede eğitir, emsal değildir. Bu tarama çekişmeli saldırıda ve transfer ölçümünde logit kısıtlamasını kullanan bir çalışma bulmamıştır. Kısıtlama doğruluk ölçümü için yerleşik bir uygulamadır, ama saldırıyı değiştirir: on sınıflı çapraz entropi altında PGD saldırganın 999 yerine 9 sınıfa itmesi gerekir, w ve transfer oranları 1000 sınıflı değerlerle karşılaştırılamaz ve RobustBench sayılarıyla tutarlılık denetimi yapılamaz. ImageNetV2 bu sorunu tümüyle ortadan kaldırdığı için bu rapor kısıtlamayı önermez.

## 6. RobustBench CIFAR-100 L∞ (ε = 8/255) listesi ve F2 seçimi

Konteynerdeki listede 38 girdi vardır. Dönüştürücü olarak yalnız Debenedetti XCiT S/M/L vardır ve üçü de RobustBench'te `additional_data: true` (ImageNet ön eğitimi) olarak işaretlidir. Ölçülen ve meta verisi alınan girdiler aşağıdadır; diğerleri (Gowal2020Uncovering, Cui2020Learnable LBGAT ailesi, Chen2020Efficient, Wu2020Adversarial, Sitawarin2020Improving, Rebuffi2021 70-16 ve 28-10, Addepalli2021Towards_WRN34, Pang2022 WRN70-16, Jia2022LAS-AT 34-20, Wang2023Better 70-16, Bai2023Improving, Cui2023Decoupled 34-10, Bai2024MixedNUTS, Amini2024MeanSparse) panel için gereksiz büyük ya da topluluk olduğundan ölçülmemiştir.

| Model | Mimari | Temiz / AA (%) | Ek veri | Dosya (bayt) |
|---|---|---|---|---|
| Rice2020Overfitting | PreActResNet-18 | 53,83 / 18,95 | yok | 44.922.584 |
| Rebuffi2021Fixing_R18_ddpm | PreActResNet-18 | 56,87 / 28,50 | yok (DDPM üretimi) | 50.441.195 |
| Rade2021Helper_R18_ddpm | PreActResNet-18 | 61,50 / 28,88 | yok (DDPM üretimi) | 50.445.746 |
| Addepalli2021Towards_PARN18 | PreActResNet-18 | 62,02 / 27,14 | yok | 44.943.410 |
| Addepalli2022Efficient_RN18 | ResNet-18 | 65,45 / 27,67 | yok | 44.963.257 |
| Sehwag2021Proxy | WRN-34-10 | 65,93 / 31,15 | yok | 185.019.203 |
| Chen2024Data_WRN_34_10 | WRN-34-10 | 64,32 / 31,13 | yok | 185.025.603 |
| Addepalli2022Efficient_WRN_34_10 | WRN-34-10 | 68,75 / 31,85 | yok | 185.033.958 |
| Jia2022LAS-AT_34_10 | WRN-34-10 | 64,89 / 30,77 | yok | ölçülmedi |
| Chen2021LTD_WRN34_10 | WRN-34-10 | 64,07 / 30,59 | yok | ölçülmedi |
| Cui2020Learnable_34_10_LBGAT0 | WRN-34-10 | 70,25 / 27,16 | yok | ölçülmedi |
| Pang2022Robustness_WRN28_10 | WRN-28-10 | 63,66 / 31,08 | yok | diskte (146.270.845) |
| Rebuffi2021Fixing_28_10_cutmix_ddpm | WRN-28-10 | 62,41 / 32,06 | yok | ölçülmedi |
| Cui2023Decoupled_WRN-28-10 | WRN-28-10 | 73,85 / 39,18 | yok | 146.269.938 |
| Wang2023Better_WRN-28-10 | WRN-28-10 | 72,58 / 38,83 | yok (difüzyon üretimi) | 146.269.624 |
| Hendrycks2019Using | WRN-28-10 | 59,23 / 28,42 | var (ImageNet ön eğitimi) | 146.249.648 |
| Gowal2020Uncovering_extra | WRN-70-16 | 69,15 / 36,88 | var | 1.067.932.383 |
| Debenedetti2022Light_XCiT-S12 | XCiT-S12 | 67,34 / 32,19 | var (ImageNet ön eğitimi) | 103.786.099 (GitHub release) |
| Debenedetti2022Light_XCiT-M12 | XCiT-M12 | 69,21 / 34,21 | var | ölçülmedi |
| Debenedetti2022Light_XCiT-L12 | XCiT-L12 | 70,76 / 35,08 | var | ölçülmedi |

Önerilen F2 eki beş modeldir: Rice2020Overfitting (zayıf, klasik PGD-AT PreActResNet-18; ölçeğin alt ucu), Addepalli2022Efficient_RN18 (makaledeki ResNet-18 ile aynı mimari, başka grup), Sehwag2021Proxy (WRN-34-10, orta), Hendrycks2019Using (ImageNet ön eğitimli WRN-28-10) ve Debenedetti2022Light_XCiT-S12 (ImageNet ön eğitimli hibrit dönüştürücü). Toplam 524.940.791 bayt (yaklaşık 525 MB), Gowal2020Uncovering_extra 1 GB'ı aştığı için dışarıdadır. Diskteki Pang2022 ve mevcut C1 CIFAR-100 ResNet-18 ile ViT-Tiny AT modelleriyle (tohum 1001-1003 ve 2001-2003) birlikte panel tohum başına sekiz modeldir; ön kayıttaki "panel en az 5 üye" koşulu (B2 için) burada ViT'nin kendisi ve ResNet çıkarıldıktan sonra altı üyeyle sağlanır. Hendrycks2019Using ile XCiT'in ikisinin de ImageNet ön eğitimli olması, XCiT'in kaynak davranışı ViT-Tiny'den farklı çıkarsa bunun dönüştürücü olmaktan mı ön eğitimden mi geldiğine panel düzeyinde kaba bir karşıt sağlar; tek modelle yapılan bu karşılaştırma çıkarım değil betimdir.

F2'nin bilinen karıştırıcısı ViT-Tiny'nin CIFAR-100'deki düşük temiz doğruluğudur: C1 sınama temiz doğrulukları ResNet-18 için 63,86, ViT-Tiny için 43,17'dir (`results/C1_REFERANS_FOYU.md` satır 229; kaynak `results/q1/e1_cifar100_summary.json`). Panelin geri kalanı 53,83-67,34 aralığındadır; ViT'nin w'su ve hedef-doğru paydası bu yüzden diğerlerinden farklı bir alt kümeye dayanır. Masa bulgusunda CIFAR-100 potansiyel payı 0,283 (SD 0,087), CIFAR-10 seçilen kontrol noktasında 0,541 (SD 0,029) bulunmuştur (`04_masa_cozumlemeleri.md` §4(4); MASA `4_potansiyel_payi.ozet`). F2'nin sorusu bu düşük payın yalnız üç modelli matrisin bir yapısı mı, yoksa panel genişleyince de süren bir özellik mi olduğudur.

## 7. Üçüncü öneri: CIFAR-10 havuzunda ε süpürmesi

Önerilen tek ek deney, CIFAR-10 havuzundaki yedi AT modelinin (ResNet18_AT_s1001, ViT_Tiny_AT_s2001, Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Debenedetti2022Light_XCiT-S12, Gowal2020Uncovering_28_10_extra) 7x7 hedef-doğru matrisinin ε ∈ {2, 4, 6, 12}/255 için yeniden ölçülmesidir; ε = 8/255 mevcuttur (`results/q1/havuz_cifar10`). Hiçbir indirme gerekmez, bütün modeller diskte ya da `models/robustbench_zoo/cifar10/Linf` altındadır.

Gerekçe masa çözümlemesinin en ciddi bulgusudur: ViT'nin yönlü terimi ρ log ölçekte +0,043, logit ölçekte −0,265'tir ve ρ_V − ρ_R farkı iki ölçek arasında işaret değiştirir (`04_masa_cozumlemeleri.md` §4(1); MASA `1_havuz_model_tablosu`); Hodge düzeyinde de r_RV logitte 0,006'ya iner ve potansiyel farkı işaret değiştirir (§4(2)). Ön kayıt logiti yalnız duyarlılık sayar, ama hakem "yönlü terimin işareti ölçek seçimine bağlıysa hangi ölçek doğrudur" diye soracaktır. ε süpürmesi bu soruyu veriye bırakır: çarpımsal model (T_ij = w_j τ̄_ij e^{r_ij/2}) bir ölçekte doğruysa, r_ij çifte ait bir özellik olarak ε değişirken o ölçekte sabit kalmalı, yanlış ölçekte ise w'nin ε ile değişmesiyle sistematik olarak kaymalıdır. Ölçülecek nicelik her çift ve ölçek için r_ij(ε)'nin ε üzerindeki eğimi ve ε içi görüntü bootstrap gürültüsüne oranıdır; ikincil olarak ViT kaynak açığının simetrik oranı q'nun ε boyunca kararlılığı. Bu, ön kayıttaki öngörüleri değiştirmez, ölçek seçimi için önceden yazılmış bir ölçüt üretir. ε ile transfer ilişkisini inceleyen çalışmalar vardır (örneğin Zhao ve ark., arXiv 2310.11850, kaynakçada), ama ε'yu bir ölçek değişmezliği sınaması olarak kullanan bir çalışma bu taramada bulunamamıştır (yalnız iki sorguyla; yenilik iddiası olarak kullanılmamalı).

İkinci aday olarak değerlendirilen ama önerilmeyen ekleme, F1 panelinin mimarilerinin standart eğitimli timm sürümleriyle (rejim karşıtlığı) ölçülmesidir. Standart modellerde ε = 4/255 PGD-10 beyaz kutu başarısı %100'e yakın olacağından log w sıfıra çöker ve ayrışım yalnız τ̄ ile r'ye indirgenir; Mahmood verisinde kurulamayan karşılaştırmayı kursa da yaklaşık 1 GB ek indirme ister ve manşetten uzaklaşır.

## 8. Uygulama notları

Kod tarafında üç değişiklik gerekir; hepsi `kod-mimar` işidir ve bu ajan dosyalara dokunmamıştır. Birincisi, `experiments/c1_c3_transfer_matrix.py` ε'u sabit tutar (satır 54, `EPS = 8 / 255`) ve `--eps` bayrağı yoktur; ε süpürmesi ve ImageNet (4/255, α = 1/255) için bayrak eklenmelidir. İkincisi ve daha önemlisi, `--cache-adv` önbellek adı `f"{src}__{args.attack}_{args.norm}_s{atk_steps}_n{args.n_samples}_seed{args.seed}_{args.dataset}"` biçimindedir (satır 369-370) ve ε içermez; ε eklenmeden önbellekle farklı ε koşulursa 8/255'lik örnekler sessizce yeniden kullanılır. Üçüncüsü, `--dataset` seçenekleri ImageNet içermez; ImageNetV2 için 224 merkez kırpmalı tek bir ortak tensör hattı (Resize 256 bilinear, CenterCrop 224, [0,1] aralığı) bir kez üretilmeli ve her modele aynı piksel uzayında verilmelidir, çünkü transferde pertürbasyon ortak uzayda tanımlanmalıdır. RobustBench modelleri normalizasyonu kendi içinde taşır, ama önerilen önişlemeleri farklıdır (Res256Crop224, BicubicRes256Crop224, Res224; Wong2020Fast için Crop288). Ortak hatta her modelin temiz doğruluğu RobustBench değerinden birkaç puan sapabilir; bu yüzden metindeki temiz ve w değerleri kendi hattımızda ölçülenler olmalıdır. ImageNet'te önbellek görüntü başına 3x224x224 float32 (602 KB) tutar; 5000 görüntü ve sekiz kaynakta yaklaşık 24 GB'tır. Önbellek yerine sekiz modelin birlikte GPU'da tutulduğu ve her kaynak grubunun hemen bütün hedeflere verildiği akış önerilir (ağırlıklar toplam yaklaşık 1,5 GB; 32 GB VRAM'e sığar). Örnek bazlı npz biçimi korunursa `q1_konsey_ayrisim.py --mod masa` değiştirilmeden kullanılabilir.

GPU süresi kestirimdir, depoda ImageNet süre kaydı yoktur. Sekiz modelin 224 piksel ileri geçiş maliyeti toplamı yaklaşık 69 GFLOP'tur (R50 4,1; R18 1,8; ConvNeXt-B 15,4; Swin-B 15,4; ViT-B 17,6; ViT-S-ConvStem, ConvNeXt-T-ConvStem ve XCiT-S12 4,5-5 civarı; değerler model kartlarından bilinen büyüklüklerdir, bu oturumda doğrulanmadı). PGD-10 yaklaşık 30 ileri geçiş eşdeğeridir; çapraz değerlendirme ve temiz geçişle görüntü başına yaklaşık 2,7 TFLOP, 5000 görüntüde 13,5 PFLOP eder. RTX 5090'da %20-40 verimle bu 15-40 dakikadır; F1 için 1 GPU-saat güvenli bütçedir ve 200 görüntülük bir pilotla ayarlanmalıdır. F2 (CIFAR-100, sekiz kaynak, n = 10000) ve ε süpürmesi (yedi kaynak, dört ε, n = 10000) 32 piksel olduğundan her biri 0,5 GPU-saatin altında kalmalıdır. Toplam yaklaşık 2 GPU-saattir.

Zamanlama kısıtı açıktır: ON_KAYIT §3, B3'ün 80 epoklu tavanının boş GPU'da ölçülmüş pilot süresine (W(80) = 20,47 sa) dayandığını ve paylaşımda sürenin yaklaşık iki katına çıkabileceğini yazar. F1, F2 ve ε süpürmesi B3 zinciri bittikten sonra, ya da B2 ile B3 arasında boşluk varsa o boşlukta koşmalıdır. Ön kayıt donmuştur ve değiştirilemez; bu üç iş ON_KAYIT'ın kapsamında değildir. Koşudan önce ayrı bir ek ön kayıt dosyası (örneğin `raporlar/konsey_2026-10-29/ON_KAYIT_EK_F1F2E.md`) yazılıp yerel olarak kaydedilirse sonuçlar "önceden kaydedilmiş keşifsel çözümleme" olarak raporlanabilir; yazılmazsa yalnız keşifsel etiketiyle. Bu rapor öngörü yazmaz; o fable'ın kararıdır.

## 9. Riskler

1. Imagenette sızıntısı: doğrulama kümesinin %96,6'sı ImageNet eğitim görüntüsüdür (Bölüm 4.2). F1 Imagenette doğrulamasıyla koşulursa w ve ayrışım sistematik olarak sapar.
2. K4 yorumu: ImageNetV2 ImageNet değildir ama ImageNet protokolüyle toplanmış 1,26 GB'lık bir kümedir; fable K4'ü buna da uyguluyorsa F1 düşer ve Imagenette'in yaklaşık 500 ImageNet doğrulama görüntüsü 10 sınıflı logitle tek seçenek kalır; bu hem küçük örneklem (hedef başına yaklaşık 350-400 hedef-doğru görüntü) hem emsalsiz saldırı kısıtlaması demektir ve önerilmez.
3. Başlatma ve gürbüzlük karışıklığı: F1 panelinde başlatma kontrol edilmez (Salman sıfırdan, Singh temiz modelden, Mo kısa AT ile ön eğitimli, Liu ve Debenedetti doğrulanmadı) ve tek düz ViT (Mo ViT-B, AA 34,40) panelin en az gürbüz ikinci modelidir. "ViT zayıf kaynaktır" okuması bu modelde gürbüzlük düzeyiyle karışır.
4. Önişleme farkları: modeller ortak 224 hattıyla beslenecek; Wong2020Fast 288 piksel ister ve bu yüzden seçilmemiştir, Mo modelleri Res224 kullanır. Temiz doğrulukların kendi hattımızda yeniden ölçülmesi zorunludur.
5. Önbellek adında ε yok (`c1_c3_transfer_matrix.py` satır 369-370); düzeltilmeden ε süpürmesi önbellekle koşulursa sessiz hata üretir.
6. GPU çakışması: B3'ün tavanı boş GPU pilotuna dayanır; ek işler B3 ile eşzamanlı koşarsa B3 süresi uzar.
7. Lisans: ImageNetV2 görüntüleri Flickr lisanslıdır, ImageNet gibi araştırma amaçlı kullanılır; Imagenette görüntüleri ImageNet'tendir; Singh ve Liu depolarında lisans görülmedi (Singh README'sinde lisans bölümü yok). Makalede yalnız türetilmiş sayılar yayımlanır, görüntü yeniden dağıtılmaz.
8. Google Drive kotası: 20 ImageNet ve 32 CIFAR-100 ağırlığından 26'sı Drive'dan gdown ile iner; Drive indirme kotası dolarsa indirme geçici olarak başarısız olabilir (genel bilgi, bu oturumda gözlenmedi).
9. ViT-Tiny'nin CIFAR-100 temiz doğruluğu (43,17) panelin altında; F2'de w farkı doğruluk farkıyla karışır.
10. Yenilik: Liu ve ark. (2302.14301) ile Awad ve ark. (2512.02830) ImageNet'te gürbüz modeller arası transfer ölçmüştür; F1 metni "ilk" iddiası taşımamalı, ayrışımın yinelenmesi olarak yazılmalıdır.

## 10. Kaynaklar

arXiv kimlikleri 30.10.2026'da arXiv özet sayfalarının meta etiketlerinden doğrulanmıştır; yayın yerleri arXiv yorum alanından ya da RobustBench `model_info` dosyasından alınmıştır.

- Liu, C. ve ark., A Comprehensive Study on Robustness of Image Classification Models: Benchmarking and Rethinking, arXiv 2302.14301 (DOI 10.48550/arXiv.2302.14301).
- Awad ve ark., Defense That Attacks: How Robust Models Become Better Attackers, arXiv 2512.02830.
- Sitawarin, C. ve ark., PubDef: Defending Against Transfer Attacks From Public Models, arXiv 2310.17645, ICLR 2024.
- Jiang ve Chen, arXiv 2606.22516 (önceki tarama).
- Shao, R. ve ark., On the Adversarial Robustness of Vision Transformers, arXiv 2103.15670.
- Mahmood, K., Mahmood, R., van Dijk, M., On the Robustness of Vision Transformers to Adversarial Examples, arXiv 2104.02610, DOI 10.1109/ICCV48922.2021.00774.
- Naseer, M. ve ark., On Improving Adversarial Transferability of Vision Transformers, arXiv 2106.04169.
- Wei, Z. ve ark., Towards Transferable Adversarial Attacks on Vision Transformers, arXiv 2109.04176.
- Bhojanapalli, S. ve ark., Understanding Robustness of Transformers for Image Classification, arXiv 2103.14586.
- Benz, P. ve ark., Adversarial Robustness Comparison of Vision Transformer and MLP-Mixer to CNNs, arXiv 2110.02797.
- Bai, Y. ve ark., Are Transformers More Robust Than CNNs?, arXiv 2111.05464.
- Singh, N. D., Croce, F., Hein, M., Revisiting Adversarial Training for ImageNet: Architectures, Training and Generalization across Threat Models, arXiv 2303.01870; depo github.com/nmndeep/revisiting-at.
- Mo, Y. ve ark., When Adversarial Training Meets Vision Transformers: Recipes from Training to Architecture, arXiv 2210.07540.
- Debenedetti, E. ve ark., A Light Recipe to Train Robust Vision Transformers, arXiv 2209.07399, SaTML 2023.
- Salman, H. ve ark., Do Adversarially Robust ImageNet Models Transfer Better?, arXiv 2007.08489.
- Paul, S., Chen, P.-Y., Vision Transformers are Robust Learners, arXiv 2105.07581 (bağlam; içerik doğrulanmadı).
- Guesmi ve ark., TESSER, arXiv 2505.19613 (arama özeti; doğrulanmadı).
- Recht, B. ve ark., Do ImageNet Classifiers Generalize to ImageNet?, arXiv 1902.10811; github.com/modestyachts/ImageNetV2; huggingface.co/datasets/vaishaal/ImageNetV2.
- Hendrycks, D. ve ark., The Many Faces of Robustness, arXiv 2006.16241; github.com/hendrycks/imagenet-r (`eval.py`).
- Hendrycks, D. ve ark., Natural Adversarial Examples, arXiv 1907.07174.
- Xiao, K. ve ark., Noise or Signal: The Role of Image Backgrounds in Object Recognition, arXiv 2006.09994.
- Tsipras, D. ve ark., Robustness May Be at Odds with Accuracy, arXiv 1805.12152.
- fastai/imagenette, github.com/fastai/imagenette (Apache-2.0); Hugging Face ayna `zeno-ml/imagenette` (dosya adı sayımı).
- RobustBench, github.com/RobustBench/robustbench, `model_info/imagenet/Linf/*.json` ve `model_info/cifar100/Linf/*.json` (master dalı, 30.10.2026).
- Zhao, Z. ve ark., arXiv 2310.11850 (kaynakçada; ε karşılaştırması bağlamı).
