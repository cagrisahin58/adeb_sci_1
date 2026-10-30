#!/bin/bash
O=/home/firat/projects/adeb_sci_1/raporlar/konsey_2026-10-29/_ek_denetim
mkdir -p $O/dis
cd $O/dis
echo "== arXiv 2307.07873 =="
curl -s "http://export.arxiv.org/api/query?id_list=2307.07873" -o arxiv_2307.07873.xml
grep -o '<title>[^<]*</title>' arxiv_2307.07873.xml | tail -1
grep -o '<name>[^<]*</name>' arxiv_2307.07873.xml | tr '\n' ' '; echo
grep -o '<arxiv:comment[^>]*>[^<]*' arxiv_2307.07873.xml | head -2
grep -o '<arxiv:doi[^>]*>[^<]*' arxiv_2307.07873.xml | head -2
echo "== Crossref 10.2307/2413122 =="
curl -s "https://api.crossref.org/works/10.2307/2413122" -o cr_2413122.json
python3 -c "import json;m=json.load(open('cr_2413122.json'))['message'];print(m.get('title'),[a.get('family') for a in m.get('author',[])],m.get('container-title'),m.get('volume'),m.get('issue'),m.get('page'),m.get('issued'))"
echo "== Crossref 10.1109/SP54263.2024.00010 =="
curl -s "https://api.crossref.org/works/10.1109/SP54263.2024.00010" -o cr_sp.json
python3 -c "import json;m=json.load(open('cr_sp.json'))['message'];print(m.get('title'),[a.get('family') for a in m.get('author',[])],m.get('container-title'))" 2>&1 | tail -1
echo "== diger arXiv kimlikleri =="
for id in 1902.10811 1809.02861 2210.07540 2303.01870 2302.14301; do
  curl -s "http://export.arxiv.org/api/query?id_list=$id" -o a_$id.xml
  echo "$id: $(grep -o '<title>[^<]*</title>' a_$id.xml | tail -1 | tr -s ' \n' ' ') | $(grep -o '<name>[^<]*</name>' a_$id.xml | head -3 | sed 's/<[^>]*>//g' | tr '\n' ';')"
  sleep 3
done
echo "== ARES yapilandirmalari =="
curl -sL https://raw.githubusercontent.com/thu-ml/ares/main/robust_training/train_configs/convnext_base.yaml -o ares_convnext_base.yaml
curl -sL https://raw.githubusercontent.com/thu-ml/ares/main/robust_training/train_configs/swin_base_patch4_window7_224.yaml -o ares_swin_base.yaml
curl -sL https://raw.githubusercontent.com/thu-ml/ares/main/robust_training/adversarial_training.py -o ares_at.py
sha256sum ares_convnext_base.yaml ares_swin_base.yaml
diff ares_convnext_base.yaml ares_swin_base.yaml
grep -n -i 'pretrain' ares_at.py ares_convnext_base.yaml ares_swin_base.yaml | head
sed -n 51p ares_at.py; sed -n 226p ares_at.py
echo "== Singh README =="
curl -sL https://raw.githubusercontent.com/nmndeep/revisiting-at/main/README.md -o singh_readme.md
sha256sum singh_readme.md
grep -n -i 'initializ\|clean model\|epoch' singh_readme.md | head -20
