# Hakem konseyi bulgularının uygulanması (31.10.2026)

Dayanak: `birlesik.md` (karar BUYUK_REVIZYON, 36 "uygulanır" bulgu, R1-R6 ret, A1-A15 açık iş) ve ana oturumun yedi bağlayıcı kararı. Yazan: makale yazarı ajan (opus). Dokunulan dosyalar yalnız `paper/manuscript/main.tex`, `macros_konsey.tex`, `sections/01-07` ve bu rapordur; `references.bib`, `paper/figures/`, `scripts/`, `results/` değişmedi. Satır numaraları düzeltme sonrası dosyalarındır. Değişiklik öncesi kaynakların kopyası oturum karalama klasöründe (`scratchpad/yedek/`) duruyor.

Özet sayılar: birleşik raporun 36 "uygulanır" bulgusundan 34'ü metinde uygulandı (B4, B5, B6, B9, B11, B14 ve B18'de yalnız metin kısmı), 2'si (B15 ve m16) yalnız şekil dosyasına dokunduğu için şekil ajanına kaldı. Ana oturumun yedi kararının yedisi de uygulandı (7. karar açık iş listesidir). Altı ret (R1-R6) uygulanmadı. Açık iş listesinde 14 kalem var (A14 bu turda M10.7 ile kapandı).

## 1. Ana oturum kararları

1. Başlık (main.tex:72): "Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design". Üstteki yoruma tarihli gerekçe eklendi (K-b(B9) +0.143, XCiT +0.20, r_RV +0.115; simetrik pay 0.936 ve 0.840). check_pdf_render başlığı main.tex'ten okuduğu için kendiliğinden yeni başlıkla geçti.
2. "Necessary condition" her yerden kalktı: özet, 01:42, 03:265 (iki cümle), 04:432, 04:443, Şekil 7 altyazısı (04:478), 05:21, 06:14. Yeni çizgi "associated with similarity as a gradient-alignment account requires, but not evidence of a mechanism". R18-R50 çifti sayısız karşı örnek olarak üç yerde: 01:42 ("a near-zero cosine can coexist with high similarity"), 04:443 ("smallest cosine of the ImageNetV2 matrix, yet its transfer similarity is high"), 05:73. Karar: 05:72 için birleşik raporun önerdiği "the cosine is not a necessary condition" kalıbı yerine "a near-zero cosine does not rule out similar transfer" yazıldı, çünkü 2. karar ifadeyi olumsuz biçimiyle de kaldırıyor. "En küçük kosinüs" sayısız nitelemedir (FOY:M10.5:2011, 0.003); log τ̄ −0.936 föyde olmadığından yazılmadı (A4).
3. Özet (main.tex:132) yeniden kuruldu, 249 kelime: K-b(B9) "refuted (+0.143): there the ViT is also a directionally weaker source"; sıfırdan ViT'nin düşük temiz doğruluğu "a contrast confounded with its lower clean accuracy" yan cümlesiyle tek yerde; aralık türü "90% intervals over training runs, conditional on test images and panel"; "two or three runs per cell"; "seven robust ResNet-family CNNs"; H3 "averaged over initialization"; gradyan cümlesinde "net of additive model effects". Karar: birleşik rapordaki taslak gerçekte 291 kelime çıktı (elle sayımla 249 denmişti); 250 sınırı için K-c (Δ_seed +0.566), H2 aralığı, AutoAttack farkı parantezi ve 4.36/19.37 cümlesi özetten çıktı, çünkü dördü de gövdede (IV-C, IV-D, IV-E, katkı 4) duruyor ve iddia sınırını taşıyan cümleler (K-b çürütmesi, karıştırıcı, logit) önceliklidir.
4. "Three seeds" yalnız C1 çifti ve CIFAR-100 çifti için kaldı (03:28, 03:197, 04:150, tab:panel_tests); 01:19 "Six new runs, two per cell"; özet "two or three runs per cell". S1 köprüsünün Welch altında eşdeğer olmadığı 04:230 (Welch %90 [−0.120, +0.119], FOY:M9.4:1561) ve 05:60'ta yazılı.
5. Gösterim: ImageNetV2 için `\Ak{\sigma}{k}`, `\Ak{\rho}{k}`, `\Ak{\omega}{k}` (çift k), `\AbarIN` ve `\Asig{scr,Liu}` (macros_konsey.tex:13-14; tanım 03:199); `\Asig{scr}` artık yalnız CIFAR-10 H1. A^ω tanımlı. Pearson korelasyonu `r_{\mathrm{P}}` (04:533, 07:146); tab:external_pool'daki çıplak r sütunu kalktı. ω ve L_k birimi 03:168 ("Rates enter the logarithm in percent ... additive constant log 100 that cancels from every contrast") ve tab:cells altyazısı ("ω = log w with w in %").
6. Atıf bağlamları: (a) Awad 02:35 "report, for a zoo of 36 CNNs and ViTs evaluated on ImageNet, that adversarially trained surrogates transfer better than standard ones in all four directions"; (b) Demontis 02:35 "alongside the complexity of the surrogate", 03:150 "close to two of the three factors of Demontis et al. ... their third ... absorbed as Proposition 1(d) describes", 05:21 ve 05:68 aynı çizgide; (c) Smouse 03:265 "in the spirit of the partial Mantel test, with all model main effects removed at once", 02:45 "the idea behind the residual statistic"; (d) 05:60 Mo ("depends on pre-training on small datasets") ile Debenedetti ("robust transformers have been trained with dedicated recipes") ayrıldı; (e) PubDef 02:37 "records transfer across 24 source models"; (f) 04:432 "The symmetric term thus tracks input-gradient alignment ... also after additive model main effects are removed; the family block structure remains (below)".
7. Bu turda sayı girmeyen çözümlemeler §4'te açık iş olarak listelendi; metindeki "not produced" cümleleri (03:336, tab:panel_tests dipnotu) olduğu gibi kaldı.

## 2. Uygulanan bulgular

Sarı:
- B1 (karıştırıcı): özet; 03:280 O1 cümlesine "here also because the design does not separate architecture from convergence in the scratch row"; 04:233 "argues against reducing ..." → "carries no interval here, is consistent with a dissimilarity that does not reduce to accuracy alone"; 05:19 ve 05:21 daraltıldı. Fark sayısı −0.104 yazılmadı (A2).
- B2 (zayıf kaynak): başlık; "weak source" 01:16'da tanımlandı ("examples transfer poorly to third models, a quantity distinct from the asymmetry within the pair") ve 03:172'de G'ye bağlandı; K-b(B9) özet, 01:28, 04:150, 05:19, 06:14'te "refuted / directionally weaker source"; 05:33 "+0.115, above the margin"; 03:334 "the CIFAR-100 refutation also follows from the original one-sided rule" (% FOY:M10.2:1842).
- B3: yukarıda karar 2.
- B4 (metin kısmı): özet aralık türü; 04:71 "so the run-level intervals below, which hold the images fixed, do not include this component".
- B5 (metin kısmı): özet "net of additive model effects"; 04:432 "the family block structure remains (below)".
- B6 (metin kısmı): özet ve 01:32 saldırı adları ve uyarlanmış TGR; 05:21 "not validated against its published gain"; 05:68 "without a check that the adaptation reproduces its published gain ... input diversity, more steps or the self-ensemble of Naseer et al. were not run"; 06:12 "adapted token gradient regularization".
- B7: özet, 01:32 ("averaged over the two initializations ... does not imply a small directional term in every cell"), 06:12 ("averaged over initialization ... within the margin").
- B8: 04:492 "The sign reverses ... H3 reverses in the same way" → "These values are large and negative on both datasets ... on CIFAR-100 this reverses a positive log estimate. H3 is −0.087 on the logit scale, inside the band but with a 95% interval that excludes zero, so the registered rule would be undecided there"; Şekil 10 altyazısı (04:504) "large and negative"; 06:14 "large and negative". Karar: birleşik rapordaki "H3 also changes sign" yazılmadı, çünkü log H3 +0.003 sıfıra eşdeğerdir ve B8'in kendi gerekçesi işaret dönüşü dilini böyle kestirimler için yasaklar.
- B9 (metin kısmı): Önerme 1(d) (03:176, kanıt cümlesi 03:179); 03:168 "σ_m also takes up half of any model main effect not captured by w"; 03:172 "A pure source effect gives q = 1/2, the null value of K-a"; 01:28 "against one half for a pure source effect"; 04:146 K-c cümlesi ("A general weakness of the ViT as a source would also lower the similarity between ViT seeds ..."); 02:37 ve 05:21'de kaynak ana etkisinin r ve log τ̄'ya bölünüşü. 2q − 1 yazılmadı (A9).
- B10: özet; 01:19 örneklem dışı ayrımı ("Those for the new two-by-two cells, the CIFAR-100 replication, the ImageNetV2 panel and the gradient tests are out of sample, whereas the CIFAR-10 panel tests extend a first seed that had been seen"); S1 Welch (karar 4).
- B11 (metin kısmı): 03:195 "seven L∞-robust CNNs of the ResNet family, four of them (PreAct) ResNet-18 variants"; özet ve 05:19 "ResNet-family CNNs"; 04:497 "For this ViT-Tiny ... against this panel of robust ResNet-family CNNs".
- B12: karar 6 (a), (b); 02:37 sonuna "That separation is a parameter-free identity on measured rates ... a source main effect enters the directional remainder as a potential and the shared similarity with half weight (Proposition 1)"; 05:21 Awad cümlesi "in contrast to source-quality effects such as the better transfer of robust surrogates, which the directional term bounds on this panel". Awad, Springer ve Zhang anahtarları atıf turunda doğrulanmış sayıldı, .bib'e dokunulmadı.
- B13, B14 (metin kısmı): karar 5.
- B16: 03 alt bölüm sırası değişti: Threat Model → Attack Methods → Adversarial Training → Architecture-by-Initialization Design → Vulnerability, Similarity and Direction (03:127) → Reference Panels → Conditioning Protocols (03:206) → Input-Gradient Alignment → Statistical Inference → Pre-Registration. T_ij ve w_j tanımı eski subsec:metrics'ten ayrışım alt bölümünün başına taşındı; subsec:metrics etiketi korunarak başlığı "Conditioning Protocols" oldu; 04:19 T_ij göndermesi subsec:decomposition_def'e çevrildi. Derlenmiş PDF'te tanımlanabilirlik artık Proposition 1, h ölçeği Proposition 2. L_k ve G_k tanımı Attack Methods'tan (03:65) G tanımının ardına (03:172) indi; Attack Methods'ta seçim kuralı ve gönderme kaldı. Karar: ayrışım ve paneller tasarımın ardına konuldu, tasarımın önüne alınmadı, çünkü birleşik rapor yalnız subsec:metrics'ten önce olmasını istiyor ve tasarım alt bölümü σ ve ρ'ya zaten denklem göndermesiyle bağlanıyor.
- B17: özette Δ_seed, w, τ̄ ve r sembolleri yok; "PGD-10 gaps" parantezi çıktı.
- B18 (kısmi): "necessary condition" tekrarları B3 ile gitti; 03:28 genel bakış paragrafı ve 03:172 kısaltıldı; 04:56'daki eski çift cümlesi silindi (m17).

Yeşil:
- m1: 03:277 "it is registered for log quantities, so logit and ratio comparisons against the same band are descriptive"; 04:225; Şekil 10 altyazısı. Gri bandın yalnız log satırlarına çizilmesi şekil ajanında.
- m2: 0.864 cümlesi dipnota taşındı (04:384); 04:495 "Against a single transformer reference, without an interval"; 04:497 Singh cümlesi betimsel.
- m3: 06:12 "the registered AutoAttack rule flags none of the six new models".
- m4: 03:277 "For the σ contrasts (H1, H2, K-c) the same margin is a convention without a separate empirical basis"; 03:280 karar ilkesi "refutation, and the equivalence arms of H1 and H2, from raw intervals; equivalence support for K-b and H3 from Holm-adjusted TOST p".
- m5: 04:372 "largest difference of 0.95 points ... among the fourteen models in the matrix (1.20 for an unused reserve)" (% FOY:M10.1:1814, 1816, 1818); 05:73 "at most 0.95 points ... for the models in the matrix".
- m6: Şekil 10 altyazısı "ImageNetV2 intervals cover image sampling only and are not comparable with the run-level intervals above".
- m7: 04:150 SVHN yan cümlesi bağlam olarak ("the pair's target-correct asymmetry itself changes sign at closely matched clean accuracy").
- m8: 05:19 "on CIFAR-10 and the log scale"; 05:21 "For a scratch-trained ViT-Tiny like ours".
- m9 (makale tarafı): 05:33 "Part (b) holds on any additive scale, including the points scale of that fit"; 01:48'e "(Section IV-I, Table 5)" göndermesi.
- m10: 03:53 ve Tablo I (04:44-45) 5.5M; kaynak yorumu `_ek_flop_olcumu.json` (param_M 5.53).
- m11: 04z:15 "The registered CIFAR-100, ImageNetV2 and gradient blocks reused existing checkpoints and trained no new model."
- m12: 05:38 "on the log scale, in an exploratory secondary analysis".
- m13: tab:registry'de q̄ → q (q_s tohum değeri, q ortalama; 03:172'de tanımlı); aile sembolleri "Panel, CIFAR-10", "Two-by-two, CIFAR-10", "Panel, CIFAR-100", "Gradient, three datasets"; H10 ve H10k korundu, altyazıya "keep the labels of the addendum", tab:mantel altyazısına ve 04:432'ye H10/H10k eşlemesi. Karar: etiketler tab:mantel'e sütun olarak değil altyazıyla kondu, çünkü tek sütunlu tablo taşıyordu.
- m14: tab:main_results, tab:protocol_settings ve Ek tablolarında "mean±SD"; tab:panel_tests, tab:fb4 ve tab:mantel'de p değerleri a×10^−b biçiminde (K-b CIFAR-100 Holm p 0.953).
- m15 (altyazı kısmı): Şekil 7 altyazısı "raw in (a) to (c) and with additive model main effects removed from both matrices in (d) to (f)". Şematik ve CIFAR-100 etiketleri şekil ajanında.
- m17: tab:external_pool'un eğim alt bloğu kaldırıldı, eğimler IV-I metnine taşındı (04:533; % FOY:RobustBench havuzu:1006,1007); 04:67 göndermesi tab:pair_decomposition'a çevrildi; 04:56 tekrarı silindi.
- m18: 01:32 "The third contribution is an intervention on the pair itself."

A14 (ana oturum kararıyla bu turda kapandı): 07:139 "Over three attack seeds on the first 1,000 test images of one seed pair, robust accuracy has a standard deviation of 0.05 points for the CNN and 0.00 for the ViT" (% FOY:M10.7:2049,2050; artefakt alanı np.std ddof 0, föy uyarısı yorumda); 07:146 "(36.15 and 36.36%)" (% FOY:M10.7:2058,2060,2062). İki TODO(foy) yorumu silindi.

Biçim için yapılan altyazı kısaltmaları (içerik değişmedi, derlemede float sayfası taşmasını gidermek için): Tablo 7 (tab:panel_tests; "Sensitivities in the lower block do not change decisions" düştü, δ satırı aynı bilgiyi veriyor), Tablo 8 (tab:cells; 29.14±0.40 altyazıdan çıktı, Tablo I'de duruyor), Tablo 9 (tab:fb4), Tablo 10 (tab:attack_side), Tablo 11 (tab:imagenet), Şekil 3 ve Şekil 7 altyazıları; tab:panel_tests tabcolsep 2.5→2.2 pt, tab:mantel 2→1.5 pt.

## 3. Reddedilenler (uygulanmadı)

- R1: Ön kayıt beyan paragrafı eke taşınmadı; gövdede kaldı (03:334-336).
- R2: Giriş katkılarındaki sayılar teke indirilmedi; yalnız 01:32'deki saldırı ve maskeleme ayrıntısı kısaltıldı.
- R3: ω ve L_k oran ölçeğine çevrilmedi; birim notu yeterli sayıldı.
- R4: "Necessary condition" Taylor argümanıyla korunmadı.
- R5: H10 ve H10k yeniden adlandırılmadı.
- R6: 04:372'deki "every candidate" ifadesi hatalı sayılmadı; yalnız açıklama eklendi.

## 4. Açık işler

| No | İş | Durum |
|---|---|---|
| A1 | Doğruluğu eşleşmiş sıfırdan ViT hücresi (GPU, ek ön kayıt) | açık |
| A2 | Föy eki M9.10: σ(V-IN) − σ(R224-IN) (−0.104), ρ basit etkileri (+0.070, −0.064), ρ etkileşimi (−0.134) birleşik varyanslı aralıklarıyla | açık; metin sayısız |
| A3 | σ'nın temiz doğruluğa masa regresyonu, V-scr'nin CNN eğilim çizgisinden sapması | açık |
| A4 | Salman R18-R50: c 0.0034 ve log τ̄ −0.936 föye | açık; metin sayısız (karar 2) |
| A5 | K-a ve K-b hiyerarşik bootstrap, CIFAR-10 ve CIFAR-100 (B = 2000), tab:panel_tests duyarlılık satırı | açık (karar 7) |
| A6 | S10-3 aile göstergeli kısmi Mantel, aile içi kısıtlı permütasyon, 11_sonuc §7'deki aile ayıklamalı (0.905, 0.892, 0.888) ve yalnız CNN-CNN Spearman (0.963, 0.929, 0.843) föye; tab:mantel'e satır | açık (karar 7) |
| A7 | TGR uyarlamasının temiz ViT-Tiny'de yayımlanmış yönü verdiğinin doğrulanması (kısa GPU) | açık; 05:68 sınırlılık cümlesi önceden yanıtlıyor |
| A8 | Genişletilmiş saldırı kümesi (Naseer self-ensemble, PNA, DI/TI 50 adım) | açık |
| A9 | Türetilmiş 2q − 1 satırı | açık |
| A10 | ResNet-18 türevleri çıkarılmış üç üyeli panelle q, ρ(V-scr), H1 | açık |
| A11 | Tezdeki AS1 yanıtının hizalanması | tez oturumu |
| A12 | Şekil yazı boyutu ≥ 6.5 pt, genel bakış oku | visio-cizici |
| A13 | Gönderim paketi: düz şekil yolları, ikinci yazar biyografisi | gönderim turu |
| A15 | Kapı ve brif: check_manuscript_claims'te "necessary condition" korumalı listede yok (denetlendi, ek iş gerekmiyor); check_pdf_render yeni başlığı main.tex'ten okuyor ve geçti; brif §2 B10 satırı, §8.1 m.6 (1.20 → 0.95) ve m.7 düzeltmesi ana oturumda | kısmen kapandı |

Şekil ajanına kalanlar (paper/figures bu yazara kapalı): B15 (fig_similarity_matrix renk çubuğu biçimi, fig_source_gap_split göstergesinde D → G ve negatif yönlü payın çizimi), B14 eksen notları ("w in %", fig_cells_interaction (c) ve fig_attack_side), m1 (fig_estimates_forest gri bant yalnız log satırlarında), m15 şekil kısmı (şematik (a)-(d), ⟨·⟩_P, CIFAR-100 etiketleri "ViT (C100)", "ResNet (C100)"), m16 (fig_protocol_sets terimleri). Şematik altyazısı (03:156) şekil değişene kadar "overline" demeye devam ediyor; şekil ⟨·⟩_P'ye geçince altyazı da değişmeli.

## 5. Derleme ve kapılar

- `bash scripts/derle_en.sh`: 25 sayfa, 0 hata, "tanımsız" sayacı 1 (bu satır `T1/pcr/n/n` font uyarısıdır; tanımsız gönderme 0, tanımsız atıf 0; PDF'te "??" yok). Overfull: yalnız şablon kaynaklı olanlar (\maketitle 9.27 pt iki kez, \output sırasında 505 pt). Değişiklik öncesi sürüm aynı koşulda 24 sayfa ve aynı şablon taşmalarıyla derleniyordu; ara derlemelerde çıkan iki tablo taşması ve üç float sayfası taşması giderildi.
- `bash scripts/compile_check.sh`: LATEXMK_EXIT=0, undefined_refs=1 (aynı font satırı), özet 249 kelime.
- `check_manuscript_claims.py`: GEÇTİ, TOPLAM=45 KALAN=0.
- `check_abstract_body.py`: GEÇTİ; EN özette 20 sayı, gövdede bulunmayan 0; EN 249, TR 248 kelime.
- `check_pdf_render.py`: GEÇTİ (yeni başlık ilk sayfada, 25 sayfa).
- `check_pdf_typeset.py`: GEÇTİ.
- `verify_manuscript_numbers.py`: KALDI (beklenen; betiği başka ajan düzeltiyor). EN_EKSIK=27: 22 "ATIF EKSIK" (03:97 tab:design altyazısı ve 03:105-109 tasarım sabitleri 32, 64, 80, 100, 224, 1001, 1003, 1e-3, 1e-4, 0.05; 04:212 "80", 04:372 "2000", 04:519 "36", 07:44 ve 07:64 "500", 07:149 "40" ve "1.10"), 4 "ÜST SINIR" (04:54 p < 2e-84 ve p < 2e-120, 07:39 p < 1e-11, 07:153 p < 1e-57), 1 demet (07:149 43.17±1.10). Hepsi bu turda dokunulmamış metindedir; bu turda eklenen sayıların (M10.7, 0.95, Welch S1, havuz eğimleri) hiçbiri listede yok. B bölümü (manşet ve özet taşıyıcıları) EN EKSIK 0.

## 6. Sayfa ve kelime

Yorum satırları hariç (`arsiv/b2_yardimci/_mk_y1_kelime_say.py`), önce → sonra:

| Dosya | Önce | Sonra | Brif üst sınırı |
|---|---|---|---|
| main.tex | 651 | 650 | 720 |
| 01 | 1152 | 1269 | 1300 |
| 02 | 1076 | 1135 | 1450 |
| 03 | 3900 | 4187 | 3400 |
| 04 | 7534 | 7604 | 8000 |
| 04z | 238 | 244 | 300 |
| 05 | 1533 | 1692 | 1700 |
| 06 | 323 | 333 | 350 |
| 07 | 1384 | 1407 | 1500 |
| Toplam | 17791 | 18521 | 18720 |

Özet 249 kelime. PDF 24 → 25 sayfa. 03 dosyası tavanın üstünde kalmaya devam ediyor (önce de 3900'dü); artış Önerme 1(d), birim ve q okunuşu, ImageNetV2 gösterimi, δ kaydı, karar ilkesi ve K-b kural cümlesinden geliyor. R1 ön kayıt paragrafını taşımayı reddettiği için daha fazla kısaltma ancak tasarım ayrıntısının tab:design altyazısına alınmasıyla (sunum merceği önerisi) yapılabilir; bu turda yapılmadı.

## 7. TR aynası için değişiklik özeti

`paper/manuscript_tr/` bu turda değişmedi. Eşitleme turunda akademik-turkce skill'iyle şunlar aktarılmalı:

- Başlık: "Zayıf Bir Kaynaktan Çok Farklı Bir Kaynak: Mimari ve Başlatma Çaprazlamalı Bir Tasarımda CNN-ViT Çekişmeli Transferinde Kırılganlık, Benzerlik ve Yön" çizgisinde bir karşılık (son biçim TR turunun işi).
- Özet: K-b(B9) "çürütüldü; CIFAR-100'de ViT yönlü olarak da zayıf kaynaktır"; sıfırdan ViT'nin düşük temiz doğruluğu karıştırıcı yan cümlesi; aralık türü (eğitim koşuları üzerinden, test görüntüleri ve panele koşullu); "hücre başına iki ya da üç koşu"; "ResNet ailesinden yedi gürbüz CNN"; H3 "başlatma üzerinden ortalandığında"; "gerekli koşul" yok; K-c ve 4.36/19.37 cümlesi özetten çıktı.
- Giriş: zayıf kaynak tanımı; iki koşu/hücre; örneklem dışı ayrımı; "saf kaynak etkisi için yarım"; üçüncü katkının açılış kalıbı; H3 niteliği; TGR ve AutoAttack kuralı cümlesi; sınır paragrafında gradyan ilişkisi ve R18-R50 karşı örneği; 01:48 göndermesi.
- İlgili çalışmalar: Demontis'in üç etkeni, Awad'ın yeni bağlamı, PubDef "24 kaynak model", ayrışımın parametresiz özdeşlik olduğu cümlesi, Smouse cümlesi.
- Yöntem: alt bölüm sırası (ayrışım ve paneller protokollerden önce; T_ij tanımı ayrışımın başında; protokol alt bölümünün adı "Koşullama Protokolleri"); Önerme 1(d); ω ve L_k birimi; σ'nın yarım ana etki notu; G'nin zayıf kaynak tanımı, q_s ve q; L_k ve G_k G'nin ardında; ResNet ailesi ve dört ResNet-18 türevi; ImageNetV2 gösterimi (A^σ_k, A^ρ_k, A^ω_k, Ā^σ_IN, A^σ_scr,Liu); Smouse ve gradyan cümleleri; δ'nın log kaydı ve σ uzlaşımı; karar ilkesinin yeni biçimi; O1 cümlesine yakınsama niteliği; tab:registry aile adları, q ve H10/H10k notu; K-b kural değişikliğine özgün kural yan cümlesi; ViT-Tiny 5.5M.
- Deneyler: Tablo I 5.5M ve "ort±SS"; 04:56 cümlesi silindi; 04:67 göndermesi; 04:71 görüntü bileşeni cümlesi; tab:external_pool eğim bloğu metne; K-b paragrafına "CIFAR-10'da", K-c cümlesi; CIFAR-100'de "yönlü olarak da zayıf kaynak" ve SVHN yan cümlesi; p değeri biçimi; logit bant kaydı; S1 Welch; 04:233 cümlesi; tab:cells birimi; 0.95 ve yedek model; ImageNetV2 gösterimi ve 0.864 dipnotu; gradyan paragrafları (izler, aile blok yapısı, R18-R50); Şekil 7 ve Şekil 10 altyazıları; logit paragrafı (işaret dönüşü dili yok); XCiT cümlesi; "Bu ViT-Tiny için" sınır cümlesi; r_P; kısaltılmış tablo altyazıları.
- Hesaplama ayrıntıları: "kayıtlı bloklar mevcut kontrol noktalarını kullandı, yeni model eğitmedi".
- Tartışma: ResNet ailesi; "CIFAR-10'da ve log ölçekte"; CIFAR-100 çürütmesi; TGR doğrulanmamış uyarlama; Awad karşıtlığı; "bizimki gibi sıfırdan eğitilmiş bir ViT-Tiny için"; Demontis'in vekil karmaşıklığı terimi; Önerme 1(b) her toplamsal ölçekte; +0.115 bandın üstünde; Mahmood adayı keşifsel ve log ölçekte; S1 Welch; Mo ve Debenedetti ayrımı; TGR ve Naseer sınırlılığı; 0.95 puan; R18-R50 cümlesi.
- Sonuç: başlatma üzerinden ortalanmış H3; AutoAttack kuralı; CIFAR-100 çürütmesi ve "büyük ve negatif"; gradyan için "ilişki, mekanizma değil".
- Ek: "ort±SS"; saldırı tohumu SD'si 0.05 ve 0.00 puan; C3 hedef hataları 36.15 ve 36.36; r_P.

## 8. M11 geçişi (31.10.2026, akşam)

Föye M11 bölümü (satır 2069-2207; hiyerarşik bootstrap M11.1, S10-3 M11.2, keşifsel çözümlemeler M11.3) eklendikten sonra "föye girince metne" diye bekleyen sayılar metne alındı. Dokunulan dosyalar `sections/03`, `04`, `05`, `01` ve iki rapor dosyasıdır (`12_makale_revizyon_brifi.md`, `11_sonuc_b8_b10.md`); `main.tex`, özet, `references.bib`, `paper/figures/`, `scripts/` ve `results/` değişmedi. Değişiklik öncesi kopyalar oturum karalama klasöründe (`scratchpad/yedek_m11/`). Her yeni sayının üstünde `% FOY:M11.x:<satır>` yorumu var.

Metne giren sayılar ve föy satırları:

- Hiyerarşik bootstrap %90, K-a ve K-b (04, IV-C yeni paragraf ve `tab:panel_tests` duyarlılık satırı "Hier. bootstrap"): CIFAR-10 q [0.894, 0.981], ρ(V-scr) [−0.021, +0.046]; CIFAR-100 q [0.800, 0.880], ρ(V-scr) [+0.106, +0.178] (FOY:M11.1:2088, 2090, 2094, 2096); B = 2,000 (2082, 2084); karar değişmedi, iki veri kümesinde ve δ = 0.06'da (2105-2110, 2112, 2114); bootstrap p tabanı 1/(B+1), K-b CIFAR-100 dışında her sınama tabanda (2088-2098, 2112, 2114). İki sınırlılık birlikte yazıldı: t aralıkları görüntü örneklemesini içermez, üç koşuluk bootstrap koşu bileşenini küçük tahmin eder. Karar: %95 bootstrap aralıkları metne alınmadı, çünkü kararları %90 aralık ve Holm p taşıyor, tablo satırı da tek sütun genişliğine sığmıyordu.
- Üretimin ön kayıttan ve hakem panelinden sonra, dondurulmuş betik dışında yapıldığı ve uygulama düzeyinde sapma olarak kaydedildiği: 03 ön kayıt paragrafı (eski "Neither document has a deviation" cümlesinin yerine; FOY:M11.1:2078, 2080; ONKAYIT_SAPMALAR.md satır 67-87). `tab:panel_tests` dipnotu kısa gönderme taşır.
- S10-3 (aile göstergeli kısmi Mantel): `tab:mantel`'e üç satır, r +0.917, +0.882, +0.878, p 10⁻⁴, Holm ve karar sütunu "--"; altyazıda "registered as exploratory in the addendum, specified after the results were seen, and is outside the family" (FOY:M11.2:2121, 2131-2133). Aynı sayılar IV-G metninde.
- Keşifsel (IV-G): sıra ölçeğinde aile ayıklamalı artık Spearman 0.905, 0.892, 0.888 (FOY:M11.3:2182-2184); yalnız CNN-CNN artık Spearman 0.963, 0.929, 0.842 (2190-2192; 0.843 değil); aile içi kısıtlı permütasyonda altı sınamanın altısı permütasyon tabanında, kısıtlı sıfır dağılımı ortalamaları −0.008 ile +0.461 arasında (2171-2176).
- Salman R18-R50: c = 0.0034, 91 çiftte en küçük; log τ̄ = −0.936, alttan 55. sıra (FOY:M11.3:2200, 2202). GPU denetimi (13_b10_r18_r50_denetimi.md §6) sayısız yan cümle. Karar: "transfer similarity is high" ifadesi sıra 55/91 ile desteklenmediği için "above-median" oldu (01:42, 05:75); 04'te sıra sayıyla verildi.

Güncellenen cümleler (satırlar bu geçişten sonraki dosyalarındır):

- 03:332 ön kayıt beyanı (sapma ve S10-3 cümleleri); 03:337 "not produced" listesinden K-a/K-b hiyerarşik bootstrap çıktı.
- 04:153 "The sensitivities in the lower block ... Section IV-H" cümlesi kalktı; 04:157 yeni bootstrap paragrafı; 04:165 `tab:panel_tests` altyazısı ("the K-c bootstrap and the hierarchical-bootstrap row also resample images"); 04:185 yeni satır; 04:189 dipnot ("were not produced on CIFAR-10" yerine üretim ve sapma göndermesi).
- 04:438 IV-G ilk paragrafın son cümlesi ("also after additive model main effects are removed; the family block structure remains (below)" kısaldı, artık bir sonraki paragraf blok yapısını sayılarla ele alıyor); 04:448 blok yapısı, S10-3, keşifsel çözümlemeler ve R18-R50 paragrafı yeniden yazıldı; iddia "associated with similar transfer but is not evidence of a mechanism" sınırında kaldı; 04:454 `tab:mantel` altyazısı; 04:468-470 S10-3 satırları.
- 05:61 sınırlılıklar: "binding panel intervals hold the test images fixed; a hierarchical bootstrap ..., produced after the results were seen, changes no decision, though over three runs per cell it understates the run component"; 05:75 gradyan sınırlılığı ("the analyses that also control the family split were specified after the results were seen"; R18-R50 cümlesi kısaldı ve IV-G'ye gönderiyor).
- 01:42 "high similarity" → "above-median similarity".
- 06 ve 07: değişmedi. 06:14'teki "an association a gradient-alignment account requires, not a mechanism" cümlesi yeni çözümlemelerle uyumlu; 07'de hiyerarşik bootstrap ya da "not produced" cümlesi yoktu.

Kelime tavanı için kısaltılanlar (içerik başka yerde duruyor): 04 IV-H "What survives" paragrafı tek cümleye indi; 04 IV-H'deki H3 logit cümlesi (IV-D'de aynısı var); 04 IV-D "band is registered only for log quantities" yan cümlesi (03 ve Şekil 10 altyazısında var); 04 IV-D "The secondary analyses are exploratory and uncorrected" (03'te var); 04:75 "These values shaped the predictions" cümlesi birleştirildi; 05:19 CIFAR-100 ve logit cümlesi sıkıştı; 05:33 Önerme 1 açıklaması kısaldı (04:67'de var); 05:61 V-scr temiz doğruluk sayıları ve tekrar eden yakınsama cümlesi tek cümleye indi (sayılar IV-D ve `tab:cells`'te); 05:69 "Equivalence of the architecture main effect therefore does not mean ..." (04 H3 paragrafında var); 05:75 Mahmood cümlesi (05:38'de var).

Kapanan açık işler: A4 (R18-R50 sayıları föyde ve metinde), A5 (K-a ve K-b hiyerarşik bootstrap, tablo satırı ve metin), A6 (S10-3, aile içi kısıtlı permütasyon, aile ayıklamalı ve yalnız CNN-CNN Spearman; 0.842 düzeltmesi), A15'in kalan kısmı (brif §2 B10 satırı, §8.1 m.6 ve m.7 düzeltildi). A2 (σ(V-IN) − σ(R224-IN) ve ρ basit etkileri), A9 (2q − 1 satırı) ve A10 (ResNet-18 türevleri çıkarılmış panel) M11'de yok; föye girmedikleri için metin sayısız kaldı ve bu işler açık kalıyor. Karar: görev metni A2, A9 ve A10'u da kapanacaklar arasında sayıyordu, ama M11 bu üç çözümlemeyi taşımadığından kapatılmadı.

Derleme ve kapılar: `derle_en.sh` 25 sayfa, 0 hata, tanımsız sayacı 1 (font satırı); taşmalar yalnız şablon kaynaklı (\maketitle 9.27 pt iki kez, \output 505 pt), yeni tablo satırlarının ilk denemede açtığı iki küçük taşma (1.0 ve 2.5 pt) giderildi. `compile_check.sh` LATEXMK_EXIT=0, undefined_refs=1. `check_manuscript_claims` GEÇTİ (45/0), `check_abstract_body` GEÇTİ (EN 249 kelime, 20 sayı, eksik 0), `check_pdf_render` GEÇTİ, `check_pdf_typeset` GEÇTİ. `verify_manuscript_numbers` KALDI, EN_EKSIK=27, hepsi önceki turdaki listeyle aynı kalemler; bu geçişte eklenen sayıların hiçbiri listede yok. Kelime (yorumlar hariç) 18,521 → 18,716 (tavan 18,720); 03 4,187 → 4,234, 04 7,604 → 7,790, 05 1,692 → 1,654.

TR aynası (`paper/manuscript_tr/`) bu geçişte de değişmedi; eşitleme turunda yukarıdaki maddeler aktarılmalı.


## 9. Son geçiş (M12, şekil istekleri, sayı kapısı)

### 9.0 ViT-Tiny yapılandırma kaydı (03:55'teki KAYNAK yorumunun belgesi)

ViT-Tiny'nin mimari boyutları depodaki hiçbir belgede yazılı değildi; 31.10.2026'da konteynerde (`adeb_eval`, timm 1.0.27) `timm.create_model('vit_tiny_patch16_224', pretrained=False, num_classes=10)` kurularak okundu. Çıktı: patch_size 16 (16 × 16 yama), img_size 224, depth 12 (blok), embed_dim 192 (genişlik), num_heads 3 (baş), parametre sayısı 5526346 (on sınıflı başlıkla; metindeki 5.5M ile ve `_ek_flop_olcumu.json` içindeki param_M 5.53 ile uyumlu). Girdi 32 piksellik CIFAR görüntüsünün 224'e bilinear büyütülmesidir (ON_KAYIT §3).

### 9.1 M12 sayıları metne (A2, A9, A10)

Föyün M12 bölümündeki (satır 2209-2375) üç keşifsel çözümleme metne alındı. Her yeni sayının üstünde `% FOY:M12.x:<satır>` yorumu var; üçü de ön kayıt dışıdır ve ONKAYIT_SAPMALAR.md satır 89 ve sonrasında kayıtlıdır. Gövdeye her iş için en çok iki cümle girdi, tablolar yeni Ek D'dedir (`app:exploratory`, "Exploratory Re-Analyses of the CIFAR-10 Families").

A2, yani 2x2 tasarımın basit etkileri: 04 IV-D'de V-IN ile R224-IN karşılaştırması paragrafının son cümlesi değişti. Eski "carries no interval here" cümlesinin yerine σ(V-IN) − σ(R224-IN) = −0.104, birleşik varyanslı %90 [−0.159, −0.049] (FOY:M12.1:2229) ve aynı cümlede Welch %90 [−0.318, +0.109] aralığının sıfırı içerdiği (FOY:M12.1:2246) yazıldı; cümle "points to a dissimilarity beyond accuracy only under pooled variances" ile biter. Bootstrap aralığı anılmadı, "significant" yok. H3 paragrafına tek cümle eklendi: ρ mimari basit etkileri +0.070 (sıfırdan) ve −0.064 (ImageNet), farkları yani etkileşim −0.134 log ve logit ölçekte negatif, basit etkilerin işaret ayrışması yalnız log ölçekte (FOY:M12.1:2234, 2235, 2238; logit 2251, 2252, 2255: −0.061, −0.112, −0.051). "Crossover" ya da "sign-changing interaction" denmedi. Ek D'de `tab:simple_effects` (Tablo XVII): σ ve ρ için dört basit etki, etkileşim ve ana etki; kestirim, birleşik varyanslı %90, Welch %90 ve logit kestirim sütunları (FOY:M12.1:2228-2239, 2245-2256). Karar: tabloya hiyerarşik bootstrap ve keşifsel Holm sütunları konmadı, çünkü görev tanımı istemiyordu ve tablo sütun genişliğine ancak bu beş sütunla sığıyor.

A9, yani 2q − 1: 04 IV-C K-a paragrafının sonuna "In terms of the derived quantity 2q − 1, the symmetric part exceeds the directional part by 0.873 of the gap ([0.849, 0.896])" (FOY:M12.2:2290); `tab:panel_tests` (Tablo VII) duyarlılık bloğuna "2q−1, derived" satırı: CIFAR-10 +0.873 [+0.849, +0.896], CIFAR-100 +0.679 [+0.589, +0.769] (FOY:M12.2:2290, 2291), tablo dipnotuna "2q−1 is a linear transform of K-a, not a test". Karar: satır Tablo V'e (`tab:pair_decomposition`) değil Tablo VII'ye girdi, çünkü 2q − 1 K-a'nın, yani panel sınamasının dönüşümüdür ve Tablo V çift düzeyi ayrışımı taşır.

A10, yani ResNet-18 türevleri çıkarılmış panel: 04 IV-D'de H1 duyarlılık paragrafının sonuna tek cümle: üç üyeli keşifsel panelde altı CIFAR-10 sınamasının yönü ve kararı ile O1 sonuç bölgesi değişmiyor, büyüklükler benzer (Ek D). Karşılaştırmalı yargı ("panel etkiyi küçültmüştü" türü) yok. Ek D'de `tab:reduced_panel` (Tablo XVIII): yedi ve üç üyeli panel yan yana, kestirim ve %90 aralık, karar sütunu, sonuç bölgesi satırı; altyazıda H2 logit kestirimi +0.390 (FOY:M12.3:2335-2340, 2344, 2345, 2351-2356, 2362-2368). Sayılar: H1 −0.412 [−0.465, −0.359], H2 +0.295 [+0.216, +0.373], H3 +0.004 [−0.021, +0.029], K-a 0.921 [0.905, 0.936], K-b +0.018 [−0.008, +0.044], K-c +0.673 [+0.641, +0.714]. Karar: altı kestirim gövde cümlesinden çıkarıldı ve yalnız Ek D tablosunda duruyor, çünkü kelime tavanı ancak böyle tuttu; gövde cümlesi Ek D'ye gönderiyor. Tartışmada (05:69) sınırlılık cümlesi eklendi: yedi üyenin dördü ResNet-18 türevi, onlarsız keşifsel denetimde karar değişmiyor, ama panel ResNet ailesinin içinde kalıyor (IV-D'ye gönderme).

A4'ün kalan maddesi, yani K-c p değerinin "p = 5.0e-4" biçimi: metinde böyle bir yazım yoktu (K-c tablo satırında yalnız Holm p 1.00×10⁻³ var; 04:158 bootstrap p tabanını zaten "bounded below by 1/(B+1)" diye anlatıyor). Değişiklik gerekmedi.

### 9.2 Şekil ajanının istekleri

03 şematik altyazısında "(overline: mean over panel members c∈P)" yerine "(⟨·⟩_P: mean over panel members c∈P)" yazıldı (03:162). 04'te `fig:protocol_sets` yolu `../figures/konsey/fig_protocol_sets.pdf` oldu (04:578). Altyazıda "endorsed pair" ve "different estimand" geçmiyordu; şeklin v5 bağlayıcı etiketleriyle uyum için altyazının son cümlesi "Connectors label the step between adjacent protocols: the identity term of Equation (raw_identity), the marginal subsets that both-correct removes, and the source robustness that successful-source selects on." oldu.

### 9.3 Sayı kapısı (verify_manuscript_numbers.py)

Başlangıçta EN_EKSIK = 83 (A3 atıf eksik 22, üst sınır 4, demet 1, yön denetlenemedi 3, KAYNAK değer eksik 18, KAYNAK belgede yok 1, grupsuz 34). Son koşuda EN_EKSIK = 0, SONUC GECTI (116 grup, 976 satır atfı; B manşet ve özet 57 kalem, eksik 0). Yapılanlar:

- Tasarım tablosu (03:103 `tab:design`): KAYNAK yorumuna ON_KAYIT §3'te yazılı değerler açıkça eklendi (32, 224, 1e-4, 0.05, 1e-3, 64, 100, 20, 80) ve R32 tohumları için `scripts/run_c1_pipeline.sh` (1001-1003).
- Eğitim paragrafı (03:82, önceden grupsuz): KAYNAK yorumu `scripts/run_c1_pipeline.sh` (200 epok, lr 0.1, batch 128, AT 100 epok, lr 1e-3, ViT batch 64, sabır 20, tohumlar), `src/training/trainer.py` (weight decay 5e-4 ve AdamW 0.05), `cli/train.py` (grad-clip 10), `experiments/rev2/make_val_split.py` (2000, tohum 777), CLAUDE.md (min_delta 0.1).
- ViT-Tiny boyutları (03:55): §9.0'daki konteyner okuması ile ON_KAYIT §3.
- 03:121 (yüzde 15), 03:166 paragrafı (log 100, ON_KAYIT §2), 03:205 (FOY:M10.1:1826), 03:210 (FOY:M10.1:1820, 1827 ve EK §5.2-5.5: 256, 224, 1000, 25, 0.6), 03:221 (`scripts/q1_e2_conditional.py`, --n-boot 10000), 03:277 (FOY:M10.5:1970, 9999 ve 1e-4), kayıt tablosu (03 `tab:registry`: eşikler ON_KAYIT ve EK'ten açıkça; `% YON: kural`).
- 02:37 (PubDef 24 kaynak model ve 2017-2026 tarama aralığı): KAYNAK yorumu `06_ek_deney_literatur.md` ve `02_literatur.md`.
- Atıf eksikleri: 04:220 (FOY 1485, 80 epok tavanı), 04:384 (FOY:M10.1 yorumu tek listeye çevrildi; 2000 de cümleden çıktı), IV-I özdeşlik paragrafı (FOY:M8.1:1153, 36 yön), 07:40 ve 07:45 (FOY:M8.10:1321, n = 500; "eski metin" adlı KAYNAK'tan "n = 500" kaldırıldı), 07:65 (FOY:C5:125), 07:151 (FOY:Turetilmis:229, 43.17 ± 1.10 demeti; bant 33-40 için `results/q1_research/E1_PILOT_KAPISI.md`), `fig:epsilon_sweep` altyazısı (FOY:Epsilon taramasi:371, 373; 0.08).
- Üst sınırlar: 04:54 "p < 2×10⁻⁸⁴" ve "p < 2×10⁻¹²⁰" yerine föyün kesin en büyük değerleri "p ≤ 1.2×10⁻⁸⁴" ve "p ≤ 1.9×10⁻¹²⁰" (föy 43, 45); 07:40 "Holm p < 10⁻¹¹" yerine "Holm p ≤ 2.2×10⁻¹²" (föy 95); 07:155 "p < 10⁻⁵⁷" yerine "p ≤ 2.729×10⁻⁵⁸" (föy 1338, 1341). Karar: föyün 1341. satırındaki "p < 10^-57" yazımı kapının belirteç çözümleyicisinde 10⁻⁵⁷ olarak okunmadığı ve föy bu turda değiştirilemediği için kesin değer yazıldı; dört anlamlı basamak bu yüzden.
- Yön: 04 H3 paragrafına `% YON: [-0.116; -0.058] FOY:M9.4:1551` (logit H3 %95 aralığı).

### 9.4 Kelime tavanı için kısaltılanlar (içerik başka yerde duruyor)

Eklenen M12 içeriği (gövde yaklaşık 170, Ek D yaklaşık 420 belirteç) kadar kısaltıldı. 01: son yol haritası paragrafı ("Section II reviews ...") silindi. 03: genel bakış paragrafındaki bölüm göndermeleri; Gowal WRN-28-10 referans cümlesi (Tablo IV dipnotu ve 05:50'de var); Demontis cümlesi kısaldı; "The panel is what makes source and target roles identifiable"; ImageNetV2 görüntü seçiminde "in lexicographic order"; gradyan alt bölümünün son yorum cümlesi (04 IV-G ilk cümlesinde ve 05'te var). 04: giriş paragrafı sıkıştı ve "Cell names follow Table I" çıktı; 04:54'te "(85.78 against 73.53%)"; 04:57 WRN 62.76 cümlesi (05:50'de var); 04:71 son kontrol noktası payı (Tablo V'te) ve görüntü bootstrap cümlesi kısaldı; 04:75 jackknife aralığı 0.919-0.935; K-c paragrafının son iki cümlesi sıkıştı; CIFAR-100 tekrar cümlesi ve "restricted to CIFAR-10" cümlesi (04:511 ve 05:19'da var); 04:154 açılış cümlesi; 04:158 ilk cümle (03 ve tablo altyazısında var); `tab:panel_tests` dipnotundaki CIFAR-100 temiz doğrulukları (04:154 ve 05:69'da var); 04:223 açılışı; 04:241 köprü cümlesi kısaldı; TGR uyarlama cümlesi (03:63, 05:21, 05:69'da var); tasarım çiftleri cümlesi birleşti; ImageNetV2 saldırı ayrıntısı (03:210'da var); Singh özet cümlesi; IV-G'de "tracks input-gradient alignment" sonuç cümlesi ve Zhang tekrarı; karışık çift cümlesi kısaldı; log ölçek gerekçesi kısaldı; δ = 0.06 tekrar cümlesi (04:227 ve tablolarda var); şekil altyazıları (`fig:source_gap_split`, `fig:cells_interaction`, `fig:attack_side`, `fig:estimates_forest`) ve `tab:imagenet` altyazısındaki A_k tanımı (03:210'da var). 05: 05:61 Welch cümlesi kısaldı; 05:69 CIFAR-100 sayıları ve son "accounting identity" cümlesi (03:156 ve 05:21'de var); 05:75 R18-R50 frekans ayrıntısı (04:454'te var); 05:83 maliyet göndermesi kısaldı. 07: 07:125 TGR cümlesi birleşti; 07:140 χ² aralık sayıları (0.8-9.9, 5.2-32.6) çıktı; 07:155 L2 cümlesinin "probes the protocol" yan cümlesi (05:75'te var).

### 9.5 Derleme ve kapılar

`derle_en.sh`: 25 sayfa (değişmedi), 0 hata, tanımsız sayacı 1 (yalnız T1/pcr yazı tipi uyarısı; tanımsız gönderme ve atıf 0). Taşmalar: şablon kaynaklı \maketitle 9.27 pt ve \output 505 pt; ayrıca \output sırasında sayfa 5'te 17.5 pt'lik bir vbox satırı var, sayfa görüntüsünde taşma yok ve `check_pdf_typeset` sütun taşması bulmadı (bu satırın önceki turda olup olmadığı yedek olmadığı için doğrulanamadı). Ek D'nin iki tablosundaki ilk denemede açılan 18.3 pt taşma satır etiketleri kısaltılarak giderildi. `compile_check.sh`: LATEXMK_EXIT=0, undefined_refs=1 (aynı yazı tipi satırı), overfull=54.

Kapılar: `verify_manuscript_numbers` GECTI (EN_EKSIK 0; TR_EKSIK 102, yalnız bilgi). `check_abstract_body` GECTI (EN özet 249 kelime, sayıların hepsi gövdede). `check_pdf_render` GECTI. `check_pdf_typeset` GECTI. `check_manuscript_claims` 45 denetimden 40'ı geçti; kalan beşi (C4, D2, F1, F2, I1) yalnız TR denetimleri, EN denetimlerinin hepsi geçti. `kapilar.sh` zinciri: öz-sınama, sayılar, özet, TR ondalık, PDF render, PDF dizgi GECTI; iddialar (TR kalemleri), bildiri, EN/TR ayna ve gönderim KALDI. Ayna kapısının tek farkı 01'in paragraf sayısıdır (EN 11, TR 12; bu turda silinen yol haritası paragrafı); gönderim kapısı kapak mektubu, öne çıkanlar, beyanlar ve kontrol listesinin yeni başlığı taşımamasından kalıyor. Bu dördünün TR eşitlemesi ve gönderim paketi güncellenene kadar kalması bekleniyor.

Kelime (yorumlar hariç): 18,716 → 18,718 (tavan 18,720). Dosya bazında: main 650, 01 1249, 02 1135, 03 4156, 04 7506, 04z 244, 05 1600, 06 333, 07 1845. Özet 249.

### 9.6 TR aynası için delta listesi

Satır numaraları EN dosyalarının bu geçişten sonraki halidir.

- 01: son paragraf (yol haritası, "Section II reviews related work ...") silindi; TR'de karşılığı silinmeli (ayna kapısının tek farkı bu).
- 02:36: yalnız KAYNAK yorumu eklendi, metin değişmedi.
- 03:28 genel bakış paragrafı kısaldı (bölüm göndermeleri yok). 03:55 Gowal WRN-28-10 cümlesi silindi. 03:156 Demontis yan cümlesi ("their third, surrogate complexity, is absorbed as Proposition 1(d) describes"). 03:162 şematik altyazısı: ⟨·⟩_P gösterimi. 03:179 son cümle ("The panel is what makes ...") silindi. 03:210 "in lexicographic order" silindi. 03:277 gradyan alt bölümünün son cümlesi "The additive fit leaves in place multiplicative or interacting model effects and the block structure of the CNN and transformer families." oldu. Ayrıca 03'e yalnız yorum satırları (KAYNAK, FOY, YON) eklendi.
- 04:19 giriş paragrafı kısaldı. 04:54 McNemar p'leri "p ≤ 1.2×10⁻⁸⁴" ve "p ≤ 1.9×10⁻¹²⁰"; "(85.78 against 73.53%)" silindi. 04:57 WRN 62.76 cümlesi silindi. 04:71 son kontrol noktası payı silindi, görüntü bootstrap cümlesi kısaldı. 04:75 jackknife aralığı silindi. 04:141 K-a paragrafına 2q − 1 cümlesi. 04:147 K-c paragrafının son iki cümlesi. 04:151 "K-b does not replicate"; CIFAR-100 tekrar cümlesi ve "restricted to CIFAR-10" cümlesi silindi. 04:154 açılış cümlesi silindi. 04:158 ilk cümle silindi. 04:183 `tab:panel_tests` yeni "2q−1, derived" satırı; 04:191 dipnot ("2q−1 is a linear transform of K-a, not a test"; CIFAR-100 temiz doğruluklar çıktı). 04:223 açılış. 04:231 A10 cümlesi. 04:236 ρ basit etkileri cümlesi. 04:241 köprü cümlesi ("This bridge, not the σ gap seen before registration, is what H1 tests"). 04:245 A2 cümlesi (−0.104, birleşik varyans ve Welch). `fig:source_gap_split`, `fig:cells_interaction`, `fig:attack_side` (04:372), `tab:imagenet` (04:403), `fig:estimates_forest` (04:518) altyazıları kısaldı. 04:336 TGR uyarlama cümlesi silindi, tasarım çiftleri tek cümle. 04:384 ImageNetV2 saldırı ayrıntısı Section III-F'ye gönderiyor. 04:387 Singh özet cümlesi silindi, "The result is the descriptive counterpart". 04:444 Zhang tekrarı ve son cümle silindi. 04:447 ImageNetV2 cümlesi "descriptively". 04:454 karışık çift cümlesi. 04:506 log ölçek gerekçesi kısaldı. 04:509 δ = 0.06 cümlesi silindi. 04:578 şekil yolu konsey kopyası; 04:579 altyazının son cümlesi (bağlayıcı etiketleri).
- 05:61 Welch cümlesi. 05:69 ResNet-18 türevleri sınırlılık cümlesi eklendi; CIFAR-100 cümlesi sayısız; son "accounting identity" cümlesi silindi. 05:75 R18-R50 örneği kısaldı. 05:83 maliyet göndermesi parantez içine.
- 07:40 Holm p "≤ 2.2×10⁻¹²". 07:125 TGR cümleleri birleşti. 07:140 χ² sayıları çıktı. 07:155 McNemar "p ≤ 2.729×10⁻⁵⁸", L2 yan cümlesi silindi. Yeni Ek D (07:157 sonrası): bölüm başlığı, bir paragraf, `tab:simple_effects` ve `tab:reduced_panel`.
