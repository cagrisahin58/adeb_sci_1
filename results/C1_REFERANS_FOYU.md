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


## Sabit dizgeler (artefakttan OKUNMAYAN, elle tasinmis literaller)

_Kaynak: `scripts/build_reference_sheet.py (satir numaralari calisma aninda bulunur)`_

Asagidaki sayilar bu betikte string literal olarak durur; uretilemedikleri icin DOGRULANMIS SAYILMAZ. Metne girmeleri durumunda kaynak notu gerekir.

| Sabit dizge | Foyde nerede | Betikte satir | Kaynak durumu |
|---|---|---|---|
| Kos. yaniltma PGD 52.15 vs 52.33, AA 58.16 vs 56.46; her ikisi dogru PGD 54.92 vs 49.61, AA 48.15 vs 45.33; n=7260 (makale Tablo 2 alt blok) | 'Tablo II: kosullu ayrisma' | 171 | KARANTINADAKI ESKI KOSU (C1 oncesi, sizintili tek kosu), ELLE TASINMIS LITERAL; hangi dosyadan alindigi betikte kayitli degil; bu betik karantina yolundan okumaz, dogrulayamaz |
| 'run3 fark' sutunu (makale Tablo 3 Diff dagger): 8.27, 0.63, 5.33, 11.17 (sirayla Unconditioned, Target-correct, Both-correct, Successful-source) | 'Tablo III: transfer protokolleri' | 199 | literal DEGIL, `c1_transfer_summary.json` icindeki `old_run3_diff` alani; ancak `scripts/c1_transfer_aggregate.py` bu alani karantinadaki `results/rev2_blockA/a2_transfer_protocols.json` (tek kosu, sizintili) dosyasindan tasimistir. Bu betik o dosyayi OKUMAZ; deger yalniz summary JSON'daki kopyadir |
| WRN-28-10 satiri: temiz 89.48 / FGSM 70.91 / PGD 66.92 / AA 62.76 | 'Tablo I: ana gurbuzluk' | 142 | literal; temiz/FGSM/PGD `results/wrn_eval/wrn_eval_summary.json` ile UYUSUYOR; AA 62.76 harici RobustBench raporudur, yerel AA artefakti ARTEFAKT YOK |
