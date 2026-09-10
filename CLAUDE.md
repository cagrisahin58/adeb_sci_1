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

## Durum ve sayılar

Sayı tabloları bu dosyada tutulmaz: geçerli tek kaynak `results/C1_REFERANS_FOYU.md`. Karantina: **C1 öncesi tüm koşular** (run1, run2, run3, `attention_analysis_run3`, `stat_addendum`, `rev2_blockA`); geçerli yollar yalnız `results/c1_*` ve `results/q1/*` (08.09.2026 netleştirmesi, tez CLAUDE.md ile aynı). Şubat 2026 durum tabloları ve faz listesi `DURUM_ARSIVI_2026-02.md` içinde (tarihsel). Güncel durum: son HANDOFF/plan dosyası ve `git log`. Ajan/skill kataloğu: `~/.claude/KATALOG.md`.

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

## Referanslar

- [TRADES](https://arxiv.org/abs/1901.08573)
- [AutoAttack](https://arxiv.org/abs/2003.01690)
- [RobustBench](https://robustbench.github.io/)
