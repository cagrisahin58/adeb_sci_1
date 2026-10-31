# Gönderim paketi notu (31.10.2026)

Hazırlayan: makale yazarı (opus). Kapsam: IEEE Access gönderim belgelerinin yeni başlığa ("Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design"), yeni özete ve brif 12 §2'deki iddia sınırına göre yeniden yazılması; gönderim kapısı (kapı 7, `scripts/gonderim_tutarlilik.py`) ile bildiri tutarlılık kapısının (kapı 5, `scripts/bildiri_tutarlilik.py`) geçirilmesi. `paper/manuscript`, `paper/manuscript_tr`, `paper/bildiri`, `results` ve föy değiştirilmemiştir.

En önemli üç nokta şunlardır. Birincisi, kapı zinciri (`bash scripts/kapilar.sh`) öz-sınama dahil on adımın onunu da geçmektedir ("OZ-SINAMA VE DOKUZ KAPI GECTI"). İkincisi, iki kapı betiğinde yalnız liste ve eşleme düzeyinde değişiklik yapılmış, ATEEC bildirisine dokunulmamıştır. Üçüncüsü, gönderimden önce kullanıcı tarafında kapanması gereken kalemler (ikinci yazar biyografisi, düz şekil yolları, hakem adaylarının iletişim bilgileri, fonlama teyidi, ATEEC kararı) aşağıda "Açık kalanlar" başlığında listelenmiştir.

## 1. Yapılanlar

### 1.1 Gönderim belgeleri (`paper/submission/`)

Eski sürümler `raporlar/hakem_konsey_2026-10-31/_gonderim_eski_2026-10-04/` klasörüne yedeklenmiştir. Yeni belgeler İngilizce ve ABD imlasıyla yazılmıştır.

`cover_letter.tex` tümüyle yeniden yazılmış ve derlenmiştir (`cover_letter.pdf`, 3 sayfa, uyarısız). Mektup sırasıyla O1 manşetini (CIFAR-10'da panel kaynak açığının 0.936'sı simetrik terimde, saf kaynak etkisinde beklenen değer yarıdır; ViT'nin yönlü terimi +0.012 ile ±0.10 içinde eşdeğer), ön kayıtlı tasarımı (29.10.2026 donmuş ön kayıt, 30.10.2026 ek; tek dondurulmuş betik ve SHA-256 kayıtları), ön kaydın kapsamadığı noktaların beyanını (görülmüş ilk tohum, H1 öngörüsünün bilinen açıkla yazılması, K-b çürütme kuralının iki yöne genişletilmesi, hiyerarşik bootstrap'ın sonradan ayrı betikle üretilmesi), dört katkıyı (tanımlanabilirlik; ölçülen büyüklükler ve CIFAR-100 çürütmesi; 2x2 müdahale ve saldırı tarafı; protokol katmanı), iddianın sınırını (logit ölçek, XCiT referansı, CIFAR-100; ImageNetV2 betimsel; gradyan hizalanması mekanizma kanıtı değil, bir ilişki) ve ATEEC durumunu anlatır. Her sayı paragrafın üstündeki `% FOY:` satırıyla föye bağlıdır. "İlk kez", "bildiğimiz kadarıyla" ve "novel" geçmez; yenilik konumlandırması ayrışımın Caussinus yarı-simetri modeline ve Demontis ve ark.'na yakın bir muhasebe özdeşliği olduğunu, içeriğin ölçülen büyüklüklerde ve müdahale yanıtında olduğunu söyler (brif §2, Yenilik satırı). Hakem panelinin B1 (temiz doğruluk karıştırıcısı), B2 (çürütmenin yumuşatılmaması), B3 ("necessary condition" yerine ilişki dili), B6 (uyarlanmış TGR'nin PGD-10'dan zayıf aktarması) ve B9 (q için yarı referansı) düzeltmeleri mektupta da uygulanmıştır.

Karar: ayrı bir "novelty statement" belgesi yazılmadı, çünkü IEEE Access böyle bir belge istemiyor ve gönderim klasöründe yoktu; yenilik konumlandırması kapak mektubunun ilk katkı paragrafındadır.

`highlights.txt` beş maddeyle yeniden yazılmıştır (O1, 2x2 ve karıştırıcı, CIFAR-100 çürütmesi ve ölçek sınırı, saldırı tarafı ile ImageNetV2'nin betimsel niteliği, protokol katmanı ile mutlak gürbüzlük). Föy satırları dosyanın sonundaki iç notlardadır. IEEE Access öne çıkanlar istemez; dosya kapı 7 tarafından denetlendiği ve portal alanlarında kullanılabileceği için tutulmuştur.

`declarations.txt` yeni başlıkla yeniden yazılmıştır. Veri erişimi ImageNetV2, RobustBench CIFAR-100 ve ImageNet panelleri ile timm başlatmalarını kapsar; kod erişimi ön kayıt belgelerini, dondurulmuş çözümleme betiğini ve hücre tablolarını kapsar ve makalenin "Data and Code Availability" bölümüyle aynı kapsamdadır. "About 40 GB" ifadesi föyde olmadığı için çıkarılmıştır. Yeni bölümler: ön kayıt beyanı (§3), önceki sunum (ATEEC, §4) ve üretken yapay zekâ kullanımı (§8, makalenin teşekkür metniyle aynı).

`pre_submission_checklist.md` 31.10 durumuna göre yeniden yazılmıştır: 25 sayfa (`main.pdf`, 31.10.2026 19:15), özet 249 kelime (`check_abstract_body.py`), 7 anahtar kelime, 12 şekil ve 18 tablo ortamı, `main.bbl`'de 77 kaynak, iki biyografi bloğu. Eski listedeki olgusal yanlışlar (dört biyografi bloğu, 17 şekillik eski envanter, depo adresinde TODO) düzeltilmiştir.

`suggested_reviewers.md`'de gerekçeler yeni çerçeveye göre yeniden yazılmıştır. Prof. Hsieh için yanlış yazılmış "ECCV 2022" künyesi `references.bib`'e göre "Transactions on Machine Learning Research, 2022" olarak düzeltilmiş; Dr. Pin-Yu Chen ile Prof. Hsieh'in aynı atıflı makalenin ortak yazarları olduğu not edilmiştir. Ad, unvan, kurum ve e-posta bilgileri bu turda yeniden doğrulanmamıştır ve belgede bu açıkça yazılıdır.

`author_biographies.tex`, `main.tex`'teki biyografilerle çelişen eski bir yardımcı dosyaydı ("M.Sc." diyordu); `main.tex`'in aynası olacak biçimde güncellenmiştir. İkinci yazarın dereceleri ve yılları bilinmediği için `TODO(A13)` yorumu bırakılmıştır.

### 1.2 ATEEC durumu

Makale (01_introduction.tex, son paragraf) "submitted to ATEEC 2026", `references.bib` (`sahin2026behavioral`) "submitted" demektedir; kullanıcı başka bir durum belirtmediği için kapak mektubunda, `declarations.txt` §4'te ve kontrol listesinde "has been submitted to ATEEC 2026 and is under review" yazılmıştır. Üç belge de bildirinin yalnız CIFAR-10 ve tek çiftle sınırlı olduğunu, makalenin onu andığını ve bir iddiasını (temiz doğruluk eşleşince yönün kararlı olmadığı) düzelttiğini söyler.

### 1.3 Gönderim kapısı (`scripts/gonderim_tutarlilik.py`)

Kapı yalnız başlık uyuşmazlığı yüzünden kalıyordu; belgeler yeniden yazılınca başlık denetimi geçmiştir. Betikte iki liste düzeyi değişiklik yapılmıştır. Birincisi, taşıyıcı sayılar listesinde protokol uçlarının biçimi `.1f`'ten `.2f`'ye çevrilmiştir: makalenin yeni sürümü uçları "+4.36" ve "+19.37" diye yazar (giriş katkı 4, IV-I, Tablo III), tek ondalık ise gönderim belgelerini makalede olmayan bir hassasiyete (+4.4, +19.4) zorluyordu. İkincisi, çürütülmüş ifade listesine dört dize eklenmiştir: "source effect of this ViT-Tiny" ve "direction is a source effect" (brif 12 §4'te ÇELİŞKİ işaretli eski okuma), "Not a Weak Source but" (hakem paneli B2 ile değişen eski başlık) ve "necessary condition" (hakem paneli B3). Eski "is symmetric" dizgesi listede kalmıştır; bu yüzden belgelerde "0.936 ... lies in the symmetric term" kalıbı kullanılmıştır.

Öz-sınamada (`scripts/test_gonderim_tutarlilik.sh`) 1. kolun aradığı "güncel başlık" sabiti 4 Ekim'deki başlık değişikliğinden beri eskiydi ve kol "SINAMA HATASI" verip koşmuyordu; sabit yeni başlığa çevrilmiştir. Yedi kolun yedisi beklenen sonucu vermektedir (bozulmamış kopya geçer; eski başlık, karantina değeri, çürütülmüş iddia ve silinmiş taşıyıcı sayı kalır; eksik dosya sessiz geçmez; geri alınınca yine geçer).

### 1.4 Bildiri tutarlılık kapısı (`scripts/bildiri_tutarlilik.py`)

Kapının denetlediği şey bildirinin taşıyıcı sayılarının artefaktlarla sayısal uyumu, Q1 kampanyasının değiştirdiği yön iddiasının tek veri kümesi sınırlamasıyla birlikte durması ve K2 kuralıdır, yani bildirideki oransal iddianın ("4.4-fold") makalede de aynı sayıyla bulunması. On iki sayının on ikisi artefaktla tutuyordu; kapı yalnız K2 yüzünden kalıyordu, çünkü makalenin 31.10 sürümü "N-fold" ifadesini bırakmış ve protokol uçlarını yazmaktadır.

Bildiriye dokunmadan doğru çözüm, kat iddiasını dayanağına eşlemektir. Kat, iki uçtan türetilir (|19.37| / |4.36| = 4.4419); K2'nin amacı olan "kat iddiası tek başına gezmez" koşulu, dayanağı makalede durduğu sürece sağlanır. Betiğe bu yüzden bir KAT ESLEMESI eklenmiştir: bildiri kat diyor ve makale demiyorsa, makalenin iki ucu artefakttan hesaplanan iki ondalıklı değerlerle taşıması aranır, uçlardan biri yoksa ya da artefaktla tutmuyorsa kapı yine kalır. Bildiri ile makalenin yeni sürümü arasında bilerek yapılmış farklar da `BILINEN_FARKLAR` listesinde, her biri makalede onu beyan eden dizeyle eşlenerek belgelenmiştir: önsürüm beyanı ("submitted to ATEEC 2026"), atıf (`sahin2026behavioral`), yön kararlılığı düzeltmesi ("corrects one claim"), başlık ve okuma çerçevesi (yeni başlık) ve kat ifadesi. Beyan dizesi makaleden düşerse fark beyansız kalır ve kapı kalır. Sayısal denetim (bildiri ile artefakt) değişmemiştir.

Öz-sınamaya (`scripts/test_bildiri_tutarlilik.sh`) iki kol eklenmiştir: makale kopyasında üst uç bozulunca (19.37 → 19.73) kapı kalmakta, makaleden "corrects one claim" silinince kapı kalmaktadır. Eski yedi kol da beklenen sonucu vermektedir.

## 2. Kapı çıktıları (31.10.2026)

Tek tek koşu:

```
gonderim_tutarlilik.py   SONUC: GECTI (baslik 4/4 belgede tutuyor; karantina ve curuk ifade yok;
                         tasiyici sayilar 37.93, 29.14, 15.01, 0.84, 4.36, 19.37, 0.23, 1.27 OK)
bildiri_tutarlilik.py    SONUC: GECTI (12/12 sayi tutuyor; KAT ESLEMESI: 4.36 VAR, 19.37 VAR;
                         bilinen farklarin 5/5'i makalede beyanli)
test_gonderim_tutarlilik.sh   7/7 kol beklenen sonuc
test_bildiri_tutarlilik.sh    9/9 kol beklenen sonuc (3b ve 3c yeni)
```

Zincir (`bash scripts/kapilar.sh`):

```
oz-sinama      GECTI
sayilar        GECTI
iddialar       GECTI
ozet           GECTI
TR ondalik     GECTI
bildiri        GECTI
EN/TR ayna     GECTI
gonderim       GECTI
PDF render     GECTI   (25 sayfa)
PDF dizgi      GECTI
OZ-SINAMA VE DOKUZ KAPI GECTI
```

## 3. Açık kalanlar

1. İkinci yazarın biyografisinde dereceler ve yıllar eksiktir (hakem paneli A13). Bilgi yazardan gelmeden doldurulmaz; `main.tex` ve `author_biographies.tex` birlikte güncellenir.
2. Şekil yolları düz değildir (A13). Makale şekilleri `../figures/final/` (3 dosya) ve `../figures/konsey/` (9 dosya) altından okur; yükleme ZIP'i için şekiller `main.tex`'in yanına kopyalanıp yollar düzleştirilmelidir. Bu iş makale dosyasına dokunduğu için bu turun dışında bırakılmıştır.
3. Hakem adaylarının unvan, kurum ve e-posta bilgileri bu turda doğrulanmamıştır; Dr. Gihyun Kim'in WACV 2024 künyesi makalenin kaynakçasında olmadığı için doğrulanamamıştır. Ayrışıma en yakın çalışmaların yazarlarından bir aday eklenmesi açık iştir.
4. Fonlama beyanı ("no specific grant") ikinci yazarla teyit edilmelidir; ORCID, portal hesabı ve APC kaynağı kullanıcı tarafındadır.
5. ATEEC kararı gelirse `sahin2026behavioral` künyesi ile makale, kapak mektubu ve `declarations.txt`'teki "submitted / under review" cümleleri birlikte güncellenir; bildiri kapısının `BILINEN_FARKLAR` listesindeki "submitted to ATEEC 2026" dizesi de o gün yeni ifadeye çevrilmelidir, yoksa kapı kalır.
6. Hakem panelinin föy gerektiren açık işleri (A2-A6, A9, A10) ve 07_appendix.tex'teki iki `TODO(foy)` yorumu (A14) makale tarafındadır; kapak mektubu bunların hiçbirinin sayısını kullanmaz.
7. `paper/submission/` altındaki 4 Ekim tarihli eski LaTeX yardımcı dosyaları (`cover_letter.aux`, `.fls`, `.fdb_latexmk`, `.log`, `.out`) yerinde durmaktadır; yeni PDF karalama klasöründe derlenip kopyalanmıştır. Yükleme paketine yalnız `cover_letter.pdf` girer.
8. Kapak mektubu 3 sayfadır. Editör kısaltma isterse ilk kesilecek paragraf dördüncü katkının ikinci yarısı (özdeşlik ve h ölçeği) ile "suits IEEE Access" paragrafının ikinci cümlesidir; sınır paragrafı ve ön kayıt beyanı kesilmez.

## 4. Düzeltme turu (31.10.2026, çelişik doğrulayıcının KUCUK_DUZELTME kararı üzerine)

Çelişik doğrulayıcı gönderim paketine "küçük düzeltme" kararı vermiş ve gönderimi engelleyen tek bulgu olarak açık depo adresini göstermiştir. Bu bölüm o bulguyla birlikte öteki bulguların nasıl karşılandığını, kapı çıktılarını ve kullanıcının koşacağı komutları kaydeder. Commit atılmamıştır.

### 4.1 Bulgu bulgu yapılanlar

1. Açık depo (yüksek önem). `https://github.com/cagrisahin58/cnn-vit-robustness-protocols` 404 dönmektedir; yerel kopya `teslim/acik_depo/cnn-vit-robustness-protocols` 4 Ekim tarihli tek commit olup eski başlığı taşımakta, ön kayıt belgelerini ve dondurulmuş betiği içermemektedir. `scripts/acik_depo_kur.sh` yeniden yazılmıştır. Betik artık `--dry-run` ile hiçbir dosyaya dokunmadan neyi kopyalayacağını boyutlarıyla listeler, `--with-npz` ile konsey turunun örnek bazlı kayıt dizinlerini ekler ve hiçbir koşulda push etmez (push satırı yorumdadır ve sonda kullanıcıya yazdırılır). Kopya listesine iki ön kayıt belgesi, dört hücre tablosu (`hucre_tablosu.json`, `_b8`, `_b9`, `_a10`), sapma kaydı `results/q1_research/ONKAYIT_SAPMALAR.md`, dondurulmuş betik `experiments/q1_konsey_ayrisim.py`, üç ek betik, `q1_ek_masa.py`, föy kurucusu, föy ve konsey çıktı JSON'ları özgün yollarıyla eklenmiştir. Karar: dosyalar özgün yollarında tutulmuştur, çünkü föy kurucusu ve SHA-256 kayıtları bu yollara başvurur. Karar: listede açıkça adı geçmeyen birkaç küçük dosya da eklenmiştir (`experiments/c1_c3_transfer_matrix.py`, `tests/test_q1_ek.py`, `b9_sarmalayici_b2.json` ve onun `.sarmalayici.json` eki, üç `kosinus_ozet.json`), çünkü föyün M10.6 bütünlük tablosu bunların özetlerini kaydeder. Eski genel döngü `results/q1/*` altındaki her şeyi kopyaladığı için 2,3 GB'lık `konsey_adv_onbellek` de depoya girecekti; döngü artık `konsey_*`, `ek_loglar` ve `ek_regresyon` dizinlerini dışarıda bırakır, konsey dosyaları açık listeden gelir. İç raporları silen `find` satırı `ONKAYIT_SAPMALAR.md` dosyasını da silecekti; bu dosya istisnaya alınmıştır. README.md ve CITATION.cff yeni başlığı taşır; README'de özet, ön kayıt tablosu, geliştirme deposundaki iki commit (e32f2ce, 7325419) ve npz dosyalarının istek üzerine verileceğini, yayımlanan sürümle Zenodo'ya konacağını söyleyen not vardır. Gerçek koşu ayrıca `REGISTRATION_SHA256SUMS.txt` yazar. Betik yalnız `--dry-run` ile koşulmuştur; yerel depo kopyasına dokunulmamıştır.
2. Belgelerde depo iddiası zamana bağlanmıştır. Kapak mektubu ve `declarations.txt` §2-§3 artık ön kayıt belgelerinin, dondurulmuş betiğin ve hücre tablolarının kabulde herkese açık depoda yayımlanacağını, o güne kadar geliştirme deposunda e32f2ce ve 7325419 commit'leriyle zaman damgalı olduğunu ve editör ile hakemlere istek üzerine verilebileceğini söyler. İki commit'in içeriği `git show --stat` ile doğrulanmıştır: e32f2ce ana ön kaydı, dondurulmuş betiği ve `hucre_tablosu.json` dosyasını, 7325419 ise eki, `hucre_tablosu_b8/b9.json` dosyalarını, üç ek betiği ve sapma kaydını içerir. Kontrol listesi §5'teki kod beyanı `[ ]` yapılmış, altına depo oluşturma, betiği koşup push etme, URL'nin 200 dönmesi ve README'nin yeni başlığı taşıması maddeleri eklenmiştir.
3. Literatür genellemesi (`cover_letter.tex`, eski satır 47) kendi çiftimize bağlanmıştır: "In our adversarially trained ResNet-18 and ViT-Tiny pair, ... transfer studies disagree on the direction of this asymmetry." "the common reading ... has so far rested on" yan cümlesi silinmiştir.
4. "Every registered test ran through one frozen analysis script" düzeltilmiştir. Mektuptaki yeni cümle şudur: "The registered tests ran through the frozen analysis script or, for the addendum, through a wrapper around it and a gradient script whose digests were recorded before their first run; every analysis output stores the digests of the scripts that produced it." Karar: yönlendirmedeki "called ... through wrapper and gradient scripts" ifadesi değiştirilmiştir, çünkü B10 Mantel testlerini koşan `q1_ek_gradyan_kosinus.py` dondurulmuş betiği çağırmaz; föy M10.6'ya göre `mantel_*.json` yalnız gradyan betiğinin özetini, `b10_aile.json` ise sarmalayıcının özetini ve dondurulmuş betiğin "dogrulandi" kaydını taşır. Ek betiklerin özetlerinin ilk koşudan önce yazıldığı `ONKAYIT_SAPMALAR.md` satır 17-24'teki "kod eki" kaydından doğrulanmıştır. Aynı düzeltme makaleye ve TR aynasına da işlenmiştir (4.3).
5. "The title states the answer in quantitative form." cümlesi silinmiştir.
6. İlk aralıkta bir kez "(90% intervals over training runs, conditional on the test images and the panel)" verilmiştir; tanım makalenin özetiyle ve Yöntem satır 289 ile aynıdır. Öne çıkanların üst notu da aynı tanıma çevrilmiştir.
7. Son paragraf "Apart from the conference version described above, the manuscript has not been published or submitted elsewhere." cümlesiyle açılır.
8. `highlights.txt` dosyasında "Every number comes from results/C1_REFERANS_FOYU.md" satırı alttaki iç not bloğuna taşınmış, vurgu 4 "transformers are less similar to the panel in a descriptive, untested comparison (-0.142)" olmuştur.
9. Kontrol listesine §0 "Upload Precondition" eklenmiştir: ikinci yazarın onayı ve fonlama teyidi gelmeden yükleme yapılmaz. §5'teki fonlama maddesi ve §10'daki son gözden geçirme bu ön koşula bağlanmıştır.
10. Kapak mektubu kısaltılmıştır. Gövde ana bulgu, ön kayıt ve 2x2 tasarım, iddianın sınırı, ATEEC beyanı, yapay zekâ beyanı ve erişilebilirlik paragraflarından oluşur. Dördüncü katkının sayıları (+4.36 / +19.37, 15.01 ± 0.84, 0.23-1.27) ve AutoAttack sayıları mektuptan çıkmış, öne çıkanlar 5'te durmaktadır; gönderim kapısı mektupla öne çıkanları birlikte okuduğu için taşıyıcı sayıların hepsi bulunur. "The first/second/third/fourth contribution" kalıbıyla açılan dört paragraf kalkmış, içerikleri farklı açılışlı paragraflarda birleştirilmiştir. Kalan her sayının paragrafının üstünde `% FOY:` satırı vardır (M9.5, M9.3, M10.2); depo paragrafının üstünde depo durumunu anlatan bir yorum bulunur. Kısaltmayla mektuptan düşen içerik şunlardır: saldırı tarafındaki 0.960 korunma oranı (öne çıkanlar 4'te duruyor), temiz doğruluk sayıları (karıştırıcı mektupta nitel olarak kalır), XCiT referansı, "whole packages" cümlesi, Demontis ve ark. adı ve portal alanı cümlesi (beyanlarda ve kontrol listesinde duruyor).
11. "corrects one claim" ifadesine dokunulmamıştır. `gonderim_tutarlilik.py` ve `bildiri_tutarlilik.py` değiştirilmemiştir.

### 4.2 Kapak mektubu derlemesi

Mektup `/tmp/kl` içinde `latexmk -pdf -interaction=nonstopmode -halt-on-error` ile derlenmiş, PDF `paper/submission/cover_letter.pdf` üzerine kopyalanmıştır: 0 hata, 0 Overfull, 2 sayfa. İkinci sayfanın yaklaşık üçte ikisi doludur ve bunun yedi satırı imza bloğudur; gövde yaklaşık 1,5 sayfa ve 749 sözcüktür (eski sürüm 3 sayfaydı).

### 4.3 Makalede değişen tek cümle

EN metinde değişiklik `paper/manuscript/sections/03_methodology.tex` satır 347'dedir; satır 338-346'daki föy yorumları korunmuştur. Eski cümle: "All tests ran through one frozen analysis script; the SHA-256 digests of that script (\texttt{4bce2c983ace\ldots}), of the cell tables and of both registration texts match the records written at freezing and those stored in every analysis output." Yeni cümle: "The registered tests ran through the frozen analysis script or, for the addendum, through a wrapper around it and a gradient script whose digests were recorded before their first run; the SHA-256 digests of the frozen script (\texttt{4bce2c983ace\ldots}), of the addendum scripts, of the cell tables and of both registration texts match the records written at freezing or before the first run and those stored in the analysis outputs."

TR aynasında değişiklik `paper/manuscript_tr/sections/03_yontem.tex` satır 339'dadır. Eski metin: "Bütün testler dondurulmuş tek bir analiz betiğiyle koşulmuştur. Bu betiğin (\texttt{4bce2c983ace\ldots}), hücre tablolarının ve iki kayıt metninin SHA-256 özetleri, dondurma anında yazılan kayıtlarla ve her analiz çıktısında saklanan özetlerle örtüşmektedir." Yeni metin: "Ön kayıtlı testler dondurulmuş analiz betiğiyle, ön kayıt ekinin testleri ise bu betiği çağıran bir sarmalayıcıyla ve bir gradyan betiğiyle koşulmuştur. Bu iki betiğin özetleri ilk koşularından önce kayda geçirilmiştir. Dondurulmuş betiğin (\texttt{4bce2c983ace\ldots}), ek betiklerin, hücre tablolarının ve iki kayıt metninin SHA-256 özetleri, dondurma anında ya da ilk koşudan önce yazılan kayıtlarla ve analiz çıktılarında saklanan özetlerle örtüşmektedir." `akademik-turkce` tarayıcısı dosyada kesin ihlal bulmamıştır; bildirdiği dört norm sapması dosya geneline aittir ve bu düzeltmeden önce de vardır.

EN metin `bash scripts/derle_en.sh` ile 25 sayfa ve 0 hatayla derlenmiştir (günlükteki tek "undefined" satırı `T1/pcr/n/n` yazı tipi uyarısıdır). TR metin Windows TeX Live `latexmk -pdf` ile 26 sayfa ve 0 hatayla derlenmiştir.

### 4.4 Kapı çıktıları (düzeltme turu sonrası)

```
oz-sinama      GECTI   kapi 19 sinamanin 84 bozmasinin HEPSINI yakaladi
sayilar        GECTI   EN_EKSIK=0 (TR_EKSIK=33, yalniz bilgi)
iddialar       GECTI   TOPLAM=45  KALAN=0
ozet           GECTI
TR ondalik     GECTI
bildiri        GECTI
EN/TR ayna     GECTI
gonderim       GECTI   baslik 4/4 belge; karantina temiz; tasiyici sayilar 8/8 OK
PDF render     GECTI   (25 sayfa)
PDF dizgi      GECTI
OZ-SINAMA VE DOKUZ KAPI GECTI
```

Açık depo betiğinin kuru koşusu (`bash scripts/acik_depo_kur.sh --dry-run`) kaynak revizyon e8bfc45 üzerinde 139 öğe, tahmini 22 MB ve 0 eksik vermiştir; `REGISTRATION_SHA256SUMS.txt` 42 dosyanın özetini taşıyacaktır. `--with-npz` ile kuru koşu 153 öğe ve tahmini 78 MB vermiştir; açık listedeki JSON'lar tam dizinlerle bir kez daha sayıldığı için bu tahmin biraz yüksektir.

### 4.5 Açık kalanlar ve kullanıcının koşacağı komutlar

Makalenin "Data and Code Availability" paragrafı (`paper/manuscript/main.tex` satır 168) hâlâ "are public at" demektedir. Bu tur o dosyayı değiştirme yetkisi taşımadığı için paragraf olduğu gibi bırakılmıştır. Depo yüklemeden önce yayımlanırsa paragraf doğru hâle gelir ve kapak mektubu ile beyanlardaki "upon acceptance" cümleleri "are available at" biçimine döndürülür; yayımlanmazsa `main.tex` ve TR aynası da "upon acceptance" diline çekilmelidir. Kontrol listesi §5 bu iki yolu yazar.

Kullanıcının adımları sırasıyla şunlardır:

```bash
# 1. Ne kopyalanacagini gor (hicbir sey yazmaz)
bash scripts/acik_depo_kur.sh --dry-run
# 2. Depoyu kur (yerel tek commit; push YOK). Ornek bazli npz istenirse --with-npz
bash scripts/acik_depo_kur.sh            # ya da: bash scripts/acik_depo_kur.sh --with-npz
# 3. GitHub'da cagrisahin58/cnn-vit-robustness-protocols adli BOS, herkese acik depoyu ac
#    (README/LICENSE eklemeden). Depo daha once acildiysa 4. adimda --force gerekir.
# 4. It
cd teslim/acik_depo/cnn-vit-robustness-protocols
git remote add origin https://github.com/cagrisahin58/cnn-vit-robustness-protocols.git
git push -u origin main
# 5. Dogrula
curl -s -o /dev/null -w '%{http_code}\n' https://github.com/cagrisahin58/cnn-vit-robustness-protocols   # 200
```
