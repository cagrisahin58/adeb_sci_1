# Faz C: Türkçe ayna (makale yazarı)

31.10.2026 gecesi yazılan bu belge, İngilizce el yazmasında yapılan şekil kurulumunun ve metin kısaltmalarının Türkçe aynaya (`paper/manuscript_tr`) işlenmesini kaydeder. Çalışma listesi olarak `08_metin_en.md` kullanılmış, İngilizce dosyalara, `main.tex` dosyalarına ve özgün şekil klasörlerine dokunulmamış, git kullanılmamıştır.

En önemli üç sonuç şunlardır. Birincisi, Türkçe ayna İngilizce sürümle aynı on yedi şekli aynı yerlerde, aynı etiketlerle ve aynı kurulu PDF'lerle (`../figures/figN_<kök>.pdf`) taşımaktadır; beş tablo kaldırılmış, bütün göndermeler şekle çevrilmiştir. İkincisi, `kapilar.sh` WSL'den koşulmuş ve öz-sınamayla birlikte dokuz kapının dokuzu da geçmiştir; EN/TR ayna kapısı artık bütün bölüm çiftlerinde eşittir ve iddia kapısı 45/45'tir. Üçüncüsü, Türkçe el yazması 0 hata, 0 tanımsız gönderme ve 0 overfull hbox ile 27 sayfa derlenmektedir; yorum dışı sözcük sayısı 17445'ten 16824'e inmiştir (621 sözcük).

## 1. Kaldırılan tablolar

İngilizce sürümde kalkan beş tablo Türkçede de aynı etiketlerle kaldırılmıştır. `03_yontem.tex` içinde `tab:design` yerine `fig:design_recipe` (Şekil 2, 3.4'te tablonun yerinde), `tab:protocol_masks` yerine metindeki iki cümle ve `fig:protocol_sets` üst kartı, `tab:registry` yerine `fig:registry_map` (Şekil 5, 3.9'da tablonun yerinde) gelmiştir. `04_deneyler.tex` içinde `tab:protocol_settings` yerine `fig:protocol_settings` (Şekil 13, IV-I'da tablonun yerinde), `07_ek.tex` içinde `tab:feature_degradation` yerine `fig:feature_degradation` alt kartı ve metne eklenen ResNet-18 en düşük kosinüsü ($0{,}8777$, föy Tablo 10 satır 323, paragrafın üstündeki `% FOY:... Tablo 10:288-323` yorumu kapsamında) gelmiştir.

Göndermeler İngilizcedeki karşılıklarıyla değiştirilmiştir: 3.4 açılışı ve IV-D açılışı (`tab:design` → `fig:design_recipe`), 3.7 (`tab:protocol_masks` → "Şekil~\ref{fig:protocol_sets} üst kartı"), 3.9 ve IV açılışı ile `tab:mantel` altyazısı (`tab:registry` → `fig:registry_map`), `tab:pair_decomposition` altyazısındaki $+4{,}36$ göndermesi (`tab:protocol_settings` → `fig:protocol_sets`, değer Şekil 14'te basılı olduğu için), IV-I'nın üç göndermesi ve Ek A. Türkçe metinde bu beş etikete giden gönderme kalmamıştır.

## 2. Şekiller ve yollar

`main.aux` numaraları İngilizceyle birebir aynıdır: study_overview 1, design_recipe 2, decomposition_schematic 3, panel_members 4, registry_map 5, prereg_chain 6, source_gap_split 7, similarity_matrix 8, cells_interaction 9, attack_side 10, gradient_alignment 11, estimates_forest 12, protocol_settings 13, protocol_sets 14, spread_clean_gap 15, epsilon_sweep 16, feature_degradation 17. Ortamlar da aynıdır (1, 5, 6, 7, 8, 11 `figure*`, ötekiler `figure`). Türkçe metinde `figures/konsey` ve `figures/final_tr` klasörlerine artık gönderme yoktur; bu klasörlerdeki dosyalar değiştirilmemiştir. Plan 12.6 gereği bu turda Türkçe ayna İngilizce etiketli PDF'leri kullanmaktadır; Türkçe etiketli şekiller ikinci turdadır ve devir notuna yazılmalıdır. Bu nedenle eski Türkçe `final_tr` sürümlerinin (epsilon taraması, dikkat entropisi, yayılım) yerini de İngilizce etiketli kurulu PDF'ler almıştır.

## 3. Altyazılar

On yedi altyazının hepsi `\textbf{...}` kalın girişle açılmaktadır. Şekildeki panel, şerit, sütun ve kart adları `08_metin_en.md` bölüm 3'teki karara uygun olarak İngilizce ve tırnaksız bırakılmış, açıklamaları Türkçe yazılmıştır (örneğin "(a) Trained models, (b) Reference panels ve (c) Matrices panellerinde", "Family sütununa göre", "Seen beforehand şeridi", "Conditioning sets kartı", "Block-output cosine başlıklı alt kart"). Harfli tek şekil Şekil 1'dir; (a)-(e) harfleri metinde İngilizcedeki dört yerde anılmaktadır (3.1'de (a), 3.5'te (e), 3.6'da (b) ve (c), 3.9'da (d)). Altyazılardaki sayılar ($0{,}10$, $\pm0{,}10$, $\pm0{,}05$, $60$, $p = 1$, $0{,}08$, $8/255$, \%90, \%95) İngilizcedeki FOY yorumlarının altında, virgüllü yazılmıştır. Yeni beş şeklin altyazısında yalnız Şekil 6'daki "Ekim 2026" takvim ifadesi vardır.

| Etiket | Kurulu dosya | TR kalın giriş |
| --- | --- | --- |
| fig:study_overview | fig1_study_overview.pdf | Çalışmanın genel görünümü. |
| fig:design_recipe | fig2_design_recipe.pdf | Mimari $\times$ başlatma tasarımı. |
| fig:decomposition_schematic | fig3_decomposition_schematic.pdf | Çalışma boyunca kullanılan ayrışım. |
| fig:panel_members | fig4_panel_members.pdf | Referans paneli üyeleri. |
| fig:registry_map | fig5_registry_map.pdf | Kayıtlı testler ve karar kuralları. |
| fig:prereg_chain | fig6_prereg_chain.pdf | Ön kayıt zinciri. |
| fig:source_gap_split | fig7_source_gap_split.pdf | Kaynak açığının simetrik ve yönlü parçalara bölünmesi. |
| fig:similarity_matrix | fig8_similarity_matrix.pdf | İkili simetrik benzerlik. |
| fig:cells_interaction | fig9_cells_interaction.pdf | CIFAR-10'da $2\times2$ tasarımın hücreleri. |
| fig:attack_side | fig10_attack_side.pdf | Kaynak başına saldırıya göre transfer. |
| fig:gradient_alignment | fig11_gradient_alignment.pdf | Benzerliğe karşı girdi gradyanı hizalanması. |
| fig:estimates_forest | fig12_estimates_forest.pdf | İki ölçekte kayıtlı kestirimler. |
| fig:protocol_settings | fig13_protocol_settings.pdf | Ayara göre protokol. |
| fig:protocol_sets | fig14_protocol_sets.pdf | Koşullama kümeleri ve ölçülen asimetri. |
| fig:spread_clean_gap | fig15_spread_clean_gap.pdf | Temiz doğruluk farkına göre protokol yayılımı. |
| fig:epsilon_sweep | fig16_epsilon_sweep.pdf | PGD-10 altında gürbüz doğruluk. |
| fig:feature_degradation | fig17_feature_degradation.pdf | Saldırı altında ViT-Tiny'nin öznitelik bozunması. |

Altyazıların tam metni ilgili `.tex` dosyalarındadır. Terimler `TERMINOLOJI.md` ile uyumludur (kaynak açığı, simetrik pay, bölünmüş yarı, mimari $\times$ başlatma, ön kayıt eki, eşi olmayan, ResNet-18 türevi, bağlayıcı yerine "adımlar", koşullama protokolü). Karar: Şekil 2 altyazısında "crosses" karşılığı "kesişmektedir" yazıldı, çünkü sözlük mimari $\times$ başlatma için "çaprazlayan" sözcüğünü yasaklamaktadır. Karar: Şekil 6'daki "commits" karşılığı "sürüm kayıtlarını (commit)" yazıldı, çünkü Türkçe akademik metinde terim ilk geçişte açıklanmalıdır.

## 4. Metin değişiklikleri

Değişiklikler İngilizcedeki paragraflarla aynı paragraflarda yapılmış, hiçbir paragraf bölünmemiş ya da birleştirilmemiştir. 3.1'in model paragrafı "Eğitilen modellerin tasarımdaki yeri Şekil~\ref{fig:study_overview}(a) içinde gösterilmiştir." cümlesiyle açılmakta, ViT-Tiny ve R224 cümleleri teke inmiş, `vit_tiny_patch16_224` adı metinden çıkmıştır. 3.3'te epok, öğrenme oranı, parti ve tohum sayıları Şekil 2'ye bırakılmış, ağırlık sönümü, kırpma, gradyan kırpma, doğrulama bölmesi, tohum 777, sabır ve eşik metinde kalmıştır. 3.4'te "daha kısa bir AdamW temiz aşamasını" yazılmıştır. 3.6'da RobustBench tanımlayıcıları metinden çıkmış, CIFAR atıfları tek `\cite` listesinde, ImageNet panelinin altı CNN'i tek `\cite` ile anılmış, `sloppypar` ortamı kalkmış ve bölümün sonuna Şekil 4 eklenmiştir; ortak hat kuralları, gösterim, Liu ve Mo'nun rolü metinde kalmıştır. 3.7'ye gevşek okumanın yalnız duyarlılık analizi olduğunu ve hangi maskelerin iki yönde aynı örnekleri kullandığını söyleyen iki cümle eklenmiştir. 3.9'da test aileleri Şekil 1(d)'ye ve Şekil 5'e bağlanmış, karar okuma paragrafı İngilizcedeki gibi kısaltılmamıştır. 3.10'da ilk paragrafa Şekil 6 göndermesi eklenmiş, ikinci paragrafın açılışı önceden görülen matrisleri şekle bırakacak biçimde kısalmış, bölümün sonuna Şekil 6 konmuştur.

Deneyler bölümünde K-a cümlesindeki "Şekil~\ref{fig:source_gap_split}a" göndermesi "Şekil~\ref{fig:source_gap_split}, CIFAR-10 paneli" olmuş, IV-I'da "Şekil~\ref{fig:protocol_settings} ve~\ref{fig:protocol_sets}" ile "Şekil~\ref{fig:protocol_settings} içindeki CIFAR-100 ve $L_2$ satırları" yazılmıştır. Hesaplama ayrıntılarında pilot projeksiyonu (20,47 saat) ve epok başına süre oranı (1,05-2,19) cümleleri çıkmış, paylaşılan GPU bilgisi ve B3 bloğu Şekil 6 göndermesiyle tek cümlede kalmıştır; çıkan sayıların föyde M9.1'de durduğu yorum satırına yazılmıştır. Ek A'da tablo göndermesi kalkmış, CNN cümlesine "$0{,}8777$ kosinüs" eklenmiş, entropi eşdeğerliği "Şekil~\ref{fig:feature_degradation} üst kartı" ile gösterilmiştir. Türkçe ek eki sorununu önlemek için şekil göndermelerinde ek alan biçimler ("Şekil 2'de") yerine "içinde" ve ayraç kullanılmıştır.

## 5. Derleme, kapılar ve üslup

Derleme `paper/manuscript_tr` içinde `/home/firat/.local/bin/latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` ile yapılmıştır: çıkış 0, `!` hatası 0, tanımsız gönderme ya da atıf 0, overfull hbox 0, 27 sayfa (1.228.822 bayt). `scripts/kapilar.sh` WSL'den koşulmuş ve "OZ-SINAMA VE DOKUZ KAPI GECTI" vermiştir; EN/TR ayna kapısı bütün bölüm çiftlerinde alt bölüm, tablo, şekil, denklem ve paragraf sayılarını eşit bulmuş, iddia kapısı TOPLAM=45, KALAN=0 vermiş, TR ondalık, özet, bildiri, gönderim, PDF render (EN, 25 sayfa) ve PDF dizgi kapıları da geçmiştir. Sayı kapısının yalnız bilgi amaçlı Türkçe satırı 33 eksikten 26 eksiğe inmiştir; kalkan Türkçe kayıt tablosunun KAYNAK eksikleri bu düşüşün çoğunu oluşturmaktadır.

Türkçe sayı denetiminde bir yeni bilgi kalemi vardır: Şekil 6 altyazısındaki "Ekim 2026" ifadesinin yılı GRUPSUZ sayılmaktadır. Bunun nedeni `verify_manuscript_numbers.py` içindeki `_YIL_ONCE` deseninin yalnız İngilizce ay adlarını tanımasıdır; aynı betiğin gün-ay-yıl deseni Türkçe ay adlarını zaten içermektedir. Karar: altyazı İngilizceyle aynı içerikte bırakıldı ve kapı betiğine dokunulmadı, çünkü Türkçe satır kapı dışıdır ve kapı betiklerinin değişikliği öz-sınama turunu gerektirir. Önerilen düzeltme, `_YIL_ONCE` desenine `Ocak|Şubat|...|Ekim|Kasım|Aralık` seçeneklerinin eklenmesidir; Türkçe denetim `--tr-zorunlu` ile kapıya katılmadan önce yapılmalıdır. Türkçe altyazılarda "\%90" ve "\%95" yazımının ATIF EKSIK sayılması önceden de vardı (eski Şekil 17 altyazısında \%95, yenisinde \%90).

`tara.py` (`--tur makale --bolum oto`) dört dosyada da kesin ihlal bulmamıştır. 03'te iki norm sapması (ad cümlesi ve kısa cümle payı) ile önceden var olan 95 sözcüklük Önerme cümlesi bilgi olarak raporlanmıştır. 04'teki üç sapma ve 07'deki dört sapma dosyaların bütününden gelmektedir. 04z, üç paragraflık küçük bir dosya olduğundan bant dışı birçok ölçüt göstermektedir; son paragrafın tamamen "-mıştır" ile bitmesi yapılmış işin raporlanmasından gelmektedir ve olağandır.

## 6. Sözcük sayısı

`arsiv/b2_yardimci/_mk_y1_kelime_say.py` ile, yorum satırları hariç: toplam 17445'ten 16824'e (621 sözcük); yöntem 3946'dan 3541'e, deneyler 7081'den 7008'e, hesaplama 217'den 190'a, ek 1744'ten 1628'e. Özet 242 sözcükte kalmıştır.

## 7. Açık kalanlar

Türkçe etiketli şekiller ikinci turdadır (plan 12.6) ve devir notuna yazılmalıdır; bu tur Türkçe PDF'te İngilizce etiketli şekiller basılmaktadır. `_YIL_ONCE` desenine Türkçe ay adlarının eklenmesi (bölüm 5) kapı sahibinin işidir. `08_metin_en.md` bölüm 8'deki açık işler (düz kopyanın yeniden üretilip fig_qc K4 ile M-K1, M-K2, M-K4 kapılarının koşulması, `panel_yapisi.yaml` M-K3, Drawing drafts paketi) bu ajanın kapsamı dışındadır ve açık kalmaktadır.

## 8. Dosyalar

Değişen dosyalar `paper/manuscript_tr/sections/03_yontem.tex`, `04_deneyler.tex`, `04z_hesaplama.tex`, `07_ek.tex` ve derleme çıktısı `paper/manuscript_tr/main.pdf` (ile `main.aux`, `main.log` gibi yan dosyalar) dosyalarıdır. Değişiklik öncesi Türkçe bölümler git HEAD'dedir; aynı kopyalar karalama klasöründe `tr/tr_once/` altında da durmaktadır. Durum dosyası `paper/figures/visio_loglari/makale_yazari_tr_durum.json`, komut günlüğü `paper/figures/visio_loglari/makale_yazari_tr_komutlar.log`.
