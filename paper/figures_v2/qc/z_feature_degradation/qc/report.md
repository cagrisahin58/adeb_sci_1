<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-08T15:58:26+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig17_feature_degradation | 94.6 | 91.1 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |

## fig17_feature_degradation -- ayarli: 94.6/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '2' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.658in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 23 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 6.3 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 8.6 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig17_feature_degradation (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig17_feature_degradation: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three runs per block; the legend says so |
| E1 Caption within the venue's word limit, with a bold lead-in | 2/4 | WARN | 0 words, 0 in mandatory sentences, 0 counted; limit 60 on ieee_access; lead-in no |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Under its own attack ViT-Tiny's CLS attention entropy stays inside the registere... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 10/10 richness items pass; distance to the liked reference 0.224 (0/5 on the disliked side); catalogue 0.352 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig17_feature_degradation -- kati: 91.1/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '2' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.658in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 23 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 6.3 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 8.6 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig17_feature_degradation (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig17_feature_degradation: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three runs per block; the legend says so |
| E1 Caption within the venue's word limit, with a bold lead-in | 2/4 | WARN | 0 words, 0 in mandatory sentences, 0 counted; limit 60 on ieee_access; lead-in no |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Under its own attack ViT-Tiny's CLS attention entropy stays inside the registere... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 10/10 richness items pass; distance to the liked reference 0.224 (0/5 on the disliked side); catalogue 0.352 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.09 [2.30-4.30] · yazı kutusu 0.13 [0.13-0.28] · sayısal 0.43 · veri alanı 0.45 · derinlik 2 · akış 2/1 etiketli · ton 0.51 [0.86-0.92] · mürekkep 0.173 | beğeniye uzaklık 0.22 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: BLOCK
- entity 'r32' is drawn in more than one colour: #9DBEA3 <- ['fig10_attack_side', 'fig16_epsilon_sweep', 'fig9_cells_interaction']; #E6F5E8 <- ['fig2_design_recipe']
- entity 'r224' is drawn in more than one colour: #594D44 <- ['fig10_attack_side', 'fig9_cells_interaction']; #999188 <- ['fig2_design_recipe']
- entity 'vit' is drawn in more than one colour: #AB6F57 <- ['fig10_attack_side', 'fig16_epsilon_sweep', 'fig17_feature_degradation', 'fig9_cells_interaction']; #D5B09F <- ['fig2_design_recipe']
