# E1 Pilot Kapısı — Ön-Kayıt Eki

**Yazım zamanı: 2026-08-17 14:4x — ViT-Tiny CIFAR-100 AT eğitimi HENÜZ
BAŞLAMADI; hiçbir ViT adversarial sayısı görülmemiştir.** Bu ek, kapı
eşiklerini veri görülmeden sabitler (ara denetim, gidişat merceği bulgusu:
pipeline'a yazılan "%5" eşiği CIFAR-100 için yanlış ölçeklenmişti).

## 1. Neden eşik değişiyor

Pipeline'daki ilk kural "AT ilk 5 epok val adv-acc < %5 → DUR" idi. Ölçülen
çapa bunu geçersiz kılıyor:

- ResNet-18 CIFAR-100 AT, epoch 1: val adv **%11,10**; temiz taban val %78,5
  → oran ≈ 0,14.
- ViT-Tiny'nin temiz tabanı ~%46 (clean eğitim hâlâ sürüyor) → aynı oranla
  beklenen ep1 adv ≈ **%6,4**.
- Yani %5 eşiği beklenen değerin yalnız 1,4 puan altında. n=2000 ve p≈0,06'da
  binom SE ≈ 0,53 puan → marj ~2,6 SE; **yanlış DUR verme olasılığı ihmal
  edilebilir değil.**
- Diğer yönden %5, CIFAR-100'de şans seviyesinin (%1) 5 katı — yani kapı
  yalnızca *tam çöküşü* yakalar, "bilimsel olarak çok zayıf ama çökmemiş"
  ViT'i hiç görmez. CIFAR-10'da (şans %10) aynı eşik zaten anlamsızdı.

## 2. Yürürlükteki kapı (bu ekle sabitlenmiştir)

**SERT DUR kuralı** — ViT-Tiny CIFAR-100 AT, **epoch 5** val ölçümünde:

> `adv_acc < 3,0` (şansın 3 katı) **VEYA**
> `adv_acc < 0,10 × (clean ön-eğitim en iyi val doğruluğu)`
> → **koşumu DURDUR**, reçeteyi revize et (`--timm-pretrained` veya patch-4
> `vit_cifar_tiny` kolu), kararı bu belgeye ek olarak yaz.

**NİTELİK ÇUBUĞU (durdurmaz, işaretler)** — epoch 10'da:

> `adv_acc < 8,0` → reçete gözden geçirilir; koşum devam eder ama makalede
> "ViT kolu bu temel reçete altında zayıf kalmıştır" niteliği **açıkça**
> yazılır ve ViT kolu ikincil olarak raporlanır.

**Clean kapısı (değişmedi):** clean ViT-T val doğruluğu < %40 → DUR.
*(Şu anki ölçüm: epoch 38'de %42,05 → kapı hâlihazırda geçilmiş görünüyor;
final değer 200 epok sonunda kaydedilecek.)*

## 3. Veri görülmeden yazılan beklenti (ViT-Tiny CIFAR-100, bu reçete)

| Metrik | Beklenen aralık |
|---|---|
| Temiz (test) | %33-40 |
| PGD-10 (test) | %10-14 |
| AutoAttack | %8-11 |

Gerekçe/çapalar: ResNet-18 sonucumuz (temiz %64,24 / PGD-10 %19,14) Rice2020
PreActResNet-18 (ek veri yok: %53,83 temiz / %18,95 AA) ile tutarlı — daha
yüksek temiz, benzer gürbüzlük, yani klasik finetune-AT tavizi. CIFAR-100'de
sıfırdan eğitilmiş ViT-Tiny için doğrudan literatür çapası **yoktur**;
yukarıdaki aralık ResNet oranından ve ViT'in temiz tabanından türetilmiştir.

**Kıyas notu (makalede zorunlu):** Debenedetti XCiT-S12'nin CIFAR-100'de
%32,19 AA'sı ile aramızda ~3 kat fark olacak — o model 26M parametre,
ImageNet ön-eğitimli, TRADES ve native-32 çözünürlüklü. "Bu temel reçete
altında" niteliği CIFAR-100 için **açıkça tekrarlanacaktır**.

## 4. E1'in rolü (veri görülmeden daraltılmıştır)

Ara denetim, E1'in ön-kayıtlı kestiriminin neredeyse totolojik olduğunu ve
ViT kolunun zayıf çıkmasının beklendiğini saptadı. Bu yüzden E1'in rolü
şimdiden daraltılıyor:

- E1'in **birincil** işlevi: ölçüm-protokolü bulgularının **ikinci bir veri
  kümesinde yönünün korunup korunmadığını** göstermek (genelleme kontrolü).
- E1 **mutlak gürbüzlük yarışması olarak sunulmayacak**; CNN-ViT mutlak farkı
  bu reçetenin sonucu olarak raporlanacak, mimari üstünlüğü iddiası
  kurulmayacak.
- E1'in save_every=1 checkpointleriyle **E2'nin seçim-piyangosu ölçümü
  CIFAR-100'de replike edilecek** (~5 GPU-saat, bedava kazanç) — bu, E1'in
  tez açısından en değerli çıktısı olacaktır.

---

## EK A — Kapı kararı (ölçüm anında yazılmıştır, 2026-08-17 ~19:07)

**Kapı noktası: ViT-Tiny s2001 CIFAR-100 AT, epoch 5.**

Ölçülen: `Clean: 40.00%`, `Adv: 10.40%` (val, n=2000, sabit bölme).

| Ön-kayıtlı eşik (§2) | Değer | Ölçüm | Hüküm |
|---|---|---|---|
| SERT DUR: `adv < 3,0` (şansın 3 katı) | 3,000 | 10,40 | **GEÇTİ** |
| SERT DUR: `adv < 0,10 × temiz-taban` | 4,745 | 10,40 | **GEÇTİ** |
| Clean kapısı: temiz val < %40 | 40,00 | 47,45 (temiz ön-eğitim en iyi) | **GEÇTİ** |

**KARAR: koşum DEVAM EDİYOR.** Reçete revizyonu (`--timm-pretrained` / patch-4
`vit_cifar_tiny`) tetiklenmedi.

**Kapının gevşek olmadığının kanıtı — ölçülen orana bakılmadan yazılmış eşikle
karşılaştırma:** ep5'te ViT'in adv/temiz-taban oranı 10,40/47,45 = **0,219**;
ResNet-18'in aynı epoktaki oranı 15,10/78,50 = **0,192**. Yani ViT, kapıyı
kuran ResNet çapasından *proporsiyonel olarak daha iyi* durumda. Eşik
(0,10) çapanın yaklaşık yarısına konmuştu; gerçekleşen oran çapanın üstünde
çıktı. Marj 2,2 kat.

**AT ilk beş epok yörüngesi (kayıt için):**

| epok | Loss | Clean | Adv |
|---|---|---|---|
| 1 | 3,5978 | 33,65 | 8,30 |
| 2 | 3,1510 | 38,25 | 9,00 |
| 3 | 3,0001 | 38,85 | 10,60 |
| 4 | 2,8830 | 40,20 | 10,30 |
| 5 | 2,7782 | 40,00 | 10,40 |

Temiz doğruluk ön-eğitim tabanından (%47,45) düşüp ~%40'ta stabilize oldu —
klasik AT tavizi; §3'te veri görülmeden yazılan "temiz (test) %33-40"
beklentisiyle tutarlı. Adv ep3'ten sonra ~%10,4'te plato yapıyor.

**HENÜZ AÇIK: ep10 nitelik çubuğu (§2).** `adv < 8,0` ise reçete gözden
geçirilir ama koşum durmaz. Ep5 değeri 10,40 olduğundan çubuğun aşılması
olası; yine de karar ep10 ölçümünde verilecek ve buraya EK B olarak
yazılacaktır. Ep5 değerine bakıp ep10 hükmü şimdi verilmemektedir.

---

## EK B — Kapı ölmüştür; yerine analiz-uygunluk kuralları (2026-08-17 ~19:35)

**Yazım zamanı: ViT-Tiny s2001 AT epoch 7 içinde. Görülen: yalnız ep1-7
doğrulama eğrisi. GÖRÜLMEYEN: hiçbir test-kümesi sayısı, hiçbir CIFAR-100
transfer/protokol ölçümü, pair2 ve pair3'ün hiçbir sayısı.**

### B.1 Kapının ölü olduğunun tespiti

Ara denetim (gidişat merceği) şunu saptadı ve doğruladım: **ep1'de adv = 8,30**
ölçüldü. Bu değer hem ep5 sert durma eşiğini (4,745) hem ep10 nitelik çubuğunu
(8,0) daha birinci epokta aşmıştı. Yani §2'deki kapı, ölçüm noktalarına
varmadan önce geçilmişti ve **hiçbir zaman bir karar üretmedi.** EK A'da
raporlanan "GEÇTİ" hükmü bu nedenle bir doğrulama değil, bir formalitedir.

**Ders (kayda geçiriliyor):** kapı, tedavinin *çökme* riskini ölçüyordu; oysa
bu reçetede gerçek risk çökme değil, **bilimsel olarak zayıf ama çalışan** bir
ViT koluydu. Eşik, ölçmesi gereken şeyin yanına konmuştu.

### B.2 Neden yeni bir DURDURMA kapısı kurulmuyor

ep1-7 verisi görülmüştür. Bu noktadan sonra kurulacak her durdurma eşiği o
veriye göre ayarlanmış olur — **kapı alışverişi (gate shopping)**. Ön-kayıt
disiplini bunu yasaklar ve zaten durdurma kararı veriyle kapanmıştır: çökme
riski yoktur. Bu yüzden §2'deki kapı **yürürlükten kaldırılmıyor, ölü ilan
ediliyor**; yerine aşağıdaki kurallar konuyor. Aşağıdakilerin hiçbiri
gözlenmiş bir büyüklüğe dayanmamaktadır.

### B.3 Dosya-çekmecesi taahhüdü (bağlayıcı)

ViT kolunun mutlak sayısı ne çıkarsa çıksın, **E1 çifti makalede raporlanır.**
Zayıf çıkması yayımlanmama gerekçesi değildir; E1 mutlak gürbüzlük yarışması
olarak değil, ölçüm-protokolü bulgularının yön kontrolü olarak kurulmuştur
(§4). Sonuç beğenilmediği için E1'in rafa kaldırılması bu belgeyle
yasaklanmıştır.

### B.4 Doğrulayıcı ön-kestirimler (hiçbiri ölçülmemiştir)

E1'in tezi desteklemesi şu üç uç noktaya bağlıdır. Karşılanmazlarsa **E1 tezi
desteklemiyor olarak raporlanır**, sessizce yeniden çerçevelenmez:

1. **Protokol yayılımı korunur ve büyür.** CIFAR-100'de dört koşullama
   protokolü arasındaki transfer asimetrisi yayılımı, CIFAR-10'daki
   $10{,}45$ puandan **büyük** olmalıdır. Gerekçe: koşullama, temiz hatayla
   ölçeklenir ve CIFAR-100'de temiz hata çok daha büyüktür.
2. **İşaret korunur.** CNN$\to$ViT $>$ ViT$\to$CNN, dört protokolün
   **dördünde de** geçerli olmalıdır.
3. **Karıştırıcı yeniden üretilir.** Ham ve koşullu oranlar arasındaki sapma,
   hedefin temiz hatasıyla birlikte artmalıdır (CIFAR-10'da $r = 0{,}997$).

### B.5 Bütçe kuralı — gerçekten açık olan tek karar

pair2 ve pair3 (~24 GPU-saat) koşulacak mı? **Ön-kayıt:** pair1'in ViT test
PGD-10 değeri

- **$< 10{,}0$** ise → E1 **yalnız yön kontrolü** olarak raporlanır (B.4'ün
  2. ve 3. maddeleri), ama **pair2/pair3 yine koşulur**: yayılımın kendisi
  için $\sigma$ gerekir ve tek çift $\sigma$ vermez.
- **$\geq 10{,}0$** ise → E1 ayrıca CIFAR-100 $\sigma$'sını da besler ve
  yayılım karşılaştırması (B.4 madde 1) nicel olarak raporlanır.

Her iki dalda da pair2/pair3 koşulmaktadır; değişen şey **E1'in taşıdığı
iddianın gücüdür**, koşum kapsamı değil.

### B.6 Gürbüz aşırı-öğrenme tanısı (durdurmaz, raporlanır)

ViT için: en iyi epok indeksi, son epok indeksi, ve patience-20'nin ep40
öncesinde ateşleyip ateşlemediği kaydedilir. ResNet s1001 ep52'de durdu;
iki kolun durma davranışı farklıysa bu, seçim-protokolü tartışmasının
CIFAR-100 ayağı olarak raporlanır.

### B.7 Ön-kayıt sapması olarak beyan edilecek durum

§3'te ViT PGD-10 test beklentisi **%10-14** yazılmıştı. Doğrulama eğrisi ep7'de
zaten 11,05'tedir ve ResNet çapasında doğrulama ile test birbirine yakın
çıkmıştı (val-best 18,85 → test 19,14). **Beklenti aralığının üstten aşılması
olasıdır.** Aşılırsa bu, iyi haber olsa dahi **ön-kayıt sapması olarak açıkça
beyan edilecek**, sessizce geçilmeyecektir.

### B.8 §4'teki vaadin düzeltilmesi (teslim edilemez olduğu tespit edildi)

§4 son maddesi "E1'in save_every=1 checkpointleriyle **E2'nin seçim-piyangosu
ölçümü** CIFAR-100'de replike edilecek" diyordu. Ara denetim bunun **tasarım
gereği teslim edilemez** olduğunu gösterdi; doğruladım:

- **Tek doğrulama bölmesi.** E1 tek bir 2000'lik bölme kullanıyor; E2'nin
  manşeti **iki temiz bölme** (V_B/V_C) üzerineydi. Izgaranın baskın boyutu
  (bölme × patience) tek bölmeyle yok oluyor.
- **Yörünge kesik.** ResNet CIFAR-100 patience-20 ile **ep52**'de durdu
  (E2: 100 epok, patience KAPALI). Çevrimdışı ızgara ep52 sonrasını simüle
  edemez; üstelik kesme noktasını, ızgaranın değiştirmesi gereken bölmenin
  kendisi belirledi.
- **Kalan boyutlar E2'nin diskalifiye ettikleri.** Geriye patience × yumuşatma
  kalıyor; E2 patience'ı ViT'te fiilen atıl, yumuşatmayı ise nötr alternatif
  değil **monoton olarak daha kötü** bir seçici ilan etti.

**Vaat şu şekilde daraltılmıştır:** E1'in seçim-protokolü katkısı
**bölme-çekilişi bootstrap'inin ikinci veri kümesinde replikasyonu** olacaktır
(tek bölme yeterlidir; E2'nin en dayanıklı niceliksel çıktısı budur).
Bunun için iki kod değişikliği gerekiyor ve **henüz yoktur**:
`scripts/q1_e2_test_curve.py` içindeki sabit `dataset="cifar10"` bir bayrağa
çevrilmeli, `scripts/q1_e2_split_bootstrap.py` tek-bölme varyantı yazılmalı.
Tahmini maliyet ~5-6 GPU-saat.

### B.9 Bilinen sınırlama (kayda geçiriliyor)

E1'de AT, `best.pth`'ten başlıyor (E2 bilinçli olarak `last.pth` kullanmıştı)
ve temiz seçim ile AT seçimi **aynı 2000'lik bölmeyi** paylaşıyor. Yani
CIFAR-100 yörüngesinin başlangıç noktası da o bölmeyle seçilmiştir. C1 ile
tutarlıdır ve makalenin beyanına uygundur, ancak bölme-bootstrap replikasyonu
raporlanırken **sınırlama olarak yazılacaktır**.

### B.10 Uygulama notu

§2'deki kapı `scripts/q1_pipeline.sh` içinde **kod olarak uygulanmamıştır**
(yalnız pair1 bittikten sonra bir log satırı basılır) ve betiğin yorumları
hâlâ terk edilmiş `%5` eşiğini anmaktadır. Betik **şu anda koşmakta** olduğu
için düzenlenmiyor (bash betikleri artımlı okur; koşan betiği düzenlemek
yürütmeyi bozar). Koşum bittiğinde bu yorumlar temizlenecektir.

---

## EK C — pair1 kapandı: ön-kayıtlı kuralların uygulanması (2026-08-19)

### C.1 Ölçülen sonuçlar (pair1, tohum ResNet 1001 / ViT 2001)

| | ResNet-18 | ViT-Tiny |
|---|---|---|
| Temiz ön-eğitim (en iyi val) | %78,50 | %47,45 |
| AT en iyi val adv | %18,85 @ **ep32** | %11,05 @ **ep7** |
| AT erken durma | **ep52** | **ep27** |
| Test temiz | **%64,24** | **%41,94** |
| Test PGD-10 | **%19,14** | **%11,35** |

### C.2 B.5 bütçe kuralı — HÜKÜM

Ön-kayıt: pair1 ViT test PGD-10 `< 10,0` ise E1 yalnız yön kontrolü; `>= 10,0`
ise E1 ayrıca CIFAR-100 sigma'sini da besler.

Ölçülen: **11,35 >= 10,0** → **E1, yayılım karşılaştırmasını (B.4 madde 1)
nicel olarak raporlar.** pair2/pair3 zaten her iki dalda da koşulacaktı;
değişen şey E1'in taşıdığı iddianın gücüdür. Koşum kapsamı değişmiyor.

### C.3 B.7 ön-kayıt sapma beyanı — İKİ HÜKÜM

Sapmaların sessizce geçilmemesi bağlayıcıydı. İki uç nokta için ayrı hüküm:

- **PGD-10 test: SAPMA YOK.** Ön-kayıt %10-14; ölçülen **11,35** → aralık
  içinde. §3'te ResNet oranından türetilen kestirim tuttu.
- **Temiz test: SAPMA VAR, BEYAN EDİLİYOR.** Ön-kayıt %33-40; ölçülen
  **41,94** → üst sınır **1,94 puan aşıldı**. Sapma ön-kayıt yönünde iyi
  haberdir (beklenenden güçlü temiz doğruluk), ancak B.7 uyarınca açıkça
  kaydedilmektedir. Kestirimin dayanağı ResNet'in AT/ön-eğitim temiz oranıydı
  (0,818); ViT'te gerçekleşen oran 41,94/47,45 = **0,884**, yani ViT temiz
  doğruluğunu AT altında ResNet'ten daha iyi korudu.

### C.4 B.6 gürbüz aşırı-öğrenme tanısı

| | en iyi epok | durma epok | ep40 öncesi mi? |
|---|---|---|---|
| ResNet-18 | 32 | 52 | hayır |
| ViT-Tiny | **7** | **27** | **evet** |

İki kolun durma davranışı belirgin biçimde farklıdır: ViT zirvesini
**ep7'de** yapıp patience-20 ile ep27'de durdu; ResNet ep32'de zirve yapıp
ep52'de durdu. B.6 uyarınca bu fark, seçim-protokolü tartışmasının CIFAR-100
ayağı olarak raporlanacaktır.

### C.5 SONRADAN GÖZLENEN (post-hoc — ön-kestirim DEĞİL, öyle sunulmayacak)

Aşağıdaki iki gözlem ölçüm sonrası yapılmıştır ve **ön-kayıtlı kestirim
olarak sunulmaları yasaktır**. Doğrulayıcı statü kazanmaları için pair2/pair3
gerekir.

**(a) Seçim piyangosu doğrulama düzeyinde tekrarlandı.** ViT'in AT doğrulama
eğrisi ep3-27 arasında dar bir gürültü bandında salınıyor:

- band: **%9,65 - %11,05**, genişlik **1,40 puan**, sd **0,397**, ort **10,34**
- "en iyi checkpoint" seçimi bandın **tepesine** düşüyor (11,05), yani
  ortalamanın ~**1,8 sd** üstüne
- 11,05 değeri ep7 ve ep12'de iki kez görülüyor; min_delta=0,1 eşiği
  nedeniyle ikincisi "iyileşme" saymıyor ve seçim ep7'de kalıyor

Bu, E2'nin CIFAR-10'daki seçim-piyangosu bulgusuyla aynı yapıdadır. **ANCAK
doğrulama düzeyindedir.** Makaleye girecek biçim, E2'nin P0 yaklaşımıyla
aynı olmalıdır: 27 checkpoint'in **gerçek 10k test** eğrisi. Bunun için
gereken kod B.8'de tespit edildiği üzere **henüz yoktur**
(`scripts/q1_e2_test_curve.py` içinde `dataset="cifar10"` sabit).

**(b) Mutlak fark büyük ölçüde temiz tabandan geliyor.** PGD-10'un temiz
ön-eğitim tabanına oranı iki mimaride neredeyse özdeş:

- ResNet: 19,14 / 78,50 = **0,244**
- ViT: 11,35 / 47,45 = **0,239**

Yani CIFAR-100'de ViT'in mutlak gürbüzlük dezavantajı, aynı oranla ölçekleyen
bir temiz-doğruluk dezavantajıdır. Bu, makalenin koşullu-ayrıştırma tezinin
(mutlak farkın büyük kısmı temiz farktan) ikinci veri kümesindeki karşılığıdır
— ama **tek çift üzerinde** ölçülmüştür ve iki oranın yakınlığı tesadüf
olabilir. sigma olmadan iddia kurulmayacaktır.
