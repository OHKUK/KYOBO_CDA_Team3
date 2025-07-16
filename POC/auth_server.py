from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Vue에서 호출 시 CORS 오류 방지용

# ✅ DB 연결 정보
DB_CONFIG = {
    'host': 'your-db-host',      # 예: 'localhost' 또는 'mysql'
    'user': 'your-db-user',
    'password': 'your-db-password',
    'database': 'your-db-name'
}

# ✅ 로그인 API
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"message": "아이디와 비밀번호를 입력해주세요."}), 400

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # 사용자 조회
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "존재하지 않는 사용자입니다."}), 401

        if user["password"] != password:
            return jsonify({"message": "아이디 또는 비밀번호가 일치하지 않습니다."}), 401

        # 로그인 성공 → 부서 정보, 이메일 등 반환
        return jsonify({
            "user_id": user["user_id"],
            "department": user["department"],
            "email": user["email"]
        })

    except Exception as e:
        print("❌ DB 오류:", e)
        return jsonify({"message": f"서버 오류: {str(e)}"}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ✅ 서버 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
