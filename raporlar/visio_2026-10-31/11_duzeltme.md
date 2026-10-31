# Düzeltme turu raporu (visio-cizici adım 9-12 sonrası, tek tur)

Tarih 31.10.2026, 23:05-23:35 (+03:00). Yazan düzeltme ajanıdır (makale-yazari ve gorsel-uretici rolü). Girdi, Faz C sonrasında çelişik doğrulayıcının verdiği on bulgudur. Her bulgunun kanıtı yeniden denetlenmiş, haklı bulunanlar EN ve TR metinde düzeltilmiş, haksız ya da gereksiz bulunanlar aşağıda gerekçesiyle reddedilmiştir. Hiçbir şekil yeniden çizilmemiş, kurulu şekillere, orijinal şekil klasörlerine (`figures/final`, `final_tr`, `konsey`, `overview`) ve veri dosyalarına dokunulmamış, git işlemi yapılmamıştır. Komut günlüğü `paper/figures/visio_loglari/duzeltme11_komutlar.log`, durum dosyası `paper/figures/visio_loglari/duzeltme11_durum.json`'dur.

En önemli üç sonuç şunlardır. Birincisi, on bulgunun altısı metinde düzeltilmiş (2, 3, 4, 5, 6, 7), biri reddedilmiş (1, ImageNet ağırlık kimlikleri 3.2'de zaten basılıdır), biri ertelenmiş (8, sayfa 5'teki boşluk), ikisi devir notu maddesi olarak kaydedilmiştir (9 ve 10). İkincisi, iki dil sıfırdan derlenmiş ve kapı zinciri WSL'den "OZ-SINAMA VE DOKUZ KAPI GECTI" vermiştir; on yedi şeklin QC puanları önceki turla aynıdır ve Drawing drafts paketi değişmeden `--yollari-tara` 0 vermektedir. Üçüncüsü, EN el yazması 25 sayfadan 26 sayfaya çıkmıştır. Son sayfada yalnız ikinci yazarın üç satırlık biyografisi vardır; bu sayı plandaki üst sınırın (26) içindedir ve kontrol listesine işlenmiştir (bölüm 2).

## 1. Bulgular ve kararlar

| No | Bulgu | Karar | Yapılan iş ve gerekçe |
| --- | --- | --- | --- |
| 1 | Tablo 1 kalkınca ImageNet ağırlık kimlikleri düştü | Reddedildi | Kimlikler 3.2'de timm adlarıyla ve atıflarıyla basılıdır: EN `03_methodology.tex` satır 56 "ImageNet weights come from `deit\_tiny\_patch16\_224.fb\_in1k` [touvron2021training] and `resnet18.a1\_in1k` [wightman2021resnet]", TR `03_yontem.tex` satır 51 aynı cümle. Bulgudaki arama LaTeX kaçışlı alt çizgiyi (`deit\_tiny`) ve büyük-küçük harf farkını kaçırmıştır; `grep -i deit` iki dosyada da bu satırı bulur. timm adı "DeiT-Ti" ve "RSB A1" adlarından daha kesin bir kimliktir. Metin ve Şekil 2 değiştirilmedi. |
| 2 | Tablo 3'ün kayıtlı karar kurallarının bir kısmı Yöntem'de yok | Düzeltildi | Kanıt doğru: HEAD tab:registry K-a payda kuralını, saldırı tarafı kurallarını ve H2'nin logit koşulunu taşıyordu, bugünkü 3.9'da "undecided" ve "logit estimate" geçmiyordu. Kurallar `results/q1/konsey_kayit_kurallari.json` ve föy M13 satır 2528 (K-a: `D_s <= DELTA` ise kararsız), 2535 (H2: Holm sonrası p, kestirim > 0 ve logit kestirim > 0) ve 2547 (B5: `G_PGD <= DELTA` kararsız, %90 alt sınır >= 0.5 destek, üst sınır < 0.5 çürütme) ile karşılaştırıldı. 3.9'un karar okuma paragrafına tek cümle eklendi; eşik sayısal olarak değil $\delta$ ile yazıldı, 0.5 eşiği `% FOY:M13:2528,2535,2547` yorumuna bağlandı. TR'de aynı paragrafa üç cümle eklendi, paragraf sayısı değişmedi. Şekil 5 yeniden çizilmedi. |
| 3 | Ek A'da ResNet blok kosinüslerinin yedisi kayboldu | Düzeltildi | Kanıt doğru: föy satır 316-323'teki ResNet-18 katman kosinüsleri şekilde ve kanıt dosyasında yok, metinde yalnız 0.8777 vardı. Cümleye komşu iki blok eklendi (EN "with a cosine of 0.8777 against 0.9607 one block earlier and 0.9108 one block later"); değerler föy satır 321 ve 323'tedir ve mevcut `FOY:... Tablo 10:288-323` atfının içindedir. TR'de uzun cümle ikiye bölünerek aynı karşılaştırma yazıldı. |
| 4 | Şekil 14 ilk kez 3.7'de anılıyor, 12 sayfa sonra basılıyor | Kısmen düzeltildi | İlk anılış sırası doğrulandı (3.7 satır 215'te Şekil 14, ardından Şekil 5-13). Önerilen en ucuz çözüm uygulandı: atıf açık ileri gönderme oldu ("with masks drawn there in the top card of Figure 14", TR "bunların maskeleri o bölümdeki Şekil 14 üst kartında"). Numaralandırma değiştirilmedi, çünkü 17 kurulum adını ve `ESLEME.md`'yi bozar. Sıra sorunu tümüyle kapanmadı (bölüm 6). |
| 5 | Şekil 17 altyazısı marjı "dashed" diyor, şekilde gölgeli bant | Düzeltildi | `fig_feature_degradation.py` satır 129 marjı `axhspan` dolgulu bant olarak, satır 130 sıfır çizgisini kesikli çizgi olarak çizer; lejant dolgulu kare gösterir. EN "dashed" yerine "shaded", TR "kesikli" yerine "gölgeli" yazıldı. |
| 6 | CIFAR-100 yayılım SD'si (1.30) basılı değil | Düzeltildi | Föy satır 163'te "13.83$\pm$1.30" bulunur ve IV-I paragrafının `FOY:TabloIII:159-163` grubu içindedir. EN cümlesine "(CIFAR-100: $13.83\pm1.30$ points)", TR'ye "(CIFAR-100'de $13{,}83\pm1{,}30$ puan)" eklendi. Sayfa denemesinde bu ekleme kaldırıldığında da EN 26 sayfa kaldığı için ekleme tutuldu. |
| 7 | Kontrol listesi TR aynasının yeni şekil setine geçmediğini söylüyor | Düzeltildi | TR 17 şekli aynı `../figures/figN_*.pdf` yollarıyla taşır. `pre_submission_checklist.md` satır 72 "uses the same 17 figure files with English labels and Turkish captions; Turkish-labelled figures follow in the second round (plan 12.6)" oldu. Aynı dosyada satır 40'taki sayfa sayısı da 26'ya güncellendi (bölüm 2). |
| 8 | Sayfa 5 sol sütunda yaklaşık üç satırlık boşluk | Ertelendi | Boşluk 60 dpi görüntüde doğrulandı. Şekil 2'nin `figure` ortamı 3.4'ün başına taşınarak denendi; boşluk ve sayfa sayısı değişmedi, değişiklik geri alındı. Boşluk IEEEtran'ın `\flushbottom` germesinden gelir, gövdede taşma yoktur ve IEEE dizgisi sayfayı yeniden kuracaktır; gönderim için zorunlu değildir. |
| 9 | `00_once_sha.txt` föy satırında FAILED veriyor | Kabul, devir notu | `sha256sum -c` 21 OK ve föy için FAILED verdi; `git diff --numstat 302d56c HEAD` föyde 288 eklenen, 0 silinen satır, tek parça `@@ -2376,0 +2377,288 @@`; çalışma kopyası HEAD ile aynıdır. Ekleme satır 2377'den başlar (bulgu "2374 sonrası" diyordu). Başlangıç kaydı olduğu için dosya güncellenmedi. Devir notuna yazılacak cümle bölüm 7'dedir. |
| 10 | TR altyazılar İngilizce panel adları taşıyor ve kalın girişle açılıyor | Kabul, devir notu | Bu turun "TR aynası İngilizce etiketli PDF'leri kullanır" kararının doğal sonucudur. Plan 12.6'daki Türkçe etiketli şekil turunda altyazılardaki İngilizce adlar Türkçe panel adlarıyla değiştirilecek, teze aktarımda kalın girişler tez şablonunun altyazı biçimine çevrilecektir. Devir maddesi bölüm 7'dedir. |

Eklenen EN cümleleri şunlardır. 3.9: "K-a is undecided if any seed pair has $G_s \leq \delta$; the retained fraction is undecided if $\Gk{PGD} \leq \delta$, supported if its 90\% lower bound reaches $0.5$ and refuted if its upper bound falls below it; H2 support also needs a positive logit estimate." İlk taslak daha uzundu ve sayfa denemesi için kısaltıldı, anlamı değişmedi.

## 2. Sayfa sayısı

İlk derlemede EN el yazması 26 sayfa verdi; son sayfada yalnız ikinci yazarın biyografisi (üç satır) vardır. Bu pay `08_metin_en.md` satır 65'te de kayıtlıdır (yaklaşık beş satırlık bir ekleme el yazmasını 26 sayfaya çıkarabilir). İki deneme yapıldı: bulgu 6'nın eklemesi geri alındığında ve Şekil 2 bölüm başına taşındığında sonuç yine 26 sayfa oldu. Sayfayı geri kazanmanın yolu, bu turun kapsamı dışındaki metni kısaltmaktır. Karar: 26 sayfa kabul edildi, çünkü plandaki sınır en çok 26 sayfadır, bulgu 2'nin önerisi bu artışı öngörmüştür ve IEEE dizgisi son sayfayı yeniden kuracaktır. Kontrol listesinin satır 40'ı "26 pages ... the last page carries only the second author biography" olarak güncellendi. TR aynası 27 sayfadır ve değişmemiştir.

| Belge | Bu turdan önce | Sonra | Hata | Tanımsız atıf / gönderme | Overfull hbox |
| --- | ---: | ---: | ---: | --- | ---: |
| EN `paper/manuscript/main.pdf` | 25 | 26 | 0 | 0 / 0 | 55 (53'ü sayfa başlığı ve altlığı, 2'si `\maketitle`) |
| TR `paper/manuscript_tr/main.pdf` | 27 | 27 | 0 | 0 / 0 | 0 |

İki belge de `.aux`, `.bbl`, `.blg`, `.fls`, `.fdb_latexmk`, `.out` ve `.log` silinerek sıfırdan derlendi (EN `scripts/derle_en.sh`, TR `paper/manuscript_tr` içinde `latexmk -pdf main.tex`). EN günlüğündeki tek "undefined" satırı sınıfın bilinen `T1/pcr/n/n` yazı tipi uyarısıdır. Overfull sayısındaki 53'ten 55'e artış yeni sayfanın başlık ve altlık kutularından gelir; gövdede taşma yoktur.

## 3. Kapı zinciri

Komut `wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && bash scripts/kapilar.sh"`, son satır "OZ-SINAMA VE DOKUZ KAPI GECTI".

| Kapı | Sonuç | Sonuç satırı (kısaltılmış) |
| --- | --- | --- |
| öz-sınama | GECTI | kapı 19 sınamanın 80 bozmasının hepsini yakaladı |
| sayılar | GECTI | FOY atıfları bloklarında, bloklardaki sayılar işaretle |
| iddialar | GECTI | (boş sonuç satırı) |
| özet | GECTI | özdeki her sayının gövdede karşılığı var |
| TR ondalık | GECTI | matematik kipinde çıplak ondalık virgül yok |
| bildiri | GECTI | bildirinin taşıyıcı sayıları artefaktlarla tutuyor |
| EN/TR ayna | GECTI | bölüm ağacı, kayan nesneler, denklemler tutuyor |
| gönderim | GECTI | gönderim malzemeleri makaleyle ve artefaktlarla tutuyor |
| PDF render | GECTI | PDF (26 sayfa) özet, anahtar kelime, başlık, yazar bandı |
| PDF dizgi | GECTI | kalın/italik Times gömülü, sütun taşması yok |

TR metinde `tara.py --tur makale --bolum oto` `03_yontem.tex`, `04_deneyler.tex` ve `07_ek.tex` için kesin ihlal vermedi; norm sapmaları dosya düzeyindedir ve bu turdan önce de vardı.

## 4. Şekil QC

Hiçbir şekil yeniden üretilmedi. Altyazı (Şekil 17) ve şekil atıflarının çevresindeki metin (Şekil 5, 14) değiştiği için düz okuma kopyaları (`paper/figures/qc/main_{en,tr}_duz.tex`) yeni metinden yeniden üretildi ve `fig_qc.py` on yedi şeklin hepsinde, önceki turun ayar kopyalarıyla (`qc_ayari_visio.yaml`, `qc_ayari_kart.yaml`) yeniden koşuldu. `included_figures.py` iki dilde 17 şekil okudu. Puanlar önceki turla aynıdır; Şekil 17'nin D3 kaybı (altyazı "90% intervals" ve "mean±SD" yazar, D3'ün sözcük listesi bunları tanımaz) `10_derleme_qc_paket.md` bölüm 3'te açıklanmıştır. Toplu sonuç `paper/figures/qc/qc_ozet_duzeltme11.json`'dadır.

| Şekil | Motor | Ayarlı puan | Karar |
| --- | --- | ---: | --- |
| fig1_study_overview | Visio | 97.4 | PASS |
| fig2_design_recipe | Visio | 97.4 | PASS |
| fig3_decomposition_schematic | Visio | 97.4 | PASS |
| fig4_panel_members | Visio | 97.4 | PASS |
| fig5_registry_map | Visio | 97.4 | PASS |
| fig6_prereg_chain | Visio | 97.4 | PASS |
| fig7_source_gap_split | kart | 100.0 | PASS |
| fig8_similarity_matrix | kart | 100.0 | PASS |
| fig9_cells_interaction | kart | 100.0 | PASS |
| fig10_attack_side | kart | 97.6 | PASS |
| fig11_gradient_alignment | kart | 95.3 | PASS |
| fig12_estimates_forest | kart | 97.6 | PASS |
| fig13_protocol_settings | kart | 94.1 | PASS |
| fig14_protocol_sets | kart | 94.1 | PASS |
| fig15_spread_clean_gap | kart | 97.6 | PASS |
| fig16_epsilon_sweep | kart | 97.6 | PASS |
| fig17_feature_degradation | kart | 96.5 | PASS |

Şekiller arası tutarlılık (`fig_qc.py --consistency`, `VZ_USLUP=8`) PASS verdi: 17 şekil tek tasarım sistemini paylaşır, 22 varlık adının hiçbiri iki renge bağlanmamıştır (`paper/figures/qc/tutarlilik_duzeltme11.txt`). İlk deneme `VZ_USLUP` verilmeden koşulmuş ve `UslupError` ile durmuştu; günlükte kayıtlıdır.

## 5. Drawing drafts

Şekil değişmediği için `paper/submission/Drawing_drafts/` yeniden kurulmadı. `install.py --yollari-tara paper/submission/Drawing_drafts` "0 file(s) hold a local user path" ve çıkış 0 verdi; `sha256sum -c SHA256SUMS.txt` 29 dosyanın hepsinde OK verdi. Altı `.vsdx` taslağının yazar adı ("ÇAĞRI ŞAHİN") önceki turdaki gibi değiştirilmeden bırakıldı.

## 6. Kalan sorunlar

Şekil numaralarının ilk anılış sırası tümüyle düzelmedi. 3.7'deki atıf artık açık bir ileri göndermedir, ancak Şekil 14 Yöntem'de Şekil 5-13'ten önce anılmaya devam eder. Ayrıca `04_experiments.tex` satır 82'deki Tablo 2 altyazısı ve satır 529'daki "every protocol of Figure 14" ifadesi de Şekil 14'ü Şekil 13'ten önce anar. Karar: numaralandırma değiştirilmedi, çünkü 17 kurulum adını, `ESLEME.md`'yi ve Drawing drafts paketini bozar; dizgici sorarsa sıra o aşamada düzeltilir.

EN el yazması 26 sayfadır ve son sayfada yalnız ikinci yazarın biyografisi vardır. 25 sayfaya dönmek için bu turun kapsamı dışındaki metinde yaklaşık beş satırlık kısaltma gerekir. Sayfa 5 sol sütundaki boşluk da sürmektedir (bulgu 8).

3.9'daki "equivalence support for K-b and H3 from Holm-adjusted TOST $p$, with refutation checked first" ifadesi, betikteki K-b ve H3 sırasıyla (destek > çürütme > kararsız, föy satır 2529 ve 2536) harfiyen örtüşmez. Uygulamada sonuç değişmez, çünkü TOST desteği aralığın $\pm\delta$ içinde kalmasını, çürütme ise kestirimin $|\cdot| > \delta$ olmasını ister ve ikisi aynı anda sağlanamaz. Bulgu listesinde olmadığı için metne dokunulmadı; ana oturumun bilgisine sunulur.

## 7. Devir notuna yazılacak maddeler

Föy, c315e09'da yalnız eklemeyle (M13, satır 2377'den itibaren 288 satır) değişmiştir; `raporlar/visio_2026-10-31/00_once_sha.txt` Faz A başlangıcını gösterir ve bu yüzden föy satırında FAILED verir. Eski satırlar ve metindeki FOY atıfları geçerlidir.

Plan 12.6'daki Türkçe etiketli şekil turu açıldığında TR altyazılardaki İngilizce panel adları ("Family sütunu", "Seen beforehand şeridi", "Block-output cosine başlıklı alt kart" gibi) Türkçe panel adlarıyla değiştirilmeli, teze aktarımda ise kalın altyazı girişleri tez şablonunun altyazı biçimine çevrilmelidir. TR aynası 27 sayfadır; plandaki sayfa bütçesi yalnız EN'e bağlıdır.

## 8. Değişen dosyalar

`paper/manuscript/sections/03_methodology.tex` (3.7 ileri gönderme; 3.9 karar kuralları cümlesi ve KAYNAK/FOY yorumu), `paper/manuscript/sections/04_experiments.tex` (IV-I, CIFAR-100 SD), `paper/manuscript/sections/07_appendix.tex` (Ek A komşu bloklar; Şekil 17 altyazısında "shaded"), `paper/manuscript_tr/sections/03_yontem.tex`, `04_deneyler.tex`, `07_ek.tex` (aynı düzeltmelerin Türkçe karşılıkları), `paper/submission/pre_submission_checklist.md` (satır 40 sayfa sayısı, satır 72 TR aynası), derlenmiş `main.pdf` dosyaları, `paper/figures/qc/main_{en,tr}_duz.tex` ve haritaları, `paper/figures/qc/<şekil>/qc/report.{json,md}`, `paper/figures/qc/qc_ozet_duzeltme11.json`, `paper/figures/qc/tutarlilik_duzeltme11.txt`, `paper/figures/visio_loglari/duzeltme11_*`.
