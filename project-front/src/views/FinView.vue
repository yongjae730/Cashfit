<template>
  <v-main>
    <v-container fluid>
      <v-card class="mx-auto mt-4 rounded-lg" elevation="2">
        <v-card-title class="d-flex align-center py-4 px-4">
          <v-icon icon="mdi-bank" size="large" class="mr-2" color="primary" />
          <span class="text-h4 font-weight-bold">금융 상품</span>
        </v-card-title>

        <!-- 탭 추가 -->
        <v-tabs v-model="activeTab" background-color="primary" dark>
          <v-tab value="deposit">예금</v-tab>
          <v-tab value="saving">적금</v-tab>
        </v-tabs>

        <v-tabs-items v-model="activeTab">
          <v-tab-item value="saving">
            <v-card-title class="d-flex align-center py-4 px-4" style="height: 80px">
              <!-- 자유적립/정액적립 필터 -->
              <v-btn-toggle v-model="savingFilter" class="filter-buttons" v-if="activeTab === 'saving'">
                <v-btn value="freeSaving" style="padding: 0">
                  <v-icon color="green" size="24">mdi-piggy-bank</v-icon>
                  <span class="btn-text">자유적립식</span>
                </v-btn>
                <v-btn value="regularSaving" style="padding: 0">
                  <v-icon color="orange" size="24">mdi-calendar-text</v-icon>
                  <span class="btn-text">정액적립식</span>
                </v-btn>
              </v-btn-toggle>
              <v-spacer />
              <v-text-field v-model="search" prepend-inner-icon="mdi-magnify" label="검색" single-line hide-details density="compact" variant="outlined" style="max-width: 300px" />
            </v-card-title>
          </v-tab-item>
        </v-tabs-items>

        <v-divider />

        <!-- 단일 데이터 테이블 -->
        <div v-if="filteredList.length > 0" class="custom-table-container">
          <v-data-table :headers="headers" :items="filteredList" :search="search" hover fixed-header height="calc(100vh - 250px)" class="financial-table elevation-1" :items-per-page="-1">
            <template #item.fin_prdt_nm="{ item }">
              <router-link :to="`/product/${item.fin_prdt_cd}`" @click="setProduct(item)" class="text-decoration-none font-weight-medium text-primary">
                {{ item.fin_prdt_nm }}
              </router-link>
            </template>
            <template v-for="header in headers.slice(2)" :key="header.value" #[`item.${header.value}`]="{ item }">
              <div v-if="Array.isArray(item[header.value])">
                <ul>
                  <li v-for="(detail, index) in item[header.value]" :key="index" v-html="detail"></li>
                </ul>
              </div>
              <div v-else v-html="item[header.value]"></div>
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
import { ref, computed, onMounted } from "vue";
import { useFinStore } from "@/stores/financial";

const store = useFinStore();
const setProduct = (item) => {
  store.setSelectedProduct(item);
};

// 상태 및 검색 필터
const search = ref("");
const finList = ref([]); // API에서 받은 금융 상품 목록
const selectedFilter = ref([]); // 기존 필터 상태 (사용하지 않더라도 유지)
const activeTab = ref("deposit"); // 현재 선택된 탭 (예금/적금)
const savingFilter = ref(""); // 자유적립식/정액적립식 선택 필터
const headers = ref([
  { title: "상품명", value: "fin_prdt_nm", align: "center", width: "150px" },
  { title: "은행명", value: "kor_co_nm", align: "center", width: "80px" },
]);

// API 데이터 가져오기
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/financials/financial-products-with-options/");
    const products = response.data;

    // 모든 기간 추출 및 동적 헤더 생성
    const allTerms = new Set();
    products.forEach((product) => {
      if (Array.isArray(product.options)) {
        product.options.forEach((option) => {
          if (option.save_trm) {
            allTerms.add(`${option.save_trm}개월`);
          }
        });
      }
    });

    allTerms.forEach((term) => {
      headers.value.push({
        title: `${term} 일반/우대`,
        value: term,
        align: "center",
        width: "120px",
      });
    });

    // 데이터 매핑
    finList.value = products.map((item) => {
      let rsrvTypes = [];
      if (item.product_type === 0) {
        rsrvTypes = ["예금"]; // 예금인 경우
      } else if (item.options?.length) {
        rsrvTypes = item.options.map((option) => option.rsrv_type_nm).filter(Boolean); // 옵션에서 rsrv_type_nm 추출
      }

      // 중복 제거 및 문자열 결합
      const uniqueRsrvTypes = [...new Set(rsrvTypes)];

      return {
        ...item,
        rsrv_type_nm: uniqueRsrvTypes.join(", "), // 유형들을 문자열로 결합
      };
    });
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
});

// 데이터 매핑 및 동적 헤더에 따른 데이터 정리
const processedList = computed(() => {
  return finList.value.map((item) => {
    const row = { ...item };

    // 각 기간에 맞는 데이터를 추가
    if (Array.isArray(item.options)) {
      item.options.sort((a, b) => {
        // 자유적립식이 정액적립식보다 먼저 오도록 정렬
        if (a.rsrv_type_nm === "자유적립식" && b.rsrv_type_nm !== "자유적립식") {
          return -1;
        }
        if (a.rsrv_type_nm !== "자유적립식" && b.rsrv_type_nm === "자유적립식") {
          return 1;
        }
        return 0; // 동일한 경우 순서 유지
      });

      item.options.forEach((option) => {
        const term = `${option.save_trm}개월`;
        const type = option.rsrv_type_nm || "예금";

        // 기존 데이터에 유형별로 데이터를 병합
        if (!row[term]) {
          row[term] = [];
        }
        row[term].push(
          `<span style="color: black">${type} :</span> 
           <span style="font-weight: bold; color: #1a73e8">${option.intr_rate}%</span> 
           <span style="color: black">/</span> 
           <span style="font-weight: bold; color: #ff5722">${option.intr_rate2}%</span>`
        );
      });
    }

    return row;
  });
});

// 필터링된 목록
const filteredList = computed(() => {
  if (activeTab.value === "deposit") {
    // 예금 탭: 예금만 필터링
    return processedList.value.filter((item) => item.rsrv_type_nm.includes("예금"));
  }

  if (activeTab.value === "saving") {
    // 적금 탭: 자유적립/정액적립 필터 적용
    if (!savingFilter.value) {
      return processedList.value.filter((item) => item.rsrv_type_nm.includes("적립식")); // 적금 전체
    }

    // 자유적립/정액적립 필터 적용
    return processedList.value.filter((item) => item.rsrv_type_nm.includes(savingFilter.value === "freeSaving" ? "자유적립식" : "정액적립식"));
  }

  return processedList.value; // 기본 데이터 반환
});
</script>

<style lang="scss">
/* 전역 스타일 */
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

<style>
.v-table > .v-table__wrapper > table > tbody > tr > th,
.v-table > .v-table__wrapper > table > thead > tr > th,
.v-table > .v-table__wrapper > table > tfoot > tr > th {
  font-weight: 900 !important;
}
</style>

<style scoped>
.filter-buttons {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 16px; /* 버튼 간 간격 추가 (수정된 부분) */
}

.filter-buttons .v-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px; /* 버튼 내부 간격 조정 */
  min-width: 120px; /* 버튼 크기 균일화 */
}

.filter-buttons .btn-text {
  margin-left: 8px; /* 아이콘과 텍스트 사이 간격 추가 (수정된 부분) */
  font-size: 16px;
  font-weight: bold;
}

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

.filter-buttons {
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 16px; /* 버튼 간 간격 추가 */
}

.filter-buttons .v-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  min-width: 120px;
}

.filter-buttons .btn-text {
  margin-left: 8px;
  font-size: 16px;
  font-weight: bold;
}
li {
  list-style-type: none;
}
</style>
