<template>
  <v-main class="bg-grey-lighten-4">
    <v-container fluid>
      <v-card class="mx-auto mt-4 rounded-lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 px-4">
          <v-icon icon="mdi-chart-line-variant" size="large" class="mr-2" color="primary" />
          <span class="text-h5 font-weight-bold">실시간 금융 상품 현황</span>
          <v-spacer />
          <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" label="검색" single-line hide-details density="compact" variant="outlined" class="max-width-200" />
        </v-card-title>

        <v-divider />

        <v-data-table :headers="headers" :items="items" :search="search" hover fixed-header height="calc(100vh - 250px)" class="financial-table">
          <!-- 변화율 템플릿 -->
          <template #item.change="{ item }">
            <v-chip :color="item.change > 0 ? 'error' : 'info'" :class="{ 'font-weight-bold': true }" size="small" variant="tonal">
              <v-icon size="small" :icon="item.change > 0 ? 'mdi-arrow-up' : 'mdi-arrow-down'" start />
              {{ Math.abs(item.change).toFixed(2) }}%
            </v-chip>
          </template>

          <!-- 기간별 수익률 템플릿 -->
          <template #item.month1="{ item }">
            <span :class="getPerformanceColor(item.month1)">{{ item.month1.toFixed(2) }}%</span>
          </template>
          <template #item.month3="{ item }">
            <span :class="getPerformanceColor(item.month3)">{{ item.month3.toFixed(2) }}%</span>
          </template>
          <template #item.month6="{ item }">
            <span :class="getPerformanceColor(item.month6)">{{ item.month6.toFixed(2) }}%</span>
          </template>
          <template #item.year1="{ item }">
            <span :class="getPerformanceColor(item.year1)">{{ item.year1.toFixed(2) }}%</span>
          </template>

          <!-- 종목 코드 템플릿 -->
          <template #item.code="{ item }">
            <v-chip color="grey-darken-1" size="small" variant="flat" class="font-weight-medium">
              {{ item.code }}
            </v-chip>
          </template>
        </v-data-table>
      </v-card>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref } from "vue";

const search = ref("");

const headers = [
  {
    title: "자산명",
    align: "start",
    key: "name",
    width: "150px",
  },
  {
    title: "종목 코드",
    align: "center",
    key: "code",
    width: "120px",
  },
  {
    title: "실시간 변동률",
    align: "center",
    key: "change",
    width: "120px",
    sortable: true,
  },
  {
    title: "1개월",
    align: "end",
    key: "month1",
    width: "100px",
    sortable: true,
  },
  {
    title: "3개월",
    align: "end",
    key: "month3",
    width: "100px",
    sortable: true,
  },
  {
    title: "6개월",
    align: "end",
    key: "month6",
    width: "100px",
    sortable: true,
  },
  {
    title: "1년",
    align: "end",
    key: "year1",
    width: "100px",
    sortable: true,
  },
  {
    title: "시가 총액",
    align: "end",
    key: "market_cap",
    width: "120px",
  },
];

const items = ref([
  {
    name: "도지코인",
    code: "DOGE/KRW",
    change: 110.06,
    month1: 251.42,
    month3: 296.94,
    month6: 162.08,
    year1: 446.76,
    market_cap: "-",
  },
  {
    name: "크로노스",
    code: "CRO/KRW",
    change: 77.68,
    month1: 113.35,
    month3: 83.92,
    month6: 30.08,
    year1: 62.09,
    market_cap: "-",
  },
  {
    name: "수이",
    code: "SUI/KRW",
    change: 49.47,
    month1: 71.05,
    month3: 319.56,
    month6: 216.83,
    year1: 477.21,
    market_cap: "-",
  },
]);

const getPerformanceColor = (value) => {
  if (value > 0) return "text-error font-weight-bold";
  if (value < 0) return "text-info font-weight-bold";
  return "text-grey";
};
</script>

<style scoped>
.financial-table {
  font-family: "Roboto", sans-serif;
}

.max-width-200 {
  max-width: 200px;
}

:deep(.v-data-table) {
  background: transparent !important;
}

:deep(.v-data-table-header) {
  background-color: #f5f5f5 !important;
}

:deep(.v-data-table-header th) {
  font-weight: bold !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-size: 0.875rem !important;
}

:deep(.v-data-table-row:hover) {
  background-color: #f5f5f5 !important;
}
</style>
