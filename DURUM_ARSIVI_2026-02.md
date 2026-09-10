# Durum arşivi (CLAUDE.md'den 2026-09-10'da taşındı; Şubat 2026 tabloları, tarihsel)

Geçerli sayılar: `results/C1_REFERANS_FOYU.md`

## Mevcut Durum (2026-02-17 - GUNCELLENDI)

### Strateji: Analiz Odaklı Yaklasım
**Robustness yarışı degil, davranış analizi**

> "Neden farklı davranıyorlar?" sorusuna cevap arıyoruz.

### Hedef Dergi: IEEE Access (Q2, IF ~3.4)

### Tamamlanan Analizler — C1 SONRASI (gecerli)

_Tek kaynak: `results/C1_REFERANS_FOYU.md` (uretici: `scripts/build_reference_sheet.py`)._
_Asagidaki degerler 3 tohum ortalamasi +/- SS, tam test kumesi (n=10.000), eps=8/255._

| Analiz | Sonuc (C1 sonrasi) | Artefakt |
|--------|--------------------|----------|
| Transfer (ham) | CNN->ViT 41,02+/-0,55 · ViT->CNN 27,45+/-0,27 · fark +13,57+/-0,33 | `results/c1_transfer/c1_transfer_summary.json` |
| Transfer (her ikisi dogru) | fark +8,27+/-0,23 · bootstrap GA [7,33; 9,22] · isaret-cevirme p ~ 0 | ayni |
| Protokol yayilimi | 15,01+/-0,84 puan (en buyuk/en kucuk tahmin orani ~4,4 kat) | ayni |
| Basarili kaynak (B2 sonrasi) | fark +19,37+/-1,27 · maske: hedef-dogru VE kaynak-temizde-dogru VE kaynak-adv-yanlis | `src/analysis/protokoller.py` |
| Kosullu ayrisma | bkz. C1_REFERANS_FOYU Tablo II | `results/c1_seeds/c1_seed_summary.json` |
| AutoAttack | bkz. asagidaki tablo | `results/c1_eval_summary.json` |

> **KARANTINA — asagidaki run2 kaydi yalniz tarihsel amaclidir, KULLANILMAZ:**
> Transfer CNN->ViT %41,2 / ViT->CNN %36,1 (5,1 puan asimetri) · AutoAttack
> ResNet %36,0 / ViT %32,4 · gradyan CNN 1,7x seyrek · oznitelik bozunmasi
> kosinus 0,995->0,958. Bu satirlarin hicbiri C1 duzeltmesinden gecmemistir.

### Model Performanslari — C1 SONRASI (gecerli)

_Tek kaynak: `results/C1_REFERANS_FOYU.md` Tablo I. 3 tohum ortalamasi +/- SS._

| Model | AT | Temiz | FGSM | PGD-10 | AutoAttack |
|-------|----|-------|------|--------|------------|
| ResNet-18 | -- | 95,25+/-0,15 | 40,29+/-1,77 | 0,03+/-0,03 | -- |
| ViT-Tiny | -- | 80,09+/-0,60 | 6,10+/-1,47 | 0,05+/-0,05 | -- |
| **ResNet-18** | **+** | **85,78+/-0,36** | **53,46+/-0,08** | **44,11+/-0,50** | **37,93+/-0,14** |
| **ViT-Tiny** | **+** | **73,53+/-0,55** | **36,31+/-0,42** | **32,69+/-0,22** | **29,14+/-0,40** |
| WRN-28-10 (harici) | + | 89,48 | 70,91 | 66,92 | 62,76 (RobustBench) |

> **KARANTINA — run1/run2 kaydi (KULLANILMAZ):** ResNet18 AT run2 81,80 / 40,97 / 36,0;
> run1 80,34 / 40,25 / 34,6. ViT-Tiny AT run2 73,60 / 36,87 / 32,4; run1 63,42 / 32,77 / 28,0.
> C1 duzeltmesi bu degerleri ANLAMLI olcude degistirmistir (ornek: ViT PGD 36,87 -> 32,69).

### Model Dosyaları
```
models/
├── robustbench/
│   └── wideresnet28_10_robust.pth  # 89.48% clean, 62.76% AA
├── resnet18/
│   ├── clean/best.pth              # 94.37%
│   ├── adv/adversarial_training/best.pth  # run1: 40.25% PGD, 34.6% AA
│   └── adv/at_run2/.../best.pth    # KARANTINA: run2 sayilari kullanilmaz
├── vit_tiny/
│   ├── clean/best.pth              # 77.50%
│   ├── adv/adversarial_training/best.pth  # run1: 32.77% PGD, 28.0% AA
│   └── adv/at_run2/.../best.pth    # KARANTINA: run2 sayilari kullanilmaz
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

