#!/bin/bash

SESSION="advlab"
BASE_DIR="$HOME/advlab"
MODELS_DIR="$BASE_DIR/models"
LOG_DIR="$BASE_DIR/logs"
CHECKPOINT_FILE="$BASE_DIR/.workflow_checkpoint"

# Log dizini oluştur
mkdir -p $LOG_DIR

# Checkpoint kontrolü
function check_checkpoint() {
  if [ -f "$CHECKPOINT_FILE" ]; then
    LAST_STEP=$(cat $CHECKPOINT_FILE)
    if [[ $LAST_STEP -ge $1 ]]; then
      return 0 # checkpoint var, adım tamamlanmış
    fi
  fi
  return 1 # checkpoint yok veya adım tamamlanmamış
}

# Checkpoint güncelleme
function update_checkpoint() {
  echo $1 > $CHECKPOINT_FILE
}

# Modelin var olduğunu kontrol et
function check_model() {
  if [ -f "$1" ]; then
    return 0 # model var
  else
    return 1 # model yok
  fi
}

# Tmux oturumu oluştur veya varsa bağlan
tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then
  tmux new-session -d -s $SESSION
else
  echo "Mevcut oturum bulundu. Yeni pencereler açılacak."
fi

# 1. Veri seti hazırla
if ! check_checkpoint 1; then
  echo "Adım 1: Veri seti hazırlanıyor..."
  tmux new-window -t $SESSION:0 -n "dataset"
  tmux send-keys -t $SESSION:0 "cd $BASE_DIR && conda activate advlab && python scripts/00_prepare_dataset.py | tee $LOG_DIR/00_dataset.log && echo 'Veri seti hazırlandı!' && echo '1' > $CHECKPOINT_FILE" C-m
fi

# 2-3. ResNet ve ViT temiz eğitim (paralel)
if ! check_checkpoint 2; then
  echo "Adım 2-3: ResNet ve ViT temiz eğitim başlatılıyor..."
  
  # ResNet temiz eğitim
  tmux new-window -t $SESSION:1 -n "resnet_clean"
  tmux send-keys -t $SESSION:1 "cd $BASE_DIR && conda activate advlab && python scripts/01_train_resnet_clean.py | tee $LOG_DIR/01_resnet_clean.log && echo 'ResNet temiz eğitim tamamlandı!'" C-m
  
  # ViT temiz eğitim
  tmux new-window -t $SESSION:2 -n "vit_clean"
  tmux send-keys -t $SESSION:2 "cd $BASE_DIR && conda activate advlab && python scripts/02_train_vit_clean.py | tee $LOG_DIR/02_vit_clean.log && echo 'ViT temiz eğitim tamamlandı!'" C-m
  
  # Monitör ekranı
  tmux new-window -t $SESSION:3 -n "monitor"
  tmux send-keys -t $SESSION:3 "watch -n 2 'nvidia-smi | grep -E \"Processes:|Default|MiB|%\"'" C-m
  
  # Bekleme ve kontrol penceresi
  tmux new-window -t $SESSION:4 -n "control"
  tmux send-keys -t $SESSION:4 "cd $BASE_DIR && conda activate advlab && echo 'Temiz modellerin eğitimi tamamlandığında aşağıdaki komutu girin:' && echo 'echo 2 > $CHECKPOINT_FILE'" C-m
fi

# 4-5. Adversarial eğitim (temiz modeller hazır olduğunda)
if check_checkpoint 2 && ! check_checkpoint 3; then
  RESNET_MODEL="$MODELS_DIR/resnet/clean/resnet18_cifar10.pth"
  VIT_MODEL="$MODELS_DIR/vit/clean/vit_tiny_cifar10.pth"
  
  if check_model "$RESNET_MODEL" && check_model "$VIT_MODEL"; then
    echo "Adım 4-5: Adversarial eğitim başlatılıyor..."
    
    # ResNet adversarial eğitim
    tmux new-window -t $SESSION:5 -n "resnet_adv"
    tmux send-keys -t $SESSION:5 "cd $BASE_DIR && conda activate advlab && python scripts/03_train_resnet_adv.py | tee $LOG_DIR/03_resnet_adv.log && echo 'ResNet adversarial eğitim tamamlandı!'" C-m
    
    # ViT adversarial eğitim
    tmux new-window -t $SESSION:6 -n "vit_adv"
    tmux send-keys -t $SESSION:6 "cd $BASE_DIR && conda activate advlab && python scripts/04_train_vit_adv.py | tee $LOG_DIR/04_vit_adv.log && echo 'ViT adversarial eğitim tamamlandı!'" C-m
    
    # Bekleme ve kontrol penceresi
    tmux new-window -t $SESSION:7 -n "control_adv"
    tmux send-keys -t $SESSION:7 "cd $BASE_DIR && conda activate advlab && echo 'Adversarial modellerin eğitimi tamamlandığında aşağıdaki komutu girin:' && echo 'echo 3 > $CHECKPOINT_FILE'" C-m
  else
    echo "HATA: Temiz eğitilmiş modeller bulunamadı! Lütfen önce temiz modelleri eğitin."
    tmux new-window -t $SESSION:5 -n "error"
    tmux send-keys -t $SESSION:5 "echo 'HATA: Temiz eğitilmiş modeller bulunamadı! Lütfen önce temiz modelleri eğitin.'" C-m
  fi
fi

# 6-9. Değerlendirme scriptleri (adversarial modeller hazır olduğunda)
if check_checkpoint 3 && ! check_checkpoint 4; then
  echo "Adım 6-9: Değerlendirme scriptleri başlatılıyor..."
  
  # Saldırı değerlendirmeleri
  tmux new-window -t $SESSION:8 -n "attack_eval"
  tmux send-keys -t $SESSION:8 "cd $BASE_DIR && conda activate advlab && \
    echo 'ResNet temiz model değerlendirmesi' && \
    python scripts/05_attack_evaluation.py --model resnet --training clean | tee $LOG_DIR/05_resnet_clean_eval.log && \
    echo 'ResNet adversarial model değerlendirmesi' && \
    python scripts/05_attack_evaluation.py --model resnet --training adv | tee $LOG_DIR/05_resnet_adv_eval.log && \
    echo 'ViT temiz model değerlendirmesi' && \
    python scripts/05_attack_evaluation.py --model vit --training clean | tee $LOG_DIR/05_vit_clean_eval.log && \
    echo 'ViT adversarial model değerlendirmesi' && \
    python scripts/05_attack_evaluation.py --model vit --training adv | tee $LOG_DIR/05_vit_adv_eval.log && \
    echo 'Saldırı değerlendirmeleri tamamlandı!'" C-m
  
  # AutoAttack değerlendirmeleri
  tmux new-window -t $SESSION:9 -n "autoattack"
  tmux send-keys -t $SESSION:9 "cd $BASE_DIR && conda activate advlab && \
    echo 'ResNet temiz model AutoAttack' && \
    python scripts/06_autoattack_evaluation.py --model resnet --training clean | tee $LOG_DIR/06_resnet_clean_autoattack.log && \
    echo 'ResNet adversarial model AutoAttack' && \
    python scripts/06_autoattack_evaluation.py --model resnet --training adv | tee $LOG_DIR/06_resnet_adv_autoattack.log && \
    echo 'AutoAttack değerlendirmeleri tamamlandı!'" C-m
  
  # Test-Time Augmentation savunması
  tmux new-window -t $SESSION:10 -n "tta"
  tmux send-keys -t $SESSION:10 "cd $BASE_DIR && conda activate advlab && \
    echo 'ResNet TTA savunması' && \
    python scripts/07_test_time_augmentation.py --model resnet --training clean | tee $LOG_DIR/07_resnet_clean_tta.log && \
    python scripts/07_test_time_augmentation.py --model resnet --training adv | tee $LOG_DIR/07_resnet_adv_tta.log && \
    echo 'ViT TTA savunması' && \
    python scripts/07_test_time_augmentation.py --model vit --training clean | tee $LOG_DIR/07_vit_clean_tta.log && \
    python scripts/07_test_time_augmentation.py --model vit --training adv | tee $LOG_DIR/07_vit_adv_tta.log && \
    echo 'TTA savunma değerlendirmeleri tamamlandı!' && echo '4' > $CHECKPOINT_FILE" C-m
fi

# 10. Sonuçları analiz et
if check_checkpoint 4 && ! check_checkpoint 5; then
  echo "Adım 10: Sonuçlar analiz ediliyor..."
  tmux new-window -t $SESSION:11 -n "analysis"
  tmux send-keys -t $SESSION:11 "cd $BASE_DIR && conda activate advlab && python scripts/08_analyze_results.py | tee $LOG_DIR/08_results_analysis.log && echo 'Sonuç analizi tamamlandı!' && echo '5' > $CHECKPOINT_FILE" C-m
fi

# Bash penceresi
tmux new-window -t $SESSION:12 -n "bash"
tmux send-keys -t $SESSION:12 "cd $BASE_DIR && conda activate advlab && echo 'İnteraktif terminal - manuel komut çalıştırmak için kullanın'" C-m

# Tmux oturumuna bağlan
tmux select-window -t $SESSION:0
tmux attach-session -t $SESSION
