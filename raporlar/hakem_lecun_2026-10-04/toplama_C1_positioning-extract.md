# Toplama C1: konumlandirma dosyasi (lens C, novelty-and-positioning)

Kaynak dosyalar (hepsi /home/firat/projects/adeb_sci_1/paper/manuscript/): `sections/01_introduction.tex` (I), `02_related_work.tex` (RW), `03_methodology.tex` (M), `04_experiments.tex` (E), `05_discussion.tex` (D), `06_conclusion.tex` (C), `main.tex` (abstract, satir 88-90), `references.bib` (bib). Yalnizca toplama; yargi yok. Hicbir manuscript dosyasi degistirilmedi.

## 10 satirlik ozet

1. Istenen 15 eser icin RW/D/I/M icindeki her konumlandirma cumlesi satir numarasiyla ve tirnakla kaydedildi (Bolum A).
2. Her eser icin references.bib girdisi (baslik, mecra, yil, DOI, arXiv) kaydedildi (Bolum B); bib satir araliklari verildi.
3. Kayit disi bulgu: Carlini 2019 bib girdisinde `eprint`/`doi` alani yok; kimlik yalnizca `journal = {arXiv preprint arXiv:1902.06705}` icinde (bib 641-646).
4. Kayit disi bulgu: Bai 2021 ve Shao 2022 (TMLR) girdilerinde `doi` yok, yalnizca `eprint` var; Demontis 2019, Naseer 2022, Zhang 2019 (TRADES), Liu 2017 icin de `doi` yok, `eprint` var.
5. Zhao "2025": metin anahtari `zhao2025revisiting`, ama bib `year = {2026}` (TPAMI vol 48 no 1, bib 470-480); metinde yil gorunmez, yalnizca anahtar.
6. TRADES "natural + boundary" ayrisimi: `boundary` sozcugu manuscriptte yalnizca AutoAttack ve E:145 baglaminda geciyor, TRADES ile baglantili degil. TRADES RW:28 ("trade-off between natural accuracy and robustness") ve M:85'te ("alternative formulations such as TRADES ... this work focuses on standard adversarial training") anilir; ayrisim kavrami olarak konumlandirilmaz. Bu eser icin kullanilabilir "boundary-error" metni YOK.
7. "Katki" paragraflari I:23, I:25, I:27 (ucuncu katki: olumsuz sonuclar); I:29 gereklilikler; I:31 ATEEC onsurum notu. Her katki icin metnin kendi itiraf ettigi en yakin eser Bolum C'de.
8. Aranan kaliplar: "we know of no" (RW:74, 1 kez), "remain scarce" (RW:54, 1 kez), "rarely reported/report(s)" (I:11, C:80, abstract), "rarely pairs" (RW:72), "orthogonal" (RW:74), "a different axis"/"different axis" (RW:62, RW:74). "to our knowledge", "first to", "novel" icin eslesme yok (grep). Bolum D.
9. Bulunamayan: Tramer 2020 ve Carlini 2019 yalnizca RW:74'te anilir (bagimsiz baska satir yok); Pinto 2022 yalnizca RW:72; Ali 2024 yalnizca RW:72; TA-Bench yalnizca RW:62; D bolumunde bu uclunun hicbiri gecmez.
10. Yu et al. 2025 ve TA-Bench'e karsi konumlandirma tek paragrafta (RW:62) ve bir cumlede (RW:74); Yu et al.'in Introduction'da (I) anilmadigi dogrulandi (I icinde `yu2025reliable` yok).

---

## Bolum A. Eser eser: metnin ne dedigi, nerede

Tum alintilar birebir; `\cite` ve `\emph` imleri korunmustur.

### A1. Carlini et al. 2019 (`carlini2019evaluating`)
- RW:74: "The evaluation-methodology literature has repeatedly shown that how robustness is measured decides what is concluded: Carlini et al.~\cite{carlini2019evaluating} catalog the failure modes of robustness evaluation, and Tram\`er et al.~\cite{tramer2020adaptive} show that defenses judged robust under fixed attacks fall to adaptive ones. That work concerns attack strength, that is, whether the measurement is strong enough."
- Baska yer: yok (grep: sections/03, 04, 05, 06, 01 icinde atif yok).

### A2. Tramer et al. 2020 (`tramer2020adaptive`)
- RW:74 (ayni paragraf): "Tram\`er et al.~\cite{tramer2020adaptive} show that defenses judged robust under fixed attacks fall to adaptive ones. That work concerns attack strength, that is, whether the measurement is strong enough. The question we ask is orthogonal: with attack strength held fixed, how much does the \emph{conditioning set} alone move the conclusion?"
- Baska yer: yok.

### A3. Yu et al. 2025 "Reliable Evaluation of Adversarial Transferability" (`yu2025reliable`)
- RW:62: "Yu et al.~\cite{yu2025reliable} report that transferability is systematically overestimated when it is measured across a single architecture family, and propose three evaluation protocols that differ in how a multi-target outcome is scored: treating an ensemble as a single target, counting how many targets are fooled, and requiring that all of them are."
- RW:62 (konumlandirma): "TA-Bench holds the scoring rule fixed and varies the attack and the model pool; Yu et al.\ vary the scoring rule along the target-aggregation axis. We vary it along the conditioning axis instead, with the models, the data and the attack budget fixed, which isolates the contribution of the conditioning set and makes it possible to state the arithmetic relation between the resulting estimates."
- RW:74: "Yu et al.\ vary the scoring rule too, but along a different axis, and we know of no controlled estimate of how much the choice of conditioning set matters."
- Giris: yok. Discussion/Conclusion: yok.

### A4. TA-Bench, Li et al. 2023 (`li2023tabench`)
- RW:62: "Two recent benchmarks move in the same direction: TA-Bench~\cite{li2023tabench} standardizes the comparison of more than thirty transfer attacks over a common pool of substitute and victim models, and Yu et al. ..." (devami A3).
- RW:62: "TA-Bench holds the scoring rule fixed and varies the attack and the model pool".
- Baska yer: yok.

### A5. Zhao et al. (`zhao2025revisiting`; bib yili 2026)
- RW:62: "systematic re-evaluations of transfer attacks likewise restrict the pool to samples that every model classifies correctly~\cite{zhao2025revisiting}."
- M:118 (atif listesi): "Conditioning transfer evaluation on correctly classified samples is established practice, usually on the samples that every model in the study classifies correctly~\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, zhao2025revisiting}".
- D: yok; RW:74 atif listesinde yok (RW:74 listesi: liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend).

### A6. Ravikumar et al. TREND (`ravikumar2023trend`)
- RW:62: "In ensemble design, Ravikumar et al.~\cite{ravikumar2023trend} restrict transfer measurement to samples correctly classified by both models precisely to account for accuracy differences between them, the same confound our conditioned metric controls."
- RW:74: "Conditioning transfer evaluation on samples the models classify correctly is established practice~\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend}, and individual papers pick one conditioning set and proceed."
- M:118: "the \emph{both-correct} protocol ... ~\cite{mahmood2021robustness, ravikumar2023trend}"; "The successful-source rate is the transferability metric of Ravikumar et al.~\cite{ravikumar2023trend}, whose Equation~(1) divides the number of examples that transfer to the target by the number generated against the source, over a pool restricted to samples both models classify correctly; it is also the protocol implied whenever a transfer rate is reported over ``successful'' adversarial examples."
- D:15: "Conditioning itself remains established practice~\cite{liu2017delving, dong2018boosting, ravikumar2023trend} and is necessary; the point is that the choice of conditioning set has to be reported with the result, in the main text."

### A7. Mahmood et al. 2021 (`mahmood2021robustness`)
- I:9: "several report that attacks move more easily from ViTs to CNNs than the reverse~\cite{mahmood2021robustness, benz2021adversarial, shao2022adversarial} ... the direction measured in this paper is the opposite of the first group's, a point Section~\ref{sec:discussion} returns to."
- RW:52: "Subsequent work revealed that ViTs remain vulnerable to adversarial attacks, particularly gradient-based methods~\cite{mahmood2021robustness}".
- RW:64: "Mahmood et al.~\cite{mahmood2021robustness} measured transfer between CNNs and ViTs with a both-correct protocol and found notably low CNN$\leftrightarrow$ViT transferability".
- RW:74 (conditioning establishment list), M:118 (both-correct protocol).
- D:17: "Under a both-correct protocol comparable to ours, Mahmood et al.~\cite{mahmood2021robustness} report the opposite direction on a different architecture pair, finding transfer into the transformer weaker than transfer out of it, and Benz et al.~\cite{benz2021adversarial} and Shao et al.~\cite{shao2022adversarial} report the same ordering on their own model sets. Our mechanism is compatible with those results: we attribute the asymmetry to the target's own vulnerability rather than to any special strength of CNN-crafted perturbations, which is also the first of the two factors Demontis et al.~\cite{demontis2019adversarial} identify, and the weaker target in Mahmood et al.'s pair is not the weaker target in ours. Testing this properly would require their per-direction clean accuracies under a shared protocol, which is the reporting we ask for and would give the mechanism a direct external test."
- Not (olgu): D:17 aciklamasi ("weaker target in Mahmood et al.'s pair is not the weaker target in ours") dogrudan test edilmemis; metin "Testing this properly would require their per-direction clean accuracies" der.

### A8. Benz et al. 2021 (`benz2021adversarial`)
- I:9: "Benz et al.~\cite{benz2021adversarial} report ViTs to be more robust for standardly trained models"; ve I:9'da transfer yonu listesinde.
- RW:52: "Benz et al.~\cite{benz2021adversarial} reported an early direct comparison including MLP-Mixer and linked the differences to frequency preferences."
- RW:64: "the frequency preferences behind that difference, CNNs leaning on high-frequency and ViTs on low-frequency content, are documented by Benz et al.~\cite{benz2021adversarial} and Shao et al.~\cite{shao2022adversarial}."
- D:17 (yukaridaki alinti).

### A9. Shao et al. 2022 (`shao2022adversarial`)
- I:9 (transfer yonu listesi).
- RW:54: "Shao et al.~\cite{shao2022adversarial} found ViTs more robust than CNNs and MLP-Mixers in white-box and transfer settings, with features that carry less high-frequency content, and showed that adversarial training applies to ViTs, although in their preliminary CIFAR-10 run the adversarially trained ViT did not improve on a large CNN."
- RW:64 (frekans), D:17.

### A10. Bai et al. 2021 (`bai2021transformers`)
- I:9: "Bai et al.~\cite{bai2021transformers} report that under matched training recipes transformers do not surpass CNNs".
- RW:52: "Bai et al.~\cite{bai2021transformers} systematically investigated whether transformers are more robust than CNNs, finding that under fair training recipes transformers are not more adversarially robust than CNNs, while exhibiting superior robustness under distribution shift attributed to self-attention".
- RW:72: "the pitfalls of unfair CNN and transformer comparisons have been highlighted before~\cite{pinto2022impartial, bai2021transformers}".

### A11. Pinto et al. 2022 (`pinto2022impartial`)
- RW:72 (tek yer): "While individual studies have examined CNN and ViT robustness separately, and the pitfalls of unfair CNN and transformer comparisons have been highlighted before~\cite{pinto2022impartial, bai2021transformers}, existing comparative work typically reports robustness scores in isolation, often with inconsistent perturbation budgets, attack configurations, or model scales, and rarely pairs the comparison with behavioral analysis."
- Pinto'nun ne yaptigi metinde ayrica anlatilmaz; yalnizca "pitfalls ... highlighted".

### A12. Ali et al. 2024, IEEE Access (`ali2024adversarial`)
- RW:72 (tek yer): "A recent study in this journal compares ViT and CNN adversarial robustness directly~\cite{ali2024adversarial}; our work differs by evaluating on the full test set with AutoAttack and paired statistics, by controlling transfer measurement for clean-accuracy differences, and by accompanying the comparison with gradient- and feature-level behavioral analyses."
- Not: Ali'nin hangi veri/saldiri/mimarilerle calistigi metinde belirtilmez.

### A13. TRADES, Zhang et al. 2019 (`zhang2019theoretically`)
- RW:28: "TRADES~\cite{zhang2019theoretically} provides a theoretically-grounded trade-off between natural accuracy and robustness:" + denklem `\mathcal{L}_{\text{TRADES}} = \mathcal{L}_{CE}(f(x), y) + \beta \cdot \text{KL}(f(x) \| f(x_{adv}))` (RW:30); "where $\beta$ controls the trade-off parameter." (RW:32).
- M:85: "While alternative formulations such as TRADES~\cite{zhang2019theoretically} offer theoretically grounded trade-off mechanisms, this work focuses on standard adversarial training to isolate architectural effects from defense-specific interactions."
- Dogal/sinir ayrisimi icin cumle yok. Ayrisim iddiasi yalnizca yazarlarin kendi "clean accuracy x conditional susceptibility" ayrisimi (I:25 "Absolute robustness, for its part, factors exactly into clean accuracy and conditional susceptibility"; D:23, D:43); bunun TRADES ile iliskisi metinde kurulmaz.

### A14. Demontis et al. 2019 (`demontis2019adversarial`)
- RW:62: "Demontis et al.~\cite{demontis2019adversarial} trace transferability to two factors, the intrinsic vulnerability of the target model and the complexity of the surrogate, and connect it to the alignment of the two models' input gradients."
- D:17: "which is also the first of the two factors Demontis et al.~\cite{demontis2019adversarial} identify".
- Baska yer: yok.

### A15. Diger yakin eserler (istenenlere ek, ayni kavram icin metinde gecenler)
- Liu et al. 2017 (`liu2017delving`) RW:62: "Foundational transfer studies already evaluate transferability on correctly classified samples~\cite{liu2017delving}"; Dong et al. 2018 (`dong2018boosting`) RW:62: "standard attack papers condition their success rates for the same reason~\cite{dong2018boosting}"; ikisi de RW:74, M:118, D:15 listelerinde.
- Naseer et al. 2022 (`naseer2022improving`) I:9 ve RW:64 ("showed that adversarial examples crafted \emph{on} ViTs transfer poorly under conventional attacks and proposed self-ensemble and token refinement"), RW:76.
- Waseda et al. 2023 (`waseda2023closer`) RW:64: "separate transfer outcomes further, by whether the target reproduces the source's exact error or fails in a different way, and report that both occur even between closely related models."
- TGR Zhang et al. 2023 (`zhang2023tgr`) RW:64, RW:76, I:27, D:21, D:29.
- Sahin & Yildirim 2026 (`sahin2026behavioral`, ATEEC) I:31 (asagida Bolum C).
- Gu 2022 / Fu 2022: D:27 ("Attention-shift results obtained with patch attacks~\cite{gu2022vision, fu2022patchfool} concern a different threat model and should not be generalized to $L_\infty$-bounded perturbations without measurement.")

---

## Bolum B. references.bib girdileri

| anahtar | bib satirlari | baslik | mecra | yil | DOI | arXiv |
|---|---|---|---|---|---|---|
| carlini2019evaluating | 641-646 | On Evaluating Adversarial Robustness | `journal = {arXiv preprint arXiv:1902.06705}` (@article) | 2019 | yok | 1902.06705 (yalnizca journal alaninda) |
| tramer2020adaptive | 648-655 | On Adaptive Attacks to Adversarial Example Defenses | NeurIPS, vol 33 | 2020 | yok | 2002.08347 |
| yu2025reliable | 460-468 | Reliable Evaluation of Adversarial Transferability | IEEE SaTML, s. 797-810 | 2025 | 10.1109/SaTML64287.2025.00049 | 2306.08565 |
| li2023tabench | 439-448 | Towards Evaluating Transfer-based Attacks Systematically, Practically, and Fairly | NeurIPS vol 36, s. 41707-41726 | 2023 | 10.52202/075280-1807 | 2311.01323 |
| zhao2025revisiting | 470-480 | Revisiting Transferable Adversarial Images: Systemization, Evaluation, and New Insights | IEEE TPAMI vol 48 no 1, s. 765-780 | **2026** (anahtar 2025) | 10.1109/TPAMI.2025.3610085 | 2310.11850 |
| ravikumar2023trend | 409-419 | TREND: Transferability-Based Robust ENsemble Design | IEEE Trans. Artificial Intelligence vol 4 no 3, s. 534-548 | 2023 | 10.1109/TAI.2022.3175172 | 2008.01524 |
| mahmood2021robustness | 183-191 | On the Robustness of Vision Transformers to Adversarial Examples | ICCV, s. 7818-7827 | 2021 | 10.1109/ICCV48922.2021.00774 | 2104.02610 |
| benz2021adversarial | 388-395 | Adversarial Robustness Comparison of Vision Transformer and MLP-Mixer to CNNs | BMVC | 2021 | 10.5244/C.35.68 | 2110.02797 |
| shao2022adversarial | 193-199 | On the Adversarial Robustness of Vision Transformers | Transactions on Machine Learning Research | 2022 | yok | 2103.15670 |
| bai2021transformers | 586-594 | Are Transformers more robust than CNNs? | NeurIPS vol 34, s. 26831-26843 | 2021 | yok | 2111.05464 |
| pinto2022impartial | 342-354 | An Impartial Take to the CNN vs Transformer Robustness Contest | ECCV (Springer) vol 13673, s. 466-480 | 2022 | 10.1007/978-3-031-19778-9_27 | 2207.11347 |
| ali2024adversarial | 356-364 | Adversarial Robustness of Vision Transformers Versus Convolutional Neural Networks | IEEE Access vol 12, s. 105281-105293 | 2024 | 10.1109/ACCESS.2024.3435347 | yok |
| zhang2019theoretically (TRADES) | 72-79 | Theoretically principled trade-off between robustness and accuracy | ICML, s. 7472-7482 | 2019 | yok | 1901.08573 |
| demontis2019adversarial | 59-66 | Why Do Adversarial Attacks Transfer? Explaining Transferability of Evasion and Poisoning Attacks | USENIX Security 19, s. 321-338 | 2019 | yok | 1809.02861 |
| liu2017delving | 421-427 | Delving into Transferable Adversarial Examples and Black-box Attacks | ICLR | 2017 | yok | 1611.02770 |
| dong2018boosting | 429-437 | Boosting Adversarial Attacks with Momentum | CVPR, s. 9185-9193 | 2018 | 10.1109/CVPR.2018.00957 | 1710.06081 |
| naseer2022improving | 213-219 | On Improving Adversarial Transferability of Vision Transformers | ICLR | 2022 | yok | 2106.04169 |
| zhang2023tgr | 300-308 | Transferable Adversarial Attacks on Vision Transformers with Token Gradient Regularization | CVPR, s. 16415-16424 | 2023 | 10.1109/CVPR52729.2023.01575 | 2303.15754 |
| waseda2023closer | 450-458 | Closer Look at the Transferability of Adversarial Examples: How They Fool Different Models Differently | WACV, s. 1360-1368 | 2023 | 10.1109/WACV56688.2023.00141 | 2112.14337 |
| sahin2026behavioral | 626-632 | A Behavioral Comparison of Adversarially Trained ResNet-18 and ViT-Tiny on CIFAR-10: Transfer Metrics, Gradient Structure, and Block-wise Feature Drift | Proc. ATEEC 2026, `note = {Preliminary version of the present study; submitted}` | 2026 | yok | yok |

Not: Bu tablo yalnizca bib alanlarinin kaydidir; DOI/arXiv kimliklerinin dis kaynakta dogrulanmasi bu toplamada YAPILMADI (ag erisimi kullanilmadi). Kokenli dogrulama durumu: dogrulanmamis.

---

## Bolum C. Belirtilen katkilar ve metnin kendi itiraf ettigi en yakin onceki is

Abstract (main.tex:89-90) ana iddialari: olcum protokolu uyusmazligin buyuk kismini aciklar; 4.4-19.4 puan yayilimi, 15.01 puan, 9.21 + 5.79 + 3.91 ayrisimi; ozdeslik; CIFAR-100 ve SVHN; kontrol noktasi secimi "a fourth, rarely reported, source of variance"; "Three further readings do not hold under direct measurement".

| Katki | Konum | Metinden alinti | Metnin kendi adlandirdigi en yakin onceki is (nerede) |
|---|---|---|---|
| K1. Protokol duyarliligini nicelemek | I:23 | "Our first contribution is to quantify protocol sensitivity. On identical models and data, the measured cross-architecture transfer asymmetry ranges from $+4.4$ to $+19.4$ points across four conditioning protocols, whereas retraining both architectures from scratch moves the same quantity by under $1.5$ points." | Yu et al. 2025 (puanlama kuralini hedef-toplama ekseninde degistirir; RW:62, RW:74); TA-Bench (puanlama sabit, saldiri ve model havuzu degisir; RW:62); Mahmood 2021, Ravikumar 2023, Zhao 2025 (tek kosullama kumesi secer; RW:74 "individual papers pick one conditioning set and proceed", M:118). Metnin kendi sozu: "we know of no controlled estimate of how much the choice of conditioning set matters" (RW:74). |
| K1a. Cebirsel ozdeslik / kapali formda duzeltme | I:23, I:25, RW:74, D:41, E:145 | "The $9.21$ points ... are removed in closed form by an identity we derive" (I:23); "which turns a known qualitative caveat into a correction that can be applied directly to published results" (RW:74) | Ravikumar 2023 ("the same confound our conditioned metric controls", RW:62); Liu 2017, Dong 2018 (kosullama "established practice", RW:62). "known qualitative caveat" (RW:74) ifadesi, niteliksel uyarinin bilindigini metnin kendisinin kabul ettigi yerdir. |
| K1b. Yon kararliligi ve yon donmesi (esit klinik dogruluk) | I:23, I:31, D:21 | "The direction of the asymmetry, unlike its magnitude, is stable \emph{as long as the two models differ in clean accuracy}; once they are matched, two of the four protocols reverse it." I:31: "it corrects one claim of the earlier version: the direction of the asymmetry is not stable once the architectures are matched in clean accuracy." | Metnin kendi onsurumu (Sahin 2026, ATEEC; I:31). Dis eser olarak: Mahmood 2021, Benz 2021, Shao 2022 (yon; I:9, D:17); Demontis 2019 (hedef zaafi faktoru; D:17). |
| K1c. CIFAR-100 tam replikasyon, kontrol noktasi secim kurali | I:23 | "A full replication on CIFAR-100 leaves the spread close to its CIFAR-10 size and preserves its sign, and the offline checkpoint-selection rule, varied on a fixed training trajectory, turns out to be a source of variance that papers rarely report." | Metin bu iki parca icin yakin bir onceki is adlandirmaz (I:23'te atif yok). C:80: "measurement choices that papers rarely report". |
| K2. Ham oranlarin hedefin temiz hatasiyla karisimi; 3x3 matris | I:25 | "The second contribution concerns unconditioned transfer rates, which are confounded by the target's clean error. In a $3\times3$ transfer matrix that adds a WideResNet-28-10 reference, the deviation of raw from conditioned rates obeys an identity ... the raw rate equals the clean error plus the conditioned rate scaled by one minus that error, to within $0.41$ points. Incoming transfer also tracks the target's own vulnerability ($r = 0.986$ across three targets), which reframes the asymmetry as a property of the weaker target." | Demontis 2019 (hedef kendi zaafi; D:17 "which is also the first of the two factors Demontis et al. identify"); Ravikumar 2023 (ayni karisimi kontrol eder; RW:62); Mahmood/Benz/Shao (karsi yon; D:17). D:21: "With three targets that correlation is suggestive; establishing it would take a larger model pool." |
| K2a. Mutlak dayaniklilik = temiz dogruluk x kosullu hassasiyet | I:25, D:23, D:43 | "Absolute robustness, for its part, factors exactly into clean accuracy and conditional susceptibility." | Yakin onceki is adlandirilmaz. TRADES bu ayrisimla iliskilendirilmez (bkz. A13). |
| K3. Uc olumsuz sonuc | I:27, I:18, RW:76, C:84 | "Three of the results we report are negative: scale-invariant sparsity differences do not correspond to spatial localization differences, on all four spatial measures; CLS attention entropy does not change measurably under attack at $n=1000$; and Token Gradient Regularization~\cite{zhang2023tgr} ... gives no transfer gain in this regime, losing to plain MI-FGSM under a matched budget." | Yalnizca ucuncusu icin: TGR (Zhang 2023), Naseer 2022 (RW:76 "Only the third is claimed in the cited work; the first two are interpretations."). Dis kaynak olarak Gu 2022, Fu 2022 (D:27, yama saldirisi, farkli tehdit modeli); Chalasani 2020 (seyreklik, RW:44); Hurley 2009 (D:25). |
| K3a. Iki davranissal fark hayatta kalir | I:27 | "Gradient sparsity differences reproduce across independent checkpoint sets, are created by adversarial training, and are accompanied by an alignment difference that exists only in absolute cosine. Adversarial damage accumulates at qualitatively different depths in the two architectures, and the measured drift profile depends on the token aggregation used to compute it." | Tsipras 2019 ve Chalasani 2020 (AT gradyan yapisini degistirir; RW:44); Moosavi 2017 (evrensel pertürbasyon; D:31). |
| K4. Raporlama gereklilikleri | I:29, D:39-45 | "The measurements translate into concrete reporting requirements for cross-architecture robustness studies" | Carlini 2019 ve Tramer 2020 (degerlendirme metodolojisi, "attack strength" ekseni; RW:74). |
| K5. Karsilastirma niteligi (Arastirma bosluğu) | RW:72 | "our work differs by evaluating on the full test set with AutoAttack and paired statistics, by controlling transfer measurement for clean-accuracy differences, and by accompanying the comparison with gradient- and feature-level behavioral analyses." | Ali et al. 2024 (IEEE Access, "in this journal"); Pinto 2022, Bai 2021 (adaletsiz karsilastirma tuzaklari). |

Onsurum aciklamasi, I:31: "A preliminary version of this study was submitted to ATEEC 2026~\cite{sahin2026behavioral}. That version reports the conditional decomposition, the four-protocol transfer comparison, the gradient structure measurements and the block-wise drift profiles on CIFAR-10 alone, and describes them as preliminary. The present paper adds two further datasets, a second threat model, the algebraic identity of Section~\ref{sec:experiments}, the checkpoint-selection ablation, the transformer-specific transfer attack, and the pre-registered analysis protocol, and it corrects one claim of the earlier version".
(bib 626-632 `note`: "Preliminary version of the present study; submitted".)

Giris'te (I:9) metnin kendi tespiti: "These disagreements are usually attributed to differences in models, training recipes, or datasets, and the standard response is to compare under a matched recipe." I:11: "the conclusion still depends on a choice that is rarely reported: the \emph{measurement protocol} ... Papers usually treat these choices as reporting details, but they are part of the result."

---

## Bolum D. Kalip taramasi ("we know of no", "remain scarce", "rarely reported", "orthogonal", "a different axis")

| Kalip | Konum | Tam cumle |
|---|---|---|
| "we know of no" | RW:74 | "Yu et al.\ vary the scoring rule too, but along a different axis, and we know of no controlled estimate of how much the choice of conditioning set matters." |
| "remain scarce" | RW:54 (Vision Transformer Robustness altbolumunun son cumlesi) | "Behavioral comparisons between CNN and ViT robustness under a single evaluation protocol remain scarce." |
| "rarely reported" | I:11 | "the conclusion still depends on a choice that is rarely reported: the \emph{measurement protocol}." |
| "rarely report(ed)" | main.tex:89 (abstract) | "Varying only the checkpoint-selection rule adds a fourth, rarely reported, source of variance." |
| "rarely report" | I:23 | "turns out to be a source of variance that papers rarely report." |
| "rarely report" | C:80 | "measurement choices that papers rarely report are of the same order as the effects being reported." |
| "rarely pairs" | RW:72 | "existing comparative work typically reports robustness scores in isolation, ..., and rarely pairs the comparison with behavioral analysis." |
| "orthogonal" | RW:74 | "The question we ask is orthogonal: with attack strength held fixed, how much does the \emph{conditioning set} alone move the conclusion?" |
| "a different axis" | RW:74 | "Yu et al.\ vary the scoring rule too, but along a different axis" |
| "different axis" (esdeger) | RW:62 | "Yu et al.\ vary the scoring rule along the target-aggregation axis. We vary it along the conditioning axis instead" |
| "established practice" (yenilik-sinirlayici) | RW:74, M:118, D:15 | RW:74 "Conditioning transfer evaluation on samples the models classify correctly is established practice"; M:118 "Both are established."; D:15 "Conditioning itself remains established practice ... and is necessary" |
| "known qualitative caveat" | RW:74 | "turns a known qualitative caveat into a correction" |
| "move in the same direction" | RW:62 | "Two recent benchmarks move in the same direction" |
| "the same confound our conditioned metric controls" | RW:62 | (Ravikumar 2023 ile ayni karisim) |
| "highlighted before" | RW:72 | "the pitfalls of unfair CNN and transformer comparisons have been highlighted before" |
| "Only the last is a published claim" / "Only the third is claimed in the cited work" | I:18, RW:76, C:84 | Uc okumadan ikisi "interpretations"; "our own earlier figures included" (I:18) |
| Tarama: "to our knowledge", "first", "novel" | tum bolumler | Eslesme yok. Not: CLAUDE.md "ilk kez/bildigimiz kadariyla icin belgelenmis tarama sart" kurali var; manuscriptte "we know of no" (RW:74) tekil bir olumsuz varlik iddiasidir ve bu dosyada belgelenmis bir tarama kaydina atif yok (rapor/RW icinde yok). |

---

## Bolum E. Diger olgular

1. M:118: "the target-correct rate is the one-sided relaxation of that pool" (hedef-dogru protokol, both-correct havuzunun tek tarafli gevsetmesi olarak sunulur).
2. M:118: "The successful-source rate is the transferability metric of Ravikumar et al.~\cite{ravikumar2023trend}, whose Equation~(1) ..." yani dort protokolden biri (successful-source) onceki isten alinmis; both-correct, Mahmood ve Ravikumar'dan; "Both are established." Dort protokolun hepsinin yeni olmadigi M:118'de dogrudan yazili: "Both are established" ikisi icin.
3. M:118: "For directional claims we take the both-correct rate as the primary estimate".
4. D:19: "The unconditioned rate should not be used for architecture comparison at all".
5. D:13: "measured on the transfer asymmetry itself, retraining both architectures from scratch moves it by a standard deviation of $0.23$ to $1.27$ points, whereas changing only the conditioning protocol moves it by $15.01\pm0.84$ points".
6. D:15 itiraf: "the four protocols estimate four different quantities, so the distance between them is not a variance, and calling it one would be a category error. We agree".
7. D:55 sinirlama: "The protocol-sensitivity result is measured on three datasets and one model pair."; "its size does not follow the clean-accuracy gap across datasets"; "That account is incomplete".
8. C:86: "Our study covers three datasets and a single model pair, so the size of the protocol effect for other architecture pairs remains to be calibrated".
9. D:61: "Our TGR result, finally, comes from an adaptation of the original method, not a reproduction of its published setting."
10. D:61: "a ViT trained with the diffusion-generated data recipe of Wang et al.~\cite{wang2023better} has been reported to surpass WideResNets on CIFAR-10~\cite{wu2025vision}. Our ViT results characterize baseline adversarial training, not the best achievable ViT robustness."
11. RW:54: "Jain et al.~\cite{jain2024towards} traced a form of gradient masking in ViTs to softmax underflow in attention, which leaves PGD-style attacks sub-optimal on them, a caveat for PGD-only ViT evaluations that AutoAttack, with its gradient-free Square component, partly guards against".
12. RW:42: "WideResNet variants occupy the top of its CIFAR-10 ranking" (RobustBench).
13. Giris (I:9) transfer yonu: "the direction measured in this paper is the opposite of the first group's" ve D:17 "Whether our direction is the correct one is a separate question."
14. Yu et al. ve TA-Bench RW:62'de "recent benchmarks"; bu ikisi icin metin, kendi protokol ekseninden (kosullama) farkini "which isolates the contribution of the conditioning set and makes it possible to state the arithmetic relation between the resulting estimates" ile verir.
15. RW:76: "We measure each directly, and none holds in our setting." (uc okumanin hicbiri tutmaz; oysa D:31 ve I:27 iki davranissal farkin hayatta kaldigini soyler; RW:76 ile I:27 arasi ifade farki: RW:76 "none holds" uc "okuma" icin, I:27 ise "Two behavioral differences do survive" baska ifadeler icin.)
