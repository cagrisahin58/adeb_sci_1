#!/usr/bin/env bash
# Konsey turu commit 1: on kayit dondurma (B0-B1 kod, smoke, zaman pilotu, cozumleme betigi, masa cozumlemeleri).
# Co-Authored-By YOK (30.09 karari). WSL'de calistirilir (Windows git'i satir sonu farki yuzunden
# eski dosyalari degismis gosterir; bu betik yalniz WSL git'iyle kullanilir).
# Kullanim:
#   bash arsiv/b2_yardimci/_konsey_commit1.sh --kuru   # git add --dry-run; commit YAPMAZ
#   bash arsiv/b2_yardimci/_konsey_commit1.sh          # git add + git commit (yerel; push kullaniciya)
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1

KURU=0
[ "${1:-}" = "--kuru" ] && KURU=1

# --- 0. Dondurulmus dosyalarin ozetleri (ON_KAYIT_2026-10-29.md Dondurma eki a ve b) ---
BEK_AYRISIM=4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389
BEK_HUCRE=2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500
BEK_GOVDE=46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5
OK=raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md
A=$(sha256sum experiments/q1_konsey_ayrisim.py | cut -d' ' -f1)
H=$(sha256sum raporlar/konsey_2026-10-29/hucre_tablosu.json | cut -d' ' -f1)
G=$(sed '/^## Dondurma eki$/,$d' "$OK" | sha256sum | cut -d' ' -f1)
echo "ayrisim  $A"
echo "hucre    $H"
echo "govde    $G"
if [ "$A" != "$BEK_AYRISIM" ] || [ "$H" != "$BEK_HUCRE" ] || [ "$G" != "$BEK_GOVDE" ]; then
    echo "HATA: ozet Dondurma ekindekiyle uyusmuyor; commit yapilmaz." >&2
    exit 2
fi
echo "ozetler Dondurma ekiyle ayni"
echo "HEAD: $(git rev-parse --short HEAD) (dondurma eki: 4972738)"
[ "$(git rev-parse --short=7 HEAD)" = "4972738" ] || echo "UYARI: HEAD 4972738 degil; Dondurma eki (f) guncellenmeli"

# --- 1. Aday yollar (bu turun isi) ---
ADAY=(
    src/models/r224.py src/models/__init__.py
    src/training/trainer.py src/training/adversarial_trainer.py
    cli/train.py experiments/c1_c3_transfer_matrix.py
    experiments/q1_konsey_ayrisim.py experiments/q1_konsey_masa.py
    experiments/q1_konsey_masa_yeniden_kos.py experiments/q1_konsey_sahte_sinama.py
    experiments/q1_etkilesim_simetri_masa.py
    raporlar/konsey_2026-10-29
    results/q1/konsey_smoke results/q1/konsey_masa results/q1/_konsey_sahte
    results/q1/konsey_pilot_zaman.json results/q1/konsey_pilot_zaman_parca_V_IN.json
    results/q1/konsey_pilot_zaman_parca_R224_IN.json results/q1/konsey_pilot_zaman_parca_R224_scr.json
    results/q1/konsey_sahte_2x2_sinama.json results/q1/konsey_sentez_r_tau_masa.json
    results/q1/etkilesim_simetri_masa.json
    results/q1_research/BEKLEYEN_SEKIL_GOREVI_2026-10-29.md results/q1_research/DEVAM_TALIMATI.md
    arsiv/b2_yardimci/_konsey_commit1.sh
)
for f in scripts/konsey_*; do ADAY+=("$f"); done

# --- 2. Haric kurallari: models/, logs/, > 5 MB, *.pt *.pth *.safetensors *.npy, onbellek klasorleri,
#        _dogrulayici/eski_kod (HEAD 4972738 kodunun birebir kopyasi; git archive ile yeniden uretilir),
#        git'in yok saydigi dosyalar (ornegin aa_chunk_*.npz) ---
LISTE=$(mktemp)
find "${ADAY[@]}" -type f \
    -not -path 'models/*' -not -path 'logs/*' \
    -not -path '*/__pycache__/*' -not -path '*/.ipynb_checkpoints/*' -not -path '*/.pytest_cache/*' \
    -not -path 'results/q1/konsey_smoke/_dogrulayici/eski_kod/*' \
    -not -name '*.pt' -not -name '*.pth' -not -name '*.safetensors' -not -name '*.npy' -not -name '*.pyc' \
    -size -5121k 2>/dev/null | sort -u > "$LISTE.aday"
git check-ignore --stdin < "$LISTE.aday" > "$LISTE.yok" || true
grep -vxF -f "$LISTE.yok" "$LISTE.aday" > "$LISTE" || true
# Degismemis izlenen dosyalari listeden at (yalniz yeni ya da degismis olanlar kalir)
DEG=$(mktemp)
{ git ls-files --others --exclude-standard -- "${ADAY[@]}"; git diff HEAD --name-only -- "${ADAY[@]}"; } | sort -u > "$DEG"
grep -xF -f "$DEG" "$LISTE" > "$LISTE.son" || true
mv "$LISTE.son" "$LISTE"

echo "=== yok sayilan (git check-ignore) aday dosya sayisi: $(wc -l < "$LISTE.yok")"
echo "=== eklenecek dosya listesi"
cat "$LISTE"
N=$(wc -l < "$LISTE")
TOPLAM=$(tr '\n' '\0' < "$LISTE" | du -cb --files0-from=- | tail -1 | cut -f1)
echo "=== dosya sayisi: $N, toplam boyut: $TOPLAM bayt ($(( TOPLAM / 1024 )) KiB)"
EN_BUYUK=$(tr '\n' '\0' < "$LISTE" | du -b --files0-from=- | sort -n | tail -1)
echo "=== en buyuk dosya: $EN_BUYUK"

if [ "$KURU" = 1 ]; then
    echo "=== KURU KOSU: git add --dry-run (commit yapilmaz)"
    git add --dry-run --pathspec-from-file="$LISTE"
    rm -f "$LISTE" "$LISTE.aday" "$LISTE.yok" "$DEG"
    exit 0
fi

git add --pathspec-from-file="$LISTE" || { echo "HATA: git add basarisiz" >&2; exit 3; }
rm -f "$LISTE" "$LISTE.aday" "$LISTE.yok" "$DEG"
echo "=== sahnelenen: $(git diff --cached --name-only | wc -l) dosya"

git commit -q -F - <<'MSG'
Konsey turu: on kayit donduruldu (B0-B1 kod, smoke, zaman pilotu, cozumleme betigi, masa cozumlemeleri)

Manset (on kayitli): CNN ile yama tabanli ViT arasindaki transfer hedefin beyaz kutu kirilganligi (w),
simetrik benzerlik (tau) ve kucuk bir yonlu terim (r) olarak ayrisir; ViT'nin "zayif kaynak" gorunumu
buyuk olcude simetrik benzemezliktir (masa: simetrik oran 0,927, jackknife 0,919-0,935) ve girdi hatti
ile egitim tarifi esitlenmis bir mimari x baslatma 2x2'si benzemezligin ve yonlu terimin hangi etmene
ait oldugunu belirler.

2x2: V-scr (C1 ViT-Tiny, 2001-2003), V-IN (deit_tiny_patch16_224.fb_in1k, 2101-2102),
R224-scr (timm resnet18, V-scr ile ayni normalizasyonsuz 32->224 girdi hatti, 1201-1202),
R224-IN (resnet18.a1_in1k, 1301-1302). IN normalizasyonu yalniz IN hucrelerinde, baslatma demetinin
parcasi (fable K3). Birincil panel 7 RobustBench CNN (B2 sonuclarindan once donduruldu).
Aileler: F_B2 (K-a, K-b, K-c) ve F_B4 (H1, H2, H3), Holm; B5 korunma orani; B6 maskeleme kurali.

Dondurma: raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md (bu commit dondurmanin zaman damgasi).
SHA-256:
  experiments/q1_konsey_ayrisim.py                 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389
  raporlar/konsey_2026-10-29/hucre_tablosu.json    2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500
  on kayit govdesi (Dondurma eki oncesi)           46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5
  govde komutu: sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | sha256sum
AT tavani 80 epok (pilot W(80) = 20,47 sa, bos GPU; paylasimda ~40,94 sa; tavan kosu ortasinda degismez).
Butce: B3 egitim payi 38,15 GPU-saat (bekci aynen); en kotu toplam 42,2 GPU-saat (B5, B6 A onceligi, K2).

Kod: src/models/r224.py (resnet18_224, resnet18_224_in1k, vit_tiny_in1k), cli/train.py (--optimizer,
--init-weights, --lr-schedule, --stop-epoch, --max-train-batches), trainer ve adversarial_trainer,
c1_c3_transfer_matrix.py (--attack pgd/mi/tgr, --steps, --sources, --cache-adv, --skip-existing),
scripts/konsey_* (indirme, smoke, pilot, B3 kuyrugu ve denetimi, B6 maskeleme).
Dogrulama: iki celisik dogrulayicinin ilk hukmu "duzeltilmeli"; kod tarafinda 10, cozumleme tarafinda
17 bulgu, hepsi duzeltildi. Varsayilan bayraklarla yeni matris kodu eski kodla hucre ve ornek duzeyinde
birebir; cozumleme betigi SENTEZ'in 223 degerini en cok 7,8e-16 farkla uretir; sahte 2x2 uctan uca
gecti; K-c uc tohumlu yol sahte sinamayla calistirildi. Dondurma dogrulayicisi: kabul (bloklayici yok;
denetim izi raporlar/konsey_2026-10-29/_dondurma_denetimi/). Hic n=10000 kosusu yapilmadi; B2-B6 kullaniciya
(raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md). Haric: models/, logs/, >5 MB, *.pt, *.pth,
*.safetensors, *.npy (onbellek tensorleri; kucuk meta JSON'lari dahil), _dogrulayici/eski_kod.
MSG
git log -1 --format='%h %ad %s' --date=iso
git log -1 --format=%B | grep -c 'Co-Authored' || true
echo "Push onerilir (dis zaman damgasi): git push origin q1"
