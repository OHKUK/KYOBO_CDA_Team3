import json
import random
import time
from datetime import datetime
import os
import requests  # 💡 빠져있던 import 추가

# ./logs/facility_events.json 경로 만들고 로그 누적 기록할 준비
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "facility_events.json")

# '설비 종류, 발생 이벤트, 역사 위치, 상태값(정상/경고/위급)' 리스트로 정의
facilities = {
    "CCTV": [
        "Video signal lost",
        "Blurred image",
        "Intrusion detected",
        "Low storage space"
    ],
    "Screen Door": [
        "Door not closed",
        "Sensor not responding",
        "Obstruction detected",
        "Response delay"
    ],
    "Air Conditioner": [
        "Temperature too high",
        "High humidity detected",
        "Filter replacement needed",
        "Power off"
    ],
    "Fire System": [
        "Fire detected",
        "Sprinkler malfunction",
        "Low battery on receiver",
        "Alarm test not executed"
    ]
}

locations = [
    "Gangnam Station Line 2",
    "Yeouido Station Line 9",
    "Gwanghwamun Station Line 5",
    "Euljiro 3-ga Station Line 3"
]

statuses = ["Normal", "Warning", "Critical"]

API_URL = "http://localhost:5000/log"  # ✅ Flask 서버 포트와 일치시켜야 함

# 랜덤으로 설비,이벤트,위치,상태,타임스탬프를 뽑아 하나의 JSON 딕셔너리를 생성함
def generate_event():
    device = random.choice(list(facilities.keys()))
    event_type = random.choice(facilities[device])
    location = random.choice(locations) + f", Exit {random.randint(1, 8)}"
    # 이벤트 내용에 "detected"나 "lost"가 포함되면 상태를 "Critical"로 고정
    status = "Critical" if "detected" in event_type or "lost" in event_type else random.choice(statuses)

    return {
        "device": device,
        "event_type": event_type,
        "status": status,
        "location": location,
        "timestamp": datetime.now().isoformat()
    }

# generate_event()로 만든 로그를 화면에 출력 후 파일에 한 줄(JSON 방식)로 append
# requests.post()로 API URL(http://localhost:5000/log)에 전송하고 결과 코드를 출력
# 예외 시 오류룰 콘솔에 남김
def write_log():
    event = generate_event()
    print("📦 Generated log:", event)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    try:
        res = requests.post(API_URL, json=event, timeout=3)
        print("📨 Sent to API server:", res.status_code)
    except Exception as e:
        print("❌ Failed to send to API server:", e)

# 1-5초 간격 마다 위 과정을 반복해 지속적으로 장애 로그를 발행
if __name__ == "__main__":
    print("✅ Running facility event log generator...\n")
    while True:
        write_log()
        time.sleep(random.randint(1, 5))
