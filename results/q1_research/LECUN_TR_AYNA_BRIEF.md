# TR ayna brifi (LeCun turu, 2026-10-04)

Hedef: `paper/manuscript_tr/` (IEEEtran, Türkçe). Kaynak: bugün yeniden kurulan EN el yazması
`paper/manuscript/` (tek doğru metin). TR, EN'in cümle düzeyinde aynasıdır: aynı bölüm ağacı, aynı
kayan nesneler (tablo/şekil sayısı ve sırası), aynı denklemler, aynı `\cite`/`\ref`/`\label`, aynı
sayılar (TR ondalık virgül `0{,}41`; binlik `10.000`). Ayna kapısı `scripts/check_en_tr_mirror.py` paragraf
sayar (200 karakterden uzun, `\` ile başlamayan satırlar) ve kayan nesneleri eşler.

## Dosya eşlemesi
main.tex ↔ manuscript_tr/main.tex (başlık, özet, veri-kod paragrafı); 01_introduction ↔ 01_giris;
02_related_work ↔ 02_ilgili_calismalar; 03_methodology ↔ 03_yontem; 04_experiments ↔ 04_deneyler;
05_discussion ↔ 05_tartisma; 06_conclusion ↔ 06_sonuc.

## Yapılacaklar (EN'deki değişikliklerin karşılıkları)
1. Başlık ve özet yeniden (başlık Türkçe karşılığı: "Koşullama Kümesi Ölçülen Transfer Asimetrisini
   Belirler: CNN ile Görü Dönüştürücüsü Gürbüzlük Karşılaştırmaları için Kesin Bir Düzeltme ve Eşlenmiş
   Çift Öngörüsü").
2. Giriş: 3. paragraf ("state but rarely vary"), dört katkı paragrafı, olumsuz sonuçlar tek cümle, ATEEC
   paragrafı.
3. İlgili çalışmalar: II-A/II-B kısaltma (iki denklem kalkar), II-F ikinci paragraf.
4. Yöntem: koyu etiketler düzyazıya; tarif adı; TRADES cümlesi; yeni alt başlık + `tab:protocol_masks` +
   `eq:general_identity` + `eq:raw_identity` taşınması; p tanımı ve AT-hedef şerhi; istatistik
   paragrafı son cümlesi; 03:102 "önceki kontrol noktası" paragrafı nitel tek cümle.
5. Deneyler: A kısaltma (77,50 ve veri miktarı cümlesi çıkar); B üç ayrı olgu, karantina "±2 kabul"
   cümlesi çıkar, Tablo 2 alt bloğu ve Tablo 3 ‡ dipnotu çıkar; C yeni alt bölüm + `tab:source_target`
   (table*); D yeni yapı (CIFAR-100 / SVHN "yakın-eşlenmiş" / L2 alt-alt bölümler; D4 kayıtlı uyum,
   +0,470 özdeşliğin dış sınaması, `fig:spread_clean_gap` → `../figures/final_tr/fig_spread_clean_gap.pdf`);
   E yeni alt bölüm + `tab:external_pool`; F yeni alt bölüm (seçim kuralı; H'den iki paragraf taşınır);
   G tek alt bölüm, dikkat metni düzeltmeleri (4,61–5,11; TOST 12/12, p=0,006; devrilen/devrilmeyen
   p=0,20 / 0,080); geometri paragrafı çıkar; H aralık-aralığa dil. Şekil 3 başlığı yeni (ikili
   uzaklıklar, "ayrı ayrı yuvarlanmış" ifadesi düşer).
6. Tartışma: Mahmood kısmi uzlaşma paragrafı; sekiz maddelik gereklilik listesi; tek paragraf
   sınırlılıklar; kısaltılmış gelecek çalışmalar.
7. Sonuç: dört paragraflık sentez.
8. `scripts/verify_manuscript_numbers.py`: `chk_en(...)` satırları `chk(...)`'ye çevrilir (TR'de de
   aranır); `check_pdf_render.py` TR'yi denetlemez.
9. `main.tex` (TR) veri-kod paragrafı EN ile aynı kapsam.

## Üslup (akademik-turkce)
Türk tez/makale dili: -mıştır/-maktadır dengesi doğal, koyu paragraf etiketi yok, uzun tire yok,
madde yalnız gereklilik listesinde, "Bu + ad" bağlantısı serbest, çıplak "Bu," açılışı yok, İngilizce
iskelet yok. Terimler yerleşik: gürbüzlük, çekişmeli, koşullama kümesi, hedef-doğru, her-ikisi-doğru,
başarılı-kaynak, ham oran, özdeşlik, yayılım, kestirim, koşum, öncül p.

## Doğrulama
`cd paper/manuscript_tr && latexmk -pdf -interaction=nonstopmode main.tex` (0 hata, 0 tanımsız);
`bash scripts/kapilar.sh` → "DOKUZ KAPI DA GECTI".
