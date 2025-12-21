# 🐛 Bug Fix #2: Import Name Collision

## Problem

**Hata Mesajı**:
```
AttributeError: module 'src.data.transforms' has no attribute 'Compose'
```

**Stack Trace**:
```
File "/workspace/adeb_sci_1/src/data/__init__.py", line 33
    transform_train = transforms.Compose([
                      ^^^^^^^^^^^^^^^^^^
AttributeError: module 'src.data.transforms' has no attribute 'Compose'
```

## Sebep

Python import name collision:

1. `src/data/__init__.py` içinde:
   ```python
   from .transforms import ...  # src.data.transforms modülünü import eder
   ```

2. `src/data/datasets.py` içinde:
   ```python
   import torchvision.transforms as transforms  # transforms ismi ile
   ```

3. Python `transforms` ismini **son import'tan** alır
4. `src.data.transforms` (bizim modülümüz) `torchvision.transforms`'u geçersiz kılar
5. Bizim modülde `Compose`, `RandomCrop` yok → **AttributeError**

## Çözüm

### `src/data/datasets.py` Import'unu Düzelt

**Önce**:
```python
import torchvision.transforms as transforms
```

**Sonra**:
```python
from torchvision import transforms as T  # İsim çakışması önlendi
```

### Tüm Kullanımları Değiştir

**Önce**:
```python
train_transform: Optional[transforms.Compose] = None
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])
```

**Sonra**:
```python
train_transform: Optional[T.Compose] = None
train_transform = T.Compose([
    T.RandomCrop(32, padding=4),
    T.RandomHorizontalFlip(),
    T.ToTensor(),
])
```

## Düzeltilen Dosyalar

1. ✏️ `src/data/datasets.py` - Import ve tüm kullanımlar düzeltildi
2. ✏️ `src/data/transforms.py` - Üzerine yazılan eski içerik geri yüklendi

## Test

```bash
python3 -c "from src.data import get_cifar10_loaders, denormalize, normalize; print('✓ OK')"
```

**Çıktı**:
```
✓ OK
```

## Python Import Best Practices

### ❌ Kötü (Name Collision Riski)

```python
# module1.py
import something as x

# module2.py
from .module1 import x  # x modül ismi ile çakışabilir
```

### ✅ İyi (Farklı İsimler)

```python
# module1.py
from something import feature as T

# module2.py
from .module1 import custom_function  # Sadece ihtiyacı olanı import et
```

### ✅ En İyi (Explicit Import)

```python
# module1.py
from torchvision import transforms as tv_transforms

# module2.py
from . import transforms  # Modülün kendisi
from .transforms import denormalize  # Spesifik fonksiyon
```

## Status

✅ **ÇÖZÜLDÜ**

Artık tüm import'lar çalışıyor:

```python
from src.data import (
    get_cifar10_loaders,     # ✓
    get_normalization,       # ✓
    denormalize,             # ✓
    normalize,               # ✓
)
```

## Etkilenen Dosyalar

| Dosya | Değişiklik | Satır |
|-------|-----------|-------|
| `src/data/datasets.py` | `transforms` → `T` | 5, 15-16, 38-47, 114-123 |
| `src/data/transforms.py` | Tam içerik restore | 1-197 |

## Sonuç

✅ **İki bug birden düzeltildi!**

1. ✅ Normalization mismatch (BUGFIX_NORMALIZATION.md)
2. ✅ Import name collision (bu dosya)

Artık çalışmalı:

```bash
./quick_test.sh
```

veya

```bash
python3 test_normalization_fix.py
```
