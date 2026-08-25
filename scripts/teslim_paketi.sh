#!/usr/bin/env bash
# TESLIM PAKETI: hocaya verilecek tek klasoru kurar ve arsivler.
#
# Icerik ve GEREKCESI TESLIM_DURUMU.md §4'te tanimlidir. Bu betik o listeyi
# uygular; listede olmayan hicbir sey pakete girmez, listede olup bulunamayan
# her sey EKRANA YAZILIR (sessiz eksik yok).
#
# Kosum:  bash scripts/teslim_paketi.sh
# Cikti:  teslim/ATEEC_ve_SCI_teslim_<tarih>/  ve ayni adla .tar.gz
set -u
cd "$(dirname "$0")/.." || exit 1

TARIH=$(git log -1 --format=%cd --date=format:%Y%m%d 2>/dev/null || echo bilinmiyor)
SHA=$(git rev-parse --short HEAD 2>/dev/null || echo bilinmiyor)
HEDEF="teslim/ATEEC_ve_SCI_teslim_${TARIH}_${SHA}"

rm -rf "$HEDEF"
mkdir -p "$HEDEF"/{01_pdf,02_sayilar,03_on_kayit,04_kapilar,05_kararlar}

eksik=()
kopyala() {  # $1=kaynak $2=hedef alt klasor
    if [ -e "$1" ]; then
        cp -r "$1" "$HEDEF/$2/" && echo "  + $1"
    else
        eksik+=("$1")
    fi
}

echo "=== 01 PDF (teslimin kendisi) ==="
kopyala paper/bildiri/bildiri.pdf            01_pdf
kopyala paper/manuscript/main.pdf            01_pdf
kopyala paper/manuscript_tr/main.pdf         01_pdf
mv "$HEDEF/01_pdf/main.pdf" "$HEDEF/01_pdf/makale_EN.pdf" 2>/dev/null || true
cp paper/manuscript_tr/main.pdf "$HEDEF/01_pdf/makale_TR.pdf" 2>/dev/null || true
mv "$HEDEF/01_pdf/bildiri.pdf" "$HEDEF/01_pdf/bildiri_ATEEC2026.pdf" 2>/dev/null || true

echo "=== 02 Sayilarin tek kaynagi ve kokeni ==="
kopyala results/C1_REFERANS_FOYU.md          02_sayilar
kopyala results/q1/KOKEN.json                02_sayilar
kopyala results/c1_transfer/c1_transfer_summary.json  02_sayilar
kopyala results/c1_eval_summary.json         02_sayilar

echo "=== 03 On-kayit belgeleri (salt-ekleme disiplininin kaniti) ==="
for f in E1_PILOT_KAPISI E2_ISTATISTIK_PROTOKOLU E3_YENIDEN_TASARIM \
         E6_ON_KAYIT E7_KOSUM_ONCESI_KONTROL; do
    kopyala "results/q1_research/$f.md"      03_on_kayit
done

echo "=== 04 Kapilar ve oz-sinamalari ==="
for f in kapilar.sh verify_manuscript_numbers.py check_manuscript_claims.py \
         check_abstract_body.py q1_tr_decimal_check.py bildiri_tutarlilik.py \
         check_en_tr_mirror.py test_claim_guards.sh test_abstract_body_check.sh \
         test_bildiri_tutarlilik.sh test_en_tr_mirror.sh; do
    kopyala "scripts/$f"                     04_kapilar
done
kopyala src/analysis/protokoller.py          04_kapilar

echo "=== 05 Kararlar ve kayitlar ==="
kopyala results/q1_research/TESLIM_DURUMU.md      05_kararlar
kopyala results/q1_research/DEVAM_TALIMATI.md     05_kararlar
kopyala results/q1_research/KAMPANYA_KARARLARI.md 05_kararlar
kopyala results/q1_research/Q1_ARASTIRMA_RAPORU.md 05_kararlar
kopyala results/q1_research/B2_DURUM.md           05_kararlar
kopyala results/q1_research/B2_KAPI_KUSURU.md     05_kararlar
kopyala paper/review/HAKEM_RAPORU_2026-08-24.md   05_kararlar

# --- kapi ciktisi paketle birlikte gitsin (iddianin kaniti) ---
echo "=== kapi ciktisi uretiliyor ==="
bash scripts/kapilar.sh > "$HEDEF/04_kapilar/KAPI_CIKTISI.txt" 2>&1
echo "  kapi sonucu: $(tail -1 "$HEDEF/04_kapilar/KAPI_CIKTISI.txt")"

cat > "$HEDEF/OKUBENI.md" <<MD
# Teslim paketi

Depo: \`$SHA\` (dal q1) · paket tarihi: $TARIH

## Ne var burada

| klasor | ne |
|---|---|
| 01_pdf | Uc cikti: ATEEC 2026 bildirisi (EN), dergi makalesi (EN) ve ayni makalenin Turkce surumu |
| 02_sayilar | Disari cikan her sayinin tek kaynagi (\`C1_REFERANS_FOYU.md\`) ve 44 artefaktin sha256 koken defteri |
| 03_on_kayit | Kosumdan once yazilmis, salt-ekleme on-kayit belgeleri |
| 04_kapilar | Alti otomatik denetim, dort oz-sinama, protokol tanimlarinin tek kaynagi ve son kapi ciktisi |
| 05_kararlar | Hangi kararin neden verildigi, hakem raporu, protokol duzeltmesinin kaydi |

## Uc cikti, iki yayin

\`makale_EN.pdf\` ile \`makale_TR.pdf\` **ayni makalenin iki dildeki surumudur**,
iki ayri makale degildir; gonderilecek olan Ingilizce surumdur. Bildiri ayri ve
gercek bir ikinci ciktidir.

## Sayilar nereden geliyor

Bu projede disariya cikan her sayi \`C1_REFERANS_FOYU.md\` dosyasindan gelir ve
o dosya artefaktlardan OTOMATIK uretilir. Iddia denetlenebilir olsun diye alti
kapi yazildi; \`04_kapilar/KAPI_CIKTISI.txt\` son kosumun sonucudur. Kapilarin
kendileri de kirilarak sinanir (\`test_*.sh\`): gecen bir kontrol, yakaladigini
kanitlamaz.

## Yeniden uretmek icin

\`\`\`bash
bash scripts/kapilar.sh                 # alti kapi
bash scripts/test_claim_guards.sh       # kapilarin kendi sinamasi
docker exec -w /workspace adeb_eval python scripts/build_reference_sheet.py
\`\`\`
MD

echo
if [ ${#eksik[@]} -gt 0 ]; then
    echo "EKSIK (${#eksik[@]}):"
    printf '  - %s\n' "${eksik[@]}"
else
    echo "EKSIK YOK"
fi

tar -czf "${HEDEF}.tar.gz" -C teslim "$(basename "$HEDEF")"
echo
echo "PAKET: $HEDEF"
echo "ARSIV: ${HEDEF}.tar.gz  ($(du -h "${HEDEF}.tar.gz" | cut -f1))"
