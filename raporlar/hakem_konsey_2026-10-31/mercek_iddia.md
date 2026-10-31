# Mercek 2: iddia-kanit uyumu ve konumlandirma (31.10.2026)

Bu rapor salt okur hakem ajaninin yapisal ciktisindan ana oturumca dosyaya aktarilmistir; metin ajanin kendi ifadeleridir.

Genel karar: BUYUK_REVIZYON

## Bulgular (siddet sirasiyla)

### 1. [kirmizi] [Zayıf halka 1/3] Manşetteki büyük benzemezlik yalnız temiz doğruluğu düşük, sıfırdan eğitilmiş ViT hücresinde var; doğruluk eşleşince etki makalenin kendi ihmal sınırına iniyor

Dosya: paper/manuscript/main.tex:65-67, main.tex:117; sections/01_introduction.tex:28-32; sections/04_experiments.tex:224, 238; sections/05_discussion.tex:60; sections/06_conclusion.tex:12

Ifade: Başlık genel bir iddia taşıyor: "Not a Weak Source but a Different One: ... in CNN-ViT Adversarial Transfer". Özette de "the scratch-trained ViT resembles the panel less than the ResNet (−0.364 [−0.415, −0.314])" yazıyor. Gövde ise bunu kabul ediyor: "a less converged solution and an architectural dissimilarity cannot be told apart" (05:60) ve "part of A^σ_scr may reflect a less converged solution" (04:238).

Kanit: Ölçek etkisi birbirinden 2,5 ila 3,5 kat farklı iki rejime ayrılıyor. Sıfırdan satırında V-scr'nin temiz doğruluğu 73.53, R224-scr'ninki 85.73 (FÖY M9.2:1496, 1498) ve σ farkı −0.364. Doğruluğun eşleştiği her karşılaştırmada fark kabaca üçte bire iniyor. ImageNet satırında V-IN 83.43, R224-IN 86.00 temiz doğrulukta; σ değerleri −0.739 ile −0.635 (FÖY 1497, 1499), yani fark −0.104. Föydeki birleşik SD 0.0273 (FÖY 1532) ve df 5 ile bu farkın %90 aralığını ben yaklaşık [−0.159, −0.049] buldum. Bu aralık önceden kaydedilmiş δ = 0.10 ihmal sınırının iki yanına taşıyor. ImageNetV2'de doğruluğu eşleşmiş Singh çiftlerinde Ā^σ_IN −0.142 [−0.197, −0.090] (04:380; FÖY M10.4:1938); bu aralığın üst ucu da bandın içine giriyor. Tek sıfırdan ImageNet çifti (Liu) −0.055 ve "uncertain". H2 (+0.260) aynı karıştırıcıyla birebir hizalı: başlatma ViT'nin temiz doğruluğunu 9.90 puan artırıyor, ResNet'inkini 0.27 puan (FÖY 1496-1499). Bu yüzden "σ yakınsama ya da doğrulukla birlikte değişir" modeli H2'yi H1 kadar iyi açıklıyor. CIFAR-100 yinelemesi karıştırıcıyı da taşıyor: ViT 41.94-44.06, ResNet 62.68-64.65 (04:158). Ön kayıttaki O1 manşeti bu farkı "mimariye ait" sayıyordu (ON_KAYIT §6 satır 100). O2 bölgesi yalnız girdi hattını dışlıyordu; yakınsama seçeneği hiçbir sınamaya bağlanmamıştı. Yazarların kendi literatür notu da bu itirazı öngörmüştü (02_literatur.md:29, Mo: "sıfırdan çekişmeli eğitilmiş ViT zaten kötü eğitilmiş bir modeldir"). Bir Q1 hakemi bu noktada şunu diyebilir: sonuç, kötü yakınsamış bir ViT-Tiny'nin CNN'lere benzemediğidir; ViT ailesi hakkında bir sonuç değildir.

Duzeltme: Kabul için en önemli koşul bu bulgudur. En az emekle en çok işi şu deney görür: doğruluğu eşleşmiş, sıfırdan eğitilmiş bir ViT hücresi, ön kayda ek olarak dondurulur, iki tohumla koşulur ve aynı yedi üyeli panele karşı ölçülür. Bunun için örneğin 32 pikselde 4×4 yamalı, CIFAR'a özgü bir ViT-Tiny ya da temiz doğruluğu en az %83'e ulaşana kadar uzatılmış bir temiz aşama kullanılabilir. Bu hücrede A^σ −0.3 düzeyinde kalırsa manşet sağlamlaşır; −0.1 düzeyine inerse manşet bu ölçeğe çekilmelidir. Deney yapılmayacaksa üç değişiklik gerekir. (1) Başlığın kapsamı daraltılır, örneğin "... for a Scratch-Trained ViT-Tiny" eklenir ya da "Mostly a Different Source" denir. (2) Özete doğruluğu eşleşmiş büyüklükler girer: V-IN ile R224-IN farkı ve Singh çiftleri. Bunun için brif §9'un önerdiği föy eki M9.10 (türetilmiş hücre karşıtlıkları ve aralıkları) önce üretilir. (3) Mevcut 20 modellik CIFAR-10 matrisinden masada σ'nın temiz doğruluğa regresyonu çıkarılır ve V-scr'nin CNN eğilim çizgisinden ne kadar saptığı raporlanır; bu GPU gerektirmez. 03:275'teki "architectural dissimilarity" ifadesine de "not separated from convergence by this design" kaydı eklenmelidir.

### 2. [sari] Başlıktaki ve özetteki "zayıf kaynak" iki farklı niceliği karıştırıyor: çift içi asimetri ile panel kaynak açığı

Dosya: paper/manuscript/main.tex:65, 117; sections/01_introduction.tex:16; sections/04_experiments.tex:70; sections/05_discussion.tex:33

Ifade: Özet asimetriyle açılıyor: "Adversarially trained ViTs look like weak transfer sources against CNNs, but two models cannot split this asymmetry between source and target." Ardından gelen yanıt başka bir nicelik hakkında: "0.936 ... of ViT-Tiny's panel source gap to ResNet-18 is symmetric". Girişteki ikilem (01:16) ikinci açıklamanın öngörüsünü şöyle kuruyor: "the difference between directions comes from how vulnerable each target is".

Kanit: Simetrik terim tanım gereği iki modelli asimetriye giremez. Makale bunu kendisi söylüyor: "cannot appear in a two-model asymmetry at all" (04:70). Çiftin asimetrisi ise yalnız yarı yarıya kırılganlıktan geliyor. Potansiyel payı 0.541; geri kalan yönlü artık r_RV = +0.115, koşum SD'si 0.010 ve görüntü bootstrap SD'si 0.030 (FÖY M9.9:1706, 1708, 1722). Bu değer kaydedilmiş δ = 0.10'u aşıyor; CIFAR-100'de +0.154 (FÖY 1718). Birincil log ölçekte ViT üç ayrı durumda yönlü olarak zayıf kaynak çıkıyor: kendi çiftinde (+0.115), CIFAR-100 panelinde (ρ +0.143, eşdeğerlik çürütüldü; FÖY M10.2:1839) ve dönüştürücü referansına karşı (XCiT ikincil panelinde ρ +0.198 ile +0.204; FÖY 1606). Başlığın "Not a Weak Source" ifadesi bu üç durumda sözcüğü sözcüğüne çürüyor. Doğru tutan okuma şudur: üçüncü modellere giden transferin düşük olması büyük ölçüde iki yönlü benzemezliktir.

Duzeltme: Yöntem bölümünde "weak source" bir kez tanımlanmalı: üçüncü modellere düşük çıkış transferi, yani panel kaynak açığı G. Çift içi asimetri bundan açıkça ayrılmalı. Özete bir yan cümle girmeli: "within the pair, about half of the log asymmetry is the ViT's higher vulnerability and half a pair-specific directional residual (+0.115)". Girişteki ikilemin ikinci kolu "explains the low level of transfer in both directions; within the pair it accounts for about half of the direction" diye yeniden kurulmalı. Başlık "Less a Weak Source than a Different One" ya da "Mostly a Different Source" biçimine yumuşatılmalı. 05:33'teki "belongs to this pair" cümlesine de r_RV'nin δ'yı aştığı yazılmalı.

### 3. [sari] [Zayıf halka 2/3] ViT'nin zayıf kaynak görünmesinin baş rakip açıklaması (saldırı yetersizliği, Naseer) yalnız PGD'ye çok yakın saldırılarla sınanmış

Dosya: paper/manuscript/main.tex:117; sections/01_introduction.tex:32; sections/03_methodology.tex:62; sections/04_experiments.tex:326-329; sections/06_conclusion.tex:12

Ifade: Özette: "The gap survives each source's best permitted attack (0.960 [0.941, 0.976])". Girişte: "Momentum PGD and our adaptation of token gradient regularization do not close the source gap either".

Kanit: İzin verilen küme PGD-10, MI-PGD-10 ve uyarlanmış TGR'den oluşuyor. MI, PGD'den neredeyse ayırt edilemiyor: ViT kaynaklarında S_MI − S_PGD +0.015 ile +0.018 arasında (FÖY M9.6:1638-1640) ve seçim açığın yalnız 0.0155'ini kapatıyor (FÖY 1623). TGR her ViT kaynağında PGD'den 0.147-0.218 log birimi daha kötü transfer ediyor (FÖY 1648). Bu, TGR'nin yayımlanmış amacının, yani ViT'den CNN'e transferi artırmanın tersidir. Uyarlama ise tek γ değerini dikkat, QKV ve MLP yollarına birlikte uyguluyor ve 224'e büyütülmüş girdide çalışıyor (03:62). Bu ayarda bozulmuş olabilir; uygulamanın standart eğitilmiş bir ViT'de yayımlanmış kazancı yeniden ürettiğini gösteren bir doğrulama metinde yok. Naseer ve ark.'nın self-ensemble ve token refinement yöntemi, makalenin 02:37'de adını andığı rakip açıklamanın kendisi, hiç koşulmamış. Adım sayısı 10'da sabit; girdi çeşitlemesi ya da vekil topluluğu da denenmemiş. Ön kayıt da bunu kabul ediyor: K8 TGR'yi tek ayarla bıraktı (ON_KAYIT §5 B5).

Duzeltme: Önerilen yol iki adımlı. İlk adımda TGR uygulaması temiz eğitilmiş ViT-Tiny'den CNN'e transferde doğrulanır; yayımlanmış yön ve kabaca büyüklük elde edilmelidir. İkinci adımda bilinen tek bir ViT'ye özgü saldırı eklenir (Naseer self-ensemble ile token refinement ya da Wei ve ark.'nın PNA'sı) ve bir de yineleme ile çeşitleme varyantı koşulur (DI/TI, 50 adım). Korunma oranı bu genişletilmiş kümeyle yeniden hesaplanır; bu ek ön kayıtla ve keşifsel etiketle yapılabilir. Deney yapılamıyorsa özet "under PGD-10 and momentum PGD, which transfer almost identically; our adapted TGR transferred worse than PGD" diye daraltılmalı ve saldırı tarafı açıklaması sınırlılıklarda açık soru olarak yazılmalıdır.

### 4. [sari] [Zayıf halka 3/3] "Architecture leaves direction unchanged" cümlesi, işaret değiştiren bir mimari × başlatma etkileşimini ana etki ortalamasıyla örtüyor

Dosya: paper/manuscript/main.tex:117; sections/01_introduction.tex:32; sections/04_experiments.tex:224, 230, 494; sections/06_conclusion.tex:12

Ifade: Özette "on the log scale architecture leaves direction unchanged (+0.003)", sonuçta "on the log scale architecture leaves the directional term unchanged" yazıyor.

Kanit: Föydeki hücre ortalamalarından basit etkileri ben hesapladım (FÖY M9.2:1496-1499). Sıfırdan satırında ρ(V-scr) − ρ(R224-scr) = 0.012 − (−0.058) = +0.070; ImageNet satırında ρ(V-IN) − ρ(R224-IN) = −0.118 − (−0.054) = −0.064. A^ρ = +0.003 bu iki zıt işaretli etkinin ortalamasıdır; etkileşim −0.134. Birleşik SD 0.0169 ile (FÖY 1532) etkileşimin standart hatası yaklaşık 0.023, t yaklaşık −5.8 (df 5). Sıfırdan satırındaki basit etkinin %90 aralığı yaklaşık [+0.039, +0.101] ve δ'ya değiyor. Logit ölçekte H3 −0.087 [−0.110, −0.064]; ön kayıt kuralı bu ölçekte karar vermezdi (04:230; FÖY 1551). Makale 04:230'da "does not imply a small directional term in every cell" diyerek bunu kısmen kabul ediyor, ama özet ve sonuç ana etki cümlesini niteleme olmadan taşıyor. Brif §9 bu farkları (+0.070, −0.064, −0.134) föyde olmadıkları için metne almıyor.

Duzeltme: Föy eki M9.10'a ρ basit etkileri ve ρ etkileşimi aralıklarıyla eklenmeli (keşifsel). Özetteki cümle şöyle yazılmalı: "averaged over initialization, architecture's effect on direction is within ±0.10 on the log scale, though its sign depends on initialization". Sonuç ve katkı 3 aynı biçimde düzeltilmeli. 04:494'teki "H3 reverses in the same way" ifadesi de düzeltilmeli (yeşil m1).

### 5. [sari] "Symmetric share" q ve "similarity" σ okuması: kaynak ana etkileri σ'ya yarı yarıya yükleniyor, bu yüzden q = 0.936 "%93.6 benzemezlik" demek değil

Dosya: paper/manuscript/sections/03_methodology.tex:211-222; sections/04_experiments.tex:145-151; sections/05_discussion.tex:21, 33

Ifade: "has symmetric share q = (σ_R − σ_V)/G" (03:215); "A high σ_m means that m shares adversarial directions with the panel" (03:211); "most of the ViT's source deficit is symmetric" (05:33); "Similarity to the target family then accounts for most of a source's transfer deficit into it" (05:21).

Kanit: Cebir Denklem tau_def ve r_def'ten doğrudan çıkıyor. log T_ij = α_i + log w_j + s_ij biçiminde bir kaynak ana etkisi varsa log τ̄_ij = ½(α_i + α_j) + s_ij ve r_ij = α_i − α_j olur. Bu durumda G = Δα + Δs ve q = (½Δα + Δs)/(Δα + Δs) bulunur. Saf bir kaynak etkisi (Δs = 0) q = 0.5 verir. Bu, K-a'nın sıfır hipotezinin neden q ≤ 0.50 olduğunu açıklıyor (tab:registry), ama metin bunu hiçbir yerde söylemiyor. Önerme 1(c) yalnız simetrik terimlerin r'den düştüğünü veriyor; tersini, yani w dışındaki model ana etkilerinin (Adam'ın gradyan normu, Zhang'ın düzgünlüğü) yarısının τ̄'ya girdiğini vermiyor. Benzemezliğe düşen pay 2q − 1'dir: CIFAR-10'da 0.872, CIFAR-100'de 0.680 (FÖY 1587, 1838; türetilmiş). Manşet bu düzeltmeyle de ayakta kalıyor. Kaynak zayıflığına karşı en güçlü kanıt aslında K-c'de: ViT tohumları arasında log τ̄ −0.443, ResNet tohumları arasında −0.489 (FÖY 1595). Düşük bir α_V, ViT ile ViT arasındaki τ̄'yı da düşürürdü; makale bu argümanı kullanmıyor.

Duzeltme: Önerme 1'e (d) maddesi eklenmeli: "a source main effect α loads fully onto r as a potential and half onto log τ̄; a pure source effect gives q = 0.5". K-a'nın 0.50 eşiği bu gerekçeyle açıklanmalı. Metinde q yanında 2q − 1 "dissimilarity share" olarak verilmeli; bunun için föye türetilmiş satır eklenmeli. σ'nın tanımına "includes half of any model main effect not captured by w" kaydı konmalı. K-c paragrafına (04:151) ViT ile ViT arasındaki benzerliğin genel bir kaynak zayıflığını neden dışladığı bir cümleyle yazılmalı.

### 6. [sari] Gradyan hizalanması için "necessary condition" iddiası kanıtlanmamış ve makalenin kendi verisi bir karşı örnek içeriyor

Dosya: paper/manuscript/main.tex:117; sections/03_methodology.tex:260; sections/04_experiments.tex:445, 480; sections/05_discussion.tex:21, 72; sections/06_conclusion.tex:14

Ifade: "input-gradient cosine, a necessary condition for similar transfer, tracks similarity on three datasets" (özet); "Alignment at one clean point is a necessary condition for similar transfer" (03:260, 04:445, 06:14).

Kanit: Gereklilik iddiası için ne türetme ne atıf veriliyor. Yüksek bir Spearman korelasyonu gerekliliği sınamaz; gereklilik "düşük c ise düşük τ̄" demektir. ImageNetV2'de IN_Salman2020Do_R18 ile R50 çiftinin kosinüsü 0.0034, ama log τ̄ değeri −0.936 ve bu, R18'in en yüksek benzerliklerinden biri (11_sonuc_b8_b10.md satır 230, 369). GPU denetimi değerin gerçek olduğunu doğruladı (13_b10_r18_r50_denetimi.md §5-6). Makale bu çifti 04:445'te "genuine" diye anıyor ve alçak frekanslarda hizalı olduklarını söylüyor. Böylece ölçülen c_ij sıfıra yakınken transfer benzerliği yüksek kalabiliyor; bu da "necessary condition" ifadesini c_ij ölçüsü için çürütüyor. EK §9 satır 200'deki "bir mekanizmanın gerekli koşulu" ifadesi bir ön kayıt nitelemesiydi, kanıtlanmış bir önerme değildi.

Duzeltme: İfade her geçtiği yerde (özet, 03, 04 altyazısı, 05, 06) "a correlate" ya da "a first-order proxy" ile değiştirilmeli, örneğin: "tracks similarity on three datasets, also after main effects are removed; it is a clean-point correlate, not a mechanism". R18-R50 çifti sınırlılıklarda açıkça karşı örnek olarak verilmeli: enerji ağırlıklı kosinüs, yüksek frekans bandında sönümlenip transfer benzerliğini gizleyebiliyor. Gereklilik dili korunacaksa birinci dereceden bir Taylor argümanı koşullarıyla birlikte yazılmalı ve bu karşı örnekle uzlaştırılmalıdır.

### 7. [sari] Panel seçimi: "CNN paneli" büyük ölçüde ResNet-18 paneli; ResNet'in σ üstünlüğünün bir kısmı mimari özdeşlik olabilir

Dosya: paper/manuscript/sections/03_methodology.tex:238; sections/04_experiments.tex:145-151, 499

Ifade: "a fixed panel of seven robust CNNs" (özet); "A symmetric dissimilarity carries the ViT's weak-source appearance against robust CNNs on both CIFAR datasets and on every scale and panel tested" (04:499).

Kanit: Yedi üyenin dördü (PreAct)ResNet-18: Wong2020Fast PRN-18, Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm (03:238; tab:external_pool "Wong2020 PRN-18"). Karşılaştırılan iki CNN de ResNet-18 (R32 ve R224). Duyarlılıklar yalnız tek üye çıkaran jackknife'ı içeriyor (q 0.931-0.941, H1 −0.376 ile −0.346; FÖY 1605, 1554); aile düzeyinde bir dışlama yok. Havuzdaki tek dikkat tabanlı model XCiT-S12, σ'da CNN'lerin arasında duruyor (−0.609; 04:74). Bu, benzemezliğin "dönüştürücü ailesi" değil, bu ViT-Tiny yapılandırmasına özgü olabileceğini düşündürüyor.

Duzeltme: Mevcut matrislerden GPU gerektirmeden bir masa duyarlılığı üretilmeli. Bütün ResNet-18 türevleri panelden çıkarılır; kalan üç üyelik panel Engstrom RN-50, Carmon WRN-28-10 ve Gowal WRN-28-10'dur. Bu panelde q, ρ(V-scr) ve H1 yeniden hesaplanır ve keşifsel etiketle raporlanır. Metinde "robust CNNs" yerine "a panel of robust ResNet and WideResNet models" yazılmalı. 04:499'daki genelleme "for this ViT-Tiny" ile sınırlanmalı.

### 8. [sari] İlgili çalışmalar: Demontis ve ark. iki etkenli diye özetlenmiş, kaynak tarafındaki üçüncü etken düşmüş; Awad atfı ters bağlamda kullanılmış

Dosya: paper/manuscript/sections/02_related_work.tex:35, 37; sections/03_methodology.tex:193; sections/05_discussion.tex:21, 68

Ifade: "Demontis et al. trace transferability to the intrinsic vulnerability of the target ... and to the alignment between the input gradients of surrogate and target" (02:35); "close to the split of Demontis et al. into target vulnerability and symmetric alignment" (03:193); "The decomposition separates the two factors that Demontis et al. call target vulnerability and gradient alignment" (05:21); "which fits the report that robust surrogates transfer better~\cite{awad2025defense}" (05:21).

Kanit: Yazarların kendi tam metin notu (raporlar/konsey_2026-10-29/02_literatur.md:57) Demontis'in üç terimini sayıyor: hedef gradyan büyüklüğü, kosinüs hizalaması ve "vekil kaybının değişkenliği", yani vekil karmaşıklığı. Aynı not "T_ij = w_j τ_ij ... vekil karmaşıklığı terimi atılmış hâlidir" diyor. Atlanan terim, manşetin çürüttüğünü söylediği kaynak etkisinin ta kendisi. Bu terim makalenin ayrışımında r'ye ve yarı yarıya τ̄'ya dağılıyor (bkz. q ve σ bulgusu). Awad ve ark. ile Springer ve ark.'nın "robust surrogates transfer better" bulgusu bir kaynak niteliği etkisidir (Zhang 2307.07873'teki düzgünlük terimi); "similarity accounts for most of the deficit" cümlesini desteklemez, onun rakibidir. 02:37'deki yenilik cümlesi ("we did not find a study that separates ... vulnerability, a similarity ... and a directional remainder") 29.10 taramasına dayanıyor ve kabul edilebilir. Ancak Demontis'in hedef, simetrik ve kaynak terimlerinden oluşan üçlü çerçevesiyle yan yana konmadığı için yenilik olduğundan büyük görünüyor.

Duzeltme: 02:35, 03:193, 05:21 ve 05:68'de Demontis üç terimiyle anılmalı. Yazılması gereken şudur: "their surrogate-complexity term has no separate slot here: a source main effect enters r as a potential and half of log τ̄". 05:21'deki Awad cümlesi "in contrast to source-quality effects such as the better transfer of robust surrogates [awad, springer, zhang2024], which our ρ bounds on this panel" biçimine çevrilmeli. 02:37'nin sonuna farkı söyleyen bir yan cümle eklenmeli: ayrışım, ölçülmüş oranlar üzerinde parametresiz bir özdeşliktir ve hedef terimi ölçülmüş bir değere sabitlenmiştir.

### 9. [yesil] Logit ölçekte H3 için "reverses in the same way" ifadesi 04:230 ile çelişiyor

Dosya: paper/manuscript/sections/04_experiments.tex:494

Ifade: "The sign reverses: ... on the logit scale it is the directionally stronger one by a margin far outside the ±0.10 band. H3 reverses in the same way."

Kanit: H3 logit ölçekte −0.087 [−0.110, −0.064] ve nokta kestirimi bandın içinde. 04:230 bunu "the registered rule would return neither support nor refutation" diye okuyor (FÖY 1551). Bu yüzden ρ(V-scr) ile "aynı biçimde" dönmüyor: ρ(V-scr) −0.304 ile bandın çok dışında (FÖY 1603).

Duzeltme: Şöyle yazılmalı: "H3 changes sign as well (−0.087), but stays inside the band, where the registered rule would be undecided".

### 10. [yesil] SVHN'deki çift asimetrisi yönlü terimin veri kümesine bağlılığına kanıt diye kullanılmış

Dosya: paper/manuscript/sections/04_experiments.tex:155

Ifade: "The directional term depends on the dataset: it is large on CIFAR-100, and on SVHN, where no panel was run, even the pair's target-correct asymmetry reverses sign"

Kanit: Hedef-doğru asimetri puan ölçeğindedir ve potansiyel bileşeni de içerir; yönlü terim ρ ya da r değildir. SVHN'de temiz fark yalnız 1.94 ve 1.74 puan (04:537), dolayısıyla işaretin dönmesi kırılganlık farkının kapanmasından da gelebilir. Yazım kararı brif §2'den geliyor, ama mantık bağı kuruluyor.

Duzeltme: "and on SVHN, where no panel was run, the pair's target-correct asymmetry itself changes sign at matched clean accuracy (Section IV-I)" biçiminde, yönlü terime kanıt olarak değil bağlam olarak verilmeli.

### 11. [yesil] Tartışmanın ilk cümleleri ölçek ve veri kümesi kaydından önce genelleniyor

Dosya: paper/manuscript/sections/05_discussion.tex:19, 21

Ifade: "once each target's white-box vulnerability is divided out, panel examples transfer into the ViT about as poorly as its own examples transfer out"; "A black-box score measured on a ViT with CNN surrogates therefore reflects dissimilarity along with vulnerability, and the surrogate family belongs in the report."

Kanit: İlk cümle K-b'nin CIFAR-10, log ölçek ve CNN paneli sonucudur; CIFAR-100'de ρ +0.143, logitte −0.304 (FÖY 1839, 1603) ve kayıt iki cümle sonra geliyor. İkinci cümle tek bir ViT-Tiny yapılandırmasından bütün ViT hedeflerine genelliyor (bkz. kırmızı bulgu).

Duzeltme: İlk cümleye "on CIFAR-10 and the log scale" eklenmeli. İkinci cümle "for a scratch-trained ViT-Tiny like ours, a black-box score ..." diye daraltılmalı.

### 12. [yesil] Tez uzlaşması paragrafı iç tutarlı, ama ölçek, r_RV büyüklüğü ve tezdeki AS1 yanıtıyla bağı eksik

Dosya: paper/manuscript/sections/05_discussion.tex:33; sections/01_introduction.tex:48

Ifade: "An additive fit with the WideResNet reference places the pair's asymmetry on the source ... with a single ViT in the family design the within-family similarity loads jointly onto the ViT's source and target effects, so dissimilarity is booked as a weak source."

Kanit: Önerme 1(b) ℓ = log T üzerinde kurulmuş (03:219); +5.13/−2.03 toplamsal uyumu ise puan ölçeğinde (04:66; FÖY 390). Cebir her toplamsal ölçekte geçerli, ama bu söylenmiyor. Paragraf r_RV = +0.115'in δ'yı aştığını yazmıyor (bkz. asimetri ile kaynak açığı bulgusu). Tez notu (TEZ_OTURUMUNDAN_NOT_2026-10-31.md §2) tezin AS1 yanıtında asimetrinin yönünü temiz doğruluk farkına bağladığını kaydediyor. Makale ise yönün yarısını w'ye (doğru sınıflanan örneklere koşullu kırılganlık), yarısını çifte özgü r'ye veriyor. 01:48'deki "the direction of the asymmetry is not stable once the architectures are matched in clean accuracy" düzeltmesinin dayanağı (SVHN, 04:537; S4 ImageNet satırı −1.28/+0.78, FÖY 1577-1578) giriş paragrafında gösterilmiyor.

Duzeltme: 05:33'e "Proposition 1(b) holds on any additive scale, including the points scale of that fit" ve "a residual of +0.115, above the margin" eklenmeli. 01:48'deki düzeltme cümlesine Section IV-I ve tab:pair_decomposition göndermesi konmalı. Tez tarafının bir sonraki turunda AS1 yanıtı "yönün yaklaşık yarısı hedef kırılganlığıdır, temiz doğruluk eşleşince yön kararsızlaşır" diye bu iki kanıtla hizalanmalı.

### 13. [yesil] Özetteki "pre-registered" vurgusu, hangi sınamaların gerçekten örneklem dışı olduğunu ayırmıyor

Dosya: paper/manuscript/main.tex:117; sections/03_methodology.tex:328

Ifade: "testing pre-registered predictions with three seeds"

Kanit: 03:328 açıkça yazıyor: CIFAR-10 panel öngörüleri ilk tohumun (masa q 0.928, FÖY 1729) iki tohuma ve yedi üyeye taşınmasıdır. H1 öngörüsü de σ farkı bilinerek yazılmıştır (ON_KAYIT §1, sahte H1 −0.335). Gerçekten örneklem dışı olanlar şunlar: üç yeni hücre (H2, H3 ve H1'in R224 köprüsü), CIFAR-100, ImageNetV2 ve gradyan ailesi.

Duzeltme: Özetteki yan cümle "pre-registered predictions, of which the new two-by-two cells, CIFAR-100, ImageNetV2 and gradient tests are out of sample" diye kısaltılarak verilebilir; ya da giriş 01:19'a bu ayrımı yapan tek bir cümle eklenir.

### 14. [yesil] ViT-Tiny parametre sayısı yanlış (5.7M); ölçülen değer 5.53M

Dosya: paper/manuscript/sections/03_methodology.tex:52; sections/04_experiments.tex:43-44

Ifade: "ViT-Tiny (vit_tiny_patch16_224 in timm; 5.7M parameters ...)" ve Tablo I'de "5.7M"

Kanit: raporlar/konsey_2026-10-29/_ek_flop_olcumu.json, modeller.c1_vit_tiny.param_M = 5.53 (on sınıflı başlık); 5.7M timm'in bin sınıflı ImageNet başlığına ait. ResNet-18 için 11.17 ile 11.2M tutarlı. Tez bu sayıyı 31.10'da düzeltti (TEZ_OTURUMUNDAN_NOT_2026-10-31.md §3).

Duzeltme: Her iki yerde 5.5M yazılmalı. Kaynak yorumu CLAUDE.md'den _ek_flop_olcumu.json'a çevrilmeli; gerekiyorsa sayı föye eklenmeli.

### 15. [yesil] CIFAR-100 bloğu için "involved no training" ifadesi belirsiz

Dosya: paper/manuscript/sections/04z_computational.tex:15

Ifade: "The CIFAR-100, ImageNetV2 and gradient blocks involved no training."

Kanit: CIFAR-100 çifti eğitilmiştir, yalnız daha önceki bir kampanyada (03:240 "selected under the single-split rule used when they were trained"; aynı paragrafın ilk cümlesi CIFAR-100 kampanyasının RTX 5090'da koştuğunu söylüyor).

Duzeltme: "The registered CIFAR-100, ImageNetV2 and gradient blocks reused existing checkpoints and trained no new model."

### 16. [yesil] Mahmood yön farkı için önerilen aday açıklama ölçeğe bağlı

Dosya: paper/manuscript/sections/05_discussion.tex:38

Ifade: "in our design ImageNet initialization both moves the ViT toward the CNN panel and gives it a negative directional term"

Kanit: V-IN'in ρ'su −0.118 (n = 2, S2 keşifsel; FÖY 1497, 1563). Logit ölçekte sıfırdan eğitilmiş ViT'nin ρ'su zaten −0.304 (FÖY 1603); başlatma olmadan da "negatif yönlü terim" logit ölçekte var. Aday açıklama ayrıca Mahmood'un puan ölçeğindeki her-ikisi-doğru asimetrisiyle karşılaştırılıyor.

Duzeltme: "on the log scale" kaydı ve S2'nin keşifsel olduğu bir yan cümleyle eklenmeli; "one candidate" dili korunmalı.

## Guclu yanlar

- Ön kayıt disiplini Q1 düzeyinin üstünde. Dondurma tarihleri ve SHA-256 özetleri föy kayıtlarıyla eşleşiyor (FÖY M9.8:1684-1686, M10.6). Kayıttan önce görülmüş veri satır satır beyan edilmiş (03:328), sonradan gevşetilen iki kural adıyla anılmış ve üretilmeyen duyarlılıklar listelenmiş (03:330).
- Olumsuz sonuçlar saklanmamış. CIFAR-100'de K-b çürütüldü, logit ölçekte yönlü terim büyük ve negatif, Liu çifti "uncertain", yörüngelerde log oran yasası tutmadı (R² 0.201) ve önceki sürümün yön iddiası düzeltildi; bunların hepsi özette ya da gövdede açıkça yer alıyor.
- Simetrik payın büyük olması sağlam bir bulgu. Log, logit ve oran ölçeklerinin hepsinde, tek üye çıkaran panel jackknife'ında (0.931-0.941), δ = 0.06'da, ikincil XCiT panelinde ve iki CIFAR veri kümesinde tutuyor. Föyden tohum başına yeniden hesapladığım q değerleri (0.368/0.391, 0.360/0.387, 0.367/0.390) metindeki 0.936 ortalamasıyla uyuşuyor.
- Tanımlanabilirlik önermesi (Proposition 1) iki modelli ve tek ViT'li tasarımlarda kaynak etkisi okumasının neden tanımlanamadığını kısa ve doğru gösteriyor. Bu, alandaki birçok transfer karşılaştırmasına uygulanabilecek yöntemsel bir katkı.
- R224-scr köprü hücresi giriş çözünürlüğü ve girdi hattı itirazını ikna edici biçimde kapatıyor. σ(R224-scr) − σ(R32) = −0.0003 [−0.035, +0.034] (S1, FÖY 1561), yani 224'e büyütülmüş hat ResNet-18'in panele benzerliğini değiştirmiyor.
- Giriş ve sonuçtaki sınır paragrafları, ImageNetV2'nin betimsel tutulması ve 04:238'deki karıştırıcı kabulü dürüst ve ölçülü. H1, H2 ve H3 sayıları föyle birebir uyuşuyor; A^σ, I^σ ve A^ρ'yı hücre ortalamalarından yeniden hesapladım (−0.364, +0.260, +0.003).
- Protokol katmanı toplam olasılık özdeşliğine ve ölçülmüş p öncülüne dayanıyor (en küçük p 0.989, h ölçeğinde |g| ≤ 0.0044). Raporlama gereklilikleri bu yüzden uygulanabilir ve kanıta bağlı.
- Veri ve kod paylaşımı örnek bazında kayıtları, dondurulmuş betiği ve hücre tablolarını kapsıyor; bütün sayılar yeniden eğitim gerektirmeden yeniden üretilebilir.
