#!/usr/bin/env bash
# IS-6(h): KOKEN kutugunu TAM uretir.
#
# Neden sarmalayici gerekiyor: git ANA MAKINEDE var ama torch YOK;
# konteynerde torch var ama git YOK. Tek ortamda kosmak artefaktin
# yarisini bos birakiyordu (ve ilk surumde "git yok" durumu sessizce
# "calisma agaci temiz" gibi gorunuyordu -- duzeltildi).
#
# Bu betik git bilgisini ana makineden okur, ortam degiskeniyle
# konteynere gecirir; python tarafi ortam degiskenini oncelikli sayar.
set -u
cd "$(dirname "$0")/.." || exit 1

SHA="$(git rev-parse HEAD 2>/dev/null)"
if [ -z "$SHA" ]; then
    echo "UYARI: git okunamadi; koken kutugunde depo alanlari BILINMIYOR kalacak."
fi
KISA="$(git rev-parse --short HEAD 2>/dev/null)"
DAL="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
TARIH="$(git log -1 --format=%cI 2>/dev/null)"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then KIRLI=1; else KIRLI=0; fi

docker exec -w /workspace \
    -e KOKEN_GIT_SHA="$SHA" -e KOKEN_GIT_KISA="$KISA" -e KOKEN_GIT_DAL="$DAL" \
    -e KOKEN_GIT_TARIH="$TARIH" -e KOKEN_GIT_KIRLI="$KIRLI" \
    adeb_eval python -B scripts/q1_koken.py

# konteyner root olarak yazar (T6) -> sahipligi geri ver
docker exec adeb_eval chown 1000:1000 /workspace/results/q1/KOKEN.json 2>/dev/null

echo
echo "--- kutuk dogrulamasi ---"
python3 - <<'PY'
import json
from pathlib import Path
d = json.loads(Path("results/q1/KOKEN.json").read_text(encoding="utf-8"))
dep, rt = d["depo"], d["calisma_zamani"]
eksik = []
if not dep.get("git_okunabildi"):
    eksik.append("git bilgisi")
if not rt.get("torch"):
    eksik.append("torch surumu")
print(f"  git   : {dep.get('git_kisa')} ({dep.get('dal')}) kirli={dep.get('calisma_agaci_kirli_mi')}")
print(f"  torch : {rt.get('torch')}  cuda {rt.get('cuda')}  gpu {rt.get('gpu')}")
print(f"  artefakt: {len(d['artefaktlar'])} kayitli, {len(d['eksik_artefaktlar'])} eksik")
print("  SONUC:", "TAM" if not eksik else "EKSIK -> " + ", ".join(eksik))
PY
