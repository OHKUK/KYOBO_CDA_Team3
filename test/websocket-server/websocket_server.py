import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, List, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("✅ WebSocket 연결됨. 현재 클라이언트 수:", len(clients))
    try:
        while True:
            await websocket.receive_text()  # Keep-alive
    except Exception as e:
        print("❌ WebSocket 연결 종료:", e)
        clients.remove(websocket)

@app.post("/push")
async def push_log(data: Union[dict, List[Any]]):
    print("🔥 WebSocket push requested:", data)  # ← 이 줄 추가
    print("현재 clients:", clients)
    events = data if isinstance(data, list) else [data]

    for event in events:
        message = json.dumps(event, ensure_ascii=False)
        for ws in clients:
            await ws.send_text(message)