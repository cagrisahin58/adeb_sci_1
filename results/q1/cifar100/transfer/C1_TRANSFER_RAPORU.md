# C1 Transfer Protokolleri - 3 Tohum

Ayni istatistik kodu (a2_transfer_protocols.py), C1 sizinti-duzeltmeli kontrol noktalarina uygulandi. Her satir 3 tohum ortalamasi +- std.

| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |
|---|---|---|---|---|
| Kosulsuz (ham) | 67.64 +- 0.85 | 49.10 +- 0.41 | **18.53 +- 0.71** | - |
| Hedef dogru | 25.67 +- 0.22 | 20.71 +- 0.90 | **4.96 +- 1.01** | - |
| Her ikisi dogru | 23.33 +- 0.18 | 12.41 +- 0.35 | **10.92 +- 0.34** | - |
| Basarili kaynak | 35.97 +- 0.94 | 24.53 +- 0.94 | **11.44 +- 1.82** | - |

## Her ikisi dogru eslesmis analiz

- Ortak kume n = 3886 +- 88
- Fark = 10.92 +- 0.34 puan (run3: -)
- Eslesmis bootstrap GA (ort): [9.48; 12.36]
- Isaret cevirme permutasyon p (en buyuk): 0.0
- Herhangi bir tohum/marjda TOST esdegerligi: HAYIR

## Protokolun yarattigi yayilim

Ayni modeller, ayni veri: en buyuk ve en kucuk protokol farki arasindaki mesafe 13.58 +- 1.71 puan.

