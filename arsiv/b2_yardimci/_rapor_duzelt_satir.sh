#!/bin/bash
# Salt okur: dogrulayici bulgulari icin satir denetimi (31.10.2026)
cd /home/firat/projects/adeb_sci_1
for n in 46 56 59 65 71 76 77; do
  echo "ZL $n: $(sed -n "${n}p" logs/konsey_zincir.log | cut -c1-300)"
done
echo ----NV
sed -n '93,115p;185,230p' logs/konsey_b3/nvidia_smi_df.log
echo ----OK
grep -n -E 'S1|Welch' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | cut -c1-1500
