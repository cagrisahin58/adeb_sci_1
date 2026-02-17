# CLAUDE.md - Adversarial Defense Study

Bu dosya, Claude Code'un bu proje ile etkili calışabilmesi icin gerekli baglamı saglar.

---

## Gelistirme Ortamı

**Container:** `med-lab` (dogrudan icindeyiz)
- Docker exec komutlarına gerek yok
- SSH ile evden baglanıldıgında: `claude --continue`

**Donanım:**
- GPU: RTX 5060 Ti (16GB VRAM)
- Framework: PyTorch 2.6.0, CUDA 12.8

**Diger Container'lar:**
- `vit_ecl` egitimi ayrı container'da calışıyor olabilir
- GPU paylaşımlı - egitim oncesi `nvidia-smi` kontrol et

---

## Proje Ozeti

**CNN vs ViT adversarial robustness karşılaştırması** icin SCI makalesi calışması.
CIFAR-10 uzerinde derin ogrenme modellerinin adversarial saldırılara karşı dayanıklılıgını degerlendirir.

**Arastırma Soruları:**
1. CNN'ler mi ViT'ler mi daha robust?
2. Transfer attack'lar mimariler arasında nasıl calışıyor?
3. Gradient karakteristikleri bu farkı acıklıyor mu?
4. ViT attention pattern'leri adversarial orneklerde nasıl bozuluyor?

---

## Mevcut Durum (2026-02-17 - GUNCELLENDI)

### Strateji: Analiz Odaklı Yaklasım
**Robustness yarışı degil, davranış analizi**

> "Neden farklı davranıyorlar?" sorusuna cevap arıyoruz.

### Hedef Dergi: IEEE Access (Q2, IF ~3.4)

### Tamamlanan Analizler (RUN2 - TUTARLI)
| Analiz | Sonuc (run2) | Durum |
|--------|-------|-------|
| Transfer Attack | CNN→ViT: 41.2%, ViT→CNN: 36.1% (5.1pp asimetri) | Tamamlandı |
| Gradient Karakteristikleri | CNN 1.7x sparse, alignment ~esit | Tamamlandı |
| Feature Degradation | cosine 0.995→0.958, norm max -1.43% | Tamamlandı |
| AutoAttack Eval (run2) | ResNet: 36.0%, ViT: 32.4% | Tamamlandı |
| Istatistiksel Dogrulama (run2) | 3 eval seed, <0.25% varyans | Tamamlandı |

### Model Performansları (GUNCELLENDI)

| Model | Clean Acc | PGD (8/255) | AutoAttack | Kaynak |
|-------|-----------|-------------|------------|--------|
| **WideResNet-28-10** | 89.48% | 66.05% | 62.76% | RobustBench |
| **ResNet18 AT (run2)** | 81.80% | **40.97%** | **36.0%** | Kendi (01/11) |
| ResNet18 AT (run1) | 80.34% | 40.25% | 34.6% | Kendi |
| **ViT-Tiny AT (run2)** | 73.60% | **36.87%** | **32.4%** | Kendi (01/11) |
| ViT-Tiny AT (run1) | 63.42% | 32.77% | 28.0% | Kendi |
| ResNet18 Clean | 94.37% | 0% | - | Kendi |
| ViT-Tiny Clean | 77.50% | 0% | - | Kendi |

### Model Dosyaları
```
models/
├── robustbench/
│   └── wideresnet28_10_robust.pth  # 89.48% clean, 62.76% AA
├── resnet18/
│   ├── clean/best.pth              # 94.37%
│   ├── adv/adversarial_training/best.pth  # run1: 40.25% PGD, 34.6% AA
│   └── adv/at_run2/.../best.pth    # run2: 40.97% PGD (YENİ!)
├── vit_tiny/
│   ├── clean/best.pth              # 77.50%
│   ├── adv/adversarial_training/best.pth  # run1: 32.77% PGD, 28.0% AA
│   └── adv/at_run2/.../best.pth    # run2: 36.87% PGD (YENİ!)
└── densenet121/
    └── clean/best.pth              # 95.09%
```

---

## Tamamlanan Fazlar

- [x] Faz 1: RobustBench CNN (WideResNet-28-10)
- [x] Faz 2: Model Egitimleri (ResNet18 AT, ViT-Tiny AT)
- [x] Faz 3: Karsılastırmalı Analiz (Transfer, Gradient, Attention)
- [x] Faz 4: Makale taslağı ve Q1 revizyonu
- [x] Early stopping mekanizması eklendi
- [x] ResNet18 AT run2 egitimi (40.97% PGD)
- [x] ViT-Tiny AT run2 egitimi (36.87% PGD)

### Bekleyen Isler
- [x] Run2 modelleri icin AutoAttack evaluation (ResNet: 36.0%, ViT: 32.4%)
- [x] Figure kalite kontrolu (final/ klasorune kopyalandı)
- [x] Run2 ile tum analizler tekrarlandi (transfer, gradient 500 ornek, feature degradation 100 ornek, stat validation)
- [x] Hakemlik (hakem-simulasyonu + sci-peer-reviewer) tamamlandi
- [x] Referans duzeltmeleri (5 hata giderildi, Bai et al. eklendi)
- [x] Makale revizyonlari (F2, F3, MAJ1-7, 14 minor)
- [x] IEEE Access format uyumu
- [x] Gonderim paketi (cover letter, reviewers, checklist)
- [x] Tablolar run2 sayilariyla guncellendi
- [x] Anlatı run2 verileriyle tutarli hale getirildi
- [x] LaTeX derleme kontrolu (0 undefined ref, 0 citation error)
- [ ] Intihal kontrolu (iThenticate)
- [ ] IEEE Author Portal'a yukleme

---

## Kritik Bilgiler

### Adversarial Training Parametreleri
```python
eps = 8/255      # 0.03137254901960784
alpha = 2/255    # 0.00784313725490196
steps = 10
```

### LR Secimi (ONEMLI!)
- **Clean training:** LR=0.1 (scratch'ten)
- **Adversarial training (pretrained'den):** LR=0.001
- LR=0.01 catastrophic forgetting yapıyor!

### Early Stopping
```bash
python -m cli.main train adversarial --patience 20  # 20 epoch iyilesme yoksa dur
```
- `--patience 0` = devre dışı (default)
- `--patience 20` = onerilen deger
- `min_delta = 0.1%` improvement threshold

**Etkinlik:** ViT-Tiny AT run2'de 51 epoch tasarruf (100→49)

---

## Hızlı Komutlar

```bash
# GPU durumu kontrol (EGITIM ONCESI!)
nvidia-smi

# Model degerlendirme
python -m cli.main evaluate robustness \
    --model-path models/resnet18/adv/adversarial_training/best.pth \
    --model-type resnet18 \
    --attacks fgsm pgd \
    --epsilons 0.00784 0.01569 0.0314

# AutoAttack evaluation
python experiments/run_autoattack_evaluation.py

# SCI analizleri
python experiments/run_sci_analysis.py --analysis gradient
python experiments/run_sci_analysis.py --analysis transfer
python experiments/run_sci_analysis.py --analysis attention
```

---

## Proje Yapısı (Ozet)

```
├── cli/                    # CLI komutları
├── src/
│   ├── models/             # ResNet, ViT, DenseNet, EfficientNet
│   ├── attacks/            # FGSM, PGD, C&W, DeepFool, AutoAttack
│   ├── defenses/           # AT, TRADES, MART, TTA
│   ├── training/           # Egitim dongulerı (+ early stopping)
│   ├── evaluation/         # Degerlendirme aracları
│   └── analysis/           # Gradient, Transfer, Attention analizi
├── models/                 # Egitilmis checkpointler
├── paper/                  # Makale dosyaları (manuscript/, figures/)
├── results/                # Deney sonucları
└── logs/                   # Egitim logları
```

---

## Ogrenilen Dersler

1. **Pretrained + yuksek LR = felaket:** 0.01 bile cok yuksek, 0.001 kullan
2. **Log dosyalarını kontrol et:** Birden fazla egitim varsa karısabilir
3. **Model capacity kritik:** WideResNet-28-10 (66%) >> ResNet18 (40%)
4. **Hibrit yaklasım:** CNN icin RobustBench, ViT icin kendi egitim
5. **Early stopping sart:** 35+ epoch iyilesme olmadan devam etmek GPU israfı
6. **GPU paylaşımı:** Baska container egitim yapıyor olabilir, kontrol et
7. **Otomatik egitim script:** `scripts/auto_train_vit.sh` GPU bekleyip egitim baslatiyor

---

## Ozgun Katkı (SCI Paper)

1. **CNN vs ViT fair comparison** - Aynı analiz pipeline ile
2. **Transfer attack analizi** - Mimariler arası saldırı transferi (asimetri!)
3. **Gradient karakteristikleri** - Robustness farkının matematiksel acıklaması
4. **Attention degradation** - ViT'te adversarial ornek etkisi

---

## Makale Durumu

| Bolum | Durum |
|-------|-------|
| Introduction | Tamamlandı, Q1 revize |
| Related Work | Tamamlandı, 2023-2025 referanslar eklendi |
| Methodology | Tamamlandı, Q1 revize |
| Experiments | Tamamlandı, Q1 revize |
| Discussion | Tamamlandı, Q1 revize |
| Conclusion | Tamamlandı, Q1 revize |

**Hedef Dergi:** IEEE Access (IF: ~3.4, Q2, Open Access)

---

## Referanslar

- [TRADES](https://arxiv.org/abs/1901.08573)
- [AutoAttack](https://arxiv.org/abs/2003.01690)
- [RobustBench](https://robustbench.github.io/)
