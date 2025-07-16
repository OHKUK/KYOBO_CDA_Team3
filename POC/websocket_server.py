import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
    try:
        while True:
            await websocket.receive_text()  # Keep-alive
    except:
        clients.remove(websocket)

@app.post("/push")
async def push_log(data: dict):
    print("🔥 WebSocket push requested:", data)  # ← 이 줄 추가
    message = json.dumps(data, ensure_ascii=False)
    for ws in clients:
        await ws.send_text(message)
    return {"message": "sent"}

# 실행 명령: uvicorn websocket_server:app --host 0.0.0.0 --port 8001
