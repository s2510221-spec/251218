import streamlit as st
import pandas as pd
import os  # 경로 설정을 위해 필요한 기본 라이브러리

# 페이지 기본 설정
st.set_page_config(
    page_title="지난 110년 기온 변화 분석",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(filename):
    # -----------------------------------------------------------
    # [수정된 부분] 경로 문제 해결 로직
    # 현재 실행 중인 스크립트(파일)의 절대 경로를 찾습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 스크립트와 같은 폴더에 있는 파일의 전체 경로를 만듭니다.
    file_path = os.path.join(current_dir, filename)
    # -----------------------------------------------------------

    if not os.path.exists(file_path):
        st.error(f"파일을 찾을 수 없습니다. 다음 경로에 파일이 있는지 확인해주세요: {file_path}")
        return pd.DataFrame()

    try:
        # csv 파일 읽기 (한글 인코딩 대응)
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8')
        
        # 컬럼명 공백 제거
        df.columns = [c.strip() for c in df.columns]
        
        # '날짜' 컬럼 전처리
        date_col = '날짜'
        if date_col in df.columns:
            # 특수문자("\t" 등) 제거
            df[date_col] = df[date_col].astype(str).str.replace('"', '').str.replace('\t', '').str.strip()
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # 연도 컬럼 생성
        df['연도'] = df[date_col].dt.year
        
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 메인 타이틀
st.title("🌡️ 지난 110년, 정말 지구가 뜨거워졌을까?")
st.markdown("데이터 분석을 통해 실제 기온 상승 여부를 확인합니다.")

# 1. 데이터 로드 (파일 이름만 입력)
filename = 'test.csv'
df = load_data(filename)

if not df.empty:
    # 2. 데이터 분석 (연도별 평균 기온)
    df_yearly = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
    
    # 10년 이동 평균선 계산 (추세선)
    df_yearly['10년 이동평균'] = df_yearly['평균기온(℃)'].rolling(window=10).mean()

    # 3. 결과 표시
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    start_year = df_yearly['연도'].min()
    end_year = df_yearly['연도'].max()
    
    # 비교를 위해 앞쪽 10년과 뒤쪽 10년 데이터만 추출
    early_temp = df_yearly[df_yearly['연도'] < start_year + 10]['평균기온(℃)'].mean()
    recent_temp = df_yearly[df_yearly['연도'] > end_year - 10]['평균기온(℃)'].mean()
    
    # 값이 존재할 경우에만 차이 계산
    if pd.notnull(early_temp) and pd.notnull(recent_temp):
        diff = recent_temp - early_temp
        
        with col1:
            st.metric("분석 기간", f"{start_year}년 ~ {end_year}년")
        with col2:
            st.metric("초기 10년 평균기온", f"{early_temp:.1f} ℃")
        with col3:
            st.metric("최근 10년 평균기온", f"{recent_temp:.1f} ℃", delta=f"{diff:.1f} ℃ 변동")
    
    # 4. 차트 그리기
    st.divider()
    st.subheader("📈 연도별 기온 변화 추이")
    
    chart_data = df_yearly.set_index('연도')[['평균기온(℃)', '10년 이동평균']]
    st.line_chart(chart_data, color=["#CCCCCC", "#FF4B4B"]) 
    # 회색: 일반 연평균, 빨강: 10년 이동평균(추세)
    
    st.caption("회색 선은 매년의 평균 기온이고, 붉은 선은 10년 단위의 이동평균선으로 장기적인 추세를 보여줍니다.")

else:
    st.warning("데이터를 표시할 수 없습니다.")
else:
    st.warning("데이터 파일(test.csv)을 찾을 수 없거나 형식이 올바르지 않습니다.")
