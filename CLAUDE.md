# CLAUDE.md - Adversarial Defense Study

> ## KARANTINA KURALI (2026-08-18) — ONCE BUNU OKU
>
> **Bu projeden disariya (makale, tez, sunum, bildiri) cikan HER SAYI
> `results/C1_REFERANS_FOYU.md` dosyasindan alinir.** O dosya
> `scripts/build_reference_sheet.py` ile otomatik uretilir ve C1 sizinti
> duzeltmesi SONRASI yeniden uretilmis sayilari tasir.
>
> **run1 ve run2 sayilari KARANTINADADIR.** Tarihsel kayit olarak
> saklanmaktadir; hicbir tabloya, sekile veya iddiaya kaynaklik edemez.
> C1 duzeltmesi sonuclari yalnizca ondalik basamakta degil, ANLATI
> duzeyinde degistirmistir — ornegin transfer asimetrisi run2 kaydinda
> 5,1 puan, C1 sonrasi ham protokolde 13,57 puan, her-ikisi-dogru
> protokolunde 8,27 puandir. Eski bir sayinin metne sizmasi, yanlis bir
> ondalik degil yanlis bir SONUC uretir.
>
> Bu kural Firat Universitesi doktora tezi ile ortak yurutulmektedir
> (tez Bolum 5.1.1). Tez tarafindaki karsiligi: `ACIK_ISLER.md` I3/I4.

Bu dosya, Claude Code'un bu proje ile etkili calışabilmesi icin gerekli baglamı saglar.

---

## Gelistirme Ortamı

**Container:** `adeb_eval` (repo `/workspace`'e mount'lu)
- Windows/WSL'den calisiliyor: `docker exec -w /workspace adeb_eval ...`
- Uzun kosumlar: `docker exec -d ...` (arka plan)
- SSH ile evden baglanıldıgında: `claude --continue`

**Donanım (2026-08 itibariyle GUNCEL):**
- GPU: **RTX 5090 (32GB VRAM)** — eski kayit RTX 5060 Ti 16GB idi; run1/run2
  ve C1 kampanyalari 5060 Ti'de, Q1 kampanyasi (E0-E7) 5090'da kosuldu.
  Makalenin "Computational Details" bolumu bu ayrimi yazmali.
- Framework: PyTorch 2.6.0a0+nv25.01, CUDA 12.8, timm 1.0.27

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

### Tamamlanan Analizler — C1 SONRASI (gecerli)

_Tek kaynak: `results/C1_REFERANS_FOYU.md` (uretici: `scripts/build_reference_sheet.py`)._
_Asagidaki degerler 3 tohum ortalamasi +/- SS, tam test kumesi (n=10.000), eps=8/255._

| Analiz | Sonuc (C1 sonrasi) | Artefakt |
|--------|--------------------|----------|
| Transfer (ham) | CNN->ViT 41,02+/-0,55 · ViT->CNN 27,45+/-0,27 · fark +13,57+/-0,33 | `results/c1_transfer/c1_transfer_summary.json` |
| Transfer (her ikisi dogru) | fark +8,27+/-0,23 · bootstrap GA [7,33; 9,21] · isaret-cevirme p ~ 0 | ayni |
| Protokol yayilimi | 10,45+/-0,76 puan (en buyuk/en kucuk tahmin orani ~3,3x) | ayni |
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

# Model degerlendirme (NOT: click multiple flag'leri tekrarlanmali:
# "-a fgsm -a pgd -e 0.0078 -e 0.0157" — bosluklu liste PARSE EDILMEZ)
python -m cli.main evaluate robustness \
    -m models/resnet18/adv/at_run2/resnet18/adv/adversarial_training/best.pth \
    -t resnet18 \
    -a fgsm -a pgd \
    -e 0.00784313725490196 -e 0.01568627450980392 -e 0.03137254901960784

# AutoAttack evaluation (seedli, ornek-bazli loglu; default n=10000)
python experiments/run_autoattack_run2.py --n-samples 10000 --seed 42

# SCI analizleri (dogru bayrak: --experiment, --analysis DEGIL)
python experiments/run_sci_analysis.py --experiment gradient
python experiments/run_sci_analysis.py --experiment transfer
python experiments/run_sci_analysis.py --experiment attention

# Run3 analizleri (kosullu transfer metrigi, tam seed, --only secimi)
python experiments/run_all_analyses_run2.py --only transfer --n-samples 10000 --seed 42
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
