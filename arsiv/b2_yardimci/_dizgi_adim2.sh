#!/usr/bin/env bash
# 2026-10-04 dizgi adim 2: fd adi, metin yamalari, derleme, dizgi denetimi.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo '=== cls bas (1-49) ve ptm izleri'
sed -n '1,49p' paper/manuscript/ieeeaccess.cls | grep -v '^\s*$' | head -40
grep -n -i -E 'ptm|RequirePackage\{(times|mathptmx|newtx|txfonts)' paper/manuscript/ieeeaccess.cls | head
grep -n -B2 'OT1/ptm/bx/n. in size <5>' paper/manuscript/main.log | head -6
echo '=== TGR butce'
python3 -c "import json;d=json.load(open('results/c1_c2/pair1/tgr_summary.json'));print(d['attack_budget'])"
echo '=== fd kopyasi (buyuk harfli ad)'
cp paper/manuscript/t1times.fd paper/manuscript/T1times.fd && ls paper/manuscript/*.fd
echo '=== yamalar'
python3 arsiv/b2_yardimci/_render_duzeltmeleri.py
python3 arsiv/b2_yardimci/_lecun_metin1.py
echo '=== EN derle'
bash scripts/derle_en.sh
grep -c "Font shape \`T1/times" paper/manuscript/main.log
grep -n -i -E 'No file T1times|t1times.fd|T1times.fd' paper/manuscript/main.log | head -3
echo '=== dizgi denetimi'
docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py paper/manuscript/main.pdf paper/manuscript/main.log --ayrinti 2>&1 | tail -25
