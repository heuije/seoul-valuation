import sys, math, importlib.util, os, zipfile
from openpyxl import load_workbook
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
src,out=sys.argv[1],sys.argv[2]
wb=load_workbook(src)
ws=wb['미국 진출 현황']
G={
5:"착공 전 단계에서 중단(2023~2025), 2026.10 사업 포기 확정\n2025.10 주정부 인센티브 전면 종료. 토지 이전·보조금 반환청구 철회 합의안은 MSF 이사회 승인 보류(2026.10.27)",
8:"투자 진행, ESS 팩 라인만 가동(2025년 초~). 셀 생산은 미개시(2026.11 기준)\n2025.11 기준 5개 라인·약 300명(발표 고용 2,600명)\n*주민 소송 진행 중(2026.02 피고 추가)",
13:"팩 라인 가동 중(2023.12~), 이후 증설 발표 없음(2026.08 기준)",
16:"ESS 셀 양산 중(2025.04~, Nissan향은 2025.06 종료)\n2026.04 PFE 대응 목적으로 공장 지분을 미국 Fixx Energy에 매각, AESC는 기술 라이선스 제공. Fixx-Fluence 셀 공급계약 체결",
18:"착공(2022.08) 후 공사 중단(2024.09~, 보도), 재개 발표 없음(2026.11 기준)\nAESC는 '공사 지속'이라고 반박(2025.06)\n*Envision 지배 유지 시 OBBBA상 45X 세액공제 불가 가능성 높아",
21:"약 10억달러 투입 후 공사 중단(2025.06~), 재개 시점 미정(2026.11 기준)\n제2공장은 2025.02 철회. BMW향 원통형 셀은 중국 장쑤 공장 생산으로 대체(2025.06)\n시공사 Clayco가 미지급금 2,620만달러 청구",
28:"착공(2024.06) 후 건물만 완공하고 생산설비 설치는 연기(2026.09 3사 합의), 생산 개시 시점 미정\n당초 2027년 생산 → 2028년 지연 보도(2025.10), 2026.05 감원(73명)",
33:"투자 완료, 모듈·시스템 조립 가동 중(2025.08 첫 출하)\n미국 셀 생산 계획은 없음",
38:"Ford 투자로 셀 생산 개시(2026.10), 첫 셀을 Louisville 공장(Fathom 프로토타입용)으로 출하(2026.11.18)\n팩 공장 2027년 가동, Fathom 양산 2027.4Q 예정\n*Ford는 45X 요건에 부합한다고 주장",
43:"ESS 전환 공사 중, 전극 믹싱 시운전 완료(2026.10), 2027년 말 가동 목표\n2028년 생산능력의 80% 이상 계약·막바지 협상 단계(첫 고객 EDF)\n*2026.01 하원 중국특위원장이 ESS 확대에 따른 라이선스 수정 여부·세액공제 청구 계획 질의(Ford 회신 미공개)",
48:"Tesla 단독 투자로 가동 중(2026.1Q 램프업 시작)\n3Q26 기준 'Nevada LFP 7GWh, Early Ramp' 표기, 자사 LFP 셀로 만든 첫 Megapack 출하",
52:"투자·계약 체결 없음, 협의 단계에서 멈춤(2024.03~2026.11)\nGM의 미국산 LFP는 LG엔솔 JV(Ultium Spring Hill) 전환으로 2027년 말 생산 목표(CATL 무관)",
58:"셀 라인 공사 중단(2024.2Q~, 자금 부족), 재개 일정 미정\n팩 라인만 2026년 고객 인도 예정(2026.03 10-K). 생산능력은 전량 중국 Huzhou",
61:"1단계 건설 완료(2026.08 보도), 상업생산 미개시\n생산 개시 2025.11 → 2026.12 연기, 2026.03 '검토 중(Under evaluation)' 표기",
66:"가동 중(2013~, 전기버스·트럭, 노조 근로자 750명 이상)\n2026.06 국방부 1260H 목록 등재",
72:"투자 없음, 진출 보류 유지(2024.05~2026.11)\nStella Li '명확성·안정성이 없어 기다리겠다'(2026.10.08)",
78:"부지·투자 발표 없이 보류(2025.07~)\n2026.02 닛산-벤츠 COMPAS 공장(멕시코) 인수 후보 보도, 결과 미확인(2026.11 기준)",
84:"가동 중(2018~), EX90·Polestar 3 판매 부진으로 가동률 저조\nXC60 생산 2027.1Q로 지연. BIS 커넥티드카 규정 개별 승인 획득(2026.05.26)으로 미국 판매 지속",
90:"BIS 승인 거부로 MY2027부터 미국 신차 판매 불가(2026.06.25), 기존 재고·A/S만 지속\n9M26 미국 판매 약 4,000대, 유럽 중심으로 전환",
95:"투자·판매법인·딜러망 없음, 검토 단계에서 멈춤(2026.01~)\nZeekr 기반 Waymo 로보택시(Ojai) 운행(2026.08)이 유일한 미국 진입 경로",
99:"중국산 Eletre 미국 판매 중단, Emeya 보류(2026.08, 관세 부담)\n2027MY는 영국산 Emira만 판매",
100:"R&D·북미본부만 운영, 판매·생산 투자 없음\n2026.06.08 국방부 1260H 목록 등재, NIO는 '사업 영향 없음'이라며 반박",
102:"R&D 거점만 운영, 미국 진출 투자 없음\nCEO가 '정책 허용 시 미국 공장 건설 수용'(2026.07) 발언, 캐나다·멕시코 우선",
105:"R&D 센터만 운영, 판매·생산 계획 없음(2026.11 기준)",
107:"미국 진출 계획 없음, 북미 생산 확정 프로젝트 없음(멕시코 판매만)\n캐나다 Brampton 공장 활용 가능성 보도 후 Stellantis가 해당 공장을 Roshel에 매각(2026.11)",
111:"R&D 거점 외 미국 진출 진행 없음(2017~), 거점 존속 여부도 미확인\n2025 해외전략(Glocal)에 미국 미포함",
114:"투자 없이 계획 철회(2015·2021 목표 무산), 2026.11 기준 미국 진출 계획 없음\n멕시코 COMPAS 공장 인수 응찰 보도(2026.02), 유럽 재진입에 집중",
117:"검토 발언 단계, 미국 파트너·투자 발표 없음(2026.10~)\n캐나다는 2027년 초 브랜드 출시 준비",
}
assert ws['B52'].value=='CATL–GM' and ws['B48'].value=='CATL–Tesla' and ws['D43'].value=='2025.12'
for r,t in G.items():
    assert ws.cell(r,7).value is not None or r in (), r
    ws.cell(r,7).value=t
ws['H52'].value="GM 10-K·10-Q에 CATL 언급 없음"
e43=str(ws['E43'].value); assert "SK온과의 JV BlueOval SK 해체 후" in e43
ws['E43'].value=e43.replace("SK온과의 JV BlueOval SK 해체 후","SK온과의 합작법인 BlueOval SK 분할로")
e48=str(ws['E48'].value); old="Ford 등과 같은 기술 라이선스 합작 형태가 아니라, 생산설비 매입 후 Tesla가 단독 소유 운영하는 방식"; assert old in e48
ws['E48'].value=e48.replace(old,"Ford처럼 CATL 라이선스로 생산하는 구조가 아니라 생산설비 매입 후 Tesla가 단독 소유·운영하는 방식(보도). 라이선스 여부는 양사 공식 확인 없음")
# GM 행: 수입 관련 출처(S52·S53) 하위행 비우기
for r in range(52,57):
    c=ws.cell(r,9)
    if c.value and str(c.value).split()[0] in ('S52','S53'):
        c.value=None; c.hyperlink=None
# Ford-CATL 일지
fc=wb['Ford-CATL']; hit=0
for row in fc.iter_rows():
    for c in row:
        v=c.value
        if isinstance(v,str) and '합작 해소' in v:
            v=v.replace("Ford·SK온, BlueOval SK 합작 해소 계약 체결(Ford는 켄터키, SK온은 테네시 공장)","Ford·SK온, BlueOval SK 합작법인 분할 계약 체결: 켄터키 2개 공장은 Ford, 테네시 공장은 SK온이 단독 소유")
            v=v.replace("합작 해소 종결, Ford Energy Battery LLC가","분할 계약 종결: Ford 보유 지분 상환, Ford Energy Battery LLC가")
            assert '합작 해소' not in v, v
            c.value=v; hit+=1
sh=wb['출처']
for row in sh.iter_rows():
    for c in row:
        if isinstance(c.value,str) and '합작 해소' in c.value:
            c.value=c.value.replace('BlueOval SK 합작 해소 종결','BlueOval SK 합작법인 분할 종결'); hit+=1
print('합작 해소 replaced',hit)
# 남은 '해소/해체' 점검
for w in wb:
    for row in w.iter_rows():
        for c in row:
            if isinstance(c.value,str) and ('합작 해소' in c.value): print('LEFT',w.title,c.coordinate)
# 행 높이: 병합 범위 기준으로 G 문구가 들어가도록만 늘림
def rng(r,col):
    for m in ws.merged_cells.ranges:
        if m.min_row==r and m.min_col==col: return m.min_row,m.max_row
    return r,r
for r in list(G)+[43,48,52]:
    a,b=rng(r,7); k=b-a+1
    need=max(14*B.est_lines(ws.cell(r,c).value,{5:52,7:52,8:40}[c])+4 for c in (5,7,8) if ws.cell(r,c).value)
    cur=sum((ws.row_dimensions[x].height or 15) for x in range(a,b+1))
    if need>cur:
        per=math.ceil(need/k)
        for x in range(a,b+1): ws.row_dimensions[x].height=max(ws.row_dimensions[x].height or 15, per)
for w in wb:
    for row in w.iter_rows():
        for c in row:
            if c.value is not None: B.apply_font(c)
wb.save(out)
print('comments in src:',[n for n in zipfile.ZipFile(src).namelist() if 'comment' in n or n.endswith('.vml')])
