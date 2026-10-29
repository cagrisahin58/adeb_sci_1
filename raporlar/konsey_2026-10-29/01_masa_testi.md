# Masa testi: kaynak ve hedef ana etkileri, aileler arası etkileşim ve simetri

Betik `experiments/q1_etkilesim_simetri_masa.py`, çıktı `results/q1/etkilesim_simetri_masa.json` (aşağıda `J`). Yeni ölçüm yapılmamış, GPU kullanılmamıştır. Havuz oranları `havuz_protokoller.json` ile en çok 3,1e-6 puan farkla örtüşmektedir (`J.sonuc.havuz_cifar10.kontrol_max_mutlak_fark_havuz_protokoller_json`). Mahmood ve ark. 2021 (arXiv:2104.02610) dış veridir; makaleye yalnız dış karşılaştırma olarak girebilir.

## 1. Yönlü aile terimi tahmin edilemez; bu bir bulgu değil cebirdir

Her hücrede 1[s∈C, t∈V] − 1[s∈V, t∈C] = 1[t∈V] − 1[s∈V] eşitliği geçerlidir ve sağ taraf ana etkilerin doğrusal birleşimidir. Bu nedenle M2'nin tasarım matrisi M1 ile aynı ranktadır (havuzda ve Mahmood'da 16 ile 16; `J...nokta.M2.rank`, `rank_M1`), uydurulan değerler en çok 1,1e-13 farklıdır ve γ_CV − γ_VC hiçbir matriste, hiçbir protokolde ve hiçbir ölçekte tahmin edilemez (`gamma_CV_eksi_gamma_VC_tahmin_edilebilir = false`, sayısal özdeşlik kontrolü 0,0). Model sayısı artırılarak da çözülmez. Aynı cebirden iki sonuç daha çıkmaktadır. Tam bir matriste aile düzeyi asimetri (CV ortalaması eksi VC ortalaması), kaynak etkilerinin aile ortalaması farkı ile hedef etkilerinin aile ortalaması farkının toplamına özdeş olarak eşittir (kontrol artığı ≤ 3e-14, `aile_asimetrisi.kontrol_A_eksi_kaynak_eksi_hedef`). Ayrıca kaynak ile hedef payları arasındaki bölüşüm, yönlü bir aile terimi d kabul edildiğinde her iki payı d kadar kaydıran bir ayar serbestliği taşır; yani “asimetri kaynak etkisiyle taşınır” okuması, yönlü aile terimi olmadığı varsayımı altında tanımlıdır ve bu varsayım dönüşüm matrislerinden sınanamaz.

H* önermesinin ikinci yarısı (“asimetri yalnız ana etkilerle belirlenir”) bu yüzden aile düzeyinde tanım gereği doğrudur ve makalede ampirik bulgu gibi sunulamaz. Sınanabilir içerik üç yerde kalır: simetrik aileler arası ceza (M1), üç ya da daha çok cinsle tanımlanan döngüsel yönlü terim ve çift düzeyindeki artık asimetri.

## 2. Simetrik ceza: havuzda yok, Mahmood'da güçlü

| Matris, protokol, ölçek | R² M0 | R² M1 | γ (M1) | ΔR² etiket permütasyonu p |
|---|---|---|---|---|
| Havuz, ham, oran | 0,917 | 0,917 | −0,60 | 0,50 (28 etiketleme) |
| Havuz, hedef-doğru, oran | 0,896 | 0,897 | −0,81 | 0,46 |
| Havuz, hedef-doğru, logit | 0,978 | 0,978 | −0,044 | 0,61 |
| Havuz, her-ikisi-doğru, oran | 0,874 | 0,875 | −0,80 | 0,46 |
| Mahmood C10, hibrit V, oran | 0,368 | 0,555 | −22,8 | 0,029 (70) |
| Mahmood C10, hibrit C, oran | 0,368 | 0,591 | −27,3 | 0,018 (56) |
| Mahmood C100, hibrit V, oran | 0,451 | 0,659 | −23,3 | 0,029 (70) |
| Mahmood C100, hibrit V, logit | 0,520 | 0,666 | −1,05 | 0,029 (70) |

Kaynak: `J.sonuc.havuz_cifar10.protokoller.<p>.<ölçek>.nokta.M0.R2`, `.M1.R2`, `.M1.gamma`, `.aile_etiket_permutasyonu.dR2`; Mahmood için `J.sonuc.mahmood2021.<ds>.<atama>.<ölçek>`. Mahmood'daki p değerleri ulaşılabilir en küçük değerdedir (iki yönlü 2/70, 1/56).

Havuzda γ'nın örnek bootstrap aralığı sıfırı dışlasa da (ham oran −0,74 ile −0,46, `ornek_bootstrap.gamma_M1`) açıklanan varyans artışı 0,001'i aşmamaktadır ve iki dönüştürücünün yerine rastgele iki model konduğunda benzer ya da daha büyük değerler çıkmaktadır. γ, iki dönüştürücü arasındaki yalnız iki hücreye dayanır; dönüştürücülerden biri bırakıldığında tahmin edilemez hale gelir (jackknife'ta 8 bırakmanın 6'sı geçerli). Mahmood'da ise aileler arası ceza 23 ile 27 puandır ve M0'ın düşük R²'sinin önemli bölümünü kapatır. Bu karşıtlık, çekişmeli eğitilmiş havuzun aile blok yapısı taşımadığını, standart eğitilmiş ve ön eğitimli Mahmood modellerinin taşıdığını düşündürmektedir; ancak iki havuz eğitim tarifi, ön eğitim ve model ölçeği bakımından da farklıdır, dolayısıyla bu yalnız keşifsel bir gözlemdir.

## 3. Sınanabilen tek yönlü terim: döngüsel dolaşım

Mahmood'un üç cinsiyle (ViT, BiT, ResNet; hibrit ViT içinde) ViT→BiT→ResNet→ViT yönünde bir dolaşım terimi κ tahmin edilebilir (rank 17, parametre 17). CIFAR-10 oran ölçeğinde κ = 3,81 puan (binom bootstrap %95 GA 3,44 ile 4,16; 420 etiketlemede p = 0,0095), logit ölçeğinde 0,113 (p = 0,024); CIFAR-100 oran ölçeğinde 2,80 (p = 0,0095), logit ölçeğinde 0,013 (GA −0,022 ile 0,047; p = 0,81). R² katkısı 0,014'ü geçmemektedir (`J.sonuc.mahmood2021.<ds>.uc_cins_dolasim`). Yönlü bir cins etkisi küçük ölçüde vardır, fakat ölçeğe bağlıdır ve aynı-cins teriminin (γ ≈ 40 puan) yanında ikincildir. Binom bootstrap m = 1000 ve hücre bağımsızlığı varsayımına dayanır, yaklaşıktır.

## 4. Ana etkiler çift asimetrisini iyi öngörür, ama bu bağımsız bir kanıt sayılmaz

Çift bırakmalı (LOPO) öngörü becerisi, sıfır öngörüsüne göre, havuzda 0,84 ile 0,99, Mahmood'da 0,82 ile 0,92 arasındadır (`LOPO_cift_birak_M0.beceri_1_eksi_SSE_bolu_SSsifir`). Tam 8×8 tasarımda LOPO hatası tam örneklem artık asimetrisinin sabit bir katıdır (K = 8 için 4/3; ham oranda aileler arası 2,928/2,196 ve aile içi 5,546/4,159). Bu yüzden aileler arası çiftlerde işaretli LOPO hatasının ortalaması özdeş olarak sıfırdır ve LOPO dış örneklem sınaması olarak sunulamaz. Bir modelin bütün aileler arası hücreleri dışarıda bırakıldığında (LMCO) beceri havuzda 0,92 ile 0,996, Mahmood'da 0,75 ile 0,93'tür. Görev metnindeki literal “modeli tamamen bırak” sınaması tanımlanamaz, çünkü bırakılan modelin kendi ana etkileri başka hücreden kestirilemez.

Artık çift asimetrisinin RMS değeri, örnek bootstrap SD'sinin RMS değerinin havuz oran ölçeğinde 8,5 ile 18,7 katı, logit ölçeğinde 1,5 ile 13,3 katıdır (`artik_asimetri_heterojenligi`). Ana etkilerin bıraktığı yapı ölçüm gürültüsü değildir; en büyük artıklar aile içi çiftlerde ve ResNet18_AT ile Standard_WRN28_10 çevresinde toplanmaktadır (LOPO model RMSE ham oranda 7,81 ve 8,46 puan, öbürleri 1,9 ile 2,9).

## 5. Ana etkiler aile niteliği değil, model niteliğidir (havuz)

| Havuz, oran | Aile asimetrisi A | Kaynak payı | Hedef payı | Kaynak payı jackknife aralığı | Perm. p (kaynak) |
|---|---|---|---|---|---|
| ham | 3,91 | 1,20 | 2,71 | −2,13 ile 4,93 | 0,86 |
| hedef-doğru | −1,42 | 1,21 | −2,63 | −2,47 ile 5,42 | 0,86 |
| her-ikisi-doğru | 0,01 | 2,04 | −2,03 | −2,98 ile 7,58 | 0,96 |
| başarılı-kaynak | 1,97 | 6,60 | −4,63 | −12,28 ile 26,30 | 0,82 |

Kaynak: `aile_asimetrisi`, `model_jackknife.ozet.kaynak_payi`, `aile_etiket_permutasyonu.kaynak_payi`. Aile kaynak payının işareti hangi dönüştürücünün bırakıldığına göre dönmektedir (ham oranda ViT_Tiny_AT bırakılınca −2,13, XCiT bırakılınca 4,93). Nedeni M0 kaynak etkilerinde görülür: ViT_Tiny_AT −4,41, Debenedetti2022_XCiT_S12 2,61, Standard_WRN28_10 −12,47 (`nokta.M0.kaynak_etkisi`, ham). Hedef-doğru protokolünde aile asimetrisi −1,42 iken aynı havuzdaki ResNet18_AT→ViT_Tiny_AT asimetrisi 4,81'dir (`nokta.cift_asimetrileri`). Logit ölçeğinde hedef-doğru kaynak payı −0,163'e döner. Örnek bootstrap belirsizliği model örneklemesinin yanında küçüktür (ham kaynak payı için bootstrap SD yaklaşık 0,07, jackknife SE 5,08).

Mahmood'da kaynak payı büyüktür ve işareti tersinedir: CIFAR-10 hibrit V atamasında −25,05 puan (dönüştürücüler daha güçlü kaynak; p = 0,029, en küçük ulaşılabilir değer). Hibrit CNN sayıldığında p 0,107'ye çıkar. 3×3 matrislerde tek dönüştürücü bulunduğundan M0, M1 ve M2 rankı 5'tir; γ tahmin edilemez ve “aile” ayrıştırması ViT_Tiny_AT'nin tek model etkisidir (tohumlar arası SD küçüktür, örneğin CIFAR-10 hedef-doğru kaynak payı 4,90 ± 0,22; `J.sonuc.uc_kare`).

## 6. H* için hüküm

H*'ın “asimetri yalnız ana etkilerle belirlenir” kısmı aile düzeyinde cebirsel olarak her zaman doğrudur ve çürütülemez olduğu için iddia olarak kullanılamaz. “Aileler arası ceza simetriktir” kısmı iki aileyle sınanamaz; üç cinsle sınanabilen döngüsel terim Mahmood'da küçük ve ölçeğe bağlıdır. Elde kalan sağlam içerik şudur: (i) çift asimetrisi büyük ölçüde model düzeyindeki kaynak ve hedef etkileriyle açıklanır; (ii) bu etkiler, çekişmeli eğitilmiş havuzda mimari ailesine bağlanamaz; (iii) aile düzeyindeki işaret havuzdan havuza (bizim havuz, Mahmood) ve ölçekten ölçeğe değişmektedir. Makalenin “kaynak etkisi okuması” model düzeyinde savunulabilir, aile düzeyinde savunulamaz; bu, tez tarafının 6 Ekim sonucuyla çelişmez, onu genelleştirir.

## 7. Güç sınırları (post-hoc güç hesabı yapılmamıştır)

Havuzda yalnız iki dönüştürücü vardır. Etiket permütasyonunda ulaşılabilir en küçük p 1/28 ≈ 0,036'dır; 0,01 düzeyinde hiçbir aile etkisi hiçbir veride gösterilemez. Dönüştürücülerden biri bırakıldığında γ tanımsızlaşır, aile kaynak payı tek modele indirgenir. Mahmood'da en küçük p 2/70 ve 1/56'dır, dış veride ise örnek düzeyi kayıt yoktur. Ayrım gücünü belirleyen etken görüntü sayısı değil aile başına model sayısıdır; görüntü bootstrap aralıkları dar, model jackknife aralıkları bir büyüklük mertebesi geniştir.
