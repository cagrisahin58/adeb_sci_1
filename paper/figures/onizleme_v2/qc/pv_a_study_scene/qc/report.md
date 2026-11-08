<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-07T21:29:53+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| pv_a_study_scene | 97.3 | 91.7 | 76.5/78 = 98.1 (90 = 70.2) | PASS | PASS | - | 1 |

## pv_a_study_scene -- ayarli: 97.3/100 PASS (ceiling 75/75 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.25pt, venue 503.23pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.25pt on 'V-scr' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.25->8, 8.275->8, 9.775->10 (Visio lattice 0.75 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.0, 8.4, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.177in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.5, 80.2], bottom edges [195.3, 258.6, 263.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 53 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes pv_a_study_scene (no extension; the PDF beside it is what pdflatex takes) |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.075 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | C4: warning only in the project settings; pv_a_study_scene does not follow the name scheme and is not in the install mapping; renders as Figure 1 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |
| _warning_ | - | WARN | C4: pv_a_study_scene does not follow the name scheme and is not in the install mapping; renders as Figure 1 |

## pv_a_study_scene -- kati: 91.7/100 PASS (ceiling 76.5/78 = 98.1)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.25pt, venue 503.23pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.25pt on 'V-scr' |
| A3 All sizes on the derived 3-step scale | 1/4 | WARN | sizes [8.25, 8.28, 9.78]; off-scale [8.25, 8.28, 9.78] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 4.177in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [3.5, 80.2], bottom edges [195.3, 258.6, 263.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 53 colours, all bound |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes pv_a_study_scene (no extension; the PDF beside it is what pdflatex takes) |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): model and run counts are printed at each station |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 56 words, 0 in mandatory sentences, 56 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Study design as one scene: trained models and fixed reference panels give transf... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 11/11 richness items pass; distance to the liked reference 0.0 (0/5 on the disliked side); catalogue 0.075 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | C4: warning only in the project settings; pv_a_study_scene does not follow the name scheme and is not in the install mapping; renders as Figure 1 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _warning_ | - | WARN | C4: pv_a_study_scene does not follow the name scheme and is not in the install mapping; renders as Figure 1 |

F: kar/cm² 3.98 [2.30-4.30] · yazı kutusu 0.23 [0.13-0.28] · sayısal 0.13 · veri alanı 0.25 · derinlik 4 · akış 2/1 etiketli · ton 0.31 [0.06-0.49] · mürekkep 0.119 | beğeniye uzaklık 0.00 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 3 figures share one design system
