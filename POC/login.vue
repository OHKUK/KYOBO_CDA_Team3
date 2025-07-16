<template>
  <div class="login-container">
    <h2 class="title">🚨 시스템 로그인</h2>

    <div class="form-group">
      <label for="userId">👤 사용자 ID</label>
      <input v-model="userId" id="userId" placeholder="아이디 입력" />
    </div>

    <div class="form-group">
      <label for="password">🔒 비밀번호</label>
      <input v-model="password" type="password" id="password" placeholder="비밀번호 입력" />
    </div>

    <button @click="login" class="login-button">로그인</button>
    <p v-if="error" class="error-msg">{{ error }}</p>
  </div>
</template>

<script>
export default {
  name: "LoginPage",
  data() {
    return {
      userId: "",
      password: "",
      error: ""
    };
  },
  methods: {
    async login() {
      this.error = "";

      if (!this.userId || !this.password) {
        this.error = "⚠️ 아이디와 비밀번호를 모두 입력해주세요.";
        return;
      }

      try {
        const res = await fetch("http://192.168.0.105:5000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: this.userId,
            password: this.password
          })
        });

        const result = await res.json();

        if (!res.ok) {
          this.error = "❌ " + result.message;
          return;
        }

        alert(`✅ 로그인 성공! 환영합니다, ${result.user_id}님 (${result.department})`);
        localStorage.setItem("user", JSON.stringify(result));
        this.$router.push("/dashboard");  // 대시보드로 이동
      } catch (err) {
        this.error = "❗서버 연결 중 문제가 발생했습니다.";
        console.error(err);
      }
    }
  }
};
</script>

<style scoped>
/* 스타일 생략 - 이전에 작성한 내용 그대로 유지하셔도 됩니다 */
</style>
