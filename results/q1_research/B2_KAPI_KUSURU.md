# Kapı kusurları — bulunanlar, kapatılanlar ve kapatılamayan sınır

> 2026-08-25. Önce B2 yeniden üretimi sırasında, sonra bağımsız bir denetim
> turunda (yirmi teyitli bulgu) ölçüldü. Hepsi aynı sınıftan: **ölçülmeyen şey
> sessizce bozulur.**

---

## 1. Beşinci kapı kördü — KAPATILDI

`scripts/bildiri_tutarlilik.py` bildirinin taşıyıcı sayılarını "otoriter
değer"lerle karşılaştırıyordu, ama o değerler betiğin içine **sabit
yazılmıştı**:

```python
("protokol ust sinir",  r"...", 14.60),
```

Kapı, koruduğu sayının bir **kopyasını** taşıyordu; artefakt değişince kaymayı
göremezdi. Ölçüldü: üst sınır 14,60 → 19,37 oldu ve kapı yine **GEÇTİ** dedi.

Öz-sınaması da yakalayamazdı: **bildiriyi** bozup kapının gördüğünü sınıyordu,
**artefaktı** bozup gördüğünü değil.

**Kapatıldı:** her otoriter değer artefakttan okunuyor; "kaç kat" iddiası
eş-varlık yerine sayısal karşılaştırılıyor; yön iddiası artefaktın işaret
desenine bağlandı. Öz-sınamaya üç kol eklendi (artefaktı boz, ikinci bir
artefaktı boz, artefaktı sil).

## 2. Özet öz-sınamasının bir kolu sessizce düşmüştü — KAPATILDI

Enjeksiyon çapası metne çiviliydi (`"a 3.3-fold spread"`); özet yeniden
yazılınca `assert` patladı, kol koşmadı ve betik yine "geçmiş" gibi göründü.
Çapa özet **ortamına** bağlandı, enjeksiyonun gerçekten yazıldığı doğrulanıyor
ve sayı-nötr bir uzunluk kolu eklendi.

## 3. Özet kapısı yanlış sebep söylüyordu — KAPATILDI

İki ayrı kusur tek sayaca yazılıyor, hepsi "gövdede bulunmayan N sayı" diye
adlandırılıyordu; uzunluk ihlalinde eksik sayı **sıfır** olduğu hâlde "1 sayı
var" diyordu. Sayaçlar ayrıldı.

## 4. İddia kapısında metin kökü ile artefakt kökü aynıydı — KAPATILDI

H1/H2 muhafızları artefakt okuyor; öz-sınama yalnız `paper/` dizinini
kopyalayıp kökü oraya çevirdiği için bozulmamış kopyada bile KALIYORDU.
`MANUSCRIPT_ROOT` (metin) ile `ARTEFAKT_ROOT` (artefakt) ayrıldı ve
öz-sınamaya "artefakt kökü boşsa H1/H2 KALMALI" kolu eklendi.

## 5. Sayı kapısı çıplak alt dize arıyordu — KISMEN KAPATILDI

Denetim ölçtü: manşet sayıya bir rakam eklendiğinde (`19.37` → `119.37`) kapı
yine **GEÇTİ** diyordu, çünkü dize hâlâ içinde geçiyordu. Daha kötüsü: **iki
kontrol yalnızca daha uzun bir sayının içinde eşleşiyordu**, yani hiç
doğrulanmıyorlardı:

| kontrol | nerede eşleşiyordu | gerçek |
|---|---|---|
| `E7 eşli GA üst` = 0,07 | gradyan tablosundaki `0.079` | metin $[-0{,}77;+0{,}06]$ yazıyordu, artefakt $[-0{,}76;+0{,}07]$ — **iki sınır da yanlıştı** |
| `E6 O1 r` = 0,999 | öznitelik tablosundaki `0.9990` | §4.6 zaten "korelasyon yerine eğim raporluyoruz" diyor — bu sayı metinde **yok** |

**Kapatılan kısım:** eşleşme artık **sayı sınırına** bağlı (öncesinde ve
sonrasında rakam olamaz). İki gizli kontrol böylece açığa çıktı; biri gerçek
bir sayı hatasıydı ve düzeltildi, öteki kaldırıldı ve yerine iddia kapısına
kararın ayakta olduğunu sınayan bir muhafız (I1) kondu.
Öz-sınama: `scripts/test_verify_numbers.sh`.

### Kapatılamayan sınır — bilinerek bırakıldı

Kapı bir **varlık** denetimidir: "bu değer metinde geçiyor mu". Bir taşıyıcı
sayı metinde birden çok yerde geçiyorsa (136 kontrolün yarıdan fazlası
böyledir), **bir geçişin bozulması ötekiler sağlamken görünmez** kalır.

Bunu kapatmak için "taşıyıcı değer daha uzun bir sayının içinde geçiyorsa
kusurdur" muhafızı denendi ve **ölçüldü: 44 yanlış alarm**. Daraltmalar da
yetmedi:

| daraltma | yanlış alarm |
|---|---|
| taşıyıcı uzunluğu ≥ 5 | 6 |
| taşıyıcı değeri ≥ 1 | 10 |
| taşıyıcı uzunluğu ≥ 6 | 0 ama `19.37` (5 karakter) kapsam dışı kalır |

Meşru örnekler: `5,2` ⊂ `95,25` · `32,6` ⊂ `32,69` · `1,00` ⊂ `1,000` ·
`2,70` ⊂ `12,70` · `25` ⊂ `49250` (posta kodu). Yani muhafız gürültüden
ayrışmıyor. **Sınır belgelenmiştir; kapatıldığı iddia edilmemektedir.**

## 6. Özet kapısına LaTeX uzunlukları giriyordu — KAPATILDI

Gövde sayı havuzu `.tex` kaynağındaki her sayısal dizeyi alıyordu. Denetim
ölçtü: özete uydurma bir `2.5 points` iddiası konduğunda kapı GEÇTİ, çünkü
gövdede `\setlength{\tabcolsep}{2.5pt}` vardı. Yani **sütun aralığı ayarı**,
bir öz iddiasının gövde karşılığı sayıldı. Biçimlendirme komutları ve uzunluk
birimleri artık havuza girmiyor. Ayrıca özet bulunamazsa kapı **sessiz
geçmiyor**, hata veriyor.

---

## 7. Ne öğrenildi

Altı kusurun altısı da şu kalıptandır: **bir denetim, denetlediği şeyin bir
kopyasına ya da onunla ilgisi olmayan bir şeye bağlıydı.** Sabit yazılmış
otoriter değer, metne çivilenmiş enjeksiyon çapası, paylaşılan sayaç,
paylaşılan kök, bağlamsız alt dize, biçimlendirme sayıları.

Bu yüzden bu projede bir kapı iki şeyi birden kanıtlamak zorundadır:
**bozulmamış girdide geçtiğini** ve **bozulmuş girdide kaldığını**. İkincisi
olmadan birincisi hiçbir şey söylemez.
