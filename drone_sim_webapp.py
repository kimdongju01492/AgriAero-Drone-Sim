
import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
import glob
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from drone_simulation import generate_fine_zigzag_path, simulate_dual_drones, generate_report, DroneAgent, get_simulated_weather, run_simulations_for_learning
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="AgriAero 드론 시뮬레이터", layout="wide", page_icon="🛰️")

st.title("🛰️ AgriAero 스마트 드론 시뮬레이션 (AI 판단 포함)")

st.sidebar.header("⚙️ 시뮬레이션 설정")
battery = st.sidebar.slider("🔋 초기 배터리 (%)", 50, 100, 100)
spray = st.sidebar.slider("💧 초기 살포량 (L)", 10, 30, 30)
st.sidebar.markdown("---")
run_ai = st.sidebar.button("🚀 AI 자율 시뮬레이션 실행")
run_batch = st.sidebar.button("🧠 100회 학습용 시뮬레이션 실행")

# 앱 패키징 관련 힌트 출력
with st.expander("💡 실행 파일(.exe)로 패키징하는 방법"):
    st.markdown("""
    - 1️⃣ 먼저 `pyinstaller`를 설치하세요: `pip install pyinstaller`
    - 2️⃣ 터미널에 다음을 입력하세요:
      ```bash
      pyinstaller --onefile --add-data "./drone_simulation.py;." drone_sim_webapp.py
      ```
    - 3️⃣ 실행 파일은 `/dist/drone_sim_webapp.exe`로 생성됩니다.
    - 📦 완성된 `.exe`는 다른 컴퓨터에서도 실행 가능 (Python 설치 없이!)
    """)

# 학습 성능 추적 시각화 영역
log_files = sorted(glob.glob("simulation_log_*.csv"))
if log_files:
    st.sidebar.markdown("---")
    st.sidebar.markdown("📈 학습 성능 그래프 보기")
    show_trend = st.sidebar.checkbox("📊 상태별 변화 추세 보기")

    if show_trend:
        summary_trend = []
        for log in log_files[-7:]:  # 최근 7일
            df_temp = pd.read_csv(log)
            status_counts = df_temp["상태"].value_counts()
            date_str = log.replace("simulation_log_", "").replace(".csv", "")
            for status, count in status_counts.items():
                summary_trend.append({"날짜": date_str, "상태": status, "횟수": count})

        df_trend = pd.DataFrame(summary_trend)
        fig_trend = plt.figure(figsize=(8, 4))
        sns.lineplot(data=df_trend, x="날짜", y="횟수", hue="상태", marker="o")
        plt.title("📈 시뮬레이션 상태별 변화 추이 (최근 7일)")
        st.pyplot(fig_trend)
