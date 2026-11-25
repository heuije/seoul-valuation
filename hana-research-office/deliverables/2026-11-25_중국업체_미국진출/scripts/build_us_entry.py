"""중국 EV·셀메이커 미국 진출 현황 엑셀 빌더.
사용: python3 build_us_entry.py <data.json> <out.xlsx>
data.json 구조:
  main:  [{"band":..., "company":..., "type":..., "year":..., "content":..., "status":..., "note":..., "src":["S1",...]}]
  ford_cmp: {"cols":["Marshall ...","Kentucky ..."], "rows":[["항목","marshall","kentucky",["S1"]],...]}
  ford_tl:  [["2023.02.13","공통","내용",["S1"]],...]
  sources: {"S1":{"pub":..,"title":..,"date":..,"url":..,"check":..},...}
"""
import json, math, re, sys
from copy import copy
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

KR, EN = "맑은 고딕", "Arial"
HAN = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
LAT = re.compile(r"[A-Za-z0-9]")
HDR_FILL = PatternFill("solid", fgColor="006C64")
BAND_FILL = PatternFill("solid", fgColor="D9EDED")
THIN = Side(style="thin", color="000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
LINK_COLOR = "FF0000FF"


def split_runs(s):
    kinds = [True if HAN.match(ch) else (False if LAT.match(ch) else None) for ch in s]
    nxt = None
    for i in range(len(kinds) - 1, -1, -1):
        if kinds[i] is None:
            kinds[i] = nxt
        else:
            nxt = kinds[i]
    prev = None
    for i, k in enumerate(kinds):
        if k is None:
            kinds[i] = prev
        prev = kinds[i] if kinds[i] is not None else prev
    runs = []
    for ch, k in zip(s, kinds):
        k = bool(k)
        if runs and runs[-1][1] == k:
            runs[-1][0] += ch
        else:
            runs.append([ch, k])
    return runs


def apply_font(cell):
    v = cell.value
    if v is None:
        return
    f = copy(cell.font)
    if not isinstance(v, (str, CellRichText)):
        f.name = EN
        cell.font = f
        return
    s = str(v)
    has_kr = bool(HAN.search(s))
    f.name = KR if has_kr else EN
    cell.font = f
    runs = split_runs(s)
    if has_kr and len(runs) > 1:
        cell.value = CellRichText([TextBlock(InlineFont(rFont=KR if k else EN, sz=f.sz, b=f.b, i=f.i, u=f.u,
                                                        color=copy(f.color) if f.color else None), t) for t, k in runs])


def est_lines(text, width):
    if not text:
        return 1
    cap = max(width * 1.05, 4)
    n = 0
    for line in str(text).split("\n"):
        u = sum(1.8 if ord(ch) > 0x2E80 else 1.0 for ch in line)
        n += max(1, math.ceil(u / cap))
    return n


def put(ws, r, c, v, bold=False, h="left", wrap=True, fill=None, color="FF000000", link=None, underline=None):
    cell = ws.cell(r, c, v)
    cell.font = Font(name=KR, size=10, bold=bold, color=color, underline=underline)
    cell.alignment = Alignment(horizontal=h, vertical="center", wrap_text=wrap)
    cell.border = BORDER
    if fill:
        cell.fill = fill
    if link:
        cell.hyperlink = link
    return cell


def header(ws, r, labels, c0=2):
    for i, lab in enumerate(labels):
        put(ws, r, c0 + i, lab, bold=True, h="center", fill=HDR_FILL, color="FFFFFFFF")


def band(ws, r, text, c0, c1):
    for c in range(c0, c1 + 1):
        put(ws, r, c, text if c == c0 else None, bold=True, fill=BAND_FILL)
    ws.merge_cells(start_row=r, start_column=c0, end_row=r, end_column=c1)


def src_label(codes, S):
    lines = []
    for k in codes:
        s = S[k]
        lines.append(f"{k} {s['pub']} {s['date']}")
    return "\n".join(lines)


def build(data, out):
    S = data["sources"]
    wb = Workbook()

    # ---- 1. 메인 표
    ws = wb.active
    ws.title = "미국 진출 현황"
    ws.sheet_view.showGridLines = False
    widths = {"A": 2, "B": 14, "C": 10, "D": 9, "E": 52, "F": 52, "G": 40, "H": 24}
    for k, w in widths.items():
        ws.column_dimensions[k].width = w
    t = ws.cell(2, 2, "중국 EV·셀메이커 미국 진출 현황")
    t.font = Font(name=KR, size=12, bold=True)
    header(ws, 3, ["기업명", "구분", "연도", "진출 내용", "진행 현황", "비고", "출처"])
    r = 4
    cur_band = None
    groups = []  # (company, start, end)
    for row in data["main"]:
        if row["band"] != cur_band:
            band(ws, r, row["band"], 2, 8)
            ws.row_dimensions[r].height = 18
            cur_band = row["band"]
            r += 1
        put(ws, r, 2, row["company"], bold=True, h="center")
        put(ws, r, 3, row["type"], h="center")
        put(ws, r, 4, row["year"], h="center")
        put(ws, r, 5, row["content"])
        put(ws, r, 6, row["status"])
        put(ws, r, 7, row.get("note", ""))
        codes = row["src"]
        put(ws, r, 8, src_label(codes, S), color=LINK_COLOR, underline="single", link=S[codes[0]]["url"] if codes else None)
        lines = max(est_lines(row["content"], widths["E"]), est_lines(row["status"], widths["F"]),
                    est_lines(row.get("note", ""), widths["G"]), est_lines(src_label(codes, S), widths["H"]))
        ws.row_dimensions[r].height = max(18, 14 * lines + 4)
        if groups and groups[-1][0] == (row["band"], row["company"]) and groups[-1][2] == r - 1:
            groups[-1][2] = r
        else:
            groups.append([(row["band"], row["company"]), r, r])
        r += 1
    for (bd, comp), a, b in groups:
        if b > a:
            ws.merge_cells(start_row=a, start_column=2, end_row=b, end_column=2)
            # 구분도 같은 값이면 병합
            if len({ws.cell(x, 3).value for x in range(a, b + 1)}) == 1:
                ws.merge_cells(start_row=a, start_column=3, end_row=b, end_column=3)

    # ---- 2. Ford-CATL
    fc = wb.create_sheet("Ford-CATL")
    fc.sheet_view.showGridLines = False
    w2 = {"A": 2, "B": 16, "C": 50, "D": 50, "E": 24}
    for k, w in w2.items():
        fc.column_dimensions[k].width = w
    t = fc.cell(2, 2, "Ford-CATL 협력 현황")
    t.font = Font(name=KR, size=12, bold=True)
    cmp_ = data["ford_cmp"]
    header(fc, 3, ["항목"] + cmp_["cols"] + ["출처"])
    r = 4
    for item, a, b, codes in cmp_["rows"]:
        put(fc, r, 2, item, bold=True, h="center")
        put(fc, r, 3, a)
        put(fc, r, 4, b)
        put(fc, r, 5, src_label(codes, S), color=LINK_COLOR, underline="single", link=S[codes[0]]["url"] if codes else None)
        lines = max(est_lines(a, w2["C"]), est_lines(b, w2["D"]), est_lines(src_label(codes, S), w2["E"]))
        fc.row_dimensions[r].height = max(18, 14 * lines + 4)
        r += 1
    r += 1
    band(fc, r, "주요 일지", 2, 5)
    fc.row_dimensions[r].height = 18
    r += 1
    header(fc, r, ["시점", "내용", None, "출처"])
    fc.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
    r += 1
    for date, plant, text, codes in data["ford_tl"]:
        body = f"[{plant}] {text}" if plant else text
        put(fc, r, 2, date, h="center")
        put(fc, r, 3, body)
        put(fc, r, 4, None)
        fc.merge_cells(start_row=r, start_column=3, end_row=r, end_column=4)
        put(fc, r, 5, src_label(codes, S), color=LINK_COLOR, underline="single", link=S[codes[0]]["url"] if codes else None)
        lines = max(est_lines(body, w2["C"] + w2["D"]), est_lines(src_label(codes, S), w2["E"]))
        fc.row_dimensions[r].height = max(18, 14 * lines + 4)
        r += 1

    # ---- 3. 주요 규제
    pl = wb.create_sheet("주요 규제")
    pl.sheet_view.showGridLines = False
    w4 = {"A": 2, "B": 24, "C": 90, "D": 26}
    for k, w in w4.items():
        pl.column_dimensions[k].width = w
    t = pl.cell(2, 2, "중국계 기업 관련 미국 주요 규제")
    t.font = Font(name=KR, size=12, bold=True)
    header(pl, 3, ["항목", "내용", "출처"])
    r = 4
    for item, text, codes in data.get("policy", []):
        put(pl, r, 2, item, bold=True, h="center")
        put(pl, r, 3, text)
        put(pl, r, 4, src_label(codes, S), color=LINK_COLOR, underline="single", link=S[codes[0]]["url"] if codes else None)
        pl.row_dimensions[r].height = max(18, 14 * max(est_lines(text, w4["C"]), est_lines(item, w4["B"]), est_lines(src_label(codes, S), w4["D"])) + 4)
        r += 1

    # ---- 4. 출처
    sh = wb.create_sheet("출처")
    sh.sheet_view.showGridLines = False
    w3 = {"A": 2, "B": 7, "C": 24, "D": 60, "E": 12, "F": 70, "G": 18}
    for k, w in w3.items():
        sh.column_dimensions[k].width = w
    t = sh.cell(2, 2, "출처 목록")
    t.font = Font(name=KR, size=12, bold=True)
    header(sh, 3, ["코드", "발행처", "제목", "발행일", "링크", "확인 방법"])
    r = 4
    for k in sorted(S, key=lambda x: int(x[1:])):
        s = S[k]
        put(sh, r, 2, k, h="center", wrap=False)
        put(sh, r, 3, s["pub"])
        put(sh, r, 4, s["title"])
        put(sh, r, 5, s["date"], h="center", wrap=False)
        put(sh, r, 6, s["url"], color=LINK_COLOR, underline="single", link=s["url"], wrap=False)
        put(sh, r, 7, s["check"])
        sh.row_dimensions[r].height = max(18, 14 * max(est_lines(s["title"], w3["D"]), est_lines(s["pub"], w3["C"])) + 4)
        r += 1

    for wsx in wb.worksheets:
        wsx.page_setup.orientation = "landscape"
        wsx.page_setup.paperSize = wsx.PAPERSIZE_A4
        wsx.sheet_properties.pageSetUpPr.fitToPage = True
        wsx.page_setup.fitToWidth = 1
        wsx.page_setup.fitToHeight = 0
        for row in wsx.iter_rows():
            for c in row:
                if c.value is not None:
                    apply_font(c)
    wb.save(out)


if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
