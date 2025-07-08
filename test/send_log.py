#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate fake facility-event JSON logs and POST them to an API server.
- Uses an event-code mapping table (code ➜ device, desc, status default)
- Writes every event to ./logs/facility_events.json
- Sends each event to API_URL  (default: http://localhost:5000/log)
"""

import json, random, time, os, calendar
from datetime import datetime, timezone, timedelta
import requests

KST = timezone(timedelta(hours=9))

# ───────────────────────────────────────────────
# 1. 이벤트 코드 매핑 테이블
# ───────────────────────────────────────────────
EVENT_MAP = {
    # 통신
    101: {"device": "CCTV",          "event_desc": "Video signal lost"},
    102: {"device": "CCTV",          "event_desc": "Blurred image"},
    103: {"device": "Monitor",       "event_desc": "Display failure"},
    104: {"device": "Boarding Gate", "event_desc": "Gate not responding"},
    105: {"device": "Boarding Gate", "event_desc": "Gate motor overheating"},
    106: {"device": "Monitor",       "event_desc": "Resolution mismatch"},
    # 소방
    201: {"device": "Fire Alarm",    "event_desc": "Fire detected"},
    202: {"device": "Fire Alarm",    "event_desc": "Battery low"},
    203: {"device": "Sprinkler",     "event_desc": "Water leakage detected"},
    204: {"device": "Fire Door",     "event_desc": "Door not closed properly"},
    205: {"device": "Fire Alarm",    "event_desc": "Test mode enabled"},
    # 전기
    301: {"device": "Elevator",      "event_desc": "Emergency stop activated"},
    302: {"device": "Escalator",     "event_desc": "Vibration detected"},
    303: {"device": "Screen Door",   "event_desc": "Door open failure"},
    304: {"device": "Screen Door",   "event_desc": "Sensor malfunction"},
    305: {"device": "Elevator",      "event_desc": "Maintenance in progress"},
}

# 역사 위치 (1호선)
STATIONS = [
    "Seoul Station Line 1",
    "City Hall Station Line 1",
    "Jonggak Station Line 1",
    "Dongmyo Station Line 1",
    "Cheongnyangni Station Line 1",
    "Hoegi Station Line 1",
    "Gunja Station Line 1",
    "Yongdap Station Line 1",
    "Guro Station Line 1",
    "Geumcheon-gu Office Station Line 1",
    "Anyang Station Line 1",
    "Suwon Station Line 1"
]

# ───────────────────────────────────────────────
# 2. 디렉터리 및 API URL
# ───────────────────────────────────────────────
LOG_DIR  = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "facility_events.json")

API_URL  = os.getenv("API_URL", "http://localhost:5000/log")

# ───────────────────────────────────────────────
# 3. 랜덤 이벤트 생성 (상태 확률: N 90, W 5, C 5)
# ───────────────────────────────────────────────
STATUS_POOL = ["Normal"] * 90 + ["Warning"] * 5 + ["Critical"] * 5

def generate_event() -> dict:
    code = random.choice(list(EVENT_MAP.keys()))
    meta = EVENT_MAP[code]

    status = random.choice(STATUS_POOL)

    # 2025년 랜덤 월·일·시각 (KST)
    year  = 2025
    month = random.randint(1, 12)
    day   = random.randint(1, calendar.monthrange(year, month)[1])
    hour, minute, second = random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)

    # KST 기준 datetime → 문자열 포맷 (타임존 없음)
    timestamp = datetime(year, month, day, hour, minute, second, tzinfo=KST)
    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp"   : formatted_time,
        "location"    : f"{random.choice(STATIONS)}, Exit {random.randint(1, 8)}",
        "device"      : meta["device"],
        "event_type"  : code,
        "event_desc"  : meta["event_desc"],
        "status"      : status,
        "equipment_id": f"{meta['device'][:3].upper()}-{code}"
    }

# ───────────────────────────────────────────────
# 4. 로그 생성 → 파일 저장 → API POST
# ───────────────────────────────────────────────
def write_and_send():
    evt = generate_event()
    print(" 📦  Generated:", evt)

    with open(LOG_FILE, "a", encoding="utf-8") as fp:
        fp.write(json.dumps(evt, ensure_ascii=False) + "\n")

    try:
        res = requests.post(API_URL, json=evt, timeout=3)
        print(" 📤  Sent to API:", res.status_code)
    except Exception as exc:
        print(" ❌  Send failed:", exc)

# ───────────────────────────────────────────────
if __name__ == "__main__":
    print("✅ Dummy log generator running… (Ctrl+C to stop)")
    while True:
        write_and_send()
        time.sleep(random.randint(1, 5))
