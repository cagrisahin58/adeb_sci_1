# Suggested Reviewers

**Manuscript:** Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design

**Revised:** 2026-10-31. The justifications were rewritten for the new framing of the manuscript (vulnerability, similarity and direction in cross-architecture transfer; pre-registered architecture-by-initialization design). Names, titles, affiliations and e-mail addresses are carried over from the 2026-07-10 list and were **not re-verified** in this round; they must be checked against the reviewers' current institutional pages before they are entered in the portal. Paper titles and venues of the works cited in the manuscript were checked against `paper/manuscript/references.bib`.

## Selection Criteria

- Active in adversarial robustness of Vision Transformers, cross-architecture transfer, or transfer attacks (published 2022 to 2025)
- No co-authorship, institutional or personal relationship with either author
- Work cited in the manuscript is allowed; the manuscript does not build on any single candidate's method, so no candidate reviews an extension of their own work
- Geographic and institutional diversity

---

## Reviewer 1

**Name:** Dr. Huaming Chen
**Title:** Senior Lecturer
**Affiliation:** School of Computer Science, The University of Sydney, Australia
**Website:** https://huaming-chen.com/
**Email:** huaming.chen@sydney.edu.au

**Justification:** Dr. Chen is a co-author of "Enhancing Transferable Adversarial Attacks on Vision Transformers through Gradient Normalization Scaling and High-Frequency Adaptation" (ICLR 2024), which studies how gradient structure on a ViT source governs transfer to other architectures. The manuscript asks whether a ViT's low transfer to CNNs is a property of the source or of the dissimilarity between the models, and tests input-gradient alignment as a correlate of pairwise similarity; a reviewer who has worked on improving ViT-source transfer is well placed to judge whether the source-side checks (momentum PGD and an adapted token gradient regularization) are adequate.

---

## Reviewer 2

**Name:** Dr. Pin-Yu Chen
**Title:** Principal Research Staff Member
**Affiliation:** Trusted AI Group, IBM Thomas J. Watson Research Center, USA
**Website:** https://sites.google.com/site/pinyuchenpage
**Email:** pin-yu.chen@ibm.com

**Justification:** Dr. Chen co-authored "On the Adversarial Robustness of Vision Transformers" (Transactions on Machine Learning Research, 2022) and "Vision Transformers are Robust Learners" (AAAI 2022), both cited in the manuscript as part of the CNN-versus-ViT robustness literature that our results are read against. His experience in evaluating robustness differences between architecture families bears directly on the manuscript's architecture-by-initialization design and on its statement that the architecture contrast compares whole packages rather than attention alone.

---

## Reviewer 3

**Name:** Dr. Cho-Jui Hsieh
**Title:** Professor
**Affiliation:** Department of Computer Science, University of California, Los Angeles (UCLA), USA
**Website:** https://web.cs.ucla.edu/~chohsieh/
**Email:** chohsieh@cs.ucla.edu

**Justification:** Prof. Hsieh is a co-author of "On the Adversarial Robustness of Vision Transformers" (Transactions on Machine Learning Research, 2022), cited in the manuscript, which reports transfer between CNNs and ViTs. His broader work on robustness evaluation fits the statistical side of the manuscript: equivalence tests with a registered margin, Holm-corrected test families and the distinction between registered and exploratory analyses. If both Dr. Pin-Yu Chen and Prof. Hsieh are entered, the editor should be told that they co-authored the same cited paper.

---

## Reviewer 4

**Name:** Dr. Gihyun Kim
**Title:** Researcher
**Affiliation:** Yonsei University, Seoul, South Korea
**Email:** (available via institutional directory)

**Justification:** Dr. Kim is the first author of "Exploring Adversarial Robustness of Vision Transformers in the Spectral Perspective" (WACV 2024; not cited in the manuscript, venue not re-verified in this round). A spectral account of ViT vulnerability offers an alternative to the gradient-alignment account that the manuscript tests and reads only as an association, so this reviewer can judge whether the manuscript's boundary on mechanism claims is drawn in the right place.

---

## Reviewer 5

**Name:** Dr. Wenshuo Ma
**Title:** Researcher
**Affiliation:** Beijing Jiaotong University, Beijing, China
**Email:** (available via institutional directory)

**Justification:** Dr. Ma is the first author of "Transferable Adversarial Attack for Both Vision Transformers and Convolutional Networks via Momentum Integrated Gradients" (ICCV 2023), cited in the manuscript, which crafts perturbations meant to transfer in both directions between ViTs and CNNs. The manuscript's directional term is precisely the part of cross-architecture transfer that such attacks target, and its finding that this term is small only on the log scale, on CIFAR-10 and against a CNN panel is a claim this reviewer can test against experience with stronger transfer attacks.

---

## Notes

- Candidates closer to the decomposition itself (authors of the transferability analyses that the manuscript relates its identity to) were not added in this round, because their contact data could not be verified here; adding one is an open item.
- We have no personal, institutional, or collaborative relationship with any of the suggested reviewers.
