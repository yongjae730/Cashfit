<template>
  <v-main>
    <v-container fluid>
      <v-card class="mx-auto mt-4 rounded-lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 px-4">
          <v-icon icon="mdi-bank" size="large" class="mr-2" color="primary" />
          <span class="text-h5 font-weight-bold">금융 상품</span>
          <v-spacer />
          <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" label="검색" single-line hide-details
            density="compact" variant="outlined" class="max-width-200" />
        </v-card-title>

        <v-divider />

        <div v-if="finList.length > 0" class="custom-table-container">
          <v-data-table :headers="headers" :items="finList || []" :search="search" hover fixed-header
            height="calc(100vh - 250px)" class="financial-table elevation-1" :items-per-page="-1">
            <template #item.fin_prdt_nm="{ item }">
              <router-link :to="`/product/${item.fin_prdt_cd}`" @click="setProduct(item)"
                class="text-decoration-none font-weight-medium text-primary">
                {{ item.fin_prdt_nm }}
              </router-link>
            </template>

            <!-- 옵션 열 -->
            <template #item.options="{ item }">
              <ul>
                <li v-for="(option, index) in item.options" :key="index">
                  {{ option.intr_rate_type_nm }}: {{ option.intr_rate }}% ~ {{ option.intr_rate2 }}% ({{ option.save_trm
                  }}개월)
                </li>
              </ul>
            </template>
          </v-data-table>
        </div>
        <v-alert v-else type="info" class="mt-4">데이터가 없습니다.</v-alert>
      </v-card>
    </v-container>
  </v-main>
</template>

<script setup>
import axios from "axios";
import { useFinStore } from "@/stores/financial";
import { onMounted, ref } from "vue";

const store = useFinStore();
const setProduct = (item) => {
  store.setSelectedProduct(item);
};
const search = ref("");

const headers = [
  {
    title: "은행명",
    align: "center",
    value: "kor_co_nm",
    width: "80px",
  },
  {
    title: "상품명",
    align: "center",
    value: "fin_prdt_nm",
    width: "150px",
  },
  {
    title: "가입 대상",
    align: "center",
    value: "join_member",
    width: "120px",
  },
  {
    title: "특이사항",
    align: "center",
    value: "spcl_cnd",
    width: "150px",
  },
  {
    title: "옵션",
    align: "center",
    value: "options",
    width: "120px", // 옵션 열을 넓게 설정
  },
  {
    title: "종류", // 새로운 열 추가
    align: "center",
    value: "product_type_display",
    width: "80px"
  },
  {
    title: "기타",
    align: "center",
    value: "etc_note",
    width: "150px",
  },
];

const finList = ref([]);  // 금융 상품 목록

onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/financials/financial-products-with-options/");
    console.log("API 응답 데이터:", response.data); // 응답 확인
    if (Array.isArray(response.data)) {
      // 데이터 가공
      finList.value = response.data.map(item => {
        const productTypeDisplay = item.product_type === 0
          ? "예금"
          : item.options[0]?.rsrv_type_nm || "정보 없음"; // rsrv_type_nm 또는 기본값
        return {
          ...item,
          product_type_display: productTypeDisplay // 새 필드 추가
        };
      });
    } else {
      console.error("API 데이터 형식이 올바르지 않습니다:", response.data);
    }
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
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
  padding: 14px !important;
  font-weight: bold !important;
  color: rgba(0, 0, 0, 0.87) !important;
  font-size: 0.875rem !important;
}

:deep(.v-data-table-row:hover) {
  background-color: #f5f5f5 !important;
}

li {
  list-style-type: none;
}
</style>
