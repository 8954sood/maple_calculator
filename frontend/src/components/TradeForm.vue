<template>
  <form class="trade-form" @submit.prevent="submitTrade">
    <div class="row">
      <select v-model="type">
        <option value="sell">판매</option>
        <option value="buy">구매</option>
      </select>
      <input v-model="title" type="text" placeholder="물품 제목" required />
    </div>
    <div class="row">
      <input v-model.number="quantity" type="number" min="1" placeholder="수량" required />
      <input v-model.number="price" type="number" min="1" placeholder="가격" required />
      <select v-model.number="priceUnit">
        <option :value="1">1의 자리</option>
        <option :value="10000">만 단위</option>
      </select>
    </div>
    <div class="row">
      <input v-model="date" type="date" required />
      <button type="submit">저장</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const type = ref('sell')
const title = ref('')
const quantity = ref(1)
const price = ref()
const priceUnit = ref(10000)
const date = ref(new Date().toISOString().slice(0, 10))

const submitTrade = async () => {
  await axios.post('/trades/', {
    type: type.value,
    title: title.value,
    quantity: quantity.value,
    price: price.value,
    price_unit: priceUnit.value,
    date: date.value
  })
  // 입력값 초기화
  title.value = ''
  quantity.value = 1
  priceUnit.value = 10000
  // 새로고침 이벤트 발생 (분석 컴포넌트에 알림)
  window.dispatchEvent(new Event('trade-updated'))
}
</script>

<style scoped>
.trade-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  background: var(--form-bg, #fff);
  border-radius: 12px;
  padding: 1.2rem 1.2rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  max-width: 650px;
  margin: 1.2rem auto;
  font-size: 1rem;
}
.row {
  display: flex;
  gap: 1rem;
}
input, select, button {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}
button {
  background: #4f8cff;
  color: #fff;
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 1rem;
}
button:hover {
  background: #2563eb;
}
@media (max-width: 700px) {
  .trade-form {
    padding: 0.7rem;
    max-width: 100%;
    font-size: 0.97rem;
  }
  .row {
    flex-direction: column;
    gap: 0.5rem;
  }
  input, select, button {
    font-size: 0.97rem;
    padding: 0.5rem 0.7rem;
  }
}
.dark .trade-form {
  background: #23272f;
  color: #f3f3f3;
}
.light .trade-form {
  background: #fff;
  color: #181a1b;
}
</style> 