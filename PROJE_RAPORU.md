# Adversarial Defense Study - Kapsamlı Proje Raporu

> Oluşturulma: 2026-01-05
> Yazar: Cagri Sahin
> Durum: Devam Ediyor

---

## 1. PROJENİN AMACI

### 1.1 Ana Hedef
**CNN (ResNet) ve Vision Transformer (ViT) mimarilerinin adversarial saldırılara karşı dayanıklılığını karşılaştırmak** ve bu farkın nedenlerini mekanistik olarak açıklamak.

### 1.2 Araştırma Soruları
1. CNN'ler mi yoksa ViT'ler mi adversarial saldırılara karşı daha dayanıklı?
2. Transfer attack'lar mimariler arasında nasıl çalışıyor? (CNN→ViT vs ViT→CNN)
3. Gradient karakteristikleri (L2 norm, sparsity) bu farkı açıklıyor mu?
4. ViT'lerin attention pattern'leri adversarial örneklerde nasıl bozuluyor?

### 1.3 Hipotezler
- **H1:** CNN'ler ViT'lerden %15-20 daha robust olacak
- **H2:** CNN'den üretilen perturbation'lar ViT'e daha iyi transfer edecek (asimetri)
- **H3:** CNN'lerin gradient'leri daha uniform, ViT'lerinki daha sparse olacak
- **H4:** Adversarial örneklerde ViT attention entropy'si artacak (dikkat dağılacak)

---

## 2. HEDEF YAYIN

### 2.1 Yayın Türü
**SCI İndeksli Dergi Makalesi** (Q1/Q2 hedefi)

### 2.2 Hedef Dergiler (Önem Sırasına Göre)
1. **IEEE Transactions on Neural Networks and Learning Systems** (IF: ~14)
2. **Pattern Recognition** (IF: ~8)
3. **Neural Networks** (IF: ~7.8)
4. **Computer Vision and Image Understanding** (IF: ~4.5)
5. **Expert Systems with Applications** (IF: ~8.5)

### 2.3 Önerilen Makale Başlığı
> "Understanding Adversarial Vulnerability Gap Between CNNs and Vision Transformers: A Mechanistic Analysis with Cross-Architecture Transfer Attacks"

### 2.4 Makale Yapısı (Planlanan)
```
1. Introduction
   - Adversarial robustness önemi
   - CNN vs ViT karşılaştırması literatür boşluğu

2. Related Work
   - Adversarial training yöntemleri (AT, TRADES, MART)
   - Transfer attack'lar
   - ViT robustness çalışmaları

3. Methodology
   - Modeller: ResNet18, ViT-Tiny, DenseNet121
   - Saldırılar: FGSM, PGD, AutoAttack
   - Savunmalar: Adversarial Training, TRADES
   - Analizler: Gradient, Transfer, Attention

4. Experiments
   - Dataset: CIFAR-10
   - Setup: PyTorch, NVIDIA GPU

5. Results
   - 5.1 Robustness Karşılaştırması
   - 5.2 Transfer Attack Analizi
   - 5.3 Gradient Karakteristikleri
   - 5.4 Attention Degradation

6. Discussion
7. Conclusion
```

---

## 3. PROJE TARİHÇESİ

### Faz 1: Altyapı Kurulumu (Tamamlandı)
- [x] Modüler kod yapısı oluşturuldu (`src/`)
- [x] Model registry sistemi (ResNet, ViT, DenseNet)
- [x] Attack registry sistemi (FGSM, PGD, AutoAttack, DeepFool, C&W)
- [x] Defense registry sistemi (AT, TRADES, MART, TTA)
- [x] CLI arayüzü (`cli/`)
- [x] Test suite (`tests/` - 32+ test)

### Faz 2: Model Eğitimi (Kısmen Tamamlandı)
- [x] ResNet18 Clean Training → 94.47% accuracy
- [x] ResNet18 Adversarial Training → ~82% clean, ~45% robust (PGD)
- [x] ViT-Tiny Clean Training → 78.69% accuracy
- [x] ViT-Tiny Adversarial Training → 64.05% clean
- [x] DenseNet121 Clean Training → ~95% accuracy
- [ ] TRADES eğitimi → **SORUNLU** (instabilite)

### Faz 3: Değerlendirme (Kısmen Tamamlandı)
- [x] FGSM attack değerlendirmesi
- [x] PGD attack değerlendirmesi
- [x] AutoAttack değerlendirmesi (ResNet)
- [x] TTA defense değerlendirmesi
- [ ] Kapsamlı epsilon sweep

### Faz 4: SCI Analizleri (Kısmen Tamamlandı)
- [x] Gradient analizi (L2 norm, sparsity, alignment)
- [x] Transfer attack analizi (CNN→ViT, ViT→CNN)
- [ ] Attention degradation analizi (görselleştirme eksik)
- [ ] Yayın kalitesi figürler

---

## 4. MEVCUT SONUÇLAR

### 4.1 Clean Accuracy
| Model | Clean Training | Adversarial Training | Fark |
|-------|---------------|---------------------|------|
| ResNet18 | 94.47% | 82.45% | -12.02% |
| ViT-Tiny | 78.69% | 64.05% | -14.64% |
| DenseNet121 | ~95% | - | - |

### 4.2 Adversarial Robustness (ε=8/255)
| Model | FGSM | PGD | AutoAttack |
|-------|------|-----|------------|
| ResNet18 Clean | 30.59% | 0.00% | 0.00% |
| ResNet18 Adv | 52.76% | 44.98% | 40.50% |
| ViT-Tiny Clean | 2.14% | 0.00% | - |
| ViT-Tiny Adv | 31.15% | 28.42% | - |

### 4.3 Transfer Attack Analizi
```
Source → Target | Success Rate
----------------|-------------
CNN → ViT       | ~65-70%
ViT → CNN       | ~40-50%
```
**Bulgu:** CNN perturbation'ları ViT'e daha iyi transfer ediyor (asimetri mevcut ✓)

### 4.4 Gradient Analizi
| Metrik | ResNet | ViT | DenseNet |
|--------|--------|-----|----------|
| L2 Norm Mean | 0.001668 | 0.000399 | 0.000058 |
| Sparsity | 3.25% | 15.04% | 68.51% |
| Alignment | 0.0622 | 0.2547 | 0.1498 |

**Bulgu:** ResNet gradient'leri daha güçlü ve uniform, ViT daha sparse ✓

### 4.5 Literatür Karşılaştırması
| Metrik | SOTA (RobustBench) | Bizim En İyi | Fark |
|--------|-------------------|--------------|------|
| AutoAttack ε=8/255 | ~71% (WRN+extra) | 40.50% | -30.5% |
| AutoAttack ε=8/255 | ~55-60% (ResNet18) | 40.50% | -15-20% |

**Durum:** Sonuçlar literatürün gerisinde, iyileştirme gerekli

---

## 5. TESPİT EDİLEN SORUNLAR

### 5.1 TRADES Implementasyonu (Kritik)
**Sorun:** TRADES eğitimi stabil değil, model çöküyor
- Pretrained + LR=0.1: Catastrophic forgetting
- Pretrained + LR=0.01: Model kötüleşiyor
- Scratch + LR=0.1: Random seviyeye düşüyor

**Olası Nedenler:**
- Cosine annealing yerine step scheduler gerekebilir
- LR warmup eksik
- Beta değeri (6.0) çok yüksek olabilir

### 5.2 Model Dosyası Tutarsızlığı
**Sorun:** Değerlendirme sonuçları (Clean: 44%) önceki raporlardan (82%) farklı
**Olası Neden:** Model dosyası değişmiş veya yanlış model yüklenmiş

### 5.3 ViT Performansı
**Sorun:** ViT clean accuracy düşük (78% vs beklenen ~90%)
**Neden:** 32x32 → 224x224 resize işlemi performansı düşürüyor
**Çözüm:** CIFAR-native ViT modeli kullanmak (vit_tiny_patch4_32)

### 5.4 Literatürden Uzaklık
**Sorun:** Robust accuracy SOTA'nın ~15-30 puan gerisinde
**Nedenler:**
- Yetersiz epoch sayısı (25-50 vs SOTA 100-200)
- Extra data kullanılmamış
- WideResNet kullanılmamış

---

## 6. YAPILACAKLAR (Öncelik Sırasına Göre)

### Acil (Bu Hafta)
1. [ ] Model dosyalarını kontrol et, doğru olanı bul
2. [ ] Standard Adversarial Training'i 100 epoch eğit
3. [ ] TRADES implementasyonunu debug et

### Kısa Vadeli (2 Hafta)
4. [ ] WideResNet-28-10 ekle ve eğit
5. [ ] ViT için CIFAR-native model dene
6. [ ] Kapsamlı epsilon sweep yap

### Orta Vadeli (1 Ay)
7. [ ] Attention degradation görselleştirmelerini tamamla
8. [ ] Yayın kalitesi figürler oluştur
9. [ ] Makale taslağını yaz

### Uzun Vadeli
10. [ ] AWP (Adversarial Weight Perturbation) ekle
11. [ ] Extra data ile eğitim (opsiyonel)
12. [ ] Ablation studies

---

## 7. TEKNİK DETAYLAR

### 7.1 Ortam
- **OS:** Ubuntu 24.04 (Docker container)
- **GPU:** NVIDIA RTX 5060 Ti (16GB VRAM)
- **Framework:** PyTorch 2.6.0, CUDA 12.8
- **Python:** 3.12.3

### 7.2 Dataset
- **CIFAR-10:** 50K train, 10K test, 32x32 RGB
- **Normalization:** [0, 1] aralığı (ImageNet norm yok)

### 7.3 Eğitim Parametreleri
```yaml
ResNet Clean:
  epochs: 50, lr: 0.1, optimizer: SGD, scheduler: cosine

ResNet Adversarial:
  epochs: 25, lr: 0.01, optimizer: SGD, defense: AT
  eps: 8/255, alpha: 2/255, steps: 10

TRADES (Hedef):
  epochs: 100, lr: 0.1, beta: 6.0
  scheduler: step (milestone)
```

### 7.4 Saldırı Parametreleri
```yaml
FGSM: eps ∈ {1/128, 2/128, 4/128, 8/128}
PGD: eps ∈ {1/128, 2/128, 4/128, 8/128}, steps=10, alpha=2/255
AutoAttack: eps ∈ {1/128, 2/128, 4/128, 8/128}, version=standard
```

---

## 8. DOSYA YAPISI

```
adeb_sci_1/
├── src/                    # Kaynak kod
│   ├── models/             # Model tanımları
│   ├── attacks/            # Saldırı implementasyonları
│   ├── defenses/           # Savunma yöntemleri
│   ├── training/           # Eğitim modülleri
│   ├── evaluation/         # Değerlendirme araçları
│   └── analysis/           # SCI analiz modülleri
├── cli/                    # CLI komutları
├── configs/                # YAML konfigürasyonlar
├── models/                 # Eğitilmiş modeller
│   ├── resnet18/clean/
│   ├── resnet18/adv/
│   └── vit_tiny/
├── results/                # Sonuçlar
│   ├── sci_paper/          # SCI analizleri
│   └── evaluation_jan05/   # Son değerlendirme
├── logs/                   # Eğitim logları
├── YOL_HARITASI.md         # İlerleme takibi
├── PROJE_RAPORU.md         # Bu dosya
└── DOCKER_VSCODE_GPU_KURULUM.md  # Kurulum rehberi
```

---

## 9. KAYNAKLAR VE REFERANSLAR

### Temel Makaleler
1. **TRADES:** Zhang et al., "Theoretically Principled Trade-off between Robustness and Accuracy", ICML 2019
2. **AutoAttack:** Croce & Hein, "Reliable evaluation of adversarial robustness with an ensemble of diverse parameter-free attacks", ICML 2020
3. **RobustBench:** Croce et al., "RobustBench: a standardized adversarial robustness benchmark", NeurIPS 2021
4. **ViT:** Dosovitskiy et al., "An Image is Worth 16x16 Words", ICLR 2021

### Benchmarklar
- RobustBench: https://robustbench.github.io/
- CIFAR-10 Leaderboard: ~71% SOTA (WRN-70-16 + extra data)

---

## 10. NOTLAR VE GÖZLEMLER

### Öğrenilen Dersler
1. TRADES eğitimi hassas - doğru LR scheduler kritik
2. Pretrained model'den başlamak her zaman iyi değil
3. Cosine annealing adversarial training için sorunlu olabilir
4. Model dosyalarını düzenli kontrol etmek önemli

### Sorular (Claude AI ile Tartışılacak)
1. TRADES için optimal LR scheduler nedir?
2. WideResNet vs ResNet18 trade-off nedir?
3. ViT için CIFAR-native model gerçekten daha iyi mi?
4. Extra data olmadan SOTA'ya ne kadar yaklaşılabilir?

---

## 11. İLETİŞİM VE TAKİP

### Dosya Güncellemeleri
- **YOL_HARITASI.md:** Her seansta güncellenir
- **PROJE_RAPORU.md:** Önemli milestone'larda güncellenir

### Claude AI Seans Notları
- Seans 1 (2025-01-05): Proje analizi, literatür karşılaştırması
- Seans 2 (2026-01-05): TRADES deneyleri, başarısız

---

> **Son Güncelleme:** 2026-01-05
> **Sonraki Adım:** Model dosyalarını kontrol et, ardından Standard AT 100 epoch eğit
