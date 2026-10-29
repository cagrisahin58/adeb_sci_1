#!/bin/bash
# Tur 2 sinamasi: scripts/konsey_b3_kuyruk.sh uctan uca, sahte egiticiyle.
# Konteynerde /workspace'ten calistirilir. Gercek models/ ve logs/ dizinlerine
# dokunmaz; her senaryo /tmp altinda ayri bir sahne dizininde kosar.
set -uo pipefail
W=/workspace
T=$W/results/q1/konsey_smoke/_dogrulayici/t2_kuyruk
GERCEK_PY=$(command -v python)
export GERCEK_PY

sahne_kur() {  # -> S
    S=$(mktemp -d /tmp/b3_sahne_XXXX)
    mkdir -p "$S/scripts" "$S/logs" "$S/results/q1" "$S/bin" "$S/data"
    cp "$W/scripts/konsey_b3_kuyruk.sh" "$W/scripts/konsey_b3_denetim.py" "$S/scripts/"
    cp "$W/results/q1/konsey_pilot_zaman.json" "$S/results/q1/"
    for f in "$W"/logs/C1_clean_vit_200[123].log; do ln -s "$f" "$S/logs/"; done
    cat > "$S/bin/python" <<EOF
#!/bin/bash
if [ "\$1" = "-m" ] && [ "\$2" = "cli.main" ]; then exec "$GERCEK_PY" "$T/sahte_egitici.py" "\$@"; fi
exec "$GERCEK_PY" "\$@"
EOF
    chmod +x "$S/bin/python"
    export SAHTE_SIRA="$S/sira.txt" SAHTE_EP1="$S/ep1.json"
    : > "$SAHTE_SIRA"
}
ep1() { printf '{"V_IN": %s, "R224_IN": %s, "R224_scr": %s}\n' "$1" "$2" "$3" > "$S/ep1.json"; }
kos() {  # ek argumanlar -> RC, cikti $S/cikti_N.txt
    N=$((N + 1))
    KONSEY_B3_KOK="$S" PATH="$S/bin:$PATH" bash "$S/scripts/konsey_b3_kuyruk.sh" "$@" > "$S/cikti_$N.txt" 2>&1
    RC=$?
    echo "  kosu $N (args: $*): rc=$RC; son satir: $(tail -1 "$S/cikti_$N.txt")"
}
sira() { echo "  cagri sirasi:"; sed 's/^/    /' "$SAHTE_SIRA"; }
denetimler() { echo "  defter denetim satirlari:"; awk -F'\t' '$4 ~ /denetim|tasindi|at_ozet/ {print "    " $3 " " $4 " " $7 " | " $11}' "$S/results/q1/konsey_b3_defter.tsv"; }

echo "=== Senaryo A: normal akis (V_IN ilk epok 90, R224_IN 80, R224_scr 35)"
N=0; sahne_kur; ep1 90 80 35
kos
sira; denetimler
A_S=$S

echo "=== Senaryo B: R224_IN KALDI (ilk epok 38 < 35 + 5), ayni komutla yeniden, sonra duzeltilmis kosu"
N=0; sahne_kur; ep1 90 38 35
kos
kos
echo "  R224_IN_s1301 AT klasoru var mi: $([ -d "$S/models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv" ] && echo EVET || echo HAYIR)"
rm -rf "$S/models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/clean"; ep1 90 80 35
kos
sira; denetimler

echo "=== Senaryo C: V_IN KALDI (ilk epok 28 < C1 ViT ilk epok ort. + 5), iki kez"
N=0; sahne_kur; ep1 28 80 35
kos
kos
sira; denetimler

echo "=== Senaryo D: A tamamlandiktan sonra --in-at-lr 0.0005 (cokus kurali sonrasi yeniden baslatma)"
S=$A_S; export SAHTE_SIRA="$S/sira_D.txt" SAHTE_EP1="$S/ep1.json"; : > "$SAHTE_SIRA"; N=10
kos --in-at-lr 0.0005
sira; denetimler
echo "  AT klasorleri ve at_lr.txt:"
for f in "$S"/models/q1/konsey/*/*/adv/adversarial_training*/; do
    echo "    ${f#$S/models/q1/konsey/} lr=$(cat "$f/at_lr.txt" 2>/dev/null || echo yok)"
done
echo "=== Senaryo D2: ayni komut tekrar (hicbir sey kosmamali)"
: > "$SAHTE_SIRA"; kos --in-at-lr 0.0005; echo "  cagri sayisi: $(wc -l < "$SAHTE_SIRA")"

echo "=== Senaryo E: --dry-run"
KONSEY_B3_KOK="$A_S" bash "$W/scripts/konsey_b3_kuyruk.sh" --dry-run | head -12
rm -rf /tmp/b3_sahne_*
