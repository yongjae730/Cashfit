import axios from "axios";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useExchangeStore = defineStore(
  "exchange",
  () => {
    const exchange = ref([]);
    const API_URL = "http://127.0.0.1:8000";
    const getExchange = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/financials/exchange-rate/`,
      })
        .then((res) => {
          console.log(res.data);
          exchange.value = res.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };
    return { exchange, getExchange };
  },
  { persist: true }
);
