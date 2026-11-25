"""2026-11-25 외부 교차검증(1~5번) 반영: FIE 요건·실효적 통제·MACR 법문 기준 정리."""

L = "검색 결과에서 주소·내용 확인(2026.11.25). 조문 원문은 이 환경에서 직접 열람 불가"
W = "검색 결과에서 주소 확인(2026.11.25)"

NEW_SRC2 = {
    "l1": dict(pub="Cornell LII(미 연방법전)", title="26 U.S. Code § 7701(a)(51) 금지외국기업(SFE·FIE·covered officer·실효적 통제) 정의", date="2025.07.04 개정", url="https://www.law.cornell.edu/uscode/text/26/7701", check=L),
    "l2": dict(pub="Cornell LII(미 연방법전)", title="26 U.S. Code § 45X Advanced manufacturing production credit", date="2025.07.04 개정", url="https://www.law.cornell.edu/uscode/text/26/45X", check=L),
    "l3": dict(pub="IRS", title="Notice 2026-15: Interim Safe Harbors for Material Assistance from a Prohibited Foreign Entity; Other PFE Guidance", date="2026.02.12", url="https://www.irs.gov/pub/irs-drop/n-26-15.pdf", check=W),
    "l4": dict(pub="Gibson Dunn", title="New Debt Issuance Considerations under the One Big Beautiful Bill Act(상장기업 채무 기준)", date="2025", url="https://www.gibsondunn.com/new-debt-issuance-considerations-under-the-one-big-beautiful-bill-act/", check=W),
    "l5": dict(pub="Holland & Knight", title="OBBB Renewable and Alternative Energy Tax Incentives(상장기업 지분 기준·SEC 13d-3)", date="2025.07.11", url="https://www.hklaw.com/-/media/files/events/2025/07/071125_obbb_renewableandalternativeenergytaxincentives.pdf", check=W),
    "l6": dict(pub="Tax Law Center", title="Summary of Prohibited Foreign Entity (PFE) Rules (48E/45Y/45X only)", date="2025", url="https://taxlawcenter.org/files/Tax-Law-Center-Summary-of-Prohibited-Foreign-Entity-Rules-for-45Y-48E-45X.pdf", check=W),
    "l7": dict(pub="Bracewell", title="Treasury and IRS Issue Guidance on Foreign Entity of Concern Rules for Clean Energy Tax Credits", date="2026.02", url="https://www.bracewell.com/resources/treasury-and-irs-issue-guidance-on-foreign-entity-of-concern-rules-for-clean-energy-tax-credits/", check=W),
    "l8": dict(pub="Sidley", title="The One Big Beautiful Bill Act: Navigating the New Energy Landscape(45X 부품별 기준표)", date="2025.07", url="https://www.sidley.com/en/insights/newsupdates/2025/07/the-one-big-beautiful-bill-act-navigating-the-new-energy-landscape", check=W),
    "l9": dict(pub="Davis Wright Tremaine", title="IRS Releases Guidance on Use of Foreign Equipment in Clean Energy Projects(ESS 55→75%, 발전설비 40→60%)", date="2026.02", url="https://www.dwt.com/blogs/energy--environmental-law-blog/2026/02/irs-clean-energy-projects-guidance", check=W),
    "l10": dict(pub="Reunion Infrastructure", title="A Comprehensive Guide to Prohibited Foreign Entities for Clean Energy Tax Credits", date="발행일 미확인", url="https://www.reunioninfra.com/insights/comprehensive-guide-to-prohibited-foreign-entities-for-clean-energy-tax-credits", check=W),
    "l11": dict(pub="Bipartisan Policy Center", title="Unpacking the FEOC Provisions in the One Big Beautiful Bill Act(45X SFE·FIE 적용 시점)", date="2025.07", url="https://bipartisanpolicy.org/explainer/unpacking-the-feoc-provisions-in-the-one-big-beautiful-bill-act/", check=W),
    "l12": dict(pub="Tax Notes(NYSBA Tax Section)", title="NYSBA Tax Section Expresses Uneasiness With Prohibited Foreign Entity Rules(비상장 '직접 임명권' vs 상장 '임명권')", date="2026.05", url="https://www.taxnotes.com/research/federal/other-documents/irs-tax-correspondence/nysba-tax-section-expresses-uneasiness-prohibited-foreign-entity-rules/7vs78", check=W),
    "l13": dict(pub="Bracewell", title="FEOC Material Assistance Rules for Clean Energy Tax Credits(covered officer 예시: 이사·CEO·CFO)", date="2026.01.16", url="https://www.bracewell.com/resources/feoc-material-assistance-rules-clean-energy-tax-credits/", check=W),
}

OLD_C4 = "PFE = 특정외국기업(SFE) + 외국영향기업(FIE). SFE에 NDAA Sec.154 지정 6개사·국방부 1260H 목록 기업 등 포함. FIE는 SFE 단독 25% 초과 지분, 합산 40% 이상 지분, 임원 임명권, 실효적 통제 계약 등. 2026년 과세연도부터 45X 청구 불가"
NEW_C4 = ("PFE = 특정외국기업(SFE) + 외국영향기업(FIE). SFE에 NDAA Sec.154 지정 6개사·국방부 1260H 목록 기업 등 포함. "
          "FIE(비상장 기업)는 다음 중 하나에 해당: ① SFE가 covered officer(이사회 구성원·고위 임원 등) 직접 임명권 보유, ② 단일 SFE 지분 25% 이상, "
          "③ SFE 합산 지분 40% 이상, ④ 채무의 15% 이상이 SFE에 발행, ⑤ 직전 과세연도에 시설·부품에 대한 실효적 통제를 SFE에 부여하는 계약에 따라 대가 지급. "
          "상장기업은 별도 규정(임원 임명 '권한' 기준, 지분은 SEC 13d-3 신고 대상 보유분만 계산, 채무는 최초 발행분 중 상장 채무의 15% 초과). "
          "45X는 2025.07.04 이후 개시 과세연도(역년 기준 2026년)부터 SFE·FIE 청구 불가")

OLD_C7 = "2025.07.04 이후 SFE와 IP 라이선스를 체결·수정하면 실효적 통제로 간주돼 라이선시가 FIE가 될 수 있음(실효적 통제 없는 IP 매매는 예외). 세부 정의는 재무부 지침에 위임"
NEW_C7 = ("2025.07.04 이후 SFE와 체결·수정한 IP 라이선스는 그 자체로 실효적 통제로 간주. 그 이전 계약도 라이선스 제공자 등이 다음 권리 중 하나를 가지면 실효적 통제에 해당하며 각 항목은 개별 판단: "
          "부품·소재 공급원 지정, 시설·생산 운영 지시, IP 이용 제한, 10년 초과 로열티 수취, 장기 서비스 계약 요구, 독자 생산에 필요한 기술자료·노하우 미제공 등. "
          "실효적 통제가 없는 진정한 IP 매매는 예외. IRS Notice 2026-15(2026.02.12)는 잠정 지침")

OLD_C10 = "45X 배터리 부품 기준 2026년 60% → 2030년 85%, ESS(48E·45Y) 2026년 55% → 2030년 75%. IRS Notice 2026-15(2026.02.12)는 잠정 지침"
NEW_C10 = ("45X 배터리 부품(판매연도 기준): 2026년 60% → 2027년 65% → 2028년 70% → 2029년 80% → 2030년 이후 85%. "
           "독립형 ESS(에너지저장기술, 48E 투자세액공제, 착공연도 기준): 2026년 55%에서 매년 5%p 상향해 2030년 이후 75%. "
           "발전설비(45Y·48E 적격시설)는 2026년 40% → 2030년 이후 60%. IRS Notice 2026-15(2026.02.12)는 잠정 지침")

OLD_H28 = "EVE는 NDAA Sec.154 지정사, 2026.06 국방부 1260H 목록 추가 보도. 지분 10%로 외국영향기업(FIE) 지분 기준 미달이나 라이선스 '실효적 통제' 적용 여부는 미확인."
NEW_H28 = ("EVE는 NDAA Sec.154 지정사로 OBBBA상 SFE(2026.06 국방부 1260H 목록 추가는 보도 기준). EVE 지분 10%는 단독 지분 기준(25% 이상) 미달이나, "
           "이사 1석이 EVE의 직접 임명권이면 covered officer 직접 임명권 요건으로 JV가 별도로 FIE에 해당할 수 있음. "
           "주주간계약·정관상 직접 임명권인지 후보 추천권인지, 라이선스의 실효적 통제 조항 확인 필요(공개 자료로 미확인, 요건은 주요 규제 탭 참조).")

OLD_H38 = "OBBBA상 2025.07.04 이후 체결·수정된 SFE와의 IP 라이선스는 '실효적 통제'로 간주돼 45X 등 세액공제 불인정 → 신규 LRS 계약에 구조적 제약."
NEW_H38 = ("OBBBA상 2025.07.04 이후 SFE와 체결·수정한 IP 라이선스는 실효적 통제로 간주돼 라이선시가 FIE가 되고 해당 부품·시설의 45X 등 세액공제 불인정 → 신규 LRS 계약에 구조적 제약. "
           "기존 계약도 계약상 권리에 따라 실효적 통제 해당 가능(주요 규제 탭 참조).")

OLD_H42 = "2023년 계약은 OBBBA 라이선스 간주 조항(2025.07.04 이후 체결·수정분) 적용 대상이 아닌 것으로 해석, Ford는 45X 적격 기대. 상세는 Ford-CATL 탭"
NEW_H42 = ("2023년 계약이 이후 수정되지 않았다면 2025.07.04 이후 체결·수정 라이선스의 실효적 통제 간주 규정은 적용되지 않을 수 있음. "
           "다만 기존 계약도 공급원 지정·운영 지시·IP 이용 제한·장기 로열티·서비스 의존·기술자료 이전 여부 등 다른 기준 검토가 필요해 45X 적격성이 자동 보장되지는 않음(계약 조건 비공개). "
           "Ford는 45X 적격 기대(회사 입장). 상세는 Ford-CATL 탭")

OLD_C35 = "OBBBA 라이선스 간주 조항은 2025.07.04 이후 체결·수정분 대상이라 2023년 계약은 해당 없음으로 해석, Ford는 45X 적격 기대."
NEW_C35 = ("2023년 계약이 이후 수정되지 않았다면 2025.07.04 이후 체결·수정 라이선스의 실효적 통제 간주 규정은 적용되지 않을 수 있음. "
           "다만 기존 계약도 공급원 지정·운영 지시·IP 이용 제한·장기 로열티·서비스 의존·기술자료 이전 여부 등 다른 기준 검토가 필요해 45X 적격성이 자동 보장되지는 않음(계약 조건 비공개). "
           "Ford는 45X 적격 기대(회사 입장).")

OLD_D35 = "2026.01 하원 중국특위원장 서한: ESS 확대에 따른 라이선스 수정 여부·세액공제 청구 계획 질의(Ford 회신 미공개)"
NEW_D35 = OLD_D35 + ". ESS 확대가 계약 '수정'으로 판단되면 2025.07.04 이후 수정분 간주 규정 적용 여부가 쟁점(해석), CATL은 '기존 라이선스 계약의 일부'라는 입장(보도)"

OLD_H47 = "2026.01 하원 중국특위원장이 ESS 확대에 따른 라이선스 수정 여부·세액공제 청구 계획 질의(Ford 회신 미공개). 상세는 Ford-CATL 탭"
NEW_H47 = ("2026.01 하원 중국특위원장이 ESS 확대에 따른 라이선스 수정 여부·세액공제 청구 계획 질의(Ford 회신 미공개). "
           "ESS 확대가 계약 '수정'으로 판단되면 간주 규정 적용 여부가 쟁점(해석), CATL은 '기존 계약의 일부'라는 입장(보도). 상세는 Ford-CATL 탭")

OLD_TL = "OBBBA 시행: 이후 체결·수정된 SFE 라이선스는 '실효적 통제'로 간주"
NEW_TL = "OBBBA 시행: 이후 체결·수정된 SFE 라이선스는 '실효적 통제'로 간주(그 이전 계약도 공급원 지정·운영 지시 등 계약상 권리 요건에 해당하면 실효적 통제)"

TEXT_FIX2 = [(OLD_C4, NEW_C4), (OLD_C7, NEW_C7), (OLD_C10, NEW_C10), (OLD_H28, NEW_H28), (OLD_H38, NEW_H38),
             (OLD_H42, NEW_H42), (OLD_C35, NEW_C35), (OLD_H47, NEW_H47), (OLD_TL, NEW_TL)]
# D35는 C35와 같은 행의 Kentucky 열이라 정확 일치로만 교체
EXACT_FIX2 = [(OLD_D35, NEW_D35)]

ADD_POLICY = {
    "OBBBA 금지외국기업(PFE)": ["l1", "l6", "l13", "l4", "l5", "l12", "l11"],
    "OBBBA 라이선스 '실효적 통제'": ["l1", "l3", "l7", "l10"],
    "물질적 지원 비율(MACR)": ["l2", "l8", "l9"],
}
ADD_FCMP = {"규제 이슈": ["l1", "l7"]}
ADD_TL = {"2025.07.04": ["l7"]}

# 수정내역(시트, 검토의견상 셀, 구분, 기존, 수정, 사유, 근거 키, 새 셀 탐색용 문구)
CAT_ERR, CAT_LAW, CAT_KEEP = "명확한 오류", "법적 해석상 보완", "검토 후 유지"
CHANGELOG = [
    ("주요 규제", "C4(1·2번)", CAT_ERR + "·" + CAT_LAW, OLD_C4, NEW_C4,
     "① 단독 지분 기준은 법문상 'not less than 25 percent'로 '25% 초과'는 오류. ② 채무 15% 요건, ③ 직전 연도 실효적 통제 계약 대가 지급 요건, ④ 상장기업 별도 규정(임명 '권한'·13d-3 지분·최초 발행 채무 15% 초과)이 빠져 있어 보완. covered officer에 이사회 구성원 포함은 로펌 해설(Bracewell 2026.01: 이사·CEO·CFO 예시) 기준이며, 조문 원문(§7701(a)(51))은 이 환경에서 직접 열람하지 못함",
     ["l1", "l6", "l13", "l4", "l5", "l12", "l11"], "FIE(비상장 기업)는"),
    ("주요 규제", "-(연관 수정)", CAT_LAW, OLD_C7, NEW_C7,
     "2025.07.04 이후 체결·수정 라이선스의 당연 간주와, 그 이전 계약에 대한 개별 실효적 통제 요건(공급원 지정·운영 지시·IP 이용 제한·10년 초과 로열티·장기 서비스·기술자료 미제공)을 구분. Notice 2026-15는 각 요건을 개별 판단한다고 명시. 서비스 계약의 기간 요건(2년)은 법문 원문으로 확인하지 못해 '장기'로만 표기",
     ["l1", "l3", "l7", "l10"], "그 자체로 실효적 통제로 간주"),
    ("주요 규제", "C10(5번)", CAT_ERR, OLD_C10, NEW_C10,
     "독립형 ESS의 세액공제는 48E(투자세액공제)이고 45Y는 발전설비의 생산세액공제라 'ESS(48E·45Y)'는 오류. 연도별 기준을 명시(45X 배터리 2029년 80%, 2030년 이후 85% 확인)",
     ["l2", "l8", "l9", "a79"], "45X 배터리 부품(판매연도 기준)"),
    ("미국 진출 현황", "H28(3번)", CAT_LAW, OLD_H28, NEW_H28,
     "SFE의 covered officer 직접 임명권은 지분율과 별개의 FIE 판정 사유. 이사 1석만으로 FIE 확정은 불가하므로 주주간계약·정관상 임명권 성격 확인 필요로 기재(공개 자료로 미확인)",
     ["l1", "l13", "l12"], "이사 1석이 EVE의 직접 임명권이면"),
    ("미국 진출 현황", "E28(3번)", CAT_KEEP, "EVE 10%(이사 1석)", "변경 없음",
     "EVE 공시 보도(2023.09) 기준 사실이라 유지. 임명권 성격(직접 임명/추천)은 비고(H28)에 확인 필요로 기재", ["a43"], None),
    ("미국 진출 현황", "H43(4번)", CAT_LAW, OLD_H42, NEW_H42,
     "계약 체결 연도만으로 실효적 통제 심사 면제나 45X 적격이 확정되지 않음. 체결·수정일 기준(당연 간주)과 계약 내용 기준(개별 요건)을 구분하고 회사 입장을 명시",
     ["l1", "l2", "l3", "l7"], "2023년 계약이 이후 수정되지 않았다면 2025.07.04 이후 체결·수정 라이선스의 실효적 통제 간주 규정은 적용되지 않을 수 있음. 다만 기존 계약도 공급원 지정·운영 지시·IP 이용 제한·장기 로열티·서비스 의존·기술자료 이전 여부 등 다른 기준 검토가 필요해 45X 적격성이 자동 보장되지는 않음(계약 조건 비공개). Ford는 45X 적격 기대(회사 입장). 상세는"),
    ("Ford-CATL", "C35(4번)", CAT_LAW, OLD_C35, NEW_C35, "미국 진출 현황 H42와 같은 이유(동일 내용 일관 수정)", ["l1", "l7"], "2023 하원 3개 위원회 조사"),
    ("Ford-CATL", "-(연관 수정)", CAT_LAW, OLD_D35, NEW_D35,
     "ESS 확대가 2025.07.04 이후 계약 '수정'에 해당하는지가 간주 규정 적용의 쟁점이라 해석임을 명시해 추가. CATL 입장은 보도 기준", ["b16", "l7"], "ESS 확대가 계약 '수정'으로 판단되면 2025.07.04"),
    ("미국 진출 현황", "-(연관 수정)", CAT_LAW, OLD_H47, NEW_H47, "Ford-CATL D35와 일관 수정", ["b16", "l7"], "ESS 확대가 계약 '수정'으로 판단되면 간주 규정"),
    ("미국 진출 현황", "-(연관 수정)", CAT_LAW, OLD_H38, NEW_H38,
     "간주 효과(라이선시의 FIE 해당 → 해당 부품·시설 세액공제 불인정)를 정확히 하고, 기존 계약도 개별 요건 심사 대상임을 추가(동일 내용 일관 수정)", ["l1", "l7"], "라이선시가 FIE가 되고"),
    ("Ford-CATL", "-(연관 수정)", CAT_LAW, OLD_TL, NEW_TL, "동일 내용 일관 수정", ["l7"], "그 이전 계약도 공급원 지정·운영 지시 등"),
    ("주요 규제", "-(자체 점검)", CAT_KEEP, "45X는 2026년 과세연도부터 SFE·FIE 청구 불가", "표현만 정밀화(2025.07.04 이후 개시 과세연도, 역년 기준 2026년)",
     "45X의 FIE 제한 시점은 다수 해설(BPC·Tax Law Center 등)이 2025.07.04 이후 개시 과세연도로 보나, 일부 해설(Bracewell)은 2027.07.04 이후로 기재. 다수 해설 기준으로 유지했으며 법문 원문 대조가 필요함",
     ["l11", "l6"], None),
    ("출처", "-", "출처·기준시점 갱신", "-", "법령·IRS 지침·해설 출처 13건 추가(기존 S1~S153 번호 유지)",
     "법문 근거 보강. 조문 원문(law.cornell.edu)은 이 환경에서 직접 열람할 수 없어 '확인 방법' 열에 명시", [], None),
]
