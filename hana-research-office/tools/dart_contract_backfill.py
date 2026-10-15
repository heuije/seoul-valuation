"""DART 공급계약 공시 백필 — 2차전지 밸류체인 맵 출처 보강용

텔레그램 뉴스봇(heuije/telegram-news-bot)의 DART 모니터링 설정을 그대로 씁니다.
같은 .env(DART_API_KEY)와 battery_companies.csv를 읽고, 기간 전체의
'단일판매ㆍ공급계약'(체결·정정·해지) 공시를 CSV로 내보냅니다.
텔레그램 발송과 Claude 요약은 하지 않습니다.

실행 (봇 폴더에서):
    python dart_contract_backfill.py                      # 2018-01-01 ~ 오늘
    python dart_contract_backfill.py --since 20230101 --no-body
    python dart_contract_backfill.py --env /path/.env --csv /path/battery_companies.csv --out dart_contracts.csv

출력 열: 기업, 티커, 접수일, 공시명, 접수번호, DART 링크, 계약상대방, 계약금액(원),
         매출액대비(%), 계약시작, 계약종료, 공급지역, 본문확보
결과 CSV는 공개 공시 정보만 담습니다. 맵 담당자에게 전달하면 관계별 DART 링크로 반영합니다.
"""
import argparse
import csv
import os
import re
import sys
import time
import zipfile
import xml.etree.ElementTree as ETree
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

DART_API = "https://opendart.fss.or.kr/api"
KEYWORDS = ["단일판매", "공급계약"]  # 공백 제거 후 부분일치 (체결·정정·해지 모두 포함)

# 맵에는 있으나 봇 CSV에 없는 상장사 (2026.10.15 기준)
EXTRA_TICKERS = {
    "025900": "동화기업", "093370": "후성", "336370": "솔루스첨단소재",
    "006110": "삼아알미늄", "008730": "율촌화학", "014820": "동원시스템즈",
}


def load_companies(csv_path):
    rows = {}
    with open(csv_path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            t = (r.get("티커") or "").strip()
            if len(t) == 6:
                rows[t] = (r.get("기업명") or "").strip()
    for t, n in EXTRA_TICKERS.items():
        rows.setdefault(t, n)
    return rows


def corp_index(key, tickers):
    raw = requests.get(f"{DART_API}/corpCode.xml?crtfc_key={key}", timeout=60).content
    z = zipfile.ZipFile(BytesIO(raw))
    root = ETree.fromstring(z.read(z.namelist()[0]))
    idx = {}
    for it in root.iter("list"):
        sc = (it.findtext("stock_code") or "").strip()
        cc = (it.findtext("corp_code") or "").strip()
        if sc in tickers and cc:
            idx[cc] = (tickers[sc], sc)
    return idx


def list_disclosures(key, corp_code, bgn, end):
    """거래소공시(I) 전체를 페이지 단위로 받아 공급계약만 남긴다."""
    out, page = [], 1
    while True:
        url = (f"{DART_API}/list.json?crtfc_key={key}&corp_code={corp_code}"
               f"&bgn_de={bgn}&end_de={end}&pblntf_ty=I&page_no={page}&page_count=100")
        d = requests.get(url, timeout=20).json()
        if d.get("status") != "000":  # 013 = 데이터 없음
            break
        for it in d.get("list", []):
            nm = (it.get("report_nm") or "").replace(" ", "")
            if any(k in nm for k in KEYWORDS):
                out.append(it)
        if page >= int(d.get("total_page", 1)):
            break
        page += 1
        time.sleep(0.2)
    return out


def fetch_body(key, rcept_no):
    raw = requests.get(f"{DART_API}/document.xml?crtfc_key={key}&rcept_no={rcept_no}", timeout=30).content
    if raw[:2] != b"PK":  # 원문 미제공(014 등)
        return None
    z = zipfile.ZipFile(BytesIO(raw))
    content = z.read(z.namelist()[0])
    try:
        t = content.decode("utf-8")
    except UnicodeDecodeError:
        t = content.decode("euc-kr", errors="replace")
    return BeautifulSoup(t, "html.parser").get_text(" ", strip=True)


def parse_body(body):
    """단일판매ㆍ공급계약체결 본문에서 핵심 항목 추출 (양식 차이로 빈 값이 나올 수 있음)."""
    if not body:
        return {}
    b = re.sub(r"\s+", " ", body)
    g = lambda p: (m.group(1).strip() if (m := re.search(p, b)) else "")
    return {
        "계약상대방": g(r"계약\s*상대(?:방)?\s*[:：]?\s*(.+?)\s*-\s*(?:최근\s*매출액|회사와의\s*관계|주요\s*사업)"),
        "계약금액(원)": g(r"계약금액(?:\s*총액)?\s*\(원\)\s*([\d,]+)") or g(r"계약금액\s*([\d,]{6,})"),
        "매출액대비(%)": g(r"매출액\s*대비\s*\(%\)\s*([\d.]+)"),
        "계약시작": g(r"계약기간\s*시작일\s*([\d.\-]+)"),
        "계약종료": g(r"계약기간\s*(?:시작일\s*[\d.\-]+\s*)?종료일\s*([\d.\-]+)"),
        "공급지역": g(r"판매\s*[ㆍ·]?\s*공급\s*지역\s*(.+?)\s*\d+\.\s"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    here = Path(__file__).resolve().parent
    ap.add_argument("--env", default=str(here / ".env"))
    ap.add_argument("--csv", default=str(here / "battery_companies.csv"))
    ap.add_argument("--since", default="20180101")
    ap.add_argument("--out", default="dart_contracts.csv")
    ap.add_argument("--no-body", action="store_true", help="본문(계약상대방 등) 조회 생략 — 빠름")
    a = ap.parse_args()

    load_dotenv(a.env, override=True)
    key = os.getenv("DART_API_KEY")
    if not key:
        sys.exit("DART_API_KEY 없음 — 봇의 .env 경로를 --env로 지정하세요")
    tickers = load_companies(a.csv)
    idx = corp_index(key, tickers)
    print(f"대상 {len(idx)}/{len(tickers)}개 기업")
    end = datetime.now().strftime("%Y%m%d")
    cols = ["기업", "티커", "접수일", "공시명", "접수번호", "DART 링크", "계약상대방", "계약금액(원)",
            "매출액대비(%)", "계약시작", "계약종료", "공급지역", "본문확보"]
    n = 0
    with open(a.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for cc, (name, tk) in idx.items():
            try:
                items = list_disclosures(key, cc, a.since, end)
            except Exception as e:
                print(f"  ⚠️ {name} 목록 오류: {e}")
                continue
            for it in items:
                rn = it.get("rcept_no", "")
                rd = it.get("rcept_dt", "")
                row = {"기업": name, "티커": tk, "접수일": f"{rd[:4]}-{rd[4:6]}-{rd[6:8]}" if len(rd) == 8 else rd,
                       "공시명": (it.get("report_nm") or "").strip(), "접수번호": rn,
                       "DART 링크": f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rn}", "본문확보": "N"}
                if not a.no_body:
                    try:
                        body = fetch_body(key, rn)
                        if body:
                            row.update(parse_body(body))
                            row["본문확보"] = "Y"
                    except Exception as e:
                        print(f"  ⚠️ {name} {rn} 본문 오류: {e}")
                    time.sleep(0.3)
                w.writerow(row)
                n += 1
            print(f"  {name}: {len(items)}건")
            time.sleep(0.2)
    print(f"완료 — {n}건 → {a.out}")


if __name__ == "__main__":
    main()
