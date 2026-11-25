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
