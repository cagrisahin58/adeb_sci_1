# Yazım brifi: LeCun turu metin yeniden kurulumu (2026-10-04)

Hedef: `paper/manuscript/` (IEEE Access, EN). Her sayı `results/C1_REFERANS_FOYU.md` içinden alınır; föyde
olmayan sayı metne girmez. Plan ve bulgular: `results/q1_research/LECUN_PLANI_2026-10-04.md`; hüküm:
`raporlar/hakem_lecun_2026-10-04/00_LECUN_HUKUM.md`. Olumsuz sonuçlar silinmez; manşetten çıkar.

## Değişmeyen omurga
Dört protokol tasarımı, örnek bazında kayıt, üç tohum (indeksle eşli), iki çıkarım birimi, ön kayıt
beyanları ve sapması, mutlak gürbüzlük sonucu (CNN üstünlüğü, McNemar her koşuda), WRN üçüncü model,
davranışsal bölümlerin tabloları. Şekil 3 merkez şekil kalır (sağ panel ikili uzaklıklar).

## Başlık
"The Conditioning Set Decides the Measured Transfer Asymmetry: An Exact Correction and a Matched-Pair
Prediction for CNN versus Vision Transformer Robustness Comparisons"

## Özet (≤250 kelime) omurgası, sırayla
1. Konu cümlesi: mimariler arası transfer karşılaştırmalarında koşullama kümesi nadiren DEĞİŞTİRİLİR
   (raporlanmaz değil: Mahmood, TREND, Zhao kümelerini yazar); aynı modellerde dört protokol ne kadar
   oynatıyor ölçtük.
2. Kurulum: AT ResNet-18 / ViT-Tiny, üç koşu, tam test, örnek bazında kayıt, sızıntısız bölme.
3. Sonuç 1: asimetri 4,4–19,4 puan; yeniden eğitim aralığı en çok 2,4 (aralık-aralığa; SD 0,23–1,27).
4. Sonuç 2, ÜÇ AYRI OLGU (toplanmaz): (i) ham ile hedef-doğru arasındaki 9,21 puanı toplam olasılık
   özdeşliği tam öngörür; öncül p AT hedeflerde 0,989–1,000, standart eğitilmiş hedeflerde 0,89'a
   iner ve p=1 yaklaşıklığının artığı 1,6 puana çıkar (yeni ölçüm); (ii) başarılı-kaynak protokolü
   farklı bir nicelik kestirir ve onaylanan ikiliden 11,10 puan uzaktadır; (iii) onaylanan iki protokol
   3,91 puan ayrışır, koşum düzeyi %95 t aralığı [3,12; 4,70].
5. Sonuç 3: yön kaynak etkisidir: hedef-doğru 3×3 matrislerinde toplamsal ayrıştırma kaynak farkı
   +5,13 (CIFAR-10) / +9,54 (CIFAR-100), hedef farkı −2,03 / −6,19; sabit WRN karşıtlıkları aynı yönde.
6. Sonuç 4: büyüklük temiz farkın fonksiyonu: eşlenmiş çiftlerde yayılım küçülür (SVHN 1,9 puan fark →
   3,7 yayılım; temiz ResNet-18 ile standart WRN-28-10 0,3 fark → 0,2 yayılım); sekiz modellik
   RobustBench havuzunda (eğitim yok) ilişki [föyden]; seçim kuralı yayılımı ~2 puan oynatır.
7. Kapanış: üç okuma doğrudan ölçümde tutmaz (tek cümle); raporlama gereklilikleri.
"We show that much of the disagreement comes from the measurement protocol" cümlesi SİLİNİR.

## §1 Giriş katkı paragrafları
- Katkı 1: protokol duyarlılığı (aralık-aralığa karşılaştırma), üç ayrı olgu, eşdeğerlik kararını
  protokolün belirlemesi.
- Katkı 2: özdeşlik ve p ölçümü; "an identity we derive" yerine "an elementary identity, the transfer
  analogue of the TRADES decomposition, whose premise we measure".
- Katkı 3 (YENİ yerine geçer): yön kaynak etkisi; "property of the weaker target" cümlesi ve r=0,986
  manşeti düşer (r föyde kalır, metinde yalnız destek).
- Katkı 4: eşlenmiş çift öngörüsü ve dış havuz; seçim kuralı duyarlılığı.
- Olumsuz sonuçlar paragrafı tek cümleye iner ve §4-G'ye işaret eder.
- ATEEC paragrafı: "corrects one claim" kalır; "two further datasets" → ayrıca dış havuz ve temiz çiftler.

## §2 İlgili çalışmalar
"we know of no controlled estimate" ve "rarely reported" → "rarely varied" / "no study varies the
conditioning set on fixed models". TRADES ayrışımı atfı özdeşlik cümlesine. II-A/II-B ders kitabı
paragrafları yarıya.

## §3 Yöntem
Dört maske tablosu (raw, tc, bc, ss + sıkı/gevşek alt seçimi) tek tabloda; 03:118 cümlesi aynen
(önceki düzeltme); özdeşliğin AT-hedef rejimi şerhi; p tanımı burada.

## §4 Deneyler, yeni sıra (etiketler korunur, yeni etiketler eklenir)
A. Mutlak gürbüzlük (kısaltılmış; Tablo 1-2).
B. Protokoller ve özdeşlik (Tablo 3, Şekil 3): üç ayrı olgu metni; "entire gap is identity" dili yerine
   "the identity predicts the raw–target-correct gap exactly"; p ölçümü AT hedeflerde; eşdeğerlik
   kararı; gevşek/sıkı alt seçim paragrafı kısa.
C. YENİ alt bölüm "Source effect, not target weakness": toplamsal ayrıştırma tablosu (CIFAR-10 ve
   CIFAR-100, kaynak/hedef etkileri, artık, R²; sabit-WRN karşıtlıkları) + Mahmood 8×8'de aynı
   ayrıştırma (ViT güçlü kaynak; CIFAR-100 ResNet-56/164 çiftlerinde bizimle aynı yön ama hedef terimi).
   04:172 ve 05:17'deki "weaker target" paragrafları buraya göre yeniden yazılır.
D. Ayarlar arası (Tablo 6 protokol×ayar) + YENİ Şekil (yayılım–temiz fark, tüm çiftler, özdeşlik
   öngörüsü içi boş işaretçi; başarılı-kaynak terimi ayrı panel). Üç-protokol eğimi +0,470 artık
   artefaktlı ve "özdeşlik teriminin dışarıda sınanması" diye konumlanır (M1); dört-protokol eğimi geri
   çekilmiş kalır.
E. YENİ alt bölüm "Standard-trained targets and an external model pool": temiz çiftler + Standard WRN
   (p 0,89–0,93; artık 1,6; 0,3 fark → 0,2 yayılım), RobustBench havuzu (modeller, p aralığı, yayılım–
   fark ilişkisi, kaynak/hedef etkileri). p=0,88 karantina cümlesi SİLİNİR, yerine bu ölçüm.
F. Seçim kuralı: mevcut PGD-10 etkisi + YENİ: son kontrol noktasında yayılım ~2 puan düşer, temiz fark
   ~1,5 puan kapanır, yön ve sınıf aynı; yörüngelerde fark ≥10,6 → "seçim artefaktı" iddiası
   sınırlanır (M2'ye cevap).
G. "Three readings that do not survive direct measurement": gradyan (seyreklik vs lokalite; Tablo 8-9),
   dikkat (Tablo 10, Şekil 6-7; TOST artık artefaktlı: 12/12, en büyük p 0,006; devrilen/devrilmeyen
   kosinüs farkı koşu düzeyinde anlamlı değil, ResNet dahil → metin düzeltilir), TGR (Tablo 11).
   Düzyazı yarıya; her birine bir paragraf + tablo göndermesi; "the one place where units disagree"
   cümlesi kalır.
H. Varyans kaynakları (mevcut; aralık-aralığa dil).

## §5 Tartışma
Protokol itirazı paragrafı kalır. Mahmood paragrafı: kısmi uzlaşma (CIFAR-100 sıfırdan ResNet'ler aynı
yön; mekanizma farklı; CIFAR-10 çiftinde protokol etkisi −0,6 [−1,3; +2,2], çelişkiyi açıklamaz) →
açık soru olarak yazılır. Sınırlılıklar tek paragraf: tek AT çifti, AT-only özdeşlik rejimi (standart
hedeflerde p düşer), iki tohumlu SVHN, ön kayıt sapması, karma kayıplı tarif ("mixed-loss PGD adversarial
fine-tuning"), 15 puanın eşlenmemiş çift özelliği olması. Raporlama gereklilikleri numaralı liste
(IEEE'de kabul), ilk ikisi vurgulu.

## §6 Sonuç
Sentez, tekrar yok; "The measurement dominates" cümlesi kalkar; "the conditioning set decides".

## Kurallar
- Hiçbir tablo/şekil etiketi silinmez; yeni etiketler: `tab:source_target`, `tab:external_pool`,
  `fig:spread_clean_gap`. TR aynası aynı yapıyı izler (ikinci geçişte).
- Dil: profesyonel Amerikan akademik; koyu etiket yok, uzun tire yok, listeler yalnız gereklilikler.
- Her yeni sayı için föy bölümü adı yorum satırında (% REF: ...) belirtilir.
