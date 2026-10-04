# D2 Figures Dossier (lens D, evidence only)

Collected 2026-10-04. Paths are relative to /home/firat/projects/adeb_sci_1 unless stated. "REF" = results/C1_REFERANS_FOYU.md (line numbers from that file). "MS" = main.pdf (24 pages, 576 x 783 pt page, IEEE Access). Sizes marked "(est.)" are estimated from renders; all others measured with PyMuPDF.

## Summary (10 lines)

1. All 8 figures were viewed as 200-dpi renders and on their pages (sayfa_05, 09, 10, 12, 16, 17); captions, first referring sentence, script, data source, fonts, raster dpi, palette and number provenance are recorded below.
2. main.pdf embeds no Type 3 fonts: fonts are Type0 DejaVuSans / -Bold / -Oblique (figures) and Type1 (Formata, Giovanni, CM, SFRM); pdf.fonttype=42 set at scripts/generate_journal_figs_c1.py:121.
3. Fig 3 (heatmap) numbers: all 9 cells match REF lines 68-77 after rounding; Fig 3 (protocol sets) numbers all match REF lines 52-55 and 57-59 and results/q1/fig_protokol_kumeleri_veri.json.
4. Fig 2 (epsilon sweep): REF holds only the eps=8/255 column (REF 12-19); the eps = 2/255, 4/255, 16/255 points are not in REF; they come from results/c1_sweep/*, and the sweep's eps=8/255 PGD means (44.19, 32.66) differ from REF Table I (44.11, 32.69).
5. Fig 4b legend means (0.013 / 0.015) are in neither REF nor the manuscript text; they equal results/c1_gradient/pair1 l2_norm_mean (0.6658, 0.7625) divided by 50 (batch size), i.e. 0.01332 and 0.01525.
6. Fig 5b: the manuscript text says "layer means near 4.9 nats"; the plotted series ranges 4.61-5.10 with a mean over 12 layers of 4.80 (recomputed from results/c1_c4/pair*/c4_summary.json).
7. CNN blue #0f62fe and ViT red #da1e28 have identical WCAG relative luminance (0.160 each, contrast 1.00); Fig 2 differs by marker only, Fig 4b by color only (overlapping alpha=0.55 histograms).
8. The overview (fig_study_overview.png, 1647x812 px, RGB raster, ~295 dpi at placed width 402.6 pt) is the AI-drawn image; its prompt (paper/bildiri/mimari_figur_promptu.md) asked for "no clip-art", "no gradients", vector, with nested-set panel; the delivered PNG has icons and no nested-set panel; all text labels in it that carry parameters/dims/lambda/eps/alpha/split size match Section 3.
9. Not found: a data artifact (JSON/CSV) for Figs 4, 4b and 5 maps (computed live from models/c1 pair 1 in the script, seed 42); a kanit JSON for any figure except fig_protocol_sets; Type 3 check by poppler (not installed in WSL; PyMuPDF was used instead).
10. Figure text on the page is 5.7-8.1 pt in vector figures (caption/table text 7 pt, body 10 pt); fig_protocol_sets sits at about 1:1 (6.8-7.3 pt).

---

## A. Global facts

| # | Fact | Location |
|---|---|---|
| G1 | Body text 10 pt; table and caption text 7 pt; figure-internal DejaVu text on pages 9/10/12/16/17 ranges 4.99-8.12 pt (page 9: 4.99, 5.7, 6.41, 7.12; page 10: 6.78, 7.27; page 12: 5.86, 6.59, 7.33; page 16: 5.05, 5.68, 6.49, 7.31, 8.12; page 17: 6.06, 6.32, 7.11, 7.9) | PyMuPDF span sizes of main.pdf |
| G2 | Fonts embedded in main.pdf: only Type0 (BMQQDV+DejaVuSans, EVICAO+DejaVuSans-Bold, GCWXDV+DejaVuSans-Oblique) and Type1; no Type3 | PyMuPDF get_page_fonts over 24 pages |
| G3 | Figure PDFs are 339.4 x 211.4 pt (Fig 2), 330.0 x 239.2 (Fig 3 heatmap), 382.9 x 289.4 (Fig 4 maps), 297.8 x 211.4 (Fig 4b), 319.2 x 311.1 (Fig 5 maps), 306.1 x 211.2 (Fig 5b), 249.4 x 266.5 (protocol sets); aspect ratios w/h 1.605, 1.379, 1.323, 1.408, 1.026, 1.449, 0.936 | paper/figures/final/*.pdf |
| G4 | Font sizes in generator: font.size 9, axes.labelsize 10, legend 8, ticks 9 | scripts/generate_journal_figs_c1.py:115-122 |
| G5 | Palette constants: C_CNN #0f62fe, C_VIT #da1e28, C_WRN #8d8d8d; Fig 5b clean line #1a7f37 | scripts/generate_journal_figs_c1.py:~108 (PAIRS/C_CNN line), 277 |
| G6 | Relative luminance: #0f62fe 0.160, #da1e28 0.160, #8d8d8d 0.266, #1a7f37 0.157; pairwise contrast ratios: blue-red 1.00, blue-green 1.02, red-green 1.02, blue-gray 1.51, red-gray 1.51 | scratchpad cv.py (computed) |
| G7 | Deuteranopia simulation (Machado): blue -> #0065fb, red -> #8c7d1e (olive), green #1a7f37 -> #756b3d; protanopia: red -> #605626, green -> #807330. Blue-vs-red remains hue-distinct (blue vs olive); red-vs-green (Fig 5b) collapse to similar olive tones (#8c7d1e vs #756b3d under deutan) | scratchpad cv.py (computed) |
| G8 | Colormap luminance: YlOrRd monotone 0.97 -> 0.05; viridis monotone 0.02 -> 0.78; inferno monotone 0.00 -> 0.94; coolwarm symmetric (0.10, 0.24, 0.43, 0.62, 0.72, 0.61, 0.43, 0.24, 0.10 across 9 samples), so +/- values of the same magnitude have the same gray level | scratchpad cv.py (computed) |
| G9 | Figure numbering vs file names: Figure 5 = fig4b_gradient_distribution (label fig:gradient_analysis), Figure 6 = fig4_gradient_comparison (label fig:gradient_heatmap), Figure 7 = fig5_attention_comparison (label fig:attention_layers), Figure 8 = fig5b_attention_entropy (label fig:feature_degradation); label "feature_degradation" names a figure of attention entropy, while tab:feature_degradation is Table 10 (block-wise cosine) | INDEKS.md; 04_experiments.tex:339, 348, 400, 409 |
| G10 | Generator command-line only; PDF text gives "pdf.fonttype 42" on all six data PDFs; fig_protocol_sets.kanit.json states font "DejaVu Sans (as in scripts/generate_journal_figs_c1.py), pdf.fonttype 42" | fig_protocol_sets.kanit.json "yerlesim.font" |
| G11 | Turkish variants exist in paper/figures/final_tr/ (same file names plus fig1, fig4a, fig5a, fig_adversarial_examples, fig_tsne_features) | ls paper/figures/final_tr |
| G12 | Unused-in-manuscript files in final/ list: generator also writes fig1_robustness_comparison, fig4a, fig5a, tsne, adversarial examples; only the 8 files above are included by \includegraphics | 03_methodology.tex:16; 04_experiments.tex:72,112,176,337,346,398,407 |

---

## B. Figure 1 (fig_study_overview.png), page 5, Section III

| # | Item | Evidence |
|---|---|---|
| 1.1 | Caption (verbatim) | "Study overview. The same CIFAR-10 split feeds two architectures, ResNet-18 and ViT-Tiny, which are trained under one matched adversarial recipe with three independent runs each and selected on a validation split held out before any training. Every evaluation is logged per sample on the full test set, which is what allows the four conditioning protocols to be applied to identical records. The five measurement families on the right are the ones Section~\ref{sec:experiments} reports." (03_methodology.tex:17) |
| 1.2 | First body reference | 03_methodology.tex:7: "Figure~\ref{fig:study_overview} summarizes the design. Two architectures are trained under one matched adversarial recipe with three independent runs each, and every evaluation is logged per sample on the full test set, so that the four conditioning protocols ... can be applied to the same records ..." |
| 1.3 | Placement | \begin{figure*}[!t], width=0.8\textwidth (03_methodology.tex:15-16); page 5 bbox 402.6 x 198.5 pt; PNG 1647 x 812 px RGB, 295 dpi at placed size; aspect 2.03:1 (paper/figures/final/fig_study_overview.png; PyMuPDF) |
| 1.4 | Source comment in tex | "Kaynak PNG 1647 px genis: 14 cm'de ~295 dpi (IEEE 300 onerisinin sinirinda; vektor/daha yuksek cozunurluklu yeniden uretim kullanici tarafinda...)" (03_methodology.tex:11-13) |
| 1.5 | Generation | AI-drawn raster from paper/bildiri/mimari_figur_promptu.md; no data script. Source comment: "bildirideki fig_b0_overview.png'nin aynisi" (03_methodology.tex:9). paper/bildiri/figures/fig_b0_overview.png (1,344,358 B, Aug 6) also exists, with mimari.png and mimari_v2.png |
| 1.6 | Prompt requirements that the delivered PNG can be compared against | Prompt (promptu.md lines ~23-24, 100): "clean, flat, vector-style ... no 3D, no gradients, no clip-art", "Kenarlik/golge/3B efekt yok", "tek sutuna (8.8 cm) kucülünce okunmali", preferred SVG/PDF or >=300 dpi, ~2600 px wide PNG |
| 1.7 | Prompt content not present in the PNG | Prompt specified stage 4 as four NESTED rectangles with per-set annotations (+13.6, +4.4, +8.3, +14.6 pts; "Successful source, N = 3,122"; italic line "conditioning set changes the answer 3.3x"; chips "Spatial locality"). The delivered PNG shows five stacked cards instead, no nested rectangles, no asymmetry numbers. Prompt numbers N=3,122 and +14.6 differ from the final study values N=2,831, +19.37 (REF 55) |
| 1.8 | Visual style observed | Pale gray soft rounded boxes with thin drop-shadow-like grey edges on the right-hand panels; blue/red header bars with white bold titles; icon set includes four CIFAR photos (car, bird, deer, ship), a blank-page "document" icon below them, a speedometer + check mark icon, a balance/scale icon, a bullseye-arrow icon, scatter/histogram icons, stacked layers icon; line weights vary between boxes; text is anti-aliased/soft (raster, not vector); slight JPEG-like fringing not measurable (PNG, RGB) |
| 1.9 | Text size (est.) | Largest label (branch titles) ~ 30 px cap height; small labels ("selection: best PGD-10 accuracy on the held-out validation split", "inner attack:") ~ 14-16 px x-height at 0.244 pt/px, i.e. about 4-5 pt on the page (est.) vs 7 pt captions |
| 1.10 | Color consistency | ResNet branch blue and ViT branch red, same hue family as data figures (#0f62fe / #da1e28 in prompt) |
| 1.11 | Contents not drawn | WRN-28-10 (used in Figs 2 and 3, Tables 4-5) absent; CIFAR-100/SVHN absent; attention entropy/displacement (Figs 7-8) not named: right column has "Block-wise feature drift" only; caption says "two architectures" |
| 1.12 | Unexplained element | Blank document icon beneath the four sample photos in the CIFAR-10 box; no label |

### Text label audit against Section 3 / REF

| Label in figure | Section-3 / REF check | Match |
|---|---|---|
| "ResNet-18 (11.2M parameters)" | 03_methodology.tex:44 "containing 11.2M parameters" | yes |
| "ViT-Tiny (5.7M parameters)" | 03_methodology.tex:50 "totals 5.7M parameters" | yes |
| "3x3 convolutional stem" | 03_methodology.tex:44 "initial 3x3 convolution instead of 7x7" | yes |
| "8 residual blocks (4 stages)" | Section 3 does not state block count; Table 10 lists layer1.0 ... layer4.1 = 8 blocks in 4 stages (page 16) | consistent with Table 10, not stated in Sec. III |
| "GAP + FC (10 classes)" | GAP not mentioned in 03_methodology.tex (grep GAP/global average: no hit) | not stated in text |
| "bilinear upsampling 32->224" | 03_methodology.tex:50 "bilinearly upsampling inputs to 224x224" | yes |
| "16x16 patching (196 tokens + CLS)" | :50 "16x16 patches (196 patches per image)" | yes |
| "12 Transformer blocks (192 dim, 3 heads)" | :50 "192-dimensional embeddings, 12 transformer blocks with 3 attention heads each" | yes |
| "CLS head (10 classes)" | consistent with CIFAR-10 | yes |
| "CIFAR-10 (32x32x3), fixed 2,000-image validation split held out before training" | :100 "fixed 2{,}000-sample validation split ... excluded from the training set of both the clean and the adversarial stage" | yes |
| "Matched adversarial training, 3 seeds per architecture" | :156 and caption: three independent runs per architecture | yes |
| "inner attack: PGD-10, eps = 8/255, alpha = 2/255" | :85 "PGD-10 (alpha = 2/255, eps = 8/255)" | yes |
| "mixed loss: (1-lambda) CE(clean) + lambda CE(adversarial), lambda = 0.5" | :83, :85 "lambda = 0.5" | yes |
| "selection: best PGD-10 accuracy on the held-out validation split" | :100 "Model selection and early stopping use PGD-10 adversarial accuracy on a fixed 2,000-sample validation split" | yes |
| "Full test set, per-sample logging (n = 10,000)" | REF line 3 "tam test kumesi (n=10.000)" | yes |
| "AutoAttack and PGD-10 robust accuracy" | REF Table I columns PGD-10, AA (REF 12-17) | yes |
| "Conditional decomposition (clean x survival)" with 2x2 matrix C,C / C,X / X,C / X,X | REF Table II (REF 21-27); text page 9 "clean-accuracy and conditional-susceptibility components" ("clean x survival" wording vs "conditional susceptibility/fooling" in text) | concept matches; wording differs |
| "Transfer under four conditioning protocols" | REF Table III | yes |
| "Gradient structure (sparsity, alignment)" | REF "Gradyan yapisi" Hoyer/Gini/Rel/Hizalanma (REF 85-96) | yes |
| "Block-wise feature drift" | REF C4 (REF 98+) | yes |

---

## C. Figure 2 (fig2_epsilon_sweep), page 9, Section IV-A

| # | Item | Evidence |
|---|---|---|
| 2.1 | Caption | "PGD-10 robust accuracy vs. perturbation budget ($\eps$), measured on the full test set. Both AT architectures degrade with similar shapes as epsilon increases, with the CNN maintaining a consistent margin." (04_experiments.tex:73) |
| 2.2 | First reference sentence | "Figure~\ref{fig:epsilon_sweep} shows PGD-10 robust accuracy across perturbation budgets $\eps \in \{2/255, 4/255, 8/255, 16/255\}$ on the full test set." (04_experiments.tex:68) |
| 2.3 | Script / function / data | scripts/generate_journal_figs_c1.py fig2() lines 204-240; reads results/c1_sweep/pair{1,2,3}/{resnet18,vit_tiny}/*_robustness_results.csv and results/wrn_eval/wrn_eval_summary.json |
| 2.4 | Axes | x: "Perturbation budget epsilon (L_inf, PGD-10)", ticks "0, 2/255, 4/255, 8/255, 16/255" at equal spacing (categorical index, not proportional to eps); y: "Accuracy (%)", 0-95 limit, ticks 0,20,40,60,80; no unit mismatch |
| 2.5 | x-tick "0" point | The leftmost point is clean accuracy (no PGD), plotted on a "PGD-10" axis label; caption does not say that eps=0 is clean accuracy |
| 2.6 | Legend | Lower left, frameless: "ResNet-18 (AT)", "ViT-Tiny (AT)", "WRN-28-10 (reference)"; does not overlap data (curves are above at x=0..4/255, legend at y 5-30 left); legend text 8 pt in PDF (~6.4 pt on page) |
| 2.7 | Error bands | fill_between m +/- s (alpha 0.18) coded at line 225 (3-seed SD); SDs are 0.09-0.59 pt so the bands are not visible at figure scale; caption does not mention them |
| 2.8 | Marker/palette | blue circles, red squares (solid), gray dashed triangles (WRN, alpha 0.9); blue/red equal luminance (G6); distinguished in grayscale by marker shape and by WRN line style |
| 2.9 | Vertical dotted line | at index 3 (eps=8/255), label "eps=8/255" at (3.05, 5) |
| 2.10 | Font sizes | in-figure 7-10 pt in PDF; placed at ~0.79 scale: ticks 7.1 pt, legend 6.4 pt, "infinity" subscript 5.0 pt (page 9) |
| 2.11 | Spines / look | top/right spines removed; default DejaVu Sans; otherwise matplotlib look with serif-free body (MS body text is Times-like) |
| 2.12 | Aspect/space | 1.605:1; y range reserves 80-95 above the curves; lower-right (below curves, eps 8/255-16/255) empty besides the "eps=8/255" label |
| 2.13 | Numbers vs REF | REF holds eps=8/255 only: clean 85.78 / 73.53 (REF 14-15), PGD-10 44.11 / 32.69 (REF 14-15), WRN clean 89.48, PGD 66.92 (REF 19). Sweep CSV means: ResNet-18 clean 85.78, 2/255 77.30, 4/255 66.73, 8/255 44.19, 16/255 20.38; ViT-Tiny clean 73.53, 64.10, 53.89, 32.66, 12.16; WRN clean 89.48, 85.35, 80.00, 66.92, 47.36 (recomputed from results/c1_sweep and results/wrn_eval, scratch d2_sweep.py) |
| 2.14 | Mismatch to REF at eps=8/255 | sweep PGD-10: 44.19 (CNN), 32.66 (ViT) vs REF Table I: 44.11 and 32.69 (per-seed CNN 44.86, 43.99, 43.73 in sweep) |
| 2.15 | Numbers printed on the figure | none (curves only; no data labels) |
| 2.16 | Margin read from the data | CNN minus ViT: clean 12.25, 2/255 13.20, 4/255 12.84, 8/255 11.53, 16/255 8.22 points (computed from 2.13); caption: "consistent margin" |
| 2.17 | Overlap with tables | Table I (page 8) carries clean/FGSM/PGD-10/AA at 8/255; the sweep's 0 and 8/255 points repeat those values; Figure 2 is the only place for 2/255, 4/255 and 16/255 |
| 2.18 | Naming | caption "epsilon"; axis uses symbol; tick labels use /255 fractions; text uses $\eps$ |

## D. Figure 3 (fig_protocol_sets), page 10, Section IV-B

| # | Item | Evidence |
|---|---|---|
| 3.1 | Caption (key phrases, verbatim) | "Nested evaluation sets of the four transfer protocols in the CNN->ViT direction (left; boxes are schematic and not area-proportional, $N$ is the mean over three seed pairs) and the asymmetry, CNN->ViT minus ViT->CNN, that each protocol measures on the same models and data (right; mean +/- SD of the paired within-seed difference over three seed pairs, individual seed pairs as open markers). ... Brackets mark the decomposition of the 15.01-point spread: the 9.21-point term is the closed-form term of Equation (raw_identity), the 5.79-point term belongs to a protocol that estimates a different quantity, and 3.91 points separate the two endorsed protocols (terms rounded separately)." (04_experiments.tex:113) Caption length: 6 sentences, ~170 words |
| 3.2 | First reference sentence | "Figure~\ref{fig:protocol_sets} draws the four sets for the CNN->ViT direction beside the asymmetry each of them yields." (04_experiments.tex:117) |
| 3.3 | Script / data | paper/figures/fig_protocol_sets.py (418 lines, kanit "surum": 2); data results/q1/fig_protokol_kumeleri_veri.json made by scripts/fig_protokol_kumeleri_veri.py (79 lines) from results/c1_transfer/c1_transfer_summary.json (sha256 60268615...); kanit json fig_protocol_sets.kanit.json records width 8.8 cm, height 9.4 cm, dpi 300, "en_kucuk_yazi_pt": 7.0, fills #EDF5FF, #D0E2FF, #78A9FF, #0F62FE |
| 3.4 | Output formats | PDF (vector, 249.4 x 266.5 pt, Type0 DejaVu fonts, no images) and PNG 1039 x 1110 RGBA (paper/figures/final/fig_protocol_sets.png) |
| 3.5 | Left panel | header "Evaluation set (CNN->ViT boxes)"; line "N: CNN->ViT / ViT->CNN" above boxes; four nested rounded boxes: "All test samples (raw) N = 10,000", "Target (ViT) correct N = 7,353 / 8,579", "Both correct N = 7,061", "Successful source (CNN white-box) N = 2,831 / 3,814"; box text 7.0-7.5 pt in PDF; white bold text on the darkest box (#0F62FE) |
| 3.6 | Right panel | header "Measured asymmetry (mean +/- SD, 3 seed pairs)"; x-axis 0-25, ticks 0,5,...,25, label "CNN->ViT - ViT->CNN (pts)"; four rows with dotted guide lines, bold vertical bar at the mean, three open circles for the seed pairs, labels "+13.57 pts / +/-0.33", "+4.36 pts / +/-0.44", "+8.27 pts / +/-0.23", "+19.37 pts / +/-1.27"; rows carry no protocol names; correspondence to the left boxes is by vertical position only (verbatim in render) |
| 3.7 | Brackets | three brackets above the first row: "5.79, different estimand" (13.57 -> 19.37), "9.21, identity term" (4.36 -> 13.57), "3.91" (4.36 -> 8.27); the 3.91 bracket lies close above the "+13.57 pts" label (render sayfa_10 / sekil png) |
| 3.8 | Footer | italic "Spread 15.01 pts (terms rounded separately)" |
| 3.9 | Numbers vs REF | REF 52-55: raw 13.57+/-0.33 (N 10000/10000), target-correct 4.36+/-0.44 (7353/8579), both-correct 8.27+/-0.23 (7061/7061), successful source 19.37+/-1.27 (2831/3814); REF 57: "Protokol yayilimi: 15.01+/-0.84 puan"; 9.21, 5.79, 3.91 are not printed in REF but appear in results/q1/fig_protokol_kumeleri_veri.json "ayrisim" (ozdeslik_terimi 9.21, farkli_estimand 5.79, artik_takdir 3.91, yayilim 15.01); seed values 13.2/13.69/13.83, 4.83/4.28/3.97, 8.51/8.05/8.24, 20.8/18.91/18.39 in the same JSON |
| 3.10 | Arithmetic of terms | 13.57-4.36 = 9.21; 19.37-13.57 = 5.80 (printed 5.79); 8.27-4.36 = 3.91; 9.21+5.79 = 15.00 vs printed 15.01 (caption and text:117 state "terms rounded separately") |
| 3.11 | Nesting claim | Boxes are drawn Successful source inside Both correct inside Target correct inside All; JSON key "ic_icelik_tutuyor": true; text :117 gives N 2,831 / 3,814 for successful source and 7,061 for both-correct |
| 3.12 | Font scale on page | about 1:1 (G3 widths: figure 249 pt placed at column width); DejaVu spans 6.78 and 7.27 pt on page 10 |
| 3.13 | Palette | blue sequential fills (4 steps, luminance 0.905, 0.750, 0.396, 0.160); black marks on right; monotone in grayscale; no red/green |
| 3.14 | Overlap with table | Table 3 (page 9) gives the same four asymmetries, SDs and N (04_experiments tab:transfer_protocols; REF 52-55) |
| 3.15 | Whitespace | blank band above the left panel (top-left) and the area right of "N: CNN->ViT / ViT->CNN"; bracket stack takes top 1/5 of right panel |
| 3.16 | Naming | Figure: "All test samples (raw)", "Target (ViT) correct", "Both correct", "Successful source"; Table 3: "Unconditioned (raw)", "Target-correct", "Both-correct", "Successful-source"; text:117: "without conditioning", "target-correct", "both-correct", "successful-source"; caption of Fig 4: "Conditioned (target-correct)"; Fig-3 axis uses ASCII arrows |

## E. Figure 4 (fig3_transfer_heatmap), page 12, Section IV-B

| # | Item | Evidence |
|---|---|---|
| 4.1 | Caption | "Conditioned (target-correct) transfer fooling rates, mean over three seed pairs. Off-diagonal asymmetry under this protocol is +4.4 points; Table~\ref{tab:transfer_protocols} shows how far the same quantity moves under other protocols." (04_experiments.tex:177) |
| 4.2 | First reference | "Figure~\ref{fig:transfer_heatmap} shows the conditioned matrix." (04_experiments.tex:172) |
| 4.3 | Script / data | generate_journal_figs_c1.py fig3() 243-267; reads results/c1_c3/pair{1,2,3}/transfer_matrix.json key "<src>-><tgt>"."cond_fooling" |
| 4.4 | Axes | x: "Target", y: "Source" (class labels ResNet-18, ViT-Tiny, WRN-28-10, 8 pt, ~5.9 pt on page); colorbar "Conditioned fooling rate (%)", 0-60, ticks every 10; shrink 0.85 |
| 4.5 | Cell numbers (1 decimal) | 48.5, 19.9, 12.5 / 15.5, 55.6, 8.7 / 21.5, 18.2, 25.2; diagonal bold; white text where value > 35 |
| 4.6 | Match to REF (cond. column, REF 68-77) | 48.52 -> 48.5; 19.93 -> 19.9; 12.48 -> 12.5; 15.52 -> 15.5; 55.57 -> 55.6; 8.65 -> 8.7; 21.48 -> 21.5; 18.15 -> 18.2; 25.16 -> 25.2 (all match; 8.65 and 18.15 rounded up, mean of three unrounded values) |
| 4.7 | Caption number | "+4.4" = 19.87-15.51 = 4.36 (REF 54, 52-55); in heatmap: 19.9 - 15.5 = 4.4 |
| 4.8 | Raster | embedded as 410 x 410 Indexed image plus 18 x 354 colorbar image, placed 144.2 pt wide = 205 dpi; text is vector (page 12) |
| 4.9 | Palette | YlOrRd monotone in luminance (G8); sequential, grayscale-safe; red-yellow family is color-blind readable via lightness; no per-cell borders/gridlines |
| 4.10 | Overlap with table | Table 4 on the same page (page 12, tab:transfer_matrix) lists all nine cond. values (48.52+/-0.84 ...); figure repeats only the conditioned column in 1 decimal and omits the raw column and +/- values |
| 4.11 | Naming | figure caption "target-correct"; colorbar "Conditioned fooling rate"; Table 4 header "Cond. (%)", caption "Cond. = target-conditioned rate"; text: "conditioned fooling rate" |
| 4.12 | Diagonal | white-box cells on the diagonal (bold) are drawn in the same matrix as black-box transfer cells; caption does not state that the diagonal is white-box (Table 4 caption does: "Diagonal entries are white-box attacks") |
| 4.13 | Look | default matplotlib imshow, no grid separators, tick marks present, square-ish aspect 1.379 incl. colorbar |

## F. Figure 5 (fig4b_gradient_distribution), page 16, Section IV-F

| # | Item | Evidence |
|---|---|---|
| 5.1 | Caption | "Distribution of per-sample gradient $L_2$ norms for both architectures. The magnitude maps for the same inputs are shown in Figure~\ref{fig:gradient_heatmap}." (04_experiments.tex:338) |
| 5.2 | First reference | "Figure~\ref{fig:gradient_analysis} adds the distribution of per-sample gradient $L_2$ norms, which the scale-invariant sparsity measures do not capture." (04_experiments.tex:342) |
| 5.3 | Script / data | generate_journal_figs_c1.py fig4() 298-345; no stored data artifact: it loads models/c1 pair 1 (resnet18_s1001, vit_tiny_s2001, lines 143-150), loops the CIFAR-10 test loader (batch 50) until 500 samples, takes the CE gradient on clean inputs (_grads 292-295), histograms 40 bins alpha 0.55 |
| 5.4 | Axes | x: "Per-sample input-gradient L_2 norm", ticks 0.00-0.16 step 0.02; y: "Count", ticks 0-140 step 20; no sample size in caption or axis |
| 5.5 | Legend | upper right, frameless: "ResNet-18 (AT) (mean 0.013)", "ViT-Tiny (AT) (mean 0.015)"; patch swatches blue and red with alpha, overlap region mixed purple |
| 5.6 | Legend numbers vs sources | not in REF; not in manuscript text (grep "0.013" none); results/c1_gradient/pair1/gradient_summary.json l2_norm_mean ResNet18_AT 0.66579, ViT_Tiny_AT 0.76249; divided by 50: 0.013316 and 0.015250 = figure legend 0.013 and 0.015 |
| 5.7 | Loss reduction (inference) | The two stored means divided by batch size 50 reproduce the legend means to three decimals; fig4() computes nn.CrossEntropyLoss() (default mean over the 50-image batch) per _grads() |
| 5.8 | Text conflict | Table 8 caption: "computed from per-sample loss gradients (n=500 test samples per run; mean+/-std over three runs)" (04_experiments.tex:283); the figure shows pair-1 only (script line 299 c1_model(...,1)) and does not state it |
| 5.9 | Distribution shape | single peak at 0-0.005 (ResNet count ~152, ViT ~67), tail to 0.16; two blue outliers near 0.105 and 0.16; right half of the x range (0.08-0.16) holds roughly 5 bars of count 1-3 (render) |
| 5.10 | Palette | blue and red alpha 0.55 overlap, no outlines/hatching; same luminance (G6) so overlap regions are not separable in grayscale |
| 5.11 | Font on page | y/x labels 8.12 pt, ticks 7.31 pt, legend 6.49 pt (page 16) |
| 5.12 | Note on text claim | Text (Sec. IV-F) and Table 8 report only scale-invariant measures; figure reports raw norms whose units depend on loss reduction (5.7) |

## G. Figure 6 (fig4_gradient_comparison), page 16

| # | Item | Evidence |
|---|---|---|
| 6.1 | Caption | "Input-gradient magnitude maps for the same test images under both models. CNN gradients place more of their mass on fewer components (Table~\ref{tab:gradient}); Table~\ref{tab:spatial} shows that this is not accompanied by a difference in spatial arrangement, so the panels should be read as sparsity and not as localization." (04_experiments.tex:347) |
| 6.2 | First reference | "Figure~\ref{fig:gradient_heatmap} shows the corresponding magnitude maps; as its caption notes, they illustrate sparsity, not localization." (04_experiments.tex:351) |
| 6.3 | Script | generate_journal_figs_c1.py fig4() 328-343: 3 x 4 grid, first batch (first 4 test images of the loader), pair 1 models, map = per-image sum over channels of squared gradient, normalized by its own max (line 333-334), cmap "inferno", interpolation "nearest" |
| 6.4 | Layout | rows labelled "Input", "ResNet-18 (AT)", "ViT-Tiny (AT)"; no column titles, no colorbar, no class labels for the four images (render: cat, ship, ship, aircraft-like); no tick labels (xticks removed) |
| 6.5 | Normalization | each map is min-max to its own maximum: maps are not comparable in magnitude across panels; neither caption nor axis says "per-image normalized" (script 333-334) |
| 6.6 | Raster | 12 images 171 x 171 px each (4 RGB, 8 Indexed) placed 51.8 pt wide = 238 dpi on page 16; 32 x 32 source upsampled with nearest-neighbor, visible 32-px blocks |
| 6.7 | Image 4 content | the fourth input contains legible printed red text (cover-like image) - visible in render |
| 6.8 | Font size | only 8 pt row labels (DejaVu), scaled ~6.5 pt on page |
| 6.9 | Palette | inferno monotone luminance (G8) |
| 6.10 | Number of sample/pair | caption does not say which seed pair nor that it is the first loader batch; script line 299-301 uses pair 1 |
| 6.11 | Page layout | figure sits right column on page 16 beside Figure 5; 382.9 x 289.4 pt PDF (aspect 1.323) |

## H. Figure 7 (fig5_attention_comparison), page 17, Section IV-G

| # | Item | Evidence |
|---|---|---|
| 7.1 | Caption | "CLS-token attention maps (post-softmax, head-averaged) across ViT layers under adversarial attack. Each row shows a different layer (1, 6, 12); columns show clean attention, adversarial attention, and their difference. A single sample is shown for illustration; the depth trend in attention displacement is reported quantitatively in the text over $n=1{,}000$ samples per run." (04_experiments.tex:399) |
| 7.2 | First reference | "Figure~\ref{fig:attention_layers} visualizes CLS-token attention maps at layers 1, 6, and 12 for a representative sample." (04_experiments.tex:403) |
| 7.3 | Script | generate_journal_figs_c1.py fig5maps() 424-453; pair 1 ViT, first test batch (16), image index 0 (cls_maps[0]), PGD eps 8/255 alpha 2/255 10 steps; rows layers [0, 5, 11]; clean/adv: viridis, vmin 0, vmax = max of the clean/adv map per row; difference: coolwarm symmetric about 0 with per-row vmax |
| 7.4 | Labels | row labels "block 1", "block 6", "block 12" (script L['block']); column titles "clean", "adversarial", "difference" |
| 7.5 | Naming | figure rows "block N" vs caption "layer (1, 6, 12)" vs text "layers 1, 6, and 12" vs Fig 8 axis "Transformer block" vs text:392 "per-layer" and "block-wise" in Table 10 |
| 7.6 | Colorbars | none; per-row color scale differs (clean/adv scale per row, difference scale per row), so row-to-row color comparison is not supported by the figure; no scale printed |
| 7.7 | Grid | 14 x 14 token grid (196 tokens) with nearest interpolation; no overlay on the input image; the input image is not shown (caption: "A single sample") |
| 7.8 | Raster | 9 images 185 x 185 px placed 67.3 pt wide = 198 dpi |
| 7.9 | Palette | viridis (monotone luminance 0.02-0.78) and coolwarm (diverging; luminance symmetric, G8); red/blue diverging pair separable under deuteranopia (blue vs olive) |
| 7.10 | Fonts | 8 pt DejaVu labels; page 17 spans 6.06-7.9 pt |
| 7.11 | Layout | aspect 1.026; page position top of right column; whitespace small |
| 7.12 | Text on pairing | text:403 "It agrees with the displacement measurement, since later layers move more" (single-sample panels) |
| 7.13 | Numbers on figure | none |

## I. Figure 8 (fig5b_attention_entropy), page 17

| # | Item | Evidence |
|---|---|---|
| 8.1 | Caption | "Per-layer entropy of the CLS attention distribution for clean and adversarial inputs, $n=1{,}000$ samples per run, mean over three runs with $\pm$1 s.d. shading. The attention maps themselves are shown in Figure~\ref{fig:attention_layers}." (04_experiments.tex:408) |
| 8.2 | First reference | "Figure~\ref{fig:feature_degradation} plots the per-layer curves, which lie on top of each other." (04_experiments.tex:392) |
| 8.3 | Script / data | generate_journal_figs_c1.py fig5b() 270-289; results/c1_c4/pair{1,2,3}/c4_summary.json ["vit"]["attention"]["entropy_clean_mean"] and "entropy_adv_mean" (12 values each); SD with ddof=1 across 3 pairs |
| 8.4 | Axes | x: "Transformer block" ticks 1-12; y: "CLS attention entropy (nats)", range ~4.45-5.2, ticks 4.5-5.2 step 0.1; the y axis does not start at zero (non-zero baseline) |
| 8.5 | Series | Clean: green #1a7f37, circles, solid; Adversarial: red #da1e28, squares, dashed; shading alpha 0.18 each; the overlap of green and red shading renders as brown-gray (render) |
| 8.6 | Plotted values | Clean mean per layer: pair means computed (pair1 5.159, 4.653, 5.052, 4.800, 4.717, 4.970, 4.924, 4.727, 4.986, 4.781, 4.708, 4.581; pair2 5.027, 4.945, ...; pair3 5.130, 5.053, ...); mean over all 12 layers and 3 pairs 4.800; SD across pairs per layer 0.026-0.246 (computed) |
| 8.7 | Text numbers | text:392 "mean per-layer change is at most 0.005 nats ... against layer means near 4.9 nats"; REF 107: "attention entropi degisimi: tum katmanlarda |delta| <= 0.0045"; REF 108: "CLS yer degistirmesi: 0.0276 (katman 1) -> 0.0841 (en derin)"; "layer means near 4.9 nats" is not in REF; plotted per-layer means range 4.61-5.10 |
| 8.8 | Readability | clean and adversarial markers coincide at every layer; the red marker covers the green one; the shading extends 4.46-5.17 (render) |
| 8.9 | Legend | upper right frameless, "Clean", "Adversarial" (7-8 pt); no entry for the shading |
| 8.10 | Shading meaning | across-run SD dominates; between-condition difference (<=0.0045 nats) invisible at the plotted scale; caption states "$\pm$1 s.d." |
| 8.11 | Fonts on page | 7.9 pt labels, 7.11 tick labels, 6.32 legend (page 17) |
| 8.12 | Palette | green/red pair low-contrast for deutan viewers (G7) and equal-luminance (contrast 1.02, G6); markers (circle vs square) and line style (solid vs dashed) differ but overlap |
| 8.13 | Naming | figure label "Transformer block"; Fig 7 rows "block N"; caption "Per-layer"; label name feature_degradation (G9) |

---

## J. Cross-figure inconsistency and rendering notes (facts only)

| # | Fact | Location |
|---|---|---|
| J1 | The same blue/red pair is used for ResNet/ViT in Figs 1, 2, 4b, 6 (row labels), and for transfer-set fill in Fig 3 (blue sequential only) | renders |
| J2 | Four of the data figures keep the DejaVu Sans default face (matplotlib default look) while body text is Times-like (SFRM), captions Formata (IEEE Access template) | G2; renders |
| J3 | No figure has in-figure titles (a) (b) subpanel letters; Fig 3 (protocol sets) uses panel headers "Evaluation set" / "Measured asymmetry" but no (a)/(b) while the caption says "(left ...)" and "(right ...)" | renders; 04_experiments.tex:113 |
| J4 | Fig 7 caption states "layer", figure says "block"; Fig 8 axis "Transformer block"; Table 10 header "Blk" | 7.5 |
| J5 | Fig 3 (heatmap) caption "Conditioned (target-correct)" vs protocol-sets figure "Target (ViT) correct" vs Table 3 "Target-correct" | 3.16, 4.11 |
| J6 | Fig 6 and Fig 7 have no colorbar | 6.4, 7.6 |
| J7 | Fig 5 and Fig 6 raster cell sizes: 238 dpi (Fig 6), 198 dpi (Fig 7), 205 dpi (Fig 4 heatmap), 295 dpi (Fig 1) at placed size; pixel-grid appearance of the 32 x 32 and 14 x 14 maps is intrinsic to nearest-neighbor upsampling | PyMuPDF image info |
| J8 | Three of the figures contain content that is also in a table (Fig 2 vs Table 1, Fig 3 protocol sets vs Table 3, Fig 4 heatmap vs Table 4) | 2.17, 3.14, 4.10 |
| J9 | Figure numbers printed in the Section IV text refer to the PDF numbering: Fig 4 = heatmap on page 12, Fig 3 = protocol sets on page 10; page 12 text "Figure 4 shows the conditioned matrix" | render sayfa_12 |
| J10 | Figure width placement: Figs 2-8 at \columnwidth (single column, about 3.5 in); overview at 0.8\textwidth in figure*. In-figure text scale on the page: Fig 2 0.79, Fig 3 heatmap 0.73, Fig 5b 0.79, Fig 4b 0.81, protocol sets ~1.0 | G1, 2.10 |
| J11 | Not verified: pdffonts/pdfimages (poppler absent in WSL); equivalent PyMuPDF extraction used | tool availability |
| J12 | Not found: stored data/kanit files for Fig 4, 4b, 5; stored sample index/class of the four gradient-map images and the attention-map sample | grep results/c1_* and paper/figures/final |
