"""DART 주석 → 분기 비용 원자료 (원재료와 소모품 사용액 + 판매비와관리비 전 계정)

연결(기본) 재무제표 주석의 「비용의 성격별 분류」에서 원재료와 소모품의 사용액·제품과 재공품의 변동·합계를,
「판매비와관리비」에서 계정별 금액을 분기 3개월 기준(백만원)으로 뽑아 재무모델 「비용 원자료」 시트 형식으로 저장합니다.
  - 1Q = 1분기 누적, 2Q·3Q = 해당 보고서 3개월 열, 4Q = 사업보고서 연간 − 3분기 누적
  - 계정명은 CANON 목록으로 맞추고, 목록에 없는 계정은 「미매칭 계정」 행으로 따로 둠 (모델의 「기타」 행이 흡수)

필요: 환경변수 DART_API_KEY, 네트워크에서 opendart.fss.or.kr 허용
실행:
    python dart_cost_quarterly.py 066970 --since 20190101 --until 20260930 --out lnf_cost_raw.xlsx
    python dart_cost_quarterly.py 066970 --xml-dir xml/        # 받아둔 원문 재사용
결과: lnf_cost_raw.xlsx(「비용 원자료」 시트) + lnf_cost_raw.json
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dart_periodic_extract import load_key, corp_code, periodic_reports, fetch_doc  # noqa: E402
from dart_sga_quarterly import extract_sga, norm_acct, num, UNIT_RE, TO_MN, _txt  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402

# 판관비 계정 (모델 행 순서). 변동비 → 고정비 순
CANON_VAR = ["운반비", "판매수수료", "수출제비용", "포장비", "견본비", "하자보수비", "대손상각비"]
CANON_FIX = ["급여", "종업원단기급여", "퇴직급여", "복리후생비", "주식보상비용", "여비교통비", "차량유지비", "세금과공과",
             "임차료", "가스사용료", "수도사용료", "전력비", "감가상각비", "사용권자산상각비", "무형자산상각비", "수선비",
             "보험료", "접대비", "광고선전비", "경상개발비", "교육훈련비", "통신비", "소모품비", "도서인쇄비", "지급수수료",
             "회의비", "공해관리비", "잡비"]
CANON = CANON_VAR + CANON_FIX
RAW_RE = re.compile(r"원재료.*(사용|소모)|원재료와소모품|원재료및소모품")
INV_RE = re.compile(r"(제품|재공품|재고자산).*변동")
TOT = {"합계", "계", "총계", "총비용", "합 계"}


def quarter_label(period):
    y, m = period.split(".")
    return f"Q{int(m) // 3} {y}"


def _cols(rows):
    """헤더 행에서 3개월·누적 위치를 찾아 (i3, ic) 반환. 3개월 열이 없으면 (None, 0)"""
    hdr = []
    for r in rows:
        if any(num(c) is not None for c in r[1:]):
            break
        hdr.append(r)
    i3 = ic = None
    for r in hdr:
        labs = [c for c in r if "3개월" in c or "누적" in c]
        if labs:
            i3 = next((i for i, c in enumerate(labs) if "3개월" in c), None)
            ic = next((i for i, c in enumerate(labs) if "누적" in c), None)
    unit = UNIT_RE.search(" ".join(" ".join(r) for r in hdr))
    return i3, (0 if ic is None else ic), (unit.group(1) if unit else None), len(hdr)


def extract_nature(xml, basis="연결"):
    """「비용의 성격별 분류」 표 → {'raw','inv','total': (3개월, 누적)}, 단위"""
    soup = BeautifulSoup(xml, "html.parser")
    sec, flag, unit = None, False, None
    for el in soup.find_all(["title", "p", "table"]):
        if el.find_parent("table") is not None:
            continue
        if el.name == "title":
            t = _txt(el)
            sec = "연결" if re.search(r"연결\s*재무\s*제표\s*주석", t) else "별도" if re.search(r"재무\s*제표\s*주석", t) else None
            flag = False
            continue
        if el.name == "p":
            t = _txt(el)
            mu = UNIT_RE.search(t)
            if mu:
                unit = mu.group(1)
            if len(t) <= 60 and "성격별" in t:
                flag = True
            elif re.match(r"^\(?\d+\)?[.)]\s*\S", t) and len(t) <= 40:
                flag = False
            continue
        rows = [[_txt(td) for td in tr.find_all(["th", "td", "te", "tu"])] for tr in el.find_all("tr")]
        rows = [r for r in rows if any(r)]
        if len(rows) <= 2 and sum(len(r) for r in rows) <= 3:
            mu = UNIT_RE.search(" ".join(" ".join(r) for r in rows))
            if mu:
                unit = mu.group(1)
            continue
        if sec != basis or not flag or len(rows) < 4:
            continue
        labels = [re.sub(r"\s+", "", r[0]) for r in rows if r]
        if not any(RAW_RE.search(x) for x in labels):
            continue
        i3, ic, u2, nh = _cols(rows)
        out = {}
        for r in rows[nh:]:
            lab = re.sub(r"\s+", "", r[0]) if r else ""
            vals = [num(c) for c in r[1:]]
            cum = vals[ic] if ic < len(vals) else None
            m3 = vals[i3] if (i3 is not None and i3 < len(vals)) else cum
            key = "raw" if RAW_RE.search(lab) and "변동" not in lab else "inv" if INV_RE.search(lab) else "total" if lab in TOT else None
            if key and key not in out:
                out[key] = (m3, cum)
        if "raw" in out:
            return out, (u2 or unit or "원")
    return None, None


def quarterize(per_period, getter):
    """{기간: 보고서 데이터} → {분기라벨: 3개월값}. 4Q = 연간 − 3Q 누적"""
    q = {}
    for p, d in per_period.items():
        y, m = p.split(".")
        v = getter(d)
        if v is None:
            continue
        m3, cum = v
        if m in ("03", "06", "09"):
            q[quarter_label(p)] = m3 if m3 is not None else cum
        else:
            prev = per_period.get(f"{y}.09")
            pv = getter(prev) if prev else None
            if cum is not None and pv is not None and pv[1] is not None:
                q[f"Q4 {y}"] = cum - pv[1]
    return q


def write_raw(path, corp, quarters, data):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "비용 원자료"
    TEAL, BLUE = PatternFill("solid", fgColor="006C64"), "0000FF"
    ws["B2"] = f"{corp} 비용 원자료 (DART 연결재무제표 주석)"
    ws["B3"] = "단위: 백만원, 분기 3개월. 4Q = 사업보고서 연간 − 3분기 누적"
    ws["B5"], ws["C5"] = "계정", "비고"
    for j, q in enumerate(quarters):
        ws.cell(4, 4 + j, int(q.split()[1]))
        ws.cell(5, 4 + j, q)
    for c in range(2, 4 + len(quarters)):
        ws.cell(5, c).fill = TEAL
        ws.cell(5, c).font = Font(bold=True, color="FFFFFF")
    rows = [("비용의 성격별 분류", None), ("원재료와 소모품의 사용액", "raw"), ("제품과 재공품의 변동", "inv"), ("성격별 비용 합계(공시)", "total"), ("", None),
            ("판매비와관리비", None)] + [(a, ("sga", a)) for a in CANON] + [("판매비와관리비 합계(공시)", "sga_total"), ("", None), ("미매칭 계정", None)]
    r = 7
    rowmap = {}
    for lab, key in rows:
        ws.cell(r, 2, lab)
        if key is None and lab:
            ws.cell(r, 2).font = Font(bold=True)
        rowmap[key if not isinstance(key, tuple) else key[1]] = r
        if key:
            for j, q in enumerate(quarters):
                v = data.get(q, {}).get(key if not isinstance(key, tuple) else "sga", {})
                v = v.get(key[1]) if isinstance(key, tuple) else v
                if isinstance(v, (int, float)):
                    c = ws.cell(r, 4 + j, round(v, 6))
                    c.font = Font(color=BLUE)
                    c.number_format = '#,##0.0;(#,##0.0);"-"'
        r += 1
    extra = sorted({a for q in quarters for a in data.get(q, {}).get("sga", {}) if a not in CANON})
    for a in extra:
        ws.cell(r, 2, a)
        for j, q in enumerate(quarters):
            v = data.get(q, {}).get("sga", {}).get(a)
            if isinstance(v, (int, float)):
                c = ws.cell(r, 4 + j, round(v, 6))
                c.font = Font(color=BLUE)
        r += 1
    wb.save(path)
    return rowmap


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stock")
    ap.add_argument("--basis", default="연결", choices=["연결", "별도"])
    ap.add_argument("--since", default="20190101")
    ap.add_argument("--until", default=time.strftime("%Y%m%d"))
    ap.add_argument("--first", default="Q1 2019", help="첫 분기 라벨")
    ap.add_argument("--last", default="Q2 2026", help="마지막 분기 라벨")
    ap.add_argument("--out", default=None)
    ap.add_argument("--env", default=None)
    ap.add_argument("--keep-xml", default=None)
    ap.add_argument("--xml-dir", default=None)
    a = ap.parse_args()

    if a.xml_dir:
        reps, name = [], a.stock
        for f in sorted(Path(a.xml_dir).glob("*.xml")):
            m = re.match(r"(\d{4}\.\d{2})_(\d+)", f.stem)
            if m:
                reps.append({"period": m.group(1), "rcept_no": m.group(2), "_file": f})
        get = lambda r: r["_file"].read_text(encoding="utf-8")  # noqa: E731
    else:
        key = load_key(a.env)
        cc, name = corp_code(key, a.stock)
        reps = periodic_reports(key, cc, a.since, a.until)
        get = lambda r: fetch_doc(key, r["rcept_no"])  # noqa: E731
    print(f"{name}: 정기보고서 {len(reps)}건")
    per = {}
    for r in reps:
        xml = get(r)
        if not xml:
            print(f"  {r['period']} 원문 없음")
            continue
        if a.keep_xml and not a.xml_dir:
            Path(a.keep_xml).mkdir(parents=True, exist_ok=True)
            Path(a.keep_xml, f"{r['period']}_{r['rcept_no']}.xml").write_text(xml, encoding="utf-8")
        nat, nu = extract_nature(xml, a.basis)
        sga = extract_sga(xml, a.basis)
        d = {}
        if nat:
            k = TO_MN.get(nu, 1e-3)
            d["nature"] = {kk: tuple(None if x is None else x * k for x in vv) for kk, vv in nat.items()}
        if sga:
            k = TO_MN.get(sga["unit"], 1e-3)
            d["sga"] = {kk: tuple(None if x is None else x * k for x in vv) for kk, vv in sga["accts"].items()}
            d["sga_total"] = tuple(None if x is None else x * k for x in sga["total"]) if sga["total"] else None
        per[r["period"]] = d
        print(f"  {r['period']}: 성격별 {'O' if nat else 'X'} · 판관비 {len(sga['accts']) if sga else 'X'}")
        if not a.xml_dir:
            time.sleep(0.4)

    ys, ye = int(a.first.split()[1]), int(a.last.split()[1])
    quarters = [f"Q{q} {y}" for y in range(ys, ye + 1) for q in (1, 2, 3, 4)]
    quarters = quarters[quarters.index(a.first): quarters.index(a.last) + 1]
    data = {q: {"sga": {}} for q in quarters}
    for key in ("raw", "inv", "total"):
        for q, v in quarterize(per, lambda d, key=key: d.get("nature", {}).get(key)).items():
            if q in data:
                data[q][key] = v
    for q, v in quarterize(per, lambda d: d.get("sga_total")).items():
        if q in data:
            data[q]["sga_total"] = v
    accts = sorted({x for d in per.values() for x in d.get("sga", {})})
    for acc in accts:
        for q, v in quarterize(per, lambda d, acc=acc: d.get("sga", {}).get(acc) or ((0.0, 0.0) if "sga" in d else None)).items():
            if q in data:
                data[q]["sga"][acc] = v
    out = a.out or f"{a.stock}_cost_raw.xlsx"
    write_raw(out, name, quarters, data)
    Path(out).with_suffix(".json").write_text(json.dumps({"corp": name, "unit": "백만원", "quarters": quarters, "data": data}, ensure_ascii=False, indent=1), encoding="utf-8")
    miss = [q for q in quarters if "raw" not in data[q] or "sga_total" not in data[q]]
    print(f"완료 → {out}" + (f" (누락 분기: {', '.join(miss)})" if miss else ""))


if __name__ == "__main__":
    main()
