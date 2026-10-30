# Konsey planı: manşet iddia, deney blokları ve uygulama (29.10.2026)

Hazırlayan: konsey sentezcisi ve deney planlayıcı (opus alt ajan). Girdiler: `00_durum_dosyasi.md`, `01_masa_testi.md`, üç öneri (`01_oneri_P1/P2/P3_*.md`), `02_literatur.md`, üç hakem raporu (`03_hakem_R1/R2/R3_*.md`). Kısaltmalar: FÖY = `results/C1_REFERANS_FOYU.md`; SENTEZ = `results/q1/konsey_sentez_r_tau_masa.json` (bu oturumda `raporlar/konsey_2026-10-29/_sentez_r_tau_masa.py` ile üretildi, GPU yok, girdiler yalnız `results/c1_c3/*` ve `results/q1/*` altındaki örnek bazlı npz dosyaları). Karantinadaki klasörlerden sayı alınmamıştır.

En önemli üç nokta şunlardır. Birincisi, bugünkü "asimetri ViT'nin kaynak etkisidir" okuması bu haliyle hakemden geçmez: mevcut veride ViT-Tiny'nin CNN paneline karşı görünen kaynak açığının yaklaşık %93'ü simetrik benzemezliktir, yönlü kısmı küçüktür (SENTEZ, aşağıda). İkincisi, seçilen manşet bu ayrışımı ölçüm katmanı yapar ve mimari ile başlatmayı ayrı ayrı değiştiren 2x2'lik bir eğitimle "benzemezlik mimarinin mi, başlatmanın mı, girdi hattının mı" sorusunu yanıtlar; her sonuç bölgesi önceden yazılmış bir başlığa karşılık gelir. Üçüncüsü, bütçe en kötü durumda bekçiyle 42,2 GPU-saatte tutulur (fable kararı K2: B5 ve B6 A önceliğinde); belirleyici ölçüm R224 ResNet'in epok süresidir ve beş dakikalık pilotla ölçülmeden eğitim başlamaz.

## 1. Seçilen manşet iddia

Manşet (önceden kayıtlı biçimi): Çekişmeli eğitilmiş CNN ile yama tabanlı ViT arasındaki transfer, hedefin beyaz kutu kırılganlığı (w), simetrik benzerlik (τ̄) ve küçük bir yönlü terim (r) olarak ayrışır; ViT'nin "zayıf kaynak" görünümü büyük ölçüde simetrik benzemezliktir ve girdi hattı ile eğitim tarifi eşitlenmiş bir mimari × başlatma tasarımı bu benzemezliğin ve yönlü terimin hangi etmene ait olduğunu belirler.

Tanımlar (hedef-doğru protokol, log ölçek, tek birincil ölçek): T_ij kaynak i'den hedef j'ye koşullu yanıltma oranı, w_j = T_jj; r_ij = log(T_ij/T_ji) − log(w_j/w_i); log τ̄_ij = ½[log(T_ij T_ji) − log(w_i w_j)]. Böylece log T_ij = log w_j + log τ̄_ij + ½ r_ij olur. Bu bir muhasebe özdeşliğidir ve öyle yazılır; iddianın içeriği bileşenlerin ölçülen büyüklüklerinde ve müdahalelere verdikleri yanıttadır. Model düzeyinde, sabit CNN paneli P üzerinde σ_m = ort_c log τ̄_mc (panel benzerliği), ρ_m = ort_c r_cm (yönlü terim; pozitifse m yönlü olarak zayıf kaynaktır) ve ω_m = log w_m tanımlanır. P1 ve P2'deki "kaynak gücü" S_m = ort_c log T_mc, bu üçünden türetilir ve "panel hizalanması" adıyla yalnız betimsel verilir (R1 F1, R2 F0).

Mevcut veride bu ayrışımın söyledikleri (SENTEZ):

| Nicelik | Değer | Anahtar |
|---|---|---|
| C1 çifti, CIFAR-10, yönlü artık r_RV (3 tohum) | 0,119 / 0,122 / 0,103; ort. 0,115, koşum SD 0,010 | `kumeler.c10_c1_secilen.tam_orneklem.r` |
| Aynı çiftte log asimetrinin potansiyel (w) payı | ort. 0,54, SD 0,03 | `...potansiyel_payi` |
| CIFAR-100, r_RV ve potansiyel payı | 0,154 (SD 0,041); 0,28 (SD 0,09) | `kumeler.c100_c1_secilen.tam_orneklem` |
| Son kontrol noktası, CIFAR-10, r_RV | 0,129 (SD 0,044) | `kumeler.c10_son_kontrol_noktasi` |
| Görüntü bootstrap SD (çift 1), r ve log τ̄ | 0,030 ve 0,016 | `goruntu_bootstrap_pair1` |
| Dört CNN'lik panelde σ: ViT, ResNet-18, XCiT-S12, panel içi | −1,086; −0,694; −0,609; −0,565 | `havuz_tohum1.*.log_tau_ort`, `panel_ici_log_tau` |
| Aynı panelde ρ: ViT, ResNet-18, XCiT-S12 | +0,043; −0,018; −0,095 | `havuz_tohum1.*.r_ort` |
| ViT'nin panel kaynak açığı (log), simetrik ve yönlü pay | 0,422 = 0,392 + 0,030 (simetrik oran 0,93) | `havuz_tohum1.kaynak_acigi_ayristirma_log` |
| Hedef tarafı: panelden ViT'ye eksi ResNet'e (log) | −0,201 = +0,160 (potansiyel) − 0,392 + 0,030 | `havuz_tohum1.hedef_farki_ayristirma_log` |

Bu tablo makalenin bugünkü 3x3 bölüşümünü (+5,13 kaynak, −2,03 hedef; FÖY:390) yeniden okur: ViT aslında daha kırılgan hedeftir (w 55,83 ile 47,56; `results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json`, `havuz_AT7.w_beyaz_kutu`), toplamsal uydurmada "az duyarlı hedef" ve "zayıf kaynak" görünmesinin ortak nedeni CNN'lere düşük benzerliğidir. Bu, P3'ün Önerme 1(c)'sinin (tek ViT'de aile benzerliğinin α_V ve β_V'ye birlikte −γ yüklenmesi) sayısal karşılığıdır. Havuz değerleri tek tohumludur; Blok 2 bunu üç tohuma ve yedi üyeli panele taşır.

Tez ile uzlaşma (karar kuralı 5): Tezin Bölüm 5.1.1 hükmü ("kaynak ve hedef etkisi bu iki modellik tasarımla ayrıştırılamıyor") doğru kalır, çünkü K = 2'de dolaşım serbestliği sıfırdır ve toplamsal bölüşüm benzerlikle kesin olarak karışır. Sabit bir dış panel ve çarpımsal ayrışımla ayrışım model düzeyinde tanımlanır; tanımlandığında ViT etkisinin büyük kısmı kaynağa değil simetrik benzerliğe düşer. Makale cümlesi böylece "iki modelde ayrışmaz, çaprazlanmış panelde ayrışır" biçimini alır.

Mevcut iddianın korunan ve değişen kısmı: Dört protokol ve toplam olasılık özdeşliği ölçüm katmanı olarak kalır ve P3'ün Önerme 3'üyle güçlenir: h = −log(1 − T) ölçeğinde ham ile hedef-doğru arasındaki fark yalnız hedef potansiyelini kaydırır; havuzda en büyük |g| 0,0044, ham ile hedef-doğru kaynak etkilerinin ayrışması oran ölçeğinde tc kaynak SD'sinin 0,316 katıdır (`results/q1/konsey_masa/_p3_potansiyel_masa.json`, `havuz_cifar10.ayar_testi`). Kaynak etkisi okuması ise geri alınmaz, düzeltilir: yönlü terim gerçektir ve tohumlar arasında kararlıdır (0,115 ± 0,010), ama ViT'nin CNN'lere karşı açığının küçük bir parçasıdır.

## 2. Hakem saldırıları nasıl kapatıldı

| Saldırı | Kaynak | Plandaki yanıt |
|---|---|---|
| "Kaynak gücü" simetrik benzerliktir | R1 F1, R2 F0 | Birincil nicelikler σ, ρ, ω; S yalnız betimsel ve "panel hizalanması" |
| ±2 puan sınırı karantinadaki `stat_addendum`dan, başka nicelik için | R1 madde 3 | Kullanılmaz. Yeni sınır δ = 0,10 log birimi (bir transfer oranında yaklaşık %10'luk göreli değişim). Dayanak: havuzdaki yedi AT modelinin 21 çiftinde r'nin RMS'i 0,0897 (`results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json`, `havuz_AT7.log_tau_simetri_ihlali_rms`); bu dağılım ViT'li 6 çifti de içerir (RMS 0,112), yalnız CNN çiftlerinde RMS 0,0605 (`results/q1/konsey_masa/_dogrulayici/delta_kaynagi.json`). Sınır bu yüzden gevşektir; δ = 0,06 duyarlılık olarak raporlanır, σ ölçeğinde δ uzlaşımdır (ON_KAYIT §5) |
| Kesin sonuç olasılığı, bilinmeyen koşum SD'si | R1 M1 | Önceden kesinlik planı (SENTEZ `kesinlik_plani`): koşum SD'si r için 0,010-0,044, log τ̄ için 0,021-0,023; 2'ye 2 karşıtlıkta %90 aralık yarı genişliği r için 0,021 ile 0,089, log τ̄ için 0,044. Post-hoc güç değildir |
| Bekçi R224-IN'i n = 1'e düşürüyor | R1, R2, R3 P1-a | Hiçbir hücrede n < 2 yok; bekçi yalnız eşit AT tavanını keser, B5 ve B6 fable kararı K2 ile A önceliğindedir (Bölüm 4, B3) |
| Normalizasyon eksik, iyileyici sınıf adına göre seçiliyor | R3 O1, O2 | ImageNet normalizasyonu yalnız IN başlatmalı hücrelerde, model içinde ve başlatma demetinin parçası olarak (fable kararı K3); R224-scr V-scr ile aynı normalizasyonsuz girdi hattını kullanır; `--optimizer adamw` bayrağı; temiz aşama sonunda manipülasyon denetimi |
| Başlatma iki mimaride eşit değil | R2 Saldırı 2 | ResNet için RSB tarifli `resnet18.a1_in1k`, ViT için `deit_tiny_patch16_224.fb_in1k`; iki hücrenin ImageNet top-1 değeri timm model kartından raporlanır |
| Panelde IN ön eğitimli XCiT'ler | R2 | Birincil panel yalnız IN ön eğitimsiz yedi gürbüz CNN; XCiT ikincil |
| R224 ile C1 ResNet arasında köprü yok | R1 M3, R2 | İkincil köprü karşıtlığı S1 (ON_KAYIT) |
| Yörüngelerde R²(λ=1) 0,201 saklanmış | R1 F3, R2, R3 P3-a | Yasa iddiası bırakıldı; sonuç ölçüm sınırı olarak metne girer; "yakınsamış model" tanımı ON_KAYIT'ta sayısal |
| w ile T aynı görüntülerden | R1 M7 | Birincil kestirim bölünmüş yarı (w çift, T tek indeksli görüntülerden ve tersi); masada fark 0,001'in altında (SENTEZ `bolunmus_yari`) |
| ViT'ye özgü transfer saldırısı yok | R2, Naseer ve ark. arXiv 2106.04169 | Blok 5'te MI-PGD ve TGR |
| Dikkat ile yama gövdesi ayrılmıyor | R2 | Başlıkta "attention" yerine "patch-based ViT"; gövde iddiası yok |
| Mahmood çelişkisinin başlatmayla açıklanması | R1 M3 | Cümle çıkarıldı; Mahmood standart rejimdedir |
| Trajektori bloğu pahalı ve kendiliğinden eşyönlü | R1, R3 P1-b | Çıkarıldı |

## 3. Elenen öneriler ve nedenleri

P1 tek başına elendi, çünkü birincil ölçütü S simetrik benzerliği ölçer ve manşetteki nedensel cümle bu ölçütten çıkmaz (R1, R2). 2x2 tasarımı, bekçi düzeltmesi ve normalizasyonla korunmuştur. Blok 2'si (78 kontrol noktalı yörünge) maliyeti yaklaşık 12 saat olduğu (R3 P1-b) ve erken durdurmanın aktarımı artırdığı zaten bilindiği (Gubri ve ark. arXiv 2304.02688; Miller ve Vosoughi arXiv 2007.00806, ikisi `02_literatur.md`'de doğrulanmış) için çıkarıldı. PGD-50 kesildi (R3).

P2'nin B2 kolları (V_IN in21k, V_CS, R_20) elendi: ResNet-IN kolu olmadığından "ön eğitim her modeli iyileştirir" hipotezinden ayrılamaz (R1 F2), R_20 doğrulukla karışır (Schmidt ve ark. arXiv 1804.11285), V_IN tarifi ön eğitimi silebilir (R3 P2-c). B3 (ImageNet) elendi: erişilebilir çift en çok üçtür, kod yolu yoktur, indirme 10-12 GB'tır ve disk %95 doludur (R3 P2-a, P2-b, O4). B1 ölçüm aracı olarak Blok 2'de yaşar.

P3'ün yasa manşeti elendi: yörüngelerde R²(λ=1) 0,201 ve kesişimsiz λ 1,878 (`results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json`, `A_kolu`), havuzdaki yönlü artıklar ±0,10 sınırında ve işaretleri modele göre değişiyor (XCiT için dört panel üyesinin dördünde negatif, ort. −0,095; SENTEZ). Çerçeve Demontis ve ark. (arXiv 1809.02861), Adam ve ark. (arXiv 1904.07980) ve Caussinus yarı-simetri modeline (DOI 10.5802/afst.519) çok yakındır (`02_literatur.md`). Önerme 1 ve 3 ölçüm katmanı olarak alındı. T1-T5 eğitimleri ve Blok 5 (ImageNet) çıkarıldı; T4 (ε 2/255 ResNet-18) yalnız risk tablosunda yedektir.

## 4. Deney blokları

Ortak ayarlar: CIFAR-10 test kümesi, n = 10000, tohum 42; PGD-10 L∞, ε = 8/255, α = 2/255 (`experiments/c1_c3_transfer_matrix.py:25-27`); dört protokol `src/analysis/protokoller.py` maskeleriyle örnek bazında. Birincil panel P (yedi IN ön eğitimsiz gürbüz CNN): Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra (diskte, `models/robustbench_zoo/cifar10/Linf/`), Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm (B1'de indirildi, yedisi de diskte; adlar `_rb_liste.json` satır 92, 228, 152). İkincil panel: Debenedetti2022Light_XCiT-S12 (konteyner önbelleğinden `models/robustbench_zoo`'ya kopyalanır), isteğe bağlı XCiT-M12/L12. Süre birimleri: matriste kaynak başına 1,15 dk saldırı ve hücre başına 0,07 dk (P3 kalibrasyonu, 8x8 için 13,5 dk; DURUM §5).

| Kimlik | Amaç | Eğitim | GPU-saat (tavan) | Öncelik | Kim |
|---|---|---|---|---|---|
| B0 | Ön kayıt dondurma ve masa çözümlemeleri | 0 | 0 | A | Masa (ajan), şimdi |
| B1 | Kod, smoke testleri, 50 iterasyonluk zaman pilotu | 0 | 0,1 | A | Ajan (her iş < 5 dk) |
| B2 | Üç tohumlu sabit panel matrisi (14 model) | 0 | 0,75 | A | Kullanıcı |
| B3 | 2x2 eğitim: mimari × başlatma | 6 | ≤ 38,15 − bekçi | A | Kullanıcı |
| B4 | Son matris (yeni 6 model eklenir, önbellekli) | 0 | 1,0 | A | Kullanıcı |
| B5 | Saldırı tarafı: MI-PGD ve TGR | 0 | 1,0 | A (K2) | Kullanıcı |
| B6 | Betimsel AutoAttack (yeni 6 model, n = 1000) | 0 | 1,2 | A (K2) | Kullanıcı |
| B7 | Ön kayıtlı çözümleme ve rapor | 0 | 0 | A | Masa (ajan) |

### B2: üç tohumlu sabit panel

Modeller: C1 ResNet-18 AT (`models/c1/resnet18_s100{1,2,3}/resnet18/adv/adversarial_training/best.pth`), C1 ViT-Tiny AT (`models/c1/vit_tiny_s200{1,2,3}/vit_tiny/adv/adversarial_training/best.pth`), panel P (7), XCiT-S12; kare 14x14 matris. Ölçülen: her model için σ, ρ, ω, S; ViT tohumları arası ve ResNet tohumları arası log τ̄ (tür içi benzerlik, R2'nin eğitimsiz eki); ViT kaynak açığının simetrik oranı. Öngörüler ve çürütme ölçütleri ON_KAYIT §B2'dedir. Süre: 14 × (1,15 + 14 × 0,07) ≈ 30 dk; XCiT ve paylaşım için pay, tavan 0,75 sa. Çıktı `results/q1/konsey_b2_panel/`. Bu blok B3'ün kapısı değildir; 2x2 her sonuçta bilgilendiricidir. Panel bileşimi yedi üye olarak ON_KAYIT §2'de B2 sonuçlarından önce dondurulmuştur; yedisi de B1 smoke matrisinde yüklendi (`results/q1/konsey_smoke/matris_panel.log`). B2'de yüklenemeyen üye ON_KAYIT §2'deki işlemsel tanımla çıkarılır (en az beş).

### B3: 2x2 eğitim

| Hücre | Model | Başlatma | Temiz aşama | Tohum | Durum |
|---|---|---|---|---|---|
| V-scr | ViT-Tiny, 32→224 | rastgele | C1 ViT tarifi, 200 epok | 2001-2003 | Mevcut (C1) |
| V-IN | aynı sarmalayıcı + model içi IN normalizasyonu (başlatma demetinin parçası) | `deit_tiny_patch16_224.fb_in1k` | AdamW lr 1e-4, kosinüs, 30 epok | 2101, 2102 | Yeni |
| R224-scr | timm `resnet18`, V-scr ile birebir aynı girdi hattı (32→224 bilinear, normalizasyon yok; K3) | rastgele | C1 ViT temiz komutu (`scripts/run_c1_pipeline.sh:58`), 200 epok | 1201, 1202 | Yeni |
| R224-IN | timm `resnet18`, 32→224 + model içi IN normalizasyonu (başlatma demetinin parçası) | `resnet18.a1_in1k` | AdamW lr 1e-4, kosinüs, 30 epok | 1301, 1302 | Yeni |

AT tarifi dört hücrede C1 ViT ile aynıdır: karışık kayıplı AT, PGD-10, ε = 8/255, α = 2/255, AdamW (ağırlık azaltma 0,05) lr 1e-3, batch 64, sabır 20, `data/val_split_indices.json` (`scripts/run_c1_pipeline.sh:62-64`; `logs/C1_at_vit_2002.log:1-6`). İyileyici bayrakla zorlanır. Başlatma etmeni ağırlık, temiz aşama uzunluğu ve girdi normalizasyonunun demetidir ve öyle beyan edilir (R1 M2; fable kararı K3): rastgele başlatmalı V-scr ve R224-scr'de normalizasyon yoktur, IN başlatmalı V-IN ve R224-IN'de model içi ImageNet normalizasyonu vardır. Demet iki mimaride özdeş olduğundan sıfırdan satırında yalnız mimari değişir. Kayıt: `--save-every 10` ile best/last (disk 57 GB boş; R3 O4). R224'ün ViT'ye göre MAC fazlası iddia edilmez, eşitlenen yalnız girdi hattıdır (R3).

GPU dayanağı: ViT AT epoğu 219 s ve temiz epok 25 s (E2 medyan üst değerleri, `logs/Q1_e2_at_vit_tiny_200x.log`, DURUM §5; C1'de 179-182 s, TIMING.md 6806 s/38 ve 7094 s/39). R224 için ölçüm yoktur; R3 tahmini AT 310 s, temiz 36 s'dir (doğrulanmadı, pilot yerini alır). Durma epokları C1'de ViT 45/38/39, ResNet 71/76/77 (FÖY:1390, 1392). Beklenen süre (ViT 45, R224 en çok 77 epok): V-IN 2,95 sa, R224-IN 6,93 sa, R224-scr 8,63 sa; altı koşu 37,0 sa. Tavan 80 epokta 42,3 sa, yani bekçi gerekir.

Bekçi (yalnız süreye bağlı, sonuçtan bağımsız): pilot t_V, t_R, t_Rc değerlerini verir; W(cap) = Σ koşular [temiz epok × temiz süre + cap × AT süresi]/3600. Sabit A blokları 1,85 sa olduğundan eğitim payı 38,15 sa'dir. Kural sırasıyla: W(80) ≤ 38,15 ise tavan 80; değilse W(70) ≤ 38,15 ise tavan 70; değilse W(60) ≤ 38,15 ise tavan 60; hiçbiri tutmazsa eğitim başlamaz ve karar kullanıcıya gider. Tavan dört yeni hücrede eşittir; V-scr'nin durma epokları (45/38/39) her seçenekte tavanın altındadır. R3 tahminiyle (310 s) W(70) = 37,7 sa, eşik yaklaşık 315 s'dir. B5 ve B6 fable kararı K2 ile A önceliğindedir ve defterden bağımsız koşulur; eğitim payı 38,15 sa ve bekçi kuralı değişmez. Sıralama tohumlar arasında örülüdür (V-IN 2101, R224-IN 1301, R224-scr 1201, sonra ikinci tohumlar); hiçbir hücre tek tohuma düşürülmez.

### B4: son matris

B2'nin 14 modeli ile yeni 6 model, 20x20; eski kaynakların çekişmeli örnekleri B2'de önbelleğe alınmışsa yalnız yeni hücreler hesaplanır: 6 × (1,15 + 20 × 0,07) + 14 × 6 × 0,07 ≈ 21 dk; R224 hedeflerinin ileri geçiş payıyla tavan 1,0 sa. Ölçülen: H1-H3 ve ikincil S1-S6 (ON_KAYIT §B4). Çıktı `results/q1/konsey_b4_matris/`.

### B5: saldırı tarafı

Kaynaklar 6 C1 modeli ve 6 yeni model; MI-PGD-10 (μ = 1,0, α = ε/10; FÖY M8.4) bütün kaynaklarda, TGR yalnız ViT kaynaklarında (`experiments/c1_c2_tgr.py`'den taşınır); hedefler panel P. Ölçülen: ResNet ile ViT arasındaki panel kaynak açığının her kaynağın en iyi saldırısı altında koruduğu oran. Tavan 1,0 sa (17 kaynak-saldırı birimi × yaklaşık 2,2 dk). Çıktı `results/q1/konsey_b5_saldiri/`.

### B6: betimsel AutoAttack

Yeni 6 model, standart AA, n = 1000; dayanak C1'de çift başına n = 10000 için 2,75-3,05 sa (TIMING.md, C1_aa_pair1-3), model başına n = 1000 yaklaşık 0,15 sa; R224 için pay, tavan 1,2 sa. Amaç gürbüzlük düzeyini raporlamak ve gradyan maskelemesini işaretlemek (PGD-10 ile AA arası fark 10 puanı aşarsa işaret). Çıktı `results/q1/konsey_b6_aa/`.

Toplam: B1 + B2 + B4 = 1,85 sa; B3 bekçiyle ≤ 38,15 sa; B5 ve B6 (A önceliği, K2) 2,2 sa. En kötü durum 42,2 sa; beklenen yaklaşık 36-38 sa ile B5 ve B6'nın 2,2 saati. Yeni çekişmeli eğitim 6, blok 8.

## 5. Şimdi CPU'da yapılabilecek masa çözümlemeleri

Yapıldı: `_sentez_r_tau_masa.py` → SENTEZ (C1 çiftlerinde r, τ̄, potansiyel payı, koşum ve görüntü SD'leri; havuzda σ, ρ ve kaynak/hedef ayrışımı; kesinlik planı). Hakem raporları `03_hakem_*.md` olarak kaydedildi.

Şimdi yapılabilecekler (her biri GPU'suz, dakikalar mertebesinde): (1) havuzun yedi AT modelinde σ, ρ ve kaynak açığı ayrışımının bütün modeller için tablosu ve panel üyesi bırakmalı jackknife; (2) Hodge ayrışımıyla r matrisinde model düzeyi ve dolaşım payı (C1 çiftinde r_RV 0,119 iken dört CNN'lik panel üzerinden model düzeyi fark ρ_V − ρ_R tam örneklemde 0,061'dir (bölünmüş yarıda 0,062); yedi modelin tamamı üzerinden kurulan Hodge ayrışımı ise çifte özgü dolaşım payını yarı değil yaklaşık üçte bir, 0,039/0,119, olarak verir; `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json`, `2_hodge_r.yari_log.RV_cifti`; düzeltme §12'de); (3) Mahmood 8x8 matrisinde (`results/q1/dis_veri/mahmood2021_tablolar.json`) aynı ayrışım, yalnız dış karşılaştırma olarak ve protokolü her-ikisi-doğru diye etiketlenerek; (4) CIFAR-100 ve SVHN 3x3 matrislerinde potansiyel payı tablosu; (5) Önerme 3'ün h ölçeği sınamasının C1 3x3'lere uygulanması; (6) ON_KAYIT çözümleme betiğinin havuz verisinde regresyon sınaması (SENTEZ değerlerini yeniden üretmeli).

## 6. Yazılacak betikler

| Betik | Girdi | Çıktı | Doğrulama (< 5 dk) |
|---|---|---|---|
| `src/models/r224.py` ve kayıt: `resnet18_224` (R224-scr, normalizasyonsuz), `resnet18_224_in1k` (R224-IN, model içi ImageNet normalizasyonu), `vit_tiny_in1k` (V-IN; sınıf adında `vit` korunur) | timm ağırlıkları | model nesneleri | Ağırlık yükleme raporu: baş dışındaki eksik anahtar 0; normalizasyon değerleri `pretrained_cfg` ile aynı |
| `cli/train.py`: `--optimizer {auto,adamw,sgd}`, `--init-weights {none,deit_tiny_in1k,resnet18_a1_in1k}`, kosinüs temiz aşama | CLI | eğitim günlüğü | 200 iterasyonluk temiz smoke; IN başlatmalı modelde doğrulama doğruluğu rastgele başlatmalının belirgin üstünde |
| `scripts/konsey_pilot_zaman.py` | iki yeni model | `results/q1/konsey_pilot_zaman.json` (t_V, t_R, t_Rc, W(80/70/60), seçilen tavan) | 50 AT iterasyonu ve 50 temiz iterasyon, dışa kestirim |
| `experiments/c1_c3_transfer_matrix.py`: yeni tipler, `--cache-adv DIR`, `--skip-existing`, `--attack {pgd,mi,tgr}`, `--steps` | model listesi | `results/q1/konsey_b*/` npz ve `transfer_matrix.json` | `--n-samples 200`, 3 model (biri `resnet18_224`) |
| `experiments/q1_konsey_ayrisim.py` | matris klasörleri, hücre tablosu | `results/q1/konsey_ayrisim.json` | Havuz klasöründe SENTEZ değerlerini 1e-6 içinde üretmeli; C1 modelleriyle sahte 2x2'de uçtan uca |
| `scripts/konsey_b3_kuyruk.sh` | pilot JSON | `results/q1/konsey_b3_defter.tsv` (duvar saati, epok, durum) | `--dry-run` |

`q1_konsey_ayrisim.py`'nin karması B3 başlamadan ON_KAYIT'a yazılır.

## 7. Kullanıcının başlatacağı komutların taslağı

Her bloktan önce: `nvidia-smi` ile başka konteynerin (histo-sparse-adv) bellek ve kullanım durumuna bakılır; 12 GB'tan fazla kullanım varsa defterde not edilir. `df -h /home/firat` 15 GB'ın altındaysa B3 başlamaz.

```bash
# B2 (yaklaşık 30 dk)
docker exec -d -w /workspace adeb_eval bash -lc "python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
  --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
  ... (s1002, s1003; ViT_Tiny_AT_s200x:vit_tiny:...) \
  --rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
  --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
  --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm \
  --rb-model Debenedetti2022Light_XCiT-S12 \
  --cache-adv results/q1/konsey_adv_onbellek --out-dir results/q1/konsey_b2_panel > logs/konsey_b2.log 2>&1"

# B3 (kuyruk, tmux içinde)
tmux new -s konsey_b3 "docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json"
# kuyruğun her adımı, ör. V-IN 2101:
#  python -m cli.main train clean -m vit_tiny_in1k --init-weights deit_tiny_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed 2101 --val-indices data/val_split_indices.json -o models/q1/konsey/V_IN_s2101
#  python scripts/konsey_b3_denetim.py temiz --takma V_IN_s2101   (ON_KAYIT §4 temiz aşama denetimi; GECTI olmadan AT başlamaz)
#  python -m cli.main train adversarial -m vit_tiny_in1k -d adversarial_training -p models/q1/konsey/V_IN_s2101/vit_tiny_in1k/clean/best.pth --optimizer adamw -e 100 --stop-epoch <TAVAN> --lr 0.001 -b 64 --patience 20 --val-indices data/val_split_indices.json --save-every 10 --seed 2101 -o models/q1/konsey/V_IN_s2101
#  (-e 100: kosinüs çizelgesi C1 ViT'deki gibi T_max = 100 üzerinden kurulur; --stop-epoch eğitimi bekçinin tavanında keser. Tam komut listesi: scripts/konsey_b3_kuyruk.sh --dry-run)

# B4, B5, B6: B2 komutuna yeni 6 model eklenir; --skip-existing, ayrıca --attack mi / tgr; AA için mevcut AA betiği n=1000.
```

## 8. İndirmeler

RobustBench CIFAR-10 L∞: Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm (boyutlar doğrulanmadı; diskteki zoo modelleri 45-292 MB, DURUM §4.1). timm: `deit_tiny_patch16_224.fb_in1k`, `resnet18.a1_in1k` (boyut doğrulanmadı, küçük). Toplamın 1 GB altında kaldığı indirme öncesi başlıklardan doğrulanırsa ajan indirir, aşarsa kullanıcı. İsteğe bağlı XCiT-M12/L12 kullanıcı adımıdır. ImageNet verisi yoktur. Önbellek: 20 kaynak × yaklaşık 123 MB (10000×3×32×32 float32) ≈ 2,5 GB.

## 9. Makalede değişecek yerler

| Yer | Değişiklik |
|---|---|
| Başlık (`main.tex:62-63`) | Sonuç bölgesine göre ON_KAYIT §Sonuç haritası; O1 için: "Not a Weak Source but a Different One: Vulnerability, Similarity and Direction in CNN-to-ViT Adversarial Transfer under an Architecture × Initialisation Design" |
| Özet (`main.tex:108`) | Soru, ayrışım ve masa sonucu (simetrik oran, potansiyel payı), 2x2 karşıtlıkları aralıklarıyla, protokol katmanı tek cümle |
| Katkılar (`01_introduction.tex:29-45`) | Dörde iner: tanımlanabilirlik (Önerme 1c, tez uzlaşması); w-τ̄-r ayrışımı ve ölçülen büyüklükler; 2x2 müdahale; protokol ve h ölçeği ayarı (Önerme 3) |
| `02_related_work.tex` | Demontis, Adam, Caussinus, HodgeRank (Jiang ve ark. arXiv 0811.1067), Balduzzi (arXiv 1806.02643), Mahmood, Shao (arXiv 2103.15670), Mo (arXiv 2210.07540), Naseer, Awad (arXiv 2512.02830), Bai (arXiv 2111.05464) |
| `03_methodology.tex` | Ayrışım tanımları, panel, 2x2 tarifi, bölünmüş yarı, ön kayıt; `fig:study_overview` yenilenir |
| `04_experiments.tex` | `tab:source_target` ayrışım tablosuyla değişir; yeni tablolar: 2x2 hücreleri (temiz, AA, ω, σ, ρ), tür içi benzerlik, saldırı tarafı; `tab:external_pool` σ ve ρ sütunları alır |
| `05_discussion.tex` | Tez uzlaşması; yörünge sonucu (R² 0,201) ölçüm sınırı; sınırlılıklar (CIFAR, Tiny ölçeği, hücrede n = 2) |
| `06_conclusion.tex` ve TR aynası | Manşetle eşitlenir; sayılar yalnız FÖY'e eklenecek yeni bölümden |

FÖY'e "M9 konsey" bölümü eklenir; metne giren her sayı oradan alınır.

## 10. Risk tablosu

| Risk | Belirti | Geri çekilme iddiası |
|---|---|---|
| R224 epoğu > yaklaşık 365 s | Pilot | Eğitim başlamaz; kullanıcıya iki seçenek (bütçe aşımı ya da R224-scr tohumlarının sonraya kalması); manşet B2 düzeyinde kalır |
| IN başlatması tutmaz | Temiz aşama denetimi | Hata AT'den önce düzeltilir; düzeltilemezse IN satırı raporlanmaz, iddia scr satırı ve B2 ile sınırlanır |
| IN hücresinde AT çöküşü | 5. epok doğrulama PGD < %15 | Kuyruk durur; kullanıcı kuyruğu `--in-at-lr 0.0005` ile yeniden başlatır, iki IN hücresinin bütün AT'leri lr 5e-4 ile koşulur (biten lr 1e-3 AT'leri silinmeden yanına taşınır ve yeniden eğitilir), beyan edilir; ek süre ON_KAYIT §4'te |
| Kararsız aralıklar (n = 2) | CI sınırları kesiyor | Kestirim çerçevesi; B2 ve masa ayrışımı manşette, 2x2 aralıklarla |
| B2'de simetrik oran düşük | ON_KAYIT §B2 çürütmesi | "ViT'nin açığı yönlüdür" okuması doğru tanımlamayla geri gelir; bugünkü kaynak iddiası güçlenmiş olarak kalır |
| Panel üyesi yüklenmez | B2 smoke | En az beş üyeyle panel; bileşim yedi üye olarak B2 sonuçlarından önce donduruldu (ON_KAYIT §2) |
| TGR taşıma hatası | Smoke | B5 yalnız MI-PGD |
| Disk dolar | `df` < 15 GB | `--save-every 0`; önbellek silinir |
| "Ayrışım tanım gereği doğru" itirazı | Hakem | İçerik ölçülen büyüklüklerde ve müdahale yanıtında; Caussinus ve Demontis atıfla |
| Eğitim yuvası boşalır | Bir koşu kalıcı olarak iptal edilir | Yedek: P3 T4 (ResNet-18, ε 2/255), yalnız betimsel |

## 11. Takvim

| Gün | İş |
|---|---|
| 0 (29-30.10) | ON_KAYIT dondurulur ve sonuç görülmeden işlenir; B1 kodu ve smoke testleri; pilot |
| 1 | B2 (kullanıcı, yaklaşık 30 dk); B2 çözümlemesi ON_KAYIT §B2'ye göre; panel dondurma |
| 1-4 | B3 kuyruğu (beklenen yaklaşık 35 sa duvar saati, paylaşımla 2-3 gün) |
| 4-5 | B4, B5 ve B6 (A önceliği, K2) |
| 5-6 | B7 çözümleme, FÖY M9, makale ve TR aynası revizyonu |
| 7 | Tek turlu hakem paneli |
| Sonra | Kullanıcının visio-cizici şekil görevi (`results/q1_research/BEKLEYEN_SEKIL_GOREVI_2026-10-29.md`); skill kurulana kadar engelli |

Deney çıktılarının besleyeceği yeni şekiller şunlardır: C1 çiftinin log asimetrisinin potansiyel ve yönlü paylarını CIFAR-10, CIFAR-100 ve son kontrol noktası için gösteren ayrışım grafiği (SENTEZ ve `konsey_ayrisim.json`); 20 modelin log τ̄ matrisini aile bloklarıyla veren benzerlik ısı haritası (`konsey_b4_matris/`); her modelin panel kaynak açığını simetrik ve yönlü parçalara bölen yığılı çubuklar (B2, B4); 2x2 hücrelerinde σ ve ρ'yu koşu noktalarıyla gösteren etkileşim grafiği (B4); tür içi ve türler arası τ̄ dağılımları (B2); saldırı türüne göre kaynak açığının korunma oranı (B5); 2x2 tasarımını ve w-τ̄-r ayrışımını anlatan şematik ile Önerme 3'ün h ölçeği ayarını anlatan şematik (veri gerektirmez).

## 12. Fable kararları ve ilerleme (29.10.2026)

Ana oturum, uygulama turundan sonra on iki karar vermiştir. Manşet §1'deki birleşik iddiadır, yani w-τ̄-r ayrışımı ile mimari × başlatma 2x2'si birlikte manşeti taşır; protokol ve özdeşlik katmanı ölçüm katmanı olarak korunur (K1). B5 (MI-PGD ve TGR) ile B6 (yeni altı modelde AutoAttack, n = 1000) A önceliğine alınmıştır; gerekçe, ViT'ye özgü transfer saldırısının yokluğunun hakem raporunda (R2, §2 tablosu) anılması ve yeni modellerde gradyan maskelemesinin işaretlenmeden 2x2 karşıtlıklarının yorumlanamamasıdır; B3'ün eğitim payı 38,15 GPU-saat ve bekçi kuralı aynen kalır, toplam en kötü durum 42,2 GPU-saattir (K2). R224-scr, V-scr ile birebir aynı normalizasyonsuz girdi hattını kullanır; ImageNet normalizasyonu yalnız IN hücrelerinde ve başlatma demetinin (ağırlık, temiz aşama uzunluğu, normalizasyon) parçasıdır, böylece sıfırdan satırında yalnız mimari değişir (K3). ImageNet verisi diskte yoktur ve disk %95 doludur; bu bir sınırlılık olarak yazılır (K4). Takma adlar `hucre_tablosu.json`'daki yirmi addır ve yeni kontrol noktaları `models/q1/konsey/<takma ad>/` altına yazılır (K5).

Çözümleme betiğinin arayüzü `--mod {masa,b2,b4,b5}`, tekrarlanabilir `--matris-dizini`, `--hucre-tablosu`, `--cikti` ve `--maskeleme-isaretli` olarak genişletilmiştir; gerekçe, B5 ve B6 A önceliğine çıktığı için bu blokların karar kurallarının sonuçtan önce betikte kodlanmış olması gereğidir (K6). Temiz aşama denetimi son epok yerine ilk epok doğruluğuna bağlanmış, R224-IN AT'si referansı (R224-scr ilk epok) oluşana kadar bekletilmiştir. Denetimin amacı ImageNet ağırlıklarının gerçekten yüklenip yüklenmediğini yakalamaktır ve yakınsamış ResNet-18 temiz doğruluğu %96,08 olduğundan son epok karşılaştırması doğru yüklenmiş bir modeli de reddedebilirdi; bu değişikliğin smoke doğrulukları (92,85 ve 79,25) görüldükten sonra yapıldığı ön kayıtta açıkça yazılıdır (K7). TGR yalnız kaynağındaki ve `experiments/c1_c2_tgr.py`'deki ayarla (α = 2/255, μ = 1,0, γ = 0,5) koşar, α = ε/10 ile ikinci bir TGR koşusu yapılmaz; özgün ayar "ViT'ye özgü saldırı zayıflatıldı" itirazına en sağlam yanıttır ve adım boyu farkı çapraz uydurmalı seçime zaten girer (K8). S4 çift listesi olduğu gibi kabul edilmiştir (K9). AT tavanı pilot kuralına göre 80 epok olarak dondurulmuştur; pilot boş GPU'da ölçülmüştür (W(80) = 20,47 sa), GPU paylaşılırsa duvar saati yaklaşık iki katına (40,94 sa) çıkabilir, ama tavan bir protokol değeridir ve koşu ortasında değiştirilmez; runbook B3'ün `nvidia-smi` ile başka eğitim görülmezken başlatılmasını ister (K10). Konseyin ilk `_p3_*`, `_P2_*` ve `_rb_*` JSON dosyaları silinmez (K11), dondurma commit'i yereldir ve ana oturumca yapılır, push kullanıcıya bırakılır (K12).

Uygulama turunda iki çelişik doğrulayıcının ilk hükmü "düzeltilmeli" olmuştur. Kod tarafında on bulgu (`05_kod_raporu.md`, "Doğrulayıcı düzeltmeleri"), çözümleme tarafında on yedi bulgu (`04_masa_cozumlemeleri.md`, "Doğrulayıcı düzeltmeleri (ikinci tur)") çıkmış ve bunların hepsi düzeltilmiştir; değişiklikler ön kayıt §8'de madde madde kayıtlıdır. Zaman pilotu V_IN AT epoğunu 125,8 s, R224 AT epoğunu 142,7 s ölçmüştür (`results/q1/konsey_pilot_zaman.json`, `t_V_at_epok_s`, `t_R224_IN_at_epok_s`); bekçi W(80) = 20,47 sa ile tavanı 80 seçmiştir (`W_sa.80`, `secilen_tavan`). Ön kayıt bu kararlarla `ON_KAYIT_2026-10-29.md` adıyla dondurulmuştur; taslak (`ON_KAYIT_TASLAGI.md`) karşılaştırma için yerinde bırakılmıştır.

Masa çözümlemelerinin makale için önemli dört sonucu şunlardır. Birincisi, ViT'nin dört CNN'lik panele karşı kaynak açığında simetrik pay log ölçekte 0,927'dir ve panel üyesi bırakmalı jackknife'ta 0,919 ile 0,935 arasında kalır (`results/q1/konsey_masa/konsey_masa_cozumlemeleri.json`, `1_havuz_model_tablosu.modeller.ViT_Tiny_AT_s2001.kaynak_acigi_R_eksi_m_yari_log.simetrik_oran`, `1_havuz_model_tablosu.jackknife_aralik.ViT_Tiny_AT_s2001.simetrik_oran`). İkincisi, yönlü terim ölçeğe bağlıdır: ViT'nin ρ değeri log ölçekte +0,043, logit ölçekte −0,265'tir ve ResNet ile farkı ρ_V − ρ_R log ölçekte bölünmüş yarıda +0,062 (tam örneklemde +0,061) iken logit ölçekte −0,095'e döner (aynı dosya, `1_havuz_model_tablosu.modeller.<model>.yari_log.rho` ve `.yari_logit.rho`); bu yüzden "küçük yönlü terim" cümlesi metinde ölçeğiyle birlikte yazılmalıdır. Üçüncüsü, r matrisinin Hodge ayrışımında potansiyel payı 0,940'tır ve C1 çiftinde r_RV = 0,119'un 0,080'i model potansiyeli farkı, 0,039'u, yani yaklaşık üçte biri çifte özgü dolaşımdır (`2_hodge_r.yari_log.G_potansiyel_payi`, `2_hodge_r.yari_log.RV_cifti`). Planın §5(2)'sindeki "yarısı çifte özgüdür" ifadesi bu sonuçla çeliştiği için düzeltilmiştir; iki sayı farklı referans kümelerinden gelir (ρ dört CNN'lik panel üzerinden, Hodge potansiyeli yedi modelin tamamı üzerinden) ve metinde hangisinin kullanıldığı tanımıyla yazılmalıdır. Logit ölçekte aynı çiftte r_RV 0,006'ya iner ve dolaşım 0,070 ile r'nin kendisinden büyüktür (`2_hodge_r.yari_logit.RV_cifti`). Dördüncüsü iki olumsuz sonuçtur: SVHN'de ResNet ile ViT arasındaki log asimetri ters işaretlidir ve r_RV iki çiftte de negatiftir (−0,106 ve −0,076; `4_potansiyel_payi.ozet.svhn_linf_secilen.r.degerler`), yani yönlü terimin işareti veri kümesine göre değişebilir; Mahmood ve ark. 2021 verisinde köşegen beyaz kutu olmadığından w tanımsızdır ve ön kayıtlı w-τ̄-r ayrışımı kurulamamaktadır (`3_mahmood.etiket`). Bu iki sonuç metinde sınırlılık olarak raporlanır, saklanmaz.

Konseyin `raporlar/konsey_2026-10-29/` altındaki ilk `_p3_*`, `_P2_*` ve `_rb_*` JSON dosyaları konseyin çalışma kopyalarıdır ve silinmez, taşınmaz; sayı kaynağı değildirler, geçerli sayı kaynakları `results/q1/konsey_masa/` altındaki yeniden üretilmiş kopyalardır (K11). Komutların güncel ve tek geçerli metni `KONSEY_RUNBOOK.md`'dedir; bu planın §7'sindeki komut taslağı yalnız tarihsel kayıttır (örneğin B3 öncesi disk eşiği runbook'ta 30 GB'tır).

## 13. Ek bloklar B8-B10 (30.10.2026)

Manşet 29.10'da çarpımsal w-τ̄-r ayrışımına ve mimari × başlatma 2x2'sine bağlanmış, ön kayıt dondurulmuştur. 30.10'da hakemin "CIFAR-10 oyuncak kurulum" itirazına karşı eğitim gerektirmeyen üç ek blok tasarlanmış (`06_ek_deney_literatur.md`, `06_ek_deney_tasarim.md`), ilk ek ön kayıt taslağı (`ON_KAYIT_EK_B8_B9_TASLAK.md`) çelişik bir hakem raporuyla sınanmıştır. Hakemin hükmü büyük revizyondur. Ana oturum bu hükmün ardından yedi karar vermiş, ek ön kayıt bu kararlarla `ON_KAYIT_EK_B8_B10_2026-10-30.md` adıyla yeniden yazılıp dondurulmuştur. Ek, dondurulmuş ön kaydı ve O1-O5a sonuç haritasını değiştirmez; yalnız önceden yazılmış ek cümleler getirir.

B9 (CIFAR-100 paneli) tasarımdaki gibi yapılır (E1). Üç tohumlu C1 CIFAR-100 ResNet-18 ve ViT-Tiny AT çiftleri, yedi üyeli RobustBench CIFAR-100 L∞ paneliyle (Rice2020Overfitting, Rade2021Helper_R18_ddpm, Addepalli2022Efficient_RN18, Sehwag2021Proxy, Pang2022Robustness_WRN28_10, Wang2023Better_WRN-28-10, Jia2022LAS-AT_34_10) ve iki ImageNet ön eğitimli ikincil üyeyle çaprazlanır. Çözümleme dondurulmuş `q1_konsey_ayrisim.py --mod b2` ile yalnız yeni `hucre_tablosu_b9.json` tablosuyla yapılır, yani B2'nin birebir yinelemesidir ve F_B9'un Holm kararları bağlayıcıdır. Gerekçe, veri kümesine genellemenin B2 ile aynı çıkarım gücüyle (üç tohum) ve aynı kodla sınanabilmesidir. ViT-Tiny'nin CIFAR-100 temiz doğruluğunun (43,17; FÖY satır 229) panelin RobustBench temiz doğruluklarının (53,83-72,58) altında kalması sınırlılık olarak yazılır. Görev metnindeki "53,83-67,34" aralığı literatür raporunun önerdiği eski beşli eke aittir; dondurulan P9'da Wang2023Better_WRN-28-10 (72,58) bulunduğundan doğru aralık 53,83-72,58'dir (RobustBench `model_info/cifar100/Linf`, 30.10.2026).

B8 (ImageNet paneli) Imagenette ile değil ImageNetV2 MatchedFrequency ile yapılır (E2). Imagenette2 doğrulama kümesinin %96,6'sı ImageNet eğitim görüntüsüdür (`06_ek_deney_literatur.md` §4.2); ImageNetV2 ise modellerin görmediği 10.000 yeni Flickr görüntüsüdür ve 1000 sınıflı tam logitle, kısıtsız kullanılır. K4 kararı disk gerekçeli bir sınırlılıktı; D diskinde 2,2 TB boş yer bulunduğundan ve kullanıcı ek veri setine onay verdiğinden ImageNetV2 indirilir. Örneklem sınıf başına iki görüntüyle n = 2000'dir; float32 önbellek 16,86 GB olup D'ye yazılır. Saldırı PGD-10, ε = 4/255, α = 1/255'tir; önişleme ortak bicubic Res256-Crop224 hattıdır ve temiz doğruluk ile w bu hatta yeniden ölçülür. B8'deki dönüştürücülerin çoğu temiz ön eğitimli ağırlıklardan başlatıldığı için B8, 2x2'nin IN satırının doğal ölçekteki karşılığı olarak çerçevelenmiştir. Beklenti dondurulmuş H1 ve H2'nin öngörülen büyüklüklerinden türetilir: A^σ_IN = A^σ_scr + I^σ ve sınır değerlerle −0,20 + 0,10 = −0,10. Holm'lu karar ailesi yoktur; B8 betimsel, aralıklı ve keşifsel etiketiyle önceden kaydedilmiştir. Hakemin kırmızı bulguları da bu kararla kapanır: taslaktaki Δσ ≤ −0,20 öngörüsü H2 ile tutarsızdı ve df 2 ile dört sınamalı Holm neredeyse kesin kararsız sonuç verirdi.

Liu çiftinin denetimi bu çerçeveden bir sapma ortaya çıkarmıştır. Liu ConvNeXt-B ile Swin-B'nin ARES deposundaki eğitim yapılandırmaları yalnız model adında ayrılır, ikisinde de ön eğitim bayrağı yoktur ve RobustBench ikisini de ek verisiz işaretler; makalenin Tablo 7'si ve README'deki AA değeri yayımlanan Swin-B'nin 21K ön eğitimsiz taban tarifle eğitildiğini dolaylı olarak gösterir. Tarif ortaklığı bu yüzden doğrulanmış, ama başlatma dolaylı kanıtla sıfırdan bulunmuştur. Liu çifti bu nedenle IN satırının kestiriminden ayrılmış, sıfırdan satırının doğal ölçekteki tek çiftlik karşılığı olarak ayrı satırda ve H1'in büyüklüğüyle (≤ −0,20) karşılaştırılarak verilir. IN satırının kestirimi iki Singh çiftine dayanır (ek ön kayıt §5.4, §5.6). Bu ayrım E2'nin "Singh, Mo, Liu temiz ön eğitimli" ifadesinden farklıdır ve ana oturumun onayına sunulmuştur; ek ön kayıt bu ayrımla dondurulmuştur.

B10 hakemin iki değişikliğiyle yapılır (E3). Soru, temiz görüntüde modeller arası girdi gradyanı kosinüsünün (c_ij) log τ̄'yu üç veri kümesinde Mantel sınamasıyla öngörüp öngörmediğidir. Birinci değişiklikle, gürbüzlük düzeyi ve algısal hizalı gradyan gibi model düzeyi ana etkiler, iki matristen toplamsal model ana etkileri çıkarılarak kalan artıklar üzerinde ayrıca sınanır; bu, Smouse, Long ve Sokal'ın (1986, DOI 10.2307/2413122) kısmi Mantel'inin bütün ana etkileri kapsayan biçimidir. İkinci değişiklikle Zhang ve ark.'nın (arXiv 2307.07873, IEEE S&P 2024) Tanım 2'deki gradyan benzerliği c_ij'nin öncülü olarak anılmış ve doğrulanmıştır. F_B10 altı sınamalıdır (üç veri kümesi × ham ve kısmi) ve Holm uygulanır.

ε süpürmesi yapılmaz (E4). Özgün `experiments/c1_c3_transfer_matrix.py`'ye dokunulmaz; bütün ekler `experiments/q1_ek_transfer_matrix.py` adlı çatallanmış kopyaya yazılır (E5). Gerekçe, matris betiğinin yerinde değiştirilmesinin zincirde koşacak B4 ve B5'i kirletmesidir. Özgün betiğin bugünkü özeti `f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7`'dir; B4 ve B5'in bu özetle koşulduğu ve B9'un da aynı dosyayla koşulacağı ek ön kaydın Dondurma eki (c)'sine yazılmıştır. Ana oturum ek dondurulmadan önce `results/q1/konsey_ayrisim_b2.json` dosyasındaki model tablosunun ρ değerlerine (karar alanlarına değil) bakmıştır. Bu durum ek ön kaydın görülmüş veri bölümüne yazılmıştır; B9, B8 ve B10 öngörüleri dondurulmuş ön kayıttaki öngörülerden türetilmiştir, B2 sonucundan değil (E6). Bütün ek koşular B3-B6 zinciri bittikten ve konteyner D bağlamasıyla yeniden kurulduktan sonra yapılır; şimdi yalnız kod, CPU denemeleri ve indirmeler yapılır (E7).

Hakemin kırmızı ve sarı bulguları şöyle kapanmıştır.

| Hakem bulgusu | Kapanış |
|---|---|
| Matris betiğinin yerinde değiştirilmesi B4 ve B5'i kirletir | Çatallanmış kopya; özgün betiğin özeti dondurma ekinde (E5) |
| B8 dönüştürücüleri IN satırıdır, Δσ ≤ −0,20 öngörüsü H2 ile tutarsız | IN satırı çerçevesi, H1 ve H2'den türetilen ≤ −0,10 beklentisi (E2); Liu çifti doğrulamada sıfırdan çıktığı için ayrı satırda |
| df 2 ve dört sınamalı Holm neredeyse kesin kararsız | B8'de Holm'lu aile kaldırıldı, betimsel ve keşifsel (E2) |
| Imagenette ILSVRC_val alt kümesi küçük ve köpek ağırlıklı | ImageNetV2 MatchedFrequency, 1000 sınıf, n = 2000 (E2) |
| ImageNetV2 n = 5000 önbelleği yaklaşık 42 GB | n = 2000, float32 önbellek 16,86 GB, D diskinde (E2) |
| Liu çiftinin tarif ortaklığı doğrulanmadı | Yapılandırma düzeyinde doğrulandı; başlatma dolaylı kanıtla sıfırdan (ek ön kayıt §5.4) |
| B10 ham Mantel model ana etkileriyle karışır; 2307.07873 anılmalı | Toplamsal ana etkileri çıkarılmış kısmi sınama, Zhang ve ark. öncül (E3) |
| K-b(B9) TOST desteği yapısal olarak ulaşılamaz (yarı genişlik 0,069) | Sınırlılık olarak yazıldı; Holm altında ancak K-a ve K-c önce reddedilir ve \|ρ̄\| ≲ 0,031 olursa mümkün (ek ön kayıt §4.3, §9) |
| gdown kotası yaklaşık 20 dosyada takılabilir | İndirme ajanı yedek kaynak arar; 48 saatte inmeyen üye için yüklenemeyen üye ve yedek kuralı (ek ön kayıt §4.1, §5.5) |

Ek blokların bütçesi aşağıdaki tabloda verilmiştir. Beklenen süreler `_ek_sure_kestirimi.json` içindeki iki kalibrasyonlu etkin hızla (20,0 ve 15,8 TFLOP/s) hesaplanmıştır; B8 ve B10'un ImageNet satırı aynı dosyadaki n = 1000 değerlerinin n = 2000'e doğrusal ölçeklenmesidir (iş modeli n ile doğrusaldır). İndirme boyutları B8 ve B9 modelleri için 4 bayt × parametre kestirimidir (`B8_indirme_fp32_MB`, `B9_indirme_fp32_MB_pang_haric`); ImageNetV2 arşivi HTTP HEAD ile ölçülmüş 1.264.079.360 bayttır (`06_ek_deney_literatur.md` §4.3). Taslaktaki Imagenette ve Imagewoof arşivleri (669,9 MB) artık indirilmez ve 20 sınıflı Tier 2 matrisi (0,5 GPU-saat) kaldırılmıştır.

| Blok | İş | Beklenen | Tavan (GPU-saat) | İndirme (MB) | Ne zaman |
|---|---|---|---|---|---|
| B8-0 | ön işleme denetimi, 14 model × 2000 görüntü × 2 hat | birkaç dakika | B8 tavanının içinde | 0 | zincir sonrası, ilk iş |
| B9 | 15x15 CIFAR-100 matrisi, n = 10000 | 28,5-36,1 dk (`B9_n10000`) | 1,0 | 899,4 (Pang hariç) | B8-0'dan sonra |
| B8 | 14x14 ImageNetV2 matrisi, n = 2000 | 23,0-29,2 dk (`B8_n1000` × 2) | 1,0 | 3284,5 model + 1264,1 veri | B9'dan sonra |
| B10 | üç kümede gradyan kosinüsü | yaklaşık 6,2 dk (`B10_gradyan_dk_hiz_b`; ImageNet 0,97 × 2) | 0,25 | 0 | B4, B8, B9'dan sonra |
| Toplam | | 57,7-71,5 dk | 2,25 | 5448,0 | |

Bu bütçe dondurulmuş Dondurma eki (e)'deki 42,2 GPU-saatin dışındadır ve B3'ün bekçi kuralına dokunmaz. D diskinde gereken yer yaklaşık 25 GB'tır: modeller yaklaşık 4,2 GB, ImageNetV2 arşivi ve açılmış hâli yaklaşık 2,5 GB, B8 önbelleği 16,86 GB, B9 önbelleği 1,84 GB. Yedek modeller (Wong2020Fast, Chen2021LTD_WRN34_10 ve Cui2023Decoupled_WRN-28-10) ilk tasarımda yalnız gerektiğinde indirilecekti; indirme sırasında üçü de D diskine indirilmiştir ve yalnız ek ön kaydın yedek kuralıyla (§4.1, §5.5) kullanılır. D diskindeki ek indirmelerin ölçülmüş toplamı yedeklerle birlikte 5910,6 MB'tır (`_ek_denetim/d4_boyutlar.tsv`, 26 dosya, bayt toplamı / 10^6). Yedekler çıkarıldığında toplam 5468,3 MB'tır ve tablodaki 5448,0 MB'lık beyanla grup düzeyinde uyumludur: CIFAR-100 modelleri 915,1 MB (beyan 899,4), ImageNet modelleri 3289,1 MB (beyan 3284,5), ImageNetV2 arşivi 1264,1 MB (beyan 1264,1). Modellerdeki küçük farklar beyanın 4 bayt × parametre kestirimi olmasından gelir.
