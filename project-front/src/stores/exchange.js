import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useExchangeStore = defineStore(
  "exchange",
  () => {
    const exchange = ref([]); // 환율 데이터
    const loading = ref(true); // 로딩 상태
    const API_URL = "http://127.0.0.1:8000/api/financials/exchange-rate/";

    // 환율 데이터 가져오기
    const getExchange = async () => {
      try {
        const response = await axios.get(API_URL);
        exchange.value = response.data.exchange_rate; // 데이터 저장
      } catch (error) {
        console.error("API 호출 중 오류:", error);
      }
    };
    return { exchange, getExchange, loading };
  },
  { persist: true }
);
