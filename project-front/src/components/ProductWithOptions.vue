<template>
  <v-card elevation="2" class="rounded-xl pa-4">
    <v-card-title>
      <v-icon color="primary" class="mr-2">mdi-chart-bar</v-icon>
      상품 옵션 정보 및 차트
    </v-card-title>
    <v-card-text>
      <!-- 옵션 정보 -->
      <div v-if="options.length > 0">
        <v-row>
          <v-col v-for="(option, index) in options" :key="index" cols="12" md="6" lg="4">
            <v-card class="pa-4 mb-4">
              <strong>기간:</strong>
              {{ option.save_trm }}개월
              <br />
              <strong>기본 금리:</strong>
              {{ option.intr_rate }}%
              <br />
              <strong>최고 우대 금리:</strong>
              {{ option.intr_rate2 }}%
            </v-card>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <p>옵션 정보를 로드하는 중...</p>
      </div>

      <!-- 차트 -->
      <v-card class="mt-6">
        <canvas ref="chartCanvas"></canvas>
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";
import axios from "axios";

Chart.register(...registerables);

const props = defineProps({
  productId: {
    type: Number,
    required: true,
  },
});

const options = ref([]);
const chartCanvas = ref(null);
let chartInstance = null;

// 옵션 데이터를 가져오기
const fetchOptions = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/financials/financial-products-with-options/`);
    const product = res.data.find((item) => item.id === props.productId);
    if (product && product.options.length > 0) {
      options.value = product.options;
      createChart(product.options); // 차트 생성
    } else {
      console.error("옵션 정보가 없습니다.");
    }
  } catch (error) {
    console.error("옵션 데이터를 가져오는 중 오류 발생:", error);
  }
};

// 차트 생성
const createChart = (data) => {
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  const labels = data.map((option) => `${option.save_trm}개월`);
  const baseRates = data.map((option) => option.intr_rate);
  const maxRates = data.map((option) => option.intr_rate2);

  chartInstance = new Chart(chartCanvas.value.getContext("2d"), {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "기간 별 금리",
          data: baseRates,
          backgroundColor: "rgba(54, 162, 235, 0.7)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
        {
          label: "최고 우대 금리",
          data: maxRates,
          backgroundColor: "rgba(255, 99, 132, 0.7)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "금리 (%)",
          },
        },
        x: {
          title: {
            display: true,
            text: "저축 기간",
          },
        },
      },
    },
  });
};

// 마운트 후 데이터 가져오기
onMounted(() => {
  fetchOptions();
});
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
