import re, sys, os, zipfile
from openpyxl import load_workbook
SRC, CALC, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
vals = load_workbook(CALC, data_only=True)
wbx = open(os.path.join(SRC, "xl/workbook.xml"), encoding="utf-8").read()
rels = open(os.path.join(SRC, "xl/_rels/workbook.xml.rels"), encoding="utf-8").read()
rid = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="worksheets/([^"]+)"', rels)) or {}
rid.update({a: b for b, a in re.findall(r'Target="worksheets/([^"]+)"[^>]*Id="(rId\d+)"', rels)})
n = 0
for name, r in re.findall(r'<sheet name="([^"]+)" sheetId="\d+" r:id="(rId\d+)"/>', wbx):
    if name not in ("요약", "매출Breakdown", "검증 내역"): continue
    p = os.path.join(SRC, "xl/worksheets", rid[r]); s = open(p, encoding="utf-8").read(); ws = vals[name]
    def fix(m):
        global n
        c = m.group(0); ref = m.group(1)
        if "<f" not in c: return c
        v = ws[ref].value
        head = re.match(r"<c [^>]*>", c).group(0)
        head2 = re.sub(r' t="[^"]*"', "", head)
        body = re.sub(r"<v>.*?</v>", "", c[len(head):-4])
        if v is None: return head2 + body + "</c>"
        n += 1
        if isinstance(v, str):
            from xml.sax.saxutils import escape
            return head2[:-1] + ' t="str">' + body + f"<v>{escape(v)}</v></c>"
        if isinstance(v, bool): return head2[:-1] + ' t="b">' + body + f"<v>{int(v)}</v></c>"
        return head2 + body + f"<v>{repr(float(v)) if isinstance(v, float) else v}</v></c>"
    s = re.sub(r'<c r="([A-Z]+\d+)"(?:\s[^>]*?)?(?<!/)>(?:(?!</c>|<c ).)*?<f[^>]*?(?:/>|>.*?</f>)(?:(?!</c>|<c ).)*</c>', fix, s, flags=re.S)
    open(p, "w", encoding="utf-8").write(s)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    order = ["[Content_Types].xml"]
    for root, _, files in os.walk(SRC):
        for f in files:
            arc = os.path.relpath(os.path.join(root, f), SRC).replace(os.sep, "/")
            if arc not in order: order.append(arc)
    for arc in order: z.write(os.path.join(SRC, arc), arc)
print("cached values set:", n)
