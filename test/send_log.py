#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate fake facility-event JSON logs and POST them to an API server.
- Uses an event-code mapping table (code ➜ device, desc, status)
- Writes every event to ./logs/facility_events.json (one-line JSON)
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
    101: {"device": "CCTV",          "event_desc": "Video signal lost",        "status": "Critical"},
    102: {"device": "CCTV",          "event_desc": "Blurred image",            "status": "Warning"},
    103: {"device": "Monitor",       "event_desc": "Display failure",          "status": "Warning"},
    104: {"device": "Boarding Gate", "event_desc": "Gate not responding",      "status": "Critical"},
    105: {"device": "Boarding Gate", "event_desc": "Gate motor overheating",   "status": "Warning"},
    106: {"device": "Monitor",       "event_desc": "Resolution mismatch",      "status": "Info"},
    # 소방
    201: {"device": "Fire Alarm",    "event_desc": "Fire detected",            "status": "Critical"},
    202: {"device": "Fire Alarm",    "event_desc": "Battery low",              "status": "Warning"},
    203: {"device": "Sprinkler",     "event_desc": "Water leakage detected",   "status": "Warning"},
    204: {"device": "Fire Door",     "event_desc": "Door not closed properly", "status": "Critical"},
    205: {"device": "Fire Alarm",    "event_desc": "Test mode enabled",        "status": "Info"},
    # 전기
    301: {"device": "Elevator",      "event_desc": "Emergency stop activated", "status": "Critical"},
    302: {"device": "Escalator",     "event_desc": "Vibration detected",       "status": "Warning"},
    303: {"device": "Screen Door",   "event_desc": "Door open failure",        "status": "Critical"},
    304: {"device": "Screen Door",   "event_desc": "Sensor malfunction",       "status": "Warning"},
    305: {"device": "Elevator",      "event_desc": "Maintenance in progress",  "status": "Info"},
}

# 역사 위치 샘플
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
# 2. 파일/디렉터리 및 API URL 설정
# ───────────────────────────────────────────────
LOG_DIR  = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "facility_events.json")

API_URL  = os.getenv("API_URL", "http://localhost:5000/log")   # 필요 시 환경변수로 변경

# ───────────────────────────────────────────────
# 3. 랜덤 이벤트 생성 함수 (상태 확률 조정 포함)
# ───────────────────────────────────────────────
def generate_event() -> dict:
    code = random.choice(list(EVENT_MAP.keys()))
    meta = EVENT_MAP[code]

    # ① 상태 확률 풀: N 90% / W 5% / C 5%
    status_pool = ["Normal"] * 90 + ["Warning"] * 5 + ["Critical"] * 5

    # ② 'detected' 또는 'lost' 가 설명에 있으면 Critical, 아니면 확률 추출
    status = (
        "Critical"
        if any(k in meta["event_desc"].lower() for k in ("detected", "lost"))
        else random.choice(status_pool)
    )

    # ───────────────────────────────────────────────
    # ▶ 한국(KST) 기준 2025년 랜덤 월·일·시각 생성
    # ───────────────────────────────────────────────
    year  = 2025
    month = random.randint(1, 12)
    day   = random.randint(1, calendar.monthrange(year, month)[1])
    hour, minute, second = (random.randint(0, 23),
                            random.randint(0, 59),
                            random.randint(0, 59))
    timestamp = datetime(year, month, day, hour, minute, second, tzinfo=KST) \
            .isoformat(timespec="seconds")
    # ───────────────────────────────────────────────

    return {
        "timestamp"   : timestamp,
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
    event = generate_event()
    print(" 📦  Generated:", event)

    with open(LOG_FILE, "a", encoding="utf-8") as fp:
        fp.write(json.dumps(event, ensure_ascii=False) + "\n")

    try:
        res = requests.post(API_URL, json=event, timeout=3)
        print(" 📤  Sent to API:", res.status_code)
    except Exception as exc:
        print(" ❌  Send failed:", exc)

# ───────────────────────────────────────────────
if __name__ == "__main__":
    print("✅ Dummy log generator running… (Ctrl+C to stop)")
    while True:
        write_and_send()
        time.sleep(random.randint(1, 5))
