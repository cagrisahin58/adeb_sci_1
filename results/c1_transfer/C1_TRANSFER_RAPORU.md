# C1 Transfer Protokolleri - 3 Tohum

Ayni istatistik kodu (a2_transfer_protocols.py), C1 sizinti-duzeltmeli kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std.

| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |
|---|---|---|---|---|
| Kosulsuz (ham) | 41.02 +- 0.55 | 27.45 +- 0.27 | **13.57 +- 0.33** | +8.27 |
| Hedef dogru | 19.87 +- 0.18 | 15.51 +- 0.59 | **4.36 +- 0.44** | +0.63 |
| Her ikisi dogru | 18.25 +- 0.17 | 9.98 +- 0.31 | **8.27 +- 0.23** | +5.33 |
| Basarili kaynak | 36.39 +- 0.76 | 17.02 +- 0.52 | **19.37 +- 1.27** | +11.17 |

## Her ikisi dogru eslesmis analiz

- Ortak kume n = 7061 +- 68
- Fark = 8.27 +- 0.24 puan (run3: 5.33)
- Eslesmis bootstrap GA (ort): [7.33; 9.22]
- Isaret cevirme permutasyon p (en buyuk): 0.0
- Herhangi bir tohum/marjda TOST esdegerligi: HAYIR

## Protokolun yarattigi yayilim

Ayni modeller, ayni veri: en buyuk ve en kucuk protokol farki arasindaki mesafe 15.01 +- 0.84 puan.

