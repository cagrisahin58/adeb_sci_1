# TR Dizin Dergi Seçimi (Karar: 2026-08-03)

## Karar: Bilişim Teknolojileri Dergisi (Gazi Üniversitesi) — birincil hedef

**Gerekçe:**
1. **Kapsam birebir uyumlu.** Dergi, bilişim güvenliği + yapay zeka kesişiminde
   yayın yapıyor ve çekişmeli saldırı / derin öğrenme güvenliği literatürüne
   aşina bir hakem havuzu var (yayın kurulunda derin öğrenme ve bilgi
   güvenliği uzmanları mevcut). Makalemiz tam bu kesişimde bir ölçüm-metodolojisi
   çalışması.
2. **TR Dizin'de köklü.** ISSN 2147-0715, TR Dizin dergi kaydı mevcut
   (dergi no 928). Üç ayda bir, açık erişim, ücretsiz.
3. **Dil.** Türkçe ve İngilizce makale kabul ediyor; Türkçe sürümümüz doğrudan
   gönderilebilir.
4. **Pratik.** DergiPark üzerinden gönderim; APC yok.

- Dergi sayfası: https://dergipark.org.tr/tr/pub/gazibtd
- TR Dizin kaydı: https://search.trdizin.gov.tr/en/dergi/detay/928

## Yedek: Zeki Sistemler Teori ve Uygulamaları Dergisi (JISTA)

Yapay zeka odaklı, Türkçe/İngilizce, TR Dizin; ret hâlinde ilk alternatif.
https://dergipark.org.tr/tr/pub/jista

## Değerlendirilen diğer adaylar

| Dergi | Durum | Neden birincil değil |
|---|---|---|
| Gazi Üniv. MMF Dergisi | SCI-E'de de taranıyor | Genel mühendislik; niş metodoloji makalesi için kapsam geniş, süreç uzun. Q1 genişletmesi ayrı planlandığı için bu metni buraya harcamak verimsiz. |
| Mühendislik Bilimleri ve Tasarım (JESD) | TR Dizin | Genel mühendislik/tasarım; güvenlik hakem havuzu zayıf. |
| KSÜ Mühendislik Bilimleri | TR Dizin | Daha düşük görünürlük. |

## Gönderim öncesi yapılacaklar (kullanıcı + Claude)

1. [ ] Derginin güncel yazım şablonunu DergiPark sayfasından indir
   (çoğunlukla Word şablonu; `manuscript_tr/` LaTeX taslağından aktarım
   gerekecek — metin birebir kopyalanır, tablolar yeniden kurulur).
2. [ ] Dergi "Öz + Abstract" ikilisini ister: Türkçe Öz hazır (main.tex);
   İngilizce Abstract, İngilizce makaledekiyle aynı (250 kelime).
3. [ ] Genişletilmiş bildiri beyanı: ATEEC 2026 bildirisi kabul edilirse
   "bu çalışmanın ön sonuçları ... sunulmuştur" dipnotu eklenecek
   (TR Dizin dergileri genişletme oranı şartı arayabilir; C1-C5 deneyleri
   ve yeni çerçeve %70+ yeni içerik sağlıyor, sorun beklenmiyor).
4. [ ] Kod erişilebilirlik cümlesi: repo kararı verilince URL eklenecek.
5. [ ] iThenticate/intihal raporu (dergi isterse; üniversite üzerinden).

## Notlar

- Türkçe taslak: `paper/manuscript_tr/` (IEEEtran, 15 sayfa, 0 hata).
  Bu bir **çalışma formatıdır**; dergi şablonuna aktarım gönderimde yapılır.
- Türkçe figürler: `paper/figures/final_tr/` (üretici:
  `scripts/generate_journal_figs_c1.py --lang tr`).
- Terminoloji: `paper/manuscript_tr/TERMINOLOJI.md`.
