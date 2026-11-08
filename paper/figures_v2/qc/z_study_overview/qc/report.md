<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-08T20:54:25+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig1_study_overview | 93.6 | 87.0 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |

## fig1_study_overview -- ayarli: 93.6/100 PASS (ceiling 78/78 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.40pt, venue 503.23pt, scale 0.9997 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.40pt on 'R224-scr' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.397->8.4 (style size), 8.422->8.4 (style size), 9.597->9.6 (style size), 9.622->9.6 (style size) (Visio lattice 0.6 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.4, 9.0, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.175in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.5, 80.2], bottom edges [195.3, 258.6, 263.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 53 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig1_study_overview (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig1_study_overview: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.108 |
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
| B1 Every colour bound in the palette | 5/5 | PASS | 53 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig1_study_overview (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig1_study_overview: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 59 words, 0 in mandatory sentences, 59 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.108 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 4.04 [2.30-4.30] · yazı kutusu 0.25 [0.13-0.28] · sayısal 0.11 · veri alanı 0.19 · derinlik 4 · akış 2/1 etiketli · ton 0.45 [0.06-0.49] · mürekkep 0.123 | beğeniye uzaklık 0.00 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 17 figures share one design system
