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

Eski tek kosu (sizintili) karsilastirmasi: kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33 (n=7260).

McNemar (kosu bazinda, tam binom): 
- cift 1: PGD p=1.2e-153 (1677/483), AA p=1.2e-84 (1362/528)
- cift 2: PGD p=1.3e-140 (1658/511), AA p=1.1e-96 (1397/504)
- cift 3: PGD p=1.9e-120 (1665/581), AA p=3.2e-93 (1478/567)

## Tablo III: transfer protokolleri

_Kaynak: `results/c1_transfer/c1_transfer_summary.json`_

| Protokol | CNN->ViT | ViT->CNN | Fark | N (CNN->ViT / ViT->CNN) | run3 fark |
|---|---|---|---|---|---|
| Kosulsuz (ham) | 41.02$\pm$0.55 | 27.45$\pm$0.27 | +13.57$\pm$0.33 | 10000 / 10000 | - |
| Hedef dogru | 19.87$\pm$0.18 | 15.51$\pm$0.59 | +4.36$\pm$0.44 | 7353 / 8579 | 0.63 |
| Her ikisi dogru | 18.25$\pm$0.17 | 9.98$\pm$0.31 | +8.27$\pm$0.23 | 7061 / 7061 | 5.33 |
| Basarili kaynak | 36.39$\pm$0.76 | 17.02$\pm$0.52 | +19.37$\pm$1.27 | 2831 / 3814 | 5.28 |

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

- cos_cls: minimum blok 10, deger 0.9343
- cos_token_mean: minimum blok 8, deger 0.9840
- cos_flat_all_tokens: minimum blok 8, deger 0.9663
- cos_block_output: minimum blok 11, deger 0.9803
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
