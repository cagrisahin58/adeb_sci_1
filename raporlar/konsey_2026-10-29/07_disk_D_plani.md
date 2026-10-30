# D diskine taşıma planı (30.10.2026)

Bu rapor salt okur bir envanter ve plandır. Hiçbir klasör taşınmamış, `adeb_eval` konteynerine komut gönderilmemiştir (yalnız ana makineden `docker inspect`, `docker diff` ve `docker top` ile okunmuştur). `scripts/d_diskine_tasi.sh` betiği yazılmış, yalnız `--dry-run` kipinde çalıştırılmıştır; bu kip hiçbir dosyayı değiştirmez ve D'de klasör açmaz. D sürücüsünün davranışını sınamak için `/mnt/d/adeb_sci_1_veri/_deneme_*` altında geçici dosyalar yazılmış, sınamadan sonra klasörle birlikte silinmiştir.

## 1. Durum özeti

WSL sanal diski (`/dev/sdd`, 1007 GB) 902 GB dolu, 55 GB boştur; depo bunun yalnız 45 GB'ını tutar (`models/` 41 GB, `results/` 1,7 GB, `data/` 1,2 GB, `logs/` 401 MB). Sanal diskin Windows'taki dosyası `C:\Users\cagri\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu22.04LTS_79rhkp1fndgsc\LocalState\ext4.vhdx` olup 909,9 GB büyüklüğündedir ve aralıklı (sparse) değildir. Windows C: sürücüsünde (ADATA LEGEND 900 PRO NVMe, 2 TB) 84 GB, D: sürücüsünde (Lexar NM790 NVMe, 4 TB) 2,2 TB boş yer vardır. Docker motoru Docker Desktop değildir; Ubuntu-22.04 dağıtımının içinde yerel olarak çalışır (`docker info`: Ubuntu 22.04.5, kök `/var/lib/docker`, sürüm 29.1.3). Bu ayrıntı aşağıdaki bütün önerileri belirler, çünkü konteyner süreçleri WSL çekirdeğinde koşar ve WSL'den `ps` ile görülür.

Rapor yazılırken B2 matrisi bitmiş (`logs/konsey_b2.log` son satırı `custom kaydedildi: results/q1/konsey_b2_panel`), `scripts/konsey_tam_zincir.sh` konteynerde başlamış ve B3 kuyruğunun ilk aşaması (`V_IN_s2101` temiz eğitimi, `models/q1/konsey/V_IN_s2101`) koşmaktadır. Zincir sırasıyla B3, B4, B6, B5 ve çözümlemeleri koşar ve en sonda konteyner içinde `chown -R 1000:1000 /workspace/results/q1 /workspace/models/q1 /workspace/logs` verir.

## 2. Envanter

Aşağıdaki tablo `du` ile ölçülmüş en büyük otuz öğeyi verir. "Okunuyor" sütunu B2 komut satırına, `scripts/konsey_tam_zincir.sh`, `scripts/konsey_b3_kuyruk.sh`, `KONSEY_RUNBOOK.md` metnine ve `experiments/c1_c3_transfer_matrix.py`, `experiments/run_autoattack_run2.py`, `src/models/r224.py` içindeki sabit yollara bakılarak doldurulmuştur. `run_autoattack_run2.py` içindeki karantina varsayılanları (`models/resnet18/adv/at_run2/...`) B6'da `--model` verildiği için okunmaz (satır 203-213).

| # | Yol | Boyut | Kampanya | Zincir okuyor mu | Öneri |
|---|-----|-------|----------|------------------|-------|
| 1 | `models/q1/e2` | 21 GiB (epok klasörleri 19 GiB) | q1 E2, 6 AT yörüngesi, son yazım 16.08 | Hayır | `epochs/` klasörleri şimdi D'ye |
| 2 | `models/q1/cifar100` | 11 GiB (epok 9,0 GiB) | q1 E1 CIFAR-100, son yazım 20.08 | Hayır | `epochs/` şimdi D'ye |
| 3 | `models/q1/svhn` | 4,3 GiB (epok 3,1 GiB) | q1 SVHN, son yazım 21.08 | Hayır | `epochs/` şimdi D'ye |
| 4 | `models/c1` | 1,8 GiB | C1 (geçerli) | Evet, B4 ve B5 | Dokunulmaz |
| 5 | `results/q1/konsey_adv_onbellek` | 1,7 GiB, büyüyor | q1 konsey | Evet, B4 `--cache-adv` | Dokunulmaz |
| 6 | `models/robustbench_zoo` | 1,1 GiB | Panel P ağırlıkları | Evet, B4 ve B5 | Dokunulmaz |
| 7 | `models/resnet18` | 854 MiB | Karantina (at_run2, at_run3, trades, trades_v3, clean) | Hayır | Grup 2, sudo ister |
| 8 | `models/vit_tiny` | 508 MiB | Karantina (at_run2, at_run3, clean) | Hayır | Grup 2, sudo ister |
| 9 | `results/q1/adv_archive` | 434 MiB | q1 E1/E2 çekişmeli örnek arşivi, son yazım 21.08 | Hayır | Şimdi D'ye |
| 10 | `models/q1/konsey_smoke` | 320 MiB | q1 konsey smoke | Hayır | Yerinde kalır (ön kayıt kanıtı, küçük) |
| 11 | `models/q1/konsey` | büyüyor | q1 konsey B3 | Evet, B3 yazıyor | Dokunulmaz |
| 12 | `models/vit_cifar_tiny` | 185 MiB | Şubat 2026, C1 öncesi | Hayır | Grup 2, sudo ister |
| 13 | `data/cifar-10-batches-py` | 178 MiB | Veri | Evet, bütün bloklar | Dokunulmaz |
| 14 | `data/cifar-100-python` | 178 MiB | Veri | Hayır | Yerinde (küçük, q1 yeniden koşularında okunur) |
| 15 | `data/train_32x32.mat` | 174 MiB | SVHN verisi (root sahipli) | Hayır | Yerinde |
| 16 | `data/train_32x32.mat.1` | 174 MiB | Yukarıdakinin bayt bayt aynı wget kopyası (`cmp` ile denetlendi) | Hayır | Şimdi D'ye |
| 17 | `data/cifar-10-python.tar.gz` | 163 MiB | Veri arşivi | Hayır | Zincir sonrası, kazanç küçük |
| 18 | `data/cifar-100-python.tar.gz` | 162 MiB | Veri arşivi | Hayır | Zincir sonrası, kazanç küçük |
| 19 | `models/robustbench` | 140 MiB | Şubat 2026 WRN-28-10 | Hayır | Yerinde (aşağıya bkz.) |
| 20 | `models/cifar10/Linf` | 140 MiB | RobustBench varsayılan `model_dir` önbelleği (Gowal2020) | Hayır | Yerinde (aşağıya bkz.) |
| 21 | `models/densenet121` | 108 MiB | Şubat 2026 | Hayır | Şimdi D'ye |
| 22 | `models/timm_agirliklar` | 67 MiB | Konsey timm ağırlıkları | Evet, B3 | Dokunulmaz |
| 23 | `data/test_32x32.mat.1` | 62 MiB | `test_32x32.mat` ile aynı kopya | Hayır | Şimdi D'ye |
| 24 | `logs/` | 401 MiB toplam, en büyüğü 15 MiB | Karışık | Zincir yazıyor | Yerinde |
| 25 | `results/q1/konsey_smoke` | 25 MiB | q1 konsey smoke | Hayır | Yerinde (ön kayıt kanıtı) |
| 26 | `results/q1/konsey_b2_panel` | 8,5 MiB | q1 konsey B2 | Evet, B4 | Dokunulmaz |
| 27 | `results/q1/e2` | 3,5 MiB | q1 E2 | Hayır | Yerinde (küçük) |
| 28 | `results/q1/havuz_cifar10` | 2,9 MiB | q1 | Hayır | Yerinde |
| 29 | `results/q1/cifar100` | 2,5 MiB | q1 | Hayır | Yerinde |
| 30 | `results/` karantina klasörleri (`transfer_analysis_run3`, `autoattack_run3_full`, `rev2_blockA` vb.) | her biri 400 KiB altında | Karantina | Hayır | Yerinde, kazanç yok |

Tablodan çıkan sonuç açıktır: yerin %75'i q1 kampanyalarının epok başına kaydedilmiş kontrol noktalarıdır. On altı `epochs/` klasörü toplam 30,72 GiB ve 978 dosya tutar; her koşunun `best.pth` ve `last.pth` dosyaları bu klasörlerin dışındadır. Epok kontrol noktaları yalnız yörünge çözümlemesi betiklerince okunur (`scripts/q1_e2_test_curve.py` satır 97, `scripts/q1_offline_select.py`, `scripts/q1_e3_*`); bu betikler zincirde yoktur ve konsey masa çözümlemeleri (`_p3_yorunge_gurbuzluk_masa.py`) epok dosyalarını değil `results/q1/e2/testcurve_*.npz` özetlerini okur. Karantina kontrol noktaları (run1, run2, run3, trades) toplamda yalnız 1,55 GiB'tır, yani karantinayı taşımanın disk üzerinde belirgin bir etkisi yoktur.

`models/robustbench` ve `models/cifar10` yerinde bırakılmıştır. İkincisi RobustBench'in varsayılan `model_dir="./models"` önbelleğidir; `c1_c3_transfer_matrix.py` kendi `models/robustbench_zoo` dizinini kullanır, ancak varsayılan dizinle çalışan eski bir betik koşulursa buraya yazmaya çalışır ve kırık bir bağa çarpar. Kazanç 280 MiB olduğu için bu risk alınmaya değmez.

## 3. Şimdi taşınabilecekler

Grup 1 sudo gerektirmez, bütün öğeleri firat sahiplidir, git izlemez (`models/` izlenmeyen, `data/` ve `results/q1/adv_archive/` `.gitignore` kapsamında) ve zincirin hiçbir adımı okumaz. Kuru koşu çıktısına göre toplam 32 GiB'tır: on altı `epochs/` klasörü 30,72 GiB, `results/q1/adv_archive` 434 MiB, iki `.mat.1` kopyası 236 MiB ve `models/densenet121` 108 MiB. Taşımadan sonra WSL diskindeki boş yer 54 GB'tan yaklaşık 86 GB'a çıkar; B3 kuyruğunun 15 GB durma eşiğinden uzaklaşılır. Epok klasörlerinin tek tek taşınması bilinçli bir seçimdir: kampanya klasörü bütünüyle taşınsaydı konteyner `best.pth` dosyalarını da göremezdi, bu biçimde yalnız yörünge dosyaları D'ye gider, seçilmiş kontrol noktaları konteynerden okunmaya devam eder.

Grup 2 karantina klasörleridir (`models/resnet18`, `models/vit_tiny`, `models/vit_cifar_tiny`, toplam 1,6 GiB). İçlerinde konteynerin root olarak yazdığı dizinler bulunduğundan kaynağın silinmesi `sudo rm -rf` ister. Kazanç küçük olduğu için isteğe bağlıdır.

Betik her öğe için şu sırayı izler: öğe yoksa, zaten bağsa, git izliyorsa ya da çalışan herhangi bir sürecin komut satırında yolu (epok klasörlerinde koşu ve kampanya kökü de) geçiyorsa atlar; D'de öğe boyutunun %10 fazlası ile 1 GiB pay yoksa durur; `rsync -rt --no-perms --no-owner --no-group` ile `/mnt/d/adeb_sci_1_veri/<aynı göreli yol>` altına kopyalar; kaynaktan sha256 manifesti üretip D'de `sha256sum -c` ile denetler ve dosya sayısını karşılaştırır; kaynağı `<yol>.__silinecek` adıyla yeniden adlandırır, aynı yola mutlak sembolik bağ koyar, manifestteki ilk dosyayı bağ üzerinden okuyup özetini karşılaştırır, tutmazsa geri alır; yalnız bunlardan sonra eski kopyayı siler. Manifestler `/mnt/d/adeb_sci_1_veri/_manifest/`, taşıma defteri `/mnt/d/adeb_sci_1_veri/_manifest/tasima_defteri.tsv`, günlük `logs/d_tasima_<zaman>.log` altına yazılır. Sınamada betiğin koşmakta olan `models/q1/konsey` yolunu ve git izlenen `data/val_split_indices.json` dosyasını atladığı görülmüştür.

Komutlar WSL kabuğunda, depo kökünde ve firat kullanıcısıyla verilir. B3 eğitimiyle disk paylaşımını azaltmak için düşük öncelik önerilir:

```bash
cd /home/firat/projects/adeb_sci_1
bash scripts/d_diskine_tasi.sh --dry-run                              # plan ve toplam (32 GiB)
nice -n 19 ionice -c3 bash scripts/d_diskine_tasi.sh                  # grup 1
df -h /home/firat /mnt/d; cat /mnt/d/adeb_sci_1_veri/_manifest/tasima_defteri.tsv
# istege bagli, karantina (sudo parolasi ister):
bash scripts/d_diskine_tasi.sh --grup 2 --dry-run
nice -n 19 ionice -c3 bash scripts/d_diskine_tasi.sh --grup 2
```

Ölçülen hızlarla (aşağıda bölüm 5) 32 GiB'ın kopyalanması ve iki taraflı sha256 denetimi kabaca 10-15 dakika sürer. Betik yarıda kesilirse biten öğeler bağ olarak kalır ve yeniden çalıştırmada atlanır; `mv` ile `rm` arasında kesilen bir öğede `<yol>.__silinecek` klasörü kalır, bağın çalıştığı `ls -L <yol>` ile görüldükten sonra elle silinir. Geri almak için bağ silinir, `rsync -rt /mnt/d/adeb_sci_1_veri/<yol>/ <yol>/` ile veri geri kopyalanır ve `cd /home/firat/projects/adeb_sci_1 && sha256sum -c /mnt/d/adeb_sci_1_veri/_manifest/<yol_alt_cizgili>.sha256` ile denetlenir.

Bağlar mutlak yolla (`/mnt/d/adeb_sci_1_veri/...`) kurulur. WSL'de çalışırlar; konteynerin içinde `/mnt/d` bağlı olmadığından konteynerden bakıldığında KIRIKTIR. Bu yüzden betiğin listesi yalnız konteynerin bu zincirde okumadığı öğelerden oluşur. Konteyner içinde epok dosyalarını okuyan bir q1 yörünge betiği konteyner yeniden oluşturulana kadar `FileNotFoundError` verir. Zincirin sonundaki `chown -R` adımı kırık bağlardan etkilenmez: GNU `chown -R` varsayılan olarak bağı izlemez, WSL'de içinde kırık bağ bulunan bir klasörde `chown -R firat:firat` denemesi çıkış kodu 0 vermiştir.

## 4. Zincir bittikten sonra: konteyneri D bağlamasıyla yeniden oluşturma

`docker inspect adeb_eval` çıktısına göre konteyner 07.07.2026'da `vsc-adeb_sci_1-3231432907506cdace4b76eba995c8ce9b3a6939736e1a626829224a5b0ce95b-uid:latest` imajından (kimlik `048217db0b5f`, temeli NGC PyTorch 25.01, Ubuntu 24.04) oluşturulmuştur. Ayarları şunlardır: kullanıcı root, giriş noktası `/opt/nvidia/nvidia_entrypoint.sh`, komut `sleep infinity`, çalışma dizini `/workspace`, tek bağlama `/home/firat/projects/adeb_sci_1:/workspace` (rw), GPU isteği `Count -1, gpu` (yani `--gpus all`), `IpcMode host`, `SecurityOpt label=disable`, ağ bridge, yeniden başlatma ilkesi yok, yayımlanmış port yok (8888 ve 6006 yalnız imajda tanımlı), ortam değişkenleri imajdan gelir. Depodaki `.devcontainer/docker-compose.yml` bu konteyneri tanımlamaz (orada servis `med-lab`, kullanıcı `ubuntu`, çalışma dizini `/workspace/adeb_sci_1`), yani mevcut ortam depodan yeniden üretilemez durumdadır.

`docker diff adeb_eval` konteynerin yazılabilir katmanında 2334 değişiklik gösterir ve katman 218 MB'tır. Bunların içinde konteyner içinde pip ile kurulmuş paketler vardır: timm 1.0.27, robustbench 1.1, autoattack 0.1, huggingface_hub 1.22.0, hf_xet 1.5.1, omegaconf 2.3.1, antlr4 4.9.3, seaborn 0.13.2, geotorch 0.4.0, torchdiffeq 0.2.5, gdown 6.1.0, pymupdf 1.28.0, pypdf 6.14.2, PySocks 1.7.1 ve click 8.4.2 (imajdaki click 8.1.7 kaldırılmış), ayrıca `/root/.cache/torch/hub` ve `/root/.cache/huggingface` önbellekleri. Konteyner doğrudan silinip imajdan yeniden oluşturulursa bunların hepsi kaybolur ve timm, robustbench ve autoattack olmadan zincirin hiçbir betiği çalışmaz. Bu nedenle ilk adım `docker commit`'tir. Commit yalnız yazılabilir katmanı yeni bir katman olarak ekler (yaklaşık 218 MB, C'deki `/var/lib/docker` içinde), `/workspace` bağlamasının içeriğini kapsamaz.

Tarif, zincir bittikten ve `docker top adeb_eval` yalnız `sleep infinity` gösterdikten sonra WSL kabuğunda uygulanır:

```bash
cd /home/firat/projects/adeb_sci_1
# 0) zincirin bittigini dogrula
tail -3 logs/konsey_zincir.log; column -t -s $'\t' results/q1/konsey_zincir_durum.tsv | tail -5
docker top adeb_eval -eo pid,args

# 1) ortami kayda gecir (yeniden uretilebilirlik)
docker exec adeb_eval pip freeze > raporlar/konsey_2026-10-29/adeb_eval_pip_freeze.txt
docker inspect adeb_eval > raporlar/konsey_2026-10-29/adeb_eval_inspect.json

# 2) konteyner ici pip kurulumlarini imaja al
docker commit -m "adeb_eval: konteyner ici pip (timm 1.0.27, robustbench 1.1, autoattack 0.1, ...)" \
    adeb_eval adeb_eval:2026-10-30

# 3) eskiyi silmeden kenara al
docker rename adeb_eval adeb_eval_eski
docker stop adeb_eval_eski

# 4) ayni ayarlar + D baglamasi
mkdir -p /mnt/d/adeb_sci_1_veri
docker run -d --name adeb_eval \
    --gpus all --ipc=host --security-opt label=disable \
    -w /workspace \
    -v /home/firat/projects/adeb_sci_1:/workspace \
    -v /mnt/d/adeb_sci_1_veri:/mnt/d/adeb_sci_1_veri \
    -v /mnt/d/adeb_sci_1_veri:/veri \
    adeb_eval:2026-10-30 sleep infinity

# 5) dogrulama
docker exec adeb_eval nvidia-smi
docker exec -w /workspace adeb_eval python -c "import torch, timm, robustbench, autoattack; print(torch.__version__, timm.__version__, torch.cuda.is_available())"
docker exec -w /workspace adeb_eval bash -c 'ls -L models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs | head -3'
docker exec -w /workspace adeb_eval python -c "import torch; d=torch.load('models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs/epoch_100.pth', map_location='cpu', weights_only=False); print(d['epoch'], d['adv_acc'])"
docker exec adeb_eval bash -c 'dd if=/dev/zero of=/veri/_dd_sinama bs=1M count=1024 conv=fdatasync && rm /veri/_dd_sinama'

# 6) her sey calisiyorsa eski konteyneri kaldir (eski imaj kalir)
docker rm adeb_eval_eski
```

Giriş noktası, kullanıcı ve ortam değişkenleri commit edilen imajdan aynen gelir; `--shm-size` verilmemiştir, çünkü `--ipc=host` ile konteyner ana makinenin `/dev/shm`'ini kullanır ve eski konteynerdeki 64 MB değeri etkisizdir. Ana bilgisayar adı değişir, bu hiçbir betiği etkilemez. Uzun vadede proje kuralı (bağımlılık Dockerfile'a yazılır) gereği `adeb_eval_pip_freeze.txt` dosyasından sabit sürümlü bir Dockerfile (`FROM nvcr.io/nvidia/pytorch:25.01-py3` ve tek `pip install` satırı) yazılmalıdır; commit edilmiş imaj bu yapılana kadar köprüdür.

D'nin konteynere iki yoldan bağlanmasının nedeni yolların iki tarafta aynı anlamı taşımasıdır. WSL'deki bağlar `/mnt/d/adeb_sci_1_veri/...` mutlak yolunu gösterdiği için D klasörü konteynerin içine de aynı yolla bağlanırsa bütün bağlar konteynerden kendiliğinden çözülür ve hiçbir betik ya da runbook komutu değişmez. `/workspace/models/q1` ya da önbellek yollarını D'ye yönlendirmenin tutarlı tek yolu da budur: WSL tarafında klasör D'ye taşınıp yerine bağ konur, konteyner bağı aynı yoldan izler. Bind mount altında bind mount (`-v /mnt/d/.../models/q1:/workspace/models/q1`) önerilmez, çünkü WSL'deki `models/q1` C'deki eski içeriği, konteynerdeki aynı yol D'deki içeriği gösterir ve tmux'tan verilen komutlarla konteyner içinden verilen komutlar iki farklı klasör görür. Konteyner içinde `/veri/...` hedefli bağ kurmak da önerilmez, çünkü bağ bind mount üzerinden WSL'ye yansır ve WSL'de `/veri` olmadığından orada kırık görünür. `/veri` bağlaması yalnız elle yazılan kısa yollar içindir; kalıcı bir dosyaya, bağa ya da yapılandırmaya `/veri` değil `/mnt/d/adeb_sci_1_veri` yazılmalıdır.

Yeni bir kampanyanın çıktısını doğrudan D'ye yazdırmak için kampanya başlamadan WSL'de `mkdir -p /mnt/d/adeb_sci_1_veri/models/q1/<ad> && ln -s /mnt/d/adeb_sci_1_veri/models/q1/<ad> models/q1/<ad>` verilir. Eğitim döngüsü kontrol noktasını önce `.tmp` adıyla yazıp `replace` ile yerine koyar (`src/training/adversarial_trainer.py` satır 541-548); yeniden adlandırmanın drvfs üzerinde çalıştığı ve root olarak yazılan dosyaların D'de nasıl göründüğü, ilk kampanyadan önce bir epokluk kısa eğitimle sınanmalıdır. `data/` ve sık okunan önbellekler C'de kalmalıdır.

Bu tarifin yerine geçebilecek, daha az parçalı bir kalıcı çözüm de vardır ve bunu öneriyorum: WSL sanal diskini bütünüyle D'ye taşımak. WSL 2.6.1 bunu `wsl --shutdown` ardından `wsl --manage Ubuntu-22.04 --move D:\WSL\Ubuntu-22.04` ile yapar; ardından `wsl --manage Ubuntu-22.04 --resize 1800GB` ile ext4 kapasitesi büyütülebilir ve `--set-sparse true` ile dosyanın boşalan alanı Windows'a geri vermesi sağlanabilir (üç seçenek de bu makinedeki `wsl --help` çıktısında bulunmuştur). Bu yolda bütün yollar aynı kalır, sembolik bağ ve konteyner değişikliği gerekmez, veri ext4 hızında okunur, Docker imajları da D'ye geçer ve C'de yaklaşık 910 GB açılır. Bedeli WSL'in kapatılmasıdır: bu, `adeb_eval` ile birlikte başka projeye ait `histo-sparse-adv` konteynerini de durdurur, bu yüzden yalnız iki projenin de işi yokken yapılabilir. 909,9 GB'lık dosyanın kopyalanma süresi ölçülmemiştir. Taşıma kesilirse dağıtım kaydı bozulabileceğinden, öncesinde depoların uzak sunucuya gönderilmiş olması gerekir; D'de 2,2 TB boş yer olduğu için istenirse önce `wsl --export Ubuntu-22.04 D:\WSL\yedek.tar` ile tam yedek de alınabilir.

## 5. Riskler

drvfs hızı bu makinede ölçülmüştür. D üzerinde 1 GiB `dd` yazması `conv=fdatasync` ile 6,18 s sürmüş (174 MB/s), aynı dosyanın okunması 3,90 s sürmüştür (275 MB/s; sayfa önbelleği boşaltılamadığından iyimser bir değerdir). D'deki 1 GiB dosyanın sha256 özeti 7,11 s, 89 MB'lık gerçek bir `best.pth` dosyasının ext4'ten D'ye `rsync` kopyası 0,72 s, 64 KiB'lık 200 küçük dosyanın kopyası 0,91 s sürmüştür. C'deki ext4 için karşılaştırma ölçümü, dolu diske 1 GiB yazmamak için yapılmamıştır. Bu hızlar arşiv ve ara sıra okunan kontrol noktaları için yeterlidir; epok dosyalarının tamamını tarayan bir yörünge çözümlemesi D'den daha yavaş okur. D:\adeb_sci_1_veri klasörü Windows Defender gerçek zamanlı taramasından muaf tutulmazsa büyük dosya yazımları ayrıca yavaşlayabilir.

İzin davranışı beklenenden farklıdır. `/mnt/d` 9p drvfs olarak `uid=1000,gid=1000` ile ve `metadata` seçeneği olmadan bağlıdır (`/etc/wsl.conf` yalnız `systemd=true` içerir). Bu yüzden D'deki her dosya `rwxrwxrwx firat firat` görünür, `chmod 600` ve `chmod 755` etkisizdir, firat olarak `chown root` "Operation not permitted" verir. Root sahipli karantina dosyalarının sahiplik bilgisi D'de korunmaz. `rsync -a` her denetimde izin farkı raporlayacağından (sınamada `.f...p.....` satırı görülmüştür) betik izinleri hiç taşımaz ve doğrulamayı izinlerden bağımsız olan sha256 ile yapar. D içinde sembolik bağ kurmak ve ext4'ten D'ye bağ kurmak sınamada çalışmıştır.

Kırık bağlar bölüm 3'te anlatıldığı gibi yalnız konteynerin içinden görülür ve konteyner bölüm 4'teki gibi yeniden oluşturulunca ortadan kalkar. D sürücüsünün harfi değişirse ya da sürücü çıkarılırsa bağlar WSL'de de kırılır. Betiğin süreç denetimi yalnız o anda çalışan komut satırlarına bakar, zincirin ileride koşacağı adımları göremez; bu adımların okuduğu yollar ayrıca `scripts/konsey_tam_zincir.sh` metninden denetlenmiş ve taşıma listesiyle kesişmediği görülmüştür.

Gözden kaçmaması gereken bir risk de Windows tarafındadır. Sanal disk dosyası 909,9 GB iken ext4 kapasitesi 1007 GB'tır; dosya yeni bloklar yazıldıkça kapasitesine kadar büyüyebilir, bu da C'de 84 GB'tan fazla yer isteyebilir. Böyle bir durumda ext4 içinde yer görünse bile C dolar ve WSL G/Ç hatası verir. Grup 1 taşıması bu baskıyı azaltır, çünkü D'ye yazılan veri sanal diski büyütmez ve ext4'te boşalan bloklar sanal diskte zaten ayrılmış alandır. B3 süresince `df -h /home/firat` ile birlikte `df -h /mnt/c` de izlenmelidir.

Depo dışındaki yer kullanımı da büyüktür. `docker system df` imajlar için 37,28 GB (35,95 GB geri kazanılabilir), durmuş konteynerler için 10,9 GB (9,15 GB geri kazanılabilir), derleme önbelleği için 2,6 GB gösterir. Bu imaj ve konteynerlerin çoğu başka projelere aittir (`medforge-lab`, `msat-lab`, `gtmba-canary` vb.); temizlik kararı bu planın kapsamı dışındadır ve kullanıcıya aittir.

## 6. WSL'i kapatıp yalnız Windows'ta çalışmak

Bu hatta WSL'i kapatmak, GPU işlerinin koştuğu ortamın tamamını kapatmak demektir. Docker motoru Ubuntu-22.04 dağıtımının içinde çalıştığından WSL kapanınca `adeb_eval` ve `histo-sparse-adv` dahil bütün konteynerler durur. Docker Desktop'a geçmek de bunu değiştirmez, çünkü Docker Desktop Linux konteynerlerini ve GPU erişimini yine WSL2 sanal makinesi üzerinden sağlar. Konteynerin imajı NVIDIA'nın Linux/amd64 için yayımladığı `nvcr.io/nvidia/pytorch:25.01-py3` temelidir; bu imajın Windows karşılığı yoktur ve PyTorch 2.6.0a0+ecf3bae derlemesi, CUDA 12.8 ile cuDNN 9.7 bileşimi Windows'ta aynen kurulamaz. Windows'ta resmi PyTorch tekerlekleriyle çalışmak farklı bir derleme, farklı cuDNN ve TF32 varsayılanları demektir; dondurulmuş ön kaydın ve C1 föyünün sayılarıyla birebir karşılaştırılabilirlik kaybolur. Bunun yanında kuyruk ve zincir betikleri bash ile yazılmıştır, runbook komutları `/workspace` yoluna bağlıdır ve Windows'ta DataLoader işçileri `spawn` ile başladığından betiklerin ayrıca uyarlanması gerekir. Sonuç olarak disk sorunu WSL'i kapatarak değil, WSL'in sanal diskini ya da büyük verisini D'ye taşıyarak çözülmelidir; ortam ve sayılar bundan etkilenmez.
