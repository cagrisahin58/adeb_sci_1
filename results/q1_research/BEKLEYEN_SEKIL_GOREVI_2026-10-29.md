# Bekleyen şekil görevi (kullanıcı, 29.10.2026)

Durum: TAMAMLANDI (01.11.2026; visio-cizici Faz A-C, commit'ler 302d56c, 118e769, 5851c86; raporlar `raporlar/visio_2026-10-31/`; TR dilli şekiller ikinci tura kaldı, bkz. `HANDOFF_2026-10-31.md`). Eski durum satırı tarih kaydı olarak korunmuştur: BEKLİYOR. Kullanıcının koşulu: "deney planlarsan bunlar bittikten sonra yaparsın, bunu kaydet ama". 29.10.2026'da konsey yeni deneyler planladığı için bu görev, o deneylerin sonuçları makaleye işlendikten sonra başlatılır.

Engel: Görev metni "/visio-cizici skill'ini yükle; skill yoksa ya da eksikse dur ve bunu söyle; skill'i kendi başına yeniden yazma" diyor. 29.10.2026 taramasında bu skill bulunamadı. Taranan yerler: C:/Users/cagri/.claude/skills, WSL ~/.claude/skills, C:/Users/cagri/projects/cc_duzen/skills, synced klasörleri ve eklentiler. Microsoft Visio kurulu görünüyor (AppData/Local/Microsoft/Visio var). Görev, skill kullanıcı tarafından kurulduktan sonra başlatılabilir.

Doldurulacak yer tutucular (görev başlatılırken): Depo /home/firat/projects/adeb_sci_1; ana dosya paper/manuscript/main.tex (TR aynası paper/manuscript_tr/main.tex); hedef dergi IEEE Access (ieeeaccess.cls, tek sütun 3,5 in, çift sütun 7,16 in); şekil kaynakları paper/figures/ (final/, final_tr/, overview/ TikZ, çizim betikleri paper/figures/*.py ve scripts/fig_*.py, kanıt dosyaları *.kanit.json).

## Kullanıcının görev metni (aynen)

GÖREV: visio-cizici skill'iyle bir makalenin şekillerini dönüştür.

  Önce /visio-cizici skill'ini yükle ve onun iş akışını uygula. Skill yoksa ya da eksikse dur ve bunu söyle; skill'i kendi başına yeniden yazma.

  Makale:
  - Depo: [MAKALE DEPOSUNUN MUTLAK YOLU]
  - Ana dosya: [örn. paper/main.tex ya da manuscript.docx]
  - Hedef dergi: [DERGİ ADI; sütun genişlikleri ve şekil kuralları dergi yönergesinden alınır]
  - Şekillerin şu anki kaynakları: [şekil klasörü, varsa çizim betikleri ve veri dosyaları]

  Ne istiyorum:
  1. Orijinal şekillere dokunma; yeniler ayrı klasöre çizilir (örn. figures/visio/ ve figures/charts/), metne yalnız kontrol geçmiş sürüm kurulur.
  2. Envanter: her şeklin türü (şematik, veri grafiği, görüntü paneli), taşıdığı iddia, veri kaynağı. Metinde görselleştirilebilecek ama şekli olmayan yerleri de listele (yöntem akışı, çalışma tasarımı, kohort akışı, uzun tablolar), her biri için yeni şekil öner.
  3. Üslup: skill'in protokolüyle makaleye en uygun üslubu seç, gerekçesini yaz, iki alternatifin önizlemesini üret ve işi durdurmadan devam et. Son mesajda "beğenmezsen 'üslup N' yaz" seçeneğini ver.
  4. Şematikler Visio'da milimetrik motorla; veri grafikleri skill'in kart sistemiyle. Her şekil çizim anında ve basılı PDF'te milimetrik kontrolcüden PASS almadan dosyaya yazılmaz; QC puanı en az 90, bloklayıcı yok.
  5. Her çizilen sayı bir dosyadan okunur (veri dosyası, tablo, çıktı kaydı). Veri dosyası olmayan bir grafik için sayıları eski şeklin pikselinden tahmin etme; o şekli "veri gerekli" diye listele ve gereken dosyayı yaz.
  6. Altyazılar dergi sınırına uyar, kalın giriş cümlesi taşır, her panel harfini anar; değişen altyazıları metne işle.
  7. Makaleyi yeni şekillerle sıfırdan derle; tanımsız atıf ve taşma olmasın; sayfa sayısını önce ve sonra raporla.
  8. Depo kurallarına uy (CLAUDE.md: commit biçimi, hangi dosyaların dışarıda kalacağı); işi commit et ve dalına push et. Zorla push yok.

  İş bölümü: fable-orkestra protokolü; şematikler tek Visio ajanında (başka bir Visio işi sürüyorsa bekler), veri grafikleri ayrı ajanda, her teslimata çelişik opus doğrulayıcı, altyazı ve derleme ayrı ajanda. Son mesajda: seçilen üslup ve gerekçesi, önizlemelerin mutlak yolları, şekil başına controller ve QC sonucu, eklenen yeni şekiller, veri bekleyen şekiller, "Senden beklenen" satırı.
  Bunlara ek olarak bazı yazı içeriklerini de görselleştirebiliyorsak görselleştirelim lütfen. Görsel sayısını arttırıp içeriği azaltalım. Tasarım dili olarak profesyonel makalelerden içerikler çekerek üslup kopyalamayı unutma. kafana göre basit çizimler yapma, ya da halihazırdaki makaledeki görsellere benzetmeye çalışma.
