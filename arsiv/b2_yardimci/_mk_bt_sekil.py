import io, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
kok = "/home/firat/projects/adeb_sci_1/paper/manuscript/sections/"
pat = re.compile(
    r"\\IfFileExists\{(\.\./figures/konsey/(fig_[a-z_]+)\.pdf)\}\{%\n"
    r"(\\includegraphics\[[^\]]*\]\{[^}]*\})\}\{%\n"
    r"\\fbox\{\\parbox\{[^}]*\}\{\\centering Figure pending: [^}]*\}\}\}\n")
for ad in ["03_methodology.tex", "04_experiments.tex"]:
    p = kok + ad
    t = io.open(p, encoding="utf-8").read()
    def rep(m):
        pdf = "/home/firat/projects/adeb_sci_1/paper/figures/konsey/" + m.group(2) + ".pdf"
        if os.path.exists(pdf):
            print("degisti:", ad, m.group(2))
            return m.group(3) + "\n"
        print("KALDI:", ad, m.group(2))
        return m.group(0)
    t2 = pat.sub(rep, t)
    # BEKLIYOR yorumlari: PDF varsa sekil kaynagini gosteren yorumla degistir
    def rep2(m):
        isim = m.group(1)
        pdf = "/home/firat/projects/adeb_sci_1/paper/figures/konsey/" + isim + ".pdf"
        if os.path.exists(pdf):
            return "% Sekil: paper/figures/konsey/" + isim + ".py (kanit " + isim + ".kanit.json); taslak, visio-cizici turu bekliyor.\n"
        return m.group(0)
    t2 = re.sub(r"% BEKLIYOR: (fig_[a-z_]+)[^\n]*\n(?:% kopyasi\)[^\n]*\n)?", rep2, t2)
    io.open(p, "w", encoding="utf-8", newline="\n").write(t2)
