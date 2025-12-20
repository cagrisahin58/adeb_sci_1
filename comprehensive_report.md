
# Adversarial Model Defense: Performans ve Dayanıklılık Raporu

## 1. Temiz Modellerin Performansı

| Model          | Temiz Doğruluk (%) |
|----------------|-------------------|
| ResNet         | 94.47             |
| ViT            | 78.69             |

---

## 2. Adversarial Eğitilmiş Modellerin Performansı

| Model          | Temiz Doğruluk (%) |
|----------------|-------------------|
| ResNet (Adv)   | 82.45             |
| ViT (Adv)      | 64.05             |

---

## 3. FGSM Saldırı Sonuçları

### ResNet

| Eğitim   | ε=0.0078 | ε=0.0157 | ε=0.0314 |
|----------|----------|----------|----------|
| Temiz    | 45.06%   | 36.74%   | 30.59%   |
| Adv      | 75.07%   | 67.16%   | 52.76%   |

### ViT

| Eğitim   | ε=0.0078 | ε=0.0157 | ε=0.0314 |
|----------|----------|----------|----------|
| Temiz    | 7.17%    | 2.18%    | 2.14%    |
| Adv      | 55.72%   | 46.98%   | 31.15%   |

---

## 4. PGD Saldırı Sonuçları

### ResNet

| Eğitim   | ε=0.0078 | ε=0.0157 | ε=0.0314 |
|----------|----------|----------|----------|
| Temiz    | 9.69%    | 0.88%    | 0.00%    |
| Adv      | 74.75%   | 65.35%   | 44.98%   |

### ViT

| Eğitim   | ε=0.0078 | ε=0.0157 | ε=0.0314 |
|----------|----------|----------|----------|
| Temiz    | 1.45%    | 0.02%    | 0.00%    |
| Adv      | 55.66%   | 46.51%   | 28.42%   |

---

## 5. AutoAttack Sonuçları (ResNet Adv)

| Saldırı Türü      | Başlangıç Doğruluk | APGD-CE | APGD-T | FAB-T | SQUARE | Son |
|-------------------|--------------------|---------|--------|-------|--------|-----|
| 1.                | 84.10%             | 76.40%  | 74.90% | 74.90%| 74.90% |74.90%|
| 2.                | 84.10%             | 66.50%  | 63.00% | 63.00%| 63.00% |63.00%|
| 3.                | 84.10%             | 43.70%  | 40.50% | 40.50%| 40.50% |40.50%|

### ResNet Clean

| Başlangıç Doğruluk | APGD-CE | APGD-T | FAB-T | SQUARE | Son |
|--------------------|---------|--------|-------|--------|-----|
| 95.10%             | 2.20%   | 1.40%  | 1.40% | 1.40%  |1.40%|
| 95.10%             | 0.00%   |        |       |        |0.00%|

---

## 6. TTA (Test Time Augmentation) Savunma Sonuçları

### ResNet Adv

| Saldırı                 | Normal  | TTA     | Fark    |
|-------------------------|---------|---------|---------|
| Temiz                   | 82.45%  | 82.82%  | +0.37%  |
| FGSM (ε=0.0078)         | 75.07%  | 75.35%  | +0.28%  |
| FGSM (ε=0.0314)         | 52.76%  | 52.87%  | +0.11%  |
| PGD (ε=0.0078)          | 74.76%  | 74.91%  | +0.15%  |
| PGD (ε=0.0314)          | 45.01%  | 45.21%  | +0.20%  |

### ResNet Clean

| Saldırı                 | Normal  | TTA     | Fark    |
|-------------------------|---------|---------|---------|
| Temiz                   | 94.47%  | 95.05%  | +0.58%  |
| FGSM (ε=0.0078)         | 45.06%  | 46.37%  | +1.31%  |
| FGSM (ε=0.0314)         | 30.59%  | 30.99%  | +0.40%  |
| PGD (ε=0.0078)          | 9.80%   | 10.32%  | +0.52%  |
| PGD (ε=0.0314)          | 0.02%   | 0.00%   | -0.02%  |

### ViT Adv

| Saldırı                 | Normal  | TTA     | Fark    |
|-------------------------|---------|---------|---------|
| Temiz                   | 64.05%  | 64.07%  | +0.02%  |
| FGSM (ε=0.0078)         | 55.72%  | 55.68%  | -0.04%  |
| FGSM (ε=0.0314)         | 31.15%  | 31.24%  | +0.09%  |
| PGD (ε=0.0078)          | 55.66%  | 55.66%  | +0.00%  |
| PGD (ε=0.0314)          | 28.44%  | 28.37%  | -0.07%  |

### ViT Clean

| Saldırı                 | Normal  | TTA     | Fark    |
|-------------------------|---------|---------|---------|
| Temiz                   | 78.69%  | 78.62%  | -0.07%  |
| FGSM (ε=0.0078)         | 7.17%   | 7.15%   | -0.02%  |
| FGSM (ε=0.0314)         | 2.14%   | 2.15%   | +0.01%  |
| PGD (ε=0.0078)          | 1.47%   | 1.61%   | +0.14%  |
| PGD (ε=0.0314)          | 0.00%   | 0.00%   | +0.00%  |

---

## 7. Sonuç

Bu çalışma, **ResNet** ve **ViT** mimarilerinin adversarial saldırılara karşı dayanıklılıklarını ve farklı savunma stratejilerinin etkinliğini değerlendirdi.

- **Adversarial eğitim**, modelin dayanıklılığını önemli ölçüde artırmakta.
- **TTA (Test Time Augmentation)** ise küçük de olsa ek bir savunma katmanı sağlayarak bazı saldırı türlerinde doğruluğu arttırmaktadır.
- **En güçlü savunma**, adversarial eğitim ve TTA kombinasyonu ile elde edilmektedir.


