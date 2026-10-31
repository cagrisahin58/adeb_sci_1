<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-10-31T20:20:08+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig6_prereg_chain | 97.4 | 94.4 | 79.5/81 = 98.1 (90 = 72.9) | PASS | PASS | - | 0 |

## fig6_prereg_chain -- ayarli: 97.4/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'C1 pair 3×3' |
| A3 All sizes on the derived 3-step scale | 2/4 | WARN | printed 9.022->9, 9.047->9, 10.846->10.9 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]); off-scale [8.422, 8.447] [style 8 sizes [8.0, 9.0, 10.9]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.575in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 2 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig6_prereg_chain.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig6_prereg_chain renders as Figure 6 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each block prints its model and image counts |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 55 words, 0 in mandatory sentences, 55 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The pre-registration chain: what was seen before registration, the frozen main r... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 2.423 (0/5 on the disliked side); catalogue 0.108 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig6_prereg_chain -- kati: 94.4/100 PASS (ceiling 79.5/81 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.42pt on 'C1 pair 3×3' |
| A3 All sizes on the derived 3-step scale | 1/4 | WARN | sizes [8.42, 8.45, 9.02, 9.05, 10.85]; off-scale [8.42, 8.45, 10.85] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 2.575in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 4/4 | PASS | single panel |
| B1 Every colour bound in the palette | 5/5 | PASS | 2 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 3 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes ../figures/fig6_prereg_chain.pdf |
| C4 Filename matches rendered figure number | 3/3 | PASS | fig6_prereg_chain renders as Figure 6 |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): each block prints its model and image counts |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 55 words, 0 in mandatory sentences, 55 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The pre-registration chain: what was seen before registration, the frozen main r... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 2.423 (0/5 on the disliked side); catalogue 0.108 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.11 [2.30-4.30] · yazı kutusu 0.26 [0.13-0.28] · sayısal 0.26 · veri alanı 0.15 · derinlik 3 · akış 2/2 etiketli · ton 0.70 [0.06-0.49] · mürekkep 0.117 | beğeniye uzaklık 2.42 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 17 figures share one design system (palettes ['adeb_konsey_uslup_7', 'adeb_konsey_uslup_8'] compared by their colour bindings; 22 entity name(s) shared, none bound twice)
