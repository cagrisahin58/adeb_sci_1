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

Beklenti "1 bildiri + 1 TR dizin + 1 SCI" idi. Ölçüm bunu **doğrulamıyor**.
Elde iki farklı yayın var, üç değil:

| # | Çıktı | Yer | Dil | Durum |
|---|---|---|---|---|
| 1 | **Bildiri** | `paper/bildiri/` | İngilizce | 6 sayfa, IEEE conference, temiz derleniyor |
| 2 | **Dergi makalesi** | `paper/manuscript/` (EN) + `paper/manuscript_tr/` (TR) | iki dilde **aynı** makale | EN 19 s., TR 18 s., temiz derleniyor |

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

**Ama gerçek bir boşluk var:** dört kapının hiçbiri `paper/bildiri/`
altını taramıyor. Bildirinin bugün tutuyor olması ölçümle bilindi, kapıyla
değil. Bildiri bir daha elden geçerse bu güvence yok.

```bash
python3 /home/firat/bildiri_tutarlilik.py     # bu ölçümü tekrarlar
cd paper/bildiri && latexmk -pdf bildiri.tex  # 6 sayfa, 0 undefined
```

---

## 3. Sizden beklediklerim — yalnızca sizin verebileceğiniz kararlar

Teknik engel kalmadı. Aşağıdakiler benim yapabileceğim işler değil.

**Yayın kararları**

1. **Dergi ve dil.** Hangi dergiye, hangi dilde? Bu karar 1. bölümdeki
   "iki mi üç mü" sorusunu da kapatır: tek dergi seçilirse iki yayın,
   iki sürüm gerçekten ayrıştırılırsa üç yayın.
2. **Bildiri hangi konferansa, ne zaman?** Metin hazır ve 6 sayfa
   sınırında. Gönderildi mi, gönderilecek mi bilmiyorum.
3. **arXiv ön-baskısı** konulacak mı? Teknik engel yok. Bazı dergiler
   ön-baskıyı kabul etmez, bu yüzden dergi kararından sonra verilmeli.

**Bütünlük kalemleri**

4. **iThenticate intihal kontrolü.** Hâlâ açık, koşulmadı.
5. **Künye.** Üç metin de "Fırat Üniversitesi / csahin@firat.edu.tr"
   diyor. Bu oturumdaki adresiniz `c.sahin@alparslan.edu.tr`. Doktora
   Fırat'ta yürüdüğü için bu tutarlı olabilir, ama iki kurumlu künye mi
   yoksa tek kurum mu istediğinizi ben karara bağlayamam.
6. **E5 (kapasite çifti)** K-01'de ertelenmişti. Düşürüldü mü, yoksa
   yeniden değerlendirilecek mi? Düşürüldüyse Sınırlılıklar'a bir cümle
   girmesi gerekir.

**Paylaşım kararı**

7. **Depo public olacak mı?** `models/` 36 GB ve izlenmiyor. Git LFS mi,
   yalnız `best.pth` dosyaları mı, hiç mi? Bu karar verilmeden depo
   bağlantısı makaleye yazılamaz. Dergi çift-körse anonim bir ayna
   gerekir (anonymous.4open.science).

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
