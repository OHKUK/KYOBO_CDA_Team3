from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import socket
import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='/app/.env')

app = Flask(__name__)
CORS(app) 
# ⭐️ 컨테이너 환경에서는 서비스 이름으로 통신해야 합니다.
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST")
LOGSTASH_PORT = 50000

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = 'subway_system'

@app.route("/api/log", methods=["POST"])
def receive_and_forward_log():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    print("✅ Received log:", data)

    with open("received_logs.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((LOGSTASH_HOST, LOGSTASH_PORT))
            log_message = json.dumps(data) + '\n'
            sock.sendall(log_message.encode('utf-8'))
        print("📨 Forwarded to Logstash successfully.")
    except Exception as e:
        print(f"❌ Failed to forward to Logstash: {e}")

    return jsonify({"message": "Log received and forwarded"}), 200

# <<<--- 로그인 API 추가 시작 --->>>
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = None
    cursor = None
    try:
        # Docker 컨테이너 이름(mysql-db)으로 접속합니다.
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT u.username, u.password, d.name as department
            FROM users u
            JOIN departments d ON u.department_id = d.id
            WHERE u.username = %s
        """
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and user["password"] == password:
            return jsonify({
                "message": "로그인 성공",
                "username": user["username"],
                "department": user["department"] # Vue에서 활용할 수 있도록 부서 정보 전달
            }), 200
        else:
            return jsonify({"message": "아이디 또는 비밀번호가 일치하지 않습니다."}), 401
            
    except mysql.connector.Error as err:
        print(f"❌ Database 연결 오류: {err}")
        # DB가 아직 준비되지 않았을 수 있습니다.
        return jsonify({"message": "서버에 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}), 503
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route("/api/alerts", methods=["GET"])
def search_alerts():
    keyword = request.args.get("keyword", "")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, device_id, alert_type, message, detected_at
            FROM alerts
            WHERE message LIKE %s
        """
        params = [f"%{keyword}%"]

        if start_date and end_date:
            query += " AND DATE(detected_at) BETWEEN %s AND %s"
            params += [start_date, end_date]

        query += " ORDER BY detected_at DESC LIMIT 50"

        cursor.execute(query, params)
        results = cursor.fetchall()

        return jsonify(results), 200

    except mysql.connector.Error as err:
        print(f"❌ 검색 중 DB 오류: {err}")
        return jsonify({"message": "DB 오류 발생"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/api/alerts/check", methods=["POST"])
def mark_alert_checked():
    data = request.get_json()
    alert_id  = data.get("id")

    if not alert_id:
        return jsonify({"message": "필수 값 누락"}), 400

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        update_sql = """
            UPDATE alerts
            SET `check` = '확인', checked_at = NOW()
            WHERE id = %s
        """
        cursor.execute(update_sql, (alert_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "해당 알람 없음"}), 404

        return jsonify({"message": "확인 처리 완료"}), 200

    except mysql.connector.Error as err:
        print(f"❌ DB 오류: {err}")
        return jsonify({"message": "DB 오류"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route("/api/alerts/bulk-check", methods=["POST"])
def mark_bulk_alerts_checked():
    data = request.get_json()

    if not isinstance(data, list) or not data:
        return jsonify({"message": "리스트 형식의 요청 데이터가 필요합니다."}), 400

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = conn.cursor()

        update_sql = """
            UPDATE alerts
            SET `check` = '확인', checked_at = NOW()
            WHERE id = %s
        """

        from datetime import datetime

        success_count = 0
        for alert in data:
            alert_id = alert.get("id")
            if not alert_id:
                continue

            try:
                cursor.execute(update_sql, (alert_id,))
                success_count += cursor.rowcount
            except Exception as e:
                print(f"❌ 일괄 확인 처리 중 오류: id={alert_id}, error={e}")
                continue

        conn.commit()

        return jsonify({"message": f"{success_count}건 확인 처리 완료"}), 200

    except mysql.connector.Error as err:
        print(f"❌ DB 오류: {err}")
        return jsonify({"message": "DB 오류"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# ✅ 여기 추가
@app.route("/", methods=["GET"])
def health_check():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
