#!/usr/bin/env bash
# ACIK DEPO KURUCU (2026-10-02; 2026-10-31 yeni baslik ve on kayit dosyalari)
#
# Makale gonderimi icin HERKESE ACIK, derlenmis bir depo uretir:
#   teslim/acik_depo/cnn-vit-robustness-protocols/   (git init + tek commit)
#
# KULLANIM
#   bash scripts/acik_depo_kur.sh --dry-run    # hicbir sey yazmaz; ne kopyalanacagini
#                                              # boyutlariyla listeler
#   bash scripts/acik_depo_kur.sh              # depoyu kurar ve YEREL tek commit atar
#   bash scripts/acik_depo_kur.sh --with-npz   # konsey kayit dizinlerini ornek bazli
#                                              # npz dosyalariyla birlikte ekler (~60 MB)
#
# BU BETIK HICBIR ZAMAN PUSH ETMEZ. GitHub'da depoyu acmak ve itmek kullanicinin
# isidir; komutlar betigin sonunda yorum ve ekran ciktisi olarak verilir.
#
# 2026-10-31 DEGISIKLIGI (celisik dogrulayici bulgusu 1): makalede ve gonderim
# belgelerinde verilen adres 404 donuyordu; yerel kopya 4 Ekim tarihli tek commit
# idi, README ve CITATION.cff eski basligi tasiyordu, on kayit belgeleri ve
# dondurulmus cozumleme betigi yoktu. Bu surum:
#   - yeni basligi README, CITATION.cff ve commit mesajina yazar,
#   - on kayit belgelerini, sapma kaydini, hucre tablolarini, dondurulmus betigi,
#     ek betikleri ve konsey cikti JSON'larini OZGUN YOLLARIYLA kopyalar (foy
#     kurucusu ve SHA-256 kayitlari bu yollari kullanir),
#   - bu dosyalarin tam dosya SHA-256 ozetlerini REGISTRATION_SHA256SUMS.txt'e yazar,
#   - konsey_adv_onbellek (2,3 GB cekismeli ornek onbellegi), konsey_smoke,
#     ek_loglar ve ek_regresyon dizinlerini disarida birakir (eski genel dongu
#     results/q1/* altindaki her seyi kopyaliyordu),
#   - --dry-run ile yalniz listeler.
#
# Kapsam, makaledeki "Data and Code Availability" vaadiyle birebir:
#   analiz hatti + tablo/sekil betikleri + ornek bazinda kayitlar
#   + sabit dogrulama bolmesi indeksleri + tohumlar (README'de)
#   + on kayit belgeleri, dondurulmus betik, hucre tablolari.
# ICERMEZ: model agirliklari (~40 GB), arsivlenmis cekismeli ornekler
#   (results/q1/adv_archive, konsey_adv_onbellek), '_' ile baslayan ic sinamalar,
#   Turkce ic raporlar (.md; on kayit belgeleri ve sapma kaydi HARIC), el yazmasi
#   kaynaklari.
#
# Karar kaydi: kullanici 2026-10-02 -- adeb_sci_1 kapali kalir, yeni depo
# acilir; gecmis yeniden yazimi gerekmez (tek commit, imza yok).
set -eu
cd /home/firat/projects/adeb_sci_1

KURU=0
NPZ=0
for a in "$@"; do
    case "$a" in
        --dry-run) KURU=1 ;;
        --with-npz) NPZ=1 ;;
        -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
        *) echo "bilinmeyen secenek: $a (gecerli: --dry-run, --with-npz)"; exit 2 ;;
    esac
done

AD=cnn-vit-robustness-protocols
OUT="teslim/acik_depo/$AD"
SHA=$(git rev-parse --short HEAD)
BASLIK="Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial Transfer under an Architecture-by-Initialization Design"
EKSIK=0
TOPLAM=0
ADET=0
ONKAYIT_LISTESI=()

if [ "$KURU" = 1 ]; then
    echo "KURU KOSU: hicbir dosya yazilmaz, $OUT silinmez. Kaynak revizyon: $SHA"
else
    rm -rf "$OUT"; mkdir -p "$OUT"
fi

# kopyala KAYNAK HEDEF_DIZIN : KAYNAK'i depoda HEDEF_DIZIN altina kopyalar.
kopyala() {
    local src="$1" hedef="$2" b
    if [ ! -e "$src" ]; then
        echo "  ! YOK: $src"; EKSIK=$((EKSIK + 1)); return 0
    fi
    b=$(du -sb "$src" | cut -f1)
    TOPLAM=$((TOPLAM + b)); ADET=$((ADET + 1))
    if [ "$KURU" = 1 ]; then
        printf '  + %-72s -> %-28s %s\n' "$src" "${hedef:-.}/" "$(du -sh "$src" | cut -f1)"
    else
        mkdir -p "$OUT/$hedef"
        cp -r "$src" "$OUT/$hedef/"
        echo "  + $src"
    fi
}
# yolunu_koru KAYNAK : depoda ayni goreli yola kopyalar.
yolunu_koru() { kopyala "$1" "$(dirname "$1")"; }

echo "== ornek bazindaki kayitlar (C1 kampanyasi) =="
for d in c1_seeds c1_transfer c1_gradient c1_c2 c1_c3 c1_c4 c1_c5 c1_a3 c1_a5 \
         c1_addenda c1_drift c1_eval c1_eval_clean c1_statval c1_sweep; do
    [ -d "results/$d" ] && kopyala "results/$d" results
done
for f in results/C1_REFERANS_FOYU.md results/c1_eval_summary.json \
         results/c1_behavior_summary.json results/c1_c45_summary.json; do
    [ -f "$f" ] && kopyala "$f" results
done
# WRN-28-10 referans degerlendirmesi (epsilon taramasi ve Tablo 1 referans satiri foyde bunu okur)
[ -d results/wrn_eval ] && kopyala results/wrn_eval results

echo "== results/q1 (konsey disi) =="
for p in results/q1/*; do
    b=$(basename "$p")
    case "$b" in
        adv_archive|_*|konsey_*|ek_loglar|ek_regresyon)
            echo "  - results/q1/$b (haric)"; continue ;;
    esac
    kopyala "$p" results/q1
done

echo "== on kayit belgeleri, sapma kaydi, hucre tablolari (zorunlu) =="
for f in raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md \
         raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md \
         raporlar/konsey_2026-10-29/hucre_tablosu.json \
         raporlar/konsey_2026-10-29/hucre_tablosu_b8.json \
         raporlar/konsey_2026-10-29/hucre_tablosu_b9.json \
         raporlar/konsey_2026-10-29/hucre_tablosu_a10.json \
         results/q1_research/ONKAYIT_SAPMALAR.md; do
    yolunu_koru "$f"; ONKAYIT_LISTESI+=("$f")
done

echo "== dondurulmus cozumleme betigi, ek betikler, foy kurucusu (zorunlu) =="
for f in experiments/q1_konsey_ayrisim.py experiments/q1_ek_transfer_matrix.py \
         experiments/q1_ek_ayrisim.py experiments/q1_ek_gradyan_kosinus.py \
         experiments/q1_ek_masa.py experiments/c1_c3_transfer_matrix.py \
         tests/test_q1_ek.py scripts/build_reference_sheet.py; do
    yolunu_koru "$f"; ONKAYIT_LISTESI+=("$f")
done

echo "== konsey cikti JSON'lari (zorunlu) =="
KONSEY_JSON=(results/q1/konsey_ayrisim_b2.json results/q1/konsey_ayrisim_b4.json
             results/q1/konsey_ayrisim_b5.json results/q1/konsey_b6_maskeleme.json
             results/q1/konsey_b9_c100/b9_dondurulmus_b2.json
             results/q1/konsey_b9_c100/b9_sarmalayici_b2.json
             results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json
             results/q1/konsey_b8_imagenetv2/b8_betimsel.json
             results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json
             results/q1/konsey_b10_gradyan/b10_aile.json)
KONSEY_JSON+=(results/q1/konsey_b10_gradyan/mantel_*.json)
KONSEY_JSON+=(results/q1/konsey_b10_gradyan/*/kosinus_ozet.json)
KONSEY_JSON+=(results/q1/konsey_ek_masa/*.json)
for f in "${KONSEY_JSON[@]}"; do
    yolunu_koru "$f"; ONKAYIT_LISTESI+=("$f")
done

if [ "$NPZ" = 1 ]; then
    echo "== --with-npz: konsey kayit dizinleri (ornek bazli npz dahil) =="
    for d in konsey_b2_panel konsey_b4_matris konsey_b5_saldiri konsey_b6_aa \
             konsey_masa konsey_b8_imagenetv2 konsey_b9_c100 konsey_b10_gradyan; do
        kopyala "results/q1/$d" results/q1
    done
    for f in results/q1/konsey_b3_defter.tsv results/q1/konsey_sentez_r_tau_masa.json \
             results/q1/konsey_pilot_zaman*.json; do
        yolunu_koru "$f"
    done
    echo "  - results/q1/konsey_adv_onbellek, konsey_smoke, _konsey_sahte (haric)"
else
    echo "== konsey kayit dizinleri ATLANDI (ornek bazli npz; --with-npz ile eklenir) =="
    for d in konsey_b2_panel konsey_b4_matris konsey_b5_saldiri konsey_b6_aa konsey_masa \
             konsey_b8_imagenetv2/matris konsey_b9_c100/matris; do
        [ -e "results/q1/$d" ] && printf '  - results/q1/%-40s %s\n' "$d" "$(du -sh "results/q1/$d" | cut -f1)"
    done
fi

echo "== kod =="
for d in src cli; do [ -d "$d" ] && kopyala "$d" .; done
for f in scripts/generate_journal_figs_c1.py \
         scripts/fig_protokol_kumeleri_veri.py scripts/q1_e3_figur.py \
         scripts/verify_manuscript_numbers.py scripts/check_manuscript_claims.py \
         scripts/fig_yayilim_temiz_fark_veri.py scripts/q1_havuz_analiz_hepsi.sh \
         scripts/dis_veri_mahmood.py scripts/q1_havuz_indir.py \
         scripts/q1_son_kontrol_noktasi_run.sh scripts/q1_temiz_ve_havuz_run.sh; do
    [ -f "$f" ] && kopyala "$f" scripts
done
for f in experiments/*.py; do
    case "$f" in
        experiments/q1_konsey_ayrisim.py|experiments/q1_ek_*.py|experiments/c1_c3_transfer_matrix.py) ;;
        *) kopyala "$f" experiments ;;
    esac
done
kopyala paper/figures/fig_protocol_sets.py paper/figures
kopyala paper/figures/fig_yayilim_temiz_fark.py paper/figures
for f in data/val_split_indices*.json; do kopyala "$f" data; done
kopyala requirements.txt .
if [ "$KURU" = 1 ]; then
    echo "  + configs/ (okunabilen dosyalar; okunamayanlar atlanir)"
    find configs -type f ! -readable | sed 's/^/  - okunamadi, atlanacak: /'
    echo "  - results/q1/dis_veri/mahmood2021.pdf (telif; silinecek)"
    echo "  - results/**/*.md (ic raporlar; C1_REFERANS_FOYU.md ve ONKAYIT_SAPMALAR.md HARIC, silinecek)"
fi

if [ "$KURU" = 0 ]; then
    mkdir -p "$OUT/configs" "$OUT/paper/figures/final"
    # Mahmood ve ark. makalesinin PDF'i (telif) depoya girmez; programla okunmus metin ve JSON'lar girer.
    rm -f "$OUT/results/q1/dis_veri/mahmood2021.pdf"
    # Turkce ic raporlar (C*_RAPORU.md, E*_RAPORU.md ...) disarida; referans foyu ve sapma kaydi kalir.
    find "$OUT/results" -name '*.md' ! -name 'C1_REFERANS_FOYU.md' ! -name 'ONKAYIT_SAPMALAR.md' \
        -print -delete | sed 's/^/  - ic rapor silindi: /'
    # configs: root:root sahipli, okunamayan dosyalar (ornegin cifar10_trades_v3.yaml,
    # makalede kullanilmayan TRADES denemesi) atlanir ve adlari yazilir.
    ( cd configs && find . -type f -readable -exec cp --parents {} "../$OUT/configs/" \; )
    find configs -type f ! -readable | sed 's/^/  - okunamadi, atlandi: /'
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
fi

if [ "$EKSIK" -gt 0 ]; then
    echo
    echo "EKSIK DOSYA: $EKSIK (yukarida '! YOK' satirlari)."
    if [ "$KURU" = 0 ]; then
        echo "Zorunlu dosyalar eksikken depo commit edilmez; $OUT yarim kaldi."
        exit 1
    fi
fi

if [ "$NPZ" = 1 ]; then
    NPZ_NOTU="The per-sample records of the council round (\`results/q1/konsey_*\` directories, \`.npz\`) are included."
else
    NPZ_NOTU="The per-sample \`.npz\` records of the council round (\`results/q1/konsey_*\` matrix directories, about 60 MB) are not in this repository; they are available from the authors on request and will be deposited on Zenodo with the published version. Without them the analysis outputs listed above can be checked against their stored digests, but the reference sheet cannot be rebuilt from scratch."
fi

if [ "$KURU" = 1 ]; then
    echo
    echo "== yazilacak ust dosyalar =="
    echo "  README.md (baslik: $BASLIK)"
    echo "  CITATION.cff (ayni baslik, ozet)"
    echo "  LICENSE (MIT), .gitignore"
    echo "  REGISTRATION_SHA256SUMS.txt (${#ONKAYIT_LISTESI[@]} dosyanin tam dosya SHA-256 ozeti)"
    echo
    echo "KURU KOSU OZETI"
    echo "  kaynak revizyon : $SHA"
    echo "  kopyalanacak oge: $ADET (dizinler tek oge sayilir)"
    echo "  tahmini boyut   : $(numfmt --to=iec "$TOPLAM" 2>/dev/null || echo "$TOPLAM bayt")"
    echo "  eksik           : $EKSIK"
    echo "  npz             : $([ "$NPZ" = 1 ] && echo dahil || echo 'haric (--with-npz ile eklenir)')"
    echo "Gercek kosu: bash scripts/acik_depo_kur.sh$([ "$NPZ" = 1 ] && echo ' --with-npz')"
    exit 0
fi

echo "== REGISTRATION_SHA256SUMS.txt =="
{
    echo "# Full-file SHA-256 digests of the registration documents, the deviation log,"
    echo "# the cell tables, the frozen analysis script, the addendum scripts and the"
    echo "# council-round outputs, computed when this release was built (source revision $SHA)."
    echo "# The registration texts define their own frozen-body digest (the document up to"
    echo "# its freeze appendix); those digests are recorded inside the documents and in"
    echo "# results/C1_REFERANS_FOYU.md, sections M9.8 and M10.6."
    ( cd "$OUT" && sha256sum "${ONKAYIT_LISTESI[@]}" )
} > "$OUT/REGISTRATION_SHA256SUMS.txt"
grep -c -v '^#' "$OUT/REGISTRATION_SHA256SUMS.txt" | sed 's/^/  ozet satiri: /'

echo "== README / LICENSE / CITATION =="
cat > "$OUT/README.md" <<EOF
# cnn-vit-robustness-protocols

Code, per-sample evaluation records, pre-registration documents and
verification scripts for

> C. Sahin and O. Yildirim, "$BASLIK", submitted to IEEE Access, 2026.

## Summary

Adversarially trained ViTs look like weak transfer sources against CNNs, but
two models cannot split this asymmetry between source and target. The paper
factors log target-correct transfer rates into target vulnerability, symmetric
similarity and directional residual, averaged over a fixed panel of seven
robust ResNet-family CNNs, and tests registered predictions with two or three
runs per cell (brackets: 90% intervals over training runs, conditional on test
images and panel). On CIFAR-10, 0.936 [0.925, 0.948] of ViT-Tiny's panel
source gap to ResNet-18 is symmetric, and the ViT's directional term (+0.012)
is equivalent to zero within +/-0.10. In an architecture-by-initialization
design on a matched pipeline, the scratch-trained ViT is less similar to the
panel than the ResNet (-0.364 [-0.415, -0.314]), a contrast confounded with
its lower clean accuracy. ImageNet initialization narrows it more for the ViT
(+0.260); averaged over initialization, architecture leaves the log
directional term within +/-0.10 (+0.003). On CIFAR-100 the symmetric share
(0.840) replicates, but equivalence of the ViT's directional term is refuted
(+0.143). A small directional term holds only on CIFAR-10, the log scale and a
CNN panel; on the logit scale it is strongly negative.

All numbers are taken from \`results/C1_REFERANS_FOYU.md\`, which
\`scripts/build_reference_sheet.py\` generates from the records.

## Pre-registration

| Path | Content |
|---|---|
| \`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md\` | Main registration (panel tests, two-by-two design, attack side, masking), frozen on 29 October 2026 before any of the new runs |
| \`raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md\` | Addendum (CIFAR-100, ImageNetV2, gradient alignment), frozen on 30 October 2026 before any of its matrices was computed |
| \`raporlar/konsey_2026-10-29/hucre_tablosu*.json\` | Cell tables (which checkpoint fills which design cell) whose digests the analysis outputs record |
| \`results/q1_research/ONKAYIT_SAPMALAR.md\` | Deviation log, including the pre-run digests of the addendum scripts |
| \`experiments/q1_konsey_ayrisim.py\` | The frozen analysis script |
| \`experiments/q1_ek_ayrisim.py\`, \`experiments/q1_ek_gradyan_kosinus.py\`, \`experiments/q1_ek_transfer_matrix.py\` | Addendum wrapper, gradient script and matrix script, digests recorded before their first run |
| \`experiments/q1_ek_masa.py\` | Exploratory and sensitivity analyses computed after the results |
| \`REGISTRATION_SHA256SUMS.txt\` | Full-file digests of the files above at release time |

The registration documents are written in Turkish. In the development
repository they were committed at freezing (main registration: commit
e32f2ce, 29 October 2026; addendum: commit 7325419, 30 October 2026).

## Layout

| Path | Content |
|---|---|
| \`results/c1_*\` | CIFAR-10 campaign: per-sample clean/robust flags for every test image, model and seed; transfer, gradient, attention and depth-profile records; aggregated summaries |
| \`results/q1/konsey_*\` | Council round: panel decomposition (\`konsey_ayrisim_b2.json\`), two-by-two design (\`b4\`), attack side (\`b5\`), masking (\`konsey_b6_maskeleme.json\`), CIFAR-100 (\`konsey_b9_c100/\`), ImageNetV2 (\`konsey_b8_imagenetv2/\`), gradient alignment (\`konsey_b10_gradyan/\`), post-hoc analyses (\`konsey_ek_masa/\`) |
| \`results/q1/\` (other) | CIFAR-100 and SVHN replications of the protocol comparison, the L2 check, the checkpoint-selection ablation, pool fits and the machine-read Mahmood et al. (2021) tables |
| \`results/C1_REFERANS_FOYU.md\` | Generated reference sheet. Every number in the paper is taken from this file |
| \`src/analysis/protokoller.py\` | The single definition of the four conditioning protocols |
| \`scripts/build_reference_sheet.py\` | Regenerates the reference sheet from the records |
| \`experiments/\` | Evaluation and analysis drivers (matrix computation needs the checkpoints) |
| \`src/\`, \`cli/\`, \`configs/\` | Training, attack and evaluation code |
| \`data/val_split_indices*.json\` | The fixed validation split (seed 777), excluded from every training stage |

$NPZ_NOTU

Seeds: ResNet-18 runs 1001, 1002, 1003; ViT-Tiny runs 2001, 2002, 2003;
validation split 777; AutoAttack and analysis sampling 42.

The reference sheet and some record keys are labelled in Turkish. Key terms:
\`temiz\` clean, \`gurbuz\` robust, \`ham\` raw (unconditioned), \`hedef dogru\`
target-correct, \`her ikisi dogru\` both-correct, \`basarili kaynak\`
successful-source, \`kosum\` training run, \`cift\` run pair, \`tohum\` seed,
\`yayilim\` spread, \`ozdeslik\` identity, \`secim\` checkpoint selection,
\`on kayit\` pre-registration, \`ek\` addendum, \`sapma\` deviation,
\`hucre tablosu\` cell table, \`dondurulmus\` frozen, \`sarmalayici\` wrapper.

## Reproduce the numbers

\`\`\`bash
pip install -r requirements.txt    # numpy, scipy, pandas and matplotlib suffice for the analysis
sha256sum -c <(grep -v '^#' REGISTRATION_SHA256SUMS.txt)
python scripts/build_reference_sheet.py   # needs the full record set (see above)
git status --short results/C1_REFERANS_FOYU.md   # no change expected
\`\`\`

\`scripts/verify_manuscript_numbers.py\` and \`scripts/check_manuscript_claims.py\`
check every carrier number and claim in the manuscript against these
records. They expect the manuscript sources under \`paper/manuscript/\`, which
are not part of this repository; they are included so that the checks can be
rerun once the paper is published.

## Not included

Trained checkpoints (about 40 GB) and the archived adversarial examples used
by the calibration runs and the council round. Both are available from the
authors on request; neither is needed to recompute the reported numbers from
the records.

## License

Code is released under the MIT License (see \`LICENSE\`). The evaluation
records and the generated reference sheet are released under CC BY 4.0.

## Citation

See \`CITATION.cff\`.
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

cat > "$OUT/CITATION.cff" <<EOF
cff-version: 1.2.0
message: "If you use this code or these records, please cite the paper below."
title: "cnn-vit-robustness-protocols"
abstract: "Code, per-sample evaluation records, pre-registration documents and verification scripts for the paper '$BASLIK'. The paper factors log target-correct transfer rates between adversarially trained models into target vulnerability, symmetric similarity and a directional residual against a fixed panel of seven robust CNNs, and tests registered predictions in an architecture-by-initialization design on CIFAR-10, with CIFAR-100, ImageNetV2 and gradient-alignment addenda."
authors:
  - family-names: Sahin
    given-names: Cagri
    affiliation: "Mus Alparslan University"
  - family-names: Yildirim
    given-names: Ozal
    affiliation: "Firat University"
year: 2026
repository-code: "https://github.com/cagrisahin58/$AD"
license: MIT
preferred-citation:
  type: unpublished
  title: "$BASLIK"
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

echo "== git (YEREL; push YOK) =="
GN=$(git config user.name); GE=$(git config user.email)
cd "$OUT"
git init -q -b main
git config user.name "$GN"; git config user.email "$GE"
git add -A
git -c commit.gpgsign=false commit -q \
    -m "Initial release: analysis pipeline, per-sample records, pre-registration documents and verification scripts" \
    -m "Accompanies the manuscript '$BASLIK' (IEEE Access submission). Snapshot of the private working repository at revision $SHA; the registration documents were committed there at freezing (e32f2ce, 7325419)."
git log --format='%h %an <%ae> %s' -1
git log --format=%B -1 | grep -c 'Co-Authored' || true
cd - > /dev/null

BOYUT=$(du -sh "$OUT" | cut -f1)
DOSYA=$(find "$OUT" -type f -not -path '*/.git/*' | wc -l)
echo
echo "DEPO  : $OUT"
echo "BOYUT : $BOYUT"
echo "DOSYA : $DOSYA"
echo
echo "BU BETIK PUSH ETMEZ. Kullanicinin adimlari:"
echo "  1. GitHub'da bos, herkese acik depo ac: cagrisahin58/$AD (README/LICENSE eklemeden)."
echo "     Eski 4 Ekim kopyasi daha once itildiyse depo zaten vardir; o zaman 2. adimda --force gerekir."
echo "  2. cd $OUT && git remote add origin https://github.com/cagrisahin58/$AD.git && git push -u origin main"
echo "  3. curl -s -o /dev/null -w '%{http_code}\n' https://github.com/cagrisahin58/$AD   # 200 beklenir"
# PUSH SATIRI (KULLANICI KOSAR, BETIK KOSMAZ):
# cd "$OUT" && git remote add origin "https://github.com/cagrisahin58/$AD.git" && git push -u origin main
