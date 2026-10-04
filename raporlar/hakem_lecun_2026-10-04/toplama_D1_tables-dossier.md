# D1 Tables dossier (lens D, figures and tables)

Collected: 2026-10-04. Sources: `paper/manuscript/sections/04_experiments.tex` (LaTeX), `paper/manuscript/main.pdf` (24 pages; text-layer geometry read with PyMuPDF inside the container), page PNGs in `teslim/render_2026-10-04/` (viewed: sayfa_08, 09, 12, 14, 15, 16, 18), 260 dpi crops of Tables 1 and 2 (scratch, `_tmp/d1_t1.png`, `d1_t2.png`). All numbers here are copied from the table source or the PDF text layer, none from quarantined results.

## Summary (10 lines)

1. All 11 tables were found in `04_experiments.tex` (lines 15, 43, 86, 149, 189, 222, 254, 281, 315, 361, 423); none exists in other sections per INDEKS.md; none is `table*`.
2. For each table the LaTeX source, rendered placement, column spec, rules, size commands, bold/italic, footnotes, abbreviations, decimals, caption content and first body reference are recorded below.
3. Measured overrun beyond the column edge (PDF line extents): Table 1 +31.6 pt, Table 2 +22.7 pt, Table 3 +19.3 pt, Table 9 +11.3 pt, Table 7 +6.9 pt; Tables 4, 6, 8, 10, 11 inside; Table 5 inside by eye.
4. Bold and italic in table text are not rendered (no bold or italic font for the table text family in the PDF font list); bold is explained in no caption.
5. Table 7's cited content: body line 269 cites it for four protocol asymmetries that the table does not contain.
6. The same quantities carry different values across Tables 2, 3, 4 (for example 48.58 vs 48.52, 41.02 vs 41.07) without a stated aggregation difference.
7. Protocol and attack naming varies across tables (Raw / Unconditioned (raw) / White-box on source (raw); Cond. / Target-correct / Cond. fooling; AA / AutoAttack / AA-L2).
8. Decimals are consistent within columns except Table 8 (4, 3 and 1 decimals in one row group).
9. Not found or not verified: Table 5's exact PDF extents (viewed only); the render at 110 dpi cannot show whether bold is subtly heavier, so weight was judged from PDF font names and 260 dpi crops of Tables 1 and 2 only; Tables 3 to 11 were not cropped at 260 dpi.
10. No opinions or severity labels are given; items are facts with locations.

## Evidence per table


### T1: Table 1 (`tab:main_results`)

Render: `teslim/render_2026-10-04/sayfa_08.png (page 8)`. Source: `paper/manuscript/sections/04_experiments.tex:15-39`.

```latex
15: \begin{table}[!t]
16: \centering
17: \caption{Main robustness results on CIFAR-10 ($\eps = 8/255$), mean$\pm$std over three independent training runs per architecture. AA denotes AutoAttack with the standard suite.}
18: \label{tab:main_results}
19: \scriptsize
20: \setlength{\tabcolsep}{2pt}
21: \begin{tabular}{lcccccc}
22: \toprule
23: \textbf{Model} & \textbf{Defense} & \textbf{Params} & \textbf{Clean} & \textbf{FGSM} & \textbf{PGD-10} & \textbf{AA} \\
24: \midrule
25: \multicolumn{7}{l}{\textit{CNN Models}} \\
26: ResNet-18 & None & 11.2M & 95.25$\pm$0.15 & 40.29$\pm$1.77 & 0.03$\pm$0.03 & -- \\
27: ResNet-18 & AT & 11.2M & 85.78$\pm$0.36 & 53.46$\pm$0.08 & 44.11$\pm$0.50 & \textbf{37.93$\pm$0.14} \\
28: WRN-28-10 & AT$^\dagger$ & 36.5M & 89.48 & 70.91 & 66.92 & 62.76 \\
29: \midrule
30: \multicolumn{7}{l}{\textit{Vision Transformer Models}} \\
31: ViT-Tiny & None & 5.7M & 80.09$\pm$0.60 & 6.10$\pm$1.47 & 0.05$\pm$0.05 & -- \\
32: ViT-Tiny & AT & 5.7M & 73.53$\pm$0.55 & 36.31$\pm$0.42 & 32.69$\pm$0.22 & \textbf{29.14$\pm$0.40} \\
33: \bottomrule
34: \multicolumn{7}{l}{\scriptsize $^\dagger$Robust checkpoint of Gowal et al.~\cite{gowal2020uncovering} via RobustBench~\cite{croce2021robustbench};}\\
35: \multicolumn{7}{l}{\scriptsize \phantom{$^\dagger$}a single external checkpoint, so no standard deviation applies.}\\
36: \multicolumn{7}{l}{\scriptsize \phantom{$^\dagger$}Clean/FGSM/PGD-10: our local full-test evaluations; AA: the}\\
37: \multicolumn{7}{l}{\scriptsize \phantom{$^\dagger$}RobustBench-reported figure (we did not rerun AutoAttack on it).}
38: \end{tabular}
39: \end{table}
```

- [T1-1] Placement: right column of page 8, top; PDF text extent x = 299.6 to 571.0 pt (page width 576 pt, right text-column edge 539.4 pt, from PyMuPDF line bboxes of main.pdf p.8). The two rows that carry the AA column end at x = 571.0, that is 31.6 pt beyond the column edge and 5 pt from the page edge. Visible in the render: the "37.93±0.14" and "29.14±0.40" cells reach the right page margin, outside the text block that the body paragraphs below it respect (they end at 539.4).
- [T1-2] Columns: 7, alignment `lcccccc` (line 21). All numeric columns centred, so the decimal points and the ± signs are not aligned (rendered: "95.25±0.15" and "0.03±0.03" are centred on different offsets; "–" in the AA column for the undefended rows is centred).
- [T1-3] Rules: booktabs `\toprule`, `\midrule` x2, `\bottomrule` (lines 22, 24, 29, 33); no vertical lines; no `\cmidrule`.
- [T1-4] Size commands: `\scriptsize` (line 19) and `\setlength{\tabcolsep}{2pt}` (line 20). Rendered font SFRM0700 (7 pt) against 10 pt body (SFRM1000). The footnote lines inside the tabular carry another `\scriptsize` (lines 34 to 37), which is a no-op at this size.
- [T1-5] Float: `table` with `[!t]` (not `table*`); the table is wider than one column (see T1-1). No `table*` anywhere in the manuscript sections or main.tex (grep for `table\*` returned nothing).
- [T1-6] Bold: `\textbf{37.93$\pm$0.14}` and `\textbf{29.14$\pm$0.40}` (lines 27, 32), i.e. the bold group includes the ± term. Only the AA cell of each AT row is bold; the best clean, FGSM and PGD-10 cells and the WRN AA (62.76) are not. The caption does not say what bold means (caption line 17 reads only: "Main robustness results on CIFAR-10 ($\eps = 8/255$), mean$\pm$std over three independent training runs per architecture. AA denotes AutoAttack with the standard suite.").
- [T1-7] Rendered weight: in the 260 dpi crop the bold AA cells and the bold column headers (`\textbf{Model}` etc.) are not visibly bolder than the other cells; italics (`\textit{CNN Models}`, line 25) render upright. PDF font list (all pages) holds SFRM0700/0800/1000 only for table text and no SFRM bold or italic variant (only CMBX10 and Formata bold for headings). Same for every table: see the cross-table list X-1.
- [T1-8] Footnote mark: `$^\dagger$` on `AT` in the WRN row (line 28). Footnote text (lines 34 to 37): "Robust checkpoint of Gowal et al. [54] via RobustBench [23]; a single external checkpoint, so no standard deviation applies. Clean/FGSM/PGD-10: our local full-test evaluations; AA: the RobustBench-reported figure (we did not rerun AutoAttack on it)." The footnote is typeset inside the tabular as four `\multicolumn{7}{l}` rows after `\bottomrule`, broken manually mid-sentence with `\phantom{$^\dagger$}` indentation.
- [T1-9] Abbreviations not defined in caption or header: "AT" (defined in 02_related_work.tex:23 and 03_methodology.tex:80, not in the caption), "Params" (no unit in header; unit M is attached per cell), "None" (defence column), "FGSM" and "PGD-10" (defined in Section III, not in caption). "AA" is defined in the caption.
- [T1-10] Decimals: all measured cells two decimals (95.25, 40.29, 0.03, 53.46 ...), ± terms two decimals; Params one decimal (11.2M, 36.5M, 5.7M). Consistent within columns.
- [T1-11] Caption states: seeds (three independent training runs per architecture), eps (8/255), dataset (CIFAR-10), "mean±std", AA definition. Caption does not state: n (the 10,000 test samples appear in the body, 04_experiments.tex:13), units (the column headers carry no "(%)"), PGD-10 step size, which statistic of "std" (the body line 13 says "the standard deviation over those runs").
- [T1-12] WRN-28-10 row has no ± (single external checkpoint; explained in footnote); its AA value is not from the authors' evaluation (footnote), while Clean/FGSM/PGD-10 are, so one row mixes two provenance classes with no per-cell marking.
- [T1-13] Row labels: model and defence in two columns ("ResNet-18 | AT"); other tables fuse them ("ResNet-18 AT"); CNN/ViT group labels are `\multicolumn{7}{l}{\textit{...}}` rows.
- [T1-14] First reference to the table: in document order 03_methodology.tex:69 "We use PGD-10 (10 iterations) for both adversarial training and evaluation throughout this work (Table~\ref{tab:main_results})." (a citation for a method statement, the table is not yet shown). First in Section IV: 04_experiments.tex:13 "Table~\ref{tab:main_results} presents the main robustness comparison across all evaluated models." Float follows at line 15.


### T2: Table 2 (`tab:conditional`)

Render: `teslim/render_2026-10-04/sayfa_09.png (page 9)`. Source: `paper/manuscript/sections/04_experiments.tex:43-62`.

```latex
43: \begin{table}[!t]
44: \centering
45: \caption{Conditional decomposition of white-box robustness on the full test set, mean$\pm$std over three runs. The lower block repeats the same quantities on our earlier single-run checkpoints.}
46: \label{tab:conditional}
47: \scriptsize
48: \setlength{\tabcolsep}{2.5pt}
49: \begin{tabular}{lcccc}
50: \toprule
51: & \multicolumn{2}{c}{\textbf{Cond.\ fooling (\%)}} & \multicolumn{2}{c}{\textbf{Both-correct robust (\%)}} \\
52: \textbf{Model} & \textbf{PGD-10} & \textbf{AA} & \textbf{PGD-10} & \textbf{AA} \\
53: \midrule
54: ResNet-18 AT & \textbf{48.58}$\pm$0.80 & \textbf{55.78}$\pm$0.23 & \textbf{59.86}$\pm$0.35 & \textbf{51.89}$\pm$0.49 \\
55: ViT-Tiny AT & 55.53$\pm$0.50 & 60.37$\pm$0.33 & 46.11$\pm$0.59 & 41.15$\pm$0.39 \\
56: \midrule
57: \multicolumn{5}{l}{\textit{Earlier single run, validation split seen during clean pre-training ($n$=7{,}260)}} \\
58: ResNet-18 AT & 52.15 & 58.16 & \textbf{54.92} & \textbf{48.15} \\
59: ViT-Tiny AT & 52.33 & \textbf{56.46} & 49.61 & 45.33 \\
60: \bottomrule
61: \end{tabular}
62: \end{table}
```

- [T2-1] Placement: left column of page 9, top. PDF text extent x = 38.7 to 300.6 pt for the italic sub-header row "Earlier single run, validation split seen during clean pre-training (n=7,260)" (line 57), against left column edge 277.9 pt and right column start 297.6 pt. The sub-header therefore overruns the column by 22.7 pt, crosses the 19.7 pt gutter and ends 3.0 pt inside the right column; in the render the line is visibly wider than the caption above it (caption right edge 275.0 pt) and ends at the gutter. The numeric body is also 3.3 pt wide: the last column "51.89±0.49" ends at x = 281.2 pt.
- [T2-2] Columns: 5, `lcccc` (line 49). Header is two-level: row 1 `\multicolumn{2}{c}{Cond. fooling (\%)}` and `\multicolumn{2}{c}{Both-correct robust (\%)}` (line 51), row 2 PGD-10, AA, PGD-10, AA. No `\cmidrule` under the group headers; the first header cell of row 1 is empty.
- [T2-3] Rules: booktabs `\toprule`, two `\midrule`, `\bottomrule` (lines 50, 53, 56, 60); no vertical lines.
- [T2-4] Size: `\scriptsize`, `\setlength{\tabcolsep}{2.5pt}` (lines 47, 48); rendered 7 pt (SFRM0700).
- [T2-5] Float: `table`, `[!t]`, not `table*`. Table is wider than its column (T2-1).
- [T2-6] Bold: bold on mean only, ± outside the braces: `\textbf{48.58}$\pm$0.80` (line 54). This differs from Table 1, where the braces enclose the ± term. Upper block: all four ResNet cells bold (fooling lower, both-correct higher). Lower block: bold only on `\textbf{54.92}`, `\textbf{48.15}` (ResNet, both-correct) and `\textbf{56.46}` (ViT, AA fooling); the PGD-10 fooling pair (52.15 vs 52.33) has no bold. Bold is not explained in the caption. Not rendered visibly bold (see X-1).
- [T2-7] Italic: sub-header row set with `\textit{...}` (line 57); renders upright.
- [T2-8] Footnote marks: none.
- [T2-9] Abbreviations: "Cond. fooling" (column header, line 51), "AA", "PGD-10", "AT" undefined in the caption; "Cond." is spelled out only in Table 4's caption (line 151: "Cond. = target-correct conditioned rate"). "Both-correct robust" is not defined in the caption (it is in Section III-F per the body line 64 reference).
- [T2-10] Decimals: all cells two decimals; upper block has ±, lower block (single run) has no ± and no mean marker. Consistent within columns.
- [T2-11] Caption (line 45): "Conditional decomposition of white-box robustness on the full test set, mean$\pm$std over three runs. The lower block repeats the same quantities on our earlier single-run checkpoints." States: full test set, three runs. Does not state: n (10,000 stated nowhere in the caption), eps, attack parameters. The lower block's n = 7,260 is given in the sub-header row, while the caption says "full test set" for the table as a whole. Units appear in the group headers as (%).
- [T2-12] Consistency of the table with text: body line 64 "for AutoAttack it reads $85.78 \times 0.442 = 37.93$ ... and $73.53 \times 0.396 = 29.14$"; the AA cond. fooling cells are 55.78 and 60.37 (1 minus these = 0.4422 and 0.3963).
- [T2-13] Same quantity in another table: PGD-10 cond. fooling for ResNet-18 AT is 48.58±0.80 here and 48.52±0.84 on the Table 4 diagonal (line 159); ViT-Tiny AT 55.53±0.50 here and 55.57±0.44 on the Table 4 diagonal (line 163). Both say "mean±std over three" runs/seed pairs; the aggregation difference is not stated in either caption.
- [T2-14] First reference: 04_experiments.tex:41 "The CNN also retains higher clean accuracy ($85.78$ vs $73.53\%$, a 12.3-point gap), reflecting the difficulty of training ViTs on small datasets from scratch; Table~\ref{tab:conditional} separates that contribution from conditional susceptibility." (the paragraph that cites it first appears before the float at line 43). Second: line 64 "Table~\ref{tab:conditional} decomposes the absolute scores into their clean-accuracy and conditional-susceptibility components (Section~\ref{subsec:metrics})."


### T3: Table 3 (`tab:transfer_protocols`)

Render: `teslim/render_2026-10-04/sayfa_09.png (page 9)`. Source: `paper/manuscript/sections/04_experiments.tex:86-103`.

```latex
86: \begin{table}[!t]
87: \centering
88: \caption{Transfer asymmetry under the unconditioned rate and three established conditioning protocols (PGD-10, $\eps$=8/255, full test set; mean$\pm$std over three seed pairs). The rightmost column repeats the difference measured on our earlier single-run checkpoints.}
89: \label{tab:transfer_protocols}
90: \footnotesize
91: \setlength{\tabcolsep}{3pt}
92: \begin{tabular}{lcccc}
93: \toprule
94: \textbf{Protocol} & \textbf{CNN$\rightarrow$ViT} & \textbf{ViT$\rightarrow$CNN} & \textbf{Diff.} & \textbf{Diff.}$^{\ddagger}$ \\
95: \midrule
96: Unconditioned (raw) & 41.02$\pm$0.55 & 27.45$\pm$0.27 & $+$13.57$\pm$0.33 & $+$8.27 \\
97: Target-correct & 19.87$\pm$0.18 & 15.51$\pm$0.59 & $+$4.36$\pm$0.44 & $+$0.63 \\
98: Both-correct & 18.25$\pm$0.17 & 9.98$\pm$0.31 & $+$8.27$\pm$0.23 & $+$5.33 \\
99: Successful-source & 36.39$\pm$0.76 & 17.02$\pm$0.52 & $+$19.37$\pm$1.27 & $+$11.17 \\
100: \bottomrule
101: \multicolumn{5}{l}{\scriptsize $^{\ddagger}$Single run, validation split seen during clean pre-training.}
102: \end{tabular}
103: \end{table}
```

- [T3-1] Placement: right column of page 9, middle. PDF text extent x = 300.6 to 558.7 pt (the row "+19.37±1.27 +11.17" ends at 558.7), against right column edge 539.4 pt: overrun 19.3 pt. In the render the last column "Diff.‡" (x 534.9 to 556.6) extends into the right margin, and the "+19.37±1.27" and "+11.17" cells almost touch.
- [T3-2] Columns: 5, `lcccc` (line 92); headers `Protocol`, `CNN$\rightarrow$ViT`, `ViT$\rightarrow$CNN`, `Diff.`, `Diff.$^{\ddagger}$` (line 94). The two last columns share the same header text "Diff.", distinguished only by the mark.
- [T3-3] Rules: booktabs; `\toprule`, `\midrule`, `\bottomrule` (lines 93, 95, 100); no vertical lines.
- [T3-4] Size: `\footnotesize` with `\setlength{\tabcolsep}{3pt}` (lines 90, 91); rendered 8 pt (SFRM0800). The footnote row uses `\scriptsize` (line 101).
- [T3-5] Float: `table`, `[!t]`; not `table*`; wider than the column (T3-1).
- [T3-6] Bold/italic: none in the table body.
- [T3-7] Footnote mark: `$^{\ddagger}$` on the last "Diff." header. Text (line 101): "Single run, validation split seen during clean pre-training." Set as a `\multicolumn{5}{l}{\scriptsize ...}` row after `\bottomrule`. Table 8 also uses `\ddagger` for a different footnote (CIFAR-native ViT); the symbol is reused with different meanings across tables (the dagger in Table 1 differs).
- [T3-8] Sign format: `$+$13.57$\pm$0.33` style, explicit plus sign on all differences (lines 96 to 99); uses the math minus in Table 6.
- [T3-9] Decimals: all two decimals, including ± terms and the single-run column. Consistent.
- [T3-10] Caption (line 88): "Transfer asymmetry under the unconditioned rate and three established conditioning protocols (PGD-10, $\eps$=8/255, full test set; mean$\pm$std over three seed pairs). The rightmost column repeats the difference measured on our earlier single-run checkpoints." States attack, eps, split, seeds (three seed pairs), mean±std. Does not state: n (denominators 10,000, 7,353/8,579, 7,061, 2,831/3,814 appear only in body, rendered page 9 text), units (percentage points), the sign convention (Diff. = CNN→ViT minus ViT→CNN is implicit; header says no "(pp)"), the unit of the cells (%), the meaning of the std in the Diff. column (the body says it is the std of the paired within-seed difference, rendered page 9 left of "The spread in the Diff. column is the standard deviation of the paired within-seed difference").
- [T3-11] Abbreviations: "Diff." only; "raw" in the first row label "Unconditioned (raw)". Protocol names in the row labels are capitalised hyphen forms (Target-correct, Both-correct, Successful-source); no definition in the caption (defined in Section III-F).
- [T3-12] Arithmetic check by reader of the table (not judgement): 41.02 - 27.45 = 13.57; 19.87 - 15.51 = 4.36; 18.25 - 9.98 = 8.27; 36.39 - 17.02 = 19.37, equal to the printed Diff. means.
- [T3-13] Same quantity vs Table 4: CNN→ViT raw 41.02±0.55 here, 41.07±0.58 in Table 4 (line 160); ViT→CNN raw 27.45±0.27 here, 27.45±0.34 in Table 4 (line 162); target-correct CNN→ViT 19.87±0.18 here, 19.93±0.20 in Table 4; target-correct ViT→CNN 15.51±0.59 here, 15.52±0.64 in Table 4. Printed Table 4 raw values give 41.07 - 27.45 = 13.62, against 13.57 here.
- [T3-14] Same quantity vs Table 11: ViT→CNN target-correct for MI-FGSM 15.71±0.60 (Table 11, line 433), against 15.51±0.59 in this table; the body (line 121) states the MI-FGSM bidirectional check uses a different step size and gives "15.42±0.52" as ViT→CNN.
- [T3-15] First reference: no `\ref` to this table before the float; the first body reference is 04_experiments.tex:119 "That shift of $4.77$ points is larger than the run-to-run standard deviation of any protocol in Table~\ref{tab:transfer_protocols} by more than a factor of three, and the other three protocols are unchanged by construction." The preceding text (lines 82 to 85, the paragraph that introduces the protocols) has no explicit mention of "Table 3". The float is at line 86; the first mention is 33 lines later. A later reference is 04_experiments.tex:451, rendered on page 18 as "(Table 3, Diff. column)".


### T4: Table 4 (`tab:transfer_matrix`)

Render: `teslim/render_2026-10-04/sayfa_12.png (page 12)`. Source: `paper/manuscript/sections/04_experiments.tex:149-170`.

```latex
149: \begin{table}[!t]
150: \centering
151: \caption{$3\times3$ transfer matrix (PGD-10, $\eps$=8/255, full test set; mean$\pm$std over three seed pairs; the WideResNet column and row use the single external checkpoint). Raw = unconditioned fooling rate, Cond. = target-correct conditioned rate. Diagonal entries are white-box attacks.}
152: \label{tab:transfer_matrix}
153: \footnotesize
154: \setlength{\tabcolsep}{3pt}
155: \begin{tabular}{llcc}
156: \toprule
157: \textbf{Source} & \textbf{Target} & \textbf{Raw (\%)} & \textbf{Cond. (\%)} \\
158: \midrule
159: ResNet-18 AT & ResNet-18 AT & 55.84$\pm$0.53 & 48.52$\pm$0.84 \\
160: ResNet-18 AT & ViT-Tiny AT & 41.07$\pm$0.58 & 19.93$\pm$0.20 \\
161: ResNet-18 AT & WRN-28-10 & 21.69$\pm$0.09 & 12.48$\pm$0.10 \\
162: ViT-Tiny AT & ResNet-18 AT & 27.45$\pm$0.34 & 15.52$\pm$0.64 \\
163: ViT-Tiny AT & ViT-Tiny AT & 67.34$\pm$0.18 & 55.57$\pm$0.44 \\
164: ViT-Tiny AT & WRN-28-10 & 18.25$\pm$0.12 & 8.65$\pm$0.14 \\
165: WRN-28-10 & ResNet-18 AT & 32.63$\pm$0.14 & 21.48$\pm$0.31 \\
166: WRN-28-10 & ViT-Tiny AT & 39.73$\pm$0.25 & 18.15$\pm$0.28 \\
167: WRN-28-10 & WRN-28-10 & 33.03 & 25.16 \\
168: \bottomrule
169: \end{tabular}
170: \end{table}
```

- [T4-1] Placement: left column of page 12, top; extent x = 54.6 to 259.5 pt, inside left column (36.2 to 277.9). No overflow or cut-off visible.
- [T4-2] Columns: 4, `llcc` (line 155); header `Source`, `Target`, `Raw (\%)`, `Cond. (\%)`. Source name repeated on three consecutive rows (no `\multirow`), which the render shows as repeated "ResNet-18 AT/ViT-Tiny AT/WRN-28-10" blocks without rules between blocks.
- [T4-3] Rules: booktabs; `\toprule`, `\midrule`, `\bottomrule` (lines 156, 158, 168); no vertical lines; no rule or spacing separating the three source blocks, and no marking of the diagonal rows in the table (the caption says diagonal entries are white-box).
- [T4-4] Size: `\footnotesize`, `\tabcolsep` 3pt (lines 153, 154); rendered 8 pt.
- [T4-5] Float: `table`, `[!t]`; fits the column; `table*` not needed.
- [T4-6] Bold/italic: none in the table. The accompanying heat map Figure 4 (page 12, right column) prints the same Cond. values at one decimal with bold on the diagonal (48.5, 55.6, 25.2) while the table prints two decimals (48.52, 55.57, 25.16).
- [T4-7] Footnote marks: none. The WRN rows/column are flagged only in the caption ("the WideResNet column and row use the single external checkpoint").
- [T4-8] Abbreviations: "Raw" and "Cond." are defined in the caption (line 151: "Raw = unconditioned fooling rate, Cond. = target-correct conditioned rate."). "AT" undefined. Table 3 uses "Unconditioned (raw)" and "Target-correct"; Table 2 uses "Cond. fooling".
- [T4-9] Decimals: two decimals everywhere; the WRN-28-10 to WRN-28-10 row has "33.03" and "25.16" without ±, centred. In the render the ± entries and the plain entries are visually offset.
- [T4-10] Caption (line 151): "$3\times3$ transfer matrix (PGD-10, $\eps$=8/255, full test set; mean$\pm$std over three seed pairs; the WideResNet column and row use the single external checkpoint). Raw = unconditioned fooling rate, Cond. = target-correct conditioned rate. Diagonal entries are white-box attacks." States: attack, eps, split, seeds, mean±std, abbreviations, diagonal meaning. Not stated: n, direction convention (row = source, column = target is in the column names only).
- [T4-11] Reader-visible values for the same cells vs Table 3 (see T3-13), vs Table 2 (T2-13), and WRN rows vs Table 1: WRN-28-10 white-box PGD-10 raw 33.03 here equals 100 - 66.92 = 33.08 of Table 1 PGD-10 robust accuracy, 0.05 off (different quantities: Table 1 counts misclassified clean inputs as non-robust).
- [T4-12] First reference: 04_experiments.tex:135 "To quantify the confound, we extend the analysis to a $3\times3$ matrix by adding the WideResNet-28-10 reference as both source and target (Table~\ref{tab:transfer_matrix})." Float at line 149; sole `\ref` in the manuscript sections.


### T5: Table 5 (`tab:cifar100_results`)

Render: `teslim/render_2026-10-04/sayfa_12.png (page 12)`. Source: `paper/manuscript/sections/04_experiments.tex:189-202`.

```latex
189: \begin{table}[!t]
190: \centering
191: \caption{CIFAR-100 replication (mean$\pm$std over three independent training runs per architecture, full test set, $\eps$=8/255). Both models are adversarially trained with the protocol of Section~\ref{subsec:training}. Absolute robustness is lower than on CIFAR-10 for both architectures, and the CNN-over-ViT ordering is unchanged.}
192: \label{tab:cifar100_results}
193: \footnotesize
194: \begin{tabular}{lccc}
195: \toprule
196: \textbf{Model} & \textbf{Clean (\%)} & \textbf{PGD-10 (\%)} & \textbf{AutoAttack (\%)} \\
197: \midrule
198: ResNet-18 AT & 63.86$\pm$1.05 & 19.30$\pm$0.32 & 15.04$\pm$0.54 \\
199: ViT-Tiny AT  & 43.17$\pm$1.10 & 11.15$\pm$0.60 & 8.87$\pm$0.83 \\
200: \bottomrule
201: \end{tabular}
202: \end{table}
```

- [T5-1] Placement: right column of page 12, middle; from the render it lies within the column (about 298 to 541 pt from the pixel position; extents not measured from the PDF text).
- [T5-2] Columns: 4, `lccc` (line 194); header `Model`, `Clean (\%)`, `PGD-10 (\%)`, `AutoAttack (\%)`; no `\setlength{\tabcolsep}` override, so default column spacing (the table is visibly wider-spaced than Tables 3, 4, 6).
- [T5-3] Rules: booktabs; `\toprule`, `\midrule`, `\bottomrule`; no vertical lines.
- [T5-4] Size: `\footnotesize` (line 193); rendered 8 pt.
- [T5-5] Float: `table`, `[!t]`; fits.
- [T5-6] Bold/italic/footnotes: none. Row labels are source-aligned with extra space (`ViT-Tiny AT  &`, line 199).
- [T5-7] Abbreviations: "AutoAttack" written in full in the header, whereas Table 1 uses "AA" and Table 7 uses "AA-L2". "AT" undefined here.
- [T5-8] Decimals: two decimals for all cells and ± terms (63.86±1.05 ... 8.87±0.83). Consistent.
- [T5-9] Caption (line 191): "CIFAR-100 replication (mean$\pm$std over three independent training runs per architecture, full test set, $\eps$=8/255). Both models are adversarially trained with the protocol of Section~\ref{subsec:training}. Absolute robustness is lower than on CIFAR-10 for both architectures, and the CNN-over-ViT ordering is unchanged." States: dataset, seeds, mean±std, split, eps, units via (%) in headers. Does not state: n (10,000 is not given), attack parameters. Caption contains two result-interpretation sentences.
- [T5-10] Number cross-check with body: the CIFAR-100 subsection paragraph beginning "One registered endpoint was missed" states the ViT clean accuracy as 43.17 plus-minus 1.10, the value printed in the table.
- [T5-11] First reference: 04_experiments.tex:220 "SVHN~\cite{netzer2011reading} does not (Table~\ref{tab:cifar100_results} reports the CIFAR-100 absolutes for comparison): adversarially trained under the same recipe, the ResNet reaches $94.27\pm0.70\%$ clean and the ViT $92.42\pm0.56\%$, a gap of $1.85$ points." The CIFAR-100 subsection text (lines 185 to 218, the paragraphs that discuss the CIFAR-100 result) never cites the table; its first citation is in the SVHN subsection, 31 lines after the float (line 189) and after the CIFAR-100 results have been discussed.


### T6: Table 6 (`tab:svhn_protocols`)

Render: `teslim/render_2026-10-04/sayfa_14.png (page 14)`. Source: `paper/manuscript/sections/04_experiments.tex:222-238`.

```latex
222: \begin{table}[!t]
223: \centering
224: \caption{SVHN transfer asymmetry under the four protocols (PGD-10, $\eps$=8/255, full test set $n$=26{,}032; mean$\pm$std over two seed pairs; two architectures only, so no third-architecture control). Unlike CIFAR-10 and CIFAR-100, the sign is not the same in all four rows.}
225: \label{tab:svhn_protocols}
226: \footnotesize
227: \setlength{\tabcolsep}{3pt}
228: \begin{tabular}{lccc}
229: \toprule
230: \textbf{Protocol} & \textbf{CNN$\rightarrow$ViT} & \textbf{ViT$\rightarrow$CNN} & \textbf{Diff.} \\
231: \midrule
232: Unconditioned (raw) & 31.89 & 31.49 & $+$0.39$\pm$0.08 \\
233: Target-correct & 26.32 & 27.33 & $-$1.00$\pm$0.22 \\
234: Both-correct & 25.36 & 25.70 & $-$0.35$\pm$0.01 \\
235: Successful-source & 61.38 & 58.69 & $+$2.70$\pm$0.40 \\
236: \bottomrule
237: \end{tabular}
238: \end{table}
```

- [T6-1] Placement: left column of page 14, top; extent x = 46.0 to 268.0 pt, inside left column. No overflow visible.
- [T6-2] Columns: 4, `lccc` (line 228); header `Protocol`, `CNN$\rightarrow$ViT`, `ViT$\rightarrow$CNN`, `Diff.`.
- [T6-3] Rules: booktabs; `\toprule`, `\midrule`, `\bottomrule`; no vertical lines.
- [T6-4] Size: `\footnotesize`, `\tabcolsep` 3pt.
- [T6-5] Float: `table`, `[!t]`; fits.
- [T6-6] Bold/italic/footnotes: none.
- [T6-7] ± convention: the two direction columns have no ± (31.89, 31.49 ...), only the Diff. column has ± (`$+$0.39$\pm$0.08`). The caption says "mean$\pm$std over two seed pairs" for the table as a whole. In Tables 3 and 4 the direction columns do carry ±.
- [T6-8] Decimals: two decimals throughout. Printed differences: 31.89 - 31.49 = 0.40 (table prints +0.39), 26.32 - 27.33 = -1.01 (prints -1.00), 25.36 - 25.70 = -0.34 (prints -0.35), 61.38 - 58.69 = 2.69 (prints +2.70); the Diff. column is the mean of per-seed differences, which the caption does not say.
- [T6-9] Sign glyphs: `$+$` and `$-$` used (math minus renders as "−").
- [T6-10] Caption (line 224): "SVHN transfer asymmetry under the four protocols (PGD-10, $\eps$=8/255, full test set $n$=26{,}032; mean$\pm$std over two seed pairs; two architectures only, so no third-architecture control). Unlike CIFAR-10 and CIFAR-100, the sign is not the same in all four rows." States attack, eps, n (26,032), seeds (two seed pairs), mean±std. Not stated: units (%), denominators per protocol, sign convention. Caption closes with an interpretive sentence. The body on rendered page 14 says that with two runs the run-to-run standard deviation carries no information.
- [T6-11] "Both-correct" row uses the same naming as Table 3; the first row is "Unconditioned (raw)".
- [T6-12] First reference: 04_experiments.tex:240 "Two of the four protocols report a CNN advantage and two report a ViT advantage (Table~\ref{tab:svhn_protocols})." Float at line 222, 18 lines earlier; the lead-in paragraph (lines 220 to 221) cites Table 5 only.


### T7: Table 7 (`tab:l2_results`)

Render: `teslim/render_2026-10-04/sayfa_14.png (page 14)`. Source: `paper/manuscript/sections/04_experiments.tex:254-267`.

```latex
254: \begin{table}[!t]
255: \centering
256: \caption{Same checkpoints, $L_2$ budget ($\eps$=0.5; mean$\pm$std over three seed pairs). PGD-L2 uses the full test set; AutoAttack-L2 uses a pre-registered $5{,}000$-sample subset, so its clean column differs slightly from the full-set value and the two are not drawn from the same samples.}
257: \label{tab:l2_results}
258: \footnotesize
259: \begin{tabular}{lcccc}
260: \toprule
261: \textbf{Model} & \textbf{Clean} & \textbf{PGD-L2} & \textbf{Clean (5k)} & \textbf{AA-L2} \\
262: \midrule
263: ResNet-18 AT & 85.78 & 63.78$\pm$0.38 & 85.33 & 60.61$\pm$0.42 \\
264: ViT-Tiny AT & 73.53 & 51.72$\pm$0.23 & 73.61 & 49.85$\pm$0.20 \\
265: \bottomrule
266: \end{tabular}
267: \end{table}
```

- [T7-1] Placement: right column of page 14, top; extent x = 303.6 to 546.3 pt against right column edge 539.4 pt: overrun 6.9 pt (the AA-L2 column "60.61±0.42" ends at 546.3 pt); the leftmost table text starts at 303.6 pt against the column left edge 297.6 pt. Visible in the render as the table sitting slightly right of the caption and text block.
- [T7-2] Columns: 5, `lcccc` (line 259); header `Model`, `Clean`, `PGD-L2`, `Clean (5k)`, `AA-L2`. No `\tabcolsep` override.
- [T7-3] Rules: booktabs; no vertical lines.
- [T7-4] Size: `\footnotesize` (line 258); rendered 8 pt.
- [T7-5] Float: `table`, `[!t]`; slightly wider than the column.
- [T7-6] Bold/italic/footnotes: none.
- [T7-7] Abbreviations: "PGD-L2", "AA-L2", "Clean (5k)" are not defined in a header note; "5k" is explained only through the caption's "pre-registered 5,000-sample subset". Table 1 labels the corresponding Linf column "AA", Table 5 "AutoAttack".
- [T7-8] ± convention: the two Clean columns have no ± (85.78, 73.53; 85.33, 73.61); the attack columns have ±. The first Clean column duplicates Table 1 Clean mean (85.78, 73.53) without its std (0.36, 0.55).
- [T7-9] Decimals: two decimals everywhere.
- [T7-10] Caption (line 256): "Same checkpoints, $L_2$ budget ($\eps$=0.5; mean$\pm$std over three seed pairs). PGD-L2 uses the full test set; AutoAttack-L2 uses a pre-registered $5{,}000$-sample subset, so its clean column differs slightly from the full-set value and the two are not drawn from the same samples." Caption does not name the dataset (CIFAR-10 appears in the body), the units (%), or the PGD-L2 step. The caption starts with "Same checkpoints", referring to the text, so the caption is not self-contained.
- [T7-11] Content/body mismatch (stated as a fact of locations): the body sentence at 04_experiments.tex:269 cites this table for protocol asymmetries ("The four protocols (Table~\ref{tab:l2_results}) report asymmetries of $+13.03\pm0.81$ (unconditioned), $+2.12\pm0.18$ (target-correct), $+4.07\pm0.36$ (both-correct) and $+12.06\pm0.23$ (successful-source)."); the table (lines 259 to 266) contains only Clean, PGD-L2, Clean (5k), AA-L2 for two models and none of those four asymmetry values. A search of the table source finds none of 13.03, 2.12, 4.07 or 12.06.
- [T7-12] First reference: 04_experiments.tex:269, the sentence quoted in T7-11; float at line 254, 15 lines earlier.


### T8: Table 8 (`tab:gradient`)

Render: `teslim/render_2026-10-04/sayfa_15.png (page 15)`. Source: `paper/manuscript/sections/04_experiments.tex:281-301`.

```latex
281: \begin{table}[!t]
282: \centering
283: \caption{Gradient characteristics computed from per-sample loss gradients ($n$=500 test samples per run; mean$\pm$std over three runs).}
284: \label{tab:gradient}
285: \footnotesize
286: \setlength{\tabcolsep}{2.5pt}
287: \begin{tabular}{lccc}
288: \toprule
289: \textbf{Metric} & \textbf{ResNet-18 AT} & \textbf{ViT-Tiny AT} & \textbf{ViT (native)$^\ddagger$} \\
290: \midrule
291: Hoyer sparsity & \textbf{0.4928}$\pm$0.0120 & 0.4561$\pm$0.0055 & 0.405 \\
292: Gini coefficient & \textbf{0.6498}$\pm$0.0089 & 0.6099$\pm$0.0051 & 0.571 \\
293: Frac.\ $<$1\% of max & \textbf{34.8\%}$\pm$2.1 & 26.8\%$\pm$0.9 & 17.9\% \\
294: Alignment (absolute) & 0.0378$\pm$0.0009 & \textbf{0.0562}$\pm$0.0004 & 0.079 \\
295: Alignment (signed) & 0.0014 & 0.0005 & -- \\
296: \bottomrule
297: \multicolumn{4}{l}{\scriptsize $^\ddagger$CIFAR-native ViT control (4$\times$4 patches, 5.4M params); a single}\\
298: \multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}checkpoint predating the fixed-split protocol, selected on the}\\
299: \multicolumn{4}{l}{\scriptsize \phantom{$^\ddagger$}test set, included only for the sign of the upsampling effect.}
300: \end{tabular}
301: \end{table}
```

- [T8-1] Placement: left column of page 15, top; extent x = 38.7 to 274.4 pt, inside left column (36.2 to 277.9). Footnote lines to x = 267.2 pt. No overflow visible.
- [T8-2] Columns: 4, `lccc` (line 287); header `Metric`, `ResNet-18 AT`, `ViT-Tiny AT`, `ViT (native)$^\ddagger$`.
- [T8-3] Rules: booktabs; no vertical lines.
- [T8-4] Size: `\footnotesize`, `\tabcolsep` 2.5pt; footnote `\scriptsize` (rendered 7 pt, SFRM0700).
- [T8-5] Float: `table`, `[!t]`; fits.
- [T8-6] Bold: `\textbf{0.4928}$\pm$0.0120` style (mean only, ± outside, lines 291 to 294) on the larger value per row for the first three metrics (ResNet) and on `\textbf{0.0562}` for absolute alignment (ViT); the last row has no bold. Not explained in the caption. Not visibly bold in the render (X-1).
- [T8-7] Footnote mark `$^\ddagger$` on the header "ViT (native)". Text (lines 297 to 299): "CIFAR-native ViT control (4$\times$4 patches, 5.4M params); a single checkpoint predating the fixed-split protocol, selected on the test set, included only for the sign of the upsampling effect." Typeset as three manually broken `\multicolumn{4}{l}` rows.
- [T8-8] Decimals: four decimals for the first two columns (0.4928±0.0120), but three decimals in the native column (0.405, 0.571, 0.079), one decimal for the percentage row (34.8%±2.1, 17.9%) and ± on that row has one decimal, while the two-model columns of the other rows have four decimals on ±. Alignment (signed) is 0.0014 and 0.0005 with four decimals and no ±. So decimals differ between columns of the same row.
- [T8-9] Percent sign placement: row "Frac. <1% of max" writes `34.8\%$\pm$2.1` (the % between mean and ±, the ± term without %), unlike Tables 2 to 5 where % is in the header.
- [T8-10] Abbreviations/terms: "Hoyer sparsity", "Gini coefficient", "Frac. <1% of max", "Alignment (absolute/signed)" are not defined in the caption (defined in Section III-F, referenced in body line 279); "AT" undefined; "native" is explained in the footnote.
- [T8-11] Caption (line 283): "Gradient characteristics computed from per-sample loss gradients ($n$=500 test samples per run; mean$\pm$std over three runs)." States n, seeds, mean±std. No direction-of-goodness note (sparser = larger Hoyer/Gini), no eps or attack (it is gradients of the loss, so no attack), no dataset name.
- [T8-12] First reference: 04_experiments.tex:279 "Table~\ref{tab:gradient} summarizes the key statistics using scale-invariant sparsity measures (Section~\ref{subsec:metrics}); gradients are computed with per-sample losses so that norms do not depend on the evaluation batch size."


### T9: Table 9 (`tab:spatial`)

Render: `teslim/render_2026-10-04/sayfa_15.png (page 15)`. Source: `paper/manuscript/sections/04_experiments.tex:315-331`.

```latex
315: \begin{table}[!t]
316: \centering
317: \caption{Spatial locality of input gradients ($n$=500 samples per run; mean$\pm$std over three runs). Paired differences are computed on the same samples. Inference is at the run level: $p$ is a one-sample $t$-test on the three per-run mean differences, Holm-corrected across the four measures, so that the unit of inference matches the unit of the claim. Lower area and entropy mean more localized; higher Moran's $I$ means more clustered.}
318: \label{tab:spatial}
319: \footnotesize
320: \setlength{\tabcolsep}{2.5pt}
321: \begin{tabular}{lcccc}
322: \toprule
323: \textbf{Measure} & \textbf{ResNet-18} & \textbf{ViT-Tiny} & \textbf{Diff.} & \textbf{$p$} \\
324: \midrule
325: Area for 50\% energy & 0.0378$\pm$0.0017 & 0.0397$\pm$0.0010 & $-$0.0019 & 0.54 \\
326: Area for 90\% energy & 0.2345$\pm$0.0078 & 0.2570$\pm$0.0067 & $-$0.0224 & 0.40 \\
327: Spatial entropy (nat) & 5.2014$\pm$0.0387 & 5.2524$\pm$0.0197 & $-$0.0509 & 0.54 \\
328: Moran's $I$ & 0.4141$\pm$0.0132 & 0.3941$\pm$0.0024 & $+$0.0200 & 0.47 \\
329: \bottomrule
330: \end{tabular}
331: \end{table}
```

- [T9-1] Placement: right column of page 15, top; extent x = 300.1 to 550.7 pt against right column edge 539.4 pt: overrun 11.3 pt, at the "p" column (header "p", values 0.54, 0.40, 0.54, 0.47 end at 550.7). Visible in the render: the p column sits at the page margin to the right of the text block.
- [T9-2] Columns: 5, `lcccc` (line 321); header `Measure`, `ResNet-18`, `ViT-Tiny`, `Diff.`, `$p$`. Model names here lack the "AT" suffix used by Tables 2, 3, 4, 5, 7, 8, 10.
- [T9-3] Rules: booktabs; no vertical lines.
- [T9-4] Size: `\footnotesize`, `\tabcolsep` 2.5pt.
- [T9-5] Float: `table`, `[!t]`; overruns the column.
- [T9-6] Bold/italic/footnotes: none in cells. Header `$p$` and `Moran's $I$` in math italic.
- [T9-7] Decimals: four decimals for the means and ± terms and for Diff.; two decimals for p. Consistent within columns.
- [T9-8] Diff. column carries no ±; its sign convention (ResNet minus ViT) is not stated. Caption states "Paired differences are computed on the same samples", while the Diff. column printed equals the difference of the printed means (0.0378 - 0.0397 = -0.0019; 0.2345 - 0.2570 = -0.0225 printed -0.0224).
- [T9-9] Caption (line 317): "Spatial locality of input gradients ($n$=500 samples per run; mean$\pm$std over three runs). Paired differences are computed on the same samples. Inference is at the run level: $p$ is a one-sample $t$-test on the three per-run mean differences, Holm-corrected across the four measures, so that the unit of inference matches the unit of the claim. Lower area and entropy mean more localized; higher Moran's $I$ means more clustered." Five-sentence caption of five lines in the render (longest caption of the 11). States n, seeds, test, correction, direction. The "p" column does not say whether it is Holm-adjusted in its own header.
- [T9-10] Unit for entropy given in the row label "(nat)"; "Area for 50% energy" has no unit (a fraction of image area, per body).
- [T9-11] First reference: 04_experiments.tex:303 "At the run level, which is the unit an architectural claim needs and the unit Table~\ref{tab:spatial} uses, three paired runs give raw $p$ of $0.036$, $0.042$ and $0.067$ for Gini, the sub-1\% fraction and Hoyer, which Holm correction across the three measures raises to $0.108$." (this precedes the float at line 315 by 12 lines and the discussion of spatial results at 333). Next: line 333 "The result is negative (Table~\ref{tab:spatial})."


### T10: Table 10 (`tab:feature_degradation`)

Render: `teslim/render_2026-10-04/sayfa_16.png (page 16)`. Source: `paper/manuscript/sections/04_experiments.tex:361-386`.

```latex
361: \begin{table}[!t]
362: \centering
363: \caption{Block-wise clean-to-adversarial cosine similarity under each model's own white-box PGD-10 attack ($n$=1000 per run; mean over three runs). All summaries are taken at the residual block output, so the ViT and CNN columns are measured at equivalent points; the ViT columns differ only in how a block's tokens are aggregated. Figures for the MLP sub-block output are given in the text.}
364: \label{tab:feature_degradation}
365: \footnotesize
366: \setlength{\tabcolsep}{2.5pt}
367: \begin{tabular}{lccc|lc}
368: \toprule
369: \multicolumn{4}{c|}{\textbf{ViT-Tiny AT}} & \multicolumn{2}{c}{\textbf{ResNet-18 AT}} \\
370: \textbf{Blk} & \textbf{CLS} & \textbf{Patch mean} & \textbf{All tokens} & \textbf{Block} & \textbf{Cosine} \\
371: \midrule
372: 1 & 0.9993 & 0.9980 & 0.9927 & layer1.0 & 0.9951 \\
373: 2 & 0.9950 & 0.9959 & 0.9901 & layer1.1 & 0.9918 \\
374: 3 & 0.9902 & 0.9940 & 0.9881 & layer2.0 & 0.9879 \\
375: 4 & 0.9873 & 0.9919 & 0.9861 & layer2.1 & 0.9853 \\
376: 5 & 0.9845 & 0.9904 & 0.9847 & layer3.0 & 0.9753 \\
377: 6 & 0.9814 & 0.9894 & 0.9835 & layer3.1 & 0.9607 \\
378: 7 & 0.9782 & 0.9885 & 0.9826 & layer4.0 & \textbf{0.8777} \\
379: 8 & 0.9743 & 0.9875 & 0.9816 & layer4.1 & 0.9108 \\
380: 9 & 0.9703 & \textbf{0.9870} & 0.9809 & & \\
381: 10 & 0.9661 & 0.9872 & 0.9805 & & \\
382: 11 & \textbf{0.9604} & 0.9874 & \textbf{0.9803} & & \\
383: 12 & 0.9663 & 0.9915 & 0.9837 & & \\
384: \bottomrule
385: \end{tabular}
386: \end{table}
```

- [T10-1] Placement: right column of page 16, middle; extent x = 320.8 to 516.3 pt, inside the right column (297.6 to 539.4). No overflow visible.
- [T10-2] Columns: 6, `lccc|lc` (line 367), the only table in the section with a vertical rule (between "All tokens" and "Block"). Header row 1: `\multicolumn{4}{c|}{ViT-Tiny AT}` and `\multicolumn{2}{c}{ResNet-18 AT}`; row 2: `Blk`, `CLS`, `Patch mean`, `All tokens`, `Block`, `Cosine`. No `\cmidrule` under group headers.
- [T10-3] Rules: booktabs horizontal rules plus the single vertical bar `|` (line 367 and 369). Rendered: the bar extends from the group header down to the last row including the empty CNN cells in rows 9 to 12.
- [T10-4] Size: `\footnotesize`, `\tabcolsep` 2.5pt; rendered 8 pt.
- [T10-5] Float: `table`, `[!t]`; fits.
- [T10-6] Bold: `\textbf{0.9870}` (Patch mean, block 9), `\textbf{0.9604}` (CLS, block 11), `\textbf{0.9803}` (All tokens, block 11), `\textbf{0.8777}` (ResNet layer4.0): the minimum of each series; not explained in the caption; not visibly bold in render (X-1). Note that the minimum of "Patch mean" is at block 9 (0.9870) while block 10 is 0.9872 and block 11 is 0.9874.
- [T10-7] Empty cells: rows 9 to 12 of the ResNet block are empty (`& & \\`, lines 380 to 383) because the CNN has 8 blocks against 12 for the ViT; blank cells are unmarked.
- [T10-8] Different row-index conventions in one table: ViT rows numbered 1 to 12 ("Blk"), CNN rows named "layer1.0 ... layer4.1" ("Block"); the rows are aligned by row position only (ViT block 1 beside layer1.0), with no depth correspondence stated.
- [T10-9] Decimals: four decimals in every cell; no ± anywhere (caption says "mean over three runs", no std).
- [T10-10] Abbreviations: "Blk", "CLS" not defined in the caption; "AT" undefined; "Cosine" is not specified (clean-to-adversarial per caption).
- [T10-11] Caption (line 363): "Block-wise clean-to-adversarial cosine similarity under each model's own white-box PGD-10 attack ($n$=1000 per run; mean over three runs). All summaries are taken at the residual block output, so the ViT and CNN columns are measured at equivalent points; the ViT columns differ only in how a block's tokens are aggregated. Figures for the MLP sub-block output are given in the text." States n, seeds, attack. Not stated: eps (8/255 is not in the caption), dataset, units. The ResNet values quoted in the body "0.8777 ± 0.0181" and "0.9108 ± 0.0060" (rendered page 16, left column) carry a std that the table omits.
- [T10-12] First reference: 04_experiments.tex:392 "Table~\ref{tab:feature_degradation} reports the block-wise profiles." The float is at line 361, 31 lines before the first reference.


### T11: Table 11 (`tab:tgr`)

Render: `teslim/render_2026-10-04/sayfa_18.png (page 18)`. Source: `paper/manuscript/sections/04_experiments.tex:423-437`.

```latex
423: \begin{table}[!t]
424: \centering
425: \caption{ViT$\rightarrow$CNN transfer under TGR~\cite{zhang2023tgr} and plain MI-FGSM at a matched budget ($n$=10{,}000 per run; mean$\pm$std over three runs).}
426: \label{tab:tgr}
427: \footnotesize
428: \begin{tabular}{lcc}
429: \toprule
430: \textbf{Measure (\%)} & \textbf{TGR} & \textbf{MI-FGSM} \\
431: \midrule
432: White-box on source (raw) & 51.56$\pm$0.80 & \textbf{66.43}$\pm$0.29 \\
433: Transfer, target-correct & 12.70$\pm$0.41 & \textbf{15.71}$\pm$0.60 \\
434: Transfer, both-correct & 7.93$\pm$0.42 & \textbf{10.08}$\pm$0.30 \\
435: \bottomrule
436: \end{tabular}
437: \end{table}
```

- [T11-1] Placement: top of the left column of page 18; extent x = 54.4 to 259.7 pt, inside the left column. No overflow.
- [T11-2] Columns: 3, `lcc` (line 428); header `Measure (\%)`, `TGR`, `MI-FGSM`.
- [T11-3] Rules: booktabs; no vertical lines.
- [T11-4] Size: `\footnotesize`; no `\tabcolsep` override.
- [T11-5] Float: `table`, `[!t]`; fits.
- [T11-6] Bold: `\textbf{66.43}$\pm$0.29`, `\textbf{15.71}$\pm$0.60`, `\textbf{10.08}$\pm$0.30` (all three MI-FGSM cells, lines 432 to 434), mean only. Not explained in the caption. In the PDF the three TGR cells and the three MI-FGSM cells use the same font (SFRM0800), i.e. no visible bold.
- [T11-7] Footnote marks: none. Row labels: "White-box on source (raw)", "Transfer, target-correct", "Transfer, both-correct" (lower-case "raw", "target-correct", "both-correct", unlike Table 3's capitalised "Target-correct").
- [T11-8] Decimals: two decimals for all cells and ±. In the render "7.93±0.42" is offset from the other rows of the TGR column because the centred cell is narrower (1-digit integer part).
- [T11-9] Abbreviations: "TGR" is cited (`\cite{zhang2023tgr}`, rendered "[12]") but not spelled out in the caption (spelled out in body, rendered page 18 "Token Gradient Regularization (TGR)"); "MI-FGSM" not spelled out in caption (momentum iterative FGSM; cited in the body at line 121 `\cite{dong2018boosting}`).
- [T11-10] Caption (line 425): "ViT$\rightarrow$CNN transfer under TGR~\cite{zhang2023tgr} and plain MI-FGSM at a matched budget ($n$=10{,}000 per run; mean$\pm$std over three runs)." States n, seeds, mean±std. Not stated: eps, step size (the budget being "matched" is not quantified in the caption), dataset, which models, "(%)" is in the row header. Uses a citation inside a caption.
- [T11-11] Cross-check: this table's MI-FGSM ViT→CNN target-correct is 15.71±0.60; the body at line 121 reports 15.42±0.52 for the MI-FGSM bidirectional check at a different step size and says the difference "is why its ViT→CNN figure differs slightly from the matched-budget value in Table~\ref{tab:tgr}".
- [T11-12] First reference: 04_experiments.tex:121 (in the transfer section, well before the float): "What is stable is the direction: ... which is why its ViT$\rightarrow$CNN figure differs slightly from the matched-budget value in Table~\ref{tab:tgr}), so the effect is not an artifact of the PGD attack itself." The dedicated sentence at line 439 "TGR does not improve transfer in this regime; it degrades it (Table~\ref{tab:tgr})." follows the float (line 423) by 16 lines.


## Cross-table consistency list

- [X-1] Bold and italic do not render in any table. PDF font list (PyMuPDF `get_fonts`, all pages) contains for table text only SFRM0700, SFRM0800, SFRM1000, SFRM0500 plus CM math fonts; there is no SFRM bold or italic. Every `\textbf` in Tables 1, 2, 3 (none), 8, 10, 11 and every `\textit` (Table 1 row groups, Table 2 sub-header) renders in the regular upright weight, as seen in the 260 dpi crops of Tables 1 and 2. Bold is also not explained in any of the 11 captions (checked by reading the 11 caption lines).
- [X-2] Bold-bracket convention differs: `\textbf{37.93$\pm$0.14}` (bold covers ± term, Table 1 lines 27, 32) against `\textbf{48.58}$\pm$0.80` (mean only; Table 2 line 54, Table 8 lines 291 to 294, Table 11 lines 432 to 434).
- [X-3] Tables wider than their column (PDF line extents against column edges 277.9 pt left / 539.4 pt right): Table 1 +31.6 pt, Table 2 +22.7 pt (sub-header row; numeric body +3.3 pt), Table 3 +19.3 pt, Table 9 +11.3 pt, Table 7 +6.9 pt. Tables 4, 6, 8, 10, 11 are inside the column (Table 5 inside by visual inspection only). No `table*` is used in the manuscript; all 11 are `table` with `[!t]`. The IEEE Access class used is two-column.
- [X-4] Font sizes: Tables 1 and 2 `\scriptsize` (7 pt rendered), Tables 3 to 11 `\footnotesize` (8 pt rendered); footnote rows `\scriptsize`. `\tabcolsep` values: 2 pt (T1), 2.5 pt (T2, T8, T9, T10), 3 pt (T3, T4, T6), default (T5, T7, T11).
- [X-5] Rules: booktabs everywhere; the only vertical rule is in Table 10 (`lccc|lc`). `\cmidrule` is not used, although Tables 2 and 10 have grouped headers.
- [X-6] Same quantity, different decimals (decimal count in the table cells): Table 1 two decimals (85.78, 44.11), Table 7 two decimals (63.78); Table 8 four decimals (0.4928) and native column three decimals (0.405) and one decimal for percent (34.8%); Table 9 four decimals with p at two; Table 10 four decimals; Figure 4 prints the conditioned rates at one decimal (48.5) where Table 4 prints two (48.52) (the caption of Figure 4 says "mean over three seed pairs"). Text writes "+4.4" for the same asymmetry that Table 3 prints as +4.36 (line 177).
- [X-7] Same quantity, different values in different tables (all ±, "three" runs/seed pairs): ResNet-18 AT PGD-10 conditioned fooling 48.58±0.80 (T2) vs 48.52±0.84 (T4 diagonal); ViT-Tiny AT 55.53±0.50 (T2) vs 55.57±0.44 (T4); CNN→ViT raw 41.02±0.55 (T3) vs 41.07±0.58 (T4); ViT→CNN raw 27.45±0.27 (T3) vs 27.45±0.34 (T4); CNN→ViT target-correct 19.87±0.18 (T3) vs 19.93±0.20 (T4); ViT→CNN target-correct 15.51±0.59 (T3) vs 15.52±0.64 (T4). No caption states why the aggregations differ.
- [X-8] Different names for the same protocol and quantity: "Unconditioned (raw)" (T3, T6) / "Raw (%)" (T4) / "White-box on source (raw)" (T11); "Target-correct" (T3, T6) / "Cond. (%)" (T4, defined in its caption as target-correct conditioned rate) / "Cond. fooling (%)" (T2, which is the white-box PGD-10 and AA conditioned fooling) / "Transfer, target-correct" (T11) / "Conditioned (target-correct)" (Figure 4 caption, line 177); "Both-correct" (T3, T6) / "Both-correct robust (%)" (T2, a different quantity: robust accuracy on both-correct samples) / "Transfer, both-correct" (T11). The word "Diff." is used for the asymmetry in T3, T6, T9 and "Diff.$^\ddagger$" for the single-run column in T3. Capitalisation: Title case in T3, T6; lower case in T11 row labels.
- [X-9] Different names for the same attack/measure: "AA" (T1, T2), "AutoAttack" (T5), "AA-L2" (T7); "PGD-L2" (T7) vs "PGD-10" elsewhere; "Clean" without units (T1, T7) vs "Clean (%)" (T5).
- [X-10] Different names for the same model: "ResNet-18" + defence column (T1), "ResNet-18 AT" (T2 to T5, T7, T8, T10), "ResNet-18" (T9); "ViT-Tiny" / "ViT-Tiny AT" / "ViT (native)" (T8); "WRN-28-10" (T4) vs "WRN-28-10" with "AT$^\dagger$" (T1); "WideResNet" in captions of T4 vs "WRN-28-10" in cells; "AT" is defined in 02_related_work.tex:23 and 03_methodology.tex:80 only.
- [X-11] "mean±std" wording: every caption writes `mean$\pm$std` (T1 to T9, T11; T10 writes only "mean over three runs" with no std; T1 and T5 write "mean$\pm$std over three independent training runs per architecture"; T2, T8, T9, T11 "over three runs"; T3, T4, T7 "over three seed pairs"; T6 "over two seed pairs"). No caption or table uses "s.d.", "SD" or "std. dev." (grep for "s.d." returned no hits in the sections). Body text writes "standard deviation" in words and prints ± both unspaced (`15.01±0.84`, `37.93±0.14%`) and spaced (`+4.36 ± 0.44`, `51.3 ± 1.8%`) on the same rendered pages 9, 14 and 16; tables always unspaced.
- [X-12] Unit of the replicate in captions: "three independent training runs per architecture" (T1, T5), "three runs" (T2, T8, T9, T10, T11), "three seed pairs" (T3, T4, T7), "two seed pairs" (T6). Six different formulations for the same design.
- [X-13] n in captions: given in T6 (26,032), T8 (500), T9 (500), T10 (1000), T11 (10,000), T2 lower block row (7,260); not given in T1, T3, T4, T5, T7 (5,000 for AA-L2 only). "full test set" stated in T2, T3, T4, T5, T6, T7 (PGD-L2).
- [X-14] Units: percentage signs appear in column headers of T2, T4, T5, T11; in the row label of T8's percentage row; nowhere for T1, T3, T6, T7, T10 (T1 columns are percent accuracies; T3 and T6 contain percentage rates and percentage-point differences).
- [X-15] ± alignment: all numeric columns are `c`; no decimal alignment (`siunitx`, `\sisetup` and `\hphantom` alignment are not used; grep for siunitx returned no hits). Rows mixing "mean±std" and plain numbers in one column appear in T1 (WRN rows), T4 (WRN row), T6, T7 (Clean columns).
- [X-16] Footnote marks: `$^\dagger$` (T1), `$^{\ddagger}$` (T3, header "Diff."), `$^\ddagger$` (T8, header "ViT (native)"). `\ddagger` has two different meanings across T3 and T8. Footnotes are `\multicolumn` rows after `\bottomrule`, manually broken in T1 and T8, one line in T3.
- [X-17] First body reference vs float position (lines): T1 ref line 13 before float 15 (and 03_methodology.tex:69); T2 ref 41 before float 43; T3 float 86, first ref 119 (33 lines after); T4 float 149, ref 135 (before); T5 float 189, ref 220 (31 lines after, first cited in SVHN subsection); T6 float 222, ref 240 (18 after); T7 float 254, ref 269 (15 after; sentence does not match table content, see T7-11); T8 float 281, ref 279 (before); T9 float 315, ref 303 (before); T10 float 361, ref 392 (31 after); T11 float 423, ref 121 (302 lines before) and 439 (16 after).
- [X-18] Captions with interpretive content in addition to description: T2 ("The lower block repeats..."), T5 ("Absolute robustness is lower than on CIFAR-10 ... unchanged"), T6 ("Unlike CIFAR-10 and CIFAR-100, the sign is not the same in all four rows."), T9 (statistical method, five sentences), T10 ("Figures for the MLP sub-block output are given in the text."). Captions that are one sentence: T1 (two), T8, T11.
- [X-19] Table counts: 11 `\begin{table}` blocks in 04_experiments.tex (lines 15, 43, 86, 149, 189, 222, 254, 281, 315, 361, 423); no tables in other sections (grep -c for `begin{table` over sections 01 to 06 and main.tex gives 0, 0, 0, 11, 0, 0, 0).
- [X-20] Table order in the PDF vs numbering: Table 5 (CIFAR-100) is typeset on page 12 right column after Table 4, and Table 6 (SVHN) and Table 7 (L2) are on page 14; Figure 3 (page 10) lies between Table 3 (page 9) and Table 4 (page 12) as in INDEKS.md.
- [X-21] Table width vs caption width: for T1, T2, T3, T9 the caption block (x 36.2 to 275.0 or 297.6 to 539.4) is narrower than the table below it.
- [X-22] Rendering resolution note: in the 110 dpi page PNG the Table 7 caption "5,000" appears as "5.000" (glyph looks dot-like); the PDF text layer holds "5,000" (checked by text extraction).
