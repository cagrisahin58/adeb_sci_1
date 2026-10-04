# B1 toplama dosyasi: ISTATISTIK DEFTERI (lens B, istatistik ve kimlik)

Tarih: 2026-10-04. Toplayici: B1. Kapsam: `paper/manuscript/sections/03_methodology.tex` (03) ve `04_experiments.tex` (04) tam okundu; 01, 05, 06 ve ozet yalniz seed sayisi ve tekrar eden istatistik cumleleri icin tarandi. Hicbir el yazmasi, veri ya da betik dosyasi degistirilmedi. Gecici betikler `_tmp/` altinda (t1..t26.py, g1..g12.sh); `scripts/verify_manuscript_numbers.py` yalniz okuma amacli calistirildi (cikti `_tmp/verify_out.txt`: TOPLAM=158 kontrol, EN_EKSIK=0, TR_EKSIK=0; bu betik sayinin metinde GECTIGINI dogrular, baglamini ya da McNemar, TOST, mekansal p, dikkat TOST'unu dogrulamaz).

Isaret sozlugu (yalniz olgu isaretidir, derece degildir):
- (a) artefakt bulunamadi ya da yalniz uretilmis .md / betik / hesaplama ile yeniden uretilebildi, saklanan JSON degeri yok
- (b) artefakt degeri yuvarlama sonrasi metinden farkli ya da metin sinirini saglamiyor
- (c) cikarim birimi ilgili yerde adlandirilmamis
- (d) ornek bazli (per-sample) p, mimari (kosu duzeyi) bir iddiayi destekliyor
- (e) GA, tohum basina uclarin ortalamasi olarak tarif ediliyor
- (f) 2 tohumlu nicelige ± SD verilmis
- (g) sayi C1 oncesi (karantinadaki run1/run2/run3) kaynakli; metin "onceki tek kosu" olarak etiketliyor
"Birim" sutununda: S = ornek bazli (per-sample, tek kosu icinde), K = kosu duzeyi (3 tohum, df=2), Kume = kume bootstrap.
"SD tanimi": c1_eval/c1_seeds/q1 ozetleri ornek SD (ddof=1) kullaniyor (ornek: values 85.37, 85.94, 86.04 -> 0.3614); istisna c1_statval (saldiri tohumu, ddof=0, 0.0471).

## 0. On ozet (10 satir)

1. 03 ve 04 icinde 181 numarali kayit (A01-A11, B01-B13, E01-E94, L01-L09, G01-G14, S01-S05, F01-F11, T01-T05, V01-V13, O01-O06) cikarildi; her biri satir numarasi, birim, n, artefakt yolu ve saklanan deger ile asagidaki tablolardadir.
2. Tohum sayilari: CIFAR-10 3 (RN18 1001-1003, ViT 2001-2003), CIFAR-100 3, SVHN 2 (1001-1002, 2001-2002), L2 kolu CIFAR-10'un ayni 3 ciftini kullaniyor, WRN tek harici kontrol noktasi, "yerel ViT" kontrolu ve "onceki tek kosu" birer kontrol noktasi, saldiri-tohumu ablasyonu tek kontrol noktasi cifti uzerinde 3 saldiri tohumu (bolum A).
3. 2 tohumlu nicelige ± SD verilen yerler: SVHN Tablo 4 (04:224-238), 04:220, 04:242 (spread 3.70±0.62) ve ilgili artefakt sd'leri; metin 04:240 iki kosudan kosu-arasi SD'nin bilgi tasimadigini ayrica yaziyor (bolum B-SVHN).
4. Sayi-artefakt uyumu: Tablo 1-5, 3x3 matris, CIFAR-100, SVHN, L2, gradyan, oznitelik kaymasi, TGR, varyans ve secim sayilarinin cogu saklanan JSON'la yuvarlama sonrasi uyusuyor; uyumsuzluklar bolum C'de.
5. (b) McNemar sinirlari: 04:41 "p<10^-84 (AA), p<10^-120 (PGD)"; saklanan en buyuk degerler 1.231e-84 ve 1.917e-120 (c1_seeds/c1_seed_summary.json pairs[].mcnemar_*.p_exact), yani yazilan "<" sinirlarini saglamiyor.
6. (b) Tablo 5 "Alignment (signed)" 0.0014 ve 0.0005 yalniz tohum 1 degeri (a3 pair1); tohum 2 ve 3: 0.0008/0.0004; tablo basligi "mean±std over three runs" diyor.
7. (b) 3x3 matrisin (c1_c3/c3_summary.json) ayni hucreleri Tablo 3'ten (c1_transfer_summary.json) farkli: CNN->ViT ham 41.07±0.58 ve 41.02±0.55; hedef-dogru 19.93±0.20 ve 19.87±0.18; ViT->CNN ham 27.45±0.34 ve 27.45±0.27; hedef-dogru 15.52±0.64 ve 15.51±0.59; metin farki anmiyor.
8. (a) saklanan artefakti bulunmayanlar: kosu-duzeyi t araligi [7.68, 8.86] ve [10.07, 11.77] (yalniz verify betigi/hesaplama), Tablo 6 kosu-duzeyi p'leri 0.54/0.40/0.54/0.47 (JSON'da yok, c5_spatial.json'daki kosu farklarindan yeniden uretildi), SVHN-dahil 3-protokol egim GA'si [+0.361, +0.665] (nokta tahmini saklanan ciftlerden 0.4697 cikiyor, GA saklanmamis), dikkat entropisi TOST (marj ±0.05, p=0.006), "devrilen/devrilmeyen" karsilastirmasi (test yok), onceki tek kosu sayilari (77.50, 0.88, TOST ±2 kabulu), CIFAR-100 tutma oranlari 0.885/0.802 (JSON yok; logs/Q1_cifar100_clean_*.log "Best test accuracy" satirlarindan uretiliyor ve bu satirlar 2000 orneklik secim kumesi dogrulugudur).
9. (d) ve (c): mimari/saldiri karsilastirmalari ornek bazli McNemar ile destekleniyor (04:41, 04:64, 04:269, 04:439); kosu-duzeyi test yalniz 04:117, 04:204 (t araligi), 04:303 ve Tablo 6'da. (e) iki yerde adlandirilmis ve "kapsama garantisi yoktur" notuyla birlikte: 04:117 ([7.33, 9.22]), 04:204 ([9.47, 12.35]) ve SVHN 04:240 ([-0.76, +0.07]).
10. Ek olgu: 03:158 "kabul ettigimiz tek esdegerlik SVHN'de" diyor; 04:392 dikkat entropisinde TOST ile ikinci bir esdegerlik kabulu (±0.05 nat, 12 katman) raporluyor.

## A. Tohum ve kontrol noktasi sayilari (veri kumesi bazinda)

| ID | Konum | Olgu | Artefakt | Saklanan |
|---|---|---|---|---|
| A01 | 03:100; 04:13 | CIFAR-10: 3 bagimsiz tekrar/mimari; seed 1001-1003 (ResNet-18), 2001-2003 (ViT-Tiny); tum tablolar "3 tohum ortalama ± SD" | results/q1/KOKEN.json tohumlar."cifar10 (C1/E2)"; c1_seeds/c1_seed_summary.json pairs (3 cift) | resnet18 [1001,1002,1003]; vit_tiny [2001,2002,2003] |
| A02 | 04:187-191 | CIFAR-100: 3 tohum cifti | KOKEN.json tohumlar."cifar100 (E1)"; q1/e1_cifar100_summary.json mimariler.*.ozet.n_tohum | 3 ve 3 |
| A03 | 04:224, 04:240, 04:244 | SVHN: 2 tohum cifti, 50 AT epoku, AA yok, 3. mimari yok | KOKEN.json "svhn (E7-kisa)"; q1/e7_svhn_summary.json mimariler.*.ozet.n_tohum | resnet18 [1001,1002]; vit_tiny [2001,2002]; n_tohum 2 |
| A04 | 04:252-256 | L2 kolu: CIFAR-10'un ayni 3 kontrol noktasi cifti; PGD-L2 tam test n=10,000; AA-L2 on-kayitli 5,000 ornekli altkume | q1/cifar10_l2/e6_aa_l2_summary.json | n_samples 5000 (AA), n_cift 3; PGD n_tohum 3, n 10000 |
| A05 | 04:28-37 | WRN-28-10: tek harici kontrol noktasi, ± yok; temiz/FGSM/PGD yerel tam test, AA RobustBench raporu (yeniden kosulmadi) | results/wrn_eval/wrn_eval_summary.json (c1_* ve q1/* disinda, karantina listesinde de degil); C1_REFERANS_FOYU.md "WRN" satiri | clean 89.48, fgsm 70.91, pgd10_eps0.03137 66.92, n=10000; AA 62.76 yalniz foyde |
| A06 | 04:296-299 | "ViT (native)": tek kontrol noktasi, sabit-bolme protokolunden once, test kumesinde secilmis (dipnot) | results/c1_gradient/pair1/gradient_statistics.csv (satir ViT_CIFAR_Native_AT) | hoyer 0.4046, gini 0.5712, rel 0.1785, align 0.0794, n=500; gradient_summary.json model_paths yalniz ResNet18_AT ve ViT_Tiny_AT'yi listeliyor (native yolu yazili degil) |
| A07 | 04:45, 04:57-59, 04:96-101, 04:305 | "Onceki tek kosu" (dogrulama bolmesi on-egitimde gorulmus, n=7,260): 1 kontrol noktasi cifti, SD yok | C1_REFERANS_FOYU.md Tablo II/III ("Eski tek kosu (sizintili)", "run3 fark" sutunu); c1_transfer_summary.json protocols.*.old_run3_diff | 8.27, 0.63, 5.33, 11.17 (g) |
| A08 | 03:156; 04:449 | Saldiri-tohumu ablasyonu: tohum 42,123,456; sabit 1,000 ornekli altkume; her mimari icin TEK kontrol noktasi (pair1: s1001, s2001) | results/c1_statval/statistical_validation.json (seeds, n_samples, model_paths); KOKEN.json attack_seed_ablasyon | n_runs 3, n_samples 1000; model_variant "run3-metric" |
| A09 | 03:100 | Dogrulama bolmesi: 2,000 ornek, seed 777, tum modellerde ortak; egitimden cikarilmis | logs/C1_clean_resnet_1001.log satir 4 ("Fixed val split ... egitim 48000 ornek; secim 2000 val ornegi uzerinden (test kullanilmiyor)") | 48000/2000 |
| A10 | 04:449, 04:453 | Tum tohumlar tek ortak dogrulama bolmesini paylasiyor; metin bunun bolme-bolme varyansini paydadan disladigini soyluyor | 04:453 metni; A09 | tek bolme |
| A11 | main.tex ozet; 01_introduction.tex:16 | Ozet ve giris "uc kosu" diyor; SVHN'in iki tohumlu oldugu 04:224/240/244'te var, 01/05/06 ve ozette taranan cumlelerde yok | grep (01, 05, 06, ozet) | -- |

## B. Istatistik defteri

### B1. Yontem bolumu (03) istatistik beyanlari

| ID | Konum | Nicelik | Basili deger | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| B01 | 03:100 | Tablo istatistigi tanimi | "mean and standard deviation over these three runs" | K, n=3 | c1_eval_summary.json values; c1_seed_summary.json aggregate | SD ddof=1 (ornek: 0.3614) | birim adli |
| B02 | 03:118 | Transfer GA tanimi | "percentile bootstrap over samples (10,000 resamples)" | S, tek kosu | c1_transfer/pair*/a2_transfer_protocols.json n_bootstrap | 10000 | birim adli (ornek) |
| B03 | 03:118; 04:84 | Transfer orani n | "full test set (10,000)" | -- | a2 JSON protocols.*.n_conditioned | 10000 (ham); hedef-dogru 7410/7347/7301 (CNN->ViT) | -- |
| B04 | 03:121; 04:279 | Hizalanma ciftleri | "500 x 499 / 2" | S | c1_a3/pair*/a3_gradient_paired.json alignment.*.n_pairs | 124750 (=500*499/2) | -- |
| B05 | 03:134 | Dikkat olcumu n | "n=1000 samples per run" | S icinde kosu | c1_c4/pair*/c4_summary.json n_samples; vit.attention.n_batches | n_samples 1000 (3 kosu); n_batches 20 | -- |
| B06 | 03:156; 04:449 | Saldiri-tohumu SD | "SD 0.05 (CNN), 0.00 (ViT)" | 3 saldiri tohumu, 1 kontrol noktasi, n=1000 | c1_statval/statistical_validation.json results[] | ResNet18_AT robust_std 0.0471 (ddof=0), clean_std 0.0; ViT robust_std 0.0, clean_std 0.0; robust_mean 45.53 / 34.70 | tek kontrol noktasi; SD tanimi ddof=0 (diger tablolarda ddof=1) |
| B07 | 03:156 | Kontrol noktasi secimi: on sekiz kombinasyon | "eighteen combinations" | 3 tohum x 2 mimari x 18 hucre | q1/e2/e2_grid.json izgara | bolmeler [B,C] x patience [0,10,20] x yumusatma [1,3,5]; hucre_sayisi 18 | -- |
| B08 | 03:158 | Testler: McNemar tam, Wilcoxon+Holm (3 seyreklik olcusu), eslesmis bootstrap (10,000), isaret-cevirme permutasyonu (20,000) | metin | S | a2 JSON n_permutation 20000, n_bootstrap 10000; a3 JSON n_bootstrap 10000 | uyusuyor | -- |
| B09 | 03:158 | "Iki cikarim birimi ... birim her testin yaninda adlandirilir ... iki birim ayrilirsa ikisi de raporlanir; gradyan bolumunde olur" | metin | -- | 04:303 | iki birim 04:303'te raporlu | -- |
| B10 | 03:158 | TOST ana marji ±2 puan, "karsilastirmalardan once, PGD dogrulugundaki kosu-arasi degiskenlikten" sabitlendi | metin | -- | a2 JSON tost_margin_rationale | "2pp marji, egitim-kosusu duzeyindeki gozlenen varyasyonun (~PGD birkac puan) altinda kalan farklari pratikte-esdeger sayma ilkesine dayanir; +-1/+-3 duyarlilik tablosu verilir" | -- |
| B11 | 03:158 | Asimetrinin kosu-arasi SD 0.23; marj "some eight times too generous" | 0.23; ~8 kat | K | c1_transfer_summary.json both_correct_paired / protocols.both_correct.diff | std 0.2312 (protokol tablosu), 0.2364 (eslesmis); 2/0.2312 = 8.65 | -- |
| B12 | 03:158 | "kabul ettigimiz tek esdegerlik SVHN'de; ±1'de de gecerli" | metin | S (iki kosu) | q1/svhn/transfer/pair{1,2}/a2_transfer_protocols.json tost_sensitivity | margin_1pp p = 0.000749 (pair1), 0.00109 (pair2); equivalent_at_0.05 true; 04:392 dikkat TOST kabulu ayri (bkz. F06) | (f); metin sayimi ("tek") ile 04:392'deki ikinci kabul |
| B13 | 03:158 | "tum betikler seed 42 ... her sayi boru hattindan yeniden uretilebilir" | metin | -- | a2 JSON seed 42; KOKEN.json attack_seed 42 | uyusuyor | -- |

### B2. Tablo 1 ve 04:41 (saglamlik)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E01 | 04:26 | ResNet-18 temiz egitim: temiz / FGSM / PGD | 95.25±0.15 / 40.29±1.77 / 0.03±0.03 | K, n=3; her kosu n=10,000 | results/c1_eval_summary.json resnet18_clean | 95.25±0.15 [95.09, 95.26, 95.39]; 40.29±1.77 [39.02, 42.31, 39.55]; 0.03±0.03 [0.0, 0.04, 0.06] | uyusuyor |
| E02 | 04:31 | ViT-Tiny temiz egitim | 80.09±0.60 / 6.10±1.47 / 0.05±0.05 | K, n=3 | c1_eval_summary.json vit_tiny_clean | 80.09±0.60; 6.10±1.47 [7.71, 4.82, 5.78]; 0.05±0.05 | uyusuyor |
| E03 | 04:27 | ResNet-18 AT: temiz / FGSM / PGD / AA | 85.78±0.36 / 53.46±0.08 / 44.11±0.50 / 37.93±0.14 | K, n=3 | c1_eval_summary.json resnet18_at; c1_seeds/c1_seed_summary.json aggregate.resnet.aa | 85.78±0.36; 53.46±0.08; 44.11±0.50; aa 37.93±0.14 [37.93, 37.79, 38.07] | uyusuyor |
| E04 | 04:32 | ViT-Tiny AT | 73.53±0.55 / 36.31±0.42 / 32.69±0.22 / 29.14±0.40 | K, n=3 | c1_eval_summary.json vit_tiny_at; c1_seed_summary.json aggregate.vit.aa | 73.53±0.55; 36.31±0.42; 32.69±0.22; aa 29.14±0.40 [29.59, 28.86, 28.96] | uyusuyor |
| E05 | 04:28, 04:34-37 | WRN-28-10 satiri | 89.48 / 70.91 / 66.92 / 62.76 | tek kontrol noktasi, n=10,000 | results/wrn_eval/wrn_eval_summary.json; AA foyde | 89.48 / 70.91 / 66.92; AA 62.76 (RobustBench) | AA artefakti yok (metin: yeniden kosulmadi); wrn_eval c1_*/q1/* disinda |
| E06 | 04:41 | CNN-ViT mutlak ustunluk: McNemar, her kosu icinde | "p < 10^-84 (AA), p < 10^-120 (PGD-10)" | S, kosu basina n=10,000 eslesmis; 3 kosu | c1_seeds/c1_seed_summary.json pairs[].mcnemar_aa/mcnemar_pgd | AA p_exact: 1.231e-84, 1.081e-96, 3.208e-93; PGD: 1.172e-153, 1.272e-140, 1.917e-120 (yalniz-ResNet/yalniz-ViT sayilari AA 1362/528, 1397/504, 1478/567; PGD 1677/483, 1658/511, 1665/581) | (b) en buyuk AA 1.231e-84 > 1e-84, en buyuk PGD 1.917e-120 > 1e-120; (d) mimari iddia, kosu-duzeyi test yok |
| E07 | 04:41 | "Seed-level variation ... at most 0.55 points on any reported accuracy" (AT cifti) | 0.55 | K, n=3 | c1_eval_summary.json | AT SD'leri: 0.36, 0.08, 0.50 (CNN temiz/FGSM/PGD), 0.55, 0.42, 0.22 (ViT); AA 0.14, 0.40; maks 0.55 | uyusuyor |
| E08 | 04:41 | Temiz-egitimli taban cizgilerde FGSM SD "up to 1.8" | 1.8 | K | c1_eval_summary.json | 1.77 | uyusuyor |
| E09 | 04:41; 04:64 | Temiz dogruluk farki | 12.3 puan | K, n=3 | c1_seed_summary.json aggregate.gaps.clean | mean 12.2567, SD 0.8992, degerler [11.27, 12.47, 13.03] | uyusuyor |
| E10 | 04:41 | AA, PGD-10'un altinda | 6.2 (CNN), 3.6 (ViT) | K | c1_seed_summary.json aggregate | 44.11-37.93 = 6.18; 32.69-29.14 = 3.55 | uyusuyor |
| E11 | 04:41 (turetilmis) | Kosu-duzeyi eslesmis t (df=2) CNN-ViT farki; metinde YOK, bu toplayicinin hesabi | -- | K, n=3 | gaps.values (c1_seed_summary.json) | temiz p=0.0018; PGD fark [11.94, 11.47, 10.84] p=0.00078; AA [8.34, 8.93, 9.11] p=0.00070; kos. yaniltma PGD [-8.155, -6.936, -5.777] p=0.0096; kos. yaniltma AA p=0.00015; her-ikisi-dogru PGD p=0.0010, AA p=0.00080 | turetilmis (_tmp/t22.py) |

### B3. Tablo 2 ve kosullu ayrisma (04:45-66)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E12 | 04:54-55 | Kosullu yaniltma PGD / AA; her-ikisi-dogru saglam PGD / AA | CNN 48.58±0.80, 55.78±0.23, 59.86±0.35, 51.89±0.49; ViT 55.53±0.50, 60.37±0.33, 46.11±0.59, 41.15±0.39 | K, n=3 | c1_seeds/c1_seed_summary.json aggregate | 48.5775±0.7953; 55.7835±0.2303; 59.8643±0.3451; 51.8863±0.4909; 55.5333±0.5040; 60.3734±0.3274; 46.1088±0.5909; 41.1534±0.3917 | uyusuyor |
| E13 | 04:58-59, 04:66 | Onceki tek kosu satirlari (n=7,260): 52.15, 58.16, 54.92, 48.15 (CNN); 52.33, 56.46, 49.61, 45.33 (ViT) | 8 sayi | 1 kosu | yalniz C1_REFERANS_FOYU.md Tablo II alt satir ("Eski tek kosu (sizintili)") | foyde ayni sekilde; c1_*/q1/* altinda JSON yok | (g); (a) |
| E14 | 04:64 | Ayrisma: 85.78 x 0.442 = 37.93; 73.53 x 0.396 = 29.14 | basili carpimlar | K | c1_seed_summary.json aggregate.*.cond_survival_aa | 44.2165 / 39.6266 -> 37.93 / 29.14; yuvarlanmis carpanla 85.78x0.442 = 37.91, 73.53x0.396 = 29.12 | (b) yuvarlanmis carpanla 0.02 fark |
| E15 | 04:64 | Ortak kume n | 7,061±68 | K | c1_seed_summary.json aggregate.both_correct.n_pgd | 7061.33±67.68 [7126, 7067, 6991] | uyusuyor |
| E16 | 04:64 | CNN onde: 13.8 ve 10.7 puan (her-ikisi-dogru PGD, AA) | 13.8; 10.7 | K | c1_seed_summary.json aggregate.gaps.both_correct_pgd / _aa | 13.7555 (SD 0.7643); 10.7330 (SD 0.5249) | uyusuyor |
| E17 | 04:64 | McNemar her-ikisi-dogru altkumede | "p<10^-67 in every run" | S, n=7126/7067/6991 | C1_REFERANS_FOYU.md Tablo II McNemar satirlari (scripts/build_reference_sheet.py uretiyor; c1_* altinda saklanan JSON degil) | PGD: 5.07e-124, 6.89e-113, 1.75e-92; AA: 5.90e-68, 1.43e-77, 1.11e-73; en buyuk 5.90e-68 | (a) yalniz uretilmis .md; (d) mimari iddia |
| E18 | 04:66 | Onceki tek kosu: kos. yaniltma 52.15 vs 52.33 (PGD), 58.16 vs 56.46 (AA) | metin | 1 kosu | FOYU | E13 ile ayni | (g) |
| E19 | 04:66 | Duzeltilmis ViT temiz 80.09±0.60 vs onceki "77.50%" | 77.50 | 1 kosu | c1_eval_summary.json yalniz 80.09±0.60'i veriyor; 77.50 icin c1_*, q1/*, foy ve betiklerde eslesme bulunamadi | -- | (a); (g) |
| E20 | 04:66 | "uc duzeltilmis kosu birbirleriyle onceki kosudan cok daha yakin" | nitel | K | c1_seed_summary.json | kos. yaniltma PGD farklari [-8.16, -6.94, -5.78] (SD 1.19) | -- |

### B4. Transfer protokolleri, Tablo 3, 04:84-127

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E21 | 04:96 | Ham: CNN->ViT, ViT->CNN, Fark | 41.02±0.55; 27.45±0.27; +13.57±0.33 | K, n=3 seed cifti; her biri n=10,000 | c1_transfer/c1_transfer_summary.json protocols.raw | 41.02±0.5467 [40.5, 40.97, 41.59]; 27.4467±0.2715 [27.3, 27.28, 27.76]; fark 13.5733±0.3308 [13.2, 13.69, 13.83] | uyusuyor |
| E22 | 04:97 | Hedef-dogru | 19.87±0.18; 15.51±0.59; +4.36±0.44 | K | protocols.target_correct | 19.8667±0.1848; 15.5067±0.5905; 4.36±0.4355 [4.83, 4.28, 3.97] | uyusuyor |
| E23 | 04:98 | Her-ikisi-dogru | 18.25±0.17; 9.98±0.31; +8.27±0.23 | K | protocols.both_correct | 18.25±0.1652; 9.9833±0.3086; 8.2667±0.2312 [8.51, 8.05, 8.24] | uyusuyor |
| E24 | 04:99 | Basarili-kaynak | 36.39±0.76; 17.02±0.52; +19.37±1.27 | K | protocols.successful_source | 36.39±0.7594; 17.0233±0.5150; 19.3667±1.2682 [20.8, 18.91, 18.39] | uyusuyor |
| E25 | 04:96-99 | Diff.‡ sutunu (onceki tek kosu) | +8.27, +0.63, +5.33, +11.17 | 1 kosu | c1_transfer_summary.json protocols.*.old_run3_diff; FOYU "run3 fark" | 8.27, 0.63, 5.33, 11.17 | (g) |
| E26 | 04:117 | Paydalar | 7,353/8,579; 7,061; 2,831/3,814 | K ortalamasi | protocols.*.n_cond_* | 7352.67/8578.67; 7061.33; 2830.67/3813.67 | uyusuyor |
| E27 | 04:117 | Asimetri araligi, protokol yayilimi, kat orani | +4.36±0.44 ... +19.37±1.27; 15.01±0.84; 4.4 kat | K | c1_transfer_summary.json protocol_spread_pp | mean 15.0067, SD 0.8409 [15.97, 14.63, 14.42]; 19.3667/4.36 = 4.44 | uyusuyor |
| E28 | 04:117 | "Tek protokol icinde tohum SD 1.5 puanin altinda" | <1.5 | K | protocols.*.diff.std | maks 1.2682 (basarili-kaynak) | uyusuyor |
| E29 | 04:117 | Ayristirma: 5.79; 9.21; 3.91; 15.00 (yuvarlanmis toplam) | 5.79; 9.21; 3.91 | turetilmis ortalamalardan | c1_transfer_summary.json protocols.*.diff.mean | 19.3667-13.5733 = 5.7933; 13.5733-4.36 = 9.2133; 8.2667-4.36 = 3.9067 | uyusuyor |
| E30 | 04:117 | Es-protokol "residual": CIFAR-100 5.97; SVHN 0.65 | 5.97; 0.65 | K (C100); n=2 (SVHN) | e1_transfer_summary.json; e7_transfer_summary.json | 10.9233-4.957 = 5.966; SVHN mutlak(-0.35-(-1.005)) = 0.655 | uyusuyor; SVHN: n=2 |
| E31 | 04:117 | CIFAR-100'de ham en buyuk; yayilimin tamami kimlik terimi: 13.58 | 13.58 | K | e1_transfer_summary.json protocols.raw/target_correct diff mean | 18.5333-4.957 = 13.5767 | uyusuyor |
| E32 | 04:117 | Eslesmis fark | 8.27±0.24 (tablodaki 0.23'ten farkli) | S -> K | c1_transfer_summary.json both_correct_paired.diff_pp | 8.27±0.2364 [8.52, 8.05, 8.24] | uyusuyor |
| E33 | 04:117 | Tohum basina eslesmis bootstrap GA | [7.61, 9.44], [7.10, 9.01], [7.28, 9.20] | S, tek kosu, 10,000 yeniden ornekleme | a2_transfer_protocols.json both_correct_paired.paired_bootstrap_ci95_pp (pair1-3) | [7.61, 9.44]; [7.1, 9.01]; [7.28, 9.2] | uyusuyor |
| E34 | 04:117 | "Uclarin ortalamasi [7.33, 9.22] ... kapsama garantisi tasimaz" | [7.33, 9.22] | tanimlayici | c1_transfer_summary.json both_correct_paired.ci_low.mean / ci_high.mean | 7.3300; 9.2167 | (e) metin kendisi "description of three intervals ... no coverage guarantee" diyor |
| E35 | 04:117 | Kosu-arasi t araligi | [7.68, 8.86] | K, df=2 | saklanan JSON'da yok; scripts/verify_manuscript_numbers.py ("T3 kosumlar arasi t alt/ust") hesapliyor; bu toplayici da diff_pp [8.52, 8.05, 8.24]'ten yeniden hesapladi | 7.683, 8.857 | (a) saklanan artefakt yok, yeniden uretilir |
| E36 | 04:117 | Isaret-cevirme permutasyon p "5x10^-5'in altinda, her tohumda" | <5e-5 | S, 20,000 permutasyon | a2 JSON both_correct_paired.signflip_permutation_p (3 cift) | 0.0, 0.0, 0.0 (ham; 1/20001 = 5.0e-5 en kucuk ulasilabilir deger) | saklanan deger tam 0.0 |
| E37 | 04:117 | TOST: ±1,±2,±3 hepsinde p=1.0, esdegerlik kurulamadi | p=1.0 | S | a2 JSON tost_sensitivity.margin_{1,2,3}pp | pair1-3: p 1.0 ve equivalent_at_0.05 false (3 marj x 3 tohum) | uyusuyor |
| E38 | 04:117 | "Onceki kontrol noktalarinda hedef-dogru protokolde ±2'de esdegerlik kabul edilmisti" | nitel | 1 kosu | c1_*/q1/* altinda esdeger kayit yok | -- | (g); (a) |
| E39 | 04:119 | Gevsek okuma: +19.37 -> +14.60; yayilim 15.01 -> 10.45; kayma 4.77 | 14.60; 10.45; 4.77 | K | a2 JSON protocols.successful_source_loose.diff_CNNtoViT_minus_ViTtoCNN (pair1-3); ozet JSON'da yok | fark [16.14, 14.46, 13.19] ort 14.597; yayilim [11.31, 10.18, 9.86] ort 10.45 SD 0.76 (toplayici hesabi); 19.3667-14.597 = 4.77 | (a) toplulastirilmis deger yok, tohum degerlerinden uretildi |
| E40 | 04:119 | "4.77, her protokolun kosu-arasi SD'sinin 3 katindan fazla" | >3 | K | protocols.*.diff.std | 4.77/1.2682 = 3.76 | uyusuyor |
| E41 | 04:121 | MI-FGSM hedef-dogru CNN->ViT, ViT->CNN | 19.07±0.33; 15.42±0.52 | K, n=3 | c1_behavior_summary.json mifgsm | 19.0741±0.3292 [18.72, 19.14, 19.37]; 15.4209±0.5225 [15.03, 15.22, 16.01] | uyusuyor |
| E42 | 04:121 | "Yon, dort protokolde, uc tohumda sabit" | 12/12 pozitif | S->K | c1_transfer_summary.json protocols.*.diff.values | tum 12 deger pozitif (en kucuk 3.97) | uyusuyor |
| E43 | 04:123 | Bilesimsel mekanizma: ViT->CNN yalniz-hedef-dogru altkume yaniltma; her-ikisi-dogru yaniltma | 41.2±0.8; 59.1±1.7; 10.0; 18.3 | K, n=3 | c1_transfer/pair*/a2b_exclusive_subsets.json | ViT->CNN excl 41.23±0.81, both 9.98±0.31; CNN->ViT excl 59.10±1.73, both 18.25±0.17 (toplayici ortalamasi) | uyusuyor; 10.0 ve 18.3'te ± yazilmamis |
| E44 | 04:123 | Altkume boyutlari | 1,517±102; 291±16 | K | a2b_exclusive_subsets.json n_excl_target_only | 1517.33±101.84; 291.33±16.29 | uyusuyor |
| E45 | 04:123 | Gozlemsel kol (18 yon cifti, 6 kume): dort-protokol egimi | -0.528, kume-bootstrap GA [-0.664, -0.418] | Kume (6) | q1/e3_surucu_ayristirma.json A_dort_protokol; e3_iki_kol_fit.json kollar.B | egim -0.5281, GA95 [-0.6640, -0.4181], r -0.4918 | uyusuyor; SVHN dislanmis havuz |
| E46 | 04:123 | Uc-protokol (basarili-kaynak haric) egimi | +0.431, GA [+0.333, +0.633] | Kume (6) | e3_surucu_ayristirma.json B_basarili_kaynak_HARIC | 0.4315, [0.3327, 0.6330], r 0.8402 | uyusuyor |
| E47 | 04:123 | "18 cift icinde 16'da basarili-kaynak en uc"; "23.77 ort acik, 13/18'de en genis" | 16/18; 23.77; 13/18 | 18 yon cifti | e3_surucu_ayristirma.json protokol_uc_olma_sayilari (successful_source max 4, min 12); protokol_cifti_ortalama_aciklik | 4+12 = 16; 23.7741; "13 of 18" icin saklanan sayac yok, e3_asimetri_fit_svhnli.json ciftler'den toplayici sayimi: target_correct-successful_source 13, raw-successful_source 3, raw-target_correct 2 | 16 ve 23.77 uyusuyor; 13/18 (a) saklanmis sayac yok, yeniden uretildi |
| E48 | 04:123 | SVHN-dahil dort-protokol egimi | -0.133, GA [-0.570, +0.469] | Kume (8), 20 cift | q1/e3_asimetri_fit_svhnli.json uydurma | egim -0.1331; egim_GA95_kume_bootstrap [-0.5700, 0.4686]; n_eslesmis_cift 20; n_kume 8 | uyusuyor |
| E49 | 04:123 | SVHN-dahil uc-protokol egimi | +0.470, GA [+0.361, +0.665] | Kume (8) | e3_asimetri_fit_svhnli.json ciftler (asimetri.raw/target_correct/both_correct) | nokta tahmini toplayici hesabiyla 0.4697 (uyusuyor); GA JSON'da yok (toplayicinin bootstrap'i [0.360, 0.682], tohum farki) | (a) GA saklanmamis |
| E50 | 04:123 | SVHN karar tarihi: yeniden atama sonuc goruldukten sonra yazildi | nitel | -- | metin | -- | -- |
| E51 | 04:127 | Kontrollu kol, uc-protokol egimi / dort-protokol egimi | +0.673 [+0.602, +0.727]; +0.273 [+0.219, +0.371] | Kume (8), 116 nokta | q1/e3_iki_kol_fit.json kollar.A | 0.6727 [0.6016, 0.7272]; 0.2729 [0.2189, 0.3712]; n_nokta 116; n_kume 8 | uyusuyor |
| E52 | 04:127 | Yalniz-cift duyarlilik (WRN'siz) dort-protokol | -0.100 [-0.464, +0.092] | Kume (6), 6 nokta | e3_iki_kol_fit.json kollar.B_ana_cift | -0.0999 [-0.4645, 0.0915] | uyusuyor |
| E53 | 04:127 | Erken kontrol noktasi duyarliligi | +0.201 ... +0.492; uc-protokol 0.661-0.673 | Kume (8) | e3_iki_kol_fit.json A_KALDIRAC_DUYARLILIGI | dort-protokol 0.2011 (ep>=2), 0.4832 (ep>=10), 0.4919 (ep>=20); uc-protokol 0.6695, 0.6607, 0.6653 | uyusuyor |
| E54 | 04:127 | Olculmemis x bosluk 7.2 puan | 7.2 | -- | e3_asimetri_fit_svhnli.json ciftler x_temiz_hata_farki (SVHN haric 18 nokta) | en buyuk ardisik aralik 4.11 -> 11.27 = 7.16 (toplayici hesabi) | (a) saklanmis deger yok |
| E55 | 04:125, 04:127 | GA tipi: yuzdelik kume bootstrap, 6-8 kume; "alt sinir olarak okunmali" | metin | Kume | e3_iki_kol_fit.json SERBESTLIK_DERECESI_NOTU | "n=116 / n=18 / n=6 SERBESTLIK DERECESI DEGILDIR" | birim adli (kume) |
| E56 | 04:125 | Kontrollu kol "116 nokta, 8 kume"; gozlemsel "18 cift, 6 kume" | 116/8; 18/6 | -- | e3_iki_kol_fit.json | A n_nokta 116 n_kume 8; B n_nokta 18 n_kume 6 | uyusuyor |

### B5. Kimlik, 3x3 matris, korelasyonlar (04:135-177)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E57 | 04:143 | Temiz-yanlis ornegin saldiri altinda yanlis kalma olasiligi (36 yon) | 0.989-1.000 | 36 yon (2 veri kumesi x 3 tohum x 3 hedef x 2 kaynak) | q1/ozdeslik_kontrol.json ozet | n_yon 36; min 0.989014; max 1.0 | uyusuyor |
| E58 | 04:143 | Kimlik artigi: maks 0.41; ort mutlak 0.095; sapmanin en cok %1.39'u | 0.41; 0.095; 1.39% | 36 yon | ozdeslik_kontrol.json ozet.ARTIK_puan, artigin_sapmaya_orani_yuzde | mutlak_max 0.41; mutlak_ort 0.0947; max 1.388 | uyusuyor |
| E59 | 04:145 | "p'nin kendi duzeltme-oncesi kosularda 0.88'e kadar dustugu" | 0.88 | pre-C1 | c1_*/q1/* ve betiklerde eslesme bulunamadi; metin kendisi "mevcut boru hattinin olcumu degildir" diyor | -- | (g); (a) |
| E60 | 04:145 | Korelasyon r | 0.997 | 6 kosegen-disi yon (3 hedef x 2 kaynak), tohum ortalamalari | c1_c3/c3_summary.json raw_minus_cond_vs_target_error; q1/c3_precision.json | pearson_r 0.99707; egim 0.76248; n_offdiagonal 6; c3_precision: 3 ayrik x degeri (hedef temiz hata 10.52, 14.21, 26.47), Fisher GA [0.9722, 0.9997] ("noktalar bagimsiz degil"), hedef-duzeyi n=3 r=0.9985 ve GA tanimsiz | uyusuyor; GA basilmamis |
| E61 | 04:147 | Egim CIFAR-10 / CIFAR-100 | 0.762; 0.656 | 6 yon (tohum ortalamasi) | c3_summary.json; q1/cifar100/transfer/e1_c3_summary.json | 0.7625; 0.6564 (r 0.9307) | uyusuyor; egim GA'si yok |
| E62 | 04:152-170 | 3x3 matris hucreleri (9 hucre x ham, kosullu; ± ile) | ornek: ResNet->ViT 41.07±0.58 / 19.93±0.20; ViT->ResNet 27.45±0.34 / 15.52±0.64; WRN->WRN 33.03 / 25.16 (± yok) | K, n=3 (WRN sat/sut tek kontrol noktasi) | c1_c3/c3_summary.json | tum 18 hucre foyle ve c3_summary.json ile ayni; WRN->WRN SD 0.00 | uyusuyor |
| E63 | 04:96-99 vs 04:160, 04:162 | Ayni nicelik iki tabloda: CNN->ViT ham 41.02±0.55 / 41.07±0.58; hedef-dogru 19.87±0.18 / 19.93±0.20; ViT->CNN ham 27.45±0.27 / 27.45±0.34; hedef-dogru 15.51±0.59 / 15.52±0.64 | Tablo 3 ve matris | K | c1_transfer_summary.json ve c1_c3/c3_summary.json | farklar 0.00-0.06 puan, SD farklari 0.02-0.07 | (b) farki metin anmiyor; ayri uretim betikleri |
| E64 | 04:172 | Gelen kosullu transfer: ResNet hedef, ViT hedef, WRN hedef | 18.50; 19.04; 10.57 | K ort., 2 yabanci kaynak | c3_summary.json incoming_transfer_vs_own_vulnerability | 18.4983; 19.04; 10.5683 | uyusuyor |
| E65 | 04:172 | Kendi beyaz kutu kosullu yaniltma | 48.52; 55.57; 25.16 | hedef basina | ayni | 48.52; 55.5733; 25.16 | uyusuyor |
| E66 | 04:172; 05_discussion:21 | r = 0.986, uc hedef | 0.986 | n=3 hedef | ayni; q1/c3_precision.json | pearson_r 0.98621 | uyusuyor; metin "suggestive" diyor; Fisher GA n<4 icin tanimsiz |
| E67 | 04:177 (aciklama) | Kosullu asimetri +4.4 | +4.4 | K | c1_transfer_summary.json protocols.target_correct.diff.mean | 4.36 | uyusuyor |

### B6. CIFAR-100 (04:187-212)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E68 | 04:198-199 | Temiz / PGD-10 / AA: ResNet; ViT | 63.86±1.05 / 19.30±0.32 / 15.04±0.54; 43.17±1.10 / 11.15±0.60 / 8.87±0.83 | K, n=3; her biri n=10,000 | q1/e1_cifar100_summary.json mimariler.*.ozet | 63.86±1.053 [64.24, 64.67, 62.67]; 19.3±0.321; 15.04±0.543 [14.75, 14.71, 15.67]; 43.17±1.099 [41.94, 43.5, 44.06]; 11.15±0.596; 8.87±0.834 [8.58, 8.22, 9.81] | uyusuyor |
| E69 | 04:204 | CIFAR-100 asimetri: hedef-dogru, ham, her-ikisi-dogru, basarili-kaynak | +4.96±1.01; +18.53±0.71; +10.92±0.34; +17.50±0.92 | K, n=3 | q1/cifar100/transfer/e1_transfer_summary.json | 4.957±1.013 [4.21, 4.55, 6.11]; 18.533±0.711; 10.923±0.342; 17.5±0.919 | uyusuyor |
| E70 | 04:204 | Protokol yayilimi | 13.83±1.30 | K | e1_transfer_summary.json protocol_spread_pp | 13.8267±1.2970 [15.01, 14.03, 12.44] | uyusuyor |
| E71 | 04:204 | "12 olcumun hepsi pozitif" | 12/12 | -- | protocols.*.diff.values | tum 12 pozitif (en kucuk 4.21) | uyusuyor |
| E72 | 04:204 | Her-ikisi-dogru GA: "ucların ortalamasi" [9.47, 12.35] | [9.47, 12.35] | tanimlayici | e1_transfer_summary.json both_correct_paired.ci_low/ci_high | 9.4733; 12.3533 | (e) metin kendisi "rather than an interval with a coverage guarantee" diyor |
| E73 | 04:204 | Kosu-arasi t araligi | [10.07, 11.77] | K, df=2 | JSON'da yok; toplayici hesabi (diff_pp [11.15, 10.53, 11.09]) | 10.074; 11.773 (verify betigi bu araligi kontrol etmiyor) | (a) |
| E74 | 04:204 | Permutasyon p "20,000 permutasyonun cozunurlugunun altinda her tohumda"; TOST hicbir marjda esdeger degil | -- | S | q1/cifar100/transfer/pair*/a2_transfer_protocols.json | signflip_permutation_p 0.0 (x3); tost p 1.0 (x3 marj x3 tohum) | uyusuyor |
| E75 | 04:206 | Kayitli on-kestirimler: 12/12; 13.83 > 10.45 (kayitli esik); 13.83 < 15.01 | metin | -- | e1 + c1 ozetleri | uyusuyor (13.83, 10.45, 15.01) | -- |
| E76 | 04:206 | CIFAR-100 egim ve r | +0.656; r = 0.931 (6 yon); 0.974 (hedeflere toplu) | 6 yon; 3 hedef | e1_c3_summary.json; q1/c3_precision.json veri_kumeleri.cifar100 | egim 0.6564; r 0.9307; hedef-duzeyi n=3 r 0.9739; Fisher GA (n6) [0.4868, 0.9926]; n3 GA tanimsiz | uyusuyor |
| E77 | 04:206 | Cakisik hedef hatalari | 36.15; 36.36; 0.21 fark | -- | c3_precision.json cifar100.X_AYRIKLIGI | 36.15; 36.36; en_kucuk_ara 0.21; etkin_ayri_x_degeri 2 | uyusuyor |
| E78 | 04:208 | ViT temiz dogruluk bandi kacirildi; PGD/AA bantlari | band 33-40 (olculen 43.17); PGD 10-14 (11.15); AA 8-11 (8.87) | K | e1_cifar100_summary.json; on-kayit q1_research/E1_PILOT_KAPISI.md | 43.17; 11.15; 8.87 | olculen sayilar uyusuyor; bant sinirlari metinde (kayit belgesi bu toplayici tarafindan acilmadi) |
| E79 | 04:208 | Tutma orani: ViT 0.885, ResNet 0.802 | 0.885; 0.802 | K | JSON yok; logs/Q1_cifar100_clean_*.log "Best test accuracy": ResNet 79.25, 79.30, 80.30; ViT 47.45, 48.50, 50.35 | AT temiz / bu kayit ortalamasi: 63.86/79.617 = 0.802; 43.17/48.767 = 0.885. Logdaki "Test Acc" satirlari 0.05 adimli (n=2000, secim kumesi); log basinda "test kullanilmiyor" satiri var | (a); pay test (n=10,000), payda secim-kumesi (n=2000) dogrulugu |
| E80 | 04:210 | Bilesim etkisi (hedef-dogru): -1.249, -1.330, -1.065; asimetrinin %17.4-29.7'si | metin | S, tek kosu basina | q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json protokoller.target_correct.AYRISTIRMA | bilesim_etkisi -1.249, -1.33, -1.065; asimetri 4.211, 4.544, 6.116; mutlak etki/asimetri = 29.7, 29.3, 17.4; JSON'un kendi bilesim_payi_yuzde alani 18.6, 18.5, 12.9 | metin orani mutlak etki/asimetri ile uyusuyor; saklanan alan farkli payda kullaniyor (b) |
| E81 | 04:210 | Bilesim etkisi (basarili-kaynak): +0.527, +0.435, +0.382; %2.1-3.1 | metin | S | ayni | 0.527, 0.435, 0.382; pay 3.1, 2.5, 2.1 | uyusuyor |
| E82 | 04:212 | Secim marjlari: AA 0.22, PGD 0.48 (en yakin tohum kenari) | 0.22; 0.48 | K | e1_cifar100_summary.json tohumlar | AA min 8.22 (bant 8) -> 0.22; PGD min 10.48 (bant 10) -> 0.48 | uyusuyor |
| E83 | 04:212 | CIFAR-100 dokuz hucre secim yayilimi 0.18-1.83 (ort 0.86); CIFAR-10 dokuz hucre 0.54-2.83 (bolme basina) | 0.18-1.83; 0.86; 0.54-2.83 | 3 tohum x 2 mimari x 9 hucre | q1/b8_secim_bandi.json veri_kumeleri.cifar100/cifar10 | yayilim_araligi [0.18, 1.83], yayilim_ort 0.8583; cifar10 [0.54, 2.83], ort 1.7542 (V_B ve V_C ayri) | uyusuyor |

### B7. SVHN (04:217-244)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| E84 | 04:220 | Temiz: ResNet, ViT; fark | 94.27±0.70; 92.42±0.56; 1.85 | K, n=2 | q1/e7_svhn_summary.json ozet | 94.27 sd 0.70 [94.76, 93.77]; 92.42 sd 0.559 [92.82, 92.03]; fark 1.85 | (f) |
| E85 | 04:220 | PGD-10: ResNet, ViT | 55.52±0.64; 52.30±0.10 | K, n=2; test n=26,032 | e7_svhn_summary.json | 55.52 sd 0.643 [55.98, 55.07]; 52.30 sd 0.099 [52.37, 52.23] | (f) |
| E86 | 04:224-235 | Tablo 4 CNN->ViT, ViT->CNN, Fark (± yalniz Fark sutununda) | ham 31.89, 31.49, +0.39±0.08; hedef-dogru 26.32, 27.33, -1.00±0.22; her-ikisi-dogru 25.36, 25.70, -0.35±0.01; basarili-kaynak 61.38, 58.69, +2.70±0.40 | K, n=2 cift | q1/svhn/transfer/e7_transfer_summary.json | farklar: 0.39 sd 0.085 [0.33, 0.45]; -1.005 sd 0.219 [-1.16, -0.85]; -0.35 sd 0.014 [-0.34, -0.36]; 2.695 sd 0.403 [2.98, 2.41] | (f); uyusuyor |
| E87 | 04:224 | Tam test n | 26,032 | -- | e7_svhn_summary.json test_n | 26032 | uyusuyor |
| E88 | 04:240 | Her-ikisi-dogru fark; permutasyon p | -0.35; p = 0.105 | S, tek kosu basina | q1/svhn/transfer/pair*/a2_transfer_protocols.json | pair1 p 0.1047, pair2 p 0.09725; e7_transfer_summary.json perm_p_max 0.1047 | basili 0.105 iki p'nin buyugu (maks) |
| E89 | 04:240 | TOST, ±1'de p=0.0007, esdeger kabul | 0.0007 | S | a2 JSON tost_sensitivity.margin_1pp | pair1 0.000749; pair2 0.00109 (ikisi de esdeger) | basili deger iki tohumdan kucuk olani (pair1) |
| E90 | 04:240 | Eslesmis GA "[-0.76, +0.07]" iki tohumun uclarinin ortalamasi; kosu-arasi aralik yok | [-0.76, +0.07] | tanimlayici, n=2 | e7_transfer_summary.json both_correct_paired.ci_low/ci_high | ci_low -0.755 [-0.75, -0.76]; ci_high 0.065 [0.07, 0.06] | (e), (f); metin kendisi belirtiyor |
| E91 | 04:240 | "iki kosunun yakin uyumu: -0.34 ve -0.36" | -0.34; -0.36 | n=2 | e7_transfer_summary.json both_correct_paired.diff_pp.values | -0.34, -0.36; (turetilmis: n=2 t araligi df=1: [-0.477, -0.223]; kosu-duzeyi eslesmis t p=0.018) | metin "kosu-arasi SD bilgi tasimaz" diyor |
| E92 | 04:240 | Ham farkin isareti: ham +0.39 ve hedef-dogru -1.00 (kimlikle) | +0.39; -1.00 | n=2 | e7 ozeti | ham degerleri [0.33, 0.45] ikisi pozitif; hedef-dogru [-1.16, -0.85] ikisi negatif | uyusuyor |
| E93 | 04:242 | Protokol yayilimi SVHN / C10 / C100 | 3.70±0.62; 15.01±0.84; 13.83±1.30 | n=2; 3; 3 | e7_transfer_summary.json protocol_spread_pp | 3.7 sd 0.6223 [4.14, 3.26] | (f) SVHN |
| E94 | 04:242 | Temiz acik farklari | 1.85; ~12; ~21 | -- | e7; c1_seed_summary; e1 | 1.85; 12.26; 20.69 | uyusuyor |

### B8. L2 tehdit modeli (04:249-271)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| L01 | 04:263-264 | PGD-L2; AA-L2; temiz (tam), temiz (5k) | ResNet 63.78±0.38, 60.61±0.42, 85.78, 85.33; ViT 51.72±0.23, 49.85±0.20, 73.53, 73.61 | K, n=3; PGD n=10,000, AA n=5,000 | q1/cifar10_l2/e6_aa_l2_summary.json | pgd_l2 63.78 sd 0.382, 51.72 sd 0.234; aa_l2 60.61 sd 0.424, 49.85 sd 0.204; temiz_5000 85.33, 73.61 | uyusuyor |
| L02 | 04:269 | L2 asimetri: ham, hedef-dogru, her-ikisi-dogru, basarili-kaynak | +13.03±0.81; +2.12±0.18; +4.07±0.36; +12.06±0.23 | K, n=3 | q1/cifar10_l2/transfer/e6_l2_transfer_summary.json; e6_onkestirim.json O3_isaret | 13.027±0.810 [12.22, 13.02, 13.84]; 2.12±0.182; 4.067±0.358; 12.057±0.232 | uyusuyor |
| L03 | 04:269 | Protokol yayilimi L2 | 10.92 | K | e6_l2_transfer_summary.json protocol_spread_pp | 10.9167±0.8173 [10.02, 11.11, 11.62] | uyusuyor |
| L04 | 04:269 | "12 olcumun hepsi pozitif" | 12/12 | -- | e6_onkestirim.json O3_isaret.pozitif_olcum | "12/12" | uyusuyor |
| L05 | 04:269, 04:271 | Egim L2 (18 yon) | +0.914 | 18 yon (7 ayri hedef-hata degeri; 6 yon ayni WRN hatasi 10.52) | q1/cifar10_l2/e6_onkestirim.json O1_yon | egim 0.91377; r 0.99910; hedef_hatasi_araligi [10.52, 26.99]; GA yok; yonler 3 tohum cifti ve ayni WRN kontrol noktasi uzerinden bagimsiz degil | GA yok; birim (kume/tohum) adli degil |
| L06 | 04:269 | McNemar AA-L2 "her tohum cifti" p<10^-57 ("under both attacks") | p<10^-57 | S, n=5,000 altkume | q1/cifar10_l2/aa_pair{1,2,3}/autoattack_summary.json mcnemar_robust | p 5.35e-59 (766/249), 2.73e-58 (800/272), 6.25e-62 (872/302) | uyusuyor (maks 2.73e-58 < 1e-57); (d) |
| L07 | 04:269 | McNemar PGD-L2 (ayni cumle) | p<10^-57 | S, n=10,000 | q1/cifar10_l2/ altinda McNemar JSON yok (grep: yalniz aa_pair* dosyalari); toplayici per-sample npz'den (robust_correct) yeniden hesapladi | 9.8e-166 (1747/487), 5.1e-134 (1714/564), 1.5e-139 (1807/600) | (a) saklanan deger yok, yeniden uretilir; (d) |
| L08 | 04:269-271 | "Koşullu oranlar L2 altinda ~2-9%, L-inf altinda 9-22%" | 2-9; 9-22 | K | L-inf: c3_summary.json kosegen-disi hedef-dogru oranlari | L-inf kosullu 8.65-21.48 ("9 to 22" ile uyusuyor); L2 kosullu araligi icin L2 uc yonlu matris artefakti bu toplayici tarafindan acilmadi (L2 hedef-dogru CNN->ViT 8.69, ViT->CNN 6.57) | L2 araligi dogrulanmadi |
| L09 | (L2 TOST, metinde yok) | L2 her-ikisi-dogru TOST ±3 marji | metinde yer almiyor | S | a2 JSON (q1/cifar10_l2/transfer/pair*) | ±3'te p 0.998, 0.982, 1.0; hicbiri esdeger degil | olgu |

### B9. Gradyan (04:276-305)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| G01 | 04:291-293 | Hoyer / Gini / %1-alti kesir: ResNet; ViT | 0.4928±0.0120 / 0.6498±0.0089 / 34.8%±2.1; 0.4561±0.0055 / 0.6099±0.0051 / 26.8%±0.9 | K, n=3; her kosu n=500 | results/c1_behavior_summary.json gradient | 0.49284±0.011972; 0.64980±0.008925; 0.34774±0.020972; ViT 0.45614±0.005547; 0.60989±0.005135; 0.26820±0.009033 | uyusuyor |
| G02 | 04:294 | Hizalanma (mutlak): ResNet; ViT | 0.0378±0.0009; 0.0562±0.0004 | K | c1_behavior_summary.json | 0.037815±0.000942; 0.056224±0.000433 | uyusuyor |
| G03 | 04:295 | Hizalanma (isaretli): ResNet 0.0014; ViT 0.0005 | 0.0014; 0.0005 (tablo basligi: 3 kosu ortalamasi±SD) | tek kosu degeri | c1_a3/pair{1,2,3}/a3_gradient_paired.json alignment.*.all_pairs_signed_mean | pair1 0.0014/0.0005; pair2 0.0008/0.0004; pair3 0.0008/0.0004 (ortalama ResNet ~0.0010, ViT ~0.0004) | (b) basili degerler tohum 1 degeri (en buyuk degerle de ayni); foyde "en buyuk 0.0014" |
| G04 | 04:291-294 | "ViT (native)" sutunu: 0.405 / 0.571 / 17.9% / 0.079 | tek kontrol noktasi | n=500, SD yok | c1_gradient/pair1/gradient_statistics.csv ViT_CIFAR_Native_AT | 0.40459; 0.57123; 0.17850; 0.07941 | uyusuyor; (g)'ye benzer: sabit-bolme oncesi kontrol noktasi, testte secilmis |
| G05 | 04:279, 04:303 | Per-sample Wilcoxon, Holm-duzeltmeli, "her kosuda p<10^-11; paired Cohen d 0.32-1.23" | p<1e-11; d 0.32-1.23 | S, n=500 (rel icin n_effective 498-500), kosu basina | c1_a3/pair*/a3_gradient_paired.json paired_sparsity_ResNet_vs_ViT | Holm p: pair1 1.5e-21 / 1.17e-44 / 1.08e-29; pair2 7.06e-47 / 2.61e-70 / 7.63e-54; pair3 2.22e-12 / 2.65e-34 / 3.25e-21 (maks 2.22e-12); d 0.321-1.227 | uyusuyor; (d) mimari iddia |
| G06 | 04:303 | Kosu-duzeyi ham p: Gini 0.036, %1-alti 0.042, Hoyer 0.067 | 0.036; 0.042; 0.067 | K, df=2 (uc kosu farki, tek-ornekli t) | JSON'da yok; verify_manuscript_numbers.py hesapliyor; toplayici c1_behavior_summary.json diff_R_minus_V.values'tan yeniden hesapladi | 0.03594; 0.04205; 0.06740 | (a) saklanan artefakt yok, yeniden uretilir; (c) 04:303'te test adi yok (testin adi Tablo 6 aciklamasinda, "one-sample t-test") |
| G07 | 04:303 | Holm uc olcude | 0.108 | K | ayni | 0.10783 | (a) yeniden uretilir |
| G08 | 04:303 | Hizalanma farki kosu-duzeyi p | 0.0009 | K, df=2 | ayni (diff_R_minus_V.gradient_alignment.values) | -0.01806, -0.01947, -0.01770; p 0.000859 | duzeltme yok, hangi ailenin parcasi oldugu adli degil; (a) yeniden uretilir |
| G09 | 04:303 | "SD kadar bosluktan en az 3 kat kucuk" | >=3 | K | c1_behavior_summary.json diff / SD | Hoyer 0.0367/0.0120 = 3.07 (CNN SD); Gini 4.5; %1-alti 3.8 | uyusuyor |
| G10 | 04:303 | Temiz-egitimli Hoyer 0.380±0.009 vs 0.347±0.002; hizalanma 0.058 vs 0.029 | metin | K, n=3 | c1_behavior_summary.json clean_gradient.per_pair (3 cift); FOYU | ViT 0.3804±0.0094; ResNet 0.3467±0.0018; hizalanma 0.0581 / 0.0293 | uyusuyor |
| G11 | 04:303 | "isaretli ortalama kosinus <=0.0014" | 0.0014 | -- | a3 JSON | maks 0.0014 | uyusuyor |
| G12 | 04:305 | Onceki kontrol noktalariyla siralama ayni; "sekiz durumun altisinda deger tohum SD'sinden fazla kaydi" | 6/8 | 1 onceki kosu | c1_*/q1/* altinda yok (yalniz karantina arsivleri) | -- | (g); (a) |
| G13 | 04:279 | "500x499/2 cift uzerinde ortalama mutlak kosinus" | n_pairs | S | a3 JSON | 124750 | uyusuyor |
| G14 | 04:279 | c1_gradient SD tanimi | -- | -- | c1_gradient/pair1/gradient_summary.json std_semantics | "std across batch means (10 batches of 50)" (kosu icinde; tablodaki ± 3 kosu uzerinden c1_behavior'dan) | olgu |

### B10. Mekansal lokalite (04:313-333)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| S01 | 04:325-328 | Alan %50, alan %90, entropi, Moran I: ResNet; ViT; fark | 0.0378±0.0017 / 0.0397±0.0010 / -0.0019; 0.2345±0.0078 / 0.2570±0.0067 / -0.0224; 5.2014±0.0387 / 5.2524±0.0197 / -0.0509; 0.4141±0.0132 / 0.3941±0.0024 / +0.0200 | K, n=3; kosu basina n=500 | results/c1_c45_summary.json spatial; c1_c5/pair*/c5_spatial.json | tum 12 sayi uyusuyor (ornek: area90 ResNet 0.234538±0.007781, ViT 0.256979±0.006741, fark -0.022441) | uyusuyor |
| S02 | 04:325-328 ("p" sutunu) | Kosu-duzeyi p: 0.54, 0.40, 0.54, 0.47 (tek-ornekli t, Holm, 4 olcu) | 0.54; 0.40; 0.54; 0.47 | K, df=2 | saklanan JSON'da yok; c1_c45_summary.json yalniz p_max (per-sample Wilcoxon en buyugu): 0.2630, 0.0385, 0.7997, 0.5353. Toplayici, c5_spatial.json paired_diff.*.mean'lerden (uc kosu) yeniden hesapladi | ham p: 0.348, 0.100, 0.268, 0.156; Holm: area90 0.402, Moran 0.467, entropi 0.535, area50 0.535 (basili degerlerle uyusuyor) | (a) saklanan kosu-duzeyi p yok, yeniden uretilir |
| S03 | 04:333 | "dort olcunun hicbiri kosu duzeyinde anlamli degil"; "alan %90, CNN icin iki yuzde puan daha kucuk" | nitel; 0.0224 | K | S02; S01 | uyusuyor | -- |
| S04 | 04:333 | "mekansal siralama iki olcude kosular arasi kararsiz" | 2/4 | K | c5_spatial.json paired_diff.*.mean (3 kosu) | area50 [-0.00214, -0.00438, +0.00092]; entropi [-0.0612, -0.1031, +0.0115] (isaret 3. kosuda doner); area90 uc kosuda negatif; Moran uc kosuda pozitif | uyusuyor |
| S05 | 04:333 | "tek kosu icinde per-sample testler cok daha kucuk p verir" | nitel | S | c5_spatial.json paired_wilcoxon_p | pair1: area50 0.052, area90 4.4e-10, entropi 0.0016, Moran 8.9e-08; pair2 area50 1.2e-4, area90 6.2e-17, entropi 3.7e-06, Moran 0.535; pair3 area50 0.263, area90 0.0385, entropi 0.80, Moran 6.1e-09 | uyusuyor |

### B11. Oznitelik kaymasi, dikkat, geometri (04:359-413)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| F01 | 04:372-383 | Tablo 7: ViT CLS / yama ort. / tum jeton (12 blok) ve ResNet 8 blok kosinus | ornek: blok 11 CLS 0.9604, blok 9 yama 0.9870, tum jeton blok 11 0.9803, layer4.0 0.8777 | kosu ortalamasi (3), n=1000/kosu; tabloda SD yok | c1_c4/pair{1,2,3}/c4_summary.json vit.cos_block_cls / cos_block_token_mean / cos_block_output; resnet.cos | toplayici 3 kosu ortalamasi: CLS [0.9993 ... 0.9604 (blok 11) 0.9663], yama ort. min 0.9870 (blok 9), tum jeton min 0.9803 (blok 11); ResNet [0.9951, 0.9918, 0.9879, 0.9853, 0.9753, 0.9607, 0.8777, 0.9108] | uyusuyor |
| F02 | 04:388 | ResNet layer4.0 | 0.8777±0.0181; norm -13.14±1.89% | K, n=3 | c1_c45_summary.json resnet_drift | cos 0.877725±0.018118; norm -13.1357±1.8912 | uyusuyor |
| F03 | 04:388 | ResNet layer4.1 | 0.9108±0.0060; +5.84±3.53% | K | ayni | 0.910776±0.006038; +5.8415±3.5338 | uyusuyor |
| F04 | 04:388 | ViT norm degisimi blok cikisinda "0.45%'in icinde" | 0.45% | K ort. | c4_summary.json vit.norm_change_pct.blockN (3 kosu ortalamasi) | maks mutlak 0.437% (blok 10); MLP alt-blok cikisinda maks 0.697% | uyusuyor (blok cikisi) |
| F05 | 04:390 | CLS / yama kayma orani (1-cos); MLP alt-blok degerleri | 3.05; 0.9343 (blok 10); 0.9840 (blok 8); 4.12 | K | c1_c45_summary.json vit_drift_minima; c4_summary.json | (1-0.9604)/(1-0.9870) = 3.05; MLP: 0.934257, 0.984024, orani 4.115 | uyusuyor |
| F06 | 04:392; 03:158 ile birlikte | Dikkat entropisi TOST: marj ±0.05 nat; 12 katmanda esdegerlik; en zayif p=0.006 | p=0.006; 12/12 | birim adli degil (n=1000/kosu; kosu mu, ornek mi, havuz mu belirtilmemis) | c1_c4, c1_drift, c1_c45_summary.json, c1_behavior_summary.json icinde TOST/p/marj kaydi yok; betik-tarama da eslesme vermedi | -- | (a); (c) |
| F07 | 04:392 | "katman basina ortalama degisim en cok 0.005 nat; katman ortalamalari ~4.9 nat; kosu SD ayni mertebe" | 0.005; ~4.9 | K ort. | c1_c45_summary.json attention.entropy_delta_mean/_std; c4_summary.json attention.entropy_clean_mean | maks |delta ort.| 0.004527 (katman 10); delta SD 0.0006-0.0088; katman bazli temiz entropi ort. 4.61-5.11 (12 katman ort. 4.80); tek kosu icinde bir katmanda |delta| 0.0147 | uyusuyor; "~4.9" yaklasik |
| F08 | 04:392 | Dikkat yer degistirmesi: katman 1 0.028; son katman 0.084 | 0.028; 0.084 | K | c1_c45_summary.json attention.displacement_mean | 0.027554; 0.084104 (SD 0.0102; 0.0076) | uyusuyor |
| F09 | 04:394 | Devrilen vs devrilmeyen son blok kosinus: ViT 0.9895 vs 0.9877 "istatistiksel olarak ayirt edilemez"; CNN 0.9058 vs 0.9143 | 0.9895; 0.9877; 0.9058; 0.9143 | birim ve test adli degil | c1_c45_summary.json flip_split_last_block, flip_split_resnet_last | ViT [0.98947, 0.00914] vs [0.98771, 0.01076]; ResNet [0.90576, 0.00371] vs [0.91434, 0.00775]; test istatistigi/p yok | (a) test kaydi yok; (c) |
| F10 | 04:413 | Geometri (n=500/kosu, beyaz kutu): ResNet 5-NN 87.3±2.6 -> 51.3±1.8; silhouette 0.196±0.010 -> -0.032±0.004; merkez kaymasi 0.238±0.012; ViT merkez kaymasi 0.083±0.004; silhouette -0.021±0.005; 5-NN 61.1±1.4 -> 48.5±1.4 | metin | K, n=3 | c1_a5/pair{1,2,3}/a5_tsne_quant.json designs.whitebox (toplayici ortalamasi, SD ddof=1) | ResNet 0.8727±0.0261 -> 0.5133±0.0175; sil 0.1957±0.0101 -> -0.0317±0.0038; kayma 0.2383±0.0118; ViT 0.0831±0.0036; sil -0.0207±0.0047; 5-NN 0.6107±0.0142 -> 0.4847±0.0142 | uyusuyor; artefaktin notu: mevcut sekil transfer tasarimiyla cizili |
| F11 | 04:359, 04:363 | Tablo 7 basligi "n=1000 per run" | 1000 | S | c4_summary.json n_samples | 1000 (x3) | uyusuyor |

### B12. TGR (04:421-441)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| T01 | 04:432-434 | TGR / MI-FGSM: beyaz kutu ham; hedef-dogru; her-ikisi-dogru | 51.56±0.80 / 66.43±0.29; 12.70±0.41 / 15.71±0.60; 7.93±0.42 / 10.08±0.30 | K, n=3; n=10,000 | c1_c2/pair{1,2,3}/tgr_summary.json | TGR 51.56±0.80 [51.2, 52.48, 51.0]; MI 66.43±0.29; TGR hedef-dogru 12.70±0.41 [13.18, 12.46, 12.47]; MI 15.71±0.60; TGR her-ikisi 7.93±0.42; MI 10.08±0.30 | uyusuyor |
| T02 | 04:439 | Fark: 14.9; 3.0; 2.2 puan | 14.9; 3.0; 2.2 | K | tgr_summary.json | 66.43-51.56 = 14.87; 3.01 (-3.00 ort. fark, SD 0.97); 2.15 (SD 0.72) | uyusuyor |
| T03 | 04:439 | McNemar her-ikisi-dogru, MI-FGSM lehine "her kosuda" | 6.1e-10; 1.1e-27; 7.0e-34 | S, n=7126/7067/6991 | tgr_summary.json mcnemar_both_correct | 6.067e-10 (71/166); 1.114e-27 (50/225); 7.018e-34 (36/222) | uyusuyor; (d) ("not a seed effect" cumlesi) |
| T04 | 04:439 (turetilmis) | Kosu-duzeyi eslesmis t, TGR eksi MI-FGSM, df=2 | metinde YOK | K, n=3 | tgr_summary.json tgr_minus_mi_* | hedef-dogru [-1.95, -3.20, -3.86] p=0.033; her-ikisi-dogru [-1.33, -2.47, -2.66] p=0.035 (toplayici) | turetilmis |
| T05 | 04:441 | "CNN->ViT asimetrisi mimariden bagimsiz saldirilarin urunu degildir" | nitel | -- | T01-T04 | -- | (d) benzeri: sonuc per-sample McNemar ve 3 tohum tutarliligina dayaniyor |

### B13. Varyans kaynaklari (04:446-459)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| V01 | 04:449 | Saldiri-tohumu: temiz tam sabit; robust SD 0.05 (CNN), 0.00 (ViT); 1,000 ornek | 0.05; 0.00 | 3 saldiri tohumu; 1 kontrol noktasi | c1_statval/statistical_validation.json | robust_std 0.0471 (ddof=0), 0.0; clean_std 0.0 | tek kontrol noktasi; SD ddof=0 |
| V02 | 04:449 | Egitim-kosusu: temiz <=0.55, PGD <=0.50 | 0.55; 0.50 | K, n=3 | c1_eval_summary.json | 0.547 (ViT temiz); 0.495 (CNN PGD, 0.50) | uyusuyor |
| V03 | 04:451, 05_discussion:13 | Protokol etkisi 15.01±0.84; egitim etkisi 0.23-1.27 | 15.01±0.84; 0.23-1.27 | K | c1_transfer_summary.json; q1/variance_ratio.json PAYDA_kosum_etkisi_AYNI_NICELIK | sd_min 0.2312, sd_max 1.2682; tohum bazli yayilim [15.97, 14.63, 14.42] | uyusuyor; "birim" 04:451'de adli (ayni nicelik, mutlak) |
| V04 | 04:451 | "15.01, tohum basina araliklarin ortalamasi; protokol ortalamalari acikligiyla ayni; C100'de 13.83 vs 13.58" | 15.01; 13.83; 13.58 | K | variance_ratio.json PAY_10_45_vs_10_24 | tohum_basina_aciklik_ortalamasi 15.0067 = protokol_ortalamalari_acikligi 15.0067; C100: 13.8267 ve 13.5767 | uyusuyor |
| V05 | 04:453 | Oran GA (chi2, df=2), basarili-kaynak protokolu | [0.8, 9.9], 1'i iceriyor | K, df=2; pay sabit kabul (6.5393) | q1/variance_ratio.json ORAN_GUVEN_ARALIGI_chi2.protokol_bazli.successful_source | oran_95_GA [0.82, 9.9]; GA_birimi_iceriyor_mu true; digerleri: ham [3.15, 37.97], hedef-dogru [2.39, 28.84], her-ikisi-dogru [4.5, 54.33] (basilmamis) | uyusuyor |
| V06 | 04:453 | Oran duyarliligi 5.2-32.6; her-ikisi-dogru 28.3 | 5.2; 32.6; 28.3 | K | variance_ratio.json ORAN_ACIKLIGI; ORAN_TANIMA_DUYARLI | min 5.16; max 32.62; sd_vs_sd both_correct 28.29 | uyusuyor |
| V07 | 04:453 | "Payda iki serbestlik derecesi tasir; bolme varyansi dislandi, oran ust sinirdir" | nitel | -- | variance_ratio.json aciklama; A10 | uyusuyor | -- |
| V08 | 04:455 | On sekiz kombinasyon: ResNet 2.62-2.85, ViT 1.58-2.09 puan (tohum basina) | 2.62-2.85; 1.58-2.09 | 3 tohum, tek yorunge/tohum; test PGD-10 | q1/e2/e2_grid.json konvansiyon_dayanikliligi.edge | yayilim_araligi [2.62, 2.85] ve [1.58, 2.09] | uyusuyor; secim olcusu testteki PGD-10 |
| V09 | 04:455 | Yumusatma: her ResNet kosusunda monoton dusurucu, ViT'de 3 kosunun ikisinde | 3/3; 2/3 | n=3 kosu | e2_grid.json mimariler.*.yumusatma_monoton_mu | resnet18 monoton_sayisi 3/3; vit_tiny 2/3 (2002 false) | uyusuyor |
| V10 | 04:455 | Yumusatmasiz (bolme x patience): tohum SD'nin 1.09 ve 1.42 kati | 1.09; 1.42 | n=3 tohum SD | e2_grid.json mimariler.*.cekirdek_k1.oran | resnet18 1.092; vit_tiny 1.416 | uyusuyor |
| V11 | 04:455 | Referansa gore oran araligi: ResNet 0.67-3.38; ViT 0.63-7.38 | metin | n=3 | e2_grid.json mimariler.*.REFERANS_DUYARLILIGI | oran_min 0.671, oran_max 3.379 (ResNet); 0.631, 7.376 (ViT); ViT'de 18 referansin 3'unde oran <1 | uyusuyor |
| V12 | 04:457 | CIFAR-100 secilen epok acikligi 25; test SD 0.32 | 25; 0.32 | n=3 | e1_cifar100_summary.json SECIM_YOLU_vs_SONUC | en_iyi_epok_acikligi 25; test_pgd10_sd 0.321 | uyusuyor |
| V13 | 04:459 | "Uc tohumlu boru hatti 21.7 GPU saati" | 21.7 | C1 CIFAR-10 uc cift | c1_seeds/c1_seed_summary.json timing.total_hours | 21.68 | uyusuyor |

### B14. Diger (sekil, tartisma, sonuc, tutarlilik)

| ID | Konum | Nicelik | Basili | Birim, n | Artefakt | Saklanan | Isaret |
|---|---|---|---|---|---|---|---|
| O01 | 04:68-75 (Sekil 2) | PGD-10 epsilon taramasi | sekilde, metinde sayi yok | K, n=3 | c1_eval_summary.json resnet18_sweep / vit_tiny_sweep | eps 0.03137: ResNet 44.19±0.59, ViT 32.66±0.18 (Tablo 1 PGD: 44.11±0.50, 32.69±0.22; ayni nicelik iki ayri degerlendirme) | olgu: iki degerlendirme farkli (0.08, 0.03 puan) |
| O02 | 05_discussion:13 | "yeniden baslatma ~0.05; yeniden egitim <=0.55" | 0.05; 0.55 | -- | B06, V02 | uyusuyor | -- |
| O03 | 05_discussion:25 | "Hoyer 0.4928 vs 0.4561, her kosuda tutarli; per-sample p<10^-11, kosu-duzeyi p=0.108" | metin | S ve K, ikisi adli | G05, G06, G07 | uyusuyor | iki birim de verilmis |
| O04 | 05_discussion:21; 04:242 | "temiz acik 12.3 ve 20.7" (tartisma) / "yaklasik 12 ve 21" (04:220, 04:242) | 12.3; 20.7 | -- | seed ozeti; e1 | 12.26; 20.69 | uyusuyor |
| O05 | 06_conclusion:9; 01_introduction:23; main.tex ozet | "+4.4 ila +19.4; yeniden egitim <1.5 puan; 15.01; 9.21; 5.79; 3.91; 12/12" | metin | K | E21-E31 | uyusuyor | -- |
| O06 | 06_conclusion:15; 05_discussion:55 | "uc veri kumesi, tek model cifti" | metin | -- | A01-A03 | SVHN 2 tohum | bkz. A11 |

## C. Isaretli olgular (kriter bazinda dokum)

(a) artefakt bulunamadi ya da yalniz uretilmis .md/betik/hesaplama ile yeniden uretilebildi:
- E13, E18, E25 (onceki tek kosu sayilari, yalniz FOYU'de ya da old_run3_diff alaninda), E17 (her-ikisi-dogru McNemar yalniz FOYU'de), E19 (77.50), E35 ve E73 (kosu-arasi t araliklari), E38 (onceki ±2 esdegerlik kabulu), E39 (gevsek okuma tohum degerleri JSON'da, toplulastirilmis deger yok), E47 (13/18 sayaci), E49 (SVHN-dahil uc-protokol egim GA'si), E54 (7.2 bosluk), E59 (0.88), E79 (0.885/0.802), L07 (PGD-L2 McNemar), G06-G08 (kosu-duzeyi p'ler), G12 (6/8 onceki kosu), S02 (Tablo 6 kosu-duzeyi p'ler), F06 (dikkat TOST), F09 (devrilen/devrilmeyen testi).

(b) artefakt degeri yuvarlama sonrasi metinden farkli ya da metindeki sinir saglanmiyor:
- E06: 04:41 "p<10^-84 (AA)" ve "p<10^-120 (PGD-10)"; en buyuk saklanan degerler 1.231e-84 ve 1.917e-120.
- G03: Tablo 5 "Alignment (signed)" 0.0014 / 0.0005 yalniz tohum 1 degerleri; tohum 2 ve 3: 0.0008 / 0.0004.
- E63: Tablo 3 ve 3x3 matrisin ayni hucreleri 0.00-0.06 puan farkli.
- E14: carpim 85.78x0.442 = 37.91 (metin 37.93), 73.53x0.396 = 29.12 (metin 29.14); saklanan carpanlarla 37.93 ve 29.14.
- E80: saklanan bilesim_payi_yuzde (18.6, 18.5, 12.9) ile metindeki %17.4-29.7 farkli paydalara dayaniyor; mutlak etki/asimetri ile metin uyusuyor.

(c) cikarim birimi adlandirilmamis:
- F06 (dikkat TOST: kosu mu, ornek mi, havuz mu), F09 (devrilen/devrilmeyen "istatistiksel olarak ayirt edilemez"), G06 (04:303'te kosu-duzeyi testin adi yok; Tablo 6 aciklamasinda "one-sample t-test" yazili), L05 ve E60/E61/E76 (egim ve korelasyonlar: 6/18 nokta, tohum ve ortak WRN uzerinden bagimsiz degil; c3_precision.json ve e3_iki_kol_fit.json bunu "serbestlik derecesi degildir" diye yaziyor, 04:145-147'de egimin birimi "targets measured" diye geciyor ama n adli degil).

(d) ornek bazli p, mimari (kosu-duzeyi) iddiayi destekliyor:
- E06 (04:41: "CNN holds an absolute robustness advantage under every attack", McNemar per-sample; kosu-duzeyi test metinde yok; ordering 3/3 ve SD ile destekleniyor; toplayici hesabi E11: kosu-duzeyi p 0.0007-0.0018).
- E17 (04:64: her-ikisi-dogru altkume, "Both factors favor the CNN").
- L06, L07 (04:269: McNemar "CNN-over-ViT ordering under both attacks").
- G05 (04:279: ResNet-ViT farki per-sample Wilcoxon; metin kosu-duzeyini 04:303'te ayri veriyor).
- T03, T05 (04:439-441: TGR/MI-FGSM McNemar "not a seed effect"; kosu-duzeyi eslesmis t toplayici hesabi T04: p 0.033 ve 0.035).
- E36, E37, E88, E89 (permutasyon ve TOST p'leri per-sample; ayni cumlelerde kosu-duzeyi t araligi yalniz CIFAR-10 ve CIFAR-100 icin verilmis; SVHN icin kosu-arasi aralik "mevcut degil" deniyor).
Metnin kendi kurali (03:158): "run level is used wherever the claim is architectural"; metin bu kurali 04:117, 04:204 (t araligi), 04:303 ve Tablo 6 icin uyguluyor.

(e) GA, tohum basina uclarin ortalamasi olarak tarif ediliyor:
- E34: 04:117 [7.33, 9.22] (metin: "a description of three intervals that carries no coverage guarantee of its own").
- E72: 04:204 [9.47, 12.35] ("average of the three per-seed bootstrap endpoints rather than an interval with a coverage guarantee").
- E90: 04:240 [-0.76, +0.07] ("averages the endpoints of two per-seed bootstraps and no across-run interval is available").
Her uc cumlede metin kendisi aciklama ekliyor; artefaktlarda (c1_transfer_summary.json both_correct_paired.ci_low/ci_high, e1_transfer_summary.json, e7_transfer_summary.json) alan adlari "ci_low", "ci_high" olup tohum ortalamasi oldugunu yalniz "mean" alt alani belirtiyor; scripts/_t4_birim.py bu uc-ortalama tanimini ayri dogruluyor.

(f) 2 tohumlu nicelige ± SD verilen yerler (SVHN):
- 04:220: 94.27±0.70, 92.42±0.56, 55.52±0.64, 52.30±0.10 (E84, E85)
- 04:224 aciklama ve 04:232-235: Diff. sutunu ±0.08, ±0.22, ±0.01, ±0.40 (E86)
- 04:242: yayilim 3.70±0.62 (E93)
- 04:240: GA [-0.76, +0.07] iki tohumdan (E90); metin "iki kosu kosu-arasi SD'yi sinirlayamaz" diyor, tablolarda ± yine de basili.
- Artefakt tarafi: e7_svhn_summary.json "sd" alanlari n=2 degerden ddof=1 (ornek 52.37 ve 52.23 -> sd 0.099); e7_transfer_summary.json protocols.*.diff.std ve protocol_spread_pp.std ayni.

(g) C1 oncesi (karantina) kaynakli, "onceki tek kosu" diye etiketli: E13, E18, E19, E25, E38, E59, G12 ve A07; ayrica A06/G04 yerel ViT kontrolu c1_gradient altinda ama sabit-bolme oncesi kontrol noktasi.

## D. Birim matrisi: mimari ya da saldiri iddialari ve kullanilan birim

| Iddia | Konum | Kullanilan istatistik | Birim | Kosu-duzeyi karsiligi metinde var mi |
|---|---|---|---|---|
| CNN mutlak saglamlik ustunlugu | 04:41 | McNemar | S (kosu basina) | yalniz siralama 3/3 ve SD; test yok |
| Kosullu ayrisma CNN lehine | 04:64 | McNemar her-ikisi-dogru | S | yok (± SD var) |
| Protokol asimetrisi isareti (C10) | 04:117 | isaret-cevirme perm. + TOST (S); t araligi (K) | S ve K | var (t [7.68, 8.86]) |
| Ayni (C100) | 04:204 | perm. + TOST (S); t araligi (K) | S ve K | var (t [10.07, 11.77]) |
| SVHN esdegerlik | 04:240 | perm. + TOST | S, n=2 | yok (metin: kosu-arasi aralik yok) |
| L2 siralama | 04:269 | McNemar | S | yok |
| Gradyan seyreklik | 04:303 | Wilcoxon+Holm (S); t + Holm (K) | S ve K | var (0.108) |
| Gradyan hizalanma | 04:303 | t (K) p=0.0009 | K | var (duzeltme yok) |
| Mekansal lokalite | 04:325 | t + Holm (K) | K | var |
| Dikkat entropisi esdegerligi | 04:392 | TOST | adli degil | -- |
| TGR < MI-FGSM | 04:439 | McNemar | S | yok |
| Protokol yayilimi / kosu SD | 04:451 | SD (K), aralik | K | var |

## E. Kapsam notlari

- Acilmayan ya da tamamen dogrulanmayanlar: pre-registration belgeleri (q1_research/E1_PILOT_KAPISI.md, E6_ON_KAYIT.md; bant sinirlari E78, kayitli esik 10.45 E75), L2 uc-yonlu matris artefakti (L08'in L2 araligi), figur dosyalari (Sekil 2-6 degerleri), TR ayna metin.
- Toplayicinin uretti turetilmis degerler (E11, E35, E39, E49, E54, T04, G06-G08, S02, F10, L07, E91) `_tmp/t1.py ... t26.py` icinde; saklanan artefakt degildir ve bu dosyada "turetilmis" ya da "toplayici hesabi" diye isaretlidir.
- verify_manuscript_numbers.py: 158 kontrol, tumu EN ve TR metinde bulundu; betik sayinin metinde gecmesini dogrular, hangi cumlede ve hangi birimle gectigini dogrulamaz; McNemar p sinirlarini, TOST p degerlerini, Tablo 6 p'lerini, dikkat TOST'unu ve kosu-arasi t araliklarini (T3 alt/ust haric) denetlemez.
