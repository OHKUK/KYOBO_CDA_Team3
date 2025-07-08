from flask import Flask, request, jsonify
import json
import socket

app = Flask(__name__)

# ⭐️ 컨테이너 환경에서는 서비스 이름으로 통신해야 합니다.
LOGSTASH_HOST = 'logstash'
LOGSTASH_PORT = 50000

@app.route("/log", methods=["POST"])
def receive_and_forward_log():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    print("✅ Received log:", data)

    with open("received_logs.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 이제 'logstash' 라는 이름의 컨테이너를 정확히 찾아갑니다.
            sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
            log_message = json.dumps(data) + '\n'
            sock.sendall(log_message.encode('utf-8'))
        print("📨 Forwarded to Logstash successfully.")
    except Exception as e:
        print(f"❌ Failed to forward to Logstash: {e}")

    return jsonify({"message": "Log received and forwarded"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

