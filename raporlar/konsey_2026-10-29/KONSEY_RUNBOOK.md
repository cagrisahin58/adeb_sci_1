# Konsey runbook: B2, B3, B4, B5, B6 ve çözümlemeler (29.10.2026)

Bu dosya, konsey planındaki (`KONSEY_PLANI.md` §4, §7) kullanıcı bloklarının sırasıyla çalıştırılacak tam komutlarını verir. Bütün komutlar WSL'de depo kökünden (`/home/firat/projects/adeb_sci_1`) yazılmıştır; Python işleri `adeb_eval` konteynerinde `/workspace` altında koşar. Kodun ve smoke testlerinin ayrıntısı `05_kod_raporu.md` dosyasındadır.

Ön koşul, yani B2'den önce mutlaka yapılması gereken iş: ön kayıt dosyası `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` (dondurulmuş hali) ile çözümleme betiği ve hücre tablosu, B2 başlamadan önce depoya işlenmiş olmalıdır. Bunu yapan yerel commit betiği `arsiv/b2_yardimci/_konsey_commit1.sh` dosyasıdır ve ana oturum tarafından çalıştırılır. Dondurma commit'i B2'den önce yapılmazsa B2 sonuçları ön kayıttan önce görülmüş sayılır ve ön kaydın değeri düşer. Commit'ten sonra `git push` önerilir: yerel commit'in tarihi elle değiştirilebilir, uzak depoya gönderilmiş commit ise dışarıdan doğrulanabilen bir zaman damgası taşır. B2'yi başlatmadan önce şu iki satırla denetlenir:

```bash
git log -1 --format='%h %ad %s' --date=iso -- raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md   # bos cikarsa B2 baslamaz
sha256sum experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json         # ON_KAYIT Dondurma eki (a) ile ayni olmali
```

Takma adlar fable kararı K5 ile aynıdır. Hücre tablosu konteyner içinden göreli yolla okunur (`raporlar/konsey_2026-10-29/hucre_tablosu.json`), çünkü K6'daki mutlak WSL yolu konteynerde yoktur; iki yol aynı dosyayı gösterir.

## 0. Her bloktan önce

```bash
cd /home/firat/projects/adeb_sci_1
docker start adeb_eval >/dev/null
nvidia-smi        # başka konteynerin (histo-sparse-adv) bellek ve kullanımı; 12 GB üstü kullanım deftere not edilir
df -h /home/firat # B3 başlangıcında en az 30 GB (§3); kuyruk 15 GB altında kendiliğinden durur, önbellek silinebilir (KONSEY_PLANI §10)
```

GPU başka bir işle paylaşılırken koşulan bloklar uzar. Zaman pilotu boş GPU'da ölçüldü (`results/q1/konsey_pilot_zaman.json`); aynı ViT-Tiny AT iterasyonu E2 kampanyasında paylaşımlı GPU'da yaklaşık iki kat yavaştı. Mümkünse B3 başka eğitimle eşzamanlı koşulmamalıdır.

## 1. B2: üç tohumlu sabit panel (14 model)

Süre: yaklaşık 30 dk, tavan 0,75 sa (`KONSEY_PLANI.md` §4 B2: 14 × (1,15 + 14 × 0,07) dk). Önbellek diske yaklaşık 1,7 GB yazar (14 × 123 MB).

```bash
docker exec -d -w /workspace adeb_eval bash -c "python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
  --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
  --model ResNet18_AT_s1002:resnet18:models/c1/resnet18_s1002/resnet18/adv/adversarial_training/best.pth \
  --model ResNet18_AT_s1003:resnet18:models/c1/resnet18_s1003/resnet18/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2002:vit_tiny:models/c1/vit_tiny_s2002/vit_tiny/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2003:vit_tiny:models/c1/vit_tiny_s2003/vit_tiny/adv/adversarial_training/best.pth \
  --rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
  --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
  --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm \
  --rb-model Debenedetti2022Light_XCiT-S12 \
  --cache-adv results/q1/konsey_adv_onbellek --out-dir results/q1/konsey_b2_panel > logs/konsey_b2.log 2>&1"
```

Bittiğini anlamak: `results/q1/konsey_b2_panel/transfer_matrix.json` oluşur ve `tail -1 logs/konsey_b2.log` satırı `custom kaydedildi: results/q1/konsey_b2_panel` olur. İlerleme: `grep -c onbellege logs/konsey_b2.log` (14'e ulaşır). Yarıda kesilirse aynı komut `--skip-existing` eklenerek yeniden verilir; biten kaynakların örnekleri önbellekten, hücreleri npz'den okunur. `--skip-existing` yalnız `--cache-adv` ile birlikte kabul edilir; önbelleksiz devamda yarıda kalan satır farklı çekişmeli örneklerle tamamlanacağı için betik bu bileşimi reddeder.

## 2. B2 çözümlemesi

```bash
docker exec -w /workspace adeb_eval python experiments/q1_konsey_ayrisim.py --mod b2 \
  --matris-dizini results/q1/konsey_b2_panel \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti results/q1/konsey_ayrisim_b2.json
```

Süre birkaç dakika (CPU, bootstrap 2000). Bittiğini anlamak: `results/q1/konsey_ayrisim_b2.json` oluşur. Panel bileşimi bu adımdan önce, ON_KAYIT §2'de yedi üye olarak dondurulmuştur (29.10 doğrulayıcı düzeltmesi); B2'de yüklenemeyen üye oradaki işlemsel tanımla çıkarılır.

## 3. B3: 2x2 eğitim kuyruğu (tmux)

Süre: pilot değerleriyle beklenen yaklaşık 17,5 sa, tavanda (80 epok) üst sınır 20,47 sa; GPU paylaşılırsa en kötü durumda yaklaşık iki katı (`results/q1/konsey_pilot_zaman.json`, `W_sa` ve `paylasimda_iki_kat_yavaslama_W_sa`; beklenen değer plandaki durma epoklarıyla, ViT 45 ve R224 77, hesaplanmıştır). AT tavanı ön kayıtla 80 epok olarak dondurulmuştur (ON_KAYIT §3, fable kararı K10); GPU paylaşımı yalnız süreyi uzatır, tavan koşu ortasında değiştirilmez.

B3'ten önce iki denetim zorunludur. Birincisi, GPU'da başka bir eğitim koşmamalıdır: `nvidia-smi` çıktısında başka konteynerin (örneğin histo-sparse-adv) eğitim süreci ve yüksek kullanım görülüyorsa B3 o iş bitene kadar başlatılmaz, çünkü pilot boş GPU'da ölçülmüştür. İkincisi, diskte en az 30 GB boş yer olmalıdır; kuyruğun kendi durma eşiği 15 GB'tır, 30 GB ise B3 süresince kontrol noktaları, B4 önbelleği ve günlükler için başlangıç payıdır.

```bash
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv   # kullanim %10'un altinda olmali; nvidia-smi ile surec listesine de bakilir
nvidia-smi
df -BG --output=avail /home/firat | tail -1                         # 30G ya da ustu olmali; altindaysa B3 baslamaz
```

Önce kuru koşu:

```bash
docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --dry-run --pilot results/q1/konsey_pilot_zaman.json
```

Asıl koşu:

```bash
tmux new -s konsey_b3 "cd /home/firat/projects/adeb_sci_1 && docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json 2>&1 | tee -a logs/konsey_b3_kuyruk.log"
```

Kuyruk her aşamadan önce boş diski ve `nvidia-smi` çıktısını `logs/konsey_b3/nvidia_smi_df.log` dosyasına yazar, disk 15 GB'ın altındaysa durur. Kesinti sonrası aynı tmux komutu yeniden verilir: biten aşama atlanır, yarıda kalan aşama `last.pth`'tan devam eder.

Bittiğini anlamak: `tail -1 logs/konsey_b3_kuyruk.log` satırı `KUYRUK TAMAM` ile başlar; `results/q1/konsey_b3_defter.tsv` dosyasında altı koşunun `temiz` ve `AT` satırları `OK` durumundadır; her koşuda `models/q1/konsey/<takma ad>/<tip>/adv/adversarial_training/TRAINING_COMPLETE` vardır. İzleme: `column -t -s $'\t' results/q1/konsey_b3_defter.tsv`.

Kuyruğun durma kodları: 3 temiz aşama denetimi KALDI (ON_KAYIT §4; AT başlamaz), 4 disk, 5 AT çöküş kuralı, 6 eğitim hatası. Temiz aşama denetimi IN koşusunun ilk epok doğrulama doğruluğunu aynı mimarinin rastgele başlatmalı hücresinin ilk epoğuyla karşılaştırır ve AT'si bitmemiş her IN koşusunda, kuyruk her başlatıldığında yeniden yapılır; kod 3 ile duran kuyruk hata giderilmeden yeniden verilirse yine durur. Düzeltme için o koşunun temiz klasörü (`models/q1/konsey/<takma ad>/<tip>/clean`) silinir ve aynı komut verilir. R224-IN denetiminin referansı R224-scr temiz aşamasıdır; R224_IN_s1301'in referansı henüz olmadığından bu koşunun AT'si bekletilir, R224_scr_s1201 temiz aşaması bitince denetim yapılır ve geçerse önce R224_IN_s1301'in, sonra R224_scr_s1201'in AT'si koşar.

AT çöküş kuralı tetiklenirse (kod 5; bir IN koşusunda 5. epok doğrulama PGD doğruluğu %15'in altında) ON_KAYIT §4 gereği iki IN hücresinin bütün AT'leri lr 5e-4 ile koşulur. Bunun için aynı tmux komutu `--in-at-lr 0.0005` eklenerek yeniden verilir:

```bash
tmux new -s konsey_b3 "cd /home/firat/projects/adeb_sci_1 && docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json --in-at-lr 0.0005 2>&1 | tee -a logs/konsey_b3_kuyruk.log"
```

Kuyruk lr'si farklı IN AT klasörlerini silmeden `adversarial_training__lr0.001_<zaman>` adıyla yanına taşır, bu AT'leri lr 5e-4 ile baştan eğitir ve deftere `TASINDI` satırı yazar. Bu noktadan sonra kuyruk her başlatılışta bu bayrakla verilmelidir; bayraksız verilirse yeni lr 5e-4 klasörleri de aynı şekilde taşınır. En kötü durumdaki ek süre yaklaşık 9,0 sa'tir (ON_KAYIT §4).

## 4. B4: son matris (20 model)

Süre: yaklaşık 21 dk, tavan 1,0 sa (`KONSEY_PLANI.md` §4 B4). B2 hücreleri kopyalanır, yalnız yeni hücreler hesaplanır; eski 14 kaynağın örnekleri önbellekten okunur.

```bash
docker exec -w /workspace adeb_eval bash -c "mkdir -p results/q1/konsey_b4_matris && cp -n results/q1/konsey_b2_panel/per_sample_*.npz results/q1/konsey_b2_panel/cells_meta.json results/q1/konsey_b4_matris/"
docker exec -d -w /workspace adeb_eval bash -c "python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
  --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
  --model ResNet18_AT_s1002:resnet18:models/c1/resnet18_s1002/resnet18/adv/adversarial_training/best.pth \
  --model ResNet18_AT_s1003:resnet18:models/c1/resnet18_s1003/resnet18/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2002:vit_tiny:models/c1/vit_tiny_s2002/vit_tiny/adv/adversarial_training/best.pth \
  --model ViT_Tiny_AT_s2003:vit_tiny:models/c1/vit_tiny_s2003/vit_tiny/adv/adversarial_training/best.pth \
  --model V_IN_s2101:vit_tiny_in1k:models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model V_IN_s2102:vit_tiny_in1k:models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1301:resnet18_224_in1k:models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1302:resnet18_224_in1k:models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_scr_s1201:resnet18_224:models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth \
  --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth \
  --rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
  --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
  --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm \
  --rb-model Debenedetti2022Light_XCiT-S12 \
  --cache-adv results/q1/konsey_adv_onbellek --skip-existing --out-dir results/q1/konsey_b4_matris > logs/konsey_b4.log 2>&1"
```

Bittiğini anlamak: `results/q1/konsey_b4_matris/transfer_matrix.json` oluşur, `ls results/q1/konsey_b4_matris/per_sample_*.npz | wc -l` 400 verir ve logun son satırı `custom kaydedildi: results/q1/konsey_b4_matris` olur. Log, B2'den gelen hücreleri `(mevcut hucre)` diye işaretler.

## 5. B5: saldırı tarafı (MI-PGD ve TGR)

Fable kararı K2 ile A önceliğindedir ve defterden bağımsız koşulur. Süre: ikisi birlikte tavan 1,0 sa (17 kaynak-saldırı birimi × yaklaşık 2,2 dk). Kaynaklar 6 C1 ve 6 yeni model, hedefler bunlar ile panel P'dir. MI-PGD föy M8.4 ayarlarıyla (μ = 1,0, α = ε/10), TGR `experiments/c1_c2_tgr.py` ayarlarıyla (α = 2/255) koşar; TGR yalnız ViT kaynaklarını (üç C1 ViT ve iki V-IN) alır, diğerlerini kendisi atlar.

```bash
M12="--model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
 --model ResNet18_AT_s1002:resnet18:models/c1/resnet18_s1002/resnet18/adv/adversarial_training/best.pth \
 --model ResNet18_AT_s1003:resnet18:models/c1/resnet18_s1003/resnet18/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2002:vit_tiny:models/c1/vit_tiny_s2002/vit_tiny/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2003:vit_tiny:models/c1/vit_tiny_s2003/vit_tiny/adv/adversarial_training/best.pth \
 --model V_IN_s2101:vit_tiny_in1k:models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/best.pth \
 --model V_IN_s2102:vit_tiny_in1k:models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training/best.pth \
 --model R224_IN_s1301:resnet18_224_in1k:models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth \
 --model R224_IN_s1302:resnet18_224_in1k:models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training/best.pth \
 --model R224_scr_s1201:resnet18_224:models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth \
 --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth"
P7="--rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
 --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
 --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm"
S12="--sources ResNet18_AT_s1001 ResNet18_AT_s1002 ResNet18_AT_s1003 ViT_Tiny_AT_s2001 ViT_Tiny_AT_s2002 ViT_Tiny_AT_s2003 V_IN_s2101 V_IN_s2102 R224_IN_s1301 R224_IN_s1302 R224_scr_s1201 R224_scr_s1202"
docker exec -d -w /workspace adeb_eval bash -c "python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 $M12 $P7 $S12 --attack mi --out-dir results/q1/konsey_b5_saldiri/mi > logs/konsey_b5_mi.log 2>&1 && python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 $M12 $P7 $S12 --attack tgr --out-dir results/q1/konsey_b5_saldiri/tgr > logs/konsey_b5_tgr.log 2>&1"
```

Bittiğini anlamak: `results/q1/konsey_b5_saldiri/mi/transfer_matrix.json` ve `results/q1/konsey_b5_saldiri/tgr/transfer_matrix.json` oluşur; `logs/konsey_b5_tgr.log` başında atlanan CNN kaynakları listelenir, son satırı `custom kaydedildi: results/q1/konsey_b5_saldiri/tgr` olur. Her kaynağın PGD-10 değeri B4 matrisinden alınır. Ön kayıtlı çözümleme (ON_KAYIT §5 B5): `docker exec -w /workspace adeb_eval python experiments/q1_konsey_ayrisim.py --mod b5 --matris-dizini results/q1/konsey_b4_matris --matris-dizini results/q1/konsey_b5_saldiri/mi --matris-dizini results/q1/konsey_b5_saldiri/tgr --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti results/q1/konsey_ayrisim_b5.json`.

## 6. B6: betimsel AutoAttack (yeni 6 model, n = 1000)

Fable kararı K2 ile A önceliğindedir ve defterden bağımsız koşulur. PGD-10 ile AA doğruluğu arasındaki fark 10 puanı aşan modeller B4 çözümlemesine `--maskeleme-isaretli AD ...` ile verilir (ON_KAYIT §5 B6 karar kuralı). Süre: tavan 1,2 sa (`KONSEY_PLANI.md` §4 B6, model başına yaklaşık 0,15 sa). Mevcut betik `experiments/run_autoattack_run2.py` yeni tipleri `--model` ile olduğu gibi yükler (smoke: `results/q1/konsey_smoke/aa/`).

```bash
docker exec -d -w /workspace adeb_eval bash -c "python experiments/run_autoattack_run2.py --n-samples 1000 --seed 42 \
  --model V_IN_s2101:vit_tiny_in1k:models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model V_IN_s2102:vit_tiny_in1k:models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1301:resnet18_224_in1k:models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1302:resnet18_224_in1k:models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_scr_s1201:resnet18_224:models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth \
  --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth \
  --output-dir results/q1/konsey_b6_aa > logs/konsey_b6_aa.log 2>&1"
```

Bittiğini anlamak: `results/q1/konsey_b6_aa/autoattack_summary.json` oluşur ve logda `Results saved to results/q1/konsey_b6_aa` satırı görünür. Kesintide aynı komut yeniden verilir; biten parçalar (`aa_chunk_*.npz`) atlanır.

PGD-10 ile AA arasındaki fark aynı örneklemde hesaplanır: AA test kümesinin ilk 1000 görüntüsünde koştuğu için PGD-10 doğruluğu da B4 köşegen hücresinin (`per_sample_{m}_to_{m}.npz`) yalnız ilk 1000 görüntüsünden alınır. Köşegenin 10000 görüntülük değeri bu kural için kullanılmaz. B4 bittikten sonra:

```bash
docker exec -w /workspace adeb_eval python scripts/konsey_b6_maskeleme.py \
  --aa-dizini results/q1/konsey_b6_aa --matris-dizini results/q1/konsey_b4_matris --n 1000 \
  --cikti results/q1/konsey_b6_maskeleme.json
```

Betik iki çıktının temiz doğru maskelerini de karşılaştırır (aynı görüntü ve aynı model denetimi; uyuşmazlık %1'i aşarsa hata verir) ve işaretli modeller için B4 çözümlemesine verilecek `--maskeleme-isaretli ...` dizgisini `maskeleme_isaretli_arg` alanına yazar. Süre birkaç saniyedir (CPU).

## 7. B4 çözümlemesi

```bash
docker exec -w /workspace adeb_eval python experiments/q1_konsey_ayrisim.py --mod b4 \
  --matris-dizini results/q1/konsey_b4_matris \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti results/q1/konsey_ayrisim_b4.json
```

B6 maskeleme çıktısında (`results/q1/konsey_b6_maskeleme.json`) `isaretli` listesi boş değilse, komutun sonuna `maskeleme_isaretli_arg` alanındaki dizgi eklenir (ON_KAYIT §5 B6; birincil çözümleme yine bütün modellerle yapılır, kural aynı çıktıda ayrıca uygulanır).

Bittiğini anlamak: `results/q1/konsey_ayrisim_b4.json` oluşur.

## 8. Her bloktan sonra

Konteynerin yazdığı dosyalar root sahiplidir; firat'a geri verilir:

```bash
docker exec adeb_eval chown -R 1000:1000 /workspace/results/q1 /workspace/models/q1 /workspace/logs
```
