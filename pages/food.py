import streamlit as st
import random

# 1. 데이터 구성 (기분: {음식명, 이미지URL, 설명})
# 안정적인 이미지 로딩을 위해 Unsplash 및 검증된 URL로 교체했습니다.
food_data = {
    "우울해요 ☁️": {
        "menu": "달콤한 초콜릿 케이크",
        "img": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=80",
        "desc": "기분이 다운될 때는 당 충전이 최고! 달콤한 초콜릿은 일시적으로 기분을 좋게 만드는 엔도르핀 생성을 도와줍니다. 진한 케이크 한 조각으로 우울함을 녹여보세요."
    },
    "화가 나요 🔥": {
        "menu": "매운 마라탕 & 떡볶이",
        "img": "https://images.unsplash.com/photo-1553603227-2358e57564a3?auto=format&fit=crop&w=800&q=80",
        "desc": "스트레스엔 매운맛! 캡사이신 성분은 뇌를 자극해 스트레스를 해소하는 데 도움을 줍니다. 화끈하게 땀을 흘리며 답답한 속을 뻥 뚫어보세요."
    },
    "행복해요 🎉": {
        "menu": "바삭한 치킨 & 맥주",
        "img": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=800&q=80",
        "desc": "기쁜 날엔 역시 치느님! 바삭한 튀김 옷과 부드러운 속살은 행복을 두 배로 만들어 줍니다. 사랑하는 사람들과 함께 나누기에 이보다 완벽한 메뉴는 없죠."
    },
    "피곤해요 🔋": {
        "menu": "따뜻한 삼계탕(닭백숙)",
        "img": "https://images.unsplash.com/photo-1548943487-a2e4e43b485c?auto=format&fit=crop&w=800&q=80",
        "desc": "지친 몸에는 보양식이 필요해요. 따뜻한 국물과 단백질이 풍부한 닭고기는 원기 회복에 탁월합니다. 든든하게 속을 채우고 에너지를 충전하세요."
    },
    "심심해요 🥱": {
        "menu": "수제 버거 & 감자튀김",
        "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
        "desc": "지루할 땐 입안 가득 꽉 차는 다채로운 맛이 필요해요! 육즙 가득한 패티와 신선한 야채의 조화는 무료한 일상에 즐거운 자극이 될 거예요."
    },
    "불안해요 😟": {
        "menu": "따뜻한 차 & 샌드위치",
        "img": "https://images.unsplash.com/photo-1528740561666-dc2479dc08ab?auto=format&fit=crop&w=800&q=80",
        "desc": "마음을 차분하게 해주는 따뜻한 차 한 잔과 소화가 잘 되는 가벼운 샌드위치를 드세요. 긴장된 몸과 마음을 이완시키는 데 도움을 줄 거예요."
    }
}

# 2. 페이지 기본 설정
st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍽️")

# 3. 타이틀 및 헤더
st.title("🍽️ 기분에 따른 메뉴 추천")
st.markdown("지금 당신의 **기분**을 알려주세요. 딱 맞는 **음식**을 골라드릴게요!")
st.divider()

# 4. 사용자 입력 (라디오 버튼)
mood_list = list(food_data.keys())
selected_mood = st.radio("현재 기분은 어떤가요?", mood_list, index=None, horizontal=True)

st.write("") # 여백

# 5. 결과 출력
if selected_mood:
    recommendation = food_data[selected_mood]
    
    with st.container():
        st.subheader(f"👉 추천 메뉴: {recommendation['menu']}")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            # 이미지 출력 (에러 방지용 설정 추가 없음, URL 자체를 안정적인 것으로 교체함)
            st.image(recommendation['img'], caption=recommendation['menu'], use_column_width=True)
            
        with col2:
            st.info("💡 **추천 이유**")
            st.write(recommendation['desc'])
            
            cheer_msg = ["맛있게 드세요!", "오늘 하루도 파이팅!", "먹는 게 남는 거예요!", "다이어트는 내일부터!"]
            st.success(f"🗣️ {random.choice(cheer_msg)}")

else:
    st.info("위에서 기분을 선택하면 맛있는 음식이 나타납니다! 👆")

# 6. 푸터
st.divider()
st.caption("※ 이 앱은 별도의 설치 없이 Streamlit Cloud에서 바로 실행됩니다.")
