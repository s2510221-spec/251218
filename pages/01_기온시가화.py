import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="지난 110년 기온 변화 분석",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(file_path):
    try:
        # csv 파일 읽기 (한글 인코딩 대응을 위해 cp949 또는 utf-8 시도)
        try:
            df = pd.read_csv(file_path, encoding='cp949')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='utf-8')
        
        # 날짜 컬럼 전처리 (csv 스니펫에 보이는 "\t1907..." 같은 특수문자 제거)
        # 컬럼명이 공백이나 특수문자로 오염되었을 수 있으므로 strip 처리
        df.columns = [c.strip() for c in df.columns]
        
        # '날짜' 컬럼 찾기
        date_col = '날짜'
        if date_col in df.columns:
            # 문자열로 변환 후 불필요한 기호 제거
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
st.markdown("업로드된 기상 데이터를 분석하여 실제로 기온이 상승하고 있는지 확인합니다.")

# 1. 데이터 로드
filename = 'test.csv'
df = load_data(filename)

if not df.empty:
    # 2. 데이터 분석 (연도별 평균 기온 계산)
    # 결측치 제외하고 연도별로 그룹화
    df_yearly = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
    
    # 10년 이동 평균선 계산 (장기 추세 확인용)
    df_yearly['10년 이동평균'] = df_yearly['평균기온(℃)'].rolling(window=10).mean()

    # 3. 주요 지표 표시 (Metric)
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    # 데이터 시작/종료 연도 확인
    start_year = df_yearly['연도'].min()
    end_year = df_yearly['연도'].max()
    
    # 초기 10년 vs 최근 10년 평균 기온 비교
    early_temp = df_yearly[df_yearly['연도'] < start_year + 10]['평균기온(℃)'].mean()
    recent_temp = df_yearly[df_yearly['연도'] > end_year - 10]['평균기온(℃)'].mean()
    diff = recent_temp - early_temp

    with col1:
        st.metric(label=f"데이터 기간", value=f"{start_year}년 ~ {end_year}년")
    with col2:
        st.metric(label=f"초기 10년 평균기온", value=f"{early_temp:.1f} ℃")
    with col3:
        st.metric(label=f"최근 10년 평균기온", value=f"{recent_temp:.1f} ℃", delta=f"{diff:.1f} ℃ 상승")

    # 4. 시각화 (라인 차트)
    st.divider()
    st.subheader(f"📈 {start_year}~{end_year} 연도별 평균 기온 추이")
    
    # 차트를 그리기 위해 연도를 인덱스로 설정
    chart_data = df_yearly.set_index('연도')[['평균기온(℃)', '10년 이동평균']]
    
    # 스트림릿 내장 라인 차트 사용 (반응형)
    st.line_chart(
        chart_data,
        color=["#FF0000", "#0000FF"], # 빨강(평균), 파랑(이동평균) - 테마에 따라 자동 조정될 수 있음
        use_container_width=True
    )
    
    st.caption("파란선(또는 옅은 색)은 해당 연도의 평균기온이며, 굵은 선은 기후 변화 추세를 보기 쉽게 10년 단위로 부드럽게 만든 이동평균선입니다.")

    # 5. 원본 데이터 확인 (옵션)
    with st.expander("원본 데이터 및 연도별 통계 보기"):
        st.dataframe(df_yearly)

else:
    st.warning("데이터 파일(test.csv)을 찾을 수 없거나 형식이 올바르지 않습니다.")
