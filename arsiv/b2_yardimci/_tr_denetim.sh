#!/usr/bin/env bash
# TR aynasi icin turkce-yazi denetimi (30.09.2026 kurali): detex -> metrik/kalip/yapi;
# HEAD'e gore degismez (cite/ref/label/sayi) karsilastirmasi; EN-TR cite coklukumesi farki.
set -u
ROOT=/home/firat/projects/adeb_sci_1
SK=/mnt/c/Users/cagri/.claude/skills/turkce-yazi/scripts
AI=/mnt/c/Users/cagri/.claude/skills/ai-izi/ai_izi_tara.py
OUT=$ROOT/raporlar/turkce_yazi_2026-09-30
mkdir -p "$OUT/duz" "$OUT/head_tr"
cd "$ROOT" || exit 1

echo "=== voice/ ve yazim kurali"
ls voice 2>/dev/null || echo "voice/ yok"
ls .claude/rules/yazim.md 2>/dev/null || echo ".claude/rules/yazim.md yok"

echo "=== duz metin"
for f in paper/manuscript_tr/sections/0?_*.tex; do
  b=$(basename "$f" .tex)
  if command -v detex >/dev/null 2>&1; then
    detex -l "$f" > "$OUT/duz/$b.txt"
  else
    python3 arsiv/b2_yardimci/_detex_basit.py "$f" "$OUT/duz/$b.txt"
  fi
  printf '%s: %s kelime\n' "$b" "$(wc -w < "$OUT/duz/$b.txt")"
done
command -v detex >/dev/null 2>&1 && echo "detex: var" || echo "detex: YOK, yedek indirgeyici kullanildi"

echo "=== kalip_tara (ozet satirlari)"
for t in "$OUT"/duz/*.txt; do
  b=$(basename "$t" .txt)
  python3 "$SK/kalip_tara.py" "$t" > "$OUT/kalip_$b.txt" 2>&1
  echo "--- $b"; tail -n 6 "$OUT/kalip_$b.txt"
done

echo "=== metrik (makale)"
for t in "$OUT"/duz/*.txt; do
  b=$(basename "$t" .txt)
  python3 "$SK/metrik.py" "$t" --tur makale > "$OUT/metrik_$b.txt" 2>&1
  echo "--- $b"; head -n 25 "$OUT/metrik_$b.txt"
done

echo "=== yapi (makale)"
for t in "$OUT"/duz/*.txt; do
  b=$(basename "$t" .txt)
  python3 "$SK/yapi.py" "$t" --tur makale > "$OUT/yapi_$b.txt" 2>&1
  echo "--- $b"; tail -n 12 "$OUT/yapi_$b.txt"
done

echo "=== degismezler: HEAD vs calisma kopyasi (TR)"
mkdir -p "$OUT/head_tr/sections"
for f in paper/manuscript_tr/sections/0?_*.tex; do
  git show "HEAD:$f" > "$OUT/head_tr/sections/$(basename "$f")"
done
git show HEAD:paper/manuscript_tr/main.tex > "$OUT/head_tr/main.tex"
( cd "$OUT/head_tr" && python3 "$AI" sections/01_giris.tex sections/02_ilgili_calismalar.tex sections/03_yontem.tex sections/04_deneyler.tex sections/05_tartisma.tex sections/06_sonuc.tex main.tex --json > "$OUT/tr_head.json" )
( cd paper/manuscript_tr && python3 "$AI" sections/01_giris.tex sections/02_ilgili_calismalar.tex sections/03_yontem.tex sections/04_deneyler.tex sections/05_tartisma.tex sections/06_sonuc.tex main.tex --json > "$OUT/tr_simdi.json" )
python3 "$AI" --karsilastir "$OUT/tr_head.json" "$OUT/tr_simdi.json" > "$OUT/tr_degismez_fark.txt" 2>&1
sed -n '1,120p' "$OUT/tr_degismez_fark.txt"

echo "=== EN-TR cite coklukumesi farki"
grep -o -h -E '\\cite\{[^}]*\}' paper/manuscript/sections/0?_*.tex paper/manuscript/main.tex | tr -d ' ' | tr ',' '\n' | sed -E 's/\\cite\{//; s/\}//' | sort | uniq -c | sort -k2 > "$OUT/en_cite.txt"
grep -o -h -E '\\cite\{[^}]*\}' paper/manuscript_tr/sections/0?_*.tex paper/manuscript_tr/main.tex | tr -d ' ' | tr ',' '\n' | sed -E 's/\\cite\{//; s/\}//' | sort | uniq -c | sort -k2 > "$OUT/tr_cite.txt"
diff "$OUT/en_cite.txt" "$OUT/tr_cite.txt" && echo "cite coklukumesi AYNI"
echo "=== EN-TR ref coklukumesi farki"
grep -o -h -E '\\(ref|eqref)\{[^}]*\}' paper/manuscript/sections/0?_*.tex | sort | uniq -c > "$OUT/en_ref.txt"
grep -o -h -E '\\(ref|eqref)\{[^}]*\}' paper/manuscript_tr/sections/0?_*.tex | sort | uniq -c > "$OUT/tr_ref.txt"
diff "$OUT/en_ref.txt" "$OUT/tr_ref.txt" && echo "ref coklukumesi AYNI"
