<template>
  <v-container>
    <!-- 로딩 상태 표시 -->
    <v-progress-linear v-if="loading" indeterminate color="primary" />

    <!-- 캐러셀 -->
    <v-carousel v-else hide-delimiters height="360px" show-arrows>
      <v-carousel-item v-for="(group, index) in groupedExchangeInfos" :key="index">
        <v-row class="justify-center">
          <v-col cols="12" md="4" lg="3" v-for="exchange in group" :key="exchange.cur_unit">
            <v-card class="exchange-card" outlined>
              <v-card-title class="exchange-title">
                <div>{{ exchange.cur_nm }} ({{ exchange.cur_unit }})</div>
              </v-card-title>
              <v-card-subtitle class="exchange-rate">매매기준율: {{ exchange.deal_bas_r }}</v-card-subtitle>
              <v-card-actions class="exchange-actions">
                <v-btn color="primary" text small @click="showDetailModal(exchange)">상세 보기</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-carousel-item>
    </v-carousel>

    <!-- 상세 정보 모달 -->
    <ExchangeDetail v-if="isDetailModalOpen" :exchange="selectedExchange" v-model:show="isDetailModalOpen" />
  </v-container>
</template>

<script setup>
import { exchangeStore } from "@/stores/exchange";
import { ref, onMounted } from "vue";
import ExchangeDetail from "@/components/ExchangeDetail.vue";

const exchangeInfos = ref([]); // 환율 정보 배열
const groupedExchangeInfos = ref([]); // 4개씩 그룹화된 환율 정보
const selectedExchange = ref(null); // 선택된 환율 정보
const isDetailModalOpen = ref(false); // 모달 표시 여부
const loading = ref(true); // 로딩 상태
const store = exchangeStore(); // Store

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(async () => {
  try {
    await store.getExchange();
    if (store.exchange && store.exchange.exchange_rate) {
      exchangeInfos.value = store.exchange.exchange_rate;

      // 데이터를 4개씩 그룹화
      groupedExchangeInfos.value = chunkArray(exchangeInfos.value, 4);
    } else {
      console.error("환율 데이터가 비어 있습니다.");
    }
  } catch (error) {
    console.error("환율 데이터를 가져오는 중 오류 발생:", error);
  } finally {
    loading.value = false; // 로딩 완료
  }
});

// 4개씩 데이터 그룹화
const chunkArray = (array, size) => {
  const result = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
};

// 상세 모달 열기 함수
const showDetailModal = (exchange) => {
  selectedExchange.value = exchange; // 선택된 환율 정보를 설정
  isDetailModalOpen.value = true; // 모달을 표시
};
</script>

<style scoped>
/* 캐러셀 스타일 */
.v-carousel {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 16px;
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

/* 카드 스타일 */
.exchange-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  height: 240px; /* 고정 높이 */
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
