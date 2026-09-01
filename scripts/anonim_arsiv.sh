#!/usr/bin/env bash
# HAKEM ICIN ANONIM ARSIV
#
# Makalenin tezi "protokolu belirtin"dir; hakem dort protokolu KENDISI
# hesaplayabilmelidir. Bu paket bunu model agirliklari olmadan mumkun kilar:
# ornek bazindaki kayitlar + analiz betikleri + bolme indeksleri + tohumlar.
#
# ICERMEZ: model agirliklari (~40 GB), yazar adlari, kurum bilgisi.
set -eu
cd /home/firat/projects/adeb_sci_1

TARIH=$(date +%Y%m%d)
SHA=$(git rev-parse --short HEAD)
OUT="teslim/ANONIM_ARSIV_${TARIH}_${SHA}"
rm -rf "$OUT"; mkdir -p "$OUT"

echo "== ornek bazindaki kayitlar =="
mkdir -p "$OUT/results"
for d in c1_seeds c1_transfer c1_gradient c1_c4 c1_c2 c1_addenda q1; do
    [ -d "results/$d" ] && cp -r "results/$d" "$OUT/results/" && echo "  + results/$d"
done
for f in results/C1_REFERANS_FOYU.md results/c1_eval_summary.json \
         results/c1_behavior_summary.json; do
    [ -f "$f" ] && cp "$f" "$OUT/results/"
done

echo "== analiz ve kapi betikleri =="
mkdir -p "$OUT/scripts" "$OUT/src" "$OUT/experiments"
cp -r src/analysis "$OUT/src/" 2>/dev/null || true
cp -r src/attacks "$OUT/src/" 2>/dev/null || true
for f in scripts/verify_manuscript_numbers.py scripts/check_manuscript_claims.py \
         scripts/check_abstract_body.py scripts/check_en_tr_mirror.py \
         scripts/gonderim_tutarlilik.py scripts/build_reference_sheet.py \
         scripts/kapilar.sh scripts/test_cebir_muhafizi.sh; do
    [ -f "$f" ] && cp "$f" "$OUT/scripts/"
done
cp experiments/*.py "$OUT/experiments/" 2>/dev/null || true

echo "== bolme indeksleri ve tohumlar =="
find . -name 'val_split*.npy' -o -name '*split_indices*' 2>/dev/null \
    | head -20 | while IFS= read -r f; do cp "$f" "$OUT/" 2>/dev/null || true; done

cat > "$OUT/README.md" <<'EOF'
# Anonymized artifact archive

This archive accompanies a manuscript under review. It contains everything
needed to recompute every number in the paper **without retraining**:

- `results/` — per-sample evaluation records (clean-correct and
  robust-correct flags for every test image, every model, every seed),
  and the aggregated summaries the tables are built from.
- `src/analysis/protokoller.py` — the single definition of the four
  conditioning protocols. All four are computed from the same per-sample
  records, so the protocol comparison can be reproduced directly.
- `scripts/` — the consistency gates. `bash scripts/kapilar.sh` runs all
  of them; `scripts/verify_manuscript_numbers.py` checks every carrier
  number in the manuscript against the artifacts that produced it.
- `experiments/` — the evaluation and analysis drivers.
- `results/C1_REFERANS_FOYU.md` — the generated reference sheet. Every
  number that leaves this project is taken from here.

**Not included:** trained model checkpoints (about 40 GB). They are not
needed to reproduce the protocol comparison, which is computed entirely
from the logged per-sample outcomes. They are available on request.

**Anonymity:** this archive contains no author names, affiliations or
institutional paths.
EOF

# --- anonimlestirme ---
# .pyc dosyalari derleme yolunu (/home/<kullanici>/...) GOMER; betikler de
# mutlak yol tasiyabilir. Ikisi de kimlik sizdirir.
echo "== anonimlestirme =="
find "$OUT" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name '*.pyc' -delete 2>/dev/null || true
echo "  __pycache__ ve .pyc temizlendi"
find "$OUT" -type f \( -name '*.py' -o -name '*.sh' -o -name '*.md' \) -print0 \
  | xargs -0 sed -i 's|/home/firat/projects/adeb_sci_1|<PROJECT_ROOT>|g' 2>/dev/null || true
echo "  mutlak proje yolu <PROJECT_ROOT> ile degistirildi"

# kimlik sizintisi taramasi
echo "== kimlik taramasi =="
SIZINTI=$(grep -ril 'sahin\|yildirim\|firat\|alparslan\|c\.sahin@' "$OUT" 2>/dev/null | head -20 || true)
if [ -n "$SIZINTI" ]; then
    echo "  UYARI -- kimlik gecen dosyalar:"
    echo "$SIZINTI" | sed 's/^/    /'
else
    echo "  temiz: yazar/kurum adi gecen dosya yok"
fi

BOYUT=$(du -sh "$OUT" | cut -f1)
ADET=$(find "$OUT" -type f | wc -l)
echo
echo "PAKET : $OUT"
echo "BOYUT : $BOYUT"
echo "DOSYA : $ADET"
