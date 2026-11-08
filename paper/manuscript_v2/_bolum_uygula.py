#!/usr/bin/env python3
"""Apply the three v2 changes to the copied sections: figure paths, figure captions and the listed body-text
position words (nothing else).

    python3 _bolum_uygula.py            (run from paper/manuscript_v2 by derle_v2.sh)

1. every `../figures/fig` becomes `../figures_v2/fig` inside \\includegraphics;
2. every \\caption{...} of a figure environment whose \\label{fig:...} is in altyazilar_v2.tex is replaced by the
   v2 caption of that label (brace-balanced match).
3. every row of govde_duzeltmeler_v2.tsv (file, old, new, reason) replaces one body-text phrase that names a
   position in a v1 figure which the v2 figure no longer has (second round, 08.11.2026, bulgu 6); the old phrase
   must occur exactly once in its file, otherwise the build stops.
A label without a v2 caption, or a v2 caption whose label is not found, stops the build. Outside the listed
phrases the body text is not touched; main_v2.tex is generated from ../manuscript/main.tex with only its input
paths changed. Only the copies under paper/manuscript_v2/sections are written, never ../manuscript.
"""
import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def balanced(s, i):
    """Index after the brace group that opens at s[i] == '{'."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{" and (j == 0 or s[j - 1] != "\\"):
            depth += 1
        elif s[j] == "}" and s[j - 1] != "\\":
            depth -= 1
            if depth == 0:
                return j + 1
    raise SystemExit("unbalanced braces")


def captions():
    t = (HERE / "altyazilar_v2.tex").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"\\altyazi\{(fig:[a-z_]+)\}", t):
        a = m.end()
        b = balanced(t, a)
        out[m.group(1)] = t[a + 1:b - 1]
    return out


def body_fixes():
    """Rows of govde_duzeltmeler_v2.tsv as {file: [(old, new), ...]}."""
    out = {}
    tsv = HERE / "govde_duzeltmeler_v2.tsv"
    if not tsv.is_file():
        return out
    for ln in tsv.read_text(encoding="utf-8").splitlines()[1:]:
        if not ln.strip():
            continue
        f, old, new = ln.split("\t")[:3]
        out.setdefault(f, []).append((old, new))
    return out


def main():
    caps = captions()
    fixes = body_fixes()
    used = set()
    n_fix = 0
    for p in sorted((HERE / "sections").glob("*.tex")):
        t = p.read_text(encoding="utf-8")
        for old, new in fixes.get(p.name, []):
            k = t.count(old)
            if k != 1:
                sys.exit(f"{p.name}: body phrase found {k} times (needs exactly 1): {old}")
            t = t.replace(old, new)
            n_fix += 1
        n_path = t.count("{../figures/fig")
        t = t.replace("{../figures/fig", "{../figures_v2/fig")
        res, pos = [], 0
        for m in re.finditer(r"\\begin\{figure\*?\}", t):
            if m.start() < pos:
                continue
            end = t.index("\\end{figure", m.end())
            block = t[m.start():end]
            lab = re.search(r"\\label\{(fig:[a-z_]+)\}", block)
            ci = block.find("\\caption{")
            if lab and ci >= 0:
                if lab.group(1) not in caps:
                    sys.exit(f"{p.name}: {lab.group(1)} has no v2 caption")
                a = ci + len("\\caption")
                b = balanced(block, a)
                block = block[:a] + "{" + caps[lab.group(1)] + "}" + block[b:]
                used.add(lab.group(1))
            res.append(t[pos:m.start()] + block)
            pos = end
        res.append(t[pos:])
        t2 = "".join(res)
        io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
        print(f"{p.name}: {n_path} figure path(s) rewritten")
    missing = set(caps) - used
    if missing:
        sys.exit(f"v2 captions without a figure: {sorted(missing)}")
    print("captions replaced:", len(used))
    n_rows = sum(len(v) for v in fixes.values())
    if n_fix != n_rows:
        sys.exit(f"body fixes applied {n_fix} of {n_rows}")
    print("body phrases replaced:", n_fix)


if __name__ == "__main__":
    main()
