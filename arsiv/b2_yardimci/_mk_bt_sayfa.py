import re, sys
for p in sys.argv[1:]:
    b = open(p, "rb").read()
    n = len(re.findall(rb"/Type\s*/Page[^s]", b))
    m = re.findall(rb"/Count\s+(\d+)", b)
    print(p, "sayfa(Type/Page):", n, "Count:", m[:3])
