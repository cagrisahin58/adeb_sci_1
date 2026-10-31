# adeb_eval konteynerinin D bağlamasıyla yeniden kurulumu, çatal regresyonu ve B8 ön işleme denetimi (31.10.2026)

Bu rapor 31.10.2026 sabahı yapılan üç işi kayda geçirir: `adeb_eval` konteynerinin `07_disk_D_plani.md` §4'teki tarifle yeniden kurulması, `scripts/ek_zincir_komutlari.sh regresyon b8denetim` koşusu ve ek ön kaydın (`ON_KAYIT_EK_B8_B10_2026-10-30.md`) §5.5 kuralına göre verilen karar ile ardından başlatılan `b9 b8 b10 cozumleme` zinciri. Bütün komutlar Windows'tan `wsl.exe -d Ubuntu-22.04 -- bash -lc` ile, `arsiv/b2_yardimci/_ek_*.sh` betikleri üzerinden verilmiştir; saatler WSL saatidir (+03). Aşağıdaki çıktılar betiklerin `tee` ile yazdığı günlüklerden kısaltılmadan alınmıştır: `arsiv/b2_yardimci/_ek_kurulum.log`, `_ek_dogrula.log`, `_ek_baslat1.log`, `_ek_baslat2.log`.

## 1. Başlangıç durumu

Bilgisayar 31.10.2026 sabahı yeniden başlatılmış, `adeb_eval` konteyneri `Exited (255)` durumunda kalmıştır. B3-B6 zinciri 30.10.2026 20:40:46'da `ZINCIR TAMAM` ile bitmiştir (`logs/konsey_zincir.log` son satırı; `results/q1/konsey_zincir_durum.tsv` son satırı `zincir ... 0 TAMAM`). Eski konteynerin kullanıcısı `docker inspect --format '{{.Config.User}}' adeb_eval` ile `root` olarak okunmuş, bu nedenle yeni konteynere `--user` eklenmemiştir. Ayrıca adı `adeb_eval_broken` olan, üç ay önce `Exited (137)` ile durmuş başka bir konteyner bulunmaktadır; bu konteynere dokunulmamıştır. Komşu `histo-sparse-adv` konteyneri çalışır durumdadır ve ona da dokunulmamıştır. Başlangıçta GPU'da 2893 MiB kullanılmakta, 29295 MiB boş bulunmaktaydı (`nvidia-smi --query-gpu=memory.used,memory.free`, 06:57). WSL diskinde 82 GB, D'de 2,2 TB, C'de 104 GB boş yer vardı (`df -h`, 06:57).

## 2. Adım 1-4: ortamın kayda geçirilmesi, commit ve yeni konteyner

Tarifin 1. adımı durmuş konteynerde çalışmadığından konteyner önce `docker start adeb_eval` ile kaldırılmıştır. `pip freeze` çıktısı `raporlar/konsey_2026-10-29/adeb_eval_pip_freeze.txt` (302 satır), `docker inspect` çıktısı `raporlar/konsey_2026-10-29/adeb_eval_inspect.json` (18636 bayt) olarak kaydedilmiştir. Inspect çıktısı konteyner kaldırıldıktan sonra alındığından `State` alanı çalışır durumu gösterir. Freeze dosyasında robustbench ve autoattack git kaynaklı satırlar olarak yer alır (satır 234 `robustbench @ git+https://github.com/RobustBench/robustbench.git@78fcc9e48a07a861268f295a777b975f25155964`, satır 18 `autoattack @ git+https://github.com/fra31/auto-attack@a39220048b3c9f2cca9a4d3a54604793c68eca7e`); betikteki `grep '^robustbench=='` deseni bu yüzden yalnız `click` ve `timm` satırlarını yakalamıştır. Commit edilen imaj `adeb_eval:2026-10-30`, kimliği `d74e25a950a4`'tür.

Komutlar `arsiv/b2_yardimci/_ek_kurulum.sh` içindedir; çıktısı aşağıdadır (`_ek_kurulum.log`):

```text
[2026-10-31 06:58:02] 0) zincir durumu
== 10. chown ve son satir
[2026-10-30 20:40:46] chown: chown -R 1000:1000 /workspace/results/q1 /workspace/models/q1 /workspace/logs
[2026-10-30 20:40:46] ZINCIR TAMAM
B5_TGR         2026-10-30 20:36:38  2026-10-30 20:40:39  0           OK       
B6_maskeleme   2026-10-30 20:40:39  2026-10-30 20:40:39  0           OK       
B4_cozumleme   2026-10-30 20:40:39  2026-10-30 20:40:42  0           OK       
B5_cozumleme   2026-10-30 20:40:42  2026-10-30 20:40:46  0           OK       
zincir                              2026-10-30 20:40:46  0           TAMAM    
[2026-10-31 06:58:02] 1a) docker start adeb_eval
adeb_eval
PID                 COMMAND
77028               /bin/bash /opt/nvidia/nvidia_entrypoint.sh sleep infinity
77162               /bin/bash /opt/nvidia/nvidia_entrypoint.sh sleep infinity
77163               nvidia-smi -q -d compute
77164               grep ^CUDA Version
77165               sed s/^.*: //
[2026-10-31 06:58:03] 1b) pip freeze ve inspect
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/dill-0.3.9-py3.12.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/opt_einsum-3.4.0-py3.12.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/lightning_thunder-0.2.0.dev0-py3.12.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/lightning_utilities-0.12.0.dev0-py3.12.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/nvfuser-0.2.23a0+6627725-py3.12-linux-x86_64.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
DEPRECATION: Loading egg at /usr/local/lib/python3.12/dist-packages/looseversion-1.3.0-py3.12.egg is deprecated. pip 25.1 will enforce this behaviour change. A possible replacement is to use pip for package installation. Discussion can be found at https://github.com/pypa/pip/issues/12330
pip freeze rc=0 satir=302
inspect rc=0 bayt=18636
click==8.4.2
timm==1.0.27
eski User=[root]
[2026-10-31 06:58:04] 2) docker commit
sha256:d74e25a950a4bf9d2358518599353d4d4edc1f728ec216a3be7bd67cb09b6049
adeb_eval:2026-10-30 d74e25a950a4 26.7GB
[2026-10-31 06:58:07] 3) rename + stop
adeb_eval_eski
[2026-10-31 06:58:20] 4) docker run
77f49ef35d9c2b304b3cd6b2fae724953a4294cecb91fbdf410d3673d7f4858d
adeb_eval|Up 3 seconds|adeb_eval:2026-10-30
adeb_eval_eski|Exited (137) 5 seconds ago|vsc-adeb_sci_1-3231432907506cdace4b76eba995c8ce9b3a6939736e1a626829224a5b0ce95b-uid:latest
adeb_eval_broken|Exited (137) 3 months ago|vsc-adeb_sci_1-3231432907506cdace4b76eba995c8ce9b3a6939736e1a626829224a5b0ce95b-uid:latest
yeni User=[root]
[{"Type":"bind","Source":"/home/firat/projects/adeb_sci_1","Destination":"/workspace","Mode":"","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/mnt/d/adeb_sci_1_veri","Destination":"/mnt/d/adeb_sci_1_veri","Mode":"","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/mnt/d/adeb_sci_1_veri","Destination":"/veri","Mode":"","RW":true,"Propagation":"rprivate"}]
[2026-10-31 06:58:24] kurulum bitti
```

Yeni konteyner tarifteki komutun aynısıyla kurulmuştur:

```bash
docker run -d --name adeb_eval \
    --gpus all --ipc=host --security-opt label=disable \
    -w /workspace \
    -v /home/firat/projects/adeb_sci_1:/workspace \
    -v /mnt/d/adeb_sci_1_veri:/mnt/d/adeb_sci_1_veri \
    -v /mnt/d/adeb_sci_1_veri:/veri \
    adeb_eval:2026-10-30 sleep infinity
```

`docker stop adeb_eval_eski` konteyneri `Exited (137)` ile durdurmuştur; bu, `sleep infinity` sürecinin SIGTERM'e yanıt vermeyip on saniye sonra öldürülmesinin olağan sonucudur.

## 3. Adım 5: doğrulama

Tarifteki beş doğrulama komutu ile görevde istenen üç ek denetim (`data/imagenetv2` erişimi, `models/robustbench_zoo/imagenet/Linf` için 15 ve `cifar100/Linf` için 11 dosya) `arsiv/b2_yardimci/_ek_dogrula.sh` ile koşulmuştur. Sekiz denetimin sekizi de geçmiştir. Çıktı aşağıdadır (`_ek_dogrula.log`):

```text
[2026-10-31 06:58:28] D1 nvidia-smi
Sat Oct 31 03:58:28 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 620.67.01              KMD Version: 621.01        CUDA UMD Version: 13.5     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5090        On  |   00000000:01:00.0  On |                  N/A |
| 30%   36C    P0             81W /  475W |    2800MiB /  32607MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
SONUC D1: GECTI
[2026-10-31 06:58:28] D2 import
2.6.0a0+ecf3bae40a.nv25.01 1.0.27 True
SONUC D2: GECTI
[2026-10-31 06:58:34] D3 epochs ls -L
epoch_001.pth
epoch_002.pth
epoch_003.pth
SONUC D3: GECTI
[2026-10-31 06:58:34] D4 epoch_100.pth yukleme
99 44.233333333333334
SONUC D4: GECTI
[2026-10-31 06:58:35] D5 /veri 1 GB dd yaz-sil
1024+0 records in
1024+0 records out
1073741824 bytes (1.1 GB, 1.0 GiB) copied, 5.46508 s, 196 MB/s
SONUC D5: GECTI
dd_dosyasi_silindi
[2026-10-31 06:58:41] D6 imagenetv2 gorunur
D_GORUNUR
SONUC D6: GECTI
[2026-10-31 06:58:41] D7 robustbench_zoo imagenet/Linf (15 bekleniyor)
15
SONUC D7: GECTI
total 3312208
-rwxrwxrwx 1 ubuntu ubuntu 275913601 Oct 30 02:31 Chen2024Data_WRN_50_2.pt
-rwxrwxrwx 1 ubuntu ubuntu 105172083 Oct 30 02:33 Debenedetti2022Light_XCiT-S12.pth.tar
-rwxrwxrwx 1 ubuntu ubuntu 102529618 Oct 30 02:30 Engstrom2019Robustness.pt
-rwxrwxrwx 1 ubuntu ubuntu 354496687 Oct 30 02:28 Liu2023Comprehensive_ConvNeXt-B.pt
-rwxrwxrwx 1 ubuntu ubuntu 352787535 Oct 30 02:28 Liu2023Comprehensive_Swin-B.pt
-rwxrwxrwx 1 ubuntu ubuntu 346330174 Oct 30 02:29 Mo2022When_ViT-B.pt
-rwxrwxrwx 1 ubuntu ubuntu 417089026 Oct 30 02:32 Peng2023Robust.pt
-rwxrwxrwx 1 ubuntu ubuntu 275912303 Oct 30 02:30 Salman2020Do_50_2.pt
-rwxrwxrwx 1 ubuntu ubuntu  46836793 Oct 30 02:29 Salman2020Do_R18.pt
-rwxrwxrwx 1 ubuntu ubuntu 102546991 Oct 30 02:29 Salman2020Do_R50.pt
-rwxrwxrwx 1 ubuntu ubuntu 355132063 Oct 30 02:26 Singh2023Revisiting_ConvNeXt-B-ConvStem.pt
-rwxrwxrwx 1 ubuntu ubuntu 114572173 Oct 30 02:26 Singh2023Revisiting_ConvNeXt-T-ConvStem.pt
-rwxrwxrwx 1 ubuntu ubuntu 348642911 Oct 30 02:27 Singh2023Revisiting_ViT-B-ConvStem.pt
-rwxrwxrwx 1 ubuntu ubuntu  91166417 Oct 30 02:26 Singh2023Revisiting_ViT-S-ConvStem.pt
-rwxrwxrwx 1 ubuntu ubuntu 102546991 Oct 30 02:33 Wong2020Fast.pt
[2026-10-31 06:58:42] D8 robustbench_zoo cifar100/Linf (11 bekleniyor)
11
SONUC D8: GECTI
total 1368332
-rwxrwxrwx 1 ubuntu ubuntu  44963257 Oct 30 02:34 Addepalli2022Efficient_RN18.pt
-rwxrwxrwx 1 ubuntu ubuntu 193470987 Oct 30 02:36 Chen2021LTD_WRN34_10.pt
-rwxrwxrwx 1 ubuntu ubuntu 146269938 Oct 30 02:36 Cui2023Decoupled_WRN-28-10.pt
-rwxrwxrwx 1 ubuntu ubuntu 103786099 Oct 30 02:35 Debenedetti2022Light_XCiT-S12.pth.tar
-rwxrwxrwx 1 ubuntu ubuntu 146249648 Oct 30 02:35 Hendrycks2019Using.pt
-rwxrwxrwx 1 ubuntu ubuntu 193475477 Oct 30 02:35 Jia2022LAS-AT_34_10.pt
-rw------- 1 ubuntu ubuntu 146270845 Mar 15  2022 Pang2022Robustness_WRN28_10.pt
-rwxrwxrwx 1 ubuntu ubuntu  50445746 Oct 30 02:34 Rade2021Helper_R18_ddpm.pt
-rwxrwxrwx 1 ubuntu ubuntu  44922584 Oct 30 02:33 Rice2020Overfitting.pt
-rwxrwxrwx 1 ubuntu ubuntu 185019203 Oct 30 02:34 Sehwag2021Proxy.pt
-rwxrwxrwx 1 ubuntu ubuntu 146269624 Oct 30 02:34 Wang2023Better_WRN-28-10.pt
[2026-10-31 06:58:42] OZET gecen=8 kalan=0
```

D4'te yazdırılan epok değeri 99'dur; kontrol noktası sözlüğündeki `epoch` alanı sıfırdan saydığı için `epoch_100.pth` dosyası bu değeri taşır ve dosya hatasız yüklenmiştir. Konteyner içinden bakıldığında dosya sahibi `ubuntu` görünür, çünkü imajda uid 1000 bu adla tanımlıdır. `Pang2022Robustness_WRN28_10.pt` dosyası `-rw-------` izinlidir ve ext4'te durur (D'deki dosyalar drvfs nedeniyle `rwxrwxrwx` görünür); konteyner root olarak çalıştığından okunabilir, ancak firat dışındaki bir kullanıcıyla çalışan bir süreç bu dosyayı okuyamaz.

## 4. Adım 6: eski konteynerin kaldırılması ve İŞ 2'nin başlatılması

Bütün denetimler geçtiği için `docker rm adeb_eval_eski` verilmiştir; eski imaj (`vsc-adeb_sci_1-...-uid:latest`, `048217db0b5f`) yerinde kalır. Aynı betikte dondurulmuş dosyaların git durumu ve özetleri denetlenmiş, ardından `scripts/ek_zincir_komutlari.sh regresyon b8denetim` ayrık olarak başlatılmıştır (`arsiv/b2_yardimci/_ek_baslat1.sh`). `git status --porcelain` çıktısının boş olması, dondurulmuş dosyaların, hücre tablolarının ve zincir betiğinin çalışma ağacında değişmediğini gösterir. Özetler Dondurma eki (a), (b) ve (c)'deki değerlerle aynıdır.

```text
[2026-10-31 06:58:56] 6) docker rm adeb_eval_eski
adeb_eval_eski
adeb_eval|Up 36 seconds|adeb_eval:2026-10-30
adeb_eval_broken|Exited (137) 3 months ago|vsc-adeb_sci_1-3231432907506cdace4b76eba995c8ce9b3a6939736e1a626829224a5b0ce95b-uid:latest
[2026-10-31 06:58:56] dondurulmus dosyalar git durumu (bos bekleniyor):
f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7  experiments/c1_c3_transfer_matrix.py
4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389  experiments/q1_konsey_ayrisim.py
4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d  raporlar/konsey_2026-10-29/hucre_tablosu_b8.json
be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd  raporlar/konsey_2026-10-29/hucre_tablosu_b9.json
[2026-10-31 06:58:56] IS 2 baslatildi
```

## 5. Çatal regresyonu

Komut `setsid nohup bash scripts/ek_zincir_komutlari.sh regresyon b8denetim > results/q1/ek_loglar/ek_zincir_1.log 2>&1 < /dev/null & disown` biçiminde 06:58:56'da başlamıştır. `bekci()` denetimleri geçmiş, betik `DUR` satırı yazmamıştır. Regresyon adımı 06:58:56-07:00:31 arasında, ön işleme denetimi 07:00:31-07:07:58 arasında koşmuş, betik 07:07:58'de `bitti` satırıyla kapanmıştır. Günlüğün tamamı şöyledir (`results/q1/ek_loglar/ek_zincir_1.log`):

```text
2026-10-31 06:58:56 adim regresyon basliyor
2804 MiB, 32607 MiB
ozgun sha256: f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7
catal sha256: edec356afa594a681e1b3646b76f28c92bbf16c9159eace3dbc3c03cd6a87145
ozgun: rc=0 sure=24 s
catal: rc=0 sure=24 s
 "ust_alan_farklari": {},
 "BIREBIR": true
}
ozgun_onb: rc=0 sure=22 s
catal_onb: rc=0 sure=23 s
 "ust_alan_farklari": {},
 "BIREBIR": true
}
ayni ResNet18_AT_s1001__pgd_linf_s10_n200_seed42_cifar10.npy
ayni ViT_Tiny_AT_s2001__pgd_linf_s10_n200_seed42_cifar10.npy
ayni WRN_28_10__pgd_linf_s10_n200_seed42_cifar10.npy
bitti: results/q1/ek_regresyon/gpu_n200
2026-10-31 07:00:31 adim b8denetim basliyor
b8 denetim rc=0
Sonuc: results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json ve imagenetv2_manifest.json (liste_sha256).
Ek on kayit §5.5 kurali T gorulmeden uygulanir; eleme varsa IN14 bu betikte duzeltilir ve sapma kaydina yazilir.
2026-10-31 07:07:58 bitti
```

İki karşılaştırma dosyası şunlardır. İkisinde de `BIREBIR` alanı `true`'dur, farklı hücre ve farklı npz yoktur; önbellekli koşunun üç önbellek dosyası da bayt düzeyinde aynıdır (`cmp -s`, yukarıdaki `ayni` satırları). Çatal betiğin özeti (`edec356a...`) sapma kaydındaki kod ekiyle aynıdır (`results/q1_research/ONKAYIT_SAPMALAR.md`, "Ek B8-B10").

```text
== results/q1/ek_regresyon/gpu_n200/karsilastirma_ozgun_catal.json
{
  "A": "results/q1/ek_regresyon/gpu_n200/ozgun",
  "B": "results/q1/ek_regresyon/gpu_n200/catal",
  "hucre_sayisi": 9,
  "npz_sayisi": 9,
  "json_farkli_hucreler": [],
  "npz_farklari": [],
  "ust_alan_farklari": {},
  "BIREBIR": true
}
== results/q1/ek_regresyon/gpu_n200/karsilastirma_ozgun_onb_catal_onb.json
{
  "A": "results/q1/ek_regresyon/gpu_n200/ozgun_onb",
  "B": "results/q1/ek_regresyon/gpu_n200/catal_onb",
  "hucre_sayisi": 9,
  "npz_sayisi": 9,
  "json_farkli_hucreler": [],
  "npz_farklari": [],
  "ust_alan_farklari": {},
  "BIREBIR": true
}
```

## 6. B8 ön işleme denetimi ve §5.5 kararı

Denetim manifesti 2000 görüntülük listeyi `BicubicRes256Crop224` ortak hattıyla, "sınıf klasörü başına sıralı ilk ceil(n/1000) dosya; sıra (sınıf, ad)" kuralıyla üretmiştir; listenin özeti `25db498ba8b2c710618e76e8a2dfe5492c9f75be0be1b7f63c253acc4f27d1a8`'dir (`results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json`, anahtarlar `n`, `secim_kurali`, `onisleme`, `liste_sha256`). Dosyanın SHA-256 özeti `7cd43424b50104431ba7d0da886ab9c95824d8f9446e9f306fe6d89fe0943dd4`, denetim dosyasının (`onisleme_denetimi.json`) özeti `9f75f8dd4ad96320e8661ff6a4c8665736d37d3d7a24d28d858dbdfa9e2c4ed1`'dir. Denetim dosyasında `ortak_onisleme` alanı `BicubicRes256Crop224`, `n` alanı 2000, `kalan` ve `isaretli` listeleri boştur.

§5.5'in bağlayıcı metni şudur: "(i) kendi hatla 1000 sınıflı temiz doğruluk en az %25 ve RobustBench'te yayımlanan temiz doğruluğun en az 0,6 katı olmalıdır; (ii) ortak hat ile kendi hat arasındaki mutlak fark en çok 5 puan olmalıdır. [...] Farkı 3 ile 5 puan arasında kalan model matriste kalır, işaretlenir [...]. Kuralı geçmeyen model matristen çıkar". Kural her model için iki yoldan uygulanmıştır. Birincisi çatal betiğin yazdığı `modeller.<takma ad>.esik.karar` alanıdır. İkincisi `arsiv/b2_yardimci/_ek_b8_kural.py` betiğidir; bu betik iki doğruluğu `onisleme_denetimi.json` dosyasından, RobustBench temiz doğruluğunu ise çatal betikten bağımsız olarak `raporlar/konsey_2026-10-29/_ek_denetim/dis/rb/in_<RobustBench adı>.json` kopyalarının `clean_acc` alanından okur ve kuralı yeniden hesaplar. İki yol on beş modelin on beşinde aynı kararı vermiş, RobustBench değerleri de çatal betiğin `esik.rb_temiz` alanıyla aynı çıkmıştır (betik çıktısında `uyumsuz=0`). Bu değerler ek §5.3 tablosundaki temiz doğruluklarla da örtüşür.

Aşağıdaki tabloda kendi hat ve ortak hat doğrulukları `onisleme_denetimi.json` dosyasının `modeller.<takma ad>.temiz_dogruluk_kendi` ve `temiz_dogruluk_ortak` anahtarlarından, fark `fark_puan` anahtarından (ortak eksi kendi), RobustBench değeri `_ek_denetim/dis/rb/in_<ad>.json` dosyasının `clean_acc` anahtarından alınmıştır; eşik (i) `max(25, 0,6 × RB)` olarak hesaplanmış, karar `esik.karar` anahtarındadır. Doğruluklar yüzde, fark puandır.

| Takma ad | RB temiz | Eşik (i) | Kendi hat | Ortak hat | Fark (ortak - kendi) | (i) | (ii) | 3-5 işareti | Karar |
|---|---|---|---|---|---|---|---|---|---|
| IN_Salman2020Do_R18 | 52,92 | 31,752 | 41,55 | 41,35 | -0,20 | geçti | geçti | yok | geçti |
| IN_Salman2020Do_R50 | 64,02 | 38,412 | 52,00 | 51,90 | -0,10 | geçti | geçti | yok | geçti |
| IN_Salman2020Do_50_2 | 68,46 | 41,076 | 56,20 | 56,75 | +0,55 | geçti | geçti | yok | geçti |
| IN_Engstrom2019Robustness | 62,56 | 37,536 | 50,95 | 51,05 | +0,10 | geçti | geçti | yok | geçti |
| IN_Chen2024Data_WRN_50_2 | 68,76 | 41,256 | 57,05 | 57,60 | +0,55 | geçti | geçti | yok | geçti |
| IN_Peng2023Robust | 73,44 | 44,064 | 59,65 | 60,45 | +0,80 | geçti | geçti | yok | geçti |
| IN_Singh_ConvNeXt-T-CvSt | 72,72 | 43,632 | 60,90 | 60,90 | 0,00 | geçti | geçti | yok | geçti |
| IN_Singh_ViT-S-CvSt | 72,56 | 43,536 | 61,00 | 61,00 | 0,00 | geçti | geçti | yok | geçti |
| IN_Singh_ConvNeXt-B-CvSt | 75,90 | 45,540 | 63,20 | 63,20 | 0,00 | geçti | geçti | yok | geçti |
| IN_Singh_ViT-B-CvSt | 76,30 | 45,780 | 64,85 | 64,85 | 0,00 | geçti | geçti | yok | geçti |
| IN_Liu_ConvNeXt-B | 76,02 | 45,612 | 65,50 | 65,50 | 0,00 | geçti | geçti | yok | geçti |
| IN_Liu_Swin-B | 76,16 | 45,696 | 64,80 | 64,80 | 0,00 | geçti | geçti | yok | geçti |
| IN_Mo_ViT-B | 68,38 | 41,028 | 55,80 | 56,75 | +0,95 | geçti | geçti | yok | geçti |
| IN_Debenedetti_XCiT-S12 | 72,34 | 43,404 | 59,90 | 60,35 | +0,45 | geçti | geçti | yok | geçti |
| IN_Wong2020Fast (yedek) | 55,62 | 33,372 | 44,55 | 43,35 | -1,20 | geçti | geçti | yok | geçti |

Modellerin kendi hatları `onisleme_denetimi.json` dosyasının `kendi_onisleme` anahtarında kayıtlıdır: altı P8 üyesinde bilinear `Resize(256)` ve `CenterCrop(224)`, Singh ve Liu çiftlerinde bicubic `Resize(256)` ve `CenterCrop(224)`, Mo ViT-B'de kırpmasız bilinear `Resize([224, 224])`, XCiT-S12'de bicubic `Resize(224)` ve `CenterCrop(224)`, Wong2020Fast'te yeniden boyutlandırmasız `CenterCrop(288)`. Kendi hattı ortak hatla aynı olan altı modelde fark beklendiği gibi sıfırdır. Kendi hat doğruluklarının hepsi RobustBench'in ImageNet doğrulama değerlerinin altındadır; bu, §5.5'in ImageNetV2 için bıraktığı payla uyumludur.

Karar: on beş modelin hiçbiri §5.5 kuralına göre elenmemiş, hiçbiri 3-5 puan aralığında işaretlenmemiştir, çünkü en düşük kendi hat doğruluğu (IN_Salman2020Do_R18, 41,55) kendi eşiğinin (31,752) ve %25'in üstündedir, en büyük mutlak fark ise yedek IN_Wong2020Fast'te 1,20 puan, panel üyeleri arasında IN_Mo_ViT-B'de 0,95 puandır. Bu yüzden yedek devreye girmez ve `scripts/ek_zincir_komutlari.sh` içindeki IN14 listesi olduğu gibi kalır.

Ek §5.1 ve §12, denetim sonucunun ve liste özetinin B8 matrisinden önce ve T görülmeden sapma kaydına yazılmasını ister. Karar: bu kayıt 07:08'de, İŞ 3 başlatılmadan hemen önce `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasının sonuna "31.10.2026, not: GPU çatal regresyonu ve B8 ön işleme denetimi (sapma değil)" başlığıyla eklenmiştir, çünkü zincirin B8 adımına ulaşması ana oturumun müdahalesini beklemez ve ön kaydın sırası ancak bu biçimde güvenceye alınır. Dosyaya yalnız ekleme yapılmış, önceki içerik değiştirilmemiştir; dosyanın özeti ekten önce `3d751094aecd1a6ce259b6bd928d112f3daf26b5b7c874818d74675cfdb40b27`, ekten sonra `853429e1e5f2a1637bb80ba28c634452e122ff3560dd2ffc19f0c07f7ae618c3`'tür. Eklenen metnin kaynağı `arsiv/b2_yardimci/_ek_sapma_ek.md` dosyasıdır.

## 7. İŞ 3: B9, B8, B10 ve çözümleme zincirinin başlatılması

Hiçbir model elenmediği için `setsid nohup bash scripts/ek_zincir_komutlari.sh b9 b8 b10 cozumleme > results/q1/ek_loglar/ek_zincir_2.log 2>&1 < /dev/null & disown` komutu 31.10.2026 07:08:48'de başlatılmıştır (`arsiv/b2_yardimci/_ek_baslat2.sh`). Günlüğün ilk satırı `2026-10-31 07:08:49 adim b9 basliyor`'dur; yani `bekci()` denetimleri yeniden geçmiştir. Başlatmadan önce `git status --porcelain -- scripts/ek_zincir_komutlari.sh 'raporlar/konsey_2026-10-29/hucre_tablosu*.json'` boş çıkmıştır. Başlangıçtan 150 saniye sonra (07:11:18) GPU kullanımı %92, kullanılan bellek 7599 MiB, boş bellek 24589 MiB'tır; konteynerde `experiments/c1_c3_transfer_matrix.py --dataset cifar100 --n-samples 10000 --seed 42 ...` süreci 2 dakika 28 saniyedir koşmaktadır. 07:11:30'da `results/q1/ek_loglar/b9_matris.log` içinde `traceback`, `error`, `hata` ya da `killed` geçen satır sayısı 0'dır. Önbellek D diskine yazılmaktadır: o anda `/mnt/d/adeb_sci_1_veri/onbellek/b9_c100/` altında üç kaynak modelin her biri için 122880128 baytlık `.npy` dosyası (float32, 10000 × 3 × 32 × 32) ve eşlik eden `.json` dosyası vardır.

Zincir bu raporun yazıldığı sırada sürmektedir; bitişi ana oturumca izlenecektir. Zincir kendi sonunda `docker exec adeb_eval chown -R 1000:1000 /workspace/results/q1` verdiği için bu adım ayrıca çalıştırılmamıştır. İŞ 2'nin yazdığı `results/q1/ek_regresyon/gpu_n200` ve `results/q1/konsey_b8_imagenetv2/denetim` klasörleri ilk zincirin sonundaki aynı `chown` ile firat sahipli olmuştur (`ls -la` çıktısında `firat firat`).

## 8. Açık noktalar

Başlatma doğrulaması sırasında `_ek_baslat2.sh` betiği `b9_matris.log` dosyasının son 15 satırını ekrana yazdırmış, bu satırlar tek bir kaynak modelin (C100_ResNet18_AT_s1003) 15 hedefe transfer hücrelerini içermiştir. Bu değerler bu rapora ve hiçbir karara taşınmamıştır; B9'un çözümlemesi dondurulmuş betikle ve dondurulmuş hücre tablosuyla yapılacağından bu görüntülemenin çözümlemeye bir etkisi yoktur, yine de B9'un T değerlerinin çözümlemeden önce görüldüğü bir olay olarak kayda geçirilmesi gerekir.

`adeb_eval_pip_freeze.txt` dosyasından sabit sürümlü bir Dockerfile yazılması (`07_disk_D_plani.md` §4 son paragrafı) bu oturumda yapılmamıştır; commit edilmiş `adeb_eval:2026-10-30` imajı bu yapılana kadar köprü olarak kalır. Hiçbir dosya git'e eklenmemiş, commit ya da push yapılmamıştır.
