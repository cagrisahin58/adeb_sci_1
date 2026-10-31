# Mercek 3: sunum ve bicim (31.10.2026)

Bu rapor salt okur hakem ajaninin yapisal ciktisindan ana oturumca dosyaya aktarilmistir; metin ajanin kendi ifadeleridir.

Genel karar: KUCUK_REVIZYON

## Bulgular (siddet sirasiyla)

### 1. [sari] Gösterim çakışması: A^σ_scr ve A^ρ iki farklı nicelik için kullanılıyor

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: 04:386 "Its contrast is $\Asig{scr} = -0.055$"; 04:389 "the within-pair contrast $A^{\rho}$ is $-0.089$, $+0.110$ and $+0.091$"; 03:304 tab:registry satırı "$\Asig{scr}$, Liu pair"; tab:imagenet 04:425 "$\Asig{scr}$, pair 3".

Kanit: 03:116 \Asig{scr} = σ(V-scr) − σ(R224-scr) (H1, −0.364) ve 03:119-120 \Arho = iki satırın ortalaması olan mimari ana etki (H3, +0.003) diye tanımlanır. ImageNetV2'de aynı semboller tek bir Liu çiftinin transformer eksi CNN farkı (−0.055) ve çift içi ρ farkı için yeniden kullanılıyor. Özet ve giriş −0.364'ü A^σ_scr diye verdiği için okur iki değeri aynı niceliğin iki ölçümü sanabilir. tab:imagenet başlığındaki A^ω metinde hiç tanımlanmıyor.

Duzeltme: ImageNetV2 nicelikleri için ayrı alt indis kullanın: Liu çifti A^σ_{Liu} (ya da A^σ_{scr,IN-V2}), çift içi farklar A^σ_k, A^ρ_k, A^ω_k (k = 1, 2, 3); 03:242'de bir cümleyle tanımlayın ve macros_konsey.tex'e \Asig{IN} yanında bu biçimi ekleyin. \bar{A}^{\sigma}_{\mathrm{IN}} 03:242, 03:303, 04:380, 04:424'te makro yerine elle yazılmış; tek makroya bağlayın.

### 2. [sari] r harfi üç ayrı anlamda: yönlü artık, protokol oranı ve Pearson korelasyonu

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: tab:external_pool 04:129 sütun başlığı "\textbf{$r$}" (Pearson), hemen üstteki sütunlar σ ve ρ; 04:534 "Pearson $r = 0.957$"; 07:145 "($+0.656$, $r = 0.931$)"; 07:152 "estimates $1 - r_{\text{cond}}$".

Kanit: Brif 12 §3.1 r'yi yönlü artık r_ij için ayırır, Spearman için r_S kullanılır. Pearson için çıplak r aynı tabloda σ, ρ ile yan yana durunca yönlü artığın panel değeri gibi okunur. r_raw ve r_cond kapı T4 nedeniyle korunuyor (brif §12.4), bu kabul edilebilir; ama Pearson için ek bir çakışmaya gerek yok.

Duzeltme: Pearson korelasyonunu r_P ya da 'Pearson correlation' sözcüğüyle yazın (04:129 başlık, 04:131-132, 04:534, 07:145); tab:external_pool alt bloğunun başlığını 'Pearson $r_{\mathrm{P}}$' yapın.

### 3. [sari] ω = log w ve L_k(m) yüzde cinsinden oranın logaritması, birim hiçbir yerde yazılmıyor

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: tab:cells 04:246 "$\omega = \log w$" ve sütun değerleri 4.024, 3.876...; fig_cells_interaction (c) ekseni 3.90-4.00; fig_attack_side x ekseni 2.2-2.85 "panel-mean log transfer $L_k(m)$"; 03:207 "$\omega_m = \log w_m$".

Kanit: tab:cells satır 254: w = 55.91 ve ω = 4.024 = ln(55.91); yani w yüzde olarak alınmış. Oran olarak w = 0.559 için ln = −0.581 olur. log τ̄ ve r birimden bağımsızdır, ama ω ve L_k'nin mutlak düzeyi bu seçime bağlıdır ve logit duyarlılığı oranla hesaplanmak zorundadır. Bir hakem ln(0.5563) hesaplayıp tabloyu hatalı sanacaktır.

Duzeltme: 03:207-211'e 'rates enter the logarithm in percent, so ω and L_k carry an additive constant of log 100 that cancels from every contrast' türünden tek cümle ekleyin; tab:cells başlığına ve fig_cells_interaction (c), fig_attack_side eksen etiketlerine '(w in %)' notu koyun ya da hepsini oran ölçeğine çevirin.

### 4. [sari] Renk çubuğu etiketleri yanlış yuvarlanmış

Dosya: paper/figures/konsey/fig_similarity_matrix.py

Ifade: Satır 207: cb.ax.yaxis.set_major_formatter(... f"{v:.1f}" ...); PNG'deki renk çubuğu −0.2, −0.5, −0.8, −1.0, −1.2, −1.5 okuyor.

Kanit: Etiketler görsel olarak eşit aralıklı (yaklaşık 67 piksel), ama yazılı değerler arasındaki farklar 0.3, 0.3, 0.2, 0.2, 0.3. Varsayılan konumlayıcı −0.25, −0.50, −0.75, −1.00, −1.25, −1.50'de çentik koyuyor ve .1f biçimi −0.25'i −0.2, −0.75'i −0.8, −1.25'i −1.2 diye basıyor. fig:similarity_matrix'te üç panelin hepsi bu ölçeği kullanıyor.

Duzeltme: Biçimi .2f yapın ya da çentikleri açıkça [-1.5, -1.0, -0.5] gibi tek ondalıkla tam gösterilen değerlere sabitleyin; kanıt dosyasına çentik değerlerini yazdırıp şekli yeniden üretin.

### 5. [sari] Şekilde D, metinde G; ImageNetV2 panelinde negatif yönlü pay sıfırın altına çizilmiş

Dosya: paper/figures/konsey/fig_source_gap_split.py

Ifade: Satır 155-157 gösterge: "total gap $D$", "registered $D$ threshold"; panel (c) çift 1: simetrik çubuk 0.167'ye çıkıyor, yönlü pay −0.044 sıfırın altında, toplam açık çizgisi 0.122'de.

Kanit: 03:213 ve tab:registry G ve G_s kullanır; brif §3.1 'Tek sembol: G' der. 14_makale_revizyon_notu.md bulgu 24 bu isteği şekil ajanına bırakmış, şekil 16:29'da yeniden üretilmiş ama gösterge hâlâ D. Föy 1930: çift 1 D_k 0.1221, simetrik 0.167, yönlü −0.044, q 1.364. Yığılı çubukta negatif parçanın sıfırın altına konması, toplamın çubuğun tepesi olduğu okumasını bozuyor (tepe 0.167, toplam 0.122).

Duzeltme: Göstergeyi G'ye çevirin. Negatif yönlü payı simetrik çubuğun üst ucundan aşağı doğru (0.122 ile 0.167 arası, taralı ya da açık renk) çizin ya da yönlü payı ayrı bir nokta olarak gösterin; altyazıya 'q n/a: G at or below the 0.10 threshold' ekleyin (föy 1932 bu çift için q 0.547 verir, şekilde basılmaması kayda uygundur).

### 6. [sari] 'İşaret döner' dili sıfıra eşdeğer kestirimler için abartılı ve revizyon notuyla çelişiyor

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: 04:494 "The sign reverses: on the log scale the ViT is, if anything, the directionally weaker source ... H3 reverses in the same way"; 04:506 fig:estimates_forest altyazısı "the ViT's directional term changes sign"; 06:14 "large and of opposite sign".

Kanit: Föy 1588: log ρ(V-scr) +0.012, %90 [−0.007, +0.031], yani sıfıra eşdeğer; H3 log +0.003 [−0.020, +0.026] (tab:fb4). Sıfır olan bir kestirimin 'işareti dönmez'. 14_makale_revizyon_notu.md bulgu 20, özet, giriş, tartışma, sonuç ve orman şekli altyazısında 'işaret döner' yerine 'büyük ve negatif' yazıldığını kaydediyor; altyazı ve 04:494 bu kayda uymuyor. CIFAR-100'de (log +0.143, logit −0.413) işaret gerçekten dönüyor.

Duzeltme: 04:494'ü 'On the logit scale the ViT's ρ is large and negative on both datasets, which makes it the directionally stronger source there; on CIFAR-100 this reverses a positive log estimate' biçiminde yazın, 'H3 reverses' yerine 'H3 is −0.087 on the logit scale (Section IV-D)' deyin; altyazıyı ve 06:14'ü aynı kalıba getirin.

### 7. [sari] Kelime bütçesi ve tekrar: yöntem tavanın üstünde, sınır ve çekince cümleleri çok kez yineleniyor

Dosya: paper/manuscript/sections/03_methodology.tex

Ifade: Yorumsuz sayım (brif §11 betiği, yeniden koşuldu): main 651, 01 1152, 02 1076, 03 3900, 04 7534, 04z 238, 05 1533, 06 323, 07 1384; toplam 17,791. 'necessary condition / on the log scale / accounting identity / not evidence of a mechanism' kalıpları 22 kez geçiyor.

Kanit: 03 dosya tavanı 3400, aşım 500 kelime (yüzde 15); toplam hedef 16,700, aşım 1,091. Sınır cümlesi (küçük yönlü terim yalnız log, CNN paneli, CIFAR-10) özet, 01:42, 04:155, 04:499, 05:19, 06:14'te; gradyan 'necessary condition' özet, 01:42, 03:260, 04:445, Şekil 7 altyazısı, 05:21, 05:72, 06:14'te; tanımlanabilirlik gerekçesi 01:16, 01:23, 03:222, 04:66, 05:33'te; V-scr temiz doğruluk karıştırıcısı 01:42, 04:238, 05:60, 06:12'de. Giriş katkı paragrafları (01:28-38) özetteki sayıların neredeyse tamamını yineliyor (0.936, +0.012, +0.566, 0.840, +0.143, −0.364, +0.260, +0.003, 0.960, 4.36, 19.37, 0.989, 0.0044); brif §12.2 'bir sayı özette, bir kez gövdede' der.

Duzeltme: 03:326-330 ön kayıt beyan paragraflarını (yaklaşık 420 kelime) ekte yeni bir 'Registration record' bölümüne taşıyıp 03'te iki cümlelik özet ve göndermeyle bırakın; 03:89 ve 03:114'teki tasarım ayrıntısını tab:design başlığıyla birleştirin. Sınır cümlesini gövdede yalnız 04:499 ve 05:56 sınırlılıklarda tutun, 04:155 ve 05:19'dan çıkarın. Gradyan çekincesini 03:260 ve 05:72'de tutun, 04:445'in ilk cümlesini ve Şekil 7 altyazısının son cümlesini atın. Giriş katkılarında sayıları en çok bir ana kestirime indirin.

### 8. [sari] Önerme numaralaması ve tanım sırası okuma akışını bozuyor

Dosya: paper/manuscript/sections/03_methodology.tex

Ifade: main.aux: prop:hscale = Proposition 1 (s.6), prop:identifiability = Proposition 2 (s.7); giriş 01:16 ve 01:23 önce 'Proposition 2'yi, 01:38 sonra 'Proposition 1'i anıyor. 03:64 L_k(m) = |P|^{-1}Σ_{c∈P}... ve \Gk{k} III-B'de tanımlanıyor; P 03:203-238'de (III-F, III-G), G 03:213'te tanımlanıyor.

Kanit: Brif 12 §3.1 son paragraf identifiability'yi Proposition 1, h ölçeğini Proposition 2 olarak öngörür; derlenmiş PDF tersini basıyor çünkü subsec:metrics, subsec:decomposition_def'ten önce geliyor. III-B'deki panel ortalaması ve kaynak açığı, panel ve G tanımlanmadan kullanılıyor.

Duzeltme: subsec:decomposition_def ve subsec:panels'i subsec:metrics'ten önceye alın (ya da protokol özdeşliği ve Proposition h-scale'i III'ün sonuna taşıyın); saldırı tarafı tanımını (03:64) III-F'deki G tanımının hemen ardından bir cümleye indirin.

### 9. [sari] Özet sembol ve sayı yüklü, IEEE Access okuyucusu için kendi başına okunmuyor

Dosya: paper/manuscript/main.tex

Ifade: main.tex:117 özet $w$, $\bar{\tau}$, $r$, $\Delta_{\mathrm{seed}}$ sembolleri ve yaklaşık 25 sayı taşıyor; "ViT seeds resemble each other more than the panel"; "(PGD-10 gaps 3.20--7.40 points)".

Kanit: IEEE Access yazar kılavuzu özette sembol ve kısaltmadan kaçınılmasını ister. Δ_seed ve 'symmetric share' tanımsız okur için anlamsızdır. 'PGD-10 gaps' PGD-10 ile AutoAttack doğruluk farkı olduğu söylenmeden yazılmış. 'resemble each other more than the panel' karşılaştırma nesnesi belirsiz (seeds resemble the panel değil, seeds resemble each other more than they resemble the panel).

Duzeltme: Sembolleri sözcükle değiştirin (target vulnerability, symmetric similarity, directional residual), Δ_seed'i 'ViT seeds are more similar to each other than to the panel (+0.566)' biçiminde verin, maskeleme parantezini 'PGD-10 exceeds AutoAttack accuracy by 3.20 to 7.40 points' yapın; 250 kelime için ImageNetV2 aralığını ya da 0.960 aralığını çıkarın (check_abstract_body kapısını yeniden koşun).

### 10. [yesil] tab:registry'de yalnız tabloda geçen etiketler ve q gösterimi

Dosya: paper/manuscript/sections/03_methodology.tex

Ifade: 03:306-307 'H10' ve 'H10k'; aile sembolleri $\mathcal{F}_{\mathrm{panel}}$, $\mathcal{F}_{2\times2}$, $\mathcal{F}_{\mathrm{C100}}$, $\mathcal{F}_{\mathrm{grad}}$ metinde hiç geçmiyor; 03:290 '$\bar q \leq 0.50$' ama metin ortalamayı q diye yazar.

Kanit: H1-H3'ten H10'a atlama ön kayıt içi numaradır, okura açıklanmaz; tab:mantel ve 04:437 bu etiketleri kullanmaz. q, q_s, q̄ üç biçimde geçiyor (03:215, 04:145, tab:panel_tests).

Duzeltme: H10 ve H10k yerine 'G-raw' ve 'G-res' gibi metinle eşleşen etiketler kullanın ya da tab:mantel'e aynı etiketleri koyun; aile sembollerini ya metinde bir kez anın ya da tablodan çıkarıp 'panel family (CIFAR-10)' yazın; q̄ yerine q yazın ve tohum değerini q_s diye tutun.

### 11. [yesil] Standart sapma ve p değeri gösterimi tablolar arasında tek biçimde değil

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: tab:main_results 04:32 'mean$\pm$std', tab:protocol_settings 04:542 'mean$\pm$std', Şekil 9 altyazısı 04:566 'mean$\pm$SD', tab:fb4 dipnotu 'Pooled SD', 07:44, 07:64, 07:118 'std'; tab:panel_tests, tab:fb4, tab:mantel '1.26e-04', '1.36e-05', '6e-04'.

Kanit: Brif §3.1: standart sapma 'SD'. Metin p değerlerini 2.73×10^{-3} biçiminde yazıyor (04:148), tablolar bilgisayar gösterimiyle.

Duzeltme: Bütün altyazılarda 'mean$\pm$SD' kullanın; tablolarda p değerlerini $1.26\times10^{-4}$ biçimine çevirin ya da bir tablo dipnotunda 'aE-b denotes a×10^{-b}' deyin.

### 12. [yesil] Altyazı ile panel harfleri ve şekil içi etiketler uyumsuz

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: 04:480 fig:gradient_alignment altyazısı '(top)' ve '(bottom)' diyor, şekilde (a)-(f) harfleri var; fig_decomposition_schematic panelleri (1)-(4) numaralı, öteki şekiller harfli; aynı şekilde üst çizgi hem τ̄ (iki yönün geometrik ortası) hem panel ortalaması için kullanılıyor (03:199 'overline: mean over panel members'); fig_similarity_matrix (b) CIFAR-100 modellerini 'V-scr' ve 'R32' diye etiketliyor.

Kanit: R32 ve V-scr tab:design'da CIFAR-10 hücre adlarıdır; CIFAR-100 çifti 03:240'ta ayrı modeller olarak anılır. Şekil 2 (3)'te σ_m = overline{log τ̄_mc} iki üst çizgiyi üst üste bindiriyor. Şekil 4 (c)'de transformer bloğu çerçevesiz, öteki bloklar çerçeveli.

Duzeltme: Şekil 7 altyazısını '(a)-(c) raw, (d)-(f) residual' diye yazın; Şekil 2 panellerini (a)-(d) yapın ve panel ortalamasını ⟨·⟩_P ile gösterin; Şekil 4 (b)'de 'ViT (C100)', 'ResNet (C100)' etiketi kullanın ve (c)'de transformer bloğunu çerçeveleyin.

### 13. [yesil] Küçük yazı boyutları ve akış okları

Dosya: paper/figures/konsey/fig_study_overview.tex

Ifade: PDF yazı boyutları (PyMuPDF ile ölçüldü): fig_study_overview en küçük 5.0 pt (6.77 in genişlik, \textwidth'e ölçeklenir), fig_decomposition_schematic en küçük 4.4 pt, fig_cells_interaction, fig_estimates_forest, fig_source_gap_split, fig_gradient_alignment 5.6 pt; genel bakışta (c) ölçüm kutusundan (d) 'Registered before measurement' kutusuna inen ok.

Kanit: IEEE grafik kılavuzu basılı boyutta en az 8 pt, alt indisler için en az 6 pt önerir. 5.6 pt değerleri çoğunlukla alt indislerdir ve kabul sınırında; 4.4 ve 5.0 pt gri açıklamalar basılıda okunmaz. Ölçümden 'ölçümden önce kaydedilen' kutuya giden ok mantık sırasını ters gösteriyor.

Duzeltme: visio-cizici turunda gri açıklama metnini en az 6.5 pt yapın, şematikteki kesir alt indislerini büyütün; (c)→(d) okunu kaldırın ya da (d)'yi (c)'ye giren kesikli bir 'decision rules' okuyla bağlayın.

### 14. [yesil] Şekil 9'da metinde olmayan terimler

Dosya: paper/figures/final/fig_protocol_sets.pdf

Ifade: Şekil içi açıklamalar 'endorsed pair' (3.91) ve 'different estimand' (11.10); panel (a) 'N: CNN→ViT / ViT→CNN' başlığı CNN→ViT kutuları için iki N veriyor.

Kanit: Değerler föyle tutarlı (13.57 − 4.36 = 9.21, 8.27 − 4.36 = 3.91, 19.37 − 8.27 = 11.10), ama 'endorsed pair' hiçbir bölümde tanımlanmıyor; 04:528 aynı farkı 'both-correct excludes them, and the directional difference reappears 3.91 points higher' diye anlatıyor.

Duzeltme: 'endorsed pair' yerine 'marginal subsets removed', 'different estimand' yerine 'source-robustness term' gibi 04:528 ile aynı dili kullanın; (a) başlığını 'N (CNN→ViT / ViT→CNN)' biçiminde netleştirin.

### 15. [yesil] tab:external_pool iki tabloyu tek gövdede birleştiriyor; ileri göndermeler uzak

Dosya: paper/manuscript/sections/04_experiments.tex

Ifade: 04:129-132 alt blok başlıkları (Slope, 95% interval, r) üstteki σ, ρ sütunlarının altına düşüyor; 04:66 ve tab:pair_decomposition altyazısı (04:81) s.9-11'den s.18'deki Tablo 13'e gönderiyor; 04:56 '... gave the same absolute ordering' cümlesi 03:79'u yineliyor.

Kanit: Tek sütunlu tabloda iki ayrı başlık satırı ve farklı anlamdaki sütunlar okuru şaşırtıyor. Tablo 13 (tab:protocol_settings) IV-B'de ilk anılıyor ama yedi sayfa sonra basılıyor.

Duzeltme: Havuz yayılım eğimlerini tab:protocol_settings'in dipnotuna ya da IV-I metnine taşıyın; IV-B'deki +4.36 için Tablo 5'in kendi üst bloğunu (+4.41) gönderin ve farkı tek dipnotta açıklayın; 04:56'daki eski çift cümlesini silin.

### 16. [yesil] Katkı sıralaması karışık biçimde

Dosya: paper/manuscript/sections/01_introduction.tex

Ifade: 01:23 'The first contribution', 01:28 'The decomposition ... form the second contribution', 01:32 'Third, we intervene', 01:38 'The fourth contribution'.

Kanit: Brif §12.2 'First, ... Second, ...' yanlış numaralamasını ve simetrik paragraf kalıbını yasaklar; burada dört paragraf üç ayrı kalıpla açılıyor, ai_izi sayacı da 01:32'yi first_second olarak işaretledi.

Duzeltme: 01:32'yi 'The third contribution is an intervention on the pair itself.' biçiminde öteki üçüyle aynı kalıba getirin ya da hiçbirinde sıra sözcüğü kullanmayın.

### 17. [yesil] IEEE Access gönderim biçimi ayrıntıları

Dosya: paper/manuscript/main.tex

Ifade: main.tex:177-179 ikinci yazar biyografisi yalnız kurum ve ilgi alanı içeriyor; iki biyografi de IEEEbiographynophoto; şekiller '../figures/konsey/...' ve '../figures/final/...' göreli yollarıyla çağrılıyor (03:36, 04:196, 04:565, 07:31).

Kanit: IEEE Access son sürümde fotoğraflı biyografi ve öğrenim bilgisi ister. ScholarOne LaTeX yüklemesi dosyaları tek klasörde toplar, '../' yolları sunucuda derlemeyi kırar. Derleme günlüğünde şablon dışında Overfull kutu yok (yalnız \output sırasında 505 pt ve \maketitle 9.27 pt, şablondan).

Duzeltme: Gönderim paketinde şekil PDF'lerini manuscript klasörüne kopyalayıp yolları düzleştirin; ikinci yazar biyografisine dereceleri ve yılları ekleyin; kabulden sonra fotoğraflı IEEEbiography ortamına geçin.

### 18. [yesil] Bilinen yer tutucular

Dosya: paper/manuscript/sections/07_appendix.tex

Ifade: 07:137 '% TODO(foy): saldiri tohumu tekrarinin SD'si ...'; 07:144 '% TODO(foy): CIFAR-100 C3 hedeflerinin temiz hatalari ...'.

Kanit: İkisi de yorum satırı, PDF'e basılmıyor; ilgili cümleler sayısız kurulmuş ('Attack seeds leave robust accuracy essentially unchanged on a fixed subset', 07:138). Başka TODO, BEKLIYOR ya da yer tutucu yok; main.bbl'de TODO dizgesi yok.

Duzeltme: Gönderimden önce föye iki değer eklenirse sayıyla, eklenmezse yorum satırlarını silerek kapatın; 07:138'deki 'essentially unchanged' ifadesi sayısız kalacaksa 'did not change robust accuracy beyond 0.1 points' gibi bir eşik ancak föyle yazılabilir.

## Guclu yanlar

- Gönderme bütünlüğü tam: 78 etiketin her biri en az bir kez gönderiliyor (sec:introduction dışında), main.aux'ta tanımsız gönderme yok, şablon kaynaklı Overfull kutular dışında taşma yok; 24 sayfalık PDF şifresiz ve özet ile anahtar kelimeler basılıyor.
- Sayı-kaynak zinciri görünür: her paragraf ve tablonun üstünde % FOY satırı var; yeniden hesapladığım değerler föyle tutuyor (Şekil 3 tohum q'ları 0.940/0.928/0.940 föy 1587; Şekil 5 açıklamaları A^σ_scr = −1.009 − (−0.645) = −0.364, I^σ = 0.270 − 0.010 = +0.260, A^ρ = ½(0.070 − 0.064) = +0.003; Şekil 9 farkları 9.21, 3.91, 11.10).
- Makine yazımı sayacı temiz: ai_izi_tara kalıp geçiş, klişe, hedging yığını, meta yorum, uzun tire ve madde yığını için sıfır verdi; 'koyu etiket' isabetlerinin tamamı tablo başlığı; 'rather than' yalnız kapı korumalı 07:152'de.
- Olumsuz sonuçlar tablolarda saklanmadan duruyor: K-b CIFAR-100 'refuted (+)', Liu çifti 'uncertain', logit duyarlılık satırları, Welch aralıkları ve üretilmeyen analizler (tab:panel_tests dipnotu, 03:330) açıkça basılıyor.
- Şekil taslakları tutarlı bir renk ve işaret dili kullanıyor (Okabe-Ito, ViT turuncu üçgen, ResNet mavi daire, betimsel veri taralı ya da açık işaret); renk dışı ikinci kanal her şekilde var ve altyazılar çoğunlukla iki ila dört cümlede kendi başına okunuyor.
- Tablo başlıkları ölçeği, örneklemi, aralık türünü ve karar kuralını açıkça veriyor (tab:fb4, tab:panel_tests, tab:attack_side); duyarlılıklar karar satırından ayrı blokta duruyor.
