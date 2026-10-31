<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-10-31T20:20:22+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig12_estimates_forest | 97.6 | 97.6 | 85/85 = 100.0 (90 = 76.5) | PASS | PASS | - | 0 |

## fig12_estimates_forest -- ayarli: 97.6/100 PASS (ceiling 85/85 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.77pt, venue 241.77pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.00pt on '−0.6' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | sizes [8.0, 9.0] [style 7 sizes [8.0, 8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 5.000in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [1.4, 69.4], bottom edges [139.2, 166.1, 307.0] |
| B1 Every colour bound in the palette | 5/5 | PASS | 6 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig12_estimates_forest.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig12_estimates_forest renders as Figure 12 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D1 No dual axis | 4/4 | PASS | built with figspec, which blocks twinx |
| D2 Axis conventions | 3/3 | PASS | enforced by figspec at draw time |
| D3 Error-bar semantics declared in the caption | 3/3 | PASS | figure drew ['ci90', 'ci95']; caption declares it |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated per panel, or exempt with a reason | 2/2 | PASS | 2 'n = ...' annotations for 2 of 3 panels; exempt:  (a key to the marks) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Registered sigma contrasts and directional terms with 90% and 95% intervals on t... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 3/3 richness items pass; distance to the liked reference 3.209 (0/5 on the disliked side); catalogue 0.427 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |

## fig12_estimates_forest -- kati: 97.6/100 PASS (ceiling 85/85 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.77pt, venue 241.77pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.00pt on '−0.6' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | sizes [8.0, 9.0] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 5.000in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [1.4, 69.4], bottom edges [139.2, 166.1, 307.0] |
| B1 Every colour bound in the palette | 5/5 | PASS | 6 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 2 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig12_estimates_forest.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig12_estimates_forest renders as Figure 12 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D1 No dual axis | 4/4 | PASS | built with figspec, which blocks twinx |
| D2 Axis conventions | 3/3 | PASS | enforced by figspec at draw time |
| D3 Error-bar semantics declared in the caption | 3/3 | PASS | figure drew ['ci90', 'ci95']; caption declares it |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated per panel, or exempt with a reason | 2/2 | PASS | 2 'n = ...' annotations for 2 of 3 panels; exempt:  (a key to the marks) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 57 words, 0 in mandatory sentences, 57 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Registered sigma contrasts and directional terms with 90% and 95% intervals on t... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 3/3 richness items pass; distance to the liked reference 3.209 (0/5 on the disliked side); catalogue 0.427 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |

F: kar/cm² 3.38 [2.30-4.30] · yazı kutusu 0.18 [0.13-0.28] · sayısal 0.21 · veri alanı 0.67 · derinlik 4 · akış 0/0 etiketli · ton 0.78 [0.06-0.49] · mürekkep 0.069 | beğeniye uzaklık 3.21 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 17 figures share one design system (palettes ['adeb_konsey_uslup_7', 'adeb_konsey_uslup_8'] compared by their colour bindings; 22 entity name(s) shared, none bound twice)
