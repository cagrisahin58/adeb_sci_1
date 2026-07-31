# C4 + C5: n=1000 oznitelik/attention ve mekansal lokalite (3 tohum)

## ViT: oznitelik kaymasi, agregasyon varyantina gore

| Blok | CLS jetonu | Yama jetonlari ortalamasi | Tum jetonlar (duzlestirilmis) | Blok cikisi |
|---|---|---|---|---|
| 1 | 0.9993$\pm$0.0002 | 0.9989$\pm$0.0005 | 0.9942$\pm$0.0012 | 0.9927$\pm$0.0004 |
| 2 | 0.9910$\pm$0.0044 | 0.9957$\pm$0.0020 | 0.9868$\pm$0.0036 | 0.9901$\pm$0.0013 |
| 3 | 0.9785$\pm$0.0087 | 0.9928$\pm$0.0007 | 0.9821$\pm$0.0022 | 0.9881$\pm$0.0011 |
| 4 | 0.9709$\pm$0.0059 | 0.9877$\pm$0.0038 | 0.9734$\pm$0.0022 | 0.9861$\pm$0.0016 |
| 5 | 0.9652$\pm$0.0063 | 0.9870$\pm$0.0049 | 0.9719$\pm$0.0035 | 0.9847$\pm$0.0019 |
| 6 | 0.9596$\pm$0.0079 | 0.9873$\pm$0.0029 | 0.9712$\pm$0.0034 | 0.9835$\pm$0.0020 |
| 7 | 0.9497$\pm$0.0072 | 0.9870$\pm$0.0048 | 0.9698$\pm$0.0056 | 0.9826$\pm$0.0020 |
| 8 | 0.9414$\pm$0.0105 | 0.9840$\pm$0.0036 | 0.9663$\pm$0.0039 | 0.9816$\pm$0.0021 |
| 9 | 0.9353$\pm$0.0044 | 0.9850$\pm$0.0038 | 0.9675$\pm$0.0019 | 0.9809$\pm$0.0018 |
| 10 | 0.9343$\pm$0.0084 | 0.9877$\pm$0.0025 | 0.9696$\pm$0.0039 | 0.9805$\pm$0.0017 |
| 11 | 0.9352$\pm$0.0037 | 0.9912$\pm$0.0018 | 0.9753$\pm$0.0028 | 0.9803$\pm$0.0017 |
| 12 | 0.9779$\pm$0.0147 | 0.9955$\pm$0.0051 | 0.9884$\pm$0.0101 | 0.9837$\pm$0.0036 |

En dusuk kosinusun gorildigu blok (1-tabanli): CLS jetonu = 10 (0.9343), Yama jetonlari ortalamasi = 8 (0.9840), Tum jetonlar (duzlestirilmis) = 8 (0.9663), Blok cikisi = 11 (0.9803)

## ResNet: katman profili (n=1000)

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

## ViT attention: entropi degisimi ve CLS yer degistirmesi

| Katman | Entropi degisimi (adv - temiz) | CLS yer degistirmesi (toplam varyasyon) |
|---|---|---|
| 1 | +0.0000$\pm$0.0006 | 0.0276$\pm$0.0102 |
| 2 | -0.0016$\pm$0.0007 | 0.0423$\pm$0.0071 |
| 3 | +0.0002$\pm$0.0014 | 0.0492$\pm$0.0088 |
| 4 | +0.0007$\pm$0.0017 | 0.0448$\pm$0.0077 |
| 5 | -0.0025$\pm$0.0021 | 0.0528$\pm$0.0043 |
| 6 | -0.0015$\pm$0.0020 | 0.0652$\pm$0.0100 |
| 7 | +0.0011$\pm$0.0036 | 0.0726$\pm$0.0065 |
| 8 | +0.0014$\pm$0.0067 | 0.0779$\pm$0.0060 |
| 9 | +0.0013$\pm$0.0019 | 0.0785$\pm$0.0105 |
| 10 | +0.0045$\pm$0.0088 | 0.0776$\pm$0.0079 |
| 11 | -0.0011$\pm$0.0036 | 0.0836$\pm$0.0025 |
| 12 | -0.0033$\pm$0.0057 | 0.0841$\pm$0.0076 |

## Saldirida devrilen ve devrilmeyen ornekler (son blok, tum jetonlar)

- ViT son blok kosinusu: devrilen 0.9895$\pm$0.0091, devrilmeyen 0.9877$\pm$0.0108

- ResNet layer4.1 kosinusu: devrilen 0.9058$\pm$0.0037, devrilmeyen 0.9143$\pm$0.0077

## C5: gradyanlarin mekansal lokalitesi (n=500)

| Olcut | ResNet-18 AT | ViT-Tiny AT | Eslesmis fark (R-V) | Wilcoxon p |
|---|---|---|---|---|
| Enerjinin %50'sini tasiyan alan orani | 0.0378$\pm$0.0017 | 0.0397$\pm$0.0010 | -0.0019$\pm$0.0027 | 2.63e-01 |
| Enerjinin %90'ini tasiyan alan orani | 0.2345$\pm$0.0078 | 0.2570$\pm$0.0067 | -0.0224$\pm$0.0133 | 3.85e-02 |
| Mekansal entropi (nat) | 5.2014$\pm$0.0387 | 5.2524$\pm$0.0197 | -0.0509$\pm$0.0580 | 8.00e-01 |
| Moran's I (4-komsuluk) | 0.4141$\pm$0.0132 | 0.3941$\pm$0.0024 | +0.0200$\pm$0.0156 | 5.35e-01 |

Dusuk alan orani ve dusuk entropi = daha lokalize; yuksek Moran's I = enerji bitisik piksellerde daha kumeli.

