# Çalışmanın hikâyesi — poster ve özet çizim için kapsamlı rapor

> **Kime yazıldı.** Bu rapor, çalışmayı **hiç makine öğrenmesi bilmeyen** bir
> akademisyene anlatabilmek için yazıldı. Her bölümün sonunda *"bunu nasıl
> çizersin"* notu var. Tüm sayılar `results/C1_REFERANS_FOYU.md`'den gelir
> (karantina kuralı); rapor onların yerine geçmez, onları anlatır.
>
> Depo: `q1` dalı · Belge tarihi: 2026-08-25

---

## 1. Tek cümle

**Aynı iki modeli, aynı veriyle, aynı saldırıyla ölçtüğünüzde bile, "hangi
mimari daha dayanıklı" sorusunun cevabı, makalelerin çoğunun hiç yazmadığı
bir seçime — *kimin sayıldığına* — bağlı çıkıyor; ve o seçimin etkisi,
modelleri sıfırdan yeniden eğitmenin etkisinden on kat büyük.**

---

## 2. Neden bu, sizin alanınızı da ilgilendiriyor

Yapay zekâ terimlerini bir kenara bırakın. Şu ikisi aynı problemdir:

| Sizin alanınızdan tanıdık hâli | Bizim alanımızdaki hâli |
|---|---|
| Bir ilacın "yanıt oranı", **tedaviyi tamamlayanlarda mı** yoksa **başlayan herkeste mi** hesaplanıyor? (per-protocol / intention-to-treat) | Bir saldırının "başarı oranı", **modelin zaten bildiği örneklerde mi** yoksa **tüm örneklerde mi** hesaplanıyor? |
| "Vaka ölüm hızı" — paydaya kim vaka sayılıyor? | "Transfer oranı" — paydaya hangi görüntü giriyor? |
| "İşsizlik oranı" — iş aramayı bırakan kişi işgücünde sayılıyor mu? | "Yanıltma oranı" — modelin temiz görüntüde de yanıldığı örnek sayılıyor mu? |

Hepsinde ortak olan şey şu: **pay aynı, payda tartışmalı.** Ve payda
tartışması yazılmadığında, iki dürüst araştırmacı aynı veriden farklı sonuç
çıkarır, üstelik ikisi de aritmetik olarak haklıdır.

Bizim katkımız bu genel gerçeği tekrar söylemek değil. **Onu ölçmek.** Kaç
puan? Hangi koşulda işaret bile değişir? Ve etkisi, alanın gürültü saydığı
şeylerin (tohum, yeniden eğitim) yanında nerede duruyor?

> **ÇİZİM 1 — açılış paneli.** İki bilim insanı, aynı veri yığınına bakıyor,
> ellerinde aynı grafik, ama konuşma balonlarında farklı sonuçlar. Aradaki
> tek fark: birinin elindeki elekte küçük delikler, ötekinde büyük. Alt
> yazı: *"Aynı veri. Aynı saldırı. Farklı elek. Farklı sonuç."*

---

## 3. Kurulum — üç cümlede

İki görüntü sınıflandırma modeli var: bir **CNN** (ResNet-18, konvolüsyonel
sinir ağı) ve bir **ViT** (ViT-Tiny, görü dönüştürücüsü). İkisi de aynı
"çekişmeli eğitim" tarifiyle sertleştirildi; yani eğitim sırasında bilerek
bozulmuş görüntüler gösterilerek saldırıya karşı dirençli hâle getirildi.
Sonra ikisine de aynı saldırı uygulandı: görüntünün her pikselini en çok
$8/255$ (yani gözle neredeyse fark edilmeyecek kadar) oynatma izni.

Kritik olan şey: **her şey sabit tutuldu.** Aynı model çifti, aynı veri,
aynı tehdit modeli, aynı saldırı bütçesi, mimari başına üç bağımsız eğitim
koşumu, tam test kümesi (10.000 görüntü), her örneğin sonucu tek tek
kaydedildi. Değişen tek şey **puanlama kuralı** oldu.

> **ÇİZİM 2 — kurulum şeması.** Solda iki kutu: "CNN" ve "ViT". Ortada bir
> saldırı oku. Sağda dört farklı elek/huni, hepsi aynı sonuç yığınından
> besleniyor ama farklı sayılar üretiyor. Sabit tutulanları kilit ikonuyla,
> değişen tek şeyi (elek) renkli göster.

---

## 4. Dört elek — makalenin kalbi

Bir saldırı "kaynak" modelde üretilip "hedef" modele uygulandığında,
"hedefin kaçta kaçı kandı" sorusunun **dört yerleşik cevabı** var. Fark
yalnızca paydada:

| Elek (protokol) | Paydaya kim giriyor | Kaç görüntü |
|---|---|---|
| **Koşulsuz (ham)** | herkes | 10.000 |
| **Hedef doğru** | hedefin temiz görüntüde bildiği örnekler | 7.353 / 8.579 |
| **Her ikisi doğru** | hem kaynağın hem hedefin bildiği örnekler | 7.061 |
| **Başarılı kaynak** | saldırının kaynakta gerçekten işe yaradığı örnekler | 2.831 / 3.814 |

Dördü de literatürde kullanılıyor. Dördü de savunulabilir. Ve dördü **aynı
deneyden farklı sayılar** veriyor:

| Elek | CNN→ViT asimetrisi |
|---|---|
| Hedef doğru | **+4,4** puan |
| Her ikisi doğru | **+8,3** puan |
| Koşulsuz | **+13,6** puan |
| Başarılı kaynak | **+19,4** puan |

**Yayılım: 15,0 puan. En büyük ile en küçük arasında 4,4 kat.**

Karşılaştırma noktası: her iki modeli sıfırdan yeniden eğitmek aynı büyüklüğü
yalnızca **1,3 puandan az** oynatıyor. Yani *ölçüm seçimi*, alanın "gürültü"
sayıp raporladığı *eğitim rastgeleliğinden* on kattan fazla büyük.

> **ÇİZİM 3 — posterin ana görseli.** Yatay bir sayı doğrusu, 0'dan 20'ye.
> Üstünde dört nokta: 4,4 / 8,3 / 13,6 / 19,4 — her biri kendi elek ikonuyla.
> Altında minicik bir aralık: "yeniden eğitmek: 1,3 puan". İki aralığın boy
> farkı posterin en güçlü tek görseli olur. Başlık: *"Aynı deney, dört
> cevap."*

---

## 5. Sonucun tamamı bir aritmetik: özdeşlik

En "masum" görünen elek — koşulsuz oran — aslında ölçtüğünü ölçmüyor. Onu
kullanan bir çalışma, hedefin **kendi hatasını** transfer başarısı sanıyor.

Bu, bir eğilim değil bir **özdeşlik**:

$$r_{\text{ham}} - r_{\text{koşullu}} = e \cdot (1 - r_{\text{koşullu}})$$

Burada $e$ hedefin temiz hata oranı. Yani ham oran, koşullu oranın üstüne
hedefin kendi zayıflığını **bilinen bir oranda** ekliyor. WideResNet-28-10
referansının da eklendiği $3\times3$'lük matriste, 36 ölçülen yönde bu
bağıntı **0,41 puandan küçük hatayla** tutuyor.

**Bunun pratik değeri:** yayımlanmış herhangi bir ham transfer oranı, hedefin
temiz doğruluğu biliniyorsa **geriye dönük düzeltilebilir.** Bilinen nitel bir
uyarı ("ham oran karışıktır"), uygulanabilir bir formüle dönüşüyor.

> **ÇİZİM 4 — özdeşlik.** Bir çubuğun iki renkli parçaya bölünmesi: alt parça
> "hedefin kendi hatası", üst parça "gerçek transfer". Yanına küçük bir
> formül. Altına: *"Ham oran bu ikisinin toplamıdır — ve payları
> hesaplanabilir."*

---

## 6. İşaretin çevrildiği yer: SVHN

CIFAR-10 ve CIFAR-100'de iki mimari temiz doğrulukta epeyce ayrışıyor (≈12 ve
≈21 puan). Orada **yön** kararlı: CNN'de üretilen saldırılar ViT'e daha iyi
geçiyor, dört eleğin dördünde de, üç tohumun üçünde de.

Ama **SVHN**'de (sokak numaraları veri kümesi) aynı tarif iki mimariyi yalnız
**1,85 puan** ayırıyor. Ve orada:

| Elek | Sonuç |
|---|---|
| Hedef doğru | **ViT** lehine (−1,00) |
| Her ikisi doğru | **ViT** lehine (−0,35) |
| Koşulsuz | **CNN** lehine (+0,39) |
| Başarılı kaynak | **CNN** lehine (+2,70) |

**İkiye iki.** Yalnızca bir eleği raporlayan iki çalışma, birbirinin tam
tersini söyler ve ikisi de doğrudur.

Üstelik koşulsuz orandaki çevrilme **öngörülebilir**: §5'teki özdeşlik,
ViT hedefinin temiz hatası CNN'inkini ~2 puan aştığında $-1{,}00$'lik koşullu
farkın $+0{,}39$'a taşınacağını önceden söylüyor.

> **ÇİZİM 5 — işaret çevrilmesi.** Bir terazi. Sol kefede ViT, sağda CNN.
> Dört farklı elek, terazinin dilini dört farklı yöne çeviriyor; ikisi sola
> ikisi sağa. Alt yazı: *"Modeller eşitlendiğinde işarete protokol karar
> veriyor."*

---

## 7. Kendi ilacımızı içtik: bir protokol adı, tanım değildir

Bu makalenin en dürüst — ve poster için en çarpıcı — anı şu:

Yukarıdaki dört elekten biri "başarılı kaynak" adını taşıyor. Ama *"saldırı
kaynakta başarılı oldu"* ifadesi tek başına bir tanım değil. Kaynağın temiz
görüntüde **doğru bilmesi** gerekiyor mu, yoksa sadece bozuk görüntüde
yanılması yeterli mi? Transfer literatürü bunu neredeyse hiç yazmıyor.

Biz **kendi boru hattımızda** bu iki okumanın ayrıştığını bulduk. Sıkı okuma
(kaynak temizde doğru **ve** bozukta yanlış) ile gevşek okuma arasındaki fark:

- CIFAR-10 asimetrisi: **19,37 → 14,60** puan
- Protokol yayılımı: **15,01 → 10,45** puan
- Kayma: **4,77 puan** — Tablo III'teki *her* protokolün koşumlar arası
  standart sapmasının **üç katından fazla**

Yani bir protokolün **adının altındaki yazılmamış bir alt seçim**, makalenin
tezinin ikinci dereceden bir örneğini üretiyor. Bunu düzelttik, sıkı tanımı
raporluyoruz, gevşek varyantı ölçülmüş duyarlılık olarak yazıyoruz, ve dört
maskenin tamamını yayımlanan kodda **tek bir yerde** tanımlıyoruz.

> **ÇİZİM 6 — özyineleme.** Bir elek resminin içinde, daha küçük iki elek.
> Alt yazı: *"Protokolün adı bir tanım değildir. Adın içinde de bir seçim
> var."* Bu panel posterin "aha" anıdır.

---

## 8. Ne bulmadık — üç negatif sonuç

Bir makalenin güvenilirliği, bulmadıklarını yazıp yazmadığından anlaşılır.
Üçünü yazdık:

1. **Seyreklik, mekânsal lokalite değildir.** Çekişmeli eğitilmiş CNN
   gradyanları kütlenin daha çoğunu daha az bileşene yığıyor (Hoyer 0,493'e
   karşı 0,456; eşleştirilmiş $p<10^{-11}$). Ama aynı gradyanların **dört
   mekânsal ölçütünden üçü sıfır sonuç** verdi: bu bileşenlerin görüntüde
   *nerede* durduğunda fark yok. Yani "CNN gradyanları daha lokalize" demek
   veriyle desteklenmiyor; yalnızca "daha seyrek" denebilir.
2. **Dikkat entropisi saldırı altında ölçülebilir biçimde değişmiyor.**
   $n=1000$ örnekte, tüm katmanlarda değişim $|\Delta| \le 0{,}0045$ nat.
   Bunu "reddedemedik" diye değil, eşdeğerlik testiyle (TOST) **eşdeğerlik
   kabul edildi** diye raporluyoruz — 12 katmanın 12'sinde.
3. **ViT'e özgü saldırı (TGR) bu rejimde kazanç vermiyor.** Eşleşmiş bütçede
   düz MI-FGSM'e kaybediyor (her ikisi doğru transfer: 7,93 vs 10,08).

> **ÇİZİM 7 — negatif sonuçlar.** Üç kutu, her birinde büyük bir "≈" (fark
> yok) işareti ve altında tek satır açıklama. Poster için sakin, gri tonlu
> bir bant; renkli panellerin arasında nefes aldırır.

---

## 9. Ayakta kalan iki davranış farkı

Her şey negatif değil. İki fark bağımsız kontrol noktası kümelerinde
tekrarlanıyor:

- **Gradyan yapısı.** CNN gradyanları daha seyrek (üç ölçütte de,
  Holm düzeltmeli), ViT'inkiler örnekler arasında daha hizalı (mutlak
  kosinüs 0,056'ya karşı 0,038). Ama **işaretli** ortalama kosinüs iki
  modelde de sıfıra yakın ($\le 0{,}0014$): paylaşılan şey ortak *yönler*
  değil, ortak *duyarlılık eksenleri*.
- **Hasarın biriktiği derinlik.** ViT'te bozulma kademeli ve sığ: benzerlik
  8-10. bloklar civarında en düşük noktasına (0,934) inip çıkışa doğru
  toparlanıyor, öznitelik normları baştan sona temiz değerin %0,7'si içinde
  kalıyor — yani pertürbasyon temsilin **yönünü** bozuyor, **büyüklüğünü**
  değil. CNN'de hasar yoğunlaşmış: son artık aşamanın ilk bloğunda kosinüs
  0,878'e çöküyor ve norm %13 daralıyor, sonra son blok kısmen onarıyor.

> **ÇİZİM 8 — derinlik profili.** İki eğri, yatay eksen "katman derinliği".
> ViT'inki yumuşak bir çanak, CNN'inki sonlara doğru keskin bir çukur ve
> ardından kısmi toparlanma. Tek bakışta "nerede" farkını anlatır.

---

## 10. Çalışmanın kendi hikâyesi — bilim yapma biçimi olarak

Poster için ayrı ve güçlü bir hikâye daha var: **bu çalışma kendini nasıl
denetledi.**

**Ön kayıt, salt ekleme.** Her deney kümesi koşulmadan önce ne bekleneceği
yazıldı ve o belgeler yalnızca eklenerek değiştirildi. Sonuç görüldükten
sonra eşik değiştirmek yasaklandı.

**Altı otomatik kapı.** Makaledeki her taşıyıcı sayı, artefaktlarla otomatik
karşılaştırılıyor; iki dilin yapısal aynalığı denetleniyor; özet ile gövde
tutarlılığı, bildirinin makaleyle uyumu ayrı ayrı sınanıyor.

**Kapıların kendisi de kırılarak sınanıyor.** Bu projenin en pahalı dersi:
*geçen bir kontrol, yakaladığını kanıtlamaz.* Bu yüzden her kapının bir
öz-sınaması var: metni bilerek boz, kapının **kaldığını** doğrula.

**Ve bu disiplin gerçekten ısırdı.** Protokol tanımı düzeltildiğinde:

| Ne oldu | Sonuç |
|---|---|
| Ön kayıtlı bir kestirim **tutmadı** | Kayıt sayıyı değil niceliği adlandırmıştı; kurtaran okuma seçilmedi, tutmadığı yazıldı |
| Bir anlatı **tersine döndü** | "CIFAR-100'de yayılım daha büyük" → artık CIFAR-10'un altında |
| Bir açıklama **çürüdü** | "Uyuşmazlık bileşim etkisidir" savunulamaz hâle geldi |
| Bir "her zaman" iddiası **düştü** | 18 çiftin 13'ünde doğruymuş, hepsinde değil |

Yirmi beş ajanlı bağımsız bir denetim turu daha koşuldu; her bulgu ayrı bir
denetçi tarafından **çürütülmeye** çalışıldı ve yalnız ayakta kalan yirmisi
işlendi. Bunlardan biri, bir tablonun iki satırının **2026-08-06'dan beri**
artefaktla tutmadığını ortaya çıkardı.

> **ÇİZİM 9 — süreç paneli.** Bir döngü: *ön kayıt → koş → kapıdan geçir →
> kapıyı kır ve sına → bulguyu çürütmeye çalış → kalanı yaz.* Ortada küçük
> bir uyarı: *"Geçen bir kontrol, yakaladığını kanıtlamaz."* Bu panel,
> herhangi bir daldan bir izleyicinin en çok konuşacağı yer olur.

---

## 11. Sonuç: dört raporlama gerekliliği

Makale bir sıralama önermiyor; bir **raporlama disiplini** öneriyor:

1. **Koşullama protokolünü yazın** ve paydaya kimin girdiğini söyleyin.
2. **Eşleştirilmiş protokolleri yeğleyin** (her iki yönü aynı örneklerde
   puanlayan). Yalnız o, eşleştirilmiş çıkarımı destekler.
3. **Ham oranları mimari karşılaştırması olarak sunmayın**; sunacaksanız
   §5'teki özdeşlikle düzeltin.
4. **Mutlak skoru ayrıştırın**: temiz doğruluk × koşullu duyarlılık. Tek
   sayı, hangisinin manşeti taşıdığını gizler.

> **ÇİZİM 10 — kapanış.** Dört madde, dört ikon, sade. Posterin sağ alt
> köşesi. Yanına bir cümle: *"Protokol belirtilmemişse okur, gerçek bir
> mimari farkı bir ölçüm seçiminden ayırt edemez."*

---

## 12. Poster mimarisi önerisi

Üç sütun, on panel:

| Sütun | Paneller | Amaç |
|---|---|---|
| **Sol — soru** | 1 (açılış), 2 (kurulum), 3 (dört cevap) | İzleyiciyi 15 saniyede içeri alır |
| **Orta — kanıt** | 4 (özdeşlik), 5 (işaret çevrilmesi), 6 (özyineleme) | Makalenin bilimsel ağırlığı |
| **Sağ — dürüstlük ve sonuç** | 7 (negatifler), 8 (derinlik), 9 (süreç), 10 (gereklilikler) | Akılda kalan kısım |

**Poster başlığı önerileri** (hepsi jargonsuz):
- *"Aynı deney, dört cevap"*
- *"Cevabı kim sayıldığı belirliyor"*
- *"Ölçüm, modelden daha çok konuşuyor"*

**Rakam hiyerarşisi** — posterde yalnız üç sayı büyük yazılmalı:
**4,4 kat** · **15 puan** · **1,3 puandan az**. Diğerleri destek metninde.

---

## 13. Bir dinleyicinin soracağı beş soru ve kısa cevapları

**"Yani hangi mimari daha dayanıklı?"**
Mutlak skorda CNN önde (AutoAttack altında %37,9'a karşı %29,1) ve bu üç
koşumun üçünde de McNemar testiyle kesin. Ama bunun ne kadarının temiz
doğruluk farkından, ne kadarının gerçek dirençten geldiği ayrıştırılmalı:
ayrıştırdığımızda ViT'in **koşullu** duyarlılığı daha yüksek çıkıyor
(%55,5'e karşı %48,6) — yani üstünlüğün önemli kısmı temiz doğruluk
farkından geliyor.

**"Dört elekten hangisi doğru?"**
Hiçbiri "yanlış" değil; dördü farklı soruları yanıtlıyor. Biz *her ikisi
doğru* protokolünü birincil sayıyoruz, çünkü tek o, iki yönü **aynı
örnekler** üzerinde puanlıyor ve eşleştirilmiş istatistiği mümkün kılıyor.
Ham oran ise mimari karşılaştırması için hiç uygun değil.

**"Bu, sadece küçük modellerde mi böyle?"**
Bilmiyoruz ve öyle yazıyoruz. Ölçüm üç veri kümesi ve tek bir model çifti
üzerinde. Etkinin büyüklüğünün başka mimari çiftlerinde kalibre edilmesi
gerekiyor. Mekanizma (hedefler arasındaki temiz doğruluk farkı) kurulumumuza
özgü değil, ama etkinin **veri kümeleri arasındaki sıralamasını** öngörmüyor.

**"Sonuç yeniden üretilebilir mi?"**
Dört protokolün tamamı örnek bazındaki kayıtlardan hesaplanıyor, yani
protokol karşılaştırması **yeniden eğitim gerektirmeden** tekrarlanabilir.
Kabul sonrasında analiz hattı, her tablo ve şekli üreten betikler, örnek
bazında kayıtlar, sabit bölme indeksleri ve tohum listeleri yayımlanacak.

**"Yeni bir yöntem önermiyor musunuz?"**
Hayır. Bu bir **ölçüm** makalesi. Katkı, herkesin kullandığı bir büyüklüğün
ne kadar tanıma bağlı olduğunu nicelemek ve düzeltilebilir hâle getirmek.

---

## 14. Poster için hazır sayı föyü

| Büyüklük | Değer |
|---|---|
| Protokol yayılımı (CIFAR-10) | **15,01 ± 0,84** puan |
| Yayılım oranı | **4,4 kat** |
| Yeniden eğitmenin etkisi (aynı nicelik) | **0,23 – 1,27** puan |
| Asimetri aralığı | +4,4 → +19,4 puan |
| Özdeşliğin hatası (36 yön) | < **0,41** puan |
| SVHN'de temiz doğruluk farkı | **1,85** puan |
| SVHN'de işaret bölünmesi | **2'ye 2** |
| Protokol adı içindeki alt seçimin etkisi | **4,77** puan |
| AutoAttack (CNN / ViT) | 37,93 ± 0,14 / 29,14 ± 0,40 |
| Koşullu yanıltma (CNN / ViT) | 48,58 ± 0,80 / 55,53 ± 0,50 |
| Gradyan seyrekliği Hoyer (CNN / ViT) | 0,4928 / 0,4561 |
| Mekânsal ölçütlerden sıfır sonuç veren | **4'te 3** |
| Dikkat entropisi değişimi | ≤ **0,0045** nat (12/12 katmanda eşdeğer) |

---

## 15. Nereden okunur

| İhtiyaç | Dosya |
|---|---|
| Her sayının tek kaynağı | `results/C1_REFERANS_FOYU.md` |
| Sayıların kökeni (44 artefakt, sha256) | `results/q1/KOKEN.json` |
| Ön kayıtlar | `results/q1_research/E*_*.md` |
| Protokol düzeltmesinin kaydı | `results/q1_research/B2_DURUM.md` |
| Kapı kusurları ve kapatılamayan sınır | `results/q1_research/B2_KAPI_KUSURU.md` |
| Hakem raporu | `paper/review/HAKEM_RAPORU_2026-08-24.md` |
| Denetimi tekrar koş | `bash scripts/kapilar.sh` |
