# Üslup seçimi ve önizlemeler (visio-cizici, adım 3 ve 5)

Tarih 31.10.2026. Hazırlayan görsel üretici ajan (gorsel-uretici). Bu adımda makalenin `.tex` dosyalarına, orijinal şekillere (`paper/figures/konsey/`, `final/`, `final_tr/`, `overview/`) ve veri dosyalarına dokunulmamıştır; bütün yeni dosyalar `paper/figures/visio/`, `paper/figures/charts/`, `paper/figures/onizleme/`, `paper/figures/visio_loglari/` ve bu klasör altındadır. Seçim `paper/figures/SECILI_USLUP` dosyasına yazılmıştır.

En önemli üç sonuç şunlardır. Birincisi, şematik için Üslup 8 (Madry 2018, Dong 2018 ve Ma 2021 kaynaklı katman bloklu klasik şema), veri şekilleri için Üslup 7 (RobustBench 2021 ve Salman 2020 kaynaklı gri çizim alanlı sağlamlık grafiği) seçilmiştir; ikisi de doğrudan çekişmeli makine öğrenmesi literatürünün şekil dilidir. İkincisi, altı önizlemenin altısı da kendi kontrolcüsünden PASS almış, iki montaj da ayrışma şartını sağlamıştır; ancak şablon düzeyinde önerilen üçüncü şematik aday Üslup 5, çizilmiş şekilde Üslup 8 ile yalnız panel sayısında ayrıştığı için (TOKEN-ONLY) atlanmış ve yerine beğeniye uzaklık sırasında sıradaki Üslup 3 önizlenmiştir. Üçüncüsü, `ieee_access` venue'su skill'in kayıt listesinde hâlâ yoktur; önizlemeler venue'yu yalnız kendi süreçlerinde kaydeden proje tarafı bir kabukla (`paper/figures/visio/_vz_ortam.py`) çizilmiştir ve kurulum fazından önce kaydın skill'e girmesi gerekir (bölüm 6).

## 1. Okunan girdiler ve işaret denetimi

`references/begeni_referansi.md` ve `.json`, `references/denge.md`, `references/ayrisma_tablosu.md`, `references/tuzaklar.md` bölüm 1 ve 3, `references/venue.md`, `motor/MOTOR_KULLANIM.md` bölüm 1-5 ve on iki üslubun `meta` alanları (ad, `fits`, beğeni, imza listesi) okunmuştur. `styles/_ISARET.json` sürüm 11'in 24 dosyalık özet listesi diskteki dosyalarla karşılaştırılmış, 24 dosyanın 24'ü tutmuştur; bu yüzden çizime geçilmiştir (T13).

## 2. Seçim ve gerekçe

### 2.1 Şematik: Üslup 8

Karar: şematik şekiller Üslup 8 ile çizilir, çünkü katalogda "uyduğu iş" sütunu bu makalenin alanını adıyla anan tek üslup odur ("Model ve saldırı mimarisi şemaları ... Adversarial makine öğrenmesi ve derin ağ mimarisi makaleleri", `styles/uslup_8.yaml` `meta.fits.schematic`) ve kaynak makaleleri (Madry 2018, Dong 2018, Ma 2021, DenseNet 2017) makalenin kendi atıf çevresindedir. Makalenin çalışma şeması model blokları (ResNet-18, ViT-Tiny), kontrol noktası desteleri ve aktarım matrisleri taşır; Üslup 8'in eğik 25 derece katman bloğu, kesikli iç kap ve görüntü destesi bu nesnelere birebir karşılık gelir ve 11. ilkenin 3B önerisini kendi ölçülmüş görünümüyle karşılar. Kullanıcının "profesyonel makalelerden üslup kopyala" isteği de bu yöndedir: Üslup 8 kırk makalelik taramadan gelir, Üslup 0 ve Üslup H imzalarından hiçbirini taşımaz (ayrışma tablosu bölüm 4: 0/4 ve 0/5).

Seçilmeyenlerin gerekçesi şöyledir. Üslup H beğeniye en yakın üsluptur ve bu yüzden ikinci önizlemedir; ama kaynağı histopatoloji makalesidir, kullanıcının bu makale için istediği profesyonel makalelerden alınmış bir dil değildir ve onun kopyası 00 satır 37'deki "neredeyse birebir kopyaladı" itirazını bu kez ters yönde doğururdu. Üslup 0 IEEE Access ev üslubudur ve dergi tam olarak budur; ancak kullanıcı aynı dilin birebir kopyasına açıkça itiraz etmiştir ve protokol Üslup 0'ı yalnız istenirse önizler. Beğeniye uzaklık Üslup 8 için şablon düzeyinde 0.533'tür (şematik sırada beşinci); bu uzaklık Üslup H dışındaki üsluplar için hedef değil ölçüdür (`references/begeni_referansi.md` bölüm 1, denge.md bölüm 5) ve çizilmiş önizlemede ölçülen değer 0.00'dır (bölüm 4).

### 2.2 Veri: Üslup 7

Karar: veri şekilleri Üslup 7 ile çizilir, çünkü "uyduğu iş" sütunu "Veri ağırlıklı adversarial sağlamlık ve kıyaslama makaleleri"dir (`meta.fits.data`), kaynakları RobustBench 2021, Cohen 2019, Ilyas 2019 ve Salman 2020'dir ve bu makalenin veri şekilleri (orman grafiği, etkileşim grafikleri, saçılım, ısı haritası) bu çevrenin ölçüm grafikleridir. Veride beğeniye uzaklık sırası H, 7, 0, 1, ... olduğu için Üslup 7 H dışındaki en yakın üsluptur (şablon düzeyinde 1.010); çizilmiş önizlemede ölçülen uzaklık 0.04'tür. Üslup 7'nin şematik yanı zayıftır ("şematik yükü ağır makalede seçilmez"), bu yüzden şematik ve veri ayrı üsluptur. İki üslup aynı aileyi (DejaVu Sans) kullanır; makalenin anlam renkleri (ViT #D55E00, ResNet-18 224 #0072B2, R32 #56B4E9, panel #999999, σ #009E73, ρ #E69F00) iki motorda da `konsey_ortak.py`'den okunur ve üslup değişse de değişmez.

Gri çizim alanının gri tonlu baskıda okunurluğu önizlemede denetlenmiştir: noktalar koyu kenarlı ve işaret biçimi (daire, üçgen, kare) çift türünü renkten bağımsız taşır.

## 3. Aday sırası ve montaj sonuçları

Adaylar betikle seçilmiştir: `ayrisma.py --onizleme 8 --tur sematik` ikinci ve üçüncü önizleme olarak H ve 5 (örneklerle sınanmış satır: 2 ve 10), `ayrisma.py --onizleme 7 --tur veri` H ve 1 (örneklerle sınanmış satır: 1 ve 5) vermiştir. Önizlenen iki şekil, en çok kompozisyon taşıyan şema olarak çalışma şeması (`fig:study_overview`, basılı şekil 1) ve en çok panelli veri şekli olarak gradyan hizalama şekli (`fig:gradient_alignment`, basılı şekil 7, 2 x 3 ızgara) seçilmiştir. Her önizleme kendi üslubunun `yontem_semasi` ya da `ic_ice_izgara` şablonuyla, aynı içerikle ve gerçek veriyle çizilmiştir.

| Montaj | Üslup | Panel | Derinlik | Görüntü | Akış | Adım | Çiftler |
| --- | --- | ---: | ---: | --- | --- | ---: | --- |
| şematik, ilk deneme | 8 / H / 5 | 6 / 4 / 5 | 4 / 3 / 4 | var / var / var | var / yok / var | 7 / 7 / 7 | 8-H geçerli; 8-5 TOKEN-ONLY (yalnız panel); H-5 geçerli |
| şematik, son | 8 / H / 3 | 6 / 4 / 4 | 4 / 3 / 4 | var / var / yok | var / yok / var | 7 / 7 / 7 | 8-H geçerli (panel, derinlik, akış); 8-3 geçerli (panel, görüntü); H-3 geçerli (derinlik, görüntü, akış) |
| veri | 7 / H / 1 | 7 / 4 / 6 | 2 / 1 / 3 | yok | yok | 4 / 4 / 4 | üç çift de geçerli (panel, derinlik) |

Karar: Üslup 5 atlanmış ve yerine Üslup 3 önizlenmiştir, çünkü protokol montajın TOKEN-ONLY dediği adayın atlanmasını ve sıradaki üsluba geçilmesini ister; şematikte beğeniye uzaklık sırası H, 5, 3, 0, 8, ... olduğu için 5'ten sonra gelen ve seçilenle ikinciden ayrışan ilk üslup 3'tür (Üslup 0 ancak istenirse aday olur). Üslup 3'ün şablonu görüntü payını 0.0-0.1 aralığında bıraktığı için görüntüsüz çizilmiştir ve bu, ayrışmanın ikinci anahtarını verir. Atlanan denemenin montajı ve sayfası saklanmıştır (`paper/figures/onizleme/sema_uc_uslup_8_H_5_token_only.*`, `sema_uslup_5.*`).

Adlandırma anahtarı üç önizlemede de aynıdır (şematikte adım 7, veride adım 4), çünkü adım şeklin yapısından ve metindeki atıflardan çizimden önce alınmıştır (01_envanter.md bölüm 7.2) ve üslupla değişmemelidir. Ayrışma bu yüzden panel, derinlik, görüntü ve akış anahtarlarından gelir.

## 4. Önizlemelerin yolları ve 5F ölçütleri

Her sayfa IEEE Access geometrisinde (tam genişlik 177.53 mm, iki sütun 85.29 mm), basım boyunda, makalenin bugünkü altyazısıyla ve gri gövde çubuklarıyla kurulmuştur (`scripts/onizleme_montaj.py sayfa`). Satırlar sayfanın altındaki şeritten, yani `denge.degerlendir` çıktısından aynen alınmıştır; köşeli parantezler beğenilen aralıktır.

Şematik (şekil 1):

- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\sema_uslup_8.pdf` (seçilen): kar/cm² 4.05 [2.30-4.30], yazı kutusu 0.24 [0.13-0.28], sayısal 0.08, veri alanı 0.16, derinlik 4, akış 5/5 etiketli, ton 0.32 [0.06-0.49], mürekkep 0.146; beğeniye uzaklık 0.00 (0/5 beğenilmeyen tarafında); eşik dışı: yalnız metin kutu oranı.
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\sema_uslup_H.pdf`: kar/cm² 4.36 [2.30-4.30], yazı kutusu 0.27, sayısal 0.10, veri alanı 0.07, derinlik 3, akış 0/0, ton 0.85 [0.06-0.49], mürekkep 0.116; beğeniye uzaklık 4.14 (0/5 beğenilmeyen tarafında); eşikler tamam.
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\sema_uslup_3.pdf`: kar/cm² 3.90, yazı kutusu 0.23, sayısal 0.10, veri alanı 0.16, derinlik 4, akış 4/3 etiketli, ton 0.35, mürekkep 0.104; beğeniye uzaklık 0.00; eşik dışı: yalnız metin kutu oranı.
- Atlanan: `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\sema_uslup_5.pdf`: kar/cm² 3.66, yazı kutusu 0.23, derinlik 4, akış 2/1 etiketli, ton 0.56, mürekkep 0.109; beğeniye uzaklık 0.88; eşikler tamam.
- Montaj: `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\sema_uc_uslup.pdf` (ve `.png`, `.json`).

Veri (şekil 7):

- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\veri_uslup_7.pdf` (seçilen): kar/cm² 2.26 [2.30-4.30], yazı kutusu 0.13, sayısal 0.46, veri alanı 0.09, derinlik 2, ton 0.83 [0.86-0.92], mürekkep 0.057; beğeniye uzaklık 0.04; eşik dışı: veri alanı payı.
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\veri_uslup_H.pdf`: kar/cm² 2.25, yazı kutusu 0.13, sayısal 0.45, veri alanı 0.22, derinlik 1, ton 0.90, mürekkep 0.061; beğeniye uzaklık 0.02; eşik dışı: veri alanı payı.
- `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\veri_uslup_1.pdf`: kar/cm² 2.66, yazı kutusu 0.16, sayısal 0.46, veri alanı 0.68, derinlik 3, ton 0.58, mürekkep 0.078; beğeniye uzaklık 0.14; eşikler tamam.
- Montaj: `\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\figures\onizleme\veri_uc_uslup.pdf` (ve `.png`, `.json`).

Bütün satırlar `paper/figures/onizleme/onizleme_ozet.json`'dadır. İki ölçüm yorum ister. Üslup H şematiğinin uzaklığı 4.14 çıkmıştır, çünkü bu önizlemede her panel tonlu kart olarak çizilmiş ve ton payı 0.85'e çıkmıştır; beğenilen HP şekil 1'in ton payı 0.399'dur (begeni_referansi.md bölüm 4). Yani beğenilen dil bu içerikte fazla tonla çizilmiştir; H seçilseydi kartların bir kısmının tonsuz kalması gerekirdi. Üslup 7 ve H veri önizlemelerinde "veri alanı payı" eşik dışıdır: ölçü satır tabanlı veri alanını arar ve küçük saçılım ızgarasında düşük okur; bu iki önizlemede çizim alanı kart genişliğinin büyük kısmını kaplasa da ölçü 0.09 ve 0.22 vermiştir. Bu bir ölçüm sınırı olabilir; gerçek çizim fazında denge kapısı (`denge.py`) karara bağlayacaktır.

## 5. Önizlemelerin kapıları ve kanıtı

| Önizleme | Motor | Kontrolcü | Geri okuma, en büyük sapma | Basılı PDF denetimi | Föy karşılaştırması |
| --- | --- | --- | --- | --- | --- |
| şema, Üslup 8 | Visio | PASS | 0.00001 mm | 0 sorun, 103 metin parçası, sayfa 177.588 x 161.925 mm | 19/19 |
| şema, Üslup H | Visio | PASS | 0.00003 mm | 0 sorun, sayfa 177.588 x 122.343 mm | 19/19 |
| şema, Üslup 3 | Visio | PASS | 0.0 mm | 0 sorun, sayfa 177.588 x 121.285 mm | 19/19 |
| şema, Üslup 5 (atlandı) | Visio | PASS | 0.00005 mm | 0 sorun, sayfa 177.588 x 127.847 mm | 19/19 |
| veri, Üslup 7 / H / 1 | kart | mmcheck PASS, 0 sorun | yok | kart denetçisi | 43/43 |

Şematik sayılar (model sayıları 20 / 15 / 14, panel üyeleri 7 / 7 / 6, ikincil üyeler, hücre başına koşu sayıları, ImageNetV2 çiftleri) hücre tablolarından ve Mantel dosyalarından `fig_study_overview_veri.py` ile aynı kuralla sayılmış ve föyün 1496-1499, 1569, 1593, 1741, 1826-1827, 1848, 1873-1887, 1909-1922 ve 1930-1932. satırlarıyla karşılaştırılmıştır (`paper/figures/visio/_icerik_study_overview.py`). Veri şekli `fig_gradient_alignment.py`'nin veri kuralını ve denetimlerini kullanır: Spearman istatistikleri yeniden hesaplanıp JSON ile 1e-9, föyün 1970-1975. satırlarıyla 1e-3 içinde eşleşir; çift türü sayıları ve ortalama c değerleri 2009-2011. satırlarla eşleşir. Gerçek görüntüler CIFAR-10 ve CIFAR-100 test dosyalarının ilk dört görüntüsüdür (`data/cifar-10-batches-py/test_batch`, `data/cifar-100-python/test`; SHA-256'ları kanıt dosyalarındadır). Kanıt dosyaları `paper/figures/visio/_onizleme_study_overview_uslup_<N>.kanit.json` ve `paper/figures/charts/_onizleme_gradient_alignment_uslup_<N>.kanit.json`'dır.

Önizleme aşamasında `fig_mm_pdf.py`, `denge.py`, `fig_qc.py` ve `zenginlik.py --makale` koşulmamıştır; bunlar çizim ve kurulum adımlarının kapılarıdır (adım 7) ve önizlemeler kurulmayacaktır. Sayfa altındaki satır `denge.degerlendir`'in sayısal kararıdır, yanıt dosyalı denge kararı değildir.

## 6. Ortam sorunları ve çözümleri

1. Venue kaydı. `ieee_access` skill'in `motor/figspec/venues.py` kaydında yoktur. Karar: venue, probe'un ölçtüğü bloktan (`raporlar/visio_2026-10-31/venue_ieee_access_blok.txt`) yalnız çizim sürecinin içinde kaydedilmiştir (`paper/figures/visio/_vz_ortam.py`, `kur()`), çünkü skill'i değiştirmek bu fazın yazma alanı dışındadır ve venue verilmeyen motor MDPI geometrisine düşerdi. Sayılar bloğun metninden yürütülür, betikte elle yazılmaz. Skill betikleri (`onizleme_montaj.py`) aynı kabukla koşar. Proje ayarındaki `venue: ieee_access` satırı yorumda kalmıştır, çünkü kabuk kullanılmadan açılırsa `venues.default_name()` KeyError verir. Kurulum fazından önce blok skill'e işlenmeli, `tests/test_venues_kind.py` koşulmalı ve satır açılmalıdır; o zaman kabuk kaldırılır.
2. UNC yolu. Windows Python `//wsl.localhost/Ubuntu-22.04/...` biçimiyle `os.chdir` yapabilir ve Visio `.vsdx`, PDF, SVG, PNG ve EPS'yi UNC klasörüne yazabilir (önce `_unc_sinama` adlı geçici bir şekille sınandı, PASS; geçici klasör silindi). Ters bölülü UNC yolu Git Bash'te bozulduğu için her komut `MSYS_NO_PATHCONV=1` ve ileri bölüyle verilmiştir.
3. Visio görüntü içe aktarımı göreli yolu reddeder ("Bu işlem tam bir dosya adını gerektiriyor", `page.Import`). Çözüm görüntü yolunu `Path.resolve()` ile tam UNC yoluna çevirmektir; kanıt dosyası göreli yolu ayrıca taşır. Hata sırasında Visio kendi PID'sini kapatmış, yabancı Visio açılmamıştır (`visio_tasklist.log`).
4. DPI. Oturum DPI'ı 120'dir ve proje ayarıyla tutar; basım ızgarası 0.6 pt'dir. Tam genişlik 177.53 mm 0.25 mm ızgarasına oturmadığı için kutu genişlikleri ızgaraya aşağı yuvarlanmıştır; Visio sayfası 177.588 mm basılır (yarım ızgara adımı içinde).
5. Yazı tipi. DejaVu Sans ve Open Sans Windows'a ve Visio'ya kayıtlıdır (`yazi_tipi_denetle.py`, PASS). Open Sans'ta birleşik üst çizgi (τ̄ için U+0304) ve ⊇ yoktur. Karar: önizlemelerde τ̄ yerine τ yazılmış, protokol katmanı ⊇ yerine sözcükle verilmiştir; gerçek çizimde Üslup 8 ve 7 DejaVu Sans kullandığı için τ̄ geri getirilebilir.
6. Git Bash heredoc'u Türkçe karakter ve uzun tire içeren yamaları bozdu; yamalar dosyaya yazılıp çalıştırıldı (tuzak 7). İçe aktarma `paper/figures/konsey/__pycache__` klasörünü yaratmıştı; bu klasör yalnız bu işin yan ürünüydü ve silindi, konsey dosyaları değişmedi.
7. Seçili üslup dosyası. Motor `SECILI_USLUP`'u `<kök>/figures/` altında ve yalnız ilk satırıyla okur; dosya görev gereği `paper/figures/` altına yazılmıştır. İlk satır şematik seçimdir (8), veri seçimi (7) yorum satırındadır. Bu yüzden çizim betikleri üslubu `--uslup` ile açıkça alır.

## 7. Çizim fazına notlar

Üslup 8 önizlemesi 161.9 mm yüksekliğindedir ve 0.70 yükseklik payının (165.3 mm) sınırına yakındır; gerçek çizimde (b) panelindeki ImageNetV2 metni kısaltılarak ve (d) ile (e) panellerindeki boşluk toplanarak yükseklik düşürülmelidir. 3B blokların ön yüzü ViT ve ResNet renklerinin koyulaşmış tonudur ve kahverengiye kaçar; ton merdiveni daha açık bir dolgudan başlatılmalıdır. Panel harfleri önizlemede (a)-(e) olarak çizilmiştir; 01_envanter.md bölüm 7.2'deki karar gereği harfler ancak yazım ajanı panelleri metinde ayrı ayrı anarsa kalır.

## 8. Yazılan dosyalar

- `paper/figures/SECILI_USLUP`
- `paper/figures/visio/_vz_ortam.py`, `_palet_uret.py`, `_icerik_study_overview.py`, `_onizleme_study_overview.py`, `_onizleme_sayfalar.py`
- `paper/figures/visio/palettes/adeb_konsey_uslup_{8,H,5,3,7,1}.yaml`
- `paper/figures/visio/_onizleme_img/cifar10_test_0-3.png`, `cifar100_test_0-3.png`
- `paper/figures/visio/_onizleme_study_overview_uslup_{8,H,5,3}.{vsdx,pdf,png,svg,eps,fig.json,kanit.json}` ve `_mm_kontrol.json`
- `paper/figures/charts/_onizleme_gradient_alignment.py` ve `_onizleme_gradient_alignment_uslup_{7,H,1}.{pdf,png,svg,eps,fig.json,mm.json,kanit.json}`
- `paper/figures/onizleme/` altında 7 sayfa önizlemesi (PDF ve PNG), iki montaj, atlanan montaj ve `onizleme_ozet.json`
- `paper/figures/visio_loglari/onizleme_komutlari.log`; Visio `tasklist` günlüğü `visio_tasklist.log`

## 9. Düzeltme eki (31.10.2026 akşamı, Faz A doğrulaması sonrası)

Bu ek `03_faz_a_dogrulama.md`'deki bulguların bu raporu ilgilendirenlerini düzeltir; yukarıdaki metin tarihsel kayıt olarak değiştirilmemiştir ve çeliştiği yerde bu ek geçerlidir. Bağlayıcı plan `04_cizim_plani.md`'dir. Önizlemeler yeniden üretilmemiştir; düzeltmeler çizim fazında uygulanır.

Bölüm 2.2'deki "anlam renkleri ... üslup değişse de değişmez" cümlesi önizleme için doğru değildir. Üslup 8 önizlemesinde ViT küpleri #ECB78C, #D0A17B ve #B38B6A (kahverengi), ResNet küpleri gri mavi tonlarla basılmıştır; anlam hex'leri yalnız lejant karelerinde görünür ve lejanttaki σ ile ρ girdilerinin şekilde karşılığı yoktur. Nedeni önizleme betiğinin 3B dolguyu hex'in beyaza 0.45 karışımından başlatıp üslubun 0, 0.12 ve 0.24 koyulaştırmasını uygulamasıdır. Çizim fazında ön yüz varlığın anlam hex'i olur, sağ ve üst yüz 0.25 ve 0.50 beyaza açılır (en küçük basamak 0.105), lejant ön yüz tonunu gösterir ve σ/ρ girdileri şekil 1 lejantından kalkar (`04_cizim_plani.md` bölüm 4). Bölüm 7'deki "kahverengiye kaçar; ton merdiveni daha açık bir dolgudan başlatılmalıdır" önerisi de bu kararla değişmiştir: merdiven daha açık bir dolgudan değil anlam hex'inden başlar (D1, bulgu M1).

Bölüm 4'teki "Bu bir ölçüm sınırı olabilir" yorumu geri alınmıştır. Üslup 7 önizlemesinde sol özet kartı genişliğin yaklaşık üçte birini kaplar, saçılımlar yaklaşık 28 mm genişliktedir ve ölçülen 0.09 bu darlığı doğru gösterir; ölçüm hatası olduğuna dair kanıt yoktur. Çizimde Spearman özet kartı kalkar, saçılımlar yaklaşık 53.8 mm sütuna çıkar ve çift türü lejantı alt şeride iner. Beklenen pay (yaklaşık 0.74) bir varsayımdır; karar `denge.py` ile verilir (D2, bulgu M5).

Bölüm 2.1'deki "bu makalenin alanını adıyla anan tek üslup odur" ifadesi abartılıdır; Üslup 4'ün `meta.fits.schematic` alanı da "saldırı ve pertürbasyon zinciri ... adversarial sağlamlık" der. Doğru ifade şudur: Üslup 8 bu makale için en uygun şematik üsluptur, çünkü kaynakları makalenin atıf çevresindedir ve eğik 25 derecelik katman bloğu modeller ile matris nesnelerine karşılık gelir. Üslup 4 elenmiştir, çünkü dili görüntü merkezlidir (görüntünün kendisinin anlattığı şemalar, görüntü ızgarası ve montaj) ve görüntü lisansı yoksa uygun değildir; bu makalenin şematik yükü ise çoğunlukla çalışma tasarımı ve kayıt şemasıdır (şekil 1, şekil 2, Y4 ve Y5), görüntü taşımaz. Seçim değişmez (D3, bulgu m6).

Bölüm 6 madde 7'deki durumun sonucu açıkça yazılmalıdır: kullanıcı "üslup N" derse iki N gerekir, biri şematik (bugün 8), biri veri (bugün 7). Motor `SECILI_USLUP`'u yalnız `<kök>/figures/` altında ve ilk satırıyla okur; bu yüzden `hepsini_ciz.py` iki ayrı `--uslup` çağrısıyla ve `paper/figures` klasörünü gösteren bir proje koşturucusuyla çalıştırılır (`04_cizim_plani.md` bölüm 11) (D4, bulgu m8).

Önizlemede panel harfleri sol üstte, başlığın önündedir. Üslup 8'in harf tokenı "(a)", düz, 9.0 pt ve panelin altındadır (`references/panel_adlandirma.md` bölüm 5); motor konumu okumadığı için çizim betiği harfi panel altına elle koyar ve panel başlığı harfle birlikte alt satıra iner (D5, bulgu m7).

Önizlemedeki üç görsel kusur çizimde giderilir: "R224-scr" etiketi ile R224-IN küpü arasında en az 1.0 mm bırakılır, (c) ve (d) panellerinin alt yarısındaki boşluk toplanır (şekil 1 hedefi 142 mm), şekil 7'de çift türü renkleri R224 hex'inden ayrılır (CNN-CNN #000000, transformer-transformer #F0E442, karma #6E6E6E). Önizleme sayfa bağlamında altyazı Times kalınla basılmıştır, IEEE Access altyazısı ise 7 pt Formata'dır (cls satır 218-219); sayfa önizlemesi yeniden üretilirse altyazı yazı tipi Formata ya da açıkça etiketlenmiş bir yedekle basılır (D6, bulgu m9).
