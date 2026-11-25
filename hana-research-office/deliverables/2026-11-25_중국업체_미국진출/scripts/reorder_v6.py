import sys, os, importlib.util, re
from openpyxl import load_workbook
from openpyxl.styles import Font
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
wb=load_workbook(sys.argv[1]); ws=wb['미국 진출 현황']
BANDMAP={"셀메이커 — 직접 투자·JV":"셀메이커","셀메이커 — 중국계 경계 사례":"셀메이커","셀메이커 — 라이선스·기술 협력":"라이선스·기술 협력","EV(완성차)":"EV"}
def span(r,c):
    for m in ws.merged_cells.ranges:
        if m.min_row==r and m.min_col==c: return m.max_row-m.min_row+1
    return 1
rows=[]; band=None; comp=typ=None
r=4
while r<=ws.max_row:
    d=ws.cell(r,4).value; b2=ws.cell(r,2).value
    if d is None and b2 in BANDMAP: band=BANDMAP[b2]; r+=1; continue
    if d is None: r+=1; continue
    if b2: comp=b2
    if ws.cell(r,3).value: typ=ws.cell(r,3).value
    k=span(r,5)
    srcs=[(ws.cell(x,8).value, ws.cell(x,8).hyperlink.target) for x in range(r,r+k) if ws.cell(x,8).value and ws.cell(x,8).hyperlink]
    rows.append(dict(band=band,company=comp,type=typ,year=str(d),content=ws.cell(r,5).value,op=ws.cell(r,6).value,status=ws.cell(r,7).value,src=srcs))
    r+=k
assert len(rows)==28, len(rows)
# 문구 수정
for x in rows:
    if x['company']=='Great Wall Motor':
        x['status']=x['status'].replace("2026.02 멕시코 COMPAS 공장 인수 응찰 보도","2026.02 닛산-벤츠 멕시코 COMPAS 공장(연 약 23만대) 인수전 참여 보도(BYD·Chery와 경쟁), 결과 미확인")
        assert '응찰' not in x['status']
    if x['company']=='Microvast': x['content']="미국(텍사스) 본사·나스닥 상장, 생산 기반은 중국\n"+x['content']
    if str(x['company']).startswith('Canadian Solar'): x['content']="캐나다 본사, 자회사 CSI Solar가 중국 상장·생산 기반\n"+x['content']
def key(x):
    y=x['year']; m=re.match(r'(\d{4})(?:\.(\d{2}))?',y); return (int(m.group(1)), int(m.group(2) or 0))
order=["셀메이커","라이선스·기술 협력","EV"]
rows.sort(key=lambda x:(order.index(x['band']),key(x),x['company']))
title=ws['B2'].value; idx=wb.sheetnames.index('미국 진출 현황')
wb.remove(ws); ws=wb.create_sheet('미국 진출 현황',idx); wb.active=idx
ws.sheet_view.showGridLines=False
widths={"A":2,"B":14,"C":10,"D":9,"E":52,"F":8.625,"G":52,"H":50.875}
for k,w in widths.items(): ws.column_dimensions[k].width=w
t=ws.cell(2,2,title); t.font=Font(name=B.KR,size=11,bold=True)
B.header(ws,3,["기업명","구분","발표일","진출 내용","운영 상태","진행 현황 상세","출처"])
S={}
r=4; cur=None; groups=[]
for x in rows:
    if x['band']!=cur:
        B.band(ws,r,x['band'],2,8); ws.row_dimensions[r].height=18; cur=x['band']; r+=1
    codes=[]
    for lab,url in x['src']:
        c=lab.split()[0]; S[c]=dict(pub=lab.split(' ',1)[1].rsplit(' ',1)[0], date=lab.rsplit(' ',1)[1], url=url); codes.append(c)
    start=r
    cells=[(2,x['company'],dict(bold=True,h="center"),14),(3,x['type'],dict(h="center"),10),(4,x['year'],dict(h="center"),9),
           (5,x['content'],{},52),(6,x['op'],dict(h="center"),8.625),(7,x['status'],{},52)]
    r=B.block(ws,r,cells,8,codes,S,50.875)
    keyg=(x['band'],x['company'])
    if groups and groups[-1][0]==keyg and groups[-1][2]==start-1: groups[-1][2]=r-1; groups[-1][3].append(start)
    else: groups.append([keyg,start,r-1,[start]])
for keyg,a,b,starts in groups:
    if len(starts)>1:
        for col in (2,3):
            for m in list(ws.merged_cells.ranges):
                if m.min_col==col and m.max_col==col and a<=m.min_row<=b: ws.unmerge_cells(str(m))
            for x in range(a,b+1):
                if x!=a: ws.cell(x,col).value=None
            ws.merge_cells(start_row=a,start_column=col,end_row=b,end_column=col)
ws.page_setup.orientation="landscape"; ws.page_setup.paperSize=ws.PAPERSIZE_A4
ws.sheet_properties.pageSetUpPr.fitToPage=True; ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0
for row in ws.iter_rows():
    for c in row:
        if c.value is not None: B.apply_font(c)
wb.save(sys.argv[2])
for x in rows: print(x['band'],'|',str(x['company']).replace('\n',' '),'|',x['year'],'|',len(x['src']))
