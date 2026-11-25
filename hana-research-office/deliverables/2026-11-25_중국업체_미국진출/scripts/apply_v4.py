import sys, math, importlib.util, os
from copy import copy
from openpyxl import load_workbook
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location("B",os.path.join(HERE,"build_us_entry.py")); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
wb=load_workbook(sys.argv[1]); ws=wb['미국 진출 현황']
T={  # row: (E, G)  E=None이면 유지
5:(None,"2026.10 타운십과 연방소송 합의로 사업 포기 확정. 토지 이전·보조금 반환청구 철회 합의안은 MSF 이사회 승인 보류(2026.10.27)\n2025.10 주정부 인센티브 전면 종료\n2025.09 주정부(MEDC) 채무불이행 통지(120일 이상 현장 활동 없음)"),
8:("일리노이 Manteno 옛 Kmart 물류센터(150만 sq ft) 단독 투자. 리튬이온 셀 40GWh·팩 10GWh 및 ESS 생산 계획\n투자 20억달러, 고용 2,600명, 주 인센티브 약 5.36억달러, 2024년 생산 개시 목표",
   "2026.11 기준 ESS 팩 라인만 가동, 셀 생산은 미개시\n2026.02 주민 소송에 피고 추가(소송 진행 중)\n2025.11 5개 라인·약 300명(발표 고용 2,600명)\n2025년 초 ESS 팩 라인 가동"),
13:("캘리포니아 Fremont(2014년 R&D 거점) 단독 팩 공장. 주거용 ESS LFP 팩(3~30kWh) 연산 1GWh, 셀 생산 없음",
    "2026.08 기준 가동 중(ESS 제품 위주), 이후 생산·증설 관련 공식 자료 없음\n2023.12 첫 팩 출하로 Gotion 미국 첫 제조 라인 가동"),
16:("테네시 Smyrna 공장(2012년부터 Nissan Leaf용 셀 생산, 2018년 Envision이 AESC 인수로 확보)\n2023.07 Fluence와 미국산 ESS 셀 공급계약 체결 후 ESS용 LFP 라인으로 전환",
    "2026.04 PFE 대응 목적으로 공장 지분을 미국 Fixx Energy에 매각, AESC는 기술 라이선스 제공. Fixx-Fluence 셀 공급계약 체결\n2025.06 Nissan향 생산 종료\n2025.04 ESS 셀 양산 개시"),
18:("켄터키 Bowling Green 단독 투자로 EV용 셀·모듈 30GWh 공장. 투자 20억달러, 고용 2,000명, 2025~2026년 가동 목표\n2022.08 착공",
    "2026.11 기준 공사 재개·가동 관련 보도 없음. Envision 지배 유지 시 OBBBA상 45X 세액공제 불가 가능성 높아\n2025.06 AESC는 '공사 지속·투자 약속 유지'로 반박\n2024.09 공사 중단·설비 미반입(2025.06 WSJ 보도)"),
21:("사우스캐롤라이나 Florence BMW향 EV 셀 공장(1단계 30GWh, 8.1억달러), 2025년 생산 목표\n2023.12 증액(누적 16.2억달러·1,620명)\n2024.03 제2공장 15억달러 추가 발표",
    "2026.11 기준 공사 재개 보도 없음. 시공사 Clayco가 미지급금 2,620만달러 청구\n2025.06 정책·시장 불확실성으로 공사 중단(약 10억달러 투입). BMW향 원통형 셀은 중국 장쑤 공장 생산으로 대체\n2025.02 제2공장 철회로 주정부 인센티브 일부 회수"),
28:("Cummins(Accelera)·Daimler Truck·PACCAR와 미시시피 Marshall County에 상용차용 각형 LFP 셀 21GWh JV(Amplify Cell Technologies). 지분 3사 각 30%, EVE 10%(이사 1석), 투자 19억달러·고용 2,000명 이상. EVE는 공동개발·라이선스·서비스(CLS) 모델로 기술 제공\n2024.06 착공",
    "2026.09 3사가 건물은 완공하되 생산설비 설치는 연기하기로 합의, 생산 개시 시점 불확실(Cummins 10-Q)\n2026.05 감원(73명)\n2025.10 생산 개시 2027→2028년 지연 보도"),
33:("텍사스 Mesquite 단독 ESS 모듈·시스템 조립 공장 연산 10GWh(셀 생산 없음), 초기 투자 1억달러\n2025.05 개소 시 약 2억달러·약 200명으로 확대",
    "2026.11 기준 가동 중, 미국 셀 생산 계획은 없음\n2025.08 첫 출하·양산 개시"),
38:("Ford 100% 자회사가 미시간 Marshall(BlueOval Battery Park Michigan)에서 CATL 라이선스로 각형 LFP 셀 생산. CATL은 지분 없이 기술·서비스(설비 셋업·교육·품질체계) 제공. 35억달러·35GWh·2026년 가동 계획\n2023.11 20GWh로 축소",
    "2026.11.18 첫 셀을 Louisville 공장(Fathom 프로토타입용)으로 출하. 팩 공장 2027년 가동, Fathom 양산 2027.4Q 예정\n2026.10 셀 생산 개시\n2026.06 첫 완제 셀 조립(파일럿)\n*Ford는 45X 요건에 부합한다고 주장"),
43:(None,
    "2026.10 전극 믹싱 시운전 완료, 2028년 생산능력의 80% 이상 계약·막바지 협상 단계, 2027년 말 가동 목표\n2026.05 분할 계약 종결로 Ford Energy 출범, 첫 고객 EDF(5년, 연 최대 4GWh)\n2026.01 하원 중국특위원장이 ESS 확대에 따른 라이선스 수정 여부·세액공제 청구 계획 질의(Ford 회신 미공개)"),
48:("Tesla가 CATL 유휴 설비를 들여와 네바다(Sparks)에 Megapack용 LFP 셀 라인 구축(보도). 생산설비 매입 후 Tesla가 단독 소유·운영하는 방식으로, CATL 라이선스 여부는 양사 공식 확인 없음",
    "2026.10 Tesla 3Q26 Update에 'Nevada LFP 7GWh, Early Ramp' 표기, 자사 LFP 셀로 만든 첫 Megapack 출하\n2026.1Q 램프업 시작\n2024.03 CATL 회장이 네바다 장비 공급 사실 확인"),
52:("GM-CATL 북미 LFP 공장 LRS(License·Royalty·Service)형 협의 보도\n2024.09 TDK가 CATL 라이선스로 미국 LFP 공장을 운영하고 GM이 셀을 구매하는 방안 보도",
    "2026.11 기준 투자·계약 체결 없음, 협의 단계에서 멈춤(2024.03~). GM 공시(10-K·10-Q)에 CATL 언급 없음\n2025.07 GM은 LG엔솔 JV(Ultium Spring Hill) 전환으로 미국산 LFP 2027년 말 생산 목표 발표(CATL 무관)"),
58:(None,
    "2026.03 팩 라인 2026년 고객 인도 예정, 셀 생산 재개 일정 미정(10-K). 생산능력 약 3.5GWh는 전량 중국 Huzhou\n2024.2Q 자금 부족으로 공사 중단\n2023.07 켄터키 분리막 공장 계획 철회(중국 연관성 논란 속 2023.05 DOE 보조금 2억달러 취소)"),
61:(None,
    "2026.08 1단계 건설 완료·하반기 2단계 착수 예정 보도, 상업생산 개시는 확인 안 됨\n2026.03 '검토 중(Under evaluation)' 표기\n2025.12 미국 제조를 CS PowerTech(CSIQ 75.1%)로 재편해 PFE 규정 대응\n2025.11 생산 개시를 2026.12로 연기"),
66:("캘리포니아 Lancaster 구 RV 공장을 인수해 전기버스 조립공장 설립(당초 연 1,000대)\n2017.10 증설로 약 45만 sq ft·연 1,500대 능력 확보, 이후 전기트럭·스쿨버스·코치로 품목 확대(현 RIDE 브랜드)",
    "2026.11 기준 가동 지속(2026년 생산량 미공개, 노조 근로자 750명 이상)\n2026.06 국방부 1260H 목록 등재. 1260H 등재로 2026.06.30부터 국방부 조달 금지\n2026.01 미국 자회사 4곳이 IEEPA 관세 환급 소송 제기"),
72:("미국 승용차 판매·현지생산 계획 없음. Stella Li 부회장이 '미국은 고려 대상 아님'(2023), '미국 판매 계획 없음'(2024.05) 발언",
    "2026.10 진출 보류 유지. Stella Li가 '명확성·안정성이 없어 기다리겠다', '지정학이 확장의 최대 과제'라고 발언\n2026.09 Xi 국빈방미 수행단 포함 검토 보도, 중국 자동차 업체 경영진은 정상회담 불참(보도). 재무장관 BYD 보조금 비판\n2026.04 상무장관 'We're not going to have them here'"),
78:("멕시코 승용차 공장 건설 검토(보도). 북미 생산거점이자 미국 관세 우회 기지로 주목, 부지·투자액 공식 발표는 없음",
    "2026.11 기준 COMPAS 공장 인수 결과 확인 안 됨\n2026.09 Trump, 중국 업체의 멕시코 생산분 미국 수출에 반대\n2026.02 Geely 등과 닛산-벤츠 COMPAS 공장(Aguascalientes, 연 약 23만대) 인수 최종후보로 보도\n2025.07 멕시코 공장 계획 보류 보도 후 사실상 정지"),
84:("Volvo Cars 첫 미국 공장(사우스캐롤라이나 Ridgeville, 2018 개소). 연산 15만대, 누적 투자 13억달러, EX90·Polestar 3 생산\n2025.07 XC60 생산 추가 계획 발표",
    "2026.10 EX90·Polestar 3 판매 부진으로 가동률 저조, XC60 생산은 2027.1Q로 지연\n2026.05 BIS 커넥티드카 규정상 개별 승인 획득해 미국 판매 지속\n2026 봄 Volvo CEO가 규제 통과 시 Geely 브랜드 차량 생산 검토 가능성 언급"),
90:("Polestar 3를 Volvo Ridgeville 공장에서 생산, 그 외 차종은 수입해 미국 판매\n2026.03 Polestar 3 글로벌 생산(중국 내수 제외)을 Ridgeville로 일원화하는 계약 체결",
    "2026.10 9M26 미국 판매 약 4,000대, 유럽 중심으로 전환\n2026.06 BIS가 커넥티드카 규정상 승인 거부 → MY2027부터 미국 신차 판매 불가(기존 재고·A/S는 지속). 생산지가 아닌 Geely 지배 구조가 판단 근거"),
95:("CES 2026에서 Geely가 Zeekr·Lynk & Co 미국 진출을 검토 중이며 '24~36개월 내 계획 발표'라고 언급(Volvo 공장 공유 가능성 거론)",
    "2026.11 기준 판매법인·딜러망·인증 등 구체적 진행 없음(사실상 보류)\n2026.08 Zeekr 차체 기반 Waymo 로보택시(Ojai) SF·LA·Phoenix 전면 운행, 현재 유일한 미국 진입 경로"),
99:(None,"2026.08 관세 부담(보도상 150%)으로 Eletre 미국 판매 중단, Emeya도 보류. 2027MY는 영국산 Emira만 판매"),
100:(None,"2026.06 국방부 1260H 목록 등재, NIO는 '미 정부 조달 제한은 사업에 영향 없음'이라며 반박"),
102:(None,"2026.07 He Xiaopeng CEO가 '미국은 반드시 진입해야 할 가장 중요한 시장 중 하나', 정책 허용 시 미국 공장 건설도 수용 가능하다고 발언. 단기로는 캐나다 우선 검토\n2026.03 멕시코 진출"),
105:(None,"2026.11 기준 미국 판매·생산 계획 없음"),
107:("Stellantis(51%)-Leapmotor(49%) JV인 Leapmotor International이 해외 판매 담당. Stellantis CEO가 Investor Day에서 중국 브랜드 생산 여지는 '멕시코, 캐나다일 수도'라고 언급하며 미국은 제외",
     "2026.11 Stellantis가 캐나다 Brampton 유휴공장을 Roshel에 매각하는 계약 체결(2026.05 Leapmotor 활용 가능성 보도)\n2026.10 멕시코에서 판매 중, 북미 생산 확정 프로젝트 없음"),
111:(None,"2026.11 기준 미국 판매·생산 계획 없음, 실리콘밸리 거점 존속 여부 미확인\n2025.04 해외전략(Glocal)에 미국 미포함\n2024 멕시코 공장·R&D 센터 계획 발표(위치·투자액·착공 여부 미확인)"),
114:("2013년 '2015년경 미국 SUV 판매' 목표 제시\n2018 '2021년 미국 진입' 목표 제시",
     "2026.11 기준 미국 진출 목표 무산, 진출 계획 없음. 유럽 재진입에 집중\n2026.02 멕시코 COMPAS 공장 인수 응찰 보도"),
117:("Reuters 인터뷰에서 부사장이 '미국 완성차와의 파트너십까지 다양한 방안에 열려 있다', 중국산 하드웨어·소프트웨어를 배제한 차량도 구현 가능하다고 언급",
     "2026.11 기준 미국 파트너·진출 일정 미발표\n2026.10 캐나다는 2027년 초 브랜드 출시 준비"),
}
assert ws['B66'].value=='BYD' and ws['B117'].value=='Chery' and ws['H3'].value=='비고' and ws['I3'].value=='출처'
for r,(e,g) in T.items():
    assert ws.cell(r,4).value, r
    if e is not None: ws.cell(r,5).value=e
    ws.cell(r,7).value=g
# 비고(H) 열 삭제: H 병합 해제, 띠 병합(B:I) 해제 후 I→H 이동
bands=[]
for m in list(ws.merged_cells.ranges):
    if m.min_col==8 and m.max_col==8: ws.unmerge_cells(str(m))
    elif m.min_col==2 and m.max_col==9: bands.append(m.min_row); ws.unmerge_cells(str(m))
    elif m.max_col>=8: raise SystemExit(f"unexpected merge {m}")
for r in range(1,ws.max_row+1):
    h,i=ws.cell(r,8),ws.cell(r,9)
    h.value=i.value; h.font=copy(i.font); h.alignment=copy(i.alignment); h.border=copy(i.border); h.fill=copy(i.fill); h.number_format=i.number_format
    h.hyperlink=i.hyperlink.target if i.hyperlink else None
    i.value=None; i.hyperlink=None; i.border=copy(ws.cell(r,10).border); i.fill=copy(ws.cell(r,10).fill); i.font=copy(ws.cell(r,10).font)
for r in bands: ws.merge_cells(start_row=r,start_column=2,end_row=r,end_column=8)
ws.column_dimensions['H'].width=50.875
if 'I' in ws.column_dimensions: del ws.column_dimensions['I']
# 행 높이
def span(r):
    for m in ws.merged_cells.ranges:
        if m.min_row==r and m.min_col==5: return m.min_row,m.max_row
    return r,r
for r in T:
    a,b=span(r); k=b-a+1
    need=max(14*B.est_lines(ws.cell(r,c).value,52)+4 for c in (5,7) if ws.cell(r,c).value)
    per=max(18,math.ceil(need/k))
    for x in range(a,b+1): ws.row_dimensions[x].height=per
ws.print_area=None
for w in wb:
    for row in w.iter_rows():
        for c in row:
            if c.value is not None: B.apply_font(c)
wb.save(sys.argv[2])
