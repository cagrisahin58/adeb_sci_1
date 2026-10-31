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
