# Çürütme kod değişikliği regresyon özeti (08.11.2026)

Bu dosya `scripts/curutme_regresyon.py` ile üretilmiş kayıp dosyalarından (`regresyon_<ad>.txt`, her satır bir `Tensor.backward()` çağrısındaki skaler kayıp, ilk 50 çağrı) hesaplanmıştır. Eski kod `/mnt/d/adeb_sci_1_veri/_regresyon_eski_kod` altına `git archive` ile çürütme konseyi commit'inden (ca2d102, `KAYNAK_COMMIT.txt`) çıkarılmış ağaçtır; bu commit ile bugünkü HEAD (e5c3374) arasında `cli/` ve `src/` altında fark yoktur (`git diff --stat ca2d102 HEAD -- cli src` boş). Yeni kod çalışma ağacıdır. Üç durum sınanmıştır: `clean_vit` (C1 V-scr temiz komutu), `clean_vin` (B3 V-IN temiz komutu, ImageNet başlatma yolu dahil) ve `at_r224scr` (B3 R224-scr AT komutu, `--stop-epoch 1`). Belirlenimli kip `CUBLAS_WORKSPACE_CONFIG=:4096:8`, `torch.use_deterministic_algorithms(True, warn_only=True)` ve flash ile mem-efficient SDPA'nın kapatılmasıdır; ayar sarmalayıcıdadır, sınanan koda dokunulmaz.

Sonuç: belirlenimli GPU kipinde ve CPU'da eski ve yeni kod 50 iterasyonun 50'sinde bayt düzeyinde aynı kaybı verir; belirlenimsiz GPU kipindeki küçük farklar aynı kodun iki koşusu arasında da aynı büyüklükte görülür, yani GPU belirlenimsizliğinden gelir ve kod değişikliğinden gelmez. Kayıp ölçütü ya da artırma sırası değişmemiştir.

`yeni3` koşuları `src/training/trainer.py`'deki tek sayılı batch düzeltmesinden sonra, `yeni4` koşusu `src/models/r224.py`'deki `custom_load=False` düzeltmesinden sonra (ImageNet başlatma yolu) son kodla yapılmıştır.


## Belirlenimli GPU kipi (--belirlenimli), eski kod ile yeni kod

| Dosya A | Dosya B | Aynı / toplam | İlk farklı indis | En büyük mutlak fark | İlk kayıp A | İlk kayıp B | Son kayıp A | Son kayıp B |
|---|---|---|---|---|---|---|---|---|
| regresyon_det_clean_vit_eski.txt | regresyon_det_clean_vit_yeni.txt | 50/50 |  | 0 | 2.353499412536621 | 2.353499412536621 | 2.3049395084381104 | 2.3049395084381104 |
| regresyon_det_clean_vit_eski.txt | regresyon_det_clean_vit_yeni3.txt | 50/50 |  | 0 | 2.353499412536621 | 2.353499412536621 | 2.3049395084381104 | 2.3049395084381104 |
| regresyon_det_clean_vin_eski.txt | regresyon_det_clean_vin_yeni.txt | 50/50 |  | 0 | 2.482851505279541 | 2.482851505279541 | 0.2460404485464096 | 0.2460404485464096 |
| regresyon_det_clean_vin_eski.txt | regresyon_det_clean_vin_yeni3.txt | 50/50 |  | 0 | 2.482851505279541 | 2.482851505279541 | 0.2460404485464096 | 0.2460404485464096 |
| regresyon_det_clean_vin_eski.txt | regresyon_det_clean_vin_yeni4.txt | 50/50 |  | 0 | 2.482851505279541 | 2.482851505279541 | 0.2460404485464096 | 0.2460404485464096 |
| regresyon_det_at_r224scr_eski.txt | regresyon_det_at_r224scr_yeni.txt | 50/50 |  | 0 | 16.03301239013672 | 16.03301239013672 | 1.826277494430542 | 1.826277494430542 |
| regresyon_det_at_r224scr_eski.txt | regresyon_det_at_r224scr_yeni3.txt | 50/50 |  | 0 | 16.03301239013672 | 16.03301239013672 | 1.826277494430542 | 1.826277494430542 |

## CPU (--cihaz cpu), eski kod ile yeni kod

| Dosya A | Dosya B | Aynı / toplam | İlk farklı indis | En büyük mutlak fark | İlk kayıp A | İlk kayıp B | Son kayıp A | Son kayıp B |
|---|---|---|---|---|---|---|---|---|
| regresyon_cpu_clean_vit_eski.txt | regresyon_cpu_clean_vit_yeni.txt | 50/50 |  | 0 | 2.3534493446350098 | 2.3534493446350098 | 2.304934501647949 | 2.304934501647949 |

## Belirlenimsiz GPU kipi, aynı eski kodun iki koşusu (belirlenimsizlik tabanı)

| Dosya A | Dosya B | Aynı / toplam | İlk farklı indis | En büyük mutlak fark | İlk kayıp A | İlk kayıp B | Son kayıp A | Son kayıp B |
|---|---|---|---|---|---|---|---|---|
| regresyon_clean_vit_eski.txt | regresyon_clean_vit_eski2.txt | 3/50 | 1 | 1.69277e-05 | 2.3534815311431885 | 2.3534815311431885 | 2.304945707321167 | 2.304943084716797 |
| regresyon_clean_vin_eski.txt | regresyon_clean_vin_eski2.txt | 1/50 | 1 | 0.00780573 | 2.482832431793213 | 2.482832431793213 | 0.2574419677257538 | 0.2554324269294739 |
| regresyon_at_r224scr_eski.txt | regresyon_at_r224scr_eski2.txt | 16/50 | 16 | 0.00274873 | 16.015642166137695 | 16.015642166137695 | 1.8306927680969238 | 1.828841209411621 |

## Belirlenimsiz GPU kipi, aynı yeni kodun iki koşusu

| Dosya A | Dosya B | Aynı / toplam | İlk farklı indis | En büyük mutlak fark | İlk kayıp A | İlk kayıp B | Son kayıp A | Son kayıp B |
|---|---|---|---|---|---|---|---|---|
| regresyon_clean_vit_yeni.txt | regresyon_clean_vit_yeni2.txt | 3/50 | 1 | 1.28746e-05 | 2.3534815311431885 | 2.3534815311431885 | 2.304943323135376 | 2.3049368858337402 |
| regresyon_clean_vin_yeni.txt | regresyon_clean_vin_yeni2.txt | 1/50 | 1 | 0.019976 | 2.482832431793213 | 2.482832431793213 | 0.25216200947761536 | 0.25585275888442993 |
| regresyon_at_r224scr_yeni.txt | regresyon_at_r224scr_yeni2.txt | 16/50 | 16 | 0.00242114 | 16.015642166137695 | 16.015642166137695 | 1.830359935760498 | 1.828841209411621 |

## Belirlenimsiz GPU kipi, eski kod ile yeni kod (önceki yürütücünün koşuları ve bu oturumun eski2 koşusu)

| Dosya A | Dosya B | Aynı / toplam | İlk farklı indis | En büyük mutlak fark | İlk kayıp A | İlk kayıp B | Son kayıp A | Son kayıp B |
|---|---|---|---|---|---|---|---|---|
| regresyon_clean_vit_eski.txt | regresyon_clean_vit_yeni2.txt | 1/50 | 1 | 1.57356e-05 | 2.3534815311431885 | 2.3534815311431885 | 2.304945707321167 | 2.3049368858337402 |
| regresyon_clean_vin_eski.txt | regresyon_clean_vin_yeni2.txt | 1/50 | 1 | 0.0111813 | 2.482832431793213 | 2.482832431793213 | 0.2574419677257538 | 0.25585275888442993 |
| regresyon_at_r224scr_eski.txt | regresyon_at_r224scr_yeni2.txt | 16/50 | 16 | 0.00274873 | 16.015642166137695 | 16.015642166137695 | 1.8306927680969238 | 1.828841209411621 |
| regresyon_at_r224scr_eski2.txt | regresyon_at_r224scr_yeni2.txt | 50/50 |  | 0 | 16.015642166137695 | 16.015642166137695 | 1.828841209411621 | 1.828841209411621 |

Not: `det_*` dosyalarının ikinci başlık satırı `belirlenimli=True` alanını taşır. R224-scr AT durumunda belirlenimsiz `eski2` ve `yeni2` koşuları rastlantısal olarak bayt düzeyinde aynı çıkmıştır; aynı durumun `eski` ve `yeni` koşuları ise 16. çağrıdan sonra ayrışır, yani bu eşitlik belirlenimlilik kanıtı sayılmaz. Belirlenimsiz kipte ilk iterasyon kaybı eski ve yeni kodda aynıdır (2.3534815311431885, `regresyon_clean_vit_eski.txt` ve `regresyon_clean_vit_yeni2.txt` satır 3); CPU'da ilk kayıp 2.3534493446350098'dir (`regresyon_cpu_clean_vit_eski.txt` satır 3), fark CPU ve GPU çekirdeklerinin sayısal farkıdır.
