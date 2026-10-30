#!/bin/bash
O=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim/dis
cd $O
for id in 2307.07873 1902.10811 1809.02861 2210.07540 2303.01870 2302.14301; do
  curl -sL "https://export.arxiv.org/api/query?id_list=$id" -o a_$id.xml
  t=$(tr '\n' ' ' < a_$id.xml | grep -o '<entry>.*</entry>' | grep -o '<title>[^<]*</title>' | head -1 | sed 's/<[^>]*>//g' | tr -s ' ')
  n=$(tr '\n' ' ' < a_$id.xml | grep -o '<name>[^<]*</name>' | sed 's/<[^>]*>//g' | tr '\n' ';')
  echo "$id | $t | $n"
  sleep 4
done
ls -la a_2307.07873.xml; head -c 300 a_2307.07873.xml
