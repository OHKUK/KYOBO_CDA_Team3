from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import json
import os
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE = "received_logs.json"
os.makedirs("./logs", exist_ok=True)

@app.route("/log", methods=["POST"])
def receive_log():
    data = request.get_json()
    print("✅ Received log:", data)

    # 저장
    with open(f"./logs/{LOG_FILE}", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    # 실시간 WebSocket 전송
    socketio.emit("new_log", data)

    # 💡 FastAPI WebSocket 서버에도 전송
    try:
        requests.post("http://localhost:5044/push", json=data)
    except Exception as e:
        print("⚠️ Failed to push to WebSocket server:", e)

    return jsonify({"message": "Log received"}), 200

@socketio.on("connect")
def handle_connect():
    print("🔗 WebSocket client connected.")

if __name__ == "__main__":
    print("🚀 Starting API + WebSocket server...")
    socketio.run(app, host="0.0.0.0", port=8000)
