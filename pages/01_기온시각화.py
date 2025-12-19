import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="기온 변화 분석",
    page_icon="🌡️",
    layout="wide"
)

# 2. 데이터 로드 함수
@st.cache_data
def load_data(filename):
    # 현재 파일의 위치를 기준으로 데이터 파일 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)

    # 파일 존재 여부 확인 (디버깅용 로그 포함)
    if not os.path.exists(file_path):
        st.error(f"❌ 파일을 찾을 수 없습니다.")
        st.code(f"찾는 위치: {file_path}")
        return pd.DataFrame()

    try:
        # 인코딩 문제 방지를 위한 예외 처리
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8')

        # 컬럼명 공백 정리
        df.columns = [c.strip() for c in df.columns]

        # 날짜 컬럼 처리
        if '날짜' in df.columns:
            # 특수문자 제거 및 날짜 변환
            df['날짜'] = df['날짜'].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
            df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
            df['연도'] = df['날짜'].dt.year
            return df
        else:
            st.error("CSV 파일에 '날짜' 컬럼이 없습니다.")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"데이터 로드 중 오류: {e}")
        return pd.DataFrame()

# 3. 메인 화면 구성
st.title("🌡️ 지난 110년 기온 변화 시각화")
st.markdown("데이터를 분석하여 온난화 경향을 확인합니다.")

# 데이터 불러오기
target_file = 'test.csv'
df = load_data(target_file)

# --- [중요] if-else 구조가 명확해야 합니다 ---
if not df.empty:
    # (1) 데이터 가공
    df_yearly = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
    df_yearly['10년 이동평균'] = df_yearly['평균기온(℃)'].rolling(window=10).mean()

    # (2) 주요 지표 계산
    start_year = df_yearly['연도'].min()
    end_year = df_yearly['연도'].max()
    
    early_temp = df_yearly[df_yearly['연도'] < start_year + 10]['평균기온(℃)'].mean()
    recent_temp = df_yearly[df_yearly['연도'] > end_year - 10]['평균기온(℃)'].mean()

    # (3) 지표 출력
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("분석 기간", f"{start_year} ~ {end_year}년")
    
    if pd.notnull(early_temp) and pd.notnull(recent_temp):
        diff = recent_temp - early_temp
        c2.metric("과거 10년 평균", f"{early_temp:.1f} ℃")
        c3.metric("최근 10년 평균", f"{recent_temp:.1f} ℃", delta=f"{diff:.1f} ℃ 변동")

    # (4) 차트 출력
    st.divider()
    st.subheader("📈 연도별 평균 기온과 추세선")
    
    # 차트 데이터 준비
    chart_data = df_yearly.set_index('연도')[['평균기온(℃)', '10년 이동평균']]
    
    # 색상 지정하여 라인 차트 그리기
    st.line_chart(chart_data, color=["#DDDDDD", "#FF0000"])
    
    st.caption("회색: 연평균 기온 / 빨강: 10년 이동평균(추세)")

else:
    # [중요] 이 else는 위쪽의 if not df.empty와 줄이 맞아야 합니다.
    st.warning("데이터를 불러오지 못했습니다. 파일 위치를 확인해주세요.")
