# Hakem raporu: fig_protocol_sets — 2026-09-29, mercek: şekil

Salt-okunur şekil hakemi (hakem-simulasyonu, opus). Ana oturum kaydetti.

**Özet:** Şekilde yanlış sayı yok. Basılan 16 sayı (4 N, 4 asimetri, 4 SD,
4 ayrışım terimi) `results/c1_transfer/c1_transfer_summary.json`
dosyasından yeniden hesaplandı ve hepsi tuttu. İşaret yönü doğru, iç içelik
sırası doğru, betik şekle JSON dışından sayı koymuyor.
**Hüküm: KÜÇÜK DÜZELTME** (🔴 yok).

## Doğrulanan sayılar (SD ddof=1)

- raw 13.5733 (±0.3308) · TC 4.3600 (±0.4355) · BC 8.2667 (±0.2312) ·
  SS 19.3667 (±1.2682). İşaret CNN→ViT − ViT→CNN, dört satırda doğru.
- N: 7352.67→7,353 / 8578.67→8,579 · 7061.33→7,061 (iki yön) ·
  2830.67→2,831 / 3813.67→3,814. Küme farkları 1,518 ve 292, metindeki
  1,517±102 ve 291±16 ile yuvarlama içinde uyumlu.
- Ayrışım (yuvarlanmamış): raw−TC 9.2133 · SS−raw 5.7933 · BC−TC 3.9067 ·
  yayılım 15.0067 = `protocol_spread_pp.mean` (üç tohumda uçlar aynı
  protokoller olduğu için iki tanım çakışıyor; tohum başına 15.97/14.63/14.42).
- Denklem (1): CNN→ViT e=0.2647, r=0.1987 → e(1−r)=21.21, ölçülen 21.15;
  ViT→CNN e=0.1421, r=0.1551 → 12.01, ölçülen 11.94. Öngörülen asimetri
  farkı 9.205, ölçülen 9.213: "kapalı formdan çıkar" iddiası 0.01 içinde.
- PDF MediaBox 249.45 pt (8.8 cm); yalnız DejaVu Sans, Type 3 yok;
  PNG 1039×850, 300 dpi. Şekil henüz hiçbir .tex'te çağrılmıyor.

## 🟡 Düzeltilmeli

- **M1** Üç SD çubuğu (0.23/0.33/0.44) işaretin (yarıçap ≈0.45 puan)
  altında kalıyor; yalnız SS'nin ±1.27'si görünür. n=3'te SD çubuğu zaten
  zayıf. Öneri: üç tohum değerini küçük açık noktalarla çiz, ortalamayı
  kısa dikey çizgiyle; "±" etiketleri kalsın; başlığa "(mean ± SD, 3 seed
  pairs)".
- **M2** "3.91 pts remain" satırı 15.01'e eklenen üçüncü terim gibi
  okunuyor; gerçekte [4.36, 8.27], [4.36, 13.57] özdeşlik aralığının
  içinde. Öneri: sağ eksende üç köşeli ayraç (9.21 Eq. 1 / 5.79 different
  estimand / 3.91 alçakta).
- **M3** Sağ satırlar yalnız CNN→ViT kutusuna bağlı görünüyor; TC ve SS
  asimetrileri iki yönde farklı kümelerden. Öneri: kutulara iki N
  ("N = 7,353 / 8,579"), sol başlık "Evaluation set (CNN→ViT boxes)".
- **M4 (gövde)** 04_experiments.tex:105 "successful-source *rate* sits 5.79
  points above it … target-correct *rate* sits 9.21 below" — oranların
  kendisi ters yönde (SS 36.39 < raw 41.02). "estimate"/"asymmetry"
  yazılmalı; "on CIFAR-100 the unconditioned rate is the largest" aynı.
- **M5** kanit.json commit 725e709 diyor ama betik, veri JSON'u ve veri
  betiği izlenmiyor; kayıtlı commit şekli üretemez. Commit'lenmeli.

## 🟢 Not

- m1 "≈" dürüst, kalsın; "terms rounded separately" yan cümlesi eklensin
  (gövdedeki "account for the full 15.01" cümlesine de).
- m2 Aynı protokole üç ad: "All test samples (raw)"; "Target (ViT) correct";
  "Successful source (CNN white-box)".
- m3 Kutular alanla orantılı değil (TC→BC %4, BC→SS %60); başlık söylüyor.
- m4 Gri baskı: luma 244/224/164/91, kenar çizgileri ayrımı sağlıyor.
- m5 8.8 cm'de en küçük yazı 6.5 pt gri; M1 ile 7 pt ve koyu olsun.
- m6 Veri betiğinde `else 10000` sessiz varsayılan: karantina deliği,
  alan yoksa hata versin.
- m7 Kanıt eksikleri: üst kaynağın sha256'sı, ViT→CNN N kaynak alanları,
  `yayilim` = `protocol_spread_pp.mean` denetimi.
- m8 Güçlü: nedensel ok yok; SS'nin BC içinde çizilmesi sıkı tanımı
  (tc & sc & sa) doğrudan gösteriyor; betik tutarlılık denetimleri iyi.

## Başlık (hakem önerisi, üç cümle)

> Nested evaluation sets of the four transfer protocols in the CNN→ViT
> direction (left; boxes are schematic and not area-proportional, N is the
> mean over three seed pairs) and the asymmetry, CNN→ViT minus ViT→CNN,
> that each protocol measures on the same models and data (right; mean ± SD
> of the paired within-seed difference over three seed pairs). The ViT→CNN
> sets nest in the same order (N = 10,000, 8,579, 7,061 and 3,814); the
> unconditioned and both-correct sets are identical in the two directions,
> the other two are not. Brackets mark the decomposition of the 15.01-point
> spread discussed in Section 4.2 (terms rounded separately).

## Ana oturumun uygulaması (aynı gün)

- M4: EN §4.2 (iki yer) + §1, TR §4.2 (iki yer) + §1 — "rate" → "estimate"
  / "kestirim". Gövdedeki "full 15.01 points" cümlesine yuvarlama kaydı.
- m6, m7: veri betiği sertleştirildi (varsayılan kaldırıldı, sha256,
  tohum değerleri, yayılım eşitlik assert'i).
- M1–M3, m2, m5, m7-kanıt: üreticiye tek tur geri verildi.
- M5: commit, üretici döndükten sonra.
