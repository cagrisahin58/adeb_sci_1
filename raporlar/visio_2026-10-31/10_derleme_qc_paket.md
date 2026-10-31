# Derleme, QC ve Drawing drafts raporu (visio-cizici adım 7, 9, 11 ve 12)

Tarih 31.10.2026, 22:47-23:02 (+03:00). Yazan derleme, QC ve paket ajanıdır (gorsel-uretici rolü). Bu adımda makale metnine, orijinal şekillere (`figures/final`, `final_tr`, `konsey`, `overview`), kurulu şekillere ve veri dosyalarına dokunulmamış, git işlemi yapılmamıştır. Komut günlüğü `paper/figures/visio_loglari/derleme_qc_paket_komutlar.log`, durum dosyası `paper/figures/visio_loglari/derleme_qc_paket_durum.json`'dur.

En önemli üç sonuç şunlardır. Birincisi, EN, TR ve kapak mektubu ara dosyaları silinerek sıfırdan derlenmiş, üçünde de hata, tanımsız atıf ve tanımsız gönderme sıfır çıkmıştır; EN 25 sayfadır ve hedef sayfa bütçesinin (25, en çok 26) içindedir, kapı zinciri WSL'den "OZ-SINAMA VE DOKUZ KAPI GECTI" vermiştir. İkincisi, on yedi kurulu şeklin on yedisi `fig_qc.py`'nin ayarlı kipinde en az 94.1 puanla ve bloklayıcısız geçmiş, katı kipte de hiçbiri BLOCK almamıştır (en düşük 94.4); ancak bu sonuç, proje paletinin ve kurulum adlarının ad şemasının QC'ye bir ayar kopyasıyla verilmesine dayanır (bölüm 3). Üçüncüsü, `paper/submission/Drawing_drafts/` 30 dosyayla kurulmuş, `install.py --yollari-tara` 0 ile çıkmıştır; altı `.vsdx` taslağının belge özellikleri yazar adını ("ÇAĞRI ŞAHİN") taşımaktadır ve paketin bu hâliyle yüklenmesi yazarın kararına bırakılmıştır.

## 1. Sıfırdan derleme

Derleme `scripts/derle_en.sh` (EN), `paper/manuscript_tr` içinde `latexmk -pdf main.tex` (TR) ve `paper/submission` içinde `latexmk -pdf cover_letter.tex` (kapak mektubu) ile WSL'de yapılmıştır. Her belgede önce `.aux`, `.bbl`, `.blg`, `.fls`, `.fdb_latexmk`, `.out` ve `.log` silinmiştir. Çıktının tamamı `paper/figures/visio_loglari/derleme_qc_paket_derleme.log` dosyasındadır.

| Belge | Önce (`00_once.md`) | Bu adımın başında | Sonra | Hata | Tanımsız atıf / gönderme | Overfull hbox | Underfull hbox |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| EN `paper/manuscript/main.pdf` | 25 | 25 | 25 | 0 | 0 / 0 | 53 | 39 |
| TR `paper/manuscript_tr/main.pdf` | 26 | 27 | 27 | 0 | 0 / 0 | 0 | 13 |
| `paper/submission/cover_letter.pdf` | 3 | 2 | 2 | 0 | 0 / 0 | 0 | 0 |

EN günlüğündeki tek "undefined" satırı ``Font shape `T1/pcr/n/n' undefined`` uyarısıdır; önceki derlemelerde de vardır ve bir atıf ya da gönderme değildir. EN'deki 53 overfull kutunun 51'i "has occurred while \output is active" türündedir ve tam olarak `\textwidth` (505.12 pt) genişliğindedir, yani ieeeaccess.cls'in sayfa başlığı ve altlığı kutusudur; kalan ikisi `main.tex` satır 142'deki `\maketitle` bloğunda 9.27 pt'lik kutulardır. Gövde metninde ve şekil ya da tablo ortamlarında overfull kutu yoktur; PDF dizgi kapısı da sütun taşması bulmamıştır. Önceki raporda bu sayı 54'tü.

TR aynası `00_once.md`'deki 26 sayfadan 27 sayfaya çıkmıştır. Artış bu adımda değil, TR yazım ajanının metin ve şekil düzenlemesinde oluşmuştur (`09_metin_tr.md` aynı sayfa sayısını yazar). Plandaki 26 sayfalık sınır gönderilecek EN el yazması içindir; TR aynası IEEEtran taslağıyla derlenen bir tez kopyasıdır ve bu sınıra bağlı değildir. Kapak mektubu, işin başında kaydedilen 3 sayfadan bu adımdan önce başka bir oturumun 19:45 derlemesiyle 2 sayfaya inmişti; yeniden derleme de 2 sayfa vermiştir. Derleme sonucunda izlenen üç PDF (`paper/manuscript/main.pdf`, `paper/manuscript_tr/main.pdf`, `paper/submission/cover_letter.pdf`) değişmiş görünür.

## 2. Kapı zinciri

Komut `wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && bash scripts/kapilar.sh"` olarak oturum açma kabuğuyla koşulmuştur (22:48:59-22:49:48). Beklenen on denetimin onu GECTI satırı vermiş, son satır "OZ-SINAMA VE DOKUZ KAPI GECTI", çıkış 0'dır.

| Kapı | Sonuç | İlk sonuç satırı (kısaltılmış) |
| --- | --- | --- |
| öz-sınama | GECTI | kapı 19 sınamanın 80 bozmasının hepsini yakaladı |
| sayılar | GECTI | FÖY atıfları bloklarında, bloklardaki sayılar işaretle |
| iddialar | GECTI | (boş sonuç satırı) |
| özet | GECTI | özdeki her sayının gövdede karşılığı var |
| TR ondalık | GECTI | matematik kipinde çıplak ondalık virgül yok |
| bildiri | GECTI | bildirinin taşıyıcı sayıları artefaktlarla sayısal olarak tutuyor |
| EN/TR ayna | GECTI | iki sürümün bölüm ağacı, kayan nesneleri, denklemleri tutuyor |
| gönderim | GECTI | gönderim malzemeleri makaleyle ve artefaktlarla tutuyor |
| PDF render | GECTI | PDF (25 sayfa) özet, anahtar kelime, başlık, yazar bandı |
| PDF dizgi | GECTI | kalın/italik Times gömülü, sütun taşması yok |

Öz-sınamanın bozma sayısı `00_once.md`'deki 84'ten 80'e inmiştir; sayı kapısı ve öz-sınaması bu adımda değiştirilmemiştir, fark sınamanın metindeki adaylardan türettiği bozmaların sayısındandır.

## 3. Şekil başına QC (`fig_qc.py`)

`fig_qc.py` ve `zenginlik.py` `\input` ağacını izlemez. Görevdeki `--tex paper/manuscript/main.tex` ile yapılan deneme koşusunda `zenginlik.py` "no figure PDF" vermiş, `fig_qc.py` de altyazı bulamamıştır. Karar: QC, makale düzeyi zenginlik ve numara denetimi `paper/figures/qc/main_en_duz.tex` düz okuma kopyası üzerinde koşulmuştur, çünkü skill `\input`'lu el yazması için bu kopyayı ister (SKILL.md, proje ayarı paragrafı) ve plan bölüm 11 de M-K1'i bu kopyayla tanımlar. Düz kopyalar (EN ve TR) yeni metinden yeniden üretilmiştir. `vz_duzlestir.py` `\InputIfFileExists`'i açmadığı için, `01_envanter.md` bölüm 2'deki yolla karalama klasöründe her `\input` ve `\InputIfFileExists` satırı mutlak yollu `\input`'a çevrilmiş ve düzleştirme bu kopya üzerinde koşulmuştur; iki dilde 17 şekil okunmuştur.

Seçili üslubun paletiyle yapılan deneme koşusunda `fig1_study_overview` ayarlı kipte 87.2 puanla BLOCK almıştır: B1 `#D55E00` (ViT rengi) için "off-palette" ve C4 0/3. Nedeni şudur: proje ayarında `palette:` satırı kapalıdır, `fig_qc` bu yüzden Üslup 8'in türetilmiş paletine düşer, oysa şekiller proje paletinin üslup tonlu kopyalarıyla (`adeb_konsey_uslup_8`, kartlarda `adeb_konsey_uslup_7`) çizilmiştir; C4'ün varsayılan ad şeması da ana metin adında `_visio` ya da `_chart` soneki ister, kurulum adları ise `ESLEME.md` gereği soneksizdir. Karar: `--palette` verilmemiş, bunun yerine `qc_kos.py` proje ayarından motor başına iki QC kopyası üretmiştir (`paper/figures/qc/qc_ayari_visio.yaml`, `qc_ayari_kart.yaml`); kopyalar proje ayarının aynısıdır ve yalnız iki satır ekler: şeklin manifestindeki `palette_path`'e eşit `palette:` ve `qc.c4.name_scheme: ^fig(?P<s>S?)(?P<n>\d+)_(?P<name>[a-z0-9_]+)$`. Bu seçim yapılmıştır, çünkü skill paletin önce proje ayarından okunmasını öngörür (`fig_qc.py` `default_palette`) ve başka bir paletle puanlanan şeklin B1'de haksız kayıp aldığını yazar; ad şeması da proje ayarıyla değiştirilebilen bir anahtardır. Betik her koşudan önce manifestin `palette_path`'inin beklenen dosya olduğunu denetler. Varsayılan ad şemasıyla her şekil C4'ten 3 puan daha kaybeder ve bu adımın hiçbir PASS kararını değiştirmez (en düşük ayarlı puan 94.1, kart şekillerinde C4 kaybıyla yaklaşık 90.6 olur; Visio şekillerinde 93.6'ya iner). Bu son iki sayı ölçülmemiş, tavandan hesaplanmıştır.

Komut, her kurulum adı için `python "$V/motor/host/fig_qc.py" --assets paper/figures --tex paper/figures/qc/main_en_duz.tex --venue ieee_access --figure <ad> --out paper/figures/qc/<ad>/qc` biçimindedir (Visio şekillerinde `VZ_USLUP=8`, kartlarda `VZ_USLUP=7`). Raporlar `paper/figures/qc/<ad>/qc/report.md` ve `report.json`'da, toplu sonuç `paper/figures/qc/qc_ozet_derleme.json`'dadır.

| Şekil | Motor | Ayarlı | Karar | Katı | Katı karar | Katı tavan (90 sınırı) | Ayarlı kayıp | Katı kayıp |
| --- | --- | ---: | --- | ---: | --- | --- | --- | --- |
| fig1_study_overview | Visio | 97.4 | PASS | 95.7 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 2/4, D2 1.5/3 |
| fig2_design_recipe | Visio | 97.4 | PASS | 94.4 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 1/4, D2 1.5/3 |
| fig3_decomposition_schematic | Visio | 97.4 | PASS | 95.7 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 2/4, D2 1.5/3 |
| fig4_panel_members | Visio | 97.4 | PASS | 95.7 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 2/4, D2 1.5/3 |
| fig5_registry_map | Visio | 97.4 | PASS | 95.7 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 2/4, D2 1.5/3 |
| fig6_prereg_chain | Visio | 97.4 | PASS | 94.4 | PASS | 79.5/81 = 98.1 (72.9) | A3 2/4 | A3 1/4, D2 1.5/3 |
| fig7_source_gap_split | kart | 100.0 | PASS | 100.0 | PASS | 85/85 = 100 (76.5) | yok | yok |
| fig8_similarity_matrix | kart | 100.0 | PASS | 100.0 | PASS | 85/85 = 100 (76.5) | yok | yok |
| fig9_cells_interaction | kart | 100.0 | PASS | 100.0 | PASS | 85/85 = 100 (76.5) | yok | yok |
| fig10_attack_side | kart | 97.6 | PASS | 97.6 | PASS | 85/85 = 100 (76.5) | A6 2/4 | A6 2/4 |
| fig11_gradient_alignment | kart | 95.3 | PASS | 95.3 | PASS | 85/85 = 100 (76.5) | A6 2/4, D6 0/2 | A6 2/4, D6 0/2 |
| fig12_estimates_forest | kart | 97.6 | PASS | 97.6 | PASS | 85/85 = 100 (76.5) | A6 2/4 | A6 2/4 |
| fig13_protocol_settings | kart | 94.1 | PASS | 94.1 | PASS | 85/85 = 100 (76.5) | A6 2/4, D3 0/3 | A6 2/4, D3 0/3 |
| fig14_protocol_sets | kart | 94.1 | PASS | 94.1 | PASS | 85/85 = 100 (76.5) | A6 2/4, D3 0/3 | A6 2/4, D3 0/3 |
| fig15_spread_clean_gap | kart | 97.6 | PASS | 97.6 | PASS | 85/85 = 100 (76.5) | A6 2/4 | A6 2/4 |
| fig16_epsilon_sweep | kart | 97.6 | PASS | 97.6 | PASS | 85/85 = 100 (76.5) | A6 2/4 | A6 2/4 |
| fig17_feature_degradation | kart | 96.5 | PASS | 96.5 | PASS | 85/85 = 100 (76.5) | D3 0/3 | D3 0/3 |

Hiçbir şekilde bloklayıcı yoktur; katı kipte de BLOCK alan şekil olmadığı için yazılacak bir BLOCK nedeni yoktur. Kayıplar her şekil türünde ayrı bir nedenden doğmaktadır. Altı Visio şeklinde A3, gövde yazısının 8.40-8.45 pt basılmasından gelir; bu boy, 8.0 pt tabanın altına düşecek 8.0 pt tasarımın 120 DPI ızgarasında tabanın üstündeki ilk noktaya (14 x 0.6 = 8.4 pt) yazılmasıdır (tuzak tablosu bölüm 1 madde 1) ve ayarlı kip bunu ne venue basamaklarına (8, 9, 10) ne de Üslup 8 puntolarına (8.0, 9.0, 10.9) eşleyebilmektedir. Katı kipteki D2 kaybı Visio şematiğine her zaman düşen 1.5 puandır. Kart şekillerindeki A6, panel çerçevelerinin sol ya da alt kenarlarının hizalı olmamasıdır ve kart düzenindeki farklı genişlikli panellerden gelir. `fig11_gradient_alignment`'ta D6, sekiz panelin yedisinde altı `n = ...` notu bulunduğunu, lejant panelinin muafiyet gerekçesinin ("a key to the marks") yazıldığını ama puanın verilmediğini söyler. `fig13`, `fig14` ve `fig17`'deki D3 kaybı bir altyazı eksiği değildir: altyazılar "mean$\pm$SD" ve "90\% intervals" yazar, D3'ün sözcük listesi ise yalnız "95%", "confidence interval", " ci", "wilson", "standard deviation" ve "interquartile" arar (`fig_qc.py` satır 1036-1040). Bu sınır `06_kart_cizim.md` madde 9'da skill'e önerilmiştir.

Şekiller arası tutarlılık (`fig_qc.py --consistency`, M-K2) PASS'tır; 17 şekil tek tasarım sistemini paylaşmakta, iki palet 22 ortak varlık adında aynı renk bağlarını taşır. 3B nesne taşıyan üç şeklin (1, 2, 3) manifestinde görünüm tektir (eğik, 25 derece). Çıktı `paper/figures/qc/tutarlilik_derleme.txt`'dedir.

## 4. Makale düzeyi zenginlik (`zenginlik.py --makale`, M-K1)

| Ölçüt | Değer | Eşik | Sonuç |
| --- | ---: | --- | --- |
| Çok panelli pay | 0.8235 | en az 0.75 | PASS |
| Veri şekillerinde derinlik 3 payı | 0.1667 (1/6) | en az 0.25 | UYARI |
| Görüntü payı | 0.0588 (1/17) | 0.10-0.25 | FAIL; yazılı gerekçeyle uygulanmaz |
| Bir hex bir aile | 0 | en çok 1 | PASS |
| Harfli şekil payı | 0.0588 | en çok 0.40 | PASS |
| Ardışık aynı adlandırma | 2 | en çok 2 | PASS |

Görüntü payı blok şiddetindedir ve yalnız yazılı gerekçeyle "uygulanmaz" sayılır (`references/denge.md`). Karar: gerekçe `--goruntu-gerekce` ile verilmiş ve ikinci bir koşu yapılmıştır, çünkü makalenin örnek ya da çekişmeli görüntü gösteren bir şekli yoktur ve bu kararın yazılı gerekçesi Faz A envanterindedir (`01_envanter.md` bölüm 3, satır 83: görüntü paneli kapsayıcı ve GPU ister, önerilmez). Gerekçesiz sonuç `paper/figures/qc/zenginlik_makale.{txt,json}`'da, gerekçeli sonuç `zenginlik_makale_gerekceli.{txt,json}`'da saklanmıştır. Tek görüntülü şekil Şekil 1'dir (CIFAR-10 ve CIFAR-100 destelerinin ön kartlarındaki ilk dört test görüntüsü). "Bir hex bir aile" maddesinin geçişi boş bir geçiştir: manifestler varlık hex'i taşımadığı için madde hiç hex okumamıştır (HP'deki durumun aynısı; `references/denge.md` bölüm 6). Derinlik 3 payında `zenginlik.py` kart şekillerinin beşini (9, 12, 14, 15, 17) ölçümle "şematik" sınıfına koymuş, payı altı veri şekli üzerinden hesaplamıştır. Şekil başına 17 satırın 17'si "kurulabilir"dir. `zenginlik.py` blok şiddetindeki FAIL'e rağmen 0 ile çıkmıştır; çıkış kodu bu yüzden karar için okunmamış, karar satırlardan verilmiştir.

## 5. Basılı numaralar ve tek ad takımı (M-K4, T28)

`included_figures.py --tablo` düz kopyalarda EN ve TR için 17 şekil vermiştir ve her satır "ok"dur (`paper/figures/visio_loglari/derleme_qc_paket_included_{en,tr}.txt`). Numaralar `ESLEME.md`'nin hedef sırasıyla ve derlenmiş `main.aux` dosyalarındaki `fig:` etiketleriyle (EN ve TR) 17/17 tutar. `ad_takimi.py` denetimi (`paper/figures/visio_loglari/derleme_qc_paket_ad_takimi.md`) her şekil için kurulum adının manifest `stem`'i, kanıt dosyası `stem`'i, Visio denetçi raporu `stem`'i, manifestin `formats` adları ve QC klasörü (`paper/figures/qc/<ad>/qc`) ile aynı olduğunu göstermiş, sorun 0 bulmuştur. Kart denetçi raporlarında (`.mm.json`) `stem` alanı yoktur; bu motorun biçimidir (`07_kurulum.md` bölüm 2).

Karar: kurulumdan önceki kapı çıktıları (`paper/figures/qc/<yapım kökü>/fig_mm_pdf.json` ve `denge.json`) yapım kökü adlı klasörlerde bırakılmıştır, çünkü `install.py` K-c ve K-d kapılarını bu yoldan okur ve klasörü taşımak bir yeniden kurulumu kırar. Yayına giden ad takımı (kurulu dosyalar, manifest, kanıt, denetçi raporu, QC raporu, Drawing drafts) tek ve numaralıdır; yapım kökü adlı klasörler çalışma izidir.

## 6. Drawing drafts paketi

Sıra skill adım 11'deki gibidir. `install.py --yollari-temizle` 17 kurulum adıyla önce `--dene` ile, sonra gerçek olarak koşulmuş, 51 JSON dosyasında 0 alan bulmuştur; kurulu JSON'ların SHA-256'ları koşudan önce ve sonra aynıdır. Paket `paketle.py` ile kurulmuştur. Her Visio şeklinde yapım klasöründeki PDF'in SHA-256'sı kurulu PDF'inkiyle karşılaştırılmış (6/6 eşit; ilk 16 hane 950f2e2d4e427fc7, 405f72d9274ef805, b434d6de3cc1548a, b3eaf0edd435bf3f, b4abce0ab38c5ba2, d5f159b26d8abbea), ardından `.vsdx` kurulum adıyla bayt bayt kopyalanmıştır. Kart şekillerinde de yapım PDF'i kurulu PDF'e eşittir (11/11) ve kurulu `.fig.json` ile `.mm.json` kopyalanmıştır. Kopyaların SHA-256'sı kaynaklarına eşittir.

| İçerik | Dosya sayısı |
| --- | ---: |
| `visio/fig1_study_overview.vsdx` ... `visio/fig6_prereg_chain.vsdx` | 6 |
| `charts/fig7_source_gap_split.{fig,mm}.json` ... `charts/fig17_feature_degradation.{fig,mm}.json` | 22 |
| `README.md` (İngilizce, `references/venue.md` bölüm 7 taslağından), `SHA256SUMS.txt` (29 satır) | 2 |
| Toplam | 30 (332 KB) |

`sha256sum -c SHA256SUMS.txt` 29/29 OK vermiştir. `install.py --yollari-tara paper/submission/Drawing_drafts` "OK 0 file(s) hold a local user path" yazmış ve 0 ile çıkmıştır (`paper/figures/visio_loglari/drawing_drafts_yol_taramasi.txt`). Ek bir taramada `.vsdx` üyeleri dahil hiçbir dosyada `wsl.localhost`, `AppData` ya da kullanıcı klasörü yolu bulunmamıştır. README'deki makaleye özgü iki cümle kaynağında denetlenmiştir: 0.25 mm ızgara ve Visio'dan geri okuma altı denetçi raporunun `grid_mm` ve `readback` alanlarından (en büyük sapma 0.00004 mm), Şekil 1'deki görüntülerin CIFAR-10 ve CIFAR-100'ün ilk dört test görüntüsü olduğu ve büyütmenin piksel tekrarıyla yapıldığı `paper/figures/visio/_icerik_study_overview.py` satır 11-14'ten okunmuştur.

Taslaklara dokunulmamış, yalnız belge özellikleri okunmuştur. Altı `.vsdx`'in altısında da `docProps/core.xml` içinde `dc:creator` ve `cp:lastModifiedBy` "ÇAĞRI ŞAHİN"dir; `dc:title`, `dc:subject`, `cp:keywords`, `dc:description` ile `docProps/app.xml` içindeki `Company` ve `Manager` boştur. Bu ad paketteki başka hiçbir dosyada geçmez. IEEE Access'in hakemlik türü ve ek dosya kuralı (kabul edilen biçimler, `.vsdx` ve `.json`'un kabul edilip edilmediği, boyut sınırı) bu oturumda dergi kılavuzundan okunmamıştır, bu yüzden ek dosya kuralı okunmadı diye kayda geçmiştir. Çift kör hakemlikte yazar adı kimliği açığa çıkarır; paketin bu hâliyle yüklenip yüklenmeyeceği yazara bırakılmıştır. Paket ayrıntısı `paper/figures/visio_loglari/drawing_drafts_paket.json`'dadır.

## 7. Korunan veri dosyaları

`sha256sum -c raporlar/visio_2026-10-31/00_once_sha.txt` (WSL) 22 dosyanın 21'inde OK, `results/C1_REFERANS_FOYU.md`'de FAILED vermiştir (`paper/figures/visio_loglari/derleme_qc_paket_sha_sonra.txt`). Föy bu ajan tarafından değiştirilmemiştir; değişiklik `c315e09` commit'indedir ("Foy M13: sekil kaynaklari ...", 21:22:17). `git diff --numstat 302d56c HEAD` föyde 288 eklenen ve 0 silinen satır gösterir, ekleme M12'den sonraki tek bir bloktur (satır 2374), çalışma kopyası HEAD ile aynıdır (özet `c85fcfc1b683e9f1...`, 2675 satır). Yani föyün daha önce var olan hiçbir satırı değişmemiştir. Bitiş ölçütü 12 bu yüzden 21 dosyada sağlanmış, föyde gerekçeli bir commit'le bilinçli bir büyüme olarak kayda geçmiştir; `00_once_sha.txt`'nin föy satırı yeni özetle güncellenmemiştir, çünkü bu dosya işin başlangıç kaydıdır.

## 8. Yazara ve düzeltme ajanına bırakılanlar

1. `paper/submission/pre_submission_checklist.md` satır 72 hâlâ "The Turkish mirror ... has not yet been brought to this figure set in this round." demektedir; TR aynası artık aynı on yedi şekli taşımaktadır. Gönderim kapısı bu satırı denetlemediği için geçmiştir; satırın güncellenmesi metin ajanının işidir.
2. `fig_qc.py` D3'ün sözcük listesine "SD" ve "90%" girmelidir; `fig13`, `fig14` ve `fig17` altyazıları aralığı zaten yazmaktadır (skill için açık sorun, `06_kart_cizim.md` madde 9 ile aynı).
3. `fig_qc.py` ve `zenginlik.py` `\input` ağacını izlemez, `vz_duzlestir.py` `\InputIfFileExists`'i açmaz; düz kopya metin her değiştiğinde yeniden üretilmelidir (skill için açık sorun, `01_envanter.md` bölüm 9).
4. Visio şekillerinde A3, 8.0 pt tasarımın 120 DPI'da 8.4 pt basılmasını ölçek dışı sayar; skill'in A3 eşlemesi tabana yükseltilen boyu da basamak saymalıdır (skill için açık sorun).
5. Proje ayarında `palette:` satırı kapalıdır ve iki motor iki ayrı palet dosyası kullanır; QC bu yüzden ayar kopyalarıyla koşulmuştur. Kalıcı çözüm, skill'in motor başına palet anahtarı kabul etmesi ya da projenin tek bir palet dosyasına geçmesidir.
6. TR dilli şekiller ikinci turdadır (plan 12.6) ve devir notuna yazılmalıdır; bu turda TR PDF'i İngilizce etiketli şekilleri basar.
7. `zenginlik.py --makale` blok şiddetindeki FAIL'de 0 ile çıkar; çıkış koduna dayanan bir kapı bu sonucu kaçırır.

## 9. Yazılan ve değişen dosyalar

Bu adımda yazılan dosyalar `raporlar/visio_2026-10-31/10_derleme_qc_paket.md`; `paper/submission/Drawing_drafts/` (30 dosya); `paper/figures/qc/<ad>/qc/report.md` ve `report.json` (17 şekil); `paper/figures/qc/qc_ayari_visio.yaml`, `qc_ayari_kart.yaml`, `qc_ozet_derleme.json`, `tutarlilik_derleme.txt`, `zenginlik_makale.{txt,json}`, `zenginlik_makale_gerekceli.{txt,json}`; `paper/figures/visio_loglari/derleme_qc_paket_komutlar.log`, `derleme_qc_paket_durum.json`, `derleme_qc_paket_derleme.log`, `derleme_qc_paket_included_en.txt`, `derleme_qc_paket_included_tr.txt`, `derleme_qc_paket_ad_takimi.md`, `derleme_qc_paket_sha_sonra.txt`, `drawing_drafts_paket.json`, `drawing_drafts_yol_taramasi.txt` dosyalarıdır. Yeniden üretilen izlenen dosyalar `paper/figures/qc/main_en_duz.tex`, `main_en_duz_harita.json`, `main_tr_duz.tex`, `main_tr_duz_harita.json` (düz okuma kopyaları), `paper/manuscript/main.pdf`, `paper/manuscript_tr/main.pdf`, `paper/submission/cover_letter.pdf` (derleme çıktıları) dosyalarıdır. Karalama betikleri (`derle.sh`, `duz_kaynak.py`, `qc_kos.py`, `qc_tablo.py`, `paketle.py`, `ad_takimi.py`, `tasma.py`) oturumun karalama klasöründedir ve depoya girmez. Bu adım `.tex`, kurulu şekil, orijinal şekil ve veri dosyalarından hiçbirine yazmamıştır; `git status --short --untracked-files=no` çıktısındaki bölüm `.tex` değişiklikleri ve `pre_submission_checklist.md` metin ajanlarındandır.
