<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-08T16:08:29+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig11_gradient_alignment | 93.6 | 89.5 | 79.5/81 = 98.1 (90 = 72.9) | PASS | BLOCK | - | 0 |

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
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig11_gradient_alignment (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig11_gradient_alignment: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 6 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 55 words, 0 in mandatory sentences, 55 counted; limit 60 on ieee_access; lead-in yes |
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
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig11_gradient_alignment (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig11_gradient_alignment: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | 6 'n = ...' annotation(s) |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 55 words, 0 in mandatory sentences, 55 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | Input-gradient cosine rises with symmetric similarity on all three data sets, ra... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.092 (0/5 on the disliked side); catalogue 0.476 |
| _skipped_ | - | SKIP | B2-B5: no manifest entities, entity styles unknown |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.29 [2.30-4.30] · yazı kutusu 0.13 [0.13-0.28] · sayısal 0.48 · veri alanı 0.59 · derinlik 2 · akış 1/1 etiketli · ton 0.67 [0.86-0.92] · mürekkep 0.121 | beğeniye uzaklık 0.09 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 14 figures share one design system
