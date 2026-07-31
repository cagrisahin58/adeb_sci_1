#!/bin/bash
# Calisma agacindaki takipsiz results/c1_seeds dosyalarini origin/main'deki
# blob'larla karsilastirir. Ciktida yalnizca FARKLI/EKSIK olanlar listelenir.
cd "$HOME/projects/adeb_sci_1" || exit 1
diffs=0
while IFS= read -r f; do
  if ! git cat-file -e "origin/main:$f" 2>/dev/null; then
    echo "EKSIK-ORIGIN: $f"
    diffs=$((diffs + 1))
    continue
  fi
  a=$(git hash-object "$f")
  b=$(git rev-parse "origin/main:$f")
  if [ "$a" != "$b" ]; then
    echo "FARKLI: $f"
    diffs=$((diffs + 1))
  fi
done < <(git ls-files --others --exclude-standard results/c1_seeds)
echo "FARK_SAYISI=$diffs"
