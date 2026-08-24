# HAKEM RAPORU — 2026-08-24

**Makale:** *The Measurement Protocol Decides the Conclusion: A Methodological
Study of CNN and Vision Transformer Adversarial Robustness Comparisons*
**Sürüm:** dal `q1` @ `fe26fb6` · EN 19 sayfa · TR aynası 19 sayfa · bildiri 6 sayfa
**Hedef:** SCI/SCIE dergisi (IEEE Access düzeyi) — gönderilecek sürüm İngilizcedir

---

## 0. Bu rapor nasıl üretildi

Altı bağımsız hakem paralel çalıştı, her biri ayrı bir eksende, hepsi salt-okur:

| # | Eksen | Araç kullanımı |
|---|---|---|
| 1 | İstatistik ve çıkarım | 35 |
| 2 | Deneysel tasarım ve iç geçerlilik (kod öncelikli) | 64 |
| 3 | Sayı–artefakt izlenebilirliği, karantina taraması | 79 |
| 4 | İddia–kanıt uyumu ve literatür konumlandırma | 52 |
| 5 | Sunum, yapı, dergi uygunluğu (PDF'ler açılarak) | 54 |
| 6 | Kırmızı takım — tezi çürütmeye çalış | 61 |

**Hakemlik sırasında depoda hiçbir dosya değiştirilmedi.** Bir ajan doğrulama
için figür üreticilerini koşturdu ve çalışma ağacında iz bıraktı; fark
ölçüldü (en büyük sapma 0,0018 nat, yeniden üretim gürültüsü) ve geri alındı.

Aşağıdaki bulguların **hangilerini kendim bağımsız olarak doğruladığımı**
`[✓ doğrulandı]` ile işaretledim. İşaretsiz olanlar tek bir hakemin
raporundan gelir ve uygulanmadan önce teyit edilmelidir.

---

## 1. Karar

**Büyük revizyon (Major Revision).** Altı hakemin altısı da bu kararda
birleşti. Çekirdek katkı gerçek ve yayımlanmaya değer; ancak üç kalem
**gönderimi durdurur** ve manşet sayıların bir kısmı yeniden üretilmelidir.

**İyi haber:** kusurların hiçbiri yeni GPU koşumu gerektirmiyor. Hepsi mevcut
örnek-bazlı kayıtlardan yeniden puanlama, figür yeniden üretimi, ve yazım
işidir.

---

## 2. GÖNDERİMİ DURDURAN ÜÇ KALEM

### B1 — İngilizce şekiller kendi tablolarını yalanlıyor [✓ doğrulandı]

İngilizce bölümler `figures/final/`, Türkçe bölümler `figures/final_tr/`
kullanıyor. İki küme **aynı değil** ve İngilizce olan yanlış.

PDF metin katmanından çıkardığım değerler:

| | EN Şekil 1 | **Tablo I (metin)** | TR Şekil 1 |
|---|---|---|---|
| ResNet-18 AT temiz | 85,4 | **85,78** | 85,8 ✓ |
| ResNet-18 AT PGD-10 | 41,0 | **44,11** | 44,1 ✓ |
| ResNet-18 AT AutoAttack | 35,7 | **37,93** | 37,9 ✓ |
| ViT-Tiny AT temiz | 75,7 | **73,53** | 73,5 ✓ |
| ViT-Tiny AT PGD-10 | 36,1 | **32,69** | 32,7 ✓ |
| ViT-Tiny AT AutoAttack | 32,9 | **29,14** | 29,1 ✓ |
| ViT-Tiny temiz | 77,5 | **80,09** | — |

Transfer ısı haritası daha da net: EN Şekil 4 **2×2** ve `52,2 / 21,0 / 20,3 /
52,3`; TR Şekil 3 **3×3** ve `48,5 / 19,9 / 12,5 / 15,5 / 55,6 / 8,7 / 21,5 /
18,2 / 25,2` — yani Tablo IV ile birebir. Bunun doğrudan sonucu:

**EN Şekil 4'ün altyazısı "köşegen dışı asimetri +4,4 puandır" diyor; şeklin
kendisi 21,0 ve 20,3 gösteriyor, yani +0,7.** Altyazı doğru, şekil yanlış.

`77,50` ve `36,1` değerleri `CLAUDE.md`'nin açıkça karantinaya aldığı
run1/run2 kaydıdır. Bir hakem Şekil 1 ile Tablo I'i yan yana koyduğunda
makalenin tüm sayısal içeriğine güvenmeyi bırakır.

**Not:** izlenebilirlik hakemi "karantina ihlali yok" demişti — o `.tex`
kaynaklarını ve üretici betikleri taramıştı, şekil PDF'lerinin metin katmanını
değil. Sunum hakemi PDF'leri açtı. Kodu ve PDF'i ben karşılaştırdım; **sunum
hakemi haklı.** Bu, kapıların neden PDF içeriğini de taraması gerektiğinin
kanıtıdır.

**Düzeltme:** `figures/final_tr/` üretim yolunu İngilizce etiketlerle
koşturup `figures/final/` içeriğini tamamen değiştirin. TR sürümdeki iki
tasarım iyileştirmesini de taşıyın: Şekil 1'de "eşleşmiş AT çifti / referans"
gruplaması, Şekil 3'te 3×3 matris ve 0–60 renk ölçeği.

### B2 — `successful-source` protokolü makalenin kendi tanımını karşılamıyor [✓ doğrulandı]

Üç hakem bunu bağımsız olarak buldu (tasarım, iddia-kanıt, kırmızı takım).
Ben de artefaktlardan yeniden hesapladım.

Metin (§3.6): *"target-correct samples whose attack **succeeded on the
source** in the white-box sense."*
Kod (`experiments/rev2/a2_transfer_protocols.py:64`):

```python
cond = pair["target_clean_correct"] & pair["source_adv_wrong"]
```

`source_adv_wrong` = `src_adv_pred != labels` — **kaynağın temizde doğru
olması istenmiyor.** Kaynağın zaten yanlış bildiği örnekler "saldırı başarılı"
sayılıyor.

Kirlenme yönler arasında asimetrik, çünkü ViT kaynağın temiz hatası %26,5,
ResNet'inki %14,2:

| | CNN→ViT | ViT→CNN | asimetri |
|---|---|---|---|
| kod (mevcut) | n≈3.120 · %38,5 | n≈5.330 · %23,9 | **+14,60 ± 1,48** |
| sıkı (metnin tanımı) | n≈2.830 · %36,4 | n≈3.810 · %17,0 | **+19,36 ± 1,26** |

Manşete etkisi:

| | dört protokol | yayılım | oran |
|---|---|---|---|
| kod | 13,57 · 4,36 · 8,27 · **14,60** | 10,24 | **3,35 kat** |
| sıkı | 13,57 · 4,36 · 8,27 · **19,36** | 15,00 | **4,44 kat** |

Bu, makalenin kendi eleştirisinin aynası: §5.2 ham oranın *hedefin* temiz
hatasıyla kirlendiğini bir raporlama kusuru ilan ediyor; bu protokol aynı
kusuru *kaynak* tarafında yapıyor. Literatürdeki kullanım (Mahmood 2021,
TREND 2023) sıkı tanımdır.

**Etkilenen zincir:** Tablo III, §4.2 manşeti, iki-sürücü ayrıştırması
(−0,567 eğimi aynı gevşek maskeyle hesaplandı), Özet, Giriş, Sonuç **ve
bildiri** (bildiri de "+4,4 ile +14,6, 3,3 kat" diyor).

**Düzeltme:** Maskeyi sıkılaştırın (npz'ler `source_clean_correct` alanını
zaten taşıyor; GPU gerekmez) veya tanımı koda uydurup sıkı varyantı duyarlılık
olarak verin. **Sıkılaştırma önerilir:** etki büyür, tanım literatürle uyumlu
olur.

### B3 — Tablo VIII'in "ViT (native)" sütununun arkasında artefakt yok

İki hakem aynı sütunu farklı açılardan vurdu.

*İzlenebilirlik hakemi:* Dört değer (Hoyer **0,405**, Gini **0,571**,
Frac<%1 **%17,9**, hizalanma **0,079**) `results/` ağacının hiçbir
JSON/CSV'sinde geçmiyor. `results/stat_addendum/stat_addendum.json >
native_vit_control` yalnız `{params, ckpt_adv_acc, ckpt_clean_acc}` içeriyor.
Kapı da bu sütunu kontrol etmiyor.

Ayrıca **0,405 değeri `results/c_addenda/clean_gradient_stats.json`'daki
`ViT_Tiny_clean.hoyer_mean = 0,40594` ile birebir çakışıyor** — sütunun
yanlışlıkla temiz eğitilmiş ana ViT'ten kopyalanmış olabileceği şüphesi.
Doğrulayacak artefakt olmadığı için karara bağlanamıyor.

*Tasarım hakemi:* Aynı kontrol noktası (`models/vit_cifar_tiny/...`) doğrulama
bölmesi ayrılmadan eğitilmiş — `logs/vit_cifar_tiny_at.log` epok başına 391
batch (=50.000 örnek) gösteriyor — ve
`src/training/adversarial_trainer.py:456` doğrulama yükleyicisi yokken **test
kümesine** düşüyor. Yani kontrol noktası test kümesinde seçilmiş, tarihi
Ocak 2026, C1 düzeltmesinden önce.

Bu sütun, makalenin 32→224 büyütme karıştırıcısına verdiği **tek** yanıttır
(§4.6 ve §5.3 buna dayanıyor). Kanıtsız ve köken beyansız bir karıştırıcı
kontrolü, tezi "seçim protokolü sonucun parçasıdır" olan bir makalede çifte
standart olarak okunur.

**Düzeltme:** Kontrol noktasını yeniden gradyan analizinden geçirip artefakt
üretin, `KOKEN.json`'a ekleyin, kapıya dört kontrol satırı koyun; sütun
dipnotuna kökenini yazın. Üretilemiyorsa sütunu kaldırıp karıştırıcıyı
Sınırlılıklar'a taşıyın.

---

## 3. MANŞET SAYILARIN YENİDEN TANIMLANMASI (kırmızı takım)

Bunlar kusur değil, **tezin nasıl sunulduğuna** dair itirazlar. Hepsi
ısırıyor ve hepsi karşılanabilir. Kırmızı takımın en değerli katkısı budur.

### K1 — CIFAR-100 ön-kayıtlı kestirimi, geçersiz ilan edilen protokol çıkarılınca TERSİNE dönüyor [✓ doğrulandı]

Kendi hesabım:

| veri kümesi | 4 protokol | ham HARİÇ | yayılımın özdeşlik payı |
|---|---|---|---|
| CIFAR-10 | 10,45 | 10,24 | %2 |
| **CIFAR-100** | **13,58** | **6,92** | **%49** |
| SVHN | 3,65 | 3,65 | %0 |
| CIFAR-10 L2 | 10,91 | 7,39 | %32 |

§4.3'ün ön-kayıtlı kestirimi: *"zor veri kümesinde yayılım büyür"* →
13,58 > 10,45 ile "doğrulandı" ilan ediliyor. Ama makale §5.2'de ham oranı
mimari karşılaştırması için **geçersiz** ilan ediyor ve §4.2.1'de ham ile
koşullu arasındaki farkın **cebirsel** olduğunu gösteriyor. Geçersiz protokol
çıkarılınca **6,92 < 10,24** — kestirim doğrulanmıyor, çürütülüyor.

Aynı şey §4.4'ün "yayılım tam olarak temiz doğruluk açıkları gibi sıralanıyor"
iddiasını da bozuyor: ham hariç sıralama 3,65 < 6,92 < 10,24, açıklar ise
1,85 < 12,3 < 20,7.

Makalenin kendi artefaktı bunu ölçmüş ama metne girmemiş:
`results/q1/e3_spread_teshis.json` → yön başına özdeşlik payı ortalama %82.

**Öneri:** Ya ham protokolü yayılım hesabından çıkarıp tüm manşetleri yeniden
yazın ve ön-kayıt sonucunu dürüstçe "kestirim doğrulanmadı" olarak raporlayın
(K8 kuralı bunu zaten emrediyor), ya da her manşetin yanına özdeşlik payını
yazın. İkincisi daha ilginç: *"yayılımın %82'si cebirsel, %18'i ampirik"*
tek başına yayımlanabilir bir cümledir.

### K2 — Özdeşliğin evrensellik iddiasının deponuzda karşı örneği var [✓ doğrulandı]

Özet ve Sonuç: *"applies to any published raw rate"*, *"in any study that
reports them"*. Özdeşliğin kendisi koşulsuz doğrudur; **evrensel olmayan
öncüldür** — temiz-yanlış örneklerin saldırı altında yanlış kalması.

Kendi ölçümüm:

| hedef tipi | P(çekişmeli yanlış \| temiz yanlış) |
|---|---|
| çekişmeli eğitilmiş (CIFAR-10, 27 yön) | 0,9929 – 1,0000 |
| **standart eğitilmiş** (`results/transfer_analysis_clean/`, 4 yön) | **0,8826 – 1,0000** |

`scripts/q1_ozdeslik_kontrol.py`'nin `KAYNAKLAR` sözlüğü sabit kodlanmış ve
yalnız çekişmeli eğitilmiş hedefleri tarıyor. Oysa transfer literatürünün
büyük çoğunluğu (Naseer, TGR, MIG, Mahmood) **standart eğitilmiş** hedeflere
saldırır — yani iddianın uygulanacağı ana rejim, ölçümün dışında kalmış.

**Öneri:** Denklem'in genel formunu yazın —
$r_{\text{ham}} = e(1-p) + r_{\text{koş}}(1-e)$ — ve iddiayı şuna çevirin:
*"öncül raporlanabilir bir niceliktir; çekişmeli eğitilmiş hedeflerde
0,989–1,000, standart eğitilmişlerde 0,88'e iner. Düzeltme uygulanmadan önce
öncül ölçülmelidir."* Bu iddiayı **zayıflatmaz, uygulanabilir kılar.**

### K3 — Yayılımın uç noktaları hiçbir zaman onaylanan iki protokol arasında değil

`results/q1/e3_surucu_ayristirma.json` → `both_correct: {max: 0, min: 0}`:
**birincil protokol 18 yön çiftinin hiçbirinde uç değil.** Sekiz veri
kümesi × tohum hücresinin hepsinde uç ya `raw` (makalenin yasakladığı) ya
`successful_source` (makalenin "farklı soruya cevap veriyor" dediği).

Aynı soruyu soran iki onaylanan protokol arasındaki mesafe: CIFAR-10 3,9 ·
CIFAR-100 6,0 · SVHN 0,66 · L2 1,95 puan.

**Bu hâlâ tezi taşıyor** — 3,9 ve 6,0, yeniden eğitmenin 0,23–1,48 puanının
belirgin biçimde üstünde. Ama manşet 2,5–3 kat şişkin, ve SVHN ile L2'de etki
seçim piyangosunun altına düşüyor.

**Öneri:** Yayılımı iki bileşene ayırın: (i) tanım gereği farklı soru soran
protokoller arası mesafe, (ii) aynı soruyu soran protokoller arası mesafe.
İkincisini manşete koyun. `both_correct` hiçbir zaman uç değil gerçeği
raporlanmalı — bu aslında **makalenin lehine**: birincil protokol dayanıklı.

### K4 — Kendi kalibrasyon eğriniz, eşleşmiş çiftte etkiyi 2 puana indiriyor

A kolu uydurması (`e3_iki_kol_fit.json`):
yayılım ≈ **0,80 + 0,672 × temiz-hata-farkı** (r = 0,980).

CIFAR-10'da açık 12,3 → tahmin 9,07 (ölçülen 9,2–11,3 ile uyumlu). ViT tarifi
düzeltilirse (Debenedetti/Mo ile ~88–90 temiz doğruluk) açık ~2'ye iner ve
tahmin **2,14 puan** olur — seçim piyangosuyla aynı mertebe.

Daha da önemlisi: **kesişim 0,80 puan.** Bu, "iki model temiz doğrulukta
eşitse protokol seçiminin taşıdığı indirgenemez etki"dir ve makale bunu hiç
raporlamıyor.

Hasım hakemin yazacağı cümle: *"Yazarlar bir ölçüm sorunu keşfettiklerini
sanıyorlar; aslında keşfettikleri şey, kötü eşleştirilmiş bir çiftte protokol
seçiminin önem kazandığı."*

**Öneri:** Kesişimi ve dışdeğerlemeyi §4.2'ye açıkça yazın. Bu itirazı
silahsızlandırır ve makaleyi **daha ilginç** yapar: tavsiye "protokolü belirt
VEYA modelleri eşle" olur ve nicel bir eşik kazanır.

### K5 — SVHN'de onaylanan iki protokol işareti ÇEVİRMİYOR

Kırmızı takımın örnek-bazlı bootstrap'i (B=4000):

| protokol | pair1 [%95 GA] | pair2 [%95 GA] |
|---|---|---|
| ham | +0,33 [−0,04; +0,72] | +0,46 [+0,05; +0,84] |
| hedef-doğru | **−1,16 [−1,59; −0,72]** | **−0,86 [−1,30; −0,41]** |
| her-ikisi-doğru | −0,34 [−0,75; +0,07] | −0,36 [−0,75; +0,05] |
| başarılı-kaynak | **+2,98 [+1,83; +4,04]** | **+2,41 [+1,29; +3,51]** |

"Ölçülen şey gürültü" itirazı **tutmuyor** — farklar anlamlı ve zıt işaretli.
Ama onaylanan iki protokolün **ikisi de negatif**. İşaret çevrilmesi
{TC, BC} ile {ham, SS} arasında; ve hamın pozitifliği özdeşliğin aritmetik
sonucu.

**Öneri:** §4.4'te açıkça yazın: *"onaylanan iki protokol SVHN'de aynı işareti
veriyor; işaret çevrilmesi koşulsuz oran ile başarılı-kaynak protokolünden
gelir, ve koşulsuz orandaki çevrilme Denklem (7)'nin doğrudan sonucudur."*
Bu iddiayı zayıflatmaz, **doğrular**: ham oran raporlamak işareti çevirebilir
ve Denklem (7) bunun ne zaman olacağını önceden söyler.

---

## 4. MAJOR — istatistik ve çıkarım

### İ1 — Uzamsal yerellik tablosunda geçersiz istatistik [✓ doğrulandı]

Tablo IX'un `p` sütunu üç koşumun **en büyük** Wilcoxon p'si (altyazıda
dürüstçe yazılı) ve buradan "dört ölçünün üçünde anlamlı fark yok" sonucu
çıkarılıyor. Artefakt (`results/c1_c5/pair*/c5_spatial.json`):

| ölçü | pair1 | pair2 | pair3 | makalede |
|---|---|---|---|---|
| area50 | 5,2e-02 | **1,2e-04** | 2,6e-01 | 0,26 |
| area90 | **4,4e-10** | **6,2e-17** | 3,9e-02 | 0,039 |
| entropi | **1,6e-03** | **3,7e-06** | 8,0e-01 | 0,80 |
| Moran's I | **9,0e-08** | 5,4e-01 | **6,1e-09** | 0,54 |

Maksimum-p geçerli bir birleştirme değil (Fisher/Tippett gibi değil), en zayıf
kanıtı seçmektir ve null lehine yanlıdır. Ayrıca aynı satırda `Diff.` sütunu
3-koşum ortalaması, `p` sütunu 500-örnek düzeyi — tek satırda iki analiz birimi.

**Önemli:** hakemin önerdiği doğru analiz (koşum düzeyi n=3 çıkarım) **aynı
null sonucu koruyor** — area90 t≈2,86 p≈0,10; entropi t≈1,52 p≈0,27;
Moran's I t≈2,24 p≈0,15. Hüküm ayakta, yalnızca yöntem savunulamaz.

### İ2 — Dikkat entropisi null'u hiçbir testle desteklenmiyor

`results/c1_c4/pair*/c4_summary.json` yalnız nokta kestirimi taşıyor: GA yok,
eşleştirilmiş test yok, TOST yok, güç hesabı yok. Oysa entropi örnek başına
hesaplanıyor (n=1000), yani eşleştirilmiş GA/TOST tek satırlık iş.

"Fark bulamadık" ile "fark yok" ayrımı makalenin kendi retorik ekseni; transfer
farkı için TOST koşan bir makalenin kendi null'unu eşdeğerlik testiyle
desteklememesi hakemin ilk yakalayacağı çelişkidir.

**Bununla birleşen sunum kusuru:** Şekil 8b `n_samples: 8, note: "figure batch
only"` verisiyle çizilmiş ve metin onu *"n=1000 null'unun görsel biçimi"* diye
sunuyor. Şekilde eğriler üst üste değil — katman 11'de ~0,04 nat ayrım var,
metnin "en çok 0,005 nat" iddiasının 8 katı. Üstelik makale §4.7'de tam olarak
*"8 örneklik figür partisi görünür bir etki önerdi, büyük ölçüm desteklemiyor"*
diye uyarıyor ve sonra o şekli kanıt olarak basıyor.

### İ3 — TOST marjı makalede hiçbir yerde yazılı değil

`03_methodology.tex:142`: *"the margin stated at each use."* Marj **hiçbir
kullanımda** belirtilmiyor. Artefaktta var ve gerekçelendirilmiş
(`a2_transfer_protocols.json` → birincil ±2 puan, duyarlılık ±1/±3; E2'de
ayrı bir marj, 1,0 puan).

Eşdeğerlik ifadesi marjsız anlamsızdır: ±0,2 puan marjında SVHN'de eşdeğerlik
reddedilir, ±2 puanda kabul edilir. Özet makalenin en çarpıcı iddiasını marjı
gizleyerek sunuyor. Ayrıca ±2 puan, test edilen niceliğin koşumlar-arası
SS'sinin (0,23 CIFAR-10 · 0,01 SVHN) 9–200 katı.

### İ4 — Seçim yayılımını "monoton kötüleştirici" bir boyut taşıyor

Üç hakem bağımsız olarak buldu. `results/q1/e2/e2_grid.json` kendi notunu
taşıyor: *"yumusatma cogu yorungede tek yonlu kotulestirici oldugu icin
yayilimi sisiriyor"*; ResNet 3/3, ViT 2/3 tohumda k arttıkça test PGD-10
monoton düşüyor.

| alt küme | ResNet | ViT |
|---|---|---|
| 18 hücre (manşet) | 2,85 / 2,83 / 2,62 | 1,58 / 2,04 / 2,09 |
| k=1 (yumuşatma yok) | 0,71 / 2,83 / 0,45 | 1,58 / 0,00 / 1,39 |
| tek bölme + k=1 | 0,52 / 1,33 / 0,00 | 0,00 / 0,00 / 0,69 |

Çekirdek oran (bölme × patience, yumuşatma hariç): ResNet **1,09×**, ViT
**1,42×** tohum SS'si — yani "dördüncü varyans kaynağı" tohum varyansıyla aynı
mertebeye iniyor.

**Öneri:** İddiayı daraltın, zayıflatmayın: *"seçim sayıyı 2,9 puana kadar
oynatabilir, ama bunun yaklaşık yarısı eğri yumuşatmasından gelir;
makalelerin fiilen değiştirdiği bölme ve patience seçimleriyle sınırlandığında
etki bir eğitim tohumuyla karşılaştırılabilir."*

### İ5 — 6–8 kümeli bootstrap ve küme bağımsızlığı

`e3_iki_kol_fit.json`: A kolu 8 küme, B kolu 6 küme. Yüzdelik küme
bootstrap'ı G < 30'da kapsamayı düşük tutar; `[0,601; 0,726]` gibi bir aralık
8 kümeden gelemeyecek kadar dar. Ayrıca WRN **tek sabit checkpoint** ve altı
kümenin hepsinde var — kümeler i.i.d. değil.

**Öneri:** Wild cluster bootstrap-t (Rademacher) veya G−1 serbestlik dereceli
t-düzeltmesi; küçük-G literatürüne atıf; `B_ana_cift` kolunu (WRN'siz) ana
sonuç yapın; GA'ların yanında küme sayısını her seferinde yazın.

### İ6 — L2 bölümünde geri çekilen sözde-tekrar korelasyonu geri gelmiş

§4.5: *"slope +0,914, r = 0,999 over eighteen directions"*.
`e6_onkestirim.json` → 18 yön ama x ekseni yalnız **3 ayrık değer** alıyor
(10,52 altı kez, hepsi aynı sabit WRN'den). `results/q1/c3_precision.json` bu
sayımı zaten reddediyor: *"noktalar bagimsiz DEGIL; bu GA kesinligi abartir"*.

Makale bu hatayı §4.2.1'de açıkça geri çekiyor ve §4.3'te nitelendiriyor;
§4.5'te nitelenmeden duruyor, üstelik daha büyük n ile sunularak kesinlik
izlenimi artırılmış. Hakem bunu "seçici titizlik" olarak okur.

---

## 5. MAJOR — iddia, literatür, sunum

### L1 — "Çürütülen üç literatür iddiası"ndan ikisi hiçbir kaynağa bağlanmamış

§4.6.1: *"the sparser-CNN result is **frequently described** in spatial
language"* — atıf yok. §5.2 reddederken `hurley2009comparing`'i anıyor, ama o
kaynak **sizin kullandığınız ölçütlerin** kaynağıdır, iddiayı kuran taraf
değil.

§4.7: *"claims of 'attention degradation'"* — atıf yok, ve makale dürüstçe
itiraf ediyor ki bu izlenimi üreten şey **kendi 8 örneklik figür partisidir**.

Yani "literatürde yaygın bir iddiayı çürütüyoruz" çerçevesi hedefsiz ve
kısmen kendine dönük — straw man okumasına açık.

**Öneri:** Ya iddiayı fiilen kuran kaynakları verin, ya çerçeveyi düşürün:
*"three commonly assumed properties — including one asserted in our own
preliminary version — fail under direct measurement."* İkincisi daha az
iddialı ama savunulabilir.

*(TGR'de kusur yok: `zhang2023tgr` doğru anlaşılmış, uyarlama üç boyutta beyan
edilmiş, kontrol aynı bütçede eşli, sonuç "in this regime" kaydıyla verilmiş.
Örnek nitelikte kapsam disiplini.)*

### L2 — Mahmood et al.'in ters yönlü bulgusuyla yüzleşilmiyor

Mahmood et al. both-correct protokolüyle (m=1000) **BiT→ViT <%16, ViT→CNN
%34–47** buluyor — sizin both-correct sonucunuzun (18,25 vs 9,98) **tam tersi
yön**. Makale §1'de literatürün "yön konusunda anlaşamadığını" söylüyor ama bu
spesifik karşıtlığı hiç ele almıyor.

Oysa bu, "asimetri zayıf hedefin özelliğidir" mekanizmanız için **mevcut en
iyi dış sınav**: Mahmood'un ayarında hangi hedef daha zayıftı? Mekanizmanız o
ayarda da yönü doğru öngörüyorsa üç hedefli $r = 0,986$ korelasyonunuza
dördüncü ve bağımsız destek eklersiniz; öngörmüyorsa sınırı dürüstçe
çizersiniz. **Her iki sonuç da makaleyi güçlendirir.**

### L3 — Değerlendirme metodolojisi literatürünün çekirdeği eksik

Tezi "ölçüm sonucu belirler" olan bir makalede bulunmayanlar:
Carlini et al. 2019 (*On Evaluating Adversarial Robustness*), Tramèr et al.
2020 (*On Adaptive Attacks*), TA-Bench (NeurIPS 2023, arXiv:2311.01323 — sizin
**en yakın komşunuz**), Waseda et al. (WACV 2023, aynı-hata/farklı-hata
ayrışması), *Reliable Evaluation of Adversarial Transferability*
(arXiv:2306.08565, protokol-2/protokol-3 ayrımı).

Hiçbiri sizin kontrollü tasarımınızı yapmıyor — yani bunlar makaleyi
zayıflatmaz, **konumlandırmayı sağlamlaştırır**. Şu hâlde bir hakem bunları
kendisi bulup "farkında değiller" der.

### L4 — "Yenilik yok, ölçüm eleştirisi" itirazına yazılı cevap yok

En sert hakemin yazacağı cümle: *"Dört protokol dört farklı tahmin edileni
(estimand) ölçüyor; farklı sorulara verilen farklı cevapların 'yayılımı'
varyans değildir."* Makale bu itirazın maddesini biliyor (§5.1 her protokolün
savunulabilir bir kullanımı olduğunu söylüyor) ama itirazı **adıyla**
karşılamıyor; üstelik §4.9'un başlığı "Sources of Variance" ve protokolü bir
varyans kaynağı olarak listeleyerek karışıklığı davet ediyor.

**Önerilen paragraf (§5.1'e):** *"Protokoller farklı tahmin edilenlerdir;
bunu tartışmıyoruz. İddiamız, yayımlanan literatürün hangisinin seçildiğini
rapor etmediği ve okuyucunun tahmin edileni geri kazanamadığıdır. Ölçtüğümüz
nicelik protokoller-arası varyans değil, rapor eksikliğinin okuyucuya bıraktığı
belirsizliktir."* Bu tek paragraf reddi çevirebilir ve şu anda makalede yok.

### S1 — Üslup temizliğinin bıraktığı dört hasar (iki dilde birden)

Bunlar benim yaptığım maddelendirme→paragraf dönüşümünün artıklarıdır.

| # | Yer | Sorun |
|---|---|---|
| a | `01:27` ↔ `05:27` ↔ `06:13` | Giriş **"üç bulgu ayakta kaldı"**, Tartışma ve Sonuç **"iki davranışsal fark"**. Sayaç güncellenmemiş. |
| b | `05:17` (EN+TR) | SVHN'de yönün korunmadığını kuran iki cümlenin hemen ardında SVHN öncesinden kalan *"Değişen yalnızca etkinin ne kadar büyük göründüğü…"* cümlesi duruyor ve öncekileri yalanlıyor. |
| c | `06:82` (EN+TR) | Sonuç **"altı raporlama gerekliliği"** diyor; §5.2 düz paragrafa çevrildiği için içinde **yedi** var ve hiçbiri numaralı değil. |
| d | `04:481` | *"Two cautions bound it further."* → iki cümle → *"survives **all three** caveats."* |

### S2 — Şekil altyazıları metnin bulgusuyla çelişiyor

**Şekil 6 panel başlıkları:** *"ResNet-18 Gradient (more **concentrated**)"* /
*"ViT-Tiny Gradient (more **distributed**)"*, altyazı *"around object edges"*
— §4.6.1 ve Tablo IX tam olarak bunu ölçüp **reddediyor**. Ayrıca şeklin
dipnotundaki `Hoyer 0.474 / 0.449` Tablo VIII'in `0,4928±0,0120 /
0,4561±0,0055` değerlerinin **dışında**.

**Şekil 7 altyazısı:** *"later layers show larger attention shifts"* — şekilde
en büyük fark **katman 6**'da, katman 12 daha soluk.

**Şekil 3 altyazısı:** *"the same test image"* — şekilde **üç farklı görüntü**
var ve üçüncü satır beyaz kutu değil, **transfer** (CNN→ViT).

### S3 — Özet 419 kelime (IEEE Access sınırı 250)

13 cümle, 21 sayısal değer. Portal gönderimde reddedebilir. Sayı yükü tezi
gömüyor. Sunum hakemi ~235 kelimelik, sayıyı 6'ya indiren bir taslak yazdı
(rapor ekinde).

### S4 — Şekiller sütun genişliğine %24–36 küçültülüyor

| Şekil | Doğal genişlik | Ölçek |
|---|---|---|
| Şekil 6 gradyan karşılaştırma | 890 pt | **0,28×** |
| Şekil 7 dikkat karşılaştırma | 849 pt | **0,30×** |
| Şekil 9 t-SNE | 1001 pt | **0,25×** |
| Şekil 5a, 8a | ~500 pt | **0,24×** |

Sütun genişliğinde üretilmiş dört şekil (1, 2, 5b, 8b) mükemmel okunuyor;
gerisi farklı bir hedef genişlik için üretilip küçültülmüş. Hakemin ilk sayfa
çevirişinde göreceği en görünür kalite sorunu.

**Ayrıca:** Şekil 7 ile Şekil 8a **birebir aynı şeyi** gösteriyor (aynı örnek,
aynı katmanlar); Şekil 7 fark panelini de içerdiği için 8a'yı tümüyle
kapsıyor. Şekil 8a silinebilir.

### S5 — Dört kayan nesne metinde hiç atıf almıyor

Şekil 4 (`fig:transfer_heatmap`), Tablo V (`tab:cifar100_results`), Tablo VII
(`tab:l2_results`), Tablo X (`tab:feature_degradation`) — dördü de `\ref`
almıyor. IEEE her kayan nesnenin anılmasını ister; Tablo V ve X iki ana
bölümün veri tabanı.

---

## 6. MINOR

**Sayı ve tanım**
- `04:124` "12 of 18" artefaktta **14/18** (`max: 2 + min: 12`); ya 14 yazın
  ya "the *minimum* in 12 of 18" deyin. 14 kendi savınızı güçlendirir.
- `04:400` "three times as far" — parantezdeki minimumlarla oran
  (1−0,9343)/(1−0,9840) = **4,12**; blok ortalaması 3,61. Hangi tanım
  kullanıldığı yazılsın. *(Bu proje "yirmi kat" hatasını bir kez yaşadı.)*
- Özet "3,3 kat" — pay ve payda aynı nicelik ve aynı ölçü olduğu için K2
  yasağına girmiyor, ama ikisi de 3 tohum ortalaması ve orana aralık
  verilmiyor. Mutlak dil yeğlenmeli.
- SVHN tablosunda ± değerleri **n=2**'den, tek serbestlik dereceli; 0,01 gibi
  bir değer "çok kararlı" izlenimi yaratıyor. Başlıkta not düşün.
- Holm kapsamı tutarsız: üç seyreklik ölçüsüne uygulanmış, dört uzamsal
  ölçüye ve koşumlar arasına uygulanmamış.
- `p < 10^-84` örnek düzeyinde; bilimsel iddianın birimi eğitim koşumu (n=3).
  Tek cümlelik niteleme yeterli.
- Tablo II ile Tablo III aynı yönler için farklı sayı veriyor
  (41,02±0,55 vs 41,07±0,58) — ayrı saldırı koşumları, açıklanmamış.
  **Dipnot bu kusuru kanıta çevirir:** *"matris bağımsız PGD rastgele
  başlangıçlarıyla ayrı bir koşumda hesaplandı; 0,06 puanlık farklar §4.9'da
  bildirilen saldırı-tohum varyansıyla (≈0,05) uyumludur."*
- Fig. 2'nin ε=8/255 noktası (44,19±0,59) Tablo I ile (44,11±0,50) uyuşmuyor
  — ayrı PGD koşumu.

**Yeniden üretilebilirlik**
- `scripts/generate_journal_figs_c1.py` **hiç tohum sabitlemiyor** (tek
  `manual_seed`/`np.random.seed` yok), oysa `03:144` *"All evaluation and
  analysis scripts fix random seeds (seed 42, including CUDA determinism
  flags), so every reported number is reproducible"* diyor. Cümle şu an kod
  tarafından desteklenmiyor.
- Kapı kapsaması: makalede **400 benzersiz değer** (347 ondalıklı); kapı 137
  kontrol = **124 benzersiz değer**. **233 ondalıklı değer kapı dışında
  (%67)** — Tablo I'in tüm hücreleri, 3×3 matris, uzamsal tablo, 12 bloklu
  sürüklenme tablosu dâhil. Tablo I'in tek bir hanesini değiştirseniz beş
  kapının beşi de yeşil kalır. *(İzlenebilirlik hakemi ~60 kapı-dışı değeri
  elle doğruladı; 58'i tuttu.)*
- `KOKEN.json`'daki **23 artefaktın 23'ü de hash'i tutuyor** [✓], ama defterde
  **olmayan** taşıyıcı artefaktlar var: `c1_eval_summary.json` (Tablo I),
  `c1_behavior_summary.json`, `c1_c45_summary.json`, `c1_c2/*/tgr_summary.json`,
  `c1_a5/*`, `c1_statval/*`, `stat_addendum.json` + 13 figür + 6 kontrol noktası.
- **0 baytlık kontrol noktası:**
  `models/q1/cifar100/vit_tiny_s2002/.../epoch_009.pth`. Sonucu:
  `testcurve_vit_tiny_s2002.npz` epok 1–31 arasında **yalnız 9'u içermiyor**.
  `q1_b8_secim_bandi.py:88` `np.intersect1d` ile deliği sessizce düşürüyor;
  muhafız `if ortak.size < 4` ayırt edici değil. Dahası `smooth()` düzgün
  ızgara varsayıyor, yani k=3/5 penceresi epok 8 ile 10'u komşu sayıyor.
  CIFAR-100 seçim yayılımı manşeti bu tohumu içeriyor.
- **Yanıltıcı artefakt adlandırması:** `results/transfer_analysis_clean/`
  içindeki dosyalar `per_sample_ResNet18_AT_to_ViT_Tiny_AT.npz` adını taşıyor
  ama `model_paths` = `models/resnet18/clean/best.pth`. **AT olmayan modeller
  `_AT` etiketiyle diskte.** Toplulaştırıcıların çoğu dosya adından `src`/`tgt`
  çıkarıyor; bir `glob` genişletmesi sessizce temiz modelleri AT havuzuna sokar.

**Biçim ve gönderim**
- Biyografi *"currently pursuing the **M.Sc.**"*, yazar dipnotu *"**Ph.D.**
  student"* — aynı sayfada çelişki.
- `\begin{IEEEbiography}[]{...}` boş köşeli parantez → **boş fotoğraf çerçevesi**
  üretir. Ya gerçek fotoğraf ya `IEEEbiographynophoto`.
- Kullanılmayan paketler: `algorithmic`, `multirow`, `xcolor`, `array`; ayrıca
  `cleveref` yüklü ama **hiç `\cref` yok**.
- 11 denklem numaralı, yalnız **biri** metinde anılıyor.
- Veri/Kod bildirimi yalnız **CIFAR-10**'u anıyor; CIFAR-100 ve SVHN yok.
  Ayrıca bildirim *"upon acceptance"*, Sonuç *"We release"* diyor — **ikisi
  aynı anda doğru olamaz** (depo kararınızla da bağlantılı).
- `main.tex:71`'de canlı `% TODO(submission): repo URL` yorumu.
- §2.1 ve §2.2, §3.3 ve §3.4 ile birebir tekrar ediyor (FGSM/PGD/TRADES ders
  kitabı tanımları iki kez, denklemleriyle). **Kesilecek yer burası** — ~¾
  sayfa kazanç, S4'ün şekil büyütmesini karşılar.
- `figures/final/` içinde makaleye hiç girmeyen 6 eski dosya var; buna karşılık
  **`fig_e3_kalibrasyon.pdf` var ve kullanılmıyor** — §4.2 makalenin en yoğun
  sayısal pasajı ve tek görseli yok. Etiketleri İngilizceye çevirip eklemek
  o pasajı okunur kılar.
- Özet "conditional-**sensitivity**" diyor, gövde beş yerde "conditional
  **susceptibility**"; "sensitivity" gövdede hiç geçmiyor.

---

## 7. Hakemler arasındaki uyuşmazlıklar — kodla hakemlendi

**(a) Doğrulama bölmesi çelişkisi.** İddia-kanıt hakemi §3.5 ile §4.3'ü
"doğrudan çelişki, MAJOR" ilan etti; tasarım hakemi aynı yeri MINOR gördü.
`scripts/q1_pipeline.sh:119-136`'ya baktım [✓]:

```bash
train_pair_member() { local ds arch seed val_json ...
    train clean       ... --val-indices "$val_json"
    train adversarial ... --val-indices "$val_json"
```

Aynı bölme her iki aşamada da **eğitimden çıkarılıyor**. Sızıntı yok; §3.5
doğru. §4.3'ün cümlesi teknik olarak doğru ama "kullanılan" sözcüğü "seçim
için kullanılan"ı kastederken okuyucu "üzerinde eğitilen" diye anlıyor.
**Hüküm: MINOR yazım kusuru** — kodu okuyan tasarım hakemi haklı. Yine de
düzeltilmeli: tezi sızıntı olan bir makalede bu cümle kendi ayağına sıkıyor.
Önerilen: *"the same held-out split serves selection at both stages, rather
than two independent splits."*

**(b) Karantina ihlali.** İzlenebilirlik hakemi "ihlal YOK" dedi ve `.tex`
kaynaklarını, figür üretici betiklerini, her iki dildeki yedi bölümü taradı —
bulduğu iki eski-koşum sayısı da açıkça etiketliydi. Sunum hakemi ise figür
**PDF'lerini** açtı ve İngilizce şekillerde karantina değerleri buldu.
İkisini de doğruladım [✓]: **metin temiz, şekiller değil.** İki hakem de kendi
kapsamında haklı; ders şu — **kapılar PDF içeriğini taramıyor.**

---

## 8. Doğrulanan güçlü yanlar

Bunlar rapora bilerek konuluyor: hakem cevap mektubunda bunlara dayanabilirsiniz
ve sonraki turda yeniden sorgulanmasınlar diye.

**Ön kayıt disiplini — makalenin en savunulabilir yanı.** Tasarım hakemi
`git show --numstat` ile denetledi: `E1_PILOT_KAPISI.md` 10 commit, **hepsinde
0 silme**. `E6_ON_KAYIT.md` **tek commit**, 2026-08-20 16:52; ilk L2 sonucu
2026-08-21 06:45 — veri görülmeden yazıldığı **git ile kanıtlı**.
`E2_ISTATISTIK_PROTOKOLU.md`'deki iki silme, kendi içinde tarihli düzeltme notu
taşıyan belge hatalarıdır, hedef/eşik değişikliği değil. **Veri görüldükten
sonra eklenmiş hedef/eşik bulunamadı.**

**C1 sızıntı düzeltmesi gerçekten öyle.** `data/val_split_indices.json` (tohum
777, 2000 indeks, tekrar yok); `src/data/datasets.py:148-158` dosyayı okuyup
eğitim indekslerinden çıkarıyor, dataset etiketi uyuşmazsa hata veriyor.
Düzeltmenin anlatıyı değiştirdiği de doğru: `old_run3_diff` alanları
(hedef-doğru 0,63 → 4,36; her-ikisi-doğru 5,33 → 8,27) makaledeki ‡ sütunuyla
birebir.

**Oran manşetinin gerekçeli reddi.** §4.9 *"χ² aralığı 0,5'ten 6,3'e uzanıyor
ve birimi içeriyor"* — `variance_ratio.json`'da birebir doğrulandı. n=3'te
oran manşeti yapmama kararı, çoğu makalenin yapmadığı doğru karardır.

**Metinde karantina ihlali yok.** Bilinen 17 karantina değeri her iki dildeki
yedi bölümde ve üretici betiklerde arandı: **etiketsiz tek örnek yok.** Eski
koşum sayıları yalnız iki yerde ve ikisi de açıkça etiketli.

**Yörünge sabitliği (E2).** `q1_offline_select.py` epok başına deterministik
tohum kullanıyor; 18 hücre **aynı ağırlıklara** çevrimdışı seçim kuralı
uyguluyor; 18 gerçekten 18. Yumuşatma konvansiyonu duyarlılığı da koşulmuş
(`edge`/`zero`/`valid` 108/108 hücrede özdeş).

**Tehdit modeli uygulaması.** AutoAttack `version='standard'`; chunking her
parçaya `seed+k` veriyor ve §4.9'da beyan edilmiş. TGR ve MI-FGSM **aynı
`mifgsm()` fonksiyonundan** çağrılıyor, tek fark hook'lar; ε/α/adım/momentum
özdeş. **Bütçe eşlemesi kusursuz.**

**SVHN önlemleri koddan doğrulandı.** `flip: False`; `split="train"` (extra-604k
yok); eps-warmup canlı ve değerlendirmeyi etkilemiyor; stratified olmaması
kasıtlı ve ön kayıtta gerekçeli.

**Atıf–iddia uyumu.** 58 `\cite`, 58 künye, öksüz yok, eksik yok. Ravikumar,
Mahmood, Bai, Benz nitelemelerinin hepsi kaynaklarına karşı doğrulandı ve
doğru çıktı. Önceki turlardaki beş referans hatasına benzer hata bulunamadı.
Gu et al. ve Fu et al.'in **yama tehdit modelinde** olduğunun açıkça
söylenmesi straw man'den kaçınmanın örnek biçimidir.

**EN–TR aynası sağlam.** İki metnin sayı kümesi birebir örtüşüyor; bir dilde
nitelenip diğerinde nitelenmemiş iddia **bulunamadı**. *(Tek istisna: EN'de
"third decimal" ifadesi yanlış — fark ikinci ondalıkta; TR bu cümleyi hiç
içermiyor, yani TR doğru olan.)*

**Sınırlılıklar bölümü.** Hakemin soracağı soruların çoğunu önceden
karşılıyor. §4.3'teki *"kaydedilen bant, kaydedildiği veri kümesinin seçim
gürültüsünün altında bir marjla tuttu"* itirafı nadir görülen bir dürüstlüktür.

**Derleme temiz.** 0 LaTeX Warning, 0 tanımsız referans, 1 kabul edilebilir
`Overfull \vbox`.

---

## 9. Öncelik sırası

**Bildiri bu hafta gidiyorsa:** B2 bildiriyi de etkiliyor ("+4,4 ile +14,6,
3,3 kat"). Karar verilmeden gönderilmemeli.

**Dergi gönderimi için sırayla:**

1. **B1** — EN şekil kümesini TR üretim yolundan yeniden üretin. Tek adım;
   B1, Şekil 4 altyazı çelişkisi ve S2'nin sayı kısmını birlikte çözer.
2. **B2** — `successful-source` tanım/kod uyumu ve türev sayıların yeniden
   üretimi (Tablo III, §4.2, iki-sürücü eğimi, Özet, Giriş, Sonuç, bildiri).
3. **B3** — Tablo VIII native-ViT sütunu: artefakt üretin ya da kaldırın.
4. **K1, K2, K3, K4, K5** — manşet sayıların yeniden tanımlanması ve özdeşlik
   payının raporlanması. Bunlar makaleyi küçültür ama **savunulabilir** kılar;
   kırmızı takımın kendi ifadesiyle: *"doğru manşet daha küçük, daha
   savunulabilir ve hâlâ yayımlanabilir."*
5. **İ1, İ2, İ3** — negatif sonuçları pozitif sonuçlarla aynı titizlikte test
   edin (koşum düzeyi çıkarım, entropi TOST'u, marjların yazılması).
6. **İ4, İ5, İ6** — yayılım ayrıştırması, küçük-G düzeltmesi, L2'deki r'nin
   nitelenmesi.
7. **L1–L4** — atıfsız hedefler, Mahmood karşıtlığı, eksik beş kaynak, estimand
   paragrafı.
8. **S1–S5** — üslup hasarı, altyazı hizalaması, özet kısaltma, şekil
   büyütme, kayan nesne atıfları.
9. **MINOR listesi** — özellikle figür tohumu, kapı kapsaması, 0 baytlık
   kontrol noktası ve `_AT` adlandırma tuzağı.

---

## 10. Kapılar hakkında çıkan ders

Beş kapı da geçiyordu ve bu raporda üç gönderim-durduran kalem çıktı. Kapıların
kapsamadığı üç alan:

| Alan | Kanıt |
|---|---|
| **Şekil PDF içeriği** | B1: şekiller tabloları yalanlıyor, hiçbir kapı görmedi |
| **Tablo hücreleri** | Makaledeki 400 değerin 233'ü (%67) kapı dışında |
| **Tanım–uygulama uyumu** | B2: metin bir şey diyor, kod başka şey yapıyor |

Kapılar **anlatı sayılarını** koruyor; tablolar, şekiller ve tanımlar
savunmasız. Bu, kapı mimarisinin bir sonraki turda genişletilmesi gereken
yönüdür.

---

*Rapor salt-okur hakemlikten üretildi; depoda hiçbir dosya değiştirilmedi.
`[✓ doğrulandı]` işaretli bulgular artefaktlar açılarak bağımsız olarak
yeniden hesaplandı.*

---

# 11. KAPANIŞ — 2026-08-24 akşamı

Rapordaki her madde **uygulanmadan önce artefakta ya da koda kadar
doğrulandı.** Doğrulama sırasında **dört hakem iddiası çürüdü**; bunlar
düzeltilmedi, çünkü kusur değildi.

## Çürüyen hakem iddiaları

| İddia | Hakem | Ölçüm | Hüküm |
|---|---|---|---|
| Tablo VIII'in native-ViT sütununun arkasında artefakt yok | izlenebilirlik | `rev2_blockA/a3_per_sample.npz`: hoyer 0,4046 · gini 0,5712 · rel 0,1785; `a3_gradient_paired.json`: hizalanma 0,0799 — **dördü de tutuyor** | ÇÜRÜDÜ (JSON'da yuvarlanmış dize aranmış, npz açılmamış) |
| 0,405 temiz ViT'ten kopyalanmış olabilir | izlenebilirlik | temiz ViT 0,40594 → **0,406**'ya yuvarlanır; native ViT 0,4046 → 0,405 | ÇÜRÜDÜ |
| §3.5 ile §4.3 doğrudan çelişiyor (MAJOR) | iddia-kanıt | `q1_pipeline.sh:119-136` aynı bölmeyi **her iki aşamada da eğitimden çıkarıyor**; sızıntı yok | MINOR yazım kusuruna indirildi (tasarım hakemi haklıydı) |
| Şekil 8b 8 örneklik partiden çizilmiş | sunum | `fig5b` zaten `results/c1_c4` okuyor (n=1000, 3 koşum). Eski `attention_entropy_fig.json`'ı **hiçbir aktif betik okumuyor** | ÇÜRÜDÜ (gerçek eksik: altyazı n'i söylemiyordu) |
| L2'de yalnız 3 ayrık hedef-hatası değeri | kırmızı takım | ölçüldü: **7** ayrık değer, altısı aynı WRN | Endişe geçerli, sayı yanlış; metne ölçülen sayı yazıldı |

## Hakemlerin kaçırdığı, doğrulama sırasında çıkan iki bulgu

**Aynı görsel iki kez basılıyordu.** `fig4_gradient_comparison.pdf` ile
`fig4a_gradient_visualization.pdf` **birebir aynı dosya**; üretici aynı şekli
iki ada yazıyor. Makale onu bir kez tam sütunda, bir kez 0,32× ölçekte
okunamaz halde gösteriyordu. Altı hakemin hiçbiri görmedi.

**SVHN makalede kaynaksız kullanılıyordu.** Ne metinde tek bir atıf ne de
`references.bib`'de künye vardı.

## Kapatılan kalemler

| # | Kalem | Commit |
|---|---|---|
| B1 | EN şekilleri artık Tablo I ile tutuyor; üretici determinist | `a7dc2f4` |
| B3 | Sütun izlenebilir çıktı; köken (test kümesinde seçim) beyan edildi | `d985344` |
| İ1 | Maks-p yerine koşum düzeyi çıkarım; sonuç **daha güçlü** (dördün üçü → dördü de anlamsız) | `d985344` |
| İ2 | Entropi null'u TOST ile desteklendi: 12/12 katmanda eşdeğerlik kabul | `2a75fa8` |
| İ3 | TOST marjları yazıldı (±2 birincil, ±1/±3 duyarlılık) | `3050197` |
| İ4 | Seçim yayılımı ayrıştırıldı (18 hücre vs çekirdek 1,09×/1,42×) | `3050197` |
| İ5 | Küçük-G ve küme bağımsızlığı uyarıları | `8a7ee13` |
| İ6 | L2'deki r kaldırıldı, eğim bırakıldı, gerekçe yazıldı | `3050197` |
| K2 | Özdeşliğin genel formu; öncül ölçülebilir koşula bağlandı | `2a75fa8` |
| K5 | SVHN'de onaylanan iki protokolün uyuştuğu yazıldı | `2a75fa8` |
| L1 | Atıfsız "çürütülen iddia" çerçevesi düşürüldü | `2a75fa8` |
| L2 | Mahmood karşıtlığıyla yüzleşildi | `2a75fa8` |
| L3 | Carlini 2019 + Tramèr 2020 eklendi ve ayrım yazıldı | `2a75fa8` |
| L4 | "Estimand" itirazı adıyla karşılandı | `2a75fa8` |
| S1 | Dört üslup hasarı (iki dilde) | `d3e29d8` |
| S2 | Üç altyazı şekille hizalandı | `d985344` |
| S3 | Özet 419 → 260 kelime; kapıya uzunluk denetimi | `2a75fa8` |
| S4 | Tekrarlanan ve okunamayan alt şekiller kaldırıldı | `8a7ee13` |
| S5 | Dört atıfsız kayan nesneye atıf | `3050197` |
| MINOR | 12/18→14, "üç kat"→4,1, SVHN künyesi, biyografi, paketler, veri beyanı, 4.3 ifadesi | `d3e29d8` |
| — | Sessiz epok deliği bildiriliyor; köken defteri 23 → 42 artefakt | `8a7ee13` |

## Açık kalan iki kalem

**B2 — `successful-source` maskesi.** Kullanıcı kararı bekliyor: maskeyi
sıkılaştırmak (asimetri 14,60 → 19,36, yayılım → 15,00, oran → 4,44 kat;
bildiri dâhil tüm manşetler değişir) ya da tanımı koda uydurmak.

**K1, K3, K4 — manşetin yeniden çerçevelenmesi.** Bunların sayıları B2'ye
bağlı: maske sıkılaşırsa yayılım 10,24 → 15,00 olur ve özdeşlik payı da
değişir. B2 kararından sonra birlikte yapılmalı.

**Depo vaadi** (bkz. `results/q1_research/TESLIM_DURUMU.md` §2b).
