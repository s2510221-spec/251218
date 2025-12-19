import streamlit as st
import pandas as pd
import numpy as np
import os

# 페이지 설정
st.set_page_config(
    page_title="110년 기온 변화 분석",
    page_icon="🌡️",
    layout="wide"
)

# ---------------------------------------------------------
# 1. 데이터 로드 및 전처리 함수
# ---------------------------------------------------------
@st.cache_data
def load_and_process_data(filename):
    # 현재 파일(app.py)과 같은 위치에서 데이터 찾기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    if not os.path.exists(file_path):
        return None, f"파일을 찾을 수 없습니다: {filename}"

    try:
        # 1. 파일 읽기 (인코딩 자동 감지 시도)
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8')

        # 2. 컬럼명 공백 제거
        df.columns = [c.strip() for c in df.columns]

        # 3. 날짜 컬럼 전처리 (핵심: 특수문자 제거)
        # 데이터에 "\t1907..." 처럼 탭과 따옴표가 섞여 있어 이를 제거합니다.
        if '날짜' in df.columns:
            df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
            df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
            
            # 연도 추출
            df['연도'] = df['날짜'].dt.year
            
            # 결측치(NaN)가 있는 행 제거
            df = df.dropna(subset=['평균기온(℃)', '연도'])
            
            return df, None
        else:
            return None, "CSV 파일에 '날짜' 컬럼이 없습니다."

    except Exception as e:
        return None, f"데이터 처리 중 오류 발생: {e}"

# ---------------------------------------------------------
# 2. 메인 앱 로직
# ---------------------------------------------------------
st.title("🌏 지난 110년, 기온은 얼마나 올랐을까?")
st.markdown("업로드된 기상 데이터를 분석하여 **장기적인 온난화 경향**을 검증합니다.")

file_name = 'test.csv'
df, error_msg = load_and_process_data(file_name)

if error_msg:
    st.error(error_msg)
    st.info("데이터 파일(test.csv)이 app.py와 같은 폴더에 있는지 확인해주세요.")

elif df is not None:
    # --- 분석 시작 ---
    
    # 1. 연도별 평균 기온 계산
    df_yearly = df.groupby('연도')['평균기온(℃)'].mean().reset_index()

    # 2. 추세선(Trend Line) 계산 - 선형 회귀 (Polyfit)
    # x: 연도, y: 평균기온
    x = df_yearly['연도']
    y = df_yearly['평균기온(℃)']
    
    # 1차 방정식 (y = ax + b) 계수 구하기
    slope, intercept = np.polyfit(x, y, 1)
    
    # 추세선 데이터 생성
    df_yearly['추세선'] = slope * x + intercept

    # --- 결과 시각화 ---

    # 1. 텍스트 지표 (Metric)
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    total_years = df_yearly['연도'].max() - df_yearly['연도'].min()
    temp_change = df_yearly['추세선'].iloc[-1] - df_yearly['추세선'].iloc[0]
    
    trend_emoji = "🔥" if slope > 0 else "❄️"
    trend_text = "상승 중" if slope > 0 else "하강 중"

    with col1:
        st.metric("분석 기간", f"{total_years}년 ({df_yearly['연도'].min()} ~ {df_yearly['연도'].max()})")
    
    with col2:
        st.metric("110년간 기온 변화 (추세 기준)", f"{temp_change:.2f} ℃ {trend_emoji}")
        
    with col3:
        st.metric("연평균 상승률", f"{slope:.4f} ℃/년", f"{trend_text}")

    # 2. 그래프 그리기
    st.subheader("📈 연도별 평균 기온과 상승 추세")
    
    # 차트용 데이터 정리 (인덱스를 연도로 설정)
    chart_data = df_yearly.set_index('연도')[['평균기온(℃)', '추세선']]
    
    # 라인 차트
    # 파란색: 실제 연평균 기온 / 빨간색: 추세선
    st.line_chart(chart_data, color=["#87CEFA", "#FF4500"])
    
    st.caption(f"""
    - **하늘색 선**: 매년 실제 관측된 평균 기온입니다. (변동이 심함)
    - **주황색 선**: 통계적으로 계산된 추세선입니다. 
    - 분석 결과, 지난 {total_years}년 동안 기온은 약 **{temp_change:.1f}도** {trend_text}이 확인됩니다.
    """)

    # 3. 데이터 보기 (접기/펴기)
    with st.expander("📊 연도별 상세 데이터 보기"):
        st.dataframe(df_yearly.style.format("{:.2f}"))
