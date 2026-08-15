# E2 Sızıntı Ablasyonu — Ön-Kayıtlı İstatistik Protokolü

**Yazım tarihi: 2026-08-14, eğitim başlatılmadan ÖNCE commit'lenmiştir.**
Bu belge, E2 sonuçları görülmeden analiz kurallarını sabitler (ön-kayıt).
Başlatma-öncesi 3-ajanlı denetimin metodoloji bulgularını işler.

## 1. Sızıntı tanımı (yapı geçerliliği)

Test edilen mekanizma, run3→C1 geçişinde düzeltilen sızıntının birebir
modelidir: **"seçim bölmesi, clean ön-eğitim sırasında modele gradyan
sağlamıştı"** (bkz. `memory/c1-sizinti-duzeltme-bulgusu`). Raporlama her iki
durumda da test kümesindedir. Makale metninde sızıntı BU şekilde tanımlanır;
"validation hem seçimde hem raporlamada kullanıldı" ifadesi YANLIŞTIR ve
kullanılmaz.

## 2. Tasarım (V_C güncellemesiyle)

- Bölmeler (seed 778, `q1_make_e2_split.py`): V_A, V_B, V_C = 2000'er örnek;
  D_core = 44.000.
- Clean ön-eğitim: D_core ∪ V_A (48k) — **V_A görülür (sızıntı tedavisi)**;
  V_B, V_C görülmez. Sabit 200 epok, seçimsiz; AT başlangıcı `last.pth`.
- AT: yalnız D_core, sabit 100 epok (`--patience 0`), her epok checkpoint.
- Aynı checkpoint dizisine ÜÇ çevrimdışı seçim kuralı
  (`q1_offline_select.py`, patience=20, min_delta=0.1, val PGD-10):
  - **A** = V_A ile seçim (sızıntılı)
  - **B** = V_B ile seçim (temiz)
  - **C** = V_C ile seçim (negatif kontrol)
- Her seçimin ürünü: seçilen epok + o checkpoint'in TAM 10k test kümesinde
  clean + PGD-10 doğruluğu ve örnek-bazlı doğru/yanlış maskeleri
  (`select_*_test.npz`).

**Neden V_C:** n=2000'lik iki bölme arasında, sızıntı sıfırken bile sonlu
örneklem gürültüsü farklı epok seçtirebilir (fark SE'si ≈ √2·1,10 ≈ 1,55
puan). V_B-vs-V_C karşıtlığı bu **saf seçim-gürültüsü tabanını** ölçer;
V_A-vs-V_B (sızıntı + gürültü) bu tabana karşı okunur. V_C eğitim
başladıktan sonra eklenemezdi (D_core'u değiştirir); bu yüzden başlatma
öncesinde tasarıma alındı.

## 3. Uç noktalar (önem sırasıyla)

**Eş-birincil 1 — McNemar (örnek düzeyi):** Her tohumda A-seçimli ve
B-seçimli modelin test PGD-10 doğru/yanlış maskeleri eşleştirilir; üç tohum
havuzlanır (~30.000 eşleşmiş birim). Aynısı B-vs-C için (gürültü tabanı).
n=3'ün rehinesi olmayan, sonuçsuzluğa karşı en güçlü test budur.

**Eş-birincil 2 — Eşleşmiş Δ + TOST (tohum düzeyi):** Tohum başına
Δ_AB = testAdv(A-seçimi) − testAdv(B-seçimi); TOST eşdeğerlik marjı
**δ = 1,0 puan**, α = 0,05 (%90 GA ⊂ ±δ). Aynı hesap Δ_BC için.
- δ gerekçesi: eğitim-koşusu std'sinin (~0,55 puan, C1) yaklaşık 2 katı ve
  protokol yayılımının (10,45 puan) ~1/10'u — "pratikte önemsiz" eşiği.
- n=3 aritmetiği: yarı-genişlik = t(0,95; df=2)·s_Δ/√3 = 1,686·s_Δ →
  eşdeğerlik ancak s_Δ < 0,59 puansa gösterilebilir. Bu dar tolerans
  bilinerek kabul edilmiştir; sonuçsuz kalırsa karar kuralı §5'te.

**İkincil:** seçilen epok farkı (A vs B vs C), seçilen checkpointlerin clean
doğruluğu, val eğrilerinin kendisi (`records`).

## 4. Karşılaştırma mantığı

1. |Δ_AB| ile |Δ_BC| aynı büyüklük sınıfındaysa ve McNemar A-vs-B anlamlı
   değilse: "bu rejimde seçim-sızıntısı etkisi, bölme gürültüsü tabanından
   ayırt edilemez" (negatif sonuç olarak raporlanır — tez için kullanışlı:
   protokol varyansı 10,45 puanken sızıntı katkısı ≤ gürültü tabanı).
2. |Δ_AB| ≫ |Δ_BC| ve McNemar A-vs-B anlamlıysa: sızıntı etkisi nicelenmiş
   olur; büyüklüğü protokol yayılımıyla kıyaslanarak raporlanır.
3. Ara durumlar: her iki eş-birincil uç nokta da raporlanır, tek başına
   TOST sonucuna manşet yüklenmez.

## 5. Önceden tanımlı özel durumlar

- **Dejenere s_Δ = 0** (üç tohumda da iki kural aynı epoğu seçti): t
  istatistiği tanımsızdır; bu durumda eşdeğerlik iddiası (a) seçimlerin
  özdeşliği olgusuna ve (b) McNemar'a dayandırılır (Δ ≡ 0 zaten δ içinde).
- **Seçim None** (hiçbir epok 0,0+min_delta'yı geçemedi): gerçek eğitimde
  fiilen imkânsız; olursa koşum incelemeye alınır, o hücre analiz dışı.
  *(Uygulama notu: toplama betiği final modda bu durumda raporu TÜMDEN
  reddeder — insan incelemesi olmadan rapor üretilmez; yalnız
  `--allow-partial` ara denetiminde tohum atlanarak devam edilir.)*
- **TOST sonuçsuz + fark testi anlamsız** (0,59 < s_Δ): manşet McNemar'a
  kayar; E4 (+2 tohum) tetiklenebilir — n=5'te s_Δ toleransı 1,05'e çıkar.
  E4 kararı E2+E1 sonuçlarıyla birlikte verilecek (rapor planındaki gibi).

## 6. Bilinen sınırlamalar (şimdiden beyan)

- **Ortak bölme:** V_A/V_B/V_C üç tohumda da aynı dosyalardır; bölme
  çekilişine dair belirsizlik tohumlar-arası std'ye yansımaz. s_Δ bu
  bileşeni eksik tahmin eder; makalede sınırlama olarak yazılır
  (bölme-yeniden-çekilişli tam faktöriyel, bütçe dışıdır).
- **Havuzlanmış McNemar'da test-kümesi tekrarı** *(eklendi 2026-08-14,
  toplama betiği doğrulama denetiminde — E2 verisi henüz üretilmeden)*:
  3 tohum AYNI 10k test kümesinde değerlendirilir; havuzdaki ~30k eşleşmiş
  birim aynı 10k örneğin 3 korelasyonlu kopyasıdır ve örnek-zorluk
  korelasyonu kesin binom p'sini anti-konservatif yapabilir. Havuzlama
  ön-kayıtlı tercihtir ve korunur; raporlamada tohum-bazlı McNemar
  p'lerinin havuzlanmışla yön/anlamlılık tutarlılığı BİRLİKTE gösterilir,
  makalede sınırlama olarak beyan edilir.
- **Tek veri kümesi/rejim:** E2 yalnız CIFAR-10 + PGD-10 seçim metriğiyle
  koşulur; genelleme iddiası yapılmaz.
- **AT'nin canlı `best.pth`'ı** V_A∪V_B∪V_C (6000) üzerinde seçilir —
  ÜÇÜNCÜ bir kuraldır, hiçbir analizde kullanılmaz
  (`models/q1/e2/BEST_PTH_KULLANMA.txt`).

## 6b. Ara denetim beklenti kaydı (2026-08-16, VERİ ÜRETİLMEDEN)

4/6 yörünge tamamlandığında koşulan 3-mercekli ara denetim, **eğitim
eğrilerinden** (test sayıları görülmeden) şu beklentiyi üretti. Sonuçlar
görüldükten sonra protokolü değiştirmek yasak olduğu için beklenti şimdi
yazılıyor:

- **Tepe bölgesi yassı:** ResNet kollarında tepenin 1 puanı içindeki epoklar
  38-99 aralığına *parçalı* dağılmış (tepe-5 yayılımı 0,68 puan); ViT'te daha
  keskin (tepe ep19, bant [17,32]). 2000'lik bölmenin binom SE'si ~1,05-1,11
  puan — yani eğrinin kendi salınımıyla aynı mertebede.
- **Beklenen s_Δ ≈ 0,79-1,04 puan > 0,59** (protokol §3'ün eşdeğerlik için
  gerektirdiği tolerans). Dolayısıyla **TOST büyük olasılıkla SONUÇSUZ
  kalacak** ve §5'in "manşet McNemar'a kayar" yedeği devreye girecek.
  δ=1,0 DEĞİŞTİRİLMEYECEK.
- **McNemar yanlış-pozitif tuzağı:** iki farklı epok checkpoint'i zaten
  binlerce örnekte uyuşmadığından, **sıfır sızıntı altında bile** havuzlanmış
  McNemar simülasyonda %37-56 oranında p<0,05 veriyor. Bu, V_C negatif
  kontrolünün süs değil *asıl test* olduğunu doğrular: manşet yalnızca
  |Δ_AB| ≫ |Δ_BC| ise sızıntıya atfedilir (§4 kuralı bağlayıcı).
- **Anlatı kuralları:** (a) "eşdeğerdir" denmeyecek; "sızıntı etkisi %95 üst
  sınırla ≤ X puan; protokol yayılımı 10,45 puan; oran ≥ N kat" formülü
  kullanılacak. (b) ViT mutlak gürbüzlüğü ASLA final epoktan raporlanmayacak
  (tepeden 8 puan aşağıda). (c) Sonuçlar mimari-başına verilecek: ViT
  sinyal-hakimiyetli, ResNet gürültü-hakimiyetli rejimde.

## 7. Tekrarlanabilirlik

- Seçim değerlendirmesi checkpoint-başına deterministik tohumlu
  (`seed*100000 + epoch`); test değerlendirmesi `seed=42`.
- Bölme dosyaları `git add -f` ile depoya alınır (data/ gitignore'da;
  `torch.randperm` yalnız aynı PyTorch sürümünde aynı çıktıyı verir —
  dosyaların kendisi kanonik kaynaktır).
- Toplama betiği (`scripts/q1_e2_report.py`) yalnız `select_*.json` +
  `select_*_test.npz` tüketir; bu protokolün dışına çıkan hiçbir karar
  kuralı içeremez.

## 8. Keşifsel artefaktlar (birincil analize GİRMEZ)

`q1_offline_select.py` her koşumda `select_*_valcurve.npz` de yazar: 100
epok × 2000 örneklik val doğru/yanlış maskeleri (~90 KB). Amaç, seçim
kararının **ampirik** kararsızlığını ölçmek — val bölmesi yeniden
örneklenerek (küme bootstrap) binlerce sözde-bölmede hangi epoğun seçileceği
dağılımı çıkarılabilir. Böylece gürültü tabanı, V_C'nin tek çekilişine ek
olarak dağılım düzeyinde raporlanır.

Kurallar: bu artefakt **birincil uç noktalara girmez**; ondan türetilen her
sayı makalede *keşifsel* etiketiyle sunulur; seçim kuralı (§2) hiçbir koşulda
bu analize göre değiştirilmez. Skaler kayıtlar (`records`) maskelerin
sayımlarından birebir türetilir — artefakt eklenmesi hiçbir sayıyı
değiştirmez (gerçek checkpointlerle doğrulandı).
