<script setup>
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import TradeForm from './components/TradeForm.vue'
import TradeAnalysis from './components/TradeAnalysis.vue'
const $store = useStore()
const $route = useRoute()
const toggleTheme = () => {
  $store.commit('toggleTheme')
}
</script>

<template>
  <div :class="[$store.state.theme, 'app-container']">
    <aside class="sidebar">
      <nav>
        <ul>
          <li :class="{active: $route.name === 'main'}"><router-link to="/">거래 분석</router-link></li>
          <li :class="{active: $route.name === 'calc'}"><router-link to="/calc">가성비 계산기</router-link></li>
        </ul>
      </nav>
    </aside>
    <div class="main-wrapper">
      <header class="header">
        <h1>메이플스토리 거래 분석</h1>
        <button @click="toggleTheme" class="theme-toggle">
          {{ $store.state.theme === 'dark' ? '라이트 모드' : '다크 모드' }}
        </button>
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  font-family: 'Apple SD Gothic Neo', 'Segoe UI', 'Malgun Gothic', 'AppleGothic', Arial, sans-serif;
  font-size: 16px;
  transition: background 0.3s, color 0.3s;
}
.sidebar {
  width: 180px;
  background: #23272f;
  color: #fff;
  padding: 2rem 0 2rem 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.sidebar nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}
.sidebar nav ul li {
  margin-bottom: 1.5rem;
  width: 100%;
}
.sidebar nav ul li a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 0.7rem 1.2rem;
  display: block;
  border-radius: 8px;
  transition: background 0.2s;
}
.sidebar nav ul li.active a,
.sidebar nav ul li a:hover {
  background: #4f8cff;
  color: #fff;
}
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.2rem 0.8rem 1.2rem;
  max-width: 650px;
  margin: 0 auto;
  font-size: 1.5rem;
}
.main-content {
  max-width: 650px;
  margin: 0 auto;
  padding: 0 1.2rem 1.5rem 1.2rem;
}
.theme-toggle {
  padding: 0.6rem 1.2rem;
  border-radius: 7px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
}
.dark {
  background: #181a1b;
  color: #f3f3f3;
}
.light {
  background: #f3f3f3;
  color: #181a1b;
}
@media (max-width: 900px) {
  .app-container {
    flex-direction: column;
  }
  .sidebar {
    flex-direction: row;
    width: 100vw;
    min-height: unset;
    padding: 0.5rem 0;
    justify-content: center;
  }
  .sidebar nav ul {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    justify-content: center;
  }
  .sidebar nav ul li {
    margin-bottom: 0;
  }
  .main-wrapper {
    width: 100vw;
  }
  .header, .main-content {
    max-width: 100%;
    padding: 0 0.5rem;
  }
  .header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
    font-size: 1.1rem;
  }
}
</style>
