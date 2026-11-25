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
src_all = dict(cell.SRC_CELL)
if ev:
    src_all.update(ev.SRC_EV)

order = []
def see(codes):
    for c in codes:
        if c not in src_all:
            raise KeyError(f"출처 없음: {c}")
        if c not in order:
            order.append(c)

for r in main:
    see(r["src"])
for row in cell.FORD_CMP["rows"]:
    see(row[3])
for row in cell.FORD_TL:
    see(row[3])
for row in policy:
    see(row[2])

remap = {old: f"S{i+1}" for i, old in enumerate(order)}
def rm(codes):
    return [remap[c] for c in codes]

data = {
    "main": [dict(r, src=rm(r["src"])) for r in main],
    "ford_cmp": {"cols": cell.FORD_CMP["cols"], "rows": [[a, b, c, rm(d)] for a, b, c, d in cell.FORD_CMP["rows"]]},
    "ford_tl": [[a, b, c, rm(d)] for a, b, c, d in cell.FORD_TL],
    "policy": [[a, b, rm(c)] for a, b, c in policy],
    "sources": {remap[k]: src_all[k] for k in order},
}
json.dump(data, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(data["main"]), "sources", len(data["sources"]), "unused", sorted(set(src_all) - set(order)))
