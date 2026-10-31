# Şekil envanteri, venue, aday pasajlar ve panel adlandırma planı (visio-cizici, adım 1, 2 ve 4)

Tarih 31.10.2026. Hazırlayan görsel üretici ajan (gorsel-uretici). Makale IEEE Access için yazılmış EN el yazmasıdır (`paper/manuscript/main.tex`, ieeeaccess.cls, 25 sayfa); TR aynası `paper/manuscript_tr/main.tex` aynı etiketleri taşır (IEEEtran taslağı, 26 sayfa). Bu raporun hiçbir adımı `.tex` dosyalarına, orijinal şekillere ya da veri dosyalarına dokunmamıştır. "Önce" kaydı `00_once.md`'dedir.

En önemli üç sonuç şunlardır. Birincisi, venue ölçülmüştür ("olculdu"): tek sütun 85.290 mm, tam genişlik 177.530 mm, metin yüksekliği 236.181 mm, gövde 10 pt; görev metnindeki 3.5 in ve 7.16 in sınıfla tutmaz. Ancak `ieee_access` skill'in venue kaydında yoktur ve kaydedilene kadar hiçbir çizim betiği koşmamalıdır, çünkü venue verilmeyen motor MDPI geometrisine düşer (bölüm 1). İkincisi, makalenin 12 şeklinin hepsinin veri dosyası vardır ve bugün de kayıtlı özetleriyle aynıdır, yani eski şekiller için "veri gerekli" yoktur; veri gereken yerler yalnız önerilen yeni şekillerdir (bölüm 5). Üçüncüsü, metinde yalnız bir panel atfı vardır; bu yüzden yedi şeklin harfli panel düzeni kalkar ve harf yalnız şekil 1'de, şartlı olarak kalır (bölüm 6).

## 1. Venue ve proje ayarı

`scripts/venue_probe.py --tex` üç denemede "olculdu" vermiştir. İlk deneme Windows Python'a ters bölülü UNC yolu verildiğinde `\\wsl.localhost\Ubuntu-22.04\wsl.localhost\...` diye iki kez birleşen bir yolla düştü; çözüm, yolu `//wsl.localhost/Ubuntu-22.04/...` biçiminde ve Git Bash'te `MSYS_NO_PATHCONV=1` ile vermektir. İkinci deneme sınıfın yazı tipi metrikleri (`t1-formata-regsymb.tfm` ve ötekiler) probe klasörüne kopyalanmadığı için ölümcül hatayla bitti; dosyalar `--kopyala` ile verildi. Üçüncü deneme ölçüleri okudu ama pdflatex 1 ile çıktı, çünkü ieeeaccess.cls belge sonunda `\EOD` ister (cls satır 1080) ve probe metni kesip `x \end{document}` ekler. Çözüm olarak `main.tex`'in karalama klasöründe bir kopyası yazıldı (`kopya_yap.py`; tek fark `\titlepgskip` satırından sonra eklenen `\EOD`) ve probe o kopyayla koşuldu. Makalenin kendisi değişmedi.

| Ölçü | pt | mm | Kaynak |
| --- | --- | --- | --- |
| `\columnwidth` (tek sütun) | 242.67355 | 85.290 | probe, cls satır 262 ile aynı |
| `\textwidth` (tam genişlik) | 505.12177 | 177.530 | probe, cls satır 263 |
| `\textheight` | 672.0 | 236.181 | probe, cls satır 265 |
| `\columnsep` | 19.77464 | 6.950 | probe, cls satır 261 |
| gövde | 10 | | probe `\f@size` |
| altyazı | 7 | | cls satır 218-219 (`\figcapfont`, Formata) |

İki sütun özdeşliği tutar (2 x 242.67355 + 19.77464 = 505.12174 pt, fark 0.00003 pt). Ölçülmeyip karar olarak yazılan alanlar şunlardır: taban punto 8.0 pt (`min_type_abs_pt` 8.0, oran 0.80); en çok şekil yüksekliği metin yüksekliğinin 0.70'i, yani 165.33 mm; PNG 600 dpi. Karar: taban 8.0 pt alınmıştır, çünkü makalenin şekil modülü (`konsey_ortak.py` `MIN_FONT`) ve skill'in IEEE yer tutucusu bu değeri kullanır; IEEE yazar kılavuzu bu oturumda okunmamıştır ve değer doğrulanmamış sayılır. Karar: yükseklik payı 0.70 alınmıştır, çünkü sınıf `\topfraction` ve `\dbltopfraction` tanımlamaz ve LaTeX varsayılanı 0.7'dir; motorun varsayılan 0.45'i (106.3 mm) bugünkü şekil 1'i (yaklaşık 129 mm) ve şekil 8'i (127 mm) bloklar.

Önerilen `Venue(...)` bloğu `venue_ieee_access_blok.txt`'tedir. Karar: blok skill'in `motor/figspec/venues.py` dosyasına yazılmamıştır, çünkü skill değişikliği bu fazın yazma alanı dışındadır ve ana oturumun kararıdır. Bu yüzden proje ayarındaki `venue: ieee_access` satırı yorumdadır; denendiğinde ayar dosyası doğru okunmakta ve `venues.default_name()` `mdpi_biomedicines_submit` döndürmektedir.

Proje ayarı `paper/figures/visio_cizici.yaml` olarak yazılmıştır. Skill ayarı `<kök>/figures/visio_cizici.yaml`'da arar; bu depoda şekil klasörü `paper/figures` olduğu için her komuta `VZ_PROJE_KOKU` (depo kökü) ve `VZ_PROJE_AYARI` (bu dosya) verilir. İçerik: kurulum hedefi `paper/figures` (kurulum adları `fig<N>_<kök>` olduğu için `final/`, `final_tr/` ve `konsey/` dosyalarıyla çakışmaz), Visio yapımı `paper/figures/visio`, kart yapımı `paper/figures/charts`, QC `paper/figures/qc`, önizleme `paper/figures/onizleme`, günlükler `paper/figures/visio_loglari`, eşleme `paper/figures/qc/ESLEME.md` (henüz yazılmadı), dil `en`, oturum DPI'ı 120. DPI Windows'tan iki yoldan okunmuştur: motorun `visio_dpi()`'ı `GetDeviceCaps(LOGPIXELSX)` ile 120 verdi, kayıt defterindeki `AppliedDPI` de 120'dir; Visio basım ızgarası 0.6 pt'dir. Makalenin paleti `konsey_ortak.py` içindeki Okabe-Ito sözlükleridir (ViT #D55E00, R224 #0072B2, R32 #56B4E9, panel #999999, XCiT #CC79A7, simetrik bileşen #009E73, yönlü bileşen #E69F00); motorun okuduğu biçimde bir palet YAML'ı yoktur ve çizim fazında `paper/figures/visio/palettes/adeb_konsey.yaml` olarak üretilip `palette:` satırı açılacaktır.

## 2. Envanterin nasıl çıkarıldığı

`included_figures.py` `\input` ağacını izlemez, `vz_duzlestir.py` ise `\InputIfFileExists` satırlarını açmaz; makalede ek ve hesaplama bölümü bu komutla girdiği için ilk düz kopya 10 şekil gördü. Karalama klasöründe her `\input` ve `\InputIfFileExists` satırını mutlak yollu `\input`'a çeviren bir kaynak kopyası yazıldı ve düzleştirme onun üzerinde koşuldu (`paper/figures/qc/main_en_duz.tex`, `main_tr_duz.tex`). Bu kopyalarla iki dilde 12 şekil okundu ve numaralar derlenmiş `main.aux` ile birebir tutar. Bu, skill için bir açık sorundur: `vz_duzlestir.py` `\InputIfFileExists{x}{}{}`'i de açmalıdır.

| No | Etiket | Bugünkü dosya | Kurulum adı önerisi | Sayfa (EN) |
| ---: | --- | --- | --- | ---: |
| 1 | fig:study_overview | konsey/fig_study_overview.pdf (TikZ) | fig1_study_overview | 5 |
| 2 | fig:decomposition_schematic | konsey/fig_decomposition_schematic.pdf | fig2_decomposition_schematic | 6 |
| 3 | fig:source_gap_split | konsey/fig_source_gap_split.pdf | fig3_source_gap_split | 11 |
| 4 | fig:similarity_matrix | konsey/fig_similarity_matrix.pdf | fig4_similarity_matrix | 11 |
| 5 | fig:cells_interaction | konsey/fig_cells_interaction.pdf | fig5_cells_interaction | 14 |
| 6 | fig:attack_side | konsey/fig_attack_side.pdf | fig6_attack_side | 15 |
| 7 | fig:gradient_alignment | konsey/fig_gradient_alignment.pdf | fig7_gradient_alignment | 16 |
| 8 | fig:estimates_forest | konsey/fig_estimates_forest.pdf | fig8_estimates_forest | 17 |
| 9 | fig:protocol_sets | konsey/fig_protocol_sets.pdf | fig9_protocol_sets | 18 |
| 10 | fig:spread_clean_gap | final/ (TR'de final_tr/) fig_spread_clean_gap.pdf | fig10_spread_clean_gap | 18 |
| 11 | fig:epsilon_sweep | final/fig2_epsilon_sweep.pdf | fig11_epsilon_sweep | 21 |
| 12 | fig:feature_degradation | final/fig5b_attention_entropy.pdf | fig12_attention_entropy | 22 |

`included_figures.py` 11 ve 12 için STALE yazar, çünkü dosya adındaki eski numara basılı numarayla tutmaz. Kurulum adları yeni şekiller girince yeniden numaralanacaktır (bölüm 6.3); eşleme dosyası elle yazılacaktır.

## 3. Şekil envanteri

Tür, iddia ve veri kaynağı aşağıdadır. İddia altyazıdan ve şekle atıf yapan metinden alınmıştır. Veri kaynağı her şeklin `.kanit.json` dosyasının girdi listesidir; listedeki her dosya bugün vardır ve kayıtlı SHA-256'sı olanların hepsi aynıdır (taranan 12 kanıt dosyası, tek eksik `paper/figures/fig_protocol_sets_v1.py`, yalnız bir önceki betiğin adı olarak geçer).

| No | Tür | Taşıdığı iddia | Veri kaynağı (kanıt dosyası girdileri; föy) |
| ---: | --- | --- | --- |
| 1 | şematik | Çalışma tasarımı: çift ve 2x2 tasarım, üç veri kümesinde sabit paneller, w-τ-r ayrışımı, kayıtlı aileler ve protokol katmanı | hücre tabloları (`raporlar/konsey_2026-10-29/hucre_tablosu*.json`), `konsey_b10_gradyan/mantel_*.json`, `konsey_b8_imagenetv2/b8_dondurulmus_b2.json`; 19 föy karşılaştırması (model sayıları 20/15/14) |
| 2 | şematik (denklem zinciri) | log T tam olarak kırılganlık, simetrik benzerlik ve yarım yön artığına ayrılır; panel ortalamaları σ ve ρ kaynak açığını simetrik ve yönlü paya böler | sayı çizmez; 2 özdeşlik denetimi (rastgele matrislerde artık) |
| 3 | veri grafiği | ViT'nin CNN eşine göre kaynak açığının büyük kısmı simetriktir (q), C10 ve C100 tohum çiftlerinde; IN-V2 çiftleri betimseldir | `konsey_ayrisim_b2.json`, `b9_dondurulmus_b2.json`, `b8_dondurulmus_b2.json`; 58 föy karşılaştırması |
| 4 | veri grafiği | V-scr tohumları kendi aralarında benzer, CNN panelinden farklı bir blok oluşturur | `konsey_ayrisim_b2.json`, `_b4.json`, B8, B9, hücre tabloları, mantel dosyaları; 93 karşılaştırma |
| 5 | veri grafiği | 2x2 tasarımda σ'da mimari farkı (H1) ve etkileşim (H2), ρ'da eşdeğerlik (H3), ω | `konsey_ayrisim_b4.json`, `_b2.json`, `hucre_tablosu.json`; föy M9.2 (satır 1490 civarı); 78 karşılaştırma |
| 6 | veri grafiği | Kaynak açığı her kaynağın en iyi saldırısı altında korunur; TGR hiç seçilmez | `konsey_ayrisim_b5.json`, `hucre_tablosu.json`; föy M9.5; 47 karşılaştırma |
| 7 | veri grafiği | Girdi gradyanı kosinüsü simetrik benzerliği üç veri kümesinde, ham ve toplamsal model etkileri çıkarılmış hâlde izler | üç `mantel_*.json`, hücre tabloları; 46 karşılaştırma |
| 8 | veri grafiği | Kayıtlı kestirimler log ve logit ölçekte; yön terimi log ölçekte ±0.10 içinde, logit'te değil; IN-V2 aralıkları karşılaştırılamaz | `konsey_ayrisim_b4.json`, `_b2.json`, `b9_dondurulmus_b2.json`, `b8_betimsel.json`; 76 karşılaştırma |
| 9 | karma (şematik ve veri) | Dört koşullama protokolü iç içe kümelerdir ve aynı modellerde farklı asimetri verir; adımlar özdeşlik terimi, marjinal alt kümeler ve kaynak sağlamlığıdır | `results/q1/fig_protokol_kumeleri_veri.json`, `results/c1_transfer/c1_transfer_summary.json`; 33 föy karşılaştırması (föy satır 53 vb.) |
| 10 | veri grafiği | Protokol yayılımı 60 model çiftinde temiz doğruluk farkıyla artar; başarılı-kaynak eksi her-ikisi-doğru ayrı bir terimdir | `results/q1/fig_yayilim_temiz_fark_veri.json` ve onun 18 üst kaynağı (c1_c3, c1_seeds, c1_transfer, q1/cifar100, cifar10_l2, svhn, havuz, son kontrol noktası, temiz çiftler) |
| 11 | veri grafiği | PGD-10 sağlam doğruluk ε ile düşer, CNN avantajı korunur; tarama Tablo 4'ten en çok 0.08 puan ayrılır | `results/c1_sweep/pair*/` altı CSV, `results/wrn_eval/wrn_eval_summary.json`; föy satır 352-375 |
| 12 | veri grafiği | ViT CLS dikkat entropisi değişimi ±0.05 nat eşdeğerlik marjı içindedir; TV yer değiştirmesi katmana göre | `results/c1_c4/pair1-3/c4_summary.json`; föy satır 326-351 |

Kompozisyon, önerilen şablon (skill kataloğunun dokuz şablon türünden), 3B'ye uygun nesne ve motor aşağıdadır. 3B yalnız şematik nesnelerde önerilir; eksenli veri grafiği 3B çizilmez.

| No | Bugünkü kompozisyon | Panel | Önerilen şablon | 3B'ye uygun nesne | Motor |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Dört gri kap (a-d): modeller, paneller, ölçüm zinciri, kayıtlı aileler ve protokol bandı; matplotlib/TikZ, 172 x 129 mm | 4 | `yontem_semasi`, içinde `ic_ice_izgara` | Model blokları (ResNet-18 ve ViT-Tiny), RobustBench kontrol noktası desteleri, tohum başına transfer matrisi levha yığını | Visio |
| 2 | Dört katlı denklem zinciri (a-d), 2x2 matris ve renkli terimler; 85 x 90 mm | 4 | `yontem_semasi` (dikey akış) | İsteğe bağlı: 2x2 transfer matrisi levhası, köşegende w | Visio |
| 3 | Üç çubuk paneli, simetrik ve yönlü pay yığılı, q etiketi; tam genişlik | 3 | `ortak_satirli_katlar` | yok | kart |
| 4 | Üç ısı matrisi, aileye göre sıralı; tam genişlik | 3 | `ortak_satirli_katlar` (ortak sıralama, ortak renk ölçeği) | yok | kart |
| 5 | Üst üste üç etkileşim grafiği (σ, ρ, ω), hücre ortalaması çizgi, koşum işaretçi; 85 x 121 mm | 3 | `tasarim_izgarasi` verisi olarak `ortak_satirli_katlar` | yok | kart |
| 6 | Tek panel nokta grafiği, tohum satırları, saldırıya göre işaretçi | 1 | `tek_kart_veri` | yok | kart |
| 7 | 2 x 3 dağılım ızgarası (a-f) | 6 | `ic_ice_izgara` | yok | kart |
| 8 | İki orman grafiği (a, b), %90 ve %95 aralık | 2 | `ortak_satirli_katlar` | yok | kart |
| 9 | Sol: iç içe dört kutu (A-D, mavi tonlar); sağ: basamaklı asimetri grafiği; 88.9 x 105 mm | 2 | `tablodan_sekle` (Tablo 2'nin maskeleri halkalara girer) ve veri kartı | Sol panelde iç içe kümeler üst üste levha olarak çizilebilir; sağ panel 2B kalır | kart (karar bölüm 7) |
| 10 | İki dağılım grafiği (a, b), sekiz grup işaretçi ve renk; 88.9 x 124 mm | 2 | `ortak_satirli_katlar` (ortak x ekseni) | yok | kart |
| 11 | Tek çizgi grafiği, üç seri; 88.9 x 65 mm | 1 | `tek_kart_veri` | yok | kart |
| 12 | İki panel (a, b), katman ekseni; 88.9 x 91 mm | 2 | `ortak_satirli_katlar` | yok | kart |

Şekillerin hiçbiri görüntü paneli değildir; makalede örnek görüntü ya da çekişmeli örnek gösteren bir şekil yoktur ve bunu üretmek kapsayıcı ve GPU ister, bu yüzden önerilmez.

## 4. Mevcut şekillerde bulunan sorunlar

Bu sorunlar yeniden çizimde giderilecektir; metinde düzeltme gerektirenler bölüm 6.2'deki listeye girmiştir.

1. Şekil 1 ve 2 şeklin içinde (a)-(d) harfleri taşır, ama altyazıları hiçbir paneli anmaz. Kural, şekildeki adla altyazıdaki adın harfiyen aynı olmasını ister.
2. Şekil 9, 10, 11 ve 12 3.5 in (88.9 mm) genişlikte çizilmiş ve `\columnwidth` (85.29 mm) ile yerleştirilmiştir; ölçek 0.959'dur ve 8 pt yazı 7.67 pt basılır. Konsey şekilleri bu düzeltmeyi 31.10.2026'da almıştır, bu dördü almamıştır. Şekil 9'un kanıt dosyası 8.89 cm'yi "başlık sığması için" bilerek tuttuğunu yazar.
3. Şekil 9'un iç içe kutuları mavi tonlarla doldurulmuştur; aynı makalede mavi (#0072B2) R224'ü kodlar. Şekil 10'da turuncu, yeşil, mavi ve kırmızı-turuncu grupları kodlar, oysa bu renkler öteki şekillerde yönlü bileşen, simetrik bileşen, R224 ve ViT'tir. "Bir hex bir aile" kuralı makale düzeyinde bozulmaktadır.
4. Şekil 1 (129 mm), 5 (121 mm), 7 (121 mm) ve 8 (127 mm) motorun varsayılan yükseklik bütçesini (106.3 mm) aşar; önerilen 0.70 payıyla (165.3 mm) geçerler.
5. Konsey şekillerinin kanıt dosyaları föyün eski özetini taşır (bölüm `00_once.md` 4). Veri JSON'ları değişmemiştir, ama yeniden çizimde föy karşılaştırmaları bugünkü föyle yeniden koşulmalıdır; karşılaştırmalar satır numarası ve çapa dizgesiyle yapıldığı için kaymış bir föy sessizce yanlış satırı eşlemez, yüksek sesle düşer.
6. Şekil 11'in WRN-28-10 çizgisi `results/wrn_eval/wrn_eval_summary.json`'dan gelir. Bu yol karantina kuralının geçerli saydığı `results/c1_*` ve `results/q1/*` dışındadır; föy ise aynı dosyayı satır 354'te kaynak gösterir ve değerleri satır 19'da taşır. Karar: çizgi korunabilir, çünkü değer föydedir; ancak yeni betikte kaynak `konsey_ortak.ALLOWED`'a açıkça eklenmeli ve kanıt dosyasına föy satırı yazılmalıdır.
7. Şekil 4 ve 7'nin altyazısındaki panel adlarını sayaç eksik okur (4'te yalnız b, 7'de a, c, d), çünkü altyazı "CIFAR-10 (a), CIFAR-100 (b)" ve "(a) to (c)" biçimindedir. Bu sayaç sınırıdır; karar etkilenmez, çünkü iki şeklin de harfleri kalkmaktadır.

## 5. Aday pasajlar, yeni şekil önerileri ve sayfa bütçesi

Bütçe şu varsayımlarla hesaplanmıştır: gövde satırı 12 pt = 4.233 mm, bir sütun 56 satır, sayfa 112 sütun satırı; tek sütunda satır başına yaklaşık 11 sözcük (ölçülmedi, tahmin); bir şeklin maliyeti şekil yüksekliği, yaklaşık 12 mm altyazı ve 7 mm kayan nesne aralığının toplamıdır ve tam genişlik şekil iki sütunu birden tüketir. Tablo yükseklikleri derlenmiş PDF'te başlık üstünden alt booktabs çizgisine ölçülmüştür (PyMuPDF; Tablo 8, 10, 13 ve 16 ölçülemedi, satır sayısından tahmin edildi). Metni yazım ajanı kısaltır; aşağıdaki "serbest kalan" sütunu yalnız bir üst sınırdır. Eksi net değer ana metnin kısaldığını gösterir.

| Kod | Metindeki yer (EN satır; TR karşılığı) | Öneri | Şablon ve 3B | Serbest kalan | Şekil maliyeti | Net (sütun satırı) |
| --- | --- | --- | --- | --- | --- | --- |
| Y1 | 3.4 Design (03_methodology 90-131, Tablo 1 satır 104) ve 3.3 Adversarial Training'in tarif kısmı (72-89); TR 03_yontem 64-123 | `fig:design_recipe`: 2x2 hücre ızgarası; her hücrede 3B model bloğu (R224 7x7 kök, ViT-Tiny 16x16 yama, 12 blok, genişlik 192, 3 baş), giriş hattı 32'den 224'e, başlatma (rastgele, DeiT-Ti, RSB A1), temiz evre, tohumlar; altta ortak AT tarifi şeridi; köprü hücresi R32 yanda | `model_acilimi_3b` ve `tasarim_izgarasi`; tek sütun 85 x 88 mm | Tablo 1 (47.7 mm, 12.9 satır) ve yaklaşık 250 sözcük (22.7 satır) | 25.3 | yaklaşık -10 |
| Y2 | 3.6 Reference Panels (193-216; TR 185-208), 547 sözcük, RobustBench kimlikleri | Panel üyeleri şekil 1'in panel kabına taşınır: üç veri kümesi sütunu, her üye bir kontrol noktası destesi, ResNet-18 türevleri ve ikincil üyeler işaretli; atıflar metinde tek cümlede kalır | `tablodan_sekle`, şekil 1 içinde; 3B deste | yaklaşık 300 sözcük (27.3) | şekil 1'e yaklaşık 20 mm (9.5) | yaklaşık -17 |
| Y3 | 3.7 Conditioning Protocols, Tablo 2 (03_methodology 217-262; TR 209-254) | Tablo 2'nin maskeleri şekil 9'un iç içe kümelerine yazılır, tablo kalkar | `tablodan_sekle`, şekil 9 içinde | Tablo 2 (42.1 mm, 11.6) ve yaklaşık 60 sözcük (5.5) | şekil 9'a yaklaşık 15 mm (3.5) | yaklaşık -14 |
| Y4 | 3.9 Statistical Inference karar okuma paragrafı ve Tablo 3 (282-334; TR 274-326) | `fig:registry_map`: kayıtlı aileler satır satır (panel C10, 2x2, saldırı tarafı, maskeleme, C100, IN-V2 betimsel, gradyan); her satırda nicelik, öngörü eşiği ve ±δ bandı küçük bir sayı doğrusunda, sınama ve çürütme kuralı; isteğe bağlı olarak sonuç işareti | `tablodan_sekle` (kural merdiveni); tam genişlik 95 mm | Tablo 3 (86.7 mm, tam genişlik, 44.3) ve yaklaşık 150 sözcük (13.6) | 53.9 | yaklaşık -4; Tablo 3 eke giderse toplam sayfa değişmez |
| Y5 | 3.10 Pre-Registration (335 sonrası; TR 327 sonrası), 442 sözcük; Tablo 3 altyazısındaki blok cümlesi; 4.11 Computational Details'ın blok süreleri | `fig:prereg_chain`: zaman şeridi (29.10 ana kayıt dondurma, B2-B6 koşuları, 30.10 ek kayıt, B8-B10), her blokta model, görüntü ve matris sayısı, kayıttan önce görülen veriler ayrı bir şeritte, iki sapma işaretli | `sayim_akisi`; tam genişlik 60 mm | yaklaşık 300 sözcük (27.3), altyazı cümlesi (4), hesaplama ayrıntılarından yaklaşık 100 sözcük (9) | 37.3 | yaklaşık -3 |
| Y6 | 4.4 Architecture by Initialization, Tablo 8 (tab:cells, 04_experiments 254; TR 255) | Şekil 5'e temiz doğruluk ve PGD-10 ile AutoAttack farkı (maskeleme denetimi, ilk 1000 görüntü) kartları eklenir; Tablo 8 eke taşınır | `tasarim_izgarasi` verisi | Tablo 8 (yaklaşık 64 mm, tam genişlik, 33.6) | şekil 5'e yaklaşık 35 mm (8.3) | ana metinde yaklaşık -25 |
| Y7 | 4.10 The Conditioning-Protocol Layer, Tablo 13 (556; TR 557) ve çevresindeki yaklaşık 150 sözcük | `fig:protocol_settings`: satırlar ayarlar (C10 L∞, C10 L2, C100, SVHN, ...), sütunlar dört protokol, nokta ±SD ve tohum çiftleri; yayılım sağ kenarda | `ortak_satirli_katlar`; tek sütun 85 x 70 mm | Tablo 13 (yaklaşık 45 mm, tam genişlik, 24.6) ve 13.6 | 21.1 | yaklaşık -17 |
| Y8 | Ek A, Tablo 16 (tab:feature_degradation, 07_appendix 90) | Katman başına blok çıkışı kosinüsü şekil 12'ye üçüncü kart olarak girer | `ortak_satirli_katlar` | Tablo 16 (62.8 mm, 16.5) | şekil 12'ye yaklaşık 30 mm (7.1) | ekte yaklaşık -9 |
| Y9 | 4.6 ImageNetV2, Tablo 11 üst blok (404; TR 405) | İsteğe bağlı: 14 modelin temiz ve sağlam doğruluğu ile σ'sı sıralı nokta grafiği; kimlikler ekteki tabloda kalır | `ortak_satirli_katlar` | Tablo 11'in yarısı (yaklaşık 41 mm tam genişlik, 21) | yaklaşık 20 | yaklaşık -1; düşük öncelik |

Önerilmeyenler ve nedenleri şunlardır. Tablo 7 (panel sınamaları) ve Tablo 9 (2x2 ailesi) kayıtlı kararların kendisini taşır; hakem bu sayıları tabloda arar ve şekil 8 onları zaten görselleştirir, bu yüzden tablolar kalır. Tablo 5 (çift ayrışımı) şekil 3 ile kısmen örtüşür, ama tohum başına standart sapmaları taşıdığı için kalır. Sınırlılıklar (616 sözcük) ve giriş görselleştirilebilir bir yapı taşımaz. Tehdit modeli ve saldırı yöntemleri paragrafları (121 ve 187 sözcük) Y1'in model açılımı içinde kısmen karşılanır; ayrı şekil önerilmez.

Toplamda Y1-Y7 kabul edilirse makaleye dört yeni şekil girer (Y1, Y4, Y5, Y7), üç şekil büyür (1, 5, 9), dört tablo kalkar ya da eke gider (1, 2, 3 ya da eke, 8 eke, 13); ana metin kabaca 90 sütun satırı, yani yaklaşık 0.8 sayfa kısalır. Şekil sayısı 12'den 16'ya çıkar. Toplam sayfa sayısı tabloların eke taşınıp taşınmamasına bağlıdır ve derlemeden önce kesin söylenemez.

## 6. Veri gerekli listesi

Eski 12 şeklin hiçbiri "veri gerekli" değildir; hepsinin veri dosyası vardır ve çizilen her sayı bir JSON ya da CSV anahtarından okunabilir (bölüm 3). Veri gereken yerler önerilen yeni şekillerdir:

| Şekil | Eksik olan | Gereken dosya |
| --- | --- | --- |
| Y1 `fig:design_recipe` | Eğitim tarifinin hiperparametreleri (AdamW, öğrenme oranı 1e-3, ağırlık azaltma 0.05, batch 64, 100 epok kosinüs, patience 20, 80 epok tavanı, temiz evre 200 ve 30 epok) föyde yok; föyde yalnız temiz ve AT epokları, tohumlar, batch 64 ve 80 epok tavanı (M9.1, satır 1446-1489) ile hücre tanımları (satır 1443) var | B3 eğitim yapılandırmasının makine okunur kopyası (örneğin `results/q1/konsey_b3_tarif.json`, B3 eğitim betiğinin argümanlarından) ve föyde bunu anan bir satır |
| Y5 `fig:prereg_chain` | Dondurma anları ve blok koşu zamanları föyde yok; föyde yalnız ön kayıt gövdesinin ve dondurulmuş betiğin SHA-256'sı var (M9.8, satır 1680-1686) | `results/q1/konsey_zaman_cizelgesi.json` (kaynaklar: `ON_KAYIT_2026-10-29.md` ve `ON_KAYIT_EK_B8_B10_2026-10-30.md` dondurma ekleri, `results/q1/konsey_zincir_durum.tsv`, `results/q1/konsey_b3_defter.tsv`) ve föyde bir zaman çizelgesi bölümü |
| Y4 `fig:registry_map` | Öngörü ve çürütme eşiklerinin (0.75, 0.50, 0.30, -0.20, 0.10, 0.5, 10 puan, 0.50 ve 0.30 Mantel boyları) makine okunur kopyası yok; Tablo 3 bunları metin olarak taşır | `results/q1/konsey_kayit_kurallari.json` (kaynak: `experiments/q1_konsey_ayrisim.py` dondurulmuş sabitleri ve iki ön kayıt metninin tabloları); sonuç işareti çizilecekse föy M9.3 ve M10 satırları yeterlidir |
| Y2 (şekil 1 panel kabı) | Yok; üyelik `hucre_tablosu.json`, `_b9.json` ve `_b8.json`'daki `modeller.<m>.birincil_panel` ve `ikincil_panel` alanlarında var | Çizimden önce üç dosyadaki üye sayıları föydeki 7, 7 ve 6 ile karşılaştırılmalıdır |
| Y6, Y7, Y8 | Yok | Y6: föy M9.1 ve M9.2, `konsey_b6_maskeleme.json`; Y7: föy satır 151-201 ve `results/c1_transfer`, q1 ayar özetleri; Y8: föy satır 284-325 ve `results/c1_c4/pair*/c4_summary.json` |

Föy kuralı gereği bu yeni dosyaların değerleri önce `results/C1_REFERANS_FOYU.md`'ye girer; şekil betiği değeri föyle karşılaştırmadan yazmaz.

## 7. Panel adlandırma planı

### 7.1 Sayım

`panel_atif_sayaci.py` düz kopyalar üzerinde EN ve TR (`--dil tr`) için koşulmuştur; çıktılar `paper/figures/qc/panel_atiflari_en.md`, `.json`, `panel_atiflari_tr.md`, `.json`'dur, yapı dosyası `paper/figures/panel_yapisi.yaml`'dır. İki dilde de metinde tek bir panel atfı vardır: `Figure~\ref{fig:source_gap_split}a` (EN `04_experiments.tex` satır 141; TR `04_deneyler.tex` satır 141, `Şekil~\ref{fig:source_gap_split}a`). Yapı dosyası verilmeden koşulduğunda sayaç bugünkü yedi harfli şeklin hepsini harften çıkarır; adım 5'in testi (en az üç panelin ayrı anılması ya da en az dört atıf) hiçbir şekilde sağlanmaz. Bugün 7 şekil harflidir ve EN'de 15, TR'de 18 rozet vardır (sayacın altyazıdan okuduğu); plan bunları sıfıra indirir.

### 7.2 Şekil başına karar

| No | Etiket | Yapı | Adım | Ad türü | Bugün | Gerekçe |
| ---: | --- | --- | ---: | --- | --- | --- |
| 1 | fig:study_overview | karma | 7 | karma: harf ve akış | (a)-(d), altyazıda yok | Dört kap bantlar arası etiketli blok okla bağlanır; harf şartlıdır (aşağıda) |
| 2 | fig:decomposition_schematic | süreç zinciri | 2 | akış | (a)-(d), altyazıda yok | Her katın çıktısı sonrakinin girdisidir; harf yerine etiketli şevron |
| 3 | fig:source_gap_split | küçük katlar | 4 | şerit | (a)-(c) | Üç veri kümesi aynı ekseni paylaşır; başlık şeridi "CIFAR-10, CIFAR-100, ImageNetV2" |
| 4 | fig:similarity_matrix | küçük katlar | 4 | şerit | (a)-(c) | Aynı sıralama ve renk ölçeği |
| 5 | fig:cells_interaction | küçük katlar | 4 | renk | (a)-(c) | σ başlığı simetrik yeşil, ρ başlığı yönlü turuncu (şekil 2 ve 3 ile aynı bağ), ω nötr; ardışık üçüncü şeridi kırar |
| 6 | fig:attack_side | tek panel | 1 | yok | yok | |
| 7 | fig:gradient_alignment | küçük katlar | 4 | şerit | (a)-(f) | Satır şeridi ham ve artık, sütun şeridi veri kümesi |
| 8 | fig:estimates_forest | küçük katlar | 4 | renk | (a), (b) | Sol kart σ etkileri (yeşil), sağ kart ρ terimleri (turuncu) |
| 9 | fig:protocol_sets | numaralı düzey | 3 | rakam | (a), (b) ve kutularda A-D | Dört iç içe protokol 1-4 rakam halkası alır, iki panel harfsiz yan yana; A-D kutu harfleri panel harfiyle karışıyordu |
| 10 | fig:spread_clean_gap | küçük katlar | 4 | şerit | (a), (b) | Ortak x ekseni (temiz doğruluk farkı) |
| 11 | fig:epsilon_sweep | tek panel | 1 | yok | yok | |
| 12 | fig:feature_degradation | küçük katlar | 4 | şerit | (a), (b) | Ortak katman ekseni |

Mevcut 12 şeklin dizisi "karma akış şerit şerit renk yok şerit renk rakam şerit yok şerit"tir; en uzun aynı tür dizisi 2, harfli pay 0.00'dır (sınır 0.40; karma şekil harfli sayılmaz). Sayaç iki dilde de bu diziyi ve iki yan kuralın geçtiğini yazmıştır.

Karar: şekil 1'de harf şartlı olarak kalır, çünkü Y2 önerisi 3.6 "Reference Panels" ile 3.1-3.3 paragraflarını şekil 1'in panellerine atıfla kısaltmayı öngörür; yazım ajanı (a) modeller, (b) paneller, (c) ölçüm, (d) kayıt panellerinden en az üçünü metinde ayrı ayrı anarsa adım 5'in testi sağlanır. Anmazsa şekil 1 "akış ve şerit" karmasına iner ve dizi yine kurala uyar. Karar: hiçbir veri şekline harf verilmemiştir, çünkü metinde atıf yoktur ve kullanıcının "görsel sayısını artırıp içeriği azaltalım" isteği metne yeni panel atıfları yazmayı değil metni kısaltmayı ister; 8. ilkenin "kimisinde harfler kalır" seçeneği şekil 1'de karşılanır.

### 7.3 Yeni şekillerle önerilen tam dizi

Y1-Y7 metne metindeki yerlerine göre girerse sıra ve adlar şöyle olur: 1 karma (overview), Y1 şerit (2x2 ızgaranın satır ve sütun şeridi; 3B model blokları), 2 akış (ayrışım), Y4 şerit (kayıt haritası, aile satır şeritleri), Y5 akış (ön kayıt ve deney zinciri), 3 şerit, 4 şerit, 5 renk, 6 yok, 7 şerit, 8 renk, Y7 şerit (protokol ayarları), 9 rakam, 10 şerit, 11 yok, 12 şerit. Bu 16 şekillik dizide en uzun aynı tür dizisi 2'dir (3 ve 4), harfli pay en çok 1/16'dır. Yeni şekiller numaraları kaydırır: önerilen sırayla şekil 2 `fig:design_recipe`, şekil 3 `fig:decomposition_schematic` olur. Kurulum adları numara kesinleşince tek ad takımına iner (T28) ve eşleme dosyası elle yazılır.

### 7.4 Değişecek atıflar ve altyazılar

Metin bu fazda değiştirilmemiştir; aşağıdaki liste yazım ajanı içindir. Satır numaraları kaynak dosyalarındır (altyazı satırı etiket satırının bir üstüdür).

| Şekil | EN | TR | Değişiklik |
| --- | --- | --- | --- |
| 3 | `04_experiments.tex` 141 (atıf) | `04_deneyler.tex` 141 (atıf) | `\ref{fig:source_gap_split}a` yerine konumla atıf: "the CIFAR-10 panel of Figure 3" / "Şekil 3'ün CIFAR-10 paneli" |
| 1 | `03_methodology.tex` 37 | `03_yontem.tex` 29 | Altyazı panelleri anar: harf kalırsa (a)-(d) ve bantlar arası okların ne taşıdığı; kalmazsa bant adları |
| 2 | `03_methodology.tex` 162 | `03_yontem.tex` 154 | Harfler kalkar; altyazı "Top to bottom: ..." kalıbıyla aşamaları ve şevronların anlamını anar |
| 3 | `04_experiments.tex` 200 | `04_deneyler.tex` 201 | (a)-(c) yerine "left, middle, right" ya da veri kümesi adları |
| 4 | `04_experiments.tex` 209 | `04_deneyler.tex` 210 | Aynı biçimde veri kümesi adları |
| 5 | `04_experiments.tex` 322 | `04_deneyler.tex` 323 | (a)-(c) yerine başlık adları ve renk kodu: "green title, σ; orange title, ρ; grey, ω" |
| 7 | `04_experiments.tex` 492 | `04_deneyler.tex` 493 | "(a) to (c)" ve "(d) to (f)" yerine "top row, raw; bottom row, residual" |
| 8 | `04_experiments.tex` 518 | `04_deneyler.tex` 519 | (a), (b) yerine sol ve sağ kart, renk kodu |
| 9 | `04_experiments.tex` 579 | `04_deneyler.tex` 581 | "(a; schematic ...)" ve "(b; ...)" yerine "left, right"; 1-4 halkalarının protokol adları (raw, target-correct, both-correct, successful-source); Y3 kabul edilirse maske koşulları |
| 10 | `04_experiments.tex` 589 | `04_deneyler.tex` 592 | (a), (b) ve "the term that panel (a) leaves out" yerine konumla atıf |
| 12 | `07_appendix.tex` 119 | `07_ek.tex` 115 | (a), (b) yerine konumla atıf; Y8 kabul edilirse üçüncü kart |

Altyazılar IEEE Access'te 7 pt Formata ile basılır ve kalın bir girişle açılmalıdır (3-90 karakter; T24). Bugünkü altyazıların hiçbirinde kalın giriş yoktur; on iki altyazının hepsi bu yönden değişecektir. Altyazı sözcük sayıları 32-88 arasıdır.

## 8. Alınan kararlar

Karar: venue `ieee_access` adıyla önerilmiş, skill'e yazılmamıştır, çünkü skill değişikliği bu fazın yazma alanı dışındadır; kayıt yapılana kadar çizim betiği koşturulmamalıdır.

Karar: proje ayarı `paper/figures/visio_cizici.yaml`'dadır ve `VZ_PROJE_AYARI` ile okunur, çünkü görev bu yolu istemiştir ve depo kökünde `figures/` klasörü yoktur.

Karar: şekil 9 kart motorunda çizilir, iç içe kümeler 2B kalır, çünkü veri paneli aynı tuvaldedir ve Visio şemasına veri kartı gömme yolu bu fazda sınanmamıştır; 3B levha görünümü istenirse şekil iki parçaya bölünür (Visio şeması ve kart) ve adlandırma akış oku olur.

Karar: karalama kopyaları (probe için `\EOD`'lu `main.tex`, düzleştirme için mutlak yollu kaynak) makale klasörüne değil karalama klasörüne yazılmıştır; düz okuma kopyaları `paper/figures/qc/`'dedir ve gönderim paketine girmez.

## 9. Araç sınırları ve açık sorunlar

1. `vz_duzlestir.py` `\InputIfFileExists{x}{}{}`'i açmaz; ek ve hesaplama bölümü bu yüzden kaçar. Geçici çözüm bölüm 2'dedir.
2. `venue_probe.py --tex` sınıfın yanındaki yazı tipi dosyalarını kopyalamaz ve `\EOD` gibi belge sonu denetimi yapan sınıflarda 1 ile çıkar. Çözüm `--kopyala` ve karalama kopyasıdır; probe'a bir `--son-ek` seçeneği eklenmesi önerilir.
3. Windows Python'a ters bölülü UNC yolu Git Bash'ten verilince yol bozulur; `//wsl.localhost/...` ve `MSYS_NO_PATHCONV=1` kullanılır.
4. `included_figures.py` ve sayaç yalnız düz kopyada doğru sonuç verir; metin her değiştiğinde düz kopya yeniden üretilmelidir.
5. IEEE Access yazar kılavuzundaki en küçük punto ve ek dosya (Drawing drafts) kuralı bu oturumda okunmamıştır.
6. Kapak mektubu PDF'i ölçüm sırasında başka bir oturumca yeniden derlenmiştir; sayfa karşılaştırmasında bu hesaba katılmalıdır.

## 10. Düzeltme eki (31.10.2026 akşamı, Faz A doğrulaması sonrası)

Bu ek `03_faz_a_dogrulama.md`'deki bulguların bu raporu ilgilendirenlerini düzeltir; yukarıdaki metin tarihsel kayıt olarak değiştirilmemiştir ve çeliştiği yerde bu ek geçerlidir. Bağlayıcı plan `04_cizim_plani.md`'dir.

Bölüm 7.2'deki "harfli pay 0.00 (karma şekil harfli sayılmaz)" yanlıştır. Motorun ölçüsü (`motor/figspec/denge.py` `adlandirma_dizisi`, satır 692-709) harf içeren karma şekli harfli sayar; şekil 1 harfle kalırsa 12 şekilde pay 1/12 = 0.083 olur. Sınır 0.40'tır ve sağlanır. Sayacın Markdown çıktısındaki 0.00 sayacın kendi yöntemidir; kurulum sonrası bağlayıcı ölçü `zenginlik.py --makale`'dir. Bölüm 7.3'teki 16 şekillik dizi de geçersizdir; 17 şekillik yeni dizide pay 1/17 = 0.059'dur (`04_cizim_plani.md` bölüm 8) (E1, bulgu m1).

Şekil 1 dört değil beş panellidir: (a) Trained models, (b) Reference panels, (c) Matrices, (d) Registered before measurement, (e) Exact split and contrasts. Harfin kalma koşulu, bu beş panelden en az üçünün metinde ayrı ayrı anılmasıdır. Bölüm 7.2'deki gerekçe ve bölüm 7.4'teki altyazı satırı bu beş adla okunmalıdır; `panel_yapisi.yaml` buna göre yeniden yazılmıştır (E2, bulgu m2).

Bölüm 7.1'deki "bugün 7 şekil harflidir" cümlesi sayacın altyazı ayrıştırmasını anlatır. Doğrusu şudur: altyazıda harf anan 7 şekil vardır (3, 4, 5, 7, 8, 10, 12); görüntünün içinde harf taşıyan şekil ise 10'dur, çünkü şekil 1 ve 2 (a)-(d), şekil 9 (a)/(b) ve A-D harflerini görüntüde taşır ama altyazıda anmaz. EN'de 15, TR'de 18 rozet sayısı da sayacın altyazıdan okuduğu sayıdır; iki dil arasındaki fark sayaç sınırından gelir (EN'de şekil 4 için yalnız "b", şekil 7 için "acd"; TR'de "bc" ve "acdf") (E3, bulgu m3).

Bölüm 3'teki şekil 10 satırında "18 üst kaynağı" yerine 17 okunmalıdır; `paper/figures/final/fig_spread_clean_gap.kanit.json` `ust_kaynaklar_sha256` 17 girdi taşır (E4, bulgu m4).

Bölüm 6'daki Y1 satırının "gereken dosya" sütunu şöyle okunmalıdır: `results/q1/konsey_b3_tarif.json`, `scripts/konsey_b3_kuyruk.sh` (satır 11 ve 90-99: AdamW, ağırlık azaltma 0.05, öğrenme oranı, `-e 100`, `-b 64`, `--patience 20`, temiz evre 200 ve 30 epok) ve `src/training/trainer.py`'den üretilir; karantina kuralı gereği föyde bu tarifi anan bir satır (M13) şarttır ve şekil betiği değeri föyle karşılaştırmadan yazmaz (E5, bulgu m5).

Bölüm 5'teki "satır başına yaklaşık 11 sözcük (tahmin)" yerine ölçülmüş 9.8 sözcük kullanılmalıdır (EN main.pdf sayfa 3-12, 640 gövde satırı; ortalama 9.76, ortanca 10); metin kazancı bu yüzden yaklaşık yüzde 12 eksik hesaplanmıştı. Bölüm 5'teki Y1-Y7 toplamının (-90 satır, 0.80 sayfa) -25 satırı Y6'nın ana metinden eke taşımasıdır ve toplam sayfayı azaltmaz; Y6 dahil o planın toplam sayfa kazancı yaklaşık 0.5 sayfaya iner. Y2'nin "şekil 1'e yaklaşık 20 mm" maliyeti şekil 1'in eski 129 mm'si üzerine kuruluydu; Üslup 8 önizlemesi 161.9 mm olduğu için Y2 şekil 1'e sığmaz ve ayrı tek sütun şekil olur. Y5 için önerilen `sayim_akisi` Üslup 8'de uygulanmaz; Y5 `yontem_semasi` ile çizilir. Y6 eklenmez. Yeni bütçe `04_cizim_plani.md` bölüm 5 ve 7'dedir (E6, bulgu m10 ve M4).

Bölüm 2 tablosunda TR kaynak klasörü yalnız şekil 10 için yazılmıştır. Doğrusu şudur: TR aynası şekil 10, 11 ve 12'yi `paper/figures/final_tr/` altından alır (`fig_spread_clean_gap.pdf`, `fig2_epsilon_sweep.pdf`, `fig5b_attention_entropy.pdf`; `04_deneyler.tex` 591, `07_ek.tex` 28 ve 114) ve bu şekillerin TR kanıtları `paper/figures/final_tr/*.kanit.json`'dır. Şekil 1-9'u TR aynası da EN etiketli `konsey/` PDF'leriyle basar (E7, bulgu m11).

Bölüm 7.2'deki şekil 9 kararı geçersizdir. Rakam adımı (3) metinde numarayla anılan düzey ister; protokoller metinde ve Tablo 2'de adla anılır. Şekil 9 `farkli_analizler` yapısıyla ve başlık şeridiyle (adım 4, kural dalı 5) çizilir; A-D harfleri ve rakam halkası kalkar, kümelere protokol adları yazılır. Bölüm 3'teki "karma (şematik ve veri)" tanımı içerik tanımıdır, adlandırma türü değildir (E8, bulgu M3).

Bölüm 1 ve 8'deki "venue skill'e yazılmamıştır" durumu değişmiştir: `ieee_access` kaydı `motor/figspec/venues.py` satır 336-356'dadır, proje ayarında `venue: ieee_access` açıktır ve `tests/test_venues_kind.py` 31.10.2026 akşamı 11 geçen testle koşulmuştur (E9, bulgu M6).
