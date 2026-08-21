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

---

## EK B — E3'ün KESTIRDIĞI NİCELİK DEĞİŞTİ (2026-08-20, sapma beyanı)

**Bu bir sapma beyanıdır ve nedeni ölçümdür.** Eski satırlar değiştirilmemiştir.

### B.1 Neden

`scripts/q1_ozdeslik_kontrol.py` (→ `results/q1/ozdeslik_kontrol.json`)
E3'ün birincil kestirim hedefinin **cebirsel bir özdeşlik** olduğunu ölçtü:

$$r_{ham} - r_{koş} = e\,(1 - r_{koş})$$

36 köşegen dışı yönde artık: mutlak ortalama 0,095 puan, en büyük 0,41 puan;
öncül $P(\text{adv yanlış}\mid\text{temiz yanlış}) = 0{,}989$–$1{,}000$.

Bu belge (§1-§4) E3'ü *"ham−koşullu sapmanın hedefin temiz hatasıyla nasıl
ölçeklendiğini kalibre etmek"* diye tanımlamıştı. **O ilişki artık ölçülecek
bir şey değildir; türetilmiştir.** 863 noktayı, sonucu önceden bilinen bir
regresyona harcamak GPU israfı olur ve makaleye sahte bir ampirik katman ekler.

### B.2 Yeni kestirim hedefi

E3 artık **protokol yayılımını** kalibre eder — makalenin manşet niceliği ve
özdeşlikle **türetilemeyen** tek nicelik:

| | eski (düşen) | yeni (yürürlükte) |
|---|---|---|
| $y$ | $r_{ham} - r_{koş}$ | dört protokolün ürettiği **asimetri yayılımı** (puan) |
| $x$ | hedefin temiz hatası | çiftteki **iki modelin temiz doğruluk FARKI** |
| durum | özdeşlik → türetilir | **ampirik, bilinmiyor** |

Gerekçe metinde zaten duruyor: tartışma bölümü *"hâlâ belirtemediğimiz şey bu
bağımlılığın işlevsel biçimidir"* diyor. E3 tam olarak onu ölçecektir.

### B.3 İki kol (havuzlama YASAK — bu kural DEĞİŞMEDİ)

- **A kolu — kontrollü (yörünge-içi).** Çiftin bir üyesi SABİT tutulur, diğeri
  kendi yörüngesi boyunca taranır. Temiz doğruluk farkı değişir, mimari ·
  tohum · veri kümesi · saldırı bütçesi **değişmez**. Nedensel yorum bu koldan
  gelir.
- **B kolu — gözlemsel.** Farklı mimariler, tohumlar ve veri kümeleri
  (CIFAR-10 · CIFAR-100 · SVHN · WRN referansı). Fark değişirken **her şey**
  değişir.
- **Manşet, iki kolun eğimlerinin UYUŞMASIDIR.** Havuzlanmış tek bir uydurma
  **üretilmeyecektir**; kodda o çıktı yolu bulunmayacaktır.

### B.4 Değişmeyen tasarım kararları

- Kantil seçimi terk edildi; yörüngenin **tüm** checkpointleri (`--stride` ile
  seyreltilebilir, seyreltme **raporlanır**).
- Çıkarım **yörünge düzeyi küme bootstrap** ($B=10.000$). Nokta sayısı büyük
  olsa da **serbestlik derecesini yörünge sayısı belirler**; metinde açıkça
  yazılacak, yoksa "n=863" sahte kesinlik izlenimi verir.
- EK A'nın ölçtüğü **iki delik** (%17,68-23,28 ve %42,28-56,40) şekilde
  görünür kılınacak; o bantlarda eğim interpolasyondur.

### B.5 Özdeşlik büsbütün atılmıyor

E3, özdeşliğin **artığını** ikincil bir çıktı olarak raporlayacaktır: artık
sıfırdan anlamlı ölçüde sapıyorsa bu, "temiz-yanlış örnekler saldırı altında
yanlış kalır" öncülünün bozulduğu bir rejim demektir ve **kendi başına**
raporlanması gereken bir bulgudur (K8).

---

## EK C — E3'ün ölçtüğü nicelik YANLIŞTI; düzeltildi ve gerçek bulgu çıktı (2026-08-21)

**Salt-ekleme.** EK B'nin ilan ettiği tasarım ile KOD arasındaki uyuşmazlık
ölçülerek bulundu; aşağıda önce uyuşmazlık, sonra düzeltme, sonra ortaya
çıkan bulgu var.

### C.1 Uyuşmazlık — ilan edilen tasarım uygulanmamıştı

EK B.2 şunu ilan etmişti:

| | ilan edilen |
|---|---|
| $y$ | dört protokolün ürettiği **asimetri** yayılımı |
| $x$ | çiftteki iki modelin temiz doğruluk **farkı** |

Kod ise başka bir şey hesaplıyordu: $y$ = **tek bir yön** için dört protokol
oranının açıklığı, $x$ = **hedefin** temiz hatası. Bu, makalenin manşet
niceliğiyle aynı tür değildir: CIFAR-100'de manşet yayılım 13,58 puan iken
tek-yön açıklığı 37 puan mertebesindedir.

### C.2 Uyuşmazlık neden önemliydi — ölçüldü

Üretici: `scripts/q1_e3_spread_teshis.py` → `results/q1/e3_spread_teshis.json`

Tek-yön açıklığının **ortalama %82,1'i** (aralık %59,7–95,2) özdeşlik
terimidir ($r_{ham}-r_{koş}=e(1-r_{koş})$, bkz. EK B / EK J).

| nicelik | eğim ($x$ = hedefin temiz hatası) | $r$ |
|---|---|---|
| tek-yön yayılımı | 0,608 | 0,934 |
| özdeşlik terimi | 0,669 | 0,971 |
| **özdeşlik çıkarılınca artık** | **0,070** | **0,117** |

Yani B kolunun ilk sonucu (eğim 0,608) **aritmetiği yeniden ölçüyordu**;
ampirik içerik sıfıra yakındı.

### C.3 Düzeltme — doğru nicelik kuruldu (yeni GPU koşumu GEREKMEDİ)

`scripts/q1_e3_asimetri.py` mevcut nokta json'larını **yöne göre eşleştirip**
asimetriyi ve onun protokoller arası yayılımını kurar.

**Doğrulama:** kurgu, makalenin yayımlanmış sayılarını yeniden üretiyor —
CIFAR-10 ana çifti 11,31 / 10,17 / 9,86 (rapor: 10,45) ve CIFAR-100 ana çifti
15,01 / 14,04 / 11,68 → **ortalama 13,58** (rapor: 13,58). Yani eşleştirme
doğru kuruldu.

**Dengesizlik giderildi.** İlk koşumda WRN içeren bütün çiftler CIFAR-100'den
geliyordu; CIFAR-10'un 3×3 artefaktlarında `source_adv_wrong` alanı yoktu
(eski şema, `4fb006a` öncesi). Alan **köşegenden yeniden kuruldu**
(src→src beyaz kutusu = kaynağın kendi çekişmeli örneğine yenilmesi) ve
yöntem CIFAR-100'de **18/18 yönde bayt-eşit** doğrulandı
(`scripts/q1_e3_bkolu_c10_wrn.py`). Orijinal npz'ler değiştirilmedi.
Nokta sayısı 12 → **18 eşleşmiş çift / 6 küme**, iki veri kümesi de WRN
çiftleri katıyor.

### C.4 BULGU — mekanizma anlatısı EKSİK

Üretici: `scripts/q1_e3_surucu_ayristir.py` → `results/q1/e3_surucu_ayristirma.json`

| $y$ | eğim ($x$ = çiftin temiz hata farkı) | $r$ | GA%95 (küme bootstrap) |
|---|---|---|---|
| **4 protokol** yayılımı | **−0,567** | −0,531 | [−0,757; −0,451] |
| **3 protokol** (başarılı-kaynak HARİÇ) | **+0,431** | +0,840 | [+0,333; +0,633] |

İşareti çeviren tek şey **başarılı-kaynak** protokolüdür: 18 çiftin 12'sinde
uç (minimum) odur ve en geniş protokol çifti hep onu içerir
(hedef-doğru ↔ başarılı-kaynak: ortalama 19,68 puan).

**En büyük yayılım, hata farkı ~0 olan çiftlerde çıkıyor** — ve bu iki veri
kümesinde de tekrarlanıyor: CIFAR-10'da ResNet↔WRN farkı 3,4–4,1 puanken
yayılım 33,3–34,2; CIFAR-100'de fark 0,6–1,0 puanken yayılım 22,7–26,6.

**Yürürlükteki hüküm:**

> Protokol yayılımının **iki** sürücüsü vardır. Birincisi hedeflerin temiz
> hata farkıdır ve üç protokol (ham, hedef-doğru, her-ikisi-doğru) için
> geçerlidir; bu bileşen özdeşlikten **türetilebilir** (öngörü artığı: mutlak
> ortalama 0,046, en çok 0,16 puan). İkincisi **başarılı-kaynak** protokolüdür;
> **kaynağın kendi gürbüzlüğüne** bağlıdır, temiz hata farkından türetilemez
> ve tek başına ilişkinin işaretini çevirecek kadar güçlüdür.

Makalenin tartışma bölümündeki *"yayılım hedefler arasındaki temiz doğruluk
farkından kaynaklanır"* ifadesi bu yüzden **eksiktir** ve dört protokolün
tamamı raporlanırken **yanlıştır**. Düzeltilecektir.

### C.5 Sınırlamalar (rapor edilecek)

- 18 çift / **6 küme**; serbestlik derecesini küme sayısı belirler.
- WRN harici bir modeldir (farklı reçete, ek veri); küçük-fark çiftlerinin
  hepsi WRN içerir, dolayısıyla "küçük fark" ile "farklı reçete" bu havuzda
  tam ayrıştırılamaz. E5 (kapasite çifti) koşulursa ayrışır.
- EK A'nın ölçtüğü iki delik (%17,68–23,28 ve %42,28–56,40) burada da geçerli.

---

## EK D — Şekil, delikler ve A kolunun kaldıraç sınaması (2026-08-21)

**Salt-ekleme.** Bu ek, E3 şekli hazırlanırken yakalanan bir hatayı ve iki
ölçümü kaydeder. (Commit `4b24290`'in mesajı kabuk tarafından kesildiği için
kayıt buraya alınmıştır.)

### D.1 [DÜZELTME] Şekil YANLIŞ EKSENİN deliklerini çiziyordu

`scripts/q1_e3_figur.py`'nin ilk sürümü, EK A'nın ölçtüğü iki deliği
(%17,68–23,28 ve %42,28–56,40) gri bant olarak çiziyordu. **O delikler
hedefin temiz hatası eksenindedir**; şekil ise EK C'den sonra **çiftin hata
farkı** eksenini kullanmaktadır. İkisi aynı birimde (puan) olduğu için
bantlar makul görünüyordu ama **başka bir niceliğin** boşluklarını
işaretliyorlardı.

EK A'nın bağlayıcı şartı *"ölçülmemiş bölgeler görünür olsun"*dur ve o şart
**kullanılan eksende** sağlanmalıdır. Delikler artık noktaların kendi $x$
değerlerinden hesaplanmaktadır.

### D.2 Kullanılan eksende ölçülen delikler

| kol | $x$'te ölçülmemiş aralıklar (puan) |
|---|---|
| A (kontrollü) | 13,7–16,0 · **18,4–26,8** · 26,9–29,1 |
| B (gözlemsel) | 1,0–3,4 · **4,1–11,3** · 13,0–15,4 · 16,5–18,6 |

**Bu, B kolunun negatif eğimi için ciddi bir sınırlamadır.** O eğim,
$x \approx 4{,}1$ ile $11{,}3$ arasındaki **7,2 puanlık boşluğun üzerinden**
geçmektedir: küçük-fark çiftleri (hepsi WRN'li) ile büyük-fark çiftleri
arasında **hiç veri yoktur**. Yani "yayılım fark büyüdükçe azalıyor" ifadesi
iki ayrık kümenin karşılaştırılmasıdır, sürekli bir eğilim ölçümü değil.
Raporlanacaktır (K8).

### D.3 A kolunun KALDIRAÇ sınaması

Şekil bir kaldıraç sorunu gösterdi: A kolu noktalarının çoğu $x = 10$–$13$'te
kümelenmiş, eğimi taşıyan ise $x = 27$–$29$'daki birkaç nokta — ve onlar
yörüngelerin **ep1**'idir, yani neredeyse hiç eğitilmemiş modeller.
"Kontrollü kol" etiketi bunu gizlememelidir.

Ölçüm (`q1_e3_iki_kol_fit.py` → `A_KALDIRAC_DUYARLILIGI`):

| alt küme | $n$ | $x$ aralığı | 4 protokol eğimi | 3 protokol eğimi |
|---|---|---|---|---|
| tam | 45+ | 7,8–29,1 | **+0,606** | +0,774 |
| ep ≥ 2 | 50 | 9,5–18,4 | +0,555 | +0,792 |
| ep ≥ 10 | 50 | 9,5–18,4 | +0,555 | +0,792 |
| ep ≥ 20 | 45 | 10,6–16,0 | +0,418 | +0,853 |

**İşaret korunuyor:** A kolunun pozitif eğimi erken checkpoint'lerin eseri
değildir. Ancak erken epoklar çıkarıldığında $x$ aralığı 10,6–16,0'a
**daralmaktadır** ve bu daralma da yazılacaktır.

### D.4 Şeklin uyduğu bağlayıcı şartlar

- Kollar **ayrı panelde**; havuzlanmış tek bir uydurma **çizilmez** (B.3).
- Her panelde **iki seri**: 4 protokol ve 3 protokol (başarılı-kaynak hariç),
  EK C'nin ayrıştırdığı iki sürücü aynı yerde görünsün diye.
- Altyazıda $n=\langle\text{nokta}\rangle$ **değil** küme sayısı yazılır.
- Ölçülmemiş bantlar gri ile işaretlenir (D.1–D.2).

### D.5 Yürürlükteki uyarı

A kolu bu ek yazılırken **hâlâ koşuyordu** (3 küme). Küme bootstrap 2–3 kümede
dejenere olur (GA [+0,583; +0,651] gerçekçi olamayacak kadar dardır).
**Küme sayısı 6–8'e çıkmadan A kolu güven aralıkları kullanılmayacaktır.**

---

## EK E — E3 NİHAİ SONUÇ (2026-08-21, SVHN dahil tüm veriyle)

**Salt-ekleme.** EK C/D'deki ara değerler SVHN çiftleri eklenmeden önceydi;
aşağıdakiler **yürürlüktedir** ve makaleye bunlar yazılır.

Üretici: `scripts/q1_e3_iki_kol_fit.py` → `results/q1/e3_iki_kol_fit.json`
Şekil: `paper/figures/raw/fig_e3_kalibrasyon.pdf` (`scripts/q1_e3_figur.py`)

$x$ = çiftin temiz hata farkı (puan) · $y$ = **asimetrinin** protokoller arası
yayılımı (puan). Çıkarım **küme** düzeyi bootstrap ($B=10.000$).

### E.1 Kollar (havuzlanmış uydurma ÜRETİLMEDİ)

| kol | $n$ / küme | $x$ aralığı | 4 protokol | 3 protokol (baş.-kaynak hariç) |
|---|---|---|---|---|
| **A** kontrollü (yörünge içi) | 116 / **8** | 0,89–30,31 | **+0,294** [+0,206; +0,489] | **+0,672** [+0,601; +0,726] |
| **B** gözlemsel (final modeller) | 18 / 6 | 0,59–22,29 | **−0,567** [−0,757; −0,451] | **+0,431** [+0,333; +0,633] |
| B, WRN'siz alt küme | 6 / 6 | 11,27–22,29 | +0,387 [+0,075; +0,576] | +0,546 [+0,398; +0,837] |

### E.2 Manşet — iki kolun eğimlerinin uyuşması

- **Üç protokolde UYUŞUYOR:** A [+0,601; +0,726] ile B [+0,333; +0,633]
  örtüşüyor, işaretler aynı. Kontrollü ve gözlemsel kanıt **aynı yönü**
  veriyor: yayılım, çiftin temiz hata farkıyla **artıyor**.
- **Dört protokolde UYUŞMUYOR** (A pozitif, B negatif) — **ama sebep kontrol
  değil havuz bileşimidir.** A kolu yalnız ResNet↔ViT tarar, WRN içermez;
  B'yi aynı bileşime kısıtlayan alt küme **+0,387** verir ve A (+0,294) ile
  hem işaret aynıdır hem güven aralıkları örtüşür. Fit bunu
  `BILESIM_mi_KONTROL_mu` alanında raporlar.

### E.3 Sağlamlık

**Kaldıraç.** A kolunun eğimi erken checkpoint'lere bağlı değildir:

| alt küme | 4 protokol | 3 protokol |
|---|---|---|
| tam | +0,294 | +0,672 |
| ep ≥ 2 | +0,220 | +0,668 |
| ep ≥ 10 | +0,524 | +0,659 |
| ep ≥ 20 | +0,524 | +0,664 |

İşaret her alt kümede korunuyor. **3 protokol eğimi olağanüstü kararlı**
(0,659–0,672); asıl güvenilir nicelik odur.

**Özdeşlik artığı.** Her noktada hesaplandı; CIFAR'da ≤0,2 puan, CIFAR-100 ve
SVHN'in erken epoklarında 0,43'e kadar — hepsi açıklanan sapmanın çok altında.

### E.4 Bağlayıcı sınırlamalar (makaleye yazılacak)

1. **B kolunun negatif eğimi bir boşluğun üzerinden geçer.** $x$'te
   4,1–11,3 arası **boştur** (7,2 puan): küçük-fark çiftleri ile büyük-fark
   çiftleri arasında veri yoktur. O eğim sürekli bir eğilim ölçümü değil,
   **iki ayrık kümenin karşılaştırmasıdır**.
2. **Serbestlik derecesini küme sayısı belirler** (A: 8, B: 6). "n = 116
   nokta" biçiminde sunmak sahte kesinlik verir.
3. **Ölçülmemiş bantlar** şekilde gri ile işaretlidir
   (A: 4,8–7,8 · 23,4–25,9 — B: 1,0–3,4 · 4,1–11,3 · 13,0–15,4 · 16,5–18,6).
4. EK C.5'in "küçük fark ile farklı reçete ayrıştırılamıyor" sınırlaması
   **gevşedi**: SVHN çifti aynı mimari ve aynı tarifle eğitildi ve temiz hata
   farkı yalnız 1,85 puandır, yani küçük-fark bölgesinde artık WRN'siz bir
   çapa vardır.

### E.5 E7 ile bağımsız tutarlılık

E7'nin protokol yayılımı (`e7_transfer_summary.json`) bu kalibrasyonu
**bağımsız olarak** doğruluyor — E3'ün noktalarından değil, SVHN'in kendi
uçtan uca analizinden geliyor:

| veri kümesi | temiz hata farkı | protokol yayılımı |
|---|---|---|
| SVHN | ~1,85 | **3,65** |
| CIFAR-10 | ~11,3 | 10,45 |
| CIFAR-100 | ~21 | 13,58 |

Üçü de pozitif eğimle uyumludur ve ilişkinin **alt-doğrusal** olduğunu
göstermektedir (SVHN→CIFAR-10 eğimi ≈0,72; CIFAR-10→CIFAR-100 ≈0,32).
