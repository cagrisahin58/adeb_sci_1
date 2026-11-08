<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-07T21:31:12+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| pv_c_relief | 97.8 | 93.0 | 91.5/93 = 98.4 (90 = 83.7) | PASS | PASS | - | 1 |

## pv_c_relief -- ayarli: 97.8/100 PASS (ceiling 90/90 = 100.0)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.25pt, venue 503.23pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.27pt on 'V-scr' |
| A3 All sizes on the derived 3-step scale | 4/4 | PASS | printed 8.275->8, 9.775->10, 9.8->10 (Visio lattice 0.75 pt, manifest; venue steps [8.0, 9.0, 10.0]) [style Z sizes [8.0, 8.4, 9.6]] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.500in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [61.1, 71.7, 240.9, 241.4], bottom edges [241.4, 241.6, 245.2, 249.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 26 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.5 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes pv_c_relief (no extension; the PDF beside it is what pdflatex takes) |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 1 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 51 words, 0 in mandatory sentences, 51 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | CIFAR-10 split-half log tau-bar as a relief: colour gives the measured bin, the ... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.507 (2/5 on the disliked side); catalogue 0.094 |
| _skipped_ | - | SKIP | C4: warning only in the project settings; pv_c_relief does not follow the name scheme and is not in the install mapping; renders as Figure 1 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |
| _warning_ | - | WARN | C4: pv_c_relief does not follow the name scheme and is not in the install mapping; renders as Figure 1 |

## pv_c_relief -- kati: 93.0/100 PASS (ceiling 91.5/93 = 98.4)

| Check | Pts | Status | Detail |
|---|---:|---|---|
| A1 Placed scale within 2% of 1.000 | 6/6 | PASS | kind double: canvas 503.25pt, venue 503.23pt, scale 1.0000 |
| A2 Minimum rendered type >= 8pt | 8/8 | PASS | smallest 8.27pt on 'V-scr' |
| A3 All sizes on the derived 3-step scale | 1/4 | WARN | sizes [8.28, 9.78, 9.8]; off-scale [8.28, 9.78, 9.8] |
| A4 Height within the float budget (no tolerance) | 4/4 | PASS | 3.500in vs budget 6.509in |
| A5 No dead margin band over 6% | 4/4 | PASS | margins balanced |
| A6 Panel frames aligned | 2/4 | WARN | left edges [61.1, 71.7, 240.9, 241.4], bottom edges [241.4, 241.6, 245.2, 249.7] |
| B1 Every colour bound in the palette | 5/5 | PASS | 26 colours, all bound |
| B2 CVD separation, or redundant channels | 5/5 | PASS | worst CVD dE 7.5 (mitigated by marker/linestyle/hatch) |
| B3 Greyscale separation, or redundant channels | 4/4 | PASS | worst dL* 10.0 |
| B4 Every series has a non-colour channel | 3/3 | PASS | all series redundant |
| B5 Low-contrast series carry direct labels | 3/3 | PASS | ok |
| C1 Fonts embedded, zero Type 3 | 6/6 | PASS | 4 fonts, all embedded |
| C2 All four formats, PNG above the dpi floor | 4/4 | PASS | have ['pdf', 'eps', 'svg', 'png'], PNG 600dpi |
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes pv_c_relief (no extension; the PDF beside it is what pdflatex takes) |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 1 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 51 words, 0 in mandatory sentences, 51 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | CIFAR-10 split-half log tau-bar as a relief: colour gives the measured bin, the ... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 7/7 richness items pass; distance to the liked reference 0.507 (2/5 on the disliked side); catalogue 0.094 |
| _skipped_ | - | SKIP | C4: warning only in the project settings; pv_c_relief does not follow the name scheme and is not in the install mapping; renders as Figure 1 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _warning_ | - | WARN | C4: pv_c_relief does not follow the name scheme and is not in the install mapping; renders as Figure 1 |

F: kar/cm² 1.89 [2.30-4.30] · yazı kutusu 0.11 [0.13-0.28] · sayısal 0.23 · veri alanı 0.19 · derinlik 3 · akış 0/0 etiketli · ton 0.09 [0.86-0.92] · mürekkep 0.215 | beğeniye uzaklık 0.51 (2/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 3 figures share one design system
