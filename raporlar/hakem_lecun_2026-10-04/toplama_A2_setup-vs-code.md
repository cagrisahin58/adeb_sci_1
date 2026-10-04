# A2: Deney kurulumu dosyesi ve koda karsi dogrulama (mercek A, bilim ve tasarim)

Tarih 2026-10-04. Toplayici A2. Yalniz olgu toplanmistir; yargi, not, oneri yoktur. Kaynak metin `paper/manuscript/sections/03_methodology.tex` (kisaltma M:satir). Kod yollari depo kokune goreli (`/home/firat/projects/adeb_sci_1`). Karantina kuralina uyuldu: hicbir sayi run1/run2/run3/rev2_blockA yollarindan kanit olarak alinmadi; `results/rev2_blockA` yalniz bir yerde, kod davranisini gostermek icin ve "KARANTINA" etiketiyle anildi.

## 10 satirlik ozet

1. Bolum 3'teki kurulum parametreleri koda karsi tarandi; 137 olgu, ilgili tablolarda MATCH / MISMATCH / NOT FOUND / KODDA VAR, METINDE YOK etiketiyle kayda gecti.
2. Egitim tarifinin buyuk kismi (SGD/AdamW, lr, 200/100 epoch, cosine, batch 128/64, kirpma 10, NaN atlama, patience 20, min_delta 0.1 puan, 2000'lik val bolmesi, tohumlar, lambda 0.5, [0,1] girdi) kodda ve C1 egitim gunluklerinde ayni bulundu (T2-T4).
3. BN egitim kipi: egitim PGD'si model.train() altinda uretiliyor, eval kipine gecilmiyor (`src/defenses/adversarial_training.py:103-112`, `src/training/adversarial_trainer.py:222`); kod yorumu bu duzeltmenin 2026-07-11'de (0f8a24f) yapildigini, C1 egitiminin 2026-07-29/30'da kosuldugunu gosteriyor. Degerlendirme saldirilari eval kipinde (`src/attacks/base.py:38`).
4. MISMATCH: ViT-Tiny parametre sayisi metinde 5.7M (M:50, 04_experiments.tex:31-32,441, 05_discussion.tex:61); kodda ve C1 gunluklerinde 5,526,346 (`logs/C1_clean_vit_2001.log:3`). 5.7M, 1000 sinifli basin sayisina denk geliyor. ResNet-18 11,173,962, WRN 36,479,194, native ViT 5,362,762 metinle uyumlu.
5. MISMATCH (kapsam): gradyan "alignment" metinde 500 ornegin tum cift kosinusu (M:121, 04_experiments.tex:279) olarak tanimli; tabloya giren sayilar (0.0378, 0.0562, 0.079) `gradient_summary.json` icindeki 50'lik parti ici tahminciden geliyor; tum-cift tahmincisi (`results/c1_a3/pair*`) 0.0381 ve 0.0566 veriyor. Isaretli alignment sutunu yalniz 1. cift degerleri.
6. Dort protokol maskesi `src/analysis/protokoller.py:57-66` icinde tek yerde; kanonik "successful_source" siki (tc & sc & sa), gevsek varyant (tc & sa) yalniz tanida. Metindeki ilk tanim cumlesi (M:118) kaynagin temiz dogrulugunu anmiyor, ikinci cumle (Ravikumar) anıyor; kod ikisini birden uyguluyor. Siki 19.37, gevsek 14.60 (3 cift ortalamasi, `a2_transfer_protocols.json`).
7. TGR uyarlamasi (`experiments/c1_c2_tgr.py`): gamma 0.5 tek, her yolda; qkv ve mlp yolunda (ornek, kanal) basina tek max ve tek min jeton girdisi sifirlaniyor; dikkat yolunda ise (ornek, kafa) basina NxN izgarada tek max ve tek min hucre sifirlaniyor. Yayimlanan yontemin kaynak kodu depoda yok; yazarin kendi notu (`scripts/_t4_tgr.py:11-13`) yol-basina katsayilari birinci elden dogrulamadigini soyluyor.
8. ViT yerel cozunurluk kontrolu tek kontrol noktasi (2026-01-10), sabit val bolmesi oncesi egitim, test uzerinde secim, gunluk 100 epoch'un 60'inda kesilmis (mid-epoch), drop_rate 0.1 (timm ViT'te 0), egitim PGD'si o tarihte eval kipinde uretilen surumle.
9. Kontrol noktasi secim kurali: egitim sirasinda val PGD-10 dogrulugunun, 0.1 puani asan ilk iyilesmelerle guncellenen "best.pth" (patience 20); temiz asama best.pth'si temiz val dogrulugunun siki maksimumu. ViT secili epoch 18-25 (cosine'de lr hala 0.85-0.92e-3), ResNet 51-57.
10. Bulunamayan: TOST marji +-2'nin "PGD dogrulugunun kosular arasi degiskenliginden" turetildigini gosteren dosya/kod (yalniz `experiments/run_stat_addendum.py:58` DELTA=0.02 sabiti ve `a2_transfer_protocols.py:129` icinde 1/2/3 puan izgarasi var); AutoAttack'in alt-saldiri iterasyon/yeniden-baslatma sayilari depoda degil kutuphanede (`autoattack 0.1`, container).

Etiketler: MATCH metin = kod; MISMATCH fark var; NOT FOUND karsiligi bulunamadi; KODDA VAR, METINDE YOK metin anmiyor (olgu kaydi).

---

## T1. Mimariler ve parametre sayilari

| ID | Metin (M:satir) | Kod / olcum (dosya:satir) | Durum |
|---|---|---|---|
| F001 | ResNet-18, 3x3 ilk konv, 7x7 degil (M:44) | `src/models/resnet.py:38-40` conv1 Conv2d(3,64,k=3,s=1,p=1); `:41` maxpool=Identity (metinde maxpool'dan soz yok) | MATCH |
| F002 | ResNet-18 11.2M (M:44) | konteynerde `ModelRegistry.get("resnet18", num_classes=10)` = 11,173,962; `logs/C1_at_resnet_1001.log:8` ayni | MATCH |
| F003 | WRN-28-10 36.5M, Gowal et al. RobustBench (M:46) | `experiments/c1_c3_transfer_matrix.py:56` ad `Gowal2020Uncovering_28_10_extra`; olcum 36,479,194 | MATCH |
| F004 | WRN "pretrained robust checkpoint", ek etiketsiz veri (M:46) | `c1_c3_transfer_matrix.py:62-63` robustbench `load_model(..., threat_model="Linf", model_dir="models/robustbench_zoo")`; ad "extra" icerir | MATCH |
| F005 | "tum modeller ham piksel [0,1], ortalama/std normalizasyonu yok" (M:97) | egitilen modeller: `src/data/datasets.py:128-135` yalniz ToTensor. WRN: RobustBench `cifar10.py:527-534` `Gowal2020Uncovering_28_10_extra` kaydinda `mean=CIFAR10_MEAN, std=CIFAR10_STD` model icinde uygulaniyor (girdi [0,1]) | MISMATCH (WRN icin: girdi [0,1] ama normalizasyon model icinde) |
| F006 | ViT-Tiny timm, 224'e bilinear buyutme (M:50) | `src/models/vit.py:385-389` `timm.create_model("vit_tiny_patch16_224", pretrained=pretrained, num_classes=num_classes)`; `:392` `nn.Upsample(size=(224,224), mode="bilinear", align_corners=False)`; `:396` forward'da uygulanir | MATCH |
| F007 | 16x16 yama, 196 yama, 192 gomme, 12 blok, 3 kafa, MLP orani 4 (M:50) | konteynerde olcum: patch (16,16), num_patches 196, embed 192, blok 12, kafa 3, mlp gizli 768 (=4x192) | MATCH |
| F008 | ViT-Tiny toplam 5.7M (M:50) | olcum 5,526,346; `logs/C1_clean_vit_2001.log:3` ve `logs/C1_at_vit_2001.log:9` ayni; `src/models/vit.py:207` docstring "~5.7M for timm vit_tiny" | MISMATCH |
| F009 | ViT sifirdan, ImageNet on-egitimi yok (M:50) | `scripts/run_c1_pipeline.sh:58` `train clean -m vit_tiny` (`--timm-pretrained` yok); `cli/train.py:33-35` bayrak varsayilan False; `logs/C1_clean_vit_2001.log:1-7` ImageNet agirligi mesaji yok | MATCH |
| F010 | (metinde yok) timm ViT-Tiny dropout/drop_path | konteynerde: tum Dropout p=0.0, drop_path Identity, global_pool "token" | KODDA VAR, METINDE YOK |
| F011 | WRN kendi egitimimiz degil, referans (M:46) | `c1_c3_transfer_matrix.py:64` `model.to(device).eval()`; egitim kodu yok | MATCH |

## T2. Egitim tarifi (temiz asama)

| ID | Metin | Kod / gunluk | Durum |
|---|---|---|---|
| F012 | CNN: SGD, ilk lr 0.1 (M:94) | `scripts/run_c1_pipeline.sh:46` `-m resnet18 -e 200 --lr 0.1 -b 128`; `src/training/trainer.py:100-105` SGD | MATCH |
| F013 | CNN agirlik azaltimi 5e-4 (M:94) | `src/training/trainer.py:34` weight_decay=5e-4 (SGD'ye `:104`) | MATCH |
| F014 | (metinde yok) SGD momentum | `src/training/trainer.py:33` momentum=0.9; `:103` | KODDA VAR, METINDE YOK |
| F015 | cosine annealing (M:94) | `src/training/trainer.py:108-111` CosineAnnealingLR(T_max=epochs); isitma yok | MATCH |
| F016 | 200 epoch (M:94) | `scripts/run_c1_pipeline.sh:46,58` `-e 200`; `logs/C1_clean_resnet_1001.log:2`, `logs/C1_clean_vit_2001.log:2` "Epochs: 200" | MATCH |
| F017 | ViT: AdamW, lr 1e-3, wd 0.05, cosine, 200 epoch (M:94) | `run_c1_pipeline.sh:58` `--lr 0.001`; `trainer.py:88-95` AdamW lr=min(lr,1e-3), weight_decay=0.05; `logs/C1_clean_vit_2001.log:5` "AdamW (lr=0.001)" | MATCH |
| F018 | (metinde yok) temiz asama batch'i | ResNet 128 (`run_c1_pipeline.sh:46`), ViT 128 (`:58`, `logs/C1_clean_vit_2001.log:2` "Batch size: 128") | KODDA VAR, METINDE YOK |
| F019 | augmentation: 4 piksel dolgulu rastgele kirpma + yatay cevirme (M:97, M:50) | `src/data/datasets.py:128-132` (C1 donemi `get_cifar10_loaders_with_val`) ve HEAD `:294-300`; yalniz egitim kumesinde, val/test yalniz ToTensor `:133-135` | MATCH |
| F020 | Temiz asamada secim: metin PGD-10 adv. dogrulugundan soz ediyor (M:100: "Model selection and early stopping use PGD-10 adversarial accuracy on a fixed 2,000-sample validation split") | temiz asama best.pth: `src/training/trainer.py:241-252` `test_acc > best_acc` (siki, min_delta yok); `cli/train.py:70` `test_loader = val_loader`, yani 2000'lik val uzerinde TEMIZ dogruluk; PGD kullanilmaz; patience yok | MISMATCH (kapsam: metin AT asamasini tarif ediyor, temiz asamanin secim olcutu anilmiyor) |
| F021 | temiz asama val bolmesini egitimden cikarir (M:100) | `logs/C1_clean_resnet_1001.log:4` "Fixed val split (data/val_split_indices.json): egitim 48000 ornek; secim 2000 val ornegi uzerinden (test kullanilmiyor)"; `cli/train.py:61-72` | MATCH |
| F022 | Temiz asama secili epoch (C1 gunlukleri, son "Best model saved") | ResNet 1001/1002/1003: epoch 197/184/182 (val temiz 95.75/95.95/96.55); ViT 2001/2002/2003: 188/185/191 (val temiz 81.90/83.85/83.25) (`logs/C1_clean_*.log`, son "Best model saved" satirindan onceki "Epoch k/200") | olgu kaydi |

## T3. Egitim tarifi (adversarial asama) ve BN kipi

| ID | Metin | Kod / gunluk | Durum |
|---|---|---|---|
| F023 | Temiz kontrol noktasindan ince ayar (M:96-97) | `run_c1_pipeline.sh:51,63` `-p models/c1/.../clean/best.pth`; `cli/train.py:169-171` agirliklar yuklenir; `logs/C1_at_resnet_1001.log:3` | MATCH |
| F024 | AT lr 1e-3, cosine, en cok 100 epoch (M:97) | `run_c1_pipeline.sh:52,64` `-e 100 --lr 0.001`; `adversarial_trainer.py:188-190` CosineAnnealingLR(T_max=epochs=100); `logs/C1_at_*.log:2` "Epochs: 100, LR: 0.001" | MATCH |
| F025 | CNN: SGD; ViT: AdamW ayni lr ve takvim (M:97) | `adversarial_trainer.py:156-171`: ViT AdamW lr=min(lr,vit_lr_cap=1e-3) wd 0.05; CNN SGD momentum 0.9 wd 5e-4 (`:41-42`); `logs/C1_at_vit_2001.log:5` "AdamW (lr=0.001)" | MATCH |
| F026 | Gradyan L2 normu 10'a kirpilir (M:97) | `adversarial_trainer.py:251` `clip_grad_norm_(..., max_norm=self.grad_clip)`; `:54` varsayilan 10.0; `cli/train.py:135-136` varsayilan 10.0; C1 donemi `git show c7eb7cb:src/training/adversarial_trainer.py` satir 215 `max_norm=10.0` | MATCH |
| F027 | Sonlu olmayan kayipli batch atlanir (M:97) | `adversarial_trainer.py:244-246` `isnan/isinf -> continue`, backward'dan once | MATCH |
| F028 | Batch: CNN 128, ViT 64 (M:97) | `run_c1_pipeline.sh:52` `-b 128` (ResNet AT); `:64` `-b 64` (ViT AT); `logs/C1_at_vit_2001.log:10` 750 batch/epoch (48000/64) | MATCH (AT asamasi icin) |
| F029 | Erken durdurma patience 20, 0.1 puan esigi (M:97) | `adversarial_trainer.py:52` min_delta=0.1; `:479` `adv_acc > best + min_delta`; `:493-500` patience sayaci; `run_c1_pipeline.sh:52,64` `--patience 20`; `logs/C1_at_*.log:6` "Early stopping enabled (patience=20)" | MATCH |
| F030 | Karisik kayip (1-lambda) CE(clean) + lambda CE(adv), lambda=0.5 (M:83-84) | `src/defenses/adversarial_training.py:31` mix_ratio=0.5; `:122` `loss = (1 - self.mix_ratio) * loss_clean + self.mix_ratio * loss_adv`; `adversarial_trainer.py:119-125` mix_ratio gecirilmez, varsayilan kalir; C1 donemi dosyada `:122` ayni | MATCH |
| F031 | Ic maksimizasyon PGD-10, alpha 2/255, eps 8/255 (M:85) | `adversarial_trainer.py:43-45` eps 8/255, alpha 2/255, steps 10; `cli/train.py:113-115` varsayilan ayni; `run_c1_pipeline.sh` bu bayraklari gecmez; `logs/C1_at_*.log:2` "eps: 0.0314" | MATCH |
| F032 | Ic PGD rastgele baslangic U(-eps,eps) (M:69) | `adversarial_training.py:65-67` uniform(-eps,eps) sonra clamp[0,1]; adimlar `:69-82`; izdusum `:81-82` | MATCH |
| F033 | Ic PGD'de model egitim kipinde (BN istatistikleri tutarli) (M:85) | `adversarial_training.py:103-112` yorum + `get_loss` icinde model.eval() cagrilmaz; `adversarial_trainer.py:222` `self.model.train()` epoch basinda; `git blame` `0f8a24f` 2026-07-11; C1 egitim gunlukleri 2026-07-29/30 (dosya mtime) | MATCH |
| F034 | (metinde yok) egitim sirasinda BN calisan istatistikleri | train kipinde her ileri gecis (10 saldiri adimi + temiz + adv = 12 gecis/iter) BN running_mean/var'i gunceller; `adversarial_training.py:72,115,118` | KODDA VAR, METINDE YOK |
| F035 | (metinde yok) temiz ve adv. batch'ler ayri ileri gecis | `adversarial_training.py:115` `model(images)`, `:118` `model(adv_images)` ayri cagrilar (BN batch istatistigi ayri) | KODDA VAR, METINDE YOK |
| F036 | Degerlendirme saldirilari kipi | `src/attacks/base.py:38` `self.model.eval()`; `scripts/c1_pgd_eval.py:49` `load_model_auto` eval dondurur (`src/utils/load_model_auto.py:65`); epoch ici val-PGD: `adversarial_training.py:132` `generate_adversarial` `self.model.eval()` | KODDA VAR, METINDE YOK (egitim PGD'si train, degerlendirme PGD'si eval) |
| F037 | (metinde yok) cosine takvimi T_max=100, patience'la erken durma takvimi kisaltmaz | `adversarial_trainer.py:188-190`; ViT 2001 son epoch 45, lr secili epoch'ta 0.000854 (`models/c1/vit_tiny_s2001/.../last.pth` history lr[24]) | KODDA VAR, METINDE YOK |
| F038 | Ince ayar saldirisi lr uyarlama/eps isitma | `adversarial_trainer.py:441-445` eps-isitma yalniz `--eps-warmup>0`; C1 boru hatti bayragi gecmez (`run_c1_pipeline.sh:49-66`) | KODDA VAR, METINDE YOK (kullanilmadi) |

## T4. Dogrulama bolmesi, tohumlar, kontrol noktasi secimi

| ID | Metin | Kod / veri | Durum |
|---|---|---|---|
| F039 | Sabit 2000'lik val bolmesi, tohum 777, indeksler kodla saklanir (M:100) | `experiments/rev2/make_val_split.py:77` `--split-seed default=777`, `:76` `--val-size default=2000`; `:108-109` `randperm(n_train)`, ilk 2000 sirali; `data/val_split_indices.json` anahtarlar `split_seed=777, val_size=2000, n_train_total=50000, len(val_indices)=2000`; `git ls-files data/val_split_indices.json` izli | MATCH |
| F040 | Bolme tum modellerce paylasilir ve hem temiz hem AT egitiminden cikarilir (M:100) | `cli/train.py:61-72` (temiz), `:176-184` (AT) `--val-indices`; `src/data/datasets.py:148-158,350-364` (indeksler egitimden cikarilir); `logs/C1_at_resnet_1001.log:4` | MATCH |
| F041 | Test seti yalniz son post-hoc degerlendirmede (M:100) | `adversarial_trainer.py:456` `eval_loader = self.val_loader if ... else self.test_loader`; `cli/train.py:70` temiz asamada test yerine val; C1 gunlukleri "(test kullanilmiyor)" | MATCH |
| F042 | Tohumlar ResNet 1001-1003, ViT 2001-2003 (M:100) | `scripts/run_c1_pipeline.sh:4,42` `RSEED=$((1000+i)); VSEED=$((2000+i))`, i=1..3; `cli/train.py:157` `set_seed(seed)`; `src/utils/seed.py:12-21` random/numpy/torch/cuda + cudnn.deterministic | MATCH |
| F043 | Tohum esleme indeksle (M:100) | `scripts/c1_transfer_rerun.py:21-25` `PAIRS = {1:(1001,2001), 2:(1002,2002), 3:(1003,2003)}`; ayni sozluk `c1_c2_tgr.py:39`, `c1_c3_transfer_matrix.py:32` | MATCH |
| F044 | Tam hat uc kez (temiz + AT) (M:100) | `run_c1_pipeline.sh:41-66` her i icin 2 temiz + 2 AT | MATCH |
| F045 | Tablolar ort ve std (3 kosu) (M:100) | `scripts/build_reference_sheet.py` ve `scripts/c1_transfer_aggregate.py:50-52` `std(ddof=1)` | MATCH |
| F046 | Kontrol noktasi secim kurali (hangi dosya raporlanan kosulari uretti) | tum C1 analizleri `models/c1/<arch>_s<seed>/<arch>/adv/adversarial_training/best.pth` okur (`c1_transfer_rerun.py:31-32`, `c1_c2_tgr.py:200-201`, `c1_c3_transfer_matrix.py:123-124`, `c1_c4_attention_features.py:124-125`, `c1_c5_spatial_locality.py:122-123`, `run_c1_pipeline.sh:71-82`); best.pth = val PGD-10 dogrulugunun `> best+0.1` ile guncellenen son hali (`adversarial_trainer.py:479-490`) | olgu kaydi |
| F047 | AT secili epoch'lar ve duruslar (C1 gunlukleri + best.pth ust verisi) | ResNet 1001/1002/1003: secili epoch 51/56/57 (0-indeks 50/55/56), val adv 45.85/46.65/46.40, val temiz 85.70/86.40/86.85, durus epoch 71/76/77, lr secili epoch'ta 4.84e-4/4.06e-4/3.91e-4. ViT 2001/2002/2003: secili 25/18/19 (0-indeks 24/17/18), val adv 34.05/34.35/34.90, val temiz 74.35/73.50/72.50, durus 45/38/39, lr 8.54e-4/9.22e-4/9.14e-4 (`last.pth` history; `logs/C1_at_*.log`) | olgu kaydi |
| F048 | (metinde yok) val-PGD her epoch'ta tek rastgele baslangicla, tohumsuz tekrar | `adversarial_trainer.py:289-339` `evaluate_adversarial` -> `generate_adversarial` `random_start=True`; epoch basina tohum sifirlanmaz | KODDA VAR, METINDE YOK |
| F049 | ViT 2001 AT calismasi cihaz | `logs/C1_at_vit_2001.log:7` "Adversarial training on cpu", epoch 1-5 CPU'da (`:11-23`, ilk batch 58.96 s/it); `:26-33` yeniden baslatma "Resuming from epoch 5 (best adv acc so far: 29.70%, patience: 0/20)" ve "on cuda"; diger 5 AT gunlugunde "Resuming" yok (`grep -c`) | olgu kaydi (metinde yok) |
| F050 | Secim gurultusu: 18 kombinasyon = bolme x patience x yumusatma (M:156) | `scripts/q1_b8_secim_bandi.py:10-12` "BOLME (V_B/V_C) x patience x yumusatma = 18 hucre"; `:39-40` PATIENCES [0,10,20], KERNELS [1,3,5], `:21` 9 hucre; `scripts/q1_offline_select.py:5-7` kural: best-by-adv-val + patience-20 + min_delta 0.1 | MATCH |
| F051 | Onceki kontrol noktasi cifti: val bolmesi temiz on-egitimde gorulmus (M:102) | `models/resnet18/adv/at_run3`, `models/vit_tiny/adv/at_run3` yollari `experiments/rev2/a3_gradient_paired.py:35-36` (karantina yolu); metin yalniz karsit olarak anar | NOT FOUND (karantina sayisi kanit alinmadi) |

## T5. Saldirilar ve butceler

| ID | Metin | Kod / sonuc dosyasi | Durum |
|---|---|---|---|
| F052 | L-inf, eps=8/255 birincil (M:32) | `scripts/c1_pgd_eval.py:32` `--eps default=8/255`; `experiments/c1_c3_transfer_matrix.py:25` EPS=8/255 | MATCH |
| F053 | eps taramasi {2,4,16}/255, tam test PGD-10 (M:32) | `scripts/c1_analyses_pipeline.sh:25-27` EPS2=0.00784313725490196, EPS4=0.01568627450980392, EPS16=0.06274509803921569; `:48-54` `cli evaluate robustness -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 --seed 42`; `cli/evaluate.py:93-97` tam test_loader | MATCH |
| F054 | PGD alpha=2/255 (M:65) tum eps'te | `src/attacks/pgd.py:25-27` varsayilan alpha=2/255, steps=10; `AttackRegistry.get(...)` alpha gecmez (`src/evaluation/evaluator.py:65-71`), yani eps=2/255 ve 16/255'te de alpha 2/255 (eps=2/255'te adim = butce; eps=16/255'te 10 adimin toplam yolu 20/255) | MATCH (alpha eps ile olceklenmez) |
| F055 | FGSM adimi = eps (M:59) | `src/attacks/fgsm.py:86` `images + self.eps * grad_sign`; rastgele baslangic yok | MATCH |
| F056 | PGD rastgele baslangic x0 = x + U(-eps,eps) (M:69) | `src/attacks/pgd.py:71-74` uniform(-eps,eps) sonra [0,1] kirpma | MATCH |
| F057 | PGD-10 hem egitimde hem degerlendirmede (M:69) | egitim `adversarial_training.py:69` `range(self.steps)`, steps=10; degerlendirme `c1_pgd_eval.py:34` `--steps default=10` | MATCH |
| F058 | PGD iz: CE, L-inf izdusum, [0,1] (M:67) | `pgd.py:90,104-105` CE ve `_project` (`src/attacks/base.py:118-125` L-inf kirpma + [0,1]) | MATCH |
| F059 | PGD degerlendirme tam test, ornek bazli kayit (M:7) | `scripts/c1_pgd_eval.py:53-54,73-74` `pgd_per_sample_*.npz` (clean_correct, robust_correct); `results/c1_seeds/pair*/pgd_per_sample_*.npz` n=10000 | MATCH |
| F060 | PGD ve AA'da temiz hatali ornekler dayaniksiz sayilir; robust = clean x kosullu hayatta kalma (M:111) | `c1_pgd_eval.py:63-64` robust_ok = adv_pred==labels (clean ile VE'lenmez, kodda zorlama yok); olcum: `results/c1_seeds/pair{1,2,3}/pgd_per_sample_*.npz` ve `per_sample_*.npz` (AA) 12 dosyada `robust & ~clean` = 0 | MATCH (veri duzeyinde; kod zorlamaz) |
| F061 | Girdi alani/eps piksel uzayinda (M:97) | ViT icin yukseltme model icinde (`vit.py:396`), gradyan 32x32 piksel uzayinda; saldirilar [0,1] ister (`base.py:85-90`) | MATCH |
| F062 | Saldiri tohumlari 42/123/456, sabit alt kume (M:156) | `experiments/run_all_analyses_run2.py:647-648` seeds [42,123,456], n_samples=1000; `:635-639` docstring "yalnizca saldiri baslatma rastgeleligi... ayni ilk 1000 ornek"; `scripts/c1_statval_rerun.py:17-18` yalniz cift 1 (`paths(1)`) | MATCH |
| F063 | Tum betikler tohum 42 + CUDA determinizm bayraklari (M:158) | `c1_pgd_eval.py:36,40-44` seed 42, cudnn.deterministic=True, benchmark=False; `c1_c3_transfer_matrix.py:35-43`; `c1_c2_tgr.py:42-50`; `cli/evaluate.py:67-77` `--seed` | MATCH |

## T6. AutoAttack

| ID | Metin | Kod | Durum |
|---|---|---|---|
| F064 | AutoAttack standart: APGD-CE, APGD-T, FAB-T, Square (M:72) | `experiments/run_autoattack_run2.py:122` `AutoAttack(model, norm=aa_norm, eps=eps, version='standard', seed=seed + k, verbose=True)`; kutuphane `autoattack 0.1` (container `pip list`) | MATCH |
| F065 | AA n=10000 (tam test) | `scripts/run_c1_pipeline.sh:79-80` `--n-samples 10000 --seed 42`; `run_autoattack_run2.py:162` varsayilan 10000; `results/c1_seeds/pair*/autoattack_summary.json` `n_samples: 10000, seed: 42, eps: 0.03137254901960784` | MATCH |
| F066 | (metinde yok) AA parti 100, 1000'lik parcalar, parca tohumu seed+k | `run_autoattack_run2.py:165-166` batch 100, chunk 1000; `:123` `seed + k`; `:124` `run_standard_evaluation(xb, yb, bs=batch_size)` | KODDA VAR, METINDE YOK |
| F067 | (metinde yok) AA alt-saldiri iterasyonlari, yeniden baslatma, hedef sinif sayisi, Square sorgu sayisi | depoda tanimli degil (kutuphane varsayilanlari); depo kodu bunlari gecmez (`run_autoattack_run2.py:122-124`) | NOT FOUND (depo icinde) |
| F068 | AA modeli eval kipinde (varsayilan) | `run_autoattack_run2.py:67` ve `:240-241` `model.eval()` | KODDA VAR, METINDE YOK |
| F069 | (metinde yok) AA ozet McNemar'i ki-kare (sureklilik duzeltmeli) | `run_autoattack_run2.py:287` `stat = (abs(b - c) - 1) ** 2 / (b + c)`; metin McNemar "exact" (M:158) icin kesin test: `scripts/build_reference_sheet.py:34` `stats.binomtest(min(b, c), n, 0.5, alternative="two-sided")` | KODDA VAR, METINDE YOK (iki ayri McNemar uygulamasi) |

## T7. Ornek sayilari, bootstrap, istatistik

| ID | Metin | Kod / dosya | Durum |
|---|---|---|---|
| F070 | Transfer tam test 10000, ornek bazli kayit (M:118) | `scripts/c1_transfer_rerun.py:39,54` n_samples 10000; `results/c1_transfer/pair{1,2,3}/transfer_summary.json` `n_samples: 10000, seed: 42, eps: 0.03137254901960784, steps: 10`; npz anahtarlari `source_clean_correct, target_clean_correct, source_adv_wrong, target_adv_wrong` | MATCH |
| F071 | Transfer saldirisi parti boyutu (metinde yok) | `experiments/run_all_analyses_run2.py:105` `test_batch_size=50`; kaynak PGD eval kipinde `:113` `PGDAttack(source_model, ...)` | KODDA VAR, METINDE YOK |
| F072 | Transfer GA: yuzdelik bootstrap, 10000 yeniden ornekleme (M:118) | `experiments/rev2/a2_transfer_protocols.py:37` `N_BOOT = 10000`; `:57-69` `rate_ci`; `results/c1_transfer/pair*/a2_transfer_protocols.json` `n_bootstrap: 10000` | MATCH |
| F073 | Es bootstrap GA, farklar icin 10000 (M:158) | `a2_transfer_protocols.py:113-118` ayni N_BOOT; `experiments/rev2/a3_gradient_paired.py:40` `N_BOOT = 10000` | MATCH |
| F074 | Isaret cevirme permutasyon testi 20000 (M:158) | `a2_transfer_protocols.py:38` `N_PERM = 20000`; `:120-124`; json `n_permutation: 20000` | MATCH |
| F075 | Rastgele akis tohumu | `a2_transfer_protocols.py:25-36` SEED=42, tuketici adina bagli `default_rng([SEED, crc32(etiket)])` | KODDA VAR, METINDE YOK |
| F076 | (metinde yok) diger bootstrap sayilari | `experiments/c1_c4_attention_features.py:51` `n_boot=2000` (dikkat/oznitelik GA); `experiments/run_all_analyses_run2.py:73` `n_boot: int = 1000`, cagri `:167` `n_boot=1000` (transfer_summary.json `conditioned_ci95`); `experiments/c1_c2_tgr.py:172` `n_boot=10000` | KODDA VAR, METINDE YOK |
| F077 | TOST birincil marj +-2 puan, "kosular arasi PGD degiskenliginden" turetildi (M:158) | `a2_transfer_protocols.py:129` izgara `[1, 2, 3]` puan, hepsi raporlanir; `experiments/run_stat_addendum.py:58` `DELTA = 0.02` (yol karantina: `stat_addendum`); marjin turetildigini gosteren dosya/satir bulunamadi | NOT FOUND (turetme kaydi); +-1/+-3 raporu MATCH |
| F078 | TOST "iki tek tarafli test" (M:158) | `a2_transfer_protocols.py:126-135` es-orneklem normal yaklasim (z; `se = d.std(ddof=1)/sqrt(n)`), `max(p_low, p_up) < 0.05`; t degil | MATCH (z-yaklasimi) |
| F079 | Wilcoxon isaretli sira + Holm (uc seyreklik olcusu) (M:158) | `experiments/rev2/a3_gradient_paired.py:142-152` kendi uygulamasi, normal yaklasim, baglanti duzeltmesi yok; Holm `:175` sonrasi; `experiments/c1_c5_spatial_locality.py:167-170` `scipy.stats.wilcoxon` | MATCH (uygulama ayrintisi metinde yok) |
| F080 | McNemar kesin (M:158) | `scripts/build_reference_sheet.py:34` binomtest iki yonlu | MATCH |
| F081 | Run duzeyi test 3 tekrar uzerinde (M:158) | `scripts/c1_seed_analysis.py:28` `_binomtest`; run duzeyi gradyan p degerleri `04_experiments.tex:303` (0.036, 0.042, 0.067) kodda ayri kontrol edilmedi | NOT FOUND (bu betikle dogrulanmadi) |
| F082 | Gradyan analizi 500 ornek (M:121) | `experiments/run_all_analyses_run2.py:257-258` `n_samples = 500; batch_size = 50`; `a3_gradient_paired.py:39` `N_SAMPLES = 500`; ornekler test setinin ilk 500'u (`shuffle=False`, `datasets.py:78-84`) | MATCH |
| F083 | Gradyan kayip: ornek bazli, parti boyutundan bagimsiz (M:121) | `src/analysis/gradient_analysis.py:34-37` `CrossEntropyLoss(reduction="sum")`; a3 `:81` ayni; gradyan temiz girdi, gercek etiket, eval kipi (`a3_gradient_paired.py:88,98-103`) | MATCH |
| F084 | Alignment = 500 ornegin tum cift ortalama mutlak kosinusu (M:121-123; 04_experiments.tex:279 "all 500x499/2 sample pairs") | tabloya giren (`results/c1_gradient/pair*/gradient_summary.json`) `gradient_alignment`: `run_all_analyses_run2.py:311` `compute_gradient_alignment(images, labels)` 50'lik parti ici tum cift (`gradient_analysis.py:237-279`), 10 parti ortalamasi, `std_semantics: 'std across batch means (10 batches of 50)'`. Degerler ResNet 0.0377/0.0370/0.0388 (ort 0.0378), ViT 0.0557/0.0564/0.0565 (ort 0.0562) = tablo (04_experiments.tex:293). Tum-cift tahmincisi `results/c1_a3/pair*/a3_gradient_paired.json` `all_pairs_abs_mean` ResNet 0.0382/0.0372/0.0390 (ort 0.0381), ViT 0.0558/0.0569/0.0570 (ort 0.0566), `n_pairs: 124750` | MISMATCH |
| F085 | Isaretli ort. kosinus "her model icin sifira yakin" (M:125); tablo isaretli sutun 0.0014 / 0.0005 (04_experiments.tex:294) | `results/c1_a3/pair1/...` `all_pairs_signed_mean` ResNet 0.0014, ViT 0.0005 (yalniz 1. cift); 2. ve 3. cift ResNet 0.0008/0.0008, ViT 0.0004/0.0004 | olgu kaydi (tablo = 1. cift) |
| F086 | Mekansal yerellik n (metinde 500 ornek degil acik; M:128) | `experiments/c1_c5_spatial_locality.py:105-106` `--n-samples default=500, --batch default=50` | MATCH |
| F087 | Dikkat metrikleri n=1000 ornek/kosu (M:134) | `experiments/c1_c4_attention_features.py:107` `--n-samples default=1000` | MATCH |
| F088 | Dikkat: son-softmax CLS->yama satiri, kafa ortalamasi (M:134) | `src/models/vit.py:341-352` `attn[:, :, 0, 1:]`, `.mean(dim=1)`; entropi icin satir yeniden normalize (`:348`) | MATCH |
| F089 | Dikkat yer degistirmesi = temiz ve adv. dagilimlar arasi toplam varyasyon mesafesi, sinir 1 (M:134) | `c1_c4_attention_features.py:190-192` `d = (am - cm).flatten(2).abs().sum(-1) / 2.0`, `cls_maps` YENIDEN NORMALIZE EDILMEZ (`vit.py:350-355`; satir toplami 1 - CLS->CLS dikkat); entropi ise yeniden normalize (`vit.py:348`) | MISMATCH (kapsam: TV, normalize edilmemis kutle uzerinde) |
| F090 | Dikkat/oznitelik analizinde ornekler | tum 1000 ornek (cevirilen/cevirilmeyen ayrimsiz) ve her model kendi PGD-10'una (`c1_c4_attention_features.py:143-144`) | KODDA VAR, METINDE YOK |
| F091 | Token toplama: yalniz CLS, 196 yama ortalamasi, tum jetonlarin duzlestirilmesi (M:131) | `c1_c4_attention_features.py:155-175` `cos_cls` (`a[:,0]`), `cos_mean` (`a[:,1:].mean(1)`), `cos_flat`/`cos_block` (duzlestirilmis) | MATCH |
| F092 | Ozellik bozulma: kosinus, norm degisimi yuzde, L2 mesafe (M:140-148) | `c1_c4_attention_features.py:171-175` kosinus ve `((flat_b.norm - flat_a.norm)/flat_a.norm*100)`; L2 mesafe bu dosyada yok; `experiments/run_all_analyses_run2.py:524` `torch.norm(clean_feat - adv_feat, p=2, dim=-1).mean()` (c1_drift cikti yolu) | MATCH (L2 mesafe baska dosyada) |

## T8. Transfer protokolleri ve maskeler

| ID | Metin | Kod | Durum |
|---|---|---|---|
| F093 | Dort protokol: ham, hedef-dogru, her-ikisi-dogru, basarili-kaynak (M:7, M:118) | `src/analysis/protokoller.py:28` `PROTOKOLLER = ["raw","target_correct","both_correct","successful_source"]` | MATCH |
| F094 | raw maskesi | `protokoller.py:58` `np.ones_like(tc)` | MATCH |
| F095 | hedef-dogru maskesi | `protokoller.py:59` `tc` (hedef temizde dogru) | MATCH |
| F096 | her-ikisi-dogru maskesi | `protokoller.py:60` `tc & sc` | MATCH |
| F097 | basarili-kaynak (kanonik, siki) maskesi | `protokoller.py:62` `tc & sc & sa` (sa = kaynak kendi cekismeli ornegini yanlis siniflar; `a2_transfer_protocols.py:87` `ss_definition: "target_clean_correct & source_clean_correct & source_adv_wrong"`) | MATCH (siki okuma; M:118 ikinci cumle ve 04_experiments.tex:119 "stricter reading") |
| F098 | Gevsek varyant yalniz duyarlilik (04_experiments.tex:119) | `protokoller.py:31,66` `TANI_PROTOKOLLERI=["successful_source_loose"]`, `tc & sa`; `yayilim` (`:92-95`) yalniz dort kanonik protokolu kullanir | MATCH |
| F099 | Basarili-kaynak tanim cumlesi (M:118): "target-correct samples whose attack succeeded on the source in the white-box sense" | maske ayrica `sc` (kaynak temizde dogru) ister (`protokoller.py:62`); cumlede kaynak temiz dogrulugu anilmaz; devamindaki cumle ("pool restricted to samples both models classify correctly") anar | MISMATCH (ilk tanim cumlesi kodun alt kumesi) |
| F100 | Siki/gevsek asimetri 19.37 / 14.60; yayilim 15.01 / 10.45 (04_experiments.tex:119) | `results/c1_transfer/pair{1,2,3}/a2_transfer_protocols.json` `diff_CNNtoViT_minus_ViTtoCNN` siki: 20.80, 18.91, 18.39 (ort 19.37); gevsek: 16.14, 14.46, 13.19 (ort 14.60) | MATCH |
| F101 | `source_adv_wrong` kaydi: ham (adv tahmin != etiket), kaynagin temiz hatasini da icerir | `run_all_analyses_run2.py:148` `src_adv_wrong.append((src_adv_pred != labels))`; `c1_c3_transfer_matrix.py:169-182`; olcum pair1 ResNet->ViT: `source_adv_wrong & ~source_clean_correct` = 1463 ornek; tc=7410, tc&sc=7126, siki=2821, gevsek=3105 (`results/c1_transfer/pair1/per_sample_ResNet18_AT_to_ViT_Tiny_AT.npz`) | olgu kaydi |
| F102 | Birincil yon kestirimi her-ikisi-dogru, es cikarim (M:118) | `a2_transfer_protocols.py:103-124` ortak kume, es bootstrap ve permutasyon | MATCH |
| F103 | Transfer: kaynakta PGD-10 (eps 8/255, alpha 2/255), kaynak ve hedef ayni 10000 ornek | `c1_transfer_rerun.py:54` -> `run_all_analyses_run2.py:113`; hedef = ayni model icin kaynak nesnesi (`:119-120`) | MATCH |
| F104 | Isi hesaplandigi ornek sirasi/parti | `run_all_analyses_run2.py:105` test_batch_size=50, `shuffle=False` | KODDA VAR, METINDE YOK |

## T9. TGR uyarlamasi (M:136-137)

| ID | Metin | Kod | Durum |
|---|---|---|---|
| F105 | TGR (Zhang vd. 2023) uyarlamasi | `experiments/c1_c2_tgr.py:10-15` docstring "BU BIR UYARLAMADIR"; yayimlanan yontemin kaynak kodu depoda yok (`grep` yalniz `c1_c2_tgr.py`, `debug_tgr_hooks*.py`, `_t4_tgr.py`) | olgu kaydi |
| F106 | Butce eps 8/255, alpha 2/255, 10 adim, momentum 1.0 (M:137) | `c1_c2_tgr.py:38` `EPS, ALPHA, STEPS, MU = 8/255, 2/255, 10, 1.0`; `res["attack_budget"]` `:234` | MATCH |
| F107 | gamma = 0.5, uc yolda tek deger (M:137) | `c1_c2_tgr.py:59` `GAMMA = 0.5`; `:62-72,80-90` `out = grad * gamma` her uc yolda ayni sabit | MATCH |
| F108 | Dikkat, QKV, MLP yollarinda geri yayilim sirasinda uc degerler sifirlanir (M:137) | `c1_c2_tgr.py:116-118` `register_full_backward_hook`: `blk.attn.attn_drop` (dikkat), `blk.attn.qkv`, `blk.mlp.fc2`; `attn.proj` kancalanmaz (`:114-115` yorum) | MATCH |
| F109 | "(ornek, kanal) basina jetonlar arasi bir max ve bir min girdi sifirlanir" (M:137) | `c1_c2_tgr.py:62-77` (qkv ve mlp yolu, girdi (B,N,C)): kanal basina `argmax/argmin` jeton ekseninde, `scatter(..., 0.0)` ile tek hucre | MATCH (qkv ve mlp yollari) |
| F110 | Ayni cumle dikkat yolu icin | `c1_c2_tgr.py:80-93` dikkat gradyani (B,H,N,N): her (ornek, kafa) icin N*N duzlestirilmis izgarada tek `argmax` ve tek `argmin` hucre sifirlanir; "kanal" ekseni yok | MISMATCH (dikkat yolunda birim (ornek, kafa), jeton-jeton izgarasi) |
| F111 | Tum satir/sutun degil (M:137) | `c1_c2_tgr.py:73-76,91-92` tek hucre | MATCH |
| F112 | gamma olcekleme zeroing'den once tum girdilere | `c1_c2_tgr.py:72` `out = grad * gamma`; sifirlama `:75-76` | KODDA VAR, METINDE YOK (kalan gradyan "gamma ile olceklenir" ifadesiyle uyumlu) |
| F113 | Ayni calismada MI-FGSM eslesmis kontrol (M:137) | `c1_c2_tgr.py:216-217` `adv_tgr = mifgsm(..., use_tgr=True)`, `adv_mi = mifgsm(..., use_tgr=False)` ayni batch | MATCH |
| F114 | MI-FGSM: L1 normalize gradyan, momentum 1.0, rastgele baslangic yok | `c1_c2_tgr.py:149-169`: `grad / grad.abs().flatten(1).mean(1)`, `momentum = mu*momentum + grad`, `adv = x.clone()` baslangic | KODDA VAR, METINDE YOK |
| F115 | Yayimlanan yontem ayrintilari (yol-basina katsayilar, satir/sutun) | `scripts/_t4_tgr.py:11-13` "ozgun TGR'nin yol-basina katsayilarini BIRINCI ELDEN dogrulamadim" | NOT FOUND (birincil kaynakla karsilastirma depoda yok) |
| F116 | Kaynak ve hedef: ViT-Tiny AT -> ResNet-18 AT, 10000 ornek, parti 50 | `c1_c2_tgr.py:200-202,185,235` | KODDA VAR, METINDE YOK (yon: yalniz ViT->CNN) |
| F117 | TGR sonuclari, 3 cift (hedef-dogru / her-ikisi-dogru, TGR vs MI) | `results/c1_c2/pair{1,2,3}/tgr_summary.json`: TGR hedef-dogru 13.18/12.46/12.47, MI 15.13/15.66/16.33; TGR her-ikisi-dogru 8.41/7.73/7.65, MI 9.74/10.20/10.31; beyaz kutu kaynak 51.2/52.48/51.0 (TGR) vs 66.28/66.76/66.25 (MI); es McNemar tgr_only/mi_only 71/166, 50/225, 36/222 | olgu kaydi |

## T10. ViT yerel cozunurluk kontrolu (M:46-50 dolayli, 04_experiments.tex:279, 297-299, 05_discussion.tex:61)

| ID | Metin | Kod / kayit | Durum |
|---|---|---|---|
| F118 | 32x32 girdi, 4x4 yama, yukseltme yok | `src/models/vit.py:201-223` `vit_cifar_tiny`: `CIFARViT(img_size=32, patch_size=4, embed_dim=192, depth=12, num_heads=3, mlp_ratio=4., drop_rate=0.1, attn_drop_rate=0.0)`; 64 yama (`:30`) | MATCH |
| F119 | Parametre 5.4M (04_experiments.tex:297) | olcum 5,362,762; `logs/vit_cifar_tiny_clean.log:3` ayni | MATCH |
| F120 | Dropout (metinde yok) | native `drop_rate=0.1` (`vit.py:221`; olcum p = {0.0, 0.1}); main ViT-Tiny dropout 0 (F010) | KODDA VAR, METINDE YOK |
| F121 | "tek kontrol noktasi, sabit bolme oncesi, test uzerinde secilmis" (04_experiments.tex:297-299) | `models/vit_cifar_tiny/adv/vit_cifar_tiny/adv/adversarial_training/best.pth` mtime 2026-01-10 01:50; `logs/vit_cifar_tiny_at.log:1-6` val bolmesi mesaji yok; tqdm 391 batch/epoch (50000/128) = tum egitim seti | MATCH |
| F122 | (metinde yok) native AT gunlugu | `logs/vit_cifar_tiny_at.log` son satir "Epoch 60/100 ... 9/391" (mid-epoch), `Epoch 59/100 - ... Adv: 23.23%` son tamamlanan epoch; "Early stopping" mesaji yok; en iyi kaydedilen adv. dogruluk 31.78% (satir 44); `TRAINING_COMPLETE`/`last.pth` yok (dizinde yalniz `best.pth`) | KODDA VAR, METINDE YOK |
| F123 | (metinde yok) native temiz asama | `logs/vit_cifar_tiny_clean.log:1-4` 200 epoch, lr 0.001, batch 128, AdamW; 200 epoch kaydi var | KODDA VAR, METINDE YOK |
| F124 | (metinde yok) native egitim sirasinda saldiri kipi | `src/defenses/adversarial_training.py:103-108` yorum: "Onceki surum saldiriyi eval-mode ... uretiyordu" (duzeltme 2026-07-11); native checkpoint 2026-01-10 | KODDA VAR, METINDE YOK |
| F125 | Native gradyan sayilari (Hoyer 0.405, Gini 0.571, <%1 17.9%, alignment 0.079) | `results/c1_gradient/pair{1,2,3}/gradient_summary.json` `statistics.ViT_CIFAR_Native_AT`: hoyer 0.40459, gini 0.57123, rel 0.17850, alignment 0.07941 (ucu de ayni, ayni checkpoint); `model_paths.ViT_CIFAR_Native_AT = None` | MATCH (alignment: 50'lik parti ici, bkz. F084) |
| F126 | Native modelin gradyan yontemi | `run_all_analyses_run2.py:262-267` checkpoint varsa `models_to_analyze`'a eklenir; ilk 500 test ornegi, eval kipi | KODDA VAR, METINDE YOK |

## T11. Kontrol noktasi secimi: ozet izlenebilirlik

| ID | Soru | Kanit | Durum |
|---|---|---|---|
| F127 | Raporlanan kosulari hangi kural uretti? | egitim sirasinda val PGD-10 + `> best+0.1`, patience 20: `adversarial_trainer.py:479-500`; C1 donemi `git show c7eb7cb:src/training/adversarial_trainer.py` satir 398, 412-416 ayni | olgu kaydi |
| F128 | C1 donemi ile HEAD arasi egitim kodu farki | `git diff c7eb7cb HEAD --stat -- src/training src/defenses src/data cli src/models`: 6 dosya; `src/defenses/adversarial_training.py` diff bos; `adversarial_trainer.py` farki grad_clip parametrelestirme, eps-isitma, TRAINING_COMPLETE, save_every; `vit.py` farki gercek dikkat cikarimi | olgu kaydi |
| F129 | Offline secim kurali (E2/CIFAR-100) | `scripts/q1_offline_select.py:5-7`; secim izgarasi 18 hucre: F050 | MATCH |
| F130 | Val bolmesi hem temiz hem AT secimini besler (M:100) | F021, F040 | MATCH |

## T12. Metinde bulunmayan, kodda dogrulanan ek olgular (secim; kayit amacli)

| ID | Olgu | Konum |
|---|---|---|
| F131 | Egitim yukleyicisi `num_workers=2`, `shuffle=True`; val/test `test_batch_size=100`, `shuffle=False` | `src/data/datasets.py:165-185` (C1 donemi), `:371-378` (HEAD) |
| F132 | ViT AT checkpoint secimi, egitim yarisindan once (epoch 18-25 / 100 toplam bütçe) | F047 |
| F133 | Temiz ViT clean val dogrulugu 81.9-83.85, AT baslangic epoch-1 val temiz 61.40% (ViT 2001) | `logs/C1_clean_vit_2001.log`, `logs/C1_at_vit_2001.log:11` |
| F134 | `c1_pgd_eval.py` test batch 100; transfer/gradyan/TGR/dikkat batch 50 | `scripts/c1_pgd_eval.py:53-54`; `run_all_analyses_run2.py:105,258`; `c1_c2_tgr.py:185` |
| F135 | `cli evaluate robustness` `ModelRegistry.get(model_type)` ile `num_classes=10` ve `load_model_weights` kullanir; `c1_pgd_eval` `load_model_auto` kullanir | `cli/evaluate.py:84-86`; `scripts/c1_pgd_eval.py:49` |
| F136 | Sizinti bayrak yolu: `--val-split` varsayilan 2000 ama `--val-indices` verilince yoksayilir | `cli/train.py:122-125,176-192` |
| F137 | Q1 boru hatti ViT-Tiny temiz asama batch'i 128, AT 64; ResNet 128/128 (CIFAR-100/SVHN icin) | `scripts/q1_pipeline.sh:104-111` (C1 ile ayni degerler) |

---

Kaynak anahtarlari: `M:` = `paper/manuscript/sections/03_methodology.tex`. Gecici betikler `raporlar/hakem_lecun_2026-10-04/_tmp/a2_*.{py,sh}` altinda. Hicbir manuscript, veri veya betik dosyasi degistirilmedi.
