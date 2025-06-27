<template>
  <div class="analysis-container">
    <div class="row">
      <input type="date" v-model="date" @change="fetchData" />
      <button @click="fetchData">조회</button>
    </div>
    <div v-if="summary" class="summary">
      <div>총 판매: <b>{{ summary.total_sell.toLocaleString() }}</b> 메소</div>
      <div>총 구매: <b>{{ summary.total_buy.toLocaleString() }}</b> 메소</div>
      <div>수익: <b>{{ summary.profit.toLocaleString() }}</b> 메소</div>
      <div>수익률: <b v-if="summary.profit_rate !== null">{{ summary.profit_rate.toFixed(2) }}%</b><span v-else>-</span></div>
    </div>
    <div v-if="trades.length" class="trade-list">
      <h3>거래 내역</h3>
      <table>
        <thead>
          <tr>
            <th>종류</th>
            <th>제목</th>
            <th>수량</th>
            <th>가격(메소)</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in trades" :key="t.id">
            <td>{{ t.type === 'sell' ? '판매' : '구매' }}</td>
            <td>{{ t.title }}</td>
            <td>{{ t.quantity }}</td>
            <td>{{ t.price.toLocaleString() }}</td>
            <td><button class="delete-btn" @click="deleteTrade(t.id)">삭제</button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-data">거래 내역이 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const date = ref(new Date().toISOString().slice(0, 10))
const trades = ref([])
const summary = ref(null)

const fetchData = async () => {
  const [tradesRes, summaryRes] = await Promise.all([
    axios.get(`/trades/${date.value}`),
    axios.get(`/summary/${date.value}`)
  ])
  trades.value = tradesRes.data
  summary.value = summaryRes.data
}

const deleteTrade = async (id) => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await axios.delete(`/trades/${id}`)
    fetchData()
    window.dispatchEvent(new Event('trade-updated'))
  }
}

onMounted(() => {
  fetchData()
  window.addEventListener('trade-updated', fetchData)
})
</script>

<style scoped>
.analysis-container {
  background: var(--form-bg, #fff);
  border-radius: 12px;
  padding: 1.2rem 1.2rem 1.2rem 1.2rem;
  box-shadow: 0 2 px 8px rgba(0,0,0,0.06);
  min-width: 900px;
  margin: 1.2rem auto;
  font-size: 1rem;
}
.row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}
.summary {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 1.2rem;
  font-size: 1.05rem;
}
.trade-list {
  margin-top: 1.2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1.05rem;
}
th, td {
  padding: 0.6rem 1rem;
  border-bottom: 1px solid #e0e0e0;
  text-align: center;
}
.delete-btn {
  background: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.4rem 0.9rem;
  cursor: pointer;
  font-weight: bold;
  font-size: 1rem;
  transition: background 0.2s;
}
.delete-btn:hover {
  background: #d32f2f;
}
.no-data {
  color: #888;
  text-align: center;
  margin-top: 1.2rem;
  font-size: 1rem;
}
@media (max-width: 700px) {
  .analysis-container {
    padding: 0.7rem;
    max-width: 100%;
    font-size: 0.97rem;
  }
  .row, .summary {
    flex-direction: column;
    gap: 0.5rem;
    font-size: 0.97rem;
  }
  th, td {
    font-size: 0.97rem;
    padding: 0.4rem 0.6rem;
  }
}
.dark .analysis-container {
  background: #23272f;
  color: #f3f3f3;
}
.light .analysis-container {
  background: #fff;
  color: #181a1b;
}
</style> 