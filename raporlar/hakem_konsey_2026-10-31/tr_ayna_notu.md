# TR ayna düzeltme turu, 31.10.2026 (tek tur)

Bu not, Türkçe aynanın (`paper/manuscript_tr/`) on yedi bulguluk düzeltme turunun kaydıdır. EN dosyalarına, `references.bib` dosyasına, `results/` klasörüne ve föye dokunulmamıştır.

## Eşitlemenin dayandığı EN durumu

EN tur sırasında da değişmeye devam etti: 01 19:08:46'da, 03 19:10:23'te, 05 19:10:18'de, 04 19:15:02'de, 07 19:12:41'de değişti. TR, EN'nin 19:15:02'deki son durumuna eşitlendi. 19:15 ile 19:20:56 arasında EN'de yeni bir değişiklik olmadı. Eşitlemenin dayandığı EN kopyası `raporlar/hakem_konsey_2026-10-31/tr_ayna_en_taban/` klasöründe duruyor (9 dosya, 19:20:56'da alındı).

Bu tur sırasında EN'de görülen ve bulgu listesinde yer almayan değişiklikler de TR'ye işlendi:

- 04 açılış paragrafı kısaltıldı ("Cell names follow ..." cümlesi çıktı).
- CIFAR-100 paragrafının son cümlesi çıktı.
- "One feature of CIFAR-100 ..." cümlesi "On CIFAR-100, ..." biçiminde sadeleşti.
- "Across the runs of Table cells" yapısına geçildi.
- A10 cümlesi "exploratory three-member panel" biçimini aldı.
- Köprü cümlesi "This bridge, not the σ gap seen before registration, is what H1 tests" oldu.
- ImageNetV2 gözlem cümlesi "descriptively" ile yeniden kuruldu.
- 05'teki Welch cümlesi "still place H1 and H2 away from zero" biçimini aldı.
- 05'teki panel bileşimi cümlesi değişti.
- 05'teki gelecek çalışma cümlesinde maliyet parantezi kullanıldı.
- 07'deki TGR cümlesi tek cümleye indi.
- 01'deki yol haritası paragrafı çıktı. TR'de de çıkarıldı, böylece paragraf sayısı 12'den 11'e indi.

Önceki bütünleştiricinin eşitlemesinden bu yana EN'den çıkarılan ama TR'de kalan cümleler de silindi. Silinenler şunlar: 03'teki "kaynak ve hedef rolleri ancak panelle tanımlanabilir" cümlesi, 03'teki gradyan bölümünde fazladan kalan "mekanizma kanıtı değil" cümlesi, 04'teki WRN ve 0,531 cümleleri, 04'teki havuz jackknife parantezi (0,919 ile 0,935), 04'teki TGR uyarlama cümlesi, 04'teki Zhang atfı ve "simetrik terim böylece ..." cümlesi, 04'teki δ = 0,06 cümlesi, 05'teki Caussinus kapanışı ve 07'deki χ² sayıları (0,8 ile 9,9 ve 5,2 ile 32,6). Bunların yanında altyazılardaki EN'de bulunmayan yorum cümleleri de çıkarıldı. Bu altyazılar fig:source_gap_split, fig:cells_interaction, fig:attack_side, fig:estimates_forest ve tab:imagenet'e aittir.

## Bulgular: kabul ve ret

Bulguların 16'sı tam olarak kabul edilip düzeltildi. Bulgu 17 kısmen karşılandı. Reddedilen bulgu yoktur.

| No | Konu | Karar | Yapılan |
|---|---|---|---|
| 1 | Kök neden: EN hareket ediyor | Kabul | EN 19:15:02 durumuna eşitlendi. Taban kopya saklandı. EN'nin dondurulması TR yazarının yetkisinde değil, orkestra işidir (aşağıdaki delta talimatına bakınız). |
| 2 | Başlık niceleme | Kabul | "Zayıf Olmaktan Çok, Farklı Bir Kaynak: Mimari × Başlatma Tasarımıyla CNN-ViT Çekişmeli Transferinde Kırılganlık, Benzerlik ve Yön" yapıldı. main.tex gerekçe yorumu güncellendi. |
| 3 | ⟨·⟩_P altyazısı | Kabul | `fig_decomposition_schematic.py:157,162` ve EN 03:162 ile doğrulandı. |
| 4 | McNemar sınırları | Kabul | `p ≤ 1,2×10⁻⁸⁴` ve `p ≤ 1,9×10⁻¹²⁰` yazıldı (föy 43-45). |
| 5 | σ(V-IN) − σ(R224-IN) | Kabul | −0,104; birleştirilmiş [−0,159; −0,049]; Welch [−0,318; +0,109]; "yalnız birleştirilmiş varyanslar altında" kaydı ve Ek~app:exploratory göndermesi eklendi. FOY:M12.1:2229,2246 konuldu. |
| 6 | ρ basit etkileri | Kabul | +0,070, −0,064, −0,134 ve Tablo~tab:simple_effects göndermesi eklendi. FOY:M12.1 ve YON satırı konuldu. Tablo 07_ek.tex'e aynı etiketle eklendi. |
| 7 | A10 keşifsel panel | Kabul | 04'e cümle (EN'nin son biçimiyle, "üç üyeli keşifsel panel") ve 05'e sınırlılık cümlesi eklendi. tab:reduced_panel 07'ye kondu. FOY:M12.3 eklendi. |
| 8 | 2q − 1 | Kabul | K-a paragrafına cümle (0,873 [0,849; 0,896]) ve tab:panel_tests'e "türetilmiş" satırı (CIFAR-100 0,679 [0,589; 0,769]) eklendi. Dipnot EN'ye eşitlendi. FOY:M12.2:2290 ve 2290,2291 konuldu. |
| 9 | Çıkarılmış içerik | Kabul | 03'teki Gowal cümlesi ve 04'teki 0,531 cümlesi silindi. Bulgudaki "WRN referansı 04:57'de duruyor" kısmı artık geçerli değil, çünkü EN o cümleyi de çıkarmıştır. TR'de de çıkarıldı. WRN tab:main_results dipnotunda ve 05'te duruyor. |
| 10 | "İki faktörlü" | Kabul | tab:registry satırı `$2\times2$, CIFAR-10` yapıldı. |
| 11 | "ek kaydın" | Kabul | "ön kayıt ekinin" yapıldı. |
| 12 | "gövde" (stem) | Kabul | 01 "yama girişini", 02 "evrişimli bir giriş katmanının", 04 "evrişimli girişli bir ViT" yapıldı. |
| 13 | "havuzlanmış" | Kabul | 04'te üç yer ve köprü cümlesi "birleştirilmiş varyans" yapıldı. Tablo dipnotunda "Birleştirilmiş SS" kullanıldı. |
| 14 | matched/unpaired | Kabul | Tabloda "eşi yok" yazıldı. Metindeki "eşleştirilmiş karşılaştırma" cümlesi, EN'den çıkarıldığı için silindi. |
| 15 | Özette "karışmaktadır" | Kabul | "... temiz doğruluğundan ayrıştırılamamaktadır" yapıldı. Özet 242 sözcüktür. |
| 16 | 02:53 bozuk cümle | Kabul | Önerilen iki cümlelik biçim kullanıldı. |
| 17 | Kip ve çatı dengesi | Kısmen | 04'te ölçüm sonucu bildiren 24 yüklem "-mıştır" yapıldı ("ölçülmüştür", "hesaplanmıştır", "bulunmuştur", "çıkmıştır" dönüşümlü kullanıldı). 05'te 5 yüklem değiştirildi; bunların ikisi edilgen yapıldı. 05:84 "sınayabilecektir" oldu. `degismez.py` iki dosyada da "KORUNDU" verdi. |

Bulgu 17'den kalan sapmalar şunlar. 04'te -mıştır payı artık bant içinde (önce 33,8 idi). 04'te -dır payı 17,1 (bant ≤14,2), edilgen pay %23,8 (bant 57-87). 05'te -mıştır payı 35,4 (bant 41,8-80,5), -maktadır payı 41,8 (bant ≤38,7). Tartışmadaki yorum yüklemleri ("açıklamaktadır", "işaret etmektedir") kipi korunarak bırakıldı. Bunları -mıştır'a çevirmek, iddiayı kesin geçmiş bulguya dönüştürüp kipi değiştirirdi. Kesin ihlal hiçbir dosyada yoktur.

## Biçim kararları

Karar: tab:panel_tests'te `\tabcolsep` değeri TR'de 1,6pt bırakıldı (EN'de 2,2pt), çünkü 2,2pt Türkçe etiketlerle 5,5pt'lik bir Overfull \hbox üretiyordu. İçerik değişmedi.

Karar: fig:protocol_sets EN gibi `../figures/konsey/fig_protocol_sets.pdf` (v5) dosyasına bağlandı ve altyazıya bağlayıcı cümlesi eklendi, çünkü eski `final_tr` sürümü v5 bağlayıcılarını taşımıyordu. Şekilde İngilizce etiketler var. Türkçe v5 varyantı istenirse figür hattında üretilmesi gerekir.

Karar: tab:simple_effects'te EN'nin "Arch./Init." kısaltmaları yerine "Mimari/Başlatma" tam sözcükleri kullanıldı. Tablo taşmadan sığıyor.

Hâlâ duran biçim uyarısı: 14. sayfadaki yalnız kayan nesne içeren sayfada 3,7pt'lik bir Overfull \vbox vardır. Bu uyarı içerikten değil, kayan nesne yerleşiminden kaynaklanıyor.

## Kapılar (19:20, düzeltmelerden sonra)

- TR derleme: `latexmk -pdf` çıkış kodu 0, 26 sayfa, hata 0, tanımsız gönderme 0, Overfull 1 (yukarıdaki \vbox).
- `check_en_tr_mirror.py`: GEÇTİ. Sekiz bölüm çiftinin hepsinde alt bölüm, tablo, şekil, denklem ve paragraf sayıları eşit. 07 çifti: 5 tablo, 2 şekil, 10 paragraf.
- `q1_tr_decimal_check.py`: TEMİZ. İki `$[0,1]$` aralık gösterimi istisna olarak listelendi.
- `check_abstract_body.py`: GEÇTİ. TR özetinde 20 sayı var ve hepsi gövdede bulunuyor. EN özeti 249, TR özeti 242 sözcük.
- Sayı, etiket ve FOY karşılaştırması (oturum betiği): bütün bölümlerde yalnız EN'de ya da yalnız TR'de bulunan sayı kalmadı. Kalan farklar, `$2\times2$` gösteriminden gelen "2" sayıları ile TR'de `[0,1]` normalizasyonundan gelen yapay "0.1" farkıdır. Etiket ve atıf farkı yoktur. FOY ve KAYNAK yorumları 03, 04 ve 07'de EN'deki yerlerine kopyalandı.
- `tara.py --tur makale --bolum oto`: sekiz dosyada kesin ihlal 0. Norm sapmaları 01'de 1, 02'de 2, 03'te 2, 04'te 3, 04z'de 11 (217 sözcüklük kısa dosya), 05'te 3, 06'da 0 ve 07'de 4.

Sözcük sayısı: gövde düzyazısı yaklaşık 11.335 sözcüktür (tara.py sayımı). Dosyalara dağılımı şöyle: 01 1103, 02 1005, 03 2863, 04 3548, 04z 217, 05 1437, 06 298, 07 864.

## TERMINOLOJI.md eklemeleri

TERMINOLOJI.md'ye "31.10.2026 TR düzeltme turu eklemeleri" başlıklı bir bölüm eklendi. Eklenen terimler şunlar: basit etki, türetilmiş nicelik, ResNet-18 türevi, birleştirilmiş varyanslı aralık ("Birl.\ \%90 GA"; "havuzlanmış" kullanılmaz), "confounded with" karşılığı ("ayrıştırılamamak / karıştırıcı etken"; "ile karışmak" kullanılmaz), eşi yok, bağlayıcı (şekil), "crosses A with B" karşılığı (mimari × başlatma için "çaprazlayan" kullanılmaz) ve başlık karşılığı. Görevde listelenen öteki terimler (w, τ̄, r, σ, ρ, ω, bölünmüş yarı, mimari × başlatma, panel, ön kayıt, Holm, TOST, Mantel, girdi gradyanı kosinüsü, betimsel, keşifsel, çürütüldü, eşdeğerlik) listede zaten vardı. Metin bu karşılıklarla tutarlıdır.

## Delta geçişi talimatı (EN yeniden değişirse)

1. Değişen EN yerlerini bulmak için WSL'de depo kökünde şu komut çalıştırılır: `diff -r raporlar/hakem_konsey_2026-10-31/tr_ayna_en_taban paper/manuscript/sections` (main.tex için `diff raporlar/hakem_konsey_2026-10-31/tr_ayna_en_taban/main.tex paper/manuscript/main.tex`).
2. Değişen her EN paragrafının TR karşılığı aynı sırada bulunur. Ayna kapısı paragraf sırasını eşlediği için EN'deki n'inci uzun paragraf TR'deki n'inci uzun paragraftır. Anlam, sayı, atıf ve dürüstlük kaydı TR'ye yeniden yazılır. Sayılar ondalık virgülle ve matematik kipinde `{,}` ile yazılır. EN'de eklenen ya da değişen `% FOY:` ve `% KAYNAK:` satırları TR'de aynı yere kopyalanır.
3. Yeni tablo ya da şekil eklenmişse TR'ye aynı `\label` ile, Türkçe altyazıyla ve aynı PDF yoluyla eklenir. Terimler TERMINOLOJI.md'den alınır.
4. Sırasıyla şunlar koşulur: TR derleme (`cd paper/manuscript_tr && latexmk -pdf main.tex`), sonra `docker exec -w /workspace adeb_eval python scripts/check_en_tr_mirror.py`, `scripts/q1_tr_decimal_check.py` ve `scripts/check_abstract_body.py`. Ardından değişen dosyalarda `tara.py --tur makale --bolum oto` ve `degismez.py eski yeni` koşulur.
5. İş bitince taban kopya yenilenir: `cp -p paper/manuscript/sections/*.tex paper/manuscript/main.tex raporlar/hakem_konsey_2026-10-31/tr_ayna_en_taban/`.
