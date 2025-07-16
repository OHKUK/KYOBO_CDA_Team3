from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Vue 접속 허용

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="subway"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and user["password"] == password:
        return jsonify({
            "user_id": user["user_id"],
            "department": user["department"]
        }), 200
    else:
        return jsonify({"message": "아이디 또는 비밀번호가 일치하지 않습니다."}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
