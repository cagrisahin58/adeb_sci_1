# Q1 Kapsam Genisletmesi - Derin Arastirma Raporu (tarih: 2026-08-03)

**Kapsam:** 6 arastirma kolu (dergi, literatur, veri kumesi, model cifti, deney tasarimi, codebase) + 2 bagimsiz dogrulama turu. Celiskili noktalarda dogrulama ajanlarinin hukmu esas alinmistir. Bu rapor kendi basina yeterlidir; tum kararlar, sayilar ve kaynaklar icindedir.

---

## 1. Yonetici Ozeti (10 Kesin Karar)

1. **Hedef dergi: Pattern Recognition (Elsevier, Q1, IF ~9.1) birincil; Neural Networks (IF 7.2) ve Neurocomputing (IF ~6+) yedek.** Machine Learning (Springer) listeden cikarildi (artik Q2); TPAMI mevcut olcekle denenmeyecek. Gonderim oncesi IF/ceyrek resmi JCR'den teyit edilecek.
2. **Cerceveleme: "Olcum protokolu (kosullama paydasi) sonucu belirler + temiz-dogruluk karistiricisi" ANA katki; uc negatif sonuc (lokalite, attention entropisi, TGR) "mekanizma hipotezlerinin sinir kosullari" bolumu.** Elsevier hakem kulturu saf negatif-sonuc makalesine soguk.
3. **Yenilik tezi AYAKTA (dogrulama hukmu):** Kosullama paydasini ayni model-veri-saldiri uclusunde sistematik degistiren calisma literaturde YOK. Iki amiral degerlendirme-elestirisi makalesi bile birbirinden farkli ve SABIT tek payda kullaniyor (Zhao TPAMI 2025: all-correct altkumesi; Yu SaTML 2025: FR=Q/P kaynak-kosullu) — bu heterojenlik tezimizin atif verilebilir kanitidir.
4. **Veri kumeleri: CIFAR-100 (zorunlu, eps=8/255) + SVHN (eps=8/255, dusuk-hata capasi; flip kapali, extra-604k yok).** TinyImageNet simdiden kosulmayacak — revizyon kozu. Kume genisletmesi YALNIZ mevcut ResNet-18/ViT-Tiny ciftiyle (dogrulama hukmu: tam capraz carpim ~320 GPU-saat, reddedildi).
5. **Ikinci model cifti: ResNet-50 (CIFAR-stem, 23.5M) vs ViT-Small/16 (timm, 32→224 upsample, 21.7M; oran 1.08x), YALNIZ CIFAR-10.** ViT-S AT'ye uc sigorta: AdamW LR 5e-4, grad clip 1.0, 10 epoch eps-warmup; bs=64. Tek-tohum patch-4 native-32 ablasyonu eklenecek.
6. **Kalibrasyon egrisi (E3) ana katkiya yukseltildi** — "olcum artefaktinin karistiriciyla kontrollu iliskilendirilmesi adversarial-ML'de ilk". ONKOSUL: E0 altyapisi (`save_every` — ara checkpoint su an YOK, yalnizca best/last kaydediliyor).
7. **Sizinti ablasyonu (E2): tek tam-butce egitim → iki secim kurali cevrimdisi uygulanir** (V_A on-egitimde gorulmus / V_B hic gorulmemis; ayni yorunge, kosu-ici varyans sifir). Istatistik cercevesi TOST esdegerlik, marj δ=1.0 puan.
8. **Tohum sayisi: manset CIFAR-10 ana ciftinde 5'e tamamlanacak (+2 tohum), diger tum konfigurasyonlar 3 tohum.** Gerekce: n=3'te sigma %95 GA carpani [0.52; 6.29] → "protokol etkisi tohum varyansinin ~20 kati" iddiasi savunulamaz; n=5'te [0.60; 2.87] → kotumser durumda bile "≥7 kat".
9. **L2 tehdit modeli: YALNIZ CIFAR-10, AutoAttack-L2 eps=0.5, ana cift final modelleri** ("5. protokol ekseni" cercevesi). Veri ajaninin CIFAR-100-L2 kalemi IPTAL (dogrulama hukmu: RobustBench'te CIFAR-100 L2 tablosu yok).
10. **Toplam butce: ~150-185 GPU-saat (+%10-15 tampon → ~170-205), adanmis RTX 5090'da ~9-10 gun, paylasimli GPU'da 2-3 hafta duvar-saati.** Kosu sirasi: E0 → E2 → E1 → E3 → E5(pilot+kalan) → E4 → E6 → E7. Dusurme sirasi: E7 SVHN → E6 L2 → E4 +2 tohum → E5 indirimleri. Scooping riski gercek ("Beyond ASR" bandi 2026'da aktif) — protokol-denetimi + kalibrasyon cekirdegiyle ERKEN arXiv on-baskisi atilacak.

---

## 2. Hedef Dergi Karari

### 2.1 Karar

| Rol | Dergi | IF (dogrulanacak) | Ceyrek | Gerekce |
|---|---|---|---|---|
| **BIRINCIL** | **Pattern Recognition** (Elsevier) | ~9.1 | Q1 | Robustluk-degerlendirme-metodolojisi icin dogrudan emsal: Liu ve ark., "A comprehensive evaluation framework for deep model robustness", PR c.137 (2023) — CIFAR-10+SVHN olceginde kabul edilmis degerlendirme-cercevesi makalesi. CNN-vs-ViT karsilastirmasi cekirdek kapsam. Sure makul (~2.9 ay ilk tur / ~4.9 ay toplam, SciRev). APC zorunlu degil (hibrit; abonelik yolu ucretsiz). |
| **YEDEK 1** | **Neural Networks** (Elsevier) | 7.2 | Q1 | Mekanizma-analizi kulturu (Rect-ViT 2025, attribution-tabanli transfer 2025). Ret halinde cerceveleme agirligi "mimari davranis farklari"na kaydirilir. Bagimsiz sure verisi yok (risk). |
| **YEDEK 2** | **Neurocomputing** (Elsevier) | ~6-6.7 | Q1 | Transfer-saldiri makaleleri duzenli basiyor; en hizli surec (~2.5 ay ilk tur / ~3.9 ay toplam; masaustu ret 9 gun). Kabul olasiligi en yuksek guvenli liman. |

**Kosullu alternatifler:** (i) **TMLR** — kultur olarak en iyi eslesme (negatif sonuc + reproducibility acikca kapsamda, ucretsiz), ama JCR ceyregi YOK → Turkiye docentlik/tesvik kriterine sayilmaz; kurumsal gereklilik netlesmeden secilmez. (ii) **IEEE TIFS** — ancak makale tehdit-modeli/guvenlik diliyle yeniden cercevelenirse. (iii) **TPAMI** — mevcut olcekle (2 veri kumesi, 2 cift) ONERILMEZ; Zhao ve ark. 2025 emsali citayi ImageNet + 23 saldiri x 11 savunma seviyesine koymus durumda. **Machine Learning (Springer): listeden cikarildi (guncel IF 4.9, Q2).**

### 2.2 Kapsam (olcek) esigi

Tipik Q1 esigi: **2-3 veri kumesi + 4-10 model.** Plan (3 veri kumesi: CIFAR-10/100/SVHN; 2 kapasite-eslenmis cift + WRN-28-10 referansi; 3-5 tohum) Pattern Recognition / Neural Networks / Neurocomputing icin **alt sinirda yeterli**; TPAMI/TIFS icin yetersiz. Emsal olcekleri: TPAMI 2025 (ImageNet, 23x11) ust uc; PR 2023 Liu (CIFAR-10+SVHN) alt-orta uc, kabul edilmis; TMLR 2022 Shao (ImageNet+CIFAR, cok aile). **3-5 egitim tohumu cogu emsalin USTUNDE (cogu 1 tohum) — metodolojik ustunluk olarak acikca pazarlanacak.** "32x32-only" elestirisine karsi: TinyImageNet revizyon kozu + limitations'ta olcekleme argumani; mumkunse salt-degerlendirme ucuncu mimari ailesi (Swin/ConvNeXt, timm) 4x4 matris opsiyonu.

### 2.3 Yayin stratejisi notlari

- APC odenmeyecek (hibrit dergilerde abonelik yolu; erisim icin arXiv on-baski — Elsevier politikasi izin veriyor).
- TR Dizin'deki Turkce makale ile ortusme: Ingilizce surum "major extension" esigini (>%50 yeni icerik) gecmeli ve Turkce surum gonderimde BEYAN edilmeli (ozgunluk/etik riski).
- IF/ceyrek degerleri ucuncu-taraf agregatorlerden; TNNLS (13.7?) ve TIFS (9.65?) iddialari guvenilmez bulundu — gonderim oncesi resmi Clarivate JCR kontrolu zorunlu.

---

## 3. Yenilik Konumlandirmasi

### 3.1 En yakin 3 rakip (kunyeler dogrulama turunda birincil kaynaktan teyit edildi)

**Rakip 1 — Zhao ve ark., "Revisiting Transferable Adversarial Images: Systemization, Evaluation, and New Insights" (IEEE TPAMI 2025; arXiv:2310.11850; onculu arXiv:2211.09565, 2022).**
- Ne yapiyor: ImageNet'te **23 saldiri x 11 savunma** (dogrulama duzeltmesi: "9 savunma" 2022 onculune aittir) sistematik yeniden degerlendirme; elestiri eksenleri (i) hiperparametre/bire-bir kiyas adaleti, (ii) gizlilik (stealthiness) olcumu eksikligi.
- Kosullama paydasi: **TEK ve SABIT** — "dort modelin tamaminin dogru sinifladigi 5000 goruntu" (all-correct altkumesi) uzerinde kosulsuz basari orani. Farkli payda secimlerini HIC karsilastirmiyor (tam metinden dogrulandi).
- **Ayrim cumlemiz (metrik duzeyinde kurulacak):** "Zhao ve ark. sabit bir all-correct altkumesi uzerinde saldirilar-arasi kiyasin adaletini inceler; biz sabit saldiri-model-veri uclusunde PAYDANIN KENDISINI degistirip sonucun 3.3 kata kadar oynadigini gosteriyoruz — dikey (ortogonal) eksen." AT'li ciftler, tohum-gurultusu tabani ve temiz-hata karistirici analizi onlarda yok.

**Rakip 2 — Yu, Gu, Li, Torr, "Reliable Evaluation of Adversarial Transferability" (arXiv:2306.08565, 2023; **IEEE SaTML 2025 KONFERANS yayini**, ieeexplore 10992575 — dergi "final surumu" DEGIL; dogrulama duzeltmesi. Camera-ready'de 13 saldiri, arXiv v1'de 12).**
- Ne yapiyor: "Transferabilite abartilmis" tezi; 4 mimari ailesinden 18 model; **uc "protokolu" payda degil HEDEF-MODEL-KAPSAMI eksenli** (P1: 18-model ensemble hedef; P2: kac hedefe transfer sayimi; P3: 18 modelin tamamini yaniltma). Metrik tek ve sabit: **FR = Q/P (kaynak-basarisi kosullu)** — tam metinden dogrulandi.
- **Ayrim:** "Protokol" kelimesini kullandigi icin ALGI riski en yuksek rakip; makalede acik karsilastirma paragrafi SART: onlarin ekseni model kapsami, bizimki olcum paydasi. Kalan tek acik is: SaTML camera-ready tam metninin kurum IEEE erisimiyle son teyidi.

**Rakip 3 — Curl ve ark., "Beyond Attack Success Rate: A Multi-Metric Evaluation of Adversarial Transferability in Medical Imaging Models" (arXiv:2604.16532, 2026 preprint).**
- Ne yapiyor: "ASR tek basina yetersiz" retorigi; CNN'ler vs ViT'ler; medikal veri kumeleri; 3500 konfigurasyon; onerdigi eksen **algisal metrikler** (PSNR/SSIM/L2).
- ASR'i acikca **kosulsuz** kullaniyor (fetch ile dogrulandi); kosullama calismasi, AT, tohum tekrari, temiz-hata karistiricisi YOK. Onemi: "Beyond ASR + CNN-ViT transfer" kelime uzayini isgal ediyor ve 2026'da bu bandin aktiflestiginin kaniti → **scooping riski gercek, takvim hizlandirilmali.**

**Ikincil komsular:** Pinto/Torr/Dokania "Impartial Take to the CNN vs Transformer Robustness Contest" (egitim-tarifi adaleti ekseni); Cinà/Pintor/Biggio AttackBench (arXiv:2404.19460, AAAI 2025) + "Evaluating the Evaluators" (arXiv:2507.03450) — implementasyon/butce ekseni, kosullama yok; Gu ve ark. transferabilite anketi (arXiv:2310.17626) — FR=Q/P'yi kataloglar ama kosullama tutarsizligini sistematize etmez.

### 3.2 Dogrulama ajaninin NET HUKMU

> **Tez ayakta; arastirma ajani halusinasyon yapmamis, karakterizasyonlar buyuk olcude isabetli.** Alanin iki amiral degerlendirme-elestirisi makalesi bile birbirinden FARKLI ve SABIT tek payda kullaniyor (Zhao: all-correct kosulsuz; Yu: kaynak-basarisi kosullu FR=Q/P). Hicbiri kosullamayi degisken yapip ayni uclude etkisini olcmuyor; tohum-gurultusu tabani, temiz-hata karistirici analizi ve asimetri yonunun protokole bagli terslenmesi hicbirinde yok. Yenilik iddiasi, Zhao'ya ve Yu'ya birer ACIK ayrim cumlesi yazilmasi KOSULUYLA savunulabilir.

### 3.3 Konumlandirma araclari (makaleye girecek)

1. **5-eksenli taksonomi paragrafi + tablosu:** saldiri-tarafi adaleti (Zhao TPAMI 2025) / model-kapsami (Yu SaTML 2025) / implementasyon-butcesi (AttackBench, Evaluating the Evaluators) / algisal metrikler (Curl 2026) / **olcum-paydasi kosullamasi (BIZ)**. Ilk ucune acik "bizde farkli olan" cumlesi.
2. **Literatur denetim tablosu (15-20 transfer makalesi):** her makalenin hangi kosullama paydasini kullandigi belgelenir. Iki dogrulanmis cipa satiri hazir: Yu FR=Q/P (kaynak-kosullu) ve Zhao all-correct altkumesi. Cok dusuk maliyet, "alan tutarsiz" iddiasini olculmus olguya cevirir — **oncelikli is.**
3. **"Muhasebe ozdesligi" itirazinin onlenmesi:** ham−kosullu farkin temiz-hatayla r=0.997 iliskisinin kismen aritmetik beklenti oldugunu BIZ soyleyecegiz; katki uc ayakta kurulacak: (i) buyuklugun tohum-gurultusunun ~20 kati olmasi, (ii) asimetri YONUNUN protokole bagli degismesi, (iii) kalibrasyon deneyiyle (E3) kontrollu/nedensel dogrulama.
4. **Ust-cerceve atiflari:** Benchmark Lottery (arXiv:2107.07002); ASRD analogu (NLP backdoor, arXiv:2404.11538 baglami); GRN ranking-instability (arXiv:2603.03493 — alan-disi birebir yontemsel analog; DIKKAT: tek yazarli hakemsiz preprint, tasiyici kanit olarak KULLANILMAZ, yalnizca analog atif). Metodoloji seceresi: Carlini 2019 (arXiv:1902.06705), Tramèr 2020 (arXiv:2002.08347), AutoAttack (arXiv:2003.01690), RobustBench (arXiv:2010.09670), Lorenz 2022 (arXiv:2112.01601), Pintor 2022 (arXiv:2106.09947).
5. **TGR-negatif bulgusu sinirlamasi:** TESSER (arXiv:2505.19613) veya baska bir 2025 ViT-ozgu saldiri deney matrisine eklenir YA DA iddia acikca "AT'li dusuk-cozunurluk rejimi" olarak sinirlanir — aksi halde hakem itirazi kacinilmaz. (Butce onceligi dusuk; asgari cozum acik sinirlamadir.)
6. **Eklenmesi gereken diger atiflar:** ACM CSUR 2025 ViT-robustness anketi (10.1145/3729167), "Defense That Attacks" (arXiv:2512.02830 — AT'li kaynaklarin transfer davranisi, en yakin tematik komsu), Waseda ve ark. WACV 2023, Electronics 2024 (13:2534), SaTML 2025 "Reliable Evaluation of Adversarial Transferability"; ViT AT tarif kaynaklari: Debenedetti SaTML 2023, Mo ve ark. NeurIPS 2022.

---

## 4. Veri Kumesi Karari

### 4.1 Karar: CIFAR-100 (zorunlu) + SVHN (stratejik capa); TinyImageNet revizyon kozu

**Kapsam kilidi (dogrulama hukmu):** Kume genisletmesi YALNIZ mevcut ResNet-18/ViT-Tiny ciftiyle yapilir; yeni cift (R50/ViT-S) yalniz CIFAR-10'da kalir. Tam capraz carpim (3 kume x 2 cift x 3 tohum ≈ 320 GPU-saat) REDDEDILDI.

| Kume | Karar | Eps konvansiyonu | Gerekce |
|---|---|---|---|
| **CIFAR-100** | ZORUNLU | **Linf 8/255** (RobustBench standardi; L2 tablosu YOK → L2 kalemi iptal) | Boru hattiyla birebir ayni (32x32, 50k; tek degisiklik num_classes=100). AT-temiz hata %40-55 bandi → kalibrasyon egrisinin x-eksenini yukari genisletir. RobustBench Linf tablosu + zoo referans modeli mevcut → 3x3 matris birebir cogaltilabilir. AT literaturunde fiili standart 2. benchmark. |
| **SVHN** | EVET (dusuk-hata capasi; ilk dusecek kalem) | **Linf 8/255 ana** + 4/255 eps-supurme noktasi (mevcut supurme sablonuna dahil) | Hedef temiz hata %5-10 → kalibrasyon egrisinin dusuk-hata ucu; "protokol yayilimi temiz hatayla olcekleniyor" tezini SVHN(~%5-10) → CIFAR-10(~%18-26) → CIFAR-100(~%44-50) uclu bandinda ongorulu yasaya cevirir. AWP/HAT sayilariyla dis kalibrasyon (HAT RN18 SVHN 8/255: 93.08 temiz / ~52.8 robust). Uygulama notlari: `split='train'` (73,257 ornek), **extra-604k KULLANILMAZ**, **RandomHorizontalFlip KAPALI** (rakamlar), 8/255 AT kararsizligina karsi **eps-warmup + dusuk LR** (dogrulama hukmu: LR-warmup tek basina yetersiz, eps-warmup SVHN'e de uygulanacak). |
| TinyImageNet-200 | SIMDIDEN KOSULMAZ | 8/255 yaygin | ~50 GPU-saat, torchvision'da yok (manuel kurulum + ImageFolder), CNN 64x64 stem karari gerekir. Makalede gelecek-is; hakem isterse major-revizyon kozu. |
| Imagenette / IN-100 | ELENDI | — | 9,469 egitim ornegi AT icin cok kucuk; sinif alt-kumesi standardize degil, karsilastirilabilirlik zayif. |
| GTSRB | ELENDI | — | Sinif dengesiz, degisken boyut, Linf-AT ana akiminda degil. |
| Fashion-MNIST | ELENDI | — | Gri 28x28, pretrained-ViT uyumsuz, bilimsel deger dusuk. |

### 4.2 Referans modeller ve kalibrasyon capalari

- **CIFAR-100 3x3 matris referansi: `Pang2022Robustness_WRN28_10`** (63.66 temiz / 31.08 AA; RobustBench zoo'dan `load_model(..., dataset='cifar100')`). **Dogrulama hukmu:** Cui2023Decoupled DEGIL (50M sentetik veri — asiri farkli rejim); Pang2022 1M sentetik kullanir, mevcut CIFAR-10 referansimiz Gowal2020_extra da ek-verili oldugundan yapisal olarak tutarli. **Matrise "ek veri" sutunu eklenecek** (Gowal/Pang: ek-verili; Rice2020: ek-verisiz — etiketli).
- **Kendi CIFAR-100 sonuclarimizin capasi: Rice2020Overfitting** (PreActRN-18, ek verisiz: 53.83 temiz / 18.95 AA) — ek-verisiz PGD-AT RN18 beklentisi temiz ~%53-56, AA ~%18-21. ViT ust-sinir capasi: Debenedetti XCiT-S12 67.34/32.19 (DIKKAT: XCiT saf ViT degil, cross-covariance attention — kayitla kullanilacak). ViT-Tiny CIFAR-100 AT beklentisi: temiz ~%50-60, AA ~%15-20 (dogrudan literatur capasi yok, ilk kosudan sonra guncellenecek).
- **SVHN referansi (RobustBench zoo YOK):** **once DenseNet-121 kendi tarifimizle (~5-6 GPU-saat)** denenir (dogrulama hukmu); WRN-28-10 self-AT ancak 20-27 GPU-saat ek maliyet acikca kabul edilirse. Aksi halde SVHN matrisi 2x2 kalir.
- **Onemli ongoru (kayit altina alinacak):** CIFAR-100'de ImageNet on-egitimi ViT'e orantisiz yarar sagladigindan temiz-dogruluk farkinin ISARETI CIFAR-10'a gore tersine donebilir — kalibrasyon egrisi icin isaret cesitliligi bonusu; metinde dikkatli cerceve ister.

### 4.3 Maliyet (dogrulama-duzeltmeli)

Veri ajaninin "35-40 GPU-saat" tahmini kendi sart kostugu SVHN referans egitimini DISLADIGINDAN 1.4-2x eksikti. Gercekci: CIFAR-100 tam pipeline ~22-24 sa; SVHN tam pipeline ~28-30 sa + referans (DenseNet-121 ~5-6 sa). Butce tablosu Bolum 7'de.

---

## 5. Model Cifti Karari

### 5.1 Karar: ResNet-50 vs ViT-Small/16 — YALNIZ CIFAR-10

| Ozellik | ResNet-50 | ViT-Small/16 |
|---|---|---|
| Kaynak | torchvision resnet50, **CIFAR-stem** (3x3 s1 conv1, maxpool=Identity) — kodda kayitli: `src/models/resnet.py:114-151` (`CIFAR10ResNet50`) | timm `vit_small_patch16_224` (AugReg ailesi — ViT-Tiny ile ayni aile), **model ici 32→224 bilinear upsample** — kodda kayitli: `src/models/vit.py:406-438` (`CIFAR10ViTSmall`) |
| Parametre (10 sinif) | 23.53M | 21.67M — **oran 1.08x** (mevcut ciftin 1.96x'ine karsi gercek "eslenmis" iddiasi) |
| Literatur capasi (CIFAR-10 Linf 8/255) | Engstrom2019 (RobustBench): 87.03 temiz / 49.25 AA (scratch-AT); Debenedetti baseline: 84.80 / 41.56 | Mo ve ark. NeurIPS 2022 ViT-S: **vanilla AT AA 46.37 (temiz 79.59) ESAS referans**; 47.33 ARD+PRM'li (dogrulama duzeltmesi — makalede ikisi birlikte verilecek, SGD+ImageNet-pretrain protokol farki acik yazilacak) |
| L2 referansi | Madry robustness lib, CIFAR-10 L2 eps=0.5: 90.83 / 69.24 AA (E6 icin hazir) | — |

**Elenen alternatifler:** ResNet-34/ViT-S (sayisal eslesme daha iyi ama CIFAR AT literaturunde RN34 baseline'i yok — yalniz butce-daraltma yedegi, −18 sa); WRN-28-10/ViT-S (1.68x, "eslenmis" savunulamaz; WRN referans rolunde kalir); ConvNeXt-T/Swin-T (CIFAR olceginde Linf-AT baseline'i yok, 32x32 icin mimari cerrahi, Swin'in yerel penceresi global-attention karsilastirmasini bulanikligiyor → "future work" cumlesi).

**Acik beyan (makaleye):** Cift **parametre-eslesmis, FLOPs-eslesmis DEGIL** (ViT-S@224 ~4.6 GFLOPs vs R50@32 ~1.3 GFLOPs, ~3.5x). Patch-4 native ablasyonu bu itirazi kismen kapatir.

### 5.2 Cozunurluk protokolu karari

Ana ciftte **32→224 model ici upsample KORUNUR** (ViT-Tiny ile birebir ayni pipeline; saldiri 32x32 piksel uzayinda → eps yarıcapi iki mimaride ayni, Shao 2021 itirazi bizi vurmuyor). Ek olarak **patch-4 native-32 ViT-S tek-tohum ablasyonu** (Mo tarifi: SGD 0.1 → /10 @36,38, clip 1.0, 40 epoch; sinif kodda hazir `src/models/vit.py:26-144`) — hem FLOPs itirazina yanit hem "adaptasyon protokolu de bir olcum-protokolu eksenidir" cercevesiyle ana teze dogrudan hizmet (ayni agirliklar, iki adaptasyon protokolu, farkli sayilar).

### 5.3 Tam hiperparametre tablolari

**ResNet-50 (mevcut ResNet-18 protokolunun birebir kopyasi):**

| Asama | Ayar |
|---|---|
| Mimari | torchvision resnet50; CIFAR-stem (3x3 s1, maxpool kaldir); fc→10 |
| Temiz egitim | SGD momentum 0.9, LR 0.1, cosine, wd 5e-4, bs 128, 200 epoch, RandomCrop(32,4)+flip |
| AT finetune | PGD-10, eps=8/255, alpha=2/255; SGD **LR 0.001** (proje dersi: 0.01 bile katastrofik), bs 128, 100 epoch butce + patience 20 |
| Beklenti | temiz 83-86 / PGD ~43-48 / AA ~38-44 |

**ViT-Small (mevcut ViT-Tiny protokolu + 3 sigorta; dogrulama-onayli):**

| Asama | Ayar |
|---|---|
| Agirlik | timm `vit_small_patch16_224` ImageNet pretrained (AugReg), model ici 32→224 upsample |
| Temiz finetune | Mevcut ViT-Tiny temiz tarifi (AdamW dusuk LR); ~30 epoch yeter |
| AT finetune | AdamW **LR 5e-4** (ilk 5 epoch adv-acc <%15 ise 2.5e-4'e dus), wd 0.05, **grad clip L2 max_norm 1.0** (su an 10.0 = fiilen devre disi; `src/training/adversarial_trainer.py:215`), cosine + 5 epoch LR warmup, **10 epoch lineer eps-warmup (0→8/255)**, PGD-10 alpha=2/255, **bs 64** (32GB'de fp32 tepe ~12-16GB; bs 128 fp32 ~24-30GB RISKLI — cikilmaz), 60 epoch butce + patience 20; aug yalniz crop+flip (**MixUp/CutMix/RandAugment YOK** — Debenedetti bulgusu) |
| Izleme | Ilk 5 epoch adv-acc esigi; loss duzlesmesi (attention cokmesi belirtisi) loglanir |
| Beklenti | temiz ~76-80 / PGD ~38-42 / AA ~35-40 (bizim finetune-AT rejimimizde; Mo'nun native-32 SGD tarifi vanilla 46.37 — fark protokol anlatisina girer) |
| Makale beyani | "Finetune-AT protokolumuz scratch-AT literatur sayilarinin (Engstrom 87.03/49.25; Mo 46.37) altindadir ve BILINCLI bir protokol secimidir" cumlesi acikca yazilir |
| Tarif disiplini | Debenedetti (TRADES+wd 0.5+native-32) ile Mo (SGD+native-32) tariflerinden parca alinip karistirilmaz — tablo disina cikilmaz (test edilmemis kombinasyon riski) |

### 5.4 Tahmini sureler (olculmus C1 capalarindan olceklenmis; dogrulama-duzeltmeli)

Olculen capalar (RTX 5090, C1 loglari): RN18 clean 28.5 dk/tohum; ViT-T clean 64.3 dk; RN18 AT 85.6 dk; ViT-T AT 131.8 dk; AA Linf n=10k cift basina 2.75-3.05 sa. Olcekleme: R50@32 ~2.3x RN18; ViT-S@224 ~3.7x ViT-T.

| Is | Tahmin |
|---|---|
| ViT-S temiz finetune, 3 tohum | **~12 sa** (dogrulama: model ajaninin butcesinde acikca yoktu — eklendi) |
| ViT-S AT @224, 3 tohum | ~24 sa (7-13 sa/kosu, early stop'a bagli) |
| R50 temiz + AT, 3 tohum | ~3.5 + ~10 sa |
| AutoAttack n=10k, 3 tohum x 2 model | ~13-18 sa (gece kuyrugu; bs=100 ViT-S'te bellek-guvenli ~6-8GB) |
| Patch-4 native ablasyon (1 tohum) | ~4-6 sa |
| Analizler (transfer/gradyan) | ~4-8 sa |
| **E5 TOPLAM** | **~70-85 GPU-saat** (±%40 belirsizlik → **ONCE 1 tohum pilot** zorunlu) |

---

## 6. Deney Tasarimi

Depodan dogrulanan kisitlar: (i) **ara checkpoint YOK** — `src/training/adversarial_trainer.py` yalnizca best.pth+last.pth kaydediyor (`models/c1/` envanteri teyitli) → kalibrasyon egrisinin "kayitli checkpoint = bedava" varsayimi GECERSIZ, E0 on kosul; (ii) clean `Trainer`'da early stopping/resume/TRAINING_COMPLETE yok; (iii) mevcut istatistik zaaflari: gelen-transfer r=0.986 yalnizca 3 hedef (Fisher-z GA tanimsiz), 3x3 r=0.997 GA'si genis [0.972; 0.9997], n=3 sigma GA carpani [0.52; 6.29].

### E0. Altyapi (GPU ~0; ~1 gun kod) — ON KOSUL, hicbir egitim bundan once baslamaz
- `adversarial_trainer.py`'a `save_every N` (yalniz agirlik, optimizersiz, fp32; boyutlar R18 45MB / ViT-T 23MB / R50 94MB / ViT-S 87MB; her-epoch kayitla E1+E2 ~25-30GB disk, 2-epoch'ta-bir ile yariya iner).
- Kaynak modellerin PGD-10 cekismeli orneklerini diske yaz (10k: fp32 123MB veya uint8 31MB) → hedef-checkpoint degerlendirmesi salt ileri-gecis.
- Cevrimdisi secim araci: kayitli checkpoint dizisine "best-by-adv-val + patience-20 simulasyonu"nu istenen dogrulama bolmesiyle sonradan uygular (E2'nin anahtari; C1'in patience-20 kuralini birebir taklit etmeli).

### E1. CIFAR-100 ana cift (RN18/ViT-T), 3 tohum — ~24 GPU-saat
- **Kosular:** 2 mimari x 3 tohum, C1 recetesi klonu, `save_every` ACIK; 4-protokol PGD + AA n=10k + gradyan analizi. Toplam 6 egitim + 3 AA.
- **Istatistik:** C1 foyuyle ayni uretim. **Kayitli on-kestirim (confirmatory):** protokol yayilimi r=0.997 iliskisine gore CIFAR-10'dakinden BUYUK olmali (temiz hata %40-55 bandi).
- **Dikkat:** dusuk dogruluk kosullu kumeleri kucultur (her-ikisi-dogru n~3-4k) → n=10k tam test korunur, alt-orneklem kullanilmaz; AA suresi CIFAR-10 ustunde planlanir (hedefli varyantlar sinif sayisina duyarli). Ilk kosu oncesi 1-tohum ViT pilot + loss egrisi kontrolu.

### E2. Sizinti ablasyonu — ~21 GPU-saat (+3 ops. AA)
- **Tasarim (tek egitim → iki kosul, eslesmis):** 50k bolunur: D_core 46k, V_A 2k, V_B 2k. Clean on-egitim D_core∪V_A (48k; V_A gorulmus, V_B hic gorulmemis); AT yalniz D_core (46k), **tam butce (100 epoch, patience KAPALI), her epoch checkpoint'i kayitli, BIR kez kosulur**. Kosul S (sizintili, run3 tipi): secim V_A; Kosul T (temiz, C1 tipi): secim V_B — iki secim kurali AYNI yorungeye cevrimdisi uygulanir → kosu-ici varyans sifir, sizinti etkisi izole.
- **Kosular:** 2 mimari x 3 tohum = 6 clean on-egitim + 6 tam-butce AT (butce kalirsa +2 tohum; AA yalniz secimlerin ayristigi tohumda).
- **Istatistik:** Birincil = eslesmis fark Δ (kosullu yaniltma PGD [CNN, ViT, CNN−ViT farki — run3 "parite" isaret degisimi], transfer hedef-dogru asimetrisi, PGD gurbuz dogruluk); ikincil = secilen epoch farki, McNemar. Beklenen etki ≈ 0 → **TOST esdegerlik, marj δ=1.0 puan (~2x en buyuk tohum std 0.55; makalede ONCEDEN gerekcelendirilir)**. n=3'te GA yari-genisligi 0.34-0.51 < δ → uygulanabilir. Etki ≥1 puan ise eslesmis t, guc ≈ 1.
- **Not:** run3→C1 kaymasindaki 50k-vs-48k veri-miktari karistiricisi ayri opsiyonel kol (+~20 sa; oncelik dusuk, kapsam disi birakildi).

### E3. Protokol-yayilimi kalibrasyon egrisi — TEZIN OMURGASI — ~6 GPU-saat
- **Eksenler:** x = hedefin temiz hatasi (asimetri surumunde cift temiz-dogruluk farki); y1 = ham−kosullu sapma (yon basina); y2 = 4-protokol yayilimi (cift basina).
- **x kaynagi (ucu birden, birbirini dogrular):** (a) E1+E2 yorunge checkpoint'leri (save_every sayesinde ek egitim maliyeti YOK; checkpoint'ler epoch'a gore degil TEMIZ-DOGRULUK KANTILLERINE gore secilir: ~40/50/60/70/80/konverjan); (b) butce-eslesmis dogrulama kosulari (mimari basina 25 ve 50 epoch butceli bagimsiz AT, ~3-4 sa — "ara checkpoint ≠ konverjan model" itirazina karsi); (c) dogal cesitlilik: CIFAR-10/100/(SVHN) final modelleri, WRN-28-10, E5 cifti (yorunge-bagimsiz noktalar, otokorelasyon sigortasi).
- **Hedef:** ≥12 bagimsiz yorunge x 6 checkpoint ≈ 72 nokta + ~10 dogal nokta; temiz hata araligi ~%5-55.
- **Istatistik:** OLS y=β0+β1x; **yorunge-duzeyi kume bootstrap (B=10,000)** ile β1 ve r GA'lari (noktalar bagimsiz degil — kume bootstrap ZORUNLU); Fisher-z ikincil; dogrusal-olmama testi (karesel terim + LOESS); gurbuz dogruluk KOVARYAT olarak coklu regresyona eklenir (checkpoint'lerde gurbuzluk de degisiyor); mevcut egim 0.762'nin mekanik ozdeslik beklentisiyle karsilastirmasi.
- **Bonus (bedava):** hedef sayisi 3→≥12 olunca gelen-transfer r=0.986 ILK KEZ GA'li raporlanir; 4x4 matris r=0.997 GA'sini ~[0.989; 0.999]'a daraltir.
- **On-kayit:** "hangi checkpoint hedef sayilir" kantil kriteri kosumdan ONCE yazilir (p-hacking elestirisine karsi).

### E4. Tohum sayisi karari: manset ciftte 5, digerlerinde 3 — ~16 GPU-saat
- Yalniz CIFAR-10 ana ciftine +2 tohum (mevcut 3 C1 tohumu yeniden kullanilir) = 4 egitim + 2 AA.
- Gerekce spesifik: "protokol yayilimi kosu-std'sinin ~20 kati" oran iddiasi paydadaki σ̂'ya dayanir; n=3 GA carpani [0.52; 6.29] → kotumser durumda "≥3 kat"a duser; n=5'te [0.60; 2.87] → kotumser durumda bile "≥7 kat" — manset hakem-direncli olur. Manset etkiler (4.4-14.6 puan, std ≤0.55, d>8) icin 3 tohum zaten yeterliydi; 5 tohum yalniz oran iddiasini korur.

### E5. Kapasite-eslenmis cift (R50/ViT-S), CIFAR-10, 3 tohum — ~70-85 GPU-saat (EN BUYUK KALEM)
- **Kosular:** 2 mimari x 3 tohum, C1 recetesi + Bolum 5.3 sigortalari; `save_every` acik (E3'e nokta saglar); 4 protokol + AA n=10k; transfer matrisi 4x4'e genisler (salt degerlendirme ~1-2 sa); patch-4 native ablasyon 1 tohum.
- **ONCE 1 tohum pilot:** sure tahmini FLOP ekstrapolasyonu ±%40; ilk epoch olcumunden sonra plan revize edilir. Pilot patlarsa alternatifler: AA n=5000 (−13 sa; GA ±0.7 puan, hala yeterli) ve/veya ResNet-34 (−18 sa; parametre eslesmesi daha da iyi ama literatur capasi zayif).
- **Istatistik:** ana ciftle ayni foy; **kayitli on-kestirim:** protokol-yayilimi ve r iliskileri kapasiteden bagimsiz kalmali. Siralama tersine donerse (ViT-S > R50) transfer-asimetri anlatisi yeniden kontrol edilir.

### E6. L2 tehdit modeli — YALNIZ CIFAR-10 — ~9.5 GPU-saat (n=5000 ile ~5)
- Linf-egitilmis ana cift final modelleri (3 tohum): AA-L2 eps=0.5 (6 model ≈ 3 cift x 3 sa) + PGD-L2 4-protokol transfer tablosu (~0.5 sa; `PGDL2Attack` kodda hazir, `src/attacks/pgd.py:135`).
- Cerceve: "tehdit modeli = 5. protokol ekseni; ayni modeller, farkli olcum aleti". **Kayitli on-kestirim:** ham−kosullu ~ temiz-hata iliskisi saldiri-agnostik olmali.
- **Dogrulama hukmu:** CIFAR-100-L2 IPTAL (RobustBench'te CIFAR-100 L2 tablosu yok; Engstrom L2 referansi 90.83/69.24 CIFAR-10). Referans: Madry robustness lib.

### E7. SVHN dusuk-hata capasi — ilk dusecek kalem
- **Tam surum (tercih):** RN18/ViT-T x 3 tohum tam pipeline ~28-30 sa + DenseNet-121 referans ~5-6 sa. **Kisa surum (butce sikisirsa):** 2 mimari x 2 tohum, AT 50 epoch (SVHN hizli konverjans), yalniz PGD protokol analizi, AA yok ≈ ~11 sa.
- Zorunlu onlemler: flip kapali, extra-604k yok, **eps-warmup + LR 0.001** (8/255 kararsizligi belgeli), 1 kosu pilot sart, sinif-dengesi kontrolu analiz koduna eklenir (SVHN dengesiz).

---

## 7. Toplam GPU Butcesi ve Oncelik Sirasi

| # | Deney | Kosu sayisi | GPU-saat | Oncelik | Dusurulebilir mi? |
|---|---|---|---|---|---|
| E0 | Altyapi (save_every, adv-ornek arsivi, cevrimdisi secim) | 0 GPU (~1 gun kod) | ~0 | 1 | HAYIR (on kosul) |
| E3 | Kalibrasyon egrisi (eval + 2-4 butce-dogrulama kosusu) | ~80 ckpt eval + 2-4 AT | 6 | 1 | HAYIR — tezin omurgasi |
| E2 | Sizinti ablasyonu | 6 pretrain + 6 tam-butce AT | 21 (+3 ops.) | 1 | HAYIR — run3→C1 kapanisi |
| E1 | CIFAR-100 ana cift, 3 tohum | 6 egitim + 3 AA | 24 | 2 | HAYIR — Q1 asgari genellik |
| E5 | Kapasite cifti R50/ViT-S, CIFAR-10, 3 tohum | 6 egitim + 3 AA + ablasyon | 70-85 | 2 | KISMEN (AA n=5k: −13; R34: −18) |
| E4 | +2 tohum CIFAR-10 (5'e tamamla) | 4 egitim + 2 AA | 16 | 3 | EVET — ama "20 kat" mansetteyse tutulur |
| E6 | AA-L2 + PGD-L2 (yalniz CIFAR-10) | 6 AA-L2 eval | 9.5 (n=5k: ~5) | 4 | EVET (once n=5k'ya indir) |
| E7 | SVHN capasi | tam: 6 egitim + ref; kisa: 4 kisa egitim | tam ~33-36 / kisa ~11 | 5 | EVET — ILK DUSECEK |
| — | Analiz/figur/tekrar tamponu (%10-15) | — | ~15-20 | — | — |

**Toplamlar (dogrulama-duzeltmeli):**
- Cekirdek (E0+E2+E3+E1): **~51 GPU-saat**
- + E5: **~121-136**
- Tam paket (E4+E6+E7-tam dahil): **~180-200**; E7-kisa ile ~158-175
- + tampon: **~170-220 GPU-saat** araligi; plan orta noktasi **~185**

**Duvar-saati:** adanmis RTX 5090 (~20 sa/gun) ile cekirdek ~2.5 gun, onerilen paket ~6.5-7 gun, tam paket ~9-10 gun; **paylasimli GPU'da (vit_ecl container'i!) x1.5-2 → 2-3 hafta.** Uzun bloklar (E5, AA kuyruklari) oncesi `nvidia-smi` kontrolu; AutoAttack kosulari gece kuyruguna.

**Kosu sirasi:** E0 → E2 (yorungeler E3'u besler) → E1 (ckpt kaydi acik) → E3 degerlendirme/regresyon → E5 pilot 1 tohum → E5 kalan → E4 → E6 → E7.
**Dusurme sirasi (once dusecek):** E7 → E6 → E4 → E5 indirimleri. **E1/E2/E3 asla dusurulmez.**
**Reddedilen kapsam:** tam capraz carpim (kume x cift matrisi, ~320 GPU-saat) ve E5'in CIFAR-100'e genisletilmesi (+~70 sa) — hakem "kapasite x kume etkilesimi" sorarsa gelecek-calisma olarak cercevelenir.

---

## 8. Codebase Degisiklik Listesi (dosya-dosya, is sirasi)

Toplam kod isi: **~3.5-4.5 is gunu** (compute haric). Sira, "hicbir egitim E0/veri-butunlugu duzeltmeleri bitmeden baslamaz" ilkesiyle:

**Adim 1 — Veri butunlugu duzeltmeleri (ilk is; ~0.5 gun):**
1. `scripts/run_c1_pipeline.sh`: idempotenlik artefakti `best.pth` → `TRAINING_COMPLETE` (mevcut kural kesinti sonrasi YARIM egitilmis modeli sessizce kabul eder — 24 egitimlik matriste fark edilmesi cok zor veri-butunlugu hatasi); AT adimlarina `--resume` bayragi ekle (su an gecilmiyor, satir 49-54/61-66).
2. `src/training/trainer.py` (clean Trainer): AdversarialTrainer'daki resume + epoch-sonu atomik last.pth + TRAINING_COMPLETE mantigini tasi (~60 satir); `cli/train.py` clean komutuna `--resume`.

**Adim 2 — E0 altyapisi (~1 gun):**
3. `src/training/adversarial_trainer.py`: `--save-every N` periyodik checkpoint (yalniz agirlik, fp32); grad clip max_norm parametrik (10.0 → ViT-S icin 1.0); LR sigortalari (eps-warmup, LR-warmup) konfigurasyona baglanir. DIKKAT: her iki trainer ViT LR'yi sessizce `min(lr, 1e-3)`'e sabitliyor (`trainer.py:88`, `adversarial_trainer.py:141`) — bu cap PARAMETRIK yapilmali (kalibrasyon icin kasitli dusuk-dogruluk egitimlerini carpitabilir).
4. Yeni: cekismeli-ornek arsivleyici (kaynak PGD-10 orneklerini npz/uint8 diske yaz) + cevrimdisi secim araci (checkpoint dizisine best-by-adv-val + patience-20 simulasyonu).
5. `cli/train.py`: `--select-on {val,test}` bayragi (E2 sizinti ablasyonu icin; AdversarialTrainer secim satiri ~375'e kosul — mevcut `--val-split 0` yolu FARKLI egitim verisi kullandigindan ozdes-veri ablasyonu icin yetersiz).

**Adim 3 — Veri katmani generic'lestirme (~0.5 gun):**
6. `src/data/datasets.py`: `DATASETS` registry (`cifar10/cifar100/svhn`; sinif sayisi, N_train, boyut) + generic `get_loaders` / `get_loaders_with_val` (Normalize'siz, raw [0,1] KORUNARAK — saldiri tabani `src/attacks/base.py:89-99` [0,1] varsayiyor); mevcut `get_cifar10_*` fonksiyonlari ince sarmalayici olur (**27 dosya import ediyor — dokunulmaz**). SVHN adaptoru: `split='train'`, flip KAPALI. `src/data/__init__.py` export guncellemesi.
7. `experiments/rev2/make_val_split.py`: hardcoded `N_TRAIN=50000` ve cikti yolu → `--dataset --n-train --val-size --out` argparse; kume basina `data/val_split_indices_<dataset>.json` (SVHN 73257!).

**Adim 4 — Model katmani (~0.5 gun):**
8. `src/models/vit.py`: `CIFAR10ViTTiny.get_attention_maps`'i (satir 327-393) `TimmViTAttentionMixin`'e cikar, `CIFAR10ViTSmall` da miras alsin (~30 satir; grid dinamik hesaplandigi icin dogrudan calisir). DIKKAT: CIFAR-native `vit_cifar_small` list, timm sarmalayici dict donduruyor — cift timm'de kalmali.
9. Yeni `src/utils/load_model_auto.py`: checkpoint head agirlik seklinden (`fc.weight`/`head.weight` satir sayisi) num_classes'i OTOMATIK cikaran `load_model_auto(model_type, ckpt_path, device)`; tum eval scriptleri buna gecer — CIFAR-100'de bayrak unutma hatasi yapisal olarak engellenir (`ModelRegistry.get` kwargs'i destekliyor ama hicbir cagri gecmiyor: cli/train.py:43,130 vb.).

**Adim 5 — CLI (~0.5 gun):**
10. `cli/train.py`: her iki komuta `--dataset [cifar10|cifar100|svhn]` (num_classes kumeden turer, `ModelRegistry.get(model, num_classes=nc)`), `--save-every`.

**Adim 6 — Eval/deney scriptleri (~1 gun):**
11. `scripts/c1_pgd_eval.py` (en temiz sablon): `--dataset --eps --norm` ekle (L2 icin `PGDL2Attack` hazir).
12. `experiments/run_autoattack_run2.py`: `--model AD:TIP:YOL` tekrarli bayrak + `--dataset --norm --eps` (hardcoded "resnet18"/"vit_tiny" satir 187-190, dataset satir 185, norm satir 116); **chunk-resume mekanizmasi (satir 97-134) aynen korunur**.
13. `experiments/rev2/a2_transfer_protocols.py`: modul-duzeyi calisiyor (main yok) → argparse'li `main()` (`--in-dir --out --src-name --tgt-name`); 4-protokol istatistik cekirdegi (raw/target_correct/both_correct/successful_source + paired bootstrap + TOST) OLDUGU GIBI yeniden kullanilir.
14. `experiments/run_all_analyses_run2.py`: `run_transfer_analysis` imzasina `models_config` ve `dataset` parametresi; `scripts/c1_transfer_rerun.py`'nin kirilgan `RUN2_MODELS` monkeypatch hilesi argparse'a cevrilir.
15. `experiments/c1_c3_transfer_matrix.py`: robustbench `load_model` cagrisina dataset parametresi + CIFAR-100 referansi `Pang2022Robustness_WRN28_10`; SVHN icin referans kendi DenseNet-121'imiz (veya 2x2 matris).

**Adim 7 — Pipeline genellemesi + duman testi (~0.5-1 gun):**
16. `scripts/run_c1_pipeline.sh`: `DATASET=`, `PAIR=`, `SEEDS=` env parametreleri + mimari-basina hiperparametre `case` blogu; cikti agaci `models/q1/${DATASET}/${arch}_s${seed}/`, `results/q1/${DATASET}/pair${i}/`; val-split artefakti kume-bazli. Yeni scriptlerde `ROOT = "/workspace" if ... else "~/projects/adeb_sci_1"` deseni korunur. Her yeni (kume x mimari) kombinasyonunda once kucuk-n duman testi (n=200), sonra tam kosum.

---

## 9. Riskler ve Acik Sorular

**Yuksek oncelikli riskler:**
1. **Scooping:** "Beyond ASR" bandi 2026'da aktif (Curl ve ark. medikal alanda cikti); ayni fikrin genel-vizyon versiyonu her an cikabilir → protokol-denetimi + kalibrasyon cekirdegiyle ERKEN arXiv on-baskisi.
2. **"Artimsal" bulunma:** Zhao TPAMI 2025 "kotu degerlendirme yaniltici sonuc uretir" ana fikrini yayimladi; ayristirma (kosullama paydasi + temiz-hata karistiricisi + tohum varyansi) net yazilamazsa ret riski yuksek. Yu SaTML 2025 "protokol" kelimesi nedeniyle algi riski — acik karsilastirma paragraflari sart.
3. **ViT-S AT cokme riski:** Mo ve ark. grad-clip'siz ViT-B/DeiT-S'in ~%10 robustluga coktugunu raporluyor; sigortalara ragmen ilk 5 epoch adv-acc izlemesi sart (<%15 → LR yarila). Sure tahminleri ±%40 → pilot olmadan 3 tohuma girilmez.
4. **Sessiz yarim-model tuzagi:** pipeline artefakt=best.pth kurali duzeltilmeden hicbir Q1 kosusu baslatilmaz (Bolum 8, Adim 1).
5. **SVHN 8/255 AT kararsizligi** literaturde belgeli; ViT-Tiny SVHN ilk kosusu patlarsa ek deneme butcesi gerekir (eps-warmup + LR 0.001 + pilot).

**Orta oncelikli riskler:**
6. Protokol-farki elestirisi: finetune-AT sayilarimiz scratch-AT literaturunun (Engstrom 49.25) altinda — makalede acik gerekce yazilmazsa "yetersiz egitim" denir.
7. Parametre eslesiyor, FLOPs eslesmiyor (~3.5x) — "parametre-eslesmis (FLOPs degil)" diye adlandirilmali; patch-4 ablasyonu kismi yanit.
8. r=0.997 / r=0.986 az noktaya dayaniyor — E3 tamamlanmadan ana kanit olarak sunulmaz; kume bootstrap zorunlu; dogal-cesitlilik noktalari plandan cikarilmaz.
9. TGR-negatif bulgusu 2025-sonrasi ViT-ozgu saldirilar (TESSER, FPA, FUGEA) denenmeden genellenirse curutulebilir → acik rejim sinirlamasi veya TESSER ekleme.
10. CIFAR-100'de ViT-Tiny temiz dogrulugu RN18'i gecerse anlatidaki isaret degisir (tez icin avantaj ama dikkatli cerceve ister); kosullu kumeler kuculur (GA'lar genisler).
11. Negatif-sonuc cercevesi Elsevier'de risk — pozitif metodolojik cikti (denetim tablosu + kalibrasyon + oneri protokolu) one alinmali.
12. GPU paylasimli (vit_ecl) — sureler x1.5-2 olabilir; disk ~30-40GB (2-epoch kayitla yariya iner).
13. E2'nin beklenen sonucu sifir etki (C1 bulgusu: sizinti aciklamasi zaten tutmamisti) — TOST marji onceden gerekcelendirilmezse "negatifi esdeger diye satiyorsunuz" elestirisi.

**Acik sorular (kapanis gerektirir):**
- Yu ve ark. SaTML 2025 camera-ready tam metni kurum IEEE erisimiyle indirilecek; 3 protokol tanimi son kez teyit (dusuk olasilikli tek acik dogrulama noktasi).
- IF/ceyrek resmi JCR teyidi (TNNLS/TIFS ucuncu-taraf degerleri celisik).
- Kurumsal gereklilik: JCR ceyregi sart mi? (TMLR opsiyonunun onunu acar/kapar.)
- E5 cifti CIFAR-100'e genisletilsin mi? (Su an HAYIR; hakem sorarsa gelecek-calisma.)
- TESSER deney matrisine eklensin mi, yoksa rejim sinirlamasi yeterli mi? (Butce onceligi dusuk; varsayilan: sinirlama.)
- ImageNet-olcekli salt-degerlendirme bileseni (RobustBench ImageNet modelleriyle 3x3) eklensin mi? — "32x32-only" elestirisine karsi en guclu ek onlem; egitim maliyeti yok, degerlendirme maliyeti orta.
- Bouthillier ve ark. "Accounting for Variance in ML Benchmarks" (MLSys 2021) atif verilecekse kunyesi ayrica teyit edilmeli (bu taramada dogrulanmadi).

---

## 10. Kaynakca

### Rakip/komsu calismalar (dogrulanmis kunyelerle)
- Zhao ve ark., Revisiting Transferable Adversarial Images (TPAMI 2025): https://arxiv.org/abs/2310.11850 · repo: https://github.com/ZhengyuZhao/TransferAttackEval · oncul: https://arxiv.org/abs/2211.09565
- Yu ve ark., Reliable Evaluation of Adversarial Transferability (SaTML 2025): https://arxiv.org/abs/2306.08565 · https://ieeexplore.ieee.org/abstract/document/10992575/
- Curl ve ark., Beyond Attack Success Rate (2026 preprint): https://arxiv.org/abs/2604.16532
- Gu ve ark., transferabilite anketi: https://arxiv.org/abs/2310.17626
- AttackBench (AAAI 2025): https://arxiv.org/abs/2404.19460 · Evaluating the Evaluators: https://arxiv.org/abs/2507.03450
- Pinto ve ark., Impartial Take: https://arxiv.org/abs/2504.20121 (baglam) · Waseda ve ark. WACV 2023: https://openaccess.thecvf.com/content/WACV2023/papers/Waseda_Closer_Look_at_the_Transferability_of_Adversarial_Examples_How_They_WACV_2023_paper.pdf
- Defense That Attacks: https://arxiv.org/pdf/2512.02830

### Degerlendirme metodolojisi seceresi
- Carlini ve ark. 2019: https://arxiv.org/abs/1902.06705 · Tramèr ve ark. 2020: https://arxiv.org/abs/2002.08347
- AutoAttack: https://arxiv.org/abs/2003.01690 · RobustBench: https://arxiv.org/abs/2010.09670 · https://robustbench.github.io/
- Lorenz ve ark. 2022: https://arxiv.org/abs/2112.01601 · Pintor ve ark. 2022: https://arxiv.org/abs/2106.09947

### Kalibrasyon-egrisi analoglari ve ust-cerceve
- Benchmark Lottery: https://arxiv.org/abs/2107.07002
- GRN ranking instability (2026, tek yazarli preprint): https://arxiv.org/pdf/2603.03493
- SOTA Claims Require SOTA Evidence: https://arxiv.org/html/2605.17273 · Posterior Agreement: https://arxiv.org/pdf/2503.16271
- ASRD baglami (NLP backdoor): https://arxiv.org/pdf/2404.11538 · https://arxiv.org/pdf/2110.02797
- Emergent Mind ASR/transfer tanimlari: https://www.emergentmind.com/topics/attack-success-rate-asr · https://www.emergentmind.com/topics/transfer-attacks

### Negatif sonuc / replikasyon gelenegi
- MLRC @ NeurIPS 2026: https://blog.neurips.cc/2026/05/04/mlrc-2026-reproducibility-as-an-official-track-at-neurips/
- TMLR politikalar: https://jmlr.org/tmlr/editorial-policies.html · http://jmlr.org/tmlr/ · https://medium.com/@TmlrOrg/tmlr-joins-neurips-icml-iclr-journal-to-conference-track-937a898eab3d
- ICBINB (PMLR v163): https://proceedings.mlr.press/v163/ · SaTML CFP: https://satml.org/participate-cfp/
- Embracing Negative Results: https://arxiv.org/pdf/2406.03980 · Refutations and Critiques Track: https://arxiv.org/pdf/2506.19882
- ALP geri cekilmesi (CMU blog): https://blog.ml.cmu.edu/2020/08/31/5-reproducibility/ · Siber guvenlik reproducibility: https://arxiv.org/html/2405.18753
- TMLR reproducibility ornegi: https://github.com/fatemehN/ReproducibilityStudy · https://openreview.net/forum?id=lE7K4n1Esk

### ViT/CNN robustluk ve AT tarifleri
- Debenedetti ve ark., Light Recipe (SaTML 2023): https://arxiv.org/abs/2209.07399 · https://ar5iv.labs.arxiv.org/html/2209.07399 · repo: https://github.com/dedeswim/vits-robustness-torch · config: https://raw.githubusercontent.com/dedeswim/vits-robustness-torch/master/configs/xcit-adv-finetuning.yaml · https://raw.githubusercontent.com/dedeswim/vits-robustness-torch/master/configs/xcit-adv-training-cifar10.yaml
- Mo ve ark. (NeurIPS 2022): https://arxiv.org/abs/2210.07540 · https://ar5iv.labs.arxiv.org/html/2210.07540 · repo: https://github.com/mo666666/When-Adversarial-Training-Meets-Vision-Transformers
- Shao ve ark. (TMLR 2022): https://arxiv.org/abs/2103.15670 · https://ar5iv.labs.arxiv.org/html/2103.15670
- Madry robustness lib: https://github.com/MadryLab/robustness
- Singh ve ark., Revisiting AT for ImageNet: https://arxiv.org/pdf/2303.01870 · Revisiting AT at Scale: https://arxiv.org/html/2401.04727 · MIMIR: https://arxiv.org/pdf/2312.04960
- ACM CSUR 2025 ViT robustness anketi: https://dl.acm.org/doi/pdf/10.1145/3729167
- Electronics 2024: https://doi.org/10.3390/electronics13132534 · MBEC 2024: https://link.springer.com/article/10.1007/s11517-024-03226-5
- TGR: https://arxiv.org/pdf/2303.15754 · TESSER: https://arxiv.org/pdf/2505.19613 · FPA: https://arxiv.org/html/2503.20310 · FUGEA (Neural Networks 2026): https://www.sciencedirect.com/science/article/abs/pii/S0893608026003874
- AAAI 2025 ViT-B/2 native-32: https://ojs.aaai.org/index.php/AAAI/article/view/32073 · https://arxiv.org/pdf/2502.21041

### RobustBench model kartlari (dogrulanan sayilar)
- Engstrom2019 (CIFAR-10 R50): https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar10/Linf/Engstrom2019Robustness.json
- CIFAR-100 Linf listesi: https://api.github.com/repos/RobustBench/robustbench/contents/model_info/cifar100/Linf
- Wang2023: https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Wang2023Better_WRN-70-16.json
- Rice2020: https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Rice2020Overfitting.json
- Debenedetti XCiT-S12: https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Debenedetti2022Light_XCiT-S12.json
- Rebuffi2021: https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Rebuffi2021Fixing_R18_ddpm.json
- Pang2022: https://raw.githubusercontent.com/RobustBench/robustbench/master/model_info/cifar100/Linf/Pang2022Robustness_WRN28_10.json
- AutoAttack repo: https://github.com/fra31/auto-attack

### SVHN/AT konvansiyonlari
- AWP: https://github.com/csdongxian/AWP · https://proceedings.neurips.cc/paper/2020/file/1ef91c212e30e14bf125e9374262401f-Paper.pdf
- HAT: https://github.com/imrahulr/hat · https://openreview.net/pdf?id=Azh9QBQ4tR7
- Xu ve ark. fairness (ICML 2021): http://proceedings.mlr.press/v139/xu21b/xu21b-supp.pdf
- Diger AT emsalleri: https://arxiv.org/pdf/2305.12118 · https://arxiv.org/pdf/2304.00202 · https://arxiv.org/pdf/2210.05958 · https://arxiv.org/html/2510.26833 · https://arxiv.org/pdf/2502.19755
- CIFAR veri kumesi makalesi (NeurIPS D&B): https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/a3c65c2974270fd093ee8a9bf8ae7d0b-Paper-round2.pdf

### Dergi bilgileri (ucuncu-taraf; JCR teyidi bekliyor)
- https://www.journalmetrics.org/journal/information-sciences · https://www.journalmetrics.org/journal/neural-networks · https://www.journalmetrics.org/journal/machine-learning
- https://wos-journal.info/journalid/19520 · https://www.bioxbio.com/journal/PATTERN-RECOGN · https://www.bioxbio.com/journal/IEEE-T-NEUR-NET-LEAR · https://www.bioxbio.com/journal/IEEE-T-INF-FOREN-SEC
- https://scirev.org/journal/pattern-recognition/ · https://scirev.org/journal/neurocomputing/ · https://scirev.org/journal/neural-networks/ · https://scirev.org/journal/ieee-transactions-on-information-forensics-and-security/
- https://www.letpub.com/index.php?page=journalapp&view=detail&journalid=3394 · https://research.com/journal/pattern-recognition-1 · https://journalsearches.com/journal.php?title=pattern+recognition
- Liu ve ark. (PR 2023, emsal): https://www.sciencedirect.com/science/article/abs/pii/S0031320323000092
- Rect-ViT (Neural Networks 2025): https://www.sciencedirect.com/science/article/abs/pii/S0893608025005465 · attribution transfer (NN 2025): https://www.sciencedirect.com/science/article/abs/pii/S0893608025002205
- Neurocomputing transfer (2024): https://www.sciencedirect.com/science/article/abs/pii/S0925231224013912
- TIFS transfer (2024): https://dl.acm.org/doi/10.1109/TIFS.2024.3411921 · TIFS bilgi: https://signalprocessingsociety.org/publications-resources/ieee-transactions-information-forensics-and-security/ieee-transactions
- NCA 2026 tarzi emsal: https://link.springer.com/article/10.1007/s00521-025-11734-0 · TNNLS: https://cis.ieee.org/publications/t-neural-networks-and-learning-systems
- TransferBench OpenReview PDF (erisim engelli, manuel okunacak): https://openreview.net/pdf?id=uT0A1pjBqu

### Yerel kanit dosyalari
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\TIMING.md` (olculmus sureler)
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\results\C1_REFERANS_FOYU.md`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\scripts\run_c1_pipeline.sh`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\src\training\adversarial_trainer.py` · `src\training\trainer.py`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\src\models\vit.py` · `src\models\resnet.py` · `src\models\registry.py`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\src\data\datasets.py` · `src\attacks\pgd.py` · `src\attacks\base.py`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\experiments\run_autoattack_run2.py` · `experiments\run_all_analyses_run2.py` · `experiments\rev2\a2_transfer_protocols.py` · `experiments\rev2\make_val_split.py` · `experiments\c1_c3_transfer_matrix.py`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\scripts\c1_pgd_eval.py` · `scripts\c1_transfer_rerun.py`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\logs\C1_at_vit_2001.log` · `logs\C1_at_resnet_1001.log` · `logs\C1_aa_pair1.log`
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\models\c1\` (checkpoint envanteri: yalnizca best.pth+last.pth)

---

*Sentez notu: Celiskili noktalarda dogrulama ajanlarinin hukumleri esas alindi — basliklar: (1) tam capraz carpim reddedildi (yeni cift yalniz CIFAR-10, kume genisletmesi yalniz mevcut cift); (2) butce veri ajaninin 35-40 saati degil kalem-kalem ~150-185 GPU-saat; (3) SVHN referansi once DenseNet-121; (4) CIFAR-100 referansi Pang2022 (Cui2023 degil), ek-veri etiketli; (5) ViT-S: bs=64, AdamW 5e-4, clip 1.0, eps-warmup (SVHN'e de); Mo vanilla 46.37 esas capa; (6) L2 yalniz CIFAR-10; (7) kunye duzeltmeleri: Yu=SaTML 2025 konferansi, Zhao=23x11.*
