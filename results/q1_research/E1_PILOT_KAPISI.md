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
