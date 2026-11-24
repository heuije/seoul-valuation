# -*- coding: utf-8 -*-
"""통신용 광모듈 밸류체인 / 기업 매핑 / 시장규모(2025~2030) 엑셀 생성."""
import re, sys
from copy import copy
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.utils import get_column_letter as CL

OUT = sys.argv[1]

# ---------------------------------------------------------------- style
TEAL = PatternFill("solid", fgColor="006C64")
BAND = PatternFill("solid", fgColor="D9EDED")
SUB = PatternFill("solid", fgColor="DAEEF3")
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BLUE, BLACK, WHITE = "0000FF", "000000", "FFFFFF"
YEARS = [2025, 2026, 2027, 2028, 2029, 2030]

KR, EN = "맑은 고딕", "Arial"
HAN = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
LAT = re.compile(r"[A-Za-z0-9]")


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


def apply_font(cell, cached=None):
    v = cell.value
    if v is None:
        return
    f = copy(cell.font)
    if isinstance(v, str) and v.startswith("="):
        f.name = KR if (isinstance(cached, str) and HAN.search(cached)) else EN
        cell.font = f
        return
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


def put(ws, r, c, v, bold=False, color=BLACK, fill=None, h="left", wrap=False, fmt=None, italic=False,
        border=True, link=None, underline=None):
    cell = ws.cell(r, c, v)
    cell.font = Font(name=EN, size=10, bold=bold, color=color, italic=italic, underline=underline)
    if fill:
        cell.fill = fill
    if isinstance(v, str) and v == "n/a":
        h = "right"
    cell.alignment = Alignment(horizontal=h, vertical="center", wrap_text=wrap)
    if fmt:
        cell.number_format = fmt
    if border:
        cell.border = BOX
    if link:
        cell.hyperlink = link
    return cell


def header(ws, r, labels, c0=2):
    for i, lab in enumerate(labels):
        put(ws, r, c0 + i, lab, bold=True, color=WHITE, fill=TEAL, h="center", wrap=True)


# ---------------------------------------------------------------- sources
S = {
    "S1": ("爱建证券", "集成度逐步提升重构光模块价值链——光模块行业深度报告", "2026.08.28",
           "LightCounting·源杰科技·QYResearch·智研咨询·DataIntelo·LP Information 인용",
           "https://pdf.dfcfw.com/pdf/H3_AP202608281828621981_1.pdf", "PDF 원문 확인"),
    "S2": ("东兴证券", "通信光互联行业：CW激光器重构全球光芯片产业格局，IDM模式构建产业链壁垒", "2026.04.22",
           "LightCounting·灼识咨询(CIC) 인용", "https://pdf.dfcfw.com/pdf/H3_AP202604221821439407_1.pdf", "PDF 원문 확인"),
    "S3": ("大公国际", "“十五五”科技基建浪潮下的光模块行业研究", "2025.12", "LightCounting 인용",
           "https://pdf.dfcfw.com/pdf/H3_AP202512241807012890_1.pdf", "PDF 원문 확인"),
    "S4": ("汉鼎智库咨询", "磷化铟光芯片衬底材料产业链分析", "2026.10.30", "Yole·LightCounting·Omdia 인용",
           "https://pdf.dfcfw.com/pdf/H3_AP202610301831244217_1.pdf", "PDF 원문 확인"),
    "S5": ("国信证券", "光模块专题：AI驱动网络变革，光摩尔定律加速", "2024.03.14", "LightCounting·Coherent 인용",
           "https://pdf.dfcfw.com/pdf/H3_AP202403151626804725_1.pdf", "PDF 원문 확인"),
    "S6": ("华鑫证券", "高速互联需求驱动光通信行业发展，国产光芯片有望加速渗透", "2024.08.03", "FTTx 광모듈 전망",
           "https://pdf.dfcfw.com/pdf/H3_AP202408031639131462_1.pdf", "PDF 원문 확인"),
    "S7": ("대신증권", "AI 병목을 넘어서 ① Networking: Everything Goes Optical", "2026 (주가 기준일 2026.02.27)",
           "Industry Research·PS Market Research 등 인용",
           "https://stock.pstatic.net/stock-research/invest/15/20260602_invest_997669000.pdf", "PDF 원문 확인"),
    "S8": ("유안타증권", "스몰캡: 광 트랜시버가 주목받는 이유", "2026.04.03", "GII·Mordor Intelligence·IDTechEx 인용",
           "https://stock.pstatic.net/stock-research/industry/18/20260403_industry_572374000.pdf", "PDF 원문 확인"),
    "S9": ("Marvell (IR)", "Custom AI Investor Event 2025", "2025.06.17",
           "650 Group·Cignal AI·Dell'Oro·LightCounting·Marvell 추정",
           "https://www.marvell.com/content/dam/marvell/en/company/assets/marvell-custom-ai-investor-event-2025.pdf",
           "PDF 원문 확인"),
    "S10": ("optics.org (Yole Group)", "Optical transceiver market poised to exceed $110BN by 2031", "2026.07.01",
            "Yole「Optical Transceivers for Datacom & Telecom 2026」",
            "https://optics.org/news/optical-transceiver-market-poised-to-exceed-110bn-by-2031---report", "웹 원문 확인"),
    "S11": ("optics.org (Yole Group)", "Photonics packaging market to triple in value by 2031", "2026.04.08", "Yole",
            "https://optics.org/news/photonics-packaging-market-to-triple-in-value-by-2031", "웹 원문 확인"),
    "S12": ("Semiconductor Today (Yole Group)", "Silicon PIC market growing at 45% CAGR from $95m in 2023 to $863m in 2029",
            "2024.12.17", "Yole「Silicon Photonics 2024」",
            "https://semiconductor-today.com/news_items/2024/dec/yole-171224.shtml", "웹 원문 확인"),
    "S13": ("IEEE ComSoc Tech Blog (LightCounting)", "LightCounting: Silicon Photonics chip market to hit $3 billion in 2029",
            "2024.05.29", "LightCounting",
            "https://techblog.comsoc.org/2024/05/29/lightcounting-silicon-photonics-chip-market-to-hit-3-billion-in-2029/",
            "웹 원문 확인"),
    "S14": ("Lightwave (LightCounting)", "Ethernet optical transceiver set to grow 120% in 2026", "2026.10.08", "LightCounting",
            "https://www.lightwaveonline.com/home/news/55410716/ethernet-optical-transceiver-set-to-grow-120-in-2026",
            "웹 원문 확인"),
    "S15": ("Lightwave (LightCounting)", "New LightCounting report: access optics sales to increase in the coming years",
            "2024.12.02", "LightCounting",
            "https://www.lightwaveonline.com/business/article/55246891/new-lightcounting-report-access-optics-sales-to-increase-in-the-coming-years",
            "웹 원문 확인"),
    "S16": ("Cignal AI", "Optical Component Revenue Reaches Nearly $25B in 2025", "2026.01.07", "Cignal AI",
            "https://cignal.ai/2026/01/optical-component-revenue-reaches-nearly-25b-in-2025/", "웹 원문 확인"),
    "S17": ("Lightwave (Cignal AI)", "Cignal AI says hyperscaler investment is radically reshaping the optical components market",
            "2026.06.30", "Cignal AI 1Q26 Optical Components Report",
            "https://www.lightwaveonline.com/home/article/55387778/cignal-ai-says-hyperscaler-investment-is-radically-reshaping-the-optical-components-market",
            "웹 원문 확인"),
    "S18": ("Dell'Oro Group", "Cloud Providers to Drive Optical Transport Market to $19 Billion in 2029", "2025.07.22",
            "Dell'Oro", "https://www.delloro.com/newsroom/cloud-providers-to-drive-optical-transport-market-to-19-billion-in-2029/",
            "웹 원문 확인"),
    "S19": ("Dell'Oro Group", "IPoDWDM Market Forecast to Grow at 27 Percent CAGR", "2026.06.16", "Dell'Oro",
            "https://www.delloro.com/newsroom/ipodwdm-market-forecast-to-grow-at-27-percent-cagr/?article_lang=en",
            "웹 원문 확인"),
    "S20": ("Dell'Oro Group", "AI Back-End Switch Market Will Push Past $100 Billion by 2030", "2026.02.04", "Dell'Oro",
            "https://www.delloro.com/newsroom/ai-back-end-switch-market-will-push-past-100-billion-by-2030/", "웹 원문 확인"),
    "S21": ("Dell'Oro Group", "AI Back-end Switch Sales to Approach $1 Trillion over the Next Five Years", "2026.07.28",
            "Dell'Oro", "https://www.delloro.com/news/ai-back-end-switch-sales-to-approach-1-trillion-over-the-next-five-years/",
            "웹 원문 확인"),
    "S22": ("Dell'Oro Group", "AI Boom Drives Data Center Capex to $1.7 Trillion by 2030", "2026.02.11", "Dell'Oro",
            "https://www.delloro.com/newsroom/ai-boom-drives-data-center-capex-to-1-7-trillion-by-2030/", "웹 원문 확인"),
    "S23": ("TelecomTV (Dell'Oro Group)", "AI buildout maintains momentum as datacentre capex to surpass $3tn by 2030",
            "2026 (7~8월)", "Dell'Oro Data Center IT Capex 5-Year Forecast (2026.07)",
            "https://www.telecomtv.com/content/digital-platforms-services/ai-buildout-maintains-momentum-as-datacentre-capex-to-surpass-3tn-by-2030-delloro-group-56102/",
            "검색 요약 확인(원문 접속 차단)"),
    "S24": ("Dell'Oro Group", "Broadband Equipment Spending to Peak at $18.8 B in 2028", "2026.01.28", "Dell'Oro",
            "https://www.delloro.com/news/broadband-equipment-spending-to-peak-at-18-8-b-in-2028/", "웹 원문 확인"),
    "S25": ("Signal Integrity Journal (Dell'Oro Group)", "Broadband Equipment Spending to $20.1 B in 2028 on Accelerated Fiber Deployments",
            "2025.07", "Dell'Oro Broadband Access 5-Year Forecast (2025.07)",
            "https://www.signalintegrityjournal.com/articles/4020-broadband-equipment-spending-to-201-b-in-2028-on-accelerated-fiber-deployments",
            "검색 요약 확인(원문 접속 차단)"),
    "S26": ("Dell'Oro Group", "Global RAN Market Stabilization Following Multi-Year Industry Reset", "2026.07.21", "Dell'Oro",
            "https://www.delloro.com/news/global-ran-market-stabilization-following-multi-year-industry-reset/", "웹 원문 확인"),
    "S27": ("TelecomTV (Dell'Oro Group)", "$160bn in RAN Before 6G, According to Dell'Oro Group", "2025.07",
            "Dell'Oro Mobile RAN 5-Year Forecast (2025.07)",
            "https://www.telecomtv.com/content/5g/160bn-in-ran-before-6g-according-to-dell-oro-group-53499/",
            "검색 요약 확인(원문 접속 차단)"),
    "S28": ("Fierce Network (Dell'Oro Group)", "AI-RAN market to hit $35B by 2030 says Dell'Oro", "2026.06", "Dell'Oro",
            "https://www.fierce-network.com/wireless/ai-ran-market-hit-35b-2030-says-delloro", "검색 요약 확인(원문 접속 차단)"),
    "S29": ("McKinsey & Company", "The cost of compute: A $7 trillion race to scale data centers", "2025.04", "McKinsey",
            "https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-cost-of-compute-a-7-trillion-dollar-race-to-scale-data-centers",
            "검색 요약 확인(사이트 자동접속 차단)"),
    "S30": ("C114 (LightCounting)", "LightCounting 2025년 광모듈 시장 실적(2026.03 업데이트)", "2026.03.13", "LightCounting",
            "https://m.c114.com.cn/w5472-1306868.html", "검색 요약 확인(원문 접속 차단)"),
    "S31": ("Yole Group", "RF GaN Compound Semiconductor Market Monitor (제품 페이지)", "2025~2026", "Yole",
            "https://www.yolegroup.com/product/quarterly-monitor/rf-gan-compound-semiconductor-market-monitor/",
            "검색 요약 확인(사이트 자동접속 차단)"),
    "S32": ("LightCounting", "December 2023: AOCs, DACs, Linear Drive Pluggable and Co-Packaged Optics (뉴스레터)", "2023.12",
            "LightCounting",
            "https://lightcounting.com/newsletter/en/december-2023-aocs-dacs-linear-drive-pluggable-and-co-packaged-optics-209",
            "검색 요약 확인(원문 접속 차단)"),
    "S33": ("optics.org (Coherent Investor Day)", "Coherent execs outline growth strategy", "2025.05.29",
            "LightCounting(Coherent 발표 인용)", "https://optics.org/news/16/5/47", "웹 원문 확인"),
    "S34": ("C114 (Cignal AI)", "CIOE 2025 Cignal AI 발표: 코히어런트 모듈 시장 전망", "2025.09.16", "Cignal AI",
            "https://m.c114.com.cn/w42-1297031.html", "검색 요약 확인(원문 접속 차단)"),
    "S35": ("Futurum Group (Marvell Investor Day)", "Marvell Investor Day 2026 Targets $80B FY 2031 Revenue With Custom Silicon and Optics",
            "2026.10", "Marvell",
            "https://futurumgroup.com/insights/marvell-investor-day-2026-targets-80b-fy-2031-revenue-with-custom-silicon-and-optics/",
            "검색 요약 확인(원문 접속 차단)"),
}

# ---------------------------------------------------------------- value chain structure (tab1 + tab2)
# (stream, 사업, 제품, 품목, 설명, 적용처, 빛과전자 분류, [해외], [국내])
VC = [
    # ===== Upstream
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "DFB 레이저",
     "전류로 신호를 직접 실어 보내는(직접변조) 가장 보편적인 레이저 칩", "10G·25G FTTH, 5G 프론트홀, 중단거리", "FTTH·ODL",
     ["Mitsubishi Electric", "Sumitomo Electric", "Broadcom", "Lumentum", "源杰科技(Yuanjie)", "光迅科技(Accelink)", "敏芯半导体(Mindsemi)"],
     ["오이솔루션"]),
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "EML",
     "변조기를 내장한 레이저. 고속·장거리에서 신호 품질이 좋음", "레인당 100G·200G(800G·1.6T 모듈), 장거리", "ODL",
     ["Lumentum", "Broadcom", "Mitsubishi Electric", "Sumitomo Electric", "Coherent", "源杰科技(Yuanjie)", "光迅科技(Accelink)"],
     ["오이솔루션(100G EML 개발)"]),
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "CW 레이저(고출력)",
     "연속광만 내는 외부 광원. 신호 변조는 실리콘포토닉스 칩이 담당", "실리콘포토닉스 800G·1.6T, LPO·CPO 외부광원", "ODL",
     ["Sumitomo Electric", "源杰科技(Yuanjie)", "Broadcom", "Lumentum", "Coherent", "Mitsubishi Electric"], []),
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "VCSEL",
     "수직 발광 레이저. 저가·저전력, 멀티모드 단거리용", "100m 이내 SR4·SR8(400G·800G), AOC", "ODL",
     ["Coherent", "Broadcom", "Lumentum", "Trumpf"], []),
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "튜너블 레이저(ITLA)",
     "파장을 바꿀 수 있는 레이저", "DWDM·코히어런트(400ZR·800ZR), 튜너블 SFP+", "ODL",
     ["Lumentum", "Coherent", "Furukawa Electric"], []),
    ("Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "펌프 레이저(980nm)",
     "광증폭기(EDFA)를 구동하는 고출력 레이저", "DCI·장거리 광증폭, CATV", "RF",
     ["Lumentum", "Coherent", "Furukawa Electric", "3SP Technologies"], ["RF머트리얼즈(패키징)"]),
    ("Upstream", "광소자 칩(능동)", "수광 칩", "PIN PD",
     "빛을 전기로 바꾸는 기본형 포토다이오드", "중단거리 수신부(ROSA)", "FTTH·ODL",
     ["Lumentum", "Broadcom", "Coherent", "Sumitomo Electric", "Mitsubishi Electric", "芯思杰", "光森电子"], ["우리로"]),
    ("Upstream", "광소자 칩(능동)", "수광 칩", "APD",
     "수신 신호를 내부 증폭하는 고감도 포토다이오드", "장거리, PON OLT 수신부", "FTTH·ODL",
     ["Mitsubishi Electric", "Sumitomo Electric", "Broadcom", "三安集成", "敏芯半导体(Mindsemi)"], ["우리로"]),
    ("Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 PIC",
     "실리콘 웨이퍼에 변조기·도파로·수광부를 집적(광원은 외부 CW 레이저)", "800G·1.6T DR/FR, CPO 광엔진", "ODL",
     ["Broadcom", "Marvell", "Cisco(Acacia)", "Coherent", "InnoLight(中际旭创)", "TSMC(파운드리)", "GlobalFoundries(파운드리)",
      "Tower Semiconductor(파운드리)"], []),
    ("Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "InP PIC",
     "인화인듐 기반으로 레이저·변조기를 한 칩에 집적", "코히어런트 장거리·DCI", "ODL",
     ["Nokia(Infinera)", "Lumentum", "Coherent"], []),
    ("Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "TFLN 변조기",
     "박막 니오브산리튬 기반 초고속 변조기", "레인당 200G·400G 차세대 모듈, 코히어런트", "ODL",
     ["HyperLight", "Fujitsu Optical Components", "Sumitomo Osaka Cement", "光库科技(AFR)"], []),
    ("Upstream", "전기 칩(IC)", "DSP", "PAM4 DSP",
     "고속 전기신호를 4단계 신호로 변환·보정하는 핵심 칩", "400G·800G·1.6T 데이터센터 모듈", "ODL",
     ["Broadcom", "Marvell", "MaxLinear", "Credo"], []),
    ("Upstream", "전기 칩(IC)", "DSP", "코히어런트 DSP",
     "빛의 위상·편광까지 쓰는 장거리용 DSP", "400ZR·800ZR, 장거리 트랜스폰더", "ODL",
     ["Marvell", "Cisco(Acacia)", "Ciena", "Nokia(Infinera)", "NTT Innovative Devices"], []),
    ("Upstream", "전기 칩(IC)", "아날로그 IC", "TIA",
     "수광 소자가 만든 미세 전류를 전압 신호로 증폭", "수신부(ROSA)", "공통",
     ["Marvell", "Broadcom", "Semtech", "MACOM", "Analog Devices"], []),
    ("Upstream", "전기 칩(IC)", "아날로그 IC", "레이저·변조기 드라이버",
     "레이저·변조기를 구동하는 고속 증폭기", "송신부(TOSA), LPO", "공통",
     ["Semtech", "MACOM", "Marvell", "Broadcom", "Analog Devices"], []),
    ("Upstream", "전기 칩(IC)", "PON SoC", "PON 칩셋(OLT·ONU SoC)",
     "PON 장비와 ONU 스틱의 통신 처리 칩", "GPON·XGS-PON ONT/OLT", "FTTH",
     ["Broadcom", "Realtek", "中兴微电子(Sanechips)", "HiSilicon"], ["자람테크놀로지"]),
    ("Upstream", "광 수동부품", "광 신호제어", "광 아이솔레이터",
     "반사된 빛이 레이저로 되돌아오지 않게 막는 부품", "송신부·레이저 보호", "공통",
     ["Coherent", "스미토모(住友)"], []),
    ("Upstream", "광 수동부품", "광 신호제어", "WDM 필터·AWG",
     "여러 파장을 합치거나 나누는 부품", "CWDM·LWDM 모듈(FR4), DWDM, PON", "공통",
     ["仕佳光子(Shijia)", "博创科技(Broadex)", "Lumentum", "Corning(AFOP)", "腾景科技"], ["피피아이"]),
    ("Upstream", "광 수동부품", "광 신호제어", "PLC 스플리터",
     "광신호 하나를 여러 가입자에게 나눠 주는 분배기", "FTTH 광분배망", "FTTH",
     ["仕佳光子(Shijia)", "博创科技(Broadex)"], ["피피아이", "우리로"]),
    ("Upstream", "광 수동부품", "광 연결·결합", "렌즈·FAU·MT 페룰·MPO",
     "광섬유와 칩을 정렬·결합하고 여러 가닥을 한 번에 연결", "800G·1.6T 모듈, CPO 광섬유 연결", "ODL",
     ["天孚通信(TFC)", "太辰光(T&S)", "US Conec", "Fujikura", "Senko", "炬光科技(Focuslight)"], []),
    ("Upstream", "패키징·기판", "패키지·방열", "TO-CAN·세라믹·버터플라이 패키지",
     "레이저·수광 칩을 담는 금속·세라믹 하우징", "통신용 TO-CAN, 기밀 패키지(텔레콤·방산)", "공통",
     ["Kyocera", "Schott", "Niterra(NTK)"], ["RF머트리얼즈"]),
    ("Upstream", "패키징·기판", "패키지·방열", "TEC(열전소자)",
     "레이저 온도를 일정하게 유지하는 냉각 소자", "EML·DWDM·튜너블 모듈", "ODL",
     ["Ferrotec", "KELK", "Phononic", "富信科技"], []),
    ("Upstream", "패키징·기판", "패키지·방열", "광모듈 PCB",
     "칩을 직접 실장하는 고다층·mSAP 기판(COB 구조의 중심)", "800G·1.6T 모듈", "ODL",
     ["欣兴电子(Unimicron)", "生益电子(Shengyi)"], []),
    ("Upstream", "반도체 기판·에피", "화합물·SOI 웨이퍼", "InP 기판",
     "DFB·EML·CW 레이저가 만들어지는 기판(현재 공급 병목)", "레이저·수광 칩", "공통",
     ["Sumitomo Electric", "AXT(北京通美)", "JX Advanced Metals"], []),
    ("Upstream", "반도체 기판·에피", "화합물·SOI 웨이퍼", "GaAs 기판",
     "VCSEL을 만드는 기판", "VCSEL", "ODL",
     ["Freiberger", "Sumitomo Electric", "AXT(北京通美)"], []),
    ("Upstream", "반도체 기판·에피", "화합물·SOI 웨이퍼", "에피웨이퍼",
     "기판 위에 발광층을 성장시킨 웨이퍼", "레이저 칩 외주 생산", "공통",
     ["IQE", "LandMark(聯亞光電)", "VPEC(全新光電)"], []),
    ("Upstream", "반도체 기판·에피", "화합물·SOI 웨이퍼", "SOI 웨이퍼",
     "실리콘포토닉스 칩용 웨이퍼", "실리콘포토닉스 PIC", "ODL",
     ["Soitec", "Shin-Etsu"], []),
    ("Upstream", "광섬유·광케이블", "광섬유·케이블", "광섬유·광케이블(프리폼 포함)",
     "빛이 지나가는 유리 섬유와 이를 묶은 케이블", "백본, FTTH, 데이터센터 배선", "FTTH",
     ["Corning", "Prysmian", "Fujikura", "Sumitomo Electric", "Furukawa(OFS)", "YOFC(长飞)", "Hengtong(亨通)", "STL(Sterlite)"],
     ["대한광통신", "LS전선"]),
    ("Upstream", "제조·검사 장비", "공정·계측 장비", "MOCVD·능동정렬/본딩·광 계측",
     "에피 성장, 광축 능동정렬, 성능 측정 장비", "칩·모듈 생산, CPO 조립", "공통",
     ["Aixtron", "ficonTEC", "ASMPT", "Keysight", "Anritsu", "EXFO"], ["성호전자(ADS테크)", "이노인스트루먼트"]),
    ("Upstream", "RF 소자(무선)", "RF 반도체·부품", "GaN RF 트랜지스터·PA",
     "기지국·레이더용 고출력 RF 증폭 반도체", "5G·AI-RAN 기지국, 방산 레이더·위성", "-",
     ["MACOM", "Qorvo", "Sumitomo Electric(SEDI)", "NXP"], ["RFHIC", "웨이비스"]),
    ("Upstream", "RF 소자(무선)", "RF 반도체·부품", "RF 필터·안테나 부품",
     "기지국 주파수 필터와 안테나 부품", "5G RU·안테나", "-",
     ["Comba Telecom", "Amphenol"], ["케이엠더블유"]),
    ("Upstream", "RF 소자(무선)", "RF 반도체·부품", "RF 케이블·커넥터",
     "고주파 신호용 케이블·커넥터", "기지국·방산·위성", "-",
     ["Rosenberger", "Huber+Suhner", "Amphenol"], ["센서뷰"]),
    # ===== Midstream
    ("Midstream", "광 서브어셈블리(OSA)", "광소자 패키징", "TO-CAN(LD·PD)",
     "칩을 TO 패키지에 넣은 기본 광소자", "저·중속 트랜시버, BOSA", "FTTH·ODL",
     ["光迅科技(Accelink)", "Source Photonics", "Hisense Broadband", "华工正源(HG Genuine)"], ["빛과전자", "오이솔루션"]),
    ("Midstream", "광 서브어셈블리(OSA)", "광소자 패키징", "TOSA·ROSA",
     "송신부(TOSA)·수신부(ROSA) 광학 조립체", "트랜시버 핵심 부품(TO-CAN 모듈 원가 TOSA 35%·ROSA 23%)", "ODL",
     ["光迅科技(Accelink)", "Source Photonics", "Hisense Broadband", "O-Net(昂纳)", "华工正源(HG Genuine)"], ["오이솔루션", "빛과전자"]),
    ("Midstream", "광 서브어셈블리(OSA)", "광소자 패키징", "BOSA",
     "송·수신을 한 패키지에 담은 양방향 조립체(광섬유 1가닥 사용)", "FTTH ONU, 양방향(Bi-Di) SFP", "FTTH",
     ["Hisense Broadband", "光迅科技(Accelink)", "Source Photonics"], ["빛과전자"]),
    ("Midstream", "광 서브어셈블리(OSA)", "광소자 패키징", "광엔진(COB)",
     "칩을 PCB에 직접 실장한 고속 송수신 엔진", "800G·1.6T 모듈, CPO", "ODL",
     ["InnoLight(中际旭创)", "Eoptolink(新易盛)", "Coherent", "Fabrinet(위탁생산)", "天孚通信(TFC)"], []),
    ("Midstream", "ODL(광트랜시버)", "저속 트랜시버(~10G)", "SFP(1G)·SFP+(10G)·XFP",
     "가장 작은 표준 규격의 1~10G 광트랜시버", "기업망, LTE 프론트홀, FTTH 백홀", "ODL",
     ["Coherent", "光迅科技(Accelink)", "Hisense Broadband", "Source Photonics", "华工正源(HG Genuine)", "Eoptolink(新易盛)"],
     ["빛과전자", "오이솔루션", "옵티코어"]),
    ("Midstream", "ODL(광트랜시버)", "중속 트랜시버(25G~100G)", "SFP28(25G)·QSFP+(40G)·QSFP28(100G)",
     "4채널 묶음(QSFP) 등 25~100G 모듈", "5G 프론트홀(25G), 데이터센터 100G", "ODL",
     ["InnoLight(中际旭创)", "Eoptolink(新易盛)", "光迅科技(Accelink)", "Hisense Broadband", "Coherent", "AAOI"],
     ["오이솔루션", "옵티코어", "빛과전자"]),
    ("Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "400G·800G(QSFP-DD·OSFP)",
     "AI 데이터센터 주력 제품(800G = 100G×8채널)", "GPU 클러스터 스케일아웃, 스위치 포트", "ODL",
     ["InnoLight(中际旭创)", "Eoptolink(新易盛)", "Coherent", "Lumentum", "Cisco", "AAOI", "光迅科技(Accelink)",
      "华工正源(HG Genuine)"], ["오이솔루션", "옵티코어"]),
    ("Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "1.6T·3.2T(OSFP 등)",
     "차세대 모듈(1.6T = 200G×8채널), 3.2T는 개발 단계", "차세대 AI 클러스터(2026년~)", "ODL",
     ["InnoLight(中际旭创)", "Eoptolink(新易盛)", "Coherent", "Lumentum"], ["오이솔루션(2H26 투입 계획)"]),
    ("Midstream", "ODL(광트랜시버)", "코히어런트 트랜시버", "400ZR/ZR+·800ZR/ZR+",
     "라우터·스위치에 바로 꽂는 장거리용 코히어런트 모듈", "데이터센터 간 연결(DCI), 메트로", "ODL",
     ["Cisco(Acacia)", "Marvell", "Ciena", "Nokia(Infinera)", "Coherent", "Lumentum"], []),
    ("Midstream", "ODL(광트랜시버)", "무선 프론트홀·백홀 트랜시버", "10G·25G(그레이·CWDM·DWDM·튜너블)",
     "기지국 무선부(RU)와 DU를 잇는 광모듈", "LTE·5G 프론트홀, 백홀", "ODL(무선)",
     ["光迅科技(Accelink)", "Hisense Broadband", "华工正源(HG Genuine)", "Eoptolink(新易盛)", "Source Photonics"],
     ["오이솔루션", "옵티코어", "빛과전자"]),
    ("Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "LPO·LRO(선형 구동)",
     "DSP를 빼거나 줄여 전력을 낮춘 플러그형 모듈", "AI 클러스터 단거리", "ODL",
     ["Eoptolink(新易盛)", "InnoLight(中际旭创)", "Coherent"], []),
    ("Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "AOC(광케이블 일체형)",
     "양 끝에 트랜시버가 붙어 있는 광케이블", "랙 내부·인접 랙 연결", "ODL",
     ["Coherent", "NVIDIA(Mellanox)", "Luxshare", "Amphenol"], []),
    ("Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "CPO(광 공동패키징)",
     "스위치·GPU 칩 바로 옆에 광엔진을 함께 패키징", "스케일아웃 스위치(2026년~), 스케일업(2028년~)", "ODL",
     ["Broadcom", "NVIDIA", "Marvell(Celestial AI)", "Cisco", "Ayar Labs", "Ranovus"], ["오이솔루션(개발 로드맵)"]),
    ("Midstream", "FTTH(광가입자망·PON)", "OLT용 트랜시버", "GPON·XGS-PON·50G-PON OLT",
     "통신사 국사 장비(OLT)에 꽂는 PON 광모듈", "광가입자망 국사", "FTTH",
     ["Hisense Broadband", "Source Photonics", "光迅科技(Accelink)", "华工正源(HG Genuine)", "Eoptolink(新易盛)"], ["빛과전자"]),
    ("Midstream", "FTTH(광가입자망·PON)", "ONU·ONT용 광부품", "ONU BOSA·SFP ONU 스틱",
     "가입자 댁내 단말(ONT)에 들어가는 광부품", "가정·기업 광단말", "FTTH",
     ["Hisense Broadband", "光迅科技(Accelink)", "Source Photonics"], ["빛과전자"]),
    ("Midstream", "RF(아날로그 광·RF-optics)", "CATV·HFC 광전송", "아날로그 광송신기·광수신기(노드)",
     "케이블TV 신호(RF)를 빛에 실어 보내고 받는 장치", "케이블TV·HFC 망", "RF",
     ["AAOI", "Teleste", "Vecima"], ["빛과전자"]),
    ("Midstream", "RF(아날로그 광·RF-optics)", "광증폭·RoF", "EDFA 광증폭기",
     "광신호를 전기로 바꾸지 않고 바로 증폭", "DCI·장거리, CATV", "RF",
     ["Lumentum", "Coherent", "光迅科技(Accelink)", "O-Net(昂纳)"], ["RF머트리얼즈"]),
    ("Midstream", "RF(아날로그 광·RF-optics)", "광증폭·RoF", "RoF·DAS 광모듈",
     "무선 신호를 광섬유로 전달(중계기·DAS)", "건물 내 이동통신 중계, 지하철", "RF",
     ["Amphenol(구 CommScope DAS)", "Corning", "JMA Wireless"], ["쏠리드", "에프알텍"]),
    ("Midstream", "무선 RF 모듈", "기지국 RF 모듈", "RU·안테나·PA 모듈",
     "기지국 무선부(라디오·안테나·증폭기)", "5G·AI-RAN 기지국", "-",
     ["Ericsson", "Nokia", "Comba Telecom"], ["케이엠더블유", "RFHIC"]),
    # ===== Downstream
    ("Downstream", "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 백엔드·프론트엔드 스위치",
     "GPU·서버를 잇는 이더넷·인피니밴드 스위치(광모듈 최대 수요처)", "AI 클러스터 스케일업·스케일아웃", "ODL",
     ["NVIDIA", "Arista", "Cisco", "Celestica", "Huawei", "HPE(Juniper)", "Accton"], ["유비쿼스(통신·기업망)", "다산네트웍스(기업망)"]),
    ("Downstream", "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 가속기 시스템(GPU 랙)",
     "GPU 랙 단위 시스템. 광모듈을 직접 조달하기도 함", "AI 학습·추론", "ODL",
     ["NVIDIA", "Google(TPU)", "AMD"], []),
    ("Downstream", "네트워크 장비(시스템)", "광전송 장비", "WDM·OTN·ROADM·IPoDWDM",
     "여러 파장을 묶어 장거리로 보내는 전송 장비", "백본·메트로·DCI", "ODL",
     ["Ciena", "Huawei", "Nokia(Infinera)", "Cisco", "ZTE", "1Finity(Fujitsu)"], ["코위버", "우리넷", "텔레필드"]),
    ("Downstream", "네트워크 장비(시스템)", "유선 액세스 장비", "PON OLT·ONT·가입자 CPE",
     "광가입자망 국사 장비와 댁내 단말", "FTTH(미국 BEAD 등 정부 보조사업 포함)", "FTTH",
     ["Huawei", "ZTE", "Nokia", "Calix", "Adtran", "FiberHome"], ["다산네트웍스", "유비쿼스", "에치에프알", "가온그룹"]),
    ("Downstream", "네트워크 장비(시스템)", "무선 장비", "RAN·AI-RAN·프론트홀·중계 장비",
     "이동통신 기지국과 프론트홀·중계·계측 장비", "5G·5G-A, 미국 주파수 경매 후 투자", "ODL(무선)",
     ["Ericsson", "Nokia", "Huawei", "ZTE"], ["삼성전자", "에치에프알", "쏠리드", "케이엠더블유", "이노와이어리스"]),
    ("Downstream", "네트워크 장비(시스템)", "케이블 HFC 장비", "DAA·Remote PHY·광노드",
     "케이블망의 분산형 접속 장비", "케이블TV·초고속인터넷(DOCSIS 4.0)", "RF",
     ["Harmonic", "Vecima", "Teleste"], []),
    ("Downstream", "네트워크 장비(시스템)", "위성·방산 통신", "위성통신 단말·방산 통신장비",
     "군 위성통신·레이더·전술통신 장비", "국방·우주", "-",
     ["L3Harris", "Viasat", "Thales"], ["RF시스템즈", "이노와이어리스"]),
    ("Downstream", "최종 수요처", "데이터센터 사업자", "하이퍼스케일러·네오클라우드",
     "AI 데이터센터를 짓고 광모듈을 대량 구매하는 사업자", "AI·클라우드", "ODL",
     ["Microsoft", "Amazon(AWS)", "Google", "Meta", "Oracle", "CoreWeave"], ["네이버", "카카오"]),
    ("Downstream", "최종 수요처", "통신 사업자", "통신사·케이블 MSO",
     "유무선 통신망에 투자하는 사업자", "FTTH·5G·백본", "FTTH·ODL·RF",
     ["AT&T", "Verizon", "T-Mobile", "China Mobile", "NTT", "Comcast", "Charter"], ["SK텔레콤", "KT", "LG유플러스"]),
]

STREAM_TITLE = {
    "Upstream": "Upstream — 소재·칩·부품 (광모듈 안에 들어가는 것)",
    "Midstream": "Midstream — 광부품·광모듈 (빛과전자 FTTH·ODL·RF가 여기에 해당)",
    "Downstream": "Downstream — 장비·최종 수요처 (광모듈을 사서 쓰는 쪽)",
}

# ---------------------------------------------------------------- market rows (tab3)
# key, stream, 사업, 제품, 품목·지표, 정의, 단위, src{year:val}, g(float|'=formula'|None), hz(원문 기간 끝), special{year:formula}, 원출처, cite, 위치, how-override, grade, note
M = []


def m(key, stream, biz, prod, item, scope, unit, src, g, hz, orig, cite, loc, grade, note, special=None, how=None):
    M.append(dict(key=key, stream=stream, biz=biz, prod=prod, item=item, scope=scope, unit=unit, src=src, g=g, hz=hz,
                  special=special or {}, orig=orig, cite=cite, loc=loc, grade=grade, note=note, how=how))


LASER = dict(orig="源杰科技(Yuanjie) 자료", cite="S1", loc="p.14 도표26", grade="B")
m("laser", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "레이저 칩 전체", "광통신용 레이저 칩, 전 세계", "USD bn",
  {2025: 3.90, 2026: 6.00, 2027: 8.70, 2028: 11.90, 2029: 17.60, 2030: 22.90}, None, 2030, note="2024년 2.54. 东兴证券(S2)도 2024 26억→2030 229억달러(LightCounting·灼识)로 동일 수준", **LASER)
m("cw", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "CW 레이저 칩", "실리콘포토닉스·CPO용 외부 광원", "USD bn",
  {2025: 0.20, 2026: 0.90, 2027: 1.90, 2028: 3.30, 2029: 6.40, 2030: 10.10}, None, 2030,
  note="2025년 400G+ 실리콘포토닉스용 CW 점유율: 住友 31.7%, 源杰 23.6%(S2 p.32)", **LASER)
m("cw1", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ CW 50mW 이하", "출력 50mW 이하", "USD bn",
  {2025: 0.10, 2026: 0.20, 2027: 0.20, 2028: 0.30, 2029: 0.30, 2030: 0.30}, None, 2030, note="", **LASER)
m("cw2", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ CW 70·100mW", "주력 출력대", "USD bn",
  {2025: 0.10, 2026: 0.70, 2027: 1.50, 2028: 2.10, 2029: 2.80, 2030: 3.20}, None, 2030, note="", **LASER)
m("cw3", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ CW 100mW 초과", "CPO·NPO용 고출력", "USD bn",
  {2027: 0.20, 2028: 0.90, 2029: 3.30, 2030: 6.60}, None, 2030, note="2025~26년은 원문 표에 값 없음", **LASER)
m("eml", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "EML 칩", "EML 레이저 칩 전체", "USD bn",
  {2025: 1.90, 2026: 3.10, 2027: 4.80, 2028: 6.60, 2029: 9.10, 2030: 10.70}, None, 2030,
  note="2025년 고속 레이저칩 점유율 Lumentum 33%(S2 p.32)", **LASER)
m("eml1", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ EML 50G 이하", "", "USD bn",
  {2025: 0.50, 2026: 0.50, 2027: 0.50, 2028: 0.60, 2029: 0.60, 2030: 0.70}, None, 2030, note="", **LASER)
m("eml2", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ EML 100G", "", "USD bn",
  {2025: 1.20, 2026: 1.50, 2027: 2.00, 2028: 2.30, 2029: 2.60, 2030: 2.20}, None, 2030, note="", **LASER)
m("eml3", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", " └ EML 200G 이상", "1.6T용", "USD bn",
  {2025: 0.20, 2026: 1.20, 2027: 2.30, 2028: 3.60, 2029: 5.90, 2030: 7.80}, None, 2030, note="", **LASER)
m("oth", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "기타 레이저(DFB·VCSEL·FP 등)", "EML·CW 외 레이저 칩", "USD bn",
  {2025: 1.80, 2026: 1.90, 2027: 2.00, 2028: 2.00, 2029: 2.10, 2030: 2.10}, None, 2030, note="DFB·VCSEL 개별 수치는 원문 미분리", **LASER)
m("dclaser", "Upstream", "광소자 칩(능동)", "레이저(발광) 칩", "데이터센터용 레이저 칩(참고)", "데이터센터 수요분", "USD bn",
  {2030: 21.1}, 0.534, 2030, "LightCounting·灼识咨询(CIC)", "S2", "p.8", "B",
  "2024년 16억달러, 원문 CAGR 53.4%(2024~30)")
m("pd", "Upstream", "광소자 칩(능동)", "수광 칩", "PIN·APD 수광 칩", "", "USD bn", {}, None, None, "-", "S1", "p.18", "-",
  "연도별 규모 공개 자료 미확인. 주요 업체 Lumentum·Broadcom·Coherent·住友·三菱(S1)")
m("siph", "Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 칩(LightCounting)", "SiPh 칩 매출(TFLN 제외)", "USD bn",
  {2029: 3.0}, "=(3.0/0.8)^(1/6)-1", 2029, "LightCounting", "S13", "본문", "B",
  "2023년 8억달러 → 2029년 30억달러 초과. TFLN 포함 시 2029년 38억달러")
m("siphy", "Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "실리콘포토닉스 PIC 다이(Yole)", "PIC 다이 기준(좁은 정의)", "USD bn",
  {2029: 0.863}, 0.45, 2029, "Yole Group", "S12", "본문", "B",
  "2023년 9,500만달러, CAGR 45%. Yole 2025년판은 2024 4.04억→2030 21억달러(검색 요약)")
m("tfln", "Upstream", "광소자 칩(능동)", "광집적회로(PIC)·변조기", "TFLN 변조기 PIC", "", "USD bn",
  {2029: 0.75}, None, 2029, "LightCounting", "S13", "본문", "B", "현재 거의 0에서 2029년 7.5억달러")
m("ic", "Upstream", "전기 칩(IC)", "DSP", "광 인터커넥트 IC(DSP·TIA·드라이버·AEC 등)", "Marvell 정의 데이터센터 Interconnect TAM",
  "USD bn", {2028: 19.0}, 0.35, 2028, "650 Group·Cignal AI·Dell'Oro·LightCounting·Marvell", "S9", "slide 16", "A",
  "CY23 43억달러, CAGR 35%. Marvell 2026.10 인베스터데이: CY30 인터커넥트 TAM 약 650억달러(S35, 검색 요약)")
m("dsp", "Upstream", "전기 칩(IC)", "DSP", "PAM4 DSP", "", "USD bn", {}, None, None, "DataIntelo", "S1", "p.21", "C",
  "2034년 148억달러(전 응용 포함)만 공개. Broadcom·Marvell 합산 점유율 90%+")
m("drv", "Upstream", "전기 칩(IC)", "아날로그 IC", "광변조기 드라이버 IC", "", "USD bn",
  {2025: 1.8}, 0.098, 2034, "DataIntelo", "S1", "p.21", "C", "2034년 42억달러, CAGR 9.8%(2026~34)")
m("tia", "Upstream", "전기 칩(IC)", "아날로그 IC", "TIA", "", "USD bn",
  {2030: 0.630}, 0.030, 2030, "DiReports", "S1", "p.22", "C", "2024년 5.27억달러, CAGR 3.0%")
m("ponsoc", "Upstream", "전기 칩(IC)", "PON SoC", "PON 칩셋", "", "USD bn", {}, None, None, "-", "-", "-", "-",
  "공개 자료 미확인")
m("awg", "Upstream", "광 수동부품", "광 신호제어", "AWG(파장분할 칩)", "", "USD bn",
  {2026: 1.55}, 0.110, 2035, "智研咨询", "S1", "p.19", "C", "2035년 39.6억달러, CAGR 약 11%(2026~35)")
m("fau", "Upstream", "광 수동부품", "광 연결·결합", "FAU(광섬유 어레이)", "", "USD bn",
  {2029: 0.13}, "=(0.13/0.10)^(1/5)-1", 2029, "QYResearch", "S1", "p.19", "C",
  "2024년 약 1억달러. 2026년 데이터센터용 FAU 수요 1.6억 개(光纤在线)")
m("iso", "Upstream", "광 수동부품", "광 신호제어", "광 아이솔레이터", "", "USD bn", {}, None, None, "本数咨询", "S1", "p.19", "-",
  "규모 미공개. 점유율 Coherent 60%, 일본 스미토모 25%")
m("pkg", "Upstream", "패키징·기판", "패키지·방열", "포토닉스 패키징(Yole 정의)", "광소자 연결·패키징 시장", "USD bn",
  {2025: 4.5}, "=(14.4/4.5)^(1/6)-1", 2031, "Yole Group", "S11", "본문", "B",
  "2031년 144억달러(트랜시버 80억, CPO 약 50억). 원문 '현재' 45억달러를 2025년으로 반영")
m("pcb", "Upstream", "패키징·기판", "패키지·방열", "800G 광모듈 PCB", "", "USD bn",
  {2025: 1.2}, 0.08, 2032, "LP Information", "S1", "p.24", "C", "2032년 20억달러 초과, CAGR 8%(2026~32)")
m("inp", "Upstream", "반도체 기판·에피", "화합물·SOI 웨이퍼", "InP 기판", "2인치 환산 128만 장", "USD bn",
  {2026: 0.2}, None, 2026, "Yole Group", "S4", "p.2", "B",
  "2025년 수요 200만~210만 장 vs 유효 캐파 60만~70만 장(Omdia·Yole)")
m("fiber", "Upstream", "광섬유·광케이블", "광섬유·케이블", "미국 광섬유 케이블", "미국 한정", "USD bn",
  {2025: 3.1, 2030: 4.6}, None, 2030, "PS Market Research", "S7", "p.53", "C",
  "글로벌 수치 미확보. CRU: AI향 광케이블 수요 2029년까지 연 26% 성장(검색 요약)")
m("gan", "Upstream", "RF 소자(무선)", "RF 반도체·부품", "GaN RF 소자", "통신·방산 GaN RF", "USD bn",
  {2030: 2.1}, None, 2030, "Yole Group", "S31", "제품 페이지", "C",
  "국방용 GaN: 2025 5.92억 → 2031 10억달러(검색 요약)")

m("tx_yole", "Midstream", "ODL(광트랜시버)", "광트랜시버 전체", "광트랜시버 전체(Yole)", "데이터컴+텔레콤", "USD bn",
  {2025: 23.0}, 0.30, 2031, "Yole Group", "S10", "본문", "B",
  "2031년 1,120억달러. Yole 보도자료 원문은 2025 234억→2031 1,123억. AI가 2030년대 초 매출 90% 이상")
m("tx_lc", "Midstream", "ODL(광트랜시버)", "광트랜시버 전체", "광트랜시버 전체(LightCounting)", "전 광모듈", "USD bn",
  {2025: 23.8}, 0.22, 2030, "LightCounting", "S30", "-", "B",
  "2025년 값은 S30(검색 요약), CAGR 22%(2025~30)는 S1 p.5. 2026.10 업데이트(S14)에서 이더넷 2026 +120%로 상향")
m("dcom", "Midstream", "ODL(광트랜시버)", "광트랜시버 전체", "데이터컴 광부품(Cignal AI)", "데이터컴 광부품 매출", "USD bn",
  {2025: 18.0, 2029: 30.0}, 0.21, 2029, "Cignal AI", "S16", "본문", "A",
  "2025년 코히어런트 모듈 약 60억달러 별도, 광부품 전체 약 250억달러. 2029년 '약 290억' 표현도 병기")
m("eth", "Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "이더넷 광트랜시버(LightCounting 최신)", "이더넷 트랜시버", "USD bn",
  {2025: 18.0}, None, 2031, "LightCounting", "S14", "본문", "B",
  "2025년 값 약 180억달러(S30). 성장률 2026 +120%, 2027 +76%, 2031 +20%로 둔화(원문). 2028~30 연도값 미공개",
  special={2026: "={I}*(1+120%)", 2027: "={J}*(1+76%)"})
m("u800", "Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "800G 모듈 출하량", "", "백만 개",
  {2025: 19.0, 2026: 35.0}, None, 2026, "LightCounting", "S1", "p.5", "B",
  "2025년 1,800만~1,990만 개(중간값 반영), 2026년 3,500만 개 이상(S3 p.2). 800G 수요는 2028년 정점")
m("u16", "Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "1.6T 모듈 출하량", "", "백만 개",
  {2025: 3.0, 2026: 10.0}, None, 2026, "LightCounting / Cignal AI", "S1", "p.5", "B",
  "2025년 250만~350만 개(S1, 중간값 반영; S3는 180만 개), 2026년 1,000만 개 돌파 전망(Cignal AI, S17)")
m("coh", "Midstream", "ODL(광트랜시버)", "코히어런트 트랜시버", "코히어런트 모듈", "코히어런트 플러그형+임베디드", "USD bn",
  {2025: 6.0, 2028: 8.0}, None, 2028, "Cignal AI", "S16", "본문", "B",
  "2028년 80억달러는 S34(2025.09 발표). 800ZR/ZR+ 2025~29 CAGR 145%, Dell'Oro ZR/ZR+ 출하 5년 CAGR 29%(S19)")
m("dcoi", "Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "데이터센터 광인터커넥트(Coherent·LightCounting)", "플러그형+CPO", "USD bn",
  {2030: 30.0}, "=(30/10)^(1/6)-1", 2030, "LightCounting", "S33", "본문", "B",
  "2024년 약 100억달러 → 2030년 300억달러(플러그형 250억 + CPO 50억)")
m("dcoi_dx", "Midstream", "ODL(광트랜시버)", "고속 데이터센터 트랜시버", "데이터센터 광인터커넥트(东兴证券)", "광의 정의(CPO·광 I/O 포함 추정)", "USD bn",
  {2030: 144.4}, 0.481, 2030, "LightCounting·灼识咨询(CIC)", "S2", "p.7", "B",
  "2024년 137억달러, CAGR 48.1%. 광인터커넥트 전체 2024 179억→2030 1,514억달러")
m("access", "Midstream", "FTTH(광가입자망·PON)", "OLT용 트랜시버", "액세스 광모듈(FTTx+무선 프론트홀)", "PON+프론트홀/백홀", "USD bn",
  {2029: 2.9}, "=(2.9/1.6)^(1/6)-1", 2029, "LightCounting", "S15", "본문", "B",
  "2024년이 사이클 저점. 2023년 약 16억달러(PON 약 10억 + 무선 약 6억, S5 p.9) 기준으로 성장률 산출")
m("fttx", "Midstream", "FTTH(광가입자망·PON)", "OLT용 트랜시버", "FTTx(PON) 광모듈", "", "USD bn",
  {2025: 0.631}, None, 2025, "华鑫证券 전망", "S6", "p.47", "B", "2025년 출하 9,208만 개(2024년 발간 전망치)")
m("fh", "Midstream", "ODL(광트랜시버)", "무선 프론트홀·백홀 트랜시버", "무선 프론트홀·백홀 광모듈", "", "USD bn", {}, None, None,
  "LightCounting", "S5", "p.9", "-", "2023년 약 6억달러만 공개, 연도별 전망 미확인")
m("cpo_lc", "Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "CPO(LightCounting)", "", "USD bn",
  {2030: 5.0}, None, 2030, "LightCounting", "S33", "본문", "B",
  "기관별 편차 큼: Yole CPO 패키징 2031년 약 50억(S11), GII 2030년 5.9억(S8 p.4)")
m("cpo_gii", "Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "CPO(GII, 참고)", "", "USD bn",
  {2030: 0.5856}, 0.382, 2030, "GII(Global Information)", "S8", "p.4", "C",
  "2024년 8,410만달러, CAGR 38.2%. Mordor 2026 1.6억→2031 7.6억, IDTechEx 2037년 200억달러 초과")
m("aoc", "Midstream", "ODL(광트랜시버)", "차세대 인터커넥트", "AOC·DAC·AEC", "", "USD bn",
  {2028: 2.8}, "=(2.8/1.2)^(1/5)-1", 2028, "LightCounting", "S32", "-", "C", "2023년 12억달러 → 2028년 28억달러")
m("edfa", "Midstream", "RF(아날로그 광·RF-optics)", "광증폭·RoF", "EDFA 광증폭기", "", "USD bn",
  {2025: 0.97, 2030: 1.39}, None, 2030, "Industry Research", "S7", "p.45", "C", "CAGR 7.2%. RF머트리얼즈 관련")
m("catv", "Midstream", "RF(아날로그 광·RF-optics)", "CATV·HFC 광전송", "CATV 아날로그 광송수신기", "", "USD bn", {}, None, None,
  "-", "-", "-", "-", "공개 자료 미확인. 하위 장비 시장은 'Cable DAA 장비' 행 참고")

m("capex", "Downstream", "최종 수요처", "데이터센터 사업자", "데이터센터 Capex(Dell'Oro 2026.02)", "전 세계 데이터센터 투자", "USD bn",
  {2025: 593, 2026: 1000, 2030: 1700}, None, 2030, "Dell'Oro Group", "S22", "본문", "A",
  "2025년 593은 S9 slide 13(Dell'Oro 인용). 2026년 '1조달러 근접'")
m("capex2", "Downstream", "최종 수요처", "데이터센터 사업자", "데이터센터 Capex(Dell'Oro 2026.07 상향)", "", "USD bn",
  {2030: 3000}, None, 2030, "Dell'Oro Group", "S23", "-", "B", "2030년 3조달러 초과로 상향(AI 가속기가 약 1/3)")
m("hyper", "Downstream", "최종 수요처", "데이터센터 사업자", "미국 Top4 하이퍼스케일러 Capex", "Amazon·Google·Meta·Microsoft", "USD bn",
  {2025: 327, 2026: 600}, None, 2026, "기업 공시 / Dell'Oro", "S9", "slide 10", "A",
  "CY23 153 → CY24 248 → CY25 327(S9). 2026년 '약 6,000억달러'(S22)")
m("mck", "Downstream", "최종 수요처", "데이터센터 사업자", "데이터센터 누적 Capex(~2030, McKinsey)", "2030년까지 누적", "USD bn(누적)",
  {2030: 6700}, None, 2030, "McKinsey & Company", "S29", "-", "B",
  "AI용 5.2조 + 일반 IT 1.5조달러. 기술(장비) 개발사 몫 약 60%. 2030 칸은 연간이 아닌 누적값")
m("aisw", "Downstream", "네트워크 장비(시스템)", "데이터센터 네트워크", "AI 백엔드 스위치", "AI 백엔드 네트워크용 DC 스위치", "USD bn",
  {2030: 100}, None, 2030, "Dell'Oro Group", "S20", "본문", "A",
  "2026.07 업데이트: 2026~30 누적 1조달러 근접, 2030년 스케일업 비중 50% 초과(S21)")
m("otn", "Downstream", "네트워크 장비(시스템)", "광전송 장비", "광전송 장비 전체", "", "USD bn",
  {2029: 19.0}, 0.05, 2029, "Dell'Oro Group", "S18", "본문", "A", "2024년 -9% 후 반등, 5년 연평균 5%")
m("ipo", "Downstream", "네트워크 장비(시스템)", "광전송 장비", " └ IPoDWDM", "ZR/ZR+ 포함", "USD bn",
  {2030: 7.0}, 0.27, 2030, "Dell'Oro Group", "S19", "본문", "A", "2030년 70억달러 초과, CAGR 27%")
m("dwdm", "Downstream", "네트워크 장비(시스템)", "광전송 장비", " └ Disaggregated WDM", "IPoDWDM·트랜스폰더·OLS", "USD bn",
  {2030: 13.0}, 0.17, 2030, "Dell'Oro Group", "S19", "본문", "A", "2030년 약 130억달러, CAGR 17%")
m("bb", "Downstream", "네트워크 장비(시스템)", "유선 액세스 장비", "브로드밴드 액세스 장비 전체", "", "USD bn",
  {2028: 18.8}, None, 2028, "Dell'Oro Group", "S24", "본문", "A",
  "2028년 정점, 2025~30 연평균 +0.3%(2026.07 업데이트 2026~30 +0.5%)")
m("pon", "Downstream", "네트워크 장비(시스템)", "유선 액세스 장비", "PON 장비", "", "USD bn",
  {2029: 12.6}, "=(12.6/10.7)^(1/5)-1", 2029, "Dell'Oro Group", "S25", "-", "B",
  "2024년 107억달러. 이후 발표 CAGR: 2025~30 1.9%(S24), 2026~30 1.6%")
m("daa", "Downstream", "네트워크 장비(시스템)", "케이블 HFC 장비", "Cable DAA 장비", "vCCAP·RPD·RMD·R-OLT", "USD bn",
  {2030: 1.2}, None, 2030, "Dell'Oro Group", "S24", "본문", "A", "DOCSIS 4.0·초기 광 전환 투자")
m("ran", "Downstream", "네트워크 장비(시스템)", "무선 장비", "RAN", "이동통신 기지국(서비스 제외)", "USD bn",
  {}, 0.01, 2030, "Dell'Oro Group", "S27", "-", "B",
  "2025~29 누적 1,600억달러(S27)를 5로 나눠 2025년 반영(자체 환산), 이후 CAGR 1%(S26, 2026.07)",
  special={2025: "=160/5"})
m("airan", "Downstream", "네트워크 장비(시스템)", "무선 장비", "AI-RAN", "", "USD bn", {}, None, None, "Dell'Oro Group", "S28", "-", "-",
  "향후 5년 누적 350억달러. RAN 전체 규모를 키우지는 않는 것으로 전망")

# ---------------------------------------------------------------- build
wb = Workbook()
ws1 = wb.active
ws1.title = "구조표"
ws2 = wb.create_sheet("밸류체인")
ws3 = wb.create_sheet("시장규모")

# ======================= tab3 first (row numbers needed for tab2 links)
COLS3 = ["No", "Stream", "사업", "제품", "품목·지표", "정의(범위)", "단위", "2025", "2026", "2027", "2028", "2029", "2030",
         "CAGR(25→30)", "적용 성장률", "값 처리", "원출처(조사기관)", "인용 문헌", "위치", "링크", "확인 방법", "신뢰도", "비고"]
put(ws3, 2, 2, "통신용 광모듈 사업·제품·품목별 시장규모 (2025~2030)", bold=True, border=False)
put(ws3, 3, 2, "단위: USD bn(별도 표기 제외) · 파란 글씨 = 원문 수치(입력) · 검정 = 원문 수치·성장률로 계산한 값 · 기울임 = 원문 전망 기간 밖 연장(자체) · 조회일 2026.11.24", border=False)
put(ws3, 4, 2, "신뢰도: A = 기관 원문 직접 확인 · B = 증권사·언론이 기관 수치를 인용(PDF·기사 원문 확인) · C = 범용 시장조사사 수치 또는 검색 요약으로만 확인", border=False)
put(ws3, 5, 2, "기관별 정의·발간 시점이 달라 행 사이 단순 비교·합산에 주의. 내부 분석 보조자료이며 투자 권유가 아님.", border=False)
HR3 = 7
header(ws3, HR3, COLS3)
YC = {y: 9 + i for i, y in enumerate(YEARS)}  # I..N
cI, cN = CL(YC[2025]), CL(YC[2030])
row_of = {}
r = HR3 + 1
cur_stream = None
cnt = {"Upstream": 0, "Midstream": 0, "Downstream": 0}
PFX = {"Upstream": "U", "Midstream": "M", "Downstream": "D"}


def fmt_for(d):
    vals = [v for v in d["src"].values()]
    mx = max(vals) if vals else 1
    if mx >= 100:
        return "#,##0"
    if mx >= 10:
        return "#,##0.0"
    return "#,##0.00"


def yr_list(ys):
    ys = sorted(ys)
    if not ys:
        return ""
    out, s = [], ys[0]
    prev = s
    for y in ys[1:] + [None]:
        if y is not None and y == prev + 1:
            prev = y
            continue
        out.append(str(s) if s == prev else f"{s}–{prev}")
        if y is not None:
            s = prev = y
    return ", ".join(out)


for d in M:
    if d["stream"] != cur_stream:
        cur_stream = d["stream"]
        for c in range(2, 2 + len(COLS3)):
            put(ws3, r, c, None, fill=BAND)
        put(ws3, r, 2, STREAM_TITLE[cur_stream], bold=True, fill=BAND)
        r += 1
    cnt[d["stream"]] += 1
    no = f"{PFX[d['stream']]}-{cnt[d['stream']]:02d}"
    d["no"] = no
    row_of[d["key"]] = r
    fm = fmt_for(d) if d["src"] else ("#,##0.0" if d["special"] else "#,##0.00")
    put(ws3, r, 2, no, h="center")
    put(ws3, r, 3, d["stream"])
    put(ws3, r, 4, d["biz"])
    put(ws3, r, 5, d["prod"])
    put(ws3, r, 6, d["item"], bold=not d["item"].startswith(" └"))
    put(ws3, r, 7, d["scope"] or "-")
    put(ws3, r, 8, d["unit"], h="center")
    # growth col P
    gcol = 16
    g = d["g"]
    if g is None:
        put(ws3, r, gcol, "n/a", h="right")
    elif isinstance(g, str):
        put(ws3, r, gcol, f"=IFERROR({g[1:]},\"n/a\")", fmt="0.0%", h="right")
    else:
        put(ws3, r, gcol, g, color=BLUE, fmt="0.0%", h="right")
    P = f"$P{r}"
    src = d["src"]
    sy = sorted(src)
    modes = {}
    for y in YEARS:
        col = YC[y]
        c = CL(col)
        beyond = d["hz"] is not None and y > d["hz"]
        if y in d["special"]:
            f = d["special"][y].format(I=f"I{r}", J=f"J{r}", K=f"K{r}", L=f"L{r}", M=f"M{r}", N=f"N{r}")
            put(ws3, r, col, f"=IFERROR({f[1:]},\"n/a\")", fmt=fm, h="right", italic=beyond)
            modes[y] = "calc"
            continue
        if y in src:
            put(ws3, r, col, src[y], color=BLUE, fmt=fm, h="right")
            modes[y] = "src"
            continue
        a = max([s for s in sy if s < y], default=None)
        b = min([s for s in sy if s > y], default=None)
        if a is not None and b is not None and a in YC and b in YC:
            A, B = f"{CL(YC[a])}{r}", f"{CL(YC[b])}{r}"
            put(ws3, r, col, f"=IFERROR({A}*({B}/{A})^(({y}-{a})/({b}-{a})),\"n/a\")", fmt=fm, h="right")
            modes[y] = "interp"
        elif g is not None and a is None and b is not None:
            # 첫 원문 연도 이전: 다음 칸 ÷ (1+g) 로 역산 (오른쪽 → 왼쪽 단방향 참조)
            nxt = f"{CL(col + 1)}{r}"
            put(ws3, r, col, f"=IFERROR({nxt}/(1+{P}),\"n/a\")", fmt=fm, h="right")
            modes[y] = "back"
        elif g is not None and y > 2025 and (a is not None or modes.get(y - 1) in ("calc", "fwd", "fwd_x")):
            # 마지막 원문(또는 계산) 연도 이후: 이전 칸 × (1+g) (왼쪽 → 오른쪽 단방향 참조)
            prev = f"{CL(col - 1)}{r}"
            put(ws3, r, col, f"=IFERROR({prev}*(1+{P}),\"n/a\")", fmt=fm, h="right", italic=beyond)
            modes[y] = "fwd_x" if beyond else "fwd"
        else:
            put(ws3, r, col, "n/a", h="right")
            modes[y] = "na"
    # back-calculation must be resolved right-to-left: fix rows where back needs later back values (already referencing next col)
    put(ws3, r, 15, f"=IFERROR(({cN}{r}/{cI}{r})^(1/5)-1,\"n/a\")", fmt="0.0%", h="right")
    parts = []
    lab = {"src": "원문", "interp": "원문 사이 보간", "back": "원문 성장률로 역산", "fwd": "원문 성장률 적용",
           "fwd_x": "원문 기간 밖 연장(자체)", "calc": "원문 성장률로 계산", "na": "자료 없음"}
    if d["key"] == "ran":
        lab["calc"] = "자체 환산(누적÷5)"
    for k in ["src", "calc", "interp", "back", "fwd", "fwd_x", "na"]:
        ys = [y for y in YEARS if modes.get(y) == k]
        if ys:
            parts.append(f"{lab[k]}: {yr_list(ys)}")
    put(ws3, r, 17, " / ".join(parts), wrap=True)
    put(ws3, r, 18, d["orig"], wrap=True)
    sc = d["cite"]
    if sc in S:
        put(ws3, r, 19, f"{sc} {S[sc][0]}, 「{S[sc][1]}」({S[sc][2]})", wrap=True)
        put(ws3, r, 21, S[sc][4], color=BLUE, link=S[sc][4], underline="single")
        put(ws3, r, 22, S[sc][5])
    else:
        put(ws3, r, 19, "-")
        put(ws3, r, 21, "-")
        put(ws3, r, 22, "-")
    put(ws3, r, 20, d["loc"], h="center")
    put(ws3, r, 23, d["grade"], h="center")
    put(ws3, r, 24, d["note"] or "-", wrap=True)
    r += 1

# Check rows for laser breakdown (source rounding)
r += 1
put(ws3, r, 2, "Check", bold=True, border=False)
put(ws3, r, 6, "원문 표 합계 검증(0이면 '-'; ±0.1은 원문 반올림 차이)", border=False)
r += 1
CHECKS3 = [("Check: 레이저 칩 전체 − (CW + EML + 기타)", "laser", ["cw", "eml", "oth"]),
           ("Check: CW − (50mW 이하 + 70·100mW + 100mW 초과)", "cw", ["cw1", "cw2", "cw3"]),
           ("Check: EML − (50G 이하 + 100G + 200G 이상)", "eml", ["eml1", "eml2", "eml3"])]
for lab_, tot, comps in CHECKS3:
    put(ws3, r, 6, lab_)
    for y in YEARS:
        c = CL(YC[y])
        refs = ",".join(f"{c}{row_of[k]}" for k in comps)
        put(ws3, r, YC[y], f"=IFERROR(ROUND({c}{row_of[tot]}-SUM({refs}),2),\"n/a\")",
            fmt='#,##0.0;(#,##0.0);"-"', h="right")
    r += 1

# Source list
r += 1
put(ws3, r, 2, "출처 목록", bold=True, border=False)
r += 1
header(ws3, r, ["코드", "발행처", "제목", "발간일", "원출처(조사기관)", "링크", "확인 방법"])
r += 1
for k, (pub, title, dt, orig, link, how) in S.items():
    put(ws3, r, 2, k, h="center")
    put(ws3, r, 3, pub, wrap=True)
    put(ws3, r, 4, title, wrap=True)
    put(ws3, r, 5, dt)
    put(ws3, r, 6, orig, wrap=True)
    put(ws3, r, 7, link, color=BLUE, link=link, underline="single")
    put(ws3, r, 8, how)
    r += 1

widths3 = {"A": 2, "B": 7, "C": 11, "D": 18, "E": 20, "F": 34, "G": 24, "H": 10, "I": 9, "J": 9, "K": 9, "L": 9, "M": 9,
           "N": 9, "O": 11, "P": 10, "Q": 30, "R": 24, "S": 46, "T": 11, "U": 40, "V": 22, "W": 7, "X": 60}
for k, v in widths3.items():
    ws3.column_dimensions[k].width = v

# ======================= tab1 구조표
put(ws1, 2, 2, "통신용 광모듈 밸류체인 구조표 (Upstream · Midstream · Downstream × 사업 · 제품 · 품목)", bold=True, border=False)
put(ws1, 3, 2, "용어: ODL = Optical Data Link(광 데이터 링크 = 광트랜시버, SFP·SFP+·QSFP 등). FTTH = 광가입자망(PON) 광부품. RF = RF-optics(케이블TV 아날로그 광송수신·RoF).", border=False)
put(ws1, 4, 2, "빛과전자(구 라이트론)는 FTTH·ODL·RF로 사업을 나누며, 그중 ODL 매출은 이동통신(무선 프론트홀)용 광트랜시버가 중심. 오른쪽 열에 각 품목이 어느 분류에 해당하는지 표기.", border=False)
header(ws1, 6, ["Stream", "사업", "제품", "품목", "무엇인가(설명)", "주요 적용처", "빛과전자 분류 대응"])
r = 7
prev = (None, None, None)
for (st, biz, prod, item, desc, use, mp, ov, kr) in VC:
    if st != prev[0]:
        for c in range(2, 9):
            put(ws1, r, c, None, fill=BAND)
        put(ws1, r, 2, STREAM_TITLE[st], bold=True, fill=BAND)
        r += 1
    put(ws1, r, 2, st if st != prev[0] else None)
    put(ws1, r, 3, biz if (st, biz) != prev[:2] else None, bold=True)
    put(ws1, r, 4, prod if (st, biz, prod) != prev else None)
    put(ws1, r, 5, item, bold=True)
    put(ws1, r, 6, desc, wrap=True)
    put(ws1, r, 7, use, wrap=True)
    put(ws1, r, 8, mp, h="center")
    prev = (st, biz, prod)
    r += 1
for k, v in {"A": 2, "B": 12, "C": 24, "D": 24, "E": 30, "F": 52, "G": 40, "H": 14}.items():
    ws1.column_dimensions[k].width = v

# ======================= tab2 밸류체인
NOV, NKR = 8, 6
put(ws2, 2, 2, "통신용 광모듈 밸류체인 — 사업·제품·품목별 기업 (셀 1개 = 기업 1개)", bold=True, border=False)
put(ws2, 3, 2, "각 Stream 위 표 = 시장규모 추정(USD bn, '시장규모' 탭 연동). 해외①~⑧ · 국내①~⑥. 괄호는 역할·상태 보충.", border=False)
put(ws2, 4, 2, "국내 기업 배치는 사용자 제공 테마 목록(무선·유선/BEAD·데이터센터 광통신·방산/우주)을 반영. 하단에 테마별 매핑표 별도 정리.", border=False)
cols2 = ["Stream", "사업", "제품", "품목"] + [f"해외{chr(0x2460 + i)}" for i in range(NOV)] + [f"국내{chr(0x2460 + i)}" for i in range(NKR)]
header(ws2, 6, cols2)
NC2 = 2 + len(cols2)
REF = "'시장규모'!"
NO = {d["key"]: d["no"] for d in M}
STREAM_MKT = {
    "Upstream": [("광칩·전기칩·수동부품 합산", ["laser", "ic", "siph", "awg", "fau"],
                  "레이저칩({laser}) + 인터커넥트 IC({ic}) + 실리콘포토닉스 칩({siph}) + AWG({awg}) + FAU({fau}). 패키징·기판·광섬유 제외(정의 상이)")],
    "Midstream": [("광트랜시버 시장 (Yole)", ["tx_yole"], "{tx_yole}. 2031년 1,120억달러"),
                  ("광트랜시버 시장 (LightCounting)", ["tx_lc"], "{tx_lc}. 2026.10 이더넷 성장률 상향 전 기준")],
    "Downstream": [("네트워크 장비 합산 (광전송+PON+RAN)", ["otn", "pon", "ran"],
                    "{otn} + {pon} + {ran}. AI 백엔드 스위치({aisw})는 연도별 공개치가 없어 제외(2030년 1,000억달러+)"),
                   ("데이터센터 Capex (Dell'Oro, 수요 동인)", ["capex"], "{capex}. 2026.07 상향 시 2030년 3조달러+({capex2})")],
}
STREAM_MKT = {k: [(a, b, c.format(**NO)) for (a, b, c) in v] for k, v in STREAM_MKT.items()}
assert all(len(t) == 9 for t in VC), [t[3] for t in VC if len(t) != 9]
r = 7
prev = (None, None, None)
mk_rows = {}
for (st, biz, prod, item, desc, use, mp, ov, kr) in VC:
    if st != prev[0]:
        # market size mini table
        r += 1 if r > 7 else 0
        mh = [st, "시장규모 추정 (USD bn)", "지표", "구성·비고"] + [str(y) for y in YEARS] + ["CAGR(25→30)"]
        for i, lab_ in enumerate(mh):
            put(ws2, r, 2 + i, lab_, bold=True, fill=SUB, h="center" if i >= 4 else "left")
        r += 1
        lines = []
        for (label, keys, comp) in STREAM_MKT[st]:
            put(ws2, r, 2, st)
            put(ws2, r, 3, "시장규모")
            put(ws2, r, 4, label, bold=True)
            put(ws2, r, 5, comp, wrap=True)
            for i, y in enumerate(YEARS):
                c3 = CL(YC[y])
                expr = "+".join(f"{REF}{c3}{row_of[k]}" for k in keys)
                put(ws2, r, 6 + i, f"=IFERROR({expr},\"n/a\")", fmt="#,##0.0", h="right")
            put(ws2, r, 12, f"=IFERROR((K{r}/F{r})^(1/5)-1,\"n/a\")", fmt="0.0%", h="right")
            lines.append((r, keys))
            r += 1
        for (lr, keys) in lines:
            put(ws2, r, 4, "Check")
            put(ws2, r, 5, f"{ws2.cell(lr, 4).value} − '시장규모' 탭 원값 합")
            for i, y in enumerate(YEARS):
                c3 = CL(YC[y])
                expr = "+".join(f"{REF}{c3}{row_of[k]}" for k in keys)
                c2 = CL(6 + i)
                put(ws2, r, 6 + i, f"=IFERROR(ROUND({c2}{lr}-({expr}),6),\"n/a\")", fmt='#,##0;(#,##0);"-"', h="right")
            r += 1
        r += 1
        for c in range(2, NC2):
            put(ws2, r, c, None, fill=BAND)
        put(ws2, r, 2, STREAM_TITLE[st], bold=True, fill=BAND)
        r += 1
    put(ws2, r, 2, st if st != prev[0] else None)
    put(ws2, r, 3, biz if (st, biz) != prev[:2] else None, bold=True)
    put(ws2, r, 4, prod if (st, biz, prod) != prev else None)
    put(ws2, r, 5, item, bold=True)
    for i in range(NOV):
        put(ws2, r, 6 + i, ov[i] if i < len(ov) else None)
    for i in range(NKR):
        put(ws2, r, 6 + NOV + i, kr[i] if i < len(kr) else None)
    prev = (st, biz, prod)
    r += 1

# theme mapping table
r += 2
put(ws2, r, 2, "국내 테마별 관련 기업 → 밸류체인 위치 (사용자 제공 목록 기준)", bold=True, border=False)
r += 1
header(ws2, r, ["테마", "기업", "밸류체인 위치", "역할", "근거"])
r += 1
THEME = [
    ("무선 투자·미국 주파수 경매·AI-RAN", "RFHIC", "Upstream > RF 소자 > GaN RF 트랜지스터·PA / Midstream > 무선 RF 모듈", "기지국용 GaN 증폭기", "회사 사업 개요"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "케이엠더블유", "Midstream > 무선 RF 모듈 > RU·안테나 / Upstream > RF 필터", "RU·안테나·필터", "회사 사업 개요, S7"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "오이솔루션", "Midstream > ODL > 무선 프론트홀 트랜시버 (+ Upstream EML·DFB 칩)", "프론트홀 광트랜시버, 데이터센터 800G·1.6T 확대", "S7"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "쏠리드", "Downstream > 무선 장비 / Midstream > RoF·DAS", "중계기·DAS·O-RAN RU", "회사 사업 개요, S7"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "이노와이어리스", "Downstream > 무선 장비 (계측·스몰셀)", "기지국 계측·스몰셀", "회사 사업 개요"),
    ("무선 투자·미국 주파수 경매·AI-RAN", "에치에프알", "Downstream > 무선 장비 (프론트홀·백홀)", "모바일 프론트홀 장비", "회사 사업 개요"),
    ("유선 투자·BEAD", "대한광통신", "Upstream > 광섬유·광케이블", "광섬유·광케이블, 북미 인캡 인수(2Q25)", "S7"),
    ("유선 투자·BEAD", "자람테크놀로지", "Upstream > 전기 칩 > PON 칩셋", "PON SoC", "회사 사업 개요"),
    ("유선 투자·BEAD", "가온그룹", "Downstream > 유선 액세스 장비 > 가입자 CPE", "셋톱박스·게이트웨이 등 가입자 단말", "회사 사업 개요"),
    ("유선 투자·BEAD", "에치에프알", "Downstream > 유선 액세스 장비", "광 액세스 장비", "회사 사업 개요"),
    ("데이터센터 광통신", "RF머트리얼즈", "Upstream > 패키지·펌프 레이저 / Midstream > EDFA", "Lumentum향 광 패키징·펌프 레이저·EDFA (대신증권 Top Pick)", "S7"),
    ("데이터센터 광통신", "대한광통신", "Upstream > 광섬유·광케이블", "데이터센터·백본 광케이블", "S7"),
    ("데이터센터 광통신", "오이솔루션", "Midstream > ODL 400G·800G·1.6T / Upstream > EML", "2025년 매출 트랜시버 90%·레이저칩 10%", "S7"),
    ("데이터센터 광통신", "성호전자", "Upstream > 제조·검사 장비 (자회사 ADS테크)", "CPO용 능동정렬 장비, 미국 고객사 235억원 수주(2026.08)", "언론 보도(머니투데이 2026.08.05)"),
    ("방산·우주 통신", "RFHIC", "Upstream > RF 소자 > GaN", "방산 레이더·위성용 GaN", "회사 사업 개요"),
    ("방산·우주 통신", "웨이비스", "Upstream > RF 소자 > GaN", "방산용 GaN RF", "회사 사업 개요"),
    ("방산·우주 통신", "RF시스템즈", "Downstream > 위성·방산 통신", "위성통신 단말·안테나", "회사 사업 개요"),
    ("방산·우주 통신", "센서뷰", "Upstream > RF 소자 > RF 케이블·커넥터", "RF 케이블·커넥터", "회사 사업 개요"),
    ("방산·우주 통신", "이노와이어리스", "Downstream > 위성·방산 통신 / 무선 장비", "통신 계측", "사용자 테마 분류"),
]
prev_t = None
for t, co, pos, role, basis in THEME:
    put(ws2, r, 2, t if t != prev_t else None, bold=True)
    put(ws2, r, 3, co, bold=True)
    put(ws2, r, 4, pos, wrap=True)
    put(ws2, r, 5, role, wrap=True)
    put(ws2, r, 6, basis)
    prev_t = t
    r += 1

for k, v in {"A": 2, "B": 12, "C": 22, "D": 30, "E": 34}.items():
    ws2.column_dimensions[k].width = v
for i in range(NOV + NKR):
    ws2.column_dimensions[CL(6 + i)].width = 25

# ---------------------------------------------------------------- fonts
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            apply_font(c)
wb.save(OUT)
print("saved", OUT, "rows3", len(M))
