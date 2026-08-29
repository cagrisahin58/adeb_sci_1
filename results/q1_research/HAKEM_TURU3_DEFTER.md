# Hakem turu 3 — dogrulanmis bulgu defteri (2026-08-29)

Bes `sci-peer-reviewer` (istatistik, iddia-kanit, ozgunluk, sunum, kirmizi
takim) bagimsiz kostu. **Hicbir bulgu dogrulanmadan uygulanmadi** — onceki
turda alti iddiadan dordu curumustu. Asagida her satir, kendi olcum
betigiyle birlikte.

---

## A. CERCEVE — yeniden yazim gerektirenler

### A1. Manset 15,01 karisik bir nicelik  ✅ DOGRULANDI (aritmetik)

15,01 puanlik "protokol yayilimi" uc ayri seyin toplamidir:

| bilesen | deger | ne |
|---|---|---|
| ham − hedef-dogru | **9,21** | Denklem (1) ozdesligi — KAPALI FORMDA duzeltilebilir |
| basarili-kaynak − ham | **5,79** | farkli bir estimand (kaynagin kendi gurbuzlugu) |
| **hedef-dogru ↔ her-ikisi-dogru** | **3,91** | makalenin ONAYLADIGI iki protokol arasi GERCEK takdir |

Ayni ayristirma: CIFAR-100 **5,97** · SVHN **0,65**.
Kaynak: 04_experiments.tex:120 ve :207 ve :245'teki kendi sayilari.
(13,57−4,36=9,21 · 19,37−13,57=5,79 · 8,27−4,36=3,91)

**Sonuc:** "15 puana karsi 1 puan" manseti oldugu gibi kalamaz. Kalan
bulgu hala guclu — ama ayristirilmis haliyle.

### A2. Ozdeslik TRADES Denklem (1)'in cebirsel esi  ✅ DOGRULANDI

`r_raw = e + r_cond(1−e)` ≡ `R_rob = R_nat + R_bdy`.
`zhang2019theoretically` kaynakcada VAR (02:28, 03:71) ama yalniz bir
savunma yontemi olarak aniliyor. Gercek ozgunluk: TRADES'te ∃-niceleyici
`p=1`'i TANIM GEREGI verir; biz oncul `p ∈ [0,989, 1,000]`'i transfer
rejiminde OLCTUK. Bu soylenmeli.

### A3. Yu ve ark. yanlis nitelendirilmis  ✅ DOGRULANDI (kaynak okundu)

02:62 "Both hold the scoring rule fixed and vary the attack and the model
pool." Yu ve ark.'nin uc protokolu: topluluk-tek-hedef / kandirilan-hedef
sayisi / tum-hedefler-kandirildi. Bunlar **puanlama kuralinin kendisini**
degistiriyor, hedef toplulastirma ekseninde. Cumle TA-Bench icin dogru,
Yu icin YANLIS.

### A4. SVHN provenansi yanlis  ✅ DOGRULANDI (git zaman damgalari)

04:126: "The pool for this fit is the one fixed in the pre-registration,
which assigns the SVHN pair to an independent consistency check."

- `E3_YENIDEN_TASARIM.md:115` SVHN'i **B (uydurulan) koluna** koyuyor
- `:242` SVHN'i x-ekseninin **<%12 bosugunu kapatmaya** atiyor
- on kayit `7a3e5af` 08-19 23:57 · SVHN sonucu `8c01e47` 08-21 09:27 ·
  "bagimsiz tutarlilik kontrolu" atamasi `7148fd9` 08-21 09:55
  → **sonuctan 28 dakika SONRA**

Duyarlilik ZATEN raporlanmis (04:126 sonu), yalniz PROVENANS cumlesi
yanlis. Olculen etki:

| havuz | dort protokol | uc protokol |
|---|---|---|
| SVHN disarida (post-hoc) | −0,528 [−0,664, −0,418] | +0,431 [+0,333, +0,633] |
| SVHN dahil (**on kayitli**) | −0,133 [−0,570, **+0,469**] | +0,470 [+0,361, +0,665] |

→ **Mekanizma iddiasinin dayandigi uc-protokollu egim AYAKTA.**
Betik: `scripts/_svhn_havuz_olc.py`

### A5. Cikarim birimi iddia basina degisiyor, her seferinde iddiayi kayiriyor  ✅

| iddia | kullanilan birim | yon |
|---|---|---|
| transfer asimetrisi | ornek | iddiayi buyutur |
| mekansal null | kosum | null'u korur |
| gradyan seyrekligi | ornek | iddiayi kurtarir |
| dikkat null'i | kosum (TOST) | null'u korur |

Tablo VIII'in KENDI basligi "Inference is at the run level ... so that the
unit of inference matches the unit of the claim" diyor.

---

## B. ISTATISTIK

### B1. [S3] Seyreklik iddiasi kosum duzeyinde DUSUYOR  ✅ DOGRULANDI

`scripts/_s3_kosum_duzeyi.py` (bagimsiz yeniden hesap):

| olcut | ResNet | ViT | ham p | Holm(3) |
|---|---|---|---|---|
| Gini | 0,6491 / 0,6590 / 0,6412 | 0,6136 / 0,6040 / 0,6121 | 0,0359 | **0,108** |
| Frac<%1 | 0,3451 / 0,3699 / 0,3282 | 0,2743 / 0,2578 / 0,2725 | 0,0420 | **0,108** |
| Hoyer | 0,4907 / 0,5058 / 0,4821 | 0,4587 / 0,4498 / 0,4599 | 0,0674 | **0,108** |
| Hizalanma (ayri aile) | 0,0377 / 0,0370 / 0,0388 | 0,0557 / 0,0564 / 0,0565 | **0,0009** | anlamli |

IUT (max-p) = 0,0674. Makale `p<10^-11` (ornek duzeyi) diyor.
**Hizalanma iddiasi ayakta, seyreklik iddiasi beyan edilen birimde degil.**

### B2. [S1] "Paired bootstrap GA" tanimli bir yordam degil  ✅ DOGRULANDI

`c1_transfer_summary.json`:
`ci_low.values = [7.61, 7.10, 7.28]` → ort **7,33**
`ci_high.values = [9.44, 9.01, 9.20]` → ort **9,22**

Makaledeki `[7,33, 9,22]` **uc ayri GA'nin uclarinin aritmetik
ortalamasi**. Kapsama garantisi yok. (Tohumlar arasi t-tabanli GA
olsaydi: 8,27 ± 4,303×0,2364/√3 = **[7,68, 8,86]**.)

### B3. [S2] TOST yonu ters  ✅ DOGRULANDI

04:120 "TOST equivalence **rejected** at all three margins (p=1,0 in
each)". TOST'ta buyuk p = **esdegerlik KURULAMADI**; TOST esdegerligi
reddedemez. Ayni makale 04:243'te DOGRU kullaniyor (p=0,0007 → kabul).
Artefakt da dogru kaydediyor: `tost_equivalent_any = False`.
Esas sonuc dogru (GA [7,33; 9,22] ±3'u disliyor) — mantik ifadesi yanlis.

### B4. [S5] TOST marji ±2 yanlis nicelikten turetilmis  ✅ DOGRULANDI

03:144: marj "run-to-run variation in PGD accuracy" ilkesiyle sabitlenmis,
ama **transfer asimetrisine** uygulaniyor. Asimetrinin kosum-arasi SS'si
**0,23** puan — ±2 bunun ~8,6 kati. Bu, makalenin 04:462'de kendi
mahkum ettigi olcek hatasi. (±1 ve ±3 duyarliligi raporlandigi icin
sonuclar ayakta; GEREKCE yanlis.)

### B5. [S6] A kolu GA'si kendi kaldirac araligini kapsamiyor  ✅ DOGRULANDI

`e3_iki_kol_fit.json`: A_GA = **[0,219, 0,371]**
kaldirac duyarliligi: ep≥2 **0,201** · ep≥10 **0,483** · ep≥20 **0,492**
→ ucu de GA'nin DISINDA. 04:130 "survives" diyor; **isaret** hayatta
kaliyor, **buyukluk** kalmiyor. (Aralik zaten aciklanmis, sozcuk yanlis.)

### B6. [S8] L2'nin ucuncu ongorusu yanlislanabilir degil  ✅ DOGRULANDI

Sapma = `e(1−r_cond)`; `e` ile artmasi Denklem (1)'in kendisinden turer.
Egim `+0,914` zaten `1−r̄_cond`. 04:272 bunu "All three registered
predictions hold" diye sayiyor; 04:209 AYNI ongoruyu CIFAR-100'de
DOGRU sekilde "consistent with ... does not test it" diye indiriyor.
Ayni ongoru, iki farkli muamele.

### B7. [S7] A kolu SVHN ICERIYOR, metin ikisini de haric ima ediyor  ✅

A: 116 nokta / **8 kume** · B: 18 nokta / 6 kume · B+SVHN: 20 / 8.
Aciklama kusuru; sonuc kusuru degil (isaretler degismiyor).

---

## C. OLGUSAL HATALAR (hepsi dogrulandi)

| # | yer | hata | dogru |
|---|---|---|---|
| C1 | 01:27 | "four spatial measures of which **three** are null" | 04:336 "**None of the four**" → dordu de null |
| C2 | 04:64 | her-ikisi-dogru McNemar `p<10^-84` | **tam kumeden odunc**; gercek altkume max p = 5,9e-68 → `p<10^-67` |
| C3 | 04:415 | "Figure~\ref{fig:feature_degradation} shows ... CLS attention **for a representative sample** together with entropy curves" | o sekil YALNIZ entropi egrileri; haritalar `fig:attention_layers`'ta (kendi basligi da oyle diyor) |
| C4 | 05:31 | CLS "drifts **three** times as far" | 04:393 "**four** times ... ratio of 4,1" |
| C5 | 05:21 | "two attack families ... **on both CIFAR datasets**" | MI-FGSM yalniz CIFAR-10 |
| C6 | 04:124 | MI-FGSM 15,42 | `c1_addenda` α=**ε/10**; §4.9 tablosu `c1_c2` α=**2/255** (15,71). Ayni ad, iki butce. §3 "butce boyunca 2/255" diyor. CNN→ViT yonu yalniz ε/10 kosumunda var → butce ACIKCA yazilmali |
| C7 | 04:41 | "at most **0,80 points** on any reported accuracy" | en buyuk dogruluk SS'si **0,55** (ViT temiz); 0,80 bir KOSULLU KANDIRMA ORANI |
| C8 | 05:21 | "rather than **11** or 21" | CIFAR-10 aciklik 85,78−73,53 = **12,3** |
| C9 | 03:104 | "two **established** alternatives" | basarili-kaynak icin ATIF YOK (her-ikisi-dogru icin var) |
| C10 | ozet EN | 264 kelime | IEEE Access siniri **250** |
| C11 | 04:336 | "Neighbourhood" | ABD imlasi: neighborhood |
| C12 | 04:245 | "behaviour" | behavior |
| C13 | 04:209 | "the first being" | AI kalintisi |

---

## D. HAKEMLERIN KENDI CURUTTUKLERI (uygulanmayacak)

- payda artefakti — B2 duzeltmesiyle olmus
- on kayitlar gercekten once yazilmis, salt-eklemeli — git dogruladi
- tanim degisikligi sonuc-kovalama degil
- A kolundan SVHN cikarilinca sonuc degismiyor (+0,318 / +0,617)
- **her-ikisi-dogru n ve puan farklari GERCEK**: n=7061±68, PGD 13,76,
  AA 10,73 — hepsi altkumeden hesaplandi ve makaledeki degerlerle
  birebir tutuyor (yalniz p siniri odunc; bkz. C2)

Betikler: `scripts/_bc_mcnemar.py`, `_bc_mcnemar_aa.py`,
`_s3_kosum_duzeyi.py`, `_svhn_havuz_olc.py`, `_stat_kalanlar.py`,
`_stat_kalan2.py`
