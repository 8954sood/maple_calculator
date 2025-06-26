import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import { createStore } from 'vuex'
import { createRouter, createWebHistory } from 'vue-router'
import MainPage from './pages/MainPage.vue'
import CalcPage from './pages/CalcPage.vue'
import ChartPage from './pages/ChartPage.vue'

const store = createStore({
  state() {
    return {
      theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  },
  mutations: {
    toggleTheme(state) {
      state.theme = state.theme === 'dark' ? 'light' : 'dark'
    }
  }
})

const routes = [
  { path: '/', name: 'main', component: MainPage },
  { path: '/calc', name: 'calc', component: CalcPage },
  { path: '/chart', name: 'chart', component: ChartPage }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
