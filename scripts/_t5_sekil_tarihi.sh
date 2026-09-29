#!/usr/bin/env bash
# Makaledeki sekil sayisinin TARIHI: hangi commit'te kac \includegraphics vardi,
# hangi dosyalar girip cikti; mimari/genel-bakis sekli hic oldu mu.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
echo "=== EN makale: commit basina sekil sayisi ve dosya adlari ==="
for c in $(git log --format=%h --reverse -- paper/manuscript/sections/04_experiments.tex | awk 'NR%6==1' ) ad0ecbe 68b8067 1170366 d747060 675bedd 414590a; do
    n=$(git show "$c:paper/manuscript/sections/04_experiments.tex" 2>/dev/null | grep -c 'includegraphics')
    t=$(git log -1 --format=%ad --date=short "$c")
    printf '%s %s  %2d sekil: ' "$c" "$t" "$n"
    git show "$c:paper/manuscript/sections/04_experiments.tex" 2>/dev/null \
        | grep -o 'includegraphics[^{]*{[^}]*}' | sed 's/.*\///; s/}//' | tr '\n' ' '
    echo
done
echo
echo "=== Tum tarih boyunca EN makalede gecen sekil dosyalari (birlesik) ==="
git log --format=%h -- paper/manuscript/sections/*.tex paper/manuscript/main.tex \
  | while read -r c; do git show "$c:paper/manuscript/sections/04_experiments.tex" 2>/dev/null \
      | grep -o 'includegraphics[^{]*{[^}]*}' | sed 's/.*\///; s/}//'; done | sort | uniq -c | sort -rn
echo
echo "=== mimari / genel bakis / pipeline adli sekil hic girmis mi (tum depo tarihi) ==="
git log --all --format=%h -- 'paper/**/*.tex' | while read -r c; do
    git show "$c" --name-only --format= 2>/dev/null; done | sort -u | grep -iE 'overview|architect|pipeline|mimari|genel' || echo "  (tex degisikliklerinde boyle bir dosya yok)"
git log --all --format=%h --diff-filter=A -- 'paper/figures/**' | while read -r c; do git show "$c" --name-only --format=; done \
  | grep -iE 'overview|architect|pipeline|mimari|genel|b0' | sort -u | sed 's/^/  eklenen: /'
echo
echo "=== simdiki durum ==="
printf 'EN makale sekil: '; grep -c 'includegraphics' paper/manuscript/sections/*.tex | awk -F: '{s+=$2} END{print s}'
printf 'EN makale tablo: '; grep -c 'begin{table}' paper/manuscript/sections/*.tex | awk -F: '{s+=$2} END{print s}'
printf 'bildiri sekil  : '; grep -c 'includegraphics' paper/bildiri/bildiri.tex
printf 'arsivde        : '; ls paper/figures/arsiv/*.pdf 2>/dev/null | wc -l
echo "--- bildirideki sekiller ---"; grep -o 'includegraphics[^{]*{[^}]*}' paper/bildiri/bildiri.tex | sed 's/.*\///; s/}//'
echo "--- fig_b0_overview basligi (bildiri) ---"
grep -A3 'fig_b0_overview' paper/bildiri/bildiri.tex | grep -o 'caption{[^}]*' | cut -c1-300
