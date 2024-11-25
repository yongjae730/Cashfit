<template>
  <v-card elevation="2" class="rounded-xl pa-4">
    <v-card-title class="d-flex align-center mb-4">
      <div class="d-flex align-center">
        <v-icon color="primary" class="mr-2">mdi-chart-bar</v-icon>
        상품 옵션 정보 및 차트
      </div>
      <!-- 차트 타입 전환 버튼 -->
      <v-btn-toggle v-model="chartType" color="primary" rounded="lg" mandatory>
        <v-btn value="line" variant="text">
          <v-icon>mdi-chart-line</v-icon>
          <span class="ml-1">그래프</span>
        </v-btn>
        <v-btn value="bar" variant="text">
          <v-icon>mdi-chart-bar</v-icon>
          <span class="ml-1">차트</span>
        </v-btn>
      </v-btn-toggle>
    </v-card-title>

    <!-- 요약 정보 카드 -->
    <div v-if="options.length > 0" class="mb-6">
      <div class="text-subtitle-1 font-weight-bold mb-3">상품 요약</div>
      <v-row>
        <v-col cols="12" md="4">
          <v-card class="stat-card">
            <div class="text-body-2 text-grey">최소 저축 기간</div>
            <div class="text-h5 font-weight-bold">{{ minTerm }}개월</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="stat-card">
            <div class="text-body-2 text-grey">최대 저축 기간</div>
            <div class="text-h5 font-weight-bold">{{ maxTerm }}개월</div>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <v-card class="stat-card">
            <div class="text-body-2 text-grey">최고 우대금리</div>
            <div class="text-h5 font-weight-bold">{{ maxRate }}%</div>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- 차트 -->
    <v-card class="chart-container pa-4">
      <canvas ref="chartCanvas"></canvas>
    </v-card>

    <!-- 상세 옵션 정보 -->
    <div v-if="options.length > 0" class="mt-6">
      <div class="text-subtitle-1 font-weight-bold mb-3">상세 옵션</div>
      <v-row>
        <v-col v-for="(option, index) in options" :key="index" cols="12" md="6" lg="4">
          <v-card class="option-card pa-4">
            <div class="mb-2">
              <v-chip v-if="option.rsrv_type_nm" :color="option.rsrv_type_nm === '정액적립식' ? 'primary' : 'success'" size="small" class="mb-2">
                {{ option.rsrv_type_nm }}
              </v-chip>
              <v-chip v-else color="info" size="small" class="mb-2">예금</v-chip>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-grey">저축 기간</span>
              <span class="font-weight-medium">{{ option.save_trm }}개월</span>
            </div>
            <div class="d-flex justify-space-between mb-2">
              <span class="text-grey">기본 금리</span>
              <span class="font-weight-medium">{{ option.intr_rate }}%</span>
            </div>
            <div class="d-flex justify-space-between" v-if="option.intr_rate !== option.intr_rate2">
              <span class="text-grey">최고 우대 금리</span>
              <span class="font-weight-bold">{{ option.intr_rate2 }}%</span>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
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
const chartType = ref("line");
let chartInstance = null;

// 계산된 속성 추가
const minTerm = computed(() => {
  return Math.min(...options.value.map((opt) => opt.save_trm));
});

const maxTerm = computed(() => {
  return Math.max(...options.value.map((opt) => opt.save_trm));
});

const maxRate = computed(() => {
  return Math.max(...options.value.map((opt) => opt.intr_rate2));
});

watch(chartType, () => {
  if (options.value.length > 0) {
    createChart(options.value);
  }
});

const createChart = (data) => {
  if (!chartCanvas.value) return;

  if (chartInstance) {
    chartInstance.destroy();
  }

  const allTerms = [...new Set(data.map((opt) => opt.save_trm))].sort((a, b) => a - b);
  const isDeposit = data[0]?.rsrv_type_nm === null;
  let datasets = [];

  if (isDeposit) {
    datasets = [
      {
        label: "기본 금리",
        data: allTerms.map((term) => {
          const opt = data.find((d) => d.save_trm === term);
          return opt ? opt.intr_rate : null;
        }),
        borderColor: "rgba(59, 130, 246, 1)",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        fill: chartType.value === "line",
        tension: 0.4,
      },
    ];

    if (data.some((opt) => opt.intr_rate !== opt.intr_rate2)) {
      datasets.push({
        label: "우대 금리",
        data: allTerms.map((term) => {
          const opt = data.find((d) => d.save_trm === term);
          return opt ? opt.intr_rate2 : null;
        }),
        borderColor: "rgba(99, 102, 241, 1)",
        backgroundColor: "rgba(99, 102, 241, 0.3)",
        fill: chartType.value === "line",
        tension: 0.4,
      });
    }
  } else {
    // 적금 데이터셋 생성...
    const regularSavings = data.filter((opt) => opt.rsrv_type_nm === "정액적립식");
    const flexibleSavings = data.filter((opt) => opt.rsrv_type_nm === "자유적립식");

    if (regularSavings.length > 0) {
      datasets.push(
        {
          label: "정액적립식 기본금리",
          data: allTerms.map((term) => {
            const opt = regularSavings.find((d) => d.save_trm === term);
            return opt ? opt.intr_rate : null;
          }),
          borderColor: "rgba(59, 130, 246, 1)",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          fill: chartType.value === "line",
          tension: 0.4,
        },
        {
          label: "정액적립식 우대금리",
          data: allTerms.map((term) => {
            const opt = regularSavings.find((d) => d.save_trm === term);
            return opt ? opt.intr_rate2 : null;
          }),
          borderColor: "rgba(99, 102, 241, 1)",
          backgroundColor: "rgba(99, 102, 241, 0.3)",
          fill: chartType.value === "line",
          tension: 0.4,
        }
      );
    }

    if (flexibleSavings.length > 0) {
      datasets.push(
        {
          label: "자유적립식 기본금리",
          data: allTerms.map((term) => {
            const opt = flexibleSavings.find((d) => d.save_trm === term);
            return opt ? opt.intr_rate : null;
          }),
          borderColor: "rgba(34, 197, 94, 1)",
          backgroundColor: "rgba(34, 197, 94, 0.1)",
          fill: chartType.value === "line",
          tension: 0.4,
        },
        {
          label: "자유적립식 우대금리",
          data: allTerms.map((term) => {
            const opt = flexibleSavings.find((d) => d.save_trm === term);
            return opt ? opt.intr_rate2 : null;
          }),
          borderColor: "rgba(16, 185, 129, 1)",
          backgroundColor: "rgba(16, 185, 129, 0.3)",
          fill: chartType.value === "line",
          tension: 0.4,
        }
      );
    }
  }

  chartInstance = new Chart(chartCanvas.value.getContext("2d"), {
    type: chartType.value,
    data: {
      labels: allTerms.map((term) => `${term}개월`),
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          align: "start",
          labels: {
            boxWidth: 20,
            padding: 20,
            usePointStyle: true,
            font: {
              size: 12,
            },
          },
        },
        tooltip: {
          mode: "index",
          intersect: false,
          callbacks: {
            label: function (context) {
              return `${context.dataset.label}: ${context.parsed.y}%`;
            },
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "금리 (%)",
            font: {
              weight: "bold",
            },
          },
          grid: {
            display: true,
            color: "rgba(0, 0, 0, 0.05)",
          },
        },
        x: {
          title: {
            display: true,
            text: "저축 기간",
            font: {
              weight: "bold",
            },
          },
          grid: {
            display: false,
          },
        },
      },
    },
  });
};

const fetchOptions = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/api/financials/financial-products-with-options/`);
    const product = res.data.find((item) => item.id === props.productId);
    if (product && product.options.length > 0) {
      options.value = product.options;
      createChart(product.options);
    }
  } catch (error) {
    console.error("옵션 데이터를 가져오는 중 오류 발생:", error);
  }
};

onMounted(() => {
  fetchOptions();
});
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 500px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 20px;
}

.stat-card {
  padding: 16px;
  background: linear-gradient(145deg, #ffffff, #f5f7fa);
  border: 1px solid #edf2f7;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
.stat-card {
  padding: 16px;
  background: linear-gradient(145deg, #ffffff, #f5f7fa);
  border: 1px solid #edf2f7;
}

.chart-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.option-card {
  background: white;
  border: 1px solid #edf2f7;
  transition: transform 0.2s;
}

.option-card:hover {
  transform: translateY(-2px);
}

canvas {
  max-width: 100%;
  height: 400px;
}
</style>
