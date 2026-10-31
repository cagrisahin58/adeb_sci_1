# Makale revizyon brifi: O1 manşetine göre EN metnin yeniden yazımı (31.10.2026)

Hazırlayan: makale yazarı (opus), yalnız planlama turu. Bu dosya dört yazar ajanın (Y1-Y4) ve şekil ajanının tek bağlamıdır; ajanlar sohbeti görmez. Dosya hiçbir makale dosyasını değiştirmez. Sayılar makaleye gireceği biçimde, ondalık noktayla yazılmıştır. FÖY = `results/C1_REFERANS_FOYU.md`; "FÖY:1526" o dosyanın 1526. satırıdır (31.10.2026 sürümü; M9 satır 1437-1779, M10 satır 1780-2042). ÖK = `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md`; EK = `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md`; PLAN = `raporlar/konsey_2026-10-29/KONSEY_PLANI.md`; R09 = `09_sonuc_b2_b6.md`; R11 = `11_sonuc_b8_b10.md` (ikisi de aynı klasörde). Depo kökü WSL'de `/home/firat/projects/adeb_sci_1`, Windows'tan `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1`.

En önemli üç nokta şunlardır. Birincisi, makalenin omurgası değişmektedir: bugünkü metin "koşullama kümesi sonucu belirler" ve "yön ViT'nin kaynak etkisidir" okumalarını taşır; yeni metin ön kayıtlı O1 bölgesini taşır (ViT'nin zayıf kaynak görünümü simetrik ve mimariye ait benzemezliktir; ImageNet başlatması bu benzemezliği ViT'de ResNet'tekinden fazla azaltır; asimetri hedef kırılganlığı ve küçük bir yönlü terimle taşınır) ve protokol çalışması dördüncü katkı olarak ölçüm katmanına iner. İkincisi, iddia dar bir sınırla yazılır: "küçük, mimariden bağımsız yönlü terim" yalnız log ölçekte, CNN panelinde ve CIFAR-10'da geçerlidir; CIFAR-100'de K-b çürütülmüştür, logit ölçekte yönlü terimin işareti döner, ImageNetV2 betimseldir, gradyan hizalanması gerekli koşuldur. Üçüncüsü, föyde bulunmayan bir dizi türetilmiş sayı (hücre farkları, masa Hodge ayrışımı, R11 §7 keşifsel değerleri, koşu süreleri) metne giremez; liste §9'dadır ve yazarlar bunları yeniden hesaplayıp yazmaz.

## 1. Başlık ve özet planı

### 1.1 Başlık

PLAN §9'daki O1 başlığı: "Not a Weak Source but a Different One: Vulnerability, Similarity and Direction in CNN-to-ViT Adversarial Transfer under an Architecture × Initialisation Design".

Karar: başlık bu yapıyla korunur, yalnız üç yazım düzeltmesi yapılır ve kelime kısaltması yapılmaz. Kullanılacak biçim (`main.tex` satır 62-64'ün yerine):

```latex
\title{Not a Weak Source but a Different One: Vulnerability, Similarity
and Direction in CNN-ViT Adversarial Transfer under an
Architecture-by-Initialization Design}
```

Gerekçeler şunlardır. "Initialisation" İngiliz imlasıdır, makale ABD imlasıyla yazılır. "CNN-to-ViT" tek yön çağrıştırır, oysa iddia ViT'nin CNN'lere kaynak olarak gücü ve iki yönün ayrışımı üzerinedir; "CNN-ViT" iki yönü kapsar. "×" işareti IEEE meta verisinde ve PDF yer imlerinde bozulabilir; "-by-" aynı anlamı taşır. Kısaltma gerekirse (editör isteği) son dört kelime ("under an Architecture-by-Initialization Design") atılır ve tasarım özetin ikinci cümlesine taşınır; başka bir kısaltma yapılmaz, çünkü "Vulnerability, Similarity and Direction" ayrışımın üç bileşeninin adıdır.

### 1.2 Özet (`main.tex` satır 107-109; sınır 250 kelime, `check_abstract_body.py`)

Özet sekiz cümlelik bir plandır. 1-6. cümleler zorunludur; kelime sınırı aşılırsa 7. cümlenin gradyan yarısı ya da 8. cümle kısaltılır, 6. cümle (iddianın sınırı) asla atılmaz. Özete giren her sayı gövdede de geçmelidir.

| Sıra | İçerik | Sayılar | FÖY |
|---|---|---|---|
| 1 | Soru: çekişmeli eğitilmiş ViT'ler CNN'lere karşı zayıf transfer kaynağı görünür; iki modelle bu asimetrinin kaynak ve hedef payına bölünmesi tanımlanamaz | yok | yok |
| 2 | Yöntem: hedef-doğru transfer oranı log ölçekte hedefin beyaz kutu kırılganlığı w, simetrik çift benzerliği τ̄ ve yönlü artık r olarak ayrışır; bunlar yedi gürbüz CNN'lik sabit bir panel üzerinden ortalanır; öngörüler önceden kaydedilmiş, model başına üç tohum | "seven", "three" | 1741 (panel 7), 1593 (üç çift) |
| 3 | B2: ViT-Tiny'nin ResNet-18'e göre panel kaynak açığının 0.936'sı simetriktir (%90 0.925-0.948); ViT'nin yönlü terimi ±0.10 içinde sıfıra eşdeğerdir (ρ = +0.012); ViT tohumları birbirine panelden çok benzer (Δ_seed = +0.566) | 0.936, 0.925, 0.948, +0.012, +0.566 | 1587, 1588, 1589 |
| 4 | 2x2: girdi hattı ve AT tarifi eşitlenmiş mimari × başlatma tasarımında sıfırdan eğitilmiş ViT panele ResNet'ten az benzer (A^σ_scr = −0.364, %90 −0.415 ile −0.314), ImageNet başlatması bu farkı ViT'de daha çok kapatır (I^σ = +0.260, %90 0.186-0.335), yönlü terimin mimari etkisi sıfıra eşdeğerdir (A^ρ = +0.003) | −0.364, −0.415, −0.314, +0.260, 0.186, 0.335, +0.003 | 1526, 1527, 1528 |
| 5 | Saldırı tarafı ve maskeleme: açık her kaynağın en iyi saldırısı altında (TGR dahil) korunur, korunma oranı 0.960 (%90 0.941-0.976); AutoAttack hiçbir yeni modeli maskeleme şüphesiyle işaretlemez (PGD-10 ile AA farkı 3.20-7.40 puan) | 0.960, 0.941, 0.976, 3.20, 7.40 | 1624, 1625, 1673 |
| 6 | İddianın sınırı: CIFAR-100'de simetrik pay (0.840) ve tohum benzerliği yinelenir, ama ViT'nin yönlü terimi küçük kalmaz (+0.143) ve logit ölçekte yönlü terimlerin işareti döner; "küçük yönlü terim" CIFAR-10 ve log ölçekle sınırlıdır | 0.840, +0.143 | 1838, 1839; logit için 1603 (sayı özete zorunlu değil) |
| 7 | Dış geçerlilik: ImageNetV2'de temiz modelden başlatılmış, aynı tarifli iki CNN-dönüştürücü çiftinde dönüştürücü panele betimsel olarak daha az benzer (Ā^σ_IN = −0.142, %90 −0.197 ile −0.090); girdi gradyanı kosinüsü üç veri kümesinde, model ana etkileri ayıklandıktan sonra da log τ̄'yı öngörür (Spearman 0.893-0.944) | −0.142, −0.197, −0.090, 0.893, 0.944 | 1938; 1971, 1973, 1975 |
| 8 | Protokol katmanı: koşullama protokolü aynı modellerde asimetriyi 4.36 ile 19.37 puan arasında taşır; h = −log(1 − T) ölçeğinde ham ile hedef-doğru oranlar yalnız hedef potansiyelinde ayrılır (en büyük ayar terimi 0.0044) | 4.36, 19.37, 0.0044 | 160, 162, 1764 |

Özette "O1", "B2", "K-a", "H1" gibi iç etiketler, "first", "to our knowledge" ve "we show that" kalıbı kullanılmaz. Anahtar kelimeler (`main.tex` 111-113) şöyle güncellenir: Adversarial robustness, transfer attacks, transferability, Vision Transformer, convolutional neural networks, pre-registration, evaluation methodology.

## 2. Manşet iddiasının sınırı

Önceden yazılmış O1 manşeti (ÖK §6, satır 100) iddianın üst sınırıdır; metin bunun ötesine geçemez, R09 §7 ve R11 §8'in nitelemeleriyle daralır. Aşağıdaki tablo her iddia parçası için söylenebileni, söylenemeyeni ve dayanağı verir.

| İddia parçası | Söylenebilir | Söylenemez | Dayanak |
|---|---|---|---|
| Simetrik pay | CIFAR-10'da ViT-Tiny'nin panel kaynak açığının büyük kısmı simetrik benzemezliktir (q 0.936); log, logit ve oran ölçeklerinde q 0.84'ün üzerindedir; CIFAR-100'de yinelenir (0.840) | "Açığın tamamı simetriktir" (logit q 1.101 yönlü payın açığı küçülttüğünü gösterir; bu ölçeğe bağlı bir ayrıntıdır) | FÖY 1587, 1603, 1604, 1838, 1857 |
| Mimariye ait benzemezlik | Girdi hattı eşitlenmiş sıfırdan eğitimde ViT-Tiny, ResNet-18'den daha az panel benzerliği taşır (H1 destek; log, logit, oran, Welch, jackknife, hiyerarşik bootstrap altında yön korunur) | "Dikkat mekanizması nedendir" (karşıtlık mimari paketinin bütünüdür: yama gövdesi, dikkat, parametre sayısı); "temiz doğruluktan bağımsızdır" (V-scr temiz doğruluğu 73.53, R224-scr 85.73; aynı hücrede birlikte değişir) | FÖY 1526, 1550-1555, 1496, 1498 |
| Başlatma etkileşimi | ImageNet başlatması σ'yı ViT'de ResNet'tekinden çok yükseltir (H2 destek, logit ölçekte de pozitif +0.354) | "Normalizasyonun etkisi"; başlatma etmeni ağırlık, temiz aşama uzunluğu ve normalizasyon demetidir, ayrı etkileri tanımlanamaz | FÖY 1527, 1534; ÖK §3 |
| Yönlü terim | Log ölçekte, CNN panelinde, CIFAR-10'da ViT'nin yönlü terimi ±0.10 içinde eşdeğerdir (K-b) ve yönlü terimin mimari ana etkisi eşdeğerdir (H3) | "Yönlü terim her ölçekte küçüktür" (logit H3 −0.087, %95 aralık sıfırı dışlar, ön kayıt kuralı bu ölçekte kararsız verirdi; oran ölçeğinde −4.13 puan); "her hücrede küçüktür" (V-IN ρ ortalaması −0.118, δ dışında); "her veri kümesinde küçüktür" (CIFAR-100 +0.143, çürütüldü); "her panelde küçüktür" (XCiT ikincil panelinde ρ(V-scr) +0.198 ile +0.204) | FÖY 1528, 1551, 1552, 1497, 1839, 1606 |
| Hücrede n | Yeni üç hücrede iki koşu, V-scr'de üç; çıkarım birimi eğitim koşusudur, birleşik varyans df 5 | Hücre içi değişkenlik iyi kestirilmiştir; Welch df 1.10-1.95'tir ve aralıklar genişler (H1 Welch %95 −0.569 ile −0.160, sıfırı yine dışlar) | FÖY 1553, 1532 |
| Ölçek | CIFAR ölçeğinde, ViT-Tiny ve ResNet-18 ile | ImageNet ölçeğinde sıfırdan satırında aynı büyüklük (tek Liu çifti −0.055, "belirsiz"); "transformer ailesi" genellemesi | FÖY 1939 |
| B8 (ImageNetV2) | Betimsel, keşifsel, "IN satırının doğal ölçekteki karşılığı"; Ā^σ_IN −0.142 "beklentiyle uyumlu" etiketi taşır | "destek", "çürütüldü", "doğrular", "yineler"; 2x2'nin sınaması değildir; dondurulmuş betiğin B8 çıktısındaki p ve Holm değerleri karar diliyle anılmaz | EK §5.6, §11; FÖY 1903, 1938, 1945 |
| B9 (CIFAR-100) | Bağlayıcı yineleme: K-a ve K-c destek, K-b çürütüldü (pozitif yön); EK §11'in iki önceden yazılmış cümlesi girer | K-b(B9) sonucunu "kararsız" ya da "küçük" diye yumuşatmak; ViT-Tiny'nin CIFAR-100 temiz doğruluğu 41.94-44.06 olduğundan B9 ViT nicelikleri temiz doğrulukla karışabilir, bu sınırlılık yazılmadan B9 cümlesi kurulmaz | FÖY 1838-1846, 1876-1878 |
| B10 (gradyan) | Simetrik terim, model düzeyi ana etkiler ayrıldıktan sonra da transferden ve saldırıdan bağımsız ölçülen girdi gradyanı hizalanmasıyla öngörülür (Zhang ve ark.'nın gradyan benzerliği tanımıyla); altı sınamanın altısı destek | "Mekanizma gösterilmiştir"; c_ij temiz görüntüde tek noktadaki hizalanmadır, gerekli koşuldur, yeterli kanıt değildir; kısmi istatistik çarpımsal ya da etkileşimli model etkilerini ayırmaz | EK §9, §11; FÖY 1983-1990 |
| B5 (saldırı tarafı) | Açık her kaynağın en iyi izinli saldırısı altında korunur (0.960); TGR hiçbir ViT kaynağında seçilmemiştir, PGD-10'dan zayıf transfer eder | "ViT'ye özgü saldırılar genel olarak işe yaramaz" (TGR yalnız kaynağındaki ayarla, uyarlanmış biçimde koşulmuştur); IN çiftinde korunma oranı (G_PGD 0.072, eşik altı, oran yorumlanmaz) | FÖY 1620-1655 |
| B6 | Altı yeni modelde PGD-10 ile AA farkı 10 puanlık eşiğin altında, maskeleme işareti yok | V-scr ve R32 için B6 kuralı tanımlanmamıştır; C1 AA değerleri farklı örneklemdedir | FÖY 1673, 1517 |
| Yenilik | Ayrışımın kendisi Caussinus yarı-simetri modeline, Demontis ve Adam'ın çerçevelerine yakındır; içerik ölçülen büyüklüklerde ve müdahale yanıtındadır | "ilk kez", "bildiğimiz kadarıyla", "novel decomposition" | ÖK §6 son cümle; PLAN §3 |
| Ayrışım bir özdeşliktir | log T = log w + log τ̄ + ½r bir muhasebe özdeşliğidir ve öyle yazılır | Özdeşliğin kendisini bulgu gibi sunmak | PLAN §1 |
| Yörüngeler | Çarpımsal yasa yörünge noktalarında tutmamıştır (R²(λ = 1) 0.201); yasa iddiası bırakılmıştır, bu bir ölçüm sınırı olarak yazılır | Yasa iddiası | FÖY 1759 |

Önceden yazılmış ek cümleler (EK §11) metne birebir anlamıyla girer: "ViT'nin kaynak açığının simetrik payla taşınması ve ViT tohumlarının birbirine panelden çok benzemesi CIFAR-100'de üç tohumla yinelenir"; "Yönlü terim veri kümesine bağlıdır; 'küçük yönlü terim' cümlesi CIFAR-10 ile sınırlanır"; Ā^σ_IN için "beklentiyle uyumlu" cümlesi; Liu satırı için "belirsiz" cümlesi; F_B10 için "en az iki veri kümesinde H10k destek" cümlesi. Karar: K-b(B9) cümlesindeki "SVHN'de ters işaretli" yan cümlesi r değeriyle değil, föyde bulunan SVHN hedef-doğru asimetrisinin ters işaretiyle (−1.16 ve −0.85 puan, FÖY 185) yazılır, çünkü SVHN'deki r_RV değerleri (−0.106, −0.076) föyde yoktur (R11 §6 bu bağlantıyı ister).

## 3. Gösterim ve makrolar

### 3.1 Gösterim tablosu

| Sembol (LaTeX) | Tanım | Ön kayıttaki adı | Not |
|---|---|---|---|
| `T_{ij}` | Kaynak i'den hedef j'ye hedef-doğru koşullu yanıltma oranı (yüzde ya da oran) | T_ij | Protokol katmanında `r_{\text{cond}}` ile aynı niceliktir; o paragrafta bir kez `r_{\text{cond}} = T_{ij}` yazılır |
| `w_j = T_{jj}` | Hedefin beyaz kutu kırılganlığı (hedef-doğru beyaz kutu PGD-10 yanıltma oranı) | w | Tablo I'in koşullu yanıltma sütunuyla aynı nicelik (FÖY 28-29, tam örneklem) |
| `\omega_m = \log w_m` | Model kırılganlığı (log) | ω | Bölünmüş yarı uygulanmaz, tam örneklem w'den |
| `\log\simt_{ij}` | ½[log(T_ij T_ji) − log(w_i w_j)], simetrik çift benzerliği | log τ̄ | Adı: "pairwise similarity"; "transfer efficiency" de olur |
| `r_{ij}` | log(T_ij/T_ji) − log(w_j/w_i), yönlü artık | r | Her zaman alt indisle yazılır; `r_{\text{raw}}`, `r_{\text{cond}}` ile karışmasın diye "directional residual $r_{ij}$" biçimi |
| `\sigma_m` | ort_{c∈P} log τ̄_mc, panel benzerliği | σ | σ standart sapma için kullanılmaz; standart sapma "SD" |
| `\rho_m` | ort_{c∈P} r_cm, yönlü terim; pozitifse m yönlü olarak zayıf kaynaktır | ρ | Spearman korelasyonu ρ ile değil `r_{\mathrm{S}}` ile yazılır |
| `G`, `G_s` | Panel kaynak açığı: ort_c log T(R→c) − ort_c log T(V→c) = (σ_R − σ_V) − ½(ρ_R − ρ_V) | D_s (B2), G_k (B5) | Tek sembol: G; tohum s için G_s; saldırı k için G_k |
| `q_s` | (σ_R − σ_V)/G_s, simetrik oran | q_s | |
| `\Dseed` | ViT tohum çiftleri arası ort log τ̄ − ort_s σ(V_s) | Δ_w | Karar: makalede Δ_w yazılmaz, çünkü w kırılganlık sembolüdür; `\Delta_{\mathrm{seed}}` |
| `\Asig{scr}` | σ(V-scr) − σ(R224-scr) | A^σ_scr (H1) | |
| `\Isig` | [σ(V-IN) − σ(V-scr)] − [σ(R224-IN) − σ(R224-scr)] | I^σ (H2) | |
| `\Arho` | ½{[ρ(V-scr) − ρ(R224-scr)] + [ρ(V-IN) − ρ(R224-IN)]} | A^ρ (H3) | |
| `\Asig{IN}` | B8'de σ(dönüştürücü_k) − σ(CNN_k), iki Singh çiftinin ortalaması `\bar{A}^{\sigma}_{\mathrm{IN}}` | Ā^σ_IN | Yalnız ImageNetV2 bağlamında |
| `L_k(m)` | ort_{c∈P} log T_k(m→c), saldırı k altında panel kaynak gücü | S_k(m) | Karar: S1-S7 etiketleriyle karışmasın diye L |
| `\Gk{PGD}`, `\Gk{best}` | PGD-10 altında ve kaynak başına en iyi saldırı altında G | G_PGD, G_best | Korunma oranı G_best/G_PGD |
| `c_{ij}` | ort_x cos(∇_x L_i(x,y), ∇_x L_j(x,y)), temiz görüntüde girdi gradyanı kosinüsü | c_ij | `L` burada kayıp; metinde kayıp `\mathcal{L}` yazılır ki L_k ile karışmasın |
| `\delta` | Eşdeğerlik sınırı, 0.10 log birimi; duyarlılık 0.06 | δ | Hodge potansiyeli için δ kullanılmaz, "potential share" sözcüğüyle yazılır |
| `h = -\log(1-T)` | Protokol ayarı ölçeği | h | Önerme 2 (eski P3 Önerme 3) |
| K-a, K-b, K-c | Panel ailesi sınamaları (simetrik oran, ViT yönlü terimi, tohum benzerliği) | aynı | Ön kayıttaki etiketler korunur, `tab:registry`'de bir kez açılır |
| H1, H2, H3 | 2x2 ailesi sınamaları | aynı | |
| S1-S7 | 2x2 ikincil (keşifsel) çözümlemeleri | aynı | Metinde "secondary analysis S2" biçimi |
| Aileler | `\mathcal{F}_{\mathrm{panel}}` (B2), `\mathcal{F}_{2\times2}` (B4), `\mathcal{F}_{\mathrm{C100}}` (B9), `\mathcal{F}_{\mathrm{grad}}` (B10) | F_B2, F_B4, F_B9, F_B10 | Blok kimlikleri yalnız `tab:registry` dipnotunda |
| Mantel | Model etiketlerinin c matrisinde ortak permütasyonu, 9999 permütasyon, tek yönlü p | aynı | p = 1e-04 permütasyon tabanıdır (FÖY 1977) |
| Hücre adları | `\cellname{R32}`, `\cellname{V-scr}`, `\cellname{V-IN}`, `\cellname{R224-scr}`, `\cellname{R224-IN}` | C1-R32, V-scr, V-IN, R224-scr, R224-IN | Karar: "C1" iç kampanya adıdır, makalede R32 (32 piksel CIFAR ResNet-18, köprü hücresi) |

Önermeler: P3 dosyasındaki Önerme 1 makalede Proposition 1 (identifiability), Önerme 3 makalede Proposition 2 (h-scale protocol invariance) olur; Önerme 2 (yön yasası) metne önerme olarak girmez, yalnız ölçüm sınırı cümlesiyle (FÖY 1759) anılır. İçerikleri `raporlar/konsey_2026-10-29/01_oneri_P3_kuram_olcum.md` satır 15-27'dedir.

### 3.2 Makrolar

Mevcut makrolar yalnız `\eps` ve `\Linf`'tir (`main.tex` 46-47). Y1 ilk iş olarak `paper/manuscript/macros_konsey.tex` dosyasını yazar ve `main.tex`'te `\newcommand{\Linf}` satırının altına `\input{macros_konsey}` ekler. Öteki yazarlar bu dosya oluşmadan derleme yapmaz (`ls paper/manuscript/macros_konsey.tex` ile denetlenir).

```latex
% macros_konsey.tex (Y1 yazar; baska ajan dokunmaz)
\newcommand{\simt}{\bar{\tau}}
\newcommand{\Asig}[1]{A^{\sigma}_{\mathrm{#1}}}
\newcommand{\Isig}{I^{\sigma}}
\newcommand{\Arho}{A^{\rho}}
\newcommand{\Dseed}{\Delta_{\mathrm{seed}}}
\newcommand{\Gk}[1]{G_{\mathrm{#1}}}
\newcommand{\rS}{r_{\mathrm{S}}}
\newcommand{\cellname}[1]{\mbox{#1}}
```

## 4. Bölüm bölüm değişiklik listesi

Satır numaraları 31.10.2026 dosyalarınındır. "Sil" paragrafın tamamen çıktığını, "yeniden yaz" konusu korunup metnin yeniden kurulduğunu, "koru" en çok üslup ve gönderme düzeltmesini, "taşı" başka dosyaya geçişi anlatır. O1 ile çelişen eski "kaynak etkisi" okumasını taşıyan yerler ÇELİŞKİ diye işaretlenmiştir; bunlar hiçbir biçimde yaşatılmaz.

### 4.1 `main.tex` (Y1)

| Satır | İşlem | Not |
|---|---|---|
| 60-64 | Yeniden yaz | §1.1 başlığı; 60-61'deki eski yorum satırı yerine tarihli yeni yorum |
| 95-108 | Yeniden yaz | §1.2 planı; 108'deki "The direction is a source effect of this ViT-Tiny" cümlesi ÇELİŞKİ. Eski `% REF:` satırları silinir, yerine `% FOY:` satırları |
| 111-113 | Yeniden yaz | §1.2 anahtar kelimeler |
| 122-127 | Ekle | 125'ten sonra `\InputIfFileExists{sections/04z_computational}{}{}`; 127'den sonra `\InputIfFileExists{sections/07_appendix}{}{}` (ek, Data Availability bölümünden önce) |
| 137-139 | Yeniden yaz | Veri kümelerine ImageNetV2 (Recht ve ark.) ve RobustBench CIFAR-100 ile ImageNet modelleri eklenir; açık depo kapsamına ön kayıt dosyaları, dondurulmuş çözümleme betiği ve hücre tabloları eklenir. "about 40 GB" ifadesi föyde olmadığı için sayısız yazılır ("available from the authors on request") |
| 144-147 | Koru | Claude beyanı aynen kalır |
| 160-166 | Koru | |

### 4.2 `sections/01_introduction.tex` (Y1; hedef 1150 kelime)

| Satır | İşlem | Not |
|---|---|---|
| 10 | Koru | Bağlam paragrafı |
| 12 | Yeniden yaz (kısalt) | Literatürdeki çelişki korunur (Bai, Benz, Mahmood, Shao, Naseer); son cümle "a point Section~\ref{sec:discussion} returns to" korunur |
| 14 | Yeniden yaz | Koşullama kümesi çerçevesi gider; yerine soru: ViT'nin "zayıf kaynak" görünümü bir kaynak özelliği mi, benzemezlik mi; iki modelle toplamsal kaynak-hedef bölüşümü tanımlanamaz (Proposition~\ref{prop:identifiability}) |
| 19 | Yeniden yaz | Yaklaşım: C1 çifti (üç tohum, sabit doğrulama bölmesi) korunur; buna sabit yedi üyeli CNN paneli, ayrışım, mimari × başlatma 2x2'si (altı yeni koşu), saldırı tarafı ve maskeleme denetimi, CIFAR-100 bağlayıcı yinelemesi, ImageNetV2 betimsel paneli ve gradyan hizalanması eklenir; hepsi ölçümden önce kaydedilmiştir |
| 21 | Sil | Üç okuma eke taşındı; girişte en çok bir yan cümle |
| 26-29 | Sil, katkı 4'e indir | Protokol duyarlılığı katkısı. 4.36 ve 19.37 (FÖY 160, 162) katkı 4'te kalabilir; 9.21, 11.10, 3.91 girişte yer almaz |
| 31-33 | Sil, katkı 4'e birleştir | p öncülü bir yan cümle: 0.989-1.000 (FÖY 641, 1151-1156) |
| 35-36 | Sil | ÇELİŞKİ: "assigns the asymmetry to the source", "a property of the examples this ViT-Tiny produces" |
| 38-43 | Sil | Eşleşmiş çift öngörüsü; protokol katmanına bir cümleyle iner (Y3 yazar) |
| 45 | Yeniden yaz (1-2 cümle) | Mutlak gürbüzlük CNN lehinedir (37.93 ile 29.14, FÖY 16-17); üç okuma Ek'e gönderilir (`app:behavior`) |
| 47 | Yeniden yaz | ATEEC ön sürümü cümlesi kalır; eklenenler listesi güncellenir (ayrışım, panel, 2x2, ön kayıt, CIFAR-100 ve ImageNetV2 panelleri, gradyan hizalanması); "corrects one claim" cümlesi korunur |
| 52 | Yeniden yaz | Organizasyon tek cümle |

Yeni katkı paragrafları (madde listesi değil, dört düz paragraf; her biri tek soruya yanıt). Katkı 1, tanımlanabilirlik: iki modelli tasarımda asimetri yalnız bir potansiyel farkını tanımlar, tek ViT'li bir ailede aile benzerliği toplamsal kaynak ve hedef terimlerine birlikte yüklenir; sabit bir dış panel ve çarpımsal ayrışım bu terimleri model düzeyinde tanımlanır kılar (sayı yok; eski +5.13/−2.03 bölüşümü yalnız Y3'te bir kez anılır). Katkı 2, ayrışım ve ölçülen büyüklükler: q 0.936 (FÖY 1587), CIFAR-100'de 0.840 (1838); ViT'nin yönlü terimi CIFAR-10'da +0.012 (1588), CIFAR-100'de +0.143 (1839); Δ_seed +0.566 (1589). Katkı 3, 2x2 müdahale: H1 −0.364, H2 +0.260, H3 +0.003 (1526-1528), saldırı tarafında 0.960 (1624), maskeleme yok (1673). Katkı 4, protokol katmanı: dört protokol 4.36-19.37 (160, 162); h ölçeğinde ham ile hedef-doğru yalnız hedef potansiyelinde ayrılır (1764). Katkılardan sonra bir paragraf iddianın sınırını yazar (log ölçek, CNN paneli, CIFAR-10; ImageNetV2 betimsel; gradyan hizalanması gerekli koşul).

### 4.3 `sections/02_related_work.tex` (Y2; hedef 1250 kelime)

Karar: alt bölümler temaya göre dörde iner, çünkü bugünkü II-A ve II-B ders kitabı paragraflarıdır ve yeni manşetle ilgileri yoktur.

| Satır | İşlem | Not |
|---|---|---|
| 14-17 (II-A Attacks) | Sil | FGSM, PGD, AutoAttack tanımları Yöntem'de zaten var; Carlini-Wagner atfı II-D'de tek yan cümle olabilir |
| 22-25 (II-B Defenses) | Sil | AT ve TRADES Yöntem'de anılır; geri kalan atıflar (MART, randomized smoothing, ensemble) bırakılabilir |
| 30-35 (II-C CNN) | Birleştir, kısalt | Yeni II-A'nın 2-3 cümlesi |
| 40-45 (II-D ViT) | Yeniden yaz | Yeni II-A "CNN and ViT robustness": Bai, Bhojanapalli, Shao, Mo, Debenedetti, Jain, Wu; Singh (ImageNet AT, ConvStem) buraya eklenir |
| 50-55 (II-E Transfer) | Yeniden yaz | Yeni II-B "What makes a source and a target": Demontis (hedef kırılganlığı ve gradyan hizalanması), Adam (gradyan normu farkı ve asimetri), Zhang 2307.07873 (gradyan benzerliği, düzgünlük ödünleşimi), Awad (gürbüz vekiller daha iyi aktarır), Naseer, TGR, MIG, Wei, Mahmood (her-ikisi-doğru, düşük CNN-ViT transferi), Liu ARES (ImageNet gürbüz modeller arası transfer ısı haritası), PubDef (kaynak model bazlı döküm); son cümle: bunların hiçbiri hedef kırılganlığını, simetrik benzerliği ve yönlü terimi ayırmaz (taranan çalışmalar için "we did not find", ÖK §6 yenilik kuralı) |
| yeni | Ekle | Yeni II-C "Asymmetric matrices": Caussinus yarı-simetri modeli π_ij = a_i b_j ψ_ij (T_ij = w_j τ_ij onun sütun etkisi ölçülmüş biçimidir); HodgeRank (Jiang) ve Balduzzi'nin potansiyel-dolaşım ayrışımı; Smouse-Long-Sokal kısmi Mantel |
| 53 ve 63-65 (protokol kısmı) | Kısalt | Yeni II-D "Evaluation protocols for transfer": koşullama kümeleri (Liu 2017, Dong, Mahmood, Ravikumar, Zhao), TA-Bench, Yu, Waseda; Carlini 2019 ve Tramèr; TRADES özdeşlik bağlantısı tek cümle |
| 60-63 (Gap) | Yeniden yaz | Ayrı "Research Gap" alt bölümü kalkar; ali2024adversarial (aynı dergi) II-A sonunda korunur |
| 67 | Sil | Üç okuma |

### 4.4 `sections/03_methodology.tex` (Y2; hedef 3000 kelime)

| Satır | İşlem | Not |
|---|---|---|
| 7 | Yeniden yaz | Tasarım özeti: çift, panel, 2x2, ayrışım, ön kayıt |
| 9-18 | Yeniden yaz | `fig:study_overview` yenilenir, yol `../figures/konsey/fig_study_overview.pdf`, altyazı §6.1 |
| 23-33 | Kısalt | Tehdit modeli; ImageNetV2 için ε = 4/255, α = 1/255 eklenir (EK §5.2); ε süpürmesi cümlesi Ek'e |
| 38-47 | Yeniden yaz | Modeller: R32 (CIFAR ResNet-18, 3×3 gövde), ViT-Tiny (timm, 32→224 bilinear), R224 (timm `resnet18`, 7×7 gövde, aynı 32→224 hattı); IN başlatmaları `deit_tiny_patch16_224.fb_in1k` (DeiT) ve `resnet18.a1_in1k` (RSB). `\paragraph{}` başlıkları kalkar (koyu etiket yasağı). ImageNet top-1 değerleri yazılmaz (föyde yok, §9) |
| 52-69 | Kısalt | FGSM denklemi Ek'e; PGD ve AA kalır; MI-PGD-10 (μ = 1.0, α = ε/10) ve TGR (α = 2/255, μ = 1.0, γ = 0.5) B5 saldırıları olarak buraya; 171'deki TGR uyarlama ayrıntıları buraya iki cümleyle |
| 74-82 | Kısalt | Karışık kayıplı AT tanımı ve "not the PGD adversarial training of Madry" cümlesi kalır |
| 87-98 | Koru, genişlet | C1 tarifi; ardından yeni alt bölüm `subsec:design` ve `tab:design` (§5.1) |
| 99-100 | Koru | Önceki çift beyanı (karantina, sayı yok) |
| 105-116 | Kısalt | Metrikler; koşullu oranın `T_{ij}` ile aynı nicelik olduğu bir kez yazılır; 116'daki "for directional claims we take the both-correct rate as the primary estimate" cümlesi yeniden yazılır: ayrışımın birincil protokolü hedef-doğrudur, çünkü w hedef-doğru koşulludur |
| 120-152 | Koru, kısalt | `tab:protocol_masks`, `eq:general_identity`, `eq:raw_identity` ve 152'deki öncül paragrafı korunur (kapı E1, E2, T4); 152'deki `\ref{subsubsec:matrix}` ve `\ref{subsec:external}` gönderileri `subsec:transfer`'e çevrilir; Proposition 2 (h ölçeği) bu paragrafın sonuna eklenir |
| yeni | Ekle | `subsec:decomposition_def`: denklemler (`eq:decomp`, `eq:r_def`, `eq:tau_def`, `eq:panel_def`), G ve q tanımı, Proposition 1 ve kısa kanıtı, `fig:decomposition_schematic` |
| yeni | Ekle | `subsec:panels`: P (yedi üye, adlar ÖK §2), ikincil XCiT-S12, P9 (CIFAR-100, yedi üye ve iki ImageNet ön eğitimli ikincil, EK §4.1), P8 ve çiftler (ImageNetV2, EK §5.3-5.4; Liu çiftinin dolaylı sıfırdan kanıtı); panel üyesinin kendi σ ve ρ'su kendisi çıkarılarak hesaplanır; ortak önişleme BicubicRes256Crop224, normalizasyon RobustBench nesnesinde nasılsa öyle (R11 §6 isteği) |
| yeni | Ekle | `subsec:gradcos_def`: `eq:cij`, ham ve ana etki artıklı Spearman, Mantel permütasyonu, Zhang 2307.07873 öncül |
| 154-182 | Taşı | Gradyan, uzamsal yerellik, belirteç toplama, dikkat ve öznitelik metrikleri Ek A'ya (Y3) taşınır; Y2 bunları siler, Y3 kısaltılmış tanımları `07_appendix.tex`'e yazar |
| 187-192 | Yeniden yaz | `subsec:statistics`: çıkarım birimi eğitim koşusu; bölünmüş yarı kestirimi; birleşik varyans df 5; Holm; δ = 0.10 (dayanağı: havuzdaki 21 çiftte r'nin RMS'i 0.0897; ÖK §5) ve δ = 0.06 duyarlılığı; karar ilkesi (destek Holm sonrası, çürütme ham aralık); `tab:registry`; sonuç haritası. 192'deki "±2 points, fixed before the comparisons" cümlesi ÇELİŞKİ değil ama karantina kaynaklı bir sınırdır (PLAN §2): silinir; SVHN eşdeğerliği için ±1 ve ±3 marjlı TOST yalnız protokol katmanında, kaynağı föy 198 olarak kalır |
| yeni | Ekle | `subsec:prereg`: dondurma (29.10.2026, ek 30.10.2026), SHA-256 özetleri (FÖY 1684-1686, 2022-2027), görülmüş veri beyanı ve notlar (§8.2) |

### 4.5 `sections/04_experiments.tex` (Y3; hedef 7300 kelime) ve yeni `sections/07_appendix.tex` (Y3; hedef 1300 kelime)

Yeni alt bölüm sırası ve kelime payları: IV-A çiftin gürbüzlüğü 350; IV-B toplamsal bölüşümden ayrışıma 700; IV-C panel sınamaları 1100; IV-D 2x2 1400; IV-E saldırı tarafı ve maskeleme 450; IV-F ImageNetV2 700; IV-G gradyan hizalanması 550; IV-H ölçek ve veri kümesi bağımlılığı 500; IV-I protokol katmanı 1100. Hesaplama ayrıntıları ayrı dosyadadır (Y4).

| Satır | İşlem | Not |
|---|---|---|
| 1-11 | Yeniden yaz | Yorum başlığı ve bölüm girişi (meta cümle yok) |
| 16-47 | Kısalt (IV-A) | `tab:main_results` korunur, iki sütun eklenir (§5.2); 47'deki McNemar ve AA sırası iki cümleye iner |
| 49-66 | Sil, birleştir | `tab:conditional` düşer; koşullu yanıltma sütunu `tab:main_results`'a geçer; 66'daki çarpanlara ayırma tek cümle |
| 68-70 | Kısalt | Önceki çift beyanı tek cümle |
| 72-79 | Taşı | `fig:epsilon_sweep` Ek A'ya |
| 85-139 | Yeniden yaz, kısalt (IV-I) | `tab:transfer_protocols` düşer (§5.10); `fig:protocol_sets` korunur; 123, 129 ve 139'un çekirdeği bir paragrafa iner; 139'daki "second and partly opposing term" ifadesi korunur (kapı F1); 131 ve 134 silinir |
| 136 | Kısalt | Yönün dört protokolde ve MI-FGSM'de korunması tek cümle (FÖY 160, M8.4) |
| 144-176 | Kısalt (IV-I) | `tab:transfer_matrix` düşer; öncül p sonucu (0.989-1.000, 36 yön, artık en çok 0.41; FÖY 641, 1151-1156) iki cümle |
| 182-245 | Sil, yerine IV-B | ÇELİŞKİ: "Source Effect, Not Target Weakness" alt bölümü ve `tab:source_target` tümüyle çıkar. Eski toplamsal sonuç IV-B'de bir kez, Proposition 1'in sonucu olarak anılır: "an additive fit assigns +5.13 to the source and −2.03 to the target (FÖY 390); Proposition 1 shows that in a one-ViT design this split absorbs family similarity". Mahmood ayrışımı (199) kısaltılıp Tartışma'ya gider (Y4); Mahmood verisinde w tanımsızdır, ayrışım kurulamaz (PLAN §12) |
| 250-253 | Kısalt (IV-I) | `tab:protocol_settings` korunur |
| 258-284 | Taşı, kısalt | CIFAR-100 C1 kayıt öngörüleri Ek C'ye; `tab:cifar100_results` düşer (AA ve PGD ortalamaları föyde yok, §9); 284'teki marjlar (0.22, 0.48) Ek C'de kalır (kapı C1) |
| 289-318 | Kısalt (IV-I) | SVHN: işaretin protokolle dönmesi ve eşdeğerlik iki-üç cümle (FÖY 159-163, 185, 198, 229); 316'daki "fixed before measurement ±2 margin" yan cümlesi silinir |
| 323-343 | Taşı, kısalt | L2 Ek C'ye; `tab:l2_results` düşer; "we report the slope rather than a correlation" cümlesi Ek C'de aynen kalır (kapı I1) |
| 348-377 | Kısalt (IV-I) | `fig:spread_clean_gap` korunur; 353-355 bir paragraf; 372 ve 377 bir paragraf (57/60, +0.796; FÖY 1038-1039; pool +0.872, FÖY 1006) |
| 382-406 | Yeniden yaz (IV-B) | 401'in son yarısı ("keeps the clean ViT-Tiny by far the weakest source") ve 406'nın son iki cümlesi ("The source effect ... is therefore better read as a property of this ViT-Tiny") ÇELİŞKİ: silinir. Havuz modelleri σ ve ρ okumasıyla yeniden yazılır (FÖY 1745-1751) |
| 411-443 | Yeniden tasarla | `tab:external_pool` §5.9'daki biçime geçer |
| 448-465 | Taşı, kısalt | Seçim kuralı Ek B'ye; IV-I'da tek cümle ("the selection rule moves the four-protocol spread by about two points without changing the direction", FÖY 817); Ek B'de "deliberately not as a ratio to seed-level dispersion", "$25$ epochs", 0.32 ve 2.85 korunur (kapı C1, C2, D2) |
| 470-623 | Taşı, kısalt | Üç okuma Ek A'ya: `tab:gradient`, `tab:spatial`, `tab:feature_degradation`, `fig:feature_degradation` taşınır; `fig:gradient_analysis`, `fig:gradient_heatmap`, `fig:attention_layers` düşer; `tab:tgr` düşer (B5 onun yerini alır; eski TGR sonucu Ek A'da tek cümle, FÖY 139-150) |
| 628-636 | Sil | "Fifteen points against at most two and a half is the ordering the paper rests on" ÇELİŞKİ (eski manşet); varyans kaynakları Ek B'de tek paragraf, "four sources of variance" ifadesiyle (kapı B3b) |
| 638 | Taşı | Hesaplama ayrıntıları `04z_computational.tex`'e (Y4) |

IV-B'den IV-I'ya yeni paragrafların konusu ve kaynakları:

IV-B: C1 çiftinde log asimetrinin ayrışımı (`tab:pair_decomposition`; potansiyel payı 0.541, r 0.115 SD 0.010, FÖY 1703-1708; son kontrol noktası ve CIFAR-100 1709-1720; görüntü bootstrap SD'si 1722); ViT daha kırılgan hedeftir (w 55.53 ile 48.58, FÖY 28-29); kayıt öncesi masa çözümlemesi: dört CNN'lik panelde ViT'nin kaynak açığı 0.422 = 0.392 simetrik + 0.030 yönlü, simetrik oran 0.928 (FÖY 1726-1729), jackknife 0.919-0.935 (1739); havuz modellerinde σ ve ρ (`tab:external_pool`, 1745-1751). Bu paragrafın verisinin ön kayıttan önce görüldüğü cümle içinde söylenir.

IV-C: `tab:panel_tests`; K-a ayrıntısı (G_s 0.391/0.387/0.390, simetrik pay 0.368/0.360/0.367, yönlü pay 0.023/0.028/0.023; FÖY 1593; CIFAR-100 1848); K-c: ViT tohumları arası log τ̄ ortalaması −0.443, ResNet tohumları −0.489 (1595; CIFAR-100 −0.487 ile −0.501, 1850); CIFAR-100 temiz doğruluk karıştırıcısı (1876-1878, 1894); `fig:source_gap_split`, `fig:similarity_matrix`.

IV-D: `tab:cells`, `tab:fb4`, `fig:cells_interaction`; manipülasyon denetimleri geçti, AT çöküşü yok, kırpılma yok (1452-1457, 1472); S1 köprü σ −0.0003 [−0.035; +0.034], ρ −0.021 (1561-1562); S2 −0.130 (1563); S3 (1564-1566); S5 −0.181 [−0.500; 0.138] (1567); S6 XCiT panelinde işaretler aynı (1568); S7 Hodge potansiyel payı 0.919 (1569); S4 sıfırdan satırında potansiyel payı 0.504 ve 0.534, IN satırında oran kararsız (1575-1578); sonuç bölgesi O1, B6'dan sonra da O1 (1536); δ = 0.06'da da O1 (1545).

IV-E: `tab:attack_side`, `fig:attack_side`; seçilen saldırılar (1635-1646); TGR 0/5 kaynakta seçildi, S_TGR − S_PGD −0.218 ile −0.147 V-scr'de (1648); B6 (1666-1675).

IV-F: `tab:imagenet`; ön işleme denetimi 15/15 geçti, en büyük fark 1.20 puan (1802-1818); örneklem n = 2000, liste özeti eşleşti (1820); ayarlar (1827); çift A^σ, Ā^σ_IN ve Liu (1930-1939); dönüştürücülerin ρ'su (1943); Hodge 0.890 (1947); dondurulmuş betik çıktısı yalnız "betimsel" ibaresiyle ve karar sözcüğü olmadan, en çok bir cümle (1945).

IV-G: `tab:mantel`, `fig:gradient_alignment`; aile dışı keşifsel kısmi Mantel tek cümle "exploratory" (1996-2001); aile çiftine göre c ortalamaları (2009-2011; ImageNetV2'de dönüştürücü-dönüştürücü ortalamasının CNN-CNN'den yüksek olması, 0.318 ile 0.187, betimsel bir gözlem olarak yazılabilir).

IV-H: `fig:estimates_forest`; logit ve oran duyarlılıkları (1551-1552, 1603-1604, 1857-1858); ikincil panel (1606, 1860); panel jackknife (1554, 1605, 1859); δ = 0.06 (1549, 1601, 1846).

IV-I: protokol katmanı; `tab:protocol_settings`, `fig:protocol_sets`, `fig:spread_clean_gap`; Proposition 2'nin sınaması: en büyük |g| 0.0044, ham ile tc kaynak etkileri h ölçeğinde tc SD'sinin 0.016'sı, oran ölçeğinde 0.316'sı (1764-1773); öncül p (641, 864-871, 936-943); SVHN (159-163, 185, 198, 229); seçim kuralı tek cümle. 139'daki "second and partly opposing term" burada kalır (kapı F1).

Ek (`07_appendix.tex`, `\appendices` ile başlar): Ek A `app:behavior` (gradyan seyrekliği ve uzamsal yerellik, dikkat entropisi ve öznitelik kayması, ε süpürmesi, eski TGR sonucu; tanımlar 03'ten taşınır); Ek B `app:selection` (seçim kuralı, varyans kaynakları; içinde `\label{subsec:selection}` korunur); Ek C `app:registrations` (CIFAR-100 ve L2 kayıtlı öngörüleri; "not testable in this design" ve marjlar; eski 280-284 ve 326-343'ün özü).

### 4.6 `sections/05_discussion.tex` (Y4; hedef 1500 kelime) ve yeni `sections/04z_computational.tex` (Y4; hedef 250 kelime)

| Satır | İşlem | Not |
|---|---|---|
| 1-7 | Yeniden yaz | Yorum başlığı |
| 14-18 | Yeniden yaz | ÇELİŞKİ: "The central result is an ordering of dispersions" eski manşettir. Yeni V-A üç katmanlıdır: bulunan (açık simetriktir, sıfırdan eğitimde mimariye aittir, IN başlatması ViT'de daha çok kapatır; yönlü terim yalnız CIFAR-10 log ölçek CNN panelinde küçüktür), önemi (zayıf kaynak okuması benzerlik okumasıdır; vekil seçimi ve transfer temelli değerlendirme için sonuç; Demontis ve Zhang ile bağ), bilinmeyen (ölçek, sıfırdan satırının ImageNet karşılığı, mekanizma) |
| 20 | Kısalt | Protokollerin farklı nicelikleri tahmin ettiği itirazı V-C içinde iki cümle |
| 27 | Yeniden yaz (V-B) | Mahmood: kendi verilerinde köşegen beyaz kutu olmadığından w tanımsızdır ve ayrışım kurulamaz; yeniden puanlama sonucu (−0.59, FÖY 650 civarı "Anahtar cift") tek cümle; "in our adversarially trained matrices it is the source side that decides the direction" ÇELİŞKİ, silinir; tez uzlaşması: iki modelde ayrışmaz, çaprazlanmış panelde ayrışır (Proposition 1) |
| 29 | Kısalt | Protokollerin kullanımı V-C'ye |
| 31 | Sil | ÇELİŞKİ: "The decomposition places that direction on the source side" |
| 33 | Sil | Koşullu ayrışım beyanı Ek'e ya da tek yan cümle |
| 35 | Kısalt | Üç okuma tek cümle ve `app:behavior` göndermesi |
| 44-54 | Yeniden yaz | `enumerate` kalkar, düz paragraf (madde yasağı). Gereklilikler: koşullama kümesini yazmak; ham oranı mimari karşılaştırması diye sunmamak; asimetriyi sabit bir panel üzerinden w, τ̄ ve r'ye ayırmak ve ölçeği belirtmek (5. madde "fixed third model ile kaynak ve hedef etkisini ayırın" ÇELİŞKİ, bununla değişir); temiz doğrulukları ve seçim kuralını yazmak; başlatmayı mimariden ayırmak |
| 56 | Koru | Uygulayıcılar için cümle; 62.76 FÖY 20 |
| 64 | Yeniden yaz | §8.1 sınırlılık listesi; "The mechanism account is incomplete ... three of the four protocols" ve "weaker question" ifadeleri korunur (kapı F2, C4); "covers three datasets" ifadesi doğru biçimde geçer (kapı G1; §10.4) |
| 72 | Yeniden yaz | Gelecek: ViT-Small ile ResNet-50 düzeyinde 2x2; ImageNet'te sıfırdan aynı tarifli çiftler; normalizasyonu başlatmadan ayıran hücre; gradyan hizalanmasının PGD yolu boyunca ölçümü |

### 4.7 `sections/06_conclusion.tex` (Y1; hedef 300 kelime)

61-67 tümüyle yeniden yazılır; 65 ÇELİŞKİ ("Its direction comes from the examples crafted on this particular ViT-Tiny"). Yeni sonuç yeni sayı getirmez, özetin sayılarını yinelemez; manşet, sınır ve tek cümlelik çağrı. 67'deki kapsam cümlesi "covers three datasets" ifadesini taşıyabilir (kapı G1; §10.4).

### 4.8 Katkılar dörde iner

PLAN §9 gereği katkılar: (1) tanımlanabilirlik (Proposition 1; iki modelli ve tek ViT'li tasarımda toplamsal bölüşüm benzerlikle karışır); (2) w-τ̄-r ayrışımı ve ölçülen büyüklükler; (3) 2x2 müdahale (H1-H3, saldırı tarafı, maskeleme); (4) protokol katmanı ve h ölçeği ayarı (Proposition 2). Eski katkılar 1, 2 ve 4 dördüncüye birleşir, eski katkı 3 (kaynak etkisi) kalkar.

## 5. Tablolar

Bütün tablolar booktabs, dikey çizgi yok, `[t]` ya da `[!t]` yerleşim, `[H]` yok; `table*` iki sütun genişliğindedir. Her hücrenin föy satırı aşağıdadır; yazar tabloya bir `% FOY:` yorum satırı bloğu ekler.

### 5.1 `tab:design` (yeni; 03, Y2; tek sütun)

Satırlar R32, V-scr, V-IN, R224-scr, R224-IN; sütunlar Architecture, Initialization, Input pipeline, Clean phase, Runs (seeds).

| Hücre | Kaynak |
|---|---|
| Mimari, başlatma, girdi hattı, temiz aşama | ÖK §3 tablosu (satır 29-34); FÖY 1443 (hücre tanımları) |
| Tohumlar | ÖK §3; FÖY 1452-1457 (yeni koşular), 1505-1507 (V-scr), 1593 (R32 tohumları 1001-1003) |
| Ortak AT tarifi (dipnot) | ÖK §3 satır 36: karışık kayıp, PGD-10, ε 8/255, α 2/255, AdamW 0.05, lr 1e-3, batch 64, sabır 20, tavan 80, T_max 100 |

Tasarım sabitleri sonuç değildir; kaynakları ÖK §3'tür ve `% KAYNAK: ON_KAYIT §3` yorumuyla verilir. Karar: bu tablo hücre adlarını tek yerde tanımlar, böylece IV'teki tablolar yalnız adla anar.

### 5.2 `tab:main_results` (korunur, değişir; IV-A)

Mevcut sütunlara "Cond.\ fooling PGD-10 ($w$)" ve "Cond.\ fooling AA" sütunları eklenir: ResNet-18 AT 48.58±0.80 ve 55.78±0.23, ViT-Tiny AT 55.53±0.50 ve 60.37±0.33 (FÖY 28-29). Mevcut hücreler FÖY 14-17 ve 20'dir. Standart eğitimli satırlarda bu sütunlar "--". `tab:conditional`'ın kalan iki sütunu (both-correct robust) metinde tek cümleye iner (FÖY 28-29).

### 5.3 `tab:pair_decomposition` (yeni; `tab:source_target`'ın yerine; IV-B, tek sütun ya da `table*`)

Üst blok satırları: CIFAR-10 selected, CIFAR-10 last checkpoint, CIFAR-100 selected. Sütunlar: target-correct asymmetry (pts), log ratio, potential component log(w_V/w_R), directional r_RV, log τ̄_RV, potential share. Hücre biçimi "ort (koşum SD)".

| Satır | FÖY |
|---|---|
| CIFAR-10 selected | 1703-1708 |
| CIFAR-10 last checkpoint | 1709-1714 |
| CIFAR-100 selected | 1715-1720 |
| Dipnot: görüntü bootstrap SD (r 0.030, log τ̄ 0.016) | 1722 |

Alt blok, 2x2'nin tohum indeksiyle eşleşmiş çiftleri (S4, betimsel; tek tek değerler): R224-scr s1201 / V-scr s2001 ve s1202 / s2002 satırları (FÖY 1575-1576); R224-IN / V-IN satırları (1577-1578) potansiyel payı sütununda "--" ve dipnot: "log ratio near zero; share undefined" (R09 §4 son paragrafı). Karar: eski toplamsal fit sayıları bu tabloya girmez, yalnız metinde bir kez (FÖY 390), çünkü Proposition 1 o bölüşümün tanımlanamadığını söyler.

### 5.4 `tab:panel_tests` (yeni; B2 ve B9 yan yana; IV-C, `table*`)

Satırlar K-a, K-b, K-c; iki sütun grubu CIFAR-10 ve CIFAR-100; her grupta Estimate (per-seed), 90% CI, 95% CI, Holm p, Decision. Alt blokta duyarlılık satırları; sütunlar yine iki veri kümesi.

| Hücre | CIFAR-10 FÖY | CIFAR-100 FÖY |
|---|---|---|
| K-a ort q, q_s, %90, %95, ham p, Holm p, karar | 1587 | 1838 |
| K-b ort ρ(V-scr), tohumlar, %90, %95, TOST p, Holm p, karar | 1588 | 1839, 1844 (TOST tek yönlü p'ler) |
| K-c Δ_seed, bootstrap %90, %95, p, Holm p, karar | 1589 | 1840 |
| Öngörülen büyüklük satırı | 1587-1589 son sütun | 1842 |
| δ = 0.06 kararları | 1601 | 1846 |
| Tam örneklem | 1602 | 1856 |
| Logit q ve ρ(V-scr) | 1603 | 1857 |
| Oran ölçeği | 1604 | 1858 |
| Panel jackknife aralığı | 1605 | 1859 |
| İkincil panel | 1606 (XCiT) | 1860 (XCiT ve Hendrycks) |

Dipnot: CIFAR-10'da K-a ve K-b hiyerarşik bootstrap duyarlılığı üretilmemiştir (FÖY 1607); CIFAR-100'de ViT-Tiny temiz doğruluğu 41.94-44.06, panel 53.82-72.57 (FÖY 1876-1885). Karar: K-c'nin tür içi değerleri (−0.443 ve −0.489; FÖY 1595) tabloda değil metinde ve `fig:similarity_matrix`'te verilir, çünkü tablo zaten iki veri kümesiyle geniştir; PLAN §9'daki ayrı "tür içi benzerlik" tablosu bu tabloya katılmıştır.

### 5.5 `tab:cells` (yeni; 2x2 hücre tablosu, B6 dahil; IV-D, `table*`)

Satırlar hücreye göre gruplanmış dokuz koşu; her grubun sonunda bir hücre ortalaması satırı (italik değil, `\midrule` ile ayrılmış). Sütunlar: Cell, Seed, Clean (%), $w$ (%), $\omega$, $\sigma$, $\rho$, PGD-10 (first 1k, %), AA (first 1k, %), PGD$-$AA (pts).

| Hücre | FÖY |
|---|---|
| Koşu satırları: Clean, w, ω, σ, ρ | 1505-1513 |
| Hücre ortalaması: n, Temiz ort, w ort, ω ort, σ ort, ρ ort | 1496-1499 |
| PGD-10 ilk 1000, AA ilk 1000, fark (altı yeni model) | 1666-1671 (ya da 1463-1468) |
| V-scr satırlarının AA sütunu | "--" ve dipnot: B6 kapsamı dışında; tam test AA'sı `tab:main_results`'ta 29.14±0.40 (FÖY 17, 1517) |
| Dipnot: maskeleme eşiği 10 puan, işaretli model yok, en büyük fark 7.40 | 1673 |

Karar: R32 köprü hücresi bu tabloda satır olarak yer almaz, çünkü üç tohumun σ ve ρ ortalaması föyde yoktur (yalnız s1001, FÖY 1745); köprü S1 farkıyla metinde verilir (1561-1562). Karar: B6 ayrı tablo olmaz, bu tablonun son üç sütunudur, çünkü B6 yalnız altı modelde üç sayı taşır ve aynı koşu satırlarına aittir.

### 5.6 `tab:fb4` (yeni; F_B4 tablosu; IV-D, tek sütun, 4 sütun)

Yön: satırlar çözümlemeler, sütunlar H1, H2, H3.

| Satır | FÖY |
|---|---|
| Contrast (tanım, kısaltılmış) | ÖK §5 B4 |
| Estimate (split-half, log) | 1526-1528 |
| 90% CI; 95% CI | 1526-1528 |
| $t$ (df 5) | 1526-1528 |
| Raw $p$ (H1 tek yönlü, H2 iki yönlü, H3 TOST) | 1526-1528, 1530 |
| Holm $p$ | 1526-1528 |
| Decision | 1526-1528 |
| Predicted size met | 1526-1527 son sütun |
| Logit estimate [90%] | 1551 |
| Ratio scale, pts [90%] | 1552 |
| Welch 95% (df) | 1553 |
| Panel jackknife range | 1554 |
| Hierarchical bootstrap 90% | 1555 |
| $\delta = 0.06$ Holm $p$, decision | 1549 |
| Dipnot: pooled SD 0.0273 ve 0.0169; logit H2 +0.354 karar koşulu; sonuç bölgesi O1 | 1532, 1534, 1536 |

### 5.7 `tab:attack_side` (yeni; B5; IV-E, tek sütun)

| Satır | FÖY |
|---|---|
| $\Gk{PGD}$ ve bootstrap %90 | 1620-1621 |
| $\Gk{best}$ | 1622 |
| Retained fraction, %90, %95 | 1624-1626 |
| Valid bootstrap copies | 1627 |
| Decision | 1628 |
| Full-sample selection ratio | 1629 |
| Descriptive pair R224-scr / V-scr: G_PGD, G_best, ratio | 1654 |
| Descriptive pair R224-IN / V-IN: G_PGD; ratio "not computed (G_PGD ≤ 0.10)" | 1655 |
| Dipnot: TGR 0/5 ViT kaynağında seçildi | 1648 |

Kaynak başına S değerleri (1635-1646) tabloya değil `fig:attack_side`'a gider. IN çiftinin JSON'daki oranı (0.937) hiçbir yerde yazılmaz (FÖY 1655).

### 5.8 `tab:imagenet` (yeni; B8 betimsel; IV-F, `table*`)

Üst blok 14 model (satır sırası: üç çift, Mo, altı P8 üyesi, XCiT). Sütunlar: Model (RobustBench id, `\texttt`), Role, Family, Clean (common pipeline, %), PGD-10 robust (%), $w$ (%), $\sigma$, $\rho$, RB clean, RB AA.

| Hücre | FÖY |
|---|---|
| 14 model satırı | 1909-1922 |
| Ön işleme denetimi (dipnot: 15/15 geçti; en büyük fark 1.20) | 1802-1818 |

Alt blok çift düzeyi: Pair, CNN, Transformer, Row (IN/scr), $A^\sigma$, 90% CI, 95% CI, $A^\sigma$ logit, $A^\rho$, $A^\omega$.

| Hücre | FÖY |
|---|---|
| Çift 1-3 | 1930-1932 |
| $\bar{A}^{\sigma}_{\mathrm{IN}}$ (çift 1-2), %90, %95, etiket "consistent with expectation" | 1938 |
| $\Asig{scr}$ Liu (çift 3), %90, %95, etiket "uncertain" | 1939 |
| Dipnot: görüntü bootstrap B = 2000, yalnız görüntü belirsizliği; df 1 ile çiftler arası aralık yok | 1941 |

Başlıkta "descriptive, exploratory; no decision family" yazılır.

### 5.9 `tab:external_pool` (korunur, yeniden tasarlanır; IV-B)

Karar: tablo hedef türüne göre p blokları yerine model satırlarına geçer, çünkü σ ve ρ model düzeyindedir ve p sütunu da model başına verilebilir. Satırlar sekiz havuz modeli. Sütunlar: Clean (%), $p$ min as target, $\sigma$ (4-CNN panel), $\rho$ (4-CNN panel), $\sigma$ (7-member panel), $\rho$ (7-member panel).

| Hücre | FÖY |
|---|---|
| Clean, p min | 936-943 |
| σ, ρ (masa, bölünmüş yarı, log) ve panel_n | 1745-1751 |
| σ, ρ (B4 panel) | 1745-1751 sağ sütunlar |
| Standard_WRN28_10 satırında σ, ρ | "--" (masa tablosu 7 model kapsar, 1753) |
| Alt blok: pool spread slopes (three protocols +0.872 [+0.534, +1.274], r 0.944; four protocols +0.559 [−0.205, +4.582]) | 1005-1006 |
| Dipnot: p tüm 56 yönde 0.9330-1.0000, artık en çok 0.35 | 945 |

Eski orta blok (standart eğitimli çiftler) tablodan çıkar; metinde en çok bir cümle (FÖY 891-897 bölgesi).

### 5.10 Düşen tablolar

| Tablo | Gerekçe |
|---|---|
| `tab:conditional` | Koşullu yanıltma w'dir; sütunları `tab:main_results`'a katılır |
| `tab:transfer_protocols` | Fark sütunu `tab:protocol_settings`'in CIFAR-10 sütunuyla aynıdır; yön başına oranlar ve N `fig:protocol_sets`'te |
| `tab:transfer_matrix` | 3x3 WRN matrisi 20x20 B4 matrisi ve `fig:similarity_matrix` ile aşılmıştır; öncül p sonucu metinde |
| `tab:source_target` | Toplamsal bölüşüm Proposition 1 gereği tanımlanamaz; yerine `tab:pair_decomposition` |
| `tab:cifar100_results` | CIFAR-100 C1 PGD ve AA ortalamaları föyde yok; CIFAR-100 model değerleri B9 bağlamında FÖY 1873-1878'den metinde |
| `tab:l2_results` | L2 mutlak gürbüzlüğü manşetle ilgisiz; L2 sütunu `tab:protocol_settings`'te kalır |
| `tab:tgr` | B5 TGR'yi panelde, seçimli ve aralıklı sınar; eski sonuç Ek A'da tek cümle |

Taşınan (Ek'e): `tab:gradient`, `tab:spatial`, `tab:feature_degradation`. Korunan: `tab:protocol_masks`, `tab:protocol_settings`, `tab:main_results` (değişik), `tab:external_pool` (yeniden tasarlanmış).

### 5.11 `tab:registry` (yeni; 03, Y2; `table*`)

Ön kayıtlı sınamaların tek tablosu; sonuç değil tasarım taşır. Sütunlar: Family, Label, Quantity, Prediction, Test, Decision rule (kısa). Satırlar: K-a, K-b, K-c (panel, CIFAR-10); H1, H2, H3 (2x2); B5 retained fraction (tek sınama); B6 masking rule (karar kuralı); K-a, K-b, K-c (CIFAR-100); $\bar{A}^\sigma_{\mathrm{IN}}$ ve Liu satırı (ImageNetV2, betimsel, aile yok); H10 ve H10k (üç veri kümesi, gradient family). Kaynak ÖK §5 (satır 58-94), EK §4.2, §5.6, §6.3 ve §7 tablosu. Dipnot: blok kimlikleri B2, B4, B5, B6, B9, B8, B10 ve donma tarihleri. Karar: bu tablo yöntem metnindeki uzun karar kuralı paragraflarının yerini alır; metin yalnız karar ilkesini ve sonuç haritasını anlatır.

Tablo sayısı: düşen 7, yeni 9 (`tab:design`, `tab:registry`, `tab:pair_decomposition`, `tab:panel_tests`, `tab:cells`, `tab:fb4`, `tab:attack_side`, `tab:imagenet`, `tab:mantel`), korunan 4 (ikisi değişik), Ek'e taşınan 3. Toplam 16 (gövde 13, Ek 3); eskiden 14.

### 5.12 `tab:mantel` (yeni; B10; IV-G, tek sütun)

Üst blok: satırlar üç veri kümesi × (raw, main-effect residual); sütunlar K, pairs, $\rS$, one-sided $p$, Holm $p$, predicted size met, decision.

| Hücre | FÖY |
|---|---|
| K, çift, r, tek yönlü p, permütasyon | 1970-1975 |
| Holm p, büyüklük, karar | 1983-1988 |
| Dipnot: p = 1e-04 permütasyon tabanı, 6/6 tabanda | 1977 |
| Dipnot: karar kuralı | 1990 |

Alt blok: c_ij ortalamaları (all; CNN-CNN; transformer-transformer; mixed, parantez içinde çift sayısı), FÖY 2009-2011. Aile dışı kısmi Mantel satırları (1996-2001) tabloya girmez, metinde "exploratory" ile tek cümle.

## 6. Şekiller

Bu turda yeni veri şekilleri şekil ajanınca matplotlib ile taslak olarak `paper/figures/konsey/` altına üretilir (klasör yoktur, ajan açar); kalıcı çizim daha sonra visio-cizici skill'iyle yapılacaktır (`results/q1_research/BEKLEYEN_SEKIL_GOREVI_2026-10-29.md`). Betik adları `paper/figures/konsey/fig_<ad>.py`; çıktı `fig_<ad>.pdf`, `fig_<ad>.png` ve `fig_<ad>.kanit.json` (girdi dosyalarının SHA-256'sı, okunan anahtarlar, çizilen değerler, föy ile karşılaştırma). Biçim kuralları `paper/figures/fig_yayilim_temiz_fark.py`'deki gibidir: tek sütun 3.5 in, çift sütun 7.16 in, Okabe-Ito renkleri, ikinci kanal olarak işaret biçimi, karantina denetimi (girdi yalnız `results/q1/` ve `results/c1_*`). Koşturma kapsayıcıda: `docker exec -w /workspace adeb_eval python paper/figures/konsey/fig_<ad>.py`. Şekil içindeki ek açıklama sayıları föy değerleriyle aynı olmalıdır; kanıt dosyası bunu denetler. Altyazılar İngilizcedir, iki ila dört cümledir, kalın giriş cümlesi taşımaz.

### 6.1 `fig:study_overview` (yenilenir; 03, `figure*`)

Kaynak `paper/figures/overview/fig_study_overview.tex` (TikZ) kopyalanıp `paper/figures/konsey/fig_study_overview.tex` olarak değiştirilir; özgün dosyaya dokunulmaz. Paneller: (a) modeller: R32 ve V-scr çifti (üç tohum), 2x2 hücreleri (tohumlar); (b) paneller: CIFAR-10 P (7) ve XCiT, CIFAR-100 P9 (7 + 2), ImageNetV2 P8 (6) ve çiftler; (c) ölçüm: transfer matrisi (CIFAR-10 20 model, FÖY 1569; CIFAR-100 15, 1826; ImageNetV2 14, 1827) → w, τ̄, r → σ, ρ, ω; (d) ön kayıtlı aileler ve protokol katmanı şeridi. Sayı yalnız model sayıları.

Altyazı taslağı: "Study overview. A ResNet-18 and ViT-Tiny pair and a two-by-two design that crosses architecture with initialization at a matched input pipeline are evaluated against fixed panels of robust CNNs on CIFAR-10 and CIFAR-100, and the same decomposition is applied descriptively to independently trained ImageNet models evaluated on ImageNetV2. Every transfer rate is factored into the target's white-box vulnerability $w$, a symmetric similarity $\bar\tau$ and a directional residual $r$, which are averaged over the panel. The registered test families and the conditioning-protocol layer are listed at the bottom."

### 6.2 `fig:decomposition_schematic` (yeni; 03, tek sütun; veri yok)

Betik `fig_decomposition_schematic.py` (matplotlib çizim). Sol: iki modelli T matrisi, köşegende w; orta: $\log T_{ij} = \log w_j + \log\bar\tau_{ij} + \tfrac12 r_{ij}$ okları; sağ: panel ortalaması ile σ_m, ρ_m ve kaynak açığının simetrik (σ_R − σ_V) ve yönlü (−½(ρ_R − ρ_V)) parçaları. Altyazı: "Decomposition used throughout. The log target-correct transfer rate splits exactly into the target's white-box vulnerability, a pairwise symmetric similarity and half a directional residual; averaging the last two over a fixed CNN panel gives model-level similarity $\sigma$ and direction $\rho$. A model's source gap to a reference model is then the sum of a symmetric part and a directional part."

### 6.3 `fig:cells_interaction` (yeni; IV-D, tek sütun, üç panel üst üste)

Veri: `results/q1/konsey_ayrisim_b4.json` `b4.model_tablosu.<m>.yari_log.{sigma, rho, omega}`; hücre ataması `raporlar/konsey_2026-10-29/hucre_tablosu.json` `modeller.<m>.hucre`; R32 köprü noktaları aynı JSON'daki `ResNet18_AT_s100{1,2,3}`. Paneller: (a) σ, x ekseni başlatma (scratch, ImageNet), ViT ve ResNet-224 için hücre ortalamalarını birleştiren iki çizgi, koşu noktaları hafif kaydırılmış, R32 noktaları scratch konumunda ayrı işaretle; ek açıklama $\Asig{scr} = -0.364$ ve $\Isig = +0.260$ (FÖY 1526-1527). (b) ρ, aynı düzen, 0 çevresinde ±0.10 bandı; (c) ω.

Altyazı: "Cell means (lines) and individual runs (markers) of the two-by-two design on CIFAR-10, split-half estimates on the log scale. (a) Panel similarity $\sigma$: trained from scratch the ViT is less similar to the CNN panel than the ResNet, and ImageNet initialization narrows the gap for the ViT more than for the ResNet. (b) Directional term $\rho$ with the $\pm0.10$ equivalence band; (c) vulnerability $\omega=\log w$. Open markers are the three 32-pixel ResNet-18 runs used as a bridge."

### 6.4 `fig:source_gap_split` (yeni; IV-C, tek sütun ya da `figure*`)

Veri: J2 `results/q1/konsey_ayrisim_b2.json` `b2.F_B2.K-a.{D, simetrik_pay, yonlu_pay, q}`; J9 `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` aynı anahtarlar; J8 `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` aynı anahtarlar (B8 betimsel, payda kuralı çift 3'te tetiklenir). Paneller: (a) CIFAR-10 üç tohum çifti, (b) CIFAR-100 üç tohum çifti, (c) ImageNetV2 üç CNN-dönüştürücü çifti (taralı, "descriptive"); yığılı çubuk: simetrik pay ve yönlü pay, üstte q. Föy karşılıkları 1593, 1848, 1930-1932.

Altyazı: "Source gap of the transformer relative to its CNN counterpart, split into a symmetric part ($\sigma$ difference) and a directional part, per seed pair on CIFAR-10 (a) and CIFAR-100 (b) and per same-recipe pair on ImageNetV2 (c). On both CIFAR datasets the symmetric part carries most of the gap in every seed; the directional part grows on CIFAR-100. The ImageNetV2 panel is descriptive, and its third pair has a gap below the registered 0.10 threshold."

### 6.5 `fig:similarity_matrix` (yeni; IV-C, `figure*`, üç ısı haritası)

Veri: `results/q1/konsey_b10_gradyan/mantel_{cifar10,cifar100,imagenetv2}.json` `log_tau_matrisi`, `modeller_ortak`; aile ve hücre `hucre_tablosu.json`, `hucre_tablosu_b9.json`, `hucre_tablosu_b8.json` `modeller.<m>.{aile, hucre}`. Sıralama: ViT-scr, ViT-IN, R224-scr, R224-IN, R32, panel CNN'leri, XCiT; aile blokları çerçeveli; ıraksak renk ölçeği ortak. Kanıt dosyası bu matrislerin bölünmüş yarı log τ̄ olduğunu (EK §6.1) ve K-c tür içi ortalamalarının föyle (1595, 1850) aynı çıktığını denetler.

Altyazı: "Pairwise symmetric similarity $\log\bar\tau_{ij}$ (split-half, log scale) for all models on CIFAR-10 (a), CIFAR-100 (b) and ImageNetV2 (c), ordered by family. Seeds of the scratch-trained ViT-Tiny form a block of high mutual similarity that is dissimilar to the CNN panel. Diagonal cells are undefined and left blank."

### 6.6 `fig:gradient_alignment` (yeni; IV-G, `figure*`, 2×3)

Veri: aynı `mantel_<veri>.json` dosyalarındaki `c_matrisi`, `log_tau_matrisi`, `modeller_ortak`; çift türü hücre tablolarının `aile` alanından. Üst sıra: ham c_ij ile log τ̄_ij saçılımı, renk çift türü (CNN-CNN, transformer-transformer, mixed). Alt sıra: toplamsal model ana etkileri çıkarılmış artıklar (EK §6.2 tanımı); betik artık Spearman'ı yeniden hesaplar ve kanıt dosyasında föy değerleriyle (FÖY 1970-1975) 1e-3 içinde eşleştiğini yazar; eşleşmezse alt sıra çizilmez ve durum bildirilir. Panel köşesinde $\rS$ ham ve artık (föyden).

Altyazı: "Input-gradient cosine on clean images against pairwise symmetric similarity, for every model pair on CIFAR-10, CIFAR-100 and ImageNetV2 (top), and the same relation after additive model main effects are removed from both matrices (bottom). The rank correlation is positive in all six panels, and permutation $p$ is at its floor in every case (Table~\ref{tab:mantel}). Alignment at a single clean point is a necessary condition for similar transfer, not evidence of a mechanism."

### 6.7 `fig:attack_side` (yeni; IV-E, tek sütun)

Veri: `results/q1/konsey_ayrisim_b5.json` `b5.birincil_C1-R32_V-scr.kaynaklar.<m>.S_tam` (pgd, mi, tgr) ve `b5.betimsel.<cift>.kaynaklar`; hücre ataması `hucre_tablosu.json`. Düzen: y ekseni on iki kaynak hücreye göre gruplu (R32, V-scr, R224-scr, R224-IN, V-IN), x ekseni $L_k(m)$; PGD-10 daire, MI-PGD kare, TGR üçgen (yalnız ViT); seçilen saldırı dolu işaret. Föy karşılığı 1635-1646.

Altyazı: "Panel-mean log transfer from each source under PGD-10, momentum PGD and, for ViT sources, token gradient regularization (TGR); filled markers are the attacks chosen by cross-fitted selection. TGR transfers worse than PGD-10 from every ViT source and is never selected, and the gap between ResNet and ViT sources is retained under each source's best attack (Table~\ref{tab:attack_side})."

### 6.8 `fig:estimates_forest` (yeni; IV-H, tek sütun, iki panel)

Veri: J4 `results/q1/konsey_ayrisim_b4.json` `b4.F_B4.karsitliklar.H{1,2,3}.{kestirim, ci90, ci95}` ve `b4.duyarlilik.yari_logit.H*`; J2 ve J9 `b2.F_B2.K-b.{ort, ci90, ci95}`, `b2.duyarlilik.yari_logit.rho_V.{ort, ci90, ci95}`; `results/q1/konsey_b8_imagenetv2/b8_betimsel.json` `ciftler[k].{A_sigma, goruntu_bootstrap_ci90, goruntu_bootstrap_ci95}`, `A_sigma_IN`, `A_sigma_scr_Liu`. (a) σ ölçekli kestirimler: H1 (log, logit), H2 (log, logit), ImageNetV2 çift 1, çift 2, Ā^σ_IN, Liu; dikey çizgiler 0, ±0.10, −0.20; ImageNetV2 satırları açık işaretli (betimsel). (b) Yönlü terimler: K-b CIFAR-10 (log, logit), K-b CIFAR-100 (log, logit), H3 (log, logit), ±0.10 bandı. Föy karşılıkları 1526-1528, 1551, 1588, 1603, 1839, 1857, 1930-1939. Karar: oran ölçeği (puan) bu şekle girmez, çünkü birimi farklıdır.

Altyazı: "Registered estimates with 90\% (thick) and 95\% (thin) intervals on the log scale and their logit-scale counterparts. (a) Architecture and interaction effects on panel similarity, with the descriptive ImageNetV2 pair estimates (open markers) for comparison. (b) Directional terms: equivalence within $\pm0.10$ holds on CIFAR-10 on the log scale but not on CIFAR-100, and on the logit scale the directional estimates change sign."

### 6.9 Korunan, taşınan ve düşen şekiller

| Şekil | Durum |
|---|---|
| `fig:protocol_sets` | Korunur (IV-I), altyazı kısaltılır; `../figures/final/fig_protocol_sets.pdf` |
| `fig:spread_clean_gap` | Korunur (IV-I) |
| `fig:epsilon_sweep` | Ek A'ya taşınır |
| `fig:feature_degradation` | Ek A'ya taşınır (entropi TOST'u) |
| `fig:gradient_analysis` | Düşer (norm dağılımı manşetle ilgisiz) |
| `fig:gradient_heatmap` | Düşer (tek görüntü örnekleri) |
| `fig:attention_layers` | Düşer (tek görüntü örneği; yer değiştirme `fig:feature_degradation`(b)'de) |

Şekil sayısı: düşen 3, yenilenen 1, eklenen 7 (6 veri, 1 şematik), Ek'e taşınan 2. Toplam 12 (gövde 10, Ek 2); eskiden 8. Şekil PDF'i derleme anında yoksa yazar ortamı yazar ve `\includegraphics` yerine `\fbox{\parbox{0.9\columnwidth}{Figure pending: fig\_<ad>}}` koyar, üstüne `% BEKLIYOR: fig_<ad>` yorumu ekler.

## 7. Atıf eklemeleri

Kimlikler atif-kontrol skill'iyle sonradan doğrulanacaktır. "Doğrulandı" sütunu konsey raporlarındaki doğrulama kaydını gösterir; "aday" yazan kimlik hafızadan gelir, yalnız arama ipucudur ve atif-kontrol doğrulamadan `.bib`'e VERIFIED gibi girmez (girerse `note = {TODO: atif-kontrol}` alanı taşır). `.bib`'e ekleme yalnız Y2'nin işidir; öteki yazarlar yalnız bu tablodaki anahtarları kullanır.

| Anahtar | Kaynak | Kimlik | Durum | Nereye |
|---|---|---|---|---|
| `demontis2019adversarial` | Demontis ve ark., USENIX Security 2019 | arXiv 1809.02861 | .bib'de var | II-B; III-D (ayrışımın yakın öncülü); V-A |
| `adam2019reducing` | Adam, Smirnov, Haibe-Kains, Goldenberg, 2019 ön baskı | arXiv 1904.07980 | doğrulandı (02_literatur satır 58); başlık atif-kontrol'den | II-B (gradyan normu farkı ve asimetri) |
| `caussinus1965contribution` | Caussinus, Ann. Fac. Sci. Toulouse 1965 | DOI 10.5802/afst.519 | künye doğrulandı, içerik doğrulanmadı | II-C; III-D (T_ij = w_j τ_ij yarı-simetri biçimi) |
| `jiang2011statistical` | Jiang, Lim, Yao, Ye, Math. Program. (HodgeRank) | arXiv 0811.1067; DOI 10.1007/s10107-010-0419-x | doğrulandı | II-C; III-D (Proposition 1(a)); IV-D (S7) |
| `balduzzi2018reevaluating` | Balduzzi, Tuyls, Pérolat, Graepel, NeurIPS 2018 | arXiv 1806.02643 | doğrulandı | II-C |
| `mahmood2021robustness` | Mahmood ve ark., ICCV 2021 | mevcut | .bib'de var | I, II-B, V-B |
| `shao2022adversarial` | Shao ve ark., TMLR 2022 | arXiv 2103.15670 | .bib'de var | I, II-A |
| `mo2022adversarial` | Mo ve ark., NeurIPS 2022 | arXiv 2210.07540 | .bib'de var | II-A; III-E (Mo ViT-B) |
| `naseer2022improving` | Naseer ve ark., ICLR 2022 | arXiv 2106.04169 | .bib'de var | II-B; IV-E |
| `awad2025defense` | Awad, Mohamed, Gomaa | arXiv 2512.02830 | doğrulandı (06_ek_deney_literatur satır 28) | II-B (gürbüz vekiller daha iyi aktarır); V-B |
| `bai2021transformers` | Bai ve ark., NeurIPS 2021 | arXiv 2111.05464 | .bib'de var | I, II-A |
| `zhang2024why` | Zhang ve ark., IEEE S&P 2024 | arXiv 2307.07873; DOI 10.1109/SP54263.2024.00010 | doğrulandı | II-B; III-F (c_ij'nin öncülü, Tanım 2); IV-G |
| `liu2023comprehensive` | Liu ve ark., ARES-Bench | arXiv 2302.14301 | doğrulandı | II-B (ImageNet'te gürbüz modeller arası transfer); III-E (Liu çifti) |
| `sitawarin2024pubdef` | Sitawarin ve ark., ICLR 2024 | arXiv 2310.17645 | doğrulandı | II-B |
| `smouse1986multiple` | Smouse, Long, Sokal, Systematic Zoology 35(4):627-632 | DOI 10.2307/2413122 | Crossref ile doğrulandı | II-C; III-F (kısmi Mantel) |
| `touvron2021training` | Touvron ve ark., DeiT, ICML 2021 | arXiv 2012.12877 | görev metninde; doğrulanmadı | III-A (V-IN başlatması) |
| `wightman2021resnet` | Wightman, Touvron, Jégou, "ResNet strikes back" | arXiv 2110.00476 | görev metninde; doğrulanmadı | III-A (R224-IN başlatması, a1 tarifi) |
| `bhojanapalli2021understanding` | Bhojanapalli ve ark., ICCV 2021 | arXiv 2103.14586 | .bib'de var | II-A |
| `recht2019imagenet` | Recht ve ark., "Do ImageNet Classifiers Generalize to ImageNet?", ICML 2019 | arXiv 1902.10811 | doğrulandı (06_ek_deney_literatur §4.3) | III-E (ImageNetV2 MatchedFrequency); IV-F; Data Availability |
| `singh2023revisiting` | Singh, Croce, Hein, NeurIPS 2023 | arXiv 2303.01870 | doğrulandı (02_literatur satır 43) | II-A; III-E (iki aynı tarifli çift, temiz modelden başlatma) |
| `croce2021robustbench` | RobustBench | mevcut | .bib'de var | III-E (panellerin kaynağı) |
| `zhang2023tgr`, `dong2018boosting` | TGR, MI-FGSM | mevcut | .bib'de var | III-A (B5 saldırıları) |
| `wong2020fast`, `engstrom2019robustness`, `carmon2019unlabeled`, `gowal2020uncovering`, `debenedetti2023light`, `rice2020overfitting`, `wang2023better` | panel üyeleri | mevcut | .bib'de var | III-E |
| `sehwag2022robust` | Sehwag ve ark., proxy dağılımları | aday arXiv 2104.09425 | doğrulanmadı | III-E (Sehwag2021Proxy) |
| `addepalli2022efficient` | Addepalli ve ark., NeurIPS 2022 | aday arXiv 2210.15318 | doğrulanmadı | III-E |
| `rade2022reducing` | Rade, Moosavi-Dezfooli, ICLR 2022 (helper-based AT) | kimlik atif-kontrol bulacak | doğrulanmadı | III-E |
| `pang2022robustness` | Pang ve ark., ICML 2022 | aday arXiv 2202.10103 | doğrulanmadı | III-E (P9) |
| `jia2022lasat` | Jia ve ark., LAS-AT, CVPR 2022 | aday arXiv 2203.06616 | doğrulanmadı | III-E (P9) |
| `hendrycks2019using` | Hendrycks, Lee, Mazeika, ICML 2019 | aday arXiv 1901.09960 | doğrulanmadı | III-E (P9 ikincil) |
| `salman2020adversarially` | Salman ve ark., NeurIPS 2020 | aday arXiv 2007.08489 | doğrulanmadı | III-E (P8) |
| `chen2024data`, `peng2023robust` | P8 üyeleri | kimlik atif-kontrol bulacak (Peng için aday arXiv 2308.16258) | doğrulanmadı | III-E (P8) |
| `mantel1967detection` | Mantel, Cancer Research 1967 | kimlik atif-kontrol bulacak | doğrulanmadı | III-F (Mantel sınamasının özgün kaynağı) |
| `springer2021little` (isteğe bağlı) | Springer, Mitchell, Kenyon, NeurIPS 2021 | arXiv 2106.02105 | doğrulandı | II-B (hafif gürbüz vekiller) |

Karar: panel üyelerinin özgün makaleleri atif-kontrol turunda doğrulanamazsa model yalnız RobustBench kimliğiyle `\texttt{}` içinde ve `\cite{croce2021robustbench}` ile anılır; uydurma ya da doğrulanmamış künye derlenmiş kaynakçada bırakılmaz. Karar: Mantel (1967) atfı eklenir, çünkü sınama adını taşıyan özgün kaynaktır ve Smouse yalnız kısmi uzantıdır.

## 8. Sınırlılıklar ve dürüstlük beyanları

### 8.1 Tartışma'nın sınırlılık paragrafına (Y4) girecekler

1. Çıkarım tek çift mimariye ve küçük modellere dayanır (ViT-Tiny ve ResNet-18, 32 pikselden 224'e büyütme); yeni hücrelerde koşu sayısı ikidir; Welch aralıkları geniştir (FÖY 1553).
2. V-scr hücresinin temiz doğruluğu (73.01-74.10) öteki hücrelerden (83.39-86.35) düşüktür ve w'su yüksektir; H1'in mimari karşıtlığı tasarım gereği bu farkla birlikte değişir ve iki açıklama ayrılamaz (FÖY 1496-1499, 1505-1513; R09 §7-§8). V-IN'de temiz doğruluk R224 düzeyine çıktığı halde ViT'nin panel benzerliği düşük kalır; bu bir sınama değildir ve fark sayısı föyde yoktur, sayısız yazılır.
3. Yönlü terimin büyüklüğü ve işareti ölçeğe, veri kümesine ve panele bağlıdır: logit ölçekte işaret döner (FÖY 1551, 1603, 1857), CIFAR-100'de K-b çürütülmüştür (1839), XCiT panelinde ρ(V-scr) yaklaşık +0.20'dir (1606), V-IN'nin ρ'su δ dışındadır (1497); H3'ün eşdeğerliği bir ana etki eşdeğerliğidir, hücre başına küçük yönlü terim anlamına gelmez.
4. Başlatma etmeni ağırlık, temiz aşama uzunluğu ve normalizasyon demetidir; normalizasyonun ayrı etkisi tanımlanamaz (ÖK §3).
5. CIFAR-100'de ViT-Tiny temiz doğruluğu panelin altındadır; B9 ViT nicelikleri temiz doğrulukla karışabilir; her-ikisi-doğru duyarlılığı (S9-4) üretilmemiştir (R11 §6 m.4).
6. ImageNetV2 paneli betimseldir: IN satırı iki Singh çiftine, sıfırdan satırı dolaylı kanıtla sıfırdan sayılan tek Liu çiftine dayanır; Mo ViT-B kısa AT'li ve çiftsizdir; panel üyelerinin başlatması doğrulanmamıştır; mimariler 2x2'dekilerden farklıdır (conv gövdeli ViT, ConvNeXt, Swin); ortak önişleme hattı bazı modellerin beklediği hattan ayrılır (fark en çok 1.20 puan, FÖY 1818); ImageNetV2 dağılım kayması w ve T'ye girer (EK §9).
7. Gradyan hizalanması temiz görüntüde tek noktadadır, PGD yolu boyunca değildir; kısmi istatistik yalnız toplamsal ana etkileri ayırır; ilişki gerekli koşuldur (EK §9).
8. TGR özgün ayarıyla ve uyarlanmış biçimde koşulmuştur; adım boyları saldırılar arasında bilinçli olarak farklıdır ve taranmamıştır (ÖK §5 B5).
9. Çarpımsal yön yasası yörüngelerde tutmamıştır (R²(λ = 1) 0.201; FÖY 1759); yasa iddiası yapılmaz.
10. Ayrışım bir özdeşliktir; içerik ölçülen büyüklüklerde ve müdahale yanıtındadır (Caussinus ve Demontis ile yakınlık).
11. Mahmood ve ark. verisinde köşegen beyaz kutu olmadığından w tanımsızdır ve ayrışım kurulamaz (PLAN §12).
12. Eski sınırlılıklardan kalanlar: L2 sonucu protokolü sınar, L2 gürbüzlüğünü değil; sızıntı ablasyonu "weaker question" yanıtlar (kapı C4); mekanizma hesabı "incomplete", "three of the four protocols" (kapı F2).

### 8.2 Ön kayıt paragrafına (Y2, `subsec:prereg`) girecek beyanlar

1. Kayıt öncesinde görülmüş veriler (ÖK §1): C1 3x3 matrisleri, tek tohumlu havuz 8x8 matrisi ve masa çözümlemeleri (σ, ρ, simetrik oran, Hodge, Mahmood, SVHN), sahte 2x2 kod sınaması, smoke matrisleri (n = 200 ve 100, MI ve TGR dahil), smoke temiz doğrulukları. B3 hücrelerinin tam tarifli hiçbir koşusu görülmemiştir.
2. K-b çürütme ölçütünün iki yöne genişletilmesi görülmüş veriden sonra yapılmıştır ve çürütmeyi kolaylaştıran yöndedir (ÖK §1, §8 m.7).
3. Temiz aşama denetiminin ilk epok ölçütüne çevrilmesi smoke doğrulukları görüldükten sonra yapılmıştır; ölçüt bir yükleme denetimidir (ÖK §8 m.17). R224-IN denetiminin referansı tek R224-scr koşusunun ilk epoğudur (n = 1; R09 §7 m.2); karar değişmezdi.
4. B5 öngörü değerinin (≥ 0.5) MI ve TGR smoke matrislerinden önce yazılıp yazılmadığı doğrulanamamaktadır (ÖK §1).
5. Ek ön kayıt dondurulmadan önce ana oturum B2 model tablosunun ρ değerlerine bakmıştır; ek öngörüler dondurulmuş ön kayıttan türetilmiştir (PLAN §13, E6).
6. B9 matrisi koşarken bir başlatma betiği bir kaynağın günlük satırlarını ekrana yazdırmıştır; çözümleme seçim bırakmayan tek çağrıdır (R11 §6 m.2).
7. Ana ön kayıt için sapma kaydı yoktur (R09 §0); ek için sapma yoktur, notlar vardır (R11 §6).
8. Üretilmeyen duyarlılık ve keşifsel çözümlemeler: CIFAR-10'da K-a ve K-b için hiyerarşik bootstrap (FÖY 1607); S9-2, S9-4, S8-1'in D_k ve q_k aralıkları, S8-3 grup jackknife'ı, S8-7, S8-8, S10-1 ile S10-7, B10'un her-ikisi-doğru Mantel'i (R11 §6 m.4).
9. İki ImageNet başlatma kontrol noktasının ImageNet top-1 değeri kayda geçmemiştir (FÖY 1690, 1775).
10. Bütünlük: dondurulmuş çözümleme betiği, hücre tabloları ve ön kayıt gövdelerinin SHA-256 özetleri çözümleme çıktılarıyla ve dondurma kayıtlarıyla eşleşir (FÖY 1684-1686, 2022-2032).

## 9. Föyde bulunmayıp metne giremeyecek kalemler

Bu kalemler hiçbir biçimde, yuvarlanmış ya da yeniden hesaplanmış olarak da metne yazılmaz. Gerekirse ana oturum föye `scripts/build_reference_sheet.py` üzerinden yeni bir alt bölüm ekletir; o zamana kadar cümle sayısız kurulur ya da yazılmaz.

| Kalem | Değer (yalnız tanımak için) | Nerede görüldü | Karar |
|---|---|---|---|
| Hücre farkları σ(V-IN) − σ(V-scr), σ(R224-IN) − σ(R224-scr), σ(V-IN) − σ(R224-IN) | +0.270, +0.009, −0.104 | R09 §8 | Girmez; föy eki önerilir (M9.10 türetilmiş karşıtlıklar) |
| ρ satır farkları ve ρ'da mimari × başlatma etkileşimi | +0.070, −0.064, −0.134 | R09 §8 | Girmez |
| exp(A^σ_scr) yorumu | 0.69 | R09 §8 | Girmez |
| Masa Hodge ayrışımı (yedi model) ve C1 çiftinde potansiyel ile dolaşım payı; logit r_RV | G 0.940, 0.080 ve 0.039, 0.006 | PLAN §12, 04 §4(2) | Girmez; yerine S7 (0.919, FÖY 1569) ve S8-2 (0.890, 1947) |
| Masa havuzunda logit ρ ve ρ_V − ρ_R | −0.265, +0.061, −0.095 | PLAN §12, 04 §4(1) | Girmez; logit yönü B2'nin föydeki logit değerleriyle anlatılır (1603) |
| SVHN'de r_RV | −0.106, −0.076 | 04 §4(4) | Girmez; SVHN hedef-doğru asimetrisi (FÖY 185) kullanılır |
| Masa havuzunda w (55.83, 47.56) | | PLAN §1 | Girmez; Tablo II değerleri (FÖY 28-29) kullanılır |
| CIFAR-100 ile CIFAR-10 simetrik ve yönlü pay ortalamaları | 0.362, 0.365, 0.025, 0.069 | R11 §7 | Girmez; tohum başına değerler (FÖY 1593, 1848) yazılabilir |
| R11 §7 keşifsel B10 değerleri (her-ikisi-doğru c, aile ayıklamalı ve yalnız CNN-CNN Spearman, S10-2 γ farkları) | 0.927... , 0.905..., 0.963..., −0.217... | R11 §7 | Girmez |
| Salman R18 ile R50 kosinüsü ve bırakmalı Spearman | 0.0034, 0.672, 0.898 | R11 §6 | Girmez; GPU denetimi bekleniyor (§11) |
| ImageNet başlatma kontrol noktalarının top-1 değeri | yok | FÖY 1690 | Girmez |
| B5 IN çiftinde korunma oranı | 0.937 | FÖY 1655 | Girmez |
| CIFAR-100 C1 PGD-10 ve AA ortalamaları (eski `tab:cifar100_results`) | 19.30, 11.15, 15.04, 8.87 | eski metin | Girmez; tablo düşer |
| Ek blokların ve B9/B8/B10 adımlarının süreleri | 36 dk, 13 dk 53 s vb. | R11 §2 | Girmez |
| GPU bellek anlık görüntüleri | 10882-11045 MiB, 2804 MiB | R09 §2, R11 §6 | Sayısız, nitel beyan |
| Temiz aşama ilk ve son epok doğrulukları ve referansları | 93.95, 25.22, 38.85, 97.25 vb. | R09 §2 | Girmez; yalnız denetim farkları (FÖY 1472) |
| Kontrol noktalarının toplam boyutu | 40 GB | eski metin | Girmez |
| B9 panelinin RobustBench temiz ve AA değerleri | 53.83/18.95 vb. | EK §4.1 | Girmez; ölçülen temiz doğruluklar (FÖY 1879-1887) |
| Föy Tablo III'ün "run3 fark" sütunu | 8.27, 0.63 vb. | FÖY 52-56 son sütun | Karantina; asla kullanılmaz |

## 10. Hesaplama ayrıntıları için olgular (`sections/04z_computational.tex`, Y4)

Dosya `\subsection{Computational Details}` ve `\label{subsec:computational}` ile başlar; `main.tex` onu §IV'ün sonuna ekler.

| Olgu | Kaynak |
|---|---|
| C1 CIFAR-10 eğitim çiftleri ve değerlendirmeleri RTX 5060 Ti (16 GB); CIFAR-100, SVHN, L2, seçim yörüngeleri, havuz ve bütün konsey blokları (B2-B10) RTX 5090 (32 GB) | `CLAUDE.md` Donanım; eski metin 04:638 |
| PyTorch 2.6.0a0 (NVIDIA nv25.01 kapsayıcısı), CUDA 12.8, timm 1.0.27, numpy 1.26.4, RobustBench `78fcc9e` | `raporlar/konsey_2026-10-29/adeb_eval_pip_freeze.txt`; `CLAUDE.md`. Karar: sürüm dizgeleri sonuç sayısı değildir, `% KAYNAK:` yorumuyla verilir |
| Kapsayıcı `adeb_eval`; ek bloklardan önce D diski bağlamasıyla yeniden kuruldu ve commit edilmiş imaj `adeb_eval:2026-10-30` kullanıldı | `10_konteyner_yeniden_kurulum.md` satır 276 |
| C1 üç tohumlu hattı 21.7 GPU-saat | FÖY 1315-1316 |
| B3 altı yeni koşunun temiz ve AT aşamaları toplam 17.79 sa; AT 36-58 epok, seçilen epoklar 16-38, hepsi erken durmayla, 80 epoklu tavana çarpan yok | FÖY 1452-1457, 1470 |
| AT epok süreleri boş GPU pilotunun 1.05-2.19 katıdır; nedeni kayıtlardan belirlenemez (paylaşım neden olarak sunulmaz); pilot W(80) 20.47 sa, eğitim payı 38.15 sa | FÖY 1478-1485; R09 §7 m.1 |
| GPU zaman zaman başka bir süreçle paylaşılmıştır; çatal regresyonu birebir çıktığından sonuçlar etkilenmemiştir (sayısız) | R11 §6 m.5; FÖY 1793-1796 |
| AA standart yapılandırma (APGD-CE, APGD-T, FAB-T, Square); B6'da test kümesinin ilk 1000 görüntüsü | FÖY 1673; eski metin 04:638 |
| Ek bloklar (B8-B10) özgün matris betiğinin çatallanmış bir kopyasıyla koşulmuş, çatal regresyonu birebir çıkmıştır | FÖY 1789-1796, 2027-2028 |
| Deterministik cuDNN ayarları, tohum 42 | eski metin 04:638 ve 03:192 |

"Ek bloklar 36 dk" ve öteki adım süreleri föyde olmadığından yazılmaz (§9).

## 11. Kelime bütçesi

Ölçü yorum satırları hariç kelimedir (aşağıdaki betik). Bugünkü toplam 19,606'dır (yorumlarla `wc -w` 22,302). Üst sınır bugünkü yorumsuz toplamın yüzde 10 fazlası olan 21,566'dır; kullanıcının "görsel sayısını artırıp içeriği azaltalım" isteği gereği hedef bunun belirgin altındadır.

| Dosya | Şimdi | Hedef | Dosya üst sınırı | Yazar |
|---|---|---|---|---|
| `main.tex` (özet ≤ 250) | 677 | 650 | 720 | Y1 |
| `01_introduction.tex` | 1316 | 1150 | 1300 | Y1 |
| `02_related_work.tex` | 1350 | 1250 | 1450 | Y2 |
| `03_methodology.tex` | 3289 | 3000 | 3400 | Y2 |
| `04_experiments.tex` | 10590 | 7300 | 8000 | Y3 |
| `04z_computational.tex` | 0 | 250 | 300 | Y4 |
| `05_discussion.tex` | 2048 | 1500 | 1700 | Y4 |
| `06_conclusion.tex` | 336 | 300 | 350 | Y1 |
| `07_appendix.tex` | 0 | 1300 | 1500 | Y3 |
| Toplam | 19606 | 16700 | 18720 | |

Sayım betiği (yazar kendi scratchpad'ine `kelime_say.py` olarak kaydeder ve `python3 kelime_say.py /home/firat/projects/adeb_sci_1/paper/manuscript` ile WSL'de koşar):

```python
import re, glob, sys
kok = sys.argv[1] if len(sys.argv) > 1 else "."
tot = 0
for f in [kok + "/main.tex"] + sorted(glob.glob(kok + "/sections/*.tex")):
    t = open(f, encoding="utf-8").read()
    lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
    n = len(" ".join(lines).split())
    tot += n
    print(n, f)
print(tot, "toplam (yorum satirlari haric)")
```

## 12. Yazar ajanlara ortak kurallar

### 12.1 Sayı ve kaynak

Her sayı föyden gelir; satır numarası paragrafın ya da tablonun hemen üstündeki ayrı bir yorum satırında `% FOY:M9.3:1526,1527` biçiminde verilir (bölüm kimliği satır kaymasına karşı). Yorum satırı asla bir metin satırının sonuna eklenmez, çünkü `%` satır sonunu yutar. Korunan eski sayıların eski `% REF:` yorumları kalır, yanına `% FOY:` satırı eklenir. Tasarım sabitleri (ε, α, epok, tohum, batch, parametre sayısı) sonuç değildir; `% KAYNAK: ON_KAYIT §3` ya da `% KAYNAK: CLAUDE.md` yorumuyla verilir. Föyde bulunamayan bir sayı gerekiyorsa cümle sayısız yazılır ve paragraf üstüne `% TODO(foy): <ne gerekiyor>` konur; raporlarda (R09, R11, PLAN) görülen sayılar föyde yoksa kullanılmaz. Karantina: run1, run2, run3, `attention_analysis_run3`, `stat_addendum`, `rev2_blockA` kaynaklı hiçbir sayı yoktur; föy Tablo III'ün "run3 fark" sütunu kullanılmaz. Ölçümler kaçamaksız, yorumlar ölçülü yazılır; olumsuz sonuçlar (K-b(B9), Liu "belirsiz", logit işaret dönüşü, yasanın yörüngelerde tutmaması) saklanmaz.

### 12.2 Üslup

ABD imlası (initialization, normalization, behavior, analyze, modeling). Uzun tire (em dash, LaTeX'te `---`) yok; aralık için "to" ya da en dash `--` yalnız sayı aralığında ve tablo içinde. Koyu ya da italik paragraf başı etiketi yok, `\paragraph{}` yok; gerekirse `\subsubsection`. Gövdede madde listesi (`itemize`, `enumerate`) yok. "In this section we ...", "This paper presents ..." gibi meta cümleler yok. Yasaklı sözcükler ve kalıplar (`raporlar/ai_izi_2026-09-30/rapor.md` ve kullanıcının listesi): Moreover, Furthermore, Additionally, Notably, Importantly, "It is worth noting", "It should be noted", leverage, utilize, delve, comprehensive, crucial, robustly (zarf), pivotal, underscore, shed light, pave the way, novel (bölüm başına en çok bir, tercihen hiç), "state-of-the-art" (karşılaştırma kıyası olmadan). "X, not Y" tiki ve "rather than" ile "instead of" kalıbı: gerçek bir karşıtlık değilse kullanılmaz, bölüm başına en çok iki (tek istisna §12.4'teki kapı korumalı ifade). Yazarın dürüstlüğünü duyuran cümleler ("we are careful to", "we deliberately") ve paragraf sonu vecizeleri yok. Ana sayıların bölümler arasında tekrarı yok: bir sayı özette, bir kez gövdede, gerekirse bir kez tartışmada. Üçlü sıralama alışkanlığı, simetrik paragraf biçimleri, noktalı virgül yığını, "First, ... Second, ..." yanlış numaralaması yok. Cümle ve paragraf uzunlukları değişkendir. Biçim: `Table~\ref{}`, `Figure~\ref{}`, `Section~\ref{}`, `Equation~\eqref{}`; kaynakça `\cite{}` (paket `cite`, natbib yok); `\cite` yalnız `.bib`'de bulunan ya da §7 tablosundaki anahtarla; yeni `hyperref` ya da `subcaption` eklenmez (`main.tex` 9-10 yorumu). Her `\label` en az bir kez gönderilir. Şekil altyazıları 2-4 cümle.

### 12.3 Derleme, sayım ve kapı komutları

Derleme (her yazar kendi değişikliğinden sonra; 0 hata, 0 tanımsız gönderme hedeflenir, yalnız henüz `.bib`'e girmemiş §7 anahtarlarının atıf uyarısı kabul edilir):

```bash
wsl.exe -d Ubuntu-22.04 -- bash -lc "bash /home/firat/projects/adeb_sci_1/scripts/derle_en.sh"
wsl.exe -d Ubuntu-22.04 -- bash -lc "bash /home/firat/projects/adeb_sci_1/scripts/compile_check.sh"
```

Üslup sayacı (sinyaldir, karar göz okumasıyladır):

```bash
wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1/paper/manuscript && python3 ~/.claude/skills/ai-izi/ai_izi_tara.py sections/<dosya>.tex"
```

Kapılar (kapsayıcıda; tek tek ya da hepsi):

```bash
wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && bash scripts/kapilar.sh"
wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && docker exec -w /workspace adeb_eval python scripts/check_manuscript_claims.py"
wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && docker exec -w /workspace adeb_eval python scripts/check_abstract_body.py"
```

Beklenen kapı durumu: `check_abstract_body` (Y1) ve `check_manuscript_claims` (hepsi) GEÇMELİ; `verify_manuscript_numbers` eski taşıyıcı sayılar çıktığı için EKSİK raporlar (beklenir, yazar listeyi raporlar, betiğe dokunmaz); `check_en_tr_mirror`, `bildiri_tutarlilik` ve `gonderim_tutarlilik` TR aynası ve başlık değişikliği yüzünden kalır (beklenir); `check_pdf_render` ve `check_pdf_typeset` derleme sonrası GEÇMELİ. Hiçbir yazar kapı betiğini, föyü ya da `build_reference_sheet.py`'yi değiştirmez; kapı güncellemesi ayrı bir kod-mimar işidir (§13).

### 12.4 Kapı korumalı ifadeler

`check_manuscript_claims.py` aşağıdaki dizgeleri arar. İçerik kısaltılırken bunlar sorumlu yazarın dosyasında doğru bir bağlamda kalır.

| Kapı | Aranan | Sorumlu ve yer |
|---|---|---|
| A | "CIFAR-100" | Herkes |
| B1, B2, B3 | "we have not measured that dependence", "A controlled leakage ablation would settle", "Three sources of variance" YOK | Herkes |
| B3b | "four sources of variance" | Y3, Ek B |
| C1 | "0.22", "0.48", "1.58", "2.85" | Y3: 0.22 ve 0.48 Ek C, 2.85 Ek B, 1.58 IV-I (temiz ViT hedefinde p = 1 artığı) |
| C2 | "$25$ epochs" ve "0.32" | Y3, Ek B |
| C3 | "not testable in this design" | Y3, Ek C |
| C4 | "weaker question" | Y4, sınırlılıklar |
| D1 | "all three predictions" ailesi YOK | Herkes |
| D2 | "deliberately not as a ratio to seed-level dispersion" | Y3, Ek B |
| E1 | "identity" ve `eq:raw_identity` | Y2 (03), Y3 (IV-I) |
| E2 | "0.989" ve "1.000" | Y2 ya da Y3 |
| E3 | "almost perfectly explained by the clean error" YOK | Herkes |
| F1 | "second driver tied to" ve "second and partly opposing term" | Y4 (sınırlılıklar) ve Y3 (IV-I) |
| F2 | "incomplete" ve "three of the four protocols" | Y4, sınırlılıklar |
| G1 | CIFAR-10, CIFAR-100 ve SVHN birlikte geçiyorsa "covers three datasets" | Y1 (sonuç) ya da Y4 (sınırlılıklar): "Our training covers three datasets; ImageNetV2 enters only through independently trained checkpoints" biçiminde doğru tutulur |
| G2 | "covers one dataset" YOK | Herkes |
| I1 | "we report the slope rather than a correlation" | Y3, Ek C (üslup kuralının tek istisnası) |
| T4 | `e\,p + r_{\text{cond}}` VAR, "primary transfer metric" YOK | Y2, `eq:general_identity` aynen kalır |

Karar: gösterim kapı T4 yüzünden protokol katmanında `r_{\text{raw}}`, `r_{\text{cond}}` olarak korunur ve `r_{\text{cond}} = T_{ij}` bir kez yazılır, çünkü kapı güncellemesi bu turun işi değildir ve yönlü artık her zaman alt indisle (`r_{ij}`) yazıldığında karışıklık sınırlıdır.

### 12.5 Okunacaklar

Her yazar şunları okur: bu brif; FÖY'ün kendi bölümünü ilgilendiren satırları; ÖK §2-§6; EK §4-§6, §9, §11; kendi dosyası ve iki komşu dosyası; R09 §7-§8 ve R11 §6-§8 (yalnız yorum ve sınırlılık için; sayılar föyden). Y2 ayrıca `01_oneri_P3_kuram_olcum.md` satır 15-27 (önermeler), `02_literatur.md` ve `06_ek_deney_literatur.md` (atıf bağlamları).

### 12.6 TR aynası

`paper/manuscript_tr/` bu turda değişmez. EN bittikten, hakem paneli ve atif-kontrol geçtikten sonra ayrı bir turda akademik-turkce skill'iyle eşitlenir.

## 13. İş bölümü ve çakışma kuralı

Aynı dosyaya iki ajan yazmaz. Bir yazar başka yazarın dosyasında değişiklik gerektiren bir şey görürse dosyaya dokunmaz, son mesajında "öteki dosyalar için istekler" başlığında yazar.

| Ajan | Dosyalar (yalnız bunlar) | Tanımladığı etiketler |
|---|---|---|
| Y1 | `main.tex` (başlık, özet, anahtar kelimeler, `\input`/`\InputIfFileExists` satırları, Data Availability), `macros_konsey.tex` (yeni), `sections/01_introduction.tex`, `sections/06_conclusion.tex` | `sec:introduction`, `sec:conclusion` |
| Y2 | `sections/02_related_work.tex`, `sections/03_methodology.tex`, `references.bib` (yalnız ekleme) | `sec:related_work`, `subsec:rw_robustness`, `subsec:rw_transfer`, `subsec:rw_decomposition`, `subsec:rw_protocols`, `sec:methodology`, `fig:study_overview`, `subsec:setup`, `subsec:attack_methods`, `subsec:training`, `subsec:design`, `tab:design`, `subsec:metrics`, `tab:protocol_masks`, `eq:general_identity`, `eq:raw_identity`, `subsec:decomposition_def`, `eq:decomp`, `eq:r_def`, `eq:tau_def`, `eq:panel_def`, `prop:identifiability`, `prop:hscale`, `fig:decomposition_schematic`, `subsec:panels`, `subsec:gradcos_def`, `eq:cij`, `subsec:statistics`, `tab:registry`, `subsec:prereg` |
| Y3 | `sections/04_experiments.tex`, `sections/07_appendix.tex` (yeni) | `sec:experiments`, `subsec:robustness`, `tab:main_results`, `subsec:pair_decomposition`, `tab:pair_decomposition`, `tab:external_pool`, `subsec:panel`, `tab:panel_tests`, `fig:source_gap_split`, `fig:similarity_matrix`, `subsec:twobytwo`, `tab:cells`, `tab:fb4`, `fig:cells_interaction`, `subsec:attack_side`, `tab:attack_side`, `fig:attack_side`, `subsec:imagenet`, `tab:imagenet`, `subsec:gradcos`, `tab:mantel`, `fig:gradient_alignment`, `subsec:scale`, `fig:estimates_forest`, `subsec:transfer`, `tab:protocol_settings`, `fig:protocol_sets`, `fig:spread_clean_gap`, `app:behavior`, `app:selection`, `app:registrations`, `subsec:selection`, `tab:gradient`, `tab:spatial`, `tab:feature_degradation`, `fig:epsilon_sweep`, `fig:feature_degradation` |
| Y4 | `sections/05_discussion.tex`, `sections/04z_computational.tex` (yeni) | `sec:discussion`, `subsec:findings`, `subsec:prior`, `subsec:implications`, `subsec:limitations`, `subsec:future`, `subsec:computational` |
| Şekil ajanı (gorsel-uretici, opus) | `paper/figures/konsey/` altındaki her şey (betikler, PDF, PNG, kanıt, TikZ kopyası) | yok |

Bu tablo dışındaki eski etiketler (`subsubsec:matrix`, `subsec:source_target`, `subsec:cifar100`, `subsec:svhn`, `subsec:l2`, `subsubsec:spread_gap`, `subsec:external`, `subsec:readings`, `subsec:gradient`, `subsubsec:spatial`, `subsec:attention`, `subsec:tgr`, `subsec:statistics_results`, `subsec:threat_model`, `subsec:architectures`, `subsec:defense_methods`, `subsec:attacks`, `subsec:defenses`, `subsec:cnn_robustness`, `subsec:vit_robustness`, `subsec:transfer_related`, `subsec:gap`, `fig:gradient_analysis`, `fig:gradient_heatmap`, `fig:attention_layers`, `tab:conditional`, `tab:transfer_protocols`, `tab:transfer_matrix`, `tab:source_target`, `tab:cifar100_results`, `tab:l2_results`, `tab:tgr`) kalkar ve hiçbir dosyada gönderilmez. Bir yazar yalnız bu tablodaki etiketlere gönderme yapar.

Sıralama: Y1'in ilk işi `macros_konsey.tex` ve `main.tex`'teki `\input{macros_konsey}` ile iki `\InputIfFileExists` satırıdır; Y2'nin ilk işi `references.bib`'e §7 anahtarlarını eklemektir. Öteki yazarlar bunları beklemeden yazmaya başlar ama derlemeyi `macros_konsey.tex` oluştuktan sonra yapar. Şekil ajanı yazarlarla paralel çalışır; şekil hazır değilse §6.9'daki yer tutucu kullanılır. Bu turdan sonra sırayla şunlar gelir: kapı güncellemesi (kod-mimar; yeni korumalı ifade önerisi: "on the log scale", "against a CNN panel", "descriptive", "necessary condition", "consistent with expectation", "uncertain", K-b(B9) "refuted"), atif-kontrol, tek turlu hakem paneli, TR aynası, visio-cizici şekil görevi.

Makaleden önce kapanması gereken açık işler (yazarların işi değildir, ana oturum içindir): IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 kosinüsünün GPU denetimi (R11 §6; o zamana kadar IV-G'nin ImageNetV2 cümlesinin üstüne `% TODO(B10-R18R50)` konur); B9 için her-ikisi-doğru duyarlılığı S9-4 (R11 §6 m.4, önerilir); ImageNet top-1 değerlerinin kaydı; istenirse §9'daki türetilmiş hücre farkları için föy eki.
