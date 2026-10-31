#!/bin/bash
cd /home/firat/projects/adeb_sci_1
ls -la paper/manuscript/macros_konsey.tex
python3 /tmp/kelime_say_y4.py paper/manuscript | grep -E "05_disc|04z|toplam"
cd paper/manuscript
for f in 05_discussion 04z_computational; do
  python3 ~/.claude/skills/ai-izi/ai_izi_tara.py sections/$f.tex 2>&1 | tail -8
done
grep -c $'—' sections/05_discussion.tex sections/04z_computational.tex
grep -n -- "---" sections/05_discussion.tex sections/04z_computational.tex | grep -v "^[^:]*:[0-9]*:%" | head
cd /home/firat/projects/adeb_sci_1
bash scripts/derle_en.sh > /tmp/y4_derle.log 2>&1; echo "derle rc=$?"
tail -15 /tmp/y4_derle.log
bash scripts/compile_check.sh > /tmp/y4_cc.log 2>&1; echo "cc rc=$?"
tail -25 /tmp/y4_cc.log
LOG=paper/manuscript/main.log
[ -f "$LOG" ] && grep -n "undefined\|multiply defined\|^! " "$LOG" | head -40
