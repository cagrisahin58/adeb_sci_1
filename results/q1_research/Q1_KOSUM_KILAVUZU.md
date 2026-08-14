# Q1 Koşum Kılavuzu (eğitim başlatma komutları)

Altyapı hazır; aşağıdaki aşamalar **rapor sırasına göre** (E2 → E1 → E5-pilot
→ E5 → E7) tek tek başlatılır. Her aşama idempotent: kesinti sonrası aynı
komut kaldığı yerden devam eder (guard = `TRAINING_COMPLETE`, `--resume`
otomatik). Başlatmadan önce `nvidia-smi` ile GPU'nun boş olduğunu kontrol et
(histo-sparse-adv konteyneri paylaşıyor olabilir).

## Aşama komutları (konteyner içinde, arka planda)

```bash
# 1) E2 - sızıntı ablasyonu (~19-28 GPU-saat; her epoch checkpoint'li, disk ~25GB)
#    (bütçe güncellendi: patience 0 → 6 AT koşusunun hepsi tam 100 epok; ayrıca
#    18 çevrimdışı seçim geçişi ~2-3 saat + 18 test değerlendirmesi ~1 saat)
docker exec -d -w /workspace -e STAGE=e2 adeb_eval bash scripts/q1_pipeline.sh

# 2) E1 - CIFAR-100 ana çift (~24 GPU-saat)
docker exec -d -w /workspace -e STAGE=e1 adeb_eval bash scripts/q1_pipeline.sh

# 3) E5 PILOT - R50 + ViT-S birer tohum (SÜRE ÖLÇÜMÜ; rapor: ±%40 belirsizlik)
docker exec -d -w /workspace -e STAGE=e5pilot adeb_eval bash scripts/q1_pipeline.sh
#    Pilot bitince: logs/Q1_cifar10_at_vit_small_4001.log içinde ilk 5 epok
#    adv-acc < %15 ise LR 2.5e-4'e düşürülecek (rapor 5.3 sigortası).

# 4) E5 - kalan tohumlar + AutoAttack (~50-60 GPU-saat)
docker exec -d -w /workspace -e STAGE=e5 adeb_eval bash scripts/q1_pipeline.sh

# 5) E7 - SVHN çapası (İLK DÜŞECEK KALEM; ~30 GPU-saat)
docker exec -d -w /workspace -e STAGE=e7 adeb_eval bash scripts/q1_pipeline.sh
```

İzleme: `tail -f logs/q1_<stage>.log` (START/DONE/FAIL/SKIP satırları).

## Eğitim sonrası analiz komutları (GPU hafif)

```bash
# E3 kalibrasyon: önce kaynak saldırıları arşivle (C1 final modellerinden)
python scripts/q1_archive_adv.py --model-type vit_tiny \
    --ckpt models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
    --dataset cifar10 --out results/q1/adv_archive/vit_s2001_pgd10.npz
python scripts/q1_archive_adv.py --model-type resnet18 \
    --ckpt models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
    --dataset cifar10 --out results/q1/adv_archive/rn18_s1001_pgd10.npz

# Sonra her E2/E1 yorungesi icin nokta uret (ornek):
python scripts/q1_e3_calibration.py points \
    --epochs-dir models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs \
    --model-type resnet18 --dataset cifar10 \
    --adv-archive results/q1/adv_archive/vit_s2001_pgd10.npz \
    --trajectory-id e2_rn18s1001_srcvit --out-dir results/q1/e3_points

# Tum noktalar toplaninca kume-bootstrap regresyonu:
python scripts/q1_e3_calibration.py fit \
    --points-dir results/q1/e3_points --out results/q1/e3_fit.json

# CIFAR-100 3x3 matrisi (E1 bittikten sonra; Pang2022 referansi otomatik):
python experiments/c1_c3_transfer_matrix.py --dataset cifar100 \
    --model "ResNet18_AT:resnet18:models/q1/cifar100/resnet18_s1001/resnet18/adv/adversarial_training/best.pth" \
    --model "ViT_Tiny_AT:vit_tiny:models/q1/cifar100/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth" \
    --out-dir results/q1/cifar100/c3_matrix_pair1

# Transfer protokolleri (a2 istatistik cekirdegi, env ile):
A2_IN_DIR=results/q1/cifar100/pair1 A2_OUT=results/q1/cifar100/pair1/a2.json \
    python experiments/rev2/a2_transfer_protocols.py

# L2 (E6; yalniz CIFAR-10 final modelleri):
python experiments/run_autoattack_run2.py --dataset cifar10 --norm L2 --eps 0.5 \
    --model "ResNet18_AT:resnet18:models/c1/resnet18_s1001/.../best.pth" \
    --model "ViT_Tiny_AT:vit_tiny:models/c1/vit_tiny_s2001/.../best.pth" \
    --output-dir results/q1/l2/pair1
```

## E4 (+2 tohum, manşet 5'e tamamlama)
E1-E3 sonuçları geldikten sonra karar verilecek (rapor: "'20 kat' oranı
manşette kalacaksa tutulur"). Komut: C1 pipeline'ının 1004/1005 + 2004/2005
tohumlarıyla `train_pair_member cifar10 ...` çağrıları — istenirse eklerim.

## Disk/GPU notları
- **Toplam disk (review düzeltmesi; rapordaki ~30-40GB eksikti):** E2 her-epoch
  ~25GB + E1 (save_every=2) ~7GB + E5 (save_every=2; R50 94MB + ViT-S 87MB
  × ~30 ckpt × 3 tohum) ~16GB + E7 ~7GB ≈ **~55GB tepe**. Kampanya öncesi
  `df -h` ile ≥80GB boş alan doğrula; E3 kantil seçimi bittikçe seçilmeyen
  `epochs/` checkpointleri silinebilir.
- AutoAttack koşuları gece kuyruğuna; chunk-resume var, kesinti güvenli
  (cache anahtarı artık norm/eps/seed içeriyor — L2 koşusu Linf parçalarını
  yeniden kullanamaz).
- ViT-S bs=64 fp32 tepe ~12-16GB → 32GB'a rahat sığar; bs artırılMAZ.
- E2 notu (review bulgusu): AT başlangıcı clean `last.pth`'tan alınır (sabit
  200-epok bütçe) — `best.pth` seçimi V_B'ye dokunurdu, V_B'nin "hiç
  kullanılmamış" statüsü korunur.

## Başlatma-öncesi denetim güncellemeleri (2026-08-14, 3 Opus ajanı)

- **E2'ye V_C negatif kontrolü eklendi:** V_A/V_B/V_C 2000'er, D_core=44k.
  V_B-vs-V_C = saf seçim-gürültüsü tabanı; V_A-vs-V_B bu tabana karşı okunur.
  Analiz kuralları EĞİTİMDEN ÖNCE sabitlendi: `E2_ISTATISTIK_PROTOKOLU.md`
  (McNemar eş-birincil, TOST δ=1.0, dejenere durumlar, ortak-bölme sınırlaması).
- **E2 seçimleri artık test değerlendirmesi içerir:** `q1_offline_select.py
  --test-eval` seçilen checkpoint'i tam 10k testte ölçer, örnek maskelerini
  `select_*_test.npz`'ye yazar. Toplama betiği `scripts/q1_e2_report.py`
  (eğitim koşarken yazılacak) TOST+McNemar'ı bunlardan üretir.
- **E2 `adv/*/best.pth` dosyalarını KULLANMA** — canlı seçim V_A∪V_B∪V_C
  (6000) üzerindedir, üçüncü kuraldır (`models/q1/e2/BEST_PTH_KULLANMA.txt`).
- **Pipeline sertleştirmeleri:** başta sert CUDA kontrolü (auto-device'ın
  sessiz CPU düşüşü C1'de yaşanmıştı) + tüm eğitim komutlarında `--device
  cuda`; her eğitim/adım 3 denemeli (aralarda 300 sn, `--resume` ile);
  `PYTHONUNBUFFERED=1` (loglar gecikmesiz).
- **Sıfırdan yeniden başlatma kuralı:** bir AT koşusunu hiperparametre
  değişikliğiyle bilerek sıfırlarken `TRAINING_COMPLETE` + `last.pth` +
  `epochs/` ÜÇÜNÜ birden sil — yalnız marker silinirse eski `epoch_*.pth`
  dosyaları yeni yörüngeyle sessizce karışır.
- **Bölme dosyaları:** `data/e2_*.json` üretimden hemen sonra `git add -f`
  ile depoya alınır (data/ gitignore'da; torch.randperm sürüme bağlı —
  dosyalar kanonik kaynak).
