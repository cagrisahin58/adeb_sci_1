
# Adversarial Defense Study

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.9+-ee4c2c.svg)](https://pytorch.org/)
[![CIFAR-10](https://img.shields.io/badge/dataset-CIFAR--10-brightgreen.svg)](https://www.cs.toronto.edu/~kriz/cifar.html)

## 📋 Overview

A comprehensive modular framework for evaluating adversarial robustness of deep learning models. This project compares ResNet (CNN) and Vision Transformer (ViT) architectures on CIFAR-10 with multiple attack methods and defense strategies.

### Key Features

- **Multiple Model Architectures**: ResNet, ViT, DenseNet, EfficientNet, RobustBench
- **Attack Methods**: FGSM, PGD, C&W, DeepFool, Spatial, AutoAttack
- **Defense Mechanisms**: Adversarial Training, TRADES, MART, TTA, Purification
- **Modular Design**: Easy to extend with new models, attacks, and defenses
- **CLI Interface**: Simple command-line tools for training and evaluation

## 📁 Project Structure

```
adeb_sci_1/
├── src/                         # Modular source code
│   ├── models/                  # Model architectures
│   │   ├── resnet.py            # ResNet18/34/50
│   │   ├── vit.py               # ViT-Tiny/Small/Base
│   │   ├── densenet.py          # DenseNet121/169/201
│   │   ├── efficientnet.py      # EfficientNet-B0/B1/B2
│   │   └── robustbench.py       # RobustBench models
│   ├── attacks/                 # Attack implementations
│   │   ├── fgsm.py              # FGSM attack
│   │   ├── pgd.py               # PGD attack
│   │   ├── cw.py                # C&W attack
│   │   ├── deepfool.py          # DeepFool attack
│   │   ├── spatial.py           # Spatial attacks
│   │   └── autoattack.py        # AutoAttack wrapper
│   ├── defenses/                # Defense mechanisms
│   │   ├── adversarial_training.py
│   │   ├── trades.py            # TRADES defense
│   │   ├── mart.py              # MART defense
│   │   ├── tta.py               # Test-Time Augmentation
│   │   └── purification.py      # Adversarial purification
│   ├── training/                # Training utilities
│   ├── evaluation/              # Evaluation and reporting
│   ├── data/                    # Dataset loaders
│   └── utils/                   # Utilities (config, seed, device)
├── cli/                         # Command-line interface
├── configs/                     # YAML configurations
├── tests/                       # Pytest tests
├── scripts/                     # Legacy scripts (preserved)
├── results/                     # Evaluation results
├── models/                      # Trained model checkpoints
└── logs/                        # Training logs
```

## 🔍 Study Components

### Models
- **ResNet18**: CNN architecture with residual connections
- **ViT-Tiny**: Vision Transformer with patch-based image processing

### Attacks
1. **FGSM** (Fast Gradient Sign Method): Single-step attack with ε ∈ {0.008, 0.016, 0.031}
2. **PGD** (Projected Gradient Descent): Multi-step iterative attack with ε ∈ {0.008, 0.016, 0.031}
3. **AutoAttack**: Ensemble of parameter-free attacks (APGD-CE, APGD-T, FAB-T, SQUARE)

### Defenses
1. **Adversarial Training**: Training models with adversarially perturbed examples
2. **TTA** (Test-Time Augmentation): Applying augmentation at inference time and averaging predictions

## 🚀 How to Use

### Prerequisites
- Python 3.8+
- PyTorch 1.9+ with CUDA support
- NVIDIA GPU (recommended)

### Environment Setup
```bash
# Create and activate conda environment
conda create -n advlab python=3.8
conda activate advlab

# Install the package
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### 🎯 Quick Start: Complete Pipeline

**Option 1: Quick Test (No Training)**
```bash
# Test the pipeline with random models (takes ~5 minutes)
./quick_test.sh
```

**Option 2: Full Pipeline for SCI Publication**
```bash
# Complete training + analysis (takes ~10-12 hours on GPU)
./run_complete_pipeline.sh
```

This will:
1. Train clean models (ResNet18, ViT-Tiny, DenseNet121)
2. Train adversarial models (with AT and TRADES)
3. Run basic robustness evaluation
4. Generate comprehensive SCI analysis (gradient, transfer, attention)
5. Create publication-quality visualizations

### Using the CLI

```bash
# Train a clean ResNet18 model
advdefense train clean --model resnet18 --epochs 50

# Train with TRADES defense
advdefense train adversarial --model resnet18 --defense trades --beta 6.0

# Evaluate robustness
advdefense evaluate robustness --model-path ./models/resnet/adv/best.pth \
    --model-type resnet18 --attacks fgsm pgd

# Run full evaluation
advdefense evaluate full --model-path ./models/best.pth --model-type resnet18

# List available models/attacks/defenses
advdefense list-models
advdefense list-attacks
advdefense list-defenses
```

### Using as a Library

```python
from src.models import ModelRegistry
from src.attacks import AttackRegistry
from src.defenses import DefenseRegistry
from src.training import Trainer, AdversarialTrainer
from src.evaluation import Evaluator

# Create model
model = ModelRegistry.get("resnet18")

# Create attack
attack = AttackRegistry.get("pgd", model=model, eps=8/255)

# Create defense
defense = DefenseRegistry.get("trades", model=model, beta=6.0)

# Evaluate
evaluator = Evaluator(model, test_loader, device)
results = evaluator.evaluate_multiple_attacks(attacks=["fgsm", "pgd"])
```

### Legacy Scripts

The original scripts are preserved in `scripts/` directory:

```bash
# Example: Train clean ResNet model
python scripts/01_train_resnet_clean.py

# Example: Evaluate ResNet model against attacks
python scripts/05_attack_evaluation.py --model resnet --training clean
```

## 📊 Key Results

### Clean Accuracy

| Model          | Clean Training | Adversarial Training |
|----------------|---------------|---------------------|
| ResNet         | 94.47%        | 82.45%              |
| ViT            | 78.69%        | 64.05%              |

### FGSM Attack Results (ε=0.0078)

| Model          | Clean Training | Adversarial Training |
|----------------|---------------|---------------------|
| ResNet         | 45.06%        | 75.07%              |
| ViT            | 7.17%         | 55.72%              |

### PGD Attack Results (ε=0.0078)

| Model          | Clean Training | Adversarial Training |
|----------------|---------------|---------------------|
| ResNet         | 9.69%         | 74.75%              |
| ViT            | 1.45%         | 55.66%              |

### TTA Defense Improvement (ResNet Clean, FGSM ε=0.0078)

| Without TTA | With TTA | Improvement |
|------------|----------|-------------|
| 45.06%     | 46.37%   | +1.31%      |

### AutoAttack Results (ResNet Adv, Final Robust Accuracy)

| ε=0.0078 | ε=0.0157 | ε=0.0314 |
|----------|----------|----------|
| 74.90%   | 63.00%   | 40.50%   |

For complete results and analysis, refer to the [comprehensive_report.md](comprehensive_report.md) file.

## 🔬 Main Findings

1. ResNet architecture demonstrates significantly better robustness than ViT across all scenarios
2. Adversarial training is highly effective in improving robustness (up to 7-9x improvement for PGD attacks)
3. Clean-trained models are extremely vulnerable to PGD and AutoAttack (accuracy near 0% with ε=0.031)
4. TTA provides marginal improvements (+0.1% to +1.3%) and is more effective on clean-trained models
5. AutoAttack is the most powerful attack method, reducing even adversarially trained model accuracy

## 📖 Citation

If you use this code for your research, please cite our work:

```
@misc{sahin2025adversarial,
  author = {Sahin, Cagri},
  title = {Adversarial Defense Study: Comparing ResNet and ViT Robustness},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/cagrisahin58/adversarial-defense-study}
}
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
