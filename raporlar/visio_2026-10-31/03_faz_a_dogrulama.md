# Faz A celisik dogrulama raporu (31.10.2026)

Salt okur hakem ajaninin yapisal ciktisi ana oturumca dosyaya aktarilmistir.

Karar: KUCUK_DUZELTME

## Ozet

Faz A (envanter, venue, üslup seçimi ve önizlemeler) çelişik doğrulama raporu, 31.10.2026, rol hakem-simulasyonu (salt okur; Visio açılmadı, dosya yazılmadı). Hedef yol: raporlar/visio_2026-10-31/03_faz_a_dogrulama.md (bu metni ana oturum kaydeder).

ÖZET: Fazın çekirdek iddiaları sağlam ve yeniden üretildi. Venue gerçekten ölçülmüş ve sınıfla tutarlı. Şekil sayımı iki dilde 12 ve aux ile tutuyor. Eski 12 şeklin bütün girdileri yerinde ve SHA-256'ları aynı. Montaj ayrışması birebir yeniden çıktı. Korunan dosyalara dokunulmamış. Buna karşın çizim fazına geçmeden düzeltilmesi gereken dört plan hatası ve bir ürün çelişkisi var. Birincisi, seçilen Üslup 8 önizlemesinde anlam renkleri yalnız lejantta kalıyor; küpler kahverengi ve gri mavi, σ/ρ renkleri şekilde hiç yok. İkincisi, Y5 için önerilen sayim_akisi şablonu Üslup 8'de 'uygulanmaz'. Üçüncüsü, şekil 9'a verilen rakam adımının ön koşulu (metinde numarayla anılma) sağlanmıyor. Dördüncüsü, Y2 seçilen üslubun 161.9 mm'lik önizlemesine sığmıyor (165.3 mm tavanı aşar). Ayrıca seçilen veri üslubunda veri alanı eşik dışı (0.09) ve bu, ölçüm sınırı sayılarak geçiştirilmiş. Venue'nun skill kaydına girmemesi yazarların da bildirdiği bir engel. Karar: KÜÇÜK DÜZELTME. Önizlemeler yeniden üretilmeden yalnız plan ve rapor düzeltmeleriyle çizime geçilebilir. Kabulün tek en önemli koşulu şu: çizim başlamadan venue REGISTRY'ye işlensin ve panel_yapisi.yaml ile şablon atamaları (şekil 9, Y2, Y5) düzeltilsin.

Genel: Minor revision, güven H.

GÜÇLÜ YANLAR
(a) Venue: venue_probe_ieee_access.json 'olculdu', pdflatex çıkışı 0. Değerler ieeeaccess.cls satır 261-265 ile birebir: columnsep 6.95 mm, columnwidth 85.29 mm, textwidth 177.53 mm, textheight 672 pt. İki sütun özdeşliği 505.12174 pt'ye karşı 505.12177 pt. Altyazı 7 pt Formata (cls 218-219). \EOD ve yazı tipi sorunlarının çözümü belgelenmiş, makale değişmemiş (main.tex satır 204'te \EOD zaten var). Ölçülmeyen alanlar (8 pt taban, 0.70 yükseklik payı) açıkça 'karar, doğrulanmadı' diye işaretli. Proje ayarı anahtarları motor/visio/proje_ayari.py docstring'iyle uyumlu (visio.out_dir/preview_dir/dpi/tasklist_log; install.target/visio_dir/charts_dir/qc_dir/log/mapping; language). palet_kaynagi zararsız bir bilgi anahtarı.
(b) Envanter tam: güncel kaynakta (HEAD c8be9b7) EN ve TR'de 12 figure ortamı var ve aux etiketleri 1-12 envanterle aynı sırada. included_figures.py --tablo düz kopyalarda 12 şekil veriyor (11 ve 12 STALE). Ham main.tex'te 0 veriyor, bu da \input ve \InputIfFileExists sınırına ilişkin teşhisi doğruluyor. Fazdan sonra gelen 0928be5 ve c8be9b7 commit'leri yalnız 03_methodology'de bir satırı ve main.tex'i değiştirmiş; altyazı satır numaraları (EN 37, 162, 579, 589, 07_appendix 119; TR 29, 154, 581, 592, 115) bugün de doğru. 12 kanıt dosyasının girdilerini yeniden hash'ledim, eksik ya da uyuşmayan yok (şekil 9 veri ve üst kaynak, şekil 10 veri ve 17 üst kaynak dahil). Föyün bugünkü özeti 00cc422f, kanıtlardaki 42c7dc34 ve 57e9659e eski; rapor bunu doğru yazmış. Şekil 11 için föy satır 19 ve 354 iddiası doğru.
(c) Bütçe aritmetiği satır satır tutuyor. 12 pt satır = 4.233 mm; 672/12 = 56 satır. Örnek hesaplar: Y1 (88+12+7)/4.233 = 25.3; Y4 (86.7+7)/4.233 x 2 = 44.3; Y1-Y7 toplamı -90 satır = 0.80 sayfa.
(d) Panel atfı iddiası doğru: iki dilde metinde tek panel atfı var (04_experiments.tex:141 'Figure~\ref{fig:source_gap_split}a'; TR aynı satır). 03_methodology 183-186'daki (a)-(d), önerme şıklarıdır, panel değil; konumla atıf yok. Ardışık tür en çok 2, harfli pay sınırın altında.
(e) Aday seçimi betikle yeniden üretildi: ayrisma.py --onizleme 8 --tur sematik H ve 5 veriyor, --onizleme 7 --tur veri H ve 1 veriyor. 5'ten 3'e geçiş protokole uygun (TOKEN-ONLY aday atlanır, sıradakine geçilir).
(f) Altı önizleme var: sema 8/H/3 ve veri 7/H/1, ayrıca atlanan 5. Hepsi IEEE Access tam genişliğinde, altyazı ve gövde çubuklarıyla bir sayfa bağlamında, alt satırda 5F ölçüleri var. Montajı dosya yazmadan onizleme_montaj.composition_keys/differing_keys ile yeniden koştum. Sonuç raporla birebir: 8-H [panel, derinlik, akış], 8-5 [panel] TOKEN-ONLY, 8-3 [panel, görüntü], H-3 [derinlik, görüntü, akış]; veri 7-H, 7-1, H-1 [panel, derinlik]. Önizlemedeki sayıları föyde yeniden okudum: Spearman r +0.943/+0.944/+0.981/+0.912/+0.694/+0.893 (föy 1970-1975), çift türü sayıları ve ortalama c 91/15/84, 55/6/44, 36/10/45 (föy 2009-2011, toplamlar 190/105/91), koşu sayıları 3/2/2/2 (föy 1496-1499). Hepsi tutuyor.
(g) git (WSL, salt okur): paper/ ve results/ altında izlenen değişiklik yok (git status --untracked-files=no boş). 00_once_sha.txt'deki 22 dosyanın 22'si 'OK'. konsey/__pycache__ yok. Yeni dosyalar yalnız paper/figures/{SECILI_USLUP, visio_cizici.yaml, panel_yapisi.yaml, visio/, charts/, qc/, onizleme/, visio_loglari/} altında izlenmeyen dosya olarak duruyor. results altındaki ?? dosyalar başlangıç kaydında da var.

MAJOR
[M1] Üslup 8 önizlemesinde anlam renkleri yalnız lejantta duruyor. SVG'de #D55E00, #0072B2, #009E73 ve #E69F00 birer kez geçiyor. ViT küpleri #b38b6a/#d0a17b/#ecb78c, ResNet küpleri #6a92a7/#88a8ba ile çizilmiş. σ/ρ lejant girdilerinin şekilde karşılığı yok. Bu, 02 bölüm 2.2'deki 'anlam renkleri üslup değişse de aynı kalıyor' iddiasıyla çelişiyor. Düzeltme: ton merdiveni varlık hex'inden başlamalı ya da lejant gerçek ön yüz tonunu göstermeli, kullanılmayan girdiler çıkarılmalı.
[M2] Y5 için sayim_akisi şablonu, uslup_8/sablonlar.yaml satır 73-74'te 'uygulanmaz'. Uygulanır bir şablona bağlanmalı.
[M3] Şekil 9 için rakam adımı (3) 'metinde numarayla anılan düzey' ister; protokoller metinde ve Tablo tab:protocol_masks'ta adla anılıyor. Ayrıca envanter şekil 9'u 'karma' diye tanımlarken yapı dosyası 'numarali_duzey' diyor. Şerit ya da karma olmalı; dizi kuralı yine sağlanır.
[M4] Y2 bütçesi eski 129 mm üzerine kurulmuş. Üslup 8'de aynı içerik 161.9 mm, tavan 165.3 mm; Y2 eklenince yaklaşık 182 mm olur ve A4 kapısı bloklar. Y2 ayrı bir şekil olmalı ya da şekil 1 yeniden kurulmalı. Y6 (şekil 5 tek sütunda 156 mm) da yeniden denetlenmeli.
[M5] Veri üslubu 7 önizlemesinde saçılım panelleri yaklaşık 28 mm genişlikte ve veri alanı 0.09. Görüntü, ölçümün haklı olduğunu gösteriyor. 'Ölçüm sınırı' yorumu kanıtsız; çizimde özet kartı daraltılmalı.
[M6] ieee_access, venues.py REGISTRY'de yok (yalnız ieee_tran, satır 223). Kabuksuz her kapı MDPI'ye düşer. Kayıt, test ve yaml satırı kapılardan önce yapılmalı (yazarlar bildirmiş).

MINOR
[m1] Harfli pay 0.00 değil 0.08 (denge.py 701-702 harfli karmayı sayar).
[m2] Önizlemede şekil 1 (a)-(e) beş harfli, plan dört panelli.
[m3] '7 şekil harfli, rozet 15/18' sayıları altyazı ayrıştırmasından geliyor; görüntüde 10 şekil harfli.
[m4] Şekil 10'un üst kaynağı 18 değil 17.
[m5] Y1 'veri gerekli' satırı scripts/konsey_b3_kuyruk.sh (satır 11, 90-99) ve src/training/trainer.py'yi kaynak olarak anmalı.
[m6] 'Alanını adıyla anan tek üslup' abartılı; Üslup 4 de adversarial sağlamlığı anıyor. Şematik yükün çoğu tasarım ve kayıt şeması.
[m7] Üslup 8'in harf konumu 'panel altında' olmalı, önizlemede sol üstte.
[m8] SECILI_USLUP paper/figures altında olduğu için motor okumuyor ve 8/7 bölünmesi 'üslup N' tek komutuyla işlemiyor.
[m9] Görsel ayrıntılar: R224-scr etiketi küpe değiyor, (c) ve (d)'de boşluk var, önizleme altyazısı Formata değil Times, şekil 7 önizlemesinde #0072B2 CNN-CNN'i kodluyor.
[m10] Satır başına sözcük ölçüldü: 9.76 (11 değil); bütçe muhafazakâr kalıyor.
[m11] Envanter tablosunda TR'de final_tr kaynakları eksik.

İDDİA VE KANIT
1 venue ölçüldü | probe json ve cls 261-265 | güçlü | doğrulandı.
2 12 şekil EN ve TR | grep, aux, included_figures | güçlü | doğrulandı.
3 eski şekillerde veri gerekli yok | 12 kanıt dosyasının SHA'sı yeniden hesaplandı | güçlü | doğrulandı.
4 tek panel atfı | grep | güçlü | doğrulandı.
5 bütçe yaklaşık -90 satır | aritmetik | orta (Y2 ve Y6 sığma sorunu) | kısmen.
6 montaj ayrışması | fonksiyon yeniden koşuldu | güçlü | doğrulandı.
7 anlam renkleri korunuyor | SVG dolguları | zayıf | çürütüldü.
8 harfli pay 0.00 | denge.py | zayıf | düzeltilmeli (0.08).
9 şekil 9 rakam | kural adım 3 | eksik | kurala aykırı.
10 korunan dosyalar değişmedi | git ve 22 SHA | güçlü | doğrulandı.

EKSİK İŞLER: üslup ile şablon uygunluk denetimi (envanterdeki her şablon seçili üslupta uygulanır mı); Y2, Y6 ve Y1 için seçili üslubun önizleme ölçeğinde yükseklik denetimi; denge.py ile veri alanı payının çizimde karara bağlanması.

HAKEMİN SORACAKLARI: 'Tablo 3 şekle dönerse kayıtlı eşikler nerede okunur?' Yanıt: Y4 tabloyu eke taşıma seçeneğini zaten tutuyor; eşikler JSON'dan ve föyden gelir. 'Şekillerdeki renkler neyi kodluyor?' M1 düzeltilmeden lejant ile işaret uyuşmuyor; düzeltme şart.

İncelenen yollar: \\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\raporlar\visio_2026-10-31\01_envanter.md, 02_uslup_secimi.md, venue_probe_ieee_access.json, venue_ieee_access_blok.txt; \\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\visio_cizici.yaml, panel_yapisi.yaml, SECILI_USLUP, qc\panel_atiflari_en.md ve _tr.md, onizleme\*.png, visio\_onizleme_study_overview_uslup_8.svg; C:\Users\cagri\.claude\skills\visio-cizici\styles\uslup_8\sablonlar.yaml, motor\figspec\denge.py.

## Bulgular

### 1. [major] Seçilen Üslup 8 önizlemesinde anlam renkleri bozulmuş; rapordaki 'anlam renkleri üslup değişse de aynı kalıyor' iddiası çizimle çelişiyor

Kanit: paper/figures/visio/_onizleme_study_overview_uslup_8.svg dolgu sayımı: #D55E00, #0072B2, #56B4E9, #009E73 ve #E69F00 birer kez geçiyor, yani yalnız lejant karelerinde. ViT küpleri #b38b6a/#d0a17b/#ecb78c (kahverengi), ResNet küpleri #6a92a7/#7ba9c2/#88a8ba (gri mavi) ile çizilmiş. Lejant 'symmetric, σ' (yeşil) ve 'directional, ρ' (turuncu) renklerini veriyor ama şekilde bu renkte hiçbir öğe yok. 02_uslup_secimi.md bölüm 2.2 ve bölüm 7 bunu yalnız 'kahverengiye kaçıyor' diye geçiştiriyor.

Duzeltme: Çizim fazında 3B ton merdiveninin ön yüzü varlığın hex'inden başlamalı (yalnız üst ve sağ yüz açılmalı) ya da lejant kareleri gerçekten basılan ön yüz tonunu göstermeli. Şekilde kullanılmayan σ/ρ lejant girdileri ya kaldırılmalı ya da (e) panelindeki σ, ρ terimleri bu renklerle basılmalı. 02 raporundaki cümle düzeltilmeli.

### 2. [major] Y5 fig:prereg_chain için önerilen 'sayim_akisi' şablonu seçilen Üslup 8'de uygulanmaz

Kanit: 01_envanter.md bölüm 5, Y5 satırı 'sayim_akisi'. Öte yandan styles/uslup_8/sablonlar.yaml satır 73-74: 'sayim_akisi: uygulanmaz: kaynaklarda (Madry, Dong, Ma, DenseNet, EDM) sayım akışı yoktur ...'. Üslup 7'de de uygulanmaz (uslup_7/sablonlar.yaml 76-77).

Duzeltme: Y5 Üslup 8'in uygulanır bir şablonuna (yontem_semasi, yatay zaman şeridi, ya da tablodan_sekle) yeniden bağlanmalı ve panel_yapisi.yaml yorumu buna göre güncellenmeli. Envanter ile üslup seçimi arasında şablon uygunluğu denetimi de yapılmalı (Y1 model_acilimi_3b Üslup 8'de satır 294'te var, sorun yok).

### 3. [major] Şekil 9'a verilen 'rakam' (adım 3) kuralın ön koşulunu sağlamıyor

Kanit: panel_adlandirma.md bölüm 1 adım 3: 'Metinde zaten numarayla anılan düzeyler'. Oysa metin protokolleri hiçbir yerde numarayla anmıyor; 03_methodology.tex 217-262 ve Tablo tab:protocol_masks adlarla veriyor (Unconditioned, Target-correct, Both-correct, Successful-source), 04_experiments.tex 579'daki altyazı da A-D/ad kullanıyor. Ayrıca 01_envanter.md bölüm 3 şekil 9'u 'karma (şematik ve veri)' diye tanımlarken panel_yapisi.yaml 'numarali_duzey' yazıyor.

Duzeltme: Şekil 9 'kucuk_katlar/serit' (iki panel yan yana, harfsiz başlık şeridi; halkalarda protokol adları) ya da 'karma' (akış + şerit) olarak yeniden sınıflandırılmalı. Bu, 16 şekillik dizide ardışık kuralı bozmuyor (… renk, şerit, şerit, yok, şerit …: en uzun 2). Rakam halkası istenirse önce yazım ajanı metinde 1-4 numaralandırmasını getirmeli; bu da 'içeriği azalt' isteğine ters düşer.

### 4. [major] Y2 (panel üyeleri şekil 1'e) seçilen üslubun ölçülmüş yüksekliğiyle sığmıyor; sayfa bütçesi eski şekil yüksekliğine göre kurulmuş

Kanit: 01_envanter.md bölüm 5 Y2: 'şekil 1'e yaklaşık 20 mm'. Bütçe bugünkü şekil 1'in yaklaşık 129 mm'si üzerine kurulu. Oysa aynı içerikle çizilen Üslup 8 önizlemesi 177.588 x 161.925 mm (02 raporu bölüm 5), tavan ise 0.70 x 236.181 = 165.33 mm. Y2 eklenince yaklaşık 182 mm olur ve A4 yükseklik kapısı toleranssız (T30) bloklar.

Duzeltme: Y2 ya şekil 1 içinde değil ayrı bir tek sütunluk 'panel üyeleri' şekli olmalı (yeni maliyet hesabıyla) ya da şekil 1'in (b) paneli yeniden kurulmalı ((d)/(e) boşlukları toplanarak en az 20 mm kazanılmalı) ve bütçe 161.9 mm tabanıyla yeniden hesaplanmalı. Aynı denetim Y6 için de yapılmalı: şekil 5 121+35 = 156 mm tek sütun, sınıra yakın.

### 5. [major] Seçilen veri üslubu (7) önizlemesinde veri alanı eşik dışı; rapor bunu kanıtsız 'ölçüm sınırı olabilir' diye geçiştiriyor

Kanit: veri_uslup_7.png: sağdaki 2x3 saçılım ızgarasının her paneli yaklaşık 28 mm genişlikte, CIFAR-10 noktaları üst üste biniyor. Sol 'Rank correlation' kartı genişliğin yaklaşık üçte birini alıyor. Ölçülen veri alanı payı 0.09 (H 0.22, Üslup 1 0.68). veri_gosterimi.md 'veri ekseni şekil genişliğinin en az %45'i' der. Görünen durum ölçümü doğruluyor, ölçüm hatası olduğuna dair kanıt yok.

Duzeltme: Çizim fazında Spearman özet kartı daraltılmalı ya da alt şeride indirilmeli ve saçılımlar en az yaklaşık 45 mm genişliğe çıkarılmalı. Denge kapısı (denge.py) koşmadan 'ölçüm sınırı' yorumu raporda varsayım olarak işaretlenmeli.

### 6. [major] Venue kaydı skill'de yok; çizim yalnız süreç içi kabukla doğru geometriyi alıyor (yazarların da bildirdiği engel)

Kanit: motor/figspec/venues.py'de yalnız 'ieee_tran' kaydı var (satır 223), ieee_access yok. visio_cizici.yaml'da 'venue: ieee_access' satırı yorumda. Kabuk paper/figures/visio/_vz_ortam.py kur(). Kabuksuz koşan her skill komutu (fig_mm_pdf, fig_qc, install, onizleme_montaj --venue varsayılanı) MDPI geometrisine düşer.

Duzeltme: Kurulum ve kapı fazından önce ana oturum venue_ieee_access_blok.txt'yi REGISTRY'ye işlemeli, tests/test_venues_kind.py ve test_venue_probe koşmalı, yaml satırını açmalı; ardından önizlemeler değil ama her kapı yeniden koşmalı. Ölçüm doğru: cls satır 261-265 ile birebir (85.29/177.53 mm, 672 pt) ve 2x242.67355+19.77464 = 505.12174 pt.

### 7. [minor] Harfli pay hesabı motorla çelişiyor

Kanit: 01_envanter.md bölüm 7.2: 'harfli pay 0.00 (karma şekil harfli sayılmaz)'. motor/figspec/denge.py satır 701-702 harf içeren karma şekli harfli sayar. Şekil 1 harfle kalırsa pay 1/12 = 0.083 olur (bölüm 7.3'teki 1/16 ise doğru).

Duzeltme: Bölüm 7.2'deki pay 0.08 olarak düzeltilmeli; sınır (0.40) yine sağlanıyor.

### 8. [minor] Şekil 1 önizlemesinde beş harf var, planda dört

Kanit: sema_uslup_8.png: (a) Trained models, (b) Reference panels, (c) Matrices, (d) Registered, (e) Exact split. panel_yapisi.yaml ve 01 bölüm 7.4 ise (a) modeller, (b) paneller, (c) ölçüm, (d) kayıt diyor.

Duzeltme: Yapı dosyası ve altyazı değişiklik listesi beş panelli düzene göre güncellenmeli; harfin kalma koşulu da (en az üç panelin metinde ayrı anılması) bu beş adla yazılmalı.

### 9. [minor] 'Bugün 7 şekil harfli', 'rozet 15/18' sayıları şekillerin kendisini değil altyazı ayrıştırmasını yansıtıyor

Kanit: 01 bölüm 7.2 tablosu şekil 1, 2 ve 9'un da görüntü içinde harf taşıdığını yazıyor ((a)-(d), (a)/(b) ve A-D); yani bugün 10 şekil harfli. EN 15 ile TR 18 arasındaki fark sayaç sınırından geliyor (panel_atiflari_en.md: şekil 4 'b', 7 'acd'; TR: 'bc', 'acdf').

Duzeltme: Raporda 'altyazıda harf anan 7 şekil; görüntüde harf taşıyan 10 şekil' diye ayrılmalı ve rozet sayısının altyazı ayrıştırma sayısı olduğu yazılmalı.

### 10. [minor] Şekil 10'un üst kaynak sayısı yanlış

Kanit: 01 bölüm 3, şekil 10: '18 üst kaynağı'. paper/figures/final/fig_spread_clean_gap.kanit.json ust_kaynaklar_sha256 17 girdi taşıyor; 17'sinin SHA-256'sı bugün tutuyor, veri JSON'u da tutuyor.

Duzeltme: 17 yazılmalı.

### 11. [minor] Y1 'veri gerekli' satırı mevcut makine kaynağını anmıyor

Kanit: Tarif scripts/konsey_b3_kuyruk.sh satır 11 ve 90-99'da duruyor (AdamW, lr 1e-3/1e-4, wd 0.05, -e 100, -b 64, --patience 20, temiz 200/30 epok). Föyde yok (grep: AdamW/patience yok), föy satır 1472'de AT çöküş denetimi TAMAM, yani lr değişmemiş.

Duzeltme: Gereken dosya konsey_b3_kuyruk.sh ve src/training/trainer.py'den üretilecek diye kaynak adıyla yazılmalı; föy satırı şartı (karantina kuralı) kalmalı.

### 12. [minor] 'Alanını adıyla anan tek üslup Üslup 8' ifadesi abartılı

Kanit: styles/uslup_4.yaml meta.fits.schematic: 'saldırı ve pertürbasyon zinciri ... adversarial sağlamlık'. Üslup 0 ise 'Çalışma tasarımı ve veri kökeni şemaları' der; bu makalenin şematik yükü (şekil 1, 2, Y4, Y5) büyük ölçüde çalışma tasarımı ve kayıt şemasıdır, mimari şeması değil (yalnız Y1).

Duzeltme: Gerekçe 'en uygun' diye yumuşatılmalı ve Üslup 4'ün neden elendiği (görüntü lisansı ve görüntü merkezli dil) bir cümleyle yazılmalı. Seçim yine savunulabilir.

### 13. [minor] Üslup 8 panel harfi konumu kaynak üsluba uymuyor

Kanit: panel_adlandirma.md bölüm 5 tablosu: Üslup 8 '(a), düz, 9.0 pt, panelin altında'. Önizlemede harfler sol üstte, başlığın önünde. Motor konumu okumuyor (aynı bölüm, son paragraf).

Duzeltme: Harf kalacaksa çizim betiğinde panel altına elle yerleştirilmeli; kalmayacaksa sorun düşer.

### 14. [minor] Seçili üslup ikiye bölündüğü için 'üslup N' tek komutu ve motorun SECILI_USLUP okuması işlemiyor

Kanit: paper/figures/SECILI_USLUP ilk satır '8', veri 7 yorumda. motor/figspec/uslup.py satır 111 dosyayı <kök>/figures/SECILI_USLUP'ta arıyor, yani paper/figures altındaki dosya okunmuyor.

Duzeltme: Son mesajda kullanıcıya 'üslup N' yazarsa şematik ve veri için ayrı ayrı N verilmesi gerektiği söylenmeli; hepsini_ciz.py çağrısı iki ayrı --uslup ile hazırlanmalı.

### 15. [minor] Önizlemede küçük görsel kusurlar ve sayfa bağlamının sadakati

Kanit: sema_uslup_8.png: 'R224-scr' etiketi R224-IN küpüne neredeyse değiyor; (c) ve (d) panellerinin alt yarısı boş. Sayfa altyazısı Times kalın 'Figure 1.' ile basılmış; IEEE Access altyazısı 7 pt Formata (cls 218-219). Şekil 7 önizlemesinde #0072B2 'CNN-CNN' çift türünü kodluyor, oysa makalede R224'ü kodluyor.

Duzeltme: Çizim fazında etiketle küp arasında en az 1 mm boşluk bırakılmalı, boşluklar toplanmalı, çift türü renkleri R224 hex'inden ayrılmalı ya da ailenin anlamı altyazıda açıkça bağlanmalı.

### 16. [minor] Sayfa bütçesindeki satır başına sözcük varsayımı ölçülmemiş

Kanit: 01 bölüm 5: '11 sözcük (tahmin)'. EN main.pdf sayfa 3-12'deki 640 tam gövde satırında (10 pt, 230-250 pt genişlik) ölçülen ortalama 9.76, ortanca 10. Metin kazancı yaklaşık %13 eksik hesaplanmış, yani bütçe muhafazakâr.

Duzeltme: Ölçülen 9.8 değeri yazılmalı. Toplamda, Y6'da tablonun eke gitmesiyle toplam sayfa kazancının yaklaşık 0.5 sayfaya indiği ayrıca belirtilmeli.

### 17. [minor] Envanterde TR şekil 11 ve 12'nin kaynak klasörü eksik

Kanit: TR 07_ek.tex 28 ve 114 final_tr/fig2_epsilon_sweep.pdf ve final_tr/fig5b_attention_entropy.pdf kullanıyor; 01 bölüm 2 tablosu yalnız şekil 10 için 'TR'de final_tr/' diyor.

Duzeltme: Tablo düzeltilmeli; TR kanıt dosyaları da (final_tr/*.kanit.json) envanterde anılmalı.

