#!/usr/bin/env bash
# Konsey turu commit 3: kosu ciktilari (B3 2x2 egitimi, B4-B6 matrisler ve AutoAttack, ek bloklar B8-B10),
# sonuc raporlari, foy M9-M10, sapma kaydi, yardimci betikler, B3 model meta dosyalari.
# Co-Authored-By YOK (30.09 karari). Push YOK (kullaniciya). WSL'de calistirilir (Windows git'i satir sonu
# farki yuzunden eski dosyalari degismis gosterir; bu betik yalniz WSL git'iyle kullanilir).
# Kullanim:
#   bash arsiv/b2_yardimci/_konsey_commit3.sh --dry-run > arsiv/b2_yardimci/_commit3_kuru.txt 2>&1
#   bash arsiv/b2_yardimci/_konsey_commit3.sh            # git add + git commit (yerel)
# Dosyalar TEK TEK adlandirilir (dizin eklenmez). Haric: *.pth/*.pt/*.safetensors, 1 MB (1048576 bayt) ve
# ustu, baglar (symlink) ve bag altindakiler, results/q1/konsey_adv_onbellek/, results/q1/adv_archive,
# _ek_denetim/dis/ (ucuncu taraf kopyalari, telif), __pycache__, .gitignore'un dislandiklari
# (git check-ignore; or. aa_chunk_*.npz), B3 egitim gunlukleri logs/konsey_b3/*.log (1-10 MB; onceki iki
# kayitta logs/ altindan hic dosya alinmadi, ayni olcut), degismemis izli dosyalar.
# Not: "find -size -1M" 1 MiB birimine yukari yuvarlar ve yalniz bos dosyalari secer; esik baytla uygulanir.
set -euo pipefail
cd /home/firat/projects/adeb_sci_1

KURU=0
case "${1:-}" in
    --dry-run|--kuru) KURU=1 ;;
    "") ;;
    *) echo "kullanim: $0 [--dry-run]" >&2; exit 1 ;;
esac
R=raporlar/konsey_2026-10-29
B=arsiv/b2_yardimci
SINIR=1048576
BU_BETIK=$B/_konsey_commit3.sh

echo "=== git status --porcelain satir sayisi (baslangic): $(git status --porcelain | wc -l)"
echo "=== HEAD: $(git rev-parse --short HEAD) (beklenen 7325419)"
[ "$(git rev-parse --short=7 HEAD)" = "7325419" ] || echo "UYARI: HEAD 7325419 degil"

# --- 0. Dondurulmus dosyalar calisma agacinda degismemis olmali ---
DONDURULMUS=(
    experiments/q1_konsey_ayrisim.py
    experiments/c1_c3_transfer_matrix.py
    $R/hucre_tablosu.json $R/hucre_tablosu_b8.json $R/hucre_tablosu_b9.json
    $R/ON_KAYIT_2026-10-29.md $R/ON_KAYIT_EK_B8_B10_2026-10-30.md
)
if [ -n "$(git status --porcelain -- "${DONDURULMUS[@]}")" ]; then
    echo "HATA: dondurulmus dosyalardan biri calisma agacinda degismis; commit yapilmaz." >&2
    git status --porcelain -- "${DONDURULMUS[@]}" >&2
    exit 2
fi
echo "=== dondurulmus dosyalar HEAD ile ayni (${#DONDURULMUS[@]} dosya)"
if [ "$KURU" = 0 ] && [ -n "$(git diff --cached --name-only)" ]; then
    echo "HATA: sahnede (index) onceden bekleyen degisiklik var; once temizlenmeli." >&2
    git diff --cached --name-only >&2
    exit 2
fi

# --- 1. Aday dosyalar ---
ADAY=()
HARIC=$(mktemp)
ekle() { local f; for f in "$@"; do ADAY+=("$f"); done; }
dizin_ekle() {
    local d f
    for d in "$@"; do
        if [ ! -d "$d" ] || [ -L "$d" ]; then printf 'dizin yok ya da bag\t%s\n' "$d" >> "$HARIC"; continue; fi
        while IFS= read -r f; do ADAY+=("$f"); done < <(find "$d" \( -type f -o -type l \) | sort)
    done
}
shopt -s nullglob

# (a) B3-B6 ciktilari
ekle results/q1/konsey_zincir_durum.tsv results/q1/konsey_zincir_dry_run.txt results/q1/konsey_b3_defter.tsv \
     results/q1/konsey_ayrisim_b4.json results/q1/konsey_ayrisim_b5.json results/q1/konsey_b6_maskeleme.json
dizin_ekle results/q1/konsey_b4_matris results/q1/konsey_b5_saldiri results/q1/konsey_b6_aa
ekle results/q1/konsey_ayrisim_b2.json; dizin_ekle results/q1/konsey_b2_panel logs/b2   # ana oturum 31.10: B2 ciktilari ve B2 gunlugu
ekle logs/konsey_b2.log logs/konsey_b4.log logs/konsey_b5_mi.log logs/konsey_b5_tgr.log logs/konsey_b6_aa.log raporlar/konsey_2026-10-29/13_b10_r18_r50_denetimi.md arsiv/b2_yardimci/_b10_r18_r50_denetim.py arsiv/b2_yardimci/_b10_denetim_cikti/denetim.json
# (b) ek bloklar B8-B10, ek gunlukleri, GPU n=200 regresyonu
dizin_ekle results/q1/konsey_b8_imagenetv2 results/q1/konsey_b9_c100 results/q1/konsey_b10_gradyan \
           results/q1/ek_loglar results/q1/ek_regresyon/gpu_n200
# (c) gunlukler: zincir, B3 kuyrugu, kuru kosu, cokus isaretleri, nvidia-smi/df izi
ekle logs/konsey_zincir.log logs/konsey_b3_kuyruk.log logs/konsey_b3_kuru_kosu.log logs/konsey_b3/nvidia_smi_df.log
for f in logs/konsey_b3/*.txt; do ekle "$f"; done
for f in logs/konsey_b3/*.log; do
    [ "$f" = logs/konsey_b3/nvidia_smi_df.log ] && continue
    printf 'egitim gunlugu (logs/ olcutu), %s bayt\t%s\n' "$(stat -c %s "$f")" "$f" >> "$HARIC"
done
# (d) raporlar ve sapma kaydi
ekle $R/09_sonuc_b2_b6.md $R/10_konteyner_yeniden_kurulum.md $R/11_sonuc_b8_b10.md \
     $R/adeb_eval_pip_freeze.txt $R/adeb_eval_inspect.json results/q1_research/ONKAYIT_SAPMALAR.md
if [ -e $R/13_b10_r18_r50_denetimi.md ]; then ekle $R/13_b10_r18_r50_denetimi.md; fi
# (e) foy ve uretici betik
ekle results/C1_REFERANS_FOYU.md scripts/build_reference_sheet.py
# (f) yardimci betikler
for f in $B/_ek_*.sh $B/_ek_*.py $B/_ek_*.log $B/_ek_*.md $B/_rapor_*.py $B/_rapor_*.sh $B/_b10_*.py; do ekle "$f"; done
for f in $B/_foy_m9_kontrol.py $B/_foy_m10_kontrol.py "$BU_BETIK" $B/_commit3_kuru.txt; do
    if [ -e "$f" ]; then ekle "$f"; fi
done
# (g) B3 model meta dosyalari (metrics.jsonl, at_lr.txt, TRAINING_COMPLETE); agirliklar asagida dislanir
dizin_ekle models/q1/konsey

# --- 2. Haric kurallari ---
LISTE=$(mktemp)
: > "$LISTE.aday"
for f in "${ADAY[@]}"; do
    neden=""
    if [ -L "$f" ]; then neden="bag"
    elif [ ! -f "$f" ]; then neden="dosya degil ya da yok"
    else
        case "$f" in
            */_ek_denetim/dis/*) neden="ucuncu taraf kopyasi (telif)" ;;
            results/q1/konsey_adv_onbellek/*|results/q1/adv_archive*) neden="onbellek" ;;
            */__pycache__/*|*.pyc|*/.pytest_cache/*) neden="pycache" ;;
            *.pth|*.pt|*.safetensors) neden="model agirligi" ;;
        esac
        d=$f
        while [ -z "$neden" ] && [ "${d%/*}" != "$d" ]; do
            d=${d%/*}
            if [ -L "$d" ]; then neden="bag altinda"; fi
        done
        if [ -z "$neden" ]; then
            s=$(stat -c %s "$f")
            if [ "$s" -ge "$SINIR" ]; then neden="1 MB ustu, $s bayt"; fi
        fi
    fi
    if [ -n "$neden" ]; then printf '%s\t%s\n' "$neden" "$f" >> "$HARIC"; else echo "$f" >> "$LISTE.aday"; fi
done
sort -u "$LISTE.aday" -o "$LISTE.aday"
git check-ignore --stdin < "$LISTE.aday" > "$LISTE.yok" || true
grep -vxF -f "$LISTE.yok" "$LISTE.aday" > "$LISTE.izsiz_dahil" || true
# Degismemis izli dosyalari at (yalniz yeni ya da degismis olanlar kalir)
DEG=$(mktemp)
{ tr '\n' '\0' < "$LISTE.izsiz_dahil" | xargs -0 -r git ls-files --others --exclude-standard --
  tr '\n' '\0' < "$LISTE.izsiz_dahil" | xargs -0 -r git diff HEAD --name-only --; } | sort -u > "$DEG"
grep -xF -f "$DEG" "$LISTE.izsiz_dahil" > "$LISTE" || true
grep -vxF -f "$DEG" "$LISTE.izsiz_dahil" > "$LISTE.degismemis" || true

# --- 3. Guvenlik denetimleri ---
YASAK=$(grep -E '\.pth$|\.pt$|\.safetensors$|^results/q1/konsey_adv_onbellek/|^results/q1/adv_archive|/_ek_denetim/dis/|/__pycache__/' "$LISTE" || true)
BUYUK=$(while IFS= read -r f; do if [ "$(stat -c %s "$f")" -ge "$SINIR" ]; then echo "$f"; fi; done < "$LISTE")
BAG=$(while IFS= read -r f; do if [ -L "$f" ]; then echo "$f"; fi; done < "$LISTE")
DONDU=$(printf '%s\n' "${DONDURULMUS[@]}" | grep -xF -f - "$LISTE" || true)
if [ -n "$YASAK$BUYUK$BAG$DONDU" ]; then
    echo "HATA: listede yasak dosya, 1 MB ustu dosya, bag ya da dondurulmus dosya var:" >&2
    printf '%s\n' "$YASAK" "$BUYUK" "$BAG" "$DONDU" | grep -v '^$' >&2 || true
    exit 4
fi
# Gizli bilgi taramasi (metin dosyalari; bu betigin kendisi desenleri icerdigi icin taranmaz)
GIZLI_DESEN='hf_[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{30,}|gho_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[abprs]-[A-Za-z0-9-]{10,}|(password|passwd|sifre)[[:space:]]*[:=][[:space:]]*[^[:space:]]{4,}'
GIZLI=$( (grep -vE '\.(npz|npy)$' "$LISTE" || true) | (grep -vxF "$BU_BETIK" || true) | tr '\n' '\0' | (xargs -0 -r grep -lEI "$GIZLI_DESEN" -- || true) )
if [ -n "$GIZLI" ]; then
    echo "HATA: gizli bilgi desenine uyan dosya var; commit yapilmaz:" >&2
    echo "$GIZLI" >&2
    exit 6
fi

echo "=== haric tutulan aday dosyalar ($(wc -l < "$HARIC")):"
sort -t$'\t' -k1,1 -k2,2 "$HARIC"
echo "=== git'in yok saydigi aday dosyalar ($(wc -l < "$LISTE.yok")):"
cat "$LISTE.yok"
echo "=== izli ve degismemis oldugu icin atlanan aday dosyalar ($(wc -l < "$LISTE.degismemis")):"
cat "$LISTE.degismemis"
echo "=== yasak denetimi: *.pth/*.pt/*.safetensors, onbellek, dis/, bag, 1 MB ustu, dondurulmus dosya yok"
echo "=== gizli bilgi taramasi: eslesme yok"
echo "=== gruplara gore eklenecek dosya sayisi"
awk -F/ '{ if (NF<=3) g=$1"/"$2; else g=$1"/"$2"/"$3; print g }' "$LISTE" | sort | uniq -c

N=$(wc -l < "$LISTE")
TOPLAM=$(tr '\n' '\0' < "$LISTE" | du -cb --files0-from=- | tail -1 | cut -f1)
EN_BUYUK=$(tr '\n' '\0' < "$LISTE" | du -b --files0-from=- | sort -n | tail -1)

if [ "$KURU" = 1 ]; then
    echo "=== KURU KOSU: git add --dry-run (commit yapilmaz)"
    git add --dry-run --pathspec-from-file="$LISTE" | tee "$LISTE.kuru"
    NK=$(wc -l < "$LISTE.kuru")
    echo "=== git add --dry-run satir sayisi: $NK (liste: $N)"
    if [ "$NK" != "$N" ]; then echo "UYARI: git add --dry-run satir sayisi listeyle uyusmuyor"; fi
    echo "=== en buyuk dosya: $EN_BUYUK"
    echo "=== not: _commit3_kuru.txt bu kosuda yazilmakta oldugu icin boyutu toplamda kismi ya da 0 sayilir."
    echo "=== dosya sayisi: $N"
    echo "=== toplam boyut: $TOPLAM bayt ($(( TOPLAM / 1024 )) KiB, $(awk -v t="$TOPLAM" 'BEGIN{printf "%.2f", t/1048576}') MiB)"
    rm -f "$LISTE" "$LISTE".* "$DEG" "$HARIC"
    exit 0
fi

git add --pathspec-from-file="$LISTE" || { echo "HATA: git add basarisiz" >&2; exit 3; }
NS=$(git diff --cached --name-only | wc -l)
echo "=== sahnelenen: $NS dosya (liste: $N)"
rm -f "$LISTE" "$LISTE".* "$DEG" "$HARIC"
if git diff --cached --name-only | grep -E '\.pth$|\.pt$|\.safetensors$|/_ek_denetim/dis/|^results/q1/konsey_adv_onbellek/'; then
    echo "HATA: sahnede yasak dosya" >&2; exit 5
fi
if [ "$NS" != "$N" ]; then echo "HATA: sahnelenen sayi listeyle uyusmuyor" >&2; exit 5; fi
echo "=== dosya sayisi: $N, toplam boyut: $TOPLAM bayt ($(( TOPLAM / 1024 )) KiB)"

git commit -q -F - <<'MSG'
Konsey turu kosulari: B3 2x2 egitimi, B4-B6 matrisler ve AutoAttack, ek bloklar B8-B10, sonuc raporlari, foy M9-M10

- B3: 2x2'nin yeni hucreleri (V-IN 2101-2102, R224-scr 1201-1202, R224-IN 1301-1302) temiz ve AT
  egitimleri; defter results/q1/konsey_b3_defter.tsv, epok metrikleri models/q1/konsey/**/metrics.jsonl
  (agirliklar depo disi).
- B4-B6: transfer matrisi, MI ve TGR saldiri kollari, AutoAttack ve maskeleme denetimi; dondurulmus on
  kaydin sirali sonuc haritasina gore sonuc bolgesi O1, B6'da maskeleme isareti yok
  (raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md).
- B9 (CIFAR-100, baglayici): K-a ve K-c destek, K-b curutuldu (pozitif yon)
  (raporlar/konsey_2026-10-29/11_sonuc_b8_b10.md).
- B8 (ImageNetV2): betimsel ve kesifsel, Holm ailesi ve baglayici karar yok.
- B10: F_B10 alti sinamanin altisi Holm sonrasi destek.
- Foy: results/C1_REFERANS_FOYU.md M9 (konsey 2x2) ve M10 (ek bloklar); scripts/build_reference_sheet.py.
- Sapma kaydi: results/q1_research/ONKAYIT_SAPMALAR.md 31.10.2026 kayitlari (ana on kayit 7,
  ek on kayit 12, GPU catal regresyonu notu).
- Konteyner yeniden kurulumu: 10_konteyner_yeniden_kurulum.md, adeb_eval pip freeze ve docker inspect
  (gizli bilgi taramasi temiz).

Haric: *.pth, 1 MB ve ustu dosyalar (B10 kosinus.npz cifar10 ve cifar100, gpu_n200 .npy onbellekleri),
aa_chunk_*.npz (.gitignore), konsey_adv_onbellek, adv_archive, _ek_denetim/dis (telif), B3 egitim
gunlukleri logs/konsey_b3/*.log (1-10 MB). Ayrinti: arsiv/b2_yardimci/_commit3_kuru.txt.
MSG
git log -1 --format='%h %ad %s' --date=iso
echo "Co-Authored satiri sayisi: $(git log -1 --format=%B | grep -c 'Co-Authored' || true)"
echo "Push yapilmadi; dis zaman damgasi icin kullanici asagidaki satiri calistirir."
# git push origin q1
