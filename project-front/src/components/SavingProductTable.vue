<template>
  <div>
    <div v-if="isLoading" class="text-center">
      <v-progress-circular indeterminate color="primary" />
      <p>데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 적금 정보 -->
    <div v-else-if="topSaving.length > 0" class="p-4 mb-6">
      <h2>적금 추천 받고 싶니?</h2>
      <v-carousel hide-delimiters height="400px" cycle show-arrows="hover">
        <v-carousel-item v-for="(saving, index) in topSaving" :key="index">
          <v-card class="expanded-details-card">
            <v-card-title class="bg-blue-lighten-5 justify-space-between">
              <RouterLink :to="{ name: 'fin' }" class="text-decoration-none font-weight-medium">더 보기</RouterLink>
            </v-card-title>

            <v-card-text class="pa-6">
              <v-row>
                <v-col cols="12" md="6">
                  <h3 class="text-h6 mb-4">상품 정보</h3>
                  <v-list>
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-bank" class="mr-2" />
                      </template>
                      <v-list-item-title>은행명</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.product?.kor_co_nm || "정보 없음" }}</span>
                      </template>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-file-document" class="mr-2" />
                      </template>
                      <v-list-item-title>상품명</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.product?.fin_prdt_nm || "정보 없음" }}</span>
                      </template>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-calendar" class="mr-2" />
                      </template>
                      <v-list-item-title>설명</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.product?.etc_note || "정보 없음" }}</span>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-col>
                <v-col cols="12" md="6">
                  <h3 class="text-h6 mb-4">금리 정보</h3>
                  <v-list>
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-chart-line" class="mr-2" />
                      </template>
                      <v-list-item-title>기본 금리</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.option?.intr_rate || "정보 없음" }}</span>
                      </template>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-star-outline" class="mr-2" />
                      </template>
                      <v-list-item-title>우대 금리</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.option?.intr_rate2 || "정보 없음" }}</span>
                      </template>
                    </v-list-item>
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon icon="mdi-calendar-clock" class="mr-2" />
                      </template>
                      <v-list-item-title>기간</v-list-item-title>
                      <template v-slot:append>
                        <span class="font-weight-medium">{{ saving.option?.save_trm || "정보 없음" }} 개월</span>
                      </template>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-carousel-item>
      </v-carousel>
    </div>

    <div v-else class="text-center">
      <p>표시할 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

// 예금 정보 관련 데이터
const topSaving = ref([]);
const isLoading = ref(true);

const fetchSaving = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:8000/api/financials/financial-products/saving_top_rate/");

    const sortedData = res.data.sort((a, b) => a.option.save_trm - b.option.save_trm);
    topSaving.value = sortedData;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};
// API 호출
onMounted(() => {
  fetchSaving();
});
</script>
