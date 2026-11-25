import sys, os, math, importlib.util
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from copy import copy
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
wb=load_workbook(sys.argv[1]); fc=wb['Ford-CATL']
def span(r,c):
    for m in fc.merged_cells.ranges:
        if m.min_row==r and m.min_col==c: return m.max_row-m.min_row+1
    return 1
cmp_=[]; r=4
while fc.cell(r,2).value and fc.cell(r,2).value!='주요 일지':
    k=span(r,3); links=[fc.cell(x,5).hyperlink.target for x in range(r,r+k) if fc.cell(x,5).hyperlink]
    cmp_.append([fc.cell(r,2).value,fc.cell(r,3).value,fc.cell(r,4).value,links]); r+=k
while fc.cell(r,2).value!='주요 일지': r+=1
r+=2; tl=[]
while r<=fc.max_row:
    if fc.cell(r,2).value:
        k=span(r,3); links=[fc.cell(x,5).hyperlink.target for x in range(r,r+k) if fc.cell(x,5).hyperlink]
        tl.append([fc.cell(r,2).value,fc.cell(r,3).value,links]); r+=k
    else: r+=1
title=fc['B2'].value; cols=[fc.cell(3,c).value for c in (3,4)]
print('cmp',[x[0] for x in cmp_],'tl',len(tl))
STATUS=["가동 현황",
 "2026.11 기준 셀 생산 중(초기 단계)\n2026.11.18 첫 셀을 Louisville 공장(Fathom 프로토타입용)으로 출하\n2026.10 셀 생산 개시",
 "2026.11 기준 미가동(ESS 전환 공사 중)\n2026.10 전극 믹싱 시운전 완료, 2027년 말 가동 목표",
 ["https://www.fromtheroad.ford.com/us/en/articles/2026/ford-fathom-lfp-prismatic-battery-cells-ship",
  "https://www.ibtimes.com/ford-starts-ev-battery-cell-production-michigan-catl-3809933",
  "https://fortune.com/company/ford-motor/earnings/q3-2026/"]]
i=[x[0] for x in cmp_].index('소유 구조'); cmp_.insert(i+1,STATUS)
idx=wb.sheetnames.index('Ford-CATL'); wb.remove(fc); fc=wb.create_sheet('Ford-CATL',idx)
fc.sheet_view.showGridLines=False
w2={"A":2,"B":16,"C":50,"D":50,"E":40}
for k,w in w2.items(): fc.column_dimensions[k].width=w
t=fc.cell(2,2,title); t.font=Font(name=B.KR,size=12,bold=True)
S={}
def reg(links):
    for u in links: S[u]=dict(pub="",date="",url=u)
    return links
B.header(fc,3,["항목"]+cols+["출처"]); r=4
for item,a,b,links in cmp_:
    r=B.block(fc,r,[(2,item,dict(bold=True,h="center"),16),(3,a,{},50),(4,b,{},50)],5,reg(links),S,40)
r+=1; B.band(fc,r,"주요 일지",2,5); fc.row_dimensions[r].height=18; r+=1
B.header(fc,r,["시점","내용",None,"출처"]); fc.merge_cells(start_row=r,start_column=3,end_row=r,end_column=4); r+=1
for date,body,links in tl:
    k=max(1,len(links)); r0=r
    r=B.block(fc,r,[(2,date,dict(h="center"),16),(3,body,{},100)],5,reg(links),S,40,hmerge=(3,4))
    if k>1: fc.merge_cells(start_row=r0,start_column=2,end_row=r-1,end_column=2)
for row in fc.iter_rows():
    for c in row:
        if c.hyperlink:
            u=c.hyperlink.target; c.value=u; c.alignment=Alignment(horizontal="left",vertical="center",wrap_text=True)
            need=14*B.est_lines(u,40)+4
            if (fc.row_dimensions[c.row].height or 15)<need: fc.row_dimensions[c.row].height=need
fc.page_setup.orientation="landscape"; fc.page_setup.paperSize=fc.PAPERSIZE_A4
fc.sheet_properties.pageSetUpPr.fitToPage=True; fc.page_setup.fitToWidth=1; fc.page_setup.fitToHeight=0
for row in fc.iter_rows():
    for c in row:
        if c.value is not None: B.apply_font(c)
wb.active=0
wb.save(sys.argv[2])
