#!/usr/bin/env bash
# E6 (L2) on kaydinin tarihi, L2 sonuclarinin tarihinden ONCE mi?
cd /home/firat/projects/adeb_sci_1 || exit 1
echo "E6 on kaydi ilk commit:"
git log --diff-filter=A --format='   %ai  %h' -- results/q1_research/E6_ON_KAYIT.md | tail -1
echo
echo "L2 artefaktlarinin ILK commit'leri:"
find results -path '*cifar10_l2*' -name '*.json' -not -path '*_b2_gerileme*' \
  | sort | head -8 | while IFS= read -r f; do
    printf '   %-58s %s\n' "$(basename "$f")" \
      "$(git log --diff-filter=A --format='%ai %h' -- "$f" | tail -1)"
done
echo
echo "E6 on kaydinda kayitli ongoruler (tam metin):"
sed -n '/Kayıtlı ön-kestirim/,/^## 3/p' results/q1_research/E6_ON_KAYIT.md | head -30
