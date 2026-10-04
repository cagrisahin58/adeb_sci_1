# LeCun planı: dürüst katkıları güçlendirme turu (2026-10-04)

Kullanıcı kararı (04.10.2026): olumsuz sonuçlar manşet olmaktan çıkar (silinmez; kısa paragraf ya da ek
dosya), ağırlık özdeşlik, protokol düzeltmesi ve kaynak-etkisi bulgularına kayar; gerekirse yeni ölçümle
güçlendirilir. Hüküm ve gerekçe: `raporlar/hakem_lecun_2026-10-04/00_LECUN_HUKUM.md`.

## Omurga (yeni çerçeve)

1. Koşullama kümesi adlandırılmalıdır; aynı modellerde dört protokol asimetriyi 4,4 ile 19,4 puan arasında
   oynatır, yeniden eğitim en çok 2,4 puan oynatır.
2. Ham oranın koşullu orandan sapması toplam olasılık yasasıdır (TRADES ayrışımının transfer karşılığı);
   yeni olan öncül p'nin ölçülmesi: 0,989 ile 1,000 (36 yön). Düzeltme kapalı formda uygulanır.
3. Yön bir kaynak etkisidir (ViT kaynaklı örnekler her hedefe daha kötü taşınır), zayıf hedef etkisi değil.
   3x3 matrislerde toplamsal ayrıştırma + Mahmood ve ark. (2021) 8x8 matrisinde dış sınama.
4. Büyüklük temiz doğruluk farkının fonksiyonudur: eşlenmiş çiftlerde yayılım küçülür (SVHN 3,7 puan;
   Mahmood'un 1,6 puanlık çiftinde özdeşlik öngörüsü). Seçim kuralı temiz farkı ve dolayısıyla yayılımı
   oynatır (saklı yörüngeler + son kontrol noktası).
5. Dış model havuzunda (RobustBench, eğitim yok) p, özdeşlik artığı ve "yayılım ∝ temiz fark" öngörüsü
   sınanır; standart eğitilmiş hedefte p ölçülür (karantinadaki 0,88'in yerine).

## Faz 1: masa başı çözümlemeler (GPU yok) — deney-takibi

| # | İş | Girdi | Çıktı |
|---|---|---|---|
| 1.1 | Toplamsal kaynak+hedef ayrıştırması (en küçük kareler, hedef-doğru oranlar, köşegen hariç) | `results/c1_c3/c3_summary.json`, `results/q1/cifar100/transfer/e1_c3_summary.json`, Mahmood CIFAR-10/100 8x8 | `results/q1/kaynak_hedef_ayristirma.json` |
| 1.2 | Mahmood tabloları yapısal olarak metinden okunur; özdeşlikle öngörülen ham oranlar, çift başına öngörülen protokol etkisi (raw−tc), kaynak/hedef etkileri | `results/q1/dis_veri/mahmood2021_metin.txt` | `results/q1/dis_veri/mahmood2021_tablolar.json`, `results/q1/dis_veri/mahmood2021_ozdeslik.json` |
| 1.3 | Seçim kuralının asimetriye etkisi: saklı yörüngelerde epok başına dört protokol asimetrisi ve yayılım (seçilen vs son epok) | `results/q1/e3_akolu/*.json`, `results/q1/e2/*` | `results/q1/secim_asimetri_etkisi.json` |
| 1.4 | Eksik artefaktlar: SVHN-dahil üç-protokol eğimi (küme bootstrap) ve dikkat entropisi TOST (katman başına, df=2, ±0,05) | `results/q1/e3_asimetri_fit_svhnli.json`, `results/c1_c4/pair*/c4_summary.json` | `results/q1/e3_uc_protokol_svhnli_fit.json`, `results/c1_c4/c4_entropy_tost.json` |

## Faz 2: yeni ölçümler (GPU, kısa) — ana oturum

| # | İş | Çıktı |
|---|---|---|
| 2.1 | Temiz eğitilmiş C1 çiftleri (3 çift) + standart eğitilmiş RobustBench "Standard" WRN: 3x3 transfer, örnek bazında kayıt → p, özdeşlik artığı, dört protokol | `results/q1/temiz_ciftler/pair{1,2,3}/` |
| 2.2 | Genişletilmiş CIFAR-10 havuzu (eğitim yok): ResNet-18 AT, ViT-Tiny AT (çift 1), Standard, Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Debenedetti2022Light_XCiT-S12, Gowal2020Uncovering_28_10_extra → tüm çiftlerde dört protokol, p, artık, yayılım-temiz fark ilişkisi | `results/q1/havuz_cifar10/` |
| 2.3 | Son kontrol noktası (`adv/.../last.pth`) ile 3 çiftte dört protokol asimetrisi (seçim artefaktı) | `results/q1/son_kontrol_noktasi/pair{1,2,3}/` |

## Faz 3: metin (Faz 1-2 sayıları föye girdikten sonra) — makale-yazari

Başlık ve özet yeni omurgaya; §1 katkılar üç olgu + kaynak etkisi + eşlenmiş çift öngörüsü; §4 sırası:
protokoller → özdeşlik ve p → kaynak-hedef ayrıştırması (yeni tablo) → ayarlar arası (tablo 6) → dış havuz
(yeni şekil: yayılım-temiz fark, tüm çiftler) → seçim kuralı; davranışsal bölümler (gradyan, dikkat, TGR)
tek alt bölümde kısa paragraflar, tabloları ek dosyaya; §5 Mahmood uzlaşması/açık soru; §6 sentez.
Şekil 3 sağ paneli ikili uzaklıklar. TR aynası, dokuz kapı, föy, paket.

## Faz 3 ayrıntı (karar: ek dosya YOK; olumsuz sonuçlar ana metinde tek kısa alt bölümde kalır,
tabloları korunur, düzyazısı kısalır; TR aynası aynı yapıyı izler)

- Başlık (seçim): "The Conditioning Set Decides the Measured Transfer Asymmetry: An Exact Correction
  and a Matched-Pair Prediction for CNN versus Vision Transformer Robustness Comparisons".
- Özet omurgası: (1) aynı modellerde dört protokol 4,4–19,4; yeniden eğitim ≤2,4 (aralık-aralığa);
  (2) üç ayrı olgu: raw−tc 9,21 özdeşlikle tam öngörülür (p ölçülü, 0,989–1,000 AT hedeflerde;
  standart hedeflerde 0,89'a iner ve artık 1,6 puana çıkar), başarılı-kaynak farklı nicelik, onaylanan
  ikili 3,91 [3,12; 4,70]; (3) yön kaynak etkisidir (toplamsal ayrıştırma, WRN karşıtlıkları, Mahmood
  8×8'de dış sınama); (4) büyüklük temiz farkın fonksiyonu: eşlenmiş çiftlerde yayılım küçülür
  (SVHN; temiz ResNet/Standard WRN 0,3 fark → 0,2 yayılım; RobustBench havuzu); seçim kuralı temiz
  farkı oynatır; (5) üç okuma doğrudan ölçümde tutmaz (bir cümle).
- §4 sırası: A mutlak gürbüzlük (kısa) → B protokoller ve özdeşlik (Şekil 3 sağ panel ikili
  uzaklıklar) → C kaynak-hedef ayrıştırması (YENİ tablo: C10/C100 3×3 + Mahmood 8×8 etkileri) →
  D ayarlar arası (Tablo 6) ve YENİ şekil: üç-protokol yayılımı vs temiz fark, tüm çiftler, özdeşlik
  öngörüsü içi boş işaretçi; başarılı-kaynak terimi ayrı panel → E dış havuz ve standart hedeflerde p
  (YENİ tablo) → F seçim kuralı (asimetriye etkisi) → G davranışsal ölçümler (gradyan/dikkat/TGR,
  tablolar kalır, düzyazı yarıya) → H varyans kaynakları.
- §5: Mahmood uzlaşması ya da açık soru; sınırlılıklar tek paragraf (tek çift, AT-only özdeşlik
  rejimi, iki tohum SVHN, ön kayıt sapması). §6 sentez, tekrar yok.
- Metin: makale-yazari (opus) tek tur + hakem-simulasyonu (yontem) tek geçiş; sonra TR ayna.

## İlerleme

- 04.10 18:xx: Mahmood PDF indirildi, Tablo 1-2 metni çıkarıldı (`results/q1/dis_veri/`). Konteynerde
  robustbench var. GPU ~12 GB dolu, 20 GB boş.
- 04.10 18:1x: Faz 1 deney-takibi ajanına verildi. Faz 2 koşuları başladı: `scripts/q1_son_kontrol_noktasi_run.sh`
  (2.3) ve `scripts/q1_temiz_ve_havuz_run.sh` (2.1 + 2.2); altı RobustBench modeli indi
  (`scripts/q1_havuz_indir.py`). `experiments/c1_c3_transfer_matrix.py`'ye `--rb-model AD[:TAKMA_AD]`
  eklendi (varsayılan referansı kapatır). Analiz betiği `experiments/q1_havuz_analiz.py` (dört protokol,
  p, p=1 artığı, yayılım-temiz fark eğimi, toplamsal ayrıştırma); C1 çift 1 üzerinde doğrulandı
  (raw/tc/bc 13,19/4,81/8,49 ≈ föy 13,20/4,82/8,52; ss 21,01 vs 20,79 ayrı saldırı koşusu).
- 04.10 18:3x: **Temiz çift 1 sonucu** (`results/q1/temiz_ciftler/pair1/havuz_protokoller.json`):
  standart eğitilmiş hedeflerde p = 0,889–0,933 (karantinadaki 0,88 yerine geçerli artefakt), p=1
  artığı en çok 1,58 puan; temiz farkı 0,31 olan ResNet-temiz/Standard WRN çiftinde dört protokol
  yayılımı 0,19 puan, 15 puan farklı çiftlerde 13,7 puan → "yayılım ∝ temiz fark" öngörüsü eğitim
  dışı modellerde de tutuyor. NOT: tam özdeşlik aynı örneklerde tanım gereği sıfır artık verir; bilgi
  taşıyan nicelik p'dir; makaledeki 0,41 puan p=1 yaklaşıklığının artığıdır (metin buna göre yazılacak).
- 04.10 18:5x: **Faz 1 bitti** (deney-takibi; betikler `experiments/q1_kaynak_hedef_ayristirma.py`,
  `q1_mahmood2021_tablolar.py`, `q1_secim_asimetri_etkisi.py`, `q1_e3_uc_protokol_svhnli_fit.py`,
  `c1_c4_entropy_tost.py`). Bulgular: (1.1) hedef-doğru oranlarda kaynak farkı (ResNet−ViT) +5,13±0,09,
  hedef farkı (ViT−ResNet) −2,03±0,51 (CIFAR-10); CIFAR-100 +9,54 / −6,19; sabit-WRN karşıtlıkları
  +3,83 / +3,33 → B3 doğru, yön kaynak etkisi. (1.2) Mahmood CIFAR-10: ViT güçlü kaynak (12/12 aile
  çifti), BiT-50x1/ViT-L-16 çiftinde özdeşlik öngörülü protokol etkisi −0,59 [−1,25; +2,15] → protokol
  yön çelişkisini açıklamıyor; CIFAR-100'de sıfırdan eğitilmiş ResNet-56/164 ile 6/6 çiftte CNN→ViT
  daha güçlü (bizimle aynı yön) ama orada HEDEF terimi taşıyor (+30,2), ham puanlamada işaret dönüşü
  öngörülüyor (aralık sıfırı içeriyor) → "kısmi uzlaşma, mekanizma açık". Not: Tablo 2 köşegeni bağımsız
  ikinci kopya, beyaz kutu değil. (1.3) Seçim kuralı: yörüngelerde temiz fark kapanmıyor (≥10,6),
  yayılım ±1,3 oynuyor, hedef-doğru asimetrisi ~2,5 puan duyarlı → M2'nin "yayılım artefakt" kısmı
  desteklenmiyor, düzey duyarlılığı föye girer. (1.4) +0,4697 [+0,3606; +0,6649] birebir yeniden
  üretildi (`results/q1/e3_uc_protokol_svhnli_fit.json`); 20 yön çiftinin 19'unda üç-protokol yayılımı
  = |raw−tc| (M1 doğru, eğim özdeşliğin kendisi); TOST 12/12 kabul, en büyük p 0,00611; devrilen/
  devrilmeyen 0,9895/0,9877 yeniden çıktı ama koşu düzeyinde p=0,20 ve ResNet farkı p=0,080.
- 04.10 18:5x: **Faz 2.3 bitti**: son kontrol noktasında temiz fark 10,1–11,2 (seçilende 11,3–13,0),
  dört-protokol yayılımı 12,5–13,2 (seçilende 14,4–16,0), hedef-doğru asimetri +4,48/+4,17/+5,27
  (seçilende +4,83/+4,28/+3,97): seçim yayılımı ~2 puan, farkı ~1,7 puan oynatır; yön ve büyüklük
  sınıfı değişmez. Faz 2.1 bitti (3 temiz çift; p aralığı 18 yönde 0,877–1,000, Standard WRN hedefte
  0,877–0,996, ViT temiz hedefte 0,923–0,934).
- 04.10 19:0x: **Faz 2.2 havuz bitti** (8 model, 28 çift): p 0,933–1,000 (Standard hedefte 0,933–0,996;
  AT hedeflerde ≥0,985), p=1 artığı en çok 0,35 puan; yayılım–temiz fark eğimi üç protokolde +0,872
  [+0,534; +1,274], r 0,944; dört protokolde +0,559 [−0,205; +4,582] (anlamsız); işaret dönen tek çift
  ViT_Tiny_AT/Standard (1/28). **Föy genişletildi** (kod-mimar, sekiz yeni bölüm), dokuz kapı geçiyor.
  Tüm çiftler (havuzun C1 ile çakışan üç çifti çıkarılınca 60 nokta): üç protokol eğimi +0,796
  (r 0,957), özdeşlik paritesi r 0,9996, en büyük sapma 1,09 (standart hedef); 57/60 çiftte üç
  protokol yayılımı = |raw−tc|.
- 04.10 19:2x: **Şekiller** (gorsel-uretici): `paper/figures/fig_yayilim_temiz_fark.py` →
  `final/fig_spread_clean_gap.*` (iki panel, 60 çift, içi boş özdeşlik öngörüsü) ve Şekil 3 sağ paneli
  ikili uzaklıklarla (9,21 özdeşlik terimi / 3,91 onaylanan ikili / 11,10 farklı nicelik; ayrışım
  parantezleri kalktı; `bas_kaynak_eksi_her_ikisi_dogru` alanı veri betiğine eklendi). Denklem numarası
  şekle basılmaz kuralı sürüyor. Eski Şekil 3 sürümü `paper/figures/arsiv/fig_protocol_sets_v3_2026-10-03.*`.
- 04.10 19:4x: **Faz 3 metin** (makale-yazari): EN el yazması yeni omurgada; başlık, 249 kelimelik özet,
  dört katkı, yeni `tab:protocol_masks` (§3, `eq:general_identity` + `eq:raw_identity` oraya taşındı),
  §4 A–H sırası, yeni `tab:source_target` (table*), `tab:external_pool`, `fig:spread_clean_gap`; §4-G
  davranışsal ölçümler tek alt bölüm; §5 Mahmood kısmi uzlaşma + sekiz maddelik gereklilik listesi;
  §6 sentez. 24 sayfa, 0 hata; ayna dışındaki sekiz kapı geçiyor; `verify_manuscript_numbers.py`'ye
  yalnız-EN 180 yeni kontrol (`chk_en`; TR eşitlenince `chk`'ye çevrilecek); `gonderim_tutarlilik.py`
  başlık normalizasyonu düzeltildi; `check_pdf_render.py` başlık dizesi güncellendi. Kararlar: karantina
  literalleri (Tablo 2 alt blok, Tablo 3 ‡) ÇIKAR, tek nitel cümle; kapak mektubu/öne çıkanlar/veri
  bildirimi bu turda (yazara ek tur verildi). Hakem (yontem merceği) tek geçiş başlatıldı.
- Açık depo kurucusu güncellendi (`scripts/acik_depo_kur.sh`: yeni betikler, results/wrn_eval, Mahmood PDF
  hariç); kopya 32 MB / 1079 dosya; föy kopyadan birebir yeniden üretiliyor.
- 04.10 20:0x: Yazar ek turu: karantina literalleri çıktı (tek nitel cümle), kapak mektubu / öne çıkanlar /
  beyanlar / veri bildirimi yeni omurgada; donanım cümlesi düzeltildi (C1 çiftleri 5060 Ti, Q1 ve havuz
  5090). Commit ca41c4a (EN Faz 3).
- 04.10 20:1x: **Hakem ikinci geçişi** (yöntem; `raporlar/hakem_lecun_2026-10-04/hakem_yontem_yeniden_yazim.md`):
  yeni tablo/şekil hücrelerinin hepsi doğru; **F3**: "büyüklük temiz farkı izler, eşlenmiş çiftlerde küçülür"
  yalnız üç protokollü yayılım (özdeşlik terimi) için doğru; dört protokollü yayılım eşlenmiş gürbüz çiftlerde
  6–13 puan (başarılı-kaynak terimi). Kararlar: iddia daraltıldı, **başlık** "… An Exact Correction and a
  Source-Effect Reading …" (Matched-Pair Prediction çıktı); M1 Şekil 3 altyazısı (11,10 + 3,91 = 15,01;
  koşulsuz kestirim CIFAR-10'da içeride, CIFAR-100'de üst uç); M2 her-ikisi-doğru satırları tabloya; M3 temiz
  çiftte ViT en zayıf kaynak, yön hedef terimiyle; M4 Mahmood CIFAR-100 6/12 işaret dönüşü; M5 gereklilik 2
  p-aralığı sınırı; M6 öngörü = özdeşliğin sonucu, ölçülen içerik üç madde; M7 son kontrol noktası epokları,
  "artefakt değil" yumuşatıldı; M8 ~40 gövde sayısı föye (kod-mimar), SVHN farkı 1,84. Yazara ve kod-mimara
  verildi; TR ayna paralel sürüyor (hakem düzeltmeleri TR'ye ikinci mesajla yansıtılacak).
- 04.10 21:xx: **Tur kapandı.** Hakem düzeltmeleri EN'e işlendi (F3 daraltma, yeni başlık, M1–M7, m1–m14;
  son kontrol noktası epokları ViT 45/38/39 ve ResNet 71/76/77, seçilen 25/18/19 ve 51/56/57); föye
  "Govde metnindeki diger sayilar (hakem M8)" bölümü (16 madde); üç yeni atıf (carmon2019unlabeled,
  wong2020fast, engstrom2019robustness; arXiv doğrulandı); TR ayna cümle düzeyinde eşitlendi (edilgen çatı,
  özet 248 sözcük, iddia kapısının iki muhafız dizesi edilgene çevrildi); sayı kapısı 426 kontrol iki dilde;
  EN 25 sayfa, TR 25 sayfa; **DOKUZ KAPI GEÇİYOR**. Açık depo kopyası yeni artefaktlarla kurulabilir
  (`scripts/acik_depo_kur.sh`); itme kullanıcıda. m15 (dört panel atfı) ve kapak mektubunun ATEEC bildirimi
  kullanıcı onayı bekliyor; ATEEC kararı gelince "submitted" → "presented".
