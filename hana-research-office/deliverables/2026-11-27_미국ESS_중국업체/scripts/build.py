import sys, os, math, importlib.util
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
HERE="/tmp/claude-0/-home-user-seoul-valuation/8e3450ec-a874-54af-9ac0-6d9b05a46018/scratchpad/scripts"
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
BLUE="FF0000FF"
YEARS=["2019","2020","2021","2022","2023","2024","2025","2026(최신)"]
U={
 "opp":"https://www.opportimes.com/en/u-s-increases-its-imports-of-lithium-ion-batteries-from-china/",
 "atl":"https://www.atlanticcouncil.org/blogs/energysource/what-us-tariffs-on-chinese-batteries-mean-for-decarbonization-and-taiwan/",
 "spz":"https://www.solarplaza.com/resource/13532/article-mapping-the-chinese-bess-supply-chain-2026/",
 "cpa":"https://prosperousamerica.org/americas-ai-boom-has-a-trade-policy-blind-spot/",
 "csr":"https://councilonstrategicrisks.org/wp-content/uploads/2025/05/75-Devil-is-in-the-Details.pdf",
 "sta":"https://www.statista.com/chart/29473/value-of-lithium-ion-battery-imports-to-the-united-states/",
 "sp26":"https://www.spglobal.com/energy/en/news-research/latest-news/electric-power/082426-us-lithium-ion-battery-imports-rebound-in-q2-despite-trade-friction",
 "qq23":"https://news.qq.com/rain/a/20250123A06ZW500",
 "jm24":"https://m.jiemian.com/article/12286043.html",
 "btd25":"https://m.bigtradedata.com/contents/91/331.html",
 "bhi":"https://www.bhi.com.cn/News/ShowDetails.aspx?columns=31&id=90083354",
 "sgw":"https://finance.sina.com.cn/roll/2026-07-22/doc-iniispmx1923159.shtml",
 "hit":"https://www.aap.com.au/aapreleases/cision20251009ae94327",
 "gtm19":"https://greentechmedia.com/amp/article/us-storage-industry-achieved-biggest-ever-quarter-year-in-2019",
 "esn20":"https://www.energy-storage.news/in-2020-the-us-went-beyond-a-gigawatt-of-advanced-energy-storage-installations-for-first-time-ever/",
 "esn22":"https://www.energy-storage.news/us-installed-almost-as-much-battery-storage-in-2022-as-previous-two-years-combined/",
 "esn24":"https://www.energy-storage.news/2024-energy-storage-installations-surpassed-12gw",
 "wm25":"https://www.woodmac.com/press-releases/2025-u.s.-energy-storage-installations-set-new-record-surpass-2024-by-52",
 "ud26":"https://www.utilitydive.com/news/us-sees-record-q1-2026-energy-storage-installations/823547/",
 "esnt":"https://www.energy-storage.news/ev-slowdown-creates-potential-lifeline-for-us-energy-storage-amid-feoc-tariffs/",
 "qq25":"https://news.qq.com/rain/a/20250410A01JZJ00",
 "cx26":"https://www.caixinglobal.com/2026-01-23/chinese-battery-makers-log-record-overseas-orders-amid-global-grid-crunch-102407425.html",
 "tyn":"https://taiyangnews.info/business/wood-mackenzie-2024-bess-suppliers-ranking",
}
# row: (구분, 지표, 단위, {year: value or ('f',formula) or text}, 비고, [url keys])
REV=[
 ("band","미국 측 통계: 중국산 리튬이온 배터리 수입"),
 ("미국 수입","중국산 리튬이온 배터리 수입액(HS 8507.60, ESS·EV 합산)","백만달러",
  {"2019":1858,"2020":2104,"2021":4520,"2022":9295,"2023":13217,"2024":16458,"2025":11800},
  "ESS 전용 코드(8507.60.0020) 연간 수치는 공개 자료에서 확인 안 됨. 2023년 이후 ESS가 대부분인 것으로 보도(EV용은 감소). 2025년은 관세 인상으로 감소",["opp","atl","spz"]),
 ("미국 수입","미국 리튬이온 배터리 총수입액(HS 8507.60)","백만달러",
  {"2020":4800,"2022":13900,"2024":23800},"중국 비중 계산용",["cpa","sta"]),
 ("미국 수입","미국 리튬이온 배터리 수입 중 중국 비중","%",
  {"2020":44,"2021":56,"2022":("f","=IFERROR(H6/H9*100,\"n/a\")"),"2023":71,"2024":69,"2025":59,"2026(최신)":66.5},
  "2022년은 중국산 수입액÷총수입액으로 계산. 2026은 2Q26 기준(S&P, 1Q26 60.3%)",["cpa","csr","sta","sp26"]),
 ("band","중국 측 통계: 대미 수출"),
 ("중국 수출","중국의 대미 리튬전지 수출액(해관, 전 용도)","백만달러",
  {"2023":13549,"2024":15315,"2025":"8,911\n(1~9월)"},"전 용도(동력·ESS·소형) 합산. 2024년은 ESS가 주도(+13% YoY), 2025년 1~9월 -12% YoY",["qq23","jm24","btd25"]),
 ("중국 수출","중국의 대미 ESS 배터리 수출액(증권사 추정)","백만달러",
  {"2024":6270},"중신증권 추정 인용 보도(원문 미확인). 미국 ESS 배터리 수입의 약 57%",["bhi"]),
 ("band","기업 공시"),
 ("Sungrow","Sungrow USA(미국 법인) 매출","억위안",
  {"2025":172.47},"총매출의 19.3%. 태양광 인버터 포함, 미국 고객에 다른 법인이 직접 판매한 매출은 제외. 경영진은 미국 비중을 총매출의 15~20%로 언급",["sgw"]),
 ("Hithium","해외 매출 비중","%",
  {"2023":1,"2024":28.6},"미국 매출은 별도 미공개(텍사스 모듈·시스템 조립 공장 보유)",["hit"]),
 ("CATL·BYD·EVE 등","미국 ESS 매출","-",{},"미국 또는 미국 ESS 매출 별도 미공개(해외 매출 합산만 공시)",[]),
]
SHP=[
 ("band","미국 ESS 시장 규모"),
 ("미국 시장","미국 ESS 연간 설치량","GWh",
  {"2019":1.1,"2020":3.5,"2021":10.9,"2022":12.2,"2023":27.7,"2024":37.1,"2025":51.0,"2026(최신)":"8.4\n(1Q26)"},
  "Wood Mackenzie. 2022·2023은 이후 상향 개정된 수치가 있음",["gtm19","esn20","esn22","esn24","wm25","ud26"]),
 ("미국 시장","미국 ESS에 탑재된 셀 중 중국산 비중","%",{"2024":"90 이상"},"Rho Motion(2024년 미국 ESS 탑재 셀 기준)",["esnt"]),
 ("미국 시장","중국산 셀 탑재량(추정)","GWh",{"2024":("f","=IFERROR(J6*0.9,\"n/a\")")},"추정: 2024년 설치량 × 중국산 비중 90%(하한)",[]),
 ("band","중국 → 미국 출하·수주"),
 ("중국 수출","중국의 대미 ESS 배터리 수출량(증권사 추정)","GWh",{"2024":"35~40"},"수출액 62.7억달러 기준 추정(원문 미확인)",["bhi"]),
 ("수주","중국 업체의 미국 ESS 수주 규모","GWh",{"2024":65.8,"2025":"50~55"},"2024: 미국 업체와 24건 계약(CESA). 2025: CNESA 집계 해외 수주(366GWh) 중 미국분. 수주는 출하보다 앞서며 인도까지 시차",["qq25","cx26"]),
 ("band","시스템 통합(완제품) 출하 점유율"),
 ("시스템 통합","북미 BESS 출하 중 중국 업체 점유율","%",{"2023":23,"2024":16},"Wood Mackenzie. 미·중 갈등·무역 보호로 하락. 2023년 북미 상위 3사(Tesla·Sungrow·Fluence) 합산 72%",["tyn"]),
 ("band","2026년 최신"),
 ("미국 수입","미국 ESS·비EV 리튬이온 배터리 수입량","톤",{"2026(최신)":"193,370\n(2Q26)"},"전분기 대비 +29%, 전년 대비 약 -8%. 2026.01부터 중국산 비EV 배터리 301조 관세 25%",["sp26"]),
]
def sheet(wb,title,name,rows,note):
    ws=wb.create_sheet(name); ws.sheet_view.showGridLines=False
    widths={"A":2,"B":14,"C":40,"D":9}
    cols=["B","C","D"]+[chr(ord("E")+i) for i in range(len(YEARS))]+[chr(ord("E")+len(YEARS)),chr(ord("E")+len(YEARS)+1)]
    for i,y in enumerate(YEARS): widths[chr(ord("E")+i)]=10
    ncol=chr(ord("E")+len(YEARS)); scol=chr(ord("E")+len(YEARS)+1)
    widths[ncol]=46; widths[scol]=60
    for k,w in widths.items(): ws.column_dimensions[k].width=w
    t=ws.cell(2,2,title); t.font=Font(name=B.KR,size=11,bold=True)
    n=ws.cell(3,2,note); n.font=Font(name=B.KR,size=9)
    B.header(ws,4,["구분","지표","단위"]+YEARS+["비고","출처"])
    last=2+3+len(YEARS)+1
    r=5
    for row in rows:
        if row[0]=="band":
            B.band(ws,r,row[1],2,last); ws.row_dimensions[r].height=18; r+=1; continue
        g,ind,unit,vals,note_,keys=row
        k=max(1,len(keys)); start=r
        cells=[(2,g,dict(bold=True,h="center"),14),(3,ind,{},40),(4,unit,dict(h="center"),9)]
        for i,y in enumerate(YEARS):
            v=vals.get(y)
            cells.append((5+i,v[1] if isinstance(v,tuple) else v,dict(h="right"),10))
        cells.append((5+len(YEARS),note_,{},46))
        S={u:dict(pub="",date="",url=U[u]) for u in keys}
        r=B.block(ws,r,cells,6+len(YEARS),keys,S,60)
        for i,y in enumerate(YEARS):
            c=ws.cell(start,5+i); v=vals.get(y)
            if isinstance(v,(int,float)):
                c.font=Font(name=B.EN,size=10,color=BLUE)
                d=len(repr(v).split('.')[1]) if isinstance(v,float) and v!=int(v) else (1 if isinstance(v,float) else 0)
                c.number_format="#,##0" if d==0 else "#,##0."+"0"*d
            elif isinstance(v,tuple):
                c.number_format="#,##0.0"; c.font=Font(name=B.EN,size=10)
            elif isinstance(v,str):
                c.font=Font(name=B.KR,size=10,color=BLUE)
    for row in ws.iter_rows():
        for c in row:
            if c.hyperlink:
                u=c.hyperlink.target; c.value=u; c.alignment=Alignment(horizontal="left",vertical="center",wrap_text=True)
                need=14*B.est_lines(u,60)+4
                if (ws.row_dimensions[c.row].height or 15)<need: ws.row_dimensions[c.row].height=need
    ws.page_setup.orientation="landscape"; ws.page_setup.paperSize=ws.PAPERSIZE_A4
    ws.sheet_properties.pageSetUpPr.fitToPage=True; ws.page_setup.fitToWidth=1; ws.page_setup.fitToHeight=0
    return ws
wb=Workbook(); wb.remove(wb.active)
note="주: 미국 시장 내 중국 기업별 ESS 매출·출하량을 직접 공시한 자료는 없어 무역통계·업계 추정·기업 공시로 대신함. 파란 글씨는 출처 수치, 검정 글씨는 계산값. 조회 2026.11.27(검색 결과 기준, 원문 직접 열람 불가)"
w1=sheet(wb,"미국 ESS 시장 내 중국 업체 매출(금액)","매출(금액)",REV,note)
w2=sheet(wb,"미국 ESS 시장 내 중국 업체 출하량","출하량",SHP,note)
for w in wb:
    for row in w.iter_rows():
        for c in row:
            if c.value is not None and not (isinstance(c.value,(int,float))): B.apply_font(c)
            elif isinstance(c.value,(int,float)): c.font=Font(name=B.EN,size=10,color=BLUE)
wb.save(sys.argv[1])
