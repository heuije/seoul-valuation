"""Fluence 엑셀: 차트·이미지를 보존하기 위해 XML을 직접 편집한다.
usage: python3 -I fl_edit.py <unzipped_dir> <out.xlsx>
"""
import re, sys, os, zipfile, shutil
from xml.sax.saxutils import escape

SRC, OUT = sys.argv[1], sys.argv[2]
P = lambda *a: os.path.join(SRC, *a)
rd = lambda p: open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8").write(s)

# ------------------------------------------------------------------ styles
styles = rd(P("xl/styles.xml"))
def add_font(xml):
    global styles
    m = re.search(r'<fonts count="(\d+)"([^>]*)>', styles)
    n = int(m.group(1))
    styles = styles.replace(m.group(0), f'<fonts count="{n+1}"{m.group(2)}>', 1)
    styles = styles.replace("</fonts>", xml + "</fonts>", 1)
    return n
def add_fill(xml):
    global styles
    m = re.search(r'<fills count="(\d+)">', styles); n = int(m.group(1))
    styles = styles.replace(m.group(0), f'<fills count="{n+1}">', 1)
    styles = styles.replace("</fills>", xml + "</fills>", 1); return n
def add_border(xml):
    global styles
    m = re.search(r'<borders count="(\d+)">', styles); n = int(m.group(1))
    styles = styles.replace(m.group(0), f'<borders count="{n+1}">', 1)
    styles = styles.replace("</borders>", xml + "</borders>", 1); return n
F_AR_BLUE = add_font('<font><sz val="10"/><color rgb="FF0000FF"/><name val="Arial"/><family val="2"/></font>')
F_AR_BLK = add_font('<font><sz val="10"/><color rgb="FF000000"/><name val="Arial"/><family val="2"/></font>')
F_KR_BLK = add_font('<font><sz val="10"/><color rgb="FF000000"/><name val="맑은 고딕"/><family val="3"/><charset val="129"/></font>')
F_KR_TITLE = add_font('<font><b/><sz val="12"/><color rgb="FF000000"/><name val="맑은 고딕"/><family val="3"/><charset val="129"/></font>')
F_KR_HDR = add_font('<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="맑은 고딕"/><family val="3"/><charset val="129"/></font>')
F_AR_LINK = add_font('<font><u/><sz val="10"/><color rgb="FF0000FF"/><name val="Arial"/><family val="2"/></font>')
FILL_TEAL = add_fill('<fill><patternFill patternType="solid"><fgColor rgb="FF006C64"/><bgColor indexed="64"/></patternFill></fill>')
B_THIN = add_border('<border><left style="thin"><color rgb="FFBFBFBF"/></left><right style="thin"><color rgb="FFBFBFBF"/></right>'
                    '<top style="thin"><color rgb="FFBFBFBF"/></top><bottom style="thin"><color rgb="FFBFBFBF"/></bottom><diagonal/></border>')

xfs_block = re.search(r'<cellXfs count="(\d+)">(.*?)</cellXfs>', styles, re.S)
XF = re.findall(r'<xf [^>]*?(?:/>|>.*?</xf>)', xfs_block.group(2), re.S)
_memo = {}
def xf(base, font, h=None, wrap=None, fill=None, border=None, numfmt=None):
    key = (base, font, h, wrap, fill, border, numfmt)
    if key in _memo: return _memo[key]
    x = XF[base]
    x = re.sub(r'fontId="\d+"', f'fontId="{font}"', x)
    if 'applyFont="1"' not in x: x = x.replace("<xf ", '<xf applyFont="1" ', 1)
    if fill is not None:
        x = re.sub(r'fillId="\d+"', f'fillId="{fill}"', x)
        if 'applyFill="1"' not in x: x = x.replace("<xf ", '<xf applyFill="1" ', 1)
    if border is not None:
        x = re.sub(r'borderId="\d+"', f'borderId="{border}"', x)
        if 'applyBorder="1"' not in x: x = x.replace("<xf ", '<xf applyBorder="1" ', 1)
    if numfmt is not None:
        x = re.sub(r'numFmtId="\d+"', f'numFmtId="{numfmt}"', x)
        if 'applyNumberFormat="1"' not in x: x = x.replace("<xf ", '<xf applyNumberFormat="1" ', 1)
    if h or wrap:
        al = re.search(r"<alignment[^>]*/>", x)
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', al.group(0))) if al else {}
        if h: attrs["horizontal"] = h
        if wrap: attrs["wrapText"] = "1"
        attrs.setdefault("vertical", "center")
        new = "<alignment " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) + "/>"
        if al: x = x.replace(al.group(0), new)
        elif x.endswith("/>"): x = x[:-2] + ">" + new + "</xf>"
        else: x = x.replace("</xf>", new + "</xf>")
        if 'applyAlignment="1"' not in x: x = x.replace("<xf ", '<xf applyAlignment="1" ', 1)
    XF.append(x); _memo[key] = len(XF) - 1
    return len(XF) - 1

# ------------------------------------------------------------------ rich text (house rule: 한글 맑은 고딕 / 영숫자 Arial)
HAN = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]"); LAT = re.compile(r"[A-Za-z0-9]")
def split_runs(s):
    kinds = [True if HAN.match(ch) else (False if LAT.match(ch) else None) for ch in s]
    nxt = None
    for i in range(len(kinds) - 1, -1, -1):
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
def inline(text, sz=10, bold=False, color="FF000000", underline=False):
    if not HAN.search(text) or len(split_runs(text)) == 1:
        return f'<is><t xml:space="preserve">{escape(text)}</t></is>'
    out = []
    for t, k in split_runs(text):
        rp = ("<b/>" if bold else "") + ("<u/>" if underline else "") + f'<sz val="{sz}"/><color rgb="{color}"/><rFont val="{"맑은 고딕" if k else "Arial"}"/>'
        out.append(f'<r><rPr>{rp}</rPr><t xml:space="preserve">{escape(t)}</t></r>')
    return "<is>" + "".join(out) + "</is>"

# ------------------------------------------------------------------ cell editing
def col2n(c):
    n = 0
    for ch in c: n = n * 26 + ord(ch) - 64
    return n
def split_ref(ref):
    m = re.match(r"([A-Z]+)(\d+)", ref); return m.group(1), int(m.group(2))
CELL_RE = r'<c r="{ref}"(?: [^>]*?)?(?:/>|>.*?</c>)'
def get_style(sheet, ref):
    m = re.search(CELL_RE.format(ref=ref), sheet, re.S)
    if not m: return 0
    s = re.search(r' s="(\d+)"', m.group(0).split(">")[0]); return int(s.group(1)) if s else 0
def set_cell(sheet, ref, body_xml, style, t=None, row_attrs=None):
    col, row = split_ref(ref)
    t_attr = f' t="{t}"' if t else ""
    cell = f'<c r="{ref}" s="{style}"{t_attr}>{body_xml}</c>' if body_xml else f'<c r="{ref}" s="{style}"/>'
    rm = re.search(rf'<row r="{row}"(?: [^>]*?)?(?:/>|>.*?</row>)', sheet, re.S)
    if not rm:
        rows = [(int(x.group(1)), x.start()) for x in re.finditer(r'<row r="(\d+)"', sheet)]
        pos = next((p for r, p in rows if r > row), sheet.index("</sheetData>"))
        ra = f' {row_attrs}' if row_attrs else ""
        return sheet[:pos] + f'<row r="{row}"{ra}>{cell}</row>' + sheet[pos:]
    rx = rm.group(0)
    if rx.endswith("/>"): rx = rx[:-2] + "></row>"
    head = re.match(r"<row[^>]*>", rx).group(0)
    nh = re.sub(r' spans="[^"]*"', "", head)
    if row_attrs and "customHeight" not in nh: nh = nh[:-1] + " " + row_attrs + ">"
    rx = nh + rx[len(head):]
    cm = re.search(CELL_RE.format(ref=ref), rx, re.S)
    if cm:
        rx = rx.replace(cm.group(0), cell, 1)
    else:
        cells = [(col2n(split_ref(x.group(1))[0]), x.start()) for x in re.finditer(r'<c r="([A-Z]+\d+)"', rx)]
        pos = next((p for c, p in cells if c > col2n(col)), rx.rindex("</row>"))
        rx = rx[:pos] + cell + rx[pos:]
    return sheet.replace(rm.group(0), rx, 1)
def num(sheet, ref, v, base=None, font=None):
    s = xf(base if base is not None else get_style(sheet, ref), font if font is not None else F_AR_BLUE)
    return set_cell(sheet, ref, f"<v>{v}</v>", s)
def fml(sheet, ref, f, base=None, h=None):
    s = xf(base if base is not None else get_style(sheet, ref), F_AR_BLK, h=h)
    return set_cell(sheet, ref, f"<f>{escape(f)}</f>", s)
def txt(sheet, ref, text, base=None, font=None, h=None, wrap=None, row_attrs=None, **kw):
    s = xf(base if base is not None else get_style(sheet, ref), font if font is not None else F_KR_BLK, h=h, wrap=wrap, **kw)
    return set_cell(sheet, ref, inline(text, **kw.get("ikw", {})) if False else inline(text), s, t="inlineStr", row_attrs=row_attrs)

LOG = []  # (시트, 셀, 항목, 기존, 변경, 근거, 링크)
SEC = "https://www.sec.gov/Archives/edgar/data/1868941/"
L = {
    "4Q26": SEC + "000186894126000056/flncq4andfullfy26earningsp.htm",
    "3Q26": SEC + "000186894126000028/flncq3fy26earningspressrel.htm",
    "10K26": SEC + "000186894126000057/flnc-20260930.htm",
    "10Q3Q26": SEC + "000186894126000029/flnc-20260630.htm",
    "10Q3Q24": SEC + "000186894124000059/flnc-20240630.htm",
    "ID": SEC + "000110465926108270/tm2625477d1_ex99-1.htm",
    "3Q24": SEC + "000186894124000057/flncq3fy24earningspressrel.htm",
    "4Q24": SEC + "000186894124000066/flncq4andfullfy24earningsp.htm",
    "1Q24": SEC + "000186894124000012/flncq1fy24earningspressrel.htm",
    "2Q24": SEC + "000186894124000041/flncq2fy24earningspressrel.htm",
    "3Q23": SEC + "000186894123000057/flncq3fy23earningspressrel.htm",
    "4Q23": SEC + "000186894123000081/flncq4andfullfy23earningsp.htm",
    "1Q25": SEC + "000186894125000013/flncq1fy25earningspressrel.htm",
}

# ================================================================== 요약 (sheet1)
s1 = rd(P("xl/worksheets/sheet1.xml"))
def N(ref, v, old, item, src, link):
    global s1
    s1 = num(s1, ref, v); LOG.append(("요약", ref, item, old, v, src, link))
# 매출(부문)
N("W12", 22.571, "(빈칸)", "3Q26 Services and Digital 매출", "10-Q 3Q26: 서비스 20.121 + 디지털 2.450(소수 셋째 자리까지 입력해 합계를 공시값과 일치)", L["10Q3Q26"])
N("W13", 627.277, "(빈칸)", "3Q26 Energy Storage Solutions 매출", "10-Q 3Q26 매출 유형별 표", L["10Q3Q26"])
N("X12", 20.689, "(빈칸)", "4Q26 Services and Digital 매출", "10-K FY26 98.872 − 10-Q 9개월 누적 78.183", L["10K26"])
N("X13", 723.402, "(빈칸)", "4Q26 Energy Storage Solutions 매출", "10-K FY26 2,235.192 − 9개월 누적 1,511.790", L["10K26"])
# 조정 EBITDA
N("W16", -29.3, "(빈칸)", "3Q26 조정 EBITDA", "3Q26 실적발표문", L["3Q26"])
N("X16", -112.0, "(빈칸)", "4Q26 조정 EBITDA", "4Q26 실적발표문(FY26 −202.8)", L["4Q26"])
# 조정 매출총이익
N("I21", 13.1, "(빈칸)", "1Q23 조정 매출총이익", "1Q24 실적발표문 전년 동기 열(13,129천달러)", L["1Q24"])
N("J21", 32.2, "(빈칸)", "2Q23 조정 매출총이익", "2Q24 실적발표문 전년 동기 열(32,208천달러)", L["2Q24"])
N("K21", 23.6, "(빈칸)", "3Q23 조정 매출총이익", "3Q24 실적발표문 전년 동기 열(23,627천달러)", L["3Q24"])
N("L21", 77.9, "(빈칸)", "4Q23 조정 매출총이익", "4Q24 실적발표문 전년 동기 열(77,932천달러)", L["4Q24"])
N("W21", 38.6, "(빈칸)", "3Q26 조정 매출총이익", "3Q26 실적발표문(38,625천달러, 5.9%)", L["3Q26"])
N("X21", -27.6, "(빈칸)", "4Q26 조정 매출총이익", "4Q26 실적발표문(−27,563천달러, −3.7%)", L["4Q26"])
# 수주
N("K24", 565, "(빈칸)", "3Q23 수주", "3Q24 실적발표문: 전년 동기 약 5.65억달러", L["3Q24"])
N("L24", 737, "(빈칸)", "4Q23 수주", "4Q23 실적발표문: 7.37억달러", L["4Q23"])
N("Q24", 778.0, 777.9, "1Q25 수주", "1Q25 실적발표문: 778.0백만달러", L["1Q25"])
N("W24", 1440, "(빈칸)", "3Q26 수주", "3Q26 실적발표문: 14.4억달러 이상", L["3Q26"])
N("X24", 3500, "(빈칸)", "4Q26 수주", "4Q26 실적발표문: 35억달러(FY26 62억달러 이상)", L["4Q26"])
# 백로그
N("J25", 2800, "(빈칸)", "2Q23 백로그", "3Q23 실적발표문: 2023.3.31 약 28억달러", L["3Q23"])
N("K25", 2900, "(빈칸)", "3Q23 백로그", "3Q23 실적발표문: 약 29억달러", L["3Q23"])
N("L25", 2900, "(빈칸)", "4Q23 백로그", "4Q23 실적발표문: 29억달러", L["4Q23"])
N("W25", 6400, "(빈칸)", "3Q26 백로그", "3Q26 실적발표문: 약 64억달러", L["3Q26"])
N("X25", 8900, "(빈칸)", "4Q26 백로그", "4Q26 실적발표문: 약 89억달러", L["4Q26"])
# 파이프라인($)
N("L26", 13000, "(빈칸)", "4Q23 파이프라인", "4QFY23 컨콜: 130억달러", "")
N("O26", 20500, "(빈칸)", "3Q24 파이프라인(역산)", "4QFY24 컨콜: 전분기 말 대비 +5억달러 → 약 210억 (역산값)", "")
N("P26", 21000, "(빈칸)", "4Q24 파이프라인", "4QFY24 컨콜: 약 210억달러", "")
N("W26", 33100, "(빈칸)", "3Q26 파이프라인", "3QFY26 컨콜: 331억달러", "")
# 누적 Deployed(GWh)
N("K35", 6.1, "(빈칸)", "3Q23 누적 Deployed(GWh)", "3Q23 실적발표문 핵심지표", L["3Q23"])
N("L35", 7.2, "(빈칸)", "4Q23 누적 Deployed(GWh)", "4Q23 실적발표문 핵심지표", L["4Q23"])
N("W35", 19.3, "(빈칸)", "3Q26 누적 Deployed(GWh)", "3Q26 실적발표문 핵심지표", L["3Q26"])
N("X35", 20.8, "(빈칸)", "4Q26 누적 Deployed(GWh)", "4Q26 실적발표문 핵심지표", L["4Q26"])
# 손익 YoY/QoQ 텍스트(사용자 표기 방식)
for ref, t, old in [("W17", "적자전환", "수식 (W16/S16-1)*100"), ("X17", "적자전환", "수식 (X16/T16-1)*100"),
                    ("W18", "적자지속", "수식 (W16/V16-1)*100"), ("X18", "적자지속", "수식 (X16/W16-1)*100")]:
    s1 = txt(s1, ref, t, h="right"); LOG.append(("요약", ref, "조정 EBITDA 증감 표기", old, t, "손실 구간은 기존 표기 방식(적자전환·적자지속)으로 통일", ""))
# 연간 2026 열(AD)
s1 = set_cell(s1, "AD8", "<v>2026</v>", xf(get_style(s1, "AC8"), F_AR_BLK))
for ref, f, base in [("AD9", "IFERROR(AD12+AD13,\"n/a\")", "AC9"), ("AD10", "IFERROR((AD9/AC9-1)*100,\"n/a\")", "AC10"),
                     ("AD12", "IFERROR(SUM(U12:X12),\"n/a\")", "AC12"), ("AD13", "IFERROR(SUM(U13:X13),\"n/a\")", "AC13"),
                     ("AD14", "IFERROR((AD13/AC13-1)*100,\"n/a\")", "AC14"), ("AD16", "IFERROR(SUM(U16:X16),\"n/a\")", "AC16"),
                     ("AD19", "IFERROR(AD16/AD9*100,\"n/a\")", "AC19"), ("AD24", "IFERROR(SUM(U24:X24),\"n/a\")", "AC24"),
                     ("AD39", "IFERROR((AD13/AD9)*100,\"n/a\")", "AC39")]:
    s1 = fml(s1, ref, f, base=get_style(s1, base), h="right")
s1 = txt(s1, "AD17", "적자전환", base=get_style(s1, "AC17"), h="right")
s1 = num(s1, "AD25", 8900, base=get_style(s1, "AC25"))
s1 = num(s1, "AD35", 20.8, base=get_style(s1, "AC35"))
LOG.append(("요약", "AD8:AD39", "2026(FY26) 연간 열 추가", "(없음)", "합계 수식·백로그·Deployed", "FY26 실적 확정(10-K 2026.11.23 공시)", L["10K26"]))
# 조정 매출총이익 연간 합계·GPM
for c, rng in [("AA", "I21:L21"), ("AB", "M21:P21"), ("AC", "Q21:T21"), ("AD", "U21:X21")]:
    s1 = fml(s1, f"{c}21", f'IFERROR(SUM({rng}),"n/a")', base=get_style(s1, "AC21"), h="right")
    s1 = fml(s1, f"{c}22", f'IFERROR({c}21/{c}9,"n/a")', base=get_style(s1, "V22"), h="right")
LOG.append(("요약", "AA21:AD22", "연간 조정 매출총이익·GPM", "(빈칸)", "분기 합계 수식", "FY23 6.6%·FY24 12.9%·FY25 13.7%·FY26 3.8%로 회사 발표와 일치", ""))
# 가이던스(최종 수정치)
s1 = txt(s1, "AE9", "약 2,400", h="right"); s1 = num(s1, "AF9", 2400)
s1 = txt(s1, "AE16", "약 -200", h="right"); s1 = num(s1, "AF16", -200)
s1 = txt(s1, "AF17", "적자전환", base=get_style(s1, "AF17"), h="right")
s1 = txt(s1, "AG9", "최초 3,200~3,600 → 8/5 2,900~3,100 → 9/16 약 2,400 → 실적 2,334", base=0)
s1 = txt(s1, "AG16", "최초 40~60 → 8/5 −30~10 → 9/16 약 −200 → 실적 −202.8", base=0)
LOG.append(("요약", "AE9·AF9", "FY26 매출 가이던스", "3200-3600 / 3400", "약 2,400", "9/16 가이던스 재하향 발표문", L["ID"]))
LOG.append(("요약", "AE16·AF16", "FY26 조정 EBITDA 가이던스", "40-60 / 50", "약 −200", "9/16 가이던스 재하향 발표문", L["ID"]))
# 메모 셀
s1 = txt(s1, "B3", "파이프라인 → 수주(Order intake) → 백로그 → 매출 인식(출하·소유권 이전) → Deployed(실질 완공)", base=0)
LOG.append(("요약", "B3", "사업 흐름 설명", "Orders → 파이프라인 진행 → 설치(Deployed) → 매출 인식",
            "파이프라인 → 수주 → 백로그 → 매출 인식 → Deployed",
            "3QFY26 컨콜: 매출은 출하·소유권 이전 시 인식, Deployed는 실질 완공 기준이라 매출보다 늦게 잡힘", ""))
s1 = txt(s1, "B7", "※ 2026.11.24 검증: 파란 글씨 = SEC 실적발표문·10-Q·10-K·컨콜 원문으로 입력·수정한 값. 근거는 「검증 내역」 탭", base=0)
wr(P("xl/worksheets/sheet1.xml"), s1)

# ================================================================== 매출Breakdown (sheet3)
s3 = rd(P("xl/worksheets/sheet3.xml"))
s3 = num(s3, "E9", 296)
LOG.append(("매출Breakdown", "E9", "4Q24 EMEA 매출", 26, 296, "10-K FY24 EMEA 526.3 − 10-Q 3Q24 9개월 누적 230.0 → 합계가 4Q24 매출 1,228.1과 일치", L["10Q3Q24"]))
for col, hdr, vals in [("G", "3Q26", (322.4, 250.1, 77.3)), ("H", "4Q26", (494.6, 95.2, 154.3))]:
    s3 = txt(s3, f"{col}4", hdr, base=get_style(s3, "F4"), h="center")
    for (r, v) in zip((5, 7, 9), vals):
        s3 = num(s3, f"{col}{r}", v, base=get_style(s3, f"F{r}"))
    for r in (6, 8, 10):
        s3 = fml(s3, f"{col}{r}", f'IFERROR({col}{r-1}/{col}$11,"n/a")', base=get_style(s3, f"F{r}"), h="right")
    s3 = fml(s3, f"{col}11", f'IFERROR({col}5+{col}7+{col}9,"n/a")', base=get_style(s3, "F11"), h="right")
LOG.append(("매출Breakdown", "G4:H11", "3Q26·4Q26 지역별 매출", "(없음)", "Americas·APAC·EMEA", "10-Q 3Q26 지역별 표, 4Q26 = 10-K FY26 − 9개월 누적", L["10K26"]))
s3 = txt(s3, "B13", "※ E9 수정(26→296), G·H열 추가: SEC 10-Q·10-K 지역별 매출(4분기 = 연간 − 9개월 누적), 2026.11.24 확인", base=0)
s3 = re.sub(r'<dimension ref="[^"]*"/>', '<dimension ref="B2:H13"/>', s3)
wr(P("xl/worksheets/sheet3.xml"), s3)

# ================================================================== 어닝콜 주요사항 (sheet2)
s2 = rd(P("xl/worksheets/sheet2.xml"))
C_FIRST, C_MID, C_LAST = 146, 147, 148
B_FIRST, B_MID, B_LAST = 158, 159, 160
def ctext(ref, text, kind):
    global s2
    base = {"f": C_FIRST, "m": C_MID, "l": C_LAST}[kind]
    s2 = txt(s2, ref, text, base=base, wrap=True, row_attrs='ht="33" customHeight="1"')
s2 = txt(s2, "C6", "AESC 테네시 공장 2라인을 530Ah 셀로 업그레이드하면서 잠재적 3라인 독점권도 확보", base=get_style(s2, "C6"))
LOG.append(("어닝콜 주요사항", "C6", "4Q24 AESC 독점권", "독점권 추가 확보 위한 협상 진행 중", "잠재적 3라인 독점권 확보",
            "4QFY24 컨콜: 'it secures our exclusivity for a potential third line'", ""))
s2 = txt(s2, "C12", "FY26 매출 44.2억달러: 1Q25 실적발표문에 없는 수치(FY25 가이던스 중간값 34억×1.3으로 보임), 컨콜 원문 확인 필요", base=get_style(s2, "C12"))
LOG.append(("어닝콜 주요사항", "C12", "1Q25 'FY26 매출 가이던스 44.2억'", "2026년 매출 가이던스: 44.2억달러", "공식 가이던스로 확인 안 됨",
            "1Q25 실적발표문 가이던스는 FY25(31~37억)만 있음", L["1Q25"]))
s2 = txt(s2, "C19", "FY26 조정 GPM 가이던스 11~13%(FY25 13.7% 대비 최대 -2.7%p): 신제품 Gridstack Pro(FY26 매출의 70%) 출시 초기 원가 부담", base=get_style(s2, "C19"), wrap=True)
LOG.append(("어닝콜 주요사항", "C19", "4Q25 GPM 하락 이유", "Gridstack Pro 출시 관련 마케팅·영업 비용 증가", "Gridstack Pro 출시 초기 원가 부담",
            "4QFY25 컨콜: 'higher costs associated with the rollout of our Gridstack Pro product'. 영업·R&D 비용은 판관비(EBITDA)에 해당", ""))
blocks = [
    ("1Q26", [
        "매출 4.75억달러, 조정 GPM 5.6%(해외 2개 프로젝트 추가원가 약 0.2억달러 + 1분기 고정비 부담), 조정 EBITDA -0.52억달러",
        "백로그 55억달러, 수주 7.5억달러(미국 5억+). 데이터센터 36GWh·장주기(LDES) 34GWh 논의, 지난 분기 60GWh는 TAM이었다고 정정",
        "FY26 가이던스 유지(매출 32~36억, 조정 EBITDA 0.4~0.6억, ARR 1.8억달러). AESC와 공급계약(MSA) 유지, 두 번째 미국산 셀 공급처 확보"]),
    ("2Q26", [
        "매출 4.65억달러, 조정 GPM 11.1%, 조정 EBITDA -0.09억달러. 약 0.8억달러가 3분기로 이연(베트남 통관·스페인 하역장비 부족 각 절반)",
        "하이퍼스케일러 2곳과 MSA 체결, 데이터센터 파이프라인 약 12GWh(+30%), 리드는 그 3배. CATL·BYD 직접 진출에도 경쟁강도 변화 없다는 입장",
        "AESC 테네시 공장 지분 과반 매각(2026.3.31)으로 PFE 문제 해소, 새 소유주와 공급계약. 매출은 하반기 약 70%(3분기 30%·4분기 70%) 예상"]),
    ("3Q26", [
        "매출 6.50억달러(기대 대비 -0.9억), 조정 GPM 5.9%, 조정 EBITDA -0.29억달러. 휴스턴 인클로저 공장(연 15GWh) 지연·중국 공장 품질 재작업",
        "수주 14.4억달러(첫 데이터센터 개발사 3억 포함), 7월 하이퍼스케일러 5.5억 낙찰. 백로그 64억(FY27 전환 22억), 파이프라인 331억달러",
        "FY26 가이던스 하향: 매출 29~31억, 조정 EBITDA -0.3~0.1억달러(약 4억달러 매출 FY27로 이연). ARR 1.8억 유지"]),
    ("9/16 수정", [
        "FY26 가이던스 재하향: 매출 약 24억, 조정 EBITDA 약 -2억달러. 휴스턴 자동용접 부진(8월 하루 1대 미만 → 9월 초 3대, 목표 11대)",
        "감소분 약 6억 중 미국 생산지연 약 4.5억·지연배상금 약 0.65억·물류 약 0.85억달러. 신임 COO(Bernerd Da Santos) 선임",
        "FY27 백로그 29억(미국 생산 필요 12억). 추가 자본 없이 영업현금흐름 중립~흑자 목표, 미국 생산이 필요한 FY27 신규 수주는 선별"]),
    ("4Q26", [
        "FY26 매출 23.3억(4Q 7.4억), 조정 GPM 3.8%(4Q -3.7%), 조정 EBITDA -2.03억(4Q -1.12억). ARR 1.71억달러(목표 1.8억 미달)",
        "4Q 수주 35억(FY26 62억+) 사상 최대, 백로그 89억달러. 마진 악화는 납기지연 배상금(LD)과 신제품 초기 원가 초과 영향",
        "10/30 CEO(Julian Nebreda)·CFO(Ahmed Pasha) 퇴임, Axel Meier 임시 CEO·Ricardo Roizen 임시 CFO. FY27 가이던스는 실적발표문에 없음(11/24 컨콜 확인 필요)"]),
]
r = 21; merges = []
for label, lines in blocks:
    r0 = r
    for i, line in enumerate(lines):
        kind = "f" if i == 0 else ("l" if i == len(lines) - 1 else "m")
        bstyle = {"f": B_FIRST, "m": B_MID, "l": B_LAST}[kind]
        s2 = txt(s2, f"B{r}", label if i == 0 else "", base=bstyle, h="center") if i == 0 else set_cell(s2, f"B{r}", "", xf(bstyle, F_KR_BLK, h="center"))
        ctext(f"C{r}", line, kind)
        r += 1
    merges.append(f"B{r0}:B{r-1}")
LOG.append(("어닝콜 주요사항", "B21:C35", "1Q26~4Q26 주요사항", "1Q26 제목만 있음", "5개 구간 15행 추가", "1Q·2Q·3QFY26 컨콜, 9/16 투자자 업데이트, 4Q26 실적발표문", L["4Q26"]))
mc = re.search(r'<mergeCells count="(\d+)">(.*?)</mergeCells>', s2, re.S)
newm = mc.group(2) + "".join(f'<mergeCell ref="{m}"/>' for m in merges)
s2 = s2.replace(mc.group(0), f'<mergeCells count="{int(mc.group(1)) + len(merges)}">{newm}</mergeCells>')
s2 = re.sub(r'<dimension ref="[^"]*"/>', f'<dimension ref="B2:F{r-1}"/>', s2)
wr(P("xl/worksheets/sheet2.xml"), s2)

# ================================================================== 검증 내역 (new sheet5)
H_TITLE = xf(0, F_KR_TITLE)
H_HDR = xf(0, F_KR_HDR, h="center", wrap=True, fill=FILL_TEAL, border=B_THIN)
C_TXT = xf(0, F_KR_BLK, wrap=True, border=B_THIN)
C_NUM = xf(0, F_AR_BLUE, h="right", border=B_THIN)
C_LNK = xf(0, F_AR_LINK, border=B_THIN)
rows = ['<row r="2"><c r="B2" s="%d" t="inlineStr">%s</c></row>' % (H_TITLE, inline("엑셀 검증 내역"))]
hdr = ["시트", "셀", "항목", "기존", "변경", "근거", "링크"]
rows.append('<row r="3">' + "".join(f'<c r="{chr(66+i)}3" s="{H_HDR}" t="inlineStr">{inline(h)}</c>' for i, h in enumerate(hdr)) + "</row>")
for i, (sh, ref, item, old, new, src, link) in enumerate(LOG):
    rr = 4 + i
    cells = []
    for j, v in enumerate([sh, ref, item, old, new, src]):
        c = chr(66 + j)
        if isinstance(v, (int, float)):
            cells.append(f'<c r="{c}{rr}" s="{C_NUM}"><v>{v}</v></c>')
        else:
            cells.append(f'<c r="{c}{rr}" s="{C_TXT}" t="inlineStr">{inline(str(v))}</c>')
    if link:
        f = escape(f'IFERROR(HYPERLINK("{link}","SEC 원문"),"n/a")')
        cells.append(f'<c r="H{rr}" s="{C_LNK}" t="str"><f>{f}</f><v>SEC 원문</v></c>')
    else:
        cells.append(f'<c r="H{rr}" s="{C_TXT}" t="inlineStr">{inline("컨콜 원문(PDF)")}</c>')
    rows.append(f'<row r="{rr}">' + "".join(cells) + "</row>")
last = 3 + len(LOG)
sheet5 = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          f'<dimension ref="B2:H{last}"/><sheetViews><sheetView showGridLines="0" workbookViewId="0"/></sheetViews>'
          '<sheetFormatPr defaultRowHeight="16.5"/>'
          '<cols><col min="1" max="1" width="2" customWidth="1"/><col min="2" max="2" width="14" customWidth="1"/>'
          '<col min="3" max="3" width="11" customWidth="1"/><col min="4" max="4" width="26" customWidth="1"/>'
          '<col min="5" max="5" width="24" customWidth="1"/><col min="6" max="6" width="24" customWidth="1"/>'
          '<col min="7" max="7" width="60" customWidth="1"/><col min="8" max="8" width="14" customWidth="1"/></cols>'
          '<sheetData>' + "".join(rows) + '</sheetData>'
          '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>')
wr(P("xl/worksheets/sheet5.xml"), sheet5)
wb = rd(P("xl/workbook.xml"))
wb = wb.replace('<sheet name="Sheet2" sheetId="4" r:id="rId4"/>', '<sheet name="Sheet2" sheetId="4" r:id="rId4"/><sheet name="검증 내역" sheetId="5" r:id="rId9"/>')
wb = re.sub(r'<calcPr[^>]*/>', '<calcPr calcId="162913" fullCalcOnLoad="1"/>', wb)
wr(P("xl/workbook.xml"), wb)
rels = rd(P("xl/_rels/workbook.xml.rels"))
rels = re.sub(r'<Relationship Id="rId8"[^>]*calcChain[^>]*/>', "", rels)
rels = rels.replace("</Relationships>", '<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet5.xml"/></Relationships>')
wr(P("xl/_rels/workbook.xml.rels"), rels)
ct = rd(P("[Content_Types].xml"))
ct = re.sub(r'<Override PartName="/xl/calcChain.xml"[^>]*/>', "", ct)
ct = ct.replace('<Override PartName="/xl/worksheets/sheet4.xml"', '<Override PartName="/xl/worksheets/sheet5.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet4.xml"')
wr(P("[Content_Types].xml"), ct)
if os.path.exists(P("xl/calcChain.xml")): os.remove(P("xl/calcChain.xml"))
# styles 저장
cx = '<cellXfs count="%d">%s</cellXfs>' % (len(XF), "".join(XF))
styles = re.sub(r'<cellXfs count="\d+">.*?</cellXfs>', lambda m: cx, styles, flags=re.S)
wr(P("xl/styles.xml"), styles)
# zip
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    order = ["[Content_Types].xml"]
    for root, _, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f); arc = os.path.relpath(full, SRC).replace(os.sep, "/")
            if arc not in order: order.append(arc)
    for arc in order:
        z.write(os.path.join(SRC, arc), arc)
print("changes", len(LOG), "xfs", len(XF))
