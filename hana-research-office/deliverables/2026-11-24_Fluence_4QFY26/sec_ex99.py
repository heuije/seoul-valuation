import re, sys, time, subprocess, html, os
OUT = sys.argv[1]; items = sys.argv[2:]
UA = "Mozilla/5.0 (compatible; research-script)"
CA = "/root/.ccr/ca-bundle.crt"
def get(u):
    for i in range(3):
        r = subprocess.run(["curl", "-s", "-A", UA, "--cacert", CA, "--max-time", "60", u], capture_output=True)
        if r.returncode == 0 and r.stdout and b"File Unavailable" not in r.stdout[:3000]:
            return r.stdout.decode("utf-8", "ignore")
        time.sleep(3)
    return ""
def to_text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", h)
    h = re.sub(r"(?i)</t[dh]>", " | ", h)
    h = re.sub(r"(?i)</tr>|<br\s*/?>|</p>|</div>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h); h = html.unescape(h)
    return "\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in h.split("\n") if l.strip())
for it in items:
    tag, idx = it.split("=", 1)
    page = get(idx)
    links = re.findall(r'href="(/Archives/edgar/data/[^"]+\.htm)"[^<]*</a></td>\s*<td[^>]*>([^<]*)</td>', page)
    ex = [l for l, t in links if "99" in t] or [l for l, t in re.findall(r'href="(/Archives/edgar/data/[^"]+\.htm)"()', page) if "ex99" in l.lower() or "pressrel" in l.lower()]
    if not ex:
        print(tag, "NO EX99", len(page)); continue
    u = "https://www.sec.gov" + ex[0]
    h = get(u); time.sleep(1)
    open(os.path.join(OUT, tag + ".htm"), "w").write(h)
    open(os.path.join(OUT, tag + ".txt"), "w").write(u + "\n" + to_text(h))
    print(tag, u, len(h))
    time.sleep(1)
