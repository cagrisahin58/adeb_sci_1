"""Salt okur: on kayit govdesinin SHA-256 ozeti (Dondurma eki (b) tanimi) ve FOY'de AutoAttack / M9 satirlari."""
import hashlib
import sys

sys.stdout.reconfigure(encoding="utf-8")
yol = "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md"
b = open(yol, "rb").read()
isaret = b"\n## Dondurma eki\n"
i = b.index(isaret)
govde = b[: i + 1]
print("govde_sha256", hashlib.sha256(govde).hexdigest())
print("beklenen     46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5")

foy = open("results/C1_REFERANS_FOYU.md", encoding="utf-8").read().splitlines()
for n, s in enumerate(foy, 1):
    t = s.lower()
    if ("autoattack" in t or " aa " in t or "m9" in t or "konsey" in t) and len(s) < 400:
        print(n, s[:300])
