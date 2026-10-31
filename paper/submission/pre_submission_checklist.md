# IEEE Access Pre-Submission Checklist

**Manuscript:** Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design

**Target:** IEEE Access (Open Access, Single-Blind Review), Regular Article

**Date:** 2026-10-31 (rewritten after the council round and the 31.10 reviewer panel; the 2026-10-04 version carried the previous title and the "conditioning set / source effect" framing and is kept in `raporlar/hakem_konsey_2026-10-31/_gonderim_eski_2026-10-04/`)

> **2026-10-31 notu.** Makale bugün O1 manşetiyle yeniden yazıldı ve başlığı
> değişti. Bu klasördeki dört belge (`cover_letter.tex`, `highlights.txt`,
> `declarations.txt`, bu liste) yeni başlığa, yeni özete ve brif 12 §2'deki
> iddia sınırına göre yeniden yazıldı; `suggested_reviewers.md` ve
> `author_biographies.tex` güncellendi. Belgelerin makaleyle tutarlılığını
> `scripts/gonderim_tutarlilik.py` (kapı 7) denetler. Aşağıdaki sayılar
> 31.10.2026 19:15 tarihli `main.pdf` ve `main.bbl` üzerinden sayıldı.

---

## 0. Upload Precondition

- [ ] **No upload before both of these arrive:** the second author's written approval of the submitted version (the cover letter states that both authors have approved it) and the second author's confirmation of the funding statement (`declarations.txt` §6, "no specific grant").

---

## 1. Manuscript Format and Content

- [x] IEEE Access LaTeX template (`ieeeaccess.cls`, mandatory)
- [x] Title matches across manuscript, cover letter, highlights, declarations and this list (gate 7)
- [x] Abstract within the 250-word limit: 249 words (EN), checked by `scripts/check_abstract_body.py` on 2026-10-31
- [x] Abstract and Index Terms render in the PDF (gate 8, `check_pdf_render.py`)
- [x] Index terms: 7 (adversarial robustness, transfer attacks, transferability, Vision Transformer, convolutional neural networks, pre-registration, evaluation methodology)
- [x] Sections: Introduction, Related Work, Methodology, Experiments, Computational Details, Discussion, Conclusion, Appendix; Data and Code Availability; Acknowledgment
- [x] Generative AI use disclosed in the Acknowledgment and in the cover letter
- [ ] **Author biographies complete.** Two `IEEEbiographynophoto` blocks are present; the second author's degrees and years are missing (reviewer panel A13). Photos and the `IEEEbiography` environment are added after acceptance.
- [ ] **ORCID iDs for all authors** (the submitting author must have ORCID linked to the IEEE account)
- [x] References in IEEE style (`IEEEtran.bst`): 77 entries in `main.bbl`

## 2. Length

- [x] Page count: **25 pages** in `ieeeaccess.cls` (`main.pdf`, 2026-10-31). IEEE Access is a flat-APC journal without a hard page limit; the length follows from the registered design (panel tests, two-by-two design, attack side, three external panels).
- [ ] Reviewer panel B18: the methodology section is above its word budget; repetitions are to be trimmed in the next manuscript round.

## 3. Figures and Tables

- [x] 12 figures, all vector PDF; 18 table environments
- [ ] **Flat figure paths for upload** (reviewer panel A13). The manuscript reads figures from `../figures/final/` (3 files) and `../figures/konsey/` (9 files); for the source ZIP they must be copied next to `main.tex` and the paths flattened.
- [ ] Font size at least 6.5 pt in every figure and the arrow from (c) to (d) in the study overview (reviewer panel A12, visio-cizici round)
- [ ] Grayscale readability check

Figures used by the manuscript (2026-10-31):

| Folder | File |
|---|---|
| figures/konsey | fig_study_overview.pdf |
| figures/konsey | fig_decomposition_schematic.pdf |
| figures/konsey | fig_similarity_matrix.pdf |
| figures/konsey | fig_source_gap_split.pdf |
| figures/konsey | fig_cells_interaction.pdf |
| figures/konsey | fig_estimates_forest.pdf |
| figures/konsey | fig_attack_side.pdf |
| figures/konsey | fig_gradient_alignment.pdf |
| figures/konsey | fig_protocol_sets.pdf |
| figures/final | fig_spread_clean_gap.pdf |
| figures/final | fig2_epsilon_sweep.pdf |
| figures/final | fig5b_attention_entropy.pdf |

## 4. References

- [x] No unresolved citations in the last compilation
- [x] Citation check of 2026-10-31 (`raporlar/atif_2026-10-31/rapor.md`); `sahin2026behavioral` (ATEEC 2026) cannot be verified externally until the proceedings appear
- [ ] Reviewer panel B12: the keys of Awad, Springer and Zhang to be confirmed in the next citation round
- [ ] DOIs added where available (recommended)

## 5. Declarations and Statements

- [x] Data availability: manuscript (Data and Code Availability) and `declarations.txt` §1, same scope (CIFAR-10, CIFAR-100, SVHN, ImageNetV2; RobustBench checkpoints; timm initializations)
- [ ] **Code availability.** On 2026-10-31 https://github.com/cagrisahin58/cnn-vit-robustness-protocols returns 404; the local copy `teslim/acik_depo/cnn-vit-robustness-protocols` is a single commit of 4 October with the old title and without the registration documents or the frozen script. The cover letter and `declarations.txt` §2-3 therefore promise the release "upon acceptance" and point to the time-stamped development commits e32f2ce (main registration, frozen script, cell table) and 7325419 (addendum, addendum cell tables, addendum scripts, deviation log). The manuscript's Data and Code Availability paragraph (`main.tex`) still says "are public at"; it must be brought into line with whichever state holds at upload.
  - [ ] Repository created on GitHub under `cagrisahin58` and published (user)
  - [ ] `bash scripts/acik_depo_kur.sh --dry-run` read, then `bash scripts/acik_depo_kur.sh` run and the printed `git push` lines executed (user)
  - [ ] The URL returns 200 (`curl -s -o /dev/null -w '%{http_code}' https://github.com/cagrisahin58/cnn-vit-robustness-protocols`)
  - [ ] README.md and CITATION.cff in the published repository carry the new title
  - [ ] If the repository is public before upload, switch "will be released ... upon acceptance" back to "are available at" in the cover letter, `declarations.txt` §2-3 and `main.tex`
- [x] Pre-registration statement: `declarations.txt` §3, consistent with Section III "Pre-Registration" of the manuscript
- [x] Conflict of interest: none declared
- [ ] Funding: "no specific grant" to be confirmed with the co-author (upload precondition, §0)

## 6. Conference Extension and Overlap

- [x] **Conference extension declared.** A preliminary version (CIFAR-10, the ResNet-18 and ViT-Tiny pair only) has been submitted to ATEEC 2026 and is under review. The manuscript cites it (Introduction, last paragraph), the cover letter and `declarations.txt` §4 declare it, and the manuscript corrects one claim of it. The portal's prior-publication field must be filled at upload.
- [ ] If the ATEEC decision arrives before or during review: update `sahin2026behavioral` (status, proceedings data) and the sentence "submitted to ATEEC 2026" in the manuscript, the cover letter and `declarations.txt` together.
- [ ] Similarity check (iThenticate) to be read against the conference version
- [x] Consistency between the conference paper and the manuscript is monitored by `scripts/bildiri_tutarlilik.py` (gate 5); the conference paper itself is not edited.

## 7. IEEE Access Portal

- [ ] IEEE Author Portal account and ORCID link
- [ ] Article type "Regular Article"
- [ ] APC source confirmed (standard IEEE Access APC; check member and institutional discounts at upload)
- [ ] Suggested reviewers entered from `suggested_reviewers.md` after their affiliations and e-mail addresses are re-checked

## 8. Copyright and Licensing

- [ ] Creative Commons license (CC BY 4.0) selected in the portal
- [ ] IEEE electronic copyright form completed in production

## 9. Submission Files

| File | Format | Status |
|---|---|---|
| Manuscript PDF | PDF | [x] compiled 2026-10-31 |
| LaTeX source | ZIP (main.tex, macros_konsey.tex, sections/, references.bib, class files, figures) | [ ] figure paths to be flattened (A13) |
| Cover letter | PDF from `cover_letter.tex` | [x] rewritten 2026-10-31 |
| Highlights | TXT | [x] rewritten 2026-10-31 (optional for IEEE Access) |
| Declarations | TXT | [x] rewritten 2026-10-31 |
| Suggested reviewers | portal entry | [ ] re-check contact data |

## 10. Final Review Before Submit

- [x] Title identical across manuscript and submission documents (gate 7)
- [ ] Author names and order consistent in manuscript, portal and cover letter
- [ ] Upload precondition of §0 met (second author's approval and funding confirmation)
- [ ] No TODO comments in the manuscript (reviewer panel A14: two `TODO(foy)` comments in `sections/07_appendix.tex`)
- [ ] The reviewer panel's open items that need the reference sheet (A2-A6, A9, A10) are either completed or their sentences stay without numbers
- [x] All gates run by `bash scripts/kapilar.sh`; see `raporlar/hakem_konsey_2026-10-31/gonderim_paketi_notu.md` for the 2026-10-31 state
