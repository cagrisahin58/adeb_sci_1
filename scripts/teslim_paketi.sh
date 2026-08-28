#!/usr/bin/env bash
# TESLIM PAKETI: hocaya verilecek klasoru kurar ve arsivler.
#
# YAPI: HER CIKTI KENDI KLASORUNDE. Uc cikti var (bildiri, Ingilizce dergi
# makalesi, Turkce surumu) ve hepsinin dayandigi ORTAK kanit (sayilarin tek
# kaynagi, koken defteri, on kayitlar, kapilar) ayri bir klasorde durur --
# cunku o kanit ucune birden aittir, kopyalanirsa uc surumu ayrisir.
#
#   00_ORTAK_KANIT/   sayilar · koken · on kayit · kapilar · kararlar · hikaye
#   01_BILDIRI/       ATEEC 2026, Ingilizce, 6 sayfa
#   02_MAKALE_EN/     SCI dergisine gonderilecek surum
#   03_MAKALE_TR/     ayni makalenin Turkce surumu (gonderilmiyor)
#
# Listede olmayan hicbir sey pakete girmez; listede olup bulunamayan her sey
# EKRANA YAZILIR (sessiz eksik yok).
#
# Kosum:  bash scripts/teslim_paketi.sh
set -u
cd "$(dirname "$0")/.." || exit 1

TARIH=$(git log -1 --format=%cd --date=format:%Y%m%d 2>/dev/null || echo bilinmiyor)
SHA=$(git rev-parse --short HEAD 2>/dev/null || echo bilinmiyor)
HEDEF="teslim/TESLIM_${TARIH}_${SHA}"

rm -rf "$HEDEF"
mkdir -p "$HEDEF"/00_ORTAK_KANIT/{sayilar,on_kayit,kapilar,kararlar,hikaye}
mkdir -p "$HEDEF"/01_BILDIRI/kaynak
mkdir -p "$HEDEF"/02_MAKALE_EN/kaynak
mkdir -p "$HEDEF"/03_MAKALE_TR/kaynak

eksik=()
al() {  # $1=kaynak $2=hedef alt yol
    if [ -e "$1" ]; then
        cp -r "$1" "$HEDEF/$2" && return 0
    fi
    eksik+=("$1")
    return 1
}

say() { printf '  %-58s %s\n' "$1" "$2"; }

# ======================================================== 00 ORTAK KANIT
echo "== 00_ORTAK_KANIT"
al results/C1_REFERANS_FOYU.md            00_ORTAK_KANIT/sayilar/ && say "referans foyu" "sayilarin TEK kaynagi"
al results/q1/KOKEN.json                  00_ORTAK_KANIT/sayilar/ && say "koken defteri" "44 artefaktin sha256'si"
al results/c1_transfer/c1_transfer_summary.json 00_ORTAK_KANIT/sayilar/ && say "transfer ozeti" "Tablo III'un kaynagi"
al results/c1_eval_summary.json           00_ORTAK_KANIT/sayilar/ && say "gurbuzluk ozeti" "Tablo I'in kaynagi"

for f in E1_PILOT_KAPISI E2_ISTATISTIK_PROTOKOLU E3_YENIDEN_TASARIM \
         E6_ON_KAYIT E7_KOSUM_ONCESI_KONTROL; do
    al "results/q1_research/$f.md" 00_ORTAK_KANIT/on_kayit/
done
say "on kayit belgeleri" "5 dosya, salt-ekleme"

for f in kapilar.sh verify_manuscript_numbers.py check_manuscript_claims.py \
         check_abstract_body.py q1_tr_decimal_check.py bildiri_tutarlilik.py \
         check_en_tr_mirror.py gonderim_tutarlilik.py \
         test_claim_guards.sh test_abstract_body_check.sh \
         test_bildiri_tutarlilik.sh test_en_tr_mirror.sh \
         test_verify_numbers.sh test_gonderim_tutarlilik.sh; do
    al "scripts/$f" 00_ORTAK_KANIT/kapilar/
done
al src/analysis/protokoller.py            00_ORTAK_KANIT/kapilar/
say "kapilar" "7 denetim + 6 oz-sinama + protokol tanimi"

al results/q1_research/TESLIM_DURUMU.md      00_ORTAK_KANIT/kararlar/
al results/q1_research/DEVAM_TALIMATI.md     00_ORTAK_KANIT/kararlar/
al results/q1_research/KAMPANYA_KARARLARI.md 00_ORTAK_KANIT/kararlar/
al results/q1_research/Q1_ARASTIRMA_RAPORU.md 00_ORTAK_KANIT/kararlar/
al results/q1_research/B2_DURUM.md           00_ORTAK_KANIT/kararlar/
al results/q1_research/B2_KAPI_KUSURU.md     00_ORTAK_KANIT/kararlar/
al paper/review/HAKEM_RAPORU_2026-08-24.md   00_ORTAK_KANIT/kararlar/
say "kararlar ve denetim" "hangi karar neden verildi"

al results/q1_research/HIKAYE_VE_POSTER_RAPORU.md 00_ORTAK_KANIT/hikaye/
say "hikaye raporu" "poster ve ozet cizim icin"

echo "  kapi ciktisi uretiliyor..."
bash scripts/kapilar.sh > "$HEDEF/00_ORTAK_KANIT/kapilar/SON_KAPI_CIKTISI.txt" 2>&1
say "son kapi ciktisi" "$(tail -1 "$HEDEF/00_ORTAK_KANIT/kapilar/SON_KAPI_CIKTISI.txt")"

# ============================================================ 01 BILDIRI
echo
echo "== 01_BILDIRI"
al paper/bildiri/bildiri.pdf 01_BILDIRI/ && mv "$HEDEF/01_BILDIRI/bildiri.pdf" \
    "$HEDEF/01_BILDIRI/BILDIRI_ATEEC2026.pdf" && say "bildiri.pdf" "6 sayfa, IEEE conference"
al paper/bildiri/bildiri.tex 01_BILDIRI/kaynak/
al paper/bildiri/bildiri.bib 01_BILDIRI/kaynak/
al paper/bildiri/figures      01_BILDIRI/kaynak/
say "kaynak" "tex + bib + figurler"

# =========================================================== 02 MAKALE EN
echo
echo "== 02_MAKALE_EN"
al paper/manuscript/main.pdf 02_MAKALE_EN/ && mv "$HEDEF/02_MAKALE_EN/main.pdf" \
    "$HEDEF/02_MAKALE_EN/MAKALE_EN.pdf" && say "main.pdf" "gonderilecek surum"
al paper/manuscript/main.tex       02_MAKALE_EN/kaynak/
al paper/manuscript/sections       02_MAKALE_EN/kaynak/
al paper/manuscript/references.bib 02_MAKALE_EN/kaynak/
al paper/figures/final             02_MAKALE_EN/kaynak/
say "kaynak" "tex + bolumler + kaynakca + figurler"
mkdir -p "$HEDEF/02_MAKALE_EN/gonderim"
for f in cover_letter.pdf cover_letter.tex highlights.txt declarations.txt \
         pre_submission_checklist.md suggested_reviewers.md \
         author_biographies.tex; do
    al "paper/submission/$f" 02_MAKALE_EN/gonderim/
done
say "gonderim" "kapak mektubu · one cikanlar · beyanlar · kontrol listesi"

# =========================================================== 03 MAKALE TR
echo
echo "== 03_MAKALE_TR"
al paper/manuscript_tr/main.pdf 03_MAKALE_TR/ && mv "$HEDEF/03_MAKALE_TR/main.pdf" \
    "$HEDEF/03_MAKALE_TR/MAKALE_TR.pdf" && say "main.pdf" "Turkce surum (gonderilmiyor)"
al paper/manuscript_tr/main.tex 03_MAKALE_TR/kaynak/
al paper/manuscript_tr/sections  03_MAKALE_TR/kaynak/
al paper/figures/final_tr        03_MAKALE_TR/kaynak/
al paper/manuscript_tr/TERMINOLOJI.md 03_MAKALE_TR/
say "kaynak" "tex + bolumler + figurler + terminoloji sozlugu"

# ================================================================ OKUBENI
cat > "$HEDEF/OKUBENI.md" <<MD
# Teslim paketi

Depo \`$SHA\` (dal \`q1\`) · paket tarihi $TARIH

## Klasorler

| Klasor | Ne var |
|---|---|
| \`00_ORTAK_KANIT/\` | Uc ciktinin da dayandigi kanit: sayilarin tek kaynagi, koken defteri, on kayitlar, yedi denetim kapisi, kararlar ve hikaye raporu |
| \`01_BILDIRI/\` | ATEEC 2026 bildirisi (Ingilizce, 6 sayfa) + kaynagi |
| \`02_MAKALE_EN/\` | SCI dergisine **gonderilecek** surum, kaynagi ve gonderim malzemeleri (kapak mektubu, one cikanlar, beyanlar, kontrol listesi) |
| \`03_MAKALE_TR/\` | Ayni makalenin Turkce surumu + terminoloji sozlugu |

## Uc cikti, iki yayin

\`02_MAKALE_EN\` ile \`03_MAKALE_TR\` **ayni makalenin iki dildeki surumudur**,
iki ayri makale degildir; gonderilecek olan Ingilizce surumdur. Bildiri ayri
ve gercek bir ikinci ciktidir. Dergi makalesi bildiriye atif verir ve
genisletilmis surum oldugunu beyan eder.

## Kanit neden ayri klasorde

Ucunun de sayilari ayni artefaktlardan gelir. Kanit her klasore
kopyalansaydi uc surum zamanla ayrisirdi; bu projede tam olarak bu tur bir
ayrisma iki kez kusur uretti. Bu yuzden tek kopya, \`00_ORTAK_KANIT/\`.

## Sayilar nereden geliyor

Disariya cikan her sayi \`00_ORTAK_KANIT/sayilar/C1_REFERANS_FOYU.md\`
dosyasindan gelir ve o dosya artefaktlardan **otomatik** uretilir. Iddianin
denetlenebilir olmasi icin yedi kapi yazildi;
\`00_ORTAK_KANIT/kapilar/SON_KAPI_CIKTISI.txt\` son kosumun sonucudur.

Kapilarin kendileri de kirilarak sinanir (\`test_*.sh\`). Bu projenin en
pahali dersi sudur: **gecen bir kontrol, yakaladigini kanitlamaz.**

## Hocaya anlatmak icin

\`00_ORTAK_KANIT/hikaye/HIKAYE_VE_POSTER_RAPORU.md\` calismayi hicbir makine
ogrenmesi bilgisi gerektirmeden anlatir; on panel icin cizim notu ve hazir
sayi foyu tasir.

## Yeniden uretmek icin

\`\`\`bash
bash scripts/kapilar.sh              # yedi kapi birden
bash scripts/test_claim_guards.sh    # kapilarin kendi sinamasi
docker exec -w /workspace adeb_eval python scripts/build_reference_sheet.py
\`\`\`

## Gonderim oncesi kalan uc is

1. iThenticate intihal kontrolu
2. IEEE Author Portal'a yukleme
3. Depo URL'sinin metne girmesi (\`main.tex\` icinde TODO olarak isaretli)
MD

# ================================================================== OZET
echo
if [ ${#eksik[@]} -gt 0 ]; then
    echo "EKSIK (${#eksik[@]}):"
    printf '  - %s\n' "${eksik[@]}"
else
    echo "EKSIK YOK"
fi

tar -czf "${HEDEF}.tar.gz" -C teslim "$(basename "$HEDEF")"
echo
echo "PAKET : $HEDEF"
echo "ARSIV : ${HEDEF}.tar.gz  ($(du -h "${HEDEF}.tar.gz" | cut -f1))"
echo "DOSYA : $(find "$HEDEF" -type f | wc -l) dosya"
