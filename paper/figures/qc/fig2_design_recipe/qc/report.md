<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-10-31T20:20:05+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig2_design_recipe | 97.4 | 94.4 | 79.5/81 = 98.1 (90 = 72.9) | PASS | PASS | - | 0 |

## fig2_design_recipe -- ayarli: 97.4/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'ViT-Tiny: ' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | printed 9.024->9, 10.849->10.9 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]); off-scale [8.399, 8.424] [style 8 sizes [8.0, 9.0, 10.9]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.467in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 11 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig2_design_recipe.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig2_design_recipe renders as Figure 2 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): the recipe figure draws no sample size |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The two-by-two design (architecture by initialisation) and the bridge cell, with... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.112 (1/5 on the disliked side); catalogue 1.799 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig2_design_recipe -- kati: 94.4/100 PASS (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind single: canvas 241.80pt, venue 241.77pt, scale 0.9999 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'ViT-Tiny: ' |
| A3 All sizes on the derived 3-step scale | 1/4 | WARN | sizes [8.4, 8.42, 9.02, 10.85]; off-scale [8.4, 8.42, 10.85] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.467in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 11 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig2_design_recipe.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig2_design_recipe renders as Figure 2 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): the recipe figure draws no sample size |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The two-by-two design (architecture by initialisation) and the bridge cell, with... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 6/6 richness items pass; distance to the liked reference 1.112 (1/5 on the disliked side); catalogue 1.799 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 6.84 [2.30-4.30] · yazı kutusu 0.44 [0.13-0.28] · sayısal 0.33 · veri alanı - · derinlik 3 · akış 0/0 etiketli · ton 0.39 [0.06-0.49] · mürekkep 0.216 | beğeniye uzaklık 1.11 (1/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 17 figures share one design system (palettes ['adeb_konsey_uslup_7', 'adeb_konsey_uslup_8'] compared by their colour bindings; 22 entity name(s) shared, none bound twice)
