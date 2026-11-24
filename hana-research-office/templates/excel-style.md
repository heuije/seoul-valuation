# 엑셀 산출물 양식 규칙 (대표이사 지시, 2026-11-24 확정)

엑셀(.xlsx) 표·모델을 만들거나 고칠 때 아래 규칙을 모두 적용한다. 공통 서식 규칙(글꼴·IFERROR·n/a 우측정렬·Check 행·틀고정 금지·메모 보존)은 `excel-model-house-rules` 스킬을 따르고, 이 문서는 그 위에 추가되는 양식 규칙이다.

## 1. 표 구조
- 같은 값이 세로로 이어지는 분류 열(예: Stream·사업·제품)은 **셀 병합**한다. 병합 셀은 가운데 정렬.
- Stream 구분 행(예: `Upstream — 소재·칩·부품 (광모듈 向 소재)`)은 연한 청록 띠로 표 전체 폭에 둔다.
- 머리글 행: 진한 청록(006C64) 바탕·흰색 굵은 글씨·가운데 정렬.
- 기준 양식: `deliverables/2026-11-24_광모듈_밸류체인/` 의 대표이사 수정 구조표(B2 제목, 3행 머리글 `Stream | 사업 | 제품 | 품목 | 품목 설명 | 적용 애플리케이션 | 비고`).

## 2. 화면
- 모든 시트 **눈금선 숨김**.
- 틀고정 추가 금지(원본에 없으면).

## 3. 제목·소제목
- B2 제목은 짧은 명사구로만 쓴다(예: `통신용 광모듈 밸류체인 구조`). 설명 문장, 기준일, 용어 풀이를 제목 줄에 붙이지 않는다.
- 소제목·구분 행도 같은 방식으로 간략히 쓴다. 필요한 설명은 비고 열이나 별도 주석 탭으로 보낸다.

## 4. 값 표기
- 원문·입력 숫자 = 파란 글씨, 탭 내 계산 = 검은 글씨. 이 색 구분이 곧 값의 출처 표시이므로 "값 처리" 같은 별도 설명 열을 만들지 않는다.

## 5. 출처
- 출처 목록은 본문 표 아래에 두지 않고 **별도 탭(출처)** 으로 관리한다. 본문에는 출처 코드(S1, S2 …)만 남긴다.
- 우선 사용: Yole Group, Omdia, LightCounting, Dell'Oro, Cignal AI, 증권사·컨설팅사 리포트(PDF), 기업 IR 자료.
- **사용 금지(현재·향후 모두)**: Research and Markets 및 같은 성격의 범용 시장조사 재판매 보고서(GII, MarketsandMarkets, Mordor Intelligence, DataIntelo, QYResearch, LP Information, DiReports, PS Market Research, Industry Research, Fortune Business Insights, Global Market Insights 등). 증권사 PDF가 이들을 인용한 수치도 쓰지 않는다.
