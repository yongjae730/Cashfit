<template>
  <div>
    <div v-if="exchangeInfos.length > 0">
      <ExchangeList :exchangeInfos="exchangeInfos" />
    </div>
    <div v-if="exchangeInfos.length > 0">
      <Calculator :exchangeInfos="exchangeInfos" />
    </div>
  </div>
</template>

<script setup>
import ExchangeList from "@/components/ExchangeList.vue";
import Calculator from "../components/Calculator.vue";
import { ref, onMounted } from "vue";
import { useExchangeStore } from "@/stores/exchange";

const exchangeInfos = ref([]);
const store = useExchangeStore();
const loading = ref(true);

onMounted(async () => {
  try {
    await store.getExchange();
    if (store.exchange && store.exchange.exchange_rate) {
      exchangeInfos.value = store.exchange.exchange_rate;
    } else {
      console.error("환율 데이터가 비어 있습니다.");
    }
  } catch (error) {
    console.error("환율 데이터를 가져오는 중 오류 발생:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped></style>
