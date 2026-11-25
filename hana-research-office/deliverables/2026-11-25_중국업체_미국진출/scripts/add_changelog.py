"""빌드된 엑셀에 '수정내역' 시트 추가. 사용: python3 add_changelog.py data.json in.xlsx out.xlsx"""
import json, sys, os, importlib.util
from openpyxl import load_workbook
from openpyxl.styles import Font
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
B = load("build_us_entry"); fx2 = load("data_us_fix2")
data = json.load(open(sys.argv[1], encoding="utf-8")); km = data["keymap"]; S = data["sources"]
wb = load_workbook(sys.argv[2])

def find(sheet, phrase):
    hits = [c.coordinate for row in wb[sheet].iter_rows() for c in row if isinstance(c.value, str) and phrase in c.value]
    assert len(hits) == 1, (sheet, phrase, hits)
    return hits[0]

FALLBACK = {4: ("미국 진출 현황", "EVE 10%(이사 1석)"), 11: ("주요 규제", "FIE(비상장 기업)는")}
n_src = len(S); first_new = 154
rows = []
for i, (sheet, rv, cat, old, new, why, keys, phrase) in enumerate(fx2.CHANGELOG):
    if sheet == "출처":
        cell = f"B{first_new + 3}:G{n_src + 3}"
    else:
        sh, ph = FALLBACK.get(i, (sheet, phrase))
        cell = find(sh, ph)
    basis = "\n".join(f"{km[k]} {S[km[k]]['pub']}" for k in keys) if keys else f"S{first_new}~S{n_src}(출처 시트)"
    rows.append([sheet, cell, rv, cat, old, new, why, basis])
rows.append(["주요 규제·Ford-CATL", "주요 규제 C14 이하, Ford-CATL 35행 이하", "-", "행 위치 변경",
             "주요 규제: 실효적 통제 C7, MACR C10 / Ford-CATL: 규제 이슈 35~39행, 주요 일지 41행~",
             "주요 규제: 실효적 통제 C14, MACR C21(이하 항목 14행씩 아래로) / Ford-CATL: 규제 이슈 35~41행, 주요 일지 43행~",
             "출처를 하위행 하나에 한 건씩 링크로 두는 기존 구조를 유지하면서 근거 출처를 추가해 행 위치만 이동(내용 변경 없음)", "-"])

ws = wb.create_sheet("수정내역")
ws.sheet_view.showGridLines = False
w = {"A": 2, "B": 5, "C": 13, "D": 12, "E": 11, "F": 12, "G": 48, "H": 56, "I": 44, "J": 30}
for k, v in w.items(): ws.column_dimensions[k].width = v
t = ws.cell(2, 2, "외부 교차검증 반영 수정내역(2026.11.25)"); t.font = Font(name=B.KR, size=12, bold=True)
B.header(ws, 3, ["No", "시트", "셀(수정 후)", "검토의견 셀", "구분", "기존 내용(변경 부분)", "수정 내용", "수정 사유", "근거(출처 코드)"])
r = 4
for i, row in enumerate(rows, 1):
    B.put(ws, r, 2, i, h="center")
    for j, v in enumerate(row):
        B.put(ws, r, 3 + j, v, h="center" if j in (0, 1, 2, 3) else "left")
    need = max(B.est_lines(v, w["CDEFGHIJ"[j]]) for j, v in enumerate(row))
    ws.row_dimensions[r].height = max(18, 16 * need + 8)
    r += 1
ws.cell(r + 1, 2, "주: 셀 주소는 병합 범위의 좌상단 기준. 조문 원문(law.cornell.edu·govinfo.gov)은 이 환경에서 접속이 막혀 IRS 지침·로펌 해설로 교차 확인").font = Font(name=B.KR, size=10)
ws.page_setup.orientation = "landscape"; ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.sheet_properties.pageSetUpPr.fitToPage = True; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
for row in ws.iter_rows():
    for c in row:
        if c.value is not None: B.apply_font(c)
wb.save(sys.argv[3])
for row in rows: print(row[0], '|', row[1], '|', row[2], '|', row[3])
