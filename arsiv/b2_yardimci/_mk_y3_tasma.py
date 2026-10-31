import re
# main.log icinde her Overfull satirini o anda acik olan sections/ dosyasina esler (kaba yigin takibi).
log = open("/home/firat/projects/adeb_sci_1/paper/manuscript/main.log", encoding="latin-1").read()
dosya = "main.tex"
for satir in log.split("\n"):
    for m in re.finditer(r"\(\./(sections/[\w]+\.tex)", satir):
        dosya = m.group(1)
    if "Overfull" in satir and "output is active" not in satir:
        print(dosya, "|", satir.strip()[:90])
