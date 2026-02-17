# IEEE Access Pre-Submission Checklist

**Manuscript:** A Comparative Study of Convolutional and Transformer Architectures Under Adversarial Perturbations: Gradient Characteristics and Transferability Analysis

**Target:** IEEE Access (Open Access, Single-Blind Review)

**Date:** 2026-02-16

---

## 1. Manuscript Format and Content

- [x] IEEE Access LaTeX template used (`\documentclass[journal]{IEEEtran}`)
- [x] Title concise and descriptive
- [x] Abstract within word limit (IEEE Access: max 250 words)
- [x] Keywords provided (5 keywords)
- [x] All 6 sections complete (Introduction, Related Work, Methodology, Experiments, Discussion, Conclusion)
- [x] Acknowledgment section included
- [ ] **Author biographies included below references** (IEEE Access REQUIRES short bios for ALL authors)
- [ ] **ORCID iDs for all authors** (submitting author MUST have ORCID linked to IEEE account)
- [x] Double-column IEEE format
- [x] References in IEEE style (`IEEEtran.bst`)

### ACTION REQUIRED:
1. Add author biographies at the end of `main.tex` (before `\end{document}`)
2. Ensure ORCID iD is linked to IEEE Author Portal account

---

## 2. Page Count

- [ ] Page count verified (IEEE Access has NO hard limit but recommends under 20 pages)
- [ ] Excessive length justified by content (if over 20 pages)

### ACTION REQUIRED:
1. Compile LaTeX and count pages
2. If over 20 pages, consider moving supplementary content to appendix or online repository

---

## 3. Figures and Tables

- [x] All 17 figures in PDF format (vector graphics)
- [x] Figures referenced in text
- [x] Figure captions are self-contained
- [ ] **Figure resolution >= 300 DPI** (verify for any rasterized elements)
- [ ] **Individual figure files ready** (PS, EPS, PDF, PNG, or TIF)
- [ ] Color figures noted (no extra charge for IEEE Access, but ensure readability in grayscale)

### Figure Inventory (paper/figures/final/):
| # | File | Description |
|---|------|-------------|
| 1 | fig1_robustness_comparison.pdf | Robustness comparison bar chart |
| 2 | fig2_epsilon_sweep.pdf | Epsilon sweep curves |
| 3 | fig3_transfer_heatmap.pdf | Transfer attack heatmap |
| 4 | fig4_gradient_comparison.pdf | Combined gradient analysis |
| 4a | fig4a_gradient_visualization.pdf | Gradient visualization |
| 4b | fig4b_gradient_distribution.pdf | Gradient distribution |
| 5 | fig5_attention_comparison.pdf | Attention comparison |
| 5a | fig5a_attention_comparison.pdf | Attention map comparison |
| 5b | fig5b_attention_entropy.pdf | Attention entropy |
| 6 | feature_degradation.pdf | Feature degradation analysis |
| 7 | adversarial_samples.pdf | Adversarial sample examples |
| 8 | fig_adversarial_examples.pdf | Adversarial examples display |
| 9 | gradient_comparison.pdf | Gradient comparison |
| 10 | gradient_landscape.pdf | Gradient landscape |
| 11 | gradient_samples_resnet.pdf | ResNet gradient samples |
| 12 | gradient_norm_distribution.pdf | Gradient norm distribution |
| 13 | fig_tsne_features.pdf | t-SNE feature visualization |

### ACTION REQUIRED:
1. Verify all figures compile correctly in the manuscript PDF
2. Confirm no figures are duplicated or unused

---

## 4. References

- [x] 35+ references in `references.bib`
- [x] Recent references included (2023-2025)
- [x] Foundational works cited (Szegedy 2014, Goodfellow 2015, Madry 2018)
- [x] IEEE style bibliography (`IEEEtran.bst`)
- [ ] **No unresolved citations** (no "?" marks in compiled PDF)
- [ ] **All DOIs verified** (recommended for IEEE)
- [ ] **No hallucinated references** (all verified as real publications)

### ACTION REQUIRED:
1. Compile and check for unresolved citation warnings
2. Verify all references exist and are correctly formatted

---

## 5. Declarations and Statements

### Data Availability Statement
**Status:** Needs to be added to manuscript or cover letter
**Recommended text:**
> The experiments in this study use the CIFAR-10 dataset, which is publicly available at https://www.cs.toronto.edu/~kriz/cifar.html. Pre-trained WideResNet-28-10 weights were obtained from the RobustBench benchmark (https://robustbench.github.io/).

### Code Availability Statement
**Status:** Needs to be added
**Recommended text:**
> The source code and trained models used in this study will be made publicly available upon acceptance of the manuscript.

### Conflict of Interest
**Status:** Declared in cover letter
> The authors declare no conflict of interest.

### Funding Statement
**Status:** Needs verification
> [If applicable: "This work was supported by..." / If no funding: "This research received no specific grant from any funding agency."]

### ACTION REQUIRED:
1. Add Data Availability and Code Availability statements to the manuscript (after Conclusion, before References)
2. Confirm funding status with co-author

---

## 6. IEEE Access Portal Requirements

### Account Setup
- [ ] IEEE Author Portal account created (https://ieee.authorportal.elsevier.com/ or ScholarOne)
- [ ] ORCID iD linked to account
- [ ] Affiliation information up to date

### Submission Portal
- **Portal:** IEEE Author Portal (formerly ScholarOne Manuscripts for some IEEE journals)
- **URL:** https://ieee.atyponrex.com/ (IEEE Access specific)
- [ ] Account verified and active

### Article Type
- [ ] "Regular Article" selected (not Brief, Letter, or Review)

### Article Processing Charge (APC)
- **Standard APC:** $2,160 USD (2025/2026 rate, plus applicable local taxes)
- **IEEE Member discount:** 5% (IEEE member) or 20% (IEEE Society member)
- **Low-income country discount:** Available if ALL authors are in eligible countries
- [ ] APC funding confirmed or institutional agreement verified

### ACTION REQUIRED:
1. Create or verify IEEE Author Portal account
2. Confirm APC payment source (institutional, grant, or personal)
3. Check if Firat University has an IEEE open access agreement

---

## 7. Copyright and Licensing

- [ ] IEEE Electronic Copyright Form (eCF) prepared (signed upon acceptance)
- [ ] Creative Commons license selected (IEEE Access uses CC BY 4.0)
- [ ] All third-party content permissions obtained (if any figures/tables reproduced)

### Notes:
- IEEE Access articles are published under CC BY 4.0 license
- No copyright transfer needed for open access (authors retain copyright)
- The eCF is completed during the production process, not at submission

---

## 8. Plagiarism and Overlap

- [ ] Manuscript checked via plagiarism detection tool (iThenticate or Turnitin)
- [ ] Similarity index below 35% (IEEE threshold, especially for conference-to-journal extensions)
- [ ] No conference paper overlap (this is original work, not a conference extension)

### ACTION REQUIRED:
1. Run plagiarism check before submission
2. IEEE will also run iThenticate during review

---

## 9. Submission Files Checklist

| File | Format | Status |
|------|--------|--------|
| Manuscript PDF | PDF | [ ] Compile and verify |
| LaTeX source | ZIP (main.tex + sections/ + references.bib) | [x] Ready |
| Cover letter | PDF (from .tex) | [x] Written |
| Figures | Individual PDF files | [x] 17 files ready |
| Highlights | TXT | [x] Written |
| Suggested reviewers | Internal reference | [x] Prepared |

### ACTION REQUIRED:
1. Compile `cover_letter.tex` to PDF
2. Compile `main.tex` to PDF and verify
3. Create ZIP of LaTeX source files
4. Upload all files to IEEE portal

---

## 10. Final Review Before Submit

- [ ] Title matches across: manuscript, cover letter, portal entry
- [ ] Author names and order: consistent in manuscript, portal, and cover letter
- [ ] No tracked changes, TODO comments, or placeholder text in manuscript
- [ ] No headers/footers from another journal
- [ ] Line numbers NOT required (IEEE Access does not require line numbers)
- [ ] Spell check completed
- [ ] Grammar check completed
- [ ] All cross-references resolve (\ref, \cref commands)
- [ ] All equations numbered correctly
- [ ] Acronyms defined at first use

---

## 11. Timeline

| Step | Target Date | Status |
|------|-------------|--------|
| Submission package preparation | 2026-02-16 | In progress |
| Author biographies added | 2026-02-17 | Pending |
| LaTeX compilation check | 2026-02-17 | Pending |
| Plagiarism check | 2026-02-17 | Pending |
| ORCID and portal setup | 2026-02-17 | Pending |
| APC confirmation | 2026-02-18 | Pending |
| **Submission** | **2026-02-18** | **Pending** |
| Expected review (4-6 weeks) | 2026-04-01 | -- |

---

## Summary of Remaining Actions

### Must Do Before Submission:
1. **Add author biographies** to `main.tex` (IEEE Access mandatory requirement)
2. **Link ORCID** to IEEE Author Portal account
3. **Compile LaTeX** and verify PDF output (no errors, correct page count)
4. **Add data/code availability statements** to manuscript
5. **Confirm APC funding** ($2,160 USD)
6. **Run plagiarism check**

### Recommended:
7. Add DOIs to all references where available
8. Verify figure numbering matches text references
9. Check all URLs in references are accessible
10. Have co-author final review the manuscript
