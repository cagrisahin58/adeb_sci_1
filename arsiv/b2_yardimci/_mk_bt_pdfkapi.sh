#!/usr/bin/env bash
cd /home/firat/projects/adeb_sci_1 || exit 1
bash arsiv/b2_yardimci/_mk_bt_derle.sh 2>&1 | grep -v '505.12177\|Underfull' | head -20
docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py 2>&1 | grep -v 'yazi tipleri' | tail -8
docker exec -w /workspace adeb_eval python scripts/check_pdf_render.py 2>&1 | grep KALDI
