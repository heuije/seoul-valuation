"""모든 표 테두리 색 RGB(128,128,128), 표 가장 왼쪽 열의 왼쪽 선·가장 오른쪽 열의 오른쪽 선 제거."""
import sys
from openpyxl import load_workbook
from openpyxl.styles import Border, Side
wb=load_workbook(sys.argv[1], rich_text=True)
G="FF808080"
def side(s, keep=True):
    return Side(style=s.style, color=G) if (keep and s is not None and s.style) else Side(style=None)
for ws in wb:
    cols=[c.column for row in ws.iter_rows() for c in row if any(getattr(c.border,x).style for x in ('left','right','top','bottom'))]
    if not cols: continue
    c0,c1=min(cols),max(cols)
    for row in ws.iter_rows():
        for c in row:
            b=c.border
            if not any(getattr(b,x).style for x in ('left','right','top','bottom')): continue
            c.border=Border(left=side(b.left, c.column!=c0), right=side(b.right, c.column!=c1), top=side(b.top), bottom=side(b.bottom))
    for m in ws.merged_cells.ranges:  # 병합 범위는 좌상단 셀 테두리가 바깥선으로 복사되므로 좌상단에서 제거
        tl=ws.cell(m.min_row,m.min_col); b=tl.border
        tl.border=Border(left=side(b.left, m.min_col!=c0), right=side(b.right, m.max_col!=c1), top=side(b.top), bottom=side(b.bottom))
    print(ws.title, '표 열 범위', c0, c1)
wb.save(sys.argv[2])
