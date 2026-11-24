# -*- coding: utf-8 -*-
"""통신용 광모듈 밸류체인 / 기업 매핑 / 시장규모(2025~2030) 엑셀 생성."""
import re, sys
from copy import copy
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.cell.rich_text import CellRichText, TextBlock
from openpyxl.cell.text import InlineFont
from openpyxl.utils import get_column_letter as CL


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


