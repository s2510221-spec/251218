import streamlit as st

# 1. MBTI 데이터 구성
mbti_data = {
    "ISTJ": {"jobs": ["회계사", "공무원"], "book": "원칙 (레이 달리오)"},
    "ISFJ": {"jobs": ["간호사", "사회복지사"], "book": "나의 라임 오렌지 나무 (조제 마우로 데 바스콘셀로스)"},
    "INFJ": {"jobs": ["상담심리사", "작가"], "book": "데미안 (헤르만 헤세)"},
    "INTJ": {"jobs": ["전략가", "데이터 과학자"], "book": "사피엔스 (유발 하라리)"},
    "ISTP": {"jobs": ["엔지니어", "정비사"], "book": "셜록 홈즈 (아서 코난 도일)"},
    "ISFP": {"jobs": ["예술가", "디자이너"], "book": "월든 (헨리 데이비드 소로)"},
    "INFP": {"jobs": ["예술 치료사", "사회활동가"], "book": "어린 왕자 (생텍쥐페리)"},
    "INTP": {"jobs": ["소프트웨어 개발자", "교수"], "book": "코스모스 (칼 세이건)"},
    "ESTP": {"jobs": ["기업가", "소방관"], "book": "부의 추월차선 (엠제이 드마코)"},
    "ESFP": {"jobs": ["연예인", "이벤트 플래너"], "book": "그리스인 조르바 (니코스 카잔차키스)"},
    "ENFP": {"jobs": ["홍보 전문가", "카피라이터"], "book": "연금술사 (파울로 코엘료)"},
    "ENTP": {"jobs": ["변호사", "발명가"], "book": "생각에 관한 생각 (대니얼 카너먼)"},
    "ESTJ": {"jobs": ["경영자", "프로젝트 매니저"], "book": "린 스타트업 (에릭 리스)"},
    "ESFJ": {"jobs": ["초등교사", "홍보 담당자"], "book": "데일 카네기 인간관계론 (데일 카네기)"},
    "ENFJ": {"jobs": ["교육자", "커뮤니케이션 전문가"], "book": "꽃으로도 때리지 말라 (김혜자)"},
    "ENTJ": {"jobs": ["최고경영자(CEO)", "정치인"], "book": "손자병법 (손무)"}
}

# 2. 앱 화면 구성
st.set_page_config(page_title="MBTI 진로 & 도서 추천", page_icon="📚")

st.title("✨ MBTI 맞춤 진로 & 도서 추천")
st.write("자신의 MBTI를 선택하면 가장 잘 어울리는 진로와 도서를 추천해 드립니다.")

st.divider()

# 3. 사용자 입력 (selectbox)
selected_mbti = st.selectbox(
    "당신의 MBTI는 무엇인가요?",
    options=list(mbti_data.keys()),
    index=None,
    placeholder="MBTI를 선택해주세요..."
)

# 4. 결과 출력
if selected_mbti:
    result = mbti_data[selected_mbti]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 추천 진로")
        for job in result["jobs"]:
            st.markdown(f"- **{job}**")
            
    with col2:
        st.subheader("📖 추천 도서")
        st.info(f"'{result['book']}'")

    st.success(f"{selected_mbti} 유형인 당신의 앞날을 응원합니다!")
else:
    st.info("왼쪽 박스를 클릭해 MBTI를 선택해 보세요.")

st.caption("제공되는 정보는 일반적인 성격 특성을 바탕으로 하며, 개인마다 차이가 있을 수 있습니다.")
