# Experiment Log

> **KARANTINA (2026-08-18):** Bu dosyadaki run1/run2 sayilari TARIHSEL kayittir.
> Makale, tez, sunum veya bildiriye **hicbiri aktarilamaz**. Gecerli sayilarin tek
> kaynagi `results/C1_REFERANS_FOYU.md` dosyasidir (uretici:
> `scripts/build_reference_sheet.py`). C1 sizinti duzeltmesi sonuclari ondalik
> duzeyinde degil ANLATI duzeyinde degistirmistir. Gerekce: `CLAUDE.md` bas kismi.


This file tracks all experiments for the SCI paper.

---

## Completed Experiments

### 2026-01-09: RobustBench WideResNet-28-10 Evaluation

**Model:** Gowal2020Uncovering_28_10_extra (RobustBench pretrained)
**Checkpoint:** `models/robustbench/wideresnet28_10_robust.pth`

| Metric | Value |
|--------|-------|
| Clean Accuracy | 89.48% |
| PGD-20 Accuracy | 66.05% |
| AutoAttack (Linf, eps=8/255) | 62.76% |

**Source:** RobustBench benchmark

---

### 2026-01-09: ResNet18 AT Verification

**Model:** ResNet18 with Adversarial Training
**Checkpoint:** `models/resnet18/adv/adversarial_training/best.pth`
**Training:** 100 epochs, LR=0.001 (from pretrained), PGD-10

| Metric | Value |
|--------|-------|
| Clean Accuracy | 80.34% |
| PGD-10 Accuracy | 40.25% |

---

### 2026-01-09: ViT-Tiny (timm) AT Verification

**Model:** ViT-Tiny (timm, 32→224 resize) with AT
**Checkpoint:** `models/vit_tiny/adv/adversarial_training/best.pth`
**Training:** 100 epochs, AdamW LR=1e-4, PGD-10

| Metric | Value |
|--------|-------|
| Clean Accuracy | 63.42% |
| PGD-10 Accuracy | 32.77% |

---

### 2026-01-09: ViT-CIFAR-Tiny Clean Training

**Model:** CIFAR-native ViT-Tiny (32x32 input, 4x4 patch, 192 dim, 12 layers)
**Checkpoint:** `models/vit_cifar_tiny/clean/best.pth`
**Training:** 200 epochs, AdamW LR=1e-3, Cosine scheduler

| Metric | Value |
|--------|-------|
| Test Accuracy | 71.75% |
| Parameters | 5.4M |

**Note:** Lower than timm version (77.50%) due to no pretrained weights and native resolution.

---

## In Progress

### 2026-01-09: ViT-CIFAR-Tiny Adversarial Training

**Model:** CIFAR-native ViT-Tiny
**Training:** 100 epochs, AdamW LR=1e-3, PGD-10 (eps=8/255)
**Status:** Training in progress (GPU ~73% utilization)

**Progress:**
- Epoch 2/100: Clean 52.70%, Adv 26.88%
- Expected completion: ~4-5 hours

---

## Pending Experiments

### ResNet18 TRADES (Needs Fix)

**Issue:** Previous training collapsed at epoch 4
**Root Cause:** Missing warmup scheduler, LR too high
**Fix:** Add warmup, reduce LR to 0.001

### Statistical Validation (3 Runs)

**Models:** ResNet18 AT, ViT-CIFAR-Tiny AT
**Seeds:** [42, 123, 456]
**Metrics:** Mean ± std, 95% CI

### Transfer Attack Analysis

**Source Models:** ResNet18 AT, WideResNet-28-10, ViT-CIFAR-Tiny AT
**Target Models:** Same
**Attack:** PGD-20 (eps=8/255)
**Metric:** Attack success rate matrix

### Gradient Analysis

**Models:** ResNet18, ViT-CIFAR-Tiny (both clean and AT)
**Metrics:**
- Gradient norm distribution
- Gradient direction consistency
- Input-gradient correlation

### Attention Degradation Analysis

**Models:** ViT-CIFAR-Tiny (clean and AT)
**Analysis:**
- Clean vs adversarial attention maps
- Layer-wise attention entropy
- CLS token attention shift

---

## Notes

- All adversarial training uses eps=8/255, alpha=2/255, steps=10
- Clean models trained for 200 epochs, AT models for 100 epochs
- ViT models use AdamW, CNN models use SGD
