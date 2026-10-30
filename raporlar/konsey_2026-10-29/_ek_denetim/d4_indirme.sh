#!/bin/bash
O=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim
cd /mnt/d/adeb_sci_1_veri
echo "== sha256sum -c (bagimsiz) =="
time sha256sum -c indirme_sha256.txt > $O/d4_sha256_c.txt 2>&1; echo "rc=$?"
grep -c ': OK$' $O/d4_sha256_c.txt; grep -v ': OK$' $O/d4_sha256_c.txt
echo "== boyutlar =="
while read h f; do printf '%s\t%s\n' "$(stat -c %s "$f")" "$f"; done < indirme_sha256.txt | tee $O/d4_boyutlar.tsv | awk -F'\t' '{s+=$1} END {printf "toplam %.1f MB (1e6) / %.1f MiB\n", s/1e6, s/1048576}'
echo "== ImageNetV2 sayim =="
V=data/imagenetv2
ls $V
K=$(ls -d $V/*/ | head -1)
echo "kok: $K"
echo "sinif klasoru: $(find $K -mindepth 1 -maxdepth 1 -type d | wc -l)"
echo "dosya: $(find $K -mindepth 2 -type f | wc -l)"
echo "adlar 0-999 mi: $(find $K -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort -n | awk 'BEGIN{ok=1} {if ($1 != NR-1) ok=0} END{print ok, NR}')"
echo "klasor basina dosya dagilimi: $(for d in $K*/; do ls $d | wc -l; done | sort | uniq -c | tr '\n' ' ')"
echo "uzantilar: $(find $K -type f -printf '%f\n' | sed 's/.*\.//' | sort | uniq -c | tr '\n' ' ')"
du -sh $V 2>/dev/null
cat _indirme/imagenetv2_sayim.json 2>/dev/null | head -30
echo "== beyan boyutlari =="
cat /home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_indirme_boyutlari.txt | head -60
