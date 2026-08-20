# C3: WRN dahil 3x3 transfer matrisi (3 tohum)

| kaynak -> hedef | ham | kosullu (hedef dogru) | ham - kosullu | hedef temiz |
|---|---|---|---|---|
| ResNet18_AT -> ResNet18_AT | 80.70+-0.24 | 69.76+-0.87 | +10.94 | 63.85 |
| ResNet18_AT -> ViT_Tiny_AT | 67.64+-0.85 | 25.67+-0.22 | +41.97 | 43.17 |
| ResNet18_AT -> WRN_28_10 | 51.23+-0.25 | 23.44+-0.38 | +27.80 | 63.64 |
| ViT_Tiny_AT -> ResNet18_AT | 49.10+-0.41 | 20.71+-0.90 | +28.39 | 63.85 |
| ViT_Tiny_AT -> ViT_Tiny_AT | 88.84+-0.56 | 74.14+-1.52 | +14.70 | 43.17 |
| ViT_Tiny_AT -> WRN_28_10 | 46.10+-0.48 | 15.50+-0.72 | +30.60 | 63.64 |
| WRN_28_10 -> ResNet18_AT | 60.28+-0.16 | 37.83+-0.90 | +22.45 | 63.85 |
| WRN_28_10 -> ViT_Tiny_AT | 69.65+-1.03 | 30.04+-0.66 | +39.61 | 43.17 |
| WRN_28_10 -> WRN_28_10 | 64.35+-0.00 | 43.98+-0.00 | +20.37 | 63.64 |

## (ham - kosullu) ile hedefin temiz hatasi iliskisi

Kosegen disi 6 yon uzerinde Pearson r = 0.931, egim = 0.656 puan/puan (kesisim +3.50).
Yorum: ham oranin kosullu orandan sapmasi neredeyse tamamen hedefin temiz hatasiyla aciklaniyor; ham transfer oranlari mimari karsilastirmasi icin uygun bir olcut degil.


## Gelen transfer ile hedefin kendi kirilganligi

| hedef | kendi beyaz kutu kosullu yaniltma | gelen transfer (ortalama) |
|---|---|---|
| ResNet18_AT | 69.76 | 29.27 |
| ViT_Tiny_AT | 74.14 | 27.86 |
| WRN_28_10 | 43.98 | 19.47 |

Uc hedef uzerinde Pearson r = 0.964. Gelen transfer oranlari, kaynak mimarisinden cok hedefin kendi kirilganligini izliyor: en gurbuz hedef (WRN) her iki kaynaktan da en az etkileniyor. Yani CNN$\to$ViT ile ViT$\to$CNN arasindaki fark, 'CNN saldirilari daha gucludur'dan cok 'ViT daha zayif bir hedeftir' okumasiyla tutarli.

