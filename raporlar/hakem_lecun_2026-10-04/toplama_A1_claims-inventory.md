# Toplama A1: iddia envanteri (lens A, bilim ve tasarim)

Toplayici A1. Yalniz toplama ve dogrulama; yargi, derece ya da oneri yok. Konumlar `main.tex:satir` ve `sections/NN_*.tex:satir` bicimindedir (kisaltma: 01 giris, 02 ilgili calisma, 03 yontem, 04 deneyler, 05 tartisma, 06 sonuc; `ABS` = main.tex:89, ozetin tek satiri). Tum alintilar `paper/manuscript/` altindaki dosyalardan birebirdir; uzun cumlelerde "..." kesme isaretidir. Kaynak sayilar `results/C1_REFERANS_FOYU.md` (kisa: FOY) ve `results/q1/*`, `results/c1_*` altindan alindi; karantina klasorlerine bakilmadi.

## 0. On satirlik ozet

1. main.tex ozeti (ABS, 248 sozcuk) ile alti bolum dosyasi bastan sona okundu; 123 iddia kaydi (C-01 ... C-123), uc yerde (ozet, giris, sonuc) karsilastirma tablosu (bolum 2, 16 satir), "first / to our knowledge / novel / we show / we prove / identity / closed form" taramasi (bolum 3) ve ozet sayilarinin ilk gecis tablosu (bolum 4, 20 satir) ile 37 dogrulama kaydi (bolum 5) ve 13 bulunamayan kalem (bolum 6) cikarildi.
2. "to our knowledge", "novel" ve "we prove" metinde HIC gecmiyor; "we show" yalniz ozette (main.tex:89); "we derive" ozet + giris (01:23) + sonuc (06:45); yenilik cumleleri 01:23, 02:74 ("we know of no controlled estimate"), 04:145 ("What is new here") ve 01:31.
3. Ozet sayilarinin tamami govdede var ve FOY / q1 artefaktlarina uyuyor (bolum 4, 5); 9.21 + 5.79 = 15.00 (15.01 degil), metin bunu 04:117 ve 04:113'te kendisi aciklıyor.
4. Uc yerin ayni sayiyi ayni sertlikte soyleyip soylemedigi bolum 2'de: ozellikle (a) "under 1.5 points" govdede standart sapmadir (0.23 ile 1.27), ozet/giris/sonucta "moves it by under 1.5 points" olarak SD'siz geciyor; (b) giris 01:25 "reframes the asymmetry as a property of the weaker target" iken 04:172 "can only be suggestive", sonuc "associates"; (c) sonuc 06:49 "depth profile ... reproduce across independent checkpoint sets" iken 04:388 "the shape of the CNN curve ... recipe-dependent".
5. Sonuc 06:45 "stable across protocols, seeds, and attack families on both CIFAR datasets"; govdede MI-FGSM ve L2 kontrolu yalniz CIFAR-10'da (04:121, 05:21, 04:269); CIFAR-100'de yalniz PGD-10 L_inf.
6. Ozet/giris/sonuc CIFAR-100 icin "sign preserved in all twelve" diyor; 04:206 uc kayitli ongoruden birinin dogrulandigini, birinin basarisiz ve birinin sinanamaz oldugunu, 04:208 bir uc nokta bandinin (ViT temiz, 33-40 yuzde, olculen 43.17) kacirildigini yaziyor; bunlar ozet/giris/sonucta yok.
7. Karantina kaynakli sayilar metinde var: "earlier single-run checkpoints" (tablo conditional alt blok, tablo transfer son sutun, 04:66, 04:117, 04:305, 04:388, 01:25, 05:23), p = 0.88 (04:145, "pre-correction runs"), ViT 77.50 (04:66). FOY bunlari "run3 fark" ve "Eski tek kosu (sizintili)" etiketiyle kendisi tasiyor (FOY:33, 51-56); 0.88 ve 77.50 FOY'da ve q1 JSON'larinda bulunamadi.
8. Bulunamayan kaynaklar (grep ile): 04:123/127'deki SVHN-dahil uc-protokol egimi +0.470 [0.361, 0.665] (yalniz `scripts/_t3_en_kisalt6.py` icinde metin olarak, hicbir sonuc JSON'unda yok); 77.50; 0.885/0.802 (ViT/ResNet temiz-egitim oranlari); ViT-native gradyan sutunu (0.405 vb.); "13 of the 18" cift sayisi dogrudan JSON'da yok.
9. GitHub adresi (main.tex:118, "publicly available at https://github.com/cagrisahin58/cnn-vit-robustness-protocols") 2026-10-04'te HTTP 404 donuyor; yerel kopya `teslim/acik_depo/...` var ama uzak adres tanimli degil (`git remote -v` bos).
10. Yeniden hesaplananlar: 9.21 ve 3.91 ve 15.01 farklari, kimlik tahmini (9.196 vs 9.21), tum ozet sayilari, CIFAR-100 / L2 / SVHN yayilimlari (13.83, 10.92, 3.70), kosu-duzeyi p degerleri (0.067, 0.036, 0.042, Holm 0.108, 0.0009; mekansal Holm 0.54/0.40/0.54/0.47) ve secim-yayilimi araliklari; hepsi metinle uyustu. Uyusmayan ya da aciklanamayan kalemler bolum 6'da.

## 1. Iddia envanteri

Tur: R sonuc, M mekanizma, Y yenilik, O oneri, L sinirlilik, B bilgi (tasarim/yontem iddiasi). "Ozet/Giris/Sonuc" sutunu: O = ozette var, G = giriste var, S = sonucta var, "-" = yok; ayrinti bolum 2'de.

### 1.1 Baslik ve ozet

| id | tam cumle (alinti) | konum | tur | kanit isareti | O/G/S |
|---|---|---|---|---|---|
| C-01 | Baslik: "The Measurement Protocol Decides the Conclusion: A Methodological Study of CNN and Vision Transformer Adversarial Robustness Comparisons" | main.tex:56-57 | R | Tablo transfer_protocols, Sek. 4.2-4.4 | baslik |
| C-02 | "Comparisons of adversarial robustness across architecture families reach conflicting conclusions, usually attributed to models, training recipes, or datasets. We show that much of the disagreement comes from the measurement protocol." | ABS | R/Y | 04 (tablo transfer_protocols); 01:9-11 | O G S |
| C-03 | "On adversarially trained ResNet-18 and ViT-Tiny pairs, three runs each, with full-test-set per-sample logging and a validation split held out before training, we fix models, data, threat model and attack budget and vary only how transfer is scored." | ABS | B | 03:100; 03:118 | O G |
| C-04 | "Across four conditioning protocols the measured CNN-to-ViT transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10, whereas retraining both architectures moves it by under 1.5 points." | ABS | R | tablo transfer_protocols; 04:451 | O G S |
| C-05 | "The 15.01-point spread has two parts: an identity we derive removes 9.21 points in closed form, and 5.79 points come from a protocol that estimates a different quantity." | ABS | R/Y | 04:113, 04:117, eq:raw_identity | O G S |
| C-06 | "What survives is 3.91 points of discretion between the two protocols we endorse." | ABS | R | 04:117 | O G S |
| C-07 | "The identity equates the deviation of unconditioned from conditioned rates with the target's clean error scaled by one minus the conditioned rate, on a premise we measure rather than assume." | ABS | M | eq:raw_identity; 04:143 | O G S |
| C-08 | "Replicating on CIFAR-100 preserves the sign in all twelve measurements." | ABS | R | 04:204; tablo cifar100_results | O G S |
| C-09 | "On SVHN, where the same recipe leaves the architectures 1.85 points apart in clean accuracy, the protocol decides the sign as well as the size: two report a CNN advantage and two a ViT advantage, though the two we endorse agree." | ABS | R | tablo svhn_protocols; 04:240 | O G S |
| C-10 | "Varying only the checkpoint-selection rule adds a fourth, rarely reported, source of variance." | ABS | R | 04:455 | O G S |
| C-11 | "Three further readings do not hold under direct measurement; we close with reporting requirements for cross-architecture robustness studies." | ABS | R/O | 04:333, 04:392, 04:439; 05:36-43 | O G S |

### 1.2 Giris (01_introduction.tex)

| id | tam cumle (alinti) | konum | tur | kanit | uyum notu |
|---|---|---|---|---|---|
| C-12 | "The literature answers this question inconsistently: Bai et al. report that under matched training recipes transformers do not surpass CNNs, whereas Benz et al. report ViTs to be more robust for standardly trained models." | 01:9 | B | bai2021transformers, benz2021adversarial | giris |
| C-13 | "...whereas Naseer et al. find that perturbations crafted on ViTs transfer poorly under conventional attacks, and the direction measured in this paper is the opposite of the first group's, a point Section 5 returns to." | 01:9 | R | 05:17 | giris; 05:17 tekrar eder |
| C-14 | "These disagreements are usually attributed to differences in models, training recipes, or datasets, and the standard response is to compare under a matched recipe." | 01:9 | B | (atif yok) | ozet "usually attributed" ile ayni |
| C-15 | "Yet even when the models, the data, the threat model, and the attack budget are all held fixed, the conclusion still depends on a choice that is rarely reported: the measurement protocol." | 01:11 | R/Y | 04.2 | "rarely reported" icin atif/tarama yok |
| C-16 | "Papers usually treat these choices as reporting details, but they are part of the result." | 01:11 | B | - | genel iddia, atifsiz |
| C-17 | "...a fixed validation split held out before any training stage, so that no model is selected on data it has seen." | 01:16 | B | 03:100 | 04:212: "the same held-out split serves selection at both stages instead of two independent splits" |
| C-18 | "All evaluations run on the full test set with per-sample outcome logging, which makes paired statistics possible: the same samples can be re-weighted under different protocols without re-running an attack." | 01:16 | B | 03:118 | SVHN tam test n = 26,032 (04:224); L2 AutoAttack 5,000 altkume (04:256); gradyan n = 500, ozellik kaymasi n = 1000 |
| C-19 | "Architecture comparisons also invite three readings that we treat as measurable hypotheses: that CNN input gradients are spatially more localized, that adversarial perturbation degrades ViT attention, and that ViT-specific transfer attacks improve cross-architecture transfer. Only the last is a published claim; the first two are interpretations..." | 01:18 | B | 04:313, 04:359, 04:421 | 02:76 ve 06:49 ayni cumle |
| C-20 | "Our first contribution is to quantify protocol sensitivity. On identical models and data, the measured cross-architecture transfer asymmetry ranges from +4.4 to +19.4 points across four conditioning protocols, whereas retraining both architectures from scratch moves the same quantity by under 1.5 points." | 01:23 | R/Y | tablo transfer_protocols | SD (govde) / "moves" (giris) |
| C-21 | "The spread decomposes as follows. The 9.21 points that separate the unconditioned estimate from the target-correct estimate are removed in closed form by an identity we derive, and 5.79 points come from a protocol that estimates a different quantity." | 01:23 | R/Y | 04:117 | 15.01 giriste gecmiyor |
| C-22 | "After the correction, 3.91 points of discretion remain between two protocols that are both defensible, still more than twice the retraining effect." | 01:23 | R | 04:117 | "endorse" (ozet) / "defensible" (giris) |
| C-23 | "The protocol also decides whether an equivalence test is accepted or rejected." | 01:23 | R | 04:117 (erken kontrol noktasi, hedef-dogru, +/-2 kabul), 04:240 (SVHN) | ilk delil karantina kaynakli |
| C-24 | "The direction of the asymmetry, unlike its magnitude, is stable as long as the two models differ in clean accuracy; once they are matched, two of the four protocols reverse it." | 01:23 | R | 04:121, 04:240-242 | 05:21 ve 06:45 ile uyumlu |
| C-25 | "A full replication on CIFAR-100 leaves the spread close to its CIFAR-10 size and preserves its sign, and the offline checkpoint-selection rule, varied on a fixed training trajectory, turns out to be a source of variance that papers rarely report." | 01:23 | R | 04:204-212, 04:455 | basarisiz kayitli ongoru yok |
| C-26 | "The second contribution concerns unconditioned transfer rates, which are confounded by the target's clean error. In a 3x3 transfer matrix that adds a WideResNet-28-10 reference, the deviation of raw from conditioned rates obeys an identity." | 01:25 | R/M | tablo transfer_matrix | |
| C-27 | "Because samples the target already misclassifies are essentially never rescued by the perturbation (0.989 to 1.000 over 36 directions), the raw rate equals the clean error plus the conditioned rate scaled by one minus that error, to within 0.41 points." | 01:25 | R | 04:143 | |
| C-28 | "Incoming transfer also tracks the target's own vulnerability (r = 0.986 across three targets), which reframes the asymmetry as a property of the weaker target." | 01:25 | M | 04:172 | 04:172: "can only be suggestive"; 06:45 "associates" |
| C-29 | "Absolute robustness, for its part, factors exactly into clean accuracy and conditional susceptibility. Both factors need to be reported, because the attribution between them changed between our earlier single-run checkpoints and three fresh runs while the absolute ordering did not." | 01:25 | R/O | tablo conditional | kanit karantina kaynakli "earlier" blok |
| C-30 | "Three of the results we report are negative: scale-invariant sparsity differences do not correspond to spatial localization differences, on all four spatial measures; CLS attention entropy does not change measurably under attack at n=1000; and Token Gradient Regularization, a ViT-specific transfer attack, gives no transfer gain in this regime, losing to plain MI-FGSM under a matched budget." | 01:27 | R | tablolar spatial, tgr; 04:392 | TGR "adaptation" notu giriste yok |
| C-31 | "Two behavioral differences do survive. Gradient sparsity differences reproduce across independent checkpoint sets, are created by adversarial training, and are accompanied by an alignment difference that exists only in absolute cosine. Adversarial damage accumulates at qualitatively different depths in the two architectures, and the measured drift profile depends on the token aggregation used to compute it." | 01:27 | R | 04:303-305, 04:388-390 | kosu-duzeyi Holm p = 0.108 (04:303) giriste yok |
| C-32 | "The measurements translate into concrete reporting requirements for cross-architecture robustness studies, which are collected at the end of the discussion." | 01:29 | O | 05:36-43 | |
| C-33 | "...it corrects one claim of the earlier version: the direction of the asymmetry is not stable once the architectures are matched in clean accuracy." | 01:31 | R | 04:240-242; sahin2026behavioral | |
| C-34 | "A preliminary version of this study was submitted to ATEEC 2026 ... The present paper adds two further datasets, a second threat model, the algebraic identity of Section 4, the checkpoint-selection ablation, the transformer-specific transfer attack, and the pre-registered analysis protocol" | 01:31 | B | references.bib `sahin2026behavioral` ("Preliminary version of the present study; submitted") | |

### 1.3 Ilgili calisma (02_related_work.tex)

| id | tam cumle (alinti) | konum | tur | kanit | not |
|---|---|---|---|---|---|
| C-35 | "Behavioral comparisons between CNN and ViT robustness under a single evaluation protocol remain scarce." | 02:54 | Y | (atifsiz) | belgelenmis tarama yok (bolum 7) |
| C-36 | "We vary it along the conditioning axis instead, with the models, the data and the attack budget fixed, which isolates the contribution of the conditioning set and makes it possible to state the arithmetic relation between the resulting estimates." | 02:62 | Y | 04:117 | Yu et al. (`yu2025reliable`) ve TA-Bench ile ayrim |
| C-37 | "...existing comparative work typically reports robustness scores in isolation, often with inconsistent perturbation budgets, attack configurations, or model scales, and rarely pairs the comparison with behavioral analysis." | 02:72 | Y | `pinto2022impartial`, `bai2021transformers` (yalniz iki atif) | genel saptama |
| C-38 | "A recent study in this journal compares ViT and CNN adversarial robustness directly; our work differs by evaluating on the full test set with AutoAttack and paired statistics, by controlling transfer measurement for clean-accuracy differences, and by accompanying the comparison with gradient- and feature-level behavioral analyses." | 02:72 | Y | `ali2024adversarial` (references.bib:356-363, journal = IEEE Access, doi 10.1109/ACCESS.2024.3435347) | "this journal" = IEEE Access dogru |
| C-39 | "That work concerns attack strength, that is, whether the measurement is strong enough. The question we ask is orthogonal: with attack strength held fixed, how much does the conditioning set alone move the conclusion?" | 02:74 | Y | `carlini2019evaluating`, `tramer2020adaptive` | |
| C-40 | "...individual papers pick one conditioning set and proceed. Yu et al. vary the scoring rule too, but along a different axis, and we know of no controlled estimate of how much the choice of conditioning set matters. We supply one by varying only the protocol with everything else held fixed." | 02:74 | Y | - | "we know of no" = bilinen en acik yenilik cumlesi |
| C-41 | "The confound in unconditioned rates then takes the form of an identity, r_raw - r_cond = e (1 - r_cond), which turns a known qualitative caveat into a correction that can be applied directly to published results." | 02:74 | Y/M | eq:raw_identity | |
| C-42 | "...three readings that architecture comparisons tend to suggest ... Only the third is claimed in the cited work; the first two are interpretations. We measure each directly, and none holds in our setting." | 02:76 | R | 04:333, 04:392, 04:439 | "none holds" = en guclu soyleyis; govde TGR'yi "adaptation" sayiyor (03:137) |

### 1.4 Yontem (03_methodology.tex)

| id | tam cumle (alinti) | konum | tur | kanit | not |
|---|---|---|---|---|---|
| C-43 | "...it is excluded from the training set of both the clean and the adversarial stage, so no checkpoint is ever selected on data it was trained on. The test set is touched only by the final post-hoc evaluations." | 03:100 | B | `data/` bolme indeksleri (seed 777) | 04:299 (tablo gradient altnotu): CIFAR-native ViT kontrolu "selected on the test set"; 04:455 test PGD-10 ustunde secim kurali izgarasi (post-hoc) |
| C-44 | "...absolute robust accuracy factorizes exactly as robust = clean x conditioned survival" | 03:111 | B | 04:64 (85.78 x 0.442 = 37.93) | tanimdan gelen esitlik |
| C-45 | "Conditioning transfer evaluation on correctly classified samples is established practice, usually on the samples that every model in the study classifies correctly; the target-correct rate is the one-sided relaxation of that pool" | 03:118 | B | liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, zhao2025revisiting | |
| C-46 | "Both are established. The successful-source rate is the transferability metric of Ravikumar et al., whose Equation (1) divides the number of examples that transfer to the target by the number generated against the source, over a pool restricted to samples both models classify correctly" | 03:118 | B | ravikumar2023trend | 04:119: metrik, "sub-choice" a gore 14.60 (gevsek) / 19.37 (siki); makale siki okumayi raporluyor |
| C-47 | "For directional claims we take the both-correct rate as the primary estimate, because it scores both directions on identical samples and therefore supports paired inference; the other three are reported beside it throughout." | 03:118 | B | 05:19 | 04:117 ayni zamanda "the two protocols we endorse ... target-correct and both-correct"; 05:19 hedef-dogru icin "pulls two directions toward each other" |
| C-48 | "Equivalence claims use two one-sided tests (TOST) at a primary margin of +/-2 points, fixed before the comparisons ... That is the right scale for an absolute accuracy and the wrong one for the transfer asymmetry, whose run-to-run standard deviation is 0.23 points, so there the margin is some eight times too generous and biases TOST toward accepting equivalence. We keep the pre-registered margin..." | 03:158 | B/L | 04:240 | +/-1 ve +/-3 de rapor ediliyor |
| C-49 | "All evaluation and analysis scripts fix random seeds (seed 42, including CUDA determinism flags), so every reported number will be reproducible from the pipeline we release." | 03:158 | B | main.tex:118 | gelecek zaman; 118'de simdiki zaman |
| C-50 | "We separate four sources of variance and report each where it applies." (egitim kosusu, saldiri baslangici, protokol, kontrol noktasi secimi) | 03:156 | B | 04:449-457 | |

### 1.5 Deneyler (04_experiments.tex)

| id | tam cumle (alinti) | konum | tur | kanit | not |
|---|---|---|---|---|---|
| C-51 | "The CNN holds an absolute robustness advantage under every attack: ResNet-18 AT reaches 37.93+/-0.14% robust accuracy under AutoAttack against 29.14+/-0.40% for ViT-Tiny AT." | 04:41 | R | tablo main_results; FOY:16-17 | McNemar p < 1e-84 (AA), < 1e-120 (PGD-10); FOY:42-44 ile uyumlu |
| C-52 | "Seed-level variation for the adversarially trained pair is at most 0.55 points on any reported accuracy, so the ordering is not run-to-run noise" | 04:41 | R | tablo main_results (en buyuk SD 0.55, ViT temiz) | |
| C-53 | "Both factors favor the CNN. It starts from a 12.3-point higher clean accuracy and loses a smaller fraction of what it solves, with conditional fooling of 48.58 versus 55.53% under PGD-10 and 55.78 versus 60.37% under AutoAttack." | 04:64 | R | tablo conditional; FOY:28-29 | |
| C-54 | "On the n=7,061+/-68 samples both models classify correctly ... the CNN leads by 13.8 and 10.7 points (McNemar p<1e-67 in every run...)" | 04:64 | R | FOY:31, 36-40 | 59.86-46.11 = 13.75; 51.89-41.15 = 10.74 |
| C-55 | "Our first checkpoints, selected with a validation split that clean pre-training had already seen, gave the same absolute ordering but the opposite conditional one: fooling rates that were indistinguishable under PGD-10 (52.15 versus 52.33%) and slightly ViT-favorable under AutoAttack (58.16 versus 56.46%)" | 04:66 | R | FOY:33 ("Eski tek kosu (sizintili)") | karantina kaynakli sayilar |
| C-56 | "We cannot isolate a cause ... a data-quantity explanation does not hold, because the corrected clean models are better despite seeing 2,000 fewer images (80.09+/-0.60 versus 77.50% for the ViT)." | 04:66; 05:57 | L | 80.09 FOY:15; 77.50 kaynak bulunamadi | 05:57 "A data-quantity explanation is ruled out" |
| C-57 | "...the mean per-seed spread between the largest and the smallest protocol estimate is 15.01+/-0.84 points, and the extreme estimates stand in a 4.4-fold ratio, whereas the seed-level standard deviation within any single protocol stays below 1.5 points." | 04:117 | R | FOY:60; q1/variance_ratio.json (aralik_ortalama 15.0067, aralik_sd 0.8409) | |
| C-58 | "The target-correct estimate sits 9.21 points below it, and that entire gap is what Equation (eq:raw_identity) predicts in closed form, so a reader given the target's clean error can remove it exactly." | 04:117 | R/M | q1/fig_protokol_kumeleri_veri.json `ozdeslik_terimi_ham_eksi_hedef_dogru` = 9.21 | tahmin 9.196 (bolum 5, V-12) |
| C-59 | "What survives the correction is the difference between the two protocols we endorse for directional claims, target-correct and both-correct, which differ only in whether the source must also be correct: 3.91 points, still more than twice what retraining both architectures moves. That residual is 5.97 points on CIFAR-100 and 0.65 on SVHN." | 04:117 | R | q1 JSON `artik_takdir_her_ikisi_eksi_hedef` = 3.91; c100 4.957 / 10.923 -> 5.966; svhn -1.005 / -0.35 -> 0.655 | 3.91 = 8.27 - 4.36; 15.01 - 9.21 = 5.80 |
| C-60 | "The pivot structure is dataset-dependent: on CIFAR-100 the unconditioned estimate is the largest of the four, so the whole 13.58-point spread there is the identity term and the successful-source estimate falls inside it." | 04:117 | R | q1/cifar100/transfer/e1_transfer_summary.json (ham 18.53, hedef-dogru 4.96, basarili-kaynak 17.50) | 13.58 = aralik-ortalamalari; seed-ortalamasi 13.83 (04:204) |
| C-61 | "Under the both-correct protocol ... the difference is 8.27+/-0.24 points ... The sign-flip permutation p is below 5e-5 in every seed, and TOST fails to establish equivalence at any of the three margins (+/-1, +/-2 and +/-3 points, p=1.0 in each)... On our earlier checkpoints, under the target-correct protocol, the same pipeline had accepted equivalence at +/-2 points." | 04:117 | R | FOY:58 | son cumle karantina kaynakli |
| C-62 | "Averaging their endpoints gives [7.33, 9.22], a description of three intervals that carries no coverage guarantee of its own; for inference at the run level, the across-run t interval is [7.68, 8.86]." | 04:117 | R | FOY:58 (GA [7.33; 9.22]) | t araligi icin FOY'da satir yok; hesaplanabilir |
| C-63 | "Under the looser reading, which also admits samples the source already misclassified, the measured asymmetry falls from +19.37 to +14.60 points and the protocol spread from 15.01 to 10.45 points. That shift of 4.77 points is larger than the run-to-run standard deviation of any protocol ... by more than a factor of three..." | 04:119 | R | q1/_b2_olcum.json (`yayilim_gevsek` / `yayilim_siki`) | 19.37 - 14.60 = 4.77; 4.77/1.27 = 3.76 |
| C-64 | "What is stable is the direction: CNN-crafted examples transfer better to the ViT than the reverse under all four protocols, in all three seeds, and also under the momentum-based MI-FGSM (19.07+/-0.33 versus 15.42+/-0.52% target-correct ...), so the effect is not an artifact of the PGD attack itself." | 04:121 | R | results/c1_behavior_summary.json `mifgsm` (19.0741 / 15.4209) | MI-FGSM yalniz CIFAR-10 |
| C-65 | "The mechanism behind the spread is compositional. Samples that the target solves on clean input but the source does not are three to four times more fragile than jointly solved ones (41.2+/-0.8% and 59.1+/-1.7% fooling versus 10.0 and 18.3%) ..." | 04:123 | M | (kaynak bu cumle icin aranmadi; bolum 7) | |
| C-66 | "across 18 direction pairs drawn from six seed-and-dataset clusters, the spread of the four-protocol asymmetry falls as the clean-error gap between the two models widens (slope -0.528, cluster-bootstrap CI [-0.664, -0.418]), whereas the spread computed without the successful-source protocol rises with it (slope +0.431, CI [+0.333, +0.633])." | 04:123 | M | q1/e3_surucu_ayristirma.json; e3_iki_kol_fit.json | uyusuyor |
| C-67 | "We therefore withdraw the four-protocol slope; the mechanism claim rests on the three-protocol one, which survives the pool question" (SVHN-dahil: -0.133, CI [-0.570, +0.469]; uc-protokol +0.470, CI [+0.361, +0.665]) | 04:123 | M | -0.133: q1/e3_asimetri_fit_svhnli.json; +0.470 [0.361, 0.665]: sonuc JSON'unda bulunamadi | bolum 6, N-1 |
| C-68 | "The pool for this fit excludes the SVHN pair, which departs from the pre-registration. The registration placed SVHN in the fitted arm ... its reassignment to an independent consistency check was written after the SVHN result was in hand, so the SVHN-inclusive fit is the pre-registered one." | 04:123 | L | - | on-kayit sapmasi metinde aciklaniyor |
| C-69 | "Excluding the successful-source protocol, the two arms agree: +0.673 (CI [+0.602, +0.727]) in the controlled arm against +0.470 (CI [+0.361, +0.665]) in the observational arm on the pre-registered pool" | 04:127 | M | +0.673: e3_iki_kol_fit.json (A, uc protokol); +0.470 bulunamadi | |
| C-70 | "Equation (eq:raw_identity) consequently reproduces every measured unconditioned rate to within 0.41 points, with a mean absolute residual of 0.095 points; the residual accounts for at most 1.39% of the deviation being explained." | 04:143 | R | q1/ozdeslik_kontrol.json (mutlak_max 0.41, mutlak_ort 0.0947, yuzde max 1.388, n_yon 36, P min 0.989014 max 1.0) | uyusuyor |
| C-71 | "The algebra itself is not new. Written over a single model instead of a source-target pair, r_raw = e + r_cond (1 - e) is the natural-plus-boundary decomposition of TRADES, where the premise corresponding to our p holds by definition ... What is new here is that in the transfer setting the premise is not definitional ... so p becomes an empirical quantity that has to be measured." | 04:145 | Y | zhang2019theoretically | ozet/giris/sonucta "an identity we derive" |
| C-72 | "Where p<1, Equation (eq:raw_identity) overstates the deviation by exactly e(1-p), so it is an upper bound and not an equality once the antecedent fails. We measure p between 0.989 and 1.000 on adversarially trained targets ... On standard-trained targets ... we observed p as low as 0.88 in our own pre-correction runs, a figure that indicates the order of magnitude but is not a measurement of the present pipeline; there the identity is a bound." | 04:145 | L | 0.989-1.000: ozdeslik_kontrol.json; 0.88: kaynak yok | 0.88 karantina kaynakli; metin kendisi "not a measurement of the present pipeline" diyor |
| C-73 | "Unconditioned transfer rates therefore do not measure transferability across architectures; they measure transferability plus the target's clean weakness, in a proportion that Equation (eq:raw_identity) makes explicit." | 04:147 | M | egim 0.762 (CIFAR-10), 0.656 (CIFAR-100): q1/c3_precision.json | 05:19, 06:45 ("not a valid basis ... at all") ile uyumlu |
| C-74 | "...incoming conditioned transfer is 18.50% for the ResNet target, 19.04% for the ViT target, and 10.57% for the WideResNet target, which tracks each target's own white-box conditioned fooling rate (48.52, 55.57 and 25.16%) with r = 0.986 over the three targets. On this evidence the CNN->ViT advantage is better read as a property of the weaker target ... the most robust target absorbs attacks from both families almost equally well. With only three targets, the correlation can only be suggestive." | 04:172 | M | FOY:81 (r = 0.986) | WRN hedefine gelen: CNN kaynakli 12.48, ViT kaynakli 8.65 (fark 3.83; tablo transfer_matrix) |
| C-75 | "One of the three registered predictions is confirmed, one fails under the reading we treat as binding, and the third is not testable in this design." | 04:206 | R/L | e1_cifar100_summary.json; 04:187 | ozet/giris/sonucta yok |
| C-76 | "...clean accuracy in the 33 to 40% band for the adversarially trained ViT and measured 43.17+/-1.10%." | 04:208 | L | e1_cifar100_summary.json (ort 43.17, sd 1.099) | |
| C-77 | "When the architectures are matched, the protocol decides the sign. ... the primary both-correct protocol ... the difference is -0.35 points, with a sign-flip permutation p of 0.105 and TOST equivalence accepted at all three margins ... The equivalence therefore rests on the within-run comparison and on the close agreement of the two runs (-0.34 and -0.36); two runs cannot bound the run-to-run variation." | 04:240 | R/L | q1/svhn/transfer/e7_transfer_summary.json (both_correct -0.35, degerler -0.34, -0.36; n_common 23870, 23565) | iki tohum |
| C-78 | "The protocol spread on SVHN is 3.70+/-0.62 points ... The relation is not monotone across the three: the largest gap does not produce the largest spread ... The direction we reported as stable ... is stable in the regime where the two models differ in clean accuracy, which is the regime both CIFAR datasets happen to occupy." | 04:242 | R | e7_transfer_summary.json (protocol_spread_pp 3.7, sd 0.622) | |
| C-79 | "SVHN was run in a reduced configuration fixed in advance: two seed pairs instead of three, 50 adversarial-training epochs, no AutoAttack, and no third architecture." | 04:244 | L | e7_svhn_summary.json (durma_epogu 50/50; n_tohum 2) | ozet "three runs each" |
| C-80 | "Under the changed norm the protocol spread shrinks to 10.92 points, against 15.01 under L_inf, yet stays far above both the two-point floor the pre-registration set and the run-to-run standard deviation, and the sign is positive in all twelve measurements ... The third prediction ... cannot fail once Equation (eq:raw_identity) holds" | 04:269 | R/L | cifar10_l2/transfer/e6_l2_transfer_summary.json (protocol_spread_pp 10.917) | |

Devam (deneyler, davranissal bolum, TGR, varyans):

| id | tam cumle / ozet (alinti) | konum | tur | kanit | not |
|---|---|---|---|---|---|
| C-81 | "Across all three scale-invariant sparsity measures, CNN gradients are sparser than ViT gradients, and the ordering reproduces in every run ... We therefore report the sparsity result as reproducible and not as significant. The alignment difference below does reach run-level significance (p=0.0009)" | 04:303 | R | tablo gradient; c1_behavior_summary.json | yeniden hesap: ham p 0.067 / 0.036 / 0.042; Holm 0.108; hizalanma 0.0009 |
| C-82 | "The ordering is a product of adversarial training, not of architecture: in the clean-trained counterparts of the same runs the ViT is the sparser model (Hoyer 0.380+/-0.009 versus 0.347+/-0.002)" | 04:303 | R | FOY:101-102 (0.3467 / 0.3804) | |
| C-83 | "...every quantity in Table (gradient) reproduces the ordering measured on our earlier single-run checkpoints, although in six of the eight cases the value itself moves by more than the seed-level standard deviation reported here." | 04:305 | R | (karantina kaynakli karsilastirma) | "independent checkpoint sets" = 3 yeni kosu + 1 eski tek kosu |
| C-84 | "The result is negative (Table spatial). None of the four measures shows a significant difference at the run level. ... Descriptions of CNN gradients as spatially localized are not supported by our measurements, and we restrict our own claims to sparsity." | 04:333 | R | tablo spatial; FOY:123-128 | esdegerlik testi yok (TOST yalniz dikkat entropisinde, 04:392); "spatial ordering is not stable across runs on two of the four measures" |
| C-85 | "In the ViT the drift is gradual and shallow ... In the CNN the damage is concentrated: ... layer4.0 ... 0.8777+/-0.0181 together with a -13.14+/-1.89% norm contraction ... On our earlier checkpoints the CNN profile fell monotonically to the last block, with no recovery, so the shape of the CNN curve, unlike the ViT profile, should be read as recipe-dependent." | 04:388 | R | FOY:112; c1_c4/pair*/c4_summary.json | 05:31 ve 06:49 ile gerilim (bolum 2, T-10) |
| C-86 | "At their respective minima the CLS pathway drifts about three times as far as the patch-token mean (0.9604 versus 0.9870, a ratio of 3.05 in 1-cos) ... Read at the MLP sub-block output instead ... a CLS minimum of 0.9343 at block 10, a patch-token minimum of 0.9840 at block 8 and a ratio of 4.12" | 04:390 | R | c1_c4/pair{1,2,3}/c4_summary.json (`cos_block_cls`, `cos_block_token_mean`: ortalamalar 0.9604 @11, 0.9870 @9, oran 3.054); FOY:108-111 (MLP alt blok) | 0.9604, 0.9870 ve 3.05 FOY'da yok, c4_summary'de var; 4.12: (1-0.9343)/(1-0.9840) = 4.106 yuvarlanmis degerlerle |
| C-87 | "Adversarial perturbation does not measurably change the entropy of the CLS attention distribution ... at most 0.005 nats ... TOST accepts equivalence in all twelve layers, the weakest at p=0.006. What does grow with depth is the displacement of the attention map, from 0.028 total variation in the first layer to 0.084 in the last ..." | 04:392 | R | FOY:113-114; c1_c45_summary.json | "attention degrades" okumasi icin yer degistirme sifir degil |
| C-88 | "...so any claim that adversarial attack degrades attention should be checked at this sample size before being made." | 04:392 | O | - | |
| C-89 | "Drift magnitude does not predict attack success either ... (0.9895 versus 0.9877)" | 04:394 | R | FOY:115 | |
| C-90 | "The attack collapses class structure most strongly in the CNN: clean-fit 5-NN label consistency drops from 87.3+/-2.6% to 51.3+/-1.8% ..." | 04:413 | R | (aranmadi, FOY'da yok) | bolum 7 |
| C-91 | "TGR does not improve transfer in this regime; it degrades it (Table tgr). The regularization behaves as designed on the source side, trading away 14.9 points of white-box strength ... conditioned transfer falls by 3.0 points under the target-correct protocol and by 2.2 under both-correct. Paired McNemar tests ... favor MI-FGSM in every run" | 04:439 | R | FOY:137-141 | 14.87, 3.01, 2.15 yeniden hesap |
| C-92 | "The claim we can support is that TGR's transfer advantage does not carry over to this regime; whether the method fails more generally is beyond what this experiment can show." | 04:441 | L | 03:137 | "Our TGR result ... comes from an adaptation of the original method, not a reproduction" (05:61) |
| C-93 | "Within a fixed seed pair, changing only the conditioning protocol moves the asymmetry by 15.01+/-0.84 points. ... Retraining both architectures from scratch moves that same asymmetry by a standard deviation of only 0.23 to 1.27 points, the value depending on which protocol it is measured under ... A fifteen-point measurement effect against a sub-1.5-point training effect is the ordering the paper rests on." | 04:451 | R | q1/variance_ratio.json | aralik (15.01) ile SD (0.23-1.27) karsilastirmasi; ayni dosyada `aralik_protokol_bazli`: 0.63, 0.86, 0.46, 2.41 |
| C-94 | "We do not headline the ratio of these two spreads ... for the successful-source protocol [chi2 interval] runs from 0.8 to 9.9 and includes unity. Reported as a sensitivity, the ratio spans 5.2 to 32.6 ... and equals 28.3 under the like-for-like comparison on the both-correct protocol" | 04:453 | L | variance_ratio.json (`ORAN_ACIKLIGI` 5.16-32.62; `sd_vs_sd` both_correct 28.29; GA [0.82, 9.9]) | 05:13 "fifteen points ... while retraining moves it by one" |
| C-95 | "...moves the reported PGD-10 accuracy by 2.62 to 2.85 points per seed for the ResNet and 1.58 to 2.09 points for the ViT. ... restricted to the split and patience choices ..., the dispersion falls to 1.09 times the seed-level standard deviation for the ResNet and 1.42 times for the ViT." | 04:455 | R | q1/e2/e2_grid.json (yayilim 2.85, 2.62, 1.58, 2.09; oran 1.092, 1.423) | |
| C-96 | "Selection choices can move a reported number by more than a training seed does, or leave it nearly untouched; which of the two happens depends on the plateau of the trajectory, not on the architecture." | 04:457 | R | q1/e1_cifar100_summary.json | |

### 1.6 Tartisma ve sonuc (05, 06)

| id | tam cumle (alinti) | konum | tur | kanit | not |
|---|---|---|---|---|---|
| C-97 | "The central result is an ordering of dispersions: measured on the transfer asymmetry itself, retraining both architectures from scratch moves it by a standard deviation of 0.23 to 1.27 points, whereas changing only the conditioning protocol moves it by 15.01+/-0.84 points." | 05:13 | R | 04:451 | |
| C-98 | "A quantity that the measurement choice moves by fifteen points while retraining moves it by one is not a stable property of the architectures, and reporting it without the protocol communicates almost nothing." | 05:13 | R | - | kat degeri soyleyisi (04:453 baslik yapmaz) |
| C-99 | "...the four protocols estimate four different quantities, so the distance between them is not a variance, and calling it one would be a category error. We agree, and we make no assumption that the architectures have a single true asymmetry ... the spread we measure is the size of that ambiguity, a bound on what the omission costs." | 05:15 | R | - | ozet "disagreement comes from the measurement protocol" |
| C-100 | "Under a both-correct protocol comparable to ours, Mahmood et al. report the opposite direction on a different architecture pair ... Our mechanism is compatible with those results ... Testing this properly would require their per-direction clean accuracies under a shared protocol, which is the reporting we ask for" | 05:17 | M/L | mahmood2021robustness | uyumluluk testlenmemis (metin kendisi soyluyor) |
| C-101 | "The unconditioned rate should not be used for architecture comparison at all ... The target-correct protocol removes that confound but admits samples the source itself cannot solve, and because those marginal subsets are highly vulnerable and asymmetrically sized, it pulls two directions toward each other by an amount that depends on the clean-accuracy gap. The both-correct protocol ... is the only one of the four that supports paired inference, which is why we treat it as the primary estimate." | 05:19 | O/M | 04:123 | "the two protocols we endorse" (04:117, ABS) |
| C-102 | "The direction is therefore a property of the unmatched regime: there the protocol changes how large the effect looks and whether equivalence is accepted, and once the models are matched it changes the sign as well." | 05:21 | R | 04:240-242 | |
| C-103 | "...the failure of a transformer-specific attack to rescue the ViT direction fits the same account. With three targets that correlation is suggestive; establishing it would take a larger model pool." | 05:21 | M/L | 04:172 | |
| C-104 | "In our corrected runs both favor the CNN, so the decomposition and the headline agree. They did not agree on our earlier checkpoints ... a paper reporting the decomposition from a single run would have drawn a mechanistic conclusion that does not replicate." | 05:23 | R | FOY:33 | karantina kaynakli "earlier" |
| C-105 | "Sparsity is not spatial locality: ... (Hoyer 0.4928 versus 0.4561, consistent in every run; per-sample p<1e-11, run-level p=0.108 after correction)" | 05:25 | R | 04:303 | |
| C-106 | "Adversarial perturbation does not measurably change CLS attention entropy. ... Attention-shift results obtained with patch attacks concern a different threat model and should not be generalized to L_inf-bounded perturbations without measurement." | 05:27 | R/O | 04:392 | |
| C-107 | "TGR costs 14.9 points of white-box strength and returns none of it at the target in our regime. The result is specific to this regime, since our targets are adversarially trained and our data are CIFAR-scale." | 05:29 | R/L | tablo tgr | |
| C-108 | "Two behavioral differences reproduce across independent checkpoint sets and are unaffected by the protocol question. ... The depth profiles differ as well: in the CNN the damage is concentrated in the last residual stage, whereas in the ViT it builds up gradually ..." | 05:31 | R | 04:388 | T-10 |
| C-109 | "Studies should state the conditioning protocol ... Unconditioned transfer rates should not be reported as architecture comparisons. ... since that relation is an algebraic identity, the correction can be applied to published raw rates without re-running anything." | 05:41 | O | eq:raw_identity | "antecedent" kosulu bu cumlede yok; 06:45 ve 04:145'te var |
| C-110 | "Next to the score, studies should report the decomposition ... Ranking claims should be separated from mechanism claims: our rankings were stable across checkpoint sets while our mechanism attribution was not, so mechanism claims should carry more training runs. ... Attention claims, finally, should be checked at a realistic sample size: the attention null result we report had looked positive on a small figure batch." | 05:43 | O | 04:66, 04:392 | |
| C-111 | "For practitioners choosing between the two families under matched standard adversarial training on this benchmark, the CNN gives higher absolute robust accuracy and the advantage holds under every view we measured." | 05:45 | O | tablo main_results | 04:66 erken kontrol noktasinda kosullu zayiflama ViT lehine (karantina kaynakli) |
| C-112 | "The protocol-sensitivity result is measured on three datasets and one model pair. ... That account is incomplete: it holds for three of the four protocols, while the successful-source protocol adds a second driver tied to the source's robustness that is strong enough to reverse the overall relationship." | 05:55 | L | 04:123 | |
| C-113 | "...a small clean-accuracy gap and a different training recipe are not separable here." | 05:55 | L | - | kucuk-bosluk ciftlerinin hepsi WRN iceriyor |
| C-114 | "We cannot isolate the cause of the differences between our two checkpoint sets. ... it does not measure leakage." | 05:57 | L | - | ozet/giris: "validation split held out before training" |
| C-115 | "Every model in this paper is trained inside a single threat model: L_inf at eps = 8/255. We evaluated the same checkpoints under an L_2 budget and the protocol spread survived, at 10.92 against 15.01 points" | 05:59 | L/R | 04:269 | ozet L2'yi anmiyor |
| C-116 | "Three runs per architecture bound seed variance but do not span the recipe space ... Our ViT results characterize baseline adversarial training, not the best achievable ViT robustness. ... The two models also differ in parameter count (11.2M versus 5.7M), so architectural attribution of the absolute gap remains partial. Our TGR result, finally, comes from an adaptation of the original method, not a reproduction of its published setting." | 05:61 | L | 03:50 | |
| C-117 | "The leakage ablation, on six full-budget trajectories, did not detect an effect of leakage on checkpoint selection, but it answers a weaker question than the one posed" | 05:71 | L | q1/e2 | ozet ve giris bu abla­syonu "selection rule varied" olarak sunar; "leakage ablation" adi yalniz 05:71'de |
| C-118 | "We asked how much of the disagreement in CNN and Vision Transformer robustness comparisons comes from the measurement and not from the models, and answered it by varying only how the comparison is scored, with everything else held fixed." | 06:43 | R | - | |
| C-119 | "Unconditioned rates are not a valid basis for such a comparison at all: ... an identity that holds to within 0.41 points across 36 measured directions and that applies to any published raw rate whose targets satisfy the measured antecedent." | 06:45 | R/O | 04:143 | |
| C-120 | "The direction is stable across protocols, seeds, and attack families on both CIFAR datasets, but not across datasets: on SVHN ... two of the four protocols reverse the sign and the primary protocol accepts equivalence. The direction, in other words, holds while the models are unmatched, and our three-target analysis associates it with the target's own vulnerability (r = 0.986)." | 06:45 | R | 04:121, 04:240 | "attack families on both CIFAR datasets": bkz. T-12 |
| C-121 | "In the conditional decomposition of absolute robustness both factors favor the CNN in our corrected runs, but the attribution between them differed on an earlier checkpoint set whose absolute ordering was identical." | 06:47 | R | tablo conditional | |
| C-122 | "Only the third is a published claim; the first two are interpretations that our own earlier figures encouraged. Two behavioral differences did survive and reproduce across independent checkpoint sets: the gradient sparsity ordering, which adversarial training creates, and the depth profile of adversarial damage, concentrated late in the CNN and spread across depth in the ViT." | 06:49 | R | 04:303-305, 04:388 | T-10 |
| C-123 | "Our study covers three datasets and a single model pair, so the size of the protocol effect for other architecture pairs remains to be calibrated; the mechanism behind it, an unequal clean-accuracy gap between targets, is not specific to our setting. The pipeline, the per-sample logs and the analysis scripts are publicly available" | 06:51 | L/B | main.tex:118 | "mechanism ... not specific to our setting" test edilmemis genelleme |

## 2. Ozet, giris, sonuc karsilastirmasi (ayni sayi, ayni kesinlik, ayni cekince)

Ozetteki "-" = o noktaya hic deginmiyor.

| id | iddia | ozet (main.tex:89) | giris | sonuc | fark |
|---|---|---|---|---|---|
| T-01 | Aralik ve yeniden egitim etkisi | "ranges from 4.4 to 19.4 points ... retraining ... moves it by under 1.5 points" | 01:23 "+4.4 to +19.4 ... moves the same quantity by under 1.5 points" | 06:45 "+4.4 to +19.4 ... that same quantity by under 1.5 points" | Uc yerde "under 1.5" SD'siz. Govde: 04:451, 05:13 "standard deviation of 0.23 to 1.27". 15.01 bir aralik (en buyuk eksi en kucuk protokol), 0.23-1.27 uc kosunun SD'si; q1/variance_ratio.json `aralik_protokol_bazli` kosular arasi aralik: ham 0.63, hedef-dogru 0.86, her-ikisi-dogru 0.46, basarili-kaynak 2.41 (2.41 > 1.5). |
| T-02 | 15.01 ayrisimi | "15.01-point spread has two parts: ... 9.21 ... 5.79" | 01:23 ayni iki sayi, 15.01 yok | 06:45 "That 15.01-point spread decomposes into 9.21 ... and 5.79" | tutarli; 9.21 + 5.79 = 15.00; metin 04:117 "rounded terms sum to 15.00" diyor |
| T-03 | 3.91 | "What survives is 3.91 points of discretion between the two protocols we endorse." | "3.91 points of discretion remain between two protocols that are both defensible, still more than twice the retraining effect" | "The 3.91 points of genuine discretion that survive the correction, between two defensible protocols, are the part a reporting standard has to address" | "endorse" (ozet, 04:117) / "defensible" (giris, sonuc); "genuine" yalniz sonuc; "more than twice" giris ve 04:117; 3.91 / 1.27 = 3.08, 3.91 / 2.41 = 1.62 |
| T-04 | Kimlik ifadesi | "an identity we derive removes 9.21 points in closed form"; "premise we measure rather than assume" | 01:25 "obeys an identity"; "to within 0.41 points"; "(0.989 to 1.000 over 36 directions)" | 06:45 "algebraically equal"; "holds to within 0.41 points across 36 measured directions"; "applies to any published raw rate whose targets satisfy the measured antecedent" | "we derive" (ozet, 01:23, 06:45) / "The algebra itself is not new" (04:145). 0.41 ve 36: ozette yok. "Antecedent" kosulu sonucta var, 05:41'de yok. |
| T-05 | Kimlik kapsami | - | "obeys an identity" | "any published raw rate whose targets satisfy the measured antecedent" | 04:143: antecedent yalniz hedefi AT-egitimli olan 36 yonde olculdu; 04:145: standart-egitimli hedeflerde p = 0.88 (karantina kaynakli), "there the identity is a bound" |
| T-06 | CIFAR-100 | "preserves the sign in all twelve measurements" | "leaves the spread close to its CIFAR-10 size and preserves its sign" | "The CIFAR-100 replication ... point the same way" | 13.83 (CIFAR-100) vs 15.01; kayitli ongorulerden biri dogrulandi, biri basarisiz, biri sinanamaz (04:206); bir uc nokta bandi kacirildi (04:208); bunlar ozet/giris/sonucta yok |
| T-07 | SVHN | 1.85; "two report a CNN advantage and two a ViT advantage, though the two we endorse agree" | "once they are matched, two of the four protocols reverse it" (SVHN adi gecmiyor) | "two of the four protocols reverse the sign and the primary protocol accepts equivalence" (1.85) | Ozet esdegerligi anmiyor; sonuc "endorse agree" cumlesini anmiyor; iki tohum, 50 epoch, AutoAttack yok (04:244) hicbirinde yok; her-ikisi-dogru farki -0.35 icin sign-flip p = 0.105 (04:240) |
| T-08 | Kontrol noktasi secimi | "adds a fourth, rarely reported, source of variance" | "turns out to be a source of variance that papers rarely report" | "measurement choices that papers rarely report are of the same order as the effects being reported" | rakamlar yalniz govde 04:455 (1.58-2.85 puan); sonuc "same order as the effects being reported": bkz. bolum 5, V-30 (CNN-ViT mutlak PGD-10 farki 11.42) |
| T-09 | Uc olumsuz sonuc | "Three further readings do not hold under direct measurement" | 01:27 uc madde, "in this regime" TGR icin | 06:49 uc madde | TGR "adaptation" 03:137, 04:421, 05:61'de, ozet/giris/sonucta yok. Mekansal sonuc: run-duzeyi anlamsizlik (n = 3), esdegerlik testi yok; dikkat entropisi: TOST kabul, ama yer degistirme 0.028 -> 0.084 artiyor |
| T-10 | "Survive" iddiasi | - | 01:27 "Gradient sparsity ... reproduce across independent checkpoint sets"; derinlik profili icin yeniden uretim iddiasi yok | 06:49 "Two behavioral differences did survive and reproduce across independent checkpoint sets: the gradient sparsity ordering ... and the depth profile" ; 05:31 ayni | 04:388: "On our earlier checkpoints the CNN profile fell monotonically to the last block, with no recovery, so the shape of the CNN curve ... should be read as recipe-dependent." 04:303: sparsity run-duzeyi Holm p = 0.108, "reproducible and not ... significant" |
| T-11 | Hedefin zayifligi | - | 01:25 "reframes the asymmetry as a property of the weaker target" | 06:45 "associates it with the target's own vulnerability (r = 0.986)" | 04:172 "can only be suggestive"; 05:21 "suggestive; establishing it would take a larger model pool"; uc hedef (biri harici WRN) |
| T-12 | Yonun kararliligi | "preserves the sign in all twelve" (CIFAR-100) | 01:23 "stable as long as the two models differ in clean accuracy" | 06:45 "stable across protocols, seeds, and attack families on both CIFAR datasets" | MI-FGSM yalniz CIFAR-10 (04:121, 05:21 "on CIFAR-10 also under MI-FGSM"); L2 yalniz CIFAR-10 (04:252, 04:269); CIFAR-100'de yalniz PGD-10 L_inf (tablo cifar100_results, 04:204) |
| T-13 | Mutlak dayaniklilik ayrisimi | - | 01:25 "factors exactly ... attribution ... changed between our earlier single-run checkpoints and three fresh runs" | 06:47 ayni | ozet yok; kanit "earlier" blok (FOY:33) |
| T-14 | Genellik/sinirlilik | baslik "decides the Conclusion"; sinirlilik cumlesi yok | 01:11 kisitsiz; 01:16 "setting is kept small so that the measurement question can be isolated" | 06:51 "three datasets and a single model pair ... remains to be calibrated; the mechanism ... not specific to our setting" | L_inf 8/255 tek tehdit modeli (05:59), tek mimari cifti (05:55), kucuk modeller (05:61) yalniz 05'te |
| T-15 | Raporlama gereksinimleri | "we close with reporting requirements" | 01:29 "collected at the end of the discussion" | 06:51 "first two matter most: state the conditioning protocol and prefer paired ones, and do not present unconditioned transfer rates as architecture comparisons" | gereksinimler 05:36-43'te (alti ogre: protokol bildir; esli protokol; ham oran yok; ayrisim; siralama vs mekanizma; agregasyon; dikkat icin ornek buyuklugu); makale Sinirlilik ve Gelecek Calisma (05:50-71) ile Sonuc'la kapaniyor |
| T-16 | Esdegerlik karari protokole bagli | - | 01:23 "also decides whether an equivalence test is accepted or rejected" | 06:45 "primary protocol accepts equivalence" (SVHN) | giris iddiasinin CIFAR-10'daki delili karantina kaynakli (04:117 son cumle); SVHN delili iki tohumlu |

## 3. Anahtar sozcuk taramasi

Tarama: `grep -n -i` ile `main.tex` ve alti bolum dosyasi, yorum satirlari haric.

### 3.1 "first"

| konum | baglam |
|---|---|
| 01:9 | "the direction measured in this paper is the opposite of the first group's" |
| 01:18 | "Only the last is a published claim; the first two are interpretations" |
| 01:23 | "Our first contribution is to quantify protocol sensitivity." |
| 02:76 | "Only the third is claimed in the cited work; the first two are interpretations" |
| 04:66 | "Our first checkpoints, selected with a validation split that clean pre-training had already seen" |
| 04:187 | "its commit precedes the first reported number, an epoch-5 pilot gate, by sixty-six minutes" |
| 04:208 | "predicted clean accuracy ... first" yok; (eslesme 04:208 "the first of the" degil; bkz. 05:17) |
| 04:388 | "the first three stages lose little, then the first block of the last residual stage collapses" |
| 04:392 | "from 0.028 total variation in the first layer" |
| 05:17 | "which is also the first of the two factors Demontis et al. identify" |
| 06:13 | "the first two are interpretations that our own earlier figures encouraged" |
| 06:15 | "of which the first two matter most" |

Oncelik iddiasi ("ilk kez") icerenler: yok. "Our first contribution" siralama anlamindadir.

### 3.2 "to our knowledge", "novel", "we prove"

Hicbiri metinde gecmiyor. En yakin: 02:74 "we know of no controlled estimate of how much the choice of conditioning set matters. We supply one" (C-40) ve 04:145 "What is new here is that in the transfer setting the premise is not definitional" (C-71).

### 3.3 "we show", "we derive", "derive"

| konum | metin |
|---|---|
| main.tex:89 | "We show that much of the disagreement comes from the measurement protocol." |
| main.tex:89 | "an identity we derive removes 9.21 points in closed form" |
| 01:23 | "removed in closed form by an identity we derive" |
| 06:45 | "9.21 points that an identity we derive removes in closed form" |

### 3.4 "identity" (ozdeslik)

| konum | metin (kisaltilmis) |
|---|---|
| main.tex:89 | "an identity we derive removes 9.21 points"; "The identity equates the deviation ... on a premise we measure rather than assume." |
| 01:25 | "the deviation of raw from conditioned rates obeys an identity" |
| 01:31 | "the algebraic identity of Section 4" |
| 02:74 | "takes the form of an identity" |
| 04:113 | "the closed-form term of Equation (eq:raw_identity)" |
| 04:117 | "Equation (eq:raw_identity) predicts in closed form" |
| 04:117 | "the whole 13.58-point spread there is the identity term" |
| 04:135 | "it is an identity resting on a single empirical fact" |
| 04:143 | "Equation (eq:raw_identity) consequently reproduces every measured unconditioned rate to within 0.41 points" |
| 04:145 | "it is an upper bound and not an equality once the antecedent fails"; "there the identity is a bound"; "The algebra itself is not new" |
| 04:147 | "it should be re-estimated whenever the identity is applied to other model pools" |
| 04:240 | "the identity says in advance when it will" |
| 04:269 | "cannot fail once Equation (eq:raw_identity) holds"; "before the identity was written down and now serves as an out-of-sample check on it" |
| 04:271 | "the identity predicts a steeper slope" |
| 05:19 | "algebraically equal to the target's clean error scaled by (1 - r_cond)" |
| 05:41 | "since that relation is an algebraic identity, the correction can be applied to published raw rates without re-running anything" |
| 06:45 | "algebraically equal"; "an identity that holds to within 0.41 points" |
| 03:111 | "robust = clean x conditioned survival" "factorizes exactly" (ikinci, tanimsal esitlik) |

### 3.5 "closed form", "exactly", "by construction", "essentially"

| konum | metin |
|---|---|
| main.tex:89 | "in closed form" |
| 01:23, 04:113, 04:117, 06:45 | "closed form" |
| 01:25 | "essentially never rescued by the perturbation (0.989 to 1.000 over 36 directions)"; "factors exactly" |
| 04:117 | "a reader given the target's clean error can remove it exactly" |
| 04:145 | "contaminated by target weakness by construction" |
| 04:269 | "cannot fail"; "rises with e by construction" |
| 04:119 | "the other three protocols are unchanged by construction" |

## 4. Ozetteki her sayi ve govdedeki ilk gecisi

| ozet ifadesi | ilk govde konumu | govde degeri | kaynak (dosya) | uyum |
|---|---|---|---|---|
| "ResNet-18 and ViT-Tiny" | 01:16 | | | |
| "three runs each" | 01:16 ("three independent training runs per architecture") | 3 (CIFAR-10, CIFAR-100); SVHN 2 (04:224, 04:244) | q1/e7_svhn_summary.json n_tohum = 2 | CIFAR icin uyumlu |
| "validation split held out before training" | 01:16 | 2,000 ornek, tohum 777 (03:100) | | |
| "four conditioning protocols" | 01:11 (dort ornek kumesi), 03:118 | ham + hedef-dogru + her-ikisi-dogru + basarili-kaynak | FOY:53-56 | ham = kosulsuz |
| "4.4 ... 19.4 points" | 01:23 (+4.4, +19.4); kesin deger 04:97, 04:99 (+4.36, +19.37) | 4.36; 19.37 | FOY:54, 56 | uyumlu |
| "CIFAR-10" | 01:16 | | | |
| "under 1.5 points" | 01:23; 04:117 ("below 1.5"); 04:451 | SD 0.23-1.27 | FOY:53-56 (+/-0.33, 0.44, 0.23, 1.27) | SD; bkz. T-01 |
| "15.01-point spread" | 04:113 (sekil altyazisi); 04:117 | 15.01 +/- 0.84 | FOY:60; q1/fig_protokol_kumeleri_veri.json `yayilim` 15.01 | uyumlu; giriste yok |
| "9.21 points" | 01:23 | 9.21 | q1 JSON `ozdeslik_terimi_ham_eksi_hedef_dogru` 9.21; 13.57 - 4.36 = 9.21 | uyumlu |
| "5.79 points" | 01:23 | 5.79 | q1 JSON `farkli_estimand_bas_kaynak_eksi_ham` 5.79; 19.37 - 13.57 = 5.80 | 0.01 yuvarlama; metin 04:117 aciklar |
| "3.91 points" | 01:23 | 3.91 | q1 JSON `artik_takdir_her_ikisi_eksi_hedef` 3.91; 8.27 - 4.36 | uyumlu |
| "deviation ... target's clean error scaled by one minus the conditioned rate" | 04:139 (Denklem) | r_raw - r_cond = e (1 - r_cond) | q1/ozdeslik_kontrol.json | tahmin 9.196 vs olculen 9.21 |
| "CIFAR-100" | 01:23 | | | |
| "twelve measurements" | 04:204 | 4 protokol x 3 tohum | q1/cifar100/transfer/e1_transfer_summary.json; en kucuk deger +3.97 (CIFAR-10 hedef-dogru tohum 3), CIFAR-100 en kucuk tohum +4.21 | hepsi pozitif |
| "SVHN" | 01:31 (veri kumesi ekleme), 04:217 | | | |
| "1.85 points apart in clean accuracy" | 04:220 | 94.27 - 92.42 = 1.85 | q1/e7_svhn_summary.json (94.27, 92.42) | uyumlu |
| "two report a CNN advantage and two a ViT advantage" | 04:240 | +0.39, +2.70 / -1.00, -0.35 | q1/svhn/transfer/e7_transfer_summary.json (ham 0.39, hedef-dogru -1.005, her-ikisi -0.35, basarili 2.695) | uyumlu |
| "the two we endorse agree" | 04:240 | hedef-dogru -1.00, her-ikisi-dogru -0.35 (ikisi de ViT lehine) | ayni | her-ikisi-dogru farki sign-flip p = 0.105, GA [-0.76, +0.07] (04:240) |
| "fourth ... source of variance" | 03:156 | | | |
| "Three further readings" | 01:18 | | | |

## 5. Dogrulama kayitlari (metin sayisi - artefakt)

Yontem: FOY ve `results/q1/*`, `results/c1_*` JSON'lari; hesaplar `raporlar/hakem_lecun_2026-10-04/_tmp/a1_*.py`. "eslesti" = metin ile artefakt degeri ayni (yuvarlama icinde).

| id | madde | metin | artefakt | durum |
|---|---|---|---|---|
| V-01 | Tablo main_results (6 satir, 24 hucre) | 04:26-32 | FOY:14-19 | eslesti |
| V-02 | Tablo conditional (kosullu ayrisma) | 04:54-59 | FOY:28-29, 33 | eslesti |
| V-03 | Tablo transfer_protocols, fark sutunu | 04:96-99 | FOY:53-56, q1/fig_protokol_kumeleri_veri.json | eslesti; son sutun (8.27, 0.63, 5.33, 11.17) FOY'da "run3 fark" |
| V-04 | Tohum bazli fark degerleri | (metinde yok) | fig_protokol JSON: ham [13.2, 13.69, 13.83]; hedef-dogru [4.83, 4.28, 3.97]; her-ikisi [8.51, 8.05, 8.24]; basarili [20.8, 18.91, 18.39] | tohum bazli aralik: 15.97, 14.63, 14.42 (ort 15.007) |
| V-05 | N'ler: 10,000/10,000; 7,353/8,579; 7,061; 2,831/3,814 | 04:117 | FOY:53-56 | eslesti |
| V-06 | Tablo transfer_matrix (9 satir) | 04:159-167 | FOY:69-77 | eslesti (WRN-WRN +/-0.00 FOY'da, metinde sd yok) |
| V-07 | r = 0.986; gelen transfer 18.50, 19.04, 10.57 | 04:172 | FOY:81 ([18.5, 19.04, 10.57]) | eslesti |
| V-08 | r = 0.997, egim 0.762 | 04:145, 04:147 | FOY:79; c3_precision.json (0.762, 0.656) | eslesti |
| V-09 | CIFAR-100 tablo (63.86, 19.30, 15.04; 43.17, 11.15, 8.87) | 04:198-199 | q1/e1_cifar100_summary.json | eslesti |
| V-10 | CIFAR-100 asimetriler +4.96, +18.53, +10.92, +17.50; yayilim 13.83 +/- 1.30 | 04:204 | e1_transfer_summary.json (4.957, 18.533, 10.923, 17.5; yayilim 13.827, sd 1.297) | eslesti |
| V-11 | CIFAR-100 13.58 | 04:117 | aralik-ortalamalari 18.533 - 4.957 = 13.576 | eslesti |
| V-12 | Kimlik tahmini: ViT hata 26.47, CNN 14.22; tahmin edilen fark | (04:117) | tablo degerlerinden: tahmin (ham-hedef) farki 9.196; olculen 9.21; her yon: tahmin 21.21 / 12.01, olculen 21.15 / 11.94 | fark 0.014 |
| V-13 | p araligi 0.989-1.000, 36 yon, artik <= 0.41, ort 0.095, <= %1.39 | 04:143 | ozdeslik_kontrol.json | eslesti (ort p = 0.9973) |
| V-14 | SVHN: 94.27 +/- 0.70, 92.42 +/- 0.56; PGD 55.52 +/- 0.64, 52.30 +/- 0.10 | 04:220 | e7_svhn_summary.json | eslesti |
| V-15 | SVHN tablo | 04:232-235 | e7_transfer_summary.json (-1.005 -> -1.00; -0.35; 2.695 -> 2.70; 0.39) | eslesti; artik 0.655 (metin 0.65) |
| V-16 | SVHN yayilim 3.70 +/- 0.62 | 04:242 | protocol_spread_pp 3.7, sd 0.622 | eslesti |
| V-17 | L2 asimetriler +13.03, +2.12, +4.07, +12.06; yayilim 10.92 | 04:269 | e6_l2_transfer_summary.json (13.027, 2.12, 4.067, 12.057; yayilim ort 10.917, aralik-ort 10.907) | eslesti |
| V-18 | CIFAR-100 ve L2 on kayitta "twelve" pozitif | 04:204, 04:269 | en kucuk degerler: CIFAR-100 +4.21; L2 +1.91 | hepsi pozitif |
| V-19 | Gradyan tablosu | 04:291-295 | FOY:90-93, 100 | eslesti; ViT-native sutunu (0.405, 0.571, 17.9, 0.079) FOY'da yok |
| V-20 | Kosu-duzeyi p: Gini 0.036, rel 0.042, Hoyer 0.067, Holm 0.108, hizalanma 0.0009 | 04:303 | c1_behavior_summary.json `diff_R_minus_V` ile 1-ornek t: 0.0359, 0.0420, 0.0674; Holm 0.108; 0.0009 | eslesti (yeniden hesap) |
| V-21 | Mekansal tablo ortalamalari ve p (0.54, 0.40, 0.54, 0.47) | 04:325-328 | FOY:123-126; c1_c5/pair*/c5_spatial.json uzerinden 1-ornek t + Holm: 0.535, 0.402, 0.535, 0.467 | eslesti (yeniden hesap) |
| V-22 | Ozellik kaymasi tablosu; CLS min 0.9604 @11, yama 0.9870 @9, oran 3.05; norm <= %0.45 | 04:372-383, 04:388-390 | c1_c4/pair{1,2,3}/c4_summary.json: `cos_block_cls` min 0.9604 @11; `cos_block_token_mean` 0.9870 @9; oran 3.054; norm max 0.437 | eslesti |
| V-23 | MLP alt blok: 0.9343 @10, 0.9840 @8; oran 4.12 | 04:390 | FOY:108-109; (1-0.9343)/(1-0.9840) = 4.106 | oran yuvarlanmis degerlerle 4.11, metin 4.12 |
| V-24 | ResNet layer4.0 0.8777 +/- 0.0181, -13.14 +/- 1.89; layer4.1 0.9108, +5.84 | 04:388 | FOY:112 | eslesti |
| V-25 | Dikkat entropisi <= 0.005; yer degistirme 0.028 -> 0.084; devrilen 0.9895 / 0.9877 | 04:392, 04:394 | FOY:113-115 (<= 0.0045; 0.0276 -> 0.0841) | eslesti |
| V-26 | TGR tablosu; 14.9, 3.0, 2.2; McNemar p | 04:432-439 | FOY:137-141; fark 14.87, 3.01, 2.15 | eslesti |
| V-27 | MI-FGSM 19.07 +/- 0.33 / 15.42 +/- 0.52 | 04:121 | c1_behavior_summary.json (19.0741 +/- 0.3292; 15.4209 +/- 0.5225) | eslesti |
| V-28 | Yayilim/kosum oranlari: 5.2-32.6; 28.3; chi2 GA 0.8-9.9 | 04:453 | variance_ratio.json (5.16-32.62; 28.29; [0.82, 9.9]) | eslesti |
| V-29 | Secim yayilimi: 2.62-2.85 (ResNet), 1.58-2.09 (ViT), 1.09x, 1.42x | 04:455 | q1/e2/e2_grid.json | eslesti |
| V-30 | CIFAR-100 9-hucre 0.18-1.83 (ort 0.86); CIFAR-10 0.54-2.83 | 04:212 | q1/b8_secim_bandi.json (0.18-1.83, ort 0.858; 0.54-2.83, ort 1.754) | eslesti |
| V-31 | Egimler: -0.528 [-0.664, -0.418]; +0.431 [0.333, 0.633]; +0.673 [0.602, 0.727]; +0.273 [0.219, 0.371]; 0.201-0.492; 0.661-0.673; B-ana-cift -0.100 [-0.464, +0.092]; 116 nokta / 8 kume; 18 cift / 6 kume; 23.77 ort aciklik; basarili-kaynak 16/18 uc | 04:123, 04:127 | e3_surucu_ayristirma.json; e3_iki_kol_fit.json | eslesti |
| V-32 | SVHN-dahil dort-protokol egimi -0.133 [-0.570, +0.469]; n_cift 20, n_kume 8 | 04:123 | e3_asimetri_fit_svhnli.json | eslesti |
| V-33 | SVHN-dahil uc-protokol egimi +0.470 [+0.361, +0.665] | 04:123, 04:127 | JSON'larda yok; metin yalniz scripts/_t3_en_kisalt6.py icinde | bulunamadi |
| V-34 | AA - PGD-10 dususu 6.2, 3.6; 12.3 puan temiz fark; 37.93 = 85.78 x 0.442 | 04:41, 04:64 | hesap: 6.18, 3.55, 12.25; 85.78 x (1 - 0.5578) = 37.93 | eslesti |
| V-35 | Ozet kelime sayisi | main.tex:89 | `wc -w` = 248 | 248 sozcuk |
| V-36 | GitHub adresi | main.tex:118 | `curl` 2026-10-04: HTTP 404; `teslim/acik_depo/cnn-vit-robustness-protocols` icinde `git remote -v` bos, tek commit `a8b138c` | adres henuz cozulmuyor |
| V-37 | `ali2024adversarial` dergisi | 02:72 "in this journal" | references.bib:356-363 `journal = {IEEE Access}` | uyumlu |

## 6. Bulunamayan, aciklanamayan ya da yalniz bir tarafi dogrulanabilen kalemler

| id | kalem | konum | ne arandi | sonuc |
|---|---|---|---|---|
| N-01 | SVHN-dahil uc-protokol egim +0.470, GA [+0.361, +0.665] | 04:123, 04:127 | `results/q1/e3_*.json`, `scripts`, `raporlar` icinde grep (0.470, 0.361, 0.665, 0.4698) | yalniz `scripts/_t3_en_kisalt6.py:40-48` (metin degisikligi betigi); sonuc JSON'unda yok. Karsilastirma: e3_surucu_ayristirma.json uc-protokol +0.4314 (18 cift, SVHN'siz); e3_fit_Bkolu.json SVHN-dahil uc-protokol icermiyor |
| N-02 | ViT temiz-egitim 77.50 (erken kontrol noktasi) | 04:66 | FOY, `results/c1_*.json`, `q1/*.json` grep | bulunamadi (karantina kaynakli olabilir) |
| N-03 | "p as low as 0.88" | 04:145 | ayni | bulunamadi; metin "pre-correction runs" diyor |
| N-04 | "ViT retained 0.885 of its clean pre-training accuracy ... against 0.802 for the ResNet" | 04:208 | `q1/*.json`, `q1/cifar100/*.md` | bulunamadi |
| N-05 | ViT-native gradyan sutunu (0.405, 0.571, 17.9%, 0.079) | tablo gradient | FOY, c1_behavior_summary.json | FOY'da yok; `results/c_addenda/clean_gradient_stats.json` icinde 0.405 oruntusu var ama tabloyla eslesmesi dogrulanmadi |
| N-06 | "widest in 13 of the 18 directions" | 04:123 | e3_surucu_ayristirma.json | `protokol_uc_olma_sayilari` max ve min sayilari var (basarili-kaynak 4 en buyuk, 12 en kucuk, yani 16 uc); "13" dogrudan yok |
| N-07 | Parcali alt-kume kirilganlik (41.2, 59.1, 10.0, 18.3; 1,517 +/- 102; 291 +/- 16) | 04:123 | aranmadi | dogrulanmadi |
| N-08 | Penultimate geometri (87.3 -> 51.3, silhouette 0.196 -> -0.032 vb.) | 04:413 | FOY'da yok | dogrulanmadi |
| N-09 | Sinif bilesimi ayrisimi (-1.249, -1.330, -1.065; +0.527, +0.435, +0.382) | 04:210 | `q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json` mevcut | acilmadi |
| N-10 | 21.7 GPU saat | 04:459 | `results/q1/KOKEN.json` `calisma_zamani` olasi | acilmadi |
| N-11 | Ham-hedef-dogru 9.21 sayisi, 3x3 matristeki ResNet18 -> WRN satirinin ham-kosullu farki ile ayni (FOY:71, +9.21) | (tesaduf) | FOY:71 | iki ayri nicelik ayni degeri veriyor (CIFAR-10: ham-hedef-dogru asimetri farki 13.57 - 4.36 = 9.21; 3x3 satiri 21.69 - 12.48 = 9.21) |
| N-12 | Belgelenmis literatur taramasi ("we know of no controlled estimate"; "scarce") | 02:54, 02:74 | `raporlar/` ve `paper/review/` dosya adlari; grep | bu toplama kapsaminda tarama kaydi bulunamadi; `raporlar/hakem_lecun_2026-10-04/toplama_C1_positioning-extract.md` ayri toplayicinindir |
| N-13 | Kayit oncesi dosyalari (pre-registration commit zamani, 66 dk) | 04:187 | bakilmadi | dogrulanmadi |

## 7. Ek notlar (olgu, yorumsuz)

- Intro 01:23 ve ozet "retraining both architectures from scratch": 03:100'de bir kosu = temiz on-egitim + cekismeli ince ayar, uc kosu, ayni dogrulama bolmesi (04:453: "all three runs share one validation split").
- Sonuc 06:45 ve 05:19: hedef-dogru protokol hem "endorse" edilenlerden biri (ABS, 04:117) hem de "pulls two directions toward each other" (05:19).
- 04:123 ve 04:127: dort-protokol egimi metinde geri cekiliyor ("We therefore withdraw the four-protocol slope"); 05:55 hala "the successful-source protocol adds a second driver ... strong enough to reverse the overall relationship" diyor.
- 04:206: kayitli ongoru 2 icin esik "10.45", bu sayi ayni zamanda 04:119'daki gevsek-okuma yayilimidir (15.01 -> 10.45).
- 04:187: kayit "does not precede the start of training"; ilk raporlanan sayidan 66 dakika once.
- `references.bib`: 64 giris; `sahin2026behavioral` "Preliminary version of the present study; submitted" (satir 626-632); `zhao2025revisiting` anahtari 2025, `year = {2026}` (satir 470-478).
- Karantina etiketli sayilarin yeri: tablo conditional alt blok (04:57-59), tablo transfer_protocols son sutun (04:88, 94, 96-99, 101), 04:66, 04:117 (son cumle), 04:145 (p = 0.88), 04:305, 04:388 (son cumle), 01:25, 05:23, 06:47; FOY bu karsilastirma sayilarini "run3 fark" (FOY:51-56) ve "Eski tek kosu (sizintili)" (FOY:33) olarak kendisi tasiyor.
