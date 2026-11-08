<!-- scoring: ayarli -->
# Figure QC report

Generated 2026-11-08T14:44:52+00:00; verdict from the ayarli scoring; both scorings are shown, 90 is the line.

| Figure | Adjusted | Strict | Strict ceiling | Verdict | Strict verdict | Blocking | Warnings |
|---|---:|---:|---|---|---|---|---:|
| fig13_protocol_settings | 96.8 | 93.2 | 94.5/96 = 98.4 (90 = 86.4) | PASS | PASS | - | 0 |

## fig13_protocol_settings -- ayarli: 96.8/100 PASS (ceiling 93/93 = 100.0)

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
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig13_protocol_settings (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig13_protocol_settings: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per setting (SVHN two) are drawn as single marks |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The transfer asymmetry of one pair depends on the conditioning protocol in every... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.105 (0/5 on the disliked side); catalogue 0.459 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |
| _skipped_ | - | SKIP | D2: a Visio schematic has no axes; not applied (İSTEM 5A, adjusted scoring) |

## fig13_protocol_settings -- kati: 93.2/100 PASS (ceiling 94.5/96 = 98.4)

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
| C3 Manuscript includes the vector asset | 4/4 | PASS | includes fig13_protocol_settings (no extension; the PDF beside it is what pdflatex takes) |
| C4 Filename matches rendered figure number | 0/3 | WARN | fig13_protocol_settings: a main-text figure name ends in _visio or _chart |
| C5 Manifest present, no AI render, no icon fonts | 3/3 | PASS | provenance=computed |
| D2 Axis conventions | 1.5/3 | WARN | unverified: figure was not drawn through figspec |
| D3 Error-bar semantics declared | 3/3 | PASS | no error bars drawn |
| D4 No text-on-text collisions | 5/5 | PASS | clean |
| D5 No internal experiment codes in the artwork | 3/3 | PASS | clean |
| D6 Sample size stated once in the schematic, or exempt with a reason | 2/2 | PASS | exempt (n_exempt_reason): three seed pairs per setting (SVHN two) are drawn as single marks |
| E1 Caption within the venue's word limit, with a bold lead-in | 4/4 | PASS | 60 words, 0 in mandatory sentences, 60 counted; limit 60 on ieee_access; lead-in yes |
| E2 Manifest states the figure's one-sentence message | 3/3 | PASS | The transfer asymmetry of one pair depends on the conditioning protocol in every... |
| E3 Structural comparison against the liked reference and the catalogue | 3/3 | PASS | 8/8 richness items pass; distance to the liked reference 0.105 (0/5 on the disliked side); catalogue 0.459 |
| _skipped_ | - | SKIP | D1: manifest is not stamped by figspec.export.save; dual-axis status unverified |

F: kar/cm² 2.33 [2.30-4.30] · yazı kutusu 0.15 [0.13-0.28] · sayısal 0.17 · veri alanı 0.47 · derinlik 1 · akış 0/0 etiketli · ton 0.62 [0.86-0.92] · mürekkep 0.136 | beğeniye uzaklık 0.10 (0/5 beğenilmeyen tarafında) | eşikler tamam

## Cross-figure consistency: PASS
- 6 figures share one design system
