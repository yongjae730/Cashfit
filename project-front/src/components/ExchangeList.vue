<template>
  <v-container class="top">
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <v-carousel height="400px" v-else :items-per-view="1" cycle interval="6000" hide-delimiters show-arrows="hover">
      <v-carousel-item v-for="(group, index) in groupedExchangeInfos" :key="index">
        <v-row>
          <ExchangeItem v-for="exchange in group" :key="exchange.cur_unit" :exchange="exchange" @show-details="showDetailModal" />
        </v-row>
      </v-carousel-item>
    </v-carousel>

    <ExchangeDetail v-model:show="isDetailModalOpen" :exchange="selectedExchange" />
  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import ExchangeItem from "@/components/ExchangeItem.vue";
import ExchangeDetail from "@/components/ExchangeDetail.vue";
import { useExchangeStore } from "@/stores/exchange";

const loading = ref(true);
const store = useExchangeStore();
const groupedExchangeInfos = ref([]);
const selectedExchange = ref(null);
const isDetailModalOpen = ref(false);

// props 정의
const props = defineProps({
  exchangeInfos: {
    type: Array,
    default: () => [],
  },
});

const chunkArray = (array, size) => {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
};
// onMounted에서 데이터 사용
watch(
  () => props.exchangeInfos,
  (newExchangeInfos) => {
    if (newExchangeInfos && newExchangeInfos.length > 0) {
      groupedExchangeInfos.value = chunkArray(newExchangeInfos, 3);
      loading.value = false;
    } else {
      // console.error("환율 데이터가 비어 있습니다.");
      loading.value = false;
    }
  },
  { immediate: true } // 컴포넌트가 마운트될 때 바로 실행되도록 설정
);

const showDetailModal = (exchange) => {
  selectedExchange.value = exchange;
  isDetailModalOpen.value = true;
};
</script>

<style scoped>
/* 캐러셀 스타일 */
.v-carousel {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 12px;
  margin-top: 20px;
}

.v-carousel-item {
  display: flex;
  align-items: center;
  justify-content: center;
}

.v-col {
  display: flex;
  justify-content: center;
}

.top {
  margin-top: 64px;
}

/* 카드 스타일 */
.exchange-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 240px; /*고정 높이*/
  background-color: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
}

.exchange-card:hover {
  transform: translateY(-4px);
  box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.15);
}

.exchange-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.exchange-rate {
  font-size: 1rem;
  color: #555;
  margin-bottom: auto; /* 하단 여백 추가 */
}

.exchange-actions {
  margin-top: auto; /* 버튼 위치 고정 */
}
</style>
