import re, sys, time, subprocess, os
OUT = sys.argv[1]; items = sys.argv[2:]
UA = "Mozilla/5.0 (compatible; research-script)"
def get(u, fn=None):
    for i in range(3):
        r = subprocess.run(["curl", "-s", "-A", UA, "--cacert", "/root/.ccr/ca-bundle.crt", "--max-time", "120", u], capture_output=True)
        if r.returncode == 0 and r.stdout and b"File Unavailable" not in r.stdout[:3000]:
            return r.stdout.decode("utf-8", "ignore")
        time.sleep(3)
    return ""
for it in items:
    tag, idx = it.split("=", 1)
    page = get(idx)
    m = re.search(r'href="/ix\?doc=(/Archives/edgar/data/[^"]+\.htm)"', page) or re.search(r'href="(/Archives/edgar/data/[^"]+flnc-\d+\.htm)"', page)
    if not m: print(tag, "no main doc"); continue
    h = get("https://www.sec.gov" + m.group(1))
    open(os.path.join(OUT, tag + ".htm"), "w").write(h)
    print(tag, m.group(1), len(h)); time.sleep(1)
