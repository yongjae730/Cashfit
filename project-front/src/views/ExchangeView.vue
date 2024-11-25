<template>
  <div>
    <!-- 로딩 상태 -->
    <div v-if="isLoading" class="text-center">
      <v-progress-circular indeterminate color="primary" />
      <p>데이터를 불러오는 중입니다...</p>
    </div>

    <!-- 데이터 렌더링 -->
    <div v-else>
      <div v-if="exchangeInfos.length > 0">
        <ExchangeList :exchangeInfos="exchangeInfos" />
      </div>
      <div v-if="exchangeInfos.length > 0">
        <Calculator :exchangeInfos="exchangeInfos" />
      </div>
      <p v-else>환율 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import ExchangeList from "@/components/ExchangeList.vue";
import Calculator from "../components/Calculator.vue";
import { ref, onMounted } from "vue";
import { useExchangeStore } from "@/stores/exchange";

const exchangeInfos = ref([]);
const isLoading = ref(true); // 단일 로딩 상태 변수
const store = useExchangeStore();

onMounted(async () => {
  try {
    await store.getExchange();
    if (store.exchange.length > 0) {
      // store.exchange는 배열임
      exchangeInfos.value = store.exchange; // 데이터를 직접 할당
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
    isLoading.value = false; // 로딩 상태 종료
  }
});
</script>

<style scoped></style>
