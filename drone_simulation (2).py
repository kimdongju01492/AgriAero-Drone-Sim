
import math
import random
import pandas as pd
import datetime

# 시뮬레이션용 더미 함수들 정의
def generate_fine_zigzag_path(bounds, step_distance=10, deg_per_meter_lat=1/111000, deg_per_meter_lon=1/(111000*0.88)):
    path = []
    y = bounds["bottom"]
    toggle = True
    while y < bounds["top"]:
        if toggle:
            path.append((y, bounds["left"]))
            path.append((y, bounds["right"]))
        else:
            path.append((y, bounds["right"]))
            path.append((y, bounds["left"]))
        toggle = not toggle
        y += step_distance * deg_per_meter_lat
    return path

def get_simulated_weather():
    return {
        "temperature": random.uniform(15, 30),
        "wind_speed": random.uniform(0, 6),
        "humidity": random.uniform(40, 90)
    }

def run_simulations_for_learning(num_runs=100):
    entries = []
    for _ in range(num_runs):
        battery = random.randint(50, 100)
        spray = random.uniform(10, 30)
        wind_speed = get_simulated_weather()["wind_speed"]
        result = "귀환" if battery < 60 or spray < 5 else "작업"
        entries.append({
            "드론": "드론1",
            "상태": result,
            "위도": 35.63,
            "경도": 127.91,
            "배터리": battery,
            "살포량": spray,
            "풍속": wind_speed
        })
    df = pd.DataFrame(entries)
    df.to_csv("simulation_log.csv", index=False, encoding="utf-8-sig")

# AI 판단용 클래스
from sklearn.tree import DecisionTreeClassifier
import joblib

class DroneAgent:
    def __init__(self, model_path="drone_policy.pkl"):
        self.model = joblib.load(model_path) if model_path and os.path.exists(model_path) else None

    def decide(self, battery, spray, wind_speed):
        if self.model:
            return "작업" if self.model.predict([[battery, spray, wind_speed]])[0] == 0 else "귀환"
        return "작업" if battery > 60 and spray > 5 else "귀환"
