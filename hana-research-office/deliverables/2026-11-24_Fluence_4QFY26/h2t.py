import re, html, sys
h = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
h = re.sub(r"(?is)<(script|style).*?</\1>", "", h); h = re.sub(r"(?is)<ix:header>.*?</ix:header>", "", h)
h = re.sub(r"(?i)</t[dh]>", " | ", h); h = re.sub(r"(?i)</tr>|<br\s*/?>|</p>|</div>", "\n", h)
h = re.sub(r"<[^>]+>", "", h); h = html.unescape(h)
open(sys.argv[2], "w").write("\n".join(re.sub(r"[ \t\xa0]+", " ", l).strip() for l in h.split("\n") if l.strip()))
