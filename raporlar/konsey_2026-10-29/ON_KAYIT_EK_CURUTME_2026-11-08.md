# Ön kayıt eki: çürütme konseyi sonrası Tier 1 blokları (A, B, C1, C2, D, G) ile B1-09 ve B1-18

Bu ek 08.11.2026'da dondurulmaya hazır duruma getirilmiştir. Dondurma, bu dosyanın ve §3'teki betiklerin aynı commit'le depoya girmesiyle gerçekleşir; commit kimliği bu gövdeye yazılmaz, `raporlar/curutme_2026-11-07/03_deney_zinciri.md` dosyasındaki "Dondurma commit'i" başlığına işlenir. Bu ek, dondurulmuş `ON_KAYIT_2026-10-29.md` ile `ON_KAYIT_EK_B8_B10_2026-10-30.md` dosyalarına eklenen ayrı bir ön kayıttır ve onları hiçbir bakımdan değiştirmez. Önceki iki kaydın tanımları (T_ij, w_j, σ_m, ρ_m, ω_m, S_m, bölünmüş yarı kestiricisi, panel üyesinin kendi değerinde panelden çıkarılması), eşdeğerlik sınırı δ = 0,10, karar ilkesi ve çözümleme betiği burada aynen geçerlidir. Blokların tarifleri, tohumları, süre sınırları ve öngörü eşikleri 07.11.2026 çürütme konseyinin iki raporundan alınmıştır: Tier 1 blokları için `raporlar/curutme_2026-11-07/02_deney_adaylari.json` ile `02_literatur_dis_gecerlilik.md` §4, B1-09 ve B1-18 için `01_ic_gecerlilik.md` (satır 75-83 ve 185-193) ile `01_bulgular.json`. Bu ekte yeni olan, blokların koşu sırasının, durdurma kurallarının ve öngörülerin sayısal karşılaştırma değerlerine bağlanması ile konsey raporlarında sayısal karşılığı verilmemiş birkaç ölçütün işlemselleştirilmesidir. İşlemselleştirmeler şunlardır ve her biri ilgili bölümde de belirtilmiştir: G'de "kısmi Mantel pozitif" ölçütü r > 0 ve tek yönlü p < 0,05, "sıfıra yakın" ölçütü p ≥ 0,05 ve |r| < 0,10 olarak (§10); B1-09 ve B1-18'de H yanlış bölgeleri (H1 > −0,15, H2 ≤ 0, H3 için dondurulmuş K-b çürütme ölçütünün karşılığı), B1-18'de seçilen değerden |Δ| < 0,10 ve ara epok yörüngesi için ≥ +0,05 (§11, §12); B pilotunda epok süresinin başlatma hariç ölçülme yolu (§6). H doğru bölgeleri B1-09 ve B1-18'de dondurulmuş ön kaydın öngörülen büyüklükleridir (föy 1526-1528). Tier 2 blokları (E, E2, F) bu ekin kapsamında değildir ve bu ekle koşulmaz.

## 1. Kayıt öncesinde görülmüş veriler

Önceki iki ön kaydın §1'inde listelenen bütün veriler ve dondurulmuş bütün sonuç dosyaları (B2, B3, B4, B5, B6, B8, B9, B10 ve masa çözümlemeleri) burada görülmüş sayılır. Bu blokların karşılaştırma değerleri bu dosyalardan gelir ve `results/C1_REFERANS_FOYU.md` satır numarasıyla verilir; bunlar sınama sayılmaz.

Çürütme konseyinin iç geçerlilik kolu 07.11.2026'da mevcut matrisler üzerinde beş yeni çözümleme üretmiş ve sonuçlarını raporuna yazmıştır: `results/q1/curutme_2026-11-07/her_ikisi_tutarli.json`, `ayrisim.json`, `cikarim.json`, `olcek.json` ve `olcekli_etki.json`. Bunlardan bu ekin öngörüleriyle doğrudan ilgili olanlar şunlardır. Tutarlı her-ikisi-doğru protokolünde CIFAR-10'da ρ(V-scr) +0,188 [%90: 0,166; 0,211] ve H3 +0,100 (TOST p 0,501), H1 −0,431, H2 +0,317 bulunmuştur (`01_bulgular.json`, B1-01 kanıt alanı; `01_ic_gecerlilik.md`:15). On CNN biriminde σ'nın standart sapması 0,102 ve V-scr'nin z değeri −4,8, V-IN'inki −2,2, XCiT-S12'ninki −0,45'tir (`olcekli_etki.json`; `01_ic_gecerlilik.md`:197). Sıfırdan satırında H1'in yaklaşık %44, %67 ya da %88'i, CNN'ler üzerinde kurulan σ-temiz doğruluk doğrusuna göre doğrulukla birlikte değişen paydır (`ayrisim.json`; `01_ic_gecerlilik.md`:7). Bu değerler B ve G'nin öngörülerinin hangi yöne düşebileceğine dair bir izlenim verdiği için açıkça beyan edilir; eşikler konseyin 07.11.2026 raporundaki değerlerdir ve bu ek yazılırken değiştirilmemiştir.

Bu ekin yazımı sırasında, 08.11.2026'da, çözümleme sarmalayıcısının (`experiments/q1_curutme_cozumleme.py`) boru hattı sınaması mevcut B4 matrisiyle (`results/q1/konsey_b4_matris`, 20 model) ve 50 bootstrap yinelemesiyle koşulmuştur; çıktılar `results/q1/curutme_2026-11-08/_duman/cozumleme_sinama_{A,B,C1,C2,G,B118}.json` dosyalarındadır ve her biri `SINAMA_SONUC_DEGIL` alanını taşır. Bu sınamada A ve G'nin birincil nicelikleriyle doğrudan ilgili şu değerler görülmüştür. A sınaması ayna panel yalnız XCiT-S12'den oluşurken yapılmıştır (`cozumleme_sinama_A.json`, `sonuc.tum_modeller.blok_sonucu`): ρ_T(V-IN) +0,011 [%90: −0,030; 0,053] ve etiketi eşdeğer; σ_T(V-IN) − σ_T(R224-IN) −0,029 [%90: −0,042; −0,014] ve etiketi negatif, yani A'nın σ satırında "H yanlış" bölgesi; ikincil sıfırdan satırında ρ_T(V-scr) +0,201 [%90: 0,146; 0,246] ve σ_T(V-scr) − σ_T(R224-scr) −0,284 [%90: −0,308; −0,266]. A'nın birincil nicelikleri üç XCiT'li paneldedir ve bu tek üyeli değerler onların yerine geçmez; ancak σ satırının tek XCiT'li panelde "H yanlış" bölgesine düştüğü bilinmektedir, A'nın eşikleri buna rağmen değiştirilmemiştir ve A'nın sonucu okunurken bu ön bilgi hesaba katılmalıdır. G sınamasında ω-düzeltmeli artık farkı mevcut dokuz eğitilmiş modelde (V-scr, V-IN, R224-scr, R224-IN) −0,029, %90 bootstrap aralığı [−0,045; −0,016] çıkmıştır (`cozumleme_sinama_G.json`, aynı anahtar, `artik_fark_V_eksi_R`). Bu değer G'nin "H yanlış" bölgesine (> −0,05) düşer; G'nin kararı yeni iki hücre (V-scr+ ve V-IN21k) ve CKA kısmi Mantel'iyle verildiğinden ve eşik konsey raporunda önceden yazılı olduğundan eşik değiştirilmemiştir, ancak G'nin sonucu okunurken bu ön bilginin varlığı hesaba katılmalıdır. B, C1 ve C2 sınamaları yeni hücre bulunmadığı için hesaplanamadı çıktısı vermiştir.

Kod sınamaları için şu koşular yapılmıştır ve hiçbiri sonuç verisi değildir: kod değişikliğinin regresyon koşuları (her biri 50 eğitim iterasyonunun kaybı; `results/q1/curutme_2026-11-08/_duman/regresyon_*.txt`, özet `regresyon_ozet.md`), B'nin bir epokluk duman koşusu (`duman_B_s2401.log`), C1 ve C2 başlatma yolunun 20 batch'lik mini temiz koşuları (`duman_C1_mini_temiz.log`, `duman_C2_mini_temiz.log`) ve bunların yükleme matrisi (n = 100; üç duman modeli ile matris betiğinin kendiliğinden eklediği RobustBench başvuru modeli WRN_28_10, toplam dört model; `yeni_tip_n100/`), A'nın n = 200 kısa koşusu (`A_n200/`; üç XCiT ve bir epokluk duman V-scr+ modeli, yani matris bu duman ViT'nin satır ve sütununu içerir; duman model hiçbir hücreye karşılık gelmez ve matriste V-scr, V-IN, R224 ya da C1-R32 modeli yoktur), CKA ve Mantel boru hattının iki duman sınaması (`G_cka_duman/`: üç duman modeli, K = 3 olduğundan Mantel tanımsız; `G_cka_duman_k4/`: üç XCiT ve duman V-scr+ modeli, K = 4, `A_n200/` matrisiyle) ve B pilotu epok süresi ayrıştırıcısının sınaması (`duman_epok_sinama.json`). Duman kontrol noktaları `/mnt/d/adeb_sci_1_veri/_duman_curutme/` altındadır ve çözümlemeye girmez. İndirme denetimi `results/q1/curutme_2026-11-08/indirme_denetimi.json` ve `indirme_sha256.txt` dosyalarındadır.

Dondurmadan sonra ve ilgili blok koşulmadan önce bir sonuç açılırsa tarihiyle §15'e sapma olarak yazılır.

## 2. Tanımlar, hücreler ve karar ilkesi

Yeni üç eğitilmiş hücre ve bir panel tanımlanır; takma ad, tohum ve kontrol noktası yolu `raporlar/konsey_2026-10-29/hucre_tablosu_curutme.json` dosyasındadır. Bu tablo dondurulmuş `hucre_tablosu.json`'un 20 modelini aynı alanlarla taşır ve ayna_panel alanını ekler.

| Hücre | Model tipi | Başlatma | Temiz aşama | AT aşaması | Tohumlar |
|---|---|---|---|---|---|
| V-scr+ | `vit_tiny` (32→224) | rastgele | E_temiz epok (§6), AdamW lr 1e-3, wd 0,05, cosine + 10 epok ısınma, batch 128; RandomCrop(32, 4) + yatay çevirme + TrivialAugmentWide + RandomErasing(p 0,25) + mixup 0,8 / cutmix 1,0 + etiket yumuşatma 0,1 | B3 tarifi | 2401, 2402 |
| V-IN21k | `vit_tiny_in21k` | `vit_tiny_patch16_224.augreg_in21k_ft_in1k`, model içi normalizasyon AugReg pretrained_cfg'den | V-IN ile aynı: 30 epok, AdamW lr 1e-4, cosine T_max 30, batch 128 | B3 tarifi | 2501, 2502 |
| R224-SWSL | `resnet18_224_swsl` | `resnet18.fb_swsl_ig1b_ft_in1k` (CC-BY-NC-4.0, ağırlık dağıtılmaz), model içi normalizasyon pretrained_cfg'den | R224-IN ile aynı: 30 epok, AdamW lr 1e-4 | B3 tarifi | 1501, 1502 |
| ayna panel | RobustBench CIFAR-10 Linf | Debenedetti2022Light XCiT-S12, XCiT-M12, XCiT-L12 | eğitim yok | eğitim yok | yok |

B3 AT tarifi, dondurulmuş ön kaydın §4'ündeki ve `results/C1_REFERANS_FOYU.md` M13.1'deki (satır 2384-2440) tariftir: karışık kayıplı AT, PGD-10, ε 8/255, α 2/255, AdamW (wd 0,05) lr 1e-3, batch 64, cosine T_max 100, tavan 80 epok (`--stop-epoch 80`), sabır 20, min_delta 0,1, sabit doğrulama bölmesi (`data/val_split_indices.json`), yalnız crop ve çevirme artırması, `--save-every 10`. Komut `logs/konsey_zincir.log`:40'taki B3 AT komutunun model tipi ve çıktı dizini değiştirilmiş biçimidir.

σ, ρ, ω ve w yalnız dondurulmuş `model_duzeyi()` ile (bölünmüş yarı, log ölçek) hesaplanır. Hücre değeri tohumların ortalamasıdır. Aralıklar görüntü bootstrap'idir (B = 2000, tohum 20261030, bütün hücrelerde ortak ağırlık, yüzdelik %90 ve %95); iki tohumla tohum değişkenliği taşınmadığından aralık yalnız raporlanır, karar nokta kestirimiyle ve aşağıda yazılı aralık koşullarıyla verilir. Bu ekteki blokların hiçbiri Holm ailesine girmez; A, B, C1, C2 ve G karar kuralları önceden yazılı sınıflandırmalardır, D bir karar kuralıdır (B6), B1-09 ve B1-18 dondurulmuş F_B4 sınamalarını yeni matrislerde betimsel olarak yineler. Bir hücre hesaplanamazsa (kontrol noktası yok ya da manipülasyon denetimi kaldı) ona bağlı karar "hesaplanamadı" olarak raporlanır.

## 3. Kod, dondurulmuş dosyalar ve regresyon

Dondurulmuş dosyalara dokunulmamıştır: `ON_KAYIT_2026-10-29.md`, `ON_KAYIT_EK_B8_B10_2026-10-30.md`, `experiments/q1_konsey_ayrisim.py` (SHA-256 `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`), `experiments/c1_c3_transfer_matrix.py` (`f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7`), `models/q1/konsey/` altı, `results/C1_REFERANS_FOYU.md`, `results/q1/konsey_b3_tarif.json`. Çözümleme sarmalayıcısı dondurulmuş betiği importlib ile yükler ve özeti farklıysa kod 5 ile durur; matris sarmalayıcısı B8 için çatallanmış `experiments/q1_ek_transfer_matrix.py`'yi aynı biçimde yükler ve özgün betiğin özetini her koşuda `curutme_meta.json`'a yazar.

Eğitim koduna dört dosyada ekleme yapılmıştır: `cli/train.py` (iki yeni `--init-weights` değeri; temiz aşamaya özgü `--trivial-augment`, `--random-erasing`, `--mixup`, `--cutmix`, `--label-smoothing`, `--lr-warmup`, `--stop-epoch`), `src/training/trainer.py` (`mixup_fn`, `train_criterion`, `lr_warmup_epochs`, `stop_epoch`), `src/models/r224.py` (`vit_tiny_in21k` ve `resnet18_224_swsl` tipleri) ve `src/models/__init__.py`. Bayrakların hepsi varsayılanda kapalıdır. Regresyon kanıtı `results/q1/curutme_2026-11-08/_duman/regresyon_ozet.md` dosyasındadır: GPU'da belirlenimli kipte (CUBLAS_WORKSPACE_CONFIG, `torch.use_deterministic_algorithms`, flash ve mem-efficient SDPA kapalı) eski kod (`git archive` ile çürütme konseyi commit'inden çıkarılmış ağaç; commit kimliği `/mnt/d/adeb_sci_1_veri/_regresyon_eski_kod/KAYNAK_COMMIT.txt` dosyasındadır ve o commit ile bugünkü HEAD arasında `cli/` ve `src/` altında fark yoktur, `git diff --stat` boş) ve yeni kod V-scr temiz komutu, V-IN temiz komutu ve R224-scr AT komutunda 50 iterasyonun 50'sinde bayt düzeyinde aynı kaybı vermiştir; CPU'da V-scr temiz komutu da 50/50 aynıdır. Belirlenimsiz kipte aynı kodun iki koşusu arasındaki fark, eski ile yeni kod arasındaki farkla aynı büyüklük düzeyindedir (V-IN temiz komutunda en büyük mutlak fark eski-eski 0,0078, yeni-yeni 0,0200, eski-yeni 0,0112).

Yeni betikler `experiments/q1_curutme_transfer_matrix.py`, `experiments/q1_curutme_cka.py`, `experiments/q1_curutme_cozumleme.py`, `scripts/curutme_indirme.py`, `scripts/curutme_regresyon.py`, `scripts/curutme_denetim.py` ve zincir betiği `scripts/curutme_zincir.sh`'tır. Bütün dosyaların SHA-256 özetleri §16'dadır ve zincir başlamadan önce bu değerlerle karşılaştırılır.

## 4. Koşu sırası ve ortak kurallar

Bloklar tek bir zincir betiğiyle (`scripts/curutme_zincir.sh`) şu sırayla koşulur: indirme denetimi, A, B, C1, C2, D, G, B1-09, B1-18. Bir blok çökerse zincir sonrakine geçmeden durur ve çıkış kodunu `results/q1/curutme_2026-11-08/zincir_durum.tsv` dosyasına yazar. İndirme denetimi beş ağırlık dosyasının SHA-256 özetini `results/q1/curutme_2026-11-08/indirme_sha256.txt` ile karşılaştırır; uyuşmazlıkta zincir kod 3 ile durur.

Her GPU adımından önce bekçi boş GPU belleğine bakar: 20 GB'tan azsa 60 s aralıkla bekler, 12 saat içinde açılmazsa zincir kod 8 ile durur. B'nin iki epokluk pilotundan önce ayrıca GPU kullanımının %10'un altına inmesi en çok 2 saat beklenir; inmezse pilot paylaşımlı GPU'da koşulur ve `B_pilot.json` dosyasına `gpu_paylasimli: true` yazılır. Paylaşımlı GPU'da ölçülen epok süresi E_temiz'i küçültür; bu durum §15'e sapma olarak yazılır ve E_temiz yine pilottan hesaplanan değerde kilitli kalır.

Eğitim bloklarında tohum başına duvar saati sınırı vardır ve `timeout` ile uygulanır. Temiz aşama bu sınır içinde bitmezse zincir durur. AT aşamasına sınırın kalanı verilir; sınır dolarsa AT o ana kadarki en iyi doğrulama kontrol noktasıyla durur, `scripts/curutme_denetim.py kirpilma` seçilen epok son biten epoğun beş epok yakınındaysa "kırpılmış olabilir" işaretini `SURE_SINIRI` dosyasına yazar ve koşu dışlanmaz. Değerlendirme adımlarında zaman aşımı vardır; zaman aşımında adım önbellek ve `--skip-existing` ile bir kez yinelenir ve bu yineleme §15'e yazılır, ikinci zaman aşımında zincir durur.

C1 ve C2'de dondurulmuş ön kaydın §4'teki AT çöküş kuralı aynen uygulanır: 5. AT epoğunda doğrulama PGD doğruluğu %15'in altındaysa eğitim durdurulur ve zincir kod 5 ile durur; lr 5e-4 ile yeniden eğitim kararı kullanıcıya aittir ve uygulanırsa §15'e yazılır. B'de çöküş kuralı yoktur, çünkü B3'te kural yalnız ImageNet başlatmalı hücrelere uygulanmıştı ve V-scr+ sıfırdan başlatılır.

## 5. A: karma dönüştürücü ayna paneli (yalnız değerlendirme)

A bloğunda sınanan hipoteze göre ViT'nin kaynak açığı karma dönüştürücü paneline karşı da ağırlıkla simetrik benzemezliktir; yani panel CNN yerine üç XCiT'ten kurulduğunda ImageNet başlatmalı ViT'nin yönlü terimi sıfıra eşdeğerdir ve ResNet'e göre panelden uzaklığı ayna simetrisi verir.

Matris B4'ün 20 modeli ile XCiT-M12 ve XCiT-L12'den oluşan 22 × 22'liktir (PGD-10, ε 8/255, α 2/255, rastgele başlangıç, tohum 42, n = 10000). B4'ün mevcut 400 hücresi ve önbelleği yeniden kullanılır, yalnız yeni 84 hücre hesaplanır. Çözümleme `--blok A` ile ayna panel {XCiT-S12, M12, L12} üzerinde yapılır.

| Nicelik | Mevcut karşılaştırma değeri | H doğruysa | H yanlışsa |
|---|---|---|---|
| ρ_T(V-IN), birincil | tek XCiT'li ikincil panelde V-scr için ρ +0,198 / +0,202 / +0,204 (föy 1606); V-IN için tek XCiT'li değer +0,011 [%90: −0,030; 0,053], etiket eşdeğer (§1, sınama çıktısı) | ≤ +0,10 ve %90 aralığı ±0,10 içinde (eşdeğer) | ≥ +0,15 ve %90 aralığı +0,10'u dışlıyor (yönlü zayıf) |
| σ_T(V-IN) − σ_T(R224-IN) | birincil panelde mimari_IN −0,104 (föy 2229); tek XCiT'li ayna panelde −0,029 [%90: −0,042; −0,014], etiket negatif, yani H yanlış bölgesi (§1, sınama çıktısı) | ≥ 0, ya da %90 aralığı 0'ı kesiyor ve nokta ≥ −0,05 (ayna) | < 0 ve %90 aralığı 0'ı dışlıyor (negatif) |

Karar kuralına göre ρ_T(V-IN) eşdeğerse başlık değişmez. +0,10 ile +0,15 arasındaysa ya da aralık +0,10'u kesiyorsa sonuç belirsizdir; başlık değişmez, Sınırlılıklar'daki tek-XCiT cümlesi üç üyeli panelin değeriyle güncellenir. Yönlü zayıf çıkarsa başlık "against CNN targets" diye daraltılır. ρ_T(V-IN) ≤ −0,10 ve aralık −0,10'u dışlıyorsa ViT karma panele karşı yönlü güçlü kaynaktır ve betimsel raporlanır. σ farkı negatif çıkarsa "different" cümlesi kalır, ancak aile yorumu (CNN'e karşı dönüştürücü) kullanılmaz. İkincil olarak sıfırdan satırı (ρ_T(V-scr) ve σ_T(V-scr) − σ_T(R224-scr)) betimsel raporlanır. D bloğunda aynı çözümleme 28 modelli matrisle yinelenir (`cozumleme_A_d28.json`); birincil sonuç A'nın 22 modelli matrisidir.

Tohum yoktur; zaman aşımı 1,0 sa (`02_deney_adaylari.json`, A.gpu_saat), beklenen 0,28 sa.

## 6. B: V-scr+ (sıfırdan ViT-Tiny, güçlü temiz tarif)

B bloğunun hipotezine (H_mimari) göre sıfırdan satırdaki benzemezlik (H1, A^σ_scr = −0,364, föy 1526) mimariye aittir; ViT temiz doğruluğu ve kırılganlığı ResNet'e yaklaştırıldığında da sürer.

Temiz aşama E_temiz epoktur. İki epokluk pilot (tohum 2401, `-e 200 --stop-epoch 2`) koşulur ve epok süresi t, konsey kuralındaki "epok süresi" tanımına uygun olarak başlatma süresi (veri ve model kurulumu) hariç ölçülür (`02_deney_adaylari.json`, B.durdurma_kurali). t, ikinci epoğun eğitim döngüsü süresi (logdaki ilerleme çubuğunun son değeri) ile epok başına doğrulama payının toplamıdır; doğrulama payı, Trainer'ın yazdığı toplam eğitim süresinden iki çubuk süresi çıkarılıp ikiye bölünerek bulunur, çubuk okunamazsa t toplam eğitim süresinin yarısıdır. Hesap `scripts/curutme_denetim.py epok --log` ile yapılır ve logdaki epok sayısı pilot epok sayısından farklıysa hesaplanamadı verilir. E_temiz = min(200, floor(6300 s / t)) olarak iki tohum için kilitlenir. Taslaktaki "pilot duvar süresi / 2" tanımı yaklaşık 44 s'lik başlatma süresini de taşıyordu ve boş GPU'da bile E_temiz'i gereksiz yere düşürürdü; bu yüzden değiştirilmiştir. E_temiz bu tanımla da 200'ün altına inebilir. Güçlü artırmalı veri yükleyici depo varsayılanı olan iki işçiyle GPU'suz ölçümde epok başına yaklaşık 25,0 s sürmektedir (`results/q1/curutme_2026-11-08/_duman/yukleyici_hizi.txt`:2). E_temiz = 200 için t ≤ 31,5 s gerekir; t yükleyici süresinin altına inemeyeceğinden kalan pay yaklaşık 6,5 s'dir ve ViT'nin ileri-geri geçişi ile doğrulamanın yükleyiciyle örtüşmeyen kısmı bu payı aşarsa temiz aşama 200 epoktan kısa olur. Paylaşımlı GPU'da yapılan bir epokluk duman koşusunda aynı tanımla t = 70,2 s ölçülmüştür (çubuk 65 s, doğrulama payı 5,2 s; `results/q1/curutme_2026-11-08/_duman/duman_epok_sinama.json`, ilk satır); bu değer E_temiz = 89 verirdi. E_temiz < 200 çıkarsa V-scr+'nın temiz tarifi konseyin 200 epoklu tarifinden kısa olur. Bu durum sonuçla birlikte beyan edilir, B'nin kararı aynı kurallarla verilir ve kısa temiz aşama eşleşme koşullarının tutmamasına yol açarsa B betimsel kalır ve G birincil okuma olur. E_temiz < 200 olduğunda cosine çizelgesi E_temiz epok üzerinden kurulur (`-e E_temiz`); ısınma 10 epoktur. AT aşaması B3 tarifidir.

Manipülasyon denetimi AT'den önce ve T görülmeden yapılır: temiz aşamanın en iyi doğrulama doğruluğu (`TRAINING_COMPLETE` best_acc) C1 V-scr temiz aşamasının doğrulama doğruluğu ortalamasının en az 5 puan üstünde olmalıdır. C1 değerleri 81,90, 83,85 ve 83,25, ortalama 83,00, eşik 88,00'dır (`logs/C1_clean_vit_2001.log`:449, `logs/C1_clean_vit_2002.log`:456, `logs/C1_clean_vit_2003.log`:455; `scripts/curutme_denetim.py esik`). Denetim tutmazsa o tohumun AT'si başlamaz, durum `MANIP_KALDI` olarak kaydedilir ve zincir devam eder.

Eşleşme koşulları iki tohum ortalamasında denetlenir: |temiz(V-scr+) − temiz(R224-scr)| ≤ 6 puan ve |w(V-scr+) − w(R224-scr)| ≤ 2 puan. R224-scr'nin temiz doğruluğu 85,73 ve w'si 48,90'dır; V-scr'ninkiler 73,53 ve 55,63'tür (föy 1498 ve 1496).

| Nicelik | Mevcut karşılaştırma değeri | H_mimari doğruysa | H_mimari yanlışsa (H_yakınsama) |
|---|---|---|---|
| σ(V-scr+) − σ(R224-scr) | σ(V-scr) − σ(R224-scr) = −0,364 (föy 1526); σ(R224-scr) −0,645 (föy 1498) | ≤ −0,20 | > −0,15 |

Karar kuralına göre eşleşme koşullarının ikisi de tutarsa ve iki tohum hesaplanırsa, fark ≤ −0,20 ise H_mimari, > −0,15 ise H_yakınsama (sıfırdan satırdaki benzemezlik yakınsama ya da gürbüzlük düzeyi olarak yeniden yazılır, Özet ve Sonuç'taki sıfırdan cümlesi koşullanır), aradaki bölge (−0,20; −0,15] kısmen sonucudur ve V-scr, V-scr+, V-IN noktalarında σ'nın temiz doğruluk ve ω üzerine eğimi betimsel verilir. Eşleşme koşullarından biri tutmazsa B betimseldir, etiket yalnız bilgi için yazılır ve G'nin ω-düzeltmeli çözümlemesi birincil okuma olur. İkincil olarak ρ(V-scr+) − ρ(R224-scr) ve σ(V-scr+) − σ(V-scr) raporlanır.

Tohumlar 2401 ve 2402. Tohum başına duvar saati sınırı 5,0 sa (temiz ve AT birlikte); beklenen iki koşu 7,7 sa, gerçek tavan 10,0 sa (`02_deney_adaylari.json`, B).

## 7. C1: V-IN21k (ImageNet-21k AugReg başlatma)

C1 bloğunda keşifsel olarak sınanan doz-yanıt hipotezine göre başlatma etkisi ön eğitim verisinin ölçeğiyle büyür. V-IN'de başlatma σ'yı +0,270 artırmış ve ρ'yu −0,130 indirmiştir (föy 2230, 2236); V-IN'in ρ'su −0,118, σ'sı −0,739'dur (föy 1497).

| Nicelik | Mevcut karşılaştırma değeri | H doğruysa | H yanlışsa |
|---|---|---|---|
| σ(V-IN21k) − σ(V-IN) | σ(V-IN) −0,739 (föy 1497) | ≥ +0,05 | \|fark\| < 0,05 |
| ρ(V-IN21k) − ρ(V-IN) | ρ(V-IN) −0,118 (föy 1497) | ≤ −0,05 (yani ρ(V-IN21k) ≤ −0,168) | \|fark\| < 0,05 |

Karar kuralına göre iki koşul birlikte sağlanırsa doz-yanıt, ikisi birlikte "H yanlış" bölgesindeyse etkisiz (ImageNet-1k ötesindeki ön eğitim verisi bu boyutta etkisizdir, tartışma cümlesi daraltılır); diğer birleşimler kısmi olarak raporlanır. σ düşerse başlatma yorumu zayıflar ve aynen yazılır.

Manipülasyon denetiminde temiz günlüğündeki `INIT_WEIGHTS_RAPORU` satırındaki kaynak dosya özeti indirme denetimindeki HF LFS özetiyle aynı olmalı ve normalizasyon pretrained_cfg ile eşleşmelidir (`scripts/curutme_denetim.py init`); tutmazsa zincir kod 3 ile durur. Yeni ağırlığın DeiT-Tiny IN-1k ağırlığından farklı olduğu `indirme_denetimi.json` dosyasında kayıtlıdır. B3'ün ilk epok denetimi her ön eğitimli ağırlıkta kendiliğinden geçtiği için kullanılmaz.

Tohumlar 2501 ve 2502. Tohum başına duvar saati sınırı 3,7 sa; beklenen iki koşu 5,3 sa, gerçek tavan 7,4 sa. AT çöküş kuralı §4'teki gibidir.

## 8. C2: R224-SWSL (IG-1B yarı zayıf gözetimli ResNet-18 başlatma)

C2 bloğunun hipotezi, büyük ön eğitimin etkisinin ViT'ye özgü olduğudur. ImageNet-1k başlatması ResNet'te σ'yı değiştirmemiştir (+0,009, föy 2231); R224-IN'in σ'sı −0,635'tir (föy 1499).

| Nicelik | Mevcut karşılaştırma değeri | H doğruysa | H yanlışsa |
|---|---|---|---|
| σ(R224-SWSL) − σ(R224-IN) | baslatma_R224 +0,009 (föy 2231) | \|fark\| ≤ 0,05 | ≥ +0,10 |
| Ölçek satırı etkileşimi [σ(V-IN21k) − σ(V-IN)] − [σ(R224-SWSL) − σ(R224-IN)] | yok (yeni) | > 0 | (H yanlış kararı birinci satırdan verilir) |

Karar kuralına göre birinci satır H bölgesinde ve etkileşim pozitifse "başlatma etkisi ViT'ye özgü" okuması ölçek satırında tutar. Birinci satır ≥ +0,10 ise büyük ön eğitim iki aileyi de panele yaklaştırır ve bu okuma ölçek satırında tutmaz. Diğer durumlar ara olarak raporlanır. Ön eğitim verileri eşleşmediği için (gözetimli IN-21k ile yarı zayıf gözetimli IG-1B) etkileşim betimseldir. Manipülasyon denetimi C1'deki gibidir. Ağırlık CC-BY-NC-4.0 lisanslıdır; kontrol noktası dağıtılmaz, yalnız türetilmiş sayılar yayımlanır.

Tohumlar 1501 ve 1502. Tohum başına duvar saati sınırı 2,5 sa; beklenen iki koşu 4,3 sa, gerçek tavan 5,0 sa. AT çöküş kuralı §4'teki gibidir.

## 9. D: ortak değerlendirme

Yeni altı modelle 28 × 28 PGD-10 matrisi üretilir (A'nın 22 modeli ve 484 hücresi yeniden kullanılır; ayarlar A ile aynı). Kontrol noktası olmayan yeni model (manipülasyon denetimi kalan tohum) atlanır ve `curutme_meta.json`'daki `atlanan_eksik` alanına yazılır. AutoAttack standart sürümü (APGD-CE, APGD-T, FAB-T, Square) yeni altı modelde test kümesinin ilk 1000 görüntüsünde koşulur ve dondurulmuş B6 kuralı aynen uygulanır: PGD-10 doğruluğu ile AutoAttack doğruluğu arasındaki fark 10 puanı aşan model işaretlenir (`scripts/konsey_b6_maskeleme.py`, föy 1673). B10 girdi gradyanı kosinüsü 28 modelde `experiments/q1_ek_gradyan_kosinus.py gradyan` ile hesaplanır ve CIFAR-10 Mantel sınaması 9999 permütasyonla yinelenir.

H doğruysa maskeleme kuralı yeni modellerin hiçbirini işaretlemez; B6'da altı modelin farkı 3,20 ile 7,40 puan arasındaydı (föy 1463-1468). H yanlışsa işaretlenen model ayrı raporlanır ve B, C1, C2, A ve G çözümlemeleri o model çıkarılarak da hesaplanır (`--dislanan`); iki sonuç birlikte yazılır, karar işaretli modeller çıkarılmış sürümle verilir. B, C1 ve C2'nin çözümlemesi bu blokta, D'nin 28 modelli matrisiyle yapılır.

Zaman aşımları matris 4200 s, AutoAttack 3600 s, B10 900 s (toplam 2,4 sa ≤ 2,5 sa; `02_deney_adaylari.json`, D.gpu_saat); beklenen 1,24 sa.

## 10. G: doğrusal CKA ve ω-düzeltmeli benzerlik (yalnız değerlendirme)

G bloğunda sınanan hipoteze göre simetrik benzerlik terimi gürbüzlük düzeyine (ω = log w) indirgenmez. Mevcut kanıt: gradyan kosinüsü ile log τ̄ arasındaki ω kısmi Mantel ilişkisi CIFAR-10'da +0,936'dır (föy 1996).

Çözümleme birbirini tamamlayan iki parçadan oluşur. Birincisi, σ'nın model düzeyinde ω üzerine doğrusal regresyonudur (224 girdili eğitilmiş hücreler: V-scr, V-scr+, V-IN, V-IN21k, R224-scr, R224-IN, R224-SWSL); V hücrelerinin artık ortalaması eksi R hücrelerinin artık ortalaması hesaplanır ve görüntü bootstrap aralığı verilir. İkincisi, sınıf başı öncesi özniteliklerden doğrusal CKA'dır (temiz: test kümesinin ilk 5000 görüntüsü; PGD: kaynak başına önbellekteki PGD-10 örneklerinin ilk 1000'i, iki yönün ortalaması); CKA matrisi ile log τ̄ arasında Mantel ve ω kısmi Mantel sınaması B10 işlevleriyle (c_ij yerine CKA_ij) 9999 permütasyonla yapılır. Karar temiz CKA ile verilir; PGD CKA ikincildir.

| Nicelik | Mevcut karşılaştırma değeri | H doğruysa | H yanlışsa |
|---|---|---|---|
| ω-düzeltmeli artık farkı (V − R) | mevcut dokuz modelde −0,029 [%90: −0,045; −0,016] (§1, sınama çıktısı; karar verisi değildir) | ≤ −0,15 | > −0,05 |
| CKA ω kısmi Mantel r (tek yönlü p) | gradyan kosinüsünde +0,936 (föy 1996) | r > 0 ve p < 0,05 (işlemselleştirme) | p ≥ 0,05 ve \|r\| < 0,10 (işlemselleştirme) |

Karar kuralına göre artık farkı ≤ −0,15 ve kısmi Mantel pozitifse benzemezlik gürbüzlük düzeyine indirgenmez. Artık farkı > −0,05 ya da kısmi Mantel sıfıra yakınsa benzemezlik büyük ölçüde gürbüzlük düzeyiyle açıklanır ve "similarity" cümleleri buna göre daraltılır. Diğer durumlar ara olarak raporlanır. B'nin eşleşme koşulları tutmazsa bu blok B sorusunun birincil okumasıdır. Konsey raporu "kısmi Mantel pozitif" ve "sıfıra yakın" ifadelerine sayısal karşılık vermemiştir (`02_deney_adaylari.json`, G.beklenen_H_dogru ve G.beklenen_H_yanlis); tablodaki p < 0,05 ve |r| < 0,10 değerleri bu ekin işlemselleştirmesidir ve `experiments/q1_curutme_cozumleme.py` içindeki `kural_G` işlevinde aynı biçimde kodlanmıştır.

Zaman aşımı 0,3 sa (CKA adımı); beklenen 0,1 sa.

## 11. B1-09: saldırı gücü ve ε duyarlılığı (yalnız değerlendirme)

B1-09 bloğunun hipotezi, 2×2 sonuçlarının tek ε'a ve on adımlı saldırıya bağlı olmadığıdır. B4'ün 20 modelli matrisi üç yeni koşulda yeniden üretilir: ε = 4/255 (α 1/255), ε = 16/255 (α 4/255) ve ε = 8/255'te PGD-50 kaynak saldırısı (α 2/255). Her biri dondurulmuş betikle `--mod b4` kipinde ve dondurulmuş `hucre_tablosu.json` ile çözümlenir.

| Nicelik | Mevcut değer (ε 8/255, PGD-10) | H doğruysa (her üç koşulda) | H yanlışsa (herhangi bir koşulda) |
|---|---|---|---|
| H1, A^σ_scr | −0,364 (föy 1526) | ≤ −0,20 | > −0,15 |
| H2, I^σ | +0,260 (föy 1527) | ≥ +0,10 | ≤ 0 |
| H3, A^ρ | +0,003 (föy 1528) | %90 aralığı ±0,10 içinde (eşdeğer) | %95 aralığı 0'ı dışlar ve \|kestirim\| > 0,10 |

Karar kuralına göre üç koşulun hepsinde H bölgesi tutarsa 2×2 sonuçları bu saldırı gücü aralığında dayanıklıdır. Bir koşulda H yanlış bölgesine düşülürse sonuç o koşul için "ε'a ya da adım sayısına bağlı" olarak raporlanır ve manşet cümlesine "at ε = 8/255 under PGD-10" kaydı eklenir. Ara değerler betimsel raporlanır. H doğru bölgeleri dondurulmuş ön kaydın öngörülen büyüklükleridir (föy 1526-1528); H yanlış bölgeleri bu ekin işlemselleştirmesidir, H3 için dondurulmuş K-b çürütme ölçütünün (%95 aralığı 0'ı dışlar ve |kestirim| > 0,10) karşılığıdır. Bu bloklarda Holm uygulanmaz; F_B4'ün dondurulmuş kararı değişmez. Girdi çeşitlendirmeli (DI/TI) saldırı ve TGR doğrulaması bu ekin kapsamında değildir ve Sınırlılıklar'da açık iş olarak kalır.

Bu blokta tohum yoktur ve zaman aşımları ε 4/255 ve ε 16/255 için 1,0'er sa, PGD-50 için 2,0 sa (toplam 4,0 sa; `01_ic_gecerlilik.md`:81). Beklenen süre B9 kalibrasyonuyla (0,244 s/birim; `02_deney_adaylari.json`, sure_kaynaklari.kalibrasyon_matris) 20 model için ε turu başına yaklaşık 0,21 sa, PGD-50 için yaklaşık 0,69 sa'tir; bu değerler kestirimdir.

## 12. B1-18: kontrol noktası seçimi (yalnız değerlendirme)

B1-18 bloğunun hipotezi, 2×2 karşıtlıklarının en iyi doğrulama kontrol noktasının seçimine bağlı olmadığıdır. Seçilen epoklar V-scr'de 25, 18 ve 19 (föy 1383-1385), B3 hücrelerinde 16 ile 38 arasındadır (föy 1452-1457); C1 çiftinde son kontrol noktasında log τ̄ −1,170, seçilen kontrol noktasında −1,083'tür (föy 1713, 1707).

Bu blokta iki matris üretilir. Birincisinde eğitilmiş 12 modelin hepsi (C1 ve B3) son kontrol noktasıyla (`last.pth`) ve yedi panel üyesi ile XCiT-S12 aynen alınır; aynı takma adlar kullanıldığı için ayrı önbellek kullanılır ve çözümleme dondurulmuş `--mod b4` ile yapılır. İkincisinde B3'ün altı koşusunun 10 epoklu ara kontrol noktaları (toplam 22) birincil panelle birlikte matrise girer ve `--blok B118` ile σ, ρ, ω yörüngesi betimsel verilir. V-scr'nin ara kontrol noktası kaydedilmediği için (save-every 0) V-scr yalnız son kontrol noktasıyla girer.

| Nicelik | Mevcut değer (seçilen kontrol noktası) | H doğruysa | H yanlışsa |
|---|---|---|---|
| H1 son kontrol noktasında | −0,364 (föy 1526) | ≤ −0,20 ve seçilen değerden farkı \|Δ\| < 0,10 | > −0,15 |
| H2 son kontrol noktasında | +0,260 (föy 1527) | ≥ +0,10 | ≤ 0 |
| H3 son kontrol noktasında | +0,003 (föy 1528) | eşdeğer (±0,10) | %95 aralığı 0'ı dışlar ve \|kestirim\| > 0,10 |
| σ(V-IN) − σ(R224-IN) ortak ara epoklarda (10, 20, 30) | −0,104 seçilen noktada (föy 2229) | her ortak epokta ≤ 0 | herhangi bir ortak epokta ≥ +0,05 |

Karar kuralına göre son kontrol noktasında üç satır H bölgesindeyse H1 sayısına "at the selected checkpoint" kaydı gerekmez; H1 yanlış bölgesine düşerse bu kayıt eklenir ve sonuç kontrol noktası seçimine bağlı olarak raporlanır. Ara epok yörüngesi betimseldir.

Bu blokta da tohum yoktur ve zaman aşımları son kontrol noktası matrisi için 1,0 sa, ara noktalar için 1,5 sa (toplam 2,5 sa; `01_ic_gecerlilik.md`:191). Tablodaki |Δ| < 0,10 ve ara epoklar için ≥ +0,05 değerleri bu ekin işlemselleştirmesidir.

## 13. Öngörülerin özeti

| Blok | Birincil nicelik | Mevcut değer (kaynak) | H doğru | H yanlış | Tohum | Sınır |
|---|---|---|---|---|---|---|
| A | ρ_T(V-IN) üç XCiT panelde | +0,198 / +0,202 / +0,204 V-scr, tek XCiT (föy 1606) | ≤ +0,10, %90 ±0,10 içinde | ≥ +0,15, %90 +0,10'u dışlar | yok | 1,0 sa |
| B | σ(V-scr+) − σ(R224-scr) | −0,364 V-scr (föy 1526) | ≤ −0,20 | > −0,15 | 2401, 2402 | 5,0 sa/tohum |
| C1 | σ ve ρ farkı V-IN21k − V-IN | σ −0,739, ρ −0,118 (föy 1497) | σ ≥ +0,05 ve ρ ≤ −0,05 | ikisi de \|·\| < 0,05 | 2501, 2502 | 3,7 sa/tohum |
| C2 | σ(R224-SWSL) − σ(R224-IN) | +0,009 (föy 2231) | \|·\| ≤ 0,05 ve etkileşim > 0 | ≥ +0,10 | 1501, 1502 | 2,5 sa/tohum |
| D | B6 işareti | fark 3,20 ile 7,40 puan (föy 1463-1468) | işaret yok | işaretli model ayrı | yok | 2,5 sa |
| G | ω-düzeltmeli artık V − R ve CKA kısmi Mantel | −0,029 dokuz modelde (§1); +0,936 kosinüs (föy 1996) | ≤ −0,15 ve Mantel pozitif | > −0,05 ya da Mantel sıfıra yakın | yok | 0,3 sa |
| B1-09 | H1, H2, H3 üç koşulda | −0,364, +0,260, +0,003 (föy 1526-1528) | hepsi H bölgesinde | bir koşulda H yanlış | yok | 4,0 sa |
| B1-18 | H1, H2, H3 son kontrol noktasında | aynı | hepsi H bölgesinde | H1 > −0,15 | yok | 2,5 sa |

Gerçek tavanların toplamı (indirme denetimi dahil) yaklaşık 32,95 GPU-saattir; beklenen toplam yaklaşık 20,7 GPU-saattir (`scripts/curutme_zincir.sh` başlık tablosu). GPU bekleme süresi bu toplamlara dahil değildir; buna bekçinin beklemesi ile B pilotundan önceki en çok 2 saatlik kullanım beklemesi ve pilotun kendi 3600 s'lik zaman aşımı da girer.

## 14. Sınırlılıklar

V-scr+ temiz aşamada R224-scr'nin almadığı ağır artırmayı alır; 2×2'nin eşitliği yalnız AT tarifi için geçerlidir. Artırmanın kendisinin benzemezlik üretip üretmediğini Tier 2'deki E2 sınar ve bu ekle koşulmaz. w eşleşmesi temiz doğruluk eşleşmesinden zor olabilir; o durumda B karıştırıcıyı ayırmaz. C1'in doz ekseni yalnız veri ölçeğini değil ön eğitim tarifini de değiştirir (DeiT fb_in1k ile AugReg in21k + in1k ince ayar); iki etki ayrılamaz ve normalizasyon değerleri iki ağırlıkta farklıdır. XCiT karma mimaridir, ImageNet üzerinde çekişmeli ön eğitimden gelir ve üç üye aynı grup ile aynı tariftendir; grup etkisi ayrılamaz. Bu ekteki her eğitilmiş hücre iki tohumludur ve aralıklar tohum değişkenliğini taşımaz. GPU başka bir proje ile paylaşılırken koşulursa B'nin E_temiz değeri ve tohum sınırına dayanan AT süreleri boş GPU'dakinden kısa kalabilir; bu durum sonuçla birlikte beyan edilir.

## 15. Sapma politikası

Bu ekte yazılı tarif, tohum, eşik, sınır ya da çözümleme yolundan her ayrılış tarihiyle, nedeniyle ve etkilediği blokla bu bölüme eklenir; ayrılışı içeren sonuç ayrıca "sapma sonrası" diye işaretlenir. Önceden tanımlanmış üç durum sapma sayılır ve kendiliğinden kaydedilir: değerlendirme adımının zaman aşımıyla bir kez yinelenmesi, B pilotunun paylaşımlı GPU'da koşması ve C1 ya da C2'de AT çöküş kuralı sonrası lr 5e-4 ile yeniden eğitim. Tohum sınırının dolması ve B'de manipülasyon denetiminin kalması sapma değildir, önceden yazılmış sonuçlardır. Zincir çöküp yeniden başlatıldığında kesinti süresi de tohum sınırına sayılır (başlangıç `_baslangic_epoch.txt` dosyasında tutulur); kesinti bir tohumun AT aşamasını kırparsa bu durum sapma olarak yazılır. Kod hatası nedeniyle bir blok yeniden koşulursa hata, düzeltme ve düzeltilen dosyanın yeni SHA-256'sı yazılır; düzeltme öncesi çıktılar silinmez, ayrı klasöre taşınır. Bir sonucun eşiklere bakılarak yeniden tanımlanması bu politikanın dışında tutulur ve yapılmaz. Tier 2 bloklarından birinin koşulması bu ekin kapsamında değildir, ayrı bir ek ön kayıt gerektirir.

Bu ek dondurulurken kayıtlı bir sapma yoktur.

## 16. Betik ve dosya SHA-256 özetleri

Özetler zincir betiği tamamlandıktan sonra, dondurmadan hemen önce `sha256sum` ile hesaplanmıştır.

| Dosya | Durum | SHA-256 |
|---|---|---|
| `cli/train.py` | değişti (bu ek) | `530880a4612eaa629785a579d8fd5482cbcf87f77ab29d33981aa63d87782692` |
| `src/training/trainer.py` | değişti (bu ek) | `3dda9001e71d2bb9a7430d765bdc4054454b1fb07a0505034af0954505d222de` |
| `src/models/r224.py` | değişti (bu ek) | `71a10c699b3ea946fc7dd93a94006d2d2a9bf70540b2f603315cfec71d531b59` |
| `src/models/__init__.py` | değişti (bu ek) | `f7e0e23f4e38a7bacfb61515e82a46a2c99294ab69da81f8e2218474c3ce0b59` |
| `experiments/q1_curutme_transfer_matrix.py` | yeni | `a4cc8f07c05fe83680a0e0f7019b6415175161eee61d0eeed88cd4a2c8097228` |
| `experiments/q1_curutme_cka.py` | yeni | `e134736fe7ec0410b7c9f945b1b85a1b2aaa82688d2480571bd687b2ce9660b2` |
| `experiments/q1_curutme_cozumleme.py` | yeni | `4311e5237fdac6e1fa8acd3780ab38ba4546540aa10accaf04e7af9a20472046` |
| `scripts/curutme_indirme.py` | yeni | `73a861512232979e818a9044d7bb14ef15e1d58e0d33bba03f017df05557e9ff` |
| `scripts/curutme_regresyon.py` | yeni | `5de8c7733d98eea6584fc6596f9bd7e7a8b7c7dde1cd46e62b86b76375ee863a` |
| `scripts/curutme_denetim.py` | yeni | `384cd3f9fe08b4853b5b2eff733b5128df0353f60b431ead86d787e71a60a086` |
| `scripts/curutme_zincir.sh` | yeni | `a294816abe6a64b4d2a513282cae75e61dc60036183594e6c03ae4df488b639e` |
| `raporlar/konsey_2026-10-29/hucre_tablosu_curutme.json` | yeni | `34ec1dc765e7522bffb1f6c75c99cb4bd85d64d04382d2365362401b456d66e7` |
| `experiments/q1_ek_transfer_matrix.py` | değişmedi, çağrılır | `edec356afa594a681e1b3646b76f28c92bbf16c9159eace3dbc3c03cd6a87145` |
| `experiments/q1_ek_gradyan_kosinus.py` | değişmedi, çağrılır | `c82a66d196c38f23d688f610caf6ffceab0c01e7ebfa68e5358f832014043eed` |
| `experiments/run_autoattack_run2.py` | değişmedi, çağrılır | `f9dab33e5e03bcc8555ef0417101a4a332965bff30b94e606eac8ec0a0bdf369` |
| `scripts/konsey_b6_maskeleme.py` | değişmedi, çağrılır | `6e14580405ce38aa5b8b59debfe3e84ffc046e9db9bd4d2dc9fef07cf3d7d69e` |
| `src/training/adversarial_trainer.py` | değişmedi, çağrılır | `55e5b0d3ae567559edc45c8eb1b4a3a339a223d515719801ea0d280c923d270f` |
| `experiments/q1_konsey_ayrisim.py` | dondurulmuş | `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389` |
| `experiments/c1_c3_transfer_matrix.py` | dondurulmuş | `f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7` |
| `raporlar/konsey_2026-10-29/hucre_tablosu.json` | dondurulmuş | `2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500` |
| `data/val_split_indices.json` | değişmedi | `e60320ed1ec9c2ff82ef9f3fe67375f93706512c0c7c0f510922cb7feb979d0a` |

İndirilen ağırlıkların özetleri `results/q1/curutme_2026-11-08/indirme_sha256.txt` dosyasındadır ve zincirin ilk bloğunda bu dosyayla denetlenir.
