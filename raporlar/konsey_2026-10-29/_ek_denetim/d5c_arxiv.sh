#!/bin/bash
O=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis
cd $O
sleep 15
curl -sL "https://export.arxiv.org/api/query?id_list=1902.10811,2210.07540,2303.01870,2302.14301" -o a_toplu.xml
tr '\n' ' ' < a_toplu.xml | grep -o '<entry>.*' | sed 's/<entry>/\n<entry>/g' | while read e; do
  [ -z "$e" ] && continue
  id=$(echo "$e" | grep -o '<id>[^<]*</id>' | head -1 | sed 's/<[^>]*>//g')
  t=$(echo "$e" | grep -o '<title>[^<]*</title>' | head -1 | sed 's/<[^>]*>//g' | tr -s ' ')
  n=$(echo "$e" | grep -o '<name>[^<]*</name>' | head -3 | sed 's/<[^>]*>//g' | tr '\n' ';')
  echo "$id | $t | $n"
done
