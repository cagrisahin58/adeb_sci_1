# Adversarial Defense Projesi - Yol Haritası

> Son güncelleme: 2026-01-08
> Amaç: CNN vs ViT adversarial robustness karşılaştırması (SCI paper)

---

## 1. MEVCUT DURUM

### 1.1 Eğitilmiş Modeller
| Model | Eğitim Türü | Clean Acc | Durum |
|-------|-------------|-----------|-------|
| ResNet18 | Clean | 94.37% | ✅ Tamamlandı |
| ResNet18 | Adversarial Training | ⚠️ | 🔄 Yeniden eğitiliyor (100 epoch) |
| ResNet18 | TRADES | - | ❌ Başarısız (instabilite) |
| ViT-Tiny | Clean | 78.69% | ⚠️ Düşük (resize sorunu) |
| ViT-Tiny | Adversarial Training | 64.05% | ⚠️ Düşük |
| DenseNet121 | Clean | ~95% | ✅ Tamamlandı |

### 1.2 Saldırı Sonuçları (ε=8/255)
| Model | FGSM | PGD | AutoAttack |
|-------|------|-----|------------|
| ResNet18 Clean | 30.59% | 0.00% | 0.00% |
| ResNet18 Adv | 52.76% | 44.98% | 40.50% |
| ViT-Tiny Clean | 2.14% | 0.00% | - |
| ViT-Tiny Adv | 31.15% | 28.42% | - |

### 1.3 Literatür Karşılaştırması
| Metrik | SOTA (RobustBench) | Bizim En İyi | Fark |
|--------|-------------------|--------------|------|
| AutoAttack ε=8/255 | ~71% (WRN+extra) | 40.50% | -30.5% |
| AutoAttack ε=8/255 | ~55-60% (ResNet18) | 40.50% | -15-20% |

---

## 2. TESPİT EDİLEN SORUNLAR

- [ ] **TRADES v2**: LR=0.001 çok düşük, loss düzgün düşmüyor
- [ ] **ViT**: 32x32→224x224 resize performansı düşürüyor
- [ ] **Epoch sayısı**: 25-50 epoch yetersiz, SOTA 100-200 kullanıyor
- [ ] **TTA**: Sadece +0.2% etki, beklenen +2-5%
- [ ] **WideResNet yok**: SOTA karşılaştırması için gerekli

---

## 3. İYİ GİDEN ŞEYLER

- [x] ResNet18 clean training başarılı (94.47%)
- [x] Adversarial training çalışıyor (+65% PGD robustness)
- [x] Gradient analizi tamamlandı (CNN vs ViT farkları net)
- [x] Transfer attack analizi tamamlandı (CNN→ViT: 70%, ViT→CNN: 40%)
- [x] Pipeline otomatize edilmiş
- [x] Kod modüler ve genişletilebilir

---

## 4. YAPILACAKLAR

### Aşama 1: TRADES Debug ve Düzeltme
- [ ] **TRADES implementasyonu debug**
  - Step scheduler kullan (cosine yerine milestone)
  - LR warmup ekle
  - Gradient clipping kontrol et
  - Beta değerini düşür (6.0 → 3.0 dene)

- [ ] **Alternatif: Daha fazla epoch Adv Training**
  - Mevcut adversarial training 100 epoch'a çıkar
  - Bu çalışan bir yöntem, TRADES'ten önce dene

### Aşama 2: Model Genişletme
- [ ] **WideResNet-28-10 ekleme**
  - SOTA karşılaştırması için
  - Beklenen: ~58-62% AutoAttack

- [ ] **ViT CIFAR-native model**
  - vit_tiny_patch4_32 (resize yok)
  - Beklenen: +10% clean accuracy

### Aşama 3: Gelişmiş Teknikler
- [ ] AWP (Adversarial Weight Perturbation)
- [ ] MART defense denemesi
- [ ] Extra data (opsiyonel)

### Aşama 4: Analiz Tamamlama
- [ ] Epsilon sweep (1/255 → 16/255)
- [ ] Layer-wise vulnerability analizi
- [ ] Attention degradation visualization
- [ ] SCI paper figürleri

---

## 5. DENEY KAYITLARI

### 2026-01-08: Model Dosyası Analizi ve Yeniden Eğitim (Seans 3)

**Sorun Tespiti:**
- ResNet18 adversarial training modeli test edildi
- Beklenen Clean Acc: ~82% (önceki raporlar)
- Gerçek Clean Acc: 44.68% ❌
- Dec 30 değerlendirmesi: 63.38% (model dosyası bozulmuş)

**Checkpoint Analizi:**
- best.pth: Epoch 12, Adv Acc: 28.98%, Clean: 44.68%
- last.pth: Epoch 24, Adv Acc: 25.11%, Clean: 43.72%
- Model performansı çok düşük, dosya bozulmuş veya yanlış parametrelerle eğitilmiş

**Çözüm:**
- Yeni adversarial training başlatıldı: 100 epoch
- Pretrained: models/resnet18/clean/best.pth (94.37% clean)
- LR: 0.01, eps: 8/255, alpha: 2/255, steps: 10
- Eğitim devam ediyor...

---

### 2026-01-05: TRADES v3 Deneyleri (Seans 2)

**Deneme 1: Pretrained + LR=0.1**
- Sonuç: Catastrophic forgetting (Clean: 15% ilk epoch'ta)
- Sebep: LR çok yüksek

**Deneme 2: Pretrained + LR=0.01**
- Sonuç: Model kötüleşiyor (epoch 11'de 33% adv)
- Sebep: LR hala yüksek veya TRADES uyumsuzluğu

**Deneme 3: Scratch + LR=0.1**
- Sonuç: Model çöküyor (epoch 14'te 10% - random seviyesi)
- Sebep: TRADES implementasyonunda veya LR scheduler'da sorun var

**Mevcut Adv Training Model Değerlendirmesi:**
| Attack | ε=0.0078 | ε=0.0157 | ε=0.0314 |
|--------|----------|----------|----------|
| Clean | 44.68% | - | - |
| FGSM | 40.64% | 36.74% | 29.20% |
| PGD | 40.70% | 36.84% | 29.00% |

> Not: Bu sonuçlar önceki raporlardan (Clean: 82%) farklı - model değişmiş olabilir

**Sonuç:** TRADES implementasyonu stabil değil, debug gerekiyor

### 2025-01-05: Proje Analizi (Seans 1)
- Tüm mevcut sonuçlar incelendi
- Literatür karşılaştırması yapıldı
- TRADES v3 ve WideResNet önceliklendirildi

---

## 6. DOSYA YAPISI

```
models/
├── resnet18/clean/best.pth          ✅
├── resnet18/adv/adversarial_training/best.pth  ✅
├── resnet18/adv/trades/best.pth     ⚠️ (v2, suboptimal)
├── vit_tiny/clean/best.pth          ✅
├── vit_tiny/adv/best.pth            ✅
└── densenet121/clean/best.pth       ✅

results/
├── sci_paper/                       ✅ Gradient + Transfer analizleri
└── *.csv, *.png                     ✅ Attack sonuçları
```

---

## 7. KOMUTLAR (Referans)

```bash
# TRADES v3 eğitimi (TODO: config güncelle)
python -m cli.main train --model resnet18 --defense trades --epochs 100

# Evaluation
python -m cli.main evaluate --model resnet18 --checkpoint models/resnet18/adv/trades/best.pth

# AutoAttack
python -m cli.main autoattack --model resnet18 --eps 0.0314
```

---

## 8. NOTLAR

- Dataset: CIFAR-10 (50K train, 10K test)
- GPU: RTX 5060 Ti (16GB VRAM)
- Framework: PyTorch 2.6.0, CUDA 12.8
- Normalization: [0,1] aralığı (ImageNet norm yok)
