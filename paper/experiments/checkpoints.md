# Model Checkpoints

This document lists all checkpoints used in the SCI paper.

---

## CNN Models

### ResNet18 (Clean)
- **Path:** `models/resnet18/clean/best.pth`
- **Clean Accuracy:** 94.37%
- **Parameters:** 11.2M
- **Training:** 200 epochs, SGD LR=0.1, Cosine scheduler

### ResNet18 (Adversarial Training)
- **Path:** `models/resnet18/adv/adversarial_training/best.pth`
- **Clean Accuracy:** 80.34%
- **PGD-10 Accuracy:** 40.25%
- **Parameters:** 11.2M
- **Training:** 100 epochs, SGD LR=0.001 (from pretrained), PGD-10

### ResNet18 (TRADES) - Pending
- **Path:** `models/resnet18/adv/trades/best.pth`
- **Status:** Needs retraining with warmup

### WideResNet-28-10 (RobustBench)
- **Path:** `models/robustbench/wideresnet28_10_robust.pth`
- **Clean Accuracy:** 89.48%
- **AutoAttack Accuracy:** 62.76%
- **Parameters:** 36.5M
- **Source:** RobustBench (Gowal2020Uncovering_28_10_extra)
- **Note:** Pretrained robust model, not trained by us

### DenseNet121 (Clean)
- **Path:** `models/densenet121/clean/best.pth`
- **Clean Accuracy:** 95.09%
- **Parameters:** 7.0M
- **Training:** 200 epochs, SGD LR=0.1

---

## ViT Models (timm-based, 32→224 resize)

### ViT-Tiny (Clean)
- **Path:** `models/vit_tiny/clean/best.pth`
- **Clean Accuracy:** 77.50%
- **Parameters:** 5.7M
- **Training:** 200 epochs, AdamW LR=1e-3

### ViT-Tiny (Adversarial Training)
- **Path:** `models/vit_tiny/adv/adversarial_training/best.pth`
- **Clean Accuracy:** 63.42%
- **PGD-10 Accuracy:** 32.77%
- **Parameters:** 5.7M
- **Training:** 100 epochs, AdamW LR=1e-4

---

## ViT Models (CIFAR-native, 32x32 input)

### ViT-CIFAR-Tiny (Clean)
- **Path:** `models/vit_cifar_tiny/clean/best.pth`
- **Clean Accuracy:** 71.75%
- **Parameters:** 5.4M
- **Architecture:** 32x32 input, 4x4 patch, 192 dim, 12 layers, 3 heads
- **Training:** 200 epochs, AdamW LR=1e-3

### ViT-CIFAR-Tiny (Adversarial Training) - In Progress
- **Path:** `models/vit_cifar_tiny/adv/adversarial_training/best.pth`
- **Status:** Training in progress
- **Parameters:** 5.4M
- **Training:** 100 epochs, AdamW LR=1e-3, PGD-10

### ViT-CIFAR-Small (Clean/AT) - Planned
- **Parameters:** 21.3M
- **Architecture:** 32x32 input, 4x4 patch, 384 dim, 12 layers, 6 heads

---

## Checkpoint Format

All checkpoints contain:
```python
{
    "model_state_dict": ...,
    "optimizer_state_dict": ...,
    "scheduler_state_dict": ...,
    "epoch": int,
    "accuracy": float,
    "extra_info": {
        "clean_acc": float,  # for AT models
        "adv_acc": float,    # for AT models
    }
}
```

---

## Verification Commands

```bash
# Check checkpoint metadata
python -c "
import torch
ckpt = torch.load('models/resnet18/clean/best.pth')
print(f'Epoch: {ckpt.get(\"epoch\", \"N/A\")}')
print(f'Accuracy: {ckpt.get(\"accuracy\", \"N/A\")}')
print(f'Extra: {ckpt.get(\"extra_info\", {})}')
"

# Evaluate checkpoint
python -m cli.main evaluate robustness \
    --model-path models/resnet18/clean/best.pth \
    --model-type resnet18
```

---

Last updated: 2026-01-09
