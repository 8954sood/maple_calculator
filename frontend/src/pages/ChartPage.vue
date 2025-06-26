<template>
  <div class="chart-container">
    <h2>거래 그래프</h2>
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

const chartRef = ref(null)
let chartInstance = null

const fetchData = async () => {
  // 날짜별 집계 데이터 가져오기 (최근 30일)
  const today = new Date()
  const days = Array.from({length: 30}, (_, i) => {
    const d = new Date(today)
    d.setDate(today.getDate() - (29 - i))
    return d.toISOString().slice(0, 10)
  })
  const labels = []
  const profits = []
  const sells = []
  const buys = []
  const rates = []
  for (const date of days) {
    const summary = (await axios.get(`/summary/${date}`)).data
    labels.push(date)
    profits.push(summary.profit)
    sells.push(summary.total_sell)
    buys.push(summary.total_buy)
    rates.push(summary.profit_rate)
  }
  return { labels, profits, sells, buys, rates }
}

const renderChart = async () => {
  const { labels, profits, sells, buys, rates } = await fetchData()
  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(chartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: '순이익',
          data: profits,
          borderColor: '#4f8cff',
          backgroundColor: 'rgba(79,140,255,0.1)',
          yAxisID: 'y',
          pointRadius: 5,
          pointHoverRadius: 8,
        },
        {
          label: '수익률(%)',
          data: rates,
          borderColor: '#ffb300',
          backgroundColor: 'rgba(255,179,0,0.1)',
          yAxisID: 'y1',
          pointRadius: 5,
          pointHoverRadius: 8,
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'nearest', intersect: false },
      plugins: {
        tooltip: {
          callbacks: {
            title: (ctx) => ctx[0].label,
            label: (ctx) => {
              const idx = ctx.dataIndex
              const profit = profits[idx]?.toLocaleString()
              const sell = sells[idx]?.toLocaleString()
              const buy = buys[idx]?.toLocaleString()
              const rate = rates[idx] !== null ? rates[idx].toFixed(2) + '%' : '-'
              return [
                `순이익: ${profit} 메소`,
                `판매: ${sell} 메소`,
                `구매: ${buy} 메소`,
                `수익률: ${rate}`
              ]
            }
          }
        }
      },
      scales: {
        y: {
          type: 'linear',
          position: 'left',
          title: { display: true, text: '순이익(메소)' }
        },
        y1: {
          type: 'linear',
          position: 'right',
          title: { display: true, text: '수익률(%)' },
          grid: { drawOnChartArea: false }
        }
      }
    }
  })
}

onMounted(() => {
  renderChart()
})
</script>

<style scoped>
.chart-container {
  background: var(--form-bg, #fff);
  border-radius: 12px;
  padding: 1.2rem 1.2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin: 1.2rem auto;
  font-size: 1rem;
  max-width: 1200px;
}
h2 {
  margin-bottom: 1.2rem;
}
canvas {
  width: 100% !important;
  max-width: 100%;
  height: 500px !important;
  margin: 0 auto;
  display: block;
}
.dark .chart-container {
  background: #23272f;
  color: #f3f3f3;
}
.light .chart-container {
  background: #fff;
  color: #181a1b;
}
</style> 