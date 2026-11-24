import re, sys, json, time, subprocess, html, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT, IDX = sys.argv[1], sys.argv[2]
want = sys.argv[3].split(",")
names = sys.argv[4:]
CA = "/root/.ccr/ca-bundle.crt"
def get(url):
    for i in range(3):
        r = subprocess.run(["curl", "-s", "--cacert", CA, "--max-time", "90", url], capture_output=True)
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
idx = json.load(open(IDX))
for n in names:
    rcp = idx[n]["rcpNo"]
    m = get(f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp}")
    for b in re.split(r"var node[12] = \{\};", m):
        g = lambda k: (re.search(r"\['%s'\] = \"([^\"]*)\"" % k, b) or [None, None])[1]
        t = g("text")
        if t and g("dcmNo") and any(w in t for w in want):
            u = f"https://dart.fss.or.kr/report/viewer.do?rcpNo={rcp}&dcmNo={g('dcmNo')}&eleId={g('eleId')}&offset={g('offset')}&length={g('length')}&dtd={g('dtd')}"
            body = to_text(get(u))
            fn = os.path.join(OUT, f"{n}__{g('eleId')}.txt")
            open(fn, "w").write(f"{t}\n{u}\n\n{body}")
            print(n, t, fn, len(body))
            time.sleep(0.5)
