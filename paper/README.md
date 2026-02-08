# SCI Q1 Publication: CNN vs ViT Adversarial Robustness

**Son Guncelleme:** 2026-01-11

## Paper Status

| Item | Status | Notes |
|------|--------|-------|
| Experiments | **95%** | Tum analizler tamamlandi |
| Statistical Validation | **100%** | 3 seed, <0.15% varyans |
| Figures | **90%** | raw/ klasorunde, final/ tasınacak |
| Manuscript | **100%** | Tum bolumler yazıldı, Q1 revize edildi |
| Review Ready | **Yakın** | AutoAttack run2 + final polish |

---

## Target Journals (Q1)

1. **Pattern Recognition** (IF: 8.0) - Pragmatic choice, comparative studies
2. **Neural Networks** (IF: 7.8) - Safe choice, analysis papers
3. **IEEE TNNLS** (IF: 14.2) - High prestige, long review

---

## Working Title

**"A Comparative Study of Convolutional and Transformer Architectures Under Adversarial Perturbations: Gradient Characteristics and Transferability Analysis"**

---

## Original Contributions

1. **CNN vs ViT fair comparison** - Same evaluation pipeline
2. **Transfer attack analysis** - Cross-architecture attack transferability (47.5% vs 33.5% asymmetry)
3. **Gradient characteristics** - Mathematical explanation (ViT 2.2x aligned, CNN 4.5x sparse)
4. **Attention degradation** - First comprehensive analysis (-7.86% norm, cosine 0.997→0.917)

---

## Current Model Performance (UPDATED 2026-01-11)

| Model | Clean Acc | PGD-10 | AutoAttack | Status |
|-------|-----------|--------|------------|--------|
| WideResNet-28-10 (RobustBench) | 89.48% | 66.05% | 62.76% | Ready |
| **ResNet18 AT (run2)** | ~80% | **40.97%** | - | **NEW** |
| ResNet18 AT (run1) | 80.34% | 40.25% | 34.6% | Ready |
| **ViT-Tiny AT (run2)** | 76.91% | **36.87%** | - | **NEW** |
| ViT-Tiny AT (run1) | 63.42% | 32.77% | 28.0% | Ready |

---

## Completed Experiments

| Experiment | Data | Figures | Status |
|------------|------|---------|--------|
| 1. Main Robustness | Table 1 | Fig 1, 2 | **Done** |
| 2. Transfer Attack | Table 2 | Fig 3 | **Done** |
| 3. Gradient Analysis | Stats | Fig 4a, 4b | **Done** |
| 4. Attention Degradation | JSON | Fig 5a, 5b | **Done** |
| 5. Statistical Validation | Table 3 | - | **Done** |
| 6. AutoAttack Eval | Table 4 | - | run1 done, run2 pending |

---

## Key Results

### Transfer Attack Asymmetry
- CNN → ViT: **47.5%** transfer success
- ViT → CNN: **33.5%** transfer success
- Asymmetry ratio: **1.42x**

### Gradient Characteristics
- CNN sparsity: **6.9%** near-zero components
- ViT sparsity: **1.5%** near-zero components
- CNN/ViT sparsity ratio: **4.5x**
- ViT gradient alignment: **0.097** (2.2x higher than CNN's 0.044)

### Attention Degradation (ViT)
- Late layer norm reduction: **-7.86%**
- Cosine similarity drop: **0.997 → 0.917**
- Most affected: blocks.10, blocks.11

### AutoAttack Results (Gold Standard)
- ResNet18 AT: **34.6%** robust accuracy
- ViT-Tiny AT: **28.0%** robust accuracy
- Gap: **6.6%** favoring CNN

---

## Directory Structure

```
paper/
├── README.md              # This file
├── manuscript/            # LaTeX files
│   ├── main.tex
│   ├── sections/          # 6 sections complete
│   │   ├── 01_introduction.tex
│   │   ├── 02_related_work.tex
│   │   ├── 03_methodology.tex
│   │   ├── 04_experiments.tex
│   │   ├── 05_discussion.tex
│   │   └── 06_conclusion.tex
│   └── references.bib     # 38 references
├── figures/
│   ├── raw/               # 17 figures generated
│   └── final/             # Publication-ready (to be populated)
├── tables/                # LaTeX tables
├── supplementary/         # Appendix materials
├── experiments/           # Experiment logs
└── review/                # Pre-submission checklist
```

---

## Quick Commands

```bash
# Evaluate model robustness
python -m cli.main evaluate robustness \
    --model-path models/resnet18/adv/adversarial_training/best.pth \
    --model-type resnet18 \
    --attacks fgsm pgd autoattack

# Run gradient analysis
python experiments/run_gradient_analysis_simple.py

# Run transfer attack analysis
python experiments/run_transfer_analysis_simple.py

# Run attention analysis
python experiments/run_attention_analysis_simple.py

# Run AutoAttack evaluation
python experiments/run_autoattack_evaluation.py

# Run statistical validation
python experiments/run_statistical_validation.py
```

---

## Pre-submission Checklist

- [x] All experiments completed with 3 seeds
- [x] AutoAttack results included (run1)
- [ ] AutoAttack results for run2 models
- [x] Statistical tests reported (mean ± std)
- [x] Related work updated (2023-2025 papers)
- [x] Figure quality sufficient (PDF, 300 DPI)
- [ ] Figures moved to final/ folder
- [x] Limitations section honest and clear
- [x] Code documented for reproducibility

---

## Notes

- All experiments use CIFAR-10 dataset
- Adversarial budget: eps=8/255 (Linf)
- Statistical validation: 3 independent runs with seeds [42, 123, 456]
- AutoAttack is the gold standard for robustness evaluation
- Early stopping with patience=20 used for efficiency
