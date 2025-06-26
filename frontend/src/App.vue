<script setup>
import { useStore } from 'vuex'
import TradeForm from './components/TradeForm.vue'
import TradeAnalysis from './components/TradeAnalysis.vue'
const $store = useStore()
const toggleTheme = () => {
  $store.commit('toggleTheme')
}
</script>

<template>
  <div :class="[$store.state.theme, 'app-container']">
    <header class="header">
      <h1>메이플스토리 거래 분석</h1>
      <button @click="toggleTheme" class="theme-toggle">
        {{ $store.state.theme === 'dark' ? '라이트 모드' : '다크 모드' }}
      </button>
    </header>
    <main class="main-content">
      <TradeForm />
      <TradeAnalysis />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  min-width: 100vw;
  font-family: 'Apple SD Gothic Neo', 'Segoe UI', 'Malgun Gothic', 'AppleGothic', Arial, sans-serif;
  font-size: 16px;
  transition: background 0.3s, color 0.3s;
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
@media (max-width: 700px) {
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
