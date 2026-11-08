# Kol D çürütücü raporu (opus-curutucu, 08.11.2026, birinci tur)

Denetlenen teslimat: `raporlar/curutme_2026-11-07/03_deney_zinciri.md`, `raporlar/konsey_2026-10-29/ON_KAYIT_EK_CURUTME_2026-11-08.md`, `scripts/curutme_zincir.sh`, kod farkı (cli/train.py, src/training/trainer.py, src/models/r224.py, src/models/__init__.py, .gitignore), çatal betikler (experiments/q1_curutme_*.py, scripts/curutme_*.py), indirme ve duman çıktıları (results/q1/curutme_2026-11-08/). Çürütücü dosya değiştirmemiştir; rapor yardımcı Fable tarafından kaydedilmiştir. Kapanışlar ikinci turda yürütücü tarafından yapılmış, sonuç `03_deney_zinciri.md` içindeki "Çürütücü bulguları ve kapanışları" bölümüne işlenmiştir.

## Karar (birinci tur)

duzeltilmeli. Zinciri bozan bir hata ya da dondurulmuş dosyaya dokunan bir değişiklik bulunmamıştır. Ön kayıtta iki, rapor ve CKA betiğinde bir major bulgu dondurmadan önce kapatılmalıdır.

## Bulgular

1. major, `ON_KAYIT_EK_CURUTME_2026-11-08.md:69` ve `scripts/curutme_denetim.py:131`. B pilotunda t = pilot duvar süresi / 2 tanımı sabit başlatma süresini de içeriyor. Duman B koşusunda duvar süresi 114 s, eğitim döngüsü 70 s (`_duman/duman_kos.log:2`, `_duman/duman_B_s2401.log:23`); yükleyici güçlü artırmayla epok başına 25,0 s (`_duman/yukleyici_hizi.txt:2`). GPU boşken bile t yaklaşık 47 s, E_temiz yaklaşık 134; paylaşımlı GPU'da 70 dolayı. E_temiz = 200 için t 31,5 s'nin altında olmalı, bu ölçülen hızla olanaksız. Konsey kuralı "epok süresi t" diyor (`02_deney_adaylari.json` B.durdurma_kurali, bütçe 23,8 s/epok). Beklenen: t epok farkından ölçülsün (ikinci epok duvar süresi eksi birincisi ya da logdaki eğitim süresi) ya da sapma açıkça yazılsın.

2. major, `ON_KAYIT_EK_CURUTME_2026-11-08.md:11` ve `:58-59` (ayrıca `03_deney_zinciri.md:31`, `:57`). "İki nicelik görülmüştür" denmesine karşın `_duman/cozumleme_sinama_A.json` daha fazlasını taşıyor: sigma_T(V-IN) eksi sigma_T(R224-IN) = -0,029, %90 aralığı [-0,042; -0,014], `sigma_etiketi: negatif` (A'nın sigma satırında "H yanlış" bölgesi); `rho_etiketi: esdeger`; ikincil sıfırdan satırında rho_T(V-scr) +0,201 [0,146; 0,246] ve sigma farkı -0,284 [-0,308; -0,266]. G için beyan edilen durum A'nın sigma satırı için beyan edilmemiş. Beklenen: bu değerler ve etiketler §1'e ve A tablosunun mevcut değer sütununa eklensin.

3. major, `03_deney_zinciri.md:31` ("Her betik sınandı") ve `experiments/q1_curutme_cka.py`. CKA betiği hiç koşulmamış; `_duman/`, loglar ve `/mnt/d/adeb_sci_1_veri/_duman_curutme` altında CKA çıktısı yok; `q1_ek_gradyan_kosinus.py mantel` adımı CKA özet dosyasıyla sınanmamış. G bloğu B1-09 ve B1-18'den önce koştuğu için bir çalışma hatası zinciri orada durdurur. Beklenen: dondurmadan önce küçük n ile duman koşusu ve ardından `mantel --sinama`.

4. minor, `scripts/curutme_zincir.sh:140-156`. Bekçi yalnız boş belleğe bakıyor; ölçüm anında 20.819 MiB boş, kullanım %94 idi; eşik 20.480 MiB olduğundan zincir hemen paylaşımlı GPU'da başlar ve AT aşamaları tohum sınırına erken takılabilir. Başlatma kararında gözetilmeli ya da bekçiye kullanım koşulu eklenmeli.

5. minor, `ON_KAYIT_EK_CURUTME_2026-11-08.md:28` ve `scripts/curutme_zincir.sh:313`. B3 AT komutu için verilen `logs/konsey_zincir.log:36` temiz komutudur; AT komutu satır 40'tadır.

6. minor, `ON_KAYIT_EK_CURUTME_2026-11-08.md:71` ve `03_deney_zinciri.md:31`. C1 log satır numaraları (105889, 108329, 107196) `splitlines()` sayımıdır (\r satır sonu sayılmış); standart araçlarla 449, 456 ve 455. Değerler (81,90; 83,85; 83,25) doğrudur.

7. minor, `ON_KAYIT_EK_CURUTME_2026-11-08.md:13`. `A_n200/` için "ViT ya da ResNet hücresi içermez" denmesine karşın matriste `Vscrp_duman` adlı ViT hücreleri var; `yeni_tip_n100/` için "yalnız üç duman modeli" denmesine karşın WRN_28_10 da var.

8. minor, `ON_KAYIT_EK_CURUTME_2026-11-08.md:36` ve `_duman/regresyon_ozet.md`. Eski kod "HEAD" diye anılıyor; `KAYNAK_COMMIT.txt` ca2d102'yi gösteriyor, HEAD e5c3374. İki commit arasında cli/ ve src/ altında fark yok; ifade düzeltilmeli.

9. minor, `03_deney_zinciri.md:71`. Kısaltılmış SHA `ce5c2bb8...ef1cda95` baş ve son parça değil; gerçek özet `...cc06ef3f863b` ile bitiyor.

10. minor, `ON_KAYIT_EK_CURUTME_2026-11-08.md:128` ve `03_deney_zinciri.md:57`. G'nin CKA Mantel satırındaki "p < 0,05" ve "|r| < 0,10" koşulları konsey JSON'unda yok (orada "pozitif" ve "sıfıra yakın"); işlemselleştirme olarak beyan edilmeli, "yeni bir eşik koymaz" cümlesi düzeltilmeli.

## Notlar

Tohum başına duvar saati sınırı her yeniden başlatmada sıfırlanıyor (`curutme_zincir.sh:243`, bas_s); başlangıç zamanı bir dosyada tutulursa toplam sınır korunur. A bloğu B4'ün 400 hücresini `--skip-existing` ile yeniden kullanıyor; temiz maskelerin bit düzeyinde aynı olması gerekiyor (`q1_ek_transfer_matrix.py:604`), metalar uyumlu ama duman testinde sınanmadı. `01_ic_gecerlilik.md` B1-18 süresini 0,5 + 2 sa, zincir 1,0 + 1,5 sa bölüyor; toplam aynı; 2,5 sa değeri 191. satırda. Tavan tablosu B pilotunun 2 saatlik beklemesini ve 3600 s zaman aşımını içermiyor. cozumleme_sinama_* ve regresyon_det_*yeni3 dosyaları ilgili düzeltmelerden sonra üretilmiş.

## Doğrulananlar

SHA-256 tablosundaki 21 dosyanın özeti sha256sum ile aynı; beş ağırlık dosyası `sha256sum -c` denetiminden geçti. Dondurulmuş dosyalar `git diff --quiet HEAD` ile değişmemiş; zincir betiği bu yollara yazmıyor. Zincir betiği `bash -n` geçti; blok sırası tasarımla aynı; tohumlar 2401/2402, 2501/2502, 1501/1502; tohum sınırları 18000, 13320, 9000 s (JSON'daki 5,0, 3,7, 2,5 sa); 6300 s konseyin 1,75 sa değeri; kuru koşu betikle tutarlı; önbellek adı adım ve eps içeriyor; b118_ara 22 ara kontrol noktası buluyor. Kod farkında yeni bayraklar verilmezse davranış eski kodla aynı; AugReg normalizasyonu 0,5/0,5, SWSL ImageNet. Regresyonda sekiz çiftin hepsinde 50 satırda sıfır fark (belirlenimli kip ve CPU); belirlenimsiz farklar özet dosyasıyla aynı. Duman: B 114 s, son kayıp 2,2337, doğrulama %26,00; A n=200 temiz 91,50/93,50/93,00, raw_fooling 42,0/39,5/38,0. Föy satırları 1383-1385, 1452-1457, 1463-1468, 1496-1499, 1526-1528, 1606, 1673, 1707, 1713, 1996, 2229-2231, 2236 açıldı ve ön kayıttaki değerlerle aynı. G sınaması -0,029 [-0,045; -0,016] `cozumleme_sinama_G.json`'da var. Süre tablosu: beklenen 20,69, tavan 32,95 GPU-saat.

## Ikinci tur (ayni curutucu, kapanislarin dogrulanmasi)

Karar: gecer. Yuruticunun 11 kapanisi hedefli olarak acildi: epok komutu t'yi son pilot epogunun cubuk suresi + dogrulama payi olarak hesapliyor, baslatma disarida, duman B icin t 70,2 s ve E_temiz 89 (`_duman/duman_epok_sinama.json`); zincir pilot logunu siliyor (:408) ve epok --log ile cagiriyor (:412). On kayit §1 ve A tablosunda cozumleme_sinama_A.json degerleri (rho +0,011 [-0,030; 0,053] esdeger; sigma -0,029 [-0,042; -0,014] negatif, H yanlis bolgesi beyaniyla; ikincil +0,201 ve -0,284) var. G_cka_duman_k4 altinda CKA ve iki Mantel adimi hatasiz; kural_G'nin okudugu alanlar uretiliyor. Minor kapanislar (konsey_zincir.log:40; C1 satirlari 449/456/455; ca2d102 ifadesi; p < 0,05 islemsellestirme beyani; 01_ic_gecerlilik.md:191; _baslangic_epoch.txt) dogrulandi. §16'daki 21 SHA sha256sum -c ile OK (zincir a294816a..., denetim 384cd3f9..., cka e134736f...); dondurulmus dosyalar git diff ile temiz; bash -n gecti; uzun tire ve koyu etiket yok.

Istege bagli notlar: (1) yeniden baslatmadaki kesinti suresi tohum sinirina sayiliyor; on kayit §15'e tek cumle onerildi (yardimci Fable tarafindan eklendi). (2) Duman G Mantel loglarinda konsey_ayrisim.py:244'ten "divide by zero in log" uyarisi; duman modeli zayif oldugu icin zararsiz, gercek kosuda gorulurse incelenmeli. (3) epok komutunun tqdm deseni yalniz 1 epokluk duman logunda sinandi; okunamazsa yedek yontem T/2 (baslatma haric).
