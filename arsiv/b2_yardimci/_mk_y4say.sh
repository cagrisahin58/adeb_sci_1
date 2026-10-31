#!/bin/bash
cd /home/firat/projects/adeb_sci_1
F=results/C1_REFERANS_FOYU.md
for r in 1669,1675 1789,1797; do
  echo "--- $r"
  sed -n "${r}p" "$F" | cut -c1-300
done
cat > /tmp/kelime_say_y4.py <<'EOF'
import re, glob, sys
kok = sys.argv[1] if len(sys.argv) > 1 else "."
tot = 0
for f in [kok + "/main.tex"] + sorted(glob.glob(kok + "/sections/*.tex")):
    t = open(f, encoding="utf-8").read()
    lines = [re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n")]
    n = len(" ".join(lines).split())
    tot += n
    print(n, f)
print(tot, "toplam (yorum satirlari haric)")
EOF
python3 /tmp/kelime_say_y4.py paper/manuscript
cd paper/manuscript
for f in 05_discussion 04z_computational; do
  echo "=== ai_izi $f"
  python3 ~/.claude/skills/ai-izi/ai_izi_tara.py sections/$f.tex 2>&1 | tail -40
done
grep -n "InputIfFileExists\|input{" main.tex
grep -n -o "rather than\|instead of\|, not [a-z]*" sections/05_discussion.tex sections/04z_computational.tex
