# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, sys.argv[2])
from common_v2 import *  # noqa
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from data_v2 import SRC, CODE, SRCD, VC, STREAM_BAND, THEME, M

OUT = sys.argv[1]
YEARS = [2025, 2026, 2027, 2028, 2029, 2030]
Y7 = YEARS + [2031]
GREY = "808080"
wb = Workbook()
ws1 = wb.active
ws1.title = "구조표"
ws2 = wb.create_sheet("밸류체인")
ws3 = wb.create_sheet("시장규모")
ws4 = wb.create_sheet("시장규모 요약")
ws5 = wb.create_sheet("DC capex")
ws6 = wb.create_sheet("출처")
ws7 = wb.create_sheet("자체조사")


def title(ws, text):
    c = ws.cell(2, 2, text)
    c.font = Font(name=EN, size=12, bold=True)
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 17.25


def band(ws, r, text, c1, c2):
    for c in range(c1, c2 + 1):
        put(ws, r, c, None, fill=BAND)
    put(ws, r, c1, text, bold=True, fill=BAND)


def merge_runs(ws, col, r0, r1, keyf):
    """keyf(r) -> 값; 같은 값이 이어지면 세로 병합(가운데 정렬)."""
    r = r0
    while r <= r1:
        k = keyf(r)
        s = r
        while r + 1 <= r1 and keyf(r + 1) == k and k is not None:
            r += 1
        if k is not None and r > s:
            ws.merge_cells(start_row=s, start_column=col, end_row=r, end_column=col)
        if k is not None:
            ws.cell(s, col).alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        r += 1


import re as _re
_KEYS = sorted(CODE, key=len, reverse=True)


def codify(text):
    for kk in _KEYS:
        text = _re.sub(rf"(?<![A-Za-z_]){_re.escape(kk)}(?![A-Za-z_0-9])", CODE[kk], text)
    return text


def cite(k):
    return f"{CODE[k]} {SRCD[k][0]}({SRCD[k][2]})" if k in CODE else "-"


# ===================================================================== 시장규모
title(ws3, "통신용 광모듈 시장규모")
H3 = ["No", "Stream", "사업", "제품", "품목·지표", "정의(범위)", "단위", "2025", "2026", "2027", "2028", "2029", "2030",
      "2031(참고)", "CAGR(25→30)", "적용 성장률", "원출처(조사기관)", "출처", "위치", "링크", "확인 방법", "신뢰도", "비고"]
header(ws3, 3, H3)
YC = {y: 9 + i for i, y in enumerate(Y7)}  # I..O
row_of, NO = {}, {}
r = 4
cur = None
cnt = {}
PFX = {"Upstream": "U", "Midstream": "M", "Downstream": "D"}
blocks = []
for d in M:
    if d["s"] != cur:
        if cur is not None:
            blocks.append((b0, r - 1))
        cur = d["s"]
        band(ws3, r, STREAM_BAND[cur], 2, 1 + len(H3))
        r += 1
        b0 = r
    cnt[cur] = cnt.get(cur, 0) + 1
    no = f"{PFX[cur]}-{cnt[cur]:02d}"
    NO[d["key"]] = no
    row_of[d["key"]] = r
    vals = [v for v in d["src"].values()]
    mx = max(vals) if vals else 0
    fm = "0.0%" if d["pct"] else ("#,##0" if mx >= 100 else ("#,##0.0" if mx >= 10 else "#,##0.00"))
    if not vals and d["special"]:
        fm = "#,##0.0"
    put(ws3, r, 2, no, h="center")
    put(ws3, r, 3, d["s"], h="center")
    put(ws3, r, 4, d["b"], h="center", wrap=True)
    put(ws3, r, 5, d["p"], h="center", wrap=True)
    put(ws3, r, 6, d["item"], bold=not d["item"].startswith(" └"))
    put(ws3, r, 7, d["scope"] or "-", wrap=True)
    put(ws3, r, 8, d["unit"], h="center")
    g = d["g"]
    if g is None:
        put(ws3, r, 17, "n/a")
    elif isinstance(g, str):
        put(ws3, r, 17, f"=IFERROR({g[1:]},\"n/a\")", fmt="0.0%", h="right")
    else:
        put(ws3, r, 17, g, color=BLUE, fmt="0.0%", h="right")
    P = f"$Q{r}"
    src = d["src"]
    sy = sorted(set(src) | set(d["special"]))
    modes = {}
    for y in Y7:
        col = YC[y]
        beyond = d["hz"] is not None and y > d["hz"]
        if y in d["special"]:
            f = d["special"][y].format(**{k: v for k, v in row_of.items()})
            put(ws3, r, col, f"=IFERROR({f[1:]},\"n/a\")", fmt=fm, h="right", italic=beyond)
            modes[y] = "calc"
            continue
        if y in src:
            put(ws3, r, col, src[y], color=BLUE, fmt=fm, h="right")
            modes[y] = "src"
            continue
        if y == 2031:
            put(ws3, r, col, "n/a")
            continue
        a = max([s for s in sy if s < y], default=None)
        b = min([s for s in sy if s > y], default=None)
        if a is not None and b is not None:
            A, B = f"{CL(YC[a])}{r}", f"{CL(YC[b])}{r}"
            put(ws3, r, col, f"=IFERROR({A}*({B}/{A})^(({y}-{a})/({b}-{a})),\"n/a\")", fmt=fm, h="right")
            modes[y] = "interp"
        elif g is not None and a is None and b is not None:
            put(ws3, r, col, f"=IFERROR({CL(col + 1)}{r}/(1+{P}),\"n/a\")", fmt=fm, h="right")
            modes[y] = "back"
        elif g is not None and y > 2025 and (a is not None or modes.get(y - 1) in ("calc", "fwd")):
            put(ws3, r, col, f"=IFERROR({CL(col - 1)}{r}*(1+{P}),\"n/a\")", fmt=fm, h="right", italic=beyond)
            modes[y] = "fwd"
        else:
            put(ws3, r, col, "n/a")
            modes[y] = "na"
    put(ws3, r, 16, f"=IFERROR((N{r}/I{r})^(1/5)-1,\"n/a\")", fmt="0.0%", h="right")
    put(ws3, r, 18, d["orig"], wrap=True)
    k = d["cite"]
    put(ws3, r, 19, cite(k), wrap=True)
    put(ws3, r, 20, d["loc"], h="center")
    if k in SRCD:
        put(ws3, r, 21, SRCD[k][4], color=BLUE, link=SRCD[k][4], underline="single")
        put(ws3, r, 22, SRCD[k][5], wrap=True)
    else:
        put(ws3, r, 21, "-")
        put(ws3, r, 22, "-")
    put(ws3, r, 23, d["grade"], h="center")
    put(ws3, r, 24, codify(d["note"] or "-"), wrap=True)
    r += 1
blocks.append((b0, r - 1))
for (s0, s1) in blocks:
    sn = {rr: (ws3.cell(rr, 3).value, ws3.cell(rr, 4).value, ws3.cell(rr, 5).value) for rr in range(s0, s1 + 1)}
    merge_runs(ws3, 3, s0, s1, lambda rr: sn[rr][0])
    merge_runs(ws3, 4, s0, s1, lambda rr: sn[rr][:2])
    merge_runs(ws3, 5, s0, s1, lambda rr: sn[rr])
# Check (레이저 칩 원문 합계)
r += 1
put(ws3, r, 6, "Check: 레이저 칩 전체 − (CW + EML + 기타)")
for y in YEARS:
    c = CL(YC[y])
    put(ws3, r, YC[y], f"=IFERROR(ROUND({c}{row_of['laser']}-({c}{row_of['cw']}+{c}{row_of['eml']}+{c}{row_of['oth']}),2),\"n/a\")",
        fmt='#,##0.0;(#,##0.0);"-"', h="right")
put(ws3, r, 24, "원문 표 반올림 차이(±0.1)")
for kc, w in {"A": 2, "B": 6, "C": 11, "D": 18, "E": 18, "F": 34, "G": 24, "H": 9, "I": 9, "J": 9, "K": 9, "L": 9, "M": 9,
              "N": 9, "O": 10, "P": 11, "Q": 10, "R": 22, "S": 36, "T": 10, "U": 40, "V": 22, "W": 7, "X": 62}.items():
    ws3.column_dimensions[kc].width = w


def ref(key, y):
    return f"'시장규모'!{CL(YC[y])}{row_of[key]}"


# ===================================================================== 구조표
title(ws1, "통신용 광모듈 밸류체인 구조")
header(ws1, 3, ["Stream", "사업", "제품", "품목", "품목 설명", "적용 애플리케이션", "비고"])
r = 4
cur = None
blocks = []
for (st, b, p, it, desc, use, mp, ov, kr, sh, basis) in VC:
    if st != cur:
        if cur is not None:
            blocks.append((b0, r - 1))
        cur = st
        band(ws1, r, STREAM_BAND[st], 2, 8)
        r += 1
        b0 = r
    put(ws1, r, 2, st, h="center")
    put(ws1, r, 3, b, bold=True, h="center")
    put(ws1, r, 4, p, h="center")
    put(ws1, r, 5, it, bold=True)
    put(ws1, r, 6, desc, wrap=True)
    put(ws1, r, 7, use, wrap=True)
    put(ws1, r, 8, mp, h="center")
    r += 1
blocks.append((b0, r - 1))
for (s0, s1) in blocks:
    sn = {rr: (ws1.cell(rr, 2).value, ws1.cell(rr, 3).value, ws1.cell(rr, 4).value) for rr in range(s0, s1 + 1)}
    merge_runs(ws1, 2, s0, s1, lambda rr: sn[rr][0])
    merge_runs(ws1, 3, s0, s1, lambda rr: sn[rr][:2])
    merge_runs(ws1, 4, s0, s1, lambda rr: sn[rr])
for kc, w in {"A": 2.0, "B": 12.0, "C": 22.875, "D": 24.125, "E": 34.5, "F": 58.125, "G": 42.5, "H": 11.875}.items():
    ws1.column_dimensions[kc].width = w
ws1.sheet_view.zoomScale = 85

# ===================================================================== 밸류체인
NOV, NKR = 10, 6
title(ws2, "통신용 광모듈 밸류체인 기업")
H2 = ["Stream", "사업", "제품", "품목", "구분"] + [f"해외{chr(0x2460 + i)}" for i in range(NOV)] + [f"국내{chr(0x2460 + i)}" for i in range(NKR)] + ["순서·점유율 근거"]
header(ws2, 3, H2)
LAST2 = 1 + len(H2)
MK = {
    "Upstream": [("광칩 + 광통신 IC 칩셋", ["chips", "chipset"], "광칩 {chips} + IC 칩셋 {chipset}(LightCounting). 수동부품·기판·광섬유는 금액 자료 없어 제외")],
    "Midstream": [("광트랜시버 (Yole)", ["tx_yole"], "{tx_yole}. 포토닉스 패키징({pkg})은 광트랜시버와 중복이라 제외"),
                  ("광트랜시버 (LightCounting)", ["tx_lc"], "{tx_lc}. 2026.10 이더넷 성장률 상향 전 기준")],
    "Downstream": [("광전송 + PON + RAN 장비", ["ot", "pon", "ran"], "{ot} + {pon} + {ran}. AI 백엔드 스위치({aisw})는 연도별 값 없어 제외"),
                   ("데이터센터 Capex (Dell'Oro)", ["capex"], "{capex}. 장비 합계와 별개인 수요 동인")],
}
r = 4
cur = None
for (st, b, p, it, desc, use, mp, ov, kr, sh, basis) in VC:
    if st != cur:
        if cur is not None:
            r += 1
        cur = st
        band(ws2, r, STREAM_BAND[st], 2, LAST2)
        r += 1
        # 시장규모 미니 표
        mh = ["Stream", "시장규모 지표", "구성", "", "단위"] + [str(y) for y in YEARS] + ["CAGR(25→30)"]
        for i, lab in enumerate(mh):
            put(ws2, r, 2 + i, lab, bold=True, fill=SUB, h="center")
        ws2.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
        r += 1
        lines = []
        for (lab, keys, comp) in MK[st]:
            put(ws2, r, 2, st, h="center")
            put(ws2, r, 3, lab, bold=True, wrap=True)
            put(ws2, r, 4, comp.format(**NO), wrap=True)
            put(ws2, r, 5, None)
            ws2.merge_cells(start_row=r, start_column=4, end_row=r, end_column=5)
            put(ws2, r, 6, "USD bn", h="center")
            for i, y in enumerate(YEARS):
                expr = "+".join(ref(k, y) for k in keys)
                put(ws2, r, 7 + i, f"=IFERROR({expr},\"n/a\")", fmt="#,##0.0", h="right")
            put(ws2, r, 13, f"=IFERROR((L{r}/G{r})^(1/5)-1,\"n/a\")", fmt="0.0%", h="right")
            lines.append((r, keys, lab))
            r += 1
        for (lr, keys, lab) in lines:
            put(ws2, r, 3, f"Check: {lab}")
            for i, y in enumerate(YEARS):
                expr = "+".join(ref(k, y) for k in keys)
                put(ws2, r, 7 + i, f"=IFERROR(ROUND({CL(7 + i)}{lr}-({expr}),6),\"n/a\")", fmt='#,##0;(#,##0);"-"', h="right")
            r += 1
        r += 1
        s_start = r
    r_item = r
    put(ws2, r, 2, st, h="center")
    put(ws2, r, 3, b, bold=True, h="center")
    put(ws2, r, 4, p, h="center")
    put(ws2, r, 5, it, bold=True, wrap=True)
    put(ws2, r, 6, "기업", h="center")
    for i in range(NOV):
        put(ws2, r, 7 + i, ov[i] if i < len(ov) else None, wrap=True)
    for i in range(NKR):
        put(ws2, r, 7 + NOV + i, kr[i] if i < len(kr) else None, wrap=True)
    put(ws2, r, LAST2, codify(basis), wrap=True)
    if sh:
        r += 1
        put(ws2, r, 2, st, h="center")
        put(ws2, r, 3, b, bold=True, h="center")
        put(ws2, r, 4, p, h="center")
        put(ws2, r, 5, it, bold=True)
        put(ws2, r, 6, "점유율", h="center")
        for i, v in enumerate(sh["ov"]):
            if isinstance(v, str) and v.startswith("="):
                put(ws2, r, 7 + i, f"=IFERROR({v[1:]},\"n/a\")", fmt="0.0%", h="center")
            elif v == "n/a":
                put(ws2, r, 7 + i, "n/a")
            else:
                put(ws2, r, 7 + i, v, color=BLUE, h="center")
        for i in range(NOV - len(sh["ov"])):
            put(ws2, r, 7 + len(sh["ov"]) + i, None)
        for i in range(NKR):
            put(ws2, r, 7 + NOV + i, None)
        put(ws2, r, LAST2, None)
        ws2.merge_cells(start_row=r_item, start_column=5, end_row=r, end_column=5)
        ws2.merge_cells(start_row=r_item, start_column=LAST2, end_row=r, end_column=LAST2)
        ws2.cell(r_item, 5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    r += 1
    # 블록 끝 처리: 다음 행이 다른 stream이면 병합
    nxt = VC.index((st, b, p, it, desc, use, mp, ov, kr, sh, basis)) + 1
    if nxt >= len(VC) or VC[nxt][0] != st:
        sn = {rr: (ws2.cell(rr, 2).value, ws2.cell(rr, 3).value, ws2.cell(rr, 4).value) for rr in range(s_start, r)}
        merge_runs(ws2, 2, s_start, r - 1, lambda rr: sn[rr][0])
        merge_runs(ws2, 3, s_start, r - 1, lambda rr: sn[rr][:2])
        merge_runs(ws2, 4, s_start, r - 1, lambda rr: sn[rr])
# 테마표
r += 2
band(ws2, r, "국내 투자 테마별 관련 기업", 2, 6)
r += 1
header(ws2, r, ["테마", "기업", "밸류체인 위치", "역할", "근거"])
r += 1
t0 = r
for (t, co, pos, role) in THEME:
    put(ws2, r, 2, t, bold=True, h="center", wrap=True)
    put(ws2, r, 3, co, bold=True)
    put(ws2, r, 4, pos, wrap=True)
    put(ws2, r, 5, role, wrap=True)
    basis = {"성호전자": f"{CODE['im']} 기업 리포트"}.get(co, f"{CODE['ds']} 기업 분석" if co in ("RF머트리얼즈", "대한광통신", "오이솔루션") else "회사 사업 개요(사용자 제공 테마)")
    put(ws2, r, 6, basis, wrap=True)
    r += 1
merge_runs(ws2, 2, t0, r - 1, lambda rr: ws2.cell(rr, 2).value)
for kc, w in {"A": 2, "B": 12, "C": 22, "D": 22, "E": 30, "F": 12}.items():
    ws2.column_dimensions[kc].width = w
for i in range(NOV + NKR):
    ws2.column_dimensions[CL(7 + i)].width = 22
ws2.column_dimensions[CL(LAST2)].width = 48

# ===================================================================== 시장규모 요약
title(ws4, "데이터센터향 광통신 시장규모 요약 (USD bn)")
H4 = ["구분", "제품군", "산식·기준", "2025", "2026", "2027", "2028", "2029", "2030", "CAGR(25→30)", "근거·출처"]
header(ws4, 3, H4)
YC4 = {y: 5 + i for i, y in enumerate(YEARS)}  # E..J
r = 4
# 가정 블록 위치를 먼저 확정(하단) → 행 번호를 미리 계산
rows4 = {}


def line(r, kind, name, how, formulas, src_text, pct=False, bold=False):
    put(ws4, r, 2, kind, h="center", wrap=True)
    put(ws4, r, 3, name, bold=bold, wrap=True)
    put(ws4, r, 4, how, wrap=True)
    for y in YEARS:
        f = formulas(y)
        if f is None:
            put(ws4, r, YC4[y], "n/a")
        else:
            put(ws4, r, YC4[y], f"=IFERROR({f},\"n/a\")", fmt="0.0%" if pct else "#,##0.0", h="right", bold=bold)
    if pct:
        put(ws4, r, 11, None)
    else:
        put(ws4, r, 11, f"=IFERROR((J{r}/E{r})^(1/5)-1,\"n/a\")", fmt="0.0%", h="right")
    put(ws4, r, 12, src_text, wrap=True)


# 가정 셀 위치(하단 ④): 행 번호 사전 지정
A_BASE = 40
AS = {"s31": A_BASE + 1, "dc24": A_BASE + 2, "all24": A_BASE + 3, "dc30": A_BASE + 4, "all30": A_BASE + 5}
band(ws4, r, "① 제품군별 데이터센터향 시장 (가치사슬 단계별, 합산 불가)", 2, 12)
r += 1
rows4["shA"] = r
line(r, "비중", "데이터센터 비중(트랜시버·칩셋·패키징)", "2025년 = 이더넷 ÷ 광트랜시버 전체(LightCounting), 2031년 가정까지 선형",
     lambda y: f"{ref('eth', 2025)}/{ref('tx_lc', 2025)}+({'$E$' + str(AS['s31'])}-{ref('eth', 2025)}/{ref('tx_lc', 2025)})*({y}-2025)/6",
     f"{CODE['lc_mar']}, 2031년 가정은 ④", pct=True)
r += 1
rows4["shB"] = r
line(r, "비중", "데이터센터 비중(광칩)", "2024·2030년 데이터센터 레이저칩 비중(④) 사이 선형",
     lambda y: f"$E${AS['dc24']}/$E${AS['all24']}+($E${AS['dc30']}/$E${AS['all30']}-$E${AS['dc24']}/$E${AS['all24']})*({y}-2024)/6",
     f"{CODE['dx']} p.8", pct=True)
r += 1
rows4["tx"] = r
line(r, "제품군", "광트랜시버", "Yole 광트랜시버 전체 × 데이터센터 비중",
     lambda y: f"{ref('tx_yole', y)}*{CL(YC4[y])}${rows4['shA']}", f"{NO['tx_yole']} ({CODE['yole_tx']})", bold=True)
r += 1
rows4["chip"] = r
line(r, "제품군", "광칩", "LightCounting 광칩 전체 × 데이터센터 비중(광칩)",
     lambda y: f"{ref('chips', y)}*{CL(YC4[y])}${rows4['shB']}", f"{NO['chips']} ({CODE['lc_chips']})", bold=True)
r += 1
rows4["ic"] = r
line(r, "제품군", "광통신 칩셋(전기 IC)", "LightCounting IC 칩셋 × 데이터센터 비중",
     lambda y: f"{ref('chipset', y)}*{CL(YC4[y])}${rows4['shA']}", f"{NO['chipset']} ({CODE['lc_chipset']})", bold=True)
r += 1
rows4["pkg"] = r
line(r, "제품군", "광 패키징", "Yole 포토닉스 패키징 × 데이터센터 비중",
     lambda y: f"{ref('pkg', y)}*{CL(YC4[y])}${rows4['shA']}", f"{NO['pkg']} ({CODE['yole_pkg']})", bold=True)
r += 1
line(r, "참고", "이더넷 광트랜시버(실측 성장률)", "LightCounting 원값(2028년 이후 미공개)",
     lambda y: ref('eth', y), f"{NO['eth']} ({CODE['lc_eth']})")
r += 1
line(r, "참고", "데이터센터 인터커넥트 TAM", "Marvell 원값(DSP·TIA·드라이버·AEC)",
     lambda y: ref('mrvl', y), f"{NO['mrvl']} ({CODE['mrvl']})")
r += 1
put(ws4, r, 3, "광칩·칩셋·패키징은 광트랜시버 원가 안에 들어가는 부품 단계라 ①끼리 더하지 않음", wrap=True, border=False)
ws4.merge_cells(start_row=r, start_column=3, end_row=r, end_column=12)
r += 2
band(ws4, r, "② 데이터센터 광통신 투자 대상 (구매 단위, 중복 제거 후 합산)", 2, 12)
r += 1
rows4["a"] = r
line(r, "a", "광 인터커넥트(트랜시버·AOC·CPO)", "① 광트랜시버", lambda y: f"{CL(YC4[y])}{rows4['tx']}", "①")
r += 1
rows4["b"] = r
line(r, "b", "DCI 광전송(IPoDWDM)", "Dell'Oro IPoDWDM(데이터센터 간 연결)", lambda y: ref('ipo', y),
     f"{NO['ipo']} ({CODE['do_ipo']}). Omdia DCI 전용 장비 2030년 57억달러({CODE['omdia_dci']})")
r += 1
rows4["c"] = r
line(r, "c", "데이터센터 광케이블(추정)", "Corning 데이터센터 매출(2025) × (1+CRU 물량 CAGR 28%)^(t−2025)",
     lambda y: f"{ref('corning', 2025)}*(1+'시장규모'!Q{row_of['dccable']})^({y}-2025)",
     f"{NO['corning']}·{NO['dccable']}. 1개사 매출 기반 하한 추정(자체)")
r += 1
rows4["d"] = r
line(r, "d", "데이터센터 PON 장비", "Dell'Oro 데이터센터 PON", lambda y: ref('dcpon', y), f"{NO['dcpon']} ({CODE['do_dcpon']})")
r += 1
rows4["sum"] = r
line(r, "합계", "데이터센터 광통신 투자 대상 합계", "a + b + c + d",
     lambda y: f"SUM({CL(YC4[y])}{rows4['a']}:{CL(YC4[y])}{rows4['d']})", "DC capex 탭 입력값", bold=True)
r += 1
put(ws4, r, 2, "Check", h="center")
put(ws4, r, 3, "합계 − 원값 재계산")
put(ws4, r, 4, None)
for y in YEARS:
    c = CL(YC4[y])
    expr = (f"{ref('tx_yole', y)}*{c}{rows4['shA']}+{ref('ipo', y)}+{ref('corning', 2025)}*(1+'시장규모'!Q{row_of['dccable']})^({y}-2025)+{ref('dcpon', y)}")
    put(ws4, r, YC4[y], f"=IFERROR(ROUND({c}{rows4['sum']}-({expr}),6),\"n/a\")", fmt='#,##0;(#,##0);"-"', h="right")
put(ws4, r, 11, None)
put(ws4, r, 12, None)
r += 1
line(r, "참고", "AI 백엔드 스위치(합계 제외)", "Dell'Oro 원값. 광부품이 아닌 네트워크 장비", lambda y: ref('aisw', y), f"{NO['aisw']} ({CODE['do_aisw']})")
r += 2
band(ws4, r, "③ 통신사 투자와 데이터센터 연결 (AT&T 사례)", 2, 12)
r += 1
header(ws4, r, ["항목", "내용", "", "", "", "", "", "", "", "", "출처"])
ws4.merge_cells(start_row=r, start_column=3, end_row=r, end_column=11)
r += 1
ATT = [
    ("투자 약속", "2026~2030년 5년간 2,500억달러 이상(광통신·무선·FWA·위성). 연 500억달러 수준으로 실제 capex(2024년 203억, 2025년 208억달러)의 2배 이상. 애널리스트 5년 capex 예상치 1,136억달러를 크게 웃돌아 capex 외 지출이 포함됐을 가능성", "att"),
    ("광가입자망", "광 커버리지 3,000만 가구 → 2030년 6,000만 가구. 2026년 신규 800만 가구(Lumen 인수 자산 포함)", "att_corning"),
    ("데이터센터 연결", "미국 데이터센터 90% 이상이 AT&T 광망 10마일 이내. AWS·Microsoft 데이터센터 간 고용량 광 연결(AWS Interconnect)", "att_dc"),
    ("광케이블 조달", "Corning과 30억달러 이상 다년 광섬유·케이블 공급계약(2026.9)", "att_corning"),
    ("업계 동향", "Verizon–Google 10억달러 이상 다크파이버 계약. 통신사 capex는 2026년 보합(-1%) 전망이나 AT&T 2분기 capex +16%", "comsoc_capex"),
    ("시사점", "통신사 투자는 데이터센터 내부 광트랜시버(② a)가 아니라 데이터센터 간 연결 광전송(② b)과 광케이블(② c)로 유입. 2025년 DCI용 WDM 직접구매 +40%(Dell'Oro)", "do_ot_sdx"),
]
for (k1, txt, sk) in ATT:
    put(ws4, r, 2, k1, bold=True, h="center")
    put(ws4, r, 3, txt, wrap=True)
    for c in range(4, 12):
        put(ws4, r, c, None)
    ws4.merge_cells(start_row=r, start_column=3, end_row=r, end_column=11)
    put(ws4, r, 12, cite(sk), color=BLUE, link=SRCD[sk][4], underline="single", wrap=True)
    ws4.row_dimensions[r].height = 30
    r += 1
# ④ 가정
assert r < A_BASE, r
r = A_BASE
band(ws4, r, "④ 가정", 2, 12)
ASV = [("s31", "데이터센터 비중 2031년(트랜시버·칩셋·패키징)", 0.90, "Yole: AI가 2030년대 초 광트랜시버 매출의 90% 이상", "yole_tx", "0.0%"),
       ("dc24", "데이터센터용 레이저칩 2024년", 1.6, "灼识咨询·LightCounting", "dx", "#,##0.0"),
       ("all24", "레이저칩 전체 2024년", 2.6, "灼识咨询·LightCounting", "dx", "#,##0.0"),
       ("dc30", "데이터센터용 레이저칩 2030년", 21.1, "灼识咨询·LightCounting", "dx", "#,##0.0"),
       ("all30", "레이저칩 전체 2030년", 22.9, "灼识咨询·LightCounting", "dx", "#,##0.0")]
for (k, lab, v, why, sk, fm) in ASV:
    rr = AS[k]
    put(ws4, rr, 2, "가정" if k == "s31" else "입력", h="center")
    put(ws4, rr, 3, lab, wrap=True)
    put(ws4, rr, 4, why, wrap=True)
    put(ws4, rr, 5, v, color=BLUE, fmt=fm, h="right")
    put(ws4, rr, 12, cite(sk), wrap=True)
for kc, w in {"A": 2, "B": 14, "C": 30, "D": 44, "E": 9, "F": 9, "G": 9, "H": 9, "I": 9, "J": 9, "K": 11, "L": 42}.items():
    ws4.column_dimensions[kc].width = w


def ref4(key, y):
    return f"'시장규모 요약'!{CL(YC4[y])}{rows4[key]}"


# ===================================================================== DC capex
title(ws5, "데이터센터향 광통신 Capex (USD bn)")
H5 = ["기준", "산식", "2025", "2026", "2027", "2028", "2029", "2030", "2026~30 누적", "판단 근거·한계"]
header(ws5, 3, H5)
YC5 = {y: 4 + i for i, y in enumerate(YEARS)}  # D..I
rows5 = {}
r = 4


def line5(r, name, how, fy, note, pct=False, bold=False, cum=True, fmt=None):
    put(ws5, r, 2, name, bold=bold, wrap=True)
    put(ws5, r, 3, how, wrap=True)
    for y in YEARS:
        f = fy(y)
        if f is None:
            put(ws5, r, YC5[y], "n/a")
        else:
            put(ws5, r, YC5[y], f"=IFERROR({f},\"n/a\")", fmt=fmt or ("0.0%" if pct else "#,##0.0"), h="right", bold=bold)
    if cum:
        put(ws5, r, 10, f"=IFERROR(SUM(E{r}:I{r}),\"n/a\")", fmt="#,##0.0", h="right", bold=bold)
    else:
        put(ws5, r, 10, None)
    put(ws5, r, 11, note, wrap=True)


band(ws5, r, "입력값", 2, 11)
r += 1
rows5["M"] = r
line5(r, "데이터센터 광통신 투자대상 시장 M(t)", "'시장규모 요약' ② 합계", lambda y: ref4("sum", y),
      "트랜시버·DCI·광케이블·PON 합계(중복 제거)", cum=False)
r += 1
rows5["cx1"] = r
line5(r, "데이터센터 Capex (2026.2 경로)", "Dell'Oro 원값", lambda y: ref("capex", y), f"{NO['capex']}", cum=False, fmt="#,##0")
r += 1
rows5["cx2"] = r
line5(r, "데이터센터 Capex (2026.7 상향 경로)", "2026년 원값 → 2030년 3조달러 사이 보간",
      lambda y: ref("capex", y) if y <= 2026 else f"{ref('capex', 2026)}*({ref('capex2', 2030)}/{ref('capex', 2026)})^(({y}-2026)/4)",
      f"{NO['capex2']}. 2027~29년은 기하 보간(자체)", cum=False, fmt="#,##0")
r += 1
rows5["sh"] = r
line5(r, "광통신 비중(Top5 클라우드 Capex 대비)", "LightCounting 원값·보간", lambda y: ref("optshare", y), f"{NO['optshare']}", pct=True, cum=False)
r += 2
band(ws5, r, "기준 A — 증분법: 당해 시장규모 − 전년 시장규모", 2, 11)
r += 1
rows5["A"] = r
line5(r, "A. 증분 투자", "M(t) − M(t−1)", lambda y: None if y == 2025 else f"{CL(YC5[y])}{rows5['M']}-{CL(YC5[y] - 1)}{rows5['M']}",
      "그해 새로 늘어난 지출만 잡음. 기존 규모만큼의 재구매(신규 클러스터·교체)는 빠져 실제 투자보다 작고, 성장 둔화 시 급감·감소 시 음수", bold=True)
r += 2
band(ws5, r, "기준 B — 연간 지출법: 당해 시장규모 = 당해 Capex", 2, 11)
r += 1
rows5["B"] = r
line5(r, "B. 연간 지출", "M(t)", lambda y: f"{CL(YC5[y])}{rows5['M']}",
      "광모듈·DCI 장비·광케이블은 매년 새 클러스터에 들어가 자본화되는 설비라 공급사 매출 = 구매자 capex. 회계상 capex 개념에 가장 부합", bold=True)
r += 2
band(ws5, r, "기준 C — Capex 비중법: 데이터센터 Capex × 광통신 비중", 2, 11)
r += 1
rows5["C1"] = r
line5(r, "C1. 비중법(2026.2 경로)", "데이터센터 Capex(2026.2) × 광통신 비중", lambda y: f"{CL(YC5[y])}{rows5['cx1']}*{CL(YC5[y])}{rows5['sh']}",
      "B와 독립된 하향식 검증용. 비중은 Top5 클라우드 기준이라 코로케이션·비AI 투자까지 포함한 전체 데이터센터 Capex에 적용하면 과대 가능", bold=True)
r += 1
rows5["C2"] = r
line5(r, "C2. 비중법(2026.7 상향 경로)", "데이터센터 Capex(2026.7) × 광통신 비중", lambda y: f"{CL(YC5[y])}{rows5['cx2']}*{CL(YC5[y])}{rows5['sh']}",
      "C1의 민감도. Dell'Oro 최신 전망(2030년 3조달러) 반영", bold=True)
r += 2
band(ws5, r, "비교", 2, 11)
r += 1
header(ws5, r, ["기준", "", "2025", "2026", "2027", "2028", "2029", "2030", "2026~30 누적", "선택 시 유의점"])
r += 1
for key, lab, nt in [("A", "A. 증분법", "투자 증가분. 누적값 = 2030년 − 2025년 시장규모"),
                     ("B", "B. 연간 지출법", "기본안으로 권고"),
                     ("C1", "C1. 비중법(2026.2)", "검증용"),
                     ("C2", "C2. 비중법(2026.7)", "검증용(상단)")]:
    line5(r, lab, "", lambda y, k=key: f"{CL(YC5[y])}{rows5[k]}" if not (k == "A" and y == 2025) else None, nt)
    r += 1
put(ws5, r, 2, "Check: A 누적 − (M2030 − M2025)")
put(ws5, r, 3, None)
for y in YEARS:
    put(ws5, r, YC5[y], None)
put(ws5, r, 10, f"=IFERROR(ROUND(J{rows5['A']}-(I{rows5['M']}-D{rows5['M']}),6),\"n/a\")", fmt='#,##0;(#,##0);"-"', h="right")
put(ws5, r, 11, None)
r += 1
line5(r, "B ÷ C1", "상향식 ÷ 하향식", lambda y: f"{CL(YC5[y])}{rows5['B']}/{CL(YC5[y])}{rows5['C1']}", "100%에 가까울수록 두 접근이 일치", pct=True, cum=False)
for kc, w in {"A": 2, "B": 32, "C": 34, "D": 9, "E": 9, "F": 9, "G": 9, "H": 9, "I": 9, "J": 12, "K": 70}.items():
    ws5.column_dimensions[kc].width = w

# ===================================================================== 출처
title(ws6, "출처 목록")
header(ws6, 3, ["코드", "발행처", "제목", "발간일", "원출처(조사기관)", "링크", "확인 방법"])
r = 4
for (k, pub, ttl, dt, orig, link, how) in SRC:
    put(ws6, r, 2, CODE[k], h="center")
    put(ws6, r, 3, pub, wrap=True)
    put(ws6, r, 4, ttl, wrap=True)
    put(ws6, r, 5, dt, h="center")
    put(ws6, r, 6, orig, wrap=True)
    put(ws6, r, 7, link, color=BLUE, link=link, underline="single")
    put(ws6, r, 8, how, wrap=True)
    r += 1
r += 1
band(ws6, r, "신뢰도 기준", 2, 8)
r += 1
for g, t in [("A", "조사기관·기업 원문(PDF·보도자료)에서 직접 확인"),
             ("B", "증권사·언론·컨설팅사가 조사기관 수치를 인용(인용 원문 확인)"),
             ("C", "1개사 실적 기반 추정 또는 검색 요약·개인 게시글로만 확인"),
             ("제외", "Research and Markets 등 범용 시장조사 재판매 보고서 수치(인용 포함)는 사용하지 않음")]:
    put(ws6, r, 2, g, h="center", bold=True)
    put(ws6, r, 3, t)
    ws6.merge_cells(start_row=r, start_column=3, end_row=r, end_column=8)
    r += 1
for kc, w in {"A": 2, "B": 7, "C": 30, "D": 60, "E": 14, "F": 30, "G": 70, "H": 30}.items():
    ws6.column_dimensions[kc].width = w

# ===================================================================== 공통 마무리
for ws in wb.worksheets:
    ws.sheet_view.showGridLines = False
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None:
                apply_font(c)
wb.save(OUT)
print("saved", OUT, "market rows", len(M), "sources", len(SRC))
