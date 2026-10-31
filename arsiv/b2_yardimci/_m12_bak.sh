#!/bin/bash
# M12 foy uretimi sonrasi hizli bakis (31.10.2026)
cd /home/firat/projects/adeb_sci_1
echo "err:"; tail -5 arsiv/b2_yardimci/_m12_foy_err.txt
sha256sum results/C1_REFERANS_FOYU.md
wc -l results/C1_REFERANS_FOYU.md
echo "--- M12 icinde ARTEFAKT YOK / bulunamadi / FARKLI:"
grep -n 'ARTEFAKT YOK: alan\|bulunamadi\|FARKLI' results/C1_REFERANS_FOYU.md | awk -F: '$1>2200' | cut -c1-300
grep -n '^## M12\|^### M12\|^## Sabit' results/C1_REFERANS_FOYU.md
