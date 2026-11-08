# Kol C3, Faz 2 bitirme: çürütücü raporu (08.11.2026, ikinci turun birinci doğrulaması)

Çelişik doğrulayıcı opus (salt okur) raporudur; yardımcı Fable (Kol C3) tarafından olduğu gibi kaydedilmiştir. Kapanışlar `02_faz2_cizim.md` "İkinci tur" bölümünün devamında yazılıdır.

verdict: duzeltilmeli

Şekiller, sayılar, kapılar ve paket büyük ölçüde sağlam. Kararı tek bir şey belirliyor: kurulum betiğine eklenen istisna asıl makalenin şekillerini artık korumuyor. Raporun "asıl makale şekilleri her kipte reddedilmeye devam eder" cümlesi bu proje için yanlış. Bunu salt okunur bir benzetimle doğruladım.

## issues

1. **major, güvenlik deliği ve yanlış beyan.** Yerler: `C:\Users\cagri\.claude\skills\visio-cizici\motor\visio\install.py:523-540` (`_tracked_is_own`) ve `:553-555`; beyan `02_faz2_cizim.md:133` ve `:187`.
   - Beklenen: paper/figures altında git'in izlediği asıl şekiller her kipte reddedilir.
   - Bulunan: v1 şekilleri (`paper/figures/fig1_study_overview.pdf` ... `fig17_*`, main.tex'in `../figures/` ile içe aldığı dosyalar) motorun kendi `kur` satırlarıyla kurulmuş, sonra kaydedilmiş. `paper/figures/visio_loglari/kurulum.log` dosyasında 119 `kur` satırı var. Bu yüzden istisnanın üç koşulu da onlarda sağlanıyor.
   - Benzetim: v1 ayarıyla (`VZ_PROJE_AYARI=.../paper/figures/visio_cizici.yaml`) `_tracked_is_own` izlenen 814 dosyanın **111**'inde True döndü. 17 asıl şeklin pdf, png, eps, svg, fig.json, kanit.json ve mm.json dosyaları artık `--yeniden` ile üzerine yazılabilir. Değişiklikten önce izlenen her hedef koşulsuz reddediliyordu.
   - Test açığı: `tests/test_motor.py:487-522` yalnız hiç kurulmamış bir asıl şekli sınıyor ("no kur row"). "Motorla kurulup kaydedilmiş asıl şekil" durumu sınanmıyor, oysa bu projenin gerçek durumu bu.
   - Düzeltme önerisi: istisnayı açık bir izin listesine bağlamak. Örneğin yalnız v2 ayarında bir `install.izinli_kayitli_yeniden: true` bayrağı ya da hedefin `paper/figures_v2` olması şartı konabilir. Yanına bu durumu sınayan bir test eklenmeli.
   - Not: `git rm --cached` ile 10 dosyanın dizinden çıkarılması da korumayı dolanmaktır. Rapor bunu yazmış, ama aynı yöntem başka bir projede asıl şekillere de uygulanabilir.

2. **orta, Şekil 16.** Yerler: `fig16_epsilon_sweep.png`, altyazı `altyazilar_v2.tex:19`, K7 gerekçesi `fig16_epsilon_sweep.kanit.json` `k7_muafiyet.gerekce`.
   - Altyazı "Each card's top edge traces ... as a true vertical length (scale bar 25 points)" diyor.
   - İkinci turda arka levhalar sola kaydırıldı. Derinlik kaydırması böylece tamamen düşey eksene, yani değer ekseninin yönüne bindi: ResNet levhası yaklaşık 128 px, WRN levhası yaklaşık 260 px yukarıda (25 puan = 222 px ölçeğiyle 14.6 ve 29.3 puan).
   - Arka levhaların dolgusu ön taban çizgisine (y=1130) kadar iniyor. Bu yüzden görünen yükseklik değer artı derinlik oluyor. Örneğin WRN'nin temiz doğruluğu ölçek çubuğuyla yaklaşık 119 puan okunuyor, gerçek değer 89.5.
   - Değerler kendi (gizli) tabanlarına göre doğru: WRN 47.4, ResNet 20.4 ve ViT 12.2 piksel düzeyinde tutuyor. Sayı satırları değeri taşıdığı için K7 kurtarıyor.
   - Yine de "true vertical length" ve ölçek çubuğu iki levhada yanlış okutuyor. Rapor (`02_faz2_cizim.md:183`) "alan grafiğine daha da benzedi" demiş ama bu okuma hatasını yazmamış.
   - Düzeltme önerisi: arka levha dolgularını kendi tabanında kesmek ya da altyazıdan "true vertical length" iddiasını çıkarmak.

3. **orta, yeni imza tekrarı (devir bulgusu 9 tekrarı yalnız yer değiştirdi).**
   - Şekil 11 "three steles", Şekil 12 "one tablet". İkisi de kaidesiz ya da kaideli, dik duran ve içinde üstte-altta iki veri paneli taşıyan taş levhalar (altyazılar 14-15. satırlar).
   - 9 ile 12 arasındaki askı tekrarı kalktı, ama yerine 11 ile 12 arasında taş levha tekrarı doğdu. Şekil 15'in arka ve ön dik kartları da aynı aileye yakın.
   - Şekil 11'in altı paneli yine aynı boyda ve düşeyde kaydırılmış bir 2×3 düzen. "Aynı boyda kart ızgarası" yasağı (`uslup_Z.yaml:286`) gevşek okunursa karşılanmış, katı okunursa sürüyor.

4. **küçük, rapor içi çelişki.** `02_faz2_cizim.md:147` "kapı iki ölçümde de geçer" diyor. Oysa `02_ilerleme.tsv`'deki tek şekillik ölçümde Şekil 12'nin katı puanı 89.1, yani katı karar BLOCK. Bu yüzden "katı BLOCK yalnız 1, 6, 8, 11, 15" sözü yalnız makale kopyası için doğru. Ayarlı puan (92.5) iki ölçümde de geçiyor.

5. **küçük, eskimiş özet.** `02_faz2_cizim.md:5` (giriş paragrafı) ve §3 tablosu (`:31-47`) birinci turun sayılarını taşıyor: "QC ayarlı 93.6 ile 100.0, katı 87.0 ile 95.9"; Şekil 11 için 94.4 mm; 16 ve 17 için 97.6 ve 100.0. Güncel değerler: ayarlı 93.6-96.8, katı 87.0-94.3. Belgenin başını okuyan kişi eski değerleri görür.

6. **küçük, Şekil 2.**
   - R32 çekmecesinin üç fiş kartı (tohum 1001-1003) üst üste binmiş ve dolabın alt kenarı onları kırpıyor. Kırpma `scratchpad\curut3\fig2_r32.png` dosyasında, üç kart ayrı seçilemiyor.
   - Raporun "öteki çekmecelerde iki fiş kartı" cümlesi (`02_faz2_cizim.md:175`) R32 için yanlış, çünkü R32'de üç koşu var.

7. **küçük, Şekil 1.**
   - (c) "PGD-10 matrices" kılavuzları, (b) başlıklarının kılavuzlarının indiği CIFAR-100 ve ImageNetV2 destelerine iniyor.
   - Yani (b) ve (c) hâlâ aynı nesneleri gösteriyor. Ayrım yazıda var, sahnede yok. Bu yüzden kapanış kısmi.

8. **küçük, metin katmanında eksi işaretleri.** fig_mm_pdf'i yeniden koştum. Şekil 11 (10 glif), 12 (7 glif) ve 1 (2 glif) T6 uyarısı veriyor: "−" glifi metin katmanında boşluk olarak çözülüyor (Open Sans glif 555). PDF'ten kopyalanan "−0.6" "0.6" olarak geliyor. T4 0 beyanı doğru, ama T6 raporda hiç anılmamış.

9. **küçük, Şekil 7.**
   - "G 0.0999 q n/a" artık föy:1932 ile tutarlı (D_k 0.0999).
   - Ama föy aynı satırda q_k 0.547 ve "hesaplandi" yazıyor. Şekilde "n/a"nın payda kuralından (D_k ≤ 0.10) geldiğini söyleyen bir açıklama yok. Lejanttaki "registered 0.10 threshold" bunu dolaylı anlatıyor.

10. **bilgi, Şekil 12.** K-b C10 logit satırının aralığı [−0.327; −0.282] eşkenar dörtgen işaretin altında kalıyor ve görünmüyor. Değer doğru (föy:1603).

11. **bilgi, Şekil 2 kontrolcü notu.** QC'yi yeniden koşunca Şekil 2 için "controller: shape_pairs_checked is 0 ... no solid shape" uyarısı çıktı. Bloklayıcı değil.

## Sayı denetimi

Otomatik açılan değerler kanıt dosyasındaki JSON anahtarlarıyla tutuyor:

| Şekil | Tutuyor | Uyuşmaz |
| --- | --- | --- |
| 12 | 72/72 | 0 |
| 7 | 37/37 | 0 |
| 15 | 241 | 0 |
| 14 | 31 | 0 |
| 10 | 29 | 0 |
| 6 | 65 | 0 |
| 2 | 51 | 0 |
| 17 | 61 | 72 |

Şekil 17'deki 72 uyuşmaz, üç koşunun ortalamasıdır (selefin bulgusuyla aynı). Okunan dosyalarda karantina yolu 17/17 şekilde 0. Şekil 16'nın okuduğu `results/wrn_eval` föyün 354. satırında kaynak olarak gösteriliyor.

Föy (`results/C1_REFERANS_FOYU.md`) karşılaştırması:

| # | Şekil, değer | Çizilen | Kaynak dosya:satır | Sonuç |
| --- | --- | --- | --- | --- |
| 1 | 12, H1 log, %90 ve %95 aralık | −0.364 [−0.415; −0.314] [−0.428; −0.300] | föy:1526 | tutuyor |
| 2 | 12, H2 log | +0.260 [0.186; 0.335] [0.165; 0.355] | föy:1527 | tutuyor |
| 3 | 12, H3 log | +0.003 [−0.020; 0.026] [−0.026; 0.033] | föy:1528 | tutuyor |
| 4 | 12, IN-V2 çift 1 | −0.167 [−0.234; −0.096] [−0.246; −0.084] | föy:1930 | tutuyor |
| 5 | 12, IN-V2 çift 2 | −0.118 [−0.202; −0.038] [−0.217; −0.023] | föy:1931 | tutuyor |
| 6 | 12, IN-V2 Ā(σ, IN) | −0.142 [−0.197; −0.090] [−0.207; −0.081] | föy:1938 | tutuyor |
| 7 | 12, IN-V2 Liu scr. | −0.055 [−0.137; 0.022] [−0.153; 0.034] | föy:1939 ve 1932 | tutuyor |
| 8 | 12, H1, H2, H3 logit | −0.498, +0.354, −0.087; aralıklar | föy:1551 | tutuyor (%95 üst sınır 0.4904 ile 0.490) |
| 9 | 12, K-b C10 log | +0.012 [−0.007; 0.031] [−0.016; 0.040] | föy:1588 | tutuyor |
| 10 | 12, K-b C100 log | +0.143 [0.101; 0.184] [0.082; 0.203] | föy:1839 | tutuyor |
| 11 | 12, K-b C10 ve C100 logit | −0.304 [−0.320; −0.289]; −0.413 [−0.546; −0.280] [−0.609; −0.217] | föy:1603, 1857 | tutuyor |
| 12 | 11, r ve n, CIFAR-10 | 0.94 / 0.94, n 190 | föy:1970-1971 (0.943 / 0.944) | tutuyor |
| 13 | 11, CIFAR-100 | 0.98 / 0.91, n 105 | föy:1972-1973 | tutuyor |
| 14 | 11, ImageNetV2 | 0.69 / 0.89, n 91 | föy:1974-1975 | tutuyor |
| 15 | 11, eksen etiketleri ve veri aralığı | x ham C10 [−1.143; −0.288], işaretler −1.0 ... −0.4 | kanit veri listeleri | tutuyor, etiketler gerçek değer |
| 16 | 16, WRN 5 değer | 89.5 / 85.4 / 80.0 / 66.9 / 47.4 | föy:360-364 | tutuyor |
| 17 | 16, ResNet-18 AT | 85.8 / 77.3 / 66.7 / 44.2 / 20.4 | föy:360-364 | tutuyor |
| 18 | 16, ViT-Tiny AT | 73.5 / 64.1 / 53.9 / 32.7 / 12.2 | föy:360-364 | tutuyor |
| 19 | 16, en büyük SD | 0.59 | föy:363 | tutuyor |
| 20 | 7, IN-V2 G ve parçalar | 0.122 (0.167 − 0.044), 0.173 (0.118 + 0.055), 0.0999 (0.055 + 0.045); q 1.36, 0.68 | föy:1930-1932 | tutuyor; çubuk uzunlukları PNG'de ölçüldü |
| 21 | 7, CIFAR-10 G ve q | 0.391 / 0.387 / 0.390; 0.94 / 0.93 / 0.94 | selefin denetimi (föy:1587, 1593); PNG ölçümü 0.392 | tutuyor |
| 22 | 1, matris boyları | 20 / 15 / 14 model | mantel_*.json `len(modeller_ortak)`; föy denetimi 19/19 TAMAM | tutuyor |
| 23 | 1, panel sayıları | 7+1, 7+2, 6+8 | hucre_tablosu*.json | tutuyor (8+12 = 20, 9+6 = 15) |
| 24 | 2, tohum aralıkları | 2001-2003, 2101-2102, 1201-1202, 1301-1302, 1001-1003 | kanit (51 tutuyor) | tutuyor |
| 25 | 15, n | 60 çift | kanit, föy:162 ailesi | tutuyor |

## Bulgu kapanış denetimi (devir numaraları)

1. **Kapandı.** Şekil 11'in eksen etiketleri gerçek işaret değerini basıyor ve veri aralıklarıyla tutuyor. PNG'ye bakıldı.
2. **Kapandı.** Paketteki 17 .vsdx dosyasında `dc:creator` ve `cp:lastModifiedBy` boş. Yapım kopyalarından yalnız `docProps/core.xml` farklı. Yapım taslaklarında "ÇAĞRI ŞAHİN" duruyor, bu beyan edilmiş. `--yollari-tara` 0 verdi. Pakette ve vsdx üyelerinde wsl.localhost, cagri, firat, ŞAHİN, `Users\`, `\home\` ve `C:` için eşleşme 0. Paket 53 dosya, SHA256SUMS 51/51 OK.
3. **Kapandı.** Şekil 7-17'nin on bir altyazısının hepsinde değeri taşıyan kodlama yazılı.
4. **Kapandı.** `karantina` alanı şekil başına gerçek sınıfları yazıyor (c1_*, wrn_eval, data/cifar, ON_KAYIT). `k7_muafiyet` Şekil 7 ve 16'da var.
5. **Kısmen kapandı.** §1 ve ikinci tur doğru. Giriş paragrafı ve §3 tablosu eskimiş (issue 5). Rapor `:147` tek şekillik ölçümde Şekil 12'nin katı BLOCK'unu söylemiyor (issue 4).
6. **Kapandı.** `govde_duzeltmeler_v2.tsv` dosyasında iki satır var ve iki değişiklik de yalnız manuscript_v2'de. Diff'te başka gövde farkı yok. main_v2.pdf 26 sayfa, tanımsız gönderme 0 (tek uyarı T1/pcr yazı tipi), taşma 57 (55 hbox, 2 vbox). PDF 23:24'te, son kurulumdan (23:23) sonra derlenmiş.
   - git status: paper/manuscript'te yalnız önceden de görülen 10 mod değişikliği var. paper/figures'ta değişen dosya yok, izlenmeyen dosyalar eski. results altında yalnız başka bir sürecin `curutme_2026-11-08` klasörü var. 08.11 16:30'dan sonra bu üç yolda değişen dosya 0.
7. **Kapandı.** Şekil 3 ve 6'da eğri bağlayıcılar var.
8. **Kapandı.** Şekil 17'de her bloktan bir ok çıkıyor.
9. **Kısmen kapandı.** Askı tekrarı kalktı, yerine 11 ile 12 arasında taş levha tekrarı doğdu (issue 3).
10. **Açık.** Şekil 8'in eğik ısı haritası gerekçeli olarak korundu. Değer düz renk basamağıyla okunuyor.
11. **Çoğunlukla kapandı.**
    - Şekil 16'da işaretler x etiketleriyle hizalı, ama bunun yan etkisi issue 2.
    - Şekil 2'de V-scr'de üç kart görünüyor, R32'nin kartları ise ezik (issue 6).
    - Şekil 15'te halkalar seçilebiliyor.
    - Şekil 7'de G dört ondalıkla basılıyor.
    - Şekil 1'de harfler kart içinde sol altta, ama (b) ile (c) hâlâ aynı nesneleri gösteriyor (issue 7).

Öteki iddialar da yeniden koşularak doğrulandı:
- **QC:** makale kopyası üzerinde yeniden koşuldu; 17/17 ayarlı kipte PASS, değerler 93.6-96.8, katı BLOCK 1, 6, 8, 11 ve 15'te, tutarlılık PASS. Çıktı `C:\Users\cagri\AppData\Local\Temp\claude\e2c0fa868388f4cf\0d0fab82-c6b8-472d-a420-d8ffb5857ab2\scratchpad\curut3\qc_makale\report.md`.
- **kapilar.json:** 17/17 dosyada basılı çizgi [0.75, 1.5] ve T4 boş.
- **Kurulu dosyalar:** PDF ve PNG yapım dosyalarıyla bayt bayt aynı.
- **pytest:** 641 geçti, 2 bilinen histopatoloji testi başarısız.

## Özgünlük yargısı (verdict'i belirlemez)

- Şekil 12'nin kitabesi düz bir forest grafiğine çerçeve ve kaide ekliyor. Okunaklı, ama yeni bir okuma fikri getirmiyor.
- Şekil 11'in dikili taşlarında derinlik kayıt sırasını taşıyor ve "main effects removed" çıkıntısı işlem adımını sahneye koyuyor. Bu, birinci turun tribününden daha anlamlı. Panel düzeni ise yine aynı boy kartlar.
- İkisi birlikte, birbirine benzeyen yeni bir "taş levha" çifti doğuruyor.
- Şekil 16'da hizalama düzeltmesi, alan grafiği klişesini güçlendirdi ve yükseklik okumasını bozdu.
- Gerçekten özgün okunanlar birinci turdaki gibi Şekil 7, 14 ve 10, kısmen de 6.

Bakış kopyaları ve betikler proje dışında, `C:\Users\cagri\AppData\Local\Temp\claude\e2c0fa868388f4cf\0d0fab82-c6b8-472d-a420-d8ffb5857ab2\scratchpad\curut3\` altında: own.py (istisna benzetimi), kanit.py, pkg.py, vz.py, mm_*.json, fig2_r32.png, qc_makale. Proje altında hiçbir dosya değiştirilmedi.
