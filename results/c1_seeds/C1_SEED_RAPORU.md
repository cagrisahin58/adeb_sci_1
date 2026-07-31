# C1: 3 Tohumlu (seed) Sonuclar - Sizinti Duzeltmeli Protokol

Sabit ortak 2000 orneklik dogrulama bolmesi (seed 777) clean on-egitimden ONCE ayrildi; model secimi val PGD-10 uzerinden. Tum degerlendirmeler tam test kumesinde (n=10000).

## Cift bazinda

| Cift | Model | Temiz | PGD-10 | AA | Kos. yanilt. (PGD) | Kos. yanilt. (AA) |
|---|---|---|---|---|---|---|
| 1 (s1001) | ResNet-18 AT | 85.37 | 44.67 | 37.93 | 47.67 | 55.57 |
| 1 (s2001) | ViT-Tiny AT | 74.10 | 32.73 | 29.59 | 55.83 | 60.07 |
| 2 (s1002) | ResNet-18 AT | 85.94 | 43.93 | 37.79 | 48.88 | 56.03 |
| 2 (s2002) | ViT-Tiny AT | 73.47 | 32.46 | 28.86 | 55.82 | 60.72 |
| 3 (s1003) | ResNet-18 AT | 86.04 | 43.73 | 38.07 | 49.17 | 55.75 |
| 3 (s2003) | ViT-Tiny AT | 73.01 | 32.89 | 28.96 | 54.95 | 60.33 |

## Ortalama +- std (3 tohum)

| Metrik | ResNet-18 AT | ViT-Tiny AT | Fark (R-V) |
|---|---|---|---|
| Temiz | 85.78 +- 0.36 | 73.53 +- 0.55 | 12.26 +- 0.90 |
| PGD-10 | 44.11 +- 0.50 | 32.69 +- 0.22 | 11.42 +- 0.55 |
| AutoAttack | 37.93 +- 0.14 | 29.14 +- 0.40 | 8.79 +- 0.40 |
| Kosullu yaniltma (PGD) | 48.58 +- 0.80 | 55.53 +- 0.50 | -6.96 +- 1.19 |
| Kosullu yaniltma (AA) | 55.78 +- 0.23 | 60.37 +- 0.33 | -4.59 +- 0.10 |

## Kosullu ayrisma (robust = temiz x kosullu hayatta kalma)

- Cift 1 ResNet-18 (AA): 85.37 x 44.43% = 37.93 (olculen 37.93)
- Cift 1 ViT-Tiny (AA): 74.10 x 39.93% = 29.59 (olculen 29.59)
- Cift 2 ResNet-18 (AA): 85.94 x 43.97% = 37.79 (olculen 37.79)
- Cift 2 ViT-Tiny (AA): 73.47 x 39.28% = 28.86 (olculen 28.86)
- Cift 3 ResNet-18 (AA): 86.04 x 44.25% = 38.07 (olculen 38.07)
- Cift 3 ViT-Tiny (AA): 73.01 x 39.67% = 28.96 (olculen 28.96)

## Her ikisi dogru (both-correct) eslesmis alt kume

| Cift | n (PGD) | ResNet PGD | ViT PGD | n (AA) | ResNet AA | ViT AA |
|---|---|---|---|---|---|---|
| 1 | 7126 | 60.26 | 45.82 | 7126 | 51.60 | 41.45 |
| 2 | 7067 | 59.62 | 45.72 | 7067 | 51.61 | 40.71 |
| 3 | 6991 | 59.72 | 46.79 | 6991 | 52.45 | 41.30 |

## Kosu bazinda McNemar (tam binom, iki yonlu)

| Cift | Saldiri | Yalniz ResNet dogru | Yalniz ViT dogru | p |
|---|---|---|---|---|
| 1 | PGD-10 | 1677 | 483 | 1.172e-153 |
| 1 | AutoAttack | 1362 | 528 | 1.231e-84 |
| 2 | PGD-10 | 1658 | 511 | 1.272e-140 |
| 2 | AutoAttack | 1397 | 504 | 1.081e-96 |
| 3 | PGD-10 | 1665 | 581 | 1.917e-120 |
| 3 | AutoAttack | 1478 | 567 | 3.208e-93 |

## Sure

Toplam C1 GPU zamani: 21.68 saat (RTX 5090).

