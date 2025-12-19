import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# -----------------------------------------------------------------------------
# 1. 설정 및 데이터 로드
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Global MBTI Analysis", layout="wide")

# 한글 폰트 문제 방지를 위해 시각화 스타일 설정 (영어 기반으로 깔끔하게)
sns.set_theme(style="whitegrid")

def create_mock_data():
    """데이터 파일이 없을 경우 테스트를 위한 더미 데이터를 생성합니다."""
    countries = [
        "South Korea", "United States", "Japan", "China", "Germany", "France", 
        "United Kingdom", "Canada", "Brazil", "Australia", "India", "Russia", 
        "Italy", "Spain", "Mexico"
    ]
    mbti_types = [
        "ISTJ", "ISFJ", "INFJ", "INTJ", 
        "ISTP", "ISFP", "INFP", "INTP", 
        "ESTP", "ESFP", "ENFP", "ENTP", 
        "ESTJ", "ESFJ", "ENFJ", "ENTJ"
    ]
    
    data = []
    for country in countries:
        # 국가별로 랜덤 비율 생성 (합이 100이 되도록 정규화)
        values = np.random.rand(16)
        values = (values / values.sum()) * 100
        row = {"Country": country}
        for mbti, val in zip(mbti_types, values):
            row[mbti] = round(val, 2)
        data.append(row)
        
    return pd.DataFrame(data)

@st.cache_data
def load_data():
    file_path = "mbti_data.csv"
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Country 컬럼이 있는지 확인
            if "Country" not in df.columns:
                st.error("CSV 파일에 'Country' 컬럼이 필요합니다.")
                return create_mock_data()
            return df
        except Exception as e:
            st.warning(f"데이터 로드 중 오류 발생: {e}. 테스트 데이터를 사용합니다.")
            return create_mock_data()
    else:
        # 파일이 없으면 더미 데이터 생성 및 알림
        st.info("업로드된 'mbti_data.csv' 파일이 없어 테스트용 데이터를 생성하여 보여줍니다.")
        return create_mock_data()

df = load_data()

# MBTI 컬럼 리스트 (Country 제외)
mbti_cols = [col for col in df.columns if col != "Country"]

# -----------------------------------------------------------------------------
# 2. 메인 화면 구성
# -----------------------------------------------------------------------------
st.title("🌏 국가별 MBTI 성향 분석 대시보드")
st.markdown("전 세계 국가의 MBTI 분포와 한국의 위치를 비교 분석합니다.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 전체 국가 평균", "🔍 국가별 상세 분석", "🏆 유형별 순위 & 한국 비교"])

# -----------------------------------------------------------------------------
# Tab 1: 전체 국가 MBTI 평균 비율
# -----------------------------------------------------------------------------
with tab1:
    st.header("전체 국가 MBTI 평균 비율")
    
    # 평균 계산
    avg_mbti = df[mbti_cols].mean().sort_values(ascending=False)
    
    # 데이터프레임 변환
    avg_df = avg_mbti.reset_index()
    avg_df.columns = ['MBTI', 'Average Percentage']

    # 시각화
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='MBTI', y='Average Percentage', data=avg_df, palette="viridis", ax=ax)
    ax.set_title("Global Average MBTI Distribution")
    ax.set_ylabel("Percentage (%)")
    st.pyplot(fig)

    st.dataframe(avg_df.T, use_container_width=True)

# -----------------------------------------------------------------------------
# Tab 2: 국가별 MBTI 성향 분석
# -----------------------------------------------------------------------------
with tab2:
    st.header("국가별 MBTI 구성 비율")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_country = st.selectbox("분석할 국가를 선택하세요:", df['Country'].unique())
    
    # 선택된 국가 데이터 필터링
    country_data = df[df['Country'] == selected_country][mbti_cols].T
    country_data.columns = ['Percentage']
    country_data = country_data.sort_values(by='Percentage', ascending=False)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=country_data.index, y='Percentage', data=country_data, palette="coolwarm", ax=ax)
        ax.set_title(f"MBTI Distribution in {selected_country}")
        ax.set_ylabel("Percentage (%)")
        st.pyplot(fig)
        
    # E/I, N/S, T/F, J/P 경향성 간단 분석
    st.subheader(f"📌 {selected_country}의 주요 성향")
    top_3 = country_data.head(3).index.tolist()
    st.write(f"가장 많은 유형 TOP 3: **{', '.join(top_3)}**")

# -----------------------------------------------------------------------------
# Tab 3: MBTI 유형별 높은 국가 TOP 10 & 한국 비교
# -----------------------------------------------------------------------------
with tab3:
    st.header("유형별 국가 순위 TOP 10 & 한국 위치")
    
    target_mbti = st.selectbox("비교할 MBTI 유형을 선택하세요:", mbti_cols)
    
    # 데이터 정렬 및 Top 10 추출
    sorted_df = df.sort_values(by=target_mbti, ascending=False).reset_index(drop=True)
    top_10 = sorted_df.head(10).copy()
    
    # 한국 데이터 찾기 (대소문자 구분 없이 검색)
    korea_row = df[df['Country'].str.contains("Korea", case=False, na=False)]
    
    plot_data = top_10.copy()
    korea_included_in_top10 = False
    
    # 한국 데이터가 존재하면 처리
    korea_val = 0
    korea_name = "South Korea"
    
    if not korea_row.empty:
        korea_name = korea_row.iloc[0]['Country']
        korea_val = korea_row.iloc[0][target_mbti]
        
        # 한국이 Top 10에 이미 있는지 확인
        if korea_name in top_10['Country'].values:
            korea_included_in_top10 = True
        else:
            # Top 10에 없으면 추가해서 시각화 (11번째 바)
            korea_data = korea_row.iloc[[0]].copy()
            plot_data = pd.concat([top_10, korea_data])
    
    # 시각화 설정
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 색상 설정 (기본 회색, 한국은 빨간색 강조)
    colors = ['lightgrey'] * len(plot_data)
    countries_list = plot_data['Country'].tolist()
    
    try:
        korea_idx = countries_list.index(korea_name)
        colors[korea_idx] = 'salmon' # 한국 강조 색상
    except ValueError:
        pass # 한국 데이터가 아예 없는 경우 패스

    sns.barplot(
        x=target_mbti, 
        y='Country', 
        data=plot_data, 
        palette=colors, 
        ax=ax
    )
    
    # 그래프 꾸미기
    ax.set_title(f"Top Countries for {target_mbti} (vs Korea)")
    ax.set_xlabel("Percentage (%)")
    
    # 막대 옆에 수치 표시
    for i, v in enumerate(plot_data[target_mbti]):
        ax.text(v + 0.1, i, f"{v:.1f}%", va='center', fontsize=10)

    st.pyplot(fig)

    if not korea_row.empty:
        rank = sorted_df[sorted_df['Country'] == korea_name].index[0] + 1
        st.info(f"🇰🇷 **{korea_name}**의 **{target_mbti}** 비율은 **{korea_val:.1f}%**로, 전체 **{len(df)}개국 중 {rank}위**입니다.")
    else:
        st.warning("데이터에서 'Korea'를 찾을 수 없습니다.")
