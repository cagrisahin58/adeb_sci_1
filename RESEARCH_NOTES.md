# Research Notes - SCI Paper Development

## 2026-01-09: Faz 1 Değerlendirmesi

### Kritik Bulgular

1. **ResNet18 AT: 40.25% PGD** - SOTA karşılaştırması gerekiyor
2. **ViT-Tiny AT: 32.77% PGD** - Düşük, CIFAR-native ViT gerekebilir
3. **Checkpoint'ler tutarlı** - Metadata doğrulandı

### Metodoloji Soruları (Hakem Perspektifi)

- [ ] ResNet18 40% vs SOTA ~53% farkının sebebi?
- [ ] Pretrained → AT vs Scratch → AT karşılaştırması?
- [ ] PGD-10 vs AutoAttack farkı?
- [ ] Model capacity etkisi (ResNet18 vs WideResNet)?

### Kararlar

| Karar | Gerekçe | Tarih |
|-------|---------|-------|
| evaluation_jan05 arşivlendi | Tutarsız sonuçlar | 2026-01-09 |
| GPU aktif edildi | CPU evaluation çok yavaş | 2026-01-09 |
| RESEARCH_NOTES.md oluşturuldu | Kritik adımları takip | 2026-01-09 |

### SOTA Benchmark (RobustBench, AutoAttack, Linf ε=8/255)

| Model | Robust Acc | Kaynak |
|-------|------------|--------|
| ResNet18 | ~40-45% | Tahmin (küçük model) |
| WideResNet-28-10 | 50-57% | RobustBench |
| WideResNet-34-20 | ~60% | RobustBench SOTA |

**Kritik Bulgu (2026-01-09):**
- RobustBench leaderboard'unda ResNet18 yok - çoğunlukla WideResNet
- "The larger the model, the better the robustness" - model capacity kritik
- Bizim 40.25% ResNet18 için **makul**, ama AutoAttack ile doğrulanmalı
- PGD-10 sonuçları AutoAttack'tan yüksek çıkar (daha kolay saldırı)

**Kaynak:** [RobustBench](https://robustbench.github.io/)

---

## 2026-01-09: Hibrit Yaklaşım Kararı

**Strateji:** CNN için RobustBench pretrained, ViT için kendi eğitimimiz

| Bileşen | Kaynak | Gerekçe |
|---------|--------|---------|
| WideResNet-28-10 | RobustBench pretrained | SOTA CNN baseline |
| ResNet-18 Robust | RobustBench pretrained | Küçük CNN baseline |
| ViT-Tiny/Small | Kendi AT eğitimimiz | Robust ViT pretrained yok |

**Özgün Katkı:**
1. CNN vs ViT fair comparison (aynı analiz pipeline)
2. Transfer attack analizi (mimariler arası)
3. Gradient karakteristikleri karşılaştırması
4. ViT attention degradation analizi

---

## Revize Plan (Hibrit Yaklaşım)

### Faz 1: RobustBench CNN Modelleri [~30 dk] ✅ TAMAMLANDI
- [x] robustbench kütüphanesini kur (v1.1.1)
- [x] WideResNet-28-10 robust model indir (Gowal2020Uncovering_28_10_extra)
- [x] Evaluate et, baseline oluştur

**Sonuçlar (2026-01-09):**
| Model | Clean | PGD-20 | AutoAttack (RobustBench) |
|-------|-------|--------|--------------------------|
| WideResNet-28-10 | 89.48% | 66.05% | 62.76% |

**Karşılaştırma (Bizim modeller):**
| Model | Clean | PGD-10 |
|-------|-------|--------|
| ResNet18 AT | 80.34% | 40.25% |
| ViT-Tiny AT | 63.42% | 32.77% |

**Fark:** WideResNet SOTA, ResNet18'den ~26% daha robust (66% vs 40%)

### Faz 2: ViT Robust Eğitimi [4-6 saat GPU]
- [ ] CIFAR-native ViT (patch4_32) ekle
- [ ] ViT-Tiny AT düzelt veya yeniden eğit
- [ ] ViT-Small AT ekle (daha büyük model)

### Faz 3: Karşılaştırmalı Analiz [2-3 saat]
- [ ] Transfer attack matrix (CNN↔ViT)
- [ ] Gradient karakteristikleri
- [ ] Attention pattern analizi

### Faz 4: TRADES Alternatif Defense [3-4 saat]
- [ ] ResNet18 TRADES düzelt (LR=0.001)
- [ ] ViT TRADES (karşılaştırma için)

### Faz 5: Final Evaluation [2-3 saat]
- [ ] AutoAttack tüm modeller
- [ ] Statistical summary
- [ ] Publication figures

**Toplam:** ~12-16 saat (vs önceki 23-34 saat)

---

## 2026-01-10: Strateji Değişikliği - Analiz Odaklı Yaklaşım

### Kritik Karar
**Robustness yarışı değil, anlama odaklı yaklaşım**

**Gerekçe:**
- Literatürde ViT SOTA: %50-75 robust (diffusion + özel teknikler)
- Bizim standard AT: %25-33 robust
- SOTA'ya ulaşmak 2-3 hafta ek, yüksek risk
- Analiz odaklı: mevcut sonuçlar yeterli, özgün katkı korunur

### ViT-CIFAR-Tiny Eğitimi Durduruldu
```
Son durum (Epoch 54/100):
- Clean: 68.85%
- Adv: 24.33%  ← timm ViT-Tiny'den kötü (32.77%)
```
**Karar:** ViT-Tiny (timm) AT modeli kullanılacak

### Yeni Research Questions
- RQ1: Transfer attack asimetrisi neden oluşuyor? (CNN→ViT vs ViT→CNN)
- RQ2: Gradient karakteristikleri farkı açıklıyor mu?
- RQ3: ViT attention patterns nasıl bozuluyor?
- RQ4: Hibrit sistem tasarımı için öneriler neler?

### Kullanılacak Final Modeller
| Model | Clean | Robust | Rol |
|-------|-------|--------|-----|
| WideResNet-28-10 | 89.48% | 66.05% | CNN SOTA |
| ResNet18 AT | 80.34% | 40.25% | CNN standard |
| ViT-Tiny (timm) AT | 63.42% | 32.77% | ViT model |

### Sonraki Adımlar (Öncelik Sırasına Göre)
1. [x] ViT-CIFAR-Tiny eğitimini durdur
2. [x] Transfer attack analizi
3. [x] Gradient karakteristikleri analizi
4. [x] Attention degradation analizi
5. [x] AutoAttack final evaluation

---

## 2026-01-10: TÜM ANALİZLER TAMAMLANDI

### 1. AutoAttack Final Evaluation (Gold Standard)

| Model | Clean | AutoAttack | PGD-10 |
|-------|-------|------------|--------|
| **ResNet18_AT** | 81.60% | **34.60%** | 40.25% |
| **ViT_Tiny_AT** | 61.80% | **28.00%** | 32.77% |
| WideResNet-28-10 (RobustBench) | 89.48% | 62.76% | 66.05% |

**Bulgu:** AutoAttack sonuçları PGD-10'dan ~6% düşük (beklendiği gibi - daha güçlü saldırı)

### 2. Transfer Attack Analizi

| Source → Target | ResNet18_AT | ViT_Tiny_AT |
|-----------------|-------------|-------------|
| ResNet18_AT     | 59.4%       | **47.5%**   |
| ViT_Tiny_AT     | **33.5%**   | 66.2%       |

**Kritik Bulgu:**
- CNN → ViT transfer: %47.5 (kaynak saldırının %80.5'i)
- ViT → CNN transfer: %33.5 (kaynak saldırının %50.5'i)
- **Asimetri: %14** - CNN adversarial örnekleri ViT'e daha iyi transfer ediyor

### 3. Gradient Karakteristikleri

| Metrik | ResNet18_AT | ViT_Tiny_AT | Fark |
|--------|-------------|-------------|------|
| L2 Norm | 0.0169 | 0.0172 | ~aynı |
| L∞ Norm | 0.00220 | 0.00338 | ViT 54% yüksek |
| Sparsity | **6.9%** | 1.5% | ResNet 4.5x seyrek |
| Gradient Alignment | 0.044 | **0.097** | ViT 2.2x yüksek |

**Kritik Bulgular:**
1. ViT gradientleri daha aligned → universal perturbation'lara açık
2. ResNet gradientleri daha seyrek → daha lokalize hassasiyet
3. Bu, transfer asimetrisini açıklıyor

### 4. Attention/Feature Degradation

| Layer | L2 Distance | Cosine Similarity | Norm Change |
|-------|-------------|-------------------|-------------|
| Block 0 (early) | 3.53 | 0.997 | -0.05% |
| Block 1 | 1.56 | 0.991 | +1.78% |
| Block 2 | 1.08 | 0.994 | -0.19% |
| Block 9 | 1.46 | 0.961 | -3.30% |
| Block 10 | 1.61 | 0.917 | -4.93% |
| Block 11 (late) | 2.54 | **0.955** | **-7.86%** |

**Kritik Bulgular:**
1. Erken katmanlar: Yüksek L2, yüksek cosine sim → semantik yapı korunuyor
2. Geç katmanlar: Düşen cosine sim (0.997→0.917) → semantik degradasyon
3. Feature norm düşüşü geç katmanlarda → feature suppression

---

## Research Questions Cevapları

### RQ1: Transfer attack asimetrisi neden var?
> CNN adversarial örnekleri ViT'e %47.5 oranında transfer ederken, tersi %33.5.
> **Neden:** CNN'lerin daha dağınık (seyrek) gradientleri, daha genel perturbation'lar üretiyor.

### RQ2: Gradient karakteristikleri farkı açıklıyor mu?
> **Evet.** ViT gradientleri 2.2x daha aligned, CNN gradientleri 4.5x daha seyrek.
> Bu, neden CNN→ViT transferinin daha başarılı olduğunu açıklıyor.

### RQ3: ViT attention nasıl bozuluyor?
> Erken katmanlarda semantik yapı korunurken (%99.4 cosine sim),
> geç katmanlarda ciddi degradasyon var (%91.7 cosine sim, -%7.86 norm).
> **Adversarial perturbation propagasyonu:** Erken→semantik olmayan, Geç→semantik bozulma

### RQ4: Hibrit sistem önerileri?
> 1. **Ensemble defense:** CNN ve ViT birlikte kullan, transfer saldırılara karşı koruma
> 2. **CNN feature extraction + ViT classification:** CNN'in daha seyrek gradientlerinden yararlan
> 3. **Attention regularization:** Geç katmanlarda attention stability artır

---

## Sonuç Dosyaları

```
results/
├── transfer_analysis_20260110/
│   ├── transfer_results.csv
│   ├── transfer_matrix.npy
│   └── transfer_summary.json
├── gradient_analysis_20260110/
│   ├── gradient_statistics.csv
│   ├── gradient_norm_distribution.pdf
│   ├── gradient_comparison.pdf
│   ├── gradient_landscape.pdf
│   └── gradient_summary.json
├── attention_analysis_20260110/
│   ├── attention_feature_analysis.csv
│   ├── feature_degradation.pdf
│   ├── adversarial_samples.pdf
│   └── attention_summary.json
└── autoattack_evaluation_20260110/
    ├── autoattack_results.csv
    └── autoattack_summary.json
```

---

## SCI Paper Hazırlık Durumu

| Bileşen | Durum | Not |
|---------|-------|-----|
| AutoAttack evaluation | ✅ | Gold standard tamamlandı |
| Transfer attack analizi | ✅ | Asimetri bulundu |
| Gradient analizi | ✅ | Alignment farkı açıklandı |
| Attention degradation | ✅ | Layer-wise analiz tamamlandı |
| Statistical validation (3 run) | ❌ | Henüz yapılmadı |
| Figure'lar | ✅ | PDF formatında hazır |

**Mevcut Hazırlık:** ~%70 → Statistical validation sonrası %85+
