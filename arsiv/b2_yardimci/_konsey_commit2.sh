#!/usr/bin/env bash
# Konsey turu commit 2: ek on kayit B8-B10 dondurma (ImageNetV2 paneli, CIFAR-100 paneli, gradyan kosinusu),
# zincir betigi, D diski plani. Co-Authored-By YOK (30.09 karari). WSL'de calistirilir (Windows git'i satir
# sonu farki yuzunden eski dosyalari degismis gosterir; bu betik yalniz WSL git'iyle kullanilir).
# Kullanim:
#   bash arsiv/b2_yardimci/_konsey_commit2.sh --kuru   # git add --dry-run; commit YAPMAZ
#   bash arsiv/b2_yardimci/_konsey_commit2.sh          # git add + git commit (yerel; push kullaniciya)
# Dosyalar TEK TEK adlandirilir (dizin eklenmez): models/, logs/, baglar (symlink), > 5 MB, *.pt, *.pth,
# *.safetensors, *.npy, *.tar*, *.html (dis/ klasorundeki dis HTML kopyalari telif geregi) HARIC.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1

KURU=0
[ "${1:-}" = "--kuru" ] && KURU=1
R=raporlar/konsey_2026-10-29
EK=$R/ON_KAYIT_EK_B8_B10_2026-10-30.md

# --- 0. Ozetler (ON_KAYIT_EK_B8_B10_2026-10-30.md Dondurma eki a-d) ---
BEK_AYRISIM=4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389
BEK_HUCRE=2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500
BEK_OK_GOVDE=46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5
BEK_B8=4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d
BEK_B9=be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd
BEK_C1C3=f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7
BEK_EK_GOVDE=76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595
ozet() { sha256sum "$1" | cut -d' ' -f1; }
A=$(ozet experiments/q1_konsey_ayrisim.py)
H=$(ozet $R/hucre_tablosu.json)
OKG=$(sed '/^## Dondurma eki$/,$d' $R/ON_KAYIT_2026-10-29.md | sha256sum | cut -d' ' -f1)
B8=$(ozet $R/hucre_tablosu_b8.json)
B9=$(ozet $R/hucre_tablosu_b9.json)
C=$(ozet experiments/c1_c3_transfer_matrix.py)
G=$(sed '/^## Dondurma eki$/,$d' "$EK" | sha256sum | cut -d' ' -f1)
printf 'ayrisim   %s\nhucre     %s\nok_govde  %s\nhucre_b8  %s\nhucre_b9  %s\nc1_c3     %s\nek_govde  %s\n' "$A" "$H" "$OKG" "$B8" "$B9" "$C" "$G"
if [ "$A" != "$BEK_AYRISIM" ] || [ "$H" != "$BEK_HUCRE" ] || [ "$OKG" != "$BEK_OK_GOVDE" ] || \
   [ "$B8" != "$BEK_B8" ] || [ "$B9" != "$BEK_B9" ] || [ "$C" != "$BEK_C1C3" ] || [ "$G" != "$BEK_EK_GOVDE" ]; then
    echo "HATA: ozet Dondurma ekindekiyle uyusmuyor; commit yapilmaz." >&2
    exit 2
fi
echo "ozetler Dondurma ekiyle ayni"
if [ -n "$(git status --porcelain -- experiments/c1_c3_transfer_matrix.py experiments/q1_konsey_ayrisim.py $R/hucre_tablosu.json $R/ON_KAYIT_2026-10-29.md)" ]; then
    echo "HATA: dondurulmus dosyalardan biri calisma agacinda degismis" >&2; exit 2
fi
echo "HEAD: $(git rev-parse --short HEAD) (dondurma eki f: e32f2ce)"
[ "$(git rev-parse --short=7 HEAD)" = "e32f2ce" ] || echo "UYARI: HEAD e32f2ce degil; Dondurma eki (f) guncellenmeli"

# --- 1. Aday dosyalar, tek tek ---
ADAY=(
    "$EK"
    $R/hucre_tablosu_b8.json
    $R/hucre_tablosu_b9.json
    $R/KONSEY_PLANI.md
    results/q1_research/ONKAYIT_SAPMALAR.md
    $R/06_ek_deney_literatur.md
    $R/06_ek_deney_tasarim.md
    $R/ON_KAYIT_EK_B8_B9_TASLAK.md
    $R/07_disk_D_plani.md
    $R/08_ek_kod_raporu.md
    tests/test_q1_ek.py
    scripts/d_diskine_tasi.sh
    scripts/konsey_tam_zincir.sh
    results/q1/konsey_zincir_dry_run.txt
    arsiv/b2_yardimci/_konsey_commit2.sh
)
[ -f $R/_commit2_kuru.txt ] && ADAY+=($R/_commit2_kuru.txt)
for f in $R/_ek_*.py $R/_ek_*.json $R/_ek_*.sh $R/_ek_*.txt \
         experiments/q1_ek_*.py scripts/ek_*.sh scripts/ek_*.py; do
    [ -e "$f" ] && ADAY+=("$f")
done
# _ek_denetim/ ve results/q1/ek_regresyon/ altindaki dosyalar tek tek (dizin olarak eklenmez)
while IFS= read -r f; do ADAY+=("$f"); done < <(find $R/_ek_denetim results/q1/ek_regresyon -type f -not -path '*/_ek_denetim/dis/*' | sort)

# --- 2. Haric kurallari ---
LISTE=$(mktemp)
HARIC=$(mktemp)
for f in "${ADAY[@]}"; do
    neden=""
    if [ -L "$f" ]; then neden="bag"
    elif [ ! -f "$f" ]; then neden="dosya degil ya da yok"
    else
        case "$f" in
            models/*|logs/*|*/__pycache__/*|*/.pytest_cache/*) neden="haric yol" ;;
            *.pt|*.pth|*.safetensors|*.npy|*.pyc|*.tar|*.tar.gz|*.gz|*.html|*.htm) neden="haric uzanti" ;;
        esac
        # yol uzerinde bag var mi (or. data/ ya da models/ bagi altinda dosya)
        d=$(dirname "$f"); while [ "$d" != "." ] && [ -z "$neden" ]; do [ -L "$d" ] && neden="bag altinda"; d=$(dirname "$d"); done
        [ -z "$neden" ] && [ "$(stat -c %s "$f")" -gt 5242880 ] && neden="5 MB ustu"
    fi
    if [ -n "$neden" ]; then echo "$neden	$f" >> "$HARIC"; else echo "$f" >> "$LISTE.aday"; fi
done
sort -u "$LISTE.aday" -o "$LISTE.aday"
git check-ignore --stdin < "$LISTE.aday" > "$LISTE.yok" || true
grep -vxF -f "$LISTE.yok" "$LISTE.aday" > "$LISTE" || true
# Degismemis izlenen dosyalari at (yalniz yeni ya da degismis olanlar kalir)
DEG=$(mktemp)
{ git ls-files --others --exclude-standard -- $(cat "$LISTE"); git diff HEAD --name-only -- $(cat "$LISTE"); } | sort -u > "$DEG"
grep -xF -f "$DEG" "$LISTE" > "$LISTE.son" || true
mv "$LISTE.son" "$LISTE"

echo "=== haric tutulan aday dosyalar ($(wc -l < "$HARIC")):"
sort "$HARIC"
echo "=== git'in yok saydigi aday dosyalar ($(wc -l < "$LISTE.yok")):"
cat "$LISTE.yok"
echo "=== eklenecek dosya listesi"
cat "$LISTE"
N=$(wc -l < "$LISTE")
TOPLAM=$(tr '\n' '\0' < "$LISTE" | du -cb --files0-from=- | tail -1 | cut -f1)
echo "=== dosya sayisi: $N, toplam boyut: $TOPLAM bayt ($(( TOPLAM / 1024 )) KiB)"
EN_BUYUK=$(tr '\n' '\0' < "$LISTE" | du -b --files0-from=- | sort -n | tail -1)
echo "=== en buyuk dosya: $EN_BUYUK"
# Son guvenlik: listede yasak bir sey var mi
YASAK=$(grep -E '^models/|^logs/|\.pt$|\.pth$|\.safetensors$|\.npy$|\.html?$' "$LISTE" || true)
BAG=$(while IFS= read -r f; do [ -L "$f" ] && echo "$f"; done < "$LISTE")
if [ -n "$YASAK$BAG" ]; then echo "HATA: listede yasak dosya ya da bag var:"; echo "$YASAK$BAG"; exit 4; fi
echo "=== yasak denetimi: models/, logs/, *.pt, *.pth, *.safetensors, *.npy, *.html, bag yok"

if [ "$KURU" = 1 ]; then
    echo "=== KURU KOSU: git add --dry-run (commit yapilmaz)"
    git add --dry-run --pathspec-from-file="$LISTE"
    rm -f "$LISTE" "$LISTE.aday" "$LISTE.yok" "$DEG" "$HARIC"
    exit 0
fi

git add --pathspec-from-file="$LISTE" || { echo "HATA: git add basarisiz" >&2; exit 3; }
rm -f "$LISTE" "$LISTE.aday" "$LISTE.yok" "$DEG" "$HARIC"
echo "=== sahnelenen: $(git diff --cached --name-only | wc -l) dosya"
git diff --cached --name-only | grep -E '^models/|^logs/|\.pt$|\.pth$|\.html?$' && { echo "HATA: sahnede yasak dosya" >&2; exit 5; }

git commit -q -F - <<'MSG'
Konsey ek bloklar B8-B10: ek on kayit donduruldu (ImageNetV2 paneli, CIFAR-100 paneli, gradyan kosinusu); zincir betigi; D diski plani

Ek on kayit: raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md (bu commit dondurmanin zaman
damgasi). Dondurulmus ON_KAYIT_2026-10-29.md'yi degistirmez. B9 = CIFAR-100 paneli, dondurulmus
q1_konsey_ayrisim.py --mod b2 ile birebir yineleme (F_B9, Holm, baglayici). B8 = ImageNetV2
MatchedFrequency n = 2000, PGD-10 eps 4/255, ortak BicubicRes256Crop224 hatti; IN satirinin dogal
olcekte betimsel karsiligi, Holm ailesi yok. B10 = modeller arasi girdi gradyani kosinusu c_ij ile
log tau, uc veri kumesi x {ham, ana etki artigi} Mantel, F_B10 alti sinama, Holm.
SHA-256:
  ek on kayit govdesi (Dondurma eki oncesi)        76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595
  govde komutu: sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md | sha256sum
  raporlar/konsey_2026-10-29/hucre_tablosu_b8.json 4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d
  raporlar/konsey_2026-10-29/hucre_tablosu_b9.json be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd
  experiments/c1_c3_transfer_matrix.py (degismedi)  f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7
  q1_konsey_ayrisim.py, hucre_tablosu.json ve dondurulmus on kayit govdesi e32f2ce'dekiyle ayni.

Liu karari (fable): Liu2023Comprehensive ConvNeXt-B / Swin-B cifti IN satiri kestirimine girmez,
sifirdan satirinda ayri verilir. Kanit: ARES yapilandirmalari yalniz model adinda ayrilir ve on egitim
bayragi yok; RobustBench additional_data false; Liu Tablo 7'nin on egitimsiz SwinB satiri (temiz,
PGD100, AA = 76,6 / 60,2 / 57,3) ARES README SwinB satiriyla ayni (dogrulayici HTML kopyasindan okudu;
kopya telif geregi depoya islenmedi, ozeti Dondurma eki e'de). IN satiri iki Singh ciftine dayanir.

Hakem hukmu ve kapanis: taslak (ON_KAYIT_EK_B8_B9_TASLAK.md) celisik hakemden "buyuk revizyon" aldi;
fable kararlari E1-E7 ile kapatildi (catal betik, ozgun matris betigine dokunulmadi; B8 Holm ailesi
kaldirildi, beklenti H1+H2'den A_IN <= -0,10; Imagenette yerine ImageNetV2; B10'a ana etki artigi
sinamasi ve Zhang ve ark. 2307.07873 onculu; K-b(B9) TOST ulasilamazligi sinirlilik). Dondurma
dogrulayicisi: kabul, commit oncesi duzeltmeler istendi ve yapildi: GPU n=200 catal regresyonu
tasarima yazildi (bash scripts/ek_regresyon.sh gpu 200; sapma degil), varsayilanlar (bicubic, 9999
permutasyon) metinle esitlendi, kismi_omega sinamalari on kayit disi kesifsel (F_B10 disi), S10-3
kodu yazilmadi notu, kosinus.npz float16 / c_ij float64 notu, onisleme denetimi kodu ek 5.5
esikleriyle (%25, 0,6 x RobustBench, mutlak fark <= 5 puan, 3-5 isaretli) karar yazar,
KONSEY_PLANI 13 indirme cumlesi. Ayrinti: Dondurma eki "Dondurma dogrulayicisi duzeltmeleri".

Indirme (D diski, /mnt/d/adeb_sci_1_veri, olculmus): 26 dosya 5910,6 MB (yedekler Wong2020Fast,
Chen2021LTD_WRN34_10, Cui2023Decoupled_WRN-28-10 dahil); yedeksiz 5468,3 MB, beyan 5448,0 MB, grup
duzeyinde uyumlu. ImageNetV2 arsivi sha256 f0c37fdf925916b19ea1323cd9a2208cdb6959ba2c32eef2a7fc393835c9ca7c
(results/q1_research/ONKAYIT_SAPMALAR.md "Ek B8-B10", kod eki ozetleriyle birlikte).

Kod: experiments/q1_ek_transfer_matrix.py (catal), q1_ek_ayrisim.py, q1_ek_gradyan_kosinus.py,
tests/test_q1_ek.py (22 CPU birim sinamasi gecti), scripts/ek_* (indirme, regresyon, sahte V2 smoke,
kuru ayristirma, zincir komutlari), scripts/konsey_tam_zincir.sh, scripts/d_diskine_tasi.sh.
CPU on regresyonu n = 40 birebir. Hic B8, B9, B10 kosusu yapilmadi; GPU isleri B3-B6 zincirinden sonra.
Haric: models/, logs/, baglar, >5 MB, *.pt, *.pth, *.npy, *.html (dis HTML kopyalari, telif).
MSG
git log -1 --format='%h %ad %s' --date=iso
git log -1 --format=%B | grep -c 'Co-Authored' || true
echo "Push onerilir (dis zaman damgasi): git push origin q1"
