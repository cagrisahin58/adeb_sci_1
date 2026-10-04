# Toplama E1: yapi ve yazim kanit dosyasi (lens E)

Kaynak: /home/firat/projects/adeb_sci_1/paper/manuscript/{main.tex, sections/01..06}. Betikler: raporlar/hakem_lecun_2026-10-04/_tmp/e1_metrics.py, e1_refs.py, e1_lim.py, e1_hedge.py, pg.py. Hicbir makale, veri ya da betik dosyasi degistirilmedi. Sayi kaynagi karantina kuralina gore C1 referans foyudur; bu dosya yalnizca metnin yapisini olcer, sayi dogrulamaz.

## Ozet (10 satir)
1. Alti bolum dosyasi icin kelime, paragraf, en uzun paragraf, 45 kelimeyi asan cumle, \paragraph, This/That/Yet/Only baslangici, "rather than"/"instead of", noktalivirgul, parantez ve vurgu sayimlari betikle hesaplandi (Tablo A).
2. Duz metin (tablo/sekil/ekran denklemi haric) toplam 14 712 kelime; ozet 248 kelime. Deneyler bolumu 7 339 kelime ile toplamin yuzde 49,9'u.
3. Ozet, giris ve sonuc arasinda 7 yakin-ayni cumle cifti (3 icerik kumesi) bulundu; giris 23. satir ile sonuc 9. satir arasinda Jaccard 0,71 (Tablo C).
4. Tartisma "Reporting Requirements" alt bolumu (05_discussion.tex:36-45) sekiz gereklilik ve bir uygulayici paragrafi iceriyor; numarasiz duz yazi; tamami asagida aynen (Tablo D).
5. Giris 29. satir gereklilikleri "tartismanin sonunda toplandi" diyor; oysa alt bolum 5.2'dir, ardindan 5.3 Limitations ve 5.4 Future Directions gelir (Tablo D notu).
6. Desen taramasi 44 sinirlilik cumlesi verdi (e1_lim.py); Tablo E bunlarin ve elle eklenenlerin aynen listesidir; Limitations alt bolumu 05_discussion.tex:50-61, dort paragraf.
7. Ileri atiflar: 21 Section~\ref ileri atif hedefi (e1_refs.py), giris roadmap'i (5) haric 16 (Tablo F); ayrica 11 tablo/sekil/denklem sunumdan once atiflanmis.
8. Sayfa butcesi (24 sayfa): giris 1-2, ilgili calisma 2-4, yontem 4-8, deneyler 8-19, tartisma 19-21, sonuc 21-22, kaynakca 22-24 (Tablo G).
9. Makine uretimi/asiri temkinli kayit icin 12 aynen alinti ve konumlari; asiri iddia/temkinli cift olarak 8 cift (Tablo H, I).
10. Bulunamayanlar: pdftotext yok (PDF metni docker icindeki PyMuPDF ile okundu); "Appendix" yok (ek bolumu bulunmuyor); cumle bolme sezgiseldir (+-%5 sapma); wc ile betik arasi kelime farki Tablo A basliginda aciklandi.

## Tablo A. Bolum olcumleri (e1_metrics.py)
Kelime: LaTeX komutlari, atiflar, $...$ ve tablo/sekil/denklem ortamlari cikarilmis duz yazi. Cumle bolme sezgisel (e1_metrics.py:sentences). Matematik $...$ "M" olarak sayildigi icin kelime sayisina 1 kelime olarak girer.

| bolum dosyasi | kelime | paragraf | en uzun paragraf (kelime, baslangic satiri) | cumle | 45 k. ustu cumle | \paragraph | This / That / Yet / Only | rather than | instead of | ; / 100 cumle | parantez | textbf / emph / textit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01_introduction | 1034 | 11 | 187, satir 23 | 39 | 4 | 0 | 0 / 1 / 1 / 1 | 0 | 0 | 10,3 (4 adet) | 5 | 0 / 3 / 0 |
| 02_related_work | 1354 | 14 | 259, satir 62 | 47 | 7 | 0 | 0 / 1 / 0 / 1 | 0 | 0 | 23,4 (11) | 7 | 0 / 2 / 0 |
| 03_methodology | 2448 | 27 | 365, satir 113 | 94 | 11 | 17 | 1 / 1 / 0 / 1 | 3 | 4 | 11,7 (11) | 39 | 3 / 10 / 0 |
| 04_experiments | 7339 | 54 | 462, satir 117 | 269 | 29 | 0 | 5 / 3 / 0 / 0 | 5 | 8 | 17,5 (47) | 80 | 77 / 28 / 3 |
| 05_discussion | 2014 | 21 | 177, satir 55 | 77 | 6 | 0 | 0 / 2 / 0 / 0 | 2 | 0 | 9,1 (7) | 10 | 0 / 3 / 0 |
| 06_conclusion | 523 | 5 | 257, satir 9 | 15 | 2 | 0 | 0 / 1 / 0 / 1 | 0 | 0 | 13,3 (2) | 0 | 0 / 0 / 0 |
| toplam | 14712 | 132 | | 541 | 59 | 17 | 6 / 9 / 1 / 4 | 10 | 12 | | 141 | 80 / 46 / 3 |

Notlar. textbf sayisinin 77'si deneyler tablolari icindedir (hucre kalini); duz yazi vurgusu emph ile yapilmis. Ozet: 248 kelime, 11 cumle (main.tex:88-90). Ikinci kelime sayimi (e1_hedge.py; tablo hucreleri dahil, tum kelime benzeri belirtece bakar) bolum kelimelerini 1032 / 1439 / 2694 / 8835 / 2029 / 511 verir; fark tablo icerigindendir. Metin yapisi: deneyler bolumu 11 alt bolum ve 3 alt-alt bolum (04_experiments.tex:10, 81, 132, 184, 217, 249, 276, 310, 356, 418, 446), \paragraph basliklari yalniz yontem bolumunde (03_methodology.tex:42-139, 17 adet).

### A.1 Her bolumde 45 kelimeyi asan en uzun uc cumle (aynen, \cite ve $ matematik "M" olarak soyulmus)
01_introduction:
- (58 k., 27. satir paragrafi) "Three of the results we report are negative: scale-invariant sparsity differences do not correspond to spatial localization differences, on all four spatial measures; CLS attention entropy does not change measurably under attack at M; and Token Gradient Regularization , a ViT-specific transfer attack, gives no transfer gain in this regime, losing to plain MI-FGSM under a matched budget."
- (58 k., 9. satir) "Transfer studies add a disagreement of their own: several report that attacks move more easily from ViTs to CNNs than the reverse , whereas Naseer et al. find that perturbations crafted on ViTs transfer poorly under conventional attacks, and the direction measured in this paper is the opposite of the first group's, a point Section X returns to."
- (54 k., 31. satir) "The present paper adds two further datasets, a second threat model, the algebraic identity of Section X, the checkpoint-selection ablation, the transformer-specific transfer attack, and the pre-registered analysis protocol, and it corrects one claim of the earlier version: the direction of the asymmetry is not stable once the architectures are matched in clean accuracy."

02_related_work:
- (80 k., 62. satir) "Two recent benchmarks move in the same direction: TA-Bench standardizes the comparison of more than thirty transfer attacks over a common pool of substitute and victim models, and Yu et al. report that transferability is systematically overestimated when it is measured across a single architecture family, and propose three evaluation protocols that differ in how a multi-target outcome is scored: treating an ensemble as a single target, counting how many targets are fooled, and requiring that all of them are."
- (75 k., 54. satir) "More recently, Jain et al. traced a form of gradient masking in ViTs to softmax underflow in attention, which leaves PGD-style attacks sub-optimal on them, a caveat for PGD-only ViT evaluations that AutoAttack, with its gradient-free Square component, partly guards against; the adversarial-training recipe they build on the corrected attack improves on existing ViT recipes on CIFAR-10 and ImageNet-100; with diffusion-augmented adversarial training, ViTs have even been reported to surpass WideResNets on small-scale datasets ."
- (58 k., 64. satir) "Mahmood et al. measured transfer between CNNs and ViTs with a both-correct protocol and found notably low CNNMViT transferability; Naseer et al. showed that adversarial examples crafted on ViTs transfer poorly under conventional attacks and proposed self-ensemble and token refinement to improve ViT-sourced transferability, and Wei et al. improved ViT-sourced transfer by bypassing attention gradients and patch-wise dropout."

03_methodology:
- (90 k., 113. satir) "Given adversarial examples M generated against source model M, the conditioned transfer rate to target model M is: Conditioning transfer evaluation on correctly classified samples is established practice, usually on the samples that every model in the study classifies correctly ; the target-correct rate is the one-sided relaxation of that pool, and conditioning matters most in cross-architecture comparisons: the raw misclassification rate M includes the target's clean error, so a target with lower clean accuracy appears more ``vulnerable'' to transfer even when no additional samples are flipped by the attack." (betik, denklemden onceki ve sonraki metni birlestirmis; cumle sinirinda yapay birlesme)
- (64 k., 120. satir) "Gradient alignment measures the average pairwise absolute cosine similarity across samples (computed over all pairs of the 500 analysis samples): We use the absolute cosine because shared sensitivity axes matter for attack geometry regardless of sign; since sign coherence is what universal-perturbation arguments additionally require, we also report the signed mean cosine, which turns out to be near zero for every model (Section X)."
- (58 k., 113. satir) "The successful-source rate is the transferability metric of Ravikumar et al. , whose Equation (1) divides the number of examples that transfer to the target by the number generated against the source, over a pool restricted to samples both models classify correctly; it is also the protocol implied whenever a transfer rate is reported over ``successful'' adversarial examples."

04_experiments:
- (77 k., 121. satir) "What is stable is the direction: CNN-crafted examples transfer better to the ViT than the reverse under all four protocols, in all three seeds, and also under the momentum-based MI-FGSM (M versus M target-correct; this bidirectional check uses the attack's own default step of M, not the M used elsewhere, which is why its ViTMCNN figure differs slightly from the matched-budget value in Table X), so the effect is not an artifact of the PGD attack itself."
- (62 k., 123. satir) "The successful-source protocol is driven differently, and separating the two drivers changes what the spread depends on: across M direction pairs drawn from six seed-and-dataset clusters, the spread of the four-protocol asymmetry falls as the clean-error gap between the two models widens (slope M, cluster-bootstrap CI M), whereas the spread computed without the successful-source protocol rises with it (slope M, CI M)."
- (61 k., 455. satir) "Smoothing the validation curve before the argmax lowers test PGD-10 accuracy monotonically in every ResNet run and in two of the three ViT runs, so it is a systematically worse rule; restricted to the split and patience choices that studies actually vary, the dispersion falls to M times the seed-level standard deviation for the ResNet and M times for the ViT."

05_discussion:
- (59 k., 71. satir) "The leakage ablation, on six full-budget trajectories, did not detect an effect of leakage on checkpoint selection, but it answers a weaker question than the one posed: the treatment was applied to a single validation split, so split identity and leakage are not separable within that design, and what it does yield is the selection-protocol dispersion of Section X."
- (54 k., 17. satir) "Our mechanism is compatible with those results: we attribute the asymmetry to the target's own vulnerability rather than to any special strength of CNN-crafted perturbations, which is also the first of the two factors Demontis et al. identify, and the weaker target in Mahmood et al.'s pair is not the weaker target in ours."
- (50 k., 25. satir) "Sparsity is not spatial locality: adversarially trained CNN gradients concentrate more mass on fewer components (Hoyer M versus M, consistent in every run; per-sample M, run-level M after correction), but four spatial descriptors of the same gradients show no corresponding difference in how those components are arranged in the image."

06_conclusion:
- (68 k., 9. satir) "Unconditioned rates are not a valid basis for such a comparison at all: in a M matrix that adds a WideResNet-28-10 reference, their deviation from conditioned rates is algebraically equal to the target's clean error scaled by one minus the conditioned rate, an identity that holds to within M points across M measured directions and that applies to any published raw rate whose targets satisfy the measured antecedent."
- (49 k., 9. satir) "The direction is stable across protocols, seeds, and attack families on both CIFAR datasets, but not across datasets: on SVHN, where the same recipe leaves the two architectures only M points apart in clean accuracy, two of the four protocols reverse the sign and the primary protocol accepts equivalence."

Not: 04_experiments.tex:117 (462 kelimelik paragraf, tek satirda) ve 04_experiments.tex:123 ile 125, 127 satirlari deneyler bolumunde birbirini izleyen uc yogun paragraf (sirasiyla 462, ve diger iki uzun paragraf). Yontem bolumunun 365 kelimelik paragrafi 113. satir (Transfer Attack Metrics, \paragraph satir 113 sonrasi).

### A.2 Temkin ve vurgu yogunlugu (e1_hedge.py; tum kelime benzeri belirtec, tablo hucreleri dahil)
Temkin sozcukleri: may, might, could, suggest*, appear*, seems, likely, partly, roughly, approximately, largely, preliminary, plausible, compatible, "consistent with", "at most", about, here, "in this regime". Vurgu: entirely, exactly, algebraic*, "closed form", dominates, "at all", never, always, every, "all four/three/twelve", any, stable, survive*, essentially, clearly.

| bolum | kelime | temkin (1000 k.'da) | vurgu (1000 k.'da) | not X but Y | neither | in other words | turns out | genuine | defensible | rarely | cannot | does/do/did not | finally, | thus/therefore/hence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 1032 | 4 (3,9) | 10 (9,7) | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 0 | 4 | 0 | 0 |
| 02 | 1439 | 4 (2,8) | 1 (0,7) | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| 03 | 2694 | 3 (1,1) | 19 (7,1) | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 04 | 8835 | 36 (4,1) | 68 (7,7) | 0 | 2 | 0 | 1 | 0 | 0 | 1 | 5 | 30 | 0 | 18 |
| 05 | 2029 | 11 (5,4) | 14 (6,9) | 3 | 0 | 0 | 0 | 0 | 1 | 0 | 4 | 9 | 2 | 5 |
| 06 | 511 | 1 (2,0) | 9 (17,6) | 1 | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 3 | 0 | 0 |

Sonuc bolumunde vurgu sozcugu yogunlugu 17,6/1000, tartisma 6,9, deneyler 7,7.

## Tablo B. Ozet cumleleri (main.tex:88-90), numarali
1 "Comparisons of adversarial robustness across architecture families reach conflicting conclusions, usually attributed to models, training recipes, or datasets."
2 "We show that much of the disagreement comes from the measurement protocol."
3 "On adversarially trained ResNet-18 and ViT-Tiny pairs, three runs each, with full-test-set per-sample logging and a validation split held out before training, we fix models, data, threat model and attack budget and vary only how transfer is scored."
4 "Across four conditioning protocols the measured CNN-to-ViT transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10, whereas retraining both architectures moves it by under 1.5 points."
5 "The 15.01-point spread has two parts: an identity we derive removes 9.21 points in closed form, and 5.79 points come from a protocol that estimates a different quantity."
6 "What survives is 3.91 points of discretion between the two protocols we endorse."
7 "The identity equates the deviation of unconditioned from conditioned rates with the target's clean error scaled by one minus the conditioned rate, on a premise we measure rather than assume."
8 "Replicating on CIFAR-100 preserves the sign in all twelve measurements."
9 "On SVHN, where the same recipe leaves the architectures 1.85 points apart in clean accuracy, the protocol decides the sign as well as the size: two report a CNN advantage and two a ViT advantage, though the two we endorse agree."
10 "Varying only the checkpoint-selection rule adds a fourth, rarely reported, source of variance."
11 "Three further readings do not hold under direct measurement; we close with reporting requirements for cross-architecture robustness studies."

## Tablo C. Ozet / giris / sonuc arasinda (yakin-)ayni cumleler (e1_metrics.py, Jaccard >= 0,45 belirtec kumesi; LaTeX matematigi "M")
Cift 1 (ozet cumle 4, giris 23. satir, sonuc 9. satir; ozet-giris 0,58; giris-sonuc 0,71; ozet-sonuc 0,48):
- Ozet (main.tex:88-90): "Across four conditioning protocols the measured CNN-to-ViT transfer asymmetry ranges from 4.4 to 19.4 points on CIFAR-10, whereas retraining both architectures moves it by under 1.5 points."
- Giris (01_introduction.tex:23): "On identical models and data, the measured cross-architecture transfer asymmetry ranges from $+4.4$ to $+19.4$ points across four conditioning protocols, whereas retraining both architectures from scratch moves the same quantity by under $1.5$ points."
- Sonuc (06_conclusion.tex:9): "The measurement dominates: on identical adversarially trained ResNet-18 and ViT-Tiny pairs, the cross-architecture transfer asymmetry ranges from $+4.4$ to $+19.4$ points across four conditioning protocols, whereas retraining both architectures from scratch moves that same quantity by under $1.5$ points."

Cift 2 (ozet cumle 5, giris 23, sonuc 9; 0,53 / 0,53 / 0,53):
- Ozet: "The 15.01-point spread has two parts: an identity we derive removes 9.21 points in closed form, and 5.79 points come from a protocol that estimates a different quantity."
- Giris (01_introduction.tex:23): "The $9.21$ points that separate the unconditioned estimate from the target-correct estimate are removed in closed form by an identity we derive, and $5.79$ points come from a protocol that estimates a different quantity."
- Sonuc (06_conclusion.tex:9): "That $15.01$-point spread decomposes into $9.21$ points that an identity we derive removes in closed form and $5.79$ points contributed by a protocol that estimates a different quantity."

Cift 3 (giris 18. satir / sonuc 13. satir; 0,54):
- Giris (01_introduction.tex:18): "Only the last is a published claim; the first two are interpretations that a sparsity result or a small batch of attention figures readily suggests, our own earlier figures included."
- Sonuc (06_conclusion.tex:13): "Only the third is a published claim; the first two are interpretations that our own earlier figures encouraged."

Ek (esik altinda, elle gozlem): ayni uc rakam (4.4, 19.4, 15.01, 9.21, 5.79, 3.91) ve "$3.91$ points" hesabi ozet, giris 23 ve sonuc 9'da; tartisma 05_discussion.tex:13'te "15.01\pm0.84" ve 04_experiments.tex:117'de ayni anlatim. "0.41 points / 36 directions / r = 0.986" ifadesi giris 25. satir, sonuc 9. satir ve tartisma 21. satirda (0,986) tekrar eder. "1.85 points" SVHN farki ozet, sonuc 9, tartisma 21'de.

## Tablo D. Tartismanin "reporting requirements" listesi (05_discussion.tex:36-45), aynen
Alt bolum basligi: "\subsection{Reporting Requirements}" (satir 36; yorum satirinda hala "5.2 Recommendations", satir 34). Giris cumlesi (satir 39): "Several requirements for cross-architecture robustness studies follow from these measurements." Liste duz yazidir, numarasizdir.

R1 (satir 41): "Studies should state the conditioning protocol and report which samples enter the denominator."
R2 (satir 41): "Where a directional claim is made, a protocol that scores both directions on identical samples should be preferred, so that paired inference is available."
R3 (satir 41): "Unconditioned transfer rates should not be reported as architecture comparisons."
R4 (satir 41): "When targets differ in clean accuracy, the raw rate is a known mixture of transferability and target weakness, $r_{\text{raw}} - r_{\text{cond}} = e\,(1 - r_{\text{cond}})$, and since that relation is an algebraic identity, the correction can be applied to published raw rates without re-running anything."
R5 (satir 43): "Next to the score, studies should report the decomposition. Absolute robustness factors exactly into clean accuracy and conditional susceptibility, and which factor carries a headline is not recoverable from the score alone."
R6 (satir 43): "Ranking claims should be separated from mechanism claims: our rankings were stable across checkpoint sets while our mechanism attribution was not, so mechanism claims should carry more training runs."
R7 (satir 43): "For layer-wise analyses the aggregation should be stated, since CLS-only, patch-mean, and all-token summaries of the same blocks give different drift magnitudes and different minima."
R8 (satir 43): "Attention claims, finally, should be checked at a realistic sample size: the attention null result we report had looked positive on a small figure batch."
Uygulayici paragrafi (satir 45): "For practitioners choosing between the two families under matched standard adversarial training on this benchmark, the CNN gives higher absolute robust accuracy and the advantage holds under every view we measured. The WideResNet reference at 62.76\% shows that a larger model trained on extra data with a stronger recipe~\cite{gowal2020uncovering} moves robustness further than the choice between these two families does."

Atif/yer notlari:
- 01_introduction.tex:29: "The measurements translate into concrete reporting requirements for cross-architecture robustness studies, which are collected at the end of the discussion." Alt bolum 5.2'dir (05_discussion.tex:36); sonrasinda 5.3 Limitations (satir 50) ve 5.4 Future Directions (satir 66) gelir. Sayfa: V baslar p19 (INDEKS), "B. REPORTING REQUIREMENTS" p20, "D. FUTURE DIRECTIONS" p21 (pg.py).
- 06_conclusion.tex:15: "From these measurements we distilled a short set of reporting requirements, of which the first two matter most: state the conditioning protocol and prefer paired ones, and do not present unconditioned transfer rates as architecture comparisons." (Ayni "ilk ikisi" R1/R2/R3 uzerinden; Tartismada oncelik sirasi belirtilmemis.)
- Ozet cumle 11: "we close with reporting requirements for cross-architecture robustness studies."
- Not: R7 ve R8 sonuc 04_experiments'taki katman/dikkat bulgularina dayanir; R6, 04_experiments.tex:66 ve 05_discussion.tex:23'e dayanir.

## Tablo E. Acik sinirlilik/kisitlama cumleleri (e1_lim.py + elle; satir numarali, aynen)

E1. Limitations alt bolumu (05_discussion.tex:50-61):
- :53 "The scope of the study limits its conclusions in specific ways."
- :55 "The protocol-sensitivity result is measured on three datasets and one model pair."
- :55 "That account is incomplete: it holds for three of the four protocols, while the successful-source protocol adds a second driver tied to the \emph{source's} robustness that is strong enough to reverse the overall relationship (Section~\ref{subsec:transfer})."
- :55 "What we still cannot state is the functional form of either dependence with confidence: the estimates rest on six seed-and-dataset clusters, and every small-gap pair in our pool involves the external WideResNet, so a small clean-accuracy gap and a different training recipe are not separable here."
- :57 "We cannot isolate the cause of the differences between our two checkpoint sets."
- :57 "The contrast is evidence that single-run mechanism claims are fragile; it does not measure leakage."
- :59 "Every model in this paper is trained inside a single threat model: $\Linf$ at $\eps = 8/255$." ... "Whether the effect holds for models \emph{trained} under another norm is untested here."
- :61 "Three runs per architecture bound seed variance but do not span the recipe space..." "Our ViT results characterize baseline adversarial training, not the best achievable ViT robustness." "The two models also differ in parameter count (11.2M versus 5.7M), so architectural attribution of the absolute gap remains partial." "Our TGR result, finally, comes from an adaptation of the original method, not a reproduction of its published setting."
E2. Gelecek calisma (05_discussion.tex:71): "The leakage ablation, on six full-budget trajectories, did not detect an effect of leakage on checkpoint selection, but it answers a weaker question than the one posed: ..." ve ":71 What remains open is the capacity-matched pair (ViT-Small against ResNet-50, say), ..."
E3. Tartisma gövdesi: :21 "With three targets that correlation is suggestive; establishing it would take a larger model pool." ; :29 "The result is specific to this regime, since our targets are adversarially trained and our data are CIFAR-scale." ; :17 "Testing this properly would require their per-direction clean accuracies under a shared protocol..." ; :15 "...the spread we measure is the size of that ambiguity, a bound on what the omission costs."
E4. Deneyler: 04_experiments.tex:66 "We cannot isolate a cause, since the corrected protocol changed validation handling and the training run together"; :123 "The pool for this fit excludes the SVHN pair, which departs from the pre-registration." ; :123 "We therefore withdraw the four-protocol slope; the mechanism claim rests on the three-protocol one, which survives the pool question..." ; :125 "Two cautions apply to these intervals. With six to eight clusters a percentile cluster bootstrap undercovers, so the intervals below should be read as lower bounds on width. And the WideResNet is a single fixed external checkpoint that appears in all six observational clusters, in twelve of the eighteen direction pairs, so those clusters are not fully independent" ; :127 "...a quantity this sensitive to which pairs enter the fit is not one a mechanism claim can rest on. ... Two limits apply." ; :172 "With only three targets, the correlation can only be suggestive." ; :206 "One of the three registered predictions is confirmed, one fails under the reading we treat as binding, and the third is not testable in this design." ; :206 "The measurement is \emph{consistent with} the prediction without \emph{testing} it, and it does not count as a third confirmation." ; :240 "...two runs cannot bound the run-to-run variation." ; :244 "SVHN was run in a reduced configuration fixed in advance: two seed pairs instead of three, $50$ adversarial-training epochs, no AutoAttack, and no third architecture." ; :252 "...this probes how the protocol affects the conclusion, not $L_2$ robustness, and the absolute values below are not comparable with $L_2$-trained references." ; :269 "The third prediction ... cannot fail once Equation~\eqref{eq:raw_identity} holds ... the fitted slope of $+0.914$ estimates $1 - r_{\text{cond}}$ rather than testing anything." ; :453 "We do not headline the ratio of these two spreads. With three runs the denominator carries two degrees of freedom..." ve ":453 Two cautions bound it further: ... which makes the ratio an upper bound."
E5. Yontem: 03_methodology.tex:137 "Because the published regularization scheme is not replicated exactly, the negative result below bounds our adaptation only; extending it to the method as published would require a replication with the original scheme." ; :102 "They enter only as a contrast: the difference between the two checkpoint sets is itself evidence about how far a single-run conclusion can move."
E6. Sonuc (06_conclusion.tex:15): "Our study covers three datasets and a single model pair, so the size of the protocol effect for other architecture pairs remains to be calibrated; the mechanism behind it, an unequal clean-accuracy gap between targets, is not specific to our setting."
Not: Limitations alt bolumu dort paragraf (satir 55, 57, 59, 61); ayni kayit "SVHN iki tohum cifti", "yalniz tek model cifti" Limitations'ta yinelenir ("three datasets and one model pair", satir 55). Limitations'ta SVHN indirgenmis yapilandirma (04_experiments.tex:244) anilmaz; pre-registration sapmasi (04_experiments.tex:123 "departs from the pre-registration") Limitations'ta anilmaz (grep: 05_discussion.tex icinde "pre-regist" yok). Her ikisi icin dogrulama: e1_lim.py ciktisi 05_discussion satirlarinda bu ifadeleri vermedi.

## Tablo F. Ileri atiflar (e1_refs.py: Section~\ref hedefi, hedefin tanimlandigi satirdan once ya da sonra)
Hedefin etiketi satiri bu atif satirindan sonraysa "ILERI".

Giris roadmap'i ve ozet cumlesi disindaki ileri atiflar:
| atif konumu | hedef | hedef etiketi | not |
|---|---|---|---|
| 01_introduction.tex:9 | sec:discussion | 05_discussion.tex:5 | "a point Section~\ref{sec:discussion} returns to" |
| 01_introduction.tex:31 | sec:experiments | 04_experiments.tex:5 | "the algebraic identity of Section~\ref{sec:experiments}" |
| 02_related_work.tex:13 | subsec:attack_methods | 03_methodology.tex:56 | ilgili calisma yontem altbolumune atif |
| 03_methodology.tex:7 | subsec:metrics | 03_methodology.tex:108 | ayni dosya |
| 03_methodology.tex:17 | sec:experiments | 04_experiments.tex:5 | |
| 03_methodology.tex:102 | subsec:robustness | 04_experiments.tex:11 | |
| 03_methodology.tex:118 | subsec:transfer | 04_experiments.tex:82 | |
| 03_methodology.tex:125 | subsec:gradient | 04_experiments.tex:277 | |
| 03_methodology.tex:131 | subsec:attention | 04_experiments.tex:357 | |
| 03_methodology.tex:156 | subsec:transfer; subsec:statistics_results | 04_experiments.tex:82; :447 | |
| 03_methodology.tex:158 | subsec:gradient | 04_experiments.tex:277 | |
| 04_experiments.tex:117 | subsec:statistics_results | 04_experiments.tex:447 | ayni dosya, ileri |
| 04_experiments.tex:123 | subsec:statistics_results | 04_experiments.tex:447 | ayni dosya, ileri |
| 04_experiments.tex:212 (iki kez) | subsec:statistics_results | 04_experiments.tex:447 | ayni dosya, ileri |
Giris roadmap'i (01_introduction.tex:36): Section atiflari sec:related_work, sec:methodology, sec:experiments, sec:discussion, sec:conclusion (bes ileri atif; roadmap gelenegi).
Toplam ileri Section~\ref hedefi: 21 (roadmap 5, giris 2, ilgili calisma 1, yontem 9, deneyler 4).
Geri atiflar (bilgi): 04_experiments.tex:64, 84, 191, 206, 242, 244, 269, 271, 279, 305, 359, 421, 441; 05_discussion.tex:13, 21, 55, 59, 71.

Sunumdan once atiflanan tablo/sekil/denklem (ilk atif satiri < etiket satiri; e1_refs.py ikinci blok):
- fig:study_overview: ilk atif 03_methodology.tex:7, etiket 03:18 (ayni bolumde 11 satir sonra)
- tab:main_results: ilk atif 03_methodology.tex:69, etiket 04_experiments.tex:18 (Methodology'de, Experiments tablosuna atif)
- tab:conditional: 04:41, etiket 04:46
- fig:epsilon_sweep: 04:68, etiket 04:74
- tab:tgr: ilk atif 04_experiments.tex:121, etiket 04:426 (305 satir sonra; p18 tablo 11, atif p10-11 civari)
- tab:transfer_matrix: 04:135, etiket 04:152
- fig:transfer_heatmap: 04:172, etiket 04:178
- tab:gradient: 04:279, etiket 04:284
- tab:spatial: 04:303, etiket 04:318
- fig:gradient_heatmap: 04:338, etiket 04:348
- fig:feature_degradation: 04:392, etiket 04:409
Tablo numarasi sirasi (INDEKS.md): Table 1 p8, 2 p9, 3 p9, 5 (cifar100) p12 ve 4 (transfer_matrix) p12 (INDEKS'te tab:cifar100_results 5 satiri tab:transfer_matrix 4'ten once yazili, ayni sayfa), 7 (l2) p14 ve 6 (svhn) p14, 8-9 p15, 10 p16, 11 p18. Table 11 (tab:tgr) 18. sayfada, 4.2 bolumunden (p10-11) atiflanir: yaklasik 7 sayfa ileri.

## Tablo G. Sayfa butcesi (INDEKS.md ve main.pdf; PyMuPDF ile sayfa basina kelime sayisi)
Toplam 24 sayfa (INDEKS.md:3). Bolum baslangic sayfalari (INDEKS.md): I p1, II p2, III p4, IV p8, V p19, VI p21. Ek PyMuPDF taramasi: "REFERENCES" basligi p22, "DATA AND CODE AVAILABILITY" ve "ACKNOWLEDGMENT" p22, kaynakca p22-24, "B. REPORTING REQUIREMENTS" p20, "D. FUTURE DIRECTIONS" p21.

| bolum | baslangic-bitis sayfasi | kapsanan sayfa (ucu dahil) | duz yazi kelimesi | kelime payi |
|---|---|---|---|---|
| Ozet + basliklar | p1 | | 248 (ozet) | |
| I Introduction | 1-2 | 2 (II, p2'nin basinda baslar) | 1034 | 7,0% |
| II Related Work | 2-4 | 3 | 1354 | 9,2% |
| III Methodology | 4-8 | 5 (IV p8'in basinda baslar) | 2448 | 16,6% |
| IV Experiments | 8-19 | 12 | 7339 | 49,9% |
| V Discussion | 19-21 | 3 | 2014 | 13,7% |
| VI Conclusion | 21-22 | 2 | 523 | 3,6% |
| Data/Ack + kaynakca | 22-24 | 3 | | |

Sayfa basina PyMuPDF kelime sayilari: p1 540, p2 876, p3 756, p4 843, p5 472 (Sekil 1), p6 821, p7 829, p8 821, p9 793, p10 902, p11 962, p12 757, p13 957, p14 889, p15 916, p16 665, p17 713, p18 885, p19 954, p20 859, p21 893, p22 915, p23 1171, p24 558.
Deneyler bolumu 8-19 arasi 11 sayfa tam ve p8 sonu (INDEKS: 11 tablo/sekil/denklem etiketi p8-p18). Sonuc p21'de baslar ve p22'de biter ("the checkpoint-selection ablation point the same way" p22 basinda). Toplamin yarisina yakini (12/24 sayfa kapsama; 11 tam sayfa) deneyler bolumudur.
Sayfa 5: yalniz Sekil 1 ve ilgili metin (472 kelime, en dusuk sayfa). Sayfa 16: Sekil 5, 6, Tablo 10 (665 kelime).
Tablo ve sekil sayisi: 11 tablo ve 8 sekil numarali (INDEKS.md satirlari: Fig 1-8, Tab 1-11), denklem 11'e kadar (eq:raw_identity = 11, p11).
Ek (Appendix) bulunmuyor: main.tex'te \appendix yok, "Appendix" aramasi bos (grep); main.tex:113 "Data and Code Availability" ve :123 "Acknowledgment" \section* ile numarasiz.

## Tablo H. Makine uretimi veya asiri temkinli kayit: 12 aynen alinti (konum satiri)
Ayirt edici belirtec: kendi metnine hakem sesiyle atif ("Only the last is a published claim", "does not count as a third confirmation"), kosulsuz dogruluk beyani ("algebraically equal", "genuine"), tekrar eden kalip "X, not Y", "rather than", "in other words", "for its part", "finally,", "turns out to be".
1. 01_introduction.tex:18 "Only the last is a published claim; the first two are interpretations that a sparsity result or a small batch of attention figures readily suggests, our own earlier figures included."
2. 01_introduction.tex:25 "Absolute robustness, for its part, factors exactly into clean accuracy and conditional susceptibility."
3. 01_introduction.tex:11 "Papers usually treat these choices as reporting details, but they are part of the result."
4. 04_experiments.tex:66 "The decomposition is worth reporting even when the two factors agree, because they need not, and because their relative weight is less stable than the ordering they produce."
5. 04_experiments.tex:206 "The measurement is \emph{consistent with} the prediction without \emph{testing} it, and it does not count as a third confirmation."
6. 04_experiments.tex:269 "...cannot fail once Equation~\eqref{eq:raw_identity} holds: the deviation \emph{is} $e\,(1 - r_{\text{cond}})$, so it rises with $e$ by construction, and the fitted slope of $+0.914$ estimates $1 - r_{\text{cond}}$ rather than testing anything."
7. 04_experiments.tex:123 "We therefore withdraw the four-protocol slope; the mechanism claim rests on the three-protocol one, which survives the pool question and is what Section~\ref{subsec:statistics_results} carries forward."
8. 04_experiments.tex:127 "...a quantity this sensitive to which pairs enter the fit is not one a mechanism claim can rest on."
9. 05_discussion.tex:15 "One objection deserves an answer in its own terms: the four protocols estimate four different quantities, so the distance between them is not a variance, and calling it one would be a category error. We agree, and we make no assumption that the architectures have a single true asymmetry that the protocols estimate with error."
10. 05_discussion.tex:43 "Attention claims, finally, should be checked at a realistic sample size: the attention null result we report had looked positive on a small figure batch."
11. 06_conclusion.tex:9 "The direction, in other words, holds while the models are unmatched, and our three-target analysis associates it with the target's own vulnerability ($r = 0.986$)."
12. 04_experiments.tex:125 "We calibrate the protocol spread against the clean-error gap in two ways that fail differently, and they agree on three of the four protocols."
Ek kalip sayimlari (Tablo A.2): "does not/do not/did not" 30 kez deneyler, 9 tartisma, 3 sonuc, 4 giris; "thus/therefore/hence" 18 deneyler; "cannot" 5 deneyler, 4 tartisma; "not X but Y" 3 tartisma, 1 sonuc.
Not: 04_experiments.tex:127 "not one a mechanism claim can rest on" ve 04_experiments.tex:123 "withdraw" gibi sonradan-geri-cekme cumleleri deneyler gövdesinde, bulgunun sayfa 11-12 civarinda; ozet ve giris bu geri cekmeyi anmaz (grep: "withdr" yalniz 04_experiments.tex:123 ve :127'de).

## Tablo I. Asiri iddia: ayni konu icin guclu ve temkinli surumler (konum)
1. Giris 25. satir (01_introduction.tex:25) "Incoming transfer also tracks the target's own vulnerability ($r = 0.986$ across three targets), which reframes the asymmetry as a property of the weaker target." / sonuc 06_conclusion.tex:9 "our three-target analysis associates it with the target's own vulnerability" / temkinli: 04_experiments.tex:172 "With only three targets, the correlation can only be suggestive." ve 05_discussion.tex:21 "With three targets that correlation is suggestive; establishing it would take a larger model pool."
2. Sonuc 06_conclusion.tex:15 "the mechanism behind it, an unequal clean-accuracy gap between targets, is not specific to our setting." / temkinli: 05_discussion.tex:55 "That account is incomplete: it holds for three of the four protocols..." ve "What we still cannot state is the functional form of either dependence with confidence"; 04_experiments.tex:123 "We therefore withdraw the four-protocol slope".
3. Sonuc 06_conclusion.tex:9 "an identity that holds to within $0.41$ points across $36$ measured directions and that applies to any published raw rate whose targets satisfy the measured antecedent." / 05_discussion.tex:41 "the correction can be applied to published raw rates without re-running anything" (R4); temkinli: 04_experiments.tex:269 "...cannot fail once Equation holds ... estimates $1 - r_{\text{cond}}$ rather than testing anything" ve 03/04 ("premise we measure rather than assume", ozet cumle 7).
4. Ozet cumle 10 "Varying only the checkpoint-selection rule adds a fourth, rarely reported, source of variance." ve giris 23 "turns out to be a source of variance that papers rarely report" / 05_discussion.tex:71 "did not detect an effect of leakage on checkpoint selection, but it answers a weaker question than the one posed" ve 04_experiments.tex:453 "We do not headline the ratio of these two spreads."
5. Sonuc 06_conclusion.tex:9 "The measurement dominates" / ozet cumle 2 "much of the disagreement comes from the measurement protocol" / 05_discussion.tex:15 "the four protocols estimate four different quantities, so the distance between them is not a variance, and calling it one would be a category error" ve ":13 'The central result is an ordering of dispersions'".
6. Sonuc 06_conclusion.tex:9 "The direction is stable across protocols, seeds, and attack families on both CIFAR datasets" ve 05_discussion.tex:21 "CNN-crafted examples transfer better to the ViT than the reverse \emph{on both CIFAR datasets}" / 04_experiments.tex:206 "One of the three registered predictions is confirmed, one fails under the reading we treat as binding, and the third is not testable"; 05_discussion.tex:55 "its size does not follow the clean-accuracy gap across datasets".
7. Sonuc 06_conclusion.tex:13 "Two behavioral differences did survive and reproduce across independent checkpoint sets: the gradient sparsity ordering..." / 05_discussion.tex:25 "(Hoyer $0.4928$ versus $0.4561$, consistent in every run; per-sample $p<10^{-11}$, run-level $p=0.108$ after correction)" (run-duzeyi p=0,108 anlamsiz).
8. 05_discussion.tex:45 "the CNN gives higher absolute robust accuracy and the advantage holds under every view we measured." / 04_experiments.tex:66 "supporting the reading that the CNN advantage was entirely a clean-accuracy effect" (onceki kontrol noktasi seti icin) ve 05_discussion.tex:23 "They did not agree on our earlier checkpoints".

## Tablo J. Ek yapi gozlemleri (dogrulanmis)
- Giris 6 paragraf + yol haritasi; 4. ve 5. paragraf katkilar: "Our first contribution is to quantify protocol sensitivity." (01_introduction.tex:23, 187 kelime), "The second contribution concerns unconditioned transfer rates" (satir 25). Ucuncu katki paragrafi baslik cumlesi "Three of the results we report are negative" (satir 27); katki numaralandirmasi birinci ve ikinci ile sinirli.
- Giris 31. satir: ATEEC 2026 on surumu ve "it corrects one claim of the earlier version" (01_introduction.tex:31).
- 06_conclusion.tex 5 paragraf, ilk paragraf 257 kelime (satir 9; tek paragrafta tum ana sonuclar).
- 04_experiments.tex satir 117 (462 kelime, bir tek paragraf) deney bolumunun en uzun paragrafi.
- Yontem 03_methodology.tex:113 (Transfer Attack Metrics) 365 kelimelik paragraf, denklemler paragrafi boler (betik denklem oncesi ve sonrasi metni birlestirir).
- Tartisma 05_discussion.tex:10 baslik "What the Measurements Show", yorum "5.1 Key Findings"; :36 yorum "5.2 Recommendations"; :66 "5.4 Future Work" (yorumlarda eski baslik adlari).
- Tartisma alt bolum 5.1 (satir 10-31) 10 paragraf, hepsi duz yazi; ilk iki paragraf retraining-karsi-protokol dagilim sirasi.
- Reporting Requirements yer yeri: 05_discussion.tex:36-45 (satir olarak 10 satir, 3 paragraf + uygulayici paragrafi).

## Bulunamayan / belirsiz
- Sayfa-sayfa paragraf eslemesi icin pdftotext yok; PyMuPDF baslik sayfalari verdi (pg.py).
- "Machine-generated register" olcutu nesnel degildir; Tablo H alintilari betik degil okuma sonucudur, Tablo A.2 sayimlari yalniz tarif edilen kelime listesine dayanir.
- Cumle bolme sezgiseldir; "et al.", ondalik ve kisaltmalar ele alinmistir, bazi denklem komsulugu cumleleri birlesmis olabilir (Tablo A.1, yontem 113. satir).
- Ozet-giris-sonuc yakin ayni cumleler Jaccard 0,45 esigiyle bulundu; daha dusuk esik kullanilmadi.
