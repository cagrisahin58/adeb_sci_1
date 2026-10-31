# C1 Referans Foyu - dergi metni icin tum sayilar

Her sayi 3 tohum ortalamasi $\pm$ standart sapma (aksi belirtilmedikce), tam test kumesi (n=10.000), $\eps=8/255$.

> Bu dosya otomatik uretilir: `python scripts/build_reference_sheet.py`. Metne sayi tasirken buradan al; artefakt yollari her bolumun altinda.


## Tablo I: ana gurbuzluk

_Kaynak: `results/c1_eval_summary.json + c1_seeds/c1_seed_summary.json`_

| Model | AT | Temiz | FGSM | PGD-10 | AA |
|---|---|---|---|---|---|
| ResNet-18 | -- | 95.25$\pm$0.15 | 40.29$\pm$1.77 | 0.03$\pm$0.03 | -- |
| ViT-Tiny | -- | 80.09$\pm$0.60 | 6.10$\pm$1.47 | 0.05$\pm$0.05 | -- |
| ResNet-18 | + | 85.78$\pm$0.36 | 53.46$\pm$0.08 | 44.11$\pm$0.50 | 37.93$\pm$0.14 |
| ViT-Tiny | + | 73.53$\pm$0.55 | 36.31$\pm$0.42 | 32.69$\pm$0.22 | 29.14$\pm$0.40 |

WRN-28-10 (harici referans): temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 (AA degeri RobustBench raporu).


## Tablo II: kosullu ayrisma

_Kaynak: `results/c1_seeds/c1_seed_summary.json`_

| Model | Kos. yaniltma PGD | Kos. yaniltma AA | Her ikisi dogru PGD | Her ikisi dogru AA |
|---|---|---|---|---|
| ResNet-18 AT | 48.58$\pm$0.80 | 55.78$\pm$0.23 | 59.86$\pm$0.35 | 51.89$\pm$0.49 |
| ViT-Tiny AT | 55.53$\pm$0.50 | 60.37$\pm$0.33 | 46.11$\pm$0.59 | 41.15$\pm$0.39 |

Ortak kume n = 7061$\pm$68. Ayrisma ornegi (AA): 85.78 x 44.2% = 37.93 (CNN), 73.53 x 39.6% = 29.14 (ViT).

[ELLE TASINMIS LITERAL, karantinadaki eski kosudan, artefaktla DOGRULANMADI; bkz. 'Sabit dizgeler' bolumu] Eski tek kosu (sizintili) karsilastirmasi: kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33 (n=7260).


HER-IKISI-DOGRU altkumesinde McNemar (tam binom, ornek bazindan):
- cift 1: n_ortak=7126, PGD p=5.07e-124, AA p=5.90e-68
- cift 2: n_ortak=7067, PGD p=6.89e-113, AA p=1.43e-77
- cift 3: n_ortak=6991, PGD p=1.75e-92, AA p=1.11e-73
  -> metne girecek ORTAK sinir: p < 1e-67  (TAM KUME sinirindan ZAYIFTIR, onunla karistirilmamalidir)

McNemar (kosu bazinda, tam binom): 
- cift 1: PGD p=1.2e-153 (1677/483), AA p=1.2e-84 (1362/528)
- cift 2: PGD p=1.3e-140 (1658/511), AA p=1.1e-96 (1397/504)
- cift 3: PGD p=1.9e-120 (1665/581), AA p=3.2e-93 (1478/567)

## Tablo III: transfer protokolleri

_Kaynak: `results/c1_transfer/c1_transfer_summary.json`_

| Protokol | CNN->ViT | ViT->CNN | Fark | N (CNN->ViT / ViT->CNN) | run3 fark |
|---|---|---|---|---|---|
| Kosulsuz (ham) | 41.02$\pm$0.55 | 27.45$\pm$0.27 | +13.57$\pm$0.33 | 10000 / 10000 | 8.27 |
| Hedef dogru | 19.87$\pm$0.18 | 15.51$\pm$0.59 | +4.36$\pm$0.44 | 7353 / 8579 | 0.63 |
| Her ikisi dogru | 18.25$\pm$0.17 | 9.98$\pm$0.31 | +8.27$\pm$0.23 | 7061 / 7061 | 5.33 |
| Basarili kaynak | 36.39$\pm$0.76 | 17.02$\pm$0.52 | +19.37$\pm$1.27 | 2831 / 3814 | 11.17 |

Eslesmis analiz: fark 8.27$\pm$0.24 puan, bootstrap GA [7.33; 9.22], isaret-cevirme permutasyon p (en buyuk) = 0.0, TOST esdegerligi hicbir marjda saglanmiyor.

Protokol yayilimi: 15.01$\pm$0.84 puan (en buyuk/en kucuk protokol tahmini orani ~4.4 kat).


## C3: WRN dahil 3x3 matris

_Kaynak: `results/c1_c3/c3_summary.json`_

| kaynak -> hedef | ham | kosullu | ham - kosullu |
|---|---|---|---|
| ResNet18_AT -> ResNet18_AT | 55.84$\pm$0.53 | 48.52$\pm$0.84 | +7.32 |
| ResNet18_AT -> ViT_Tiny_AT | 41.07$\pm$0.58 | 19.93$\pm$0.20 | +21.14 |
| ResNet18_AT -> WRN_28_10 | 21.69$\pm$0.09 | 12.48$\pm$0.10 | +9.21 |
| ViT_Tiny_AT -> ResNet18_AT | 27.45$\pm$0.34 | 15.52$\pm$0.64 | +11.93 |
| ViT_Tiny_AT -> ViT_Tiny_AT | 67.34$\pm$0.18 | 55.57$\pm$0.44 | +11.76 |
| ViT_Tiny_AT -> WRN_28_10 | 18.25$\pm$0.12 | 8.65$\pm$0.14 | +9.60 |
| WRN_28_10 -> ResNet18_AT | 32.63$\pm$0.14 | 21.48$\pm$0.31 | +11.16 |
| WRN_28_10 -> ViT_Tiny_AT | 39.73$\pm$0.25 | 18.15$\pm$0.28 | +21.58 |
| WRN_28_10 -> WRN_28_10 | 33.03$\pm$0.00 | 25.16$\pm$0.00 | +7.87 |

(ham - kosullu) ile hedefin temiz hatasi: Pearson r = 0.997, egim 0.762 (6 kosegen disi yon).

Gelen transfer ile hedefin kendi kirilganligi: r = 0.986 (hedefler: ResNet18_AT, ViT_Tiny_AT, WRN_28_10; kendi kosullu yaniltma [48.52, 55.57, 25.16], gelen transfer [18.5, 19.04, 10.57]).


## Gradyan yapisi

_Kaynak: `results/c1_behavior_summary.json + results/c1_a3/pair*/`_

| Olcut | ResNet-18 AT | ViT-Tiny AT |
|---|---|---|
| Hoyer | 0.4928$\pm$0.0120 | 0.4561$\pm$0.0055 |
| Gini | 0.6498$\pm$0.0089 | 0.6099$\pm$0.0051 |
| Rel-esik (%1 alti) | 0.3477$\pm$0.0210 | 0.2682$\pm$0.0090 |
| Hizalanma (mutlak kosinus) | 0.0378$\pm$0.0009 | 0.0562$\pm$0.0004 |

- hoyer: Cohen d 0.32-0.77, Holm p max 2.2e-12

- gini: Cohen d 0.65-1.23, Holm p max 2.6e-34

- rel: Cohen d 0.44-0.86, Holm p max 3.2e-21
- isaretli ortalama kosinus (mutlak deger) en buyuk: 0.0014
- ResNet temiz: Hoyer 0.3467$\pm$0.0018, hizalanma 0.0293$\pm$0.0004
- ViT temiz: Hoyer 0.3804$\pm$0.0094, hizalanma 0.0581$\pm$0.0022

## C4: oznitelik kaymasi ve attention (n=1000)

_Kaynak: `results/c1_c45_summary.json`_

**MANSET: residual BLOK CIKISI (makale Tablo 10), uc kosum ortalamasi; blok numaralari 1-tabanli, SD kosumlar arasi**

- CLS (cos_block_cls): minimum blok 11, deger 0.9604$\pm$0.0029
- Yama ortalamasi (cos_block_token_mean): minimum blok 9, deger 0.9870$\pm$0.0014
- Tum jetonlar (cos_block_output): minimum blok 11, deger 0.9803$\pm$0.0017
- Oran (1 - cos) CLS minimumu / yama ortalamasi minimumu = 3.05 (ham ortalamalardan)

MLP alt-blok cikisi serisi (DUYARLILIK analizi; manset DEGIL; kaynak c1_c45_summary.json vit_drift_minima, blok 1-tabanli):
- cos_cls (MLP alt-blok): minimum blok 10, deger 0.9343
- cos_token_mean (MLP alt-blok): minimum blok 8, deger 0.9840
- cos_flat_all_tokens (MLP alt-blok): minimum blok 8, deger 0.9663
- cos_block_output (blok cikisi, tum jetonlar): minimum blok 11, deger 0.9803
- ResNet: layer4.0 kosinus 0.8777$\pm$0.0181 (norm -13.14%), layer4.1 kosinus 0.9108$\pm$0.0060 (norm +5.84%)
- attention entropi degisimi: tum katmanlarda |delta| <= 0.0045
- CLS yer degistirmesi: 0.0276 (katman 1) -> 0.0841 (en derin)
- ViT son blok, devrilen 0.9895 vs devrilmeyen 0.9877

## C5: mekansal lokalite (n=500)

_Kaynak: `results/c1_c45_summary.json`_

| Olcut | ResNet | ViT | Fark (R-V) | Wilcoxon p (en buyuk) |
|---|---|---|---|---|
| Enerji %50 alani | 0.0378$\pm$0.0017 | 0.0397$\pm$0.0010 | -0.0019 | 2.63e-01 |
| Enerji %90 alani | 0.2345$\pm$0.0078 | 0.2570$\pm$0.0067 | -0.0224 | 3.85e-02 |
| Mekansal entropi | 5.2014$\pm$0.0387 | 5.2524$\pm$0.0197 | -0.0509 | 8.00e-01 |
| Moran's I | 0.4141$\pm$0.0132 | 0.3941$\pm$0.0024 | +0.0200 | 5.35e-01 |

**Negatif sonuc:** mekansal lokalite farki yok; makalede yalnizca 'daha seyrek' denebilir, 'daha lokalize/yogunlasmis' denemez.


## C2: TGR vs MI-FGSM (ViT -> CNN)

_Kaynak: `results/c1_c2/pair*/tgr_summary.json`_

| Olcut | TGR | MI-FGSM |
|---|---|---|
| Kaynakta beyaz kutu (ham) | 51.56$\pm$0.80 | 66.43$\pm$0.29 |
| Transfer, hedef dogru | 12.70$\pm$0.41 | 15.71$\pm$0.60 |
| Transfer, her ikisi dogru | 7.93$\pm$0.42 | 10.08$\pm$0.30 |

Eslesmis McNemar (her ikisi dogru): cift 1 p=6.07e-10, cift 2 p=1.11e-27, cift 3 p=7.02e-34

## Transfer asimetrisi, dort protokol, ayarlar

_Kaynak: `results/c1_transfer/c1_transfer_summary.json; results/q1/cifar100/transfer/e1_transfer_summary.json; results/q1/svhn/transfer/e7_transfer_summary.json; results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json`_

Hucre = CNN->ViT eksi ViT->CNN (yuzde puan). 3 kosumlu ayarlarda kosum ortalamasi$\pm$SD (ddof=1); SVHN'de yalniz IKI kosum vardir, SD YAZILMAZ, iki deger ayri ayri verilir (kosum 1 / kosum 2). Fark ve yayilim kosum basina tam hassasiyetle hesaplanir (artefaktta oranlar 2 ondalikli saklidir), yuvarlanmis ozetten degil. Yayilim = kosum basina (en buyuk - en kucuk protokol farki), sonra kosum ortalamasi$\pm$SD.

| Protokol | CIFAR-10 Linf | CIFAR-100 Linf | SVHN Linf | CIFAR-10 L2 |
|---|---|---|---|---|
| Unconditioned (raw) | +13.57$\pm$0.33 | +18.53$\pm$0.71 | +0.33 / +0.45 | +13.03$\pm$0.81 |
| Target-correct | +4.36$\pm$0.44 | +4.96$\pm$1.01 | -1.16 / -0.85 | +2.12$\pm$0.18 |
| Both-correct | +8.27$\pm$0.23 | +10.92$\pm$0.34 | -0.34 / -0.36 | +4.07$\pm$0.36 |
| Successful-source | +19.37$\pm$1.27 | +17.50$\pm$0.92 | +2.98 / +2.41 | +12.06$\pm$0.23 |
| Spread | 15.01$\pm$0.84 | 13.83$\pm$1.30 | 4.14 / 3.26 | 10.92$\pm$0.82 |
| n (test kumesi) | 10000 | 10000 | 26032 | 10000 |
| Cift (kosum) sayisi | 3 | 3 | 2 | 3 |
| Pozitif isaretli (kosum x protokol) | 12/12 | 12/12 | 4/8 | 12/12 |
- CIFAR-10 Linf: kaynak `results/c1_transfer/c1_transfer_summary.json`; kosumlar [1, 2, 3]; artefaktin kendi diff ve protocol_spread_pp alanlariyla UYUMLU (en buyuk sapma < 1e-6 puan)
- CIFAR-100 Linf: kaynak `results/q1/cifar100/transfer/e1_transfer_summary.json`; kosumlar [1, 2, 3]; artefaktin kendi diff ve protocol_spread_pp alanlariyla UYUMLU (en buyuk sapma < 1e-6 puan)
- SVHN Linf: kaynak `results/q1/svhn/transfer/e7_transfer_summary.json`; kosumlar [1, 2]; artefaktin kendi diff ve protocol_spread_pp alanlariyla UYUMLU (en buyuk sapma < 1e-6 puan)
- CIFAR-10 L2: kaynak `results/q1/cifar10_l2/transfer/e6_l2_transfer_summary.json`; kosumlar [1, 2, 3]; artefaktin kendi diff ve protocol_spread_pp alanlariyla UYUMLU (en buyuk sapma < 1e-6 puan)

### Yon bazinda oranlar (Tablo 6 ve 7 icin)

| Ayar | Protokol | CNN->ViT | ViT->CNN | Fark |
|---|---|---|---|---|
| CIFAR-10 Linf | Unconditioned (raw) | 41.02$\pm$0.55 | 27.45$\pm$0.27 | +13.57$\pm$0.33 |
| CIFAR-10 Linf | Target-correct | 19.87$\pm$0.18 | 15.51$\pm$0.59 | +4.36$\pm$0.44 |
| CIFAR-10 Linf | Both-correct | 18.25$\pm$0.17 | 9.98$\pm$0.31 | +8.27$\pm$0.23 |
| CIFAR-10 Linf | Successful-source | 36.39$\pm$0.76 | 17.02$\pm$0.52 | +19.37$\pm$1.27 |
| CIFAR-100 Linf | Unconditioned (raw) | 67.64$\pm$0.85 | 49.10$\pm$0.41 | +18.53$\pm$0.71 |
| CIFAR-100 Linf | Target-correct | 25.67$\pm$0.22 | 20.71$\pm$0.90 | +4.96$\pm$1.01 |
| CIFAR-100 Linf | Both-correct | 23.33$\pm$0.18 | 12.41$\pm$0.35 | +10.92$\pm$0.34 |
| CIFAR-100 Linf | Successful-source | 33.88$\pm$0.68 | 16.38$\pm$0.27 | +17.50$\pm$0.92 |
| SVHN Linf | Unconditioned (raw) | 31.21 / 32.56 | 30.88 / 32.11 | +0.33 / +0.45 |
| SVHN Linf | Target-correct | 25.90 / 26.75 | 27.06 / 27.60 | -1.16 / -0.85 |
| SVHN Linf | Both-correct | 25.07 / 25.64 | 25.41 / 26.00 | -0.34 / -0.36 |
| SVHN Linf | Successful-source | 60.86 / 61.90 | 57.88 / 59.49 | +2.98 / +2.41 |
| CIFAR-10 L2 | Unconditioned (raw) | 32.83$\pm$0.49 | 19.80$\pm$0.34 | +13.03$\pm$0.81 |
| CIFAR-10 L2 | Target-correct | 8.69$\pm$0.15 | 6.57$\pm$0.04 | +2.12$\pm$0.18 |
| CIFAR-10 L2 | Both-correct | 7.69$\pm$0.12 | 3.62$\pm$0.24 | +4.07$\pm$0.36 |
| CIFAR-10 L2 | Successful-source | 21.44$\pm$0.70 | 9.38$\pm$0.68 | +12.06$\pm$0.23 |

### Her ikisi dogru, eslesmis analiz (ayar basina)

| Ayar | n ortak | Fark (puan) | Bootstrap GA alt | Bootstrap GA ust | Isaret-cevirme perm. p (en buyuk) | TOST esdegerligi (herhangi marj) |
|---|---|---|---|---|---|---|
| CIFAR-10 Linf | 7061$\pm$68 | +8.27$\pm$0.24 | +7.33$\pm$0.26 | +9.22$\pm$0.22 | 0.0 | saglanmiyor |
| CIFAR-100 Linf | 3886$\pm$88 | +10.92$\pm$0.34 | +9.47$\pm$0.34 | +12.35$\pm$0.36 | 0.0 | saglanmiyor |
| SVHN Linf | 23870 / 23565 | -0.34 / -0.36 | -0.75 / -0.76 | +0.07 / +0.06 | 0.1047 | saglaniyor |
| CIFAR-10 L2 | 7061$\pm$68 | +4.07$\pm$0.36 | +3.39$\pm$0.35 | +4.76$\pm$0.36 | 0.0 | saglanmiyor |

## Turetilmis

_Kaynak: `yukaridaki ayar ozetlerinin kosum degerleri; results/c1_eval_summary.json; results/q1/e1_cifar100_summary.json; results/q1/e7_svhn_summary.json; results/*/pair*/a2_transfer_protocols.json`_

Hepsi kosum basina tam hassasiyetle hesaplanir; yuvarlanmis tablo degerlerinin farki DEGILDIR.

### Protokol farklarinin farki (puan)

| Fark | CIFAR-10 Linf | CIFAR-100 Linf | SVHN Linf | CIFAR-10 L2 |
|---|---|---|---|---|
| raw - tc (Unconditioned eksi Target-correct) | +9.21$\pm$0.76 | +13.58$\pm$1.71 | +1.49 / +1.30 | +10.91$\pm$0.83 |
| ss - raw (Successful-source eksi Unconditioned) | +5.79$\pm$1.60 | -1.03$\pm$1.61 | +2.65 / +1.96 | -0.97$\pm$0.90 |
| bc - tc (Both-correct eksi Target-correct) | +3.91$\pm$0.32 | +5.97$\pm$0.98 | +0.82 / +0.49 | +1.95$\pm$0.25 |
| ss - bc (Successful-source eksi Both-correct) | +11.10$\pm$1.09 | +6.58$\pm$0.89 | +3.32 / +2.77 | +7.99$\pm$0.29 |

### bc - tc, kosum duzeyi %95 t araligi (df = kosum sayisi - 1)

- CIFAR-10 Linf: ortalama +3.91, SD 0.32, %95 t araligi [+3.12; +4.70] (df=2, t=4.303); kosum degerleri +3.68, +3.77, +4.27; aralik sifiri icermez
- CIFAR-100 Linf: ortalama +5.97, SD 0.98, %95 t araligi [+3.53; +8.40] (df=2, t=4.303); kosum degerleri +6.94, +5.98, +4.98; aralik sifiri icermez
- SVHN Linf: yalniz 2 kosum (df=1); aralik HESAPLANMADI. Iki kosum degeri: +0.82 / +0.49
- CIFAR-10 L2: ortalama +1.95, SD 0.25, %95 t araligi [+1.33; +2.56] (df=2, t=4.303); kosum degerleri +1.78, +1.83, +2.23; aralik sifiri icermez

### Temiz dogruluk farki, ResNet-18 AT eksi ViT-Tiny AT (puan)

| Ayar | ResNet-18 AT temiz | ViT-Tiny AT temiz | Fark (R - V) | Kaynak |
|---|---|---|---|---|
| CIFAR-10 | 85.78$\pm$0.36 | 73.53$\pm$0.55 | +12.26$\pm$0.90 | `results/c1_eval_summary.json resnet18_at/vit_tiny_at clean.values` |
| CIFAR-100 | 63.86$\pm$1.05 | 43.17$\pm$1.10 | +20.69$\pm$1.89 | `results/q1/e1_cifar100_summary.json mimariler/*/ozet/test_clean/degerler` |
| SVHN | 94.76 / 93.77 | 92.82 / 92.03 | +1.94 / +1.74 | `results/q1/e7_svhn_summary.json mimariler/*/ozet/test_clean/degerler` |

(Fark kosum cifti basina alinir: kosum k icin ResNet tohum 100k, ViT tohum 200k. SVHN'de iki kosum, SD yazilmaz.)

### Basarili-kaynak: siki ve gevsek okuma

Siki okuma: kaynak temiz girdide dogru ve saldiri sonrasi yanlis (ss_definition). Gevsek okuma: kaynagin temizde zaten yanlis siniflandirdigi ornekler de dahil. Kaynak: her ayarin `pair*/a2_transfer_protocols.json` dosyasindaki `protocols/successful_source_loose`. Yayilim = kosum basina (en buyuk - en kucuk) {Unconditioned, Target-correct, Both-correct, Successful-source} farki; gevsek yayilimda son protokol gevsek okumadir.

| Ayar | ss siki | ss gevsek | siki - gevsek | Yayilim (siki) | Yayilim (gevsek) |
|---|---|---|---|---|---|
| CIFAR-10 Linf | +19.37$\pm$1.27 | +14.60$\pm$1.48 | +4.77$\pm$0.39 | 15.01$\pm$0.84 | 10.45$\pm$0.76 |
| CIFAR-100 Linf | +17.50$\pm$0.92 | +11.44$\pm$1.82 | +6.06$\pm$0.94 | 13.83$\pm$1.30 | 13.58$\pm$1.71 |
| SVHN Linf | +2.98 / +2.41 | +2.62 / +2.66 | +0.36 / -0.25 | 4.14 / 3.26 | 3.78 / 3.51 |
| CIFAR-10 L2 | +12.06$\pm$0.23 | +9.51$\pm$0.89 | +2.55$\pm$0.85 | 10.92$\pm$0.82 | 10.91$\pm$0.83 |

## Tablo 8 ek sutunlari: isaretli hizalanma ve native-ViT kontrolu

_Kaynak: `results/c1_a3/pair*/a3_gradient_paired.json (isaretli kosinus); results/c1_gradient/pair*/gradient_summary.json (native-ViT ve capraz kontrol)`_

Onceki foy ('Gradyan yapisi') isaretli kosinusu yalniz TEK sayi olarak veriyordu (iki modelin mutlak degerce en buyugu); asagida uc kosum ayri ayri, ortalama$\pm$SD (ddof=1).

`results/c1_gradient/pair*/gradient_summary.json` isaretli kosinus ALANI TASIMAZ; isaretli deger `results/c1_a3/pair*/a3_gradient_paired.json` -> `alignment/<model>/all_pairs_signed_mean` alanindadir (artefakta 4 ondalikli yazilmis).

| Olcut | ResNet-18 AT | ViT-Tiny AT | Kosum degerleri (R / V) |
|---|---|---|---|
| Hizalanma (isaretli, tum cift ortalamasi) | 0.0010$\pm$0.0003 | 0.0004$\pm$0.0001 | 0.0014, 0.0008, 0.0008 / 0.0005, 0.0004, 0.0004 |
| Hizalanma (mutlak, tum cift ortalamasi; Tablo 8 mutlak satirindan FARKLI olcum) | 0.0381$\pm$0.0009 | 0.0566$\pm$0.0007 | 0.0382, 0.0372, 0.0390 / 0.0558, 0.0569, 0.0570 |

ResNet-18 AT ve ViT-Tiny AT sutunlari `gradient_summary.json` uc kosum ortalamasidir (Tablo 8 ile ayni); native-ViT kontrolu (`gradient_summary.json`, kosum basina n=500; sparsity_*_std alanlari 10 grup ortalamasi arasi SDdir, burada KULLANILMAZ):

| Olcut | ResNet-18 AT | ViT-Tiny AT | ViT (native) | Native kosum degerleri |
|---|---|---|---|---|
| Hoyer | 0.4928$\pm$0.0120 | 0.4561$\pm$0.0055 | 0.4046 (tek checkpoint, SD yok) | 0.4046, 0.4046, 0.4046 |
| Gini | 0.6498$\pm$0.0089 | 0.6099$\pm$0.0051 | 0.5712 (tek checkpoint, SD yok) | 0.5712, 0.5712, 0.5712 |
| Rel-esik (%1 alti) | 0.3477$\pm$0.0210 | 0.2682$\pm$0.0090 | 0.1785 (tek checkpoint, SD yok) | 0.1785, 0.1785, 0.1785 |
| Hizalanma (mutlak kosinus) | 0.0378$\pm$0.0009 | 0.0562$\pm$0.0004 | 0.0794 (tek checkpoint, SD yok) | 0.0794, 0.0794, 0.0794 |

Native-ViT: uc kosum dosyasindaki Hoyer degerleri ozdes; makale tek checkpoint diyor (egitim bolunme protokolunden once, test kumesinde secilmis). Model yollari: `gradient_summary.json` model_paths yalniz ResNet18_AT ve ViT_Tiny_AT'i listeler, native checkpoint yolu artefaktta YOK.

Native-ViT isaretli hizalanma: ARTEFAKT YOK (`a3_gradient_paired.json` ve `gradient_summary.json` isaretli kosinusu yalniz ResNet18_AT ve ViT_Tiny_AT icin tasir).

## Tablo 9 ek sutunlari: Diff SD ve kosum duzeyi p (Holm)

_Kaynak: `results/c1_c45_summary.json spatial/*/diff; results/c1_c5/pair*/c5_spatial.json paired_diff_ResNet_minus_ViT (kosum basina fark)`_

Kosum duzeyi p: uc kosumun ResNet-eksi-ViT fark ortalamalarina tek orneklem iki yonlu t testi (H0: fark = 0, df=2); dort olcu uzerinde Holm duzeltmesi. Diff SD = kosumlar arasi SD (ddof=1). Wilcoxon sutunu onceki foydeki ornek duzeyi en buyuk p'dir ve ayri bir birimdir.

| Olcut | Fark (R-V) ort.$\pm$SD | Kosum degerleri | t (df=2) | p (ham) | p (Holm) | Wilcoxon p (en buyuk) |
|---|---|---|---|---|---|---|
| Enerji %50 alani | -0.0019$\pm$0.0027 | -0.0021, -0.0044, +0.0009 | -1.217 | 0.348 | 0.535 | 2.63e-01 |
| Enerji %90 alani | -0.0224$\pm$0.0133 | -0.0241, -0.0349, -0.0083 | -2.912 | 0.100 | 0.402 | 3.85e-02 |
| Mekansal entropi | -0.0509$\pm$0.0580 | -0.0612, -0.1031, +0.0115 | -1.521 | 0.268 | 0.535 | 8.00e-01 |
| Moran's I | +0.0200$\pm$0.0156 | +0.0260, +0.0024, +0.0317 | +2.229 | 0.156 | 0.467 | 5.35e-01 |

## Tablo 10: residual blok cikisi kosinusu (n=1000, uc kosum)

_Kaynak: `results/c1_c4/pair*/c4_summary.json vit/cos_block_cls, vit/cos_block_token_mean, vit/cos_block_output; resnet/cos`_

Kosum ortalamasi$\pm$kosumlar arasi SD (ddof=1); her kosumun degeri c4_summary.json icindeki n=1000 ornek ortalamasidir. Blok numarasi 1-tabanli (makale 'Blk' sutunu). `cos_block_cls` = CLS jetonu, `cos_block_token_mean` = yama jetonlari ortalamasi, `cos_block_output` = tum jetonlar, hepsi blok CIKISINDA.

| Blok | CLS | Yama ortalamasi | Tum jetonlar |
|---|---|---|---|
| 1 | 0.9993$\pm$0.0001 | 0.9980$\pm$0.0004 | 0.9927$\pm$0.0004 |
| 2 | 0.9950$\pm$0.0019 | 0.9959$\pm$0.0012 | 0.9901$\pm$0.0013 |
| 3 | 0.9902$\pm$0.0031 | 0.9940$\pm$0.0008 | 0.9881$\pm$0.0011 |
| 4 | 0.9873$\pm$0.0036 | 0.9919$\pm$0.0020 | 0.9861$\pm$0.0016 |
| 5 | 0.9845$\pm$0.0041 | 0.9904$\pm$0.0023 | 0.9847$\pm$0.0019 |
| 6 | 0.9814$\pm$0.0031 | 0.9894$\pm$0.0017 | 0.9835$\pm$0.0020 |
| 7 | 0.9782$\pm$0.0041 | 0.9885$\pm$0.0019 | 0.9826$\pm$0.0020 |
| 8 | 0.9743$\pm$0.0058 | 0.9875$\pm$0.0021 | 0.9816$\pm$0.0021 |
| 9 | 0.9703$\pm$0.0044 | 0.9870$\pm$0.0014 | 0.9809$\pm$0.0018 |
| 10 | 0.9661$\pm$0.0044 | 0.9872$\pm$0.0013 | 0.9805$\pm$0.0017 |
| 11 | 0.9604$\pm$0.0029 | 0.9874$\pm$0.0021 | 0.9803$\pm$0.0017 |
| 12 | 0.9663$\pm$0.0061 | 0.9915$\pm$0.0027 | 0.9837$\pm$0.0036 |

Minimumlar ve oran (manset; 'C4' bolumundeki ayni sayilar):

- CLS (cos_block_cls): minimum blok 11, 0.9604$\pm$0.0029
- Yama ortalamasi (cos_block_token_mean): minimum blok 9, 0.9870$\pm$0.0014
- Tum jetonlar (cos_block_output): minimum blok 11, 0.9803$\pm$0.0017
- (1 - cos) orani, CLS minimumu / yama ortalamasi minimumu: 3.05
- Blok cikisi oznitelik normu degisimi: kosum ortalamasinin mutlak degerce en buyugu 0.44% (`vit/norm_change_pct/block*`, makale '%0.45 icinde' diyor)

ResNet-18 AT, katman kosinusu (kosum ortalamasi$\pm$SD):

| Katman | Kosinus | Norm degisimi (%) |
|---|---|---|
| layer1.0 | 0.9951$\pm$0.0003 | -0.19$\pm$0.02 |
| layer1.1 | 0.9918$\pm$0.0003 | -0.43$\pm$0.06 |
| layer2.0 | 0.9879$\pm$0.0014 | -0.47$\pm$0.05 |
| layer2.1 | 0.9853$\pm$0.0016 | -0.66$\pm$0.04 |
| layer3.0 | 0.9753$\pm$0.0018 | -1.50$\pm$0.05 |
| layer3.1 | 0.9607$\pm$0.0046 | -2.93$\pm$0.38 |
| layer4.0 | 0.8777$\pm$0.0181 | -13.14$\pm$1.89 |
| layer4.1 | 0.9108$\pm$0.0060 | +5.84$\pm$3.53 |

## Dikkat entropisi ve CLS dikkat yer degistirmesi (katman basina)

_Kaynak: `results/c1_c4/pair*/c4_summary.json vit/attention/{entropy_clean_mean, entropy_adv_mean, entropy_delta_mean, displacement_mean}`_

Entropi nat cinsinden, CLS dikkat dagilimi. Yer degistirme = temiz ile cekismeli CLS dikkat dagilimlari arasindaki toplam varyasyon uzakligi (`c1_c45_aggregate.py` etiketi: 'CLS yer degistirmesi (toplam varyasyon)'). Hucre = kosum ortalamasi$\pm$SD (ddof=1), her kosum n=1000 ornek. Fark = cekismeli - temiz (kosum basina alinip ortalanir).

| Katman | Temiz entropi | Cekismeli entropi | Fark (adv - temiz) | TV yer degistirmesi |
|---|---|---|---|---|
| 1 | 5.1055$\pm$0.0695 | 5.1055$\pm$0.0697 | +0.0000$\pm$0.0006 | 0.0276$\pm$0.0102 |
| 2 | 4.8839$\pm$0.2069 | 4.8823$\pm$0.2068 | -0.0016$\pm$0.0007 | 0.0423$\pm$0.0071 |
| 3 | 4.8591$\pm$0.1681 | 4.8593$\pm$0.1668 | +0.0002$\pm$0.0014 | 0.0492$\pm$0.0088 |
| 4 | 4.8528$\pm$0.0514 | 4.8534$\pm$0.0496 | +0.0007$\pm$0.0017 | 0.0448$\pm$0.0077 |
| 5 | 4.8201$\pm$0.0948 | 4.8176$\pm$0.0968 | -0.0025$\pm$0.0021 | 0.0528$\pm$0.0043 |
| 6 | 4.8046$\pm$0.2458 | 4.8030$\pm$0.2471 | -0.0015$\pm$0.0020 | 0.0652$\pm$0.0100 |
| 7 | 4.9001$\pm$0.0747 | 4.9013$\pm$0.0770 | +0.0011$\pm$0.0036 | 0.0726$\pm$0.0065 |
| 8 | 4.6128$\pm$0.1115 | 4.6142$\pm$0.1094 | +0.0014$\pm$0.0067 | 0.0779$\pm$0.0060 |
| 9 | 4.7541$\pm$0.2012 | 4.7555$\pm$0.2009 | +0.0013$\pm$0.0019 | 0.0785$\pm$0.0105 |
| 10 | 4.6481$\pm$0.1905 | 4.6526$\pm$0.1818 | +0.0045$\pm$0.0088 | 0.0776$\pm$0.0079 |
| 11 | 4.6987$\pm$0.0257 | 4.6976$\pm$0.0233 | -0.0011$\pm$0.0036 | 0.0836$\pm$0.0025 |
| 12 | 4.6637$\pm$0.0927 | 4.6604$\pm$0.0978 | -0.0033$\pm$0.0057 | 0.0841$\pm$0.0076 |
| Genel (katman ortalamasi) | 4.8003$\pm$0.0362 | 4.8002$\pm$0.0372 | -0.0001$\pm$0.0021 | 0.0630$\pm$0.0011 |

- En buyuk |entropi farki| (kosum ortalamasi, katman basina): 0.0045 nat (katman 10)
- Katman ortalamasi temiz entropi 4.80 nat
- TV yer degistirmesi: 0.0276 (katman 1) -> 0.0841 (katman 12), kosum ortalamasi

## Epsilon taramasi (PGD-10, Linf)

_Kaynak: `results/c1_sweep/pair*/*/*_robustness_results.csv; results/wrn_eval/wrn_eval_summary.json; results/c1_eval_summary.json`_

ResNet-18 AT ve ViT-Tiny AT: uc kosum ortalamasi$\pm$SD (ddof=1), tam test kumesi n=10000. WRN-28-10: TEK model (RobustBench Gowal2020), SD yok, n=10000, saldiri PGD-10 (alpha=2/255).

| eps | ResNet-18 AT | ViT-Tiny AT | WRN-28-10 |
|---|---|---|---|
| 0 (temiz) | 85.78$\pm$0.36 | 73.53$\pm$0.55 | 89.48 |
| 2/255 | 77.30$\pm$0.12 | 64.10$\pm$0.16 | 85.35 |
| 4/255 | 66.73$\pm$0.35 | 53.89$\pm$0.17 | 80.00 |
| 8/255 | 44.19$\pm$0.59 | 32.66$\pm$0.18 | 66.92 |
| 16/255 | 20.38$\pm$0.23 | 12.16$\pm$0.09 | 47.36 |

Tablo I ile 8/255 (ve temiz) tutarliligi: tarama kosumlari tabloyu uretenlerle AYNI kosum degerleri mi?

| Model | Olcut | Tarama ort.$\pm$SD | Tablo I (c1_eval_summary) ort.$\pm$SD | Ortalama farki (tarama - Tablo I) | Kosum basina fark |
|---|---|---|---|---|---|
| ResNet-18 AT | temiz | 85.78$\pm$0.36 | 85.78$\pm$0.36 | +0.00 | +0.00, +0.00, +0.00 |
| ResNet-18 AT | PGD-10 8/255 | 44.19$\pm$0.59 | 44.11$\pm$0.50 | +0.08 | +0.19, +0.06, +0.00 |
| ViT-Tiny AT | temiz | 73.53$\pm$0.55 | 73.53$\pm$0.55 | +0.00 | +0.00, +0.00, +0.00 |
| ViT-Tiny AT | PGD-10 8/255 | 32.66$\pm$0.18 | 32.69$\pm$0.22 | -0.03 | -0.05, +0.01, -0.06 |
| WRN-28-10 | PGD-10 8/255 | 66.92 | Tablo I WRN satiri ELLE YAZILMIS LITERAL (66.92; 'Sabit dizgeler' bolumu) | +0.00 | tek model |

## Kaynak-hedef toplamsal ayristirma (hedef-dogru oranlar)

_Kaynak: `results/q1/kaynak_hedef_ayristirma.json`_

Yontem (artefaktin kendi alani): oran(s->t) = mu + alpha_s + beta_t + eps, kosegen disi hucreler, toplam-sifir (etki kodlamasi), numpy lstsq. 3x3'te 6 hucre, 5 parametre, 1 artik serbestlik derecesi. Ozet matris: uc tohum ortalamasi (c3_summary 'cond' = hedef-dogru). Cift basina: transfer_matrix.json ve per_sample npz; bc ve ss protokolleri src/analysis/protokoller.py maskeleriyle npz'den hesaplanir; ciftler arasi SD ddof=1 (n=3). Kaynak farki = alpha_ResNet - alpha_ViT; hedef farki = beta_ViT - beta_ResNet; toplamlari artik farkiyla birlikte ResNet->ViT eksi ViT->ResNet asimetrisine esittir. Mahmood: 8x8 bc matrisi, ayni model; aile duzeyi farklar alpha/beta aile ortalamalarinin farki.. Birim: yuzde puan. Artefakt uretim zamani: 2026-10-04T15:21:58.090312+00:00.

Okuma: kaynak etkisi farki = alpha_ResNet - alpha_ViT; hedef etkisi farki = beta_ViT - beta_ResNet; asimetri = ResNet->ViT eksi ViT->ResNet = kaynak farki + hedef farki + artik farki. 'Cift' = bir egitim cifti (uc tohum cifti); ortalama$\pm$SD ciftler arasidir (ddof=1, n=3).


### CIFAR-10: cift basina ayristirma (uc cift)

| Protokol | Kaynak etkisi farki (R-V) | Hedef etkisi farki (V-R) | Asimetri (R->V eksi V->R) | Artik farki | En buyuk mutlak artik | R2 | Kaynak farki, cift degerleri | Hedef farki, cift degerleri |
|---|---|---|---|---|---|---|---|---|
| Unconditioned (raw) | +4.47$\pm$0.10 | +8.13$\pm$0.33 | +13.62$\pm$0.38 | +1.03$\pm$0.06 | 0.51$\pm$0.03 | 0.9964$\pm$0.0004 | +4.44 / +4.58 / +4.39 | +7.75 / +8.34 / +8.30 |
| Target-correct | +5.13$\pm$0.09 | -2.03$\pm$0.51 | +4.41$\pm$0.45 | +1.30$\pm$0.10 | 0.65$\pm$0.05 | 0.9782$\pm$0.0032 | +5.09 / +5.23 / +5.08 | -1.55 / -1.96 / -2.57 |
| Both-correct | +6.76$\pm$0.35 | -0.53$\pm$0.59 | +8.30$\pm$0.16 | +2.07$\pm$0.22 | 1.04$\pm$0.11 | 0.9643$\pm$0.0072 | +6.37 / +6.88 / +7.04 | +0.03 / -0.50 / -1.13 |
| Successful-source | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK |

- Successful-source: artefakt notu: yok (ornek bazli kayitta source_adv_wrong alani yok)

Sabit-WRN karsitliklari (CIFAR-10, cift basina oranlar, ortalama$\pm$SD): WRN hedefine ResNet kaynaktan ve ViT kaynaktan gelen oran (fark = ResNet - ViT); WRN kaynagindan ResNet ve ViT hedefe giden oran (fark = ResNet hedef - ViT hedef).

| Protokol | WRN hedefine ResNet'ten | WRN hedefine ViT'ten | Hedef karsitligi (R-V) | WRN kaynagindan ResNet'e | WRN kaynagindan ViT'e | Kaynak karsitligi (R-V) |
|---|---|---|---|---|---|---|
| Unconditioned (raw) | 21.69$\pm$0.09 | 18.25$\pm$0.12 | +3.44$\pm$0.16 | 32.63$\pm$0.14 | 39.73$\pm$0.25 | -7.10$\pm$0.32 |
| Target-correct | 12.49$\pm$0.10 | 8.65$\pm$0.13 | +3.83$\pm$0.17 | 21.48$\pm$0.31 | 18.15$\pm$0.28 | +3.33$\pm$0.59 |
| Both-correct | 9.33$\pm$0.29 | 4.64$\pm$0.10 | +4.69$\pm$0.38 | 19.65$\pm$0.30 | 17.04$\pm$0.44 | +2.60$\pm$0.72 |
| Successful-source | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK | ARTEFAKT YOK |


CIFAR-10: uc tohum ortalamasi matris (`results/c1_c3/c3_summary.json`), tek uydurma (kosegen haric 6 hucre, 5 parametre, 1 artik serbestlik derecesi).

| Olcut | Hedef-dogru (target_correct) | Ham (raw), duyarlilik |
|---|---|---|
| Kaynak etkisi farki (R-V) | +5.13 | +4.47 |
| Hedef etkisi farki (V-R) | -2.02 | +8.13 |
| Asimetri (R->V eksi V->R) | +4.41 | +13.62 |
| Artik farki | +1.30 | +1.03 |
| En buyuk mutlak artik | 0.65 | 0.51 |
| R2 | 0.9782 | 0.9964 |
| mu | 16.04 | 30.14 |
| Hucre / parametre / artik serbestlik | 6 / 5 / 1 | 6 / 5 / 1 |
| WRN hedefine ResNet'ten / ViT'ten / fark | 12.48 / 8.65 / +3.83 | 21.69 / 18.25 / +3.44 |
| WRN kaynagindan ResNet'e / ViT'e / fark | 21.48 / 18.15 / +3.33 | 32.63 / 39.73 / -7.10 |

CIFAR-10, hedef-dogru ozet matris, model etkileri (toplam-sifir kodlama, mu = 16.04):

| Model | Kaynak etkisi alpha | Hedef etkisi beta |
|---|---|---|
| ResNet18_AT | +1.87 | +3.40 |
| ViT_Tiny_AT | -3.26 | +1.37 |
| WRN_28_10 | +1.39 | -4.77 |

Ornek bazli npz ile JSON ozeti tutarliligi (en buyuk mutlak sapma, puan): pair1: ham 3.6e-15, hedef-dogru 0.0038; pair2: ham 7.1e-15, hedef-dogru 0.0050; pair3: ham 3.6e-15, hedef-dogru 0.0036


### CIFAR-100: cift basina ayristirma (uc cift)

| Protokol | Kaynak etkisi farki (R-V) | Hedef etkisi farki (V-R) | Asimetri (R->V eksi V->R) | Artik farki | En buyuk mutlak artik | R2 | Kaynak farki, cift degerleri | Hedef farki, cift degerleri |
|---|---|---|---|---|---|---|---|---|
| Unconditioned (raw) | +6.48$\pm$0.38 | +10.72$\pm$0.97 | +18.53$\pm$0.71 | +1.34$\pm$0.03 | 0.67$\pm$0.01 | 0.9946$\pm$0.0003 | +6.07 / +6.81 / +6.55 | +11.80 / +10.41 / +9.94 |
| Target-correct | +9.54$\pm$0.64 | -6.19$\pm$0.93 | +4.96$\pm$1.02 | +1.60$\pm$0.10 | 0.80$\pm$0.05 | 0.9871$\pm$0.0015 | +8.82 / +10.04 / +9.76 | -6.10 / -7.16 / -5.30 |
| Both-correct | +11.79$\pm$0.83 | -2.85$\pm$0.93 | +10.92$\pm$0.34 | +1.98$\pm$0.20 | 0.99$\pm$0.10 | 0.9851$\pm$0.0035 | +11.82 / +12.61 / +10.95 | -2.62 / -3.87 / -2.05 |
| Successful-source | +20.82$\pm$1.43 | -8.12$\pm$2.23 | +17.50$\pm$0.92 | +4.80$\pm$0.12 | 2.40$\pm$0.06 | 0.9830$\pm$0.0008 | +20.61 / +22.34 / +19.51 | -8.70 / -9.99 / -5.66 |


Sabit-WRN karsitliklari (CIFAR-100, cift basina oranlar, ortalama$\pm$SD): WRN hedefine ResNet kaynaktan ve ViT kaynaktan gelen oran (fark = ResNet - ViT); WRN kaynagindan ResNet ve ViT hedefe giden oran (fark = ResNet hedef - ViT hedef).

| Protokol | WRN hedefine ResNet'ten | WRN hedefine ViT'ten | Hedef karsitligi (R-V) | WRN kaynagindan ResNet'e | WRN kaynagindan ViT'e | Kaynak karsitligi (R-V) |
|---|---|---|---|---|---|---|
| Unconditioned (raw) | 51.23$\pm$0.25 | 46.10$\pm$0.48 | +5.13$\pm$0.38 | 60.28$\pm$0.16 | 69.65$\pm$1.03 | -9.37$\pm$0.95 |
| Target-correct | 23.44$\pm$0.38 | 15.50$\pm$0.72 | +7.94$\pm$0.54 | 37.83$\pm$0.90 | 30.04$\pm$0.66 | +7.79$\pm$0.95 |
| Both-correct | 18.33$\pm$0.84 | 8.52$\pm$0.39 | +9.81$\pm$1.03 | 32.01$\pm$0.75 | 27.18$\pm$0.76 | +4.83$\pm$0.75 |
| Successful-source | 27.49$\pm$0.93 | 11.46$\pm$0.74 | +16.03$\pm$1.42 | 63.74$\pm$2.52 | 50.83$\pm$0.72 | +12.91$\pm$2.29 |


CIFAR-100: uc tohum ortalamasi matris (`results/q1/cifar100/transfer/e1_c3_summary.json`), tek uydurma (kosegen haric 6 hucre, 5 parametre, 1 artik serbestlik derecesi).

| Olcut | Hedef-dogru (target_correct) | Ham (raw), duyarlilik |
|---|---|---|
| Kaynak etkisi farki (R-V) | +9.54 | +6.48 |
| Hedef etkisi farki (V-R) | -6.19 | +10.72 |
| Asimetri (R->V eksi V->R) | +4.96 | +18.53 |
| Artik farki | +1.60 | +1.34 |
| En buyuk mutlak artik | 0.80 | 0.67 |
| R2 | 0.9871 | 0.9946 |
| mu | 25.53 | 57.33 |
| Hucre / parametre / artik serbestlik | 6 / 5 / 1 | 6 / 5 / 1 |
| WRN hedefine ResNet'ten / ViT'ten / fark | 23.44 / 15.50 / +7.93 | 51.23 / 46.10 / +5.13 |
| WRN kaynagindan ResNet'e / ViT'e / fark | 37.83 / 30.04 / +7.79 | 60.28 / 69.65 / -9.37 |

CIFAR-100, hedef-dogru ozet matris, model etkileri (toplam-sifir kodlama, mu = 25.53):

| Model | Kaynak etkisi alpha | Hedef etkisi beta |
|---|---|---|
| ResNet18_AT | +1.19 | +4.33 |
| ViT_Tiny_AT | -8.35 | -1.85 |
| WRN_28_10 | +7.16 | -2.48 |

Ornek bazli npz ile JSON ozeti tutarliligi (en buyuk mutlak sapma, puan): pair1: ham 7.1e-15, hedef-dogru 0.0036; pair2: ham 7.1e-15, hedef-dogru 0.0049; pair3: ham 7.1e-15, hedef-dogru 0.0048


Cift basina ortalama ve SD alanlarinin `degerler` dizisinden yeniden hesabiyla tutarlilik: en buyuk sapma 0.00e+00 (UYUMLU).


### Mahmood ve ark. (2021) CIFAR-10 8x8 matrisi: toplamsal ve aile-terimli uydurma

Protokol: both_correct (Mahmood Denklem 3), m = 1000; kosegen (bagimsiz kopya) haric 56 hucre.

| Uydurma | R2 | En buyuk mutlak artik | Hucre | Parametre | Artik serbestlik | Ayni-cins gamma |
|---|---|---|---|---|---|---|
| Toplamsal (mu + alpha_kaynak + beta_hedef) | 0.3681 | 74.04 | 56 | 15 | 41 | yok |
| Toplamsal + ayni-cins terimi | 0.7852 | 29.33 | 56 | 16 | 40 | +42.68 |

Not (artefakttan): Toplamsal model Mahmood matrisinde cins-ici blok yapisini tasiyamaz (dusuk R2); ayni-cins gostergesi eklenmis duyarlilik uydurmasi.

| Aile karsitligi | Toplamsal: kaynak farki (CNN-ViT) | Toplamsal: hedef farki (ViT-CNN) | Aile-terimli: kaynak farki (CNN-ViT) | Aile-terimli: hedef farki (ViT-CNN) |
|---|---|---|---|---|
| CNN_vs_ViT_hibrit_haric | -25.01 | +2.08 | -10.78 | -12.15 |
| CNN_vs_ViT_hibrit_dahil | -25.05 | -1.92 | -10.82 | -16.14 |
| BiT_vs_ViT | -25.95 | -7.03 | -11.72 | -21.26 |
| ResNet_vs_ViT | -24.06 | +11.18 | -9.84 | -3.05 |

| Model | Cins (uydurmadaki) | Toplamsal alpha | Toplamsal beta | Aile-terimli alpha | Aile-terimli beta |
|---|---|---|---|---|---|
| ViT-B-32 | ViT | +18.56 | -3.57 | +11.44 | -10.68 |
| ViT-B-16 | ViT | +10.09 | +8.09 | +2.98 | +0.98 |
| ViT-L-16 | ViT | +8.79 | +4.58 | +1.68 | -2.53 |
| ViT-R50 | ViT | +12.66 | -12.94 | +5.55 | -20.05 |
| BiT-M-R50x1 | BiT | -16.62 | +12.78 | -9.51 | +19.89 |
| BiT-M-R101x3 | BiT | -10.31 | +7.35 | -3.20 | +14.46 |
| ResNet-56 | ResNet | -11.32 | -9.01 | -4.21 | -1.89 |
| ResNet-164 | ResNet | -11.85 | -7.28 | -4.73 | -0.17 |

Aileler arasi 16 cift, toplamsal uydurmadan ayristirma (asimetri = CNN->ViT eksi ViT->CNN):

| Cift | Asimetri | Kaynak farki | Hedef farki | Artik farki |
|---|---|---|---|---|
| BiT-M-R50x1 vs ViT-B-32 | -56.30 | -35.18 | -16.35 | -4.77 |
| BiT-M-R50x1 vs ViT-B-16 | -32.50 | -26.72 | -4.68 | -1.10 |
| BiT-M-R50x1 vs ViT-L-16 | -36.80 | -25.41 | -8.20 | -3.19 |
| BiT-M-R50x1 vs ViT-R50 | -56.30 | -29.28 | -25.72 | -1.30 |
| BiT-M-R101x3 vs ViT-B-32 | -53.40 | -28.87 | -10.92 | -13.61 |
| BiT-M-R101x3 vs ViT-B-16 | -24.70 | -20.41 | +0.74 | -5.04 |
| BiT-M-R101x3 vs ViT-L-16 | -31.00 | -19.10 | -2.77 | -9.13 |
| BiT-M-R101x3 vs ViT-R50 | -50.80 | -22.97 | -20.29 | -7.54 |
| ResNet-56 vs ViT-B-32 | -12.00 | -29.88 | +5.44 | +12.44 |
| ResNet-56 vs ViT-B-16 | -4.90 | -21.41 | +17.10 | -0.59 |
| ResNet-56 vs ViT-L-16 | -7.70 | -20.11 | +13.59 | -1.18 |
| ResNet-56 vs ViT-R50 | -17.00 | -23.98 | -3.93 | +10.91 |
| ResNet-164 vs ViT-B-32 | -13.10 | -30.40 | +3.71 | +13.59 |
| ResNet-164 vs ViT-B-16 | -5.90 | -21.94 | +15.38 | +0.66 |
| ResNet-164 vs ViT-L-16 | -9.80 | -20.64 | +11.86 | -1.03 |
| ResNet-164 vs ViT-R50 | -19.30 | -24.51 | -5.66 | +10.86 |

Sabit ucuncu model karsitligi (BiT-M-R50x1 ve ViT-L-16 ayni ucuncu modele karsi; hucre = ham matris farki, puan):

| Ucuncu model k | Sabit hedef k: (BiT-M-R50x1->k) eksi (ViT-L-16->k) | Sabit kaynak k: (k->BiT-M-R50x1) eksi (k->ViT-L-16) |
|---|---|---|
| ViT-B-32 | -51.1 | -14.7 |
| ViT-B-16 | -67.5 | -45.5 |
| ViT-R50 | -25.6 | +9.5 |
| BiT-M-R101x3 | +6.7 | +62.2 |
| ResNet-56 | -6.0 | +17.2 |
| ResNet-164 | -5.8 | +17.3 |


### Mahmood ve ark. (2021) CIFAR-100 8x8 matrisi: toplamsal ve aile-terimli uydurma

Protokol: both_correct (Mahmood Denklem 3), m = 1000; kosegen (bagimsiz kopya) haric 56 hucre.

| Uydurma | R2 | En buyuk mutlak artik | Hucre | Parametre | Artik serbestlik | Ayni-cins gamma |
|---|---|---|---|---|---|---|
| Toplamsal (mu + alpha_kaynak + beta_hedef) | 0.4508 | 66.29 | 56 | 15 | 41 | yok |
| Toplamsal + ayni-cins terimi | 0.8425 | 24.33 | 56 | 16 | 40 | +40.05 |

Not (artefakttan): Toplamsal model Mahmood matrisinde cins-ici blok yapisini tasiyamaz (dusuk R2); ayni-cins gostergesi eklenmis duyarlilik uydurmasi.

| Aile karsitligi | Toplamsal: kaynak farki (CNN-ViT) | Toplamsal: hedef farki (ViT-CNN) | Aile-terimli: kaynak farki (CNN-ViT) | Aile-terimli: hedef farki (ViT-CNN) |
|---|---|---|---|---|
| CNN_vs_ViT_hibrit_haric | -22.77 | +14.74 | -9.43 | +1.39 |
| CNN_vs_ViT_hibrit_dahil | -21.93 | +11.56 | -8.58 | -1.79 |
| BiT_vs_ViT | -23.65 | -0.67 | -10.30 | -14.02 |
| ResNet_vs_ViT | -21.90 | +30.15 | -8.55 | +16.81 |

| Model | Cins (uydurmadaki) | Toplamsal alpha | Toplamsal beta | Aile-terimli alpha | Aile-terimli beta |
|---|---|---|---|---|---|
| ViT-B-32 | ViT | +16.68 | +4.27 | +10.01 | -2.41 |
| ViT-B-16 | ViT | +9.13 | +14.19 | +2.45 | +7.52 |
| ViT-L-16 | ViT | +9.62 | +8.43 | +2.94 | +1.76 |
| ViT-R50 | ViT | +8.43 | -3.77 | +1.76 | -10.44 |
| BiT-M-R50x1 | BiT | -15.40 | +11.47 | -8.73 | +18.15 |
| BiT-M-R101x3 | BiT | -8.27 | +7.79 | -1.60 | +14.46 |
| ResNet-56 | ResNet | -11.48 | -20.55 | -4.80 | -13.88 |
| ResNet-164 | ResNet | -8.70 | -21.83 | -2.03 | -15.15 |

Aileler arasi 16 cift, toplamsal uydurmadan ayristirma (asimetri = CNN->ViT eksi ViT->CNN):

| Cift | Asimetri | Kaynak farki | Hedef farki | Artik farki |
|---|---|---|---|---|
| BiT-M-R50x1 vs ViT-B-32 | -42.80 | -32.09 | -7.20 | -3.51 |
| BiT-M-R50x1 vs ViT-B-16 | -19.50 | -24.53 | +2.72 | +2.31 |
| BiT-M-R50x1 vs ViT-L-16 | -32.10 | -25.02 | -3.04 | -4.04 |
| BiT-M-R50x1 vs ViT-R50 | -45.90 | -23.84 | -15.24 | -6.83 |
| BiT-M-R101x3 vs ViT-B-32 | -36.20 | -24.95 | -3.52 | -7.72 |
| BiT-M-R101x3 vs ViT-B-16 | -8.90 | -17.40 | +6.40 | +2.10 |
| BiT-M-R101x3 vs ViT-L-16 | -23.70 | -17.89 | +0.64 | -6.45 |
| BiT-M-R101x3 vs ViT-R50 | -37.70 | -16.71 | -11.56 | -9.44 |
| ResNet-56 vs ViT-B-32 | +5.20 | -28.16 | +24.82 | +8.54 |
| ResNet-56 vs ViT-B-16 | +13.20 | -20.61 | +34.74 | -0.94 |
| ResNet-56 vs ViT-L-16 | +5.40 | -21.10 | +28.99 | -2.49 |
| ResNet-56 vs ViT-R50 | +11.70 | -19.91 | +16.79 | +14.82 |
| ResNet-164 vs ViT-B-32 | +8.10 | -25.39 | +26.10 | +7.39 |
| ResNet-164 vs ViT-B-16 | +17.00 | -17.83 | +36.02 | -1.19 |
| ResNet-164 vs ViT-L-16 | +6.00 | -18.32 | +30.26 | -5.94 |
| ResNet-164 vs ViT-R50 | +14.30 | -17.14 | +18.06 | +13.37 |

Sabit ucuncu model karsitligi (BiT-M-R50x1 ve ViT-L-16 ayni ucuncu modele karsi; hucre = ham matris farki, puan):

| Ucuncu model k | Sabit hedef k: (BiT-M-R50x1->k) eksi (ViT-L-16->k) | Sabit kaynak k: (k->BiT-M-R50x1) eksi (k->ViT-L-16) |
|---|---|---|
| ViT-B-32 | -50.1 | -23.1 |
| ViT-B-16 | -63.3 | -48.7 |
| ViT-R50 | -29.9 | +1.8 |
| BiT-M-R101x3 | +6.5 | +47.7 |
| ResNet-56 | -5.0 | +16.1 |
| ResNet-164 | -4.3 | +20.4 |


## Dis veri: Mahmood ve ark. (ICCV 2021)

_Kaynak: `results/q1/dis_veri/mahmood2021_tablolar.json; results/q1/dis_veri/mahmood2021_ozdeslik.json; aile duzeyi kaynak/hedef etkileri icin results/q1/kaynak_hedef_ayristirma.json (Mahmood2021 bolumu)`_

Kunye (artefakttan): Mahmood, Mahmood, van Dijk. On the Robustness of Vision Transformers to Adversarial Examples. ICCV 2021, arXiv:2104.02610. Tablo 2 yonu: first column = model used to generate the adversarial examples, C_i; top row = model used to evaluate, C_j (satir = kaynak). Protokol alintisi: "we ﬁnd a set of m = 1000 examples that both classiﬁers correctly iden- tify".

Yon dogrulamasi (artefakt hukmu): Bolum 4.3 anlatisi ve sayfa 7 orneginin yedi hucresi de 'satir = kaynak' okumasiyla birebir tutuyor; Bolum 4.2'deki 'ust satir = kaynak' cumlesi baslik ve anlatiyla celisen bir yazim hatasidir.

Kosegen (artefakt hukmu): Kosegen beyaz kutu DEGILDIR: i = j icin bagimsiz egitilmis ikinci kopyaya transferdir. Ayristirmalarda kosegen kullanilmaz.

### Temiz dogruluklar (yuzde)

| Model | Aile (artefakttaki) | CIFAR-10 | CIFAR-100 |
|---|---|---|---|
| ViT-B-32 | ViT | 98.6 | 91.7 |
| ViT-B-16 | ViT | 98.9 | 92.8 |
| ViT-L-16 | ViT | 99.1 | 94.0 |
| ViT-R50 | hibrit | 98.6 | 91.8 |
| BiT-M-R50x1 | CNN | 97.5 | 87.4 |
| BiT-M-R101x3 | CNN | 98.7 | 91.8 |
| ResNet-56 | CNN | 92.8 | 71.6 |
| ResNet-164 | CNN | 93.8 | 74.2 |

CIFAR-100 kaynak notu: Ana metin Tablo 1'de YOK; ek malzeme Tablo 3 (sayfa 14) iceriyor ve oradan okundu.

### Rejim notlari (artefakttan, satir satir)

- on_egitim: ViT ve BiT-M modelleri ImageNet-21K on egitimli, CIFAR'a ince ayarli (alinti asagida); ResNet-56/164 icin on egitim belirtilmiyor
- on_egitim_alinti: pre-training dataset (X ′, Y ′) is ImageNet-21K and the training dataset (X, Y ) is either CIFAR-10, CIFAR-100 or ImageNet.
- egitim: standart (cekismeli egitim YOK); Tablo 1'de PGD/C&W/APGD saglam dogrulugu ~%0 (tablolar.json)
- epsilon: l_inf, eps = 0.031 (Tablo 1 basligi); bizimki 8/255
- saldiri: hucre basina FGSM, PGD, MIM'in EN BUYUGU (Tablo 2 basligi); bizimki tek PGD-10
- protokol: her ikisi dogru (Denklem 3), cift basina m = 1000 ornek; bizimki tam test kumesi, dort protokol
- kosegen: i = j bagimsiz egitilmis kopya; beyaz kutu degil
- model_olcegi: ViT-B/L ve BiT-M buyuk on egitimli modeller; bizimki ViT-Tiny / ResNet-18 / WRN-28-10, CIFAR uzerinde sifirdan cekismeli egitim

Ozdeslikte kullanilan p (bizim AT yonlerimizde olculen): p_min = 0.989014, p_ort = 0.997261; kaynak `results/q1/ozdeslik_kontrol.json`. Not: p bizim cekismeli egitilmis (AT) yonlerimizde olculdu; Mahmood modelleri standart egitimli, orada p olculmedi. p = 1 ust sinir olarak raporlanir.

Ozdeslik yontemi (artefakttan): Ozdeslik r_ham = e_t * p + r_tc * (1 - e_t). Mahmood yalniz bc (her ikisi dogru) verir; merkez tahminde r_tc = r_bc alinir. Varsayimsiz aralik: q = P(kaynak temiz yanlis | hedef temiz dogru) <= min(1, e_s / (1 - e_t)), r_tc in [r_bc(1-q), r_bc + q(1-r_bc)]. p iki degerle: 1 (ust sinir) ve ozdeslik_kontrol.json'daki bizim yonlerimizin en kucuk p'si. Asimetri aileler arasi ciftte CNN->ViT eksi ViT->CNN; protokol etkisi = ongorulen ham asimetri eksi bc asimetrisi. Kosegen (bagimsiz kopya) kullanilmaz.

### Anahtar cift: BiT-M-R50x1 ve ViT-L-16

| Veri | p | Temiz fark (CNN-ViT, puan) | Her-ikisi-dogru asimetri (CNN->ViT eksi ViT->CNN) | Ozdeslik-ongorulu ham asimetri | Ham asimetri araligi | Protokol etkisi (ham eksi bc) | Protokol etkisi araligi | Isaret merkezde doner mi | Isaret aralikta donebilir mi |
|---|---|---|---|---|---|---|---|---|---|
| CIFAR-10 | p=1 (ust sinir) | -1.60 | -36.80 | -37.39 | [-38.05; -34.65] | -0.59 | [-1.25; +2.15] | hayir | hayir |
| CIFAR-10 | p=p_min=0.989014 (ozdeslik_kontrol min) | -1.60 | -36.80 | -37.37 | [-38.03; -34.63] | -0.57 | [-1.23; +2.17] | hayir | hayir |
| CIFAR-100 | p=1 (ust sinir) | -6.60 | -32.10 | -33.63 | [-38.73; -20.13] | -1.53 | [-6.63; +11.97] | hayir | hayir |
| CIFAR-100 | p=p_min=0.989014 (ozdeslik_kontrol min) | -6.60 | -32.10 | -33.56 | [-38.66; -20.06] | -1.46 | [-6.56; +12.04] | hayir | hayir |

Artefaktin yorum alani: BiT-M-R50x1 vs ViT-L-16: temiz fark -1.60 puan (CNN eksi ViT), bc asimetrisi -36.80 puan, p=1 ile ongorulen ham asimetri -37.39 puan; protokol etkisi -0.59 puan.

### Aile duzeyi asimetri ve guclu kaynak ailesi sayimi

| Veri | Aile kumesi | Model sayisi | CNN->ViT bc ortalamasi (%) | ViT->CNN bc ortalamasi (%) | Aile asimetrisi (CNN->ViT eksi ViT->CNN) | Cift sayimi (ViT daha guclu / CNN guclu) | Guclu kaynak ailesi (artefakt: hibrit_* satirlari; alt aile: sayimdan) |
|---|---|---|---|---|---|---|---|
| CIFAR-10 | hibrit_haric | 3 ViT / 4 CNN | 8.71 | 32.72 | -24.01 | 12/12 | ViT |
| CIFAR-10 | hibrit_ViT_sayildi | 4 ViT / 4 CNN | 8.49 | 35.46 | -26.97 | 16/16 | ViT |
| CIFAR-10 | alt_aile_BiT-M_vs_ViT | 3 ViT / 2 CNN | 10.62 | 49.73 | -39.12 | CNN guclu: 0/6 | ViT |
| CIFAR-10 | alt_aile_ResNet_vs_ViT | 3 ViT / 2 CNN | 6.80 | 15.70 | -8.90 | CNN guclu: 0/6 | ViT |
| CIFAR-100 | hibrit_haric | 3 ViT / 4 CNN | 22.34 | 31.37 | -9.02 | 6/12 | ViT |
| CIFAR-100 | hibrit_ViT_sayildi | 4 ViT / 4 CNN | 22.29 | 32.66 | -10.37 | 8/16 | ViT |
| CIFAR-100 | alt_aile_BiT-M_vs_ViT | 3 ViT / 2 CNN | 24.73 | 51.93 | -27.20 | CNN guclu: 0/6 | ViT |
| CIFAR-100 | alt_aile_ResNet_vs_ViT | 3 ViT / 2 CNN | 19.95 | 10.80 | +9.15 | CNN guclu: 6/6 | CNN |

`hibrit_haric`: ViT-R50 (hibrit) disarida; 3 ViT x 4 CNN = 12 cift. `hibrit_ViT_sayildi`: ViT-R50 ViT sayilir; 4 ViT x 4 CNN = 16 cift (artefaktin model listelerinden).

### Aileler arasi 12 cift: temiz fark ve ozdeslik-ongorulu protokol etkisi

| Veri | Cift | En buyuk temiz hata farki (puan) | En kucuk mutlak bc asimetrisi | En buyuk mutlak protokol etkisi (p=1) | Hangi cift | Etki / mutlak asimetri en buyuk (p=1) | Isaret donen (merkez, p=1) | Isaret donen (merkez, p_min) | Isaret donebilir (aralik, p=1) |
|---|---|---|---|---|---|---|---|---|---|
| CIFAR-10 | 12 | 6.30 | 4.90 | 5.41 | ResNet-56 vs ViT-L-16 | 1.061 | 0/12 | 0/12 | 0/12 |
| CIFAR-100 | 12 | 22.40 | 5.20 | 20.51 | ResNet-56 vs ViT-L-16 | 3.797 | 6/12 | 6/12 | 6/12 |

Artefaktin uzlasma yorumu: Mahmood CIFAR-10'da guclu kaynak ailesi ViT, bizde CNN. Aileler arasi 12 ciftin hicbirinde ozdeslikle ongorulen ham-bc protokol etkisi asimetrinin isaretini cevirmiyor, varsayimsiz aralikta bile (en buyuk |etki| 5.41 puan, en kucuk |bc asimetrisi| 4.90 puan). CIFAR-10'da protokol farki iki calismanin yon celiskisini aciklamaz.

### CIFAR-100, ResNet-56 ve ResNet-164 x ViT ciftleri: yon ve protokol etkisi

| Cift (CNN vs ViT) | Temiz fark (CNN-ViT) | bc asimetrisi (CNN->ViT eksi ViT->CNN) | p=1 ham ongoru | Protokol etkisi | Etki araligi | Isaret merkezde doner mi | Isaret aralikta donebilir mi |
|---|---|---|---|---|---|---|---|
| ResNet-56 vs ViT-B-32 | -20.1 | +5.2 | -12.34 | -17.54 | [-30.31; +6.39] | evet | evet |
| ResNet-164 vs ViT-B-32 | -17.5 | +8.1 | -7.62 | -15.72 | [-28.56; +5.54] | evet | evet |
| ResNet-56 vs ViT-B-16 | -21.2 | +13.2 | -7.04 | -20.24 | [-33.10; +2.50] | evet | evet |
| ResNet-164 vs ViT-B-16 | -18.6 | +17.0 | -1.43 | -18.43 | [-31.41; +1.59] | evet | evet |
| ResNet-56 vs ViT-L-16 | -22.4 | +5.4 | -15.11 | -20.51 | [-30.26; +4.14] | evet | evet |
| ResNet-164 vs ViT-L-16 | -19.8 | +6.0 | -12.28 | -18.28 | [-27.71; +4.09] | evet | evet |

Yon sayimi: CNN daha guclu kaynak 6/6 cift (ResNet ailesi, ViT-B-32/B-16/L-16); ResNet temiz dogrulugu ResNet-56 71.6, ResNet-164 74.2.

- CIFAR-10: bc'de CNN guclu kaynak olan cift 0 (yok); ham ongoruyle isaret donen cift (p=1, merkez) 0. Merkez tahmin r_tc = r_bc; aralik alanlari varsayimsiz sinirlari verir. Aralik sifiri iceriyorsa donus kesin degildir.
- CIFAR-100: bc'de CNN guclu kaynak olan cift 6 (ResNet-56 vs ViT-B-32, ResNet-164 vs ViT-B-32, ResNet-56 vs ViT-B-16, ResNet-164 vs ViT-B-16, ResNet-56 vs ViT-L-16, ResNet-164 vs ViT-L-16); ham ongoruyle isaret donen cift (p=1, merkez) 6. Merkez tahmin r_tc = r_bc; aralik alanlari varsayimsiz sinirlari verir. Aralik sifiri iceriyorsa donus kesin degildir.

### Aile duzeyi kaynak ve hedef etkileri (`results/q1/kaynak_hedef_ayristirma.json`)

| Veri | Aile karsitligi | Toplamsal kaynak farki (CNN-ViT) | Toplamsal hedef farki (ViT-CNN) | Aile-terimli kaynak farki | Aile-terimli hedef farki |
|---|---|---|---|---|---|
| CIFAR-10 | CNN_vs_ViT_hibrit_haric | -25.01 | +2.08 | -10.78 | -12.15 |
| CIFAR-10 | CNN_vs_ViT_hibrit_dahil | -25.05 | -1.92 | -10.82 | -16.14 |
| CIFAR-10 | BiT_vs_ViT | -25.95 | -7.03 | -11.72 | -21.26 |
| CIFAR-10 | ResNet_vs_ViT | -24.06 | +11.18 | -9.84 | -3.05 |
| CIFAR-100 | CNN_vs_ViT_hibrit_haric | -22.77 | +14.74 | -9.43 | +1.39 |
| CIFAR-100 | CNN_vs_ViT_hibrit_dahil | -21.93 | +11.56 | -8.58 | -1.79 |
| CIFAR-100 | BiT_vs_ViT | -23.65 | -0.67 | -10.30 | -14.02 |
| CIFAR-100 | ResNet_vs_ViT | -21.90 | +30.15 | -8.55 | +16.81 |

### Bizim CIFAR-10 cifti uzerinde ayni ozdeslik ongorusu (yaklasim sinamasi)

Kaynak: `results/c1_transfer/c1_transfer_summary.json`. Temiz dogruluk ResNet-18 AT 85.79, ViT-Tiny AT 73.53, fark +12.26 puan. Dort protokol asimetrisi (CNN->ViT eksi ViT->CNN): Unconditioned (raw) +13.57, Target-correct +4.36, Both-correct +8.27, Successful-source +19.37. Gozlenen ham eksi tc +9.21, ham eksi bc +5.31. Kaynak temiz hata: ResNet-18 AT 14.21, ViT-Tiny AT 26.47; Mahmood'da en buyuk kaynak temiz hata CIFAR-10 7.20, CIFAR-100 28.40.

| p | Ham asimetri ongorusu (bc'den, r_tc = r_bc) | Ham asimetri ongorusu (tc'den, tam ozdeslik) | Gozlenen ham asimetri | Yaklasim hatasi (bc'den) | Ongorulen protokol etkisi (ham eksi bc) |
|---|---|---|---|---|---|
| p=1 (ust sinir) | +17.11 | +13.56 | +13.57 | +3.54 | +8.85 |
| p=p_min=0.989014 (ozdeslik_kontrol min) | +16.98 | +13.43 | +13.57 | +3.41 | +8.71 |

Artefaktin notu: Mahmood'a r_tc = r_bc yaklasimiyla uygulanan ongoru bizim veride sinanir (yaklasim_hatasi alani); yaklasim hatasi kaynak temiz hatasiyla buyur, bu yuzden bizim ciftteki hata Mahmood CIFAR-10 icin ust sinir niteligindedir.


## Secim kuralinin asimetriye etkisi

_Kaynak: `results/q1/secim_asimetri_etkisi.json (yorungeler/e3_akolu_v2); results/q1/son_kontrol_noktasi/pair{1,2,3}/havuz_protokoller.json; C1 secilmis kontrol noktasi degerleri: results/c1_transfer/c1_transfer_summary.json (values), results/c1_seeds/c1_seed_summary.json (pairs)`_

### A. Saklanan egitim yorungeleri: secilen epok ve son epok

Yontem (artefakttan): A kolu kayitlari trajectory_id basina epok sirasina dizilir. Asimetri makale konvansiyonuna (CNN->ViT eksi ViT->CNN) cevrilir: ResNet yorungelerinde kayittaki (P->M) - (M->P) isaret degistirir. Yayilim dort protokolde ve uc protokolde (successful_source haric) max-min. Yorunge ici iliski: yayilimin |temiz hata farki|'na EKK egimi ve Pearson r (epok noktalari, cikarim amacli degil, betimsel). Secim baglantisi: E2 (CIFAR-10, 18 hucre + valA/B/C tek kural) ve B8 (CIFAR-100, 9 hucre) izgaralarindaki secilen epok, saklanan en yakin A kolu epoguna eslenir.

Yon notu (artefakttan): CIFAR-10 yorungeleri E2 yeniden egitimleridir (C1 modelleri DEGIL); es model C1 best.pth. Bu nedenle CIFAR-10'da 'son epok' C1 ciftinin son kontrol noktasi degil, ayni tohumlu E2 kosusunun 100. epogudur. CIFAR-100'de yorunge E1 egitiminin kendisidir ve erken durdurmayla biter; son epok = durus epogu.

Dizin notu (artefakttan): e3_akolu (ilk kosum) successful_source'u GEVSEK maskeyle (tc & sa) yazar ve PGD tohumu (yorunge, epok)'a bagli degildir; e3_akolu_v2 siki maske ve ck_tohum tasir ve e3_iki_kol_fit.json'un kullandigi dizindir. Ana sonuclar v2'den. Kanonik dizin: `results/q1/e3_akolu_v2`.

Temiz fark = temiz HATA farki, ViT eksi CNN (puan). 'Secilen' = referans secim hucresinin epoku (artefaktta `referans_hucre`), 'en yakin saklanan epok'taki deger; 'Son' = yorungenin son epogu; Delta = son - secilen. Yayilim = dort protokolde max-min asimetri. tc = hedef-dogru asimetri (CNN->ViT eksi ViT->CNN). Saklanan epoklar yaklasik 10 epok aralikli; ara deger kestirimi yapilmamistir.

| Yorunge | Secilen (saklanan) -> son epok | Temiz fark: secilen / son / Delta | Yayilim (dort protokol): secilen / son / Delta | tc asimetri: secilen / son / Delta | bc asimetri: secilen / son / Delta |
|---|---|---|---|---|---|
| A_c100_rn18_s1001 | 31 -> 52 | 22.46 / 20.51 / -1.95 | 15.57 / 13.43 / -2.14 | 3.48 / 5.09 / +1.61 | 10.82 / 11.06 / +0.24 |
| A_c100_rn18_s1002 | 21 -> 44 | 21.68 / 19.06 / -2.62 | 15.17 / 12.58 / -2.59 | 3.33 / 4.74 / +1.41 | 8.89 / 9.74 / +0.85 |
| A_c100_rn18_s1003 | 51 -> 69 | 18.91 / 18.15 / -0.76 | 13.40 / 12.62 / -0.79 | 3.10 / 3.36 / +0.27 | 8.46 / 8.21 / -0.26 |
| A_c100_vit_s2001 | 11 -> 27 | 20.90 / 21.15 / +0.25 | 13.57 / 14.68 / +1.11 | 5.10 / 4.34 / -0.76 | 11.50 / 10.04 / -1.46 |
| A_c100_vit_s2002 | 11 -> 31 | 21.17 / 21.62 / +0.45 | 14.10 / 14.76 / +0.66 | 4.43 / 4.75 / +0.32 | 10.27 / 10.03 / -0.25 |
| A_c100_vit_s2003 | 21 -> 40 | 19.13 / 19.93 / +0.80 | 12.64 / 13.41 / +0.77 | 5.29 / 5.15 / -0.14 | 10.28 / 10.07 / -0.21 |
| A_c10_rn18_s1001 | 61 -> 100 | 12.65 / 11.83 / -0.82 | 12.57 / 12.36 / -0.22 | 3.76 / 3.71 / -0.05 | 8.24 / 7.62 / -0.62 |
| A_c10_rn18_s1002 | 51 -> 100 | 12.12 / 13.66 / +1.54 | 12.76 / 10.70 / -2.06 | 3.83 / 2.83 / -1.00 | 7.71 / 7.00 / -0.71 |
| A_c10_rn18_s1003 | 41 -> 100 | 12.47 / 13.83 / +1.36 | 13.30 / 10.98 / -2.32 | 3.90 / 2.64 / -1.26 | 8.11 / 6.65 / -1.46 |
| A_c10_vit_s2001 | 31 -> 100 | 12.29 / 12.78 / +0.49 | 13.06 / 14.35 / +1.29 | 5.34 / 8.04 / +2.70 | 8.37 / 10.24 / +1.87 |
| A_c10_vit_s2002 | 21 -> 100 | 11.55 / 12.27 / +0.72 | 14.06 / 13.35 / -0.71 | 5.56 / 7.99 / +2.43 | 8.39 / 9.83 / +1.43 |
| A_c10_vit_s2003 | 31 -> 100 | 10.59 / 12.24 / +1.65 | 13.93 / 13.25 / -0.68 | 5.07 / 7.53 / +2.46 | 8.23 / 9.45 / +1.22 |

Grup ozeti (yorunge = bir egitim tohumu; ortalama$\pm$SD ddof=1, ardindan en kucuk; en buyuk), Delta = son - secilen:

| Veri | Taranan model | n yorunge | Temiz fark Delta | Yayilim Delta | tc asimetri Delta | bc asimetri Delta | Temiz fark: secilen araligi -> son araligi |
|---|---|---|---|---|---|---|---|
| cifar100 | ResNet-18 | 3 | -1.78$\pm$0.94 (-2.62; -0.76) | -1.84$\pm$0.94 (-2.59; -0.79) | +1.09$\pm$0.73 (+0.27; +1.61) | +0.28$\pm$0.55 (-0.26; +0.85) | 18.91; 22.46 -> 18.15; 20.51 |
| cifar100 | ViT-Tiny | 3 | +0.50$\pm$0.28 (+0.25; +0.80) | +0.84$\pm$0.24 (+0.66; +1.11) | -0.19$\pm$0.55 (-0.76; +0.32) | -0.64$\pm$0.71 (-1.46; -0.21) | 19.13; 21.17 -> 19.93; 21.62 |
| cifar10 | ResNet-18 | 3 | +0.69$\pm$1.31 (-0.82; +1.54) | -1.53$\pm$1.15 (-2.32; -0.22) | -0.77$\pm$0.64 (-1.26; -0.05) | -0.93$\pm$0.46 (-1.46; -0.62) | 12.12; 12.65 -> 11.83; 13.83 |
| cifar10 | ViT-Tiny | 3 | +0.95$\pm$0.61 (+0.49; +1.65) | -0.03$\pm$1.15 (-0.71; +1.29) | +2.53$\pm$0.15 (+2.43; +2.70) | +1.51$\pm$0.33 (+1.22; +1.87) | 10.59; 12.29 -> 12.24; 12.78 |

Secim hucreleri arasi aralik (secim izgarasindaki hucrelerin en yakin saklanan epoklari; E2/B8 izgaralari), en kucuk; en buyuk:

| Yorunge | Secim hucresi | Eslesen saklanan epoklar | En buyuk uzaklik (epok) | Yayilim (dort) | Yayilim (uc) | tc asimetri | bc asimetri |
|---|---|---|---|---|---|---|---|
| A_c100_rn18_s1001 | 9 | [11, 21, 31, 41] | 5 | 14.66; 16.22 | 14.66; 16.22 | 3.04; 4.27 | 10.76; 11.69 |
| A_c100_rn18_s1002 | 9 | [21, 44] | 3 | 12.58; 15.17 | 12.58; 15.17 | 3.33; 4.74 | 8.89; 9.74 |
| A_c100_rn18_s1003 | 9 | [11, 21, 51] | 4 | 13.40; 15.48 | 13.40; 15.48 | 2.68; 3.81 | 8.46; 9.90 |
| A_c100_vit_s2001 | 9 | [1, 11] | 4 | 13.57; 18.18 | 13.57; 18.18 | 5.10; 7.87 | 11.50; 13.97 |
| A_c100_vit_s2002 | 9 | [1, 11] | 4 | 14.10; 20.29 | 14.10; 20.29 | 4.43; 6.10 | 10.27; 13.11 |
| A_c100_vit_s2003 | 9 | [1, 21] | 5 | 12.64; 15.48 | 12.52; 15.48 | 5.29; 9.42 | 10.28; 15.53 |
| A_c10_rn18_s1001 | 21 | [31, 41, 51, 61, 71, 81] | 5 | 12.57; 13.12 | 8.41; 9.80 | 3.24; 4.66 | 7.49; 8.25 |
| A_c10_rn18_s1002 | 21 | [21, 31, 51] | 3 | 11.53; 12.76 | 8.92; 10.03 | 2.58; 3.83 | 6.56; 7.71 |
| A_c10_rn18_s1003 | 21 | [21, 41, 61] | 4 | 10.73; 13.30 | 9.47; 11.98 | 2.40; 3.90 | 6.77; 8.11 |
| A_c10_vit_s2001 | 21 | [21, 31] | 3 | 13.06; 14.19 | 9.14; 12.42 | 4.46; 5.34 | 8.23; 8.37 |
| A_c10_vit_s2002 | 21 | [21, 31] | 4 | 14.06; 14.48 | 8.38; 8.92 | 4.57; 5.56 | 8.19; 8.39 |
| A_c10_vit_s2003 | 21 | [11, 21, 31] | 5 | 13.93; 14.75 | 7.70; 12.79 | 4.24; 5.12 | 7.84; 9.28 |

Veri kumesi duzeyinde yorunge ozetleri (artefaktin `veri_kumesi_duzeyi` alani; tum epok yorungesi uzerinden; en kucuk; en buyuk, yorunge sayisiyla):

| Veri | Yorunge | Son - ilk yayilim (dort) | Yayilim max-min (dort) | tc asimetri max-min | bc asimetri max-min | Yorunge ici r: yayilim (uc) ~ temiz fark | Yorunge ici r: yayilim (dort) ~ temiz fark |
|---|---|---|---|---|---|---|---|
| cifar100 | 6 | -5.53; -2.07 | 2.69; 6.18 | 1.68; 8.64 | 3.08; 7.42 | 0.312; 0.998 | 0.312; 0.998 |
| cifar10 | 6 | -9.08; +1.61 | 3.85; 10.05 | 3.59; 12.44 | 4.86; 12.90 | 0.762; 1.000 | 0.005; 0.960 |
| svhn | 4 | -29.96; -27.35 | 29.33; 33.02 | 16.24; 23.63 | 15.31; 23.41 | -0.932; 0.980 | 0.803; 0.950 |

- Eksik (SVHN_secim_izgarasi): yok (E7 icin secim izgarasi dosyasi yok)
- Eksik (C1_ViT_2002_epok18_secimi): C1 modellerinin epok yorungesi A kolunda yok; CIFAR-10 A kolu E2 yeniden egitimlerini tarar. C1 secim epoku logs/ altindadir, burada kullanilmadi.
- Eksik (ara_epoklar): A kolu stride ~10; secilen epoklarin tam degeri yok, en yakin saklanan epok kullanildi.

### B. Son kontrol noktasi (`last.pth`) ile C1 secilmis kontrol noktasi, ayni egitim ciftleri

Cift p = egitim cifti p (tohum 100p ResNet-18, 200p ViT-Tiny). Asimetri = ResNet-18 AT -> ViT-Tiny AT eksi ViT-Tiny AT -> ResNet-18 AT (puan). Son kontrol noktasi: ornek bazli kayitlardan, `src/analysis/protokoller.py` (dort protokol, n=10000), WRN-28-10 referansi ayni. C1 secilmis kontrol noktasi (`best.pth`): `c1_transfer_summary.json` CNN_to_ViT ve ViT_to_CNN kosum degerleri (2 ondalikli saklidir), temiz dogruluk `c1_seed_summary.json`. Yayilim (dort) = en buyuk - en kucuk protokol asimetrisi; yayilim (uc) = raw, tc, bc uzerinden. Temiz fark = ResNet-18 AT eksi ViT-Tiny AT.

Son kontrol noktasi (`last.pth`), `results/q1/son_kontrol_noktasi/pair*/havuz_protokoller.json`:

| Cift | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz ResNet-18 | Temiz ViT-Tiny | Temiz fark (R-V) |
|---|---|---|---|---|---|---|---|---|---|
| cift 1 | +11.99 | +4.48 | +7.50 | +17.34 | 12.86 | 7.51 | 86.56 | 76.48 | +10.08 |
| cift 2 | +12.66 | +4.17 | +7.84 | +16.67 | 12.50 | 8.49 | 86.95 | 75.74 | +11.21 |
| cift 3 | +12.79 | +5.27 | +8.58 | +18.44 | 13.17 | 7.52 | 86.48 | 76.13 | +10.35 |
| ort.$\pm$SD | +12.48$\pm$0.43 | +4.64$\pm$0.56 | +7.97$\pm$0.55 | +17.48$\pm$0.90 | 12.84$\pm$0.34 | 7.84$\pm$0.56 | 86.66$\pm$0.25 | 76.12$\pm$0.37 | +10.55$\pm$0.59 |

C1 secilmis kontrol noktasi (`best.pth`), `c1_transfer_summary.json` ve `c1_seed_summary.json`:

| Cift | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz ResNet-18 | Temiz ViT-Tiny | Temiz fark (R-V) |
|---|---|---|---|---|---|---|---|---|---|
| cift 1 | +13.20 | +4.83 | +8.51 | +20.80 | 15.97 | 8.37 | 85.37 | 74.10 | +11.27 |
| cift 2 | +13.69 | +4.28 | +8.05 | +18.91 | 14.63 | 9.41 | 85.94 | 73.47 | +12.47 |
| cift 3 | +13.83 | +3.97 | +8.24 | +18.39 | 14.42 | 9.86 | 86.04 | 73.01 | +13.03 |
| ort.$\pm$SD | +13.57$\pm$0.33 | +4.36$\pm$0.44 | +8.27$\pm$0.23 | +19.37$\pm$1.27 | 15.01$\pm$0.84 | 9.21$\pm$0.76 | 85.78$\pm$0.36 | 73.53$\pm$0.55 | +12.26$\pm$0.90 |

Fark (son kontrol noktasi - C1 secilmis), cift basina:

| Cift | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz ResNet-18 | Temiz ViT-Tiny | Temiz fark (R-V) |
|---|---|---|---|---|---|---|---|---|---|
| cift 1 | -1.21 | -0.35 | -1.01 | -3.46 | -3.11 | -0.86 | +1.19 | +2.38 | -1.19 |
| cift 2 | -1.03 | -0.11 | -0.21 | -2.24 | -2.13 | -0.92 | +1.01 | +2.27 | -1.26 |
| cift 3 | -1.04 | +1.30 | +0.34 | +0.05 | -1.25 | -2.34 | +0.44 | +3.12 | -2.68 |
| ort.$\pm$SD | -1.09$\pm$0.10 | +0.28$\pm$0.89 | -0.30$\pm$0.68 | -1.88$\pm$1.78 | -2.16$\pm$0.93 | -1.37$\pm$0.83 | +0.88$\pm$0.39 | +2.59$\pm$0.46 | -1.71$\pm$0.84 |

Fark ozeti (son - C1 secilmis; ortalama$\pm$SD, parantezde en kucuk ve en buyuk cift degeri): yayilim (dort) -2.16$\pm$0.93 (-3.11; -1.25); yayilim (uc) -1.37$\pm$0.83 (-2.34; -0.86); temiz fark -1.71$\pm$0.84 (-2.68; -1.19); tc asimetri +0.28$\pm$0.89 (-0.35; +1.30). Aralik (en kucuk; en buyuk): temiz fark son 10.08; 11.21, C1 secilmis 11.27; 13.03; yayilim (dort) son 12.50; 13.17, C1 secilmis 14.42; 15.97; tc asimetri son +4.17; +5.27, C1 secilmis +3.97; +4.83.

Son kontrol noktasi, ayni cift, yon bazinda p ve oncul p ozeti:

| Cift | Yon | p en kucuk | p en buyuk | p=1 artigi, en buyuk mutlak (puan) | p=1 artigi, ortalama mutlak (puan) |
|---|---|---|---|---|---|
| cift 1 | 6 | 0.9915 | 1.0000 | 0.20 | 0.07 |
| cift 2 | 6 | 0.9959 | 1.0000 | 0.10 | 0.04 |
| cift 3 | 6 | 0.9946 | 1.0000 | 0.13 | 0.05 |

Son kontrol noktasi, WRN-28-10 referansli ciftler (cift basina, puan):

| Cift | Yon | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz fark (mutlak) |
|---|---|---|---|---|---|---|---|---|
| cift 1 | ResNet18_AT -> WRN_28_10 eksi ters | -10.93 | -9.66 | -10.47 | -46.09 | 36.43 | 1.27 | 2.92 |
| cift 1 | ViT_Tiny_AT -> WRN_28_10 eksi ters | -20.29 | -11.09 | -12.65 | -41.12 | 30.03 | 9.20 | 13.00 |
| cift 2 | ResNet18_AT -> WRN_28_10 eksi ters | -10.32 | -9.32 | -9.80 | -45.64 | 36.32 | 1.00 | 2.53 |
| cift 2 | ViT_Tiny_AT -> WRN_28_10 eksi ters | -20.32 | -10.38 | -12.21 | -42.70 | 32.32 | 9.94 | 13.74 |
| cift 3 | ResNet18_AT -> WRN_28_10 eksi ters | -10.73 | -9.37 | -10.19 | -44.44 | 35.07 | 1.36 | 3.00 |
| cift 3 | ViT_Tiny_AT -> WRN_28_10 eksi ters | -20.10 | -10.45 | -12.53 | -39.89 | 29.44 | 9.65 | 13.35 |


## Standart egitimli hedeflerde oncul p (temiz ciftler)

_Kaynak: `results/q1/temiz_ciftler/pair{1,2,3}/havuz_protokoller.json`_

Ucu de standart (cekismeli olmayan) egitimli modellerdir: ResNet-18 ve ViT-Tiny temiz egitim cifti (tohum 100p / 200p), Standard WRN-28-10 (RobustBench `Standard`, her ciftte ayni model). Saldiri PGD-10, Linf, eps = 8/255, n = 10000. p = P(cekismeli ornek yanlis, hedef temizde yanlis iken); p=1 artigi = gozlenen ham oran eksi p = 1 varsayimiyla ozdeslik ongorusu (puan). Tohum 42. Kosegen yonler (kaynak = hedef) dahil degildir.

| Model | cift 1 | cift 2 | cift 3 | ort.$\pm$SD |
|---|---|---|---|---|
| ResNet18_clean | 95.09 | 95.26 | 95.40 | 95.25$\pm$0.16 |
| ViT_Tiny_clean | 79.40 | 80.51 | 80.36 | 80.09$\pm$0.60 |
| Standard_WRN28_10 | 94.78 | 94.78 | 94.78 | 94.78$\pm$0.00 |

### Yon basina p ve p=1 artigi (uc cift)

| Yon (kaynak->hedef) | Hedefte temiz yanlis sayisi (cift 1 / 2 / 3) | p (cift 1 / 2 / 3) | p ort.$\pm$SD | p en kucuk; en buyuk | p=1 artigi (puan) | Artik ort.$\pm$SD | En buyuk mutlak artik |
|---|---|---|---|---|---|---|---|
| ResNet18_clean->ViT_Tiny_clean | 2060 / 1949 / 1964 | 0.9233 / 0.9338 / 0.9231 | 0.9267$\pm$0.0061 | 0.9231; 0.9338 | -1.58 / -1.29 / -1.51 | -1.46$\pm$0.15 | 1.58 |
| ResNet18_clean->Standard_WRN28_10 | 522 / 522 / 522 | 0.9923 / 0.9943 / 0.9962 | 0.9943$\pm$0.0019 | 0.9923; 0.9962 | -0.04 / -0.03 / -0.02 | -0.03$\pm$0.01 | 0.04 |
| ViT_Tiny_clean->ResNet18_clean | 491 / 474 / 460 | 0.8961 / 0.9114 / 0.9087 | 0.9054$\pm$0.0081 | 0.8961; 0.9114 | -0.51 / -0.42 / -0.42 | -0.45$\pm$0.05 | 0.51 |
| ViT_Tiny_clean->Standard_WRN28_10 | 522 / 522 / 522 | 0.8889 / 0.8774 / 0.8927 | 0.8863$\pm$0.0080 | 0.8774; 0.8927 | -0.58 / -0.64 / -0.56 | -0.59$\pm$0.04 | 0.64 |
| Standard_WRN28_10->ResNet18_clean | 491 / 474 / 460 | 1.0000 / 1.0000 / 0.9978 | 0.9993$\pm$0.0013 | 0.9978; 1.0000 | +0.00 / +0.00 / -0.01 | -0.00$\pm$0.01 | 0.01 |
| Standard_WRN28_10->ViT_Tiny_clean | 2060 / 1949 / 1964 | 0.9330 / 0.9338 / 0.9231 | 0.9300$\pm$0.0060 | 0.9231; 0.9338 | -1.38 / -1.29 / -1.51 | -1.39$\pm$0.11 | 1.51 |

### Hedef turune gore p ve p=1 artigi (uc cift x kaynaklar, 6 deger / hedef)

| Hedef | Deger sayisi | p en kucuk | p en buyuk | p ortalama | Artik en kucuk (puan) | Artik en buyuk (puan) | En buyuk mutlak artik | Ortalama mutlak artik |
|---|---|---|---|---|---|---|---|---|
| ViT_Tiny_clean | 6 | 0.9231 | 0.9338 | 0.9284 | -1.58 | -1.29 | 1.58 | 1.43 |
| Standard_WRN28_10 | 6 | 0.8774 | 0.9962 | 0.9403 | -0.64 | -0.02 | 0.64 | 0.31 |
| ResNet18_clean | 6 | 0.8961 | 1.0000 | 0.9523 | -0.51 | +0.00 | 0.51 | 0.23 |
| Tum yonler | 18 | 0.8774 | 1.0000 | 0.9403 | -1.58 | +0.00 | 1.58 | 0.66 |

Artefaktin `oncul_p_ozeti` alanlariyla (hedef bazinda p_min) tutarlilik: en buyuk sapma 0.00e+00; cift basina `ozdeslik_artigi_mutlak_max_puan`: cift 1 1.58, cift 2 1.29, cift 3 1.51.

### Cift basina dort protokol asimetrisi ve yayilim

Asimetri = ilk model -> ikinci model eksi ters yon (puan); yayilim = en buyuk - en kucuk protokol asimetrisi (dort ve uc: raw, tc, bc). Temiz fark mutlak.

| Cift | Yon | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz fark (mutlak) | Isaret donuyor (dort) |
|---|---|---|---|---|---|---|---|---|---|
| cift 1 | ResNet18_clean -> ViT_Tiny_clean | +10.09 | -3.56 | -1.30 | -1.32 | 13.65 | 13.65 | 15.69 | evet |
| cift 1 | ResNet18_clean -> Standard_WRN28_10 | -3.35 | -3.54 | -3.51 | -3.50 | 0.19 | 0.19 | 0.31 | hayir |
| cift 1 | ViT_Tiny_clean -> Standard_WRN28_10 | -8.45 | +5.33 | +3.37 | +3.39 | 13.78 | 13.78 | 15.38 | evet |
| cift 2 | ResNet18_clean -> ViT_Tiny_clean | +7.81 | -5.22 | -3.02 | -3.02 | 13.03 | 13.03 | 14.75 | evet |
| cift 2 | ResNet18_clean -> Standard_WRN28_10 | -2.96 | -3.18 | -3.10 | -3.07 | 0.22 | 0.22 | 0.48 | hayir |
| cift 2 | ViT_Tiny_clean -> Standard_WRN28_10 | -6.51 | +6.27 | +4.16 | +4.17 | 12.78 | 12.78 | 14.27 | evet |
| cift 3 | ResNet18_clean -> ViT_Tiny_clean | +8.39 | -4.69 | -2.40 | -2.40 | 13.08 | 13.08 | 15.04 | evet |
| cift 3 | ResNet18_clean -> Standard_WRN28_10 | -1.08 | -1.24 | -1.14 | -1.06 | 0.18 | 0.16 | 0.62 | hayir |
| cift 3 | ViT_Tiny_clean -> Standard_WRN28_10 | -6.36 | +6.34 | +4.21 | +4.21 | 12.70 | 12.70 | 14.42 | evet |

### Cift turune gore ozet (uc cift, ortalama$\pm$SD)

| Cift turu | Temiz fark (cift 1 / 2 / 3) | Temiz fark ort.$\pm$SD | Yayilim dort (1 / 2 / 3) | Yayilim dort ort.$\pm$SD | Yayilim uc (1 / 2 / 3) | Yayilim uc ort.$\pm$SD | Isaret donen cift (dort protokol) |
|---|---|---|---|---|---|---|---|
| ResNet18_clean / ViT_Tiny_clean | 15.69 / 14.75 / 15.04 | 15.16$\pm$0.48 | 13.65 / 13.03 / 13.08 | 13.25$\pm$0.34 | 13.65 / 13.03 / 13.08 | 13.25$\pm$0.34 | 3/3 |
| ResNet18_clean / Standard_WRN28_10 | 0.31 / 0.48 / 0.62 | 0.47$\pm$0.16 | 0.19 / 0.22 / 0.18 | 0.19$\pm$0.02 | 0.19 / 0.22 / 0.16 | 0.19$\pm$0.03 | 0/3 |
| ViT_Tiny_clean / Standard_WRN28_10 | 15.38 / 14.27 / 14.42 | 14.69$\pm$0.60 | 13.78 / 12.78 / 12.70 | 13.08$\pm$0.60 | 13.78 / 12.78 / 12.70 | 13.08$\pm$0.60 | 3/3 |

ResNet18_clean ve Standard_WRN28_10 cifti (eslenmis temiz dogruluk): temiz fark 0.31 / 0.48 / 0.62 puan, yayilim (dort) 0.19 / 0.22 / 0.18 puan, yayilim (uc) 0.19 / 0.22 / 0.16 puan (cift 1 / 2 / 3). Bu ciftte dort protokol asimetrisi (raw / tc / bc / ss): -3.35 / -3.54 / -3.51 / -3.50; -2.96 / -3.18 / -3.10 / -3.07; -1.08 / -1.24 / -1.14 / -1.06 (cift basina).

### Cift basina yayilim ~ temiz fark egimi (3 nokta) ve toplamsal etkiler

| Cift | Egim (dort) | R2 (dort) | Egim (uc) | R2 (uc) | Nokta |
|---|---|---|---|---|---|
| cift 1 | +0.888 | 0.9993 | +0.888 | 0.9993 | 3 |
| cift 2 | +0.904 | 0.9998 | +0.904 | 0.9998 | 3 |
| cift 3 | +0.900 | 0.9999 | +0.902 | 0.9999 | 3 |

Her egim YALNIZ 3 noktadan (uc cift) hesaplanir; model bootstrap GA'si bu klasorlerde bos kalir (artefakt notu: ciftler modelleri paylasir; GA model birak-tut bootstrap'indan, cift sayisi serbestlik derecesi DEGILDIR). Yayilim ~ temiz fark iliskisi icin tum-cift egimi 'Yayilim - temiz fark iliskisi (tum ciftler)' bolumundedir.

| Cift | Model | Kaynak etkisi | Hedef etkisi |
|---|---|---|---|
| cift 1 | ResNet18_clean | +23.39 | +25.75 |
| cift 1 | ViT_Tiny_clean | -48.27 | -51.23 |
| cift 1 | Standard_WRN28_10 | +24.88 | +25.48 |
| cift 1 | (uydurma) | R2 0.9994 | en buyuk mutlak artik 0.88; mu 34.25 |
| cift 2 | ResNet18_clean | +21.64 | +24.44 |
| cift 2 | ViT_Tiny_clean | -45.45 | -49.28 |
| cift 2 | Standard_WRN28_10 | +23.81 | +24.84 |
| cift 2 | (uydurma) | R2 0.9996 | en buyuk mutlak artik 0.70; mu 34.36 |
| cift 3 | ResNet18_clean | +22.46 | +24.43 |
| cift 3 | ViT_Tiny_clean | -46.33 | -50.01 |
| cift 3 | Standard_WRN28_10 | +23.88 | +25.58 |
| cift 3 | (uydurma) | R2 0.9998 | en buyuk mutlak artik 0.48; mu 34.28 |


## RobustBench havuzu (CIFAR-10, egitim yok)

_Kaynak: `results/q1/havuz_cifar10/havuz_protokoller.json`_

Model sayisi 8; tohum 42; PGD-10, Linf, eps = 8/255, n = 10000, ornek bazli kayit. Uretim: 2026-10-04T15:40:03+00:00. p ve p=1 artigi tanimlari 'Standart egitimli hedeflerde oncul p' bolumundeki gibidir.

### Modeller, temiz dogruluklar ve hedef bazinda p

| Model | Temiz dogruluk (%) | p en kucuk (bu hedefe giden yonler) | p en buyuk |
|---|---|---|---|
| ResNet18_AT | 85.37 | 0.9911 | 0.9993 |
| ViT_Tiny_AT | 74.10 | 0.9919 | 0.9981 |
| Standard_WRN28_10 | 94.78 | 0.9330 | 0.9962 |
| Wong2020_PRN18 | 83.34 | 0.9892 | 0.9994 |
| Engstrom2019_RN50 | 87.03 | 0.9846 | 1.0000 |
| Carmon2019_WRN28_10 | 89.69 | 0.9884 | 1.0000 |
| Debenedetti2022_XCiT_S12 | 90.06 | 0.9940 | 1.0000 |
| Gowal2020_WRN28_10 | 89.48 | 0.9895 | 1.0000 |

Tum yonler (kosegen haric, n = 56): p en kucuk 0.9330, p en buyuk 1.0000; p=1 artigi en buyuk mutlak 0.35 puan, ortalama mutlak 0.06 puan.

Yonlu kayitlardan yeniden hesap: p 0.9330; 1.0000, artik en kucuk -0.35, en buyuk +0.00, ortalama mutlak 0.06 puan (yon sayisi 56) (artefaktin ozetiyle UYUMLU).

### Cift basina dort protokol asimetrisi, yayilim ve temiz fark

Asimetri = ilk model -> ikinci model eksi ters yon (puan). Temiz fark mutlak (puan).

| Cift | raw | tc | bc | ss | Yayilim (dort) | Yayilim (uc) | Temiz fark (mutlak) | Isaret donuyor (dort) |
|---|---|---|---|---|---|---|---|---|
| ResNet18_AT / ViT_Tiny_AT | +13.19 | +4.81 | +8.49 | +21.01 | 16.20 | 8.38 | 11.27 | hayir |
| ResNet18_AT / Standard_WRN28_10 | +26.74 | +37.83 | +32.99 | +52.66 | 25.92 | 11.09 | 9.41 | hayir |
| ResNet18_AT / Wong2020_PRN18 | -1.21 | -3.26 | -1.95 | -7.54 | 6.33 | 2.05 | 2.03 | hayir |
| ResNet18_AT / Engstrom2019_RN50 | -6.29 | -5.76 | -6.95 | -23.26 | 17.50 | 1.20 | 1.66 | hayir |
| ResNet18_AT / Carmon2019_WRN28_10 | -10.89 | -8.40 | -10.73 | -41.24 | 32.83 | 2.49 | 4.32 | hayir |
| ResNet18_AT / Debenedetti2022_XCiT_S12 | -11.84 | -9.15 | -11.32 | -38.56 | 29.41 | 2.69 | 4.69 | hayir |
| ResNet18_AT / Gowal2020_WRN28_10 | -11.22 | -8.94 | -10.58 | -45.64 | 36.70 | 2.28 | 4.11 | hayir |
| ViT_Tiny_AT / Standard_WRN28_10 | -6.72 | +14.53 | +9.83 | +14.81 | 21.53 | 21.25 | 20.68 | evet |
| ViT_Tiny_AT / Wong2020_PRN18 | -12.53 | -6.39 | -9.31 | -24.60 | 18.20 | 6.14 | 9.24 | hayir |
| ViT_Tiny_AT / Engstrom2019_RN50 | -16.68 | -7.15 | -10.66 | -27.97 | 20.82 | 9.53 | 12.93 | hayir |
| ViT_Tiny_AT / Carmon2019_WRN28_10 | -21.21 | -9.53 | -12.72 | -39.65 | 30.12 | 11.68 | 15.59 | hayir |
| ViT_Tiny_AT / Debenedetti2022_XCiT_S12 | -22.40 | -10.87 | -14.45 | -41.16 | 30.29 | 11.53 | 15.96 | hayir |
| ViT_Tiny_AT / Gowal2020_WRN28_10 | -21.20 | -9.69 | -12.57 | -42.04 | 32.35 | 11.51 | 15.38 | hayir |
| Standard_WRN28_10 / Wong2020_PRN18 | -14.12 | -26.78 | -21.82 | -37.48 | 23.36 | 12.66 | 11.44 | hayir |
| Standard_WRN28_10 / Engstrom2019_RN50 | -15.66 | -24.54 | -20.42 | -38.66 | 23.00 | 8.88 | 7.75 | hayir |
| Standard_WRN28_10 / Carmon2019_WRN28_10 | -17.05 | -23.31 | -19.73 | -46.91 | 29.86 | 6.26 | 5.09 | hayir |
| Standard_WRN28_10 / Debenedetti2022_XCiT_S12 | -17.77 | -23.70 | -20.11 | -45.26 | 27.49 | 5.93 | 4.72 | hayir |
| Standard_WRN28_10 / Gowal2020_WRN28_10 | -16.86 | -23.27 | -19.30 | -50.73 | 33.87 | 6.41 | 5.30 | hayir |
| Wong2020_PRN18 / Engstrom2019_RN50 | -5.69 | -3.31 | -5.78 | -18.14 | 14.83 | 2.47 | 3.69 | hayir |
| Wong2020_PRN18 / Carmon2019_WRN28_10 | -10.51 | -6.09 | -9.25 | -36.68 | 30.58 | 4.42 | 6.35 | hayir |
| Wong2020_PRN18 / Debenedetti2022_XCiT_S12 | -10.72 | -6.09 | -9.48 | -33.41 | 27.33 | 4.63 | 6.72 | hayir |
| Wong2020_PRN18 / Gowal2020_WRN28_10 | -10.83 | -6.64 | -9.06 | -40.31 | 33.67 | 4.19 | 6.14 | hayir |
| Engstrom2019_RN50 / Carmon2019_WRN28_10 | -5.85 | -4.20 | -5.49 | -25.44 | 21.25 | 1.65 | 2.66 | hayir |
| Engstrom2019_RN50 / Debenedetti2022_XCiT_S12 | -6.07 | -4.05 | -5.35 | -20.32 | 16.27 | 2.02 | 3.03 | hayir |
| Engstrom2019_RN50 / Gowal2020_WRN28_10 | -6.76 | -5.40 | -6.19 | -31.31 | 25.91 | 1.36 | 2.45 | hayir |
| Carmon2019_WRN28_10 / Debenedetti2022_XCiT_S12 | +0.34 | +0.72 | +0.75 | +6.51 | 6.17 | 0.41 | 0.37 | hayir |
| Carmon2019_WRN28_10 / Gowal2020_WRN28_10 | -1.12 | -1.44 | -1.22 | -10.15 | 9.03 | 0.32 | 0.21 | hayir |
| Debenedetti2022_XCiT_S12 / Gowal2020_WRN28_10 | -1.50 | -2.21 | -1.68 | -14.23 | 12.73 | 0.71 | 0.58 | hayir |

Cift sayisi 28; dort protokolde isaret donen cift 1/28.

### Toplamsal kaynak ve hedef etkileri (hedef-dogru oranlar, kosegen haric)

mu = 16.96, R2 = 0.8955, en buyuk mutlak artik 11.95, artik RMS 2.52, hucre 56.

| Model | Kaynak etkisi | Hedef etkisi |
|---|---|---|
| ResNet18_AT | +3.65 | +2.76 |
| ViT_Tiny_AT | -4.87 | -0.63 |
| Standard_WRN28_10 | -14.53 | +7.21 |
| Wong2020_PRN18 | +3.40 | +1.62 |
| Engstrom2019_RN50 | +3.25 | -0.14 |
| Carmon2019_WRN28_10 | +3.10 | -3.25 |
| Debenedetti2022_XCiT_S12 | +3.06 | -3.31 |
| Gowal2020_WRN28_10 | +2.94 | -4.26 |

### Yayilim ~ temiz fark egimi (model birak-tut bootstrap, B asagida)

| Yayilim | Egim | Kesisim | R2 | Pearson r | Cift | Egim %95 GA (model bootstrap) | Gecerli bootstrap ornegi |
|---|---|---|---|---|---|---|---|
| Dort protokol | +0.559 | +19.47 | 0.1226 | 0.3501 | 28 | [-0.205; +4.582] | 1998 |
| Uc protokol (raw, tc, bc) | +0.872 | -0.17 | 0.8908 | 0.9438 | 28 | [+0.534; +1.274] | 2000 |

GA, modeller (cift degil) uzerinden birak-tut bootstrap'tan gelir; cift sayisi serbestlik derecesi DEGILDIR (artefakt notu: ciftler modelleri paylasir; GA model birak-tut bootstrap'indan, cift sayisi serbestlik derecesi DEGILDIR).


## Yayilim - temiz fark iliskisi (tum ciftler)

_Kaynak: `results/q1/fig_yayilim_temiz_fark_veri.json`_

Her nokta bir yonsuz model cifti: |temiz dogruluk farki| ve protokol yayilimi (puan). Asimetri = ilk model eksi ikinci model yonu farki. Uretim: 2026-10-04T15:43:37+00:00. Nokta sayisi: 60; grup sayisi 8.

### Grup basina nokta sayisi ve aralik (puan)

| Grup | Nokta | Temiz fark mutlak (en kucuk; en buyuk) | Yayilim dort (en kucuk; en buyuk) | Yayilim uc (en kucuk; en buyuk) |
|---|---|---|---|---|
| CIFAR-10 L2, AT cifti | 3 | 11.27; 13.03 | 10.02; 11.62 | 9.99; 11.62 |
| CIFAR-10 Linf, AT cifti | 3 | 11.27; 13.03 | 14.42; 15.97 | 8.37; 9.86 |
| CIFAR-10 Linf, RobustBench havuzu | 25 | 0.21; 20.68 | 6.17; 33.87 | 0.32; 21.25 |
| CIFAR-10 Linf, WRN-28-10 referansiyla | 6 | 3.43; 16.47 | 29.79; 36.41 | 1.70; 12.50 |
| CIFAR-10 Linf, son kontrol noktasi | 9 | 2.53; 13.74 | 12.50; 36.43 | 1.00; 9.94 |
| CIFAR-10 Linf, standart egitimli modeller | 9 | 0.31; 15.69 | 0.18; 13.78 | 0.16; 13.78 |
| CIFAR-100 Linf, AT cifti | 3 | 18.61; 22.30 | 12.44; 15.01 | 11.69; 15.01 |
| SVHN Linf, AT cifti | 2 | 1.74; 1.94 | 3.26; 4.14 | 1.30; 1.49 |
| Tum noktalar | 60 | 0.21; 22.30 | 0.18; 36.43 | 0.16; 21.25 |

Ortusme kontrolu: havuzdaki ResNet18_AT / ViT_Tiny_AT / Gowal2020_WRN28_10 temiz dogruluklari (85.37 / 74.10 / 89.48) `c1_seed_summary.json` cift 1 ve `wrn_eval_summary.json` ile AYNI (ayni kontrol noktalari); bu uc modelden olusan 3 havuz cifti, C1 cift 1'in (ayri saldiri kosusuyla yeniden olculmus) ayni model cifti noktalariyla ortusur; tum-cift veri setinde (fig_yayilim_temiz_fark_veri.py) bu uc cift havuz grubundan CIKARILIR, yalniz 'AT cifti' / 'WRN-28-10 referansiyla' gruplarinda sayilir (havuz grubunda 25 nokta kalir).

### Egimler (yayilim ~ temiz fark, OLS; nokta = yonsuz model cifti)

| Yayilim | Egim | Kesisim | Pearson r | Spearman rho | Nokta | Grup-birak egimleri (en kucuk; en buyuk) |
|---|---|---|---|---|---|---|
| Dort protokol | +0.092 | +19.48 | 0.0532 | 0.1284 | 60 | -0.015; +0.246 |
| Uc protokol (raw, tc, bc) | +0.796 | -0.01 | 0.9571 | 0.9618 | 60 | +0.767; +0.855 |

Grup-birak egimleri, Dort protokol:

| Birakilan grup | Egim |
|---|---|
| CIFAR-10 L2, AT cifti | +0.138 |
| CIFAR-10 Linf, AT cifti | +0.120 |
| CIFAR-10 Linf, RobustBench havuzu | +0.023 |
| CIFAR-10 Linf, WRN-28-10 referansiyla | +0.097 |
| CIFAR-10 Linf, son kontrol noktasi | +0.188 |
| CIFAR-10 Linf, standart egitimli modeller | -0.010 |
| CIFAR-100 Linf, AT cifti | +0.246 |
| SVHN Linf, AT cifti | -0.015 |

Not (artefakttan): ciftler modelleri ve kosulari paylasir; n_cift serbestlik derecesi DEGILDIR, grup-birak egimleri duyarlilik icindir

Grup-birak egimleri, Uc protokol:

| Birakilan grup | Egim |
|---|---|
| CIFAR-10 L2, AT cifti | +0.791 |
| CIFAR-10 Linf, AT cifti | +0.799 |
| CIFAR-10 Linf, RobustBench havuzu | +0.782 |
| CIFAR-10 Linf, WRN-28-10 referansiyla | +0.796 |
| CIFAR-10 Linf, son kontrol noktasi | +0.795 |
| CIFAR-10 Linf, standart egitimli modeller | +0.767 |
| CIFAR-100 Linf, AT cifti | +0.855 |
| SVHN Linf, AT cifti | +0.796 |

Not (artefakttan): ciftler modelleri ve kosulari paylasir; n_cift serbestlik derecesi DEGILDIR, grup-birak egimleri duyarlilik icindir

### Ozdeslik paritesi (p=1 yaklasikligi)

n = 60 nokta; ozdeslik-ongorulu ile olculen ham eksi tc farki arasinda mutlak sapma en buyuk 1.09 puan, ortalama 0.13 puan; Pearson r = 0.9996. Not (artefakttan): p=1 yaklasikligi; sapma = e_B(1-p_AB) - e_A(1-p_BA) terimidir.

Uc-protokol yayilimi = |ham - tc| asimetri farki (1e-9 icinde): 57/60 nokta. Not (artefakttan): uc-protokol yayilimi, bc arada kaldiginda |raw-tc| asimetri farkina esittir (hukum M1).

Kaynak notu: nokta listesi 17 artefaktin ozetinden toplanir (yollar ve SHA-256 ozetleri artefaktin `kaynaklar` alanindadir).


## Uc-protokol egimi, SVHN dahil

_Kaynak: `results/q1/e3_uc_protokol_svhnli_fit.json`_

Yontem (artefakttan): x = x_temiz_hata_farki (puan), y = asimetrinin raw/tc/bc uzerinden max-min yayilimi (successful_source haric); EKK egimi; GA kume bootstrap (8 kume, B=10.000, tohum 42, q1_e3_asimetri.py ile ayni yordam). Dort protokol ve SVHN-haric uydurmalar saklanan artefaktlara karsi gerileme kontroludur. Makaledeki ifadenin kaynagi (artefakttan): makale +0.470 [+0.361, +0.665] diyor; bu dosya o sayinin yeniden uretilip uretilmedigini gosterir. Uretim: 2026-10-04T15:24:33.935750+00:00.

| Uydurma | Egim | %95 GA (kume bootstrap) | Kesisim | Pearson r | Nokta | Kume | GA sifiri iceriyor mu | Atlanan bootstrap | y araligi (en kucuk; en buyuk) |
|---|---|---|---|---|---|---|---|---|---|
| Uc protokol (raw, tc, bc), SVHN dahil | +0.4697 | [+0.3606; +0.6649] | +2.51 | 0.8661 | 20 | 8 | hayir | 0 | 1.31; 15.01 |
| Dort protokol, SVHN dahil | -0.1331 | [-0.5700; +0.4686] | +24.26 | -0.1050 | 20 | 8 | evet | 0 | 3.26; 36.41 |
| Yalniz ozdeslik terimi (mutlak (ham - tc) ongorusu), SVHN dahil | +0.4712 | [+0.3615; +0.6666] | +2.51 | 0.8656 | 20 | 8 | hayir | 0 | 1.33; 15.05 |
| Uc protokol, SVHN haric (gerileme kontrolu) | +0.4315 | [+0.3327; +0.6330] | +3.20 | 0.8402 | 18 | 6 | hayir | 0 | 1.70; 15.01 |

### Saklanan artefaktlara karsi yeniden uretim

| Kontrol | Saklanan egim | Saklanan GA | Yeniden egim | Yeniden GA | Egim farki |
|---|---|---|---|---|---|
| Dort protokol (e3_asimetri_fit_svhnli.json) | -0.1331 | [-0.5700; +0.4686] | -0.1331 | [-0.5700; +0.4686] | 7.0e-07 |
| Uc protokol, SVHN haric (e3_iki_kol_fit.json B kolu) | +0.4315 | [+0.3327; +0.6330] | +0.4315 | [+0.3327; +0.6330] | 0.0e+00 |

### Uc-protokol yayilimi = mutlak (ham - tc) esitligi

Esit cift sayisi: 19/20 (yon cifti); mutlak (ham - tc) ile ozdeslik ongorusu arasinda en buyuk sapma 0.16 puan.

- Esitligin bozuldugu cift: c100_pair3, ResNet18_AT->WRN_28_10; temiz fark 0.96, yayilim (uc) 4.4138, mutlak (ham - tc) 4.3956, ozdeslik ongorusu 4.4056; neden (artefakttan): both_correct disarida


## Dikkat entropisi TOST ve devrilen/devrilmeyen kosinus

_Kaynak: `results/c1_c4/c4_entropy_tost.json`_

Yontem (artefakttan): Katman basina kosu duzeyi TOST (n=3, df=2), marj +-0.05 nat (onceden sabit), p_TOST = max(iki tek yonlu p); %90 GA'nin marj icinde olmasi esdeger kontrol. Kosinus: son blok (block11.mlp ViT, layer4.1 ResNet), kosu ortalamalarinin ortalamasi ve kosu duzeyi eslestirilmis t. Birim: kosu (egitim cifti), n = 3; ornek bazli entropi saklanmadigi icin ornek duzeyi test YOK. Uretim: 2026-10-04T15:25:20.833542+00:00.

Marj +-0.05 nat; katman sayisi 12; esdeger katman sayisi (marj 0.05) 12/12; en buyuk TOST p = 0.00611, artefakt katman indeksi 9 (0-tabanli; foyun diger bolumlerindeki 1-tabanli numara: katman 10); katman ortalamasi mutlak degisimin en buyugu 0.0045 nat; kosular arasi SD'nin en buyugu 0.0088 nat; temiz entropi katman ortalamasi araligi 4.613; 5.105 nat.

| Katman (1-tabanli; artefakt indeksi) | Kosu degerleri (adv - temiz, nat) | Ortalama | SD (kosular arasi) | TOST p | %90 GA | GA marj icinde | Esdeger | Temiz entropi |
|---|---|---|---|---|---|---|---|---|
| 1 (indeks 0) | +0.0006 / -0.0001 / -0.0005 | +0.0000 | 0.0006 | 2.07e-05 | [-0.0009; +0.0010] | evet | evet | 5.105 |
| 2 (indeks 1) | -0.0016 / -0.0008 / -0.0022 | -0.0016 | 0.0007 | 3.75e-05 | [-0.0028; -0.0003] | evet | evet | 4.884 |
| 3 (indeks 2) | -0.0014 / +0.0014 / +0.0006 | +0.0002 | 0.0014 | 1.41e-04 | [-0.0022; +0.0027] | evet | evet | 4.859 |
| 4 (indeks 3) | +0.0025 / -0.0010 / +0.0005 | +0.0007 | 0.0017 | 2.08e-04 | [-0.0023; +0.0036] | evet | evet | 4.853 |
| 5 (indeks 4) | -0.0050 / -0.0014 / -0.0012 | -0.0025 | 0.0021 | 3.33e-04 | [-0.0061; +0.0010] | evet | evet | 4.820 |
| 6 (indeks 5) | +0.0008 / -0.0029 / -0.0025 | -0.0015 | 0.0020 | 2.97e-04 | [-0.0050; +0.0019] | evet | evet | 4.805 |
| 7 (indeks 6) | +0.0050 / -0.0021 / +0.0005 | +0.0011 | 0.0036 | 8.91e-04 | [-0.0049; +0.0071] | evet | evet | 4.900 |
| 8 (indeks 7) | +0.0025 / -0.0057 / +0.0075 | +0.0014 | 0.0067 | 0.0031 | [-0.0098; +0.0127] | evet | evet | 4.613 |
| 9 (indeks 8) | +0.0011 / -0.0004 / +0.0034 | +0.0013 | 0.0019 | 2.58e-04 | [-0.0019; +0.0046] | evet | evet | 4.754 |
| 10 (indeks 9) | -0.0004 / -0.0007 / +0.0147 | +0.0045 | 0.0088 | 0.0061 | [-0.0103; +0.0193] | evet | evet | 4.648 |
| 11 (indeks 10) | +0.0007 / -0.0053 / +0.0012 | -0.0011 | 0.0036 | 9.16e-04 | [-0.0073; +0.0050] | evet | evet | 4.699 |
| 12 (indeks 11) | -0.0058 / -0.0072 / +0.0033 | -0.0033 | 0.0057 | 0.0025 | [-0.0128; +0.0063] | evet | evet | 4.664 |

Gerileme kontrolu: `c1_c45_summary.json` entropy_delta SD'si ile bu dosyadaki SD arasinda en buyuk fark 2.6e-07 nat.

### Son blok kosinusu: devrilen ve devrilmeyen ornekler

Tanim notu (artefakttan): 'devrilmeyen' grubu temizde zaten yanlis siniflanan ornekleri de icerir (flipped = ok_clean & adv_wrong, experiments/c1_c4_attention_features.py).

| Model | Katman | Devrilen, kosu ortalamalari | Devrilmeyen, kosu ortalamalari | Devrilen ort.$\pm$SD (kosular arasi) | Devrilmeyen ort.$\pm$SD | Havuz (n agirlikli): devrilen / devrilmeyen | n devrilen (kosu 1 / 2 / 3) | n devrilmeyen (kosu 1 / 2 / 3) | Fark ortalama (devrilen - devrilmeyen) | Fark, kosu degerleri | t (kosu duzeyi, eslestirilmis) | df | p (iki yonlu) | Isaret tutarliligi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ViT | block11.mlp | 0.9790 / 0.9938 / 0.9956 | 0.9754 / 0.9928 / 0.9950 | 0.9895$\pm$0.0091 | 0.9877$\pm$0.0108 | 0.9895 / 0.9877 | 409 / 422 / 406 | 591 / 578 / 594 | +0.0018 | +0.0036 / +0.0010 / +0.0007 | +1.879 | 2 | 0.2010 | 3/3 kosuda devrilen > devrilmeyen |
| ResNet | layer4.1 | 0.9076 / 0.9015 / 0.9082 | 0.9208 / 0.9058 / 0.9165 | 0.9058$\pm$0.0037 | 0.9143$\pm$0.0077 | 0.9058 / 0.9144 | 404 / 420 / 432 | 596 / 580 / 568 | -0.0086 | -0.0132 / -0.0043 / -0.0083 | -3.311 | 2 | 0.0804 | 0/3 kosuda devrilen > devrilmeyen |

Yorum siniri: kosu duzeyi n = 3; ornek bazli test yok.


## Govde metnindeki diger sayilar (hakem M8, 2026-10-04)

_Kaynak: `results/q1/ozdeslik_kontrol.json; results/q1/c3_precision.json; results/c1_c3/c3_summary.json; results/q1/cifar10_l2/e6_onkestirim.json; results/c1_transfer/c1_transfer_summary.json; results/q1/cifar100/transfer/e1_transfer_summary.json; results/c1_addenda/pair*/mifgsm_transfer.json; results/c1_transfer/pair*/a2b_exclusive_subsets.json; results/q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json; results/q1/e1_cifar100_summary.json; logs/Q1_cifar100_clean_*.log; results/q1_research/E1_PILOT_KAPISI.md (kayitli bantlar); results/q1/e3_iki_kol_fit.json; results/q1/e3_surucu_ayristirma.json; results/q1/e3_asimetri_fit.json; results/q1/e2/e2_grid.json; results/q1/b8_secim_bandi.json; results/q1/variance_ratio.json; results/c1_seeds/c1_seed_summary.json; results/c1_gradient/pair*/gradient_summary.json; results/q1/cifar10_l2/e6_aa_l2_summary.json; results/q1/e7_svhn_summary.json; git (kayit ve pilot kapisi kayitlari); logs/C1_at_vit_200{1,2,3}.log; logs/C1_at_resnet_100{1,2,3}.log; results/q1/temiz_ciftler/pair{1,2,3}/havuz_protokoller.json; results/q1/havuz_cifar10/havuz_protokoller.json`_

Hakem M8 (yontem mercegi), metinde foyde karsiligi olmayan yaklasik kirk sayi saptadi. Asagida her madde kendi alt basligindadir ve kendi artefaktindan okunur; 'Metin bicimi' sutunu sayinin metinde gececegi yuvarlamayi gosterir.


### M8.1 Ozdeslik artiklari (36 yon)

Artefakt: `results/q1/ozdeslik_kontrol.json`, uretim 2026-08-20T14:05:03.081817+00:00; yon sayisi 36.

| Olcut | Tam deger | Metin bicimi | Artefakt alani |
|---|---|---|---|
| En buyuk mutlak artik (puan) | 0.41 | 0.41 | ozet/ARTIK_puan/mutlak_max |
| Ortalama mutlak artik (puan) | 0.0947222 | 0.095 | ozet/ARTIK_puan/mutlak_ort |
| Artik / sapma orani, en buyuk (%) | 1.388 | 1.39 | ozet/artigin_sapmaya_orani_yuzde/max |
| Artik / sapma orani, ortalama (%) | 0.348944 | 0.35 | ozet/artigin_sapmaya_orani_yuzde/ort |
| P(adv yanlis, verili temiz yanlis), en kucuk | 0.989014 | 0.989 | ozet/P_advyanlis_verili_temizyanlis/min |
| P(adv yanlis, verili temiz yanlis), ortalama | 0.997261 | 0.997 | ozet/P_advyanlis_verili_temizyanlis/ort |


### M8.2 Ham - kosullu egimleri (CIFAR-10 Linf, CIFAR-100 Linf, CIFAR-10 L2)

| Ayar | Egim (metin bicimi) | Egim (tam) | Kesisim | Pearson r | Yon sayisi | Artefakt alani |
|---|---|---|---|---|---|---|
| CIFAR-10 Linf (ham - kosullu ~ hedef temiz hatasi) | 0.762 | 0.762482 | - | 0.997 | 6 | results/c1_c3/c3_summary.json raw_minus_cond_vs_target_error |
| CIFAR-10 Linf (c3_precision, 4 ondalik) | 0.7625 | 0.7625 | 1.0892 | 0.9971 | 6 | results/q1/c3_precision.json veri_kumeleri/cifar10/RAPOR_EDILEN_n6 |
| CIFAR-100 Linf | 0.656 | 0.6564 | 3.5007 | 0.9307 | 6 | results/q1/c3_precision.json veri_kumeleri/cifar100/RAPOR_EDILEN_n6 |
| CIFAR-10 L2 | 0.914 | 0.913765 | 0.1030 | 0.9991 | 18 | results/q1/cifar10_l2/e6_onkestirim.json O1_yon |

L2 on-kestirim noktalari: 18 yon, 7 ayri hedef temiz hatasi degeri (10.52, 13.95, 14.06, 14.63, 25.90, 26.53, 26.99); sabit WideResNet'e giden yon sayisi 6. Hedef hatasi araligi 10.52; 26.99.


### M8.3 Her-ikisi-dogru farki icin kosum duzeyi t araligi (df=2)

Kosum duzeyi t araligi: ortalama $\pm$ t(0.975; df=2) x SD / sqrt(3); uc kosum (cift) degerinden. Her ayar icin iki kaynak verilir: eslestirilmis fark (`both_correct_paired/diff_pp/values`, ornek duzeyinde hesaplanmis, metindeki aralik bundan gelir) ve tabloda yazili protokol farki (`protocols/both_correct/diff/values`, 2 ondalikli yuvarlanmis).

| Ayar | Kaynak | Kosum degerleri | Ortalama | SD (ddof=1) | t(0.975; 2) | t araligi (metin bicimi) | t araligi (3 ondalik) |
|---|---|---|---|---|---|---|---|
| CIFAR-10 Linf | `c1_transfer_summary.json` both_correct_paired/diff_pp/values | 8.52 / 8.05 / 8.24 | 8.270 | 0.236 | 4.3027 | [7.68; 8.86] | [7.683; 8.857] |
| CIFAR-10 Linf | `c1_transfer_summary.json` protocols/both_correct/diff/values | 8.51 / 8.05 / 8.24 | 8.267 | 0.231 | 4.3027 | [7.69; 8.84] | [7.692; 8.841] |
| CIFAR-100 Linf | `e1_transfer_summary.json` both_correct_paired/diff_pp/values | 11.15 / 10.53 / 11.09 | 10.923 | 0.342 | 4.3027 | [10.07; 11.77] | [10.074; 11.773] |
| CIFAR-100 Linf | `e1_transfer_summary.json` protocols/both_correct/diff/values | 11.15 / 10.53 / 11.09 | 10.923 | 0.342 | 4.3027 | [10.07; 11.77] | [10.074; 11.773] |


### M8.4 MI-FGSM iki yonlu kontrol (alpha = eps/10)

Saldiri (artefaktin kendi alani): MI-FGSM (mu=1.0, steps=10, alpha=eps/10); eps = 0.031373; tohum 42. Deger = kosullu (hedef-dogru) yaniltma orani (%), kosum basina; ortalama$\pm$SD uc kosum arasi (ddof=1).

| Yon | Kosum degerleri (%) | Ortalama$\pm$SD | n kosullu (kosum 1 / 2 / 3) | Kosum basina %95 GA |
|---|---|---|---|---|
| CNN -> ViT | 18.72 / 19.14 / 19.37 | 19.07$\pm$0.33 | 7410 / 7347 / 7301 | [17.81; 19.61]; [18.25; 20.04]; [18.49; 20.29] |
| ViT -> CNN | 15.03 / 15.22 / 16.01 | 15.42$\pm$0.52 | 8537 / 8594 / 8605 | [14.28; 15.80]; [14.48; 15.98]; [15.24; 16.79] |

Yon farki (CNN -> ViT eksi ViT -> CNN), kosum basina: +3.69 / +3.92 / +3.35; ortalama$\pm$SD +3.65$\pm$0.28.

Capraz kontrol, `results/c1_behavior_summary.json` mifgsm alani (ortalama, SD): ResNet18_AT->ViT_Tiny_AT: 19.07, 0.33; ViT_Tiny_AT->ResNet18_AT: 15.42, 0.52.


### M8.5 Marjinal alt kumeler, bilesim terimleri, korunma oranlari ve bant marjlari

#### Yalniz-hedef-dogru (marjinal) alt kumeler, CIFAR-10

(kaynak: `results/c1_transfer/pair*/a2b_exclusive_subsets.json`): hedefin temizde dogru, kaynagin temizde yanlis bildigi ornekler; 'ortak dogru' ise her ikisinin dogru bildigi kume.

| Yon | Marjinal alt kume boyutu | Yaniltma, marjinal (%) | Yaniltma, ortak dogru (%) | Ortak dogru ortalama (3 ondalik) | Boyut (kosum 1 / 2 / 3) | Marjinal yaniltma (kosum 1 / 2 / 3) | Ortak dogru yaniltma (kosum 1 / 2 / 3) |
|---|---|---|---|---|---|---|---|
| ViT -> CNN (hedef CNN) | 1517$\pm$102 | 41.2$\pm$0.8 | 10.0$\pm$0.3 | 9.983 | 1411 / 1527 / 1614 | 41.70 / 40.30 / 41.70 | 9.63 / 10.12 / 10.20 |
| CNN -> ViT (hedef ViT) | 291$\pm$16 | 59.1$\pm$1.7 | 18.2$\pm$0.2 | 18.250 | 284 / 280 / 310 | 60.20 / 60.00 / 57.10 | 18.14 / 18.17 / 18.44 |

Ortak dogru kume boyutu (kosum 1 / 2 / 3): 7126 / 7067 / 6991.


#### Sinif bilesimi terimi, CIFAR-100

(kaynak: `results/q1/cifar100/transfer/pair*/a2b_class_balance_cifar100.json` protokoller/*/AYRISTIRMA/bilesim_etkisi; puan, CNN -> ViT eksi ViT -> CNN asimetrisinin bilesim bileseni):

| Protokol | Bilesim etkisi (kosum 1 / 2 / 3) | Ortalama$\pm$SD |
|---|---|---|
| Unconditioned (raw) | +0.000 / +0.000 / +0.000 | +0.000$\pm$0.000 |
| Target-correct | -1.249 / -1.330 / -1.065 | -1.215$\pm$0.136 |
| Both-correct | +0.000 / +0.000 / +0.000 | +0.000$\pm$0.000 |
| Successful-source | +0.527 / +0.435 / +0.382 | +0.448$\pm$0.073 |


#### Temiz on-egitim dogrulugunun adversarial egitimde korunmasi, CIFAR-100

pay = adversarial egitimli modelin temiz test dogrulugu (`e1_cifar100_summary.json` mimariler/*/ozet/test_clean/ort); payda = ayni tohumun temiz on-egitim logundaki `Best test accuracy` satiri (`logs/Q1_cifar100_clean_*.log`), uc tohum ortalamasi.

| Model | Temiz on-egitim, en iyi (tohum 1 / 2 / 3) | Ortalama | AT sonrasi temiz (ort) | Korunma orani |
|---|---|---|---|---|
| ResNet-18 | 79.25 / 79.30 / 80.30 | 79.617 | 63.86 | 0.802 |
| ViT-Tiny | 47.45 / 48.50 / 50.35 | 48.767 | 43.17 | 0.885 |


#### Kayitli bantlara marj, ViT-Tiny, CIFAR-100

(bantlar `results/q1_research/E1_PILOT_KAPISI.md` 'Beklenen aralik' tablosundan okunur; deger = `e1_cifar100_summary.json` vit_tiny/ozet/*/degerler, tohum duzeyi):

| Uc nokta | Kayitli bant (%) | Tohum degerleri | Alt kenara marj | Ust kenara marj | En yakin kenara marj (puan) |
|---|---|---|---|---|---|
| PGD-10 | 10-14 | 11.35 / 10.48 / 11.62 | +0.48 | +2.38 | +0.48 |
| AutoAttack | 8-11 | 8.58 / 8.22 / 9.81 | +0.22 | +1.19 | +0.22 |
| Temiz | 33-40 | 41.94 / 43.50 / 44.06 | +8.94 | -4.06 | bant disinda (marj negatif) |


### M8.6 Iki kollu kalibrasyon (E3)

| Kol ve uydurma | Egim | %95 GA (kume bootstrap) | Nokta | Kume | Artefakt alani |
|---|---|---|---|---|---|
| B (gozlemsel havuz), dort protokol | -0.528 | [-0.664; -0.418] | 18 | 6 | results/q1/e3_iki_kol_fit.json kollar/B/dort_protokol |
| B (gozlemsel havuz), uc protokol (basarili-kaynak haric) | +0.431 | [+0.333; +0.633] | 18 | 6 | results/q1/e3_iki_kol_fit.json kollar/B/uc_protokol_bas_kaynak_haric |
| A (kontrollu kol), uc protokol | +0.673 | [+0.602; +0.727] | 116 | 8 | results/q1/e3_iki_kol_fit.json kollar/A/uc_protokol_bas_kaynak_haric |
| A (kontrollu kol), dort protokol | +0.273 | [+0.219; +0.371] | 116 | 8 | results/q1/e3_iki_kol_fit.json kollar/A/dort_protokol |
| B, yalniz ana cift (WRN'siz), dort protokol | -0.100 | [-0.464; +0.092] | 6 | 6 | results/q1/e3_iki_kol_fit.json kollar/B_ana_cift/dort_protokol |

Hedef-dogru ile basarili-kaynak arasi ortalama aciklik (B kolu, 18 yon): 23.77 puan (en buyuk 36.41); `results/q1/e3_surucu_ayristirma.json` protokol_cifti_ortalama_aciklik.

Basarili-kaynagin dort protokolun ucu (en kucuk ya da en buyuk) oldugu yon sayisi: 16/18 (en kucuk 12, en buyuk 4); `protokol_uc_olma_sayilari`.

Ayni yon listesinden (`results/q1/e3_asimetri_fit.json` ciftler/*/asimetri, 18 yon) yeniden hesap: en genis protokol cifti hedef-dogru ile basarili-kaynak olan yon sayisi 13/18; basarili-kaynagin uc oldugu yon sayisi 16/18.


### M8.7 Secim izgarasi (CIFAR-10 18 hucre, 9 hucrelik sweep, CIFAR-100 epok acikligi)

CIFAR-10 izgarasi (`results/q1/e2/e2_grid.json`): 18 hucre = bolme ['B', 'C'] x patience [0, 10, 20] x yumusatma k [1, 3, 5]; uc nokta: GERCEK 10k test PGD-10 (testcurve_*.npz).

| Model | Protokol yayilimi, tohum basina aralik (puan) | Cekirdek (yumusatma haric) oran | Oran araligi (18 referans; en kucuk; en buyuk) | Orani 1'in altinda kalan referans | Tohum SD (referans protokolde) |
|---|---|---|---|---|---|
| ResNet-18 | [2.62; 2.85] | 1.092 | 0.671; 3.379 | 2/18 | 0.533 |
| ViT-Tiny | [1.58; 2.09] | 1.416 | 0.631; 7.376 | 3/18 | 0.340 |

CIFAR-100 ve CIFAR-10 icin 9 hucrelik (patience x yumusatma) secim yayilimi (`results/q1/b8_secim_bandi.json`):

| Veri kumesi | Yayilim araligi (puan) | Yayilim ortalamasi (tam) | Yorunge sayisi | Ortalama (metin bicimi) |
|---|---|---|---|---|
| CIFAR-100 | [0.18; 1.83] | 0.8583 | 6 | 0.86 |
| CIFAR-10 (bolme basina) | [0.54; 2.83] | 1.7542 | 12 | 1.75 |

CIFAR-100 secim yolu ve sonuc (`results/q1/e1_cifar100_summary.json` mimariler/*/ozet):

| Model | En iyi epok (tohum 1 / 2 / 3) | En iyi epok acikligi | Durma epogu (tohum 1 / 2 / 3) | Durma epogu acikligi | Test PGD-10 SD (tam) | Test PGD-10 SD (metin bicimi) |
|---|---|---|---|---|---|---|
| ResNet-18 | 32 / 24 / 49 | 25 | 52 / 44 / 69 | 25 | 0.321 | 0.32 |
| ViT-Tiny | 7 / 11 / 20 | 13 | 27 / 31 / 40 | 13 | 0.596 | 0.60 |


### M8.8 Varyans oranlari

chi-kare araligi: n=3 -> df=2. Pay (protokol sd ortalamasi) sabit kabul edildi. Bir veya daha fazla protokolde GA 1'i iceriyorsa oran MANSETE KONAMAZ; makale bu yuzden mutlak yayilim dilini kullaniyor.

| Protokol | Kosum SD | Oran %95 GA (2 ondalik) | Oran %95 GA (metin bicimi) | GA 1'i iceriyor mu |
|---|---|---|---|---|
| Unconditioned (raw) | 0.3308 | [3.15; 37.97] | [3.1; 38.0] | hayir |
| Target-correct | 0.4355 | [2.39; 28.84] | [2.4; 28.8] | hayir |
| Both-correct | 0.2312 | [4.50; 54.33] | [4.5; 54.3] | hayir |
| Successful-source | 1.2682 | [0.82; 9.90] | [0.8; 9.9] | evet |

| Olcut | Tam deger | Metin bicimi | Artefakt alani |
|---|---|---|---|
| Oran duyarlilik araligi, en kucuk | 5.16 | 5.2 | ORAN_ACIKLIGI/min |
| Oran duyarlilik araligi, en buyuk | 32.62 | 32.6 | ORAN_ACIKLIGI/max |
| Benzeri-benzeriyle (both-correct) sd/sd orani | 28.29 | 28.3 | ORAN_TANIMA_DUYARLI/sd_vs_sd/degerler/both_correct |
| Basarili-kaynak chi-kare GA, alt | 0.82 | 0.8 | protokol_bazli/successful_source/oran_95_GA[0] |
| Basarili-kaynak chi-kare GA, ust | 9.9 | 9.9 | protokol_bazli/successful_source/oran_95_GA[1] |


### M8.9 GPU-saat (uc tohum hatti)

| Olcut | Tam deger | Metin bicimi | Artefakt alani |
|---|---|---|---|
| Toplam saat (artefakt) | 21.68 | 21.7 | timing/total_hours |
| Asama saniyelerinin toplami / 3600 | 21.6769 | 21.7 | timing/stage_seconds (20 asama) |


### M8.10 Gradyan seyrekligi ve hizalanma, kosum duzeyi p

Kosum duzeyi: uc kosumun (cift 1-3) ResNet18_AT ve ViT_Tiny_AT 500 ornek ortalamalari uzerinde eslestirilmis t testi (df=2, iki yonlu); Holm duzeltmesi yalniz uc olcek-bagimsiz seyreklik olcusu uzerinde (hizalanma ayri olcudur).

| Olcu | ResNet-18 AT (kosum 1 / 2 / 3) | ViT-Tiny AT (kosum 1 / 2 / 3) | Fark ortalamasi (R-V) | t (df=2) | p ham (metin bicimi) | p ham (6 ondalik) | p Holm (uc olcu) |
|---|---|---|---|---|---|---|---|
| Gini | 0.6491 / 0.6590 / 0.6412 | 0.6136 / 0.6040 / 0.6121 | +0.0399 | +5.131 | 0.036 | 0.035945 | 0.108 |
| Rel-esik (%1 alti) | 0.3451 / 0.3699 / 0.3282 | 0.2743 / 0.2578 / 0.2725 | +0.0795 | +4.722 | 0.042 | 0.042046 | 0.108 |
| Hoyer | 0.4907 / 0.5058 / 0.4821 | 0.4587 / 0.4498 / 0.4599 | +0.0367 | +3.654 | 0.067 | 0.067401 | 0.108 |
| Hizalanma (mutlak kosinus) | 0.0377 / 0.0370 / 0.0388 | 0.0557 / 0.0564 / 0.0565 | -0.0184 | -34.104 | 0.0009 | 0.000859 | - |

Uc seyreklik olcusunun Holm duzeltilmis p'sinin en buyugu: 0.108.


### M8.11 L2 AutoAttack McNemar siniri (`mcnemar_gurbuz`)

| Cift | A / B | Yalniz A dogru | Yalniz B dogru | McNemar p (tam binom) |
|---|---|---|---|---|
| cift 1 | ResNet18_AT / ViT_Tiny_AT | 766 | 249 | 5.353e-59 |
| cift 2 | ResNet18_AT / ViT_Tiny_AT | 800 | 272 | 2.729e-58 |
| cift 3 | ResNet18_AT / ViT_Tiny_AT | 872 | 302 | 6.253e-62 |

Uc cift icin ortak sinir: en buyuk p = 2.729e-58; p < 10^-57 (ceil kuralina gore; bkz. foyun HER-IKISI-DOGRU McNemar notu). Eksik cift: yok.


### M8.12 SVHN temiz ve PGD-10 degerleri, temiz fark

SVHN test kumesi n = 26032; iki tohum cifti (ResNet tohum 1001, 1002; ViT tohum 2001, 2002).

| Model | Temiz (tohum 1 / 2) | Temiz, artefaktin ort / sd alani | PGD-10 (tohum 1 / 2) | PGD-10, artefaktin ort / sd alani |
|---|---|---|---|---|
| ResNet-18 AT | 94.76 / 93.77 | 94.27 / 0.70 | 55.98 / 55.07 | 55.52 / 0.64 |
| ViT-Tiny AT | 92.82 / 92.03 | 92.42 / 0.56 | 52.37 / 52.23 | 52.30 / 0.10 |

| Temiz dogruluk farki (ResNet - ViT, puan) | Deger | Metin bicimi (2 ondalik) |
|---|---|---|
| Cift 1 / cift 2 (tohum cifti basina) | +1.9400 / +1.7400 | +1.94 / +1.74 |
| Ciftlerin fark ortalamasi | 1.8400 | 1.84 |
| Tam hassasiyetli ortalamalar farki (ort ResNet - ort ViT, iki tohum degerinden) | 1.8400 | 1.84 |
| Artefaktin 2 ondalikli `ort` alanlarinin farki (YUVARLANMIS ortalamalar) | 1.8500 | 1.85 |

Not: iki tohum cifti icin dogru fark ortalamasi 1.84 puandir (iki yontem de bunu verir). 1.85 degeri yalniz yuvarlanmis ortalamalarin (94.27 - 92.42) farkindan cikar; tam hassasiyetli degildir. Metne ciftlerin fark ortalamasi olan 1.84 girmelidir.

PGD-10 farki (ResNet - ViT): cift basina +3.61 / +2.84; ortalama 3.225 (artefakt ort alanlarindan 3.22).


### M8.13 On kayit ile ilk sayi arasindaki sure

Commit kimlikleri `results/q1_research/TUR4_EYLEM_PLANI.md` Faz 2B/2C maddesi 2.3'ten okunur (E1 ongoru kaydi `bb08868`, ilk sayi bildiren epok-5 pilot kapisi `aae9bfc`); sure git commit zamanlarindan hesaplanir. `results/q1/KOKEN.json` bu iki commit'in zamanini tasimaz.

| Olcut | Deger |
|---|---|
| Ongoru kaydi commit zamani | bb08868: 2026-08-17T17:59:33+03:00 |
| Pilot kapisi commit zamani | aae9bfc: 2026-08-17T19:05:11+03:00 |
| Aradaki sure (dakika, tam) | 65.63 |
| Metin bicimi (tam dakikaya yuvarlanmis) | 66 |


### M8.14 Son kontrol noktasi epoklari (durma ve secilen epok)

Kaynak: C1 adversarial egitim loglari (`logs/C1_at_vit_200{1,2,3}.log`, `logs/C1_at_resnet_100{1,2,3}.log`); ilerleme cubuklari (carriage return) ayrilarak 'Epoch N/100 - Loss' satirlari, 'Best model saved!' (secilen = en iyi dogrulama adversarial dogrulugunun epogu) ve 'Early stopping triggered at epoch N' (durma = son egitilen epok) okunur. Egitim bazi loglarda yeniden baslatilmistir ('Resuming'); epok sayaci devam eder.

| Model | Tohum | Durma epogu | Secilen (en iyi) epok | Durma - secilen | Son sabir sayaci | En iyi val adv (%) | Logdaki son epok | Yeniden baslatma |
|---|---|---|---|---|---|---|---|---|
| ViT-Tiny AT | 2001 | 45 | 25 | 20 | 20/20 | 34.05 | 45 | 1 |
| ViT-Tiny AT | 2002 | 38 | 18 | 20 | 20/20 | 34.35 | 38 | 0 |
| ViT-Tiny AT | 2003 | 39 | 19 | 20 | 20/20 | 34.90 | 39 | 0 |
| ResNet-18 AT | 1001 | 71 | 51 | 20 | 20/20 | 45.85 | 71 | 0 |
| ResNet-18 AT | 1002 | 76 | 56 | 20 | 20/20 | 46.65 | 76 | 0 |
| ResNet-18 AT | 1003 | 77 | 57 | 20 | 20/20 | 46.40 | 77 | 0 |

ViT-Tiny AT: durma epoklari 45 / 38 / 39; secilen epoklar 25 / 18 / 19 (tohum sirasiyla).

ResNet-18 AT: durma epoklari 71 / 76 / 77; secilen epoklar 51 / 56 / 57 (tohum sirasiyla).


### M8.15 Temiz ciftlerde toplamsal kaynak-hedef ayristirmasi ve sabit-Standard karsitliklari

Hedef-dogru oranlar (`toplamsal_kaynak_hedef_hedef_dogru`; 6 kosegen-disi hucre, mu + alpha_kaynak + beta_hedef, toplam-sifir kodlama, 1 artik serbestlik derecesi). Kaynak farki = alpha_ResNet18_clean - alpha_ViT_Tiny_clean; hedef farki = beta_ViT_Tiny_clean - beta_ResNet18_clean; asimetri = (ResNet18_clean -> ViT_Tiny_clean) eksi (ViT_Tiny_clean -> ResNet18_clean) hedef-dogru orani (`yonlu/*/oranlar/target_correct`); artik farki = asimetri - kaynak farki - hedef farki (burada hesaplanir). Ortalama$\pm$SD uc cift arasidir (ddof=1).

| Olcut | Cift 1 / 2 / 3 | Ortalama$\pm$SD |
|---|---|---|
| Kaynak farki (ResNet - ViT) | +71.66 / +67.09 / +68.79 | +69.18$\pm$2.31 |
| Hedef farki (ViT - ResNet) | -76.99 / -73.72 / -74.44 | -75.05$\pm$1.72 |
| Asimetri (R->V eksi V->R) | -3.56 / -5.22 / -4.69 | -4.49$\pm$0.85 |
| Artik farki (hesaplanan) | +1.77 / +1.41 / +0.96 | +1.38$\pm$0.40 |
| R2 | 0.9994 / 0.9996 / 0.9998 | 0.9996$\pm$0.0002 |
| En buyuk mutlak artik (puan) | 0.88 / 0.70 / 0.48 | 0.69$\pm$0.20 |
| mu | 34.25 / 34.36 / 34.28 | 34.30$\pm$0.06 |

| Model | Kaynak etkisi (cift 1 / 2 / 3) | Ortalama$\pm$SD | Hedef etkisi (cift 1 / 2 / 3) | Ortalama$\pm$SD |
|---|---|---|---|---|
| ResNet18_clean | +23.39 / +21.64 / +22.46 | +22.50$\pm$0.87 | +25.75 / +24.44 / +24.43 | +24.88$\pm$0.76 |
| ViT_Tiny_clean | -48.27 / -45.45 / -46.33 | -46.68$\pm$1.44 | -51.23 / -49.28 / -50.01 | -50.17$\pm$0.99 |
| Standard_WRN28_10 | +24.88 / +23.81 / +23.88 | +24.19$\pm$0.60 | +25.48 / +24.84 / +25.58 | +25.30$\pm$0.40 |

Sabit-Standard karsitliklari (hedef-dogru oran, %; `yonlu/*/oranlar/target_correct`; fark = ResNet18_clean tarafi eksi ViT_Tiny_clean tarafi):

| Karsitlik | Birinci taraf (cift 1 / 2 / 3) | Ortalama$\pm$SD | Ikinci taraf (cift 1 / 2 / 3) | Ortalama$\pm$SD | Fark (cift 1 / 2 / 3) | Fark ortalama$\pm$SD |
|---|---|---|---|---|---|---|
| Hedef Standard: ResNet18_clean->Standard ile ViT_Tiny_clean->Standard | 82.23 / 80.13 / 81.83 | 81.40$\pm$1.11 | 12.34 / 14.45 / 14.00 | 13.60$\pm$1.11 | +69.89 / +65.68 / +67.83 | +67.80$\pm$2.11 |
| Kaynak Standard: Standard->ResNet18_clean ile Standard->ViT_Tiny_clean | 85.77 / 83.31 / 83.07 | 84.05$\pm$1.50 | 7.02 / 8.19 / 7.67 | 7.62$\pm$0.59 | +78.76 / +75.12 / +75.41 | +76.43$\pm$2.02 |


### M8.16 Havuz: XCiT ve ViT-Tiny kaynak etkisi (foyde zaten var; aralik ifadeleri turetildi)

Bu degerler foyun 'RobustBench havuzu' bolumundeki model etkileri tablosunda da vardir; burada metindeki aralik ifadeleri ayni artefakttan (`results/q1/havuz_cifar10/havuz_protokoller.json` toplamsal_kaynak_hedef_hedef_dogru) turetilir.

| Olcut | Deger |
|---|---|
| R2 / hucre | 0.8955 / 56 |
| ViT_Tiny_AT kaynak etkisi | -4.87 |
| ViT_Tiny_AT hedef etkisi | -0.63 |
| Debenedetti2022_XCiT_S12 kaynak etkisi | +3.06 |
| Diger 6 gurbuz modelin kaynak etkisi araligi (ViT_Tiny_AT ve Standard haric) | +2.94; +3.65 |
| Ayni 6 gurbuz modelin hedef etkisi araligi | -4.26; +2.76 |


## M9: Konsey turu, mimari x baslatma 2x2 ve w-tau-r ayrisimi (2026-10-30)

_Kaynak: `results/q1/konsey_ayrisim_b2.json; results/q1/konsey_ayrisim_b4.json; results/q1/konsey_ayrisim_b5.json; results/q1/konsey_b6_maskeleme.json; results/q1/konsey_b3_defter.tsv; results/q1/konsey_b4_matris/transfer_matrix.json; results/q1/konsey_b6_aa/autoattack_results.csv; raporlar/konsey_2026-10-29/hucre_tablosu.json; results/q1/konsey_pilot_zaman.json; results/c1_seeds/c1_seed_summary.json (yalniz V-scr AA capraz basvurusu); results/q1/konsey_sentez_r_tau_masa.json; results/q1/konsey_masa/konsey_masa_cozumlemeleri.json; results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json; results/q1/konsey_masa/_p3_potansiyel_masa.json; experiments/q1_konsey_ayrisim.py (dondurulmus, yalniz esik sabitleri ve sha256); raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md (yalniz Dondurma eki ve govde sha256)`_

29-30.10.2026 konsey turunda on kayitli B2, B3, B4, B5 ve B6 bloklari kosuldu. Asagidaki her alt bolum kendi artefaktindan okunur ve altinda kaynak dosya ile anahtar yollari yazilidir. Yuvarlama: log olcekli nicelikler ve oranlar 3 ondalik, puanlar (yuzde) 2 ondalik, t istatistigi 2 ondalik, p degerleri bilimsel gosterim; 3 ondalikta sifira yuvarlanan ya da elle yeniden uretilmesi gereken farklarda 4 ondalik (ilgili satirda belirtilir).

Hucre tanimlari (`raporlar/konsey_2026-10-29/hucre_tablosu.json` hucreler): C1-R32: C1 ResNet-18 AT, 32x32 girdi (mevcut, kopru karsitligi S1 ve B2); V-scr: C1 ViT-Tiny AT, 32->224, rastgele baslatma (mevcut); V-IN: ViT-Tiny, deit_tiny_patch16_224.fb_in1k baslatma, model ici ImageNet normalizasyonu (yeni); R224-scr: timm resnet18, 32->224, rastgele baslatma, V-scr ile ayni girdi hatti (fable K3) (yeni); R224-IN: timm resnet18, resnet18.a1_in1k baslatma, model ici ImageNet normalizasyonu (yeni); panel: birincil panel P: ImageNet on egitimsiz gurbuz CNN (RobustBench CIFAR-10 Linf); ikincil_panel: ikincil panel: Debenedetti2022Light_XCiT-S12.


### M9.1 B3 egitim defteri (alti yeni kosu)

Egitim (B3 defteri; 'Dogrulama PGD' secilen epoktaki dogrulama bolmesi PGD dogrulugu, %):

| Takma ad | Hucre | Tohum | Temiz epok | AT epok (kosulan) | Secilen epok | Erken durma | Tavanda durdu | Kirpilmis olabilir | Dogrulama PGD (%) |
|---|---|---|---|---|---|---|---|---|---|
| V_IN_s2101 | V-IN | 2101 | 30 | 38 | 18 | evet | hayir | hayir | 45.15 |
| R224_IN_s1301 | R224-IN | 1301 | 30 | 36 | 16 | evet | hayir | hayir | 46.40 |
| R224_scr_s1201 | R224-scr | 1201 | 200 | 42 | 22 | evet | hayir | hayir | 46.40 |
| V_IN_s2102 | V-IN | 2102 | 30 | 47 | 27 | evet | hayir | hayir | 42.90 |
| R224_IN_s1302 | R224-IN | 1302 | 30 | 37 | 17 | evet | hayir | hayir | 46.95 |
| R224_scr_s1202 | R224-scr | 1202 | 200 | 58 | 38 | evet | hayir | hayir | 45.85 |

Test kumesinin ilk 1000 goruntusu (B6; PGD-10 B4 kosegeninden, AA `results/q1/konsey_b6_aa/autoattack_results.csv`; %):

| Takma ad | Temiz (ilk 1000) | PGD-10 | AutoAttack | Fark PGD-10 - AA (puan) |
|---|---|---|---|---|
| V_IN_s2101 | 85.80 | 43.30 | 40.10 | 3.20 |
| R224_IN_s1301 | 87.40 | 45.80 | 38.40 | 7.40 |
| R224_scr_s1201 | 87.20 | 43.90 | 39.50 | 4.40 |
| V_IN_s2102 | 83.70 | 42.20 | 38.80 | 3.40 |
| R224_IN_s1302 | 86.90 | 47.40 | 41.80 | 5.60 |
| R224_scr_s1202 | 85.70 | 45.10 | 41.10 | 4.00 |

Defterdeki temiz ve AT asama surelerinin toplami (sure_s): 17.79 sa. AT satirindaki epok ile at_ozet kosulan_epok: uyusuyor (6/6). Durum 'OK' disindaki egitim satiri: 0.

Denetimler (defter): V_IN_s2101: temiz denetimi GECTI (fark +68.73 puan); AT cokus denetimi TAMAM 34.90; R224_IN_s1301: temiz denetimi GECTI (fark +48.40 puan); AT cokus denetimi TAMAM 41.90; R224_scr_s1201: temiz denetimi satiri yok; AT cokus denetimi satiri yok; V_IN_s2102: temiz denetimi GECTI (fark +69.38 puan); AT cokus denetimi TAMAM 33.35; R224_IN_s1302: temiz denetimi GECTI (fark +49.00 puan); AT cokus denetimi TAMAM 42.55; R224_scr_s1202: temiz denetimi satiri yok; AT cokus denetimi satiri yok.

AT epok suresi (hesaplama ayrintilari beyani icin; 'Defter' = AT satirindaki sure_s / epok, turetilmis; 'Pilot' = on kayit oncesi bos GPU'da olculen epok suresi):

| Takma ad | Hucre | AT sure_s | AT epok | Defter epok suresi (s) | Pilot epok suresi (s) | Defter / pilot (kat) |
|---|---|---|---|---|---|---|
| V_IN_s2101 | V-IN | 5628 | 38 | 148.1 | 125.8 | 1.18 |
| R224_IN_s1301 | R224-IN | 7050 | 36 | 195.8 | 142.7 | 1.37 |
| R224_scr_s1201 | R224-scr | 13126 | 42 | 312.5 | 142.5 | 2.19 |
| V_IN_s2102 | V-IN | 12530 | 47 | 266.6 | 125.8 | 2.12 |
| R224_IN_s1302 | R224-IN | 6766 | 37 | 182.9 | 142.7 | 1.28 |
| R224_scr_s1202 | R224-scr | 8685 | 58 | 149.7 | 142.5 | 1.05 |

Defter / pilot kat araligi: 1.05; 2.19 (6 kosu). Pilot tahmini duvar saati W(80) = 20.47 sa (secilen tavan 80 epok; egitim payi 38.15 sa). Pilot yontemi: '50 olculen iterasyon (5 isinma), AT batch 64, temiz batch 128; epok = iterasyon x (48000/batch) + val temiz + val PGD-10 (5/20 batch olceklenmis)'.

_Kaynak: `results/q1/konsey_b3_defter.tsv` (takma_ad, asama, epok, sure_s, durum; at_ozet notu: secilen_epok, kosulan_epok, erken_durma, tavanda_durdu, kirpilmis_olabilir, val_pgd; denetim_temiz notu: fark; AT notu: cokus denetimi); `raporlar/konsey_2026-10-29/hucre_tablosu.json` modeller.<m>.hucre, .tohum; `results/q1/konsey_b6_maskeleme.json` n, modeller.<m>.temiz_dogruluk_aa, .pgd10_dogruluk, .aa_dogruluk, .fark_puan; `results/q1/konsey_pilot_zaman.json` parcalar.<hucre>.t_at_epok_s, secilen_tavan, W_sa.<tavan>, egitim_payi_sa, yontem_


### M9.2 2x2 hucre tablosu (temiz dogruluk, w, sigma, rho)

Hucre ozetleri (w = beyaz kutu hedef-dogru kirilganlik, %; omega = log w; sigma ve rho bolunmus yari, log olcek; temiz dogruluk tam test kumesi):

| Hucre | Tohum sayisi n | Temiz dogruluk (model degerleri, %) | Temiz ort (%) | w (model degerleri, %) | w ort (%) | omega ort | sigma ort | rho ort | AA ilk 1000 (model degerleri, %) |
|---|---|---|---|---|---|---|---|---|---|
| V-scr | 3 | 74.10 / 73.47 / 73.01 | 73.53 | 55.91 / 55.86 / 55.12 | 55.63 | 4.019 | -1.009 | +0.012 | B6 kapsami disi (konsey_b6_maskeleme.json'da yok) |
| V-IN | 2 | 83.39 / 83.47 | 83.43 | 48.24 / 51.11 | 49.68 | 3.905 | -0.739 | -0.118 | 40.10 / 38.80 |
| R224-scr | 2 | 86.35 / 85.11 | 85.73 | 49.33 / 48.47 | 48.90 | 3.890 | -0.645 | -0.058 | 39.50 / 41.10 |
| R224-IN | 2 | 85.76 / 86.25 | 86.00 | 48.34 / 47.73 | 48.04 | 3.872 | -0.635 | -0.054 | 38.40 / 41.80 |

Model duzeyi:

| Hucre | Model | Tohum | Temiz (%) | w (%) | omega | sigma | rho | AA ilk 1000 (%) |
|---|---|---|---|---|---|---|---|---|
| V-scr | ViT_Tiny_AT_s2001 | 2001 | 74.10 | 55.91 | 4.024 | -1.015 | +0.025 | B6 disi |
| V-scr | ViT_Tiny_AT_s2002 | 2002 | 73.47 | 55.86 | 4.023 | -1.000 | +0.007 | B6 disi |
| V-scr | ViT_Tiny_AT_s2003 | 2003 | 73.01 | 55.12 | 4.009 | -1.011 | +0.004 | B6 disi |
| V-IN | V_IN_s2101 | 2101 | 83.39 | 48.24 | 3.876 | -0.702 | -0.131 | 40.10 |
| V-IN | V_IN_s2102 | 2102 | 83.47 | 51.11 | 3.934 | -0.776 | -0.105 | 38.80 |
| R224-scr | R224_scr_s1201 | 1201 | 86.35 | 49.33 | 3.899 | -0.625 | -0.038 | 39.50 |
| R224-scr | R224_scr_s1202 | 1202 | 85.11 | 48.47 | 3.881 | -0.664 | -0.079 | 41.10 |
| R224-IN | R224_IN_s1301 | 1301 | 85.76 | 48.34 | 3.878 | -0.642 | -0.056 | 38.40 |
| R224-IN | R224_IN_s1302 | 1302 | 86.25 | 47.73 | 3.866 | -0.628 | -0.052 | 41.80 |

w = exp(omega) denetimi: en buyuk mutlak fark 1.42e-14 puan. Temiz dogruluk `konsey_ayrisim_b4.json`'da yoktur; B4'un girdi matrisinden (`results/q1/konsey_b4_matris/transfer_matrix.json` results.<kaynak>-><m>.target_clean_acc, butun kaynaklarda ayni oldugu denetlendi) okunmustur. Bu dosyanin sha256'si 4e2de4c6c0107580..., B4 JSON'daki kayit (veri.girdi_sha256) ile UYUSUYOR. AA sutunundaki goruntu sayisi `results/q1/konsey_b6_maskeleme.json` n alanindan: n = 1000.

V-scr hucresinin AA degeri B6 kapsami disindadir (ON_KAYIT Dondurma eki (i) m.7: B6'da AA yalniz yeni alti modelde kosar, V-scr ve C1-R32 icin maskeleme isareti tanimlanmamistir). Ayni modellerin C1 AA degerleri `results/c1_seeds/c1_seed_summary.json` pairs.<cift>.vit.aa alanindadir ve foyun 'Tablo I: ana gurbuzluk' bolumundeki AA sutunu da bu dosyanin aggregate alanindan gelir: ViT_Tiny_AT_s2001 29.59; ViT_Tiny_AT_s2002 28.86; ViT_Tiny_AT_s2003 28.96 (%). Bu degerler C1 AA degerlendirmesinin orneklemindendir (foy basligindaki tanim: tam test kumesi), B6 sutunu ise test kumesinin ilk 1000 goruntusundendir; iki orneklem karsilastirilamaz, hucre tablosunun AA sutununa ancak orneklemi etiketlenerek ya da dipnotla bos birakilarak girer.

_Kaynak: `results/q1/konsey_ayrisim_b4.json` b4.hucreler; b4.F_B4.karsitliklar.H2.hucre_n, .H2.hucre_ort (sigma), .H3.hucre_ort (rho); b4.ikincil.S3.etkilesim.hucre_ort (omega); b4.model_tablosu.<m>.yari_oran.omega (w), .yari_log.{omega, sigma, rho}; veri.girdi_sha256; `results/q1/konsey_b4_matris/transfer_matrix.json` results.*-><m>.target_clean_acc; `results/q1/konsey_b6_maskeleme.json` modeller.<m>.aa_dogruluk; `raporlar/konsey_2026-10-29/hucre_tablosu.json` modeller.<m>.tohum; `results/c1_seeds/c1_seed_summary.json` pairs.<cift>.{vit_seed, resnet_seed, vit.aa, resnet.aa} (B6 disi hucre)_


### M9.3 B4 birincil aile F_B4 (H1, H2, H3; Holm)

| Sinama | Kestirim | %90 aralik | %95 aralik | t (df) | Ham p | Holm p | Karar | Ongorulen buyukluk |
|---|---|---|---|---|---|---|---|---|
| H1, A^sigma_scr = sigma(V-scr) - sigma(R224-scr) | -0.364 | [-0.415; -0.314] | [-0.428; -0.300] | -14.60 (5) | 1.36e-05 | 4.09e-05 | destek | (A <= -0,20): evet |
| H2, I^sigma = [sigma(V-IN) - sigma(V-scr)] - [sigma(R224-IN) - sigma(R224-scr)] | +0.260 | [+0.186; +0.335] | [+0.165; +0.355] | +7.03 (5) | 9.00e-04 | 9.00e-04 | destek | (I >= +0,10): evet |
| H3, A^rho = 1/2 {[rho(V-scr) - rho(R224-scr)] + [rho(V-IN) - rho(R224-IN)]} | +0.003 | [-0.020; +0.026] | [-0.026; +0.033] | +0.29 (5) | 1.89e-04 | 3.79e-04 | destek (esdeger, Holm sonrasi TOST p < 0,05) | (H3: esdegerlik; buyukluk satiri yok) |

Ham p: H1 tek yonlu (p_tek_kucuk), H2 iki yonlu (p_iki), H3 TOST (iki tek yonlu p'nin buyugu, tost_p); F_B4.not: 'H1 tek yonlu (H0: A >= 0), H2 iki yonlu, H3 TOST +-0,10; birlesik varyans dort hucre. Omega tam orneklem w'den (ON_KAYIT §2).'. Holm denetimi (bu betigin holm() fonksiyonuyla p_ham'dan): en buyuk mutlak fark 0.00e+00.

TOST esdegerlik siniri delta = 0.1 (meta.delta = 0.1; duyarlilik meta.delta_duyarlilik = 0.06); Holm alfa = 0.05; birlesik SD (sigma karsitliklari) 0.0273, (rho karsitligi) 0.0169.

H2 logit olcekli kestirim (karar kosulu): +0.354; H2 ters yon Holm anlamli: hayir; H3 ham %90 aralik +-delta icinde: evet; H1 esdeger: hayir; H2 esdeger: hayir; hesaplanamayip p = 1 sayilan sinama: yok.

Sonuc bolgesi: **O1** (kural: sira: O2 > O5 > O1 > O3 > O3-varyant > O5a; O4 ek niteleme); O4 nitelemesi: hayir; B6 maskeleme kuralindan sonra uygulanan bolge: O1 (isaretli: yok).

Gozlenen %90 yari genislikler (turetilmis, (ci90[1] - ci90[0]) / 2): H1 0.050; H2 0.075; H3 0.023.

_Kaynak: `results/q1/konsey_ayrisim_b4.json` b4.F_B4.karsitliklar.H{1,2,3}.{kestirim, ci90, ci95, t, df, sp_birlesik}; b4.F_B4.p_ham; b4.F_B4.p_holm; b4.F_B4.karar.{H1, H2, H3, *_ongoru_buyuklugu_tuttu, H2_logit_kestirim, H2_negatif_anlamli_holm, H3_ham_ci90_delta_icinde, delta, sonuc_bolgesi, sonuc_kurali, O4_niteleme}; b4.F_B4.maskeleme_kurali; b4.F_B4.p_1_sayilan_hesaplanamayan; meta.{delta, delta_duyarlilik, alfa}_


### M9.4 B4 duyarliliklar ve ikincil ongoruler (S1-S7)

Duyarliliklar (ON_KAYIT geregi karar degistirmez). delta duyarliliginda sonuc bolgesi: O1.

| Duyarlilik | H1 | H2 | H3 | Anahtar |
|---|---|---|---|---|
| delta = 0.06 (Holm p; karar) | 4.09e-05; destek | 1.80e-03; destek | 2.13e-03; destek (esdeger, Holm sonrasi TOST p < 0,05) | b4.duyarlilik.delta_0.06 |
| Tam orneklem, log (%90; %95) | -0.364 [-0.414; -0.314]; [-0.428; -0.300] | +0.260 [+0.186; +0.334]; [+0.166; +0.355] | +0.004 [-0.020; +0.027]; [-0.026; +0.033] | b4.duyarlilik.tam_log.H*.{kestirim, ci90, ci95} |
| Logit olcek (%90; %95) | -0.498 [-0.570; -0.426]; [-0.590; -0.406] | +0.354 [+0.247; +0.461]; [+0.218; +0.490] | -0.087 [-0.110; -0.064]; [-0.116; -0.058] | b4.duyarlilik.yari_logit.H*.{kestirim, ci90, ci95} |
| Oran olcegi, puan (%90; %95) | -8.50 [-9.85; -7.14]; [-10.23; -6.76] | +5.85 [+3.83; +7.86]; [+3.28; +8.42] | -4.13 [-4.90; -3.37]; [-5.11; -3.16] | b4.duyarlilik.yari_oran.H*.{kestirim, ci90, ci95} |
| Welch, %95 (df) | [-0.569; -0.160] (1.10) | [+0.029; +0.491] (1.63) | [-0.052; +0.059] (1.95) | b4.duyarlilik.welch.H*.{ci95, df} |
| Panel jackknife (en kucuk ile en buyuk) | -0.376 (Sehwag2021Proxy_R18 cikinca) ile -0.346 (Engstrom2019Robustness cikinca) | +0.249 (Engstrom2019Robustness cikinca) ile +0.266 (Wong2020Fast cikinca) | +0.001 (Wong2020Fast cikinca) ile +0.006 (Sehwag2021Proxy_R18 cikinca) | b4.duyarlilik.panel_jackknife.<uye>.H* |
| Hiyerarsik bootstrap (B = 2000), %90; %95 | [-0.393; -0.335]; [-0.397; -0.330] | [+0.204; +0.316]; [+0.196; +0.324] | [-0.024; +0.031]; [-0.030; +0.036] | b4.duyarlilik.hiyerarsik_bootstrap.H*.{ci90, ci95} |

Ikincil cozumlemeler (kesifsel, coklu duzeltme yok):

| Cozumleme | Kestirim | %90 aralik | Ek bilgi | Ongoru | Anahtar |
|---|---|---|---|---|---|
| S1, kopru sigma: sigma(R224-scr) - sigma(C1-R32) (kestirim 4 ondalik) | -0.0003 | [-0.035; +0.034] | df 3; Welch %90 [-0.120; +0.119] (Welch df 1.02); TOST p 3.27e-03 | ikisi de esdeger: evet | b4.ikincil.S1.sigma |
| S1, kopru rho | -0.021 | [-0.064; +0.023] | df 3; Welch %90 [-0.114; +0.072] (Welch df 1.33); TOST p 1.17e-02 | ikisi de esdeger: evet | b4.ikincil.S1.rho |
| S2, rho(V-IN) - rho(V-scr) | -0.130 | [-0.161; -0.099] | iki yonlu p 3.86e-04 | negatif: evet | b4.ikincil.S2 |
| S3, omega baslatma etkisi ViT: omega(V-IN) - omega(V-scr) | -0.114 | [-0.151; -0.077] | iki yonlu p 1.62e-03 | omega(V-IN) < omega(V-scr): evet | b4.ikincil.S3.V_baslatma |
| S3, omega baslatma etkisi ResNet: omega(R224-IN) - omega(R224-scr) | -0.018 | [-0.058; +0.023] | iki yonlu p 4.19e-01 | betimsel | b4.ikincil.S3.R224_baslatma |
| S3, omega etkilesimi | -0.096 | [-0.151; -0.041] | iki yonlu p 1.71e-02 | betimsel | b4.ikincil.S3.etkilesim |
| S5, protokol katmani ornek disi sapma (puan) | -0.181 | [-0.500; +0.138] | n = 4; cift sapmalari -0.309 / -0.473 / +0.151 / -0.093; egim, kesisim 0.796, -0.010 | ort sapma bant icinde: evet; curutme (%90 bant disinda): hayir | b4.ikincil.S5.ozet; .egim_kesisim |
| S6, ikincil panel (Debenedetti2022Light_XCiT-S12): A^sigma_scr; I^sigma | -0.284; +0.254 | - | - | isaret ayni A: evet; I: evet | b4.ikincil.S6 |
| S7, Hodge (K = 20): potansiyel payi | 0.919 | - | rastgele beklenti 0.100; dolasim RMS 0.022; r RMS 0.078 | betimsel | b4.ikincil.S7 |

S4, tohum indeksiyle eslesmis ciftler (betimsel; tam orneklem; potansiyel payi = log_w_potansiyel / log_oran, log_oran sifira yakinken kararsizdir):

| Cift (ResNet / ViT) | Hedef-dogru asimetri (puan) | log oran | Potansiyel (w) bileseni | Yonlu artik r | log tau | Potansiyel payi | Potansiyel payi (bolunmus yari) |
|---|---|---|---|---|---|---|---|
| R224_scr_s1201 / ViT_Tiny_AT_s2001 | +4.18 | +0.248 | +0.125 | +0.123 | -1.141 | 0.504 | 0.504 |
| R224_scr_s1202 / ViT_Tiny_AT_s2002 | +4.43 | +0.266 | +0.142 | +0.124 | -1.142 | 0.534 | 0.536 |
| R224_IN_s1301 / V_IN_s2101 | -1.28 | -0.056 | -0.002 | -0.054 | -0.753 | 0.037 | 0.038 |
| R224_IN_s1302 / V_IN_s2102 | +0.78 | +0.036 | +0.068 | -0.032 | -0.825 | 1.896 | 1.961 |

_Kaynak: `results/q1/konsey_ayrisim_b4.json` b4.duyarlilik.{delta_<meta.delta_duyarlilik>, tam_log, yari_logit, yari_oran, welch, panel_jackknife, hiyerarsik_bootstrap}; b4.ikincil.{S1 (kestirim, ci90, df, welch.ci90, welch.df, tost_p), S2, S3, S4, S5, S6, S7}_


### M9.5 B2 aile F_B2 (K-a, K-b, K-c; Holm)

| Sinama | Gozlenen | %90 aralik | %95 aralik | Ham p | Holm p | Karar | Ongorulen buyukluk |
|---|---|---|---|---|---|---|---|
| K-a, simetrik oran q_s = [sigma(R_s) - sigma(V_s)] / D_s | ort q 0.936 (q_s: 0.940 / 0.928 / 0.940) | [0.925; 0.948] | [0.919; 0.953] | 4.19e-05 | 1.26e-04 | destek | (her tohumda q >= 0,75): evet |
| K-b, ViT yonlu terimi rho(V-scr) | ort rho +0.012 (tohumlar: +0.025 / +0.007 / +0.004) | [-0.007; +0.031] | [-0.016; +0.040] | TOST 2.73e-03 | 2.73e-03 | destek (Holm sonrasi TOST p < 0,05) | ham %90 aralik +-delta icinde: evet |
| K-c, tur ici benzerlik Delta_w | Delta_w +0.566 | bootstrap [+0.537; +0.604] | bootstrap [+0.533; +0.608] | 5.00e-04 | 1.00e-03 | destek | (Delta_w >= 0,30): evet |

F_B2.not: 'K-a p tek yonlu t (H0: ort q <= 0,50); K-b p TOST'un buyuk tek yonlu p'si; K-c p hiyerarsik bootstrap (H0: Delta_w <= 0). Destek Holm sonrasi, curutme ham aralikla okunur; ON_KAYIT §5 karar ilkesi.'. TOST siniri delta = 0.1; Holm alfa = 0.05. Holm denetimi (holm() ile p_ham'dan): en buyuk mutlak fark 0.00e+00. Hesaplanamayip p = 1 sayilan: yok.

K-a ayrintisi: D_s 0.391 / 0.387 / 0.390; simetrik pay 0.368 / 0.360 / 0.367; yonlu pay 0.023 / 0.028 / 0.023; payda kurali tetiklenen tohum: yok; ozdeslik artigi en buyuk 4.3e-16; ciftler: ResNet18_AT_s1001 / ViT_Tiny_AT_s2001; ResNet18_AT_s1002 / ViT_Tiny_AT_s2002; ResNet18_AT_s1003 / ViT_Tiny_AT_s2003.

K-c ayrintisi: ViT tur ici log tau -0.453 / -0.466 / -0.410 (ort -0.443); sigma_V -1.015 / -1.000 / -1.011; bootstrap B = 2000, yeniden cekilen tek tohumlu ornek 284; ResNet tur ici log tau -0.496 / -0.494 / -0.476 (ort -0.489).

Duyarliliklar (karar degistirmez):

| Duyarlilik | q | rho(V-scr) ve diger | Anahtar |
|---|---|---|---|
| delta = 0.06 | Holm p 1.26e-04, 8.98e-03, 1.00e-03 | K-a destek; K-b destek (Holm sonrasi TOST p < 0,05); K-c destek | b2.F_B2.duyarlilik_delta_0.06 |
| Tam orneklem, log | ort q 0.937 | ort rho(V-scr) +0.012, %90 [-0.007; +0.031] | b2.duyarlilik.tam_log |
| Yari logit | ort q 1.101 (q_s: 1.125 / 1.093 / 1.086) | ort rho(V-scr) -0.304, %90 [-0.320; -0.289], %95 [-0.327; -0.282] | b2.duyarlilik.yari_logit |
| Yari oran (rho puan) | ort q 1.542 | ort rho(V-scr) -14.66 puan, %90 [-14.93; -14.39] | b2.duyarlilik.yari_oran |
| Panel jackknife | ort q 0.931 (Sehwag2021Proxy_R18 cikinca) ile 0.941 (Carmon2019Unlabeled cikinca) | ort rho(V-scr) +0.001 (Engstrom2019Robustness cikinca) ile +0.022 (Gowal2020Uncovering_28_10_extra cikinca) | b2.duyarlilik.panel_jackknife |
| Ikincil panel (Debenedetti2022Light_XCiT-S12) | q_s 0.899 / 0.825 / 0.842 | rho(V-scr) +0.198 / +0.202 / +0.204 | b2.duyarlilik.ikincil_panel |
| K-a ve K-b hiyerarsik bootstrap | bulunamadi | JSON'da anahtar yok; dondurulmus betik B2'de hiyerarsik bootstrap'i yalniz K-c birincil araligi olarak uretir | b2.duyarlilik.hiyerarsik_bootstrap |

_Kaynak: `results/q1/konsey_ayrisim_b2.json` b2.F_B2.K-a.{q, sinama.ort, sinama.ci90, sinama.ci95, D, simetrik_pay, yonlu_pay, ozdeslik_artik_max, payda_kucuk_tohumlar}; b2.F_B2.K-b.{degerler, ort, ci90, ci95, tost_p}; b2.F_B2.K-c.{Delta_w, bootstrap, log_tau_tur_ici, sigma_V}; b2.F_B2.{p_ham, p_holm, karar, not, duyarlilik_delta_<meta.delta_duyarlilik>}; b2.duyarlilik.{tam_log, yari_logit, yari_oran, panel_jackknife, ikincil_panel}; b2.tur_ici_resnet_log_tau; meta.{delta, alfa}_


### M9.6 B5 saldiri tarafi (korunma orani)

Tanim (b5.tanim): S_k(m) = ort_{c in P} log T_k(m->c); G_k = ort_R S_k - ort_V S_k; korunma orani = G_best/G_PGD; en iyi saldiri her kaynak icin panelde en yuksek S_k'yi veren izinli saldiri, capraz uydurmali bolunmus yari secimle (cift yarida sec, tek yarida degerlendir ve tersi).

Esikler: korunma orani esigi B5_ESIK = 0.5 (`experiments/q1_konsey_ayrisim.py` satir 61); G_PGD hesaplanabilirlik esigi = 0.1 (J5 meta.delta; betikte `if not (Gp > DELTA)` kosulu, DELTA = 0.10, satir 58). Izinli saldirilar: CNN pgd, mi; ViT pgd, mi, tgr.

| Nicelik | Deger | Anahtar |
|---|---|---|
| G_PGD (log birimi; 4 ondalik) | 0.3893 | b5.birincil_C1-R32_V-scr.G_PGD |
| G_PGD bootstrap %90 | [0.370; 0.409] | .bootstrap.G_PGD_ci90 |
| G_best (capraz uydurmali secim; 4 ondalik) | 0.3738 | .G_best |
| Secimin kapattigi acik G_PGD - G_best (turetilmis; 4 ondalik) | 0.0155 | .G_PGD - .G_best |
| Korunma orani G_best / G_PGD | 0.960 | .oran |
| Korunma orani %90 | [0.941; 0.976] | .bootstrap.ci90 |
| Korunma orani %95 | [0.937; 0.981] | .bootstrap.ci95 |
| Gecerli bootstrap kopyasi / B | 2000 / 2000 | .bootstrap.gecerli, .B |
| Karar | destek | .karar |
| Tam orneklem secim duyarliligi: oran | 0.960 | .duyarlilik_tam_orneklem_secim.oran |

Kaynak bazinda secilen saldiri ve panel ortalamasi S_k (tam orneklem, log; farklar turetilmis):

| Kaynak | Hucre | Secilen (cift / tek yari) | Secilen (tam orneklem) | S_PGD | S_MI | S_TGR | S_MI - S_PGD | S_TGR - S_PGD |
|---|---|---|---|---|---|---|---|---|
| ResNet18_AT_s1001 | C1-R32 | pgd / pgd | pgd | 2.822 | 2.820 | - | -0.002 | - |
| ResNet18_AT_s1002 | C1-R32 | pgd / pgd | pgd | 2.842 | 2.838 | - | -0.004 | - |
| ResNet18_AT_s1003 | C1-R32 | mi / mi | mi | 2.836 | 2.838 | - | +0.002 | - |
| ViT_Tiny_AT_s2001 | V-scr | mi / mi | mi | 2.431 | 2.449 | 2.284 | +0.018 | -0.147 |
| ViT_Tiny_AT_s2002 | V-scr | mi / mi | mi | 2.454 | 2.469 | 2.266 | +0.015 | -0.188 |
| ViT_Tiny_AT_s2003 | V-scr | mi / mi | mi | 2.446 | 2.462 | 2.228 | +0.016 | -0.218 |
| R224_scr_s1201 | R224-scr | pgd / pgd | pgd | 2.852 | 2.839 | - | -0.014 | - |
| R224_scr_s1202 | R224-scr | pgd / pgd | pgd | 2.834 | 2.824 | - | -0.010 | - |
| R224_IN_s1301 | R224-IN | pgd / pgd | pgd | 2.844 | 2.837 | - | -0.008 | - |
| R224_IN_s1302 | R224-IN | pgd / pgd | pgd | 2.856 | 2.833 | - | -0.023 | - |
| V_IN_s2101 | V-IN | pgd / pgd | pgd | 2.822 | 2.816 | 2.604 | -0.006 | -0.217 |
| V_IN_s2102 | V-IN | mi / mi | mi | 2.735 | 2.744 | 2.567 | +0.009 | -0.168 |

TGR'nin en iyi saldiri secildigi kaynak sayisi: 0 / 5 ViT kaynagi (TGR yalniz ViT kaynaklarinda izinli). V-scr kaynaklarinda S_TGR - S_PGD araligi -0.218; -0.147 (3 kaynak); V-IN kaynaklarinda S_TGR - S_PGD araligi -0.217; -0.168 (2 kaynak).

Betimsel hucre ciftleri (on kayit geregi karar yok):

| Cift (ResNet hucresi _ ViT hucresi) | G_PGD | G_best | Korunma orani | Tam orneklem secim orani | Not |
|---|---|---|---|---|---|
| R224-scr_V-scr | 0.399 | 0.383 | 0.959 | 0.959 | betimsel |
| R224-IN_V-IN | 0.072 | - | - | - | G_PGD <= J5 meta.delta (0.1); on kayitli B5 hesaplanabilirlik kurali (`if not (Gp > DELTA)`) birincil sinama icin tanimlidir, betimsel cifte uygulanmasi `raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md` §7 m.4 kararidir; JSON'daki G_best ve oran bu karar geregi foye alinmaz, oran yorumlanmaz |

b5.not: 'B5 ayri ailedir (tek sinama), Holm'a girmez; F_B2 ve F_B4 kararlarini degistirmez.'.

_Kaynak: `results/q1/konsey_ayrisim_b5.json` b5.tanim; b5.izinli; b5.birincil_C1-R32_V-scr.{G_PGD, G_best, oran, bootstrap.{ci90, ci95, G_PGD_ci90, gecerli, B}, karar, duyarlilik_tam_orneklem_secim.oran, kaynaklar.<m>.{S_tam, secilen_cift_tek, secilen_tam_orneklem}}; b5.betimsel.<cift>.{G_PGD, G_best, oran, kaynaklar}; meta.delta; `experiments/q1_konsey_ayrisim.py` B5_ESIK, DELTA (kaynak metninden); `raporlar/konsey_2026-10-29/hucre_tablosu.json` modeller.<m>.hucre_


### M9.7 B6 AutoAttack ve maskeleme kurali

| Model | Temiz (AA dosyasi) | Temiz (B4 matrisi) | PGD-10 | AutoAttack | Fark (puan) | Isaretli | Temiz maske uyusmazligi | AA dogru, PGD-10 yanlis |
|---|---|---|---|---|---|---|---|---|
| V_IN_s2101 | 85.80 | 85.80 | 43.30 | 40.10 | 3.20 | hayir | 0 | 0 |
| V_IN_s2102 | 83.70 | 83.70 | 42.20 | 38.80 | 3.40 | hayir | 0 | 0 |
| R224_IN_s1301 | 87.40 | 87.40 | 45.80 | 38.40 | 7.40 | hayir | 0 | 0 |
| R224_IN_s1302 | 86.90 | 86.90 | 47.40 | 41.80 | 5.60 | hayir | 0 | 0 |
| R224_scr_s1201 | 87.20 | 87.20 | 43.90 | 39.50 | 4.40 | hayir | 0 | 0 |
| R224_scr_s1202 | 85.70 | 85.70 | 45.10 | 41.10 | 4.00 | hayir | 0 | 0 |

Kural: test kumesinin ilk n = 1000 goruntusunde PGD-10 ile AutoAttack farki esik_puan = 10.0 puani asan model isaretlenir (PGD kaynagi: per_sample_{m}_to_{m}.npz target_adv_wrong, ilk n goruntu; AA kaynagi: per_sample_{m}.npz robust_correct, ilk n goruntu). Isaretli model: yok; maskeleme_isaretli_arg: ''; hatalar: yok. En buyuk fark R224_IN_s1301 (7.40 puan; esige uzaklik 2.60 puan). Fark araligi 3.20; 7.40 puan.

`results/q1/konsey_b6_aa/autoattack_results.csv` ile capraz denetim (clean_accuracy, robust_accuracy): 6 / 6 modelde uyusuyor. B4 maskeleme kurali: uygulanan bolge O1; not: 'B6'da isaretli model verilmedi (--maskeleme-isaretli)'.

_Kaynak: `results/q1/konsey_b6_maskeleme.json` n, esik_puan, pgd_kaynagi, aa_kaynagi, isaretli, maskeleme_isaretli_arg, hatalar, modeller.<m>.{temiz_dogruluk_aa, temiz_dogruluk_matris, pgd10_dogruluk, aa_dogruluk, fark_puan, isaretli, temiz_maske_uyusmazligi, aa_robust_pgd_yanilmis}; `results/q1/konsey_b6_aa/autoattack_results.csv` model, clean_accuracy, robust_accuracy; `results/q1/konsey_ayrisim_b4.json` b4.F_B4.maskeleme_kurali_


### M9.8 Butunluk (dondurulmus betik, hucre tablosu, on kayit govdesi)

| Dosya | JSON kaydi | On kayit Dondurma eki kaydi | Dosyadan hesaplanan (bu betik) | Durum |
|---|---|---|---|---|
| `experiments/q1_konsey_ayrisim.py` | 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 (J2, J4, J5 meta.betik_sha256; uc JSON ayni) | 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | UYUSUYOR |
| `raporlar/konsey_2026-10-29/hucre_tablosu.json` | 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 (J2, J4, J5 meta.hucre_tablosu_sha256; uc JSON ayni) | 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 | 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 | UYUSUYOR |
| `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` govdesi (ilk satirdan '## Dondurma eki' basligina kadar) | JSON'da kayitli degil; dosyadan hesaplandi | 46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5 | 46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5 | UYUSUYOR |

JSON uretim zamanlari: J2 2026-10-30T01:46:40.768882+00:00; J4 2026-10-30T20:40:40.619077+00:00; J5 2026-10-30T20:40:44.160853+00:00. numpy (JSON meta): 1.26.4. Birincil panel eksik uyesi: J2 yok; J4 yok; J5 yok. Matris cakismasi: J2 yok; J4 yok; J5 pgd yok, mi yok, tgr yok.

Bu bolumde (M9.1-M9.9) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: B2 K-a ve K-b hiyerarsik bootstrap duyarliligi (b2.duyarlilik.hiyerarsik_bootstrap); Iki ImageNet baslatma kontrol noktasinin ImageNet top-1 degeri (ON_KAYIT Dondurma eki (i) m.9; `raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md` §7 m.6; `raporlar/konsey_2026-10-29/hucre_tablosu.json` imagenet_top1 alani yok).

_Kaynak: `results/q1/konsey_ayrisim_b2.json`, `results/q1/konsey_ayrisim_b4.json`, `results/q1/konsey_ayrisim_b5.json` meta.{betik_sha256, hucre_tablosu_sha256, uretildi_utc, numpy}, panel.birincil_eksik, veri.cakismalar; `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` Dondurma eki (a) ve (b) (sha256 kayitlari, metinden); dosya sha256'lari bu betikte hashlib ile hesaplanir (`experiments/q1_konsey_ayrisim.py`, `raporlar/konsey_2026-10-29/hucre_tablosu.json`, `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` govdesi)_


### M9.9 Masa cozumlemeleri (SENTEZ ve konsey_masa)

On kayit oncesi masa cozumlemeleridir; yeni olcum yoktur ve sinama degildir (SENTEZ tanim: 'Konsey sentezi masa cozumlemesi (29.10.2026). Yeni olcum yok, GPU yok.'; `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json` not: 'Tek tohumlu havuz ve dort uyeli panel: on kayit oncesi gorulmus veri, sinama degil.'). Betimsel olarak okunur.

C1 ResNet-18 / ViT-Tiny ciftinin log asimetri ayrisimi (uc tohum cifti; ort ve kosum SD'si JSON'dan; potansiyel payi = log_w_potansiyel / log_oran):

| Kume | Nicelik | Ort | SD (kosum) | Cift degerleri |
|---|---|---|---|---|
| c10_c1_secilen | Hedef-dogru asimetri (puan) | +4.41 | 0.45 | +4.81 / +4.50 / +3.92 |
| c10_c1_secilen | log oran | +0.251 | 0.032 | +0.279 / +0.256 / +0.217 |
| c10_c1_secilen | Potansiyel (w) bileseni | +0.136 | 0.023 | +0.160 / +0.133 / +0.114 |
| c10_c1_secilen | Yonlu artik r | +0.115 | 0.010 | +0.119 / +0.122 / +0.103 |
| c10_c1_secilen | log tau | -1.083 | 0.022 | -1.100 / -1.091 / -1.058 |
| c10_c1_secilen | Potansiyel payi | 0.541 | 0.029 | 0.574 / 0.522 / 0.526 |
| c10_son_kontrol_noktasi | Hedef-dogru asimetri (puan) | +4.64 | 0.56 | +4.48 / +4.17 / +5.27 |
| c10_son_kontrol_noktasi | log oran | +0.273 | 0.029 | +0.267 / +0.247 / +0.305 |
| c10_son_kontrol_noktasi | Potansiyel (w) bileseni | +0.144 | 0.034 | +0.183 / +0.117 / +0.133 |
| c10_son_kontrol_noktasi | Yonlu artik r | +0.129 | 0.044 | +0.084 / +0.130 / +0.172 |
| c10_son_kontrol_noktasi | log tau | -1.170 | 0.021 | -1.194 / -1.160 / -1.155 |
| c10_son_kontrol_noktasi | Potansiyel payi | 0.531 | 0.134 | 0.685 / 0.473 / 0.436 |
| c100_c1_secilen | Hedef-dogru asimetri (puan) | +4.96 | 1.02 | +4.21 / +4.54 / +6.12 |
| c100_c1_secilen | log oran | +0.215 | 0.048 | +0.179 / +0.197 / +0.270 |
| c100_c1_secilen | Potansiyel (w) bileseni | +0.061 | 0.020 | +0.038 / +0.075 / +0.070 |
| c100_c1_secilen | Yonlu artik r | +0.154 | 0.041 | +0.141 / +0.122 / +0.200 |
| c100_c1_secilen | log tau | -1.138 | 0.023 | -1.112 / -1.154 / -1.148 |
| c100_c1_secilen | Potansiyel payi | 0.283 | 0.087 | 0.211 / 0.380 / 0.258 |

Goruntu bootstrap SD'si, cift 1 (goruntu_bootstrap_pair1): c10_c1_secilen r SD 0.030, log tau SD 0.016 (B = 300); c10_son_kontrol_noktasi r SD 0.030, log tau SD 0.016 (B = 300); c100_c1_secilen r SD 0.031, log tau SD 0.016 (B = 300).

| Nicelik (tam orneklem, log) | Deger | Anahtar |
|---|---|---|
| Kaynak acigi toplam | +0.422 | havuz_tohum1.kaynak_acigi_ayristirma_log.toplam |
| Kaynak acigi simetrik pay | +0.392 | havuz_tohum1.kaynak_acigi_ayristirma_log.simetrik_pay |
| Kaynak acigi yonlu pay | +0.030 | havuz_tohum1.kaynak_acigi_ayristirma_log.yonlu_pay |
| Kaynak acigi simetrik oran | 0.928 | havuz_tohum1.kaynak_acigi_ayristirma_log.simetrik_oran |
| Kaynak acigi kontrol artigi | -8.0e-16 | havuz_tohum1.kaynak_acigi_ayristirma_log.kontrol_artik |
| Hedef farki toplam | -0.201 | havuz_tohum1.hedef_farki_ayristirma_log.toplam |
| Hedef farki potansiyel pay | +0.160 | havuz_tohum1.hedef_farki_ayristirma_log.potansiyel_pay |
| Hedef farki simetrik pay | -0.392 | havuz_tohum1.hedef_farki_ayristirma_log.simetrik_pay |
| Hedef farki yonlu pay | +0.030 | havuz_tohum1.hedef_farki_ayristirma_log.yonlu_pay |
| Hedef farki kontrol artigi | -3.6e-16 | havuz_tohum1.hedef_farki_ayristirma_log.kontrol_artik |

Tanimlar (SENTEZ): kaynak acigi 'panel ortalamasi log T(R->c) - log T(V->c) = simetrik (log tau_R - log tau_V) + yonlu (-0.5*(r_R - r_V))'; hedef farki 'panel ortalamasi log T(c->V) - log T(c->R) = potansiyel (log w_V - log w_R) + simetrik (log tau_V - log tau_R) + yonlu (0.5*(r_V - r_R))'. Panel: Wong2020_PRN18, Engstrom2019_RN50, Carmon2019_WRN28_10, Gowal2020_WRN28_10 (havuz_tohum1.ViT_Tiny_AT.panel).

Ayni ayrisimin `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json` karsiligi, ResNet-18 AT (R) ile her model (m) arasindaki panel kaynak aciginin simetrik orani (1_havuz_model_tablosu.modeller.<m>.kaynak_acigi_R_eksi_m_<olcek>.simetrik_oran; jackknife_aralik.<m>.simetrik_oran; panel uyeleri icin panel kendisi haric): ViT_Tiny_AT_s2001: yari_log 0.927, tam_log 0.928, yari_logit 1.097; panel uyesi birakmali jackknife araligi (yari_log) [0.919; 0.935]; Wong2020Fast: yari_log 0.961, tam_log 0.958, yari_logit 1.339; Engstrom2019Robustness: yari_log 0.921, tam_log 0.920, yari_logit 1.258; Carmon2019Unlabeled: yari_log 1.087, tam_log 1.087, yari_logit 1.674; Debenedetti2022Light_XCiT-S12: yari_log 0.688, tam_log 0.688, yari_logit 1.232; panel uyesi birakmali jackknife araligi (yari_log) [0.426; 0.798]; Gowal2020Uncovering_28_10_extra: yari_log 1.341, tam_log 1.341, yari_logit 2.137.

Havuz modellerinde sigma ve rho (`tab:external_pool` icin). 'Masa' sutunlari `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json` 1_havuz_model_tablosu.modeller.<m>.{yari_log, tam_log} alanindan, panel 4 CNN: Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra (1_havuz_model_tablosu.panel). 'B4' sutunlari `results/q1/konsey_ayrisim_b4.json` b4.model_tablosu.<m>.yari_log alanindan, panel 7 uyeli birincil panel: Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra, Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm (panel.birincil). panel_n, panel uyesinin kendisi haric hesaba giren panel modeli sayisidir.

| Model | Masa sigma (yari, log) | Masa rho (yari, log) | Masa panel_n | Masa sigma (tam, log) | Masa rho (tam, log) | B4 sigma (yari, log) | B4 rho (yari, log) | B4 panel_n |
|---|---|---|---|---|---|---|---|---|
| ResNet18_AT_s1001 | -0.694 | -0.018 | 4 | -0.694 | -0.018 | -0.648 | -0.022 | 7 |
| ViT_Tiny_AT_s2001 | -1.086 | +0.043 | 4 | -1.086 | +0.043 | -1.015 | +0.025 | 7 |
| Wong2020Fast | -0.656 | -0.033 | 3 | -0.656 | -0.033 | -0.576 | -0.033 | 6 |
| Engstrom2019Robustness | -0.566 | -0.058 | 3 | -0.565 | -0.058 | -0.508 | -0.055 | 6 |
| Carmon2019Unlabeled | -0.519 | +0.008 | 3 | -0.519 | +0.008 | -0.472 | -0.009 | 6 |
| Debenedetti2022Light_XCiT-S12 | -0.609 | -0.096 | 4 | -0.609 | -0.095 | -0.561 | -0.095 | 7 |
| Gowal2020Uncovering_28_10_extra | -0.521 | +0.083 | 3 | -0.521 | +0.084 | -0.467 | +0.065 | 6 |

Kaynak secimi: `tab:external_pool` sekiz modellik havuz verisinden kuruludur (`results/q1/konsey_masa/_p3_potansiyel_masa.json` havuz_cifar10.klasor = `results/q1/havuz_cifar10`, 8 model: ResNet18_AT, ViT_Tiny_AT, Standard_WRN28_10, Wong2020_PRN18, Engstrom2019_RN50, Carmon2019_WRN28_10, Debenedetti2022_XCiT_S12, Gowal2020_WRN28_10). Masa sutunlari bu veriden hesaplanir (`experiments/q1_konsey_masa.py` kaynak metninde `results/q1/havuz_cifar10`: VAR); B4 sutunlari ayni modellerin B4 matrisindeki (`results/q1/konsey_b4_matris/transfer_matrix.json`) ve farkli paneldeki degeridir. Bu foyde `tab:external_pool` icin secilen kaynak masa sutunlaridir (ayni veri, 4 CNN'lik panel); B4 sutunlari yalniz karsilastirma icindir. Masa model tablosu 7 model kapsar; havuzun kalan 1 uyesi icin bu dosyada sigma ve rho yoktur. SENTEZ havuz_tohum1 log_tau_ort ve r_ort degerleri masa tam_log sigma ve rho ile 1e-9 icinde ayni: ViT_Tiny_AT = ViT_Tiny_AT_s2001; ResNet18_AT = ResNet18_AT_s1001; Debenedetti2022_XCiT_S12 = Debenedetti2022Light_XCiT-S12.

Carpimsal yasa masasi (log oran ile log w orani; lambda = 1 sabit R2, kesisimsiz lambda, kesisimli egim ve kesisim):

| Kume | n | R2 (lambda = 1) | Kesisimsiz lambda | Kesisimli egim, kesisim | Pearson r | Isaret uyumu |
|---|---|---|---|---|---|---|
| Yorunge noktalari (A_kolu), birlesik | 100 | 0.201 | 1.878 | 1.464, +0.110 | 0.958 | 92/100 |
| A_kolu.veri_ayrimi.cifar10 | 66 | - | - | 1.451, +0.106 | 0.965 | 59/66 |
| A_kolu.veri_ayrimi.cifar100 | 34 | - | - | 2.067, +0.097 | 0.925 | 33/34 |
| havuz_AT7 (7 AT modeli; R2 lambda uydurmali: 0.953) | - | 0.953 | 1.015 | - | - | 21/21 |

Onerme 3 ayar testi, havuz (`results/q1/konsey_masa/_p3_potansiyel_masa.json` havuz_cifar10.ayar_testi; n = 10000, B = 400): en buyuk |g| 0.0044, ortalama |g| 0.0008 (4 ondalik), en kucuk p 0.933.

| Nicelik | oran | logit | h | Anahtar |
|---|---|---|---|---|
| Ham - tc kaynak etkisi / tc kaynak SD | 0.316 | 1.655 | 0.016 | havuz_cifar10.ayar_testi.<olcek>.kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD |
| Ham - tc kaynak etkisi, en buyuk mutlak (olcek birimi) | 2.063 | 1.638 | 0.001 | havuz_cifar10.ayar_testi.<olcek>.kaynak_alfa_raw_eksi_tc_en_buyuk_mutlak |
| Ham - tc hedef etkisi ile tau korelasyonu | 0.997 | 0.941 | 1.000 | havuz_cifar10.ayar_testi.<olcek>.hedef_beta_raw_eksi_tc_ile_tau_korelasyonu |
| Ham - tc dolasim RMS / tc dolasim RMS | 0.179 | 0.637 | 0.009 | havuz_cifar10.ayar_testi.<olcek>.dolasim_raw_eksi_tc_rms_bolu_dolasim_tc_rms |
| bc - tc kaynak etkisi / tc kaynak SD | 0.348 | 0.338 | 0.363 | havuz_cifar10.ayar_testi.<olcek>.kaynak_alfa_bc_eksi_tc_bolu_tc_alfa_SD |
| bc - tc dolasim RMS / tc dolasim RMS | 0.197 | 0.445 | 0.177 | havuz_cifar10.ayar_testi.<olcek>.dolasim_bc_eksi_tc_rms_bolu_dolasim_tc_rms |

ImageNet baslatma kontrol noktalarinin ImageNet top-1 degeri: bulunamadi.

_Kaynak: `results/q1/konsey_sentez_r_tau_masa.json` tanim, kumeler.<kume>.{tam_orneklem.<nicelik>.{ort, sd_kosum, degerler}, goruntu_bootstrap_pair1}, havuz_tohum1.{kaynak_acigi_ayristirma_log, hedef_farki_ayristirma_log, <m>.{panel, log_tau_ort, r_ort}}; `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json` betik, not, 1_havuz_model_tablosu.{panel, modeller.<m>.{yari_log, tam_log, kaynak_acigi_R_eksi_m_<olcek>}, jackknife_aralik}; `results/q1/konsey_ayrisim_b4.json` panel.birincil, b4.model_tablosu.<m>.yari_log; `results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json` A_kolu, havuz_AT7; `results/q1/konsey_masa/_p3_potansiyel_masa.json` havuz_cifar10.{klasor, modeller, n, B, ayar_testi}; `raporlar/konsey_2026-10-29/hucre_tablosu.json` imagenet_top1 (yok)_


## M10: Ek bloklar, CIFAR-100 paneli, ImageNetV2 paneli ve gradyan kosinusu (2026-10-31)

_Kaynak: `results/q1/ek_regresyon/gpu_n200/karsilastirma_*.json; results/q1/ek_loglar/*.log, regresyon_gpu200.txt; results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json; results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json; results/q1/konsey_b9_c100/b9_dondurulmus_b2.json; results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json; results/q1/konsey_b9_c100/matris/{transfer_matrix.json, cells_meta.json}; raporlar/konsey_2026-10-29/hucre_tablosu_b9.json; results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json; results/q1/konsey_b8_imagenetv2/b8_betimsel.json; results/q1/konsey_b8_imagenetv2/matris/{transfer_matrix.json, cells_meta.json}; raporlar/konsey_2026-10-29/hucre_tablosu_b8.json; raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_<model>.json; results/q1/konsey_b10_gradyan/<veri>/kosinus_ozet.json; results/q1/konsey_b10_gradyan/mantel_<veri>.json; results/q1/konsey_b10_gradyan/b10_aile.json; results/q1/konsey_ayrisim_b2.json (yalniz CIFAR-10 karsilastirma sutunu); raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md (yalniz Dondurma eki ve govde sha256); results/q1_research/ONKAYIT_SAPMALAR.md (yalniz Ek B8-B10 kayitlari)`_

Ek on kayitli B8, B9 ve B10 bloklarinin sonuclaridir. B9 baglayicidir (aile F_B9, Holm); B8 betimseldir (Holm yok, baglayici karar yok); B10'un karar ailesi F_B10'dur (Holm). Asagidaki her alt bolum kendi artefaktindan okunur ve altinda kaynak dosya ile anahtar yollari yazilidir. Yuvarlama M9 kuraliyla: log olcekli nicelikler, oranlar ve korelasyonlar 3 ondalik, puanlar (yuzde) 2 ondalik, p degerleri bilimsel gosterim.


### M10.1 On kosullar (catal regresyonu, B8 on isleme denetimi, ImageNetV2 orneklemi, matris ayarlari)

GPU catal regresyonu (ozgun matris betigi `experiments/c1_c3_transfer_matrix.py` ile catal betik; klasor adlari A / B sutununda):

| Karsilastirma | A / B | Hucre sayisi | npz sayisi | JSON'u farkli hucre | npz farki | Ust alan farki | BIREBIR |
|---|---|---|---|---|---|---|---|
| `karsilastirma_ozgun_catal.json` | `results/q1/ek_regresyon/gpu_n200/ozgun` / `results/q1/ek_regresyon/gpu_n200/catal` | 9 | 9 | 0 | 0 | 0 | evet |
| `karsilastirma_ozgun_onb_catal_onb.json` | `results/q1/ek_regresyon/gpu_n200/ozgun_onb` / `results/q1/ek_regresyon/gpu_n200/catal_onb` | 9 | 9 | 0 | 0 | 0 | evet |

Onbellek dosyalarinin bayt karsilastirmasi (`results/q1/ek_loglar/regresyon_gpu200.txt`, 'ayni'/'FARKLI' satirlari): 3 ayni, 0 FARKLI. Zincir gunluklerindeki adim donus kodlari (`results/q1/ek_loglar/ek_zincir_{1,2}.log`): b8 denetim rc=0; b9 rc=0; b8 rc=0; b10 c10 rc=0; b10 c100 rc=0; b10 in rc=0.

B8 on isleme denetimi (n = 2000 goruntu; ortak hat BicubicRes256Crop224; temiz dogruluk %; varyant farki = ortak - kendi, puan; 'Esik (i)' kendi hat icin alt sinir, puan; RB temiz `esik.rb_temiz`):

| Takma ad | RobustBench adi | Temiz, ortak hat | Temiz, kendi hat | Varyant farki | Mutlak fark | RB temiz | Esik (i) | (i) gecti | (ii) gecti | isaretli_3_5 | Karar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IN_Salman2020Do_R18 | Salman2020Do_R18 | 41.35 | 41.55 | -0.20 | 0.20 | 52.92 | 31.75 | evet | evet | hayir | gecti |
| IN_Salman2020Do_R50 | Salman2020Do_R50 | 51.90 | 52.00 | -0.10 | 0.10 | 64.02 | 38.41 | evet | evet | hayir | gecti |
| IN_Salman2020Do_50_2 | Salman2020Do_50_2 | 56.75 | 56.20 | +0.55 | 0.55 | 68.46 | 41.08 | evet | evet | hayir | gecti |
| IN_Engstrom2019Robustness | Engstrom2019Robustness | 51.05 | 50.95 | +0.10 | 0.10 | 62.56 | 37.54 | evet | evet | hayir | gecti |
| IN_Chen2024Data_WRN_50_2 | Chen2024Data_WRN_50_2 | 57.60 | 57.05 | +0.55 | 0.55 | 68.76 | 41.26 | evet | evet | hayir | gecti |
| IN_Peng2023Robust | Peng2023Robust | 60.45 | 59.65 | +0.80 | 0.80 | 73.44 | 44.06 | evet | evet | hayir | gecti |
| IN_Singh_ConvNeXt-T-CvSt | Singh2023Revisiting_ConvNeXt-T-ConvStem | 60.90 | 60.90 | +0.00 | 0.00 | 72.72 | 43.63 | evet | evet | hayir | gecti |
| IN_Singh_ViT-S-CvSt | Singh2023Revisiting_ViT-S-ConvStem | 61.00 | 61.00 | +0.00 | 0.00 | 72.56 | 43.54 | evet | evet | hayir | gecti |
| IN_Singh_ConvNeXt-B-CvSt | Singh2023Revisiting_ConvNeXt-B-ConvStem | 63.20 | 63.20 | +0.00 | 0.00 | 75.90 | 45.54 | evet | evet | hayir | gecti |
| IN_Singh_ViT-B-CvSt | Singh2023Revisiting_ViT-B-ConvStem | 64.85 | 64.85 | +0.00 | 0.00 | 76.30 | 45.78 | evet | evet | hayir | gecti |
| IN_Liu_ConvNeXt-B | Liu2023Comprehensive_ConvNeXt-B | 65.50 | 65.50 | +0.00 | 0.00 | 76.02 | 45.61 | evet | evet | hayir | gecti |
| IN_Liu_Swin-B | Liu2023Comprehensive_Swin-B | 64.80 | 64.80 | +0.00 | 0.00 | 76.16 | 45.70 | evet | evet | hayir | gecti |
| IN_Mo_ViT-B | Mo2022When_ViT-B | 56.75 | 55.80 | +0.95 | 0.95 | 68.38 | 41.03 | evet | evet | hayir | gecti |
| IN_Debenedetti_XCiT-S12 | Debenedetti2022Light_XCiT-S12 | 60.35 | 59.90 | +0.45 | 0.45 | 72.34 | 43.40 | evet | evet | hayir | gecti |
| IN_Wong2020Fast | Wong2020Fast | 43.35 | 44.55 | -1.20 | 1.20 | 55.62 | 33.37 | evet | evet | hayir | gecti |

Model sayisi 15; `kalan` listesi: bos; `isaretli` listesi: bos; karari 'gecti' disinda olan: yok; en buyuk mutlak varyant farki 1.20 puan (IN_Wong2020Fast). Model ici normalizasyon katmani tasiyan model: 10/15. Kural (JSON `not`): 'Esik kurali ek on kayit §5.5 (ON_KAYIT_EK_B8_B10_2026-10-30.md): (i) kendi hatta 1000 sinifli temiz dogruluk >= %25 ve >= RobustBench temiz dogrulugunun 0,6 kati; (ii) |ortak - kendi| <= 5 puan; 3 ile 5 puan arasi matriste kalir ve isaretlenir. 'kaldi' alan model matristen cikar (P8 uyesiyse yedek IN_Wong2020Fast ayni denetimle girer; cift uyesiyse cift duzeyi niceliklerden cikar). Sonuc T gorulmeden sapma kaydina yazilir.'

ImageNetV2 orneklemi (`results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json`): n = 2000; dosya listesi uzunlugu 2000; tensor sekli [2000, 3, 224, 224]; on isleme BicubicRes256Crop224; secim kurali 'sinif klasoru basina sirali ilk ceil(n/1000) dosya; sira (sinif, ad)'; liste_sha256 25db498ba8b2c710618e76e8a2dfe5492c9f75be0be1b7f63c253acc4f27d1a8. Ayni ozet: B8 matrisi (`transfer_matrix.json` manifest_liste_sha256) AYNI; B10 ImageNetV2 kosinus ozeti (imagenetv2_liste_sha256) AYNI; sapma kaydi (`results/q1_research/ONKAYIT_SAPMALAR.md`) AYNI. B8 matrisindeki manifest_n = 2000.

Matris kosu ayarlari (`cells_meta.json`; eps ve alpha x 255 turetilmis) ve dondurulmus betigin veri denetimi (`veri`):

| Blok | Veri | Saldiri | eps x 255 | alpha x 255 | Adim | Tohum | n | Kaynak basina tohum | On isleme | JSON hucre sayisi | Klasordeki per_sample npz | Model sayisi | Cakisma | Tablo disi model | Hedef maskesi tutarli |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B9 | cifar100 | pgd linf | 8.00 | 2.00 | 10 | 42 | 10000 | evet | - | 225 | 225 | 15 | 0 | 0 | evet |
| B8 | imagenetv2 | pgd linf | 4.00 | 1.00 | 10 | 42 | 2000 | evet | BicubicRes256Crop224 | 196 | 196 | 14 | 0 | 0 | evet |

_Kaynak: `results/q1/ek_regresyon/gpu_n200/karsilastirma_*.json` A, B, hucre_sayisi, npz_sayisi, json_farkli_hucreler, npz_farklari, ust_alan_farklari, BIREBIR; `results/q1/ek_loglar/regresyon_gpu200.txt` (ayni/FARKLI satirlari); `results/q1/ek_loglar/ek_zincir_{1,2}.log` (rc satirlari); `results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json` n, ortak_onisleme, modeller.<m>.{model, temiz_dogruluk_ortak, temiz_dogruluk_kendi, fark_puan, esik.{karar, esik_i, i_gecti, mutlak_fark_puan, ii_gecti, isaretli_3_5, rb_temiz}}, kalan, isaretli, normalizasyon, not; `results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json` n, dosyalar, tensor_sekli, onisleme, secim_kurali, liste_sha256; `results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json` manifest_liste_sha256, manifest_n; `results/q1/konsey_b10_gradyan/imagenetv2/kosinus_ozet.json` imagenetv2_liste_sha256; `results/q1_research/ONKAYIT_SAPMALAR.md` (liste ozeti kaydi); `<matris>/cells_meta.json`; `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json`, `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` veri.{hucre_sayisi, modeller, cakismalar, tablo_disi_modeller, tutarlilik}_


### M10.2 B9 aile F_B9: F_B2'nin CIFAR-100 yinelemesi (K-a, K-b, K-c; Holm)

CIFAR-100 (B9) ve karsilastirma icin CIFAR-10 (B2, M9.5 ile ayni kaynak):

| Sinama | CIFAR-100 gozlenen | CIFAR-100 %90 aralik | CIFAR-100 %95 aralik | CIFAR-100 ham p | CIFAR-100 Holm p | CIFAR-100 karar | CIFAR-10 gozlenen | CIFAR-10 %90 aralik | CIFAR-10 Holm p | CIFAR-10 karar |
|---|---|---|---|---|---|---|---|---|---|---|
| K-a, simetrik oran q_s | ort q 0.840 (q_s: 0.848 / 0.861 / 0.810) | [0.795; 0.885] | [0.773; 0.906] | 1.02e-03 | 2.05e-03 | destek | ort q 0.936 (q_s: 0.940 / 0.928 / 0.940) | [0.925; 0.948] | 1.26e-04 | destek |
| K-b, ViT yonlu terimi rho(V-scr) | ort rho +0.143 (tohumlar: +0.134 / +0.123 / +0.170) | [+0.101; +0.184] | [+0.082; +0.203] | TOST 9.53e-01 | 9.53e-01 | curutuldu (pozitif yon) | ort rho +0.012 (tohumlar: +0.025 / +0.007 / +0.004) | [-0.007; +0.031] | 2.73e-03 | destek (Holm sonrasi TOST p < 0,05) |
| K-c, tur ici benzerlik Delta_w | Delta_w +0.519 | bootstrap [+0.469; +0.599] | bootstrap [+0.463; +0.604] | 5.00e-04 | 1.50e-03 | destek | Delta_w +0.566 | bootstrap [+0.537; +0.604] | 1.00e-03 | destek |

B9 karar ayrintilari (b2.F_B2.karar): K-a_ongoru_buyuklugu_tuttu (her tohumda q >= 0,75): evet; K-b_ham_ci90_delta_icinde: hayir; K-b_eski_yalniz_pozitif_okuma_curutme: evet; K-c_ongoru_buyuklugu_tuttu (Delta_w >= 0,30): evet.

B9 K-b TOST tek yonlu p'leri: alt 1.69e-03, ust 9.53e-01 (tost_p = buyugu 9.53e-01); sd 0.025, df 2. F_B2.not: 'K-a p tek yonlu t (H0: ort q <= 0,50); K-b p TOST'un buyuk tek yonlu p'si; K-c p hiyerarsik bootstrap (H0: Delta_w <= 0). Destek Holm sonrasi, curutme ham aralikla okunur; ON_KAYIT §5 karar ilkesi.'. TOST siniri delta = 0.1; Holm alfa = 0.05; bootstrap B = 2000, tohum 20261029. Holm denetimi (holm() ile p_ham'dan): en buyuk mutlak fark 0.00e+00. Hesaplanamayip p = 1 sayilan: yok.

delta = 0.06 duyarliligi (b2.F_B2.duyarlilik_delta_0.06): Holm p 2.05e-03, 9.86e-01, 1.50e-03; K-a destek; K-b curutuldu (pozitif yon); K-c destek.

K-a ayrintisi: D_s 0.388 / 0.459 / 0.448; simetrik pay 0.329 / 0.395 / 0.363; yonlu pay 0.059 / 0.064 / 0.085; tek yonlu t p (p_tek_H0_q_le_0.5) 1.02e-03; payda kurali tetiklenen tohum cifti: yok; ozdeslik artigi en buyuk 7.8e-16; ciftler: C100_ResNet18_AT_s1001 / C100_ViT_Tiny_AT_s2001; C100_ResNet18_AT_s1002 / C100_ViT_Tiny_AT_s2002; C100_ResNet18_AT_s1003 / C100_ViT_Tiny_AT_s2003.

K-c ayrintisi: ViT tur ici log tau -0.417 / -0.514 / -0.529 (ort -0.487); sigma_V -0.971 / -1.031 / -1.015; bootstrap B = 2000, yeniden cekilen tek tohumlu ornek 284; ResNet tur ici log tau -0.468 / -0.520 / -0.514 (ort -0.501).

B9 duyarliliklari ve kesifsel S9-1, S9-3 (karar degistirmez):

| Duyarlilik | q | rho(V-scr) ve diger | Anahtar |
|---|---|---|---|
| Tam orneklem, log | ort q 0.840 | ort rho(V-scr) +0.143, %90 [+0.101; +0.184], %95 [+0.082; +0.203] | b2.duyarlilik.tam_log |
| Yari logit | ort q 1.026 (q_s: 0.997 / 1.086 / 0.996) | ort rho(V-scr) -0.413, %90 [-0.546; -0.280], %95 [-0.609; -0.217] | b2.duyarlilik.yari_logit |
| Yari oran (rho puan) | ort q 1.216 | ort rho(V-scr) -14.61 puan, %90 [-17.32; -11.89], %95 [-18.61; -10.60] | b2.duyarlilik.yari_oran |
| Panel jackknife | ort q 0.831 (C100_Jia2022LAS-AT_34_10 cikinca) ile 0.847 (C100_Wang2023Better_WRN-28-10 cikinca) | ort rho(V-scr) +0.127 (C100_Wang2023Better_WRN-28-10 cikinca) ile +0.150 (C100_Rice2020Overfitting cikinca) | b2.duyarlilik.panel_jackknife |
| Ikincil panel (C100_Debenedetti2022Light_XCiT-S12, C100_Hendrycks2019Using) | q_s 0.799 / 0.834 / 0.771 | rho(V-scr) +0.129 / +0.136 / +0.221 | b2.duyarlilik.ikincil_panel |

Sarmalayici yan bilgisi (`results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json`; mod b9; dondurulmus betik cagrisi `--mod b2 --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b9.json --cikti results/q1/konsey_b9_c100/b9_sarmalayici_b2.json --bootstrap 2000 --panel-en-az 5 --matris-dizini results/q1/konsey_b9_c100/matris`): dondurulmus_ozet.karar ile `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` b2.F_B2.karar AYNI; ozgun_matris_betigi_degismedi: evet. Temiz dogruluk (temiz_dogruluk_yuzde, %): C100_ResNet18_AT_s1001 64.23; C100_ResNet18_AT_s1002 64.65; C100_ResNet18_AT_s1003 62.68; C100_ViT_Tiny_AT_s2001 41.94; C100_ViT_Tiny_AT_s2002 43.50; C100_ViT_Tiny_AT_s2003 44.06; C100_Rice2020Overfitting 53.82; C100_Rade2021Helper_R18_ddpm 61.50; C100_Addepalli2022Efficient_RN18 65.45; C100_Sehwag2021Proxy 65.93; C100_Pang2022Robustness_WRN28_10 63.64; C100_Wang2023Better_WRN-28-10 72.57; C100_Jia2022LAS-AT_34_10 64.89; C100_Debenedetti2022Light_XCiT-S12 67.34; C100_Hendrycks2019Using 59.22. Sarmalayicinin karistirici notu (JSON metni): 'E1: C1 ViT-Tiny CIFAR-100 temiz dogrulugu panelden belirgin dusuktur; w ve hedef-dogru payda farkli bir alt kumeye dayanir. Sinirlilik olarak yazilir; bu dosya yalniz bu kosudaki temiz dogruluklari betimsel verir.'

_Kaynak: `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` b2.F_B2.K-a.{q, sinama.{ort, ci90, ci95}, D, simetrik_pay, yonlu_pay, p_tek_H0_q_le_0.5, ozdeslik_artik_max, payda_kucuk_tohumlar, ciftler}; b2.F_B2.K-b.{degerler, ort, sd, df, ci90, ci95, tost_p, tost_p_alt, tost_p_ust}; b2.F_B2.K-c.{Delta_w, bootstrap, log_tau_tur_ici, sigma_V}; b2.F_B2.{p_ham, p_holm, karar, not, p_1_sayilan_hesaplanamayan, duyarlilik_delta_<meta.delta_duyarlilik>}; b2.duyarlilik.{tam_log, yari_logit, yari_oran, panel_jackknife, ikincil_panel}; b2.tur_ici_resnet_log_tau; meta.{delta, alfa, bootstrap_B, bootstrap_tohum}; `results/q1/konsey_ayrisim_b2.json` b2.F_B2 (ayni anahtarlar, CIFAR-10 sutunlari); `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json` meta.{mod, dondurulmus_cagri_argv, ozgun_matris_betigi_degismedi}, temiz_dogruluk_yuzde, karistirici_notu, dondurulmus_ozet.karar_


### M10.3 B9 model tablosu (CIFAR-100)

CIFAR-100, 10000 test goruntusu (temiz ve PGD beyaz kutu `transfer_matrix.json` kosegeninden, %; PGD-10 gurbuz dogruluk turetilmis: 100 - raw_fooling, yani saldiri altinda dogru siniflanan ornek orani, temiz dogrulukla kosullanmamis; w = beyaz kutu hedef-dogru kirilganlik, model_tablosu.yari_oran.omega, %; omega = log w; sigma ve rho bolunmus yari, log olcek; hucre, aile ve panel atamasi `raporlar/konsey_2026-10-29/hucre_tablosu_b9.json`):

| Model | Hucre | Aile | Tohum | Birincil panel | Ikincil panel | Temiz (%) | PGD beyaz kutu ham yaniltma (%) | PGD-10 gurbuz dogruluk (%) (turetilmis: 100 - raw_fooling) | w (%) | omega | sigma | rho | panel_n |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C100_ResNet18_AT_s1001 | C1-R32 | CNN | 1001 | hayir | hayir | 64.23 | 80.84 | 19.16 | 70.17 | 4.251 | -0.642 | +0.016 | 7 |
| C100_ResNet18_AT_s1002 | C1-R32 | CNN | 1002 | hayir | hayir | 64.65 | 80.83 | 19.17 | 70.35 | 4.253 | -0.636 | -0.004 | 7 |
| C100_ResNet18_AT_s1003 | C1-R32 | CNN | 1003 | hayir | hayir | 62.68 | 80.42 | 19.58 | 68.76 | 4.231 | -0.653 | +0.000 | 7 |
| C100_ViT_Tiny_AT_s2001 | V-scr | ViT | 2001 | hayir | hayir | 41.94 | 88.61 | 11.39 | 72.84 | 4.288 | -0.971 | +0.134 | 7 |
| C100_ViT_Tiny_AT_s2002 | V-scr | ViT | 2002 | hayir | hayir | 43.50 | 89.54 | 10.46 | 75.95 | 4.330 | -1.031 | +0.123 | 7 |
| C100_ViT_Tiny_AT_s2003 | V-scr | ViT | 2003 | hayir | hayir | 44.06 | 88.42 | 11.58 | 73.72 | 4.300 | -1.015 | +0.170 | 7 |
| C100_Rice2020Overfitting | panel | CNN | - | evet | hayir | 53.82 | 78.15 | 21.85 | 59.40 | 4.084 | -0.670 | +0.024 | 6 |
| C100_Rade2021Helper_R18_ddpm | panel | CNN | - | evet | hayir | 61.50 | 67.04 | 32.96 | 46.41 | 3.837 | -0.388 | -0.053 | 6 |
| C100_Addepalli2022Efficient_RN18 | panel | CNN | - | evet | hayir | 65.45 | 65.57 | 34.43 | 47.39 | 3.859 | -0.439 | +0.106 | 6 |
| C100_Sehwag2021Proxy | panel | CNN | - | evet | hayir | 65.93 | 63.36 | 36.64 | 44.43 | 3.794 | -0.407 | +0.003 | 6 |
| C100_Pang2022Robustness_WRN28_10 | panel | CNN | - | evet | hayir | 63.64 | 64.39 | 35.61 | 44.04 | 3.785 | -0.396 | -0.033 | 6 |
| C100_Wang2023Better_WRN-28-10 | panel | CNN | - | evet | hayir | 72.57 | 55.51 | 44.49 | 38.69 | 3.656 | -0.468 | -0.048 | 6 |
| C100_Jia2022LAS-AT_34_10 | panel | CNN | - | evet | hayir | 64.89 | 62.86 | 37.14 | 42.76 | 3.756 | -0.421 | +0.002 | 6 |
| C100_Debenedetti2022Light_XCiT-S12 | ikincil_panel | XCiT | - | hayir | evet | 67.34 | 62.21 | 37.79 | 43.88 | 3.781 | -0.489 | +0.000 | 7 |
| C100_Hendrycks2019Using | ikincil_panel | CNN | - | hayir | evet | 59.22 | 65.81 | 34.19 | 42.38 | 3.747 | -0.567 | +0.009 | 7 |

Hucre ortalamalari (turetilmis, model degerlerinin aritmetik ortalamasi):

| Hucre | n | Temiz ort (%) | w ort (%) | sigma ort | rho ort |
|---|---|---|---|---|---|
| C1-R32 | 3 | 63.85 | 69.76 | -0.644 | +0.004 |
| V-scr | 3 | 43.17 | 74.17 | -1.006 | +0.143 |

Denetimler: kosegen cond_fooling ile w arasindaki en buyuk mutlak fark 4.96e-03 puan (5e-03'ten kucuk: evet; round(cond_fooling, 2) == cond_fooling olan hucre 225/225); `transfer_matrix.json` temiz dogrulugu ile sarmalayici temiz_dogruluk_yuzde arasindaki en buyuk mutlak fark 0.00e+00 puan (15 model); hucre tablosundaki model sayisi 15, model_tablosu 15; 100 - raw_fooling ile kosegen npz'den 100 * ort(~target_adv_wrong) en buyuk mutlak fark 7.11e-15 puan; kosegen npz'lerde temiz yanlis olup saldiri altinda dogru siniflanan ornek sayisi (modeller toplami) 7.

_Kaynak: `results/q1/konsey_b9_c100/matris/transfer_matrix.json` n_samples, steps, results.<m>-><m>.{raw_fooling, cond_fooling}, results.*-><m>.target_clean_acc, results.*.cond_fooling (denetim); `results/q1/konsey_b9_c100/matris/per_sample_<m>_to_<m>.npz` target_adv_wrong, target_clean_correct (denetim); `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` b2.model_tablosu.<m>.{yari_oran.omega, yari_log.{omega, sigma, rho, panel_n}}, b2.hucreler; `raporlar/konsey_2026-10-29/hucre_tablosu_b9.json` modeller.<m>.{hucre, aile, tohum, birincil_panel, ikincil_panel}; `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json` temiz_dogruluk_yuzde (denetim)_


### M10.4 B8 ImageNetV2 paneli (betimsel; model tablosu ve ozet olculer)

B8 betimseldir: Holm yok, baglayici karar yok (`results/q1/konsey_b8_imagenetv2/b8_betimsel.json` etiket: 'KESIFSEL / BETIMSEL: IN satirinin dogal olcekte kestirimi; Holm ailesi yok, karar yok').

ImageNetV2, 2000 goruntu, PGD-10 linf eps x 255 = 4.00 (temiz ortak hatta, `b8_betimsel.json` model_tablosu_ozet.temiz_dogruluk_yuzde; PGD beyaz kutu ham yaniltma `transfer_matrix.json` kosegeni; PGD-10 gurbuz dogruluk turetilmis: 100 - raw_fooling, yani saldiri altinda dogru siniflanan ornek orani, temiz dogrulukla kosullanmamis; w = model_tablosu_ozet.w_yuzde; sigma ve rho bolunmus yari, log; hucre ve aile `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json`; cift numarasi `b8_betimsel.json` ciftler.<k>.cift (hucre tablosu tohum alaniyla esitligi denetlenir; ciftsiz modelde tohum alani parantez icinde), satir `b8_betimsel.json` ciftler.<k>.satir; RB sutunlari RobustBench model_info kopyalarinin clean_acc ve autoattack_acc alanlari, ortak hatta olculmemistir):

| Takma ad | RobustBench adi | Hucre (kod yolu) | Aile | Cift no | Satir | Temiz (%) | PGD beyaz kutu ham yaniltma (%) | PGD-10 gurbuz dogruluk (%) (turetilmis: 100 - raw_fooling) | w (%) | sigma | rho | panel_n | RB bildirilen temiz (%) | RB bildirilen AA (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IN_Singh_ConvNeXt-T-CvSt | Singh2023Revisiting_ConvNeXt-T-ConvStem | C1-R32 | CNN | 1 | cift 1, IN satiri | 60.90 | 60.15 | 39.85 | 34.56 | -0.963 | -0.122 | 6 | 72.72 | 49.46 |
| IN_Singh_ConvNeXt-B-CvSt | Singh2023Revisiting_ConvNeXt-B-ConvStem | C1-R32 | CNN | 2 | cift 2, IN satiri | 63.20 | 55.95 | 44.05 | 30.30 | -1.118 | -0.298 | 6 | 75.90 | 56.14 |
| IN_Liu_ConvNeXt-B | Liu2023Comprehensive_ConvNeXt-B | C1-R32 | CNN | 3 | cift 3, scr satiri | 65.50 | 54.35 | 45.65 | 30.38 | -1.148 | -0.140 | 6 | 76.02 | 55.82 |
| IN_Singh_ViT-S-CvSt | Singh2023Revisiting_ViT-S-ConvStem | V-scr | ViT | 1 | cift 1, IN satiri | 61.00 | 60.10 | 39.90 | 34.59 | -1.130 | -0.211 | 6 | 72.56 | 48.08 |
| IN_Singh_ViT-B-CvSt | Singh2023Revisiting_ViT-B-ConvStem | V-scr | ViT | 2 | cift 2, IN satiri | 64.85 | 55.80 | 44.20 | 31.84 | -1.237 | -0.188 | 6 | 76.30 | 54.66 |
| IN_Liu_Swin-B | Liu2023Comprehensive_Swin-B | V-scr | Swin | 3 | cift 3, scr satiri | 64.80 | 54.60 | 45.40 | 29.94 | -1.203 | -0.049 | 6 | 76.16 | 56.16 |
| IN_Mo_ViT-B | Mo2022When_ViT-B | V-scr | ViT | - (tohum alani 4, ciftsiz) | ciftsiz (b8_betimsel ciftler disinda) | 56.75 | 71.95 | 28.05 | 50.57 | -1.184 | +0.024 | 6 | 68.38 | 34.40 |
| IN_Salman2020Do_R18 | Salman2020Do_R18 | panel | CNN | - | panel | 41.35 | 77.10 | 22.90 | 44.62 | -1.070 | +0.202 | 5 | 52.92 | 25.32 |
| IN_Salman2020Do_R50 | Salman2020Do_R50 | panel | CNN | - | panel | 51.90 | 70.20 | 29.80 | 42.58 | -0.819 | +0.003 | 5 | 64.02 | 34.96 |
| IN_Salman2020Do_50_2 | Salman2020Do_50_2 | panel | CNN | - | panel | 56.75 | 68.70 | 31.30 | 44.85 | -0.895 | -0.120 | 5 | 68.46 | 38.14 |
| IN_Engstrom2019Robustness | Engstrom2019Robustness | panel | CNN | - | panel | 51.05 | 74.35 | 25.65 | 49.76 | -0.890 | -0.043 | 5 | 62.56 | 29.22 |
| IN_Chen2024Data_WRN_50_2 | Chen2024Data_WRN_50_2 | panel | CNN | - | panel | 57.60 | 64.10 | 35.90 | 37.67 | -0.813 | +0.025 | 5 | 68.76 | 40.60 |
| IN_Peng2023Robust | Peng2023Robust | panel | CNN | - | panel | 60.45 | 59.55 | 40.45 | 33.09 | -1.039 | -0.067 | 5 | 73.44 | 48.94 |
| IN_Debenedetti_XCiT-S12 | Debenedetti2022Light_XCiT-S12 | ikincil_panel | XCiT | - | ikincil_panel | 60.35 | 64.40 | 35.60 | 41.01 | -1.112 | -0.194 | 6 | 72.34 | 41.78 |

Denetimler: temiz dogruluk (`transfer_matrix.json` hedef temiz, temiz_dogruluk alani ve b8_betimsel) en buyuk mutlak fark 0.00e+00 puan; kosegen cond_fooling ile w en buyuk mutlak fark 4.86e-03 puan (5e-03'ten kucuk: evet; round(cond_fooling, 2) == cond_fooling olan hucre 196/196); 100 - raw_fooling ile kosegen npz'den 100 * ort(~target_adv_wrong) en buyuk mutlak fark 7.11e-15 puan; kosegen npz'lerde temiz yanlis olup saldiri altinda dogru siniflanan ornek sayisi (modeller toplami) 1; b8_betimsel sigma ve rho ile `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` b2.model_tablosu.<m>.yari_log en buyuk mutlak fark 0.00e+00; RB clean_acc ile on isleme denetimindeki esik.rb_temiz en buyuk mutlak fark 0.00e+00 puan (14 model); hucre etiketi uyusmayan: yok.

Cift duzeyi (A = donusturucu - CNN; A^sigma bolunmus yari, log; aralik goruntu bootstrap'i; D, simetrik pay, yonlu pay ve q dondurulmus betigin K-a alanlarindan, ayni cift sirasiyla; D_k yuvarlama kuralina istisna olarak 4 ondalik, payda kurali D_k <= 0.1 (`results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` meta.delta) ile karsilastirma icin):

| Cift | CNN | Donusturucu | Satir | A^sigma | %90 aralik | %95 aralik | A^sigma (logit) | A^rho | A^omega (log w) | D_k | Simetrik pay | Yonlu pay | q_k | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | IN_Singh_ConvNeXt-T-CvSt | IN_Singh_ViT-S-CvSt | IN | -0.167 | [-0.234; -0.096] | [-0.246; -0.084] | -0.193 | -0.089 | +0.001 | 0.1221 | 0.167 | -0.044 | 1.364 | hesaplandi |
| 2 | IN_Singh_ConvNeXt-B-CvSt | IN_Singh_ViT-B-CvSt | IN | -0.118 | [-0.202; -0.038] | [-0.217; -0.023] | -0.147 | +0.110 | +0.050 | 0.1731 | 0.118 | +0.055 | 0.682 | hesaplandi |
| 3 | IN_Liu_ConvNeXt-B | IN_Liu_Swin-B | scr | -0.055 | [-0.137; +0.022] | [-0.153; +0.034] | -0.061 | +0.091 | -0.015 | 0.0999 | 0.055 | +0.045 | 0.547 | hesaplandi |

Satir kestirimleri (`results/q1/konsey_b8_imagenetv2/b8_betimsel.json`; 'Beklenti' sutunu JSON'daki beklenti ve beklenti_esigi alanlaridir, kaynagi ek on kayit §5.6; betimsel etiket karar degildir):

| Nicelik | Ciftler | Cift degerleri | Kestirim | %90 aralik | %95 aralik | Betimsel etiket | Beklenti |
|---|---|---|---|---|---|---|---|
| A_sigma_IN (A^sigma_IN = ort_k [sigma(donusturucu_k) - sigma(CNN_k)], P8, bolunmus yari, log; IN satiri yalniz --in-ciftleri (varsayilan Singh 1, 2)) | 1, 2 | -0.167 / -0.118 | -0.142 | [-0.197; -0.090] | [-0.207; -0.081] | beklentiyle uyumlu | '<= -0.1, iki ciftte de negatif (dondurulmus H1+H2; karar degil)' (esik -0.1; nokta esikte ya da altinda: evet) |
| A_sigma_scr_Liu (ayni nicelik --scr-ciftleri icin (varsayilan Liu 3); 2x2'nin scr satiri) | 3 | -0.055 | -0.055 | [-0.137; +0.022] | [-0.153; +0.034] | belirsiz | '<= -0,20 (H1'in ongorulen buyuklugu; karar degil)' (esik -0.2; nokta esikte ya da altinda: hayir) |

A_sigma_IN iki cift farki 0.048; not: 'iki ciftle df 1; ciftler arasi t araligi kurulmaz (ek on kayit §5.6)'. Goruntu bootstrap'i B = 2000, tohum 20261030 ('ortak goruntu agirliklari; cift kumesi sabit; yalniz goruntu belirsizligi').

Donusturucu rho ve sigma, ayri ayri (donusturucu_rho_ayri_ayri): IN_Singh_ViT-S-CvSt rho -0.211, sigma -1.130; IN_Singh_ViT-B-CvSt rho -0.188, sigma -1.237; IN_Liu_Swin-B rho -0.049, sigma -1.203; IN_Mo_ViT-B rho +0.024, sigma -1.184.

Dondurulmus betigin B8 ciktisi (`results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json`; p degerleri, Holm ve etiketler B8'de karar DEGILDIR, yalniz betimsel): K-a ort q 0.864, %90 [0.126; 1.603], payda kurali tetiklenen cift: cift 3 (IN_Liu_ConvNeXt-B / IN_Liu_Swin-B, D = 0.0999; JSON indeksi 2); K-b 4 donusturucunun ort rho -0.106, %90 [-0.238; +0.026], %95 [-0.285; +0.073], TOST p 5.40e-01; K-c Delta_w +0.228, bootstrap %90 [-0.063; +0.513], p 6.55e-02, donusturucu ciftleri arasi log tau (K-c.log_tau_tur_ici, 6 cift) en kucuk -1.301 (IN_Liu_Swin-B|IN_Mo_ViT-B), en buyuk -0.659 (IN_Singh_ViT-S-CvSt|IN_Singh_ViT-B-CvSt); p_ham null (hesaplanamadi), 5.40e-01, 6.55e-02; p_holm 1.00e+00, 1.00e+00, 1.96e-01; hesaplanamayip p = 1 sayilan indeks 0 (K-a); betigin etiketleri K-a 'kararsiz (payda kucuk: bir tohumda D_s <= 0,10)', K-b 'kararsiz', K-c 'kararsiz'.

S8-2 Hodge (kesifsel, K = 14): potansiyel payi 0.890; rastgele beklenti 2/K 0.143; dolasim RMS 0.059; r RMS 0.177.

B8 duyarliliklari (`results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` b2.duyarlilik; ek on kayit §5.7 S8-3; betimsel, karar yok; rho(V-scr) V-scr hucresindeki 4 donusturucu uzerinden):

| Duyarlilik | q | rho(V-scr) ve diger | Anahtar |
|---|---|---|---|
| Tam orneklem, log | ort q 0.882 | ort rho(V-scr) -0.107, %90 [-0.240; +0.026], %95 [-0.287; +0.073] | b2.duyarlilik.tam_log |
| Yari logit | ort q 0.858 (q_s: 1.319 / 0.725 / 0.529) | ort rho(V-scr) -0.052, %90 [-0.178; +0.073], %95 [-0.222; +0.117] | b2.duyarlilik.yari_logit |
| Yari oran (rho puan) | ort q 0.819 | ort rho(V-scr) +2.71 puan, %90 [-4.38; +9.79], %95 [-6.87; +12.29] | b2.duyarlilik.yari_oran |
| Panel jackknife | ort q 0.830 (IN_Peng2023Robust cikinca) ile 0.908 (IN_Salman2020Do_R50 cikinca) | ort rho(V-scr) -0.126 (IN_Salman2020Do_50_2 cikinca) ile -0.068 (IN_Salman2020Do_R18 cikinca) | b2.duyarlilik.panel_jackknife |
| Ikincil panel (IN_Debenedetti_XCiT-S12) | q_s 0.811 / 4.067 / -0.082 | rho(V-scr) +0.052 / +0.006 / +0.124 / +0.205 | b2.duyarlilik.ikincil_panel |

delta = 0.06 duyarliligi (b2.F_B2.duyarlilik_delta_0.06; betimsel): Holm p 1.00e+00, 1.00e+00, 1.96e-01; betigin etiketleri K-a 'kararsiz (payda kucuk: bir tohumda D_s <= 0,10)', K-b 'kararsiz', K-c 'kararsiz'.

_Kaynak: `results/q1/konsey_b8_imagenetv2/b8_betimsel.json` etiket, model_tablosu_ozet.<m>.{temiz_dogruluk_yuzde, w_yuzde, sigma, rho, panel_n, hucre}, ciftler.<k>.{cift, cnn, donusturucu, satir, A_sigma, A_sigma_logit, A_rho, A_omega_log_w, goruntu_bootstrap_ci90, goruntu_bootstrap_ci95, durum}, A_sigma_IN, A_sigma_scr_Liu (tanim, beklenti, ciftler, cift_degerleri, kestirim, goruntu_bootstrap, beklenti_esigi, betimsel_etiket, nokta_beklenti_esiginde_ya_da_altinda, iki_cift_farki, not), donusturucu_rho_ayri_ayri, hodge_r_kesifsel; `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` b2.F_B2.{K-a.{D, ciftler, payda_kucuk_tohumlar (0 tabanli indeks)}, K-b.{ci90, ci95}, K-c.log_tau_tur_ici, p_ham, p_holm, karar, p_1_sayilan_hesaplanamayan, duyarlilik_delta_<meta.delta_duyarlilik>}, b2.duyarlilik.{tam_log, yari_logit, yari_oran, panel_jackknife, ikincil_panel}, b2.model_tablosu.<m>.yari_log, meta.{delta, delta_duyarlilik}; `results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json` n_samples, steps, norm, eps_255, temiz_dogruluk, results; `results/q1/konsey_b8_imagenetv2/matris/per_sample_<m>_to_<m>.npz` target_adv_wrong, target_clean_correct (denetim); `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json` modeller.<m>.{hucre, aile, tohum}; `results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json` modeller.<m>.{model, esik.rb_temiz}; `raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_<RobustBench adi>.json` clean_acc, autoattack_acc_


### M10.5 B10 girdi gradyani kosinusu ile log tau (Mantel, aile F_B10)

Mantel sinamalari (Spearman r, c_ij ile log tau; 'ham' ve model ana etkileri cikarilmis 'ana_etki_artik'; tek yonlu p birincil; 'p tabani' turetilmis, 1/(perm+1), permutasyon sinamasinin ulasabilecegi en kucuk p):

| Veri kumesi | Sinama | K (model) | Cift sayisi | r | Tek yonlu p | Iki yonlu p | Permutasyon | p tabani 1/(perm+1) (turetilmis) | Tohum | Permutasyon ort / SD | c turu | Dislanan model |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cifar10 | ham | 20 | 190 | +0.943 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | +0.002 / 0.122 | tum | yok |
| cifar10 | ana_etki_artik | 20 | 190 | +0.944 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | +0.001 / 0.075 | tum | yok |
| cifar100 | ham | 15 | 105 | +0.981 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | +0.004 / 0.169 | tum | yok |
| cifar100 | ana_etki_artik | 15 | 105 | +0.912 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | +0.002 / 0.102 | tum | yok |
| imagenetv2 | ham | 14 | 91 | +0.694 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | -0.001 / 0.165 | tum | yok |
| imagenetv2 | ana_etki_artik | 14 | 91 | +0.893 | 1.00e-04 | 1.00e-04 | 9999 | 1.00e-04 | 20261030 | +0.001 / 0.112 | tum | yok |

Tek yonlu p'si p tabanina esit olan sinama: 6/6.

Aile F_B10 (`results/q1/konsey_b10_gradyan/b10_aile.json`; aile buyuklugu 6, Holm):

| Sinama | Istatistik | Ham p | Holm p | Permutasyon | Ongorulen buyukluk | Buyukluk tuttu | Karar |
|---|---|---|---|---|---|---|---|
| H10-cifar10 | +0.943 | 1.00e-04 | 6.00e-04 | 9999 | 0.500 | evet | destek |
| H10k-cifar10 | +0.944 | 1.00e-04 | 6.00e-04 | 9999 | 0.300 | evet | destek |
| H10-cifar100 | +0.981 | 1.00e-04 | 6.00e-04 | 9999 | 0.500 | evet | destek |
| H10k-cifar100 | +0.912 | 1.00e-04 | 6.00e-04 | 9999 | 0.300 | evet | destek |
| H10-imagenetv2 | +0.694 | 1.00e-04 | 6.00e-04 | 9999 | 0.500 | evet | destek |
| H10k-imagenetv2 | +0.893 | 1.00e-04 | 6.00e-04 | 9999 | 0.300 | evet | destek |

Karar kurali (JSON): 'ek on kayit §6.3: (i) kestirim <= 0,20 ve ham p >= 0,20 ise curutuldu; (ii) Holm sonrasi p < 0,05 ise destek; (iii) kalan kararsiz'. Hesaplanamayip p = 1 sayilan: yok. Holm denetimi (holm() ile p_tek_ham'dan): en buyuk mutlak fark 0.00e+00. F_B10 istatistikleri ile mantel_<veri>.json sinamalar.{ham, ana_etki_artik}.istatistik en buyuk mutlak fark 0.00e+00. Mantel notu (JSON): 'Birincil: ham Mantel (Spearman, tek yonlu, pozitif). Ana etki artigi ve kismi Mantel model duzeyi ana etkileri (gurbuzluk duzeyi, gradyan buyuklugu ve algisal hizalanma gibi model ozellikleri) ayiklar. Yorum ek on kayda gore yapilir.'

Aile disi, kesifsel kismi Mantel sinamalari (F_B10'a ve Holm hesabina girmez; ek on kayit §6.2):

| Sinama | Veri kumesi | K | Cift sayisi | r | Tek yonlu p | Iki yonlu p | Permutasyon | Kovaryat sayisi |
|---|---|---|---|---|---|---|---|---|
| kismi_omega | cifar10 | 20 | 190 | +0.936 | 1.00e-04 | 1.00e-04 | 9999 | 2 |
| kismi_omega | cifar100 | 15 | 105 | +0.954 | 1.00e-04 | 1.00e-04 | 9999 | 2 |
| kismi_omega | imagenetv2 | 14 | 91 | +0.532 | 2.00e-04 | 2.00e-04 | 9999 | 2 |
| kismi_omega_gradnorm | cifar10 | 20 | 190 | +0.937 | 1.00e-04 | 1.00e-04 | 9999 | 3 |
| kismi_omega_gradnorm | cifar100 | 15 | 105 | +0.941 | 1.00e-04 | 1.00e-04 | 9999 | 3 |
| kismi_omega_gradnorm | imagenetv2 | 14 | 91 | +0.597 | 1.00e-04 | 1.00e-04 | 9999 | 3 |

`results/q1/konsey_b10_gradyan/b10_aile.json` kesifsel_* ile mantel_<veri>.json sinamalar.<ad>.istatistik en buyuk mutlak fark 0.00e+00.

c_ij ozetleri (kosinus_ozet.json; ortalama, en kucuk ve en buyuk turetilmis, c matrisinin ust ucgeni; aile gruplari turetilmis: c_tum ust ucgeni, aile atamasi hucre tablolarinin aile alanindan (cifar10 `raporlar/konsey_2026-10-29/hucre_tablosu.json`, cifar100 `raporlar/konsey_2026-10-29/hucre_tablosu_b9.json`, imagenetv2 `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json`); donusturucu = aile alani CNN olmayan model (Swin, ViT, XCiT); parantez icinde cift sayisi):

| Veri kumesi | n goruntu | Model sayisi | Cift sayisi | c_ij ort (tum goruntu) | c_ij en kucuk; en buyuk | c_ij ort (iki model dogru) | NaN kosinus | CNN-CNN ort (n) (turetilmis) | Donusturucu-donusturucu ort (n) (turetilmis) | Karma ort (n) (turetilmis) |
|---|---|---|---|---|---|---|---|---|---|---|
| cifar10 | 10000 | 20 | 190 | 0.460 | 0.231; 0.746 | 0.463 | 0 | 0.543 (91) | 0.464 (15) | 0.370 (84) |
| cifar100 | 10000 | 15 | 105 | 0.376 | 0.169; 0.692 | 0.379 | 0 | 0.462 (55) | 0.359 (6) | 0.271 (44) |
| imagenetv2 | 2000 | 14 | 91 | 0.218 | 0.003; 0.486 | 0.192 | 0 | 0.187 (36) | 0.318 (10) | 0.221 (45) |

Tanim (JSON): 'c_ij = ort_x cos(grad_x CE(f_i(x), y), grad_x CE(f_j(x), y)); eval, fp32, [0,1] uzayi'.

_Kaynak: `results/q1/konsey_b10_gradyan/mantel_<veri>.json` c_turu, dislanan, not, sinamalar.{ham, ana_etki_artik, kismi_omega, kismi_omega_gradnorm}.{K, cift_sayisi, istatistik, p_tek, p_iki, perm, tohum, perm_ort, perm_sd}; `results/q1/konsey_b10_gradyan/b10_aile.json` F_B10.{sinamalar.<k>.{sinama, istatistik, p_tek_ham, p_holm, perm, ongorulen_buyukluk, ongorulen_buyukluk_tuttu, karar}, aile_buyuklugu, p_1_sayilan, kural}, kesifsel_kismi_omega.<veri>, kesifsel_kismi_omega_gradnorm.<veri>; `results/q1/konsey_b10_gradyan/<veri>/kosinus_ozet.json` n, modeller, c_tum, c_iki_model_dogru, nan_kosinus_sayisi, tanim; `raporlar/konsey_2026-10-29/hucre_tablosu.json`, `raporlar/konsey_2026-10-29/hucre_tablosu_b9.json`, `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json` modeller.<m>.aile (aile gruplari icin)_


### M10.6 Butunluk (ek on kayit govdesi, hucre tablolari, dondurulmus ve ek betikler)

| Dosya | Kayit yeri | Kayitli sha256 | Dosyadan hesaplanan (bu betik) | JSON kayitlari | Durum |
|---|---|---|---|---|---|
| `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md` govdesi (ilk satirdan '## Dondurma eki' basligina kadar) | ek Dondurma eki (d) | 76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595 | 76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595 | - | UYUSUYOR |
| `experiments/q1_konsey_ayrisim.py` | ek Dondurma eki (a) | 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | b9_dondurulmus_b2.json meta.betik_sha256 ayni; b8_dondurulmus_b2.json meta.betik_sha256 ayni; b9_sarmalayici_b2.json.sarmalayici.json meta.dondurulmus_betik_sha256_dogrulandi ayni; b8_betimsel.json meta.dondurulmus_betik_sha256_dogrulandi ayni; b10_aile.json meta.dondurulmus_betik_sha256_dogrulandi ayni | UYUSUYOR |
| `raporlar/konsey_2026-10-29/hucre_tablosu.json` | ek Dondurma eki (a) | 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 | 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 | - | UYUSUYOR |
| `raporlar/konsey_2026-10-29/hucre_tablosu_b9.json` | ek Dondurma eki (b) | be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd | be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd | b9_dondurulmus_b2.json meta.hucre_tablosu_sha256 ayni; b9_sarmalayici_b2.json.sarmalayici.json meta.hucre_tablosu_sha256 ayni | UYUSUYOR |
| `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json` | ek Dondurma eki (b) | 4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d | 4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d | b8_dondurulmus_b2.json meta.hucre_tablosu_sha256 ayni; b8_betimsel.json meta.hucre_tablosu_sha256 ayni | UYUSUYOR |
| `experiments/c1_c3_transfer_matrix.py` | ek Dondurma eki (c) | f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7 | f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7 | b9_sarmalayici_b2.json.sarmalayici.json meta.ozgun_matris_betigi_sha256_simdi ayni; b8_betimsel.json meta.ozgun_matris_betigi_sha256_simdi ayni; b10_aile.json meta.ozgun_matris_betigi_sha256_simdi ayni | UYUSUYOR |
| `experiments/q1_ek_transfer_matrix.py` | sapma kaydi, kod eki | edec356afa594a681e1b3646b76f28c92bbf16c9159eace3dbc3c03cd6a87145 | edec356afa594a681e1b3646b76f28c92bbf16c9159eace3dbc3c03cd6a87145 | B8 matrisi transfer_matrix.json ek_betik_sha256 ayni | UYUSUYOR |
| `experiments/q1_ek_ayrisim.py` | sapma kaydi, kod eki | d264c4e584fcfb3c0e3dd9517cfe2cea4ea1fe564117c88459e2b9721027a641 | d264c4e584fcfb3c0e3dd9517cfe2cea4ea1fe564117c88459e2b9721027a641 | b9_sarmalayici_b2.json.sarmalayici.json meta.sarmalayici_sha256 ayni; b8_betimsel.json meta.sarmalayici_sha256 ayni; b10_aile.json meta.sarmalayici_sha256 ayni | UYUSUYOR |
| `experiments/q1_ek_gradyan_kosinus.py` | sapma kaydi, kod eki | c82a66d196c38f23d688f610caf6ffceab0c01e7ebfa68e5358f832014043eed | c82a66d196c38f23d688f610caf6ffceab0c01e7ebfa68e5358f832014043eed | mantel_cifar10 betik_sha256 ayni; mantel_cifar100 betik_sha256 ayni; mantel_imagenetv2 betik_sha256 ayni; cifar10 kosinus_ozet betik_sha256 ayni; cifar100 kosinus_ozet betik_sha256 ayni; imagenetv2 kosinus_ozet betik_sha256 ayni | UYUSUYOR |
| `tests/test_q1_ek.py` | sapma kaydi, kod eki | 169a522bf07ff1a8ce7d5828c182cb9893030d098cc99cc731d110e8b1e3facd | 169a522bf07ff1a8ce7d5828c182cb9893030d098cc99cc731d110e8b1e3facd | - | UYUSUYOR |
| `results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json` | sapma kaydi (B8 on isleme denetimi notu) | 9f75f8dd4ad96320e8661ff6a4c8665736d37d3d7a24d28d858dbdfa9e2c4ed1 | 9f75f8dd4ad96320e8661ff6a4c8665736d37d3d7a24d28d858dbdfa9e2c4ed1 | - | UYUSUYOR |

Girdi ve cikti ozetleri: B9 veri.girdi_sha256 (226 dosya, `results/q1/konsey_b9_c100/matris` matrisi ve per_sample npz): yeniden hesaplananla farkli 0; B8 veri.girdi_sha256 (197 dosya, `results/q1/konsey_b8_imagenetv2/matris` matrisi ve per_sample npz): yeniden hesaplananla farkli 0; b10_aile girdiler.cifar10 (results/q1/konsey_b10_gradyan/mantel_cifar10.json) ayni; mantel_cifar10 kosinus_ozet_sha256 (results/q1/konsey_b10_gradyan/cifar10/kosinus_ozet.json) ayni; b10_aile girdiler.cifar100 (results/q1/konsey_b10_gradyan/mantel_cifar100.json) ayni; mantel_cifar100 kosinus_ozet_sha256 (results/q1/konsey_b10_gradyan/cifar100/kosinus_ozet.json) ayni; b10_aile girdiler.imagenetv2 (results/q1/konsey_b10_gradyan/mantel_imagenetv2.json) ayni; mantel_imagenetv2 kosinus_ozet_sha256 (results/q1/konsey_b10_gradyan/imagenetv2/kosinus_ozet.json) ayni; `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json` meta.dondurulmus_cikti_sha256 ile `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json` ayni; `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` ile `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json` meta.uretildi_utc disinda AYNI.

JSON uretim zamanlari: b9_dondurulmus_b2.json 2026-10-31T04:43:48.044428+00:00; b9_sarmalayici_b2.json 2026-10-31T04:43:49.864241+00:00; b9_sarmalayici_b2.json.sarmalayici.json 2026-10-31T04:43:50.244033+00:00; b8_dondurulmus_b2.json 2026-10-31T04:43:51.751189+00:00; b8_betimsel.json 2026-10-31T04:43:53.452600+00:00; b10_aile.json 2026-10-31T04:44:08.752419+00:00; mantel_cifar10 2026-10-31T04:43:58.333024+00:00; mantel_cifar100 2026-10-31T04:44:02.827799+00:00; mantel_imagenetv2 2026-10-31T04:44:07.285684+00:00. numpy (JSON meta): 1.26.4.

Bu bolumde (M10.1-M10.6) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: yok.

_Kaynak: `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md` Dondurma eki (a)-(c) kod bloklari ve (d) govde ozeti (metinden); `results/q1_research/ONKAYIT_SAPMALAR.md` Ek B8-B10 'kod eki' kod blogu ve on isleme denetimi kaydi (metinden); `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json`, `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` meta.{betik_sha256, hucre_tablosu_sha256, uretildi_utc, numpy}, veri.girdi_sha256; `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json`, `results/q1/konsey_b8_imagenetv2/b8_betimsel.json`, `results/q1/konsey_b10_gradyan/b10_aile.json` meta.{sarmalayici_sha256, dondurulmus_betik_sha256_dogrulandi, ozgun_matris_betigi_sha256_simdi, hucre_tablosu_sha256, dondurulmus_cikti_sha256}, girdiler; `results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json` ek_betik_sha256; `results/q1/konsey_b10_gradyan/mantel_<veri>.json` betik_sha256, kosinus_ozet, kosinus_ozet_sha256, uretildi_utc; `results/q1/konsey_b10_gradyan/<veri>/kosinus_ozet.json` betik_sha256; dosya sha256'lari bu betikte hashlib ile hesaplanir_


### M10.7 Ek yer tutuculari icin kaynak veriler (saldiri tohumu tekrari; CIFAR-100 C3 hedef temiz hatalari)

(a) Saldiri tohumu tekrari (saldiri baslatma rastgeleligi; egitim tohumu degil). Ayni kontrol noktasi cifti, test kumesinin ilk 1000 goruntusu (yukleyici karistirmaz), saldiri tohumlari 42, 123, 456, eps x 255 = 8.00; saldiri PGD, adim sayisi `experiments/run_all_analyses_run2.py` STEPS = 10, adim boyu ALPHA = 2/255 (kaynak metninden). Uretim zamani (JSON): 2026-07-31T14:22:41.038207; model_variant alani: 'run3-metric'.

| Model | Kontrol noktasi | Saldiri tohumu sayisi | Goruntu | Temiz ort (%) | Temiz SD (puan) | Gurbuz ort (%) | Gurbuz SD, artefakt alani (puan) | Gurbuz SD, artefakt alani (4 ondalik) | Gurbuz SD, ddof=1 (turetilmis; puan) | Gurbuz SD, ddof=1 (turetilmis; 4 ondalik) |
|---|---|---|---|---|---|---|---|---|---|---|
| ResNet18_AT | `models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth` | 3 | 1000 | 85.70 | 0.00 | 45.53 | 0.05 | 0.0471 | 0.06 | 0.0577 |
| ViT_Tiny_AT | `models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth` | 3 | 1000 | 75.70 | 0.00 | 34.70 | 0.00 | 0.0000 | 0.00 | 0.0000 |

SD tanimi: artefakttaki clean_std ve robust_std alanlari `np.std` varsayilanidir (ddof = 0, n = 3 saldiri tohumu); kaynak metninde `'robust_std': float(np.std(robust_accs))` satiri: VAR. 'ddof=1' sutunu turetilmistir: SD x sqrt(n / (n - 1)). Foy basligindaki '+- standart sapma' tanimi egitim tohumu SD'sidir (ddof = 1); bu alt bolumdeki SD saldiri tohumu SD'sidir ve onunla karistirilmamalidir. Kontrol noktalari ilk C1 ciftidir (1001 / 2001); temiz dogruluk ilk 1000 goruntudendir ve Tablo I'in tam test kumesi ortalamasiyla karsilastirilamaz.

(b) CIFAR-100 C3 on-kestirimi hedefleri (`results/q1/c3_precision.json` veri_kumeleri.cifar100; kosegen disi yon sayisi 6, ayri hedef sayisi 3). Hedef temiz hatasi = 100 - hedef temiz dogrulugu (%); hedef sapmasi = ham - kosullu (puan), JSON'daki hedef sirasiyla:

| Hedef | Hedef temiz hatasi (%) | Hedef sapmasi (puan) | Capraz denetim: 100 - B9 matrisi hedef temiz dogrulugu ort (turetilmis) |
|---|---|---|---|
| ResNet18_AT | 36.15 | 25.42 | 36.15 (3 model; fark 0.00 puan) |
| ViT_Tiny_AT | 56.83 | 40.79 | 56.83 (3 model; fark 0.00 puan) |
| WRN_28_10 | 36.36 | 29.20 | - |

Hedef hatalari sirali: 36.15 / 36.36 / 56.83; en kucuk ara 0.21 puan; aralik 20.69 puan; en kucuk ara / aralik 0.0103; iki hedef cakisiyor: evet; etkin ayri x degeri 2. Capraz denetim sutunu B9 matrisinin (`results/q1/konsey_b9_c100/matris/transfer_matrix.json` results.*->C100_<model>_s*.target_clean_acc) uc tohum ortalamasidir; WRN_28_10 hedefi B9 matrisinde yoktur. Ayni egim ve r bu foyde M8.2 'CIFAR-100 Linf' satirindadir.

Bu alt bolumde (M10.7) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: yok.

_Kaynak: `results/c1_statval/statistical_validation.json` seeds, n_samples, eps, model_variant, timestamp, model_paths, results.<i>.{model, clean_mean, clean_std, robust_mean, robust_std, n_runs, n_samples}; `experiments/run_all_analyses_run2.py` STEPS, ALPHA ve run_statistical_validation govdesi (kaynak metninden); `results/q1/c3_precision.json` veri_kumeleri.cifar100.{n_kosegen_disi, n_ayri_hedef, hedefler, hedef_temiz_hatasi, hedef_sapmasi, X_AYRIKLIGI}; `results/q1/konsey_b9_c100/matris/transfer_matrix.json` results.*.target_clean_acc (capraz denetim)_


## M11: Hakem paneli sonrasi masa cozumlemeleri (2026-10-31)

_Kaynak: `results/q1/konsey_ek_masa/bootstrap_cifar10.json; results/q1/konsey_ek_masa/bootstrap_cifar100.json; results/q1/konsey_ek_masa/mantel_aile.json; results/q1/konsey_ek_masa/kesifsel.json; results/q1/konsey_b10_gradyan/mantel_<veri>.json (yalniz yeniden uretim karsilastirmasi); experiments/q1_ek_masa.py (yalniz sha256)`_

Hakem paneli sonrasi 31.10.2026'da uretilen uc masa cozumlemesi. Her alt bolum kendi JSON'undan okunur ve altinda kaynak dosya ile anahtar yollari yazilidir; etiketler JSON'un 'etiket' alanindandir. Yuvarlama: oranlar, log olcekli nicelikler ve korelasyonlar 3 ondalik, c_ij 4 ondalik, p degerleri bilimsel gosterim.


### M11.1 Hiyerarsik bootstrap duyarliligi: K-a, K-b ve K-c (CIFAR-10 B2, CIFAR-100 B9)

Etiket (`etiket`): on kayitli, sonradan uretildi (31.10.2026, hakem paneli sonrasi).

Tanim (`tanim`): ON_KAYIT §5 Duyarliliklar: 'hiyerarsik bootstrap (hucre icinde kosular, goruntuler ortak, B = 2000)'. Uygulama: (i) goruntu bootstrap agirliklari W (n x B) dondurulmus bootstrap_agirlik() ile bir kez cekilir ve butun hucrelerde, butun modellerde ve uc nicelikte (K-a, K-b, K-c) ortaktir; her kopyada sigma, rho ve S dondurulmus model_duzeyi() ile bolunmus yari, log olcek ve birincil panel P uzerinden agirlikli oranlardan hesaplanir. (ii) K-c icin tohumlar dondurulmus b2_coz() dongusuyle birebir cekilir (V-scr icinde yerine koyarak; ozdes tohum ciftleri disarida; yalniz tek farkli tohum iceren ornek yeniden cekilir). (iii) Ardindan ayni RNG ile her kopyada once C1-R32 hucresinin, sonra V-scr hucresinin kosulari hucre icinde yerine koyarak cekilir (sR, sV; her biri hucre buyuklugu kadar). K-a: k'inci cift (R[sR[k]], V[sV[k]]), q_k = [sigma(R) - sigma(V)] / [S(R) - S(V)], istatistik ort_k q_k. K-b: ort_i rho(V[sV[i]]). Aralik yuzdelik (%90: 5-95, %95: 2,5-97,5; np.percentile dogrusal aradegerleme), K-c ile ayni. Bootstrap p: K-a (1 + #{ort q* <= 0,50})/(B + 1); K-b TOST max[(1 + #{rho* <= -delta})/(B + 1), (1 + #{rho* >= +delta})/(B + 1)]; K-c dondurulmus tanim. Karar karsilastirmasi: dondurulmus b2_karar() kurallari, t araliklari ve t p'leri yerine bootstrap araliklari ve bootstrap p'leri konarak (Holm, aile buyuklugu 3) yeniden uygulanir; nokta kestirimleri degismez. Duyarlilik varyanti (cift_duzeyi): kosu ciftleri birim olarak cekilir (sR cift indeksi olarak kullanilir).

`results/q1/konsey_ek_masa/bootstrap_cifar10.json` meta: betik_sha256 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (dosyadan hesaplanan 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1; AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389; uretildi_utc 2026-10-31T15:03:21.836906+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 200. Veri cifar10 (B2); matris results/q1/konsey_b2_panel; hucre tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json; dondurulmus cikti results/q1/konsey_ayrisim_b2.json; B 2000; bootstrap tohumu 20261029 (ON_KAYIT_2026-10-29.md bootstrap tohumu belirtmez; dondurulmus betigin BOOT_TOHUM sabiti kullanildi (dondurulmus K-c bootstrap'iyla ayni tohum ve ayni RNG akisi; W ilk cekim, K-c tohum cekimleri ikinci, K-a/K-b tohum cekimleri ucuncu)); n_goruntu 10000.

`results/q1/konsey_ek_masa/bootstrap_cifar100.json` meta: betik_sha256 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (dosyadan hesaplanan 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1; AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389; uretildi_utc 2026-10-31T15:03:29.780096+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 229. Veri cifar100 (B9); matris results/q1/konsey_b9_c100/matris; hucre tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b9.json; dondurulmus cikti results/q1/konsey_b9_c100/b9_dondurulmus_b2.json; B 2000; bootstrap tohumu 20261029 (ON_KAYIT_2026-10-29.md bootstrap tohumu belirtmez; dondurulmus betigin BOOT_TOHUM sabiti kullanildi (dondurulmus K-c bootstrap'iyla ayni tohum ve ayni RNG akisi; W ilk cekim, K-c tohum cekimleri ikinci, K-a/K-b tohum cekimleri ucuncu)); n_goruntu 10000.

| Veri | Nicelik | Nokta | t %90 | t %95 | Hiyerarsik bootstrap %90 | Hiyerarsik bootstrap %95 | Bootstrap SD | Bootstrap p | Anahtar |
|---|---|---|---|---|---|---|---|---|---|
| cifar10 | K-a ort q | 0.936 | [0.925; 0.948] | [0.919; 0.953] | [0.894; 0.981] | [0.887; 0.991] | 0.026 | 5.00e-04 (H0: ort q <= 0,50) | K-a.{nokta_ort_q, t_ci90, t_ci95, bootstrap} |
| cifar10 | K-a ort q, cift duzeyi varyant |  |  |  | [0.894; 0.975] | [0.887; 0.982] | 0.024 |  | K-a.cift_duzeyi_varyant |
| cifar10 | K-b ort rho(V-scr) | +0.012 | [-0.007; +0.031] | [-0.016; +0.040] | [-0.021; +0.046] | [-0.029; +0.052] | 0.020 | TOST 5.00e-04 (alt 5.00e-04, ust 5.00e-04; delta 0,06: 7.50e-03); t TOST 2.73e-03 | K-b.{nokta_ort_rho, t_ci90, t_ci95, t_tost_p, bootstrap} |
| cifar10 | K-b ort rho(V-scr), cift duzeyi varyant |  |  |  | [-0.021; +0.046] | [-0.026; +0.052] | 0.020 |  | K-b.cift_duzeyi_varyant |
| cifar10 | K-c Delta_w (yeniden uretim) | +0.566 |  |  | [+0.537; +0.604] | [+0.533; +0.608] |  | 5.00e-04 (H0: Delta_w <= 0) | K-c.{Delta_w, yeniden_bootstrap} |
| cifar10 | K-c Delta_w (dondurulmus JSON) |  |  |  | [+0.537; +0.604] | [+0.533; +0.608] |  | 5.00e-04 | K-c.dondurulmus_bootstrap |
| cifar100 | K-a ort q | 0.840 | [0.795; 0.885] | [0.773; 0.906] | [0.800; 0.880] | [0.790; 0.890] | 0.025 | 5.00e-04 (H0: ort q <= 0,50) | K-a.{nokta_ort_q, t_ci90, t_ci95, bootstrap} |
| cifar100 | K-a ort q, cift duzeyi varyant |  |  |  | [0.800; 0.880] | [0.792; 0.890] | 0.025 |  | K-a.cift_duzeyi_varyant |
| cifar100 | K-b ort rho(V-scr) | +0.143 | [+0.101; +0.184] | [+0.082; +0.203] | [+0.106; +0.178] | [+0.098; +0.185] | 0.022 | TOST 9.70e-01 (alt 5.00e-04, ust 9.70e-01; delta 0,06: 1.00e+00); t TOST 9.53e-01 | K-b.{nokta_ort_rho, t_ci90, t_ci95, t_tost_p, bootstrap} |
| cifar100 | K-b ort rho(V-scr), cift duzeyi varyant |  |  |  | [+0.105; +0.178] | [+0.098; +0.186] | 0.022 |  | K-b.cift_duzeyi_varyant |
| cifar100 | K-c Delta_w (yeniden uretim) | +0.519 |  |  | [+0.469; +0.599] | [+0.463; +0.604] |  | 5.00e-04 (H0: Delta_w <= 0) | K-c.{Delta_w, yeniden_bootstrap} |
| cifar100 | K-c Delta_w (dondurulmus JSON) |  |  |  | [+0.469; +0.599] | [+0.463; +0.604] |  | 5.00e-04 | K-c.dondurulmus_bootstrap |

Karar karsilastirmasi (`karar.karsilastirma`, `karar.delta_0.06.karsilastirma`; kural: 'dondurulmus b2_karar(); t araliklari ve t p'leri yerine bootstrap araliklari ve p'leri'):

| Veri | Sinama | Dondurulmus karar (delta 0,10) | Bootstrap araligiyla (delta 0,10) | Degisti | Dondurulmus karar (delta 0,06) | Bootstrap araligiyla (delta 0,06) | Degisti |
|---|---|---|---|---|---|---|---|
| cifar10 | K-a | destek | destek | hayir | destek | destek | hayir |
| cifar10 | K-b | destek (Holm sonrasi TOST p < 0,05) | destek (Holm sonrasi TOST p < 0,05) | hayir | destek (Holm sonrasi TOST p < 0,05) | destek (Holm sonrasi TOST p < 0,05) | hayir |
| cifar10 | K-c | destek | destek | hayir | destek | destek | hayir |
| cifar100 | K-a | destek | destek | hayir | destek | destek | hayir |
| cifar100 | K-b | curutuldu (pozitif yon) | curutuldu (pozitif yon) | hayir | curutuldu (pozitif yon) | curutuldu (pozitif yon) | hayir |
| cifar100 | K-c | destek | destek | hayir | destek | destek | hayir |

cifar10: Holm p bootstrap p'lerinden (K-a, K-b, K-c) 1.50e-03, 1.50e-03, 1.50e-03; dondurulmus Holm p 1.26e-04, 2.73e-03, 1.00e-03; degisen sinama yok (delta 0,06: yok). Nokta kestirimleri ile dondurulmus JSON en buyuk mutlak fark 0.00e+00 (nokta_esit evet); K-c yeniden uretim farki ci90 0.00e+00, ci95 0.00e+00, p 0.00e+00, yeniden cekilen tek tohumlu ornek 284 (dondurulmus 284; K-c_esit evet); bootstrap kopyalarinda bir ciftte D <= 0,10 olan kopya sayisi 0 (cift duzeyi varyant 0); bootstrap p tabani 1/(B+1) (turetilmis) 5.00e-04.

cifar100: Holm p bootstrap p'lerinden (K-a, K-b, K-c) 1.50e-03, 9.70e-01, 1.50e-03; dondurulmus Holm p 2.05e-03, 9.53e-01, 1.50e-03; degisen sinama yok (delta 0,06: yok). Nokta kestirimleri ile dondurulmus JSON en buyuk mutlak fark 0.00e+00 (nokta_esit evet); K-c yeniden uretim farki ci90 0.00e+00, ci95 0.00e+00, p 0.00e+00, yeniden cekilen tek tohumlu ornek 284 (dondurulmus 284; K-c_esit evet); bootstrap kopyalarinda bir ciftte D <= 0,10 olan kopya sayisi 0 (cift duzeyi varyant 0); bootstrap p tabani 1/(B+1) (turetilmis) 5.00e-04.

_Kaynak: `results/q1/konsey_ek_masa/bootstrap_cifar10.json`, `results/q1/konsey_ek_masa/bootstrap_cifar100.json` etiket, tanim, meta.{betik_sha256, dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, veri, blok, matris_dizini, hucre_tablosu, dondurulmus_cikti, B, bootstrap_tohum, tohum_kaynagi, n_goruntu}; K-a.{nokta_ort_q, t_ci90, t_ci95, bootstrap, cift_duzeyi_varyant}; K-b.{nokta_ort_rho, t_ci90, t_ci95, t_tost_p, bootstrap, cift_duzeyi_varyant}; K-c.{Delta_w, yeniden_bootstrap, dondurulmus_bootstrap}; karar.{kural, karsilastirma, degisen, p_holm_bootstrap, p_holm_dondurulmus, delta_0.06}; dogrulama.{nokta_kestirimleri_dondurulmus_json_ile_maks_fark, nokta_esit, K-c_yeniden_uretim_maks_fark, K-c_esit}; `experiments/q1_ek_masa.py` sha256 bu betikte hashlib ile_


### M11.2 S10-3: aile gostergeli kismi Mantel (ek on kayit §6.4)

Etiket (`etiket`): on kayitli (ek on kayit §6.4, kesifsel oncelik), sonradan uretildi (31.10.2026, hakem paneli sonrasi).

Tanim (`tanim_S10_3`): Ek on kayit §6.4 S10-3: 'ayni aileden olma gostergesini (CNN-CNN, donusturucu-donusturucu, karma) ek ortak degisken alan kismi Mantel'. Uygulama (ek §6.2 kismi istatistiginin dogal uzantisi): sirasiz ciftler uzerinde her matris (c ve log tau ayri ayri) X_ij = mu + a_i + a_j + b_CC*CC_ij + b_TT*TT_ij + e_ij modeliyle deger olceginde en kucuk kareler ile kestirilir (karma ciftler referans; aile: hucre tablosundaki 'aile' alani, CNN = CNN, ViT/XCiT/Swin = donusturucu); istatistik e(c) ile e(log tau) arasindaki Spearman korelasyonudur. Permutasyon (birincil, ek §6.2'deki 'kismi istatistikte c artik matrisi' kuralinin aynisi; Smouse, Long ve Sokal 1986 artik permutasyonu): e(c) artik matrisinin satir ve sutunlari ortak permute edilir, e(log tau) sabit; 9999 permutasyon, tohum 20261030, p_tek = (1 + #{r* >= r})/(perm + 1). Duyarlilik: ham c matrisi permute edilip sabit tasarima gore yeniden artiklanir (Legendre ve Legendre 2012 'ham X permutasyonu'; gradyan betiginin kismi Mantel semasi).

Ek §6.2 yeniden uretim tanimi (`tanim_6_2_yeniden_uretim`): Ek §6.2 yeniden uretimi: ham = Spearman(ust c, ust log tau), c'nin satir/sutun ortak permutasyonu; ana_etki_artik = e_ij artiklari (X_ij = mu + a_i + a_j, deger olceginde en kucuk kareler) arasinda Spearman, c artik matrisinin ortak permutasyonu; 9999 permutasyon, tohum 20261030 (her sinama kendi RNG'siyle). Kod gradyan betiginden bagimsizdir (I - X X^+ izdusumu, scipy rankdata, Pearson).

`results/q1/konsey_ek_masa/mantel_aile.json` meta: betik_sha256 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (dosyadan hesaplanan 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1; AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389; uretildi_utc 2026-10-31T15:06:36.581560+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 6. Permutasyon 9999; tohum 20261030 (ek on kayit §6.2 (20261030)).

| Veri kumesi | K (model) | Cift sayisi | Cift turu CNN-CNN / donusturucu-donusturucu / karma | Tasarim rank (ana etki / ana etki + aile) | S10-3 r | Tek yonlu p | Iki yonlu p | Permutasyon ort / SD | Duyarlilik r (ham c permutasyonu) | Duyarlilik tek yonlu p | Permutasyon | Tohum | p tabani 1/(perm+1) (turetilmis) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cifar10 | 20 | 190 | 91 / 15 / 84 | 20 / 21 | +0.917 | 1.00e-04 | 1.00e-04 | +0.001 / 0.074 | +0.917 | 1.00e-04 | 9999 | 20261030 | 1.00e-04 |
| cifar100 | 15 | 105 | 55 / 6 / 44 | 15 / 16 | +0.882 | 1.00e-04 | 1.00e-04 | +0.002 / 0.101 | +0.882 | 1.00e-04 | 9999 | 20261030 | 1.00e-04 |
| imagenetv2 | 14 | 91 | 36 / 10 / 45 | 14 / 15 | +0.878 | 1.00e-04 | 1.00e-04 | +0.000 / 0.112 | +0.878 | 1.00e-04 | 9999 | 20261030 | 1.00e-04 |

Ek §6.2 istatistiklerinin bagimsiz yeniden uretimi (`veri.<veri>.yeniden_uretim_6_2`) ve `results/q1/konsey_b10_gradyan/mantel_<veri>.json` sinamalar.<sinama> ile karsilastirma:

| Veri kumesi | Sinama | r (yeniden) | Tek yonlu p (yeniden) | r (mantel JSON) | Tek yonlu p (mantel JSON) | |fark| r (bu betik) | En buyuk |fark| (istatistik, p_tek, p_iki, perm_ort, perm_sd; JSON) | Esit (1e-6) |
|---|---|---|---|---|---|---|---|---|
| cifar10 | ham | +0.943 | 1.00e-04 | +0.943 | 1.00e-04 | 0.00e+00 | 2.17e-19 | evet |
| cifar10 | ana_etki_artik | +0.944 | 1.00e-04 | +0.944 | 1.00e-04 | 0.00e+00 | 2.17e-19 | evet |
| cifar100 | ham | +0.981 | 1.00e-04 | +0.981 | 1.00e-04 | 1.11e-16 | 1.11e-16 | evet |
| cifar100 | ana_etki_artik | +0.912 | 1.00e-04 | +0.912 | 1.00e-04 | 1.11e-16 | 1.11e-16 | evet |
| imagenetv2 | ham | +0.694 | 1.00e-04 | +0.694 | 1.00e-04 | 0.00e+00 | 2.78e-17 | evet |
| imagenetv2 | ana_etki_artik | +0.893 | 1.00e-04 | +0.893 | 1.00e-04 | 1.11e-16 | 1.11e-16 | evet |

Tolerans 1e-06; yeniden_uretim_hepsi_esit_1e-6 evet; c ve log tau matris simetrisi en buyuk asimetri: cifar10 c 0.0e+00, log tau 0.0e+00; cifar100 c 0.0e+00, log tau 0.0e+00; imagenetv2 c 0.0e+00, log tau 0.0e+00.

Model gruplari (`veri.<veri>.modeller`, `.aile`, `.grup`): cifar10: donusturucu = ViT_Tiny_AT_s2001, ViT_Tiny_AT_s2002, ViT_Tiny_AT_s2003, V_IN_s2101, V_IN_s2102, Debenedetti2022Light_XCiT-S12; cifar100: donusturucu = C100_ViT_Tiny_AT_s2001, C100_ViT_Tiny_AT_s2002, C100_ViT_Tiny_AT_s2003, C100_Debenedetti2022Light_XCiT-S12; imagenetv2: donusturucu = IN_Singh_ViT-S-CvSt, IN_Singh_ViT-B-CvSt, IN_Liu_Swin-B, IN_Mo_ViT-B, IN_Debenedetti_XCiT-S12.

_Kaynak: `results/q1/konsey_ek_masa/mantel_aile.json` etiket, tanim_S10_3, tanim_6_2_yeniden_uretim, tolerans, yeniden_uretim_hepsi_esit_1e-6, meta.{betik_sha256, dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, perm, tohum, tohum_kaynagi}; veri.<veri>.{K, cift_sayisi, cift_turu_sayilari, tasarim_rank, S10_3, S10_3_duyarlilik_ham_c_permutasyonu, yeniden_uretim_6_2, mantel_json_karsilastirma, simetri, modeller, grup}; `results/q1/konsey_b10_gradyan/mantel_<veri>.json` sinamalar.{ham, ana_etki_artik}.{istatistik, p_tek}_


### M11.3 Kesifsel: aile ici kisitli permutasyon, aile ayiklamali ve CNN-CNN artik Spearman, R18-R50 ve en kucuk c_ij

Etiket (`etiket`): kesifsel.

Tanim `aile_ici_kisitli_permutasyon`: Ek §6.2'nin ham ve ana_etki_artik istatistikleri ayni; permutasyon yalniz ayni grup icinde (CNN modelleri kendi aralarinda, donusturuculer kendi aralarinda) yapilir; grup sirasi CNN, donusturucu; her grupta indeksler artan sirada; 9999 permutasyon, tohum 20261030; p_tek = (1 + #{r* >= r})/(perm + 1). Kisitli permutasyon sayisi n_CNN! x n_donusturucu! olarak raporlanir.

Tanim `aile_ayiklamali_artik_spearman_sira`: 11_sonuc_b8_b10.md §7 yontemi: ana etki artiklari e(c), e(log tau) (deger olceginde) siraya cevrilir; siralar [1, CC, TT] (gostergelerin siralari) uzerine en kucuk kareyle ayiklanir; istatistik ayiklanmis siralar arasindaki Pearson (sira kismi korelasyonu). Permutasyon: e(c) artik matrisi ortak permute edilir, e(log tau) ve gostergeler sabit (gradyan betiginin kismi Mantel semasi); 9999, tohum 20261030. 'deger_olcegi_farki' = bu istatistik eksi mantel_aile.json S10_3 istatistigi (ayni veri; ayiklama deger olceginde).

Tanim `cnn_cnn_artik_spearman`: (i) tam_matris_artigi: butun modellerle kestirilmis ana etki artiklari yalniz CNN-CNN ciftlerine sinirlanir; Spearman; p: e(c) artik matrisinin CNN blogunda CNN etiketleri ortak permute edilir. (ii) cnn_alt_matrisi: toplamsal model yalniz CNN alt matrisinde yeniden kestirilir; Spearman; Mantel p ayni bicimde. 9999, tohum 20261030.

Tanim `r18_r50_ve_en_kucuk_c`: mantel_imagenetv2.json c_matrisi ve log_tau_matrisi'nden IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 hucresi; sira = kosegen disi sirasiz ciftlerdeki artan sira (1 = en kucuk); en kucuk c_ij ve onu veren cift; her veri kumesi.

`results/q1/konsey_ek_masa/kesifsel.json` meta: betik_sha256 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (dosyadan hesaplanan 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1; AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389; uretildi_utc 2026-10-31T15:07:01.403456+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 6. Permutasyon 9999; tohum 20261030.

(a) Aile ici kisitli permutasyonla Mantel (`veri.<veri>.aile_ici_kisitli_permutasyon`):

| Veri kumesi | n CNN | n donusturucu | Kisitli permutasyon sayisi | Sinama | r | Tek yonlu p | Iki yonlu p | Permutasyon ort / SD | Permutasyon |
|---|---|---|---|---|---|---|---|---|---|
| cifar10 | 14 | 6 | 62768369664000 | ham | +0.943 | 1.00e-04 | 1.00e-04 | +0.461 / 0.099 | 9999 |
| cifar10 | 14 | 6 | 62768369664000 | ana_etki_artik | +0.944 | 1.00e-04 | 1.00e-04 | +0.447 / 0.091 | 9999 |
| cifar100 | 11 | 4 | 958003200 | ham | +0.981 | 1.00e-04 | 1.00e-04 | +0.389 / 0.183 | 9999 |
| cifar100 | 11 | 4 | 958003200 | ana_etki_artik | +0.912 | 1.00e-04 | 1.00e-04 | +0.284 / 0.147 | 9999 |
| imagenetv2 | 9 | 5 | 43545600 | ham | +0.694 | 1.00e-04 | 1.00e-04 | -0.008 / 0.165 | 9999 |
| imagenetv2 | 9 | 5 | 43545600 | ana_etki_artik | +0.893 | 1.00e-04 | 1.00e-04 | +0.072 / 0.109 | 9999 |

(b) Aile ayiklamali artik Spearman, sira olcegi (`veri.<veri>.aile_ayiklamali_artik_spearman_sira`):

| Veri kumesi | r (sira olcegi) | Tek yonlu p | Iki yonlu p | Permutasyon ort / SD | r (deger olcegi, M11.2 S10-3 ile ayni hesap) | Fark sira - deger (4 ondalik) | Permutasyon |
|---|---|---|---|---|---|---|---|
| cifar10 | +0.905 | 1.00e-04 | 1.00e-04 | +0.000 / 0.076 | +0.917 | -0.0123 | 9999 |
| cifar100 | +0.892 | 1.00e-04 | 1.00e-04 | +0.002 / 0.102 | +0.882 | +0.0106 | 9999 |
| imagenetv2 | +0.888 | 1.00e-04 | 1.00e-04 | +0.000 / 0.113 | +0.878 | +0.0095 | 9999 |

(c) Yalniz CNN-CNN ciftlerinde artik Spearman (`veri.<veri>.cnn_cnn_artik_spearman`):

| Veri kumesi | n CNN | Cift sayisi | r, tam matris artigi | Tek yonlu p | r, CNN alt matrisi artigi | Tek yonlu p | CNN-CNN ham Spearman (c, log tau) |
|---|---|---|---|---|---|---|---|
| cifar10 | 14 | 91 | +0.963 | 1.00e-04 | +0.965 | 1.00e-04 | +0.818 |
| cifar100 | 11 | 55 | +0.929 | 1.00e-04 | +0.926 | 1.00e-04 | +0.978 |
| imagenetv2 | 9 | 36 | +0.842 | 3.00e-04 | +0.824 | 3.00e-04 | +0.567 |

(d) c_ij ozeti (`veri.<veri>.c_ozet`; c 4 ondalik):

| Veri kumesi | En kucuk c_ij (cift) | O ciftin log tau | Ikinci en kucuk c_ij (cift) | En buyuk kosegen disi c_ij |
|---|---|---|---|---|
| cifar10 | 0.2312 (ViT_Tiny_AT_s2002 - Carmon2019Unlabeled) | -1.123 | 0.2325 (ViT_Tiny_AT_s2001 - Carmon2019Unlabeled) | 0.7461 |
| cifar100 | 0.1692 (C100_ViT_Tiny_AT_s2003 - C100_Hendrycks2019Using) | -1.118 | 0.1810 (C100_ViT_Tiny_AT_s2002 - C100_Hendrycks2019Using) | 0.6920 |
| imagenetv2 | 0.0034 (IN_Salman2020Do_R18 - IN_Salman2020Do_R50) | -0.936 | 0.0703 (IN_Salman2020Do_50_2 - IN_Chen2024Data_WRN_50_2) | 0.4855 |

ImageNetV2 IN_Salman2020Do_R18 - IN_Salman2020Do_R50 (`veri.imagenetv2.c_ozet.R18_R50`): c 0.0034 (simetrik hucre 0.0034); log tau -0.936 (simetrik hucre -0.936); c sirasi 1/91 (artan, 1 = en kucuk); log tau sirasi 55/91; ana etki artigi c 0.0084, log tau +0.366.

Bu bolumde (M11.1-M11.3) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: yok.

_Kaynak: `results/q1/konsey_ek_masa/kesifsel.json` etiket, tanim, meta.{betik_sha256, dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, perm, tohum}; veri.<veri>.{n_CNN, n_donusturucu, kisitli_permutasyon_sayisi, aile_ici_kisitli_permutasyon, aile_ayiklamali_artik_spearman_sira, cnn_cnn_artik_spearman, c_ozet}_


## M12: Hakem paneli acik isleri A2, A9 ve A10 (2026-10-31)

_Kaynak: `results/q1/konsey_ek_masa/a2_basit_etkiler.json; results/q1/konsey_ek_masa/a9_2q_eksi_1.json; results/q1/konsey_ek_masa/a10_panel.json; results/q1/konsey_ek_masa/a10_b4.json ve a10_b2.json (dondurulmus betik ciktilari, a10_panel.json icinden okunur); arsiv/b2_yardimci/_m12_ek_masa.py (yalniz sha256)`_

Hakem paneli acik isleri A2 (2x2 basit etkiler), A9 (2q - 1) ve A10 (ResNet-18 turevleri cikarilmis panel). Her alt bolum kendi JSON'undan okunur; etiketler JSON'un 'etiket' alanindandir. Yuvarlama: log olcekli nicelikler ve oranlar 3 ondalik, standartlastirilmis etki 2 ondalik, p degerleri bilimsel gosterim.


### M12.1 2x2 basit etkiler ve turetilmis hucre farklari: sigma ve rho (A2; B4, CIFAR-10)

Etiket (`etiket`): kesifsel, on kayit disi (31.10.2026, hakem paneli acik isi A2; turetilmis karsitliklar).

Tanim (`tanim`): Model duzeyi sigma ve rho dondurulmus model_duzeyi() ile (bolunmus yari, log olcek, birincil panel P, 7 uye) hesaplanir; hucreler dondurulmus hucre_uyeleri() ile (V-scr 3, V-IN 2, R224-scr 2, R224-IN 2 kosu). Karsitlik katsayilari KONTR sozlugundedir. (i) Birlesik varyansli t: dondurulmus karsitlik(deger, katsayi, HUC4); varyans dort hucreden birlestirilir (df = 1 + 1 + 1 + 2 = 5), H1-H3 ile ayni yontem; p_iki iki yonlu t. (ii) Welch: ayni islevin welch alani (yalniz katsayisi sifir olmayan hucreler). (iii) Hiyerarsik bootstrap: dondurulmus b4_coz() akisinin birebir kopyasi (rng = default_rng(BOOT_TOHUM = 20261029); once goruntu agirliklari W = bootstrap_agirlik(n, 2000, rng); her kopyada HUC4 sirasinda hucre icinde kosular yerine koyarak cekilir); yuzdelik %90 (5-95) ve %95 (2,5-97,5). H1, H2, H3 araliklari dondurulmus JSON'un duyarlilik.hiyerarsik_bootstrap alaniyla karsilastirilir. (iv) Yalniz goruntu bootstrap: ayni W, kosular sabit (hucre ortalamasi butun kosular). Standartlastirilmis etki = kestirim / birlesik SD. Kesifsel Holm: on kayitli karsiligi olmayan karsitliklarin iki yonlu birlesik varyans p'leri (sigma: mimari_IN, baslatma_V, baslatma_R224, mimari_ana_etki; rho: mimari_scr, mimari_IN, baslatma_R224, etkilesim). Hucre ici aralik verilmez (hucre basina n = 2; V-scr 3); hucre ortalamalari betimseldir. Logit olcek duyarliligi ayni karsitliklarin birlesik varyansli t kestirimidir.

`results/q1/konsey_ek_masa/a2_basit_etkiler.json` meta: betik arsiv/b2_yardimci/_m12_ek_masa.py betik_sha256 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245 (dosyadan hesaplanan 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245; AYNI); kutuphane experiments/q1_ek_masa.py 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 (AYNI); uretildi_utc 2026-10-31T15:37:09.263421+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 405; girdilerden dosyasi simdi farkli olan: yok. Veri cifar10 (B4); matris results/q1/konsey_b4_matris; hucre tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json; dondurulmus cikti results/q1/konsey_ayrisim_b4.json; B 2000; bootstrap tohumu 20261029 (dondurulmus betigin BOOT_TOHUM sabiti; RNG akisi dondurulmus b4_coz ile ayni); n_goruntu 10000; panel Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra, Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm.

(a) Bolunmus yari, log olcek; dort hucre birlesik varyansli t (`karsitliklar.<sigma|rho>.<ad>`.{tanim, kestirim, ci90, ci95, df, p_iki, p_holm_kesifsel_aile, standart_etki_kestirim_bolu_sp, on_kayitli_karsiligi}):

| Nicelik | Karsitlik | Tanim | Kestirim | t %90 | t %95 | df | p (iki yonlu) | Holm p (kesifsel aile) | Kestirim / birlesik SD | On kayitli karsiligi |
|---|---|---|---|---|---|---|---|---|---|---|
| sigma | mimari_scr | V-scr - R224-scr (sifirdan baslatmada mimari basit etkisi) | -0.364 | [-0.415; -0.314] | [-0.428; -0.300] | 5 | 2.72e-05 | - | -13.33 | H1 (F_B4) |
| sigma | mimari_IN | V-IN - R224-IN (ImageNet baslatmada mimari basit etkisi) | -0.104 | [-0.159; -0.049] | [-0.174; -0.034] | 5 | 1.25e-02 | 4.99e-02 | -3.81 | yok (yeni, kesifsel) |
| sigma | baslatma_V | V-IN - V-scr (ViT'te baslatma basit etkisi) | +0.270 | [+0.219; +0.320] | [+0.205; +0.334] | 5 | 1.18e-04 | 8.25e-04 | +9.86 | yok (yeni, kesifsel) |
| sigma | baslatma_R224 | R224-IN - R224-scr (ResNet-224'te baslatma basit etkisi) | +0.009 | [-0.046; +0.065] | [-0.061; +0.080] | 5 | 7.44e-01 | 1.00e+00 | +0.35 | yok (yeni, kesifsel) |
| sigma | etkilesim | (V-IN - V-scr) - (R224-IN - R224-scr) = mimari_IN - mimari_scr | +0.260 | [+0.186; +0.335] | [+0.165; +0.355] | 5 | 9.00e-04 | - | +9.52 | H2 (F_B4) |
| sigma | mimari_ana_etki | 1/2 (mimari_scr + mimari_IN), baslatma uzerinden ortalanmis mimari etkisi | -0.234 | [-0.271; -0.197] | [-0.282; -0.187] | 5 | 5.47e-05 | 4.38e-04 | -8.57 | yok (yeni, kesifsel) |
| rho | mimari_scr | V-scr - R224-scr (sifirdan baslatmada mimari basit etkisi) | +0.070 | [+0.039; +0.101] | [+0.031; +0.110] | 5 | 6.00e-03 | 3.00e-02 | +4.17 | yok (yeni, kesifsel) |
| rho | mimari_IN | V-IN - R224-IN (ImageNet baslatmada mimari basit etkisi) | -0.064 | [-0.098; -0.030] | [-0.107; -0.020] | 5 | 1.30e-02 | 4.99e-02 | -3.77 | yok (yeni, kesifsel) |
| rho | baslatma_V | V-IN - V-scr (ViT'te baslatma basit etkisi) | -0.130 | [-0.161; -0.099] | [-0.169; -0.090] | 5 | 3.86e-04 | - | -7.69 | S2 (ikincil, ON_KAYIT §5) |
| rho | baslatma_R224 | R224-IN - R224-scr (ResNet-224'te baslatma basit etkisi) | +0.004 | [-0.030; +0.038] | [-0.039; +0.048] | 5 | 8.13e-01 | 1.00e+00 | +0.25 | yok (yeni, kesifsel) |
| rho | etkilesim | (V-IN - V-scr) - (R224-IN - R224-scr) = mimari_IN - mimari_scr | -0.134 | [-0.180; -0.088] | [-0.193; -0.075] | 5 | 2.04e-03 | 1.22e-02 | -7.94 | yok (yeni, kesifsel) |
| rho | mimari_ana_etki | 1/2 (mimari_scr + mimari_IN), baslatma uzerinden ortalanmis mimari etkisi | +0.003 | [-0.020; +0.026] | [-0.026; +0.033] | 5 | 7.80e-01 | - | +0.20 | H3 (F_B4) |

(b) Duyarlilik araliklari (`karsitliklar.<sigma|rho>.<ad>`.{welch, hiyerarsik_bootstrap, yalniz_goruntu_bootstrap, logit_duyarlilik}):

| Nicelik | Karsitlik | Welch %90 | Welch df | Hiyerarsik bootstrap %90 | Hiyerarsik bootstrap %95 | Yalniz goruntu bootstrap %90 | Logit kestirim | Logit t %90 |
|---|---|---|---|---|---|---|---|---|
| sigma | mimari_scr | [-0.472; -0.256] | 1.10 | [-0.393; -0.335] | [-0.397; -0.330] | [-0.378; -0.350] | -0.498 | [-0.570; -0.426] |
| sigma | mimari_IN | [-0.318; +0.109] | 1.07 | [-0.151; -0.058] | [-0.155; -0.053] | [-0.116; -0.092] | -0.144 | [-0.223; -0.065] |
| sigma | baslatma_V | [+0.043; +0.496] | 1.03 | [+0.223; +0.315] | [+0.218; +0.320] | [+0.256; +0.283] | +0.372 | [+0.300; +0.444] |
| sigma | baslatma_R224 | [-0.084; +0.102] | 1.26 | [-0.019; +0.036] | [-0.023; +0.040] | [-0.001; +0.020] | +0.018 | [-0.061; +0.097] |
| sigma | etkilesim | [+0.113; +0.407] | 1.63 | [+0.204; +0.316] | [+0.196; +0.324] | [+0.243; +0.277] | +0.354 | [+0.247; +0.461] |
| sigma | mimari_ana_etki | [-0.308; -0.161] | 1.63 | [-0.262; -0.207] | [-0.265; -0.202] | [-0.244; -0.224] | -0.321 | [-0.374; -0.267] |
| rho | mimari_scr | [-0.031; +0.172] | 1.21 | [+0.028; +0.114] | [+0.021; +0.121] | [+0.043; +0.099] | -0.061 | [-0.092; -0.030] |
| rho | mimari_IN | [-0.140; +0.013] | 1.04 | [-0.096; -0.033] | [-0.103; -0.026] | [-0.087; -0.040] | -0.112 | [-0.146; -0.079] |
| rho | baslatma_V | [-0.182; -0.078] | 1.54 | [-0.171; -0.092] | [-0.177; -0.086] | [-0.159; -0.103] | -0.034 | [-0.065; -0.003] |
| rho | baslatma_R224 | [-0.122; +0.130] | 1.02 | [-0.030; +0.038] | [-0.037; +0.043] | [-0.015; +0.024] | +0.017 | [-0.017; +0.051] |
| rho | etkilesim | [-0.208; -0.060] | 1.95 | [-0.184; -0.086] | [-0.195; -0.076] | [-0.168; -0.100] | -0.051 | [-0.097; -0.005] |
| rho | mimari_ana_etki | [-0.034; +0.041] | 1.95 | [-0.024; +0.031] | [-0.030; +0.036] | [-0.016; +0.023] | -0.087 | [-0.110; -0.064] |

(c) Hucre ozetleri, betimsel (`hucre_ozetleri.<nicelik>.<hucre>`; hucre ici aralik yok):

| Nicelik | Hucre | n | Kosu degerleri | Ortalama | SD | Aralik |
|---|---|---|---|---|---|---|
| sigma | V-scr | 3 | -1.015, -1.000, -1.011 | -1.009 | 0.007 | aralik yok, betimsel (hucre ici n = 3) |
| sigma | V-IN | 2 | -0.702, -0.776 | -0.739 | 0.053 | aralik yok, betimsel (hucre ici n = 2) |
| sigma | R224-scr | 2 | -0.625, -0.664 | -0.645 | 0.027 | aralik yok, betimsel (hucre ici n = 2) |
| sigma | R224-IN | 2 | -0.642, -0.628 | -0.635 | 0.010 | aralik yok, betimsel (hucre ici n = 2) |
| rho | V-scr | 3 | +0.025, +0.007, +0.004 | +0.012 | 0.011 | aralik yok, betimsel (hucre ici n = 3) |
| rho | V-IN | 2 | -0.131, -0.105 | -0.118 | 0.018 | aralik yok, betimsel (hucre ici n = 2) |
| rho | R224-scr | 2 | -0.038, -0.079 | -0.058 | 0.029 | aralik yok, betimsel (hucre ici n = 2) |
| rho | R224-IN | 2 | -0.056, -0.052 | -0.054 | 0.003 | aralik yok, betimsel (hucre ici n = 2) |
| omega | V-scr | 3 | +4.024, +4.023, +4.009 | +4.019 | 0.008 | aralik yok, betimsel (hucre ici n = 3) |
| omega | V-IN | 2 | +3.876, +3.934 | +3.905 | 0.041 | aralik yok, betimsel (hucre ici n = 2) |
| omega | R224-scr | 2 | +3.899, +3.881 | +3.890 | 0.013 | aralik yok, betimsel (hucre ici n = 2) |
| omega | R224-IN | 2 | +3.878, +3.866 | +3.872 | 0.009 | aralik yok, betimsel (hucre ici n = 2) |

Kesifsel Holm ailesi (`kesifsel_holm.aile`): sigma.mimari_IN, sigma.baslatma_V, sigma.baslatma_R224, sigma.mimari_ana_etki, rho.mimari_scr, rho.mimari_IN, rho.baslatma_R224, rho.etkilesim. Dogrulama (`dogrulama`): model duzeyi sigma ve rho ile dondurulmus JSON en buyuk mutlak fark 0.00e+00; on kayitli karsitliklar (H1, H2, H3, S2) kestirim ve t araliklari en buyuk fark 0.00e+00; hiyerarsik bootstrap H1-H3 araliklari ile dondurulmus `duyarlilik.hiyerarsik_bootstrap` en buyuk fark 0.00e+00; hedef maskesi tutarli evet.

_Kaynak: `results/q1/konsey_ek_masa/a2_basit_etkiler.json` etiket, tanim, meta.{betik, betik_sha256, kutuphane_betik, kutuphane_betik_sha256_dogrulandi, dondurulmus_betik_sha256_dogrulandi, uretildi_utc, numpy, scipy, girdi_sha256, veri, blok, matris_dizini, hucre_tablosu, dondurulmus_cikti, B, bootstrap_tohum, tohum_kaynagi, n_goruntu, panel}; karsitliklar.<sigma|rho>.<ad>; hucre_ozetleri; kesifsel_holm; dogrulama; `arsiv/b2_yardimci/_m12_ek_masa.py` sha256 bu betikte hashlib ile_


### M12.2 K-a icin turetilmis 2q - 1 satiri (A9; CIFAR-10 B2, CIFAR-100 B9)

Etiket (`etiket`): turetilmis (31.10.2026, hakem paneli acik isi A9; 2q - 1, K-a'nin dogrusal donusumu).

Tanim (`tanim`): q_s = simetrik_pay_s / D_s (K-a, dondurulmus F_B2). 1 - q_s yonlu payin D'deki payidir (ozdeslik D = simetrik + yonlu). 2q - 1 = (simetrik pay - yonlu pay)/D: simetrik payin yonlu payi D cinsinden asma orani; q = 0,5 (K-a'nin sifir hipotezi) 2q - 1 = 0'a karsilik gelir. Ortalama: 2 ort(q) - 1. Dogrusal donusum oldugundan t araliklari (dondurulmus F_B2.K-a.sinama.ci90/ci95) ve hiyerarsik bootstrap yuzdelik araliklari (M11.1, K-a.bootstrap) uc noktalarin 2x - 1 donusumudur; p degerleri K-a'nin p'leriyle aynidir. Denetim: kosu basina (simetrik - yonlu)/D ile 2q - 1 arasindaki en buyuk fark.

`results/q1/konsey_ek_masa/a9_2q_eksi_1.json` meta: betik arsiv/b2_yardimci/_m12_ek_masa.py betik_sha256 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245 (dosyadan hesaplanan 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245; AYNI); kutuphane experiments/q1_ek_masa.py 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 (AYNI); uretildi_utc 2026-10-31T15:37:09.266134+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 4; girdilerden dosyasi simdi farkli olan: yok.

| Veri | Ort q (kaynak) | 2 ort(q) - 1 | Kosu basina 2q - 1 (cift sirasiyla) | t %90 | t %95 | Hiyerarsik bootstrap %90 | Hiyerarsik bootstrap %95 | Tek yonlu p (H0: 2q - 1 <= 0; K-a p'si) | Kaynak satiri |
|---|---|---|---|---|---|---|---|---|---|
| cifar10 | 0.936 | +0.873 | +0.881, +0.857, +0.880 | [+0.849; +0.896] | [+0.838; +0.907] | [+0.787; +0.961] | [+0.773; +0.982] | 4.19e-05 | `results/q1/konsey_ayrisim_b2.json` b2.F_B2.K-a.{q, D, simetrik_pay, yonlu_pay, sinama.ort, sinama.ci90, sinama.ci95, p_tek_H0_q_le_0.5, ciftler}; `results/q1/konsey_ek_masa/bootstrap_cifar10.json` K-a.{nokta_ort_q, bootstrap.ci90, bootstrap.ci95} |
| cifar100 | 0.840 | +0.679 | +0.696, +0.723, +0.620 | [+0.589; +0.769] | [+0.547; +0.812] | [+0.599; +0.761] | [+0.580; +0.780] | 1.02e-03 | `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` b2.F_B2.K-a.{q, D, simetrik_pay, yonlu_pay, sinama.ort, sinama.ci90, sinama.ci95, p_tek_H0_q_le_0.5, ciftler}; `results/q1/konsey_ek_masa/bootstrap_cifar100.json` K-a.{nokta_ort_q, bootstrap.ci90, bootstrap.ci95} |

cifar10 denetim (`veri.cifar10.denetim`): kosu basina (simetrik - yonlu)/D ile 2q - 1 en buyuk fark 1.22e-15; dondurulmus ozdeslik artigi 4.27e-16; M11.1 bootstrap JSON nokta ort q ile dondurulmus ort q farki 0.00e+00; ciftler ResNet18_AT_s1001 / ViT_Tiny_AT_s2001; ResNet18_AT_s1002 / ViT_Tiny_AT_s2002; ResNet18_AT_s1003 / ViT_Tiny_AT_s2003.

cifar100 denetim (`veri.cifar100.denetim`): kosu basina (simetrik - yonlu)/D ile 2q - 1 en buyuk fark 1.67e-15; dondurulmus ozdeslik artigi 7.77e-16; M11.1 bootstrap JSON nokta ort q ile dondurulmus ort q farki 0.00e+00; ciftler C100_ResNet18_AT_s1001 / C100_ViT_Tiny_AT_s2001; C100_ResNet18_AT_s1002 / C100_ViT_Tiny_AT_s2002; C100_ResNet18_AT_s1003 / C100_ViT_Tiny_AT_s2003.

_Kaynak: `results/q1/konsey_ek_masa/a9_2q_eksi_1.json` etiket, tanim, meta; veri.<veri>.{ort_q, iki_ort_q_eksi_1, iki_q_eksi_1_s, t_ci90, t_ci95, bootstrap_ci90, bootstrap_ci95, p_tek_H0_2q_eksi_1_le_0_(K-a ile ayni), kaynak, kaynak_anahtar, bootstrap_kaynak, bootstrap_anahtar, ciftler, denetim}_


### M12.3 ResNet-18 turevleri cikarilmis 3 uyeli panelle B4 ve B2 (A10; kesifsel, on kayit disi panel)

Etiket (`etiket`): kesifsel, on kayit disi panel, 3 uye (31.10.2026, hakem paneli acik isi A10).

Tanim (`tanim`): Panel uyesi 'ResNet-18 turevi' sayilir eger RobustBench (cifar10, Linf) model nesnesindeki iki evrisimli artik blok sayisi 8 ise (BasicBlock, PreActBlock, _PreActBlock; ResNet-18 ve PreAct-ResNet-18'in [2, 2, 2, 2] dizilimi). Nesneler robustbench.model_zoo.cifar10.linf sozlugunden CPU'da kurulur (agirlik yuklenmez); blok sinifi ve sayisi, Conv2d sayisi ve parametre sayisi kaydedilir. hucre_tablosu_a10.json dondurulmus tablonun kopyasidir; yalniz bu uyelerin birincil_panel alani false yapilir ve belgeleme icin 'a10_kesifsel' anahtari eklenir (dondurulmus betik bu anahtari okumaz). Dondurulmus betik degistirilmeden alt surecle cagrilir: once runbook bicimiyle (varsayilan --panel-en-az 5), sonra betigin istege bagli --panel-en-az 3 bayragiyla. ON_KAYIT §2'nin en az bes uyelik panel kurali bu ikinci cagrida bilerek gevsetilmistir; sonuclar on kayit disi ve kesifseldir, F_B2/F_B4 kararlarinin yerine gecmez. Dondurulmus panelle karsilastirmada 'ayni_yon' kestirim isaretinin, 'karar_ayni' karar dizgesinin aynen tutmasidir. Bagimsiz denetim: dondurulmus islevler importlib ile yuklenip 3 uyeli panelle H1-H3 kestirimleri ve K-a q, K-b rho yeniden hesaplanir ve alt surec ciktisiyla karsilastirilir.

`results/q1/konsey_ek_masa/a10_panel.json` meta: betik arsiv/b2_yardimci/_m12_ek_masa.py betik_sha256 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245 (dosyadan hesaplanan 57016d02354f205d712aace1ae3c210d8eae0ce6ceac669e2cac560694e93245; AYNI); kutuphane experiments/q1_ek_masa.py 40454344bd3f8b1a0318d4bdb295d1dad05f187d74fe22f739501654a785b8c1 (AYNI); dondurulmus_betik_sha256_dogrulandi 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 (AYNI); uretildi_utc 2026-10-31T15:37:24.179897+00:00; numpy 1.26.4; scipy 1.14.1; girdi dosyasi sayisi (girdi_sha256) 8; girdilerden dosyasi simdi farkli olan: yok. Matris dizinleri {'b4': 'results/q1/konsey_b4_matris', 'b2': 'results/q1/konsey_b2_panel'}; bootstrap B 2000, tohum 20261029; dondurulmus betige verilen panel_en_az 3.

(a) Mimari dogrulama (`mimari_dogrulama`; kaynak robustbench.model_zoo.cifar10.linf, /usr/local/lib/python3.12/dist-packages/robustbench):

| Panel uyesi (dondurulmus) | Sinif | MRO | Artik blok sinifi | Blok sayisi | Conv2d sayisi | Parametre sayisi | ResNet-18 turevi |
|---|---|---|---|---|---|---|---|
| Wong2020Fast | Wong2020FastNet | Wong2020FastNet > PreActResNet > Module > object | PreActBlock | 8 | 20 | 11171146 | evet |
| Engstrom2019Robustness | Engstrom2019RobustnessNet | Engstrom2019RobustnessNet > ResNet > Module > object | Bottleneck | 16 | 53 | 23520842 | hayir |
| Carmon2019Unlabeled | WideResNet | WideResNet > Module > object | BasicBlock | 16 | 37 | 38119866 | hayir |
| Gowal2020Uncovering_28_10_extra | DMWideResNet | DMWideResNet > Module > object | _Block | 12 | 28 | 36479194 | hayir |
| Sehwag2021Proxy_R18 | ResNet | ResNet > Module > object | BasicBlock | 8 | 20 | 11173962 | evet |
| Addepalli2022Efficient_RN18 | ResNet | ResNet > Module > object | BasicBlock | 8 | 20 | 11173962 | evet |
| Rade2021Helper_R18_ddpm | DMPreActResNet | DMPreActResNet > Module > object | _PreActBlock | 8 | 20 | 12548426 | evet |

Cikarilan (`cikarilan`): Wong2020Fast, Sehwag2021Proxy_R18, Addepalli2022Efficient_RN18, Rade2021Helper_R18_ddpm. Kalan panel (`kalan_panel`): Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra. Tablo farki (`tablo_farki`): modeller.Addepalli2022Efficient_RN18.birincil_panel, modeller.Rade2021Helper_R18_ddpm.birincil_panel, modeller.Sehwag2021Proxy_R18.birincil_panel, modeller.Wong2020Fast.birincil_panel. Varsayilan bayrakla dondurulmus betik (`varsayilan_bekci_hatasi`): b4 'birincil panelde 3 uye var; ON_KAYIT §2 en az 5 ister', b2 'birincil panelde 3 uye var; ON_KAYIT §2 en az 5 ister'.

(b) Dondurulmus betik cagrilari (`dondurulmus_cagrilar`):

| Cagri | Komut | Donus kodu | Cikti | Cikti sha256 |
|---|---|---|---|---|
| b4_varsayilan | `python -B experiments/q1_konsey_ayrisim.py --mod b4 --matris-dizini results/q1/konsey_b4_matris --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_a10.json --cikti results/q1/konsey_ek_masa/a10_b4_varsayilan_bekci.json` | 0 | `results/q1/konsey_ek_masa/a10_b4_varsayilan_bekci.json` | 60d752977472c5d3d2504775c5795cc9c94b71eb1ebfe9dd82e913f5a663f05a |
| b2_varsayilan | `python -B experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini results/q1/konsey_b2_panel --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_a10.json --cikti results/q1/konsey_ek_masa/a10_b2_varsayilan_bekci.json` | 0 | `results/q1/konsey_ek_masa/a10_b2_varsayilan_bekci.json` | 7f44e664e1e01b5c6081334643dde48d002c6f0e40ddd0f433f8c5fb054e97ce |
| b4 | `python -B experiments/q1_konsey_ayrisim.py --mod b4 --matris-dizini results/q1/konsey_b4_matris --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_a10.json --cikti results/q1/konsey_ek_masa/a10_b4.json --panel-en-az 3` | 0 | `results/q1/konsey_ek_masa/a10_b4.json` | 9340c12b90eb93cf7b4efd64fb5e5e850d2cffcff1b378adb66d868c2771bc27 |
| b2 | `python -B experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini results/q1/konsey_b2_panel --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_a10.json --cikti results/q1/konsey_ek_masa/a10_b2.json --panel-en-az 3` | 0 | `results/q1/konsey_ek_masa/a10_b2.json` | 5ab88eaa0069c451911b8d9579fd175749ec3c279dbca4b4240d107cbed6ef18 |

(c) B4 aile F_B4 (`b4_a10.<H>`, `b4_dondurulmus_panel.<H>`; bolunmus yari, log, birlesik varyans df 5):

| Hipotez | Panel | Kestirim | t %90 | t %95 | p ham | p Holm | Hiyerarsik bootstrap %90 | Welch %90 | Karar |
|---|---|---|---|---|---|---|---|---|---|
| H1 | 3 uye (A10) | -0.412 | [-0.465; -0.359] | [-0.479; -0.344] | 9.64e-06 | 2.89e-05 | [-0.445; -0.378] | [-0.553; -0.270] | destek |
| H2 | 3 uye (A10) | +0.295 | [+0.216; +0.373] | [+0.194; +0.395] | 6.45e-04 | 6.45e-04 | [+0.236; +0.355] | [+0.149; +0.440] | destek |
| H3 | 3 uye (A10) | +0.004 | [-0.021; +0.029] | [-0.028; +0.036] | 2.94e-04 | 5.89e-04 | [-0.028; +0.034] | [-0.031; +0.039] | destek (esdeger, Holm sonrasi TOST p < 0,05) |
| H1 | 7 uye (dondurulmus) | -0.364 | [-0.415; -0.314] | [-0.428; -0.300] | 1.36e-05 | 4.09e-05 | [-0.393; -0.335] | [-0.472; -0.256] | destek |
| H2 | 7 uye (dondurulmus) | +0.260 | [+0.186; +0.335] | [+0.165; +0.355] | 9.00e-04 | 9.00e-04 | [+0.204; +0.316] | [+0.113; +0.407] | destek |
| H3 | 7 uye (dondurulmus) | +0.003 | [-0.020; +0.026] | [-0.026; +0.033] | 1.89e-04 | 3.79e-04 | [-0.024; +0.031] | [-0.034; +0.041] | destek (esdeger, Holm sonrasi TOST p < 0,05) |

| Panel | Sonuc bolgesi | O4 niteleme | H2 logit kestirim | Karar, delta 0,06 | S2 rho(V-IN) - rho(V-scr) [%90] |
|---|---|---|---|---|---|
| 3 uye (A10) | O1 | hayir | +0.390 | H1 destek; H2 destek; H3 destek (esdeger, Holm sonrasi TOST p < 0,05) | -0.138 [-0.172; -0.104] |
| 7 uye (dondurulmus) | O1 | hayir | +0.354 | H1 destek; H2 destek; H3 destek (esdeger, Holm sonrasi TOST p < 0,05) | -0.130 [-0.161; -0.099] |

(d) B2 aile F_B2, CIFAR-10 (`b2_a10`, `b2_dondurulmus_panel`):

| Nicelik | Panel | Kestirim | Kosu degerleri | %90 | %95 | p ham | p Holm | Karar |
|---|---|---|---|---|---|---|---|---|
| K-a ort q | 3 uye (A10) | 0.921 | 0.923, 0.911, 0.928 | [0.905; 0.936] | [0.898; 0.943] | 7.67e-05 | 2.30e-04 | destek |
| K-b ort rho(V-scr) | 3 uye (A10) | +0.018 | +0.036, +0.011, +0.007 | [-0.008; +0.044] | [-0.020; +0.056] | TOST 5.77e-03 | 5.77e-03 | destek (Holm sonrasi TOST p < 0,05) |
| K-c Delta_w | 3 uye (A10) | +0.673 |  | bootstrap [+0.641; +0.714] |  | 5.00e-04 | 1.00e-03 | destek |
| K-a ort q | 7 uye (dondurulmus) | 0.936 | 0.940, 0.928, 0.940 | [0.925; 0.948] | [0.919; 0.953] | 4.19e-05 | 1.26e-04 | destek |
| K-b ort rho(V-scr) | 7 uye (dondurulmus) | +0.012 | +0.025, +0.007, +0.004 | [-0.007; +0.031] | [-0.016; +0.040] | TOST 2.73e-03 | 2.73e-03 | destek (Holm sonrasi TOST p < 0,05) |
| K-c Delta_w | 7 uye (dondurulmus) | +0.566 |  | bootstrap [+0.537; +0.604] |  | 5.00e-04 | 1.00e-03 | destek |

(e) Dondurulmus panelle karsilastirma (`karsilastirma`):

| Sinama | Kestirim, 7 uye | Kestirim, 3 uye | Ayni yon | Karar, 7 uye | Karar, 3 uye | Karar ayni |
|---|---|---|---|---|---|---|
| H1 | -0.364 | -0.412 | evet (kestirim isareti) | destek | destek | evet |
| H2 | +0.260 | +0.295 | evet (kestirim isareti) | destek | destek | evet |
| H3 | +0.003 | +0.004 | evet (kestirim isareti) | destek (esdeger, Holm sonrasi TOST p < 0,05) | destek (esdeger, Holm sonrasi TOST p < 0,05) | evet |
| sonuc_bolgesi |  |  |  | O1 | O1 | evet |
| K-a | +0.936 | +0.921 | evet (q - 0,5 isareti) | destek | destek | evet |
| K-b | +0.012 | +0.018 | evet (kestirim isareti) | destek (Holm sonrasi TOST p < 0,05) | destek (Holm sonrasi TOST p < 0,05) | evet |
| K-c | +0.566 | +0.673 | evet (kestirim isareti) | destek | destek | evet |

Bagimsiz yeniden hesap (`bagimsiz_yeniden_hesap`; dondurulmus islevler importlib ile, panel Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra): H1-H3 kestirim en buyuk fark 0.00e+00, t %90 en buyuk fark 0.00e+00; K-a q 0.00e+00; K-b rho 0.00e+00.

Bu bolumde (M12.1-M12.3) JSON'da bulunamayip 'bulunamadi' yazilan kalemler: yok.

_Kaynak: `results/q1/konsey_ek_masa/a10_panel.json` etiket, tanim, meta; mimari_dogrulama; cikarilan; kalan_panel; tablo_farki; dondurulmus_cagrilar; varsayilan_bekci_hatasi; b4_a10; b4_dondurulmus_panel; b2_a10; b2_dondurulmus_panel; karsilastirma; bagimsiz_yeniden_hesap (b4_a10 ve b2_a10 alanlari `results/q1/konsey_ek_masa/a10_b4.json` ile `results/q1/konsey_ek_masa/a10_b2.json` dosyalarindan, dondurulmus panel alanlari `results/q1/konsey_ayrisim_b4.json` ile `results/q1/konsey_ayrisim_b2.json` dosyalarindan kopyalanmistir)_


## M13: Sekil kaynaklari, tasarim tarifi, kayit haritasi ve zaman cizelgesi (2026-10-31)

_Kaynak: `results/q1/konsey_b3_tarif.json; results/q1/konsey_kayit_kurallari.json; results/q1/konsey_zaman_cizelgesi.json; arsiv/b2_yardimci/_m13_tarif.py, arsiv/b2_yardimci/_m13_kayit.py, arsiv/b2_yardimci/_m13_zaman.py, arsiv/b2_yardimci/_m13_ortak.py (yalniz sha256)`_

Uc yeni sekil (Y1 fig:design_recipe, Y4 fig:registry_map, Y5 fig:prereg_chain) icin makine okunur kaynaklardir. Her JSON uretici betiginin kaynak dosyalarindan okunur; degerin yaninda kaynak dosya ve satiri JSON'da yazilidir. Sonuc sayilari burada tekrarlanmaz; foyun ilgili satiri verilir ve satirin sha256'si bu calismada denetlenir.


### M13.1 Tasarim ve egitim tarifi: 2x2 hucreler ve R32 koprusu (Y1, fig:design_recipe)

Etiket (`etiket`): Y1 fig:design_recipe kaynagi: 2x2 tasarim ve egitim tarifi (B3 ve C1).

`results/q1/konsey_b3_tarif.json` meta: betik arsiv/b2_yardimci/_m13_tarif.py betik_sha256 08468c4725e935f09dc67d3f006afcefbfe13fd5b736ba08e12987222e25dde5 (dosyadan hesaplanan AYNI); ortak modul arsiv/b2_yardimci/_m13_ortak.py c17618e252c0d08b8b4a5e01960d676f4f9e71b9d80e39cfd9906b5cc1069d98 (AYNI); uretildi_utc 2026-10-31T18:18:19.218184+00:00; python 3.10.12; kaynak dosya sayisi (kaynaklar_sha256) 41; kaynaklardan simdi farkli olan (foy haric; foy satirlari satir sha256'siyla ayrica denetlenir): yok. Foy ozeti (`meta.foy_ozeti.m13_haric_sha256`; foyden '## M13:' bolumu cikarilmis metnin sha256'si, denetimi arsiv/b2_yardimci/_m13_kontrol.py): 00cc422f01c0d9641d46bebd544eea0cb2a915256906bacf77d7f898f937979f. Git'ten salt okunan surumler (`meta.git_kaynaklari.blob`): 7 dosya (77ae259, 77ae259^).

(a) Hucreler ve girdi hatti (`hucreler.<h>`.{blok, girdi_hatti, tohumlar, on_kayit_satiri}):

| Hucre | Blok | Model | Girdi hatti | Normalizasyon | Baslatma | Tohumlar | On kayit satiri | Kod kaynagi |
|---|---|---|---|---|---|---|---|---|
| V-scr | C1 (mevcut) | timm vit_tiny_patch16_224 | 32->224 bilinear buyutme | yok | rastgele | 2001, 2002, 2003 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:31` | `src/models/vit.py:386`; `src/models/vit.py:392`; `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:31` |
| V-IN | B3 (yeni) | timm vit_tiny_patch16_224 | 32->224 bilinear buyutme | model ici ImageNet (pretrained_cfg); ortalama [0.485, 0.456, 0.406], SD [0.229, 0.224, 0.225], cfg ile ayni evet (`logs/konsey_b3/V_IN_s2101_temiz.log:3`) | deit_tiny_patch16_224.fb_in1k | 2101, 2102 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:32` | `src/models/r224.py:75`; `src/models/r224.py:48`; `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:32` |
| R224-scr | B3 (yeni) | timm resnet18 | 32->224 bilinear buyutme | yok | rastgele | 1201, 1202 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:33` | `src/models/r224.py:114`; `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:33` |
| R224-IN | B3 (yeni) | timm resnet18 | 32->224 bilinear buyutme | model ici ImageNet (pretrained_cfg); ortalama [0.485, 0.456, 0.406], SD [0.229, 0.224, 0.225], cfg ile ayni evet (`logs/konsey_b3/R224_IN_s1301_temiz.log:3`) | resnet18.a1_in1k | 1301, 1302 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:34` | `src/models/r224.py:49`; `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:34` |
| C1-R32 | C1 (mevcut), kopru (S1, B2) | CIFAR ResNet-18 (3x3 kok, maxpool yok) | 32x32 (buyutme yok) | yok (resnet.py'de normalizasyon ve buyutme satiri sayisi 0) | rastgele | 1001, 1002, 1003 | hucre tablosu: C1 ResNet-18 AT, 32x32 girdi (mevcut, kopru karsitligi S1 ve B2) | `src/models/resnet.py:18`; `raporlar/konsey_2026-10-29/hucre_tablosu.json hucreler.C1-R32` |

(b) Temiz asama (`hucreler.<h>.kosular.<ilk kosu>.temiz`; B3 hucrelerinde iki kosu tohum disinda ozdes, bkz. denetimler):

| Hucre | Epok | Eniyileyici | lr (etkin) | Agirlik azaltma | Momentum | LR cizelgesi | Batch | --init-weights | Komut ve eniyileyici kaynagi |
|---|---|---|---|---|---|---|---|---|---|
| V-scr | 200 | AdamW | 0.001 | 0.05 | - | cosine (T_max 200) | 128 | none | `scripts/run_c1_pipeline.sh:58-60`; src/training/trainer.py:104; src/training/trainer.py:112; src/training/trainer.py:108 |
| V-IN | 30 | AdamW | 0.0001 | 0.05 | - | cosine (T_max 30) | 128 | deit_tiny_in1k | `logs/konsey_zincir.log:36`; src/training/trainer.py:91 |
| R224-scr | 200 | AdamW | 0.001 | 0.05 | - | cosine (T_max 200) | 128 | none | `logs/konsey_zincir.log:51`; src/training/trainer.py:91 |
| R224-IN | 30 | AdamW | 0.0001 | 0.05 | - | cosine (T_max 30) | 128 | resnet18_a1_in1k | `logs/konsey_zincir.log:47`; src/training/trainer.py:91 |
| C1-R32 | 200 | SGD | 0.1 | 0.0005 | 0.9 | cosine (T_max 200) | 128 | none | `scripts/run_c1_pipeline.sh:46-48`; src/training/trainer.py:104; src/training/trainer.py:33; src/training/trainer.py:34 |

(c) AT asamasi (`hucreler.<h>.kosular.<ilk kosu>.AT`; eps, alpha, adim ve gradyan kirpma cli/train.py varsayilanlari, satirlari JSON'da):

| Hucre | Epok tavani | LR cizelgesi | Sabir | Eniyileyici | lr (etkin) | Agirlik azaltma | Momentum | Batch | eps | alpha | PGD adim | Gradyan kirpma | --save-every | Komut ve tavan kaynagi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V-scr | 100 | cosine (T_max 100) | 20 | AdamW | 0.001 | 0.05 | - | 64 | 8/255 | 2/255 | 10 | 10 | 0 | `scripts/run_c1_pipeline.sh:62-66`; --stop-epoch yok (varsayilan 0, cli/train.py:179); tavan = -e |
| V-IN | 80 | cosine (T_max 100) | 20 | AdamW | 0.001 | 0.05 | - | 64 | 8/255 | 2/255 | 10 | 10 | 10 | `logs/konsey_zincir.log:40`; --stop-epoch komut (logs/konsey_zincir.log:40) |
| R224-scr | 80 | cosine (T_max 100) | 20 | AdamW | 0.001 | 0.05 | - | 64 | 8/255 | 2/255 | 10 | 10 | 10 | `logs/konsey_zincir.log:57`; --stop-epoch komut (logs/konsey_zincir.log:57) |
| R224-IN | 80 | cosine (T_max 100) | 20 | AdamW | 0.001 | 0.05 | - | 64 | 8/255 | 2/255 | 10 | 10 | 10 | `logs/konsey_zincir.log:54`; --stop-epoch komut (logs/konsey_zincir.log:54) |
| C1-R32 | 100 | cosine (T_max 100) | 20 | SGD | 0.001 | 0.0005 | 0.9 | 128 | 8/255 | 2/255 | 10 | 10 | 0 | `scripts/run_c1_pipeline.sh:50-54`; --stop-epoch yok (varsayilan 0, cli/train.py:179); tavan = -e |

Ortak (`ortak`): AT kaybi karisik kayip: (1 - mix_ratio) * CE(temiz) + mix_ratio * CE(PGD), mix_ratio 0.5, PGD rastgele baslangic evet (src/defenses/adversarial_training.py:122; src/defenses/adversarial_training.py:31; src/defenses/adversarial_training.py:30; savunma kurulumu bu iki degeri gecmez (src/training/adversarial_trainer.py:131)); erken durma olcutu dogrulama PGD dogrulugu en iyi + min_delta (puan), min_delta 0.1 (src/training/adversarial_trainer.py:52; src/training/adversarial_trainer.py:512); veri cifar10, dogrulama bolmesi `data/val_split_indices.json` n 2000 (data/val_split_indices.json len(val_indices); val_size alani 2000); artirma RandomCrop(32, padding=4) + RandomHorizontalFlip + ToTensor (src/data/datasets.py:296; src/data/datasets.py:298; src/data/datasets.py:269); pilot secilen tavan 80 (`results/q1/konsey_pilot_zaman.json secilen_tavan`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:36`); secim kurali `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:23`.

V-IN kosulari: V_IN_s2101 temiz `logs/konsey_zincir.log:36`, AT `logs/konsey_zincir.log:40` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet); V_IN_s2102 temiz `logs/konsey_zincir.log:60`, AT `logs/konsey_zincir.log:63` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet).

R224-scr kosulari: R224_scr_s1201 temiz `logs/konsey_zincir.log:51`, AT `logs/konsey_zincir.log:57` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet); R224_scr_s1202 temiz `logs/konsey_zincir.log:72`, AT `logs/konsey_zincir.log:74` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet).

R224-IN kosulari: R224_IN_s1301 temiz `logs/konsey_zincir.log:47`, AT `logs/konsey_zincir.log:54` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet); R224_IN_s1302 temiz `logs/konsey_zincir.log:66`, AT `logs/konsey_zincir.log:69` (kuyruk sablonu `scripts/konsey_b3_kuyruk.sh:99`, sablonla ayni bayraklar evet).

Denetimler (`denetimler`): B3 AT tavani pilotla ayni evet; B3 komutlari kuyruk sablonuyla ayni evet; B3 hucre ici kosular tohum disinda ozdes evet; egitim gunlugu basliklari (Epochs, LR, eniyileyici) cozumlenen degerlerle 42/42 uyusuyor; AT eps, alpha ve adim hucreler arasi ayni evet.

Gerceklesen epoklar bu bolumde tekrarlanmaz (`foy_referanslari`): B3, M9.1 tablosunun 'AT epok (kosulan)' sutunu, V_IN_s2101 satir 1452 (satir ayni); R224_IN_s1301 satir 1453 (satir ayni); R224_scr_s1201 satir 1454 (satir ayni); V_IN_s2102 satir 1455 (satir ayni); R224_IN_s1302 satir 1456 (satir ayni); R224_scr_s1202 satir 1457 (satir ayni); C1 V-scr ve C1-R32, M8.14 basligi satir 1377 (satir ayni); B3 toplam egitim suresi M9.1 satir 1470 (satir ayni).

AT tavani cumlesi (`ortak.at_tavani_on_kayit_cumlesi`, `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:36`, tam alinti): "AT tavanı 80 epoktur ve dört yeni hücrede eşittir." On kayit hucre tablosunda 'mevcut' isaretli hucreler: V-scr; yeni hucreler: V-IN, R224-scr, R224-IN.

V-scr AT tavani (`denetimler.V_scr_AT_tavani_ve_gerceklesen_durma`): 100 (--stop-epoch yok (varsayilan 0, cli/train.py:179); tavan = -e; kosinus T_max 100); B3 tavani 80 (results/q1/konsey_pilot_zaman.json secilen_tavan); gerceklesen durma epoklari B3 tavaninin altinda evet (M8.14 'Durma epogu' sutunu, satir 1383-1385, satirlar ayni; epoklar burada tekrarlanmaz).

(d) C1 hucrelerinin kosu anindaki kod surumu (`hucreler.<V-scr|C1-R32>.kosu_ani_kodu`): (b) ve (c) tablolarindaki C1 'varsayilan' kaynaklari bugunku kod satirlaridir; kosular 77ae259 (2026-07-29T01:12:33+00:00) ile yapilmistir. Dayanak (`dayanak`): ilk C1 egitim adimi 2026-07-29T01:11:17+00:00 (`TIMING.md:5`, commit'e gore -76 s), son adim 2026-07-30T18:00:21+00:00 (`TIMING.md:21`); izlenen dosyalari degistiren bir sonraki commit f633190 (2026-08-13T19:46:13+00:00), son adim ondan once evet; egitim dosyalari commit'le degismedi evet; --val-indices secenegi commit oncesinde var hayir, commit'te var evet; TIMING.md saatleri ile gunluk mtime farki en buyuk 0.51 s. Kosu aninda olmayan CLI secenekleri: --optimizer, --lr-schedule, --init-weights, --grad-clip, --stop-epoch, --save-every, --vit-lr-cap, --lr-warmup (davranis o surumde sabit kodla belirleniyordu). Asagidaki tablo her degeri 77ae259 metninden yeniden okur:

| Hucre | Asama | Deger | 77ae259 (kosu ani) | Kosu ani kaynagi | Bugunku tarif | Ayni |
|---|---|---|---|---|---|---|
| V-scr | temiz | model_sinifi | CIFAR10ViTTiny | `git:77ae259:src/models/vit.py:284` | CIFAR10ViTTiny | evet |
| V-scr | temiz | eniyileyici | AdamW | `git:77ae259:src/training/trainer.py:83; git:77ae259:src/training/trainer.py:84` | AdamW | evet |
| V-scr | temiz | lr_etkin | 0.001 | `git:77ae259:src/training/trainer.py:88` | 0.001 | evet |
| V-scr | temiz | agirlik_azaltma | 0.05 | `git:77ae259:src/training/trainer.py:92` | 0.05 | evet |
| V-scr | temiz | lr_cizelgesi | cosine, T_max = -e (200) | `git:77ae259:src/training/trainer.py:108` | cosine, T_max 200 | evet |
| V-scr | temiz | baslatma | rastgele (--init-weights secenegi yok) | `git:77ae259:cli/train.py (secenek listesi)` | none | evet |
| V-scr | AT | model_sinifi | CIFAR10ViTTiny | `git:77ae259:src/models/vit.py:284` | CIFAR10ViTTiny | evet |
| V-scr | AT | eniyileyici | AdamW | `git:77ae259:src/training/adversarial_trainer.py:137; git:77ae259:src/training/adversarial_trainer.py:138` | AdamW | evet |
| V-scr | AT | lr_etkin | 0.001 | `git:77ae259:src/training/adversarial_trainer.py:141` | 0.001 | evet |
| V-scr | AT | agirlik_azaltma | 0.05 | `git:77ae259:src/training/adversarial_trainer.py:145` | 0.05 | evet |
| V-scr | AT | lr_cizelgesi | cosine, T_max = -e (100) | `git:77ae259:src/training/adversarial_trainer.py:160` | cosine, T_max 100 | evet |
| V-scr | AT | epok_tavani | -e (100); --stop-epoch secenegi yok | `git:77ae259:cli/train.py (secenek listesi)` | 100 | evet |
| V-scr | AT | eps | 0.0313725 | `git:77ae259:cli/train.py:92` | 0.0313725 | evet |
| V-scr | AT | alpha | 0.00784314 | `git:77ae259:cli/train.py:93` | 0.00784314 | evet |
| V-scr | AT | pgd_adim | 10 | `git:77ae259:cli/train.py:94` | 10 | evet |
| V-scr | AT | gradyan_kirpma | 10 | `git:77ae259:src/training/adversarial_trainer.py:215 (sabit kod)` | 10 | evet |
| V-scr | AT | mix_ratio | 0.5 | `git:77ae259:src/defenses/adversarial_training.py:31` | 0.5 | evet |
| V-scr | AT | pgd_rastgele_baslangic | True | `git:77ae259:src/defenses/adversarial_training.py:30` | True | evet |
| V-scr | AT | erken_durma_min_delta | 0.1 | `git:77ae259:src/training/adversarial_trainer.py:52` | 0.1 | evet |
| C1-R32 | temiz | model_sinifi | CIFAR10ResNet18 | `git:77ae259:src/models/resnet.py:13` | CIFAR10ResNet18 | evet |
| C1-R32 | temiz | eniyileyici | SGD | `git:77ae259:src/training/trainer.py:83; git:77ae259:src/training/trainer.py:84` | SGD | evet |
| C1-R32 | temiz | lr_etkin | 0.1 | `komut (scripts/run_c1_pipeline.sh:46-48); git:77ae259:src/training/trainer.py:98` | 0.1 | evet |
| C1-R32 | temiz | momentum | 0.9 | `git:77ae259:src/training/trainer.py:33` | 0.9 | evet |
| C1-R32 | temiz | agirlik_azaltma | 0.0005 | `git:77ae259:src/training/trainer.py:34` | 0.0005 | evet |
| C1-R32 | temiz | lr_cizelgesi | cosine, T_max = -e (200) | `git:77ae259:src/training/trainer.py:108` | cosine, T_max 200 | evet |
| C1-R32 | temiz | baslatma | rastgele (--init-weights secenegi yok) | `git:77ae259:cli/train.py (secenek listesi)` | none | evet |
| C1-R32 | AT | model_sinifi | CIFAR10ResNet18 | `git:77ae259:src/models/resnet.py:13` | CIFAR10ResNet18 | evet |
| C1-R32 | AT | eniyileyici | SGD | `git:77ae259:src/training/adversarial_trainer.py:137; git:77ae259:src/training/adversarial_trainer.py:138` | SGD | evet |
| C1-R32 | AT | lr_etkin | 0.001 | `komut (scripts/run_c1_pipeline.sh:50-54); git:77ae259:src/training/adversarial_trainer.py:150` | 0.001 | evet |
| C1-R32 | AT | momentum | 0.9 | `git:77ae259:src/training/adversarial_trainer.py:41` | 0.9 | evet |
| C1-R32 | AT | agirlik_azaltma | 0.0005 | `git:77ae259:src/training/adversarial_trainer.py:42` | 0.0005 | evet |
| C1-R32 | AT | lr_cizelgesi | cosine, T_max = -e (100) | `git:77ae259:src/training/adversarial_trainer.py:160` | cosine, T_max 100 | evet |
| C1-R32 | AT | epok_tavani | -e (100); --stop-epoch secenegi yok | `git:77ae259:cli/train.py (secenek listesi)` | 100 | evet |
| C1-R32 | AT | eps | 0.0313725 | `git:77ae259:cli/train.py:92` | 0.0313725 | evet |
| C1-R32 | AT | alpha | 0.00784314 | `git:77ae259:cli/train.py:93` | 0.00784314 | evet |
| C1-R32 | AT | pgd_adim | 10 | `git:77ae259:cli/train.py:94` | 10 | evet |
| C1-R32 | AT | gradyan_kirpma | 10 | `git:77ae259:src/training/adversarial_trainer.py:215 (sabit kod)` | 10 | evet |
| C1-R32 | AT | mix_ratio | 0.5 | `git:77ae259:src/defenses/adversarial_training.py:31` | 0.5 | evet |
| C1-R32 | AT | pgd_rastgele_baslangic | True | `git:77ae259:src/defenses/adversarial_training.py:30` | True | evet |
| C1-R32 | AT | erken_durma_min_delta | 0.1 | `git:77ae259:src/training/adversarial_trainer.py:52` | 0.1 | evet |

Eniyileyici gozlemi (`kosu_ani_kodu.eniyileyici_gozlemi`): V-scr temiz: gunlukte gozlendi; V-scr AT: gunlukte gozlendi; C1-R32 temiz: gunlukte eniyileyici satiri yok; eniyileyici koddan cikarilmistir (git:77ae259:src/training/trainer.py:98-105 (SGD dali; yazdirma yok: True); momentum git:77ae259:src/training/trainer.py:33; agirlik azaltma git:77ae259:src/training/trainer.py:34); C1-R32 AT: gunlukte eniyileyici satiri yok; eniyileyici koddan cikarilmistir (git:77ae259:src/training/adversarial_trainer.py:150-157 (SGD dali; yazdirma yok: True); momentum git:77ae259:src/training/adversarial_trainer.py:41; agirlik azaltma git:77ae259:src/training/adversarial_trainer.py:42). C1 kosu ani kodu bugunku tarifle ayni (`denetimler.C1_kosu_ani_kodu_bugunku_tarifle_ayni`): evet.

_Kaynak: `results/q1/konsey_b3_tarif.json` etiket, meta.{betik, betik_sha256, ortak_modul, ortak_modul_sha256, uretildi_utc, python, kaynak_sayisi, kaynaklar_sha256, foy_ozeti, yeniden_uretim_notu, git_kaynaklari}; hucreler.<h>.{blok, girdi_hatti, tohumlar, on_kayit_satiri, hucre_tablosu_tanimi, takma_adlar, kosular.<k>.{temiz, AT}, kosu_ani_kodu}; ortak (at_tavani_on_kayit_cumlesi dahil); denetimler (C1_kosu_ani_kodu_bugunku_tarifle_ayni, V_scr_AT_tavani_ve_gerceklesen_durma dahil); foy_referanslari_


### M13.2 Kayit haritasi: on kayitli sinamalar, esikler, aileler ve gerceklesen kararlar (Y4, fig:registry_map)

Etiket (`etiket`): Y4 fig:registry_map kaynagi: on kayitli sinamalarin kayit haritasi.

`results/q1/konsey_kayit_kurallari.json` meta: betik arsiv/b2_yardimci/_m13_kayit.py betik_sha256 031585b2c56f3f75c28cd6c8be67f6d11de0d3ce5a6237fcf39e7543b0183c1f (dosyadan hesaplanan AYNI); ortak modul arsiv/b2_yardimci/_m13_ortak.py c17618e252c0d08b8b4a5e01960d676f4f9e71b9d80e39cfd9906b5cc1069d98 (AYNI); uretildi_utc 2026-10-31T18:18:19.309861+00:00; python 3.10.12; kaynak dosya sayisi (kaynaklar_sha256) 14; kaynaklardan simdi farkli olan (foy haric; foy satirlari satir sha256'siyla ayrica denetlenir): yok. Foy ozeti (`meta.foy_ozeti.m13_haric_sha256`; foyden '## M13:' bolumu cikarilmis metnin sha256'si, denetimi arsiv/b2_yardimci/_m13_kontrol.py): 00cc422f01c0d9641d46bebd544eea0cb2a915256906bacf77d7f898f937979f.

(a) Sabitler (`sabitler`; deger kaynak satirindan duzenli ifadeyle okunmus, on kayit satirinda ondalik virgullu yazimi aranmistir):

| Sabit | Ad | Deger | Betik satiri | On kayit satiri | On kayitta bulunan yazim |
|---|---|---|---|---|---|
| DELTA | delta (birincil esdegerlik siniri, log birimi) | 0.1 | `experiments/q1_konsey_ayrisim.py:58` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:50` | 0,10 |
| DELTA_DUY | delta duyarliligi | 0.06 | `experiments/q1_konsey_ayrisim.py:59` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:50` | 0,06 |
| ALFA | Holm alfa | 0.05 | `experiments/q1_konsey_ayrisim.py:60` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:58` | 0,05 |
| B5_ESIK | B5 korunma orani esigi | 0.5 | `experiments/q1_konsey_ayrisim.py:61` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:90` | 0,5 |
| BOOT_TOHUM | bootstrap tohumu | 20261029 | `experiments/q1_konsey_ayrisim.py:62` | - | - |
| BOOTSTRAP_B | bootstrap kopya sayisi (varsayilan) | 2000 | `experiments/q1_konsey_ayrisim.py:1149` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:64` | 2000 |
| S5_BANT | S5 bandi (puan) | 1.5 | `experiments/q1_konsey_ayrisim.py:63` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82` | 1,5 |
| S5_EGIM | S5 ongoru dogrusu egimi | 0.796 | `experiments/q1_konsey_ayrisim.py:63` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82` | +0,796 |
| S5_KESISIM | S5 ongoru dogrusu kesisimi (puan) | -0.01 | `experiments/q1_konsey_ayrisim.py:63` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82` | −0,01 |
| B6_ESIK_PUAN | B6 maskeleme esigi (PGD-10 - AA, puan) | 10 | `scripts/konsey_b6_maskeleme.py:28` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:94` | 10 |
| B8_BEKLENTI_A_SIGMA_IN | B8 IN satiri beklenti esigi | -0.1 | `experiments/q1_ek_ayrisim.py:47` | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:122` | −0,10 |
| B10_PERM | B10 Mantel permutasyon sayisi | 9999 | `experiments/q1_ek_ayrisim.py:48` | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:159` | 9999 |
| B10_PERM_TOHUM | B10 permutasyon tohumu | 20261030 | `experiments/q1_ek_gradyan_kosinus.py:46` | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:159` | 20261030 |

TOST siniri tanimi `experiments/q1_konsey_ayrisim.py:318`; karar ilkesi `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:54` (ek on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:17`); hesaplanamayan sinamanin Holm'da p = 1 sayilmasi `experiments/q1_konsey_ayrisim.py:311`.

(b) Aileler (`aileler`; aile buyuklugu sonuc JSON'undaki p_holm uzunlugundan):

| Aile | Blok | Veri | Sinamalar | Holm | Aile buyuklugu (JSON) | On kayit satiri | Not |
|---|---|---|---|---|---|---|---|
| F_B2 | B2 | CIFAR-10 | K-a, K-b, K-c | evet | 3 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:58` | - |
| F_B4 | B4 | CIFAR-10 | H1, H2, H3 | evet | 3 | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:66` | - |
| F_B9 | B9 | CIFAR-100 | K-a, K-b, K-c | evet | 3 | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:51` | - |
| F_B10 | B10 | CIFAR-10, CIFAR-100, ImageNetV2 | H10-cifar10, H10k-cifar10, H10-cifar100, H10k-cifar100, H10-imagenetv2, H10k-imagenetv2 | evet | 6 | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:159` | - |
| B5 | B5 | - | - | hayir | - | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:90` | tek sinamali ayri aile |
| B8 | B8 | - | - | hayir | - | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:120` | karar ailesi yok, betimsel |
| S1-S7 | B4 ikincil | - | - | hayir | - | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:76` | kesifsel, coklu duzeltme yok |

(c) Sinamalar (`sinamalar`; 'Karar' sutunu foyun gosterilen tablo hucresidir, 'JSON ile ayni' sonuc JSON'unun karar anahtariyla, S satirlarinda b4.ikincil mantiksal anahtarlariyla karsilastirmadir, '-' karsilastirilmayan betimsel satirdir; 'Ongorulen buyukluk ve esikler' yalniz JSON'daki esik alanlarindan basilir, alan yoksa '-'; S satirlarinin ongorusu `ongoru` ve `ongoru_on_kayit` alanlarindandir; sonuc sayilari icin foy satirina bakilir):

| Sinama | Blok | Aile | Nicelik | Ongoru | Ongoru (on kayit alintisi) | Ongorulen buyukluk ve esikler | Karar kurali (kaynak satirlari) | On kayit satiri | Karar (foy) | Foy satiri | JSON ile ayni |
|---|---|---|---|---|---|---|---|---|---|---|---|
| K-a | B2 | F_B2 | q_s = [sigma(R_s) - sigma(V_s)] / D_s, tohum basina; ort q | her tohumda q_s >= esik | - | ongorulen_buyukluk 0.75 (`experiments/q1_konsey_ayrisim.py:500`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:60`); H0 esigi 0.5 (`experiments/q1_konsey_ayrisim.py:497`); curutme esigi 0.5 (`experiments/q1_konsey_ayrisim.py:452`) | payda_kurali: bir tohumda D_s <= DELTA ise kararsiz, Holm'da p = 1 (`experiments/q1_konsey_ayrisim.py:542`); curutme: ort q %90 araligi ust siniri < esik (`experiments/q1_konsey_ayrisim.py:452`); destek: Holm sonrasi p < ALFA (`experiments/q1_konsey_ayrisim.py:454`); sira: payda kurali > curutme > destek > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:60` | destek | M9.5 satir 1587 (satir ayni) | evet |
| K-b | B2 | F_B2 | rho(V-scr), tohum ortalamasi | esdeger, \|rho\| < DELTA | - | esdegerlik siniri (-0.1; 0.1), TOST +-DELTA: iki tek yonlu sinama (H0: mu <= -DELTA ve H0: mu >= +DELTA); buyuk p Holm'a girer (`experiments/q1_konsey_ayrisim.py:58`; TOST tanimi `experiments/q1_konsey_ayrisim.py:318`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:62` yazim 0,10) | curutme: %95 aralik sifiri disliyor ve \|ort\| > DELTA (iki yonde) (`experiments/q1_konsey_ayrisim.py:461`); destek: Holm sonrasi TOST p < ALFA (`experiments/q1_konsey_ayrisim.py:462`); sira: destek > curutme > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:62` | destek (Holm sonrasi TOST p < 0,05) | M9.5 satir 1588 (satir ayni) | evet |
| K-c | B2 | F_B2 | Delta_w = ort log tau(V_s, V_s') - ort_s sigma(V_s) | Delta_w >= esik | - | ongorulen_buyukluk 0.3 (`experiments/q1_konsey_ayrisim.py:540`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:64`) | curutme: %90 bootstrap araligi ust siniri < DELTA (once denetlenir) (`experiments/q1_konsey_ayrisim.py:474`); destek: curutme tutmuyorsa Holm sonrasi p < ALFA (`experiments/q1_konsey_ayrisim.py:476`); sira: curutme > destek > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:64` | destek | M9.5 satir 1589 (satir ayni) | evet |
| K-a | B9 | F_B9 | q_s = [sigma(R_s) - sigma(V_s)] / D_s, tohum basina; ort q | her tohumda q_s >= esik | - | ongorulen_buyukluk 0.75 (`experiments/q1_konsey_ayrisim.py:500`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:60`); H0 esigi 0.5 (`experiments/q1_konsey_ayrisim.py:497`); curutme esigi 0.5 (`experiments/q1_konsey_ayrisim.py:452`) | payda_kurali: bir tohumda D_s <= DELTA ise kararsiz, Holm'da p = 1 (`experiments/q1_konsey_ayrisim.py:542`); curutme: ort q %90 araligi ust siniri < esik (`experiments/q1_konsey_ayrisim.py:452`); destek: Holm sonrasi p < ALFA (`experiments/q1_konsey_ayrisim.py:454`); sira: payda kurali > curutme > destek > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:53; raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:60` | destek | M10.2 satir 1838 (satir ayni) | evet |
| K-b | B9 | F_B9 | rho(V-scr), tohum ortalamasi | esdeger, \|rho\| < DELTA | - | esdegerlik siniri (-0.1; 0.1), TOST +-DELTA: iki tek yonlu sinama (H0: mu <= -DELTA ve H0: mu >= +DELTA); buyuk p Holm'a girer (`experiments/q1_konsey_ayrisim.py:58`; TOST tanimi `experiments/q1_konsey_ayrisim.py:318`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:62` yazim 0,10) | curutme: %95 aralik sifiri disliyor ve \|ort\| > DELTA (iki yonde) (`experiments/q1_konsey_ayrisim.py:461`); destek: Holm sonrasi TOST p < ALFA (`experiments/q1_konsey_ayrisim.py:462`); sira: destek > curutme > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:53; raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:62` | curutuldu (pozitif yon) | M10.2 satir 1839 (satir ayni) | evet |
| K-c | B9 | F_B9 | Delta_w = ort log tau(V_s, V_s') - ort_s sigma(V_s) | Delta_w >= esik | - | ongorulen_buyukluk 0.3 (`experiments/q1_konsey_ayrisim.py:540`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:64`) | curutme: %90 bootstrap araligi ust siniri < DELTA (once denetlenir) (`experiments/q1_konsey_ayrisim.py:474`); destek: curutme tutmuyorsa Holm sonrasi p < ALFA (`experiments/q1_konsey_ayrisim.py:476`); sira: curutme > destek > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:53; raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:64` | destek | M10.2 satir 1840 (satir ayni) | evet |
| H1 | B4 | F_B4 | A^sigma_scr = sigma(V-scr) - sigma(R224-scr) | A^sigma_scr <= esik | - | ongorulen_buyukluk -0.2 (`experiments/q1_konsey_ayrisim.py:658`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:70`) | (i) ham %90 aralik (-DELTA; DELTA) icinde -> curutuldu (esdeger) (`experiments/q1_konsey_ayrisim.py:650`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_konsey_ayrisim.py:652`); (iii) kestirim > 0 ve %95 alt sinir > 0 -> curutuldu (ters yon) (`experiments/q1_konsey_ayrisim.py:654`); (iv) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:70` | destek | M9.3 satir 1526 (satir ayni) | evet |
| H2 | B4 | F_B4 | I^sigma = [sigma(V-IN) - sigma(V-scr)] - [sigma(R224-IN) - sigma(R224-scr)] | I^sigma >= esik | - | ongorulen_buyukluk 0.1 (`experiments/q1_konsey_ayrisim.py:672`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:72`) | p_iki `experiments/q1_konsey_ayrisim.py:345`; holm_girdisi `experiments/q1_konsey_ayrisim.py:618`; (i) ham %90 aralik (-DELTA; DELTA) icinde -> curutuldu (esdeger) (`experiments/q1_konsey_ayrisim.py:662`); (ii) Holm sonrasi p < ALFA, kestirim > 0 ve logit kestirim > 0 -> destek (`experiments/q1_konsey_ayrisim.py:664`); (iii) kestirim < 0 ve ham iki yonlu p < ALFA -> curutuldu (ters yon) (`experiments/q1_konsey_ayrisim.py:666`); (iv) kalan -> kararsiz (logit isaret donusu dahil) (`experiments/q1_konsey_ayrisim.py:669`) | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:72` | destek | M9.3 satir 1527 (satir ayni) | evet |
| H3 | B4 | F_B4 | A^rho = 1/2 {[rho(V-scr) - rho(R224-scr)] + [rho(V-IN) - rho(R224-IN)]} | esdeger, \|A^rho\| < DELTA | - | esdegerlik siniri (-0.1; 0.1), TOST +-DELTA: iki tek yonlu sinama (H0: mu <= -DELTA ve H0: mu >= +DELTA); buyuk p Holm'a girer (`experiments/q1_konsey_ayrisim.py:58`; TOST tanimi `experiments/q1_konsey_ayrisim.py:318`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:74` yazim 0,10) | curutme: %95 aralik sifiri disliyor ve \|kestirim\| > DELTA (`experiments/q1_konsey_ayrisim.py:680`); destek: Holm sonrasi TOST p < ALFA (`experiments/q1_konsey_ayrisim.py:678`); sira: destek > curutme > kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:74` | destek (esdeger, Holm sonrasi TOST p < 0,05) | M9.3 satir 1528 (satir ayni) | evet |
| S1-sigma | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | sigma koprusu ve rho koprusu ikisi de esdeger: ham %90 araligi (-DELTA; DELTA) icinde | "öngörü ikisi de ±0,10 içinde" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78`) | esdegerlik siniri (-0.1; 0.1), ham %90 t araligi (-DELTA; DELTA) icinde (iki ucta kesin esitsizlik); TOST degil, kesifsel, Holm yok (`experiments/q1_konsey_ayrisim.py:58`; icinde tanimi `experiments/q1_konsey_ayrisim.py:359`, uygulama `experiments/q1_konsey_ayrisim.py:786`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78` yazim 0,10) | betik `experiments/q1_konsey_ayrisim.py:786` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78` | ikisi de esdeger: evet | M9.4 satir 1561 (satir ayni) | evet |
| S1-rho | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | sigma koprusu ve rho koprusu ikisi de esdeger: ham %90 araligi (-DELTA; DELTA) icinde | "öngörü ikisi de ±0,10 içinde" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78`) | esdegerlik siniri (-0.1; 0.1), ham %90 t araligi (-DELTA; DELTA) icinde (iki ucta kesin esitsizlik); TOST degil, kesifsel, Holm yok (`experiments/q1_konsey_ayrisim.py:58`; icinde tanimi `experiments/q1_konsey_ayrisim.py:359`, uygulama `experiments/q1_konsey_ayrisim.py:786`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78` yazim 0,10) | betik `experiments/q1_konsey_ayrisim.py:786` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:78` | ikisi de esdeger: evet | M9.4 satir 1562 (satir ayni) | evet |
| S2 | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | rho(V-IN) - rho(V-scr) < 0 (negatif) | "öngörü negatif" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:79`) | - | betik `experiments/q1_konsey_ayrisim.py:791` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:79` | negatif: evet | M9.4 satir 1563 (satir ayni) | evet |
| S3-ViT | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | omega(V-IN) < omega(V-scr), yani ViT baslatma etkisi < 0 | "öngörü ω(V-IN) < ω(V-scr)" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80`) | - | betik `experiments/q1_konsey_ayrisim.py:795` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80` | omega(V-IN) < omega(V-scr): evet | M9.4 satir 1564 (satir ayni) | evet |
| S3-ResNet | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | yok (betimsel; on kayitta S3 ongorusu yalniz ViT baslatma etkisi icindir) | "öngörü ω(V-IN) < ω(V-scr)" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80`) | - | betik `experiments/q1_konsey_ayrisim.py:795` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80` | betimsel | M9.4 satir 1565 (satir ayni) | - |
| S3-etkilesim | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | yok (betimsel; on kayitta S3 ongorusu yalniz ViT baslatma etkisi icindir) | "öngörü ω(V-IN) < ω(V-scr)" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80`) | - | betik `experiments/q1_konsey_ayrisim.py:795` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:80` | betimsel | M9.4 satir 1566 (satir ayni) | - |
| S5 | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | cift sapmalarinin ortalamasi +-S5_BANT puan icinde | "Öngörü: ortalama sapma ±1,5 puan içinde" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82`) | bant 1.5 (`experiments/q1_konsey_ayrisim.py:63`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82`); ongoru dogrusu egim 0.796, kesisim -0.01 (`experiments/q1_konsey_ayrisim.py:63`; uygulama `experiments/q1_konsey_ayrisim.py:813`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82`) | curutme: ortalama sapmanin %90 araligi [-S5_BANT; S5_BANT] bandinin tumuyle disinda -> mekanizma cumlesi daraltilir, manset etkilenmez (`experiments/q1_konsey_ayrisim.py:821`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82`); betik `experiments/q1_konsey_ayrisim.py:820` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:82` | ort sapma bant icinde: evet; curutme (%90 bant disinda): hayir | M9.4 satir 1567 (satir ayni) | evet |
| S6 | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | A^sigma_scr ve I^sigma'nin isareti ikincil panelde birincil panelle ayni | "A^σ_scr ve I^σ'nın işareti birincil panelle aynı" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:83`) | - | betik `experiments/q1_konsey_ayrisim.py:828` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:83` | isaret ayni A: evet; I: evet | M9.4 satir 1568 (satir ayni) | evet |
| S7 | B4 ikincil | yok (kesifsel, coklu duzeltme yok) | - | yok (betimsel; on kayit satirinda ongoru ifadesi yok) | "S7, r matrisinde Hodge ayrışımıyla model düzeyi ve dolaşım payı." (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:84`) | - | betik `experiments/q1_konsey_ayrisim.py:835` | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:84` | betimsel | M9.4 satir 1569 (satir ayni) | - |
| S4 | B4 ikincil | yok (betimsel) | - | yok (betimsel) | "betimsel" (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:81`) | - | - | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:81` | betimsel tablo; karar yok | M9.4 satir 1571 (satir ayni) | - |
| B5 | B5 | tek sinamali ayri aile (Holm yok) | korunma orani G_best / G_PGD (C1-R32 ve V-scr; capraz uydurmali secim) | oran >= B5_ESIK | - | esik 0.5 (`experiments/q1_konsey_ayrisim.py:61`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:90`) | (i) G_PGD <= DELTA -> kararsiz (payda kucuk) (`experiments/q1_konsey_ayrisim.py:944`); (ii) %90 bootstrap ust siniri < B5_ESIK -> curutuldu (manset PGD ailesiyle sinirlanir) (`experiments/q1_konsey_ayrisim.py:946`); (iii) %90 bootstrap alt siniri >= B5_ESIK -> destek (`experiments/q1_konsey_ayrisim.py:948`); (iv) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:90` | destek | M9.6 satir 1628 (satir ayni) | evet |
| B6 | B6 | karar kurali (sinama degil; B4 bolgesini duzenler) | PGD-10 dogrulugu - AutoAttack dogrulugu (ilk 1000 test goruntusu, puan) | - | - | esik 10 (`scripts/konsey_b6_maskeleme.py:28`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:94`) | fark > B6_ESIK_PUAN olan model isaretlenir; isaretli varsa H1-H3 isaretliler cikarilarak yeniden hesaplanir, karar degisirse ilgili manset kararsiz sayilir (`scripts/konsey_b6_maskeleme.py:69`) | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:94` | isaretli: yok (Isaretli sutunu: V_IN_s2101 hayir; V_IN_s2102 hayir; R224_IN_s1301 hayir; R224_IN_s1302 hayir; R224_scr_s1201 hayir; R224_scr_s1202 hayir) | M9.7 satir 1666-1671 (satirlar ayni); M9.3 satir 1536 (satir ayni) | evet |
| B8-A_sigma_IN | B8 | yok (betimsel, kesifsel; Holm yok) | A^sigma = sigma(donusturucu) - sigma(CNN), P8, bolunmus yari, log; goruntu bootstrap'i | - | - | beklenti_esigi -0.1 (`experiments/q1_ek_ayrisim.py:47`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:122`) | (i) %90 aralik (-DELTA; DELTA) icinde -> ihmal edilebilir (`experiments/q1_ek_ayrisim.py:166`); (ii) kestirim <= esik, ciftlerin hepsi negatif ve %90 ust sinir < 0 -> beklentiyle uyumlu (`experiments/q1_ek_ayrisim.py:168`); (iii) kestirim > 0 ve %95 alt sinir > 0 -> ters yon (`experiments/q1_ek_ayrisim.py:170`); (iv) kalan -> belirsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:122` | beklentiyle uyumlu | M10.4 satir 1938 (satir ayni) | evet |
| B8-A_sigma_scr_Liu | B8 | yok (betimsel, kesifsel; Holm yok) | A^sigma = sigma(donusturucu) - sigma(CNN), P8, bolunmus yari, log; goruntu bootstrap'i | - | - | beklenti_esigi -0.2 (`experiments/q1_ek_ayrisim.py:269`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:126`) | (i) %90 aralik (-DELTA; DELTA) icinde -> ihmal edilebilir (`experiments/q1_ek_ayrisim.py:166`); (ii) kestirim <= esik, ciftlerin hepsi negatif ve %90 ust sinir < 0 -> beklentiyle uyumlu (`experiments/q1_ek_ayrisim.py:168`); (iii) kestirim > 0 ve %95 alt sinir > 0 -> ters yon (`experiments/q1_ek_ayrisim.py:170`); (iv) kalan -> belirsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:126` | belirsiz | M10.4 satir 1939 (satir ayni) | evet |
| B8-K-abc | B8 | yok (dondurulmus betik ciktisi yalniz betimsel) | - | - | - | - | - | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:137` | etiketler B8'de karar degildir | M10.4 satir 1945 (satir ayni) | - |
| H10-cifar10 | B10 | F_B10 | Spearman(c_ij, log tau_ij), Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.5 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1983 (satir ayni) | evet |
| H10k-cifar10 | B10 | F_B10 | Spearman(c artigi, log tau artigi), model ana etkileri cikarilmis, Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.3 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1984 (satir ayni) | evet |
| H10-cifar100 | B10 | F_B10 | Spearman(c_ij, log tau_ij), Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.5 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1985 (satir ayni) | evet |
| H10k-cifar100 | B10 | F_B10 | Spearman(c artigi, log tau artigi), model ana etkileri cikarilmis, Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.3 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1986 (satir ayni) | evet |
| H10-imagenetv2 | B10 | F_B10 | Spearman(c_ij, log tau_ij), Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.5 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1987 (satir ayni) | evet |
| H10k-imagenetv2 | B10 | F_B10 | Spearman(c artigi, log tau artigi), model ana etkileri cikarilmis, Mantel | Spearman > 0 | - | ongorulen_buyukluk 0.3 (`experiments/q1_ek_ayrisim.py:297`; on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163`); B10 curutme: kestirim esigi (kestirim <= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`); B10 curutme: ham Mantel p esigi (p >= esik) 0.2 (`experiments/q1_ek_ayrisim.py:308`) | (i) kestirim <= esik ve ham Mantel p >= p esigi -> curutuldu (`experiments/q1_ek_ayrisim.py:308`); (ii) Holm sonrasi p < ALFA -> destek (`experiments/q1_ek_ayrisim.py:310`); (iii) kalan -> kararsiz | `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:163` | destek | M10.5 satir 1988 (satir ayni) | evet |

Sonuc bolgesi (`sonuc_bolgesi`): denetim sirasi `experiments/q1_konsey_ayrisim.py:637`, on kayit tablosu `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:98`, sira cumlesi `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:107`; gerceklesen bolge O1 (O4 nitelemesi hayir; `results/q1/konsey_ayrisim_b4.json b4.F_B4.karar.sonuc_bolgesi, .O4_niteleme`), foy M9.3 satir 1536 (satir ayni; satirda bolge var evet).

Denetimler (`denetimler`): sinama sayisi 30; JSON karari ile foy hucresi (`json_ile_foy_ozet`): 25/25 karsilastirilan sinamada JSON karari foy hucresiyle ayni; 30 sinamanin 5 tanesi karsilastirilmadi (betimsel ya da karar degil); ayni olmayan: yok; karsilastirilmayan (`json_ile_foy_karsilastirilmayan`): S3-ResNet/B4 ikincil (yok: betimsel satir (foy hucresi 'betimsel'), JSON'da karar anahtari yok); S3-etkilesim/B4 ikincil (yok: betimsel satir (foy hucresi 'betimsel'), JSON'da karar anahtari yok); S7/B4 ikincil (yok: betimsel satir (foy hucresi 'betimsel'), JSON'da karar anahtari yok); S4/B4 ikincil (yok: betimsel tablo, karar yok); B8-K-abc/B8 (yok: dondurulmus betik ciktisi B8'de karar degildir); dondurulmus betik sha256 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 (on kayit metninde geciyor evet; dosyadan simdi hesaplanan AYNI); JSON uretilirken okunan foyun ozeti (M13 bolumu cikarilmis metnin sha256'si, `foy_sha256_tanimi`) 00cc422f01c0d9641d46bebd544eea0cb2a915256906bacf77d7f898f937979f.

On kayit metninde deger aramasi (`denetimler.on_kayit_deger_aramasi`; her esik ve sabitte `on_kayit_eslesmeleri` ve `on_kayit_aranan_yazimlar`): 53 deger; kural: Deger yalniz yuvarlamasiz yazimlarla aranir: en kisa ondalik gosterim ve sonuna sifir eklenmis bicimleri (en cok uc ondalik; ornegin 0.1 icin 0,1 / 0,10 / 0,100; 0.796 icin yalniz 0,796), ondalik ayirac virgul. Sozcuk siniri: eslesmenin oncesinde rakam, virgul ya da nokta; sonrasinda rakam ya da ayiracla baslayan rakam olamaz. Isaret: negatif deger icin hemen onde eksi (U+2212, '-' ya da '–') zorunlu; pozitif deger icin hemen onde eksi olamaz ('+' ve '±' serbest). En az bir eslesme yoksa uretim durur.

_Kaynak: `results/q1/konsey_kayit_kurallari.json` etiket, meta (foy_ozeti, yeniden_uretim_notu dahil); sabitler.<ad>.{ad, deger, kaynak, on_kayit, on_kayit_metninde_yazimi, on_kayit_eslesmeleri, on_kayit_aranan_yazimlar}; delta_tost_tanimi; karar_ilkesi; aileler.<aile>.{blok, veri, sinamalar, holm, aile_buyuklugu_json, on_kayit, not}; sinamalar[].{kimlik, blok, aile, nicelik, ongoru, ongoru_on_kayit, ongoru_turu, ongorulen_buyukluk, esdegerlik_siniri, ongoru_dogrusu, sinama (p_iki, holm_girdisi dahil), destek, curutme (kural, on_kayit dahil), payda_kurali, kurallar_sirasiyla, etiketler_sirasiyla, esik, bant, beklenti_esigi, on_kayit, gerceklesen (karar_json, json_ile_foy_ayni, json_ile_foy_karsilastirma dahil)}; sonuc_bolgesi; denetimler_


### M13.3 On kayit ve deney zinciri zaman cizelgesi (Y5, fig:prereg_chain)

Etiket (`etiket`): Y5 fig:prereg_chain kaynagi: on kayit ve deney zinciri zaman cizelgesi.

`results/q1/konsey_zaman_cizelgesi.json` meta: betik arsiv/b2_yardimci/_m13_zaman.py betik_sha256 951b998a8631c7bcc1cdd31e7b0e16e7a91e106ca68f777df5b6f645547351bb (dosyadan hesaplanan AYNI); ortak modul arsiv/b2_yardimci/_m13_ortak.py c17618e252c0d08b8b4a5e01960d676f4f9e71b9d80e39cfd9906b5cc1069d98 (AYNI); uretildi_utc 2026-10-31T18:18:19.357534+00:00; python 3.10.12; kaynak dosya sayisi (kaynaklar_sha256) 40; kaynaklardan simdi farkli olan (foy haric; foy satirlari satir sha256'siyla ayrica denetlenir): yok. Foy ozeti (`meta.foy_ozeti.m13_haric_sha256`; foyden '## M13:' bolumu cikarilmis metnin sha256'si, denetimi arsiv/b2_yardimci/_m13_kontrol.py): 00cc422f01c0d9641d46bebd544eea0cb2a915256906bacf77d7f898f937979f.

Saat dilimi (`saat_dilimi`): konsey zinciri gunlugu, durum TSV'si ve B3 defteri UTC'ye gore 0 saat fark; ek zincir gunlukleri 3 saat fark. Kanit: results/q1/konsey_zincir_durum.tsv B2_cozumleme.baslangic ile results/q1/konsey_ayrisim_b2.json meta.uretildi_utc (artik -1.769 s, JSON zamani adim icinde evet); results/q1/konsey_zincir_durum.tsv B4_cozumleme.baslangic ile results/q1/konsey_ayrisim_b4.json meta.uretildi_utc (artik -1.619 s, JSON zamani adim icinde evet); results/q1/konsey_zincir_durum.tsv B5_cozumleme.baslangic ile results/q1/konsey_ayrisim_b5.json meta.uretildi_utc (artik -2.161 s, JSON zamani adim icinde evet); results/q1/ek_loglar/ek_zincir_2.log:12 cozumleme baslangici ile results/q1/konsey_b9_c100/b9_dondurulmus_b2.json meta.uretildi_utc (artik -2.044 s, JSON zamani adim icinde evet); results/q1/ek_loglar/ek_zincir_2.log:12 cozumleme baslangici ile results/q1/konsey_b10_gradyan/b10_aile.json meta.uretildi_utc (artik -22.752 s, JSON zamani adim icinde evet).

(a) Olaylar, UTC'ye gore sirali (`dondurma`, `B2`, `konsey_zinciri`, `B3_asamalari`, `ek_zincir`, `masa_cozumlemeleri`; +03 karsiliklari JSON'da `*_yerel` alanlarinda; sure gunluk saatlerinin farkidir, s):

| Olay | Baslangic (UTC) | Bitis (UTC) | Sure (s) | Kaynak |
|---|---|---|---|---|
| On kayit dondurma (commit e32f2ce) | 2026-10-29 13:53:52 | - | - | `git log -1 --format=%H|%cI e32f2ce`; dosyayi ekleyen ilk commit evet |
| B2 matrisi (dosya zamanlari) | 2026-10-30 01:35:04.900090 | 2026-10-30 01:45:46.404337 | 641 | os.stat st_mtime: results/q1/konsey_b2_panel/cells_meta.json (baslangic vekili; experiments/c1_c3_transfer_matrix.py:313 hucre hesabindan once yazar) ve results/q1/konsey_b2_panel/transfer_matrix.json (bitis) (dosya degistirilme zamani (gunluk degil)) |
| konsey zinciri: zincir (BASLADI) | 2026-10-30 01:46:39 | - | - | `results/q1/konsey_zincir_durum.tsv:2` |
| konsey zinciri: B2_bekle (ATLANDI) | 2026-10-30 01:46:39 | 2026-10-30 01:46:39 | 0 | `results/q1/konsey_zincir_durum.tsv:3` |
| konsey zinciri: B2_cozumleme (OK) | 2026-10-30 01:46:39 | 2026-10-30 01:46:42 | 3 | `results/q1/konsey_zincir_durum.tsv:4` |
| konsey zinciri: B3_on_denetim (OK) | 2026-10-30 01:46:42 | 2026-10-30 01:46:50 | 8 | `results/q1/konsey_zincir_durum.tsv:5` |
| konsey zinciri: B3_kuru (OK) | 2026-10-30 01:46:50 | 2026-10-30 01:46:51 | 1 | `results/q1/konsey_zincir_durum.tsv:6` |
| konsey zinciri: B3_kuyruk (OK) | 2026-10-30 01:46:51 | 2026-10-30 19:34:57 | 64086 | `results/q1/konsey_zincir_durum.tsv:7` |
| B3 V_IN_s2101 temiz | 2026-10-30 01:46:52 | 2026-10-30 01:55:06 | 494 | `logs/konsey_zincir.log:36, logs/konsey_zincir.log:38`; defter `results/q1/konsey_b3_defter.tsv:2` |
| B3 V_IN_s2101 AT | 2026-10-30 01:55:07 | 2026-10-30 03:28:55 | 5628 | `logs/konsey_zincir.log:40, logs/konsey_zincir.log:45`; defter `results/q1/konsey_b3_defter.tsv:4` |
| B3 R224_IN_s1301 temiz | 2026-10-30 03:28:59 | 2026-10-30 03:38:49 | 590 | `logs/konsey_zincir.log:47, logs/konsey_zincir.log:48`; defter `results/q1/konsey_b3_defter.tsv:6` |
| B3 R224_scr_s1201 temiz | 2026-10-30 03:38:52 | 2026-10-30 04:51:10 | 4338 | `logs/konsey_zincir.log:51, logs/konsey_zincir.log:52`; defter `results/q1/konsey_b3_defter.tsv:8` |
| Ek on kayit dondurma (commit 7325419) | 2026-10-30 04:17:42 | - | - | `git log -1 --format=%H|%cI 7325419`; dosyayi ekleyen ilk commit evet |
| B3 R224_IN_s1301 AT | 2026-10-30 04:51:12 | 2026-10-30 06:48:42 | 7050 | `logs/konsey_zincir.log:54, logs/konsey_zincir.log:55`; defter `results/q1/konsey_b3_defter.tsv:10` |
| B3 R224_scr_s1201 AT | 2026-10-30 06:48:44 | 2026-10-30 10:27:30 | 13126 | `logs/konsey_zincir.log:57, logs/konsey_zincir.log:58`; defter `results/q1/konsey_b3_defter.tsv:12` |
| B3 V_IN_s2102 temiz | 2026-10-30 10:27:31 | 2026-10-30 10:34:33 | 422 | `logs/konsey_zincir.log:60, logs/konsey_zincir.log:61`; defter `results/q1/konsey_b3_defter.tsv:14` |
| B3 V_IN_s2102 AT | 2026-10-30 10:34:34 | 2026-10-30 14:03:24 | 12530 | `logs/konsey_zincir.log:63, logs/konsey_zincir.log:64`; defter `results/q1/konsey_b3_defter.tsv:16` |
| B3 R224_IN_s1302 temiz | 2026-10-30 14:03:25 | 2026-10-30 14:22:02 | 1117 | `logs/konsey_zincir.log:66, logs/konsey_zincir.log:67`; defter `results/q1/konsey_b3_defter.tsv:18` |
| B3 R224_IN_s1302 AT | 2026-10-30 14:22:03 | 2026-10-30 16:14:49 | 6766 | `logs/konsey_zincir.log:69, logs/konsey_zincir.log:70`; defter `results/q1/konsey_b3_defter.tsv:20` |
| B3 R224_scr_s1202 temiz | 2026-10-30 16:14:55 | 2026-10-30 17:10:10 | 3315 | `logs/konsey_zincir.log:72, logs/konsey_zincir.log:73`; defter `results/q1/konsey_b3_defter.tsv:22` |
| B3 R224_scr_s1202 AT | 2026-10-30 17:10:10 | 2026-10-30 19:34:55 | 8685 | `logs/konsey_zincir.log:74, logs/konsey_zincir.log:75`; defter `results/q1/konsey_b3_defter.tsv:23` |
| konsey zinciri: B4 (OK) | 2026-10-30 19:34:57 | 2026-10-30 19:42:12 | 435 | `results/q1/konsey_zincir_durum.tsv:8` |
| konsey zinciri: B6_AA (OK) | 2026-10-30 19:42:12 | 2026-10-30 20:29:18 | 2826 | `results/q1/konsey_zincir_durum.tsv:9` |
| konsey zinciri: B5_MI (OK) | 2026-10-30 20:29:18 | 2026-10-30 20:36:38 | 440 | `results/q1/konsey_zincir_durum.tsv:10` |
| konsey zinciri: B5_TGR (OK) | 2026-10-30 20:36:38 | 2026-10-30 20:40:39 | 241 | `results/q1/konsey_zincir_durum.tsv:11` |
| konsey zinciri: B6_maskeleme (OK) | 2026-10-30 20:40:39 | 2026-10-30 20:40:39 | 0 | `results/q1/konsey_zincir_durum.tsv:12` |
| konsey zinciri: B4_cozumleme (OK) | 2026-10-30 20:40:39 | 2026-10-30 20:40:42 | 3 | `results/q1/konsey_zincir_durum.tsv:13` |
| konsey zinciri: B5_cozumleme (OK) | 2026-10-30 20:40:42 | 2026-10-30 20:40:46 | 4 | `results/q1/konsey_zincir_durum.tsv:14` |
| konsey zinciri: zincir (TAMAM) | - | 2026-10-30 20:40:46 | - | `results/q1/konsey_zincir_durum.tsv:15` |
| ek zincir: regresyon (ozgun: rc=0 sure=24 s; catal: rc=0 sure=24 s; ozgun_onb: rc=0 sure=22 s; catal_onb: rc=0 sure=23 s) | 2026-10-31 03:58:56 | 2026-10-31 04:00:31 | 95 | `results/q1/ek_loglar/ek_zincir_1.log:1, results/q1/ek_loglar/ek_zincir_1.log:19` (bitis: sonraki adimin baslangici) |
| ek zincir: b8denetim (b8 denetim rc=0) | 2026-10-31 04:00:31 | 2026-10-31 04:07:58 | 447 | `results/q1/ek_loglar/ek_zincir_1.log:19, results/q1/ek_loglar/ek_zincir_1.log:23` (bitis: gunlugun 'bitti' satiri) |
| ek zincir: b9 (b9 rc=0) | 2026-10-31 04:08:49 | 2026-10-31 04:22:42 | 833 | `results/q1/ek_loglar/ek_zincir_2.log:1, results/q1/ek_loglar/ek_zincir_2.log:3` (bitis: sonraki adimin baslangici) |
| ek zincir: b8 (b8 rc=0) | 2026-10-31 04:22:42 | 2026-10-31 04:38:55 | 973 | `results/q1/ek_loglar/ek_zincir_2.log:3, results/q1/ek_loglar/ek_zincir_2.log:8` (bitis: sonraki adimin baslangici) |
| ek zincir: b10 (b10 c10 rc=0; b10 c100 rc=0; b10 in rc=0) | 2026-10-31 04:38:55 | 2026-10-31 04:43:46 | 291 | `results/q1/ek_loglar/ek_zincir_2.log:8, results/q1/ek_loglar/ek_zincir_2.log:12` (bitis: sonraki adimin baslangici) |
| ek zincir: cozumleme | 2026-10-31 04:43:46 | 2026-10-31 04:44:09 | 23 | `results/q1/ek_loglar/ek_zincir_2.log:12, results/q1/ek_loglar/ek_zincir_2.log:22` (bitis: gunlugun 'bitti' satiri) |
| masa cozumlemesi: bootstrap_cifar10.json | 2026-10-31 15:03:21.836906 | - | - | `results/q1/konsey_ek_masa/bootstrap_cifar10.json` meta.uretildi_utc |
| masa cozumlemesi: bootstrap_cifar100.json | 2026-10-31 15:03:29.780096 | - | - | `results/q1/konsey_ek_masa/bootstrap_cifar100.json` meta.uretildi_utc |
| masa cozumlemesi: mantel_aile.json | 2026-10-31 15:06:36.581560 | - | - | `results/q1/konsey_ek_masa/mantel_aile.json` meta.uretildi_utc |
| masa cozumlemesi: kesifsel.json | 2026-10-31 15:07:01.403456 | - | - | `results/q1/konsey_ek_masa/kesifsel.json` meta.uretildi_utc |
| masa cozumlemesi: a2_basit_etkiler.json | 2026-10-31 15:37:09.263421 | - | - | `results/q1/konsey_ek_masa/a2_basit_etkiler.json` meta.uretildi_utc |
| masa cozumlemesi: a9_2q_eksi_1.json | 2026-10-31 15:37:09.266134 | - | - | `results/q1/konsey_ek_masa/a9_2q_eksi_1.json` meta.uretildi_utc |
| masa cozumlemesi: a10_b4_varsayilan_bekci.json | 2026-10-31 15:37:18.283682 | - | - | `results/q1/konsey_ek_masa/a10_b4_varsayilan_bekci.json` meta.uretildi_utc |
| masa cozumlemesi: a10_b2_varsayilan_bekci.json | 2026-10-31 15:37:19.974223 | - | - | `results/q1/konsey_ek_masa/a10_b2_varsayilan_bekci.json` meta.uretildi_utc |
| masa cozumlemesi: a10_b4.json | 2026-10-31 15:37:21.559767 | - | - | `results/q1/konsey_ek_masa/a10_b4.json` meta.uretildi_utc |
| masa cozumlemesi: a10_b2.json | 2026-10-31 15:37:23.570831 | - | - | `results/q1/konsey_ek_masa/a10_b2.json` meta.uretildi_utc |
| masa cozumlemesi: a10_panel.json | 2026-10-31 15:37:24.179897 | - | - | `results/q1/konsey_ek_masa/a10_panel.json` meta.uretildi_utc |

(b) Blok basina matris boyutlari (`matrisler`; B10 satirlarinda 'Hucre' sutunu sirasiz cift sayisidir):

| Blok | Saldiri | n goruntu | Model | Hucre / cift | eps x 255 | Kaynak |
|---|---|---|---|---|---|---|
| B2 | pgd | 10000 | 14 | 196 | 8 | `results/q1/konsey_b2_panel/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B4 | pgd | 10000 | 20 | 400 | 8 | `results/q1/konsey_b4_matris/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B5-MI | mi | 10000 | 19 | 228 | 8 | `results/q1/konsey_b5_saldiri/mi/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B5-TGR | tgr | 10000 | 19 | 95 | 8 | `results/q1/konsey_b5_saldiri/tgr/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B9 | pgd | 10000 | 15 | 225 | 8 | `results/q1/konsey_b9_c100/matris/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B8 | pgd | 2000 | 14 | 196 | 4 | `results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json attack, n_samples, models, results, sources, eps` |
| B6-AA | - | 1000 | 6 | - | - | `results/q1/konsey_b6_maskeleme.json n, modeller` |
| B10-cifar10 | - | - | 20 | 190 | - | `results/q1/konsey_b10_gradyan/mantel_cifar10.json sinamalar.ham.K, .cift_sayisi` |
| B10-cifar100 | - | - | 15 | 105 | - | `results/q1/konsey_b10_gradyan/mantel_cifar100.json sinamalar.ham.K, .cift_sayisi` |
| B10-imagenetv2 | - | - | 14 | 91 | - | `results/q1/konsey_b10_gradyan/mantel_imagenetv2.json sinamalar.ham.K, .cift_sayisi` |

Donanim (`donanim`): NVIDIA GeForce RTX 5090, toplam bellek 32607 MiB, zincir basinda kullanilan 4214 MiB (`logs/konsey_zincir.log:18-19 (nvidia-smi dokumu, B3 on denetimi)`); ek zincir basinda kullanilan 2804 / 32607 MiB (`results/q1/ek_loglar/ek_zincir_1.log:2`). B3 toplam egitim suresi bu bolumde tekrarlanmaz: M9.1 satir 1470 (satir ayni); `results/q1/konsey_b3_defter.tsv sure_s (asama temiz ve AT satirlari toplami)` ile yeniden hesaplanan toplam iki ondalikta o satirdaki degerle ayni evet; zincir gunlugu karsiligi `logs/konsey_zincir.log:77`; egitim payi on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:171`.

(c) Sapma kaydi basliklari (`sapma_kaydi_basliklari`; `results/q1_research/ONKAYIT_SAPMALAR.md` '###' satirlari):

| Tarih | Baslik | 'sapma degil' ibaresi | Kaynak |
|---|---|---|---|
| 2026-10-30 | indirme kaydı: ImageNetV2 arşivi (sapma değil) | evet | `results/q1_research/ONKAYIT_SAPMALAR.md:7` |
| 2026-10-30 | kod eki: üç yeni betiğin dondurma anındaki özetleri (sapma değil) | evet | `results/q1_research/ONKAYIT_SAPMALAR.md:17` |
| 2026-10-30 | not: çatal regresyonu (sapma değil) | evet | `results/q1_research/ONKAYIT_SAPMALAR.md:30` |
| 2026-10-31 | not: GPU çatal regresyonu ve B8 ön işleme denetimi (sapma değil) | evet | `results/q1_research/ONKAYIT_SAPMALAR.md:34` |
| 2026-10-31 | ana ön kayıt §7 kayıtları (B2-B6 sonrası) | hayir | `results/q1_research/ONKAYIT_SAPMALAR.md:40` |
| 2026-10-31 | ek ön kayıt §12 kayıtları (B8-B10 sonrası) | hayir | `results/q1_research/ONKAYIT_SAPMALAR.md:53` |
| 2026-10-31 | ana ön kayıt §7: hiyerarşik bootstrap duyarlılığı sonradan üretildi | hayir | `results/q1_research/ONKAYIT_SAPMALAR.md:67` |
| 2026-10-31 | ek ön kayıt §12: S10-3 sonradan üretildi | hayir | `results/q1_research/ONKAYIT_SAPMALAR.md:75` |
| 2026-10-31 | keşifsel: A2/A9/A10 türetilmiş ve yeniden panelli çözümleme (ön kayıt dışı) | hayir | `results/q1_research/ONKAYIT_SAPMALAR.md:89` |

Kayit oncesi gorulen veriler (`kayit_oncesi_gorulen_veriler`): ana on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md:5-14`, ek on kayit `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md:5-14`. Denetimler (`denetimler`): B3 asama sayisi 12; defter baslangiclari zincir gunluguyle ayni evet; defter ile gunluk bitis farki en buyuk 0 s; on kayit dondurmasi B2 matrisinden once evet; ek dondurma B3 kuyrugu sirasinda evet; ek dondurma ek zincirden once evet.

Bu bolumde (M13.1-M13.3) satir sha256'si JSON'daki kayittan farkli cikan foy referanslari: yok.

_Kaynak: `results/q1/konsey_zaman_cizelgesi.json` etiket, meta (foy_ozeti, yeniden_uretim_notu dahil); saat_dilimi; dondurma.<on_kayit|ek_on_kayit>.{commit, utc, kaynak, dondurma_commiti_dosyayi_ekleyen_ilk_commit}; B2; konsey_zinciri[]; B3_asamalari[]; ek_zincir[]; masa_cozumlemeleri; matrisler; donanim; egitim_suresi; sapma_kaydi_basliklari; kayit_oncesi_gorulen_veriler; denetimler_


## Sabit dizgeler (artefakttan OKUNMAYAN, elle tasinmis literaller)

_Kaynak: `scripts/build_reference_sheet.py (satir numaralari calisma aninda bulunur)`_

Asagidaki sayilar bu betikte string literal olarak durur; uretilemedikleri icin DOGRULANMIS SAYILMAZ. Metne girmeleri durumunda kaynak notu gerekir.

| Sabit dizge | Foyde nerede | Betikte satir | Kaynak durumu |
|---|---|---|---|
| Kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33; n=7260 (makale Tablo 2 alt blok) | 'Tablo II: kosullu ayrisma' | 171 | KARANTINADAKI ESKI KOSU (C1 oncesi, sizintili tek kosu), ELLE TASINMIS LITERAL; hangi dosyadan alindigi betikte kayitli degil; bu betik karantina yolundan okumaz, dogrulayamaz |
| 'run3 fark' sutunu (makale Tablo 3 Diff dagger): 8.27, 0.63, 5.33, 11.17 (sirayla Unconditioned, Target-correct, Both-correct, Successful-source) | 'Tablo III: transfer protokolleri' | 199 | literal DEGIL, `c1_transfer_summary.json` icindeki `old_run3_diff` alani; ancak `scripts/c1_transfer_aggregate.py` bu alani karantinadaki `results/rev2_blockA/a2_transfer_protocols.json` (tek kosu, sizintili) dosyasindan tasimistir. Bu betik o dosyayi OKUMAZ; deger yalniz summary JSON'daki kopyadir |
| WRN-28-10 satiri: temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 | 'Tablo I: ana gurbuzluk' | 142 | literal; temiz/FGSM/PGD `results/wrn_eval/wrn_eval_summary.json` ile UYUSUYOR; AA 62.76 harici RobustBench raporudur, yerel AA artefakti ARTEFAKT YOK |
