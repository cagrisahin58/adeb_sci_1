# Hakem raporu (ikinci geçiş): yeniden yazılmış EN metin, 2026-10-04, mercek: yöntem

Kaynak: hakem-simulasyonu ajanı (opus), tek geçiş; ana oturum kaydetti. Okunan sürüm: makale-yazarının ilk
yeniden kurulumu (karantina literalleri ve kapak mektubu ek turundan ÖNCE; F1 o turda çözüldü).

## Türkçe özet
Yeniden yazım panelin B1–B3 bulgularının çoğunu karşılıyor: başlık literatür düzeyi iddiayı bıraktı, 9,21 /
11,10 / 3,91 toplanmadan ayrı olgular olarak verildi, kaynak etkisi tabloyla desteklendi, Mahmood uzlaşması
kısmi ve açık soru. Ancak "büyüklük temiz farkı izler, eşlenmiş çiftlerde küçülür" iddiası özet, sınırlılıklar,
sonuç ve başlıkta DÖRT protokollü yayılım için kullanılıyor; havuzda bu yayılımın farkla ilişkisi yok (r 0,05) ve
eşlenmiş gürbüz çiftlerde 6–13 puan kalıyor (başarılı-kaynak terimi). Şekil 3 altyazısındaki "üç uzaklık
yayılımı bölmez" aritmetik olarak eksik: 11,10 + 3,91 = 15,01 tam tutar, CIFAR-10'da özdeşlik terimi aralığın
uçlarına katkı vermez. Kaynak-hedef tablosunda birincil her-ikisi-doğru protokolünün satırları yok (hedef terimi
−0,53 ± 0,59, sıfırdan ayırt edilemez). Föyde olup metne alınmayan iki bulgu: standart eğitimli ViT-Tiny en
zayıf kaynak (yön hedef terimiyle), Mahmood CIFAR-100 yeniden puanlamasında 12 çiftin 6'sında işaret dönüşü.
Yaklaşık kırk gövde sayısı föyde yok; SVHN farkı 1,85 değil 1,84. On altı sayı yeniden hesaplandı, yeni
tabloların ve şeklin bütün hücreleri doğru. Hüküm: Major revision (metin ve kayıt düzeltmeleri; eğitim yok).

## Ana oturum kararları (2026-10-04 akşam)
- F1: karantina literalleri yazarın ek turunda çıkarıldı (tek nitel cümle kaldı).
- F2: depo kullanıcı tarafından açılacak (önceki karar); "reproduce every number" dili depo itilmeden
  gönderim yapılmayacağı notuyla kalır; eksik toplayıcılar açık depo kurucusuna eklendi.
- F3: iddia üç protokollü yayılıma (özdeşlik terimi) daraltılır; başarılı-kaynak fazlasının eşlenmiş gürbüz
  çiftlerde küçülmediği özete yazılır; **başlık** "… An Exact Correction and a Source-Effect Reading for CNN
  versus Vision Transformer Robustness Comparisons" (Matched-Pair Prediction çıkar).
- M1–M7 ve küçükler yazara verildi; M8 (kırk gövde sayısı) kod-mimar ile föye bağlanıyor; m15 (dört yeni
  atıf) bu turda eklenmedi (atıf kontrolü gerekir).

## Hakem metni (İngilizce, olduğu gibi)

**Overall:** Major revision. Confidence: M–H. The science and the new desk analyses are sound and every new
table cell checks out. Two submission-gate defects remain, and one headline claim is contradicted by the
paper's own pool. All fixes are text or bookkeeping; none needs training.

### Strengths
- Every cell of the three new artifacts matches the reference sheet (tab:protocol_masks, all 13 rows of
  tab:source_target incl. the fixed-WRN sign convention, all 14 rows of tab:external_pool). Recomputed
  fig:spread_clean_gap: three-protocol slope +0.7963, r = 0.9571; four-protocol +0.0923, r = 0.0532; 57/60
  equality; largest parity deviation 1.09, mean 0.126.
- B2: 9.21, 11.10 and 3.91 stated as pairwise distances, never added; [3.12, 4.70] = 3.91 ± 4.303 × 0.32/√3.
- B1: title no longer literature-level; conclusion gives range-vs-range 15 vs 2.4 (0.63/0.86/0.46/2.41).
- B3: source-effect reading supported by additive fit and fixed-WRN contrasts; Mahmood paragraph honest.
- Tautological residual acknowledged (04:153); L2 slope and three-protocol slope reclassified as identity checks.
- Pool caveat and XCiT counterexample reported.

### 🔴 Fatal
- **F1** Quarantined literals (Table II lower block, Table III footnote, "attribution differed" thread).
- **F2** Data and Code Availability false today (URL 404; snapshot lacked aggregators).
- **F3** "Magnitude follows the gap / shrinks for matched pairs" claimed for the four-protocol spread and the
  asymmetry; the pool contradicts both (four-protocol slope +0.092, r 0.053; pool +0.559 [−0.205, +4.582];
  Carmon/Gowal gap 0.21 spread 9.03; XCiT/Gowal 0.58 → 12.73; ResNet18_AT/Engstrom 1.66 → 17.50; bc asymmetry
  −6.95 at 1.66 gap; last checkpoint bc 8.27 → 7.97 while gap closes 1.71). Only the three-protocol spread
  (identity term) follows the gap. Fix: scope the claim; abstract sentence on the successful-source excess;
  reconsider "Matched-Pair Prediction" in the title.

### 🟡 Major
- **M1** Fig. 3 caption "do not partition" half wrong: (ss−bc) + (bc−tc) = 15.01 exactly on CIFAR-10; raw is
  interior there, upper end on CIFAR-100 (13.58 of 13.83).
- **M2** tab:source_target omits the primary both-correct protocol (sheet: C10 bc source +6.76±0.35, target
  −0.53±0.59; C100 bc +11.79/−2.85; fixed-WRN bc contrasts +4.69, 2.60). Target term is protocol-dependent.
- **M3** 05:26 "our own … before adversarial fine-tuning, already favor ViT-crafted examples" misleads: clean
  tc fit (pair1, R² 0.9994) source α ViT −48.27 / ResNet +23.39, target β ViT −51.23 / ResNet +25.75; the ViT
  is the weakest source, the direction is target-carried. Drop "adversarial against standard training" as a
  candidate cause for Mahmood's reversed source effect.
- **M4** Mahmood re-scoring reports CIFAR-10 only; CIFAR-100 identity flips sign at centre in 6/12 cross-family
  pairs (all ResNet-56/164 × ViT); intervals include zero; p=1 applied to standard-trained models against the
  paper's own rule (insensitive on CIFAR-10 since target errors ≤ 2.5).
- **M5** Identity's practical use circular (requirement 2); state Eq. (7) holds by construction, content is p;
  give the p-interval bound for published raw rates.
- **M6** Matched-pair prediction presented as empirical confirmation of arithmetic; list measured content:
  p ≥ 0.985 on AT targets; bc between raw and tc in 57/60; ss term unrelated to gap. "identity term grows by
  0.87" is the three-protocol spread (differs in 3/28 pool pairs).
- **M7** Selection framing: state that last.pth is the early-stopping epoch (ViT 38/39/45, ResNet 71/76/77 of
  100); soften "not an artifact"; note selection effect on spread (2.16) ≈ retraining range (2.41).
- **M8** ~40 body numbers without sheet entry (identity residuals 0.41/0.095/1.39; slopes 0.656/0.914;
  t-intervals [7.68, 8.86], [10.07, 11.77]; MI-FGSM 19.07/15.42; marginal subsets 41.2/59.1/10.0/18.3,
  1,517/291; 0.885/0.802; composition terms; 66 minutes; two-arm paragraph numbers; selection grid
  2.62–2.85, 1.58–2.09, 1.09, 1.42, 0.67–3.38, 0.63–7.38, 25 epochs, 0.32; ratios 0.8–9.9, 5.2–32.6, 28.3;
  21.7 GPU-hours; gradient p 0.036/0.042/0.067/0.108/0.0009; L2 McNemar 10⁻⁵⁷; SVHN 94.27±0.70, 92.42±0.56,
  55.52, 52.30; TOST ±1). Error: SVHN gap is 1.84 (94.265 − 92.425), not 1.85; SVHN ±SD from n=2 printed.

### 🟢 Minor
m1 abstract p lower bound (pool AT targets reach 0.9846); m2 03:191 "the one equivalence we accept" vs
attention TOST 12/12; m3 tab:source_target 4.41 vs Table III 4.36 (separate run) disclosure; m4 inclusion
rule of the 60 pairs (CIFAR-100 WRN and L2-WRN pairings excluded); m5 R² on 6-cell/5-parameter fit; m6
"closed form" for bc−tc never written; m7 "no training of our own" → "no new training"; m8 XCiT-S12 is a
convolution-attention hybrid; m9 "pre-registered" → "registered before measurement"; m10 two-arm paragraph
and test-selected native-ViT column still in main text; m11 "rarely vary" / "remain scarce" undocumented;
m12 03:97 "all tables … three runs" untrue for SVHN/pool/WRN; m13 "unflipped" group includes
clean-misclassified samples; m14 "clean error predicts exactly" also needs r_cond and p; m15 panel
references (Springer 2021; Zhang S&P 2024; Bouthillier 2021; Kapoor & Narayanan 2023) absent.

### Claims vs evidence (özet)
Holds: protocols move 4.4–19.4 vs retraining ≤2.4; 9.21 predicted by LTP; 3.91 [3.12, 4.70]; p ranges;
source term; Mahmood source term; three-protocol spread tracks gap; selection ≈2 points; three readings fail.
Fix framing: three facts "do not add up" (M1); Mahmood CIFAR-100 omitted (M4); clean pair implication (M3).
Contradicted: 15-point magnitude shrinks for matched pairs (F3). Missing: earlier-checkpoint literals (F1);
reproducibility (F2).

### Questions a reviewer will ask
1. Why does the 15-point spread not shrink for matched robust pairs (Carmon/Gowal 9.03)? → identity term only.
2. Isn't 15.01 = 11.10 + 3.91? → yes on CIFAR-10; raw interior; present it so.
3. Under both-correct, is the ViT the less vulnerable target? → fixed-WRN contrast yes (2.60); additive −0.53±0.59.
4. Does standard training reverse the source effect? → no; target term flips the net direction.
5. How to apply the correction to a published raw rate without p? → p-interval bound.
6. Is the matched-pair prediction more than Eq. (8) rearranged? → p ≈ 1, bc interior 57/60, ss independent.
7. What epoch is "last checkpoint"? → ViT 38–45, ResNet 71–77; E2 runs to 100 keep the gap > 10.59.
8. Where is the repository / the earlier-checkpoint records? → fix before submission.
