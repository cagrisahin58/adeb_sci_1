# E2 Sızıntı Ablasyonu — Sonuç ve Çürütme Denetimi

**Durum:** kampanya tamam (18/18 hücre, 6 tam-bütçe yörünge), ön-kayıtlı
analiz koşuldu, sonuç 4 mercek + 3 şüpheci hakemden oluşan bir çürütme
denetiminden geçirildi (2026-08-16/17).

**Tek cümlelik hüküm:** Sızıntının checkpoint seçimine etkisi **saptanamadı**
(ve ViT kolunda tedavi zaten teslim edilememiştir); buna karşılık **seçim
protokolünün kendisi** sabit bir yörüngede raporlanan PGD-10 doğruluğunu
ResNet-18'de **2,62-2,85**, ViT-Tiny'de **1,58-2,09 puan** aralığında
oynatmaktadır. Bu yayılımın eğitim-tohumu yayılımına ORANI ise tanıma ve
referans seçimine duyarlıdır (§3'e bakınız) ve **manşet olarak
kullanılmayacaktır**; manşet mutlak yayılım ve bölme-bootstrap dağılımıdır.

> **İKİ KEZ DÜZELTİLDİ.**
> **(1) 2026-08-17 sabah:** ilk sürüm manşeti "1,67 / 0,82 puana kadar" diye
> kurmuştu — bunlar n=3'ün **maksimumuydu** (diğer çekilişler 0,00 ve
> 0,00/−0,32) ve "tohum yayılımının üç katı" ifadesi maksimumu standart
> sapmaya bölüyordu (eşli oranda ResNet'te 0,77×, yani tersine dönüyordu).
> **(2) 2026-08-17 öğle (R3 denetimi):** yerine konan "1,54× / 2,17×" oranı da
> **tek bir keyfi referans protokolüne** dayanıyordu. 18 referansın tamamı
> tarandığında oran ResNet'te **0,67-3,38×** (medyan 1,40; 2/18 referansta
> ≤1), ViT'te **0,63-7,38×** (medyan 1,36; 3/18 ≤1); ayna referansla (V_C
> yerine V_B) ViT iddiası **0,63×'e tersine dönüyor**. Ayrıca yayılımın
> baskın kaldıracı **eğri yumuşatmasıdır** ve yumuşatma nötr bir alternatif
> değil **monoton olarak daha kötü** bir seçicidir; pratikte değiştirilen
> boyutlarla sınırlanınca (bölme × patience, k=1) oran **1,09× (ResNet) /
> 1,42× (ViT)**'e iniyor. Bu yüzden oran manşetten çıkarıldı, duyarlılık
> aralığıyla birlikte §3'te raporlanıyor.

---

## 1. Ham sonuçlar (ön-kayıtlı analiz, `e2_report.json`)

| Kol | Seçilen epok A/B/C | Δ_AB (sızıntı) | Δ_BC (gürültü tabanı) |
|---|---|---|---|
| ResNet s1001 | 63 / 63 / 32 | 0,00 | +0,82 |
| ResNet s1002 | 49 / 49 / 49 | 0,00 | 0,00 |
| ResNet s1003 | 45 / 44 / 60 | +0,30 | −0,32 |
| **ResNet ort.** | | **+0,100 ± 0,173** | **+0,167 ± 0,588** |
| ViT s2001 | 19 / 28 / 18 | −1,04 | +1,67 |
| ViT s2002 | 18 / 20 / 20 | −1,06 | 0,00 |
| ViT s2003 | 36 / 28 / 28 | −1,05 | 0,00 |
| **ViT ort.** | | **−1,050 ± 0,010** | **+0,557 ± 0,964** |

## 2. Çürütme denetiminin hükmü: atıf düzeyinde ARTEFAKT

**Gerçek olan:** e_A ve e_B farklı checkpoint'lerdir ve aralarında ~1,1 puanlık
gerçek bir kalite farkı vardır (bağımsız tahminciler birleşimi θ = −1,108 ±
0,183; homojenlik χ²(5)=7,23, p=0,204). Veri bütünlüğü 18/18 temiz.

**Artefakt olan:** bu farkın **sızıntıya atfedilmesi**.

> **DÜZELTME (2026-08-17, `q1_e2_audit.py` ile yeniden üretim denemesi):**
> Bu belgenin ilk sürümü "dürüst iki yönlü p = 0,10–0,19 (dört bağımsız
> kuruluş)" diyordu. Denetim betiği **dokuz** null kuruluşu hesapladı ve
> yalnız **biri** (simetrik tahminci üzerinde n=3 parametrik t, p=0,113) bu
> aralığa düşüyor. Sayılar **iki çıkarım çerçevesine** ayrılıyor:
> - **Bölmeler rastgele (değiştirilebilir) kabul edilirse:** tasarımla
>   eşleşmiş null'lar (ortak-bölme yapısı korunmuş, ayrık değerlendirici,
>   gerçek 10k test) **p = 0,0074 – 0,052** veriyor — yani bu çerçevede etki
>   sınırda anlamlı.
> - **Bölme kimliği sabit kabul edilirse:** tam permütasyon tabanı 1/6–1/3;
>   **p = 0,25 – 0,67** — hiçbir test anlamlıya ulaşamaz.
>
> "Sızıntı saptanamadı" hükmü **ikinci çerçeveye** dayanır ve gerekçesi
> tedavinin tek bir bölmeye uygulanmış olmasıdır (bölme düzeyinde n=1):
> V_A'nın davranışının temiz bölmelerden farklı olması, sızıntıdan da o
> bölmenin idiyosenkrazisinden de kaynaklanabilir ve bu tasarımla
> ayrıştırılamaz. **Makale hangi çerçevede konuştuğunu açıkça yazmalı;
> "dürüst p = 0,10–0,19" ifadesi kaynaksız olduğu için kullanılmayacak.**

### Geri çekilen sayılar
- **s_Δ = 0,010** tekrarlanabilirlik değil **tesadüf**: tek ölçümün eşleşmiş
  SE'si 0,372; P(s ≤ 0,010 | gerçek Δ'lar özdeş) = 7,2×10⁻⁴. Aynı üç
  checkpoint çifti ayrık tahmincilerle ölçüldüğünde sd = 0,97 / 1,13 / 1,32.
- **t_p = 3×10⁻⁵** bu varyans deflasyonunun ürünüdür.
- **Havuzlanmış McNemar p = 10⁻⁶** yanlış niceliği ölçer (checkpoint çiftini
  sabit alır); negatif kontrolde de ateşliyor (§6b'nin önceden ilan ettiği
  %37-56 yanlış-pozitif oranıyla uyumlu).

### Öldürücü üç itiraz
1. **Mekanizmanın tek olası kanalında araç yok.** Yörünge sabit olduğundan
   sızıntı Δ_AB'yi ancak V_A'nın adv eğrisini bozarak etkileyebilir. Ölçülen:
   V_A adv fazlası ViT'te −0,47/−0,55/−0,08 (işaret negatif). **Çift ayrışma:**
   ResNet'te sızıntı izi var (clean fazlası +1,81/+1,59/+2,10; z = **+2,74 /
   +2,49 / +3,19**, `e2_audit.json → 7_manipulasyon_dozu`) ama etki yok;
   ViT'te iz yok (z = +0,05 / −0,09 / −0,14) ama "etki" var.
2. **Manipülasyon kontrolü ViT'te başarısız.** Clean ön-eğitim iki kolda da
   V_A'yı ezberledi (%100 train acc), ama AT epoch 1'de beklenen fazlanın
   ViT'te yalnız **%0,6-6,4'ü** ölçülüyor (+0,45/+0,12/+1,25 vs beklenen
   ~+19,6), ResNet'te **%43-57'si** (ve 100 epok kalıcı). **ViT kolunda tedavi
   fiilen uygulanmamıştır** — ölçülecek sızıntı yoktur.
   *Payda tanımı (beyan zorunlu):* "beklenen doz" = clean ön-eğitimin
   train−test genelleme açığı (100 − holdout doğruluğu). Alternatif payda
   (AT ep1'deki havuz temiz doğruluğu) ViT sonucunu değiştirmez ama ResNet
   oranını %12,7-17,2'ye indirir.
3. **Karşılaştırıcı keyfiliği + sahte-tekrarlama.** V_B ↔ V_C takası manşeti
   −1,05 → −0,49'a (p=0,47) taşıyor. V_A/V_B/V_C tek çekiliştir (seed 778,
   altı koşumun hepsi aynı dosya): **bölme düzeyinde etkin n = 1**, üç tohum
   yörüngeyi tekrarlar, tedaviyi değil.

### Çürütülen yan hikâyeler
- "ViT'in tepesi keskin, ResNet'inki düz, o yüzden yalnız ViT etkileniyor"
  **yanlış**: iki bağımsız temiz bölmenin aynı epoğu seçme olasılığı
  (`e2_bootstrap.json → P_ayni_epok`) ResNet s1001'de **0,23-0,35**, ViT
  s2002'de **0,66-0,81** — yani ViT seçimi ResNet'ten *daha* kararlı. Mimari
  asimetrisi seçim kararlılığıyla açıklanamaz.
- ResNet'in Δ_AB = +0,10'u "sızıntıya bağışıklık" değil, **seçim çakışması**:
  üç tohumun ikisinde A ve B aynı checkpoint'i seçtiği için Δ tanım gereği 0.

*(Bu bölümdeki "komşu-epok kalite değişimi", "etkileşim p" ve "null'da desen
olasılığı ≈0,25" gibi ilk sürümde yer alan sayılar, üretici kodları
bulunmadığı için ÇIKARILDI — R3 kuralı: makaleye girecek hiçbir sayı yalnız
düzyazıda yaşayamaz.)*

## 3. Makaleye giren ifadeler

**Kurulabilir (ASIL BULGU — protokol ızgarası, `e2_grid.json`):** *"Sabit bir
eğitim yörüngesi üzerinde yalnızca checkpoint-seçim protokolü değiştirildiğinde
— iki hiç-görülmemiş doğrulama bölmesi × üç erken-durdurma sabrı × üç
yumuşatma penceresi = 18 hücre — aynı 10k test kümesinde raporlanan PGD-10
doğruluğu ResNet-18'de 2,62-2,85, ViT-Tiny'de 1,58-2,09 puan aralığında
değişmektedir (yörünge-içi sd: ResNet 0,82; ViT 0,74)."*

**Zorunlu nitelemeler (R3 denetimi):**
- **Izgaranın boyut etiketi:** `patience=0` **saf argmax değildir** —
  `min_delta=0,1` koşulsuz uygulandığı için "koşan en iyiyi 0,1 puandan fazla
  aşan son epok" (ratchet) kuralıdır. Gerçek argmax kolu artık ayrıca
  hesaplanıyor (`e2_grid.json → argmax_kolu`, `ratchet_ozet`): **36 hücrenin
  7'sinde** farklı epok seçiliyor (ResNet 5/18, ViT 2/18); en büyük test
  etkisi **2,37 puan** (ResNet) ve **1,14 puan** (ViT). Argmax kolunun kendi
  yayılımı ResNet 0,88-2,32 / ViT 2,02-2,09 puan — yön değişmiyor.
- **Yayılımın baskın kaldıracı yumuşatmadır ve çoğu yörüngede tek yönlüdür:**
  marjinal ortalamalar k=1/3/5 için **6 yörüngenin 5'inde monoton düşüyor**
  (ör. ResNet s1001: 43,06 / 42,53 / 41,90); **istisna ViT s2002**
  (33,27 / 31,76 / 32,45 — düşüp yukarı dönüyor). `e2_grid.json →
  yumusatma_monoton_mu`. Yani yayılımın bir kısmı "protokol belirsizliği"
  değil "kötü bir seçicinin maliyeti"dir — ama bu niteleme 6/6 değil 5/6'dır.
- **Çekirdek ızgara** (makalelerin fiilen değiştirdiği boyutlar: bölme ×
  patience, k=1): protokol sd ResNet 0,58 / ViT 0,48; tohum sd 0,53 / 0,34 →
  oran **1,09× / 1,42×**.
- **Oranın referans duyarlılığı:** 18 referans protokolün tamamında ResNet
  0,671-3,379× (medyan 1,397; 2/18 ≤1), ViT 0,631-7,376× (medyan 1,358;
  3/18 ≤1). n=3'ün χ² belirsizliğiyle oranın %95 GA'sı **ResNet
  [0,24; 2,95], ViT [0,35; 4,17]** — ikisi de 1'i içeriyor (`e2_grid.json →
  REFERANS_DUYARLILIGI`, `oran_95_GA`). **Tek bir oran sayısı
  raporlanmayacak.**
- **Konvansiyon kontrolü aslında iki ailedir:** hücre düzeyinde sayıldığında
  edge/zero/valid **108/108 hücrede özdeş** seçim veriyor; nedensel (causal)
  yalnız 36/108'de aynı (`e2_grid.json → konvansiyon_hucre_ozdesligi`).
  Bağımsız olan tek alternatif nedensel ailedir; **"dört konvansiyon" ifadesi
  kullanılmayacak.**
- Patience ViT'te fiilen atıl (marjinal yayılım 0,00/0,00/0,35 puan).

**Kurulabilir (örnekleme dağılımı, `e2_split_bootstrap.json`):** *"Doğrulama
bölmesinin çekilişi bootstrap ile yeniden örneklendiğinde, ön-kayıtlı seçim
kuralının ulaştığı gerçek test doğruluğunun standart sapmasi 0,31-0,81 puan,
%95 aralık genişliği 0,69-2,18 puan ve oracle'a (en iyi checkpoint) göre
ortalama pismanlik 0,16-1,53 puandir; hiç sızıntı yokken iki bağımsız temiz
bölmenin ürettiği fark ortalama 0,30-0,97 puan olup 1 puanı aşma olasılığı
%9-53'tür."* — bu, "bölme düzeyinde n=1" sınırlamasını yeni eğitim olmadan
onaran gerçek bir dağılımdır ve **E2'nin en dayanıklı niceliksel çıktısıdır**
(protokol ızgarasının tanım duyarlılığından etkilenmez).

**Kurulabilir (sızıntı, §4 Kural 3 uyarınca):** ViT'te gözlenen −1,05 puanlık
fark raporlanır ama **sızıntıya atfedilmez**; simetrik tahminci
Δ_{A−(B+C)/2} = −0,77 ± 0,49 sıfırı içerir (n=3 t, p=0,113) ve bölme kimliği
sabit alındığında permütasyon tabanı zaten p ≥ 0,25'tir. Bölmeler
değiştirilebilir kabul edilirse aynı veri p = 0,007–0,052 verir; iki çerçeve
arasındaki seçim tasarımla belirlenemez (bölme düzeyinde n=1) ve bu
belirsizlik **açıkça beyan edilecektir**.

**Kurulabilir (KOŞULLU ATIF — makalenin taahhüt ettiği uç nokta,
`e2_conditional.json`):** *"Koşullu yanıltmada ViT eksi CNN farkının işareti,
seçim protokolünden bağımsız olarak korunmaktadır: dokuz seçilmiş
checkpoint'in (+3,84…+6,79), 18 protokol × 3 tohum çiftinden oluşan 54 temiz
ızgara hücresinin (+1,48…+7,45), sızıntılı bölmenin 27 hücresinin
(+2,80…+7,96) ve protokollerin erişebildiği tüm epok çiftlerinin (170/170,
+0,86…+9,05) tamamında pozitiftir; işaret yalnızca hiçbir protokolün
seçmediği yakınsama-öncesi bölgede (epok ≤25) değişmektedir."*

> **AŞIRI-İDDİA DÜZELTMESİ (2026-08-17 akşam, geçmiş denetçisi):** Bu bulgu
> ilk sürümde `05_discussion.tex`'teki taahhüdün "kesin cevabı" ilan
> edilmişti. **Bu doğru değildi.** Taahhüt şuydu: *"aynı veri üzerinde çiftler
> eğit, yalnızca seçim bölmesinin ön-eğitimde görülüp görülmediğini değiştir
> ve koşullu atfın ters dönüp dönmediğini ölç."* E2 bu tasarımı **kurmuyor**:
> altı yörüngenin **hepsinde** V_A clean ön-eğitimde görülmüştür (ön-kayıt §2,
> D_core ∪ V_A = 46.000); değişen şey "ön-eğitim bölmeyi gördü mü" değil,
> "hangi bölme seçiyor". Taahhüdü fiilen kuracak kol **P1 (sızıntı-takası)**
> ve o koşulmuyor. Üstüne ViT kolunda manipülasyon kontrolü başarısızdır.
>
> **Doğru ifade:** E2, taahhüdün *ilgili ama daha zayıf* bir versiyonunu
> cevaplıyor — "seçim bölmesinin kimliği (ve seçim protokolü) koşullu atfı
> ters çeviriyor mu?" → hayır, 251 ölçümün tamamında işaret korunuyor.
> Taahhüdün kendisi ya P1 koşularak karşılanacak ya da makale metni
> **ölçülen tasarımla yeniden yazılacak** (tercih edilen: ikincisi;
> `05_discussion.tex` gelecek-iş maddesi P1 + P1b olarak kalır).

Sızıntılı kolda fark **nominal olarak daha büyüktür** (V_A ile +6,29; temiz
V_B ile +4,88; negatif kontrol V_C ile +5,09) — ama bu sıralama sızıntıya
**atfedilmez**: eşli A−B farkı n=3'te p=0,09 ve belgenin kendi çerçevesinde
(bölme düzeyinde n=1, işaret permütasyonu tabanı 0,25) anlamlı olamaz; ayrıca
V_C > V_B olması sıralamanın bölme kimliğine de bağlanabileceğini gösterir.
Kesin olan tek şey **işaretin hiçbir protokolde dönmemesidir**.

Buna karşılık şu karşılaştırma bilgilendirici: makalenin eski sızıntılı koşumu
neredeyse parite gösteriyordu (+0,18), oysa **kontrollü sızıntı altında bile**
fark +6,29 çıkıyor. Yani o eski paritenin açıklaması seçim sızıntısı
**olamaz**; geriye eğitim-koşusu varyansı / reçete farkı kalır — makalenin
kendi ihtiyatlı ifadesini ("aynı anda hem validasyon işlemesi hem eğitim
koşusu değişti") doğrulayan bir sonuç.

**KURULAMAZ (yasak cümleler):**
- "Seçim sızıntısı ViT'te ~1,05 puan gürbüzlük kaybettiriyor (p=3e−5)."
- "Etki üç tohumda tekrarlanabilir / sd=0,01."
- "|Δ_AB| ≫ |Δ_BC|; sızıntı etkisi nicelenmiştir." (§4 Kural 2 dili —
  eşleşmiş |Δ_AB|−|Δ_BC| = +0,49 ± 0,97, %95 GA sıfırı içeriyor)
- "Sızıntı ViT'i etkiliyor, CNN'i etkilemiyor" (etkileşim p = 0,098-0,109)
- "V_C negatif kontrolü gürültü tabanının küçük olduğunu doğruluyor"
  (negatif kontrol ateşliyor: ViT B-C clean p = 8,9×10⁻¹³)
- Herhangi bir mekanizma cümlesi ("sızıntılı bölme ezberci checkpoint'leri
  ödüllendiriyor")
- **"X puana kadar oynuyor"** biçiminde, n=3'ün maksimumuna dayanan hiçbir
  ifade (ara hakemlik kararı; maksimumlar yalnız dağılımın uç noktası olarak,
  sd/aralık ile birlikte verilir)
- "Tohum yayılımının üç katı" (max ÷ sd karışımı; doğrusu 1,54× / 2,17×)
- "Sızıntı katkısı protokol yayılımının ~1/10'u" (ölçek uyumsuzluğu: 10,45
  puan **transfer asimetrisinin** protokol yayılımı, E2'nin 1,05'i ise
  **mutlak gürbüz doğruluk** farkı — aynı cetvele konulamaz)

## 4. Zorunlu sınırlamalar (makalede beyan)

1. Ortak bölme / sahte-tekrarlama: bölme düzeyinde n=1; s_Δ sızıntı bileşeni
   hakkında sıfır bilgi taşır (ön-kayıt §6'da önceden beyan edilmişti).
2. Varyans deflasyonu: s_Δ=0,010 tek ölçüm SE'sinden 37 kat küçük.
3. n=3 güç tabanı: **n=3'te işaret permütasyonunun ulaşabileceği en küçük iki
   yönlü p = 0,25** — yani bölme kimliği sabit çerçevede hiçbir test α=0,05'e
   ulaşamaz (`e2_audit.json → 5_durust_p.kuruluslar.*.b_isaret_permutasyonu`).
4. δ=1,0 kırılganlığı: δ* = 1,0669 (`e2_audit.json → 4_delta_yildiz`) —
   δ=1,05'te "FARKLI", δ=1,07'de eşdeğerlik dalına geçiyor. Ayrıca δ
   eğitim-tohumu std'sine kalibre edilmişti; ilgili bileşen seçim
   gürültüsüdür (ön-kayıt §2'nin hesabı: √2 × 1,10 ≈ 1,55 puan).
5. Karşılaştırıcı keyfiliği (B↔C takası: −1,05 → −0,49, p=0,47).
6. Çoklu karşılaştırma: 2 mimari × 3 ikili kontrast × 2 metrik = 12 hücre;
   ön-kayıt suskun. Düzeltme, §2'de beyan edilen çerçeveye göre yapılacak
   (tek bir "düzeltilmiş p" sayısı raporlanmayacak).
7. Uç nokta bağımsız değil: 18 hücrede seçim ve raporlama **aynı saldırı**
   (PGD-10, eps 8/255, seed 42); AutoAttack yok.
8. **Val→test aktarımı** *(düzeltildi 2026-08-17)*: ilk sürümdeki "eğim
   +0,457, artık sd 0,790" ikilisi **28 makul kuruluşun hiçbirinde**
   üretilemedi; kuruluşu belgelenmemişti ve kullanılmayacak. Yeniden
   hesaplanan gerçek değerler: seçilen epok çiftlerinde eğim 0,017–0,679
   (artık sd 0,34–0,86, kuruluşa göre), P0 sayesinde tüm 100 epok üzerinden
   ise eğim **0,80–0,95**, artık sd **0,56–0,70**. Yani aktarım seviye
   düzeyinde iyi, tekil seçim farklarında gürültülü. Nitel hüküm ayakta:
   vekil val ile 1 puanlık farklar güvenilir ölçülemez → P0 zorunluydu.
9. **McNemar yanlış-pozitif oranı** *(düzeltildi)*: §6b'nin öngördüğü
   "%37–56" yerine ölçülen gerçek aralık **%21–59** (ViT kolu %50–59,
   ResNet kolu %21–32). Nitel iddia her hücrede ayakta: en düşük oran bile
   nominal %5'in dört katından büyük.
10. **Manipülasyon dozu paydası tanıma duyarlı**: "beklenen ~+19,6 puan"
    değeri "clean ön-eğitimin train–test genelleme açığı" tanımıyla çıkar
    (100 − 80,4). Alternatif makul payda (AT ep1'deki havuz temiz doğruluğu)
    ile ViT oranı %0,3–3,1 (iddia ayakta) ama ResNet %12,7–17,2 olur ve
    "~%50" ifadesi çöker. **Payda makalede açıkça beyan edilecek.**

## 5. Yapılanlar / yapılacaklar

- **P0 (koşuldu):** `scripts/q1_e2_test_curve.py` — 6 yörünge × 100 checkpoint
  için tam 10k test clean/PGD-10 + örnek maskeleri
  (`testcurve_<arch>_s<seed>.npz`). Tüm betimleyici analizler artık vekil val
  yerine **birincil uç noktada** yapılabilir; gerçek test-optimal epok bilinir.
- **Yapılmayacak:** E4'ün +2 tohumu bu soruna **çare değildir** (aynı bölmeyle
  tohum eklemek deflasyonu tekrarlar; eksik boyut tohum değil **bölme
  çeşitliliği**). Sızıntı iddiası taşınmayacağı için P1 (sızıntı-takası, 21
  GPU-saat), P1b (pozitif kontrol/doz-yanıt, 21 GPU-saat) ve P2 (K bağımsız
  bölme çekilişi, K=5 için ~105 GPU-saat) **şimdilik koşulmayacak**; hakem
  talebi gelirse öncelik P1b → P1 → P2.
- **A1-A4 analiz betikleri (koşuldu, hepsi GPU'suz):** `q1_e2_grid.py`
  (protokol ızgarası + konvansiyon dayanıklılığı), `q1_e2_split_bootstrap.py`
  (bölme bootstrap'i birincil uç noktada), `q1_e2_conditional.py` (koşullu
  atıf, 4 katman), `q1_e2_audit.py` (denetimin tüm sayılarını üreten artefakt
  — hakemin "bu sayıların kodu yok" itirazına cevap; 9 maddeden 6'sı TUTUYOR,
  2'si KISMEN, 1'i TUTMUYOR ve düzeltildi).
- **`05_discussion.tex:80` taahhüdü KISMEN karşılandı:** E2, taahhüdün daha
  zayıf versiyonunu (seçim bölmesi/protokolü koşullu atfı çevirir mi?)
  cevaplıyor; taahhüdün kendisi (ön-eğitimde görülme durumunu değiştiren
  çiftler) **kurulmadı**. Metin ölçülen tasarımla yeniden yazılacak; P1
  gelecek-iş maddesi olarak kalacak. Bkz. §3 aşırı-iddia düzeltmesi.
- **MAKALENİN EN BÜYÜK RİSKİ (gidişat denetçisi, KRİTİK) — ÇÖZÜLDÜ
  (2026-08-17):** ana metindeki *"protokol yayılımı ≈ eğitim-koşusu sd'sinin
  yirmi katı"* iddiası, E2'de **iki kez geri çektiğimiz hatanın aynısıydı** —
  10,24 puanlık *aralığı* 0,50-0,55'lik *sd*'ye bölüyor ve üstüne ölçek
  uyumsuzdu (pay: transfer asimetrisi; payda: mutlak doğruluk).

  **Düzeltme:** `scripts/q1_variance_ratio.py` yazıldı → artefakt
  `results/q1/variance_ratio.json`. Her iki yayılım **aynı nicelik** (köşegen-
  dışı asimetri) üzerinde hesaplandı:
  - PAY (protokol etkisi): tohum-içi açıklık **10,45 ± 0,76** puan; sd 4,82
  - PAYDA (koşum etkisi, AYNI NİCELİK): protokole göre sd **0,23 - 1,48** puan
  - ORAN: ölçek-uyumlu iki tanımda **3,26× - 22,72×**
  - Hatalı biçim (aralık/sd) kayıt için saklandı: 7,06× - 45,21× → "yirmi"
    bu aralığın içindeydi ama **keyfiydi**.
  - **Pay ile payda bağımsız değil:** en büyük asimetriyi veren protokol
    (successful-source) en büyük koşum sd'sine de sahip (1,48) ve aralığın
    alt ucunu o üretiyor. En muhafazakâr eşleştirme bile ölçüm etkisini
    koşum etkisinin **3 katından fazla** bırakıyor — sav ayakta.

  8 konum düzeltildi (4 EN + 4 TR): `02_related_work.tex:74`,
  `04_experiments.tex:369`, `05_discussion.tex:15`, `06_conclusion.tex:9` ve
  TR eşleri. Tek kat-değeri manşeti kaldırıldı, yerine aralık + bağımlılık
  uyarısı yazıldı. Özet zaten güvenliydi ("3,3 katlık yayılım"), dokunulmadı.
  İki dil de temiz derlendi (EN 16 s., TR 15 s.; 0 tanımsız ref/atıf).
  **arXiv ön-baskısı önündeki engel kaldırıldı.**
- **E2'nin ana tezle birleşme yolu** (gidişat denetçisi): ikinci bir manşet
  değil, **ana manşetin paydasını düzeltmek**. Makalenin raporladığı 0,50-0,55
  koşum varyansı, üç tohumun tek bir seed-777 bölmesini paylaşması nedeniyle
  eksik ölçülmüştür; E2'nin bölme-bootstrap'i eksik bileşeni veriyor
  (sd 0,31-0,81). Hakemin "bu bölüm ne katıyor" sorusunun cevabı budur.
- **Bütünlük kanıtı (A4 madde 9):** aynı checkpoint'in iki bağımsız
  değerlendirmesinde (seçim koşumu vs P0 test eğrisi) temiz doğruluk 18/18
  hücrede **tam olarak eşit** (0 örnek uyuşmazlığı); çekişmeli fark ort
  +0,018, |max| 0,130 puan — saldırı-tohumu ölçüm tabanı, manşetin ~%12'si.

## 6. Tez cümlesi (E2'den türetilebilecek en güçlü hali)

> "Sabit bir eğitim yörüngesinde, yalnızca checkpoint-seçim protokolü
> değiştirildiğinde — hangi hiç görülmemiş doğrulama bölmesinin seçim yaptığı,
> hangi erken-durdurma eşiğinin kullanıldığı ve doğrulama eğrisinin
> yumuşatılıp yumuşatılmadığı — aynı test kümesinde raporlanan PGD-10
> doğruluğu ResNet-18'de 2,62-2,85, ViT-Tiny'de 1,58-2,09 puan aralığında
> değişmektedir. Yalnız bölme çekilişi yeniden örneklendiğinde bile raporlanan
> değerin standart sapması 0,31-0,81 puan, %95 aralık genişliği 0,69-2,18
> puandır ve seçim kuralı en iyi checkpoint'in ortalama 0,16-1,53 puan
> gerisinde kalmaktadır. Seçim sızıntısının bu yayılıma ek katkısı ise tek
> bölme çekilişiyle ayrıştırılamamıştır: bölme kimliği sabit alındığında
> hiçbir test anlamlıya ulaşamaz (permütasyon tabanı p ≥ 0,25), bölmeler
> değiştirilebilir alındığında ise aynı veri p = 0,007-0,052 verir."

**Neden oran manşete konmuyor:** protokol sd'sinin tohum sd'sine oranı
tanıma ve referans protokol seçimine duyarlıdır (18 referansta ResNet
0,67-3,38×, ViT 0,63-7,38×; çekirdek k=1 ızgarasında 1,09× / 1,42×; n=3 ile
%95 GA her iki mimaride 1'i içerir). Mutlak yayılım ve bootstrap dağılımı
kullanılır.

Bu bileşen **sıfır-şişkin ve kesiklidir**: iki temiz bölme ya aynı epoğu seçer
(Δ=0) ya da farklı seçer ve 1-2 puan fark üretir — yani gürbüzlük sayısı
sürekli bir gürültüyle değil, **manzara dejenere olduğunda ateşlenen bir
piyangoyla** oynuyor.

## 7. Kanoniklik kuralı (R3 zorunluluğu)

İki değerlendirme tabanı var ve aynı büyüklükler için farklı sayı veriyorlar
(saldırı tohumu farkı):
- **Ön-kayıtlı birincil tablo** (`e2_report.json`): `select_*_test.npz`
  tabanlı, saldırı tohumu 42. ViT Δ_AB = −1,050; ResNet +0,100.
- **Tüm protokol/ızgara/bootstrap/koşullu analizleri**: `testcurve_*.npz`
  tabanlı, tohum 42·10⁵+epok. ViT Δ_AB = −0,983; ResNet +0,14.

**Kural:** birincil (ön-kayıtlı) sonuçlar select tabanında raporlanır;
betimleyici/keşifsel analizlerin tamamı testcurve tabanındadır ve makalede
öyle etiketlenir. İki taban arasındaki ölçüm tabanı: temiz doğrulukta **tam
sıfır** (18/18 hücre), çekişmeli doğrulukta ortalama 0,018 / en fazla 0,130
puan.
