# -*- coding: utf-8 -*-
"""v2 데이터: 출처, 구조/밸류체인, 시장규모 행."""

# ------------------------------------------------------------------ 출처 (순서대로 S1, S2 ... 부여)
# key: (발행처, 제목, 발간일, 원출처 기관, 링크, 확인 방법)
SRC = [
    ("aj", "爱建证券", "集成度逐步提升重构光模块价值链——光模块行业深度报告", "2026.08.28", "LightCounting·源杰科技 등", "https://pdf.dfcfw.com/pdf/H3_AP202608281828621981_1.pdf", "PDF 원문 확인"),
    ("dx", "东兴证券", "通信光互联行业：CW激光器重构全球光芯片产业格局", "2026.04.22", "LightCounting·灼识咨询(CIC)", "https://pdf.dfcfw.com/pdf/H3_AP202604221821439407_1.pdf", "PDF 원문 확인"),
    ("dg", "大公国际", "“十五五”科技基建浪潮下的光模块行业研究", "2025.12", "LightCounting", "https://pdf.dfcfw.com/pdf/H3_AP202512241807012890_1.pdf", "PDF 원문 확인"),
    ("hd", "汉鼎智库咨询", "磷化铟光芯片衬底材料产业链分析", "2026.10.30", "Yole·LightCounting·Omdia", "https://pdf.dfcfw.com/pdf/H3_AP202610301831244217_1.pdf", "PDF 원문 확인"),
    ("gx", "国信证券", "光模块专题：AI驱动网络变革，光摩尔定律加速", "2024.03.14", "LightCounting", "https://pdf.dfcfw.com/pdf/H3_AP202403151626804725_1.pdf", "PDF 원문 확인"),
    ("hx", "华鑫证券", "高速互联需求驱动光通信行业发展，国产光芯片有望加速渗透", "2024.08.03", "FTTx 광모듈 전망", "https://pdf.dfcfw.com/pdf/H3_AP202408031639131462_1.pdf", "PDF 원문 확인"),
    ("ds", "대신증권", "AI 병목을 넘어서 ① Networking: Everything Goes Optical", "2026 (주가 기준일 2026.02.27)", "기업 분석", "https://stock.pstatic.net/stock-research/invest/15/20260602_invest_997669000.pdf", "PDF 원문 확인"),
    ("im", "iM증권", "성호전자: CPO 도메인의 확장에서 찾는 성장 기회", "2026.05.26", "기업 탐방", "https://stock.pstatic.net/stock-research/company/61/20260526_company_704029000.pdf", "PDF 원문 확인"),
    ("mrvl", "Marvell (IR)", "Custom AI Investor Event 2025", "2025.06.17", "650 Group·Cignal AI·Dell'Oro·LightCounting", "https://www.marvell.com/content/dam/marvell/en/company/assets/marvell-custom-ai-investor-event-2025.pdf", "PDF 원문 확인"),
    ("omdia_ieee", "Omdia (IEEE 802.3 발표)", "Optical Components Market Update", "2025.10", "Omdia", "https://www.ieee802.org/3/ad_hoc/E4AI/public/25_1023/huff_e4ai_01_251023.pdf", "PDF 원문 확인"),
    ("omdia_dci", "Omdia", "Global Purpose-Built DCI Forecast: 2025–30", "2025.12.29", "Omdia", "https://omdia.tech.informa.com/om136060/global-purpose-built-dci-forecast-202530", "웹 원문 확인"),
    ("stl", "STL (실적발표 자료)", "Earnings Call Presentation Q2 FY26", "2025.11", "CRU", "https://stl.tech/wp-content/uploads/2025/11/Earnings-call_Presentation-Q2_FY26.pdf", "PDF 원문 확인"),
    ("yole_tx", "optics.org (Yole Group)", "Optical transceiver market poised to exceed $110BN by 2031", "2026.07.01", "Yole「Optical Transceivers for Datacom & Telecom 2026」", "https://optics.org/news/optical-transceiver-market-poised-to-exceed-110bn-by-2031---report", "웹 원문 확인"),
    ("yole_pkg", "AnySilicon (Yole Group)", "Photonics packaging heads toward a $14.4 billion market by 2031", "2026.03.18", "Yole「Photonics Packaging 2026」", "https://anysilicon.com/news/photonics-packaging-heads-toward-a-14-4-billion-market-by-2031/", "웹 원문 확인"),
    ("yole_pkg2", "optics.org (Yole Group)", "Photonics packaging market to triple in value by 2031", "2026.04.08", "Yole", "https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031", "웹 원문 확인"),
    ("yole_siph", "Semiconductor Today (Yole Group)", "Silicon PIC market growing at 45% CAGR from $95m in 2023 to $863m in 2029", "2024.12.17", "Yole「Silicon Photonics 2024」", "https://semiconductor-today.com/news_items/2024/dec/yole-171224.shtml", "웹 원문 확인"),
    ("yole_gan", "Yole Group", "RF GaN Compound Semiconductor Market Monitor (제품 페이지)", "2025~2026", "Yole", "https://www.yolegroup.com/product/quarterly-monitor/rf-gan-compound-semiconductor-market-monitor/", "검색 요약 확인(사이트 자동접속 차단)"),
    ("lc_siph", "IEEE ComSoc Tech Blog (LightCounting)", "LightCounting: Silicon Photonics chip market to hit $3 billion in 2029", "2024.05.29", "LightCounting", "https://techblog.comsoc.org/2024/05/29/lightcounting-silicon-photonics-chip-market-to-hit-3-billion-in-2029/", "웹 원문 확인"),
    ("lc_chips", "新浪财经 (发现报告 요약)", "LightCounting 광칩 시장 전망(2025 40억 → 2031 150억달러)", "2026.10.29", "LightCounting", "https://finance.sina.com.cn/wm/2026-10-29/doc-iniwwaxf5392802.shtml", "원문 서버 차단. 2031년 InP 광칩 69억달러(46%)가 汉鼎智库 PDF와 일치"),
    ("lc_chipset", "C114 (LightCounting)", "LightCounting：2024年光芯片市场规模约35亿美元 (광통신 칩셋)", "2025.03.04", "LightCounting", "https://m.c114.com.cn/w5472-1284363.html", "웹 원문 확인"),
    ("lc_dec", "LightCounting", "Sales of optical transceivers will reach $23 billion in 2025", "2025.12", "LightCounting", "https://www.lightcounting.com/newsletter/en/december-2025-quarterly-market-update-322", "웹 원문 확인"),
    ("lc_mar", "C114 (LightCounting)", "LightCounting：光芯片和光模块产能正逐步赶上需求", "2026.03.13", "LightCounting", "https://m.c114.com.cn/w5472-1306868.html", "웹 원문 확인"),
    ("lc_ai", "LightCounting", "AI creates a new wave in demand for optical transceivers and accelerates CPO adoption", "2026.01", "LightCounting「Optics for AI Clusters」", "https://www.lightcounting.com/newsletter/en/january-2026-optics-for-ai-clusters-366", "웹 원문 확인"),
    ("lc_eth", "Lightwave (LightCounting)", "Ethernet optical transceiver set to grow 120% in 2026", "2026.10.08", "LightCounting", "https://www.lightwaveonline.com/home/news/55410716/ethernet-optical-transceiver-set-to-grow-120-in-2026", "웹 원문 확인"),
    ("lc_top10", "C114 (LightCounting)", "光模块厂商全球Top10：中国包揽前2，7家入围", "2026.05.28", "LightCounting", "https://m.c114.com.cn/w5472-1311209.html", "웹 원문 확인"),
    ("lc_access", "Lightwave (LightCounting)", "New LightCounting report: access optics sales to increase in the coming years", "2024.12.02", "LightCounting", "https://www.lightwaveonline.com/business/article/55246891/new-lightcounting-report-access-optics-sales-to-increase-in-the-coming-years", "웹 원문 확인"),
    ("coh_id", "optics.org (Coherent Investor Day)", "Coherent execs outline growth strategy", "2025.05.29", "LightCounting(Coherent 발표 인용)", "https://optics.org/news/16/5/47", "웹 원문 확인"),
    ("cig", "Cignal AI", "Optical Component Revenue Reaches Nearly $25B in 2025", "2026.01.07", "Cignal AI", "https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/", "웹 원문 확인"),
    ("cig_1q", "Lightwave (Cignal AI)", "Cignal AI says hyperscaler investment is radically reshaping the optical components market", "2026.06.30", "Cignal AI", "https://www.lightwaveonline.com/home/article/55387778/cignal-ai-says-hyperscaler-investment-is-radically-reshaping-the-optical-components-market", "웹 원문 확인"),
    ("cig_coh", "C114 (Cignal AI)", "CIOE 2025 Cignal AI 발표: 코히어런트 모듈 시장 전망", "2025.09.16", "Cignal AI", "https://m.c114.com.cn/w42-1297031.html", "검색 요약 확인"),
    ("do_ot25", "Dell'Oro Group", "Cloud Providers to Drive Optical Transport Market to $19 Billion in 2029", "2025.07.22", "Dell'Oro", "https://www.delloro.com/newsroom/cloud-providers-to-drive-optical-transport-market-to-19-billion-in-2029/", "웹 원문 확인"),
    ("do_ot_sdx", "SDxCentral (Dell'Oro Group)", "Huawei, Ciena, and Nokia lead $16B optical transport rebound as DCI surges", "2026.02.27", "Dell'Oro", "https://www.sdxcentral.com/news/huawei-ciena-and-nokia-lead-16b-optical-transport-rebound-as-dci-surges/", "웹 원문 확인"),
    ("do_ot26", "Dell'Oro Group", "Optical Transport Equipment Market Forecast to Grow 16 Percent in 2026", "2026.05.19", "Dell'Oro", "https://www.delloro.com/news/optical-transport-equipment-market-forecast-to-grow-16-percent-in-2026/", "웹 원문 확인"),
    ("do_ipo", "Dell'Oro Group", "IPoDWDM Market Forecast to Grow at 27 Percent CAGR", "2026.06.16", "Dell'Oro", "https://www.delloro.com/newsroom/ipodwdm-market-forecast-to-grow-at-27-percent-cagr/?article_lang=en", "웹 원문 확인"),
    ("do_aisw", "Dell'Oro Group", "AI Back-End Switch Market Will Push Past $100 Billion by 2030", "2026.02.04", "Dell'Oro", "https://www.delloro.com/newsroom/ai-back-end-switch-market-will-push-past-100-billion-by-2030/", "웹 원문 확인"),
    ("do_aisw2", "Dell'Oro Group", "AI Back-end Switch Sales to Approach $1 Trillion over the Next Five Years", "2026.07.28", "Dell'Oro", "https://www.delloro.com/news/ai-back-end-switch-sales-to-approach-1-trillion-over-the-next-five-years/", "웹 원문 확인"),
    ("do_capex", "Dell'Oro Group", "AI Boom Drives Data Center Capex to $1.7 Trillion by 2030", "2026.02.11", "Dell'Oro", "https://www.delloro.com/newsroom/ai-boom-drives-data-center-capex-to-1-7-trillion-by-2030/", "웹 원문 확인"),
    ("do_capex2", "TelecomTV (Dell'Oro Group)", "AI buildout maintains momentum as datacentre capex to surpass $3tn by 2030", "2026.08.18", "Dell'Oro", "https://www.telecomtv.com/content/digital-platforms-services/ai-buildout-maintains-momentum-as-datacentre-capex-to-surpass-3tn-by-2030-delloro-group-56102/", "웹 원문 확인"),
    ("do_bb", "Dell'Oro Group", "Broadband Equipment Spending to Peak at $18.8 B in 2028", "2026.01.28", "Dell'Oro", "https://www.delloro.com/news/broadband-equipment-spending-to-peak-at-18-8-b-in-2028/", "웹 원문 확인"),
    ("do_bb25", "Signal Integrity Journal (Dell'Oro Group)", "Broadband Equipment Spending to $20.1 B in 2028 on Accelerated Fiber Deployments", "2025.07", "Dell'Oro", "https://www.signalintegrityjournal.com/articles/4020-broadband-equipment-spending-to-201-b-in-2028-on-accelerated-fiber-deployments", "검색 요약 확인"),
    ("do_dcpon", "Dell'Oro Group", "PON in Data Centers Expected to Grow at 52 Percent CAGR from 2026-2030", "2026.08.05", "Dell'Oro", "https://www.delloro.com/news/pon-in-data-centers-expected-to-grow-at-52-percent-cagr-from-2026-2030/", "웹 원문 확인"),
    ("do_ran", "Dell'Oro Group", "Global RAN Market Stabilization Following Multi-Year Industry Reset", "2026.07.21", "Dell'Oro", "https://www.delloro.com/news/global-ran-market-stabilization-following-multi-year-industry-reset/", "웹 원문 확인"),
    ("do_ran25", "TelecomTV (Dell'Oro Group)", "$160bn in RAN Before 6G, According to Dell'Oro Group", "2025.07", "Dell'Oro", "https://www.telecomtv.com/content/5g/160bn-in-ran-before-6g-according-to-dell-oro-group-53499/", "검색 요약 확인"),
    ("do_airan", "Fierce Network (Dell'Oro Group)", "AI-RAN market to hit $35B by 2030 says Dell'Oro", "2026.06", "Dell'Oro", "https://www.fierce-network.com/wireless/ai-ran-market-hit-35b-2030-says-delloro", "검색 요약 확인"),
    ("mck", "McKinsey & Company", "The cost of compute: A $7 trillion race to scale data centers", "2025.04", "McKinsey", "https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-cost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers", "검색 요약 확인(사이트 자동접속 차단)"),
    ("mrvl26", "Futurum Group (Marvell Investor Day)", "Marvell Investor Day 2026 Targets $80B FY 2031 Revenue With Custom Silicon and Optics", "2026.10", "Marvell", "https://futurumgroup.com/insights/marvell-investor-day-2026-targets-80b-fy-2031-revenue-with-custom-silicon-and-optics/", "검색 요약 확인"),
    ("em_pf", "东方财富 财富号", "全球光纤预制棒产销量排名（CRU 2025‑2026）", "2026.08.07", "CRU", "https://caifuhao.eastmoney.com/news/20260807195607281051400", "웹 원문 확인(개인 게시글, CRU 원문 미확인)"),
    ("em_chip", "东方财富 财富号", "全球光芯片格局深度解析", "2026.04.16", "업계 2차 자료", "https://caifuhao.eastmoney.com/news/20260416214408650573440", "웹 원문 확인(개인 게시글)"),
    ("corning", "Converge Digest (Corning 실적)", "Corning delivers record 2025 results, raises Springboard growth targets", "2026.01", "Corning", "https://convergedigest.com/corning-delivers-record-2025-results-raises-springboard-growth-targets/", "검색 요약 확인"),
    ("att", "Fierce Network", "AT&T unveils $250B investment to expand 5G, fiber, satellite network infrastructure", "2026.03.10", "AT&T", "https://www.fierce-network.com/broadband/att-unveils-250b-investment-expand-5g-fiber-satellite-network-infrastructure", "웹 원문 확인"),
    ("att_dc", "Lightwave", "AT&T’s CEO says a large majority of U.S. data centers are close to its fiber network", "2026 (3Q 실적발표)", "AT&T", "https://www.lightwaveonline.com/home/news/55415762/atts-ceo-says-a-large-majority-of-us-data-centers-are-close-to-its-fiber-network", "웹 원문 확인"),
    ("att_corning", "Fierce Network", "Corning bags $3B fiber supply deal with AT&T", "2026.09", "AT&T·Corning", "https://www.fierce-network.com/broadband/corning-bags-3b-fiber-supply-deal-att", "웹 원문 확인"),
    ("comsoc_capex", "IEEE ComSoc Tech Blog (LightCounting)", "Impact of optical component shortages & bottlenecks explained + Hyperscaler’s CAPEX", "2026.08.14", "LightCounting", "https://techblog.comsoc.org/2026/08/14/impact-of-optical-component-shortages-bottlenecks-explained-hyperscalers-capex/", "웹 원문 확인"),
    ("bit16t", "딜사이트", "빛과전자, 1.6T급 광트랜시버 풀라인업 구축", "2026.01.05", "회사 발표", "https://dealsite.co.kr/articles/154462", "검색 요약 확인"),
]
CODE = {k: f"S{i + 1}" for i, (k, *_r) in enumerate(SRC)}
SRCD = {k: v for (k, *v) in SRC}

# ------------------------------------------------------------------ 구조표 + 밸류체인
# (stream, 사업, 제품, 품목, 설명, 적용, 비고, 해외[], 국내[], 점유율 dict|None, 근거)
U, MS, D = "Upstream", "Midstream", "Downstream"
VC = [
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "DFB 레이저", "전류로 신호를 직접 실어 보내는(직접변조) 가장 보편적인 레이저 칩", "10G·25G FTTH, 5G 프론트홀, 중단거리", "FTTH·ODL",
     ["Broadcom(미국)", "Mitsubishi Electric(일본)", "Sumitomo Electric(일본)", "Lumentum(미국)", "Coherent(미국)", "Yuanjie·源杰(중국)", "Accelink·光迅(중국)", "Mindsemi·敏芯(중국)"], ["오이솔루션"], None, "순서 무관"),
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "EML", "변조기를 내장한 레이저. 고속·장거리에서 신호 품질이 좋음", "레인당 100G·200G(800G·1.6T 모듈), 장거리", "ODL",
     ["Lumentum(미국)", "Sumitomo Electric(일본)", "Broadcom(미국)", "Mitsubishi Electric(일본)", "Coherent(미국)", "Yuanjie·源杰(중국)", "Accelink·光迅(중국)"], ["오이솔루션(100G EML 개발)"],
     {"ov": ["=28.8/87.3", "=20/87.3", "=18.8/87.3", "=7/87.3", "=4.5/87.3", "=3.8/87.3", "n/a"]},
     "400G+용 고속 레이저칩(100G+ EML·50mW+ CW) 2025년 외부판매 점유율. 전체 87.3억위안(灼识咨询, dx p.32)"),
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "CW 레이저(고출력)", "연속광만 내는 외부 광원. 신호 변조는 실리콘포토닉스 칩이 담당", "실리콘포토닉스 800G·1.6T, LPO·CPO 외부광원", "ODL",
     ["Sumitomo Electric(일본)", "Yuanjie·源杰(중국)", "Broadcom(미국)", "Lumentum(미국)", "Mitsubishi Electric(일본)", "Coherent(미국)"], [],
     {"ov": ["=5/15.9", "=3.8/15.9", "=2.8/15.9", "=1.8/15.9", "=0.8/15.9", "n/a"]},
     "400G+ 실리콘포토닉스용 CW 2025년 외부판매 점유율. 전체 15.9억위안(dx p.32)"),
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "VCSEL", "수직 발광 레이저. 저가·저전력, 멀티모드 단거리용", "100m 이내 SR4·SR8(400G·800G), AOC", "ODL",
     ["Coherent(미국)", "Broadcom(미국)", "Lumentum(미국)", "Trumpf(독일)", "Everbright·长光华芯(중국)"], [], None, "순서 무관"),
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "튜너블 레이저(ITLA)", "파장을 바꿀 수 있는 레이저", "DWDM·코히어런트(400ZR·800ZR), 튜너블 SFP+", "ODL",
     ["Lumentum(미국)", "Coherent(미국)", "Furukawa Electric(일본)", "Nokia·Infinera(핀란드)"], [], None, "순서 무관"),
    (U, "광소자 칩(능동)", "레이저(발광) 칩", "펌프 레이저(980nm)", "광증폭기(EDFA)를 구동하는 고출력 레이저", "DCI·장거리 광증폭, CATV", "RF",
     ["Lumentum(미국)", "Coherent(미국)", "Furukawa Electric(일본)", "3SP Technologies(프랑스)"], ["RF머트리얼즈(패키징)"], None, "순서 무관"),
    (U, "광소자 칩(능동)", "수광 칩", "PIN PD", "빛을 전기로 바꾸는 기본형 포토다이오드", "중단거리 수신부(ROSA)", "FTTH·ODL",
     ["Lumentum(미국)", "Broadcom(미국)", "Coherent(미국)", "Sumitomo Electric(일본)", "Mitsubishi Electric(일본)", "Accelink·光迅(중국)", "芯思杰(중국)"], ["우리로"], None, "순서 무관"),
    (U, "광소자 칩(능동)", "수광 칩", "APD", "수신 신호를 내부 증폭하는 고감도 포토다이오드", "장거리, PON OLT 수신부", "FTTH·ODL",
     ["Mitsubishi Electric(일본)", "Sumitomo Electric(일본)", "Broadcom(미국)", "Coherent(미국)", "三安集成(중국)", "Mindsemi·敏芯(중국)"], ["우리로"], None, "순서 무관"),
    (U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 PIC", "실리콘 웨이퍼에 변조기·도파로·수광부를 집적(광원은 외부 CW 레이저)", "800G·1.6T DR/FR, CPO 광엔진", "ODL",
     ["Broadcom(미국)", "Marvell(미국)", "Cisco·Acacia(미국)", "Coherent(미국)", "Innolight·中际旭创(중국, 자체 설계)", "TSMC(대만, 위탁생산)", "Tower Semiconductor(이스라엘, 위탁생산)", "GlobalFoundries(미국, 위탁생산)"], [], None, "순서 무관"),
    (U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "InP PIC", "인화인듐 기반으로 레이저·변조기를 한 칩에 집적", "코히어런트 장거리·DCI", "ODL",
     ["Nokia·Infinera(핀란드)", "Lumentum(미국)", "Coherent(미국)"], [], None, "순서 무관"),
    (U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "TFLN 변조기", "박막 니오브산리튬 기반 초고속 변조기", "레인당 200G·400G 차세대 모듈, 코히어런트", "ODL",
     ["HyperLight(미국)", "Fujitsu Optical Components(일본)", "Sumitomo Osaka Cement(일본)", "AFR·光库(중국)"], [], None, "순서 무관"),
    (U, "전기 칩(IC)", "DSP", "PAM4 DSP", "고속 전기신호를 4단계 신호로 변환·보정하는 핵심 칩", "400G·800G·1.6T 데이터센터 모듈", "ODL",
     ["Broadcom(미국)", "Marvell(미국)", "Credo(미국)", "MaxLinear(미국)"], [], None, "Broadcom·Marvell 합산 고속 PAM4 DSP 점유율 90% 이상(CAICT, aj p.21)"),
    (U, "전기 칩(IC)", "DSP", "코히어런트 DSP", "빛의 위상·편광까지 쓰는 장거리용 DSP", "400ZR·800ZR, 장거리 트랜스폰더", "ODL",
     ["Marvell(미국)", "Cisco·Acacia(미국)", "Ciena(미국)", "Nokia·Infinera(핀란드)", "NTT Innovative Devices(일본)"], [], None, "순서 무관"),
    (U, "전기 칩(IC)", "아날로그 IC", "TIA", "수광 소자가 만든 미세 전류를 전압 신호로 증폭", "수신부(ROSA)", "공통",
     ["Marvell(미국)", "Broadcom(미국)", "Semtech(미국)", "MACOM(미국)", "Analog Devices(미국)"], [], None, "순서 무관"),
    (U, "전기 칩(IC)", "아날로그 IC", "레이저·변조기 드라이버", "레이저·변조기를 구동하는 고속 증폭기", "송신부(TOSA), LPO", "공통",
     ["Semtech(미국)", "MACOM(미국)", "Marvell(미국)", "Broadcom(미국)", "Analog Devices(미국)"], [], None, "순서 무관"),
    (U, "전기 칩(IC)", "아날로그 IC", "CDR·리타이머", "신호의 타이밍(클럭)을 복원해 잡음을 줄이는 칩", "광트랜시버 내장, LRO", "공통",
     ["Marvell(미국)", "Broadcom(미국)", "Semtech(미국)", "MACOM(미국)", "Credo(미국)"], [], None, "순서 무관"),
    (U, "전기 칩(IC)", "PON SoC", "PON 칩셋(OLT·ONU SoC)", "PON 장비와 ONU 스틱의 통신 처리 칩", "GPON·XGS-PON ONT/OLT", "FTTH",
     ["Broadcom(미국)", "Realtek(대만)", "Sanechips·中兴微(중국)", "HiSilicon(중국)"], ["자람테크놀로지"], None, "순서 무관"),
    (U, "광 수동부품", "광 신호제어", "광 아이솔레이터", "반사된 빛이 레이저로 되돌아오지 않게 막는 부품", "송신부·레이저 보호", "공통",
     ["Coherent(미국)", "Sumitomo(일본)", "TFC·天孚(중국)"], [], None, "순서 무관"),
    (U, "광 수동부품", "광 신호제어", "WDM 필터·AWG", "여러 파장을 합치거나 나누는 부품", "CWDM·LWDM 모듈(FR4), DWDM, PON", "공통",
     ["Shijia·仕佳光子(중국)", "Broadex·博创(중국)", "Accelink·光迅(중국)", "Lumentum(미국)", "Corning·AFOP(미국)", "腾景科技(중국)"], ["한국첨단소재(구 피피아이)", "우리로"], None, "순서 무관"),
    (U, "광 수동부품", "광 신호제어", "PLC 스플리터", "광신호 하나를 여러 가입자에게 나눠 주는 분배기", "FTTH 광분배망", "FTTH",
     ["Shijia·仕佳光子(중국)", "Broadex·博创(중국)", "Accelink·光迅(중국)"], ["한국첨단소재(구 피피아이)", "우리로"], None, "순서 무관"),
    (U, "광 수동부품", "광 연결·결합", "렌즈·FAU", "빛을 모으는 렌즈와 광섬유를 칩 앞에 정렬하는 광섬유 어레이(FAU)", "TOSA·ROSA·광엔진 내부, CPO", "ODL",
     ["TFC·天孚(중국)", "Focuslight·炬光(중국)", "Coherent(미국)", "Accelink·光迅(중국)"], [], None, "순서 무관"),
    (U, "광 수동부품", "광 연결·결합", "광커넥터·페룰·MPO", "광섬유 끝을 정밀하게 맞대어 잇는 연결 부품(LC·MPO, 지르코니아 페룰)", "광케이블·패치코드 양 끝, 장비·모듈 포트", "공통",
     ["US Conec(미국)", "Senko(일본)", "Corning(미국)", "Fujikura(일본)", "Sumitomo Electric(일본)", "CCTC·三环(중국)", "T&S·太辰光(중국)"], [], None, "순서 무관"),
    (U, "패키징·기판", "패키지·방열", "TO-CAN·세라믹·버터플라이 패키지", "레이저·수광 칩을 담는 금속·세라믹 하우징", "통신용 TO-CAN, 기밀 패키지(텔레콤·방산)", "공통",
     ["Kyocera(일본)", "Schott(독일)", "Niterra·NTK(일본)"], ["RF머트리얼즈"], None, "순서 무관"),
    (U, "패키징·기판", "패키지·방열", "TEC(열전소자)", "레이저 온도를 일정하게 유지하는 냉각 소자", "EML·DWDM·튜너블 모듈", "ODL",
     ["Ferrotec(일본)", "KELK(일본)", "Phononic(미국)", "富信科技(중국)"], [], None, "순서 무관"),
    (U, "패키징·기판", "패키지·방열", "광모듈 PCB", "칩을 직접 실장하는 고다층·mSAP 기판(COB 구조의 중심)", "800G·1.6T 모듈", "ODL",
     ["Unimicron·欣兴(대만)", "Shengyi·生益电子(중국)"], [], None, "aj p.24 주요 업체"),
    (U, "반도체 기판·에피", "화합물·SOI 웨이퍼", "InP 기판", "DFB·EML·CW 레이저가 만들어지는 기판(현재 공급 병목)", "레이저·수광 칩", "공통",
     ["Sumitomo Electric(일본)", "AXT·北京通美(미국)", "JX Advanced Metals(일본)"], [], None, "순서 무관"),
    (U, "반도체 기판·에피", "화합물·SOI 웨이퍼", "GaAs 기판", "VCSEL을 만드는 기판", "VCSEL", "ODL",
     ["Freiberger(독일)", "Sumitomo Electric(일본)", "AXT(미국)"], [], None, "순서 무관"),
    (U, "반도체 기판·에피", "화합물·SOI 웨이퍼", "에피웨이퍼", "기판 위에 발광층을 성장시킨 웨이퍼", "레이저 칩 외주 생산", "공통",
     ["IQE(영국)", "LandMark·聯亞(대만)", "VPEC·全新(대만)"], [], None, "순서 무관"),
    (U, "반도체 기판·에피", "화합물·SOI 웨이퍼", "SOI 웨이퍼", "실리콘포토닉스 칩용 웨이퍼", "실리콘포토닉스 PIC", "ODL",
     ["Soitec(프랑스)", "Shin-Etsu(일본)"], [], None, "순서 무관"),
    (U, "광섬유 소재", "프리폼·광섬유", "프리폼(모재)", "고순도 석영 유리봉. 고온에서 뽑아 광섬유를 만듦(광섬유 원가의 65~70%)", "VAD·OVD·PCVD 공정", "FTTH",
     ["YOFC·长飞(중국)", "Corning(미국)", "Hengtong·亨通(중국)", "ZTT·中天(중국)", "FiberHome·烽火(중국)", "Furukawa·OFS(일본)", "Sumitomo Electric(일본)", "Fujikura(일본)", "STL(인도)"], ["대한광통신"],
     {"ov": ["17~19%", "14~16%", "10~12%", "9~11%", "8~9%", "7~8%", "5~7%", "4~5%", "2~4%"]},
     "CRU 2025~26년 생산량 기준 점유율(东方财富 게시글 인용, CRU 원문 미확인)"),
    (U, "광섬유 소재", "프리폼·광섬유", "단일모드 광섬유(SMF)", "빛이 한 경로로만 진행해 손실이 적은 광섬유", "장거리·DCI(G.652·G.657·초저손실)", "FTTH",
     ["Corning(미국)", "YOFC·长飞(중국)", "Hengtong·亨通(중국)", "ZTT·中天(중국)", "FiberHome·烽火(중국)", "Fujikura(일본)", "Sumitomo Electric(일본)", "Furukawa·OFS(일본)", "Prysmian(이탈리아)"], ["대한광통신", "LS전선"], None, "순서 무관"),
    (U, "광섬유 소재", "프리폼·광섬유", "멀티모드 광섬유(MMF)", "코어가 굵어 여러 경로로 빛이 진행, 수백 m 이내 연결", "데이터센터 내부(OM3·OM4·OM5)", "ODL",
     ["Corning(미국)", "Prysmian(이탈리아)", "Furukawa·OFS(일본)", "YOFC·长飞(중국)"], [], None, "순서 무관"),
    (U, "제조·검사 장비", "공정·계측 장비", "MOCVD·능동정렬/본딩·광 계측", "에피 성장, 광축 능동정렬, 성능 측정 장비", "칩·모듈 생산, CPO 조립", "공통",
     ["Aixtron(독일)", "ficonTEC(독일)", "ASMPT(싱가포르)", "Keysight(미국)", "Anritsu(일본)", "EXFO(캐나다)"], ["성호전자(ADS테크, 능동정렬 장비)", "이노인스트루먼트"], None, "성호전자 자회사 ADS테크는 광트랜시버·CPO 능동정렬 장비 업체(im)"),
    (U, "RF 소자(무선)", "RF 반도체·부품", "GaN RF 트랜지스터·PA", "기지국·레이더용 고출력 RF 증폭 반도체", "5G·AI-RAN 기지국, 방산 레이더·위성", "-",
     ["MACOM(미국)", "Qorvo(미국)", "Sumitomo Electric·SEDI(일본)", "NXP(네덜란드)"], ["RFHIC", "웨이비스"], None, "순서 무관"),
    (U, "RF 소자(무선)", "RF 반도체·부품", "RF 필터·안테나 부품", "기지국 주파수 필터와 안테나 부품", "5G RU·안테나", "-",
     ["Comba Telecom(중국)", "Amphenol(미국)"], ["케이엠더블유"], None, "순서 무관"),
    (U, "RF 소자(무선)", "RF 반도체·부품", "RF 케이블·커넥터", "고주파 신호용 케이블·커넥터", "기지국·방산·위성", "-",
     ["Rosenberger(독일)", "Huber+Suhner(스위스)", "Amphenol(미국)"], ["센서뷰"], None, "순서 무관"),
    # ---------------- Midstream
    (MS, "광 서브어셈블리(OSA)", "광소자 패키징", "TO-CAN(LD·PD)", "칩을 TO 패키지에 넣은 기본 광소자", "저·중속 트랜시버, BOSA", "FTTH·ODL",
     ["Accelink·光迅(중국)", "Source Photonics·索尔思(중국)", "Hisense Broadband·纳真(중국)", "HGG·华工正源(중국)"], ["빛과전자", "오이솔루션"], None, "순서 무관"),
    (MS, "광 서브어셈블리(OSA)", "광소자 패키징", "TOSA·ROSA", "송신부(TOSA)·수신부(ROSA) 광학 조립체", "트랜시버 핵심 부품(TO-CAN 모듈 원가 TOSA 35%·ROSA 23%)", "ODL",
     ["TFC·天孚(중국)", "Accelink·光迅(중국)", "Sumitomo Electric(일본)", "Coherent(미국)", "Source Photonics·索尔思(중국)", "O-Net·昂纳(중국)", "HGG·华工正源(중국)"], ["오이솔루션", "빛과전자"], None, "순서 무관"),
    (MS, "광 서브어셈블리(OSA)", "광소자 패키징", "BOSA", "송·수신을 한 패키지에 담은 양방향 조립체(광섬유 1가닥 사용)", "FTTH ONU, 양방향(Bi-Di) SFP", "FTTH",
     ["Hisense Broadband·纳真(중국)", "Accelink·光迅(중국)", "Source Photonics·索尔思(중국)"], ["빛과전자"], None, "순서 무관"),
    (MS, "광 서브어셈블리(OSA)", "광소자 패키징", "광엔진(COB·CPO/NPO용)", "칩을 PCB에 직접 실장한 고속 송수신 엔진", "800G·1.6T 모듈, CPO·NPO 스위치", "ODL",
     ["Broadcom(미국)", "NVIDIA(미국)", "TSMC(대만)", "Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Coherent(미국)", "TFC·天孚(중국)", "Fabrinet(태국, 위탁생산)"], [], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "광트랜시버 전체", "2025년 매출 순위(LightCounting)", "광모듈 매출 기준 상위 10개사(DWDM 모듈 업체 제외)", "-", "ODL",
     ["Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Coherent(미국, 3위 추정)", "Accelink·光迅(중국)", "Molex·Lumentum 중 1곳(5위)", "Hisense Broadband·纳真(중국)", "HGG·华工正源(중국)", "Source Photonics·索尔思(중국)", "Molex·Lumentum 중 1곳(9위)", "Cambridge·剑桥(중국)"], [],
     {"ov": ["=5.333/23.8", "=3.5/23.8", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a"]},
     "LightCounting Top10(lc_top10). 점유율 = 2025년 매출(Innolight 53.33억, Eoptolink 35억달러) ÷ 시장 238억달러(lc_mar)"),
    (MS, "ODL(광트랜시버)", "저속 트랜시버(~10G)", "SFP(1G)·SFP+(10G)·XFP", "가장 작은 표준 규격의 1~10G 광트랜시버", "기업망, LTE 프론트홀, FTTH 백홀", "ODL",
     ["Coherent(미국)", "Accelink·光迅(중국)", "Hisense Broadband·纳真(중국)", "Source Photonics·索尔思(중국)", "HGG·华工正源(중국)", "Eoptolink·新易盛(중국)"], ["빛과전자", "오이솔루션", "옵티코어"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "중속 트랜시버(25G~100G)", "SFP28(25G)·QSFP+(40G)·QSFP28(100G)", "4채널 묶음(QSFP) 등 25~100G 모듈", "5G 프론트홀(25G), 데이터센터 100G", "ODL",
     ["Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Accelink·光迅(중국)", "Hisense Broadband·纳真(중국)", "Coherent(미국)", "AAOI(미국)", "HGG·华工正源(중국)"], ["오이솔루션", "옵티코어", "빛과전자"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "400G·800G(QSFP-DD·OSFP)", "AI 데이터센터 주력 제품(800G = 100G×8채널)", "GPU 클러스터 스케일아웃, 스위치 포트", "ODL",
     ["Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Coherent(미국)", "Accelink·光迅(중국)", "Lumentum(미국)", "Cisco(미국)", "HGG·华工正源(중국)", "AAOI(미국)"], ["오이솔루션", "옵티코어", "빛과전자"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "1.6T·3.2T(OSFP 등)", "차세대 모듈(1.6T = 200G×8채널), 3.2T는 개발 단계", "차세대 AI 클러스터(2026년~)", "ODL",
     ["Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Coherent(미국)", "Lumentum(미국)"], ["오이솔루션(2H26 투입 계획)", "빛과전자(1.6T OSFP 라인업)"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "코히어런트 트랜시버", "400ZR/ZR+·800ZR/ZR+·CFP2-DCO", "라우터·스위치에 바로 꽂는 장거리용 코히어런트 모듈", "데이터센터 간 연결(DCI), 메트로", "ODL",
     ["Cisco·Acacia(미국)", "Marvell(미국)", "Ciena(미국)", "Nokia·Infinera(핀란드)", "Coherent(미국)", "Lumentum(미국)", "Accelink·光迅(중국)"], [], None, "1Q26 ZR/ZR+ 출하 1위 Cisco Acacia, 2위 Marvell(Dell'Oro, do_ipo). 3위 이하 순서 무관"),
    (MS, "ODL(광트랜시버)", "무선 프론트홀·백홀 트랜시버", "10G·25G(그레이·CWDM·DWDM·튜너블)", "기지국 무선부(RU)와 DU를 잇는 광모듈", "LTE·5G 프론트홀, 백홀", "ODL(무선)",
     ["Accelink·光迅(중국)", "Hisense Broadband·纳真(중국)", "HGG·华工正源(중국)", "Eoptolink·新易盛(중국)", "Source Photonics·索尔思(중국)"], ["오이솔루션", "옵티코어", "빛과전자"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "차세대 인터커넥트", "LPO·LRO(선형 구동)", "DSP를 빼거나 줄여 전력을 낮춘 플러그형 모듈", "AI 클러스터 단거리", "ODL",
     ["Eoptolink·新易盛(중국)", "Innolight·中际旭创(중국)", "Coherent(미국)"], [], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "차세대 인터커넥트", "AOC·DAC(케이블 일체형)", "AOC는 트랜시버 일체형 광케이블, DAC는 구리 직결 케이블", "랙 내부·인접 랙 연결", "ODL",
     ["Innolight·中际旭创(중국)", "Eoptolink·新易盛(중국)", "Coherent(미국)", "NVIDIA·Mellanox(미국)", "Amphenol(미국)", "Molex(미국)", "Luxshare(중국)"], ["옵티시스"], None, "순서 무관"),
    (MS, "ODL(광트랜시버)", "차세대 인터커넥트", "CPO(광 공동패키징)", "스위치·GPU 칩 바로 옆에 광엔진을 함께 패키징", "스케일아웃 스위치(2026년~), 스케일업(2028년~)", "ODL",
     ["Broadcom(미국)", "NVIDIA(미국)", "Marvell·Celestial AI(미국)", "Cisco(미국)", "Ayar Labs(미국)", "Ranovus(캐나다)"], ["오이솔루션(개발 로드맵)"], None, "순서 무관"),
    (MS, "FTTH(광가입자망·PON)", "OLT용 트랜시버", "GPON·XGS-PON·50G-PON OLT", "통신사 국사 장비(OLT)에 꽂는 PON 광모듈", "광가입자망 국사", "FTTH",
     ["Hisense Broadband·纳真(중국)", "Source Photonics·索尔思(중국)", "Accelink·光迅(중국)", "HGG·华工正源(중국)", "Eoptolink·新易盛(중국)"], ["빛과전자"], None, "순서 무관"),
    (MS, "FTTH(광가입자망·PON)", "ONU·ONT용 광부품", "ONU BOSA·SFP ONU 스틱", "가입자 댁내 단말(ONT)에 들어가는 광부품", "가정·기업 광단말", "FTTH",
     ["Hisense Broadband·纳真(중국)", "Accelink·光迅(중국)", "Source Photonics·索尔思(중국)"], ["빛과전자"], None, "순서 무관"),
    (MS, "RF(아날로그 광·RF-optics)", "CATV·HFC 광전송", "아날로그 광송신기·광수신기(노드)", "케이블TV 신호(RF)를 빛에 실어 보내고 받는 장치", "케이블TV·HFC 망", "RF",
     ["AAOI(미국)", "Teleste(핀란드)", "Vecima(캐나다)"], ["빛과전자"], None, "순서 무관"),
    (MS, "RF(아날로그 광·RF-optics)", "광증폭·RoF", "EDFA 광증폭기", "광신호를 전기로 바꾸지 않고 바로 증폭", "DCI·장거리, CATV", "RF",
     ["Lumentum(미국)", "Coherent(미국)", "Accelink·光迅(중국)", "O-Net·昂纳(중국)"], ["RF머트리얼즈"], None, "순서 무관"),
    (MS, "RF(아날로그 광·RF-optics)", "광증폭·RoF", "RoF·DAS 광모듈", "무선 신호를 광섬유로 전달(중계기·DAS)", "건물 내 이동통신 중계, 지하철", "RF",
     ["Amphenol(미국, 구 CommScope DAS)", "Corning(미국)", "JMA Wireless(미국)"], ["쏠리드", "에프알텍"], None, "순서 무관"),
    (MS, "무선 RF 모듈", "기지국 RF 모듈", "RU·안테나·PA 모듈", "기지국 무선부(라디오·안테나·증폭기)", "5G·AI-RAN 기지국", "-",
     ["Ericsson(스웨덴)", "Nokia(핀란드)", "Comba Telecom(중국)"], ["케이엠더블유", "RFHIC"], None, "순서 무관"),
    (MS, "광케이블", "광케이블", "통신망용 광케이블", "광섬유 다발에 보호 피복을 씌운 케이블", "기간망·가입자망(FTTH 드롭)·해저", "FTTH",
     ["Corning(미국)", "YOFC·长飞(중국)", "ZTT·中天(중국)", "Hengtong·亨通(중국)", "FiberHome·烽火(중국)", "Prysmian(이탈리아)", "Fujikura(일본)", "Sumitomo Electric(일본)"], ["LS전선", "대한광통신", "티엠씨(선박·해양용)", "LS마린솔루션(해저 시공)"], None, "순서 무관(점유율 자료는 범용 시장조사 출처라 제외)"),
    (MS, "광케이블", "광케이블", "데이터센터용 고밀도 케이블", "수천 심을 좁은 공간에 담는 리본·MPO 트렁크 케이블", "AI 데이터센터 내부·캠퍼스 연결", "ODL",
     ["Corning(미국)", "Fujikura(일본)", "Sumitomo Electric(일본)", "Prysmian(이탈리아)", "YOFC·长飞(중국)"], ["대한광통신"], None, "순서 무관"),
    # ---------------- Downstream
    (D, "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 백엔드·프론트엔드 스위치", "GPU·서버를 잇는 이더넷·인피니밴드 스위치(광모듈 최대 수요처)", "AI 클러스터 스케일업·스케일아웃", "ODL",
     ["NVIDIA(미국)", "Arista(미국)", "Cisco(미국)", "Celestica(캐나다)", "Huawei(중국)", "HPE·Juniper(미국)", "Accton(대만)"], ["유비쿼스(통신·기업망)", "다산네트웍스(기업망)"], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 가속기 시스템(GPU 랙)", "GPU 랙 단위 시스템. 광모듈을 직접 조달하기도 함", "AI 학습·추론", "ODL",
     ["NVIDIA(미국)", "Google·TPU(미국)", "AMD(미국)"], [], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "광전송 장비", "WDM·OTN·ROADM(장거리·메트로)", "여러 파장을 묶어 장거리로 보내는 전송 장비", "통신사 기간망·메트로", "ODL",
     ["Huawei(중국)", "Ciena(미국)", "Nokia(핀란드)", "ZTE(중국)", "Cisco(미국)", "1Finity·Fujitsu(일본)"], ["코위버", "우리넷", "텔레필드"], None, "2025년 매출 상위 3사 Huawei·Ciena·Nokia(Dell'Oro, do_ot_sdx). 4위 이하 순서 무관"),
    (D, "네트워크 장비(시스템)", "광전송 장비", "DCI·분리형 OLS·IPoDWDM", "데이터센터 간 연결 전용 장비. 광계층(OLS)을 분리해 구매", "하이퍼스케일러 DCI(스케일어크로스)", "ODL",
     ["Ciena(미국)", "Nokia(핀란드)", "Cisco(미국)"], [], None, "분리형 WDM 점유율 Ciena 약 40%, 2위 Nokia(1Q26, do_ipo)"),
    (D, "네트워크 장비(시스템)", "광전송 장비", "패킷 전송(PTN·MSPP)", "이더넷 패킷을 광으로 전송하는 장비", "통신사 메트로·백홀", "ODL",
     ["Huawei(중국)", "ZTE(중국)", "Nokia(핀란드)"], ["우리넷", "코위버"], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "유선 액세스 장비", "PON OLT·ONT·FTTR·가입자 CPE", "광가입자망 국사 장비와 댁내 단말", "FTTH(미국 BEAD 등 정부 보조사업 포함)", "FTTH",
     ["Huawei(중국)", "ZTE(중국)", "Nokia(핀란드)", "FiberHome(중국)", "Calix(미국)", "Adtran(미국)"], ["다산네트웍스", "유비쿼스", "머큐리", "에치에프알", "가온그룹(광단말·CPE)"], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "유선 액세스 장비", "데이터센터 PON", "데이터센터 관리망(OOB)·인프라 관리망에 PON 적용", "하이퍼스케일러·네오클라우드·코로케이션(2026년~)", "FTTH",
     [], [], None, "업체 공개 자료 미확인"),
    (D, "네트워크 장비(시스템)", "무선 장비", "RAN·AI-RAN·프론트홀·중계 장비", "이동통신 기지국과 프론트홀·중계·계측 장비", "5G·5G-A, 미국 주파수 경매 후 투자", "ODL(무선)",
     ["Ericsson(스웨덴)", "Nokia(핀란드)", "Huawei(중국)", "ZTE(중국)"], ["삼성전자", "에치에프알", "쏠리드", "케이엠더블유", "이노와이어리스"], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "케이블 HFC 장비", "DAA·Remote PHY·광노드", "케이블망의 분산형 접속 장비", "케이블TV·초고속인터넷(DOCSIS 4.0)", "RF",
     ["Harmonic(미국)", "Vecima(캐나다)", "Teleste(핀란드)"], [], None, "순서 무관"),
    (D, "네트워크 장비(시스템)", "위성·방산 통신", "위성통신 단말·방산 통신장비", "군 위성통신·레이더·전술통신 장비", "국방·우주", "-",
     ["L3Harris(미국)", "Viasat(미국)", "Thales(프랑스)"], ["RF시스템즈", "이노와이어리스"], None, "순서 무관"),
    (D, "최종 수요처", "데이터센터 사업자", "하이퍼스케일러·네오클라우드", "AI 데이터센터를 짓고 광모듈을 대량 구매하는 사업자", "AI·클라우드", "ODL",
     ["Microsoft(미국)", "Amazon·AWS(미국)", "Google(미국)", "Meta(미국)", "Oracle(미국)", "CoreWeave(미국)"], ["네이버", "카카오"], None, "순서 무관"),
    (D, "최종 수요처", "통신 사업자", "통신사·케이블 MSO", "유무선 통신망에 투자하는 사업자", "FTTH·5G·백본", "FTTH·ODL·RF",
     ["AT&T(미국)", "Verizon(미국)", "T-Mobile(미국)", "China Mobile(중국)", "NTT(일본)", "Comcast(미국)", "Charter(미국)"], ["SK텔레콤", "KT", "LG유플러스"], None, "순서 무관"),
]

STREAM_BAND = {
    U: "Upstream — 소재·칩·부품 (광모듈 向 소재)",
    MS: "Midstream : 광부품·광모듈 (빛과전자 FTTH·ODL·RF 등)",
    D: "Downstream : 장비·최종 수요처",
}

THEME = [
    ("무선 투자·미국 주파수 경매·AI-RAN", "RFHIC", "Upstream > RF 소자 > GaN RF 트랜지스터·PA", "기지국용 GaN 증폭기"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "케이엠더블유", "Midstream > 무선 RF 모듈 > RU·안테나", "RU·안테나·필터"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "오이솔루션", "Midstream > ODL > 무선 프론트홀 트랜시버", "프론트홀 광트랜시버, 데이터센터 800G·1.6T 확대"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "쏠리드", "Downstream > 무선 장비 / Midstream > RoF·DAS", "중계기·DAS·O-RAN RU"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "이노와이어리스", "Downstream > 무선 장비", "기지국 계측·스몰셀"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "에치에프알", "Downstream > 무선 장비", "모바일 프론트홀 장비"),
    ("유선 투자·BEAD", "대한광통신", "Upstream > 광섬유 소재 / Midstream > 광케이블", "프리폼·광섬유·광케이블, 북미 인캡 인수(2Q25)"),
    ("유선 투자·BEAD", "자람테크놀로지", "Upstream > 전기 칩 > PON 칩셋", "PON SoC"),
    ("유선 투자·BEAD", "가온그룹", "Downstream > 유선 액세스 장비", "광단말·셋톱 등 가입자 CPE"),
    ("유선 투자·BEAD", "에치에프알", "Downstream > 유선 액세스 장비", "광 액세스 장비"),
    ("데이터센터 광통신", "RF머트리얼즈", "Upstream > 패키지·펌프 레이저 / Midstream > EDFA", "Lumentum향 광 패키징·펌프 레이저·EDFA"),
    ("데이터센터 광통신", "대한광통신", "Midstream > 광케이블 > 데이터센터용", "데이터센터·백본 광케이블"),
    ("데이터센터 광통신", "오이솔루션", "Midstream > ODL 400G·800G·1.6T / Upstream > EML", "2025년 매출 트랜시버 90%·레이저칩 10%"),
    ("데이터센터 광통신", "성호전자", "Upstream > 제조·검사 장비(자회사 ADS테크)", "광트랜시버·CPO 능동정렬 장비(모듈 제조사 아님)"),
    ("방산·우주 통신", "RFHIC", "Upstream > RF 소자 > GaN", "방산 레이더·위성용 GaN"),
    ("방산·우주 통신", "웨이비스", "Upstream > RF 소자 > GaN", "방산용 GaN RF"),
    ("방산·우주 통신", "RF시스템즈", "Downstream > 위성·방산 통신", "위성통신 단말·안테나"),
    ("방산·우주 통신", "센서뷰", "Upstream > RF 소자 > RF 케이블·커넥터", "RF 케이블·커넥터"),
    ("방산·우주 통신", "이노와이어리스", "Downstream > 위성·방산 통신", "통신 계측"),
]

# ------------------------------------------------------------------ 시장규모 행
M = []


def m(key, s, b, p, item, scope, unit, src, g, hz, orig, cite, loc, grade, note, special=None, pct=False):
    M.append(dict(key=key, s=s, b=b, p=p, item=item, scope=scope, unit=unit, src=src, g=g, hz=hz, orig=orig,
                  cite=cite, loc=loc, grade=grade, note=note, special=special or {}, pct=pct))


LA = dict(orig="源杰科技 자료(爱建证券 인용)", cite="aj", loc="p.14 도표26", grade="B")
# Upstream
m("chips", U, "광소자 칩(능동)", "광칩 전체", "광칩 전체(LightCounting)", "레이저·수광·실리콘포토닉스 칩", "USD bn",
  {2025: 4.0, 2031: 15.0}, None, 2031, "LightCounting(2026.10)", "lc_chips", "-", "B",
  "2031년 InP 기반 광칩 69억달러(전체의 46%)가 hd PDF p.2와 일치")
m("inp_chips", U, "광소자 칩(능동)", "광칩 전체", " └ InP 기반 광칩(EML·DFB·CW 등)", "광칩 중 InP 기판 기반", "USD bn",
  {2031: 6.9}, None, 2031, "LightCounting(2026.10)", "hd", "p.2", "B",
  "비중 2025년 58% → 2031년 46%(금액 기준). 2025년 = 광칩 전체 × 58%",
  special={2025: "=I{chips}*0.58"})
m("laser", U, "광소자 칩(능동)", "레이저(발광) 칩", "레이저 칩 전체(源杰)", "광통신용 레이저 칩", "USD bn",
  {2025: 3.90, 2026: 6.00, 2027: 8.70, 2028: 11.90, 2029: 17.60, 2030: 22.90}, None, 2030,
  note="2030년 값이 LightCounting 광칩 전체(위 행)보다 큼. 회사 자료(IPO 목적)로 정의·추정 방식 상이", **LA)
m("cw", U, "광소자 칩(능동)", "레이저(발광) 칩", " └ CW 레이저 칩", "실리콘포토닉스·CPO용 외부 광원", "USD bn",
  {2025: 0.20, 2026: 0.90, 2027: 1.90, 2028: 3.30, 2029: 6.40, 2030: 10.10}, None, 2030, note="", **LA)
m("eml", U, "광소자 칩(능동)", "레이저(발광) 칩", " └ EML 칩", "EML 레이저 칩", "USD bn",
  {2025: 1.90, 2026: 3.10, 2027: 4.80, 2028: 6.60, 2029: 9.10, 2030: 10.70}, None, 2030, note="100G 이하·200G 이상 세부는 원문 표 참조", **LA)
m("oth", U, "광소자 칩(능동)", "레이저(발광) 칩", " └ 기타 레이저(DFB·VCSEL·FP 등)", "EML·CW 외 레이저 칩", "USD bn",
  {2025: 1.80, 2026: 1.90, 2027: 2.00, 2028: 2.00, 2029: 2.10, 2030: 2.10}, None, 2030, note="", **LA)
m("dclaser", U, "광소자 칩(능동)", "레이저(발광) 칩", "데이터센터용 레이저 칩", "데이터센터 수요분", "USD bn",
  {2030: 21.1}, 0.534, 2030, "LightCounting·灼识咨询(CIC)", "dx", "p.8", "B", "2024년 16억달러, CAGR 53.4%(2024~30). 같은 해 전체 26억→229억달러")
m("vcsel_u", U, "광소자 칩(능동)", "레이저(발광) 칩", "VCSEL 출하량", "", "억 개",
  {2031: 6.5}, 0.38, 2031, "LightCounting(2026.10)", "lc_chips", "-", "C", "2025~31년 출하량 CAGR 38%. 금액 미공개")
m("pd", U, "광소자 칩(능동)", "수광 칩", "PIN·APD 수광 칩", "", "USD bn", {}, None, None, "-", "-", "-", "-", "개별 금액 미공개")
m("siph", U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 칩(LightCounting)", "SiPh 칩 매출(TFLN 제외)", "USD bn",
  {2029: 3.0}, "=(3.0/0.8)^(1/6)-1", 2029, "LightCounting(2024.5)", "lc_siph", "본문", "B",
  "2023년 8억달러. 광칩 중 SiPh 비중 32%(2025)→42%(2031)는 출하량 기준(aj p.15)이라 금액 환산에 쓰지 않음")
m("siph_y", U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 PIC 다이(Yole)", "PIC 다이 기준(좁은 정의)", "USD bn",
  {2029: 0.863}, 0.45, 2029, "Yole Group", "yole_siph", "본문", "B", "2023년 9,500만달러, CAGR 45%")
m("tfln", U, "광소자 칩(능동)", "광집적회로(PIC)·변조기", "TFLN 변조기 PIC", "", "USD bn",
  {2029: 0.75}, None, 2029, "LightCounting(2024.5)", "lc_siph", "본문", "B", "현재 거의 0에서 성장")
m("chipset", U, "전기 칩(IC)", "광트랜시버용 IC 칩셋", "광통신 IC 칩셋(LightCounting)", "DSP·드라이버·TIA·CDR 등 전기 칩", "USD bn",
  {2030: 11.0}, 0.17, 2030, "LightCounting(2025.3)", "lc_chipset", "본문", "B",
  "2024년 약 35억달러, CAGR 17%(2025~30). 기사 제목의 '光芯片'은 칩셋(전기 IC) 시장의 오기 → 광칩과 별개 시장")
m("mrvl", U, "전기 칩(IC)", "광트랜시버용 IC 칩셋", "데이터센터 인터커넥트 TAM(Marvell)", "DSP·TIA·드라이버·AEC 등", "USD bn",
  {2028: 19.0}, 0.35, 2028, "650 Group·Cignal AI·Dell'Oro·LightCounting·Marvell", "mrvl", "slide 16", "A",
  "CY23 43억달러. 2026.10 인베스터데이: CY30 인터커넥트 TAM 약 650억달러(mrvl26)")
m("dsp", U, "전기 칩(IC)", "DSP", "PAM4·코히어런트 DSP", "", "USD bn", {}, None, None, "-", "lc_chipset", "-", "-",
  "개별 금액 미공개(칩셋 행에 포함). 코히어런트 DSP 출하 2030년 500만 개 초과")
m("ponsoc", U, "전기 칩(IC)", "PON SoC", "PON 칩셋", "", "USD bn", {}, None, None, "-", "-", "-", "-", "공개 자료 미확인")
m("passive", U, "광 수동부품", "수동부품 전체", "PLC·AWG·커넥터·렌즈·아이솔레이터", "", "USD bn", {}, None, None, "-", "-", "-", "-",
  "공신력 있는 금액 자료 미확인(범용 시장조사 출처 제외)")
m("inp_sub", U, "반도체 기판·에피", "화합물·SOI 웨이퍼", "InP 기판", "2인치 환산 128만 장", "USD bn",
  {2026: 0.2}, None, 2026, "Yole Group", "hd", "p.2", "B", "2025년 수요 200만~210만 장 vs 유효 캐파 60만~70만 장(Omdia·Yole)")
m("preform", U, "광섬유 소재", "프리폼·광섬유", "프리폼·광섬유", "", "USD bn", {}, None, None, "CRU", "em_pf", "-", "-",
  "금액 미공개. 글로벌 프리폼 생산능력 약 2.5만톤(CRU 2025~26)")
m("gan", U, "RF 소자(무선)", "RF 반도체·부품", "GaN RF 소자", "통신·방산 GaN RF", "USD bn",
  {2030: 2.1}, None, 2030, "Yole Group", "yole_gan", "제품 페이지", "C", "국방용 GaN 2025년 5.92억 → 2031년 10억달러")
# Midstream
m("pkg", MS, "광 서브어셈블리(OSA)", "광소자 패키징", "포토닉스 패키징(Yole)", "광소자 조립·패키징(트랜시버·CPO 등)", "USD bn",
  {2031: 14.4}, 0.215, 2031, "Yole Group(2026.3)", "yole_pkg", "본문", "B",
  "CAGR 21.5%(2025~31). 2031년 트랜시버 80억·CPO 약 50억달러(yole_pkg2). 광트랜시버 시장과 일부 중복")
m("tx_yole", MS, "ODL(광트랜시버)", "광트랜시버 전체", "광트랜시버 전체(Yole)", "데이터컴+텔레콤", "USD bn",
  {2025: 23.0, 2031: 112.0}, None, 2031, "Yole Group(2026.7)", "yole_tx", "본문", "B", "AI가 2030년대 초 매출의 90% 이상")
m("tx_lc", MS, "ODL(광트랜시버)", "광트랜시버 전체", "광트랜시버 전체(LightCounting)", "광모듈+AOC", "USD bn",
  {2025: 23.8}, 0.22, 2030, "LightCounting(2026.3)", "lc_mar", "본문", "B",
  "2025년 YoY +55%. 2025~30 CAGR 22%(aj p.5 인용). 2025.12 추정치 230억(lc_dec)")
m("eth", MS, "ODL(광트랜시버)", "광트랜시버 전체", " └ 이더넷 광트랜시버(LightCounting)", "SFP~OSFP 이더넷 모듈", "USD bn",
  {2025: 18.0}, None, 2031, "LightCounting(2026.3·2026.10)", "lc_mar", "본문", "B",
  "2025년 약 180억달러(+70%). 증가율 2026 +120%, 2027 +76%, 2031 +20%(lc_eth). 2028~30 연도값 미공개",
  special={2026: "=I{eth}*(1+120%)", 2027: "=J{eth}*(1+76%)"})
m("ai", MS, "ODL(광트랜시버)", "광트랜시버 전체", " └ AI 클러스터용(이더넷 100G+·CPO)", "AI 스케일아웃·스케일업", "USD bn",
  {2025: 16.5, 2026: 26.0}, None, 2026, "LightCounting(2026.1)", "lc_ai", "본문", "A", "2027~31년은 성장 둔화로만 제시")
m("aoc", MS, "ODL(광트랜시버)", "광트랜시버 전체", " └ AOC", "", "USD bn",
  {2025: 1.1}, None, 2025, "LightCounting(2025.12)", "lc_dec", "본문", "A", "2024년의 2배 이상")
m("dcom", MS, "ODL(광트랜시버)", "광트랜시버 전체", "데이터컴 광부품(Cignal AI)", "데이터컴 광부품 매출", "USD bn",
  {2025: 18.0, 2029: 30.0}, 0.21, 2029, "Cignal AI", "cig", "본문", "A", "2025년 코히어런트 모듈 약 60억달러 별도")
m("dcoi", MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "데이터센터 광인터커넥트(LightCounting)", "플러그형+CPO", "USD bn",
  {2030: 30.0}, "=(30/10)^(1/6)-1", 2030, "LightCounting(Coherent 발표)", "coh_id", "본문", "B",
  "2024년 약 100억달러 → 2030년 300억(플러그형 250억 + CPO 50억)")
m("dcoi_dx", MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "데이터센터 광인터커넥트(灼识咨询)", "광의 정의(CPO·광 I/O 포함 추정)", "USD bn",
  {2030: 144.4}, 0.481, 2030, "LightCounting·灼识咨询(CIC)", "dx", "p.7", "B", "2024년 137억달러, CAGR 48.1%")
m("u800", MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "800G 모듈 출하량", "", "백만 개",
  {2025: 19.0, 2026: 35.0}, None, 2026, "LightCounting", "aj", "p.5", "B", "2025년 1,800만~1,990만 개(중간값), 2026년 3,500만 개 이상(dg p.2). 2028년 수요 정점")
m("u16", MS, "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "1.6T 모듈 출하량", "", "백만 개",
  {2025: 3.0, 2026: 10.0}, None, 2026, "LightCounting / Cignal AI", "aj", "p.5", "B", "2025년 250만~350만 개(중간값), 2026년 1,000만 개 돌파(cig_1q)")
m("coh", MS, "ODL(광트랜시버)", "코히어런트 트랜시버", "코히어런트 모듈(Cignal AI)", "플러그형+임베디드", "USD bn",
  {2025: 6.0, 2028: 8.0}, None, 2028, "Cignal AI", "cig", "본문", "B",
  "2028년 80억달러는 cig_coh. Omdia 코히어런트 포트 CAGR 21%(2024~29, omdia_ieee p.21)")
m("cpo", MS, "ODL(광트랜시버)", "차세대 인터커넥트", "CPO(LightCounting)", "", "USD bn",
  {2030: 5.0}, None, 2030, "LightCounting(Coherent 발표)", "coh_id", "본문", "B", "Yole CPO 패키징 2031년 약 50억달러(yole_pkg2)")
m("access", MS, "FTTH(광가입자망·PON)", "OLT용 트랜시버", "액세스 광모듈(FTTx+무선 프론트홀)", "PON+프론트홀/백홀", "USD bn",
  {2029: 2.9}, "=(2.9/1.6)^(1/6)-1", 2029, "LightCounting", "lc_access", "본문", "B",
  "2024년 사이클 저점. 2023년 약 16억달러(PON 10억+무선 6억, gx p.9) 기준 성장률")
m("fttx", MS, "FTTH(광가입자망·PON)", "OLT용 트랜시버", "FTTx(PON) 광모듈", "", "USD bn",
  {2025: 0.631}, None, 2025, "华鑫证券 전망(2024)", "hx", "p.47", "B", "2025년 출하 9,208만 개")
m("catv", MS, "RF(아날로그 광·RF-optics)", "CATV·HFC 광전송", "CATV 아날로그 광송수신기", "", "USD bn", {}, None, None, "-", "-", "-", "-",
  "공개 자료 미확인. 하위 장비는 Cable DAA 장비 행 참고")
m("dccable", MS, "광케이블", "광케이블", "AI 데이터센터용 광케이블 수요(CRU)", "물량 기준", "CAGR",
  {}, 0.28, None, "CRU", "stl", "p.9", "B", "2025~30년 물량 CAGR 28%. 금액 미공개")
m("corning", MS, "광케이블", "광케이블", "Corning 데이터센터(Enterprise) 광 매출", "1개사 실적(시장 하한 참고)", "USD bn",
  {2025: 3.0}, None, 2025, "Corning", "corning", "-", "C", "2025년 +61%, 약 2/3가 하이퍼스케일러. Meta와 최대 60억달러 다년 공급계약")
m("telcable", MS, "광케이블", "광케이블", "통신망용 광케이블", "", "USD bn", {}, None, None, "-", "-", "-", "-",
  "공신력 있는 금액 자료 미확인(범용 시장조사 출처 제외)")
# Downstream
m("capex", D, "최종 수요처", "데이터센터 사업자", "데이터센터 Capex(Dell'Oro 2026.2)", "전 세계 데이터센터 투자", "USD bn",
  {2025: 593, 2026: 1000, 2030: 1700}, None, 2030, "Dell'Oro Group", "do_capex", "본문", "A", "2025년 593은 mrvl slide 13(Dell'Oro 인용)")
m("capex2", D, "최종 수요처", "데이터센터 사업자", "데이터센터 Capex(Dell'Oro 2026.7 상향)", "", "USD bn",
  {2030: 3000}, None, 2030, "Dell'Oro Group", "do_capex2", "본문", "A", "2030년 3조달러 초과. 2026.2 전망 대비 약 2배")
m("omdia_cx", D, "최종 수요처", "데이터센터 사업자", "클라우드 사업자 Capex(Omdia)", "클라우드 SP", "USD bn",
  {2025: 350, 2030: 545}, None, 2030, "Omdia", "omdia_ieee", "p.3", "A", "2024년 약 2,000억달러")
m("hyper", D, "최종 수요처", "데이터센터 사업자", "미국 Top4 하이퍼스케일러 Capex", "Amazon·Google·Meta·Microsoft", "USD bn",
  {2025: 327, 2026: 600}, None, 2026, "기업 공시 / Dell'Oro", "mrvl", "slide 10", "A",
  "CY23 153 → CY24 248 → CY25 327. 2026년 약 6,000억달러(do_capex)")
m("mck", D, "최종 수요처", "데이터센터 사업자", "데이터센터 누적 Capex(~2030, McKinsey)", "2030년까지 누적", "USD bn(누적)",
  {2030: 6700}, None, 2030, "McKinsey & Company", "mck", "-", "B", "AI용 5.2조 + 일반 IT 1.5조달러. 2030 칸은 누적값")
m("optshare", D, "최종 수요처", "데이터센터 사업자", "광통신 지출 / Top5 클라우드 Capex", "Top5 클라우드", "%",
  {2025: 0.027, 2026: 0.031, 2031: 0.041}, None, 2031, "LightCounting(2026.1)", "lc_ai", "본문", "A", "스케일업 광연결 확대로 비중 상승", pct=True)
m("aisw", D, "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 백엔드 스위치", "AI 백엔드 네트워크용 스위치", "USD bn",
  {2030: 100}, None, 2030, "Dell'Oro Group", "do_aisw", "본문", "A", "2026.7: 2026~30 누적 1조달러 근접(do_aisw2)")
m("ot", D, "네트워크 장비(시스템)", "광전송 장비", "광전송 장비 전체", "", "USD bn",
  {2025: 16.0}, 0.05, 2026, "Dell'Oro Group", "do_ot_sdx", "본문", "A",
  "2026년 +16%(do_ot26). 2027년 이후는 2025.7 발표 5년 연평균 5%(do_ot25)로 연장(자체)",
  special={2026: "=I{ot}*(1+16%)"})
m("ipo", D, "네트워크 장비(시스템)", "광전송 장비", " └ IPoDWDM", "ZR/ZR+ 포함", "USD bn",
  {2030: 7.0}, 0.27, 2030, "Dell'Oro Group", "do_ipo", "본문", "A", "2030년 70억달러 초과, CAGR 27%")
m("dwdm", D, "네트워크 장비(시스템)", "광전송 장비", " └ 분리형 WDM", "IPoDWDM·트랜스폰더·OLS", "USD bn",
  {2030: 13.0}, 0.17, 2030, "Dell'Oro Group", "do_ipo", "본문", "A", "2030년 약 130억달러, CAGR 17%")
m("dci", D, "네트워크 장비(시스템)", "광전송 장비", "Purpose-built DCI(Omdia)", "DCI 전용 장비", "USD bn",
  {2030: 5.7}, None, 2030, "Omdia", "omdia_dci", "본문", "A", "2030년 57억달러 초과")
m("bb", D, "네트워크 장비(시스템)", "유선 액세스 장비", "브로드밴드 액세스 장비 전체", "", "USD bn",
  {2028: 18.8}, None, 2028, "Dell'Oro Group", "do_bb", "본문", "A", "2028년 정점, 2025~30 연평균 +0.3%")
m("pon", D, "네트워크 장비(시스템)", "유선 액세스 장비", "PON 장비", "", "USD bn",
  {2029: 12.6}, "=(12.6/10.7)^(1/5)-1", 2029, "Dell'Oro Group", "do_bb25", "-", "B", "2024년 107억달러. 이후 발표 CAGR 1.9%(2025~30, do_bb)")
m("dcpon", D, "네트워크 장비(시스템)", "유선 액세스 장비", "데이터센터 PON 장비", "", "USD bn",
  {}, 0.52, 2030, "Dell'Oro Group", "do_dcpon", "본문", "A",
  "2026~30년 누적 30억달러 초과, CAGR 52%로 연도별 역산(자체). 2026년 +844%로 2025년 역산",
  special={2026: "=3*0.52/(1.52^5-1)", 2025: "=J{dcpon}/(1+844%)"})
m("ran", D, "네트워크 장비(시스템)", "무선 장비", "RAN", "기지국(서비스 제외)", "USD bn",
  {}, 0.01, 2030, "Dell'Oro Group", "do_ran25", "-", "B", "2025~29 누적 1,600억달러 ÷ 5로 2025년 환산(자체), 이후 CAGR 1%(do_ran)",
  special={2025: "=160/5"})
m("airan", D, "네트워크 장비(시스템)", "무선 장비", " └ AI-RAN", "", "USD bn", {}, None, None, "Dell'Oro Group", "do_airan", "-", "-", "향후 5년 누적 350억달러")
m("daa", D, "네트워크 장비(시스템)", "케이블 HFC 장비", "Cable DAA 장비", "vCCAP·RPD·RMD·R-OLT", "USD bn",
  {2030: 1.2}, None, 2030, "Dell'Oro Group", "do_bb", "본문", "A", "DOCSIS 4.0·초기 광 전환")
