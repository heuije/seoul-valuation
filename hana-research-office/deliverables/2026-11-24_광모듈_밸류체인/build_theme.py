"""투자 테마별 관련 기업 탭만 다시 만든다 (DART 2025 사업보고서 기준)."""
import re, sys
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont

SRC, OUT = sys.argv[1], sys.argv[2]
SHEET = "투자 테마별 관련 기업"

# ---------------------------------------------------------------- 하우스룰 글꼴 코드 (스킬 원문 그대로)
KR, EN = "맑은 고딕", "Arial"
HAN = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
LAT = re.compile(r"[A-Za-z0-9]")
def split_runs(s):
    kinds = [True if HAN.match(ch) else (False if LAT.match(ch) else None) for ch in s]
    nxt = None
    for i in range(len(kinds)-1, -1, -1):
        if kinds[i] is None: kinds[i] = nxt
        else: nxt = kinds[i]
    prev = None
    for i, k in enumerate(kinds):
        if k is None: kinds[i] = prev
        prev = kinds[i] if kinds[i] is not None else prev
    runs = []
    for ch, k in zip(s, kinds):
        k = bool(k)
        if runs and runs[-1][1] == k: runs[-1][0] += ch
        else: runs.append([ch, k])
    return runs
def apply_font(cell, cached=None):
    v = cell.value
    if v is None: return
    f = copy(cell.font)
    if isinstance(v, str) and v.startswith("="):
        f.name = KR if (isinstance(cached, str) and HAN.search(cached)) else EN
        cell.font = f; return
    if not isinstance(v, (str, CellRichText)):
        f.name = EN; cell.font = f; return
    s = str(v); has_kr = bool(HAN.search(s))
    f.name = KR if has_kr else EN
    cell.font = f
    runs = split_runs(s)
    if has_kr and len(runs) > 1:
        cell.value = CellRichText([TextBlock(InlineFont(rFont=KR if k else EN, sz=f.sz, b=f.b, i=f.i, u=f.u,
            color=copy(f.color) if f.color else None), t) for t, k in runs])

# ---------------------------------------------------------------- 데이터 (DART 2025 사업보고서, 단위 백만원)
DART = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo="
RCP = {
    "RFHIC": ("20260331004907", "2026.03.31 기재정정"), "케이엠더블유": ("20260319000852", "2026.03.19"),
    "오이솔루션": ("20260319001159", "2026.03.19"), "쏠리드": ("20260324000935", "2026.03.24 기재정정"),
    "이노와이어리스": ("20260325001192", "2026.03.25 기재정정"), "에치에프알": ("20260319001383", "2026.03.19"),
    "대한광통신": ("20260319000854", "2026.03.19"), "자람테크놀로지": ("20260318000646", "2026.03.18"),
    "가온그룹": ("20260317000844", "2026.03.17"), "RF머트리얼즈": ("20260318001224", "2026.03.18"),
    "성호전자": ("20260320001361", "2026.03.20"), "웨이비스": ("20260317000533", "2026.03.17"),
    "RF시스템즈": ("20260317000729", "2026.03.17"), "센서뷰": ("20260311004387", "2026.03.11"),
    "빛과전자": ("20260320001115", "2026.03.20"), "옵티코어": ("20260323001681", "2026.03.23"),
}
W, L, D, B = "무선 투자·미국 주파수 경매·AI-RAN", "유선 투자·BEAD", "데이터센터 광통신", "방산·우주 통신"
# (테마, 기업(표시), 기업키, Stream, 기업 유형, 주력 제품, 역할, 주력제품 매출, 총 매출액, 매출 기준·산정)
ROWS = [
    (W, "RFHIC", "RFHIC", "Upstream", "칩·소자", "GaN 트랜지스터·전력증폭기",
     "기지국용 GaN 전력증폭기(레이더·RF 에너지용 병행)", 184907, 185804,
     "연결. GaN 트랜지스터 등 44,726 + GaN 전력증폭기 등 140,181. 통신·방산 구분 미공시. 연결에 RF머트리얼즈·RF시스템즈 포함"),
    (W, "케이엠더블유", "케이엠더블유", "Midstream", "RF 부품·모듈", "RF 부품(필터·안테나·시스템)",
     "기지국 RU·안테나·필터(그 외 LED 조명 20%)", 78402, 97519,
     "연결. RF부문 = SYSTEM 2,145 + ANTENNA 18,974 + FILTER 등 57,283"),
    (W, "오이솔루션", "오이솔루션", "Midstream", "광모듈", "광트랜시버",
     "무선 프론트홀 광트랜시버, 데이터센터 800G·1.6T 확대", 53741, 57377,
     "연결 부문정보(광통신 모듈 부문). 광통신 소자 부문 3,636(6%) 별도"),
    (W, "쏠리드", "쏠리드", "Downstream·Midstream", "통신장비", "무선 통신장비(중계기·DAS·O-RAN RU)",
     "중계기·DAS·O-RAN RU", 261333, 294830,
     "연결. 통신장비 부문(LTE·5G 등), 기타매출 11% 제외"),
    (W, "이노와이어리스", "이노와이어리스", "Downstream", "계측·통신장비", "이동통신 계측·스몰셀",
     "무선망 최적화·기지국 계측(T&M)·스몰셀(현 사명 LIG아큐버)", 74924, 186101,
     "연결. 무선망 최적화 39,415 + Big Data 10,389 + T&M 7,250 + SmallCell 17,870. 오토모티브(48%)·방산(7%) 제외"),
    (W, "에치에프알", "에치에프알", "Downstream", "통신장비", "Mobile Access(프론트홀·인빌딩)",
     "모바일 프론트홀·인빌딩 중계장비", 26972, 141983,
     "연결 부문별 매출(Mobile Access)"),
    (L, "대한광통신", "대한광통신", "Upstream·Midstream", "소재·케이블", "광섬유·광케이블",
     "프리폼·광섬유·광케이블, 북미 인캡 인수(2Q25). 전력선(OPGW) 42%", 81415, 139447,
     "연결. 통신사업(광케이블 외)"),
    (L, "자람테크놀로지", "자람테크놀로지", "Upstream·Midstream", "칩·광모듈", "PON 칩(XGSPON)·광트랜시버",
     "XGSPON 칩·SFP+ ONU, 통신사향 광트랜시버", 5517, 10644,
     "별도(종속회사 없음). XGSPON칩 및 관련제품 1,917(제품 811 + 용역 1,106) + 광트랜시버 3,600"),
    (L, "가온그룹", "가온그룹", "Downstream", "통신장비", "네트워크(광단말·가입자 CPE)",
     "광단말·가입자 CPE(OTT 셋톱 60%)", 205436, 517550,
     "연결. 네트워크 부문(Broadband 서비스)"),
    (L, "에치에프알", "에치에프알", "Downstream", "통신장비", "Broadband Access(OLT·ONU·ONT)",
     "가입자망 광회선 장비(OLT·ONU·ONT)", 111930, 141983,
     "연결 부문별 매출(Broadband Access, 무선데이터 전송장비 포함)"),
    (D, "RF머트리얼즈", "RF머트리얼즈", "Upstream", "부품", "통신용 패키지",
     "Lumentum향 광 패키지, RFHIC향 GaN 패키지, 펌프 레이저·EDFA", 22203, 64084,
     "연결. 통신용 패키지(광·무선 합산, 광 단독 미공시). 연결 매출의 52%는 자회사 RF시스템즈 군수용 장비부품"),
    (D, "대한광통신", "대한광통신", "Midstream", "소재·케이블", "광케이블",
     "데이터센터·백본 광케이블", 81415, 139447,
     "연결. 통신사업 전체(데이터센터용 구분 미공시)"),
    (D, "오이솔루션", "오이솔루션", "Midstream", "광모듈", "광트랜시버",
     "데이터센터 400G·800G·1.6T, EML 등 레이저 칩 자체 생산", 53741, 57377,
     "연결 부문정보(광통신 모듈 부문). 광통신 소자 부문 3,636(6%) 별도"),
    (D, "빛과전자 (추가)", "빛과전자", "Midstream", "광모듈", "광트랜시버(ODL)",
     "이동통신용 SFP·QSFP 위주, 1.6T OSFP 라인업. FTTH(PON) 광부품 14,876(50%)", 14962, 30050,
     "별도(제품별 연결 미공시, 연결 매출 31,770)"),
    (D, "옵티코어 (추가)", "옵티코어", "Midstream", "광모듈", "광트랜시버",
     "무선 프론트홀·백홀·광가입자망 광트랜시버, 광다중화장치", 9371, 21512,
     "연결. 제품 중 광트랜시버"),
    (D, "성호전자", "성호전자", "Upstream", "공정장비", "광트랜시버 조립용 능동정렬 장비",
     "자회사 ADS테크(2026년 인수): 광모듈·칩 정렬·접합·검사 장비. 본업은 전원공급장치·필름콘덴서", None, 231577,
     "연결. ADS테크는 2026년 편입이라 2025년 실적에 없음(2026.09 분기보고서 종속기업 요약 매출 27,212)"),
    (B, "RFHIC", "RFHIC", "Upstream", "칩·소자", "GaN 트랜지스터·전력증폭기",
     "레이더·전자전용 GaN 전력증폭기", 184907, 185804,
     "연결. 무선 테마와 같은 수치(통신·방산 구분 미공시)"),
    (B, "웨이비스", "웨이비스", "Upstream", "칩·소자", "GaN RF 반도체(칩·트랜지스터·모듈)",
     "방산용 GaN RF 칩·패키지 트랜지스터·모듈 국산화", 40239, 40706,
     "별도(종속회사 없음). 제품매출"),
    (B, "RF시스템즈", "RF시스템즈", "Downstream", "방산 시스템", "방산 레이다·안테나 시스템",
     "유도무기 탐색기 안테나·감시정찰 레이다·환경제어 시스템(RF머트리얼즈 자회사)", 32675, 38174,
     "별도(종속회사 없음). 레이다 12,945 + 안테나 15,142 + 환경제어 4,584 + 방산 상품 4"),
    (B, "센서뷰", "센서뷰", "Upstream", "부품", "RF 케이블·커넥터(국방·항공·우주)",
     "국방·항공·우주용 RF 케이블·필터·안테나(민수통신 73%)", 4886, 19016,
     "연결. 국방·항공·우주 부문"),
    (B, "이노와이어리스", "이노와이어리스", "Downstream", "계측·통신장비", "방산 전자전 장비",
     "레이더·통신 신호 탐지·분석(전자전)", 12734, 186101,
     "연결. 방산 제품군(2025년부터 별도 구분)"),
]

# ---------------------------------------------------------------- 시트 다시 쓰기
wb = load_workbook(SRC, rich_text=True)
ws = wb[SHEET]
hdr_src = ws["B2"]
HFONT, HFILL, HALIGN, HBORDER = copy(hdr_src.font), copy(hdr_src.fill), copy(hdr_src.alignment), copy(hdr_src.border)
DBORDER = copy(ws["C3"].border)
TFONT = copy(ws["B1"].font)

for rng in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(rng))
for row in ws.iter_rows():
    for c in row:
        c.value = None; c.hyperlink = None
        c.font = Font(name=KR, size=10); c.fill = PatternFill(); c.border = Border(); c.alignment = Alignment()
        c.number_format = "General"

BLACK, BLUE = "FF000000", "FF0000FF"
def put(r, col, v, bold=False, color=BLACK, h="left", wrap=True, fmt=None, link=None):
    c = ws.cell(r, col, v)
    c.font = Font(name=KR, size=10, bold=bold, color=color, underline="single" if link else None)
    c.alignment = Alignment(horizontal=h, vertical="center", wrap_text=wrap)
    c.border = copy(DBORDER)
    if fmt: c.number_format = fmt
    if link: c.hyperlink = link
    return c

ws["B1"] = "국내 투자 테마별 관련 기업"
ws["B1"].font = TFONT
ws["B1"].alignment = Alignment(horizontal="left", vertical="center")
HEAD = ["테마", "기업", "Stream", "기업 유형", "주력 제품", "역할", "25년 매출(비중)",
        "주력제품 매출\n(백만원)", "총 매출액\n(백만원)", "매출 기준·산정", "출처"]
for i, h in enumerate(HEAD):
    c = ws.cell(2, 2 + i, h)
    c.font, c.fill, c.alignment, c.border = copy(HFONT), copy(HFILL), copy(HALIGN), copy(HBORDER)

r = 3
na_rows = []
for (t, co, key, st, typ, prod, role, rev, tot, basis) in ROWS:
    put(r, 2, t, bold=True, h="center")
    put(r, 3, co, bold=True)
    put(r, 4, st, h="center")
    put(r, 5, typ, h="center")
    put(r, 6, prod)
    put(r, 7, role)
    put(r, 8, f'=IFERROR(IF(ISNUMBER(I{r}),TEXT(I{r}/100,"#,##0")&"억원("&TEXT(I{r}/J{r},"0%")&")",NA()),"n/a")', h="right", wrap=False)
    if rev is not None:
        put(r, 9, rev, color=BLUE, h="right", fmt="#,##0")
    else:
        put(r, 9, None, h="right")
        na_rows.append(r)
    put(r, 10, tot, color=BLUE, h="right", fmt="#,##0")
    put(r, 11, basis)
    rcp, dt = RCP[key]
    put(r, 12, f"DART 사업보고서 {dt}".replace(" 기재정정", "(정정)"), color=BLUE, link=DART + rcp)
    if key == "성호전자":
        ws.cell(r, 12).value = "DART 사업보고서 2026.03.20"
    r += 1
last = r - 1

# 테마 열 병합
s = 3
for rr in range(4, last + 2):
    if rr > last or ws.cell(rr, 2).value != ws.cell(s, 2).value:
        if rr - 1 > s:
            ws.merge_cells(start_row=s, start_column=2, end_row=rr - 1, end_column=2)
        s = rr

note = ("주) DART 2025 사업보고서 기준(2026.11.24 조회). 25년 매출(비중) = 주력제품 매출 ÷ 총 매출액, 억원 미만 반올림. "
        "연결 = 연결 재무제표 기준, 별도 = 종속회사가 없거나 제품별 매출을 별도 기준으로만 공시한 경우.")
nc = ws.cell(last + 2, 2, note)
nc.font = Font(name=KR, size=10)
nc.alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)

for col, w in {"A": 2, "B": 23.125, "C": 15, "D": 17, "E": 13, "F": 28, "G": 42, "H": 15, "I": 12, "J": 12, "K": 48, "L": 27}.items():
    ws.column_dimensions[col].width = w
for rr in range(1, last + 3):
    ws.row_dimensions[rr].height = None

# 글꼴 규칙 적용
for row in ws.iter_rows(min_row=1, max_row=last + 2):
    for c in row:
        if c.value is None: continue
        if isinstance(c.value, str) and c.value.startswith("="):
            apply_font(c, cached="n/a" if c.row in na_rows else "억원")
        else:
            apply_font(c)
ws.sheet_view.showGridLines = False
wb.save(OUT)
print("rows", 3, last, "n/a rows", na_rows)
