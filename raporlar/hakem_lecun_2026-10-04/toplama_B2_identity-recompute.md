# B2: Ozdeslik ve manset ayrisiminin artifact'lardan yeniden hesabi

Toplayici B2, mercek B. Yalnizca olcum ve dogrulama; yargi yok. Betikler: `raporlar/hakem_lecun_2026-10-04/_tmp/b2_recompute.py`, `b2_extra.py` (cikti: `_tmp/b2out.txt`). Hesap konteynerde (adeb_eval, numpy), ornek bazli `per_sample_*.npz` maskelerinden (anahtarlar: target_clean_correct, target_adv_wrong, source_clean_correct, source_adv_wrong). Karantina klasorlerine basvurulmadi.

## 10 satirlik ozet
1. Makalenin manset sayilari (asimetriler 13.57 / 4.36 / 8.27 / 19.37; terimler 9.21 + 5.79; artik 3.91) ornek bazli maskelerden iki ondalikta yeniden uretildi; istisnalar 19.37 (maskelerden 19.36) ve 15.01 (maskelerden 15.00): ikisi de ozet JSON'daki iki-ondalik yuvarlanmis tohum degerlerinden geliyor.
2. SD'ler (0.33 / 0.44 / 0.23 / 1.27) ozet JSON'da yuvarlanmis tohum farklarindan hesaplanmis; maskelerden 0.33 / 0.43 / 0.23 / 1.26 cikiyor.
3. Ozdeslik onculu p: 36 yonde min 0.989014 (CIFAR-100 pair3, ViT->ResNet), max 1.000; artik -0.41..0.00; ort. mutlak artik 0.0947 (paper 0.095); artik/sapma en fazla %1.388 (paper 1.39). p'li bicim e*p + r_cond*(1-e) 1e-14 hassasiyetle tutuyor (cebirsel).
4. 36 yonun kaynagi `results/c1_c3` (CIFAR-10, WRN dahil) ve `results/q1/cifar100/transfer`; `results/c1_transfer` yalniz ResNet<->ViT icerir (6 yon, p 0.9943..0.9985).
5. `c1_c3` ile `c1_transfer`, ayni modellerin iki ayri saldiri kosusu: ham ResNet->ViT 41.07 (tab:transfer_matrix) ile 41.02 (tab:transfer_protocols); ham asimetri tohumlari 13.19/13.89/13.79 ile 13.20/13.69/13.83.
6. 3x3 iddiasi r=0.986 yeniden uretildi (0.9862; n=3 hedef); gelen kosullu transfer [18.50, 19.04, 10.57], kosegen kosullu [48.52, 55.57, 25.16].
7. Egimler: CIFAR-10 0.7625-0.7628 (paper 0.762), CIFAR-100 0.6565-0.6570 (paper 0.656); Pearson r CIFAR-10 0.9970, CIFAR-100 0.9306 (paper yalniz CIFAR-10 r'sini veriyor).
8. CIFAR-100 yayilim 13.58 (13.5765), tohum basina ort. 13.83, artik 5.97; SVHN artik 0.65-0.66 ve isaret degisimi (raw +0.39, tc -1.01/-1.00, bc -0.35, ss +2.69/+2.70) yeniden uretildi.
9. Uretilemeyen/bulunamayan: "p=0.88, standart egitimli hedef, duzeltme oncesi" (mevcut artifact'larda standart egitimli hedef yok); CIFAR-100 egimi icin kayit dosyasi; L2 ss 12.06 (maskelerden 12.05); +0.914 egimi hesaplanmadi.
10. `c1_c3` per-sample dosyalarinda `source_adv_wrong` yok; successful-source bu dizinden uretilemez.

## Tablo A. CIFAR-10 manset ayrisimi
Kaynak: `results/c1_transfer/pair{1,2,3}/per_sample_{ResNet18_AT_to_ViT_Tiny_AT,ViT_Tiny_AT_to_ResNet18_AT}.npz`. Protokol tanimi (`a2_transfer_protocols.json`, "ss_definition": "target_clean_correct & source_clean_correct & source_adv_wrong"): raw = tum N; tc = hedef temiz-dogru; bc = hedef ve kaynak temiz-dogru; ss = ss_definition maskesi.

| Protokol | pair1 (CNN->ViT, ViT->CNN, fark) | pair2 | pair3 | Ort. fark (yeniden hesap) | Paper / ozet JSON | Uyum (2 ondalik) |
|---|---|---|---|---|---|---|
| raw | 40.50, 27.30, 13.20 | 40.97, 27.28, 13.69 | 41.59, 27.76, 13.83 | 13.5733 | 13.57 (tab:transfer_protocols; c1_transfer_summary.json protocols.raw.diff.mean 13.5733) | evet |
| target_correct | 19.7571, 14.935, 4.8221 | 19.7632, 15.4759, 4.2873 | 20.0794, 16.1069, 3.9725 | 4.3606 | 4.36 | evet |
| both_correct | 18.1448, 9.6267, 8.5181 | 18.169, 10.1174, 8.0515 | 18.438, 10.1988, 8.2392 | 8.2696 | 8.27 | evet |
| successful_source | 37.2563, 16.4642, 20.7921 | 36.049, 17.1399, 18.9091 | 35.8591, 17.4658, 18.3933 | 19.3648 | 19.37 (ozet JSON 19.3667 = yuvarlanmis [20.8, 18.91, 18.39] ortalamasi) | HAYIR: 19.36 vs 19.37 |

n (CNN->ViT / ViT->CNN, tohum ortalamasi): raw 10000/10000; tc 7353 (7410, 7347, 7301) / 8579 (8537, 8594, 8605); bc 7061 (7126, 7067, 6991) paylasimli; ss 2831 (2821, 2860, 2811) / 3814 (3869, 3839, 3733). Paper 04_experiments.tex:117 ile ayni.

Tohum SD'leri (n-1):

| Protokol | Maskelerden SD | Ozet JSON std | Paper | Uyum |
|---|---|---|---|---|
| raw | 0.3308 | 0.3308 | 0.33 | evet |
| tc | 0.4295 | 0.4355 | 0.44 | HAYIR: 0.43 vs 0.44 |
| bc | 0.2348 | 0.2312 | 0.23 | evet |
| ss | 1.2627 | 1.27 | 1.27 | HAYIR: 1.26 vs 1.27 |

Ayrisim aritmetigi (protokol ortalamalari, maskelerden): raw - tc = 13.5733 - 4.3606 = 9.2127 (paper 9.21, evet); ss - raw = 19.3648 - 13.5733 = 5.7915 (5.79, evet); bc - tc = 8.2696 - 4.3606 = 3.9090 (3.91, evet); toplam 9.2127 + 5.7915 = 15.0042 (paper 15.01; metin 04_experiments.tex:117 yuvarlanmis terimlerin toplamini 15.00 diye kendisi belirtiyor).

Tohum basina yayilim (max - min, 4 protokol): maskelerden 15.9700, 14.6218, 14.4208, ort. 15.0042, SD 0.8424. Ozet JSON `protocol_spread_pp`: [15.97, 14.63, 14.42], ort. 15.0067, SD 0.8409; `fig_protokol_kumeleri_veri.json` ayrisim.yayilim 15.01. Paper 15.01 +- 0.84. Uyum: 15.01 yalniz yuvarlanmis tohum degerlerinden cikiyor (maskelerden 15.00); SD 0.84 evet. Uc ve alt protokol orani 19.3648/4.3606 = 4.44 (paper "4.4-fold", evet).

`fig_protokol_kumeleri_veri.json` (kaynak_sha256 60268615...): ayrisim.yayilim 15.01; ozdeslik_terimi_ham_eksi_hedef_dogru 9.21; farkli_estimand_bas_kaynak_eksi_ham 5.79; artik_takdir_her_ikisi_eksi_hedef 3.91; tohum_basina_ortalama_yayilim 15.01; ic_icelik_tutuyor true. Protokol asimetri_ort ham/tc/bc/ss 13.57/4.36/8.27/19.37, asimetri_sd 0.33/0.44/0.23/1.27 (c1_transfer_summary.json'dan turetilmis, ayni degerler).

## Tablo B. Ozdeslik onculu
Kaynak: `results/q1/ozdeslik_kontrol.json`, betik `scripts/q1_ozdeslik_kontrol.py` (kaynaklar: `results/c1_c3/pair{1,2,3}` ve `results/q1/cifar100/transfer/pair{1,2,3}`, kosegen haric 6 yon x 3 tohum x 2 veri kumesi = 36); bagimsiz yeniden hesap `b2_recompute.py`.

| Nicelik | Yeniden hesap | ozdeslik_kontrol.json ozet | Paper (04_experiments.tex:143) | Uyum |
|---|---|---|---|---|
| yon sayisi | 36 | n_yon 36 | 36 | evet |
| p min | 0.989014 (CIFAR-100 pair3, ViT_Tiny_AT->ResNet18_AT; e=37.32, ham 49.28, kosullu 19.7352) | 0.989014 | 0.989 | evet |
| p max / ort. | 1.000000 / 0.997261 | 1.0 / 0.99726 | 1.000 | evet |
| artik (ham - tahmin) min / max | -0.4100 / 0.0000 | -0.41 / 0.0 | "within 0.41" | evet |
| ort. mutlak artik | 0.0947 | 0.09472 | 0.095 | evet |
| artik/sapma azami | %1.388 | 1.388 | 1.39% | evet |
| p'li bicim artigi | maks. mutlak 1.1e-14 | yok | e*p + r_cond*(1-e) | cebirsel esitlik |

Tum artiklar <= 0: ham oran, p=1 varsayimli tahminin altinda ya da esit. `c1_transfer` icindeki 6 yon (yalniz ResNet<->ViT): p min 0.994310, max 0.998456 (`b2_extra.py`).

Egim ve korelasyon, (ham - kosullu) ~ e (hedef temiz hata, puan):

| Veri | Yon-tohum n | Pearson r | Egim | Yon-ortalama n=6: r / egim / kesisim | Paper / kayit |
|---|---|---|---|---|---|
| CIFAR-10 (c1_c3) | 18 | 0.9970 | 0.7628 | 0.9971 / 0.7626 / 1.0861 | `c3_summary.json` raw_minus_cond_vs_target_error: pearson_r 0.99707, slope 0.76248, intercept 1.08917, n_offdiagonal 6; paper "0.762", "r = 0.997" (satir 145, 147) |
| CIFAR-100 | 18 | 0.9306 | 0.6570 | 0.9307 / 0.6565 / 3.4973 | paper "0.656" (satir 147); kayit dosyasi bulunmadi |

Her veri kumesinde yon-tohum satirlarinda iki ondalikta 7 ayri hedef-hata degeri var.

p<1 bolgesi ("p as low as 0.88" on standard-trained targets, pre-correction; paper satir 145): mevcut `c1_*` ve `q1/*` altinda standart egitimli hedef yok; bu deger yeniden uretilemedi.

## Tablo C. 3x3 matris ve r=0.986
Kaynak: `results/c1_c3/c3_summary.json`; per_sample maskeleri.

| Kaynak -> hedef | ham (yeniden hesap, ort.+-SD n-1) | kosullu | Paper tab:transfer_matrix | Uyum |
|---|---|---|---|---|
| R->R | 55.84+-0.53 | 48.52+-0.84 | 55.84 / 48.52 | evet |
| R->V | 41.07+-0.58 | 19.93+-0.20 | 41.07 / 19.93 | evet |
| R->W | 21.69+-0.09 | 12.49+-0.10 | 21.69 / 12.48 | kosullu 12.49 vs 12.48 |
| V->R | 27.45+-0.34 | 15.52+-0.64 | 27.45 / 15.52 | evet |
| V->V | 67.34+-0.18 | 55.57+-0.43 | 67.34 / 55.57+-0.44 | SD 0.43 vs 0.44 |
| V->W | 18.25+-0.12 | 8.65+-0.13 | 18.25 / 8.65+-0.14 | SD 0.13 vs 0.14 |
| W->R | 32.63+-0.14 | 21.48+-0.31 | 32.63 / 21.48 | evet |
| W->V | 39.73+-0.25 | 18.15+-0.28 | 39.73 / 18.15 | evet |
| W->W | 33.03 | 25.16 | 33.03 / 25.16 | evet |

(R = ResNet18_AT, V = ViT_Tiny_AT, W = WRN_28_10.) Gelen kosullu transfer (iki yabanci kaynagin ortalamasi): ResNet hedefi 18.5001, ViT hedefi 19.0406, WRN hedefi 10.5703; kosegen (beyaz kutu) kosullu: 48.5172, 55.5744, 25.1565. Pearson r = 0.9862 (maskelerden); paper'daki yuvarlanmis degerlerle de 0.9862; `c3_summary.json` incoming_transfer_vs_own_vulnerability pearson_r 0.98621. Uyum: evet (0.986). n = 3 hedef; paper metni "suggestive" diyor (satir 156).

Ek hesap (makalede yok): ayni 3 hedef icin gelen kosullu transfer ile hedef temiz hatasi (14.213, 26.473, 10.520) korelasyonu r = 0.7198.

Protokol tablosu ile 3x3 tablosu farki: ResNet->ViT ham 41.02+-0.55 (`c1_transfer`) ve 41.07+-0.58 (`c1_c3`); CNN->ViT kosullu 19.87 ve 19.93; ViT->ResNet kosullu 15.51+-0.59 ve 15.52+-0.64. `c1_c3`'ten ayni protokol asimetrileri: raw 13.6233, tc 4.4089, bc 8.3025 (`c1_transfer`: 13.5733, 4.3606, 8.2696). bc n ayni (7126/7067/6991), adv sonuclari farkli: iki ayri saldiri kosusu. Fig. 3 altyazisindaki "+4.4" (satir 177) iki kaynaktan da 4.4'e yuvarlanir.

## Tablo D. CIFAR-100
Kaynak: `results/q1/cifar100/transfer/pair{1,2,3}`; `e1_transfer_summary.json`.

| Protokol | Fark (tohumlar) | Ort. (maskelerden) | Summary diff.mean (SD) | Uyum |
|---|---|---|---|---|
| raw | 19.22, 18.58, 17.80 | 18.5333 | 18.5333 (0.7111) | evet |
| target_correct | 4.2108, 4.5436, 6.1159 | 4.9568 | 4.9567 (1.0132; maskeler 1.0176) | evet |
| both_correct | 11.1522, 10.529, 11.0886 | 10.9233 | 10.9233 (0.342) | evet |
| successful_source | 16.842, 17.1115, 18.5499 | 17.5011 | 17.50 (0.9193) | evet |

Yayilim: protokol ortalamalarinin max-min = 13.5765 (paper 13.58, evet); tohum basina 15.0092, 14.0364, 12.4340, ort. 13.8265 (summary protocol_spread_pp [15.01, 14.03, 12.44], ort. 13.8267; paper 13.83, evet). Artik bc - tc = 5.9665 (paper 5.97, evet). Ham en buyuk protokol (18.53 > ss 17.50); ss - raw = -1.0322, yani ss, raw - tc araliginin icinde (paper'in "falls inside it" ifadesiyle tutarli). raw - tc = 13.5765 = yayilim.

## Tablo E. SVHN
Kaynak: `results/q1/svhn/transfer/pair{1,2}`; `e7_transfer_summary.json`; iki tohum.

| Protokol | Tohum farklari | Ort. (maskelerden) | Summary diff.mean (SD) | Paper tab:svhn_protocols | Uyum |
|---|---|---|---|---|---|
| raw | +0.3304, +0.4571 | +0.3937 | 0.39 (0.0849) | +0.39+-0.08 | evet |
| target_correct | -1.1624, -0.8555 | -1.0090 | -1.005 (0.2192) | -1.00+-0.22 | yuvarlama: -1.01 / -1.005 / -1.00 |
| both_correct | -0.3393, -0.3565 | -0.3479 | -0.35 (0.0141) | -0.35+-0.01 | evet |
| successful_source | +2.9760, +2.4054 | +2.6907 | 2.695 (0.4031) | +2.70+-0.40 | yuvarlama: 2.69 / 2.695 / 2.70 |

Isaretler: raw +, tc -, bc -, ss +; iki protokol CNN, iki protokol ViT avantaji bildirir (paper satir 240), yeniden uretildi. Yayilim: protokol ortalamalarinin max-min = 3.6996 (summary protocol_spread_pp 3.70; tohum 4.1384, 3.2609). Artik bc - tc: maskelerden 0.6611; summary'den -0.35 - (-1.005) = 0.655; paper tablosundan 0.65 (metinde 0.65). Hedef temiz hatalari: pair1 ResNet 5.244, ViT 7.176; pair2 ResNet 6.227, ViT 7.967; ViT - ResNet ortalama 1.936 (paper "about two points"). SVHN yonlerinin p degerleri 0.9976-0.9994; bu 4 yon 36'ya dahil degil (`ozdeslik_kontrol.json` yalniz c1_c3 + cifar100 kullanir). Summary'den okunanlar (yeniden hesaplanmadi): perm_p_max 0.1047 (paper 0.105), tost_equivalent_any true, ci_low/ci_high tohum degerleri -0.75/-0.76 ve 0.07/0.06 (ort. -0.755, 0.065; paper [-0.76, +0.07]).

## Tablo F. Diger bagli sayilar

| Nicelik | Yeniden hesap | Paper | Uyum |
|---|---|---|---|
| Gevsek ss asimetrisi (tc & source_adv_wrong, kaynak temiz-dogru sarti yok) | tohum 16.1362, 14.4613, 13.1883; ort. 14.5953 | +14.60 (satir 119) | evet |
| Gevsek durumda yayilim (tohum basina ort.) | 11.3141, 10.1740, 9.8575; ort. 10.4485 | 10.45 | evet |
| Katilastirma kaymasi 19.37 - 14.60 | 4.77 | 4.77 | evet (paper degerleriyle; maskelerle 19.3648 - 14.5953 = 4.7695) |
| L2 asimetriler raw / tc / bc / ss (`results/q1/cifar10_l2/transfer`) | 13.0267 / 2.1206 / 4.0659 / 12.0529 | +13.03 / +2.12 / +4.07 / +12.06 | ss: 12.05 vs 12.06 (HAYIR) |
| L2 yayilim (tohum basina ort.) | 10.9157 (ortalamalarin max-min 10.9061) | 10.92 | evet |
| L2 SD'ler (n-1) raw / tc / bc / ss | 0.8100 / 0.1813 / 0.3593 / 0.2327 | 0.81 / 0.18 / 0.36 / 0.23 | evet |

L2 icin `e6_l2_transfer_summary.json` bu gorevde okunmadi; ss 12.06 ile 12.05 farkinin kaynagi (yuvarlanmis tohum degerleri) dogrulanmadi.

## Tablo G. Yeniden uretilemeyenler ve nedenleri

| Nicelik | Durum | Neden |
|---|---|---|
| ss asimetrisi 19.37 | maskelerden 19.36 | ozet JSON yuvarlanmis tohum farklarinin ortalamasini aliyor |
| tam yayilim 15.01 | maskelerden 15.00 (15.0042) | ayni neden; paper metni 15.00 toplamini kendisi aciklar |
| SD tc 0.44, ss 1.27 | 0.43, 1.26 | yuvarlanmis tohum degerleri uzerinden SD |
| c1_c3'te successful-source | uretilemez | npz'lerde source_adv_wrong yok (yalniz 3 anahtar) |
| p = 0.88 (standart egitimli hedef) | uretilmedi | mevcut c1_*/q1/* altinda standart egitimli hedef yok |
| CIFAR-100 egimi 0.656 icin kayit | bulunmadi (hesap 0.6565-0.6570) | `c3_summary.json` yalniz CIFAR-10 |
| +0.914 egimi (L2) | hesaplanmadi | kapsam disi; yalniz `scripts/_stat_kalan2.py:44`, `_t3_en_cerceve.py:112` icinde geciyor |
| Bootstrap GA, TOST, permutasyon p | yeniden hesaplanmadi | kapsam disi; summary JSON'dan okundu (CIFAR-10 bc: ci_low/ci_high ort. 7.33/9.22, perm_p_max 0.0, tost_equivalent_any false) |

## Kaynak izi
- Ozdeslik tanimi: `paper/manuscript/sections/04_experiments.tex:134-141` (etiket eq:raw_identity); genel bicim satir 145.
- Tablolar: tab:transfer_protocols satir 89-104; tab:transfer_matrix satir 152; tab:svhn_protocols satir 225.
- Karantina dizinlerine (run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA) basvurulmadi.
