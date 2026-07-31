# C3: WRN dahil 3x3 transfer matrisi (3 tohum)

| kaynak -> hedef | ham | kosullu (hedef dogru) | ham - kosullu | hedef temiz |
|---|---|---|---|---|
| ResNet18_AT -> ResNet18_AT | 55.84+-0.53 | 48.52+-0.84 | +7.32 | 85.79 |
| ResNet18_AT -> ViT_Tiny_AT | 41.07+-0.58 | 19.93+-0.20 | +21.14 | 73.53 |
| ResNet18_AT -> WRN_28_10 | 21.69+-0.09 | 12.48+-0.10 | +9.21 | 89.48 |
| ViT_Tiny_AT -> ResNet18_AT | 27.45+-0.34 | 15.52+-0.64 | +11.93 | 85.79 |
| ViT_Tiny_AT -> ViT_Tiny_AT | 67.34+-0.18 | 55.57+-0.44 | +11.76 | 73.53 |
| ViT_Tiny_AT -> WRN_28_10 | 18.25+-0.12 | 8.65+-0.14 | +9.60 | 89.48 |
| WRN_28_10 -> ResNet18_AT | 32.63+-0.14 | 21.48+-0.31 | +11.16 | 85.79 |
| WRN_28_10 -> ViT_Tiny_AT | 39.73+-0.25 | 18.15+-0.28 | +21.58 | 73.53 |
| WRN_28_10 -> WRN_28_10 | 33.03+-0.00 | 25.16+-0.00 | +7.87 | 89.48 |

## (ham - kosullu) ile hedefin temiz hatasi iliskisi

Kosegen disi 6 yon uzerinde Pearson r = 0.997, egim = 0.762 puan/puan (kesisim +1.09).
Yorum: ham oranin kosullu orandan sapmasi neredeyse tamamen hedefin temiz hatasiyla aciklaniyor; ham transfer oranlari mimari karsilastirmasi icin uygun bir olcut degil.


## Gelen transfer ile hedefin kendi kirilganligi

| hedef | kendi beyaz kutu kosullu yaniltma | gelen transfer (ortalama) |
|---|---|---|
| ResNet18_AT | 48.52 | 18.50 |
| ViT_Tiny_AT | 55.57 | 19.04 |
| WRN_28_10 | 25.16 | 10.57 |

Uc hedef uzerinde Pearson r = 0.986. Gelen transfer oranlari, kaynak mimarisinden cok hedefin kendi kirilganligini izliyor: en gurbuz hedef (WRN) her iki kaynaktan da en az etkileniyor. Yani CNN$\to$ViT ile ViT$\to$CNN arasindaki fark, 'CNN saldirilari daha gucludur'dan cok 'ViT daha zayif bir hedeftir' okumasiyla tutarli.

