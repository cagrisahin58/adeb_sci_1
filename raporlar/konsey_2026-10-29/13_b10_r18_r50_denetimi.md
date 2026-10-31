# B10 ImageNetV2 panelinde IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 kosinüsünün GPU denetimi

Tarih: 31.10.2026. Hazırlayan: araştırma kodu uygulayıcısı (opus alt ajan). Bu rapor `11_sonuc_b8_b10.md` §6'da şüphe olarak kaydedilen ve §8'de makaleden önce yapılması istenen kısa GPU denetiminin sonucudur. `results/q1` altındaki hiçbir dosya değiştirilmemiş, oraya yeni dosya yazılmamış, B10 yeniden koşulmamıştır. Bütün ara çıktılar `arsiv/b2_yardimci/_b10_denetim_cikti/` altındadır.

Varılan karar şudur: R18 ile R50 arasındaki 0,0034'lük ortalama kosinüs bir kod, yükleme ya da önbellek yapaylığı değildir, B10'un tanımladığı niceliğin doğru hesaplanmış gerçek değeridir. Değer sıfırdan bağımsız bir betikle yeniden hesaplandığında ilk 100 görüntüde kayıtla görüntü düzeyinde örtüşmüş (en büyük mutlak fark 5×10⁻⁶), model nesneleri, kontrol noktası dosyaları ve veri listesi ayrı ayrı doğrulanmıştır. Yakın sıfır değerin nedeni iki modelin gradyanlarının ilişkisiz olması değil, frekans bantları arasında bir sönümlenmedir: iki gradyan alçak frekanslarda belirgin biçimde hizalıdır (8×8 ortalama havuzdan sonra kosinüs 0,495), ama gradyan enerjisinin yaklaşık dörtte üçünü taşıyan en yüksek frekans bandında ters yönlüdür ve bu bandın katkısı (−0,091) alçak bantların toplam katkısını (+0,095) neredeyse tam olarak götürmektedir. Yeniden koşu gerekmez.

## 1. B10'da c_ij'nin hesaplanış biçimi

`experiments/q1_ek_gradyan_kosinus.py` (sha256 `c82a66d1…3eed`; kayıttaki `betik_sha256` ile aynı, `denetim.json` alanı `b10_betik_ayni` = true) `gradyan` alt komutunda modelleri `q1_ek_transfer_matrix.py`'nin `load_wrn` yükleyicisiyle RobustBench'ten (`models/robustbench_zoo`) yükler, eval kipine alır ve parametrelerin gradyanını kapatır. ImageNetV2 için `v2_loaders(kok, 2000, 25, "BicubicRes256Crop224", 10)` her sınıf klasörünün sıralı ilk iki dosyasını (sıra: sınıf, ad) bütünüyle belleğe yükleyip karıştırmasız bir DataLoader kurar; `_iter_batches` ilk n örneği verir. Her yığında her model için `girdi_gradyani` doğru etiketli çapraz entropi kaybının (`reduction="sum"`) [0,1] piksel uzayındaki girdiye göre gradyanını alır; normalizasyon RobustBench nesnesinin içindeki `ImageNormalizer` katmanında olduğu için gradyan normalizasyonun içinden geçer. `cift_kosinus` K modelin gradyan yığınından `combinations(range(K), 2)` sırasıyla çift başına görüntü kosinüslerini hesaplar. Gradyanlar saklanmaz, gradyan önbelleği yoktur; B8 matrisinin çekişmeli örnek önbelleği (`--cache-adv`) B10'da kullanılmaz. `kosinus.npz` görüntü × çift kosinüsü (float16, 2000×91), model × görüntü gradyan normunu (14×2000) ve temiz doğru maskesini tutar; `kosinus_ozet.json`'daki `c_tum[i][j]` bu sütunun `nanmean`'idir, model sırası `modeller` alanındadır (R18 sıra 0, R50 sıra 1, çift sütunu 0).

Zincirdeki çağrı `scripts/ek_zincir_komutlari.sh` içindeki `adim_b10` işlevindedir:

```bash
python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset imagenetv2 --v2-kok data/imagenetv2 \
  --in-onisleme BicubicRes256Crop224 --n-samples 2000 --batch-size 25 $IN14 --cikti $B10D/imagenetv2
```

`$IN14`, `--rb-model Salman2020Do_R18:IN_Salman2020Do_R18 --rb-model Salman2020Do_R50:IN_Salman2020Do_R50 ...` biçiminde on dört RobustBench modelini verir. RobustBench'in model tanımında (`robustbench/model_zoo/imagenet.py`) iki model de `normalize_model(pt_models.resnet18()/resnet50(), mu, sigma)` biçiminde torchvision ResNet'idir ve ayrı Google Drive kimliklerinden gelir.

## 2. Denetim betiği ve koşu

Denetim betiği `arsiv/b2_yardimci/_b10_r18_r50_denetim.py`'dir. B10 betiğini kopyalamaz, `importlib` ile modül olarak yükler ve onun `_modul` yükleyicisiyle `q1_ek_transfer_matrix`'i alır; zincirle aynı sırayı izler (`set_seed(42)`, `load_wrn(device, dataset="imagenetv2", rb_name=...)`, `v2_loaders("data/imagenetv2", 2000, 25, "BicubicRes256Crop224", 10)`, `_iter_batches`, `girdi_gradyani`, `cift_kosinus`). 2000'lik liste kurulduktan sonra ilk 100 görüntü (sınıf 0-49, sınıf başına iki dosya) işlenmiştir. Altı model yüklenmiştir: R18, R50, Salman2020Do_50_2, Engstrom2019Robustness, Singh ConvNeXt-T-ConvStem ve Singh ConvNeXt-B-ConvStem. Kayıtlı değerleri okuyan ikinci yardımcı `arsiv/b2_yardimci/_b10_kayit_oku.py`'dir (salt okur, GPU kullanmaz).

```bash
wsl.exe -d Ubuntu-22.04 -- bash -lc "cd /home/firat/projects/adeb_sci_1 && \
  docker exec -w /workspace adeb_eval python -B arsiv/b2_yardimci/_b10_r18_r50_denetim.py \
  > arsiv/b2_yardimci/_b10_denetim_cikti/kosu.log 2>&1"
# real 1m23.713s; rc=0
docker exec -w /workspace adeb_eval python -B arsiv/b2_yardimci/_b10_kayit_oku.py \
  arsiv/b2_yardimci/_b10_denetim_cikti/kayit.json
```

Koşu RTX 5090'da yapılmıştır (`denetim.json` `cihaz`), komşu konteynerin kullandığı yaklaşık 3 GB'a dokunulmamıştır. Gradyan bölümü 14,0 s sürmüştür (`gpu_gradyan_s`); betiğin toplam süresi 80,6 s'dir (`toplam_s`), bunun 49,3 s'si 2000 görüntünün işlemcide çözülmesidir (`veri.yukleme_s`). GPU'nun meşgul olduğu süre bir dakikanın altındadır.

## 3. Yeniden hesaplanan ve kayıtlı değerler

Veri listesi zincirdekiyle aynıdır. Kurulan listenin özeti `25db498b…d1a8`'dir; bu değer `kosinus_ozet.json`'daki `imagenetv2_liste_sha256` ve B8 matris manifestinin (`results/q1/konsey_b8_imagenetv2/matris/imagenetv2_manifest.json`) `liste_sha256` alanıyla aynıdır, ilk 100 dosya yolu da manifestle birebir örtüşür (`denetim.json` `veri.liste_ayni`, `veri.ilk100_dosyalar_b8_manifestle_ayni`; ilk ve son dosya `0/58fbc3e7….jpeg` ve `49/19f22eec….jpeg`). `kosinus.npz` görüntü düzeyinde değer sakladığı için karşılaştırma aynı 100 görüntü üzerinde yapılmıştır.

| Çift | Yeni, 100 görüntü ort. (SD) | Kayıt, aynı 100 görüntü ort. (SD) | Kayıt, 2000 ort. (`c_tum`) | Görüntü düzeyi en büyük mutlak fark |
|---|---|---|---|---|
| R18, R50 | 0,00419 (0,00222) | 0,00419 (0,00222) | 0,00345 | 0,000005 |
| R18, Salman2020Do_50_2 | 0,18548 (0,09558) | 0,18548 (0,09558) | 0,17543 | 0,000116 |
| R50, Engstrom2019Robustness | 0,25499 (0,09458) | 0,25500 (0,09458) | 0,24007 | 0,000120 |
| Singh ConvNeXt-T-CvSt, Singh ConvNeXt-B-CvSt | 0,53393 (0,14851) | 0,53393 (0,14852) | 0,47230 | 0,000244 |

Kaynak: `arsiv/b2_yardimci/_b10_denetim_cikti/denetim.json`, `karsilastirma` alanı (`yeni_ort100`, `yeni_sd100`, `kayit_ort100`, `kayit_sd100`, `kayit_c_tum`, `goruntu_maks_mutlak_fark`). Farklar kaydın float16 saklanmasından beklenen düzeydedir. Gradyan normları da kayıtla aynıdır (altı modelin hepsinde en büyük göreli fark 1×10⁻⁷; `norm_ve_dogruluk.*.norm_maks_goreli_fark`); 100 görüntüde R18'in ortalama normu 1,00289, R50'ninki 1,06701'dir. Yeni hesapta R18-R50 kosinüsü 100 görüntünün hepsinde pozitiftir (en küçük 0,0012, en büyük 0,01567; `yeni_min`, `yeni_maks`).

## 4. R18-R50 çifti için teşhis

Model nesneleri birbirinden farklıdır ve beklenen mimarilerdir. R18 nesnesi 11.689.512 parametreli, `layer1`'de 2 bloklu, `fc` girdisi 512 olan bir ResNet; R50 nesnesi 25.557.032 parametreli, `layer1`'de 3 bloklu, `fc` girdisi 2048 olan bir ResNet'tir. Python kimlikleri farklıdır ve iki model hiçbir parametre tensörünü paylaşmaz (`kimlik.id_farkli` = true, `kimlik.ortak_parametre_tensoru` = 0). İlk evrişim katmanlarının özeti farklıdır (conv1 ağırlık toplamı 0,978363 ile 1,434142, normu 6,550015 ile 6,050051). İki modelde de normalizasyon tamponu ImageNet ortalaması (0,485, 0,456, 0,406) ve standart sapmasıdır (0,229, 0,224, 0,225) (`kimlik.*.normalizasyon_tamponlari`). Kontrol noktaları diskten okunmuştur: dosyalar yüklemeden önce vardı, değiştirilme zamanları yüklemeyle değişmemiştir, yani indirme ya da yeniden yazma olmamıştır (`yukleme.*.ckpt_vardi`, `mtime_degismedi`). Dosyalar `/mnt/d/adeb_sci_1_veri/models/robustbench_zoo/imagenet/Linf/` altındaki ayrı dosyalardır; boyutları 46.836.793 ve 102.546.991 bayt, sha256 özetleri `a94c5130…d99f` ve `1835a5bb…ce46`'dır (`yukleme.*.ckpt_bayt`, `ckpt_sha256`).

Hesap belirlenimcidir ve eşleme doğrudur. Aynı ilk yığın için R18 ve R50 gradyanı ikinci kez alındığında birinci geçişle kosinüs her görüntüde 1,0000000'dır; R18'in kendisiyle kosinüsü 1'dir (`teshis.oz_kosinus_*`). Görüntü eşlemesi bir sıra kaydırılınca R18-R50 kosinüsü 0,00419'dan 0,00004'e, yedi ve elli sıra kaydırılınca 0,00000 ve 0,00002'ye iner (`teshis.kaydirilmis_indeks`). Denetim çiftlerinde de eşleşik değer ile kaydırılmış değer arasında aynı ayrım vardır (örneğin R18 ile Salman2020Do_50_2'de 0,18548 ile −0,00083). Küçük de olsa R18-R50 değeri görüntüye özgü bir sinyal taşımaktadır; bir indeks kayması ya da ilgisiz iki görüntünün karşılaştırılması söz konusu değildir.

Ortak bir görüntüden bağımsız bileşen de yoktur. Birim normlu gradyanların 100 görüntü üzerindeki ortalamasının normu bütün modellerde 0,0988 ile 0,1017 arasındadır; bu, 100 karşılıklı dik birim vektörün ortalamasında beklenen 1/√100 = 0,1 düzeyidir (`teshis.ortalama_gradyan_normu`). Ortalama bileşen çıkarılınca R18-R50 kosinüsü değişmez (0,00419; `ortalama_cikarilmis_kosinus_R18_R50`). Kanal ortalamaları 10⁻⁶ ile 10⁻⁵ düzeyindedir (`kanal_ortalamasi_x1e4`).

Temiz doğruluk kayıtla ve ön işleme denetimiyle uyumludur. İlk 100 görüntüde R18 49,0, R50 60,0 doğruluk vermiştir ve görüntü düzeyi doğru maskeleri `kosinus.npz`'deki maskeyle aynıdır (`norm_ve_dogruluk.*.temiz_dogru100_*`, `dogru_maskesi_ayni`). 2000 görüntüdeki kayıtlı değerler 41,35 ve 51,90'dır (`kosinus_ozet.json` `temiz_dogruluk_yuzde`); ön işleme denetiminde ortak hatla 41,35 ve 51,9, kendi hatla 41,55 ve 52,0'dır (`results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json`, `modeller.IN_Salman2020Do_R18` ve `IN_Salman2020Do_R50`, `temiz_dogruluk_ortak` ve `temiz_dogruluk_kendi`). İlk 100 görüntüdeki 6 ile 9 puanlık yükseklik bütün modellerde görülür (Salman2020Do_50_2 64,0 ile 56,75; Engstrom2019Robustness 60,0 ile 51,05; Singh ConvNeXt-T 67,0 ile 60,9) ve ilk 50 sınıfın bu altkümede daha kolay olmasıyla açıklanır; R18 ve R50'ye özgü bir sapma yoktur.

## 5. Yakın sıfır değerin kaynağı

Gradyanlar 224×224 ızgarada iki boyutlu Fourier dönüşümüyle beş banda ayrılmış (bant sınırları en büyük eksen frekansına göre 0-1/32, 1/32-1/16, 1/16-1/8, 1/8-1/4 ve 1/4-1/2 devir/piksel), Parseval eşitliğiyle toplam kosinüs bant katkılarına bölünmüştür. ResNet tipi bu dört modelde gradyan enerjisinin %53-74'ü en yüksek banttadır: R18'de 0,740, R50'de 0,702, Salman2020Do_50_2'de 0,620, Engstrom2019Robustness'ta 0,534 (`teshis.frekans.*.enerji_payi`, son öğe). R18-R50 çiftinde ilk dört bandın toplam kosinüse katkıları 0,021, 0,020, 0,028 ve 0,026'dır, en yüksek bandın katkısı ise −0,091'dir; bant içi kosinüsler alçaktan yükseğe 0,532, 0,476, 0,391, 0,203 ve −0,127'dir (`teshis.frekans["IN_Salman2020Do_R18|IN_Salman2020Do_R50"]`). Bu ayrışımda ilk dört bandın toplamı 0,095, son bandınki −0,091'dir ve fark 100 görüntülük ortalama 0,004 ile uyumludur.

Karşılaştırma çiftlerinde en yüksek bandın katkısı pozitiftir: R18 ile Salman2020Do_50_2'de 0,094 (bant içi 0,138), R50 ile Engstrom2019Robustness'ta 0,082 (bant içi 0,134), R18 ile Engstrom2019Robustness'ta 0,030 (bant içi 0,048). R50 ile Salman2020Do_50_2 çiftinde de bu bant negatiftir (katkı −0,047, bant içi −0,072). En yüksek banttaki ters yönlülük R50'nin Salman grubundaki iki kardeşiyle ilişkisinde görülmekte, aynı mimarideki Engstrom2019Robustness ile görülmemektedir. Alçak frekanslarda ise R18 ve R50 bu panelde en hizalı ResNet çiftlerinden biridir: 8×8 ortalama havuzdan sonraki kosinüs R18-R50'de 0,495, R18-Salman2020Do_50_2'de 0,375, R50-Engstrom2019Robustness'ta 0,592'dir (`teshis.alcak_gecirgen_8x8_kosinus`). Gradyan işaretlerinin uyuşma oranı R18-R50'de 0,604'tür ve R18-Salman2020Do_50_2'nin 0,575'inden yüksektir (`teshis.isaret_uyumu`); iki modelin 100 görüntüdeki tahmin uyumu %71'dir (`teshis.tahmin_uyumu_yuzde`). Bu bulgular aynı çiftin yüksek transfer benzerliğiyle (log τ̄ = −0,936; `11_sonuc_b8_b10.md` §6) çelişmez: saldırının dayandığı gradyan yapısı alçak ve orta frekanslarda ortaktır, kosinüs ise en yüksek bandın enerjisi tarafından baskılanmaktadır. Görüntü başına standart sapmanın çok küçük olması da (0,0022) iki bandın katkılarının her görüntüde aynı yönde ve benzer büyüklükte olmasından ileri gelmektedir; sönümlenme görüntüye bağlı değil, modellerin yapısına bağlıdır.

En yüksek banttaki ters yönlülüğün kaynağı bu denetimde sınanmamıştır. Akla en yakın açıklama, iki modelin 7×7 adımı 2 olan ilk evrişiminin ve ardından gelen maksimum havuzun girdi gradyanında ürettiği yüksek frekanslı örtüşme deseninin, ilk katman süzgeçlerinin frekans yanıtına bağlı olarak R50'de kardeşlerinden ters işaretli çıkmasıdır; bu bir varsayımdır ve rapora sonuç olarak girmemelidir.

## 6. Karar ve sonuçları

R18-R50 kosinüsü yapaylık değil, gerçektir. Kod, model yükleme, veri listesi, görüntü eşlemesi ve normalizasyon bağımsız olarak doğrulanmış, kayıtlı değer görüntü düzeyinde yeniden üretilmiştir. Etkilenen çift ve gereken yeniden koşu yoktur; `results/q1/konsey_b10_gradyan/imagenetv2` çıktısı ve onun üzerine kurulan `mantel_imagenetv2.json` ile `b10_aile.json` geçerlidir. `11_sonuc_b8_b10.md` §6'daki şüphe maddesi bu raporla kapatılabilir; §8'deki "GPU denetimi bitene kadar yapılmaz" koşulu da kalkmış olur.

Yorum açısından bir not düşülmelidir. Zhang ve ark. Tanım 2'deki c_ij, enerjiyle ağırlıklı bir ölçüdür ve ResNet gövdeli modellerde enerjinin büyük kısmı en yüksek frekans bandında bulunduğu için bu banttaki işaret, alçak frekanslardaki güçlü hizalanmayı gizleyebilmektedir. B10'un ön kayıtlı sonucu bu ölçüyle elde edilmiştir ve değiştirilmemelidir. Alçak geçiren ya da bant bazlı bir kosinüsle Mantel sınamasını yinelemek ön kayıt dışı bir keşifsel çözümleme olur; böyle bir çözümleme yapılacaksa yalnız "keşifsel" etiketiyle ve bu raporun bulgusuna dayanılarak gerekçelendirilmelidir. Makalede R18-R50 değerinin anılması gerekirse, "ölçünün en yüksek frekans bandındaki sönümlenme nedeniyle sıfıra yakın çıktığı, alçak frekanslı bileşenlerde ise iki modelin hizalı olduğu" bilgisi bu raporun `denetim.json` kaynağıyla verilebilir.

## 7. Yazılan dosyalar

`arsiv/b2_yardimci/_b10_r18_r50_denetim.py` (denetim betiği), `arsiv/b2_yardimci/_b10_kayit_oku.py` (kayıtlı npz ve özet okuyucu), `arsiv/b2_yardimci/_b10_denetim_cikti/denetim.json` (bu rapordaki bütün yeni sayıların kaynağı), `arsiv/b2_yardimci/_b10_denetim_cikti/kosu.log`, `arsiv/b2_yardimci/_b10_denetim_cikti/kayit_oku.log`, `arsiv/b2_yardimci/_b10_denetim_cikti/kayit.json` ve `kayit_cos100.npy`, `kayit_norm100.npy`, `kayit_ok100.npy` (kayıttan alınan ilk 100 görüntü değerleri), `arsiv/b2_yardimci/_b10_denetim_cikti/ortalama_gradyan.pt` (altı modelin birim normlu ortalama gradyan görüntüsü) ve bu rapor.
