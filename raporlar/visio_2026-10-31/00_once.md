# Önce kaydı: visio-cizici işi, 31.10.2026

Bu kayıt, IEEE Access makalesinin şekillerini visio-cizici skill'iyle yeniden çizme işine başlamadan önceki durumu tutar. Kaydı görsel üretici ajan almıştır; ölçümler WSL (Ubuntu-22.04) içinde ve Windows Python ile, depo kökü `/home/firat/projects/adeb_sci_1` üzerinde yapılmıştır. Bu fazda hiçbir `.tex` dosyası, hiçbir orijinal şekil ve hiçbir veri dosyası değiştirilmemiştir.

## 1. Depo durumu

Dal `q1`, HEAD `b4a3ac47e125446f1fa5c915c0bfcb798f554c73`. Son üç commit (`git log -3`, tarih ISO):

| Commit | Tarih | Konu |
| --- | --- | --- |
| b4a3ac4 | 2026-10-31 19:24:36 +0300 | Makale TR aynası EN ile eşitlendi: yeni başlık, 2x2 ve ayrışım bölümleri, Ek D, hesaplama ayrıntıları; ayna/ondalık/özet kapıları geçti |
| 2f63cd2 | 2026-10-31 19:18:28 +0300 | Makale EN: hakem paneli düzeltmeleri, başlık "Less a Weak Source than a Different One", M11-M12 masa çözümlemeleri, atıf doğrulama, sayı kapısı yeniden tasarımı (EN_EKSIK 0) |
| 52364bc | 2026-10-31 17:16:57 +0300 | Makale EN yeniden yazımı (konsey manşetine göre): yeni başlık, 2x2 ve w-tau-r ayrışımı, B2-B10 tabloları, 7 yeni şekil taslağı, ek bölümü, hesaplama ayrıntıları |

`git status --short` çıktısının tamamı `00_once_git_status.txt` dosyasındadır (296 satır, kaydın alındığı an). İzlenen ve değişmiş dosya sayısı ölçüm sırasında 14'ten 15'e çıkmıştır; başka ajanlar aynı anda metin ve gönderim dosyaları üzerinde çalışmaktadır. Kayıt anında izlenen değişmiş dosyalar `paper/manuscript_tr/main.pdf`, `paper/manuscript_tr/sections/04_deneyler.tex`, `05_tartisma.tex`, `07_ek.tex`, `paper/submission/` altındaki altı dosya ve `scripts/` altındaki dört gönderim ve bildiri betiğidir. Bu fazın yazdığı dosyalar yalnız izlenmeyen yeni dosyalardır (bölüm 5).

Bu faz sürerken başka bir oturum 19:40:20'de `e8bfc45` commit'ini attı ("TR iddia kapısı 45/45 ...; gönderim paketi yeni başlığa göre"). Commit yukarıdaki izlenen değişikliklerin hepsini içerir (TR'de üç bölümde birkaç satırlık düzeltme, gönderim dosyaları, TR PDF ve kapak mektubu PDF'i) ve sonrasında izlenen değişmiş dosya kalmamıştır. Şekil etiketlerinin kaynak satırları commit'ten sonra yeniden denetlenmiş ve aynı bulunmuştur; EN ve TR sayfa sayıları yine 25 ve 26'dır. İşin sonundaki "sonra" karşılaştırması bu yüzden `b4a3ac4` ile değil, işin başladığı andaki bu iki durumla birlikte okunmalıdır. Korunan 22 veri dosyasının özeti bu fazın sonunda `sha256sum -c` ile yeniden denetlenmiş ve hepsi OK çıkmıştır.

## 2. Derlenmiş belgelerin sayfa sayıları

Sayım `pypdf` 6.9.2 ile WSL'de yapılmıştır (`pdfinfo` WSL'de kurulu değil).

| Belge | Sayfa | Dosya zamanı |
| --- | --- | --- |
| `paper/manuscript/main.pdf` (EN, ieeeaccess.cls) | 25 | 2026-10-31 19:15:12 |
| `paper/manuscript_tr/main.pdf` (TR aynası, IEEEtran taslağı) | 26 | 2026-10-31 19:25:50 |
| `paper/submission/cover_letter.pdf` | 3 | 2026-10-31 19:28:45 |

Kapak mektubu PDF'i kapı koşusu sırasında (19:27-19:28) başka bir oturumca yeniden derlenmiştir; sonraki karşılaştırmada bu zaman damgası göz önünde tutulmalıdır. `paper/supplementary/` altında derlenmiş PDF yoktur. Derlenmiş `main.aux` dosyalarına göre EN ve TR'de 12 şekil (şekil 11 ve 12 ekte) ve 18 tablo vardır; şekil etiketlerinin numaraları iki dilde aynıdır.

## 3. Gönderim kapısı

Komut WSL'de oturum açma kabuğuyla (`bash -lc`, profil okunur; tuzak T1) koşulmuştur: `cd /home/firat/projects/adeb_sci_1 && bash scripts/kapilar.sh`. Kapılar `adeb_eval` kapsayıcısında koşar; kapsayıcı 12 saattir ayaktadır. Başlangıç 19:27:28, bitiş 19:28:23 (+03:00).

| Kapı | Sonuç | İlk sonuç satırı (kısaltılmış) |
| --- | --- | --- |
| öz-sınama | GECTI | kapı 19 sınamanın 84 bozmasının hepsini yakaladı |
| sayılar | GECTI | FÖY atıfları bloklarında, bloklardaki sayılar işaretle |
| iddialar | GECTI | (boş sonuç satırı) |
| özet | GECTI | özdeki her sayının gövdede karşılığı var |
| TR ondalık | GECTI | matematik kipinde çıplak ondalık virgül yok |
| bildiri | GECTI | bildirinin taşıyıcı sayıları artefaktlarla sayısal olarak tutuyor |
| EN/TR ayna | GECTI | iki sürümün bölüm ağacı, kayan nesneleri, denklemleri tutuyor |
| gönderim | GECTI | gönderim malzemeleri makaleyle ve artefaktlarla tutuyor |
| PDF render | GECTI | PDF (25 sayfa) özet, anahtar kelime, başlık, yazar bandı |
| PDF dizgi | GECTI | kalın/italik Times gömülü, sütun taşması yok |

Son satır "OZ-SINAMA VE DOKUZ KAPI GECTI", çıkış 0. Beklenen denetim sayısı 10'dur (öz-sınama ve dokuz kapı) ve 10 GECTI satırı okunmuştur. Bu kapının "PASS n FAIL 0" biçiminde bir satırı yoktur; karar satır satır GECTI ve son toplam satırıyla verilmiştir.

## 4. Korunacak veri dosyalarının SHA-256'ları

22 dosyanın özeti `00_once_sha.txt` dosyasındadır (`sha256sum` çıktısı, WSL). Kapsam: `results/C1_REFERANS_FOYU.md`; `results/q1/konsey_ayrisim_b2.json`, `_b4.json`, `_b5.json`; `results/q1/konsey_b6_maskeleme.json`; `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json`; `results/q1/konsey_b8_imagenetv2/b8_betimsel.json`; `results/q1/konsey_b10_gradyan/` üst düzeyindeki dört JSON (`b10_aile.json`, üç `mantel_*.json`); `results/q1/konsey_ek_masa/` altındaki on bir JSON. Föyün bugünkü özeti `00cc422f01c0d964...`'tür. İşin sonunda aynı komut yeniden koşulur ve iki liste satır satır karşılaştırılır (bitiş ölçütü 12).

Konsey şekillerinin kanıt dosyalarındaki föy özeti bugünkünden farklıdır (sekiz dosyada `42c7dc34...`, `fig_study_overview`'da `57e9659e...`). Föy bu şekiller üretildikten sonra M11-M12 bölümleriyle büyümüştür. Şekillerin veri JSON'ları ise kayıtlı özetleriyle bugün de aynıdır (bkz. `01_envanter.md` bölüm 3); yeniden çizimde her sayı föyle yeniden karşılaştırılır.

## 5. Bu fazda yazılan dosyalar

`raporlar/visio_2026-10-31/` altına `00_once.md`, `00_once_sha.txt`, `00_once_git_status.txt`, `venue_probe_ieee_access.json`, `venue_ieee_access_blok.txt`, `kopya_yap.py` (probe kopyasını yazan betik) ve `01_envanter.md`; `paper/figures/` altına `visio_cizici.yaml`, `panel_yapisi.yaml` ve `qc/` içine düz okuma kopyaları (`main_en_duz.tex`, `main_tr_duz.tex`, harita JSON'ları) ile panel atıf sayımları (`panel_atiflari_en.*`, `panel_atiflari_tr.*`). `paper/figures/visio/`, `charts/`, `onizleme/` ve `visio_loglari/` klasörleri boş olarak açılmıştır.
