<template>
  <div class="calc-container">
    <h2>가성비 계산기</h2>
    <form class="calc-form" @submit.prevent="calcProfit">
      <div class="row">
        <label>비약 종류</label>
        <select v-model="type">
          <option value="wealth">재물 획득의 비약</option>
          <option value="exp">경험 축적의 비약</option>
        </select>
      </div>
      <div class="row">
        <label>비약 판매가</label>
        <input v-model.number="pricePotion" type="number" min="1" required placeholder="판매가" />
        <select v-model.number="unitPotion">
          <option :value="1">1의 자리</option>
          <option :value="10000">만 단위</option>
        </select>
      </div>
      <div class="row">
        <label>쥬니퍼베리 씨앗 오일 1개 가격</label>
        <input v-model.number="priceOil" type="number" min="0" required placeholder="씨앗 오일 가격" />
        <select v-model.number="unitOil">
          <option :value="1">1의 자리</option>
          <option :value="10000">만 단위</option>
        </select>
      </div>
      <div class="row">
        <label>쥬니퍼베리 씨앗 1개 가격 (대체재)</label>
        <input v-model.number="priceSeed" type="number" min="0" required placeholder="씨앗 가격" />
        <select v-model.number="unitSeed">
          <option :value="1">1의 자리</option>
          <option :value="10000">만 단위</option>
        </select>
      </div>
      <div class="row">
        <label>최상급 아이템 결정 1개 가격</label>
        <input v-model.number="priceCrystal" type="number" min="0" required placeholder="결정 가격" />
        <select v-model.number="unitCrystal">
          <option :value="1">1의 자리</option>
          <option :value="10000">만 단위</option>
        </select>
      </div>
      <div class="row">
        <label>현자의 돌 1개 가격</label>
        <input v-model.number="priceStone" type="number" min="0" required placeholder="현자의 돌 가격" />
        <select v-model.number="unitStone">
          <option :value="1">1의 자리</option>
          <option :value="10000">만 단위</option>
        </select>
      </div>
      <div class="row">
        <label>수수료율</label>
        <select v-model.number="feeRate">
          <option :value="5">수수료 5% (기본)</option>
          <option :value="3">수수료 3% (MVP/PC방)</option>
        </select>
      </div>
      <div class="row">
        <label>씨앗 오일 대신 씨앗 사용</label>
        <input type="checkbox" v-model="useSeed" />
      </div>
      <div class="row" v-if="useSeed">
        <label>10% 실패 확률 반영</label>
        <input type="checkbox" v-model="useFailProb" />
      </div>
      <div class="row">
        <button type="submit">순수익 계산</button>
      </div>
    </form>
    <div v-if="result" class="result-box">
      <div>총 재료비: <b>{{ result.totalCost.toLocaleString() }}</b> 메소</div>
      <div>순수익: <b>{{ result.profit.toLocaleString() }}</b> 메소</div>
      <div>수익률: <b>{{ result.profitRate.toFixed(2) }}%</b></div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const type = ref('wealth')
const pricePotion = ref()
const priceOil = ref()
const priceSeed = ref()
const priceCrystal = ref()
const priceStone = ref()
const unitPotion = ref(10000)
const unitOil = ref(10000)
const unitSeed = ref(10000)
const unitCrystal = ref(10000)
const unitStone = ref(10000)
const feeRate = ref(5)
const useSeed = ref(false)
const useFailProb = ref(false)
const result = ref(null)

const STORAGE_KEY = 'maple-calc-inputs-v1'

// 입력값 저장
watch([
  type, pricePotion, priceOil, priceSeed, priceCrystal, priceStone,
  unitPotion, unitOil, unitSeed, unitCrystal, unitStone, feeRate, useSeed, useFailProb
], () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    type: type.value,
    pricePotion: pricePotion.value,
    priceOil: priceOil.value,
    priceSeed: priceSeed.value,
    priceCrystal: priceCrystal.value,
    priceStone: priceStone.value,
    unitPotion: unitPotion.value,
    unitOil: unitOil.value,
    unitSeed: unitSeed.value,
    unitCrystal: unitCrystal.value,
    unitStone: unitStone.value,
    feeRate: feeRate.value,
    useSeed: useSeed.value,
    useFailProb: useFailProb.value
  }))
}, { deep: true })

// 입력값 복원
onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const data = JSON.parse(saved)
      type.value = data.type ?? 'wealth'
      pricePotion.value = data.pricePotion
      priceOil.value = data.priceOil
      priceSeed.value = data.priceSeed
      priceCrystal.value = data.priceCrystal
      priceStone.value = data.priceStone
      unitPotion.value = data.unitPotion ?? 10000
      unitOil.value = data.unitOil ?? 10000
      unitSeed.value = data.unitSeed ?? 10000
      unitCrystal.value = data.unitCrystal ?? 10000
      unitStone.value = data.unitStone ?? 10000
      feeRate.value = data.feeRate ?? 5
      useSeed.value = data.useSeed ?? false
      useFailProb.value = data.useFailProb ?? false
    } catch {}
  }
})

const calcProfit = () => {
  // 재료 소모량
  const oilCount = 10
  const crystalCount = 3
  const stoneCount = type.value === 'wealth' ? 1 : 2
  const outputCount = 3 // 1회 제작 시 비약 3개 생산

  // 단위 환산
  const potionPrice = pricePotion.value * unitPotion.value * outputCount * (1 - feeRate.value / 100)
  const oilPrice = priceOil.value * unitOil.value
  const seedPrice = priceSeed.value * unitSeed.value
  const crystalPrice = priceCrystal.value * unitCrystal.value
  const stonePrice = priceStone.value * unitStone.value

  // 오일 대신 씨앗 사용 시
  let oilCost = 0
  if (useSeed.value) {
    const seedPerOil = useFailProb.value ? (6 / 0.9) : 6
    oilCost = seedPrice * seedPerOil * oilCount
  } else {
    oilCost = oilPrice * oilCount
  }
  const crystalCost = crystalPrice * crystalCount
  const stoneCost = stonePrice * stoneCount

  const totalCost = oilCost + crystalCost + stoneCost
  const profit = potionPrice - totalCost
  const profitRate = totalCost > 0 ? (profit / totalCost) * 100 : 0

  result.value = {
    totalCost,
    profit,
    profitRate
  }
}
</script>

<style scoped>
.calc-container {
  background: var(--form-bg, #fff);
  border-radius: 12px;
  padding: 1.2rem 1.2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin: 1.2rem auto;
  font-size: 1rem;
  max-width: 650px;
}
h2 {
  margin-bottom: 1.2rem;
}
.calc-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.row {
  display: flex;
  align-items: center;
  gap: 1rem;
}
label {
  min-width: 170px;
  font-weight: 500;
}
input[type="number"], select {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
  flex: 1;
}
input[type="checkbox"] {
  width: 18px;
  height: 18px;
}
button {
  background: #4f8cff;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.6rem 1.2rem;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover {
  background: #2563eb;
}
.result-box {
  margin-top: 1.5rem;
  background: #f6f8fa;
  border-radius: 8px;
  padding: 1rem 1.2rem;
  font-size: 1.08rem;
}
.dark .calc-container {
  background: #23272f;
  color: #f3f3f3;
}
.light .calc-container {
  background: #fff;
  color: #181a1b;
}
.dark .result-box {
  background: #181a1b;
  color: #f3f3f3;
}
.light .result-box {
  background: #f6f8fa;
  color: #181a1b;
}
</style> 