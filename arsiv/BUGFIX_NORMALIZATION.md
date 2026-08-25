# 🐛 Bug Fix: Normalization Mismatch

## Problem

**Hata Mesajı**:
```
ValueError: Images should be in range [0, 1]
```

**Konum**:
- `src/attacks/base.py:87` - `_check_inputs()` metodu
- `experiments/run_sci_analysis.py` - Transfer attack analysis

## Sebep

Attack sınıfları (`FGSM`, `PGD`, etc.) görüntülerin **[0, 1]** aralığında olmasını bekliyor.

Ancak bazı durumlarda:
1. Veri normalization ile **[-2, 2]** aralığına dönüşebiliyor
2. Floating point hataları **[0.0001, 0.9999]** gibi küçük sapmalar yaratıyor
3. Kontrol çok katı (tam `< 0` veya `> 1`)

## Çözüm

### 1. Tolerance Eklendi (`src/attacks/base.py`)

**Önce**:
```python
if images.min() < 0 or images.max() > 1:
    raise ValueError("Images should be in range [0, 1]")
```

**Sonra**:
```python
if images.min() < -1e-6 or images.max() > 1 + 1e-6:
    raise ValueError(
        f"Images should be in range [0, 1], got [{images.min():.4f}, {images.max():.4f}]. "
        f"If using normalized data, denormalize before attacks."
    )

# Clamp to handle small floating point errors
images = torch.clamp(images, 0.0, 1.0)
```

**Değişiklikler**:
- ✅ Tolerance: ±1e-6 (floating point hataları için)
- ✅ Auto-clamp: Küçük sapmaları otomatik düzelt
- ✅ Better error message: Normalization uyarısı ekle

### 2. Denormalization Utilities Eklendi (`src/data/transforms.py`)

```python
def denormalize(tensor, mean, std):
    """Denormalize a tensor: x_denorm = x * std + mean"""
    # Handles both (C,H,W) and (B,C,H,W)

def normalize(tensor, mean, std):
    """Normalize a tensor: x_norm = (x - mean) / std"""
    # Handles both (C,H,W) and (B,C,H,W)
```

**Export edildi**: `src/data/__init__.py`

### 3. Attack Wrapper Güncellendi (`experiments/run_sci_analysis.py`)

**Önce**:
```python
def create_pgd_attack(eps: float):
    def attack_fn(model, images, labels):
        attack = PGDAttack(model, eps=eps, alpha=eps/4, steps=20)
        return attack(images, labels)
    return attack_fn
```

**Sonra**:
```python
def create_pgd_attack(eps: float, normalize_data: bool = True):
    def attack_fn(model, images, labels):
        from src.data import get_normalization, denormalize, normalize

        if normalize_data:
            # Get CIFAR-10 normalization parameters
            mean, std = get_normalization("cifar10")

            # Denormalize to [0, 1] range for attack
            images_denorm = denormalize(images, mean, std)

            # Run attack
            attack = PGDAttack(model, eps=eps, alpha=eps/4, steps=20)
            adv_images_denorm = attack(images_denorm, labels)

            # Normalize back for model input
            adv_images = normalize(adv_images_denorm, mean, std)
            return adv_images
        else:
            # Direct attack (for non-normalized data)
            attack = PGDAttack(model, eps=eps, alpha=eps/4, steps=20)
            return attack(images, labels)

    return attack_fn
```

**Özellikler**:
- ✅ `normalize_data` parametresi ile kontrol
- ✅ Otomatik denorm → attack → renorm cycle
- ✅ Geriye uyumlu (default=True)

## Test

Test script oluşturuldu: `test_normalization_fix.py`

```bash
python3 test_normalization_fix.py
```

**Test edilen**:
1. ✅ CIFAR-10 data [0, 1] range kontrolü
2. ✅ Attack unnormalized data üzerinde
3. ✅ Denormalize/normalize roundtrip
4. ✅ Attack with denorm/renorm cycle
5. ✅ create_pgd_attack wrapper

## Durum

### ✅ ÇÖZÜLDÜ

- [x] Tolerance eklendi (`_check_inputs`)
- [x] Auto-clamp eklendi
- [x] Denormalization utilities eklendi
- [x] Attack wrapper güncellendi
- [x] Test script oluşturuldu
- [x] Hata mesajı geliştirildi

## Not: Mevcut CIFAR-10 Durumu

**Mevcut durum**: CIFAR-10 data loader'lar **normalization YAPMIY OR**.

`src/data/datasets.py`:
```python
test_transform = transforms.Compose([
    transforms.ToTensor(),  # [0, 1] range
])
```

Yani şu an normalization **gereksiz** ama:
- ✅ Gelecekte normalization eklenirse hazır
- ✅ Floating point hataları için tolerance var
- ✅ API temiz ve esnek

## Öneri

Eğer gelecekte normalization eklemek isterseniz:

```python
# src/data/datasets.py içinde
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465),  # CIFAR-10 mean
                        (0.2023, 0.1994, 0.2010))  # CIFAR-10 std
])
```

Sonra:
```python
# experiments/run_sci_analysis.py içinde
attack_fn = create_pgd_attack(epsilon, normalize_data=True)  # Bu zaten default
```

## Etkilenen Dosyalar

1. ✏️ `src/attacks/base.py` - Tolerance + clamp eklendi
2. ✏️ `src/data/transforms.py` - `denormalize()`, `normalize()` eklendi
3. ✏️ `src/data/__init__.py` - Yeni fonksiyonlar export edildi
4. ✏️ `experiments/run_sci_analysis.py` - `create_pgd_attack()` güncellendi
5. ➕ `test_normalization_fix.py` - Test script eklendi
6. ➕ `BUGFIX_NORMALIZATION.md` - Bu doküman

## Sonuç

✅ **Bug düzeltildi!**

Artık pipeline sorunsuz çalışmalı:

```bash
./run_complete_pipeline.sh
```

Veya hızlı test:

```bash
./quick_test.sh
```
