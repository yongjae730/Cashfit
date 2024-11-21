import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useExchangeStore = defineStore(
  "exchange",
  () => {
    const exchange = ref([]);
    const loading = ref(true); // 로딩 상태 추가
    const API_URL = "http://127.0.0.1:8000";

    const getExchange = async function () {
      loading.value = true; // API 호출 시작 시 로딩 시작
      try {
        const res = await axios.get(`${API_URL}/api/financials/exchange-rate/`);
        exchange.value = res.data;
      } catch (error) {
        console.log(error);
      } finally {
        loading.value = false; // API 호출 완료 시 로딩 종료
      }
    };

    return { exchange, getExchange, loading };
  },
  { persist: true }
);
