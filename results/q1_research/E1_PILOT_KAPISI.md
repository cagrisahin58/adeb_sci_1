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

---

## EK D — pair2 kapandı (2026-08-19)

### D.1 Ölçülen sonuçlar (tohum ResNet 1002 / ViT 2002)

| | ResNet-18 | ViT-Tiny |
|---|---|---|
| AT en iyi val adv | %18,85 @ ep24 | %10,90 @ **ep11** |
| AT erken durma | ep44 | ep31 |
| Test temiz | **%64,67** | **%43,50** |
| Test PGD-10 | **%19,09** | **%10,48** |

### D.2 İki tohumun karşılaştırması (n=2, hüküm KURULMUYOR)

| | s1001/s2001 | s1002/s2002 | fark |
|---|---|---|---|
| ResNet temiz | 64,24 | 64,67 | 0,43 |
| ResNet PGD-10 | 19,14 | 19,09 | **0,05** |
| ViT temiz | 41,94 | 43,50 | 1,56 |
| ViT PGD-10 | 11,35 | 10,48 | **0,87** |

**B.7 sapma beyanı (devam):** her iki ViT tohumu da PGD-10 için ön-kayıtlı
%10-14 aralığının **içinde** (11,35 ve 10,48). Temiz doğruluk ise iki tohumda
da %33-40 aralığının **üstünde** (41,94 ve 43,50); EK C.3'te beyan edilen
sapma pair2'de teyit edilmiştir, yani tek koşumluk bir tesadüf değildir.

### D.3 B.6 tanısı — seçim yolları ayrışıyor, test sonucu ayrışmıyor (ResNet)

| | en iyi epok | durma epok |
|---|---|---|
| ResNet s1001 | 32 | 52 |
| ResNet s1002 | **24** | **44** |
| ViT s2001 | 7 | 27 |
| ViT s2002 | **11** | **31** |

ResNet'te iki tohum **farklı** checkpointlerde zirve yapıyor (ep32 vs ep24) ama
test PGD-10 farkı yalnız **0,05 puan**. Yani seçim *hangi* checkpoint'e
düştüğünü değiştiriyor, *sonucu* burada değiştirmiyor. Bu, E2'nin CIFAR-10
seçim-piyangosu bulgusuna **karşı-ağırlık** oluşturan bir gözlemdir ve
raporlanacaktır. ViT'te fark daha büyük (0,87 puan). n=2'de hüküm
kurulmamaktadır; pair3 beklenmektedir.

### D.4 Seçim piyangosu imzası ikinci tohumda tekrarlandı (post-hoc)

EK C.5(a)'daki gözlem ViT s2002'de de görülüyor:

| | plato bandı (ep3+) | genişlik | sd | ort | seçilen | ort'tan uzaklık |
|---|---|---|---|---|---|---|
| ViT s2001 | 9,65 - 11,05 | 1,40 | 0,397 | 10,34 | 11,05 | **+1,79 sd** |
| ViT s2002 | 8,90 - 10,90 | 2,00 | 0,517 | 9,82 | 10,90 | **+2,09 sd** |

İki tohumda da "en iyi checkpoint" seçimi, doğrulama platosunun ortalamasının
yaklaşık **2 standart sapma üstüne** düşüyor. Bu, seçim kuralının yapısal
sonucudur (maksimum alıyor), sürpriz değil; **sürpriz olan platonun
genişliği** — 1,4-2,0 puan, yani ViT'in mutlak gürbüzlüğünün ~%15-20'si
kadar. Ölçüm hâlâ **doğrulama düzeyindedir**; makaleye girecek biçim gerçek
10k test eğrisidir ve gereken kod B.8'de tespit edildiği gibi henüz yoktur.

---

## EK E — ResNet kolu tamamlandı (n=3); seçim yolu ile sonuç ayrışıyor

**2026-08-20.** Artefakt: `scripts/q1_e1_summary.py` →
`results/q1/e1_cifar100_summary.json`. Aşağıdaki hiçbir sayı elle girilmemiştir.

### E.1 ResNet-18 CIFAR-100, üç tohum

| tohum | test clean | test PGD-10 | en iyi epok | durma epoğu |
|---|---|---|---|---|
| 1001 | 64,24 | 19,14 | 32 | 52 |
| 1002 | 64,67 | 19,09 | 24 | 44 |
| 1003 | 62,67 | 19,67 | 49 | 69 |
| **ort ± sd** | **63,86 ± 1,05** | **19,30 ± 0,32** | açıklık **25** | açıklık **25** |

ViT kolu (n=2, s2003 koşuyor): temiz 42,72 ± 1,10 · PGD-10 10,91 ± 0,62.

### E.2 B.4 madde 1 için ilk girdi (yayılım karşılaştırması henüz YAPILAMAZ)

B.4'ün birinci doğrulayıcı ön-kestirimi CIFAR-100'de **transfer protokol
yayılımının** CIFAR-10'daki 10,45 puandan büyük olmasını gerektiriyor. Bu
ölçüm **henüz yapılmamıştır**: transfer matrisi ve protokol analizi E1
pipeline'ında koşmuyor, elle tetiklenecek (bkz. `Q1_KOSUM_KILAVUZU.md`).
Yukarıdaki sayılar yalnız mutlak performanstır ve B.4'ü **test etmez**.

### E.3 Seçim yolu çok oynak, sonuç değil — E2 manşetine olası sınır

ResNet'te üç tohum **çok farklı** noktalarda seçiliyor: en iyi epok 24 ile 49
arasında (25 epokluk açıklık), durma epoğu 44 ile 69 arasında. Buna karşılık
test PGD-10 standart sapması yalnız **0,32 puan**.

Yani bu yörüngelerde seçimin *nereye* düştüğü büyük ölçüde değişiyor ama
*sonuç* değişmiyor. Bu, E2'nin seçim-piyangosu manşetine (CIFAR-10'da mutlak
yayılım ResNet 2,62-2,85 / ViT 1,58-2,09 puan) **potansiyel bir sınır**dır ve
raporlanacaktır.

**AYNI DENEY DEĞİLDİR — aşırı yorum yasak.** Fark şudur:

- **E2:** *tek* yörüngeye *farklı seçim protokolleri* uygulanır. Yörünge
  sabit, değişen tek şey seçim kuralıdır.
- **Buradaki gözlem:** *farklı tohumlar*, her biri *kendi* yörüngesi ve
  *kendi doğal durma noktası* ile. Yörünge farkı ile seçim farkı iç içedir.

Dolayısıyla bu tablo E2'yi çürütmez; **E2 muadili ölçümün CIFAR-100'de
yapılması gerektiğini** gösterir. O ölçüm B.8'de tanımlıdır (tek yörüngeye
çevrimdışı seçim ızgarası + gerçek 10k test eğrisi) ve **kodu henüz yoktur**
(`scripts/q1_e2_test_curve.py` içinde `dataset="cifar10"` sabit).

**Bu belgeyle bağlayıcı hâle getirilen kural:** E2 manşeti makalede
raporlanırken, CIFAR-100'de seçim yolunun 25 epok oynamasına rağmen test
sd'sinin 0,32 puanda kalması **sınırlama olarak** yazılacaktır — B.8 ölçümü
yapılsın ya da yapılmasın. Bulgunun beğenilmemesi onu gizleme gerekçesi
değildir (B.3 dosya-çekmecesi taahhüdünün bu bulguya uzantısı).

### E.4 Ön-kayıt karşılaştırması (ResNet kolu için)

ResNet CIFAR-100 için §3'te ön-kayıtlı bir aralık **yazılmamıştı** (beklenti
tablosu yalnız ViT içindi; ResNet çapa olarak kullanılmıştı). Dolayısıyla
ResNet kolunda beyan edilecek bir sapma yoktur. Kayıt için: ResNet CIFAR-100
sonucumuz (63,86 temiz / 19,30 PGD-10) §3'te anılan Rice2020 PreActResNet-18
çapasıyla (%53,83 temiz / %18,95 AA) tutarlıdır — daha yüksek temiz, benzer
gürbüzlük.

---

## EK F — E1 eğitim aşaması KAPANDI (n=3, 2026-08-20)

Artefakt: `results/q1/e1_cifar100_summary.json` (üretici `scripts/q1_e1_summary.py`).

### F.1 Sonuçlar

| | ResNet-18 | ViT-Tiny |
|---|---|---|
| test clean | **63,86 ± 1,05** | **43,17 ± 1,10** |
| test PGD-10 | **19,30 ± 0,32** | **11,15 ± 0,60** |
| tohum değerleri (clean) | 64,24 · 64,67 · 62,67 | 41,94 · 43,50 · 44,06 |
| tohum değerleri (PGD) | 19,14 · 19,09 · 19,67 | 11,35 · 10,48 · 11,62 |
| en iyi epok | 32 · 24 · 49 (açıklık 25) | 7 · 11 · 20 (açıklık 13) |
| durma epoğu | 52 · 44 · 69 (açıklık 25) | 27 · 31 · 40 (açıklık 13) |

### F.2 B.7 ön-kayıt hükmü — NİHAİ

§3'te **veri görülmeden** yazılan beklenti tablosuna karşı:

| metrik | ön-kayıt | ölçülen (n=3) | hüküm |
|---|---|---|---|
| PGD-10 (test) | %10-14 | 11,15 ± 0,60; üç değer de aralıkta | **KESTİRİM TUTTU** |
| Temiz (test) | %33-40 | 43,17 ± 1,10; **üç değer de üstünde** | **SAPMA — beyan edildi** |
| AutoAttack | %8-11 | koşuyor | açık |

Temiz sapması EK C.3'te tek tohumla beyan edilmişti; **üç tohumda da**
gerçekleştiği için tesadüf değildir. Kestirim ResNet'in AT/ön-eğitim temiz
oranından (0,818) türetilmişti; ViT'te gerçekleşen oran ~0,91, yani ViT temiz
doğruluğunu çekişmeli eğitim altında ResNet'ten belirgin biçimde **daha iyi**
korudu. Bu, kestirimin dayanağının (mimariden bağımsız sabit oran) yanlış
olduğunu gösterir ve makalede böyle yazılacaktır.

### F.3 EK E.3'ün teyidi — seçim yolu oynak, sonuç değil

ViT kolunda da aynı desen: en iyi epok 7 ile 20 arasında (13 epokluk açıklık),
buna karşılık test PGD-10 sd'si **0,60 puan**. ResNet'te açıklık 25 epok,
sd 0,32 puan.

Yani **her iki mimaride de** seçimin düştüğü nokta tohumlar arasında büyük
ölçüde kayıyor ama test sonucu dar bir bantta kalıyor. EK E.3'te konan
bağlayıcı kural (E2 manşeti raporlanırken bu sınırın **sınırlama olarak**
yazılması) burada n=3 ile teyit edilmiştir.

Yeniden hatırlatma: bu, E2'nin ölçtüğü şeyin **aynısı değildir** (E2 tek
yörüngeye farklı seçim protokolleri uygular; burada her tohumun kendi
yörüngesi vardır). E2 muadili ölçüm B.8'de tanımlıdır ve kodu hâlâ yoktur.

### F.4 Sırada ne var

1. **AutoAttack** (pipeline koşuyor, pair1-3): ön-kayıtlı %8-11 beklentisi
   burada sınanacak.
2. **Transfer/protokol analizi** (`scripts/q1_e1_analysis.sh`): B.4'ün üç
   doğrulayıcı ön-kestirimi burada sınanacak. **E1'in tezle bağlantısı bu
   adımdadır**; F.1'deki mutlak sayılar B.4'ü test etmez.
3. WRN-28-10 CIFAR-100 referansı (Pang2022) indirildi ve matrise otomatik
   giriyor → 3×3 karıştırıcı analizi CIFAR-100'de de mümkün.
   **Kayda değer:** bu referansın temiz doğruluğu **63,64**, yani bizim
   ResNet-18'imizden (64,23) *düşük*. CIFAR-10'da tersiydi (89,48 vs 85,78).
   Dolayısıyla CIFAR-100 WRN'i E3'ün boş düşük-hata bandını **doldurmaz**
   (temiz hatası ~%36, aralığın ortası); E7-kısa kararının gerekçesi
   güçlenmiştir (bkz. `E3_YENIDEN_TASARIM.md` §2).

---

## EK G — B.4 ön-kestirimlerinin NİHAİ hükmü: üçü de doğrulandı (2026-08-20)

Artefaktlar: `results/q1/cifar100/transfer/e1_transfer_summary.json`,
`.../e1_c3_summary.json`, `results/q1/c3_precision.json`,
`.../pairN/a2b_class_balance_cifar100.json`.
Üretici zincir: `scripts/q1_e1_analysis.sh`.

### G.1 Ölçülen asimetriler (CIFAR-100, 3 tohum çifti)

| protokol | pair1 | pair2 | pair3 | ort |
|---|---|---|---|---|
| ham | +19,22 | +18,58 | +17,80 | +18,53 |
| hedef-doğru | +4,21 | +4,54 | +6,12 | +4,96 |
| her-ikisi-doğru | +11,15 | +10,53 | +11,09 | +10,92 |
| başarılı-kaynak | +9,85 | +11,04 | +13,44 | +11,44 |

**Protokol yayılımı: 13,58 ± 1,71 puan** (tohum başına 15,01 / 14,03 / 11,69).

### G.2 B.4 madde 1 — DOĞRULANDI

> Ön-kayıt: *"CIFAR-100'de dört koşullama protokolü arasındaki transfer
> asimetrisi yayılımı, CIFAR-10'daki 10,45 puandan **büyük** olmalıdır."*

Ölçülen **13,58 > 10,45**. Gerekçe de tuttu: koşullama temiz hatayla
ölçekleniyor ve CIFAR-100'de temiz hata çok daha büyük.

### G.3 B.4 madde 2 — DOĞRULANDI

> Ön-kayıt: *"CNN→ViT > ViT→CNN, dört protokolün dördünde de geçerli olmalı."*

**12/12 ölçümün tamamı pozitif** (4 protokol × 3 tohum). Yön, ikinci veri
kümesinde de korunuyor.

### G.4 B.4 madde 3 — YÖN DOĞRULANDI, ama kanıt gücü CIFAR-10'dakinden ZAYIF

> Ön-kayıt: *"Ham ve koşullu oranlar arasındaki sapma, hedefin temiz
> hatasıyla birlikte **artmalıdır** (CIFAR-10'da r = 0,997)."*

Ön-kestirim **yönseldir**, bir r değerine bağlanmamıştır. Eğim iki veri
kümesinde de pozitif: CIFAR-10 **+0,762**, CIFAR-100 **+0,656**. → **DOĞRULANDI.**

**Ancak kesinlik farkı belirgindir ve raporlanacaktır** (`q1_c3_precision.py`):

| | hedef temiz hataları | en küçük ara / aralık | etkin ayrık x | r (n=6) | %95 GA |
|---|---|---|---|---|---|
| CIFAR-10 | 10,52 · 14,21 · 26,47 | 0,23 | **3** | 0,9971 | [0,972; 0,9997] |
| CIFAR-100 | 36,15 · 36,36 · 56,83 | **0,010** | **2** | 0,9307 | [0,487; 0,993] |

CIFAR-100'de ResNet-18 (36,15) ile WRN-28-10 (36,36) referansının temiz
hatası **çakışıyor**. Yani korelasyon üç nokta üzerinden değil **iki küme**
üzerinden hesaplanıyor; doğrusal ilişki için güçlü kanıt sayılamaz ve %95
GA'sı [0,49; 0,99] ile neredeyse bilgisizdir. CIFAR-10'da üç hedef de ayrıktır.

**Bunun nedeni EK F.4'te kaydedilmişti:** CIFAR-100 WRN referansının temiz
doğruluğu (63,64) bizim ResNet-18'imizle (63,85 ort) neredeyse aynı; CIFAR-10'da
ise WRN belirgin biçimde daha yüksekti. Aynı olgu E3'ün boş düşük-hata bandını
da açıklıyor (bkz. `E3_YENIDEN_TASARIM.md` §2) ve E7-kısa kararının
gerekçesidir.

**Makale için zorunlu niteleme:** CIFAR-100 karıştırıcı analizi, CIFAR-10'daki
r = 0,997 sonucunun *yönünü* tekrarlar ama *kesinliğini* tekrarlamaz. İki r
yan yana konarken bu fark açıkça yazılacaktır.

### G.5 Ek not — makalenin mevcut r = 0,997 iddiası da nitelenmeli

`q1_c3_precision.py` bir yan bulgu üretti: köşegen-dışı **6 nokta 3 hedef ×
2 kaynaktan** gelir, yani x değişkeni yalnız 3 ayrı değer alır ve noktalar
bağımsız değildir. n=6 varsayan Fisher-z aralığı kesinliği **abartır**. Hedef
düzeyinde toplandığında n=3 olur ve Fisher-z aralığı **tanımsızdır**
(SE = 1/√(n−3)).

CIFAR-10 için r hedef düzeyinde 0,9985'tir, yani sonuç sağlamdır; ama
makalede r = 0,997 verilirken **"üç hedef üzerinde"** nitelemesi bulunmalıdır.
Bu, bu oturumda düzeltilen "kat değeri" ailesinin aynısıdır: az sayıda
bağımsız birimden hesaplanan bir istatistiği niteliksiz raporlamak.

### G.6 Sınıf bileşimi kontrolü (CIFAR-100)

`a2b_class_balance` üç çiftte de koştu; iki sağlama testi geçti (ham ve
her-ikisi-doğru protokollerinde iki yönün bileşimi tam özdeş, TV = 0).

Bileşim etkisi hedef-doğru protokolünde −1,249 / −1,330 / −1,065 puan
(asimetrinin %12,9-18,6'sı), başarılı-kaynakta ihmal edilebilir (%0,1-1,3).
CIFAR-10'da bu paylar %6-14 idi. **İşaret CIFAR-100'de de negatif**: sınıf
bileşimi farkı asimetriyi küçültüyor, yani gerçek sınıf-içi oran farkı
ölçülenden büyük. Koşullama asimetriyi bir örnekleme artefaktı olarak
üretmiyor.

### G.7 Post-hoc gözlem (ön-kestirim DEĞİL)

Protokollerin **sıralaması** veri kümeleri arasında değişiyor. CIFAR-10'da uç
değeri çoğunlukla başarılı-kaynak veriyordu; CIFAR-100'de üç çiftin üçünde de
**ham** veriyor ve başarılı-kaynak ortalarda kalıyor. Yani protokol seçimi
yalnız asimetrinin büyüklüğünü değil, **hangi protokolün uç değeri üreteceğini**
de veri kümesine bağlı olarak değiştiriyor. Ölçüm-protokolü tezini güçlendirir;
post-hoc olduğu için doğrulayıcı statüde sunulmayacaktır.

### G.8 E1'in hükmü

Üç doğrulayıcı ön-kestirimin **üçü de doğrulandı**. B.4'ün açık şartı
("karşılanmazlarsa E1 tezi desteklemiyor olarak raporlanır") tetiklenmedi:
**E1, ölçüm-protokolü bulgularının ikinci bir veri kümesinde korunduğunu
göstermektedir.** Kalan tek açık uç nokta AutoAttack'tır (ön-kayıt %8-11).

---

## EK H — E1 TAMAMEN KAPANDI (2026-08-20 01:28)

`logs/q1_e1.log`: `=============== Q1-E1 TAMAM ===============`

### H.1 Nihai sonuç tablosu (CIFAR-100, n=3)

| | ResNet-18 | ViT-Tiny |
|---|---|---|
| Temiz | **63,86 ± 1,05** | **43,17 ± 1,10** |
| PGD-10 | **19,30 ± 0,32** | **11,15 ± 0,60** |
| AutoAttack | **15,04 ± 0,54** | **8,87 ± 0,83** |

Tohum değerleri (AA): ResNet 14,75 · 14,71 · 15,67 — ViT 8,58 · 8,22 · 9,81.

McNemar (gürbüz, eşleştirilmiş, tam test kümesi) üç çiftte de ResNet lehine:
p = 8,5e-77 / 1,4e-87 / 3,0e-70.

### H.2 Ön-kayıtlı uç noktaların NİHAİ hükmü (§3 tablosu)

| metrik | ön-kayıt | ölçülen (n=3) | hüküm |
|---|---|---|---|
| PGD-10 | %10-14 | 11,15 (11,35 · 10,48 · 11,62) | **TUTTU** |
| AutoAttack | %8-11 | 8,87 (8,58 · 8,22 · 9,81) | **TUTTU** |
| Temiz | %33-40 | 43,17 (41,94 · 43,50 · 44,06) | **SAPMA, beyan edildi** |

Üç uç noktadan **ikisi tuttu**, biri üstten sapıp beyan edildi (EK C.3, F.2).
Sapmanın nedeni belgelendi: kestirim ResNet'in AT/ön-eğitim temiz oranından
türetilmişti; ViT o oranı korumadı (0,91'e karşı 0,82), yani "mimariden
bağımsız sabit taviz oranı" varsayımı yanlıştı.

**Not:** çekişmeli uç noktalar (asıl ilgi alanı) tuttu; tutmayan uç nokta
temiz doğruluktu ve sapma **iyi haber yönündeydi**. Ön-kayıtlı kestirimin
işe yaradığı, tam da yanlış çıktığı yerde bir mekanizma hatası ortaya
çıkardığı için gösterilebilir.

### H.3 AA/PGD oranı — post-hoc gözlem

| | AA/PGD | (CIFAR-10 karşılığı) |
|---|---|---|
| ResNet-18 | 15,04/19,30 = **0,779** | 37,93/44,11 = 0,860 |
| ViT-Tiny | 8,87/11,15 = **0,795** | 29,14/32,69 = 0,891 |

CIFAR-100'de PGD-10, gürbüzlüğü CIFAR-10'dakinden **daha fazla** abartıyor
(oran 0,78-0,80 vs 0,86-0,89). İki mimaride oran birbirine yakın, yani bu bir
mimari etkisi değil veri kümesi etkisi. Post-hoc; ön-kestirim değildir.

### H.4 E1'in nihai hükmü

- **B.3 dosya-çekmecesi taahhüdü** yerine getirildi: tüm sayılar, beğenilsin
  ya da beğenilmesin, kayda geçti.
- **B.4 doğrulayıcı ön-kestirimlerinin üçü de doğrulandı** (EK G).
- **B.5 bütçe kuralı** eşiği aşıldı (ViT PGD 11,35 ≥ 10,0), üç çift de koşuldu.
- **B.6 tanısı** ve **EK E.3 sınırı** kaydedildi: seçim yolu oynak, sonuç dar
  bantta; E2 manşeti raporlanırken sınırlama olarak yazılacak.
- **B.7 sapma beyanları** yapıldı (temiz doğruluk, iki kez: tek tohumda ve
  n=3'te).
- **B.8 vaadi** daraltılmış hâliyle açık: bölme-bootstrap replikasyonu için
  gereken kod (`q1_e2_test_curve.py --dataset`) hâlâ **yazılmadı**.

**E1 kapandı; tezle bağlantısı EK G'de kurulmuştur.** Kalan tek açık iş
B.8'in kodu ve makaleye yazım.
