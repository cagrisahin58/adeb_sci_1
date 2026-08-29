#!/usr/bin/env bash
# Bu revizyonun kelime dengesi + kaynakca durumu
cd /home/firat/projects/adeb_sci_1 || exit 1

echo "=== GOVDE KELIME DELTASI (HEAD -> calisma agaci) ==="
tot_o=0; tot_y=0
for f in paper/manuscript/sections/0*.tex; do
    o=$(git show "HEAD:$f" 2>/dev/null | wc -w)
    y=$(wc -w < "$f")
    tot_o=$((tot_o + o)); tot_y=$((tot_y + y))
    printf "  %-26s %6d -> %6d  (%+d)\n" "$(basename "$f")" "$o" "$y" "$((y - o))"
done
printf "  %-26s %6d -> %6d  (%+d)\n" "TOPLAM" "$tot_o" "$tot_y" "$((tot_y - tot_o))"

echo
echo "=== KAYNAKCA ==="
bib=paper/manuscript/references.bib
echo "  bib girdisi   : $(grep -c '^@' $bib)"
echo "  metinde anilan: $(grep -oh '\\cite[a-z]*{[^}]*}' paper/manuscript/sections/*.tex paper/manuscript/main.tex \
      | sed 's/.*{//; s/}//' | tr ',' '\n' | tr -d ' ' | sort -u | grep -c .)"
echo "  ANILMAYAN:"
comm -23 <(grep '^@' $bib | sed 's/.*{//; s/,.*//' | sort -u) \
         <(grep -oh '\\cite[a-z]*{[^}]*}' paper/manuscript/sections/*.tex paper/manuscript/main.tex \
           | sed 's/.*{//; s/}//' | tr ',' '\n' | tr -d ' ' | sort -u) | sed 's/^/    /'
