# Çürütme turu 1: iç geçerlilik, istatistik ve ölçüm (07.11.2026, ikinci tur)

Mercek: Q1 düzeyinde istatistik ve deney tasarımı hakemi. Hedef: IEEE Access gönderimi "Less a Weak Source than a Different One" (paper/manuscript, 31.10.2026 sürümü). Sayılar yalnız `results/C1_REFERANS_FOYU.md` (föy), `results/q1/` altındaki dondurulmuş çıktılar ve bu turda koşulan `results/q1/curutme_2026-11-07/*.json` dosyalarından alınmıştır. Bu turun bütün çözümlemeleri keşifsel ve ön kayıt dışıdır; dondurulmuş betik (`experiments/q1_konsey_ayrisim.py`, SHA-256 4bce2c98...) değiştirilmemiş, yalnız fonksiyonları içe aktarılmıştır ve her çıktının `meta.dondurulmus_betik_ayni` alanı `true` yazar. Bu sürüm, çürütücü raporundaki (`01_ic_gecerlilik_curutucu.md`) düzeltmeleri işler; nelerin değiştiği dosya sonundaki "İkinci turda değişenler" bölümündedir.

## Özet

Makalenin manşeti hedef-doğru protokolde ve log ölçekte kurulmuştur ve bu turda iki ölçüm duyarlılığına karşı kırılgan çıkmıştır. Dört oranın da aynı "iki model de temiz doğru" maskesinde hesaplandığı tutarlı her-ikisi-doğru protokolünde, CIFAR-10'da kaynak açığı yaklaşık iki katına çıkmakta (0,711 ile 0,767), simetrik bileşen küçülmeyip 0,368'den yaklaşık 0,42'ye büyümekte, ancak yönlü pay 0,02'den yaklaşık 0,31'e çıktığı için q 0,577'ye inmekte ve ρ(V-scr) +0,188 [0,166; 0,211] ile eşdeğerlik bandının dışına düşmektedir; yani bu protokolde ViT farklı olmakla kalmayıp yönlü olarak da zayıf bir kaynaktır ve başlığın "Less a Weak Source" kısmı doğrudan sorgulanır (`her_ikisi_tutarli.json`). Ölçek tarafında K-b'nin eşdeğerliği log-logit ailesinde yalnız κ ∈ [−0,20; 0,25] penceresinde tutmakta, makalenin Önerme 2'de öne çıkardığı h ölçeğinde ρ(V-scr) −0,316 olmaktadır; H3 ise κ ∈ [−0,7; 0,9] gibi geniş bir pencerede bant içinde kalır (`olcek.json`). Sıfırdan satırındaki benzemezlik temiz doğrulukla ayrıştırılamamaktadır: CNN'ler üzerinde kurulan σ-temiz doğruluk doğrusu, seçilen doğruya göre H1'in yaklaşık %44, %67 ya da %88'ini doğrulukla birlikte değişen pay olarak göstermektedir ve bu kestirimlerin hepsi dış değerlemedir (`ayrisim.json`). Mimari ailesi sorusunda kanıt karışıktır: V-scr ImageNet başlatmalı ViT'ye eşleşmiş ResNet'lerinden 0,29 ile 0,34 log birimi daha yakındır, ama V-IN de V-scr'ye CNN'lerden daha yakın değildir ve V-scr'nin σ'sı CNN dağılımının 4,8 standart sapma altındadır (`olcekli_etki.json`). Holm ailesinin 15 sınamaya genişletilmesi, Welch aralıkları, δ taraması ve tohum, görüntü ve panel bileşenlerini birlikte taşıyan belirsizlik hiçbir kayıtlı kararı değiştirmemektedir; makalenin istatistik iskeleti sağlamdır, zayıflığı ölçüm tanımında ve tasarımın kimlik gücündedir. On dokuz bulgunun on üçü yeni eğitim ya da yeni değerlendirme istemektedir; tam paket RTX 5090'da yaklaşık 297 GPU-saat, kabul için asgari sayılabilecek paket yaklaşık 58 GPU-saattir.

## Bulgular

### B1-01 (major) Manşet koşullama protokolüne bağlı: tutarlı her-ikisi-doğru protokolünde ViT yönlü olarak da zayıf bir kaynak çıkıyor

Makale bütün ayrışımı hedef-doğru orana dayandırır (03_methodology.tex:215). Bu protokolde T_Vc, V'nin temiz örnekte yanıldığı görüntüleri de içerir; CNN hedeflerinde bu marjinal alt küme ortalama 1517 görüntüdür ve ortak doğru küme 7061 olduğundan hedef-doğru paydanın yaklaşık %18'ini oluşturur (föy M8.5, 1211-1215; Tablo II). Makale bu marjinal görüntülerin ortak çözülenlerden üç ila dört kat daha kırılgan olduğunu ve her-ikisi-doğru protokolünde çift düzeyindeki yönlü farkın 3,91 puan arttığını kendisi raporlar (04_experiments.tex:540); CIFAR-100 için ön kayıtlı her-ikisi-doğru duyarlılığının üretilmediğini de yazar (04_experiments.tex:154; 05_discussion.tex:69). Eksik olan, bu protokolün ayrışımın kendisine, yani q, K-b ve H3'e ne yaptığıdır.

Bu turda her (i, j) çifti için T_ij, T_ji, w_i ve w_j aynı ortak maskede ve bölünmüş yarıyla yeniden hesaplandı (`results/q1/curutme_2026-11-07/her_ikisi_tutarli.json`). CIFAR-10'da kaynak açığı G tohum başına 0,711, 0,729 ve 0,767 olur (`cifar10.G`); hedef-doğru protokoldeki karşılıkları 0,391, 0,387 ve 0,390'dır (04_experiments.tex:141; föy M9.5). Simetrik bileşen (q × G) 0,423, 0,415 ve 0,435 ile hedef-doğrudaki 0,368, 0,360 ve 0,367'den büyüktür; yönlü bileşen ise 0,023 ile 0,028'den 0,288, 0,314 ve 0,332'ye çıkar. q'nun 0,936'dan `cifar10.q_ort` = 0,577'ye düşmesinin tamamı bu yönlü artıştan gelir. ρ(V-scr) `cifar10.K-b.ort` = +0,188, %90 aralık [0,166; 0,211], %95 aralık [0,155; 0,221], TOST p 0,996; bu, ön kaydın K-b çürütme ölçütünü (%95 aralık sıfırı dışlar ve |kestirim| > 0,10) karşılar. 2×2 ailesinde H1 −0,431 ve H2 +0,317 ile destek sürer; H3 `cifar10.B4.H3` = +0,100 [0,081; 0,119], TOST p 0,501 ile eşdeğerlik kurulamaz. CIFAR-100'de q 0,495, ρ(V-scr) +0,287 [0,235; 0,338]'dir. Doğru okuma "simetrik pay çöktü" değil, "bu protokolde ViT farklı olmanın yanında yönlü olarak da zayıf bir kaynaktır" okumasıdır; başlığın "Less a Weak Source" kısmını doğrudan hedef alan da budur.

Ön kayıtla ilişki açık yazılmalıdır. Ön kayıtlı her-ikisi-doğru duyarlılığı (S9-4) `src/analysis/protokoller.py:60` içindeki `both_correct = tc & sc` tanımına dayanır; köşegende kaynak ile hedef aynı olduğundan w hedef-doğru kalır. Bu uygulama, bu turdaki "yarı tutarlı" sürüme denktir ve orada ρ(V-scr) +0,492, H3 +0,244'tür (`ayrisim.json`, `e_her_ikisi_dogru.cifar10`). Ortak maskeli sürüm bu turun sapmasıdır: w'yi T ile aynı maskede hesaplar ve bu yüzden w çifte bağlı hale gelir, yani artık tek bir model niceliği değildir. Yarı tutarlı sürümün daha büyük ρ vermesinin maske uyuşmazlığından geldiği bir varsayımdır, gösterilmemiştir; iki sürüm de manşetle çelişir ve ılımlı olan ortak maskeli sürüm karşı sayı olarak kullanıldı.

> Hakem cümlesi: "Under the both-correct protocol the source gap nearly doubles and its directional part rises from 0.02 to about 0.31, so the symmetric share falls to 0.58, the ViT's directional term becomes +0.19 and H3 is no longer equivalent; the ViT is then a directionally weak source as well, and the headline is a property of the target-correct protocol."

Kapatan iş: analiz (GPU yok). Tutarlı ve ön kayıt tanımlı (yarı tutarlı) her-ikisi-doğru ayrışımları gövdeye duyarlılık satırı olarak girmeli, CIFAR-100 için kayıtlı S9-4 üretilmeli, w'nin çifte bağlı hale gelmesinin yorumu yazılmalı ve hedef-doğru protokolün neden kestirilmek istenen nicelik olduğu, yani kaynağın kendi temiz hatalarındaki örneklerin neden onun transfer kapasitesine sayılması gerektiği kuramsal olarak savunulmalıdır. Savunma kurulamazsa başlık ve manşet "hedef-doğru protokolde" kaydıyla daraltılmalıdır. Doğruluğu eşleşmiş hücre (B1-03) iki protokolü birbirine yaklaştıracağı için bu bulguyu dolaylı olarak da kapatır.

Kapatılmazsa düşecek cümle: main.tex:133 "On CIFAR-10, 0.936 [0.925, 0.948] of ViT-Tiny's panel source gap to ResNet-18 is symmetric, and the ViT's directional term ($+0.012$) is equivalent to zero within $\pm0.10$."; 01_introduction.tex:28 "On CIFAR-10 a share of $0.936$ of ViT-Tiny's panel source gap relative to ResNet-18 is symmetric, against one half for a pure source effect"; başlıktaki "Less a Weak Source" (main.tex:72).

### B1-02 (major) K-b'nin eşdeğerliği dar bir ölçek penceresinde; Önerme 2'nin h ölçeğiyle birincil ölçek arasında gerilim

Makale yönlülük iddiasını log ölçekle sınırlamıştır: özet "A small directional term holds only on CIFAR-10, the log scale and a CNN panel; on the logit scale it is strongly negative" der (main.tex:133) ve aynı kayıt 01_introduction.tex:42, 05_discussion.tex:19 ve 04_experiments.tex:144'te vardır. Bu bulgunun yeni payı iki noktadır. Birincisi pencerenin darlığıdır. f_κ(x) = log x − κ log(1 − x) ailesi (κ = 0 log, κ = 1 logit) κ ∈ [−1; 2] aralığında 0,05 adımla tarandı (`olcek.json`); κ = 0 satırı kayıtlı değerleri birebir verir (q 0,9363; ρ +0,0119; H1 −0,3643; H2 +0,2601; H3 +0,0034). ρ(V-scr) κ'ya karşı neredeyse doğrusaldır, `cifar10.rho_V_sifir_gecisi_kappa` = 0,038'de sıfırı keser ve %90 aralığı yalnız κ ∈ [−0,20; 0,25]'te ±0,10 bandında kalır. CIFAR-100'de sıfır geçişi 0,257'de, pencere [0,20; 0,30]'dadır; CIFAR-10'daki eşdeğerlik ile CIFAR-100'deki çürütme bu yüzden iki veri kümesinin penceresinin log ölçeğe göre farklı yerlere düşmesinden ibaret olabilir. Buna karşılık H3'ün %90 aralığı κ ∈ [−0,7; 0,9] gibi geniş bir pencerede bant içinde kalır (`H3_ci90_band_icinde_kappa_min/max`); "ölçek seçimi" itirazı yalnız K-b için geçerlidir. İkincisi Önerme 2 ile gerilimdir. Dördüncü katkı h = −log(1 − T) ölçeğini, protokol seçiminin yalnız hedef potansiyellerini kaydırdığı ölçek olarak öne çıkarır (01_introduction.tex:38). Bu ölçekte ρ(V-scr) `cifar10.h_olcegi.K-b.ort` = −0,316 [−0,327; −0,306], q 2,07, H3 −0,090 [−0,109; −0,071]; H1 −0,134 ile öngörülen −0,20 büyüklüğünün, H2 +0,094 ile öngörülen +0,10'un altına iner. Bandın ölçekler arasında aynı anlamı taşımadığı doğrudur, ama işaretin ve büyüklük sırasının değişmesi bu itirazla kapanmaz.

> Hakem cümlesi: "The equivalence of the ViT's directional term holds only for κ between −0.20 and 0.25 in a log-to-logit family, while H3 holds over a wide range; on the h scale that the authors single out as protocol-invariant, the directional term is −0.32 and H1 falls to −0.13, so the authors should explain why the protocol-invariant scale is not the primary one."

Kapatan iş: analiz (GPU yok). Ölçek ailesi taraması eke konmalı; K-b ile H3'ün ölçek duyarlılığının farklı olduğu yazılmalı; Önerme 2'nin h ölçeği ile birincil log ölçek arasındaki gerilim Tartışma'da açıklanmalı ya da yönlülük için ölçekten bağımsız bir özet (örneğin r'nin işaret tutarlılığı) önerilmeli.

Kapatılmazsa düşecek cümle: 04_experiments.tex:506 "The log scale is primary because the quasi-symmetry form $T_{ij} = w_j\simt_{ij}$ is additive on it and because the registration fixed it as primary before any of these runs." Bu cümle Önerme 2'nin h ölçeğini neden birincil yapmadığını açıklamadığı sürece eksik kalır.

### B1-03 (major) Sıfırdan satırındaki benzemezlik temiz doğrulukla ayrıştırılamıyor; doğruluğun payı %44 ile %88 arasında

V-scr'nin temiz doğruluğu 73,01 ile 74,10, öbür hücrelerin 83,39 ile 86,35'tir (föy 1505-1513). Makale bu karıştırıcıyı kabul eder (04_experiments.tex:245), ancak büyüklüğünü ölçmez; önceki panelin A3 açık işi de üretilmemiştir (birlesik.md:248). Bu turda yirmi modelli CIFAR-10 matrisinde σ, yalnız CNN modelleri üzerinden temiz doğruluğa regrese edildi (`ayrisim.json`, `f_sigma_temiz_dogruluk`). On dört CNN'in tamamıyla (temiz doğruluk 83,34 ile 89,69) eğim puan başına 0,020, r = 0,33 (p 0,26); V-scr tohumlarının artığı ortalama −0,203'tür, yani H1'in (−0,364) yaklaşık %44'ü doğrulukla birlikte değişen paydır. R224-scr'nin bu doğruya göre kendi artığı (−0,082) da hesaba katılırsa iki hücre arasında artık farkı −0,121 kalır ve pay yaklaşık %67'ye çıkar. Yalnız kendi eğittiğimiz yedi CNN'le (R32 ve R224) eğim 0,026, r = 0,93 ve V-scr'nin ortalama artığı −0,043'tür (`yalniz_kendi_CNN.V-scr_ort_artik`); bu doğruya göre pay yaklaşık %88'dir. Ancak bu yedi modelin temiz doğruluğu yalnız 85,11 ile 86,35 arasında, yani 1,24 puanlık bir aralıktadır, ikisi ImageNet başlatmalı R224-IN'dir ve V-scr için yaklaşık 12 puanlık bir dış değerleme yapılmaktadır. Üç kestirimin de dış değerleme olması ve birbirinden bu kadar uzak düşmesi, karıştırıcının payının eldeki veriyle belirlenemediğini gösterir; bulgunun kendisi bu belirsizliktir. V-IN'in artıkları −0,093 ve −0,169'dur (tüm CNN doğrusu); doğruluğu eşleşmiş ViT'de de bir benzemezlik kalır, ancak V-IN başlatma demetini taşır (B1-10).

> Hakem cümlesi: "The scratch-trained ViT is 12 points less accurate than every other cell; depending on the reference line, 44 to 88 percent of H1 moves with clean accuracy, and all of these estimates extrapolate far outside the accuracy range of the CNNs, so an accuracy-matched control is required before H1 can be read as an architecture effect."

Kapatan iş: eğitim. En ucuz ve en kesin kontrol, temiz aşaması kısaltılarak temiz doğruluğu yaklaşık 73,5'e indirilmiş üç R224-scr koşusudur (aşağı eşleştirme), ardından aynı AT tarifi. R224-scr'nin AT aşaması B3 defterinde ortalama 3,03 sa'dir (13126 ve 8685 s, föy M9.1); kısaltılmış temiz aşama 200 epokluk aşamanın (ortalama 1,06 sa) küçük bir kesridir, koşu başına yaklaşık 3,2 sa, üç koşu yaklaşık 10 sa. Yukarı eşleştirme için ViT-Tiny daha uzun temiz aşama ve güçlü veri artırmayla en az %83'e çıkarılmalıdır (önceki panelin A1'i); üç tohum, koşu başına yaklaşık 5 sa, 15 sa. İki matris turu yaklaşık 1 sa (B9'un 15 modelli matrisi 833 s, föy M13.3; yirmi modele ölçeklenince yaklaşık 0,4 sa). Toplam yaklaşık 26 GPU-saat. Ön kayıt eki önce dondurulmalıdır.

Kapatılmazsa düşecek cümle: 01_introduction.tex:32 "Trained from scratch on the same input pipeline, the ViT is less similar to the panel than the ResNet ($\Asig{scr} = -0.364$)"; başlıktaki "a Different One" (main.tex:72); 05_discussion.tex:19 "The dissimilarity is present when both architectures are trained from scratch on a matched pipeline".

### B1-04 (major) Mimari ailesi sorusunda kanıt karışık; ayrıştırıcı karşılaştırma için tek bir başka transformer var

K-c, ViT tohumlarının birbirine panelden daha çok benzediğini gösterir (Δseed +0,566, föy 1589) ve makale bunu "genel bir kaynak zayıflığı bu benzerliği de düşürürdü" diye okur (04_experiments.tex:147). Aynı tarifle eğitilmiş tohumların birbirine benzemesi her mimari için beklendiğinden (ResNet tohumları arası log τ̄ −0,489, föy 1595) aile sorusunu ayrıştıran karşılaştırma farklı başlatmalı ya da farklı tasarımlı bir dikkat modelidir. Matristeki değerler iki yöne birden işaret eder (`ayrisim.json`, `b_capraz_benzerlik`). Aile okumasını destekleyen yönde, V-scr ile V-IN arası log τ̄ −0,798'dir; V-scr'nin CNN'lerle benzerliği ise −1,085 (R224-IN), −1,084 (R32), −1,135 (R224-scr) ve −1,009 (panel ortalaması) olduğundan V-scr öbür ViT'ye eşleşmiş ResNet'lerinden 0,29 ile 0,34 log birimi daha yakındır. Ayrıca CNN'ler arası σ yayılımıyla ölçeklendiğinde V-IN de dağılımın dışındadır: on CNN biriminde (yedi panel üyesi ve kendi üç CNN hücremiz) σ'nın standart sapması 0,102 iken V-scr'nin z değeri −4,8, V-IN'inki −2,2'dir (`olcekli_etki.json`, B1-19). Özgül çözüm okumasını destekleyen yönde, V-IN'in V-scr'ye benzerliği (−0,798) kendi CNN'lerle benzerliğinden (−0,842 R224-scr, −0,787 R224-IN, −0,800 R32, −0,739 panel) büyük değildir; yani V-IN, sıfırdan ViT'ye CNN'lerden daha yakın durmaz. Matristeki tek başka dikkat modeli XCiT-S12 ise CNN dağılımının içindedir (z −0,45) ve V-scr ona CNN'lere olduğu kadar uzaktır (−1,084); ancak XCiT ImageNet ön eğitimlidir, konvolüsyon bileşenleri taşır ve panele en yakın modeldir, bu yüzden tek başına aile itirazını taşımaz. XCiT'e karşı yönlü terimin +0,20 olması makalede zaten yazılıdır (05_discussion.tex:69; 01_introduction.tex:42). Karışık kanıtın kaynağı, tasarımda ViT-Tiny dışında aynı tarifle eğitilmiş hiçbir transformer bulunmamasıdır.

> Hakem cümlesi: "The scratch ViT is closer to the ImageNet-initialized ViT than to the ResNets, which supports a family reading, but the ImageNet-initialized ViT is no closer to the scratch ViT than to the ResNets and the only other attention model in the matrix sits inside the CNN distribution, so without a second independently designed transformer trained under the same recipe, family dissimilarity cannot be separated from a solution specific to this ViT-Tiny."

Kapatan iş: eğitim. Aynı CIFAR tarifinde sıfırdan eğitilmiş iki bağımsız transformer tasarımı (DeiT-S ya da Swin-T) ve bir modern CNN (ConvNeXt-T), ikişer tohum, toplam altı koşu; aile benzemezliği varsa transformer-transformer τ̄ değerleri transformer-CNN değerlerinden yüksek çıkmalıdır. FLOP oranı R224'e göre ConvNeXt-T (konvolüsyon kökü) için 9,175/3,627 = 2,53, ViT-S için 9,237/3,627 = 2,55'tir (`raporlar/konsey_2026-10-29/_ek_flop_olcumu.json`); R224-scr koşusu 4,09 sa olduğundan (föy M9.1) koşu başına yaklaşık 10 sa, altı koşu 60 sa, matris 1 sa. Toplam yaklaşık 61 GPU-saat.

Kapatılmazsa düşecek cümle: 04_experiments.tex:147 "A general weakness of the ViT as a source would have lowered this within-family similarity as well." Bu cümle aile benzemezliği için değil, yalnız genel bir kaynak zayıflığına karşı kanıt olarak kalabilir; başlıktaki "a Different One" mimari ailesine değil bu ViT-Tiny çözümüne bağlanmalıdır.

### B1-07 (major) Kapasite ve hesap yükü denetlenmiyor

ViT-Tiny 5,53 milyon parametre ve 2,149 GFLOP, R224 11,18 milyon ve 3,627 GFLOP, R32 11,17 milyon ve 1,111 GFLOP taşır (`_ek_flop_olcumu.json`). Makale bunu "whole packages, patch stem, attention and parameter count together" diye kabul eder (01_introduction.tex:42), sınırlılık olarak yazar (05_discussion.tex:23) ve gelecek çalışma olarak ViT-Small ile ResNet-50 karşılaştırmasını önerir (05_discussion.tex:83); önceki konseyin R3 hakemi de bunu not etmiştir (03_hakem_R3_uygulanabilirlik.md:109). Yeni pay, kapasitenin B1-03'teki doğruluk karıştırıcısının olası bir kaynağı olmasıdır: daha küçük model daha düşük temiz doğruluk verir ve bu iki etki mevcut tasarımda aynı hücrede birleşir. Başlık ve Tartışma "different one" sözünü mimari düzeyinde kurduğu sürece Q1 hakemi kapasite eşleşmiş bir karşılaştırma isteyecektir.

> Hakem cümlesi: "ViT-Tiny has half the parameters of ResNet-18 and the lowest clean accuracy in the design, so the architecture contrast is also a capacity contrast; the capacity-matched design the authors list as future work (ViT-S against ResNet-50) is needed before the result can be attributed to the architecture family."

Kapatan iş: eğitim. ViT-S (22,78 milyon, 9,237 GFLOP) ile ResNet-50 (25,56 milyon, 8,178 GFLOP) 2×2, dört hücre, üçer tohum. FLOP oranı R224'e göre ResNet-50 için 2,25, ViT-S için 2,55, ortalama yaklaşık 2,4; B3'ün koşu başına ortalaması 17,79/6 = 2,97 sa (föy M9.1, 1470) olduğundan koşu başına yaklaşık 7,1 sa, 12 koşu 85,5 sa, iki matris 2 sa. Toplam yaklaşık 88 GPU-saat.

Kapatılmazsa düşecek cümle: main.tex:72 başlık ("a Different One"); 06_conclusion.tex:12 "Trained from scratch on a matched input pipeline and recipe, the ViT is less similar to the panel than the ResNet" cümlesi mimari ailesi genellemesi olarak okunamaz.

### B1-08 (major) Genelleme: tek 2×2 veri kümesi, CIFAR-100'de K-b çürümesi, ImageNet sıfırdan satırı belirsiz, tek AT tarifi

2×2 tasarım yalnız CIFAR-10'dadır. CIFAR-100 yinelemesinde K-b çürütülmüştür (+0,143, TOST p 0,953; föy 1839) ve tutarlı her-ikisi-doğru protokolünde CIFAR-100'de q 0,495'e iner (B1-01). ImageNetV2'de tek sıfırdan çift Δσ_scr,Liu = −0,055 [−0,137; +0,022] ile belirsizdir (föy M10.4, 1932, 1939) ve iki Singh çifti konvolüsyon köklü ViT'lerdir. Bütün modeller tek bir karışık kayıplı ince ayar tarifiyle eğitilmiştir (03_methodology.tex:78); TRADES, AWP, üretilmiş veriyle eğitim ya da transformer'a özgü tarifler yoktur. Birincil panelin yedi üyesinin dördü ResNet-18 türevidir ve hiçbiri transformer değildir (03_methodology.tex:189). Makale bu sınırların çoğunu yazar (06_conclusion.tex:14); Q1 hakemi ise CIFAR-10'daki tek bir 2×2'den ve ölçek, protokol ve veri kümesiyle işareti değişen bir yönlü terimden başlık düzeyinde bir genelleme kabul etmeyecektir.

> Hakem cümlesi: "The two-by-two design exists only on CIFAR-10 with two small models and one fine-tuning recipe, the directional equivalence fails on CIFAR-100 and the only scratch pair at ImageNet scale is inconclusive, so the claim should either be replicated on a second dataset and a modern recipe or be restricted to this setting in the title."

Kapatan iş: eğitim. En az CIFAR-100'de 2×2'nin yinelenmesi (C100 çifti zaten var; V-IN, R224-scr ve R224-IN üç hücre ikişer tohum: 6 koşu × 2,97 sa = 17,8 sa, matris 0,5 sa) ve CIFAR-10 çiftinin TRADES ile iki mimari × iki tohumla yeniden eğitilmesi (4 koşu × yaklaşık 3 sa = 12 sa). Toplam yaklaşık 30 GPU-saat. Üçüncü bir veri kümesi (Tiny-ImageNet ya da ImageNet-100) istenirse veri iki katı olduğundan koşu başına yaklaşık 6 sa, sekiz koşu 48 sa eklenir.

Kapatılmazsa düşecek cümle: main.tex:72 başlığın genelliği; 06_conclusion.tex:12 "Measured against a fixed panel of robust CNNs, with the vulnerability of each target taken out, most of ViT-Tiny's source gap on CIFAR-10 is symmetric" yalnız hedef-doğru protokol kaydıyla kalabilir.

### B1-09 (major) Tek saldırı gücü ve tek ε; saldırı tarafı zayıf bir alternatif kümeyle sınanmış

Ayrışımın bütün terimleri tek bir saldırı (PGD-10) ve tek bir ε (CIFAR'da 8/255) ile ölçülmüştür (03_methodology.tex:52, 66). q ve ρ'nun ε'a ve adım sayısına bağımlılığı bilinmemektedir. Saldırı tarafı sınaması MI-PGD ve uyarlanmış TGR ile yapılmış, TGR her ViT kaynağında PGD-10'dan 0,147 ile 0,218 log birimi kötü çıkmıştır (föy M9.6, 1648); bu, TGR'nin yayımlanmış amacının tersidir. Makale uyarlamanın doğrulanmadığını ve girdi çeşitlendirmeli ya da daha çok adımlı saldırıların koşulmadığını yazar (05_discussion.tex:69); önceki panelin A7 ve A8 işleri açıktır. Yeni pay, ε ve adım duyarlılığının ayrışım düzeyinde hiç üretilmemiş olması ve ucuzluğudur. Korunma oranı 0,960 (föy 1624) zayıf bir alternatif kümeye karşı ölçülmüştür.

> Hakem cümlesi: "All transfer matrices use a single ten-step attack at a single budget, and the only ViT-specific attack performs worse than PGD, so the retained fraction of 0.96 is measured against a weak alternative set; report the decomposition at ε of 4/255 and 16/255 and under input-diversity and more-step attacks."

Kapatan iş: veri (yeni eğitim yok). Yirmi modelli matrisin ε = 4/255 ve 16/255'te yeniden üretilmesi (iki tur, tur başına yaklaşık 0,5 sa), PGD-50 ve DI/TI ile kaynak saldırıları (kaynak üretimi yaklaşık beş kat, yaklaşık 2,5 sa) ve TGR'nin temiz ViT-Tiny'den CNN'e yayımlanmış yönü verdiğinin doğrulanması (0,5 sa). Toplam yaklaşık 4 GPU-saat.

Kapatılmazsa düşecek cümle: 01_introduction.tex:32 "a fraction of $0.960$ of the gap is retained"; 05_discussion.tex:21 "the gap between ResNet and ViT sources is retained under each source's best attack".

### B1-10 (major) Başlatma demeti iki mimaride aynı değil

V-IN `deit_tiny_patch16_224.fb_in1k`, R224-IN `resnet18.a1_in1k` ile başlatılmıştır (03_methodology.tex:56); bunlar iki farklı ImageNet tarifidir (DeiT ile "ResNet strikes back" A1) ve iki kontrol noktasının ImageNet top-1 doğruluğu kaydedilmemiştir (03_methodology.tex:300). Makale demetin ağırlık, kısa AdamW temiz aşaması ve normalizasyonu birlikte taşıdığını ve etkileşimden yalnız mimariden bağımsızsa düştüğünü yazar, ancak "The bundle is the same for both architectures" der (03_methodology.tex:96). Ön eğitim tarifleri farklı olduğundan demet iki mimaride aynı değildir; H2 (+0,260) mimari ile başlatma etkileşimini, ön eğitim tarifinin kalitesindeki farktan ayırmaz. Başlatmanın ViT'nin temiz doğruluğunu 73,53'ten 83,43'e, ResNet'inkini 85,73'ten 86,00'ya taşıması (föy 1496-1499) bu ayrımın neden önemli olduğunu gösterir, ancak H2'nin ne kadarının doğruluk kazancından geldiği bu turda ölçülmemiştir. Önceki konseyin R1 hakemi demet itirazını M2 olarak kaydetmiştir (03_hakem_R1_istatistik.md:38); yeni pay tarif farkıdır.

> Hakem cümlesi: "The ImageNet bundle is not the same for both architectures: the ViT starts from a DeiT checkpoint and the ResNet from an RSB-A1 checkpoint, with unrecorded top-1 accuracy, so the interaction H2 cannot be attributed to architecture by initialization rather than to the quality of two different pre-training recipes."

Kapatan iş: eğitim. Rastgele ağırlık ve ImageNet normalizasyonlu hücre (normalizasyonu ayırır; ViT ve ResNet ikişer tohum, sıfırdan 200 epokluk temiz aşama, koşu başına yaklaşık 4 sa, 16 sa) ve aynı tarif ailesinden ön eğitilmiş kontrol noktalarıyla IN hücrelerinin yinelenmesi (ikişer tohum; V-IN 2,65 ve R224-IN 2,16 sa/koşu, föy M9.1; 2 × 2,65 + 2 × 2,16 = 9,6, yaklaşık 10 sa). Toplam yaklaşık 26 GPU-saat.

Kapatılmazsa düşecek cümle: 03_methodology.tex:96 "The bundle is the same for both architectures"; 01_introduction.tex:32 "ImageNet initialization raises the ViT's panel similarity more than the ResNet's (interaction $\Isig = +0.260$)".

### B1-05 (minor) V-scr hücresi başka kampanyadan; kalan fark donanım ve kod tarihi

Bu itiraz önceki konseyin R1 hakeminin M3 bulgusunun tekrarıdır (03_hakem_R1_istatistik.md:39) ve makale kampanya ve tavan farkını açıklar (03_methodology.tex:96). Bu turda föyle yeniden denetlendiğinde tavan farkının fiilen etkisiz olduğu görüldü: V-scr'nin AT öğrenme oranı çizelgesi kosinüs, T_max 100'dür (föy 2450), B3 hücreleri de aynı kosinüs T_max 100 çizelgesiyle eğitilmiş ve 80 epokluk tavan yalnız `--stop-epoch` ile uygulanmıştır (föy M13.1, (c) tablosu); V-scr 45, 38 ve 39'da (föy M8.14, 1383-1390), B3 koşuları 36 ile 58 arasında durmuştur (föy M9.1). Dolayısıyla epok başına öğrenme oranı yörüngesi bütün hücrelerde aynıdır ve tavan hiçbir koşuda bağlayıcı olmamıştır. Çürütücünün "kosinüs tavanı her epoğu etkiler" gerekçesi bu yüzden uygulanmadı. Kalan ve yeni pay şudur: V-scr RTX 5060 Ti'de ve 77ae259 kod sürümüyle (Temmuz 2026), öbür hücreler RTX 5090'da eğitilmiştir (04z_computational.tex:15); föy M13.1 (d) tarif değerlerinin aynı olduğunu gösterir, ama donanım ve sürüm farkının sayısal etkisi sınanmamıştır ve bu fark V-scr hücresiyle tam örtüşür. Ayrıca V-scr'nin üç tohumu kayıttan önce görülmüştür (03_methodology.tex:298).

> Hakem cümlesi: "The scratch ViT cell alone was trained on a different GPU with an older code version and was seen before registration; even if recipes and schedules match, a re-run in the same chain would remove the only cell-aligned campaign difference."

Kapatan iş: eğitim (isteğe bağlı). V-scr'yi B3 zincirinde üç tohumla yeniden eğitmek (R224-scr ile aynı temiz komut, koşu başına yaklaşık 4 sa; föy M9.1 R224-scr 4,09 sa), matrisle yaklaşık 12,5 GPU-saat. Bu koşular B1-06'nın V-scr tohumlarını da karşılar.

Kapatılmazsa düşecek cümle: Doğrudan düşen bir cümle yok; 01_introduction.tex:19'daki örneklem dışı ayrımı ("Those for the new two-by-two cells ... are out of sample") V-scr için zaten yapılmıştır.

### B1-06 (minor) Yeni hücrelerde iki koşu; varyans kestirimleri tek serbestlik dereceli, kararlar değişmiyor

Üç yeni hücrede ikişer koşu vardır ve hücre içi varyans her hücrede tek serbestlik derecesiyle kestirilir. σ için hücre SD'leri V-scr 0,0075, V-IN 0,0526, R224-scr 0,0275, R224-IN 0,0100'dür (`cikarim.json`, `varyans_heterojenligi`); en büyük ve en küçük varyansın oranı 49,3, ρ için 126,8'dir. Bu oranlar bir ya da iki serbestlik dereceli kestirimlerin uçlarından geldiği için kendi başına homojenlik ihlalinin kanıtı değildir, ancak birleşik df = 5 aralıklarının bu varsayıma dayandığını gösterir. Welch serbestlik dereceleriyle Holm sonrası p'ler H1 0,027, H2 0,042, H3 0,026'dır (`welch_F_B4`); üç karar da sürer. Gözlenen ρ etkileşimi −0,134 [−0,180; −0,088] (Holm p 0,012; föy 2238), birleşik SD'den hesaplanan %80 güçlü en küçük etkinin (0,080; `guc_ve_MDE`) 1,7 katıdır ve mevcut tasarımda ayrışır. Hücre başına beş tohumla H2 için en küçük etki 0,170'ten 0,087'ye, ρ etkileşimi için 0,080'den 0,045'e iner. Bu kestirimler gözlenen etkiden değil birleşik SD'den türetildiği için post-hoc güç değildir.

> Hakem cümlesi: "Two runs per new cell give one-degree-of-freedom variance estimates; the decisions survive Welch intervals, but with a Welch–Holm p of 0.042 for H2 the margin is thin, and five seeds per cell would make the two-by-two inference credible."

Kapatan iş: eğitim. Üç yeni hücreye üçer tohum (hücre başına beş): 3 × (4,09 + 2,65 + 2,16) = 26,7 sa (föy M9.1), matris 0,5 sa; toplam yaklaşık 27 GPU-saat.

Kapatılmazsa düşecek cümle: Karar düşmez; 04_experiments.tex:231'deki Welch cümlesi ("Welch intervals ... are much wider because the new cells have two runs each") Holm sonrası Welch p'leriyle güçlendirilmelidir.

### B1-11 (minor) w beyaz kutu saldırısına bağlı; AutoAttack'lı w ile farklı bir bölüştürme q'yu 0,866'ya taşır

Ayrışım w'yi PGD-10 beyaz kutu saldırısından alır. Kayıtlı AutoAttack sonuçlarından koşullu w yeniden hesaplandı (yeni altı model ilk 1000 görüntü, `konsey_b6_aa`; C1 çifti tam test, `c1_seeds/c1_seed_summary.json`). log w'deki artış hücre ortalamasıyla V-scr 0,084, V-IN 0,076, R224-scr 0,095, R224-IN 0,148, R32 0,138'dir (`ayrisim.json`, `a_w_saldiri_bagimliligi.hucre_ort_d_omega`). Panel terimi karşıtlıklarda düştüğünden kaymalar hesaplanabilir: H1 +0,006, H2 +0,030, H3 +0,042 (yeni nokta +0,045), q tohum başına 0,838, 0,861 ve 0,899, ortalama 0,866. Bu bir duyarlılık değil, farklı bir bölüştürmedir: köşegen dışındaki T'ler PGD-10 ile bırakılıp yalnız w AutoAttack'le değiştirilmiştir, yani payda ile pay farklı saldırılardan gelir; tutarlı bir sürüm bütün matrisin daha güçlü bir saldırıyla yeniden üretilmesini ister. Panel üyelerinin AutoAttack'lı w'si ölçülmediğinden K-b için yalnız eşik verilebilir: panel ortalaması log w artışı 0,153'ü aşarsa K-b'nin %90 üst sınırı 0,10'u geçer; kendi CNN'lerimizdeki 0,095 ile 0,148 aralığı K-b'yi +0,024 ile +0,076 arasına koyar. Ayrıca H1'in −0,065'lik kısmı doğrudan −½Δω teriminden gelir (`d_H1_bolusu.H1_eksi_yarim_delta_omega`).

> Hakem cümlesi: "Vulnerability is measured with PGD-10, whose gap to AutoAttack differs by architecture; replacing w alone with its AutoAttack value moves the symmetric share to 0.87 and H3 to +0.045, which shows that the split between vulnerability and direction depends on the white-box attack and calls for the full decomposition under a stronger attack."

Kapatan iş: veri. Yedi panel üyesinde 2000 görüntülük ve altı yeni modelde tam test AutoAttack (B6'da altı model × 1000 görüntü 2826 s, föy M13.3; küçük modelde 1000 görüntü başına yaklaşık 0,13 sa, WRN-28-10 ağırlıklı panelde yaklaşık dört kat); toplam yaklaşık 14 GPU-saat. Tutarlı sürüm için B1-09'un daha güçlü saldırılı matrisiyle birleştirilir.

Kapatılmazsa düşecek cümle: 01_introduction.tex:28 "On CIFAR-10 a share of $0.936$" sayısı "PGD-10 vulnerability" kaydıyla okunmalıdır.

### B1-12 (minor) Tohum, görüntü ve panel bileşenleri birlikte alındığında belirsizlik büyür, kararlar değişmez

Önceki panel, K-b aralığının yalnız üç tohumun yayılımını taşıdığını ve görüntü gürültüsünün bunun üç katı olduğunu not etmişti (birlesik.md:502); hiyerarşik bootstrap (tohum ve görüntü) bu yüzden M11'de üretildi. Panel üyeliği ise hiçbir aralığa girmemektedir; makale aralıkların "conditional on test images and panel" olduğunu yazar (main.tex:133). Bu turda panel üyesi bırakmalı jackknife SE'si, hiyerarşik bootstrap SD'siyle birleştirildi (`olcekli_etki.json`, `uc_bilesenli_belirsizlik`; bileşenler bağımsız sayıldı, normal yaklaşım). ρ(V-scr) için hiyerarşik SD 0,0203, panel SE'si 0,0164, birleşik %90 aralık [−0,031; +0,055]; panel bileşeni toplam varyansın %40'ıdır. Yalnız koşu SE'siyle karşılaştırıldığında panel SE'si 2,5 kat (varyans olarak yaklaşık 6,3 kat) büyüktür (`ayrisim.json`, `g_panel_rastgele_etki`). q için birleşik aralık [0,891; 0,982], H1 için [−0,411; −0,317] (panel payı %62), H2 için [0,200; 0,321], H3 için [−0,025; +0,032]. K-b ve H3 üç bileşenli aralıkla da bandın içindedir. Panel yedi üyenin dördü ResNet-18 türevi olduğundan jackknife panel bileşenini eksik kestirir.

> Hakem cümlesi: "For the directional term, panel membership contributes as much uncertainty as seeds and images together; the decisions survive a three-component interval, but statements about robust CNNs in general require the panel to be treated as a random sample, which a mostly ResNet-18 panel is not."

Kapatan iş: analiz. Üç bileşenli aralıklar tab:panel_tests ve tab:fb4'e duyarlılık satırı olarak eklenmeli; "against robust CNNs" ifadeleri "against this panel" diye tutarlı biçimde daraltılmalı. GPU yok.

Kapatılmazsa düşecek cümle: 05_discussion.tex:21 "Similarity to the target family then accounts for most of a source's transfer deficit into it" genellemesi.

### B1-13 (minor) Eşdeğerlik sınırı log birimine bağlı ve ölçek ile protokole taşınamaz

TOST sınamaları δ'ya duyarsızdır: K-b (CIFAR-10) Holm sonrası destek δ = 0,035'e kadar sürer, hiyerarşik bootstrap %90 aralığı 0,046'ya denktir; H3 için t ile 0,030, Welch ile 0,060 (`cikarim.json`, `delta_taramasi.ozet`). CIFAR-100'de K-b desteği için δ = 0,185 gerekir. δ'nın dayanağı (0,0897) ViT çiftlerini de içeren bir RMS'tir (ON_KAYIT_2026-10-29.md:50) ve makale bunu "loose" diye kabul eder (03_methodology.tex:264). Yeni pay, log birimiyle tanımlı bir bandın B1-01 ve B1-02'de 0,2 ile 0,5 log birimi oynayan bir niceliğe uygulanması ve ±0,10'un kaynak açığının (0,389) yaklaşık dörtte birine karşılık geldiğinin yazılmamasıdır.

> Hakem cümlesi: "The ±0.10 margin is defined in log units from a pool that contains the ViT itself and has no counterpart on the logit, h or both-correct scales, where the same quantity moves by 0.2 to 0.5, so equivalence should also be stated against a margin expressed relative to the source gap."

Kapatan iş: analiz. δ'nın kaynak açığına oranı yazılmalı ve eşdeğerlik ölçek ve protokol duyarlılıklarıyla birlikte raporlanmalı. GPU yok.

Kapatılmazsa düşecek cümle: 01_introduction.tex:28 "the ViT's directional term $\rho = +0.012$ lies within the registered equivalence bound of $\pm0.10$" tek başına bırakılamaz.

### B1-14 (minor) Ayrışım çift düzeyinde serbestlik derecesi sıfır olan bir özdeşlik; sınanabilir içerik raporlanmıyor

log T = log w + log τ̄ + r/2 iki model için tam belirlenimlidir; makale bunu "accounting identity" diye yazar (03_methodology.tex:143). Sınanabilir içerik r'nin potansiyelle açıklanan payı ve w katsayısının bire sabitlenmesinin veriye uyumudur. Yirmi modelli matriste potansiyel payı 0,919'dur (föy M9.4 S7 ile aynı; `ayrisim.json`, `c_hodge_ve_serbest_potansiyel`); dolaşım RMS'i 0,022, iki bölünmüş yarı arasındaki farkın yarısıyla kestirilen gürültü RMS'i 0,036'dır ve dolaşımın iki yarı arasındaki korelasyonu 0,56'dır. Serbest bırakılan potansiyelin −ω'ya eğimi b = 0,950, R² = 0,957'dir; katsayının bire sabitlenmesi ρ(V-scr)'ye +0,028, H3'e +0,004 ekler.

> Hakem cümlesi: "The decomposition is an identity with zero degrees of freedom per pair; its empirical content is the quasi-symmetry fit, which should be reported as such (circulation against noise, and the free slope of the potential on log w, 0.95 here)."

Kapatan iş: analiz. Dolaşım-gürültü karşılaştırması ve serbest eğim Yöntem'e bir paragrafla eklenmeli. GPU yok.

Kapatılmazsa düşecek cümle: 03_methodology.tex:143 "its content lies in the measured sizes of the terms and in how they respond to the design" ifadesi, içeriğin sınamasını göstermeden zayıf kalır.

### B1-15 (minor) Maskeleme denetimi yalnız altı modelde ve ilk 1000 görüntüde

Maskeleme kuralı PGD-10 ile AutoAttack arasında 10 puanı bayrak sayar ve yalnız altı yeni modelde, ilk 1000 görüntüde uygulanmıştır (föy M9.7). Farklar 3,20 ile 7,40 arasıdır, en büyükleri R224-IN'dedir (7,40 ve 5,60; föy M9.1). Panel üyeleri ve V-scr B6 kapsamı dışındadır; V-scr'nin tam test farkı 32,69 ile 29,14 arasında 3,55 puandır (föy Tablo I). Eşiğin seçimi gerekçelendirilmemiştir ve fark hücreler arasında iki kattan fazla değiştiği için doğrudan w'ye ve B1-11'deki kaymalara girer.

> Hakem cümlesi: "The masking check covers six of twenty models on 1,000 images with an unjustified 10-point flag; the PGD–AutoAttack gap more than doubles between cells and enters w directly, so it should be reported for all models on the full test set."

Kapatan iş: veri. B1-11'in AutoAttack koşusuyla kapanır; ek GPU yok. Eşiğin gerekçesi yazılmalı.

Kapatılmazsa düşecek cümle: 06_conclusion.tex:12 "the registered AutoAttack rule flags none of the six new models" doğru kalır ama maskeleme yokluğunun kanıtı olarak okunamaz.

### B1-16 (minor) R32 köprüsü tek ayaklı

S1 köprüsünün Welch altında eşdeğer olmadığı makalede yazılıdır (04_experiments.tex:241; föy 1561, Welch %90 [−0,120; +0,119]). Yeni pay, köprünün yalnız CNN tarafında olmasıdır: ViT için 32 piksel girdili bir hücre yoktur. Büyütülmüş 32 piksellik görüntüde 16 piksellik yamaların her biri özgün görüntünün yaklaşık 2,3 piksellik bir bölgesine karşılık gelir; büyütmenin ViT'yi kendi başına benzemez kılıp kılmadığı ölçülmemiştir.

> Hakem cümlesi: "The resolution bridge exists only on the CNN side; a ViT at native 32-pixel resolution (patch 4) would show whether upsampling itself makes the ViT dissimilar."

Kapatan iş: eğitim. 32 piksel, 4 piksellik yamalı ViT-Tiny, iki tohum, C1 tarifi; koşu başına yaklaşık 2 sa (kestirim), matrisle yaklaşık 5 GPU-saat. B1-03'ün yukarı eşleştirme koluyla birleştirilebilir.

Kapatılmazsa düşecek cümle: 04_experiments.tex:241 "The 32-pixel ResNet-18 of the pair and the 224-pixel ResNet-18 of the design relate to the panel in the same way" yalnız CNN tarafı için geçerlidir; Welch kaydı cümlede zaten vardır.

### B1-17 (minor) ImageNetV2 sıfırdan satırı tek dolaylı çifte dayanıyor

ImageNetV2 panelinin betimsel olduğu ve aralıklarının yalnız görüntü örneklemini taşıdığı makalede yazılıdır (04_experiments.tex:387; 05_discussion.tex:23). Yeni pay, B1-03 ile birlikte okumadır: tek sıfırdan çift Δσ_scr,Liu = −0,055 [−0,137; +0,022] ile belirsizdir (föy 1939) ve CIFAR'daki büyük sıfırdan benzemezliği (−0,364) doğal ölçekte görülmemektedir; bu, küçük veride yakınsama okumasıyla uyumludur.

> Hakem cümlesi: "At ImageNet scale the only scratch pair shows −0.055 with an interval covering zero, which is what one would expect if the CIFAR scratch-row dissimilarity were a small-data convergence effect."

Kapatan iş: veri. RobustBench ImageNet listesinden ek aynı tarifli CNN-transformer çiftleri; B8'in 14 modelli matrisi 973 s sürmüştür (föy M13.3), iki ek çiftle yaklaşık 1 GPU-saat.

Kapatılmazsa düşecek cümle: 04_experiments.tex:393 "the large scratch-row dissimilarity found on CIFAR should not be carried to this scale" cümlesi zaten vardır; eksik olan, bunun CIFAR bulgusunun yorumuna geri bağlanmasıdır.

### B1-18 (minor) Kontrol noktası seçimi ve erken durma σ'yı hücreye göre farklı etkileyebilir

Bütün koşular doğrulama PGD doğruluğuyla erken durdurulmuş ve en iyi epok seçilmiştir. Seçilen epoklar V-scr'de 25, 18 ve 19, R32'de 51, 56 ve 57 (föy M8.14, 1383-1390), B3 hücrelerinde 16 ile 38 arasındadır (föy M9.1). Seçimin σ üzerindeki etkisi küçük değildir: C1 çiftinde son kontrol noktasında log τ̄_RV −1,170, seçilen kontrol noktasında −1,083'tür (föy 1707, 1713); fark −0,087, H1'in yaklaşık dörtte biridir. 2×2 hücrelerinde son ya da ara kontrol noktalarıyla bir matris üretilmemiştir; seçim kuralının ViT'yi daha erken, daha az yakınsamış bir noktada dondurması B1-03'teki karıştırıcıyla aynı yönde işleyebilir.

> Hakem cümlesi: "Checkpoints are selected by validation PGD accuracy at epochs 16 to 57, and in the original pair the last checkpoint lowers the pairwise similarity by 0.09, a quarter of H1; the two-by-two contrasts should be shown at the last checkpoint and along the training trajectory."

Kapatan iş: veri. B3 koşuları `--save-every 10` ile kaydedilmiştir (föy M13.1 (c)); son kontrol noktalarıyla bir yirmi modelli matris (yaklaşık 0,5 sa) ve her koşunun 10 epokluk ara kontrol noktalarıyla panele karşı kısa matrisler (yaklaşık 2 sa). V-scr için ara kontrol noktası kaydedilmediğinden (save-every 0) yalnız son kontrol noktası kullanılabilir. Toplam yaklaşık 2,5 GPU-saat.

Kapatılmazsa düşecek cümle: 01_introduction.tex:32'deki H1 sayısı "at the selected checkpoint" kaydını taşımalıdır.

### B1-19 (minor) Etki büyüklüğü CNN'ler arası yayılımla ölçeklenmiyor

Makale H1'i (−0,364) log biriminde ve tohum SD'siyle verir; CNN'ler arasındaki doğal mimari ve tarif yayılımına göre ne kadar büyük olduğunu vermez. Panel üyelerinin σ'sı −0,576 ile −0,381 arasındadır; yedi panel üyesi ve kendi üç CNN hücremizden oluşan on birimde σ'nın standart sapması 0,102'dir (`olcekli_etki.json`, `olcekli_etki`). Bu ölçekte H1 −3,6 SD, V-scr'nin σ'sı CNN dağılımının −4,8 SD altında, V-IN'inki −2,2 SD, XCiT-S12'ninki −0,45 SD'dir. Bu, B1-04'teki karışık tabloyu sayıya döker: sıfırdan ViT CNN dağılımının çok dışındadır, ImageNet başlatmalı ViT de dışındadır ama yarı uzaklıkta, öbür dikkat modeli ise içindedir. Bu ölçek, okurun H1'i yorumlaması için tohum SD'sinden daha uygun bir referanstır ve hakemin "−0,364 büyük mü" sorusunu doğrudan yanıtlar.

> Hakem cümlesi: "Express the architecture effect relative to the spread among robust CNNs: the scratch ViT lies 4.8 CNN standard deviations below their mean, the ImageNet-initialized ViT 2.2, and XCiT within the CNN range, which should be reported alongside the seed-level intervals."

Kapatan iş: analiz (yapıldı). Ölçeklenmiş etki büyüklüğü tab:fb4'e ve B1-04 tartışmasına eklenmeli. GPU yok.

Kapatılmazsa düşecek cümle: Doğrudan düşen cümle yok; 04_experiments.tex:227'deki "beyond the predicted size of −0.20" karşılaştırması tek referans olarak kalır.

## Denenen ama düşmeyen itirazlar

Hakemin büyük olasılıkla soracağı dört itiraz bu turda sayıyla sınandı ve makaleyi zayıflatmadı; yanıt mektubunda bunlar kullanılabilir. Holm ailesinin bütün doğrulayıcı sınamaları (F_B2, F_B4, F_B9, F_B10; 15 sınama) tek aile sayacak biçimde genişletilmesi hiçbir kararı değiştirmemektedir; K-b(CIFAR-100) dışındaki en büyük düzeltilmiş p K-b(CIFAR-10) için 0,0055'tir (`cikarim.json`, `holm_aileleri`, `tek_ailede_karari_degisen` boş). Welch serbestlik dereceleriyle F_B4'ün üç sınaması da Holm sonrası desteklenmektedir (0,027, 0,042, 0,026). TOST kararları δ'ya duyarsızdır (B1-13). Tohum, görüntü ve panel bileşenlerini birlikte taşıyan aralıklarla K-b ve H3 bant içinde, H1 ve H2 sıfırdan uzak kalır (B1-12). Bu sonuçlar, makalenin zayıflığının çıkarım iskeletinde değil ölçüm tanımında ve tasarımın kimlik gücünde olduğunu göstermektedir.

## En tehlikeli üç bulgu

| Sıra | Kimlik | Neden tehlikeli | Kapatma türü | GPU-saat |
|---|---|---|---|---|
| 1 | B1-01 | Tutarlı her-ikisi-doğru protokolünde yönlü pay 0,02'den yaklaşık 0,31'e çıkıyor; q 0,577, ρ +0,188 ve H3 TOST p 0,501. ViT bu protokolde yönlü olarak da zayıf kaynak; başlığın "Less a Weak Source" kısmını doğrudan hedef alıyor ve hakem aynı kayıtlardan yeniden üretebilir | analiz ve kuramsal savunma | 0 |
| 2 | B1-03 | σ-temiz doğruluk doğrusu seçimine göre H1'in %44, %67 ya da %88'i doğrulukla birlikte değişiyor; hepsi dış değerleme, karıştırıcının payı belirlenemiyor | eğitim | 26 |
| 3 | B1-02 | K-b'nin eşdeğerliği log-logit ailesinde yalnız κ ∈ [−0,20; 0,25] penceresinde; makalenin protokol-değişmez saydığı h ölçeğinde ρ −0,316 ve H1 −0,134 | analiz | 0 |

## Yeni eğitim ya da veri gerektiren bulgular

| Kimlik | Tür | İş | GPU-saat (RTX 5090) | Dayanak |
|---|---|---|---|---|
| B1-03 | eğitim | Aşağı eşleştirilmiş R224-scr (3 koşu) ve yukarı eşleştirilmiş sıfırdan ViT (3 koşu), iki matris | 26 | föy M9.1 R224-scr AT 3,03 sa; M13.3 B9 matrisi 833 s |
| B1-04 | eğitim | DeiT-S ya da Swin-T, ikinci transformer ve ConvNeXt-T, sıfırdan, ikişer tohum (6 koşu), matris | 61 | `_ek_flop_olcumu.json` FLOP oranı 2,53-2,55; R224-scr 4,09 sa |
| B1-07 | eğitim | ViT-S ile ResNet-50 2×2, dört hücre, üçer tohum | 88 | FLOP oranı 2,25 ve 2,55; 2,97 sa/koşu |
| B1-08 | eğitim | CIFAR-100'de 2×2 (6 koşu) ve TRADES ile çift (4 koşu) | 30 | föy M9.1 ortalama 2,97 sa/koşu |
| B1-09 | veri | ε 4/255 ve 16/255 matrisleri, PGD-50 ve DI/TI, TGR doğrulaması | 4 | föy M13.3 matris süreleri |
| B1-10 | eğitim | Normalizasyon hücresi (4 koşu) ve tarif eşleşmiş IN hücreleri (4 koşu) | 26 | föy M9.1 hücre süreleri |
| B1-05 | eğitim | V-scr'nin B3 zincirinde üç tohumla yeniden eğitimi (isteğe bağlı) | 12,5 | föy M9.1, M13.1 |
| B1-06 | eğitim | Üç yeni hücreye üçer tohum (n = 5) | 27 | föy M9.1: 4,09 + 2,65 + 2,16 sa |
| B1-11 | veri | Panelde ve yeni modellerde AutoAttack ile w | 14 | föy M13.3 B6 2826 s / 6 model / 1000 görüntü |
| B1-15 | veri | B1-11 ile aynı koşu | 0 | |
| B1-16 | eğitim | 32 piksel, 4 piksellik yamalı ViT-Tiny, iki tohum | 5 | kestirim |
| B1-17 | veri | ImageNetV2'ye ek aynı tarifli çiftler | 1 | föy M13.3 B8 973 s |
| B1-18 | veri | Son ve ara kontrol noktalarıyla matrisler | 2,5 | föy M13.1 save-every 10; M13.3 matris süreleri |
| Toplam | | on üç bulgu (sekiz eğitim, beş veri) | yaklaşık 297 | |

Asgari paket olarak tek başına en çok riski kapatan işler B1-03'ün aşağı eşleştirme kolu (yaklaşık 10 sa), B1-06 (27 sa), B1-09 (4 sa), B1-11 (14 sa) ve B1-18 (2,5 sa) olup toplamı yaklaşık 58 GPU-saattir; kampanya farkı da dışlanmak istenirse B1-05 ile yaklaşık 70 GPU-saate çıkar. B1-01 ve B1-02 GPU istemez, ama metinde ve başlıkta daraltma ya da kuramsal savunma gerektirir. Süreler B3 kampanyasının GPU'yu zaman zaman paylaştığı koşullardan türetildiği için (defter/pilot oranı 1,05 ile 2,19, föy M9.1) boş GPU'da daha kısa sürebilir.

## Koşulan analizler ve dosyaları

Bütün betikler konteynerde `docker exec -w /workspace adeb_eval python arsiv/b2_yardimci/<betik>` ile koşuldu, her biri birkaç saniyede bitti ve GPU kullanmadı.

| Betik | Çıktı | İçerik |
|---|---|---|
| `arsiv/b2_yardimci/_curutme_ortak.py` | (modül) | Dondurulmuş betikten içe aktarma, ölçek fonksiyonları, her-ikisi-doğru alıcısı, JSON yazımı ve SHA-256 meta |
| `arsiv/b2_yardimci/_curutme_olcek.py` | `results/q1/curutme_2026-11-07/olcek.json` | κ taraması (log-logit ailesi) ve h ölçeğinde q, K-b, H1-H3; CIFAR-10 ve CIFAR-100 |
| `arsiv/b2_yardimci/_curutme_cikarim.py` | `results/q1/curutme_2026-11-07/cikarim.json` | 15 sınamalık Holm ailesi, Welch ile F_B4, δ taraması, MDE ve TOST gücü, hücre varyans oranları |
| `arsiv/b2_yardimci/_curutme_ayrisim.py` | `results/q1/curutme_2026-11-07/ayrisim.json` | AutoAttack'lı w kaymaları, çapraz başlatma benzerliği, Hodge dolaşımı ve serbest eğim, H1 bölüşü, yarı tutarlı her-ikisi-doğru, σ-temiz doğruluk, panel jackknife SE |
| `arsiv/b2_yardimci/_curutme_her_ikisi.py` | `results/q1/curutme_2026-11-07/her_ikisi_tutarli.json` | Çift başına ortak maskeli tutarlı her-ikisi-doğru ayrışımı; K-a, K-b, H1-H3 (CIFAR-10), K-a, K-b (CIFAR-100) |
| `arsiv/b2_yardimci/_curutme_olcekli_etki.py` | `results/q1/curutme_2026-11-07/olcekli_etki.json` | CNN σ yayılımıyla ölçeklenmiş etki büyüklüğü ve z değerleri; tohum, görüntü ve panel bileşenli belirsizlik (ikinci tur) |

Doğrulama: `olcek.json` κ = 0 satırı ve `ayrisim.json` `d_H1_bolusu.H1_yeniden` kayıtlı değerleri (q 0,936; ρ +0,012; H1 −0,364; H2 +0,260; H3 +0,003; föy 1526-1528, 1587-1588) dördüncü ondalığa kadar yeniden üretmektedir; `c_hodge_ve_serbest_potansiyel.potansiyel_payi_ortalama_r` = 0,919 föydeki S7 değeriyle, `olcekli_etki.json` hücre ortalamaları föy 1496-1499 ile aynıdır.

## Kararlar

Tutarlı her-ikisi-doğru ayrışımında w'yi de ortak maskede hesapladım, çünkü bu dört oranın aynı görüntü kümesinde ölçüldüğü tek sürümdür; bunun bedeli w'nin çifte bağlı hale gelmesidir ve raporda böyle yazdım. Ön kaydın uyguladığı tanım (protokoller.py, köşegende hedef-doğru w) yarı tutarlı sürüme denk düştüğü için ortak maskeli sürüm bir sapmadır; iki sürüm de manşetle çeliştiğinden karşı sayı olarak daha ılımlı olanı (+0,188) kullandım ve yarı tutarlı sürümün maske uyuşmazlığından şiştiği yönündeki ilk tur iddiamı, gösterilmediği için geri çektim.

B1-01'i birinci sırada tuttum, çünkü yeni eğitim gerektirmeden q'yu, K-b'yi ve H3'ü değiştiriyor; ancak okumayı çürütücünün işaret ettiği biçimde düzelttim: simetrik bileşen bu protokolde büyür, düşen şey simetrik paydır ve bunun nedeni yönlü payın artmasıdır. Hangi protokolün kestirilmek istenen nicelik olduğu kuramsal bir sorudur ve hedef-doğru protokol savunulabilir; eksik olan, bu savunmanın ve duyarlılığın ayrışım düzeyinde metinde bulunmamasıdır.

B1-03'te σ-temiz doğruluk ilişkisini üç kestirimle verdim (tüm CNN doğrusu, R224-scr artığı düşülmüş tüm CNN doğrusu ve kendi CNN doğrusu), çünkü üçü de dış değerlemedir ve sonuç doğrunun seçimine çok bağlıdır. İlk turda "%12 ile 88" yazmıştım; %12 açıklanmayan paydı, doğru aralık %44 ile %88'dir.

B1-04'ü "karışık kanıt" olarak yeniden yazdım ve major tuttum, çünkü başlık mimari ailesi düzeyinde kurulmuşken bunu ayrıştıracak ikinci bir transformer tasarımda yoktur. Çürütücünün gösterdiği yön (V-scr'nin V-IN'e CNN'lerden 0,29 ile 0,34 daha yakın olması) ve B1-19'daki ölçeklenmiş etki büyüklüğü aile okumasını destekleyen kanıt olarak bulguya girdi.

B1-05'i minöre indirdim ve çürütücünün kosinüs çizelgesi gerekçesini uygulamadım, çünkü föy M13.1 (c) B3 hücrelerinin de kosinüs T_max 100 çizelgesiyle eğitildiğini ve 80 epokluk tavanın yalnız `--stop-epoch` ile uygulandığını göstermektedir; bütün koşular tavanın altında durduğundan öğrenme oranı yörüngesi hücreler arasında aynıdır. Kalan pay donanım ve kod sürümüdür.

B1-06'yı minöre indirdim, çünkü kararlar Welch altında sürüyor ve gözlenen ρ etkileşimi en küçük saptanabilir etkinin 1,7 katıdır. B1-10'dan "H2'nin büyük kısmı doğruluk kazancıyla gelir" cümlesini dayanağı olmadığı için çıkardım, B1-15'ten kaynaksız "olağan değildir" yargısını kaldırdım ve B1-07'deki atıfsız genellemeyi silip bulguyu önceki konseyin ve makalenin zaten yazdığı sınırla bağladım.

GPU-saat kestirimlerinde B3 defterinin gerçekleşen sürelerini (föy M9.1) taban aldım, büyük modeller için `_ek_flop_olcumu.json`'daki FLOP oranıyla doğrusal ölçekledim. Yeni mimarilerin CIFAR'da sıfırdan çekişmeli eğitimle kararlı eğitilip eğitilmeyeceği ayrı bir risktir ve süreye dahil değildir. Önceki hakem panelinin (birlesik.md) uyguladığı metin daraltmalarını tekrar etmedim; yalnız o panelin açık bıraktığı işlerin (A1, A3, A7, A8) yetersiz kaldığını yeni sayılarla gösterdiğim yerlerde bulgu yazdım ve metinde zaten yazılı olan kısımları her bulguda adıyla andım.

## İkinci turda değişenler

B1-01'e kaynak açığı ve bileşen bağlamı (G 0,711 ile 0,767; simetrik 0,42; yönlü 0,31), ön kayıt tanımıyla ilişki (S9-4 yarı tutarlı sürüme denk, ortak maske sapma), w'nin çifte bağlılığı ve makalede zaten yazılı kısımlar eklendi; "dörtte biri" %18 olarak düzeltildi, "yapay olarak şişirir" iddiası geri çekildi. B1-02 makalenin mevcut log ölçek kayıtlarını anar, H3'ün geniş penceresini ve h ölçeğinde H1 −0,134'ü ekler. B1-03'ün aralığı %44 ile %88 olarak düzeltildi, kendi CNN doğrusunun x aralığı 85,11 ile 86,35 yazıldı, hakem cümlesi yumuşatıldı, süre 26 sa oldu. B1-04 karışık kanıt olarak yeniden yazıldı, süre altı koşuyla 61 sa oldu. B1-05 minöre indi, R1 M3 tekrarı ve tavanın fiilen etkisiz olduğu yazıldı. B1-06 minöre indi. B1-07'de FLOP oranı 2,25 ve 2,55 olarak düzeltildi, süre 88 sa oldu. B1-10'un süresi 26 sa olarak düzeltildi ve dayanaksız cümle çıkarıldı. B1-11'e farklı bölüştürme sınırı, B1-12'ye varyans oranı 6,3 ve üç bileşenli aralık eklendi. B1-15, B1-16 ve B1-17 metinde zaten yazılı olanları anar. Yeni bulgular B1-18 (kontrol noktası seçimi) ve B1-19 (CNN yayılımıyla ölçeklenmiş etki) eklendi; hiyerarşik belirsizlik B1-12'ye katıldı. "Kararlar" bölümü düzyazıya çevrildi.
