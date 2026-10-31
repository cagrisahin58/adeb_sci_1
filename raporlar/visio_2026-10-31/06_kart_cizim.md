# Kart veri grafikleri (visio-cizici Faz B, Üslup 7)

Tarih 31.10.2026 gecesi. Hazırlayan kart veri grafiği ajanı (gorsel-uretici). Bu adımda Visio açılmamış, `.tex` dosyalarına, föye, `results/` altına ve özgün şekil klasörlerine (`paper/figures/final`, `final_tr`, `konsey`, `overview`, eski `*.py`) dokunulmamıştır. Bağlayıcı plan `04_cizim_plani.md` bölüm 3, 6, 8, 9 ve 11'dir; bütün sayılar o gün geçerli föyle (SHA-256 öneki `c85fcfc1b683e9f1`, M13 bölümü eklenmiş sürüm) karşılaştırılmıştır, planın andığı Faz A özeti (`00cc422f`) artık geçerli değildir.

En önemli üç sonuç şunlardır. Birincisi, planda motoru kart olan on bir şeklin on biri de Üslup 7 ile çizilmiş ve şekil başına dört kapının dördünden de geçmiştir: kart denetçisi PASS ve sıfır sorun, basılı PDF denetçisi PASS, denge "kurulabilir", föy karşılaştırmasında uyuşmayan sıfır; yükseklikler planın tavanlarının altındadır. İkincisi, Üslup 7'nin omurgasız ekseni veri alanı payını ölçülemez kıldığı için her veri kartında yalnız değer ekseninin taban çizgisi ince mürekkep çizgisi olarak bırakılmıştır; böylece pay muafiyetsiz ölçülmüş ve en düşük değer protokol kümeleri şeklinde 0.472 çıkmıştır (eşik 0.45). Üçüncüsü, çizim sırasında skill ve palet tarafında altı açık sorun bulunmuştur (bölüm 4); hiçbiri bir şeklin kapısını düşürmemiştir, ama ikisi (ayar ailesinin yedi renkli tonu ve gölge denetiminin üst üste binen işaretçileri gölge sayması) şekil tasarımında geri adım gerektirmiş ve kararlar bölümüne yazılmıştır.

## 1. Şekil başına sonuç

Kök adları numarasızdır ve kurulumda `fig<N>_<kök>` adını alacaktır (plan bölüm 9 sıra numarası parantezde). Kapı sütunları: K1' kart denetçisi (`<kök>.mm.json`), K2 `fig_mm_pdf.py --floor 8.0`, K3 `denge.py` kararı ve veri alanı payı, K5 föy karşılaştırma sayısı ve uyuşmayan, K6 yükseklik ve plan tavanı. Zenginlik satırı `scripts/zenginlik.py` çıktısıdır (karakter yoğunluğu, yazı kutusu alanı, sayısal oran, beğeniye uzaklık).

| Kök (sıra) | Tür, kind | Adım, tür | K1' | K2 | K3 (pay) | K5 | K6 (mm / tavan) | Zenginlik (kar/cm², yazı kutusu, sayısal, uzaklık) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_gap_split (7) | ortak_satirli_katlar, double | 4, serit | PASS 0 | PASS | kurulabilir (0.555) | 58 / 0 | 66.0 / 72 | 2.61, 0.15, 0.46, 0.05 |
| similarity_matrix (8) | ortak_satirli_katlar, double | 4, serit | PASS 0 | PASS | kurulabilir (uygulanmaz, ısı haritası) | 93 / 0 | 53.5 / 70 | 2.35, 0.13, 0.27, 0.42 |
| cells_interaction (9) | tasarim_izgarasi, single | 4, renk | PASS 0 | PASS | kurulabilir (0.795) | 78 / 0 | 121.0 / 125 | 2.64, 0.15, 0.27, 3.40 |
| attack_side (10) | tek_kart_veri, single | 1, yok | PASS 0 | PASS | kurulabilir (0.666) | 47 / 0 | 95.0 / 98 | 2.83, 0.16, 0.38, 0.00 |
| gradient_alignment (11) | ortak_satirli_katlar 2 x 3, double | 4, serit | PASS 0 | PASS | kurulabilir (0.628) | 46 / 0 | 110.0 / 118 | 1.93, 0.11, 0.44, 0.20 |
| estimates_forest (12) | tasarim_izgarasi, single | 4, renk | PASS 0 | PASS | kurulabilir (0.672) | 76 / 0 | 127.0 / 130 | 3.35, 0.18, 0.20, 3.21 |
| protocol_settings, Y7 (13) | tek_kart_veri, single | 1, yok | PASS 0 | PASS | kurulabilir (0.560) | 75 / 0 | 80.0 / 88 | 2.96, 0.16, 0.29, 0.00 |
| protocol_sets, Y3 ile (14) | tasarim_izgarasi, single | 4 (kural dalı 5), serit | PASS 0 | PASS | kurulabilir (0.472) | 36 / 0 | 115.0 / 120 | 4.20, 0.23, 0.22, 2.55 |
| spread_clean_gap (15) | tasarim_izgarasi, single | 4, serit | PASS 0 | PASS | kurulabilir (0.789) | 48 / 0 | 119.0 / 122 | 3.02, 0.17, 0.36, 2.90 |
| epsilon_sweep (16) | tek_kart_veri, single | 1, yok | PASS 0 | PASS | kurulabilir (0.590) | 28 / 0 | 62.0 / 66 | 2.52, 0.15, 0.35, 0.00 |
| feature_degradation, Y8 ile (17) | tasarim_izgarasi, single | 4, serit | PASS 0 | PASS | kurulabilir (0.777) | 169 / 0 | 118.0 / 122 | 2.69, 0.16, 0.56 (uyarı), 3.34 |

Bütün tuvaller kendi `kind`'inin tam genişliğindedir (single 85.29 mm, double 177.53 mm; ölçek 1.000) ve hiçbiri 165.33 mm'lik genel tavanı aşmaz. Föy karşılaştırma sayıları planda anılan konsey sayılarıyla aynıdır ya da üstündedir (gradyan 46, kaynak açığı 58, matris 93, hücreler 78, saldırı 47, orman 76); protokol kümelerinde 33 yerine 36 karşılaştırma vardır, çünkü üç basamak uzaklığı ayrıca protokol ortalamalarından yeniden hesaplanmıştır. Plan bölüm 6'nın 0.74'lük beklentisine karşı gradyan şeklinin ölçülen payı 0.628'dir; fark, eksen omurgasının sütun genişliğinin tamamını değil yalnız çizim alanını kaplamasından gelir ve eşiğin rahatça üstündedir.

İki uyarı not edilmiştir. Öznitelik bozulması şeklinde sayısal oran 0.56'dır ve 0.55'lik uyarı eşiğini aşar; nedeni üç kartın her birinde 1-12 katman numaralarının tik etiketi olarak basılmasıdır. Katman numaraları metinde ayrı ayrı anıldığı için (blok 9 ve 11 minimumları) etiketler korunmuştur. Benzerlik matrisi beş ölçütün ikisinde (ton ve boşluk) beğenilmeyen setin tarafında kalan tek şekildir; ısı haritasının mürekkep payı (0.36) bunun ana nedenidir. Bu iki madde blok değil uyarıdır ve şekilleri kurulamaz kılmaz. (Düzeltme turu 2 notu: ilk sürümde burada "benzerlik matrisi 0.42 ile beğeniye en uzak şekildir" yazıyordu; bu yanlıştı. Tablonun kendisinde hücreler 3.40, öznitelik 3.34, orman 3.21, yayılım 2.90 ve protokol kümeleri 2.55 uzaklıktadır. Bu büyük değerler tasarım ızgarası şablonuyla çizilen veri şekillerinin `zenginlik.py` tarafından şematik sayılıp şematik ton ve boşluk aralıklarına karşı ölçülmesinden gelir; bölüm 7.4'te açık sorun olarak yazılmıştır.)

## 2. Betikler ve ortak yardımcılar

Her şeklin betiği `paper/figures/charts/fig_<kök>.py`'dir ve yalnız `--uslup 7` ile koşar. Ortak yardımcı `paper/figures/charts/_kart_ortak.py` ortam değişkenlerini (`VZ_PROJE_KOKU`, `VZ_PROJE_AYARI`) kurar, depo köküne geçer, skill'i ve `paper/figures/konsey`'i yola ekler, Üslup 7'yi `ieee_access` venue'su ve `paper/figures/visio/palettes/adeb_konsey_uslup_7.yaml` paletiyle açar, paletin yolunu manifestin `palette_path` alanına yazdırır, eksen dilini uygular, kanıt dosyasını yazar ve denge yanıt dosyasını üretir. Faz A'nın `_vz_ortam.py` kabuğu kullanılmamıştır. Kapı koşturucusu `paper/figures/charts/_kart_kapilar.py`'dir; her komutu ve çıkış kodunu `paper/figures/visio_loglari/kart_ajani_komutlar.log`'a, özeti `paper/figures/qc/kart_kapilar_ozet.json`'a yazar. Durum dosyası `paper/figures/visio_loglari/kart_ajani_durum.json`'dur.

Veri kuralı her şekilde konsey betiğinin ya da eski final betiğinin kendisidir. Gradyan, kaynak açığı, matris, hücreler, saldırı tarafı ve orman şekillerinde konsey betiklerinin `main()` içindeki veri ve föy bloğu ya kelimesi kelimesine kopyalanmış ya da sabitleri ve yardımcı işlevleri içe aktarılmıştır (`fig_gradient_alignment.ana_etki_artik`, `fig_protocol_sets.load_and_check`, `fig_yayilim_temiz_fark.load_and_check`); özgün betikler değişmemiştir. Epsilon taraması, öznitelik bozulması ve Y7 için föyün kaynak satırlarında anılan dosyalar doğrudan okunmuş ve föy tablosunun her hücresiyle karşılaştırılmıştır.

Her şeklin yanında şu dosyalar durur: PDF, EPS, SVG, 601 dpi PNG, `.fig.json` manifesti (şablon adı `sablon` alanında), `.mm.json` kart denetçisi raporu, `.kanit.json` (her değer için kaynak dosya, anahtar yolu, hesap, föy satırı, kaynak SHA-256; ayrıca föy karşılaştırmasının tamamı, okunan anahtarlar, çizilen değerler, git bilgisi, notlar ve kararlar) ve `.denge_ajan.json`. QC raporları `paper/figures/qc/<kök>/` altında `fig_mm_pdf.json`, `denge.json` ve `zenginlik.json` olarak durur.

## 3. Kararlar

Karar: değer ekseninin taban çizgisi bütün veri kartlarında ince mürekkep çizgisi olarak bırakıldı, çünkü Üslup 7 (seaborn koyu ızgara dili) hiç eksen omurgası çizmez ve `pdfolcu.data_area_share` omurgasız şekilde "no data axis found" verip maddeyi "uygulanmaz"a düşürür; görev metni ölçülmemiş muafiyeti kabul etmez. Gri çizim alanı, beyaz ızgara ve çentiksiz eksen korunmuştur.

Karar: gradyan şeklinde Spearman özet kartı kaldırıldı ve satırlar solda 8 mm'lik dar bir şerit kartına döndürülmüş yazıyla adlandırıldı, çünkü kart denetçisi her yazının bir kartın içinde durmasını ister; altı r değeri ve n her panelde basılıdır.

Karar: gradyan şeklinde karışık çiftler açık gri kare olarak ve katmanlar arkadan öne sarı, gri, siyah sırasıyla çizildi, çünkü `denge.py`'nin gölge denetimi üst üste binen dolu gri bir kareyi siyah ya da sarı işaretçinin arkasında "gri gölge" saydı ve şekli kurulamaz yaptı; açık işaretçi beyaz kopya sayılır ve gölge değildir, ton palette `mixed` girdisine bağlı kalır.

Karar: yayılım şeklinde standart eğitimli modeller grubu mürekkep kenarlı açık işaretçiyle (palet şekli korunarak) çizildi, çünkü paletin `ayar` ailesi gri havuz dışında yedi renkli ton taşır ve denge kapısı bir şekilde altıdan fazla vurgu tonunu yasaklar; `ayar_std` girdisi bu şekilde kullanılmamıştır.

Karar: benzerlik matrisinde konseyin sürekli cividis ölçeği yerine üslubun beş basamaklı tek ton rampası (`isi_1`-`isi_5`) kullanıldı, basamak sınırları veri aralığından türetildi (0.1'e dışa yuvarlanmış aralık, beş eşit basamak, basamak 0.05'e yukarı yuvarlanmış) ve hücreler raster yerine vektör olarak çizildi; kartlar beyaz bırakıldı, çünkü rampanın en açık basamağı gri çizim alanıyla aynı tondur. Matrisler simetrik olduğu için (denetlendi) yalnız satırlar adlandırıldı.

Karar: protokol kümeleri şeklinde A-D harfleri ve (a)/(b) kaldırıldı, iki kart başlık şeridiyle adlandırıldı, kümeler protokol ailesinin dört moruyla dolduruldu ve her kümeye Tablo 2'deki maske koşulu sözcüklerle yazıldı (betik `03_methodology.tex` içindeki `tab:protocol_masks` satırlarını okuyup varlığını denetler). Üç basamak uzaklığı basamakların üstüne yalnız sayı olarak basıldı, terim adları (özdeşlik terimi, marjinal alt kümelerin çıkarılması, kaynak sağlamlığı) altyazıya bırakıldı, çünkü tek sütun genişliğinde terim adları 120 mm tavanı altındaki her yükseklikte satır değerleriyle çakışıyordu; ortalama ve SD sağdaki değer sütunundadır. Yayılım (15.01) denetlenmiş ama basılmamıştır, altyazı taşır.

Karar: hücre etkileşimi ve orman şekillerinde ±0.10 bandı üslubun `vurgu_kutusu` tonuyla (turuncu ailesinin açık tonu) çizildi, çünkü üslubun gri bant tonu çizim alanıyla aynıdır ve bant ρ'ya aittir. Hücreler şeklinde A^σ_scr ve I^σ etiketleri "A" ve "I" olarak yazıldı, çünkü üst ve alt simgeler yüzde 70 boyda basılıp 8 pt tabanının altına iner.

Karar: epsilon taramasında WRN-28-10 yolu (`results/wrn_eval/wrn_eval_summary.json`) yalnız bu süreçte `konsey_ortak.ALLOWED`'a eklendi, çünkü föy dosyayı satır 354'te kaynak gösterir ve değerlerini satır 19 ve 360-364'te basar; kanıt dosyasının `karantina_istisnasi` alanı yolu, föy satırlarını ve gerekçeyi taşır. ResNet-18 AT, C1 çiftinin 32 piksellik CIFAR kökü olduğu için `r32` rengini, WRN-28-10 sağlam CNN paneli rengini aldı.

Karar: öznitelik bozulmasında entropi değişiminin aralığı TOST dosyasının koşu düzeyi %90 aralığıdır (`results/c1_c4/c4_entropy_tost.json`, `entropi_TOST.katmanlar[k].GA90`), çünkü eşdeğerlik kararı bu aralığı ±0.05 nat marjıyla karşılaştırır; konsey şekli %95 t aralığı çiziyordu, altyazı buna göre değişmelidir. Üç koşunun değerleri her ortalamanın yanında açık işaretçiyle çizildiği için hiçbir kart tek serili değildir. Y8 kartı ViT'in üç jeton birleşimini (CLS, yama ortalaması, bütün jetonlar) çizer; ResNet-18 katman kosinüsleri farklı bir katman ekseni olduğu için çizilmemiştir.

Karar: tek kartlı şekillerde (saldırı tarafı, Y7) anahtar, eksenin altında aynı kartın içinde durur, çünkü 1. adım tek kart ister; çok kartlı şekillerde anahtar alttaki harfsiz şerit kartındadır (konvansiyon şeridi, adı yoktur).

## 4. Açık sorunlar (skill ve palet sahibine)

1. `motor/figspec/veri_dili.veri_grafigi_oku` Üslup 7'yi okuyamaz, çünkü üslubun `bilesen_kurallari.veri_grafigi` eşlemesi okuyucunun tanımadığı beş anahtar taşır (`eksen`, `izgara_rengi`, `cizim_alani`, `aralik`, `lejant`) ve okuyucu bilinmeyen anahtarda hata verir. Proje yardımcısı (`_kart_ortak.vg()`) bilinen anahtarları skill'in kendi varsayılanlarıyla okur, üslubun ek anahtarlarını olduğu gibi taşır; hiçbir değer uydurulmaz. Okuyucu ile katalog aynı turda uyumlanmalıdır (T33).
2. Üslup 7'nin "eksen omurgası yok" tokenı ile veri alanı payı ölçümü birlikte çalışmaz; omurgasız bir veri şekli ölçülemez. Ya ölçüm çizim alanının dolgu dikdörtgenini eksen sayabilmeli ya da üslup tokenı bir taban çizgisine izin vermelidir.
3. Paletin `ayar` ailesi gri havuz dışında yedi renkli ton taşır ve aynı şekilde çizildiğinde denge kapısının altı vurgu sınırını aşar. Palet üreteci (`paper/figures/visio/_palet_uret.py`) bu sınırı ölçmelidir; bugün bir grup nötr çizilmektedir.
4. `motor/figspec/palette.load` varlık kaydındaki `marker_edge` alanını taşımaz (`cift_vit` için 0.4 pt siyah kenar). Yardımcı alanı palet YAML'ından doğrudan okur.
5. Gölge denetimi saçılım grafiğinde üst üste binen dolu gri bir işaretçiyi gölge sayar (gradyan şeklinde ilk koşuda üç yanlış pozitif). Veri işaretçisi çiftleri gölge tanımından çıkarılmalıdır.
6. Kart motorunun `Canvas.save`'i kompozisyon şablonu almaz; yardımcı, kaydettikten sonra manifeste `sablon` alanını ekler (denge `sablon_beyani` uyarısını bu alanla kapatır). Manifestin geri kalanı değişmez.

## 5. Yazım ajanına değişecek atıf ve altyazılar

Altyazılar Faz C'de yazılacaktır; aşağıdaki liste şekilde değişen adları ve kodlamaları verir.

| Şekil | Altyazıda değişecek |
| --- | --- |
| source_gap_split | Yığılı çubuk yerine nokta ve aralık: yeşil işaret simetrik pay, turuncu parça yönlü pay, siyah elmas toplam açık G, açık işaret betimsel; q sağ sütunda; (a)-(c) yerine veri kümesi adları |
| similarity_matrix | Beş basamaklı tek ton ölçek ve basamak sınırları alt şeritte; yalnız satırlar adlandırılmıştır; (a)-(c) yerine veri kümesi adları |
| cells_interaction | Başlık rengi aileyi taşır (σ yeşil, ρ turuncu, ω nötr); R32 kendi tik etiketiyle; A ve I adları |
| attack_side | Değişmez; yalnız kalın giriş ve L(m) gösterimi |
| gradient_alignment | Özet kart yok; "top row, raw; bottom row, residual"; r ve n her panelde; çift türleri siyah, sarı, açık gri |
| estimates_forest | Üst kart σ karşıtlıkları, alt kart yönlü terimler; satır kısaltmaları C10, C100, IN-V2; daire log, elmas logit, açık betimsel |
| protocol_settings (Y7) | Yeni şekil; Tablo 13'ün yerine; satır ayarlar, şeritler protokoller, SVHN'de iki çift ortalamasız; sağ sütun yayılım |
| protocol_sets | Üst kümeler (maskeler sözcüklerle), alt asimetri; basamak sayılarının terim adları altyazıda; yayılım 15.01 altyazıda |
| spread_clean_gap | Üst ve alt kart, konumla atıf; sekiz grup ayar ailesiyle, standart eğitim açık mürekkep işaret |
| epsilon_sweep | Doğrudan etiketler; ResNet-18 AT açık mavi |
| feature_degradation (Y8) | Üç kart; entropi aralığı %90 TOST aralığı (eski altyazı %95 diyor); üçüncü kart blok çıkışı kosinüsü; Tablo 16 eke ya da kaldırmaya |

## 6. Kapsam dışı kalanlar ve doğrulanmamış noktalar

`fig_qc.py` ve kurulum (`install.py`) Faz C'nin işidir ve koşulmamıştır; ayarlı ve katı QC puanı bu yüzden henüz yoktur. TR şekilleri plan bölüm 12 madde 6 gereği ikinci turda aynı betiklerin dil seçeneğiyle üretilecektir; bu turda yalnız EN çizilmiştir. Y1, Y4 ve Y5 Visio ajanının şekilleridir; veri dosyaları (`konsey_b3_tarif.json`, `konsey_kayit_kurallari.json`, `konsey_zaman_cizelgesi.json`) ve föyün M13 bölümü (satır 2377) bu ajan çalışırken diskte bulunmuştur. Yayılım şeklinde föy her noktayı değil grup aralıklarını listeler; tekil noktalar föyün kaynak gösterdiği veri dosyasındaki tanım alanlarına karşı denetlenmiştir. Taban punto 8.0 pt ve 0.70 yükseklik payı IEEE kılavuzundan doğrulanmamış venue değerleridir (plan bölüm 12 madde 3).

## 7. Düzeltme turu 2 (çelişik doğrulayıcının on bir bulgusu)

Bu bölüm 31.10.2026 gecesi, çelişik doğrulayıcının on bir bulgusundan sonra aynı ajan rolüyle yazılmıştır. Her bulgunun kanıtı yeniden okunmuş, betikler düzeltilmiş, on bir şekil yeniden çizilmiş ve kapılar yeniden koşulmuştur. Visio açılmamış, `.tex` dosyalarına, föye, `results/` altına ve özgün şekil klasörlerine dokunulmamıştır. Birinci turun çıktıları (PDF, PNG, EPS, SVG, manifest, kanıt, denge yanıtı) kullanıcı değişikliği onaylayana kadar `paper/figures/charts/_tur1_yedek/` altında saklanmaktadır. Durum dosyası `paper/figures/visio_loglari/kart_ajani_tur2_durum.json`, komut günlüğü yine `paper/figures/visio_loglari/kart_ajani_komutlar.log`'dur.

En önemli üç sonuç şunlardır. Birincisi, on bir bulgunun dokuzu haklı bulunmuş ve düzeltilmiş, biri (eşik çizgileri) bu şekilde geçerli olmadığı için reddedilmiş, biri (köken kaydı) git kullanılmadan yapılabilecek kısmıyla düzeltilmiş, commit gerektiren kısmı kullanıcıya bırakılmıştır. İkincisi, on bir şeklin on biri varsayılan kapıların hepsinden yeniden geçmiştir; aralık çizen beş şeklin manifesti artık `errorbar_kinds` taşır ve Faz C'deki D3 denetimi gerçekten koşacaktır. Üçüncüsü, `--cizgi-kati` denetiminde belirteç dışı basılı kalınlık (0.4 ve 0.5 pt) hiçbir şekilde kalmamıştır; dört şeklin katı kipte düşmesi başıboş kalınlıktan değil, denetimin kullanılmayan belirteci ve bir üçgen işaretçiyi sorun saymasından gelir (bölüm 7.4).

### 7.1. Bulgu başına sonuç

| Bulgu (şiddet) | Şekil | Sonuç | Yapılan |
| --- | --- | --- | --- |
| 1. Simgeler düz harfe indi (sarı) | gradient_alignment, cells_interaction, estimates_forest | Düzeltildi | y ekseni "log τ̄" ve "log τ̄ residual" (U+0304 birleşik üst çizgi, DejaVu'da basılıyor); betik ayrıca `max |T - T^T| = 0`'ı föy karşılaştırmasına ekledi. Hücreler şeklinde iki satırlı "A(σ, scr) = −0.364" ve "I(σ) = +0.260"; ormanda satır "IN-V2 Ā(σ, IN)" (U+0100) ve alt x ekseni "directional term ρ or A(ρ)" |
| 2. Hata çubuğu anlamı manifeste yok (sarı) | estimates_forest, protocol_sets, protocol_settings, epsilon_sweep, feature_degradation | Düzeltildi | `_kart_ortak.hata()` SD için `annotate.errorbar(kind="sd")`'yi çağırır; motorun tanımadığı %90 aralığı `_kart_ortak.aralik()` ile `errorbar_kinds`'e yazılır. Manifestler: orman `[ci90, ci95]`, öznitelik `[ci90, sd]`, epsilon, protokol kümeleri ve Y7 `[sd]`; her manifest ek olarak `errorbar_tanimlari` alanında türün tanımını ve ci90 için gerekçeyi taşır. Öznitelik şeklinin anahtarına "bars: 90% interval (top), ±SD (middle, bottom)" satırı eklendi (yükseklik 121 mm, tavan 122) |
| 3. Negatif yönlü pay ayırt edilmiyor (sarı) | source_gap_split | Düzeltildi | ImageNetV2 çift 1'in negatif yönlü parçası (yonlu_pay −0.0445) beyaz dolgulu, ρ tonunda kesikli kenarlı çizilir; anahtara "negative directional part (narrows the gap)" girdisi eklendi, anahtar iki satıra çıktı (yükseklik 69 mm, tavan 72) |
| 4. Isı haritası basamakları (yeşil) | similarity_matrix | Kısmen düzeltildi | Basamak sınırları birleşik dağılımın beşte birlik dilimleri (0.05'e yuvarlanmış iç sınırlar); köşegen koyu gri (üslubun muted tonu) dolgulu ve anahtarda öyle. Mavi rampa ve beş basamak korundu, gerekçe bölüm 7.2 |
| 5. Eşik çizgileri logit satırlarını kesiyor (yeşil) | estimates_forest | Reddedildi | Bölüm 7.2 |
| 6. Tohum noktaları SD çizgisiyle üst üste (yeşil) | protocol_settings | Düzeltildi | Tohumlar 0.09 satır birimi yukarı kaydırıldı; SD çizgisi uç çentiksiz `annotate.errorbar`; Unconditioned işaretinin kenarı vurgu kalınlığında (0.55 pt); anahtara "SVHN: two pairs, no mean" girdisi; "L2" yerine "L₂" (yükseklik 84 mm, tavan 88) |
| 7. N'nin anlamı, '3.91' taşması (yeşil) | protocol_sets | Düzeltildi | Dipnot iki satır: "N: mean over the three seed pairs; CNN→ViT / ViT→CNN where the two differ". N'ler `results/c1_transfer/c1_transfer_summary.json` `protocols.<p>.n_cond_*.mean` alanlarına karşı denetlenir (7352.67 → 7,353, 7061.33 → 7,061; föy satır 31 "Ortak kume n = 7061±68"). '3.91' basamağın sağına alındı (yükseklik 118 mm, tavan 120) |
| 8. Etiket tutarsızlıkları (yeşil) | spread_clean_gap, epsilon_sweep | Düzeltildi | Yayılım anahtarı "L∞" ve "L₂" yazar (palet etiketinin görüntü biçimi; palet dosyası değişmedi); alt kart y ekseni "difference (pts)", çünkü kart başlığı niceliği tam adıyla yazar. Epsilon'da WRN-28-10 doğrudan etiketi iki satırlı "WRN-28-10 (one model)" |
| 9. Rapordaki 0.42 cümlesi yanlış (yeşil) | 06_kart_cizim.md | Düzeltildi | Bölüm 1'deki cümle düzeltildi; şablon ve tür eşlemesi bölüm 7.4'te açık sorun |
| 10. Köken kaydı eksik (yeşil) | on bir kanıt dosyası | Kısmen düzeltildi | `git` alanı artık girdileri, şekil betiğini, `_kart_ortak.py`'yi, içe aktarılan konsey modüllerini, föyü ve paleti izler; izlenmeyen ya da değişmiş olanlar `dirty_or_untracked`'ta görünür ve kod ile föyün SHA-256'sı `kod_ve_foy_sha256`'da durur. Yer tutuculu ya da yalnız kayıt düzeyinde kalan anahtar yolları (saldırı tarafı 30 değer, orman 70 değer, hücreler 12, gradyan 18) alan ve indis düzeyinde somut yollara çevrildi; saldırı tarafı ve ormanın 101 sayısal değeri kaynak dosyada yol izlenerek yeniden okundu, uyuşmayan 0. Commit gerektiren kısım bölüm 7.2'de |
| 11. Belirteç dışı çizgi kalınlıkları (yeşil) | altı şekil | Düzeltildi | `_kart_ortak.agirlik()` paletin `marker_edge` kalınlığını (0.4 pt) ve üslubun vermediği `referans_pt`, `baglayici_pt`, `egim_pt` varsayılanlarını (0.5 pt) en yakın `ST.weights` belirtecine bağlar; on bir şeklin basılı kalınlıkları artık yalnız 0.354, 0.49 ve 0.55 pt'dir |

### 7.2. Doğrulayıcı ile uyuşmazlık

Eşik çizgileriyle ilgili bulgu 5 reddedilmiştir, çünkü betik bu çizgileri zaten `ax.vlines(v, ylo, yhi)` ile yalnız log satırlarının y aralığında çizer (`yhi = idx[-1] + 0.5`, `ylo = -0.6`). Yeniden üretilen PNG'de ±0.10 kesikli ve −0.20 noktalı çizgiler son log satırının (IN-V2 Liu scr.) altındaki ayırıcı çizgide durur ve "H1 logit", "H2 logit" satırlarına inmez. Eksenin tamamını kesen tek dikey çizgi sıfır çizgisidir ve bu bilerek böyledir. Doğrulayıcının tarif ettiği kusur konsey özgününde vardır; bu şekle devralınmamıştır. Betikte değişiklik yapılmamış, yalnız bu gerekçe kararlar listesine yazılmıştır.

Bulgu 4'ün iki parçası uygulanmamıştır. Basamak sayısı yedi yapılmamıştır, çünkü Üslup 7 ısı haritası için tam beş ton (`isi_1`-`isi_5`) taşır ve altıncı ya da yedinci ton paletin taşımadığı türetilmiş bir renk olurdu; bilgi kaybı sorunu beşte birlik dilim sınırlarıyla giderilmiştir (CIFAR-10 hücrelerinin tek basamakta yığılması kalkmıştır). Rampa mavi kalmıştır, çünkü mavi dışı tek tonlu bir rampa üslup dışında yeni tonlar ister; doğrulayıcının ikinci seçeneği uygulanır ve altyazı "the blue ramp is not the ResNet (R224) colour" demelidir (bölüm 7.5).

Bulgu 3'ün "(>1)" seçeneği uygulanmamıştır, çünkü q sütunu 11 mm'dir ve "1.364 (>1)" sığmaz; q'nun 1'i aşmasının nedeni artık açık kesikli parçayla ve anahtar girdisiyle şeklin içinde görünür.

Bulgu 10'un commit kısmı bu turda yapılamaz, çünkü görev "git yok" der. Kurulumdan önce betiklerin (`paper/figures/charts/fig_*.py`, `_kart_ortak.py`, `_kart_kapilar.py`) commit edilmesi ve on bir şeklin o commit üzerinde bir kez daha üretilmesi gerekir; komut bölüm 7.6'dadır. O güne kadar kanıttaki `kod_ve_foy_sha256` kodu ve föyü sabitler. Kanıtlardaki commit artık `c315e09`'dur ve föy o commit'te değişmemiş görünür (SHA-256 öneki `c85fcfc1`).

Bulgu 2 için skill sahibinden `ci90` türü istenmemiş, tür manifeste gerekçesiyle yazılmıştır. `fig_qc.py` D3 türleri doğrulamaz, yalnız altyazıda "95%", "confidence interval", " ci", "standard deviation" gibi bir ifade arar; altyazıda "90% confidence interval" yazılması D3'ü geçirir.

### 7.3. Son kapı durumu

Varsayılan kapılar `paper/figures/charts/_kart_kapilar.py` ile koşulmuş, özet `paper/figures/qc/kart_kapilar_ozet.json`'dadır. Katı çizgi denetimi ayrıca `fig_mm_pdf.py --cizgi-kati` ile koşulmuş, raporları `paper/figures/qc/<kök>/fig_mm_pdf_cizgi_kati.json`'dadır.

| Kök | Kart denetçisi | fig_mm_pdf (8.0 pt) | denge (veri alanı payı) | Föy karşılaştırma / uyuşmayan | Yükseklik / tavan (mm) | errorbar_kinds | Zenginlik (kar/cm², yazı kutusu, sayısal, uzaklık) | --cizgi-kati |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| gradient_alignment | PASS 0 | PASS | kurulabilir (0.628) | 49 / 0 | 110 / 118 | yok | 1.94, 0.11, 0.44, 0.20 | PASS |
| source_gap_split | PASS 0 | PASS | kurulabilir (0.555) | 58 / 0 | 69 / 72 | yok | 2.81, 0.16, 0.43, 0.06 | PASS |
| similarity_matrix | PASS 0 | PASS | kurulabilir (uygulanmaz) | 93 / 0 | 56.98 / 70 | yok | 2.24, 0.12, 0.27, 0.39 | FAIL (0.49 belirteci kullanılmıyor) |
| cells_interaction | PASS 0 | PASS | kurulabilir (0.795) | 78 / 0 | 121 / 125 | yok | 2.72, 0.15, 0.27, 3.39 | PASS |
| attack_side | PASS 0 | PASS | kurulabilir (0.666) | 47 / 0 | 95 / 98 | yok | 2.83, 0.16, 0.38, 0.00 | FAIL (0.49 belirteci kullanılmıyor) |
| estimates_forest | PASS 0 | PASS | kurulabilir (0.672) | 76 / 0 | 127 / 130 | ci90, ci95 | 3.38, 0.18, 0.21, 3.21 | PASS |
| protocol_sets | PASS 0 | PASS | kurulabilir (0.472) | 36 / 0 | 118 / 120 | sd | 4.35, 0.24, 0.20, 2.58 | PASS |
| spread_clean_gap | PASS 0 | PASS | kurulabilir (0.789) | 48 / 0 | 119 / 122 | yok | 3.04, 0.17, 0.37, 2.89 | PASS |
| epsilon_sweep | PASS 0 | PASS | kurulabilir (0.590) | 28 / 0 | 62 / 66 | sd | 2.70, 0.16, 0.33, 0.00 | FAIL (0.55 belirteci kullanılmıyor) |
| feature_degradation | PASS 0 | PASS | kurulabilir (0.777) | 169 / 0 | 121 / 122 | ci90, sd | 3.01, 0.17, 0.53, 3.15 | FAIL (üçgen işaretçi 1.302 mm ok ucu sanılıyor) |
| protocol_settings | PASS 0 | PASS | kurulabilir (0.560) | 75 / 0 | 84 / 88 | sd | 3.10, 0.17, 0.26, 0.00 | PASS |

Öznitelik bozulmasında sayısal oran 0.56'dan 0.53'e inmiş ve uyarı eşiğinin (0.55) altına düşmüştür. Protokol kümelerinde karakter yoğunluğu 4.35'tir; blok eşiği 4.5 olduğu için geçer, ama iki satırlı dipnot onu eşiğe yaklaştırmıştır. Gradyan şeklinin föy karşılaştırma sayısı, üç veri kümesinde log τ matrisinin simetri denetimi eklendiği için 46'dan 49'a çıkmıştır.

### 7.4. Yeni açık sorunlar (skill ve palet sahibine)

7. `scripts/zenginlik.py` şeklin türünü şablondan türetir ve `tasarim_izgarasi` şablonuyla çizilen veri şekillerini şematik sayar; bu yüzden hücreler, orman, öznitelik, yayılım ve protokol kümeleri şekilleri şematik ton (0.06-0.49) ve boşluk (0.421-0.778) aralıklarına karşı ölçülür ve beğeniye uzaklıkları 2.6-3.4 çıkar. Kart motorunun manifesti `kind` ve veri ekseni taşıdığı hâlde tür şablondan okunmaktadır; tür manifestten (kart motoru, eksen sayısı) okunmalı ya da `tasarim_izgarasi` için veri aralıkları tanımlanmalıdır.
8. `fig_mm_pdf.py --cizgi-kati` bir şeklin kullanmadığı belirteci ("token width(s) never printed") sorun sayar; tek kartlı bir şeklin vurgu çizgisi yoksa ya da ısı haritasında normal çizgi yoksa şekil düşer. Kullanılmayan belirteç uyarı olmalı, yalnız belirteç dışı basılı kalınlık katı kipte sorun sayılmalıdır. Aynı kipte öznitelik şeklinin üçgen işaretçisi 1.302 mm'lik bir ok ucu olarak okunmuştur (kart şekli hiç ok çizmez, manifest `naming.flows` boştur).
9. `motor/figspec/annotate.ERRORBAR_KINDS` %90 aralığını tanımaz; ön kayıtlı eşdeğerlik (TOST) ve ön kayıtlı %90 kestirim aralıkları bu makalede ana sonuçtur. `ci90` türü eklenmeli ve D3'ün altyazı sözcük listesine "90%" girmelidir.
10. Matplotlib taraması (`hatch`) PDF'e 72 pt'lik desen karoları olarak yazılır ve `fig_mm_pdf` bunları kapalı kutu sayıp yazıların bu kutulardan taştığını söyler (kaynak açığı şeklinin ilk denemesinde dört "box_spill" sorunu). Kart şekillerinde tarama bu yüzden kullanılamaz; desen karoları kapalı kutu sayılmamalıdır.
11. Paletin `ayar_c100` tonu (#6597B0) `r32` tonuna CIEDE2000 ile 10.69 uzaklıktadır (palet başlığı); iki ton aynı şekilde birlikte çizilmez, ama palet üreteci bu çifti ayrıştırmalıdır. Paletin `prot_raw` tonu (#E7D4E8) üslubun çizim alanına (#EAEAF2) çok yakındır; bu turda işaret kenarı kalınlaştırılmış, ton değiştirilmemiştir (palet yalnız `_palet_uret.py` ile üretilir).

### 7.5. Faz C altyazısına eklenecekler

| Şekil | Altyazıda yazılacak |
| --- | --- |
| gradient_alignment | Eksen "log τ̄" metindeki log τ̄_ij'dir |
| cells_interaction | "A(σ, scr)" metindeki A^σ_scr (H1), "I(σ)" metindeki I^σ (H2) |
| estimates_forest | "Ā(σ, IN)" metindeki Ā^σ_IN, "A(ρ)" metindeki A^ρ (H3); kalın çubuk %90, ince çizgi %95 aralık (ImageNetV2 satırlarında görüntü bootstrap aralığı) |
| feature_degradation | Üst kartta çubuklar TOST dosyasının %90 aralığı, orta ve alt kartta ±1 SD (ddof = 1); eski altyazının %95'i değişir |
| epsilon_sweep, protocol_sets, protocol_settings | Çubuklar ±1 SD, üç tohum çifti üzerinden; protokol kümelerinde N üç tohum çiftinin ortalamasıdır; Y7'de SVHN'in iki çifti ortalamasız çizilir |
| similarity_matrix | Basamak sınırları birleşik beşte birlik dilimlerdir; mavi rampa ResNet (R224) rengi değildir; koyu gri köşegen tanımsızdır |
| source_gap_split | Açık, kesikli kenarlı turuncu parça negatif yönlü paydır ve açığı daraltır (ImageNetV2 çift 1, q > 1) |

### 7.6. Dosyalar ve kullanıcıya kalan komut

Değişen betikler `paper/figures/charts/_kart_ortak.py` ve on bir `paper/figures/charts/fig_<kök>.py`'dir; yama betikleri bu ajanın karalama klasöründedir (`.../scratchpad/kart2/`). Her şeklin PDF, PNG, EPS, SVG, `.fig.json`, `.mm.json`, `.kanit.json` ve `.denge_ajan.json` dosyaları yeniden yazılmıştır; QC raporları `paper/figures/qc/<kök>/` altındadır. Birinci tur yedeği `paper/figures/charts/_tur1_yedek/` (88 dosya) kullanıcı onayına kadar silinmez.

Kurulumdan önce kullanıcının koşması gereken komut (git bu ajana kapalıdır):

```bash
cd /home/firat/projects/adeb_sci_1
git add paper/figures/charts/_kart_ortak.py paper/figures/charts/_kart_kapilar.py paper/figures/charts/fig_*.py
git commit -m "Kart veri sekilleri (Uslup 7) betikleri: duzeltme turu 2"
for s in gradient_alignment source_gap_split similarity_matrix cells_interaction attack_side estimates_forest protocol_sets spread_clean_gap epsilon_sweep feature_degradation protocol_settings; do python paper/figures/charts/fig_$s.py --uslup 7; done
python paper/figures/charts/_kart_kapilar.py gradient_alignment source_gap_split similarity_matrix cells_interaction attack_side estimates_forest protocol_sets spread_clean_gap epsilon_sweep feature_degradation protocol_settings
```

Betikler Windows Python'la yazılmıştır; WSL'de koşulacaksa skill yolu (`_kart_ortak.SKILL`) ve yazı tipleri o ortamda da çözülmelidir, aksi hâlde aynı komutlar Windows Git Bash'ten `//wsl.localhost/Ubuntu-22.04/home/firat/projects/adeb_sci_1` kökünden koşulur.
