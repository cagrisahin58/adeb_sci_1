Güncel devir: HANDOFF_2026-10-31.md (01.11.2026)

# Konsey durum dosyası (29.10.2026)

Hazırlayan: deney analisti (opus alt ajan). Bu dosya yalnız durum tespitidir; öneri içermez. Her sayı bir dosyaya bağlanmıştır; `FÖY` kısaltması `results/C1_REFERANS_FOYU.md` dosyasını, `HÜKÜM` `raporlar/hakem_lecun_2026-10-04/00_LECUN_HUKUM.md` dosyasını, `İKİNCİ` aynı klasördeki `hakem_yontem_yeniden_yazim.md` dosyasını gösterir. Karantinadaki klasörlerden (run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA) hiçbir sayı alınmamıştır. "Türetilmiş" diye işaretlenen satırlar bu dosya için artefakttan hesaplanmıştır, föyde yoktur.

Konseyin önce bilmesi gereken üç olgu şunlardır. Birincisi, makalenin yön iddiası ("asimetri bu ViT-Tiny'nin kaynak etkisidir") tek bir transformatör örneğine dayanır ve dış havuzda bu ViT-Tiny, gürbüz modeller arasında kaynak etkisi bakımından tek aykırı noktadır; havuzdaki tek öteki dikkat tabanlı model olan XCiT-S12 melezdir ve CNN'ler gibi davranır. İkincisi, toplamsal kaynak-hedef ayrıştırması üçüncü bir model (WRN-28-10) ve etkileşimsizlik varsayımı ile 1 artık serbestlik derecesine dayanır; artık farkı asimetrinin yaklaşık üçte biridir, tezin "ayrıştırılamıyor" hükmü tam bu noktadan çıkar. Üçüncüsü, RobustBench kataloğunda CIFAR için saf ViT yoktur, yalnız XCiT ailesi (S12, M12, L12) vardır; ikinci bir saf ViT ancak kendi eğitimimizle elde edilebilir.

## 1. Makalenin şu anki iddiaları

Başlık `paper/manuscript/main.tex:62-63`: "The Conditioning Set Decides the Measured Transfer Asymmetry: An Exact Correction and a Source-Effect Reading for CNN versus Vision Transformer Robustness Comparisons". Özet tek satırdır (`main.tex:108`); katkılar `sections/01_introduction.tex:29, 33, 36, 43, 45`.

| No | İddia (alıntı özü) | Yer | Föydeki kanıt | En sert itiraz |
|---|---|---|---|---|
| İ1 | Dört protokol CNN→ViT asimetrisini "between 4.4 and 19.4 points" arasına koyar, yeniden eğitim "at most 2.4 points (run-to-run SD 0.23 to 1.27)" | main.tex:108; 01:29 | FÖY:47-60 (+13.57, +4.36, +8.27, +19.37; yayılım 15.01±0.84); FÖY M8.8 (satır 1291 vd.) | Dört protokol dört ayrı kestirilen niceliktir, yayılım tanım gereğidir (mercek_A:145, soru 1); seçim kuralının yayılım etkisi (2.16) yeniden eğitim aralığına (2.41) eşittir, yani karşılaştırma tabanı yalnız tohum varyansıdır (İKİNCİ:73-74, M7) |
| İ2 | "The unconditioned estimate lies 9.21 points above the target-correct one, where the law of total probability places it"; p, AT hedeflerde 0.989-1.000, standart eğitimlilerde 0.88'e iner, p=1 hatası en çok 1.6 | main.tex:108; 01:33 | FÖY:212 (raw−tc +9.21±0.76); `results/q1/ozdeslik_kontrol.json` (p_min 0.989014, FÖY:641); FÖY:841-873 (p en küçük 0.8774, artık en büyük 1.58) | Özdeşlik kuruluş gereği doğrudur, içerik yalnız p'dir; düzeltmenin pratik kullanımı döngüseldir (İKİNCİ:68, M5); "ImageNet ölçeğinde de geçerli kalır, çünkü aritmetiktir" (HÜKÜM:36) |
| İ3 | Onaylanan iki protokol 3.91 puan farklı (koşum düzeyi %95 aralık [3.12, 4.70]); başarılı-kaynak her-ikisi-doğrunun 11.10 üstünde | main.tex:108; 01:29 | FÖY:208-222 | 11.10 + 3.91 = 15.01 tam tutar, ham iç noktadır (İKİNCİ:57-58, M1); bc−tc için "kapalı biçim" metinde hiç yazılmamıştır (İKİNCİ:86, m6) |
| İ4 | "The direction is a source effect of this ViT-Tiny": kaynak terimleri +5.13 (C10) ve +9.54 (C100), hedef terimleri −2.03 ve −6.19 | main.tex:108; 01:36 | FÖY:385-395 (C10 çift başına), FÖY:432 vd. (C100), sabit-WRN karşıtlıkları FÖY:397-403 | Hedef terimi protokole bağlı: her-ikisi-doğruda −0.53±0.59, sıfırdan ayırt edilemez (FÖY:391; İKİNCİ:59-60, M2); temiz çiftte yön hedef terimiyle taşınır (İKİNCİ:61-64, M3); 6 hücre, 5 parametre (İKİNCİ:85, m5) |
| İ5 | Özdeşlik terimi temiz farkı izler: SVHN'de üç protokol yayılımı 1.49 ve 1.30, 0.47 fark için 0.19, 28 havuz çiftinde fark başına 0.872 artış; başarılı-kaynak fazlası küçülmez (0.21 farkta 9.03) | main.tex:108; 01:43 | FÖY:212 (SVHN raw−tc +1.49/+1.30); FÖY:891-899; FÖY:1002-1011 (egim +0.872, GA [+0.534; +1.274]); FÖY:982 (Carmon/Gowal 9.03) | Eşleşmiş çift öngörüsü aritmetiğin yeniden düzenlenmesidir; ölçülen içerik yalnız p ≥ 0.985, 57/60 iç nokta ve ss teriminin farktan bağımsızlığıdır (İKİNCİ:70-72, M6); üç protokol eğimi özdeşliğin iki kez ölçülmesidir (HÜKÜM:52, M1) |
| İ6 | Kontrol noktası seçimi yayılımı yaklaşık iki puan, temiz farkı yaklaşık 1.7 puan kaydırır, yönü değiştirmez | main.tex:108; 01:43 | FÖY:794-800 (son kontrol noktası: yayılım 12.84±0.34, temiz fark +10.55±0.59, bc +7.97±0.55) | ViT 18-25. epokta, 1 puanlık standart hatası olan 2.000 örneklik sinyalle seçilmiştir; 12 puanlık fark kısmen seçim artefaktıdır (mercek_A:65, Y2) |
| İ7 | Mutlak gürbüzlük her saldırıda CNN lehinedir ve temiz doğruluk ile koşullu duyarlılığa tam ayrışır | 01:45 | FÖY:8-45 (AA 37.93±0.14 / 29.14±0.40; McNemar) | Tarif standart PGD-AT değil, karışık kayıplı ince ayardır; iki modelin AA değeri referans PGD-AT'nin çok altındadır (mercek_A:68, Y3; HÜKÜM:62, M6) |
| İ8 | Üç okuma doğrudan ölçümde düşer: yerellik, CLS dikkat entropisi, TGR kazancı | 01:45 | FÖY:125 vd. (C5), FÖY:1107 vd. (TOST), FÖY:139 vd. (C2) | TGR bir uyarlamadır, özgün yöntemin yeniden üretimi değildir (mercek_A soru 9; 05_discussion.tex:64) |

## 2. Açık hakem itirazları

Aşağıdakiler LeCun turunda (04.10) ya metinle yalnız yumuşatılmış ya da hiç ele alınmamış itirazlardır. Yazım ve dizgi kusurları (B5, F1, F2) bilimsel olmadığı için dışarıda bırakılmıştır.

| No | İtiraz | Kaynak | Bugünkü durumu |
|---|---|---|---|
| A1 | Özdeşlik tanım gereği doğrudur; yeni olan yalnız p'nin ölçümüdür ve AT hedeflerde p ≈ 1 olduğu için düzeltme önemsizleşir | HÜKÜM:56 (M3); İKİNCİ:68 (M5); mercek_C:132 (soru 1) | Metin "elementary identity ... whose premise we measure" diyor (01:33); itirazın özü duruyor, p aralığı ile yayımlanmış ham oranlara sınır verme işi yapılmadı (İKİNCİ:69) |
| A2 | Tek çift, iki küçük model, yalnız CIFAR ölçeği | HÜKÜM:36, 62 (M6); mercek_A:68 (Y3); mercek_C:136 (soru 5) | Yalnız Sınırlılıklar paragrafında kabul ediliyor (05_discussion.tex:64); dış havuz protokol analizi için kullanıldı, mimari iddia hâlâ tek çifte dayanıyor |
| A3 | Aile ile mimari karışıyor: "CNN" ve "ViT" etiketi ön eğitim, ölçek ve gürbüzlük düzeyiyle birlikte değişiyor | Mahmood rejim notları FÖY:630-640; 05_discussion.tex:27 ("ImageNet-21k pre-training or model scale, remains open") | Çözülmedi. Bizim tasarımda tek transformatör aynı zamanda en zayıf modeldir (Bölüm 7a) |
| A4 | XCiT-S12 konvolüsyon-dikkat melezidir; havuzdaki "ViT karşı örneği" saf ViT değildir | İKİNCİ:86 (m8) | Metin "an attention model with convolutional components" diyor (05_discussion.tex:31); ikinci saf ViT yok |
| A5 | Eğitim tarifi karışıyor: karışık kayıplı (λ = 0.5) ince ayar, ViT'de AdamW, ResNet'te SGD, ViT 32→224 büyütülmüş girdide sıfırdan | HÜKÜM:62 (M6); mercek_A:68 (Y3); `logs/C1_at_vit_2001.log:5` ("Using AdamW optimizer for ViT (lr=0.001)") | Adlandırma düzeltildi; tarif farkının kaynak etkisine katkısı ölçülmedi |
| A6 | Ön eğitim farkı: Mahmood'un ViT ve BiT modelleri ImageNet-21K ön eğitimli, bizim ViT-Tiny sıfırdan; iki rejimde kaynak etkisinin işareti ters | FÖY:632-633; FÖY:700 (Mahmood C10 toplamsal kaynak farkı −25.01); mercek_A:140 (madde 7, "pretrained ViT") | Açık soru olarak bırakıldı (05_discussion.tex:27) |
| A7 | Kapasite eşleşmiyor (11.2M ile 5.7M parametre) | 05_discussion.tex:64; 05_discussion.tex:72 ("capacity-matched pair ... ViT-Small against ResNet-50") | Gelecek iş olarak yazıldı |
| A8 | Seçim kuralı etkisi (2.16) yeniden eğitim aralığına (2.41) eşit; ViT erken ve gürültülü seçiliyor | İKİNCİ:73-74 (M7); mercek_A:65 (Y2) | Son kontrol noktası ölçüldü (FÖY:788-800); karşılaştırma tabanı değişmedi |
| A9 | Toplamsal uydurma 6 hücre, 5 parametre; etkileşim sınanamaz | İKİNCİ:85 (m5); FÖY:380 | Değişmedi |
| A10 | SVHN iki tohum, 50 epok, AutoAttack yok | HÜKÜM:58 (M4) | Metinde nitelendi; veri aynı |
| A11 | "Rarely vary" ve "remain scarce" belgelenmiş taramaya dayanmıyor | İKİNCİ:89 (m11); mercek_C:70-72 (Y7) | Belgelenmiş tarama yok |

## 3. Tez çelişkisi: tam ayrışma noktası

Tez notu (`TEZ_OTURUMUNDAN_NOT_2026-10-06.md:10`) iki sabit-WRN karşıtlığını aynen kullanır: WRN hedefine ViT kaynağından 8.65, ResNet kaynağından 12.48; WRN kaynağından ViT hedefine 18.15, ResNet hedefine 21.48 (FÖY:73-77). Makale de aynı dört hücreyi kullanır (FÖY:401). Yani veri üzerinde çelişki yoktur; çelişki tanımlanabilirlik varsayımındadır.

İki modellik tasarımda iki köşegen dışı hücre vardır ve asimetri = (α_R − α_V) + (β_V − β_R) yazıldığında iki bilinmeyen tek gözleme düşer; tezin "bu tasarımla ayrıştırılamıyor" hükmü bu anlamda doğrudur. Makale ayrıştırmayı iki ek dayanakla yapar: üçüncü model (WRN-28-10) ve kaynak ile hedef arasında etkileşim olmadığı varsayımı. Bu varsayımın bedeli föyde görünür: hedef-doğru protokolde asimetri +4.41, kaynak farkı +5.13, hedef farkı −2.03, artık farkı +1.30 (FÖY:390); her-ikisi-doğruda asimetri +8.30, artık farkı +2.07 (FÖY:391). Artık, asimetrinin yaklaşık %25-30'udur ve 1 serbestlik derecesiyle sınanamaz. Ham protokolde ise hedef farkı +8.13'tür ve kaynak farkını (+4.47) geçer (FÖY:389); "kaynak etkisi" okuması yalnız koşullu protokollerde geçerlidir. Ayrıca sabit-WRN karşıtlığı "ViT'nin ResNet'e karşı kaynak etkisi"ni değil "WRN'ye karşı kaynak etkisi"ni ölçer; etkileşim varsa ikisi farklıdır.

Özetle tezin cümlesi "iki modelle ayrıştırılamaz" düzeyinde, makalenin cümlesi "üçüncü model ve etkileşimsizlik varsayımıyla ayrıştırılır" düzeyinde doğrudur. İkisini birleştirecek kanıt, her aileden birden çok örnek (en az iki ViT, en az iki CNN) içeren ve etkileşime serbestlik derecesi bırakan bir matristir. Bugünkü 8x8 havuzda CNN tarafı zengindir ama transformatör tarafında yalnız ViT-Tiny ve melez XCiT-S12 vardır.

## 4. Varlık envanteri

### 4.1 Kontrol noktaları (`models/`, toplam 40 GB; `du -sh`)

| Yol | Mimari | Veri | Eğitim | Tohum | Boyut | Durum |
|---|---|---|---|---|---|---|
| `models/c1/resnet18_s100{1,2,3}/resnet18/{clean,adv/adversarial_training}/{best,last}.pth` | ResNet-18 | CIFAR-10 | temiz 200 epok + karışık kayıplı AT | 1001-1003 | 86 MB/dosya | Geçerli (C1) |
| `models/c1/vit_tiny_s200{1,2,3}/vit_tiny/...` | ViT-Tiny (timm, 224 büyütme) | CIFAR-10 | aynı | 2001-2003 | 64 MB/dosya | Geçerli (C1) |
| `models/q1/cifar100/{resnet18_s100x,vit_tiny_s200x}/...` + `epochs/` | ResNet-18, ViT-Tiny | CIFAR-100 | aynı, epok dosyaları saklı (ResNet 53/45/70, ViT 28/32/41 dosya) | 3+3 | 43 MB/epok (ResNet) | Geçerli (Q1) |
| `models/q1/e2/...` + `epochs/` | ResNet-18, ViT-Tiny | CIFAR-10 | E2 seçim deneyi, 100 epok, her epok saklı (101 dosya/koşu) | 3+3 | 36 GB'ın çoğu | Geçerli (Q1) |
| `models/q1/svhn/...` + `epochs/` | ResNet-18, ViT-Tiny | SVHN | 50 epok AT | 1001-1002, 2001-2002 | 25-26 epok dosyası/koşu | Geçerli (Q1) |
| `models/robustbench_zoo/cifar10/Linf/` | Carmon2019Unlabeled (WRN-28-10), Engstrom2019Robustness (ResNet-50), Gowal2020Uncovering_28_10_extra (WRN-28-10), Standard (WRN-28-10, standart eğitim), Wong2020Fast (PreActResNet-18) | CIFAR-10 | dış | tek | 45-292 MB | Kullanımda |
| `models/robustbench_zoo/cifar100/Linf/Pang2022Robustness_WRN28_10.pt` | WRN-28-10 | CIFAR-100 | dış | tek | 146 MB | Kullanımda |
| Konteyner içi `/root/.cache/torch/hub/checkpoints/debenedetti2022light-xcit-s-cifar10-linf.pth.tar` | XCiT-S12 | CIFAR-10 | dış | tek | 103.6 MB | Bağlı birimde değil; konteyner yeniden kurulursa kaybolur |
| `models/resnet18/*`, `models/vit_tiny/*` (at_run2, at_run3, trades) | ResNet-18, ViT-Tiny | CIFAR-10 | C1 öncesi | | | KARANTİNA |
| `models/vit_cifar_tiny/{clean,adv}/...`, `models/densenet121/clean/` | CIFAR-native ViT, DenseNet-121 | CIFAR-10 (doğrulanmadı) | | | | Kaynak durumu bu dosyada doğrulanmadı |

L2 için ayrı eğitilmiş model yoktur; L2 transferi Linf ile eğitilmiş C1 kontrol noktalarında yapılmıştır (`results/q1/cifar10_l2/` yalnız sonuç içerir; 05_discussion.tex:64).

### 4.2 Veri setleri

`data/` (konteynerde `/workspace/data`, aynı bağlama): CIFAR-10 (`cifar-10-batches-py`), CIFAR-100 (`cifar-100-python`), SVHN (`train_32x32.mat`, `test_32x32.mat`), sabit bölme dizinleri (`val_split_indices*.json`, `e2_val_{A,B,C}.json`). ImageNet ve Tiny-ImageNet bulunamadı: `/home/firat`, `/mnt/c/Users/cagri`, `/mnt/d`, `/mnt/e` 5 düzey, `/mnt/f` 4 düzey derinlikte ve konteyner kökünde 4 düzeyde arandı; `/data` yok. ImageNet ön eğitimli timm ağırlıkları da konteyner önbelleğinde yok.

### 4.3 Kod yetenekleri

`experiments/c1_c3_transfer_matrix.py` keyfi model listesiyle transfer matrisi üretir: `--model AD:TIP:YOL` (tekrarlanabilir, yerel kontrol noktası), `--rb-model AD[:TAKMA]` (RobustBench, tekrarlanabilir), `--dataset {cifar10,cifar100,svhn}`, `--norm {linf,l2}` (Linf: PGD-10, ε = 8/255, α = 2/255; L2: ε = 0.5, α = 0.125), `--n-samples`, `--seed`, `--out-dir`; örnek bazlı npz yazar, var olan `transfer_matrix.json` üzerine yazmaz. Kısıt: RobustBench modelleri `threat_model="Linf"` sabit kodlu yüklenir (satır 60), yani L2 kataloğu bu bayrakla açılamaz. `experiments/q1_havuz_analiz.py KLASOR [--tohum --bootstrap --cikti]` bir matris klasöründen dört protokolü, p'yi, toplamsal kaynak-hedef uydurmasını ve yayılım eğimlerini çıkarır; maskeler `src/analysis/protokoller.py` içinde tek yerde tanımlıdır. `experiments/q1_kaynak_hedef_ayristirma.py` argümansızdır, 3x3 matrisleri ve Mahmood tablolarını ayrıştırır.

`src/attacks/` altında FGSM, PGD (Linf, rastgele başlangıçlı), PGD-L2, C&W (L2 ve Linf), DeepFool, AutoAttack (Linf, L2) ve uzamsal saldırılar vardır. MI-FGSM ve TGR yalnız `experiments/c1_c2_tgr.py` içinde, ViT→CNN yönü ve sabit çiftler için yazılmıştır; genel bir transfer saldırısı modülü değildir. Girdi çeşitliliği (DI), öteleme değişmezliği, SGM, LinBP ya da çoklu vekil (ensemble) saldırısı yoktur. Model kaydı: resnet18/34/50, densenet121/169/201, efficientnet_b0-b2, vit_cifar_tiny/small, vit_tiny/small/base (timm, 224 büyütme). Temiz eğitim CLI'ında `--timm-pretrained` bayrağı ImageNet ön eğitimli başlatma sağlar (`cli/train.py:33-57`); AT `--pretrained YOL` ve `--patience` alır.

## 5. Hesap süresi (RTX 5090, paylaşımlı)

Epok süreleri günlüklerdeki tqdm satırlarından okunmuştur (türetilmiş; betik `epok_sure.py` oturum çalışma alanındadır, sonuç aşağıda). Donanım notu: CLAUDE.md C1 kampanyasını 5060 Ti'ye, `TIMING.md` başlığı ise RTX 5090'a yazar; Q1 (E2, CIFAR-100, SVHN) koşuları her iki kaynakta 5090'dır. Bu yüzden bütçe için Q1 değerleri esas alınmalıdır.

| İş | Süre | Kaynak |
|---|---|---|
| Temiz ön eğitim ResNet-18, CIFAR-10, 200 epok | 0.63-0.68 sa | `logs/Q1_e2_clean_resnet18_100{1,2,3}.log` |
| Temiz ön eğitim ViT-Tiny, CIFAR-10, 200 epok | 1.31-1.38 sa | `logs/Q1_e2_clean_vit_tiny_200{1,2,3}.log` |
| AT ResNet-18, CIFAR-10, 100 epok tam | 2.66-2.78 sa (medyan epok 93-99 sn) | `logs/Q1_e2_at_resnet18_100{1,2,3}.log` |
| AT ViT-Tiny, CIFAR-10, 100 epok tam | 6.01-6.15 sa (medyan epok 213-219 sn) | `logs/Q1_e2_at_vit_tiny_200{1,2,3}.log` |
| AT ResNet-18, erken durdurmalı (71-77 epok) | 1.24-1.46 sa eğitim; 4696-5546 sn duvar | `logs/C1_at_resnet_100x.log`; `TIMING.md` |
| AT ViT-Tiny, erken durdurmalı (38-39 epok) | 1.82-1.89 sa; 6806-7094 sn duvar | `logs/C1_at_vit_200{2,3}.log`; `TIMING.md` |
| AT CIFAR-100 (erken durdurmalı) | ResNet 0.71-1.35 sa, ViT 1.31-1.68 sa | `logs/Q1_cifar100_at_*.log` |
| AT SVHN, 50 epok | ResNet 0.85-1.01 sa, ViT 2.66-2.88 sa | `logs/Q1_svhn_at_*.log` |
| AutoAttack, bir çift (iki model, n = 10000) | 9910-10980 sn (2.75-3.05 sa) | `TIMING.md` (C1_aa_pair1-3) |
| Beyaz kutu PGD-10, bir model, n = 10000 | ResNet 20-31 sn, ViT 44-48 sn | `TIMING.md` (C1_pgd_*) |
| 3x3 transfer matrisi (3 kaynak, 9 hedef değerlendirmesi, n = 10000) | yaklaşık 3.6-4.5 dk | npz zaman damgaları, `results/q1/temiz_ciftler/pair{2,3}/` (türetilmiş) |
| 8x8 havuz matrisi (8 kaynak, 64 değerlendirme) | yaklaşık 13.5 dk; kaynak başına yaklaşık 1.3-1.6 dk | `results/q1/havuz_cifar10/*.npz` zaman damgaları 18:23:17 → 18:36:49 (türetilmiş) |
| Üç temiz 3x3 + 8x8 havuz, tek iş | 28.4 dk | `logs/q1_temiz_ve_havuz.log` (BASLADI 15:08:25Z, BITTI 15:36:50Z) |

Buna göre yeni bir çift (iki mimari, temiz + 100 epok AT) yaklaşık 10.8 GPU-saat, erken durdurmalı C1 tarifiyle C1 günlüklerine göre yaklaşık 4.5-4.9 GPU-saattir (yukarıdaki satırların toplamı, türetilmiş). WRN-70-16 ya da XCiT-L12 gibi büyük RobustBench modelleriyle matris süresi ölçülmedi; tahmin edilmedi. İki uyarı: `logs/C1_at_vit_2001.log` bir yeniden başlatma içerir (FÖY:1385) ve epok çubuklarının toplamı 14.0 sa verir, bu koşu süre tabanı olarak kullanılmamalıdır. GPU 29.10'da başka bir işle 12.2 GB ve %89 kullanımdaydı (`nvidia-smi`).

## 6. RobustBench kataloğu (indirmesiz)

Konteynerdeki robustbench 1.1 ve timm 1.0.27'nin `model_dicts` sözlüğü okundu (`raporlar/konsey_2026-10-29/_rb_liste.py`, çıktı `_rb_liste.json`). Katalogda CIFAR-10 Linf için 76, CIFAR-10 L2 için 21, CIFAR-100 Linf için 38 model vardır; CIFAR-100 L2 kataloğu yoktur.

Dönüştürücü ailesi yalnız `Debenedetti2022Light_XCiT-S12`, `XCiT-M12` ve `XCiT-L12`'den oluşur ve hem CIFAR-10 Linf hem CIFAR-100 Linf'te bulunur; L2'de hiçbir dönüştürücü yoktur. Diskte bunlardan yalnız CIFAR-10 XCiT-S12 vardır (konteyner önbelleği). Melez ya da bileşik modeller `Bai2023Improving_edm` (CIFAR-10, CIFAR-100), `Bai2023Improving_trades` (CIFAR-100), `Bai2024MixedNUTS` ve `Peng2023Robust` (RaWideResNet) olarak listelenir; iç mimarileri bu dosyada doğrulanmadı.

ViT-Tiny ile ölçek olarak eşleşebilecek küçük CNN'ler CIFAR-10 Linf'te Andriushchenko2020Understanding ve Wong2020Fast (PreActResNet-18), Sehwag2021Proxy_R18, Rebuffi2021Fixing_R18_ddpm, Rade2021Helper_R18_{extra,ddpm}, Addepalli2021Towards_RN18, Addepalli2022Efficient_RN18, Gowal2021Improving_R18_ddpm_100m; CIFAR-100 Linf'te Rebuffi2021Fixing_R18_ddpm, Rade2021Helper_R18_ddpm, Addepalli2021Towards_PARN18, Addepalli2022Efficient_RN18'dir. CIFAR-10 L2'de küçük CNN'ler Sehwag2021Proxy_R18, Rebuffi2021Fixing_R18_cutmix_ddpm ve Rade2021Helper_R18_ddpm'dir. Diskte olanlar Bölüm 4.1'deki altı model ile XCiT-S12'dir. Katalog dışı saf ViT kontrol noktaları için Mo ve ark. (arXiv 2210.07540) ve Debenedetti ve ark. (arXiv 2209.07399) adayları vardır; kontrol noktalarının erişilebilirliği ve XCiT'in ön eğitim ayrıntısı doğrulanmadı.

## 7. Konsey için olgusal düğümler (artefakttan, yorum içermez)

(a) Havuzda kaynak etkisi ile kaynağın kendi beyaz kutu koşullu yanıltma oranı (türetilmiş; kaynak etkileri FÖY:993-1000, köşegen oranları `logs/q1_temiz_ve_havuz.log` havuz bölümü, `cond` alanı):

| Model | Kaynak etkisi (tc) | Kendi PGD-10 koşullu yanıltma (%) | Temiz (%) |
|---|---|---|---|
| ViT_Tiny_AT | −4.87 | 55.83 | 74.10 |
| ResNet18_AT | +3.65 | 47.56 | 85.37 |
| Wong2020_PRN18 | +3.40 | 42.10 | 83.34 |
| Engstrom2019_RN50 | +3.25 | 37.68 | 87.03 |
| Debenedetti2022_XCiT_S12 | +3.06 | 32.76 | 90.06 |
| Carmon2019_WRN28_10 | +3.10 | 28.68 | 89.69 |
| Gowal2020_WRN28_10 | +2.94 | 25.25 | 89.48 |

Altı gürbüz CNN ve melez arasında kaynak etkisi 2.94 ile 3.65 arasında kalır, beyaz kutu oranı ise 25.25 ile 47.56 arasında değişir. ViT-Tiny bu bandın 7.8 puan altındadır. Bu desen tek bir transformatör noktasına dayanır; gürbüzlük ile mimari bu havuzda ayrıştırılamaz.

(b) Standart eğitimli çiftte ViT-Tiny hem en zayıf kaynak (−46.68±1.44) hem en az kırılgan hedeftir (−50.17±0.99); Standard WRN'den ResNet18_clean'e hedef-doğru oran 84.05±1.50, ViT_Tiny_clean'e 7.62±0.59'dur (FÖY:1410-1420). Aynı ViT-Tiny standart rejimde de dış modellerle çok az özellik paylaşır.

(c) Mahmood ve ark.'nın ImageNet-21K ön eğitimli modellerinde CIFAR-10 toplamsal kaynak farkı (CNN eksi ViT) −25.01, aile terimli uydurmada −10.78'dir (FÖY:700); işaret bizimkinin tersidir. CIFAR-100'de sıfırdan eğitilmiş ResNet-56/164 ile ViT çiftlerinin 6/6'sı bizim yönümüzü verir (FÖY:680-692).

(d) Son kontrol noktasında temiz fark 12.26'dan 10.55'e, her-ikisi-doğru asimetrisi 8.27'den 7.97'ye, dört protokol yayılımı 15.01'den 12.84'e iner; özdeşlik öncülü p en az 0.9915'tir (FÖY:800, 825-827). E2 koşularında 100 epoklık tam yörüngeler ve her epok kontrol noktası diskte durur (Bölüm 4.1).

(e) Mevcut matris betiği yeni kontrol noktalarını ve XCiT-M12/L12 gibi katalog modellerini kod değişikliği olmadan alabilir; 8x8 bir matris yaklaşık çeyrek saattir (Bölüm 5). Bütçeyi belirleyecek kalem yeni eğitimdir: ViT-Tiny için tam AT 6 GPU-saat civarındadır.
