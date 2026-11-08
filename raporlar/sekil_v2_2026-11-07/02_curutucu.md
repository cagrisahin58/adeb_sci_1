# Kol C2, Faz 2 çürütücü raporu (08.11.2026, birinci tur)

Çelişik doğrulayıcı opus (salt okur) raporudur; yardımcı Fable tarafından olduğu gibi kaydedilmiştir. İkinci tur kapanışları `02_faz2_cizim.md` içinde "Çürütücü bulguları ve kapanışları" bölümündedir.

verdict: duzeltilmeli

Sayılar sağlam. Kanıt dosyalarındaki 1083 değerin 774'ü kaynak JSON anahtarına doğrudan oturuyor. Kalan 72 "uyuşmaz", fig17'de üç koşunun ortalamasıdır ve föy karşılaştırmasıyla tutuyor (169/169 TAMAM). 237 değer ise formül anahtarı taşıdığı için betikle açılamadı. Karantina kaynağından tek bir sayı yok. Asıl makale, asıl şekiller ve results/ değişmemiş; main_v2 tek kaynaktan derleniyor.

Verdict'i iki şey belirliyor. Birincisi, Şekil 11'de eksen sayıları yanlış basılmış; veri şeklinde düzeltilebilir bir doğruluk hatası bu. İkincisi, yürütücünün raporunda doğrulanmayan beyanlar var: "pakette yerel yol 0", "her şekilde iki çizgi kalınlığı basıldı", karantina beyanı. Bunlara Üslup Z'nin kendi "yapılmaz" listesinin dört şekilde çiğnenmesi ve K7 altyazı şartının altı şekilde eksik kalması ekleniyor.

## issues

1. **major**, fig11_gradient_alignment.png ve paper/figures_v2/z_gradient_alignment.py:75-88. Beklenen, eksen etiketinin işaret çizgisinin gerçek değerini basması. `nice()` adımı 2.5×10ⁿ seçebiliyor (0.25), etiket ise `Z.fmt(v, 1)` ile tek ondalığa yuvarlanıyor. Bu yüzden −0.75 "−0.8", −0.25 "−0.2", 0.25 "0.2", 0.75 "0.8" olarak basılmış. PNG'de işaret aralıkları eşit, etiket farkları eşit değil: ham CIFAR-10/100 x ekseninde "−1.0, −0.8, −0.5, −0.2"; artık CIFAR-10/100 x ekseninde "0.0, 0.2, 0.5, 0.8"; artık ImageNetV2'de "−0.2, 0.0, 0.2, 0.5". Altı kartın beşinde x ekseni yanlış okunuyor. QC, kontrolcü ve fig_mm_pdf bunu yakalamamış. Düzeltme için 2.5 adımı atılmalı ya da etiket iki ondalıkla basılmalı.

2. **orta**, paper/submission/Drawing_drafts_v2/evidence/fig1_study_overview.kanit.json, `goruntuler.cifar10.png` ve `goruntuler.cifar100.png` alanları. Rapor (02_faz2_cizim.md §5) "0 file(s) hold a local user path" diyor. Bu iki alanda `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\...` yolu duruyor. Tarayıcı ters bölülü UNC yolunu kaçırıyor. Çift kör pakette kullanıcı adı ve kurum ipucu sızıyor; .vsdx yazar alanındaki "ÇAĞRI ŞAHİN" sorunu da duruyor (zaten beyan edilmiş).

3. **orta**, Üslup Z kendi yasağını çiğniyor. uslup_Z.yaml:286 "Kutudan kutuya düz oklu akış, aynı boyda kart ızgarası" der, :217 bağlayıcının eğri olmasını ve zeminde ilerlemesini ister.
   - fig3: üç kutu, aralarında düz aşağı oklar. Klasik kutu-ok akışı; 3 mm geri çekilme gözle zor seçiliyor.
   - fig6: üç kart arasında iki düz ok.
   - fig11: 2×3 aynı boyda kart ızgarası.
   - fig17: üç aynı boyda kart yan yana.

   Faz 1 çürütücüsünün "kutu ve ok akışı kırılmamış" bulgusu fig3 ve fig6'da sürüyor.

4. **orta**, paper/manuscript_v2/altyazilar_v2.tex. K7 altyazının hangi kodlamanın değer taşıdığını söylemesini istiyor. Bu açıkça söylenen şekiller 7, 8, 9, 10 ve 16; 14 yalnız basamak uzaklıkları için söylüyor. fig11, fig12, fig13, fig15 ve fig17 altyazılarında böyle bir cümle yok (örneğin "values are positions on the flat card").

5. **orta**, 17 kanıt dosyasının hepsinde `karantina` alanı aynı kalıp metin: "okunan dosyalar yalniz su siniflardandir: results/q1/*, föy, hucre_tablosu*.json, src/models/*.py ...". Oysa okunan_dosyalar başka şeyler de içeriyor:
   - fig13, fig14: results/c1_transfer/...
   - fig16: results/c1_sweep/...
   - fig17: results/c1_c4/...
   - fig1: data/cifar-*/
   - fig6: raporlar/.../ON_KAYIT*.md ve results/q1_research/ONKAYIT_SAPMALAR.md
   - fig3: paper/figures/konsey/*.py
   - fig14: 03_methodology.tex

   İhlal yok: c1_* proje kuralında geçerli, wrn_eval de fig16'da `karantina_istisnasi` olarak föy satır 354'e bağlanmış. Ama beyan yanlış. Faz 1 bulgu 9'un aynısı; düzelmemiş, hatta "results/c1_*" sınıfı listeden düşmüş.

6. **orta**, 02_faz2_cizim.md §1. "hiyerarşi iki basamakta (0.75 ve 1.5) kuruldu ve her şekilde ikisi de basıldı" cümlesi doğru değil. qc/z_*/kapilar.json `K2_fig_mm_pdf.basili_cizgi_pt` alanı fig1, 2, 4, 5, 11, 12 ve 15'te yalnız [0.75] diyor. Bu yedi şekilde vurgu kalınlığı basılmamış; T4 ise 0. Sonuç bozulmuyor ama beyan dayanaksız.

7. **orta**, 02_faz2_cizim.md §3 ile qc/makale/report.md:9-23 arasında. Rapor "bloklayıcı yok" diyor ve 90 altında yalnız Şekil 1'i anıyor. QC raporunda katı karar beş şekilde BLOCK: 1 (87.0), 6, 8, 11 ve 15 (89.5). Sayılar raporun tablosunda doğru verilmiş, metin bunu söylemiyor.

8. **orta**, raporlar/sekil_v2_2026-11-07/02_ilerleme.tsv, qc_ayarli ve qc_kati sütunları. Beş satır son QC koşusuyla uyuşmuyor (TSV → report.md):

   | Şekil | TSV | report.md |
   | --- | --- | --- |
   | 16 | 94.6/91.1 | 97.6/93.5 |
   | 13 | 96.8/93.2 | 94.6/91.1 |
   | 8 | 94.6/91.1 | 93.6/89.5 |
   | 12 | 94.6/91.1 | 96.8/93.2 |
   | 17 | 94.6/91.1 | 100.0/95.9 |

   Yürütücü yalnız "not" sütununun eskidiğini yazmış. qc/z_*/kapilar.json içindeki K5 değerleri de eski koşudan kalma; fig1, 3, 5, 6 ve 17'de o koşunun consistency sonucu BLOCK.

9. **orta**, fig8_similarity_matrix.png. Faz 1 çürütücüsü "eğik düzleme yatırılmış ısı haritası" klişesini reddetmişti. v2'de üç matris yine dimetrik düzleme yatırılmış ısı haritası. Değer düz renkle okunuyor (K7 karşılanıyor), ama klişe kaldırılmamış, üçe çoğaltılmış.

10. **orta**, fig17_feature_degradation.png. 12 özdeş bloğun düşey yığını bir "katman dizisi" kalıbı; eğik yerine dik dizilmiş olması onu ortadan kaldırmıyor. 02_kompozisyon.md:75'teki "satırlar ince kılavuzlarla disklere bağlanır" iddiası PNG'de görünmüyor: kılavuz yok, yalnız hizalama var. Üstteki "per-block readouts" oku yalnız blok 12'nin tepesinden çıkıyor; her bloktan değil.

11. **orta**, gövde metniyle çelişki. "top card of Figure 14" (03_methodology.tex:215) ve "top card of Figure 17" (07_appendix.tex:84) v2'de karşılıksız; ikincisinde üstte kart yok. Yürütücü bunu beyan etmiş. main_v2.pdf'te okuru yanlış yere gönderiyor; gönderimden önce kapanmalı.

12. **küçük**, fig4: altyazı "books on two shelves", "front shelf / back shelf" diyor. PNG'de kitap yok, iki katalog kartı var; 02_kompozisyon.md:113 kitaptan vazgeçildiğini kendisi yazıyor. Altyazı şekille harfiyen eşleşmiyor.

13. **küçük**, fig2: altyazı ve kompozisyon "one index card per run" diyor. V-scr çekmecesinde 3 koşu için tek kart görünüyor (kartlar üst üste çakışmış); V-IN, R224-scr ve R224-IN'de 2, R32'de 3 kart görünüyor. Derinliğin taşıdığı söylenen bilgi V-scr'de kayboluyor.

14. **küçük**, fig1: "(b) Reference panels, sliced into (c) PGD-10 matrices" tek satırda birleşik. (c)'nin sahnede ayrı bir yeri ya da kılavuzu yok, (b) ile aynı nesneleri gösteriyor. Ayrıca uslup_Z.yaml:221 panel harfini kartın içinde sol altta ister; şekilde harfler kart dışında sol üstte.

15. **küçük**, fig5: 02_kompozisyon.md:117 ve manifestteki `sahne_kalibi: iki_kollu_merdiven` "sol kol ana kayıt, sağ kol ek kayıt" diyor. PNG tek kollu, yedi basamaklı bir merdiven.

16. **küçük**, fig16_epsilon_sweep.fig.json `sahne_kalibi: "teras"` alanı eskimiş; kompozisyon terastan kesik profile geçildiğini yazıyor. Kesik profilli levhalar da bilinen "3B şerit veya alan grafiği" kalıbına çok yakın. Değer tablodan okunduğu için K7 karşılanıyor. Arkadaki levhaların işaretleri x etiketlerinin sağına kaymış.

17. **küçük**, fig15: altyazı ve lejant arka kartta "open rings the identity prediction at p = 1" diyor. 600 dpi kırpmada bu halkalar seçilemiyor; işaretlerin altında kalmış.

18. **küçük**, fig7: ImageNetV2 çift 3 için föy:1932 D_k 0.0999, q 0.547 ("hesaplandi") veriyor. Şekil "G 0.100 q n/a" basıyor. Kural v1'den gelen `esik_G_imagenetv2`; ama 0.0999'u 0.100'e yuvarlayıp yanına "eşiğin altında" anlamında n/a koymak okurda çelişki doğuruyor. Üç ondalık ya da "<0.10" yazılmalı.

19. **küçük**, 02_faz2_cizim.md §1 "Muafiyet ... gerekçesi kanıt ile denge dosyalarındadır" diyor. fig7 ve fig16'da K7 gerekçesi fig.json'da (`ikiz_kodlama`) ve denge kapısında var; kanit.json'da yok. Görev "kanıt dosyasına yazılı olmalı" diyordu.

20. **küçük**, imza tekrarları: fig9 (iki direğe asılı üç kart) ile fig12 (raya asılı iki kart) aynı fikir; dikey yığılmış 2B grafik kartlarının yapısal askıyla bağlanması. fig11 ile fig15 de "arka kart yükseltide, ön kart zeminde" düzeninde. Aşağıdaki matrise bakınız.

21. **bilgi**, main_v2.log: 26 sayfa (PyMuPDF; asıl makale de 26). Tanımsız gönderme ve atıf 0 (tek "undefined" T1/pcr yazı tipi uyarısı). Taşma uyarısı 57: 53 adet 505 pt (sınıftan), 2 adet 9.27 pt ve 2 yeni adet 5.83 pt vbox; rapor doğru. derle_v2.sh bölümleri her derlemede kopyalıyor. main_v2.tex ile main.tex arasındaki fark tek bir yorum satırı; bölüm farkı yalnız şekil yolları ve 17 altyazı. Altyazıların hepsi kalın girişli ve ≤60 sözcük.

22. **bilgi**, Drawing_drafts_v2: 53 dosya (17 vsdx, 34 json, README, SHA256SUMS). `sha256sum -c` 51/51 OK. README İngilizce. 17 vsdx yapım klasöründekilerle bayt bayt aynı; yapım PDF'leri kurulu PDF'lerle bayt bayt aynı.

23. **bilgi**, git status: paper/manuscript altındaki 10 "M" yalnız dosya modu değişikliği (100755 → 100644, 0 satır) ve oturum başındaki görüntüde de vardı. paper/figures altındaki izlenmeyen dosyalar 31.10 tarihli. results altında yeni olan yalnız results/q1/curutme_2026-11-08 (başka süreç, yürütücü beyan etmiş). 08.11 16:30'dan sonra paper/figures, paper/manuscript ve results'ta başka dosya değişmemiş.

24. **bilgi**, oklch_olc.py --uslup Z yeniden koşuldu ("ihlaller: yok"). En büyük kroma 0.0857 (isi_5); L farkları vurgu 0.0843, ısı 0.0843, gövde 0.0844, zemin-ısı 0.0834, köşegen-ısı 0.130. uslup_Z.yaml sürüm 3'te çizgiler ince, normal ve eksen 0.2646 mm (0.75 pt), vurgu 0.5292 mm (1.5 pt); ok gövdesi, halka ve line.min_pt 0.75. _ISARET.json sürüm 14, 26/26 SHA tutuyor.

    Mavi payı kendim ölçtüm (HSV 180-270°, s>0.08 ve v>0.15; s>0.15 ile de):

    | Şekil | s>0.08 | s>0.15 |
    | --- | --- | --- |
    | fig1 | 0.017 | 0.023 |
    | fig7 | 0.067 | 0.056 |
    | fig12 | 0.049 | 0.126 |
    | fig9 | 0.009 | 0.012 |
    | fig17 | 0 | 0 |
    | fig16 | 0 | 0 |

    Mavi sayılan pikseller #9E94B2'den geliyor: OKLCH tonu 300°, kroma 0.045. Gerçek mavi yok; ölçüt farkı açıklaması doğru. fig12'de doymuş piksellerin %13'ü bu ton ama cırtlak değil.

25. **bilgi, DPI kararı**: 120 DPI'da çizim 96 kararıyla çelişiyor, ama bu yöntemsel bir sapma, kalite sorunu değil. fig_mm_pdf 17/17 PASS. En küçük basılı punto 8.4 (8.425), 8 pt tabanının üstünde. Basılı çizgiler 0.75 ve 1.5, T4 0. Merdiven 8.4/9.0/9.6, 96 DPI'da 8.25/9.0/9.75 basar ve tabanın üstünde kalır. Tek ızgara ve ekran ölçeğine dokunmama amacı korunmuş. Not düzeyinde kalır; verdict'e katkısı yok.

## 30 sayının kaynak denetimi

Kaynak dosya results/C1_REFERANS_FOYU.md (satır numarası verilenler) ve results/q1/konsey_zaman_cizelgesi.json.

| # | Şekil, kanıt alanı | Değer | Kaynak | Sonuç |
| --- | --- | --- | --- | --- |
| 1 | 14, Unconditioned ort±SD | 13.57±0.33 | föy:53 | tutuyor |
| 2 | 14, Target-correct | 4.36±0.44 | föy:54 | tutuyor |
| 3 | 14, Both-correct | 8.27±0.23 | föy:55 | tutuyor |
| 4 | 14, Successful-source | 19.37±1.27 | föy:56 | tutuyor |
| 5 | 14, N target-correct | 7,353 / 8,579 | föy:54 | tutuyor |
| 6 | 14, N both-correct | 7,061 | föy:55 | tutuyor |
| 7 | 14, N successful | 2,831 / 3,814 | föy:56 | tutuyor |
| 8 | 14, basamak raw−tc | 9.21 | föy:212 | tutuyor |
| 9 | 14, basamak bc−tc | 3.91 | föy:214 | tutuyor |
| 10 | 14, basamak ss−bc | 11.10 | föy:215 | tutuyor |
| 11 | 13, spread C10 L∞ | 15.01 | föy:162 | tutuyor |
| 12 | 13, spread C100 L∞ | 13.83 | föy:162 | tutuyor |
| 13 | 13, spread SVHN | 4.14/3.26 | föy:162 | tutuyor |
| 14 | 13, spread C10 L2 | 10.92 | föy:162 | tutuyor |
| 15 | 16, WRN temiz | 89.5 | föy:360 (89.48) | tutuyor |
| 16 | 16, WRN 8/255 | 66.9 | föy:363 (66.92) | tutuyor |
| 17 | 16, WRN 16/255 | 47.4 | föy:364 (47.36) | tutuyor |
| 18 | 16, ResNet-18 AT temiz | 85.8 | föy:360 (85.78) | tutuyor |
| 19 | 16, ResNet-18 AT 8/255 | 44.2 | föy:363 (44.19) | tutuyor |
| 20 | 16, ViT-Tiny AT 2/255 | 64.1 | föy:361 (64.10) | tutuyor |
| 21 | 16, ViT-Tiny AT 16/255 | 12.2 | föy:364 (12.16) | tutuyor |
| 22 | 16, en büyük SD | 0.59 | föy:363 | tutuyor |
| 23 | 9, A(σ, scr) | −0.364 | föy:1526 | tutuyor |
| 24 | 9, I(σ) | +0.260 | föy:1527 | tutuyor |
| 25 | 11, r CIFAR-10 ham / artık | 0.94 / 0.94 | föy:1970-1971 (0.943/0.944) | tutuyor |
| 26 | 11, r CIFAR-100 ham / artık | 0.98 / 0.91 | föy:1972-1973 | tutuyor |
| 27 | 11, r ImageNetV2 ham / artık | 0.69 / 0.89 | föy:1974-1975 | tutuyor |
| 28 | 7, CIFAR-10 G ve q (3 çift) | 0.391/0.387/0.390; 0.94/0.93/0.94 | föy:1587, 1593 | tutuyor |
| 29 | 7, CIFAR-100 G ve q (3 çift) | 0.388/0.459/0.448; 0.85/0.86/0.81 | föy:1838, 1848 | tutuyor |
| 30 | 7, ImageNetV2 çift 1, 2 | G 0.122 q 1.36; G 0.173 q 0.68 | föy:1930-1931 | tutuyor |
| 31 | 7, ImageNetV2 çift 3 | G 0.100, q n/a | föy:1932 (0.0999, q 0.547) | yuvarlama ve kural çelişkisi (bulgu 18) |
| 32 | 5, K-a ve K-c öngörü | ≥0.75, ≥0.3 | föy:1587, 1589 | tutuyor |
| 33 | 6, B5 MI/TGR hücre, model | 228 / 95, 19 | zaman_cizelgesi.json matrisler.B5-* | tutuyor |
| 34 | 6, B3 süre ve kayıt commit'i | 17.8 h, e32f2ce | egitim_suresi.defter_toplam_sure_sa = 17.79; dondurma.on_kayit.commit | tutuyor |

Otomatik açılan 774 değer de kendi JSON anahtarıyla tutuyor. Karantina yollarına (run1, run2, run3, attention_analysis_run3, stat_addendum, rev2_blockA) dokunan dosya 0.

## Tekrar ve klişe matrisi

| Şekil | Kompozisyon fikri | PNG'de görünen | Derinlik anlamı | Tekrar veya klişe |
| --- | --- | --- | --- | --- |
| 1 | maket masası (pv_a) | plaka üstünde yığınlar ve desteler | hat sırası, zayıf okunuyor | (b)(c) birleşik |
| 2 | kartotek dolabı | metin dolu çekmece kutuları | koşu kartları (V-scr'de görünmüyor) | metin kutusu |
| 3 | üç katlı buzlu kesit | üç kutu, düz oklar | 3 mm, zor seçiliyor | kutu-ok akışı (yasak) |
| 4 | kitaplık, sonra katalog kartı | iki rafta iki tablo kartı | kayıt düzeyi | tablo |
| 5 | iki kollu merdiven | tek kollu basamaklı tablo | kayıt sırası | yok |
| 6 | zaman rafı | üç kart, düz oklar | zaman, görünüyor | kutu-ok akışı (yasak) |
| 7 | zemin levhaları | eğik levhalarda çubuklar | veri kümesi sırası | özgün |
| 8 | üç kaide | üç eğik ısı haritası | kayıt sırası | eğik ısı haritası klişesi |
| 9 | kule | direklere asılı üç grafik kartı | yok | 12 ile aynı fikir |
| 10 | abaküs | çerçeve içinde nokta grafiği | yok | özgün, boncuklar telde değil |
| 11 | iki basamaklı tribün | 2×3 aynı boy kart ızgarası | işlem adımı | ızgara (yasak), 15 ile benzer |
| 12 | asılı etiketler | rayda iki orman kartı | yok | 9 ile aynı fikir |
| 13 | patlatılmış levhalar | dört kayık kart ve sırt | protokol katmanı | 9 ve 12'ye yakın |
| 14 | teraslı havuz | basamaklı piramit ve kart | iç içelik | özgün |
| 15 | derin sahne | arka ve ön iki saçılım kartı | okuma sırası | 11 ile benzer |
| 16 | kesik profil | 3B şerit veya alan grafiği | sağlamlık sırası | 3B alan grafiği klişesine yakın |
| 17 | omurga | 12 blok yığın ve üç kart | yok | katman dizisi ve aynı boy kart |

Sahne plakası sekiz şekilde (1, 5, 6, 7, 8, 11, 14, 15); sınır tam dolu. Harfli şekil payı 1/17. Adlandırma dizisinde aynı tür en çok iki kez ardışık; tutuyor.

## Özgünlük yargısı

Paletin kumu, tek ışık yönü ve zanaat tutarlı; cırtlak renk ve mavi-turuncu zıtlığı gerçekten kalkmış. Ama şekillerin çoğunun 3B dili, düz bir 2B grafiğin kenarına kalınlık ve gölge eklenmesinden ibaret. On iki şekilde değer düz kart yüzünde, derinlik ise kart kalınlığı ya da sıra kaydırması. Gerçekten yeni okunan fikirler fig7 (eğik levhada ikiz kodlamalı şeritler), fig14 (iç içe teraslar), fig10 (abaküs) ve kısmen fig6 (derinliği zaman olan raf). fig8 ve fig17, Faz 1'de reddedilen eğik ısı haritası ve katman dizisi kalıplarının biraz değiştirilmiş hâli. fig16 bilinen 3B alan grafiğine çok yakın. fig3 ve fig6 kutu-ok akışını üslubun kendi yasağına rağmen sürdürüyor. "Komple özgün ve 3 boyutlu" ölçütü yaklaşık altı şekilde karşılanıyor, kalanı "kartlaştırılmış v1" düzeyinde. Bu öznel bir yargıdır ve verdict'i tek başına belirlemiyor; verdict 1-8 numaralı somut bulgulara dayanıyor.

Çürütücünün bakış kopyaları ve betikleri proje dışında: C:/Users/cagri/AppData/Local/Temp/claude/e2c0fa868388f4cf/0d0fab82-c6b8-472d-a420-d8ffb5857ab2/scratchpad/curut2/ (kapi.py, kapi2.py, kanit.py, mavi.py ve üç kırpma PNG'si). Proje altında hiçbir dosya değiştirilmedi.
