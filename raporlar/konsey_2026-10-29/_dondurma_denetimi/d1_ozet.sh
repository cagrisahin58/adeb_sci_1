#!/bin/bash
# Denetim 1: sha256 ozetleri yeniden hesapla
cd /home/firat/projects/adeb_sci_1 || exit 1
echo "HEAD: $(git rev-parse HEAD)  dal: $(git branch --show-current)"
sha256sum experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json
echo "--- govde (sed tarifiyle) ---"
sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | sha256sum
echo "--- govde satir sayisi ---"
sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | wc -l
echo "--- Dondurma eki baslik satirlari ---"
grep -n '^## Dondurma eki' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md
grep -c '^## Dondurma eki$' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md
echo "--- CRLF ve BOM denetimi ---"
for f in raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json raporlar/konsey_2026-10-29/KONSEY_PLANI.md raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md; do
  printf '%s crlf=%s bom=' "$f" "$(grep -c $'\r' "$f")"
  head -c3 "$f" | xxd -p
done
echo "--- ozetlerin ekte gecen bicimi ---"
grep -n -i 'sha256\|sha-256\|46ab58\|4bce2c\|2a8913' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md
echo "--- git durum (bu dosyalar) ---"
git status --porcelain -- raporlar/konsey_2026-10-29/ experiments/q1_konsey_ayrisim.py | head -50
echo "--- git log son 3 ---"
git log --oneline -3
echo "--- HEAD'de q1_konsey_ayrisim.py izleniyor mu ---"
git ls-files experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json
