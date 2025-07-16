import json
import random
import time
from datetime import datetime
import os
import requests  # 💡 빠져있던 import 추가

# Directory and file for logs
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "facility_events.json")

# Device types and possible event types
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

API_URL = "http://localhost:8000/log"  # ✅ Flask 서버 포트와 일치시켜야 함

def generate_event():
    device = random.choice(list(facilities.keys()))
    event_type = random.choice(facilities[device])
    location = random.choice(locations) # + f", Exit {random.randint(1, 8)}"

    # 💡 상태 비율 조정: Normal 90%, Warning 5%, Critical 5%
    status_pool = ["Normal"] * 90 + ["Warning"] * 5 + ["Critical"] * 5
    status = "Critical" if "detected" in event_type or "lost" in event_type else random.choice(status_pool)

    return {
        "device": device,
        "event_type": event_type,
        "status": status,
        "location": location,
        "timestamp": datetime.now().isoformat()
    }

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

if __name__ == "__main__":
    print("✅ Running facility event log generator...\n")
    while True:
        write_log()
        time.sleep(random.randint(1, 5))
