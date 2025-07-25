<<<<<<<< HEAD:POC/hagyuung/AlertDashboard.vue
<template>
  <div class="container">
    <!-- 좌측 메뉴 -->
    <aside class="sidebar">
      <h2 class="logo">🚇 서울 지하철 관제</h2>
      <ul>
        <li
          v-for="item in categories"
          :key="item"
          :class="{ active: category === item }"
          @click="setCategory(item)"
        >
          {{ item }}
        </li>
      </ul>
    </aside>

    <!-- 메인 -->
    <main class="main">
      <!-- 상단바 -->
      <header class="topbar">
        <h1>{{ category }} 관제 대시보드</h1>
        <button @click="logout">로그아웃</button>
      </header>

      <!-- 실시간 알람 -->
      <section class="alert-section">
        <h2>🛎️ 실시간 알림</h2>
        <ul>
          <li v-for="(alert, index) in alerts" :key="index">
            <span class="badge" :class="alert.status">{{ alert.status }}</span>
            {{ alert.timestamp }} | {{ alert.location }} | {{ alert.device }} {{ alert.event_type }}
          </li>
        </ul>
      </section>

      <!-- Kibana 대시보드 -->
      <section class="dashboard">
        <iframe
          :src="dashboardUrl"
          frameborder="0"
          width="100%"
          height="480"
        ></iframe>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      category: "소방",
      categories: ["소방", "전기", "통신"],
      alerts: [],
      socket: null,
    };
  },
  computed: {
    dashboardUrl() {
      const urls = {
        소방: "http://192.168.56.1:5601/goto/65e42a60-5ca0-11f0-9a58-9d0a970cdc47",
        전기: "http://192.168.56.1:5601/goto/8f100580-5ca0-11f0-9a58-9d0a970cdc47",
        통신: "http://192.168.56.1:5601/goto/b017d500-5ca0-11f0-9a58-9d0a970cdc47",
      };
      return urls[this.category];
    },
  },
  mounted() {
    this.socket = new WebSocket("ws://192.168.56.1:8000");
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.status_kr && data.status_kr["상태"] === "심각") {
        this.alerts.unshift(data);
        if (this.alerts.length > 10) this.alerts.pop();
      }
    };
  },
  methods: {
    setCategory(cat) {
      this.category = cat;
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString("ko-KR", { hour12: false });
    },
    logout() {
      alert("로그아웃 완료");
    },
  },
};
</script>

<style scoped>
/* 폰트 */
* {
  font-family: "Nanum Gothic", sans-serif;
  box-sizing: border-box;
}

.container {
  display: flex;
  height: 100vh;
  background-color: #f0f2f5;
  color: #222;
}

/* 좌측 메뉴 */
.sidebar {
  width: 220px;
  background: #003366;
  color: #fff;
  padding: 1.5rem;
}
.logo {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  padding: 0.75rem;
  margin-bottom: 0.3rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}
.sidebar li.active,
.sidebar li:hover {
  background: #005599;
}

/* 메인 */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 상단바 */
.topbar {
  background: #fff;
  border-bottom: 2px solid #003366;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.topbar h1 {
  font-size: 1.2rem;
}
.topbar button {
  padding: 0.4rem 1rem;
  border: none;
  background: #005599;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

/* 알람 */
.alerts {
  padding: 1.2rem 1.5rem;
  background: #fefefe;
}
.alerts h3 {
  margin-bottom: 1rem;
  font-weight: bold;
  color: #c80000;
}
.alerts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.alerts li {
  background: #ffeeee;
  margin-bottom: 8px;
  padding: 0.8rem;
  border-left: 4px solid #cc0000;
  border-radius: 4px;
  font-size: 0.92rem;
  display: flex;
  gap: 10px;
  align-items: center;
}
.time {
  font-weight: bold;
  color: #555;
  width: 160px;
}
.status {
  font-weight: bold;
  color: #c80000;
  width: 60px;
}
.location {
  flex: 1;
}
.desc {
  font-weight: 500;
  color: #222;
}

/* 대시보드 */
.dashboard {
  flex: 1;
  background: #fff;
  padding: 1rem 1.5rem;
}
</style>
========
<template>
  <div class="container">
    <!-- 좌측 메뉴 -->
    <aside class="sidebar">
      <h2 class="logo">🚇 서울 지하철 관제</h2>
      <ul>
        <li
          v-for="item in categories"
          :key="item"
          :class="{ active: category === item }"
          @click="setCategory(item)"
        >
          {{ item }}
        </li>
      </ul>
    </aside>

    <!-- 메인 -->
    <main class="main">
      <!-- 상단바 -->
      <header class="topbar">
        <h1>{{ category }} 관제 대시보드</h1>
        <button @click="logout">로그아웃</button>
      </header>

      <!-- 실시간 알람 -->
      <section class="alerts">
        <h3>🚨 실시간 경고 알림</h3>
        <ul>
          <li v-for="(alert, idx) in alerts" :key="idx">
            <span class="time">{{ formatTime(alert.alarm["@timestamp"]) }}</span>
            <span class="status">{{ alert.alarm["상태"] }}</span>
            <span class="location">{{ alert.alarm["위치"] }}</span>
            <span class="desc">
              {{ alert.alarm["시설"] }} - {{ alert.alarm["이벤트"] }}
            </span>
          </li>
        </ul>
      </section>

      <!-- Kibana 대시보드 -->
      <section class="dashboard">
        <iframe
          :src="dashboardUrl"
          frameborder="0"
          width="100%"
          height="480"
        ></iframe>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      category: "소방",
      categories: ["소방", "전기", "통신"],
      alerts: [],
      socket: null,
    };
  },
  computed: {
    dashboardUrl() {
      const urls = {
        소방: "http://192.168.56.1:5601/goto/2d765d20-5d3f-11f0-bfd9-13636741db68",
        전기: "http://192.168.56.1:5601/goto/3a2c9b10-5d3f-11f0-bfd9-13636741db68",
        통신: "http://192.168.56.1:5601/goto/42196a10-5d3f-11f0-bfd9-13636741db68",
      };
      return urls[this.category];
    },
  },
  mounted() {
      const socket = new WebSocket('ws://192.168.56.1:8001/ws');
      socket.onopen = () => {
        console.log(':흰색_확인_표시: WebSocket 연결됨');
      };
      socket.onmessage = (event) => {
        console.log(':화살표가_있는_봉투: 새 데이터:', event.data);
        const parsed = JSON.parse(event.data);
        const status = parsed["상태"];
        // :흰색_확인_표시: 심각, 경고만 표시
        if (status !== "심각" && status !== "경고") return;
        // :흰색_확인_표시: 최대 10개까지 유지
        this.alerts.unshift({ alarm: parsed });
        if (this.alerts.length > 10) {
          this.alerts.pop();
        }
      };
      socket.onerror = (error) => {
        console.error(':x: WebSocket 에러:', error);
      };
      socket.onclose = () => {
        console.log(':x: WebSocket 닫힘');
      };
  },
  methods: {
    setCategory(cat) {
      this.category = cat;
    },
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString("ko-KR", { hour12: false });
    },
    logout() {
      alert("로그아웃 완료");
    },
  },
};
</script>
<style scoped>
/* 폰트 */
* {
  font-family: "Nanum Gothic", sans-serif;
  box-sizing: border-box;
}

.container {
  display: flex;
  height: 100vh;
  background-color: #f0f2f5;
  color: #222;
}

/* 좌측 메뉴 */
.sidebar {
  width: 220px;
  background: #003366;
  color: #fff;
  padding: 1.5rem;
}
.logo {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  padding: 0.75rem;
  margin-bottom: 0.3rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}
.sidebar li.active,
.sidebar li:hover {
  background: #005599;
}

/* 메인 */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 상단바 */
.topbar {
  background: #fff;
  border-bottom: 2px solid #003366;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.topbar h1 {
  font-size: 1.2rem;
}
.topbar button {
  padding: 0.4rem 1rem;
  border: none;
  background: #005599;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
}

/* 알람 */
.alerts {
  padding: 1.2rem 1.5rem;
  background: #fefefe;
}
.alerts h3 {
  margin-bottom: 1rem;
  font-weight: bold;
  color: #c80000;
}
.alerts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.alerts li {
  background: #ffeeee;
  margin-bottom: 8px;
  padding: 0.8rem;
  border-left: 4px solid #cc0000;
  border-radius: 4px;
  font-size: 0.92rem;
  display: flex;
  gap: 10px;
  align-items: center;
}
.time {
  font-weight: bold;
  color: #555;
  width: 160px;
}
.status {
  font-weight: bold;
  color: #c80000;
  width: 60px;
}
.location {
  flex: 1;
}
.desc {
  font-weight: 500;
  color: #222;
}

/* 대시보드 */
.dashboard {
  flex: 1;
  background: #fff;
  padding: 1rem 1.5rem;
}
</style>
>>>>>>>> 60ff5b1a005673acba0f50802123e3780f51f740:test/Dashboard.vue
