#!/usr/bin/env bash
# Salt okur: HEAD surumunun PDF sayfa sayisi ve kelime toplami.
cd /home/firat/projects/adeb_sci_1 || exit 1
git show HEAD:paper/manuscript/main.pdf > /tmp/eski.pdf
python3 -c "import pypdf;print('eski sayfa', len(pypdf.PdfReader('/tmp/eski.pdf').pages))"
rm -rf /tmp/eskims; mkdir -p /tmp/eskims/sections
git show HEAD:paper/manuscript/main.tex > /tmp/eskims/main.tex
for f in $(git ls-tree --name-only HEAD paper/manuscript/sections/); do
  git show "HEAD:$f" > "/tmp/eskims/sections/$(basename "$f")"
done
cat > /tmp/kelime_say.py <<'EOF'
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
echo "--- eski"; python3 /tmp/kelime_say.py /tmp/eskims
echo "--- yeni"; python3 /tmp/kelime_say.py /home/firat/projects/adeb_sci_1/paper/manuscript
