#!/bin/bash
# IS 1, adim 1-4: 07_disk_D_plani.md §4 tarifi (31.10.2026)
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
R=raporlar/konsey_2026-10-29
ts() { echo "[$(date '+%F %T')] $*"; }

ts "0) zincir durumu"
tail -3 logs/konsey_zincir.log
column -t -s $'\t' results/q1/konsey_zincir_durum.tsv | tail -5

ts "1a) docker start adeb_eval"
docker start adeb_eval || { ts "HATA: start"; exit 1; }
docker top adeb_eval -eo pid,args

ts "1b) pip freeze ve inspect"
docker exec adeb_eval pip freeze > $R/adeb_eval_pip_freeze.txt; echo "pip freeze rc=$? satir=$(wc -l < $R/adeb_eval_pip_freeze.txt)"
docker inspect adeb_eval > $R/adeb_eval_inspect.json; echo "inspect rc=$? bayt=$(wc -c < $R/adeb_eval_inspect.json)"
grep -iE '^(timm|robustbench|autoattack|torch|click)==' $R/adeb_eval_pip_freeze.txt
echo "eski User=[$(docker inspect --format '{{.Config.User}}' adeb_eval)]"

ts "2) docker commit"
docker commit -m "adeb_eval: konteyner ici pip (timm 1.0.27, robustbench 1.1, autoattack 0.1, ...)" \
    adeb_eval adeb_eval:2026-10-30 || { ts "HATA: commit"; exit 1; }
docker images --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}' | grep adeb_eval

ts "3) rename + stop"
docker rename adeb_eval adeb_eval_eski || { ts "HATA: rename"; exit 1; }
docker stop adeb_eval_eski

ts "4) docker run"
mkdir -p /mnt/d/adeb_sci_1_veri
docker run -d --name adeb_eval \
    --gpus all --ipc=host --security-opt label=disable \
    -w /workspace \
    -v /home/firat/projects/adeb_sci_1:/workspace \
    -v /mnt/d/adeb_sci_1_veri:/mnt/d/adeb_sci_1_veri \
    -v /mnt/d/adeb_sci_1_veri:/veri \
    adeb_eval:2026-10-30 sleep infinity || { ts "HATA: run"; exit 1; }
sleep 3
docker ps -a --filter name=adeb_eval --format '{{.Names}}|{{.Status}}|{{.Image}}'
echo "yeni User=[$(docker inspect --format '{{.Config.User}}' adeb_eval)]"
docker inspect --format '{{json .Mounts}}' adeb_eval
ts "kurulum bitti"
