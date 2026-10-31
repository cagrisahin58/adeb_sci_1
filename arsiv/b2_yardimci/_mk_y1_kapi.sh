#!/bin/bash
# Y1: KALAN kapilar, yasak dizgelerin yeri ve ai_izi sayaci. Salt okur.
cd /home/firat/projects/adeb_sci_1 || exit 1
docker exec -w /workspace adeb_eval python scripts/check_manuscript_claims.py 2>&1 | grep -E 'KALDI'
echo "== yasak dizgeler =="
grep -n -i -E 'all three predictions|three sources of variance|almost perfectly explained' paper/manuscript/main.tex paper/manuscript/sections/*.tex
echo "== Y1 dosyalarinda uzun tire / paragraph / itemize =="
grep -n -E -- '---|—|\\paragraph|\\begin\{(itemize|enumerate)\}' paper/manuscript/main.tex paper/manuscript/sections/01_introduction.tex paper/manuscript/sections/06_conclusion.tex
cd paper/manuscript
for f in sections/01_introduction.tex sections/06_conclusion.tex main.tex; do
  echo "== ai_izi $f"
  python3 "$HOME/.claude/skills/ai-izi/ai_izi_tara.py" "$f" 2>&1 | tail -40
done
