# E7 Transfer Protokolleri - SVHN, 2 Tohum

Ayni istatistik kodu (a2_transfer_protocols.py), E7 (SVHN, kisa surum) kontrol noktalarina uygulandi. Her satir 2 tohum ortalamasi +- std. UCUNCU MIMARI YOKTUR (2x2 matris).

| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |
|---|---|---|---|---|
| Kosulsuz (ham) | 31.89 +- 0.95 | 31.49 +- 0.87 | **0.39 +- 0.08** | - |
| Hedef dogru | 26.32 +- 0.60 | 27.33 +- 0.38 | **-1.00 +- 0.22** | - |
| Her ikisi dogru | 25.36 +- 0.40 | 25.70 +- 0.42 | **-0.35 +- 0.01** | - |
| Basarili kaynak | 62.50 +- 0.93 | 59.86 +- 0.91 | **2.64 +- 0.03** | - |

## Her ikisi dogru eslesmis analiz

- Ortak kume n = 23718 +- 216
- Fark = -0.35 +- 0.01 puan (run3: -)
- Eslesmis bootstrap GA (ort): [-0.77; 0.06]
- Isaret cevirme permutasyon p (en buyuk): 0.10465
- Herhangi bir tohum/marjda TOST esdegerligi: EVET

## Protokolun yarattigi yayilim

Ayni modeller, ayni veri: en buyuk ve en kucuk protokol farki arasindaki mesafe 3.65 +- 0.19 puan.

