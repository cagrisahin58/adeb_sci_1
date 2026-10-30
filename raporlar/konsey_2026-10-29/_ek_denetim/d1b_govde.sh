#!/bin/bash
cd /home/firat/projects/adeb_sci_1
echo "ON_KAYIT govde:"; sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | sha256sum
echo "EK govde:"; sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md | sha256sum
sha256sum raporlar/konsey_2026-10-29/hucre_tablosu_b8.json raporlar/konsey_2026-10-29/hucre_tablosu_b9.json raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md
grep -n '^## ' raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md
echo "KONSEY_PLANI prefix check:"
git show HEAD:raporlar/konsey_2026-10-29/KONSEY_PLANI.md > /tmp/kp_head.md
N=$(stat -c %s /tmp/kp_head.md); echo "head size $N"
head -c $N raporlar/konsey_2026-10-29/KONSEY_PLANI.md | sha256sum; sha256sum /tmp/kp_head.md
git diff --stat HEAD -- raporlar/konsey_2026-10-29/KONSEY_PLANI.md
git diff HEAD -- raporlar/konsey_2026-10-29/KONSEY_PLANI.md | grep '^-' | head
