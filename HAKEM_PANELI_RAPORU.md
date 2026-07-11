# Hakem Paneli Raporu ve Revizyon Durumu (2026-07-07)

3 Fable hakem subagent'ı (reproducibility denetçisi + SCI hakemi + kod denetçisi)
paralel inceleme yaptı; moderatör bulguları birleştirdi; 17 kritik/majör bulgunun
**17'si de** bağımsız çürütücü doğrulayıcılar tarafından ONAYLANDI (0 çürütüldü).
Panel kararı: **mevcut haliyle gönderilemez** — ama çalışma kurtarılabilir:
modeller gerçekten eğitilmiş ve ölçülmüş; sorun sayıların/figürlerin sunumu ve
birkaç metodolojik hata.

## Kritik Bulgular (5)

| ID | Bulgu | Durum |
|----|-------|-------|
| M1 | 5 figür (4a,4b,5a,5b,5) np.random/torch.rand **demo verisinden** üretilmiş (checkpoint yolu yanlış → sessiz fallback) | Kod düzeltildi; figürler makalede yoruma alındı; R8 ile yeniden üretilecek |
| M2 | Fig2 epsilon sweep `# Interpolated` **hardcoded** değerler; gerçek tarama (bildiri_eps_sweep) 9-11pp farklı | Hardcoded dict silindi; figür yorumda; R4 gerekli |
| M3 | Transfer "asimetrisi" (5.1pp) hedef temiz-hata farkının artefaktı; **düzeltilince kayboluyor/tersine dönüyor** | Koşullu fooling-rate metriği kodlandı; makale anlatısı düzeltildi; R6 gerekli |
| M4 | Fig3 heatmap **run1** verisi (47.5/33.5), başlık/tablo run2 (41.2/36.1) diyor | Yükleyici run3 JSON'a bağlandı, placeholder silindi; R6+R8 |
| M5 | Fig1'de **kaynağı olmayan** FGSM değerleri (48.5/70.2/42.3) + yanlış "PGD-20" etiketi | known_results dict silindi, gerçek artefakt yükleyici yazıldı; figür yorumda |

## Majör Bulgular (12, hepsi onaylı)

- **M6** 3.6pp AA farkı n=500'de anlamsız (p≈0.23, CI ±4.2pp) → metin yumuşatıldı; R5 (n=10k + McNemar) karar verecek
- **M7** Tablo 1 PGD değerleri test-seti üzerinden **model seçimi maksimumu** (selection leakage); Tablo 5 ile çelişiyor (40.97 vs 40.03) → trainer'a val-split eklendi; açıklama makaleye girdi; R3 gerekli
- **M8** Metodolojide **yapılmamış** "10.000 örnek + bootstrap CI + p<0.001" iddiası → silindi; koşullu metrik tanımı yazıldı
- **M9** fig4_gradient/tsne/adv_examples **run1** checkpoint'lerinden → yollar at_run2'ye çevrildi; R8
- **M10** AT eğitiminde saldırı gradyanları parametre güncellemesine **karışıyor** (`loss.backward()` birikimi) → `torch.autograd.grad` ile düzeltildi (AT+TRADES+MART); yeniden eğitim önerilir (R1/R2) veya limitation
- **M11** Sparsity metriği (|g|<1e-6) **ölçek bağımlı** + 32→224 upsample confound'u → Hoyer/Gini/göreli-eşik eklendi; native-ViT kontrolü koda bağlandı; R7
- **M12** "pretrained ImageNet backbones" iddiası yanlış (scratch eğitim) → düzeltildi, recipe-duyarlılık atıfları eklendi (Debenedetti 2023, Mo 2022)
- **M13** Tablo 1 clean değerleri n=500 alt kümesinden; gerçek fark 8.2pp değil ~6.1pp → metin düzeltildi; R3
- **M14** WRN 66.05 = RobustBench **PGD-20**, PGD-10 sütununda → dipnot açıklaması; run_wrn_eval.py yazıldı (R9)
- **M15** Deney scriptlerinde seed yok (AutoAttack dahil) → tam seed eklendi (cudnn deterministic dahil)
- **M16** "first systematic layer-wise analysis" aşırı iddia (Bhojanapalli/Shao mevcut) → yeniden konumlandırıldı
- **M17** run_sci_analysis.py'de gizli çift-normalizasyon (default'ta ~5x epsilon) → default False + assertion + protokol hizası

Minörler (M18-M26): shuffle iddiası, MLP-hook "attention" adlandırması, n=512/112,
alignment alt-örnekleme, early-stopping saklanması, 6-7% tutarsızlığı, NaN-guard
sırası, Wei→Zhu vb. — tamamı işlendi.

## Uygulanan Düzeltmeler

**Kod (16 dosya):** `src/defenses/{adversarial_training,trades,mart}.py` (M10),
`src/training/adversarial_trainer.py` (M25 + val_loader/M7),
`src/analysis/gradient_analysis.py` (M11/M21), `src/models/vit.py`
(get_attention_maps — gerçek attention çıkarımı), `src/data/datasets.py`
(+get_cifar10_loaders_with_val), `cli/train.py` (--val-split),
`experiments/run_autoattack_run2.py` (argparse+seed+per-sample+McNemar),
`experiments/run_all_analyses_run2.py` (koşullu transfer+bootstrap CI+--only+seed+tam n),
`experiments/run_sci_analysis.py` (M17), `experiments/run_wrn_eval.py` (YENİ),
`paper/figures/*` (tüm demo/fallback/hardcoded yollar söküldü — eksik artefakt
artık **hata verir**, sessizce sahte veri çizmez). Tümü py_compile'dan geçti.

**Makale:** abstract + 6 bölüm; asılsız iddialar silindi, confound'lar açıklandı,
fabrikasyon figürler yoruma alındı (`% TODO(run3-...)` işaretli), LaTeX temiz
derleniyor (0 undefined ref/citation). Koşular bitince TODO işaretli yerler
gerçek sayılarla güncellenecek.

## Bekleyen Koşular (kullanıcı onayı gerekli)

**KARAR NOKTASI:** Yol A (önerilen) = M10 düzeltmesiyle **yeniden eğitim (run3)**,
~15-28 GPU-saat ekstra; Yol B = run2 checkpoint'leriyle devam + M10 limitation
paragrafı (05_discussion'da hazır, yorumda).

| # | Komut | Süre (RTX 5060 Ti) | Ne çözer |
|---|-------|--------------------|----------|
| R1* | `python -m cli.main train adversarial --model resnet18 -d adversarial_training -p models/resnet18/clean/best.pth -e 100 --lr 0.001 -b 128 --patience 20 --val-split 2000 -o models/resnet18/adv/at_run3 --seed 42` | ~5-8 sa | M10+M7 (temiz AT + val seçimi) |
| R2* | aynısı `--model vit_tiny -b 64 --seed 123 -o models/vit_tiny/adv/at_run3` | ~8-12 sa (early stop) | M10+M7 |
| R3 | `cli.main evaluate robustness` ×4 (AT+clean, her model; `-a fgsm -a pgd -e 0.03137...`, `-o results/final_eval/...`) | ~1.5-2 sa | M7/M13/M23 — Tablo 1 tek tutarlı kaynak |
| R4 | eps sweep: `-a pgd -e 2/255 -e 4/255 -e 8/255 -e 16/255 -o results/epsilon_sweep_run3/<model>` | ~2-3 sa | M2 — gerçek fig2 |
| R5 | `python experiments/run_autoattack_run2.py --n-samples 10000 --seed 42 --output-dir results/autoattack_run3_full` | ~10-14 sa | M6 — anlamlılık kararı (McNemar otomatik) |
| R6 | `python experiments/run_all_analyses_run2.py --only transfer --n-samples 10000 --seed 42` | ~1.5-2.5 sa | M3 — asimetri kalıyor mu? |
| R7 | `python experiments/run_all_analyses_run2.py --only gradient --seed 42` | ~20-40 dk | M11 — sparsity gerçek mi artefakt mı |
| R8 | `--only attention` + `python paper/figures/generate_advanced_figures.py` + `python paper/figures/generate_from_experiments.py --all` + final/ kopyala | ~30-60 dk | M1/M9 — tüm figürler gerçek veriden |
| R9 | `python experiments/run_wrn_eval.py` | ~1-1.5 sa | M14 — WRN yerel artefakt |
| R10 | `--only statistical --seed 42` | ~30-60 dk | Tablo 5 tazeleme (yalnız retrain olduysa) |

\* R1/R2 yalnız Yol A'da. Yol B'de R3-R9 run2 yollarıyla koşulur
(`--resnet-path/--vit-path` argümanları mevcut).

Sıra: (R1,R2) → R3 → (R4,R5,R6,R7,R9 paralel/sıralı) → R8 → R10 → makale
TODO'larını gerçek sayılarla doldur → yeniden derle.

**Not:** Koşulardan önce `nvidia-smi` (GPU paylaşımlı, vit_ecl kontrol).
Transkript/plan: scratchpad `panel_plan.json`.

---

## GÜNCELLEME (2026-07-07 akşam): Pipeline başlatıldı + M10 sonrası ek bulgu

**Kesintiye dayanıklılık eklendi:**
- Trainer'a `--resume` (her epoch atomik `last.pth`: model+optimizer+scheduler+epoch+patience+history; `TRAINING_COMPLETE` işareti)
- AutoAttack 1000'lik chunk'larla kaydediyor (kesintide yalnız yarım chunk tekrarlanır)
- `run_revision_pipeline.sh`: idempotent R1→R10 zinciri (tamamlanan adım atlanır)
- **Kesinti sonrası tek komut:** `bash ~/projects/adeb_sci_1/scripts/resume_pipeline.sh`
  (tmux `revpipe` oturumu; izleme: `tail -f logs/revision_pipeline.log`)

**M10 düzeltmesinin ortaya çıkardığı ek bulgu (M27):** Temiz AT ile ilk run3
denemesi çöktü (epoch 8'de clean %16). Teşhis (`scripts/diagnose_at_collapse2.py`):
saldırının **eval modda** üretilip eğitimin **train modda** yapılması BN
istatistik uyumsuzluğu yaratıyor; run2'de M10 kirliliği (eval-mode gradyanlar)
bunu istemeden maskeliyordu. Düzeltme: saldırı üretimi eğitim moduyla tutarlı
(Rice et al. 2020 standard AT pratiği; `src/defenses/adversarial_training.py`).
Kanıt: 300-batch testte eval-val %50'ye çöküş → düzeltmeyle %83'te stabil;
tam eğitimde Epoch1 Clean %82.0/Adv %14.5, Epoch2 %82.3/%20.9 (sağlıklı).
Metodolojiye cümle + rice2020overfitting atıfı eklendi.

**Ortam notları:** `adeb_eval` konteyneri imajdan yeniden oluşturuldu
(`--ipc=host`; ilk pip denemesi torch'u ezmişti — bozuk kopya `adeb_eval_broken`
adıyla duruyor, silinebilir). Eksik paketler `--no-deps` ile kuruldu
(timm, autoattack, robustbench, geotorch, torchdiffeq + saf-python bağımlılıklar).
Validasyon notu: val split AT aşamasında ayrılıyor; örnekler clean-pretraining'de
görüldüğünden val clean acc şişkindir (%99+) — seçim yine leakage-free (test'e
dokunmuyor); makalede beyan edildi (3.5).

---

## SONUÇ (2026-07-09): Tüm koşular bitti, makale run3 sayılarıyla güncellendi

**Run3 final sonuçları (tam test, n=10.000, seed 42):**

| Model | Clean | FGSM | PGD-10 | AutoAttack |
|---|---|---|---|---|
| ResNet-18 AT | 85.42 | 49.91 | 40.91 | **35.74** |
| ViT-Tiny AT | 75.65 | 40.07 | 35.99 | **32.94** |
| WRN-28-10 (yerel) | 89.48 | 70.91 | 66.92 | 62.76 (RB) |

- **AA farkı 2.80pp, McNemar p=3.1e-12** (940 vs 660 tek-taraflı doğru) → ana iddia artık istatistiksel olarak sağlam (M6 çözüldü).
- **Transfer (koşullu, n=10k):** CNN→ViT 20.95 [20.08-21.92] vs ViT→CNN 20.32 [19.46-21.21] → **asimetri YOK**; ham metrik 8.3pp sahte asimetri üretiyordu (M3 kanıtlandı). White-box koşullu ~%52.2/52.3 (simetrik!). Makale bunu metodolojik bulgu olarak sunuyor.
- **Gradient (per-sample tanım, ölçek-bağımsız):** Hoyer 0.474 vs 0.449; Gini 0.634 vs 0.606; native-ViT kontrolü daha da az sparse → upsample artefaktı DEĞİL (M11 çözüldü, iddia mütevazılaştırıldı). Alignment (tüm-çiftler): 0.038 vs 0.052 → ViT 1.36× (run2'deki "neredeyse özdeş" bulgusu alt-örnekleme + eski model artefaktıymış; anlatı güncellendi).
- **Feature degradation (12 blok, n=100):** 0.994 → min 0.955 (Blok 8) → 0.965 plato; "monotonik ilerleyici" değil "erken-düşüş + orta-ağ platosu" (M19 uyarınca yeniden çerçevelendi).
- **Eğitim:** R1 epoch 84 early-stop; R2 epoch 51. M27 (BN mod tutarlılığı) düzeltmesiyle clean acc +3.6/+2.1 puan.

**Makale durumu:** Abstract + 6 bölüm run3 sayılarıyla güncellendi; TÜM figürler
gerçek artefaktlardan yeniden üretildi ve fig1/fig2/fig3 görsel olarak
kaynak-veriyle doğrulandı (fig2'de WRN epsilon-eşleşme bug'ı bulunup düzeltildi);
tüm TODO(run3) işaretleri kapatıldı (tek kalan: gönderim öncesi gerçek repo URL'si);
latexmk temiz derleniyor (0 undefined ref/citation).

**Kalan işler:** (1) intihal kontrolü (iThenticate), (2) repo URL'si + IEEE Author
Portal yüklemesi, (3) isteğe bağlı: cover letter'ın run3 sayılarıyla revizyonu,
(4) git commit (çalışma ağacında büyük değişiklik seti birikti).
