# E3 Yeniden Tasarımı — ön-kayıt sapması ve gerekçesi

**Tarih: 2026-08-19.** Bu belge, K-01 kararının (bkz. `KAMPANYA_KARARLARI.md`)
açtığı borcu kapatır: *"E3 yeniden tasarımı yazılmalı — E5 kararının
önkoşulu."*

E3 tezin omurgasıdır: ham−koşullu sapmanın ve 4-protokol yayılımının, hedefin
temiz hatasıyla nasıl ölçeklendiğini kalibre eder. Ön-kayıtlı tasarım
**çalışmıyor**; aşağıda önce ölçüm, sonra düzeltme, sonra sapmanın beyanı yer
alır.

---

## 1. Ölçülen sorun — kantil seçimi noktaları çökertiyor

Ön-kayıt her yörüngeden `CLEAN_TARGETS = [40, 50, 60, 70, 80, konverjan]`
kantillerine göre 6 checkpoint seçmeyi öngörüyordu (≥12 yörünge × 6 ≈ **72
nokta** hedefi).

`scripts/q1_e3_calibration.py` içindeki seçim `chosen[ep] = ck` biçimindedir:
**birden fazla hedef aynı epoğa düşerse girdiler sessizce tek noktaya çöker.**
Yörüngelerin temiz doğruluk aralığı hedeflerin çoğunu kapsamadığı için bu
düzenli olarak oluyor.

Ölçüm (`scripts/q1_e3_coverage.py` → `results/q1/e3_coverage.json`;
`cmd_points` ile **aynı** seçim mantığı, GPU'suz):

> **DÜZELTME (2026-08-20).** Bu bölümün ilk sürümü, E1 **hâlâ koşarken**
> üretilmiş bayat bir artefakta dayanıyordu (11 yörünge / 33 nokta / %50 /
> 756 ckpt). O anda `resnet18_s1003` 2 checkpoint'teydi ve `vit_tiny_s2003`
> hiç yoktu. Kök sebep: `q1_e3_coverage.py`'de **bitmişlik kapısı yoktu**.
> Kapı eklendi (`TRAINING_COMPLETE` aranıyor) ve ölçüm yenilendi. Aşağıdaki
> sayılar 12/12 yörünge tamamlandıktan sonraki **geçerli** değerlerdir.
> Hükmün yönü değişmemiştir; çöküş %50 yerine %47,2'dir.

| yörünge grubu | checkpoint | temiz doğruluk (val) | ayrı nokta |
|---|---|---|---|
| ResNet-18 CIFAR-10 (×3) | 100 · 100 · 100 | 82,3 - 89,3 | **2/6** her birinde |
| ViT-Tiny CIFAR-10 (×3) | 100 · 100 · 100 | 57,7 - 76,7 | 4/6 · 5/6 · 4/6 |
| ResNet-18 CIFAR-100 (×3) | 52 · 44 · 69 | 59,8 - 65,5 | 3/6 · 3/6 · 4/6 |
| ViT-Tiny CIFAR-100 (×3) | 27 · 31 · 40 | 33,1 - 43,6 | 3/6 · 3/6 · 3/6 |

**Toplam: 12 yörünge, 72 hedef → 38 ayrı nokta (%47,2 çöküş).** ResNet
CIFAR-10'da her yörünge yalnız **2** nokta veriyor; 40/50/60/70 hedeflerinin
dördü de aynı (en düşük temiz doğruluklu) checkpoint'e düşüyor.

Aynı yörüngelerin **tüm** checkpointleri kullanılsaydı: **863 nokta.**

## 2. Ölçülen ikinci sorun — x ekseninin kapsaması

Yukarıdaki tablo *doğrulama* doğruluğudur (kantil seçimi onu kullanır). E3'ün
regresyon ekseni ise **test** temiz hatasıdır. Yetkili ölçüm P0 test
eğrilerinden (`results/q1/e2/testcurve_*.npz`, gerçek 10.000 örnek test) →
`results/q1/e3_xekseni_test.json`:

| yörünge | temiz hata (test) |
|---|---|
| ResNet-18 s1001/2/3 | %12,38-18,14 · %12,15-19,38 · %12,06-18,45 |
| ViT-Tiny s2001/2/3 | %24,80-41,55 · %24,39-43,11 · %23,47-40,75 |

600 noktanın bant dağılımı:

| bant | nokta |
|---|---|
| %0-5 | **0 — BOŞ** |
| %5-10 | **0 — BOŞ** |
| %10-12 | **0 — BOŞ** |
| %12-20 | 300 |
| %20-30 | 262 |
| %30-45 | 38 |

**İki boşluk vardır:**

1. **%12'nin altı tamamen boştur.** Dış çapa WRN-28-10 (temiz 89,48 → hata
   %10,52) yalnız %10,5'e iniyor. Ön-kayıtlı hedef aralık %5-55 idi;
   alt uç **karşılanmıyor**. Bu, K-01'de E7-kısa'nın koşulmasına karar
   verilmesinin ölçülmüş gerekçesidir (SVHN AT temiz ~%92-95 → hata %5-8).
2. **%19,4 - %23,5 arası boştur** — ResNet yörüngelerinin üst ucu ile ViT
   yörüngelerinin alt ucu arasındaki kopukluk. Bu bant CIFAR-100 noktalarıyla
   dolar (E1), yani E1 bittiğinde kapanması beklenir; kapanmazsa regresyon iki
   ayrık kümeye fit ediliyor demektir ve **doğrusallık testi bunu yakalamalıdır**.

## 3. Yeniden tasarım

### 3.1 Kantil seçimi TERK EDİLİYOR — tüm checkpointler kullanılacak

Yörünge başına 6 kantil yerine **yörüngenin tüm checkpointleri** noktaya
dönüşür (gerekirse sabit adımla seyreltilir, aşağıya bakınız).

**Bu ön-kayıttan bir sapmadır ve beyan edilmektedir (§4).** Sapmanın yönü
kritiktir: bir **seçim adımını kaldırıyoruz**, eklemiyoruz. Ön-kaydın kantil
kriterini yazma gerekçesi p-hacking eleştirisiydi; tüm noktalar kullanıldığında
kiraz toplama **fiziksel olarak imkânsızdır**, dolayısıyla sapma
ön-kaydın amacını zayıflatmaz, güçlendirir.

**Otokorelasyon.** Aynı yörüngenin ardışık checkpointleri bağımsız değildir;
nokta sayısını 38'den 863'e çıkarmak **bağımsız bilgi miktarını artırmaz**.
Bunu karşılayan mekanizma zaten ön-kayıtlıdır ve kodda vardır:
**yörünge düzeyi küme bootstrap (B=10.000)** — `cluster_bootstrap`,
`q1_e3_calibration.py:200`. Serbestlik derecesi yörünge sayısıyla belirlenir,
nokta sayısıyla değil. Bu, metinde **açıkça** yazılacaktır; aksi halde "n=863"
sahte bir kesinlik izlenimi verir.

**Maliyet.** Ek eğitim YOKTUR; yalnız ileri geçiş. Kaba tahmin: 863
checkpoint × 10.000 örnek × (temiz + çekişmeli arşiv) ≈ 2-4 GPU-saat. Bütçe
sıkışırsa **sabit adımla seyreltme** (her 2. veya 5. checkpoint) yapılır —
bu da sonuçtan bağımsız, deterministik bir kuraldır, dolayısıyla seçim
serbestliği yaratmaz. Seyreltme uygulanırsa adım **önceden** yazılır.

### 3.2 İki kol AYRI raporlanacak — havuzlama YASAK

| kol | noktalar | temiz hatayı ne değiştiriyor | statü |
|---|---|---|---|
| **A — kontrollü** | yörünge-içi checkpointler | yalnız **eğitim olgunluğu**; mimari, veri, reçete, tehdit modeli sabit | nedensel yorum mümkün |
| **B — gözlemsel** | RobustBench zoo, WRN-28-10, CIFAR-10/100/SVHN final modelleri, (ertelenmiş E5) | mimari + kapasite + reçete + ek veri **birlikte** | yalnız ilişkisel |

**Manşet, iki kolun eğimlerinin uyuşmasıdır.** Bu, tek koldan güçlüdür:
kontrollü kol nedenselliği, gözlemsel kol dış geçerliliği verir; uyuşmaları
her ikisinin de aynı mekanizmayı ölçtüğünün kanıtıdır.

**İki kol tek OLS'ye HAVUZLANMAYACAKTIR.** Havuzlama, A kolunun tek
avantajını (karıştırıcıların sabit olması) yok eder ve regresyonu B kolunun
geniş aralığının domine etmesine yol açar.

**Özgünlük iddiası A koluna aittir.** Araştırma raporu E3'ün katkısını
"ölçüm artefaktının karıştırıcıyla **kontrollü** ilişkilendirilmesi" olarak
tanımlıyor. Zoo modelleriyle x eksenini genişletmek bu iddiayı **korumaz,
değiştirir** — bu yüzden zoo, A kolunun yerine değil **yanına** konur.
Buna karşılık B kolu, `05_discussion.tex`'teki uygulama hedefi (yayımlanmış
ham oranların yeniden yorumlanması) için doğru koldur: düzeltme yayımlanmış
modellere uygulanacaksa yayımlanmış modellerde kalibre edilmelidir.

### 3.3 Kovaryat ve doğrusallık (ön-kayıttan DEĞİŞMEDİ)

- Gürbüz doğruluk **kovaryat** olarak çoklu regresyona girer (checkpointler
  boyunca gürbüzlük de değişiyor).
- Doğrusal olmama testi (karesel terim + LOESS) korunur; §2'deki ikinci
  boşluk nedeniyle **zorunludur**.
- Fisher-z ikincil kalır.

## 4. Ön-kayıt sapmasının beyanı (makalede yer alacak)

> E3'ün ön-kaydı, her eğitim yörüngesinden temiz-doğruluk kantillerine göre
> altı checkpoint seçmeyi öngörüyordu. Koşum sonrası ölçüm, yörüngelerin
> temiz-doğruluk aralığının hedeflerin çoğunu kapsamadığını ve seçimin
> noktaları çökerttiğini gösterdi: 72 hedef yalnız 38 ayrı checkpoint
> üretiyor, ResNet yörüngelerinde altı hedefin dördü tek bir checkpoint'e
> düşüyordu. Bu nedenle kantil seçimi terk edilmiş ve her yörüngenin tüm
> checkpointleri kullanılmıştır. Sapma bir seçim adımını **kaldırmaktadır**;
> çıkarım, ön-kayıtta olduğu gibi yörünge düzeyi küme bootstrap'e
> dayanmaktadır, dolayısıyla serbestlik derecesi nokta sayısıyla değil
> yörünge sayısıyla belirlenir.

## 5. Bu tasarımın E5 ve E7 üzerindeki sonuçları

- **E5 (ertelendi, K-01):** bu tasarım altında E5'in E3'e katkısı iki
  yörünge daha eklemektir; kontrollü kol zaten 6-11 yörünge taşıyor. Erteleme
  kararı **doğrulanmıştır**. E5 koşulursa gerekçesi E3 değil, "kapasite
  eşlenmiş çift" iddiası olmalıdır ve o iddia 1 tohumla kurulamaz (payda σ'sı
  yok) — bu sınır K-01'de zaten kaydedildi.
- **E7-kısa (koşulacak, K-01):** §2'de ölçülen boş alt bandın **tek** çaresi.
  Bu belge, E7 kararının ölçülmüş gerekçesidir.
- **E1:** %19,4-23,5 boşluğunu kapatması beklenir; kapatıp kapatmadığı
  E1 bitince bu belgeye ek olarak yazılacaktır.

## 6. Yapılacaklar (kod)

1. `q1_e3_calibration.py cmd_points`: `--all-checkpoints` (varsayılan) ve
   `--stride N` bayrakları; kantil kolu `--quantile-mode` altında geriye dönük
   uyumluluk için bırakılır.
2. `cmd_fit`: nokta json'larına **kol etiketi** (`arm: A|B`) eklenir; fit iki
   kolu ayrı koşar ve eğim farkı için küme bootstrap GA'sı üretir.
3. Havuzlanmış fit **üretilmeyecek** — kodda böyle bir çıktı yolu
   bırakılmayacak ki sonradan yanlışlıkla raporlanmasın.

---

## EK A — §2'nin vaat ettiği boşluk ölçümü (2026-08-20)

§2 iki boşluk saymış ve ikincisi için bir **beklenti** yazmıştı:

> *"İkinci bir boşluk daha ölçüldü: %19,4-23,5 arası — ResNet ile ViT
> yörüngeleri arasındaki kopukluk. **E1'in CIFAR-100 noktalarıyla kapanması
> bekleniyor.**"*

E1 bitti; beklenti ölçüldü. **Beklenti karşılanmadı.**

Üretici: `scripts/q1_e3_bosluk_kontrol.py` → `results/q1/e3_bosluk_kontrol.json`
(girdi: `e3_coverage.json` yörünge aralıkları + `e1_cifar100_summary.json`
gerçek test temiz doğrulukları).

### A.1 Ölçülen kapsama

Yörüngelerin temiz hata ekseninde kapladığı birleşim:

| kapsanan aralık | genişlik |
|---|---|
| %10,72 – 17,68 | 6,96 |
| %23,28 – 42,28 | 19,00 |
| %56,40 – 66,95 | 10,55 |

**Ölçülen boşluklar:**

| boşluk | genişlik | durum |
|---|---|---|
| **%17,68 – 23,28** | **5,60** | §2'nin adıyla andığı kopukluk; **hâlâ boş** |
| **%42,28 – 56,40** | **14,12** | **§2'de HİÇ ANILMAMIŞ**; bu ölçümde ortaya çıktı |
| %12'nin altı | — | E7 (SVHN) kapatacak; koşum 2026-08-20'de başladı |

### A.2 E1 boşluğu neden kapatmadı

CIFAR-100 modellerinin gerçek test temiz hataları: ResNet **%35,33 / 35,76 /
37,33**, ViT **%55,94 / 56,50 / 58,06**. Altı noktanın hepsi boşluğun **çok
üzerinde**. Ön-kayıtlı boşluğun kapsanan oranı: **%4,6** — ve o %4,6 bile
boşluğa giren bir noktadan değil, iki CIFAR-10 ViT yörüngesinin (s2002, s2003)
alt ucunun boşluğun üst kenarına **0,19 puan** girmesinden geliyor.

Beklenti neden yanlıştı: CIFAR-100'ün "daha zor" olması, temiz hatayı boşluğun
**içine** değil **üstüne** taşır. Zorluk arttıkça hata artar; ara bir bandı
doldurmak için ara bir zorluk gerekir, daha yükseği değil.

### A.3 Bunun E3 için sonucu — raporlanması ZORUNLU

E3'ün regresyonu %10,72-66,95 arasını kapsıyor ama içinde toplam **19,72
puanlık iki delik** var. Bu bantlarda:

- eğim **hiçbir noktayla desteklenmiyor**; oradaki değerler **interpolasyondur**,
- iki kol (A: yörünge-içi, B: gözlemsel) de aynı deliklere sahiptir, dolayısıyla
  "iki kolun eğimleri uyuşuyor" manşeti bu bantlar için kanıt taşımaz,
- doğrusallık varsayımı deliklerin içinde **sınanmamıştır**.

**Bağlayıcı:** E3 raporlanırken bu iki delik şekil üzerinde görünür kılınacak
ve metinde adıyla anılacaktır (K8). Kapsama, "n=863 nokta" ifadesiyle
sunulmayacaktır — 863 nokta 12 yörüngeden gelir ve eksende **sürekli değildir**.

### A.4 Boşlukları ne kapatabilir

| boşluk | aday | durum |
|---|---|---|
| %17,68 – 23,28 | E5 (ResNet-50 / ViT-Small, CIFAR-10) | **ERTELENDİ** (K-01) |
| %42,28 – 56,40 | CIFAR-100 ViT yörüngesinin erken epokları | ölçülebilir: B.8 borcu kapanınca (`q1_e2_test_curve.py --dataset cifar100`, İŞ-6a ile **kod hazır**) |
| %12 altı | E7 (SVHN) | koşuyor |

İkinci boşluk için ucuz bir yol var: CIFAR-100 yörüngelerinin **test** eğrileri
henüz üretilmedi (şimdiye kadar yalnız val vekili vardı). Kod artık
veri-kümesi-parametrik; koşulduğunda o yörüngelerin erken epokları %42-56
bandına düşebilir. **Düşeceği varsayılmayacak, ölçülecektir** — bu ekin
yazılmasına yol açan hata tam olarak buydu.
