# B2 kolu çürütücü raporu (opus-curutucu, 07.11.2026)

Teslimat: `02_literatur_dis_gecerlilik.md`, `02_deney_adaylari.json`, `02_yeni_atiflar.bib`, `02_atif_dogrulama.json` (yürütücü: literatur-tarayici). Çürütücü dosya değiştirmemiştir; bu rapor yardımcı Fable tarafından olduğu gibi kaydedilmiştir. İkinci tur sonucu için dosya sonundaki ek bölüme bakılmalıdır.

## Birinci tur hükmü: duzeltilmeli

Raporun omurgası sağlam. 35 künyenin hepsi gerçek. Föy (`results/C1_REFERANS_FOYU.md`) satır atıfları, GPU-saat aritmetiği, indirme boyutları, lisanslar ve timm adları tuttu. Yine de üç şey düzeltilmeden rapor olduğu gibi kullanılamaz. Birincisi, tek "yüksek" tehdidi taşıyan kimlikli kaynak (Kvinge 2211.10558) özetine göre bu bulguyu söylemiyor. İkincisi, B bloğu Jones karıştırıcısını, yani gürbüzlük düzeyini değil, yalnız temiz doğruluğu eşliyor. Üçüncüsü, birkaç iç tutarsızlık var: Jiang kaynakçada sanılıyor, D bloğundaki model sayısı yanlış, "tavan" gerçek bir üst sınır değil.

## Doğrulama özeti

- Betik: `bib_dogrula.py` 35/35 VERIFIED verdi (başlık benzerliği 1,0). Çıktı: `C:\Users\cagri\AppData\Local\Temp\claude\e2c0fa868388f4cf\0d0fab82-c6b8-472d-a420-d8ffb5857ab2\scratchpad\dogrula.json`.
- Yazar ve yıl: Betik yalnız başlığı denetlediği için yazar listesi ile ilk sürüm yılı export.arxiv.org kayıtlarıyla ayrıca karşılaştırıldı; 35/35 birebir eşleşti (scratchpad `cmp.py`, `abs1.txt`, `abs2.txt`).
- Jones UAI 2022: PMLR sayfasında başlık, dört yazar ve 928-937 sayfaları doğrulandı.
- Şüpheli künye yok. Sorun künyede değil, iki kaynağın içeriğinin aktarımında (madde 1 ve 4).
- Föy satırları 1478, 1481, 1485, 1496-1499, 1526-1527, 1587, 1606, 1838, 1938 ve 2229-2236 açıldı, hepsi doğru.
- Süreler: `TIMING.md` satır 7, 13 ve 20; B3 defteri; zaman çizelgesi (B9 833 s, B10 291 s, B6_AA 2826 s, B5 440/241 s) doğru.
- Boyut ve lisans: HEAD ile yeniden ölçüldü: 183746227, 412327155, 22883348 ve 46807446 bayt, toplam 665764176. Lisanslar apache-2.0 ve cc-by-nc-4.0.
- timm 1.0.27: `vit_tiny_patch16_224.augreg_in21k_ft_in1k` ve `resnet18.fb_swsl_ig1b_ft_in1k` mevcut.
- XCiT parametreleri: M12 yaklaşık 46 M, L12 yaklaşık 103 M tahmini 12 katmanlı sürüm için makul. Diskteki S12 dosyası 103,6 MB, 26 M fp32'ye denk.
- Dondurulmuş betik SHA-256 `4bce2c98...b667389` ile eşleşiyor.
- Çakışmalar: references.bib ile eprint ya da başlık çakışması yok. Konsey raporlarıyla 8 kimlik çakışıyor: 2505.19613, 2106.14881, 2501.18629, 2412.05351, 2304.02688, 2007.00806, 1804.11285, 2606.22516.

## Bulgular

1. Yüksek. `02_literatur_dis_gecerlilik.md:32`, `:119`, `:142`; `02_deney_adaylari.json:54`, `:155`. Kvinge ve ark. 2211.10558 "Jones'un bulgusunu kimlikli kaynakla taşır" diye yüksek şiddetle sunuluyor ve makaleye girmesi önerilen beş atıftan biri. arXiv özeti ne "AT eps arttıkça modeller arası benzerlik artar" diyor ne de ViT-ResNet karşılaştırmasından söz ediyor; yalnız "neural frames" yöntemini ve AT ile genelleme arasındaki ödünleşimi anıyor. Ayrıca yayın yeri (NeurIPS 2023 NeurReps çalıştayı) arXiv yorum alanında yazıyor ama bib notuna (`02_yeni_atiflar.bib:13`) alınmamış; raporun 138. satırıyla çelişiyor. Ya tam metinden ilgili bölüm sayfa numarasıyla gösterilmeli ya da Kvinge "yüksek" satırından çıkarılmalı. Jones PMLR künyesiyle elle eklenmeli; künye doğrulanmış, eksik olan yalnız DOI.

2. Yüksek. `02_literatur_dis_gecerlilik.md:87`, `:111`, `:113`; `02_deney_adaylari.json:57`, `:61-62`. B bloğu "literatürün tek yüksek tehdidini" (Jones: benzerlik gürbüzlükle artar) hedeflediğini söylüyor; oysa manipülasyon denetimi de H ölçütleri de yalnız temiz doğruluğa bakıyor (en çok 6 puan). Föy 1496 ve 1498'e göre V-scr'nin w değeri 55,63, R224-scr'ninki 48,90; Jones'un karıştırıcısı bu w farkıdır. Temiz doğruluk eşlenip w eşlenmezse H_yakınsama ile H_mimari ayrılmaz. İkinci karıştırıcı: V-scr+ temiz aşamada R224-scr'nin almadığı ağır artırma (TrivialAugment, mixup, cutmix) alıyor; 2x2 mantığı yalnız AT tarifi için savunulmuş. H ölçütlerine w eşleme koşulu (örneğin |w(V-scr+) - w(R224-scr)| <= 2 puan) eklenmeli; G bloğundaki omega kısmi Mantel B'ye bağlanıp Tier 1'e alınmalı; artırma farkı ya R224-scr+ koluyla giderilmeli ya da sınırlılık olarak önceden yazılmalı; yönetici özetindeki "doğrudan kapatır" yumuşatılmalı.

3. Orta. `02_literatur_dis_gecerlilik.md:69`, `:83`, `:121`; `02_deney_adaylari.json:44-45`. A bloğu "dönüştürücü ayna paneli" olarak üç XCiT kullanıyor; XCiT konvolüsyonlu yama gövdesi ve LPI konvolüsyon katmanları taşıyan karma bir mimari ve konseyin tablosunda da "karma" (`06_ek_deney_tasarim.md:63`). Rapor 37. satırda benzemezliğin yama gövdesinden gelebileceğini kendisi öne sürüyor; bu "kendi ailesine karşı" okumasını zayıflatıyor. Başlatma da tam eşleşmiyor: Debenedetti XCiT'leri ImageNet üzerinde çekişmeli ön eğitimden geliyor, V-IN temiz DeiT-Tiny (`src/models/r224.py:48`). Konsey IN ön eğitimli XCiT'leri R2 hakeminin itirazıyla birincil panelden bilerek çıkarmıştı (`KONSEY_PLANI.md:43`; `03_hakem_R2_ml_hakem.md:32`, `:41`); M12 ve L12 "isteğe bağlı, kullanıcı adımı" bırakılmıştı (`KONSEY_PLANI.md:155`; `01_oneri_P2_dis_gecerlilik.md:47`). Rapor "neden şimdi farklı" demiyor. Üç nokta sınırlılık olarak eklenmeli; H tanımı genişletilmeli (sigma_T(V-IN) - sigma_T(R224-IN) < 0 sonucu ve rho'nun +0,10 ile +0,15 arasındaki ara bölgesi sınıflandırılmamış).

4. Orta. `02_literatur_dis_gecerlilik.md:40`, `:142`. Wu ve ark. 1802.09707 "simetrik benzerliğin asimetriyi açıklayamayacağı" iddiasıyla ayrışımın nitel öncülü sayılıyor ve önerilen ilk atıf; arXiv özetinde asimetri ya da simetri geçmiyor, rapor da "arama özetinden" diye işaretlemiş. Tam metindeki bölüm ya da şekil sayfa numarasıyla doğrulanmadan önerilmemeli.

5. Orta. `02_literatur_dis_gecerlilik.md:55`; `02_deney_adaylari.json:33`. Liu 2504.10804 ve TESSER için "ViT kaynaklı örnekler ViT hedeflerine daha iyi aktarılır" deniyor. Liu özeti ViT'de üretilen örneklerin genel olarak (CNN'lere de) daha iyi aktarıldığını söylüyor; TESSER özeti yalnız ATT'ye göre ViT hedeflerinde +%7,2 bildiriyor. A bloğunun gerekçesinde yanlış atfedilmiş; düzeltilmeli.

6. Orta. `02_deney_adaylari.json:60`; `02_literatur_dis_gecerlilik.md:77`, `:125`. "Tavan" defterde gözlenen en kötü toplam, olası en kötü değil. AT 80 epok tavanına dayanırsa koşu başına 5,9 sa (80 x 266,6 s); B iki koşu 15,8 sa, toplam plan yaklaşık 43,1 GPU-saat olur ve 40'lık bütçe aşılır. E'de durdurma kuralı var, B ve C1'de yok. Tohum başına saat sınırlı durdurma kuralı yazılmalı ya da tavan gerçek üst sınır olarak yeniden hesaplanmalı.

7. Orta. `02_literatur_dis_gecerlilik.md:57`. "Jiang ve Chen 2606.22516 kaynakçada" deniyor; references.bib'de ve .tex dosyalarında yok, yeni bib'e (`02_yeni_atiflar.bib:346`) eklenmiş. Awad 2512.02830 gerçekten kaynakçada. Satır düzeltilmeli.

8. Orta. `02_deney_adaylari.json:107` ile `:111` çelişiyor. D'de "4 yeni (Tier 1)" model yazıyor, matris 26 modelle hesaplanmış; B, C1 ve C2 ikişer tohumla 6 yeni model getirir, AA satırı da "x 6 model" diyor. Doğru matris 28 model; düzeltilmiş hesap sigma F yaklaşık 92,6 GFLOP x 59 x 0,244 s yaklaşık 0,37 sa. Tavan aşılmıyor, metin tutarsız.

9. Orta. `02_literatur_dis_gecerlilik.md:101`; `02_deney_adaylari.json:121-130`. E bloğu konvolüsyon gövdesinin benzemezliği taşıyıp taşımadığını soruyor ama ImageNetV2 panelinde konvolüsyon gövdeli Singh ViT-S ve ViT-B de CNN paneline daha az benziyor (çift değerleri -0,167 ve -0,118; rho -0,211 ve -0,188; `11_sonuc_b8_b10.md:156`, `:168`, `:185`). H_govde öngörüsü (>= +0,18) bu kanıtı yok sayıyor; yeniden gerekçelendirilmeli.

10. Düşük-orta. `02_literatur_dis_gecerlilik.md:34`, `:87`. Lee ve ark. 2112.13492 bir tarif değil, mimari ek (SPT ve LSA) ve Tiny-ImageNet üzerinde; Gani ve ark. kendi kendine gözetimli başlatma öneriyor. V-scr+ tarifinin dayanağı yalnız DeiT III (2204.07118) olmalı.

11. Düşük-orta. `02_literatur_dis_gecerlilik.md:44`. "Düşük çözünürlükte (CIFAR-10) ViT'nin Mamba tabanlı modellerden iyi olduğu" üç özetin hiçbirinde yok; Du ve ark. özeti tersini söylüyor. Düzeltilmeli.

12. Düşük-orta. `02_deney_adaylari.json:78`, `:74`; `02_literatur_dis_gecerlilik.md:91`. C1'in H_dogru tanımında rho için pay yok (en küçük düşüş bile destek sayılır); manipülasyon denetimi önceden eğitilmiş her ağırlıkta kendiliğinden geçer (V-IN ilk epokta 93,95, referans 25,22), IN-21k ile IN-1k'yı ayıramaz; "doz ekseni" ön eğitim tarifini de değiştiriyor (V-IN DeiT fb_in1k, C1 AugReg), yazılmamış.

13. Düşük. `02_deney_adaylari.json:37-38`, `:73`, `:90`. d_yolu alanları D diskiyle uyuşmuyor: `/mnt/d/adeb_sci_1_veri/models/robustbench_zoo/cifar10/` yok (yalnız cifar100 ve imagenet var); `models/timm_agirliklar` depoda gerçek klasör, D'ye bağlantı değil. var_mi değerleri doğru.

14. Düşük. `02_deney_adaylari.json:43`. Yedi panel üyesinin sigma F değeri 27,0 değil, föy FLOP tablosuna göre 28,0 (4 x 1,111 + 2,596 + 2 x 10,487).

15. Düşük. `02_literatur_dis_gecerlilik.md:7`. "Bir haftalık GPU zamanıyla" ile beklenen 20,1 ve tavan 27,5 GPU-saat uyuşmuyor.

16. Düşük. `02_literatur_dis_gecerlilik.md:15`, `:17`. Karar kartında seçenek listesi ve "Cevap satırı: Karar: ____" var; 29.10 kuralıyla (soru, seçenek listesi ve cevap satırı yok, tek net öneri) çelişiyor.

17. Düşük. `02_yeni_atiflar.bib:96-134`, `:226-244`. Anahtar adı ile year alanı tutarsız: kim2024exploring year 2022, yao2025 year 2024, ma2024 year 2023, wang2023cnns year 2022; hepsinin yayın yeri sürümü var. IEEE biçimi için @inproceedings ve yayın yılıyla verilmeli.

## Hükmün iç tutarlılığı

"Olduğu gibi savunulabilir" ile "Tier 1 koşulsun" birlikte gerekçelendirilmiş. Makale zaten "against a single transformer reference the scratch-trained ViT is a directionally weaker source" (`01_introduction.tex:42`) ve doğruluk karıştırıcısını (`04_experiments.tex:245`) yazıyor; 111. satırdaki kapsam cümlesi bugünkü kapsamla çelişmiyor. Zayıf halka B'nin Jones itirazını "doğrudan kapatır" diye sunulması; madde 2 düzelmeden gerekçe eksik.

## Önceki turla tekrar

C1 (in21k) ve E (konvolüsyon gövdesi) için "neden şimdi farklı" gerekçesi yazılmış ve `KONSEY_PLANI.md:56` ile uyumlu. A bloğu için eksik (madde 3). Raporun 21. satırındaki "yinelemez" ifadesi 8 kimliğin konsey taramalarında zaten bulunmasıyla tam örtüşmüyor.

## Ek risk: hesaplama ayrıntıları paragrafı

`TIMING.md` başlığındaki "RTX 5090" ifadesi 30.07.2026 tarihli 22e4bef işleminde zaten var; proje CLAUDE.md'sindeki "C1 kampanyası 5060 Ti'de" bilgisi 16.08'de (b4cc383) eklenmiş. `04z_computational.tex:15`'teki "RTX 5060 Ti" sonradan yazılmış kayda dayanıyor (10. satırdaki kaynak yorumu CLAUDE.md'yi gösteriyor). Koşu sırasında yazılmış kayıt 5090'ı gösterdiğine göre makaledeki cümle büyük olasılıkla yanlış; gönderimden önce koşu günlüklerinden denetlenmeli.

## İkinci tur (yardımcı Fable notu, 07.11.2026)

Yürütücü 17 maddenin tamamını kapattığını bildirdi; eşleme ana raporun 10. bölümünde. Yardımcı Fable üçüncü opus açmadığı için ikinci tur çürütücüye yeniden verilmemiştir; nokta denetimi yapılmıştır: bib 36 kayıt, jones2022trained PMLR künyesiyle ve KİMLİKSİZ notuyla eklenmiş, karar kartındaki seçenek listesi ve cevap satırı kaldırılmış, JSON yapısı (meta, adaylar, onerilmeyenler) geçerli. Kalan tek açık: Jones ve ark. (UAI 2022) içeriği yalnız özet düzeyinde doğrulanmıştır, tam metin okunmamıştır; makaleye atıf girmeden önce ilgili şekil ve sayfa gösterilmelidir. Kvinge yüksek tehditten düşük-ortaya indirildiği için "yüksek" tehdidi yalnız Jones taşımaktadır.
