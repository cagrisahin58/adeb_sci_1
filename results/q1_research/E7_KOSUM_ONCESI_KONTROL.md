# E7-kısa — koşum öncesi kontrol listesi

**Tarih: 2026-08-20.** K-01 kararı (`KAMPANYA_KARARLARI.md`) E7'yi **kısa
sürümde** koşmaya karar verdi. Bu belge, başlatmadan önce yapılan
doğrulamaları ve bulunan tek uyuşmazlığı kaydeder.

---

## 1. BULGU — pipeline TAM sürümü koşuyor, kısa sürümü DEĞİL

`scripts/q1_pipeline.sh` `e7)` dalı şu anda:

| | pipeline'da yazılı | K-01'de onaylanan (kısa) |
|---|---|---|
| tohum | **3** (1001-1003 / 2001-2003) | **2** |
| AT epok | **100** | **50** |
| AutoAttack | yok ✓ | yok ✓ |
| tahmini maliyet | ~33-36 GPU-saat | **~11 GPU-saat** |

**Olduğu gibi `STAGE=e7` başlatmak onaylanan bütçenin ~3 katını harcar.**

**Yapılacak (E1 pipeline'ı çıktıktan SONRA — koşan bash betiği düzenlenmez):**
`e7)` dalına kısa/tam anahtarı eklenecek, örn. `E7_SEEDS` ve `E7_EPOCHS`
ortam değişkenleri; varsayılan **kısa** olacak ki kaza eseri tam sürüm
koşulmasın. Tam sürüm bilinçli olarak `E7_FULL=1` ile istenecek.

---

## 2. Doğrulanan zorunlu önlemler (`Q1_ARASTIRMA_RAPORU.md` §E7)

| önlem | durum | kanıt |
|---|---|---|
| flip KAPALI | ✓ | `DATASETS["svhn"]["flip"] = False` (`src/data/datasets.py`) |
| extra-604k KULLANILMIYOR | ✓ | `_make_dataset` SVHN'de `split="train"`; extra split hiç anılmıyor |
| eps-warmup | ✓ **ölü bayrak değil** | `cli/train.py:137` tanımlı → `:223` `eps_warmup_epochs=` olarak trainer'a geçiyor → `src/training/adversarial_trainer.py:211` kullanıyor |
| LR 0.001 | ✓ | `e7)` dalında `--lr 0.001` |
| AutoAttack yok | ✓ | `e7)` dalında AA adımı yok |
| sınıf-dengesi kontrolü | ✓ | `experiments/rev2/a2b_class_balance.py` (veri kümesinden bağımsız; CIFAR-10/100'de kalibre edildi) |
| 1 koşu pilot | ⚠ | kısa sürümde ilk çift zaten pilot işlevi görüyor; ayrı bir kapı **kurulmayacak** (E1'de kapının ölü çıkması dersi — bkz. `E1_PILOT_KAPISI.md` EK B.1) |

---

## 3. TUZAK — SVHN'de `--stratified` KULLANILMAYACAK

CIFAR-100 dalı doğrulama bölmesini `--stratified` ile üretiyor, SVHN dalı
üretmiyor. **Bu bir tutarsızlık değil, kasıtlı ve doğru bir farktır.**
Sonradan "tutarlılık" adına SVHN'e `--stratified` eklenmesi bir HATA olur.

Gerekçe: `make_val_split.py::_stratified_indices` **sınıf başına EŞİT** örnek
verir (`base, extra = divmod(val_size, n_cls)`). CIFAR-100'de bu doğrudur
(veri kümesi zaten dengeli; rastgele bölme sınıf başına 7-35 örnek bırakıp
seçim metriğini gürültülü yapıyordu). **SVHN dengesizdir**; eşit-sınıf
bölmesi 2000 örneği her sınıfa 200 olarak dağıtır ve doğrulama kümesini
**dengeli** yapar. O zaman erken durdurma dengeli bir dağılımda seçim yapar,
sonuç ise dengesiz test kümesinde raporlanır — seçim ölçütü ile raporlama
ölçütü arasında dağılım uyuşmazlığı doğar ve seçici nadir sınıflarda iyi olan
checkpointlere kayar.

**Ölçülen değerler (doğrulandı):**

- SVHN eğitim sınıf payları: 0,0636 - 0,1892 → **dengesizlik oranı 2,98×**
- Rastgele 2000'lik bölmede en nadir sınıf: **127 ± 11** örnek → dejenere
  sınıf riski **yok** (CIFAR-100'deki 7-35 sorununun SVHN'de karşılığı yoktur)
- Mevcut `data/val_split_indices_svhn.json` **orantılıdır**: sınıf sayıları
  145/378/288/239/205/168/146/146/156/129, eğitim dağılımından
  **TV uzaklığı 0,0192**; "hepsi 200 mü?" → **hayır**

Yani mevcut bölme dosyası doğru kurulmuş ve **yeniden üretilmesine gerek
yoktur**.

---

## 4. Koşumdan sonra yapılacak analiz

E1 ile aynı zincir kullanılacaktır (`scripts/q1_e1_analysis.sh` SVHN'e
uyarlanarak): transfer matrisi → 4 protokol → **sınıf bileşimi kontrolü** →
toplulaştırma. Sınıf bileşimi kontrolü SVHN'de **kritiktir**: CIFAR'da bileşim
etkisi asimetrinin %1-19'u çıktı (hep negatif); dengesiz bir kümede bu payın
büyümesi beklenir ve büyürse **raporlanacaktır**.

**Dikkat:** `q1_e1_analysis.sh` içinde `DS=cifar100` sabittir ve
`c1_c3_transfer_matrix.py` SVHN'de WRN referansını **otomatik eklemez**
(`has_rb` yalnız cifar10/cifar100 için doğrudur; rapor §E7 bu yüzden
"DenseNet-121 referansı `--model` listesine açıkça verilir" diyor). SVHN
koşumunda referans model **elle** verilmelidir, yoksa matris 3×3 değil 2×2
olur ve karıştırıcı analizi kurulamaz.

---

## 5. E7'nin taşıyacağı iddia

E7 mutlak gürbüzlük yarışması değildir. Tek işlevi **E3'ün boş düşük-hata
bandını doldurmaktır** (ölçülen boşluk: temiz hata %12'nin altı tamamen boş;
bkz. `E3_YENIDEN_TASARIM.md` §2). CIFAR-100 WRN referansının bu boşluğu
doldurmadığı EK F.4'te ölçüldü (temiz hatası ~%36). E7 dışında düşük-hata
çapası **yoktur**.
