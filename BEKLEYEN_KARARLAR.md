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
