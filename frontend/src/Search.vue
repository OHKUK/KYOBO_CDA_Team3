<template>
  <div class="search-container">
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

    <!-- ✅ 2. 여기 filter-bar 추가 -->
    <div class="filter-bar">
      <label
        ><input type="checkbox" v-model="filterChecked" /> 확인된 알람만
        보기</label
      >
      <label
        ><input type="checkbox" v-model="filterUnchecked" /> 미확인 알람만
        보기</label
      >
    </div>
    <!-- ✅ 선택된 항목 있을 때만 표시 -->
    <button
      v-if="selectedAlerts.length"
      @click="markSelectedAsChecked"
      class="bulk-check"
    >
      선택된 알림 확인 처리
    </button>

    <!-- 검색 결과 테이블 -->
    <table v-if="alerts.length > 0">
      <thead>
        <tr>
          <th><input type="checkbox" @change="toggleAll($event)" /></th>
          <!-- ✅ 전체 선택 -->
          <th>알림 번호</th>
          <th>장비 ID</th>
          <th>알림 종류</th>
          <th>메시지</th>
          <th>발생 시각</th>
          <th>확인 여부</th>
          <!-- ✅ 추가 -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="alert in filteredResults" :key="alert.id">
          <td>
            <input
              type="checkbox"
              :value="alert"
              v-model="selectedAlerts"
              :disabled="alert.check === '확인'"
            />
            <!-- ✅ 개별 선택 -->
          </td>
          <td>{{ alert.id }}</td>
          <td>{{ alert.device_id }}</td>
          <td>{{ alert.alert_type }}</td>
          <td>{{ alert.message }}</td>
          <td>{{ formatDate(alert.detected_at) }}</td>
          <td>
            <span v-if="alert.check === '확인'">✔ 확인됨</span>
            <button v-else @click="markAsChecked(alert)">확인</button>
          </td>
          <!-- ✅ 추가 -->
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
      filterChecked: false, // ✅ 여기에 추가
      filterUnchecked: false, // ✅ 여기에 추가
      selectedAlerts: [], // ✅ 선택된 알림 목록
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
        const apiUrl = process.env.VUE_APP_API_URL;
        const res = await axios.get(`${apiUrl}/api/alerts`, { params });
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
    async markAsChecked(alert) {
      try {
        const apiUrl = process.env.VUE_APP_API_URL;
        const res = await axios.post(`${apiUrl}/api/alerts/check`, {
          id: alert.id,
        });

        if (res.status === 200) {
          alert.check = "확인"; // ✅ 상태 직접 갱신
        }
      } catch (err) {
        console.error("❌ 확인 실패:", err);
        alert("확인 처리 중 오류가 발생했습니다.");
      }
    },
    toggleAll(e) {
      // ✅ 전체 체크박스 선택
      if (e.target.checked) {
        this.selectedAlerts = this.filteredResults.filter(
          (a) => a.check !== "확인"
        );
      } else {
        this.selectedAlerts = [];
      }
    },

    async markSelectedAsChecked() {
      try {
        const payload = this.selectedAlerts.map((a) => ({
          id: a.id,
        }));

        const res = await axios.post("/api/alerts/bulk-check", payload); // ✅ 서버에 여러 개 전송

        if (res.status === 200) {
          // ✅ 성공 시 화면 갱신
          this.selectedAlerts.forEach((alert) => {
            alert.check = "확인";
          });
          this.selectedAlerts = [];
        }
      } catch (err) {
        console.error("❌ 일괄 확인 실패:", err);
        alert("일괄 확인 처리 중 오류가 발생했습니다.");
      }
    },
  },
  computed: {
    filteredResults() {
      return this.alerts.filter((a) => {
        if (this.filterChecked && !this.filterUnchecked) {
          return a.check === "확인"; // 확인된 것만 보기
        }
        if (!this.filterChecked && this.filterUnchecked) {
          return !a.check || a.check !== "확인"; // 미확인만 보기
        }
        return true; // 아무 것도 안 누른 경우 전체 보기
      });
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
.filter-bar {
  /* ✅ 새로 추가 */
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  display: flex;
  gap: 20px;
  align-items: center;
}
.bulk-check {
  margin-bottom: 0.5rem;
  padding: 0.4rem 1rem;
  background: #228b22;
  color: white;
  border: none;
  border-radius: 4px;
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
td,
th {
  border: 1px solid #ccc;
  padding: 0.6rem;
  text-align: left;
}
</style>
