<template>
  <v-main class="bg-grey-lighten-4">
    <v-container fluid>
      <v-card class="mx-auto mt-4 rounded-lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 px-4">
          <v-icon icon="mdi-bank" size="large" class="mr-2" color="primary" />
          <span class="text-h5 font-weight-bold">예금 상품</span>
          <v-spacer />
          <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" label="검색" single-line hide-details density="compact" variant="outlined" class="max-width-200" />
        </v-card-title>

        <v-divider />

        <div v-if="finList.length > 0" class="custom-table-container">
          <v-data-table :headers="headers" :items="finList" :search="search" hover fixed-header height="calc(100vh - 250px)" class="financial-table elevation-0" :items-per-page="-1">
            <!-- 상품명에 RouterLink 추가 -->
            <template #item.fin_prdt_nm="{ item }">
              <router-link :to="`/product/${item.fin_prdt_cd}`" @click="setProduct(item)" class="text-decoration-none font-weight-medium text-primary">
                {{ item.fin_prdt_nm }}
              </router-link>
            </template>

            <!-- Footer 템플릿을 빈 값으로 오버라이드 -->
            <template #footer></template>
          </v-data-table>
        </div>
        <v-alert v-else type="info" class="mt-4">데이터가 없습니다.</v-alert>
      </v-card>
    </v-container>
  </v-main>
</template>

<script setup>
import { useFinStore } from "@/stores/financial";
import { onMounted, ref } from "vue";

const search = ref("");

const headers = [
  {
    title: "상품명",
    align: "start",
    key: "fin_prdt_nm",
    width: "150px",
  },
  {
    title: "은행명",
    align: "center",
    key: "kor_co_nm",
    width: "120px",
  },
  {
    title: "상품 코드",
    align: "center",
    key: "fin_prdt_cd",
    width: "120px",
  },
  {
    title: "가입 대상",
    align: "center",
    key: "join_member",
    width: "120px",
    sortable: true,
  },
  {
    title: "가입 방법",
    align: "end",
    key: "join_way",
    width: "100px",
    sortable: true,
  },
];

const store = useFinStore();
const finList = ref([]);
const setProduct = (item) => {
  store.setSelectedProduct(item);
};

onMounted(() => {
  store.getFins();
  finList.value = store.fin;
});
</script>

<style>
/* 전역 스타일로 설정 */
.v-data-table-footer {
  display: none !important;
}

.custom-table-container {
  /* 스크롤바 스타일링 */
  & ::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
  }

  & ::-webkit-scrollbar-track {
    background: #f1f1f1 !important;
    border-radius: 4px !important;
  }

  & ::-webkit-scrollbar-thumb {
    background: #c1c1c1 !important;
    border-radius: 4px !important;
  }

  & ::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8 !important;
  }
}
</style>

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
