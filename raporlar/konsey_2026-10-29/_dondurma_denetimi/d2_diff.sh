#!/bin/bash
cd /home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29 || exit 1
OUT=_dondurma_denetimi/d2_diff.txt
diff ON_KAYIT_TASLAGI.md ON_KAYIT_2026-10-29.md > "$OUT"
echo "diff cikis kodu: $?"
wc -l "$OUT"
echo "--- degisen satir numaralari (taslak tarafi) ---"
grep -E '^[0-9]+' "$OUT"
echo "--- kelime duzeyinde fark (git diff --word-diff, no-index) ---"
git diff --no-index --word-diff=porcelain ON_KAYIT_TASLAGI.md ON_KAYIT_2026-10-29.md > _dondurma_denetimi/d2_worddiff.txt
wc -l _dondurma_denetimi/d2_worddiff.txt
echo "--- taslak dosyasinin zaman damgasi ---"
stat -c '%y %n' ON_KAYIT_TASLAGI.md ON_KAYIT_2026-10-29.md
