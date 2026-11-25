"""2026-11-25 출처 링크 검증 반영.
- 재검색으로 주소를 찾지 못한 출처는 확인된 대체 기사로 바꾸거나 제외
- 확인된 근거가 없는 문장은 확인된 사실로 수정
- 주소 수정 5건, 날짜 수정 1건
"""

W = "검색 결과에서 주소 확인(2026.11.25)"
D = "원문 접속 확인(2026.11.25)"

NEW_SRC = {
    "n1": dict(pub="Shaw Local(Daily Journal)", title="Fire chief questions Gotion's fire safety readiness", date="2025.12.05", url="https://www.shawlocal.com/daily-journal/2025/12/05/fire-chief-questions-gotions-fire-safety-readiness/", check=W),
    "n2": dict(pub="Shaw Local(Daily Journal)", title="Gotion updates Manteno village on safety issues", date="2026.01.07", url="https://www.shawlocal.com/daily-journal/2026/01/07/gotion-updates-manteno-village-on-safety-issues", check=W),
    "n3": dict(pub="Electrek", title="China's Gotion High-Tech rolls first battery pack off its new US assembly line", date="2023.12.29", url="https://electrek.co/2023/12/29/chinas-gotion-high-tech-rolls-first-battery-pack-off-its-new-us-assembly-line/", check=W),
    "n4": dict(pub="SC Daily Gazette", title="Electric vehicle battery company halts construction of SC manufacturing plant", date="2025.06.05", url="https://scdailygazette.com/2025/06/05/electric-vehicle-battery-company-halts-construction-of-sc-manufacturing-plant/", check=W),
    "n5": dict(pub="SC Daily Gazette", title="SC battery cell plant ups jobs numbers to employ more than 1,600 workers in Florence", date="2023.12.12", url="https://scdailygazette.com/2023/12/12/sc-battery-cell-plant-ups-jobs-numbers-to-employ-more-than-1600-workers-in-florence/", check=W),
    "n6": dict(pub="ENR", title="Second expansion in four months brings South Carolina EV battery project to $3.1B", date="2024.03", url="https://enr.com/articles/58390-second-expansion-in-four-months-brings-south-carolina-ev-battery-project-to-31b", check=W),
    "n7": dict(pub="Spectrum News", title="AESC loses incentives(South Carolina)", date="2025.02.05", url="https://spectrumlocalnews.com/sc/south-carolina/news/2025/02/05/south-carolina-news-aesc-loses-incentives", check=W),
    "n8": dict(pub="Electrek", title="Ford cuts back major EV investment in Michigan battery plant", date="2023.11.21", url="https://electrek.co/2023/11/21/ford-cuts-back-major-ev-investment-michigan-battery-plant/", check=W),
    "n9": dict(pub="IBTimes", title="Ford Starts Making EV Battery Cells in Michigan With China's CATL Technology", date="2026.11", url="https://www.ibtimes.com/ford-starts-ev-battery-cell-production-michigan-catl-3809933", check=W),
    "n10": dict(pub="TechCrunch", title="Ford halts work on $3.5B EV battery factory with China's CATL", date="2023.09.25", url="https://techcrunch.com/2023/09/25/ford-halts-work-on-3-5b-ev-battery-factory-with-chinas-catl", check=W),
    "n11": dict(pub="Transport Topics", title="GOP lawmaker questions Ford battery agreement with CATL", date="2023.04", url="https://www.ttnews.com/articles/gop-ford-battery-agreement", check=W),
    "n12": dict(pub="White & Case", title="Amendments to IRA tax credits in the House Ways and Means budget bill", date="2025.05", url="https://www.whitecase.com/insight-alert/amendments-ira-tax-credits-house-ways-and-means-budget-bill", check=W),
    "n13": dict(pub="White & Case", title="New law changes IRA tax credits(July 4 budget bill)", date="2025.07", url="https://www.whitecase.com/insight-alert/amendments-to-ira-tax-credits-congressional-budget-bill-july-4", check=W),
    "n14": dict(pub="govinfo.gov", title="Public Law 119-21(One Big Beautiful Bill Act) 법률 원문", date="2025.07.04", url="https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm", check=W),
    "n15": dict(pub="Federal Register(미 국방부)", title="Notice of Availability of Designation of Chinese Military Companies(2026-11571)", date="2026.06.10", url="https://www.federalregister.gov/documents/2026/06/10/2026-11571/notice-of-availability-of-designation-of-chinese-military-companies", check=W),
    "n16": dict(pub="Fortune(Quartr 녹취록)", title="Ford Motor Q3 2026 earnings call transcript", date="2026.10.28", url="https://fortune.com/company/ford-motor/earnings/q3-2026/", check=W + ", 팀 컨콜 노트와 일치"),
    "n17": dict(pub="Electrek", title="GM to use cheaper batteries from China's CATL for Chevy Bolt EV", date="2025.08.07", url="https://electrek.co/2025/08/07/chevy-bolt-ev-cheaper-batteries-chinas-catl/", check=W),
    "n18": dict(pub="Roll Call", title="NDAA provision targets Chinese rail cars and electric buses", date="2019.12.10", url="https://rollcall.com/2019/12/10/ndaa-provision-targets-chinese-rail-cars-and-electric-buses/", check=W),
    "n19": dict(pub="eletric-vehicles.com", title="China weighs sending BYD and Xiaomi CEOs to Washington with Xi", date="2026.09", url="https://eletric-vehicles.com/general/china-weighs-sending-byd-and-xiaomi-ceos-to-washington-with-xi/", check=W),
    "n20": dict(pub="Ford Authority", title="Chinese auto execs won't be at Trump summit with Xi", date="2026.09", url="https://fordauthority.com/2026/09/chinese-auto-execs-wont-be-at-trump-summit-with-xi/", check=W),
    "n21": dict(pub="electrive", title="BYD halts Mexico factory plans amid Trump's trade tensions", date="2025.07.03", url="https://www.electrive.com/2025/07/03/byd-halts-mexico-factory-plans-amid-trumps-trade-tensions", check=W),
    "n22": dict(pub="Stellantis(SEC 6-K)", title="Stellantis Brampton 공장 Roshel 매각 계약 발표", date="2026.11", url="https://www.sec.gov/Archives/edgar/data/0001605484/000160548426000099/a99111092026_stla.htm", check=D),
    "n23": dict(pub="Transport Topics", title="Stellantis sells Brampton plant to Roshel", date="2026.11", url="https://www.ttnews.com/articles/stellantis-sells-plant-roshel", check=W),
    "n24": dict(pub="ITV News", title="China and Canada expand tariff relief while Ottawa-Washington relations are strained", date="2026.11.17", url="https://www.itv.com/news/2026-11-17/china-and-canada-look-for-better-joint-trade", check=W),
    "n25": dict(pub="Ford(From The Road)", title="Ford is in the battery business now", date="2026.11.19", url="https://www.fromtheroad.ford.com/us/en/articles/2026/ford-is-in-the-battery-business-now", check=W),
    "a25": dict(pub="新浪财经(储能世界 전재)", title="远景动力调整美国投资战略，加快储能布局抢占新赛道", date="2025.06.18", url="https://finance.sina.com.cn/roll/2025-06-18/doc-infansqk8290384.shtml", check=D),
    "n26": dict(pub="Michigan Public", title="Ford pauses work at EV battery site in Marshall, but state officials say they're staying the course", date="2023.09.25", url="https://www.michiganpublic.org/transportation-infrastructure/2023-09-25/ford-pauses-work-at-ev-battery-site-in-marshall-but-state-officials-say-theyre-staying-the-course", check=W),
}

# 주소 수정(검증 에이전트가 검색 결과에서 찾은 주소)
URL_FIX = {
    "a27": dict(url="https://newkentuckyhome.ky.gov/Newsroom/NewsPage/20220413_EnvisionAESC", pub="Kentucky Cabinet for Economic Development", date="2022.04.13"),
    "a30": dict(url="https://bgdailynews.com/?p=689798"),
    "b6": dict(url="https://waysandmeans.house.gov/?p=12685"),
    "a6": dict(url="https://www.yahoo.com/news/us/articles/state-board-tables-approval-gotion-152110041.html", pub="WOOD TV8(Yahoo News 게재)", date="2026.10.27", check="검색 결과에서 주소 확인(2026.11.25)"),
    "b19": dict(url="https://www.ess-news.com/2026/05/18/ford-and-edf-sign-gigawatt-scale-bess-agreement-for-north-american-market/", pub="ESS News(pv magazine 계열)"),
    "b17": dict(url="https://www.aol.com/articles/us-lawmaker-scrutinizes-ford-plan-182334633.html", pub="Reuters(AOL 게재)"),
}
DATE_FIX = {"a59": "2025.09.01"}

# 출처 교체(행 안에서 old → new 목록, 빈 목록이면 제외)
SWAP = {
    "a1": [], "a11": ["n1", "n2"], "a16": ["n3"], "a21": [], "a36": ["n4"], "a37": [], "a40": [], "a41": [],
    "a60": [], "b52": ["n15"], "b3": ["n8"], "b36": ["n9"], "b30": ["n16"], "b46": ["n17"], "c7": ["n15"],
    "c4": ["n18"], "c16": ["n19", "n20"], "c21": ["n21"], "c55": [], "c66": ["n22", "n23"], "b35": ["n9"],
    "b4": ["n11"], "b2": ["n10", "n26"], "b7": ["n12"], "b8": ["n13"], "b9": ["n14"], "b34": ["n25"],
    "c83": [], "c86": ["n24"], "c87": [],
}
# 행별 추가 출처
ADD = {
    ("Envision AESC", "2022.12"): ["n5", "n6", "n7", "a25"],
}

# 문장 수정 (old, new) — 확인 안 된 사실 제거·정정
TEXT_FIX = [
    # Gotion Manteno
    ("2025.11 기준 5개 라인·약 300명. 2026.10 기준 약 600명 근무(2026년 목표 1,400명 미달). 자체 LFP 셀 생산 개시는 확인 안 됨(팩·ESS 조립 위주)",
     "2025.11 기준 5개 라인·약 300명. 자체 LFP 셀 생산 개시는 확인 안 됨(팩·ESS 조립 위주)"),
    ("주민 소송 진행 중. 2026.03 OSHA 벌금 2건 부과(이의 제기), 2026.10 화상사고 조사. 주 계약상 고용 의무 2029년 1,650명",
     "주민 소송 진행 중(2026.02 피고 추가). 2025.12 소방당국이 화재안전 미비를 지적했고, 2026.01 회사가 미해결 사항 해소를 보고"),
    # AESC Florence
    ("2025.02 제2공장 철회, 2025.06 정책·시장 불확실성으로 공사 중단(공정률 약 75%, 약 12억달러 투입). 2026.10 기준 재개 일정 없음. 현지 언론은 '개장하지 않을 것'으로 보도, 시공사 Clayco가 미지급금 2,620만달러 청구",
     "2025.02 제2공장 철회로 주정부 인센티브 일부 회수, 2025.06 정책·시장 불확실성으로 공사 중단(약 10억달러 투입, 재개 시점 미정). 2026.11 기준 공사 재개 보도 없음. 시공사 Clayco가 미지급금 2,620만달러 청구"),
    # Hithium
    ("2025.08 첫 출하·양산 개시. 2026.01 기준 가동률 약 60%, 직원 160명. 미국 셀 생산 계획은 발표 없음",
     "2025.08 첫 출하·양산 개시. 미국 셀 생산 계획은 발표 없음"),
    # BYD Lancaster
    ("2026.06 국방부 1260H 목록 등재(BYD 반박).", "2026.06 국방부 1260H 목록 등재."),
    ("2019년 법률로 연방 대중교통 자금 사용 차단.", "2019년 국방수권법(NDAA)으로 연방 대중교통 자금의 중국 업체 버스 구매 금지(2년 유예 후 시행)."),
    # BYD 승용차
    ("2026.09 Xi 국빈방미 수행단 포함 검토 보도가 있었으나 협의 결과는 확인 안 됨",
     "2026.09 Xi 국빈방미 수행단 포함 검토 보도가 있었으나 중국 자동차 업체 경영진은 정상회담에 참석하지 않음(보도)"),
    # NIO
    ("San Jose 인원 100명 미만으로 축소 보도(2024~2025). 2026.06.08", "2026.06.08"),
    # Leapmotor
    ("2026.10 기준 멕시코에서 판매 중, 북미 생산 확정 프로젝트는 없음. 캐나다 Brampton 유휴공장 활용 가능성 보도",
     "2026.10 기준 멕시코에서 판매 중, 북미 생산 확정 프로젝트는 없음. 2026.05 캐나다 Brampton 유휴공장 활용 가능성이 보도됐으나, 2026.11 Stellantis가 해당 공장을 Roshel에 매각하는 계약 체결"),
    ("Brampton 공장 매각 합의 보도도 있어 활용 여부 불확실", "Stellantis는 Leapmotor 차량의 설계·생산을 맡지 않고 브랜드·IP도 보유하지 않음(공시)"),
    # Ford-CATL 비교표
    ("CATL 인력이 램프업 기간 상주하며 설비 셋업·인력 교육·품질체계 지원(팩 구역 출입 불가)", "CATL 인력이 램프업 기간 상주하며 설비 셋업·인력 교육·품질체계 지원"),
    ("당초 35억달러(축소 후 공식 수치 미공개, 보도상 약 30억달러)", "당초 35억달러(축소 후 공식 수치 미공개, 2023.11 약 15억달러 감액 보도, 2026.11 보도상 약 30억달러 공장)"),
    # 타임라인
    ("하원 세입위 법안에 금지외국기업 라이선스 생산 부품의 45X 배제 조항 포함 → 최종법에서 삭제",
     "하원 세입위 법안에 금지외국기업과의 라이선스로 생산한 부품의 45X 배제 조항 포함 → 최종법(OBBBA)에서는 '실효적 통제' 기준으로 변경"),
    ("첫 LFP 셀을 Louisville 공장(Fathom 프로토타입용)으로 출하", "첫 LFP 셀을 Louisville 공장(Fathom 프로토타입용)으로 출하, 2026.11.19 Ford가 공장 공식 가동 발표"),
    # 주요 규제
    ("15% 지분 기준 논란으로 처리 연기, 2027.01.03 회기 만료 전 레임덕 처리 시한", "15% 지분 기준 논란으로 11월로 처리 연기(2026.11 기준 처리 결과 미확인)"),
    ("2026.11.17 연장·확대 합의 보도. USTR은 'problematic'이라며 해당 차량의 미국 진입 불허 입장, USMCA 재검토 쟁점",
     "2026.11.17 Carney-Xi 회담에서 관세 완화 품목을 돼지고기·새우로 확대(EV 쿼터 변경은 보도 없음). USTR은 'problematic'이라며 해당 차량의 미국 진입 불허 입장"),
    ("2026.06.08 갱신 시 BYD·NIO·CALB 등 65개 추가(총 188개, EVE 추가는 보도 기준)", "2026.06.08 갱신 시 BYD·NIO·CALB 등 65개 추가(총 188개, EVE 추가는 보도 기준, 2026.06.10 관보 고시)"),
]

# 검증 결과 반영한 확인 방법(원래 키 기준). 미지정은 아래 기본값 규칙 적용
DIRECT_OK = {"a17", "a18", "a43", "a44", "a25", "b14", "c47"}  # 비-SEC 직접 접속 200
