# Tur 4 — ic hakemlik hukmu ve birlesik eylem plani (2026-08-29)

> ## ILERLEME (son guncelleme: 2026-08-29, commit d747060)
>
> **BITTI — Faz 0 (commit 1170366):**
> - 0.1 Denklem (1) cebiri `e(1-p)` -> `e*p`, artı ust-sinir cumlesi
> - 0.2 Manset ayrisimi: `15,01 = 9,21` (ozdeslik) `+ 5,79` (farkli estimand);
>   `3,91` = duzeltme SONRASI artik. CIFAR-100'de iki-parcali bolumleme
>   GECERLI DEGIL (kosulsuz oran dordun en buyugu); metin bunu soyluyor.
> - 0.3 Tek "birincil": Bolum 3 bir metrik AILESI tanitiyor, birincil tahmin
>   = her-ikisi-dogru, tek yerde ilan ediliyor
> - 0.4 `fig:feature_degradation` oksuzlugu giderildi (tur 3 regresyonu)
> - 1.4 `p=0,88` nitelendi · 1.5 YZ beyani eklendi (EN+TR)
> - YAPISAL MUHAFIZ + sinamasi: `scripts/test_cebir_muhafizi.sh`
>
> **BITTI — Faz 2A (commit d747060):**
> - 1.2 ViT derinlik profili DOGRU TENSORDE yeniden olculdu (artik blok
>   cikisi). CLS min blok 11 @ 0,9604 · yama-ort blok 9 @ 0,9870 ·
>   oran 3,05 kat · norm %0,45. Tablo VII blok cikisina cevrildi, artik
>   CNN sutunuyla DENK noktada. MLP serisi metinde duyarlilik olarak duruyor.
>   Eski artefaktlar: `results/c1_c4_t4oncesi/`
> - 2.1 Kol karsilastirmasi ON KAYITLI havuza tasindi. Olculdu: o havuzda
>   B araligi A'yi KAPSIYOR -> "uyusmuyorlar" hukmu geri cekildi; uc
>   protokollu uyusma her havuzda gecerli.
>
> **KAPILAR:** yedi kapi da geciyor. Sayi kapisi 152 -> 158 kontrol.
> EN 21 sayfa, TR 21 sayfa, 0 tanimsiz gonderme, 0 Overfull.
>
> **GPU:** hicbir kosum calismiyor. Yeniden kosum gerektiren is KALMADI.
>
> ### SIRADAKI — "DEVAM" burada baslar (hicbiri GPU gerektirmez)
> - **2.2** Birim politikasi CIFAR-100/SVHN bolumlerine tasinmali; SVHN
>   esdegerlik raporlamasindaki kaymalar iddia lehine
> - **2.3** On kayit beyanlari kayittan guclu (epok-7 gercegi, E2 null'u)
> - **2.4** Prior-art: "kanonik kaynak yok" iddiasi `ravikumar2023trend`
>   (TM = f_st/f_ss) ile curutulebilir; 02:74 "olculmemistir" kendi Yu
>   cumlesiyle celisik
> - **2.5** Zincir celiskileri (giris yon cumlesi, ozet SVHN, sonuc "survived")
> - **2.6** Gonderim mekanigi: `access.cls`, ATEEC kapsam beyani, pakette
>   geri cekilmis egimin sekli, eski `paper/cover_letter.txt`
> - **Faz 3** kapi/altyapi · **1.3** TGR sapma beyani · **1.7** anonim arsiv
> - **BEKLEYEN KULLANICI BILGISI:** fon (kurum adi + hibe/proje numarasi)

**Kurulum:** 3 Fable hakim × 10 Opus duzenleyici × 3 Sonnet toplayici = **123 ajan**,
0 hata, 9,1M token, ~55 dk. Sonnetler yalniz kanit topladi; Opuslar dogrulayip
bulguya cevirdi; hukmu Fable'lar verdi.

**Hukum: UCU DE `major_revizyon`.** Ucu de ayni bulguyu bir numaraya koydu.

| alan | hukum | engelleyici | ikincil | **reddedilen** |
|---|---|---|---|---|
| A — bilimsel gecerlilik | major | 7 | 10 | 12 |
| B — konumlandirma | major | 6 | 9 | 14 |
| C — sunum ve teslim | major | 8 | 9 | 10 |

36 iddia REDDEDILDI (n=3'te uygulanamaz prosedurler, dogrulanamayan alintilar,
yeni GPU kosumu talepleri, sayfa-asimi ucreti efsanesi). Panel disiplinli calisti.

**Onemli:** Hicbir duzeltme yeni GPU kosumu gerektirmiyor (TGR karari haric,
o da opsiyonel). Is tamami metin + artefakt + kapi duzeyinde.

---

## Dogrulama durumu isaretleri

- ✅ **Ben bagimsiz dogruladim** (betikle, bu oturumda)
- ◐ Panel birinci elden dogruladigini bildiriyor; ben yeniden dogrulamadim
- ? Uygulamadan once dogrulanmali

---

## FAZ 0 — Dogrulanmis kritik duzeltmeler (yazar karari gerekmez)

### 0.1 ✅ Denklem (1)'in genel bicimi cebirsel olarak YANLIS

`04_experiments.tex:133` (ve TR aynasi):

```
BASILI : r_ham = e(1-p) + r_kos(1-e)      <-- YANLIS
DOGRU  : r_ham = e·p    + r_kos(1-e)
```

`p = P(adv yanlis | temiz yanlis)` oldugu icin toplam olasilik yasasi
`e·p + r_kos(1-e)` verir. **Bagimsiz olcum** (`scripts/_t4_ozdeslik_dogrula.py`,
6 yon, ornek bazinda):

| bicim | hata |
|---|---|
| dogru | **0,0000 puan** (6/6 yon) |
| basili | **26,99 puana kadar** |

Ustelik makalenin kendi cumlesi — *"$p=1$'de Denklem (1)'e indirgenir"* —
basili bicim icin yanlis: $p=1$'de $r_{kos}(1-e)$ verir.

**Eylem:** formulu duzelt; artigin kapali formda $-e(1-p)$ oldugunu ve
ozdesligin $p\le1$'de **ust sinir** oldugunu iki cumleyle yaz. Iki dil.

> Bu hata C1 duzeltmesinden beri metindeydi ve uc hakem turunu gecti.
> Sayi kapisi CEBIRI denetlemiyor — bu yuzden 152 kontrol yakalayamadi.

### 0.2 ✅ Manset ayristirmasi yanlis acikligi ozdeslige atfediyor

Denklem (1) `r_kos`'u **hedef-dogru** oran olarak tanimliyor (03:100).
Dolayisiyla ozdesligin kapali formda kapattigi aciklik:

```
ham <-> hedef-dogru = 13,573 - 4,360 = 9,21 puan
```

Benim tur 3'te yazdigim *"her-ikisi-dogru <-> ham = 5,31 puani Denklem (1)
duzeltir"* **yanlis**. 5,31, 9,21'lik aralığın icinde kalan bir parcadir;
3,91 de oyle. Ucu bagimsiz bilesen degil.

**Dogru cerceve (ham eksen noktasi):**

```
15,01 = 9,21 (ham <-> hedef-dogru; Denklem (1) TAM kaldirir)
      + 5,79 (ham <-> basarili-kaynak; farkli estimand)
```

ve **3,91**, duzeltme SONRASI onayladigimiz iki protokol (hedef-dogru vs
her-ikisi-dogru) arasinda KALAN takdirdir — ayri bir bilesen degil, artik.

**Eylem:** 8 yerde es zamanli (EN+TR ozet, 01:23, 02:74, 04:105, 06:9).
Tez ayakta kalir; 3,91 hala yeniden egitmenin iki katindan fazla.

### 0.3 ✅ Iki farkli protokol "birincil" ilan edilmis

- `03:100` — *"Our **primary** transfer metric is the conditioned fooling rate"*
  (= hedef-dogru, Denklem 2)
- `04:228` / `05:19` — her-ikisi-dogru *"which we treat as **primary**"*

**Eylem:** 03:100'de kosullu yaniltma oranini **metrik ailesi** olarak tanit,
"birincil" sifatini kaldir; birincil TAHMIN = her-ikisi-dogru (esli cikarim
gerekcesiyle) tek yerde beyan edilsin. Iki dil.

### 0.4 ✅ `fig:feature_degradation` oksuz kaldi (benim regresyonum)

Sayfa kısaltmasında bu sekle giden **tek** isaret cumlesini sildim; sekil
artik metinde hic anilmiyor (`scripts/_t3_sekil_denetim.py` ile teyit).

**Eylem:** entropi sekline bir atif cumlesi geri koy (kaldirdigim tekrar
degil, yeni ve kisa bir cumle). Iki dil.

---

## FAZ 1 — Yazar karari gerektirenler

| # | karar | secenekler | panelin egilimi |
|---|---|---|---|
| 1.1 | **Ayrisim sunumu** | (a) iki-parcali 9,21 + 5,79 cercevesi · (b) uc-protokollu ayrisim (manseti 9,21'e kucultur) | (a) — B10 (b)'yi "teknik olarak daha saglam ama YAZAR tercihi" diyor |
| 1.2 | **ViT katman profili** ◐ | (a) `cos_block_output` serisini Tablo VII'ye ekle, derinlik anlatisini yeniden yaz · (b) MLP alt-blok etiketini acikca yaz, "siniflandiricinin okudugu" yorumunu geri cek | ikisi de kabul; (b) daha ucuz |
| 1.3 | **TGR** ◐ | (a) yayimlanmis katsayilarla (0,25/0,75/0,5) 3 cifti yeniden kos · (b) sapmayi acikca beyan et | (b) asgari yukumluluk; (a) tercih |
| 1.4 | **$p=0{,}88$** ◐ | (a) yeniden olc · (b) "C1-oncesi, mertebe gostergesi" diye niteleyip kapiya bagla | (b) |
| 1.5 | **YZ kullanim beyani** | IEEE zorunlulugu; hicbir belgede yok | taslak Claude, karar kullanici |
| 1.6 | **Fon beyani** | `declarations.txt`'te placeholder | kullanici |
| 1.7 | **Anonim inceleme arsivi** | results/ 449MB + bolme indeksleri → Zenodo / Anonymous-GitHub? | kullanici |

---

## FAZ 2 — Panel bulgulari (uygulamadan once dogrula) ◐

### 2.1 Kol karsilastirmasi geri cekilen havuza dayali (A, engelleyici 2)

`04:111` SVHN'li havuzu **on kayitli** ilan edip dort protokollu egimi geri
cekiyor; `04:115` kol karsilastirmasini SVHN'**siz** havuzdan kuruyor.
Panel: on kayitli havuzda B kolunun GA'si `[-0,570; +0,469]` A kolunun
`[+0,219; +0,371]`'ini **tamamen kapsiyor** → *"uyusmuyorlar"* hukmu o
havuzda yanlis. Ayrica A kolunda havuzlanmis OLS `+0,273` ile kume-ici
`+0,609` ayrik.

> Uc protokollu egim her kurulumda saglam (+0,673 / +0,707 / +0,470) —
> **mekanizma iddiasi ayakta.**

**Dogrulama yolu:** `results/q1/e3_iki_kol_fit.json` +
`e3_asimetri_fit_svhnli.json` uzerinde GA ortusmesini yeniden hesapla.

### 2.2 Birim politikasi ilan edilip uygulanmamis (A, engelleyici 5)

Tur 3'te Bolum 3'e yazdigim politika CIFAR-100 ve SVHN bolumlerine
tasinmamis; SVHN esdegerlik raporlamasindaki kaymalarin **tumu iddia
lehine**. Ayrica CIFAR-100/SVHN'deki "bootstrap GA" ifadeleri 04:105'teki
uc-uc-ortalamasi serhini tasimiyor.

### 2.3 On kayit beyanlari kayittan guclu (A, engelleyici 6)

Panel birinci elden: uc ongorunun **ikisi kosum sirasinda, epok 7'de**
yazilmis. Ayrica E2 null'u, manipulasyon kontrolunun coktugu soylenmeden
raporlaniyor.

**Dogrulama yolu:** `git log --diff-filter=A` ve `git log -p` ile on kayit
dosyalarinin tarihleri vs sonuc artefakt tarihleri.

### 2.4 Prior-art konumlandirmasi kendi kaynakcasiyla curutulebilir (B)

*"Basarili-kaynak icin kanonik kaynak yok"* — panel `ravikumar2023trend`'de
`TM = f_st/f_ss` tam esdegerini buldugunu bildiriyor. Ayrica `02:74`'teki
*"olculmemistir"* iddiasi kendi Yu cumlesiyle celisiyor.

### 2.5 Zincir-govde celiskileri (C, engelleyici 3)

Giris kendi icinde *"yon kararli / degil"*; ozet SVHN cumlesi govdeyi
asiyor; Sonuc *"survived"* diyor.

### 2.6 Gonderim mekanigi (B+C)

- `access.cls` sablonu yok — makale **dogru sinifta olculmemis**
- ATEEC bildirisinin kapsami iki belgede yanlis beyan ediliyor
- Gonderim paketinde geri cekilmis egimin sekli duruyor
- Eski `paper/cover_letter.txt` curutulmus sonuc tasiyor

---

## FAZ 3 — Kapi ve altyapi

| # | is |
|---|---|
| 3.1 | **Yapisal muhafiz**: kapiya `e\,p` VAR / `e\,(1-p)` YOK kontrolu (bu hata sinifi bir daha gecmesin) |
| 3.2 | Altkume McNemar $10^{-67}$'yi `build_reference_sheet.py`'ye ekle (karantina kuralinin lafzi: her sayi foyden) |
| 3.3 | `_svhn_havuz_olc.py`'ye JSON cikti; `results/q1/e3_onkayitli_havuz_fit.json` |
| 3.4 | Kapiya ~15 yeni `chk`: kosum p'leri, SVHN TOST/perm, +0,470+GA, TOST 0,006, paydalar |
| 3.5 | Kullanilmayan 12 PDF'i `paper/figures/arsiv/`e tasi; `teslim_paketi.sh`'i tex'te cagrilanlardan uret |
| 3.6 | Depo koku karantina bantlari; root:root uc dosyanin izni (**sudo — kullanici**) |

---

## Sira (bagimliliklarla)

```
0.1 ──> 0.2 ──> (1.1 karari) ──> 8 yerde metin
 │
 ├─> 0.3, 0.4  (bagimsiz, hemen)
 │
 ├─> 2.1, 2.2, 2.3  (dogrulama sonrasi metin)
 │
 ├─> 1.2/1.3/1.4 kararlari ──> ilgili metin+kod
 │
 └─> 3.1..3.4 (kapilar) ──> FAZ 2 metni bitince
                              │
      1.5/1.6/1.7 (kullanici, paralel) ──┴─> 2.6 gonderim ──> kapanis
```

**Kapanis:** `bash scripts/kapilar.sh` · `verify_manuscript_numbers.py`
(152 + yeni) · EN/TR ayna · karantina grep · `teslim_paketi.sh` ·
`access.cls`'te sayfa olcumu · `git push origin q1` · iThenticate.

**Tahmini:** 2–4 gun (panelin ortak tahmini), yeni GPU kosumu olmadan.
