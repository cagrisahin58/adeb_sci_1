# Makale revizyon notu: doğrulayıcı bulgularının işlenmesi (31.10.2026)

Hazırlayan: makale yazarı (opus), tek tur düzeltme. Girdi: doğrulayıcının 27 bulgusu (kesinti sonrası devam turu). Dayanak: `12_makale_revizyon_brifi.md`, FÖY = `results/C1_REFERANS_FOYU.md` (31.10.2026 sürümü), ÖK = `ON_KAYIT_2026-10-29.md`. Git komutu kullanılmadı; föy, kapı betikleri, şekil betikleri ve dondurulmuş dosyalar değişmedi.

## Özet

27 bulgunun 21'i olduğu gibi düzeltildi, 6'sı kısmen düzeltildi (bulgunun haklı kısmı uygulandı, bir parçası aşağıdaki "Doğrulayıcı ile uyuşmazlık" başlığında kanıtla gerekçelendirildi ya da yetki dışı olduğu için ilgili ajana bırakıldı). Tümüyle reddedilen bulgu yok. Her bulgunun kanıtı föyden ya da ön kayıttan yeniden okundu; doğrulayıcının satır numaralarının hepsi doğru çıktı.

Derleme (`scripts/derle_en.sh`, `scripts/compile_check.sh`): 0 hata, 0 tanımsız gönderme ya da atıf (betiklerin "tanimsiz 1" sayımı `T1/pcr/n/n` yazı tipi uyarısıdır, gönderme değildir), 24 sayfa. `compile_check.sh`'nin saydığı 51 Overfull satırının 49'u `\output` sırasında 505 pt (şablon başlık bloğu), 2'si `main.tex` satır 126 `\maketitle` (9.27 pt); ikisi de şablondan gelir ve bu turun değişikliklerinden bağımsızdır. `main.bbl`'de "atif-kontrol" ya da "TODO" dizgesi artık geçmiyor.

Kapılar: `check_manuscript_claims.py` GEÇTİ (45/45), `check_abstract_body.py` GEÇTİ (EN özet 250 kelime, özetteki 31 sayının hepsi gövdede; TR 248 kelime). `check_pdf_typeset.py` GEÇTİ. `check_pdf_render.py` iki maddede KALDI: betik eski başlık dizgelerini ("The Conditioning Set Decides the Measured Transfer Asymmetry", "Source-Effect Reading", satır 65 ve 68) arıyor; başlık brif §1.1 gereği değişti, bu kapı güncellemesi kod-mimar işidir (brif §13). `verify_manuscript_numbers.py` KALDI (EN_EKSIK = 256, TR_EKSIK = 0), beklenen durum; liste aşağıda.

Kelime (yorum satırları hariç, brif §11 betiği): main.tex 651 (özet 250), 01 1152, 02 1076, 03 3900, 04 7534, 04z 238, 05 1533, 06 323, 07 1384; toplam 17,791 (tavan 18,720, hedef 16,700).

## Bulgu bulgu işlem kaydı

1. 04 IV-H "every scale, panel and dataset": düzeltildi; ImageNetV2 genellemeden çıkarıldı, "on both CIFAR datasets and on every scale and panel tested, and the descriptive ImageNetV2 panel points the same way" (FÖY 1903, 1945).
2. 05 V-A "agree with the initialized row": düzeltildi; "descriptively, less similar to the panel, consistent with the registered expectation" (FÖY 1938).
3. H3 ölçek nitelemesi: düzeltildi; özette "on the log scale architecture leaves direction unchanged", sınır cümlesi "CIFAR-10, the log scale and a CNN panel"; sonuçta "on the log scale architecture leaves the directional term unchanged" (FÖY 1551, 1552, 1606).
4. 04 satır 152 yorumuna M9.5:1593 eklendi.
5. 04 S4 paragrafı yorumuna 1575, 1576 eklendi.
6. `tab:pair_decomposition` üstüne `% FOY:TabloIII:160 ; Kaynak-hedef:390` eklendi.
7. 07 son kontrol noktası yorumuna 799, 808 eklendi.
8. 07 CIFAR-100 seçim yayılımı yorumu M8.7:1286 yerine 1280.
9. 07 yorumlarına 364, 100, 255, 146 eklendi.
10. 04 IV-I S5 paragrafına `% KAYNAK: ON_KAYIT Sec. 5 (S5 bandi +-1.5 puan)` eklendi (ÖK satır 82 doğruladı).
11. Öncül p: "is at least 0.989 (mean 0.997) against its upper bound of 1.000"; "1.000" dizgesi kapı E2 için metinde (FÖY 641, 1161, 1162).
12. McNemar: "on the full test set, paired by image" (FÖY 43-45; her-ikisi-doğru sınırı 36-40 ayrı).
13. Çift işaret: S2 ve S3 cümlelerinde "lowers ... by −x" yerine "changes ... by −x".
14. `tab:panel_tests` "Predicted size met": CIFAR-10 hücresine K-b eklendi (FÖY 1588 "evet"); iki hücre aynı kalıba getirildi.
15. 07 L2: "seven distinct target-error values, and six of the directions share the fixed WideResNet target" (FÖY 1174).
16. Kaynakçada "tODO: atif-kontrol" basımı: kısmen; aşağıya bakınız.
17. H1'in yeni bilgi içeriği: düzeltildi. `subsec:prereg`'e sayısız cümle: sahte çalıştırma ve masa çözümlemesi V ile R32 arasındaki σ farkını göstermişti, H1 öngörüsü bu fark bilinerek yazıldı, H1'in bunun ötesinde sınadığı şey 224 piksellik ResNet-18'in ResNet tarafını yeniden üretmesidir. IV-D'de S1 cümlesinin ardından H1 ile S1 ilişkisi tek cümle. ÖK §1'deki sahte H1 kestirimi (−0.335) föyde olmadığı için yazılmadı.
18. Sonuç ve giriş karıştırıcıyı taşımıyordu: düzeltildi. 06'da "Trained from scratch on a matched input pipeline and recipe, the ViT is less similar to the panel than the ResNet, a contrast that also carries the ViT's lower clean accuracy"; saldırı cümlesi "Momentum PGD and our adaptation of token gradient regularization do not close the gap"; 01'de "The source gap does not depend on a weak attack either" yerine aynı daraltma; özette "best permitted attack".
19. Tasarım sözcükleri: düzeltildi. 03'te "the scratch row differs in the architecture package and, for V-scr, in training campaign and adversarial-epoch cap"; demet "cancels from the interaction contrast only if its effect does not depend on architecture"; 05 sınırlılıkta "whose separate effects, and their interaction with architecture, are not identified".
20. Logit ölçek: kısmen; aşağıya bakınız. Özet, giriş (01:42), tartışma (05:19), sonuç (06:14) ve `fig:estimates_forest` altyazısı "işaret döner" yerine logit ölçekte ViT'nin yönlü teriminin büyük ve negatif olduğunu yazıyor; IV-H'ye log ölçeğin neden birincil olduğunu söyleyen cümle eklendi.
21. Koşullu aralıklar: kısmen; 03 `subsec:statistics` ve `tab:panel_tests` altyazısına cümle eklendi ("K-a and K-b intervals are t intervals over the three seed values and are conditional on the fixed test images and panel members; only the K-c bootstrap also resamples images"; ÖK satır 64 K-c bootstrap'inin görüntüleri de çektiğini doğruladı). Föye ρ düzeyinde görüntü bootstrap'i eklemek bu turun yetkisinde değil.
22. Mantel aile blok yapısı: kısmen; ikinci yol uygulandı. 03:260, 04 IV-G (aile blokları, karma çiftlerin en düşük hizalanma, tohumların neredeyse kopya olmasının permütasyon değiş-tokuş edilebilirliğini zorlaması) ve 05 sınırlılık cümlesi; özette "a necessary condition for similar transfer" kaydı ve "predicts" yerine "tracks". Aile ayıklamalı Spearman föyde yok (brif §9), birinci yol bu turda yapılamaz.
23. O1 tanımsızdı: düzeltildi; 03 `subsec:statistics`'te O1 bölgesi ve önceden yazılmış manşet yan cümleyle verildi (ÖK satır 100), IV-D cümlesi bu tanıma gönderiyor.
24. Şekilde D, metinde G: kısmen; aşağıya bakınız. Altyazıya q'nun okunuşu eklendi.
25. MI-FGSM iki değer: düzeltildi; 04 IV-I "CNN→ViT 19.07±0.33% against ViT→CNN 15.42±0.52%", 07'de C2 değerinin ayrı koşu olduğu ve aynı yön için 15.42 verdiği (FÖY 146, 1196).
26. Nedensel fiiller: düzeltildi; 05 "accounts for most of a source's transfer deficit into it", 04 "ViT-Tiny's weak-source appearance against CNNs is carried by its dissimilarity to them".
27. Üslup ve bütçe: kısmen; 04:380 "Unlike the CIFAR-100 pair, the Singh pairs are matched in clean accuracy and vulnerability." 03 aşağıya bakınız.

## Doğrulayıcı ile uyuşmazlık

Bulgu 16 (kırmızı, kaynakça). Basım sorunu haklıydı ve düzeltildi: 12 girdideki `note = {TODO: atif-kontrol}` alanı, IEEEtran'ın basmadığı `x-atifkontrol = {TODO: dogrulanmadi}` alanına taşındı; derlenmiş `main.bbl`'de dizge artık yok, girdilerin "doğrulanmadı" işareti `.bib`'de korunuyor. Künyelerin doğrulanması ise makale yazarının işi değil, brif §13'te bu turdan sonra sıralanmış atif-kontrol turunun işidir; bu yüzden doğrulama burada yapılmadı ve PDF atif-kontrol geçmeden dışarı gönderilmemelidir. Doğrulanamayan panel üyeleri için brif §7 kararı (yalnız RobustBench kimliği ve `\cite{croce2021robustbench}`) atif-kontrol sonucuna göre uygulanacak.

Bulgu 20 (logit ölçek). Önerilen gerekçe "özdeşlik yalnız log ölçekte kesindir" yanlıştır: Denklem (tau_def, r_def) tanımlarında log yerine herhangi bir dönüşüm (logit dahil) konduğunda özdeşlik cebirsel olarak yine kesin çıkar, çünkü tanımlar dönüştürülmüş oranların doğrusal birleşimleridir. ÖK satır 17 de ölçekleri yalnız "birincil doğal log, logit ve oran duyarlılık" diye sabitler. IV-H'ye bu nedenle iki doğru gerekçe yazıldı: yarı-simetri biçimi T_ij = w_j τ̄_ij log ölçekte toplamsaldır ve log ölçek ön kayıtta ölçümden önce birincil diye sabitlenmiştir. Ayrıca "eşdeğerlik sınırının üç katı" türetilmiş oranı föyde olmadığı için yazılmadı; yerine "far outside the ±0.10 band".

Bulgu 21 (görüntü bootstrap'i). Metin düzeltmesi yapıldı; "mümkünse föye K-b için ρ düzeyinde görüntü bootstrap'i eklenmeli" önerisi bu turun yetkisi dışındadır (föy ve `build_reference_sheet.py` değişmez). Ana oturum için açık iş: B2 K-a ve K-b için görüntü bootstrap'i (ÖK §5 duyarlılığı, FÖY 1607 "üretilmedi"); hakemin ilk soracağı kalem olabileceği notu yerindedir.

Bulgu 22 (Mantel). Birinci yol (föye aile içi Spearman ve aile kovaryatlı kısmi Mantel) bu turda yapılamaz; R11 §7'deki değerler föyde yok (brif §9). Ana oturum için açık iş olarak önerilir; o zamana kadar metin sınır cümlesini taşıyor.

Bulgu 24 (şekilde D). Altyazı düzeltildi (q'nun okunuşu: "q exceeds one when the directional part narrows the gap"). Şekil betiği `paper/figures/konsey/fig_source_gap_split.py` bu rolün yazma alanı dışında (görev metni yalnız `paper/manuscript` dosyalarına yetki veriyor; brif §13 bu klasörü şekil ajanına verir). Şekil ajanı için istek: göstergede "total gap D" ve "registered D threshold" yerine G ("total gap G", "registered G threshold"), sonra kapsayıcıda yeniden üretim.

Bulgu 27 (03 bütçesi). 04:380 düzeltildi. 03 yorumsuz 3900 kelime, ama bunun 804'ü tablo ve şekil ortamıdır (`tab:registry`, `tab:design`, `tab:protocol_masks`, iki altyazı); düzyazı yaklaşık 3100 kelimedir ve kesinti öncesi düzyazıyla (3058) aynı düzeydedir. Aşım, brif §5.11'in karar kuralı paragraflarının yerine koyduğu `tab:registry`'den gelir. Bu turda karar kuralı paragrafı tablodan yinelenen kısım atılarak kısaltıldı ve bir cümle sadeleştirildi, ama doğrulayıcının istediği yeni beyanlar (O1 tanımı, H1 görülmüş veri beyanı, koşullu aralık, aile blok yapısı) 03'e girdiği için net sayı arttı. 3400'e inmek için ayrı bir kısaltma turu ya da tablo kelimelerinin bütçe dışında sayılması gerekir; toplam tavanın (18,720) altında kalındı.

## Kalan yer tutucular

`sections/07_appendix.tex` satır 137 `% TODO(foy)`: saldırı tohumu tekrarının SD'si föyde yok, cümle sayısız. Satır 144 `% TODO(foy)`: CIFAR-100 C3 hedeflerinin temiz hataları föyde yok, cümle sayısız. Şekil yer tutucusu (`BEKLIYOR`) yok. `references.bib`'de 12 girdi `x-atifkontrol = {TODO: dogrulanmadi}` taşır (aşağıda).

## .bib'e giren doğrulanmamış aday kimlikler (atif-kontrol için)

| Anahtar | Aday kimlik | Not |
|---|---|---|
| touvron2021training | arXiv 2012.12877 | yayın yeri (ICML 2021) API'de yok |
| wightman2021resnet | arXiv 2110.00476 | ön baskı |
| sehwag2022robust | arXiv 2104.09425 | RobustBench Sehwag2021Proxy_R18 ve Sehwag2021Proxy eşleşmesi doğrulanacak |
| addepalli2022efficient | arXiv 2210.15318 | RobustBench Addepalli2022Efficient_RN18 |
| rade2022reducing | kimlik yok | arXiv ve DOI bulunamadı; başlık hafızadan; RobustBench Rade2021Helper_R18_ddpm |
| pang2022robustness | arXiv 2202.10103 | RobustBench Pang2022Robustness_WRN28_10 |
| jia2022lasat | arXiv 2203.06616 | RobustBench Jia2022LAS-AT_34_10 |
| hendrycks2019using | arXiv 1901.09960 | RobustBench Hendrycks2019Using |
| salman2020adversarially | arXiv 2007.08489 | RobustBench Salman2020Do_R18, _R50, _50_2 |
| chen2024data | DOI 10.1016/j.patcog.2024.110394 | Crossref aramasından; RobustBench Chen2024Data_WRN_50_2 eşleşmesi doğrulanmadı |
| peng2023robust | arXiv 2308.16258 | BMVC 2023 |
| mantel1967detection | kimlik yok | Cancer Research 27(2):209-220, cilt ve sayfa hafızadan, DOI yazılmadı |

## TR aynası için bölüm bölüm değişiklik özeti

Özet (`main.tex`): "Vision Transformers" yerine "ViTs"; "white-box" düştü; "three seed pairs" yerine "three seeds"; tasarım "architecture-by-initialization design at a matched pipeline"; H3 "on the log scale"; "best permitted attack"; maskeleme parantezi "PGD-10 gaps 3.20–7.40 points"; CIFAR-100 cümlesi "symmetric share and seed similarity replicate but the ViT's small directional term does not (+0.143), and on the logit scale it is strongly negative on both datasets, confining a small directional term to CIFAR-10, the log scale and a CNN panel"; gradyan "a necessary condition for similar transfer, tracks similarity"; son cümle "The conditioning protocol alone moves the asymmetry from 4.36 to 19.37 points".

Giriş (01): katkı 3'te saldırı cümlesi "Momentum PGD and our adaptation of TGR do not close the source gap either: under each source's best permitted attack among these and PGD-10 ..."; sınır paragrafında "on the logit scale the ViT's directional term is large and negative".

Yöntem (03): `subsec:design` sıfırdan satırı "architecture package and, for V-scr, training campaign and adversarial-epoch cap"; demet etkileşimden ancak etkisi mimariye bağlı değilse düşer. `subsec:metrics` p cümlesinin "exact only on targets whose p is close to one" kuyruğu düştü. `subsec:gradcos_def` sonuna aile blok yapısı. `subsec:statistics`: aralıkların sabit görüntü ve panele koşullu olduğu; karar ilkesi paragrafı kısaltıldı; O1 bölgesi ve önceden yazılmış manşet. `subsec:prereg`: H1'in görülmüş σ farkı bilinerek yazıldığı ve neyi sınadığı.

Deneyler (04): IV-A McNemar "full test set, paired by image"; IV-C K-b son cümlesi nedensellikten arındı, `tab:panel_tests` altyazısına koşullu aralık cümlesi ve öngörülen büyüklük satırı eşitlendi, `fig:source_gap_split` altyazısına q okunuşu; IV-D O1 göndermesi, S2 ve S3 "changes ... by", S1 sonrası H1 cümlesi; IV-F Singh cümlesi yeniden yazıldı; IV-G aile blok yapısı ve değiş-tokuş edilebilirlik; IV-H log ölçeğin birincilliği, sınır cümlesi ImageNetV2'yi dışarıda tutuyor, orman şekli altyazısı; IV-I MI-FGSM yönleri açık, öncül p "at least 0.989 (mean 0.997) against its upper bound of 1.000".

Tartışma (05): V-A logit cümlesi, "accounts for most of a source's transfer deficit", ImageNetV2 "descriptively ... consistent with the registered expectation"; V-D başlatma demetinin mimariyle etkileşimi, kısmi istatistiğin aile bloklarını ayırmadığı.

Sonuç (06): sıfırdan satırı temiz doğruluk karıştırıcısıyla; H3 "on the log scale"; saldırı cümlesi daraltıldı; logit ölçekte ViT'nin yönlü olarak güçlü kaynak olduğu.

Ek (07): Ek A TGR cümlesine ayrı koşu ve 15.42 kaydı; Ek C L2 hedef hata cümlesi. Kaynakça: TR'de de `note` yerine `x-atifkontrol` (aynı `.bib` kullanılıyorsa otomatik).

## verify_manuscript_numbers.py eksik listesi (EN_EKSIK = 256; kapı betiği sonraki turda güncellenecek)

Listedeki kalemler eski taşıyıcı sayılardır (eski tablolar düştü ya da sayılar Ek'e farklı biçimde taşındı); bir kısmı (ör. Hoyer 0.4928) Ek tablolarında `±` biçimiyle durduğu hâlde betiğin taradığı biçime uymuyor. Satır biçimi: betiğin etiketi = değer.

- C3 gelen-transfer r = 0.986
- C3 egim (0,762) = 0.762
- ozdeslik artik/sapma max % = 1.39
- Hoyer ResNet = 0.4928
- Hoyer ViT = 0.4561
- alan50 ResNet = 0.0378
- alan50 ViT = 0.0397
- TGR hedef-dogru = 12.70
- MI hedef-dogru = 15.71
- ResNet layer4.0 kosinus = 0.8777
- oran ust (22,7) = 32.6
- benzeri-benzeriyle oran (20,9) = 28.3
- E1 temiz ResNet = 63.86
- E1 PGD ResNet = 19.30
- E1 AA ResNet = 15.04
- E1 temiz ViT = 43.17
- E1 PGD ViT = 11.15
- E1 AA ViT = 8.87
- E1 karistirici r n=3 (0,974) = 0.974
- E1 cakisik hedef hatasi A = 36.15
- E1 cakisik hedef hatasi B = 36.36
- E1 bilesim etkisi t1 = -1.249
- E1 bilesim etkisi t2 = -1.330
- E1 bilesim etkisi t3 = -1.065
- E2 secim yayilimi alt ResNet = 2.62
- E2 secim yayilimi ust ResNet = 2.85
- E2 secim yayilimi ust ViT = 2.09
- E2 oran alt ResNet = 0.67
- E2 oran ust ResNet = 3.38
- E2 oran alt ViT = 0.63
- E2 oran ust ViT = 7.38
- E3 4-protokol egim = 0.528
- E3 4-protokol GA ust = 0.418
- E3 3-protokol egim = 0.431
- E3 3-protokol GA alt = 0.333
- E3 3-protokol GA ust = 0.633
- E3 en genis protokol cifti = 23.77
- E7 temiz ResNet = 94.27
- E7 temiz sd ResNet = 0.70
- E7 PGD ResNet = 55.52
- E7 temiz ViT = 92.42
- E7 PGD ViT = 52.30
- E7 ham fark = 0.39
- E7 basarili-kaynak fark = 2.70
- E7 protokol yayilimi = 3.70
- E7 esli GA alt = 0.76
- E7 esli GA ust = 0.07
- E3 A 4prot GA alt = 0.219
- E3 A 4prot GA ust = 0.371
- E3 A 3prot egim = 0.673
- E3 A 3prot GA alt = 0.602
- E3 A 3prot GA ust = 0.727
- E3 B 4prot egim = 0.528
- E3 B 4prot GA ust = 0.418
- E3 B 3prot egim = 0.431
- E3 B 3prot GA alt = 0.333
- E3 B 3prot GA ust = 0.633
- B8 C100 yayilim ust = 1.83
- B8 C10 yayilim alt = 0.54
- B8 C10 yayilim ust = 2.83
- B8 C100 yayilim ort = 0.86
- E6 PGD-L2 ResNet = 63.78
- E6 PGD-L2 sd ResNet = 0.38
- E6 PGD-L2 ViT = 51.72
- E6 AA-L2 ResNet = 60.61
- E6 temiz 5k ResNet = 85.33
- E6 AA-L2 ViT = 49.85
- E6 temiz 5k ViT = 73.61
- E6 O1 egim = 0.914
- T4 OZDESLIK TERIMI (ham - hedef-dogru) = 9.21
- T3 aciklik ham->basarili-kaynak = 5.79
- T3 tohum1 GA alt = 7.61
- T3 tohum1 GA ust = 9.44
- T3 tohum2 GA alt = 7.10
- T3 tohum2 GA ust = 9.01
- T3 tohum3 GA alt = 7.28
- T3 tohum3 GA ust = 9.20
- T3 kosumlar arasi t alt = 7.68
- T3 kosumlar arasi t ust = 8.86
- T3 kosum p Frac = 0.042
- T3 kosum p hizalanma = 0.0009
- T3 kosum Holm (uc olcu) = 0.108
- T4 C100 artik (her-ikisi - hedef-dogru) = 5.97
- T4 C100 yayilim = ozdeslik payi = 13.58
- T4 blok CLS minimumu = 0.9604
- T4 blok yama-ort minimumu = 0.9870
- T4 blok tum-jeton minimumu = 0.9803
- T4 CLS/yama kayma orani = 3.05
- KH C10 target_correct kaynak_etkisi_farki_ResNet_eksi_ViT sd = 0.09
- KH C10 target_correct hedef_etkisi_farki_ViT_eksi_ResNet sd = 0.51
- KH C10 target_correct max_abs_artik ort = 0.65
- KH C10 target_correct R2 ort = 0.9782
- KH C10 target_correct R2 sd = 0.0032
- KH C10 raw kaynak_etkisi_farki_ResNet_eksi_ViT ort = 4.47
- KH C10 raw hedef_etkisi_farki_ViT_eksi_ResNet ort = 8.13
- KH C10 raw asimetri_ResNettoViT_eksi_ViTtoResNet ort = 13.62
- KH C10 raw asimetri_ResNettoViT_eksi_ViTtoResNet sd = 0.38
- KH C10 raw max_abs_artik ort = 0.51
- KH C10 raw R2 ort = 0.9964
- KH C10 raw R2 sd = 0.0004
- KH C10 sabit WRN WRN_hedef_fark_ResNet_eksi_ViT sd = 0.17
- KH C10 sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT ort = 3.33
- KH C100 target_correct kaynak_etkisi_farki_ResNet_eksi_ViT ort = 9.54
- KH C100 target_correct kaynak_etkisi_farki_ResNet_eksi_ViT sd = 0.64
- KH C100 target_correct hedef_etkisi_farki_ViT_eksi_ResNet ort = 6.19
- KH C100 target_correct R2 ort = 0.9871
- KH C100 target_correct R2 sd = 0.0015
- KH C100 raw kaynak_etkisi_farki_ResNet_eksi_ViT ort = 6.48
- KH C100 raw kaynak_etkisi_farki_ResNet_eksi_ViT sd = 0.38
- KH C100 raw hedef_etkisi_farki_ViT_eksi_ResNet ort = 10.72
- KH C100 raw hedef_etkisi_farki_ViT_eksi_ResNet sd = 0.97
- KH C100 raw max_abs_artik ort = 0.67
- KH C100 raw max_abs_artik sd = 0.01
- KH C100 raw R2 ort = 0.9946
- KH C100 sabit WRN WRN_hedef_fark_ResNet_eksi_ViT ort = 7.94
- KH C100 sabit WRN WRN_hedef_fark_ResNet_eksi_ViT sd = 0.54
- KH C100 sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT ort = 7.79
- KH C10 sabit WRN orani (ozet matris) WRN_hedef_ResNetten = 12.48
- KH C10 sabit WRN orani (ozet matris) WRN_hedef_ViTden = 8.65
- KH C10 sabit WRN orani (ozet matris) WRN_kaynak_ResNete = 21.48
- KH C10 sabit WRN orani (ozet matris) WRN_kaynak_ViTe = 18.15
- KH C10 both_correct kaynak_etkisi_farki_ResNet_eksi_ViT ort = 6.76
- KH C10 both_correct hedef_etkisi_farki_ViT_eksi_ResNet ort = 0.53
- KH C10 both_correct asimetri_ResNettoViT_eksi_ViTtoResNet ort = 8.30
- KH C10 both_correct asimetri_ResNettoViT_eksi_ViTtoResNet sd = 0.16
- KH C10 both_correct max_abs_artik ort = 1.04
- KH C10 both_correct max_abs_artik sd = 0.11
- KH C10 both_correct R2 ort = 0.9643
- KH C10 both_correct R2 sd = 0.0072
- KH C10 both_correct sabit WRN WRN_hedef_fark_ResNet_eksi_ViT ort = 4.69
- KH C10 both_correct sabit WRN WRN_hedef_fark_ResNet_eksi_ViT sd = 0.38
- KH C10 both_correct sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT ort = 2.60
- KH C10 both_correct sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT sd = 0.72
- KH C100 both_correct kaynak_etkisi_farki_ResNet_eksi_ViT ort = 11.79
- KH C100 both_correct kaynak_etkisi_farki_ResNet_eksi_ViT sd = 0.83
- KH C100 both_correct hedef_etkisi_farki_ViT_eksi_ResNet ort = 2.85
- KH C100 both_correct max_abs_artik ort = 0.99
- KH C100 both_correct R2 ort = 0.9851
- KH C100 both_correct R2 sd = 0.0035
- KH C100 both_correct sabit WRN WRN_hedef_fark_ResNet_eksi_ViT ort = 9.81
- KH C100 both_correct sabit WRN WRN_hedef_fark_ResNet_eksi_ViT sd = 1.03
- KH C100 both_correct sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT ort = 4.83
- KH C100 successful_source kaynak_etkisi_farki_ResNet_eksi_ViT ort = 20.82
- KH C100 successful_source kaynak_etkisi_farki_ResNet_eksi_ViT sd = 1.43
- KH C100 successful_source hedef_etkisi_farki_ViT_eksi_ResNet ort = 8.12
- KH C100 successful_source hedef_etkisi_farki_ViT_eksi_ResNet sd = 2.23
- KH C100 successful_source max_abs_artik ort = 2.40
- KH C100 successful_source R2 ort = 0.9830
- KH C100 successful_source R2 sd = 0.0008
- KH C100 successful_source sabit WRN WRN_hedef_fark_ResNet_eksi_ViT ort = 16.03
- KH C100 successful_source sabit WRN WRN_hedef_fark_ResNet_eksi_ViT sd = 1.42
- KH C100 successful_source sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT ort = 12.91
- KH C100 successful_source sabit WRN WRN_kaynak_fark_ResNet_eksi_ViT sd = 2.29
- Mahmood C10 toplamsal R2 = 0.3681
- Mahmood C10 toplamsal max artik = 74.04
- Mahmood C10 aile-terimli R2 = 0.7852
- Mahmood C10 aile-terimli max artik = 29.33
- Mahmood C10 CNN_vs_ViT_hibrit_haric toplamsal kaynak = 25.01
- Mahmood C10 CNN_vs_ViT_hibrit_haric toplamsal hedef = 2.08
- Mahmood C10 CNN_vs_ViT_hibrit_haric aile-terimli kaynak = 10.78
- Mahmood C10 CNN_vs_ViT_hibrit_haric aile-terimli hedef = 12.15
- Mahmood C100 toplamsal R2 = 0.4508
- Mahmood C100 toplamsal max artik = 66.29
- Mahmood C100 aile-terimli R2 = 0.8425
- Mahmood C100 aile-terimli max artik = 24.33
- Mahmood C100 CNN_vs_ViT_hibrit_haric toplamsal kaynak = 22.77
- Mahmood C100 CNN_vs_ViT_hibrit_haric toplamsal hedef = 14.74
- Mahmood C100 CNN_vs_ViT_hibrit_haric aile-terimli kaynak = 9.43
- Mahmood C100 CNN_vs_ViT_hibrit_haric aile-terimli hedef = 1.39
- Mahmood C100 ResNet_vs_ViT toplamsal kaynak = 21.90
- Mahmood C100 ResNet_vs_ViT toplamsal hedef = 30.15
- Mahmood C100 ResNet_vs_ViT aile-terimli kaynak = 8.55
- Mahmood C100 ResNet_vs_ViT aile-terimli hedef = 16.81
- Mahmood anahtar cift etki araligi alt = 1.25
- Mahmood anahtar cift etki araligi ust = 2.15
- Mahmood anahtar cift protokol etkisi (p_min) = 0.57
- havuz Carmon2019_WRN28_10/Gowal2020_WRN28_10 temiz fark = 0.21
- havuz Carmon2019_WRN28_10/Gowal2020_WRN28_10 dort yayilim = 9.03
- havuz Debenedetti2022_XCiT_S12/Gowal2020_WRN28_10 temiz fark = 0.58
- havuz Debenedetti2022_XCiT_S12/Gowal2020_WRN28_10 dort yayilim = 12.73
- havuz ResNet18_AT/Engstrom2019_RN50 temiz fark = 1.66
- SVHN temiz ResNet kosum1 = 94.76
- SVHN temiz ViT kosum1 = 92.82
- SVHN temiz ResNet kosum2 = 93.77
- SVHN temiz ViT kosum2 = 92.03
- SVHN temiz fark ort = 1.84
- temiz ciftler p en kucuk (4) = 0.8774
- Standard WRN hedef p en buyuk = 0.9962
- ViT temiz hedef p en kucuk = 0.9231
- ViT temiz hedef p en buyuk = 0.9338
- ResNet temiz hedef p en kucuk = 0.8961
- Standard WRN hedef artik en buyuk = 0.64
- ResNet temiz hedef artik en buyuk = 0.51
- temiz cift ('ResNet18_clean', 'ViT_Tiny_clean') temiz fark ort = 15.16
- temiz cift ('ResNet18_clean', 'ViT_Tiny_clean') temiz fark sd = 0.48
- temiz cift ('ResNet18_clean', 'ViT_Tiny_clean') yayilim ort = 13.25
- temiz cift ('ResNet18_clean', 'Standard_WRN28_10') temiz fark ort = 0.47
- temiz cift ('ResNet18_clean', 'Standard_WRN28_10') temiz fark sd = 0.16
- temiz cift ('ResNet18_clean', 'Standard_WRN28_10') yayilim ort = 0.19
- temiz cift ('ResNet18_clean', 'Standard_WRN28_10') yayilim sd = 0.02
- temiz cift ('ViT_Tiny_clean', 'Standard_WRN28_10') temiz fark ort = 14.69
- temiz cift ('ViT_Tiny_clean', 'Standard_WRN28_10') yayilim ort = 13.08
- temiz cift kaynak farki ort = 69.18
- temiz cift kaynak farki sd = 2.31
- temiz cift hedef farki ort = 75.05
- temiz cift hedef farki sd = 1.72
- temiz cift sabit-Standard Standard->ResNet = 84.05
- temiz cift sabit-Standard Standard->ViT = 7.62
- temiz cift sabit-Standard ResNet->Standard = 81.40
- temiz cift sabit-Standard ViT->Standard = 13.60
- temiz cift sabit-Standard kaynak karsitligi = 67.80
- temiz cift sabit-Standard hedef karsitligi = 76.43
- havuz toplamsal R2 = 0.8955
- havuz ViT_Tiny_AT kaynak etkisi = 4.87
- havuz ViT_Tiny_AT hedef etkisi = 0.63
- son ckpt yayilim dort ort = 12.84
- son ckpt yayilim uc ort = 7.84
- son ckpt temiz fark ort = 10.55
- son ckpt ss asimetri ort = 17.48
- son ckpt p en kucuk = 0.9915
- son - secilen temiz fark ort = 1.71
- secilen temiz fark ort = 12.26
- secilen temiz fark sd = 0.90
- yorunge C10 temiz fark en kucuk = 10.59
- yorunge ('cifar100', 'ResNet-18') yayilim Delta ort = 1.84
- yorunge ('cifar100', 'ResNet-18') yayilim Delta sd = 0.94
- yorunge ('cifar100', 'ViT-Tiny') yayilim Delta sd = 0.24
- yorunge ('cifar10', 'ResNet-18') yayilim Delta ort = 1.53
- yorunge ('cifar10', 'ResNet-18') yayilim Delta sd = 1.15
- yorunge ('cifar10', 'ViT-Tiny') yayilim Delta sd = 1.15
- yorunge C10 ViT tc Delta ort = 2.53
- C1 kosumlar arasi aralik raw = 0.63
- C1 kosumlar arasi aralik target_correct = 0.86
- C1 kosumlar arasi aralik both_correct = 0.46
- C10 bc-tc t alt = 3.12
- C10 bc-tc t ust = 4.70
- C100 bc-tc ort = 5.97
- C100 bc-tc t alt = 3.53
- C100 bc-tc t ust = 8.40
- L2 bc-tc t alt = 1.33
- L2 bc-tc t ust = 2.56
- SVHN bc-tc cift2 = 0.49
- C10 ss-bc ort = 11.10
- C10 raw-tc sd = 0.76
- E3 SVHN dahil uc egim = 0.470
- E3 SVHN dahil uc GA alt = 0.361
- E3 SVHN dahil uc GA ust = 0.665
- E3 ozdeslik terimi egim = 0.471
- E3 ozdeslik terimi GA alt = 0.3615
- E3 ozdeslik terimi GA ust = 0.6666
- E3 SVHN dahil dort egim = 0.133
- TOST temiz entropi en kucuk = 4.61
- TOST temiz entropi en buyuk = 5.11
- devrilen/devrilmeyen p ResNet = 0.080
- tum ciftler uc grup-birak en kucuk = 0.767
- tum ciftler uc grup-birak en buyuk = 0.855
