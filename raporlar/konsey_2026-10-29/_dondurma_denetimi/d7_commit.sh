#!/bin/bash
cd /home/firat/projects/adeb_sci_1 || exit 1
K=raporlar/konsey_2026-10-29/_commit1_kuru.txt
echo "=== WSL git status (izlenen, degismis) ==="
git status --porcelain --untracked-files=no
echo "=== WSL git: core.autocrlf / hooks / template ==="
git config --get core.autocrlf; git config --get commit.template; ls .git/hooks | grep -v sample
echo "=== .gitattributes ==="
cat .gitattributes 2>/dev/null | head -20
echo "=== git diff HEAD --stat (aday izlenen dosyalar) ==="
git diff HEAD --stat -- src/models/__init__.py src/training/trainer.py src/training/adversarial_trainer.py cli/train.py experiments/c1_c3_transfer_matrix.py results/q1_research/DEVAM_TALIMATI.md
echo "=== kuru cikti ozet satirlari ==="
grep -n '^===\|^ayrisim\|^hucre\|^govde\|^ozetler\|^HEAD\|UYARI' "$K"
echo "=== kuru ciktida yasakli desenler ==="
grep -E "^add '" "$K" | grep -E "models/|logs/|\.pt'|\.pth'|\.safetensors'|\.npy'|paper/|configs/|onbellek|\.pyc'|eski_kod|DOCKER|PROJE_RAPORU|YOL_HARITASI|auto_train|tmux_train|train_robust|test_normalization" | head -40
echo "=== kuru ciktida add satiri sayisi ==="
grep -c "^add '" "$K"
echo "=== kuru ciktida klasor dagilimi ==="
grep "^add '" "$K" | sed "s/^add '//; s/'$//" | awk -F/ '{ if ($1=="results") print $1"/"$2"/"$3; else print $1"/"$2 }' | sort | uniq -c | sort -rn | head -30
echo "=== zorunlu dosyalar kuru listede mi ==="
for f in raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md raporlar/konsey_2026-10-29/KONSEY_PLANI.md raporlar/konsey_2026-10-29/04_masa_cozumlemeleri.md raporlar/konsey_2026-10-29/05_kod_raporu.md raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md src/models/r224.py src/models/__init__.py cli/train.py src/training/trainer.py src/training/adversarial_trainer.py experiments/c1_c3_transfer_matrix.py scripts/konsey_b3_kuyruk.sh scripts/konsey_b3_denetim.py scripts/konsey_b6_maskeleme.py results/q1/konsey_pilot_zaman.json results/q1/konsey_sahte_2x2_sinama.json results/q1/konsey_sentez_r_tau_masa.json results/q1/konsey_masa/konsey_masa_cozumlemeleri.json results/q1/konsey_masa/konsey_ayrisim_masa.json results/q1/konsey_masa/_dogrulayici/delta_kaynagi.json results/q1/_konsey_sahte/sahte_b2_kc3.json results/q1/_konsey_sahte/kc3_sinama.py results/q1/konsey_smoke/_dogrulayici/d5_temiz_referans.json results/q1/konsey_smoke/matris_panel/transfer_matrix.json results/q1/konsey_smoke/matris_panel.log results/q1/etkilesim_simetri_masa.json results/q1_research/DEVAM_TALIMATI.md arsiv/b2_yardimci/_konsey_commit1.sh data/val_split_indices.json; do
  if grep -qxF "add '$f'" "$K"; then echo "LISTEDE  $f"; else
    if git ls-files --error-unmatch "$f" >/dev/null 2>&1 && git diff HEAD --quiet -- "$f"; then echo "HEAD'DE (degismemis) $f"; else echo "YOK!!    $f"; fi
  fi
done
echo "=== scripts/konsey_* ve src/attacks degisiklikleri ==="
ls scripts/konsey_*
git status --porcelain -- src experiments scripts cli | head -40
echo "=== en buyuk 8 dosya (kuru liste) ==="
grep "^add '" "$K" | sed "s/^add '//; s/'$//" | tr '\n' '\0' | du -b --files0-from=- 2>/dev/null | sort -n | tail -8
echo "=== kuru ciktidan sonra degisen/eklenen aday dosyalar (mtime > kuru) ==="
find raporlar/konsey_2026-10-29 results/q1/konsey_smoke results/q1/konsey_masa results/q1/_konsey_sahte experiments scripts src cli -newer "$K" -type f 2>/dev/null | grep -v __pycache__ | head -40
echo "=== 23.75 / 26.55 / 25.35 depo icinde (results/q1) ==="
grep -rl "23.75\|26.55" results/q1/konsey_smoke results/q1/konsey_masa 2>/dev/null | head
echo "=== C1 ViT temiz log Epoch 1 ==="
for s in 2001 2002 2003; do grep -m1 "Epoch 1/200" -A6 logs/C1_clean_vit_$s.log 2>/dev/null | grep -i -m2 "val\|acc" ; echo "-- $s"; done
echo "=== data/val_split_indices.json izleniyor mu ==="
git ls-files data/val_split_indices.json
