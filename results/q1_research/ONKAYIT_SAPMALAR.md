# Ön kayıt sapma kaydı

Bu dosya, `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` (dondurulmuş ön kayıt, §7 "Sapmalar") ile `raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md` (ek ön kayıt, §12) dosyalarının adını verdiği sapma kaydıdır. Dosya 30.10.2026'da ek ön kaydın dondurulmasıyla birlikte oluşturulmuştur. Her kayıt tarihiyle ve ilgili çözümleme yapılmadan önce yazılır. Ek ön kaydın §12'sine göre indirme arşivinin ve manifestin özetleri, ön işleme denetiminin sonucu ve üç yeni betiğin ilk koşudan önceki özetleri (kod eki) bu ekte tanımlı kurallardan doğduğu için sapma sayılmaz; yine de transfer matrisi görülmeden buraya yazılır. Dondurulmuş ana ön kayda ait kayıtlar ayrı bir başlık altında tutulur.

## Ek B8-B10

### 30.10.2026, indirme kaydı: ImageNetV2 arşivi (sapma değil)

ImageNetV2 MatchedFrequency arşivi `imagenetv2-matched-frequency.tar.gz` D diskine indirilmiş ve SHA-256 özeti indirme kaydından (`/mnt/d/adeb_sci_1_veri/indirme_sha256.txt`, satır `_indirme/arsiv/imagenetv2-matched-frequency.tar.gz`) aktarılmıştır. Arşivin boyutu 1.264.079.360 bayttır ve ek ön kaydın §5.1'de HTTP HEAD ile beyan ettiği değerle aynıdır (`raporlar/konsey_2026-10-29/_ek_denetim/d4_boyutlar.tsv`).

```text
f0c37fdf925916b19ea1323cd9a2208cdb6959ba2c32eef2a7fc393835c9ca7c  imagenetv2-matched-frequency.tar.gz
```

Seçilen 2000 görüntülük listenin özeti (`imagenetv2_manifest.json`, `liste_sha256`) B8-0 ön işleme denetimi koşusundan sonra ve B8 matrisinden önce bu başlığın altına yazılacaktır; henüz üretilmemiştir.

### 30.10.2026, kod eki: üç yeni betiğin dondurma anındaki özetleri (sapma değil)

Ek ön kaydın §3'üne göre aşağıdaki üç betik ilk koşudan önce eke uydurulmuş ve özetleri burada kayda geçirilmiştir. Özetler ek ön kaydın dondurulduğu anda, dondurma doğrulayıcısının düzeltmelerinden sonra WSL'de `sha256sum` ile hesaplanmıştır. Bu dosyalar ilgili koşudan önce yeniden değişirse yeni özet tarihiyle yine "kod eki" olarak buraya yazılır; koşudan sonra değişirlerse bu bir sapmadır.

```text
edec356afa594a681e1b3646b76f28c92bbf16c9159eace3dbc3c03cd6a87145  experiments/q1_ek_transfer_matrix.py
d264c4e584fcfb3c0e3dd9517cfe2cea4ea1fe564117c88459e2b9721027a641  experiments/q1_ek_ayrisim.py
c82a66d196c38f23d688f610caf6ffceab0c01e7ebfa68e5358f832014043eed  experiments/q1_ek_gradyan_kosinus.py
169a522bf07ff1a8ce7d5828c182cb9893030d098cc99cc731d110e8b1e3facd  tests/test_q1_ek.py
```

Çatal matris betiği `q1_ek_transfer_matrix.py` ImageNetV2 yükleyicisini, `--eps`, `--alpha`, `--batch-size`, `--cache-root`, `--cache-f16` bayraklarını, ortak önişleme hattını (varsayılan `BicubicRes256Crop224`) ve ön işleme denetimini taşır. Denetim işlevi dondurma doğrulayıcısının isteğiyle ek §5.5'in kuralına uydurulmuştur: önceki sürüm eşik uygulamıyor ve çıktı notunda taslağın eşiklerini (%40, 3 puan) taşıyordu; bu sürüm her model için (i) kendi hatta temiz doğruluğun en az %25 ve RobustBench temiz doğruluğunun en az 0,6 katı olmasını, (ii) ortak hat ile kendi hat arasındaki mutlak farkın en çok 5 puan olmasını denetler, 3 ile 5 puan arasını işaretler ve kararı `onisleme_denetimi.json` içindeki `esik` alanına yazar. Varsayılan bayraklarla çatalın davranışı değişmemiştir. Çözümleme betiği `q1_ek_ayrisim.py` dondurulmuş `experiments/q1_konsey_ayrisim.py`'yi SHA-256 denetimiyle yükler, B8 betimsel çözümlemesini ve F_B10 ailesini (altı sınama, Holm) kurar; `kismi_omega` ve `kismi_omega_gradnorm` sınamalarını `kesifsel_` önekiyle F_B10 dışında verir. Gradyan betiği `q1_ek_gradyan_kosinus.py` görüntü başına kosinüsleri `kosinus.npz` içinde float16 saklar, c_ij'yi float64 ortalama olarak hesaplar ve Mantel sınamasını varsayılan 9999 permütasyon ve tohum 20261030 ile yapar. Ek §6.4'teki S10-3 (aile göstergeli kısmi Mantel) için kod yazılmamıştır. Birim sınamaları (22 sınama) konteyner CPU'sunda `CUDA_VISIBLE_DEVICES=` ile geçmiştir.

### 30.10.2026, not: çatal regresyonu (sapma değil)

Ek ön kaydın §3'ü, dondurma doğrulayıcısının düzeltmesiyle, çatal regresyonunu zincir bittikten sonra GPU'da `bash scripts/ek_regresyon.sh gpu 200` ile yapılacak biçimde tanımlar. Taslak metindeki "n = 200, CPU" ifadesi dondurulmadan önce düzeltildiğinden bu durum sapma değildir. CPU'da n = 40 ile yapılan ön karşılaştırma birebir çıkmıştır (`results/q1/ek_regresyon/cpu_n40/karsilastirma_ozgun_catal.json`, `BIREBIR: true`). GPU regresyonunun sonucu koşudan sonra buraya yazılır.
