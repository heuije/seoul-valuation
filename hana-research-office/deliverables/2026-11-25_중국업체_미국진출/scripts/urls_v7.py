import sys, os, re, math, importlib.util
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import Alignment
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
wb=load_workbook(sys.argv[1]); sh=wb['출처']
FIX={"S2":("WOOD TV8","https://www.woodtv.com/news/michigan/state-board-tables-approval-of-gotion-settlement-framework/"),
     "S118":("하원 중국특위·세입위","https://chinaselectcommittee.house.gov/media/press-releases/gallagher-smith-rodgers-seek-compliance-after-ford-refuses-cooperate")}
url={}
for r in range(4,sh.max_row+1):
    k=sh.cell(r,2).value
    if k in FIX:
        sh.cell(r,3).value=FIX[k][0]; sh.cell(r,6).value=FIX[k][1]; sh.cell(r,6).hyperlink=FIX[k][1]
    url[k]=sh.cell(r,6).value
# 1) 본문 시트 출처 칸: 'S코드 발행처 날짜' → 기사 주소 그대로
W={'미국 진출 현황':50.875,'Ford-CATL':40,'주요 규제':40}
for n,w in W.items():
    ws=wb[n]; ws.column_dimensions[{'미국 진출 현황':'H','Ford-CATL':'E','주요 규제':'D'}[n]].width=w
    for row in ws.iter_rows():
        for c in row:
            if c.hyperlink:
                k=str(c.value).split()[0]; u=url[k]
                c.value=u; c.hyperlink=u
                al=copy(c.alignment); c.alignment=Alignment(horizontal=al.horizontal, vertical=al.vertical, wrap_text=True)
                need=14*B.est_lines(u,w)+4
                if (ws.row_dimensions[c.row].height or 15)<need: ws.row_dimensions[c.row].height=need
# 2) 출처 시트: 코드 열 삭제(왼쪽으로 이동)
for r in range(1,sh.max_row+1):
    for c in range(2,7):
        a,b=sh.cell(r,c),sh.cell(r,c+1)
        a.value=b.value; a.font=copy(b.font); a.alignment=copy(b.alignment); a.border=copy(b.border); a.fill=copy(b.fill)
        a.hyperlink=b.hyperlink.target if b.hyperlink else None
    g=sh.cell(r,7); g.value=None; g.hyperlink=None; g.border=copy(sh.cell(r,8).border); g.fill=copy(sh.cell(r,8).fill)
for col,w in zip("BCDEF",(24,60,12,70,18)): sh.column_dimensions[col].width=w
if 'G' in sh.column_dimensions: del sh.column_dimensions['G']
sh['B2'].value=sh['B2'].value  # 제목 유지
# 3) 수정내역 근거 열: 코드 → 주소
cl=wb['수정내역']
for r in range(4,cl.max_row+1):
    v=cl.cell(r,10).value
    if isinstance(v,str) and re.match(r'S\d+ ',v):
        cl.cell(r,10).value="\n".join(url[l.split()[0]] for l in v.split("\n"))
    elif isinstance(v,str) and v.startswith('S154~S166'):
        cl.cell(r,10).value="출처 시트 마지막 13건"
    h=cl.cell(r,8).value
    if isinstance(h,str) and '(기존 S1~S153 번호 유지)' in h: cl.cell(r,8).value=h.replace('(기존 S1~S153 번호 유지)','')
    vals=[cl.cell(r,c).value for c in range(3,11)]
    if any(vals):
        need=max(B.est_lines(v,{3:13,4:12,5:11,6:12,7:48,8:56,9:44,10:30}[c]) for c,v in zip(range(3,11),vals) if v)
        cl.row_dimensions[r].height=max(cl.row_dimensions[r].height or 15, 16*need+8)
for w_ in wb:
    for row in w_.iter_rows():
        for c in row:
            if c.value is not None: B.apply_font(c)
wb.save(sys.argv[2])
