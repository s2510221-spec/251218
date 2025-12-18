import streamlit as st

# 1. MBTI별 포켓몬 데이터 (이름, 이미지ID, 이유)
# 이미지는 PokeAPI의 공식 아트워크 URL을 사용합니다.
pokemon_data = {
    "ISTJ": {"name": "거북왕 (Blastoise)", "id": 9, "reason": "책임감이 강하고 원칙을 중요시합니다. 묵묵히 팀을 지탱하는 든든한 방패 같은 존재입니다."},
    "ISFJ": {"name": "럭키 (Chansey)", "id": 113, "reason": "타인을 돕는 것을 좋아하고 헌신적입니다. 팀의 체력을 책임지는 치유의 아이콘입니다."},
    "INFJ": {"name": "가디안 (Gardevoir)", "id": 282, "reason": "통찰력이 뛰어나고 타인의 감정을 잘 읽습니다. 신비롭고 미래를 내다보는 힘을 가졌습니다."},
    "INTJ": {"name": "뮤츠 (Mewtwo)", "id": 150, "reason": "전략적이고 독립적입니다. 엄청난 잠재력과 지능을 가지고 혼자서도 세상을 바꿀 힘이 있습니다."},
    "ISTP": {"name": "개굴닌자 (Greninja)", "id": 658, "reason": "효율적이고 상황 판단이 빠릅니다. 말이 길지 않고 행동으로 보여주는 쿨한 해결사입니다."},
    "ISFP": {"name": "이브이 (Eevee)", "id": 133, "reason": "자유로운 영혼을 가졌습니다. 어떤 환경이든 자신만의 색깔로 적응하고 진화할 수 있는 가능성이 있습니다."},
    "INFP": {"name": "뮤 (Mew)", "id": 151, "reason": "이상적이고 순수합니다. 좀처럼 모습을 드러내지 않지만, 깊은 내면에 따뜻한 마음을 품고 있습니다."},
    "INTP": {"name": "후딘 (Alakazam)", "id": 65, "reason": "논리적이고 분석적입니다. 끊임없이 생각하고 연구하며 지식을 탐구하는 지성파입니다."},
    "ESTP": {"name": "리자몽 (Charizard)", "id": 6, "reason": "에너지가 넘치고 모험을 즐깁니다. 도전적인 상황에서 더욱 불타오르는 열정의 소유자입니다."},
    "ESFP": {"name": "푸린 (Jigglypuff)", "id": 39, "reason": "관심받는 것을 좋아하고 사교적입니다. 어디서든 노래하며 분위기를 띄우는 타고난 스타입니다."},
    "ENFP": {"name": "피카츄 (Pikachu)", "id": 25, "reason": "열정적이고 친화력이 좋습니다. 누구와도 금방 친구가 되며 주변에 긍정적인 전기를 퍼뜨립니다."},
    "ENTP": {"name": "팬텀 (Gengar)", "id": 94, "reason": "장난기가 많고 창의적입니다. 남들이 생각지 못한 방법으로 문제를 해결(또는 장난)하는 재주가 있습니다."},
    "ESTJ": {"name": "망나뇽 (Dragonite)", "id": 149, "reason": "질서를 중요시하고 리더십이 있습니다. 겉은 온순해 보이지만 목표를 위해서는 강력한 힘을 발휘합니다."},
    "ESFJ": {"name": "캥카 (Kangaskhan)", "id": 115, "reason": "동료애가 깊고 보살피는 것을 좋아합니다. 내 사람을 건드리면 무섭게 변하는 든든한 보호자입니다."},
    "ENFJ": {"name": "루카리오 (Lucario)", "id": 448, "reason": "카리스마가 있고 정의롭습니다. 타인의 파동(감정)을 읽고 올바른 길로 이끄는 리더입니다."},
    "ENTJ": {"name": "메타그로스 (Metagross)", "id": 376, "reason": "철저하고 계획적입니다. 네 개의 뇌로 슈퍼컴퓨터처럼 계산하여 반드시 승리를 쟁취합니다."}
}

# 2. 페이지 기본 설정
st.set_page_config(page_title="MBTI 포켓몬 도감", page_icon="🐾")

# 3. 헤더 영역
st.title("🐾 나의 MBTI 포켓몬 찾기")
st.markdown("당신의 **MBTI** 성향과 가장 닮은 **포켓몬**은 누구일까요?")
st.divider()

# 4. 사용자 입력
col1, col2 = st.columns([1, 2])
with col1:
    st.write("### 👇 MBTI 선택")
    selected_mbti = st.selectbox(
        "본인의 MBTI를 선택해주세요:",
        options=list(pokemon_data.keys()),
        index=None,
        placeholder="Select MBTI..."
    )

# 5. 결과 출력 영역
if selected_mbti:
    data = pokemon_data[selected_mbti]
    
    # 이미지 URL 생성 (PokeAPI 공식 아트워크 사용)
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{data['id']}.png"
    
    st.subheader(f"당신은... {data['name']} 타입!")
    
    # 화면 분할 (이미지와 설명)
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.image(image_url, caption=data['name'], use_column_width=True)
        
    with res_col2:
        st.success("매칭 이유")
        st.write(f"**{data['reason']}**")
        st.info("이 포켓몬은 당신의 성격적 특성을 아주 잘 반영하고 있답니다!")

else:
    # 선택 전 대기 화면
    st.info("👈 왼쪽에서 MBTI를 선택하면 결과가 나타납니다!")

# 6. 푸터
st.divider()
st.caption("※ 재미로 보는 테스트입니다. 포켓몬 이미지는 PokeAPI를 활용했습니다.")
