#!/usr/bin/env bash
# TUR 4 (A10): C4 oznitelik analizini blok-cikisi CLS serisiyle YENIDEN kos.
#
# Neden: cos_cls / cos_token_mean yalniz .mlp alt-bloklari icin
# hesaplaniyordu; siniflandirici ise son BLOK cikisinin CLS'ini okur.
# Bolum 4.7'nin derinlik anlatisi bu yuzden olculmemis bir tensore
# dayaniyordu. Kod artik blok cikisinda da CLS ve token-ortalama uretiyor.
#
# Eski artefaktlar SILINMEZ: tarihsel kayit olarak results/c1_c4_t4oncesi/
# altina tasinir (karantina disiplini).
set -eu
cd /home/firat/projects/adeb_sci_1

ESKI=results/c1_c4_t4oncesi
if [ ! -d "$ESKI" ]; then
    mkdir -p "$ESKI"
    cp -r results/c1_c4/pair* "$ESKI"/
    echo "eski artefaktlar saklandi: $ESKI"
else
    echo "yedek zaten var: $ESKI"
fi

# atla-eger-var korumasini asmak icin yalniz ozet dosyalarini kaldir
for p in 1 2 3; do
    rm -f "results/c1_c4/pair${p}/c4_summary.json"
done
echo "ozet dosyalari temizlendi; kosum basliyor"

docker exec -w /workspace adeb_eval \
    python experiments/c1_c4_attention_features.py --n-samples 1000 --seed 42
