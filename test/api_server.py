from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/log", methods=["POST"])
def receive_log():
    data = request.get_json()  # 헤더가 Content-Type: application/json 이어야 정상 파싱
    print("✅ Received log:", data)  # 실시간 디버깅용

    with open("received_logs.json", "a", encoding="utf-8") as f:  # received_logs.json 파일에 한 줄씩 append
        f.write(json.dumps(data, ensure_ascii=False) + "\n")  # ensure_ascii=False → 한글 깨짐 방지

    return jsonify({"message": "Log received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # 모든 IP 바인딩·포트 5000 사용 → 로그 생성기의 API_URL과 일치해야 함


# Flask 서버가 JSON 수신 → 즉시 콘솔+파일 기록
# 나중에 Logstash가 이 파일을 읽거나, 코드에 Logstash 전송 로직(requests.post("http://logstash:5044", json=data))을 추가하면 전체 파이프라인 완성