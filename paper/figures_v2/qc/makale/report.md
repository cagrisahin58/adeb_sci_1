<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-08T16:09:44+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig10_attack_side | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig11_gradient_alignment | 93.6 | 89.5 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |
| fig12_estimates_forest | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig13_protocol_settings | 94.6 | 91.1 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig14_protocol_sets | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig15_spread_clean_gap | 93.6 | 89.5 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |
| fig16_epsilon_sweep | 97.6 | 93.5 | 83.5/85 = 98.2 (90 = 76.5) | PASS | PASS | - | 0 |
| fig17_feature_degradation | 100.0 | 95.9 | 83.5/85 = 98.2 (90 = 76.5) | PASS | PASS | - | 0 |
| fig1_study_overview | 93.6 | 87.0 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |
| fig2_design_recipe | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 1 |
| fig3_decomposition_schematic | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig4_panel_members | 94.6 | 91.1 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig5_registry_map | 96.2 | 92.0 | 79.5/81 = 98.1 (90 = 72.9) | PASS | PASS | - | 0 |
| fig6_prereg_chain | 93.6 | 89.5 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |
| fig7_source_gap_split | 96.8 | 94.3 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |
| fig8_similarity_matrix | 93.6 | 89.5 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |
| fig9_cells_interaction | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |

## fig10_attack_side -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '1002' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.192in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 14 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig10_attack_side.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig10_attack_side: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): every source is one wire; the twelve sources are listed by seed |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Per source, the chosen attack is PGD-10 or momentum PGD, never TGR; ViT-scr sour... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.353 (2/5 on the disliked side); catalogue 0.067 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig10_attack_side -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '1002' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.192in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 14 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig10_attack_side.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig10_attack_side: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): every source is one wire; the twelve sources are listed by seed |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Per source, the chosen attack is PGD-10 or momentum PGD, never TGR; ViT-scr sour... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.353 (2/5 on the disliked side); catalogue 0.067 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.29 [2.30-4.30] · yazı kutusu 0.14 [0.13-0.28] · sayısal 0.42 · veri alanı 0.55 · derinlik 1 · akış 0/0 etiketli · ton 0.12 [0.86-0.92] · mürekkep 0.138 | beğeniye uzaklık 0.35 (2/5 beğenilmeyen tarafında) | eşikler tamam

## fig11_gradient_alignment -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on ' 1.0' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.397->8.4 (style size), 8.422->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.717in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [44.1, 46.8, 53.4, 193.0], bottom edges [118.7, 234.3, 238.1] |
| B1 Every colour bound in the palette | 5/5 | PASS | 16 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig11_gradient_alignment.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig11_gradient_alignment: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 6 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 53 words, 0 in mandatory sentences, 53 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Input-gradient cosine rises with symmetric similarity on all three data sets, ra... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.092 (0/5 on the disliked side); catalogue 0.476 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig11_gradient_alignment -- kati: 89.5/100 BLOCK (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on ' 1.0' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.717in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [44.1, 46.8, 53.4, 193.0], bottom edges [118.7, 234.3, 238.1] |
| B1 Every colour bound in the palette | 5/5 | PASS | 16 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig11_gradient_alignment.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig11_gradient_alignment: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 6 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 53 words, 0 in mandatory sentences, 53 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Input-gradient cosine rises with symmetric similarity on all three data sets, ra... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.092 (0/5 on the disliked side); catalogue 0.476 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.29 [2.30-4.30] · yazı kutusu 0.13 [0.13-0.28] · sayısal 0.48 · veri alanı 0.59 · derinlik 2 · akış 1/1 etiketli · ton 0.67 [0.86-0.92] · mürekkep 0.121 | beğeniye uzaklık 0.09 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig12_estimates_forest -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'H1 log' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.983in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | left edges [4.3], bottom edges [182.4, 325.3] |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig12_estimates_forest.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig12_estimates_forest: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each card prints its estimate count in the title strip |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | H1 and H2 clear the registered margin on both scales; the directional terms stay... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.063 (0/5 on the disliked side); catalogue 0.569 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig12_estimates_forest -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'H1 log' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.983in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | left edges [4.3], bottom edges [182.4, 325.3] |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig12_estimates_forest.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig12_estimates_forest: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each card prints its estimate count in the title strip |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | H1 and H2 clear the registered margin on both scales; the directional terms stay... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.063 (0/5 on the disliked side); catalogue 0.569 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.99 [2.30-4.30] · yazı kutusu 0.17 [0.13-0.28] · sayısal 0.23 · veri alanı 0.62 · derinlik 3 · akış 0/0 etiketli · ton 0.71 [0.86-0.92] · mürekkep 0.127 | beğeniye uzaklık 0.06 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig13_protocol_settings -- ayarli: 94.6/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'spread' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 5.050in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 20 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.7 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig13_protocol_settings.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig13_protocol_settings: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per setting (SVHN two) are drawn as single marks |
| E1 Caption within the venue's word limit, with a bold lead-in | 2/4 | WARN | 61 words, 0 in mandatory sentences, 61 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The transfer asymmetry of one pair depends on the conditioning protocol in every... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.105 (0/5 on the disliked side); catalogue 0.459 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig13_protocol_settings -- kati: 91.1/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'spread' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 5.050in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 20 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.7 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig13_protocol_settings.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig13_protocol_settings: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per setting (SVHN two) are drawn as single marks |
| E1 Caption within the venue's word limit, with a bold lead-in | 2/4 | WARN | 61 words, 0 in mandatory sentences, 61 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The transfer asymmetry of one pair depends on the conditioning protocol in every... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.105 (0/5 on the disliked side); catalogue 0.459 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.33 [2.30-4.30] · yazı kutusu 0.15 [0.13-0.28] · sayısal 0.17 · veri alanı 0.47 · derinlik 1 · akış 0/0 etiketli · ton 0.62 [0.86-0.92] · mürekkep 0.136 | beğeniye uzaklık 0.10 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig14_protocol_sets -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Unconditioned' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.983in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 34 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.7 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig14_protocol_sets.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig14_protocol_sets: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 5 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The four nested sets give asymmetries from 4.36 to 19.37 points; identity, margi... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.223 (2/5 on the disliked side); catalogue 0.07 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig14_protocol_sets -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Unconditioned' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.983in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 34 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.7 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig14_protocol_sets.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig14_protocol_sets: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 5 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The four nested sets give asymmetries from 4.36 to 19.37 points; identity, margi... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.223 (2/5 on the disliked side); catalogue 0.07 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.20 [2.30-4.30] · yazı kutusu 0.25 [0.13-0.28] · sayısal 0.20 · veri alanı 0.47 · derinlik 2 · akış 3/2 etiketli · ton 0.38 [0.86-0.92] · mürekkep 0.143 | beğeniye uzaklık 0.22 (2/5 beğenilmeyen tarafında) | eşikler tamam

## fig15_spread_clean_gap -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Three-protocol spread' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.325in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [7.1, 11.5, 59.5], bottom edges [107.7, 224.4, 228.2] |
| B1 Every colour bound in the palette | 5/5 | PASS | 19 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig15_spread_clean_gap.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig15_spread_clean_gap: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 1 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 53 words, 0 in mandatory sentences, 53 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The three-protocol spread grows with the clean-accuracy gap as the identity pred... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.167 (0/5 on the disliked side); catalogue 0.188 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig15_spread_clean_gap -- kati: 89.5/100 BLOCK (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Three-protocol spread' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.325in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [7.1, 11.5, 59.5], bottom edges [107.7, 224.4, 228.2] |
| B1 Every colour bound in the palette | 5/5 | PASS | 19 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig15_spread_clean_gap.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig15_spread_clean_gap: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 1 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 53 words, 0 in mandatory sentences, 53 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The three-protocol spread grows with the clean-accuracy gap as the identity pred... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.167 (0/5 on the disliked side); catalogue 0.188 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.72 [2.30-4.30] · yazı kutusu 0.16 [0.13-0.28] · sayısal 0.36 · veri alanı 0.55 · derinlik 2 · akış 0/0 etiketli · ton 0.51 [0.86-0.92] · mürekkep 0.100 | beğeniye uzaklık 0.17 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig16_epsilon_sweep -- ayarli: 97.6/100 PASS (ceiling 82/82 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'points' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.500in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [17.0, 24.0, 31.0], bottom edges [111.4, 128.3, 145.3] |
| B1 Every colour bound in the palette | 5/5 | PASS | 18 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 6.8 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 9.2 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per AT model are stated in the note line, WRN is one model |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Robust accuracy under PGD-10: three cut-out profiles whose heights are the accur... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 0.31 (2/5 on the disliked side); catalogue 0.0 |
| _skipped_ | - | SKIP | C3/C4: not referenced by any float in the manuscript |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |
| _skipped_ | - | SKIP | E1: no caption |

## fig16_epsilon_sweep -- kati: 93.5/100 PASS (ceiling 83.5/85 = 98.2)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'points' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.500in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [17.0, 24.0, 31.0], bottom edges [111.4, 128.3, 145.3] |
| B1 Every colour bound in the palette | 5/5 | PASS | 18 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 6.8 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 9.2 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per AT model are stated in the note line, WRN is one model |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Robust accuracy under PGD-10: three cut-out profiles whose heights are the accur... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 0.31 (2/5 on the disliked side); catalogue 0.0 |
| _skipped_ | - | SKIP | C3/C4: not referenced by any float in the manuscript |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | E1: no caption |

F: kar/cm² 3.20 [2.30-4.30] · yazı kutusu 0.19 [0.13-0.28] · sayısal 0.49 · veri alanı - · derinlik 2 · akış 14/3 etiketli · ton 0.15 [0.86-0.92] · mürekkep 0.234 | beğeniye uzaklık 0.31 (2/5 beğenilmeyen tarafında) | eşikler tamam

## fig17_feature_degradation -- ayarli: 100.0/100 PASS (ceiling 82/82 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '2' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.658in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 23 colours, all bound |
| B2 CVD separation | 5/5 | PASS | single series |
| B3 Greyscale separation | 4/4 | PASS | single series |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three runs per block; the legend says so |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Under its own attack ViT-Tiny's CLS attention entropy stays inside the registere... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 10/10 richness items pass; distance to the liked reference 0.224 (0/5 on the disliked side); catalogue 0.352 |
| _skipped_ | - | SKIP | C3/C4: not referenced by any float in the manuscript |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |
| _skipped_ | - | SKIP | E1: no caption |

## fig17_feature_degradation -- kati: 95.9/100 PASS (ceiling 83.5/85 = 98.2)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on '2' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.658in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 23 colours, all bound |
| B2 CVD separation | 5/5 | PASS | single series |
| B3 Greyscale separation | 4/4 | PASS | single series |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three runs per block; the legend says so |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Under its own attack ViT-Tiny's CLS attention entropy stays inside the registere... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 10/10 richness items pass; distance to the liked reference 0.224 (0/5 on the disliked side); catalogue 0.352 |
| _skipped_ | - | SKIP | C3/C4: not referenced by any float in the manuscript |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | E1: no caption |

F: kar/cm² 2.09 [2.30-4.30] · yazı kutusu 0.13 [0.13-0.28] · sayısal 0.43 · veri alanı 0.45 · derinlik 2 · akış 2/1 etiketli · ton 0.51 [0.86-0.92] · mürekkep 0.173 | beğeniye uzaklık 0.22 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig1_study_overview -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'R224-scr' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.397->8.4 (style size), 8.422->8.4 (style size), 9.597->9.6 (style size), 9.622->9.6 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.175in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.5, 80.2], bottom edges [195.3, 258.6, 263.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 52 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig1_study_overview.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig1_study_overview: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.123 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig1_study_overview -- kati: 87.0/100 BLOCK (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'R224-scr' |
| A3 All sizes on the derived 3-step scale | 0/4 | WARN | sizes [8.4, 8.42, 9.6, 9.62]; off-scale [8.4, 8.42, 9.6, 9.62] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.175in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.5, 80.2], bottom edges [195.3, 258.6, 263.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 52 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig1_study_overview.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig1_study_overview: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.123 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.09 [2.30-4.30] · yazı kutusu 0.25 [0.13-0.28] · sayısal 0.10 · veri alanı 0.19 · derinlik 4 · akış 2/1 etiketli · ton 0.32 [0.06-0.49] · mürekkep 0.122 | beğeniye uzaklık 0.00 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig2_design_recipe -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'R32 bridge, seeds 1001–1003' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.625in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 25 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig2_design_recipe.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig2_design_recipe: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): runs per cell are drawn as index cards and listed by seed |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Two architectures cross two initializations in four cells with their own clean s... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.223 (1/5 on the disliked side); catalogue 0.708 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |
| _warning_ | - | WARN | controller: shape_pairs_checked is 0 and the reason given is: no solid shape |

## fig2_design_recipe -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'R32 bridge, seeds 1001–1003' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.625in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 25 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig2_design_recipe.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig2_design_recipe: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): runs per cell are drawn as index cards and listed by seed |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Two architectures cross two initializations in four cells with their own clean s... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.223 (1/5 on the disliked side); catalogue 0.708 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _warning_ | - | WARN | controller: shape_pairs_checked is 0 and the reason given is: no solid shape |

F: kar/cm² 5.31 [2.30-4.30] · yazı kutusu 0.32 [0.13-0.28] · sayısal 0.31 · veri alanı - · derinlik 3 · akış 0/0 etiketli · ton 0.50 [0.06-0.49] · mürekkep 0.385 | beğeniye uzaklık 1.22 (1/5 beğenilmeyen tarafında) | eşikler tamam

## fig3_decomposition_schematic -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'per pair (i, j)' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.792in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 18 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 5 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig3_decomposition_schematic.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig3_decomposition_schematic: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): a definitional schematic; no sample is drawn |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The log transfer rate splits exactly into vulnerability, similarity and directio... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.173 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig3_decomposition_schematic -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'per pair (i, j)' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.792in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 18 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 5 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig3_decomposition_schematic.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig3_decomposition_schematic: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): a definitional schematic; no sample is drawn |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The log transfer rate splits exactly into vulnerability, similarity and directio... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.173 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 3.85 [2.30-4.30] · yazı kutusu 0.21 [0.13-0.28] · sayısal 0.00 · veri alanı 0.14 · derinlik 2 · akış 3/3 etiketli · ton 0.44 [0.06-0.49] · mürekkep 0.108 | beğeniye uzaklık 0.00 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig4_panel_members -- ayarli: 94.6/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'CIFAR-10 and CIFAR-100' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.750in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [7.9, 15.6], bottom edges [103.9, 297.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| B2 CVD separation | 5/5 | PASS | single series |
| B3 Greyscale separation | 4/4 | PASS | single series |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig4_panel_members.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig4_panel_members: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): every member is one book; the counts are in the evidence file |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The reference panels list every RobustBench member with its role; ImageNetV2 add... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 4/4 richness items pass; distance to the liked reference 2.699 (1/5 on the disliked side); catalogue 0.72 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig4_panel_members -- kati: 91.1/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'CIFAR-10 and CIFAR-100' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.750in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [7.9, 15.6], bottom edges [103.9, 297.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| B2 CVD separation | 5/5 | PASS | single series |
| B3 Greyscale separation | 4/4 | PASS | single series |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig4_panel_members.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig4_panel_members: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): every member is one book; the counts are in the evidence file |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 58 words, 0 in mandatory sentences, 58 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The reference panels list every RobustBench member with its role; ImageNetV2 add... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 4/4 richness items pass; distance to the liked reference 2.699 (1/5 on the disliked side); catalogue 0.72 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 6.22 [2.30-4.30] · yazı kutusu 0.39 [0.13-0.28] · sayısal 0.00 · veri alanı - · derinlik 1 · akış 2/2 etiketli · ton 0.64 [0.06-0.49] · mürekkep 0.198 | beğeniye uzaklık 2.70 (1/5 beğenilmeyen tarafında) | eşikler tamam

## fig5_registry_map -- ayarli: 96.2/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'K-a  ' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.397->8.4 (style size), 8.422->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.467in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 5 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig5_registry_map.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig5_registry_map: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): a registry of thresholds draws no sample |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The registry: every pre-registered test with its quantity, predicted size, falsi... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.141 (0/5 on the disliked side); catalogue 0.694 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig5_registry_map -- kati: 92.0/100 PASS (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'K-a  ' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.467in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 15 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 5 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig5_registry_map.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig5_registry_map: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): a registry of thresholds draws no sample |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The registry: every pre-registered test with its quantity, predicted size, falsi... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.141 (0/5 on the disliked side); catalogue 0.694 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.04 [2.30-4.30] · yazı kutusu 0.24 [0.13-0.28] · sayısal 0.25 · veri alanı 0.13 · derinlik 3 · akış 0/0 etiketli · ton 0.56 [0.06-0.49] · mürekkep 0.272 | beğeniye uzaklık 1.14 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig6_prereg_chain -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'Seen beforehand' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.422->8.4 (style size), 8.447->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.617in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.1, 169.5, 360.2], bottom edges [115.9, 138.5, 166.8] |
| B1 Every colour bound in the palette | 5/5 | PASS | 12 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig6_prereg_chain.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig6_prereg_chain: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each block prints its model and image counts |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The pre-registration chain: what was seen before registration, the frozen main r... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 1.199 (0/5 on the disliked side); catalogue 0.183 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig6_prereg_chain -- kati: 89.5/100 BLOCK (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'Seen beforehand' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.42, 8.45]; off-scale [8.42, 8.45] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.617in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.1, 169.5, 360.2], bottom edges [115.9, 138.5, 166.8] |
| B1 Every colour bound in the palette | 5/5 | PASS | 12 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig6_prereg_chain.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig6_prereg_chain: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each block prints its model and image counts |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The pre-registration chain: what was seen before registration, the frozen main r... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 1.199 (0/5 on the disliked side); catalogue 0.183 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.25 [2.30-4.30] · yazı kutusu 0.26 [0.13-0.28] · sayısal 0.25 · veri alanı - · derinlik 2 · akış 2/2 etiketli · ton 0.59 [0.06-0.49] · mürekkep 0.109 | beğeniye uzaklık 1.20 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig7_source_gap_split -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'pair 1' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.422->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.758in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 14 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig7_source_gap_split.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig7_source_gap_split: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three pairs per data set, each printed on its own row |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | On CIFAR-10 and CIFAR-100 the symmetric part carries 81 to 94 percent of the sou... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.159 (0/5 on the disliked side); catalogue 0.391 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig7_source_gap_split -- kati: 94.3/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'pair 1' |
| A3 All sizes on the derived 3-step scale | 3/4 | WARN | sizes [8.42]; off-scale [8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.758in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 14 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 20.0 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.1 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig7_source_gap_split.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig7_source_gap_split: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three pairs per data set, each printed on its own row |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | On CIFAR-10 and CIFAR-100 the symmetric part carries 81 to 94 percent of the sou... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.159 (0/5 on the disliked side); catalogue 0.391 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.72 [2.30-4.30] · yazı kutusu 0.16 [0.13-0.28] · sayısal 0.37 · veri alanı - · derinlik 2 · akış 0/0 etiketli · ton 0.50 [0.86-0.92] · mürekkep 0.154 | beğeniye uzaklık 0.16 (0/5 beğenilmeyen tarafında) | eşikler tamam

## fig8_similarity_matrix -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on '1' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.422->8.4 (style size), 9.622->9.6 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.825in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [4.8, 26.3], bottom edges [98.0, 105.4] |
| B1 Every colour bound in the palette | 5/5 | PASS | 17 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig8_similarity_matrix.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig8_similarity_matrix: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and pair counts are printed under each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Scratch-trained ViT-Tiny seeds form a block of high mutual similarity that is di... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.218 (2/5 on the disliked side); catalogue 0.0 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig8_similarity_matrix -- kati: 89.5/100 BLOCK (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on '1' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.42, 9.62]; off-scale [8.42, 9.62] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.825in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [4.8, 26.3], bottom edges [98.0, 105.4] |
| B1 Every colour bound in the palette | 5/5 | PASS | 17 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig8_similarity_matrix.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig8_similarity_matrix: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and pair counts are printed under each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Scratch-trained ViT-Tiny seeds form a block of high mutual similarity that is di... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.218 (2/5 on the disliked side); catalogue 0.0 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.97 [2.30-4.30] · yazı kutusu 0.17 [0.13-0.28] · sayısal 0.24 · veri alanı - · derinlik 4 · akış 0/0 etiketli · ton 0.39 [0.86-0.92] · mürekkep 0.138 | beğeniye uzaklık 0.22 (2/5 beğenilmeyen tarafında) | eşikler tamam

## fig9_cells_interaction -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Panel similarity σ' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.399->8.4 (style size), 8.424->8.4 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.400in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 20 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig9_cells_interaction.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig9_cells_interaction: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 3 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 51 words, 0 in mandatory sentences, 51 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | ViT-Tiny's panel similarity rises with ImageNet initialization while ResNet-18's... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.144 (0/5 on the disliked side); catalogue 0.402 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig9_cells_interaction -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'Panel similarity σ' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | sizes [8.4, 8.42]; off-scale [8.4, 8.42] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.400in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 20 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 16.9 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 19.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures_v2/fig9_cells_interaction.pdf |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig9_cells_interaction: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 3 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 51 words, 0 in mandatory sentences, 51 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | ViT-Tiny's panel similarity rises with ImageNet initialization while ResNet-18's... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.144 (0/5 on the disliked side); catalogue 0.402 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.34 [2.30-4.30] · yazı kutusu 0.14 [0.13-0.28] · sayısal 0.26 · veri alanı - · derinlik 2 · akış 2/1 etiketli · ton 0.56 [0.86-0.92] · mürekkep 0.098 | beğeniye uzaklık 0.14 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 17 figures share one design system
