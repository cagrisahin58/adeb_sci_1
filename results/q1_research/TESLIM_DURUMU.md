# TESLİM DURUMU — çalışmadan kaç yayın çıktı, ne eksik

> **2026-08-21.** Bu belge, "hocama teslim edeceğim tek paket" hedefi için
> yazıldı. İçindeki her cümle ÖLÇÜLDÜ; hiçbiri hatırlanmadı veya varsayılmadı.
> Ölçüm komutları her bölümün sonunda duruyor, tekrar koşulabilir.
>
> Kampanya durumu için `DEVAM_TALIMATI.md`, sayılar için
> `results/C1_REFERANS_FOYU.md` tek kaynaktır. Bu belge onların yerine
> geçmez, yayın düzeyinde durumu özetler.

---

## 1. Kaç yayın çıktı? — ölçülen cevap

Beklenti "1 bildiri + 1 TR dizin + 1 SCI" idi. Ölçüm bunu doğrulamadı;
**2026-08-24'te karar verildi: iki yayın, ikisi de İngilizce.** Türkçe
ayna korunuyor ama gönderilmiyor (bkz. §2b).

| # | Çıktı | Yer | Dil | Durum |
|---|---|---|---|---|
| 1 | **Bildiri** | `paper/bildiri/` | İngilizce | 6 sayfa, IEEE conference, temiz derleniyor |
| 2 | **Dergi makalesi** | `paper/manuscript/` (EN) + `paper/manuscript_tr/` (TR) | iki dilde **aynı** makale | EN 19 s., TR 19 s., temiz derleniyor |

**Neden üç değil iki:** `manuscript/` ile `manuscript_tr/` aynı makalenin
iki dildeki taslağıdır, iki ayrı makale değildir. Kanıt:

- Bölüm ağacı satır satır ayna: 5 bölüm, 22 alt bölüm, 2 alt-alt bölüm,
  aynı sırada, aynı başlıklarla.
- `verify_manuscript_numbers.py` 137 taşıyıcı sayının **hepsini iki dilde
  de** buluyor (`EN_EKSIK=0 TR_EKSIK=0`). Aynı tablolar, aynı şekiller,
  aynı iddialar.

İkisini de yayımlamak **çift yayın** olur. Şu anki halleriyle bunlardan
yalnızca biri gönderilebilir; diğeri o dilin taslağıdır.

**Üçe çıkarmanın yolu var ama karar sizin ve hocanızın:** Q1 kampanyası
makaleye SVHN, CIFAR-100, $L_2$ tehdit modeli, özdeşlik türetimi, ön-kayıt
ve TGR'yi ekledi. Bu malzeme, iki sürümü gerçekten farklı kapsamda iki
makaleye ayırmaya yetecek hacimde. Ama bu bir **içerik ayrıştırma kararıdır**,
kendiliğinden olmuş bir şey değil; bugün itibarıyla iki metin aynıdır.

**Başka dalda iş yok.** Depoda yalnızca `main` ve `q1` var. Bildiri her
iki dalda da duruyor ve **bayt bayt aynı** (Q1 kampanyası bildiriye hiç
dokunmadı). `adeb_son/main` ikinci bir uzak depo, eski bir anlık görüntü.

```bash
git branch -a -v
git diff --stat origin/main origin/q1 -- paper/bildiri/   # boş = aynı
docker exec -w /workspace adeb_eval python scripts/verify_manuscript_numbers.py | tail -2
```

---

## 2. Bildirinin durumu — sayıları tutuyor, ama hiçbir kapı onu taramıyor

Bildiri Q1 kampanyasından önce yazıldı ve kampanya boyunca hiç güncellenmedi.
Bu yüzden "eskimiş sayı taşıyor mu" sorusu ölçüldü. **Taşımıyor:**

| Büyüklük | Bildiride | Artefaktta | Sonuç |
|---|---|---|---|
| AutoAttack ResNet / ViT | 37,93±0,14 / 29,14±0,40 | aynı | tutuyor |
| Temiz doğruluk farkı | 12,3 puan | aynı | tutuyor |
| Koşullu yanıltma CNN / ViT | 48,6 / 55,5 | 48,58 / 55,53 | yuvarlama |
| Hoyer CNN / ViT | 0,493 / 0,456 | 0,4928 / 0,4561 | yuvarlama |
| Hizalanma CNN / ViT | 0,038 / 0,056 | 0,0378 / 0,0562 | yuvarlama |
| Protokol aralığı | +4,4 ile +14,6 | 4,36 ile 14,60 | tutuyor |
| Protokol oranı | 3,3 kat | 14,60/4,36 = 3,35 | tutuyor |

Bildirinin "yön protokoller ve tohumlar boyunca kararlıdır" cümlesi de
ayakta: CIFAR-10'da dört protokolün dördü de artı işaretli. Kampanyanın
bulduğu **işaret çevrilmesi SVHN'dedir**, bildiri ise açıkça "tek veri
kümesi, tek model çifti, ön sonuçlar" diyor. Yani çürütülmüş iddia yok.

Bu ölçümü anlık bırakmamak için **beşinci kapı** yazıldı: dört kapının
hiçbiri `paper/bildiri/` altını taramıyordu.
`scripts/bildiri_tutarlilik.py` on bir büyüklüğü ve iki iddiayı denetler,
`scripts/test_bildiri_tutarlilik.sh` kapıyı kendi üzerinde kırarak sınar.

```bash
python3 scripts/bildiri_tutarlilik.py         # beşinci kapı
bash    scripts/test_bildiri_tutarlilik.sh    # kapının kendi sınaması
cd paper/bildiri && latexmk -pdf bildiri.tex  # 6 sayfa, 0 undefined
```

---

## 2b. KARARLAR — 2026-08-24'te verildi

| # | Karar | Sonuç |
|---|---|---|
| 1 | **Hedef: SCI/SCIE dergisi, TR Dizin DEĞİL** | Gönderilecek sürüm `paper/manuscript/` (İngilizce). Türkçe ayna `paper/manuscript_tr/` korunuyor ama gönderilmiyor. |
| 2 | Bildiri **ATEEC 2026**'ya, bu hafta | `paper/bildiri/`, 6 sayfa, künye düzeltildi, gönderilebilir |
| 3 | arXiv ön-baskısı **yok** | — |
| 4 | iThenticate sonradan | kullanıcı bildirecek |
| 5 | Künye: **Muş Alparslan** (asıl) + Fırat doktora öğrencisi | üç belgede de uygulandı (`fe26fb6`) |
| 6 | E5 | **kapandı** — makale zaten Sınırlılıklar'da ve Gelecek Yönelimler'de karşılıyor, ek iş yok |
| 7 | Depo **kapalı** | **AÇIK ÇELİŞKİ, aşağıya bakınız** |

### Kapanmamış tek kalem: depo vaadi

Makale üç yerde "kaynak kod, kontrol noktaları ve örnek bazında kayıtlar
kabul sonrasında herkese açık hâle getirilecektir" diyor
(`manuscript/main.tex` Data and Code Availability, `manuscript_tr/main.tex`
Veri ve Kod Erişilebilirliği, ve her iki Sonuç bölümünün son cümlesi).
Depo kapalı kalırsa bu vaat yerine getirilmemiş olur.

SCI hedefi bunu daha da bağlayıcı yapar: birçok SCIE dergisi kod/veri
erişilebilirlik beyanını gönderim formunda ayrıca soruyor ve bir hakem
"protokol karşılaştırması yeniden üretilebilsin diye yayımlıyoruz" cümlesini
okuyup depo bağlantısı ister. İki seçenek var:

1. **Kabul sonrası aç** (önerilen). Depo şimdi kapalı kalır, kabul edilince
   açılır. `models/` 36 GB olduğu için tamamı değil, yalnız analiz kodu +
   örnek bazında kayıtlar + bölme indeksleri + tohum listesi yayımlanabilir;
   kontrol noktaları "istek üzerine" olarak nitelenir. Metinde küçük bir
   düzeltme gerekir.
2. **Vaadi geri çek.** Üç yerdeki cümle "veri kümeleri herkese açıktır,
   analiz kodu makul istek üzerine sağlanacaktır" biçimine çekilir. Dürüst
   ama hakem gözünde zayıf durur.

**KAPANDI (2026-08-25): 1. seçenek uygulandı.** Vaat geri çekilmedi,
**kapsamı yazıldı.** Kabul sonrasında yayımlanacak küme, makaledeki her sayıyı
yeniden üretmeye yetendir: analiz hattı, her tabloyu ve şekli üreten betikler,
örnek bazında değerlendirme kayıtları, sabit doğrulama bölmesi indeksleri ve
tohum listeleri. Dört koşullama protokolünün tamamı örnek bazındaki kayıtlardan
hesaplandığı için protokol karşılaştırması **yeniden eğitim gerektirmeden**
tekrarlanabilir. Kontrol noktaları (~36 GB) "istek üzerine" olarak nitelendi.

Yol boyunca ikinci bir kusur çıktı: iki Sonuç bölümü vaadi **şimdiki zamanda**
("yayımlıyoruz") yazıyordu; depo kapalıyken bu, gönderim anında doğru olmayan
bir cümledir. Dört yerin dördü de gelecek zamana ve aynı kapsama çekildi.

---

## 2c. 2026-08-25 KARARLARI

| # | Karar | Gerekçe |
|---|---|---|
| 8 | **B2: kod düzeltildi, metin değil** | Makalenin kendi Tartışma bölümü bu protokolü "zaten işe yaramış bir saldırının ne kadar taşındığı" diye tanımlıyor; gevşek maske o soruyu yanıtlamıyordu. Ayrıntı ve kalan iş: `B2_DURUM.md` |
| 9 | **SVHN, B kolu uydurmasına girmiyor** | `E3_YENIDEN_TASARIM.md` EK E.1/E.5 bileşimi ön-kayıtla sabitliyor; sonucu gördükten sonra değiştirmek K5'i bozardı. Duyarlılık olarak raporlanacak |
| 10 | **Üç kaynak eklendi** | TA-Bench (NeurIPS 2023), Waseda vd. (WACV 2023), Yu vd. (SaTML 2025, s. 797-810) — künyeleri arXiv/DBLP'den doğrulandı |
| 11 | **Depo: kabul sonrası kapsamlı açılım** | yukarıya bakınız |

**Makale şu anda kendi kapısından GEÇMİYOR** ve bu bilerek böyle: A kolu
yeniden koşulana kadar H1/H2 muhafızları kırmızı kalır.

---

## 3. Sizden beklediklerim — CEVAPLANDI

Bu bölümdeki yedi sorunun hepsi 2026-08-24'te yanıtlandı; kararlar
§2b'deki tabloda. Açık kalan tek kalem **depo vaadi** (§2b sonu):
makale kabul sonrası yayımlama sözü veriyor, depo ise kapalı
kalacak. İki seçenek §2b'de duruyor, metin karar verilene kadar
değiştirilmedi.


---

## 4. Paket işi — bir sonraki oturumda yapılacak

Hedef: hocaya verilecek tek bir teslim paketi. İçine gireceklerin listesi
ve neden gireceği:

| Ne | Neden |
|---|---|
| Üç PDF (bildiri, makale EN, makale TR) | teslimin kendisi |
| `results/C1_REFERANS_FOYU.md` | dışarı çıkan her sayının tek kaynağı (karantina kuralı) |
| `results/q1/KOKEN.json` | 23 artefaktın sha256 köken defteri |
| Ön-kayıt belgeleri (`E1_PILOT_KAPISI`, `E2_ISTATISTIK_PROTOKOLU`, `E3_YENIDEN_TASARIM`, `E6_ON_KAYIT`, `E7_KOSUM_ONCESI_KONTROL`) | salt-ekleme disiplininin kanıtı; hakem sorarsa buradan cevaplanır |
| `Q1_ARASTIRMA_RAPORU.md`, `KAMPANYA_KARARLARI.md` | hangi kararın neden verildiği |
| Dört kapı betiği + çıktıları | sayıların denetlenebilir olduğunun kanıtı |
| Bu belge + `DEVAM_TALIMATI.md` | nerede kalındığı |

**Pakete girmeden önce kapatılması gereken tek teknik borç:** kapıların
`paper/bildiri/` altını da taraması (2. bölümdeki boşluk).

---

## 5. Bu oturumda yapılanlar

`20a77f3` — **üslup temizliği (EN+TR eş zamanlı).** Maddelendirmeler düz
paragrafa çevrildi (ana metinde artık hiç `enumerate`/`itemize` yok),
paragraf başı kalın cümle açıcıları kaldırıldı (11+11), Tartışma'daki
cümle biçimli `\paragraph{}` başlıkları kaldırıldı (5+5), altyazılar
kısaltılıp kaybolan bilgi ilgili paragrafa gömüldü (6+6), metin içi
tireler sıfırlandı (`---` 44→0 her iki dilde). Yöntem'deki 17 ad öbeği
etiketi, tablolardaki "değer yok" tireleri ve LaTeX yorum ayraçları
kasıtlı olarak korundu. Hiçbir sayı değişmedi.

`7c43081` — 16 figür PDF'i ve bir JSON çalışma ağacıyla eşitlendi. Fark
ölçüldü: en büyük sapma 0,0013 nat, yani yeniden üretim gürültüsü.

Ayrıca **Kapı 2'de bir kusur bulundu ve kapatıldı.**
`check_manuscript_claims.py` sabit host yolu okuyordu; kapsayıcı içinde o
yol yok, dolayısıyla YOKLUK kontrolleri boş metin üzerinde sahte geçiyordu.
Yol taşıyıcı-uyumlu yapıldı ve sıfır `.tex` okunursa kapı kendini hata
verir hale getirildi. Bu yeni koruma hemen ikinci bir kusuru yakaladı:
öz-sınamanın `sed` ile kaynak satırı yamayan kök enjeksiyonu, satır biçimi
değişince sessizce işlemez olmuştu; `MANUSCRIPT_ROOT` değişkenine geçirildi.

**Doğrulama durumu (hepsi bu oturumda koşuldu):**

```
verify_manuscript_numbers.py   137/137   EN_EKSIK=0 TR_EKSIK=0
check_manuscript_claims.py      31/31    host ve kapsayıcı aynı sonucu veriyor
test_claim_guards.sh             4/4     kırılma yakalandı, temiz kopya 0
check_abstract_body.py          17/17    iki dilde
test_abstract_body_check.sh      2/2     enjeksiyon yakalandı, yuvarlama alarm vermedi
q1_tr_decimal_check.py          temiz
latexmk EN                      19 sayfa, 0 undefined
latexmk TR                      18 sayfa, 0 undefined, 0 overfull
latexmk bildiri                  6 sayfa, 0 undefined
results/ altında takipsiz          0     (K7)
```
