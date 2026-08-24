# E6 Transfer Protokolleri - CIFAR-10, L2 tehdit modeli, 3 Tohum

Ayni istatistik kodu (a2_transfer_protocols.py), C1 kontrol noktalarina L2 BUTCESI (eps=0,5) altinda uygulandi. Her satir 3 tohum ortalamasi +- std. DIKKAT: modeller L-infinity ile EGITILMISTIR; bu sayilar L2-EGITILMIS referanslarla KARSILASTIRILAMAZ (E6_ON_KAYIT §0).

| Protokol | CNN->ViT | ViT->CNN | Fark | run3 fark |
|---|---|---|---|---|
| Kosulsuz (ham) | 32.83 +- 0.49 | 19.80 +- 0.34 | **13.03 +- 0.81** | - |
| Hedef dogru | 8.69 +- 0.15 | 6.57 +- 0.04 | **2.12 +- 0.18** | - |
| Her ikisi dogru | 7.69 +- 0.12 | 3.62 +- 0.24 | **4.07 +- 0.36** | - |
| Basarili kaynak | 21.44 +- 0.70 | 9.38 +- 0.68 | **12.06 +- 0.23** | - |

## Her ikisi dogru eslesmis analiz

- Ortak kume n = 7061 +- 68
- Fark = 4.07 +- 0.36 puan (run3: -)
- Eslesmis bootstrap GA (ort): [3.39; 4.76]
- Isaret cevirme permutasyon p (en buyuk): 0.0
- Herhangi bir tohum/marjda TOST esdegerligi: HAYIR

## Protokolun yarattigi yayilim

Ayni modeller, ayni veri: en buyuk ve en kucuk protokol farki arasindaki mesafe 10.92 +- 0.82 puan.

