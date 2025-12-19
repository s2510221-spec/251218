import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# -----------------------------------------------------------------------------
# [중요] 페이지 설정은 그 어떤 코드보다 가장 먼저 실행되어야 합니다.
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Global MBTI Analysis", 
    layout="wide"
)

# -----------------------------------------------------------------------------
# 1. 설정 및 데이터 로드 함수
# -----------------------------------------------------------------------------
# 시각화 스타일 설정 (한글 폰트 깨짐 방지 위해 영문 스타일 사용)
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
    # 파일 경로는 현재 파일의 위치에 따라 상대적으로 설정해야 할 수 있습니다.
    # 같은 폴더에 있다고 가정합니다.
    file_path = "mbti_data.csv" 
    
    # 만약 pages 폴더 안에 있다면 상위 폴더를 참조해야 할 수도 있으니 확인 필요
    # 여기서는 같은 폴더 혹은 실행 위치 기준을 우선합니다.
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Country 컬럼이 있는지 확인
            if "Country" not in df.columns:
                return create_mock_data()
            return df
        except Exception:
            return create_mock_data()
    else:
        # 파일이 없으면 더미 데이터 반환
        return create_mock_data()

# 데이터 로드 실행
df = load_data()

# MBTI 컬럼 리스트 추출 (Country 제외)
mbti_cols = [col for col in df.columns if col != "Country"]

# -----------------------------------------------------------------------------
# 2. 메인 화면 구성
# -----------------------------------------------------------------------------
st.title("🌏 국가별 MBTI 성향 분석")
st.markdown("전 세계 국가의 MBTI 분포와 한국의 위치를 비교 분석합니다.")

# 데이터가 Mock Data인지 확인하여 안내 (선택적)
if not os.path.exists("mbti_data.csv"):
    st.info("💡 CSV 데이터가 감지되지 않아 **테스트용 데이터**로 실행 중입니다.")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 전체 국가 평균", "🔍 국가별 상세 분석", "🏆 유형별 순위 & 한국 비교"])

# --- Tab 1: 전체 평균 ---
with tab1:
    st.header("전체 국가 MBTI 평균 비율")
    if not mbti_cols:
        st.error("데이터에 MBTI 컬럼이 없습니다.")
    else:
        avg_mbti = df[mbti_cols].mean().sort_values(ascending=False)
        avg_df = avg_mbti.reset_index()
        avg_df.columns = ['MBTI', 'Average Percentage']

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='MBTI', y='Average Percentage', data=avg_df, palette="viridis", ax=ax)
        ax.set_title("Global Average MBTI Distribution")
        ax.set_ylabel("Percentage (%)")
        st.pyplot(fig)

# --- Tab 2: 국가별 분석 ---
with tab2:
    st.header("국가별 MBTI 구성 비율")
    col1, col2 = st.columns([1, 3])
    
    with col1:
        selected_country = st.selectbox("분석할 국가를 선택하세요:", df['Country'].unique())
    
    # 선택 국가 데이터 필터링
    country_data = df[df['Country'] == selected_country][mbti_cols].T
    country_data.columns = ['Percentage']
    country_data = country_data.sort_values(by='Percentage', ascending=False)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=country_data.index, y='Percentage', data=country_data, palette="coolwarm", ax=ax)
        ax.set_title(f"MBTI Distribution in {selected_country}")
        st.pyplot(fig)

# --- Tab 3: 순위 및 한국 비교 ---
with tab3:
    st.header("유형별 국가 순위 TOP 10 & 한국 비교")
    target_mbti = st.selectbox("비교할 MBTI 유형을 선택하세요:", mbti_cols)
    
    sorted_df = df.sort_values(by=target_mbti, ascending=False).reset_index(drop=True)
    top_10 = sorted_df.head(10).copy()
    
    # 한국 데이터 찾기 (대소문자 무관)
    korea_row = df[df['Country'].str.contains("Korea", case=False, na=False)]
    
    plot_data = top_10.copy()
    korea_name = "South Korea"
    
    # 한국 데이터가 있고, TOP 10에 없다면 그래프에 추가
    if not korea_row.empty:
        korea_name = korea_row.iloc[0]['Country']
        if korea_name not in top_10['Country'].values:
            korea_data = korea_row.iloc[[0]].copy()
            plot_data = pd.concat([top_10, korea_data])
            
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 한국만 다른 색으로 표시
    colors = ['lightgrey'] * len(plot_data)
    countries_list = plot_data['Country'].tolist()
    
    if korea_name in countries_list:
        try:
            korea_idx = countries_list.index(korea_name)
            colors[korea_idx] = 'salmon'
        except ValueError:
            pass

    sns.barplot(x=target_mbti, y='Country', data=plot_data, palette=colors, ax=ax)
    ax.set_title(f"Top Countries for {target_mbti}")
    
    # 막대 옆에 숫자 표시
    for i, v in enumerate(plot_data[target_mbti]):
        ax.text(v + 0.1, i, f"{v:.1f}%", va='center', fontsize=10)
        
    st.pyplot(fig)
