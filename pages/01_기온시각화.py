import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="기온 변화 대시보드",
    page_icon="🌡️",
    layout="wide"
)

# 2. 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    if not os.path.exists(file_path):
        return None, f"파일을 찾을 수 없습니다: {filename}"

    try:
        # 파일 읽기
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8')

        # 컬럼명 공백 제거
        df.columns = [c.strip() for c in df.columns]

        # 날짜 컬럼 전처리
        if '날짜' in df.columns:
            df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
            df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
            df['연도'] = df['날짜'].dt.year
        else:
            return None, "CSV 파일에 '날짜' 컬럼이 없습니다."

        # [핵심 수정] 기온 컬럼 데이터 전처리 강화
        # 1. 혹시 문자로 되어있을 수 있으니 강제로 숫자로 변환 (에러나면 NaN 처리)
        if '평균기온(℃)' in df.columns:
            df['평균기온(℃)'] = pd.to_numeric(df['평균기온(℃)'], errors='coerce')
            
            # 2. 기온 데이터가 비어있는(NaN) 행은 삭제 (이게 없으면 nan 뜸)
            df = df.dropna(subset=['평균기온(℃)', '연도'])
        else:
            return None, "CSV 파일에 '평균기온(℃)' 컬럼이 없습니다."

        return df, None
            
    except Exception as e:
        return None, f"오류 발생: {e}"

# 3. 메인 앱 화면
st.title("🌡️ 지난 110년, 기온은 실제로 상승했을까?")
st.markdown("데이터를 분석하여 **연도별 기온 변화**와 **장기적인 추세**를 Plotly 그래프로 확인합니다.")

# 데이터 로드
df, error = load_data('test.csv')

if error:
    st.error(error)
elif df is not None:
    # --- 데이터 분석 ---
    
    # 1. 연도별 평균 기온 구하기
    df_yearly = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
    
    # [안전 장치] 연도별 평균에서도 혹시 모를 NaN 제거
    df_yearly = df_yearly.dropna()

    # 데이터가 충분한지 확인
    if len(df_yearly) > 1:
        # 2. 추세선(Trend Line) 계산
        x = df_yearly['연도']
        y = df_yearly['평균기온(℃)']
        
        # 1차 방정식 계수 산출 (여기서 NaN이 있으면 에러남 -> 위에서 처리 완료)
        slope, intercept = np.polyfit(x, y, 1)
        
        # 추세선 값 생성
        df_yearly['추세선'] = slope * x + intercept
        
        # --- 상단 지표 (Metric) ---
        st.divider()
        col1, col2, col3 = st.columns(3)
        
        start_year = df_yearly['연도'].min()
        end_year = df_yearly['연도'].max()
        total_change = df_yearly['추세선'].iloc[-1] - df_yearly['추세선'].iloc[0]
        
        col1.metric("분석 기간", f"{start_year}년 ~ {end_year}년")
        col2.metric("110년간 기온 상승폭", f"{total_change:.2f} ℃")
        
        # nan이 뜨던 곳 해결
        col3.metric("연평균 상승률", f"{slope:.4f} ℃/년")

        # --- Plotly 시각화 ---
        st.divider()
        st.subheader("📈 인터랙티브 기온 그래프 (Plotly)")

        # 그래프 그리기
        fig = px.line(df_yearly, x='연도', y='평균기온(℃)', title='연도별 평균 기온 vs 온난화 추세선')
        
        fig.update_traces(line=dict(color='lightgray', width=2), name='실제 연평균 기온')
        
        fig.add_trace(go.Scatter(
            x=df_yearly['연도'], 
            y=df_yearly['추세선'],
            mode='lines',
            name='온난화 추세선',
            line=dict(color='red', width=3, dash='dot')
        ))

        fig.update_layout(
            hovermode="x unified",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            xaxis_title="연도",
            yaxis_title="기온 (℃)"
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("데이터 자세히 보기"):
            st.dataframe(df_yearly)
            
    else:
        st.warning("분석할 데이터가 충분하지 않습니다. (2년 이상의 데이터 필요)")
