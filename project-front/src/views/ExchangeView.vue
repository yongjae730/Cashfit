<template>
  <v-container class="py-8" style="margin-top: 40px">
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="64" width="4" class="mb-4" />
      <p class="text-h6 text-grey-darken-1">데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 데이터 렌더링 -->
    <div v-else>
      <div v-if="exchangeInfos.length > 0" class="exchange-content">
        <!-- 타이틀 섹션 -->
        <v-card class="mb-8 title-card" elevation="2">
          <div class="d-flex align-center pa-6 gradient-background">
            <v-avatar color="white" size="56" class="mr-6" elevation="2">
              <v-icon icon="mdi-currency-usd" size="32" color="primary" />
            </v-avatar>
            <div>
              <h1 class="text-h4 font-weight-bold text-white mb-1">환율 정보</h1>
              <p class="text-grey-lighten-4 mb-0">실시간 환율 정보 및 계산기</p>
            </div>
          </div>
        </v-card>

        <!-- 환율 리스트 -->
        <div class="mb-8">
          <ExchangeList :exchangeInfos="exchangeInfos" />
        </div>

        <!-- 계산기 -->
        <div class="calculator-section">
          <Calculator :exchangeInfos="exchangeInfos" />
        </div>
      </div>

      <!-- 데이터 없음 상태 -->
      <v-card v-else class="pa-6 text-center empty-state" elevation="2">
        <v-icon icon="mdi-alert-circle" size="48" color="grey" class="mb-4" />
        <p class="text-h6 text-grey-darken-1">환율 데이터가 없습니다.</p>
      </v-card>
    </div>
  </v-container>
</template>

<script setup>
import ExchangeList from "@/components/ExchangeList.vue";
import Calculator from "../components/Calculator.vue";
import { ref, onMounted } from "vue";
import { useExchangeStore } from "@/stores/exchange";

const exchangeInfos = ref([]);
const isLoading = ref(true);
const store = useExchangeStore();

onMounted(async () => {
  try {
    await store.getExchange();
    if (store.exchange.length > 0) {
      exchangeInfos.value = store.exchange;
    } else {
      swal({
        title: "실패",
        text: "데이터 로드 중 문제가 발생했습니다. 다시 시도해주세요.",
        icon: "error",
        button: "확인",
      });
    }
  } catch (error) {
    swal({
      title: "실패",
      text: "데이터 로드 중 문제가 발생했습니다. 다시 시도해주세요.",
      icon: "error",
      button: "확인",
    });
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.gradient-background {
  background: linear-gradient(135deg, #1a237e 0%, #0d47a1 100%);
  border-radius: 12px;
}

.title-card {
  border-radius: 16px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.title-card:hover {
  transform: translateY(-2px);
}

.exchange-content {
  animation: fadeIn 0.5s ease-out;
}

.calculator-section {
  animation: slideUp 0.5s ease-out;
}

.empty-state {
  border-radius: 16px;
  background: linear-gradient(to bottom right, #ffffff, #f8f9fa);
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

:deep(.v-card) {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
}

:deep(.v-progress-circular) {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
