#!/bin/bash
# Celisik dogrulayici, D4: kuyruk kuru kosusu + --help ciktilari + bayrak ayristirma.
set -uo pipefail
cd /workspace
D=results/q1/konsey_smoke/_dogrulayici
bash scripts/konsey_b3_kuyruk.sh --dry-run --pilot results/q1/konsey_pilot_zaman.json > "$D/d4_kuyruk_dry_run.txt" 2>&1
echo "kuru kosu rc=$?"
ls results/q1/konsey_b3_defter.tsv 2>/dev/null && echo "UYARI: kuru kosu defter olusturdu" || echo "defter yok (beklenen)"
python -m cli.main train clean --help > "$D/d4_help_clean.txt" 2>&1
python -m cli.main train adversarial --help > "$D/d4_help_adversarial.txt" 2>&1
python scripts/konsey_b3_denetim.py tavan --pilot results/q1/konsey_pilot_zaman.json
python "$D/d4_bayraklar.py" "$D/d4_kuyruk_dry_run.txt" "$D/d4_bayraklar.json"
