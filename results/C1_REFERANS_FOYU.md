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

## Sabit dizgeler (artefakttan OKUNMAYAN, elle tasinmis literaller)

_Kaynak: `scripts/build_reference_sheet.py (satir numaralari calisma aninda bulunur)`_

Asagidaki sayilar bu betikte string literal olarak durur; uretilemedikleri icin DOGRULANMIS SAYILMAZ. Metne girmeleri durumunda kaynak notu gerekir.

| Sabit dizge | Foyde nerede | Betikte satir | Kaynak durumu |
|---|---|---|---|
| Kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33; n=7260 (makale Tablo 2 alt blok) | 'Tablo II: kosullu ayrisma' | 171 | KARANTINADAKI ESKI KOSU (C1 oncesi, sizintili tek kosu), ELLE TASINMIS LITERAL; hangi dosyadan alindigi betikte kayitli degil; bu betik karantina yolundan okumaz, dogrulayamaz |
| 'run3 fark' sutunu (makale Tablo 3 Diff dagger): 8.27, 0.63, 5.33, 11.17 (sirayla Unconditioned, Target-correct, Both-correct, Successful-source) | 'Tablo III: transfer protokolleri' | 199 | literal DEGIL, `c1_transfer_summary.json` icindeki `old_run3_diff` alani; ancak `scripts/c1_transfer_aggregate.py` bu alani karantinadaki `results/rev2_blockA/a2_transfer_protocols.json` (tek kosu, sizintili) dosyasindan tasimistir. Bu betik o dosyayi OKUMAZ; deger yalniz summary JSON'daki kopyadir |
| WRN-28-10 satiri: temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 | 'Tablo I: ana gurbuzluk' | 142 | literal; temiz/FGSM/PGD `results/wrn_eval/wrn_eval_summary.json` ile UYUSUYOR; AA 62.76 harici RobustBench raporudur, yerel AA artefakti ARTEFAKT YOK |
