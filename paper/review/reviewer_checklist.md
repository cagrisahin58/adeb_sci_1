# Pre-Submission Reviewer Checklist

Complete this checklist before submitting to any journal.

---

## Experimental Rigor

- [ ] All experiments repeated 3 times with different seeds
- [ ] Mean ± std reported for all metrics
- [ ] Statistical significance tests (p-values) computed
- [ ] AutoAttack evaluation included (gold standard)
- [ ] Hyperparameter sensitivity analysis included

---

## Reproducibility

- [ ] Code repository publicly available
- [ ] All hyperparameters documented
- [ ] Random seeds specified
- [ ] Dataset splits documented
- [ ] Model checkpoints available (or will be upon acceptance)
- [ ] `commands.sh` contains all reproducible commands

---

## Baseline Comparisons

- [ ] SOTA baseline included (WideResNet-28-10 from RobustBench)
- [ ] Fair comparison (same evaluation protocol)
- [ ] Parameter counts reported
- [ ] Training compute documented

---

## Figures and Tables

- [ ] All figures at 300 DPI minimum
- [ ] Vector format (PDF) preferred
- [ ] Color-blind friendly palette
- [ ] Clear axis labels and legends
- [ ] Tables include uncertainty (±std)
- [ ] Consistent number formatting

---

## Writing Quality

- [ ] No grammatical errors
- [ ] Consistent terminology
- [ ] All acronyms defined
- [ ] Claims supported by evidence
- [ ] Limitations section included
- [ ] Future work discussed

---

## Related Work

- [ ] Recent papers (2024-2025) included
- [ ] Key adversarial robustness papers cited
- [ ] RobustBench leaderboard referenced
- [ ] TRADES, MART, AT papers cited
- [ ] ViT robustness papers cited

---

## Ethics and Broader Impact

- [ ] Potential misuse discussed
- [ ] Defensive applications emphasized
- [ ] No personal data used

---

## Technical Correctness

- [ ] Threat model clearly defined
- [ ] Attack parameters consistent (eps=8/255)
- [ ] Defense implementations verified
- [ ] No data leakage in evaluation
- [ ] Test set only used for final evaluation

---

## Specific Checks for This Paper

### CNN vs ViT Comparison
- [ ] Same epsilon budget used
- [ ] Same number of attack steps
- [ ] Model capacity differences discussed
- [ ] Training compute normalized

### Transfer Attack Analysis
- [ ] All model pairs evaluated
- [ ] Attack success rate correctly computed
- [ ] Source model accuracy reported

### Gradient Analysis
- [ ] Gradient computation verified
- [ ] Norm calculation correct
- [ ] Statistical tests applied

### Attention Analysis
- [ ] Attention extraction method documented
- [ ] Entropy calculation verified
- [ ] Qualitative examples provided

---

## Final Checks

- [ ] Abstract within word limit
- [ ] Paper within page limit
- [ ] References properly formatted
- [ ] Supplementary materials complete
- [ ] Author information correct (or anonymized for double-blind)

---

## Submission Preparation

### For IEEE Journals
- [ ] IEEE template used
- [ ] Graphical abstract prepared
- [ ] Cover letter written
- [ ] Suggested reviewers listed
- [ ] Conflict of interest declared

### For Pattern Recognition / Neural Networks
- [ ] Elsevier template used
- [ ] Highlights section prepared
- [ ] Keywords selected

---

## Known Issues to Address

1. **ViT performance lower than CNN:** Discuss model capacity and training data requirements
2. **CIFAR-10 only:** Acknowledge limitation, suggest ImageNet as future work
3. **No certified defense:** Clarify focus on empirical robustness

---

Last updated: 2026-01-09
