<template>
  <div class="saving-container">
    <div v-if="isLoading" class="loading-container">
      <v-progress-circular indeterminate color="primary" />
      <p>데이터를 불러오는 중입니다...</p>
    </div>

    <div v-else-if="topSaving.length > 0" class="carousel-container">
      <v-carousel hide-delimiters show-arrows="hover" cycle height="300px">
        <v-carousel-item v-for="(saving, index) in topSaving" :key="index">
          <v-card class="saving-card">
            <v-card-title class="saving-title">
              <div class="bank-info">
                <span class="bank-name">{{ saving.product?.kor_co_nm || "정보 없음" }}</span>
                <span class="product-name">{{ saving.product?.fin_prdt_nm || "정보 없음" }}</span>
              </div>
            </v-card-title>
            <v-card-text class="saving-details">
              <div class="details-section">
                <h3>예금 정보</h3>
                <ul>
                  <li>
                    <v-icon icon="mdi-bank" class="mr-2" />
                    <span>{{ saving.product?.kor_co_nm || "정보 없음" }}</span>
                  </li>
                  <li>
                    <v-icon icon="mdi-file-document" class="mr-2" />
                    <span>{{ saving.product?.fin_prdt_nm || "정보 없음" }}</span>
                  </li>
                </ul>
              </div>
              <div class="details-section">
                <h3>금리 정보</h3>
                <ul>
                  <li>
                    <v-icon icon="mdi-chart-line" class="mr-2" />
                    <span>
                      기본 금리:
                      <span class="rate">{{ saving.option?.intr_rate || "정보 없음" }}%</span>
                    </span>
                  </li>
                  <li>
                    <v-icon icon="mdi-star-outline" class="mr-2" />
                    <span>
                      우대 금리:
                      <span class="rate-highlight">{{ saving.option?.intr_rate2 || "정보 없음" }}%</span>
                    </span>
                  </li>
                  <li>
                    <v-icon icon="mdi-calendar-clock" class="mr-2" />
                    <span>
                      저축 기간:
                      <span class="term">{{ saving.option?.save_trm || "정보 없음" }}개월</span>
                    </span>
                  </li>
                </ul>
              </div>
            </v-card-text>
          </v-card>
        </v-carousel-item>
      </v-carousel>
    </div>

    <div v-else class="no-data">
      <p>표시할 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";

const topSaving = ref([]);
const isLoading = ref(true);

const fetchData = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/api/financials/financial-products/deposit_top_rate/");
    const sortedData = response.data.sort((a, b) => a.option.save_trm - b.option.save_trm);
    topSaving.value = sortedData;
  } catch (error) {
    console.error("데이터 로드 실패:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchData();
});
</script>

<style scoped>
.saving-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
}

.carousel-container {
  margin-top: 20px;
}

.saving-card {
  padding: 20px;
  border-radius: 12px;
  background-color: #ffffff;
  border: 1px solid #eaeaea;
}

.saving-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.bank-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.bank-name {
  font-size: 16px;
  font-weight: bold;
}

.product-name {
  font-size: 14px;
  color: #888;
}

.saving-details {
  display: flex;
  justify-content: space-between;
}

.details-section h3 {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

.details-section ul {
  list-style: none;
  padding: 0;
}

.details-section ul li {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
}

.details-section ul li .rate {
  color: #1a73e8;
  font-weight: bold;
}

.details-section ul li .rate-highlight {
  color: #ff5722;
  font-weight: bold;
}

.details-section ul li .term {
  color: #4caf50;
  font-weight: bold;
}

.no-data {
  margin-top: 50px;
  font-size: 16px;
  color: #888;
}
</style>
