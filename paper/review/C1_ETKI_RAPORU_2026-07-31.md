# C1 Etki Raporu — Sızıntı Düzeltmesi Yayımlanmış Bulguları Değiştiriyor

**Tarih:** 2026-07-31
**Kapsam:** `results/c1_seeds/` (3 tohum, leak-fix) ile `results/rev2_blockA/` (tek koşu, eski protokol) karşılaştırması
**Durum:** Aksiyon gerekli. Hem `paper/bildiri/bildiri.tex` hem `paper/manuscript/sections/` revizyon istiyor.

---

## 1. Özet

rev2 C1 pipeline'ı, sabit ortak doğrulama bölmesiyle (leak fix) mimari başına 3 tohum yeniden eğitti. Ortaya çıkan sayılar Blok A'nın eski sayılarından **yön değiştirecek kadar** farklı. Tohum başına standart sapmalar ≤0.80 puan ve üç tohumun üçü de aynı yönü gösteriyor, dolayısıyla bu bir varyans etkisi değil.

Makalenin ve bildirinin "üç okuma" (multi-view) çerçevesini taşıyan **iki iddiadan ikisi de düşüyor**:

| # | İddia | Eski veri | C1 verisi | Sonuç |
|---|---|---|---|---|
| 1 | "PGD farkının tamamı temiz doğruluk farkından gelir; koşullu yanıltma eşit" | 52.15 vs 52.33 (ayırt edilemez) | 48.58 vs 55.53 (fark −6.96 ± 1.19) | **Geçersiz** |
| 2 | "AutoAttack altında koşullu sıralama hafifçe ViT lehine döner" | 58.16 vs 56.46 (ViT önde) | 55.78 vs 60.37 (ResNet önde) | **Ters döndü** |

Leak-fix'li protokolde CNN **her üç görünümde de** (mutlak, koşullu, both-correct) önde. Tek sayının üç farklı okuma desteklediği anlatı, bu veriyle artık kurulamıyor.

---

## 2. Sayılar

### 2.1 Mutlak doğruluk

| Metrik | Blok A (eski, 1 koşu) | C1 (3 tohum, ort. ± std) | Değişim |
|---|---|---|---|
| ResNet-18 AT temiz | 85.42 | 85.78 ± 0.36 | +0.36 |
| ViT-Tiny AT temiz | 75.65 | 73.53 ± 0.55 | −2.12 |
| ResNet-18 AT PGD-10 | 40.87 | 44.11 ± 0.50 | +3.24 |
| ViT-Tiny AT PGD-10 | 36.06 | 32.69 ± 0.22 | −3.37 |
| ResNet-18 AT AA | 35.74 | 37.93 ± 0.14 | +2.19 |
| ViT-Tiny AT AA | 32.94 | 29.14 ± 0.40 | −3.80 |
| **AA farkı (R−V)** | **2.80** | **8.79 ± 0.40** | **3.1 kat** |

### 2.2 Koşullu yanıltma oranı — kritik değişim

| Saldırı | Model | Blok A | C1 (ort. ± std) |
|---|---|---|---|
| PGD-10 | ResNet-18 AT | 52.15 | **48.58 ± 0.80** |
| PGD-10 | ViT-Tiny AT | 52.33 | **55.53 ± 0.50** |
| PGD-10 | *fark (R−V)* | *−0.18 (eşit)* | ***−6.96 ± 1.19*** |
| AA | ResNet-18 AT | 58.16 | **55.78 ± 0.23** |
| AA | ViT-Tiny AT | 56.46 *(ViT önde)* | **60.37 ± 0.33** *(ResNet önde)* |
| AA | *fark (R−V)* | *+1.70* | ***−4.59 ± 0.10*** |

Yorum: eski veride ViT, kendi temizde çözdüğü örneklerde oransal olarak *daha az* kaybediyordu. C1'de tam tersi. Koşullu ayrışma her tohumda birebir tutuyor (ör. çift 1 AA: 85.37 × 44.43% = 37.93 ölçülen 37.93), yani hesaplama tarafında sorun yok.

### 2.3 Both-correct eşleşmiş altküme

| Metrik | Blok A (n=7.260) | C1 (n=7.061 ± 68) |
|---|---|---|
| ResNet PGD-10 | 54.92 | 59.86 ± 0.35 |
| ViT PGD-10 | 49.61 | 46.11 ± 0.59 |
| *fark* | *5.30* | ***13.76*** |
| ResNet AA | 48.15 | 51.89 ± 0.49 |
| ViT AA | 45.33 | 41.15 ± 0.39 |
| *fark* | *2.82* | ***10.73*** |

Both-correct farkı PGD'de 2.6 kat, AA'da 3.8 kat büyüyor. McNemar p değerleri her üç tohumda da $10^{-84}$ ile $10^{-153}$ arasında; eski veride AA için $p=1.7\times10^{-7}$ idi.

---

## 3. Revizyon gereken yerler

Aşağıdaki satırlar eski sayıları içeriyor ve C1 ile güncellenmeli.

### 3.1 Bildiri — `paper/bildiri/bildiri.tex`

| Yer | Ne var | Ne gerekiyor |
|---|---|---|
| Abstract | "35.74\% vs 32.94\%", "the entire PGD-10 gap traces to the clean accuracy gap", "conditional ordering under AutoAttack turns slightly in favor of the ViT" | Sayılar + **iki iddianın yeniden yazımı** |
| Tablo I (`tab:main`) | AT satırlarının Temiz/PGD-10/AA sütunları | C1 ortalamaları (± std eklenebilir) |
| Tablo II (`tab:cond`) | 52.15 / 58.16 / 52.33 / 56.46 / 54.92 / 48.15 / 49.61 / 45.33 | Tümü |
| §III-A gövde | "statistically indistinguishable (52.15\% vs 52.33\%)", "turns slightly in favor of the ViT", "$\sim$1,300 samples ... below 8\% PGD survival" | Anlatı yeniden kurulmalı |
| §V Discussion | "three readings" çerçevesi | Yeni bulguya göre |
| §VI Conclusion | Aynı çerçeve | Yeni bulguya göre |

### 3.2 Makale — `paper/manuscript/sections/`

| Dosya | Etkilenen yer |
|---|---|
| `04_experiments.tex` | Satır 53-54 (koşullu tablo), satır 62 (uzun ayrıştırma paragrafı, üç okumayı da açık açık kuruyor) |
| `05_discussion.tex` | Eski sayıları içeren pasajlar |
| `06_conclusion.tex` | Satır 9: "conditioned fooling 52.15\% vs 52.33\%", "per-model AutoAttack conditional ordering slightly favors the ViT" |

---

## 4. C1'in **kapsamadığı** analizler

C1 yalnızca temiz / PGD-10 / AutoAttack ve bunların koşullu türevlerini yeniden üretti. Aşağıdakiler **hâlâ eski, sızıntılı checkpoint'lerin sayıları** ve leak-fix altında ayakta kalıp kalmadıkları bilinmiyor:

| Analiz | Artefakt | Bildiride nerede |
|---|---|---|
| Transfer protokolleri (**ikinci ana bulgu**) | `results/rev2_blockA/a2_transfer_protocols.json` | Tablo III, §III-B tamamı |
| Exclusive subset mekanizması | `a2b_exclusive_subsets.json` | §III-B ("1.282 vs 305") |
| Gradyan yapısı | `a3_gradient_paired.json` | §III-C tamamı |
| t-SNE nicelleştirme | `a5_tsne_quant.json` | (bildiride yok, makalede var) |
| Blok bazlı öznitelik kayması | `attention_analysis_run3`, `c_addenda` | §III-D, Şekil 4 |
| FGSM sütunu + epsilon taraması | `final_eval_seeded`, `epsilon_sweep_seeded` | Tablo I, Şekil 2 |

**Öncelik:** transfer protokolü analizi. Bildirinin ikinci ana bulgusu ve en özgün metodolojik katkısı o; leak fix koşullu oranları bu kadar değiştirdiyse, koşullamaya dayanan transfer protokollerini de değiştirmesi kuvvetle muhtemel.

---

## 5. Bu bulgu makaleyi zayıflatmıyor

Anlatı değişiyor ama zayıflamıyor, aksine güçleniyor. Eski çerçeve "tek sayı üç farklı okuma destekler" diyordu. Yeni çerçeve daha keskin ve daha savunulabilir bir metodoloji iddiası sunuyor:

> Temiz ön eğitimle çekişmeli ince ayar arasında paylaşılmayan bir doğrulama bölmesi, koşullu sıralamayı **tersine çevirecek** kadar etki ediyor. Ölçüm protokolü, karşılaştırmanın sonucunun bir parçasıdır.

Bu, bildirinin zaten savunduğu "protokol seçimi yönlü sonuç yaratabilir, silebilir veya tersine çevirebilir" tezinin ikinci ve daha güçlü bir örneği: sadece değerlendirme protokolü değil, **eğitim protokolü** de aynı şeyi yapıyor. Bildiride 1 sayfa boşluk var (5/6), bu genişletme için yer yeterli.

Ek olarak, 3 tohumlu sonuç bir sınırlılığı da kapatıyor: mevcut metin "testler sabit kontrol noktalarına koşulludur, eğitim tohumu belirsizliğini nicelemez" diye uyarıyordu. C1 ile artık niceliyoruz.

---

## 6. Yapılacaklar (GPU makinesi)

1. **Transfer analizini C1 modelleriyle yeniden koş** — `experiments/rev2/a2_transfer_protocols.py`, üç çift için. Tablo III ve §III-B'nin kaderi buna bağlı.
2. `a2b_exclusive_subsets.py` — aynı checkpoint'lerle (mekanizma açıklaması buna dayanıyor).
3. `a3_gradient_paired.py` — gradyan bulgusu için.
4. Öznitelik kayması ve epsilon taraması — C1 checkpoint'leriyle.
5. `fig_b4_data_adv.pdf` — İngilizce etiketlerle yeniden üret (script çevrildi, `models/` gerektiği için sadece GPU'da koşar):
   ```
   python paper/bildiri/generate_bildiri_data_fig.py
   ```
6. Hepsi geldikten sonra bildiri + makale revizyonu.

---

## Kaynak artefaktlar

- C1: `results/c1_seeds/c1_seed_summary.json`, `results/c1_seeds/C1_SEED_RAPORU.md`
- Eski: `results/rev2_blockA/a1_conditioned_main.json`
- C1 toplam GPU süresi: 21.68 saat (RTX 5090)
