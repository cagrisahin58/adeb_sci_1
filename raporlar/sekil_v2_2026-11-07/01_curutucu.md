# Kol C, Faz 1 çürütücü raporu (opus-curutucu, 08.11.2026, birinci tur)

Verdict: duzeltilmeli.

Sayılar ve kapı kayıtları doğru, karantina ihlali bulunmadı. Teslimat yine de kullanıcının ölçütünü karşılamıyor. Üç önizlemeden yalnız pv_b gerçek bir 3B modelleme, o da derin öğrenme makalelerinde sık görülen bir kalıp. Renk tarafında ViT ile ResNet hâlâ turuncu ile mavinin zıtlığıyla ayrılıyor; Üslup Z'nin kendi "yapılmaz" listesi bunu yasaklıyor. pv_c'de ise gri baskıda köşegen ölçülen hücrelerle karışıyor.

## Doğrulananlar

Palet: OKLCH değerleri bağımsız betikle yeniden hesaplandı. En yüksek kroma isi_5'te 0.08539. Gruplar içinde en küçük L farkı vurguda 0.08429, ısıda 0.08417, gövdede 0.08439; yürütücünün iddiası doğru. Saf RGB yok. Piksel ölçümüne göre renkli piksellerin pv_a'da yüzde 22'si, pv_b'de yüzde 42'si, pv_c'de hiçbiri mavi.

İşaret dosyası: _ISARET.json'daki 26 SHA'nın 26'sı dosyalarla tutuyor.

Kapılar: kontrolcü, fig_mm_pdf, denge, zenginlik ve fig_qc beşi de her önizleme için var; değerler raporla aynı (QC ayarlı 97.3 / 100.0 / 97.3, katı 91.7 / 94.2 / 91.7, en küçük yazı 8.25-8.275 pt).

pv_c sayıları: basamak sınırları üç Mantel dosyasının birleşik beşte birliklerinden yeniden çıktı (-1.084, -0.836, -0.704, -0.567). CIFAR-10 basamak sayıları 26, 74, 100, 118, 62 (toplam 380 = 190 çiftin iki katı). Grup boyları hücre tablosuyla aynı. Föy satır 1970'teki K = 20 ve satır 1595'teki K-c değerleri tutuyor.

pv_b sayıları: 40 değerin hepsi pv_b_model_yapisi.txt satırlarıyla eşleşiyor; 32'den 224'e büyütme src/models/vit.py:392'de doğrulandı.

İzdüşüm: PNG'de plaka kenarları 35.9° ve 17.8° ölçüldü; manifestlerdeki bütün nesneler 36/18 açısını taşıyor. Yüz tonları ve gölge yönü üç şekilde tutarlı. Motorda yalnız uslup.py satır 1060'taki hata iletisi değişmiş.

## Bulgular

1. Kritik. Özgünlük ölçütü karşılanmıyor (üç PNG; uslup_Z.yaml:30-31). pv_a, fig1'in beş panelinin bir plakanın üstüne yeniden dizilmesi; nesnelerin plakadaki yeri hiçbir şey anlatmıyor, 4. istasyon plakanın dışında, 5. istasyon bir metin kartı, destelerden matrislere giden bağ hâlâ ok. pv_b, "katmanları eğik sıraya dizilmiş patlatılmış ağ" kalıbı; ResNet'in BasicBlock içi açılmıyor. pv_c, fig8'in CIFAR-10 kartını eğik plakaya yatırıyor; yükseklik yalnız grup üyeliğini taşıyor. Gerilim: kullanıcı "komple 3 boyutlu" istiyor, skill kuralı (uc_boyut.md:5, :11) 3B veri kodlamayı yasaklıyor; BEKLEYEN_KARARLAR'a yazılmalı. Sahne dili nesnenin yerini anlam taşıyacak biçimde kurmalı (örneğin zaman ya da kayıt sırası derinlik ekseninde).

2. Orta. Turuncu ile mavinin zıtlığı yalnız soluklaştırılmış (uslup_Z.yaml:119, :121 ile :279 çelişiyor). ResNet arduvaz (ton 246°), ViT kiremit (ton 43°); ton farkı yaklaşık 203°, tümler çift. Öneri: ResNet'i zeytin ya da sıcak gri yapmak, ayrımı L farkı ve dokuyla kurmak.

3. Orta. pv_c'de gri baskı ayrışması bozuk. Lejant gri değerleri 239, 212, 182, 154, 126; köşegen 170, yani 3. ile 4. basamağın arasına düşüyor. En açık basamak (239) plakayla (243/238) neredeyse aynı. Öneri: köşegeni koyu nötre (L 0.45 altı) ya da tarama dokusuna almak; isi_1 ile sahne arasında en az 0.08 L farkı.

4. Orta. pv_c'de plato duvarları arkadaki hücrelerin en çok üçte ikisini kapatıyor; ölçülen değerin görünmemesi veri şeklinde kabul edilemez. Öneri: platoyu kaideye gömmek ya da yalnız kenar şeridiyle göstermek.

5. Orta. pv_c "sematik" diye sınıflanarak veri denetimlerinden kaçmış (pv_c_relief.fig.json:1048, :1058); QC raporunda B2-B5, D1 ve D2 atlanmış. Öneri: veri türüyle yeniden koşmak ya da atlanan denetimleri açıkça yazmak.

6. Orta. pv_a, fig1'in (d) panelindeki "Protocol layer: nested conditioning sets" kutusunu ve (e) panelindeki "panel means" kutusunu rapora yazmadan bırakmış (rapor satır 110).

7. Orta. Ayrışma kuralı OZGUN istisnasıyla gevşetilmiş (ayrisma.py:35-39, ~505); Z tanım gereği düşemez hâle gelmiş. Kalıntılar: SEMA.md:174 "66/66", SEMA.md:5 "on iki üslup", ayrisma.py main örneğinde "/66"; SKILL.md:123 "üç anahtar" ile SEMA.md:166 ve SKILL.md:230 "iki" çelişkisi önceden var.

8. Küçük-orta. İstasyon numaraları sahnede yok; pv_b'de "1 Input" başlığı sol altta, giriş levhası sol üstte, kılavuz yok; pv_a'da "3 Matrices" kılavuzları destelerin ve CIFAR-100 kartının üstünden geçiyor; pv_b'de "patch embedding" kılavuzu belirsiz.

9. Küçük. pv_a ve pv_c kanıtlarının karantina alanı "yalnız results/c1_*, results/q1/*, föy, src/" diyor; oysa raporlar/konsey_2026-10-29/hucre_tablosu*.json ve data/ altındaki CIFAR dosyaları okunuyor. İhlal değil, beyan yanlış.

10. Küçük. pv_b etiketleri fazla genel: "timm resnet18" 224 hattını belirtmiyor; altyazıdaki "Both ... resized to 224×224" R32 köprüsü için doğru değil; V-IN hücresi deit_tiny_patch16_224 ağırlığı (src/models/r224.py:53) etikette yok.

11. Orta. DPI kararı Faz 2 için risk: 96 DPI'da bütün çizgiler 0.751 pt, kıl çizgi iki katına çıkıyor; ekran ölçeği yüzde 125'e dönerse motor Faz 2 ortasında durur. Öneri: Faz 2 başında DPI'ı ölçüp ayarla uyuşmazsa duran tek v2 ayar dosyası.

12. Küçük. pv_c karakter yoğunluğu 1.80 kar/cm² ve yazı kutusu 0.10, beğenilen bandın altında; denge.md:94'e göre kısıt değil ama raporda yazılmalıydı.

13. Bilgi. "627 geçti, 2 başarısız" test sonucu yeniden koşulmadı.

## Özgünlük yargısı

pv_b üçünün en güçlüsü ve tek gerçek 3B modelleme; ışık, gölge ve izdüşüm tutarlı, zanaat iyi. Ama biçim derin öğrenme literatüründe en çok görülen mimari çizim dili ve "klişelerden kurtul" isteğine cevap vermiyor; buzlu mercekteki blok açılımı dikkatin yapısını göstermiyor. pv_a, fig1'in kutularının düz izometrik levhalara dönüşmüş hâli; sahne bir taşıyıcı tablaya indirgenmiş, şeklin yarısına yakını metin; kutu ve ok akışı kırılmamış, dağıtılmış.

pv_c kullanıcının "3 boyutlu yeni figür" beklentisini karşılamıyor; eğik düzleme yatırılmış ısı haritası, 3B görünüm bilgi katmıyor, okunurluğu düşürüyor ve hücrelerin bir kısmını örtüyor. Soluk toprak paleti "cırtlak olmasın" isteğini karşılıyor, ama asıl zıtlık ekseni korunduğu için "zıt renklere odaklanma" eleştirisi yerinde duruyor. Teslimat teknik olarak temiz ve dürüst belgelenmiş bir ara adım; "hayran bırak" düzeyinde özgün bir dil değil.

Çürütücünün bakış kopyaları ve betikleri (proje dışı): C:/Users/cagri/AppData/Local/Temp/claude/e2c0fa868388f4cf/0d0fab82-c6b8-472d-a420-d8ffb5857ab2/scratchpad/curut/
