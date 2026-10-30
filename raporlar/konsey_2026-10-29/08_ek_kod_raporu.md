# Ek bloklar için kod raporu: B8, B9, B10 (30.10.2026, ikinci geçiş)

Bu rapor kod-mimar rolündeki opus alt ajanlar tarafından iki geçişte yazılmıştır. İlk geçiş kota kesilmesiyle yarıda kalmış, ikinci geçiş eksikleri tamamlamış ve kodu `ON_KAYIT_EK_B8_B10_2026-10-30.md` belirtimine uydurmuştur. GPU işi başlatılmamış, commit yapılmamıştır. `experiments/c1_c3_transfer_matrix.py`, `experiments/q1_konsey_ayrisim.py`, `hucre_tablosu.json`, `hucre_tablosu_b8.json`, `hucre_tablosu_b9.json`, `ON_KAYIT_2026-10-29.md`, zincir betikleri, `logs/`, `models/q1/konsey` ve `paper/` dosyalarına dokunulmamıştır; iş sonunda özetler yeniden hesaplanmış ve dondurma değerleriyle aynı bulunmuştur (Bölüm 6). Bütün denemeler CPU'da, konteynerde `CUDA_VISIBLE_DEVICES=` ve `nice -n 19` ile yapılmıştır.

En önemli üç nokta şunlardır. Birincisi, ek ön kayıtla koddaki dört uyumsuzluk kapatılmıştır: Mantel permütasyon varsayılanı 9999'dur, F_B10 altı sınamalı tek Holm ailesidir, B8'de IN satırı kestirimine yalnız iki Singh çifti girer ve Liu çifti ayrı scr satırındadır, ImageNet önişleme varsayılanı `BicubicRes256Crop224`'tür. İkincisi, çatal matris betiği varsayılan bayraklarla özgün betikle CIFAR-10'da n = 40'ta hücre hücre ve örnek örnek aynıdır; ek ön kayıt §3'ün istediği n = 200 CPU karşılaştırması yapılamamıştır, çünkü 8 çekirdekli makinenin yük ortalaması B3 eğitimiyle 8 civarındadır, bu karşılaştırma zincir sonrasına GPU'da n = 200 olarak bırakılmıştır ve sapma kaydına yazılmalıdır. Üçüncüsü, 26 indirmenin 26'sı D diskinde `sha256sum -c` ile yeniden doğrulanmış, ImageNetV2'nin açılmış hâli canlı sayımda 1000 sınıf klasörü ve 10.000 dosya vermiştir.

## 1. Yazılan dosyalar

| Dosya | Ne yapar |
|---|---|
| `experiments/q1_ek_transfer_matrix.py` | Özgün matris betiğinin `cp` ile alınmış çatalı. Ek bayraklar: `--eps`, `--alpha` (255 cinsinden), `--batch-size` (varsayılan 50), `--cache-root`, `--cache-f16`, `--dataset imagenetv2`, `--v2-kok`, `--v2-sinif-dosya` (varsayılan 10), `--in-onisleme` (varsayılan `BicubicRes256Crop224`, seçenek `Res256Crop224`), `--onisleme-denetimi`, `--yalniz-denetim`. Önbellek adı yalnız yeni bayraklarda `_e{eps}_a{alpha}`, `_b{batch}`, `_f16` eki alır; önişleme adı önbellek metasında (`onisleme`) bulunur ve farklı önişlemeyle aynı önbelleğe yazma girişimi durdurulur. |
| `experiments/q1_ek_ayrisim.py` | Dondurulmuş çözümleme betiğini SHA-256 denetimiyle (`4bce2c98...b667389`, uyuşmazsa `SystemExit`) `importlib` ile yükleyen sarmalayıcı. `--mod b9` dondurulmuş `main(['--mod','b2',...])` çağrısını yapar ve temiz doğruluk yan dosyası yazar; `--mod b8` ek ön kayıt §5.6'ya göre σ, ρ, ω tablosunu, Singh çiftlerinden Ā^σ_IN'yi, Liu çiftinden ayrı scr satırını, görüntü bootstrap'ını (B = 2000, tohum 20261030) ve betimsel etiketleri üretir; `--mod b10` üç veri kümesinin Mantel çıktılarını F_B10 (altı sınama, Holm) ve §6.3 karar kurallarıyla birleştirir, 9999 dışında permütasyonla üretilmiş girdi varsa `perm_uyarisi` yazar. |
| `experiments/q1_ek_gradyan_kosinus.py` | B10. `gradyan` alt komutu temiz görüntüde doğru etiketli CE kaybının girdi gradyanını alır ve çift başına görüntü kosinüslerini biriktirir; `mantel` alt komutu log τ̄ matrisini dondurulmuş betiğin işlevleriyle kurar, ham Mantel ve ana etkisi çıkarılmış artık Mantel (birincil) ile kovaryatlı kısmi Mantel'i (keşifsel) uygular. Varsayılan 9999 permütasyon, tohum 20261030, p = (1 + #)/(perm + 1). |
| `scripts/ek_indir.py` | WSL'de standart kütüphaneyle indirme, HEAD boyut denetimi, SHA-256 kaydı, sembolik bağ ve güvenli arşiv açma. |
| `scripts/ek_regresyon.sh` | Özgün ile çatalın varsayılan bayraklarla karşılaştırması (`cpu N [onb]` ya da `gpu 200`); `gpu` kipi eğitim süreci varsa durur. |
| `scripts/ek_sahte_v2_smoke.py` | Sahte ImageNetV2 klasörü ve iki rastgele ağırlıklı 1000 sınıflı modelle ImageNetV2 yolunun uçtan uca CPU sınaması. |
| `scripts/ek_kuru_ayristirma.py` | İkinci geçişte eklendi. Gerçek `hucre_tablosu_b9.json` ve `hucre_tablosu_b8.json` takma adlarıyla sahte matris kurar, sarmalayıcıyı `--sinama` kipinde `b9` ve `b8` ile, dondurulmuş betiği B8 tablosuyla `--mod b2` kipinde çağırır. Sayılar sahtedir. |
| `scripts/ek_zincir_komutlari.sh` | Zincir sonrası koşu sırası (Bölüm 5); bekçi denetimleri içerir, kullanıcı tmux'ta başlatır. |
| `tests/test_q1_ek.py` | 21 birim sınaması. İkinci geçişte iki sınama eklendi: varsayılanların ek ön kayıtla uyumu (9999, tohum 20261030, bicubic, IN çiftleri 1 ve 2, scr çifti 3, bootstrap 2000) ve bicubic yükleyicinin `robustbench.data.PREPROCESSINGS['BicubicRes256Crop224']` ile birebir aynı tensör vermesi. |

İkinci geçişteki kod değişiklikleri yalnız şunlardır: `q1_ek_gradyan_kosinus.py`'de `PERM_VARSAYILAN` 5000'den 9999'a ve `--in-onisleme` varsayılanı bicubic'e çekildi; `q1_ek_transfer_matrix.py`'de `--in-onisleme` varsayılanı ve belge metni değişti; `q1_ek_ayrisim.py`'ye `PERM_ON_KAYIT` ve `perm_uyarisi` eklendi. F_B10 ailesi ve B8'in IN/scr ayrımı ilk geçişte zaten ek ön kayda uygun yazılmıştı; ikisi de birim sınamasıyla ve gerçek tablolarla kuru ayrıştırmayla denetlendi.

Özgün betikten bilinçli iki ayrılık ilk geçişteki gibidir ve varsayılan CIFAR-10 davranışını değiştirmez: XCiT hub önbelleği eşlemesi (model, veri kümesi) anahtarlıdır ve ImageNetV2'de normalizasyon eklenmez. Kurulu robustbench kaynağına göre Salman, Engstrom, Wong, Liu ve Mo modelleri normalizasyonu `normalize_model` sarmalayıcısıyla, Peng modeli `NormalizedConfigurableModel` ile içinde taşır; Singh ConvNeXt-T, ConvNeXt-B ve ViT-B ConvStem, Chen2024Data_WRN_50_2 ve ImageNet XCiT'te modülde normalizasyon katmanı yoktur. RobustBench bu modelleri de [0, 1] girdiyle değerlendirdiğinden aynısı yapılmıştır; doğruluğu ön işleme denetiminin temiz doğruluklarıyla görülecektir.

## 2. Sınamalar

| Sınama | Sonuç | Kanıt |
|---|---|---|
| Birim sınamaları (21) | geçti | `results/q1/ek_regresyon/birim_sinamalar.txt` (21 passed); komut `docker exec -w /workspace -e CUDA_VISIBLE_DEVICES= adeb_eval python -m pytest -q -p no:cacheprovider -o addopts="" tests/test_q1_ek.py` |
| Özgün ve çatal, varsayılan bayraklar, CIFAR-10, C1 ResNet s1001 + ViT s2001 + WRN_28_10, n = 40, CPU | geçti | `results/q1/ek_regresyon/cpu_n40/karsilastirma_ozgun_catal.json`: 9 hücre, 9 npz, `BIREBIR: true` |
| Aynı karşılaştırma n = 200, CPU (ek ön kayıt §3) | atlandı | B3 eğitimi CPU'yu dolduruyor (8 çekirdek, yük ortalaması 7,98, 06:36); ilk geçişte n = 200 CPU koşusunun GPU kullanımını %33-57'ye düşürdüğü görülmüştü. Zincir sonrasında `bash scripts/ek_regresyon.sh gpu 200` |
| Gerçek B9 ve B8 hücre tablolarıyla kuru ayrıştırma (sahte matris) | geçti | `results/q1/ek_regresyon/kuru_ayristirma/ozet.json` (`GECTI: true`) |
| Üç betiğin `--help` çıktısı (konteyner, CPU) | geçti | `results/q1/ek_regresyon/denetim_2026-10-30.txt`: dört çağrının dördü de rc = 0 |
| ImageNetV2 yolu uçtan uca, sahte veri, iki rastgele model, n = 8, bicubic varsayılan | geçti | `results/q1/ek_regresyon/v2_sahte/ozet.json` (`on_isleme: BicubicRes256Crop224`), taze ve float16 önbellekli koşu `BIREBIR: true` |
| İndirmelerin SHA-256 doğrulaması | geçti | `results/q1/ek_regresyon/indirme_sha256_denetim_2026-10-30.txt`: 26 dosyanın 26'sı OK |
| ImageNetV2 klasör adlarının ImageNet sınıf indeksi olması | dolaylı geçti | Bölüm 4 |
| Gerçek RobustBench ImageNet modelleriyle ön işleme denetimi ve matris | atlandı | Konteyner `/mnt/d`'yi görmüyor; zincir sonrası ilk adım |
| B8, B9, B10 sarmalayıcılarının gerçek matrislerle koşusu | atlandı | Matrisler yok |

n = 40 karşılaştırmasındaki çatal çıktısı (06:19-06:25) ikinci geçişteki varsayılan değişikliklerinden önce üretilmiştir. Sonraki değişiklikler yalnız `--in-onisleme` varsayılanını ve belge metnini etkiler; bu bayrak yalnız `--dataset imagenetv2` yolunda okunur, CIFAR-10 hücre metasına ve önbellek adına girmez. n = 200 GPU karşılaştırması güncel sürümle yapılacağından bu fark orada da kapanır.

Kuru ayrıştırmanın ayrıntısı şöyledir. Dondurulmuş betik `4bce2c98...b667389` özetiyle yüklenmiş, B9'da 15 model, 7 üyeli birincil ve 2 üyeli ikincil panel kurulmuş, dondurulmuş F_B2 üç sınamayla (K-a, K-b, K-c) üretilmiş ve sarmalayıcı 15 modelin temiz doğruluğunu yazmıştır. B8'de 14 model ve 6 üyeli P8 kurulmuş, IN satırına 1 ve 2 numaralı çiftler (Singh ConvNeXt-T/ViT-S-CvSt, ConvNeXt-B/ViT-B-CvSt), scr satırına 3 numaralı çift (Liu ConvNeXt-B/Swin-B) girmiş, beklenti eşikleri −0,10 ve −0,20, bootstrap tohumu 20261030 çıkmıştır; dondurulmuş `--mod b2` çağrısı B8 tablosuyla da hatasız çalışmıştır.

## 3. İndirme durumu

Toplam 26 öğe indirilmiştir ve 4.646.547.929 bayt tutmaktadır; başarısız öğe yoktur, hiçbir Google Drive dosyası kotaya takılmamıştır (`/mnt/d/adeb_sci_1_veri/_indirme/indirmeler.json`, `ilerleme.log`). Her dosyanın boyutu HEAD değerine eşittir (`_indirme/boyutlar_head.json`). İkinci geçişte `cd /mnt/d/adeb_sci_1_veri && sha256sum -c indirme_sha256.txt` 26 dosyanın hepsinde OK vermiştir (51 s).

ImageNetV2 arşivinin SHA-256'sı `f0c37fdf925916b19ea1323cd9a2208cdb6959ba2c32eef2a7fc393835c9ca7c`, boyutu 1.264.079.360 bayttır ve Hugging Face'in LFS özetiyle aynıdır. Hugging Face'teki `.tar.gz` adlı dosya sıkıştırılmamış POSIX tar'dır; açıcı `r:*` kipine çevrilmiştir. Açılmış küme `/mnt/d/adeb_sci_1_veri/data/imagenetv2/imagenetv2-matched-frequency-format-val/` altındadır. İkinci geçişteki canlı sayım: 1000 sınıf klasörü, adlar 0-999 eksiksiz, her klasörde 10 dosya, toplam 10.000; kök altında başka öğe yoktur (`results/q1/ek_regresyon/denetim_2026-10-30.txt`).

Depodaki bağlar şöyledir. `data/imagenetv2` D'deki klasöre sembolik bağdır ve WSL'de çözülür. `models/robustbench_zoo/imagenet` ve `models/robustbench_zoo/cifar100` gerçek klasörlerdir, içlerindeki `Linf/<ad>.pt` (XCiT için `.pth.tar`) dosyaları tek tek D'ye bağdır: 25 bağın 25'i WSL'de çözülür. `cifar100/Linf/Pang2022Robustness_WRN28_10.pt` daha önceden depoda bulunan sıradan dosyadır ve yeniden indirilmemiştir; böylece CIFAR-100 klasöründe 11 model bulunur. Bağlar konteynerde yeniden kurulumdan önce kırıktır.

| Grup | Model | Bayt | SHA-256 (ilk 16) |
|---|---|---|---|
| B8 | Singh2023Revisiting_ConvNeXt-T-ConvStem | 114.572.173 | ac231a29e1e5b2a7 |
| B8 | Singh2023Revisiting_ViT-S-ConvStem | 91.166.417 | 1b7d520ada671842 |
| B8 | Singh2023Revisiting_ConvNeXt-B-ConvStem | 355.132.063 | 376af337b449bc87 |
| B8 | Singh2023Revisiting_ViT-B-ConvStem | 348.642.911 | 73d0e0618cafaeca |
| B8 | Liu2023Comprehensive_ConvNeXt-B | 354.496.687 | e962df7de19b6bf5 |
| B8 | Liu2023Comprehensive_Swin-B | 352.787.535 | af49b8c6f8ac52c4 |
| B8 | Mo2022When_ViT-B | 346.330.174 | b12f310872c88730 |
| B8 | Salman2020Do_R18 | 46.836.793 | a94c5130284c43d2 |
| B8 | Salman2020Do_R50 | 102.546.991 | 1835a5bbe5e31ef3 |
| B8 | Salman2020Do_50_2 | 275.912.303 | 96e9c755874d701a |
| B8 | Engstrom2019Robustness | 102.529.618 | f26eb0ce4dab9ed4 |
| B8 | Chen2024Data_WRN_50_2 | 275.913.601 | ffc0dc0d50fbf6ea |
| B8 | Peng2023Robust | 417.089.026 | 5acdc6f6a3083e98 |
| B8 | Debenedetti2022Light_XCiT-S12 (GitHub sürümü) | 105.172.083 | aa4ccf769eff2965 |
| B8 yedek | Wong2020Fast | 102.546.991 | 1224019bf5ccaa0a |
| B9 | Rice2020Overfitting | 44.922.584 | 0e4d0635b5abfb21 |
| B9 | Rade2021Helper_R18_ddpm | 50.445.746 | df4e03ec48af3928 |
| B9 | Addepalli2022Efficient_RN18 | 44.963.257 | aafda6c19381b62f |
| B9 | Sehwag2021Proxy | 185.019.203 | e5a948084ee7e84d |
| B9 | Wang2023Better_WRN-28-10 | 146.269.624 | f375fc23f485f99c |
| B9 | Jia2022LAS-AT_34_10 | 193.475.477 | 122582e46c2f155a |
| B9 | Debenedetti2022Light_XCiT-S12 (GitHub sürümü) | 103.786.099 | 85e52ccae157db0d |
| B9 | Hendrycks2019Using | 146.249.648 | 598ea1c374d6e639 |
| B9 yedek | Chen2021LTD_WRN34_10 | 193.470.987 | 71a8997930b4f003 |
| B9 yedek | Cui2023Decoupled_WRN-28-10 | 146.269.938 | fd39303c8c40db53 |

Salman2020Do_R50 ile Wong2020Fast'in boyutu aynıdır, SHA-256'ları farklıdır; iki ayrı kontrol noktasıdır. Tam özetler `/mnt/d/adeb_sci_1_veri/indirme_sha256.txt` dosyasındadır.

## 4. Doğrulamalar

Zhang ve ark., arXiv 2307.07873, ilk geçişte export.arxiv.org API ile doğrulanmıştır: başlık "Why Does Little Robustness Help? A Further Step Towards Understanding Adversarial Transferability", DOI 10.1109/SP54263.2024.00010; öncül B10 betiğinin belgesinde anılmıştır. Liu çiftinin tarif ortaklığı ve başlatma durumu ek ön kayıt §5.4'te ARES yapılandırmalarıyla ele alınmış, çift scr satırına alınmıştır; RobustBench `model_info` dosyalarında Liu, Singh ve Mo modellerinin `additional_data` alanı `false`'tur.

ImageNetV2'nin README'si klasör adlarıyla sınıf indeksi arasındaki eşlemeyi yazmaz; yalnız `ImageFolder` ile yüklenmesini söyler (raw.githubusercontent.com/modestyachts/ImageNetV2/master/README.md, 30.10.2026). Aynı grubun resmî yükleyicisi `ImageNetV2_pytorch/imagenetv2_pytorch/ImageNetV2_dataset.py` etiketi `int(self.fnames[i].parent.name)` ile, yani klasör adının tamsayı değeri olarak alır ve arşivi aynı Hugging Face adresinden indirir (30.10.2026'da okundu). Çatal betiğin `v2_secim` işlevi de etiketi `int(p.name)` ile alır ve klasörleri sayısal sıraya dizer; bu yüzden `ImageFolder`'ın sözlük sırası ("0", "1", "10", "100") ile oluşacak kaydırma hatası bu yolda yoktur. Eşlemenin gerçek modellerde doğruluğu ek ön kayıt §5.1'deki gibi ön işleme denetiminin temiz doğruluklarıyla dolaylı olarak sınanacaktır.

## 5. Zincir sonrası koşu

Koşu sırası ek ön kayıt §10 ile aynıdır ve `scripts/ek_zincir_komutlari.sh` dosyasındadır. Betik her adımdan önce eğitim ya da zincir süreci olup olmadığına (WSL'den `pgrep` konteyner süreçlerini görmektedir, denendi), konteynerin `/mnt/d`'yi görüp görmediğine, boş VRAM'in 12 GB'ı aşıp aşmadığına ve özgün matris betiği ile dondurulmuş çözümleme betiğinin SHA-256'larına bakar, biri tutmazsa durur. Günlükler `results/q1/ek_loglar/` altına yazılır. Ön koşul, konteynerin `07_disk_D_plani.md` §4'teki tarifle `-v /mnt/d/adeb_sci_1_veri:/mnt/d/adeb_sci_1_veri` bağlamasıyla yeniden kurulmuş olmasıdır.

```bash
cd /home/firat/projects/adeb_sci_1
# 1) regresyon (n = 200, GPU, onbellekli ikinci karsilastirma dahil) ve B8 on isleme denetimi
bash scripts/ek_zincir_komutlari.sh regresyon b8denetim
#    results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json ek on kayit §5.5 kuralina gore okunur,
#    eleme varsa betikteki IN14 listesi T gorulmeden duzeltilir ve sapma kaydina yazilir
# 2) B9 (ozgun betik), B8 (catal, BicubicRes256Crop224, eps 4/255, alfa 1/255, float32 onbellek), B10, cozumlemeler
bash scripts/ek_zincir_komutlari.sh b9 b8 b10 cozumleme
```

Önbellekler `/mnt/d/adeb_sci_1_veri/onbellek/b9_c100` ve `/mnt/d/adeb_sci_1_veri/onbellek/b8_imagenetv2` (14 × 2000 × 3 × 224 × 224 × 4 bayt, yaklaşık 16,9 GB) altına yazılır. Çıktılar `results/q1/konsey_b9_c100/`, `results/q1/konsey_b8_imagenetv2/` ve `results/q1/konsey_b10_gradyan/` altındadır. B10'un CIFAR-10 kolu `results/q1/konsey_b4_matris` klasörünü okur; zincir betiğindeki B4 komutuyla aynı 20 model ve takma adlar kullanılmıştır.

## 6. Açık noktalar

1. Ek ön kayıt §3'ün "n = 200, CPU" regresyonu yapılamadı; n = 40 CPU geçti, n = 200 GPU karşılaştırması zincir sonrası ilk adımdır. Bu durum sapma kaydına (`results/q1_research/ONKAYIT_SAPMALAR.md`, "Ek B8-B10") yazılmalıdır.
2. Ek ön kaydın gövdesindeki iki betimleyici cümle artık eski varsayılanları anlatıyor: §5.2 "betiğin varsayılanı (bilinear Res256Crop224) B8'de kullanılmaz" ve §6.2 "betiğin varsayılanı 5000 kullanılmaz". Koşu komutları iki bayrağı da açıkça verdiği için hesapta fark yoktur. Gövdeyi değiştirmek özetini (`d14d6915...cd197c33`, bugün yeniden üretildi) bozacağından gövdenin olduğu gibi bırakılması ve varsayılanların eke uydurulduğunun kod eki kaydında belirtilmesi önerilir; §3 bu uydurmayı zaten öngörür.
3. Liu satırının betimsel etiketinde "ihmal edilebilir" bandı ±0,10 (δ) olarak korunmuş, yalnız beklenti eşiği −0,20 alınmıştır. §5.6'daki "aynı kuralla, −0,10 yerine −0,20 eşiğiyle" ifadesi bu okumayla uygulanmıştır; ana oturum farklı okuyorsa `b8_etiket` işlevinde tek satırlık değişikliktir.
4. `models/robustbench_zoo/` git'te izlenmiyor ve `.gitignore`'da da değil; içinde D'ye işaret eden sembolik bağlar var. Commit sırasında bu klasörün eklenmemesi gerekir. `data/` yok sayılıyor.
5. `scripts/konsey_tam_zincir.sh` git'te izlenmeyen dosya olarak görünüyor (`git status`: `??`); bugünkü özeti `65fb45f5db0d4b5aa064a86e49269133a767827c44847dbd7f6b73427aa0c16f`'dir. B4/B5'in kanıt zinciri için bu özetin bir yere kaydedilmesi düşünülebilir.
6. Kod eki (ek ön kayıt §12 ve Dondurma eki (h)) için ilk koşudan önceki özetler aşağıdadır. Dondurulmuş dosyaların özetleri dondurma değerleriyle aynıdır: `c1_c3_transfer_matrix.py` `f25d9062...86140b7`, `q1_konsey_ayrisim.py` `4bce2c98...b667389`, `hucre_tablosu.json` `2a891331...e5500`, `hucre_tablosu_b8.json` `4afa5fbc...a388d`, `hucre_tablosu_b9.json` `be778f42...dde3bd`; ek ön kayıt gövdesi `d14d6915...cd197c33`.

```text
43794a265886f86e88d0c86842b62f2c33d8316adcf2ce3661a6a561bcbd943a  experiments/q1_ek_transfer_matrix.py
d264c4e584fcfb3c0e3dd9517cfe2cea4ea1fe564117c88459e2b9721027a641  experiments/q1_ek_ayrisim.py
c82a66d196c38f23d688f610caf6ffceab0c01e7ebfa68e5358f832014043eed  experiments/q1_ek_gradyan_kosinus.py
0319542be13e2d0b72cc82901a51d027416f4eb361cf9571df89d5936d9ebe75  scripts/ek_indir.py
7da6eba467254c85ae53a1be6af8d247e07d94184e63aa82c9affc75947da6ce  scripts/ek_regresyon.sh
8026a4bac82f9ef330b0ef0bef3f6e16086d3da978cffc5ebae67fe7608a9557  scripts/ek_zincir_komutlari.sh
e79ef6144ad7885124b4933d321dd4faa5a6f17fc4ffa9bc39f42dfa8c8528a5  scripts/ek_sahte_v2_smoke.py
508eac1b14a885e172c0938b7f664a5423bb3113cff4f8ad669e28f4afde9b58  scripts/ek_kuru_ayristirma.py
e6517f8d6ce11670b8e3188d66dca0d32cbd471912a3fe6246223344ba4fb240  tests/test_q1_ek.py
```
