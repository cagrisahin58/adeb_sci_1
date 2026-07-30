# Bildiri Temizlik ve Denetim Prompt'u (yeniden kullanılabilir)

> Başka bir Claude Code oturumuna olduğu gibi yapıştır; köşeli parantezli alanları doldur.

---

Akademik bir bildirinin son temizlik ve denetim turunu yürüteceksin. Bildiri: `[TEX_DOSYA_YOLU]` (kaynakça: `[BIB_DOSYA_YOLU]`, dil: `[TR/EN]`, sayfa limiti: `[N]`). Sayıları, bulguları ve iddiaları DEĞİŞTİRME; yalnızca dil, biçim ve doğruluk denetimi yap. İş bitiminde derleme temiz olmalı (0 undefined referans, 0 overfull, sayfa limiti içinde) ve değişiklikler tek commit'te toplanmalı (push etme, kullanıcı onayına sun).

## 1. Yapay zekâ kalıntısı üslup temizliği (kendin yap)
- Uzun tire (em-dash: `---` veya `—`) kullanımını TAMAMEN kaldır: cümleyi böl, virgül, iki nokta veya parantez kullan. Akademik Türkçe/İngilizce metinde retorik uzun tire, yapay zekâ yazımının en bilinen izidir.
- Kısa çizgili geçici bileşikleri azalt ("erken-düşüş", "ölçek-değişmez" gibi): doğal dile aç ("erken düşüş", "ölçekten bağımsız"). İstisnalar: yerleşik teknik terimler, tanımlı protokol/metrik adları (ilk geçtiği yerde tanımlanmışsa) ve sayı aralıkları (`10--11` meşrudur).
- Diğer kalıp izleri: "İlk olarak/İkinci olarak/Üçüncü olarak" zincirlerini varyasyonla kır; art arda aynı sözcükle başlayan cümleleri değiştir; 40+ kelimelik cümleleri böl; İngilizceden birebir çeviri kokan yapıları doğallaştır; boş vurgu kalıplarını ("önemle belirtmek gerekir ki", "dikkat çekici biçimde") kaldır.
- Figür/tablo caption'larını 1-2 cümleye indir: caption yalnızca ne gösterildiğini söyler; yorum, seçim ölçütü ve teknik detay gövde metnine taşınır (gövdede yoksa ekle, bilgi kaybetme).

## 2. Atıf denetimi (subagent'a ver — web erişimli)
Subagent'a şu görevi ver: tex + bib dosyalarını okusun ve üç denetim yürütsün:
- **İddia-kaynak uyumu (halüsinasyon):** her `\cite` için iliştirildiği cümledeki iddiayı çıkar; kaynağın gerçekten bunu söyleyip söylemediğini değerlendir (bilinen klasiklerde kendi bilgisiyle, emin olamadığında WebSearch/WebFetch teyidiyle). Yanlış yönde/anlamda kullanım bulgudur.
- **Künye doğruluğu:** bib girdilerinin yazar/yıl/başlık/venue/cilt/sayfa/DOI alanlarını web ile kontrol et; arXiv diye verilmiş ama hakemli venue'da yayımlanmış işleri, yazar adı hatalarını, eksik zorunlu alanları raporla (doğru künyeyi tam ver).
- **Tutarlılık:** atıfsız kalmış güçlü iddialar; metinde hiç `\cite` edilmeyen ölü bib girdileri.
Rapor: [önem] + konum + sorun + önerilen düzeltme.

## 3. Üslup denetimi (1. adımdan SONRA ikinci subagent'a ver)
Subagent temizlenmiş metni okusun: dilbilgisi/yazım, terminoloji tutarlılığı (aynı kavrama tek karşılık; teknik terimlerin ilk kullanımda `[EN karşılığı]` verilmesi), anlatım akışı, gereksiz tekrar (aynı sayının üçten fazla yerde geçmesi), tablo/figür-metin uyumu, bölüm dengesi. Kalan yapay zekâ izlerini de işaretlesin (1. maddedeki listeyle).

## 4. Uygulama ve doğrulama
- İki subagent'ın bulgularını değerlendir: haklı olanları uygula, katılmadıklarını gerekçesiyle listele (körü körüne uygulama).
- Derle; sayfa sayısını ve limitini raporla; figürlerdeki metinlerin bildiri diliyle aynı dilde olduğunu kontrol et.
- Bitiş raporu: yapılan değişiklik kategorileri + uygulanan/reddedilen bulgu sayıları + derleme çıktısı. Commit mesajını hazırla, kullanıcı onayına sun.

## Kurallar
- Bilimsel içerik dokunulmazdır: sayı, bulgu, iddia gücü (hedge düzeyi) değişmez; yalnızca dil/biçim/doğruluk.
- Kaynakça düzeltmelerinde her yeni künye web-teyitli olmalı; teyitsiz künye yazma.
- Şüpheye düştüğün her içerik kararını (ör. bir iddianın yumuşatılması gerekip gerekmediği) uygulamadan kullanıcıya listele.
