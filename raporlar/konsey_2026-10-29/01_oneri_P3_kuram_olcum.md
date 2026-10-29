# Konsey önerisi P3: kuram ve ölçüm merceği (29.10.2026)

Hazırlayan: öneri sahibi araştırmacı (opus alt ajan). Kısaltmalar: `FÖY` = `results/C1_REFERANS_FOYU.md`; `M1` = `raporlar/konsey_2026-10-29/_p3_potansiyel_masa.json`; `M2` = `_p3_yorunge_gurbuzluk_masa.json`; `M3` = `_p3_havuz_gurbuzluk_yasasi.json`; `M4` = `_p3_carpimsal_yasa_masa.json` (dördü de aynı klasörde, aynı adlı `.py` betikleriyle bu oturumda üretildi; yeni ölçüm ve GPU yoktur, girdiler yalnız `results/q1/*` ve `results/c1_*`); `HÜKÜM` = `raporlar/hakem_lecun_2026-10-04/00_LECUN_HUKUM.md`. tc = hedef-doğru, bc = her-ikisi-doğru, w = modelin kendi beyaz kutu PGD-10 koşullu yanıltma oranı (matrisin köşegeni), ρ = beyaz kutu PGD-10 doğruluğu.

## 1. Manşet iddia

Çekişmeli eğitilmiş modellerde transferin yönünü gürbüzlük, miktarını mimari belirler: herhangi iki model arasındaki hedef-doğru transfer oranlarının oranı, serbest parametre olmadan hedeflerin beyaz kutu kırılganlık oranına eşittir, log(T_ij / T_ji) = log(w_j / w_i); bu yüzden CNN ile ViT arasındaki asimetri gürbüzlük sırası döndüğünde döner ve mimari yalnız simetrik bir transfer verimi τ_ij üzerinden etkili olur.

Önerilen başlık (tutarsa): "Robustness Sets the Direction, Architecture Sets the Amount: A Vulnerability–Similarity Law for Adversarial Transfer between CNNs and Vision Transformers".

Mevcut manşet (koşullama kümesi, kesin düzeltme, kaynak etkisi okuması) bu merceğe göre iki parçada güçlü değildir. Özdeşlik kuruluş gereği doğrudur ve içerik yalnız p'dir (HÜKÜM M3); kaynak etkisi okuması ise aşağıdaki Önerme 1'e göre bu tasarımda tanımlanamaz ve Önerme 2'nin daha yalın açıklamasıyla birebir aynı deseni üretir. Bu yüzden değiştirilmesi, protokol çalışmasının ise ölçüm katmanı olarak korunması önerilmektedir: yasanın tam tuttuğu koşullama kümesi tc'dir, ham protokol bilinen bir ayar dönüşümü ekler, bc ise çift düzeyinde bir bileşim terimi ekler (Önerme 3).

## 2. Kuram: üç önerme ve kanıt taslakları

### Önerme 1 (tanımlanabilirlik)

K modelli tam bir transfer matrisinde T, ters-simetrik kısım A = T − Tᵀ ve simetrik kısım S olarak ortogonal ayrışır. (a) A'nın en küçük kareler ayrışımı A_ij = δ_i − δ_j + c_ij biçimindedir; δ_i = (1/K)Σ_j A_ij model potansiyeli (K − 1 serbestlik), c dolaşımdır ((K − 1)(K − 2)/2 serbestlik; HodgeRank, Jiang ve ark., arXiv 0811.1067, DOI 10.1007/s10107-010-0419-x). K = 2'de dolaşım serbestliği sıfırdır ve asimetrinin sınanabilir içeriği yoktur; tezin 6 Ekim hükmü bu durumun önermesidir. (b) Toplamsal uydurmada bir çiftin kaynak payı ½[(δ_i − δ_j) + (s_i − s_j)], hedef payı ½[(δ_i − δ_j) − (s_i − s_j)] olur; s simetrik kısımdan gelir, dolayısıyla bölüşüm simetrik kısmın toplamsal olduğu varsayımına dayanır. (c) Bir ailede tek model varsa (bizde tek saf ViT) aynı-aile benzerlik terimi γ·1[i, j ∈ C] köşegen dışında 1 − 1[i = V] − 1[j = V] biçimine indirgenir, yani toplamsaldır; uydurma onu α_V ve β_V'ye birlikte −γ olarak yükler. Sonuç kesindir: CNN'in kaynak payı +γ, hedef payı −γ kayar, asimetri değişmez. Kanıt doğrudan yerine koymadır.

Bu önermenin deneysel içeriği bugünden görünür. Havuzda tanımlanabilen benzerlik terimleri sıfırdan büyüktür: sağlam iki WRN-28-10 çifti için +5.23 [4.86; 5.61], ResNet18_AT ile PRN18 çifti için +2.84 [2.48; 3.17], ViT-Tiny ile XCiT için +1.07 [0.72; 1.42] puan (tc, oran; `M1.havuz_cifar10.benzerlik.tc.oran`). Makalenin 3x3 kaynak payı +5.13 ve hedef payı −2.03'tür (FÖY:390); bölüşümün eşitlendiği γ değeri (5.13 + 2.03)/2 = 3.58 puandır (türetilmiş), yani CNN'ler arası benzerlik bu büyüklükteyse "kaynak etkisi" okuması tümüyle benzerlikten doğar. Yanlılık işaret olarak makalenin lehinedir; en sert hakem bunu bulur.

### Önerme 2 (kırılganlık-benzerlik ayrışımı ve yön yasası)

T_ij = w_j τ_ij ve τ_ij = τ_ji ise log(T_ij/T_ji) = log w_j − log w_i olur: asimetri log ölçekte dolaşımsızdır ve potansiyeli ölçülmüş log w'dir, eğim λ = 1'dir, uydurulacak parametre yoktur. Log ölçekte toplamsal uydurma yapıldığında log τ_ij = m + c_i + c_j + ε_ij yazılırsa kaynak etkisi α_i = c_i (benzerlik merkeziliği), hedef etkisi β_j = log w_j + c_j olur. Herkese benzemeyen bir model (c düşük) hiçbir kaynak özelliği taşımadan "zayıf kaynak" görünür. Önerme 1(c) ile birlikte bu, makalenin ViT kaynak etkisinin ViT'nin düşük benzerlik merkeziliğinin başka bir adı olabileceğini gösterir. Sınanacak kısım λ = 1 ve τ simetrisidir; ayrışımın kendisi değil.

### Önerme 3 (protokol ayarı)

h = −log(1 − T) ölçeğinde toplam olasılık özdeşliği h^ham_ij − h^tc_ij = −log(temiz doğruluk_j) + g_ij verir; g_ij = −log(1 + e_j(1 − p_ij)/((1 − e_j)(1 − T^tc_ij))) ve p = 1'de sıfırdır. Bu nedenle ham ile tc arasında kaynak etkileri, dolaşım ve tüm simetrik benzerlik terimleri değişmez; yalnız hedef potansiyelleri kapalı biçimde kayar. bc böyle bir ayar dönüşümü değildir (kaynak temiz doğruluğuna bağlı çift terimi ekler). Havuzda en büyük |g| 0.0044'tür; h ölçeğinde ham ile tc kaynak etkileri tc kaynak etkileri SD'sinin %1.6'sı, dolaşım %0.9'u kadar ayrışır, oran ölçeğinde bu değerler %31.6 ve %17.9'dur; bc ile tc arasında h ölçeğinde %36.3 ve %17.7'dir (`M1.havuz_cifar10.ayar_testi`). Özdeşlik böylece "tanım gereği doğru bir eşitlik" olmaktan çıkar ve hangi sonuçların protokolden bağımsız olduğunu söyleyen bir sınıflandırma aracına dönüşür.

## 3. Neden önemsiz ya da bilinen değil, en sert hakem ne der

Hakemin ilk itirazı "gürbüz hedefe az transfer olur, bu bilinir" olacaktır. Demontis ve ark. (arXiv 1809.02861, USENIX Security 2019) transferi hedefin içsel kırılganlığı ile vekil modelin karmaşıklığına bağlar; yön yasası daha keskin ve çürütülebilir bir şey söyler: çekişmeli eğitilmiş modellerde kaynak, simetrik τ dışında yönlü hiçbir katkı yapmaz ve ölçek katsayısı 1'dir. Kaynak tarafının yönlü katkısı olsaydı (T_ij = q_i w_j τ_ij), log oranına log(q_i/q_j) eklenir ve λ = 1 uyumu bozulurdu. Awad ve ark. (arXiv 2512.02830) çekişmeli eğitilmiş kaynakların daha iyi aktardığını bildirir; bu bulgu bizim çerçevede τ'ya, yani simetrik kısma düşer ve yön yasasıyla çelişmez.

İkinci itiraz "w köşegenden alınıyor, döngüsel" olacaktır. Yasa köşegen dışı iki hücreyi, başka modellerin pertürbasyonlarıyla ölçülmüş iki köşegen hücreye bağlar; pozitif rastgele bir matriste λ'nın 1 çıkması için neden yoktur. "Tek ViT, yalnız CIFAR, geçici yörünge modelleri" itirazını Blok 2-4 kapatır.

## 4. Mevcut kanıt (yeni ölçüm yok)

| Sınama | Sonuç | Kaynak |
|---|---|---|
| Havuz, 7 AT modeli, 21 çift, yön yasası λ = 1 sabit | λ uydurması 1.015; R² (λ = 1) 0.953; işaret 21/21 | `M4.havuz_AT7` |
| C1 3x3, üç çift | λ 0.885 ile 0.932; R² (λ = 1) 0.963 ile 0.973; 3/3 | `M4.c10_3x3` |
| CIFAR-100 3x3, üç çift | λ 1.147 ile 1.245; R² (λ = 1) 0.907 ile 0.960; 3/3 | `M4.c100_3x3` |
| Simetrik verim τ, havuz | ViT'li 6 çift 0.322 ile 0.372; diğer 15 çift 0.451 ile 0.749 (örtüşmez); CNN-XCiT 0.451 ile 0.598 | `M4.havuz_AT7.tau_ciftler` |
| Doğrusal biçim A_ij = κ(ρ_i − ρ_j), havuz tc | κ 0.373; R² 0.950; 21/21; ViT-Tiny potansiyel artığı +0.67 puan (CNN çizgisinin üstünde) | `M3.sonuc.target_correct.AT7` |
| Potansiyel payı (Hodge), havuz tc | oran 0.929 [0.922; 0.935], logit 0.991, h 0.904; rastgele beklenti 0.25; AT7 oran 0.977 | `M1.havuz_cifar10.hodge` |
| Sabit mimaride işaret dönüşü, CIFAR-10 | ResNet-18 E2 epok 1 (PGD 16.90 / 15.68 / 16.70, ViT eşi 32.73 / 32.46 / 32.89): A_tc −7.68 / −8.53 / −8.31, A_bc −3.66 / −4.32 / −4.71; epok 11'den sonra pozitif | `M2.kayitlar` |
| Yörüngeler, A_tc ~ ΔPGD doğruluğu | CIFAR-10: eğim 0.426, kesişim −0.28, r 0.982, işaret 66/66; CIFAR-100: 0.974, −3.03, r 0.963, 32/34 | `M2.ozet.*.target_correct` |
| Yörüngeler, log oran ~ log w oranı | r 0.958, kesişim 0.11, işaret 92/100; ama eğim 1.46 (C10) ve 2.07 (C100), λ = 1'den sapar | `M4.A_kolu` |

Tablonun iki olumsuz satırı saklanmamalıdır. Birincisi, yörünge kontrol noktalarında yön tutar ama büyüklük λ = 1'in iki katına kadar çıkar; yakınsamamış modellerde τ gürbüzlükle birlikte değişiyor olabilir. İkincisi, CIFAR-10 yörüngelerinde w'ye göre eşleşmiş ResNet noktalarında A_tc +1.33 ile +3.46 arasında kalır (`M2.kayitlar`, ResNet epok 11-61), yani ρ'ya göre doğrusal biçim burada w oranından daha iyi tutar (66/66 ile 59/66). Hangi gürbüzlük değişkeninin yasayı taşıdığı Blok 2'de ayrıştırılacaktır.

Kapsam sınırı da veridedir. Standart eğitimli modellerde w doyar (yaklaşık %100) ve yasa simetri öngörür; oysa bizim temiz çiftte ViT-Tiny net ihracatçıdır (tc asimetrisi −4.49±0.85, FÖY:1403) ve Mahmood ve ark.'nın ön eğitimli modellerinde de ViT güçlü taraftır (FÖY:660-663). Buradan literatürdeki zıt yönler için ön eğitim gerektirmeyen bir uzlaşma çıkar: gürbüzlük farkı varken yönü gürbüzlük, yokken mimariye bağlı bir artık belirler; Blok 3'teki ön eğitimli ViT bunu da sınar.

Tez çelişkisi böylece çözülür: tezin "kaynak ve hedef etkisi ayrıştırılamıyor" cümlesi Önerme 1'in K = 2 ve tek-ViT hâlidir ve doğrudur; makale kaynak etkisi okumasını bırakıp tanımlanabilir nicelik olan potansiyel ile simetrik τ'yu raporlar.

## 5. Deney blokları

Süreler `00_durum_dosyasi.md` Bölüm 5'teki günlük ölçümlerinden türetilmiştir; matris için 8x8 (13.5 dk) ve 3x3 (3.6-4.5 dk) ölçümlerinden doğrusal kestirimle kaynak başına 1.15 dk saldırı ve hücre başına 0.07 dk değerlendirme alınmıştır. GPU paylaşımlı olduğu için üst sınırlar da verilir.

### Blok 1, masa başı ve ön kayıt (yapıldı, 0 GPU-saat)

Dört betik ve JSON yukarıdadır. Ana oturum, aşağıdaki öngörü ve çürütme ölçütlerini Blok 2'den önce tarihli bir ön kayıt dosyasına yazıp işlemelidir.

### Blok 2, tohum-çaprazlı ve yoğun yörüngeli matris (eğitimsiz, kullanıcı başlatır, ≤ 2 GPU-saat)

Amaç: λ'yı yeni çiftlerde sınamak, ViT tohumları arası τ'yu (aynı tür benzerliği) ölçmek, sıfır geçişini yerinde bulmak. CIFAR-10 modelleri: C1 ResNet-18 ve ViT-Tiny, her biri 3 tohum; Wong2020, Engstrom2019, Carmon2019, Gowal2020, XCiT-S12, Standard; ResNet-18 E2 s1001 epok 2, 3, 4, 5, 6, 7, 8, 10 (`models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs/`), toplam 20 model. CIFAR-100: C1 eşi 3+3 model, Pang2022 WRN ve ResNet-18 E1 s1001 epok 1-6, toplam 13 model. Saldırı PGD-10 L∞, ε = 8/255, n = 10.000, tohum 42, örnek bazlı kayıt; dört protokol `src/analysis/protokoller.py` maskeleriyle. Süre: 20 × (1.15 + 20 × 0.07) ≈ 51 dk ve 13 × (1.15 + 13 × 0.07) ≈ 27 dk. Öngörü P5: ResNet epokları ViT eşini gürbüzlükte geçerken A_tc işaret değiştirir. İki biçim farklı yer öngörür: ρ eşleşmesi epok 6 civarındadır (PGD 32.81 / temiz 82.39, ViT eşi 32.73 / 74.10; `results/q1/e2/testcurve_resnet18_s1001.npz`, `results/c1_seeds/c1_seed_summary.json`), w eşleşmesi ise epok 11'in ötesindedir; epok 11'de A_tc zaten +1.33'tür (`M2`), bu doğrusal ρ biçimini öne çıkarır. Çürütme: geçiş hiç olmaz ya da iki eşleşme noktasının ±1 epok dışında kalır. İki sonuç da bilgilidir: hangisi tutarsa makalenin nicel yasası odur. Ek ölçüm: τ(ViT_s1, ViT_s2) ile τ(ViT, CNN) karşılaştırması.

### Blok 3, beş eğitim (kullanıcı başlatır, ≤ 26 GPU-saat)

Amaç: yasayı yakınsamış modellerde ve iki yeni saf ViT türünde dış örneklemle sınamak. Tarif C1 ile aynıdır (`scripts/run_c1_pipeline.sh`: temiz ön eğitim, karışık kayıplı AT, lr 1e-3, sabır 20, `data/val_split_indices.json`).

| Kod | Model | Gerekçe | Süre (beklenen / üst sınır) | Süre kaynağı |
|---|---|---|---|---|
| T1, T2 | ViT-Tiny, ImageNet ön eğitimli başlangıç (`--timm-pretrained`), temiz ince ayar 50 epok + AT, tohum 2101, 2102 | ikinci saf ViT türü, farklı rejim ve muhtemelen farklı gürbüzlük (A4, A6) | 2.2 / 6.5 sa her biri | temiz 200 epok 1.31-1.38 sa (`logs/Q1_e2_clean_vit_tiny_200x.log`); AT erken durdurmalı 1.82-1.89 sa, tam 100 epok 6.01-6.15 sa (durum §5) |
| T3 | CIFAR-yerli ViT (`vit_cifar_tiny`, yama 4, 32x32), sıfırdan, tohum 2201 | üçüncü saf ViT türü, büyütmesiz yamalama | 4.0 / 7.3 sa | temiz 200 epok 107.28 dk ve AT yaklaşık 3.3 dk/epok, eski GPU (`logs/vit_cifar_tiny_clean.log`, `logs/vit_cifar_tiny_at.log`), üst sınır sayıldı |
| T4 | ResNet-18, AT ε_eğitim = 2/255, C1 s1001 temiz başlangıç, tohum 1101 | yakınsamış ve ViT-Tiny'den az gürbüz CNN (çaprazlama) | 1.4 / 2.8 sa | ResNet AT 1.24-1.46 sa erken durdurmalı, 2.66-2.78 sa tam (durum §5) |
| T5 | ResNet-18, AT ε_eğitim = 4/255, aynı başlangıç, tohum 1102 | gürbüzlükte ViT-Tiny'ye yakın CNN (doz) | 1.4 / 2.8 sa | aynı |

Toplam beklenen yaklaşık 11 sa, üst sınır 25.9 sa. T1'in timm ağırlık etiketinin (augreg in21k→in1k) konteynerde doğrulanması gerekir; doğrulanmadı. Öngörü P2: T4'ün w'si ViT-Tiny'ninkinden büyük olacak ve üç ViT tohumuna karşı A_tc < 0 olacaktır (yakınsamış modelde işaret dönüşü). Çürütme: T4 daha az gürbüz olduğu hâlde A_tc ≥ 0 ya da %95 aralık sıfırı içerir. P2 çürürse epok-1 dönüşü geçici modele özgüdür ve yön mimariye bağlı bir bileşen taşır; bu da güçlü ve yayımlanabilir bir sonuçtur.

### Blok 4, son matris ve sağlamlık (kullanıcı başlatır, ≤ 3.5 GPU-saat)

Blok 2'nin 12 yakınsamış CIFAR-10 modeli (epok kontrol noktaları hariç) ile T1-T5, toplam 17 model, PGD-10 L∞ (17 × (1.15 + 17 × 0.07) ≈ 40 dk); aynı matris L2 PGD ile (`--norm l2`, ≈ 40 dk, saldırı duyarlılığı); yeni beş model için AutoAttack n = 2.000 (C1 çift başına n = 10.000 için 2.75-3.05 sa, TIMING.md; ölçekli kestirim model başına ≈ 0.3 sa) ρ'nun saldırıya duyarlılığı için. Öngörü P1 (birincil): eski 7 modelin dışında kalan bütün yeni çiftlerde λ ∈ [0.77; 1.30] (|log λ| ≤ log 1.3, mevcut yakınsamış matrislerin 0.885-1.245 aralığından önceden sabitlenir), R² (λ = 1) ≥ 0.85, |log(w_j/w_i)| ≥ 0.10 olan çiftlerde işaret uyumu ≥ %90. Çürütme: λ'nın %95 aralığı bölgenin tümüyle dışında, ya da R² < 0.70, ya da işaret uyumu < %80. Öngörü P3: her yeni ViT türü için yönlü artık r_V = ortalama[log(T_CV/T_VC) − log(w_V/w_C)] eşdeğerlik sınırı ±0.10 içindedir (yaklaşık ±2 puan). Çürütme: r_V'nin %90 aralığı sınırı aşar. Öngörü P4 (ikincil, iki yönlü): farklı saf ViT türleri arası τ, ViT-CNN τ'sundan en az 0.10 büyükse aile blok yapısı vardır; değilse ViT-Tiny kendine özgüdür. İki sonuç da makalede "mimari miktarı nasıl belirler" bölümünü doldurur.

### Blok 5, ImageNet dış sınaması (isteğe bağlı, lisanslı veri, yalnız kullanıcı başlatır, bütçeye sayılmadı)

RobustBench ImageNet L∞ kataloğundan 5-6 CNN ve dönüştürücü, doğrulama kümesinden 5.000 görüntü; P1 ve P3 aynen. İndirme 1 GB'ı aşar.

## 6. İstatistik çözümleme planı

Kestirilen nicelikler: λ (log oranın log w oranına kesişimsiz eğimi) ve R² (λ = 1); çaprazlama çiftlerinde A_tc ve log oranı; tür başına yönlü artık r_V; tür çiftleri için log τ. Hücre düzeyi belirsizlik, bütün hücrelerde aynı görüntü indeksleriyle ortak görüntü bootstrap'ıyla (B = 2.000) hesaplanır; Blok 1 betiği bunu B = 400 ile yapar. Çiftler modelleri paylaştığı için λ'nın model düzeyi belirsizliği birini-bırak jackknife ile, aile ve tür iddialarının birimi ise model türüdür: tohumlar tür içi tekrar sayılır, aile karşıtlıkları tür etiketlerinin kesin permütasyonuyla sınanır (9 türde ulaşılabilir en küçük p 1/126). Birincil hipotezler P1, P2 (tek yönlü) ve P3 (TOST) Holm düzeltmesiyle α = 0.05'te; P4, P5 ve bütün protokol, ölçek ve saldırı varyantları betimseldir. Birincil protokol tc'dir, çünkü w tc koşulludur; bc ve ham sonuçlar Önerme 3'ün dönüşümüyle birlikte duyarlılık olarak verilir. Birincil ölçek log orandır; oran, logit ve h ölçeğindeki Hodge payları ek tablodadır. Güç hesabı yapılmaz; ulaşılabilir en küçük p'ler yazılır.

## 7. Başlık, özet ve katkılarda değişiklik

Başlık Bölüm 1'deki gibi olur. Özet şu sırayı izler: (i) transfer asimetrisinin yalnız model potansiyelini tanımladığı ve tek ViT'li tasarımda kaynak-hedef bölüşümünün aile benzerliğiyle kesin olarak karıştığı (Önerme 1); (ii) yön yasası, sıfır serbest parametreyle havuzda R² 0.953 ve 21/21, 3x3'lerde ve yeni modellerde dış örneklem sonucu; (iii) sabit mimaride ve yakınsamış çaprazlanmış modellerde işaret dönüşü; (iv) mimarinin simetrik τ'da toplandığı; (v) koşullama kümesinin rolü: yasa tc'de tam tutar, ham protokol bilinen bir hedef potansiyeli kayması, bc bir bileşim terimi ekler; (vi) standart eğitimde w doyduğu için yasanın kapsam dışına düştüğü ve orada ViT'nin net ihracatçı olduğu. Katkılarda "kaynak etkisi" maddesinin yerini Önerme 1-2 ve çaprazlama alır; özdeşlik ve dört protokol Önerme 3 olarak ölçüm katmanına iner, 4.4-19.4 yayılımı, 9.21 ve 3.91 yöntem bölümünde kalır.

## 8. İddia tutmazsa geri çekilme

P1 çürürse yasa yalnız bugünkü yedi modelde gözlemsel bir düzenlilik olarak raporlanır ve makale şu iddiaya çekilir: asimetri yalnız bir model potansiyelini tanımlar, kaynak-hedef bölüşümü ≥ 2 tür içermeyen tasarımlarda aile benzerliğiyle kesin olarak karışır ve yeni türler bu potansiyelin gürbüzlükle açıklanmayan bir mimari bileşen taşıdığını gösterir; büyüklüğü r_V ile verilir. Başlık bu durumda "A Directional Architecture Term in CNN–ViT Adversarial Transfer That Survives Robustness Matching" olur. P2 çürür, P1 tutarsa yasa yalnız büyüklük için geçerli sayılır ve işaret iddiası geri alınır. Her durumda Önerme 1 ve 3 ile Blok 1 sayıları kalır; bunlar tanımlanabilirlik ve protokol değişmezliği üzerine kendi başına savunulabilir bir yöntem katkısıdır.

## 9. Kullanıcının başlatacağı komutlar (taslak)

Blok 2: `python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 --out-dir results/q1/p3_blok2_c10` ile her yerel model için `--model AD:TIP:YOL` (C1 `best.pth` dosyaları ve `models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs/epoch_00X.pth`), her katalog modeli için `--rb-model AD`. Blok 3 örneği (T4): `python -m cli.main train adversarial -m resnet18 -d adversarial_training -p models/c1/resnet18_s1001/resnet18/clean/best.pth -e 100 --lr 0.001 -b 128 --patience 20 --eps 0.00784313725490196 --alpha 0.00196078431372549 --seed 1101 --val-indices data/val_split_indices.json -o models/q1/p3/resnet18_eps2_s1101`; T5'te `--eps 0.01568627450980392 --alpha 0.00392156862745098`.

Kaynaklar: Demontis ve ark., arXiv 1809.02861 (doğrulandı); Jiang ve ark., arXiv 0811.1067, DOI 10.1007/s10107-010-0419-x (doğrulandı); Awad ve ark., arXiv 2512.02830 (özet doğrulandı); Springer ve ark., arXiv 2106.02105 ve Zhang ve ark., arXiv 2307.07873 (başlık doğrulandı); Mahmood ve ark., arXiv 2104.02610 (FÖY künyesi). "İlk kez" ifadesi için belgelenmiş tarama yapılmadı; bu öneride kullanılmamıştır.
