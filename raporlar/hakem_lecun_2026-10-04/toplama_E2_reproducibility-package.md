# E2 dossier: reproducibility package (lens E, evidence only)

Snapshot audited: `/home/firat/projects/adeb_sci_1/teslim/acik_depo/cnn-vit-robustness-protocols/` (git HEAD a8b138c, single commit; its message says "Snapshot of the private working repository at revision dc0168f"; main repo HEAD is now ded2356). Audit date 2026-10-04. Paths below are relative to the snapshot unless prefixed `MAIN:` (= /home/firat/projects/adeb_sci_1). README line numbers are approximate (section names given).

## Summary (10 lines)

1. Every path the README names exists in the snapshot, except `paper/manuscript/`, which the README itself says is not included (T1).
2. `python scripts/build_reference_sheet.py` run inside the container from the snapshot: clean exit, snapshot `git status` unchanged, `diff` against `MAIN:results/C1_REFERANS_FOYU.md` empty (byte-identical) (T2).
3. The four protocol masks in `src/analysis/protokoller.py` match the prose in 03_methodology.tex; I recomputed all four rates, both directions, from `results/c1_transfer/pair*/per_sample_*.npz` with that module and they equal Table III (T3).
4. No script in the snapshot imports `protokoller.py`; the README calls it "the single definition" (T3-F3c).
5. Seeds 1001-1003, 2001-2003, 777, 42 and (42,123,456) are in code/records; the training launchers are not, and the shipped config yaml (lr 0.01, 25 epochs) differs from the paper recipe (lr 1e-3, up to 100 epochs) (T4).
6. Personal/internal strings: git author e-mail cagrisahin58@gmail.com; `/workspace` paths in 3 files plus `/workspace/logs/...` in `results/q1/e2/e2_audit.json`; Turkish docstrings/labels; run2/run3 names in 4 experiment scripts, in KOKEN.json, and hard-coded earlier-checkpoint literals in the sheet builder (T5, T6).
7. Licenses: LICENSE is MIT; CC BY 4.0 for the records appears only as one README sentence, with no license file (T7).
8. Of 11 tables, the sheet regenerates the CIFAR-10 ones; CIFAR-100, SVHN, L2 and calibration numbers exist as stored summaries plus per-sample npz but no snapshot script aggregates them (MAIN has about 67 `q1_*`/`c1_*` scripts, not copied); earlier-checkpoint blocks have no records (T9).
9. Of the 8 included figure files only fig3 and fig5b regenerate from the snapshot (I ran them); fig2 fails (missing `results/wrn_eval/`), fig_protocol_sets plot fails (needs main.aux), fig4/fig4b/fig5 need checkpoints, the overview figure has no source in the snapshot, `paper/figures/final/` holds only `.gitkeep` (T10).
10. Data and Code Availability over-promise candidates ("scripts that generate every table and figure", "reproduce every number reported here") are itemised in T11; not found: earlier-checkpoint records, training launchers, wrn_eval records, overview-figure source, any proof the GitHub remote exists.

Housekeeping: my test runs created root-owned `paper/figures/raw/`, `__pycache__` and figure PDFs inside the snapshot; all were removed through docker. Final `git status --short` of the snapshot is empty and `paper/figures/final/` holds only `.gitkeep`.

---

## T1. README promises vs contents (README sections Layout, Seeds, Reproduce the numbers, Not included)

| # | README claim (quote) | Path | Exists | Detail |
|---|---|---|---|---|
| 1 | "`results/c1_*` ... per-sample clean/robust flags for every test image, model and seed; transfer, gradient, attention and depth-profile records" | results/c1_seeds, c1_transfer, c1_gradient, c1_c2..c5, c1_a3, c1_a5, c1_addenda, c1_drift, c1_eval, c1_eval_clean, c1_statval, c1_sweep | yes | file counts: c1_seeds 85 (72 npz, 3 csv, 10 json), c1_transfer 31, c1_c3 31, c1_gradient 9, c1_drift 9, c1_addenda 9, c1_c2 6, c1_c5 6, c1_eval 6, c1_eval_clean 6, c1_sweep 6, c1_a3 6, c1_c4 3, c1_a5 3, c1_statval 2; root JSON c1_eval_summary, c1_behavior_summary, c1_c45_summary |
| 2 | "`results/q1/` CIFAR-100 and SVHN replications, the L2 check, the checkpoint-selection ablation and the pre-registered pool fits" | results/q1 | yes | 598 files; 18 top-level JSON; subdirs cifar100, svhn, cifar10_l2, e2, e3_akolu, e3_akolu_v2, e3_points |
| 3 | "`results/C1_REFERANS_FOYU.md` Generated reference sheet. Every number in the paper is taken from this file" | results/C1_REFERANS_FOYU.md | yes | 141 lines; sections listed in T2 |
| 4 | "`src/analysis/protokoller.py` The single definition of the four conditioning protocols" | | yes | T3 |
| 5 | "`scripts/build_reference_sheet.py` Regenerates the reference sheet from the records" | | yes | 288 lines |
| 6 | "`scripts/generate_journal_figs_c1.py`, `paper/figures/fig_protocol_sets.py`, `scripts/fig_protokol_kumeleri_veri.py` Figure generators" | | yes (all 3) | run results in T10 |
| 7 | "`experiments/` Evaluation and analysis drivers (these need the checkpoints)" | experiments/ | yes | 15 .py files |
| 8 | "`src/`, `cli/`, `configs/` Training, attack and evaluation code" | | yes | configs: default.yaml, attacks/pgd.yaml, models/resnet18.yaml, models/vit_tiny.yaml, experiments/{cifar10_resnet_adv, cifar10_trades, cifar10_vit_native}.yaml; `cifar10_trades_v3.yaml` skipped as unreadable (MAIN:scripts/acik_depo_kur.sh comment) |
| 9 | "`data/val_split_indices*.json` The fixed validation split (seed 777)" | data/ | yes | 3 files: val_split_indices.json (split_seed 777, val_size 2000, n_train_total 50000), val_split_indices_cifar100.json (777, 2000, stratified true), val_split_indices_svhn.json (777, 2000, n_train_total 73257) |
| 10 | "`scripts/verify_manuscript_numbers.py` and `scripts/check_manuscript_claims.py` ... expect the manuscript sources under `paper/manuscript/`, which are not part of this repository" | | scripts yes; `paper/manuscript/` no | I ran both in the snapshot container: verify_manuscript_numbers.py ends "TOTAL: TOPLAM=158 EN_EKSIK=158 TR_EKSIK=158 ... UYARI: TR metni okunamadi ... SONUC: KALDI"; check_manuscript_claims.py ends "TOPLAM=45  KALAN=0" with lines "H1. A kolu B2 tanimiyla YENIDEN KOSULDU (116 nokta) GECTI" |
| 11 | "`pip install -r requirements.txt  # numpy, scipy, pandas and matplotlib suffice for the analysis`" | requirements.txt | yes | the file lists torch, torchvision, timm, numpy, tqdm, matplotlib, seaborn, pandas, torchattacks, autoattack, pyyaml, omegaconf, click; `scipy` is NOT listed although `scripts/build_reference_sheet.py:27` and `scripts/verify_manuscript_numbers.py:339` import it; README states no Python version |
| 12 | CITATION.cff, LICENSE | | yes | T7 |
| 13 | "Not included: Trained checkpoints (about 40 GB) and the archived adversarial examples ... (434 MB)" | models/, results/q1/adv_archive | absent | consistent with header of MAIN:scripts/acik_depo_kur.sh |

Size: 910 tracked files (`git ls-files | wc -l`); 23 MB working tree; .git 9.6 MB; 348 `.npz` per-sample files under results/.

## T2. Reference-sheet regeneration

| Item | Result |
|---|---|
| Command | `docker exec -w /workspace/teslim/acik_depo/cnn-vit-robustness-protocols adeb_eval python scripts/build_reference_sheet.py` |
| Output last line | "kaydedildi: /workspace/teslim/acik_depo/cnn-vit-robustness-protocols/results/C1_REFERANS_FOYU.md" |
| Snapshot `git status --short` after run | empty (file unchanged vs commit) |
| `diff results/C1_REFERANS_FOYU.md MAIN:results/C1_REFERANS_FOYU.md` | empty (identical) |
| ROOT handling | `scripts/build_reference_sheet.py:13` `ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` (patched by the kurucu script) |
| Inputs the builder reads | JSON summaries: `results/c1_eval_summary.json`, `c1_seeds/c1_seed_summary.json`, `c1_transfer/c1_transfer_summary.json`, `c1_c3/c3_summary.json`, `c1_behavior_summary.json`, `c1_c45_summary.json`, `c1_c2/pair*/tgr_summary.json`; per-sample npz only for the both-correct McNemar block (`results/c1_seeds/pair*/pgd_per_sample_*.npz`, `aa_chunk_*.npz`; build_reference_sheet.py:26-60) |
| Sheet sections | Tablo I (line 8), Tablo II (22), Tablo III (47), C3 (63), Gradyan yapisi (84), C4 (104), C5 (117), C2 (131) |
| Sections absent from sheet | CIFAR-100, SVHN, L2, checkpoint-selection, calibration arms (no `q1` string in build_reference_sheet.py) |
| README statements | "Every number in the paper is taken from this file"; "Everything needed to recompute that comparison is here" |

## T3. Four protocols: code vs prose

Code, `src/analysis/protokoller.py:21`: `PROTOKOLLER = ["raw", "target_correct", "both_correct", "successful_source"]`; masks at lines 58-63:

```
"raw": np.ones_like(tc, dtype=bool),
"target_correct": tc,
"both_correct": tc & sc,
# BEYAZ KUTU BASARISI = temizde dogru VE cekismelide yanlis.
"successful_source": tc & sc & sa,
```
(tc = target clean correct, sc = source clean correct, sa = source adversarial wrong). Non-canonical `successful_source_loose = tc & sa` at line 66 (diagnostic only; `TANI_PROTOKOLLERI`, line 31).

Prose, `MAIN:paper/manuscript/sections/03_methodology.tex:114`: "The base member is the \emph{target-correct} rate: among the samples that the target model classifies correctly on clean inputs, the fraction that becomes misclassified under adversarial examples crafted on the source model."
03_methodology.tex:118: "the raw misclassification rate $\frac{1}{n} \sum_{i} \mathbf{1}[f_T(x_{adv,i}^S) \neq y_i]$ includes the target's clean error"; "the \emph{both-correct} protocol, which conditions on samples that both the source and the target classify correctly"; "the \emph{successful-source} protocol, which conditions on target-correct samples whose attack succeeded on the source in the white-box sense"; about Ravikumar et al.: "over a pool restricted to samples both models classify correctly".
04_experiments.tex:119: "whether that phrase requires the source to classify the clean input correctly is a sub-choice that transfer studies rarely state."

Facts:
- F3a. The prose for successful-source (03:118) says "target-correct samples whose attack succeeded on the source in the white-box sense"; it does not itself state that the source must be clean-correct. The code mask requires it (`tc & sc & sa`). The module docstring (protokoller.py:1-22) records that until 2026-08-25 eight files used `tc & sa` and that this loose variant moves the CIFAR-10 asymmetry by "4,77 puan".
- F3b. Recomputation (script `raporlar/hakem_lecun_2026-10-04/_tmp/e2_recompute.py`, `protokol_oranlari(..., tani=False)`) over `results/c1_transfer/pair{1,2,3}/per_sample_{ResNet18_AT_to_ViT_Tiny_AT,ViT_Tiny_AT_to_ResNet18_AT}.npz` (keys: source_clean_correct, target_clean_correct, source_adv_wrong, target_adv_wrong), mean of 3 pairs:
  - ResNet->ViT: raw 41.02, target_correct 19.87, both_correct 18.25, successful_source 36.39
  - ViT->ResNet: raw 27.45, target_correct 15.51, both_correct 9.98, successful_source 17.02
  Sheet Tablo III (results/C1_REFERANS_FOYU.md lines 53-58) and paper `tab:transfer_protocols` (04_experiments.tex:95-98) show the same values.
- F3c. No `.py` in the snapshot imports `src.analysis.protokoller`: grep for `protokol_oranlari|import protokoller|analysis.protokoller` returns only the module's own definition and a docstring mention (`scripts/fig_protokol_kumeleri_veri.py:10`). That script restates `successful_source = tc & sc & sa` in a comment (line 14). `experiments/c1_c3_transfer_matrix.py:165-182` and `experiments/run_all_analyses_run2.py:178` only write the per-sample flags. README: "The single definition of the four conditioning protocols".
- F3d. protokoller.py has a Turkish docstring and Turkish `ETIKETLER` values ("Kosulsuz (ham)", "Hedef dogru", "Her ikisi dogru", "Basarili kaynak").

## T4. Seeds, split indices, configs named in the paper vs snapshot

| Paper statement (location) | In snapshot? | Evidence |
|---|---|---|
| "seed 777, indices stored with the code" (03_methodology.tex:100) | yes | data/val_split_indices.json `split_seed: 777`, `val_size: 2000`; cifar100 and svhn files likewise |
| "independent seeds (1001 to 1003 for ResNet-18, 2001 to 2003 for ViT-Tiny)" (03:100) | yes, in analysis code and record names | `scripts/build_reference_sheet.py:29`; `experiments/c1_c2_tgr.py:39`; `results/c1_seeds/pair2/pgd_per_sample_resnet18_s1002.npz`; dirs `results/q1/cifar100/{resnet18_s1001..vit_tiny_s2003}` |
| "three attack seeds (42, 123, 456) on a fixed subset" (03:156; 04:449) | yes | `results/c1_statval/statistical_validation.json:3-8` seeds [42,123,456], n_samples 1000 |
| "seed 42, including CUDA determinism flags" (03:158) | partly | `scripts/generate_journal_figs_c1.py` FIG_SEED=42 and CUBLAS_WORKSPACE_CONFIG; `seed: 42` in configs/default.yaml:5, cifar10_resnet_adv.yaml:4, cifar10_trades.yaml:4; `cli/train.py:23,119` default seed 42 |
| Training recipe "SGD LR 1e-3, cosine, up to 100 epochs; AdamW for ViT; clip 10; batch 128/64; patience 20, 0.1 pp" (03:97) | no single config matches | `configs/experiments/cifar10_resnet_adv.yaml`: lr 0.01, epochs 25, sgd, momentum 0.9, weight_decay 0.0005, cosine, batch_size 128, eps 0.031373, steps 10; cifar10_vit_native.yaml and cifar10_trades.yaml also present |
| Training launchers for seeds 1001-1003/2001-2003 | absent | grep for "1001"/"2001" over snapshot .py/.sh/.yaml finds only analysis PAIRS tables; snapshot `scripts/` has 6 files (build_reference_sheet, check_manuscript_claims, fig_protokol_kumeleri_veri, generate_journal_figs_c1, q1_e3_figur, verify_manuscript_numbers); MAIN:scripts has 233 files incl. train_robust.py, q1_devam.sh, auto_train_vit.sh (not copied); `src/training/{trainer,adversarial_trainer}.py` and `cli/train.py` are present |
| SVHN seeds | 2 pairs only | `results/q1/svhn/{resnet18_s1001,1002; vit_tiny_s2001,2002}`; paper `tab:svhn_protocols` caption "mean±std over two seed pairs" (04:224) |
| Hardware/software (04:459: "NVIDIA RTX 5090 ... PyTorch 2.6.0 with CUDA 12.8") | not in snapshot | requirements.txt has lower bounds only (`torch>=1.9.0`, `timm>=0.6.0`, `torchattacks>=3.4.0`) |
| Provenance box | present | `results/q1/KOKEN.json` lines 4-11: git_sha 2269d2655f03..., dal q1, `"calisma_agaci_kirli_mi": true`; per-artefact sha256 |

## T5. Personal paths, e-mails, Turkish-only internal notes

| Finding | Location |
|---|---|
| Author e-mail in git metadata | snapshot `git log`: "Cagri Sahin <cagrisahin58@gmail.com>"; body mentions "private working repository at revision dc0168f" |
| No `/home/firat`, `C:\Users`, `@gmail`, `@alparslan`, `@firat` strings in tracked text (outside .git; results JSON checked separately) | grep -rIn: none |
| `/workspace` container path | `scripts/check_manuscript_claims.py:26,30`; `paper/figures/fig_protocol_sets.py:18,357` (`docker exec -w /workspace adeb_eval ...`); `results/q1/e2/e2_audit.json:969,1011,1053,1095,1137,1179` (`"log": "/workspace/logs/Q1_e2_clean_*.log"`) |
| GitHub handle | CITATION.cff:12 `https://github.com/cagrisahin58/cnn-vit-robustness-protocols` |
| Turkish diacritics in code | scripts/q1_e3_figur.py (10 lines), check_manuscript_claims.py (21), verify_manuscript_numbers.py (1), generate_journal_figs_c1.py (11), src/analysis/protokoller.py (1); ASCII-Turkish docstrings/labels in many more (e.g. build_reference_sheet.py docstring; sheet headings "Tablo I: ana gurbuzluk", "Kosulsuz (ham)", "Eslesmis McNemar") |
| English gloss | README Layout section lists: temiz, gurbuz, ham, hedef dogru, her ikisi dogru, basarili kaynak, kosum, cift, tohum, yayilim, ozdeslik, secim |
| Turkish internal reports | none: `find . -name '*.md'` returns README.md and results/C1_REFERANS_FOYU.md only |
| Turkish notes inside data | `data/val_split_indices.json` `note`: "rev2 C1 ortak sabit val bolmesi; clean pretraining VE adversarial fine-tuning bu ornekleri egitimden cikarir (leak fix). Egitim seed'lerinden bagimsizdir."; cifar100/svhn files carry a similar note |
| Internal provenance note | results/q1/KOKEN.json:3 "aciklama": "Q1 bas artefaktlarinin koken kutugu. ... (IS-6h)" |
| Dependence on Turkish mirror | `scripts/check_manuscript_claims.py:35` reads `manuscript_tr`; `scripts/verify_manuscript_numbers.py:20-25` TR_FILES `01_giris.tex ... 06_sonuc.tex` |

## T6. Quarantined run1/run2/run3 content in the snapshot

No `results/run1`, `run2`, `run3`, `attention_analysis_run3`, `stat_addendum`, `rev2_blockA` directory exists in the snapshot (find by path name returns only two experiment scripts).

| Occurrence | Location |
|---|---|
| Scripts named for run2/run3 | `experiments/run_all_analyses_run2.py` (RUN2_MODELS `models/resnet18/adv/at_run2/...` lines 38-41; default out dir `results/transfer_analysis_run3`, line 85), `experiments/run_autoattack_run2.py`, `experiments/run_stat_addendum.py:5` (writes results/stat_addendum), `experiments/run_c_addenda.py` |
| `src/analysis/gradient_analysis.py:256` | docstring "Reported run2 values used |cos| - keep True for comparability" |
| Hard-coded earlier-checkpoint literals | `scripts/build_reference_sheet.py:144-145`: "Eski tek kosu (sizintili) karsilastirmasi: kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33 (n=7260)"; same text at sheet line 33; same numbers in paper `tab:conditional` lower block (04_experiments.tex:56-58) |
| `old_run3_diff` keys | `results/c1_transfer/c1_transfer_summary.json` lines 49, 97, 145, 193 = 8.27, 0.63, 5.33, 11.17; shown in sheet Tablo III column "run3 fark" (sheet lines 51-58) and in paper `tab:transfer_protocols` column "Diff.$^\ddagger$" (04:95-98, footnote "Single run, validation split seen during clean pre-training") |
| Neutral numeric fact | the earlier-checkpoint raw difference (8.27) is numerically equal to the current both-correct difference ("+8.27$\pm$0.23", sheet line 57) |
| Quarantined paths cited as provenance | `results/q1/KOKEN.json:124,219,224` (`results/rev2_blockA/a2_transfer_protocols.json`, `a3_gradient_paired.json`, `a3_per_sample.npz`), `:214` (`results/stat_addendum/stat_addendum.json`), with sha256; the referenced files are not in the snapshot |
| `results/c1_statval/statistical_validation.json:10` | `"model_variant": "run3-metric"`; model paths `models/c1/resnet18_s1001/...` (C1 checkpoints) |
| Input outside the c1_*/q1/* whitelist | `scripts/generate_journal_figs_c1.py:168,216` read `results/wrn_eval/wrn_eval_summary.json`; `MAIN:results/wrn_eval/` files dated Jul 8 (git: 0f8a24f "Hakem paneli 2026-07-10 revizyonu"); not copied to snapshot |

## T7. License files

| Item | Fact | Location |
|---|---|---|
| Code license | MIT, "Copyright (c) 2026 Cagri Sahin, Ozal Yildirim", standard text | LICENSE |
| Data license | "The evaluation records and the generated reference sheet are released under CC BY 4.0." Only in README; no separate license file; `grep -rIl "CC BY"` returns README.md only | README (License section) |
| CITATION.cff | `license: MIT`; authors Sahin (Mus Alparslan University), Yildirim (Firat University); `preferred-citation: type: unpublished`, `notes: "Submitted to IEEE Access."`; `title: "cnn-vit-robustness-protocols"` | CITATION.cff |
| Third-party notices | no NOTICE file; no RobustBench/WRN weights redistributed | |
| .gitignore | `__pycache__/`, `*.pyc`, `.DS_Store`, `paper/figures/final/*.png`, `paper/figures/final/*.pdf` | .gitignore:1-5 |
| Affiliations in paper | main.tex:66-72 Mus Alparslan University (c.sahin@alparslan.edu.tr), Firat University (ozalyildirim@firat.edu.tr) | consistent with CITATION.cff |

## T8. What a reader needs (GPU, checkpoints)

| Need | For what | Evidence |
|---|---|---|
| CPU only (numpy, scipy, pandas, matplotlib) | sheet regeneration, protocol recomputation, fig3, fig5b, fig_protokol_kumeleri_veri.json | I ran build_reference_sheet.py; fig_protokol_kumeleri_veri.py (JSON byte-identical, git status clean); `generate_journal_figs_c1.py --only fig3` and `--only fig5b` (PDFs written) |
| Checkpoints `models/c1/{resnet18_s100X,vit_tiny_s200X}/.../best.pth` | fig4, fig5maps, tsne, adv-examples; all `experiments/c1_*.py` | `generate_journal_figs_c1.py:146-149`; `--only fig4` ends "FileNotFoundError: ... 'models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth'" |
| GPU | attacks, training | README: checkpoints about 40 GB and adversarial archive 434 MB "available from the authors on request"; paper 04:459 RTX 5090 32 GB, 21.7 GPU-hours for the three-seed training |
| RobustBench WRN-28-10 weights | WRN row/column | main.tex:118 |
| Compiled `paper/manuscript/main.aux` | fig_protocol_sets.py | run output "HATA / ERROR: paper/manuscript/main.aux not found: compile the manuscript first (needed for the equation number)" |
| Manuscript sources | verify_manuscript_numbers.py, check_manuscript_claims.py | T1 row 10 |

## T9. Table label -> reproducible from records alone (snapshot only, no GPU, no checkpoint)

| Table label (file:line) | Content | Source in snapshot | From records alone? | Notes |
|---|---|---|---|---|
| tab:main_results (04:18) | clean/FGSM/PGD/AA | sheet Tablo I; c1_eval_summary.json, c1_seeds/c1_seed_summary.json; per-sample npz in c1_seeds | yes for ResNet-18, ViT-Tiny rows | WRN row: sheet line 19 "AA degeri RobustBench raporu"; `wrn_eval` records not in snapshot |
| tab:conditional (04:46) upper block | cond. fooling, both-correct robust | sheet Tablo II; c1_seed_summary.json; per-sample npz | yes | |
| tab:conditional lower block | earlier single run | literals in build_reference_sheet.py:144 | no | no record of earlier checkpoints in snapshot |
| tab:transfer_protocols (04:89) cols 1-4 | four protocols | c1_transfer per-sample npz + summary | yes (recomputed, F3b) | |
| tab:transfer_protocols col 5 | earlier single run | `old_run3_diff` in c1_transfer_summary.json | no (stored values only) | |
| tab:transfer_matrix (04:152) | 3x3 incl. WRN | sheet C3; c1_c3 (31 files, 9 npz per pair) | yes as stored | WRN weights external |
| tab:cifar100_results (04:192) | CIFAR-100 | results/q1/e1_cifar100_summary.json; q1/cifar100/pair*/ (22 npz each); q1/cifar100/transfer | records and summaries present; no aggregation script and no sheet section in snapshot | `MAIN:scripts/q1_e1_summary.py` not copied; numbers checked only by verify_manuscript_numbers.py (needs manuscript) |
| tab:svhn_protocols (04:225) | SVHN, 2 seed pairs | q1/e7_svhn_summary.json; q1/svhn/transfer/e7_transfer_summary.json; per-sample npz | same as above | |
| tab:l2_results (04:257) | L2 eps 0.5; AA-L2 on 5000 subset | q1/cifar10_l2/e6_aa_l2_summary.json, e6_onkestirim.json, transfer/e6_l2_transfer_summary.json, aa_pair*/ | same as above | |
| tab:gradient (04:284) | sparsity, alignment | sheet "Gradyan yapisi"; c1_behavior_summary.json; c1_a3/pair* | yes | the $^\ddagger$ row (04:298, earlier checkpoint) has no records |
| tab:spatial (04:318) | spatial locality | sheet "C5 (n=500)"; c1_c5 npz | yes | |
| tab:feature_degradation (04:364) | C4 | sheet "C4"; c1_c4, c1_drift | yes | |
| tab:tgr (04:426) | TGR vs MI-FGSM | sheet "C2"; c1_c2/pair*/tgr_summary.json, per_sample_tgr.npz | yes | |
| Pool-fit / calibration numbers in text (04:127: "+0.673 (CI [+0.602, +0.727])", "+0.470 (CI [+0.361, +0.665])") | | q1/e3_*.json, q1/e3_akolu, e3_points | records present; generating scripts not in snapshot (`q1_e3_figur.py` only plots) | `q1_e3_figur.py` output: "kol A: 116 nokta / 8 kume; kol B: 18 nokta / 6 kume" |

## T10. Figures (8 includegraphics in sections/)

| Figure file (included at) | Generator in snapshot | Run in snapshot (2026-10-04) |
|---|---|---|
| fig_study_overview.png (03:16) | none; source is `MAIN:paper/figures/overview/fig_study_overview.tex` (untracked in main: `?? paper/figures/overview/`), not copied | n/a |
| fig2_epsilon_sweep.pdf (04:72) | generate_journal_figs_c1.py `fig2` | FAILS: FileNotFoundError `results/wrn_eval/wrn_eval_summary.json` |
| fig_protocol_sets.pdf (04:112) | paper/figures/fig_protocol_sets.py + scripts/fig_protokol_kumeleri_veri.py | data script OK (JSON identical); plot script FAILS (main.aux not found) |
| fig3_transfer_heatmap.pdf (04:176) | `fig3` | OK, writes PDF |
| fig4b_gradient_distribution.pdf (04:337), fig4_gradient_comparison.pdf (04:346) | `fig4` | FAILS, needs models/c1/*.pth |
| fig5_attention_comparison.pdf (04:398) | `fig5maps` | needs checkpoints (c1_model, loads best.pth) |
| fig5b_attention_entropy.pdf (04:407) | `fig5b` | OK, writes PDF |
| Published copies | `paper/figures/final/` holds only `.gitkeep`; .gitignore excludes final PDFs/PNGs | `ls -A paper/figures/final` |

## T11. "Data and Code Availability" (MAIN:paper/manuscript/main.tex:113-118) vs snapshot

Quote (main.tex:118): "The analysis pipeline, the scripts that generate every table and figure in this paper, the per-sample evaluation records, the fixed validation-split indices and the seed lists are publicly available at \texttt{https://github.com/cagrisahin58/cnn-vit-robustness-protocols}; together they reproduce every number reported here, and because the four conditioning protocols are all computed from the per-sample records, the protocol comparison can be repeated without retraining. Trained checkpoints total about $40$~GB and are available from the authors on request."

| Claim fragment | Matches snapshot? | Evidence |
|---|---|---|
| "analysis pipeline" | yes | experiments/, src/analysis (rerun needs checkpoints), scripts/build_reference_sheet.py |
| "scripts that generate every table" | partly | the sheet script covers the CIFAR-10 tables; none aggregates the CIFAR-100, SVHN, L2 tables (T9); earlier-checkpoint blocks are literals |
| "scripts that generate every ... figure" | partly | 2 of 8 included figures regenerate (T10); overview source missing; fig2 breaks on missing wrn_eval |
| "per-sample evaluation records" | yes | 348 npz |
| "fixed validation-split indices" | yes | data/val_split_indices*.json |
| "seed lists" | yes | README Seeds paragraph and code |
| "together they reproduce every number reported here" | partly | the sheet reproduces the C1 numbers; earlier-checkpoint numbers (tab:conditional lower block, tab:transfer_protocols col 5, tab:gradient $^\ddagger$ row) and the WRN row are not derived from records in the snapshot; verify_manuscript_numbers.py (158 numbers) cannot run without the manuscript |
| "protocol comparison can be repeated without retraining" | yes | recomputed in T3-F3b |
| "publicly available at https://github.com/cagrisahin58/..." | not verifiable here | snapshot has no configured remote (README/CITATION state the URL); the harness context states the owner still has to create and push the repo; no network check performed |
| "Trained checkpoints total about 40 GB ... on request" | matches README "Not included" | |
| Acknowledgment (main.tex:126) "implementing the analysis and verification scripts released with the paper" | verify/check scripts are included | |
| Sections 01-06 repository wording | no conflicting statement | grep of "github|released|publicly available|on request" in sections finds the repository claim only in main.tex:118 |

## T12. Could not be found

- Training launcher commands for runs 1001-1003 / 2001-2003.
- Records for the earlier single-run checkpoints (tab:conditional lower block, tab:transfer_protocols col 5, tab:gradient $^\ddagger$ row).
- `results/wrn_eval/` in the snapshot (needed by fig2 and the WRN row).
- Source of `fig_study_overview.png` in the snapshot.
- Evidence that the GitHub repository exists online.
- Availability statement of the Turkish mirror (`manuscript_tr`) was not audited.
