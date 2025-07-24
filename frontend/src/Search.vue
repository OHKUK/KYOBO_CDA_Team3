<template>
  <div class="search-container">
    <!-- 🔙 돌아가기 버튼 -->
    <button @click="$emit('goBack')" class="back-button">← 돌아가기</button>

    <h2>🔍 알림 검색</h2>

    <!-- 검색 조건 -->
    <div class="search-bar">
      <input
        v-model="keyword"
        @keyup.enter="searchAlerts"
        placeholder="메시지 내용을 입력하세요"
      />

      <label>시작일:</label>
      <input type="date" v-model="startDate" />

      <label>종료일:</label>
      <input type="date" v-model="endDate" />

      <button @click="searchAlerts">검색</button>
    </div>

    <!-- 검색 결과 테이블 -->
    <table v-if="alerts.length > 0">
      <thead>
        <tr>
          <th>장비 ID</th>
          <th>알림 종류</th>
          <th>메시지</th>
          <th>발생 시각</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="alert in alerts" :key="alert.id">
          <td>{{ alert.device_id }}</td>
          <td>{{ alert.alert_type }}</td>
          <td>{{ alert.message }}</td>
          <td>{{ formatDate(alert.detected_at) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else-if="searched">🔍 검색 결과가 없습니다.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchView",
  data() {
    return {
      keyword: "",
      startDate: "",
      endDate: "",
      alerts: [],
      searched: false,
    };
  },
  methods: {
    async searchAlerts() {
      if (!this.keyword.trim()) {
        alert("검색어를 입력해주세요.");
        return;
      }

      try {
        const params = {
          keyword: this.keyword,
        };

        if (this.startDate) params.start_date = this.startDate;
        if (this.endDate) params.end_date = this.endDate;

        const res = await axios.get("/api/alerts", { params });
        this.alerts = res.data;
        this.searched = true;
      } catch (err) {
        console.error("❌ 검색 오류:", err);
        alert("검색 중 오류가 발생했습니다.");
      }
    },
    formatDate(str) {
      return new Date(str).toLocaleString("ko-KR");
    },
  },
};
</script>

<style scoped>
.search-container {
  padding: 1.5rem;
  font-family: Arial, sans-serif;
}
.back-button {
  margin-bottom: 1rem;
  padding: 0.4rem 1rem;
  background: #ddd;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.search-bar {
  margin-bottom: 1rem;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.search-bar input[type="text"],
.search-bar input[type="date"] {
  padding: 0.5rem;
}
.search-bar button {
  padding: 0.5rem 1rem;
  background: #003366;
  color: white;
  border: none;
  border-radius: 4px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
thead {
  background: #003366;
  color: white;
}
td, th {
  border: 1px solid #ccc;
  padding: 0.6rem;
  text-align: left;
}
</style>
