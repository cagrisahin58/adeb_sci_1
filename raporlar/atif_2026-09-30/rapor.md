# Kaynakça ve atıf-bağlam denetimi, 2026-09-30

Kapsam: `paper/manuscript/references.bib` (64 girdi, tamamı metinde atıflı), IEEE Access, IEEEtran.bst. Denetleyen: atıf denetçisi (Sonnet 5.5). Yedek: `paper/manuscript/references.bib.bak` (denetim öncesi dosyanın birebir kopyası). `.tex` dosyalarına ve `results/q1_research/*.md` dosyalarına dokunulmadı.

## Türkçe özet

Uydurma (HALLUCINATED) kayıt bulunmadı. 64 girdinin 63'ü DOI ya da arXiv kimliği artı ikinci bir kaynakla (yayın yeri sayfası, OpenAlex, Crossref, PMLR/NeurIPS/AAAI/USENIX sayfası) doğrulandı; kalan bir girdi (`sahin2026behavioral`) yazarın kendi bildirisidir ve yalnızca depo içi kaynakla (`paper/bildiri/bildiri.tex` başlık ve yazarları) eşleşti, dış dizinlerde bulunamaz (UNCERTAIN, beklenen durum). Betiğin 29 NOT_FOUND ve 20 TITLE_MATCH_NO_DOI sınıfı, ezici çoğunlukla "DOI'siz konferans bildirisi" olmasından kaynaklanıyordu; hepsi tek tek çözüldü. Betiğin önerdiği aday DOI'lerin bir kısmı yanlış makaleyi gösteriyordu (örneğin `fu2022patchfool` için Gu ve ark.nın DOI'si, `naseer2022improving` için başka bir makale, `zhu2024enhancing` için TGR makalesi); bu adaylar KULLANILMADI.

Künyede gerçek düzeltme gerektiren 15 kayıt var (sayfa aralığı, yazar parçacığı, tür, başlık büyük harf koruması, cilt no). En sık görülen sorun: CVPR/ICCV makalelerinde sayfa numaraları CVF Open Access baskısından alınmış, DOI ise IEEE Xplore baskısını gösteriyor (5 kayıt). DOI eklendiğinde sayfa aralığı da IEEE baskısına çevrildi (kanıt Crossref).

Atıf–bağlam uyumunda 3 kırmızı (🔴), 10 sarı (🟡) bulgu var. En ağır olan: girişteki "CNN'den ViT'ye mi tersi mi" cümlesi TREND makalesine (yalnızca CNN'ler, hiç ViT yok) dayandırılmış; ayrıca ilgili çalışmalarda Shao ve Bhojanapalli'ye kaynağın söylemediği nedenler yüklenmiş. Hiçbir cümle değiştirilmedi; öneriler aşağıda ve "yazara devredilen cümleler" bölümünde.

Bir de içerik bulgusu var, atıf hatası değil: Mahmood, Benz ve Shao'nun üçü de CNN→ViT aktarımını ViT→CNN'den zayıf buluyor. Makalenin ana yönü tersidir. Tartışma bölümü yalnızca Mahmood'u anıyor; Benz ve Shao da anılmalı (bkz. Ö1).

Uyarı: denetim sırasında `01_introduction.tex`, `02_related_work.tex`, `03_methodology.tex` dosyaları başka bir oturum tarafından düzenlendi (commit edilmemiş fark var). Aşağıdaki dosya:satır numaraları 2026-09-30 öğleye yakın anki çalışma kopyasına aittir; cümleler alıntılandığı için kayma olsa da bulunabilir.

## 1. Sınıf sayıları, önce ve sonra

| Class | Before (betik.json) | After (this audit) |
|---|---|---|
| VERIFIED (DOI or arXiv id plus second source) | 13 | 63 |
| TITLE_MATCH_NO_DOI | 20 | 0 |
| NOT_FOUND | 29 | 0 |
| GRI_LIT (grey literature) | 2 | 0 (timm: DataCite DOI resolves; CIFAR tech report: author page; both counted VERIFIED) |
| SUSPECT | 0 | 0 |
| HALLUCINATED | 0 | 0 |
| UNCERTAIN | 0 | 1 (`sahin2026behavioral`, self-citation, internal source only) |
| Total | 64 | 64 |

Context classes are separate from existence classes: 3 red, 10 yellow, remainder green (section 4).

## 2. Changed keys (nothing removed, nothing renamed)

No key was deleted or renamed, so no `.tex` file needs to change for the bibliography to compile. `bibtex` with IEEEtran.bst on a scratch copy: 64 entries, zero warnings, ghost/orphan check clean.

| Key | Change | Reason and evidence |
|---|---|---|
| xie2020adversarial | pages 819--828 to 816--825, DOI added | Crossref 10.1109/CVPR42600.2020.00090 gives IEEE pagination; old pages were CVF Open Access pagination. https://api.crossref.org/works/10.1109/CVPR42600.2020.00090 |
| bhojanapalli2021understanding | pages 10231--10241 to 10211--10221, DOI added | Crossref 10.1109/ICCV48922.2021.01007 (OpenAlex lists both paginations). |
| mahmood2021robustness | pages 7838--7847 to 7818--7827; "Van Dijk" to "van Dijk"; DOI added | Crossref 10.1109/ICCV48922.2021.00774; arXiv 2104.02610 lists "Marten van Dijk". |
| moosavi2017universal | pages 1765--1773 to 86--94, DOI added | Crossref 10.1109/CVPR.2017.17 (CVF pagination was in the old entry). |
| ma2023transferable | pages 4630--4639 to 4607--4616, DOI added | Crossref 10.1109/ICCV51070.2023.00427. |
| guo2018countering | "Van Der Maaten" to "van der Maaten" | arXiv 1711.00117 author list; fixes BibTeX sort/particle handling. |
| krizhevsky2009learning | "and others" removed | The report has two authors (Krizhevsky, Hinton); author page https://www.cs.toronto.edu/~kriz/cifar.html |
| bai2021transformers | title `CNNs` protected as `{CNNs}` | IEEEtran lowercases unprotected titles; the compiled `main.bbl` printed "cnns". Defect visible in the PDF today. |
| paul2022vision | volume 36, number 2, DOI added | Crossref 10.1609/aaai.v36i2.20103. |
| li2023tabench | pages 41707--41726, DOI added | Crossref 10.52202/075280-1807. |
| lyu2024adaptive | pages 134043--134074, DOI added | Crossref 10.52202/079017-4260. |
| tramer2020adaptive | volume 33 added | NeurIPS 2020 = vol. 33, https://proceedings.neurips.cc/paper/2020/hash/11f38f8ecd71867b42433548d1078e38-Abstract.html |
| vaswani2017attention | `@article` to `@inproceedings`, booktitle | NeurIPS is a proceedings, not a journal; IEEEtran printed it without "in". |
| rw2019timm | URL to github.com/huggingface/pytorch-image-models, `{PyTorch}` protected, stray `journal`/`publisher` removed, note on old URL | Repository moved (old URL answers 301); DOI 10.5281/zenodo.4414861 resolves at DataCite (title "rwightman/pytorch-image-models", concept record). |
| demontis2019adversarial | `{E}xplaining` protected | BibTeX does not capitalise after "?"; the title printed "explaining" lowercase. |

Additional non-substantive edits (all 64 entries touched by re-serialisation, values preserved; verified by a field-by-field diff script):

- Booktitles harmonised to one form per venue: `Proc. International Conference on Learning Representations ({ICLR})`, `... Machine Learning ({ICML})`, `Advances in Neural Information Processing Systems ({NeurIPS})`, `Proc. IEEE/CVF Conference on Computer Vision and Pattern Recognition ({CVPR})` (pre-2018 papers without "/CVF"), `... International Conference on Computer Vision ({ICCV})`, `... Winter Conference on Applications of Computer Vision ({WACV})`, `Proc. AAAI Conference on Artificial Intelligence ({AAAI})`, `Proc. IEEE Conference on Secure and Trustworthy Machine Learning ({SaTML})`, `Proc. British Machine Vision Conference ({BMVC})`, `Proc. European Conference on Computer Vision ({ECCV})` (series/volume/publisher of the two LNCS entries kept), `Proc. IEEE Symposium on Security and Privacy ({SP})`, `Proc. 28th USENIX Security Symposium (USENIX Security 19)`. RobustBench: `Advances in Neural Information Processing Systems ({NeurIPS}), Datasets and Benchmarks Track`.
- 18 `doi` fields added where Crossref returned an exact title and author match (carlini2017towards, he2016deep, zagoruyko2016wide, jain2024towards, zhang2023tgr, benz2021adversarial, waseda2023closer, yu2025reliable, debenedetti2023light, mo2022adversarial, plus the eight above). IEEEtran.bst has no DOI field, so nothing prints; this is provenance for future audits.
- `eprint` fields (arXiv ids, all checked against the arXiv API title and author list) added to 53 entries for the same reason. Also ignored by IEEEtran.
- Entries deliberately left as `@article` with `journal={arXiv preprint ...}`: papernot2016transferability, gowal2020uncovering, carlini2019evaluating. All three are arXiv-only as of today (RobustBench lists Gowal as "arXiv, Oct 2020").
- Key/year mismatches left alone because `.tex` files cite the keys: loshchilov2017decoupled (ICLR 2019), loshchilov2016sgdr (ICLR 2017), zhao2025revisiting (TPAMI 48(1), Jan 2026; DOI year 2025 online first), zhu2024, others are correct.

## 3. Resolution of the script's SUSPECT / NOT_FOUND / NO_ID records

The script has no class named SUSPECT in this run; the non-VERIFIED classes were NOT_FOUND (29), TITLE_MATCH_NO_DOI (20), GRI_LIT (2). Resolution:

- 20 TITLE_MATCH_NO_DOI: exact title and author match on the candidate DOI, confirmed by fetching each DOI from Crossref. Two mismatches on pages (see section 2). One candidate was wrong: `vaswani2017attention` candidate 10.65215/ysbyhc05 is not the NeurIPS paper; not used.
- 29 NOT_FOUND: every one is a DOI-less proceedings paper or arXiv-only paper. Resolved through arXiv API (title, author list, order), OpenAlex (venue, year, pages) and proceedings pages. The candidate DOIs the script proposed belong to different papers in all 29 cases (e.g. croce2020reliable to a 2026 healthcare paper, chalasani2020concise to a Russian journal item) and were ignored. Papers checked against a proceedings page: MART (ICLR 2020 poster page), Loshchilov (ICLR 2019/2017 OpenReview), Tramer 2020 (NeurIPS 33), Raghu (NeurIPS 34 pp. 12116--12128), Bai (NeurIPS 34, pp. 26831--26843), Rice (PMLR 119 pp. 8093--8104), Chalasani (PMLR 119 pp. 1383--1391, author order Wu before Jha confirmed), Demontis (USENIX Sec 19 pp. 321--338), Shao (TMLR, Oct 2022), Fu (ICLR 2022), Zhu (ICLR 2024, proceedings.iclr.cc), Jain (CVPR 2024 pp. 24736--24745, CVF page), Wu (AAAI 39(1) pp. 886--894).
- 2 GRI_LIT: rw2019timm (DataCite record resolves; the earlier "404 at Crossref" was the wrong registry); krizhevsky2009learning (author page lists the tech report).
- netzer2011reading, NOT_FOUND by the script: the SVHN page http://ufldl.stanford.edu/housenumbers/ lists the paper (NIPS Workshop 2011). Verified.
- sahin2026behavioral: title and both authors match `paper/bildiri/bildiri.tex` lines 16 to 26; no external index (ATEEC 2026 proceedings not yet public). UNCERTAIN by rule, no action needed; the manuscript already says "submitted".

## 4. ATIF–BAĞLAM UYUMU

Method: for each cited source I read the abstract from the publisher/arXiv page and, for every claim that depends on more than the abstract, the full text (arXiv PDF converted locally with `pdftotext`; web summaries of PDFs were not trusted after one of them returned a fabricated "quote" for TREND). Severity: 🔴 misreports the source, 🟡 weak or over-stated, 🟢 appropriate. Line numbers are of the working copy at audit time. The Turkish mirror (`paper/manuscript_tr/sections/`) carries the same citations; mirror lines are given in brackets where relevant.

### 4.1 Findings that need action

| # | Sev | File:line | Sentence (quoted) | What the source actually says | Suggested fix (writer decides) |
|---|---|---|---|---|---|
| A1 | 🔴 | 01_introduction.tex:9 [tr 01_giris:9] | "studies of cross-architecture transfer likewise disagree on whether attacks move more easily from CNNs to ViTs or the reverse~\cite{mahmood2021robustness, ravikumar2023trend, naseer2022improving}" | Ravikumar et al. (TREND, arXiv 2008.01524) study CNNs only (VGG11, VGG11BN, ResNet18 and relatives, CIFAR and ImageNet); the word "transformer" does not occur in the paper. It says nothing on CNN to ViT direction. Mahmood et al. (Sec. 4.3): BiT-M-50x1 to ViT-L-16 fools ViT-L-16 5.7/15.5/11.8% (CIFAR-10/100/ImageNet), ViT-L-16 to BiT fools 42.5/47.6/34.3%, so CNN to ViT is the weaker direction. Naseer et al.: conventional attacks from ViTs "show very low black-box transferability", ViT to CNN "only moderate". Benz et al. (Sec. 5, Table 4): "the transferability from CNN to ViT is often lower than 20%, while the opposite scenario is higher". Shao et al. (Sec. 5.2.2, Fig. 4): CNN sources give low error rate on ViT targets, ViT sources give higher. | Remove `ravikumar2023trend` from this citation. Add `benz2021adversarial` and `shao2022adversarial` (both already in the .bib). Reconsider "disagree": Mahmood, Benz and Shao agree with each other that CNN to ViT is weaker, which is the opposite of this paper's direction; the disagreement is between them and this paper, plus Naseer's weak ViT-sourced transfer. |
| A2 | 🔴 | 02_related_work.tex:54 [tr 02_ilgili_calismalar:54] | "Shao et al. demonstrated that adversarial training can improve ViT robustness and that ViT features rely less on high-frequency content, though challenges remain due to training instability." | Abstract: "adversarial training is also applicable to ViT for training robust models"; features "contain less high-frequency patterns". "Training instability" appears nowhere in the paper (text search for instab-/unstable/difficult: none in this sense). Appendix F is a 20-epoch preliminary run in which ViT-B/4 does not beat WideResNet-34-10; authors "conjecture ViT may need larger training data or longer training". The headline result (ViTs more robust than CNNs and MLP-Mixer in white-box and transfer settings) is not mentioned. | "...showed that adversarial training is applicable to ViTs, although in a preliminary CIFAR-10 run the ViT did not improve on a large CNN." Drop the instability clause or attribute it to a source that makes it. |
| A3 | 🔴 | 02_related_work.tex:52 [tr :52] | "Initial studies suggested that ViTs exhibit some inherent robustness properties due to their global receptive field~\cite{bhojanapalli2021understanding}." | Abstract: "when pre-trained with a sufficient amount of data, ViT models are at least as robust as the ResNet counterparts on a broad range of perturbations". No attribution to a global receptive field; "global" occurs only in an ablation that restricts attention to local patches. The pre-training condition is dropped in the sentence. | "...found ViTs at least as robust as ResNets across many perturbations when pre-trained on enough data." |
| A4 | 🟡 | 02_related_work.tex:54 [tr :54] | "Jain et al. proposed Adaptive Attention Scaling Adversarial Training (AAS-AT) to address ViT-specific training challenges, achieving state-of-the-art robustness on CIFAR-10 and ImageNet-100" | The paper's main contribution is a diagnosis: softmax underflow in attention causes gradient masking, so PGD/CW/GAMA are sub-optimal on ViTs; the AAS attack rescales pre-softmax outputs. AAS-AT applies that attack every few epochs and "outperforms" existing AT methods by 1.3--3.5 points on CIFAR-10 and improves ImageNet-100; no state-of-the-art claim. Wu et al. (cited in the same sentence) reach 74.97% on CIFAR-10. | Say "improves over existing ViT adversarial-training recipes by 1.3--3.5 points on CIFAR-10". Worth a sentence for this paper: the gradient-masking finding bears on PGD-only ViT evaluations (the paper also uses AutoAttack). |
| A5 | 🟡 | 02_related_work.tex:64 [tr :64] | "Chen et al. systematically analyze the factors affecting cross-architecture transferability, finding that architectural inductive biases, with CNNs preferring high-frequency information while ViTs favor low-frequency patterns, shape transfer success." | UNVERIFIED. The publisher page (ScienceDirect) returned 403; only a secondary abstract was reachable: the paper proposes an attack that exploits the differing inductive biases of CNNs and ViTs. The abstract does not mention frequency or a systematic factor analysis. The frequency preference is documented in Benz (ViT relies more on low frequency) and Shao. | Writer should check the full text. If the frequency statement is not in Chen, attribute it to `benz2021adversarial`/`shao2022adversarial`; describe Chen as an attack paper. |
| A6 | 🟡 | 02_related_work.tex:62 | "The transferability depends on factors including model architecture, training data, and attack methods~\cite{demontis2019adversarial}." | Abstract: two main factors, "the intrinsic adversarial vulnerability of the target model, and the complexity of the surrogate model", plus gradient alignment as a metric. Architecture, training data and attack method are not the paper's factors. | "depends on the target's intrinsic vulnerability and on the complexity of the surrogate model~\cite{demontis2019adversarial}". This is also the strongest external support for the paper's central mechanism (target weakness) and could be cited in section 5. |
| A7 | 🟡 | 02_related_work.tex:44 ; 04_experiments.tex:303 | "sparser~\cite{chalasani2020concise} gradients" ; "adversarial training sparsifies CNN gradients far more strongly, consistent with~\cite{chalasani2020concise}" | Chalasani et al. prove sparse attributions for 1-layer networks and show empirically that adversarially trained models give sparser *feature attributions* (Integrated Gradients, DeepSHAP). Raw input gradients are not what they measure. | "sparser feature attributions". Line 303 "consistent with" is fine once the object is named. |
| A8 | 🟡 | 02_related_work.tex:34 | "Adaptive Randomized Smoothing~\cite{lyu2024adaptive}, which improves certification radii through multi-step defenses" | Abstract: ARS certifies test-time *adaptive* models by composing several steps (f-DP analysis); reports +1 to +15 points standard test accuracy on the authors' CIFAR-10/CelebA adaptivity benchmarks and up to +1.6 points certified accuracy on ImageNet. No statement about certification radii. | "extends randomized smoothing to certify test-time adaptive, multi-step models". |
| A9 | 🟡 | 03_methodology.tex:118 ; 02_related_work.tex:74 ; 05_discussion.tex:15 | "Conditioning transfer evaluation on correctly classified samples follows established practice~\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, zhao2025revisiting}" (introducing the target-correct rate) | Liu: 100 images "classified correctly by all five models", reason stated. Dong: 1000 images correct for all seven models, reason stated ("less meaningful to study the success rates ... if the models cannot classify the original image correctly"). Zhao: 5000 images correct for all four models. Mahmood: per pair, m = 1000 examples "that both classifiers correctly identify". Ravikumar: pool correct for both source and target. All five use a jointly-correct pool; none conditions on the target alone, which is what the sentence is defining. (TA-Bench, cited elsewhere, also uses images correct for all victims.) | "Conditioning on jointly correct samples is established practice [...]; the target-correct rate is its one-sided relaxation." Keeps the citations, fixes the object. 03:118 also repeats mahmood/ravikumar for both-correct, which is accurate. |
| A10 | 🟡 | 02_related_work.tex:62 | "recent evaluation guidelines make such protocol choices explicit~\cite{zhao2025revisiting}" | Zhao et al.'s guidelines: plot transferability against iteration count; use fair hyper-parameters; measure stealthiness beyond one L_p norm. None concerns the conditioning set. The jointly-correct pool is a line in their experimental setup, not a guideline. | Drop the clause or say "systematic evaluations already select samples correctly classified by all models". |
| A11 | 🟡 | 03_methodology.tex:85 | "computed with the model in training mode so that attack generation and the parameter update see consistent batch-normalization statistics, following standard adversarial-training implementations~\cite{rice2020overfitting}" | The Rice et al. paper does not discuss BN mode. Their released code does: locuslab/robust_overfitting `train_cifar.py` calls `model.train()` and generates PGD inside the training loop (checked on GitHub raw file). So the claim is true of the code, not of the paper. | "as in the reference implementation of~\cite{rice2020overfitting}" or cite the repository. |
| A12 | 🟡 | 02_related_work.tex:42 | "The RobustBench leaderboard~\cite{croce2021robustbench} tracks state-of-the-art CNN robustness, with WideResNet variants achieving the highest robust accuracy on CIFAR-10." | The CIFAR-10 L_inf leaderboard is architecture-agnostic (99 entries fetched today; XCiT-L12/M12/S12 entries at 57.6/57.3/56.1% AutoAttack are on it). The top 12 are all WideResNet variants (75.28% MeanSparse WRN-94-16, 73.71% Bartoldson WRN-94-16, ...), so the second half is right. Gowal WRN-28-10 is listed at 62.80%; the paper's own table gives 62.76% (the reference sheet uses 62.76). | "tracks robust accuracy across architectures, with WideResNet variants at the top". |
| A13 | 🟡 | 05_discussion.tex:61 | "with diffusion-generated synthetic data ViTs have been reported to surpass WideResNets on CIFAR-10~\cite{wang2023better, wu2025vision}" | Only Wu et al. report a ViT surpassing WideResNets (ViT-B/2, 74.97% on CIFAR-10, +3.9 over previous best). Wang et al. is the WideResNet-with-diffusion-data baseline (WRN-70-16, 70.69%) that Wu et al. beat. | "[wu2025vision], building on the diffusion-data recipe of [wang2023better]". |

Note on the cross-cutting content point (Ö1 below): A1 is a citation error; the omission it exposes is separate.

Ö1. 05_discussion.tex:17 cites only Mahmood for the opposite direction. Benz (Table 4) and Shao (Fig. 4) report the same direction as Mahmood, on different model sets and datasets. A reviewer who knows those two papers will read the current text as if one paper disagreed with this one. Mahmood's direction claim as quoted in 05:17 ("finding transfer into the transformer weaker than transfer out of it") is accurate against their Sec. 4.3 and their both-correct protocol.

### 4.2 Citations checked and found appropriate (🟢)

| Key | Where | Check |
|---|---|---|
| bai2021transformers | 01:9, 02:52 | Abstract: fair comparison finds CNNs "can easily be as robust as Transformers" against adversarial attacks with Transformer training recipes; stronger OOD generalisation attributed to self-attention. Matches both sentences. |
| benz2021adversarial | 01:9, 02:52 | Abstract: ViT and MLP-Mixer, "especially ViT", more robust than CNNs; robust ViTs rely more on low-frequency features. Matches "linked the differences to frequency preferences". |
| mahmood2021robustness | 02:52, 02:64, 03:118, 05:17 | Both-correct protocol confirmed (Eq. 3, m = 1000 jointly correct); low CNN to ViT transferability confirmed; white-box vulnerability of ViTs confirmed. |
| naseer2022improving | 02:64, 02:76, 01:9 | ViT-sourced conventional attacks transfer poorly; self-ensemble and token refinement are the two proposed remedies. |
| wei2022towards | 02:64 | PNA (bypass attention gradients) and PatchOut (patch subset) are the two components. |
| zhang2023tgr | 02:64, 03:137, 04:421, 05 | Token-gradient regularisation eliminates extreme back-propagated gradients in attention, QKV and MLP paths. Sec. 3 already states the adaptation departs from the published scheme. |
| ma2023transferable, zhu2024enhancing | 02:64, 02:54 | Titles and abstracts match the one-line descriptions. |
| waseda2023closer | 02:64 | "same mistake" versus "different mistake" classes; different mistakes "occur even between similar models". |
| li2023tabench | 02:62 | 30+ methods, 25 substitute/victim models on ImageNet. |
| yu2025reliable | 02:62 | Transferability "often overestimated" when tested on CNNs only; three protocols (hard-ensemble, count of fooled targets, all targets fooled). Matches the description exactly. |
| ravikumar2023trend | 02:62, 03:118, 05:15 | Metric T = f_st / f_ss over the subset "correctly classified by both the source and the target model", "to account for differences in accuracies". The Sec. 3 description of Eq. (1) is accurate. Only the intro use (A1) is wrong. |
| liu2017delving, dong2018boosting | 02:62 individually | Both state the reason for restricting to correctly classified images. Only the grouping in A9 needs a wording change. |
| paul2022vision | 02:54 | Corruptions, perturbations, distribution shift, natural adversarial examples; masking analysis stands for occlusion. |
| carlini2019evaluating, tramer2020adaptive | 02:74 | Failure modes of evaluation; 13 defenses from ICLR/ICML/NeurIPS broken by adaptive attacks. |
| raghu2021vision | 02:52, 04:359 | Layer-wise CKA representation comparison of ViTs and CNNs. |
| gu2022vision, fu2022patchfool | 02:52, 04:403, 05:27 | Gu: attention "can be easily fooled to focus more on the adversarially perturbed patches". Fu: Patch-Fool attacks the self-attention mechanism through a single patch. Both patch threat models, as the text says. |
| pinto2022impartial, ali2024adversarial | 02:72 | Pinto: unfairness of CNN vs Transformer comparisons; Ali: IEEE Access 12, direct ViT/CNN comparison. |
| zhang2019theoretically | 02:28, 03:85, 04:145 | Paper eq. (1): R_rob = R_nat + R_bdy, so "natural-plus-boundary decomposition" is correct and the mapping to r_raw = e + r_cond (1 - e) is exact. Nit for 04:145: it is the robust error that is defined by an existential quantifier over the neighbourhood (so a clean-misclassified point counts with delta = 0); R_bdy is defined through the neighbourhood of the decision boundary. "the boundary term is defined by an existential quantifier" would read more precisely as "the robust error is". |
| hurley2009comparing | 03:121, 05:25 | Scaling axiom D2 ("sparsity is scale invariant") holds for Hoyer and Gini; Gini alone satisfies all six criteria. Text says "axioms" (plural); D2 is the scale-invariance one. Also useful for 05:25: the paper's assumption A1 states that sparsity is unchanged under any permutation of the coefficients, which is exactly why sparsity cannot say anything about spatial layout. |
| moosavi2017universal | 05:31 | Universal perturbations rely on correlated decision-boundary normals lying in a low-dimensional subspace; consistent with "shared sensitivity axes". The signed-cosine argument in 03:125 is the paper's own. |
| chalasani2020concise | existence, direction | Adversarial training gives sparser attributions (object wording in A7). |
| tsipras2019robustness | 02:44 | Gradients of adversarially trained models "align well with human perception". |
| gowal2020uncovering | 03:46, 04:34, 04:41, 05, main.tex:120 | WRN-28-10 with 500K extra pseudo-labelled images; 89.48 clean, 62.76 in the paper's table. |
| croce2021robustbench | 03:32, 03:46, 04:34, main:120 | epsilon = 8/255 L_inf is the RobustBench standard; checkpoint distribution confirmed (`Gowal2020Uncovering_28_10_extra`). Only 02:42 needs a wording change (A12). |
| croce2020reliable | 02:51, 03:72 | APGD-CE, APGD-T, FAB-T, Square = standard AutoAttack. |
| debenedetti2023light, mo2022adversarial | 03:50, 05:61 | Both report ViT adversarial-training results are recipe-sensitive. |
| xie2020intriguing, xie2020adversarial, wu2020skip | 02:80 | Two-domain BN hypothesis (mixture statistics), auxiliary BN branches in AdvProp, skip-connection gradients for transferability. |
| papernot2016transferability, madry2018towards, goodfellow2015explaining, carlini2017towards, wang2020improving, guo2018countering, cohen2019certified, tramer2018ensemble, he2016deep, zagoruyko2016wide, dosovitskiy2021image, vaswani2017attention, loshchilov2017decoupled, loshchilov2016sgdr, rw2019timm, krizhevsky2009learning, netzer2011reading, szegedy2014intriguing, bhojanapalli (existence), sahin2026behavioral | various | Standard uses; descriptions match the sources. |

### 4.3 Sentences handed to the writer (not changed)

A1 (01:9), A2 (02:54), A3 (02:52), A4 (02:54), A5 (02:64), A6 (02:62), A7 (02:44, 04:303), A8 (02:34), A9 (03:118, 02:74), A10 (02:62), A11 (03:85), A12 (02:42), A13 (05:61), plus Ö1 (05:17, add Benz and Shao). The Turkish mirror has the same sentences at the bracketed positions and needs the same edits: 01_giris:9, 02_ilgili_calismalar:34, 42, 44, 52, 54, 62, 64, 74; 03_yontem:82 (rice), 116; 04_deneyler:299; 05_tartisma:15, 17, 61.

### 4.4 Uygulama kaydı (2026-09-30 öğleden sonra, ana oturum)

A1–A13 ve Ö1 hem EN hem TR metne uygulandı; betikler `arsiv/b2_yardimci/_atif_baglam_en.py` ve `_atif_baglam_tr.py` (her eski dize tam bir kez eşleşti, 16/16 + 16/16). Notlar:

- A1: TREND (arXiv 2008.01524) özeti ana oturumca yeniden okundu; dönüştürücü/ViT sözcüğü geçmiyor, yön iddiası yok. Giriş cümlesi yeniden kuruldu: Mahmood, Benz ve Shao ViT→CNN yönünü daha kolay bulur; Naseer ViT kaynaklı geleneksel saldırıların zayıf transferini bildirir; bu makalenin yönü ilk grubun tersidir ve Bölüm 5'e bağlandı.
- A4: Jain'in 1,3–3,5 puanlık sayıları metne alınmadı (nitel: "mevcut ViT tariflerini geçer"); gradyan maskeleme bulgusu ve AutoAttack'ın gradyansız Square bileşeninin kısmi güvencesi eklendi.
- A5: Chen ve ark. özetine Semantic Scholar, Crossref, OpenAlex ve Elsevier yönlendirmesi üzerinden ulaşılamadı (özet alanı boş / 403). OpenAlex anahtar kelimesi "inductive bias" ile uyumlu olarak saldırı makalesi diye anıldı; frekans tercihi Benz ve Shao'ya bağlandı. Tam metin erişimi olunca yeniden bakılmalı.
- A9: 03:118 ve 02:74 düzeltildi; 05:15 genel ifade olduğundan bırakıldı. `paper/bildiri/bildiri.tex:57` bilinçli olarak DEĞİŞTİRİLMEDİ: ATEEC bildirisi gönderilmiş durumda.
- Ö1 + A6: 05:17'ye Benz ve Shao eklendi; hedef-kırılganlığı mekanizması Demontis'in ilk etkenine bağlandı.
- `paper/bildiri/bildiri.bib` `extract_bib.py` ile yeniden üretildi (26 girdi).

## 5. Ghost / orphan / duplicate

- Cited in text but missing from the .bib (orphans): none.
- In the .bib but never cited (ghosts): none. 64 keys, 64 cited (main.tex plus six section files, comments excluded).
- Same work under two keys: none. No duplicate keys. Near-duplicate check on DOI, arXiv id and title: none.
- Self-citation rate: 1 of 64 (`sahin2026behavioral`, the preliminary version; disclosed in 01_introduction.tex).
- Ordering: `\bibliographystyle{IEEEtran}` with the `cite` package orders by first citation; nothing to change in the .bib.

### Other files sharing the bibliography

- `paper/manuscript_tr/main.tex` uses `\bibliography{../manuscript/references}`, so it picks up the corrected file automatically. Its cites mirror the English text (positions listed in section 4.3).
- `paper/bildiri/bildiri.bib` is a generated copy (25 entries, `paper/bildiri/extract_bib.py`, last written 31 Jul). It was already stale before this audit for three entries (goodfellow2015explaining, krizhevsky2009learning, rw2019timm). After today's corrections it lacks the fixed pages, DOIs and booktitles for the entries it copies. Not regenerated (not requested): run `python3 paper/bildiri/extract_bib.py` from WSL. All 25 keys exist in `references.bib`; `bildiri.tex` line 57 repeats the "established practice" citation of A9 (liu, dong, mahmood, ravikumar), so A9 applies there too.

## 6. Format (IEEEtran)

- Required fields are present for every entry type (checked by bibtex: zero warnings). `@techreport` (krizhevsky) has institution; `@misc` (timm) has howpublished and note.
- No URL-only entries. `rw2019timm` has a DOI and a URL; `krizhevsky2009learning` is a tech report without URL (optional).
- Title capitalisation: IEEEtran lowercases titles, so acronyms need braces. Defects found in the compiled `main.bbl`: "cnns" (bai2021), "Pytorch" (timm), "explaining" after a question mark (demontis). Fixed. Existing protections ({RobustBench}, {SGDR}, {CNN}, {Transformer}, {WideResNets}, {MLP-Mixer}, {TREND}, {Patch-Fool}, {ResNets}, {ResNet-18}, {ViT-Tiny}, {CIFAR-10}) confirmed to print correctly.
- Abbreviation consistency: mixed forms of ICLR/ICML/NeurIPS/CVPR/AAAI/SaTML/BMVC/ECCV harmonised (list in section 2). Ordinal prefixes ("37th", "40th", "32nd") removed; USENIX keeps "28th" because it is part of the official name.
- Left as is: `Proc. ATEEC 2026` and `NIPS Workshop on Deep Learning and Unsupervised Feature Learning` (the workshop's name at the time).

## 7. Verified reference map (for incremental re-audits)

Key, DOI (Crossref-resolved) and arXiv id (arXiv API title/author match). "-" means none exists.

| Key | DOI | arXiv |
|---|---|---|
| szegedy2014intriguing | - | 1312.6199 |
| goodfellow2015explaining | - | 1412.6572 |
| madry2018towards | - | 1706.06083 |
| carlini2017towards | 10.1109/SP.2017.49 | 1608.04644 |
| croce2020reliable | - | 2003.01690 |
| papernot2016transferability | - | 1605.07277 |
| demontis2019adversarial | - | 1809.02861 |
| zhang2019theoretically | - | 1901.08573 |
| wang2020improving | - | (OpenReview rklOg6EFwS, ICLR 2020) |
| tramer2018ensemble | - | 1705.07204 |
| guo2018countering | - | 1711.00117 |
| cohen2019certified | - | 1902.02918 |
| he2016deep | 10.1109/CVPR.2016.90 | 1512.03385 |
| zagoruyko2016wide | 10.5244/C.30.87 | 1605.07146 |
| xie2020adversarial | 10.1109/CVPR42600.2020.00090 | 1911.09665 |
| dosovitskiy2021image | - | 2010.11929 |
| vaswani2017attention | - | 1706.03762 |
| bhojanapalli2021understanding | 10.1109/ICCV48922.2021.01007 | 2103.14586 |
| mahmood2021robustness | 10.1109/ICCV48922.2021.00774 | 2104.02610 |
| shao2022adversarial | - | 2103.15670 |
| paul2022vision | 10.1609/aaai.v36i2.20103 | 2105.07581 |
| naseer2022improving | - | 2106.04169 |
| croce2021robustbench | - | 2010.09670 |
| loshchilov2017decoupled | - | 1711.05101 |
| loshchilov2016sgdr | - | 1608.03983 |
| rw2019timm | 10.5281/zenodo.4414861 (DataCite) | - |
| moosavi2017universal | 10.1109/CVPR.2017.17 | 1610.08401 |
| jain2024towards | 10.1109/CVPR52733.2024.02336 | - |
| zhang2023tgr | 10.1109/CVPR52729.2023.01575 | 2303.15754 |
| ma2023transferable | 10.1109/ICCV51070.2023.00427 | - |
| zhu2024enhancing | - | - (ICLR 2024, proceedings.iclr.cc) |
| lyu2024adaptive | 10.52202/079017-4260 | 2406.10427 |
| pinto2022impartial | 10.1007/978-3-031-19778-9_27 | 2207.11347 |
| ali2024adversarial | 10.1109/ACCESS.2024.3435347 | - |
| wu2025vision | 10.1609/aaai.v39i1.32073 | - |
| raghu2021vision | - | 2108.08810 |
| benz2021adversarial | 10.5244/C.35.68 | 2110.02797 |
| wang2023better | - | 2302.04638 |
| ravikumar2023trend | 10.1109/TAI.2022.3175172 | 2008.01524 |
| liu2017delving | - | 1611.02770 |
| dong2018boosting | 10.1109/CVPR.2018.00957 | 1710.06081 |
| li2023tabench | 10.52202/075280-1807 | 2311.01323 |
| waseda2023closer | 10.1109/WACV56688.2023.00141 | 2112.14337 |
| yu2025reliable | 10.1109/SaTML64287.2025.00049 | 2306.08565 |
| zhao2025revisiting | 10.1109/TPAMI.2025.3610085 | 2310.11850 |
| wei2022towards | 10.1609/aaai.v36i3.20169 | 2109.04176 |
| gowal2020uncovering | - | 2010.03593 |
| chalasani2020concise | - | 1810.06583 |
| hurley2009comparing | 10.1109/TIT.2009.2027527 | 0811.4706 |
| tsipras2019robustness | - | 1805.12152 |
| fu2022patchfool | - | 2203.08392 |
| gu2022vision | 10.1007/978-3-031-19775-8_24 | 2111.10659 |
| wu2020skip | - | 2002.05990 |
| xie2020intriguing | - | 1906.03787 |
| chen2023understanding | 10.1016/j.ins.2023.119474 | - |
| bai2021transformers | - | 2111.05464 |
| rice2020overfitting | - | 2002.11569 |
| debenedetti2023light | 10.1109/SaTML54575.2023.00024 | 2209.07399 |
| mo2022adversarial | 10.52202/068431-1351 | 2210.07540 |
| sahin2026behavioral | - | - (internal: paper/bildiri/bildiri.tex) |
| netzer2011reading | - | - (ufldl.stanford.edu/housenumbers) |
| carlini2019evaluating | - | 1902.06705 |
| tramer2020adaptive | - | 2002.08347 |
| krizhevsky2009learning | - | - (cs.toronto.edu/~kriz/cifar.html) |

## 8. Limits of this audit

- Chen et al. (2023, Information Sciences) full text and abstract were not reachable (publisher 403); existence and künye are verified through Crossref (DOI, volume, article number), the content claim is not (A5).
- Jain, Wu and Zhu have no arXiv version; their contents were checked against the CVF page, the AAAI page and the ICLR proceedings page, and for Jain against the CVF PDF.
- Incoming-direction statements (A1) were checked in the papers' own tables and figure captions, not in abstracts.
- Sections 01, 02, 03 were being edited by another session during this audit (uncommitted diff). If those edits rewrite a flagged sentence, the finding still applies to the underlying claim; re-run `grep -n` on the quoted phrase.
