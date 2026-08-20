#!/bin/bash
# =============================================================================
# Q1 GENISLETME PIPELINE'I (arastirma raporu: results/q1_research/Q1_ARASTIRMA_RAPORU.md)
# Kosum sirasi: E2 -> E1 -> E5-pilot -> E5 (E3 degerlendirmesi ayri; E0 kod tamam)
#
# Idempotenlik: guard = TRAINING_COMPLETE (best.pth DEGIL - yarim egitim
# yarim kabul edilmez; rapor Bolum 8 Adim 1). Kesinti sonrasi ayni komut
# --resume ile kaldigi yerden devam eder.
#
# Kullanim (konteyner icinde, arka planda):
#   STAGE=e2       bash scripts/q1_pipeline.sh   # sizinti ablasyonu (~19-28 GPU-sa)
#   STAGE=e1       bash scripts/q1_pipeline.sh   # CIFAR-100 ana cift (~36-45 GPU-sa)
#   STAGE=e5pilot  bash scripts/q1_pipeline.sh   # R50+ViT-S 1 tohum (sure olcumu!)
#   STAGE=e5       bash scripts/q1_pipeline.sh   # R50+ViT-S kalan tohumlar
#   STAGE=e7       bash scripts/q1_pipeline.sh   # SVHN capasi (ilk dusecek kalem)
# =============================================================================
set -uo pipefail
cd /workspace || exit 1
mkdir -p logs data
STAGE="${STAGE:?STAGE ver: e2|e1|e5pilot|e5|e7}"
LOG="logs/q1_${STAGE}.log"
log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }

# print() ciktilari log dosyasina gecikmesiz aksin (blok tamponlama kapali)
export PYTHONUNBUFFERED=1

# Sert CUDA kontrolu: "auto" cihaz secimi CUDA yokken SESSIZCE CPU'ya duser
# (bu repoda yasandi: logs/C1_at_vit_2001.log "on cpu") - kampanya baslamadan kes
if ! python -c "import torch, sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    log "FAIL  CUDA gorunmuyor (torch.cuda.is_available()=False) - kampanya baslatilmadi"
    exit 1
fi

EPS8=0.03137254901960784

# guard: TRAINING_COMPLETE dosyasi (yarim egitim asla atlanmaz)
# Gecici hatalara (paylasilan GPU'da anlik OOM vb.) karsi 3 deneme; --resume
# sayesinde her deneme kaldigi yerden devam eder, is kaybi olmaz.
run_train() {
    local name="$1" ckdir="$2"; shift 2
    if [ -e "$ckdir/TRAINING_COMPLETE" ]; then log "SKIP  $name"; return 0; fi
    local attempt
    for attempt in 1 2 3; do
        log "START $name (deneme $attempt/3)"
        if "$@" --resume >> "logs/${name}.log" 2>&1 && [ -e "$ckdir/TRAINING_COMPLETE" ]; then
            log "DONE  $name"; return 0
        fi
        if [ "$attempt" -lt 3 ]; then
            log "RETRY $name (deneme $attempt basarisiz; 300 sn sonra --resume ile tekrar)"
            sleep 300
        fi
    done
    log "FAIL  $name (logs/${name}.log)"; exit 1
}

run_step() {
    local name="$1" guard="$2"; shift 2
    if [ -e "$guard" ]; then log "SKIP  $name"; return 0; fi
    local attempt
    for attempt in 1 2 3; do
        log "START $name (deneme $attempt/3)"
        if "$@" >> "logs/${name}.log" 2>&1 && [ -e "$guard" ]; then
            log "DONE  $name"; return 0
        fi
        if [ "$attempt" -lt 3 ]; then
            log "RETRY $name (deneme $attempt basarisiz; 300 sn sonra tekrar)"
            sleep 300
        fi
    done
    log "FAIL  $name (logs/${name}.log)"; exit 1
}

log "=============== Q1-${STAGE^^} BASLANGIC ==============="

# ---------------------------------------------------------------------------
# Mimari-basina hiperparametreler (rapor Bolum 5.3)
# clean:  <lr> <epochs> <batch> <ekstra...>
# at:     <lr> <epochs> <batch> <patience> <ekstra...>
# ---------------------------------------------------------------------------
# NOT: --device cuda ACIK verilir - "auto" CUDA kaybinda sessizce CPU'ya
# duserdi; acik deger fallback yapmaz, surec hata verir ve retry devreye girer.
clean_args() {
    case "$1" in
        resnet18|resnet50) echo "--device cuda --lr 0.1 --epochs 200 --batch-size 128" ;;
        vit_tiny)          echo "--device cuda --lr 0.001 --epochs 200 --batch-size 128" ;;  # C1 klonu
        vit_small)         echo "--device cuda --lr 0.001 --epochs 30 --batch-size 64 --timm-pretrained" ;;
    esac
}
at_args() {
    case "$1" in
        resnet18|resnet50) echo "--device cuda --lr 0.001 --epochs 100 --batch-size 128 --patience 20" ;;
        vit_tiny)          echo "--device cuda --lr 0.001 --epochs 100 --batch-size 64 --patience 20" ;;
        # ViT-S sigortalari (rapor 5.3): LR 5e-4, clip 1.0, 10ep eps-warmup,
        # 5ep lr-warmup, bs 64, 60 epoch butce
        vit_small)         echo "--device cuda --lr 0.0005 --epochs 60 --batch-size 64 --patience 20 --grad-clip 1.0 --eps-warmup 10 --lr-warmup 5" ;;
    esac
}

# Tam pipeline: clean pretrain -> AT finetune -> PGD eval  (dataset, arch, seed)
train_pair_member() {
    local ds="$1" arch="$2" seed="$3" val_json="$4" save_every="$5"
    local root="models/q1/${ds}/${arch}_s${seed}"
    local clean_dir="${root}/${arch}/clean"
    local at_dir="${root}/${arch}/adv/adversarial_training"

    run_train "Q1_${ds}_clean_${arch}_${seed}" "$clean_dir" \
        python -m cli.main train clean -m "$arch" --dataset "$ds" \
            $(clean_args "$arch") --seed "$seed" -o "$root" \
            --val-indices "$val_json"

    run_train "Q1_${ds}_at_${arch}_${seed}" "$at_dir" \
        python -m cli.main train adversarial -m "$arch" --dataset "$ds" \
            $(at_args "$arch") --seed "$seed" -o "$root" \
            --pretrained "${clean_dir}/best.pth" \
            --val-indices "$val_json" --save-every "$save_every" \
            --eps $EPS8

    run_step "Q1_${ds}_pgd_${arch}_${seed}" \
        "results/q1/${ds}/${arch}_s${seed}/pgd_summary_${arch}.json" \
        python scripts/c1_pgd_eval.py --model-type "$arch" --dataset "$ds" \
            --ckpt "${at_dir}/best.pth" \
            --out "results/q1/${ds}/${arch}_s${seed}"
}

case "$STAGE" in
# ---------------------------------------------------------------------------
e1)  # CIFAR-100 ana cift (RN18/ViT-T), 3 tohum, save_every 1
    # BOLME: sinif-dengeli (stratified) ZORUNLU - 100 sinifta rastgele 2000'lik
    # bolme sinif basina 7-35 ornek birakiyordu (secim metrigi asiri gurultulu).
    run_step Q1_val_split_c100 data/val_split_indices_cifar100.json \
        python experiments/rev2/make_val_split.py --dataset cifar100 --stratified
    # CIFTLESTIRILMIS SIRA (hakem onerisi): pair1 tam bitsin -> pair2 -> pair3.
    # Boylece ilk ViT kaniti ~2 saatte gelir ve on-kayitin istedigi 1-tohum
    # PILOT KAPISI dogal olarak olusur (asagidaki durdurma kurallari).
    # DURDURMA KURALLARI (pilot, logs/Q1_cifar100_*_2001.log):
    #   clean ViT-T val acc < %40      -> DUR: --timm-pretrained veya patch-4
    #   AT ilk 5 epok val adv-acc < %5 -> DUR: LR/eps-warmup gozden gecir
    for i in 1 2 3; do
        rs=$((1000 + i)); vs=$((2000 + i))
        train_pair_member cifar100 resnet18 "$rs" data/val_split_indices_cifar100.json 1
        train_pair_member cifar100 vit_tiny "$vs" data/val_split_indices_cifar100.json 1
        if [ "$i" = 1 ]; then
            log "PILOT KAPISI: pair1 tamam. logs/Q1_cifar100_clean_vit_tiny_2001.log"
            log "  ve *_at_vit_tiny_2001.log incelenmeli (clean val>=%40, AT ilk-5 adv>=%5)."
        fi
    done
    # AutoAttack: cift bazli (indeks eslesmesi: 1001<->2001 ...)
    for i in 1 2 3; do
        rs=$((1000 + i)); vs=$((2000 + i))
        run_step "Q1_c100_aa_pair${i}" "results/q1/cifar100/pair${i}/autoattack_summary.json" \
            python experiments/run_autoattack_run2.py --n-samples 10000 --seed 42 \
                --dataset cifar100 \
                --model "ResNet18_AT:resnet18:models/q1/cifar100/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth" \
                --model "ViT_Tiny_AT:vit_tiny:models/q1/cifar100/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth" \
                --output-dir "results/q1/cifar100/pair${i}"
    done
    ;;
# ---------------------------------------------------------------------------
e2)  # Sizinti ablasyonu: tam butce (patience KAPALI), her epoch ckpt, tek egitim
    # Guard = e2_val_C.json: bolme betiginin EN SON atomik yazdigi dosya -
    # varsa 5 dosyanin besi de tam demektir
    run_step Q1_e2_split data/e2_val_C.json python scripts/q1_make_e2_split.py
    for seed in 1001 1002 1003; do
        root="models/q1/e2/resnet18_s${seed}"
        run_train "Q1_e2_clean_resnet18_${seed}" "${root}/resnet18/clean" \
            python -m cli.main train clean -m resnet18 --dataset cifar10 \
                $(clean_args resnet18) --seed "$seed" -o "$root" \
                --val-indices data/e2_exclude_for_clean.json
        # DIKKAT (review bulgusu): AT baslangici best.pth DEGIL last.pth -
        # clean asamasinin secimi V_B uzerinden yapiliyor; V_B'nin "hic
        # kullanilmamis" kalmasi icin sabit-butce son checkpoint alinir
        run_train "Q1_e2_at_resnet18_${seed}" "${root}/resnet18/adv/adversarial_training" \
            python -m cli.main train adversarial -m resnet18 --dataset cifar10 \
                --device cuda --lr 0.001 --epochs 100 --batch-size 128 --patience 0 \
                --seed "$seed" -o "$root" \
                --pretrained "${root}/resnet18/clean/last.pth" \
                --val-indices data/e2_exclude_for_at.json --save-every 1 \
                --eps $EPS8
    done
    for seed in 2001 2002 2003; do
        root="models/q1/e2/vit_tiny_s${seed}"
        run_train "Q1_e2_clean_vit_tiny_${seed}" "${root}/vit_tiny/clean" \
            python -m cli.main train clean -m vit_tiny --dataset cifar10 \
                $(clean_args vit_tiny) --seed "$seed" -o "$root" \
                --val-indices data/e2_exclude_for_clean.json
        run_train "Q1_e2_at_vit_tiny_${seed}" "${root}/vit_tiny/adv/adversarial_training" \
            python -m cli.main train adversarial -m vit_tiny --dataset cifar10 \
                --device cuda --lr 0.001 --epochs 100 --batch-size 64 --patience 0 \
                --seed "$seed" -o "$root" \
                --pretrained "${root}/vit_tiny/clean/last.pth" \
                --val-indices data/e2_exclude_for_at.json --save-every 1 \
                --eps $EPS8
    done
    # Cevrimdisi secim: her yorungeye UC kural (V_A sizintili / V_B temiz /
    # V_C negatif kontrol). --test-eval: secilen checkpoint tam 10k test
    # kumesinde degerlendirilir (clean + PGD-10, ornek-bazli maskeler npz'ye) -
    # TOST/McNemar toplamasi bu ciktilardan yapilir
    for spec in "resnet18 1001" "resnet18 1002" "resnet18 1003" \
                "vit_tiny 2001" "vit_tiny 2002" "vit_tiny 2003"; do
        set -- $spec; arch="$1"; seed="$2"
        epdir="models/q1/e2/${arch}_s${seed}/${arch}/adv/adversarial_training/epochs"
        for cond in A B C; do
            run_step "Q1_e2_select_${arch}_${seed}_${cond}" \
                "results/q1/e2/select_${arch}_s${seed}_val${cond}.json" \
                python scripts/q1_offline_select.py --epochs-dir "$epdir" \
                    --model-type "$arch" --dataset cifar10 \
                    --val-indices "data/e2_val_${cond}.json" \
                    --test-eval \
                    --out "results/q1/e2/select_${arch}_s${seed}_val${cond}.json"
        done
    done
    # Tuzak isareti: AT'nin CANLI best.pth'i V_A+V_B+V_C (6000) uzerinde
    # secilmistir - UCUNCU bir kuraldir ve E2 analizinde YERI YOKTUR
    mkdir -p models/q1/e2
    printf '%s\n' \
        "E2 adv/*/best.pth DOSYALARINI KULLANMA: canli egitim secimi V_A+V_B+V_C (6000) uzerinde yapilmistir." \
        "Gecerli E2 secimleri: results/q1/e2/select_*.json (+ _test.npz) ve epochs/epoch_XXX.pth dizileri." \
        > models/q1/e2/BEST_PTH_KULLANMA.txt
    ;;
# ---------------------------------------------------------------------------
e5pilot)  # R50 + ViT-S, 1 tohum: SURE OLCUMU (rapor: +-40% belirsizlik, pilot sart)
    run_step Q1_val_split_c10 data/val_split_indices.json \
        python experiments/rev2/make_val_split.py --dataset cifar10
    train_pair_member cifar10 resnet50 3001 data/val_split_indices.json 2
    train_pair_member cifar10 vit_small 4001 data/val_split_indices.json 2
    log "PILOT TAMAM - logs/Q1_cifar10_*_3001.log ve *_4001.log surelerini incele,"
    log "ViT-S ilk-5-epoch adv-acc kontrolu: <%15 ise LR 2.5e-4'e dusur (rapor 5.3)"
    ;;
e5)  # kalan tohumlar (pilot onaylandiktan sonra)
    # On kosullar (review bulgusu): val split + pilot ciktilarinin varligi.
    # train_pair_member idempotent oldugundan pilot tohumlarini da cagirmak
    # bedava (TRAINING_COMPLETE varsa SKIP) ve pilot silinmisse kendini onarir.
    run_step Q1_val_split_c10 data/val_split_indices.json \
        python experiments/rev2/make_val_split.py --dataset cifar10
    train_pair_member cifar10 resnet50 3001 data/val_split_indices.json 2
    train_pair_member cifar10 vit_small 4001 data/val_split_indices.json 2
    for seed in 3002 3003; do
        train_pair_member cifar10 resnet50 "$seed" data/val_split_indices.json 2
    done
    for seed in 4002 4003; do
        train_pair_member cifar10 vit_small "$seed" data/val_split_indices.json 2
    done
    for i in 1 2 3; do
        rs=$((3000 + i)); vs=$((4000 + i))
        run_step "Q1_e5_aa_pair${i}" "results/q1/cifar10_e5/pair${i}/autoattack_summary.json" \
            python experiments/run_autoattack_run2.py --n-samples 10000 --seed 42 \
                --dataset cifar10 \
                --model "ResNet50_AT:resnet50:models/q1/cifar10/resnet50_s${rs}/resnet50/adv/adversarial_training/best.pth" \
                --model "ViT_Small_AT:vit_small:models/q1/cifar10/vit_small_s${vs}/vit_small/adv/adversarial_training/best.pth" \
                --output-dir "results/q1/cifar10_e5/pair${i}"
    done
    ;;
# ---------------------------------------------------------------------------
e7)  # SVHN capasi: flip zaten kapali (DATASETS), eps-warmup + LR 0.001 (rapor E7)
    # K-01 karari (KAMPANYA_KARARLARI.md): VARSAYILAN KISA SURUM.
    #   kisa: 2 tohum x 50 epok  ~11 GPU-saat  <- onaylanan
    #   tam : 3 tohum x 100 epok ~33-36 GPU-saat, BILINCLI olarak E7_FULL=1 ister
    # Varsayilan kisa tutuluyor ki kaza eseri butcenin 3 kati harcanmasin.
    if [ "${E7_FULL:-0}" = "1" ]; then
        E7_RN_SEEDS="1001 1002 1003"; E7_VIT_SEEDS="2001 2002 2003"; E7_EPOCHS=100
        log "E7: TAM surum (E7_FULL=1) -- 3 tohum x 100 epok"
    else
        E7_RN_SEEDS="1001 1002"; E7_VIT_SEEDS="2001 2002"; E7_EPOCHS=50
        log "E7: KISA surum (varsayilan, K-01) -- 2 tohum x 50 epok; tam surum icin E7_FULL=1"
    fi
    # SVHN val bolmesi BILEREK --stratified DEGIL: esit-sinif bolmesi dengesiz
    # SVHN'de val kumesini dengeli yapar, test dengesiz kalir -> secim olcutu ile
    # raporlama olcutu uyusmaz. Ayrinti: E7_KOSUM_ONCESI_KONTROL.md §3.
    run_step Q1_val_split_svhn data/val_split_indices_svhn.json \
        python experiments/rev2/make_val_split.py --dataset svhn
    for seed in $E7_RN_SEEDS; do
        root="models/q1/svhn/resnet18_s${seed}"
        run_train "Q1_svhn_clean_resnet18_${seed}" "${root}/resnet18/clean" \
            python -m cli.main train clean -m resnet18 --dataset svhn \
                $(clean_args resnet18) --seed "$seed" -o "$root" \
                --val-indices data/val_split_indices_svhn.json
        run_train "Q1_svhn_at_resnet18_${seed}" "${root}/resnet18/adv/adversarial_training" \
            python -m cli.main train adversarial -m resnet18 --dataset svhn \
                --device cuda --lr 0.001 --epochs "$E7_EPOCHS" --batch-size 128 --patience 20 \
                --eps-warmup 10 --seed "$seed" -o "$root" \
                --pretrained "${root}/resnet18/clean/best.pth" \
                --val-indices data/val_split_indices_svhn.json --save-every 2 \
                --eps $EPS8
        run_step "Q1_svhn_pgd_resnet18_${seed}" \
            "results/q1/svhn/resnet18_s${seed}/pgd_summary_resnet18.json" \
            python scripts/c1_pgd_eval.py --model-type resnet18 --dataset svhn \
                --ckpt "${root}/resnet18/adv/adversarial_training/best.pth" \
                --out "results/q1/svhn/resnet18_s${seed}"
    done
    for seed in $E7_VIT_SEEDS; do
        root="models/q1/svhn/vit_tiny_s${seed}"
        run_train "Q1_svhn_clean_vit_tiny_${seed}" "${root}/vit_tiny/clean" \
            python -m cli.main train clean -m vit_tiny --dataset svhn \
                $(clean_args vit_tiny) --seed "$seed" -o "$root" \
                --val-indices data/val_split_indices_svhn.json
        run_train "Q1_svhn_at_vit_tiny_${seed}" "${root}/vit_tiny/adv/adversarial_training" \
            python -m cli.main train adversarial -m vit_tiny --dataset svhn \
                --device cuda --lr 0.001 --epochs "$E7_EPOCHS" --batch-size 64 --patience 20 \
                --eps-warmup 10 --seed "$seed" -o "$root" \
                --pretrained "${root}/vit_tiny/clean/best.pth" \
                --val-indices data/val_split_indices_svhn.json --save-every 2 \
                --eps $EPS8
        run_step "Q1_svhn_pgd_vit_tiny_${seed}" \
            "results/q1/svhn/vit_tiny_s${seed}/pgd_summary_vit_tiny.json" \
            python scripts/c1_pgd_eval.py --model-type vit_tiny --dataset svhn \
                --ckpt "${root}/vit_tiny/adv/adversarial_training/best.pth" \
                --out "results/q1/svhn/vit_tiny_s${seed}"
    done
    ;;
*)
    log "Bilinmeyen STAGE: $STAGE"; exit 1 ;;
esac

log "=============== Q1-${STAGE^^} TAMAM ==============="
