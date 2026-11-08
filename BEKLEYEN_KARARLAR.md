# Bekleyen kararlar (01.11.2026)

Her karar soru, kanıt, seçenekler ve öneri sırasıyla yazılmıştır; cevap verildiğinde "Cevap:" satırı doldurulur ve uygulanan iş commit'le birlikte `HANDOFF` notuna işlenir. Devir notu `HANDOFF_2026-10-31.md` dosyasıdır.

## K1. Herkese açık deponun yayımı ve zamanı

Soru: github.com/cagrisahin58/cnn-vit-robustness-protocols deposu gönderimden önce mi açılsın, yoksa kabule mi bırakılsın?

Kanıt: Depo 31.10.2026'da 404 dönmektedir ve yerel kopya `teslim/acik_depo/cnn-vit-robustness-protocols` eski başlıklı tek commit'tir (`raporlar/hakem_konsey_2026-10-31/gonderim_paketi_notu.md` §4.1). Kurulum betiği `scripts/acik_depo_kur.sh` push etmez, komutlar aynı notun §4.5 bölümündedir. Metin bugün "upon acceptance / kabulde yayımlanacak" der (`paper/manuscript/main.tex` Data and Code Availability paragrafı, `paper/manuscript_tr/main.tex` Veri erişimi paragrafı, `paper/submission/cover_letter.tex`, `paper/submission/declarations.txt` §2-3).

Seçenekler: (1) Depo yüklemeden önce açılır ve dört dosyadaki ifade "available at" diline çevrilir. (2) Depo kabule kadar kapalı kalır, ön kayıt e32f2ce ve 7325419 commit'leriyle zaman damgalı olarak istek üzerine verilir.

Öneri: Seçenek 1, çünkü ön kayıtlı bir çalışmada hakemin ön kayıt belgesini ve dondurulmuş betiği doğrudan görebilmesi iddianın en güçlü dayanağıdır ve iş yalnız betik koşusu ile dört dosyada tek cümlelik değişiklikten ibarettir.

Cevap:

## K2. Drawing drafts içindeki `.vsdx` dosyalarında yazar adı

Soru: `paper/submission/Drawing_drafts/visio/` altındaki altı `.vsdx` dosyasının belge özelliklerinde (`docProps/core.xml`, `dc:creator` ve `cp:lastModifiedBy`) duran "ÇAĞRI ŞAHİN" adı kalsın mı?

Kanıt: Ad yalnız bu altı dosyada geçer, paketin öteki dosyalarında yoktur (`raporlar/visio_2026-10-31/10_derleme_qc_paket.md` bölüm 6). Kontrol listesi dergiyi "Single-Blind Review" diye yazar (`paper/submission/pre_submission_checklist.md` başlık satırları), ancak hakemlik türü ve ek dosya kuralı dergi kılavuzundan okunmamıştır.

Seçenekler: (1) Ad olduğu gibi kalır. (2) Ad belge özelliklerinden silinir, `SHA256SUMS.txt` yeniden üretilir. (3) Paket ilk gönderimde yüklenmez, yalnız istenirse verilir.

Öneri: Önce IEEE Access kılavuzundan hakemlik türü teyit edilsin; tek körse seçenek 1 yeterlidir, çift körse seçenek 2 uygulanmalıdır, çünkü yazar adı tek kör hakemlikte zaten görünür ama çift körde kimliği açığa çıkarır.

Cevap:

## K3. EN el yazmasının sayfa sayısı

Soru: EN el yazması 26 sayfa olarak mı gönderilsin, yoksa yaklaşık beş satır kısaltılıp 25 sayfaya mı dönülsün?

Kanıt: Son sayfada yalnız ikinci yazarın üç satırlık biyografisi vardır; plandaki sınır en çok 26 sayfadır ve iki deneme sayfayı geri kazanmamıştır (`raporlar/visio_2026-10-31/11_duzeltme.md` bölüm 2). Kontrol listesi IEEE Access'in kesin sayfa sınırı olmadığını, ayrıca yöntem bölümünün sözcük bütçesinin üstünde olduğunu yazar (`paper/submission/pre_submission_checklist.md` §2, hakem paneli B18).

Seçenekler: (1) 26 sayfa kalır. (2) Yöntem bölümündeki tekrarlar kısaltılarak 25 sayfaya dönülür.

Öneri: Seçenek 2, çünkü B18 zaten yöntem bölümünde kısaltma istemektedir ve aynı iş sayfayı da geri kazandırır; kısaltmadan sonra kapı zinciri ve EN/TR ayna kapısı yeniden koşulmalıdır.

Cevap:

## K4. İkinci yazarın biyografisi ve fonlama beyanı

Soru: İkinci yazarın derece ve yıl bilgileri ile "no specific grant" fonlama beyanının teyidi ne zaman ve kimden alınacak?

Kanıt: `paper/submission/author_biographies.tex` içinde `TODO(A13)` yorumu durur ve aynı bilgi `paper/manuscript/main.tex` biyografi bloğunda eksiktir (`raporlar/hakem_konsey_2026-10-31/gonderim_paketi_notu.md` §3 madde 1 ve 4). Kontrol listesi §0, ikinci yazarın yazılı onayı ve fonlama teyidi gelmeden yükleme yapılmayacağını söyler.

Seçenekler: (1) Bilgi ikinci yazardan istenir ve iki dosya birlikte güncellenir. (2) Biyografi derece ve yıl olmadan kısa biçimde bırakılır.

Öneri: Seçenek 1, çünkü yükleme ön koşulu zaten ikinci yazarın onayını gerektirdiği için aynı yazışmada biyografi bilgisi ve fonlama teyidi birlikte istenebilir.

Cevap:

## K5. ATEEC 2026 bildirisi kararı gelince yapılacak güncellemeler

Soru: ATEEC 2026 bildirisinin kabul ya da ret kararı geldiğinde metin ve kapılar nasıl güncellenecek?

Kanıt: Makale, kapak mektubu, `declarations.txt` §4 ve kontrol listesi bildiriyi "submitted to ATEEC 2026 / under review" diye anar, `references.bib` içindeki `sahin2026behavioral` künyesi "submitted" der (`raporlar/hakem_konsey_2026-10-31/gonderim_paketi_notu.md` §1.2 ve §3 madde 5). `scripts/bildiri_tutarlilik.py` içindeki `BILINEN_FARKLAR` listesi "submitted to ATEEC 2026" dizesini makalede arar ve dize değişirse kapı kalır.

Seçenekler: (1) Karar gelince künye, dört belgedeki ifade ve `BILINEN_FARKLAR` dizesi aynı commit'te güncellenir. (2) Karar gönderimden önce gelmezse metin olduğu gibi gönderilir ve güncelleme hakem sürecinde yapılır.

Öneri: Karar gönderimden önce gelirse seçenek 1, gelmezse seçenek 2; iki durumda da künye, dört belge ve kapı dizesi tek commit'te birlikte değiştirilmelidir, çünkü ayrı değiştirilirse bildiri kapısı kalır.

Cevap:

## K6. İddia kapısında korunan TR ifade

Soru: TR Sınırlılıklar paragrafındaki "Başarılı kaynak protokolü ise kaynağın kendi gürbüzlüğüne bağlı ikinci bir sürücü ekler." cümlesindeki "sürücü" sözcüğü "etken" ile değiştirilsin mi?

Kanıt: Cümle `paper/manuscript_tr/sections/05_tartisma.tex` satır 76'dadır; `scripts/check_manuscript_claims.py` satır 123 (F1 denetimi) tam olarak "ikinci bir sürücü ekler" dizesini arar, bu yüzden metin tek başına değişirse iddia kapısı kalır.

Seçenekler: (1) İfade olduğu gibi kalır. (2) Metin "ikinci bir etken ekler" olur ve kapı sabiti ayrı bir commit'te aynı dizeye çevrilir.

Öneri: Seçenek 2, çünkü "sürücü" İngilizce "driver" sözcüğünün çevirisi olarak Türkçe akademik metinde yabancı durur ve değişiklik iki satırlıktır; metin ile kapı sabiti aynı oturumda değiştirilip kapı zinciri WSL'den koşulmalıdır.

Cevap:

## K7. Yeni şekil dilinde (Üslup Z) veri şekillerinin 3B olup olmayacağı

Soru: Kullanıcı ikinci makale için "komple özgün ve 3 boyutlu yeni şekillerle ve figürlerle" demiştir; veri şekillerinde (benzerlik matrisi, 2x2 etkileşimi, protokol grafikleri) ölçülen değer de yükseklik ya da derinlikle çizilsin mi?

Kanıt: visio-cizici skill'inin kuralı veri grafiğinin 3B çizilmemesini ister, çünkü 3B çubuk ve derinlikli eksen değeri taşıyan uzunluğu ve açıyı izdüşümle değiştirir (`C:/Users/cagri/.claude/skills/visio-cizici/references/uc_boyut.md` satır 5 ve 11); denge kapısı da `3b_veri` yanıtını ihlal sayar. Kol C Faz 1 önizlemesi `paper/figures/onizleme_v2/pv_c_relief` bu yüzden matrisi düz bıraktı: ölçülen değer yalnız eşit hücrelerin rengi, 3B öğeler (kaide, grup sekmeleri, çerçeveler) yalnız donmuş grup tasarımını taşıyor. Çürütücü raporu (`raporlar/sekil_v2_2026-11-07/01_curutucu.md` bulgu 1) bunun kullanıcının "3 boyutlu yeni figür" beklentisini karşılamadığını yazdı. Ayrıntı `raporlar/sekil_v2_2026-11-07/01_uslup_tasarim.md` bölüm 8'dedir. Aynı işte ikinci bir onay konusu vardır: Üslup Z özgün olduğu için kataloğun ayrışma şartı onda ölçüm sınırı aranmadan okunuyor (`scripts/ayrisma.py` `OZGUN` kümesi); bu istisna da kullanıcı onayı bekliyor.

Seçenekler: (1) Kural korunur: veri şekilleri düz kalır, 3B yalnız taşıyıcı sahne, model ve tasarım bilgisinde kullanılır. (2) Üslup Z için kural gevşetilir: veri yüksekliği basılı sayının ve 2B ikizin yanında, tek dimetrik eksende gerçek uzunlukla çizilir, denge kapısının `3b_veri` maddesi bu üslupta gerekçeli muafiyete açılır (motor değişikliği gerekir). (3) Karma: makale gövdesinde veri şekilleri düz, ek dosyada ya da kapak görselinde 3B kabartma sürümleri.

Öneri: Seçenek 3, çünkü dergi okuru değeri uzunluk ve renkten doğru okumalı, kullanıcının "komple 3B" beklentisi de gövde dışındaki görsellerde ve bütün şematiklerde karşılanabilir; seçenek 2 skill kuralını bir üslup için delerek bütün kataloğun veri dürüstlüğü ilkesini zayıflatır.

Cevap (ana oturum, 08.11.2026; kullanıcının 07.11 sözü "komple özgün ve 3 boyutlu yeni şekillerle" bağlayıcı sayıldı): Seçenek 2'nin sınırlı biçimi, yalnız ikinci makale (manuscript_v2) için. Veri şekilleri 3B sahnede kurulur; ölçülen değer her zaman düz bir ikiz kodlamayla da okunur (hücre rengi, basılı sayı ya da düz yüzeyde uzunluk), yükseklik kullanılıyorsa tek dimetrik eksende gerçek uzunlukla ve ikiz kodlamayla aynı şekilde çizilir; altyazı hangi kodlamanın değer taşıdığını söyler. Denge kapısının 3b_veri maddesi Üslup Z'de bu koşula bağlı gerekçeli muafiyet alır (muafiyet kanıt dosyasına yazılır). Asıl makale ve 17 kurulu şekil değişmez. OZGUN ayrışma istisnası kabul; ayrışma raporu yine üretilir (78/78).
