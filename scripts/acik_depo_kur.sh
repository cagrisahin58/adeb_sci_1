#!/usr/bin/env bash
# ACIK DEPO KURUCU (2026-10-02)
#
# Makale gonderimi icin HERKESE ACIK, derlenmis bir depo uretir:
#   teslim/acik_depo/cnn-vit-robustness-protocols/   (git init + tek commit)
#
# Kapsam, makaledeki "Data and Code Availability" vaadiyle birebir:
#   analiz hatti + tablo/sekil betikleri + ornek bazinda kayitlar
#   + sabit dogrulama bolmesi indeksleri + tohumlar (README'de).
# ICERMEZ: model agirliklari (~40 GB), arsivlenmis cekismeli ornekler
#   (results/q1/adv_archive, 434 MB, E3 ara urunu), '_' ile baslayan ic
#   sinamalar, Turkce ic raporlar (.md), el yazmasi kaynaklari.
#
# Karar kaydi: kullanici 2026-10-02 -- adeb_sci_1 kapali kalir, yeni depo
# acilir; gecmis yeniden yazimi gerekmez (tek commit, imza yok).
set -eu
cd /home/firat/projects/adeb_sci_1

AD=cnn-vit-robustness-protocols
OUT="teslim/acik_depo/$AD"
SHA=$(git rev-parse --short HEAD)
rm -rf "$OUT"; mkdir -p "$OUT"

echo "== ornek bazindaki kayitlar =="
mkdir -p "$OUT/results/q1"
for d in c1_seeds c1_transfer c1_gradient c1_c2 c1_c3 c1_c4 c1_c5 c1_a3 c1_a5 \
         c1_addenda c1_drift c1_eval c1_eval_clean c1_statval c1_sweep; do
    [ -d "results/$d" ] && cp -r "results/$d" "$OUT/results/" && echo "  + results/$d"
done
for f in results/C1_REFERANS_FOYU.md results/c1_eval_summary.json \
         results/c1_behavior_summary.json results/c1_c45_summary.json; do
    [ -f "$f" ] && cp "$f" "$OUT/results/"
done
for p in results/q1/*; do
    b=$(basename "$p")
    case "$b" in adv_archive|_*) echo "  - results/q1/$b (haric)"; continue;; esac
    cp -r "$p" "$OUT/results/q1/"
done
# Turkce ic raporlar (C*_RAPORU.md, E*_RAPORU.md ...) disarida; yalniz referans foyu kalir.
find "$OUT/results" -name '*.md' ! -name 'C1_REFERANS_FOYU.md' -print -delete | sed 's/^/  - ic rapor silindi: /'

echo "== kod =="
mkdir -p "$OUT/scripts" "$OUT/experiments" "$OUT/data" "$OUT/configs" "$OUT/paper/figures/final"
cp -r src "$OUT/src"
[ -d cli ] && cp -r cli "$OUT/cli"
for f in scripts/build_reference_sheet.py scripts/generate_journal_figs_c1.py \
         scripts/fig_protokol_kumeleri_veri.py scripts/q1_e3_figur.py \
         scripts/verify_manuscript_numbers.py scripts/check_manuscript_claims.py; do
    [ -f "$f" ] && cp "$f" "$OUT/scripts/"
done
cp experiments/*.py "$OUT/experiments/"
cp paper/figures/fig_protocol_sets.py "$OUT/paper/figures/"
cp data/val_split_indices*.json "$OUT/data/"
# configs: root:root sahipli, okunamayan dosyalar (ornegin cifar10_trades_v3.yaml,
# makalede kullanilmayan TRADES denemesi) atlanir ve adlari yazilir.
( cd configs && find . -type f -readable -exec cp --parents {} "../$OUT/configs/" \; )
find configs -type f ! -readable | sed 's/^/  - okunamadi, atlandi: /'
cp requirements.txt "$OUT/requirements.txt"
touch "$OUT/paper/figures/final/.gitkeep"

# Referans foyu kurucusu depo kokunu betigin konumundan bulsun
# (orijinal: /workspace ya da ~/projects/adeb_sci_1).
sed -i 's|^ROOT = .*|ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))|' \
    "$OUT/scripts/build_reference_sheet.py"
grep -n '^ROOT = ' "$OUT/scripts/build_reference_sheet.py"
# Ayni sey Path tabanli dort betik icin: /workspace ya da ~/projects/adeb_sci_1 yerine depo koku.
for f in fig_protokol_kumeleri_veri.py q1_e3_figur.py verify_manuscript_numbers.py generate_journal_figs_c1.py; do
    sed -i -E 's|^ROOT = Path\("/workspace"\) if Path\("/workspace/results"\)\.is_dir\(\) else Path\.home\(\) / "projects/adeb_sci_1"$|ROOT = Path(__file__).resolve().parents[1]|' "$OUT/scripts/$f"
    grep -n '^ROOT = ' "$OUT/scripts/$f"
done

find "$OUT" -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$OUT" -name '*.pyc' -delete 2>/dev/null || true

echo "== README / LICENSE / CITATION =="
cat > "$OUT/README.md" <<'EOF'
# cnn-vit-robustness-protocols

Code, per-sample evaluation records and verification scripts for

> C. Sahin and O. Yildirim, "The Measurement Protocol Decides the Conclusion:
> A Methodological Study of CNN and Vision Transformer Adversarial Robustness
> Comparisons", submitted to IEEE Access, 2026.

The paper's claim is that the conditioning protocol used to score transfer
attacks moves the measured CNN-to-ViT asymmetry by more than retraining
does. Everything needed to recompute that comparison is here, and none of it
needs a GPU or a trained checkpoint: the four protocols are computed from the
same per-sample outcome records.

## Layout

| Path | Content |
|---|---|
| `results/c1_*` | CIFAR-10 campaign: per-sample clean/robust flags for every test image, model and seed; transfer, gradient, attention and depth-profile records; aggregated summaries |
| `results/q1/` | CIFAR-100 and SVHN replications, the L2 check, the checkpoint-selection ablation and the pre-registered pool fits |
| `results/C1_REFERANS_FOYU.md` | Generated reference sheet. Every number in the paper is taken from this file |
| `src/analysis/protokoller.py` | The single definition of the four conditioning protocols (raw, target-correct, both-correct, successful-source) |
| `scripts/build_reference_sheet.py` | Regenerates the reference sheet from the records |
| `scripts/generate_journal_figs_c1.py`, `paper/figures/fig_protocol_sets.py`, `scripts/fig_protokol_kumeleri_veri.py` | Figure generators |
| `experiments/` | Evaluation and analysis drivers (these need the checkpoints) |
| `src/`, `cli/`, `configs/` | Training, attack and evaluation code |
| `data/val_split_indices*.json` | The fixed validation split (seed 777), excluded from every training stage |

Seeds: ResNet-18 runs 1001, 1002, 1003; ViT-Tiny runs 2001, 2002, 2003;
validation split 777; AutoAttack and analysis sampling 42.

The reference sheet and some record keys are labelled in Turkish. Key terms:
`temiz` clean, `gurbuz` robust, `ham` raw (unconditioned), `hedef dogru`
target-correct, `her ikisi dogru` both-correct, `basarili kaynak`
successful-source, `kosum` training run, `cift` run pair, `tohum` seed,
`yayilim` spread, `ozdeslik` identity, `secim` checkpoint selection.

## Reproduce the numbers

```bash
pip install -r requirements.txt    # numpy, scipy, pandas and matplotlib suffice for the analysis
python scripts/build_reference_sheet.py
git status --short results/C1_REFERANS_FOYU.md   # no change expected
```

`scripts/verify_manuscript_numbers.py` and `scripts/check_manuscript_claims.py`
check every carrier number and claim in the manuscript against these
records. They expect the manuscript sources under `paper/manuscript/`, which
are not part of this repository; they are included so that the checks can be
rerun once the paper is published.

## Not included

Trained checkpoints (about 40 GB) and the archived adversarial examples used
by the calibration runs (434 MB). Both are available from the authors on
request; neither is needed for the protocol comparison.

## License

Code is released under the MIT License (see `LICENSE`). The evaluation
records and the generated reference sheet are released under CC BY 4.0.

## Citation

See `CITATION.cff`.
EOF

cat > "$OUT/LICENSE" <<'EOF'
MIT License

Copyright (c) 2026 Cagri Sahin, Ozal Yildirim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

cat > "$OUT/CITATION.cff" <<'EOF'
cff-version: 1.2.0
message: "If you use this code or these records, please cite the paper below."
title: "cnn-vit-robustness-protocols"
authors:
  - family-names: Sahin
    given-names: Cagri
    affiliation: "Mus Alparslan University"
  - family-names: Yildirim
    given-names: Ozal
    affiliation: "Firat University"
year: 2026
repository-code: "https://github.com/cagrisahin58/cnn-vit-robustness-protocols"
license: MIT
preferred-citation:
  type: unpublished
  title: "The Measurement Protocol Decides the Conclusion: A Methodological Study of CNN and Vision Transformer Adversarial Robustness Comparisons"
  authors:
    - family-names: Sahin
      given-names: Cagri
    - family-names: Yildirim
      given-names: Ozal
  year: 2026
  notes: "Submitted to IEEE Access."
EOF

cat > "$OUT/.gitignore" <<'EOF'
__pycache__/
*.pyc
.DS_Store
paper/figures/final/*.png
paper/figures/final/*.pdf
EOF

echo "== kalan mutlak yol / makine yolu =="
grep -rn -E '/home/firat|/workspace|adeb_sci_1' "$OUT" --include='*.py' --include='*.sh' --include='*.yaml' \
    | cut -c1-160 | head -20 || true

echo "== git =="
GN=$(git config user.name); GE=$(git config user.email)
cd "$OUT"
git init -q -b main
git config user.name "$GN"; git config user.email "$GE"
git add -A
git -c commit.gpgsign=false commit -q \
    -m "Initial release: analysis pipeline, per-sample records and verification scripts" \
    -m "Accompanies the manuscript 'The Measurement Protocol Decides the Conclusion' (IEEE Access submission). Snapshot of the private working repository at revision $SHA."
git log --format='%h %an <%ae> %s' -1
git log --format=%B -1 | grep -c 'Co-Authored' || true
cd - > /dev/null

BOYUT=$(du -sh "$OUT" | cut -f1)
ADET=$(find "$OUT" -type f -not -path '*/.git/*' | wc -l)
echo
echo "DEPO  : $OUT"
echo "BOYUT : $BOYUT"
echo "DOSYA : $ADET"
echo "ITMEK : cd $OUT && git remote add origin https://github.com/cagrisahin58/$AD.git && git push -u origin main"
