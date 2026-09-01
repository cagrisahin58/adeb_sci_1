#!/usr/bin/env bash
# FAZ 2.3: on kayit beyanlari kayitla tutuyor mu?
# Her on kayit dosyasinin ILK commit'i ve ilgili sonuc artefaktinin
# ilk commit'i yan yana konur. Sonuc, kayittan ONCE mi SONRA mi?
cd /home/firat/projects/adeb_sci_1 || exit 1

ilk() { git log --diff-filter=A --format='%ai  %h' -- "$1" | tail -1; }
son() { git log -1 --format='%ai  %h  %s' -- "$1"; }

echo "=================== ON KAYIT DOSYALARI ==================="
for f in results/q1_research/E3_YENIDEN_TASARIM.md \
         results/q1_research/E6_ON_KAYIT.md \
         results/q1_research/E2_ISTATISTIK_PROTOKOLU.md \
         results/q1_research/E1_PILOT_KAPISI.md \
         results/q1_research/E7_KOSUM_ONCESI_KONTROL.md; do
    [ -f "$f" ] || continue
    printf '%-46s\n' "$(basename "$f")"
    printf '   ilk : %s\n' "$(ilk "$f")"
    printf '   son : %s\n' "$(son "$f")"
    printf '   commit sayisi: %s\n' "$(git log --oneline -- "$f" | wc -l)"
done

echo
echo "=================== SONUC ARTEFAKTLARI ==================="
for f in results/q1/e6_l2_ozet.json results/q1/e1_cifar100_summary.json \
         results/q1/e7_svhn_summary.json results/q1/e3_asimetri_fit.json \
         results/q1/e3_asimetri_fit_svhnli.json; do
    [ -f "$f" ] || { echo "$(basename "$f")  YOK"; continue; }
    printf '%-40s ilk: %s\n' "$(basename "$f")" "$(ilk "$f")"
done

echo
echo "=================== L2 (E6) ONGORULERI ==================="
echo "E6_ON_KAYIT.md icindeki ongoru satirlari ve hangi commit'te eklendi:"
git log --format='%ai %h' --follow -p -- results/q1_research/E6_ON_KAYIT.md \
  | grep -E '^\+.*(ongoru|Ongoru|ONGORU|kestirim|tahmin|bekliyoruz|predict)' \
  | head -12
