# B2 — `successful_source` protokol düzeltmesi: DURUM ve DEVAM

> **KAPANDI — 2026-08-25.** A kolu 116/116 noktayla yeniden koşuldu, iki-kol
> uydurması ve şekil yeni koldan üretildi, metin iki dilde işlendi.
> **Altı kapının altısı da geçiyor** (`bash scripts/kapilar.sh`).
> Aşağıdaki kayıt neyin neden yapıldığını saklar; §6'daki komutlar artık
> yeniden üretim içindir, yarım kalan iş için değil.
>
> Kapanış ölçümleri: köken defteri 44 artefakt / 0 eksik · derleme EN 21 s.,
> TR 20 s., bildiri 6 s., üçünde de 0 undefined · öz-sınamalar: iddia tabanı
> KALAN=0 ve altı kol, özet dört kol, bildiri altı kol, ayna dört kol.

---

## 1. Kusur neydi

Makale (Bölüm 3.5) protokolü şöyle tanımlıyor: *"saldırının kaynakta **beyaz
kutu anlamında başarılı** olduğu hedef-doğru örnekler."* Kod ise sekiz ayrı
dosyada şunu hesaplıyordu:

| | maske |
|---|---|
| **metin** (doğru) | `target_clean_correct & source_clean_correct & source_adv_wrong` |
| **kod** (yanlış) | `target_clean_correct & source_adv_wrong` |

Gevşek maske, kaynağın **temizde zaten yanıldığı** örnekleri de payda alıyordu;
orada "başarılı olmuş bir saldırı" yoktur, önceden var olan bir hata vardır.
Makalenin kendi Tartışma bölümü bu protokolü "zaten işe yaramış bir saldırının
ne kadar taşındığı" diye tanımladığı için gevşek maske makalenin sorduğu soruyu
yanıtlamıyordu.

**Neden kod düzeltildi, metin değil:** tezi *"protokolünüzü tam yazın, protokol
sonucun parçasıdır"* olan bir makale, kendi yazdığı protokol ile kendi koştuğu
protokol ayrışmış hâlde gönderilemez.

---

## 2. Ölçülen etki

`raw`, `hedef doğru` ve **birincil saydığımız `her ikisi doğru` tanım gereği
değişmiyor.** Yalnız `başarılı kaynak` değişiyor.

| veri kümesi | başarılı kaynak (gevşek → sıkı) | yayılım (gevşek → sıkı) |
|---|---|---|
| CIFAR-10 $L_\infty$ | $+14{,}60\pm1{,}48 \rightarrow \mathbf{+19{,}37\pm1{,}27}$ | $10{,}45\pm0{,}76 \rightarrow \mathbf{15{,}01\pm0{,}84}$ |
| CIFAR-100 | $+11{,}44\pm1{,}82 \rightarrow \mathbf{+17{,}50\pm0{,}92}$ | $13{,}58\pm1{,}71 \rightarrow \mathbf{13{,}83\pm1{,}30}$ |
| SVHN | $+2{,}64\pm0{,}03 \rightarrow \mathbf{+2{,}70\pm0{,}40}$ | $3{,}65\pm0{,}19 \rightarrow \mathbf{3{,}70\pm0{,}62}$ |
| CIFAR-10 $L_2$ | $+9{,}51\pm0{,}89 \rightarrow \mathbf{+12{,}06\pm0{,}23}$ | $10{,}91\pm0{,}83 \rightarrow \mathbf{10{,}92\pm0{,}82}$ |

**SVHN işaret deseni değişmedi** (her iki varyantta 4/8 pozitif), yani
makalenin en çarpıcı bulgusu olan işaret çevrilmesi olduğu gibi duruyor.

### 2b. Düzeltmenin ZORLADIĞI iki geri adım (K8)

Düzeltme CIFAR-10 manşetini güçlendiriyor; bu yüzden zayıflattığı yerleri
açıkça yazmak şart:

1. **"Yayılım daralmıyor, genişliyor" anlatısı TERSİNE DÖNDÜ.** Eskiden
   CIFAR-100 (13,58) > CIFAR-10 (10,45) idi. Şimdi CIFAR-100 (13,83) <
   CIFAR-10 (15,01). Doğru ifade "genişliyor" değil, **"iki CIFAR veri
   kümesinde karşılaştırılabilir"**. Bölüm 4.4 paragraf başı, Bölüm 5 ve
   Sonuç bölümleri buna göre düzeltilmeli.
2. **$L_2$'de "aynı büyüklükte" ifadesi düştü.** 10,92'ye karşı 15,01. Zaten
   ön-kayıtın ötesinde bir süslemeydi: `E6_ON_KAYIT.md` Ö2 açıkça *"E6'nın
   işi yayılımın L∞'dakiyle aynı BÜYÜKLÜKTE olduğunu göstermek değil, norm
   değişince YOK OLMADIĞINI göstermektir"* diyor ve eşik 2 puandır. Ön-kestirim
   **tutuyor** (10,92 > 2), yalnız süsleme kalkacak.

---

## 3. Yol boyunca bulunan ÜÇ ayrı kusur

Hiçbiri B2'nin parçası değildi; yeniden üretim sırasında ölçüldü.

**(a) `a2`'de paylaşılan rastgele akış.** Tek bir modül düzeyi RNG'yi bütün
bootstrap'lar ve permütasyon testi paylaşıyordu. Beşinci protokolü eklemek,
ondan sonra gelen **alakasız** permütasyon testini kaydırdı (SVHN $p$
0,10465 → 0,10665). Düzeltme: her tüketici adına bağlanmış kendi akışını alır
(`_akis()`). Etki ölçüldü — GA kayması en fazla **0,03 puan**, **TOST
hükümlerinin hepsi aynı**, SVHN $p$ 0,105'te kalıyor. Hiçbir makale iddiası
değişmedi.

**(b) A kolunda adım-bağımlı sonuç.** PGD'nin `random_start`'ı tarama boyunca
tek akıştan çekiyordu; bir kontrol noktasının sayısı **ondan önce kaç nokta
tarandığına** bağlıydı. Ölçüldü: aynı yörünge stride=10 ve stride=50 ile
tarandığında ep1 birebir tutuyor (ilk çağrı), ep51/ep100 tutmuyor (ham oranda
0,16, hedef-doğruda 0,22 puana kadar). Yani yayımlanan bir noktayı yeniden
üretmek için **hangi adımla tarandığını bilmek** gerekiyordu. Düzeltme: her
nokta `(yörünge, epok)`'tan türetilen kendi tohumunu alır (`_ck_tohum`).
Sınandı: iki farklı adımla tarandığında ortak epoklar **birebir aynı**.

**(c) Protokol tanımı sekiz dosyada kopyalanmıştı.** Metin/kod ayrışmasına izin
veren şey buydu. Artık tek kaynak: `src/analysis/protokoller.py`. Bağlananlar:
`a2_transfer_protocols.py`, `a2b_class_balance.py`, `q1_e3_akolu.py`,
`q1_e3_bkolu.py`, `q1_e3_bkolu_c10_wrn.py`, `q1_e3_calibration.py`.

---

## 4. Kapsam kararı: SVHN'in B kolundaki yeri

SVHN transfer artefaktları artık tam şemalı olduğu için `q1_e3_bkolu.py` ilk
kez SVHN B kolu noktaları da üretti (36 → 40 nokta). Bunlar uydurmaya
**girmiyor**, çünkü `E3_YENIDEN_TASARIM.md` EK E.1 B kolunu 18 nokta / 6 küme
olarak sabitliyor ve EK E.5 SVHN'e ayrı bir rol veriyor: *"E3'ün noktalarından
değil, SVHN'in kendi uçtan uca analizinden gelen bağımsız tutarlılık
kontrolü."*

**Sonucu gördükten sonra bileşimi değiştirmek ön-kayıt disiplinini bozardı**
(K5). Bu yüzden kayıtlı bileşim korundu ve seçim koda yazıldı
(`q1_e3_asimetri.py`, `E3B_SVHN` değişkeni). Duyarlılık **raporlanacak**:

| bileşim | 4 protokol eğimi | GA95 |
|---|---|---|
| kayıtlı (18 çift / 6 küme) | $-0{,}528$ | $[-0{,}664;\ -0{,}418]$ |
| + SVHN (20 çift / 8 küme) | $-0{,}133$ | $[-0{,}570;\ +0{,}469]$ — **sıfırı içeriyor** |

Bu, makalenin **zaten yazdığı** "o eğim 7,2 puanlık ölçülmemiş bir boşluğun
üzerinden geçer, sürekli bir eğilim değil iki ayrık kümenin karşılaştırmasıdır"
uyarısının nicel karşılığıdır. Eklenmesi uyarıyı somutlaştırır.

---

## 5. Şu ana kadar YAPILAN

- [x] Tek kaynak modülü + altı betiğin bağlanması
- [x] Rastgele akış ayrımı (a2) + kayma ölçümü
- [x] Kontrol noktası başına tohumlama (A kolu) + adım-bağımsızlık sınaması
- [x] `a2` × 11 çift (CIFAR-10/100, SVHN, $L_2$) yeniden üretildi
- [x] Gerileme kontrolü: `raw`/`hedef doğru`/`her ikisi doğru` ve eşleşmiş
      analiz **birebir aynı**; gevşek varyant eski değeri **birebir** veriyor
- [x] Dört tohum toplulaştırması + sınıf bileşimi
- [x] B kolu noktaları, asimetri uydurması, sürücü ayrıştırması, yayılım
      teşhisi, $L_2$ ön-kestirimi, varyans oranı
- [x] `C1_REFERANS_FOYU.md` yeniden üretildi
- [x] Üç kaynak doğrulandı ve eklendi (TA-Bench NeurIPS 2023 · Waseda WACV
      2023 · Yu SaTML 2025 s. 797-810), iki dilde konumlandırıldı
- [x] Depo vaadi kapsamlandı (dört yerde; Sonuç bölümlerindeki şimdiki zaman
      "yayımlıyoruz" düzeltildi — depo kapalıyken yanlıştı)
- [x] Kapıya H1/H2 muhafızları

## 6. KALAN — iki komut

**(1) A kolunu bitir** (GPU, ~22/116 nokta hazır, kalan ~80 dk):

```bash
bash scripts/_b2_akolu_v2.sh          # atlayarak devam eder, 4 deneme
```

**(2) İki-kol uydurmasını ve şekli yeni A kolundan üret:**

```bash
docker exec -w /workspace adeb_eval env E3A_DIR=results/q1/e3_akolu_v2 \
    python -B scripts/q1_e3_iki_kol_fit.py
docker exec -w /workspace adeb_eval python -B scripts/q1_e3_figur.py
```

> `q1_e3_iki_kol_fit.py` ve `q1_e3_figur.py` hâlâ `results/q1/e3_akolu`
> yoluna çivili. Ya yolu parametreleştirin ya da v2'yi yerine koyun.
> Yerine koyarken **eski dizini silmeyin**, `e3_akolu_v1_gevsek` olarak
> saklayın: gevşek değerler `asimetri_gevsek_successful_source` alanında
> yeni dosyalarda da duruyor, ikisi karşılaştırılabilir olmalı.

**(3) Sonra metin.** §7'deki liste.

---

## 7. Metne işlenecekler (A kolu bitince tek geçişte)

Kapı `verify_manuscript_numbers.py` sekiz taşıyıcı sayıyı **YOK** diyor; liste
odur. Ek olarak kapının görmediği şunlar elle güncellenecek:

| yer | eski | yeni |
|---|---|---|
| §4.2 paydalar | 3.122/5.331 | **2.831/3.814** |
| §4.2 aralık | $+4{,}36$–$+14{,}60$ | $+4{,}36$–$+19{,}37$ |
| §4.2 yayılım + kat | $10{,}45\pm0{,}76$, 3,3 kat | $15{,}01\pm0{,}84$, **4,4 kat** |
| §4.2 protokol ort. açıklığı | 10,24 | **15,01** (artık tohum-başına ortalamayla **eşit**; "üçüncü tohumda uç protokol farklı" nüansı CIFAR-10'da kalktı, CIFAR-100'de duruyor) |
| §4.2 eşli GA | $[7{,}33; 9{,}21]$ | $[7{,}33; 9{,}22]$ |
| §4.2 en geniş protokol çifti | 19,68 | **23,77** |
| §4.2 uç olma sayıları | 12/18 en küçük, 2 en büyük | **12 en küçük, 4 en büyük** |
| §4.2 B kolu 4-protokol eğimi | $-0{,}567$ $[-0{,}757; -0{,}451]$ | $-0{,}528$ $[-0{,}664; -0{,}418]$ |
| §4.4 CIFAR-100 eşli GA | $[9{,}48; 12{,}36]$ | $[9{,}47; 12{,}35]$ |
| §4.4 paragraf başı | "yayılım genişliyor" | **karşılaştırılabilir** (§2b) |
| §4.6 $L_2$ yayılımı | 10,91, "aynı büyüklükte" | 10,92, süsleme **kalkacak** (§2b) |
| §4.7 oran duyarlılığı | 3,3–22,7 · 20,9 | varyans oranı artefaktı: **5,2–32,6** |
| §5, §6 | 13,58 > 10,45 karşılaştırması | §2b'ye göre |
| bildiri | $+4{,}4$–$+14{,}6$ · 3,3 kat | $+4{,}4$–$+19{,}4$ · 4,4 kat |

**Ayrıca eklenecek (öneri):** tek bir protokol adının altındaki yazılmamış alt
seçimin CIFAR-10 asimetrisini **4,77 puan** oynattığı — yani koşumlar arası
standart sapmanın (≤1,48) üç katından fazla — ölçülmüş bir duyarlılık olarak
raporlanması. Bu, makalenin kendi tezinin ikinci dereceden bir örneğidir ve
kendi boru hattımızda bulunmuştur; sessizce düzeltmek yerine yazmak hem daha
dürüst hem daha güçlüdür.

---

## 8. Üretilen yardımcı dosyalar

`scripts/_b2_*.{py,sh}` ve `scripts/_yama_*.py` geçicidir (alt çizgi öneki).
`_b2_gerileme.sh` + `_b2_karsilastir.py` + `_b2_kayma.py` üçlüsü **saklanmalı**:
gerileme kontrolünü tekrar koşturur. `results/q1/_b2_gerileme/` ve
`results/q1/_b2_olcum.json` ara çıktılardır, arşivlenebilir.

---

## 10. KAPANIŞ ÖLÇÜMLERİ — 2026-08-25

### A kolunun yeniden koşumu: iki etki ayrı ölçüldü

| etki | ne değişti | ortalama \|fark\| | en büyük |
|---|---|---|---|
| Tohumlama | `random_start` artık (yörünge, epok)'a bağlı | 0,07–0,17 puan | 0,99 |
| Tanım | sıkı eksi gevşek, yalnız başarılı kaynak | **4,12 puan** | 7,65 |

Tohumlama etkisinin ortalaması ~0, yani **yansız**: eski sayılar sistematik
olarak kaymış değildi, yalnızca tarama sırasına bağlıydı. Asıl değişiklik
tanım düzeltmesidir.

### İki kol: bir açıklama daha çürüdü

| nicelik | eski | yeni |
|---|---|---|
| A, dört protokol | $+0{,}293$ | $+0{,}273$ [$+0{,}219$; $+0{,}371$] |
| A, üç protokol | $+0{,}672$ | $+0{,}673$ [$+0{,}602$; $+0{,}727$] |
| B, dört protokol | $-0{,}567$ | $-0{,}528$ [$-0{,}664$; $-0{,}418$] |
| B, ana çift | $+0{,}387$ | **$-0{,}100$** [$-0{,}464$; $+0{,}092$] |

Eski metin, iki kolun dört protokollü eğimlerindeki uyuşmazlığı "bir kontrol
etkisi değil bileşim etkisi" diye açıklıyor ve kanıt olarak gözlemsel kolun
aynı mimari çiftine kısıtlandığında kontrollü kolla uyuştuğunu gösteriyordu.
**Artık uyuşmuyor.** Yazılan: bileşim farkın büyük kısmını açıklıyor ama
kapatmıyor; iki kol üç protokollü eğimde uyuşuyor, dört protokollüde
uyuşmuyor — ki mekanizma iddiasının dayandığı nicelik zaten üç protokollü
eğimdir.

### Yolda bulunan ve kapatılan altı kapı/sınama kusuru

1. Beşinci kapının "otoriter" değerleri **sabit yazılmıştı** → artefakttan
   okunuyor; öz-sınamaya artefaktı bozan üç kol eklendi.
2. Özet öz-sınamasının birinci kolu **sessizce düşmüştü** (enjeksiyon çapası
   metne çiviliydi) → çapa özet ortamına bağlandı, enjeksiyonun yazıldığı
   doğrulanıyor, sayı-nötr dördüncü kol eklendi.
3. Özet kapısı **yanlış sebep söylüyordu** (uzunluk ihlalini "eksik sayı"
   diye raporluyordu) → sayaçlar ayrıldı.
4. İddia kapısında **metin kökü ile artefakt kökü aynıydı** → ayrıldı;
   öz-sınama artefakt kökünü açıkça veriyor ve boş kökte H1/H2'nin kaldığını
   sınayan yeni bir kol taşıyor.
5. **EN/TR ayna denetimi hiç yoktu** → altıncı kapı yazıldı ve hemen iki
   gerçek kusur buldu (bkz. §11).
6. Kalibrasyon şeklinin `final/` kopyası `raw/` ile **sessizce ayrışmıştı** →
   eşitlendi.

### §11. Ayna kapısının bulduğu iki gerçek kusur

- **Türkçe Yöntem'de "Öznitelik Bozunması Metrikleri" başlığı hiç yoktu**
  (başlık, iki denklem, $L_2$ uzaklığı tanımı). Türkçe Bölüm 4 aynı
  metrikleri kullanıyor ve raporluyordu; yani Türkçe sürüm kullandığı
  metrikleri tanımlamıyordu. Eklendi.
- **İngilizce Tartışma'da Mahmood ve ark.'nın ters yönlü bulgusuyla yüzleşen
  paragraf hiç yoktu**; Türkçede vardı. Gönderilecek sürüm İngilizce olduğu
  için bu, gönderilen metnin eksiğiydi. İngilizce aynası eklendi.

İkisi de sayı taşımadığı için sayı kapısı görmedi; ikisi de muhafızlı bir
ifade olmadığı için iddia kapısı da görmedi.
