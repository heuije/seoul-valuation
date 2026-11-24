import re, sys, json, time, subprocess, html, os, urllib.parse
OUT = sys.argv[1]
names = sys.argv[2:]
CA = "/root/.ccr/ca-bundle.crt"
def get(url, data=None):
    cmd = ["curl", "-s", "--cacert", CA, "--max-time", "60", url]
    if data:
        for k, v in data.items(): cmd += ["--data-urlencode", f"{k}={v}"]
    for i in range(3):
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0 and r.stdout: return r.stdout.decode("utf-8", "ignore")
        time.sleep(2)
    return ""
def to_text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", h)
    h = re.sub(r"(?i)</t[dh]>", " | ", h)
    h = re.sub(r"(?i)</tr>|<br\s*/?>|</p>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    return "\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in h.split("\n") if l.strip())
WANT = ["주요 제품", "매출 및 수주", "요약재무정보", "사업의 개요"]
res = {}
for n in names:
    s = get("https://dart.fss.or.kr/dsab007/detailSearch.ax", {"textCrpNm": n, "startDate": "20260101", "endDate": "20261124", "publicType": "A001", "maxResults": "50", "currentPage": "1"})
    rows = re.findall(r"(?s)<tr>(.*?)</tr>", s)
    pick = None
    for row in rows:
        t = re.sub(r"\s+", " ", to_text(row))
        m = re.search(r"rcpNo=(\d+)", row)
        if m and "사업보고서 (2025.12)" in t and "첨부정정" not in t:
            pick = (m.group(1), t.replace("\n", " "))
            break
    if not pick:
        res[n] = {"error": "no 2025 annual report", "rows": [to_text(r).replace("\n", " ")[:200] for r in rows][:5]}
        continue
    rcp = pick[0]
    m = get(f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp}")
    nodes = re.findall(r"node[12]\['text'\] = \"([^\"]*)\";\s*node[12]\['id'\] = \"[^\"]*\";\s*node[12]\['rcpNo'\] = \"(\d+)\";\s*node[12]\['dcmNo'\] = \"(\d+)\";\s*node[12]\['eleId'\] = \"(\d+)\";\s*node[12]\['offset'\] = \"(\d+)\";\s*node[12]\['length'\] = \"(\d+)\";\s*node[12]\['dtd'\] = \"([^\"]*)\"", m)
    if not nodes:
        # fallback: generic parse
        blocks = re.split(r"var node[12] = \{\};", m)
        nodes = []
        for b in blocks:
            g = lambda k: (re.search(r"\['%s'\] = \"([^\"]*)\"" % k, b) or [None, None])[1]
            if g("text") and g("dcmNo"):
                nodes.append((g("text"), rcp, g("dcmNo"), g("eleId"), g("offset"), g("length"), g("dtd")))
    info = {"rcpNo": rcp, "row": pick[1], "sections": {}}
    for (txt, rc, dcm, ele, off, ln, dtd) in nodes:
        if any(w in txt for w in WANT):
            u = f"https://dart.fss.or.kr/report/viewer.do?rcpNo={rcp}&dcmNo={dcm}&eleId={ele}&offset={off}&length={ln}&dtd={dtd}"
            body = to_text(get(u))
            fn = os.path.join(OUT, f"{n}__{ele}.txt")
            open(fn, "w").write(f"{txt}\n{u}\n\n{body}")
            info["sections"][txt] = fn
            time.sleep(0.5)
    res[n] = info
    time.sleep(1)
json.dump(res, open(os.path.join(OUT, "index.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v.get("rcpNo"), list(v.get("sections", {}).keys()) or v.get("error"), v.get("rows")) for k, v in res.items()}, ensure_ascii=False, indent=1))
