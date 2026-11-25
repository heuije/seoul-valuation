"""데이터 모듈을 합쳐 출처 코드를 S1..Sn(첫 등장 순)으로 재번호하고 JSON으로 저장."""
import json, sys, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    p = os.path.join(HERE, name + ".py")
    if not os.path.exists(p):
        return None
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


cell = load("data_us_cell")
ev = load("data_us_ev")
main = list(cell.MAIN_CELL) + (list(ev.MAIN_EV) if ev else [])
policy = list(cell.POLICY_CELL) + (list(ev.POLICY_EV) if ev else [])

OPS = {
    ("Gotion", "2022.10"): "철회", ("Gotion", "2023.09"): "부분가동", ("Gotion", "2023.12"): "가동",
    ("Envision AESC", "2023.07"): "가동", ("Envision AESC", "2022.04"): "건설 중단", ("Envision AESC", "2022.12"): "건설 중단",
    ("EVE Energy\n(이브에너지)", "2023.09"): "연기", ("Hithium\n(하이시엄)", "2024.07"): "가동",
    ("CATL", "2023.02"): "-", ("CATL–Ford", "2023.02"): "시험생산", ("CATL–Ford", "2025.12"): "건설 중",
    ("CATL–Tesla", "2024.01"): "가동", ("CATL–GM", "2024.03"): "검토",
    ("Microvast", "2021"): "건설 중단", ("Canadian Solar\n(e-STORAGE)", "2024.11"): "연기",
    ("BYD", "2013.05"): "가동", ("BYD", "2024.05"): "보류", ("BYD", "2024.02"): "보류",
    ("Geely\n(Volvo)", "2015.05"): "가동", ("Geely\n(Polestar)", "2024.09"): "판매 중단",
    ("Geely\n(Zeekr·Lynk & Co)", "2026.01"): "보류", ("Geely\n(Lotus)", "2026.08"): "판매 중단",
    ("NIO", "2026.06"): "R&D 거점", ("XPeng", "2026.07"): "R&D 거점", ("Li Auto", "2025.12"): "R&D 거점",
    ("Leapmotor\n(Stellantis JV)", "2026.05"): "계획 없음", ("SAIC\n(MG)", "2017"): "R&D 거점",
    ("Great Wall Motor", "2013"): "철회", ("Chery", "2026.10"): "검토",
}
for r in main:
    r["op"] = OPS[(r["company"], r["year"])]
assert len(OPS) == len(main), (len(OPS), len(main))
src_all = dict(cell.SRC_CELL)
if ev:
    src_all.update(ev.SRC_EV)


# ---- 2026-11-25 출처 검증 반영
fx = load("data_us_fix")
import json as _json
_base = HERE
_s2k = _json.load(open(os.path.join(_base, "s2k.json")))
_ver = _json.load(open(os.path.join(_base, "verify.json"), encoding="utf-8"))
_k2s = {k: s for s, k in _s2k.items()}
src_all = {k: dict(v) for k, v in src_all.items()}
for k, v in src_all.items():
    s = _k2s.get(k)
    if s is None:
        continue
    r = _ver.get(s)
    if src_all[k]["url"].startswith("https://www.sec.gov") or k in fx.DIRECT_OK:
        v["check"] = fx.D
    elif r and r[1] in ("존재", "주소 수정"):
        v["check"] = fx.W
    else:
        v["check"] = "재검색 미확인"
for k, f in fx.URL_FIX.items():
    src_all[k].update(f)
for k, dt in fx.DATE_FIX.items():
    src_all[k]["date"] = dt
src_all.update(fx.NEW_SRC)

def _swap(codes, key=None):
    out = []
    for c in codes:
        for n in fx.SWAP.get(c, [c]):
            if n not in out:
                out.append(n)
    for n in fx.ADD.get(key, []):
        if n not in out:
            out.append(n)
    return out

_hits = {o: 0 for o, _ in fx.TEXT_FIX}
def _tx(t):
    if not isinstance(t, str):
        return t
    for o, n in fx.TEXT_FIX:
        if o in t:
            _hits[o] += 1
            t = t.replace(o, n)
    return t

main = [dict(r, src=_swap(r["src"], (r["company"], r["year"])), content=_tx(r["content"]), status=_tx(r["status"]), note=_tx(r.get("note", ""))) for r in main]
FORD_CMP = {"cols": cell.FORD_CMP["cols"], "rows": [[a, _tx(b), _tx(c), _swap(d)] for a, b, c, d in cell.FORD_CMP["rows"]]}
FORD_TL = [[a, b, _tx(c), _swap(d)] for a, b, c, d in cell.FORD_TL]
policy = [[a, _tx(b), _swap(c)] for a, b, c in policy]
_miss = [o[:40] for o, h in _hits.items() if h == 0]
assert not _miss, _miss
_left = sorted({c for r in main for c in r["src"]} | {c for r in FORD_CMP["rows"] for c in r[3]} | {c for r in FORD_TL for c in r[3]} | {c for r in policy for c in r[2]})
_bad = [c for c in _left if src_all[c]["check"] == "재검색 미확인"]
print("남은 미확인 출처:", _bad)

order = []
def see(codes):
    for c in codes:
        if c not in src_all:
            raise KeyError(f"출처 없음: {c}")
        if c not in order:
            order.append(c)

for r in main:
    see(r["src"])
for row in FORD_CMP["rows"]:
    see(row[3])
for row in FORD_TL:
    see(row[3])
for row in policy:
    see(row[2])

remap = {old: f"S{i+1}" for i, old in enumerate(order)}
def rm(codes):
    return [remap[c] for c in codes]

data = {
    "main": [dict(r, src=rm(r["src"])) for r in main],
    "ford_cmp": {"cols": FORD_CMP["cols"], "rows": [[a, b, c, rm(d)] for a, b, c, d in FORD_CMP["rows"]]},
    "ford_tl": [[a, b, c, rm(d)] for a, b, c, d in FORD_TL],
    "policy": [[a, b, rm(c)] for a, b, c in policy],
    "sources": {remap[k]: src_all[k] for k in order},
}
json.dump(data, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(data["main"]), "sources", len(data["sources"]), "unused", sorted(set(src_all) - set(order)))
