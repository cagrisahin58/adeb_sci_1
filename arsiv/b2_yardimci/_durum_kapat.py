#!/usr/bin/env python3
"""B2_DURUM.md'yi KAPANDI durumuna cevirir (kayit korunur)."""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/results/q1_research/B2_DURUM.md")
t = p.read_text(encoding="utf-8")

if "KAPANDI" in t.split("\n")[2]:
    print("zaten kapali")
    sys.exit(0)

ESKI_BAS = """> **2026-08-25.** Bu belge yarım kalan tek işi tarif eder. İçindeki her sayı
> ölçüldü; hiçbiri hatırlanmadı. Devam etmek için §6'daki iki komut yeter.
>
> **Makale şu anda GEÇMİYOR** ve bu bilerek böyle: `check_manuscript_claims.py`
> içine H1/H2 muhafızları kondu. A kolu yeniden koşulmadan makale "temiz"
> görünemez."""

YENI_BAS = """> **KAPANDI — 2026-08-25.** A kolu 116/116 noktayla yeniden koşuldu, iki-kol
> uydurması ve şekil yeni koldan üretildi, metin iki dilde işlendi.
> **Altı kapının altısı da geçiyor** (`bash scripts/kapilar.sh`).
> Aşağıdaki kayıt neyin neden yapıldığını saklar; §6'daki komutlar artık
> yeniden üretim içindir, yarım kalan iş için değil.
>
> Kapanış ölçümleri: köken defteri 44 artefakt / 0 eksik · derleme EN 21 s.,
> TR 20 s., bildiri 6 s., üçünde de 0 undefined · öz-sınamalar: iddia tabanı
> KALAN=0 ve altı kol, özet dört kol, bildiri altı kol, ayna dört kol."""

if t.count(ESKI_BAS) != 1:
    print(f"BASARISIZ: {t.count(ESKI_BAS)} eslesme")
    sys.exit(1)
t = t.replace(ESKI_BAS, YENI_BAS, 1)

EK = """

---

## 10. KAPANIŞ ÖLÇÜMLERİ — 2026-08-25

### A kolunun yeniden koşumu: iki etki ayrı ölçüldü

| etki | ne değişti | ortalama \\|fark\\| | en büyük |
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
ifade olmadığı için iddia kapısı da görmedi."""

p.write_text(t.rstrip() + EK + "\n", encoding="utf-8")
print("B2_DURUM.md kapanisa cevrildi")
