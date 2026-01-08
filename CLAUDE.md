# CLAUDE.md - Adversarial Defense Study

Bu dosya, Claude Code'un bu proje ile etkili bir şekilde çalışabilmesi için gerekli bağlamı sağlar.

## Proje Özeti

Bu proje, **CNN vs ViT adversarial robustness karşılaştırması** üzerine bir SCI makalesi için geliştirilmiş kapsamlı bir adversarial defense çerçevesidir. CIFAR-10 veri seti üzerinde derin öğrenme modellerinin adversarial saldırılara karşı dayanıklılığını değerlendirir.

**Ana Hedef:** ResNet (CNN) ve Vision Transformer (ViT) mimarilerinin adversarial robustness açısından karşılaştırmalı analizi.

## Hızlı Başlangıç

```bash
# Ortam kurulumu
pip install -r requirements.txt

# Clean model eğitimi
python -m cli.main train clean --model resnet18 --epochs 50

# Adversarial training
python -m cli.main train adversarial --model resnet18 --defense adversarial_training --epochs 100

# Model değerlendirme
python -m cli.main evaluate clean --model-path models/resnet18/clean/best.pth --model-type resnet18

# Robustness değerlendirme
python -m cli.main evaluate robustness --model-path models/resnet18/adv/adversarial_training/best.pth --model-type resnet18
```

## Proje Yapısı

```
advdefense/
├── cli/                          # CLI komutları
│   ├── main.py                   # Ana giriş noktası
│   ├── train.py                  # Eğitim komutları (clean, adversarial)
│   └── evaluate.py               # Değerlendirme komutları
│
├── src/                          # Ana kaynak kodu
│   ├── models/                   # Model mimarileri
│   │   ├── registry.py           # Model registry sistemi
│   │   ├── resnet.py             # CIFAR-10 ResNet (18, 34, 50)
│   │   ├── vit.py                # Vision Transformer (Tiny, Small, Base)
│   │   ├── densenet.py           # DenseNet (121, 169, 201)
│   │   ├── efficientnet.py       # EfficientNet (B0, B1, B2)
│   │   └── robustbench.py        # RobustBench model wrapper
│   │
│   ├── attacks/                  # Saldırı implementasyonları
│   │   ├── registry.py           # Attack registry sistemi
│   │   ├── fgsm.py               # FGSM, Targeted FGSM
│   │   ├── pgd.py                # PGD, Targeted PGD, PGD-L2
│   │   ├── cw.py                 # Carlini & Wagner (L2, Linf)
│   │   ├── deepfool.py           # DeepFool
│   │   ├── spatial.py            # Spatial attacks (rotation, translation)
│   │   └── autoattack.py         # AutoAttack wrapper
│   │
│   ├── defenses/                 # Savunma mekanizmaları
│   │   ├── registry.py           # Defense registry sistemi
│   │   ├── adversarial_training.py  # Standard adversarial training
│   │   ├── trades.py             # TRADES defense
│   │   ├── mart.py               # MART defense
│   │   ├── tta.py                # Test-time augmentation
│   │   └── purification.py       # Input purification (denoise, JPEG)
│   │
│   ├── training/                 # Eğitim döngüleri
│   │   ├── trainer.py            # Clean training
│   │   └── adversarial_trainer.py # Adversarial training
│   │
│   ├── evaluation/               # Değerlendirme araçları
│   │   ├── evaluator.py          # Model evaluator
│   │   ├── metrics.py            # Accuracy, robustness metrics
│   │   └── reporters.py          # CSV, Plot reporters
│   │
│   ├── analysis/                 # Analiz araçları
│   │   ├── gradient_analysis.py  # Gradient analizi (CNN vs ViT)
│   │   ├── transfer_analysis.py  # Transfer attack analizi
│   │   ├── attention_analysis.py # Attention map analizi
│   │   └── visualization.py      # Görselleştirme araçları
│   │
│   ├── data/                     # Veri yükleyiciler
│   │   ├── datasets.py           # CIFAR-10 loaders
│   │   └── transforms.py         # Data augmentation
│   │
│   └── utils/                    # Yardımcı fonksiyonlar
│       ├── checkpoint.py         # Model kaydetme/yükleme
│       ├── config.py             # YAML config parser
│       ├── device.py             # Device detection (CUDA/MPS/CPU)
│       └── seed.py               # Reproducibility
│
├── configs/                      # YAML yapılandırma dosyaları
│   ├── default.yaml              # Varsayılan ayarlar
│   ├── models/                   # Model-specific configs
│   ├── attacks/                  # Attack configs
│   └── experiments/              # Deney configs
│
├── models/                       # Eğitilmiş model checkpointleri
│   ├── resnet18/
│   │   ├── clean/best.pth        # 94.37% clean accuracy
│   │   └── adv/
│   │       ├── adversarial_training/best.pth
│   │       └── trades/best.pth
│   ├── vit_tiny/
│   │   ├── clean/best.pth        # 78.69% clean accuracy
│   │   └── adv/best.pth
│   └── densenet121/
│       └── clean/best.pth        # ~95% clean accuracy
│
├── results/                      # Deney sonuçları
│   ├── sci_paper/                # SCI paper için analizler
│   └── evaluation_*/             # Değerlendirme CSV/PNG'leri
│
├── logs/                         # Eğitim logları
├── tests/                        # Unit testler
├── experiments/                  # Deney scriptleri
└── data/                         # CIFAR-10 veri seti (auto-download)
```

## Teknik Detaylar

### Dataset ve Normalization
- **Dataset:** CIFAR-10 (50K train, 10K test, 32x32 RGB)
- **Normalization:** `[0, 1]` aralığı (ImageNet normalization KULLANILMIYOR)
- **Augmentation:** RandomCrop(32, padding=4), RandomHorizontalFlip

### Adversarial Attack Parametreleri
```python
# Standart parametreler (ε = 8/255 ≈ 0.0314)
eps = 8/255     # 0.03137254901960784
alpha = 2/255   # 0.00784313725490196 (PGD step size)
steps = 10      # PGD iteration sayısı
```

### Model Performans Referansları

| Model | Training | Clean Acc | PGD Acc (ε=8/255) |
|-------|----------|-----------|-------------------|
| ResNet18 | Clean | 94.37% | 0.00% |
| ResNet18 | Adv Training | ~82% | ~45% |
| ViT-Tiny | Clean | 78.69% | 0.00% |
| ViT-Tiny | Adv Training | 64.05% | ~28% |
| DenseNet121 | Clean | ~95% | 0.00% |

### Bilinen Sorunlar ve Çözümler

1. **ViT resize sorunu:** ViT modelleri 224x224 bekler, CIFAR-10 32x32. `timm` ile resize yapılıyor ama performans düşük. Çözüm: `vit_tiny_patch4_32` gibi CIFAR-native model kullanılmalı.

2. **TRADES instabilitesi:** TRADES defense yüksek LR ile çöküyor. LR=0.001 ve warmup kullanılmalı.

3. **Catastrophic forgetting:** Pretrained model üzerinde adversarial training yaparken LR çok yüksek olmamalı (0.1 yerine 0.001).

## Sık Kullanılan Komutlar

### Model Eğitimi

```bash
# Clean ResNet18 eğitimi
python -m cli.main train clean --model resnet18 --epochs 100 --lr 0.1

# Adversarial Training (pretrained'den)
python -m cli.main train adversarial \
    --model resnet18 \
    --defense adversarial_training \
    --pretrained models/resnet18/clean/best.pth \
    --epochs 100 \
    --lr 0.001 \
    --eps 0.0314 \
    --alpha 0.00784 \
    --steps 10

# TRADES eğitimi
python -m cli.main train adversarial \
    --model resnet18 \
    --defense trades \
    --epochs 100 \
    --beta 6.0
```

### Model Değerlendirme

```bash
# Clean accuracy
python -m cli.main evaluate clean \
    --model-path models/resnet18/clean/best.pth \
    --model-type resnet18

# Robustness (multiple attacks & epsilons)
python -m cli.main evaluate robustness \
    --model-path models/resnet18/adv/adversarial_training/best.pth \
    --model-type resnet18 \
    --attacks fgsm pgd \
    --epsilons 0.00784 0.01569 0.0314

# Full evaluation suite
python -m cli.main evaluate full \
    --model-path models/resnet18/clean/best.pth \
    --model-type resnet18
```

### Analiz Scriptleri

```bash
# Gradient analizi (CNN vs ViT)
python experiments/run_sci_analysis.py --analysis gradient

# Transfer attack analizi
python experiments/run_sci_analysis.py --analysis transfer

# Attention degradation (ViT)
python experiments/run_sci_analysis.py --analysis attention
```

## Registry Sistemi

Proje, modeller, saldırılar ve savunmalar için registry pattern kullanır:

```python
# Model oluşturma
from src.models import ModelRegistry
model = ModelRegistry.get("resnet18")  # veya "vit_tiny", "densenet121"

# Attack oluşturma
from src.attacks import AttackRegistry
attack = AttackRegistry.get("pgd", model=model, eps=8/255, alpha=2/255, steps=10)

# Defense oluşturma
from src.defenses import DefenseRegistry
defense = DefenseRegistry.get("adversarial_training", model=model, eps=8/255)
```

### Mevcut Modeller
- `resnet18`, `resnet34`, `resnet50`
- `vit_tiny`, `vit_small`, `vit_base`
- `densenet121`, `densenet169`, `densenet201`
- `efficientnet_b0`, `efficientnet_b1`, `efficientnet_b2`

### Mevcut Saldırılar
- `fgsm`, `targeted_fgsm`
- `pgd`, `targeted_pgd`, `pgd_l2`
- `cw`, `cw_linf`
- `deepfool`, `deepfool_linf`
- `spatial`, `rotation`, `translation`
- `autoattack` (Linf, L2)

### Mevcut Savunmalar
- **Training-time:** `adversarial_training`, `trades`, `mart`
- **Inference-time:** `tta`, `tta_tencrop`, `denoise`, `jpeg`, `randomization`

## Kod Stili ve Conventions

### Import Sırası
```python
# 1. Standard library
import os
from pathlib import Path

# 2. Third-party
import torch
import torch.nn as nn
from tqdm import tqdm

# 3. Local
from src.models import ModelRegistry
from src.attacks import PGDAttack
```

### Checkpoint Formatı
```python
{
    'epoch': int,
    'model_state_dict': dict,
    'optimizer_state_dict': dict,
    'best_acc': float,      # Clean accuracy için
    'best_adv_acc': float,  # Adversarial accuracy için (AT modellerinde)
    'config': dict,         # Eğitim konfigürasyonu
}
```

### Epsilon Değerleri
Her zaman 255 tabanlı kullan ve float'a çevir:
```python
eps = 8/255   # DOĞRU: 0.03137254901960784
eps = 0.031   # YANLIŞ: Yaklaşık değer, hataya sebep olabilir
```

## Test Etme

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Belirli test dosyası
pytest tests/test_models.py -v

# Coverage ile
pytest tests/ --cov=src --cov-report=html
```

## GPU/Device Yönetimi

```python
from src.utils.device import get_device

# Otomatik device seçimi
device = get_device("auto")  # CUDA > MPS > CPU

# Manuel seçim
device = get_device("cuda")
device = get_device("cpu")
```

## Yapılacaklar ve Mevcut Durum

### Tamamlanan
- [x] ResNet18 clean training (94.37%)
- [x] ViT-Tiny clean training (78.69%)
- [x] DenseNet121 clean training (~95%)
- [x] Gradient analizi (CNN vs ViT)
- [x] Transfer attack analizi

### Devam Eden
- [ ] ResNet18 adversarial training (100 epoch)
- [ ] TRADES debug ve stabilizasyonu

### Planlanmış
- [ ] WideResNet-28-10 ekleme (SOTA karşılaştırması için)
- [ ] CIFAR-native ViT modeli
- [ ] Epsilon sweep analizi
- [ ] AWP (Adversarial Weight Perturbation)
- [ ] SCI paper figürleri

## Ortam Bilgisi

- **Framework:** PyTorch 2.6.0
- **CUDA:** 12.8
- **GPU:** RTX 5060 Ti (16GB VRAM)
- **Python:** 3.10+

## Referanslar

- [TRADES Paper](https://arxiv.org/abs/1901.08573)
- [AutoAttack](https://arxiv.org/abs/2003.01690)
- [RobustBench](https://robustbench.github.io/)
- [timm Library](https://github.com/huggingface/pytorch-image-models)
