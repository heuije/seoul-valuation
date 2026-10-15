"""DART 정기보고서 핵심 표 추출 — 생산능력·생산실적·가동률·가격변동(ASP)·매출실적·수주

엘앤에프·롯데에너지머티리얼즈 등 상장사의 2019년 이후 분기·반기·사업보고서를 OpenDART에서 받아
「II. 사업의 내용」의 표를 항목별로 엑셀 시트에 그대로 옮깁니다. 정정보고서가 있으면 최신본만 씁니다.
이 원자료 시트를 기준으로 공장별 분기 CAPA 등 모델 시트를 따로 만듭니다.

필요: 환경변수 DART_API_KEY (텔레그램 봇 .env의 키와 같은 것), 네트워크에서 opendart.fss.or.kr 허용
실행:
    python dart_periodic_extract.py 066970 --since 20190101 --out lnf_dart_raw.xlsx
    python dart_periodic_extract.py 020150 --out lotteemat_dart_raw.xlsx      # 롯데에너지머티리얼즈
옵션: --env 경로(.env), --keep-xml 폴더(원문 XML 보관, 검증용)
"""
import argparse
import json
import os
import re
import sys
import time
import zipfile
from io import BytesIO
from pathlib import Path

import requests
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

API = "https://opendart.fss.or.kr/api"
# 항목별 표 제목(직전 문단·제목)에서 찾을 키워드
CATS = {
    "생산능력": ["생산능력"],
    "생산실적·가동률": ["생산실적", "가동률"],
    "가격변동(ASP)": ["가격변동", "가격 변동", "판매가격"],
    "매출실적": ["매출실적", "매출 실적", "판매실적"],
    "수주": ["수주"],
    "원재료": ["원재료"],
    "생산설비·투자": ["생산설비", "시설투자", "투자계획", "신규투자"],
}
REPORT_RE = re.compile(r"(분기보고서|반기보고서|사업보고서)\s*\((\d{4})\.(\d{2})\)")


def load_key(env_path):
    if env_path and Path(env_path).exists():
        for line in Path(env_path).read_text(encoding="utf-8").splitlines():
            if line.startswith("DART_API_KEY="):
                os.environ.setdefault("DART_API_KEY", line.split("=", 1)[1].strip())
    k = os.getenv("DART_API_KEY")
    if not k:
        sys.exit("DART_API_KEY가 없습니다 — 환경변수로 설정하거나 --env로 .env 경로를 주세요")
    return k


def corp_code(key, stock):
    raw = requests.get(f"{API}/corpCode.xml?crtfc_key={key}", timeout=60).content
    z = zipfile.ZipFile(BytesIO(raw))
    soup = BeautifulSoup(z.read(z.namelist()[0]), "html.parser")
    for it in soup.find_all("list"):
        if (it.find("stock_code").text or "").strip() == stock:
            return it.find("corp_code").text.strip(), it.find("corp_name").text.strip()
    sys.exit(f"종목코드 {stock}의 corp_code를 찾지 못했습니다")


def periodic_reports(key, cc, since, until):
    """정기공시 목록 → 기간(YYYY.MM)별 최신 접수본 하나씩"""
    out, page = {}, 1
    while True:
        d = requests.get(f"{API}/list.json", params=dict(crtfc_key=key, corp_code=cc, bgn_de=since, end_de=until,
                         pblntf_ty="A", page_no=page, page_count=100), timeout=30).json()
        if d.get("status") != "000":
            break
        for it in d.get("list", []):
            m = REPORT_RE.search(it.get("report_nm", ""))
            if not m:
                continue
            per = f"{m.group(2)}.{m.group(3)}"
            if per not in out or it["rcept_no"] > out[per]["rcept_no"]:  # 정정본(나중 접수)이 우선
                out[per] = {"period": per, "kind": m.group(1), "rcept_no": it["rcept_no"], "report_nm": it["report_nm"].strip(),
                            "rcept_dt": it.get("rcept_dt", "")}
        if page >= int(d.get("total_page", 1)):
            break
        page += 1
        time.sleep(0.2)
    return [out[k] for k in sorted(out)]


def fetch_doc(key, rcept_no):
    raw = requests.get(f"{API}/document.xml", params=dict(crtfc_key=key, rcept_no=rcept_no), timeout=60).content
    if raw[:2] != b"PK":
        return None
    z = zipfile.ZipFile(BytesIO(raw))
    names = sorted(z.namelist(), key=lambda n: (not n.startswith(rcept_no), -z.getinfo(n).file_size))  # 본문 우선
    b = z.read(names[0])
    for enc in ("utf-8", "euc-kr", "cp949"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            pass
    return b.decode("utf-8", errors="replace")


def _txt(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


H1 = re.compile(r"^(\d+|[IVX]+)\.\s")
H2 = re.compile(r"^[가-하][.)]\s?")
H3 = re.compile(r"^(\(\d+\)|\d+\)|[①-⑳])")


def extract_tables(xml):
    """제목 계층(1.→가.→(1))을 따라가며, 표 바로 위 소제목에 키워드가 있는 표를 행 단위로 반환.
    상위 제목(예: 「3. 원재료 및 생산설비」)만으로는 분류하지 않아 다른 표가 섞이지 않게 함"""
    soup = BeautifulSoup(xml, "html.parser")
    lv, notes, out = {1: "", 2: "", 3: ""}, [], []
    for el in soup.find_all(["title", "p", "table"]):
        if el.name in ("title", "p"):
            if el.find_parent("table") is not None:
                continue
            t = _txt(el)
            if not t or len(t) > 90:
                continue
            k = 1 if (el.name == "title" or H1.match(t)) else 2 if H2.match(t) else 3 if H3.match(t) else 0
            if k:
                lv[k] = t
                for j in range(k + 1, 4):
                    lv[j] = ""
                notes = []
            else:
                notes = (notes + [t])[-2:]
            continue
        if el.find_parent("table") is not None:
            continue  # 중첩 표는 바깥 표에서 처리
        key = " / ".join(x for x in (lv[2], lv[3]) if x) or lv[1]
        cats = [c for c, kws in CATS.items() if any(kw in key for kw in kws)]
        if not cats:
            continue
        rows = []
        for tr in el.find_all("tr"):
            cells = [_txt(td) for td in tr.find_all(["th", "td", "te", "tu"])]
            if any(cells):
                rows.append(cells)
        if rows:
            out.append({"cats": cats, "context": " / ".join(x for x in (lv[1], lv[2], lv[3], *notes) if x), "rows": rows})
    return out


def write_xlsx(path, corp, reports, results):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    KR, EN = "맑은 고딕", "Arial"
    han = re.compile(r"[가-힣]")
    wb = Workbook()
    ws0 = wb.active
    ws0.title = "목록"
    ws0.append(["회사", corp])
    ws0.append(["기간", "보고서", "접수번호", "접수일", "DART 링크", "추출 표 수"])
    for r in reports:
        n = sum(len(x) for x in results.get(r["rcept_no"], {}).values())
        ws0.append([r["period"], r["report_nm"], r["rcept_no"], r["rcept_dt"],
                    f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={r['rcept_no']}", n])
    for cat in CATS:
        ws = wb.create_sheet(cat[:31].replace("/", "·"))
        ws.append(["기간", "접수번호", "표 문맥(직전 제목·문단)", "표 번호", "행 번호", "셀1", "셀2", "셀3", "셀4", "셀5", "셀6", "셀7", "셀8", "셀9", "셀10", "…"])
        for r in reports:
            for ti, tb in enumerate(results.get(r["rcept_no"], {}).get(cat, []), 1):
                for ri, row in enumerate(tb["rows"], 1):
                    ws.append([r["period"], r["rcept_no"], tb["context"], ti, ri] + row)
    for ws in wb.worksheets:  # 사내 엑셀 규칙: 한글 셀 맑은 고딕, 숫자·영문 Arial, 10pt
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                c.font = Font(name=KR if (isinstance(c.value, str) and han.search(c.value)) else EN, size=10)
    wb.save(path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stock", help="종목코드 6자리 (엘앤에프 066970)")
    ap.add_argument("--since", default="20190101")
    ap.add_argument("--until", default=time.strftime("%Y%m%d"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--env", default=None)
    ap.add_argument("--keep-xml", default=None)
    a = ap.parse_args()
    key = load_key(a.env)
    cc, name = corp_code(key, a.stock)
    reps = periodic_reports(key, cc, a.since, a.until)
    print(f"{name}: 정기보고서 {len(reps)}건 ({reps[0]['period'] if reps else '-'} ~ {reps[-1]['period'] if reps else '-'})")
    results = {}
    for r in reps:
        xml = fetch_doc(key, r["rcept_no"])
        if xml is None:
            print(f"  {r['period']} 원문 없음")
            continue
        if a.keep_xml:
            Path(a.keep_xml).mkdir(parents=True, exist_ok=True)
            Path(a.keep_xml, f"{r['period']}_{r['rcept_no']}.xml").write_text(xml, encoding="utf-8")
        by = {}
        for tb in extract_tables(xml):
            for c in tb["cats"]:
                by.setdefault(c, []).append(tb)
        results[r["rcept_no"]] = by
        print(f"  {r['period']} {r['kind']}: " + ", ".join(f"{c} {len(v)}" for c, v in by.items()))
        time.sleep(0.4)
    out = a.out or f"{a.stock}_dart_raw.xlsx"
    write_xlsx(out, name, reps, results)
    Path(out).with_suffix(".json").write_text(json.dumps({"corp": name, "reports": reps, "tables": results}, ensure_ascii=False), encoding="utf-8")
    print(f"완료 → {out} (+ .json)")


if __name__ == "__main__":
    main()
