# Mercek A: bilimsel çekirdek ve deney tasarımı (opus düzenleyici)

Tarih 2026-10-04. Kaynaklar: toplayıcı dosyaları `toplama_A1_claims-inventory.md` ve `toplama_A2_setup-vs-code.md` baştan sona okundu; sonuç doğuran her olgu birincil dosyada (tex satırı, JSON anahtarı, eğitim günlüğü, kaynak kod, render sayfası) yeniden doğrulandı. Sayıların tümü `results/C1_REFERANS_FOYU.md`, `results/c1_*` ve `results/q1/*` altından alındı; karantina klasörlerinden kanıt alınmadı. Yardımcı betikler: `raporlar/hakem_lecun_2026-10-04/_tmp/lensA_*.{sh,py}`. Satır kısaltmaları: `main.tex:N`; `01:N` = `sections/01_introduction.tex:N`, aynı biçimde 02 ile 06 arası. Not: A1 dosyası sonuç bölümünü 06:43-51 diye anıyor; dosya 15 satırdır ve doğru satırlar 06:7, 06:9, 06:11, 06:13, 06:15'tir. Bu raporda doğru satırlar kullanıldı.

## Özet (TR)

Makalenin ölçüm altyapısı (örnek bazında kayıt, tek yerde tanımlı dört protokol maskesi, sızıntısız doğrulama bölmesi, dürüst olumsuz sonuçlar) güçlüdür ve kod, metinle büyük ölçüde örtüşmektedir.
Ancak başlıktaki ve özetin ilk cümlesindeki iddia ("protokol sonucu belirler", "anlaşmazlığın büyük kısmı protokoldendir") makalenin kendi ayrıştırmasıyla desteklenmemektedir.
Makalenin onayladığı iki protokol (hedef-doğru ve her-ikisi-doğru) üç veri kümesinin hiçbirinde yön bakımından ayrışmamaktadır; işaret yalnız makalenin kendisinin reddettiği iki protokolde ve yalnız SVHN'de değişmektedir.
Literatürdeki anlaşmazlıkların hiçbiri yeniden çözümlenmemiştir ve karşılaştırma tabanı tarif ya da veri kümesi değil, aynı tarif ve aynı bölmedeki üç tohumun standart sapmasıdır.
Mekanizma iddiasının dayandığı üç-protokol eğimi, 20 yön çiftinin 19'unda ham eksi hedef-doğru farkına, yani özdeşlik terimine eşittir; bu nedenle eğimin pozitif çıkması yapı gereğidir ve SVHN dahil +0,470 değerinin sonuç dosyası yoktur.
ViT'nin seçilen kontrol noktaları 100 epokluk bütçenin 18 ile 25. epoklarında, öğrenme oranı henüz düşmeden ve temiz doğruluk hâlâ yükselirken alınmıştır; makalenin kendi mekanizmasına göre bu seçim temiz doğruluk farkını, dolayısıyla 15,01 puanlık yayılımı büyütmektedir.
Önerim büyük revizyondur: başlık ve özet onaylanan protokollerdeki 3,91 puanlık farka ve özdeşliğin düzeltici gücüne göre yeniden kurulmalı, mekanizma eğimi özdeşliğin örneklem dışı sınaması olarak yeniden adlandırılmalı, standart eğitimli hedeflerde p mevcut kontrol noktalarıyla ölçülmeli ve seçim kuralının asimetriye etkisi raporlanmalıdır.
Bu düzeltmelerin çoğu yeni eğitim gerektirmez; yalnız ViT'nin tam bütçeyle eğitildiği bir duyarlılık koşusu yeni hesap ister.

## Overall

**Major revision.** The measurement infrastructure is better than most papers in this area, and the setup matches the code on almost every recipe detail. The problem is the framing of the scientific claim, not the data. Read through its own decomposition, the paper shows that (i) unconditioned transfer rates are contaminated by the target's clean error through an accounting identity whose premise holds on adversarially trained targets, and (ii) the two conditioning protocols the authors endorse differ by 3.91 points in magnitude but never in direction on any dataset. That is a useful, publishable methodological result. It is not "the measurement protocol decides the conclusion", and it is not evidence that "much of the disagreement" in the literature comes from the protocol. At a top venue the first red item alone would sink the paper as framed; at IEEE Access it is fixable by rewriting the title, abstract, introduction and conclusion around what is actually demonstrated, plus one cheap measurement and one sensitivity run.

## Strengths

1. Per-sample logging on the full test set lets all four protocols be computed from identical records without re-running attacks (`results/c1_transfer/pair*/per_sample_*.npz`; 01:16). The masks are defined once (`src/analysis/protokoller.py:57-66`), and the strict/loose successful-source sub-choice is surfaced and quantified (04:119: 19.37 vs 14.60; `a2_transfer_protocols.json`). This is exactly the kind of artifact a reporting-standards paper needs.
2. The validation split is fixed (seed 777, `data/val_split_indices.json`) and excluded from both training stages; the C1 logs confirm it ("test kullanilmiyor", `logs/C1_clean_resnet_1001.log:4`). Recipe details (optimizers, lr, schedule, clipping, λ = 0.5, train-mode inner PGD, eval-mode evaluation attacks) match the code (A2 T2-T4; verified `src/defenses/adversarial_training.py:103-122`, `src/training/adversarial_trainer.py:479-500`).
3. The identity r_raw − r_cond = e(1 − r_cond) is verified numerically, and its premise p is measured rather than assumed: p in [0.989, 1.000] over 36 directions, max residual 0.41 points, mean 0.095 (`results/q1/ozdeslik_kontrol.json`; 04:143). Making a qualitative caveat into a usable correction is the paper's most transferable contribution.
4. Unit-of-inference discipline: per-sample vs run-level tests are named, and where they disagree both are reported (03:158, 04:303). Across-run t intervals are given alongside averaged bootstrap endpoints (04:117, 04:204).
5. Candour about failure: one of three CIFAR-100 registered predictions fails and one is untestable (04:206), a registered endpoint band is missed (04:208), the four-protocol slope is withdrawn (04:123), the SVHN pool reassignment is flagged as post-hoc (04:123), and the earlier claim of direction stability is corrected (01:31).
6. SVHN supplies a natural test of the clean-gap account: with a 1.85-point gap the spread drops to 3.70 ± 0.62 (`results/q1/svhn/transfer/e7_transfer_summary.json`; 04:242).
7. The class-composition decomposition rules out a class-mix artifact (04:210) and passes its own arithmetic check (exactly zero under unconditioned and both-correct).

## 🔴 Fatal (as framed)

### R1. The headline claim is not supported by the paper's own evidence

**What.** Title "The Measurement Protocol Decides the Conclusion" (main.tex:56-57) and abstract "We show that much of the disagreement comes from the measurement protocol" (main.tex:89), repeated in 01:11, 01:23 and 06:7-9.

**Evidence against, all from the paper's own artifacts.**
- Among the two protocols the paper endorses for directional claims (target-correct, both-correct; 04:117, 04:240), the direction never differs on any dataset: CIFAR-10 +4.36 / +8.27 (FOY Table III; Table 3, p. 9), CIFAR-100 +4.96 / +10.92 (04:204; `e1_transfer_summary.json`), SVHN −1.00 / −0.35 (04:240; `e7_transfer_summary.json`). On CIFAR-10 both also fail TOST at ±3 (4.36 > 3; 8.27 with CI [7.68, 8.86]). In the corrected runs the endorsed protocols therefore lead to the same qualitative conclusion everywhere.
- The protocol "decides the sign" only through the unconditioned rate (which the paper says "should not be used for architecture comparison at all", 05:19) and the successful-source rate (which "estimates a different quantity", 04:117), and only on SVHN, where all four estimates lie between −1.00 and +2.70 points.
- The 15.01-point spread is decomposed by the paper itself into a known confound (9.21, removed by the identity) and a different estimand (5.79). What survives is 3.91 points of magnitude between two different conditioning populations. The paper concedes the category-error objection (05:15: "We agree").
- The literature disagreements invoked in 01:9 are not re-analysed. Bai et al. vs Benz et al. concern absolute robustness under different training regimes (standard vs adversarial); this paper's absolute ordering is protocol-invariant (04:41, 05:45). On transfer direction, this paper finds CNN→ViT on CIFAR under all four protocols, so the protocol does not reconcile it with Mahmood/Benz/Shao either; 05:17 states that the compatibility test "would require their per-direction clean accuracies" and was not done.
- The abstract names "models, training recipes, or datasets" as the competing explanations. None is the baseline. The baseline is the seed SD at one recipe with a shared validation split (04:451, 04:453). The paper's own data show that changing the dataset moves the primary (both-correct) asymmetry from +10.92 to −0.35, an 11.27-point change comparable to the protocol spread.

**Why it matters.** A top reviewer will read the title, then Table 3 and Fig. 3 (p. 9-10), and see that the "conclusion" only flips for protocols the authors themselves reject. The paper then looks like it argues against a straw man: nobody defends raw cross-architecture transfer rates after reading 04:135-147.

**Fix (no new training).** Retitle and reframe around what is shown, for example "Conditioning choices in cross-architecture transfer comparisons: an exact correction for unconditioned rates and the residual discretion between paired protocols". Lead with (a) the identity as a correction for published raw rates, (b) 3.91 points between endorsed protocols against a like-for-like seed range of 0.86 (target-correct) and 0.46 (both-correct) (`results/q1/variance_ratio.json`, `PAYDA_kosum_etkisi_AYNI_NICELIK.aralik_protokol_bazli`), and (c) the SVHN regime result. Either delete "much of the disagreement comes from the measurement protocol" or earn it: apply the identity to at least one published table of raw transfer rates whose clean accuracies are reported (02:74 says the correction "can be applied directly to published results", but the paper never does it).

### R2. The mechanism claim rests on a slope that is positive by construction

**What.** 04:123: "the mechanism claim rests on the three-protocol one"; 04:127: "The agreement that does carry the claim is the three-protocol one".

**Evidence.** For the 20 direction pairs in `results/q1/e3_asimetri_fit_svhnli.json`, the three-protocol spread (max − min over raw, target-correct, both-correct) equals |raw − target-correct| in 19 of 20 pairs, and that term agrees with the identity prediction stored in the same file (`ozdeslik_ongorusu_ham_eksi_tc`) to within about 0.15 points (recomputed with `_tmp/lensA_threeprot.py`; for example CIFAR-10 pair 1: spread 8.38, identity 8.34; SVHN pair 1: 1.49, 1.49). Since the identity term is the difference of e(1 − r_cond) across the two directions, it rises with the clean-error gap by construction. The paper applies exactly this argument to its own L2 prediction (04:269: "cannot fail once Equation (eq:raw_identity) holds ... estimates 1 − r_cond rather than testing anything") but not to the slope on which the mechanism claim rests. The "agreement between arms" (04:127) is therefore the identity holding twice, not independent evidence for a mechanism.

In addition, the SVHN-inclusive three-protocol slope "+0.470, CI [+0.361, +0.665]" (04:123, 04:127), the value on the pre-registered pool, exists in no result JSON. It appears only as text inside a manuscript-editing script (`scripts/_t3_en_kisalt6.py:40-48`). `e3_iki_kol_fit.json` holds only the SVHN-excluded 0.431 [0.333, 0.633] and the controlled arm. I re-checked A1's grep: no `results/q1` file contains the triple.

**Why it matters.** A careful reviewer who notices the circularity will discount the whole quantitative mechanism section (04:123-127, 05:55), and an unbacked number on the pre-registered pool is a reproducibility red flag in a paper whose selling point is reproducibility.

**Fix.** Reclassify the three-protocol slope as an out-of-sample check of the identity (which is legitimate and useful). State that the non-tautological mechanism content is the marginal-subset account of target-correct vs both-correct (04:123, first half: 41.2/59.1% vs 10.0/18.3% fooling; 1,517 vs 291 samples) and the separate successful-source driver. Produce the artifact for +0.470 [0.361, 0.665] with its generating script, or remove the number.

## 🟡 Major

### Y1. "Retraining moves it by under 1.5 points" compares an SD with a range
main.tex:89, 01:23 and 06:9 state "under 1.5 points" without saying it is a standard deviation; the body (04:451, 05:13) says SD 0.23-1.27, while the protocol figure it is set against (15.01) is a range. The like-for-like seed range is 0.63 / 0.86 / 0.46 / 2.41 for the four protocols (`variance_ratio.json`), so for successful-source the seed-to-seed movement exceeds 1.5. "Retraining" also means three seeds sharing one recipe and one validation split, which the paper itself calls an upper-bound denominator (04:453). **Fix:** write "a seed-to-seed standard deviation of 0.23-1.27 points (range 0.46-2.41)" in all three places and call the comparison "seed variance", not "retraining".

### Y2. The clean-accuracy gap, and therefore the headline spread, depends on an early, noisy ViT selection
By the paper's own mechanism the spread scales with the clean-error gap (04:123, 04:242). The ViT AT checkpoints are selected at epochs 25/18/19 of a 100-epoch cosine schedule with lr still 0.85-0.92 × 10⁻³ and stopped at 45/38/39 (A2 F047, from `last.pth` history). In `logs/C1_at_vit_2002.log`, the selected epoch 18 has val clean/adv 73.50/34.35, while epoch 35 reaches 77.15/33.85 and clean accuracy is still rising when patience runs out. The selection criterion is single-restart PGD-10 on 2,000 samples, whose binomial SE at 34% is about 1.06 points, ten times the 0.1-point improvement threshold (`adversarial_trainer.py:479`). The ViT is therefore selected on a noise spike before its schedule decays, at a clean accuracy several points below what continued training gives, and this widens the 12.3-point gap that drives the 15.01 spread. 04:455 measures the selection rule's effect on absolute PGD-10 only, never on the asymmetry. **Fix:** using the stored trajectories (`results/q1/e2`, `results/q1/e3_akolu*`), report the four-protocol asymmetry and spread at (a) the last checkpoint and (b) the best checkpoint under the alternative selection cells. Ideally also add one ViT run trained to schedule completion without early stopping. State in the abstract that the 15-point magnitude is conditional on a 12-point clean gap.

### Y3. Small, below-reference models in a single regime limit what can be generalised
One model pair, one trained threat model (L∞ 8/255), adversarially trained targets only, a 50/50 mixed clean/adversarial loss (03:85; not Madry PGD-AT), SGD fine-tuning of the ResNet at lr 10⁻³ from a clean checkpoint (03:97), and a ViT-Tiny trained from scratch on 32→224-upsampled inputs (80.09% clean). Both robust accuracies (37.93 / 29.14 AA) sit well below commonly reported PGD-AT baselines for these model sizes. 05:45 calls this "matched standard adversarial training", but the mixed-loss, fine-tune recipe is not the standard one. 06:15 asserts the mechanism "is not specific to our setting" without a test. **Fix:** name the recipe precisely (mixed-loss fine-tuning), give the gap to a cited reference number, and move the single-pair, AT-only scope into the abstract. Keep 06:15 to "we expect ... ; untested".

### Y4. Claims that rest on unprovenanced or quarantined numbers
- p = 0.88 on standard-trained targets (04:145) comes from "pre-correction runs" and is found in neither the reference sheet nor any c1/q1 artifact (A1 N-03; re-grepped). It underwrites the scope statement that the identity is only a bound for standard targets, which is the regime most transfer studies use. **Fix (cheap):** measure p in the current pipeline on the C1 clean-trained checkpoints, which exist (`models/c1/*_s*/*/clean/best.pth`, dated 2026-07-29/30), and replace 0.88.
- ViT 77.50% (04:66) has no artifact (A1 N-02).
- The introduction's "The protocol also decides whether an equivalence test is accepted or rejected" (01:23) rests on the earlier single-run checkpoints (04:117, last sentence) and on SVHN, where only the both-correct protocol was TOST-tested. In the corrected CIFAR runs no endorsed protocol accepts equivalence. **Fix:** rest it on current evidence or drop it.
- "Attribution changed between checkpoint sets" (01:25, 05:23, 06:11) compares three fresh runs with one leaked single run. The earlier checkpoints are dated 2026-07-07/08 (`models/*/adv/at_run3/.../best.pth`) and predate the commit that moved the inner PGD from eval-mode to train-mode BN (`0f8a24f`, 2026-07-11). `scripts/diagnose_at_collapse2.py` (2026-07-07 20:15) slightly precedes the at_run3 directory (20:22), so the working tree was probably already fixed, but the manuscript should state that both sets used the same inner-loop code, because 05:57 lists only "validation handling and ... training run" as differences.

### Y5. Summary sentences claim more than the body
- 06:9 "stable across protocols, seeds, and attack families on both CIFAR datasets": MI-FGSM is checked only on CIFAR-10 (04:121, 05:21), and PGD and MI-FGSM belong to the same family of iterative sign-gradient attacks.
- 06:13 and 05:31: the depth profile "did survive and reproduce across independent checkpoint sets", whereas 04:388 says the CNN curve differed on the earlier checkpoints and "should be read as recipe-dependent".
- 01:25 "reframes the asymmetry as a property of the weaker target" vs 04:172 "With only three targets, the correlation can only be suggestive" (r = 0.986, one of the three targets being an external WRN).
- 06:9 "measurement choices that papers rarely report are of the same order as the effects being reported": selection moves PGD-10 by 1.58-2.85 (04:455), while the absolute CNN-ViT PGD-10 gap is 11.42 (Table 1).
**Fix:** align every summary sentence with the hedge in the body.

### Y6. Asymmetric evidentiary standards for the behavioural results
Sparsity "survives" (01:27, 06:13) at a run-level Holm p of 0.108 (04:303), justified by 3/3 sign agreement (with three runs a two-sided sign test cannot go below 0.25). Spatial locality "does not hold ... on all four spatial measures" (01:27) on run-level p of 0.40-0.54 with no equivalence test (04:333; TOST is used only for attention entropy, 04:392). With n = 3 runs both are inconclusive under the same test. The alignment difference (p = 0.0009) is the only run-level-significant gradient result, and it "predates the defense" (04:303: 0.058 vs 0.029 already in the clean pair). **Fix:** use one vocabulary: "consistent in sign across 3/3 runs, not significant at run level" for sparsity; "no consistent difference, equivalence not tested" for locality, or add a pre-stated TOST margin.

### Y7. Novelty of the identity is overstated in the front matter
"an identity we derive" (main.tex:89, 01:23, 06:9) vs "The algebra itself is not new" (04:145). It is the law of total probability over the target's clean-correct and clean-wrong samples, and the paper itself notes it is the TRADES natural-plus-boundary split. **Fix:** "an accounting identity whose premise (p ≈ 1) we measure", which is accurate and still shows what is new.

### Y8. The SVHN "sign decided by the protocol" result is about the signs of near-zero estimates
Two seeds, 50 epochs, no AutoAttack, no third architecture (04:244). The four estimates are +0.39, −1.00, −0.35 and +2.70 (`e7_transfer_summary.json`); paired CIs are given only for both-correct ([−0.76, +0.07]). Whether raw +0.39 or target-correct −1.00 differ from zero is not reported, so "two report a CNN advantage and two a ViT advantage" (main.tex:89) counts point-estimate signs. The TOST acceptance is a per-sample test on two fixed checkpoint pairs, not a run-level architectural statement (04:240 says so, but 05:21 and 06:9 cite it plainly). **Fix:** report paired CIs for all four SVHN protocols and phrase the result as "the endorsed protocols agree that there is no material asymmetry; the raw and successful-source rates would report opposite small effects".

### Y9. The TGR negative result rests on an unverified adaptation
The abstract and 02:76 ("none holds in our setting") count TGR among the readings that fail. The implementation is an adaptation whose per-path coefficients the authors did not verify against the original (`scripts/_t4_tgr.py:11-13`). On the attention path it zeroes one max and one min cell per (sample, head) over the N×N grid, not per (sample, channel) as 03:137 states (`experiments/c1_c2_tgr.py:80-93`). It is tested only ViT→CNN, against AT targets. 04:441 and 05:61 hedge correctly. **Fix:** run the original implementation if available, or write "our adaptation of TGR" wherever the result is summarised, and correct 03:137 for the attention path.

## 🟢 Minor

1. ViT-Tiny parameter count: the text says 5.7M (03:50; Table 1, p. 8; Fig. 1, p. 5; 04:441; 05:61), but the model has 5,526,346 parameters (`logs/C1_clean_vit_2001.log:3`); 5.7M is the 1000-class ImageNet head count. Write 5.5M.
2. Alignment estimator: the text describes all 500×499/2 pairs (03:121, 04:279), but the table values come from the within-batch-of-50 estimator in `results/c1_gradient/pair*/gradient_summary.json` (0.0378 / 0.0562). The all-pairs estimator gives 0.0381 / 0.0566 (`results/c1_a3/pair*/a3_gradient_paired.json`), and the signed column (0.0014 / 0.0005) is pair 1 only. The numbers barely move; the description should match.
3. Clean-stage selection uses clean validation accuracy (`src/training/trainer.py:241`, `cli/train.py:70`), not PGD-10 as 03:100 implies.
4. The first definition of successful-source (03:118) omits "source correct on the clean input"; the code uses tc & sc & sa (`protokoller.py:62`).
5. Attention displacement is TV on the un-renormalised CLS→patch mass (`experiments/c1_c4_attention_features.py:190-192`, `src/models/vit.py:345-355`), while entropy uses the renormalised row. State it or renormalise.
6. ViT seed 2001 AT ran epochs 1-5 on CPU and resumed on CUDA (`logs/C1_at_vit_2001.log:7, 26-33`), which qualifies 03:158 "every reported number will be reproducible ... CUDA determinism". Disclose it.
7. "Pre-registered analysis protocol" (01:31): the registration post-dates the start of training (04:187) and is an in-repo append-only file. Call it a "time-stamped registration".
8. The CIFAR-native ViT control is one checkpoint, test-selected, its log cut at epoch 60/100, dropout 0.1 (04:297-299; `logs/vit_cifar_tiny_at.log`). Downgrade "so the ordering is not an artifact of the upsampling" (04:303) to "consistent with".
9. The GitHub URL in main.tex:118 returns 404 (A1 V-36). It must be live before submission.
10. The "controlled arm" (04:125) moves the gap along a training trajectory, so the gap is confounded with training progress. "Within-trajectory arm" is a more accurate name.
11. AutoAttack summary McNemar in `experiments/run_autoattack_run2.py:287` is continuity-corrected chi-square, while the paper says exact (03:158). The reference sheet uses `binomtest`; confirm that only the exact values reach the paper.

## Claims vs evidence

| # | Claim (location) | Evidence | Verdict |
|---|---|---|---|
| 1 | Protocol "decides the conclusion" (title; main.tex:89) | Endorsed protocols agree in sign on all 3 datasets (Table 3 p. 9; 04:204; 04:240) | Not supported as stated (R1) |
| 2 | "much of the disagreement [in the literature] comes from the measurement protocol" (main.tex:89) | No literature re-analysis; absolute ordering protocol-invariant (04:41) | Not tested (R1) |
| 3 | Asymmetry 4.4-19.4 across protocols (main.tex:89) | FOY Table III; `variance_ratio.json` | Supported |
| 4 | Retraining moves it "under 1.5 points" (main.tex:89) | SD 0.23-1.27; range 0.46-2.41 | Supported only as an SD; wording misleading (Y1) |
| 5 | 9.21 removed by identity; 5.79 different estimand; 3.91 residual (main.tex:89) | `fig_protokol_kumeleri_veri.json`; identity prediction 9.196 (A1 V-12) | Supported (accounting) |
| 6 | Identity "we derive"; premise measured (main.tex:89; 04:143) | p 0.989-1.000 over 36 AT directions (`ozdeslik_kontrol.json`) | Supported for AT targets; novelty overstated (Y7); standard targets rest on quarantined 0.88 (Y4) |
| 7 | CIFAR-100 sign preserved 12/12 (main.tex:89) | `e1_transfer_summary.json` (min +4.21) | Supported; 1 of 3 registered predictions failed and 1 band missed, not in abstract |
| 8 | SVHN: protocol decides the sign (main.tex:89; 04:240) | +0.39, −1.00, −0.35, +2.70; 2 seeds; CI only for both-correct | Weak: signs of near-zero point estimates (Y8) |
| 9 | Mechanism: three-protocol slope +0.431 / +0.470 / +0.673 (04:123-127) | 19/20 pairs: spread ≡ identity term; +0.470 has no artifact | Circular; provenance gap (R2) |
| 10 | Direction tracks target vulnerability r = 0.986 (01:25; 04:172) | 3 targets, one external | Suggestive only (body says so; intro does not) |
| 11 | Selection rule is a "fourth source of variance" (main.tex:89; 04:455) | `e2_grid.json`: PGD-10 moves 1.58-2.85 | Supported for absolute accuracy; effect on the asymmetry not measured (Y2) |
| 12 | Sparsity ordering "survives" (01:27; 06:13) | Holm run-level p 0.108; 3/3 sign | Reproducible in sign, not significant (Y6) |
| 13 | Depth profile reproduces across checkpoint sets (05:31; 06:13) | 04:388: CNN curve differed on earlier set | Contradicted by body (Y5) |
| 14 | No spatial localization difference (01:27; 04:333) | p 0.40-0.54, n = 3, no TOST | Inconclusive, not negative (Y6) |
| 15 | Attention entropy unchanged (04:392) | TOST ±0.05 nats accepted in 12 layers, n = 1000 | Supported |
| 16 | TGR gives no gain (01:27; 04:439) | McNemar favours MI-FGSM in all runs (FOY C2) | Supported for this adaptation and regime only (Y9) |
| 17 | Direction stable across "attack families on both CIFAR datasets" (06:9) | MI-FGSM on CIFAR-10 only | Overstated (Y5) |
| 18 | CNN absolute advantage under every attack (04:41) | McNemar p < 1e-84 (AA) per run; FOY Table I | Supported |

## Missing experiments or references (ranked by value per GPU-hour)

1. **p on standard-trained targets in the current pipeline** (no training; C1 clean checkpoints exist). This replaces the quarantined 0.88 and sets the identity's scope for the regime most transfer papers use.
2. **The selection rule's effect on the asymmetry itself** (no training; stored trajectories in `results/q1/e2`, `e3_akolu*`). This is the like-for-like competitor to the protocol effect that the paper currently lacks.
3. **Applying the identity to at least one published raw-rate table** with reported clean accuracies. This is the only way to support "much of the disagreement" and "can be applied directly to published results" (02:74).
4. **All 9 cross-pairings of the 3 ResNet × 3 ViT seeds** for the retraining variance of the asymmetry. Pairing by index (03:100) is arbitrary and uses a third of the available contrasts. (This is how I would do it differently, not an error.)
5. **One ViT run trained to schedule completion** (or last-checkpoint evaluation) to show how the spread moves with the clean gap within CIFAR-10 (Y2).
6. **A documented literature sweep** behind "rarely reported" (01:11, main.tex:89, 02:54 "remain scarce"): how many CNN-vs-ViT transfer papers state their conditioning set. Without it, these remain unsupported assertions.
7. Longer term, already acknowledged (05:71): a capacity-matched pair and a pretrained ViT. Mo et al. and Debenedetti et al. are cited for recipe sensitivity; no new reference is required.

## Questions a reviewer will ask, with pre-emptive answers

1. **"Your four protocols estimate four different quantities. Why is their spread a 'measurement effect' rather than a definitional fact?"** The paper's current answer (05:15) is the reader's ambiguity when the protocol is unnamed. A stronger answer is to lead with the 3.91 points between the two endorsed protocols, both defensible for directional claims, set against a seed range of at most 0.86 under those protocols.
2. **"Why compare against seed variance and not recipe or dataset variance, which are what you say the literature blames?"** Currently there is no answer. Report the dataset effect on the primary asymmetry (+10.92 vs −0.35) honestly, and either add the selection-rule effect on the asymmetry or limit the claim to seed variance.
3. **"Would the 15-point spread exist with a well-trained ViT?"** By the paper's own mechanism it would shrink with the gap (SVHN: 3.70 at a 1.85-point gap). Say so in the abstract, and report the within-CIFAR-10 sensitivity of Y2.
4. **"Is the three-protocol slope anything more than the identity?"** No. Present it as an out-of-sample check of the identity (R2).
5. **"Does p ≈ 1 hold for standard-trained targets?"** Measure it on the C1 clean checkpoints (Y4).
6. **"Were the earlier checkpoints trained with the same inner-loop code?"** The timestamps suggest yes (diagnostic script 2026-07-07 20:15, at_run3 created 20:22, fix committed 2026-07-11). State it explicitly.
7. **"Why was the ViT selected at epoch ~20 of 100 while its clean accuracy was still rising?"** Patience 20 with a 0.1-point threshold on a validation signal with about 1-point SE. Acknowledge this, and quantify its effect on the gap and the spread.
8. **"Can SVHN with two seeds support an equivalence claim?"** Only per checkpoint pair, as 04:240 already says. Remove the unqualified uses in 05:21 and 06:9.
9. **"Is the TGR failure a property of TGR or of your adaptation?"** It can't be told apart without the reference implementation; say "our adaptation" throughout.
10. **"Why is sparsity a positive result at p = 0.108 while locality is a negative one at p ≈ 0.5?"** Under the same test both are inconclusive at three runs; harmonise the vocabulary (Y6).
