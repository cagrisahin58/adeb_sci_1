# B1 kod raporu: sarmalayıcılar, eğitim bayrakları, transfer matrisi, pilot ve kuyruk (29.10.2026)

Hazırlayan: B1 bloğunun kod uygulayıcısı (opus alt ajan). Bağlı belgeler: `KONSEY_PLANI.md` (§2, §4, §6, §7, §8), `ON_KAYIT_TASLAGI.md`, `KONSEY_RUNBOOK.md`. Bu rapordaki sayıların hepsi smoke ve pilot çıktılarıdır, makaleye girecek sonuç değildir; her sayının yanında kaynak dosyası verilmiştir. Konteyner saati UTC'dir, JSON içindeki zaman damgaları yerel saatin üç saat gerisindedir.

En önemli üç nokta şunlardır. Birincisi, bütün smoke testleri ve regresyon geçmiştir; varsayılan bayraklarla yeni transfer matrisi kodu eski kodla hücre hücre ve örnek örnek aynı çıktıyı üretmektedir. İkincisi, zaman pilotu R224 AT epoğunu 142,7 s, V-IN AT epoğunu 125,8 s ölçmüş, bekçi tavanı 80 epok seçmiş ve en kötü durum eğitim süresi 20,47 sa çıkmıştır; ancak ölçüm boş GPU'da yapılmıştır ve GPU paylaşılırsa bu süre iki katına yaklaşabilir. Üçüncüsü, plan taslağındaki `-e <TAVAN>` yerine AT `-e 100 --stop-epoch <TAVAN>` ile koşturulmaktadır; böylece kosinüs öğrenme oranı çizelgesi C1 ViT (V-scr) tarifindeki gibi 100 epok üzerinden kurulur. Bu karar ve `ON_KAYIT_TASLAGI.md` §3 tablosundaki R224-scr satırının K3 ile çelişmesi ana oturumun onayını beklemektedir (Bölüm 9).

## 1. Değişen ve eklenen dosyalar

Değişen dosyalar (git diff, 420 ekleme, 53 silme):

| Dosya | Değişiklik |
|---|---|
| `src/models/__init__.py` | `r224` modülünün kaydı |
| `src/training/trainer.py` | `optimizer_name` (auto, adamw, sgd), `lr_schedule` (cosine, constant), `max_train_batches` |
| `src/training/adversarial_trainer.py` | `optimizer_name`, `stop_epoch` (çizelge `epochs` üzerinden, eğitim tavanda durur), `max_train_batches`; `TRAINING_COMPLETE` dosyasına yalnız `stop_epoch` verildiğinde `stop_epoch` ve `stopped_at_cap` satırları eklenir |
| `cli/train.py` | `train clean`: `--optimizer`, `--init-weights`, `--lr-schedule`, `--max-train-batches`; `train adversarial`: `--optimizer`, `--stop-epoch`, `--max-train-batches` |
| `experiments/c1_c3_transfer_matrix.py` | `--attack {pgd,mi,tgr}`, `--steps`, `--sources`, `--cache-adv`, `--skip-existing`; XCiT hub önbelleğinin depodaki kopyadan geri konması |

Eklenen dosyalar:

| Dosya | İş |
|---|---|
| `src/models/r224.py` | `resnet18_224`, `resnet18_224_in1k`, `vit_tiny_in1k` sarmalayıcıları, `ResizeNormalize`, `load_imagenet_init` (yükleme raporu) |
| `scripts/konsey_indir.py` | timm ve RobustBench indirmeleri, XCiT kopyası, `results/q1/konsey_smoke/indirmeler.json` |
| `scripts/konsey_smoke_modeller.py` | sarmalayıcı, yükleme ve normalizasyon smoke testi |
| `scripts/konsey_smoke_egitim.sh` | 200 iterasyonluk temiz eğitim smoke testi (CLI yolu) |
| `scripts/konsey_smoke_regresyon.sh` | eski ve yeni matris kodunun git worktree ile karşılaştırılması |
| `scripts/konsey_smoke_karsilastir.py` | iki matris klasörünün hücre ve npz düzeyinde karşılaştırılması |
| `scripts/konsey_smoke_matris.sh`, `scripts/konsey_smoke_mi_esit.py` | yeni matris bayraklarının ve MI/TGR eşitliğinin smoke testleri |
| `scripts/konsey_pilot_zaman.py` | zaman pilotu ve bekçi kuralı |
| `scripts/konsey_b3_kuyruk.sh` | B3 kuyruğu (defter, disk ve GPU kaydı, devam, `--dry-run`) |
| `scripts/konsey_b3_denetim.py` | kuyruk yardımcısı: tavan okuma, ON_KAYIT §4 temiz aşama denetimi, AT çöküş kuralı, AT özeti ve kırpılma işareti |
| `raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md` | kullanıcının çalıştıracağı komutlar |

Disk üzerindeki yeni varlıklar: `models/timm_agirliklar/` (67 MB), `models/robustbench_zoo/cifar10/Linf/` altına üç yeni `.pt` ve XCiT kopyası, `models/q1/konsey_smoke/` (smoke kontrol noktaları, gereksiz `last.pth` dosyaları silindikten sonra 320 MB), `results/q1/konsey_smoke/` (20 MB), `results/q1/konsey_pilot_zaman*.json`. Konteynerin yazdığı dosyalar `chown -R 1000:1000` ile firat'a geri verilmiştir.

## 2. Girdi hattı ve K3 kararının uygulanışı

V-scr'nin (C1 `vit_tiny`) girdi hattı kodda şöyledir. Veri yükleyici `src/data/datasets.py::_default_transforms` içinde eğitimde `RandomCrop(32, padding=4)`, `RandomHorizontalFlip` ve `ToTensor`, değerlendirmede yalnız `ToTensor` uygular; değer aralığı [0, 1]'dir ve normalizasyon yoktur (aynı dosyadaki not: "Normalizasyon YOKTUR: tüm modeller [0,1] ham piksel girdisi tüketir"). Model içinde `src/models/vit.py::CIFAR10ViTTiny` girdiyi `nn.Upsample(size=(224, 224), mode="bilinear", align_corners=False)` ile büyütür ve timm `vit_tiny_patch16_224`'e verir.

R224-scr (`resnet18_224`) bu hattı birebir kullanır: aynı yükleyici, aynı `nn.Upsample` nesnesi, normalizasyon yok. Smoke testinde iki büyütme katmanının çıktısı aynı girdide `torch.equal` ile özdeş bulunmuş, R224-scr'nin durum sözlüğünde büyütmeye ait tampon olmadığı doğrulanmıştır (`results/q1/konsey_smoke/modeller.json`, `r224_scr_girdi_hatti_vscr_ile_ayni`). ImageNet normalizasyonu yalnız IN başlatmalı tiplerde, büyütmeden sonra model içinde uygulanır. Bunun için normalizasyon tipe bağlanmış ve ayrı bir kayıt adı açılmıştır: `resnet18_224_in1k` (R224-IN) ve `vit_tiny_in1k` (V-IN). Ortalama ve standart sapma timm `pretrained_cfg`'den okunur ve kalıcı tampon olarak kontrol noktasına girer; normalizasyonlu bir kontrol noktası normalizasyonsuz tipe katı yüklemede hata verir (`kayit_yukleme_turu` testi). `--init-weights deit_tiny_in1k` yalnız `vit_tiny_in1k` ile, `--init-weights resnet18_a1_in1k` yalnız `resnet18_224_in1k` ile kabul edilir; uyumsuz tip `ValueError` verir (`uyumsuz_tip_reddi` testi). `vit_tiny_in1k` sınıf adı `CIFAR10ViTTinyIN1k`'dır, adında "vit" korunmuştur; TGR kancaları ve dikkat çıkarımı `self.model.blocks` ile çalışır ve normalizasyon her yolda (`forward`, `get_features`, `get_attention_maps`) uygulanır, çünkü büyütme ile normalizasyon tek `resize` modülündedir.

## 3. Smoke testleri

Her test 5 dakikanın altında koşmuştur. Kalan test yoktur.

| Test | Sonuç | Kaynak |
|---|---|---|
| Ağırlık yükleme, `deit_tiny_patch16_224.fb_in1k` | Geçti: 150/152 anahtar yüklendi; atlanan yalnız `head.weight`, `head.bias`; baş dışında eksik 0, fazla 0, şekil uyuşmazlığı 0 | `results/q1/konsey_smoke/modeller.json`, `agirlik_yukleme_deit_tiny_in1k` |
| Ağırlık yükleme, `resnet18.a1_in1k` | Geçti: 120/122; atlanan yalnız `fc.weight`, `fc.bias`; eksik 0, fazla 0, uyuşmazlık 0 | aynı dosya, `agirlik_yukleme_resnet18_a1_in1k` |
| Normalizasyon değerleri | Geçti: iki IN tipinde ortalama (0,485; 0,456; 0,406), std (0,229; 0,224; 0,225), `pretrained_cfg` ile 1e-6 içinde aynı; ileri geçiş elle normalizasyonla aynı | aynı dosya, `normalizasyon_*` |
| V-IN mimarisi V-scr ile aynı | Geçti: 152 anahtarın adı ve şekli aynı, 5 526 346 parametre | aynı dosya, `v_in_mimari_vscr_ile_ayni` |
| C1 ViT kontrol noktası eski tiple yükleniyor | Geçti | aynı dosya, `c1_vit_yukleme` |
| 200 iterasyon temiz eğitim, ViT | Geçti: V-IN doğrulama doğruluğu %92,85, aynı ayarla rastgele başlatma %32,45 (AdamW lr 1e-4, b 128, sabit val bölmesi) | `results/q1/konsey_smoke/egitim_v_in.log`, `egitim_v_rand.log`, "Best accuracy" satırı |
| 200 iterasyon temiz eğitim, R224 | Geçti: R224-IN %79,25, rastgele başlatma %34,45 | `egitim_r_in.log`, `egitim_r_scr.log` |
| AT CLI yolu (`--optimizer adamw -e 100 --stop-epoch 1`, 20 batch) | Geçti: zorlanmış AdamW (wd 0,05), çizelge T_max 100, birinci epok sonrası lr 0,0009997532801828658; `TRAINING_COMPLETE`'te `stop_epoch=1`, `stopped_at_cap=True`; `--save-every 1` epok kontrol noktası yazdı | `results/q1/konsey_smoke/egitim_r_in_at.log` (AT kontrol noktası yer açmak için sonradan silindi) |
| Transfer matrisi, 3 model (`resnet18_224`, C1 ViT, Sehwag2021Proxy_R18), n = 200, `--cache-adv` | Geçti: 9 hücre, önbelleğe 3 kaynak yazıldı | `results/q1/konsey_smoke/matris_uc/`, `matris_uc.log` |
| Önbellekten yeniden koşu | Geçti: üç kaynak önbellekten okundu, `matris_uc` ile birebir | `karsilastirma_uc_tekrar.json` |
| `--skip-existing` ile model ekleme (B2'den B4'e akış): 3 modellik klasöre `vit_tiny_in1k` ve XCiT eklendi | Geçti: 9 hücre "mevcut hücre" olarak okundu, 16 yeni hücre hesaplandı; boş klasörde aynı 5 modelle yapılan koşuyla 25 hücre birebir | `matris_ekle.log`, `karsilastirma_ekle_taze.json` |
| Önbelleğin sıra bağımsızlığı: boş önbellek, ters model sırası | Geçti: üç kaynağın çekişmeli örnek dizileri birebir (en büyük fark 0,0), ortak 9 hücre birebir; karşılaştırma dosyasında `BIREBIR: false` yalnız model listelerinin farklı olmasından gelir | `karsilastirma_uc_ters.json`, `karsilastirma_uc_taze_ortak.json` |
| MI-PGD eşitliği | Geçti: matris kodundaki `mifgsm_m84`, `experiments/run_c_addenda.py::mifgsm` (föy M8.4, C22) ile aynı batch'te birebir; L∞ 0,03137 | `results/q1/konsey_smoke/mi_tgr_esitlik.json` |
| TGR eşitliği | Geçti: matrisin TGR çağrısı `experiments/c1_c2_tgr.py::mifgsm(use_tgr=True)` ile birebir, düz MI-FGSM'den farklı | aynı dosya |
| `--attack mi --sources ResNet18_AT_s1001` | Geçti: tek kaynak, üç hedef; JSON'da `alpha` 0,003137 (ε/10) | `matris_mi/transfer_matrix.json` |
| `--attack tgr` | Geçti: ResNet18_AT_s1001 ve WRN_28_10 kaynak olarak atlandı, iki ViT kaynağı (C1 ViT, `vit_tiny_in1k`) koştu | `matris_tgr.log` |
| Panel yükleme (B2 smoke): yedi panel üyesi ve XCiT | Geçti: dokuz modelin hepsi yüklendi ve n = 200 matriste koştu (29 s) | `matris_panel.log` |
| AutoAttack betiği yeni tiple (`vit_tiny_in1k`, n = 50) | Geçti | `results/q1/konsey_smoke/aa/autoattack_summary.json` |
| Kuyruk yardımcısı | Geçti: tavan 80 okundu; V-IN temiz denetimi GEÇTİ (val %92,85, C1 ViT temiz ortalaması %83,00); R224-IN denetimi referans yokken ERTELENDİ; çöküş denetimi 1 epokta BEKLE; özet satırı üretildi | `results/q1/konsey_smoke/denetim_yardimcisi.txt` |
| Kuyruk `--dry-run` | Geçti: komutlar basıldı, defter oluşmadı | `results/q1/konsey_smoke/kuyruk_dry_run.txt` |

## 4. Regresyon

Değişiklik öncesi kod HEAD (4972738) için depo içinde geçici bir git worktree'ye alındı, iki C1 modeli (ResNet18_AT_s1001, ViT_Tiny_AT_s2001) varsayılan bayraklarla n = 200'de eski ve yeni kodla ayrı ayrı koşturuldu. Varsayılan davranış gereği RobustBench referansı (WRN_28_10, Gowal2020Uncovering_28_10_extra) otomatik eklendiğinden matris 3x3'tür. Eski ile yeni koşu arasında 9 hücrenin JSON değerleri ve 9 npz dosyasının dört dizisi birebir aynıdır; ayrıca eski kodun iki koşusu da birbirinin aynısıdır, yani karşılaştırma GPU belirlenimsizliğine karşı da sağlamdır (`results/q1/konsey_smoke/regresyon/karsilastirma_eski_yeni.json` ve `karsilastirma_eski_eski2.json`, `BIREBIR: true`). Worktree kaldırıldı; konteynerin yazdığı root sahipli `__pycache__` dosyaları yüzünden `git worktree remove` yarıda kaldığı için kalan klasör sahiplik düzeltildikten sonra elle silindi ve `git worktree prune` çalıştırıldı.

## 5. İndirmeler

Boyutlar indirmeden önce HTTP başlıklarından öğrenildi (Google Drive için `content-range`, Hugging Face için `x-linked-size`); toplam 209 493 962 bayt (yaklaşık 209 MB) olduğundan indirme yapıldı. İndirilen dosyaların boyutları başlıklarla aynıdır (`results/q1/konsey_smoke/indirmeler.json`).

| Model | Kaynak | Bayt | sha256 (ilk 12) |
|---|---|---|---|
| Sehwag2021Proxy_R18 | RobustBench, gdrive `1-ZgoSlD_AMhtXdnUElilxVXnzK2DcHuu` | 44 763 573 | cc35dcef82a7 |
| Addepalli2022Efficient_RN18 | RobustBench, gdrive `1m5vhdzIUUKhDbsZdOG9z76Eyp6f4xe_f` | 44 778 553 | a8fd58136e2e |
| Rade2021Helper_R18_ddpm | RobustBench, gdrive `1f2yJUo-jxCQNk589frzriv6wPyrQEZdX` | 50 261 042 | 1d70d209474e |
| deit_tiny_patch16_224.fb_in1k | HF `timm/...`, model.safetensors | 22 883 348 | 21d4764d94f6 |
| resnet18.a1_in1k | HF `timm/...`, model.safetensors | 46 807 446 | 80c49dee3da4 |

Debenedetti2022Light_XCiT-S12 indirilmedi; konteynerin torch hub önbelleğindeki `debenedetti2022light-xcit-s-cifar10-linf.pth.tar` (103 647 475 bayt) `models/robustbench_zoo/cifar10/Linf/Debenedetti2022Light_XCiT-S12.pth.tar` olarak kopyalandı, iki dosyanın sha256'sı aynıdır (20c1be6fd4af...). RobustBench 1.1 bu modeli `models/robustbench_zoo`'dan değil timm yolundan yüklediği için kopya yedek işlevi görür; hub dosyası silinirse `experiments/c1_c3_transfer_matrix.py::_restore_rb_timm_cache` onu kopyadan geri koyar. Yeni üç modelin parametre sayıları 11 173 962, 11 173 962 ve 12 548 426'dır.

## 6. Zaman pilotu ve seçilen tavan

Ölçüm `scripts/konsey_pilot_zaman.py` ile, her hücrede gerçek eğitim bileşenleriyle yapıldı: 5 ısınma ve 50 ölçülen AT iterasyonu (batch 64; karışık kayıplı AT, PGD-10, AdamW lr 1e-3, gradyan kırpma 10), 5 ısınma ve 50 ölçülen temiz iterasyon (batch 128), epok sonu değerlendirmesi olarak 2000 örneklik doğrulama bölmesinde temiz ileri geçiş ve PGD-10 (5 batch ölçülüp 20 batch'e ölçeklendi). Epok süresi iterasyon süresinin epok başına iterasyon sayısıyla (AT 750, temiz 375) çarpımına değerlendirme süresinin eklenmesiyle bulundu.

| Hücre | AT iterasyonu (s) | Temiz iterasyon (s) | AT epoğu (s) | Temiz epok (s) | Tepe bellek (GiB) |
|---|---|---|---|---|---|
| V_IN | 0,1614 | 0,0343 | 125,8 | 13,4 | 3,8 |
| R224_IN | 0,1839 | 0,0405 | 142,7 | 15,5 | 3,0 |
| R224_scr | 0,1837 | 0,0404 | 142,5 | 15,5 | 3,0 |

Kaynak: `results/q1/konsey_pilot_zaman.json` ve `results/q1/konsey_pilot_zaman_parca_*.json`. Bekçi kuralıyla W(80) = 20,47 sa, W(70) = 18,19 sa, W(60) = 15,90 sa bulundu; W(80) eğitim payı 38,15 sa'in altında kaldığından seçilen tavan 80'dir. R224 AT epoğu 365 s eşiğinin altında olduğundan "eğitim başlamaz" bayrağı kalkmamıştır (`egitim_baslamaz: false`, `r224_esik_asildi: false`). Tavanda koşu başına üst süre V_IN 2,91 sa, R224_IN 3,30 sa, R224_scr 4,03 sa'tir (`kosu_basina_beklenen_sa_tavanda`). Plandaki durma epoklarıyla (ViT 45, R224 77; `KONSEY_PLANI.md` §4) beklenen toplam yaklaşık 17,5 sa'tir; bu değer pilot epok süreleriyle elle hesaplanmıştır: 2 × [(30 × 13,4 + 45 × 125,8) + (30 × 15,5 + 77 × 142,7) + (200 × 15,5 + 77 × 142,5)] / 3600.

Ölçüm anında GPU'da yaklaşık 3,77 GB bellek başka bir süreç tarafından tutuluyordu (histo-sparse-adv konteyneri çalışır durumdaydı), ancak kullanım her ölçümden önce alınan beş örnekte %1-2 idi; JSON'daki `olcum_sismis_olabilir` alanı bu yüzden `false`'tur ve uyarı listesine bellek notu düşülmüştür. Ters yönlü risk daha önemlidir: aynı ViT-Tiny AT iterasyonu E2 kampanyasında yaklaşık 0,32 s sürmüştür (`logs/Q1_e2_at_vit_tiny_2001.log`, birinci epok, 688 iterasyonun 686'ncısı 03:39'da), pilot ise 0,16 s ölçmüştür. Eğitim GPU paylaşılarak koşulursa süreler iki katına yaklaşabilir; bu durumda W(80) 40,94 sa olur ve payı aşar (`paylasimda_iki_kat_yavaslama_W_sa`). Pilot, plandaki R3 tahmininden (R224 AT 310 s) belirgin biçimde hızlı çıkmıştır; C1 ViT AT eğitim döngüsü ise `logs/C1_at_vit_2002.log`'da epok başına yaklaşık 2:46-2:51 sürmüştür.

## 7. Kuyruk ve `--dry-run` çıktısı

Kuyruk `scripts/konsey_b3_kuyruk.sh` konteyner içinde koşar. Sırası V_IN_s2101, R224_IN_s1301, R224_scr_s1201, V_IN_s2102, R224_IN_s1302, R224_scr_s1202'dir. Tavanı pilot JSON'dan okur; `egitim_baslamaz` ise başlamaz. Her aşamadan önce boş diski ve `nvidia-smi` çıktısını kaydeder, disk 15 GB'ın altındaysa durur. `results/q1/konsey_b3_defter.tsv` dosyasına başlangıç, bitiş, süre, epok, durum, boş disk, GPU belleği ve kullanımı ile notu yazar ve her aşamadan sonra toplam eğitim saatini paya karşı basar. Biten aşamayı (`TRAINING_COMPLETE`) atlar; yarıda kalan aşama baştan başlamaz, `--resume` ile `last.pth`'tan devam eder ve yarıda kalan epok yeniden koşulur. RNG durumu kontrol noktasında saklanmadığı için devam eden koşu kesintisiz koşuyla bit düzeyinde aynı değildir.

ON_KAYIT §4'ün iki denetimi kuyruğa bağlanmıştır. Temiz aşama denetimi her IN koşusunun temiz aşamasından sonra yapılır; V-IN referansı C1 ViT-Tiny temiz `best.pth` doğruluklarının ortalamasıdır (%83,00), R224-IN referansı biten R224-scr temiz aşamalarının ortalamasıdır. KALDI sonucunda kuyruk AT'ye geçmeden durur. AT çöküş kuralı IN koşularında beş dakikada bir `last.pth` geçmişinden okunur; 5. epok doğrulama PGD doğruluğu %15'in altındaysa eğitim durdurulur ve kuyruk 5 koduyla kapanır; lr 5e-4'e geçiş kararı otomatik verilmez. AT bittiğinde seçilen epok, koşulan epok ve "kırpılmış olabilir" işareti (seçilen epok ≥ tavan − 5) deftere yazılır.

`--dry-run` çıktısı (`results/q1/konsey_smoke/kuyruk_dry_run.txt`, ilk iki koşu; kalan dört koşu aynı kalıptadır, tohum ve takma ad değişir):

```text
# KURU KOSU (--dry-run): komutlar yalniz basilir, hicbir sey calismaz
# pilot: results/q1/konsey_pilot_zaman.json  tavan: 80  egitim payi: 38.15 sa  disk esigi: 15 GB
# her asamadan once: df -BG /workspace (< 15 GB ise dur) ve nvidia-smi kaydi
## V_IN_s2101
[temiz] python -m cli.main train clean -m vit_tiny_in1k --init-weights deit_tiny_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed 2101 --val-indices data/val_split_indices.json -o models/q1/konsey/V_IN_s2101 --resume   # atla: models/q1/konsey/V_IN_s2101/vit_tiny_in1k/clean/TRAINING_COMPLETE varsa
[denetim] python scripts/konsey_b3_denetim.py temiz --takma V_IN_s2101   # KALDI ise dur (kod 3)
[AT]    python -m cli.main train adversarial -m vit_tiny_in1k -d adversarial_training -p models/q1/konsey/V_IN_s2101/vit_tiny_in1k/clean/best.pth --optimizer adamw -e 100 --stop-epoch 80 --lr 0.001 -b 64 --patience 20 --val-indices data/val_split_indices.json --save-every 10 --seed 2101 -o models/q1/konsey/V_IN_s2101 --resume   # atla: models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/TRAINING_COMPLETE varsa
[izleme] her 5 dk: python scripts/konsey_b3_denetim.py cokus --takma V_IN_s2101   # 5. epok val PGD < %15 ise egitim durdurulur (kod 5)
[ozet]  python scripts/konsey_b3_denetim.py ozet --takma V_IN_s2101 --tavan 80
## R224_IN_s1301
[temiz] python -m cli.main train clean -m resnet18_224_in1k --init-weights resnet18_a1_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed 1301 --val-indices data/val_split_indices.json -o models/q1/konsey/R224_IN_s1301 --resume   # atla: models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/clean/TRAINING_COMPLETE varsa
[denetim] python scripts/konsey_b3_denetim.py temiz --takma R224_IN_s1301   # KALDI ise dur (kod 3)
[AT]    python -m cli.main train adversarial -m resnet18_224_in1k -d adversarial_training -p models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/clean/best.pth --optimizer adamw -e 100 --stop-epoch 80 --lr 0.001 -b 64 --patience 20 --val-indices data/val_split_indices.json --save-every 10 --seed 1301 -o models/q1/konsey/R224_IN_s1301 --resume   # atla: models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/TRAINING_COMPLETE varsa
[izleme] her 5 dk: python scripts/konsey_b3_denetim.py cokus --takma R224_IN_s1301   # 5. epok val PGD < %15 ise egitim durdurulur (kod 5)
[ozet]  python scripts/konsey_b3_denetim.py ozet --takma R224_IN_s1301 --tavan 80
## R224_scr_s1201
[temiz] python -m cli.main train clean -m resnet18_224 --init-weights none --optimizer adamw --lr-schedule cosine -e 200 --lr 0.001 -b 128 --seed 1201 --val-indices data/val_split_indices.json -o models/q1/konsey/R224_scr_s1201 --resume   # atla: models/q1/konsey/R224_scr_s1201/resnet18_224/clean/TRAINING_COMPLETE varsa
[denetim] ertelenmis R224_IN temiz denetimleri bu asamadan sonra yeniden yapilir
[AT]    python -m cli.main train adversarial -m resnet18_224 -d adversarial_training -p models/q1/konsey/R224_scr_s1201/resnet18_224/clean/best.pth --optimizer adamw -e 100 --stop-epoch 80 --lr 0.001 -b 64 --patience 20 --val-indices data/val_split_indices.json --save-every 10 --seed 1201 -o models/q1/konsey/R224_scr_s1201 --resume   # atla: models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/TRAINING_COMPLETE varsa
[ozet]  python scripts/konsey_b3_denetim.py ozet --takma R224_scr_s1201 --tavan 80
```

## 8. Transfer matrisi bayraklarının sözleşmesi

Varsayılan bayraklarla kod eski kodla aynıdır; yeni JSON alanları (`attack`, `sources`, `cache_adv`, `per_source_seed`, `model_specs`) ve `cells_meta.json` yalnız yeni bayraklardan biri kullanıldığında yazılır. `--cache-adv` açıkken her kaynaktan önce `set_seed(seed)` çağrılır; bu, bir kaynağın PGD rastgele başlangıcını kaynak sırasından ve listedeki diğer modellerden bağımsız kılar ve B2 önbelleğini B4'te geçerli tutar (sıra testi, Bölüm 3). Bunun bedeli, önbellekli koşunun önbelleksiz eski koşuyla rastgele başlangıç bakımından bit düzeyinde aynı olmamasıdır; B2'deki C1 hücreleri bu yüzden `results/c1_c3/` altındaki eski C1 matrisleriyle örnek düzeyinde özdeş olmayacaktır, istatistik olarak aynı protokolü ölçer. Önbellek dosyası kaynak, saldırı, norm, adım, n, tohum ve veri kümesiyle adlandırılır; meta dosyasındaki ayarlar ve kontrol noktasının sha256'sı uyuşmazsa koşu durur. `--skip-existing` hücre düzeyinde çalışır ve dosyadaki hedef temiz maskesi yeni hesaplananla aynı değilse durur.

MI-PGD (`--attack mi`) föy M8.4'ün kaynağı olan `run_c_addenda.py` C22 uygulamasının kopyasıdır: μ = 1,0, α = ε/adım (10 adımda ε/10), L1 toplam normalizasyonu, rastgele başlangıç yok. TGR (`--attack tgr`) `c1_c2_tgr.py` modülünü dosya yolundan yükleyip `mifgsm(use_tgr=True)` fonksiyonunu doğrudan çağırır; ayarlar C2'deki gibidir (α = 2/255, μ = 1,0, ortalama mutlak değer normalizasyonu).

## 9. Plandan sapmalar, kararlar ve açık sorular

1. AT çizelgesi. Plan taslağındaki komut (`KONSEY_PLANI.md` §7) `-e <TAVAN>` kullanıyordu; bu, kosinüs çizelgesini T_max = tavan ile kurar ve V-scr'nin (C1, T_max = 100) çizelgesinden ayrılır. Örneğin 45. epokta lr, T_max = 80 iken yaklaşık 4,0e-4, T_max = 100 iken yaklaşık 5,8e-4 olur. "AT tarifi dört hücrede C1 ViT ile aynıdır" hükmünü korumak için kuyruk `-e 100 --stop-epoch <TAVAN>` kullanır. Ana oturumun bu kararı onaylaması ve ON_KAYIT'a yazması gerekir.
2. ON_KAYIT ile K3 çelişkisi. `ON_KAYIT_TASLAGI.md` §3 tablosunda R224-scr satırı "model içi ImageNet normalizasyonu" der, `KONSEY_PLANI.md` §4 B3 tablosu da öyledir; K3 kararıyla kod R224-scr'de normalizasyon uygulamaz. Dondurmadan önce iki tablodaki R224-scr satırı ve "V-scr'de girdi normalizasyonu yoktur" cümlesi K3'e göre düzeltilmelidir (normalizasyon başlatma demetinin parçasıdır, iki scr hücresinde de yoktur). `hucre_tablosu.json` zaten K3 ile uyumludur.
3. Üçüncü kayıt adı. K3'ün tipe bağlı uygulanması için `resnet18_224_in1k` adı eklendi; görev metni yalnız `resnet18_224` ve `vit_tiny_in1k` adlarını sayıyordu. Takma adlar (K5) değişmedi.
4. B5'te MI ile TGR'nin adım boyu farklıdır (ε/10 ile 2/255). Görev metni "MI için M8.4, TGR c1_c2_tgr.py'den taşınır" dediği için ikisi de kaynağındaki gibi bırakıldı. "Her kaynağın en iyi saldırısı" karşılaştırmasında bu farkın beyan edilmesi ya da TGR'nin `--steps` dışında α = ε/10 ile de koşturulması ana oturumun kararıdır; kod şu an TGR α'sını değiştirme bayrağı sunmaz.
5. Temiz aşama kosinüs seçeneği. `Trainer` zaten her durumda kosinüs (T_max = epok) kullanıyordu; `--lr-schedule {cosine,constant}` bayrağı varsayılanı değiştirmeden eklendi. `--save-every` iki komutta da önceden vardı.
6. Zorlanmış AdamW ağırlık azaltması 0,05'tir ve ViT LR tavanı uygulanmaz; V-IN AT lr 1e-3 tavanla aynı olduğu için C1 tarifinden fark doğmaz.
7. R224-IN temiz denetiminin referansı sıra gereği ilk R224-IN koşusundan sonra oluşur; R224_IN_s1301'in AT'si denetim ERTELENDİ iken başlar, denetim R224_scr_s1201 temiz aşamasından sonra yapılır. Ağırlık yükleme hatası ise yükleme sırasında katı rapor kuralıyla yakalanır (baş dışında tek uyumsuzluk eğitimi başlatmaz). ON_KAYIT §4 metni "C1 ya da kendi temiz aşama doğruluğu" dediği için bu uygulamanın ana oturumca onaylanması gerekir.
8. İki başlatma kontrol noktasının ImageNet top-1 değerleri (`KONSEY_PLANI.md` §2, R2 Saldırı 2 satırı) timm model kartından henüz alınmadı.
9. Pilot boş GPU'da ölçüldü; eğitim paylaşımlı GPU'da koşulursa bekçinin varsayımı bozulabilir (Bölüm 6). Kuyruk gerçek süreleri deftere yazar ve toplamı paya karşı basar, ama payı aşınca kendiliğinden durmaz.

## 10. Test edilmeyenler

n = 10000 ölçekli hiçbir koşu yapılmadı (B2, B4, B5, B6 kullanıcıya bırakıldı). B3 kuyruğu yalnız `--dry-run` ve yardımcı alt komutlarla sınandı; gerçek bir koşu, kesinti sonrası devam, disk eşiğinde durma, çöküş izleyicisinin eğitimi durdurma yolu ve defter yazımı uçtan uca koşturulmadı. Temiz aşama `--resume` yolu bu oturumda denenmedi (mevcut kod yoludur). `experiments/q1_konsey_ayrisim.py` başka bir ajanın işidir ve bu raporda sınanmadı; runbook yalnız K6 arayüzüyle çağırır.

## Doğrulayıcı düzeltmeleri

Çelişik doğrulayıcının bulduğu on sorunun onu da ikinci turda ele alınmıştır. Bu bölüm yukarıdaki §3'ün kuyruk yardımcısı satırını, §7'deki `--dry-run` çıktısını ve §9'daki 1, 4 ve 7 numaralı açık soruları geçersiz kılar; güncel kuru koşu çıktısı `results/q1/konsey_smoke/kuyruk_dry_run.txt` dosyasındadır. Sınama betikleri ve kayıtları `results/q1/konsey_smoke/_dogrulayici/` altında `t2_` önekiyle durur.

1. Temiz aşama kapısının tek seferlik çalışması giderildi. `scripts/konsey_b3_kuyruk.sh` artık defterdeki eski denetim satırına hiç bakmaz: AT'si bitmemiş her IN koşusunda denetim, kuyruk her başlatıldığında AT'den hemen önce yeniden yapılır ve GECTI dışında bir sonuçta AT başlamaz (`in_at` ve `temiz_denetim` işlevleri). Sahte eğiticili uçtan uca sınamada (`_dogrulayici/t2_kuyruk/sinama.sh`, kayıt `t2_kuyruk/sinama.log`) R224-IN ilk epoğu 38, referans 35 iken kuyruk iki ardışık başlatmada da kod 3 ile durdu ve R224_IN_s1301 için AT klasörü oluşmadı; temiz klasör silinip ilk epok 80 yapılınca koşu yeniden eğitildi, denetim GECTI verdi ve kuyruk tamamlandı. V-IN için aynı sınama (ilk epok 28) iki başlatmada da kod 3 verdi ve yalnız bir temiz çağrı yapıldı. Sınama için kuyruğa yalnız sınamada kullanılan bir kök dizin değişkeni (`KONSEY_B3_KOK`, boşsa `/workspace`) eklendi.

2. Temiz aşama ölçütü yeniden tanımlandı ve ön kayda yazıldı (`ON_KAYIT_TASLAGI.md` §4 ve §8 madde 17). Karşılaştırma artık temiz aşamanın ilk epoğu sonundaki doğrulama doğruluğuyla yapılır: V-IN, C1 ViT-Tiny temiz koşularının ilk epok ortalamasından (23,75; 26,55; 25,35, ortalama 25,22; `logs/C1_clean_vit_200[123].log`, `Epoch 1/200` satırları, çıkaran betik `_dogrulayici/t2_c1_ilk_epok.py`), R224-IN ise en az bir epoğu biten R224-scr temiz koşularının ilk epoğundan (`last.pth`, `history.test_acc[0]`) en az 5 puan yüksek olmalıdır. Son epok doğruluğu yalnız betimsel olarak deftere yazılır. Mevcut C1 temiz `best.pth` ve `last.pth` dosyalarında epok geçmişi yoktur (`_dogrulayici/t2_gecmis_kontrol.py`); bu yüzden C1 referansı loglardan okunur, yeni koşularda ise eğitici geçmişi `last.pth` içine yazdığından oradan okunur, yoksa `logs/konsey_b3/<takma ad>_temiz.log` kullanılır. Doğrulayıcının ikinci kaygısı, yani R224_IN_s1301'in AT'sinin denetimi ertelenmişken koşması da giderildi: referans yoksa bu koşunun AT'si bekletilir, R224_scr_s1201 temiz aşaması bitince denetim yapılır ve geçerse önce R224_IN_s1301'in, sonra R224_scr_s1201'in AT'si koşar. Sınamadaki çağrı sırası şudur: V_IN_s2101 temiz ve AT, R224_IN_s1301 temiz, R224_scr_s1201 temiz, R224_IN_s1301 AT, R224_scr_s1201 AT, ardından ikinci tohumlar özgün sırayla. Toplam iş değişmez, yalnız bir AT bir temiz aşamadan sonraya kayar. Bu ölçüt değişikliğinden önce smoke temiz doğrulukları görülmüştü; ön kayıt §8 madde 17 bunu açıkça yazar.

3. `experiments/c1_c3_transfer_matrix.py` artık `--cache-adv` verilmeden `--skip-existing` kullanılmasını reddeder (argüman ayrıştırmasından hemen sonra, model yüklenmeden). Doğrulayıcının önerdiği ikinci yol, yani `--skip-existing` ile de kaynak başına tohum atmak, seçilmedi; çünkü ilk koşu önbelleksiz ve tek tohumla yapılmışsa devam koşusu yine farklı örnek üretirdi. Sınama: önbelleksiz `--skip-existing` çağrısı çıkış kodu 1 ve açıklayıcı iletiyle durdu, çıktı klasörü oluşmadı (`_dogrulayici/t2_sinamalar.log`, madde 1). Varsayılan yol değişmediğinden regresyon sonucu (§4) geçerliliğini korur. Runbook iki bayrağı zaten birlikte kullanıyordu; ilgili cümle eklendi.

4. B6 maskeleme kuralı için PGD-10 doğruluğu artık AA ile aynı örneklemden alınır. Yeni betik `scripts/konsey_b6_maskeleme.py`, AA'nın `per_sample_{m}.npz` dosyasındaki `robust_correct` ile B4 köşegenindeki `per_sample_{m}_to_{m}.npz` dosyasının `target_adv_wrong` alanını yalnız ilk n = 1000 görüntüde karşılaştırır, iki çıktının temiz doğru maskelerini de denetler (uyuşmazlık %1'i aşarsa hata) ve işaretli modeller için `--maskeleme-isaretli` dizgisini üretir. İki çıktının da test kümesini karıştırmadan sırayla okuduğu kodda doğrulandı (`run_autoattack_run2.py` ilk n örneği toplar; transfer matrisi `_iter_batches` ile ilk n örneği verir; test yükleyicisi `shuffle=False`). Smoke: V_IN_smoke için AA n = 50 ile `matris_ekle` köşegeni karşılaştırıldı; temiz maske uyuşmazlığı 0, PGD-10 ve AA doğruluğu ikisi de 0,00 çıktı (`results/q1/konsey_smoke/b6_maskeleme_smoke.json`). Smoke modeli çekişmeli eğitilmediği için bu sınama yalnız düzeneği ve örneklem eşleşmesini gösterir, farkın hesabını anlamlı bir değerle sınamaz. AA'dan uzun n istendiğinde betik hata verdi. `KONSEY_RUNBOOK.md` §6 ve §7 ile `ON_KAYIT_TASLAGI.md` §5 B6 buna göre yazıldı.

5. `KONSEY_PLANI.md` §7'deki örnek AT komutu `-e 100 --stop-epoch <TAVAN>` olarak düzeltildi, temiz komutuna `--lr-schedule cosine` ve denetim satırı eklendi. Kosinüs çizelgesinin T_max = 100 ile kurulduğu ve tavanın `--stop-epoch` ile uygulandığı `ON_KAYIT_TASLAGI.md` §3'e ve §8 madde 19'a yazıldı. §9'daki açık soru 1 böylece kapanmıştır, ancak dondurma kararı ana oturumundur.

6. `KONSEY_PLANI.md` §6 tablosuna üçüncü kayıt adı `resnet18_224_in1k` eklendi ve üç kaydın hangi hücreye karşılık geldiği yazıldı.

7. AT çöküş kuralı kuyruğa bayrakla eklendi ve ön kayıt metni işleme göre yazıldı. Kuyruk kural tetiklenince kod 5 ile durur; kullanıcı aynı komutu `--in-at-lr 0.0005` ile yeniden verir. Kuyruk her AT klasörüne kullanılan lr'yi `at_lr.txt` olarak yazar; lr'si istenenden farklı IN AT klasörlerini (bitmiş ya da yarım) silmeden `adversarial_training__lr<eski>_<zaman>` adıyla yanına taşır, deftere `TASINDI` satırı yazar ve AT'yi yeni lr ile baştan koşar. R224-scr AT lr'si 1e-3'te sabit kalır, temiz aşamalar yeniden kullanılır. Sahte eğiticili sınamada (senaryo D) tamamlanmış kuyruk `--in-at-lr 0.0005` ile yeniden verildiğinde dört IN AT klasörü taşındı ve yalnız bu dört AT lr 5e-4 ile yeniden çağrıldı; aynı komutun tekrarı hiçbir eğitim çağırmadı (senaryo D2). En kötü durumdaki ek süre `ON_KAYIT_TASLAGI.md` §4'e yazıldı: kural son IN koşusunda (R224_IN_s1302) tetiklenirse üç IN AT'sinin tavanda yeniden eğitimi ve boşa giden yaklaşık beş epok, pilot değerleriyle 2 × 80 × 125,8 + 80 × 142,7 + 5 × 142,7 = 32257,5 s, yani yaklaşık 8,96 sa (`results/q1/konsey_pilot_zaman.json`, `t_V_at_epok_s`, `t_R224_IN_at_epok_s`, `secilen_tavan`). W(80) = 20,47 sa ile toplam yaklaşık 29,4 sa'tir ve 38,15 sa'lik payın içinde kalır; GPU paylaşımlı koşuda bu güvence yoktur. Çöküş izleyicisinin eğitimi gerçekten durdurma yolu (5 dakikalık bekleme döngüsü) sınamada koşturulmadı, çünkü sahte eğitici anında bitiyor.

8. `raporlar/konsey_2026-10-29/_rb_liste.json` ve `_rb_imagenet_P2.json` ile bu turda konteynerin oluşturduğu `__pycache__` dosyaları `chown -R 1000:1000` ile firat'a verildi; `raporlar/konsey_2026-10-29`, `results/q1/konsey_smoke`, `scripts`, `experiments`, `src` ve `cli` altında root sahipli dosya kalmadı.

9. `src/training/adversarial_trainer.py` içinde `train_loss`, `max_train_batches > 0` iken koşulan batch sayısına bölünür (`trainer.py` ile aynı düzeltme). Yalnız derleme sınandı (`py_compile`); kısa bir AT smoke koşusu bu turda yapılmadı. Değişiklik yalnız smoke kipindeki basılan kaybı etkiler, eğitim ve seçim yolunu etkilemez.

10. B5'te TGR'nin ayarları (α = 2/255, μ = 1,0, γ = 0,5; `experiments/c1_c2_tgr.py` satır 38 ve 59) ve MI-PGD ile adım boyu farkının bilinçli olduğu `ON_KAYIT_TASLAGI.md` §5 B5'e ve §8 madde 20'ye yazıldı. Kod değişmedi; §9'daki açık soru 4, TGR'nin α = ε/10 ile ayrıca koşturulmaması kararıyla kapanmıştır. Bu kararın ana oturumca onaylanması gerekir.

Güncel kuyruk `--dry-run` çıktısının ilk iki koşusu (kalan dört koşu aynı kalıptadır):

```text
# KURU KOSU (--dry-run): komutlar yalniz basilir, hicbir sey calismaz
# pilot: results/q1/konsey_pilot_zaman.json  tavan: 80  egitim payi: 38.15 sa  disk esigi: 15 GB  IN AT lr: 0.001  R224_scr AT lr: 0.001
# her asamadan once: df -BG /workspace (< 15 GB ise dur) ve nvidia-smi kaydi
# IN kosularinda AT'den once denetim her baslatmada yeniden yapilir; GECTI olmadan AT baslamaz
## V_IN_s2101
[temiz] python -m cli.main train clean -m vit_tiny_in1k --init-weights deit_tiny_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed 2101 --val-indices data/val_split_indices.json -o models/q1/konsey/V_IN_s2101 --resume
[denetim] python scripts/konsey_b3_denetim.py temiz --takma V_IN_s2101   # ilk epok val >= C1 ViT ilk epok ort. + 5; KALDI ise dur (kod 3)
[AT-on] .../adv/adversarial_training/at_lr.txt (yoksa 0.001) != 0.001 ise klasor adversarial_training__lr<eski>_<zaman> adiyla tasinir
[AT]    python -m cli.main train adversarial -m vit_tiny_in1k -d adversarial_training -p models/q1/konsey/V_IN_s2101/vit_tiny_in1k/clean/best.pth --optimizer adamw -e 100 --stop-epoch 80 --lr 0.001 -b 64 --patience 20 --val-indices data/val_split_indices.json --save-every 10 --seed 2101 -o models/q1/konsey/V_IN_s2101 --resume
[izleme] her 5 dk: python scripts/konsey_b3_denetim.py cokus --takma V_IN_s2101   # 5. epok val PGD < %15 ise egitim durdurulur (kod 5); yeniden baslatma: --in-at-lr 0.0005
[ozet]  python scripts/konsey_b3_denetim.py ozet --takma V_IN_s2101 --tavan 80
## R224_IN_s1301
[temiz] python -m cli.main train clean -m resnet18_224_in1k --init-weights resnet18_a1_in1k ... --seed 1301 ... -o models/q1/konsey/R224_IN_s1301 --resume
[denetim] python scripts/konsey_b3_denetim.py temiz --takma R224_IN_s1301   # ilk epok val >= R224_scr ilk epok ort. + 5; ERTELENDI ise AT, R224_scr temiz asamasindan sonraya kalir; KALDI ise dur (kod 3)
[AT]    python -m cli.main train adversarial -m resnet18_224_in1k ... -e 100 --stop-epoch 80 --lr 0.001 ... --seed 1301 -o models/q1/konsey/R224_IN_s1301 --resume
```

Bu turda da test edilmeyenler: gerçek eğiticiyle kuyruk koşusu, çöküş izleyicisinin eğitimi durdurması, disk eşiğinde durma ve `adversarial_trainer.py` kayıp düzeltmesinin koşu içinde gözlenmesi. Yeni ilk epok ölçütünün gerçek koşularda beklenen farkı verip vermediği B3'ün ilk temiz aşamasında görülecektir; smoke değerleri (yaklaşık yarım epokta V-IN 92,85, R224-IN 79,25, R224-scr 34,45) eşiğin rahatça aşılacağını düşündürür, ama bu bir sınama değildir.
