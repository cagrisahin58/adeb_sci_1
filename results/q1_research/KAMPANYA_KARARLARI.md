# Kampanya Kararları — Q1 (karar günlüğü)

Bu dosya, Q1 kampanyasında verilen **geri dönüşü pahalı** kararları ve
gerekçelerini tarihiyle kaydeder. Amaç: bir karar sonradan sorgulandığında
"neden böyle yapmıştık" sorusunun kaynağa dayanarak cevaplanabilmesi.

---

## K-01 (2026-08-19) — E7-kısa KOŞULACAK, E5 ERTELENDİ

**Karar veren:** kullanıcı (Çağrı Şahin), ara denetim bulgularının sunulması
üzerine.

### Karar

- **E7-kısa: KOŞULACAK** (~11 GPU-saat). Tanım `Q1_ARASTIRMA_RAPORU.md` §E7
  kısa sürümü: 2 mimari × 2 tohum, AT 50 epok (SVHN hızlı konverjans),
  yalnız PGD protokol analizi, **AutoAttack yok**.
- **E5: ERTELENDİ** (70-85 GPU-saat). E3 yeniden tasarımı kesinleşene kadar
  başlatılmayacak.
- **E4: DÜŞTÜ.** **E6: TUTULDU.**
- Koşum sırası: E1 (koşuyor) → E7-kısa → E6 → [E5 kararı yeniden gözden geçirilir].

### Gerekçe — E7 neden düşürülemez (ilk düşecek kalem olarak planlanmıştı)

E3 tezin omurgasıdır ve temiz-hata ekseninde bir regresyon kurar. Mevcut
yörüngelerin **ölçülen** kapsaması:

Aşağıdaki tablo **gerçek 10.000 örnek test** ölçümüdür (P0 test eğrileri,
`results/q1/e3_xekseni_test.json`); ilk yazımda kullanılan doğrulama-tabanlı
rakamlar bu yetkili değerlerle **düzeltilmiştir** (2026-08-19).

| kaynak | temiz doğruluk (test) | temiz hata |
|---|---|---|
| ResNet-18 CIFAR-10 (×3) | 80,62 - 87,94 | **%12,06 - 19,38** |
| ViT-Tiny CIFAR-10 (×3) | 56,89 - 76,53 | **%23,47 - 43,11** |
| WRN-28-10 (dış çapa) | 89,48 | %10,52 |

600 noktanın bant dağılımı: %0-5 → **0**, %5-10 → **0**, %10-12 → **0**,
%12-20 → 300, %20-30 → 262, %30-45 → 38.

**%12'nin altı tamamen boştur** (ön-kayıtlı hedef aralık %5-55 idi; alt uç
karşılanmıyor). E7 (SVHN, AT temiz ~%92-95 → hata %5-8) planlanmış **tek**
düşük-hata çapasıydı. E7 düşerse o uçta kalan yegâne nokta WRN-28-10'dur
(hata %10,52) — farklı mimari, farklı reçete, ek veri. Yani regresyonun bir
ucu tek bir dış modele dayanır.

*(İkinci bir boşluk daha ölçüldü: %19,4-23,5 arası — ResNet ile ViT
yörüngeleri arasındaki kopukluk. E1'in CIFAR-100 noktalarıyla kapanması
bekleniyor; ayrıntı ve doğrusallık testi zorunluluğu için bkz.
`E3_YENIDEN_TASARIM.md` §2.)*

Ayrıca `Q1_ARASTIRMA_RAPORU.md` §2.2 Q1 dergi eşiğini "2-3 veri kümesi" olarak
koyuyor ve 3 kümeli planı **"alt sınırda yeterli"** diye niteliyor. E7 düşerse
2 kümeye inilir, yani alt sınırın altına.

**Maliyet/fayda:** E7-kısa 11 GPU-saatte gerçek bir boşluğu kapatıyor; E5
70-85 GPU-saatte E3'e yalnız 2 yörünge daha ekliyor (aşağıya bakınız). Bütçe
E7'ye harcanmalı.

### Gerekçe — E5 neden erteleniyor

E5'in E3'e katkısı, E3'ün **yeniden tasarımına** bağlıdır. Ara denetimin
ölçtüğü üzere E3'ün ön-kayıtlı kantil hedefleri çöküyor: hedefler
{40, 50, 60, 70, 80, konverjan} iken ResNet yörüngeleri 80,6-87,9 aralığında
kaldığı için 40/50/60/70 **aynı** checkpoint'e düşüyor. 6 E2 yörüngesinden
beklenen "≥72 nokta" gerçekte **18 nokta**.

En olası düzeltme (kantil seçimini terk edip **tüm** checkpointleri yörünge
düzeyi küme bootstrap'iyle kullanmak) benimsenirse E5'in katkısı marjinaldir.
Bu yüzden sıra **E3 tasarımı → E5 kararı** olmalıdır; ters sıra 70-85 saati
geri dönüşsüz harcar.

E5 koşulursa bile **1 tohumla** koşulacak ve iddiası daraltılacaktır: 1 tohum
protokol yayılımını (çift-içi nicelik) taşır, ama araştırma raporundaki
kayıtlı ön-kestirimi ("protokol yayılımı ve r ilişkileri kapasiteden bağımsız
kalmalı" — bir **oran** iddiası) **taşımaz**, çünkü 1 tohumda payda sigma'sı
yoktur. Bu, sonuç gelmeden şimdi kaydedilmiştir.

### Bağlı diğer karar: E4 neden düştü ve yerine ne kondu

E4'ün (+2 tohum, n=5) tek gerekçesi n=3'te sigma kestiriminin güven aralığıydı.
Ama hesaplandığında n=5 bile makalenin kurmak istediği "en az üç kat" tabanını
**kurtarmıyor**: n=5'te çarpan [0,60; 2,87] → en muhafazakâr eşleştirmenin alt
sınırı 3,26/2,87 = **1,13**. Yani 16 GPU-saat harcamak sorunu çözmezdi.
Doğru hamle koşum eklemek değil **iddiayı yeniden yazmaktı** ve yazıldı
(commit 95d6338: oran manşetten çıkarıldı, mutlak dile geçildi).

### Bu kararın açtığı borçlar

1. **E7-kısa için zorunlu önlemler** (`Q1_ARASTIRMA_RAPORU.md` §E7): flip
   kapalı, extra-604k yok, **eps-warmup + LR 0.001** (8/255 kararsızlığı
   belgeli), 1 koşu pilot şart, **sınıf-dengesi kontrolü analiz koduna
   eklenmeli** (SVHN dengesizdir). Bu kontrol henüz **yoktur**.
2. ~~**E3 yeniden tasarımı yazılmalı** — E5 kararının önkoşulu.~~
   **KAPANDI (2026-08-19):** `E3_YENIDEN_TASARIM.md`. Ölçülen çöküş 72 hedef →
   **38 ayrı nokta (%47,2)**; ResNet yörüngelerinde 2/6.
   *(İlk yazımdaki 66→33/%50 değerleri E1 koşarken üretilmiş bayat bir
   artefakttan geliyordu; betiğe bitmişlik kapısı eklenip yenilendi.)* Kantil seçimi terk edildi,
   tüm checkpointler + yörünge düzeyi küme bootstrap; iki kol (kontrollü /
   gözlemsel) ayrı raporlanacak, havuzlama yasak. Sapma beyanı yazıldı.
   Tasarım, E5 ertelemesini ve E7-kısa kararını **doğruladı**.
3. E5 ertelendiği için, makalede E5'e dayanan hiçbir iddia kurulmayacak.


---

## K-02 (2026-08-20) — E6 UYGULANDI ve E7'nin ARKASINA KUYRUKLANDI

**Karar veren:** K-01'de kullanıcı ("E6: TUTULDU", sıra "E1 → E7-kısa → E6").
Bu kayıt, o kararın **uygulamasını** belgeler; kararı değiştirmez.

### Bulunan durum

K-01'de E6 tutulmuştu ama ortada **hiçbir uygulama yoktu**: `q1_pipeline.sh`'ta
`e6` aşaması yok, ön-kayıt belgesi yok, tek çıktı yok. Yani karar kâğıt
üstündeydi ve sessizce düşmüş sayılabilirdi.

### Ölçülen gerçek — E6 sanıldığı kadar pahalı değil

E6 **eğitim gerektirmiyor**; mevcut C1 checkpointlerinin farklı bir norm altında
**değerlendirilmesi**. Altyapı da zaten yerindeydi:

| bileşen | durum |
|---|---|
| `PGDL2Attack` | `src/attacks/pgd.py:135` — hazır |
| `c1_pgd_eval.py --norm l2` | bayrak zaten var |
| `run_autoattack_run2.py --norm L2` | bayrak zaten var |
| `c1_c3_transfer_matrix.py` L2 | **eksikti → eklendi** (`--norm {linf,l2}`, varsayılan `linf`, eski davranış birebir korunur) |

### Yapılanlar

1. **Ön-kayıt yazıldı:** `results/q1_research/E6_ON_KAYIT.md` — hiçbir L2
   ölçümü görülmeden. Sabitlenen tasarım (ε=0,5; PGD-L2 steps=10, α=0,125,
   n=10.000; AA-L2 n=5.000), üç sınanabilir ön-kestirim (Ö1 yön, Ö2 yayılım
   ≥2 puan, Ö3 işaret) ve dört analiz-uygunluk kuralı (U1-U4).
2. **Koşucu yazıldı:** `scripts/q1_e6_l2.sh` — **ayrı betik**, koşan
   `q1_pipeline.sh`'a dokunulmadı (T5: koşan bash betiği düzenlenmez).
   İçinde bir **GPU çakışma muhafızı** var: `q1_pipeline.sh` koşuyorsa
   başlamayı reddeder (sınandı: E7 koşarken doğru şekilde durdu).
3. **Sağlama testi yazıldı:** `scripts/q1_e6_u4_check.py` — aynı checkpoint
   L∞ ve L2 değerlendirmelerinde **aynı temiz doğruluğu** vermelidir; vermezse
   yükleme/ön-işleme hatası vardır ve analiz durur.
4. **Makaleye tehdit modeli kapsamı yazıldı** (iki dilde) — E6 koşulsun ya da
   koşulmasın doğru olması gereken beyan.

### Bağlayıcı çerçeve (E6_ON_KAYIT §0'dan)

> Modeller **L∞ ile eğitilmiştir**. E6 onları L2 altında **ölçer**. Bu,
> modellerin L2-gürbüz olduğu iddiası değildir ve çıkan sayılar RobustBench'in
> **L2-eğitilmiş** girdileriyle karşılaştırılamaz. E6'nın taşıdığı tek nicelik,
> protokol yayılımının ve ham−koşullu ilişkisinin norm değişince ne yaptığıdır.

### Neden şimdi koşulmadı

E7 (SVHN) 2026-08-20 13:41'de başlatıldı ve GPU'yu kullanıyor. İki GPU işini
üst üste bindirmek ikisini de yavaşlatır. E6 muhafızı bunu kod düzeyinde
engelliyor; E7 bitince `bash scripts/q1_e6_l2.sh` tek komutla başlar.
