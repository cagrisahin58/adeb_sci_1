# E1 Transfer Protokolleri - CIFAR-100, 3 Tohum

Ayni istatistik kodu (a2_transfer_protocols.py), E1 (CIFAR-100) kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std.

| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |
|---|---|---|---|---|
| Kosulsuz (ham) | 67.64 +- 0.85 | 49.10 +- 0.41 | **18.53 +- 0.71** | - |
| Hedef dogru | 25.67 +- 0.22 | 20.71 +- 0.90 | **4.96 +- 1.01** | - |
| Her ikisi dogru | 23.33 +- 0.18 | 12.41 +- 0.35 | **10.92 +- 0.34** | - |
| Basarili kaynak | 33.88 +- 0.68 | 16.38 +- 0.27 | **17.50 +- 0.92** | - |

## Her ikisi dogru eslesmis analiz

- Ortak kume n = 3886 +- 88
- Fark = 10.92 +- 0.34 puan (run3: -)
- Eslesmis bootstrap GA (ort): [9.47; 12.35]
- Isaret cevirme permutasyon p (en buyuk): 0.0
- Herhangi bir tohum/marjda TOST esdegerligi: HAYIR

## Protokolun yarattigi yayilim

Ayni modeller, ayni veri: en buyuk ve en kucuk protokol farki arasindaki mesafe 13.83 +- 1.30 puan.

